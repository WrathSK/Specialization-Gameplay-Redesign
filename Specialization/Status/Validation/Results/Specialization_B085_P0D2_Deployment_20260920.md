# B085.112 / modinfo112 — P0-D2 deployment

W0003持续开发测试授权。安全只读OS检查：无Civilization VI进程；没有启动游戏。两个worktree在事务前clean。实现commit `f149f8434a48419b11f618fe4cff857c274e2d8d`已push origin/develop；main仍`e3651f9b7c90110f3a8890a7b12ca299996b306b`，无promotion/tag。

通过现有temporary_playtest执行B084→stable恢复桥→B085；140文件逐项SHA256/清单一致。
package digest: `573b43d03017ff94da7f8b6eb23589f78fe1189f82b902ab92c6e363296fcabc`。

运行目录：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods/SpecializationP0`。
恢复点根目录：相邻`SpecializationDeploymentBackups`（不在Mods内）。

- B084完整恢复包：`.temporary-develop-backup-go8xo6eu`，137文件；digest `9607d29df06776d55d099a97ebac2f5f89b5c96e91de2a2b95800522b51e6083`，与切换前逐项一致。
- B085 receipt：`B085.112-f149f84-playtest.json`，DEVELOP_ACTIVE。
- 稳定恢复包：`.temporary-stable-backup-tztezp25`；digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`。
- B083等既有恢复点保留。没有修改存档、其它Mod或游戏配置。

## 最小用户验收

确认诊断标题`P0-B-085.112`。一座科研ACTIVE III城，学院＋普通工业/商业领域建筑；点击**学以致用**（左摘要、右领域/建筑组成）。0→1→2名工作科研专家，按“每名floor”核对原生收益，注意基础3F3P和其它能力独立存在。

示例：单领域D1生产力原值0.5→每名0，两名仍0；商业D3金币原值4.5→每名4，两名8。增加普通建筑后核对D增长；方便时ACTIVE降级/恢复、存读档一次确认不叠加。无需手动掠夺、不运行旧精度实验。新载体入档后的旧版本存档兼容不保证，保留切换前独立存档。

LOCAL_SIMULATION_PASS：本地模拟，不等于Civ VI实机通过。当前USER_GAME_TEST_REQUIRED。P0-D3未开始。
