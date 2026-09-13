> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

> 最新结果：UI 当前路线及三条场景读档读取、第四条加入后的同城两条分页均已用户确认通过；B003 仅改善显示。详见 Specialization_P0_B003_Readability.md。以下待测表述保留为历史，Gameplay 权威网络恢复仍未完成。

> **用户澄清更正**：此前“UI端点/多路线通过”误记已撤销。实际通过的是Route events (Game)的新建路线事件端点捕获与多事件显示；Read routes (UI)仍待测。读档后事件表清空是B002临时日志的实现限制，不是有效路线重建。最新四图记录与单项步骤见Specialization_P0_B002_User_Result.md。

> **用户结果更新**：UI路线出发/目的城市读取、新增第二条路线后两条均显示，已USER_GAME_TEST_PASS，不重复此项。Gameplay Route events尚未明确回报，仍USER_GAME_TEST_REQUIRED。Actual收益口径仍采用用户后续确认的NativeDistrictCopyBasis。

> **用户已确认更新收益口径**：Actual采用煤电厂/大酒店原生区域复制算法（NativeDistrictCopyBasis），不再等同GetAdjacencyYield。下文“固定行业收益目前不进入公式”是澄清前历史，已被覆盖；是否包含某类收益以原生复制行为为准。Base规则不变，B002商路步骤不变。具体适配限制见Architecture相应正文。

# B002：相邻来源边界与商路上下文修订

## 用户证据

USER_GAME_TEST_PASS：用户明确确认UI基础相邻、当前相邻和相邻翻倍政策前后能正确区分。第一张截图10:55:05显示Campus科学2/2，其它yield为0；政策前后通过依据用户文字，不假称截图包含全部变化。此PASS限已测UI通道，未覆盖Gameplay或真正cross-yield adjacency。

用户另报工业区基础+5，行业给予区域+1文化/+3金币但相邻接口不返回这些值。源码表明有多种符合该数值的行业，截图不足以唯一确认具体行业。当前缓存中的BREWING和DECORATION效果均使用MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE，CLOTH也有固定区域产出效果。它们是固定加成，不因区域基础相邻是否为5而改变。因此没有出现在相邻getter里与其来源一致，不能以此认定ActualAdjacency漏读真正交叉相邻。

USER_GAME_TEST_FAIL：11:10:53截图，B001 TRADE失败于BEFORE_GetTrade / GetTrade:ABSENT。还没执行GetOutgoingRoutes，不应归因路线起终点参数。11:10:41截图显示Aberdeen→Edinburgh的商人路线，端点具体ID待探针确认。

## 建筑机制（STATIC_CONFIRMED）

本机缓存DebugGameplay.sqlite只读核对：
- 大酒店BUILDING_JNR_GRAND_HOTEL：Building_YieldDistrictCopies的OldYieldType=YIELD_CULTURE，NewYieldType=YIELD_CULTURE。另有HD_HOTEL_THEATER_ADJACENCY_TOURISM，ModifierType=MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_ADJACENCY_YIELD_MOFIFIER，SubjectRequirementSet=DISTRICT_IS_THEATER，YieldType=CULTURE、Amount=100。复制产出和相邻旅游为两个独立效果。
- 燃煤电厂BUILDING_COAL_POWER_PLANT：Building_YieldDistrictCopies为PRODUCTION→PRODUCTION；还绑定POWER_PLANT_BUILDING_PRODUCTION_PERCENTAGE_BOOST、POWER_PLANT_DISTRICT_PRODUCTION_PERCENTAGE_BOOST。建筑的复制效果、建造加成及其它供电/区域系统不能混作区域本体Actual adjacency。
- 贸易本埠BUILDING_GOV_CITYSTATES：绑定GOV_SPIES_IMMEDIATE_TRADING_POST，类型MODIFIER_PLAYER_ADJUST_IMMEDIATE_TRADING_POST，参数ImmediateTradingPost=1。由引擎掌握路线关系并创建贸易站，不依赖Gameplay Lua读取city:GetTrade。

源码定位（Steam workshop/content/289070）：2701747165/Database/theater.sql:203、246、284；2465378070/UpdateDataBase/DL_Buildings.sql:282、849、876、906。行业见2616754773/Database/Improvements.sql:163–164、207–208。

Building_YieldDistrictCopies表证明建筑从区域yield复制并产出指定yield，但仅靠表不能证明在这组大型Mod中是否把固定区域加成也纳入复制基数。对“只复制Actual adjacency”还是“额外包含行业固定值”的具体运行边界仍USER_GAME_TEST_REQUIRED，不从名字反推，也不把建筑额外产出加回原区域相邻。后续若需要这条效果路线，应单独比较同区域行业前后、建筑复制前后的城市产出，不用当前getter测试替代。

## 当前设计取舍

严格保持：Base adjacency（基础）/ Actual adjacency（相邻系统经Modifier后的yield）/ 固定区域产出 / 建筑复制产出为不同来源。Industry I/III与Culture IV工作相邻用Base，Research IV与Industry IV用Actual，规则不变。故固定行业+1文化/+3金币目前不进入这些公式。这是现有设计范围，而不是需要修复的漏算。

若用户希望专业能力也分享行业固定区域收益，可以单独设计“可共享区域产出”的明确口径，包括哪些来源与哪些排除；不可仍称Actual adjacency。尤其复制建筑及我们自身城市补贴必须防重复计算、循环反馈。当前没有擅自扩展收益，先报告这个取舍。

## B002商路修订

官方Base/UI/TradeOverview.lua:70、320及TradeSupport.lua:17在UI读取city:GetTrade():GetOutgoingRoutes()和OriginCityID。已改Read routes为明确UI路径，展示现有路线端点；不向Gameplay回写这一UI快照。

Gameplay/Temp_Interface.lua虽有类似helper源码，但此次实机证明当前城市对象GetTrade缺失；文件目录/函数定义不等于该路径在这套配置中实际可调用。今后不以未运行helper做Gameplay确认。

找到更直接Gameplay先例：和而不同Gameplay/Buildings.lua:147–203的SukienniceTradeRouteActivityChanged，以及Commemorations.lua:446–520，接收(playerId, originPlayerId, originCityId, targetPlayerId, targetCityId)。B002只监听TradeRouteActivityChanged，将前五字段及至多六个尾参数标量记录，限定涉及测试玩家，最多32条；Route events (Game)显示选中城最近3条。尚未确认额外参数含义，不按它增删网络，不把“活动事件”称为“建立事件”。

UI现有路线枚举＋Gameplay活动事件是两个独立验证方向。后者无法天然恢复读档前全部有效路线；活动的增删语义、稳定路线身份、终止/掠夺/重载重建仍待解决。正式Gameplay网络重建BLOCKED于缺少已验证的完整权威关系恢复路径；不把已知贸易站当成当前有效路线（贸易站可在路线结束后保留）。不因为UI端点通过就宣布网络实现可行。

## 当前用户仅两项，小批复测

沿用现有存档，手动重启加载P0-B-002，没有SQL增量、无需新局。

1. 选Aberdeen，点Read routes (UI)，Next翻到原来的路线。应FROM Aberdeen，TO Edinburgh，originMatchesSelection=true，sameOwnerRaw=true；选择Edinburgh读取Outgoing不应把这条入站路线算成出站。直接截图。缺失/反向/UNRESOLVED为失败；相邻不重测。
2. 若方便发起一条新路线（截图显示还有一个空余容量，但不要求为了此项强行造商人），在B002加载后建立一条已知A→B，随后选A点Route events (Game)，应出现匹配端点的原始事件。再选B也应可查同一事件。没有新动作时NO_MATCHING_EVENT_OBSERVED是正常未捕获，不是无路线证明；发生明确新建却仍无事件，回传。不要为收集事件取消原来路线。此项可暂缓到自然出现新路线。

PASS只代表各自观察子项通过；绝不代表有效网络恢复通过。已运行test_specialization_p0.py：UI路线无Gameplay派发、方向/分页/空列表/未知端点，Gameplay城GetTrade=nil时事件显示仍正常、非测试玩家事件排除；mock事件字段按源码假设，不是实机签名验收。

本轮修改Probe.lua（版本和UI标签，不改相邻计算）、Gameplay.lua（移除失败的TRADE getter请求，新增只读事件观察）、UI/P0Panel.lua/xml（UI路线和事件按钮）、modinfo、test_specialization_p0.py及报告。备份DevelopmentBackups/SpecializationP0-P0-B-001/。未改SQL、专业收益或网络sqrt，不启动游戏。
