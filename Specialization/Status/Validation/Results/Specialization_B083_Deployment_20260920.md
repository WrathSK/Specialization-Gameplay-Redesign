# B083.110 实验工具修复部署

W0003有效，部署前只读ps再次确认无Civ VI进程。实施commit `8a163f2045c432f9c15877656187ba9a5eaeacea`已push且clean。使用temporary_playtest B082→stable→B083，未启动游戏。

131文件逐项SHA256与Mod/完全一致，modinfo110；digest `a508c6def28d40ce18e95df67edfd39bd261b5703ddac33fc9a833fc9836e9af`。

- receipt：外部SpecializationDeploymentBackups/B083.110-8a163f2-playtest.json，DEVELOP_ACTIVE。
- B082完整备份：同目录 `.temporary-develop-backup-jrku85fm`，digest `1e56c4449b7fed86df7ff93015be3382be5a56bab3158e516626ee3fff29ea91`，已复核；更早B081恢复点仍保留。
- main仍 `e3651f9b7c90110f3a8890a7b12ca299996b306b`，无修改。

游戏诊断应显示P0-B-083.110。原生精度仍待测，旧正式收益不变。测试步骤不增加：OFF/读数→0.3/读数→0.5/读数→1/读数→OFF/读数；同城同回合保持人口/专家/政策不变，最后报告一张即可。
