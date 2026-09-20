# B086.113 / modinfo113 — P0-D3 test deployment

W0003持续开发测试授权。只读OS检查确认无Civ VI进程；没有启动游戏。两个Git worktree部署前clean。实现commit `84a6f12ce2c7dc8bf727892cd2d2d5b2a88bf50e`已push origin/develop；main仍`e3651f9b7c90110f3a8890a7b12ca299996b306b`，无promotion/tag。

现有temporary_playtest事务：B085恢复stable桥，再activate B086。源码/运行包143文件逐项SHA256/清单一致，digest `52215943b62d8ce72d1d7c376f9094a1ff0536946261fcc3eabf13e98b6208c6`。

运行目录：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods/SpecializationP0`。
恢复点根目录：相邻`SpecializationDeploymentBackups`（Mods外）。

- B085完整恢复：`.temporary-develop-backup-j94a5v8v`，140文件，digest `573b43d03017ff94da7f8b6eb23589f78fe1189f82b902ab92c6e363296fcabc`。
- B086 receipt：`B086.113-84a6f12-playtest.json`，DEVELOP_ACTIVE。
- stable恢复：`.temporary-stable-backup-49lwobfi`，digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`。
- B084及更早恢复点保留。没有修改游戏配置/存档/其它Mod。

## 一次最小用户验收

1. 确认标题P0-B-086.113；选择Research ACTIVE IV城，已有图书馆、大学等两座合格普通学院建筑。
2. **学术主持**左键摘要、右键逐栋明细；0→1→2名工作科研专家。每增加1专家，每座合格建筑基础Science应+1；两栋、两名时主持合计+4。对照原生建筑收益明细，不仅看城市总量（P0-C也会改变科技）。
3. 增加一座普通学院建筑看新建筑同样+W；便利时ACTIVE降级/恢复及存读档一次，确认没有叠加。无需人工掠夺，不用旧精度实验。

保持切换前独立存档；新carrier入档后的旧包向后兼容不承诺。LOCAL_SIMULATION_PASS（本地通过，非引擎PASS）；正式逐建筑收益USER_GAME_TEST_REQUIRED。完成后仅等待用户验收，不开始下一批。
