# P06b — 城市身份事件证据与生命周期传播

独立审计 IA20261007 / W13；基线 `32971f6390f1be9dac534345f3cdc8abc7162ca5`。slice覆盖完成，不是总审计或新的native PASS。只写审计产物。

## 问题与结论

本slice回答：**永久record如何接收native生命周期事件并证明当前对象连续性；记录增加后分发成本如何增长，UNKNOWN通知是否能可靠后补？** 复用P06a保存、P07a–c事务，不逐能力重做收益/保存验收。

- **IA-P06b-F01：MEDIUM / FIX_BEFORE_NEXT_PROFESSION。** 已登记的O(C)事件广播有可收窄的native定位成本；无关外国Transfer在C=1/4/20/40时分别GetCityAt1/4/20/40次。不是新性能regression，不证明当前卡顿。新增lifecycle consumer/专业前宜明确候选路由与必要fallback责任。
- **IA-P06b-Q01：MEDIUM / MONITOR。** 一次Transfer发生时对象nil/throw/仍旧引用会被过滤；后续Initialized/Load无法仅凭当前foreign对象补出匹配loss。局部复现事实成立，native时序未知。当前facts拒读仍保护资格，不等于外国Owner继续运行或实际残留yield已证实。
- 同一持久城的结构观察、路由与native连续性证据有区别。没有发现原token/严格tokenless链被城市名或坐标猜测取代；多foreign hop、毁城同址新代和未知取得仍有明确已知支持限制。

## Identity / proof职责

| 层 | 真正保证 | 不保证 |
|---|---|---|
| [CityIdentityRead](../../../Mod/CityIdentityRead.lua) | 复制预算、旧record结构/锚点一致；Preview/Compare观察 | Preview始终migrationAllowed=false、cityKey=nil、generation UNKNOWN；LOCAL_CANDIDATE不是世代证明或迁移授权 |
| Store.Owns / positions | 按登记位置定位worker、阻止legacy fallback和重复登记 | 位置命中本身不证明新native对象是原城市 |
| canonical token / origin | 本存档接受范围内固定serial/origin绑定 | 不是通用cityKey；token缺失不能直接复制旧token给新对象 |
| current/currentFirst | 接受返回后当前Owner/ID/区域ID，独立于历史origin | 不改历史receipt/first.turn，不恢复旧Governor/route样本 |
| loss/lastLoss/returnProof | 精确foreign endpoint与已接受连续性证据 | 只留当前/最近slot，不复原未保存的session事件链或任意foreign hop |
| referenceInvalidated | 原ACTIVE current被确切Removed时暂停读 | 缺城市不自动判毁灭，也不为新同址城释放旧history |

源码：[Store](../../../Mod/CityProgressionStore.lua)31–44、130–159、188–248、492–638、794–805、918–1008、1168–1179；[FreshBindingHook](../../../Mod/FreshBindingHook.lua)5/12仍DEV wrapper、生产BlocksLegacy拦截；[CityFlow](../../../Mod/CityFlowProbe.lua)126–138正式先走Store，未登记生产城不读旧FLOW冒充历史。

## 正式转换map

| 转换 | 必要事实 / 结果 |
|---|---|
| 新局index初始化 | existing index只加载；缺index须start turn、单个enabled human、零城/无旧authority/读回。未知IsSavedGame或旧档不自动创建 |
| 正常新城 | FOUND_CITY UnitActivate＋Initialized同回合、同Owner/位置/reference；不要求已消耗Settler对象尚在 |
| 首次无历史征服 | Conquered→Added→Initialized→Transfer严格链，Major/City-State合格来源；一次冻结LegacySet，后建不追加 |
| 原专业/候选城loss | 匹配Transfer参数与真实当前对象才写HELD_TRANSFER/loss，再module-owned退出；UNKNOWN不补造 |
| retained token原Owner返回 | 已存loss/匹配old foreign Owner、新current真实ref、原token、退出全部确认；无pending；专业城还核唯一完整同type区域 |
| tokenless返回 | 已观察精确foreign endpoint，同回合Removed<Added<Initialized<Transfer严格proof；冲突暂停。含CityBuilt再要求匹配typed Conquered/version2 |
| 接受返回后load | 从current/lastLoss/returnProof验证；native token仍nil可由已保存接受proof支持，冲突token拒绝 |
| 链中途load | 不重建消失的session链，不按当前对象推断已经返回 |

[Spec ELIG/PROG](../../Design/Specialization_v0.1_Design_Spec.md)决定Gameplay；[E2相应合同](../../Architecture/v2/P0_E2_Plan.md)与直接源码决定现行支持边界。原Owner当前四专业单人范围不反向改写未来enabled AI语义。Probe实际资格不假定player0；选定fixture仍明确stub pid0，不能冒充完整资格实机联合证据。

六类native观察slot各只存最近≤6参数，不是无限事件日志；只在相关worker后才observe。returned district全集查询用于一次真实接受返回时验证旧first type唯一性，不能为省扫描删掉此门禁。

## Confirmed — IA-P06b-F01：事件候选定位仍广播

令C为所有已登记workers，Cready为ready/无fault/有root。manager1172–1174对七类事件逐worker Handle；过滤在worker内部，而modern普通寻址已有positions[x:y]→token→worker。

| 通知 | 单次成本 / 近似复杂度 | 保留原因 / worst case |
|---|---|---|
| Transfer | C次Handle；Cready个GetCityAt，存在对象再建ref/读4getters；相关worker另reconcile/exit定位 | foreign退出事件必要，但无关foreign也付C查询；Ftransfer×Cready定位 |
| Added/Initialized/Built/Conquered | C次坐标比较，相关worker才track/reconcile | 固定坐标候选可复用现有positions；加载W个native city通知时比较约W×C |
| Removed | 每Cready最多3个endpoint比较，临时endpoint数组/空表 | current-or-origin、loss.target、transition.to都需覆盖，不能仅索引origin ID |
| LoadScreenClose | C次恢复reconcile，HELD额外Exit定位 | load全记录复核有独立职责，不能机械用增量代替 |
| 真实return | 相关一次Dplayer区域遍历及具名return callbacks | Freturn×Dplayer；保留完整/唯一/当前资格验证 |

最小actual Store fixture：C=1/4/20/40普通登记P0 record，一条与全部记录无关的foreign Transfer，各调用GetCityAt1/4/20/40，永久写0。无需Governor资格假设；这与P13a Dcache可达C_D>8的UNKNOWN不同。

[脚本](Evidence/W13/reproduce_lifecycle_dispatch.py)只计native function入口；mock GetCityAt自身线性找城市的成本不算production O(C²)。本轮没有计latency、实际分配、engine实现或事件频率，也没有单位移动/per-frame触发证据。

**MEDIUM / FIX_BEFORE_NEXT_PROFESSION。** 这是已声明保守广播的扩展方向，不是B108新回归。现在调整候选入口主要限Store manager/索引和定向测试；未来更多状态/consumer会使全广播验证成本与fallback责任更难统一。先收窄已有坐标事件，不需新cityKey或全事件总线；Load、异常fallback仍有职责。

候选边界：坐标事件用positions定位候选，worker仍完整验证；Removed索引须维护三个endpoint，冲突保留；Transfer可一次可靠newOwner/newID对象定位再按坐标路由，早期UNKNOWN不得丢必要fallback/pending核证。**不能过滤所有foreign事件**，local→disabled退出正需要它们。未来测试分别核无关事件定位量、有效loss/return、late object、当前/origin ID、多记录隔离与reload；不要求native先证明预算超限才处理已确认重复定位。

## Provisional — IA-P06b-Q01：UNKNOWN时一次Transfer被丢弃

Handle617–625先live定位以判断相关性；nil、抛错、旧Owner/ID均不observe/不保留通知参数。随后coordinate事件或load仅reconcile()，不能满足598–602的newOwner/newID/oldOwner匹配，因此不能首次建立loss。

| 明确fixture输入 | 恢复foreign对象＋Initialized后 | boot后 | 补匹配Transfer |
|---|---|---|---|
| GetCityAt=nil | saved stage ACTIVE、loss=nil、exit0；facts拒读 | 不补loss | HELD_TRANSFER、exit1 |
| GetCityAt抛错 | 同上 | 同上 | 同上 |
| Transfer时仍是旧native reference | 同上 | 同上 | 同上 |

这是**条件性恢复边界：MEDIUM / MONITOR**。表中的ACTIVE是record stage，不是专业ACTIVE等级；facts拒读证明不会据旧record正常激活新Owner。AuditExit是stub，不证明具体carrier/Modifier残留；native早期时序与重复通知是否存在仍UNKNOWN。

若以后出现实际失城后记录不更新、或调整路由需要依赖此保证，应定域保存有界可信event候选并在可靠live ref到达时复核；不按位置/名字猜loss、不清history、不延迟固定回合后强制确认。当前不新建队列或修改任何实现。后补匹配事件可恢复，是明确反证，不能称永远无解或当前资产已损坏。

## 已知支持限制与no-action

- **多foreign hop K01 / DEFER**：loss.target未随foreign→foreign更新；0→3→4→0无法匹配旧Owner门禁。E2269已明确外方→另一外方不猜匹配；后续tokenless只扩严格原Owner单-hop，未补此范围。属于已接受正常城市永久成果原则下的已知实施限制，不重开成Gameplay归属TBD，不与支持的0→3→0→3→0混同。
- **同址新代 K02 / DEFER**：历史position/reservation不自动释放；raze/refound尚未支持，不拿native缺失、CityBuilt或坐标单独复活旧成果。继续保存唯一反证，不因Git存在删历史。
- **未知外交首次取得/新Free-City取得、多enabled Owner/AI/MP**：当前范围未实现；已受管理原Owner返回与第一次无history取得不同，不把现有区域反推旧专业。
- **旧档/中途加Mod**：用户限定新局创建时启用；test-only Legacy adapter不是生产迁移许可。new-save early primitive的已记录可辨识限制保留。
- **NO_ACTION**：同reference removal永久invalidated、strict proof、foreign hydration窄豁免、duplicate无generation新增、conflicting token/endpoint hold、已确认exit≤3有界尝试/成功不重做。它们不是所有native类型都PASS。

## 已有测试／实机证据的范围

只读测试，不运行历史回归。B108规模断言计index/record写隔离、coldboot/idle0写；P.Count为no-op，不能说明event fan-out预算。B109更新新局primitive/旧初始化合同；B111冻结snapshot/empty mode/missing conflict；B128 current引用/未专业城返回；B136较新actual gate及strict chain；recapture测试使用显式Legacy adapter及routes0。所有native事件/Property/mock对象均同步，不证明所有引擎交错。

direct native结果只读文字：B103单Research tokenless return/变CityID/P2/冷加载，B109三城V3，B111双城两个取得模式，B106 FOUND_CITY positive/交易negative，B105 refutes首Publish作为完整生命周期。没有重看原图或新native PASS，既有USER_GAME_TEST只继承同范围。

[原始JSON](Evidence/W13/lifecycle_dispatch_result.json)记录4规模＋3UNKNOWN场景、source/fixture/script hash；existing Lua5.5，无安装/DB/game/runtime访问。current source与原审计基线的主体未变，已复用保存/事务结论，不重复全读Store。

实际readscope：IdentityRead/FreshBindingHook全文、CityFlow126–149；Store transition/Handle/recapture/reconcile/manager/new-game/admission具名闭包，Spec ELIG/PROG完整相关条款及E2具名合同；五直接E2 fixture/现代反证摘段/具名native结果。未覆盖所有出口consumer、全游戏事件可用性与所有native模式。完整P06/P13/总审计未关闭。

## 续接

下一 **P02a Shared accepted合同与技术分层对照**：从Design Content README/current Spec完整SCOPE/ELIG/TERMS/PROG/SHARED相关节，以及Shared_D0045概念对象/规则metadata开始，核Identity/Potential/ACTIVE、普通建筑/D、具名长期资产和特殊unit生命周期在现行Architecture/Shared直接接口中是否正确分层。复用已核Owns/reference/UNKNOWN/持久/派生边界；Network另P02b，不逐专业复制规则或重验native。原三处未衔接设计边界保持，不自行补规则。此slice保存checkpoint后再进入。
