# B011 本地验证结果

Document Owner: Codex
Build: P0-B-011 / modinfo18
Verification: LOCAL_SIMULATION_PASS

LOCAL_SIMULATION_PASS仅本地模拟，非游戏通过。全部命令使用既有PYTHONPATH=/tmp/city-gpp-test-runtime python3，无新依赖。

已执行并exit 0：test_completion_probe.py（新）、test_specialization_p0.py、test_specialization_identity.py、test_background_routes.py、test_city_role_facts.py、test_trade_route_probe.py。

新增测试执行实际CompletionProbe.lua和P0Panel.lua：原生事件类型/实例区分、放置与完成、owner范围、Load阶段、64条环形记录/丢弃计数、异常/缺失接口、只读分页、新脚本上下文清零与防重复注册。无SetProperty或单位/产出写入。身份SQL/资源引用隔离数据库回归通过，不要求用户重测A1。

运行新增CompletionProbe.lua，Gameplay.lua仅include/start；Probe版本与modinfo18及面板标题对齐，UI新增两个只读按钮。数据库、UUID、原Marker/总督/商路实现不改。旧B010完整运行包新增DevelopmentBackups/SpecializationP0-B010-before-B011-completion-probe备份。实际游戏加载/事件时序与UI布局仍待B011用户验证。

现有test_specialization_p0.py新增加载CompletionProbe.lua以匹配Gameplay include；其余既有测试未修改。测试输出中的通用USER_GAME_TEST_REQUIRED不代表重新派发旧案例；当前只派发B011两案。
