# 恢复记录与本地提交器集成

Document Owner: Codex
Design Reference: D0007 / ELIG / PROG
Architecture Reference: A0037
Scope: MOCK_ONLY / NO_ENGINE_ADAPTER

CityOperationGate新增可选recovery存储依赖及CommitRecordedMock。配置recovery的实例拒绝旧CommitMock入口，避免绕过记录。Prepare/提交复核先读存储；只允许明确READ_OK且record=nil。已有任何记录（包括损坏/未知schema）或读取失败均停实例，不读城市或写新记录。这里存储是受信MOCK依赖，READ_OK nil不证明真实旧档从未存在记录。

提交前复核通过后，以原事实与目标创建PENDING，最多一次保存；即使保存接口抛错也读回完整比较。未完整确认记录则不调用城市writer。确认后重新检查城市身份/原事实/运行许可，并再次核对记录未被替换，才调用一次mock城市writer。后续继续沿用此前读回/不确定性分支，不重试、不回滚。

目标同城匹配时返回TARGET_OBSERVED_PENDING，并停实例；未写、冲突、读回失败同样不开放后续操作。尚未实现完成标记或自动清记录，不能用于连续正常业务。已保存PENDING跨JSON/新Lua VM恢复后，新的Gate也拒绝开始新的计划。

LOCAL_SIMULATION_PASS表示本地模拟，不等于游戏通过。四组exit=0：test_recorded_city_commit.py、test_city_commit_readback.py、test_city_operation_gate.py、test_pending_city_recovery.py。覆盖记录保存后抛错、静默丢写、读回失败、记录冲突、保存回调撤销许可/改变城市、城市写前/写后抛错、已有记录/损坏记录/读取失败启动拒绝及新VM恢复。没有实际Property或配置写入。

## 边界

两份存储之间仍不具有已证明的引擎原子性或持久顺序。测试只证明所注入MOCK读写按协议执行；不能声称游戏崩溃后一定保留intent或数据。真实adapter必须把读/写边界与城市事件时序审计结合，防止最后复核后又改变身份/原事实。当前模型不提供引擎compare-and-swap。

PENDING记录还没有DONE/ABORT终态与安全恢复开放流程；读到目标值不自动清除记录，读到原值不自动重试。错误保留依赖PENDING已经成功存储；记录写入失败且无记录时，跨新实例无法仅凭nil证明前次失败，但本流程该路径未允许城市写入。历史迁移/外部写入损坏仍须独立处理。

下一步本地完成终态记录及加载判定，再决定小范围DEV接入，不先接专业收益。当前用户无需测试，B010延后，运行B018/25保持。

修改CityOperationGate.lua，新增test_recorded_city_commit.py及本报告/当前文档；既有其它Tests、Source和Design保持hash。备份：DevelopmentBackups/Specialization-before-recorded-city-commit。[Status](../../Status/Specialization_P0_Status.md)为唯一任务入口。未启动游戏。
