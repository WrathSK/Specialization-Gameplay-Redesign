# B068.95 按钮文字与潜力标识修正

Document Owner: Codex

USER_GAME_TEST_PASS（用户实机口述通过）：移民/施工队紫色滤镜、左上诊断入口位置。不能扩大为全部读取项/日志导出均通过。
USER_GAME_TEST_FAIL：用户报告所有诊断按钮无文字，点击似乎仍有效。未提供新截图。

已查看本机UserInterface.log与Localization.log，并复制冻结到外部Evidence/B068-Blank-Captions-Logs，保留原日志。可见现有SPC内部建筑图标缺失及其它Mod本地化参数错误，没有直接证明空白文字根因；当前日志目录及已搜索投递路径未找到Lua.log，不能宣称SPC_DIAGNOSTIC_REPORT实际日志导出已通过。

B068.95以显式居中FontNormal14 Label替代17个可见按钮（15入口+打开/关闭）的GridButton内置String，同时初始化时SetText。原回调/布局/隐藏状态不变；根因尚非实机确认，修正策略是绕过按钮内部文字路径。潜力Badge改挂同一WorldTrackerHeader，x=header width+8、y=36，165×28；文字仅“科研1级/文化4级/工业1级/商业2级”，无空格，仍指永久Potential。悬停保留专业、潜力、投资次数与Governor说明；切城失选和只读请求不变。

STATIC_CONFIRMED：6个UI/版本文件变化，其余108个运行文件包括Gameplay、所有收益、滤镜完全相同；D0025不变。恢复点local/before-b068-95。
LOCAL_SIMULATION_PASS：test_b068_95.py沿用实际B068 UI mock，显式文字17项、读取/导出回调、Potential1–4、选中切换、同header位置；全部Lua/XML语法通过，git diff --check无错误。模拟不能代替游戏字体渲染。

USER_GAME_TEST_REQUIRED：旧存档重载后，仅看按钮中文是否恢复、选中两座不同专业/潜力城市时左上短标识是否正确并位于诊断入口下方。无需重测滤镜、收益、网络或单位消耗。若仍空白，仅需一张完整面板截图；Lua.log若实际存在可一并回传，不要求更改游戏配置。

源码文件：UI/P0Panel.lua/xml、UI/CityPotential.lua/xml、Probe.lua、SpecializationP0.modinfo。新增测试test_b068_95.py；README/Architecture/Status同步。无Design修改，无启动游戏，无commit/push。
