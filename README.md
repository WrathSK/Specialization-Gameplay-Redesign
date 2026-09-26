# Specialization Gameplay Redesign

Civilization VI / Harmony in Diversity 的城市专业化与国内商路网络 Mod。v0.1 围绕科研、文化、商业、工业四个专业开发；设计接受、代码实现、稳定推广和实机验证是不同阶段。

## main：稳定源码与配套资料

本分支保存用户指定的 **B069.96 / modinfo96 Playtest Baseline**，配套设计为 D0025。这是开发中的稳定游玩基线，不是完整 v0.1 发布或全部机制/性能已经验证的承诺。基线依据见本分支 [Status](Specialization/Status/Specialization_P0_Status.md)、[Playtest 合同](Specialization/Architecture/Playtest_Workflow.md)和 [modinfo](Mod/SpecializationP0.modinfo)。

- [本分支知识导航](Specialization/README.md)：与 main 源码配套的设计、架构和证据。
- [源码](Mod/)、[测试说明](DevelopmentTests/README.md)、[部署工具说明](tools/README.md)。旧测试与报告保留各自版本范围，不作为 develop 的当前测试队列。
- 工程维护从[根 AGENTS](AGENTS.md)及[项目约定](Specialization/AGENTS.md)开始。main 保持稳定保护，普通开发在独立 develop worktree；修改、合并与部署分别遵守既有授权边界。

## 最新设计与开发资料：develop

下面链接明确指向 **develop**，其设计和技术资料可能超前于本分支实现，不应视为 main 已具备的功能。

| 想阅读的内容 | develop 入口 |
|---|---|
| 开发分支 | [develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop) |
| 中文设计阅读版 | [Design 导航](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/README.md) |
| 技术组成与合同 | [Architecture 导航](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Architecture/README.md) |
| 当前进度、验证与下一授权边界 | [Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md) |
| 技术依据与重要反证 | [技术索引](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/README.md) |

## 源码与游戏运行包

仓库 `Mod/` 是对应分支的源码；外部 Civilization VI `Mods/SpecializationP0` 是部署副本。**main HEAD 不代表游戏当前正在使用的包**：获授权的临时 develop 测试可能使运行包与 main 不同。实际包状态须核对既有部署记录、receipt及必要的文件一致性，不能从分支或 push 推断。

提交、push、README维护均不部署、不自动promotion。稳定更新及临时测试切换各自需要适用的授权与恢复保护；不得绕过现有部署工具，不由代理启动游戏。

玩法决定由用户最终确认；Codex承担获授权的工程和文件维护。机器路径通过[配置示例](local.config.example.json)写入忽略的 `local/config.json`；凭据不入库。[截图、存档、备份等外部材料](Specialization/Reports/Proposals/Phase1_External_Materials.md)不因Git存在而被替代。
