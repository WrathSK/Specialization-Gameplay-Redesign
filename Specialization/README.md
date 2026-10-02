# Specialization：项目导航

Civ VI / Harmony in Diversity城市专业化与国内商路网络Mod。当前v0.1只实施科研、文化、商业、工业；其它专业的Design不扩大实施范围。Design冻结不等于当前运行包已实现。

直接阅读玩法：[Design中文阅读导航](Design/README.md)，按共同规则、专业及未来区域查阅。

## 从哪里开始

先读[根AGENTS](../AGENTS.md)与[本目录约定](AGENTS.md)，再按[W0001](Workflow/README.md)进行task-scoped读取。Gameplay Design由用户最终决定；权限与决策边界集中在[W0005](Workflow/README.md#w0005--authority-and-repository-knowledge)。

| 要回答的问题 | 权威入口 |
|---|---|
| 游戏应当怎样运行？ | [Design Spec](Design/Specialization_v0.1_Design_Spec.md) → [各专业/Shared内容索引](Design/Content/README.md)；接受与修订见[ChangeLog](Design/Design_ChangeLog.md) |
| 技术上如何实现？ | [技术阅读入口](Architecture/README.md) → 系统说明、合同与相关证据；Codex仍按当前任务读取 |
| 当前做到哪里、还缺什么、下一步允许什么？ | [Status CURRENT块](Status/Specialization_P0_Status.md)与[Authority所指manifest](Workflow/Authority.json)；计划建议不等于授权 |
| 哪些结论已被证明？ | Status引用的[Validation Results](Status/Validation/Results/)；STATIC / LOCAL / USER_GAME_TEST分别保留范围 |
| 哪些调查不应重复？ | [技术索引](Reports/Technical/README.md)及当前计划引用的技术约束；只读与本任务有关的报告 |
| 源码、测试、部署在哪里？ | [Mod](../Mod/)、[测试](../DevelopmentTests/README.md)、[部署工具](../tools/README.md)、[Playtest Workflow](Architecture/Playtest_Workflow.md) |

main为最后明确promote的可信源码；develop为独立worktree中的当前开发源码。外部SpecializationP0是部署副本。当前build、live/stable关系、待验状态只查Status/Authority，本文不复制版本账本。

新截图请投递到develop根目录`ScreenShots/`（整个目录不进Git）。阅读后归档到`local/legacy-workspace/Specialization/Status/Validation/Evidence/<Batch>/`；旧游戏目录Specialization已完整迁出，旧文档不再作为当前入口。

[当前归档位置与历史路径映射](Reports/Proposals/Legacy_Workspace_Relocation.md)说明旧路径如何定位原件。[Phase 1外部材料记录](Reports/Proposals/Phase1_External_Materials.md)保留迁移时的历史事实；其旧收件箱/证据位置不再是活动路径。其它日志、备份、DB仍在原位置。历史报告用于追溯，不重新派发任务。新任务/压缩后恢复使用以上入口，不要求读取旧交接全文。
