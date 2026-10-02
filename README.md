# Specialization Gameplay Redesign

[English](#english) · [中文](#中文)

## English

### What is this project?

**Specialization Gameplay Redesign** is an unofficial gameplay mod in development for **Sid Meier’s Civilization VI with Harmony in Diversity (HD)**. It aims to give cities distinct, lasting roles and make choices about local investment and domestic trade routes matter across an empire.

### Design and scope

The v0.1 design centres on four specializations:

- **Research:** scientific specialists, research infrastructure and academic knowledge.
- **Culture:** collections, interpretation and cultural exchange.
- **Industry:** construction experience, building templates and engineering capabilities.
- **Commerce:** discovering commercial value and allocating capital across time and cities.

City districts and specialist jobs shape local development, while domestic trade networks connect cities through qualified sources, trade centres and recipients. The shared progression system separates permanent investment from the abilities a city can currently activate.

### My role and AI-assisted development

I am **Xuting Zheng**. I lead gameplay design, define requirements and development priorities, and conduct in-game testing. I make decisions about mechanics and trade-offs, report observed behaviour, and determine whether tested results meet the intended rules.

**Codex handles code implementation, technical investigation, repository maintenance and local checks under my direction.** My focus is on translating design intent into clear requirements and evaluating how the resulting systems behave in actual play.

### Current status

**v0.1 is in development.** City progression, specialization claims and selected abilities have implementations with scoped in-game test records. Advanced systems and validation remain incomplete. Current runtime support is limited to the local human player in single-player; AI-player participation, multiplayer and other recorded specializations are outside the current implementation scope.

You are viewing **develop**, the active development branch, which may include changes awaiting in-game validation. [main](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/main) retains the last approved stable playtest source baseline; development changes are promoted separately. The [project map](Specialization/README.md) provides the documentation for this branch.

[Current progress and open issues](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) are tracked separately from design decisions. Validation records distinguish local checks from game-tested scenarios and document the scope of each result.

### Selected development examples

**Preserving investment while allowing capabilities to change.** The design separates **Identity** (a city’s specialization), **Potential** (its permanent investment level) and **ACTIVE** (the level currently enabled). For an eligible city, moving a governor away can reduce its active level without erasing its Potential. This keeps long-term investment distinct from current operating conditions. [Shared rules](Specialization/Design/Shared.md)

**Keeping specialization claims consistent across saves.** I specified a one-turn claim process and tested it in-game. A save/load test revealed that the process did not resume correctly after recapturing a city. Codex implemented a targeted synchronization fix, which I retested and accepted for the documented Commerce scenario. [Validation record](Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)

**Investigating performance through playtests.** I supplied gameplay observations and a late-game save that had never enabled this mod to help assess a memory-growth issue. I tested targeted changes and a bounded garbage-collection mitigation, then accepted the stabilization work as sufficient to resume feature planning. The contribution of this mod to remaining process-memory growth is still unresolved. [Investigation and findings](Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure)

### Explore the project

| Interest | Start here |
|---|---|
| Gameplay rules and future designs | [Design reading guide](Specialization/Design/README.md) |
| System structure and technical contracts | [Architecture](Specialization/Architecture/README.md) |
| Progress and test results | [Status](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Validation records](Specialization/Status/Validation/Results/) |
| Technical investigations and limitations | [Technical evidence index](Specialization/Reports/Technical/README.md) |
| Source on this branch | [Mod/](Mod/) |
| Development and agent guidance | [AGENTS](AGENTS.md) · [Project map](Specialization/README.md) |
| Local checks and deployment | [Tests](DevelopmentTests/README.md) · [Tools](tools/README.md) |

Detailed design and engineering records are mainly in Chinese. This overview is a reading guide; the linked records define the rules, implementation status and validation scope.

<details>
<summary>Local setup and project notes</summary>

Machine-specific configuration belongs in ignored `local/config.json`; see the [example](local.config.example.json). Original screenshots, saves and bulk logs remain outside Git under the [external-materials convention](Specialization/Reports/Proposals/Legacy_Workspace_Relocation.md). The installed game package is a deployment copy: identify it from deployment records, not branch HEAD. See the [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md).

This project is unofficial and does not imply affiliation with Civilization VI or HD.

</details>

## 中文

### 这是什么项目？

**Specialization Gameplay Redesign** 是一个为 **《文明 VI》与 Harmony in Diversity（和而不同，HD）** 开发中的非官方玩法 Mod。它希望让城市形成不同且持久的发展角色，使本地投资与国内商路的选择能够影响整个文明的发展。

### 设计内容与范围

v0.1 的设计围绕四个专业展开：

- **科研：** 科研人才、研究设施与学术知识。
- **文化：** 馆藏、诠释与文化交流。
- **工业：** 建设经验、建筑模板与工程能力。
- **商业：** 商业价值发现，以及跨时间、跨城市的资本配置。

区域与专家岗位影响本地发展，国内贸易网络通过合格来源、贸易中心和接收城市建立联系。共同成长系统则将永久投资与城市当前能够激活的能力分开处理。

### 我的职责与AI辅助开发

我是 **Xuting Zheng**。我负责玩法设计、需求与开发优先级，并亲自进行游戏内测试。我决定机制与取舍，反馈实际观察，并判断测试结果是否符合预期规则。

**Codex 在我的指导下负责代码实现、技术调查、仓库维护与本地检查。** 我的重点是将设计意图转化为清楚的需求，并评估这些系统在实际游玩中的表现。

### 当前状态

**v0.1 仍在开发中。** 城市成长、专业认领及部分能力已有实现，并有明确场景范围的实机测试记录；高级系统和验证尚未全部完成。当前运行支持限于单人游戏中的本地人类玩家，AI 参与、多人游戏及其它已记录专业不在当前实施范围内。

你正在查看 **develop**，即当前开发分支，其中可能包含尚待实机验证的修改。[main](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/main) 保留上一次获准的稳定游玩源码基线，开发变更需另行批准推广。本分支的资料入口见[项目导航](Specialization/README.md)。

[当前进度与待处理问题](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) 与设计决定分别记录。验证资料区分本地检查和游戏内测试，并说明各项结果的适用范围。

### 设计与开发案例

**保留长期投资，同时允许当前能力变化。** 设计将 **Identity（专业身份）**、**Potential（永久投资等级）** 与 **ACTIVE（当前激活等级）** 分开。对有参与资格的城市而言，调离总督可能降低当前激活等级，但不会抹去其永久潜力。长期投入因此与当前生效条件保持独立。[共同规则](Specialization/Design/Shared.md)

**让专业认领在保存／加载后正确续接。** 我确定了一回合认领流程，并在游戏中测试。保存／加载测试发现，夺回城市后的认领流程无法正确恢复。Codex 随后进行了针对性的同步修复，由我复测并验收记录中的商业场景。[验收记录](Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)

**通过实机测试调查性能问题。** 我提供游玩观察，以及一个从未启用本 Mod 的后期存档，帮助判断内存增长问题。我测试了定向修改与有界垃圾回收缓解措施，并接受本轮稳定化工作已足以恢复功能规划。本 Mod 对剩余进程内存增长的具体贡献仍未确定。[调查与结论](Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure)

### 继续阅读

| 想了解什么 | 入口 |
|---|---|
| 玩法规则与未来设计 | [Design 阅读导航](Specialization/Design/README.md) |
| 系统组成与技术合同 | [Architecture](Specialization/Architecture/README.md) |
| 进度与测试结果 | [Status](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [验收记录](Specialization/Status/Validation/Results/) |
| 技术调查与限制 | [技术证据索引](Specialization/Reports/Technical/README.md) |
| 本分支源码 | [Mod/](Mod/) |
| 开发与代理工作规则 | [AGENTS](AGENTS.md) · [项目导航](Specialization/README.md) |
| 本地检查与部署 | [测试说明](DevelopmentTests/README.md) · [工具说明](tools/README.md) |

详细设计与工程记录主要使用中文。本页是阅读入口，具体规则、实现进度和验证范围以链接中的正式资料为准。

<details>
<summary>本地配置与项目说明</summary>

本机配置放在忽略的 `local/config.json`，参见[配置示例](local.config.example.json)。截图原件、存档及大体积日志依照[外部材料约定](Specialization/Reports/Proposals/Legacy_Workspace_Relocation.md)保留在 Git 之外。游戏内安装的运行包是部署副本，应根据部署记录而不是分支 HEAD 确认其版本，具体见 [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md)。

本项目为非官方项目，不表示与《文明 VI》或 HD 存在官方关联。

</details>
