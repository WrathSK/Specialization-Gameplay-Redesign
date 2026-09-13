# B018：组合资格只读诊断本地交付

Document Owner: Codex
Build: P0-B-018 / modinfo25
Design Reference: D0007

新增QualificationProbe.lua，将Carrier、CurrentPlayerRoster与EligibilityLifecycle候选组合成私有诊断。原型保留在DevelopmentTests；运行封装将生命周期MOCK_ONLY入口显式换为DEV_DIAGNOSTIC_ONLY，READY_OFFLINE改为READY_DIAGNOSTIC，不假装游戏对象是mock，也不导出正式授权API。无Property写入或收益。实际载体/名单接口使用真实Gameplay globals，每轮更新引用，允许初始化时缺失而LoadScreenClose时就绪。

INITIALIZE只观察名单，不发许可；LOAD_CLOSE两次重新查询之间仅撤销私有许可对象，检查旧对象失效与新对象有效。该自检不改变真实玩家资格，不模拟城市征服，不证明实际事件撤销。失败清除诊断许可；内部gate/token不经ExposedMembers暴露，只发布标量表/文字。没有真实周期调度或正式提交器。

UI Runtime eligibility只读取当前版本自动结果，直接显示本玩家许可、名单压缩区间、诊断获准/未知名单、54–61当前成员关系及内部自检。54–61只作证据对照显示，不用于筛选或硬排除。新增按钮位于已有按钮上方，结果区使用紧凑行；实际布局仍待用户截图确认。

LOCAL_SIMULATION_PASS（本地，不等于实机）：六组均exit=0：test_qualification_probe.py、test_specialization_p0.py、test_eligibility_probe.py、test_city_journal_probe.py、test_background_routes.py、test_specialization_identity.py。覆盖实际组合脚本、API晚就绪、名单内未知、名单失效清许可、重载实例、内部失效/重取及旧功能回归。SQL/资源静态检查未新增问题。执行输出见备份目录verification_result.json。

运行新增QualificationProbe.lua；修改Gameplay、Probe版本、modinfo、P0Panel.lua/xml；测试新增test_qualification_probe.py、更新两个运行测试loader/版本。实际B015城市、旧EligibilityProbe、数据库和后台商路源码未变。UUID不变，Design不改，未启动游戏。

备份：DevelopmentBackups/Specialization-before-B018-runtime-qualification。新增实机两案见[B018](../Cases/B018_Runtime_Eligibility.md)，仅USER_GAME_TEST_REQUIRED，无新增实机PASS。
