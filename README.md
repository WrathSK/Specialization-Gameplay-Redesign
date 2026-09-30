# Specialization Gameplay Redesign

[English](#english) · [中文](#中文)

## English

### What is this project?

An unofficial gameplay mod in development for **Sid Meier’s Civilization VI with Harmony in Diversity (HD)**. It explores how cities can develop distinct, lasting roles through their districts, specialist jobs, investment and connections to other cities.

The design aims to make decisions about where to invest and how to connect cities matter across an empire. That is a design goal, not a claim of demonstrated player outcomes.

### Design and scope

The current v0.1 implementation scope covers four specializations. Their accepted designs have different focuses:

- **Research:** scientific specialists, infrastructure and the accumulation of academic knowledge.
- **Culture:** collections, interpretation and cultural exchange.
- **Industry:** construction experience, building templates and engineering capabilities.
- **Commerce:** discovering commercial value and allocating capital across time and cities.

Completing a city's first qualifying district normally establishes its specialization. Investment raises its permanent **Potential**; governor qualifications determine the level currently **ACTIVE**. Domestic trade routes connect qualified sources, trade centers and receiving cities. These distinctions let long-term investment survive changes in current operating conditions. See the [shared rules](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/Shared.md) for exceptions and ownership rules.

These are design directions, not a completed feature list. Military and other recorded specializations remain outside v0.1 implementation. Current runtime support is limited to the local human player in single-player; AI participation and multiplayer are outside scope.

### My role and AI-assisted development

I am **Xuting Zheng**. I own the gameplay design and acceptance decisions and carry out in-game validation. My work includes defining system rules, choosing tradeoffs, setting requirements and priorities, reporting observed behavior, and deciding whether a tested result meets the intended design.

**Codex implements the code and maintains repository files under my direction.** It also performs authorized technical investigation and local checks. I do not claim to have personally written all source code or automated tests. The repository records distinguish intended behavior, implementation decisions, local simulation and user-run game evidence.

### Current status

This is **not a complete v0.1 release**.

You are viewing **main**, the last user-designated stable playtest source baseline: **B069.96 / modinfo96**. Its [branch-matched documentation](Specialization/README.md) describes that older implementation. The latest design, development status and examples below explicitly link to [develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop); they are **not features newly delivered on main**. Documentation updates do not promote development code.

Development includes city progression, specialization-claim projects and selected profession effects, with scoped in-game results. Advanced systems remain incomplete. Industrial-template initialization and recovery currently have an unresolved state-model boundary; the [current Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) records its scope. Passing local simulation does not establish engine correctness, and acceptance of one scenario does not validate every lifecycle or ability.

The external game package is a deployment copy. Neither branch HEAD identifies what is running in a particular installation; deployment records and receipts do. No release date is promised.

### Selected development examples

1. **A project that must occupy one turn.** I specified the timing and tested the specialization-claim flow in-game. Save/load testing exposed a resume failure; Codex made a targeted synchronization repair. I accepted the tested Commerce recapture/claim-resume scenario. The [acceptance record](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md) preserves what the screenshot shows versus what my explicit confirmation establishes; it is not universal save/load certification.
2. **Performance stabilization with remaining uncertainty.** I supplied gameplay observations and a control save that had never enabled this mod. Targeted updates and bounded garbage collection provided mitigation evidence. I accepted closure of that stabilization phase. The [findings](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure) retain unresolved memory attribution: different saves cannot be subtracted to measure this mod's cost, and closure does not prove zero leaks or overhead.

### Explore the project

| Interest | Start here |
|---|---|
| Gameplay rules and future designs | [Design reading guide](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/README.md) |
| System structure and technical contracts | [Architecture](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Architecture/README.md) |
| Progress and demonstrated results | [Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Validation records](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop/Specialization/Status/Validation/Results) |
| Technical findings and limitations | [Technical evidence index](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/README.md) |
| Source on this branch | [Mod/](Mod/) |
| Development and agent guidance | [AGENTS](AGENTS.md) · [Project map](Specialization/README.md) |
| Local checks and deployment safeguards | [Tests](DevelopmentTests/README.md) · [Tools](tools/README.md) |

Detailed design and engineering records are mainly in Chinese. This overview does not replace their authority. Machine-specific configuration belongs in ignored `local/config.json`; see the [example](local.config.example.json). Raw screenshots, saves and bulk logs remain outside Git under the [external-materials convention](Specialization/Reports/Proposals/Phase1_External_Materials.md). No official affiliation with Civilization VI or HD is implied.

## 中文

### 这是什么项目？

这是一个为 **《文明VI》与 Harmony in Diversity（和而不同，HD）** 开发中的非官方玩法Mod。它探索如何通过区域、专家岗位、投资和城市间联系，让城市形成不同且持久的发展角色。

设计希望让“在哪里投资、怎样连接城市”成为影响整个文明发展的选择。这是设计目标，不是已经通过玩家研究证明的效果。

### 设计内容与范围

当前v0.1的实施范围包含四个专业。已接受设计各有侧重：

- **科研：** 科研人才、基础设施与学术知识的积累。
- **文化：** 馆藏、诠释与文化交流。
- **工业：** 建设经验、建筑模板与工程能力。
- **商业：** 商业价值发现，以及跨时间、跨城市的资本配置。

通常，城市首个完成的合格区域决定其专业身份。投资提高永久**潜力（Potential）**，总督资格决定当前**激活等级（ACTIVE）**。国内商路连接合格来源、贸易中心和接收城市。长期投资与当前生效条件分开处理；例外和易主规则见[共同规则](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/Shared.md)。

这些是设计方向，不是全部已完成的功能清单。军事和其它已记录专业不在当前v0.1实施范围内。当前运行支持限于单人游戏中的本地人类玩家，不包括AI参与和多人游戏。

### 我的职责与AI辅助开发

我是 **Xuting Zheng**。我负责玩法设计和最终验收，并亲自进行游戏内验证。具体包括系统规则、取舍、需求与优先级决定，反馈实际观察，以及判断测试结果是否符合设计意图。

**Codex在我的指导与授权下实现代码、维护仓库文件，并进行技术调查和本地检查。** 我不声称全部源码或自动化测试均由我亲手编写。仓库分别记录设计意图、实现决定、本地模拟与用户实机证据。

### 当前状态

项目**尚未完成v0.1正式发布**。

你正在查看 **main**：用户指定的上一稳定游玩源码基线 **B069.96 / modinfo96**。[本分支配套资料](Specialization/README.md)描述的是这套较早实现。最新设计、开发进度及下方案例明确链接到 [develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop)，**不表示这些成果已进入main**。文档更新不构成功能推广。

开发中已有城市成长、专业认领项目及部分专业效果的实现，并取得限定场景的实机结果；高级系统仍未全部落地。工业模板初始化与恢复目前还有状态模型边界，具体范围见[当前Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md#current-authoritative-state)。本地模拟通过不等于引擎实测通过，一个场景验收也不代表全部生命周期或能力均已验证。

游戏内运行包是外部部署副本。main或develop的HEAD都不能证明某台机器实际运行什么；需要查部署记录和receipt。本页不承诺发布日期。

### 两个开发案例

1. **必须占用一个回合的项目。** 我确定了专业认领的时长要求并进行实机测试。保存／加载暴露续接失败后，Codex进行了定域同步修复，我接受了所测商业候选夺回后的认领续接结果。[验收记录](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)区分截图直接显示的内容与我的明确确认，不将其扩大为所有存档／读档场景通过。
2. **保留未知边界的性能稳定化。** 我提供实际游玩观察及一个从未启用本Mod的对照存档。定域更新与受控垃圾回收取得运行缓解证据，我接受了这一轮稳定化结项。[调查结论](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure)仍保留未完成的内存归因：不同存档不能直接相减来计算本Mod成本，结项也不证明零泄漏或零额外开销。

### 继续阅读

| 想了解什么 | 入口 |
|---|---|
| 玩法规则与未来设计 | [Design阅读导航](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Design/README.md) |
| 系统组成与技术合同 | [Architecture](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Architecture/README.md) |
| 进度与已证明的结果 | [Status](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [验收记录](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop/Specialization/Status/Validation/Results) |
| 技术调查与限制 | [技术证据索引](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/develop/Specialization/Reports/Technical/README.md) |
| 本分支源码 | [Mod/](Mod/) |
| 开发与代理工作规则 | [AGENTS](AGENTS.md) · [项目导航](Specialization/README.md) |
| 本地检查与部署保护 | [测试说明](DevelopmentTests/README.md) · [工具说明](tools/README.md) |

详细设计与工程记录主要使用中文，本页概览不替代其权威。本机配置放在忽略的`local/config.json`，参见[配置示例](local.config.example.json)。截图原件、存档及大体积日志依照[外部材料约定](Specialization/Reports/Proposals/Phase1_External_Materials.md)保留在Git之外。本项目不表示与《文明VI》或HD存在官方关联。
