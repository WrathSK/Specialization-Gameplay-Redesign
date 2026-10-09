# 系统合同、实施切片与技术调查

首次阅读请从[技术入口](../README.md)或[系统组成](../Specialization_v0.1_Architecture.md#系统如何组成)开始。此页按职责检索，不派发下一工程任务。实际进度与授权只见[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)及[Authority](../../Workflow/Authority.json)。

最初Architecture v2的Batch A–D2是传播/性能基础改造；后续P0批次是在该基础上适配冻结玩法。例如Batch D1优化折扣传播，P0-D1实现科研跨学科研究。旧进度历史化不等于合同废止；不需要按编号顺序读完本目录。

## 当前切片与目标合同

| 问题 | 资料 | 角色与边界 |
|---|---|---|
| 当前保存切片、授权、最小验收 | [E2当前路由](P0_E2_Plan.md#current-slice--recovery-and-action-routing) | 当前实施合同与结果；建议不等于新授权 |
| 科研传统如何开始保存与计龄 | [P0-F计划](P0_F_Research_Tradition.md) | F1年龄/影子、F2实际收益；计划待授权，跨Owner与旧P4起点不猜测 |
| Identity/Potential/ACTIVE、永久成果及Shared服务应如何分层 | [状态/服务目标](D0032_Adaptation.md) | 目标合同，结合后续切片；其中规划时版本/下一步不是今天的任务 |
| 依赖顺序、单writer切换、存档支持 | [实施计划](D0032_Implementation_Plan.md) | 批次依赖和迁移合同，完成状态查Status |
| 哪些接口还需要原型/实机 | [技术spike登记](D0032_Technical_Spikes.md) | 技术未知不授权简化Design；具体已关闭项查后续切片 |
| 哪些旧效果需要退出 | [原始考古矩阵](D0032_Runtime_Archaeology.md)、[切换责任](D0032_Implementation_Plan.md#明确的旧效果切换责任) | 考古是B076时点，不能作为当前逐模块清单 |

## 事件传播与网络基础合同

| 责任 | 现行基础合同 | 使用边界 |
|---|---|---|
| 输入版本、变化发布、有效性 | [Batch A](Batch_A_Input_Contract.md) | 事实变化才发布；不是完整持久状态方案 |
| 共享网络视图、重复读取 | [Batch B](Batch_B_Shared_Network.md) | 共享计算基础，各专业payload独立 |
| 折扣请求/样本/ACK/撤销 | [Batch C1](Batch_C1_Discount_Lifecycle.md) | 延迟样本与确认失效分开 |
| 折扣扫描与dirty传播 | [Batch D1](Batch_D1_Discount_Propagation.md) | 无关事件不触发昂贵工作 |
| Copy/Industry请求生命周期 | [Batch C2](Batch_C2_Copy_Industry_Lifecycle.md) | 引用/epoch、single-flight、确认退出 |
| 其它通知、读取与idle工作 | [Batch D2](Batch_D2_Runtime_Propagation.md) | RuntimeWork及事件驱动；历史压力结果不是每批默认验证要求 |

合同中的实现版本和当时部署/待测文字只描述原检查点。后续修改沿当前切片审阅；[性能milestone结果](../../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)仅证明所测idle行为，不关闭长局内存未知。

## 共享事实与收益应用

- [巨作事实层P0-K计划](P0_K_Great_Work_Facts.md)：已支持作品/历史时代/城市馆藏与国内索引；事实层已获授权实施，不包含新文化收益；实际证据/待验范围看Status。

- [P0-A实际事实与shadow](P0_A_District_Completeness.md)：普通建筑目录、深度、只读专业事实；[读取修复](P0_A_Native_Read_Fix_B078.md)。目录覆盖不能由部分对象PASS外推。
- [基础专家支持](P0_B1_Specialist_Support.md)、[二级资格/住房/GPP](P0_B2_Lv2_Qualification.md)：各自consumer和精确旧writer退出边界。

## 收益应用与精度

- [商业模块准备](Commerce_Preparation.md)：O商路只读、P商业化、Q资本、R发展、S信誉、T重组；区分当前D0045合同、旧writer和窄未决项。
- [工业模块准备](Industry_Preparation.md)：G奇观历史、H标准化、I工程、J队伍；纠正每模板holder、N/E/L、III/IV成本与固定注入。两份仅调查/计划，不派发实施、不替代B165待验，不加入日常全量context。

- [文化后续模块准备入口](Culture_Preparation.md)：L2意义延展、L3巨作启迪、M时代对话、N1–3人文考察/见闻/Network及U2馆藏展示的计划与只读调查。现行Culture D0049：L2自动能力已验，L3百分比自动路径本地完成、原生待验；M/N/U2仍逐批审核/授权，不加入日常全量context。
- [人文考察团UI计划](P0_N_Expedition_UI.md)：训练、独立管理、目标／任务、失效后重挂靠、城市见闻及Network呈现；仅提案，借UI不等于复用Spy引擎。

- [文化风雅熏陶L1已测结算](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md)：所测逐栋加值与结算已通过；[原始实施检查点](P0_L1_Aesthetic.md#b148175--implementation-checkpoint)保留技术依据，当前任务/下一授权仍看Status。
- [科研基础设施正式cutover](P0_C_Research_Infrastructure.md)、[此前计划](P0_C_Plan.md)、[原生门禁](P0_C_Primitive_Gate.md)：计划/门禁是来源，不重新派发旧测试。
- [跨学科研究正式路径](P0_D1_Research_Cross_Cutover.md)：后续已接受floor实现；[原计划](P0_D1_Plan.md)、[早期门禁](P0_D1_Primitive_Gate.md)、[区域精度实验](P0_D1_District_Precision_Probe.md)保留反证与测试路径。
- [学以致用](P0_D2_Research_Apply.md)：每专家floor；[学术主持](P0_D3_Research_Chair.md)：逐普通建筑consumer。
- [精度待办](Yield_Precision_Backlog.md)：尚需研究/未批准的后续事项，不自动成为本轮实施任务。

## 呈现与跨context界面

- [Institution / Ability / Carrier合同](Presentation_Institution_Carrier_Model.md)、[载体分类调查](Presentation_Carrier_Inventory.json)：分层、累计presentation-only原则继续适用；旧命名/能力候选由当前Content决定。
- [前置U1原型计划](P0_U1_Plan.md)、[科研显示原型](U1_Presentation_Prototype.md)：只覆盖指定surface和技术验证，不等于完整U1或所有专业UI。
- [身份观察入口](P0_E1_Identity_Evidence.md)保留早期实际证据；当前保存/所有权接管以E2路由为准，不按E1旧待测描述恢复任务。

## 历史调查与审计来源

以下保留在原路径：它们是审阅provenance和历史结构，不是当前源码地图。

- AV2-I001 / B069： [状态归属](State_Ownership_Save.md)、[桥接依赖](Dependencies_Bridges.md)、[事件传播](Events_Dirty.md)、[当时发现与批次](Findings_Batches.md)、[事件目录](Event_Catalog.tsv)、[源码索引](Source_Index.md)。原调查基线`e3651f9`，STATIC_CONFIRMED；不是事件真实频率或泄漏证明。
- D0032适配时点：[源码/hash快照](D0032_Runtime_Inventory.json)、[文档验证](D0032_Validation.md)。实际当前review provenance仍由[Runtime_Index](../../Workflow/Runtime_Index.json)维护。
- [早期Architecture v2调查计划](../Architecture_v2_Plan.md)：旧派工已被后续合同/当前切片取代；不重新执行其中的“下一步”。
- [运行观测instrumentation调查](../../Reports/Technical/Specialization_B072_Runtime_Audit.md)：独立于玩法完成度；原生I/O能力不因本地模拟通过而自动确认。

源码注册不证明原生API必定存在或事件顺序稳定；技术调查、目标合同、本地模拟、用户实测分开使用。按[W0001](../../Workflow/README.md)只读任务相关部分，本索引不扩大强制读取集合。
