# Audit follow-up priorities and Advisory publication review

## Refactor program intake — 2026-10-24

This section is the current scheduling checkpoint and supersedes conflicting timing in the historical sections below. The user explicitly assigned Primary and authorized S0–S10 of the reviewed refactor program, with **U1 after S0/S1**. Current source basis: `25327e7808f39da692b0270727047d1a3988e958`, B271.298 / S0718. The [U1 decisions](Refactor_Program_U1.md#accepted-u1--2026-10-24) are accepted with the user's revisions. D0058/A0182 formalize them before S2; no deployment is authorized. The Advisor originals remain read-only, local review inputs. This existing scheduling record is the only intake map; original finding IDs are retained rather than creating a second registry.

### Explicit user decisions

| Date | Recorded decision | Boundary |
|---|---|---|
| 2026-10-23 | Internal SPC InternalOnly carriers are non-pillageable. | Already implemented in B271. Do not reopen as a policy question; actual pillage-event acceptance remains unobserved. |
| 2026-10-23 | Write the constraints before refactoring. | S0/S1 text review at U1 before S2 code/tests. |
| 2026-10-24 | Fold Commercialization accrual loss, IndustrySupport retry storm and GC UI_PENDING starvation into the refactor. | S4, no separate hotfix. |
| 2026-10-24 | “网络待确认之后，新的事实被更新之前，先保持之前的数值（即不更新载体）（只有新的事实会更新载体）”. | Direction accepted; D-1/D-2 exact scope, cold-load and qualification precedence require U1. No runtime hold is implemented by this record. |
| 2026-10-24 handoff | City-ownership gameplay remains excluded; A8 was assessed and the user explicitly approved the eight-era correction. | Keep the section-6 exclusions. Technical lifecycle prerequisites are not permission to decide new ownership outcomes. |

### Before evidence and interpretation

| Evidence | Recorded observation | Limits |
|---|---|---|
| B270 T58–69 | Approximately 7,800 city visits and 169,000 building checks per local turn; footprint about +0.10 GB/turn; Gameplay Lua roughly 350–790 MiB sawtooth. | Advisor `B269_B270_Log_Review.md:52–58`, LOG_OBSERVED. These are whole-turn figures, **not per-AI-phase figures**; the plan's mixed phrasing is corrected here without editing the Advisor original. |
| B271 T69–74 | Commercialization carrier value absent at the observed accrual point in 2 of 3 eligible turns; IndustrySupport LOCAL_END audit counts 618 / 3,263 / 11,802 / 5,507 / 9,855. | Advisor `B271_Log_Review.md:27–39`. First observed treasury difference bounds an interval, not the exact engine commit instruction. |
| B271 GC/memory | UI_PENDING and NETWORK_INFLIGHT skips; Gameplay heap reached 1,214 MiB before a collection; footprint about +0.32 GB/turn. | `B271_Log_Review.md:39–40,60–72`; C was enabled and Commerce/workload changed. Not controlled SPC attribution. Older Memory_Growth §1's “never above ~1 GiB” statement is superseded by later logs, not copied as current fact. |
| B271 event delivery | Ten names unavailable in the observed Gameplay/UI build; C windows T71–73 capped at 400. ~390 GovernorChanged callbacks per AI phase. | `B271_Log_Review.md:42–56`. Callback count multiplies subscriptions; it is not a distinct native-event count. No general all-version API claim or complete uncapped order inferred. |
| B271 D4 | 4,557 intended XP2 rows passed the recorded copied-engine-DB check; no pillage occurred in the later session. | Existing [B271 result](../../Status/Validation/Results/Specialization_B271_Turn_Timing_Carrier_Pillage.md), STATIC/LOCAL evidence only; not rerun here and not new native PASS. |

Native sources above are the two reviewed reports under `Reports/Advisory/V01_Playtest_Evidence/`, with their hashes in U1. Raw evidence stays local. Work/heap/footprint remain distinct. A different-save or workload difference is not a causal subtraction establishing SPC-attributable growth. Later checkpoints must retain UNKNOWN where attribution is not measured.

### Current-HEAD disposition

**FIXED** means the named subset is already implemented; **CHANGED** means partial implementation or materially changed evidence; **OPEN** means the planned gap is still present. These are static dispositions, not blanket native acceptance. Unless a DevelopmentTests/tools prefix is given, source files below are under `Mod/` (including `UI/`). All source references below were checked at the pinned source-review HEAD; no historical source line is adopted unchecked. Compound rows share one planned work item; no claim is made to re-audit every unselected entry in the 191-item advisory register. Recheck touched lines again before each implementation stage.

#### S2 — Test and observability prerequisites

B272 S2 complete: [actual results and execution closure](../../Status/Validation/Results/Specialization_B272_Refactor_S2.md). The rows below retain their original source basis;13 strict before-counterexamples now reproduce the named later-stage gaps. Harness/attribution/alarms are implemented, not proof that those later repairs are complete.

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Native-faithful common harness / C061 | CHANGED: B270/B271 already use Lua5.1 and ordered multiple listeners (`DevelopmentTests/test_b270_event_scope.py:3,13–19`; `test_b271_diagnostics.py:8,21–30`). Old `test_runtime_audit.py:4,38` remains lua55/single-slot; `refresh_fixture.py:21–25` defaults to frame draining. | Integrate common order control, separate contexts, explicit missing events and no-frame default; do not claim these improvements never existed. |
| Executed closure, reverse index, cold load / C067–C069 | CHANGED: `test_b267_regression.py:8–30` already has a versioned runner and explicit exclusions. `project_paths.py:5–15` configures external DB, not environment identity; B271 doubles share a VM. No common module→test/executed-closure facility found in the scoped inventory. | Build on existing machinery; preserve explicit exclusions and frozen failures. |
| T01 locality baseline / F01, Ext-F01 | OPEN: `ResearchChair.lua:76–87` ignores city scope in its real loop. | Two local cities, foreign/UNKNOWN/former-holder cases, actual consumer work counts. |
| T02 invalidation closure / Ext-F02 | OPEN: `DistrictCompleteness.lua:135–142,180–198` has broad invalidation with partial owner filtering. | Exercise producer and downstream scheduling together. |
| T03 cache boundary / F38,C025 | OPEN structural risk: `DistrictCompleteness.lua:147–153` fixed eight entries. | Warm 8/9/16/32 plus K boundary. Actual legal >8 hot set is not established by source alone. |
| T04 real shared capture / F02 | OPEN: `EffectiveFacts.lua:13–58` rereads; `RuntimeWork.lua:3–26` currently shares only inside an Audit. | Baseline and repaired real multi-consumer closure; preserve write barriers and copies. |
| T05 recovery budget / F27 | OPEN: `IndustrySupport.lua:68–75,105`; GC partial defer `PerformanceCounters.lua:313–324`. | No-progress budgets, same-value availability recovery and successful siblings. |
| T06 exact retirement / F08,F20 | CHANGED: `RuntimeWork.lua:233–243` RetireOnce exists; Store `831–845` has partial exit tracking. | Former holders, missing old definitions, failures, retry and completion. |
| T07 catalogue/report cost / Ext-F03,F12 | CHANGED: compact `DistrictCompleteness.lua:173–174` exists; `Lv2Housing.lua:23` still detailed. | Count catalogue, presence/location/report and diagnostic work separately. |
| T08 freshness / hold rule | OPEN: `Commerce.lua:225–253` clears on unavailable input; `NetworkBridge.lua:220–224` only partial recovery notify. | Baseline failure, accepted pending-hold/confirmed-loss tests, two real same-turn changes and fresh confirmations. |
| Defect fixtures / F03,F05,F08,F16,B271 | OPEN: `UI/DialogueRefresh.lua:72`, `Gameplay.lua:793–974`, Store `818,831–845`, `UI/CrewProjectOrder.lua:33–41`. | Nil ACTIVE, throwing Start/adapter, failed-once exit, recovery notify and turn-boundary Gold; no assertion weakening. |
| Callback/audit labels and collector / TOOL-02, Ext-F12 | FIXED subset in B271: `PerformanceCounters.lua:58–64,85–94`; `EventTimingDiagnostics.lua:55–69`; `tools/turn_timing_evidence.py:10,29–59`. | Retain OTHER and bounded per-turn collection. S2 does not rebuild already working diagnostics. |
| Scope/fallback and observer native-read attribution / Ext-A0,F12 | OPEN: `CarrierHealthTrace.lua:10–23`, `Commerce.lua:350–378` native reads lack diagnostic-specific accounting. | Add bounded attribution, not a second always-on sampler or inference from output counts. |
| Static alarms / PROP-N2,CR-2 | OPEN/CHANGED evidence: B271 lists observed-unavailable names; `DistrictCompleteness.lua:180` still registers one; `ResearchChair.lua:76–87` proves scope discard. | Add missing-event/scope/detail-reader/retry/producer-owner checks with reviewed exceptions and live replacement coverage. |

#### S3 — Composition and readiness

B273 S3 complete: [actual scope, results and execution closure](../../Status/Validation/Results/Specialization_B273_Refactor_S3.md). Four S2 S3 gates now pass unchanged,23 additional cases pass. Original rows below retain their before basis; no global-audit or native-PASS claim.

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Startup isolation / F05,C052 | CHANGED: a few protected starts exist, but `Gameplay.lua:768` announces INITIALIZED before mostly unprotected `793–974`; seal `1034` can be skipped. | Preserve TradeRouteProbe793→NetworkBridge858, InspirationProbe938→Inspiration940, Dialogue931→retired984; D-3 skip dependents, protected epilogue. |
| Post-commit fan-out / F35 | OPEN: investment commit `Gameplay.lua:655`, fanout657–669, token670. UNIT_ACTION already sets token572 before fanout573–587. | Per-consumer isolation and reliable response receipt; do not “fix” already early-token branches by adding duplicates. |
| Permanent-write observer / LC-01,F18 | OPEN: Store `605–606` saves then invokes observer; outer catch `1554–1557` can HoldCompletion. | Observer failure cannot turn a committed transaction into a failed transaction. |
| Adapter isolation / F16 slice,C055 | OPEN: `UI/CrewProjectOrder.lua:33–41,90–98` unprotected adapter chain. | Native items fail open, SPC items fail closed, shutdown exports clear; registry follows S9. |
| Readiness fallback / F19,C170 | OPEN: e.g. ResearchApply129, Infrastructure156, Chair116, Cross124, TraditionEffects84, Support55, Lv2GPP119, Housing98, NetworkBridge646 only set ready at load event. ReadinessSummary8–12 is a hand-list. | Store-ready latch via load OR first publish/turn; self-registration; diagnostics do not substitute for writer readiness. |

#### S4 — Native defects and the accepted hold direction; stop U2

B274 S4a local recovery subset complete: [actual result/closure](../../Status/Validation/Results/Specialization_B274_Refactor_S4a.md). Industry budget/reentry, GreatWork signature, GC UI deferral and compact Housing pass; network hold/provenance/cold-load and Development startup containment remain S4b. Revised U1 D13 makes U2 an internal checkpoint, no automatic native stop/deployment.

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Great Work city containment / F03,C011 | OPEN: `UI/DialogueRefresh.lua:54–81` whole-loop pcall, nil ACTIVE concatenation72. | Per-city failure/token; preserve signature until S5 hook migration. |
| Network capture city containment / C011,C176,D-2 | CHANGED: `NetworkInput.lua:30–41` already reuses same-reference old facts; `43–44` asserts for first unreadable/nil ACTIVE; Bridge185–188 catches whole capture. | Per-city retained/unknown provenance, not false all-fresh or zero; D-2 approval first. |
| Development startup containment / C176 | OPEN: `DevelopmentInvestment.lua:155–169` all-city pcall then loaded=true. | Isolate failed city and preserve recovery, no transaction-policy change. |
| Removed-unit relevance / F04,Ext-F07 | OPEN: `NetworkBridge.lua:622–630` ignores payload and refreshes all tracked players. TradeRouteProbe124–130 filtering does not protect it. | Check confirmed snapshot trader IDs; unknown cases retain explicit conservative path. |
| Confirmation recovery / B271 §1.1 | CHANGED: `NetworkBridge.lua:174,220–224` already handles AVAILABLE recovery, not equal-value revalidation/signal catch-up; `387–389` rejects stale signal. | Notify coherent availability even without new value revision. |
| D-1 Commerce warm/cold hold | OPEN: `Commerce.lua:89–99` cold cleanup; `225–253` clears on prepare failure. Eligibility precedes network at124,148; owner exit419–425. | Hold only network-derived output, preserve confirmed eligibility/access-marker exits and transaction exclusions. |
| D-1 Culture warm/cold hold | CHANGED: `CultureNetwork.lua:185–191` normally holds warm failure; `237–247` clears installed carriers on first audit. Receiver Identity-only policy100–104 differs from source ACTIVE169–182. | Fix cold path; do not impose a new receiver ACTIVE requirement. |
| D-1 Standardization exact hold | CHANGED: `StandardizationEffects.lua:131–154` retains old sources/merges load values, then writes at181–183. | Retained source set is not “no carrier updates”; hold the combined physical output under D-1. Undecomposable cold-load aggregate plus mixed confirmed source loss/unknown source uses accepted exception A: hold temporarily, recover from relevant facts/availability, never periodic scan. Existing Development contracts are outside this hold. |
| Pending retries / F27,Ext-F06 | OPEN: `IndustrySupport.lua:50–61,68–75,105` repeats pending every publish. | Sample generation, availability/lifecycle wakes and attempt budget, not only bounded queue length. |
| UI_PENDING GC starvation | CHANGED: `PerformanceCounters.lua:217–220,313–324` detects UI pending, deferred reevaluation only for network. | Extend eligible reevaluation; no frequency/threshold increase to mask work. |
| Housing compact facts / Ext-F11 | OPEN: `Lv2Housing.lua:23`; compact fields `DistrictCompleteness.lua:26–32,173` suffice. | Use ReadFacts without eligibility change. |

#### Approved A8 correction — after S4, before dependent propagation work

A8 is no longer excluded: the user explicitly approved eight collection eras after the bounded assessment, correcting the original mistaken count. Extend Inspiration to E0–8/max24%, Dialogue X0–8/max40 per round, valid receipts and total carrier coverage; preserve pool/work-own-era/quota/history. Source: CultureInspirationModel, DialogueProjectModel/Projects/Effects and their SQL; catalogue already spans8. Keep baseline seven-era tests as before evidence and add the explicitly accepted successor tests, not assertion weakening.

#### S5 — Propagation foundation, in a→b→c→d order

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| S5a declared fact-change registry / F02,C027 | OPEN: separate fan-outs `Gameplay.lua:24–53,569–587,598–617,650–670`. | Declared kinds/cause/owner/city/reference/revision; Mark-only, per-consumer pcall; no autodiscovery bus. |
| S5a permanent commit propagation / F18 | OPEN: `IndustrySupport.lua:78–82` filename-filtered wrapper; `InvestmentAction.lua:43–49` Store path skips notifier. | Include investment commits and replace hand-wired chains without losing receipts. |
| S5b typed current identity facts / F02,C133 | OPEN: `EffectiveFacts.lua:13–58` no published revision; native GovernorGate and copies every read. | Property-signature/turn expiry, reference/version and D-15 barriers; UNKNOWN not cached success. |
| S5c D consumer registry/invalidation / C018,Ext-F02 | OPEN: `DistrictCompleteness.lua:135–142,180–198` no registered-consumer API. | Scope producer invalidation and consumer delivery together. |
| S5c network registry/busy merge | OPEN: `NetworkBridge.lua:101–109` fixed list; `254` drops Receive while busy. | Merge pending causes/packets coherently, not duplicate broadcasts. |
| S5c route-signal owner / F10 | OPEN: `TradeRouteProbe.lua:6,130,134` owns signal. | Transfer to NetworkBridge before removing Probe. |
| S5d real consumer locality / F01 | CHANGED: Chair76–87 ignores city; Meaning129–158 and Inspiration120–147 already honor it/merge pending, but broad fallbacks remain225–228/185–190. | Migrate only remaining gaps; verified GameEvents signatures in TargetHook246–268. |
| S5d Dialogue relay / F09 | OPEN: `UI/GPPRefresh.lua:31–41,65–74`; `DialogueEffects.lua:194–206` depends on old dispatch. | **Own hooks first**, then remove relay/retired hooks. Q7 transport remains until S10 duty migration. |
| S5d live native triggers / PROP-N2,CR-2 | CHANGED native evidence: ten unavailable names in B271 §1.5. | Remove/replace each reliance with verified trigger coverage; investigate callback multiplication, not assume 390 native governor changes. |
| S5d indexed invalidator / F30 | OPEN: `RuntimeWork.lua:219–227` installs CityRemoved per NewTargets, scans shared retired caches. | One owner:city index, retaining exact former-holder cleanup. |
| S5d foreign UI marks / F21 | CHANGED: `UI/DialogueRefresh.lua:121–144` has selective work triggers but foreign CityAdded/Removed broad marks135–139. | Gate unrelated marks, preserve legitimate cross-owner exits. |

#### S6 — Shared facts and work; stop U3

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| AnchorFacts/WorkerFacts / F14,Ext-F05,D-8 | CHANGED: SpecialistSupport23–44 helper exists; separate worker/anchor reads in Lv2GPP30–36, Commerce138–145, Development183–190. | One sample, separate per-ability qualification/pillage policy. |
| Compact business D cache / F38,C025,Ext-F03 | OPEN capacity: `DistrictCompleteness.lua:147–174` eight shared entries for compact and lazy detail. | Size business cache to relevant cities and separate report cache, prove T03/T07. |
| Reverse dependency helper / Ext-F09 | OPEN: `StandardizationEffects.lua:208–220`, `CultureNetwork.lua:253–268` enumerate receivers; Commerce200–202 has direct reverse lookup. | Share mechanism without changing source/recipient rules. |
| Capital source read-phase reuse / Ext-F11 | OPEN: `CapitalInvestment.lua:133–148` allocates cache per prepare/destination. | Share only valid phase; keep confirmation's fresh prepare296–298 and current funds/contract checks. |
| Lazy investment quotes / F28 | CHANGED: Development already guards withQuotes237–245 and dirty flush304–314 passes false. Capital Refresh173–186 still prepares all quotes, treasury380 marks all. | Preserve Development's completed improvement; defer Capital expensive quotes while keeping access/confirmation correct. |
| Unit-panel publish replies / F29 | OPEN: `UI/UnitPanelActions.lua:82–100,137`, `UnitTargetMarkers.lua:42–51,89` polling remains. | Event/publish replies with stale-token rejection; shared transport follows S9. |
| UnitTargets scope / F33 | OPEN: `UnitTargets.lua:17–31` whole-owner city/district enumeration. | Scope known deltas while preserving full legitimate target discovery and authoritative consume-site checks39–70. |
| HalfYield normal hot path / F36 | OPEN: `HalfYieldProbe.lua:31–45,74–75` scans outer world before enabled checks. | Move to DEV in S6 or S10; preserve any exact cleanup duty before removal. |
| Carrier feedback recheck / F32 | CHANGED: `DistrictCompleteness.lua:180` CityBuildingsChanged was unavailable in B271. | Do not attribute a native storm to that dead path. Re-evaluate live BuildingAdded/Removed dependencies; no blanket prefix suppression. |
| Network input increments / Ext-F07 | OPEN: `NetworkBridge.lua:185–188` captures before content comparison. | Determine affected references before capture where the protocol proves scope; retain coherent transaction proof. |

#### S7 — Mechanism extraction; approved DDR changes isolated

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| S7a owned carrier kernel / F11,F34,C019 | OPEN: independent kernels ResearchApply48–76, Infrastructure78–105, Chair62–74, IndustrySupport27–37, IndustryWonderEffects28–42. | Define/Apply/Observe/Exit and owned-ID registry, preserving actual native/readback/qualification behavior. |
| D4 immunity + redundant rebuild | FIXED configuration: `Data/InternalCarrierPillage.sql:2–5`, modinfo481. OPEN cleanup: ResearchApply71, Infrastructure97, Chair66, Cross71. | Clean redundant internal-carrier pillage handling in S7a; retain real-building/anchor pillage effects and native-pending label. |
| S7b property cell / F26,C073,ST-02 | OPEN: Store1089–1099 vs ExpeditionSpyStore135–145 vs CrewProjects45–47 differ on setter-error outcomes. | Share readback mechanism with explicit existing caller policies; binary32 handling does not replace Capital's decimal codec. A semantic unification needs a new DDR. |
| S7c turn ledger / F23,ST-01,EXT-01/02 | OPEN: ResearchTradition28–30 and CommerceModel79–81 absorb UNKNOWN_INTERVAL; Commerce133–136 rejects unknown Reputation. | D-6 pause/no-credit/resume and no-bonus policy only after acceptance. |
| S7d three 1T projects / F07,C014,C168,LC-02,TX-N4 | OPEN: ClaimProjects38–49 and DialogueProjects71–80 withdraw UNKNOWN access; EngineeringStudyProjects70–75 preserves it. | Common pure model/controller/UI; divergent outcomes are D-4, not a mechanical refactor. |
| S7d Crew completion/recovery / C167,CR-1 | OPEN: CrewProjects120–131 CALLING/HELD;262–282 shared +1 receipt and init/bind. | D-5 proof-based multi-completion/reobservation; do not invent source attribution or replay uncertain outcomes. |
| S7d Crew consume ownership / F12,C080 | OPEN: `UnitActions.lua:108–127,137–138,154–156` owns consume/add-progress and string classification. | Move to CrewProjects with typed outcomes and existing irreversible receipt guarantees. |
| S7e tombstones / F20 | CHANGED: RuntimeWork233–243 RetireOnce already used by Infrastructure85–92; Cross64–67 and CommerceConvergence8–25 still recurring scans. | Data registry and exact RetireOnce where applicable, not deletion of live exits. |
| S7f common city reference / F31 | OPEN: RuntimeWork238–239 and IndustrySupport14 construct raw token keys. | Store token plus native owner/target checks; do not drop ConstructionProbe19–24 safeguards. |

#### S8 — Store technical lifecycle, not ownership gameplay

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Declared sub-record hooks / F06,C003,D-7 | OPEN: Store93–152 inlines profession validation into one validator. | Registry key/validate/exit/loss/return/P4/tick; Store orders commits. D-7 applies to ability records, not corrupt base identity/envelope. |
| Exit receipts and HELD retry / F08,C009 technical | CHANGED: Store831–845 has per-exit pcall/attempts/in-memory finished;818 rejects missing old definitions;1273–1284 turn ticks lack held-exit retry. | ExitCompleted and bounded turn retry; consolidate legacy exits, missing definition is absent for that retired cleanup only. |
| Deterministic return / C005 | OPEN: Store919 uses pairs without ordered per-observer isolation. | Preserve current gameplay outcomes; missed-loss inference, multi-hop, reservations, tombstones/raze and acquisition remain excluded. |

#### S9 — UI boundary; stop U4

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Adapter registry / F16 rest,PROP-N3 | OPEN: `UI/CrewProjectOrder.lua:30–41,89–108` lists adapters directly. | Registry and owner-specific revisions after S3 isolation; native base behavior preserved. |
| Gameplay-owned rules / F15,D-10 | OPEN: `UI/DevelopmentInvestmentRead.lua:22–46`, `UI/DialogueProjectUI.lua:27–41`, `ExpeditionSpyRead.lua:76–89` (UI includes: `UI/ExpeditionSpyWindow.lua:2`, `UI/ExpeditionSpyActivity.lua:5`). | Move target/era/entry decisions, UI returns raw facts; no A8 count change or Expedition repair. |
| Token-keyed request channel / F25 | OPEN: shared Snapshot/LastToken Gameplay572/670, UnitTargetSnapshot80, polling consumers and UI closures. | Separate player-action/DEV channels; reuse appropriate bounded lifecycle, no protocol weakening. |
| Applied display projection / F17,D-11 | OPEN: InstitutionPresentation74–98 recomputes Reputation/Standardization; actual Commerce gate133–136 can reject those values. | Owners publish applied values/reasons to InstitutionView; retain uncertainty and held effects honestly. |
| One adjacency sampler / F22 | OPEN: `UI/IndustryRefresh.lua:18–23`, `UI/ResearchCrossRefresh.lua:20–31`. | One raw owner/sample with distinct consumer policies. |

#### S10 — Move duties first, then reviewed removal

| Planned item / original IDs | HEAD status and source evidence | Next action / boundary |
|---|---|---|
| Binding/CityFlow/Construction / F10 | OPEN load-bearing chain: EffectiveFacts15→CityFlowProbe18→BindingProbe; Store1490–1491 AllocateFoundation; UnitActions25/121→ConstructionProbe7–26. | Move production readers/actions before quarantine. RouteSignal migration is already S5c. |
| Q1 CultureInspirationProbe | OPEN duty: CultureInspiration7,67,208 depends on retired Probe Withdraw; Probe62–65 returns before its own exit registration149. | Transfer exact withdrawal dependency, not just remove Start. |
| Q2 timing stack | OPEN: CrewProjectOrder67–72 includes ProjectTurnRead/TimedProjectSelection; TimedProjectDisplay8/42/51 references overflow sink while serving formal projects. | Separate production timing/display before Probe retirement. |
| Q3 CrewPrecision | OPEN: CrewPrecision22–27 wraps UnitActions.Run;42–46 records precision and returns original receipt. | Move decorator/observation, preserve receipt. |
| Q4 MeaningProbe / Q5 ExpeditionGate | CHANGED: not Started in current Gameplay; nil-guarded Meaning call613 and modinfo123–125/259/534–549 package references remain. | Remove only reviewed dormant code; retain required SQL unit rows to clean break. |
| Q6 inheritance experiment / CityIdentityMapping | OPEN: Gameplay947–951 isolates inheritance modules, but995–997 starts CityIdentityMapping; latter147–150 listeners,41 writes property. | Remove actual DEV paths/duties as a unit, not claim all inactive. |
| Q7 Dialogue transport | OPEN: Dialogue298–328 ACK/sample; UI/DialogueRefresh25/30–32/41/87/106–107 generation/ready; Gameplay397 paired confirmation; Dialogue30 owned-carrier delegation. | All duties move before file removal, independently of S5d hook replacement. |
| Q8 HalfYield/GreatWorkProbe | OPEN: HalfYield31–45 world loop; GreatWorkProbe14–16 cleanup and37 conditional ready transfer work. | Move to DEV/exact cleanup owner; do not generalize GreatWork as an unarmed every-turn sweep. |
| Other quarantine files | OPEN package entries: modinfo172–173 DiscountEligibility,198–199 CopyYieldRefresh,224 NetworkIsolation,252–253/470 BoostRefresh. Gameplay1010–1011 still starts NetworkIsolation. | Review remaining callers/exports/withdrawal duties before removal; filename alone is not proof of dead code. |
| C075 ActionPanel replacement | OPEN: modinfo50 replacement; UI/TimedTurnProbe2/4–5 original handler capture. | Remove full dead replacement after production timing duties migrate. |
| TOOL-04 removal safety | OPEN: `tools/deploy.py:51–53` rejects runtime-only files; `temporary_playtest.py:37–62` uses a separate receipt transaction. | Review exact deletion allowlist, both deployment paths and complete rollback before removal ships. No unknown-file deletion relaxation. |

### Authorization, dependency triggers and exclusions

The [accepted U1 record](Refactor_Program_U1.md#accepted-u1--2026-10-24) supersedes pending defaults. S2–S10 are authorized after D0058/A0182 synchronization. U2 after S4, U3 after S6 and U4 after S9 are internal engineering checkpoints, not routine native/deployment stops. A concrete blocking native uncertainty requires a minimal user test; ordinary stages continue after local gates. No automatic deployment. U5 is final native integration; main promotion needs a separate decision. D4/D5/D7/D13/D14 revisions apply exactly as recorded, not the original Advisor defaults.

Re-review is triggered by a new consumer, manual-to-automatic use, wider work set/frequency, new recovery path, longer reference lifetime or relevant observed failure, not merely the next profession. This applies now to the four current professions. Report B's P1 timing is read as **before the next dependent use**, with a scoped disposition; it does not revive every historical issue or authorize unrelated fixes.

The following remain outside the program: ownership semantic DDRs (missed loss, multi-hop returns, AF-13, tombstones/raze/acquisitions, Crew/Expedition training and Restructuring outcomes); Expedition functional repairs/reattachment; Meaning GP/DQ, exact District purchase discount, Research network redesign and era UI; fifth-profession vocabulary/ordinary ontology and broader unit framework; promotion-policy/HD dependency declaration/carrier-ID pruning. A8 assessment identified current E/X0–7 versus eight catalogue eras. The user explicitly approved E/X0–8, Inspiration max24%, Dialogue max40 per round and corresponding validation/carriers; pool/own-era/quota/history unchanged. A separate implementation batch follows S4. F24/F37 or other unselected report items do not enter by proximity. If an implementation encounters them as a prerequisite, stop the affected path rather than silently expanding scope.

Existing temporary develop deployment capability is present (`tools/temporary_playtest.py:37–62,111`), independent of main-only stable_gate. No automatic D-13 deployment permission was granted; an approved activation requires stable runtime first, and later switches require exact-receipt restore→activate. Do not invent a new deployment framework or bypass the existing transaction. The old W0003 ACTIVE prose versus Authority-ended state is addressed in the U1 draft only.

User decision: U1 accepted. User testing: final U5, earlier only for a blocking native fact. Primary next: S2→S10 with internal checkpoints; main/live remain B271.298 until separately approved replacement.

---

## Historical record header — 2026-10-21

Date: 2026-10-21
Maintainer: Primary (user-authorized main task)
Basis: develop `718c49b`; accepted source/runtime B266.293 / modinfo293 from `0c2c4ae`. Earlier checkpoints retain their own B249/B204 evidence bases.
Scope: record the user-approved v0.1 roadmap and bounded pre-playtest list after the latest Advisor review. Documentation only; no repair, Design revision, test dispatch, deployment, release designation, PR or main promotion.

## Historical v0.1 approved roadmap — 2026-10-21

This checkpoint governs current scheduling and supersedes conflicting timing in the historical checkpoints below. It does not close findings, expand native acceptance or authorize the complete Advisor implementation roadmap. The user approved recording this plan; implementation stops at separately approved batch boundaries.

### Reviewed basis and comparison

Primary reviewed the Stable local Advisor files under `Specialization/Reports/Advisory/V01_Readiness/`: `V01_Preplaytest_Fix_List.md`, `V01_Architecture_Plan.md` and `V01_Architecture_Register.md`, against the earlier tracked follow-up checkpoint. The Advisor originals remain unchanged and locally ignored. They provide evidence and recommendations, not independent gameplay authority.

- The earlier deferred subjects remain: ownership changes, Expedition, remaining Meaning, exact District-body purchase discount, Research network, era coverage and remaining audit work. Completed repairs are not reopened merely because their historical findings remain indexed.
- The newer review adds cross-cutting concerns: single-city failures affecting empire-wide consumers, persistent HELD/CALLING/UNKNOWN_INTERVAL states, startup/observer coupling, UI-hosted readers, test fidelity, diagnostic coverage and measured performance.
- Advisor P0 includes work required before the next feature; it does not mean every P0 is a blocker for this limited playtest. Merged candidates, watch items and positive findings are not independent defect counts.
- Report descriptions with truncations or stale step references are an index, not an executable specification. Recheck the relevant source and accepted contract before each repair.
- Network fault containment is not automatically non-semantic: skipping a city, treating unavailable facts as NONE or changing freeze/withdrawal outcomes can alter the accepted complete-topology/UNKNOWN policy. A local signature-read guard must be distinguished from that policy decision.
- Diagnostic counters currently shown only in a runtime panel are not assumed to reach the collector. Static checks and inferred engine behavior remain separate from native evidence.

### Ordered work and exit criteria

| Stage | Work | Exit / boundary |
|---|---|---|
| 1. Pre-playtest preparation | Implement the five bounded items below, perform local checks and prepare the player briefing. | Reviewed build and collection path ready; the user designates the first campaign baseline. No separate native acceptance campaign required, but first-session delivery remains to be verified. |
| 2. Integrated native play | Approximately 3–4 campaigns with deliberate coverage, logs, saves, screenshots and UI feedback. | Assess covered and missing scenarios, not campaign count alone. Record defects without silently repairing deferred semantics. |
| 3. Evidence triage and necessary foundations | Reproduce observed failures and implement only foundations actually needed by the next repair: realistic regression fixtures, startup/observer isolation, trustworthy readers and explicit recovery boundaries. | Each dependency is scoped and verified before its consumer repair. Do not require a universal framework or complete foundation rewrite. |
| 4. Ownership transitions | Consolidate the existing Design categories into a rule-to-test matrix, then implement remaining transitions for current modules. | Per-profession outcomes are explicit; relevant loss, return, acquisition and interruption cases are verified. Unsupported acquisition routes belong here. |
| 5. Expedition | Continue root-cause work and repair using the collected evidence and required shared dependencies. | Known supported paths and unresolved engine constraints have explicit outcomes and evidence. |
| 6. Remaining selected foundations and completion work | Select remaining foundational repairs by risk/dependency; integrate approved buttons/icons, UI corrections and balance adjustments. | Balance is assessed on repaired behavior. Existing deferred subjects receive an explicit disposition, rather than being silently declared complete. |
| 7. v0.1 freeze | Audit the intended release baseline and perform final integrated native regression after the last material changes. | Exact baseline, evidence, supported scope, accepted limitations and outstanding work are recorded; promotion/PR still need user authorization. |
| 8. Maintenance and new modules | Apply useful remaining fixes in subsequent maintenance versions, then resume new modules when their prerequisites are ready. | Current correctness/recovery/severe performance risks are resolved or explicitly accepted; foundations amplified by the next module are addressed. Clearing the entire historical audit backlog is not an entry requirement. |

Stages express dependencies, not a ban on iteration. A foundation needed for ownership or Expedition moves ahead of that work. A new concrete blocker is triaged by impact; it does not automatically reopen all deferred findings. The frozen v0.1 baseline remains distinguishable from later maintenance builds.

### Explicit pre-playtest implementation list

These are the bounded changes selected for the next implementation proposal. The prior user–Advisor confirmations establish the intended direction; this documentation batch executes none of them. D1-prime replaces the older proposal to merely raise the fixed record budget from 96 to 144.

| ID / Advisor mapping | Change | Validation and exclusions |
|---|---|---|
| PRE-01 / A4, D1-prime | Remove the fixed per-role limit on meaningful `a.Record` output; deduplicate repeated state reports by meaningful identity/content; retain a runaway breaker with an explicit throttle marker. Preserve the separate native-sampling bound. Make suppression/error metadata collector-visible and review passive-window/ring/reader limits together. | Locally verify state changes survive, duplicates are suppressed, breaker loss is visible and native sampling remains bounded. Buffer sizes are implementation choices to review, not a promise of lossless collection while disconnected. |
| PRE-02 / A5, D2 | Add collector-visible readiness summaries for Store and relevant writers, including startup completion seal, load-event timing and not-ready reasons. | Verify record shapes and readiness interpretation locally, then verify actual new-game/load delivery during play. This observes missing initialization; it does not add automatic startup repair or rewrite all handlers. |
| PRE-03 / A6, D3 P1–P4 | Record Commerce treasury/yield/carrier expectations at turn boundaries, network pending/stale/rejection/drop/verified transitions, and sender state; preserve collector metadata. | Verify bounded output and transition context. Actual treasury accrual timing remains native evidence to collect. Do not change withdrawal, sender or UNKNOWN policy. Optional P5 is not included by default. |
| PRE-04 / A7, D4 | Add bounded carrier-health observation for the identified ResearchSupport/Lv2GPP carriers: load baseline, pillage events and changed health states. | Verify fixed scope and safe reads; use native evidence to determine actual pillage/repair behavior. Do not add immunity, carrier rebuilding or scan all internal types. |
| PRE-05 / A9 | Remove the experimental overflow project's ordinary-play exposure. Prefer data gating after checking startup dependencies; remove definitions only if dependency/save review supports it. | Verify ordinary availability and package/startup references. Do not assume deleting the project is safe merely because it is experimental. |

Recommended execution order: PRE-01 first so subsequent diagnostics are retained; PRE-02–04 next; PRE-05 can be a separate small data sub-batch. Local validation remains required. First-session log delivery is `USER_GAME_TEST_REQUIRED`; no local check is reported as native PASS.

### Playtest preparation and coverage

Preparation is not another gameplay repair:

- Record the exact build, enabled dependencies, supported scope and known escape rules. Use Standard-speed single-player human, the dedicated America/Roosevelt test pair and four professions unless the user separately changes scope.
- Start collection before the new game/load; account for reload disconnect gaps and the collector idle timeout. Preserve saves around important transitions. Verify useful records arrive in the first session before relying on long-run evidence.
- First campaign: basic four-profession operation, startup/new-game/load behavior and UI. Middle campaigns: cross-profession combinations, multi-city actions, restructuring, purchases and interruptions. At least one longer/larger campaign: accumulated history, later eras, reload and performance observations. Targeted short tests can cover rare cases.
- Carry the existing REALLOCATING cold-load and Standardization + Development additive-output checks forward; individual feature acceptance is not combination acceptance.
- Treat approximately 3–4 campaigns as a budget. Maintain a covered/missing scenario list and distinguish natural play from cheats, same-turn from cross-turn results, and observed failures from engine hypotheses.
- Record each session's actual build. UI or diagnostic changes still get revision attribution; SQL/type/carrier/save-shape changes require a compatibility decision and may require a new campaign. Do not combine different baselines as one controlled observation.
- A1 ownership/acquisition failures remain deferred: avoid unsupported transfers/Free City acquisitions and own-city loss; preserve a pre-event save for reload if triggered. A2/A3 use the existing one-at-a-time Crew project and immediate/empty-queue project precautions. Preserve the Expedition briefing, including saves before restructuring/mission operations and the known unsupported purchase/queue combinations.
- A8's eight-era decision remains deferred, not silently implemented here. Review the known era-limit risk before late-era coverage; do not claim late-game completeness while that boundary is untested or excluded.

### Ownership abstraction boundary

Share mechanisms where they actually repeat: city references and transition evidence, reconciliation phases, commit ordering, idempotency, exit notifications, error/retry accounting and common test scenarios. Each profession still owns its Design outcomes: retaining/freezing/clearing/resuming history, contract continuation or termination, withdrawing yields, and unit source loss/rebinding. First record the existing category decisions in a transition matrix; unresolved outcomes go to the user. This plan does not approve a universal state engine or automatic HELD release.

### Release boundary and next action

The current runtime remains B266.293. No alpha/beta/RC tag or first-playtest baseline is created by this document. Release naming can be selected independently of the internal build sequence; approval to document this roadmap is not approval to publish a release.

- User decision: next implementation batch and eventual baseline/version designation.
- User testing: none dispatched by this record; integrated testing follows the prepared baseline.
- Primary next: present the bounded pre-playtest list, then await implementation authorization. No repairs, art application, PR or main promotion in this batch.

## Historical v0.1 playtest scheduling checkpoint — 2026-10-18

The following preserves the earlier B249 scheduling record. The 2026-10-21 roadmap above takes precedence for current timing and dependencies.

The user explicitly moves the following outstanding work to **high priority after the v0.1 native playtest**. This supersedes the earlier before-dependent-module scheduling for this playtest phase. It changes timing, not Design, evidence strength or existing runtime behavior. Previously completed repairs remain completed; existing protections and accepted effects stay enabled as currently implemented.

| Outstanding work | Current boundary and next permitted stage |
|---|---|
| Handling loss of the user's cities, across all professions and shared services | Remaining implementation, diagnosis and native acceptance for city loss and its consequences, including source binding, contracts, histories, re-conquest and loss during REALLOCATING, are post-playtest high priority. The user will avoid own-city-loss scenarios in this playtest. Existing acquisition/claim, ACTIVE changes and voluntary restructuring are not disabled or reclassified by this exclusion. |
| Expedition task bugs, root-cause work and repairs | Post-playtest high priority. Preserve working missions, accepted insights/Tourism/network effects and existing diagnostics; do not restart speculative repairs or require another native diagnostic gate now. Source-loss reattachment is covered by the city-loss row. |
| Remaining Meaning Extension implementation | Post-playtest high priority, explicitly reconfirmed by the user. The automatic seven-domain/five-yield implementation remains; the deferred Government/Diplomacy Culture projection is not silently enabled or removed from accepted Design. |
| Industry exact District-body purchase discount | Post-playtest high priority; still technically unimplemented. Building-specific purchase effects and the accepted Standardization mainline remain. |
| Research network redesign | Post-playtest high priority. The old Research boost remains isolated in v0.1; common topology and other profession networks remain. |
| Great Work era-coverage presentation | Post-playtest high priority. This is the held presentation work, not removal of era facts used by working Culture abilities. |
| Remaining independent-audit and Advisor findings | Post-playtest high priority, including the new Industry audit's remaining follow-ups. Preserve original IDs, severity, refactor-timing recommendations and evidence in their original reports; this is a scheduling override, not closure or implementation approval. The user also intends a later Advisor audit. |

The following two checks instead belong **inside the v0.1 native playtest**, when the user performs them:

- Save and cold-load while a city is REALLOCATING, then continue the same restructuring transaction. The accepted B249 continuous flow remains accepted; no repetition of all passed steps is required. See the [B249 native boundary](../../Status/Validation/Results/Specialization_B249_Native_Review.md#remaining-validation-boundary).
- Observe Standardization and Development Investment on the same eligible building and verify the accepted additive production behavior. [B246](../../Status/Validation/Results/Specialization_B246_Native_Review.md) did not exercise this combination; the individually accepted effects are not a native combination PASS.

No additional test is dispatched by this record. Functional completion takes priority; UI beautification/restructuring, player-text polish and balance work do not become entry gates. A newly observed concrete safety/correctness problem can still be reported with its actual scope; it does not silently restart every deferred audit. Subsequent implementation still requires its own approved batch.

### Meaning Extension clarification

Meaning is not waiting for its first implementation or a P0 toggle. [B166](../../Status/Validation/Results/Specialization_B166_Meaning_Automatic_User_Pass.md) records user acceptance of automatic operation and cold reconstruction. Current `CultureMeaningModel.Domains` contains Campus, Industrial Zone, Commercial Hub, Harbor, Encampment, Holy Site and Neighborhood; `ActiveWriteYields` contains Science, Production, Gold, Food and Faith. `Gameplay.lua` starts the normal `CultureMeaning` writer. Government Plaza/Diplomatic Quarter Culture remains quarantined after the native coexistence failure; the engine-level reason is not promoted to a proved universal rule. Theming is accepted provisionally for v0.1 with a future balance note. Only the remaining work is deferred, not the existing ability.

## Industry implementation audit review at B249

Primary read the Stable local report `Specialization/Reports/Advisory/Industry_Plan_Review/Industry_Implementation_Audit.md` in full. Its reviewed SHA256 is `8a06d2730aefa54f42447acc45eba439993c5ea75113bae2ba8cd20c55e7b079`; its inspected baseline was `8aa10f8` / B246.273, before B247–B249. The Advisor original and its older local report dependencies remain unchanged and locally ignored; this checkpoint records the review in the existing tracked plan, without publishing an additional historical report chain.

The report supports the recorded Industry mainline acceptance within its observed scope; it does not claim all Industry boundaries have native evidence. Primary's bounded checks used the current Industry/Research plans and reading pages, B166/B249 evidence, `CultureMeaningModel`/startup, `Restructuring.Publish`, `CityProgressionStore.BeginRestructuring`, `EngineeringStudyProjects.Refresh`, and the existing B247 cancellation assertion. No tests were rerun and no external DB/performance measurement was repeated.

| Advisor item | Primary review and scheduling |
|---|---|
| F1: unobserved native boundaries | Crew enemy-contact retreat, legal Faith purchase, unfinished-study interruption, non-Standard speeds and the recorded `CREW_NATIVE_COST_MISMATCH` diagnostic gap do not acquire a PASS here. Remaining investigation/verification is post-playtest high priority; no dedicated test is added now. Own-city-loss transitions follow the explicit exclusion above. Reviewing non-Standard-speed coverage does not authorize expanding the current Standard-speed scope. |
| F2: Research Design versus runtime | Confirmed reading risk: `Research.md` retains the accepted formula while B234/current runtime scope isolates the effect. The old contract is retained Design, not an enabled v0.1 effect. This record and Status make the runtime boundary explicit; no Design rewrite or network implementation is performed. |
| F3: stale Industry preparation header | Confirmed: the opening B239 pending wording predates accepted occupancy evidence. Current Status and the B249 checkpoint take precedence. The old preparation wording is recorded as deferred documentation cleanup, not a new gameplay failure or repeated native gate. |
| F4: carrier footprint | The Advisor's B246 loaded-DB snapshot reports 4,554 internal Building rows of 4,875 and 8,797 Mod modifiers of 25,323. Counts are attributed evidence, not a fresh B249 count or proof of CPU/memory regression. Measurement, cleanup-only definition retirement and possible compaction remain post-playtest review candidates. Do not add the suggested pre-playtest timing gate, remove save-referenced definitions, or assume bit carriers stack for this effect. |
| F5: local-test assumptions | Retain the lesson from B236 native amplification and B238 paused occupancy: Design-derived expectations and realistic native transforms matter. The original failures and later acceptances stay separate. This record does not rewrite assertions or claim local simulation proves native behavior. |
| F6: earlier recommendations adopted | Historical positive evidence, not an outstanding repair. Keep completed work completed. |
| F7: cross-profession follow-ups | Additive Standardization/Development goes into the playtest above. B249 already contains identity-exit cancellation of pending Engineering Study in `BeginRestructuring`, the consumer refresh in `Restructuring.Publish`, and a local regression assertion. These static checks refute treating that wiring as wholly missing; they do not prove restructuring cold-load or every Industry transition natively. Crew amplification remains a future balance point. |

User decision: the scheduling above is accepted; no new Gameplay rule, repair or general Advisory proposal is adopted.
User testing: the two named integration checks belong to the v0.1 playtest; no additional test now.
Primary next: prepare the bounded functional playtest plan when requested, using the existing build and this explicit support boundary; do not start a new repair batch.

## Earlier B204 scheduling and publication review

The remaining sections preserve the 2026-10-13 review at `bae883a` / B204. Their before-dependent-module timing and B204 next-step statements are superseded for the current playtest phase by the checkpoint above; findings and publication qualifications are unchanged.

## User-confirmed scheduling

All outstanding findings from both the [independent audit](../Audit/P16b_P17_Final_Audit.md) and [Advisor architecture review](../Advisory/Architecture_Engineering_Audit/Final_Review.md) remain deferred follow-ups, not a blanket block on development. Previously completed repairs stay completed; historical findings are not silently reopened.

Before developing a module that would materially multiply an existing problem or make repair substantially harder, review the relevant finding against current code, propose a bounded repair and obtain the usual implementation authorization. Do that repair before building the dependent feature. This is sequencing, not standing permission to implement every finding.

Historical severity and timing labels, including FIX_NOW, remain evidence of the original recommendation. They do not override this scheduling decision. Local bugs, speculative native risks and cleanup items do not automatically block unrelated work. A newly confirmed concrete safety/correctness risk should be reported with its affected scope, rather than silently ignored or turned into a project-wide stop.

| Development trigger | Findings to re-check before that work |
|---|---|
| Expedition reattachment, repeated missions or N2 rewards | Expedition A/B/D/E/F/G/H; cap ownership, recovery, native-read availability and context-faithful tests |
| New persisted city asset or transaction | AF-01/12/13; independent audit P06a/P07 boundaries; commit visibility, exact receipts, history preservation and recovery policy |
| New investment-dependent consumer or central module integration | SD-01, AF-02/09/10; wrapper return values, actual Start composition and event delivery |
| New high-frequency state writer or carrier family | AF-06/07 and prior hot-path findings; actual notification cadence, facts collection and scoped invalidation |
| New network consumer or Harbor/Commerce route expansion | AF-14 and P13a-Q04; partial/UNKNOWN policy and explicit transport bounds |
| Industry template knowledge or Crew source/inventory work | AF-23 and P07c-F01; reliable presence before initialization and receipt readback |
| First additional profession | AF-28; kind vocabulary and persistence validation, followed only by the shared primitives that profession actually needs |

These are planning triggers, not an exhaustive duplicate finding register or a requirement to finish an entire platform rewrite. Use the linked reports for original evidence and limits. No new permanent registry, manifest or mandatory all-report reading set is introduced.

## Newly reviewed Advisory reports

- [Future specialization feasibility](../Advisory/Future_Specialization_Feasibility/Future_Specialization_Feasibility.md): useful planning inventory for seven future professions. Its strongest reusable themes are unit attribution/training snapshots, route facts, multi-turn projects, and profession-unit lifecycle. Difficulty/carrier-count estimates are advisory forecasts, not measured delivery schedules or native costs. Community and Landscape remain candidates; none enters v0.1 by publication.
- [Self-healing reconciliation proposal](../Advisory/Self_Healing_Rules/Self_Healing_Reconciliation_Rules.md): useful catalogue of stuck-state concerns and proposed recovery policies. None of R1–R20 or D1–D10 is adopted here. Per-feature ownership, irreversible outcomes and existing accepted protection rules remain authoritative.
- Their four [architecture-review dependencies](../Advisory/Architecture_Engineering_Audit/Final_Review.md#8-checkpoint--handoff) are included byte-for-byte at the author's Stable checkpoint, to keep their links and finding IDs accessible. Phase B/C qualifications in Final_Review take precedence over Phase A wording. Publication does not certify every claim.

## Primary review qualifications

### Recovery proposal: not an implementation-ready common policy

1. Returning capacity is not automatically harmless: it permits another admission. A late native birth or an off-map travelling Spy can make a false release produce over-capacity or lose ownership. The reports themselves leave off-map enumeration UNKNOWN. A deadline and an empty visible queue alone do not prove absence.
2. Generation changes only reject observations that can be reliably attributed to a generation. Current `ExpeditionTraining.Birth` and `Complete` native callbacks carry player/unit/city information, not the request generation. The existing Store generation is not proof that arbitrary late native events become safe (proposal R6).
3. A receipt written with a Store transition is not an atomic commit with a native unit destruction or reward operation. R7 needs an explicit per-operation readback/uncertainty contract; it does not remove the native-action crash window.
4. Saved history is authoritative for facts that the engine no longer retains. It must not be downgraded to a disposable belief and rebuilt from current observations. UNKNOWN remains distinct from absence and confirmed loss.
5. The proposed local-turn/load reconciliation must not replace foreign-event paths needed for loss exits or UNKNOWN recovery. `LoadScreenClose` and turn-start are candidate hooks, not proof that every required UI/native fact is ready.
6. R19's one-write-per-city-per-turn limit cannot suppress ordered transactions or real same-turn changes. Coalesce only redundant derived recomputation; define actual collection cost before claiming linear complexity.
7. Releasing a hold, choosing partial aggregate fallback, dropping an uncertain reward, or accepting older save shapes can alter accepted semantics. Decide these per feature before implementation, without adopting a universal release rule or adding an unapproved save-compatibility obligation.

### Feasibility report: preserve uncertainty and incremental sequencing

- Source-visible modifier/API examples are implementation candidates, not native PASS. Statements that no route exists mean no route found in the inspected sources, as qualified in the report's limits. External HD version remains UNKNOWN; current installed behavior was not independently re-tested here.
- Re-read current accepted Design when a feature is scheduled. Candidate names, unresolved formulas, and draft diplomacy/landscape/community directions remain at their existing maturity.
- Do not automatically schedule every proposed spike, an entire platform batch, a global turn scan, or GC changes. Inherit applicable existing evidence; request only the new native uncertainty for the actual batch.
- Static re-check of `CommerceConvergence.outputChanged` confirms an unscoped Audit after a changed global revision at a publish/playback callback, but multiple writes before that callback can coalesce. The report's shorthand “each write costs a world audit” is not a measured one-to-one invocation count, CPU cost or memory attribution.
- Source history since the architecture-review basis has no Mod change, but does include the new publication-gate test. “Source unchanged” must not be read as all DevelopmentTests being byte-identical.

## Review coverage and publication boundary

Primary read both new reports in full, revisited the architecture review's final priorities/limits and Stable handoff, checked Design maturity excerpts, and spot-checked `RuntimeWork.Hook`, `CommerceConvergence.outputChanged`, `CrewPrecision`'s wrapper, `ExpeditionTraining` queue/receipt callbacks, and `ExpeditionSpyGate`/Store load and generation boundaries. This is bounded publication review, not a second complete architecture audit. No external game-source rescan, gameplay regression, native experiment or new API availability claim was made.

The older local `Publication_Safety_Audit` report is not included in this publication. Its conclusions about zero deleted paths and expired credentials need author-side qualification before publication; its no-hook/path-remediation observations also predate `cb28bb6` and `bae883a`. It remains unchanged and ignored. Raw logs and frozen evidence remain untouched.

The six included Advisor originals are immutable for this checkpoint: no editorial rewrite, change of findings or hidden adoption. Primary's qualifications live here. Before staging and commit, verify their bytes still match the reviewed checkpoint; check local links/anchors, staged privacy/secrets, exact file scope, and current context integrity. A privacy PASS establishes only the scanner's covered patterns, not complete absence of sensitive information.

User decision: scheduling above confirmed; recovery/feature design proposals remain unaccepted.
User testing: none requested; existing B204 native test remains pending.
Primary next: resume normal authorized development; consult relevant findings before the dependent module, propose scoped repair where required, and wait for implementation authorization.
