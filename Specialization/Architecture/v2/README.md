# Architecture v2 — current D0032 adaptation / historical AV2-I001

入口职责：Architecture记录技术合同；Gameplay意义由用户接受的Design决定，见[W0005](../../Workflow/README.md#w0005--authority-and-repository-knowledge)。当前进度与授权边界以[Status CURRENT块](../../Status/Specialization_P0_Status.md)及[Authority](../../Workflow/Authority.json)为准。下方按时间累积的旧“当前/待授权”标题只保留当时证据，不覆盖最新状态。A0161目标合同及后续批次变更按任务读取，不要求重读全部历史。

当前实施：[B108新局多城authority](P0_E2_Plan.md#b108135-implementation-result--evidence-boundary)本地通过、实机待验；新测试局，三城＋一次冷加载。旧writer/迁移退出，无Claim/F。

历史计划：[B107后E2收束](P0_E2_Plan.md#post-b107--remaining-e2-plan--new-path-isolation-over-migration-compatibility)。优先新局多城统一保存/旧writer退出；旧新混合实机兼容不再为必做门禁。待授权，runtime仍B107。

已验证进度：[P0-E2 B107.134正面建城登记](P0_E2_Plan.md#b107134--authorized-positive-founding-registration-implementation)简化新局单城路径实机通过：P0自动登记、科研P1及用户确认重启后P2保留；旧新混合对照延后，P0单独冷加载未确认。E2仍partial，无Claim/F。

历史进度：[P0-E1只读身份核对B088.115](P0_E1_Identity_Evidence.md)本地完成；原生观察发现分城转自由城后City记录缺失，正确UNKNOWN；永久连续性门禁保留，不进入E2/F。U1技术用户PASS，最终排版后置。

历史进度：[U1科研展示原型B087.114](U1_Presentation_Prototype.md)本地通过，待实际显示确认；非完整U1，不继续下一批。

历史计划：U1已收窄为[前置展示原型计划](P0_U1_Plan.md)，仅验证机构/能力文字/carrier隐藏的技术与显示；非完整实施，等待授权。

此前计划：P0-D3用户整体PASS；[P0-U1提前计划](P0_U1_Plan.md)已备，当前机构/技术carrier隐藏先行，历史机构保留依赖。未授权实施，无部署。

历史进度：P0-D3 B086.113 [学术主持实现](P0_D3_Research_Chair.md)完成静态/本地验证，真实逐建筑收益待用户验收；D2用户PASS。Design不改，不启动下一批。下方旧进度为历史。

Current P0-D1: [B084.111 formal cross-disciplinary implementation](P0_D1_Research_Cross_Cutover.md), user-authorized temporary floor, LOCAL_SIMULATION_PASS / formal USER_GAME_TEST_REQUIRED. This supersedes earlier primitive gate status; Design D0035 unchanged; P0-D2 not started.



开发导航：[Workflow W0001](../../Workflow/README.md) → [Authority](../../Workflow/Authority.json) → batch manifest。只改变context加载，不改变Architecture合同；当前A0161状态优先于后面的历史标题。

## 当前工作：P0-D1已授权，原生精度门禁未关闭

[门禁证据](P0_D1_Primitive_Gate.md)：离线候选通过不等于引擎/正式实现通过；旧writer完整保留，B081不变。下段是计划阶段历史。

[计划](P0_D1_Plan.md)：跨学科研究BASE×0.5及旧科研人口效果精确退出。无源码修改/部署，无当前用户测试。

### P0-C已验收

[实施/cutover与本地证据](P0_C_Research_Infrastructure.md)：四bit专家Science、旧48精确退出、摘要/详情按需；用户单学院澄清解除旧门禁。无下一批实施。

### Historical preflight

[门禁记录](P0_C_Primitive_Gate.md)：本地D×专家/SQL候选通过；多学院原生覆盖待确认。未修改Mod、未cutover、未部署；P0-C不标PASS。诊断后续遵守简明结果、按需详情合同。

## 当前已完成实现：P0-B2 / A0161

[P0-B2 Lv2资格](P0_B2_Lv2_Qualification.md)：B080.107/modinfo107，LOCAL_SIMULATION_PASS + 用户报告实机PASS；住房按不同Tier存在性、原生2 base GPP路径保留，UNKNOWN不再清空。P0-B1用户PASS含工业；P0-A D/专家读取PASS，掠夺未测。当前Design D0035仅四专业范围，Military未来；A0161合同未改变。[P0-C具体计划](P0_C_Plan.md)已备并获实施授权，见上方门禁；E未开始，部署以Status为准。

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

Current P0-D1 technical gate: [B082 district precision probe](P0_D1_District_Precision_Probe.md), opt-in only, not formal cutover. User requires district yield attribution; fallback quantum0.5/1 does not change50% conversion. Native validation pending.
