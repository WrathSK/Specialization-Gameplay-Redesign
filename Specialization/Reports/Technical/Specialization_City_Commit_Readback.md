# 城市计划提交与读回：本地失败边界

Document Owner: Codex
Design Reference: D0007 / ELIG / PROG
Architecture Reference: A0035
Scope: MOCK_ONLY / NO_CIV_SETTER

## 结果

CityOperationGate新增CommitMock，将私有计划消费/提交前复核紧邻一次注入的mock writer，再重新解析身份并读回事实。未注册运行包或调用任何Civ VI setter。LOCAL_SIMULATION_PASS仅本地模拟通过，不等于实机。

两组测试通过：test_city_commit_readback.py的11种场景，以及test_city_operation_gate.py原组合回归。过程输出及保护hash见DevelopmentBackups/Specialization-before-city-commit-readback/verification_result.json。

| 观察 | 返回/行为 |
|---|---|
| 提交前无许可、城市/原事实不符、旧句柄 | REJECTED_BEFORE_WRITE，不调用writer |
| 一次writer后，同城读回完整目标值、许可仍有效 | COMMITTED_MOCK；即使writer抛错也按读回认定目标值存在 |
| 同城目标值可见，但许可已撤销或发生重入 | TARGET_OBSERVED_HALTED；保留写入成果，停止后续提交 |
| 同城读回旧值 | OLD_VALUE_OBSERVED_HALTED；不证明历史上绝无短暂写入，不自动重试 |
| 同城读回第三种内容 | CONFLICT_OBSERVED_HALTED；不覆盖其它写入者、不回滚 |
| writer尝试后，读回失败/身份变化 | WRITE_OUTCOME_UNKNOWN_HALTED；不把异常当成未写入 |

所有提交尝试最多调用一次writer，句柄不能重用。writer和后续读回期间重入会停当前Gate实例；读回用于对账，不发收益，因此资格失效后仍允许尝试读取，但必须确认同城及owner证据。重新Refresh资格不能清除此Gate的halted状态。

## 检查覆盖

正常写入、先写再抛错、写前抛错、无写静默返回、读回报错、owner变化、许可撤销、回调重入、第三方内容冲突、提交前事实变更、提交前许可撤销。每案核对writer次数及二次调用不写；不确定结果停后续计划，成功结果保留原目标，旧事实不做回滚。

## 未解决的引擎边界

结果COMMITTED_MOCK仅表示本地同城读回与目标完全一致，不保证跨存档持久化、数据库原子性、城市永久UID或真实事件顺序。没有消耗Settler或修改任何正式收益。

resolve/write都是受信MOCK依赖。最后检查与实际引擎写入之间的引擎事件时序尚未验证，不能宣称本模型提供引擎compare-and-swap。读取失败后的停止状态只在当前Gate实例内存中，创建新实例/读档不会自动继承；未来须有持久错误/恢复协议，不能因为本地停止而宣称崩溃安全。

历史B015的持久GAP仅有原记录范围的证据，本轮没有把它接到新计划schema，也没有默认它足以处理所有不确定写入。新模块不支持正式迁移或跨owner转移。

## 下一步

先设计并本地验证未确认提交的恢复记录，使重载不会把不确定写入忘掉；明确何时只读核对、何时拒绝继续。随后再选择最小DEV运行接入。当前没有新用户测试或游戏PASS，运行保持B018/25，Design不变。

当前任务/验证入口：[Status](../../Status/Specialization_P0_Status.md)。
