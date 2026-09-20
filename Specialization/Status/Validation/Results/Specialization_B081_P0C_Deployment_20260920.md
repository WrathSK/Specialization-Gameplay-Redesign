# B081.108 / P0-C 临时开发测试部署

2026-09-20，W0003 standing authorization。实施commit `6736fc55f5f7e3f890a89c830e3ece59d0067008` 已push、develop clean。只读ps确认Civ VI/launcher无匹配进程；未启动/退出/操作游戏。

通过现有temporary_playtest restore B080→stable，再activate stable→B081。128个文件逐项SHA256完全对应已提交Mod/，modinfo108；集合digest `7e481a836717d850d532eda187b4f0e7c9bcd81494af029f2b155ddd68ecaeb0`。不是stable promotion。

- Live: `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods/SpecializationP0`
- Receipt: `.../SpecializationDeploymentBackups/B081.108-6736fc5-playtest.json`，DEVELOP_ACTIVE。
- 旧B080完整包: `.../SpecializationDeploymentBackups/.temporary-develop-backup-vp7i_5qi`，digest `65bcf9271d282a7510174df810ca0453f1eea02be2dd512e79b4c04233ceedb5`，完整逐文件核验；不位于Mods内。
- 稳定恢复点在新receipt的stable_backup中；main B069.96 digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`，main HEAD `e3651f9b7c90110f3a8890a7b12ca299996b306b`未改。

诊断应显示`P0-B-081.108`。左键“科研基础设施”看摘要，右键看学院组成。一次科研城验证：ACTIVE IV专家0→1→2、方便时改变学院D、ACTIVE III→IV、保存重载；确认配置D/旧残留0及原生科技。原生总科技不只包含本项，不要求等于D×人数。旧III/其它百分比仍按原版本运行。

本地PASS不等于用户实机PASS；本批未完成用户验收，也不宣称55GB根因解决。回滚使用完整B080包和切换前独立存档，新保存不保证降级兼容。下一批不启动。
