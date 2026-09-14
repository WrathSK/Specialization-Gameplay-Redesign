# AV2-A — 事实版本、发布与撤销合同

Document Owner: Codex
State: IMPLEMENTED_IN_DEVELOP / LOCAL_SIMULATION_PASS / awaiting user review
Develop build: P0-B-070.97 / modinfo97
Stable runtime: B069.96 / modinfo96 — UNCHANGED, NOT DEPLOYED
Design: D0025 unchanged
Base: AV2-I001 / commit 79281ff98cebbe12260703fce780df98c0cc8155

## 范围与证据

只实现Batch A。没有shared derived-result cache、UI sample协议重构、消费者监听器清理、保存迁移、carrier/UI/适配/玩法修改。LOCAL_SIMULATION_PASS表示真实Lua模块在本地mock引擎通过，不等于Civ VI事件投递/Modifier时序通过。无需现在切包；任何未来develop实机切包仍须明确授权及恢复点。

本页是相对AV2-I001源码快照的实施增量；I001三张地图/Source_Index/Event_Catalog继续作为79281ff调查证据，不能把其旧CURRENT误作本build代码。

## 1. 版本模型与owner

`NetworkInput.Capture`只读原生及现有EffectiveFacts，产生规范化逻辑输入；`NetworkBridge`是唯一正式接受/发布owner。不创建新Property，所有版本是session内存。

| 字段/事实 | 来源与owner | 进入签名的逻辑内容 | 生命周期 |
|---|---|---|---|
| 路线事实 | 已批准BackgroundRoutes→NetworkSender完整包，Gameplay计数/端点验证 | 排序后的owner/city/trader集合，加两端current reference | seq/epoch/turn/signal仅验收，不是逻辑变化；成功替换或确认撤销增加routeRevision |
| current city reference | 原生GetOwner/GetID/GetX/GetY及现有Binding token | owner、id、位置、token；包含国外路线端点，不读取其专业 | 不是新增永久UID；旧继承限制不变 |
| Identity / Potential / source qualification | 现有EffectiveFacts.Read→Flow/Journal/投资凭据 | specialization、potential、token、first districtID/type | 有效确认的NONE/潜力0表示不具专业资格；已知来源消失/改变才撤销 |
| ACTIVE | EffectiveFacts与原生Governor投影 | 实际整数active；不是总督事件次数 | potential保持不变时ACTIVE仍可独立改变签名；没有新增潜力/总督规则 |
| Trade Center | Commerce Identity或原生Capital | 城市身份字段及capital cityID/current reference | 路线不变也可发布新输入 |
| Research/Culture配置 | 现有SPCBoostConfig.k | kResearch/kCulture | 当前仍各1；本轮不改配置。未来efficiency必须扩展合同后才能纳入缓存 |
| UI其它样本 | 不参与当前Network拓扑/National输入 | 工业BASE、Copy actual、购买许可、收藏/相邻**不进入此签名** | 它们是下游效果自己的额外输入，不可用此版本缓存完整最终收益 |

`inputRevision`：完整已接受逻辑输入不同才+1；重复Audit/turn/seq不增加。

`derivedRevision`：该次VERIFIED输入成功通过现有derive后+1；`derivedFor=inputRevision`。确认不可用撤销时`derivedFor=nil`；旧derivedRevision不是可用凭据。查询仍每次运行derive，不按调用次数修改derivedRevision，也没有提前实现Batch B。

`revision`保留为routeRevision兼容字段，明确撤销现在也增加；不能当全Network版本。

可供后续缓存的键：`contract + epoch + player + inputVersion`，并要求`validity=VERIFIED`、`derivedFor=inputVersion`。`Input(pid)`返回元数据值副本；它不主动扫描。Batch B必须先经过Refresh/事实owner通知，再判断键，不得把“没人更新元数据”当作事实没变。签名为长度前缀、固定字段、排序集合；数值使用显式17位有效数字表示，3与3.0相同。没有历史签名数组。

## 2. 有效性与读取可用性分开

| 情况 | 正式validity / availability | 行为 |
|---|---|---|
| 尚无完整输入 | UNKNOWN / UNAVAILABLE | inputVersion=0，无正式空集合发布 |
| 完整事实成功接受 | VERIFIED / AVAILABLE | 成功派生后一次发布 |
| dirty、坏包、临时getter失败 | 原VERIFIED保留 / NEEDS_REVALIDATION | 不把失败伪装成空网络；无输入变化则无consumer通知 |
| 同一current reference的ACTIVE/专业读取暂不可用 | 使用该城市上次已确认输入；availability=NEEDS_REVALIDATION | 不猜0；保留最后已确认值，成功重读同值不增版本 |
| 初次出现且事实不可读 | UNKNOWN或保留之前完整输入 / UNAVAILABLE或NEEDS_REVALIDATION | 不以该城市猜造完整快照；候选最多一份，可后续刷新完成 |
| 原生端点/单位不存在、战争、reference改变，或失败全集读取伴原生数目减少 | CONFIRMED_INVALID / UNAVAILABLE | 正式撤销一次，inputVersion/routeRevision递增，下游可见撤销元数据 |
| 新完整路线集合含真实删除 | VERIFIED的新完整输入 | 直接替换一次，不先发布空网络 |

`routeValidity`和`revalidation`另暴露原路线是否仍获确认、是否待核对；availability不是业务零值。sender相同fingerprint抑制保留，不为了清诊断标记强制额外发送包。

已有Flow且读取失败保持UNKNOWN；明确从未跟踪的旧城（Flow ready且城市无Flow记录）沿用不参与规则，不补写/猜Identity。已确认城市记录突然不可读不会被当成“从未跟踪”。这不是永久资料损坏修复；持续UNKNOWN仍需诊断，不自动删除凭据。

## 3. 发布、撤销、重入与顺序

1. 接收包先验证epoch/seq/turn/signal、格式、全集count、owner/端点/单位；候选与正式状态分开。
2. 捕获当前逻辑输入，签名相等即停止，**不derive、不发布、不通知正式consumer、不进行Building/Property写**。捕获本身仍扫描，这是Batch A有意保留的成本。
3. 输入不同才derive；成功后先完整更新accepted input、routes及版本，再向Lv3Effects/StandardizationDiscount/NetworkBoost/CommerceConvergence通知，参数为publication metadata。现有Audit可忽略参数，也可从`Input(pid)`读取；查询National/ConnectedKinds/RecipientSources按已接受事实计算。
4. 新完整route包直接替换；明确失效缺少可用全集时发布CONFIRMED_INVALID，而不是静默清表。仍保留原来整批撤销策略，不声称已实现逐路线最小撤销。
5. 如果新输入不可读，但独立原生证据已确认旧city/reference丢失，或完整候选证明旧路线删除，仍正式撤销；不借UNKNOWN掩盖已知失效。
6. 同pid同步refresh保护防止通知中的查询再次发布。接收旧/重复seq、旧epoch/turn会被拒绝；更新包清掉未发布旧候选，包含“新包恰好等于现有正式内容”的情况。没有任意外部fact-version setter。
7. consumer异常仅记录有限错误字段，不回滚已发布事实、不循环retry。后续既有事件/对账继续承担效果恢复；这是Batch D的消费者执行边界，不是保证所有效果应用原子化。

暂存至多一份candidate/current accepted input；候选不跨turn/signal使用，load清空。新的空路线完整包是合法VERIFIED输入，与UNAVAILABLE不同。读档重新建立epoch与输入；不读历史event列表恢复网络。

## 4. 触发范围 / 从旧版本移除的语义

保留CityBuilt/OnDistrictConstructed/PlayerTurnActivated核对入口，但Rebuild不再无条件derive并Audit四个下游，只有逻辑输入diff才发布。

加入GovernorAssigned/Changed/Established/Promoted、CapitalCityChanged（API存在时）、CityAddedToMap核对；现有CityTransfered/CityRemoved/war等证据入口也核对城市输入。UnitAction与旧INVEST诊断动作返回后、GPP后台通知入口先Refresh，覆盖投资提交及原生总督投影晚于第一事件的补偿入口。没有新增UI listener/timer，仍保留回合和查询核对。原生特定事件是否存在/何时送达未新实测，不能承诺所有变动同帧生效。

route seq / turn / signal / Audit运行次数不再等价完整Network版本变化。一次改变后重复Rebuild不增加派生版本。不是移除所有消费者自己的turn/Governor监听——那属于Batch D。

## 5. 已迁移与仍未迁移

| 已迁移 | 仍待后续 |
|---|---|
| NetworkBridge 接收/确认撤销/Refresh/Rebuild及National、ConnectedKinds、RecipientSources、Read | Batch B共享derive：本轮每次查询仍重算；完整事实扫描也尚未优化 |
| current reference/Identity/Potential/ACTIVE/Capital输入签名；route明确失效可见版本 | Batch C：Copy/Discount/Dialogue/GWA各自样本过期、ACK及暂空wanted；Industry无统一sample epoch |
| 发布前接受全部输入，四个network通知可读取完整metadata | Batch D：四个消费者及其它模块独立的原生事件Audit仍在；不能承诺每次重复Governor事件全系统Audit=0 |
| National使用已确认ACTIVE，UNKNOWN重读不自动变零 | CommerceIV/Copy/Discount等仍独立读取EffectiveFacts、城市yield、模板等；不能将Network版本当其完整收益输入版本。其暂空/恢复属于C/D，不是本轮全部修复 |
| 真实route/input失效发布撤销 | Batch E：owner迁移、32-city、receipt/历史cache清理仍隔离/延期；不改存档 |

因此Batch B的**Network拓扑/National共享视图**已有本地验证前置条件；缓存全部消费者最终产出仍不安全。后续Batch B必须沿用未知保留/明确撤销与新版本合同，不能退回旧route revision。

## 6. Counters与本地验证

复用固定计数器新增6项：fact_change、input_duplicate、input_publication、withdrawal、revalidate_same、stale_input。总34固定keys；current/total/previous/peak；无逐事件字符串日志/磁盘写/历史数组。withdrawal计数是已接受事实减少/替换或明确失效，不等于实际拆建筑数量。

入口：[test_arch_v2_batch_a.py](../../../DevelopmentTests/test_arch_v2_batch_a.py)。需要现有Lupa lua55测试环境。

- 用户A–I全部覆盖：重复输入、ACTIVE3→4→3、资格失去/恢复、capital/center变化、route增删、重核同值、UNKNOWN、旧包/旧epoch。
- 额外：Potential改变而ACTIVE不变；3/3.0等价；未知初始不发布空；旧候选被更高seq同内容包替换；native参考重用、战争、商人删除；读取失败与独立已知撤销并存；同步重入、load新epoch。
- 完整保留B069行为回归断言：真实collector/sender/receiver与Commerce native-write mock，普通已知/未知单位10次操作零重复写，增加/删除、bounded retry、10000回合固定计数结构。只补native坐标/Property getter fixture与modinfo97断言，不修改历史脚本。
- 24组与79281ff旧源码运行结果对照：source levels、capital、Commerce center身份变化；National的N/max ACTIVE/source集、direct types、三类recipient source集合逐值一致。
- 全73个Lua语法、manifest引用；本批SQL/Design/消费者玩法源码不变。native事件投递/实际性能/游戏内存未验证，不宣称PERFORMANCE BLOCKER解决。

本轮还通过部署工具的临时目录回归（无实际部署）；核对main worktree clean及实际运行包115文件摘要仍为`7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`，D0025 hash未变。批次新增NetworkInput后develop为116文件/modinfo97，不能据此替换当前stable运行包。

## 7. Gate

完成本地检查后commit/push develop；无需现在实机切包。建议 **Architecture v2 Batch A Milestone Candidate**，候选tag名`arch-v2-batch-a-b070.97`，未授权自动打tag或promotion。下一步由用户审阅，再决定是否授权Batch B。
