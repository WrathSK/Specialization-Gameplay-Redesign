# Architecture v2 第一轮调查 — AV2-I001

Document Owner: Codex
State: Investigation complete / awaiting user review; NO REFACTOR
Source commit: `e3651f9b7c90110f3a8890a7b12ca299996b306b`
Source/runtime: B069.96 / modinfo96
Accepted Design: D0025 (unchanged)
Evidence: STATIC_CONFIRMED — 当前代码/SQL注册和调用链的静态证据，不等于事件实际频率、内存泄漏或游戏内故障已获证实。

## 当前实施增量

当前主线：**A✅ → B✅ → C1✅ → D1✅ → C2✅ → D2 → E**。[D2 B076.103](Batch_D2_Runtime_Propagation.md)本地完成、未部署、待审阅。建议Runtime Milestone Candidate；E后置，建议先用户授权临时部署长测。以下AV2-I001为历史调查，不把旧未实施描述当当前状态。


B072.99独立instrumentation：[Runtime Audit](../../Reports/Technical/Specialization_B072_Runtime_Audit.md)，本地通过、原生文件能力待验证，不是Batch C/D。[Yield Precision Contract待办](Yield_Precision_Backlog.md)只记录、不实施。


[Batch A版本/发布合同](Batch_A_Input_Contract.md)已在develop B070.97实现并本地验证；下文AV2-I001仍是B069.96源代码调查快照。Batch A已获用户接受；[Batch B共享视图](Batch_B_Shared_Network.md)在develop B071.98本地验证完成，C已拆分且C1及本轮限定Copy/Industry的C2本地完成，D1已接受，D2本地完成等待审阅，E尚未实施，stable不变。

## 阅读顺序 / 范围

1. [状态归属与保存合同](State_Ownership_Save.md)
2. [运行依赖与跨Context桥接](Dependencies_Bridges.md)
3. [事件、失效传播与模块评级](Events_Dirty.md)
4. [建议重构批次与结论](Findings_Batches.md)
5. [逐事件目录](Event_Catalog.tsv)、[源码注册/Property原文索引](Source_Index.md)

只调查计划1–3。完整carrier清单、外部Mod兼容地图、缓存架构实现、性能修复、UI改动均未开展。相关依赖只记录引用。所有CURRENT来自Mod源码，不从旧DEV注释推断运行状态。TARGET仅是待批准建议。

## 覆盖与可信边界

Gameplay.lua中的Start顺序、modinfo的AddGameplayScripts/AddUserInterfaces/ReplaceUIScript是运行入口判据；ImportFiles不是启动判据。代码存在的Events注册在游戏API可用时才会成功；本报告不能证明所有条件事件均存在或触发顺序跨版本稳定。逐事件目录展开源码循环，分类按本模块消费者而非事件名字，DIAGNOSTIC不等于零成本。界面帧回调的真实调度频率仍由Civ VI决定。

永久成果、引擎事实、重建样本、收益投影、测试开关分开。Property和Building仅说明存放介质，不能说明权威等级。没有把已批准的后台UI当前商路来源降级为不可靠历史日志，也没有假造纯Gameplay全集API。

main与外部运行包只读；没有新增实机要求。完成后develop单独commit/push，不promotion，不自动打tag。建议报告为 **Architecture v2 Investigation Milestone Candidate**，不是重构完成里程碑。
