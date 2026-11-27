# Contract and fail-fast audit of internal modules — 2026-11-25

Author: Primary (Claude). Requested by the Owner on 2026-11-25. Baseline: develop `af09068f` (runtime B545.572). Chinese reading summary: [Contract_FailFast_Audit_2026-11-25_zh.md](Contract_FailFast_Audit_2026-11-25_zh.md).

Evidence level: STATIC_CONFIRMED (code reading). No test, deployment or game run was part of this audit, and no source was changed. Each finding was checked for its producers and callers, the tests that pin the guard, and documents that record a hazard. Every Medium finding was re-verified by Primary against the source.

## Question and method

The Owner asked for two principles, **design by contract** and **fail fast**, to be applied to modules that do not talk to the game engine directly, plus the internal functions of mixed modules. The audit looked for two things:

1. **Defence against imagined problems.** An internal consumer re-checks the type or format of data that our own code produced, and quietly falls back when the check fails.
2. **Over-defence.** Retries, fallbacks, second paths or compatibility branches with no evidence that the case can occur.

What counts as a boundary (kept, not a finding):
- Engine API results, database rows and engine-serialised operation strings.
- The availability and freshness of saved properties and cross-context data: nil before the producer starts, older revisions, load ordering, partial writes.
- Hazards with recorded evidence.
- Irreversible-operation receipts and the S7d6 gate.
- UNKNOWN, PENDING and HELD states that Design or Architecture defines as gameplay meaning.

What does **not** count as a boundary: the type or format of payloads that our own code in the same package produced, whether they arrive through `shared.*`, ExposedMembers, LuaEvents or a save property written and read on the same build.

Sites were classified as **K** keep, **F** fail fast (the contract already guarantees the shape, so the guard hides bugs), **R** remove (unevidenced over-defence), or **Q** Owner question. Only F, R and Q are findings. Modules were grouped as A (persistence and lifecycle), B (facts and catalogs), C (models, scheduling and network internals) and D (wiring, mixed gameplay modules, diagnostics and UI helpers). The module inventory is in ignored `local/contract-audit/inventory.tsv`. The per-group working notes, which hold the full producer, caller, test and document evidence, are in `local/contract-audit/{A,B,C,D,D2}_notes.md` and `VERIFY_notes.md`.

Civ6 caveat that applies to every F recommendation: an `error` raised in an event handler does not crash the game. It aborts that callback and can leave a half-written state. A fail-fast check must therefore sit before the first write, or inside an existing pcall or occupancy boundary that already handles a throw (Architecture "Store普通写与故障占用（B169）").

## Verdict

- **44 findings:** 0 High, 4 Medium, 40 Low. One Medium (CA-D13) was downgraded to Low during verification.
- **No guard produces a wrong gameplay number on the supported path today.** The codebase is already broadly fail-fast: models, Store writes, FactChanges and RuntimeComposition assert their preconditions.
- **The real weakness is visibility, not the presence of guards.** In four places a programming error is caught and turned into an ordinary-looking UNKNOWN, HELD or PENDING state, or a field that nothing reads (theme T1). Fail-closed containment is the right policy there, but discarding the cause makes a bug look like a designed state.
- **The largest volume is noise:**
  - dead branches kept alive only by test fixtures (T2);
  - presence checks on modules and methods that always exist (T4);
  - re-validation of our own payloads (T3).

  These cost readability and occasionally hide a skipped registration, but do not change results.

## Themes and findings

### T1 — Swallowed errors (fail fast in the sense of "fail visibly")

| ID | Sev | Class | Finding | Location |
|---|---|---|---|---|
| CA-A02 | Medium | F | Per-city turn ticks catch errors and store them in `d.commerceError` / `d.traditionError` / `shared.PermanentWriteObserverError` / `facts.trainingReferenceObservationError`, none read in production. A failed tick is absorbed by TurnLedger as an ordinary gap (zero credit, `TurnLedger.lua:4-6`); a repeating failure is invisible. Keep the per-city pcall; surface the error through Status/Describe or a bounded print. | `CityProgressionStore.lua:581-589, 620-631, 40, 350` |
| CA-C01 | Medium | F | `ReputationInput` wraps `ValidateReputation` in pcall and returns UNKNOWN `COMMERCE_REPUTATION_VALIDATION_UNAVAILABLE`, dropping the error text. The only caller (`CityProgressionStore.lua:557`) passes a non-isolated record already validated at load and before every save, so only programming errors reach it. This conflicts with Design's "错误及来源可见" (Commerce.md:100/205). Drop the pcall on the non-isolation path, or carry `why`. The isolation / SEVERE_LEAF branch :65-73 stays (D0059). | `CommerceModel.lua:74-75` |
| CA-D07 | Medium | F | `code()` maps any uncoded Lua error (nil index, etc.) to a generic reason (`COMMERCE_STATE_UNKNOWN`, `STD_READ_PENDING`, `REST_READ_FAILED`); Restructuring's pattern even matches any upper-case word. The city stays HELD with its old effect and the cause is lost. Keep HELD-not-zero (design); record the raw error as CapitalInvestment.lua:17-22 and CultureNetwork already do. No test asserts the collapsed codes. | `Commerce.lua:46`, `StandardizationEffects.lua:27`, `CrewProjects.lua:25,102-103`, `Restructuring.lua:15`, `DevelopmentInvestment.lua:14` |
| CA-C05 | Low | F/Q | `PlayerActionReplies` type/NaN/inf/metatable checks on payloads built by our Gameplay producers; on rejection Gameplay records only a generic `PLAYER_*_REPLY_UNAVAILABLE`. UNIT_ACTION has no Fail reply at all (`Gameplay.lua:481-485`; Fail exists only for View/Targets/Presentation, `PlayerActionReplies.lua:73,119,166`), so the requesting UI relies on its own timeout, if any (not traced). Keep `Accepts`, P05 transport budgets and fresh-table copy. Tests pin the checks (`test_refactor_s9c4a.py:25`, `s9c5a.py:21-24`, `s9c6a.py:27`). | `PlayerActionReplies.lua:38-48,53-69,80-115,125-163` |
| CA-B05 | Low | R/F | FactConsumerBindings probes for methods our modules always define, with a three-name fallback (`RoleFactsChanged`→`RefreshFacts`→`Refresh`). For non-ordered rows a missing method silently drops the propagation with no `d.errors` entry (Standardization refresh, DialogueProjects access, EngineeringStudy credit, Lv3Support/Lv3Effects). Keep "target nil" (real startup failure); assert on a missing method. | `FactConsumerBindings.lua:13,21,113-115,154-157,167,191` |
| CA-B06 | Low | F | FactUse turns producer shape violations into UNKNOWN, indistinguishable from a real UNKNOWN for its only consumer (Commerce). Keep ready/availability, `activeStatus`/`investmentPending` and `depthError` (Tier rule). | `FactUse.lua:18,20,25,28,32,35-36` |
| CA-B08 | Low | F | Bad internal input to ReverseDependencies disables the whole index for the session; callers fall back to full recomputation, violating the P05 work bound silently. Keep the capacity disable; assert on bad scope/shape. | `ReverseDependencies.lua:11,22-23,27,43` |
| CA-B10 | Low | F | DistrictCompleteness tolerates fixture-only shapes (missing catalog entry → `UNREVIEWED_BUILDING`, contribution 0 = silent under-count). Assert in `Calculate`; the existing pcall'd read at :241 already turns a throw into "temporarily unavailable". `test_shared_d_fact_read.py:316` uses `unplaced`. | `DistrictCompleteness.lua:28,31,69,75-76,129,140` |
| CA-B04 | Low | Q/R | Layered pcalls around the training observer. Hazard B391 (B396 audit #17) justifies one pcall around the observer call, not around plain field lookups or counter increments. `test_b393_observer_isolation.py:50-60` pins the current shape with throwing metatables. | `EffectiveFacts.lua:282,290,297,303`, `CityProgressionStore.lua:345-351` |

### T2 — Test-only or legacy paths kept in production source

| ID | Sev | Class | Finding | Location |
|---|---|---|---|---|
| CA-A01 | Medium | Q | Legacy two-record adapter (`legacyTest`, `modern==false`), schema-1 / PREPARED / Import support and the `shared.BindingProbe` path stay in production source. Architecture line 131 sanctions `StartLegacyTest` for explicit fixtures, so this is a recorded choice; production only calls `Start` (`Gameplay.lua:634`) and `loadIndex` rejects schema 1 (L1723), but `validate()` still accepts schema-1 shapes. Many tests depend on it (`test_p0_e2*`, `test_b108_e2_multicity`, `test_effective_facts`, `test_city_flow_resume`, `test_refactor_s8c5c`, refactor_selection.json). Retiring it to Git history like B528 is a test-migration batch. | `CityProgressionStore.lua:159,172-176,243,246-252,956,961,1553,1574,1626,1687-1697,1776-1789,2022-2049,2195-2198,2400` |
| CA-D13 | Low (downgraded) | Q | InvestmentAction keeps a second ledger authority for an irreversible debit: if the Store does not own the city, read/write go to the city property. Unreachable in production because every entry first calls `facts()` → `EffectiveFacts.Read`, which asserts `Store.Owns` (EffectiveFacts.lua:108); the `OnPermanentCityWrite` call is dead (`Gameplay.lua:770`). Same fixture family as CA-A01. Fixtures: `test_p0_k.py:605`, `test_refactor_s5b.py:29,103`, `test_pu04_negative.py:41`, `test_refactor_s7f.py:75`. | `InvestmentAction.lua:13-15,44-55,186` |
| CA-B01 | Low | R | Dead legacy authority in EffectiveFacts: `CityFlowProbe.lua` no longer exists, `shared.CityFlowProbe` is set only in tests, and the property-ledger fallback :116 is unreachable after the :108 assert. About 5 fixtures need the real Store. | `EffectiveFacts.lua:63-64,107-112,116` |
| CA-C06 | Low | R | NetworkInput "untracked city" branch needs `shared.CityFlowProbe.ready` (never set in production), calls `Store.BlocksLegacy` (CA-A01) and a DEV property. | `NetworkInput.lua:86-93,98` |
| CA-A05 | Low-Medium | Q | Subrecord rebuild candidates (`KnownCandidate`, `TemplateMetadataCandidate`, `CompletedClaimCandidate`) and deferred-lifecycle machinery repair shapes no current writer produces (B333: "no false producer exists"). Accepted under D7 / SAFE-004 (D0059) before the same-build-only policy (Architecture:47). | `StoreSubrecords.lua:135-203`, `CityProgressionStore.lua:1180-1226` |
| CA-C07 | Low | R/Q | NetworkIsolation controller retired in A0187 (`test_o8_residual_cleanup.py` asserts `shared.NetworkIsolation==nil`), but `isolated()`/`isolatedForProof()` checks remain (always false) and `ExperimentalStop` is unreachable. A0187 deliberately left them. | `NetworkBridge.lua:20,28,33,55,171,234,300,365,405,552,682,739,831,918,972-985,1025,1034`; `Commerce.lua:48`, `CultureNetwork.lua:68`, `LegacyCleanup.lua:131`, `RuntimeGC.lua:90`, `NetworkSender.lua:18`, `UI/BackgroundRoutes.lua:101` |
| CA-C08 | Low | R | NetworkBridge public functions with no production caller: `d.Read` (B031 DEV report + `detailPage`), `ConnectedKinds`, `National`, `RecipientSources`, `DiscountBatch`, `CurrentNational`, `CurrentConnectedKinds`, `ExperimentalStop`, and the `confirmedOnly=false` arm of `currentView`. About 13 tests call them. P08 retirement with test migration. | `NetworkBridge.lua:684-686,697,787,791,800,804,808,917-970,972` |
| CA-C03 | Low | R | `bitParts` / `DiagnosticParts` have no caller; `Parts`' `variant` parameter is dead (only caller passes two arguments). Side note: no Gameplay module sets `v.diagnostic`; the UI diagnostic path `UI/BoostGreatWorkRead.lua:265-330` (from `P0Panel.lua:70`) looks fixture-only. | `CultureMeaningModel.lua:83-89,112-114,120-124` |
| CA-C04 | Low | R | RuntimeWork fixture-only arms: EffectiveFacts `NewReader`/`Inspect` fallback (both always exist, `EffectiveFacts.lua:317,324`), the "pre-Store fixtures only" acknowledge arm, `if P.Count`/`if P.Observe` (always defined, `Probe.lua:457-458`), `SPCRuntimeComposition and`. The comment at :301 calls the `not e.name` path "legacy" though it is the normal production exit path for five modules (doc fix). | `RuntimeWork.lua:6,12,122,126,199-201,214,224,301,310-313,509,515` |
| CA-D06 | Low | R | Fallbacks only test stubs reach: no-`Inspect` arm, and `CurrentEffectPartners or CurrentDomesticPartners` (different semantics: no applied-effect retention). `CurrentEffectPartners` always exists (`NetworkBridge.lua:771`). Pinned by `test_refactor_s6f.py:167,179`, `test_scoped_depth_write.py:20`, stub bridges in `test_pu01_fact_use.py`, `test_refactor_s8b7b.py`. | `Commerce.lua:240-242,249`, `DevelopmentInvestment.lua:253` |
| CA-A08 | Low | R | Engine-API presence fallbacks for old fixtures (`FindID` "old compatibility adapter", `Map.GetAdjacentPlot`) silently rescan. | `SampleLifecycle.lua:147,156` |
| CA-A10 | Low | R | `ShadowRouteState.normalize()` repeats every check of `BackgroundRoutes.collect()` on the same synchronous snapshot, can reject a valid snapshot, and its output is read only by tests (D0032 archaeology: "Test/reference-only"). P08 retirement review. | `ShadowRouteState.lua`, gate at `UI/BackgroundRoutes.lua:136` |
| CA-D03 | Low | R | Dead "no observer" path: `CrewProjectOrder.lua:136,139,142` always pass an observer, but three adapters keep a second revision-only branch, exercised only by `test_refactor_s9a2.py:26`. | `UI/CommerceUI.lua:28,39-43,47`, `UI/CapitalInvestmentUI.lua:20,30-34,37`, `UI/DevelopmentInvestmentUI.lua:21,31-35,38` |
| CA-D09 | Low | R | Dead compatibility arm `effectAvailability==nil and availability=='AVAILABLE'`; the producer always sets both (`NetworkBridge.lua:477-478`). | `CultureNetwork.lua:216` |

### T3 — Re-validating our own payloads (types, formats, ranges)

| ID | Sev | Class | Finding | Location |
|---|---|---|---|---|
| CA-A03 | Low | R/F | Training observation re-checks issuer, integer serial <2^53, state, input ≤512 and token length, all guaranteed by producers (`EffectiveFacts.lua:73-75,97,303`, `ExpeditionTraining.lua:90-95`); a violation silently returns false or `FACTS_UNOBSERVED`. The pcall isolation stays (B391). | `CityProgressionStore.lua:258,288-291,304,308,1821` |
| CA-A07 | Low | R | Cross-context own data type checks silently skip the cache or answer "request invalid". Keep nil/version freshness. | `SampleLifecycle.lua:254-260,268-272,274,285`, `RuntimeGC.lua:152,160` |
| CA-A09 | Low | R | `Write` re-validates `expected` already validated by `Read`/`Write`; `Game`/`P.SetProperty` presence asserts; repeated `integer(pid)`. | `ExpeditionSpyStore.lua:111,121,125,127,139` |
| CA-B03 | Low | F | Governor ceiling shape re-check; `Probe.lua:328-342` only returns KNOWN with 1–4, so a bad value would become `UNKNOWN_GOVERNOR`. Assert (pure read, safe to throw). | `EffectiveFacts.lua:150-151` |
| CA-B11 | Low | F/R | UI re-checks presentation payload types that `PlayerActionReplies.lua:123-164` already asserts before publishing. Keep identity/freshness (owner, cityID, x/y, token, epoch, version, error). | `InstitutionPresentation.lua:44-45,89,121`, `UI/CityPotential.lua:107-110` |
| CA-C02 | Low | F/R | Aggregate. Silent arms: `CapitalInvestmentModel.lua:39-52,176` (re-checks `ReputationUse` output inside `Quote` :164); `CommerceModel.lua:72,84-86`; `NetworkInput.lua:30` (no BoostConfig → K=1), `:49`; `RuntimeWork.lua:96-101` (malformed transfer scope silently widened to a full audit); `NetworkBridge` `(shared.RouteSignalRevision or 0)` at :28,39,70,187,413,475,567,750,995 while :1018 increments unguarded, plus :9,120,198,420,713,1007. Duplicate asserts (model validates input and output, Store validates again): CommerceModel :111-160, :130,133, `Commerce.lua:208`; CapitalInvestmentModel :111,195,208; DevelopmentInvestmentModel :39,58,64; DialogueProjectModel :44,48,69,76; EngineeringStudyModel :35,38,53,55 (Hold :44 validates nothing, unlike Dialogue's Hold). | as listed |
| CA-D02 | Low | R | `NewViewObserver.Observe` validates revision <2^53, token 1..512, reference scalars and NaN on views from our Gameplay context; on violation it returns "changed" and stops caching (extra repaint). Pinned by `test_refactor_s9a2.py:64`. Also `CommerceUI.lua:10` `M.Available` type checks on our own view. | `UI/SafeAdapters.lua:141-162` |
| CA-D10 | Low | R | Type/range re-checks on payloads from our own UI-context readers (generation <2^53, `type(v)=='table'`, `protocol==2`); the producer already asserts (`UI/DevelopmentInvestmentRead.lua:9`). Keep freshness/identity. | `DevelopmentInvestment.lua:261`, `StandardizationEffects.lua:400-401` |
| CA-D15 | Low | R | UI-side type/NaN re-checks of our values; the invariant `total==each*count` belongs at the producer (CultureMeaning). | `UI/BoostGreatWorkRead.lua:116-134`, `UI/TimedProjectSelectionClient.lua:46-50,58`, `UI/DialogueRefresh.lua:76-77` |

### T4 — Presence checks on modules and methods that always exist

`RuntimeComposition.Run` contains startup failures: a failed module leaves its `shared.*` export nil and its declared dependants are skipped. So `if shared.X` is a real availability check when X is **not** a declared dependency, and those were kept. The findings below cover declared or transitive dependencies, `include`d modules and methods that are always defined.

| ID | Sev | Class | Finding | Location |
|---|---|---|---|---|
| CA-D05 | Low | R | About 25 guards on declared/transitive dependencies (`shared.FactChanges and`, `bridge.ProofRevision and … or 0`, `if shared.CityProgressionStore`, `shared.Commerce and`, AcceptFact `type(event)` re-checks already asserted in `FactChanges.Emit` :223-226). Worst case: `if shared.FactChanges then RegisterConsumer` would silently skip a registration instead of failing. | `Commerce.lua:26,35-36,437-439,488,512,518`; `CapitalInvestment.lua:127,173-174,358`; `DevelopmentInvestment.lua:84,317,431`; `StandardizationEffects.lua:383`; `Standardization.lua:269`; `GreatWorkFacts.lua:395,439,456`; `CrewProjects.lua:410`; `Restructuring.lua:141,145`; `InvestmentAction.lua:14,46-55,186,193`; `CultureInspiration.lua:243`; `IndustryHistory.lua:114`; `ExpeditionTraining.lua:360` |
| CA-D01 | Low | R | `include('UnitSiteFacts')` is unconditional at line 1, yet `if SPCUnitSiteFacts … else <full district scan>` keeps a module-absent arm (introduced B313, `08db0cba`). The pcall + full-scan fallback when the engine-reading hint fails is a separate, correct-by-construction path and stays. | `InvestmentAction.lua:31-34`, `UnitActions.lua:25-27`, `UnitTargets.lua:94` |
| CA-D04 | Low | R | Wiring checks for methods that are always exported (`ResumeProofRegistration`, `WithPhase`). | `Gameplay.lua:623,626` |
| CA-D11 | Low | Q/R | ExpeditionTrainingDiagnostics is a hard include in CrewProjects, Restructuring and ~10 modules but `pcall(include)` + `traceLoaded and` in Commerce, Capital, Development, CultureNetwork, Gameplay; the include-failure arm is dead. CultureDiagnostics is a recorded optional tap (B394) and stays. Production also depends on diagnostics helpers (CapitalInvestment view reasons come from `CapitalInvestmentDiagnostics.Error`), so retiring either module needs a P08 review. | `Commerce.lua:7`, `CrewProjects.lua:5,19` |
| CA-D12 | Low | R | Start shuts down a previous instance that cannot exist; `shared` is created fresh at `Gameplay.lua:16`. | `GreatWorkFacts.lua:55` |
| CA-B02 | Low | R | `changes and changes.Generation` presence checks cannot fail (FactChanges starts before the Store, EffectiveFacts depends on the Store, `Gameplay.lua:616-683`). | `EffectiveFacts.lua:165,171,180,205` |
| CA-B07 | Low | R | Fallback for a missing `service.Inspect`, which always exists; the fallback would also skip the phase/freshness guard. | `CurrentSpecializationFacts.lua:14` |
| CA-B09 | Low | R | Redundant defences around the district write fence (pcall around `FenceCarrierWrite`, method/scope checks, `facts.Version` middle fallback); all fall back to over-invalidation (extra work only). Keep `facts==nil`/`dc==nil`. | `EffectiveFacts.lua:34,44`, `DistrictCompleteness.lua:197-202` |
| CA-A04 | Low | R | `publishFact` fallback record is dead (all 14 callers pass a committed record); `copyIndex` re-validates the in-memory index on every admission. | `CityProgressionStore.lua:32,36,2178` |
| CA-A06 | Low | R | StoreDeferredLifecycle / StoreLifecycleRecovery: legacy schema 1 still accepted in `parent`/`reference`, `Validate` 2–3 times per `Clear`/`copy`/`finish`, `plain`/`getmetatable` checks, `assert(SPC*Model …)` for modules the Store always includes. Asserts on rare paths: noise. | `StoreDeferredLifecycle.lua:23-28`, `StoreLifecycleRecovery.lua:8-60` |
| CA-D14 | Low | Q | Checks that module tables/methods were not swapped between two reads in one session; accepted in B368 but no runtime hazard is named; only test wrappers trigger it. | `ExpeditionTraining.lua:88-112` |

### Policy question without a defect class

| ID | Sev | Class | Finding | Location |
|---|---|---|---|---|
| CA-D08 | Low | Q | Two policies for one dependency: if DistrictCompleteness fails to start, three modules subscribe to raw District events themselves, while four others declare it as a dependency and are skipped. | `Commerce.lua:713-718`, `CultureNetwork.lua:582-591`, `CultureInspiration.lua:233` |

Observation (no class): `CapitalInvestment.lua:358-359` and `DevelopmentInvestment.lua:396-397` parse Commerce's private `pid:id` view-key format, which is coupling rather than defence.

## Kept on purpose (examples, with reasons)

- **Store** (B169, B244, SAFE-004, P06): pre-commit `validate()`, CAS/readback, occupancy UNKNOWN, load-side validation and subrecord isolation, exit/return attempt budgets.
- **ExpeditionSpyStore** (C095/C073): load validation. **RuntimeGC** (B270): heap reads. **SampleLifecycle**: `Receive` parsing of an engine-serialised string.
- **FactChanges**: it already asserts every precondition before touching the queue.
- **Catalogs**: database boundary. Tier errors fail closed by the accepted Tier rule.
- **NetworkBridge**: packet ingress, proof/notification recovery (P06) and view version stamps (P07).
- **Design semantics**: UNKNOWN≠0 in DialogueEffects and the Commerce reputation clamp; HELD-not-zero containment.
- **UI ProductionPanel containment** (`UI/SafeAdapters.lua:5-120`): adapters run inside a replaced native panel, so failures disable only our own rows, with a visible tooltip.
- **Diagnostics modules**: all live, none wraps production logic.

## Suggested batches (not authorised; each needs an Owner-approved plan)

1. **Make swallowed errors visible:** CA-A02, CA-C01, CA-D07, plus a Fail reply for UNIT_ACTION (CA-C05 part). Small and local; it changes diagnostics, not gameplay. Highest value.
2. **Contract asserts at internal seams:** CA-B03, CA-B05, CA-B06, CA-B08, CA-B10. Each needs its throw located before the first write or inside an existing pcall boundary.
3. **Delete dead presence checks and second paths:** T4, plus CA-D01, CA-D03, CA-D06, CA-D09, CA-C03, CA-C04. Mostly deletion with fixture updates.
4. **Drop own-payload re-validation:** T3 (except CA-B03, which is in batch 2). Tests pin some guards (`test_refactor_s9a2.py:64`, `test_refactor_s9c*`); those assertions would be replaced, not weakened.
5. **Owner decisions first:** legacy fixture retirement (CA-A01 with CA-D13, CA-B01, CA-C06); SAFE-004 under same-build (CA-A05); isolation remnants (CA-C07); dead NetworkBridge API (CA-C08); observer pcall layers (CA-B04); typed reply validation (CA-C05); module-swap checks (CA-D14); diagnostics as hard dependency (CA-D11); DistrictCompleteness failure policy (CA-D08).

## Owner decisions (2026-11-25, after the report)

- **Engineering policy.** Do not over-defend: a contract violation inside our own code should blow up, because it means there is a bug. Keep enough probes and error logs to find the root cause. Probes must stay isolated from production modules, so that deleting a probe has no effect on production. Production may at most record a failure it caught into a plain shared error log (`SPCSafeCallbacks.Record` → `shared.ErrorLog`), with no effect on control flow. Printing and collection live in a separate context.
- **No compatibility before release.** No compatibility with old versions or old saves of any kind before release.
- **CA-C05: option A.** Remove the reply format re-validation and keep only request identity and transport budgets.
- **CA-A01 and CA-D13: retire them.** This covers the legacy test adapter, schema-1 support and the second ledger path. Under the no-compatibility rule, CA-A05, the schema-1 parts of CA-A06 and CA-A08 join the same retirement batch.
- **Batch 1 is authorised and implemented as B546.573:** CA-A02, CA-C01, CA-D07 and CA-C05, plus the isolated `UI/ErrorProbe` printer and the `[SPC][ERR]` collector allowlist. See the Status checkpoint S1157.
- **Batch 2 (legacy compatibility retirement) is authorised, with CA-A05, and implemented as B547.574 (2026-11-26).** It covers CA-A01, CA-D13, CA-B01, CA-C06, CA-A05, the schema-1 part of CA-A06 and CA-A08, plus the consumers of `UsesNewAuthority` (Standardization template ledger, ResearchTraditionEffects strict carrier reference) and Commerce's `BlocksLegacy` source check. Subrecord isolation (SAFE-004) stays. The stub-store fallbacks in `CityReference.Read` and `RuntimeWork` acknowledge are left for the presence-check batch, because many fixtures use stores without those methods; only their `UsesNewAuthority` asserts went. See the Status checkpoint S1159.
- **Batch 3 (internal asserts) is authorised and implemented as B548.575 (2026-11-26):** CA-B03, CA-B05, CA-B06, CA-B08 and CA-B10. Real UNKNOWN states stay UNKNOWN; shape violations from our own producers throw inside existing read-side protection. See the Status checkpoint S1161.
- **Batch 4 (dead presence checks), with CA-D14, is authorised and implemented as B549.576 (2026-11-26):** CA-D05, CA-D01, CA-D04, CA-D12, CA-B02, CA-B09 (EffectiveFacts fence), CA-A04, the model-presence part of CA-A06, CA-C04 (except NewReader/Inspect), the RuntimeWork pre-Store acknowledge arm, CA-D06, CA-D09, CA-D03, CA-C03 (model functions only), CA-D11 (dead include arm only) and CA-D14. **Kept, with a code comment, as a fixture-double follow-up:** the `CityReference.Read` no-Store arm and the RuntimeWork `NewReader`/`Inspect` fallback (dozens of fixture doubles lack `ReferenceToken` or define only `Read`), and CA-B07 plus the DistrictCompleteness `facts.Version` arm of CA-B09 (a CurrentGameplay test replays a frozen-baseline EffectiveFacts without those methods). The duplicate `Validate` calls in CA-A06 were not changed. See the Status checkpoint S1163.
- **Batch 5 (own-payload re-validation) is authorised and implemented as B550.577 (2026-11-26):** CA-A03, CA-A07, CA-A09, CA-B11, CA-C02, CA-D02, CA-D10 and the TimedProjectSelectionClient and DialogueRefresh parts of CA-D15. Own data is validated once at the save boundary; models no longer re-check the saved copy they start from; consumers keep freshness, identity, native-read and load-time checks. Engine-provided district and yield indexes keep their scalar check. **Not changed:** the `UI/BoostGreatWorkRead` part of CA-D15, because no production code produces the fields it reads (the path looks fixture-only and joins the diagnostic-path decision). See the Status checkpoint S1165.
- **Fixture-double migration is authorised and implemented as B551.578 (2026-11-26):** the four arms kept in B549 are gone (CityReference no-Store arm, RuntimeWork NewReader/Inspect fallback, CurrentSpecializationFacts without Inspect, DistrictCompleteness `facts.Version` arm). Fixture doubles now provide what the real modules always define; assertions are unchanged. See the Status checkpoint S1168.

## Coverage

- **Groups A, B and C:** every assigned module read in full.
- **Group D:**
  - Read in depth: Gameplay wiring, Commerce, CultureNetwork, CapitalInvestment, DevelopmentInvestment, StandardizationEffects, Standardization, GreatWorkFacts, CrewProjects, Restructuring, InvestmentAction, the seven diagnostics modules and five UI helpers.
  - grep plus spot reads only: DialogueProjects, DialogueEffects, CultureInspiration, CultureAesthetic, CultureMeaning, IndustryHistory, ExpeditionTraining, ExpeditionSpyGate and ExpeditionSpyRead. The bodies of CultureAesthetic and CultureMeaning were not read line by line, and ExpeditionSpyGate/Read are mostly engine reads.
- **Out of scope:** UI files that are almost entirely engine/Controls code.
