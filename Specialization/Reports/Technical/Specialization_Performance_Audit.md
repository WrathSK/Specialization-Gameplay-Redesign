# Specialization Performance Audit — B067.93 / B068.95

Document Owner: Codex
Document State: READ_ONLY_AUDIT_COMPLETE / PERFORMANCE_BLOCKER_UNRESOLVED
Audit Date: 2026-09-13
Design: D0025 ACCEPTED（未修改）
Scope: 完整B067.93保留运行源码；核对当前B068.95差异。不是修复版、不是部署验收。

## 用户摘要

本轮只读检查了事件、建筑/Property写入、网络重建、缓存、重试、监听生命周期及Git历史。只新建本报告；未改源码、Design、Architecture、Status、游戏配置或部署文件，未启动游戏、未运行会写文件的测试。

最强线索是：普通单位任务也会把商路状态标成失效；尚未重读路线就把“不可用”发到Gameplay，下游撤销收益建筑；读回相同路线后又恢复建筑。底层写入函数大多有差异检查，但它们收到的目标值在反复变化。因此“每次移动都触发城市建筑更新”有具体代码路径可解释，不能只给建筑setter加一次相等判断了事。

第二个问题是多个通用事件和定时器执行全城扫描，且查询单城的网络来源时又重建整个网络。第三个问题是这些后台读数请求、建筑写入和通用发布事件之间存在反馈风险；下一阶段必须测是否持续产生后续事件/请求，而不能以一次模拟成功认定生命周期安全。

70+GB进程内存是用户实机报告；静态检查没有定位到能直接证明该数量的单一泄漏。发现无上限的施工队永久收据/DEV生成账本、未清理历史城市key的若干缓存，但它们并不是每次普通单位移动追加。大量临时表/字符串、原生Modifier/事件队列是否积压仍未知。

当前BLOCKED（正常游玩被严重性能问题阻塞，需要定位和修复）；原有逐项玩法PASS不等于长局稳定。用户现在无需操作，不要求继续游玩当前异常版本。建议下一阶段先隔离错误的商路失效信号与撤销/恢复链，再用固定大小计数器验证，不先扩展UI或玩法。

## 1. 证据等级、范围与限制

- STATIC_CONFIRMED：本报告所列代码路径、守卫、循环与容器证据；不等于Civ VI运行通过。
- USER_GAME_TEST_FAIL：用户报告前期End Turn变慢、约T40卡死、进程70+GB、普通单位移动伴随城市建筑更新。未拿到该长局逐事件轨迹/内存profile，不能断言每一个回调的原生发射次序。
- 本轮没有LOCAL_SIMULATION_PASS或修复后USER_GAME_TEST_PASS。读代码不能替代生命周期压测。
- 把B067.93作为主基准：`local/before-b068/Mod`，与其既有sha256.json逐文件核对。B060.85只作比较点，不是已知性能良好版本。
- 当前实际源码/部署是B068.95；不能误称仍在运行B067.93。核心嫌疑链在B067.93与当前源码均存在。
- 文中未给每秒实际调用次数：频率取决于引擎事件发射、玩家数、城市数和当前单位。列出的是触发上界结构/静态成本，不伪造profiling数字。
- 附录定位以B067.93备份内文件行号为准；该冻结副本位于仓库`local/`，不应修改。文件名中的旧B0xx编号不代表当前未启用；部分注释仍写“未接入收益”，实际调用已接入。

## 2. 按严重度排序

| 严重度 | 嫌疑 | 精确证据 | 当前判断 |
|---|---|---|---|
| P0 likely | 所有单位操作误作商路dirty，并立即撤销网络 | TradeRouteProbe末尾监听无单位/玩家过滤；BackgroundRoutes:117–123清空snapshot并render；NetworkSender:signature包含signal/generation/status；NetworkBridge:21、25、53–56 | 可静态走通“无真实路线变化→清空→重建→建筑撤销/恢复”；最贴合移动声效 |
| P0 likely | 高频全城扫描叠加，单城网络查询重复全局derive | CopyYieldRefresh通用publish/playback；DiscountEligibility；StandardizationDiscount:49–69；NetworkBridge:96/106/127查询内derive；CommerceConvergence:56起遍历所有Players/cities | CPU/临时分配热点明确；随城市/来源/玩家数放大 |
| P1 plausible（需优先计数） | UI脚本请求→Gameplay建筑变更→GameCore通知→UI再读/发请求反馈 | BackgroundRoutes render→sendNetwork；Copy/Discount/GPP后台EXECUTE_SCRIPT；NetworkBridge Receive→Audits；sender成功后才写last；单模块busy非跨事件合并 | 能构成反馈图；不能仅据图称已证明无限递归或70GB根因 |
| P1 plausible | 每回合读数失效造成零→原值的额外写入 | Network要求turn/signal一致；Discount样本turn/revision；Copy/Dialogue/GWA样本turn | 即使真收益未变也可能撤销再恢复；AI回合多次Audit放大成本 |
| P1 plausible | 选中移民/施工队的高频后台目标扫描 | UnitPanelActions .2秒UI更新、约.5秒ACTION_VIEW；UnitTargets刷新合法目标；UnitTargetMarkers约5秒补采样 | 与单位操作场景吻合，但非所有普通单位的主解释 |
| P1 plausible | 旧探针/整表清理继续驻留，初始化规模大 | NetworkBoost旧fractional/整数/test全族cleanup；Dialogue/GWA cleanup；Commerce全世界48bit族检查 | 冷启动/城市转移额外负担；不是每帧无限增长证据 |
| P1 plausible / 长期风险 | 无界动作账本、历史城市缓存 | UnitActions Player receipts与DEV spawn；多个pid:city缓存无回收 | 明确无固定条数上限，但与普通移动不直接相关 |
| Low probability（现有静态证据） | 自动继承模块目前造成事件风暴 | Gameplay:474 InheritanceIsolation=true，三模块未Start，OnPermanentCityWrite=nil | 代码在目录中不等于运行；保持隔离 |
| Low probability | Potential可见建筑不停切换 | B067无此建筑；B068使用UI/CityPotential只读标识，不是建/拆Building | 排除“新Potential镜像建筑”为这条路径的写入者 |
| 未证实 | 每次打开面板重复注册、每次移动无限历史追加 | UI通常Init一次+Shutdown移除；事件日志有32/64上限；未发现打开按钮内反复Add | 不可宣布不存在原生context生命周期泄漏；需有限计数验证 |

## 3. Unit Move → City Center：调用图与幂等性

```text
普通单位任务开始/结束（实际move触发这些事件的频度须计数）
  ├─ Gameplay TradeRouteProbe：无过滤，RouteSignalRevision++
  │    └─ Lv3Effects.Audit → ConnectedKinds拒绝旧signal → 商业III所需carrier变空
  └─ UI BackgroundRoutes：相同UnitOperation事件 / observeGame发现signal变化
       → mark：UNKNOWN、snapshot=nil → render → NetworkSender(Valid=0)
       → Gameplay NetworkBridge.Receive：b.routes/sources/centers/recipients=nil
       → Lv3Effects / StandardizationDiscount / NetworkBoost / CommerceConvergence.Audit
       → 对已有有效网络收益的城市：desired变0/空 → RemoveBuilding
       → publish/playback/SystemUpdate flush → collect当前路线（可能与之前完全相同）
       → COMPLETE_UI_SHADOW、新generation → NetworkSender(Valid=1)
       → derive → Audits → CreateBuilding恢复
       → 原生城市/Modifier/UI更新（具体声效源需要计数/原生观察确认）
```

`NetworkBoostInteger.sql`、`CommerceConvergence.sql`、`Dialogue.sql`、`GreatWorkAdjacency.sql`均使用City Center内部建筑；Boost还挂HD Player Property Modifier。InternalOnly并不承诺建/拆时完全无UI/原生更新。

**结论：发现系统层面的非幂等往返，不是普遍存在无条件Remove(old)/Add(same)。**例如目标原本4，普通任务无真实网络变化却产生4→0→4；底层每次比较都认为需写。若从未有网络收益且目标始终0，该链不必产生实际Building写入；不能声称每一个单位移动一定建/拆。

补充风险：StandardizationDiscount:35移除依据本地applied集合而非再次HasBuilding；若外部已经移除，可能重复请求删除一次，但本地key随后删除。这不是当前最强反复写根因。

```text
潜在跨context反馈（非已证无限循环）
建筑写 → GameCore publish/playback → Copy/Discount/Routes UI刷新
     → EXECUTE_SCRIPT → Gameplay Audit/写建筑 → 后续GameCore事件 ...
```

单模块busy只能防当次同步重入，不防任务排队后反复执行。NetworkSender在Request成功返回后才last=signature，缺少请求发出前的同签名in-flight保护；需测试原生是否同步重入/积压，不能凭pcall成功当作ACK。

## 4. End Turn / Route / City四条路径

### B. End Turn

```text
PlayerTurnActivated + PlayerTurnDeactivated（不少模块不筛本地玩家）
 → TradeRouteProbe全单位候选扫描（仅测试玩家）
 → BackgroundRoutes mark/dispatch；旧turn网络不可用
 → Housing/GPP/Lv3/Lv4/Crew/Copy/Dialogue/Commerce等独立Audits
 → 当前turn的UI样本未到时，部分能力desired=0
 → 新routes/copy/discount/works样本返回 → 再Audits/恢复carrier
```

没有统一的“本回合一个稳定输入版本完成后再结算”。同一回合边界会触发多套扫描；异步样本到达顺序可造成额外写入。

### C. Route dirty

```text
实际Route/War/City事件 + 过宽的UnitOperation + 每10秒fallback
 → UNKNOWN先发送 → 全城市GetOutgoingRoutes → normalize/dedupe
 → 网络Receive（最多128routes/16KB）→ derive
 → 每个RecipientSources/ConnectedKinds/National查询再derive
 → 同一输入版本被多个收益模块重复查询/结算
```

后台直接读取UI上下文数据符合用户批准来源；问题在本Mod调度/失效/应用，不是“必须打开BTS”或BTS不可信。下一阶段不改来源合同，也不能将真实结束/掠夺路线长期保留。需要区分“正在重新核对”和“权威证明路线已移除”，完整快照验证后按差异发布。

### D. City / Building

```text
CityBuilt / OnDistrictConstructed
 → Binding / CompletionRecord / Journal / CityFlow建立或推进永久事实
 → EffectiveFacts读取Identity/Potential/总督
 → Lv1/Lv2/Lv3/Lv4/Crew访问marker按desired差异写
OnBuildingConstructed / CityBuildingsChanged（各模块订阅名不同）
 → Housing/GPP/Industry/Standardization/其它Audit
 → 内部建筑如引发原生通用发布 → UI全城采样 → 后续Audit
```

Standardization账本按合格真实建筑增量记录；未发现每次Unit Move直接提高Potential或写模板。不能把各个`BuildingConstructed`/`OnBuildingConstructed`/`CityBuildingsChanged`名称当成同一个原生事件；哪些由CreateBuilding发射仍需计数。Governor条件通过数据库Effect调整Property，不是Lua不停创建Governor marker。

## 5. 高频事件表（精确注册清单见附录A）

| Event / timer | Context / handler | 频率性质 | 扫描/写入 |
|---|---|---|---|
| UnitOperationStarted / Deactivated / OperationsCleared / UnitRemovedFromMap | Game TradeRouteProbe；UI BackgroundRoutes | 每相应单位任务，无商人或owner过滤 | 改signal、立即网络失效、后续全routes与收益建筑 |
| TradeRouteActivityChanged / Added/Removed / War / CityAdded/Removed | UI BackgroundRoutes；Game probe子集 | 路线/战争/城市事件 | mark并立即发送invalid；完整采样 |
| GameCoreEventPublishComplete / PlaybackComplete | BackgroundRoutes | 通用高频 | 即便不dirty也生成报告字符串/render/send签名检查 |
| 同上 | CopyYieldRefresh、IndustryRefresh、DiscountEligibility | 通用高频 | 全城/区域/可购买建筑扫描；部分签名去重在扫描之后 |
| GameCoreEventPublishComplete | Game StandardizationDiscount.Audit | 通用高频 | 双城市循环；每城Network derive、模板/分类、Building reconcile |
| SystemUpdateUI | BackgroundRoutes；Copy/Industry/Discount/Boost初始补采样；GPP flush；Dialogue有界ACK处理 | UI系统通知 | dirty/初始化条件各异；并非全部每帧写，但失败条件可一直成立 |
| PlayerTurnActivated/Deactivated | 多Gameplay Audits及UI采样 | 每玩家turn边界；不少handler无pid过滤 | 本玩家全城甚至全世界城市再扫；旧turn失效→零→恢复风险 |
| CityWorker/Focus/Population / Governor系列 | GPP/Lv3/Lv4/Housing/Copy/Commerce等 | 人口/总督变化，多个监听并行 | 读取专家、facts、建筑族；变更后写 |
| OnDistrict/OnBuildingConstructed / CityBuilt / transfer | 多模块 | 城市建设/资格/所有权 | 永久事实有限写；大量Audit与cleanup；继承仍隔离 |
| .25秒、10秒fallback | BackgroundRoutes SetUpdate | 活跃UIcontext定时；空context回调可靠性已有历史限制 | render；10秒主动UNKNOWN再扫描，即便路线未变 |
| 1秒 | CopyYieldRefresh | 后台定时 | 全区域×6yield读；签名不同才请求 |
| .2秒 / 约.5秒 | UnitPanelActions | 选中单位/动作UI | 重排布局；选中Settler/Crew刷新只读行动状态/目标 |
| .25秒 / 约5秒 | B067 UnitTargetMarkers | 选中可用单位 | 重采目标/重建显示；不是持续创建无界实例 |
| B068约2秒 | CityPotential | 仅选中城市 | 只读城市facts，无建筑/Property写；本轮暂停改进 |

只读命令不等于零性能影响：经UI.RequestPlayerOperation进入Gameplay的读数，也可能产生通用游戏事件。

## 6. Building / Marker完整写入族

以下族名缩写对应源文件构造的完整BUILDING_SPC_* ID；逐写入行见附录B。全部建筑原生状态随存档持久，派生权威仍在Property/游戏事实；**可能触发城市更新：是（发生实际建/拆时）**。正常无变更刷新应无写；表中“局部幂等”不保证上游输入不振荡。

| Building / marker family | 用途 / writer | 触发 | 每刷新remove/add? / 幂等 |
|---|---|---|---|
| DEV Research/Culture/Commerce SUPPORT | ResearchSupport，常数Lv1 | load/turn/新城/区域/转移及显式Audit | Has差异守卫；局部幂等 |
| DEV INDUSTRY_LV1各值 | IndustrySupport，基础相邻Lv1 | UI base样本、turn、区域/改良/专家变化 | 守卫；样本失败/恢复可变化 |
| DEV LV2_HOUSING各值 | Lv2Housing | 总督/建筑/turn/city | 守卫 |
| DEV GPP四类bit | Lv2GPP | 专家/总督/turn + GPP_DIRTY | 守卫 |
| DEV LV3四类、IND_GOLD | Lv3Support | 总督/区域/建筑/turn | 守卫 |
| B038人口R/C、商业III网络族 | Lv3Effects | 专家/人口/总督/turn、Route signal、Network Receive | 守卫；**网络失效清空后恢复** |
| Lv4Percent R/C族 | Lv4Percent | 专家/总督/turn/build | 守卫 |
| B050人口/负值试验族 | HalfYieldProbe | 手动ON/OFF及enabled时人口/turn/transfer | 守卫；仅启用城市应用，探针仍驻留 |
| B051 SCIENCE/PRODUCTION POS/NEG/POP | CopyYields | UI区域yield样本/总督/turn/人口/移除 | 守卫；旧turn样本失效可先清空 |
| B054 建筑×等级 | StandardizationDiscount | generic Publish、network、总督、UI资格 | cached-old删除/Has检查添加；**unknown→空→重加** |
| B055旧Boost / B057测试 / B058整数 | NetworkBoost | 初始化cleanup、network、总督、turn、控制 | guardedset；**在首都撤销/恢复影响City Center和HD玩家Property** |
| B055 GW CITY/OBJECT | GreatWorkProbe | 旧手动试验/初始化cleanup | guardedset |
| B059 D档及TEST25/50/100 | Dialogue | 收藏样本、load/turn/总督、控制 | guardedset；严格turn样本导致过渡变化 |
| B060六yield正负bit | GreatWorkAdjacency | adjacency样本、Dialogue Audit/收藏/资格 | 只删不需要、只加不存在；扫描整族 |
| B061三yield各16bit（现B062实现） | CommerceConvergence | network/turn/专家/总督/build/city | Has差异；**全世界城市检查，网络unknown→空** |
| CREW_PROJECT_ACCESS | CrewProjects | load/turn/区/建筑/城市/生产完成 | 守卫；全世界扫描但只合格城添加 |
| B053 GOLD测试族 | PurchaseProbe | 手动/转移cleanup | guardedset |
| SPC_P0_GOV_* | GovernorProbe.sql原生Property Effect | 原生Requirement评估 | **不是Building**；无Lua循环SetProperty |
| Potential标识 | B067不存在；B068 CityPotential只读UI | 选城/约2秒 | **不是Building，不持久、不写Property** |
| Standardization模板 | Standardization账本 | 初始化补录/合格建筑事件 | **不是Building**；永久Property，见下节 |

批量cleanup大多仍先HasBuilding才Remove；不能将“每次遍历建筑定义”误报成“每次都写建筑”。同样，old==desired时无写也不代表扫描成本为零。

## 7. Property全部写入路径

| Writer | 权威/用途 | 自动或手动 / 边界 | 状态不变是否仍写 |
|---|---|---|---|
| BindingProbe | Game每玩家binding表、City token | 新城绑定；32次累计限制 | 已绑定守卫；非移动刷新 |
| CompletionRecordProbe | City首个区域完成观察记录 | 首次合法完成 | 已记录不再写 |
| CityJournalProbe / CityFlowProbe | City永久Identity/flow账本 | binding/完成事件推进 | 按状态/阶段校验；非通用每帧 |
| InvestmentAction | City投资账本、Unit预留UID | 明确Prepare/Confirm；消耗事务分阶段写 | 投资+1需多次确认写，最多4Potential；非移动自发投资 |
| Standardization | City模板learned | 首次Industry初始化+合格建筑事件 | 既有learned去重，不持续每帧全楼扫描 |
| UnitActions | Player Crew receipts；Unit RESERVED | Confirm，INTENT/GRANT_ATTEMPTED/COMPLETED写整份receipt表 | **每次施工新增永久token，无固定总上限** |
| UnitActions DEV spawn | Player SPC_CREW_DEV_SPAWN token集合 | 仅手动DEV生成 | 每独立token新增，无上限；普通移动不写 |
| Gameplay marker | City SPC_P0_MARKER | 手动Mark请求 | 请求Token直接Set，无值相等守卫；已隐藏但代码保留 |
| StorageProbe / EnvelopeProbe | Game DEV存储/阶段表 | 手动测试按钮 | 初始/阶段规则限制；非自动高频 |
| HalfYieldProbe | City enabled开关 | 手动ON/OFF | **重复ON/OFF仍SetProperty**；不作为移动根因 |
| YieldCarrierProbe | Plot SPC_B029_ONE/HALF | 手动控制 | 可重复写0/1；不是常态后台路径 |
| CityInheritance / InheritanceShadow | Game/City继承账本 | **隔离未Start** | 不计当前运行写入；附录仍列源码位置 |
| GovernorProbe.sql | City governor条件Property | 原生Modifier | 引擎评估频率未知，无Lua写循环 |
| NetworkBoost SQL HD配套 | Player Boost Property | 随Boost建筑Modifier应用/撤销 | **网络振荡可以间接反复改原生Property** |

未发现普通UnitOperation回调直接SetPotential/投资/模板。最强高频写来自Building及其挂载的原生Modifier，而不是永久Identity重复写。

## 8. Network复杂度与扫描成本

设P=玩家数，C=当前测试玩家城市数，W=全世界城市总数，D=该玩家全部区域数，R=路线数，S=有效专业源数，E=分发后实际source→recipient关联数量，B=标准化建筑分类数，F=一次EffectiveFacts读取成本（含城市永久账本/区域/总督校验）。不是把F当免费。

- UI collect：O(C+R)主要native读取，另有规范化key排序/验证；≤128路线网络wire、≤512城市derive；上限不等于便宜。
- 一次derive：O(C×F + R + 中心来源关联 + E)，最坏分发关联可达O(R×S)。新分配sources/centers/recipients表。
- `ConnectedKinds` / `RecipientSources` / `National`每次重新derive。查询C个城市不是一次O(C+R)，而可重复C次全图构造。
- Discount Audit：候选循环C次，每次derive+每源账本clone/模板分组+建筑分类遍历；随后第二次城市循环reconcile。主项近似O(C×derive + C×B + 模板合并总量)，另有排序和初次4B建筑Has检查。
- UI DiscountEligibility：每城候选可购建筑调用原生CanStartCommand；即使最终signature未变也已付采样成本。
- Copy UI：O(6D)yield读取+排序/封包；Gameplay多个城市Plan又验证样本/查询来源，可重复扫描D和derive。
- CommerceConvergence Audit：遍历W而非C；每城48个bit目标核对，并再次48bit观察值读取；符合商业IV的城另扫routes/来源yield。非测试玩家也进入plan的拒绝/清理路径。
- GWA：6×2×13=156个bit定义移除检查/城，另按需添加，叠加作品和相邻扫描；不是156次写。
- Research/Lv2/Lv3/Industry每个独立Audit重新走城市/facts/建筑族；单次操作命中多个handler时不能只计算其中一个模块。
- Boost init清理旧fractional、整数、测试族；成本按所有城市×定义族计，不能误算为每次普通Audit都整族清理。

示例只作复杂度说明：10城、每城一次RecipientSources查询，会触发至少10次derive城市遍历（100次facts读取起），而不是一次10城读取；同一publish链多个调用者再叠加。没有实机计数，不换算成毫秒或GB。

## 9. 内存 / 日志 / 重试清单

| 容器/机制 | 上限与回收 | 移动/turn/UI会否追加 | 风险判断 |
|---|---|---|---|
| shared.Events / TradeEvents | 各32，超限移除首条 | 每请求/商路事件可追加但有界 | 不是无限日志表 |
| CompletionProbe players.rows | 每玩家64，超限丢最老 | 建城/区域观察追加 | 有界 |
| TradeRouteProbe pending | 固定事件名key布尔；刷新清空 | 单位事件只改同key/计数 | 不按事件保存payload；previous每玩家一份 |
| AutoRouteProbe | 每玩家覆盖；units≤2048/traders≤256 | turn重建临时rows/text | 持久有界，分配/日志频率有成本 |
| BackgroundRoutes lastGood/firstComplete/lastChange/public | 各单份；Replace/Reset | 每刷新覆盖；generation整数增长非历史数组 | 不保存全部旧快照；临时routes/strings频繁分配 |
| ShadowRouteState | 当前集合替换，Invalidate/Reset | 不累积历代快照 | 缓存表本身非已证泄漏 |
| NetworkBridge players | 每玩家当前routes/sources/recipients；≤128routes | 每次derive新表覆盖 | 高频临时分配；旧表是否被外部持有需profile |
| NetworkSender last/seq | 一个签名+计数，无pending队列 | 每revision可发请求 | **Lua无界queue未发现，原生请求队列未知** |
| DialogueRefresh pending | 单packet；每packet最多2次retry；turn/新dirty可再开始 | 单次有界，不代表整个加载周期尝试有界 | ACK不可达时重复批次/日志风险 |
| BackgroundRoutes attempts | 当前批≤3；mark重置为0 | 新dirty/10秒fallback可不断再开始 | 不是无限while；总体尝试无总上限 |
| Boost/Industry/Discount初始化retry | 成功/ready条件后停；无总失败次数界 | System/publish失败时重复 | 功能缺失可能变长期忙循环 |
| Copy/Industry/Discount/Dialogue samples/last/errors | 按player/city/district覆盖；若干旧city key不主动删除 | 新城市/区域增长；普通移动同key覆盖 | 随历史对象增长，无统一生命周期清理 |
| CommerceConvergence last/errors | pid:cityID，无已消失城市统一prune | 全世界新城市增长；重复事件同key覆盖 | 非参与城市也留拒绝/摘要；不是每turn一个新key |
| ConstructionProbe plans/busy | 按city，完成取走plan；busy可能保留false key | 手动Prepare | 城市历史key增长，非普通移动 |
| UnitActions/InvestmentAction plans | 每player当前plan；移除/确认清空 | 选择/prepare替换 | 有界在玩家数，非动作历史 |
| Crew receipts / DEV spawn | **永久每token新增、无cap/prune；整表Property保存** | 只施工confirm/DEV spawn | 明确无界；O(累计动作)保存和clone压力 |
| 投资收据/Binding/Journal/Flow | 投资最多3次提升；binding累计32；状态覆盖 | 不因每turn新增投资 | 有限/设计限制，不为性能随机清除永久事实 |
| Standardization learned | 最多数据库可记录建筑种类；按城市保存 | 合格首次建筑增量 | 有界于建筑目录，不逐事件复制历史 |
| UnitTargetMarkers InstanceManager | ResetInstances归还池；当前合法目标实例复用，高水位可能保留 | 目标变化重建显示 | 未见不Reset的每帧无限GetInstance；B068改lens |
| UI P0报告/分页 | 当前报告覆盖；B068 readings按action:city:page保存，page≤512但无统一eviction | 主要手动读；不每move新增key | 长局手动访问可增长，非首要自动泄漏 |
| B068 DiagnosticLog | 每scope最多128种message，counts累加；6后台scope | 同错误合并，新消息换旧 | 有界，不据此证明其它原生日志/队列安全 |
| Gameplay print / route render | 多处直接print；render高频创建整段报告字符串 | 每刷新/请求发生；部分错误仅去重最后一次 | 磁盘日志非70GB充分解释；字符串与原生缓冲需计数 |
| listener closures / native City引用 | Gameplay共享表持有到context结束；applied等少量旧City引用 | 通常覆盖；未证每move创建永久闭包 | 真实context销毁/原生引用释放未profile |

**没有找到已证明“每次普通单位移动把完整snapshot永久push入无限数组”的代码。**存在真实无界结构，但不能为凑结论将其归因到70GB。应分别测Lua容器条目数、原生Building写次数、请求in-flight数量、进程内存趋势；不要新增逐事件完整payload日志。

## 10. Listener生命周期

- Gameplay模块在Gameplay初始化Start；多数通过shared字段避免重复，但并非每个Start都设同样守卫。Gameplay完整重载依赖引擎销毁旧context，没有所有模块统一unsubscribe协议。
- UI BackgroundRoutes有active初始化守卫，保存event/callback并在Shutdown Remove与ClearUpdate；DialogueRefresh/GPPRefresh/Industry/Copy/Discount也保存hooks并清理；详见附录A原行。
- UnitTargetMarkers清理InstanceManager、更新回调和LuaEvents/Events监听；UnitPanelActions ClearUpdate，未每次选择单位注册新监听。
- 部分UI InitHandler没有额外active守卫（例如BoostRefresh），正常一次Init/Shutdown路径会Remove。若同context重复Init而无Shutdown，可重复注册；尚无此事故证据。
- 未发现打开Diagnostics按钮内部不断Events.Add；不能把HUD面板开关本身当已证listener泄漏。
- 下一阶段固定计数记录每context init/shutdown、当前注册数；目标一次创建对应一次清理。不做无限列表保存callback信息。

## 11. 历史比较

Git实际仅两次commit：`1c0b97f`（初始B051.67）和`3382d7d9291052790a08e35b27e74c916316f17a`（B060.85）。B067.93来自保留完整备份；没有伪造中间Git history。B051.67也不是用户确认正常长局的性能基准。

B060.85已经包含TradeRouteProbe无过滤UnitOperation、BackgroundRoutes失效/重采样、NetworkSender按generation/status/signal去重、标准化、Boost整数、巨作、Crew/Settler轮询。故不能把所有热点归罪Commerce IV。

B060→B067新增CommerceConvergence及48bit城市建筑：接在NetworkBridge.Receive/Rebuild之后，且独立对所有玩家turn等事件扫描全世界城市，**在既有网络振荡上放大负担**。重写后的Commerce只取R/C/I来源，未见商业IV互相经济递归；不能恢复B061失败实现。

所有权/影子三文件新增但B067禁用Start；永久写回调为nil。时代对话改25%本身是数值变更，不新增每事件历史表。B068 UI修订增加只读Potential/有限日志、改lens；核心商路和Buildingwriter未改，因此不能用回退UI单独解释/解决根问题。

具体文件差异见附录D。

## 12. 下一阶段最小隔离 / 修复提案（本轮未执行）

1. 先围绕最强链：把普通单位操作与真实商路变化区别开；将“需要核对”与“已证失效”分开。一次完整快照验证成功后按内容差异发布；不在每次dirty先推空、再推相同数据。真实结束/掠夺/端点失效必须继续可靠撤销，不以保留陈旧路线掩盖问题。
2. 固定大小计数器：每个scope一份当回合+累计计数，不保存payload/历史；包括unit callbacks、route scans、derive、facts/city/building检查、真实add/remove、Property写、send/receive/ACK/in-flight、每模块Audit、listener init/shutdown、重入跳过。手动输出一个汇总，不每事件print。
3. 对比内容相同的重复输入：正式Building写应为0；普通非商人移动且网络无变化时不应触发撤销/重加。先本地事件模型验证“unknown→ready相同内容”的处理，再准备独立短局用户测试；**当前不要求用户测试异常版本**。
4. 若反馈计数持续自增，逐项隔离NetworkSender和Copy/Discount通用publish路径，一次一个开关；不随机debounce、不改成每秒轮询、不先关闭日志宣布成功。
5. 共享一次已验证输入版本的network派生结果，避免单城查询重建全图；将昂贵扫描置于有依据的dirty后面，限制Audit于参与玩家/城市。此为定位后最小改造方向，不本轮重构。
6. 内存：计数容器条目与动作账本长度；不删除永久收据。先确认增长是否与原生写/请求持续增加相关；只有复现数据支持时再设计收据归档/缓存清理。保留所有隔离证据。
7. 恢复正常长局验收前，必须证明闲置时调用收敛、无变更重复输入无写、真实变化只需有限次数写、load一次初始化、内存不持续单调飙升。一次短功能PASS不能关闭此BLOCKER。

## 13. 暂停队列

- UI小调整：按用户本轮要求记入本报告待办，性能阻塞解除后再回Status正式队列；本轮严格只读，不重写Status。
- 诊断按钮文字/城市Potential短标识进一步微调：暂停；已确认紫色lens/左上入口正常不重发测试。
- Potential可见Building：继续暂停；当前UI只读标识不是权威。
- 新功能、balance、Commerce/GW扩展、所有权自动继承：不推进。

用户需要决定：本轮无；审阅后再授权最小性能隔离/修复阶段。
用户需要测试：无；不要求继续运行异常版本。
Codex下一步：停止，等待用户决定下一阶段范围。

## 附录A：完整事件注册/生命周期源码索引（B067.93）

覆盖所有Lua文件；保留多行注册表的上下文。包括未Start的隔离模块及仅手动UI入口，不能把静态注册文本都当已运行。`hook/listen/bind`包装名称以相邻定义判定Events或GameEvents。正文表解释高频handler行为；此处用于追溯具体事件名。

### BindingProbe.lua

```lua
...
114:   if not ok then b.last="ERROR "..tostring(err) end
115:   print("[SPC][B013][BINDING] city="..tostring(cid).." "..b.last)
116:  end
117:  local function listen(ns,name,fn)
118:   local e=P.Field(ns,name)
119:   if e and type(e.Add)=="function" then
120:    local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
121:   else data.hooks[name]="ABSENT" end
122:  end
123:  listen(GameEvents,"CityBuilt",foundation)
124:  listen(Events,"LoadScreenClose",function()
125:   data.phase="AFTER_LOAD_CLOSE"
126:   -- Automatic read-only audit; no repair, allocation or confirmation during load.
127:   for pid,player in pairs(Players) do
```

### CityFlowProbe.lua

```lua
...
159:   resume(pid,city)
160:  end
161:  local event=P.Field(GameEvents,"OnDistrictConstructed")
162:  if event and event.Add then local ok=pcall(event.Add,complete);data.hooks.complete=ok and "REGISTERED" or "ERROR" end
163:  local load=P.Field(Events,"LoadScreenClose")
164:  if load and load.Add then load.Add(function()
165:   data.ready=true
166:   for pid,player in pairs(Players) do if P.IsTestPlayer(pid) then
167:    local b=bucket(pid)
```

### CityInheritance.lua

```lua
...
98:  local function safe(fn,...)
99:   local ok,e=pcall(fn,...);if not ok then local code=tostring(e):match('INHERIT_[A-Z_]+') or 'INHERIT_ERROR';d.errors.last=code;print('[SPC][B066] '..tostring(e)) end
100:  end
101:  local function hook(ns,n,fn) local e=ns and ns[n];if e and type(e.Add)=='function' then e.Add(function(...) safe(fn,...) end) end end
102:  hook(GameEvents,'CityConquered',function(newpid,oldpid,cid,x,y) transfer(newpid,cid,oldpid,x,y,'CityConquered') end)
103:  hook(Events,'CityTransfered',function(pid,cid)
104:   if type(pid)~='number' or type(cid)~='number' then return end
105:   local c=CityManager.GetCity(pid,cid);if c then transfer(pid,cid,nil,c:GetX(),c:GetY(),'CityTransfered') end
106:  end)
107:  hook(GameEvents,'CityBuilt',function(pid,cid,x,y)
108:   if not d.ready then return end
109:   local v=read();local changed=false
110:   for uid,s in pairs(shadow().records) do
...
117:   end
118:   if changed then save(v) end
119:  end)
120:  hook(Events,'LoadScreenClose',function()
121:   d.ready=true
122:   -- Only resume a transfer already durably confirmed; never infer a transfer from coordinates on load.
123:   for uid,r in pairs(read().records) do if not r.retired and r.status~='APPLIED' then safe(restore,uid) end end
```

### CityJournalProbe.lua

```lua
...
149:  function j.EnsureInherited(pid)
150:   assert(j.phase=="AFTER_LOAD_CLOSE" and not bucket(pid).halted,"INHERIT_JOURNAL_HELD")
151:  end
152:  local function listen(ns,name,fn)
153:   local e=P.Field(ns,name)
154:   if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);j.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
155:   else j.hooks[name]="ABSENT" end
156:  end
157:  listen(GameEvents,"OnDistrictConstructed",completed)
158:  listen(Events,"LoadScreenClose",function()
159:   j.phase="AFTER_LOAD_CLOSE"
160:   for pid,player in pairs(Players) do if P.IsTestPlayer(pid) then
161:    local ok,err=pcall(function() for _,city in player:GetCities():Members() do j.Read(pid,city) end end)
```

### CommerceConvergence.lua

```lua
...
99:   rows[#rows+1]='网络：'..tostring(b and b.reason)..' | 当前/样本回合='..Game.GetCurrentGameTurn()..'/'..tostring(b and b.turn)
100:   return table.concat(rows,'\n')
101:  end
102:  local function hook(t,name) local e=P.Field(t,name);if e and e.Add then e.Add(d.Audit) end end
103:  for _,name in ipairs({'LoadScreenClose','PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityWorkerChanged','CityPopulationChanged','CityFocusChanged','CityTransfered'}) do hook(Events,name) end
104:  for _,name in ipairs({'CityBuilt','OnBuildingConstructed','OnDistrictConstructed'}) do hook(GameEvents,name) end
105: end
```

### CompletionProbe.lua

```lua
...
80:   if #b.rows>64 then table.remove(b.rows,1);b.dropped=b.dropped+1 end
81:   print("[SPC]["..P.VERSION.."][COMPLETION] "..row.text:gsub("\n"," | "))
82:  end
83:  local function listen(namespace,name,fn)
84:   local e=P.Field(namespace,name)
85:   if e and type(P.Field(e,"Add"))=="function" then
86:    local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
87:   else data.hooks[name]="ABSENT" end
88:  end
89:  listen(GameEvents,"CityBuilt",function(pid,cid,x,y) observe("built",pid,cid,x,y) end)
90:  listen(GameEvents,"OnDistrictConstructed",function(pid,typeID,x,y) observe("constructed",pid,nil,x,y,typeID) end)
91:  -- Only the first six documented fields are used; do not guess progress payload positions.
92:  listen(Events,"DistrictAddedToMap",function(pid,did,cid,x,y,typeID) observe("added",pid,cid,x,y,typeID,did) end)
93:  listen(Events,"LoadScreenClose",function() data.phase="AFTER_LOAD_CLOSE" end)
94:  print("[SPC]["..P.VERSION.."][COMPLETION] INITIALIZED; memory-only observations, counters reset per load")
95: end
```

### CompletionRecordProbe.lua

```lua
...
83:   b.busy=false;if not ok then b.last="ERROR "..tostring(err) end
84:   print("[SPC][B014][RECORD] "..b.last)
85:  end
86:  local function listen(ns,name,fn)
87:   local e=P.Field(ns,name)
88:   if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);d.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
89:   else d.hooks[name]="ABSENT" end
90:  end
91:  listen(GameEvents,"OnDistrictConstructed",onComplete)
92:  listen(Events,"LoadScreenClose",function() d.phase="AFTER_LOAD_CLOSE" end)
93: end
```

### CopyYields.lua

```lua
...
141:   lines[#lines+1]='读取不触发刷新；已配置不是实测增量。'
142:   return table.concat(lines,'\n')
143:  end
144:  local function hook(source,n,f) local e=P.Field(source,n);if e and e.Add then e.Add(f) end end
145:  -- Only lifecycle cleanup visits ineligible owners; no periodic specialization work for them.
146:  local function cleanupDormant()
147:   for pid,p in pairs(Players) do if not P.IsTestPlayer(pid) then
...
151:    if not ok then print('[SPC][B051][CLEANUP_ERROR] '..tostring(err)) end
152:   end end
153:  end
154:  hook(Events,'LoadScreenClose',function() data.ready=true;data.generation=data.generation+1;data.samples={};data.seq={};data.receiveErrors={};cleanupDormant();data.Audit() end)
155:  hook(Events,'CityTransfered',cleanupDormant)
156:  for _,n in ipairs({'PlayerTurnActivated','CityPopulationChanged','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','CityTransfered','DistrictRemovedFromMap'}) do hook(Events,n,data.Audit) end
157: end
```

### CrewProjects.lua

```lua
...
41:   end
42:   data.busy=false
43:  end
44:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
45:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
46:  for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictBuildProgressChanged','DistrictRemovedFromMap','CityProductionCompleted'}) do hook(Events,n,data.Audit) end
47:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
48: end
```

### Dialogue.lua

```lua
...
105:  end
106:  local function auditAll() for pid in pairs(Players) do d.Audit(pid) end end
107:  for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','PlayerTurnDeactivated'}) do
108:   local e=P.Field(Events,name);if e and e.Add then e.Add(auditAll) end
109:  end
110:  local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() d.ready=false;d.samples={};d.last={};d.Init();auditAll() end) end
111: end
```

### EligibilityProbe.lua

```lua
...
44:   data.samples[phase]=s
45:  end
46:  local e=Events and Events.LoadScreenClose
47:  if e and type(e.Add)=="function" then
48:   local ok=pcall(e.Add,function() sample("LOAD_CLOSE") end)
49:   data.hooks.LoadScreenClose=ok and "REGISTERED" or "ERROR"
50:  else data.hooks.LoadScreenClose="ABSENT" end
51:  sample("INITIALIZE")
```

### EnvelopeProbe.lua

```lua
...
80:    end
81:   end
82:  end
83:  if Events and Events.LoadScreenClose and Events.LoadScreenClose.Add then
84:   local ok=pcall(function() Events.LoadScreenClose.Add(onLoad) end)
85:   data.hook=ok and "REGISTERED" or "REGISTER_FAILED"
86:  end
87: end
```

### Gameplay.lua

```lua
...
327:   shared.LastToken=params.Token
328:   stage("ACK "..shared.Snapshot)
329: end
330: GameEvents.SPC_P0_Request.Add(function(...)
331:   local ok,err=pcall(request,...)
332:   if not ok then shared.FailureAt=shared.Stage;stage("ERROR "..P.Scalar(err)) end
333: end)
...
347:   print("[SPC]["..P.VERSION.."][TRADE_EVENT_RAW] "..line)
348: end
349: local tradeEvent=P.Field(Events,"TradeRouteActivityChanged")
350: if tradeEvent and type(tradeEvent.Add)=="function" then
351:   tradeEvent.Add(function(...)
352:     local ok,err=pcall(onTradeActivity,...)
353:     if not ok then print("[SPC][TRADE_EVENT_ERROR] "..P.Scalar(err)) end
354:   end)
```

### GreatWorkProbe.lua

```lua
...
34:    ..'\n二者互斥；未配置旅游业加成；排除遗物、产品、未知类型。'
35:    ..'\n这是手动实验，不是已完成的时代补贴/50%基础相邻能力。'
36:  end
37:  local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() if d.ready then d.Clean() end end) end
38: end
```

### HalfYieldProbe.lua

```lua
...
70:   end
71:   return data.Describe(pid,c)
72:  end
73:  local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
74:  hook('LoadScreenClose',function() data.ready=true;data.Audit() end)
75:  for _,n in ipairs({'CityPopulationChanged','PlayerTurnActivated','CityTransfered'}) do hook(n,data.Audit) end
76: end
```

### IndustrySupport.lua

```lua
...
83:    ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
84:    ..'\nRead only; verify native specialist yields. Crew projects available from Industry Lv1; project engine behavior requires B044 testing.'
85:  end
86:  local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
87:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
88:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','CityTransfered','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','CityWorkerChanged'}) do hook(Events,n,data.Audit) end
89:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
90: end
```

### InheritanceShadow.lua

```lua
...
70:   local v=cp(old);v.sequence=v.sequence+1;local e={seq=v.sequence,name=name,args=table.concat(text,','),at=table.concat(states,';'),turn=Game.GetCurrentGameTurn()};v.events[#v.events+1]=e
71:   if #v.events>24 then table.remove(v.events,1) end;save(old,v);print('[SPC][B064][EVENT] '..e.seq..' '..name..' '..e.args..' '..e.at)
72:  end
73:  local function hook(ns,name,fn,label)
74:   local e=ns and ns[name];local ok=e and type(e.Add)=='function' and pcall(e.Add,function(...) safe(fn,...) end)
75:   d.hooks[#d.hooks+1]=(label or name)..':'..(ok and 'ON' or 'ABSENT')
76:  end
77:  for _,name in ipairs({'CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'}) do hook(Events,name,function(...) event(name,...) end) end
78:  for _,name in ipairs({'CityBuilt','CityConquered'}) do hook(GameEvents,name,function(...) event(name,...) end,'Game.'..name) end
79:  hook(Events,'LoadScreenClose',function()
80:   d.ready=true
81:   for pid,p in pairs(Players) do if P.IsTestPlayer(pid) then for _,c in p:GetCities():Members() do safe(function() d.Capture(c,'LOAD_VALIDATED') end) end end end
82:  end)
```

### InvestmentAction.lua

```lua
...
128:  end
129:  -- Invalidate a prepared unit if it is removed, even if its numeric ID is reused.
130:  local removed=P.Field(Events,'UnitRemovedFromMap')
131:  if removed and removed.Add then removed.Add(function(pid,id)
132:   if plans[pid] and plans[pid].unitID==id then plans[pid]=nil;shared.InvestmentPreview=nil end
133:  end) end
134:  local load=P.Field(Events,'LoadScreenClose')
135:  if load and load.Add then load.Add(function()
136:   plans={};shared.InvestmentPreview=nil
137:   for pid,player in pairs(Players) do
138:    if P.IsTestPlayer(pid) then
```

### Lv2GPP.lua

```lua
...
109:   end)
110:   local out="B035 Lv2 GPP | "..(ok and result or "ERROR "..tostring(result));print("[SPC][B035] "..out);return out
111:  end
112:  local function bind(events,event,fn) local e=P.Field(events,event);if e and e.Add then e.Add(fn) end end
113:  bind(Events,"LoadScreenClose",function() data.ready=true;data.Audit() end)
114:  for _,event in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorEstablished","GovernorChanged","PlayerTurnActivated","PlayerTurnDeactivated","CityTransfered"}) do bind(Events,event,data.Audit) end
115:  for _,event in ipairs({"OnDistrictConstructed","BuildingConstructed","CityBuilt"}) do bind(GameEvents,event,data.Audit) end
116: end
```

### Lv2Housing.lua

```lua
...
92:   local out="B034 Lv2 Housing | "..(ok and out or "ERROR "..tostring(out))
93:   print("[SPC][B034] "..out);return out
94:  end
95:  local function bind(events,name,fn)
96:   local e=P.Field(events,name);if e and e.Add then e.Add(fn) end
97:  end
98:  bind(Events,"LoadScreenClose",function() data.ready=true;data.Audit() end)
99:  for _,name in ipairs({"GovernorAssigned","GovernorEstablished","GovernorChanged","PlayerTurnActivated","CityTransfered","CityBuildingsChanged"}) do bind(Events,name,data.Audit) end
100:  for _,name in ipairs({"BuildingConstructed","OnDistrictConstructed","CityBuilt"}) do bind(GameEvents,name,data.Audit) end
101: end
```

### Lv3Effects.lua

```lua
...
110:   end)
111:   return (ok and out or ('\nLv3 effects ERROR '..tostring(out)))..'\nLv3 effects status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
112:  end
113:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
114:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
115:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged'}) do hook(Events,n,data.Audit) end
116:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
117: end
```

### Lv3Support.lua

```lua
...
72:   return '\nLv3 top-up carrier (added to Lv1): '..(ok and (f..'F / '..p..'P / '..g..'G') or ('ERROR '..tostring(f)))
73:    ..'\nLv3 status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
74:  end
75:  local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
76:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
77:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered'}) do hook(Events,n,data.Audit) end
78:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
79: end
```

### Lv4Percent.lua

```lua
...
68:   end)
69:   return ok and out or ('Lv4百分比读取失败：'..tostring(out))
70:  end
71:  local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
72:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
73:  for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged','DistrictRemovedFromMap'}) do hook(Events,n,data.Audit) end
74:  for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
75: end
```

### NetworkBoost.lua

```lua
...
120:   out[#out+1]='配置≠实测；读取基线后同回合触发一次未触发的尤里卡/鼓舞，再读取。'
121:   return table.concat(out,'\n')
122:  end
123:  local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
124:  for _,n in ipairs({'GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','PlayerTurnActivated','PlayerTurnDeactivated'}) do hook(Events,n,d.Audit) end
125:  hook(Events,'CityTransfered',function() if d.ready and not d.busy then
126:   d.busy=true;local ok,err=pcall(d.Clean);d.busy=false
127:   if not ok then print('[SPC][B055][CLEAN] '..tostring(err));d.ready=false;return end;d.Audit()
128:  end end)
```

### NetworkBridge.lua

```lua
...
207:   if shared.CommerceConvergence then shared.CommerceConvergence.Audit() end
208:  end
209:  for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
210:   local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(d.Rebuild) end
211:  end
212:  local turn=P.Field(Events,"PlayerTurnActivated");if turn and turn.Add then turn.Add(d.Rebuild) end
213:  local e=P.Field(Events,"LoadScreenClose");if e and e.Add then e.Add(function() d.ready=true end) end
214: end
```

### PurchaseProbe.lua

```lua
...
25:   return d.Describe(c)
26:  end
27:  local e=P.Field(Events,'LoadScreenClose')
28:  if e and e.Add then e.Add(function()
29:   -- Reload always leaves the experiment OFF, including a captured former test city.
30:   for _,p in pairs(Players) do for _,c in p:GetCities():Members() do
31:    local ok,err=pcall(function() set(c,'DISCOUNT',false);set(c,'FIXTURE',false) end)
```

### QualificationProbe.lua

```lua
...
197:   if not ok then gate.Invalidate();latest={status="UNKNOWN",reason=tostring(err)};publish("LOAD_ERROR","NOT_PROVEN") end
198:  end
199:  local e=Events and Events.LoadScreenClose
200:  if e and type(e.Add)=="function" then
201:   local ok=pcall(e.Add,onLoad);data.hook=ok and "REGISTERED" or "ERROR"
202:  end
203:  publish("INITIALIZE")
204:  -- Only scalar diagnostics cross contexts. The private gate and tokens are not exported.
```

### ResearchSupport.lua

```lua
...
114:   print("[SPC][B024] "..out);return out
115:  end
116:  local load=P.Field(Events,"LoadScreenClose")
117:  if load and load.Add then load.Add(function() data.ready=true;data.Audit() end) end
118:  for _,name in ipairs({"PlayerTurnActivated","CityTransfered"}) do
119:   local event=P.Field(Events,name);if event and event.Add then event.Add(data.Audit) end
120:  end
121:  -- Installed after B015/B021, so facts are committed before effects are reconciled.
122:  local event=P.Field(GameEvents,"OnDistrictConstructed")
123:  if event and event.Add then event.Add(completed) end
124:  local built=P.Field(GameEvents,"CityBuilt")
125:  if built and built.Add then built.Add(data.Audit) end
126: end
```

### Standardization.lua

```lua
...
149:   end)
150:   return ok and text or ('B052 读取未完成：'..(tostring(text):match('STD_[A-Z_]+') or 'STD_READ_FAILED'))
151:  end
152:  local function hook(src,n,fn)
153:   local ev=P.Field(src,n);if ev and ev.Add then ev.Add(fn);data.hooks[n]=true end
154:  end
155:  hook(Events,'LoadScreenClose',function() data.ready=true;data.Discover();data.Flush() end)
156:  hook(Events,'PlayerTurnActivated',function(pid) data.Discover(pid);data.Flush() end)
157:  hook(GameEvents,'OnDistrictConstructed',function(pid) data.Discover(pid);data.Flush() end)
158:  for _,name in ipairs({'BuildingConstructed','OnBuildingConstructed'}) do
159:   hook(GameEvents,name,function(pid,cid,bid) data.Queue(pid,cid,bid,name);data.Flush() end)
160:  end
161:  -- HD RegionalYields.lua uses x,y,buildingId,playerId. Recheck this building only.
162:  hook(Events,'BuildingAddedToMap',function(x,y,bid,pid)
163:   if type(pid)~='number' or not P.IsTestPlayer(pid) then return end
164:   local b=P.Info('Buildings',bid);local ok,cat=pcall(catalog)
165:   if not ok or not b or not cat.buildings[b.BuildingType] then return end
...
167:   for _,c in player:GetCities():Members() do data.Queue(pid,c:GetID(),bid,'BUILDING_ADDED_RECHECK') end
168:   data.Flush()
169:  end)
170:  hook(Events,'GameCoreEventPublishComplete',data.Flush)
171: end
```

### StandardizationDiscount.lua

```lua
...
111:   lines[#lines+1]='只读；原生价格以购买页为准，允许同一合格建筑双币折扣。'
112:   return table.concat(lines,'\n')
113:  end
114:  local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
115:  cleanupOtherOwners=function()
116:   local ok,err=pcall(function() init();for pid,p in pairs(Players) do if not P.IsTestPlayer(pid) then for _,c in p:GetCities():Members() do reconcile(pid,c,{}) end end end end)
117:   if not ok then print('[SPC][B054][CLEANUP] '..tostring(err)) end
118:  end
119:  hook('LoadScreenClose',function() d.ready=true;d.generation=d.generation+1;d.samples={};d.seq={};d.applied={};cleanupOtherOwners();d.Audit() end)
120:  hook('CityTransfered',function() d.applied={};cleanupOtherOwners();d.Audit() end)
121:  for _,n in ipairs({'GameCoreEventPublishComplete','PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'}) do hook(n,d.Audit) end
122: end
```

### TradeRouteProbe.lua

```lua
...
115:       print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] GLOBAL_UNAVAILABLE "..scalar(err))
116:     end
117:   end
118:   local function listen(namespace,name,fn)
119:     local event=P.Field(namespace,name)
120:     if event and type(P.Field(event,"Add"))=="function" then event.Add(fn)
121:     else print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] EVENT_ABSENT "..name) end
122:   end
123:   -- Event payloads are never route facts. No assumption about start/end semantics.
124:   for _,name in ipairs({"TradeRouteActivityChanged","TradeRouteRemovedFromMap","UnitRemovedFromMap",
125:       "UnitOperationDeactivated","UnitOperationStarted","UnitOperationsCleared","CityRemovedFromMap","CityAddedToMap","DiplomacyDeclareWar"}) do
126:     local eventName=name;listen(Events,eventName,function() pending[eventName]=true;shared.RouteSignalRevision=shared.RouteSignalRevision+1;if shared.Lv3Effects then shared.Lv3Effects.Audit() end end)
127:   end
128:   for _,name in ipairs({"CityConquered","TradeRoutePlundered"}) do
129:     local eventName=name;listen(GameEvents,eventName,function() pending[eventName]=true;shared.RouteSignalRevision=shared.RouteSignalRevision+1;if shared.Lv3Effects then shared.Lv3Effects.Audit() end end)
130:   end
131:   listen(Events,"LoadScreenClose",function() refresh("LoadScreenClose") end)
132:   listen(Events,"PlayerTurnActivated",function(pid)
133:     if P.IsTestPlayer(pid) then refresh("PlayerTurnActivated") end
134:   end)
135:   listen(Events,"PlayerTurnDeactivated",function(pid)
136:     if P.IsTestPlayer(pid) then refresh("PlayerTurnDeactivated") end
137:   end)
138:   refresh("INITIALIZE")
```

### UI/BackgroundRoutes.lua

```lua
...
168:   retryPending=public.status=="UNKNOWN" and attempts<3
169:   render()
170: end
171: local function listen(name)
172:   local event=P.Field(Events,name)
173:   if event and type(P.Field(event,"Add"))=="function" then
174:     local callback=function()
175:       mark(name)
176:       -- These lifecycle boundaries must not depend on an empty context receiving SetUpdate.
177:       if name=="LoadScreenClose" or name=="PlayerTurnActivated" or name=="PlayerTurnDeactivated" then dispatch() end
178:     end
179:     event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
180:   end
181: end
182: local function initialize()
...
188:   lastGame=ExposedMembers.SPC_P0;lastSignal=lastGame and lastGame.RouteSignalRevision
189:   for _,name in ipairs({"LoadScreenClose","TradeRouteActivityChanged","TradeRouteAddedToMap","TradeRouteRemovedFromMap",
190:     "UnitOperationStarted","UnitOperationsCleared","UnitOperationDeactivated","UnitRemovedFromMap",
191:     "CityAddedToMap","CityRemovedFromMap","DiplomacyDeclareWar","PlayerTurnActivated","PlayerTurnDeactivated"}) do listen(name) end
192:   -- Native UI uses publish-complete to flush a batch of GameCore changes.
193:   -- No visibility check, UI opening, or event payload as route truth.
194:   for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete"}) do
...
203:         end)
204:         if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;retryPending=false;render() end
205:       end
206:       event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
207:     end
208:   end
209:   local systemEvent=P.Field(Events,"SystemUpdateUI")
...
217:       end)
218:       if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;render() end
219:     end
220:     systemEvent.Add(callback);hooks[#hooks+1]={event=systemEvent,callback=callback}
221:   end
222:   dispatch() -- no panel/UI open action involved
223:   ContextPtr:SetUpdate(function(dt)
224:     contextPulses=contextPulses+1
225:     if not active or type(dt)~="number" or dt<0 then return end
226:     clock=clock+dt;scanAge=scanAge+dt;sinceDirty=sinceDirty+dt
...
233:     if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;render() end
234:   end)
235: end
236: ContextPtr:SetInitHandler(initialize)
237: ContextPtr:SetShutdown(function()
238:   active=false;normalized:Reset();ContextPtr:ClearUpdate()
239:   for _,h in ipairs(hooks) do if type(P.Field(h.event,"Remove"))=="function" then h.event.Remove(h.callback) end end
240:   if ExposedMembers.SPC_P0_BackgroundRoutes==public then ExposedMembers.SPC_P0_BackgroundRoutes=nil end
241: end)
```

### UI/BoostRefresh.lua

```lua
...
9:  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='BOOST_INIT',Token=P.VERSION..':boost:init'})
10:  busy=false;if not ok then print('[SPC][B055][INIT] '..tostring(err)) end
11: end
12: ContextPtr:SetInitHandler(function()
13:  for _,name in ipairs({'SystemUpdateUI','LoadScreenClose','GameCoreEventPlaybackComplete'}) do
14:   local e=P.Field(Events,name);if e and e.Add then e.Add(refresh);hooks[#hooks+1]=e end
15:  end
16:  refresh()
17: end)
18: ContextPtr:SetShutdown(function() for _,e in ipairs(hooks) do if e.Remove then e.Remove(refresh) end end end)
```

### UI/CopyYieldRefresh.lua

```lua
...
47:  local ok,err=pcall(refresh)
48:  if not ok then busy=false;public.state='ERROR';public.error=code(err);print('[SPC][B051][BACKGROUND_ERROR] '..tostring(err)) end
49: end
50: local function bind(name,fn)
51:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
52: end
53: ContextPtr:SetInitHandler(function()
54:  -- Established event-driven path: runs even when this empty context receives no frame updates.
55:  for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(name,safelyRefresh) end
56:  bind('LoadScreenClose',function() initialized=false;sent=nil;safelyRefresh() end)
57:  bind('SystemUpdateUI',function()
58:   local shared=ExposedMembers.SPC_P0;local d=shared and shared.CopyYields
59:   if not initialized or (d and d.ready and d.generation~=public.generation) then safelyRefresh() end
60:  end)
61:  safelyRefresh()
62:  ContextPtr:SetUpdate(function(dt)
63:   if type(dt)~='number' or dt<0 then return end
64:   elapsed=elapsed+dt;if elapsed>=1 then elapsed=0;safelyRefresh() end
65:  end)
66: end)
67: ContextPtr:SetShutdown(function()
68:  ContextPtr:ClearUpdate()
69:  for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end
70:  if ExposedMembers.SPC_CopyBackground==public then ExposedMembers.SPC_CopyBackground=nil end
71: end)
```

### UI/DialogueRefresh.lua

```lua
...
8: local function mark(reason)
9:  dirty=true;revision=revision+1;public.reason=reason
10: end
11: -- Empty background contexts do not reliably receive SetUpdate in Civ VI.
12: -- Generic engine pulses may retransmit the SAME packet at most twice; never scan.
13: local safe
14: local function stopRetry() end
...
74:  busy=false
75: end
76: safe=function() local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';print('[SPC][B059][UI] '..tostring(err)) end end
77: local function bind(name,fn)
78:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
79: end
80: ContextPtr:SetInitHandler(function()
81:  -- These events describe collection/city/eligibility changes, not our own yield refreshes.
82:  for _,name in ipairs({'GreatWorkCreated','GreatWorkMoved','CityAddedToMap','CityRemovedFromMap','CityTransfered','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','FeatureAddedToMap','CityTileOwnershipChanged'}) do
83:   local reason=name;bind(name,function() mark(reason) end)
84:  end
85:  bind('LoadScreenClose',function() mark('LOAD_SCREEN_CLOSE');safe() end)
86:  for _,name in ipairs({'SystemUpdateUI','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'}) do bind(name,pulse) end
87:  safe()
88: end)
89: ContextPtr:SetShutdown(function()
90:  stopRetry()
91:  for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.fn) end end
92:  if ExposedMembers.SPC_DialogueBackground==public then ExposedMembers.SPC_DialogueBackground=nil end
```

### UI/DiscountEligibility.lua

```lua
...
46: local function safe()
47:  local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err);print('[SPC][B054][UI] '..tostring(err)) end
48: end
49: local function bind(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f);hooks[#hooks+1]={e,f} end end
50: ContextPtr:SetInitHandler(function()
51:  for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(n,safe) end
52:  bind('LoadScreenClose',function() sent=nil;initialized=false;safe() end)
53:  bind('SystemUpdateUI',function()
54:   local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
55:   if not initialized or (d and d.generation~=generation) then safe() end
56:  end)
57:  safe()
58: end)
59: ContextPtr:SetShutdown(function() for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end end)
```

### UI/GPPRefresh.lua

```lua
...
18:  if not ok then dirty=true;print("[SPC][B035][GPP_SEND_ERROR] "..tostring(err)) end
19:  busy=false
20: end
21: local function bind(name,fn)
22:  local e=P.Field(Events,name)
23:  if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
24: end
25: ContextPtr:SetInitHandler(function()
26:  if active then return end;active=true
27:  for _,name in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorChanged","GovernorEstablished","GovernorPromoted"}) do bind(name,mark) end
28:  for _,name in ipairs({"LoadScreenClose","PlayerTurnActivated","PlayerTurnDeactivated"}) do bind(name,function() mark();flush() end) end
29:  for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete","SystemUpdateUI"}) do bind(name,flush) end
30:  flush()
31: end)
32: ContextPtr:SetShutdown(function()
33:  active=false
34:  for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.fn) end end
35:  hooks={}
```

### UI/IndustryRefresh.lua

```lua
...
36:  busy=false
37:  if not ok then print('[SPC][B036][BASE_UI_ERROR] '..tostring(err)) end
38: end
39: local function bind(name,fn)
40:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
41: end
42: ContextPtr:SetInitHandler(function()
43:  if active then return end;active=true
44:  for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','LoadScreenClose','PlayerTurnActivated'}) do bind(name,refresh) end
45:  -- Retry initialization only until first successful sample; no per-frame world scan.
46:  bind('SystemUpdateUI',function() if not initialized then refresh() end end)
47:  refresh()
48: end)
49: ContextPtr:SetShutdown(function() active=false;for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end;hooks={} end)
```

### UI/P0Panel.lua

```lua
...
83: -- event pulses do not collect works or adjacency and never create a scan loop.
84: local function gwaPulse()
85:   local f=gwaFlight;if not f or f.busy then return end
86:   if displayResponse() then gwaFlight=nil;ContextPtr:ClearUpdate();return end
87:   f.pulses=f.pulses+1
88:   if f.pulses<3 then return end
89:   f.pulses=0
90:   if f.retries>=2 then
91:     gwaFlight=nil;ContextPtr:ClearUpdate()
92:     status(P.VERSION.." | 相邻请求未收到回复[NEWLINE]"..gwaDiagnostics())
93:     return
94:   end
95:   f.retries=f.retries+1;f.busy=true
96:   local ok,err=pcall(UI.RequestPlayerOperation,f.pid,PlayerOperations.EXECUTE_SCRIPT,f.packet)
97:   f.busy=false
98:   if displayResponse() then gwaFlight=nil;ContextPtr:ClearUpdate()
99:   elseif not ok then status('相邻发送失败：'..tostring(err)..'[NEWLINE]'..gwaDiagnostics()) end
100: end
101: local function waitForResponse()
102:   if displayResponse() then return end
103:   local elapsed=0
104:   ContextPtr:SetUpdate(function(dt)
105:     elapsed=elapsed+dt
106:     if displayResponse() then ContextPtr:ClearUpdate()
107:     elseif elapsed>=10 then
108:       ContextPtr:ClearUpdate()
109:       status(P.VERSION.." | NO RESPONSE: "..P.Scalar(pendingAction).."[NEWLINE]Click Show / Copy to check a late response.")
110:     end
111:   end)
112: end
113: request=function(action,advance)
114:   ContextPtr:ClearUpdate()
115:   gwaFlight=nil
116:   local playerID=Game.GetLocalPlayer()
117:   if not P.IsTestPlayer(playerID) then trace("OUTSIDE_TEST_CIV");return end
...
180: end
181: local completionPage=1
182: local function showCompletion(older)
183:   ContextPtr:ClearUpdate();pendingToken=nil
184:   local pid=Game.GetLocalPlayer()
185:   if not P.IsTestPlayer(pid) then return end
186:   local data=(ExposedMembers.SPC_P0 or {}).CompletionProbe
...
202: local function initialize()
203:   showRoot();Controls.Window:SetHide(true)
204:   Controls.Title:SetText("SPC "..P.VERSION.." | Specialization diagnostics")
205:   Controls.OpenButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(false) end)
206:   Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(true) end)
207:   Controls.QualificationButton:RegisterCallback(Mouse.eLClick,function()
208:     ContextPtr:ClearUpdate();pendingToken=nil
209:     local shared=ExposedMembers.SPC_P0 or {}
210:     local d=shared.QualificationProbe
211:     local pid=Game.GetLocalPlayer()
...
216:     status(localReport:gsub("\n","[NEWLINE]"))
217:   end)
218:   local unknownPage=0
219:   Controls.EligibilityUnknownButton:RegisterCallback(Mouse.eLClick,function()
220:     ContextPtr:ClearUpdate();pendingToken=nil
221:     local shared=ExposedMembers.SPC_P0 or {}
222:     local d=shared.EligibilityProbe
223:     local sample=d and d.samples.LOAD_CLOSE
...
243:     end
244:     localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
245:   end)
246:   Controls.EligibilityButton:RegisterCallback(Mouse.eLClick,function()
247:     ContextPtr:ClearUpdate();pendingToken=nil
248:     local pid=Game.GetLocalPlayer()
249:     local shared=ExposedMembers.SPC_P0 or {}
250:     local d=shared.EligibilityProbe
...
266:     lines[#lines+1]="只读；未写资格或城市成果。截图即可。"
267:     localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
268:   end)
269:   Controls.CityJournalButton:RegisterCallback(Mouse.eLClick,function() request("CITY_JOURNAL_READ") end)
270:   Controls.CompletionRecordButton:RegisterCallback(Mouse.eLClick,function() request("COMPLETION_RECORD_READ") end)
271:   Controls.BindingReadButton:RegisterCallback(Mouse.eLClick,function() request("BINDING_READ") end)
272:   Controls.CarrierStepButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_DETAIL") end)
273:   Controls.CarrierOffButton:RegisterCallback(Mouse.eLClick,function() request("CARRIER_OFF") end)
274:   for _,a in ipairs({"READ","OFF","AUTO","TEST5"}) do local action=a;Controls["Commerce"..a.."Button"]:RegisterCallback(Mouse.eLClick,function() request("COMMERCE_"..action) end) end
275:   Controls.InheritRecordButton:RegisterCallback(Mouse.eLClick,function() request("SHADOW_SELECT") end)
276:   Controls.InheritReadButton:RegisterCallback(Mouse.eLClick,function() request("SHADOW_READ") end)
277:   Controls.SourceYieldButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_READ") end)
278:   Controls.ConstructionPreviewButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_PREVIEW") end)
279:   Controls.ConstructionApplyButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_APPLY") end)
280:   Controls.Lv2GPPButton:RegisterCallback(Mouse.eLClick,function() request("LV2_GPP_READ") end)
281:   Controls.Lv2HousingButton:RegisterCallback(Mouse.eLClick,function() request("LV2_HOUSING_READ") end)
282:   Controls.InvestPrepareButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_PREPARE") end)
283:   Controls.InvestConfirmButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_CONFIRM") end)
284:   Controls.NetworkButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_READ") end)
285:   Controls.Lv4PercentButton:RegisterCallback(Mouse.eLClick,function() request("LV4_PERCENT_READ") end)
286:   Controls.ResearchReadButton:RegisterCallback(Mouse.eLClick,function() request("RESEARCH_READ") end)
287:   Controls.CityFlowButton:RegisterCallback(Mouse.eLClick,function() request("CITY_FLOW_READ") end)
288:   Controls.EnvelopeReadButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_READ") end)
289:   Controls.EnvelopeNextButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_NEXT") end)
290:   Controls.StorageReadButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_READ") end)
291:   Controls.StorageWriteButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_WRITE") end)
292:   Controls.CompletionButton:RegisterCallback(Mouse.eLClick,function() showCompletion(false) end)
293:   Controls.CompletionNextButton:RegisterCallback(Mouse.eLClick,function() showCompletion(true) end)
294:   Controls.CaptureButton:RegisterCallback(Mouse.eLClick,function() request("CAPTURE") end)
295:   Controls.HalfReadButton:RegisterCallback(Mouse.eLClick,function() request('HALF_READ') end)
296:   Controls.HalfOnButton:RegisterCallback(Mouse.eLClick,function() request('HALF_ON') end)
297:   Controls.HalfOffButton:RegisterCallback(Mouse.eLClick,function() request('HALF_OFF') end)
298:   Controls.BoostTestZeroButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_ZERO') end)
299:   Controls.BoostTestHalfButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HALF') end)
300:   Controls.BoostTestHighButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HIGH') end)
301:   Controls.BoostTestAutoButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_AUTO') end)
302:   Controls.BoostReadButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_READ') end)
303:   Controls.BoostBaseButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_BASELINE') end)
304:   Controls.DialogueTest25Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST25') end)
305:   Controls.DialogueTest50Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST50') end)
306:   Controls.DialogueTest100Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST100') end)
307:   Controls.GWAReadButton:RegisterCallback(Mouse.eLClick,function() request('GWA_READ') end)
308:   Controls.GWAOffButton:RegisterCallback(Mouse.eLClick,function() request('GWA_OFF') end)
309:   Controls.GWAAutoButton:RegisterCallback(Mouse.eLClick,function() request('GWA_AUTO') end)
310:   Controls.GWBaselineButton:RegisterCallback(Mouse.eLClick,function() request('GW_BASELINE') end)
311:   Controls.GWReadButton:RegisterCallback(Mouse.eLClick,function() request('GW_READ') end)
312:   Controls.GWCityButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_AUTO') end)
313:   Controls.GWObjectButton:RegisterCallback(Mouse.eLClick,function() request('GW_OBJECT') end)
314:   Controls.GWOffButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_OFF') end)
315:   Controls.DiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ') end)
316:   Controls.NextDiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ',true) end)
317:   Controls.PurchaseBaseButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_BASE') end)
318:   Controls.PurchaseOnButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_ON') end)
319:   Controls.PurchaseOffButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_OFF') end)
320:   Controls.PurchaseReadButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_READ') end)
321:   Controls.TemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ") end)
322:   Controls.NextTemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ",true) end)
323:   Controls.Lv4CopyButton:RegisterCallback(Mouse.eLClick,function() request("LV4_COPY_READ") end)
324:   Controls.AdjacencyButton:RegisterCallback(Mouse.eLClick,function() request("ADJACENCY") end)
325:   Controls.BackgroundRoutesButton:RegisterCallback(Mouse.eLClick,function()
326:     ContextPtr:ClearUpdate();pendingToken=nil
327:     if not P.IsTestPlayer(Game.GetLocalPlayer()) then return end
328:     local data=ExposedMembers.SPC_P0_BackgroundRoutes
329:     localReport=P.VERSION.." | 后台路线（只看已有缓存）\n"
330:       ..((data and data.version==P.VERSION and data.text) or "没有后台记录。请截图；此按钮不会启动读取。")
331:     status(localReport:gsub("\n","[NEWLINE]"))
332:   end)
333:   Controls.RouteStateButton:RegisterCallback(Mouse.eLClick,function()
334:     ContextPtr:ClearUpdate();pendingToken=nil
335:     local pid=Game.GetLocalPlayer()
336:     if not P.IsTestPlayer(pid) then return end
337:     local data=ExposedMembers.SPC_P0 or {}
...
342:         or "尚无自动记录；截图即可。此按钮不会触发采样。")
343:     status(localReport:gsub("\n","[NEWLINE]"))
344:   end)
345:   Controls.RouteEventsButton:RegisterCallback(Mouse.eLClick,function() request("TRADE_EVENTS") end)
346:   Controls.TradeButton:RegisterCallback(Mouse.eLClick,function() request("TRADE") end)
347:   Controls.NextButton:RegisterCallback(Mouse.eLClick,function()
348:     if pageAction=="ADJACENCY" or pageAction=="TRADE" then request(pageAction,true) end
349:   end)
350:   Controls.GovernorButton:RegisterCallback(Mouse.eLClick,function() request("GOVERNOR") end)
351:   Controls.SpecialistsButton:RegisterCallback(Mouse.eLClick,function() request("SPECIALISTS") end)
352:   Controls.MarkButton:RegisterCallback(Mouse.eLClick,function() request("MARK_CITY") end)
353:   Controls.CopyButton:RegisterCallback(Mouse.eLClick,function() copy(false) end)
354:   Controls.BaselineButton:RegisterCallback(Mouse.eLClick,function() copy(true) end)
355:   trace("READY ISOLATED_PROBES")
356: end
357: ContextPtr:SetInitHandler(initialize)
358: Events.LoadScreenClose.Add(showRoot)
359: Events.SystemUpdateUI.Add(gwaPulse)
360: ContextPtr:SetShutdown(function() gwaFlight=nil;Events.SystemUpdateUI.Remove(gwaPulse);ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
```

### UI/UnitPanelActions.lua

```lua
...
114:  end
115:  parent:CalculateSize();parent:ReprocessAnchoring()
116: end
117: ContextPtr:SetInitHandler(function()
118:  timer=0;ContextPtr:SetHide(false)
119:  Controls.PrepareButton:RegisterCallback(Mouse.eLClick,function() dispatch(false) end)
120:  Controls.ConfirmButton:RegisterCallback(Mouse.eLClick,function() dispatch(true) end)
121:  ContextPtr:SetUpdate(update)
122: end)
123: ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Controls.ActionGroup:SetHide(true) end)
```

### UI/UnitSites.lua

```lua
...
70: end
71: local function initialize()
72:  showRoot();refresh()
73:  Controls.PrecisionButton:RegisterCallback(Mouse.eLClick,precision)
74:  Controls.ReadButton:RegisterCallback(Mouse.eLClick,function() read() end)
75:  Controls.SpawnCrewButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_SPAWN') end)
76:  Controls.PrepareUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_PREPARE') end)
77:  Controls.ConfirmUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_CONFIRM') end)
78:  Controls.BuilderTargetsButton:RegisterCallback(Mouse.eLClick,function() LuaEvents.SPC_ToggleBuilderTargets() end)
79:  Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() token=nil;Controls.Window:SetHide(true) end)
80:  local timer=0
81:  ContextPtr:SetUpdate(function(dt)
82:   timer=timer+dt;if timer<0.2 then return end
83:   local step=timer;timer=0;refresh()
84:   if not token and not precisionVisible and ExposedMembers.SPC_UnitPanelStatus then Controls.Report:SetText(tostring(ExposedMembers.SPC_UnitPanelStatus):gsub("\n","[NEWLINE]")) end
...
94:  end)
95:  print('[SPC][B040][UNIT_SITE_UI_READY] visibility fix 52')
96: end
97: ContextPtr:SetInitHandler(initialize)
98: Events.LoadScreenClose.Add(showRoot)
99: ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
```

### UI/UnitTargetMarkers.lua

```lua
...
65: local function init()
66:  manager=InstanceManager:new('TargetInstance','Anchor',ContextPtr)
67:  ContextPtr:SetHide(false);timer=0;age=0;active=true
68:  ContextPtr:SetUpdate(function(dt) if active then update(dt) end end)
69:  LuaEvents.SPC_ToggleBuilderTargets.Add(toggle)
70:  for _,name in ipairs({'UnitSelectionChanged','InterfaceModeChanged','LoadScreenClose'}) do
71:   local e=Events[name];if e then e.Add(changed);hooks[#hooks+1]={e,changed} end
72:  end
73: end
74: ContextPtr:SetInitHandler(init)
75: ContextPtr:SetShutdown(function()
76:  active=false;clear();ContextPtr:ClearUpdate();LuaEvents.SPC_ToggleBuilderTargets.Remove(toggle)
77:  for _,h in ipairs(hooks) do h[1].Remove(h[2]) end
78: end)
```

### UnitActions.lua

```lua
...
161:   return output
162:  end
163:  local removed=Events and Events.UnitRemovedFromMap
164:  if removed and removed.Add then removed.Add(function(pid,id)
165:   if plans[pid] and plans[pid].unitID==id then plans[pid]=nil end
166:  end) end
167: end
```

## 附录B：全部直接Building/Property写入定位

所有B067 Lua文本的写入调用；孤立源码的继承路径仍未运行。原生SQL Property Effect另见正文第7节。

### BindingProbe.lua

```lua
73:   assert(same(ledger(pid),before,0),"STALE_LEDGER")
74:   b.gameWrites=b.gameWrites+1
75:   pcall(function() Game:SetProperty(key(pid),next) end)
76:   assert(same(ledger(pid),next,0),"GAME_WRITE_UNCONFIRMED")
77:  end
102:    assert(city and city:GetID()==cid and city:GetOwner()==pid and city:GetX()==x and city:GetY()==y
103:     and city:GetProperty(TOKEN)==nil,"CITY_CHANGED_BEFORE_WRITE")
104:    b.cityWrites=b.cityWrites+1;pcall(function() city:SetProperty(TOKEN,uid) end)
105:    assert(city:GetProperty(TOKEN)==uid,"CITY_WRITE_UNCONFIRMED")
106:    local confirmed=clone(next);confirmed.records[tostring(cid)].state="CONFIRMED"
```

### CityFlowProbe.lua

```lua
36:   assert(same(read(pid,city),old),"STALE_FLOW")
37:   assert(identity(pid,city)==nextValue.token,"WRITE_IDENTITY_CHANGED")
38:   b.writes=b.writes+1;pcall(function() city:SetProperty(KEY,clone(nextValue)) end)
39:   assert(same(read(pid,city),nextValue),"FLOW_WRITE_UNCONFIRMED")
40:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityFlowProbe.lua') end
```

### CityInheritance.lua

```lua
15:   assert(type(v)=='table' and v.schema==1 and type(v.records)=='table','INHERIT_BAD_LEDGER');return cp(v)
16:  end
17:  local function save(v) Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'INHERIT_WRITE_FAILED') end
18:  local function shadow() return Game:GetProperty('SPC_INHERITANCE_SHADOW_V1') or {records={}} end
19:  local function valid(s)
59:   local ok,e=pcall(function()
60:    for _,k in ipairs({'JOURNAL','FLOW','INVEST','TEMPLATES','TOKEN'}) do
61:     if a[k]~=nil and not eq(c:GetProperty(fields[k]),a[k]) then c:SetProperty(fields[k],cp(a[k]));assert(eq(c:GetProperty(fields[k]),a[k]),'INHERIT_CITY_WRITE_FAILED') end
62:    end
63:    shared.CityFlowProbe.ResumeInherited(r.owner,c)
```

### CityJournalProbe.lua

```lua
54:   assert(equal(read(pid,city),old,0),"STALE_JOURNAL")
55:   b.writes=b.writes+1
56:   pcall(function() city:SetProperty(KEY,nextValue) end)
57:   assert(equal(read(pid,city),nextValue,0),"WRITE_UNCONFIRMED")
58:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityJournalProbe.lua') end
```

### CommerceConvergence.lua

```lua
47:    for bit=0,15 do local r=assert(row(y,bit),'DATABASE_MISSING');local want=math.floor(n/2^bit)%2==1
48:     if want==adding and b:HasBuilding(r.Index)~=want then
49:      if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
50:      assert(b:HasBuilding(r.Index)==want,'CARRIER_WRITE_FAILED');d.writes=d.writes+1
51:     end
```

### CompletionRecordProbe.lua

```lua
75:    assert(integer(v.districtID) and integer(v.turn),"INVALID_EVENT_FIELDS")
76:    assert(shared.BindingProbe.Resolve(pid,city)==token and city:GetProperty(KEY)==nil,"STALE_BINDING_OR_RECORD")
77:    b.writes=b.writes+1;pcall(function() city:SetProperty(KEY,v) end)
78:    local after=read(pid,city,token);assert(after,"WRITE_UNCONFIRMED")
79:    for k,value in pairs(v) do assert(after[k]==value,"READBACK_MISMATCH") end
```

### CopyYields.lua

```lua
71:      local id=row(y,mode,bit).Index;local has=b:HasBuilding(id);assert(type(has)=='boolean','COPY_CARRIER_UNKNOWN')
72:      if has~=want then
73:       if want then c:GetBuildQueue():CreateBuilding(id) else b:RemoveBuilding(id) end
74:       assert(b:HasBuilding(id)==want,'COPY_WRITE_UNCONFIRMED');data.changes=data.changes+1
75:      end
```

### CrewProjects.lua

```lua
31:       wanted=valid and wanted==true
32:       if present~=wanted then
33:        if wanted then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
34:        assert(b:HasBuilding(row.Index)==wanted,'PROJECT_ACCESS_WRITE_UNCONFIRMED')
35:       end
```

### Dialogue.lua

```lua
7:   local row=assert(P.Info('Buildings',id),'DIALOGUE_DATABASE_MISSING');local b=c:GetBuildings()
8:   if b:HasBuilding(row.Index)~=want then
9:    if want then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
10:    assert(b:HasBuilding(row.Index)==want,'DIALOGUE_WRITE_FAILED');d.changes=d.changes+1
11:   end
```

### EnvelopeProbe.lua

```lua
52:     else
53:      b.attempts=b.attempts+1
54:      local ok=pcall(function() Game:SetProperty("SPC_DEV_ENVELOPE_B019_P"..pid,M.Expected(pid,step+1)) end)
55:      local after=read(pid)
56:      if after==step+1 then outcome=ok and "SAVED_READBACK_MATCH" or "SAVED_AFTER_THROW"
```

### Gameplay.lua

```lua
319:   if params.Action=="MARK_CITY" and marker==nil then
320:     stage("BEFORE_SET")
321:     city:SetProperty("SPC_P0_MARKER",params.Token)
322:     stage("AFTER_SET")
323:     marker=city:GetProperty("SPC_P0_MARKER")
```

### GreatWorkAdjacency.lua

```lua
12:    local id=key(y,sign..bit);local r=P.Info('Buildings',id)
13:    assert(r,'GWA_DATABASE_MISSING')
14:    if b:HasBuilding(r.Index) and not want[id] then b:RemoveBuilding(r.Index);assert(not b:HasBuilding(r.Index),'GWA_REMOVE_FAILED') end
15:   end end end
16:   for id in pairs(want) do local r=P.Info('Buildings',id)
17:    if not b:HasBuilding(r.Index) then c:GetBuildQueue():CreateBuilding(r.Index) end
18:    assert(b:HasBuilding(r.Index),'GWA_WRITE_FAILED')
19:   end
```

### GreatWorkProbe.lua

```lua
7:   local b=c:GetBuildings()
8:   if b:HasBuilding(r.Index)~=want then
9:    if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
10:   end
11:   assert(b:HasBuilding(r.Index)==want,'B055_GW_WRITE_UNCONFIRMED')
```

### HalfYieldProbe.lua

```lua
22:      local b=c:GetBuildings();local has=b:HasBuilding(row.Index)
23:      if has~=want then
24:       if want then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
25:       assert(b:HasBuilding(row.Index)==want,'B050_WRITE_UNCONFIRMED')
26:      end
64:    SPCHalfYieldProbe.Plan(c:GetPopulation())
65:    if c:GetProperty(key)~=true then data.baseline[pid..':'..c:GetID()]=totals(c) end
66:    c:SetProperty(key,true);data.ready=true;data.Audit()
67:   elseif action=='HALF_OFF' then
68:    -- Revoke carriers before clearing flag, so an uncertain removal can be retried.
69:    reconcile(pid,c,nil);c:SetProperty(key,false);data.errors[pid..':'..c:GetID()]=nil
70:   end
71:   return data.Describe(pid,c)
```

### IndustrySupport.lua

```lua
33:    assert(type(present)=='boolean','CARRIER_READ_UNKNOWN')
34:    if write and present~=wanted then
35:     if wanted then city:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
36:     assert(b:HasBuilding(row.Index)==wanted,'CARRIER_WRITE_UNCONFIRMED')
37:     data.changes=data.changes+1;present=wanted
```

### InheritanceShadow.lua

```lua
17:   if eq(old,v) then return end
18:   assert(eq(read(),old),'SHADOW_STALE');v.revision=old.revision+1
19:   Game:SetProperty(KEY,cp(v));assert(eq(read(),v),'SHADOW_WRITE_UNCONFIRMED');d.writes=d.writes+1
20:  end
21:  local function safe(fn,...)
```

### InvestmentAction.lua

```lua
35:   assert(not halted[pid],'REENTRANT_HELD');facts(pid,c)
36:   assert(same(c:GetProperty(KEY),old),'STALE_LEDGER')
37:   c:SetProperty(KEY,cp(nextValue))
38:   assert(not halted[pid] and same(c:GetProperty(KEY),nextValue),'LEDGER_WRITE_UNCONFIRMED')
39:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'InvestmentAction.lua') end
113:     cityUID=f.token,expectedRevision=intent.revision}
114:    destructive=true;write(pid,c,old,intent)
115:    u=settler(pid,c,p.unitID,p.site);u:SetProperty(UNIT_KEY,uid)
116:    assert(u:GetProperty(UNIT_KEY)==uid and not halted[pid],'UNIT_RESERVATION_UNCONFIRMED')
117:    Players[pid]:GetUnits():Destroy(u)
```

### Lv2GPP.lua

```lua
47:   local b=city:GetBuildings();local present=b:HasBuilding(id);assert(type(present)=="boolean","GPP_CARRIER_READ_UNKNOWN")
48:   if present==wanted then return end
49:   if wanted then city:GetBuildQueue():CreateBuilding(id) else b:RemoveBuilding(id) end
50:   assert(b:HasBuilding(id)==wanted,"GPP_CARRIER_CHANGE_UNCONFIRMED");data.changes=data.changes+1
51:  end
```

### Lv2Housing.lua

```lua
45:   assert(type(present)=="boolean","HOUSING_CARRIER_READ_UNKNOWN")
46:   if present==wanted then return end
47:   if wanted then city:GetBuildQueue():CreateBuilding(id) else buildings:RemoveBuilding(id) end
48:   assert(buildings:HasBuilding(id)==wanted,"HOUSING_CHANGE_UNCONFIRMED")
49:   data.changes=data.changes+1
```

### Lv3Effects.lua

```lua
65:         local b=c:GetBuildings();local present=b:HasBuilding(row.Index);assert(type(present)=='boolean','LV3_CARRIER_UNKNOWN')
66:         if present~=want then
67:          if want then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
68:          assert(b:HasBuilding(row.Index)==want,'LV3_WRITE_UNCONFIRMED');data.changes=data.changes+1
69:         end
```

### Lv3Support.lua

```lua
55:         local b=c:GetBuildings();local present=b:HasBuilding(row.Index);assert(type(present)=='boolean','LV3_CARRIER_UNKNOWN')
56:         if present~=want then
57:          if want then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
58:          assert(b:HasBuilding(row.Index)==want,'LV3_WRITE_UNCONFIRMED');data.changes=data.changes+1
59:         end
```

### Lv4Percent.lua

```lua
38:          local b=c:GetBuildings();local present=b:HasBuilding(row.Index);assert(type(present)=='boolean','LV4_CARRIER_UNKNOWN')
39:          if present~=want then
40:           if want then c:GetBuildQueue():CreateBuilding(row.Index) else b:RemoveBuilding(row.Index) end
41:           assert(b:HasBuilding(row.Index)==want,'LV4_WRITE_UNCONFIRMED');data.changes=data.changes+1
42:          end
```

### NetworkBoost.lua

```lua
20:   assert(type(present)=='boolean','B055_CARRIER_UNKNOWN')
21:   if present~=want then
22:    if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
23:    assert(b:HasBuilding(r.Index)==want,'B055_WRITE_UNCONFIRMED');d.changes=d.changes+1
24:   end
```

### PurchaseProbe.lua

```lua
7:   local r=row(kind);local b=c:GetBuildings()
8:   if b:HasBuilding(r.Index)~=want then
9:    if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
10:   end
11:   assert(b:HasBuilding(r.Index)==want,'B053_CARRIER_UNCONFIRMED')
```

### ResearchSupport.lua

```lua
33:   if present==wanted then return end
34:   data.changes=data.changes+1
35:   if wanted then city:GetBuildQueue():CreateBuilding(id) else b:RemoveBuilding(id) end
36:   assert(b:HasBuilding(id)==wanted,"CARRIER_CHANGE_UNCONFIRMED")
37:  end
```

### Standardization.lua

```lua
30:  local function write(c,old,nextValue)
31:   assert(same(c:GetProperty(KEY),old),'STD_CONCURRENT_CHANGE')
32:   c:SetProperty(KEY,nextValue)
33:   assert(same(c:GetProperty(KEY),nextValue),'STD_WRITE_UNCONFIRMED')
34:   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'Standardization.lua') end
```

### StandardizationDiscount.lua

```lua
33:   local needed={};for id,level in pairs(want) do needed[carriers[id][level]]=true end
34:   for index in pairs(old) do if not needed[index] then
35:    b:RemoveBuilding(index);assert(not b:HasBuilding(index),'DISCOUNT_REMOVE_UNCONFIRMED');old[index]=nil;d.changes=d.changes+1
36:   end end
37:   for index in pairs(needed) do if not b:HasBuilding(index) then
38:    c:GetBuildQueue():CreateBuilding(index);assert(b:HasBuilding(index),'DISCOUNT_ADD_UNCONFIRMED');d.changes=d.changes+1
39:   end;old[index]=true end
40:  end
```

### StorageProbe.lua

```lua
29:   if write and state=="EMPTY" then
30:    b.attempts=b.attempts+1
31:    local ack=pcall(function() Game:SetProperty(key,want) end)
32:    local readOK,after=pcall(function() return Game:GetProperty(key) end)
33:    state=readOK and (equal(after,expected(pid),0) and "MATCH" or "WRITE_UNCONFIRMED") or "READBACK_ERROR"
```

### UnitActions.lua

```lua
85:     local seen=Players[pid]:GetProperty('SPC_CREW_DEV_SPAWN') or {}
86:     assert(not seen[p.Token],'SPAWN_REQUEST_ALREADY_USED');seen[p.Token]=true
87:     Players[pid]:SetProperty('SPC_CREW_DEV_SPAWN',seen)
88:     destructive=true;UnitManager.InitUnit(pid,'UNIT_SPC_CREW_250',c:GetX(),c:GetY())
89:     return 'DEV spawn requested: Crew 250. Select unit; verify appearance and 1 charge. No project paid.'
118:    local function record(state)
119:     receipts[plan.token]={state=state,unitID=plan.unitID,cityID=c:GetID(),target=s.target,amount=math.min(amount,s.cost-s.progress)}
120:     Players[pid]:SetProperty(KEY,receipts)
121:    end
122:    destructive=true;record('INTENT');u:SetProperty('SPC_CREW_RESERVED',plan.token)
123:    assert(u:GetProperty('SPC_CREW_RESERVED')==plan.token,'RESERVATION_UNCONFIRMED')
124:    Players[pid]:GetUnits():Destroy(u)
```

### YieldCarrierProbe.lua

```lua
19:   if action=='OFF' then
20:    -- OFF always available, even if the SQL definitions are missing in this save.
21:    p:SetProperty('SPC_B029_ONE',0);p:SetProperty('SPC_B029_HALF',0)
22:   elseif action=='STEP' then
23:    for _,bit in ipairs({'ONE','HALF'}) do for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do
25:    end end
26:    if not one and not half then baseline[pid..':'..c:GetID()]=read(c) end
27:    p:SetProperty('SPC_B029_ONE',1)
28:    p:SetProperty('SPC_B029_HALF',one and 1 or 0)
29:   else assert(action=='READ','ACTION') end
30:   return SPCYieldCarrierProbe.Describe(pid,c)
```

## 附录C：容器追加 / 缓存 / 重试定位

不是每一条append都是泄漏；临时数组与永久持有要区别。正文第9节列生命周期判断。

### CityInheritanceRead.lua

```lua
14:    if city and city:GetID()==s.id and city:GetOwner()==s.owner then local def=P.Info('Districts',d:GetType());s.districts[#s.districts+1]=tostring(def and def.DistrictType or d:GetType())..':'..tostring(d:IsComplete()) end
34:    rows[#rows+1]=k..'：'..(before==nil and '原无' or '原有')..' → '..(after==nil and '现无' or '现有')..' | '..(same(before,after) and '内容一致' or '内容不同')
36:   rows[#rows+1]='原始账本：专业='..tostring(j.specialization)..' | 投资笔数='..count(inv.investments)..' | 模板数='..count(std.learned)
37:   rows[#rows+1]='账本旧Owner/CityID='..tostring(j.owner)..'/'..tostring(j.cityID)..'（保留旧值不等于已适配新Owner）'
38:   rows[#rows+1]='区域：'..table.concat(s.districts,', ')
39:   rows[#rows+1]='本按钮不改Property/身份/Potential/收益；换Owner后现有机制未必可用。'
```

### CommerceConvergence.lua

```lua
40:   for bit=0,15 do local r=row(y,bit);assert(r,'DATABASE_MISSING');if b:HasBuilding(r.Index) then total=total+2^bit;bits[#bits+1]=tostring(2^bit) end end
66:     plans[#plans+1]={key=key,c=c,plan=good and plan or {amount={}},error=not good and tostring(plan) or nil}
89:   if not good then rows[#rows+1]='当前来源未就绪（旧产出不作有效来源）：'..tostring(current):match('[^\r\n]+') end
90:   if d.error or d.errors[key] then rows[#rows+1]='应用状态：'..tostring(d.error or d.errors[key]):match('[^\r\n]+') end
93:    rows[#rows+1]=y..' 源='..name..string.format(' | 基数=%.4f | 20%%/实验=%.4f | 取整=%d',p and p.basis[y] or 0,p and p.raw[y] or 0,p and p.amount[y] or 0)
95:    rows[#rows+1]='已配置='..tostring(old and (old.amount[y] or 0) or '未知')..' | 载体='..n..' ['..bits..'] | 实际='..string.format('%.4f',value)..' | OFF差值='..(base and string.format('%.4f',value-base[y]) or '无基线')
97:   rows[#rows+1]='OFF基线仅同城固定条件可比较；不同回合/人口/倍率变化会混入差值。'
99:   rows[#rows+1]='网络：'..tostring(b and b.reason)..' | 当前/样本回合='..Game.GetCurrentGameTurn()..'/'..tostring(b and b.turn)
```

### CompletionProbe.lua

```lua
79:   b.rows[#b.rows+1]=row
80:   if #b.rows>64 then table.remove(b.rows,1);b.dropped=b.dropped+1 end
```

### ConstructionProbe.lua

```lua
51:    -- One invocation only. Do not pass surplus to the engine, recurse or retry on uncertainty.
62:   return ok and out or ('B039 '..(attempted and 'RESULT_UNCERTAIN (do not retry blindly): ' or 'REJECTED: ')..short(out))
```

### CopyYields.lua

```lua
124:   lines[#lines+1]='后台='..(bg and tostring(bg.state) or '未启动')..' | 请求='..(bg and tostring(bg.requests) or '0')..' | 接收序号='..tostring(data.seq[pid] or '无')..' | 有效批次='..(s and tostring(s.turn) or '无')
125:   if bg and bg.error then lines[#lines+1]='后台原因：'..bg.error end
126:   if data.receiveErrors[pid] then lines[#lines+1]='接收原因：'..code(data.receiveErrors[pid]) end
130:    lines[#lines+1]=y..' 本项预期='..(good and tostring(n) or '暂不可判断')..' | 已配置='..(plan and tostring(plan.amount) or '未知')
133:     lines[#lines+1]='本项原因：'..code(err)
136:     lines[#lines+1]=message
139:   lines[#lines+1]='原生总量 Science='..c:GetYield(P.Info('Yields','YIELD_SCIENCE').Index)..' / Production='..c:GetYield(P.Info('Yields','YIELD_PRODUCTION').Index)
140:   if c:GetProperty('SPC_B050_HALF_ENABLED') then lines[#lines+1]='注意：B050半点实验仍开启，请先Half OFF。' end
141:   lines[#lines+1]='读取不触发刷新；已配置不是实测增量。'
```

### CrewPrecision.lua

```lua
1: -- B046 observation only. No retries, setters, grant, rounding or consumption.
```

### Dialogue.lua

```lua
5:  local levels={};for _ in GameInfo.Eras() do levels[#levels+1]=true end
72:      assert(P.Info('GreatWorks',typ),'DIALOGUE_WORK_TYPE');cities[cid][#cities[cid]+1]={id=wid,type=typ}
96:   if p.error then rows[#rows+1]='未完成：'..p.error;return table.concat(rows,'\n') end
97:   rows[#rows+1]=string.format('%s ACTIVE=%s | 合格%d件 / 排除%d件 / 创作者时代D=%d',p.specialization,tostring(p.active),p.count,p.excluded,p.d)
98:   rows[#rows+1]=string.format('理论+%d%% Culture/Tourism | 已配置%s%%',p.percent,tostring(p.applied))
99:   if p.test then rows[#rows+1]='临时本城实验：+'..p.test..'%（替换AUTO，不叠加；读档恢复AUTO）' end
100:   local eras={};for era in pairs(p.eras) do eras[#eras+1]=era end;table.sort(eras)
101:   rows[#rows+1]=table.concat(eras,', ')
102:   for i=1,math.min(3,#p.rows) do local w=p.rows[i];rows[#rows+1]=Locale.Lookup(w.name)..' → '..w.era..(w.artifact and '（文物历史时代）' or '') end
103:   rows[#rows+1]='配置≠实测；请比较下方作品实际产出，theming按原生行为。'
```

### DialogueModel.lua

```lua
17:    out.count=out.count+1;out.rows[#out.rows+1]={name=w.Name,era=era,id=entry.id,artifact=kind=='ARTIFACT'}
30:     works[#works+1]={id=id,type=row.GreatWorkType}
```

### EligibilityProbe.lua

```lua
33:     if type(pid)=="number" and pid>=0 and pid<math.huge and pid%1==0 then ids[#ids+1]=pid end
52:  -- No per-turn retries: preserve startup failures for this minimal diagnostic batch.
```

### GPPReadout.lua

```lua
14:   parts[#parts+1]=cl..":"..(ok and type(value)=="number" and tostring(value) or "UNKNOWN")
```

### Gameplay.lua

```lua
14:   shared.Events[#shared.Events+1]=line
15:   if #shared.Events>32 then table.remove(shared.Events,1) end
302:         lines[#lines+1]=e.text;shown=shown+1
306:     if shown==0 then lines[#lines+1]="NO_MATCHING_EVENT_OBSERVED (existing route may predate load)" end
342:   for i=1,math.min(select("#",...),6) do extra[#extra+1]=P.Scalar(tail[i]) end
345:   shared.TradeEvents[#shared.TradeEvents+1]={op=op,oc=oc,dp=dp,dc=dc,text=line}
346:   if #shared.TradeEvents>32 then table.remove(shared.TradeEvents,1) end
```

### GreatWorkAdjacency.lua

```lua
61:     local fields={};for field in line:gmatch('[^,]+') do fields[#fields+1]=field end
64:     local values={};for i=4,9 do local n=tonumber(fields[i]);M.Parts(n);values[#values+1]=n end
76:   for _,y in ipairs(M.Yields) do rows[#rows+1]=string.format('%s BASE=%g | 每件=%g | 配置合计(倍率前)=%g',y,p.base[y],p.base[y]/2,p.active and p.base[y]/2*p.count or 0) end
77:   rows[#rows+1]='配置不是实测；半点/作品倍率按下方原生读数验证。'
```

### GreatWorkAdjacencyModel.lua

```lua
7:  for bit=0,12 do if n%2==1 then parts[#parts+1]=sign..bit end;n=math.floor(n/2) end
18:     M.Parts(n);r[#r+1]=n
20:    rows[#rows+1]=table.concat(r,',')
```

### InheritanceShadow.lua

```lua
51:   for _,k in ipairs({'TOKEN','FLOW','JOURNAL','INVEST','TEMPLATES'}) do local now=c and c:GetProperty(fields[k]);lines[#lines+1]=k..' 备份='..(a[k]~=nil and '有' or '无')..' 当前='..(now~=nil and '有' or '无')..' 一致='..tostring(eq(a[k],now)) end
52:   lines[#lines+1]='事件记录总序号='..v.sequence..'（保留最近24条，显示最后6条）'
53:   for i=math.max(1,#v.events-5),#v.events do local e=v.events[i];lines[#lines+1]=e.seq..' '..e.name..' '..e.args..' | 位置状态 '..e.at end
54:   lines[#lines+1]='Hook '..table.concat(d.hooks,',')
55:   lines[#lines+1]='错误='..tostring(d.errors.last or '无')..'；当前位置仅观察，不认定身份继承。'
65:    if endpoint or coords then relevant=true;states[#states+1]=r.uid..':'..(c and c:GetOwner()..'/'..c:GetID() or 'NONE') end
69:   local text={};for i=1,math.min(n,8) do local x=args[i];text[#text+1]=(type(x)=='number' or type(x)=='boolean' or type(x)=='string' or x==nil) and tostring(x) or ('<'..type(x)..'>') end
70:   local v=cp(old);v.sequence=v.sequence+1;local e={seq=v.sequence,name=name,args=table.concat(text,','),at=table.concat(states,';'),turn=Game.GetCurrentGameTurn()};v.events[#v.events+1]=e
71:   if #v.events>24 then table.remove(v.events,1) end;save(old,v);print('[SPC][B064][EVENT] '..e.seq..' '..name..' '..e.args..' '..e.at)
75:   d.hooks[#d.hooks+1]=(label or name)..':'..(ok and 'ON' or 'ABSENT')
```

### Lv2GPP.lua

```lua
101:     native[#native+1]=cl..":"..(good and type(value)=="number" and tostring(value) or "UNKNOWN")
```

### Lv2Housing.lua

```lua
82:     if wanted[i] then n=n+1;if i>0 then tiers[#tiers+1]=i end end
```

### Lv3Effects.lua

```lua
7:  for _,k in ipairs({'RESEARCH','CULTURE'}) do for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_LV3_POP_'..k..'_'..i end end
8:  for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do names[#names+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
46:     else flags[#flags+1]=name:match('_COM_(%u+)$') end
102:     lines[#lines+1]='Population support: ACTIVE='..tostring(f.active)..' pop='..pop..' live workers='..tostring(workers or 'UNKNOWN')
103:     lines[#lines+1]='Base bonus expected='..expected..' carrier='..coef[f.specialization]*pop..' (not measured effect)'
104:     lines[#lines+1]='Last audit workers='..tostring(last and last.workers or 'NONE')..' native city total='..tostring(total)
106:     lines[#lines+1]='Commerce specialist +2 per type: '..(#flags>0 and table.concat(flags,',') or 'NONE')
```

### Lv3Support.lua

```lua
6:  local names={};for k in pairs(districts) do names[#names+1]='BUILDING_SPC_DEV_LV3_'..k end
7:  for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'..i end
```

### Lv4CopyRead.lua

```lua
24:     out.sources[#out.sources+1]={cityID=id,districtID=sf.first.districtID,active=sf.active}
67:       for _,key in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}) do if yields[key]~=0 then values[#values+1]=key..'='..yields[key] end end
68:       lines[#lines+1]=Locale.Lookup(row.Name)..': '..(#values>0 and table.concat(values,' ') or '0')
73:    lines[#lines+1]='科研：全部非学院区域合计='..sum..'；50%='..SPCLv4CopyRead.Half(sum)..'；ACTIVE生效预期='..(m.active==4 and SPCLv4CopyRead.Half(sum) or 0)
75:   if m.networkError then lines[#lines+1]=notice(m.networkError)
77:    if m.industryRecipient==true then lines[#lines+1]='本城已接收工业网络，但当前没有有效的工业四级来源；本项生产力预期为0。'
78:    elseif m.industryRecipient==false then lines[#lines+1]='本城尚未接收工业网络；本项生产力预期为0。'
79:    else lines[#lines+1]='工业网络接收状态尚未读取，请重新读取。' end
84:     sources[#sources+1]={cityID=s.cityID,production=value.production}
85:     lines[#lines+1]='工业来源 '..label(cities:FindID(s.cityID))..'：区域Production='..value.production..'；50%='..SPCLv4CopyRead.Half(value.production)
88:    lines[#lines+1]='本城工业接收预期：max='..amount..'；来源='..tostring(id or '无')..'（不求和）'
90:   lines[#lines+1]='上方自动复制配置与原生总量用于验收；下方来源计算不代表实测增量。'
```

### NetworkBoost.lua

```lua
12:  testRows[#testRows+1]='BUILDING_SPC_B057_'..kind..'_'..amount
114:    out[#out+1]=(kind=='RESEARCH' and '科研→鼓舞' or '文化→尤里卡')..(p and string.format(' | ACTIVE=%d N=%d | 预期+%.6f百分点',p.level,p.n,p.amount) or ' | 待后台刷新')
115:    if p and not p.test then out[#out+1]=string.format('Raw=%.6f FinalRaw=%.6f → Applied=%d',p.raw,p.finalRaw,p.amount) end
116:    out[#out+1]='配置='..tostring(a and a.amount or 0)..' | k='..SPCBoostConfig.k[kind]
118:   if d.testRaw[pid]~=nil then out[#out+1]=string.format('FinalRaw=%.6f → floor(raw+0.5)=%d；重载退出实验',d.testRaw[pid],SPCNetworkBoost.Quantize(d.testRaw[pid])) end
119:   out[#out+1]='状态='..tostring(d.errors[pid] or (d.ready and 'READY' or 'PENDING'))
120:   out[#out+1]='配置≠实测；读取基线后同回合触发一次未触发的尤里卡/鼓舞，再读取。'
```

### NetworkBridge.lua

```lua
44:     rows[#rows+1]={op=a,oc=o,dp=c,dc=z,trader=u}
133:   for src in pairs((recipients[kind] or {})[selected:GetID()] or {}) do result[#result+1]=src end
158:      entries[#entries+1]="接入 "..labels[sources[src]]..": "..name(pid,src)..(src==id and " [首都自身]" or " [直连]")
162:       entries[#entries+1]="接收 "..labels[k]..": 来源 "..name(pid,src)
167:       entries[#entries+1]="商路 "..name(route.op,route.oc).." → "..name(route.dp,route.dc)
177:     for i=(page-1)*3+1,math.min(page*3,#entries) do lines[#lines+1]=entries[i] end
178:     lines[#lines+1]="再次点网络明细翻页；接收来源不等于可转发来源。"
179:     lines[#lines+1]="DEV网络状态；商业III专家奖励另按ACTIVE门控。"
190:     lines[#lines+1]=labels[k]..": 本中心接入来源="..connected.." | 全国接收城市="..size(set).." | 本城接收="..(set[id] and "是" or "否")
192:    lines[#lines+1]="来源数≠接收城市数；网络明细可看城市/方向。DEV网络；商业III专家奖励另按ACTIVE门控。"
```

### NetworkSender.lua

```lua
15:     local r=s.routes[key];data[#data+1]=table.concat({r.originPlayer,r.originCityID,r.destinationPlayer,r.destinationCityID,r.traderUnitID},",")
```

### Probe.lua

```lua
50:   out[#out+1]="City="..tostring(cityID).." "..city:GetName().." | CIVILIZATION_SPC_TEST / LEADER_SPC_TEST"
51:   out[#out+1]="Marker="..tostring(val(city,"GetProperty","SPC_P0_MARKER")).." | Spec(test)="..tostring(val(city,"GetProperty","SPC_P0_FIRST_SPEC"))
52:   out[#out+1]="Potential/Active=NOT_IMPLEMENTED (no invented levels)"
73:   out[#out+1]="Governor established="..tostring(gov and val(gov,"IsEstablished") or false)
76:   out[#out+1]="Engine Req2/3/4 raw="..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_2")).."/"
82:       out[#out+1]=(info and info.DistrictType or tostring(d:GetType())).." workers="..tostring(val(plot,"GetWorkerCount"))
85:   if not enumOK then out[#out+1]="DISTRICTS UNKNOWN: "..tostring(err) end
103:   local ok, err = pcall(function() for row in info() do rows[#rows+1] = row end end)
114:   for k in pairs(v) do keys[#keys+1] = k end
116:   for _,k in ipairs(keys) do out[#out+1] = tostring(k).."="..P.Encode(v[k],seen) end
153:     lines[#lines+1] = "[SPC]["..P.VERSION.."]["..context.."][turn="..tostring(turn)
363:     out[#out+1]="lookup=NATIVE_REQUIREMENTS (no governor Lua getter)"
367:     out[#out+1]="control="..P.Scalar(control).." | present="..P.Scalar(present).." established="..P.Scalar(established)
369:     for n=2,4 do raw[#raw+1]=P.Scalar(get(city,"GetProperty","SPC_P0_GOV_REQ_"..n)) end
370:     out[#out+1]="Established title thresholds 2/3/4="..table.concat(raw,"/")
372:       out[#out+1]="NOT_READY: native probe control missing; do not infer no governor"
374:       out[#out+1]="CONTROL_OK: raw conditions still require state-change validation"
376:     out[#out+1]="1=condition active; nil/0=inactive candidate. No exact title count inferred."
378:     out[#out+1]="ROLE cityKey="..P.Scalar(role.cityKey).." | capital="..role.capitalStatus.." | center="..role.centerStatus
379:     out[#out+1]="Specialization=UNKNOWN | Potential=UNKNOWN | ACTIVE=UNKNOWN (no persistent writer)"
380:     out[#out+1]="Governor ceiling="..P.Scalar(role.governorLevelCeiling).." | "..role.governorGateStatus.." (not ACTIVE)"
381:     out[#out+1]="Legacy spec diagnostic="..P.Scalar(role.legacySpecDiagnostic).." (not adopted)"
409:         out[#out+1]=P.Scalar(info.DistrictType).." workers="..workers.." complete="..tostring(complete)
413:     if count==0 then out[#out+1]="NO_SPECIALTY_DISTRICT (not a specialist test pass)" end
415:   out[#out+1]="RAW_API_ONLY | USER_GAME_TEST_REQUIRED"
447:           list[#list+1]={district=d,info=info,id=get(d,"GetID"),type=dt}
454:     out[#out+1]="district "..index.."/"..#list.." id="..item.id.." "..P.Scalar(item.info.DistrictType)
455:     out[#out+1]="complete="..P.Scalar(get(d,"IsComplete")).." | BASE_CANDIDATE / ACTUAL_CANDIDATE"
469:       out[#out+1]=P.Scalar(yield.YieldType)..": "..number(bok,b).." / "..number(aok,a)
472:     out[#out+1]="UI_ONLY: UNKNOWN is not zero; policy/cross-yield semantics unverified"
482:       list[#list+1]=row
486:     diagnostics[#diagnostics+1]="UI OUTGOING rawCount="..#list.." (not recipient N)"
487:     if #list==0 then out[#out+1]="本城当前没有出发商路。";diagnostics[#diagnostics+1]="NO_OUTGOING_ROUTES" else
489:       out[#out+1]="当前第 "..index.." / "..#list.." 条 · Next district / route 查看下一条"
490:       diagnostics[#diagnostics+1]="route "..index.."/"..#list.." trader="..P.Scalar(P.Field(row,"TraderUnitID"))
506:       out[#out+1]="出发："..originName
507:       out[#out+1]="到达："..destinationName
508:       diagnostics[#diagnostics+1]="FROM "..originDetail
509:       diagnostics[#diagnostics+1]="TO   "..destinationDetail
510:       diagnostics[#diagnostics+1]="originMatchesSelection="..tostring(op==owner and oc==id)
511:       diagnostics[#diagnostics+1]="sameOwnerRaw="..(type(op)=="number" and type(dp)=="number" and tostring(op==dp) or "UNKNOWN")
513:     out[#out+1]="仅显示商路端点；尚未判定专业网络接收关系。"
514:     out[#out+1]=""
515:     out[#out+1]="排错信息（无需手抄 ID）"
516:     out[#out+1]=table.concat(diagnostics,"\n")
```

### PurchaseProbeRead.lua

```lua
11:   out[#out+1]=ok and v or '价格接口不可读，请查看原生购买面板并回传截图。'
13:  out[#out+1]='请分别打开金币/信仰购买页核对；不要实际购买。'
```

### QualificationProbe.lua

```lua
53:    if not seen[pid] then seen[pid]=true;ordered[#ordered+1]=pid end
62:    elseif e.status=="ENABLED" then out.enabled[#out.enabled+1]=pid
150:   local function flush() if first~=nil then out[#out+1]=first==last and tostring(first) or (first.."-"..last) end end
163:    if data.permissions[pid] then permitted[#permitted+1]=pid end
164:    if latest.unknown[pid] then unknown[#unknown+1]=pid end
169:     local target=latest.current[pid] and present or absent;target[#target+1]=pid
```

### ResearchSupport.lua

```lua
99:     if row and city:GetBuildings():HasBuilding(row.Index) then enabled[#enabled+1]=k end
```

### ShadowRouteState.lua

```lua
28:     traders[r.traderUnitID]=true;keys[#keys+1]=key
41:   local current,lastGood,revision=nil,nil,0
45:   function state:Reset() current=nil;lastGood=nil;revision=0;reason="CONTEXT_RESET" end
49:     if lastGood and lastGood.player~=nextState.player then self:Reset() end
51:     for _,k in ipairs(nextState.orderedKeys) do if not lastGood or not lastGood.routes[k] then added=added+1 end end
52:     if lastGood then for _,k in ipairs(lastGood.orderedKeys) do if not nextState.routes[k] then removed=removed+1 end end end
53:     if not lastGood or nextState.fingerprint~=lastGood.fingerprint then revision=revision+1 end
55:     current=nextState;lastGood=nextState;reason=nil
```

### SourceYieldProbe.lua

```lua
13:   if nameOK and type(name)=='string' then lines[#lines+1]='name='..name end
21:     lines[#lines+1]=key..' total='..string.format('%.6f',value)
24:     lines[#lines+1]=key..' UNKNOWN: '..err:sub(1,100)
27:   lines[#lines+1]='Includes outside inputs; NOT verified local-only basis.'
```

### Standardization.lua

```lua
93:     local function retry(id,e)
111:       else retry(id,e) end
115:     -- Unknown facts are retained for bounded retries; never guess or erase old knowledge.
116:     if not ok then for id,e in pairs(q.buildings) do retry(id,e) end end
131:    if v==nil then lines[#lines+1]='尚无账本：非工业专业或后台初始化尚未完成。'
134:     for id in pairs(v.learned) do ids[#ids+1]=id;if cat.buildings[id] and cat.buildings[id].enabled then enabled=enabled+1 end end;table.sort(ids)
136:     lines[#lines+1]='已初始化 | 模板='..#ids..' | revision='..v.revision..' | 页 '..page..'/'..pages
137:     lines[#lines+1]='折扣范围内='..enabled..' | 仅保留='..(#ids-enabled)..'（不代表当前可金币购买）'
141:      lines[#lines+1]=label..' | T'..receipt.tier..' | '..(row and row.group or '需分类迁移')
144:    lines[#lines+1]='本次加载：首次扫描='..data.scans..' / 写入='..data.writes
145:    lines[#lines+1]='最近记录='..tostring(data.last[key(pid,c:GetID())] or '无新增')
146:    lines[#lines+1]='状态='..tostring(data.errors[key(pid,c:GetID())] or data.warnings[key(pid,c:GetID())] or '正常')
147:    lines[#lines+1]='只读永久模板；当前折扣另见Read discounts。'
```

### StandardizationDiscount.lua

```lua
22:    maxLevel=math.max(maxLevel,f.active);sourceNames[#sourceNames+1]=tostring(source:GetName())..' ACTIVE '..f.active
58:      parts[#parts+1]='C'..id..':'..c:GetX()..':'..c:GetY()
59:      for building,l in pairs(targets[id]) do parts[#parts+1]=id..':'..building..':'..l end
101:   local info=plan.info[c:GetID()];local targets=plan.targets[c:GetID()] or {};local ids={};for id in pairs(targets) do ids[#ids+1]=id end;table.sort(ids)
107:    lines[#lines+1]=Locale.Lookup(catalog.buildings[id].name)..' | 配置='..(applied[index] and targets[id]*10 or 0)..'%'
110:   if err then lines[#lines+1]='状态='..(tostring(err):match('DISCOUNT_[A-Z_]+') or '来源/后台待更新') end
111:   lines[#lines+1]='只读；原生价格以购买页为准，允许同一合格建筑双币折扣。'
```

### TradeRouteProbe.lua

```lua
58:         rows[#rows+1]={id=id,text=line,display=compact,match=match}
71:       local dirtyList={};for k in pairs(pending) do dirtyList[#dirtyList+1]=k end;table.sort(dirtyList);pending={}
84:             lines[#lines+1]="CANDIDATE_ONLY engineCount="..r.engineCount.." traders="..r.traders.." matchingOperations="..r.matched.." unknownOperations="..r.unknown
85:             display[#display+1]="引擎路线计数："..r.engineCount.."；商人数量："..r.traders
86:             display[#display+1]="匹配建商路任务："..r.matched.."；未知任务类型："..r.unknown
87:             for _,row in ipairs(r.rows) do lines[#lines+1]=row.text end
88:             display[#display+1]="端点仍属候选：nil表示缺失，不是有效坐标。"
89:             for j=1,math.min(#r.rows,6) do display[#display+1]=r.rows[j].display end
90:             if #r.rows>6 then display[#display+1]="其余任务未显示；共"..#r.rows.."名商人，不据截断显示认定全集。" end
91:             display[#display+1]="候选读取成功 ≠ 当前路线集合验证通过。"
93:             lines[#lines+1]="UNAVAILABLE "..scalar(r)
94:             display[#display+1]="候选接口不可用："..shortError(r)
96:           display[#display+1]="正式路线来源：BLOCKED；未启用网络或收益。"
```

### UI/BackgroundRoutes.lua

```lua
10: local lastGood,firstComplete,lastChange
20: local attempts,retryPending=0,false
30: local function ordered(map) local a={};for k in pairs(map) do a[#a+1]=k end;table.sort(a);return a end
97:     lines[#lines+1]="状态：COMPLETE_UI_SHADOW | turn="..s.turn.." | seq="..generation
98:     lines[#lines+1]="触发："..public.reason.."；本玩家当前商路："..s.count
99:     lines[#lines+1]="Gameplay对照："..comparison(s)
100:     if firstComplete then lines[#lines+1]="首次自动完成："..firstComplete.reason.." / "..firstComplete.count.."条" end
101:     if lastChange then lines[#lines+1]="最近变化：+"..lastChange.added.." / -"..lastChange.removed end
102:     if lastChange and lastChange.firstRemoved then lines[#lines+1]="已移除："..lastChange.firstRemoved end
103:     for i=1,math.min(#s.keys,6) do lines[#lines+1]=i..". "..s.routes[s.keys[i]].display end
104:     if #s.keys>6 then lines[#lines+1]="仅显示前6条；缓存完整数量="..s.count end
106:     lines[#lines+1]="状态："..public.status.."；原因："..(public.error or pendingReason)
107:     lines[#lines+1]="没有可用的当前快照；不把未知当零条，也不使用旧结果。"
109:   lines[#lines+1]="刷新次数="..generation.."；系统通知="..systemPulses.."；Context更新="..contextPulses
110:   lines[#lines+1]="发布完成="..publishPulses.."；播放完成="..playbackPulses.."；本批尝试="..attempts.."/3"
111:   lines[#lines+1]="采样入口："..lastFlush
112:   lines[#lines+1]="标准缓存："..normalized:Summary()
113:   lines[#lines+1]="此按钮只看缓存，不触发采样。"
121:   attempts=0;retryPending=false
129:     lastGood=nil;firstComplete=nil;lastChange=nil;normalized:Reset()
140:     if lastGood and lastGood.player~=pid then lastGood=nil;firstComplete=nil;lastChange=nil end
141:     for _,k in ipairs(s.keys) do if not lastGood or not lastGood.routes[k] then added=added+1 end end
142:     if lastGood then for _,k in ipairs(lastGood.keys) do if not s.routes[k] then removed=removed+1;firstRemoved=firstRemoved or lastGood.routes[k].display end end end
143:     if added>0 or removed>0 or not lastGood then lastChange={added=added,removed=removed,firstRemoved=firstRemoved} end
145:     lastGood=s;public.snapshot=s;public.status=s.status;public.reason=pendingReason;public.error=nil
154:     if lastGame~=nil then lastGood=nil;firstComplete=nil;lastChange=nil;normalized:Reset() end
168:   retryPending=public.status=="UNKNOWN" and attempts<3
179:     event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
202:           if dirty or retryPending then dispatch(name) else render() end
204:         if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;retryPending=false;render() end
206:       event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
220:     systemEvent.Add(callback);hooks[#hooks+1]={event=systemEvent,callback=callback}
```

### UI/BoostGreatWorkRead.lua

```lua
24:     rows[#rows+1]=v.name..string.format(' | cost=%.4f | %.4f→%.4f | Δ=%.4f (%.6f%%)',v.cost,old.progress,v.progress,delta,v.cost>0 and delta/v.cost*100 or 0)
29:   if #rows>3 then for i=#rows,4,-1 do rows[i]=nil end;rows[#rows+1]='本次多于3项；为便于比较，每次只触发一项。' end
30:   if turn~=baseline.turn then rows[#rows+1]='已跨回合：Δ含正常研究，不能据此判断Boost精度。' end
31:   rows[#rows+1]='百分比是总进度变化/成本，含原有Boost；临近完成会受剩余需求限制。'
50:     signature[#signature+1]='B'..r.Index..':'..tostring(tval)
53:       seen[id]=true;count=count+1;signature[#signature+1]='W'..id..'@'..r.Index
56:       names[#names+1]=Locale.Lookup(w.Name)..' ['..w.GreatWorkObjectType..'/'..tostring(w.EraType)..']'
68:    rows[#rows+1]=string.format('对照T%d → T%d：作品ΔC=%+.4f / ΔT=%+.4f；整城ΔC=%+.4f',a.turn,turn,culture-a.culture,tourism-a.tourism,total-a.total)
69:    rows[#rows+1]=(sig==a.signature and '收藏/所在建筑/主题状态一致；' or '注意：收藏或建筑/主题状态已变化；')..'跨回合差值可能含人口/专家等其它变化。'
72:   if bg then rows[#rows+1]='事件后台：扫描='..bg.scans..' / 发送='..bg.sends..' / '..bg.state..' / '..bg.reason;rows[#rows+1]='传输：重发='..tostring(bg.retries or 0)..' / API返回='..tostring(bg.transport or 'NONE') end
73:   rows[#rows+1]=string.format('主题化建筑=%d / 未知=%d；其中作品C=%.4f / T=%.4f',themed,themeUnknown,themedCulture,themedTourism)
74:   for i=1,math.min(2,#names) do rows[#rows+1]=names[i] end
75:   if #names>2 then rows[#rows+1]='另有'..(#names-2)..'件，完整名称请看巨作界面。' end
89:   for _,y in ipairs(ys) do rows[#rows+1]=string.format('%s %.4f / %.4f',y,totals[y],c:GetYield(P.Info('Yields','YIELD_'..y).Index)) end
```

### UI/BoostRefresh.lua

```lua
1: -- Background startup retry: no dependency on opening P0 or the native trade screen.
14:   local e=P.Field(Events,name);if e and e.Add then e.Add(refresh);hooks[#hooks+1]=e end
```

### UI/CopyYieldRefresh.lua

```lua
26:     rows[#rows+1]=c:GetID()..','..d:GetID()..','..string.format('%.17g',sum)..','..string.format('%.17g',prod)
51:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
```

### UI/CrewProjectOrder.lua

```lua
11:    insertion=insertion or (#others+1);crew[#crew+1]=item
12:   else others[#others+1]=item end
18:   if i==insertion then for _,item in ipairs(crew) do result[#result+1]=item end end
19:   if others[i] then result[#result+1]=others[i] end
```

### UI/DialogueRefresh.lua

```lua
6: local public={scans=0,sends=0,retries=0,state='STARTUP',reason='INITIALIZATION'}
26:    if pending.pulses>=3 and pending.retries<2 then
27:     pending.pulses=0;pending.retries=pending.retries+1;public.retries=public.retries+1
29:     if pending==flight and flight.retries>=2 then public.state='ACK_TIMEOUT' end
50:   local cities={};for _,c in Players[pid]:GetCities():Members() do cities[#cities+1]=c end
53:    local id=c:GetID();rows[#rows+1]=id..',-1,EMPTY'
54:    for _,w in ipairs(SPCDialogueModel.Collect(P,c)) do rows[#rows+1]=id..','..w.id..','..w.type end
55:    local f=s.EffectiveFacts.Read(pid,c);signature[#signature+1]=id..':'..f.specialization..':'..f.active
68:   pending={seq=seq,turn=turn,generation=s.Dialogue.generation,packet=packet,pulses=0,retries=0};public.state='WAIT_ACK'
78:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
```

### UI/DiscountEligibility.lua

```lua
30:     rows[#rows+1]=cid..','..b.Index..','..(allowed and '1' or '0');count=count+1
49: local function bind(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f);hooks[#hooks+1]={e,f} end end
```

### UI/GPPRefresh.lua

```lua
23:  if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
```

### UI/GreatWorkBasis.lua

```lua
18:    rows[#rows+1]={id=w.id,name=w.name,group=group,baseFirst=first,baseTourism=tour}
43:     works[#works+1]={id=id,name=Locale.Lookup(w.Name),object=w.GreatWorkObjectType,culture=y.YIELD_CULTURE or 0,faith=y.YIELD_FAITH or 0,tourism=number(w.Tourism),building=r.Index,slot=slot}
55:    rows[#rows+1]=string.format('%s组%d件 | 最高基础 %g / %g旅游 | 应补总量 %g / %g旅游',kind=='CULTURE' and '文化' or '遗物信仰',g.count,g.first,g.tourism,g.totalFirst,g.totalTourism)
58:    rows[#rows+1]=string.format('%s | 基础%g/%g旅游 → 补%g/%g旅游',w.name,w.baseFirst,w.baseTourism,w.addFirst,w.addTourism)
60:   if #p.rows>4 then rows[#rows+1]='另有'..(#p.rows-4)..'件已计入；显示前4件。' end
61:   rows[#rows+1]='排除遗物/产品/未知类型='..p.excluded..'；按当前作品重算，不保存最高值。'
```

### UI/IndustryRefresh.lua

```lua
25:      -- Mark before request to prevent synchronous publish recursion; retry send errors.
40:  local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
```

### UI/P0Panel.lua

```lua
82: -- B060 read/control requests are idempotent. Only an outstanding click may retry;
90:   if f.retries>=2 then
95:   f.retries=f.retries+1;f.busy=true
147:   if action:find('^GWA_') then gwaFlight={pid=playerID,packet=packet,pulses=0,retries=0,busy=true} end
196:   for i=last,math.max(1,last-1),-1 do lines[#lines+1]=b.rows[i].text end
197:   if #b.rows==0 then lines[#lines+1]="本次脚本加载后无记录；不代表城市从未建过区域。" end
198:   lines[#lines+1]="计数每次读档重置；未写专业/Potential。截图即可。"
226:       lines[#lines+1]="无当前版本加载结束记录；此按钮不会采样。"
229:       for pid,row in pairs(sample.rows) do if row.status=="UNKNOWN" then ids[#ids+1]=pid end end
233:       lines[#lines+1]="汇总="..sample.status.." 未知="..sample.unknown.." 页="..unknownPage.."/"..pages
240:         lines[#lines+1]="player="..pid.." | "..(code or raw:sub(1,90))
242:       if #ids==0 then lines[#lines+1]=sample.reason or "没有逐槽位UNKNOWN记录。" end
253:       lines[#lines+1]="没有当前版本记录；此按钮不会启动采样。"
255:       lines[#lines+1]="LoadScreenClose="..tostring(d.hooks.LoadScreenClose)
259:         lines[#lines+1]=phase.." | "..(row and row.status or "NO_RECORD")
262:           lines[#lines+1]="汇总="..sample.status.." 启用="..sample.enabled.." 未启用="..sample.disabled.." 未知="..sample.unknown
266:     lines[#lines+1]="只读；未写资格或城市成果。截图即可。"
```

### UI/UnitSites.lua

```lua
48:    out[#out+1]=i..'：'..n(s.cost*multiplier/100)..' / '..n(q:GetProjectCost(project.Index))..' / '..n(q:GetProjectProgress(project.Index))..' / '..n(P.CrewAmount('UNIT_SPC_CREW_'..s.charge))
54:   local parts={};for i,s in ipairs(P.Specs) do parts[#parts+1]=i..'级='..(counts[s.charge] or 0) end
55:   out[#out+1]='当前己方施工队数量：'..table.concat(parts,'，')
57:    out[#out+1]='最近一次确认（回合'..n(sample.turn)..'，城市ID '..n(sample.cityID)..'）：'
58:    if sample.error then out[#out+1]='施工前读取未知：'..sample.error end
59:    out[#out+1]='原进度='..n(sample.before)..'；施工后='..n(sample.after)..'；原成本='..n(sample.cost)
60:    out[#out+1]='预期增加='..n(sample.expected)..'；实际增加='..n(sample.observed)..'；差值='..n(sample.difference)
61:    out[#out+1]='单位仍存在='..tostring(sample.unitPresent)..'；'..tostring(sample.note or sample.afterReadError or '同一目标可比较')
62:    if sample.difference then out[#out+1]=math.abs(sample.difference)<0.000001 and '本次读取数值相符；仍请核对实际游戏结果。' or '本次存在数值差异，请回传此报告；尚未采用取整规则。' end
63:   else out[#out+1]='尚无本次加载后的施工确认记录。' end
```

### UI/UnitTargetMarkers.lua

```lua
8:  if manager then manager:ResetInstances() end
48:       local instance=manager:GetInstance();local x,y=UI.GridToWorld(r.plot)
71:   local e=Events[name];if e then e.Add(changed);hooks[#hooks+1]={e,changed} end
```

### UnitActions.lua

```lua
86:     assert(not seen[p.Token],'SPAWN_REQUEST_ALREADY_USED');seen[p.Token]=true
117:    local receipts=Players[pid]:GetProperty(KEY) or {};assert(not receipts[plan.token],'RECEIPT_EXISTS')
119:     receipts[plan.token]={state=state,unitID=plan.unitID,cityID=c:GetID(),target=s.target,amount=math.min(amount,s.cost-s.progress)}
140:   local output=ok and result or ((destructive and 'HELD / RESULT UNCERTAIN (do not retry): ' or 'REJECTED: ')..tostring(result):match('[^\r\n]+'))
```

### UnitSiteProbe.lua

```lua
18:    lines[#lines+1]='City='..city:GetName()..' #'..city:GetID()
22:     if c and c:GetOwner()==pid and c:GetID()==city:GetID() then districts[#districts+1]=d end
26:     lines[#lines+1]=name..': '..(good and value or ('UNKNOWN '..tostring(value):match('[^\r\n]+')))
75:    lines[#lines+1]=(info.UnitType=='UNIT_SPC_CREW_250' and ('Crew 250 | charges='..unit:GetBuildCharges()..'. Use Prepare / Confirm unit action.') or 'No action executed. Builder is a location tester, not a Crew.')
76:    lines[#lines+1]='Existing investment still uses city center. Candidate site rules only.'
```

### UnitTargets.lua

```lua
18:      local id=c:GetID();districts[id]=districts[id] or {};table.insert(districts[id],d)
33:         candidates[#candidates+1]=Map.GetPlot(d:GetX(),d:GetY())
53:          if pc and pc:GetOwner()==pid and pc:GetID()==c:GetID() then candidates[#candidates+1]=p;scanned[index]=true end
61:          candidates[#candidates+1]=Map.GetPlot(d:GetX(),d:GetY())
71:     if good and value and not seen[value.plot] then seen[value.plot]=true;response.plots[#response.plots+1]=value
72:     elseif not good then response.unknown[#response.unknown+1]={cityID=c:GetID(),reason=tostring(value):match('[^\r\n]+')} end
```

### YieldCarrierProbe.lua

```lua
42:    lines[#lines+1]=y..' total='..string.format('%.6f',current[y])..' delta='..(base and string.format('%.6f',current[y]-base[y]) or 'NO_BASELINE_THIS_LOAD')
44:   lines[#lines+1]='OFF required after test. Modifiers may amplify base amounts.'
```

## 附录D：历史差异与完整性

### B060.85 → B067.93

| File | Difference |
|---|---|
| `BindingProbe.lua` | CHANGED |
| `CityFlowProbe.lua` | CHANGED |
| `CityInheritance.lua` | NEW |
| `CityInheritanceRead.lua` | NEW |
| `CityJournalProbe.lua` | CHANGED |
| `CommerceConvergence.lua` | NEW |
| `Data/CommerceConvergence.sql` | NEW |
| `Data/Dialogue.sql` | CHANGED |
| `DialogueModel.lua` | CHANGED |
| `Gameplay.lua` | CHANGED |
| `InheritanceShadow.lua` | NEW |
| `InvestmentAction.lua` | CHANGED |
| `NetworkBridge.lua` | CHANGED |
| `NetworkSender.lua` | CHANGED |
| `Probe.lua` | CHANGED |
| `SpecializationP0.modinfo` | CHANGED |
| `Standardization.lua` | CHANGED |
| `UI/P0Panel.lua` | CHANGED |
| `UI/P0Panel.xml` | CHANGED |

### B067.93 → 当前B068.95

- `Data/Colors.sql`
- `DiagnosticLog.lua`
- `Gameplay.lua`
- `Probe.lua`
- `SpecializationP0.modinfo`
- `UI/BoostRefresh.lua`
- `UI/CityPotential.lua`
- `UI/CityPotential.xml`
- `UI/CopyYieldRefresh.lua`
- `UI/DialogueRefresh.lua`
- `UI/DiscountEligibility.lua`
- `UI/GPPRefresh.lua`
- `UI/IndustryRefresh.lua`
- `UI/P0Panel.lua`
- `UI/P0Panel.xml`
- `UI/UnitPanelActions.lua`
- `UI/UnitSites.lua`
- `UI/UnitSites.xml`
- `UI/UnitTargetMarkers.lua`
- `UI/UnitTargetMarkers.xml`

### 读取时校验

- B067.93原manifest全部Mod条目核对一致：111项；未修改冻结备份。
- B067.93: 111 files；本报告复算摘要SHA256（sorted path TAB sha256 LF）：`ae636ea4e54c46dff864311f8a6bddca893b7c0767fb236b33d6c97805eebc42`。
- current canonical: 114 files；本报告复算摘要SHA256（sorted path TAB sha256 LF）：`7ea80c290b098931df40b9ec2c76b3fc9fe6e654d65f61d47ba68a8001a6ecd8`。
- deployment: 114 files；本报告复算摘要SHA256（sorted path TAB sha256 LF）：`7ea80c290b098931df40b9ec2c76b3fc9fe6e654d65f61d47ba68a8001a6ecd8`。
- 当前源码与部署逐文件一致。D0025 SHA256：`81dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b`。
- 报告生成前后：Mod、DevelopmentTests、既有Specialization文档、B067备份、部署副本逐文件hash不变；唯一新增项目文件为本报告。未commit/push/deploy、未改游戏配置、未运行游戏。
