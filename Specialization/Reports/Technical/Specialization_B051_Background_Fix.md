# B051.66 后台事件刷新与分段诊断

Document Owner: Codex
Design: D0013 unchanged
Build: P0-B-051 / modinfo66
Validation: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED

## 证据与修改

[新截图](../../Status/Validation/Results/Specialization_B051_Copy_Diagnostic.md)显示自动SCIENCE目标未知、已配置0，而UI只读合计6/目标3。正式路径未能计算，尚不能证明是效果挂载失效。

旧CopyYieldRefresh只依靠空UI context的SetUpdate计时器；不同于已用户实测的IndustryRefresh，其没有GameCoreEventPublishComplete/PlaybackComplete等入口。是否正是用户机器的根因尚待验证，不能只凭静态差异定论。

现在加入上述引擎事件、PlayerTurnActivated、LoadScreenClose与初始化SystemUpdateUI fallback；保留计时器作补充。签名/序号防重复与busy防请求引发事件重入保持，读档代际变化强制再提交。不要求点击面板，不利用读报告动作补发奖励。

新增只读诊断：后台加载/采样状态、请求次数、Gameplay接收序号、有效批次回合、接收错误和目标计算错误码。不在界面显示完整调用栈。Gameplay收到无效快照仍撤销旧效果，不将未知伪装成有效0。公式、目标范围、SQL载体和结算函数均未改。

## 本地验证

DevelopmentTests/test_b051_background_fix.py复用原实际Lua测试场景，但所有周期触发改为游戏事件，完全不调用逐帧update；模拟请求中同步发布事件以验证不递归累加。覆盖原max/半点/人口/撤销/重载/重复测试，再测Gameplay重载监听先后顺序与SystemUpdateUI恢复，以及COPY_BACKGROUND_PENDING直接显示。LOCAL_SIMULATION_PASS指本地模拟，不是实机。

SQL仍从只读数据库复制到内存检查；数据库已含B051时，仅移除内存副本中的本批定义再执行原SQL，不改实际数据库。全Lua/XML/manifest通过；CopyYields.sql、Plan/target/reconcile及关键Crew/Investment/NetworkBridge文件保持。STATIC_CONFIRMED不代表原生运行通过。

## 最小复验（仅一座科研城）

重新加载现有存档，确认标题/报告显示B051.66。保持图中ACTIVE4科研城与工业区，先不开专门面板观察城市科技，再点Read Lv4 copy。

若工业区仍6且没有其它基数变动：SCIENCE本项预期=3、已配置=3；真实科技应增加对应金额（城市倍率仍按原生计算）。没有其它变化且无百分比影响时12.1875应约15.1875。重复读取不累加。用户已接受的界面滞后可过一回合观察，但如报告仍未知/0，直接回传报告即可，不必再做总督往返/调专家。

若后台未启动或采样/接收/计算失败，新报告会给具体阶段与错误码；一张完整报告足以决定下一步。修正仍USER_GAME_TEST_REQUIRED，不重新派原三案。工业接收城失败未关闭，待科研路径确认后复核同一修正是否覆盖工业。
