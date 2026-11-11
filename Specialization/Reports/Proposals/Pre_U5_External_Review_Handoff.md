# Current-HD Pre-U5 — Targeted External Code Review

Primary handoff, 2026-11-06. **Review input, not Architecture authority, acceptance, deployment permission or a new convergence plan.**

**Current result and deployment boundary:see section9. Sections1–6 preserve the original B412 review input;they are not a request to repeat that completed audit.** The original current-HD repair slices and disposable multi-Crew evidence probe were submitted for a bounded source review. Local checks exist; native completion attribution, the original-HD U5 baseline and later HD-independent migration remain separate gates. Do not reopen the accepted overall architecture or treat this as a whole-repository audit.

## 1. Fixed input and authority

| Item | Review value |
|---|---|
| Formal contract | Accepted Design D0059 / Architecture A0184; current Authority/Status supplies later execution scope, not the historical PU01-only authorization wording |
| Before Pre source | `fb7be65b664b78f2c692cdc9d661511f37823b2e` — first accepted formal synchronization, before PU01 implementation |
| Review source tip | **`b8622426a50cef08beff6253bcf9de77a10944a6` — B412.439 / modinfo439** |
| Scope measurement | Runtime diff:30files,1195insertions,167deletions; this is a source review size, not a performance result |
| Tested Mod/DevelopmentTests/tools identity | SHA256`aae215526454f1f5ee4a8738835b1ab20be9ae50424fd9ccfaee48dfb52e780e`,bound successfully to the review source commit |
| Actual runtime | Recorded live remains B399.426; source B412 has **not** been deployed/run in game. Recorded main remains B307.334. No live readback was performed here. |

The commit containing this handoff may be later than the source tip; handoff/current-record changes do not widen the runtime review. If the source tree changes, identify the exact delta rather than silently reviewing moving HEAD. Preserve frozen evidence and existing accepted decisions.

## 2. Reviewer task — copy this section into Claude Code

Act as an independent scoped reviewer. Follow root/project AGENTS and W0005 role boundaries. Inspect the fixed source range above against the accepted contracts below. Read-only production/test/formal files; existing offline tests may run without game/socket/configuration/deployment changes. Write only your own scoped Advisory result if authorized by the review session; do not commit/push or apply repairs. No new probe,code migration,Design decision or package deletion is requested.

Answer whether the current-HD Pre repair candidate and **its disposable probe** contain an actionable local correctness/safety defect before the Owner's targeted native evidence. Keep actual code defects separate from already-declared native unknowns, historical failures and later O-package obligations. Do not use missing native evidence to fabricate a local fix or weaken irreversible-operation proof.

Start with a short Chinese Owner summary. Then provide findings ordered by practical impact,each with exact source line,trigger/before-after outcome,affected scope,contract and a minimal counterexample or existing executed evidence. Indicate `local fix required`, `Owner semantic decision`, `native evidence required`, or `deferred outside this slice`. Finish with a narrow readiness conclusion,not U5 PASS or general architecture approval. If no local blocker is found,explain that unresolved native attribution remains open rather than declaring every slice complete.

## 3. Minimum reading route

1. Root [AGENTS](../../../AGENTS.md),[project guidance](../../AGENTS.md),branch [Authority](../../Workflow/Authority.json) and [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state). Do not load all historical batches by default.
2. [Architecture CURRENT and accepted convergence boundaries](../../Architecture/Specialization_v0.1_Architecture.md#current-authoritative-state),[P01–P10 and evidence-driven defensive engineering](../../Architecture/Specialization_v0.1_Architecture.md#runtime-integration-contract--p01p10). Follow only relevant current Design objects/qualification sections for the purpose under review.
3. The accepted [ordered slice table](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/fb7be65b664b78f2c692cdc9d661511f37823b2e/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/Architecture_Convergence_Integrated_Roadmap_DRAFT.md#4-ordered-slices-gates-and-rollback-boundaries),as preserved planning evidence,not a second authority or a request to repeat C1–C5/Tier design review.
4. [Engine Reference ER01/ER02](../Technical/Engine_Reference.md#er01--completion-events-separate-identity-consumed-fields-and-unknown-semantics),[S7d6 completion proof limit](../../Status/Validation/Results/Refactor_S7d6_Crew_Proof_Gap.md),[B238 native review](../../Status/Validation/Results/Specialization_B238_Native_Review.md#results-and-diagnosis). Single delivered completion does not establish multiple-city ordinals/late-duplicate semantics.
5. Source diff and the relevant owner/test rows below. Expand by real calls/shared boundaries,not into unrelated profession designs or all Engine Reference material.

```sh
git diff fb7be65b664b78f2c692cdc9d661511f37823b2e..b8622426a50cef08beff6253bcf9de77a10944a6 -- Mod
git diff --name-only fb7be65b664b78f2c692cdc9d661511f37823b2e..b8622426a50cef08beff6253bcf9de77a10944a6 -- DevelopmentTests tools
```

## 4. Actual repair responsibilities and targeted checks

| Responsibility | Source entrypoints | Check against actual consumers |
|---|---|---|
| Fact availability/use and reliable infrastructure negatives | `FactUse`,`CurrentSpecializationFacts`,`DistrictCompleteness`,`SpecialistSupport`,`ResearchInfrastructure/Apply/Chair/Cross`,`Commerce` | Required UNKNOWN is not zero;known negatives revoke correctly;purpose-independent domains remain usable;same-reference second changes/write fences stay fresh. Existing Governor algorithm was tested,not gratuitously replaced. |
| Native action prepare/confirm | `RestructuringUI` | A prepares once and becomes inert;B alone confirms matched plan/unit;no extra native operation/replay. |
| Responsibility delivery | `FactChanges`,`FactConsumerBindings`,`NetworkBridge` | phase0 order;owner responsibility registered before ACK;false/missing/failed/skipped/throw retained;old ACK cannot clear newer work;same-value recovery scoped;no idle retry/all-city scans. |
| Crew receipts and source proof | `CrewProjects`,`CrewModel` | Per-source/order unresolved receipts separate from consumed high-water;CALLING precedes native creation;valid B can proceed after independently proved +1 while A remains unresolved;unknown unit/source/outcome never replayed. **PU05b is not repaired.** |
| Reputation/locked investment terms | `CityProgressionStore`,`CommerceModel/Commerce`,`CapitalInvestmentModel/CapitalInvestment`,`UI/CapitalInvestmentPanel`,`UI/CommercePanel` | Lawful exit resets only required reputation fields;confirmed/inapplicable/narrow policy-zero/unsafe distinct;STABLE has no irrelevant reputation dependency;VENTURE locks provenance;no repricing signed contracts or unknown payment resets. |
| First completion source and project access | `CityProgressionStore`,`ClaimProjects`,`DialogueProjects` | PU07 selected source option A;do not poison unrelated cities or invent first history/clear sticky errors without proof;UNKNOWN preserves installed markers but grants no new starts/rewards;confirmed negatives/used-era quota still withdraw. |
| Mandatory cleanup | `RuntimeComposition`,`Gameplay`,`ExpeditionTraining` | Fixed29exit/23return duties across34owners survive failed/skipped/missing Starts;actual callbacks retain ownership/exact IDs. Training busy/throw/failed removal/save/reentry never pretends completion. |
| Diagnostic absence capability | `DevelopmentTests/refactor_harness.py`,`test_pu11_package_absence.py` | Actual modinfo entry/include visibility,throw/silent-nil and forbidden globals,fresh VMs;real roots/Flight/GC. Expected missing PerformanceCounters failure is characterization,**not** O7 independence PASS. |
| New disposable evidence | `CrewCompletionDiagnostics`,`Gameplay:954–958`,`UI/CrewProjectUI:112–113`,`tools/collect_expedition_trace.py` | Protected seams do not control owners or wrap existing callbacks/readers;no authority writes/operations;bounded native reads/retention,zero idle sampling,explicit missing hook/truncation,actual on/off/absent equivalence. |

Corresponding maintained tests: `test_pu01_fact_use`, `test_pu02_restructuring_ui`, `test_pu03_delivery`, `test_pu04_negative`, `test_pu05a_receipts`, `test_pu06a_reputation_exit`, `test_pu06b_reputation_use`, `test_pu06c_capital_terms`, `test_pu07_source_attribution`, `test_pu08_cleanup`, `test_pu09_marker_roots`, `test_pu11_package_absence`, `test_b412_crew_observation`. Read/run only the closure needed for a finding.

## 5. Evidence and limits

- Latest probe gate: **103unique selected local methods,22new+81retained**,no errors/failures/skips;149observed source modules/fragments. These counts overlap earlier batch suites and are not additive path coverage.223Lua5.1,25XML,5artdef,346runtime/345package,157own includes;0new/widened static alarms. Source-bound digest and privacy checks passed.
- CPython3.14.8/source-built Lupa2.8 Lua5.1,explicit repository native/SQL controls,no live DB/game/socket. Do not accidentally run the historical Lua55 wheel or a shadowing `/tmp` test module and call it the same environment.
- [Status S0895](../../Status/Specialization_P0_Status.md#crew-completion-probe-ready-locally--s0895) records exact test suites/limits. Local full artifact: `local/refactor/B412_crew_observation-0760be0aa85c4eaabbea637e56b7ae41/closure.json`,SHA256`ae3c7ed74dfb04391a6ff4c4f17a653e1ef667db498f1e8122ba1b77c2b01e7a`. Runner/transcripts/static output are alongside. **Ignored local artifacts/hashes are not permanent backups**;versioned source/tests allow comparable new runs,not recovery of old execution bytes.
- Minimal probe checks,when the verified Lua51 environment is available: set `PYTHONPATH=<source-built-lupa>:DevelopmentTests`,then run `python3.14 -m unittest test_b412_crew_observation test_pu05a_receipts test_refactor_s7d6_proof`. No native attachment is part of those tests.
- Existing S7d6 tests intentionally pass by reproducing the deficit/conditional ambiguity;they do not prove desired grants work. Trace sequence/BEFORE_CREW/AFTER_CREW identify observer ordering/registration placement,not a native unique completion. Verify observed order against actual `CREW_BOUND/CREW_HELD`;native registration/delivery order is not certified by local fixtures.
- Probe reuses the existing20-project UI reader;it exports aggregate counts/progress/queued project counts,**not** full queue size/current slot identity or a completion-instance ordinal. Owner/city/turn checks label returned currentness only. Raw event strings/objects are safely redacted or type-marked;arguments beyond12/orders beyond8 are explicit truncation.
- Frozen older ResearchHealth assertions,four B138 GC functions and the previously documented obsolete startup/marker/template assertions remain NOT_PASS where recorded. They were not weakened or relabeled;check an affected real path if relevant,do not mass-repair historical fixtures or treat every inherited mismatch as a new regression.

## 6. Still-open gates and exclusions

Native same-tier/same-turn Crew attribution/possible late duplicates remains OPEN. PU07 fully unbound first-source/post-fault cold behavior and native queued-marker removal remain unproved. Current-build new-game/same-build-load support is inherited;Capital3/Crew2 changes require a new campaign for the eventual candidate deployment. Source/package rollback is not saved-history or native-money rollback.

P3 production Flight/currentGC/error/facts/ACK/exact-cleanup transfer and true valid-save on/off/absent certification remain later affected-owner/O7 work. No file/SQL retirement,HD-free Tier/provider/UI migration,ownership gameplay,Expedition feature fix or GC-policy change is included. No new broad/random pillage/trader-death campaign. Existing accepted culture/research evidence remains scoped and retained.

No external review or native test is claimed performed by writing this handoff. Request only the smallest missing native fact needed to distinguish the existing histories;one short run cannot prove arbitrary late callbacks impossible.

## 7. Owner native-test checklist — after separate deployment approval

- **B413.440已获批部署，346/346文件核对一致（源码02d732e，Status S0901）。** 使用B413新档／该构建自己的存档，不用旧构建存档承诺迁移。
- 照常先运行 `tuner -300`，并在施工队测试期间保持采集。已核对本机快捷入口指向develop采集器；无需打开P0面板来启用新探针。
- 两座工业城最好均为工业三级，选择同一等级、同一价档的施工队，各一份，安排在同一回合自然完成。Cheat Panel可协助城市准备／生产力设置；本组完成尽量不要直接点强制完成，以免混淆事件路径。
- 记录实际产生几只队伍及发生回合。若严格保护导致未发放，保留现场和日志即可；本版只取证，不承诺已修复多城发放，也不要手动补发来充当通过。
- 主测试先做；取消／重选前先冷读同构建存档，避免尚未确认的取消事件可能提前启动观察窗口。另作零进度／已有进度取消后重选；条件方便时留完成前一回合的同构建存档，复读一次。不要人为触发Lua完成事件来证明原生重复行为。
- 每个Lua上下文先保留最多8条相关前置事件；普通工期不会提前启动窗口。首个已核实项目类型的施工队完成事件起最多6回合，总量仍限64条事件、256次城市访问、32次原有UI读者调用和192行加停止记录。前置截断会明确提示，缺少已发布施工队订单线索的普通事件不会为探测相关性而访问城市；超限或读不到会明确提示。若要继续另一轮，可冷读同构建存档重新开始窗口。无新事实时不周期重试。
- 采集结果在既有忽略目录 `local/diagnostics/B205/session-*/`。`summary.txt`包含 `crew_proof:`摘要；`records.log`保留收到的 `CREW_PROOF_EVENT/STATE/STATUS`。检查Gameplay/UI各自ARMED、Gameplay AFTER_ATTACHED以及缺钩子/截断/环覆盖提示；缺失不是通过。无需另开大规模能力验收。

Primary next:the Owner authorized the narrow delta review below. No game,probe run,deployment or main promotion;request deployment only after that recheck.

## 8. B413 narrow short recheck — current request

Owner explicitly authorizes this short independent recheck after local repairs;do not repeat the original overall architecture audit. Fix the reviewed source at the commit containing this section(**B413.440**,tested source digest below);base is`d88a144e3ee6c383c4f92bfe27aaeb553e141fc7`. If HEAD is later,report its exact delta before using it. Read-only source/tests/formal records;return findings only,do not repair,write,commit,push,deploy,launch game or expand the audit. Native multi-Crew attribution remains OPEN.

- P-1:cheap confirmed Crew project/published order-view/already-observed-city relevance precedes city/Property access. At most8pre-completion related events share the existing total64-event cap;after that,ordinary construction makes0native samples. The six-turn window begins only on a verified Crew project-completion event. No unverified completion/cancel argument interpretation. Inspect whether retained completion budget,explicit truncation and bounded followup remain sound;early ordinary events without an existing published Crew hint are outside the observation claim.
- P-2:Stop clears pending/city state and leaves fixed inert callbacks;no Remove at all,including mid-snapshot Stop. Inspect real Crew/Store on/off/absent equivalence under snapshot,tombstone and shifting live-list dispatch installed before registration. Confirm the actual `InitUnit`/order/receipt path is tested,not only callback counts.
- L1:within existing Commerce guarded read phase,same-reference confirmed anchor failure/zero workers wins over UNKNOWN_GOVERNOR. Unknown anchor/workers/reference and mutation still hold;no governor cache,new eligibility,network/transaction/formula/save change. Actual Store+EF+DC+catalogue+Commerce fixture covers it.
- L3:maintained CommerceState fixture now exposes ReputationInput;original IV20-turn16→III15 business assertion is retained.
- L4:versioned`DevelopmentTests/run_pre_u5_review.py` owns execution and explicit Lua51/legacy-fixture profiles. Only B245 Receipts/Guards and PU06a MoneyReceipts get the existing synthetic numeric/f32 adapter;current protocol/terms/strict-source cases do not. Original obsolete B245 TraceAndScope byte-equality/UI assertions remain NOT_PASS/not selected,not erased or weakened. Confirm comparable runs need no ignored runner.
- L5:actual Gameplay missing CultureDiagnostics must register nonzero missing attempts;BackgroundRoutes has an explicit0-attempt non-consumer check and no absence-coverage claim. No production include added.
- L2:intentionally retained global EffectiveFacts write fence/D recapture cost. Current Status assigns the later O1 shared-fact slice and concrete correctness/work gates;do not optimize or mark resolved.

Read only the changed runtime4paths,maintained fixture/tests/runner and relevant current Status/RIC;expand to actual consumers only if needed. Relevant fixed tests can run via the versioned entry;full local artifacts are optional supporting evidence,not needed to discover execution steps. Return a short Chinese Owner summary,any actionable defect with source lines and a concrete counterexample,and scoped readiness. No native/U5/deployment PASS.

Local result:258unique selectedPASS(13new),0failures/errors/skips;157observed source modules/fragments,not full path coverage. Fixed-B412 comparison:8expected defect failures with exact original production sources. Lua51/package:223Lua,25XML,5artdef,346runtime/345package,157own includes;0new alarms. Source digest`24e1e879f01460539a7908d1ad7e33f3362d407bb0e6a0966f6d75b6cfa85ea8`. Artifact`local/refactor/B413_review-cfb0abde9724478c8a8175e8c8a5649b/closure.json`,SHA256`9db1eb0c90e249bf0983e839ada9004252c057f1fe8e2a73cb880ce6abef9c0f`;before artifact`local/refactor/B413_before-4b9d7e9f7cf0444ea5d48396853fb787/closure.json`,SHA256`4747a90d2ffc66fbad424222882816fce24fb319dc61d381275a69a9b5d2ebeb`. These ignored files/hashes are not permanent backup. Versioned command:`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<lupa-environment>:DevelopmentTests python3.14 DevelopmentTests/run_pre_u5_review.py`;add`--before`for fixed-B412 counterexamples.

## 9. Owner-returned short review and D-1 completion

Owner supplied the completed Claude review of`d88a144..102bb16`on2026-11-06. It confirms P-1/P-2/L1 and L5 locally sound;L2 remains OPEN. Its sole new defect is test-only D-1:the shared Commerce fixture unconditionally calls ReputationInput while exact historical`afd2204`has no such function. The fixture now conditionally exposes that field;the versioned gate includes the unchanged S7c FrozenD6 and CommerceFallback cases and protects selection of the frozen/current16→15 regressions.262selected local methods pass;the8original fixedB412 counterexamples remain characterized. All346Mod files are byte-identical to reviewed102bb16;no runtime build bump or production edits. Current evidence/limits are in Status S0900.

The returned review explicitly waives another external round for this exact one-line condition and test selection. No native/U5 PASS follows. L1's display-only observation is not repaired;other inherited historical-test failures are not counted as PASS. Native same-tier/same-turn completion attribution and prior PU07 boundaries remain OPEN.

Future external review coordination belongs to the Owner:Primary prepares scoped materials and entry only,without calling Claude or submitting/polling via CLI,tools or computer use. Next request deployment approval for B413.440;do not deploy,launch the game,advance another package or repeat the architecture audit automatically. After approved deployment,main two-city natural completion comes first;cancellation/reselection starts after cold-reading the same-build save because cancellation event semantics remain unverified.

Deployment update(2026-11-06):Owner approved B413.440;receipt`B413.440-02d732e-playtest.json`isDEVELOP_ACTIVE and346/346files MATCH. Prior request-for-approval wording in section9 is historical;the current gate is Owner-native evidence under Status S0901. No game launch or native PASS.
