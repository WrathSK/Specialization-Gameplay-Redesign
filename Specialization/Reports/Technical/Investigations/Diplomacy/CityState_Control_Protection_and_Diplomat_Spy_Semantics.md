# City-State Control / Protection + Diplomat-vs-Spy Semantics

> Publication note: machine-specific prefixes have been replaced with source labels; technical conclusions, evidence scope and historical observations are unchanged. `CIV_ASSETS` denotes the installed `Civ6.app/Contents/Assets`; `WORKSHOP_289070` denotes Civilization VI Workshop content, with each following numeric directory identifying its published item; `CIV6_USER_DATA` denotes the configured Civilization VI user-data root. Suffixes and line references preserve the original source location. These are source locators, not public links or shell variables.


Investigation / Non-authoritative / No design decision implied

Status: Stable
维护者: General Investigation Agent（主会话统一写入；三个子调查只读取证）
范围: 仅持续宗主锁、城邦宣战前保护、Spy 框架复用的身份／外交后果。无玩法设计、实施、原型、测试、游戏启动、部署、AI logic 修改或 Git 写操作。
依据: develop `e8b5f7f19249db75442407534e74b5bda149e9d3`；Authority D0047／Status CURRENT S0430。入口使用用户已明确补充的本机路径；不追认首轮 C1 的更早读取。首轮记录保留在[概览](Diplomacy_Surface_Overview.md)。

独立维护原因：概览已有约 2.6 万字符；本轮三个问题分别需要维护 GP action、战争资格及 espionage result 的证据链。概览保留简明结论与本报告入口，本主题不再新增其它分报告。

## 最重要的结论

1. **Suzerainty Lock: UNKNOWN** — 已证一次夺宗主并清除其它玩家已有使者，未证持续锁定或宗主变更前 veto。
2. **City-State War Protection: PARTIAL** — 原生定向外交动作禁令存在，指定城邦、第三方保护者及全部战争入口的覆盖未证。
3. **Diplomat via Spy Framework without Spy diplomatic penalties: PARTIAL** — 独立 UI／普通展示可借鉴，真实 Spy 身份／原生任务管线免外交后果的脱钩未证。

此处 CONFIRMED／PARTIAL 只评价下述静态证据覆盖，**不是 native PASS**。本轮没有新增 LOCAL_SIMULATION_PASS 或 USER_GAME_TEST 证据。

## 证据与来源口径

- **S / STATIC_CONFIRMED**：本轮读取的原版／HD 定义、附件、Lua 调用或事件注册。它不证明本项目调用后原生成功。
- **D / DOCUMENTED_ONLY**：API 维护者文档记录；空白参数和版本差异不能填成已验证签名。
- **UNKNOWN**：尚无足够证据。区分“本次限定检索未找到”“某张已查静态表没有匹配行”和“闭源引擎能力未知”，不合并成“不支持”。
- **AI-CONSUMED**：原版 AI warning 的静态承载路径可以记录；新增保护／Diplomat 的实际 AI 决策与执行依然 UNKNOWN。
- 当前加载定义 DB 为 `CIV6_USER_DATA/Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`；仅 `mode=ro`。本轮定位时 size=25,255,936 bytes、mtime=2026-10-04 20:01:18 America/Vancouver，与首轮记录一致。它不是存档实时状态。
- 原版与当前加载定义分开报告。例如当前 Raffles 附件和 Canada trait 附件有差异；不由差异猜是哪一个 Mod 改动，也不扫描其它 Mod 找归属。

## A. Stable / Locked Suzerainty

### Confirmed facts

**A1：目前确认的是一次行动改变使者和当下宗主；持续锁定未确认。**

当前 DB 的完整已加载链如下；“完整”只限定这条查询链，不指完整引擎参数签名：

| 环节 | 已查定义 |
|---|---|
| DynamicModifier | 唯一对应 `MODIFIER_UNIT_BECOME_CITY_SUZERAIN` → `COLLECTION_OWNER` → `EFFECT_BECOME_CITY_SUZERAIN` |
| Modifier | 唯一对应实例 `GREATPERSON_CITY_STATE_STEAL_ENVOYS`；`RunOnce=1 / NewOnly=0 / Permanent=1 / Repeatable=0` |
| Requirement／stack | 该实例 Owner／Subject RequirementSet、StackLimit 均 NULL |
| 已用参数 | `RemoveOthers=1`；本轮未查到该实例其它参数 |
| Action 附件 | Matthew Perry 与 Stamford Raffles；target=`GREAT_PERSON_ACTION_ATTACHMENT_TARGET_UNIT_GREATPERSON`，各 1 charge，须位于城邦领土 |
| 参数／撤销元数据 | GameEffects 的描述、Context／Subject interfaces、SupportsRemove 等为空；GameEffectArguments 无该 Effect 行。空白不证明参数不存在或能安全撤销 |

原版 Babylon 定义中，Perry 的该 action、RunOnce／Permanent 和 RemoveOthers 参数均可直接核对：family (`CIV_ASSETS/DLC/Babylon/Data/Babylon_GreatPeople.xml:90`)、单次标记 (`CIV_ASSETS/DLC/Babylon/Data/Babylon_GreatPeople.xml:325`)、参数 (`CIV_ASSETS/DLC/Babylon/Data/Babylon_GreatPeople.xml:760`)。

**RemoveOthers 的语义有直接原版文义：先给予足够使者成为此城邦宗主，再移除所有其它玩家的使者。** 这支持“清除当前已有 Envoys”，而不是从 Effect 名称猜测。原版行动说明 (`CIV_ASSETS/DLC/Babylon/Text/en_US/Babylon_GreatPeople_Text.xml:93`)没有给出以后不得再派使者的持续禁令。

原版该 action 附件只有 Perry；Raffles 的原版行动资格 (`CIV_ASSETS/DLC/Babylon/Data/Babylon_GreatPeople.xml:131`)不同。当前加载 DB 则将同一 steal Modifier 也挂到 Raffles。后者不能称为未经修改的原版先例。

**A2：已找到邻近机制，但没有闭合成宗主锁。**

| 机制 | STATIC_CONFIRMED | 不能推出的结论 |
|---|---|---|
| Rogue State | `POLICY_ROGUE_STATE` → `ROGUESTATE_DISABLE_INFLUENCE` → `MODIFIER_PLAYER_DISABLE_INFLUENCE / COLLECTION_OWNER / EFFECT_ADJUST_DISABLE_INFLUENCE`，Disable=1，RunOnce=0／Permanent=0 | 原版说明是**停止赚取新使者所需 Influence**，不是禁派已有使者、城邦禁收或锁定宗主 |
| 在此城邦送 3 Envoys | `MODIFIER_CITY_GRANT_FREE_ENVOYS_HERE / EFFECT_GRANT_FREE_ENVOYS_HERE`，已有单次 Amount=3 的 GP 定义 | 当前加载 DB 的已查附件表未找到仍使用该实例的 action carrier；不能保证任意 Gameplay 定向增发 |
| 联盟共享宗主 | `ALLIANCE_SHARE_SUZERAIN` → `EFFECT_ALLIANCE_SHARE_SUZERAIN`，经济联盟 Lv3 附件，RunOnce=0 | 共享表面不是持续维持某一 major 的宗主身份 |
| 宗主门槛 | `INFLUENCE_TOKENS_MINIMUM_FOR_SUZERAIN=3` | 这是全局参数，未取得逐城邦 threshold override |

Rogue State 的政策 Modifier (`CIV_ASSETS/DLC/Expansion2/Data/Expansion1_Policies.xml:472`)、Disable 参数 (`CIV_ASSETS/DLC/Expansion2/Data/Expansion1_Policies.xml:1453`)及原版说明 (`CIV_ASSETS/DLC/Expansion2/Text/en_US/Expansion1_Civics_Text.xml:153`)区分了“赚取”与“派遣”。没有按 DISABLE_INFLUENCE 名称推定禁收方向。

本次 SUZERAIN／INFLUENCE／ENVOY Effect／Requirement family 查询**未找到**直接的持续 suzerain override、变更前 veto、特定 rival→minor 派遣禁令或逐城邦 threshold setter。这只限定到已查 family，不声称所有静态文件或闭源引擎中都不存在。

**A3：事件后修复的静态组件部分成立，自动维持的技术可靠性未建立。**

| 能力 | 等级与直接证据 | 限制 |
|---|---|---|
| READ 各 major Envoys／宗主 | S：minor `GetTokensReceived(majorID)`、`GetMostTokensReceived()`、`GetSuzerain()`；循环 AliveMajorIDs。原版调用 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:1451`) | 当前计数可重读；无宗主 -1 不能单独解释为平票 |
| READ eligibility | S：major `CanGiveInfluence()`／`CanGiveTokensToPlayer(minorID)`、minor `CanReceiveInfluence()` | 是资格查询，不是可注册 veto 或可写 eligibility setter |
| LISTEN | S：`InfluenceChanged`／`InfluenceGiven` 注册；可见面板的回调调用 Refresh。注册 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:1823`)、回调 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:1708`) | 支持“收到 UI 通知后重读”的用法；不保证 Gameplay 同步、批量变化后的最终状态或所有原因均发事件 |
| WRITE 普通派遣 | S：本地 UI 请求 `GIVE_INFLUENCE_TOKEN`，PARAM_PLAYER_ONE=目标 minor。调用 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:758`) | 需已有可派 Envoy 与资格；不是免费自动补发 |
| WRITE 免费定向／重夺 | S：GP action 配置；D：Gameplay `GiveFreeTokenToPlayer` 文档；自动稳定写入 UNKNOWN | 原生 GP action 不能直接当作任意 major/minor 脚本接口；社区文档参数为空，限定 HD 调用点未找到签名 |
| AI-CONSUMED | UNKNOWN | 原生 count／action 配置不证明自动 fallback 的 AI 竞争／执行行为 |

HD citystates replacement 保留上述读取／派遣／监听表面：逐 major 读取 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:2090`)、派遣 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:1028`)、监听 (`WORKSHOP_289070/2465378070/UI/Replacement/citystates.lua:2601`)。UI 的 `SetGivingTokensConsidered` 仅有面板时机调用，不计为规则锁。公开 [PlayerInfluence 文档](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerInfluence)仅作为上下文／名称记录，缺参数部分仍 D。

### Inference

- **高置信度**：一次退休 charge、RunOnce 和原版行动文义支持“当下改变 Envoys”的解释；Permanent 标记不能升级成“永远不会被夺宗主”。
- **高置信度**：若仅按使者数量恢复领先，必须同时达到门槛并严格超过最大 rival；平票不够。这是算法条件分析，不是新的 Gameplay 决定，也不是引擎保证。
- **高置信度**：变化后修复不等于变更前 veto。宗主易主、收益或征兵相关通知可能已先发生；本轮没有证明能让这些中间状态对其它系统不可见。
- 多 AI／批量派遣／双倍奖励、重复或递归回调可能导致追补升级；“接近就补”也可能使竞争不收敛。不能确认这只是抽象层面的脆弱。

### Unknown

RemoveOthers 后别人能否立即重派；内部发放数量算法与重算顺序；可靠免费定向 WRITE 签名／成功确认；GamePlay 事件覆盖、同步与最终读数；AI 连续变化、同回合重入、reload／多人、战争、城邦消失／解放；真正永久／protected suzerainty。

**Fallback 判定：静态组件 PARTIAL，自动维持的技术可靠性 UNKNOWN。** 本轮不能把它写成已确认可实现的宗主锁。

## B. City-State War Protection

### Confirmed facts

**RULE-LEVEL VETO: CONFIRMED（S：原生外交动作禁令存在；不表示通用 Lua veto 已确认）。**

**TARGETED major→city-state protection: PARTIAL（有目标文明类型禁令候选，完整保护未确认）。**

原版有两个独立的规则禁令 family：定义 (`CIV_ASSETS/DLC/Expansion2/Data/Expansion2_Modifiers.xml:452`)。

| Modifier／Effect | 原生 Canada 配置 | 已知作用方向 |
|---|---|---|
| `MODIFIER_PLAYER_ADJUST_BANNED_DIPLOMATIC_ACTION` → `EFFECT_ADJUST_BANNED_DIPLOMATIC_ACTIONS`，COLLECTION_OWNER | `TRAIT_NO_SUPRISE_WAR_FOR_CANADA`：Banned=true、DiplomaticActionType=SURPRISE_WAR | 限制持有者自身的特定外交动作 |
| `MODIFIER_PLAYER_ADJUST_BANNED_DIPLOMATIC_ACTION_SPECIFIC_CIVILIZATION` → 同尾缀 Effect，COLLECTION_OWNER | `TRAIT_NO_SUPRISE_WAR_ON_CANADA`：CivilizationType=CANADA、DiplomaticActionType=SURPRISE_WAR；挂 `TRAIT_LEADER_MAJOR_CIV` | 对指定文明类型的定向禁令；不是只有全局禁战 |

以上 action／civilization 值完整 ID 分别为 `DIPLOACTION_DECLARE_SURPRISE_WAR`／`CIVILIZATION_CANADA`，见参数 (`CIV_ASSETS/DLC/Expansion2/Data/Expansion2_Civilizations_Major.xml:591`)。当前 DB 保留这两个配置，但原版自身禁令的 Trait 附件与加载后附件不同；HD 的Canada 定义修改 (`WORKSHOP_289070/2465378070/UpdateDataBase/DL_Civilizations.sql:2364`)将其移至 `TRAIT_LEADER_LAST_BEST_WEST`。不将原版 trait 归属当作当前加载归属。

| READ／WRITE／LISTEN | 已确认表面 | 本轮边界 |
|---|---|---|
| READ S | `CanDeclareWarOn(targetID)` 被原版／HD 城邦 UI 用来禁用按钮；`IsDiplomaticActionValid(action,target,true)` 提供有效性／FailureReasons | 是规则资格 getter，不是可注册前置 veto |
| WRITE S | 原生 banned action Effect 配置、Trait 附件与定向参数 | 任意 target PlayerID／protector PlayerID 的 setter 未确认；未调用、未实施 |
| LISTEN S | `DiplomacyDeclareWar` 的已见 HD 消费回调 | 宣战发生通知不是宣战前允许／拒绝回调 |
| AI-CONSUMED | all-major trait 的静态规则配置已见；实际执行 UNKNOWN | 不证明所有 AI、单位攻击、团队／联盟带战入口均受候选城邦禁令覆盖 |

城邦 UI 的资格读取 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:1496`)与按钮禁用／Canada 提示 (`CIV_ASSETS/Base/Assets/UI/PartialScreens/CityStates.lua:1139`)是直接消费者。DiplomacyStatementSupport (`CIV_ASSETS/Base/Assets/UI/DiplomacyStatementSupport.lua:167`)处理另一条外交 choices 表面。

**同名函数陷阱：** DeclareWarPopup.lua 的 `CanDeclareWar` (`CIV_ASSETS/Base/Assets/UI/Popups/DeclareWarPopup.lua:39`)只判断目标是不是 FULL_CIV；它不是 GameEvent veto。随后 major 走 RequestSession，非 major 走 `UI.RequestPlayerOperation(...DIPLOMACY_DECLARE_WAR...)`。因此改 diplomacy choices／弹窗不能证明封闭城邦所有战争入口。

**名称含“保护／禁战”的邻近定义另行排除：**

- `REQUIREMENT_PLAYER_CITY_STATE_PROTECTOR` 的已查高／中保护及侵略实例，附件落在 `EFFECT_DIPLOMACY_SIMPLE_EFFECT`（例如 InitialValue=6／3）：这是态度评价承载，不是已证 immunity。
- Teddy 的 `TRAIT_NO_WAR_MINOR_CIV_HOME_CONTINENT` 与 Scotland 的 `AGENDA_FLOWER_OF_SCOTLAND_BAN_WARS` 落在 `EFFECT_ADJUST_DIPLOMATIC_ACTION_PREFERENCE`（Action、Favored=0）。本轮未取得这类 preference 到资格 veto 的调用证据，不因 NO_WAR／BAN 名称把它计为硬规则禁令。
- 原版及当前 DB 的 NO_INFLUENCE／INFLUENTIAL／MAX_INFLUENCE 状态均列有 DECLARE_WAR_MINOR_CIV，见静态状态动作 (`CIV_ASSETS/Base/Assets/Gameplay/Data/DiplomaticActions.xml:221`)。MAX_INFLUENCE 名称本身不等于永久免战；仍不代替全部 engine 资格判断。
- 当前 `ResolutionEffects → Modifiers → DynamicModifiers` 对 banned／WAR／PEACE families 的查询为 0 条附件。**这张已查加载静态表没有匹配行**，不扩大成“引擎没有任何此类能力”。

### Inference

- **高置信度**：Canada 是规则级动作禁令的原生先例，有 target CivilizationType 的表面；比改善 AI 好感更接近目标。
- **中等置信度候选**：将 specific-civilization family 用于城邦类型和 minor 宣战 action，可能成为定向规则保护的承载。原生实例只展示 Canada＋surprise war，minor 分支是否适用尚未确认。
- 没有原生附件证明“某保护者对侵略者和平”这一第三方关系与目标城邦可以组合为当前规则条件；不能自行补成完整保护设计。

### Unknown

通用 `GameEvents.CanDeclareWar`／宣战前验证 hook；targeted permanent peace／protected minor；SetPermanentAlliance 对 minor 的安全语义；CivilizationType 目标是否覆盖 minor／重复文明／指定 PlayerID；全部战争入口及第三方 protector 条件；撤销、重新附加、保存／读档时序。

C10 指定的 Base／Expansion1 Scripts 根不存在，未寻找替代；Expansion2 Scripts 中所列 war／peace／permanent 方法精确符号无命中。**这是本次定域 Lua 语料未找到可注册 veto**，不是证明引擎绝不支持。WorldCongress 的 WC_Validate 回调仅属议会资格。

### 事后 fallback（不等价）

`DIPLOACTION_DECLARE_PROTECTORATE_WAR.RequiresWarOnAlliedCityState=true` 是城邦已遭战争后的宣战资格；capture emergency 的 Trigger=CAPTURE_CITY_STATE、Goal=LIBERATE_CITY_STATE、WarOnTarget=1，是占领后的解放。已有宣战监听 (`WORKSHOP_289070/2465378070/Gameplay/CivilizationTraits.lua:1166`)也是事后通知。

公开 [PlayerDiplomacy 文档](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerDiplomacy)记录 MakePeaceWith／NeverMakePeaceWith／SetPermanentAlliance，但参数空白，保持 D；NeverMakePeaceWith 不能误当永久和平。宣战后结束战争／拉保护者入战不能撤回已触发的全部后果，不等于 DIP-002 的宣战前禁止；本报告不选择该 fallback。

## C. Diplomat-vs-Spy Semantics

### Confirmed facts

**C1：显式 Spy 标志和原生 operation／状态表面存在；没有取得引擎身份判定的完整实现。**

| 身份／框架层 | 证据 | 不能推定 |
|---|---|---|
| Unit 定义 | 原版 UNIT_SPY 有 `Spy=true`、PROMOTION_CLASS_SPY、civilian formation、IgnoreMoves；还有 CLASS_SPY tag。Unit 字段 (`CIV_ASSETS/Base/Assets/Gameplay/Data/Units.xml:769`)、tag (`CIV_ASSETS/Base/Assets/Gameplay/Data/Units.xml:715`) | 单位显示名称或 civilian 外形不能代替这些字段 |
| 当前加载身份 | `Spy=1 OR UnitType/PROMOTION_CLASS含SPY` 的已查结果只有 UNIT_SPY；General／Merchant／Scientist 的 Spy=0；未查到 UNIT_GREAT_DIPLOMAT 行 | 这不证明未来自定义单位只需改一个字段就控制全部 engine 语义 |
| UI collection | 普通 `GetUnits():Members()` 再按 `GameInfo.Units[..].Spy` 过滤。Overview (`CIV_ASSETS/Base/Assets/UI/PartialScreens/EspionageOverview.lua:88`) | UI 的过滤方式不是引擎独立 Spy collection／IsSpy／注册规则的完整证明 |
| HD 硬编码 | promotion popup 用 `UnitType == UNIT_SPY`。HD UI (`WORKSHOP_289070/2465378070/UI/Replacement/HD_PKSpyUnitPromotionPopup.lua:114`) | 注释掉的 PromotionClass 判定不能当运行规则；也不能由此说其它 Spy 类型绝不会被 native 识别 |
| 容量／offmap／俘虏 | Diplomacy 有 GetSpyCapacity／captured／offmap getters。Overview (`CIV_ASSETS/Base/Assets/UI/PartialScreens/EspionageOverview.lua:113`) | 没有取得独立 espionage manager 的注册／反注册 API |
| EspionageViewManager | 已读代码仅缓存当前 view city 和城市对象 | 不能将这个 Lua view 缓存误当引擎 espionage registration manager |

**C2：任务时长／部署／逃脱由原生操作承载；UI 不是独立的任务引擎。**

| 标签 | 原版直接表面 | 限制 |
|---|---|---|
| READ S | GetSpyOperation／GetSpyOperationEndTurn；GetTimeToComplete；GetTravelTime／GetEstablishInCityTime；GetMission(playerID,missionID) | 所见旅行／建立计算由 UnitManager native helpers 返回，没有可复制的完整 Lua 算法；非 Spy applicability UNKNOWN |
| WRITE S | CanStartOperation 后 RequestOperation(SPY_TRAVEL_NEW_CITY／mission hash)；SET_ESCAPE_ROUTE player operation | 只有静态调用证据，未执行；换名／换 UI 不证明脱离 engine 语义 |
| LISTEN S | SpyAdded、SpyRemoved、SpyMissionCompleted(playerID,missionID) | 三 UI 根精确查询未找到独立 SpyDetected／Captured／Killed／Escaped／Caught 注册；不是证明 API 不存在 |
| AI-CONSUMED | 静态检测 Requirement→外交 Effect→AI warning 声明链已见；新增 Diplomat 实际消费 UNKNOWN | engine producer／完整触发矩阵未取得，不能把每次任务结果都推成固定 AI 行为 |

旅行和建立时长的原生 helper 调用 (`CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:404`)、travel 请求 (`CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:606`)、mission 请求 (`CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:472`)和完成回调 (`CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:418`)属于同一原生状态管线。

任务记录有 Operation、InitialResult、EscapeResult；EspionageSupport 将 MUST_ESCAPE 描述为 detected，再区分 escaped／killed／captured，也有直接 killed／captured 的 InitialResult。结果读取／映射 (`CIV_ASSETS/Base/Assets/UI/EspionageSupport.lua:123`)。Counterspy、offensive mission、listening post、travel 是不同 operation；LISTENING_POST 的 Offensive=0 仍是 Spy operation，不能把“非 offensive”当成非 Spy 身份或免责开关。

**外交后果的直接静态链：**

`TRAIT_LEADER_MAJOR_CIV → STANDARD_DIPLOMATIC_ESPIONAGE → MODIFIER_PLAYER_DIPLOMACY_ESPIONAGE / COLLECTION_MAJOR_PLAYERS / EFFECT_DIPLOMACY_ESPIONAGE`

Subject requirement：`ON_ESPIONAGE_DETECTED → REQUIRES_ESPIONAGE_DETECTED → REQUIREMENT_ESPIONAGE_DETECTED（Triggered=1）`。当前 DB 参数为 ModifierPerTransgression=-5、ReductionTurns=15、ReductionValue=1、MessageThrottle=20、DiplomacyKey=WARNING_STOP_SPYING_ON_ME；这是一条现成外交承载链。原版 Requirement (`CIV_ASSETS/Base/Assets/Gameplay/Data/Leaders.xml:6470`)、Effect family (`CIV_ASSETS/Base/Assets/Gameplay/Data/Modifiers.xml:2304`)。对应 Warning 声明 (`CIV_ASSETS/Base/Assets/Gameplay/Data/DiplomacyStatements_Warning.xml:443`)有 Initiator=AI；这是静态消费配置，不是本轮 AI 实测。

GS 的 `DIPLOACTION_KEEP_PROMISE_DONT_SPY` 关联 PROMISE_DONT_SPY_ON_ME、FavorCost=30、GrievancesForRefusal=25、GrievancesPerIncursion=25，原版参数 (`CIV_ASSETS/DLC/Expansion2/Data/Expansion2_DiplomaticActions.xml:5`)与本轮 DB 一致。当前 StateActions 多种关系状态均静态允许该行动；这不证明每次 detected 都必然提出承诺或产生同量 grievances。

Popup 的被发现警告 (`CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:317`)按目标 `CanReceiveInfluence()` 区分非城邦，没有 FRIENDLY／DECLARED_FRIEND 的 UI 豁免判断。原版选择器还排除 ALLIED／同队目标 (`CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:169`)；GS replacement 另排除 Free Cities。继承此选择器会排除目标盟友，改 UI 过滤又不证明 native operation 会接受盟友或免检测。

HD 继续消费 SpyMissionCompleted 和 killed result，重置自己的 promotion locks：回调 (`WORKSHOP_289070/2465378070/UI/Replacement/HD_PKSpyUnitPromotionPopup.lua:321`)。它不是 Diplomat 脱钩先例。已查 UI 是读取／显示结果，不是 UI 自行发放外交惩罚。

### Inference：复用层级

| 分层 | 评价 | 条件 |
|---|---|---|
| 可能安全复用 | 独立列表／城市 owner/id、排序、banner、选择与进度显示样式 | 不请求 SPY operations，不依赖原生 Spy 容量／任务状态；“UI pattern”不包含已过滤后的合法目标集合 |
| 可能安全复用 | 自己已有 endTurn 后借鉴 endTurn−currentTurn 的普通显示式；所见 view-city 缓存 | 这里只说明展示式／普通缓存不自行注册间谍，不设计 timer 存储、任务或部署规则 |
| UNKNOWN | 距离／旅行／建立／任务时长 native helpers | 原版没有提供可复制完整算法；非 Spy 是否适用未证，不能直接列作安全通用框架 |
| 高风险复用 | 真正 Spy 身份、capacity／offmap／captured 管理、SPY_* 原生操作 | 已有结果与检测外交链；改 UnitType 名字／label 不证明隔离 |
| 高风险复用 | counterspy、detected／captured、escape、原生 mission lifecycle | 这些层有明确原生 outcome 与外交 Requirement 耦合；无已证全量免责开关 |
| UNKNOWN | 新 Spy 类型／promotion、custom native mission、显式注册／反注册或脱钩机制 | 静态字段／UI过滤不足以建立完整 engine 合同 |

**回答 C3：只能确认独立借鉴 UI／普通展示的边界；尚不能确认在保留 Spy identity／原生 espionage operation 管线时，让 Diplomat 不被外交系统按 Spy 处理。** 非 Spy custom unit 不因 Great Person 外形自动成为已证 Spy，但进入真实 Spy APIs 后的资格、容量和后果仍待验证。

### Unknown

完整引擎 Spy 身份 predicate／显式 IsSpy／registration；哪个 native producer、operation 与结果组合触发 REQUIREMENT_ESPIONAGE_DETECTED；友好／友谊／联盟的检测和 counterspy 条件；非 Spy 使用 native helpers 的合法性；custom peaceful operation 是否可避免整个后果管线；自动驱逐、关边、谴责的直接因果桥。已确认 warning／opinion／promise／grievance 静态承载，不能扩大为这些其它后果必然发生。

## Minimal native test suggestions

本轮未执行。用户先讨论是否采用这些杠杆；需要新增验证对象／诊断时，另行授权实施，不从本报告自动生成 prototype。

| 问题 | 最小后续场景 | 要区分的事实 |
|---|---|---|
| RemoveOthers／宗主锁 | 正常 Perry action 前后记录全部 major Envoys／宗主；随后另一个 major 再派一枚 | 清除已有使者与禁止以后派遣；数量和重算顺序 |
| 自动追补 | 只有未来选定并授权机制后，验证一城邦、两 major 的正常派遣／奖励／清除事件，回调读数与 targeted WRITE，再单次读档 | 通知先后、重复／递归、最终状态、eligibility；未有可靠签名前不声称能自动补发 |
| 规则保护 | 先以 Canada 的原生 ban 作基线；若未来授权最小 fixture，再用一个受保护／一个对照 minor、一个受限制／一个对照 major | 资格 getter、实际城邦按钮及单位攻击、一个 AI、团队／宗主带战；第三方 protector 条件与撤销／读档独立验证 |
| Spy 外交语义 | 原生 listening post 对照一项可能被发现的任务，记录 mission history、counterspy、warning／opinion、promise／grievances；友好条件单列 | 一次没被检测不是免疫；非 offensive 不等于非 Spy |
| 非 Spy helpers | 仅在以后另获授权的验证对象上核对 native travel／timer、容量／captured 是否纳入 | 不以静态 UI 过滤直接宣称 future Diplomat SAFE |

## Read Ledger

- Stage A／执行前 C7–C12 计划保留在[概览 Read Ledger](Diplomacy_Surface_Overview.md#read-ledger)。本轮先记录后读取；所有外部入口已由用户明确授权，此次不使用后来的许可改写首轮 C1。
- A：mode=ro 查询 become-suzerain／Influence／Envoy／Requirement family 及 GP／Policy／Alliance 附件；按 C11 文件名定位后只读 Babylon GP、Rogue State 的直接定义／en_US 文本、原版 CityStates include 链和 HD manifest 注册的相关文件。确认行动文义后停止。没有为找具体 WRITE 签名广泛扫描 HD／其它 Mod。
- B：mode=ro 查询 banned／war／peace／preference／protector／Emergency／Resolution 的必要关联；原版 Canada、城邦按钮、宣战弹窗／有效性调用及 HD 明确对应附件。C10 两个不存在 Scripts 根停止，存在的 Expansion2 Scripts 精确符号无命中；未进入场景或 AI 决策。
- C：mode=ro 查询 Units／UnitOperations／espionage Modifier／Requirement／promise 直接链；原版 Spy UI／include／operation／event，HD manifest 指定 promotion popup。C12 精确八事件查询闭合到三个注册，其它符号只报限定无命中；不读 AI planner 或二进制。
- 主会话另对 RemoveOthers 文义、Rogue State 文义、banned family／Canada 参数、宣战分流、Spy 完成结果／检测 Requirement 和当前 DB 关键行作只读交叉核对。公开 PlayerInfluence／PlayerDiplomacy／GameDiplomacy 文档仅作 D 补充。
- 未做全 repo 或磁盘扫描、递归通读 Assets／HD／其它 Mod、区域扩展无依赖读取、Historical／备份／存档／私人设置读取；未调用任何游戏写接口。
- 收口：三个子调查已停读；主会话核对关键原文／DB 行与 Markdown 链接、保留首轮时序记录。HEAD 未变，tracked／staged diff 为空，仅本主题三个 Markdown 为 untracked；未执行 Git 写操作。来源 DB size／mtime 与本轮初始定位一致。文档核对不登记为 LOCAL 或 native PASS。

## Handoff

**Stable checkpoint：本报告、概览和主题 README 已停写。** 本报告不接受或替换 Gameplay；DIP-002 与 DIP-MISSION 的正式规则／成熟度保持。未实施、未测试、未运行游戏或部署，未 add／commit／push。

用户需要决定：基于三个结论继续外部设计讨论，并决定是否接受指定 checkpoint／请求 Main Task 审阅入库。用户需要测试：本轮无；未来按明确选择与单独授权执行上表最小场景。Codex 下一步：等待用户反馈，不继续其它调查或实施，不自行联系 Main Task。Git 只读。
