# B040入口不可见：修正待复验
Document Owner: Codex
Build: B040 / modinfo52
State: USER_GAME_TEST_REQUIRED

用户报告找不到Unit sites按钮：入口可见性USER_GAME_TEST_FAIL，不能判断Gameplay位置接口失败。
当前本机Modding.log列出SPC_B040_UnitSites Applying Component；未找到Lua.log，不能据此认定唯一根因。源码遗漏显式根Context显示和InitHandler，按钮默认隐藏且只按选择解锁。
修正：InitHandler内绑定控件/更新，LoadScreenClose显式显示test-civ根Context；按钮对test-civ常显，无合适单位点击显示提示；移动/改选清旧报告保留。不改位置逻辑/消费/Design。窗口标题B040.52。
test_unit_site_visibility.py复用旧模块测试并适配52生命周期mock，初始化、读档显示、无选择提示、请求/回应、移动清除通过LOCAL_SIMULATION_PASS；不是实机PASS。
仅需重载原存档检查右上P0下方入口；若仍不见回传全屏截图（含右上P0）。出现后继续原三案，无需重建城市。
备份DevelopmentBackups/Specialization-before-B040-visibility-fix。
