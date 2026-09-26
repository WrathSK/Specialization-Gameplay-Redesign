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

旧截图、日志、备份和大体积证据继续保存在外部工作区，路径见[外部材料说明](Reports/Proposals/Phase1_External_Materials.md)与忽略的`local/config.json`。历史报告用于追溯，不重新派发任务。新任务/压缩后恢复也使用以上入口，不要求读取某个聊天记录或旧交接全文。
