# Evidence Appendix

Investigation / Non-authoritative / No design decision implied

Status: Stable | Maintainer: Primary

Source baseline: `920b4ed2a8da5dd394b95fe03f96c81dc2a8a069` (develop and origin/develop matched; tracked tree clean on entry).

Current formal metadata: D0058 / A0183 / S0866. Recorded runtime: B399.426 from `491517093de18c8b151053724e316f1e08228995`; stable/main B307.334. This audit did not re-run deployment verification.

[Overview](Executive_Overview.md) · [Matrix](Gap_Matrix_v1.md) · [Decisions](Decision_Register.md)

All source paths and line numbers below refer to the source baseline, not the eventual report-publication commit. Repository-relative locators retain evidence without private machine paths. Short source ranges identify the relevant function; they are not claims that every unrelated branch of the file was audited.

## 1. Evidence meaning and method

- **STATIC_CONFIRMED:** read current source/contracts; a reachable error path is not evidence it occurred natively.
- **Recorded LOCAL_SIMULATION_PASS:** attributed to a prior result and its exact selection/environment; no gameplay tests were rerun here. Available test names alone are coverage leads, not PASS.
- **Recorded USER_GAME_TEST_PASS/FAIL:** only the user's named scenarios in frozen results; this audit did not reopen raw archives or saves.
- **INFERRED:** a reasoned consequence or work shape; **UNKNOWN:** not established.
- No CPU/heap profile, native event signature experiment, DB scan, broad foreign-Mod audit or optimization measurement was performed. Current handoff directions and formal contracts remain distinct.

Read ledger: routed root/project/Investigation guidance, W0005 role/language/publication, Authority metadata and Status CURRENT. Read current Architecture clauses, Network Design and accepted U1/recovery scope, prior Reconstruction/Logical/Direct Listener evidence and B396 main/major evidence leads. Followed named fact/binding/Store/owner/transport/presentation/deployment paths and existing test definitions. Three disjoint read-only reviews covered facts, notification/recovery, and ownership/extension; Primary integrated and spot-checked high-impact source paths. No other Mod files, historical archive sweeps or whole-repository content audit. New report files only; old evidence remains frozen.

## 2. Source and contract index

| ID | Current source/function anchors | Contract / result / scope |
|---|---|---|
| E01 | Status/Specialization_P0_Status.md:1–27; Workflow/Authority.json current metadata | D0058/A0183/S0866; U5 held; latest user handoff supplies current audit authorization, not source implementation permission |
| E02 | Status/Validation/Results/Specialization_B399_Network_Project_Coverage_Reconciliation.md:1–49 | Narrows route/Claim tests; ordinary network evidence sufficient; original engineering obligations distinct from player tests |
| E03 | Mod/NetworkSender.lua:19–78; Mod/UI/BackgroundRoutes.lua:213–241; NetworkBridge.lua:20–23/371 | B397 result and test_b397_network_transport.py:77–295; current three-way signal equality and bounded lifecycle witnesses. B399 ordinary recovery supersedes older “awaiting user” status |
| E04 | Mod/Commerce.lua:40/148–165/323–356 | workers() emits COMMERCE_WORKERS_UNKNOWN; prepare failure code survives; finite hold allow-list lacks it; domain0 can reach apply. resolve() failure at337–339 instead holds |
| E05 | Mod/ResearchInfrastructure.lua:31–54; SpecialistSupport.lua:45–65 | ACTIVE assertion precedes independent anchor negatives in Infrastructure; SpecialistSupport has negative-first precedent. A0183:143 priority |
| E06 | Mod/EffectiveFacts.lua:20–42/78–123/127–230; Probe.lua:320–346; CurrentSpecializationFacts.lua:3–18; DistrictCompleteness.lua:69–100/143–156/182–240 | Phase-local known-only reuse, owner/ref/write barriers; retained D and separate availability. A0183 P01/P06/P07 and handoff Principle A |
| E07 | Mod/GreatWorkFacts.lua:30–85/132–264/266–285/362–377; CultureAestheticModel.lua:13–16; CultureMeaningModel.lua:48–51; CultureInspirationModel.lua:14; CultureAesthetic.lua:89–95; CultureMeaning.lua:108–116; CultureInspiration.lua:110–115 | Retained confirmed work data, current-only passive consumers, current detached completion sample; per-consumer pending notifications |
| E08 | Mod/FactChanges.lua:97–104/116–160/182–203; FactConsumerBindings.lua:11–46/52–122; Gameplay.lua:837–848; RuntimeWork.lua:55–103/226–231/265–290; NetworkBridge.lua:126–143 | Immediate scalar invalidation; deferred attempts; distinct owner recovery. Proof emission failure stamps signature before fallible EmitDerived. A0183:146/166–175 |
| E09 | Mod/Commerce.lua:16/240–279; CultureNetwork.lua:137–173/308–314; NetworkRecoveryStore.lua:15–45; NetworkRecoveryCell.lua:112+ | Recovery model/cell/adapter exist but production consumer wiring absent. A0183:16–23 and approved Recovery proposal; s9g1/g2/g3/g4 tests are prerequisites, not actual cold consumer proof |
| E10 | Mod/StoreSubrecords.lua:100–201; StoreDeferredLifecycle.lua:6/23–66; StoreLifecycleRecovery.lua:14–63; CityProgressionStore.lua:1061–1109/1127–1167/1439/1471 | Real production restore/deferred episode recovery and deterministic repair. A0183:17–23/640; approved Recovery proposal per-ability baseline table |
| E11 | Mod/CityProgressionStore.lua:340/823–825/2102–2109/2127–2128 | completionError is durable admission gate; no clearing assignment located. No native occurrence confirmed |
| E12 | Mod/IndustryHistory.lua:48–61/180–210; EngineeringStudyProjects.lua:66–92/122–147 | E coverage strict unknown; present N union distinct from completion E. test_industry_history.py:231+ deliberately preserves coverage downgrade |
| E13 | Mod/ClaimProjects.lua:91–107/111–139/144–186; CityProgressionStore.lua:872–897 | Full-turn native call guarded; direct native completed handler differs. test_b124_claim.py:59–60 intentionally accepts direct completion; event cancellation semantics not proved |
| E14 | Mod/CrewProjects.lua:272–292; Architecture/Specialization_v0.1_Architecture.md:98–100/638 | D5 unique request/unit/source/completion required. test_refactor_s7d6_proof.py:22–34 characterizes unresolved ambiguity, not successful multi-city attribution |
| E15 | Mod/ResearchTraditionEffects.lua:68–84; Gameplay.lua:249–281; InstitutionPresentation.lua:59–101; PlayerActionReplies.lua:147–159 | Applied publication exists, but current institution request derives percent via Shadow(age), presentation derives Standardization percentages. A0183:642/D11 |
| E16 | Mod/CityProgressionStore.lua:39/44/105/504–590/736–748/780–806/1349–1428 | Fixed subrecord keys and explicit ability business transitions; shared reliable commit with model interpretation |
| E17 | Mod/CityProgressionStore.lua:202–212/1237–1248/1270–1278/1311–1313/1334–1395/1442–1449; ClaimProjects.lua:111–129 | City identity vs unique original-type anchor; return waits for exit and matched native episode. A0183:82–106; broad ownership guarantee explicitly absent |
| E18 | Mod/Probe.lua:5–6/135–149; CityIdentityRead.lua:93; EffectiveFacts.lua:5/89; CityProgressionStore.lua:105/1963–1974; RestructuringModel.lua:4; NetworkInput.lua:29; NetworkBridge.lua:533/690–691; Lv2GPP.lua:17–19; InstitutionPresentation.lua:6–30; UI/LevelBannerModel.lua:4; UI/Institutions.lua:48–49; UI/CapitalInvestmentPanel.lua:8 | Verified representative registration/edit seams; not all lists have the same business purpose. A0183:645 excludes unapproved fifth-profession runtime vocabulary |
| E19 | Mod/CityProgressionStore.lua:1563–1592; InvestmentAction.lua:126–143; Restructuring.lua:203–225; CapitalInvestment.lua:76/137–172 | Parent CAS/readback; intent→unit reservation→native destruction→receipt; no cross-object automatic atomicity or safe blind replay |
| E20 | Mod/ClaimProjects.lua:183–197; DialogueProjects.lua:299–307; EngineeringStudyProjects.lua:217–244; Standardization.lua:283/298–306; CultureNetwork.lua:478–492 | Completion/history/boundary listeners have unique duties; conditional fallback listeners are not normal duplicate registrations. Direct Listener Audit remains older source evidence |
| E21 | Mod/Gameplay.lua:32–42; Mod/UI/DialogueRefresh.lua:55–81/110–122/147/167; GreatWorkFacts.lua:30–52; DistrictCompleteness.lua:85–100/265–306; FactChanges.lua:66–94 | Complete GW proof city census, selected slot recollection, whole-building D sample, scoped and owner fallback, load-bearing owner network-generation wake. Work shape only |
| E22 | Mod/Gameplay.lua:862/874–876/906–918/930/995–998/1002/1012; EffectiveFacts.lua:80; CityFlowProbe.lua:18/126–129; ConstructionProbe.lua:7–26; CultureInspiration.lua:70/198; Mod/UI/DialogueRefresh.lua:26–46/94–99; Dialogue.lua:38–61/298–327; Mod/SpecializationP0.modinfo:50 | Production duties in legacy/probe names; old Dialogue positive writer and Half loop already retired. P08 and original S10 Q1–Q8 |
| E23 | tools/deploy.py:35–56; tools/temporary_playtest.py:37–94; Architecture/Specialization_v0.1_Architecture.md:643 | Formal deploy explicitly rejects removed extras; temporary exact-hash transaction lacks same removed-diff review. Both need reviewed deletion/rollback before shipping removed files |
| E24 | Architecture/Specialization_v0.1_Architecture.md:20/92–112/172/186; Mod/DistrictCompleteness.lua:28–44/69–74/216 | Cache prose says <=8 shared; code has business2048/report8. Compact revision includes building rows. Separate approved history owners need precise wording |
| E25 | Mod/PerformanceCounters.lua:9/155–165; earlier Reconstruction/Scan_Inventory.md; B396 performance sections | dc_failure exists but is not in that exported work boundary list. Not every recorded scalar means collector coverage. No new like-for-like native timing/memory result |
| E26 | Mod/RestructuringUI.lua:38–47; Restructuring.lua:203–225; Specialization_B399_Button_Treasury_U5_Review.md:7–24 | Missing prepared-A inert guard; helper replay does not reproduce whole native visual mapping; actual controls/async timing remain unknown |
| E27 | Specialization_B399_Fifth_Playtest_20261101.md; Specialization_B399_Button_Treasury_U5_Review.md; Specialization_B399_Queue_Repair_Removable_Boundaries.md | Scoped native acceptances; nonblocking extra41/52, separate displaced-Expedition issue, multi-item queue deferral. Not architectural root-cause proof |

Paths in the last column without a directory are relative to `Specialization/Status/Validation/Results/` unless explicitly named otherwise. `Architecture/`, `Design/`, `Workflow/` and `Reports/` source documents are under `Specialization/`. All `Mod/` and `DevelopmentTests/` paths are repository-root relative. Within a source-anchor cell, unprefixed Lua basenames denote files under `Mod/`; UI files are explicitly prefixed `Mod/UI/`.

## 3. Per-fact inventory

| Fact / authoritative owner | Source and confirmed value | Failure, first acquisition and invalidation | Retention/scope/recovery |
|---|---|---|---|
| F01 identity/Potential/ACTIVE — Store + EffectiveFacts/GovernorGate | Store original/current identity, reliable investments, six governor fields; ACTIVE=min(Potential,ceiling) | Invalid/missing/inconsistent governor remains UNKNOWN; no synthetic ACTIVE. Native/Store changes invalidate; writes barrier both sides | Only synchronous known phase reuse, owner/id/xy/token/turn/Store witnesses; no generic cross-event ACTIVE retention. E06 |
| F02 D — DistrictCompleteness | Native districts/buildings, completion/pillage and ordinary catalog | Failed capture retains e.value, sets unavailable/error; first no value UNKNOWN; dirty before D notification | Business2048/report8/inflight8; new dirty/new turn/explicit relevant miss captures; load clears. Consumer READY policy separate. E06 |
| F03 Great Works — GreatWorkFacts | UI complete city/slot evidence, Gameplay epoch/turn/input/reference/catalog validation | Unknown sample preserves matching confirmed values; dirty availability separate; absent first sample unavailable | Session reference-scoped values; new accepted sample and same-value availability recovery notify; pending failed consumer retry separately bounded. E07 |
| F04 network — Bridge/Input | Complete accepted routes + current city role facts; provenance confirmed/retained/unknown | Never UNKNOWN=empty. Topology pending differs from one unreadable source. First no snapshot unavailable; full proof remains strict | Epoch/seq/signal/ref/generation fences. Warm source samples, current D-1 installed-output hold; approved cold D-2 attribution not wired for Commerce/Culture. E03/E09 |
| F05 workers — phase sharing over native getter closures | Plot GetWorkerCount through consumers; integer and parent/plot/ref checks | Failed read not cached, first unknown. Sampling does not decide locked vs auto native/HD semantics |2048phase entries/inflight8; no retained worker across events. Different consumers retain independent eligibility. E06 |
| F06 anchors — SpecialistSupport + shared phase geometry | Enumerated city districts; owner/id/type/completion/pillage | Successful missing/pillaged is a confirmed negative; thrown enumeration is UNKNOWN; check actual ability rule | Phase-local. CultureNetwork independently captures geometry because recipient identity gate differs from ACTIVE gate; collection reuse opportunity only. E05/E06 |
| F07 Reputation — Commerce subrecord, Store-owned tick | Saved age/cursor/origin plus reliable turn ledger | Unknown Reputation gives0 bonus, preserves other lawful Gold; absent optional record differs from isolated bytes | City token/ref, strict origin and missed interval protection; config writer cannot mutate reputation. E16; Commerce.lua:148–155; A0183:639 |
| F08 city ability histories — own models + Store reliable commit | Tradition/Dialogue/Engineering/Insights/templates/contracts, each explicit schema/receipts | Isolate unknown/damaged subrecord; deterministic repairs first; no guessed paid outcome or arbitrary zero | Per-city parent/ref/CAS; real persisted deferred lifecycle witnesses. Current known baseline gap not solved by generic cache. E10/E16/E19 |
| F09 Industry Wonder credit and Crew assets — independent approved owners | Completing-civilization E vs city N; player completion observations vs unique source/unit/request receipts | Historical coverage gap cannot become complete through current possession; cumulative count not grant proof | Dedicated history/asset owners and protected native outcomes; strict permanent history, not passive LKG. E12/E14/E19 |

## 4. Per-consumer uses and restrictions

Rows name actual consumer families; shared facts are not automatically usable by all of them. This is the core requested fact/use inventory, not an inventory of all UI or diagnostic functions.

| Consumers | Facts/interfaces used | Use class and current behavior | Migration restriction |
|---|---|---|---|
| ResearchSupport | EffectiveFacts and SpecialistSupport.Anchor (ResearchSupport.lua:16–18) | Passive base support; confirmed anchor gate | Preserve exact negative/pillage/ACTIVE precedence |
| IndustrySupport | Role/anchor plus validated UI adjacency sample (IndustrySupport.lua:24–33; SampleLifecycle.AnchorReference) | Passive support driven by base adjacency, not weighted D | Preserve sample/ref confirmation and source-specific formula |
| Lv2Housing | Role/anchor and D.ReadFacts ordinary tier presence (Lv2Housing.lua:20–40) | Passive housing, tier facts distinct from support adjacency | Preserve qualification and complete/pillage rules |
| Lv2GPP | EffectiveFacts worker sample and anchor; GP-class mapping | Passive GP carriers; actual native worker semantics remain separate | No reopening HD auto/locked assignment campaign; not worker allocator |
| ResearchApply | CurrentSpecializationFacts + D.ReadFacts | Passive specialist support; requires current READY | Candidate retained D behavior needs DEC-01; do not use worker-trigger count as value dependency proof |
| ResearchInfrastructure | EffectiveFacts then D/worker/anchor | Passive flat infrastructure; ACTIVE-before-D order E05 | Confirmed exact exit should not wait behind unrelated UNKNOWN |
| ResearchChair | EffectiveFacts + D + workers | Passive qualifying building effect | Preserve qualification/pillage and own readback; current READY gate not transaction reader |
| ResearchCross | Current role and confirmed adjacency input | Passive district adjacency projection/retained installed output | SampleLifecycle confirmation and values have separate windows; no assumed generic fact-cache migration |
| ResearchTraditionEffects | Current role, stored Tradition age, Applied publication | Passive percent; history origin/aging itself strict | UI must consume actual applied result; retained passive input cannot invent age |
| CultureAesthetic, CultureMeaning, CultureInspiration | Current role, GW Summary and D models | Passive effect; current KNOWN/READY checks, warm holds | No implicit old-GW authority for project rewards; preserve existing floor/formulas |
| DialogueEffects | Role/history + current KNOWN GreatWorkFacts.Summary snapshot | Passive cumulative reward projection | Permanent Dialogue completion remains separate; confirmed negatives and invalid history handling remain explicit |
| CultureNetwork | Bridge effect view, city Insights, sourceSamples, receiver identity anchor | Passive network projection; receiver gate differs from local ACTIVE | D-1/D-2 and whole-set provenance; no copying SpecialistSupport ACTIVE rule |
| Commerce | role, D, actual workers, selected domains, source native yields, Reputation, CurrentEffectPartners | Passive Gold plan; role/domain generations also support TransactionCurrent | Fix G03 separately; source read failure already holds; unknown Reputation bonus0 stays |
| StandardizationEffects | role, templates, Engineering L, Bridge effect view | Passive self/network max carrier result | Freeze entire combined physical output while topology pending; Standardization-only cold exception |
| IndustryWonderEffects | current role, Wonder age/era/history | Passive older-Wonder production | Source era/history policy remains independent; no eight-era collection shortcut |
| CapitalInvestment | current EffectiveFacts/D, Commerce.TransactionCurrent, CurrentCapitalSources, Store contract, Treasury | Irreversible quote/debit/settlement; saved contract terms may survive route loss | No passive LKG authorization; signed-contract settlement does not acquire a new route gate |
| DevelopmentInvestment | current role/D/workers, strict outgoing partners, Gameplay targets and quote facts | Irreversible debit and existing contract effects | Capacity must be current when signing; later worker loss does not cancel lawful signed contract |
| InvestmentAction, Restructuring | Store/admission/reference/current Potential, prepared target, native Unit receipts | Irreversible identity/investment and destruction | No generic retry; held outcomes retain evidence; UI plan is not authority |
| ClaimProjects | frozen candidates/current queue, timer, unique district, native completion | Permanent identity outcome; timer and direct event proof differ | DEC-08; shared timing does not prove cancellation authenticity |
| DialogueProjects, EngineeringStudyProjects | strict role, owner-specific history, Queue/WorkSet/boundary and native completion | Permanent reward/quota/L mutation | No common cancellation policy; unknown current production neither canceled nor complete |
| CrewProjects/UnitActions | source admission, living/queue inventory, player count, exact unit/source receipt | Irreversible formation/consumption | Count difference not extra grant; D5 and unknown native outcome guards remain |
| InstitutionOverview/Institutions/Presentation, banner, P0 | typed read projections, Store summary, derived current role, owner records | UI/diagnostic; not business authority; some candidate math remains | Desired vs applied vs retained vs unavailable must be explicit; no new sampling/writes from display |

Core anchors E04–E20 and earlier Reconstruction/Shared_State.md locate the implementations. Representative direct reader lines: ResearchApply26–43; ResearchInfrastructure31–54; ResearchChair34–47; CultureAestheticModel13–16; CultureMeaningModel48–51; CultureInspirationModel14; Commerce123–165/183–206; Capital137–172; Development208–221; NetworkBridge620–660. No blanket assertion that every family uses the same façade.

## 5. Representative actual event and update chains

**Governor/worker:** NativeFacts.lua:16–37/45–64 invalidates scoped freshness and emits ACTIVE/WORKERS. FC phase0 then phase1; binding calls owner Audit/Mark under Gameplay.lua:837–848 read phase. Owner Pulls facts and reconciles own effects. Owner-local publish/turn recovery is separate. Registration is immediate; effect completion can be later and failure is not globally acknowledged.

**Building/district/pillage:** DistrictCompleteness.MarkDirty143–156 marks before emission; hooks265–306 use verified owner/city where available, owner fallback otherwise. D is captured on demand, then profession model computes and effect owner applies. OnDistrictConstructed supplies type/xy rather than a verified city ID here, so do not narrow it by assuming an argument signature. Internal carrier notifications must be reviewed by real owned-ID/scope behavior, not a universal prefix claim.

**Great Works:** events invalidate input362–377 → UI/DialogueRefresh complete city census/selective cached slot collection → Gameplay391–424 independently validates GreatWorkFacts and legacy Dialogue and pairs the receipt → per-consumer callbacks/failed-only new-sample recovery → passive models. Legacy Dialogue positive yield retirement does not remove transport/ACK duties.

**Route/source:** UI route sample → NetworkSender strict current signals/epoch/sequence → Bridge Receive/full proof → availability/provenance published → NETWORK notification → owner Pull/effect/strict credential. Role source changes also affect owner COMMERCE generation; owner-wide proof wake is load-bearing. D-1 prevents topology-pending physical rewrites except priority confirmed eligibility/owner/reference exits; current proof permits later D-2 isolated source handling.

**Load:** composition preserves dependency order → Store validates/reconstructs lawful records and deferred episodes → session fact caches rebuild → named transport lifecycle witnesses obtain proof → owners reconcile effects. Not every queued duty is persisted or rebuilt by one generic queue. Pending cold source attribution and late lifecycle return still need their specific proof.

## 6. B396 current disposition, not 197 new tasks

B396 baseline is `eeb4a08`/B396.423, older than this audit. The 23 high/medium evidence entries reduce to the groups below; duplicated finding IDs about one transport defect are not separate work packages. Selected low/unverified leads were followed only where they intersected the authorized facts/notification/lifecycle/extension scope.

| B396 IDs / claim group | Current disposition | Basis and remaining limit |
|---|---|---|
| PA-COM-06, PA-NETGW-01, URC-01, VSM-01 | NET-1 repaired | E03 current equality + recorded real-module tests and ordinary B399 recovery; not a live latch claim |
| PA-NETGW-02, URC-02, VSM-02 | NET-2 repaired with bounded recovery | E03; actual original dropped-operation point remains inferred, not a new native fact |
| REFACTOR_STATUS-09, VSM-03 | “No positive Commerce/Industry evidence” is superseded | B397 Industry and B399 fifth tests/coverage reconciliation; retain scene-specific limits rather than repeat all abilities |
| VSM-04, REFACTOR_STATUS-01 | Cold attribution production gap remains | E09; do not confuse production deferred lifecycle recovery with unwired network attribution |
| A_IND-08 | Strict E coverage limitation confirmed; decision, not unsafe-credit defect | E12/DEC-07; existing tests deliberately preserve uncertainty |
| PA-RES-06 | Observability limitation remains partly supported | E25 exported counter list omits dc_failure; no global assertion that all hold reasons never log; no new probes |
| A_ROLE_04 | Strict Store/phase fault boundary; recovery-completion question | E06/E10; current deterministic/deferred repairs real. No evidence every permanent failure can lawfully clear |
| A_ROLE_05 | Sticky completionError remains | E11/DEC-13; no native occurrence proved; no guessed first-completion reset |
| FUT-02 | Current unique-anchor assumption confirmed; future DB/native claims not re-queried | E17/E18/DEC-10; kind registry cannot solve anchor multiplicity |
| SF-01, PERF-01, PERF-02 | Whole-catalog/GW work exists | E21; older Scan Inventory omitted UI GW detail; no current CPU ranking or measured gain |
| PERF-03 | Multiple audit entrances/read-phase windows remain | E08/E21; phase cache is not a single native-turn global cache |
| PERF-04 | Broad route/source wake opportunity, not automatic defect | E21; verified foreign relevance and former-holder exits must precede narrowing |
| PERF-06 | Standardization retained work is a bounded-history/recovery concern | Standardization.lua:283/298–306 and prior audit; approved history discovery means direct turn listener alone is justified. No new frequency profiling |
| WORKLOAD-01 | Comparable before/after closure not established | E25/DEC-12; native campaigns differ; local visits != CPU/RAM |
| REFACTOR_STATUS-03 | Full cumulative U4 closure not established by this audit | Read existing individual results only; do not sum selected passes into a clean full suite |
| DLA-04/DLA-05 | Prior class-D “turn discovery is legacy” too broad | A0183 approved history + E20; retry/work scope can still merit targeted evidence |
| DLA-07 | Claim completion/cancellation authority remains unknown | E13; intentional historical direct-completion test prevents calling it a new timer regression |
| PA-COM-10/PA-COM-11/PA-COM-12 | Not exhaustively revalidated | G03 is concretely checked; do not adopt all Commerce report/provenance leads by association |
| PA-COM-13 / dead names and conditional listeners | No automatic deletion finding | Successful composition/Start/guards matter; native event availability is not proved from name or Add presence |
| REFACTOR_STATUS-06/07/08 | Applied display, retirement and narrow document drift remain | E15/E22–24; staged work, not permission to clean now |
| EFFECT-09 / late recapture | Safety barrier confirmed; eventual recovery unproved | E17/DEC-14; local combined test first, no new ownership policy |
| VSM-05/07/08 | Current test disposition narrowed by user | HD GPP repeat tests not required; ownership/pillage uncontrolled/excluded; transitional baseline explicit |
| PERF-08/other low scope leads | Opportunities only where actual dependency/work evidence exists | E21; no blanket foreign-event filtering or deletion based on old counts |

The old report's counts, panel scores, 98-session measures and CPU/performance implications were not re-derived from raw logs. They remain historical evidence, not current denominators. Unreviewed lower-severity claims remain leads, not silently confirmed or refuted.

## 7. Existing test and native evidence ledger

| Locator | What it can support | What it cannot support |
|---|---|---|
| DevelopmentTests/test_b397_network_transport.py:77–295; frozen B397 Network Proof Transport result | Recorded87-method final selection, actual Sender/collector/Bridge/bindings and strict transaction guards; unchanged content, first drop, bounds/replay | Not fresh execution in this audit; not every legacy suite green. B397 records baseline historical failures explicitly |
| test_great_work_notifications.py:17–113 | Existing owner-specific pending/latest-fact/reference/failed-only notification cases | Generic FC consumer completion protocol |
| test_refactor_s5c2.py:59–133 | Existing negative/source/route ordering composition assertions | Every native event signature or optional unknown branch |
| test_refactor_s9g1.py:28–77; test_refactor_s9g2.py:28–51; test_refactor_s9g3.py:46–108; test_refactor_s9g4.py:20–60 | Codec/cell/adapter lifecycle/domain-provenance prerequisites | Production Commerce/Culture cold writer integration |
| test_refactor_s9f4.py:46–166; test_refactor_s8b10.py:17–36 | Actual deferred lifecycle/atomic parent recovery and terminal Claim-timer cleanup assertions | Generic all-subrecord zero baseline or unknown payment repair |
| test_store_write_boundaries.py:137+; test_industry_history.py:231+ | Existing CAS/loss/return/write-failure and persistent E-coverage uncertainty tests | Missing historical E reconstruction |
| test_refactor_s7d1.py:104–151 | Real Claim/Dialogue/Study owners share Queue/WorkSet/full-turn mechanisms | Identical UI opt-in policy or identical irreversible completion proof |
| test_refactor_s7d6_proof.py:22–34 | Explicit unresolved same-counter multi-city Crew characterization | Multi-city unique grant PASS |
| Specialization_B395_Culture_Research_Playtest_20261029.md; Specialization_B397_Industry_Playtest_20261031.md | Scoped accepted Research/Culture/Industry effects, ages/projects/ordinary actions | All future changed paths, native plunder/ownership guarantees |
| Specialization_B399_Fifth_Playtest_20261101.md; Specialization_B399_Network_Project_Coverage_Reconciliation.md | Ordinary source/route changes and cold proof recovery, three Capital settlements, Development/Reputation/REALLOCATING described scenes | Deliberate dropped packets, corrupt/unreadable sources, all unique Crew and Claim settlement outcomes |
| Specialization_B399_Button_Treasury_U5_Review.md | Prepared-A guard defect; bounded duplicate Commercialization/direct-payment exclusion | Full native UI hitbox cause or ultimate external41/52Gold source |

Frozen native results are cited, not rewritten; raw private logs/screenshots/saves remain outside this report package. No additional mandatory player campaign is introduced.

## 8. Deliverable verification and handoff

Document QA: all six new Markdown files decode; all20 local report links resolve;117 distinct source-anchor groups resolve to existing files and valid line bounds. Three scoped cross-reviews were incorporated, including corrected support inputs, Dialogue effect-versus-completion sampling, confirmed-exit exceptions, deployment-tool asymmetry and migration-baseline dependencies. Line-bound checks prove location, not semantic truth of every claim. The dependency Mermaid source was reviewed for node/edge consistency but was not renderer-tested (no local Mermaid package was available; none was installed). Existing tracked files and the index were unchanged before explicit report staging. This is document QA, not code/runtime acceptance. Publication uses the existing staged privacy/credential gate separately. All G rows have a classification, evidence locator, decision/disposition, dependency and testable exit; all DEC items distinguish unresolved decisions from already accepted constraints. Current formal sources and existing reports remain unchanged.

User decision: review Decision Register. User testing: none now. Primary next: stop after the reviewed report checkpoint; approved target v2 and any subsequent implementation require the next task boundary.
