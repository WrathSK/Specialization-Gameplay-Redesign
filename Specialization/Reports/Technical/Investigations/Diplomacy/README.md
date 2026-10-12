# Diplomacy / 外交接口调查

> Publication note: machine-specific prefixes have been replaced with source labels; technical conclusions, evidence scope and historical observations are unchanged. `CIV_ASSETS` denotes the installed `Civ6.app/Contents/Assets`; `WORKSHOP_289070` denotes Civilization VI Workshop content, with each following numeric directory identifying its published item; `CIV6_USER_DATA` denotes the configured Civilization VI user-data root. `STEAM_APPS` denotes the selected Steam library's `steamapps` directory. Suffixes and line references preserve the original source location. These are source locators, not public links or shell variables.


Investigation / Non-authoritative / No design decision implied

Status: Stable
维护者: General Investigation Agent（本调查会话）

本主题调查 Civ VI／Harmony in Diversity 暴露的文明关系、正式外交关系、联盟、外交支持、城邦／使者及世界议会接口。能力标签为 READ／WRITE／LISTEN／AI-CONSUMED；发现接口不表示获准调用写接口或修改玩法。

本轮排除外交专业设计、任务机制实施、原型和测试、游戏启动、部署、存档改动，以及 AI 接受联盟或投票的决策逻辑。外交任务的其它区域机制不因引用而进入本轮调查。

当前报告：[Diplomacy Surface Overview](Diplomacy_Surface_Overview.md)。只维护必要的主题 Markdown，不预建分报告。Stable 仅表示证据版本可引用，不表示用户接受、Design 冻结或实施授权。

本轮定域续查：[City-State Control / Protection + Diplomat-vs-Spy Semantics](CityState_Control_Protection_and_Diplomat_Spy_Semantics.md)，仅调查宗主锁、宣战前城邦保护与 Spy 复用语义。三条证据链及原生验证缺口需要独立维护，因此只新增这一份报告；概览已加入结论和入口。

2026-10-04 首个 checkpoint 覆盖 A–F 六项，已停写本 README 和概览。两文件暂留 untracked，等待用户审阅／外部设计讨论及 Main Task 的显式入库决定；后续不在后台改写这个版本。

checkpoint 交接：调查者停写指定 Stable 文件 → Main Task 只读审阅 → 用户接受 → Main Task 显式 stage／commit／push。本会话 Git 只读。

## 本机技术来源

以下入口由用户补充，据用户说明已由 Main Task 核对存在；本次只记录，未重新读取来源。它们仅供用户明确授权的具体调查主题按 Stage A／B／C 定域只读使用。许可适用于收到本补充后的操作，不追认更早的 C1 读取；概览中的实际授权顺序记录保持。

| 入口 | 精确路径 | 用途与限制 |
|---|---|---|
| Civ VI 用户数据根 | `CIV6_USER_DATA` | 用户数据 workspace，不是 canonical repo；不读存档、备份、无关私人配置，不递归扫描 |
| 当前加载定义 DB | `CIV6_USER_DATA/Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite` | 仅 SQLite `mode=ro`；查询 Gameplay 定义、schema、Modifier／Effect 及关联；不代表存档实时状态或实机 PASS，不写入或复制进 Git |
| Mod 安装注册 DB | `CIV6_USER_DATA/Firaxis Games/Sid Meier's Civilization VI/Mods.sqlite` | 仅 `mode=ro` 查询必要安装路径、注册信息及相关 schema；不展开无关 Mod 或私人设置 |
| 本游戏 Steam manifest | `STEAM_APPS/appmanifest_289070.acf` | 仅读必要安装目录、appid、buildid 等字段；不扫描其它游戏或账户资料 |
| 原版源码／资料根 | `CIV_ASSETS` | 当前主题相关 Lua／SQL／XML／modinfo；沿明确调用、include、事件或 DB 关系读取，不通读 Assets 或读取无关二进制、影片、资源包 |
| HD 核心 manifest | `WORKSHOP_289070/2465378070/DL.modinfo` | 所在目录为 HD 核心；先通过 manifest 定位主题文件，再沿明确证据读取，不通读整个 Mod |
| HD 区域扩展 manifest | `WORKSHOP_289070/2701747165/DistrictExpansionHD.modinfo` | 所在目录为区域扩展，不是 HD 核心；仅当前主题出现明确依赖时读取，不默认展开 |

提供入口不恢复或扩大调查，也不授权调用游戏写接口、修改原件／配置／存档／runtime，或运行原型、测试、游戏、部署。每个新主题仍须明确授权并重新从 Stage A 开始；未列出的外部来源、其它主题、Historical 或广泛扫描仍须先确认。精确路径失效只报告缺口，不扫描磁盘猜替代位置。

此前来源补充只修改本 README，未重读来源，也未追认 C1。用户本次另行明确授权了 A／B／C 定域续查；它不扩大其它主题、玩法或实施边界。本轮文字核对完成，本 README、概览和唯一续查报告均为 **Stable**，已停写，等待用户讨论。Git 始终只读。

## Spy probability follow-up — 2026-10-09

[Spy Mission Probability and Diplomat Reuse](Spy_Mission_Probability_and_Diplomat_Reuse.md) is a separate, focused **Stable / stopped** checkpoint. It compares installed native and loaded HD mission parameters, rank / promotion / Gain Sources / Counterspy inputs, result presentation, and non-Spy reuse boundaries. The exact engine formula, risky-mission ceiling, stacking and non-Spy calculator contract remain UNKNOWN; no community probability table or new Diplomat rule is adopted. Earlier Stable reports are unchanged. This follow-up performs no prototypes, tests, game launch, deployment or Git writes; further work awaits user discussion.
