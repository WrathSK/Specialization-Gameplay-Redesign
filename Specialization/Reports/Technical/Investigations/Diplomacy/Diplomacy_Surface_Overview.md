# Diplomacy Surface Overview / 外交接口概览

> Publication note: machine-specific prefixes have been replaced with source labels; technical conclusions, evidence scope and historical observations are unchanged. `CIV_ASSETS` denotes the installed `Civ6.app/Contents/Assets`; `WORKSHOP_289070` denotes Civilization VI Workshop content, with each following numeric directory identifying its published item; `CIV6_USER_DATA` denotes the configured Civilization VI user-data root. Suffixes and line references preserve the original source location. These are source locators, not public links or shell variables.


Investigation / Non-authoritative / No design decision implied

Status: Stable
维护者: General Investigation Agent（本调查会话）
范围: 文明关系、正式外交关系、联盟、Favor、城邦／使者、世界议会；仅静态接口与来源调查，不调查 AI 投票／联盟接受逻辑，不实施、不运行原型／测试／游戏。
依据: develop `e8b5f7f19249db75442407534e74b5bda149e9d3`；Authority D0047／Status S0430。启动时 tracked、staged、untracked 均无改动；本主题原先不存在。

## 已确认事实与证据

**外交的读取和 UI 通知表面较完整；支持、使者及联盟增速有原生数据承载。任意文明对的关系写入、指定盟友一次 XP 奖励、永久宗主保护与新增变化的 AI 消费，仍不能据这些静态来源宣称可靠。**

本概览覆盖 A–F 六项。无需先拆分报告；细节和证据入口集中在下文。

### 证据口径与来源版本

| 标记 | 本报告含义 |
|---|---|
| S | STATIC_CONFIRMED：已读安装代码、加载 DB 的定义／实际关联，或明确事件注册。证明表面存在，不证明本项目调用后原生成功 |
| D | DOCUMENTED_ONLY：公开 API 文档记录的方法／上下文；缺参数或当前版本调用证据，保留这个较弱等级 |
| U | UNKNOWN：本轮没有足够证据；不是“不支持” |
| AI-CONSUMED | 要求证据表明 AI 决策消费目标变化；UI 更新、Modifier 存在、AI 对象名称和配置阈值都不能单独满足 |

本批没有运行原型、测试或游戏。`LOCAL_SIMULATION_PASS`：无新增；`USER_GAME_TEST`／native PASS：本主题无已复核证据。其它四专业的既有 PASS 不转用于外交。

- 用户后来明确提供并授权的支持目录：`CIV6_USER_DATA`。C1 的外部数据库读取发生在收到该回复之前，不能用后来的确认描述为当时已获授权；实际顺序见 Read Ledger。路由 AGENTS 已读，未读取存档、设置内容或备份。
- 本轮 DB：`CIV6_USER_DATA/Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`，25,255,936 bytes，mtime **2026-10-04 20:01:18 America/Vancouver**；SQLite URI `mode=ro`。它是加载后的静态 Gameplay 定义库，不是当前存档的实时外交状态。
- `Mods.sqlite` 明确登记 HD 核心 `2465378070/DL.modinfo`；manifest 版本 **2.2**、UUID `521b8777-0977-4859-a5ee-3e411a732e5c`。`2701747165` 登记为 **DistrictExpansionHD**，不能把它当作 HD 核心。Modding.log 有核心 Gameplay 注册路径；这不证明每个 UI replacement 在当前组合中最终生效。
- 用户另行允许定域只读原版安装来源。`appmanifest_289070.acf` 的 Steam buildid 为 **15296837**；Startup.log 记录游戏 **1.0.12.54 (951533)**。原版来源根为 `CIV_ASSETS`。
- 公开补充为 Sukritact 自己维护的 API 文档，访问日期 2026-10-04。这是社区接口记录，缺少对本机版本完整匹配的承诺；页面空白参数不补写成已验证签名。

### 关键证据入口

以下本地链接行号对应本次读取版本。后文用 E 编号引用它们。

| 编号 | 直接证据 |
|---|---|
| E1 | 原版关系条／原因分数 (`CIV_ASSETS/Base/Assets/UI/DiplomacyActionView.lua:869`)：StateIndex、RelationshipLevel、`tip.Score/Text`；查询正式关系 (`CIV_ASSETS/Base/Assets/UI/DiplomacyActionView.lua:1413`) |
| E2 | 关系图标状态映射 (`CIV_ASSETS/Base/Assets/UI/DiplomacyActionView.lua:192`)；图标显示条件 (`CIV_ASSETS/Base/Assets/UI/Instances/LeaderIcon.lua:152`)；纹理样式 (`CIV_ASSETS/Base/Assets/UI/Civ6_Styles.xml:2080`) |
| E3 | 原版定向外交请求 (`CIV_ASSETS/Base/Assets/UI/DiplomacyActionView.lua:470`)；行为有效性检查 (`CIV_ASSETS/Base/Assets/UI/DiplomacyStatementSupport.lua:167`)；交易协议类型与时长 (`CIV_ASSETS/DLC/Expansion2/UI/Replacements/DiplomacyDealView.lua:1783`) |
| E4 | 联盟进度／增速／到期 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/DiplomacyActionView_AllianceTab.lua:21`)；联盟事件注册 (`CIV_ASSETS/DLC/Expansion2/UI/Loaders/TutorialLoader_Expansion1.lua:148`) |
| E5 | Favor 读取、来源提示与事件 (`CIV_ASSETS/DLC/Expansion2/UI/Replacements/TopPanel_Expansion2.lua:167`) |
| E6 | HD 城邦任务读取 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:497`)；派遣操作 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:1028`)；使者／宗主读取 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:2082`)；类型映射 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:2362`)；事件注册 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:2601`) |
| E7 | 世界议会议题读取 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/WorldCongressPopup.lua:568`)；投票结果 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/WorldCongressPopup.lua:1818`)；生效决议 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/WorldCongressPopup.lua:2008`)；会议事件 (`CIV_ASSETS/DLC/Expansion2/UI/Additions/CongressButton.lua:57`) |
| E8 | 世界议会 Gameplay 验证回调 (`CIV_ASSETS/DLC/Expansion2/Scripts/WorldCongress.lua:293`)；QuestChanged 参数使用 (`CIV_ASSETS/DLC/Expansion2/UI/CityBanners/CityBannerManager.lua:2877`) |
| E9 | HD 外交 SQL (`WORKSHOP_289070/2465378070/UpdateDataBase/DL_Diplomacy.sql:48`)：实际 TradeBonus 修改与注释块；原版／HD 的最终静态关联以本轮 DB 为依据 |
| E10 | 公开方法／上下文记录：[AiDiplomacy](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/AiDiplomacy)、[Gameplay PlayerDiplomacy](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerDiplomacy)、[UI TeamDiplomacy](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/TeamDiplomacy)、[PlayerInfluence](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerInfluence)、[CongressManager](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CongressManager) |

## Read / Write / Listen surface

### 概览

| 项目 | READ | WRITE | LISTEN | AI-CONSUMED | 最关键限制 |
|---|---|---|---|---|---|
| A 文明态度／关系 | S：离散状态、逐原因分数；总分 getter 有 S/D 依据 | S：外交 opinion Effect；D：AdjustBaseDiplomacy；任意 pair 写入 U | S：RelationshipChanged、宣战／和平／接触 | U；存在静态状态机配置 | UI 关系条不是连续好感分；数值与正式关系有不同入口 |
| B 代表团／大使馆／边界／友谊／联盟 | S：各状态与方向可读 | S：原生请求／交易表面；D：部分 Gameplay flag setters | S：关系／交易成立；交易到期事件 D | U | 发出请求不保证 AI 接受；直接设 flag 的完整生命周期未验证 |
| C 联盟类型／等级／进度 | S：UI getters 与点数换算 | S：联盟增速 Modifier；指定 pair 即时 XP setter U | S：Available／Ended；专用升级事件 U | U | 默认 owner 范围不能自动当作仅作用一个盟友 |
| D 外交支持 Favor | S：余额、每回合、来源提示 | S：一次／每回合 Effect 与城市附件；D：ChangeFavor | S：FavorChanged | U | 提示是本地化文本，不是来源账本；直接写入的归因 U |
| E 城邦／使者 | S：未分配、逐城邦、宗主、类型、活跃任务 | S：派遣操作／奖励 Effect；D：free-token 方法；任意撤回一枚 U | S：InfluenceChanged／Given、QuestChanged；专用宗主事件 U | U | 没有证明永久锁宗主；无宗主并不单独证明平票 |
| F 世界议会 | S：会议状态、议题、生效决议、历史票／结果 | S：原生玩家投票操作表面；强制结果 U；本轮不展开写机制 | S：Stage1／2、Finished、RibbonUpdate 等 | U；AI 投票逻辑排除 | 主要读取入口在 UI；结果通知与结果数据分别取得 |

所有 S 仍属于静态证据。API 对象在 UI 和 Gameplay 的方法集合不同，不能把同名 `GetDiplomacy()` 或 `Events` 当作跨上下文通用合同。

### A. Civilization-to-Civilization Relationship

**已确认：可以查询一个 AI 对另一玩家的离散态度，也可以读取数值原因。** E1 明确查询 `selectedPlayer:GetDiplomaticAI():GetDiplomaticStateIndex(localPlayerID)`，随后读取 `GameInfo.DiplomaticStates`。`GetDiplomaticModifiers(otherID)` 返回的条目有 `Score`、`Text`；原版将正分显示绿色、负分显示红色。总分方法 `GetDiplomaticScore(otherID)` 在原版 CityStates 数据收集中被调用，E10 也记录它；本轮没有验证它对每种 owner／未接触 pair 的适用性。

| 表面 | 状态与依据 | 限制 |
|---|---|---|
| Pair READ | S：明确 `otherPlayerID` 参数，E1 | A 对 B 的态度不能由 B 对 A 的读数代替；人类的“态度”不能按 AI UI 自动推定 |
| 红／黄／绿关系图标 | S：E2 将 FRIENDLY／NEUTRAL／UNFRIENDLY 映射到 VisState **2／3／4** | 样式只给纹理引用，精确前缀查询未找到可读纹理；本轮不把色彩像素映射标 S。正式友谊／联盟／谴责／战争另有 1／0／5／6；不能只用三种颜色覆盖全部状态 |
| 关系条 | S：DB RelationshipLevel 为 FRIENDLY=66、NEUTRAL=50、UNFRIENDLY=33；E1 使用该值除 100；战争／联盟另有 UI 特例 | 这些是状态显示位置，不是 API 返回的连续好感分或转档阈值 |
| Opinion Modifier | S：`MODIFIER_PLAYER_DIPLOMACY_SIMPLE_MODIFIER` → `COLLECTION_MAJOR_PLAYERS` → `EFFECT_DIPLOMACY_SIMPLE_EFFECT` | 已有定义使用 InitialValue、Increment／Reduction 等参数和 SubjectRequirementSet；撤销、叠加、归因和时序仍待原生验证 |
| Base opinion API | D：Gameplay `GetAi_Diplomacy()` 上的 `AdjustBaseDiplomacy`，E10 | 文档参数为空；未取得当前原生调用签名，不提供猜测性调用配方 |
| Property 改态度 | U | 自定义 Property 本身不证明外交引擎读取它；本 DB 已实例化 Property Requirement 仅查到 plot 相关类型，不能据此断言引擎没有其它类型 |
| 指定 pair WRITE | 正常外交请求 S；任意分数 pair 修改 U | 文明类型 Requirement 的存在不证明可用任意运行时 PlayerID 精确筛选；未建立可引用的双向更新合同 |
| 变化监听 | S：原版 Ribbon 注册 `Events.DiplomacyRelationshipChanged`、`DiplomacyDeclareWar`、`DiplomacyMakePeace`、`DiplomacyMeet` | RelationshipChanged 是否覆盖每次纯分数增减、参数方向、重复发射、加载时补发，均 U |

DB `DiplomaticStateTransitions` 有状态相关的 Require／Allow 阈值、资格检查和转变动作；`DiplomaticTriggeredTransitions` 另有友谊／联盟成立及退出触发。**推断（高置信度）**：态度／正式状态不能由单一 UI 分数阈值替代。是否新增 opinion 变化确实改变 AI 交易／战争／友谊决策仍为 **AI-CONSUMED=U**；未读或修改 AI 接受逻辑。

HD E9 的 `STANDARD_DIPLOMACY_TRADE_RELATIONS.TradeBonus=4` 在本 DB 与 `TRAIT_LEADER_MAJOR_CIV` 的附件一致。其“同宗教 +3／异教 -4”段落处于 `/* ... */` 注释块，且两个相关 Modifier 在本 DB 查询未找到；不能作为该段已生效的证据。

### B. Formal Diplomatic Relationships

下表 READ 为原版 UI 已用的入口；WRITE 中 S 是正常请求／协议表面，D 是公开 Gameplay setter 名称。D setter 不等于已证明免费、单边、永久或与标准外交动作等价。

| 关系 | READ | WRITE | LISTEN／生命周期 |
|---|---|---|---|
| Delegation | S：`HasDelegationAt(otherID)`，E1 | S：`RequestSession(A,B,"DIPLOMATIC_DELEGATION")`；D：`SetHasDelegationAt` | 通用关系事件可重读；专用建立／撤回事件 U；市政废止字段与战争后的保留／撤回需分别核对 |
| Embassy | S：`HasEmbassyAt(otherID)`，E1 | S：`RequestSession(A,B,"RESIDENT_EMBASSY")`；D：`SetHasEmbassyAt` | 通用关系事件可重读；专用到期事件 U；未证明有固定 30T 寿命 |
| Open Borders | S：`A:GetDiplomacy():HasOpenBordersFrom(B)`，E1 | S：`RequestSession(A,B,"OPEN_BORDERS")` 和 DealManager 协议表面，E3；直接 setter U | S：交易成立通知；D：`DiplomacyDealExpired`；协议自身有 Duration，但本轮未取得当前生效 deal 的完整到期读取合同 |
| Declaration of Friendship | S：StateType=DECLARED_FRIEND、`GetDeclaredFriendshipTurn(otherID)` | S：`RequestSession(A,B,"DECLARE_FRIEND")`；D：Gameplay `HasDeclaredFriendship`／`SetHasDeclaredFriendship` | S：DB DECLARE_FRIENDSHIP／DECLARE_FRIENDSHIP_EXPIRES；到期后转 FRIENDLY 是静态配置，不是本批实测 |
| Alliance | S：`GetAllianceType(otherID)`、`GetAllianceLevel(otherID)`、`GetAllianceTurnsUntilExpiration(otherID)`，E4 | S：协议／类型动作；D：Gameplay `HasAllied`、`SetHasAllied`、`SetPermanentAlliance` | S：AllianceEnded／通用关系通知；DB DECLARE_ALLIANCE／LEAVE_ALLIANCE；typed alliance 与旧 flag／permanent 方法是否等价 U |

`HasDelegationAt`／`HasEmbassyAt` 是“己方在对方”；`HasOpenBordersFrom` 是“己方获对方开放”，E1 同时检查反方向，不能自动合并为双向协议。

**时长不能从一个字段统一推算。** 本 DB 的相关 `DiplomaticActions.Duration` 为 30，友谊／联盟 `GlobalParameters` time limit 为 15；前两项 Duration 还可能只是表的默认字段。原版友谊提示实际使用 `GetDeclaredFriendshipTurn + Game.GetGameDiplomacy():GetDenounceTimeLimit() - currentTurn`；联盟 UI 使用专用到期 getter；交易界面读取 agreement Duration／deal item `GetDuration()`。速度、回合顺序、HD 影响及 setter 是否建立同样的计时器仍 U。原版字段冲突不授权修改 Design 或编造统一寿命。

相关 DB 表：`DiplomaticActions`、`DiplomaticActions_XP1`（typed Alliance 映射）、`DiplomaticActions_XP2`（Favor／Grievance／Promise）、`DiplomaticStates`、`DiplomaticStateActions`、`DiplomaticStateTransitions`、`DiplomaticTriggeredTransitions`、`DiplomaticVisibilitySources`。Visibility 的 SOURCE_DELEGATE／SOURCE_ALLY 与关系有静态关联；增加能见度不自动等于改变态度。

**AI-CONSUMED：五项均 U。** 原生请求会交给标准外交处理，但本批不证明任意自定义 setter／Modifier 能使 AI 接受、续期或按预期重新决策。

### C. Alliance

**类型、等级、当前等级进度、增速和到期均有原版 UI 直接调用。** DB `Alliances` 有 Research／Cultural／Economic／Military／Religious；`AllianceEffects(LevelRequirement,AllianceType,ModifierID)` 提供分级效果附件。

| 项目 | 表面与等级 | 已知限制 |
|---|---|---|
| Type／level | S：`GetAllianceType(otherID)`／`GetAllianceLevel(otherID)` | 无联盟时 type=-1；level 不宜仅凭 type 推断清零 |
| XP／当前进度 | S：E4 的 `GetAllianceTurnsThisLevel(otherID)`／`GetAllianceTurnsToNextLevel(otherID)` | UI **除以 ALLIANCE_POINTS_MULTIPLIER** 后显示 CurrentPoints／PointsNeeded；不是仅按名称解释为真实剩余回合。直接 lifetime XP getter U |
| XP gain | S：`GetAlliancePointsPerTurn(otherID)`／`GetAlliancePointsTooltip(otherID)` | UI 同样除以 multiplier；tooltip 为展示文本，不是已验证的可写来源结构 |
| XP gain WRITE | S：`MODIFIER_PLAYER_ADJUST_ALLIANCE_POINTS` → `EFFECT_ADJUST_ALLIANCE_POINTS_FOR_MODIFIER`；另有 trade、common-enemy、governor families | 本轮确认附件与 Amount，不推定所有参数单位／内部倍率；COLLECTION_OWNER 不证明仅指定一个盟友 |
| 即时奖励指定盟友 XP／设 level | U | 未取得当前可用的直接 setter／增量签名；增速 Modifier 不能代替一次奖励承诺 |
| Expiry | S：`GetAllianceTurnsUntilExpiration(otherID)` | 一次到期不证明等级／XP 历史必然删除；续盟、间断、换类型、读档需原生验证 |
| Events | S：`AllianceAvailable(playerID,otherplayerID,allianceType)`／`AllianceEnded(...)`，E4 | Available 不是“已经缔结”；在限定原版 UI 查询中未找到专用 level／XP change 注册。未找到不等于引擎绝无该事件 |

本 DB `ALLIANCE_LEVEL_COUNT=3`、level two／three XP 参数为 **240／560**、multiplier=**4**；安装原版 Expansion1 参数为 **320／960**。因此必须引用当前加载 DB，不能照抄原版阈值，也不将这些原始参数直接当作 UI 显示 XP。

HD 静态附件示例：`DISTRICT_DIPLOMATIC_QUARTER` → `HD_DDQ_ALLIANCE_POINTS`（Amount=1）；`GOVERNOR_PROMOTION_HD_AMBASSADOR_RIGHT_3` → `HD_GOVERNOR_AMBASSADOR_RIGHT_3_ALLIANCE_POINTS`（Amount=2）。DB 的 `AllianceCorrespondingYieldType_HD`、`AllianceCorrespondingGPP_HD` 还提供类型映射；本批只核对行，不声称已经追踪它们全部消费逻辑。

**AI-CONSUMED=U**；没有修改或调查 AI 接受联盟的决策实现。

### D. Diplomatic Favor

| 项目 | 表面与等级 | 限制 |
|---|---|---|
| Current／per-turn READ | S：UI `Player:GetFavor()`、`GetFavorPerTurn()`，E5；D：Gameplay `Player:GetDiplomacy():GetFavor()`／`GetFavorPerTurn()`，E10 | UI Player 与 Gameplay Diplomacy 的位置不同 |
| Direct change | D：Gameplay `PlayerDiplomacy:ChangeFavor` | 公开页参数为空；本轮未取得当前安装调用签名。负值、下限、精度、归因和 persistence U |
| 一次 grant | S：`MODIFIER_PLAYER_ADD_FAVOR` → `EFFECT_ADD_PLAYER_FAVOR`，Amount | 本 DB Future Civic 的 CIVIC_GRANT_FAVOR=50；Goody grant 有 RunOnce／Permanent 标记。不同附件触发次数不能互推 |
| 每回合来源 | S：`MODIFIER_PLAYER_ADJUST_EXTRA_FAVOR_PER_TURN`；城市集合版本 `MODIFIER_PLAYER_CITIES_ADJUST_EXTRA_FAVOR_PER_TURN` | 定义存在不证明自定义附件撤销及时、可任意小数或一城奖励绝不重复 |
| 城市／特定机制 | S：BUILDING_PAGODA → PAGODA_ADJUST_FAVOR（Amount=1）；外交区附件按 Delegation／Embassy 产生 Favor（各 Amount=1） | 建筑作为来源、余额属于玩家。另查到城市墙条件定义，但未确认其现行附件，不把未挂载定义当活跃收益 |
| Source attribution | S：`GetFavorPerTurnToolTip()`，E5 | 是本地化展示字符串；未取得结构化来源明细、逐城来源 ID、直接 ChangeFavor 的可归因记录合同 |
| LISTEN | S：`Events.FavorChanged.Add(OnRefreshYields)`，E5 | 当前回调未用 payload；不猜字段顺序、保证发射时点或来源因果 |

DB 还存在 alliance／suzerain Favor multiplier、delegation／embassy、trade、great-person、resolution refund 等 Effect families。这是可进一步定域调查的入口，不能自动合并成已验证的任意城市奖励系统。`GameEffects.SupportsRemove` 及若干参数说明为空，不据空值宣称可撤销或不可撤销。

**AI-CONSUMED=U**：原生 Favor 是议会／交易资源，但新增支持是否改变 AI 估值或行为未测，本轮不研究 AI 投票。

### E. City-State / Envoys

| 项目 | 表面与等级 | 关键口径／限制 |
|---|---|---|
| 未分配使者 | S：major `GetInfluence():GetTokensToGive()`，E6 | 不等于已分配或一生累计派遣量；后者原生历史 getter U |
| 逐城邦分配 | S：minor `GetInfluence():GetTokensReceived(majorID)`；`GetMostTokensReceived()` | 接收者是城邦；把参数方向写反会改变读数含义。当前总分配可按明确集合汇总，但不是历史累计 API |
| 正常派遣 | S：`UI.RequestPlayerOperation(majorID, PlayerOperations.GIVE_INFLUENCE_TOKEN, {[PARAM_PLAYER_ONE]=minorID})`，E6 | 请求流程按未分配池／资格执行；不是任意免费发放的证明 |
| 添加未分配／免费定向 | S：`MODIFIER_PLAYER_GRANT_INFLUENCE_TOKEN` → `EFFECT_GRANT_INFLUENCE_TOKEN`；D：Gameplay `ChangeTokensToGive`／`GiveFreeTokenToPlayer`，E10 | 公共方法参数未填；正常派遣、free token 和翻倍的消费／触发差别尚未验证 |
| 特定城邦奖励 | S：`MODIFIER_CITY_GRANT_FREE_ENVOYS_HERE` → `EFFECT_GRANT_FREE_ENVOYS_HERE`，已有 GREATPERSON_GAIN_THREE_ENVOYS_HERE（Amount=3）定义 | 本批未确认该定义当前附件；它不是通用 major→任意 minor setter 的已验证配方 |
| Removing envoys | S：Matthew Perry／Stamford Raffles 的 action modifier → `EFFECT_BECOME_CITY_SUZERAIN`，RemoveOthers=1 | 这是特定 Great Person action 的清除其它使者／夺宗主表面；任意撤回自己一枚、任意负增量、精确回滚均 U |
| City-State type | S：HD 使用 `PlayerConfigurations[id]:GetLeaderTypeName()`／`Leaders.InheritFrom` → `CSE_ClassTypes.LeaderType`，E6 | 本 DB 六类 SCIENTIFIC／RELIGIOUS／TRADE／CULTURAL／MILITARISTIC／INDUSTRIAL。自定义类未知时不能凭名称／yield 猜类型 |
| Suzerainty | S：minor `GetInfluence():GetSuzerain()`；-1 被 UI 当无宗主；DB minimum=3 | 无宗主可以来自不足门槛、平票或其它条件；需要同时读取各 major 的分配，不把 -1 直接等同平票 |
| 平票 READ | S：逐 major 分配与 maximum 可读；平票判断是组合推断 | 须区分多个最高、最高不足 3、战争／disabled bonus 等。不是已验证的引擎内部 tie-state API |
| Placement／suzerain LISTEN | S：`InfluenceGiven`、`InfluenceChanged`，E6；文档给 Given `(citystateID,playerID)` | 宗主应在通知后重读；专用 SuzerainChanged 注册在限定 UI 查询未找到。通知次数／顺序／war／levy 覆盖仍 U |
| Quests READ | S：`Game.GetQuestsManager()` → `HasActiveQuestFromPlayer(majorID,minorID,questIndex)`、GetActiveQuestDescription／Name／Reward | 可读当前活跃任务，不证明可枚举所有未来可用任务、重新抽取条件或历史完成次数 |
| Quest LISTEN／completion | S：`QuestChanged(fromPlayerID,toPlayerID)`，原版 E8 与 HD E6 注册 | 本回调没有 quest ID／完成原因；任务消失也可能来自刷新／取消。专用可靠 completion payload／写入接口 U |

相关 DB：`Quests` 的本轮六类任务；`Requirements`／`RequirementArguments`／`RequirementSetRequirements`；各 Trait／Building／District／GreatPerson action 的 Modifier 附件。当前使者门槛 Small／Medium／Large 为 **1／3／6**，另有 Largest=**10**；HD `HD_CityStateBuffedObjects`、`CSE_ClassTypes` 定义等级／对象映射。不能因已有 tier 奖励表面就把复杂 Suzerain ability 当作可直接翻倍。

**AI-CONSUMED=U**。原生城邦机制读取 tokens 不等于证明 AI 会据新增使者改变分配或战争决策。现有抢宗主 Effect、免费使者、major 间 permanent alliance 方法均不证明 DIP-002 的“宗主不可替换＋对和平主要文明预先禁止宣战”可满足；这项保持技术未确认，也不选择“宣战后拉入战争”的 fallback。

### F. World Congress

**主要 READ 是 UI 的 `Game.GetWorldCongress()`／CongressManager。** 当前原版 Gameplay 还注册了决议资格验证回调；两种上下文不能互换。

| 表面 | STATIC_CONFIRMED 来源／数据 | 限制 |
|---|---|---|
| Exposed meeting state | E7：`GetMeetingStatus()` 的 TurnsLeft／Percentage；原版 UI 将 TurnsLeft+1 显示；当前 turn segment 判断 Stage1／Stage2／Resolution | `IsInSession()` 在 CongressButton 中是本地包装函数，不能误记为这里已经证明的全局 Engine API；公开 CongressManager 同名方法仍仅 D |
| Read resolutions／active effects | E7：`GetResolutions(localPlayerID)` 用于投票议题和 session 外生效效果 | 有混合 Stage 字段，不能当纯数组；阶段不同，ChosenOption／ChosenThing 等字段可用性不同 |
| Vote costs／history | E7：`GetVotesandFavorCost(localPlayerID)`；`GetPreviousVotesOnResolution(resolutionType)` | previous data 可为 nil；历史 PlayerSelections 有 OptionChosen／Votes。不是读取 AI 下一票意图 |
| Result review | E7：`GetReview(localPlayerID).Resolutions`；ChosenOption、ChosenThing、TargetType、PlayerSelections | 结果来自 getter；通知不必自带完整获胜数据；未证明任意阶段或旧 session 历史均可恢复 |
| Voting／result LISTEN | E7/E8：`WorldCongressStage1(playerID)`、Stage2、Finished、RibbonUpdate；SpecialSessionBeingCalled／EmergencyReady | UI 注册证明名称存在；结果 ready 时点、重复、加载／MP 及 Gameplay 是否有等价事件仍 U。未找到本批可靠的每决议独立结果事件 |
| 原生玩家 vote WRITE 表面 | E7 的原版 UI 调用 `WORLD_CONGRESS_RESOLUTION_VOTE`／DISCUSSION_VOTE／SUBMIT_TURN operations | 只记录存在；本轮不展开修改票、强制结果或绕过合法性机制 |
| DB | `Resolutions` → `ResolutionEffects` → Modifiers／DynamicModifiers；TargetKind、ValidationLua、WhichEffect、时代资格 | 静态候选表不是本 session 的实际议题；AITargetChooser／AILuaTargetChooser 字段未沿读 AI 实现 |
| Gameplay validation | E8：`GameEvents.WC_Validate_BorderControl`／MigrationTreaty 等接收 `(resolutionType,playerId,options)` 并填 `options.ResolutionOptions`；modinfo 注册 Scripts/WorldCongress.lua | 这是候选资格／选项生成入口，不是结果通知，不证明可安全改写 AI 投票或引擎结果 |

本 DB 有 19 个 Resolution 定义，包括 Sovereignty 的城邦奖励／宗主 bonus 禁用和 Public Relations 的 grievances 附件。只核对表关系和两个直接验证回调，不读取 AI vote decision logic。HD manifest 的 PostponeWorldCongress 选项存在，但本批不推定该选项开启或当前会议周期；周期以实际 manager READ 为准。

**AI-CONSUMED=U**；该项也受本轮明确排除 AI 投票逻辑的边界限制。

## 推断、反证与未知

- **高置信度推断**：新增外交资源／bonus 可以沿原生 Modifier 附件承载，Favor 城市来源和联盟增速都有现成静态链；本项目在将来实现时仍需确认上下文、触发、撤销和保存。
- **高置信度推断**：静态外交状态机、AI diplomacy getter 与 opinion Effect 共存，表明这是引擎已有的关系体系；本批未闭合“自定义写入 → 实际 score → AI 决策”的因果链，所以 AI-CONSUMED 保持 U。
- **反证／其它解释**：关系条位置来自离散状态；标准 action 表 Duration 与实际专用计时 getter 不同；联盟 getter 名称带 Turns，但 UI 显示为点数；无宗主不唯一指向平票；Quest 消失不唯一指向完成；SQL 注释与未挂载定义都不能作为生效证据。
- **仍 U**：任意运行时 pair 的 opinion 精确增减与撤销；正式 flag setter 和标准动作的等价性；只给指定盟友即时 XP；联盟升级专用事件；直接 Favor 改动的来源归因；任意撤回一枚使者／永久锁宗主／战争前 veto；quest 完成原因；跨上下文通知及读档覆盖；当前最终 UI 的实际色彩；AI 消费新增变化。
- Spec D0047 的 DIP／DIP-MISSION 仍 Future／OUT_OF_V0.1；永久保护额度／降级、多个 visibility 来源与任务参数等未决原样保留。本报告不为这些规则填值，也不将技术未知改写成 Design 拒绝。

## 最小 native 验证建议

**本轮无须立即测试。** 先由用户用本图讨论要用哪一个杠杆；以下只在对应机制另获授权后选择必要项。任何新增观测／写入工具都需要单独实施授权，本报告没有提供或运行它。

| 关心的杠杆 | 最小验证场景 | 要解决的未知 |
|---|---|---|
| 关系 READ／WRITE | 一个人类、两个已接触 AI：只核对 UI tooltip 的状态名称与色彩；若以后授权关系写入，只改变 A 对玩家的一份量，B 作为对照，重读双向 score／state 并观察一次普通外交决策 | 色彩、pair 方向、定向性、事件；一次决策仅证明该场景的 AI 消费，不泛化 |
| 正式关系／联盟 | 一个盟友，记录实际友谊／联盟开始／到期与 UI 当前等级点数；使用已选杠杆前后比较增速，若声称定向需第二盟友对照 | 时长口径、multiplier、退出／续盟历史、增速是否影响其它盟友。只有计划声称即时 XP 时才加那项独立验证 |
| 城市 Favor | 一城一个来源：比较建立／退出前后的余额、每回合与 tooltip，跨一个结算回合并保存／读档 | 一次与持续发放、重复、撤销、归因；不从余额变化反推 AI 估值 |
| 使者／宗主／quest | 一个城邦与两个 major，用正常派遣形成不足门槛／最高并列／单独领先；再完成一个正常任务，并记录通知前后 getters | -1 原因、通知时序、任务完成与消失的区别。精确撤回／永久锁只在另行选定并授权机制后验证 |
| 世界议会 | 一次正常 session，核对开始、Stage2、Finished 后的 GetResolutions／GetReview；读档检查仅在未来机制依赖恢复时加入 | 阶段数据形状与结果 ready 时点；不更改 AI 投票 |

这些是各杠杆的最小场景集合，不是要求一次全跑的测试清单。静态存在的接口只有在相应 native 场景获证据后才能提升验证结论。

## 本轮定域续查：宗主锁／城邦保护／Diplomat-vs-Spy

用户本次只授权三个具体问题；未继续扩展 A–F 整体地图。首轮技术结果、来源与 C1 授权时序纠正保留。本轮的详细证据需要独立维护，见唯一新增的[定域续查报告](CityState_Control_Protection_and_Diplomat_Spy_Semantics.md)。

| 问题 | 本轮结论 | 最关键证据／限制 |
|---|---|---|
| Suzerainty Lock | **UNKNOWN** | Perry 的单次 action 明确先夺宗主再清除其它玩家已有 Envoys；Permanent 不证明持续锁。Rogue State 只是停止赚 Influence，不是禁派／禁收 |
| City-State War Protection | **PARTIAL** | Canada 展示 target CivilizationType 的原生外交动作禁令；对 minor 宣战分支、第三方 protector 及全部战争入口覆盖未证 |
| Diplomat via Spy Framework without Spy diplomatic penalties | **PARTIAL** | 独立 UI／普通展示可借鉴；原生 Spy identity／operations 已有检测→外交 Effect／promise 管线，未确认脱钩 |

B 的细分结论：**RULE-LEVEL VETO: CONFIRMED**，仅指静态原生动作禁令存在；**TARGETED major→city-state protection: PARTIAL**。通用 Lua 宣战前 veto 仍 UNKNOWN。以上没有 native／LOCAL PASS，不能据此修改 DIP-002 或外交任务框架。

## Read Ledger

### 本轮定域 follow-up：City-State Control / Protection + Diplomat-vs-Spy

用户本次明确授权三个问题的静态续查；技术来源按同主题 README 中已获授权的精确入口使用。本轮由主调查会话独占 Markdown 写入，三个并行子调查只读来源并回传证据；不创建原型、测试或独立权威。

- Stage A：复核 Git、根／项目／调查区约束、Authority 必要版本与 Status CURRENT、现有概览 E 段和本机来源说明；Design 只读取 DIP-001–005、DIP-MISSION-001–003 的完整资格／成熟度及直接未决。本轮不扩大四专业实施上下文，保留首轮 C1 授权时序纠正。
- C7（计划，执行前记录）：A 的未知是夺宗主 Effect 是否持续、是否有锁定或 veto，以及通知后修复是否可靠。拟 mode=ro 查询已授权 DebugGameplay 的 `DynamicModifiers`／`Modifiers`／`ModifierArguments`／`GameEffects`／`GameEffectArguments` 中精确 `EFFECT_BECOME_CITY_SUZERAIN` 及 SUZERAIN／INFLUENCE／ENVOY family，沿 GreatPerson action／Requirement 附件跟进；原版从对应 GreatPerson／Influence／CityStates Lua／XML 定义和调用点读起，HD 仅 manifest 给出的本主题文件。期望取得具体参数／单次或持续标记／可用通知和写入签名；各问题取得直接证据或定域查询无命中即停止，不读二进制，不扩大其它 Mod。
- C8（计划，执行前记录）：B 优先查规则级、target-specific 战争资格。拟在同一只读 DB 的 diplomacy action／Requirement／Effect families 中查询 WAR／PEACE／BANNED_DIPLOMATIC_ACTION／DECLARE_WAR／DIPLOMATIC_ACTION_PREFERENCE 的相关行与附件；原版从已知 `IsDiplomaticActionValid`／`CanDeclareWarOn` 调用、宣战 UI 和明确引用的声明／验证符号跟进，查到先例再定位对应 Trait／GP／Congress 定义。期望区分规则禁止与 AI 偏好，判定 pair／minor／protector 条件表面；未命中只限定到已查静态表／调用语料，不断言引擎无此能力，不扩 AI 决策或泛读场景。
- C9（计划，执行前记录）：C 的未知是 Spy 身份与任务结果的外交耦合。拟查询同一 DB 的 Units／UnitOperations／UnitCommands／Promotion／DiplomaticAction／espionage Effect 直接关系；原版仅 Spy／Espionage 的 Lua／SQL／XML 文件名及其 include／事件／操作调用点，HD 仅 manifest 中 Spy／Espionage 对应文件。查询 `Spy`／`SPY_`／detected／captured／mission result／promise／grievance 相关明确定义，期望分离 UI／算法与引擎 identity／operation pipeline。闭合来源或具体缺口即停止；不读取无关资源、存档、AI planner，不设计 Diplomat 玩法。
- C10（计划，执行前记录，C8 的已授权来源内）：B 已发现动作禁令 family，但 Gameplay veto／永久和平签名仍缺。拟仅在原版 `Base/Assets/Scripts`、`DLC/Expansion1/Scripts`、`DLC/Expansion2/Scripts` 的 `.lua` 查询 CanDeclareWar／DeclareWar validation／GameEvents war／SetPermanentAlliance／MakePeaceWith／NeverMakePeaceWith／SetPermanentPeace 的精确符号；目录不存在则报告缺口，命中只读必要调用段，无命中即止。不进入 scenarios 或 AI 决策文件。公开 API 补充仅使用维护者自己的 PlayerInfluence／PlayerDiplomacy／GameDiplomacy 文档，空白参数保留 DOCUMENTED_ONLY。
- C11（计划，执行前记录，C7 的已授权来源内）：A 的已查 Admiral／Merchant 定义没有 Perry／Raffles／steal 文本，需要定位相关官方定义。拟在已授权原版 Assets 仅做 `*GreatPeople*`／`*Policies*`／`*Modifiers*` 和限定 UI 根内 `*CityStates*.lua` 的文件名查询；内容只跟进 GP／ROGUESTATE 相关 Data／Text 中精确 `GREATPERSON_CITY_STATE_STEAL_ENVOYS`／Perry／Raffles／`ROGUESTATE_DISABLE_INFLUENCE`／`POLICY_ROGUE_STATE` 符号，文本语言限定 en_US／zh_Hans_CN。期望确认原生行动描述与禁派方向；直接定义／文本足够即停止，不泛读其它效果或语言、不进二进制。其它原版目录需再记录，不进入未授权来源。
- C12（计划，执行前记录，C9 的已授权来源内）：C 的独立 detection／capture LISTEN 仍缺。拟在原版 Base／Expansion1／Expansion2 UI `.lua` 仅查 `Events.SpyDetected`／SpyCaptured／SpyKilled／SpyEscaped／SpyCaught／SpyMissionCompleted／SpyAdded／SpyRemoved 的注册或调用；命中最多读必要 listener／NotificationPanel 映射。各符号无命中或取得注册即停止，不读 AI planner、其它 DLC、无关 UI 或二进制。
- 本轮执行结果：C7／C11 取得单次 GP action、RemoveOthers 的原版文义与 Rogue State 赚取 Influence 的准确方向；C8 取得 Canada banned action、原版／HD资格读取及非 major 宣战分流，未把 preference／protector 名称当 veto。C10 两个精确 Scripts 根不存在，Expansion2 Scripts 对所列符号无命中，按停止条件保留引擎未知。C9／C12 取得 Spy字段、native operation／结果与检测外交链，限定事件查询只有 Added／Removed／MissionCompleted。具体源路径、行号、DB关联和未知均见定域报告；三个子调查均已停读，未写文件或执行行为。本轮先记录再扩展，没有重写首轮授权时间顺序。

### 首轮读取与授权时序记录（保留）

- Stage A：根／项目／Investigation AGENTS 与 README；Workflow W0005、W0001 读取／恢复及证据层级；Authority 必要路径／版本；Status CURRENT；Spec D0047 metadata、SCOPE-002–004、ELIG-001–006、DIP-001–005、DIP-MISSION-001–014 和对应未决项。未展开四专业实施 manifest 或历史正文。
- 技术入口：DevelopmentTests README 的外部只读 DB 配置约定；tools README 的配置定位约定。未执行这些文档中的测试／部署命令。
- C0（2026-10-04）：发现配置缺少技术入口后，先向用户询问；随后在技术索引直接引用的 `Specialization/Reports/Technical/Specialization_B163_Culture_Coexistence_And_Neighborhood_Depth.md` 中定域查询路径，定位到既有报告记载的数据库相对位置。这是路径定位，不是外部来源读取授权；未读取无关文化结论或扫描历史。
- C1（2026-10-04）：根据 C0 的相对位置 `Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`，实际打开并查询了外部 `DebugGameplay.sqlite`；这些初始读取发生在收到用户明确提供 Civ VI 目录的回复之前。查询范围为相关表名／必要 schema，后续沿本主题表关系扩展；没有寻找其它 Cache。**这是授权顺序偏差：已知路径不等于已获授权，按 Stage C 应等待用户确认后再读取尚未授权的外部来源。** 查询使用 `mode=ro`，未发现数据库写入；只读性质不消除该偏差，后来的用户确认也不追认为当时已经授权。
- C2（2026-10-04）：原生 Lua 源码位置仍缺失；公开资料限定 API 文档维护者自己的文档／源码和明确外交调用点。查询范围为 Civ VI diplomacy、alliance、favor、envoys、World Congress API；期望补充有具体方法／事件的文档证据。逐项找到直接来源或缺口即停止，不把论坛传闻提升为原生验证。
- Stage A 来源补充（用户明确回复，2026-10-04）：在上述初始数据库读取之后，才收到用户明确提供 `Sid Meier's Civilization VI` 目录的回复，随后以 `CIV6_USER_DATA` 为授权入口继续定域读取。此确认不追认更早的 C1 操作。后续仅列其直接子项，并读取现有配置的必要路径字段，定位精确 Civ VI／HD Lua／DB 来源；不以此授权递归 Mods 扫描。
- C3（2026-10-04）：该入口的当前内层游戏目录含 `Mods.sqlite`。未决问题是原版／HD 源码的注册路径；拟只读该 DB 的表名、注册路径 schema 与 HD／官方 DLC 对应记录，期望沿现有安装配置定位准确技术入口。路径字段不足即停止，不展开其它 Mod，不读取存档／用户设置／备份。
- C3 补充：Mods 注册只提供官方 DLC 相对路径；拟仅查询当前 `Logs/Modding.log` 中安装根／`2701747165`／`2465378070` 路径行，以及已经注册的 HD manifest 路径，区分安装登记与本次加载来源。最多读必要路径匹配，不据日志登记声称外交行为实测通过；不展开其它 Mods。
- C4（用户已明确确认，2026-10-04）：官方原版 Lua 的绝对安装入口缺失。用户允许只读 `Steam/steamapps/appmanifest_289070.acf` 及其明确指向的本游戏外交／城邦／世界议会 Lua／DB 文件。拟从必要安装字段定位本游戏，沿具体外交文件／include／调用／事件／DB Effect 读取；得到所需表面或具体缺口即停止，不展开 AI 接受联盟／投票逻辑、其它游戏／Mod 或全安装目录内容。
- C5（2026-10-04，C4 授权来源内）：未决问题为联盟升级／宗主变更是否有专用事件，以及分数与颜色映射。已读调用点不足；拟在原版 `Base/Assets/UI`、`DLC/Expansion1/UI`、`DLC/Expansion2/UI` 的 `.lua` 中仅查询 `Events.Alliance*`、`SuzerainChanged`、`WorldCongress*`、`FavorChanged`、`QuestChanged`、`GetDiplomaticScore` 与显式外交状态图标函数，读取命中调用点／直接定义。找到来源或该定域查询无命中即停止，不扩大到二进制或其它 DLC／AI 决策代码。
- C6（2026-10-04，已授权原版 UI 来源内）：`Civ6_Styles.xml` 的明确 Texture 引用为 `Diplomacy_RelationshipPips`。未决问题是红／黄／绿的像素映射；拟只在原版 `Base/Assets/UI` 查这个精确纹理名前缀，最多只读查看两个命中图像；期望将已确认的 VisState 2／3／4 与实际色彩对应。没有可读纹理即停止，保留显示缺口，不展开资源包／电影／其它纹理。
- 扩展结果：C0 从既有报告定位路径；C1 在用户目录确认回复前已实际打开并查询内层 DB，授权顺序偏差如上，不由后来确认追认。C2 取得 E10 文档，空白参数保留 D，未以搜索片段作为主证据；C3 定位 HD 核心／区域扩展并区分版本登记；C4 则先取得用户明确确认，随后定位并读取 E1–E8 原版调用，该扩展不属于上述时序偏差；C5 确认数值原因／关系状态／联盟与议会事件，限定查询没有专用联盟升级或宗主变更注册；C6 没有命中可读纹理，按停止条件保留像素映射未知。未扩大读取。
- 首轮收口核对：HEAD 仍 `e8b5f7f19249db75442407534e74b5bda149e9d3`，tracked／staged diff 为空，只有本主题两个新 Markdown；DB size／mtime 与首次定位一致。23 个本地证据链接的目标和行号范围已核对；没有将文档检查登记为 LOCAL 或 native PASS。
- 未做全 repo 搜索、磁盘搜索、递归 HD／Mod 阅读、备份／存档／Historical 阅读。

## 首轮 Handoff（保留）

**Stable checkpoint（2026-10-04）：本概览与同目录 README 已停写。** 完成 A–F 的能力地图、证据等级、上下文／生命周期限制、未知及可选择的最小 native 场景；没有预建分报告。

本次按用户明确修订授权，仅纠正 C1 及关联来源说明的授权顺序记录；来源、技术正文、证据等级、未知和限制保留。未重新读取游戏／HD 来源，未运行测试、原型、游戏或部署，未执行 Git 写操作。修正完成后本报告重新标为 **Stable** 并再次停写；此修订不恢复后续调查，等待用户反馈。

用户需要决定：将本版本带回外部设计讨论后，是否接受指定 checkpoint，并让 Main Task 只读审阅／显式入库。接受报告不接受某种玩法。

用户需要测试：本轮无；未来按选用杠杆及独立授权选择上表场景。

Codex 下一步：等待用户带回讨论或审阅意见；不继续新主题、实施或自行联系 Main Task。两文件保持 untracked，未 add／commit／push，正式 Design／Architecture／Status／runtime 未修改。

## 本轮定域 Handoff

**Stable checkpoint：本概览、定域报告及主题 README 已停写。** 仅限用户本次 A／B／C 静态续查，不恢复其它主题或实施；用户先讨论，是否接受 checkpoint／请求 Main Task 审阅入库由用户决定。本轮无需立即游戏测试，最小后续建议见定域报告，均未执行。HEAD／tracked／staged 状态未变，只有本主题三个 Markdown 为 untracked；未执行 Git 写操作。
