# B060 新组件未加载

Document Owner: Codex

B060.85用户截图已收到ACK，明确GWA_MODULE_NOT_LOADED，后台模块=false、本次已收到=true；不是学院BASE=0的证据。用户确认本城学院BASE Science +2。2026-09-13只读检查：当前Startup.log InitialInit 11:28:27；最新DebugGameplay.sqlite更新时间12:14:08，BUILDING_SPC_B060_%为0（应156）；12:14:18 Modding.log注册/应用B059但没有SPC_B060_Adjacency。磁盘manifest包含B060组件。证据支持当前进程组件清单未刷新，新Lua模块/SQL均未完整加载。先完全退出应用重启、读原存档再验证，不改代码、不删缓存、不新建局。

USER_GAME_TEST_PASS仅限85报告成功揭示模块缺失；相邻读取/收益仍USER_GAME_TEST_REQUIRED。最小测试：用户完全退出Civ VI后重启并加载原存档，选同Culture4城，GW adjacency Read。学院BASE+2应贡献SCIENCE BASE=2、每件=1（其它专业区域Science基础相邻若有则另计）；报告正常后才继续原收益批次。若仍失败只回传完整报告。上一轮“回主菜单重载”不足，已更正。

外部证据：W/Specialization/Status/Validation/Evidence/B060-85-Module-Missing/manifest.json。源码与运行维持B060.85；Design D0023未改。
