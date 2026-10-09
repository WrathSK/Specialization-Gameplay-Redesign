# B170限定人工验收与B171 P0面板整理

Date: 2026-10-08。B171.198 source `2d3d2f45c6dfc30746d0ac13e5b219abbd76cce6`，对照B170.197；L1 UI表现批次，本地完成，不改Gameplay、永久数据、后台GC/Network/当前能力。实际部署单独记录。

## B170用户反馈与流程纠正

用户明确“人工pass流程1/2”：现有意义延展收益及同回合D变化正常，记B170本批正常自动读取的USER_GAME_TEST_PASS，基于用户文字、无新截图，不伪装成逐图核验。此前最小流程第3步没有指出具体入口；意义延展的左右键实际均为CULTURE_MEANING_STATUS，不存在“意义延展详细报告切换”。该要求撤回，无需用户补做；不是把未测写成PASS。

Shared D普通/详细模式切换的隔离与逐值一致性仍由B170本地测试证明，未新增原生详细切换证据。既有Research/Aesthetic特定详细入口继续保留；不为修正流程添加Meaning详细UI或额外验收。B170实施在已接受范围完成，其全定义扫描/GW子项与native性能未知不被抹掉。

## 15个默认任务按钮

由上至下，三列五行：

| 左 | 中 | 右 |
|---|---|---|
| 城市专业／潜力 | 总督条件 | 专家与岗位 |
| 巨作事实 | 风雅熏陶 | 意义延展 |
| 跨学科研究 | 学以致用 | 主持／学术传统 |
| 科研基础设施 | 标准化模板 | 移民／施工队 |
| 巨作启迪测试 | 结束启迪测试 | 写入诊断日志 |

仍在调查的B168 NEXT/READ/END入口保留，两个按钮相邻。Meaning当前只读报告保留，不显示成启动能力开关。

默认隐藏：旧E2往返/迁移，当前商路/网络来源及接收详细入口，Network隔离对照，工业网络折扣专项，内存观测、GC试运行、自动项目原型及原本已隐藏的旧half/boost/购买/商业/建设实验。隐藏不代表相关收益或模块被停用、不改原验收结论。代码/控件/回调原位保留，可在未来对应任务明确恢复；没有全库删除或GC/Network默认策略变化。Unit右键旧事件观察回调保留并明确仅排障，日常左键读单位。

XML所有task button明确Hidden；去掉旧内存/GC入口在Lua初始化中重新SetHide(false)的覆盖。保留按钮重新定位，消除Templates与旧记录/内存按钮、启迪END与旧networkdetail的碰撞。ReportScroll由310高增至380，Window仍840×664，无新增字体、图标或本地化key。

## 本地验证

[新定向入口](../../../../DevelopmentTests/test_p0_panel_current_layout.py)：**7方法／208 subTest PASS**。执行完整实际P0Panel.lua初始化，核最终可见15项、旧控件隐藏、3×5边界/无重叠/报告间隔、原有18个报告动作、B168 NEXT/READ/END左右键、Meaning左右键只读STATUS、初始化/开关窗口/Shutdown无业务请求或GC/Network更改。所有callbacks/backend原位保留。

Lua解析、XML ID唯一及完整Files清单、modinfo198/P0-B-171.198标识和diff范围检查通过。旧test_compact_p0_panel固定B036/manifest45及旧路径，保持历史原断言不运行、不改成当前绿色。没有运行Gameplay regression/stress、外部DB或游戏。

修改运行源码仅UI/P0Panel.lua/XML及Probe/modinfo版本标识。定向测试新增，现有Design、其它Gameplay、旧测试、冻结审计、部署工具和main不变。实际字体/分辨率/UI scale仍待原生显示，几何模拟不当截图验收。

## 使用与停止

本批不设置独立强制UI门禁，也不重复B170保存/收益测试。下一次正常使用面板时，顺带确认15项、无重叠、报告滚动与长中文正常即可；异常再定域处理。B168精度调查独立继续，不启用Floor或正式L3。完成检查点并按现有W0003安全门禁处理部署后停止，不自动开始其它审计修复或玩法。
