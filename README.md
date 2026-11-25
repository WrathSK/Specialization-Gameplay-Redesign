# Specialization Gameplay Redesign

[English](#english) · [中文](#中文)

## English

### Overview

**Specialization Gameplay Redesign** is an unofficial gameplay mod in development for *Sid Meier’s Civilization VI: Gathering Storm*. It gives cities lasting roles and connects their development through domestic trade.

A city gains a specialization when it completes an eligible district. Players can invest in that city to increase its permanent **Potential**, while its current **ACTIVE** level determines which abilities are available. Districts, buildings, specialists, and trade routes provide the conditions each ability uses.

In **v0.1 alpha**, Research, Culture, Industry, and Commerce are playable by the local human player in single-player. Key mechanics have been tested in both an HD-compatible environment and an official Gathering Storm-based environment using testing aids. Individual results and configurations are recorded in the [playtest backlog](Specialization/Status/Playtest_Backlog.md).

### The specialization system

The full design covers a shared city progression model, a domestic trade network, **11 primary specializations**, and **six auxiliary district rule sets**.

The four implemented specializations establish the v0.1 foundation:

- **Research** develops specialists, research infrastructure, and knowledge across districts.
- **Culture** turns Great Works into local yields and tourism, and sends expeditions abroad.
- **Industry** shares construction knowledge, trains construction crews, and develops engineering traditions.
- **Commerce** creates commercial value and directs capital and development investment between cities.

Seven additional specializations have documented design foundations: **Military**, **Landscape/Preserve**, **Religion/Holy Site**, **Harbor**, **Government Plaza**, **Diplomatic Quarter**, and **Community/Neighborhood**. The design also records rules for **Entertainment Complex/Water Park**, **Aqueduct**, **Dam**, **Canal**, **Aerodrome**, and **Spaceport**. These areas remain future work, with their individual maturity and open questions described in the [design guide](Specialization/Design/README.md).

### Design and engineering

Xuting Zheng leads gameplay design and project direction, defines system boundaries and trade-offs, and conducts in-game testing and acceptance. Codex implements Lua, SQL, UI, and tooling changes, investigates technical constraints, and runs local checks under that direction. External reviews provide additional feedback on scoped questions.

**Shared facts, independent abilities.** City and network changes notify affected consumers. Specializations reuse shared facts, then independently calculate and apply their effects. Real writes invalidate the relevant facts so a second change in the same turn can still be processed. In one targeted local combination test, anchor sampling fell from three reads to one and city-index reads from four to two, with equivalent outputs. [Architecture closeout](Specialization/Reports/Proposals/Architecture_Convergence_Closeout_Review.md)

**Shared rules across building environments.** Building tiers follow the actual upgrade chain loaded for the same district. A building inserted into that chain can change later tiers, while virtual or unrelated prerequisites do not automatically add a tier. A shared catalog supplies these facts to abilities in both official and HD environments, using the approved depth calculation rules. Both environments have targeted playtest records. [Environment and shared depth](Specialization/Architecture/Specialization_v0.1_Architecture.md#environment-assembly-and-shared-depth--a0185)

**Evidence for irreversible grants.** Construction crew grants require evidence linking the city, order, completion, and unit. A bounded diagnostic recorded two cities completing the same crew in one turn. In the observed sequence, each order produced one bound unit, with no additional grant after the recorded reload. Other counter and callback orders retain their own evidence boundaries. [B413 playtest record](Specialization/Status/Specialization_P0_Status.md#focused-b413-native-evidence-reviewed--s0902)

### Status and next steps

**v0.1 is in alpha playtesting.** The stable playtest baseline on `main` is **B528.555**. Ongoing work continues on `develop`.

Upcoming work includes:

1. Balancing the four existing specializations.
2. Refining city ownership transfer, city loss, and specialization history rules.
3. Designing an allocated resource to replace governor levels as the source of current specialization capacity.
4. Revisiting domestic trade network connection rules.
5. Refining and implementing the additional documented specializations.

Current support covers new games started on the active build and saves loaded on that same build. Static checks, local simulations, and in-game observations are recorded with their own scopes. [Current status](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Stable playtest guide](Specialization/Stable_Playtest.md)

### Explore the repository

| Interested in | Start here |
|---|---|
| Gameplay rules and future designs | [Design guide](Specialization/Design/README.md) · [Shared rules](Specialization/Design/Shared.md) · [Domestic network](Specialization/Design/Network.md) |
| System structure and implementation | [Architecture guide](Specialization/Architecture/README.md) · [Mod source](Mod/) |
| Test results and technical investigations | [Current validation status](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [Technical evidence](Specialization/Reports/Technical/README.md) |
| Development and project navigation | [Development guide](Specialization/Development_Guide.md) · [Project map](Specialization/README.md) · [Tools](tools/README.md) |

Detailed gameplay design and engineering records are primarily in Chinese, with some technical documentation in English.

This is an unofficial project, unaffiliated with Firaxis Games, 2K, or the Harmony in Diversity team.

---

## 中文

### 项目简介

**Specialization Gameplay Redesign** 是一款为《文明 VI：风云变幻》开发中的非官方玩法 Mod。项目让城市形成持久的发展方向，并通过国内商路将各城的发展联系起来。

城市完成符合条件的区域后获得专业身份。玩家可以向城市投资，提高永久**潜力（Potential）**；当前**激活等级（ACTIVE）**则决定此刻能够使用哪些能力。区域、建筑、专家和商路分别为各项能力提供所需条件。

在 **v0.1 Alpha** 阶段，科研、文化、工业和商业四个专业已可由单人游戏中的本地玩家使用。重点机制已在 HD 兼容环境，以及使用测试辅助 Mod 的《风云变幻》官方内容环境中分别进行实机测试。具体配置与场景见[实机记录](Specialization/Status/Playtest_Backlog.md)。

### 专业化系统

完整设计涵盖共同城市成长、国内商路网络、**11 个主专业方向**和 **6 组辅助区域规则**。

v0.1 以四个专业建立系统基础：

- **科研**发展专家、研究设施与跨区域的学术知识。
- **文化**让巨作带来本城产出与旅游业绩，并向外国派遣考察团。
- **工业**分享建设知识、训练施工队，并积累工程传统。
- **商业**创造商业收益，并在城市之间进行资本与发展投资。

其余七个主专业已有设计基础，分别是**军事、景观／保护区、宗教／圣地、港口、市政／政府广场、外交区、社区／都会**。设计中还记录了**娱乐中心／水上乐园、水渠、堤坝、运河、航空港／机场、宇航中心**六组辅助区域规则。各项仍需后续完善与实施，成熟度和未决事项见[设计阅读导航](Specialization/Design/README.md)。

### 设计与工程实践

Xuting Zheng 负责玩法设计、项目方向、系统边界与关键取舍，并进行实机测试与验收。Codex 在这些决定下实现 Lua、SQL、界面和工具，调查技术限制并执行本地验证。外部审阅针对具体问题提供额外反馈。

**共享事实，专业独立处理。** 城市或商路变化时，系统通知受影响的能力。各专业复用共享事实，再独立计算并更新自身效果。真实写入会使相关事实失效，确保同回合的后续变化仍能被处理。在一次定向本地组合测试中，锚点采样从 3 次降为 1 次，城市索引读取从 4 次降为 2 次，结果保持一致。 [架构结项记录](Specialization/Reports/Proposals/Architecture_Convergence_Closeout_Review.md)

**让不同建筑体系使用共享规则。** 建筑层级依据本局加载的同区域升级链计算。扩展在链中插入建筑，可以改变后续建筑的层级；虚拟或无关前置条件不会自动增加层级。共享目录向官方与 HD 环境中的能力提供这些事实，沿用已批准的基础设施深度计算规则。两种环境均有定向实机记录。 [环境与共享深度](Specialization/Architecture/Specialization_v0.1_Architecture.md#environment-assembly-and-shared-depth--a0185)

**为不可逆操作保留完成凭据。** 施工队发放需要能够关联城市、订单、完成依据和实际单位。一次有上限的诊断记录了两座城市同回合完成同级施工队的过程。在所测顺序下，两笔订单各绑定一支队伍，记录中的读档后没有额外发放。其他计数和回调顺序保留各自的证据边界。 [B413 实机记录](Specialization/Status/Specialization_P0_Status.md#focused-b413-native-evidence-reviewed--s0902)

### 当前状态与后续方向

**v0.1 处于 Alpha 实机测试阶段。** `main` 的当前稳定测试基线为 **B528.555**，后续开发在 `develop` 上继续。

接下来的工作包括：

1. 调整现有四个专业的平衡性。
2. 完善城市易主、失城及专业历史的保留规则。
3. 设计替代总督等级的专业资源分配机制。
4. 重新调整国内商路网络的连接规则。
5. 完善已有设计基础的其他专业并分批实施。

当前支持从运行构建开启的新局及同构建存档。静态检查、本地模拟和实机观察分别记录其适用范围。 [当前状态](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [稳定测试说明](Specialization/Stable_Playtest.md)

### 阅读导航

| 想了解的内容 | 从这里开始 |
|---|---|
| 玩法规则与未来设计 | [设计导航](Specialization/Design/README.md) · [共同规则](Specialization/Design/Shared.md) · [国内网络](Specialization/Design/Network.md) |
| 架构与实现 | [架构入口](Specialization/Architecture/README.md) · [Mod 源码](Mod/) |
| 测试结果与引擎调查 | [现行验收状态](Specialization/Status/Specialization_P0_Status.md#current-authoritative-state) · [技术证据](Specialization/Reports/Technical/README.md) |
| 开发与项目导航 | [开发指南](Specialization/Development_Guide.md) · [项目内部导航](Specialization/README.md) · [工具](tools/README.md) |

详细设计和工程记录以中文为主，部分技术文档使用英文。

本项目为非官方作品，与 Firaxis Games、2K 及 Harmony in Diversity 团队无官方隶属关系。
