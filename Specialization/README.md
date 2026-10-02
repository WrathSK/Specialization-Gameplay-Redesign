# Specialization：main 配套知识导航

本页导航 **main 稳定源码所配套的资料**。本分支为 B069.96 / modinfo96 Playtest Baseline，配套Design为D0025；不是最新开发设计，也不是完整v0.1发布。基线身份由本分支Status、部署合同和源码共同确认，不能用来推断外部游戏当前运行包。

## 阅读本分支资料

| 问题 | main 内的配套入口 |
|---|---|
| 本基线的游戏规则是什么？ | [Accepted Design Spec](Design/Specialization_v0.1_Design_Spec.md)、[接受与修订记录](Design/Design_ChangeLog.md) |
| 本基线技术上如何构成？ | [Architecture](Architecture/Specialization_v0.1_Architecture.md) |
| 本基线有哪些验证与未解决问题？ | [Status](Status/Specialization_P0_Status.md)、[长局问题清单](Status/Playtest_Backlog.md)、[验证结果](Status/Validation/Results/) |
| 调查依据在哪里？ | [技术索引](Reports/Technical/README.md)；报告中的“当前/下一步”须按其版本语境阅读 |
| 如何维护、测试和部署？ | [根AGENTS](../AGENTS.md)、[项目约定](AGENTS.md)、[测试说明](../DevelopmentTests/README.md)、[部署与Git合同](Architecture/Playtest_Workflow.md)、[部署工具](../tools/README.md) |
| 源码与外部证据在哪里？ | [Mod](../Mod/)是本分支源码；[当前原图归档与历史路径映射](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Proposals/Legacy_Workspace_Relocation.md)定位已迁出的证据；[Phase 1记录](Reports/Proposals/Phase1_External_Materials.md)保留当时的材料边界 |

本分支内的架构调查、旧交接与Historical用于追溯，不派发develop下一任务，不把局部本地/实机证据扩大为整个系统通过。用户是最终设计权威；Codex按授权维护文件，技术限制不能成为自行改玩法的理由。

## 阅读最新设计与开发进度

普通开发在独立的 [develop 分支](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop)。最新资料请直接使用以下跨分支链接：

- [Design 中文阅读导航](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/README.md)
- [Architecture 技术阅读入口](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Architecture/README.md)
- [当前 Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md)
- [技术证据索引](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/README.md)

这些页面不替换本分支源码的配套设计，也不表示新设计已经在main落地。main/develop保持隔离；文档更新和正常commit/push不构成promotion、合并或部署授权。

## 外部运行包边界

外部游戏SpecializationP0仅为部署副本，机器路径见忽略的 `local/config.json`。临时develop测试可能使运行包不同于main；实际状态以既有部署记录/receipt和必要核验为准。本页不声称已检查当前运行包。

保持稳定分支、明确授权、目标校验、安全替换和恢复边界；不编辑外部运行包或无关Mod，不自动启动游戏，不删除历史证据或备份。
