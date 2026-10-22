# D0032 runtime archaeology and retirement map

Document Owner: Codex
Baseline: develop65170105 / Mod B076.103 / 121 files
Evidence: STATIC_CONFIRMED = code/manifest inspection, not new game validation.

## Scope and interpretation

[Source inventory](D0032_Runtime_Inventory.json) records all121 runtime files, hashes, manifest roles, includes, registered/candidate callbacks, persistence/write sites and per-file classification. Generated SQL is reviewed by definition family and argument pattern, not mistaken for1894 separate business modules. `Gameplay.lua` Start/dispatch and manifest actions decide execution, not filenames/comments: UnitActionSitePolicy still says offline yet is included and called by UnitSiteProbe; ResearchSupport says DEV yet automatically grants yields. ImportFiles alone is not a Start. Current cached DebugGameplay DB contains **zero SPC Buildings**; it is useful external primitive/catalog evidence only, not this running package's instantiated database. PAC-I001's1894 definitions remain a dated catalog snapshot, not a fresh count or per-city instance count.

KEEP preserves responsibility/contract, not an assertion all unrelated defects are solved. ADAPT reuses structure with explicit semantic changes. REPLACE changes the ability's core meaning; RETIRE stops its old effect/writer. Files may contain both reusable primitives and retired policies. Every flagged **EFFECT** must have a cutover owner; hiding the UI is insufficient.

## Core matrix

| Module / file(s) under Mod | Current responsibility/status | Class | D0032 responsibility / reason | Dependency and retirement condition |
|---|---|---|---|---|
| Gameplay.lua | Starts progression, effects, probes; Request dispatch; inheritance explicitly nil | ADAPT | Thin startup/validated action routing with explicit per-feature old/new mode | Each cutover must disable old Start, direct calls, bridge notify and hidden force-on requests before new writer |
| Probe.lua / Data/GovernorProbe.sql | Engine wrappers, test-player filter, governor Property projections, counted writes, queue helpers | ADAPT | Keep native title gate/write counters; normalize facts and separate ordinary catalog from probe fixtures | Participation/source ref layer; no speculative replacement of tested governor primitive |
| BindingProbe/FreshBindingHook | Game+City confirmed UID token, original owner/id/position;32 lifetime creations | ADAPT | Keep original scope until explicit cityKey/schema migration | State/save spike; not owner-independent today; do not silently reset/reuse IDs |
| CityJournalProbe/CityFlowProbe | First completed district locksIdentity/P1; dual persisted consistency/HELD protocol | ADAPT | Single confirmed progression view; future History/REALLOCATING discriminants | P0-A read facade only; later versioned migration must stop old first-completion writer for migrated city |
| EffectiveFacts | Validates Flow, receipts, governor; Potential=1+investments | ADAPT | Preserve current read; later support restructuring debit and distinct mode | No derived rebuild from carrier; cannot reuse receipt-count formula after P−1 |
| InvestmentAction | **STATE/UNIT EFFECT** Settler consume+receipt→Potential; confirm revalidates | ADAPT | Keep normal investment; reject REALLOCATING; use new city/ref state when migrated | Do not rename this Commerce investment or conflate gold contracts; old ledger only retired after verified migration |
| ResearchSupport / ResearchSupport.sql / ConstantSupport.sql | **EFFECT** R/C/Commerce working specialist3F3P | ADAPT | Numeric primitive KEEP; common eligibility/unique/pillage/state adapter update | No tier-D substitution; preserve support, remove only old III extra under own cutover |
| IndustrySupport / IndustryRefresh / IndustrySupport.sql | **EFFECT** per-worker3F + integer0..255 BASEP; verified C2 UI sample | ADAPT | Same base support K1, normalize district/pillage, parameters; no actual fallback | Reuse C2 epoch/single-flight. Current integer restriction is technical limit, not universal fraction rule |
| Lv2Housing / Lv2Housing.sql | **EFFECT** district+present-tier housing selectors; player-wide native district walks | ADAPT | Same per-tier Housing, shared current ordinary/pillage facts | Current HasBuilding alone no explicit pillage predicate; do not replace tier presence with weighted D |
| Lv2GPP / Lv2GPP.sql / GPPReadout | **EFFECT** workers×2 baseGPP, Culture3classes; bit carrier+readout | ADAPT | Keep native baseGPP, normalized specialist anchor/current eligibility | Reuse bits as technical only; 0.1 newGPP not proven by integer2 path |
| Lv3Support / Lv3Support.sql | **EFFECT** R/C/Commerce+2F2P topup; Industry+2F and2×BASE Gold bits | RETIRE | All four new designs remove these upgrades | Cutover deletes fixed4+IndustryGold8, disables every call. Lv1 support untouched |
| Lv3Effects / Lv3Effects.sql | **EFFECT** R/C workers×0.5population; Commerce connected-kind+2S/C/P | RETIRE | Not new Applied Learning/Meaning/Commercialization | Per-profession old masks removed before replacement. Keep other domains' old mode until separately cut over |
| Lv4Percent / Lv4Percent.sql | **EFFECT** R/C5%cityyield per worker | RETIRE | Research tradition age is not worker%; Culture local observations tourism is not culture% | No relabeling carrier formula; remove corresponding8 bits on cutover |
| CopyYields / CopyYieldRefresh / CopyYields.sql | **EFFECT** ResearchIV50%all-nonCampus ACTUAL sum; IndustryIV max50%sourceactualP reception; integer/half adapter | REPLACE | Retire both old formulas. Pure precision decomposition may be reused after explicit interface qualification | Research BASE limited nine domains is different input; Industrynewtemplates no50%P. Stop UI actual sampler when last old consumer removed |
| NetworkInput | A complete logical signature: routes/refs/Identity/Potential/ACTIVE/capital/config | ADAPT | Preserve full signature principle; new mode/refs and ruleset versions | Payload versions separate; no routeRevision-only key |
| NetworkBridge | B shared topology/National view; D2 Current reads noCapture; formal withdrawals | ADAPT | Preserve common NET topology, source provenance, verified view. Split legacy National and independent payload consumers/direct edge queries | Mode/source/reference additions invalidate correctly; confirmed invalid removes only affected capability, not signed development contracts |
| NetworkSender / UI/BackgroundRoutes | Approved current UI routes, native-count validation, oneflight/ACK/retry, same suppression | KEEP | Sole route producer; retain directed endpoints | No new provider, no trade-screen-open requirement, no polling replacement |
| TradeRouteProbe | Trader-filtered dirty signals + bounded raw diagnostics; not route authority | ADAPT | Preserve required signal path; diagnostic ownership explicit | Do not retire signal because filename Probe; avoid rebuilding from historical TradeEvents |
| ShadowRouteState | Historical candidate model imported, no formal route authority | KEEP | Test/reference-only | Not substitute for verified bridge; no new gameplay use |
| NetworkBoost / BoostConfig / BoostIntegerConfig / BoostRefresh | **EFFECT** ResearchInspiration + CultureEureka kLsqrtN; floor(x+.5); native+HD property bridge | ADAPT | Researchlegacy retained DESIGN_DEFERRED; Culture branch RETIRE on newCultureNetwork | Culture retirement removes integer,legacy,test selectors and blocks its requests; Research must not be removed incidentally |
| StandardizationCatalog | HDtier/dummy metadata + reviewed building matching/discount directory | ADAPT | Ordinary catalog source evidence with separate standardization policy/groups; add district templates | Do not reuse enable=true for every shared ability or erase historical knowledge |
| Standardization | **STATE EFFECT** permanent per-city building learned ledger, initial backfill+event queue | ADAPT | Preserve ledger semantics; typed district knowledge,cityKey/catalog schema | Reclassify only reviewed migration; oldhistory not regenerated from current buildings |
| StandardizationDiscount / UI/DiscountEligibility / correspondingSQL | **EFFECT** ACTIVE1–4 max×10% permitted purchase path; C1singleflight/D1sharedbatch | ADAPT | III+template union + independent best efficiency; purchase allowed only native; add separate construction projection | Oldrates/carriers RETIRE at own cutover, keep C1/D1. Production path absent today, not “Standardization done” |
| CrewProjects / CrewProjects.sql / Crew.sql | **UNIT EFFECT** all5 native project-unit grants from IndustryI; fixed denominations | ADAPT | III T1–3 / IV traditionT4–5, sourcebinding2slots | Native grant currently no persistent training-city capacity; gate at completion as well as UI. Source attribution/cap spike first |
| UnitActions / ConstructionProbe / CrewPrecision | **UNIT/PROGRESS EFFECT** consume1Team→cappedAddProgress; building/district/wonder target; receipts | ADAPT | Keep preview/confirm/recheck/wastedoverflow/speed floor; Wonder-only, source slot release, Macro target effect | Oldordinary-target branch RETIRE; do not reuse uncertain AddProgress intent automatically |
| UnitTargets / UnitActionSitePolicy / UnitSiteProbe | Target enumeration, site qualification, read diagnostics; policy used by diagnostic UnitSiteProbe; formal UnitTargets/confirm have separate validation | ADAPT | Wonder-only Crew; Settler unchanged; distinct restructuring stages later | Same legal target owner as confirm; normal preview never commits |
| DialogueModel / Dialogue / Dialogue.sql | **EFFECT** dynamic25%×max(0,eraKinds−1), ACTIVE4; no permanent project quota | REPLACE | CurrentknownGW facts reusable; newIII cityhistory5%X per full-turn project separate | Remove D-selectors+TEST selectors; cannot translate current25% into earned history |
| GreatWorkAdjacencyModel / GreatWorkAdjacency / SQL | **EFFECT** per-work50%BASE sixyield on RequiresPopulation districts | REPLACE | NewMeaning uses ordinary D per defineddomain; no oldfloor waiver | Remove signed156 pieces before new output; pure base getter maybe Researchreuse after scope check |
| UI/DialogueRefresh | Currentcollection+oldBASEpayload coupled; bounded ACK and dirty | ADAPT | One confirmed GW fact service/location version; separate adjacency consumer | Existing protocol not automatically C2 safe; full replacement validation/ref/epoch before permanent reward |
| UI/GreatWorkBasis | Historical highest-value per-work difference read report, no formal grant | RETIRE | Historical diagnostic only; not newGWauthority | Hide/disable current design report routing, preserve history code |
| CommerceConvergence / SQL | **EFFECT** incomingonly maxsourceS/C/P×20%floor at IV; plans-before-writes | REPLACE | NewdomainGold commercialization, contracts etc not implemented | Remove48bits and dispatcherControl/Audit/bridge callbacks at Commercecutover; never use20% as fallback |
| CityPotential / UI XML | Selectedcity shortbadge, D2dirty/token response (no2s repeatedrequest) | ADAPT | Presentation-only readmodel institutions/history; retain currentbadge until UIbatch | No facadeBuildings; no newGameplaywrites to showPotential |
| UI/UnitPanelActions / UnitTargetMarkers / UnitSites | Preview/confirm, purplelens, hiddenoldentry; D2idle suppression | ADAPT | Retaintestedflows, per-action statecontracts | Preserve mapsite/confirm separation; no pollingfulltargets |
| UI/CrewProjectOrder | HD ProductionPanel replacement sorts crew rows only | ADAPT | Reuse host hook cautiously for future Commercepre-request interception | Not a present clickinterceptor; UIprototype gate separate |
| UI/GPPRefresh / BoostGreatWorkRead | Batchednative dirty notification / manual evidence | ADAPT | Retained notifications only for activeconsumers; future readmodelversion | OldBoost/GWlabels notnewdesignmechanics |
| PerformanceCounters / DiagnosticLog / RuntimeAuditCore / UI RuntimeAudit | Fixedcounters,boundedlog/capabilityguard,turnsummary | KEEP | Extendfewfixedmetrics only on demand of futurebatches | No extraautomaticIO; no nativefile availabilityclaim |
| UI/P0Panel / XML / manualreadhelpers | Reports+hiddenexperimentalcontrols; someREADcanRefresh | ADAPT | Explicit read/refresh/experimental distinction, selectedcity comparison | “Read” not universalzeroeffect: Network.Read can refresh/publish. NewP0-A diagnostic must not invoke oldaudits |
| Storage/Envelope/Eligibility/Qualification/Completion/CompletionRecord probes | Fixtures,eligibilityevidence,completionobservation, somepersistentwrites | ADAPT | Preserve bounded evidence, separate mutation fixtures from formal state | Not all probes safe read-only; oldcompletionrecord notcrediblemissinghistory recovery |
| HalfYield/Purchase/GreatWork/YieldCarrier probes + correspondingSQL | **EXPERIMENT EFFECT** manually enabled modifiers/properties, somepersistacrossload | ADAPT | Keep isolatedtestbackend, explicitcleanup/detection beforenewsettlement | Prefix exactcleanupinclnonbuildingflags; hiddenbutton notproofinactive |
| CityInheritance / InheritanceShadow / CityInheritanceRead | Imported but notStarted;sharednil | KEEP (ISOLATED) | Historical reference only; newtransferdesign must notenable oldmodule | Futureidentity/Legacytestgate; no auto恢复 |
| Other Config/Data/Colors/Text and UI context XML | Testcivilization/assets, localization, panelcontexts,purplecolor | KEEP/ADAPT per inventory | Keepblanktestcarrier/context wiring; futureLocalization separate | No unrelated test-civilization ability changes or institution Building creation |

## Effect-bearing definition families — cleanup ownership

Counts below are the frozen PAC catalog counts where generated from external data; current SQL patterns are checked. Counts are not live city writes. Every family remains internal, including former “institution candidates”.

| SQL family | Definitions / native effect | Future treatment |
|---|---|---|
| ResearchSupport+ConstantSupport |3 fixed support Buildings, Building_CitizenYieldChanges | Keep3F3P, qualify via facts |
| IndustrySupport |9(food+8Pbits) citizen yield | AdaptK/base/qualification, noLv3Gold |
| Lv2Housing |9 housing selectors, reviewed tier directory | Adaptshared eligibility; don'tweightedD |
| Lv2GPP |32 specialist-classGPP bits | Adaptfacts, keepbaseGPP primitive |
| Lv3Support |4fixed+8IndustryGold | RETIRE effects |
| Lv3Effects |16R/Cpopulation+3Commercekind | RETIRE effects |
| Lv4Percent |16R/Cpercent | RETIRE effects |
| CopyYields |80S/Ppositive/negative/population correction | Retireoldowners; genericnumericpieces maystay only under explicitnewowner |
| NetworkBoost |1032legacyL/N | Alreadycleanup-only, ensure can'trevive |
| NetworkBoostInteger / BoostIntegerTest |90integer(45each)+4test | Researchlegacy retained; Culturecleaned atnetworkcutover |
| Dialogue |numberofloadedEras Dselectors (PAC8)+3test | REPLACE effect, noearnedhistoryfromselector |
| GreatWorkAdjacency |156sixyield/signedbits, sevenworkcategories | REPLACE effect; broadcategory restriction notnewknownworkallowlist |
| CommerceConvergence |48 S/C/Pbits | RETIRE completeoldgrant |
| StandardizationDiscount |catalogtargets×4 (PAC336) targetpurchase modifiers | KeepC1D1; replacerates/sourcegate; newproductionnotpresent |
| CrewProjects |1accessBuilding+5projectgrantunit modifiers | Adaptgate/source/cap; duplicategranttest mandatory |
| HalfYieldProbe / PurchaseProbe / GreatWorkProbe |32half+2purchase+2GW | Explicitexperimentalquarantine/cleanup only |
| YieldCarrierProbe |Trait/player Property-conditioned1/1.5S/C/P; noBuildings | Nonbuildingretirementaudit too:flags canoutlive UI |
| GovernorProbe |Trait-attached requirement→cityProperties | KeepACTIVEreadprimitive; not a yield/institution |
| Civilizations/config/text/icons/colors |blanktestidentity and presentation support | No ordinary infrastructure or institution entities added; test fixture Buildings remain internal |

Disabling a Lua writer does not remove saved Buildings, trait-conditioned experiment flags, player HD Boost properties, queued Crew projects or pending native grants. Cutover manifest must enumerate these, check zero old effect after reload and block hidden controls restoring them. Keep frozen SQL Type IDs as cleanup/tombstone definitions for the declared supported save route; do not delete IDs first and lose ability to identify/remove them. A fresh-save-only candidate may omit retired definitions only after explicit save compatibility gate.

## Present limitations not repaired by A–D2

- ResearchSupport and Lv2Housing retain broad turn/load audits and repeated player district enumeration. D2's nine-module comparison did not make every module O(C); report them as ADAPT, not a new claimed leak.
- Some local old consumers (Housing/Lv3Effects/Lv4Percent/Commerce) still turn unavailable inputs into empty wanted plans. C1/C2 fixed their own paths, not all project-wide withdrawal behavior. Replacement consumers must obey verified/temporary/confirmed distinction.
- GW producer still enumerates all buildings/slots on a realdirtybatch and couples adjacency. Need sharedknownregistry and affected-city indexing for newfourCultureconsumers; no recurringcollect on hover.
- Currentsource filter is test-trait scoped; generalenabledplayer support and32-city ceiling remain knownlimits, not changed here.
- Crew receipts grow withactions; diagnosticcachedkey tables maygrowwithhistoricalcityrefs; future save/lifecycle work must not discard dedupe orpermanentawards to boundmemory.
- New tradition/observation/contracts/history/REALLOCATING state is absent. Existingunitreceipt/progression records are foundations, not implementations oftheseabilities.
- No currentcommercialization50/100 orGreatMerchant sacrifice implementation was found; these are NOT_ADOPTED design explorations, not effects requiring an inventedruntimecleanup.

Refer to the adaptation state table and implementation plan for dependencies, gates and rollback. No archaeology finding authorizes a source edit in this batch.
