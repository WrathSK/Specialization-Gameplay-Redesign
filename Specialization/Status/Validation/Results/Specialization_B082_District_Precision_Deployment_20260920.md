# B082.109 区域精度实验部署

W0003授权有效；只读ps确认游戏退出，没有启动/操作游戏。实施commit `9e6a1061c97578b4a05b0e917985714d559218a0`，commit/push且clean后部署。

通过现有temporary_playtest完成B081→stable→B082。131文件逐项SHA256完全一致，modinfo109，digest `1e56c4449b7fed86df7ff93015be3382be5a56bab3158e516626ee3fff29ea91`。不是promotion。

- live：外部既有SpecializationP0，诊断版本应为P0-B-082.109。
- receipt：运行目录同级上层SpecializationDeploymentBackups/B082.109-9e6a106-playtest.json，DEVELOP_ACTIVE。
- B081完整恢复点：SpecializationDeploymentBackups/.temporary-develop-backup-5rs2g74_；128文件，digest `7e481a836717d850d532eda187b4f0e7c9bcd81494af029f2b155ddd68ecaeb0`，已复核。旧receipt保留其路径。
- main保持 `e3651f9b7c90110f3a8890a7b12ca299996b306b` / B069.96，无修改。

实验默认OFF；最小流程见[实验合同](../../../Architecture/v2/P0_D1_District_Precision_Probe.md)。本地PASS不等于原生小数PASS；P0-D1正式cutover未开始。独立测试存档，结束OFF，不把实验收益带入长局。
