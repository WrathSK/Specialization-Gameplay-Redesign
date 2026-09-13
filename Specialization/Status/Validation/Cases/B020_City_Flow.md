# B020：真实新城DEV流程，两案

Document Owner: Codex
Build: P0-B-020 / modinfo27
Verification: USER_GAME_TEST_REQUIRED

使用现有测试文明存档即可。更新后退主菜单重新加载，面板必须B020。本批仅创建一座新城，不要同时建其它新城，以便玩家级写入计数易核对。只用Read city flow (B020)，不要点B019 Next。不能用本次加载前已存在城市代替新城。

## B020-1：新城→首个学院完成（同一次加载）

1. 在本次加载后正常建立一座新城，选中它，点击Read city flow (B020)。应DONE、rev=3、DEV=NONE/0、LIVE_THIS_LOAD、本次加载写入3、stopped=false、最近FOUNDATION_DONE。截图1。
2. 在此城放置学院但未完成，点击Read：仍NONE/0、rev3、写入3。不用为此单独截图，若不符则截图并停止。
3. 完成学院（Cheat Panel可用，请简单说明完成方式），再次Read。应DONE、rev=6、DEV=RESEARCH/1、LIVE_THIS_LOAD、写入6、stopped=false、最近COMPLETION_DONE。截图2。

PASS：只在真正完成学院后更新，旧B015与B020事件接线正常，新表三阶段完整写入。任一字段不符、错误/停住、写入计数非预期即FAIL候选，先回报。

## B020-2：保存重载，只读保持

保存上述游戏，退主菜单重新加载，选同一城市，点击Read city flow。
应DONE、rev=6、DEV=RESEARCH/1、LOAD_READ_ONLY、本次加载写入0、stopped=false。再次Read数值仍保持。截图3。
PASS：原记录保持，加载和重复读取不写入。LOAD_READ_ONLY是本批明确限制，不是错误；本批不验证重载后继续给该城写新专业事实。

总计三张关键截图，按顺序投递Specialization/ScreenShots，默认文件名即可。失败保留当前截图、最后操作和存档；如有Lua.log，保留[SPC][B020]、[B015][JOURNAL]及ERROR附近内容。无需反复点击、删Property或重新做旧测试。无新建文明/修改收益要求。
