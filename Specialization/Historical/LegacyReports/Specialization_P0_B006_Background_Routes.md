# P0-B-006：独立后台 UI 商路影子读取

> 历史版本B006：B6-1用户截图停在UNKNOWN / LoadScreenClose。当前运行包为B007；仅按[调度修复与单项重试](Specialization_P0_B007_Background_Dispatch_Fix.md)重试B6-1，B6-2/B6-3暂停。下文保留原计划；10秒兜底依赖Context更新回调，尚未实机证明。

## CURRENT AUTHORITATIVE STATE

2026-09-11。用户认可调查后台UI方案并要求继续推进。B006实际实现独立InGame UI context自动当前路线读取，用于诊断与Gameplay任务/计数交叉对照；**尚未批准/实现以UI快照驱动正式网络**。不创建虚拟建筑、不发收益、不把UI_SHADOW_ONLY改名为GAMEPLAY_CURRENT。

本轮运行包P0-B-006 / modinfo13，SQL与UUID不变。原B005完整备份在DevelopmentBackups/SpecializationP0-P0-B-005。

## STATIC_CONFIRMED

UI/BackgroundRoutes.xml是独立AddUserInterfaces context，XML没有任何控件。对应BackgroundRoutes.lua由自己的Context初始化/更新生命周期驱动，不调用BTS、Open、Refresh、原生贸易面板或P0按钮。P0的Background routes按钮只读取ExposedMembers.SPC_P0_BackgroundRoutes.text；不要求选城市、不派发Gameplay请求，也不调用采样函数。P0窗口关闭不关闭该独立context。

数据读取：仅本地Test玩家（当前不是全玩家/多人生产实现）→UI PlayerTrade:GetNumOutgoingRoutes读前计数→每城GetTrade:GetOutgoingRoutes→只取TraderUnitID和两端player/cityID→核对起点归属、解析端点当前owner/cityID→按复合快照key去重→读后计数核对→原子替换。

错误/缺字段/计数前后不一致/端点未解析/冲突商人记录→UNKNOWN，并清除对外当前snapshot。完整空集则COMPLETE_UI_SHADOW/count=0。不会把上次成功结果当作本次有效；lastGood只在内部用于变化对比，不结算。

快照包含version、generation、reason、turn、player、sourceContext=UI、authority=UI_SHADOW_ONLY以及标量路线记录。此处owner/cityID是引擎引用，复合key是owner+trader+两端引用的快照key，**不是跨征服/夷平/单位复用的永久UID**。城市名仅是这个诊断快照的显示字段，正式RouteState/schema仍保持无UI字段原则。

## 调度与对照

- 初始化立即尝试读取，不等窗口打开。
- LoadScreenClose、路线、单位任务开始/清除、单位删除、城市变化、战争、回合等通知标dirty；不从事件参数写入路线。
- 独立context的更新回调每约0.25秒检查调度，事件后至少留约0.20秒合并窗口再读。缺失/漏事件时约10秒做一次完整核对。此定时方案是P0可见UI客户端中的实验，不承诺暂停/后台窗口/无UI主机的运行时效。
- 游戏端已有dirty事件增加RouteSignalRevision；UI只读该revision，发现变化也标dirty。不同context的加载次序、更新回调能否如期执行，需要用户实测。
- Gameplay自动任务样本额外导出engineCount、matchingTraderIDs、unknownOperations、turn、signalRevision。没有从UI输入数据重算它。
- MATCH仅表示同回合、没有已知dirty使其变旧、数量相同且商人ID集合相同。它不证明UI端点可作为Gameplay权威事实。已知变旧/尚未生成时PENDING，类型未知时UNKNOWN，数量或ID不同则MISMATCH。没有收到事件不保证样本绝对新鲜。
- Gameplay任务probe依旧在初始化/load/回合采样，不因点击Background routes更新；故删除后UI已更新而Gameplay暂PENDING是预期状态，不能强行显示MATCH。

背景context有512城/4096原始路线的失败上限（超限UNKNOWN，不截断为全集）；单次读只检查已知标量，不遍历引擎路线对象/元表。重复事件合并、初始化防重复注册，shutdown移除回调及清理自己导出的缓存。不保存路线为City/Player Property，不写UI操作请求，不与离线TradeRouteState连接。

面板显示当前完整数量、采样触发原因、首次成功原因、Gameplay对照、最近增删数、首条已删除路线以及前6条城市名方向。显示截断明确提示，总缓存不按6条截断。当前四商路测试可一次看完。nil任务坐标在旧Game面板明确写缺失，不再把unknownOperations=0当端点完整。

## LOCAL_SIMULATION_PASS

新增test_background_routes.py验证：无任何UI控件/操作请求仍可初始化、load重读；空/多路线、同起点/同终点、重复事件仅一次扫描；无事件时fallback删一条；读前后计数不符UNKNOWN；端点失效/易主UNKNOWN；外贸端点；同城对不同商人不吞；相同记录重复去重，冲突商人拒绝；GetTrade缺失；游戏端样本过期/ID同数不同/MATCH比较；非Test不读取；shutdown清理；新context以真实源覆盖故意伪造的999条导出缓存。

test_specialization_p0.py新增Background routes按钮只读缓存断言，读取函数故意报错且无Gameplay请求变化；并通过既有Lua/XML/manifest/原探针回归。test_trade_route_probe.py通过追加诊断字段/dirty revision后的既有行为检查。静态/模拟通过不是实机PASS。

## USER_GAME_TEST_REQUIRED

见Specialization_P0_Batch_B006.md，最多三项：新后台context初始化、读档自动重建、可选可直接操作的单商人删除。只验证后台方案新行为，不重做UI按钮的逐路分页。

完整战争/征服/夷平/自然结束/取消/闲置商人/同数量换线的真实生命周期与事件时序、联机一致性尚未验收；不要把一次删商人通过外推为全生命周期通过。

## BLOCKED / DESIGN DECISION REQUIRED

纯Gameplay端点参数目前仍nil，没有新发现的纯Gameplay全集来源。独立后台UI能避免人工打开窗口，但并没有消除UI context依赖。正式网络权威架构、适用玩家范围/多人模式仍未决定。本轮只安装shadow诊断，不更改原型的GAMEPLAY_CURRENT接入门槛。

所有多源L/工业结算规则、sqrt(N)、未来Spaceport/Entertainment范围保持。

## 文件

新增运行文件UI/BackgroundRoutes.lua、UI/BackgroundRoutes.xml；修改P0Panel.lua/xml（只读按钮/版本）、TradeRouteProbe.lua（游戏端诊断字段/dirty revision/明确缺失提示）、Probe.lua版本、modinfo独立context注册。新增DevelopmentTests/test_background_routes.py，更新test_specialization_p0.py。Architecture、Status和本批次文档同步；没有改动第三方/原版文件、没有启动游戏。
