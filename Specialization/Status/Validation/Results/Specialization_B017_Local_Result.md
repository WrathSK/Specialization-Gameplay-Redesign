# B017本地交付：未知槽位可读明细

Document Owner: Codex
Build: P0-B-017 / modinfo24

本轮搜索现有Logs及工作区可发现的Lua日志，未找到B016逐槽位输出；没有修改日志开关或游戏配置。不能据1/55/8汇总断言未知8的原因。此前B016两案通过结论不变。

新增UI按钮Eligibility unknowns直接读取Gameplay已有LOAD_CLOSE缓存，每页8个UNKNOWN，按编号排序；已知assert原因缩为完整代码，其它错误截取90字符，原始原因保持于缓存。按钮无采样、无请求、无写入；没有改变实际EligibilityProbe或Gameplay采样代码，不以空文明名推断玩家永不参与。

LOCAL_SIMULATION_PASS（本地模拟，不等于实机）：test_specialization_p0.py覆盖真实按钮的9条分页、非UNKNOWN排除、无缓存、无请求/原记录不变及原P0回归；test_eligibility_probe.py实际模块/manifest回归通过，仅更新测试版本预期。XML解析与加载引用通过。

修改Probe.lua版本、modinfo、UI/P0Panel.lua/xml和上述两组测试；实际EligibilityProbe.lua及Gameplay.lua未变。Design、数据库、UUID和配置不变。备份/差异校验在DevelopmentBackups/Specialization-before-B017-unknown-details。未启动游戏。

[用户单案](../Cases/B017_Unknown_Slots.md)只补未知原因，不重复初始化/重载验证。正式资格服务不能把UNKNOWN当DISABLED或启用；若未来缩小到活跃玩家集合，还需验证名单API，而不能仅为清零未知数字改变语义。
