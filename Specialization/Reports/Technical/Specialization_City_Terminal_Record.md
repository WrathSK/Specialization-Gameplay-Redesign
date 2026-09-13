# 城市提交完成记录与显式恢复

Document Owner: Codex
Design Reference: D0007 / PROG / ELIG
Architecture Reference: A0038
Scope: MOCK_ONLY / NOT_DEPLOYED

本轮修改PendingCityRecovery与CityOperationGate，新增test_city_terminal_record.py。新增DONE终态，但不删除记录：ClosePlan仅对同城目标值匹配的PENDING产生DONE计划；InspectDone仍验证schema/原目标身份及当前事实匹配。原Inspect继续只读保持暂停，不自动改变PENDING。

Gate.ResolveRecordedMock显式核对当前资格、同城目标值及未变化的原记录，写一次DONE并读回确认，随后再核对目标事实与许可，才清本实例暂停并开放下一笔。恢复不调用城市writer。写DONE后抛错但完整读回一致可确认；丢写、冲突、资格丢失或重入保持暂停。已是DONE也需重新对账，新实例不把DONE字面值直接当授权。成功恢复丢弃旧计划句柄，下一笔重新规划。

当前恢复存储限定单城市顺序通道：接受的DONE绑定cityUID/owner/完整目标，下一笔必须以该事实为原值，新PENDING替换上笔DONE；保留最后一笔凭据，不是全历史账本。拒绝紧邻同operationID，不承诺帝国级ID唯一或跨所有历史重放识别。后者仍依永久动作账本及未来ID分配。

LOCAL_SIMULATION_PASS表示本地模拟，不等于实机。五组最终通过：terminal_record、recorded_city_commit、city_commit_readback、city_operation_gate、pending_city_recovery。测试实际组合完成初始化→学院两笔，DONE丢写/写后报错、冲突暂停、恢复重入、JSON新VM读档前阻止计划、显式对账后正常继续。新旧记录不自动清除。

## 保留边界

未接Civ VI setter/事件，仍不保证两个Property的崩溃原子性或保存顺序。DONE只有与当前事实核对后才有意义；不能凭DONE清除其它城市/owner故障。读到PENDING原值、第三方值或缺失证据，不自动重试、回滚或写ABORT；这些分支保持待处理。未实现跨owner永久UID、旧档迁移和实际收益撤销。

该模型现在支持限定单城市连续完成与加载对账，可作为最小DEV验证的准备基础。下一步审查如何将记录和成果放入一个可验证存储结构，避免为了两个Property顺序给实机引入不必要风险，再准备DEV接入；不继续添加游戏收益。

运行保持B018/25，Design及其它源码未改，无新用户测试。备份/最终输出：DevelopmentBackups/Specialization-before-city-terminal-record。[Status](../../Status/Specialization_P0_Status.md)为唯一任务入口。未启动游戏。
