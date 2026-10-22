# B115 — 开始观察时空目标判据失败

2026-09-27，B115.142，21回合，城131073。用户在第一步停止；已实际查看21:02:37原图。**USER_GAME_TEST_FAIL：观察未能开始**，不是完整生产结算方案的实机反证。无需继续后续流程。

截图显示STOPPED、Gameplay目标非空：NONE，断言位置TimedProductionProbe.lua:79；事件0条。UI队列=0，城市面板显示没有生产任何东西，右下角选择生产项目。原生当前场景CurrentlyBuilding返回字符串NONE；B115开始及后续sample仅将nil/空字符串认作无目标，误拒绝了本场景。45项本地fixture默认空字符串，未覆盖该原生返回值。异步请求已到Gameplay并发布拒绝，不应重新调查为请求桥未送达。

UI另显示“当前目标进度：纪念碑=0”，但代码在队列为空时仍用hash查所有GameInfo表，截图没有显示raw hash，不能断言是0索引碰撞还是原生残留引用。此读数不能证明正在生产纪念碑；后续应先检查队列为空，不解析目标，非空时再核对目标类型/有效hash。错误堆栈被原样带入简报导致不可读，应改为简短原因，将详细错误保留日志。

建议修复范围：统一显式NONE空目标识别用于开始与后续采样，仍拒绝真实非空目标/未知接口，不放宽其它归属与按钮保护；补原生NONE fixture和空队列诊断测试；压缩错误展示。仅建议，本次未改runtime或部署。分类：NATIVE_EMPTY_TARGET_SENTINEL_BOUNDARY，外加DIAGNOSTIC_PRESENTATION_DEFECT。

## 用户测试操作更正

用户明确：开始生产后不能通过普通操作让城市恢复什么都不生产，只能完成后不选新目标。此前“先选Q再清空”测试说明错误。用户可执行基线改为自然完成后的空队列A→开启观察→正常跨一回合→报告→选择此前未投入的Q→立即报告。中断负例需另一次自然空队列→开始→选择Q，即可证明中断；不要求再清空。切换再清空仅保留为本地防御性模拟，不是原生已验证操作，不允许为此自动清队列。

B114按钮限定实机PASS保留。B115本轮没有生产结算/收获/溢出/保存证据，没有新Design决定；先修开始门禁再继续最小测试。

## 原始证据

`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B115_Empty_Target_Boundary_20260927/Screenshot 2026-09-27 at 9.02.37 PM.png`

SHA256：`83c92f40da9705f91f13f0fce9bca97603f4354d260cf413368d711854b31cb6`。已读原图，移动前后hash一致。
