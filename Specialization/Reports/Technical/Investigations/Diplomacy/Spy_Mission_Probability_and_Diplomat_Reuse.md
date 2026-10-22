# Spy Mission Probability and Diplomat Reuse

Investigation / Non-authoritative / No design decision implied

Status: Stable
Maintainer: General Investigation Agent (root is the sole report writer; delegated evidence reads only)
Scope: native / current HD Spy mission probabilities, difficulty / level modifiers, Gain Sources / Counterspy state, outcome boundaries, and non-Spy technical reuse. No abilities, gameplay decisions, AI audit, prototype, tests, game launch, save changes, deployment, or Git writes.
Reading baseline: develop `e27897d3c1fb7ab04f01079c9ca989a1d306e190`; Authority D0049 / S0457 / B173.200. Starting tracked / staged / untracked state clean. Implementation activity belongs to Main Task.

## Executive summary

Native Spy odds are queried with **UnitManager.GetResultProbability(operation.Index, actualUnit, targetPlot)**. The exposed Lua adds the two initial-success categories and rounds to an integer percentage. Mission metadata and level-oriented bonuses are visible, but the probability formula, tier lookup, roll sequence and clamping are native-hidden in the inspected chain. No exact tier probability table is established here. [E1–E3]

**90% is not a verified universal cap.** Neither the native nor HD probability presenter clamps to 90; native text explicitly describes Gain Sources and Listening Post as automatically successful. The maximum for risky missions, and whether effective bonuses can exceed a displayed plateau, remain UNKNOWN. A configured maximum Spy level is not a probability ceiling. [E1–E5]

HD changes mission difficulty / duration parameters, the configured rank limit from 4 to 5, the promotion tree, and defensive bonuses. A vanilla community odds table cannot establish current HD odds. Gain Sources exposes player-and-city keyed timed state; Counterspy has district targeting and additional scope / level modifiers. They carry more state than a standalone completion roll. [E3–E7]

For a non-Spy Diplomat, the native helper's applicability is **UNKNOWN**; an exact independent copy of the native calculation is **not supported by current evidence**. Independent arithmetic / lookup, display patterns and separate difficulty inputs are technically reusable concepts, without adopting native Spy operations. Their probability values, cap and gameplay meaning are user decisions. Native operations retain detection / escape / capture and diplomatic coupling risks. [E1, E2, E8, E9]

Evidence labels: **STATIC_CONFIRMED** means read source / loaded DB configuration; **DOCUMENTED_ONLY** means a documented intention or incomplete external API record; **INFERENCE** means a reasoned technical conclusion; **UNKNOWN** remains unproved. No prototype, local test or native gameplay observation was performed for this report.

## Confirmed mechanics and tables

### Probability query, presentation and the 90% question

| Question | Evidence / answer | Boundary |
|---|---|---|
| Discrete tiers or continuous formula? | Integer mission parameters, ranks and level bonuses exist; a common native helper returns fractional outcome probabilities | Exact transformation / tier values / continuous versus threshold model UNKNOWN. UI color bands are not probability tiers |
| Actual odds for each tier? | No tier-to-probability lookup or executable probability formula is exposed in the inspected Lua / DB chain | Community table not accepted or reconstructed from labels |
| 90% display clamp? | STATIC_CONFIRMED: none in native or HD Support; display = floor(100×(success-undetected + success-must-escape)+0.5) | A hypothetical raw probability near 90% can round to 90%; this does not establish an engine cap |
| Universal 90% maximum? | DOCUMENTED_ONLY native intentions include automatically successful Gain Sources / Listening Post; UI handles success=100 | Risky-mission ceiling / native override / guaranteed-task result vector still untested |
| Can bonuses exceed an internal/displayed maximum? | HD and vanilla configure level-oriented bonuses; no verified saturation formula | UNKNOWN; stacking and a max-level constant do not prove odds above 90% |
| Does the display match real success? | It directly aggregates the helper's initial-success categories, then rounds | Not empirical frequency validation, undetected success, safe return or final UI Success |
| Does duration affect odds? | UI calls GetTimeToComplete separately; mission rows / promotions have separate time and probability fields | No explicit Lua time→odds formula; internal dependency UNKNOWN |

GetResultProbability is a native boundary, not a Lua implementation. The visible calls supply a registered operation **Index**, a real selected unit and a plot. No argument permits an arbitrary difficulty / probability / relationship / synthetic level bundle. Native operation requests use **Hash**; Index and Hash should not be conflated. The chooser validates with CanStartOperation and checks GameInfo.Units[unitType].Spy. [E1, E2]

Support colors use thresholds >85 / >65 / >45 / >25 solely for presentation. Popup sums initial-failure categories separately and shows capture-or-death as **100 minus the two already-rounded displayed totals**. That residual is not an exact native capture/death split. HD's Support retains these calculations; its only difference is an added rank-5 name branch. Expansion1/2's named chooser override changes destination enumeration, not this formula; the final loaded UI/VFS winner was not tested. [E1, E2, E7]

### Currently loaded mission definitions and difficulty inputs

`B / L / E / EL` below mean **BaseProbability / LevelProbChange / EnemyProbChange / EnemyLevelProbChange**, raw integer columns. They are **not established percent values**, a documented dice distribution, or an independently executable formula. A zero B for a support operation does not mean 0% success. Vanilla comparison uses installed Base + Expansion1/2 definitions; loaded HD columns use the current read-only DB. All rows are VisibleInUI=1, but actual eligibility still requires a valid native unit / city / district and CanStartOperation. Turns are nominal DB values, not guaranteed speed- or promotion-adjusted duration. [E2–E4]

| Operation (UNITOPERATION_SPY_ prefix) | TargetDistrict / native city fallback | Turns vanilla→loaded | B vanilla→loaded | Loaded L / E / EL | Loaded Offensive |
|---|---|---:|---:|---|---:|
| Steal Tech Boost | Campus | 8→4 | 14→10 | 3 / 0 / 5 | 1 |
| Great Work Heist | Theater Square | 8→6 | 15→13 | 3 / 0 / 5 | 1 |
| Siphon Funds | Commercial Hub | 8→8 | 13→14 | 3 / 3 / 5 | 1 |
| Sabotage Production | Industrial Zone | 8→6 | 14→17 | 3 / 3 / 5 | 1 |
| Disrupt Rocketry | Spaceport | 8→16 | 15→20 | 3 / 6 / 5 | 1 |
| Breach Dam | Dam | 8→6 | 15→18 | 3 / 3 / 5 | 1 |
| Foment Unrest | No specified district; city fallback | 8→4 | 13→11 | 3 / 0 / 5 | 1 |
| Neutralize Governor | No specified district; city fallback | 8→8 | 14→19 | 3 / 3 / 5 | 1 |
| Fabricate Scandal | No specified district; native eligibility | 16→8 | 13→13 | 3 / 0 / 0 | 1 |
| Gain Sources | City | 8→2 | 0→0 | 0 / 0 / 0 | 1 |
| Listening Post | City | 8→4 | 0→0 | 0 / 0 / 0 | 0 |
| Counterspy | Chosen own district | 16→16 | 0→0 | 0 / 0 / 0 | 0 |
| Travel New City (deployment) | Native destination city | 3→0 | 0→0 | 0 / 0 / 0 | 0 |

Vanilla risky rows above use L=1; E/EL=3/1 except Fabricate Scandal's 0/0. HD's relevant edits are in DL_Units.sql, and the loaded DB confirms the final values. Recruit Partisans is deleted from current UnitOperations, even though Types / old or generated modifier definitions may remain. It is not a currently available mission row. Travel's Turns=0 does not prove instant travel: native helpers separately calculate travel and establishment. [E3, E4]

Target plot is an explicit probability input, so treating odds as only mission type + rank is unsupported. The engine decides how to consume city properties, security, defensive modifiers and district eligibility. Visible evidence includes Gain Sources' city state, Counterspy targeting and modifier scope; this report does not reconstruct all city-security consumers or reward eligibility. [E1, E2, E6]

### Levels, promotions, Gain Sources and Counterspy

Native Overview reads spy:GetExperience():GetLevel() for rank presentation; completed history supplies LevelAfter. Mission-specific chance effects carry OperationType, Offensive and Amount, while time effects carry OperationType and ReductionPercent. Native / HD descriptions interpret chance Amount as operating **as if additional levels experienced**, not percentage points. The inspected UI does not calculate XP→rank progression or rank→odds. [E1, E6]

| Mechanism | Installed vanilla reference | Current loaded HD configuration | Qualification |
|---|---|---|---|
| Configured maximum / promotion layout | ESPIONAGE_MAX_LEVEL=4; base11 + E1 three + E2 three Spy promotions, their DB Level=1 | MAX_LEVEL=5; 20 promotions, five at each Level1–4; no Spy prerequisite rows; HD UI uses custom row unlock state | Promotion-tree tier, experience rank and temporary effective-level bonus are distinct; final effective-level clamp UNKNOWN |
| Gain Sources bonus | ESPIONAGE_BONUS_GAIN_SOURCES=2 | Same 2; operation Turns2, duration multiplier6 versus vanilla3 | Native text intends a temporary improvement to offensive operations in the same city; internal composition with rank / promotions UNKNOWN |
| Tech / Heist / Siphon / Foment / Scandal chance promotions | Typical mission-specific Amount2 | Amount3; attached through Burglar / Swindler / Persuader promotions | EFFECT_ADJUST_UNIT_SPY_OPERATION_CHANCE / COLLECTION_OWNER; OperationType + Offensive=1 + Amount, not +3 percentage points |
| Rocket / Sabotage / Governor / Dam chance promotions | Amount2 | Amount5, grouped by Elite Demolitionist | Same level-oriented chance family; no established conversion to an exact percent |
| Mission time promotions | Linguist ReductionPercent25 | Transfiguration15; Linguist20 | Separate EFFECT_ADJUST_UNIT_SPY_OPERATION_TIME; each attaches 11 current modifier rows including Gain Sources and an obsolete Recruit Partisans definition. Not proof of combined35% reduction |
| Global boosts from a Spy at home | Quartermaster Amount1; E2 Polygraph defensive Amount1, native text conditioned on home territory | Cryptographer reuses Quartermaster Amount2 and Polygraph Defense=1 / Amount2, both explicit home-territory requirement | These are global/all-Spy bonus definitions; requirements do not explicitly require an active Counterspy operation |
| Inquisitor defensive global boost | No equivalent in this exact base promotion comparison | SPY_INQUISITOR_ENEMY_LEVEL, Defense=1 / Amount3, home-territory requirement | HD English prose says2; source / loaded DB say3. Preserve discrepancy, use3 only as configuration |
| Human defensive bonus | No counterpart in the inspected native promotion chain | Palace → HD_SPY_LOVE_AND_PEACE, player bonus Amount6 / Offense0 / Permanent1, SubjectRequirementSet PLAYER_IS_HUMAN | Human-gated defensive configuration; active instance / actual odds / survival not tested |
| Counterspy district protection | Native text: selected district and adjacent districts; Seduction has defensive operation chance Amount2 | HD Polygraph promotion inherits Surveillance entire-city coverage plus adjacent-level boost1; native Seduction promotion removed | Separate coverage effects, not a probability table; exact distance boundaries / overlaps remain untested |

Multiple relevant definitions can apply: a Spy has a native rank, a mission-specific promotion, city Gain Sources state and qualifying global boosts; HD's custom tier UI allows access to later rows. **Their simultaneous representation does not prove additive effective levels**, multiplication of success probabilities, priority, duplicate-spy stacking, or what happens beyond MAX_LEVEL. The same warning applies to the 15% and 20% time modifiers. [E3, E6, E7]

**Gain Sources lifecycle:** the native chooser and Overview call player:GetDiplomacy():GetSourceTurnsRemaining(city), displaying the bonus only when positive. This confirms a player/city-addressed timed READ surface, rather than an exposed unit-attached Lua modifier. The native briefing says automatic success, offensive-operation bonus in this city for a duration, and no Spy risk. HD's comment says12 turns, but actual multiplier6 and nominal mission Turns2 are definitions, not a verified duration formula under speed / time modifiers. GetOperationDetailText and GetTimeToComplete remain native. Sharing by replacement Spies, moving / death / capture, timer refresh versus extension, ownership changes and reload cleanup are UNKNOWN. No Gain Sources state setter was found in the inspected HD UnitAbilities script's exact-symbol query. [E2, E5–E7]

**Counterspy lifecycle:** chooser uses native eligible district plots and submits Counterspy with district X/Y. Baseline district/adjacent scope is documented in native text; entire-city and adjacent-level extension effects are distinct. Remaining time is unit:GetSpyOperationEndTurn()−currentTurn; Counterspy / Listening Post are classified renewable and cancelled through native operations. This involves location, duration, coverage and defensive bonuses; exact comparison with an attacking Spy's rank / mission and overlapping defenders is hidden. [E1, E2, E6, E8]

**Representative target-city security carrier:** current BUILDING_CONSULATE attaches CONSULATE_SPY_BONUS → COLLECTION_PLAYER_CITIES / EFFECT_ADJUST_CITY_SPY_BONUS, Amount1. Its TEST_ANY requirement accepts a city with Consulate **or** Encampment. This establishes a conditional city-target bonus definition; its numeric contribution to the native probability formula is not computed here. A separate LOCAL_INFORMANTS_SPY_DEFENSE_BONUS definition has Amount3 but no current GovernorPromotionModifiers attachment in the query, so it is not presented as an active governor ability. The city-security example is loaded-DB evidence, not an attribution of every change to HD. [E3]

## Outcomes, HD differences, and reuse

### Success / failure is not the complete outcome

GetMission(playerID, missionID) yields native history with Operation, InitialResult, EscapeResult, LootInfo and level fields. **outcomeDetails.Success is calculated by the Lua presenter**, not an observed native mission.Success field. [E1, E8]

| InitialResult | EscapeResult used by presenter | UI Success | Description meaning |
|---|---|---:|---|
| SUCCESS_UNDETECTED | Not used | true | Initial success, undetected |
| SUCCESS_MUST_ESCAPE | FAIL_MUST_ESCAPE | true | Initial success, detected, escaped |
| SUCCESS_MUST_ESCAPE | KILLED / CAPTURED | false | Description still identifies initial success, then death / capture |
| FAIL_UNDETECTED | Not used | false | Undetected initial failure |
| FAIL_MUST_ESCAPE | FAIL_MUST_ESCAPE | false | Detected failure, escaped |
| FAIL_MUST_ESCAPE | KILLED / CAPTURED | false | Detected failure, death / capture |
| KILLED / CAPTURED | Not used | false | Direct death / capture outcome |

Counterspy has a separate presenter branch marked Success=true. A success requiring escape counts toward the preview success percentage but may later appear with UI Success=false after capture/death. Thus initial completion, survival, undetected completion and retained rewards must not be merged into one probability. Reward settlement / reversal is not established by these UI branches. [E1, E8]

The escape UI exposes a pursuing spy / police, exit route travel times, an escaping-Spy queue, and SET_ESCAPE_ROUTE submission. This establishes a separate escape **state and decision stage**. It does not reveal whether the engine uses one combined random draw, multiple rolls, their order, independence, or the exact conditional/joint distribution. Escape parameters are visible (base10, level boost1, counterspy-level modifier−1, correct-police modifier−4); HD's alternative values are commented out and do not change the loaded values. [E3, E5, E8]

### Diplomatic consequence boundary

Current DB and native definitions confirm:

> TRAIT_LEADER_MAJOR_CIV → STANDARD_DIPLOMATIC_ESPIONAGE → COLLECTION_MAJOR_PLAYERS / EFFECT_DIPLOMACY_ESPIONAGE, with triggered REQUIREMENT_ESPIONAGE_DETECTED.

Parameters are ModifierPerTransgression=−5, ReductionTurns=15, ReductionValue=1, MessageThrottle=20 and WARNING_STOP_SPYING_ON_ME. The warning definition has an AI initiator. GS's DONT_SPY promise action has FavorCost=30, refusal grievances=25 and incursion grievances=25. These are **STATIC_CONFIRMED configurations**, not proof that every detected/captured/killed result necessarily applies all penalties or prompts a promise. The native producer mapping each result to detection / incursion is UNKNOWN. [E9]

Popup can hide a consequence frame for a failure-and-escape combination which Support describes as detected. This is presentation, not an exemption from the detection requirement. Renaming a unit / UI, choosing a non-offensive operation, or copying the native mission request cannot establish immunity from the Spy pipeline. The prior [Spy semantic boundary report](CityState_Control_Protection_and_Diplomat_Spy_Semantics.md) remains unchanged. [E8, E9]

### Technical reuse assessment

| Route | Assessment | Evidence / conditions |
|---|---|---|
| A. Call the native probability calculator for a non-Spy/custom mission | STATIC_CONFIRMED helper exists in Spy UI; non-Spy/custom applicability UNKNOWN | Observed arguments require actual unit / registered operation / target plot. No arbitrary parameter interface or verified Gameplay-context contract; calling the getter is not equivalent to executing a mission, but qualification remains unproved |
| B. Reproduce the exact native calculation independently | Evidence insufficient | Display aggregation / rounding can be copied; full tier mapping, formula, clamps, city-security composition and outcome distribution cannot be derived from the exposed constants alone |
| C. Independent simpler probability system | INFERENCE: technically feasible without native espionage state | Independent lookup/arithmetic can accept explicitly supplied difficulty and other inputs, cap odds, and separate timer / result presentation. This is a concept, not a selected rule, implementation or exact native reproduction |

The API maintainer's [UnitManager page](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager) lists the queries as UI methods; [GetResultProbability](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager.GetResultProbability) leaves arguments / returns unspecified and provides no formula. This is DOCUMENTED_ONLY support; the installed call sites provide the concrete signature evidence. It does not license synthetic unit tables, custom operation parameters or non-Spy use. [E10]

Low-coupling concepts: a distinct difficulty input, probability display, optional discrete lookup, progress display and separate completion result. High-risk dependencies: actual Spy identity / capacity, native SPY_* operations, espionage state, counterspy, detection / escape / capture and promise pipeline. Copying ordinary math or UI alone does not register a Spy (INFERENCE); adopting native operations lacks an established exemption. No new Diplomat ability is proposed.

### Six future-design questions: technical boundary only

| Question | Technical evidence / answer |
|---|---|
| Should missions use discrete success tiers? | User design decision. An independent lookup is straightforward; the native formula / tier values remain unverified |
| Is an independent 90% cap straightforward? | Yes, as an explicit independent numerical bound (INFERENCE). That would be a chosen rule, not a recovered native universal maximum |
| Can mission difficulty be separated from Spy experience? | Independent inputs can be separate (INFERENCE). Native operations already store mission parameters separately, but their combined calculation is hidden and not exposed as arbitrary caller inputs |
| Can relationships / Alliance levels be alternative inputs without Spy identity? | Their existing READ surfaces are present: GetDiplomaticStateIndex(otherID) and GetAllianceLevel(otherID) [E11]. Independent arithmetic need not register a Spy (INFERENCE); context, refresh and weights still require a separately approved contract |
| Can guaranteed and probabilistic missions coexist? | Independent systems can branch (INFERENCE); native text already describes automatic-success support missions. No decision about which future mission belongs in either category |
| Must execution-period benefits require a completion roll? | No such general technical requirement was found. Native Listening Post text describes visibility while running and automatic success; independent execution effects / completion rolls can be separate (INFERENCE). Native lifecycle rules are not a compulsory custom-unit template |

## Unknowns and minimal future validation

**Unresolved:** exact tier probabilities / formula; risky-mission 90% or other ceiling; effective-rank aggregation / saturation; strength or coverage of all city security; internal time dependency; the outcome RNG and reward-retention distribution; Gain Sources sharing / removal on move, death, ownership change or reload; custom / non-Spy native helper eligibility; a complete immunity / de-registration mechanism. No native PASS is claimed.

Recommendations only, requiring later separate authorization:

1. **Read the raw native result vector in a controlled existing Spy scene** for one risky mission / fixed target while changing one rank-oriented input at a time, with Gain Sources and Counterspy conditions recorded. Compare raw vector, UI rounding, effective inputs and native duration. A raw success sum >0.90 would falsify a universal risky-mission 90% ceiling for that scene; saturation at 0.90 in one scene would not prove a global cap. Avoid using only color or rank labels as tiers.
2. **Only if route A remains attractive, perform a non-Spy helper contract check** in an isolated fixture: accepted unit / operation / plot and return structure, without requesting a Spy operation. A valid query would prove only that read surface for the fixture, not mission execution, save lifecycle or penalty immunity. Failed / unsupported input is not permission to register the Diplomat as a Spy.

Existing completion records can check that preview categories / history / UI differ as described; a few successes cannot validate statistical odds or independent rolls. No large outcome-frequency campaign, complete Spy AI audit or mission prototype is made a requirement here.

## Evidence roots and Read Ledger

Snapshot: GAMEPLAY_DB 33,112,064 bytes, mtime **2026-10-08T21:26:01.943380−07:00**; Steam appid289070 / buildid15296837; HD manifest id521b8777-0977-4859-a5ee-3e411a732e5c / version2.2. A DB definition is not a native instance or current save observation. Exact source references below are root-alias-relative; private machine paths and raw original source copies are not included.

| Evidence | Precise source / query keys |
|---|---|
| E1 Probability / result presentation | CIV_ASSETS Base/Assets/UI/EspionageSupport.lua L27–64,97–110,123–190,219–225; Popups/EspionagePopup.lua L70–76,193–245,270–320 |
| E2 Native eligibility / city state / deployment | CIV_ASSETS Base/Assets/UI/Choosers/EspionageChooser.lua L109–122,193–235,370–374,404–408,421–428,450–458,630–638,741–754; PartialScreens/EspionageOverview.lua L416–423,639–640 |
| E3 Current loaded DB | PRAGMA table_info(UnitOperations); UNITOPERATION_SPY_% exact rows, UnitOperations_XP2 Spy-row query; GlobalParameters ESPIONAGE_% keys; Spy UnitPromotions / UnitPromotionPrereqs / UnitPromotionModifiers→Modifiers→DynamicModifiers→ModifierArguments / requirements; current city-spy bonus families→BuildingModifiers / GovernorPromotionModifiers and CITY_HAS_CONSULATE_OR_ENCAMPMENT TEST_ANY. No AI operation tables read |
| E4 Vanilla mission data | CIV_ASSETS Base/Assets/Gameplay/Data/UnitOperations.xml L105–114; DLC/Expansion2/Data/Expansion1_UnitOperations.xml L10–54; Expansion2_UnitOperations.xml L12 |
| E5 Native state / guarantee descriptions | CIV_ASSETS Base/Assets/Gameplay/Data/GlobalParameters.xml L266–278; Base/Assets/Text/en_US/Espionage_Text.xml L59–63,215–216,282–283. Text establishes intended mechanics, not native test PASS |
| E6 Native promotion / effect references | CIV_ASSETS Base/Assets/Gameplay/Data/UnitPromotions.xml L308–318,2233–2321,2328–2397,2399–2411,2488–2492; Base/Assets/Gameplay/Data/Modifiers.xml L1710–1712,1720–1722; Base/Assets/Text/en_US/Promotions_Text.xml L769–770; DLC/Expansion2/Data/Expansion1_UnitPromotions.xml L12–14,48–88; Expansion2_UnitPromotions.xml L50–52,587–621; Expansion2_Modifiers.xml L1258–1265; DLC/Expansion2/Text/en_US/Expansion2_Promotions_Text.xml L98–99 |
| E7 HD changes | HD_CORE DL.modinfo L2,924–946,1785,1807–1809,1947–1949,2213–2217; UpdateDataBase/DL_Units.sql L61–86,108–166; DL_GlobalParameters.sql L15–23,288; DL_UnitPromotions.sql L978,1042–1081,1093–1117,1134–1135,1149–1158,1171–1182; Texts/HD_Text_UnitPromotions.sql L166,180–196; UI/Replacement/EspionageSupport.lua L27–64,100–103 (only content change versus native is rank5 label); UI/Replacement/HD_PKSpyUnitPromotionPopup.lua L27–44,292–317; Gameplay/UnitAbilities.lua L518,575 for inspected listeners, not probability formula |
| E8 Completion / escape stages | CIV_ASSETS Base/Assets/UI/Popups/EspionagePopup.lua L383–435,449–455,472–483,624; Popups/EspionageEscape.lua L1–72,73–138. Named filename query found Base escape Lua/XML only in Base/E1/E2 UI roots; no exposed escape-probability formula in the read Lua |
| E9 Detection / opinion / promise | GAMEPLAY_DB exact STANDARD_DIPLOMATIC_ESPIONAGE / ON_ESPIONAGE_DETECTED / REQUIRES_ESPIONAGE_DETECTED / DIPLOACTION_KEEP_PROMISE_DONT_SPY chains; CIV_ASSETS Base/Assets/Gameplay/Data/Leaders.xml L997,1275–1279,2811–2850,5651–5654,6277–6280,6470–6474; Modifiers.xml L2304–2307; DiplomacyStatements_Warning.xml L443–452; DLC/Expansion2/Data/Expansion2_DiplomaticActions.xml L5 |
| E10 Public primary API record | API maintainer's UnitManager / UnitManager.GetResultProbability pages linked above, read2026-10-09; UI context recorded, signatures / formula incomplete, DOCUMENTED_ONLY |
| E11 Alternative relationship / Alliance inputs | CIV_ASSETS Base/Assets/UI/DiplomacyActionView.lua L869–874; DLC/Expansion1/UI/Replacements/DiplomacyActionView_Expansion1.lua L51–60. Rechecked exact getters already cited by prior report; no AI behavior audit |
| Repository context | [Existing Spy boundary](CityState_Control_Protection_and_Diplomat_Spy_Semantics.md) C section, unchanged; [current Spec](../../../../Design/Specialization_v0.1_Design_Spec.md) DIP / DIP-MISSION L347–414. Future framework context does not authorize new mechanics or implementation |

### READ / WRITE / LISTEN / AI-CONSUMED

| Label | Established scope |
|---|---|
| READ | Native UI GetResultProbability / GetTimeToComplete / GetMission / GetSourceTurnsRemaining(city) / GetExperience():GetLevel; actual method execution was not performed |
| WRITE | Existing Spy RequestOperation / cancellation / SET_ESCAPE_ROUTE call sites; no calls executed, no safe non-Spy substitution proved |
| LISTEN | Native SpyMissionCompleted refreshes history; HD UnitPromoted and custom offensive-mission listener exist; not proof of native RNG / calculation stages |
| AI-CONSUMED | Static detected-espionage diplomatic Effect / AI warning chain. AI mission selection and custom Diplomat consequences UNKNOWN and outside the audit |
| UNKNOWN | Exact probability formula / tier values, clamps, stacking, complete lifetime / distribution / custom-helper contract |

- `REPO`: current canonical develop checkout; repository references use relative links.
- `GAMEPLAY_DB`: previously authorized current Civ VI Cache/DebugGameplay.sqlite, SQLite `mode=ro`; loaded definitions, not save / live state.
- `CIV_ASSETS`: previously authorized installed Civ6.app/Contents/Assets, only named / referenced Lua and Gameplay definitions.
- `HD_CORE`: previously authorized Workshop core 2465378070, starting at DL.modinfo. No implicit access to other Mods or whole parent directories.
- Stage A completed: project / Investigation rules and navigation, Authority metadata / Status CURRENT, Diplomacy README and the existing Spy semantic boundary section; current Spec DIP and DIP-MISSION full sections. Their future framework is context, not new implementation or design authority.
- C-SPY-P1 (planned before reading): old report identifies native EspionagePopup.lua / EspionageSupport.lua and UnitManager helpers; exact probability remains unresolved. Read only those files / direct includes, the named EspionageChooser / Overview necessary calls, and their directly referenced success / result symbols. Query the authorized DB schema for spy / espionage / operation tables and exact UnitOperations / GlobalParameters / result or difficulty relationships. Goal: expose UI helper inputs / returned categories, installed probability constants or formula, duration and cap boundaries. Stop at native-hidden calculation; no binary reverse engineering, AI planners, or whole Assets scan.
- C-SPY-P2 (planned before reading): current versus vanilla difficulty, promotion, Gain Sources and Counterspy configuration needs direct evidence. Read HD DL.modinfo first, then its explicitly named spy / espionage / promotion / relevant unit files, and native Gameplay definitions referenced by DB rows. Query only necessary mission rows, Spy promotions / modifiers / requirements / arguments, spy probability / rank / duration GlobalParameters. Goal: compact current mission and modifier tables plus state lifetime evidence. Stop at directly relevant definitions / helper calls; no whole HD, other professions, or unrelated unit audit.
- C-SPY-P3 (planned before reading): existing report establishes Spy detection / diplomacy and outcome fields but not distribution. Follow native EspionageSupport / Popup mission-result callbacks and exact DB detected-espionage opinion / promise / grievance chains. Check primary API maintainer docs for the exact probability helpers / mission records found in source; public primary sources only. Goal: staged outcome representation, consequence triggers and non-Spy callable boundary. Stop when engine producer / formula is unavailable; no inferred joint distribution from UI labels, no custom operation execution.
- C-SPY-P4 (planned before reading): Base UI delegates probability to native UnitManager; current expansion overrides may change the presentation. Search only exact EspionageSupport.lua / EspionagePopup.lua / EspionageChooser.lua filename patterns within the authorized DLC/Expansion1/UI and DLC/Expansion2/UI roots, including their named suffix variants; follow direct include / replacement references. Goal: compare the actual installed expansion UI chain, without asserting final VFS winner. Stop after these matches and direct references; no broad Assets symbols or unrelated UI.
- C-SPY-P5 (planned before the additional inventory / remaining file read): C-SPY-P3 followed the Popup event to Base escape queue / route fragments; number / order of native rolls remains hidden. Query filename patterns *EspionageEscape* in Base/Assets/UI and DLC/Expansion1/UI / Expansion2/UI only, then read the remaining necessary route UI. Goal: determine whether there is a separate exposed escape query / variant, not infer a complete distribution. Stop at native request / helper boundary. The exact relationship / Alliance getters cited in the prior report were separately rechecked under Stage B in DiplomacyActionView.lua / DiplomacyActionView_Expansion1.lua; they were not read under a later plan.
- C-SPY-P6 (planned before reading): target-city security inputs are not fully represented by mission metadata and Spy promotions. Within the already authorized DB, inspect Spy Effect family names / collections, then only city-target security families and a few direct building / district / governor attachments with their arguments / requirements. Goal: demonstrate whether target-specific difficulty carriers exist, not build a world security / policy / AI audit. Stop after representative exact chains and the native consumption gap; no new external source root or all-modifier dump.
- No community probability table accepted in advance. New external local directories require user confirmation; precise path gaps are reported without disk scanning.

Execution checkpoints, after the plans above:

| Checkpoint | Reads actually completed / stop |
|---|---|
| C-SPY-P1 | Native Support / Popup / chooser probability calls, DB mission columns / exact Spy rows and espionage parameters; no source formula / tier odds table exposed. Stopped at UnitManager native boundary |
| C-SPY-P2 | HD manifest-selected Spy sections of unit / global parameter / promotion / text / UI files and necessary direct UnitAbilities symbols; native corresponding definitions; loaded attachments / arguments / requirements. Confirmed configuration changes and text discrepancy, not effective odds or all lifecycle behavior |
| C-SPY-P3 | Completed-history categories, Base escape queue / route fragments along the direct UI chain, current detected-espionage / promise DB chain, primary API maintainer pages. No result→diplomatic-producer mapping or independent RNG proof |
| C-SPY-P4 | Exact-name/suffix UI inventory in E1/E2 found only EspionageChooser_Expansion1.lua variants; they alter target lists. HD manifest independently named Support replacement, checked separately; only rank5-name difference. No final VFS/native test |
| C-SPY-P5 | Root completed the additional Base/E1/E2 escape filename inventory and remaining Base Lua lines after recording this plan. Only Base Escape Lua/XML matched; no separate escape probability formula exposed. Relationship / Alliance getters were earlier direct Stage B reads, not retroactively authorized by this plan |
| C-SPY-P6 | Spy Effect family names / collections, then only two city-spy bonus definitions and their direct building / governor / requirement relationships. Consulate conditional city carrier verified; no complete security / policy / governor / AI audit |

Not performed: whole Assets / HD / repository scans, source binaries, unrelated Mods, historical records, save / personal configuration reads, AI selection logic, a community-table adoption, formula fitting or statistical gameplay experiments. Source originals / DB were read only; only this new report and its necessary Diplomacy README navigation are written.

## Handoff

Stable / stopped, 2026-10-09. Text, relative links, evidence identifiers and absence of private machine paths checked; DB size / mtime and reading-baseline HEAD unchanged at closure. Only this new report and necessary topic navigation were edited; older Stable reports, formal sources and runtime remain untouched. No tests, prototypes, game launch, deployment or Git writes.

Exact native tier odds / risky cap / stacking and non-Spy helper validity remain UNKNOWN; independent technical concepts are available, no Diplomat mechanic selected. Stop at native helper / producer boundaries and the described bounded source checks. Native testing, if ever wanted, requires a separate user-authorized task; current Main Task batches are not extended. Stable marks this evidence checkpoint, not native PASS, user acceptance or Design authority. Wait for user discussion; no further investigation or implementation starts automatically.
