> 后续进度B006：已实现独立后台UI shadow reader（不依赖BTS），静态/模拟通过，实机待验。下文“尚未实现”是调查时历史；正式收益/权威来源约束保持，见B006_Background_Routes。

# Better Trade Screen 后台读取方案调查

2026-09-11。用户提出不打开UI而触发其读取逻辑的思路；本轮只调查并记录，不把候选自动升级为正式权威来源。运行包仍B005。

## STATIC_CONFIRMED

本机BTS位于Steam workshop/289070/873246701。UI/TradeSupport.lua:211 CheckConsistencyWithMyRunningRoutes遍历玩家城市并调用city:GetTrade():GetOutgoingRoutes()，将其与缓存比对，补入新增并删除不存在项。260行LoadRunningRoutesInfo载入历史缓存后，273行调用该一致性检查。2262行Tracker初始化调用LoadRunningRoutesInfo并注册operation/turn等事件。TradeOverview.lua:2316 Initialize调用Tracker初始化，而1871行OnOpen只进入Open；数据读取并非必须由打开窗口动作触发。

TradeOverview.lua:197 Refresh还刷新排序、筛选和控件实例；不宜直接调用整个Refresh/Open作为无窗口数据接口。应只借鉴实际读取流程，独立写窄数据采样器，不调用BTS私有函数、不复制其缓存计时算法、不硬依赖BTS。

此前我们Read routes (UI)按钮是在自己的P0 UI context直接调用引擎城市GetTrade/GetOutgoingRoutes，没有读取BTS的表、按钮或截图。BTS与官方/我们的UI采样底层使用同类引擎接口。

## 候选架构与边界

无需打开窗口的独立InGame UI context自动采样，在初始化/load就绪、路线dirty及必要核对时读取当前全集，复制必需标量，附generation/turn/complete/sourceContext=UI，交给Gameplay侧对照。先只做shadow diagnostic，不喂正式RouteState的GAMEPLAY_CURRENT契约或发收益。

Gameplay已有商人任务/计数可作交叉校验，还可核对端点当前存在与owner；计数相等不能证明端点完整或正确。缺帧/缺UI context/部分读取均UNKNOWN，不沿用旧快照。初始化先后、同回合失效撤销、多人同步/非本地玩家视图仍USER_GAME_TEST_REQUIRED。

这个方向能避免玩家打开面板，但仍依赖UI context，是数据桥接，并不会使缺失的Gameplay getter出现。用户最新思路允许研究该方案；此前“完全不依赖UI snapshot作为权威”约束尚不能宣称由此满足。若后续采用其作为正式数据源，需明确修订权威架构和单人/多人适用范围，而非悄悄给UI数据改名。

当前建议优先下一步验证独立后台UI shadow reader的初始化/恢复/撤销，再决定是否改变正式来源；保留纯Gameplay任务读取作为校验线索。当前没有实现后台桥接、没有新增用户测试、没有游戏启动。
