# 商路接入与分发网络：实现计划与替代方案

Document Owner: Codex
Document State: BACKGROUND_SOURCE_DIRECTION_ACCEPTED_IMPLEMENTATION_PENDING
Design Authority: User
Design Basis: D0008 / NET-001至004、NET-RC、IND-NET
Implementation Scope: 本轮仅设计/静态复核/既有模拟回归；不部署网络收益或桥接权威

## CURRENT：用户已澄清并认可后台UI来源

[当前决定](../Technical/Specialization_Network_Background_Source_Decision.md)：用户不接受先打开窗口，但接受后台读取BTS当前数据。后台路径可继续，不再需要来源方向批准。此前将其描述为必须放宽纯Gameplay限制的解释已被纠正。桥接实现与生命周期验证仍待完成，未自动接受本提案全部细节/未知状态收益政策或C玩法替代。

## HISTORICAL：以下为澄清前提案，不作为当前待批准要求

## 用户结论

网络的连接、去重、强度计算本地模型已经具备。缺口是可靠地告诉Gameplay“现在具体有哪些路线”，不是开平方或分发规则难以计算。独立后台UI已能在不打开贸易窗口时读到完整端点，Gameplay目前只确认任务与数量。纯Gameplay方案当前BLOCKED，但不能断言整个机制无法实现。

优先建议试验后台UI→Gameplay桥接，尽量保留现有游戏玩法。它必须明确放宽早先“UI Snapshot不能成为正式来源”的工程约束，因此标DESIGN_DECISION_REQUIRED，不能把用户要求研究替代方案当成已经接受。D0008保持不动。

## 当前证据与此次复核

- 既有B005：Gameplay当前商人任务/数量与重载通过，坐标参数nil。
- 既有B007/B008/B009：独立后台UI初始化、保存重载、新增、删城重建有实机证据。它不要求打开BTS窗口，也没有自动操作窗口；是已加载的UI Lua代码直接调用City:GetTrade():GetOutgoingRoutes。
- 本轮再次只读查询Cache/DebugGameplay.sqlite：trade类Requirement仅联盟有商路、联盟双方路线、紧急事件双方/目标、城邦目的地等；trade类collection仅联盟/紧急事件。没有据此能确认枚举全部普通国内商路的集合。原生贸易站/派遣奖励的effect可以在引擎内部获得目的地，不意味着向Gameplay Lua公开当前全集。
- 本轮复查HD 2465378070/ModSupport/BetterTradeScreen/TradeSupport.lua:216/304/331仍为UI Outgoing读取。没有新的Gameplay调用签名证据，不再次派发已返回nil的旧探针。
- 更完整静态边界与文件证据见[第二轮审计](../Technical/Specialization_Trade_Authority_Second_Audit.md)。没有枚举危险的数字参数或尝试启动游戏。
- LOCAL_SIMULATION_PASS：本轮重跑test_trade_route_state.py、test_network_multisource.py、test_d0005_models.py；全集替换、取消/端点变化、错误旧缓存重建、max ACTIVE/去重、首都自接入及工业分项来源通过；输入仍为MOCK，不是实际Gameplay全集。

## 玩法到状态层：固定实现分工

1. 当前城市角色：以已经确认的城市事实提供专业，按当前资格/总督重算ACTIVE；首都与商业专业城市识别中心。不从现有区域倒推旧城历史；旧档无专业城市可以成为普通recipient，不能因此自动成为source。
2. 当前路线：仅保留owner、trader/engine identity、双端当前cityID与映射、国内标记、采样generation/turn与完整性；路径图形、UI文案不进计算核心。跨owner永久UID尚缺，不能把owner:cityID快照键包装成永久身份。
3. 接入：有效S→H建立直接来源证据；首都自专业单独添加合法本地来源依据。保存source UID、类型、ACTIVE、中心、支撑路线；同源多路线保留多份依据。
4. 分发：H→D同时携带H全部当前接入来源，不做每路线分配。收到网络的另一个中心不继承S作为自身直接源，不递归转发。
5. 接收：每类型建立city去重集合，记录center→source→route/free资格。最后一份依据失效才撤销。多路线/中心重叠不重复N。
6. 强度：只在来源与接收都完整时交给已有独立强度模型；Research/Culture合并用D0008确定规则，工业保留模板、来源输出与按项比较信息。本轮不接Boost、折扣或跨城收益。
7. 更新：路线变化重建拓扑；ACTIVE/中心身份变化即使路线没变也重建派生状态。失效路线不保留旧资格；加载丢弃派生结果，重新核对真实来源。永久事实不保存网络结果。

## A：后台UI数据桥接（建议优先试验，尚未接受）

玩法不需要换：仍是真实商路，仍消耗真实Trade Route Capacity，方向/全部网络分发保持。改变的是计算核心接受路线来源的技术约束，而非要求玩家打开窗口。

建议分三步，而不是直接信任UI表发收益：

1. 无收益影子桥接：后台完成一次全部城市Outgoing读取，前后路线数稳定、字段齐全、商人无冲突；复制成有上限的纯标量批次。使用load generation、采样序号、turn、来源player与完整结束标记，旧generation、重放、缺页/重复页、不同player混页一律拒绝。如何通过现有EXECUTE_SCRIPT通道提交、单次大小上限及回调时序先本地检查再做窄实机实验，不能只靠ExposedMembers函数修改Gameplay状态。
2. Gameplay只做校验及影子网络：对照当前商人任务ID集合和数量、城市存在/owner、版本/回合；完整批次一次替换。相同计数不证明端点，所以明确authority=UI_BRIDGED_CURRENT_CANDIDATE，绝不改标GAMEPLAY_CURRENT；新建事件只触发刷新，不能补全缺页。重复刷新幂等，失效旧generation停止供结算。
3. 通过新增生命周期测试后才讨论正式采用及收益：首次加载不打开UI、正常路线结束/掠夺后撤销、同数量换线等；复用既有截图，不重测分页与普通端点。B010仍延后，不把这些测试借用B010名义派发。

尚需证明：UI观察是否覆盖所有enabled AI而不只本地玩家；跨上下文请求可靠性；初始化先后及同回合刷新；失效通知后全量发布时机；多人确定性。初始试验可以单人无收益，但不能据此把Accepted资格模型改成永久human-only。AI/多人不能在未测试时宣布支持。

未知状态处理建议：诊断显示“网络状态等待重建”，不把历史结果当当前事实；正式临时停收益还是延迟结算会影响玩法，尤其一次性Boost，须在接收益前单独确认。不能在本次方案中偷偷确定丢失Boost/延后补发规则。

门槛：若仍漏掉普通取消/同数量换线，或不能覆盖当前参与者，不能因部分路线读取成功就进入正式收益。

## B：纯Gameplay，继续寻找原生连通性（备选研究，不承诺成功）

只有找到新的可审计API/普通国内路线collection或真正反映当前S→H关系的原生条件才值得新probe。有限城市对条件可能替代完整route record，但必须证明方向、即时撤销和读档自恢复；目前无这组证据。继续盲试旧API不会推动机制。

虚拟建筑可以在连接集合已知后表达效果，不能解决路线结束判断；贸易站属于历史存在，不等于当前连通。二者不作为本选项已解决的证据。

## C：改为显式连接槽位（玩法替代，最后考虑）

若A不接受/不可用，B无突破，可以设计“全国连接槽位+城市连接操作”而非实际商路自动连通。这样路线取消无需推断，连接本身成为明确游戏事实，但玩家要额外管理，且“Trade Route Capacity本身就是网络带宽”必须重写：槽位与实际贸易路线如何共用容量、是否占用Trader、重新分配成本/时间都需用户决定。

不能简单按总Trade Route Capacity送一套独立槽位，否则同一带宽被贸易与网络双重使用；也不能悄悄改成无限道路/贸易站连通。该方案会改变NET-001至004，不落盘Accepted Spec，不现在实现。

## 推荐决定与执行队列

DESIGN_DECISION_REQUIRED：是否批准A的“无收益后台UI桥接候选实验”，允许它作为候选当前路线来源接受验证，但不立即成为正式权威、不启用网络收益？推荐批准A；无需现在接受C的玩法变更。

用户批准后：先实现纯标量完整批次传递+Gameplay校验+真实城市角色影子派生，本地覆盖重放/缺页/同数量替换/断开后剩余依据，然后只给一小批新增初始化/撤销测试。技术研究期间不暂停不依赖商路的Local能力，但本用户已要求把Network列为下一重点，不继续长串无关存储边界实验。
