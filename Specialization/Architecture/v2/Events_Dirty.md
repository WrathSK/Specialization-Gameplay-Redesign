# Event / Trigger Map + Dirty Propagation

Document Owner: Codex
Evidence: STATIC_CONFIRMED; 事件频率/CPU/内存占用不能由注册数量推定。

## 1. 逐事件目录与分类合同

[Event_Catalog.tsv](Event_Catalog.tsv)展开了当前Gameplay启动模块和manifest UI注册事件、Context init/shutdown与SetUpdate。每行含namespace.event/module/source line/class/direct/indirect/work/scan/write。多注册同事件明确写在work列；源码helper/callback/Property索引见[Source_Index](Source_Index.md)。未Start的继承模块仅在源码索引保留，不作为活动事件统计。

- DIRECT：对本模块输入确实有直接意义，如工作专家变化、作品移动、建筑获得；并非每次事件都会改变最终值，仍应compare。
- INDIRECT：只可能间接影响；UnitOperation对路线不能直接证明创建/移除。绑定未知签名/单位消失只允许重核或native证据。
- RECONCILIATION：load/turn/有界UI轮询、启动补偿。
- DIAGNOSTIC：观察或显式实验；写入列仍可能为yes，尤其B014/实验fixture。它们不应成为正式玩法权威。

Init时直接调用：TradeRouteProbe.refresh、Eligibility sample、Qualification collect/publish；UI各Init初始化/refresh。FreshBindingHook是同步自定义函数hook，不是Events注册。CrewPrecision包装UnitActions.Run；CrewProjectOrder包装外部ProductionPanel.GetDataHelper，仅重排项目，无SPC监听。PerformanceCounters没有事件注册，在Count调用时发现turn变化。

Gameplay里请求不是另一个独立事件总线：`GameEvents.SPC_P0_Request`唯一入口按Action分派，数据校验/ACK差别见桥接表。隐藏P0按钮的RegisterCallback均在Source_Index保留，不能从主面板隐藏推断后台代码不再运行。

## 2. 当前实际传播 / old==new停止位置

| 路径 | event→dirty→scan→derive→compare→write→下游 | dirty含义 / equality边界 | CURRENT→TARGET |
|---|---|---|---|
| Route正常重验 | Unit/filter或route signal→UI dirty→full collect→fingerprint→sender→Game完整校验→derive(仅变化)→notify→各Audit | B069 dirty=NEEDS_REVALIDATION，旧verified不清；sender fingerprint相同在编码前停；receiver比较在derive前停，UI仍要full collect才能知道相同 | 保留已修正路径，不把dirty→0故障当仍必现 |
| Route明确失效 | CheckEvidence/consumer调用Verified→发现缺端点/trader/战争/失败fullread后数量减少→**整个**b.routes及派生表=nil→某些调用notify→后续完整collect恢复余下路线 | 一条确失效会使整个batch不可用，不是按失效route局部过滤；Verified本身不notify、不增revision，CheckEvidence和Receive外层才通知；查询也可改变shared内存 | 统一失效publication/revision与受影响集合，保留真实撤销，不容长期stale |
| Network Rebuild | CityBuilt/完成/每PlayerTurnActivated→每stored player derive→缓存替换→无条件4个consumer Audit | 无topology equality前置；只有route Receive才有fingerprint stop；没有全Network输入revision | 建立fact+capital+route revision后共享derive，变更才通知 |
| Local Lv1/2/3/4 | 多个city/governor/worker/turn→直接Audit→世界cities→每城facts/district→desired→HasBuilding compare→write | 无dirty集合；old==new直到末端carrier。busy只阻同步重入；Lv3Effects完成即通知Lv4Percent/Copy，即使没有变化 | 先shared facts/read index，再按具体city依赖传播 |
| GPP UI通知 | worker/focus/governor→dirty bool→generic pulse flush→GPP+Lv3Support+Lv3Effects+Boost+Dialogue→再Lv4/Copy | UI在scan前dirty gate健康；接收端扇出未比较输入变化 | 收窄到真正需要worker/active变化的模块 |
| Industry BASE | Publish/Playback→全玩家district scan→base value比较→Request→Game验证district→world Audit→Lv3Support/CrewAccess | equality只减传输；当前same值没有Game ACK证据；sample不带epoch/turn | BASE fact owner / ACK / target city更新；项目资格不随base派发 |
| Copy | Publish/Playback或1s timer→全district×6yield→签名/ACK比较→Receive先清sample→全district校验→Audit→每城target重复district/network→carrier比较 | invalid或跨turn sample变零desired；没有lastverified完整事务；收到相同内容新seq仍Audit。1s callback可靠性不是保证，因此generic仍广泛触发 | 先sample生命周期/单flight/dirty契约，再有限reconciliation；不改单项收益 |
| Discount | Generic Publish→Audit全城candidate，每城derive/ledger→plan signature→过期sample空wanted→carrierwrite→UI pulse全candidate资格scan→seq/revision sample→Receive前后Audit | 比较晚；plan变更清sample，turn变更不改plan也会使sample失效；applied cache不能代表事实全集 | 先输入版本/明确失效与暂未就绪语义，再dirty consumer与安全apply |
| Dialogue/GWA | work/terrain/governor事件→dirty→generic drain→allcities slots + BASE vectors→signature→one packet→Dialogue collection accepted→Dialogue.Audit→GWA.Audit(oldAdj)→GWA.Receive(newAdj)→GWA.Audit | idle generic不scan，retry bounded；多个sample逻辑分阶段，turn不一致先emptywanted；角色变化也会重扫整个收藏 | 保留dirty/ACK；以后collection和BASE分version或同事务快照，单次下游apply |
| Standardization | 建筑事件→queue单building→flush→hasBuilding+learned compare→仅新增知识write | pending为空generic flush不scan city；但Discover每turn查全部参与city，AddedToMap按owner全city试同building | 保留一次补录/增量主线，未来精准city resolver |
| Commerce IV | route notify/多类事件→world plans→每eligible城routes/source total→统一apply→carrier compare | 不通过其它Commerce source避免直接递归；不共享network derive但有每城重复routescan；source城市yield刷新没有专属版本 | source yield依赖的单向通知和affected centers，保留先plan后apply |
| Unit UI | 选中unit→VIEW0.5s / TARGETS5s→Game可能全player目标scan→reply→UI compare | 真正Confirm严格原生重验；只读VIEW也会扫targets/清旧内存plan；UI tick无形带来重复工作 | 共享展示snapshot/事件版本，确认仍独立验证，不动消耗流程 |

## 3. 重点事件重复证据

- Governor/worker在Gameplay GPP/Lv3/Lv4/Commerce等各自Audit，同时UI GPP dirty收到后再跑一串Audit。数量需counter实测，静态只能证明多条可达路径。
- OnDistrictConstructed由Journal、Flow、完成诊断、常数收益、Network Rebuild、Standardization及多效果监听。同一完成既是永久事实写点又引发多次consumer work；不是单个owner提交后统一传播。
- GameCoreEventPublishComplete：Routes/GPP/Dialogue作为有条件drain；Copy/Industry/UI Discount会扫描，Gameplay Discount也直接Audit；Standardization仅Flush pending。不能把所有generic监听一刀切判坏。
- PlayerTurnActivated/Deactivated：多Gameplay模块不按事件pid筛选而扫描world/所有参与player。BackgroundRoutes只local turn；Standardization Discover(pid)相对收窄；Dialogue UI任意turn激活mark。
- 普通已识别非商人操作B069已过滤Route dirty；UnitRemoved无法再查unit类型可能触发重验/证据检查，是谨慎fallback而非必然路线变化。
- Engine Property派生更新（Governor flags）、BuildingChanged、Publish可能时序错位；本报告不宣布具体原生事件先后顺序恒定，也不额外要求当前长局测试。

## 4. 动态模块CURRENT / TARGET评级

GOOD接近目标；ACCEPTABLE冗余或限制可控；REFACTOR_CANDIDATE有明确重复扫描/依赖缺口；P0_ARCHITECTURE_RISK是可能造成震荡/无界增长的结构风险，**不是已证实当前崩溃或内存问题的原因**。

| 模块 | 评级 | CURRENT / evidence | TARGET（仅建议） | Source |
| --- | --- | --- | --- | --- |
| BindingProbe/FreshBindingHook | REFACTOR_CANDIDATE | city ledger+token三写，累计32，Fresh同步包装；正常确认不重复分配 | 单一城市ID注册/版本化迁移；保留缺史拒绝 | [BindingProbe.lua:1](../../../Mod/BindingProbe.lua) |
| CityJournal/CityFlow | REFACTOR_CANDIDATE | 双持久first/spec事实、两个completion listener依序、player-wide held | 先定义权威与投影/恢复协议，再迁移；不要先合并函数 | [CityFlowProbe.lua:1](../../../Mod/CityFlowProbe.lua) |
| EffectiveFacts / Governor adapter | ACCEPTABLE | 纯读不写；原生条件一致性校验；每consumer重复复制/验证 | 保留门控语义；未来同revision共享事实读取 | [EffectiveFacts.lua:1](../../../Mod/EffectiveFacts.lua) |
| InvestmentAction | ACCEPTABLE | 最多3receipt；确认重读anchor/turn/unit，pending区分INTENT/CONSUMED | 保留单次消耗协议；未定结果继续HELD，不重构结算优先 | [InvestmentAction.lua:1](../../../Mod/InvestmentAction.lua) |
| UnitActions Crew receipts | P0_ARCHITECTURE_RISK | 每次施工新增永久receipt，整表读写，无cap/prune；不等于已证实70GB根因 | 先设计去重保留窗口/归档及save migration，后单独变更 | [UnitActions.lua:1](../../../Mod/UnitActions.lua) |
| ConstructionProbe/UnitActionSitePolicy | ACCEPTABLE | 当前queue前后校验，正式Crew复用只读snapshot；隐藏DEV Apply仍可写 | 保留合法目标/结算；之后隔离测试接口 | [ConstructionProbe.lua:1](../../../Mod/ConstructionProbe.lua) |
| CrewPrecision | ACCEPTABLE | 包装每次Confirm前后只读；额外target扫描但非普通单位事件 | 保留诊断，未来显式instrumentation开关 | [CrewPrecision.lua:1](../../../Mod/CrewPrecision.lua) |
| CrewProjects | REFACTOR_CANDIDATE | 多事件全世界access对账，Industry.Audit又调用，BASE本不影响access | identity工业区变更精准刷新，生命周期限定清理 | [CrewProjects.lua:1](../../../Mod/CrewProjects.lua) |
| ResearchSupport | REFACTOR_CANDIDATE | completion单城不错；turn/CityBuilt全世界；errors粘滞session | 保留单城完成路径，限定参与者/明确重试 | [ResearchSupport.lua:1](../../../Mod/ResearchSupport.lua) |
| IndustrySupport + IndustryRefresh | REFACTOR_CANDIDATE | Publish/Playback全district扫描后sent比较；Receive全局Audit；sample无seq/epoch | BASE fact版本化/目标城市刷新，ACK合同先行 | [IndustrySupport.lua:1](../../../Mod/IndustrySupport.lua) |
| Lv2Housing | REFACTOR_CANDIDATE | 全世界scan，每city重新district+tiers；no-op只在building层 | 共享effective/district facts，按city和tier依赖更新 | [Lv2Housing.lua:1](../../../Mod/Lv2Housing.lua) |
| Lv2GPP | REFACTOR_CANDIDATE | UI dirty+Gameplay事件重复Audit，全世界city/重复district | worker/facts owner通知一次，消费者限定city | [Lv2GPP.lua:1](../../../Mod/Lv2GPP.lua) |
| Lv3Support | REFACTOR_CANDIDATE | 直接事件+Industry/UI请求多路全城Audit | ACTIVE/BASE revision决定城市dirty | [Lv3Support.lua:1](../../../Mod/Lv3Support.lua) |
| Lv3Effects | REFACTOR_CANDIDATE | 每Audit后无条件Lv4Percent/Copy；Commerce query重derive | 拆依赖通知，不因任意Audit传播全部下游 | [Lv3Effects.lua:1](../../../Mod/Lv3Effects.lua) |
| Lv4Percent | REFACTOR_CANDIDATE | worker/active事件自身Audit又被Lv3Effects重复调用 | 同城effective/worker revision消费；保留公式 | [Lv4Percent.lua:1](../../../Mod/Lv4Percent.lua) |
| BackgroundRoutes + NetworkSender | ACCEPTABLE | B069 dirty保留verified、同fingerprint停发送、单flight/有限collector retry | 保留来源与现有保护；补生命周期边界证据后再考虑优化 | [UI/BackgroundRoutes.lua:1](../../../Mod/UI/BackgroundRoutes.lua) |
| NetworkBridge derive/query | REFACTOR_CANDIDATE | National/ConnectedKinds/RecipientSources每调用重derive；Rebuild无条件通知 | 多输入NetworkState revision+一次derive共享视图 | [NetworkBridge.lua:1](../../../Mod/NetworkBridge.lua) |
| NetworkBridge Verified撤销路径 | REFACTOR_CANDIDATE | Verified读可清整个snapshot；失效不增revision；queries未统一通知 | 单一发布/撤销owner与revision合同；不能简单缓存旧revision | [NetworkBridge.lua:1](../../../Mod/NetworkBridge.lua) |
| NetworkBoost | REFACTOR_CANDIDATE | 每Audit National重derive；多事件及UI GPP链；load world clean | 共享National revision，整数Applied相同停止；保持量化函数 | [NetworkBoost.lua:1](../../../Mod/NetworkBoost.lua) |
| Standardization ledger | ACCEPTABLE | learned单次初始化，Queue building增量，≤2turn retry；Discover仍全city | 保留ledger增量主线；减少discover/AddedToMap广扫 | [Standardization.lua:1](../../../Mod/Standardization.lua) |
| StandardizationDiscount + UI | P0_ARCHITECTURE_RISK | generic Publish无条件全城derive；turn/plan样本过期先空want；ACK前后两Audit | 先定义lastverified资格/明确失效，单flight，再按版本精准消费；风险未证实每次都振荡 | [StandardizationDiscount.lua:1](../../../Mod/StandardizationDiscount.lua) |
| CopyYields + CopyYieldRefresh | P0_ARCHITECTURE_RISK | publish/playback与1s callback全scan；ACK不等可反复发送；invalid/oldturn变0；每target重扫 | 样本事务/dirty gating/ACK边界，随后共享网络和district索引；非本轮修复 | [UI/CopyYieldRefresh.lua:1](../../../Mod/UI/CopyYieldRefresh.lua) |
| CommerceConvergence | REFACTOR_CANDIDATE | 全世界plans/apply，每eligible城扫routes；计划前算后写已有防反馈 | 保留max/floor/不聚合Commerce源；source yield direct事件依赖 | [CommerceConvergence.lua:1](../../../Mod/CommerceConvergence.lua) |
| DialogueRefresh/Dialogue/GWA | REFACTOR_CANDIDATE | dirty/有限ACK重试健康；collection+Adj非原子、turn审计可能先旧样本撤销、GWA重复audit | 保留dirty主线；分输入revision/一致样本应用；不动GW设计 | [Dialogue.lua:1](../../../Mod/Dialogue.lua) |
| DialogueModel / GWAdjacencyModel / CopyYields.Plan / Boost.Quantize | GOOD | 确定性纯计算，明确排除分类/精度；無事件/持久副作用 | 保留函数，供未来模块验证复用；不重写公式 | [DialogueModel.lua:1](../../../Mod/DialogueModel.lua) |
| GPPRefresh | ACCEPTABLE | bool dirty→generic flush，闲置不scan；发送失败重标但无ACK | 保留合并方式；缩小Gameplay dispatcher扇出 | [UI/GPPRefresh.lua:1](../../../Mod/UI/GPPRefresh.lua) |
| BoostRefresh | ACCEPTABLE | ready后退出；未ready反复初始化无retry上限 | 保留启动补偿，后续统一初始化失败预算 | [UI/BoostRefresh.lua:1](../../../Mod/UI/BoostRefresh.lua) |
| UnitTargets / UnitPanelActions / UnitTargetMarkers | REFACTOR_CANDIDATE | 单pending/原生重验安全；选中Crew每0.5s View可全city targets；lens另5s重复 | UI只读snapshot按选择/queue/progression revision复用；不改consume | [UnitActions.lua:1](../../../Mod/UnitActions.lua) |
| CityPotential | ACCEPTABLE | 只选中city、2s request，no propertywrite；仍有泛化request引擎通知成本 | 以后用progression change通知替代重复query；本轮不UI polish | [UI/CityPotential.lua:1](../../../Mod/UI/CityPotential.lua) |
| PerformanceCounters | GOOD | 28固定keys current/total/prev/peak，无逐事件字符串/IO | 保留；不要扩成无限事件history | [PerformanceCounters.lua:1](../../../Mod/PerformanceCounters.lua) |
| DiagnosticLog | ACCEPTABLE | 每scope128不同文本，重复计数；文本长度未单独cap | 保留去重；未来统一bounded diagnostics contract | [DiagnosticLog.lua:1](../../../Mod/DiagnosticLog.lua) |
| P0Panel / UnitSites / read helpers | ACCEPTABLE | 按手动读取；report最大12000scalars/depth12；readings按action/city/page无cap | 保留必要诊断；未来session dictionary prune，不当性能修复优先 | [UI/P0Panel.lua:1](../../../Mod/UI/P0Panel.lua) |
| TradeRouteProbe | REFACTOR_CANDIDATE | 候选诊断+正式RouteSignalRevision同模块；turn扫描unit及日志 | 将正式dirty信号owner与候选探针分离，保留批准collector | [TradeRouteProbe.lua:1](../../../Mod/TradeRouteProbe.lua) |
| CompletionProbe / CompletionRecordProbe | ACCEPTABLE | 近期观察有64cap；B014额外持久首次写，不供正式收益 | 不要混为Identity；未来减少常驻实验工作 | [CompletionRecordProbe.lua:1](../../../Mod/CompletionRecordProbe.lua) |
| Storage/Envelope/Eligibility/Qualification probes | ACCEPTABLE | 固定fixture/启动名册诊断；不作为正式资格/事实 | 保留只读检查和显式test边界 | [EnvelopeProbe.lua:1](../../../Mod/EnvelopeProbe.lua) |
| HalfYield/Purchase/GreatWork/YieldCarrier test backends | REFACTOR_CANDIDATE | 隐藏实验仍Start；Half flag跨save恢复并turn世界scan；各自cleanup不统一 | 独立实验生命周期合同；不贸然清旧存档flag | [HalfYieldProbe.lua:1](../../../Mod/HalfYieldProbe.lua) |
| CityInheritanceRead/Shadow/Inheritance | ACCEPTABLE (ISOLATED) | 未Start、shared入口=nil；不是当前动态风险来源 | 继续隔离；不列入本轮可启用重构 | [Gameplay.lua:1](../../../Mod/Gameplay.lua) |

## 5. 尚未量化、不据此下结论

1. 建筑写入实际触发哪些engine/UI事件、是否同帧/异步，必须未来对照counter/定点测试；静态可达环不等于无限环已发生。
2. Counter只观察本Mod包装的直接Lua写，不含原生Modifier内部写；不能据PropertyWrites=0断言引擎完全无写。
3. historical city字典大多按曾见城市增长，Crew receipt按动作增长，DiagnosticLog固定条目但字符串长度可变；不同增长维度不能都称“无限event payload history”。
4. 本轮未展开完整carrier/外部适配调查；仅已实际用到HD队列helper、地块标记、tier及BTS同源UI路线引用，保留后续任务。
