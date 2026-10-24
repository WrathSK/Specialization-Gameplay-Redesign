# Specialization Gameplay Redesign

[English](#english) · [中文](#中文)

## English

### Overview

**Specialization Gameplay Redesign** is an unofficial gameplay mod in development for **Sid Meier’s Civilization VI with Harmony in Diversity (HD)**. It is designed to give cities distinct, lasting roles and make choices about local investment and domestic trade routes matter across an empire.

### System Design Architecture and v0.1 Scope

The project encompasses a comprehensive empire-wide specialization architecture built around a shared city progression model, a domestic trade network, **11 primary specializations**, and **6 auxiliary district rules**:

- **Shared Progression & Domestic Network:** City districts and specialist jobs shape local development, while domestic trade networks connect cities through qualified sources, trade centres, and recipients. The shared progression model separates permanent investment from currently active capabilities.
- **v0.1 Implementation Focus (4 Core Specializations):** To validate the underlying architecture and establish baselines for yield formulas, balance, and opportunity costs, v0.1 focuses on implementing and playtesting the four foundational specializations:
  - **Research:** scientific specialists, research infrastructure, and academic knowledge.
  - **Culture:** collections, era interpretation, and cultural exchange.
  - **Industry:** construction experience, building templates, and engineering capabilities.
  - **Commerce:** commercial value discovery and capital allocation across time and cities.
- **Broader Design Framework (7 Future Specializations & 6 Auxiliary Districts):** Beyond the v0.1 runtime scope, the core design philosophy, structural frameworks, and direction are already established and documented for **7 additional specializations** (**Military**, **Landscape/Preserve**, **Religion/Holy Site**, **Harbor** [dual maritime-commerce and naval-military tracks], **Government Plaza**, **Diplomatic Quarter** [with an accompanying **Allied Diplomatic Missions** framework], and **Community/Neighborhood**), alongside **6 auxiliary districts** (**Entertainment/Water Park**, **Aqueduct**, **Dam**, **Canal**, **Aerodrome**, and **Spaceport**). These remaining modules await v0.1 baseline acceptance, parameter/formula tuning, and further auxiliary restructuring before implementation. See the [Design Reading Guide](Specialization/Design/README.md) for the full design map and per-module maturity.

### Development and Workflow

- **Design & Direction (Xuting Zheng):** Leads gameplay architecture, defines requirements and development priorities, resolves design trade-offs when engine constraints arise, and conducts all in-game playtesting and acceptance.
- **Implementation & Tooling (Codex):** Handles Lua/SQL/UI implementation, technical investigations, repository maintenance, and local checks under explicit direction and task-scoped batch boundaries (`AGENTS.md`, `Specialization/Workflow/`), keeping implementation separate from read-only advisory or investigation reviews.
- **Verification Boundaries:** Progress and validation records strictly separate static code/database checks (`STATIC_CONFIRMED`), local Python/Lua simulations (`LOCAL_SIMULATION_PASS`), and human in-game playtest results (`USER_GAME_TEST_PASS`), documenting the exact scenario scope for each accepted feature.

### Selected Development Examples

- **Preserving long-term investment while allowing active capabilities to change:** The progression design separates **Identity** (a city’s specialization), **Potential** (its permanent investment level), and **ACTIVE** (the level currently enabled). For an eligible city, moving a governor away can reduce its active level without erasing its permanent Potential, keeping long-term investment distinct from current operating conditions. See [Shared rules](Specialization/Design/Shared.md).
- **Keeping specialization claims consistent across save/load:** During in-game testing of a one-turn specialization claim process, a save/load check revealed that the process did not resume correctly after recapturing a city. Under user direction, Codex implemented a targeted state synchronization fix, which was then retested in-game and accepted for the documented Commerce scenario. See [Validation record](Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md).
- **Investigating late-game performance through controlled playtests:** Gameplay observations and a late-game control save (which had never enabled this mod) were supplied to help assess a memory-growth issue. Following in-game testing of targeted changes and a bounded garbage-collection mitigation, the stabilization work was accepted as sufficient to resume feature planning, while the mod's exact contribution to remaining process-memory growth remains documented as an open question. See [Investigation and findings](Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure).

### Current Status and Branches

**v0.1 is in alpha development and playtesting.** City progression, specialization claims, and selected abilities across the four v0.1 specializations have implementations with scoped in-game test records; advanced systems and full validation remain in progress. Current runtime support is limited to the local human player in single-player. AI participation, multiplayer, and the remaining documented specializations are outside the current v0.1 implementation scope.

- **[main](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/main)** holds the approved playtest source; see the [Stable Playtest Guide](Specialization/Stable_Playtest.md).
- **[develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop)** holds ongoing development; see the [Development Guide](Specialization/Development_Guide.md).
- **[Current progress and open issues](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state)** are tracked in `Status` and `Authority.json`, separate from design specifications. Relative documentation links describe the branch you are viewing.

### Quick Navigation

| What you want to explore | Where to start |
|---|---|
| Full gameplay design map (11 specializations & 6 auxiliary districts) | [Design reading guide](Specialization/Design/README.md) · [Shared rules](Specialization/Design/Shared.md) · [Domestic network](Specialization/Design/Network.md) |
| System structure and technical contracts | [Architecture reading entry](Specialization/Architecture/README.md) |
| Current progress and scoped test results | [Status](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Validation records](Specialization/Status/Validation/Results/) |
| Technical investigations and engine constraints | [Technical evidence index](Specialization/Reports/Technical/README.md) · [Advisory reviews](Specialization/Reports/Advisory/README.md) |
| Project navigation and AI workflow rules | [Project map](Specialization/README.md) · [Root AGENTS](AGENTS.md) · [Workflow](Specialization/Workflow/README.md) |
| Runtime source, local checks, and tools | [Mod/](Mod/) · [DevelopmentTests](DevelopmentTests/README.md) · [Tools](tools/README.md) |

Detailed gameplay design and engineering records are mainly in Chinese, with newer technical and governance documentation in English. This overview serves as a reading guide; the linked records define the formal rules, implementation status, and validation scope.

<details>
<summary>Local setup and repository notes</summary>

Machine-specific configuration belongs in ignored `local/config.json`; see the [configuration example](local.config.example.json). Original screenshots, saves, and bulk logs remain outside Git under the [external-materials convention](Specialization/Reports/Proposals/Legacy_Workspace_Relocation.md). The installed game package is an external deployment copy: identify it from deployment records rather than branch `HEAD`. See the [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md).

This project is an unofficial mod and is not affiliated with Firaxis Games, 2K, or the Harmony in Diversity (HD) team.

</details>

---

## 中文

### 项目简介

**Specialization Gameplay Redesign** 是一个为 **《文明 VI》与 Harmony in Diversity（和而不同，HD）** 开发中的非官方玩法 Mod。项目旨在让城市形成不同且持久的发展角色，使本地投资与国内商路的选择能够深刻影响整个文明的演进。

### 系统设计版图与 v0.1 实施范围

本项目构建了一套完整的全帝国城市专业化系统设计，涵盖共同城市成长系统、国内贸易网络、**11 个主专业方向**以及 **6 个辅助区域规则**：

- **共同成长与国内网络：** 区域与专家岗位塑造本地发展，国内贸易网络通过合格来源、贸易中心和接收城市建立跨城联系。共同成长系统将城市的永久投资与当前可激活的能力解耦。
- **v0.1 首发实施重点（4 大核心专业）：** 为验证底层系统架构，并为后续全系统确立收益公式、数值平衡与机会成本的参照基线，v0.1 阶段精选了最核心的四个专业作为实现与实机测试目标：
  - **科研：** 科研人才、研究设施与学术知识。
  - **文化：** 馆藏、时代诠释与文化交流。
  - **工业：** 建设经验、建筑模板与工程能力。
  - **商业：** 商业价值发现，以及跨时间、跨城市的资本配置。
- **完整系统框架（7 个未来主专业 + 6 个辅助区域）：** 除 v0.1 首发四专业外，其余 **7 个主专业**（**军事**、**景观／保护区**、**宗教／圣地**、**港口**［海洋商业与海军军事双线］、**市政／政府广场**、**外交区**［含配套的**联盟外交任务**框架］、**社区／都会**）的设计理念、哲学方向与主体框架均已敲定落盘；另有 **6 个辅助区域**（**娱乐中心／水上乐园**、**水渠**、**堤坝**、**运河**、**航空港／机场**、**宇航中心**）已记录独立规则方向，待后续重构与衔接适配。这些非首发模块将在 v0.1 完成基线验收后，逐步填入具体参数公式并推进实施。各模块的完整设计与当前成熟度边界见 [Design 阅读导航](Specialization/Design/README.md)。

### 开发分工与验证原则

- **玩法设计与项目主导（Xuting Zheng）：** 负责全系统玩法架构、需求定义与优先级排序，在遇到底层引擎或接口限制时决定机制取舍，并负责全部游戏内实机测试与最终验收。
- **代码实现与工程维护（Codex）：** 在明确的任务批次边界（`AGENTS.md`、`Specialization/Workflow/`）与指导下，负责代码实现、技术调查、仓库维护与本地检查，并将主线实现与只读的审阅（Advisory）及专项调查（Investigation）隔离。
- **验证边界：** 进度与验收记录严格区分静态核对（`STATIC_CONFIRMED`）、本地 Python/Lua 模拟（`LOCAL_SIMULATION_PASS`）与游戏内实机测试结果（`USER_GAME_TEST_PASS`），并明确标注每项测试通过的具体游戏场景范围。

### 设计与开发案例

- **保留长期投资，同时允许当前激活能力动态变化：** 共同成长系统将 **Identity（专业身份）**、**Potential（永久投资等级）** 与 **ACTIVE（当前激活等级）** 分离。对符合资格的城市而言，调离总督可能降低其当前激活等级，但不会抹去已积累的永久潜力，从而使长期投入与当前生效条件保持独立。见[共同规则](Specialization/Design/Shared.md)。
- **确保专业认领在保存／读档后正确续接：** 在对一回合专业认领流程进行实机测试时，保存／加载测试暴露出夺回城市后的认领流程无法正确恢复。Codex 在项目主导者指导下完成了针对性的状态同步修复，随后经实机复测验收了文档记录中的商业场景。见[验收记录](Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)。
- **通过对照实机测试调查后期性能问题：** 为评估后期内存增长问题，测试中提供了实机游玩观察及一个从未启用本 Mod 的原版／HD 后期对照存档。经对定向修改与有界垃圾回收（GC）缓解措施的实机验证，确认本轮稳定化工作已足以恢复功能规划；同时将本 Mod 对剩余进程内存增长的具体贡献如实保留为待解问题。见[调查与结论](Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure)。

### 当前状态与分支说明

**v0.1 处于 alpha 开发与实机测试阶段。** 城市成长、专业认领及首发四专业的部分能力已有实现，并附有明确场景范围的实机测试记录；高级系统与完整验证仍在进行中。当前运行支持限于单人游戏中的本地人类玩家，AI 玩家参与、多人游戏及其它已记录的未来专业不在当前 v0.1 实施范围内。

- **[main](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/main)** 保存获准的实机测试源码，详见[稳定测试说明](Specialization/Stable_Playtest.md)。
- **[develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop)** 保存持续开发内容，详见[开发指南](Specialization/Development_Guide.md)。
- **[当前进度与待处理问题](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state)** 独立记录在 `Status` 与 `Authority.json` 中，与设计规范分开维护。页面中的相对链接对应你当前正在查看的分支。

### 快速导航

| 想了解的内容 | 阅读入口 |
|---|---|
| 完整玩法设计版图（11 主专业与 6 辅助区域） | [Design 阅读导航](Specialization/Design/README.md) · [共同规则](Specialization/Design/Shared.md) · [国内网络](Specialization/Design/Network.md) |
| 系统架构与技术合同 | [Architecture 阅读入口](Specialization/Architecture/README.md) |
| 当前进度与分场景测试结果 | [Status 当前状态](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Validation 验收记录](Specialization/Status/Validation/Results/) |
| 技术调查与引擎限制证据 | [技术证据索引](Specialization/Reports/Technical/README.md) · [Advisory 审阅报告](Specialization/Reports/Advisory/README.md) |
| 项目总导航与 AI 协作规则 | [项目内部导航](Specialization/README.md) · [根 AGENTS](AGENTS.md) · [Workflow 规范](Specialization/Workflow/README.md) |
| 本分支源码、本地检查与工具 | [Mod/](Mod/) · [测试说明](DevelopmentTests/README.md) · [工具说明](tools/README.md) |

详细玩法设计与工程记录主要使用中文，近期技术报告与工作流规范主要使用英文。本页为总览阅读入口，具体规则、实现进度和验证范围以链接中的正式记录为准。

<details>
<summary>本地配置与仓库说明</summary>

本机配置保存在 Git 忽略的 `local/config.json` 中，参见[配置示例](local.config.example.json)。截图原件、存档及大体积日志依照[外部材料约定](Specialization/Reports/Proposals/Legacy_Workspace_Relocation.md)保留在 Git 之外。游戏内安装的运行包是外部部署副本，应根据部署记录而非分支 `HEAD` 确认其版本，具体见 [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md)。

本项目为非官方衍生作品，与《文明 VI》官方及 Harmony in Diversity（HD）团队无官方隶属关系。

</details>