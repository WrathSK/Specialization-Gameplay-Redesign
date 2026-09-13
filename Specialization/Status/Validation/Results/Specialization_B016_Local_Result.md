# B016本地交付结果

Document Owner: Codex
Build: P0-B-016 / modinfo23
Design: D0007 / unchanged

LOCAL_SIMULATION_PASS：本地模拟，不等于Civ VI实机通过。

- test_eligibility_probe.py：实际运行脚本自动初始化/加载结束、多个玩家绑定、未就绪/读表中断、重建会话、缺失事件、无城市/Property/UI访问；XML/manifest引用。
- test_specialization_p0.py：原有窄请求/写入/诊断回归与新按钮只读缓存通过。第一次执行因测试loader未加载EligibilityProbe失败，补入真实模块后通过；没有用stub绕过。
- test_specialization_identity.py：实际SQL/原版资源引用检查通过，隔离SQLite通过；不扩大实机证据。
- test_city_journal_probe.py：B015城市资格/完成/重载/故障停止回归通过。
- test_background_routes.py：后台UI商路影子回归通过，仍非权威Gameplay路线。

STATIC_CONFIRMED：新文件在ImportFiles及Files各注册一次；Gameplay启动；UI新增按钮只显示当前版本缓存，无请求/扫描；UUID不变。脚本两次轻量玩家配置读取不等于正式参与者周期处理；没有新建专业状态、没有使用资格结果启用收益。诊断不读取Human，未宣称AI实机通过。

新增运行EligibilityProbe.lua，修改Gameplay.lua、Probe.lua版本、modinfo、P0Panel.lua/xml；新增test_eligibility_probe.py，更新test_specialization_p0.py的真实模块loader及按钮断言。旧CityJournal/Binding/DB/后台商路源码保持，Design不改。当前所有旧探针照旧运行，本轮只保证新增资格诊断本身无写入。

备份及校验：DevelopmentBackups/SpecializationP0-B015-before-B016-eligibility。结果计划见[B016两案](../Cases/B016_Eligibility.md)。USER_GAME_TEST_REQUIRED：等待用户验证自动采样和读档；未启动游戏，没有新增实机PASS。
