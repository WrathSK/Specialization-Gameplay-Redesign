# B087.114 U1展示原型部署

W0003持续授权；只读OS确认游戏退出，未启动游戏。实现commit 8dc611879d7e8c101dcca95a7f183df9674e3a8f 已push。147文件逐文件hash/清单与运行包一致：1f2d753c8d186d7cc75cbb42f43e2715ea49a716707025dbbd4accc2de15fa14。

初次直接activate被既有“runtime必须是stable”门禁拒绝，发生于任何备份/写入之前。随后按历史流程restore B086→stable桥→activate B087，两次事务成功，无门禁绕过。

B086完整恢复点：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/.temporary-develop-backup-efozu0mi`，hash 52215943b62d8ce72d1d7c376f9094a1ff0536946261fcc3eabf13e98b6208c6。
stable恢复点：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/.temporary-stable-backup-t2zblnph`，hash 7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df。
部署receipt：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/B087.114-8dc6118-playtest.json`。

main保持e3651f9，无promotion/tag/游戏配置或其它Mod改动。真实显示仍待用户确认；最小步骤见[原型报告](../../../Architecture/v2/U1_Presentation_Prototype.md)。不继续完整U1。
