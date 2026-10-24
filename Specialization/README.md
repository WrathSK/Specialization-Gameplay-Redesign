# Specialization：项目内部导航

本目录集中维护 **Specialization Gameplay Redesign**（《文明 VI》/ Harmony in Diversity 城市专业化与国内商路网络 Mod）的设计规范、技术架构、进度状态、验证记录与工作流约定。

- **设计版图与当前实施边界：** 完整设计体系涵盖共同规则、国内网络、**11 个主专业方向**（含配套联盟外交任务框架）及 **6 个辅助区域**。**当前 v0.1 阶段仅实施科研、文化、商业、工业四个核心专业**，以此建立系统架构、数值公式与机会成本的基准；其余已确立设计框架的未来主专业与待重构的辅助区域不扩大当前 v0.1 运行包的实施范围。设计文档冻结不等于当前运行包已全部实现。
- **按受众快速分流：**
  - **直接阅读玩法设计：** [Design 中文阅读导航](Design/README.md)（按共同规则、国内网络、v0.1 四专业、7 个未来主专业及 6 个辅助区域查阅）。
  - **面向实机测试玩家：** [稳定测试说明](Stable_Playtest.md)。
  - **面向开发与维护者：** [开发指南](Development_Guide.md)。
  - **面向 AI 会话 / 工程协作：** 先读[根 AGENTS](../AGENTS.md) 与[本目录 AGENTS](AGENTS.md)，再按 [W0001](Workflow/README.md) 进行任务定界（task-scoped）读取。玩法语义与取舍由用户最终决定，权限与角色边界集中在 [W0005](Workflow/README.md#w0005--authority-and-repository-knowledge)。

## 按问题查找资料

| 你想了解的问题 | 入口与阅读路径 | 说明与边界 |
|---|---|---|
| **游戏规则应当怎样运行？** | [Design 阅读导航](Design/README.md) · [Design Spec](Design/Specialization_v0.1_Design_Spec.md) → [Content 索引](Design/Content/README.md) | 人类读者建议从阅读导航进入；接受与取代追溯见 [Design ChangeLog](Design/Design_ChangeLog.md) |
| **系统在技术上如何组织与实现？** | [技术架构阅读入口](Architecture/README.md) → [架构总说明](Architecture/Specialization_v0.1_Architecture.md) | 导航系统分层、跨 context 传播、保存与呈现合同；AI 会话按任务范围读取 |
| **当前做到哪里、还缺什么、下一步允许做什么？** | [Status CURRENT 块](Status/Specialization_P0_Status.md#current-authoritative-state) · [Authority.json](Workflow/Authority.json) | 唯一当前状态与任务路由；历史计划或建议不等于实施授权 |
| **哪些结论已经过验证？适用范围是什么？** | [Validation Results](Status/Validation/Results/) · [历史 Closure 取回](Status/Validation/Results/Refactor_Closure_History.md) · [Playtest Backlog](Status/Playtest_Backlog.md) | 严格区分 `STATIC_CONFIRMED`、`LOCAL_SIMULATION_PASS` 与 `USER_GAME_TEST_PASS`，不跨场景外推 |
| **哪些底层限制与技术调查不应重复踩坑？** | [技术证据索引](Reports/Technical/README.md) | 按城市生命周期、商路桥接、内存性能、原生精度等问题检索反证与实测记录 |
| **非权威的审阅报告与专项调查在哪里？** | [Advisory 审阅区](Reports/Advisory/README.md) · [Investigation 调查区](Reports/Technical/Investigations/README.md) | 供用户决策参考的限定范围审阅与长期调研，不构成独立设计或实施权威 |
| **源码、本地测试与部署工具在哪里？** | [Mod 源码](../Mod/) · [本地测试](../DevelopmentTests/README.md) · [部署与诊断工具](../tools/README.md) | 实机替换与分支维护须遵循 [Playtest Workflow](Architecture/Playtest_Workflow.md) |
| **历史设计修订与早期文档快照在哪里？** | [Historical 索引](Historical/README.md) · [设计历史导航](Historical/Design/README.md) | 冻结历史仅用于溯源，不作为当前任务队列或现行指令加载 |

## 分支、运行包与版本账本原则

- `main` 保存最后明确批准推广（promote）的实机测试源码；`develop` 为独立工作树（worktree）中的持续开发源码。两分支共用相同的导航 README 结构，具体状态随所在分支的 `Status` 记录。
- 游戏目录下的外部 `SpecializationP0` 是部署副本，不能仅凭分支 `HEAD` 推断当前游戏加载的版本。
- 当前构建号、源码与运行包对应关系、待验状态统一由 [Status](Status/Specialization_P0_Status.md#current-authoritative-state)、[Authority.json](Workflow/Authority.json) 及部署凭据维护，本导航页不重复复制版本账本。

## 外部材料、截图投递与历史路径映射

- **新截图投递：** 请投递到 `develop` 根目录下的 `ScreenShots/`（整个目录由 Git 忽略，不进版本库）。逐张读取并明确批次后，归档至 `local/legacy-workspace/Specialization/Status/Validation/Evidence/<Batch>/`。
- **旧工作区迁移说明：** 原游戏支持目录下的旧 `Specialization` 资料已完整迁出，旧目录文档不再作为活动入口。如需按历史报告中的旧路径定位原件或截图证据，请查阅[旧工作区资料迁移与历史路径映射](Reports/Proposals/Legacy_Workspace_Relocation.md)（早期背景见 [Phase 1 外部材料记录](Reports/Proposals/Phase1_External_Materials.md)）。
- **外部运行环境文件：** 游戏数据库、运行日志、存档与部署备份仍保存在 Git 之外的原位置。新会话或上下文压缩后恢复时，直接使用上方表格入口按任务读取，无需加载旧交接全文。
