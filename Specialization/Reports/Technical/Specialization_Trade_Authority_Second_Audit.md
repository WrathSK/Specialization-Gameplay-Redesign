# Gameplay商路权威来源：第二轮静态复核

> 交接取代说明：纯Gameplay未找到全集的证据保留；本文原“正式来源BLOCKED/不得后台UI”的当时授权限制已被用户G0006明确取消。当前采用后台UI完整来源并有运行桥接，不再提议用户重新授权同一方向。

Document Owner: Codex
Design Rule ID: NET-002至004 / NET-RC-002至004
Architecture Revision: A0004
Research Outcome: NO_NEW_FULL_ENUMERATION_PATH_CONFIRMED

## 结论与证据等级

STATIC_CONFIRMED仅指本机源码、modinfo、缓存数据库和二进制字符串证据，不等于游戏调用通过。当前仍未找到可确认覆盖全体己方当前商路、可重建端点的Gameplay Lua来源；不能证明引擎绝对不存在隐藏接口。正式来源维持BLOCKED，不改用UI、历史事件或虚拟建筑冒充。

这次新增核查的是GameEffects当前Modifier对象及原生商路collection，不重试B005已返回nil的operation坐标。只读扫描官方Assets、HD及已安装workshop Lua/SQL/XML；数据库mode=ro，无任何游戏进程操作。具体文件hash与查询结果见[静态证据](Specialization_Trade_Authority_Second_Audit_Evidence.json)。

## 新证据与边界

| 路径/先例 | 能证明什么 | 缺口 |
|---|---|---|
| HD Gameplay/CityYield.lua:139–158；DL.modinfo:1867–1870 | AddGameplayScripts明确加载；GameEffects.GetModifiers/GetModifierDefinition/GetModifierOwner/GetObjectString用于读档重建城市收益缓存 | 先例枚举的是Modifier而非所有商路；只筛选YIELD_CREATOR类，不包含商路全集承诺 |
| GameCore_XP2.dll中Lua_IGameEffects.cpp附近 | 存在GetModifierSubjects、GetModifierTrackedObjects、GetObjectType、GetObjectsPlayerId等名称及参数错误文本 | 符号不是运行可用性/返回schema证明；未发现直接枚举所有游戏对象的对应先例，不能把GetModifiers当GetAllTradeRoutes |
| 缓存DynamicModifiers查询CollectionType LIKE %TRADE% | 三条定义，仅COLLECTION_ALLIANCE_TRADEROUTES和COLLECTION_EMERGENCY_TRADE_ROUTES两种集合 | 联盟/紧急事件特定上下文不足以覆盖普通国内路线；给玩家附加这些Modifier不能自行保证枚举全体商路 |
| 官方Expansion2/Data/Expansion1_Modifiers.xml:278/283/374 | 对应取消路线/调整路线yield的原生效果确实使用上述受限集合 | 不证明可用COLLECTION_PLAYER_TRADE_ROUTES或COLLECTION_ALL_TRADE_ROUTES；安装内容扫描未找到这两个名字的定义/用例 |
| 其它安装Mod：2428969051/ui/dmt_modifiercalculator.lua:102、1312585482/BRSPage_Yields.lua:89/138 | 有GetModifierSubjects的UI分析用途；后者注明subject与tracked对象的过滤差异 | 不把注释当引擎契约；更不能把“受效果跟踪的对象”当全体当前商路 |

原生HasTradeRoute字符串只出现在一组一般状态/错误标签旁，不能据此发明City/Unit方法。未发现新的GetOperationParameter调用签名先例；不穷举数字参数、不对引擎对象做元表扫描。

## 已有路径复核

- 官方TradeSupport.lua:17、TradeOverview.lua:70/157和HD/BTS TradeSupport.lua:216等仍终止于UI City:GetTrade():GetOutgoingRoutes。它们不要求玩家打开窗口，但执行上下文仍是UI；B007/B009成功范围不改变。
- HD Temp_Interface的目录名不能证明Gameplay；CityYield.lua则有真实Gameplay注册证据，两者明确区分。
- BTS TradeSupport.lua:98–126的GetLastRouteForTrader读取上次端点，用于自动重复商路。历史端点+当前任务存在并未证明任务和该历史端点对应；不作为新测试方案。
- B005已有用户证据：商人任务/数量和加载读取通过，坐标参数nil。没有新签名证据就不重新派发该实验。
- CountOutgoingRoutes和可建路线判断仍只分别提供数量/潜在合法性。等数量换线无法由计数识别；交易站和标志建筑也可能在路线结束后保留，不能据此重建事实。

## 为什么本轮没有GameEffects探针

要升级为值得用户测试的候选，至少先具备：覆盖全部普通国内商路的集合来源；能映射稳定快照身份及双向端点的对象字段；明确Gameplay注册与无状态写入的读取方式。目前前两项都缺失。在只含联盟/紧急事件对象的存档上测试返回若干subjects，无法验收所需全集，也不能将空结果判为无路线。

本轮不添加零收益Modifier/虚拟建筑、不注册运行脚本，不把特定集合的并集宣称全集。没有新增USER_GAME_TEST_REQUIRED批次，B010维持延后。

## 次优路径与设计边界

1. 保持当前契约：继续需要新的官方/本机Gameplay全集证据；没有证据前正式Network结算不启用。
2. 后台UI桥接：现有成功读取可作为候选技术来源，但若将其升级为权威，会改变用户明确要求的“正式状态不依赖UI Snapshot”。它还需要跨上下文同步、加载就绪、多人一致性、撤销与未知状态结算规则；不是仅开个接口即可等价。
3. 原生连通性/效果标记：可能只支持网络接收资格而不暴露route records；这会改变当前状态层契约，且目前尚无完整连通性来源证明。

若将来选择2或3，须先提交具体可审核方案并标DESIGN_DECISION_REQUIRED，不能静默fallback。本轮没有要求用户立即放宽约束，没有改变Design Spec。建议不再无依据重试旧接口；在权威来源缺口解决前，可独立推进不依赖网络的本地能力适配研究。

## 本轮验证与保护

无功能改动、无本地模拟新结果、无游戏PASS。源码/Tests/Accepted Design/既有Historical/Backups/截图全部保持原内容。Architecture仅登记研究边界，Status保留原实机结果和B010延后状态。
