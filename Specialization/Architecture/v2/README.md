# Architecture v2 — current D0032 adaptation / historical AV2-I001


开发导航：[Workflow W0001](../../Workflow/README.md) → [Authority](../../Workflow/Authority.json) → batch manifest。只改变context加载，不改变Architecture合同；当前A0161状态优先于后面的历史标题。

## 当前实现：P0-A / A0161

[P0-A区域完善度与科研影子](P0_A_District_Completeness.md)：B077.104/modinfo104，LOCAL_SIMULATION_PASS，原生接口/事件及诊断显示尚待用户实机。无新收益/新carrier/旧writer退出，未部署；live B076.103、main B069.96保持。用户授权的首批已完成，不自动推进下一批。

## 目标架构入口：A0160 / D0032

D0032是玩法权威；本目录新增目标合同不代表已实现。Runtime仍B076.103，A/B/C1/D1/C2/D2保留，E未实施。

1. [D0032目标架构与状态合同](D0032_Adaptation.md)
2. [Runtime考古和旧效果退出矩阵](D0032_Runtime_Archaeology.md)
3. [实施依赖、P0批次与迁移](D0032_Implementation_Plan.md)
4. [技术spike](D0032_Technical_Spikes.md)
5. [全源码索引/hash](D0032_Runtime_Inventory.json)、[文档验证](D0032_Validation.md)

**GATE B — READY FOR P0-A**；第一批只建议Shared区域完善度影子纵切，待用户授权。没有runtime改动/部署。A–D2报告是已完成的性能合同；PAC的累计presentation-only原则有效，但旧能力候选需以D0032映射为准。以下AV2-I001与旧地图是B069历史证据，不是当前源码逐项现状。

## Historical AV2-I001 header and investigation

Document Owner: Codex
State: Investigation complete / awaiting user review; NO REFACTOR
Source commit: `e3651f9b7c90110f3a8890a7b12ca299996b306b`
Source/runtime: B069.96 / modinfo96
Accepted Design: D0025 (unchanged)
Evidence: STATIC_CONFIRMED — 当前代码/SQL注册和调用链的静态证据，不等于事件实际频率、内存泄漏或游戏内故障已获证实。

## 当前实施增量

[Presentation / Institution / Ability / Carrier — PAC-I001](Presentation_Institution_Carrier_Model.md)：用户确认分层及PAC-R0002永久Potential累计机构、阶段能力归属、presentation-only路线；现有载体与Tooltip调查已完成，具体UI接入待审阅。独立于A–D2完成状态，不是BatchE或新玩法实施。[完整ID分类](Presentation_Carrier_Inventory.json)。

当前主线：**A✅ → B✅ → C1✅ → D1✅ → C2✅ → D2✅ → E（未开始）**。B076.103已临时部署；[短时实机验证](../../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)支持`av2-runtime-b076.103` Runtime milestone，仅限已测idle改善，保留ACK未完成/长局内存未知。不是stable promotion。以下AV2-I001是历史调查。


B072.99独立instrumentation：[Runtime Audit](../../Reports/Technical/Specialization_B072_Runtime_Audit.md)，本地通过、原生文件能力待验证，不是Batch C/D。[Yield Precision Contract待办](Yield_Precision_Backlog.md)只记录、不实施。


[Batch A版本/发布合同](Batch_A_Input_Contract.md)已在develop B070.97实现并本地验证；下文AV2-I001仍是B069.96源代码调查快照。Batch A已获用户接受；[Batch B共享视图](Batch_B_Shared_Network.md)在develop B071.98本地验证完成，C已拆分且C1及本轮限定Copy/Industry的C2本地完成，D1已接受，D2本地完成且短时idle实机通过（范围见上），E尚未实施，stable不变。

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
