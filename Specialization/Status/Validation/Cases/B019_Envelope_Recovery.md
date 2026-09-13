# B019：合成单表分阶段保存与恢复

Document Owner: Codex
Build: P0-B-019 / modinfo26
Verification: USER_GAME_TEST_REQUIRED

本批尚无游戏证据。使用现有Scotland (Specialization Test)存档；安装新包后退出到主菜单再加载。面板标题必须B019。无须选城市、造区域或过回合。探针只写独立合成Game Property，不操作真实城市成果。不要使用旧Read storage / Write test table按钮。

## B019-1：只记计划后的重载

1. 打开Specialization P0，点击 **Read envelope (B019)**。应为阶段0/6 EMPTY、本次加载写入0、自动读档阶段0、load=true、hook=REGISTERED。
2. 点击一次 **Next envelope stage**。应为1/6 BEFORE_PENDING（计划已记；成果未写）、写入1。保存一张截图。
3. 保存游戏，退出主菜单，重新加载。不要点Next；点击Read envelope。应仍为1/6 BEFORE_PENDING、写入0、自动读档阶段1。保存一张截图。

PASS：计划记录正常保存，加载没有自动补写成果或推进阶段。FAIL：阶段变化、记录丢失、加载写入非0、自动阶段NONE、load=false、异常/无响应。

## B019-2：成果已写后的重载、对账与下一笔

接B019-1第3步，使用同一存档。

1. 点击一次Next，出现2/6 TARGET_PENDING（成果已写；待对账）、本次加载写入1；保存游戏并退出主菜单重新加载。
2. 只点Read，应为2/6 TARGET_PENDING、写入0、自动读档阶段2。保存一张截图。
3. 点击Next，应为3/6 DONE、写入1；点击Read应保持3/6且写入仍1。
4. 每次等显示更新，再依次点三次Next，观察4 BEFORE_PENDING → 5 TARGET_PENDING → 6 DONE；写入依次2→3→4。再点一次Next，应为COMPLETE_NO_WRITE，仍6/6、写入4。保存一张截图。

PASS：加载准确保持目标已写阶段，只有显式Next才对账；第二笔正常推进，全部完成后不重复写。FAIL：阶段跳跃/倒退、错误、重复完成仍写入或数量不同。

总计四张关键截图即可，按顺序投递Specialization/ScreenShots；不用复制剪贴板、重命名或手抄ID。任何一步不符合先停止，不清除Property、不覆盖原测试存档，回传当前截图和最后操作；若有Lua.log，回传含[SPC][B019][ENVELOPE]及ERROR的部分。完整日志可在工作目录Logs中保留供检查。若面板仍B018，先回报版本，不继续测试。未知/坏表没有重置按钮，这是保护行为。

本批不测试异常杀进程、跨owner城市身份、真实资源或资格撤销。正常读档PASS也不等于引擎崩溃原子性通过。
