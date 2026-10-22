# Audit follow-up priorities and Advisory publication review

Date: 2026-10-21
Maintainer: Primary (user-authorized main task)
Basis: develop `718c49b`; accepted source/runtime B266.293 / modinfo293 from `0c2c4ae`. Earlier checkpoints retain their own B249/B204 evidence bases.
Scope: record the user-approved v0.1 roadmap and bounded pre-playtest list after the latest Advisor review. Documentation only; no repair, Design revision, test dispatch, deployment, release designation, PR or main promotion.

## v0.1 approved roadmap — 2026-10-21

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
