# B068.94 本地结果

Document Owner: Codex

STATIC_CONFIRMED：D0025哈希不变；全部Lua语法/XML/manifest文件存在与去重，git diff --check通过；精确20文件差异记录，94既有文件不变，原Gameplay只读新增之外逐字一致。

LOCAL_SIMULATION_PASS：test_b068_ui.py全部通过；test_b068_regression.py全部通过（只适配版本及批准的面板15入口+关闭上限16；原机制断言保留）。包括城市标识1–4、切城/失选、真实只读dispatch、相同目标不重画、失选清层、日志去重、真实面板init/anchor/read/export；保留原核心和隔离回归。不是引擎原生UI验证。

源码与部署114文件哈希一致：784bee62c8707090eab02b9b2fae3dae93736bff694ce9d6b9b782cf0d961a6e。

USER_GAME_TEST_REQUIRED：HUD布局/紫色原生层/切换兼容/Tooltip/Lua.log保存。

用户新投递Screenshot 2026-09-13 at 5.16.46 PM已读取，作为改动前HUD参考归档到外部Evidence/B068-UI-Before，原名和SHA256保留，不作为本轮实机PASS。
