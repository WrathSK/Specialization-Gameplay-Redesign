# B025：Gameplay数量校验接口错误

Document Owner: Codex
Verification: USER_GAME_TEST_FAIL（网络读取未完成）

用户先测试科研首都天然贸易中心与其向外分发。两图00:30:20首都Stirling、00:30:40目的城纽约均B025 NETWORK UNKNOWN，NetworkBridge.lua:34 function expected instead of nil，调用栈经过Receive及Gameplay请求入口。截图顶栏路线数由2/4至3/4，但不从此推断具体路线拓扑。

第34行误用UI的GetNumOutgoingRoutes；既有Gameplay TradeRouteProbe明确使用CountOutgoingRoutes。说明请求已抵达Gameplay并通过前面的数据解析/端点检查，到计数校验失败；尚未证明网络派生或首都身份通过，也不代表BTS上游数据不可靠。

[两图](../Evidence/B025-Fail/)已原名移动归档，SHA256一致。原B025测试结果为失败，不升级后续B026。用户测试顺序调整为首都优先，无需先准备双专业商业中心组合。
