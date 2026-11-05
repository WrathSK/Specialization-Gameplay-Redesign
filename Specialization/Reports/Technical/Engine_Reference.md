# Engine Reference — Architecture Convergence, first tranche

Reference only / no Design or Architecture authority. Maintainer: Primary. Evidence date: 2026-11-04.
Project baseline: develop `954dc67aca007082a5a164becdbafbacbad1403a`, D0058/A0183/S0866. Supported planning scope: current macOS Steam/Aspyr, Gathering Storm, existing official prerequisites and Leugi art-package dependency; not all rulesets/platforms or zero third-party dependencies.

This is a short question-based reference, not an API encyclopedia. Source inspection and archive integrity are **STATIC_CONFIRMED**. No new LOCAL_SIMULATION or USER_GAME_TEST was executed. A script call site proves usage, not the engine's complete contract or timing. Community/reverse-engineered material remains separately qualified.

## Source index and Raw locations

Local archive ID **ER-20261104** identifies sibling `Civ6_Engine_References/Tranche_2026-11-04`, outside the repositories. Its local `manifest.json` resolves source IDs to exact originals, hashes, commits, versions, paths, retrieval scope and licenses. Private machine paths stay there. Existing HD source ID **ENV-20261104** points into the completed environment backup; none of the HD package was copied again.

| Source IDs | Version / acquired scope | Applicable evidence and rights boundary |
|---|---|---|
| OFF-01–14 | Installed official macOS files; Steam15296837 / Aspyr1.4.6 / bundle376653.178; full selected Lua/manifests | Actual shipped consumers and conditional loading examples. Local proprietary source only; no redistribution permission inferred. |
| OFF-DEF-01–08 | Same installation, selected Base/GS Modifiers/Requirements/Buildings/Policies XML plus one official CivRoyale requirement example | Definition and content mapping evidence, not successful SQL assembly or behavior acceptance. |
| HD-08–18 | Exact HDv2.2 backup, Workshop2465378070; manifest references existing originals by path/hash | Definitions, input helpers, marker producer and UI wrappers; mixed-source notices remain; no copying HD economic implementation into core. |
| SUK-* | [Sukritact KB](https://github.com/Sukritact/Civilization-VI-Modding-Knowledge-Base/tree/144f27f5ea28c8a381f72343cad4c5ddbfb7c7b0), commit `144f27f5ea28c8a381f72343cad4c5ddbfb7c7b0`; eight selected files | Community documentation. No license file found at this tree; reference/paraphrase, no assumed code redistribution. TBD/incomplete signatures are not native proof. |
| HEM-* | [Hemmelfort notes](https://github.com/Hemmelfort/Civ6ModdingNotes/tree/aeb4e11dbf310d9ad4f87f7d15d01c229ae856a9), commit `aeb4e11dbf310d9ad4f87f7d15d01c229ae856a9`; four files including MIT license | Examples/collected community notes, not this project's native results. Root MIT does not erase mixed-source provenance. |
| CRU-* | [cru121 reference](https://github.com/cru121/civ6-gamecore-reference/tree/5af389445118bed2bdebf7a8a42b219c8fba5175), commit `5af389445118bed2bdebf7a8a42b219c8fba5175`; selected notes/pages/data and both licenses | Windows/symbol/Linux analysis and community-derived parameters. README17/34 ties analysed Steam15038592 GameCore to byte-identical Windows15296837; this is same-version, other-platform evidence, not analysis of the Aspyr binary. Documentation CC-BY4.0, code separately MIT; CE/DevCE absent from supported Mac scope; addresses not portable. |
| GCO-* | [Gedemon GCO](https://github.com/Gedemon/Civ6-GCO/tree/4a96120a5765480a4e04646927a09d893ba37d69), commit `4a96120a5765480a4e04646927a09d893ba37d69`; GameScript and Credits only | Actual mod implementation, not official behavior. No repository license found; local reference only, no redistribution assumed. |
| OWNER-* / DERIVED-HD-CLOSURE | Complete original supplied handoffs / small static extraction inventory | Owner instructions are authority for scope, not engine evidence. Derived inventory is explicitly not an original or runtime closure. |

Slothoth/Companion remain **link-only, not archived**; no specific CivFanatics primary post was needed/selected. Do not call the first tranche a complete backup of those sources. Sukritact and cru event parameter records share community ancestry; agreement is not independent validation. Local Raw and hashes alone are not a permanent off-machine backup.

## ER01 — Completion events: separate identity, consumed fields and unknown semantics

| Event | Official installed consumer (Raw ID and original lines) | Confirmed / not established |
|---|---|---|
| `Events.CityProjectCompleted` | OFF-01 `DLC/Expansion2/UI/Loaders/TutorialLoader_Expansion2.lua:211–220` | Consumer uses player/city/project prefix. Lua ignores unbound extra arguments: this does **not** establish exactly three arguments, cancellation semantics or uniqueness. This UI example alone is not Gameplay delivery proof; project native records below are separate. |
| `Events.CityProjectCompletedNarrative` | OFF-02 `Base/Assets/UI/Popups/ProjectBuiltPopup.lua:27–46,215` | Popup declares seven fields and checks its seventh `bCanceled`. This is a distinct event; do not transplant that cancellation field into another event. |
| `Events.CityProductionCompleted` | OFF-03 `Base/Assets/UI/TutorialUIRoot.lua:1919–1945,3360` | Tutorial declares six parameter names, including fifth `canceled`, and consumes `orderType==0`/unit definition. The official name is a cancellation lead consistent with community labels, not proof of cancel behavior, complete event arity or a generic fourth-field meaning. |

**Community records:** SUK-PROJECT lists seven fields including bCancelled; SUK-PRODUCTION and CRU-EVENT-PARAMS list five for production; HEM-COMPLETION indexes the fourth item according to order type and reports community-observed repeat district callbacks in Gameplay. These are documented claims, not a new project observation. Do not turn the inconsistency into “the API is unreliable”. The generated CRU GameCore event-page naming is also not sufficient to resolve event identity.

**Project consequence:** Crew must bind a verified city/project completion to its own admitted source/reference/episode/order serial and unique receipt; aggregate counters alone cannot identify two cities. OFF-12 `WorldRankings_Expansion2.lua:289–351` uses `GetNumProjectsAdvanced` for player-level victory milestones. Current `Mod/UI/CrewProjectUI.lua:14–33` and `Mod/CrewProjects.lua:265–294` reuse that aggregate; shared player+project receipt scope is a source defect, not a hypothetical native flaw. Existing [B238 native review](../../Status/Validation/Results/Specialization_B238_Native_Review.md#results-and-diagnosis) records a scoped single Crew completion/load/binding, so Gameplay delivery is not wholly unknown. [S7d6](../../Status/Validation/Results/Refactor_S7d6_Crew_Proof_Gap.md) leaves independent same-turn multi-city attribution/late duplicates open. PU05a fixes proved shared unresolved-receipt scope locally; PU05b retains that separate irreversible-proof standard. Exact complete-argument/cancel semantics are not inferred from single delivery. Claim's true native early completion remains independent of its timer.

OFF-11 `AustraliaScenario.lua:1428–1429` consumes `InitUnit`'s returned object in the ordinary path. SUK-INITUNIT leaves return/arguments incomplete; CRU-UNITMANAGER labels recovered optional/no-result paths for its analysed build. None proves successful creation with a randomly lost return in supported normal macOS execution. Keep controlled one-shot receipts; do not add unit-set/count snapshots, automatic regrant or a universal recovery machine from synthetic nil/throw fixtures.

## ER02 — Queue and position inputs belong to their verified context

OFF-04 `Base/Assets/UI/CitySupport.lua:203–276` resolves current target definitions and calls the native UI `GetBuilding/District/Unit/ProjectCost` and matching Progress methods (including corps/army modifiers). Its `:600–611` calls `Map.GetCityPlots():GetPurchasedPlots(city)`. HD-12 `UI/Additions/HD_Utils.lua:7–40,222–229` wraps these UI calls. A project-owned coherent UI sampling/transport interface can replace that helper dependency; this evidence does not make the methods callable from Gameplay.

OFF-05 `ProductionHelper.lua:175–203` and OFF-06 `ProductionPanel.lua:2679–2707` distinguish current target from later queue slots/requests. SUK-GETAT documents UI-only zero-based queue slots with typed entries; SUK-CURRENT is a separate Gameplay method with incomplete return documentation. Request acceptance, native queue insertion and the full-turn business timer remain separate.

**Wonder placement:** `Mod/UnitTargets.lua:53–63` and `Mod/UnitSiteProbe.lua:52` read `HD_UNCOMPLETED_WONDER`; HD-13 Gameplay/Misc583–599 writes it. Replacing GetCityPlots alone is insufficient. A stronger official UI lead is OFF-13 PlotToolTip669,782–783 and OFF-14 MapSearch583,637: `Plot:GetWonderType()` identifies the placed wonder, `cityBuildings:HasBuilding(wonderType)` distinguishes completion. The separately mentioned GetConstructionsAtLocation examples still have plotId/plotID ambiguity. **Gameplay-context behavior remains NEEDS_NATIVE**, not a selected working replacement.

**Reuse existing transport:** `Mod/TimedProjectReaders.lua` already owns typed reader slots including `ExposedMembers.SPC_EngineeringStudyRead` and `SPC_ExpeditionQueueRead`. O4 first checks this existing production UI-sampling/Gameplay handoff rather than creating a parallel bridge. Unique native completion, lawful location, source/reference/queue witnesses remain separate; no guessed plot or extra retry framework.

## ER03 — Conditional data/UI assembly has official examples

OFF-09 `DLC/Babylon/Babylon.modinfo:34–37,169–170,231–235` demonstrates positive `ModInUse` on UpdateDatabase and, separately, criteria-driven ReplaceUIScript (the latter Heroes_Mode criterion uses ConfigurationValueMatches at38–44). OFF-10 `Expansion2.modinfo:26–34` supplies explicit LoadOrder and file Priority staging. CRU-MODINFO is a separate inferred Windows vocabulary, not the normative syntax source.

**Negative criterion evidence:** pinned HD-08 DL.modinfo134/173/177 uses `<ModInUse inverse="1">`. Actual original-profile GAME-CACHE lacks the corresponding inverse-gated UC Campus content (Claude review A23): supporting **INFERENCE** that the selector is honored on this Mac, not a new SPC native test. A negative criterion need not be invented; select the smallest evidenced assembly path and verify SPC's actual selected components.

**O5a candidate, not executed:** SPC-owned common definitions, explicit selected provider components or reviewed replacement of SPC rows, and a data-produced SPC assembly marker before dependent Lua. Do not select by HD-table presence or assume UI-only Modding.IsModActive in Gameplay. Final effective mapping precedes target/carrier generation. HD-only JOIN statements are separated from unconditional definitions (DevelopmentInvestment.sql3–7 vs15–20); exact LoadOrder bands account for selected companions and late HD components. All49 current InGame UpdateDatabase references are unconditional. A final HD DB SQL replay cannot prove loading order; independent game-built profile fixtures/load evidence are required.

## ER04 — Cold restore and persistent facts

OFF-07 `Base/Assets/UI/FrontEnd/LoadScreen.lua:47–55` emits `LoadScreenClose` from the Start/Continue button. `:457–485` handles LoadGameViewStateDone by enabling that button. OFF-08 `InGame.lua:90–94` describes HUD/gamecache readiness, not SPC history/network/effect reconciliation. Existing B105 native evidence rejects “first Publish means lifecycle complete” in its measured scenarios; it is not a universal save/load ordering test.

Current `RuntimeWork.lua:493–510` and `Gameplay.lua:1031–1032` do not provide a proved full effect-ready barrier. CRU-LOAD describes inferred serializer/cache phases from the same-version Windows/Linux analysis, not the Aspyr binary; CRU-PROPERTY distinguishes ordinary Lua SetProperty from unsafe experimental native memory writes. Neither proves macOS hidden-carrier restoration timing.

**Still ENGINEERING_EVIDENCE_OPEN:** exact same-build carrier/Modifier/reference restore boundary and first coherent input publication. Preserve OD-1: incomplete initialization is not a new loss, not permission to write K-only/zero or treat the last output as transaction proof. Seek the smallest existing or separately authorized native observation only if this blocks the affected implementation; no probe was added here.

## ER05 — Effective-chain Tier and actual HD seams

**Corrected source:** production Tier comes from HD_BuildingTiers through OrdinaryBuildingCatalog203–207 (and StandardizationCatalog4–23 / DevelopmentInvestmentCatalog5–21). It does **not** come from old SPC_Lv2HousingTiers; the latter has no production reader. In the actual original-profile game-built cache, early-order SPC_Lv2HousingTiers contains only21 official rows. That is a load-order/test-basis blind spot, not the current Tier authority.

HD-18 `UpdateDataBase/HD_BuildingTiers.sql:11–22` initializes eligible rows, sets city-center0, then advances prerequisites to2/3/4. Its Holy Site bump at23 is special handling; it is not a general graph algorithm. GAME-CACHE current facts: Market2 follows Fair/Waystation; Bank3 follows Market/Mint/Sukiennice; Workshop2 follows WaterMill/WindMill; ResearchLab4 follows four JNR alternatives. Thus differences from official three-level chains reflect enabled HD/UC content, not a corrupt housing table.

**Latest Owner definition, formal recording pending:** SPC defines Tier as a building's position in the loaded environment's effective same-district upgrade chain. Prefer deriving from real district/prerequisite/replacement facts; not HD's table as authority, not a fixed per-environment hardcoded catalog. Changed predecessor content can legitimately shift Market T1→T2. Missing/cyclic/incomplete/ambiguous cases are errors, never silent T0/T1; unrelated objects are not-applicable. Replacement equivalence, same-level alternatives and actual same-district upgrade edges must be distinguished from outside-district buildings, virtual gates and other non-upgrade unlock conditions. Non-upgrade unlocks do not automatically increment Tier. A predecessor's absence from a Tier table alone never justifies skipping it; positively identify its role, otherwise a genuinely missing/incomplete chain remains an error (Owner N1). Ordinary eligibility remains independent. D formulas and three-tier D6/four-tier D10 unchanged. The intervening cross-environment fixed-Tier proposal is withdrawn.

**N1, Owner confirmed:** Industrial Water Mill (`BUILDING_IZ_WATER_MILL`) is **T1**. Its `BUILDING_JNR_MILL_RACE` → `BUILDING_JNR_DUMMY_IZ_RIVER` prerequisites are confirmed virtual unlock gates, not upgrade buildings; they do not add a level or make Workshop's WaterMill/WindMill alternatives incomplete. This is an evidence-based classification, not a general skip of all absent Tier rows.

**N2, migration comparison:** HD old values remain a diagnostic baseline, never final semantic authority. The new provider follows approved actual-chain semantics. Explain Data Center's capped old value and Hospitium/Garden's forced old bump individually; do not alter the new rule just to reproduce the old table. Same-profile checks report unexplained deltas and consumer impact, not automatic all-row equality. D formulas/D6/D10 unchanged.

The existing [integrated plan §6](Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/Architecture_Convergence_Integrated_Roadmap_DRAFT.md#effective-chain-tier-contract--a21-evidence-basis--a22-semantics) lists exact cases including the confirmed Water Mill virtual-unlock T1 rule and remaining candidates: Holy Site's forced tier4 with tier2 prerequisites; Mansion's cross-district Palace unlock; future-only Sewer wording; Data Center's tier4 predecessors vs a possible next chain position beyond current0–4 reader support. These are **coverage/interpretation checks, not newly assigned Tiers**. Use a small explicit map only for a genuine unresolved relation; no automatic enrollment or new plugin system.

| Core input/execution contract | Current dependency / equivalent-provider duty |
|---|---|
| Effective building/district/replacement/ordinary/tier facts | HD tier/dummy tables are hard requirements of three catalogs and two SQL JOIN files. SPC shared catalog owns output; approved ontologies remain separate. Final graph and mapped definitions before consumers/target generation. |
| Actual workers/anchor/D/ACTIVE | Current native APIs and shared owners in both profiles; lock state is not occupancy. Do not copy HD base specialist GPP/economy as core. |
| Great Works/creator-era facts | Current definitions + native creator fallback; GreatWorkCatalog318–340 filters absent definitions. Unknown present metadata is not era0; eight eras unchanged. |
| Queue/target/location | Current ConstructionProbe/Crew snapshot path, UnitTargets and UnitSiteProbe helper/marker inputs; owned coherent UI sampling with existing reader slots. Unique completion proof separate. |
| Output primitives | Three HD-defined wrappers over official Effects/Collections need SPC-owned definitions; presence/readback alone not execution or arithmetic proof. |
| UI base / callback adapter | Five unconditional HD-base replacements: CrewProjectOrder2 DL_ProductionPanel; ExpeditionSpyUnitPanel2 DL_UnitPanel; TimedProjectCityPanel2 DL_CityPanel; InstitutionOverview3 DL_CityPanelOverview; TimedTurnProbe2 HD_ActionPanel. Only two Espionage replacements already use official bases. CrewProjectOrder33–44 GetDataHelper is HD-only (HD ProductionPanel106); O5 owns environment/base selection and the fixed no-HD load smoke after assembly; O6 owns the concrete official-base callback/behavior/interaction work (Owner N3). Reuse the environment/evidence, no duplicate full test; load alone does not certify behavior. |
| History/delivery/effect owner | Store/profession/Bridge/writers unchanged in responsibility. Environment adapters never own formulas, permanent history, irreversible receipts, ACK business or lifecycle. |

**Pinned profiles:** U5 and later HD before/after regression use the same actual full profile including HD District Expansion2701747165, HD Corporations2616754773 and enabled UC Campus/Commerce/Theater/Industry/Spirituality/Worship/Aqueduct/Entertainment/Suburbs. Exact IDs/versions in integrated §6 and ENV metadata. Reduced-HD is a separate unrun certification, not the regression substitute or mandatory core dependency list. The only currently inspected DB is HD-populated; an independent HD-free baseline still needs the Owner-authorized later launch. No official-only DB acceptance is claimed.

## ER06 — Output definition closure at type level

Scope: the 49 currently declared InGame UpdateDatabase references, including **loaded legacy/probe definitions**. Static extraction finds 22 distinct literal ModifierType names: 17 exact official DynamicModifiers definitions, two SPC definitions and three HD-supplied names. This is not a carrier count or per-effect behavior audit. The small derived extraction remains outside Git as DERIVED-HD-CLOSURE; source identities are in the local manifest.

| ModifierType | Definition owner / source locator | Collection / Effect |
|---|---|---|
| `MODIFIER_BUILDING_YIELD_CHANGE` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:595` | `COLLECTION_OWNER` / `EFFECT_ADJUST_BUILDING_YIELD_CHANGE` |
| `MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST` | HD: `UpdateDataBase/DL_Modifiers.sql:168` | `COLLECTION_OWNER` / `EFFECT_ADJUST_BUILDING_PURCHASE_COST` |
| `MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2080` | `COLLECTION_CITY_DISTRICTS` / `EFFECT_ADJUST_DISTRICT_TOURISM_CHANGE` |
| `MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE` | HD: `UpdateDataBase/DL_Modifiers.sql:152` | `COLLECTION_CITY_DISTRICTS` / `EFFECT_ADJUST_DISTRICT_YIELD_CHANGE` |
| `MODIFIER_CITY_ENABLE_BUILDING_FAITH_PURCHASE` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:650` | `COLLECTION_OWNER` / `EFFECT_ENABLE_BUILDING_FAITH_PURCHASE` |
| `MODIFIER_CITY_INCREASE_GREAT_PERSON_POINT_BONUS` | OFFICIAL: `DLC/Expansion2/Data/Expansion1_Modifiers.xml:1045` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_GREAT_PERSON_POINTS_MODIFIER` |
| `MODIFIER_PLAYER_ADJUST_CIVIC_BOOST` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:1730` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CIVIC_BOOST` |
| `MODIFIER_PLAYER_ADJUST_PROPERTY` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2690` | `COLLECTION_OWNER` / `EFFECT_ADJUST_PLAYER_PROPERTY` |
| `MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:1735` | `COLLECTION_OWNER` / `EFFECT_ADJUST_TECHNOLOGY_BOOST` |
| `MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_CHANGE` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:840` | `COLLECTION_PLAYER_CITIES` / `EFFECT_ADJUST_CITY_YIELD_CHANGE` |
| `MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:530` | `COLLECTION_OWNER` / `EFFECT_ADJUST_BUILDING_PRODUCTION` |
| `MODIFIER_SINGLE_CITY_ADJUST_CITY_GROWTH` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2145` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_GROWTH` |
| `MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2165` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_YIELD_MODIFIER` |
| `MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION` | OFFICIAL: `DLC/Expansion2/Data/Expansion2_Modifiers.xml:1178` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_YIELD_PER_POPULATION` |
| `MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION` | HD: `UpdateDataBase/DL_Modifiers.sql:143` | `COLLECTION_OWNER` / `EFFECT_ADJUST_DISTRICT_PRODUCTION` |
| `MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2105` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_GREATWORK_YIELD` |
| `MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT` | OFFICIAL: `DLC/Expansion2/Data/Expansion2_Modifiers.xml:1163` | `COLLECTION_OWNER` / `EFFECT_ADJUST_GREAT_PERSON_POINTS` |
| `MODIFIER_SINGLE_CITY_ADJUST_TOURISM` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2175` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_TOURISM` |
| `MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2110` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS` |
| `MODIFIER_SINGLE_CITY_ADJUST_YIELD_CHANGE` | OFFICIAL: `Base/Assets/Gameplay/Data/Modifiers.xml:2190` | `COLLECTION_OWNER` / `EFFECT_ADJUST_CITY_YIELD_CHANGE` |
| `MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION` | SPC: `Data/EngineeringStudy.sql:33` | `COLLECTION_OWNER` / `EFFECT_ADJUST_WONDER_ERA_PRODUCTION` |
| `MODIFIER_SPC_P0_GOV_PROPERTY` | SPC: `Data/GovernorProbe.sql:3` | `COLLECTION_PLAYER_CITIES` / `EFFECT_ADJUST_CITY_PROPERTY` |

The HD wrapper definitions are HD-09 `UpdateDataBase/DL_Modifiers.sql:143,152,168`. Their underlying official effects have explicit OFF-DEF-01 `Modifiers.xml` usage: district production862, building purchase1012, district yield1372/1377. SPC's wonder-era and city-property wrappers also use official effects at1052/2287. This establishes a narrow data-wrapper replacement path, **not completed execution compatibility**; preserve collection, attachment, arguments and per-family arithmetic, and avoid duplicate global-name registration. No DLL/HD economy is required merely to name these wrappers. **A24 gate:** every loaded Modifiers.ModifierType resolves to DynamicModifiers in each pinned game-built DB; GAME-CACHE has no ModifierType foreign key on Modifiers, so SQL load and installed carrier readback can otherwise hide a missing effect definition. A healthy capture alone does not establish behavior under deliberate malformed SQL/undefined types; do not claim such fault injection occurred.

The three collections used by SPC custom/HD wrappers have official usage: OWNER531, PLAYER_CITIES781, CITY_DISTRICTS2071. Four RequirementTypes appear in SPC inserts:

| RequirementType | Evidence / boundary |
|---|---|
| `REQUIREMENT_DISTRICT_TYPE_MATCHES` | OFF-DEF-02 Requirements.xml35/39/43, official usage. |
| `REQUIREMENT_CITY_HAS_GOVERNOR` | OFF-DEF-07 Expansion1_Policies.xml1928, official usage. |
| `REQUIREMENT_CITY_HAS_GOVERNOR_WITH_X_TITLES` | OFF-DEF-07 :1896, official usage; doesn't authorize profession-specific governor caches. |
| `REQUIREMENT_PLOT_PROPERTY_MATCHES` | Actual GAME-CACHE Types declares KIND_REQUIREMENT; official OFF-DEF-08 CivRoyaleScenario_UnitAbilities.xml422 uses it (another official Civilizations.xml392 also does). HD supplies no native implementation. SPC CultureAesthetic.sql25 and CultureAesthetic56/72/126/132 own their plot properties. Stock definition/usage confirmed, low HD-absence risk; CRU-PLOT-REQ remains same-version other-platform corroboration, not Mac effect-acceptance proof. |

Other outputs use official relational tables such as Building_CitizenYieldChanges/GreatPersonPoints/YieldChanges. Do not generalize one primitive's rounding/stacking to another. Existing precision and coexistence reports remain the evidence, not recreated tests.

## ER07 — Loading order and retired external consumers

HD-08 has early tier setup16001, wrapper definitions16010, requirements16014 and main last phase30000; conditional resource/removable-district components reach10000000. Pinned HD District Expansion DB components reach18001 and HD Corporations30001. Selection and all actual content-changing phases must be considered; 30000 is not a global HD maximum. Current SPC affected component orders are Discounts2000001, ResearchCross2000002, EngineeringStudy2000003 and Development10001080. These manifest numbers explain current declared order only; no actual SQL execution or independence run occurred here.

Loaded legacy NetworkBoost*.sql writes `HD_Player_Extra_Tech_Boost` via a stock property effect. Its external consumer is HD-specific, but positive owners are separately retired/inactive. Distinguish a live core reward from an installed definition/exact cleanup dependency; the external property name is not permission to delete SQL or current carrier IDs. No HD manifest dependency/reference exists in current SPC; the real seams are the tables, wrappers, helpers/marker and UI bases above.

## Remaining gates and use

This tranche is sufficient to expose concrete coupling and support a **plan** re-audit. It is not a no-HD startup/mechanism acceptance or implementation approval. Keep precise gates for completion/cancel semantics; lawful wonder location; same-build effect-ready boundaries; effective-chain Tier coverage/errors; exact SQL/UI assembly; and actual scope/rounding/stacking. Resolve with existing evidence and targeted authorised local/native checks during the relevant slice, not blanket probing.

The integrated candidate owns proposed order and affected responsibilities. Future approved Architecture Markdown owns final contracts. Reference updates neither change gameplay nor weaken tests. No production/test/formal source, probe or game setting was changed by creating this reference.

### Correction provenance

Claude's Stable Targeted_Reaudit_Integrated_Roadmap A21–A28 and the Owner's final Tier correction prompted these bounded corrections. Source/DB queries were read-only and immutable. No code/test execution, intentional malformed load, native launch or new effect PASS. New OFF-DEF-08 and HD-18 source identities are in the appended local tranche index; previous review-manifest bytes remain frozen. Missing independent HD-free DB, Gameplay wonder semantics, actual selected assembly/UI callbacks and native effects remain explicit gates.
