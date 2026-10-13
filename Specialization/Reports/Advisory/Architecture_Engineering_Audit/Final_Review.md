# Final Review: Architecture and Engineering Risks Before Further Expansion

Advisory / Non-authoritative / No design decision implied
Status: Stable
Maintainer: Advisor session (Claude), attribution only — not session authorization
Scope: Phase B cross-review against the prior comprehensive audit and the Phase C final prioritized assessment, for the user-authorized comprehensive architecture/engineering audit. Phase A evidence: [Architecture_Findings.md](Architecture_Findings.md) (AF-01…AF-28, SD-01…SD-18) and [Expedition_Review.md](Expedition_Review.md) (clusters A–L). Run record: [Audit_Ledger.md](Audit_Ledger.md).
Basis:
- Repository: `develop` `2b75e12`, later `f843c0f`. The two differ only in Advisory AGENTS and Context_Lock; no `Mod/`, `DevelopmentTests/`, Design, Architecture or Status change.
- Runtime: B204.231, source `84773a8`.
- Prior audit (another agent's interpretation): `Specialization/Reports/Audit/P16b_P17_Final_Audit.md` and its ledger and phase reports. Committed `e02ef75` on 2026-10-07; last baseline `194a459` (B168.195).
- Since that baseline: 116 commits, 36 of which touch `Mod/`.
- External sources: read-only Civ VI install and HD Workshop `2465378070`. HD version UNKNOWN.

**Evidence scope.**
- Everything here is static source and record reading (STATIC_CONFIRMED) or labelled inference.
- No tests were run, so there is no new LOCAL_SIMULATION_PASS. The game was not launched, so there is no new USER_GAME_TEST evidence.
- Prior-audit local reproductions and other agents' native records are cited as their interpretation.
- B204 remains USER_GAME_TEST_REQUIRED.

---

## 1. Bottom line

1. **No CRITICAL finding.**
   - The runtime is consistently fail-closed. No reviewed path silently double-grants, replays an uncertain native action, or corrupts a save.
   - The prior audit's conclusion stands: nothing justifies a whole rewrite.
2. **The dominant long-term risk is cost and fragility that grow with each ability.** Five root causes drive it:
   - (a) Composition and propagation are hand-wired.
   - (b) Failure states are terminal and bespoke, and they spread across abilities.
   - (c) Gameplay authority depends on UI-context liveness inside shared, single-winner replaced panels coupled to HD's private files.
   - (d) The test harness cannot represent the native context and event model. This is where the B201–B203 local-pass / native-fail sequence occurred.
   - (e) Several world-scope or catalog-scope cost terms are unbounded, and none is measured beyond T62 / 13 cities.
3. **Since the prior audit, the project fixed two of its eight priorities and partly fixed two more.**
   - Fixed: Store N×T reference checks (B169); Great Work callback isolation (B173).
   - Partly fixed: D detail separation (B170); scoped investment propagation (B174). In the deployed composition, the B174 normal-Settler path is defeated by a decorator (SD-01).
   - New code since then (Dialogue M, Expedition B178–B204) introduced the integration risks the prior audit had marked NOT_YET_AUDITED, chiefly AF-03, AF-04 and AF-09.
4. **The Expedition B202–B204 binding is sound on the happy path; its exit side is not.**
   - HELD is a terminal sink.
   - Removing the queued team through the stock Production Manager strands the reservation. After a reload this costs the player's only Expedition slot for that save.
   - These do not block the pending B204 native test, but they should be settled before reattachment, N2 rewards or repeat missions build on this binding.

## 2. Phase B — cross-review against the prior audit

### 2.1 Status of the prior audit's ranked priorities at HEAD

| Prior (rating then) | Status at HEAD | Evidence | Relation to Phase A |
|---|---|---|---|
| P06a-F01 Store per-write full reference check, N×T (MEDIUM / FIX_NOW) | **RESOLVED** by `943f26c` (B169) | `Mod/CityProgressionStore.lua:749-752`: `checkReference` runs only when the endpoint key changes. Ticks and Dialogue writes take the fast path (`:190-200`, `:176-180`) | Correctly absent from Phase A. Residual per-write copy cost is under AF-24 |
| P06a-F02 bad `current` makes healthy records unreadable (HIGH / DEFER) | **CHANGED** by `943f26c` | Read-side spread fixed (`:665-676`, `:793-819`). Replaced by a deliberate Store-wide block on *structural* writes while any UNKNOWN reservation exists (`:677-688`; Architecture `:79`). [owner-verified] This also blocks every new-city admission (`:1088-1091`) | Phase A AF-13 caught the loss-write part, not the admission part. Folded into AF-13 with a new DDR |
| P13a-F02 fact collection coupled to the whole Buildings catalog (MEDIUM / FBDF) | **PARTIALLY RESOLVED** by `343868e` (B170) | Diagnostic tree split from five consumers. D presence still scales with B_loaded. The Great Work collector still costs C_own × B_loaded every local turn. `Lv2Housing.lua:22` is still on the full Read | Phase A AF-07 rated HIGH. **Adjusted to MEDIUM** (§2.4) |
| P13a-F03 hand-listed consumer chains (MEDIUM / FBDF) | **PARTIALLY RESOLVED** by `dcc43aa` (B174), but defeated on the normal Settler path by SD-01 | `Mod/CrewPrecision.lua:22-46` drops `UnitActions.Run`'s second return. The prior audit's P07c classification of CrewPrecision as observation-only was true at `194a459` and became stale on 2026-10-09 | Confirmed independently (AF-02). SD-01 is a new discovery |
| P06a-F03 / P13a-Q02 Identity vocabulary and business logic inside the Store (MEDIUM / FBDF) | **OPEN, worse**: B175 inlined Dialogue validation and loss policy into the Store | `CityProgressionStore.lua:97-100`, `:616-618` | Confirmed independently (AF-01, rated HIGH; see §2.4) |
| P13a-F04 Great Work single-callback chain (MEDIUM / FBDF) | **RESOLVED** by `bc54482` (B173) | `GreatWorkFacts.RegisterConsumer`: per-consumer pending and failure isolation | Phase A lists it as a strength and as the template for AF-02/AF-19. It is the precedent that per-consumer isolation is achievable without a bus |
| P09b-F01 public accepted network input is a mutable alias (MEDIUM / FBDF) | **OPEN** | `NetworkInput.lua:31-34` reads `b.input.cities` from the public `shared.NetworkBridge.players` bucket. Held-over values keep validity VERIFIED (`NetworkBridge.lua:280`) | **Phase A missed it.** Adopted (§2.3). Couples to AF-14 |
| P08a-F01 writer failure/readback contracts differ (MEDIUM / FBDF) | **OPEN, diverged further** | B172/B175 writers copied scheduler variants; SD-17 drain without pcall | Confirmed (AF-18) |
| P06b-F01 foreign `CityTransfered` dispatched to every registered record (MEDIUM / FBDF) | **OPEN** | `CityProgressionStore.lua:1249-1257` | Confirmed (AF-26). Phase A rated LOW; MEDIUM is defensible if the Store lifecycle routing changes next |

Functional gates:
- **P07c-F01** (Crew receipt has no readback before debit/grant): OPEN. Phase A folded it into AF-27 at LOW; it is lifted back to MEDIUM / FBDF before J1/J2.
- **P10b-F01** (template init treats `HasBuilding=nil` as absent): OPEN. Phase A missed it (§2.3).
- **P14a-F01** (stable deploy rename interruption): OPEN and byte-identical. Phase A did not review deployment tools (§2.3).

### 2.2 Independently confirmed (both audits, separately)

| Topic | Phase A | Prior |
|---|---|---|
| Store as the accretion point; business logic in persistence | AF-01 | P06a-F03, P13a-Q02 |
| Hand-wired propagation lists | AF-02 | P13a-F03 |
| Divergent writer mechanics and scheduler copies | AF-18, SD-17 | P08a-F01, P08a-Q01, P09b-Q01 |
| D/Great Work collection scaling with the catalog | AF-07 | P13a-F02 |
| Identity event broadcast to every record | AF-26 | P06b-F01 |
| Second-loss Claim key stale | SD-16 | P07b-F01 |
| Crew receipt ledger without readback | AF-27 | P07c-F01 (prior measured consequence) |
| Uncertain outcomes never replayed; INTENT and CALLING hold | AF-12 | P07a-Q01, P07b-Q01 |
| UNKNOWN transfer without confirmed loss; loss/return one-shot | AF-13 | P06b-Q01 |
| Test fidelity limits (Lupa 5.5 vs native VM, process-local reload) | AF-09, AF-22 | P12a / P15 caveats |

### 2.3 Prior findings Phase A missed (adopted)

| Item | Current rating | Note |
|---|---|---|
| **P09b-F01** public mutable accepted-input alias | MEDIUM / FBDF | Schedule with AF-14. Any "freeze at last confirmed" option widens reliance on this alias. The writable surface is the whole bucket, including `b.refreshing`, `b.inputSignature` and `b.routes`. Readers the prior audit missed: `CityProgressionStore.NativeDescribe`, `PerformanceCounters`, `UI/RuntimeAudit` (all read-only) |
| **P10b-F01** nil presence acknowledged as an empty template init | MEDIUM / FBDF (before H1 typed knowledge or any new template-init producer) | `Standardization.lua:51` is the one site where an unchecked `HasBuilding` result feeds a persistent INITIALIZED acknowledgement. The project convention at about 13 other sites treats non-boolean as UNKNOWN. A retroactive rebuild of existing empty ledgers is DDR |
| **P14a-F01** stable deploy rename interruption | MEDIUM / DEFER (before the next authorized stable apply or promotion, or any `tools/deploy.py` edit) | Window: a catchable interrupt between rename and `moved=True`. Stable path unexercised since B069.96 |
| **P13a-Q04** route capacity 128 / 16,384 bytes; sender returns silently | MEDIUM / MONITOR; FBDF before any route-capacity increase (Harbor/Commerce O) | Over the cap, a player keeps a stale VERIFIED snapshot with no signal. That is the same diagnosability gap as AF-14 |
| **P06a-Q01** uncommitted root visible to re-entrant reads during the native setter | MEDIUM / MONITOR; FBDF if AF-01 adds a registry or post-write hooks | Native reachability UNKNOWN |
| P13b-F01 Great Work dirty-scope retains removed IDs | LOW / MONITOR | Bounded; converges on the next valid sample |
| P01-F03 = P15-F01 Design README version labels stale (now two revisions behind) | LOW / DEFER | Duplicate IDs in the prior audit; navigation only |

### 2.4 Disagreements and how they resolve

Each change below is applied in §3. None is made for agreement's sake.

1. **AF-07, catalog-scale presence checks: HIGH → MEDIUM / FBDF. The LRU sub-claim → LOW / MONITOR.**
   - Every normal D consumer needs ACTIVE ≥ 2, and ACTIVE ≥ 2 needs an established governor (`Mod/Data/GovernorProbe.sql:34-38`) [owner-verified]. One player has at most about 7–8 governors, so the legal D working set is at most the LRU capacity of 8. Phase A's "9+ cities → about 0% hit" is structurally true but not reachable under current rules. The prior audit's MONITOR was right.
   - The real residual is the **Great Work collector**: C_own × B_loaded on every local turn and every transfer.
   - A constraint Phase A overlooked: bounding the collector to static `Building_GreatWorks` rows is unsafe, because base data has dynamic `EXTRA_GREAT_WORK_SLOTS` modifiers. Any candidate set must be DB-derived with a fail-closed fallback.
   - Escalation triggers: a D consumer that is not governor-gated, AI or multi-player enablement, or a mod that raises the governor count.
2. **AF-08, retirement: HIGH → MEDIUM / FBDF.**
   - The retained Dialogue transport and governor duty is a recorded, user-approved decision (`Specialization/Architecture/v2/P0_M_Dialogue.md:10,83`) [owner-verified], not accidental coupling. "Naive removal" is already forbidden by that plan.
   - What remains open: SD-04 (retirement fails open on partial startup), eight different retirement mechanisms with no end-of-life criterion, and an exact exit plan for each future cutover (H, N3, P, J).
3. **AF-06, coarse invalidation: split.**
   - (b) **The global write counter keeps HIGH / FBDF.** Every Store write, including per-turn Research ageing, and every carrier write by any module bumps one scalar, and the next publish triggers an unscoped world-wide Commerce audit (`Probe.lua:552-554` → `CommerceConvergence.lua:157-166`). Keyed revisions need no native-signature assumptions. The prior audit described the counter but never evaluated cross-module amplification.
   - (a) **Full-scope hooks for unverified event signatures → MEDIUM / FBDF.** This is a deliberate conservative contract (Architecture `:111`; B138 tests show some foreign events are required). Narrowing it depends on the user's evidence-standard decision.
4. **AF-05, world sweeps on transfer: keep HIGH / FBDF, restate the rationale.**
   - The prior audit missed this. No prior report mentions `NetworkBoost.Clean` on `CityTransfered` or the StandardizationDiscount transfer cleanup; both predate its baseline.
   - Its hot-path row ("each writer × own exact IDs; the 1720 union is not scanned by every module") is literally true but incomplete: NetworkBoost's own 1,126 IDs (about 65% of the union) are multiplied by every world city on every transfer, including AI↔AI transfers.
   - Phase A overstated one inference: "dominating conquests" should read "a large share". The growth axis is world size × transfer frequency (late-game wars, loyalty, cessions) plus the HD catalog, not the number of abilities.
   - GreatWorkProbe and CopyYields also re-run world cleanup on transfer.
   - Any narrowing must keep a fallback for transfers that cannot be attributed (P06b-Q01).
5. **AF-03, UI-closure dependency: keep HIGH / FBDF, correct details.**
   - Claim's UI queue reader is the *primary* native path, not a fallback (`OverflowStorageProbe.lua:15`: `GetSize` is UI-only).
   - Consequences differ by tenant:
     - Claim: timer STOPPED, re-selectable (recoverable; costs production time).
     - Dialogue and Expedition: durable holds.
   - The prior audit's LOW / MONITOR was reasonable when Claim was the only tenant. The trigger that mattered was new Gameplay-authority tenants (Dialogue M, Expedition B202), not context rebuilds.
   - Counterevidence to add: B126/B129 Claim and B202 native records show the steady state works. The risk is outage and ordering.
6. **AF-12, holds: keep MEDIUM / FBDF, narrow the remediation.**
   - Holds are deliberate per feature.
   - Phase A's "common receipt key" conflicts with the prior audit's rule not to merge success evidence across assets. Keep only common stage names and a typed TERMINAL_HELD signal.
   - P07b-Q01: Claim's "new legal completion" escape route is impractical for a 1,000,000-cost project, so Claim CALLING is effectively unrecoverable. Dialogue (B175) has an abandon path and Claim does not. Settle one 1T hold/abandon convention before the next 1T project; abandon policy is DDR.
7. **AF-13, loss/return: keep MEDIUM / FBDF, re-frame.**
   - Cite Architecture `:79` (B169) as a deliberate decision.
   - Add the admission blocking (§2.1).
   - The prior audit's W20 inventory already mapped the 1,720 fixed carriers to exit owners; it is stale for about 12 later IDs. Remediation #1 becomes cheap: promote it to a committed test.
   - New DDR: whether an UNKNOWN Store reservation should also suppress loss recording, exits, and all future admissions.
8. **AF-19, carrier registry → static test.** The prior audit (P08a `:110`) found a runtime owned-carrier registry unnecessary. A static test over the declared exact lists gives the same guarantee without new runtime state.
9. **AF-27, Crew receipts.** Lift the no-readback sub-item to MEDIUM / FBDF before J1/J2 (the prior audit measured a debit with no persisted receipt). The "unbounded ledger" remark must not lead to pruning: dedupe receipts are NO_ACTION in the prior audit, and retention is DDR.
10. **SD-12 → LOW / OBSERVATION.** `SPC_Lv2HousingTiers` has no runtime reader, and 22 of its 50 rows are base-game buildings. It shows that no LoadOrder policy exists, not a live defect.
11. **SD-02, tradition owner policy.** The prior audit registered this as known Design→implementation adaptation **K01 (MEDIUM / DEFER)**, so it is not a new discovery. Phase A adds the second terminal path (`UNKNOWN_INTERVAL` after recapture) and the point that the fix must resume the cursor, not merely delete one write.

### 2.5 Constraints from the prior audit that bound Phase A remediation

These amend remediation wording in [Architecture_Findings.md](Architecture_Findings.md). Ratings are as given in §3.
- AF-02: the action→handler and cause→consumer tables stay **explicit central declarations**, not self-registration by modules (P05b `:11`).
- AF-10: a start table with `dependsOn` must **preserve the declared order**, not auto-sort topologically (P05b `:55`).
- AF-07: per-turn memoization must not reuse across a real change within the same turn (P13a-F01). A "retired-clean" mark must not shrink the exact cleanup lists (P08a `:97`).
- AF-01: replacing the Preview delegation must be behaviour-preserving (P05b `:32-36`). The extension registry must also settle commit visibility (P06a-Q01).
- AF-21: replacing literal stamps with invariants needs the user's frozen-test policy (P15 `:52`).
- AF-09 and AF-25: adopt incrementally, for new UI-mediated tests and the B202–B204 observers first. No full-Mod simulator (P12a `:76-77`). Do not rewrite frozen assertions.
- General: do not unify long-term assets, state machines or formulas for DRY. Retired definitions still carry exact cleanup. UNKNOWN is not confirmed loss. Git, runtime hash, receipt and recovery package keep separate duties (P16b `:13`, `:64`, `:145`).

With these amendments, no Phase A remediation boundary contradicts the prior audit's NO_ACTION list.

### 2.6 New discoveries (Phase A only; not in the prior audit)

- **Code after the prior baseline:**
  - SD-01 (decorator defeats B174)
  - The whole Expedition review (clusters A–L, including the Production Manager cancellation gap and NAME-after-END)
  - SD-04 (Dialogue retirement fails open)
  - AF-08's eight retirement mechanisms
  - AF-20 (seven manifest-listed test files outside the executed closure; the closure exists only in ignored local evidence)
  - AF-09's evidence from three consecutive local-pass / native-fail batches
- **Areas the prior audit marked NOT_YET_AUDITED:** AF-04 (HD private-file includes, undeclared dependency, seven replaced contexts, ProductionPanel LoadOrder only 100 above HD); SD-03 (TimedTurnProbe owns End Turn with no possible arming).
- **Code present at the prior baseline but not flagged:**
  - AF-05 transfer sweeps
  - AF-06(b) global counter amplification
  - AF-14 all-or-nothing capture with opposite consumer polarities
  - SD-06 (one unresolvable district event holds every not-yet-specialized city)
  - SD-07 (unsupported acquisition breaks network capture at cold load)
  - SD-08 (Commerce facts before the test-player check)
  - SD-09 (`OnBuildingConstructed` subscriptions to a name used nowhere in base or HD Lua)
  - AF-17 confirmed design drift tooling gap

**Coverage note.** The prior audit's statement that "no high-value slice is missing" was valid at its baseline. After B175–B204, native integration (AF-03, AF-04) and test fidelity (AF-09) became high-value, and its ranked list contains none of them. Read this review's ranking as *additive* to its remaining open priorities, not as a replacement.

**Unaudited by both audits:**
- native load trace and actual override winner
- loaded-DB dynamic carrier counts (no configured DB path)
- native timing and allocation
- full object graphs
- external recovery packages
- the user's enabled mod set

---

## 3. Phase C — final prioritized register

Ratings incorporate the Phase B adjustments. Evidence, modules and full remediation detail are in the Phase A files under the same IDs. "FBDF" means FIX_BEFORE_DEPENDENT_FEATURE, and the dependent feature is named. Regression risk is for the proposed boundary, not the defect.

### 3.1 FIX_NOW (small, concrete, independent of future features)

| ID | Sev | What and why now | Boundary / regression risk |
|---|---|---|---|
| SD-01 | MEDIUM | The CrewPrecision decorator truncates `UnitActions.Run`, so the deployed build never runs B174 scoped propagation or the Dialogue entry refresh after a normal Settler investment. Every Settler confirm also overwrites the last real Crew precision sample. The Architecture claim at `:87` is currently false | Return all values from the wrapper (`return original(pid,params)` captured as multiple values), and add one real-Start-order composition test (AF-10). Regression risk LOW. The LOCAL_SIMULATION_PASS for B174 should be re-scoped as "subset composition" |
| Expedition B | MEDIUM–HIGH | Removing the team via the stock Production Manager, a late placement confirmation, or a lost CANCEL strands TRAINING. After a reload, the player permanently loses the cap1 slot | Option 1 is technical: intercept ProductionManager and give placement-armed CANCEL a lifetime that covers the placement. That adds an eighth single-winner replaced context. Option 2 is a Gameplay-side bounded resolver for "queued, now empty, no receipts, past a processing boundary"; it changes the B202 evidence rule (`P0_N_Expedition.md:25`), so it is **DDR**. Bundle with cluster C (cancelled completion as non-evidence). Regression risk LOW–MEDIUM |
| AF-20 | MEDIUM | The executed test closure exists only in ignored local evidence. Three suites the manifest names as direct regressions, including 39 NAME-authority negatives, have not run since B194 while B202–B204 changed naming | Run and classify the six non-frozen excluded files once. Record the closure as a machine-readable list (a schema change needs user approval under W0005). No runtime risk |
| SD-03 | MEDIUM | The B116 TimedTurnProbe still replaces HD's ActionPanel (End Turn, Enter) and nothing can arm it | Remove the replacement, with user authorization, plus one native end-turn check. Regression risk LOW |
| SD-02 | MEDIUM | Prior K01. Academic Tradition sets an absorbing `OWNER_POLICY_UNRESOLVED` on capture, and a second absorbing `UNKNOWN_INTERVAL` follows on recapture | Confirm the D0040 reading first (`Research_D0040.json:329-331`). Then implement "freeze while unsupported owner, resume at the recapture turn without credit". Tests pinned to the old behaviour need an explicit update. Escalate if the reading is genuinely ambiguous |

### 3.2 HIGH — FIX_BEFORE_DEPENDENT_FEATURE

| ID | Finding | Dependent feature (trigger) | Remediation boundary / trade-off / regression |
|---|---|---|---|
| Expedition A (+H, D, E) | HELD is a terminal sink. With no unit there is no exit, so cap1 is lost for the save. HELD loses the prior phase and stops tracking. Validation-only errors become HELD. One-shot UI follow-ups have no recovery owner | Reattachment, N2 rewards, repeat missions | Structured hold kind plus prior phase. A Gameplay-owned bounded resolver that re-proves facts and bumps the generation; it never grants or deletes without fresh proof. Set the mutation flag only immediately before the first write. Make follow-ups mirror-driven. **DDR**: cap1 release and spent production, END-only for a surviving unit, retryable naming, never-submitted travel. Precondition UNKNOWN: whether off-map Spies are enumerable. Regression MEDIUM (cap authority) |
| AF-03 | Gameplay transitions depend on UI-context closures hosted in the ProductionPanel replacement (no teardown, no adapter isolation). An outage becomes a durable Dialogue/Expedition hold | Next production-queue ability; any new UI-only fact | A dedicated UI native-read bridge with a readiness epoch and READER_ABSENT vs READ_FAILED. Per-adapter pcall. Classify reader absence as transient. Outage policy (defer vs hold) is **DDR**. Regression MEDIUM |
| AF-04 | Seven replaced native panels include HD private files by name. HD is not a declared dependency. ProductionPanel LoadOrder is only 100 above HD's. There is no SQL LoadOrder band policy, and tests run on the composed DB | Next HD update (outside the user's cadence); any new replacement or HD-dependent SQL | Decide whether HD is declared (scope decision). Symbol guards with vanilla fallback (the InstitutionOverview pattern). A read-only compatibility check (include targets, wrapped symbols, HD fingerprint in receipts). A LoadOrder band policy plus a manifest check. Regression LOW |
| AF-01 | The per-city Store is the integration point for every persisted asset (now four inline domains including B175 Dialogue). Whole-city fail-closed on load. Isolation does not hold for loss, return or admission | Next persisted per-city asset (Culture N2 records, Commerce contracts, Wonder credits, Teams) | A code-level extension registration (validate, onTransfer, onReturn) with a single commit/readback. The placement rule for new ledgers and the failure granularity are **DDR**. Must settle commit visibility (P06a-Q01) and keep Preview replacement behaviour-preserving. Regression LOW–MEDIUM if applied to new assets first |
| AF-02 | Hand-wired propagation: a 640-line string dispatcher and six divergent consumer lists. About 4–6 central edits per ability; omissions are invisible | Next ability that reacts to investment, unit action, governor or Great Work facts | Explicit central cause→consumer declaration iterated by the existing sites, deterministic order with per-call pcall (the GreatWorkFacts precedent), plus a static completeness test. Which effects must refresh synchronously is **DDR**. Regression MEDIUM; use an old/new delivery-set parity test |
| AF-09 | The harness runs all contexts in one Lua state with per-file mocks and synchronous single-slot events. Four recorded native failures of this class, plus B201–B203 | Next UI-mediated ability (reattachment, N2/N3 bridges) | Incrementally: per-context runtime or `_ENV` sandbox, multi-listener event mock in registration order, lifecycle profiles (init or frames delivered, delayed, withheld), a 5.1-profile runtime. Start with new tests and the B202–B204 observers. No full-Mod simulator. Test-only risk |
| AF-05 | World × 1,126-ID NetworkBoost Clean, plus StandardizationDiscount, GreatWorkProbe and CopyYields cleanups, on every `CityTransfered` | Large-map or late-war playtests; any new writer with a transfer handler; any further performance pass | Scope cleanup to the transferred city, with a fallback for unattributable transfers. One legacy sweep per save behind a flag. Guard B055 lookups. Narrowing Architecture `:115` is a contract change; the B055 save window is **DDR**. Regression MEDIUM (stale carrier) |
| AF-06(b) | One global write counter: every Store or carrier write triggers an unscoped world Commerce audit | Any new state-writing ability (each adds amplification) | Keyed revisions (player/city/output kind), Commerce first. Needs no native-signature evidence. Regression MEDIUM-LOW |

### 3.3 MEDIUM — FIX_BEFORE_DEPENDENT_FEATURE

| ID | Finding | Trigger |
|---|---|---|
| AF-10 (+SD-04) | Composition by include/Start order. Unguarded startup; INITIALIZED published first; retirement flag after five unguarded Starts can fail open | Next module addition, probe cleanup or retirement. Explicit start table in the declared order, per-module isolation and status, INITIALIZED last |
| AF-12 (+SD-06, P07b-Q01) | Terminal holds with no shared resolution vocabulary. One unresolvable district event holds every UNASSIGNED city. Claim CALLING effectively unrecoverable | Before more abilities gate on `investmentPending` and before the next 1T project. Common stage names and a typed TERMINAL_HELD (no common receipt key); abandon policy **DDR** |
| AF-13 | Loss/return one-shot. UNKNOWN reservation blocks loss writes, exits and all admissions (deliberate, B169). Exit registration voluntary | Features relying on confirmed-loss exits. Promote the W20 carrier→exit inventory to a test; pass the pre-loss reference; **DDR** on UNKNOWN-reservation scope and late return |
| AF-14 + P09b-F01 (+SD-07) | All-or-nothing network capture with per-consumer opposite polarity and string-typed classification. Unsupported acquisitions break capture at every cold load. The previous-value path reads a public mutable alias | Next network consumer, or any hold/freeze work. Typed per-city status at providers, one declared polarity mapping behind an owner-private read-only boundary, cold-load tests. Partial-network semantics **DDR** |
| AF-07 | Great Work collector C_own × B_loaded every local turn; D presence over the full catalog; Lv2Housing on full Read | Next Great Work consumer or next carrier family. DB-derived GW candidate set (static + dynamic slot modifiers) with fail-closed fallback. Relaxing B170 D semantics is a contract change |
| AF-08 | Eight retirement mechanisms and no end-of-life criterion (Dialogue's retained duty is deliberate) | Next cutover (H, N3, P, J). One retirement contract via the Start option and exit registry; an exact exit plan per cutover; sunset window **DDR** |
| AF-06(a) | Full-scope hooks for unverified event signatures | After the user decides the evidence standard (Architecture `:111`) |
| AF-11 | Module roles unclassified; probe-named production authorities (CityFlowProbe, BindingProbe, ConstructionProbe, TradeRouteProbe signal) | Before any probe cleanup. A role field in `Runtime_Index.json` (user decision given Architecture `:107`) |
| AF-15 | Shared D0045 mechanisms (1T transaction, professional-unit protection, city reference) have no runtime home | Next 1T ability, J2 protection, T1. A narrow primitive used by new work first; no retrofit before native PASS |
| AF-16 | Facts model cannot express REALLOCATING / permanent debit; 27 direct readers | A dedicated slice before Commerce T |
| AF-17 | No ability-level conformance register; parameters hand-copied; manifest staleness carries no Design-drift signal | Before P0-V and balance tuning (governance decision) |
| AF-18 (+P08a-F01) | Bridge, transport and scheduler scaffolding copied per feature and drifting | Adopt shared helpers for the next consumer; DEFER migrating existing ones |
| AF-19 | Peer-to-peer carrier exclusion lists | Next carrier-writing Culture ability. A static test, not a runtime registry |
| AF-21, AF-22 | Cross-ability regression discouraged (literal stamps, exec/slicing, no reverse index). Non-hermetic DB/environment. Save/load simulated in one VM | Next change to a shared adapter (CrewProjectOrder, Gameplay.lua, P0Panel) or a persistence feature |
| AF-23 (+P10b-F01) | Template ledger tied to the live HD catalog without provenance. nil presence acknowledged as an empty init | H1 typed knowledge or any new template-init producer. Reject non-boolean presence before ACK; migration semantics **DDR** |
| AF-24 | Closure-per-call `P.Field`, unmemoized `IsTestPlayer`, turn read per counter increment. The GC trial locks itself off past 2 s | Cheap helper fixes alongside any performance pass. GC cadence is a user decision |
| AF-27 Crew sub-item (P07c-F01) | Crew receipt stage continues without readback | Before J1/J2 use Crew receipts as source or inventory evidence |
| Expedition F, I, J, K | UI reader in shared panel; name-based identity; owner-scoped source reference with listener-order cleanup; closed unversioned Store schema | Reattachment / N2 / broader civilizations. See [Expedition_Review.md](Expedition_Review.md) |

### 3.4 MONITOR, DEFER, NO_ACTION

**MONITOR**
- AF-07 LRU sub-claim: unreachable while every D consumer is governor-gated. Re-evaluate on a non-gated consumer, AI/MP, or a governor-count change.
- P13a-Q04 route-capacity silent cap: escalate before Harbor/Commerce O.
- P06a-Q01 setter visibility: escalate if AF-01 adds hooks.
- AF-25 instrumentation: becomes FBDF as the prerequisite for validating AF-05/06/07.
- SD-08, SD-09, SD-17, SD-18: cheap; fold into the next touch of those modules.
- Expedition G (complete-pair hold on load).
- P13b-F01.
- P09b-Q02.

**DEFER**
- AF-28 four-kind hard-coding (until a fifth kind is authorized).
- AF-26 identity tombstones and index routing (with cityKey work).
- AF-27 schema and versioning, beyond the Crew sub-item.
- P14a-F01 deploy rename window (before the next stable apply).
- Expedition L (singleton state; before multi-player).
- AF-18 migration of existing producers.
- P01-F03 / P15-F01 navigation labels.
- SD-12 (observation only).

**NO_ACTION**
- P06a-F01 and P13a-F04 (resolved).
- P08b-F01 (the probe starts retired).
- Prior audit retention rules: dedupe receipts and reservations are not GC-deletable; retired definitions keep exact cleanup; UNKNOWN is not confirmed loss.
- A whole rewrite, or DRY unification of assets, state machines or formulas.

---

## 4. The three highest-value engineering improvements before further expansion

These are ranked by how much future rework each prevents per unit of risk. Each is a *boundary* for user review, not an implementation plan or authorization. Each can be adopted by the next new ability first rather than retrofitted all at once.

### 1. Typed failure states with bounded, Gameplay-owned resolution

Covers AF-12, AF-13, AF-14 + P09b-F01, AF-03 consequences, and Expedition A/B/D/E/F.

**Why first.**
- It is the only class with permanent, per-save player-visible loss: cap1, a city that can never specialize, empire-wide network withdrawal at every cold load.
- Every planned transactional feature (N2 rewards, reattachment, Commerce contracts, Industry teams, 1T studies) adds new entries into the same terminal sinks.
- Today each module classifies failures by substring and chooses hold or withdraw independently.

**Boundary.**
- Providers publish a small typed status: VERIFIED / PENDING / CONFIRMED_INVALID / TERMINAL_HELD plus a code. Start with EffectiveFacts, the Store and NetworkBridge.
- Consumers map status to hold or withdraw in one declared table. Error strings remain diagnostics only.
- Holds record a structured kind and the prior phase.
- A UI-reader outage is classified as transient.
- The mutation flag is set immediately before the first write.
- One Gameplay-owned bounded resolver per transactional feature re-proves facts fresh and bumps the generation. It never grants and never deletes without proof. Expedition is the first adopter, together with the Production Manager cancellation fix.

**Keep:** never replay uncertain native actions; fail closed; UNKNOWN ≠ 0; no shared receipt key across assets.

**Decisions it needs (DDR):** cap1 release and spent production; partial-network semantics; per-feature abandon policy; UNKNOWN-reservation scope; outage policy (defer vs hold).

### 2. Declared composition: start order, propagation and persistence registration, verified by a real-composition test

Covers AF-10, AF-02, AF-01, SD-01, SD-04, AF-08 retirement contract, AF-19 static test.

**Why second.**
- Each ability currently costs about 4–6 central dispatcher edits, plus Store schema, validator and transfer edits, plus peer exclusion lists.
- No test runs the deployed composition, which is how SD-01 shipped unnoticed against a LOCAL_SIMULATION_PASS.
- Retirement has eight mechanisms, and one fails open.

**Boundary (staged).**
- (a) One test that runs the real Gameplay Start order. Do this first; it is the safety net for everything else.
- (b) An explicit central start table in the declared order, with per-module isolation and published status, INITIALIZED last, and retirement through the Start option.
- (c) An explicit central cause→consumer declaration, iterated by the existing call sites (no bus, no self-registration), plus a completeness test.
- (d) A code-level Store extension registration for the *next* persisted asset (no save-format change), with commit visibility settled.
- (e) A static test that every InternalOnly carrier has exactly one exit owner and is excluded by every building-event consumer. Promote the prior audit's W20 inventory for this.

**Keep:** declared order; explicit lists (now checked); exact-ID exits; single-commit atomicity. Respect the Architecture "no bus / no generic engine" constraints, adopting these as narrow primitives, which is itself a user decision.

### 3. A native-faithful, versioned test harness

Covers AF-09, AF-20, AF-21, AF-22, and the Expedition test gaps.

**Why third.**
- The project's dominant iteration cost is local PASS → deploy → native stall → a user game session. B201, B202 and B203 each followed that path, and four earlier failures came from context or library leaks the mocks allowed.
- Every UI-mediated feature planned next (reattachment, N2/N3 bridges, repeat missions) is in exactly the class the harness cannot represent.
- Evidence claims cannot be reproduced from Git.

**Boundary (incremental).**
- Per-context Lua runtimes or `_ENV` sandboxes that share only `ExposedMembers` and a deferred operation queue.
- A curated per-context API allowlist with provenance, where unknown APIs error.
- A multi-listener event mock in registration order, with lifecycle profiles (init or frames delivered, delayed, withheld).
- A 5.1-profile runtime and a `cold_load()` helper.
- A machine-readable executed closure per batch, with EXCLUDED reasons and a module→test reverse index.
- Adopt for new tests and the B202–B204 observers first. No full-Mod simulator; frozen tests stay frozen unless the user sets a policy.

**Why not performance first.** AF-05, AF-06(b) and AF-07 are real and structural. But the only native evidence (T39–T62, 10–13 cities, no reported stutter) does not show a present problem, and there is no measurement beyond it (AF-25). Recommended instead:
- Take the cheap, semantics-preserving fixes opportunistically: SD-08 reorder, scope transfer cleanup to the transferred city, closure-free `P.Field`.
- Define one bounded late-game benchmark (a user decision).
- Decide the larger restructuring (keyed revisions, candidate sets, GW candidate sets) on measured data before any large-map or wartime playtest. AF-06(b) is the first to take up when that happens.

## 5. Concerns to defer

These should not displace the three above:
- Generalizing the specialization set (AF-28), until a fifth kind is authorized.
- Identity tombstones and refounding (AF-26), Expedition multi-player and singleton state (L), and the name-based identity carrier (I), until scope widens beyond the cap-1 test civilization.
- Migrating existing producers to shared bridge/scheduler helpers (AF-18). New consumers adopt first.
- Schema-version formalization (AF-27), beyond the Crew readback gate.
- The 1T primitive (AF-15) and REALLOCATING (AF-16), until their first dependent slice.
- Deployment rename window (P14a-F01), until the next stable apply.
- GC cadence and LRU sizing, until measured.
- Navigation and metadata labels (P01/P15).

## 6. Consolidated user decisions surfaced (not decided here)

**Gameplay or save semantics (DESIGN_DECISION_REQUIRED)**
1. Expedition: cap1 release for a unit-less HELD; spent production; END-only resolution for a surviving unit; empty-queue-after-queued as cancellation evidence (replacing B202 `P0_N_Expedition.md:25`); retryable pre-binding naming failures; never-submitted travel back to CREATED; identity carrier beyond the test civilization.
2. Per-feature abandon policy for terminal holds (Investment INTENT, Claim CALLING, tradition, `completionError`), and one 1T hold/abandon convention.
3. Partial-network semantics (exclude, freeze or withdraw) and the per-ability hold/withdraw mapping, including unsupported acquisitions.
4. Whether an UNKNOWN Store reservation should also suppress loss recording, exits and all admissions (B169 accepted rejecting unprovable reference changes; nothing records weighing these side effects). Also late return acceptance and inferred loss.
5. Placement and failure granularity of new per-city ledgers.
6. Which effects must refresh synchronously after investment and unit actions.
7. Outage policy when a UI reader is absent: defer vs durable hold.
8. Save-compatibility window for retired carriers, B055 rows and superseded unit types; catalog-drift migration; rebuilding empty template ledgers (P10b).

**Scope, governance and contract decisions (user approval; not gameplay)**

9. HD and District Expansion HD as declared dependencies; release identity (test civilization vs general rule set).
10. Narrow shared primitives within Architecture `:65` / `:87` / `:107` and D0032 `:25`: cause/consumer declaration, start table, Store extension registration, bridge primitive, typed status.
11. Contract changes: narrowing Architecture `:115` foreign reconciliation; relaxing B170 full D presence; the evidence standard for verified native event signatures (`:111`).
12. A role/lifecycle field in `Runtime_Index.json`; a conformance register; a machine-readable test closure in batch manifests; the frozen-test policy.
13. Which DEV and prototype controls stay in playtest builds (TimedTurnProbe, overflow-sink project, free CREATE, cheats).
14. A late-game benchmark definition and turn-time / GC-pause budgets.

## 7. Unknowns that bound these conclusions

These are native questions that static review cannot settle:
- listener dispatch order
- whether `CityProductionCompleted.canceled` fires on queue removal
- whether a Lua `CreateBuilding` raises `BuildingConstructed`, and whether `OnBuildingConstructed` exists
- ExposedMembers lifetime across in-game loads, and SetUpdate delivery to hidden contexts
- equal-LoadOrder tie-breaks and duplicate action ids
- whether the Production Manager lists and removes the Expedition entry under HD
- whether off-map Spies appear in `GetUnits():Members()`
- city-ID reuse
- native property serialization limits
- engine cost of about 1.7k internal buildings
- late-game frequency and cost of every hot path

Also not read: the HD version string; loaded-DB carrier counts; the user's enabled mod set.

None of these is requested as a test. Each is listed so that a future native session can be scoped deliberately.

## 8. Checkpoint / handoff

**Completed scope.** Phase A (independent investigation, persisted before cross-review), Phase B (cross-review of all eight prior priorities, the functional gates, the low-rated and Q observations, and the prior audit's constraints), and Phase C (this register).

**Stable files** (writes paused for checkpoint):
- `Specialization/Reports/Advisory/Architecture_Engineering_Audit/Audit_Ledger.md`
- `Specialization/Reports/Advisory/Architecture_Engineering_Audit/Architecture_Findings.md`
- `Specialization/Reports/Advisory/Architecture_Engineering_Audit/Expedition_Review.md`
- `Specialization/Reports/Advisory/Architecture_Engineering_Audit/Final_Review.md`

All four are local and ignored by Git, which is the expected state.

**File precedence.** Phase A files are kept as written for provenance. Where §2.4 adjusts a rating or wording, this file supersedes them.

**Remaining questions.** The DDR and user decisions in §6, and the native UNKNOWNs in §7.

**Next entry.** User review of §3.1 (FIX_NOW) and §4 (top three boundaries).
- Acceptance of these reports into Git follows the existing checkpoint process: Primary reviews read-only, the user accepts named files, and Primary commits.
- Acceptance for Git is not acceptance of the recommendations.
- No Design decision, implementation, test, deployment or game launch is implied or requested.

**User decision.** The §6 items as and when relevant. **User testing.** None requested. **Primary next.** None, unless the user separately authorizes work.
