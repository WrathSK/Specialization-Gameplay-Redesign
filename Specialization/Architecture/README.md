# 技术架构阅读入口

先读[系统如何组成](Specialization_v0.1_Architecture.md#系统如何组成)，再按问题进入细节。这里导航技术职责；玩法请读[Design](../Design/README.md)，实际验收与当前允许动作只看[Status CURRENT](../Status/Specialization_P0_Status.md#current-authoritative-state)。

| 我想了解 | 阅读入口 | 文档角色 |
|---|---|---|
| 系统从哪里启动，各层怎样配合？ | [架构总说明](Specialization_v0.1_Architecture.md#系统如何组成) | 当前源码结构说明；明确尚未落地部分 |
| 城市身份、投资和保存怎样保持？ | [事实、保存与当前资格](Specialization_v0.1_Architecture.md#事实保存与当前资格)、[同构建存档支持范围](Specialization_v0.1_Architecture.md#accepted-convergence-boundaries--2026-11-04) | 当前职责与支持范围。早期切换证据见 [E2 历史记录](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing) |
| 商路如何跨UI/Gameplay传递，怎样避免旧数据回放？ | [网络与跨context](Specialization_v0.1_Architecture.md#网络与跨context数据)、[传播合同分组](v2/README.md#事件传播与网络基础合同) | 现行基础合同，不统一各专业收益公式 |
| 收益、隐藏载体与玩家机构如何分工？ | [收益与呈现](Specialization_v0.1_Architecture.md#收益应用与玩家呈现) | 当前consumer和展示原型，与未来目标分开 |
| 怎样追查状态归属、依赖和旧效果移交的原始依据？ | [早期状态与服务合同](v2/D0032_Adaptation.md)、[依赖与移交记录](v2/D0032_Implementation_Plan.md) | 按问题查原始合同。当前实现和后续安排分别查正式架构与 Status |
| 当前具体实施计划在哪里？ | [Authority所指manifest](../Workflow/Authority.json)、[Status](../Status/Specialization_P0_Status.md#current-authoritative-state) | 唯一当前任务路由，不由本页派发 |
| 为什么某条实现路线不能直接采用？ | [按问题找技术证据](../Reports/Technical/README.md) | 限制、反证、局部实测及历史方案 |
| 如何测试、部署或恢复？ | [测试导航](../../DevelopmentTests/README.md)、[Playtest合同](Playtest_Workflow.md)、[中途恢复](../Workflow/README.md#action-scoped-reading-and-interruption-recovery) | 工程操作与安全边界 |
| 过去的调查和方案？ | [v2分类索引](v2/README.md)、[冻结历史](../Historical/README.md) | 历史进度不再派工；有效技术依据仍保留 |

## 两套批次名称的区别

Architecture v2最初的 **Batch A/B/C1/D1/C2/D2** 处理事实发布、共享网络视图、请求生命周期和重复工作。后来的 **P0-A/B/C/D/E…** 是将冻结玩法逐步接入这些基础设施的实施批次。例如Batch D1是折扣传播优化，P0-D1是科研跨学科研究，不是同一阶段。

A0161等是架构合同修订，D编号是设计修订，B编号是实现检查点。阅读系统职责不必先记住这些编号；追溯证据时保留其原版本语境。后续P0切片可替换早期具体实现，不因此废弃仍适用的事件驱动、UNKNOWN、撤销和单writer合同。

本入口不增加Codex强制读取集合；仍按当前任务读取正式合同、直接源码与必要证据。
