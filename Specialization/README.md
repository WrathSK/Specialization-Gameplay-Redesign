# Specialization：唯一协作入口

Document Owner: Codex
Design Authority: User
Handoff State: READY_WITH_NOTED_GAPS

这是Civ VI / Harmony in Diversity四专业城市成长与商路网络Mod的开发目录。当前是可用Cheat Panel验证机制的测试版，尚非完整v0.1。不要从老文件中的“probe/DEV/只读”字样推断所有模块仍无实际收益。

## 新代理阅读顺序

1. [AGENTS](AGENTS.md)：写入权限、禁止启动游戏、证据等级、截图与交付约定。
2. [Accepted Design Spec](Design/Specialization_v0.1_Design_Spec.md)及[ChangeLog](Design/Design_ChangeLog.md)：当前D0025；只在用户明确决定后改规则。
3. [Status](Status/Specialization_P0_Status.md)：唯一当前验证矩阵、待办和最小用户测试。
4. [Architecture](Architecture/Specialization_v0.1_Architecture.md)：当前运行模块和边界。
5. [技术索引](Reports/Technical/README.md)与[测试运行说明](../DevelopmentTests/README.md)：按待办读相关报告，不重做已解决调查。
6. [交接审计](Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md)：本轮差异、剩余外部依赖与校验。

## 路径与版本

- 仓库根R是本目录的父目录；[唯一源码](../Mod/)为`R/Mod/`。
- 外部游戏SpecializationP0仅为部署副本；机器路径见忽略的`R/local/config.json`。
- 运行版本以Status为准；当前P0-B-069.96 / modinfo96；B061隔离保留，B062从B060.85 checkpoint独立重做商业四，UUID不变。
- [Tests](../DevelopmentTests/)已迁入；七个必要基准位于Fixtures。其余历史测试适用性见测试README。
- 旧Backups、截图投递、PNG证据、DB、日志仍在外部旧工作区；[路径与证据说明](Reports/Proposals/Phase1_External_Materials.md)。
- Phase 1/2已获用户批准完成，GitHub initial baseline已建立；后续完整批次默认commit并push对应分支；具体约束见根AGENTS。

## 权威边界

玩法意图：Accepted Spec > Architecture > Status > 历史材料。运行现状及任务顺序以Status为准，Spec内旧“本轮不开发”等发布背景不构成永久暂停。当前D0025标题/ChangeLog/hash与具名Rule ID优先于Spec尾段残留的旧版本叙述；D0017记录本轮明确批准的小数处理，不推断GW未决曲线。

v0.1仅Research/Culture/Industry/Commerce、共同成长、网络、Crew与相关跨系统机制。其它专业/辅助区仍Future；科研IV读取其它区域产出不等于实现其专业化能力。

旧入口/阶段叙述已归档：[此前README](Historical/DocumentSnapshots/README_before_fresh_agent_handoff.md)。历史只提供证据，不派发下一任务。不要在不同文档复制一整套数值表。

## 当前稳定游玩 / 开发入口

B069.96 / modinfo96为v0.1 Playtest Baseline，不是final release。main保持当前长局；普通开发在同级`Specialization-Gameplay-Redesign-develop` worktree的develop进行。

- [部署与Git合同](Architecture/Playtest_Workflow.md)
- [长局问题清单](Status/Playtest_Backlog.md)
- [Architecture v2调查计划](Architecture/Architecture_v2_Plan.md)

运行包不会因普通开发自动更新。当前玩法、Design与存档合同不变。
