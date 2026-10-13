# Architecture and Engineering Findings (Phase A, independent)

Advisory / Non-authoritative / No design decision implied
Status: Stable (Phase A content frozen before Phase B; Phase B/C additions live in Final_Review.md)
Maintainer: Advisor session (Claude), attribution only — not session authorization
Scope: Structural risks that grow with additional abilities and specializations, across six dimensions: modularity, state/persistence, performance/scalability, native integration, shared mechanisms/debt, testing/evidence, plus Design↔implementation consistency. The Expedition B202–B204 detail is in [Expedition_Review.md](Expedition_Review.md). Gameplay balance, wording and the known B204 native-test requirement are excluded.
Basis: `develop` at `2b75e12` (HEAD later `f843c0f`; there is no `Mod/` or `DevelopmentTests/` difference, see [Audit_Ledger.md](Audit_Ledger.md)). Runtime B204.231 / modinfo231. External read-only sources: Civ VI install (`<CivVI>` = configured Steam install, `Civ6.app/Contents/Assets/...`) and Harmony in Diversity = Workshop item `2465378070` (`<Workshop289070>/2465378070`, identified by `DL.modinfo` name `LOC_HARMONY_IN_DIVERSITY_NAME`). The HD version string was not recorded and is UNKNOWN. Reading `DebugGameplay.sqlite` was not possible, because `local/config.json` is absent.

**Independence.** This file was written before reading `Specialization/Reports/Audit/` (the previous comprehensive audit). Nothing under that directory was opened during Phase A.

## How to read this report

- **Evidence levels.**
  - STATIC_CONFIRMED means the claim was read in source.
  - Nothing here is LOCAL_SIMULATION_PASS (no tests were run) or USER_GAME_TEST evidence.
  - Historical result files are another agent's interpretation and are labelled as such.
- **Method.**
  - Nine independent slices were investigated, and each was adversarially re-verified by a separate agent. A completeness critic then covered the gaps.
  - The results were consolidated into root-cause clusters. The report owner spot-checked the highest-impact claims (marked **[owner-verified]**).
  - Ratings are the verifier-adjusted ones unless stated. Where slices disagreed, the divergence is noted.
- **Ratings.**
  - Severity: CRITICAL / HIGH / MEDIUM / LOW / OBSERVATION.
  - Timing: FIX_NOW / FIX_BEFORE_DEPENDENT_FEATURE (abbreviated **FBDF**) / MONITOR / DEFER / NO_ACTION.
- **Labels.**
  - `DDR` = DESIGN_DECISION_REQUIRED (the user decides).
  - "Contract change" means the item amends a documented Architecture contract, so it needs user approval even though it is not a gameplay change.

No finding was rated CRITICAL. The runtime is consistently fail-closed: no reviewed path silently double-grants rewards or corrupts saved state. The dominant risk is that **cost and fragility grow superlinearly with each new ability**.

## Summary table

| ID | Finding | Sev / Timing | Dimension |
|---|---|---|---|
| AF-01 | Per-city progression Store is the accretion point and a whole-city fail-closed boundary | HIGH / FBDF | State, modularity |
| AF-02 | Change propagation is hand-wired: a 640-line string dispatcher plus divergent consumer lists | HIGH / FBDF | Modularity, performance |
| AF-03 | Gameplay authority depends on UI-context closures hosted in a shared ProductionPanel replacement | HIGH / FBDF | Native integration |
| AF-04 | Native panel replacements are hard-wired to HD private files; no declared HD dependency or LoadOrder policy | HIGH / FBDF | Native integration |
| AF-05 | World-scope reconciliation and cleanup sweeps have no bounded candidate set | HIGH / FBDF | Performance |
| AF-06 | Event scope and invalidation are too coarse (unscoped foreign events, global write counter) | HIGH / FBDF | Performance |
| AF-07 | Building-presence checks scale with the whole Buildings catalog, including about 1.7k+ SPC carriers | HIGH / FBDF | Performance |
| AF-08 | Retirement and cutover have no single contract; retired modules remain load-bearing | HIGH / FBDF | Debt |
| AF-09 | Test harness: one Lua state for all contexts, per-file mocks, synchronous single-slot events | HIGH / FBDF | Testing |
| AF-10 | Module composition by include/Start order: unguarded startup, decorators, implicit globals | MEDIUM / FBDF | Modularity |
| AF-11 | Module role and lifecycle are unclassified; probe-named modules carry production duties | MEDIUM / FBDF | Debt |
| AF-12 | Uncertain-outcome holds are terminal, re-implemented per feature, and propagate across abilities | MEDIUM / FBDF | State |
| AF-13 | Loss/return lifecycle is one-shot and event-bound; exit registration is voluntary | MEDIUM / FBDF | State |
| AF-14 | Network capture is all-or-nothing per player; failure polarity is per-consumer and string-typed | MEDIUM / FBDF | State, integration |
| AF-15 | Shared D0045 mechanisms (1T transaction, professional units, city reference) have no runtime home | MEDIUM / FBDF | Modularity, Design |
| AF-16 | Identity/Potential facts model cannot express REALLOCATING or a permanent debit | MEDIUM / FBDF (before Commerce T) | Design, state |
| AF-17 | No Design↔runtime conformance register; parameters hand-copied; confirmed drift | MEDIUM / FBDF | Design |
| AF-18 | Cross-context bridges, transport and concurrency scaffolding are bespoke per feature | MEDIUM / FBDF (new work) | Integration, debt |
| AF-19 | Carrier ownership is peer-to-peer exclusion lists; building-event reentrancy is per module | MEDIUM / FBDF | Modularity, performance |
| AF-20 | Executed test closure is not versioned; manifest-listed regressions lapsed unnoticed | MEDIUM / FIX_NOW | Testing, evidence |
| AF-21 | Cross-ability regression is structurally discouraged (literal stamps, source slicing/exec, no reverse index) | MEDIUM / FBDF | Testing |
| AF-22 | Evidence environment is non-hermetic; save/load is simulated inside one VM | MEDIUM / FBDF | Testing |
| AF-23 | Persisted data depends on the live HD catalog without provenance | MEDIUM / FBDF (template ledger) | State, integration |
| AF-24 | Allocation-heavy helpers on hot paths; the GC trial is the only late-game backstop | MEDIUM / FBDF (helpers) | Performance |
| AF-25 | Instrumentation blind spots; no performance evidence after B139 or beyond T62 / 13 cities | LOW / FBDF (prerequisite) | Performance, evidence |
| AF-26 | City identity: location routing, never-shrinking index, three encodings | LOW / FBDF | State |
| AF-27 | Persistence primitives and schema-version semantics are ad hoc per store | LOW / MONITOR | State |
| AF-28 | Four-specialization set hard-coded in ≥17 Lua and several SQL files | LOW / FBDF (only if a fifth kind is authorized) | Modularity |

Concrete standalone defects are listed at the end as SD-01 … SD-18.

---

## 1. Architecture and modularity

### AF-01 Per-city progression Store is the accretion point and a whole-city fail-closed boundary — HIGH / FBDF

**Slices.** A1-03, A2-01, A5-09, A7-03. Verifiers rated it HIGH three times and once lowered it to MEDIUM for the fault dimension only.

**Facts (STATIC_CONFIRMED)**
- `Mod/CityProgressionStore.lua:1-2` — the persistence layer includes ability models (ResearchTradition, DialogueProjectModel).
- `:90-109` — `validate()` inlines four ability domains:
  - Industry `templateLifecycle`
  - `SPCResearchTradition.Validate`
  - `SPCDialogueProjectModel.Validate`
  - `claimTimer`
- `:110-115` — it then delegates to the legacy `SPCCityIdentityRead.Preview(...)`, which encodes legacy shape rules (`Mod/CityIdentityRead.lua:44,73,79,84-91`). That file describes itself as "read-only evidence".
- `:270-277` — `WriteInvestment` embeds the Research P4 tradition-start rule.
- `:591-594` and `:616-619` — the Store owns each asset's owner-change policy:
  - Standardization `ValidateRetained`
  - Dialogue cancel
  - `researchTradition.state='OWNER_POLICY_UNRESOLVED'`
- `:497-502` — `restore()` sets the worker `fault` on any validation failure at load. `:143-149` — `active()` then refuses all reads. `Base`, `Investment`, `DialogueState` and `ReadTradition` all route through `active()`, and `Mod/EffectiveFacts.lua:15,19` depends on it.
- `Mod/ResearchTradition.lua:10-14` — a cross-domain invariant: exactly 3 investment receipts.
- `Mod/CityIdentityRead.lua:8-24` — one copy budget (8,192 nodes / 65,536 string bytes) is shared by every domain in the record.
- `Mod/ExpeditionSpyStore.lua:94-147` — a second store re-implements the schema, generation and compare-and-set (CAS) logic instead of reusing the first.

**Inference (high on mechanism, medium on projected cost)**
- Each new persisted per-city asset (Culture permanent records, Commerce contracts, Wonder credits, N2 observations, Teams) adds at least four edit sites to the most regression-sensitive module (1,261 lines).
- A defect or a stricter validator in one domain holds Identity, Potential and Investment reads for the whole city. Through AF-14, that also fails the player's network input at cold load.
- Ability rules placed in the Store are not revisited when that ability's Design changes; SD-02 is the realized case.

**Counterevidence**
- `save()` validates before writing (`:165-169`), so a malformed runtime write cannot persist.
- Production isolation is per city (`:658`, `:806`).
- Old saves are explicitly unsupported (`:827`), so migration pressure is low.
- The single-record design is deliberate (`Specialization_v0.1_Architecture.md:65`), and Architecture `:83` lists specialization coupling as a retained audit item.
- Single-record atomicity on loss and return is a real benefit.

**Consequence.** Each new ability either edits the save authority or forks yet another store with its own CAS, readback and UNKNOWN semantics.

**Remediation boundary (advisory)**
1. A code-level extension registry: each asset registers its name, version, `validate`, `onTransfer`, `onReturn` and `onInvestmentCommitted`, while one commit and readback is kept. This needs no save-format change.
2. A Store-owned validator replaces the Preview delegation.
3. A placement rule for new ledgers: core record vs. isolated per-domain key.

Placement, and failure granularity (should a broken optional extension hold only that ability?), are **DDR**.

**Trade-offs.** Isolation loses single-write atomicity across domains, and a city could run on a partially trusted record.

**Regression risk.** LOW–MEDIUM if new assets adopt the registry first. HIGH if all four inline domains are retrofitted in one step.

### AF-02 Change propagation is hand-wired: string dispatcher plus divergent consumer lists — HIGH (extensibility) / FBDF

**Slices.** A1-01, A3-05, A5-06, A5-07, A7-06, A7-07. Present correctness impact is MEDIUM or lower: no stale-effect defect has been proven from list divergence alone.

**Facts**
- `Mod/Gameplay.lua:38-675` — `request()` is a single if-chain over about 129–131 literal action strings plus three prefix families. It has one shared reply slot (`shared.Snapshot`/`LastToken`, about 60 assignments) that is also read by production panels (`UI/UnitPanelActions.lua:94-95`).
- There are six hand-maintained consumer fan-out lists, which differ in membership, scope and guards:
  - `Gameplay.lua:21-37` (2 consumers plus Dialogue)
  - `:487-504` (14 consumers, run for SPAWN, PREPARE and CONFIRM; Lv3Effects and NetworkBoost unscoped at `:502-503`)
  - `:565-583` (INVEST_*, omits NetworkBoost and Dialogue)
  - `:515-532` (15 consumers, three guard styles, including the no-op `Lv4Percent` and the never-started `CultureMeaningProbe`)
  - `:323`
  - `Mod/NetworkBridge.lua:59` (5 legacy consumers)
- `git show 94c964b` — adding Culture Inspiration L3 edited five `Gameplay.lua` sites plus two peer exclusion lists, 13 Mod files in total. A notification-isolation fix followed (`bc54482`).
- `Gameplay.lua` is touched by 61 of 140 Mod commits; `UI/P0Panel.lua` by 58.
- Unreachable branches have been left behind by retirement intercepts (`:79-86`, `:246-296`, and the GW_READ duplicate at `:418` shadowed by `:390`).
- 14–18 tests slice `request()` by text marker.

**Inference.** About 4–6 central edits per ability. An intentional omission cannot be told apart from an accidental one. A miss shows up only as a stale effect until some unrelated event refreshes it. Each preview click runs about 14 player-wide audits.

**Counterevidence**
- Most consumers also subscribe to native events and converge later.
- The INVEST_* path is DEV-hidden (`P0Panel.xml:11,13`).
- One sub-claim is REFUTED: retiring Lv2GPP would *not* stop governor propagation, because consumers subscribe natively.
- Architecture explicitly declines a general event bus (`:87`, `:107`).
- Expedition already bypasses the chain with its own channel (c61524e changed `Gameplay.lua` by +2 lines).

**Remediation boundary**
- Within the "no bus" constraint: one declarative cause→consumer table `{consumer, causes, scopeRule, guard}`, iterated by the existing call sites with deterministic order and per-call pcall (the `GreatWorkFacts.RegisterConsumer` pattern).
- An action→handler table that owning modules fill. Duplicate registration fails at start. A separate DEV table.
- Owner-keyed reply slots.
- A static test that every module exposing `Audit` is registered or explicitly exempt.

Which effects must refresh synchronously after an investment or unit action is a **DDR** (it also decides whether the current omissions are intended). Adopting shared primitives in spite of Architecture `:87`/`:107` is a contract change.

**Regression risk.** MEDIUM. Run an old-versus-new delivery-set parity test per cause first. Text-slicing tests need rework.

### AF-10 Module composition by include/Start order — MEDIUM / FBDF

**Slices.** A1-05, A1-06, A5-05, A4-09, A7 verifier-missed. SD-01 and SD-04 are realized instances.

**Facts**
- Startup sequence:
  - `Gameplay.lua:676-682` registers the request handler and publishes "INITIALIZED" *before* any module starts.
  - About 60–62 `.Start(P,shared)` calls follow (`:706-912`).
  - Only Claim, DialogueProjects and DialogueEffects are pcall-isolated (`:861-883`).
- Start-time peer asserts tie modules together: `CultureInspiration.lua:7`, `CultureMeaning.lua:8`, `ExpeditionTraining.lua:5`, `ClaimProjects.lua:4`.
- The head of the production fact chain requires DEV-only probes at Start (`CityFlowProbe.lua:60-69` → `FreshBindingHook.lua:5,8`). Removing those probes aborts Gameplay before `EffectiveFacts` starts (`:745-748`).
- Hook-order traps:
  - `Gameplay.lua:858` resets `shared.OnPermanentCityWrite=nil` before ClaimProjects wraps it.
  - `CrewPrecision.lua:22-23` replaces `shared.UnitActions.Run` and works only because UnitActions starts first (`:792-799`); see SD-01.
- Implicit globals: `SPCNetworkInput` is used without an include (`ExpeditionSpyGate.lua:98,351,498`; `ExpeditionTraining.lua:11`), and `SPCResearchTradition` is reachable only through the Store's include.
- No test runs the real Start order. `DevelopmentTests/test_investment_update_propagation.py:112-113` starts a hand-picked subset.

**Inference.** A throw in any unguarded Start aborts every later Start, including Expedition, NetworkIsolation and the GC trial, while requests are still served against a partial `shared` table and the UI shows INITIALIZED. Cleaning up a probe can disable production modules.

**Counterevidence.** Errors reach `Lua.log`, so the failure is not fully silent. Many Starts validate lazily. Mark/Flush designs reduce sensitivity to same-event ordering.

**Remediation boundary**
- An explicit start table `{name, start, dependsOn, lifecycle}`: production first, per-module pcall with published status, INITIALIZED last, and fail-closed dependents.
- Retire modules through the Start option.
- A lint for `SPC*` globals.
- One composition test that uses the real Start order.

**Regression risk.** LOW–MEDIUM.

### AF-15 Shared D0045 mechanisms have no runtime home — MEDIUM / FBDF

**Slices.** A7-04, A7-05, A5-15, A2-06.

**Facts**
- Three independent full-production-turn (1T) project transaction implementations: `ClaimProjects.lua:106-188`, `DialogueProjects.lua:124-236`, `TimedProject.lua:79-104`. `Industry_Preparation.md:135` still lists the 1T primitive as "to establish", while `Shared_D0045.json:98` says the Industry study "uses the same full1T transaction semantics as Dialogue".
- Professional-unit protection is defined once for three professions (`Shared_D0045.json:147-160`), but its only implementation is the Spy-shell stack (`Data/ExpeditionSpyGate.sql:2-6`).
- Crew units set `CanCapture=0` without the other protection fields (`Data/Crew.sql:2-16`).
- Expedition alone cost about 3.3k Lua lines, 29 test files and builds B178–B204 (another agent's tally; native confirmation pending).
- City references are encoded at least three to five ways (`NetworkInput.lua:7-10`, `SampleLifecycle.lua:6-9`, `CityProgressionStore.lua:31`, and others). The literal `SPC_DEV_BINDING_B013_TOKEN` recurs in the newest modules instead of the shared constant (`CityIdentityRead.lua:4`).

**Inference (medium).** Industry I3/J1/J2 and Commerce T1 will clone the 1T and unit logic again.

**Counterevidence**
- Design and Architecture reject a generic engine but plan shared primitives (`D0032_Adaptation.md:25`; `Shared_D0045.json:83`).
- Cancellation policy legitimately differs per asset.
- Much of N1's cost was native discovery that refactoring cannot remove.
- One sub-claim is REFUTED: `ResearchCrossModel.lua:5` is a whitelist, not a copied mapping.

**Remediation boundary**
- A narrow 1T transaction primitive with per-asset policy callbacks, used first by the next new 1T ability rather than retrofitted.
- A shared domain/yield-share table.
- One cross-profession unit-protection investigation before J2/T1.
- A `CityReference` module and a constants table for save-visible keys.

"Primitive vs. framework" is a user-approved Architecture decision.

**Regression risk.** LOW for new work; MEDIUM–HIGH if retrofitted onto Claim/Dialogue/Expedition before native PASS.

### AF-16 The facts model cannot express REALLOCATING or a permanent Potential debit — MEDIUM / FBDF (before Commerce T)

**Slices.** A7-10 (QUALIFIED), A7 verifier-missed.

**Facts**
- `Mod/EffectiveFacts.lua:22-24,46` allows only NONE with potential 0, or foundation 1 + receipts (capped at 3 receipts).
- `CityProgressionStore.lua:86` asserts `base.potential==1`.
- "REALLOCATING" does not appear anywhere in Mod, while D0032 defines it (`D0032_Adaptation.md:31-36`) and `Commerce_Preparation.md:28-29` forbids faking it by clearing Identity.
- 27 Lua files call `EffectiveFacts.Read` directly. The `CurrentSpecializationFacts` facade is bypassed (REFUTED as a containment point).
- The Preview rule (`CityIdentityRead.lua:79`) and the tradition rule (`ResearchTradition.lua:14`) both enforce an append-only receipt count that "cannot encode a permanent debit" (`D0032_Adaptation.md:32`).

**Consequence.** Done ad hoc during Commerce T, this becomes the widest-reaching late change in v0.1: about 27 readers plus Store validation.

**Remediation boundary.** A dedicated slice before T: an identity-mode field and a permanent debit on the progression record and on `EffectiveFacts.Read`, with an explicit consumer contract (under REALLOCATING: no profession, ACTIVE 0, no first-completion or claim). This is linked to the AF-01 DDR.

**Regression risk.** HIGH if done ad hoc; MEDIUM as a dedicated slice.

### AF-28 Four-specialization set hard-coded — LOW / FBDF only if a fifth kind is authorized

**Slices.** A1-04, A7-11 (both downgraded to LOW).

**Facts**
- A central map (`Probe.lua:5-6`) is used by 7 modules, but local copies exist in `Lv2GPP.lua:8-10`, `Lv3Support.lua:11`, `Lv3Effects.lua:12` and others.
- Persisted-record checks hard-code the set (`CityProgressionStore.lua:25,58,73,86,378,1017`; `NetworkInput.lua:45-46`).
- `InstitutionPresentation.lua:4-13` is keyed by level and covers Research only, while `Harbor_D0037.json:18-23` has two simultaneous level III/IV institutions.

**Counterevidence.** v0.1 is limited to four kinds by Authority. Unknown kinds fail closed and loud.

**Remediation.** Only after authorization: a descriptor table (kind → districts, GP classes, text keys, claim project, participation) and presentation keyed by institution id. Whether to prepare for Government, Military or Harbor now is a user decision.

---

## 2. State and persistence

### AF-12 Uncertain-outcome holds are terminal, re-implemented per feature, and propagate across abilities — MEDIUM / FBDF

**Slices.** A2-02, X-06, A2 verifier-missed, and the Expedition clusters A/H in [Expedition_Review.md](Expedition_Review.md), where the same root is rated HIGH because of the cap1 consequence.

**Facts**
- **Investment.** INTENT is persisted before the native Destroy (`InvestmentAction.lua:128-136`). Load recovery only calls `finish()`, which requires CONSUMED_CONFIRMED (`:54`, `:176-177`), so INTENT never resolves. It then blocks Prepare and ReadView (`:71`, `:94`) and blocks recapture (`CityProgressionStore.lua:575`).
- **Claim.** CALLING is persisted before `FinishProgress` (`ClaimProjects.lua:166-168`), and new requests are refused while CALLING (`:106`).
- **Research tradition.** `OWNER_POLICY_UNRESOLVED` and `UNKNOWN_INTERVAL` are absorbing (`ResearchTradition.lua:27-29`).
- **Registration.** One test-player `OnDistrictConstructed` without a resolvable city calls `HoldCompletion` on every worker (`CityProgressionStore.lua:1148-1158`, **[owner-verified]**). That persists `completionError` on every UNASSIGNED ACTIVE record (`:319-321`). Nothing ever clears it, and `active()` fails on it (`:148`).
- **Propagation.** `EffectiveFacts.lua:47` sets `investmentPending`, which then blocks Dialogue (`DialogueProjects.lua:36,94`) and Expedition (`ExpeditionSpyGate.lua:338,495`; `ExpeditionTraining.lua:33`) in that city.

**Inference.** Which holds can be resolved is an implementation accident: Dialogue can, Claim and Investment cannot, and Expedition only by destroying a live unit. One stuck intent disables unrelated abilities in that city. One unresolved district event permanently holds every not-yet-specialized city, and through AF-14 the player's network.

**Counterevidence.** Never replaying an uncertain native action is deliberate and user-endorsed (`D0032_Adaptation.md:58`). Fail-closed never double-grants.

**Remediation boundary**
- A shared convention, not an engine: common stage names (INTENT / SIDE_EFFECT_ATTEMPTED / COMMITTED / HELD), a typed `TERMINAL_HELD` signal so gates can tell a transient pending from a terminal hold, and a common receipt key.
- Optionally, a user-confirmed RESOLVE/ABANDON that never grants anything.

The abandon policy per feature is **DDR**.

**Regression risk.** MEDIUM.

### AF-13 Loss/return lifecycle is one-shot and event-bound; exit registration is voluntary — MEDIUM / FBDF

**Slices.** A2-04, A2-11, A2 verifier-missed (one-shot recapture; UNKNOWN reservation).

**Facts**
- `CityProgressionStore.lua:614-619`: HELD_TRANSFER is written only from a live `CityTransfered`. On load, `reconcile()` runs with no arguments, so `recapture()` returns false (`:552-553`, `:629`).
- Recapture must satisfy, at the moment of the event, all of: same-turn proof, all exits finished (at most 3 attempts per session), no pending investment, an unambiguous district rebind, and Industry `ValidateRetained` (`:557-594`). Any failure is swallowed by pcall, and the city stays HELD.
- An UNKNOWN reservation elsewhere makes the loss write raise `STORE_REFERENCE_UNKNOWN` inside `storage.Write`. That faults the worker (`:749-752`, `:681-685`, `:168-169`), so no `loss` is recorded and no exits run.
- Pcall-isolated modules register their exit at the *end* of Start (`ClaimProjects.lua:204`), so a startup failure silently drops the exit.
- `DevelopmentTests/test_p0_e2_exit.py:24` hard-codes 21 modules, against 34 `RegisterExit` names in Mod. Nothing maps every InternalOnly carrier to an exit owner.
- The loss evidence omits the pre-loss local reference (`:619`), so consumers infer identity differently (owner/cityID versus location).

**Inference.** A missed loss leaves internal carriers applying to the foreign owner indefinitely. A failed return holds the city permanently.

**Counterevidence**
- Requiring confirmed native loss is deliberate (B096/B169; Architecture `:59`).
- HELD_TRANSFER exits re-run on load.
- Some modules clean foreign carriers themselves at startup.

**Remediation boundary**
1. A static test deriving every InternalOnly `BUILDING_SPC_*` and plot-flag carrier and asserting exactly one exit owner.
2. Register exits before fallible startup steps.
3. Persist "return evidence accepted, preconditions pending" so a later session can finish the return.
4. Pass the pre-loss reference to exits.

Whether load may infer an unconfirmed loss, or accept a held return later, is **DDR**.

### AF-14 Network capture is all-or-nothing per player; failure polarity is per-consumer and string-typed — MEDIUM / FBDF

**Slices.** X-01, X-02, A2-04, plus a trigger widened during consolidation.

**Facts [owner-verified]**
- `Mod/NetworkInput.lua:26-44`: `Capture` loops over every owned city. A city whose facts raise, with no same-session previous value, causes `error('NETWORK_FACTS_UNAVAILABLE')` for the whole player whenever `BlocksLegacy(c)` is true. In production `BlocksLegacy` always returns true (`CityProgressionStore.lua:983`).
- `CityFlowProbe.lua:128-129` raises `FOUNDATION_EVIDENCE_PENDING` for any owned city not routed to a Store record.
- Admission covers only own founding and conquest from an AI major or city-state (`CityProgressionStore.lua:1039,1066`). Free City, trade and gift acquisition are explicitly deferred (`P0_E2_Plan.md:834`).
- Other triggers: a HELD record, a persisted `completionError` (AF-12), a faulted worker (AF-01), and a razed-and-refounded plot (AF-26).
- Consumers react with opposite polarity:
  - **Withdraw:** `Lv3Effects.lua:65-66`, `NetworkBoost.lua:71-73`, `CommerceConvergence.lua:89-90`.
  - **Hold:** `CopyYields.lua:41-45`, `StandardizationDiscount.lua:165-175`, `Lv2Housing.lua:48,76`.
  - **Mixed:** `Lv3Support.lua:58-61` decides by substring; `CultureAesthetic.lua:90-92`.
- Classification is by substring or regex over error text (`Lv3Support.lua:58`, `CopyYields.lua:93`, `UnitActions.lua:141,156`, `CityProgressionStore.lua:624`, `ExpeditionSpyGate.lua:120-122`).
- No test references `NETWORK_FACTS_UNAVAILABLE` or `FOUNDATION_EVIDENCE_PENDING`.

**Inference.** At every cold load while one such city is owned:
- national Boost, Commerce Convergence and Commerce Lv3 links are withdrawn empire-wide;
- Copy and Standardization keep possibly stale carriers.

The result is a mixed partial state that is hard to diagnose from player reports. Renaming an error code can silently flip hold versus withdraw.

**Counterevidence**
- `P0_E2_Plan.md:480` accepts that ownership changes can invalidate the verified snapshot.
- Fail-closed is documented as intentional (`NetworkInput.lua:36-37`).
- National totals genuinely depend on every city.

**Remediation boundary**
- A typed per-city status (`VERIFIED` / `PENDING` / `CONFIRMED_INVALID` / `TERMINAL_HELD` + code) at the providers (EffectiveFacts, Store, NetworkBridge; precedent `NetworkBridge` validity, `EffectiveFacts.activeStatus`).
- One declared mapping from status to hold or withdraw per consumer.
- Cold-load tests with one held or unregistered city among healthy ones.

Partial-network semantics (exclude, freeze, or withdraw) and the per-ability mapping are **DDR**.

### AF-23 Persisted data depends on the live HD catalog without provenance — MEDIUM / FBDF (template ledger); LOW (tooling)

**Slices.** A2-07, X-04, X-05.

**Facts**
- `Mod/Standardization.lua:22-25,53-54` asserts the current catalog district and tier for every learned row (`STD_CATALOG_MIGRATION_REQUIRED`). The template record has no catalog-version field (`CityIdentityRead.lua:84-91`), although `D0032_Adaptation.md:47` requires one.
- Recapture calls `ValidateRetained` inside the one-shot window (`CityProgressionStore.lua:591-594`), so catalog drift turns into a permanent HELD_TRANSFER.
- `tools/deploy.py` records no HD identifier. `Data/CultureMeaningProbe.sql` (405,746 bytes, loaded at `modinfo:22`) has no committed generator.

**Remediation boundary.** Persist catalog provenance. Separate structural validity from current-catalog match. Record an HD fingerprint in deploy receipts and native results. Commit generators with `--check`.

Migration semantics are **DDR**.

### AF-26 City identity: location routing, never-shrinking index, three encodings — LOW / FBDF (prerequisite for cityKey, reattachment, N2)

**Slices.** A2-03, A2-05, A2-12.

**Facts**
- `CityProgressionStore.lua:866-871` routes by `positions[x:y]`.
- `:781-796` — index entries cannot be removed, and `candidate()` refuses any recorded location (`:1003-1004`).
- `referenceKey` ignores `referenceInvalidated` (`:665-676`).
- Every listed event goes to every worker ever allocated (`:1249-1257`, `:793-808`, `:894-905`).
- Expedition persists `SPCNetworkInput.Reference` (owner/ID/x/y/raw token) as its source binding, although that module's header says it is "not a … save ledger" (`NetworkInput.lua:1`).

**Remediation.** A tombstone state that releases location and reference occupancy; a Store-provided `IsCurrentReference` accessor; event routing through the index.

Refounding semantics are **DDR**.

### AF-27 Persistence primitives and schema-version semantics are ad hoc — LOW / MONITOR

**Slices.** A2-06, A2-08, A2-10, A2-13, X-03, plus E1-14 / Expedition cluster K.

**Facts**
- There are 26 local deep-equal and 16 local copy helpers.
- Failure contracts diverge: the Store throws and faults; `ExpeditionSpyStore` returns `(nil, code)` with classified readback; Crew rewrites with no readback (`UnitActions.lua:117-121`).
- The Store's `schema` field records provenance (1/2/3), not format.
- The two stores take opposite unknown-field policies (open versus closed-world). The closed one has no version, so a newer record reads as `STORE_CORRUPT` (Expedition cluster K).
- There is no writer-build stamp in saves.
- Crew receipts are an unbounded ledger with no consumer, contrary to the retention requirement in `D0032_Adaptation.md:58`.

**Remediation.** A small `CheckedRecord` helper modelled on `ExpeditionSpyStore.lua:134-147`; an explicit format version separate from provenance; a distinct `STORE_NEWER_SCHEMA` outcome; a save-level last-writer stamp. Whether cross-build loads are blocked or tolerated is **DDR**.

---

## 3. Performance and scalability

Costs multiply: (world or event scope) × (catalog or carrier rows) × (consumers) × (allocations per check). Existing native performance evidence (B129–B139, another agent's transcription of user screenshots) covers T39–T62, about 10–13 own cities and at most 5 routes. It does not cover any B140–B204 code path.

### AF-05 World-scope reconciliation and cleanup sweeps have no bounded candidate set — HIGH / FBDF (transfer/init); MEDIUM / MONITOR (per-turn foreign)

**Slices.** A3-01, A3-02 (lowered to MEDIUM/MONITOR), A3-12, A5-10, A5-11, and the A3 verifier-missed StandardizationDiscount item.

**Facts [owner-verified for NetworkBoost]**
- `Mod/NetworkBoost.lua:28-35`: `d.Clean` runs every player × every city × (1,032 B055 + 90 B058 + 4 test) carrier IDs, each with `P.Info` + `HasBuilding`.
- `:158-164`: any `CityTransfered`, with no owner filter, runs a full Clean.
- The B055 catalog is a hard runtime dependency: `row(id)` asserts `B055_DATABASE_MISSING` (`:19,31,167`), so the 928,526-byte `NetworkBoost.sql` cannot be shrunk without code changes.
- `Mod/StandardizationDiscount.lua:275-281`: every `CityTransfered` resets `applied` and presence-checks every enabled carrier × 4 levels for every non-test city. Those carriers are generated from `HD_BuildingTiers`, so the count grows with HD and other mods (UNKNOWN; DB unreadable).
- Per-turn foreign reconciliation:
  - `CommerceConvergence.lua:14` reads facts before `IsTestPlayer`, so it throws once per AI city per audit (SD-08).
  - `ResearchInfrastructure.lua:84` still checks 52 retired or bit carriers per foreign city.
  - `HalfYieldProbe.lua:31-46,75` sweeps the world on every player's turn without dedupe.
- B133 per-conquest increments of 220k/351k/278k building checks (B129 report, another agent's transcription) are consistent with transfer sweeps dominating conquests.

**Counterevidence**
- Sweeps run only at init and on transfer. B139 recorded no obvious stutter (user report).
- Newer writers filter to the test player first (`ResearchApply.lua:84` and others), and Architecture `:111` forbids new world-scan defaults.
- Architecture `:115` deliberately keeps conservative foreign-turn reconciliation.

**Remediation boundary**
- Per-writer bounded foreign-cleanup candidate sets: test-player capitals, Store registered/loss/target cities, and an applied index.
- Scope `CityTransfered` cleanup to the transferred city.
- Run one legacy sweep per save, recorded in a flag.
- Move `IsTestPlayer` ahead of `facts()` (SD-08).

Narrowing Architecture `:115` is a contract change. The save-compatibility window for B055 rows is **DDR**.

**Regression risk.** MEDIUM: a missed stale carrier gives a wrong Boost or Discount, so prove candidate completeness with fixtures.

### AF-06 Event scope and invalidation are too coarse — HIGH / FBDF

**Slices.** A3-03, A3-06, A3-07 (lowered to LOW), A3-08, A5-13, and verifier-missed items.

**Facts**
- `Mod/RuntimeWork.lua:30-32,59-81`: `Hook` narrows only a few events. Every other event calls `fn()` at full world scope.
- `CommerceConvergence.lua:168` hooks CityProductionCompleted, CityTileOwnershipChanged, Government/Research/Civic events through `Hook`, so each foreign event runs a world audit.
- `IndustrySupport.lua:79` and five other modules do the same for improvement, feature and DistrictBuildProgressChanged events.
- Raw GameEvents binds pass native arguments as `scope` (full scope) in six modules.
- `Mod/Probe.lua:552-554`: every `CreateBuilding`, `RemoveBuilding` and `SetProperty` (including Store writes) bumps the single `ExposedMembers.SPC_RuntimeUIRevision`.
  - Seven consumers recompute on it.
  - `CommerceConvergence.lua:159-166` runs an unscoped world audit when it moves.
  - `UI/IndustryRefresh.lua:45` filters native SPC events to avoid self-triggering, then marks dirty on the global counter at `:12-13`, which defeats that filter.
- `DistrictCompleteness.lua:180-187` invalidates every D entry on any player's district or transfer event and on `GameEvents.BuildingConstructed`.
- Whether a Lua `CreateBuilding` raises `BuildingConstructed` is UNKNOWN natively. If it does, every carrier write fans out into world audits.
- Base-game UI uses owner-first signatures for these events (`TutorialUIRoot.lua:1919,1995,2206,2359`; `Automation_ObserverCamera.lua:647`).

**Inference (LOW–MEDIUM on attribution).** Commerce world audits driven by foreign events and revision bumps are the most plausible main source of the 527k–708k building checks per turn observed at T40–45 (B129 report). Structurally (HIGH), each new module hooking these events or reading the global counter adds another world sweep per foreign event.

**Counterevidence**
- D2 deliberately did not guess signatures (`Batch_D2_Runtime_Propagation.md:34`); Architecture `:111` allows narrowing only by verified native arguments.
- Commerce does not loop on its own writes.
- Over-invalidation fails safe.

**Remediation boundary**
- One event-normalization table (event → owner/city extractor, evidence citation, full-scope fallback), shared by `Hook`, D invalidation and the UI producers.
- Keyed revisions (player/city/output kind) instead of the scalar counter, Commerce first.
- Move the route signal out of the diagnostic probe.

The evidence standard for a "verified" signature is a contract decision.

**Regression risk.** MEDIUM-LOW per event if the fallback is kept.

### AF-07 Building-presence checks scale with the whole Buildings catalog — HIGH / FBDF

**Slices.** A3-04, A3-11.

**Facts**
- `OrdinaryBuildingCatalog.lua:238-255` admits every `GameInfo.Buildings` row, including internal SPC rows. `DistrictCompleteness.lua:83-89,107-126` checks each row with `HasBuilding` + `P.Count` on every capture.
- The D cache is an LRU of at most 8 entries with a deep clone on every read (`:151-169`).
- `GreatWorkFacts.lua:31-52` checks every Buildings row per city, recollected on every local turn and every transfer (`UI/DialogueRefresh.lua:136-137`).
- There are at least 1,729 static `BUILDING_SPC_*` rows, plus four generated rows per HD-tier building.
- Retired carriers are re-checked on every audit, forever: 48 in `ResearchInfrastructure.lua:6-10`, 12 in `SpecialistSupport.lua:5-20` retired by three separate owners, and the Lv3/Lv4 Culture withdrawals on every `CultureAesthetic` reconcile.
- Tests assert only the cache-size bound, never the hit rate above 8 cities.
- Architecture `:73` records that the full-Buildings-scale cost is still open.

**Inference.** With 9 or more D-needing cities swept per turn, the LRU hit rate approaches 0% (HIGH, static). Roughly 150–250k checks per turn at about 20 specialized cities (LOW–MEDIUM). Every new carrier family slows every capture in every city.

**Counterevidence.** B170 deliberately kept full presence checks to preserve UNKNOWN/unreviewed-building semantics. At T40, D was not the dominant cost (3–7 rebuilds per turn).

**Remediation boundary**
- Restrict D presence to D-domain rows plus unreviewed non-internal rows. Bound the Great Work collector to `Building_GreatWorks` rows.
- Size or memoize the cache per (pid, cid, turn, epoch). Invalidate D by owner and city.
- One retirement owner with a session "retired-clean" mark.

Reversing B170's conservative stance is a contract change.

**Regression risk.** MEDIUM: D feeds five or more writers, so reuse the B170 value-by-value comparison.

### AF-24 Allocation-heavy helpers; the GC trial is the only late-game backstop — MEDIUM / FBDF (helpers), MONITOR (GC)

**Slices.** A3-09, A3-10.

**Facts**
- `Probe.lua:99-117`: `P.Field` allocates a closure per call, and `P.Call`/`P.Info` build on it.
- `IsTestPlayer` is unmemoized (315 call sites in 97 files, per the slice).
- `PerformanceCounters.lua:14-24` calls `Game.GetCurrentGameTurn()` on every counter increment, including inside `HasBuilding` loops.
- Deep clones on every fact read: `EffectiveFacts.lua:6,46`; `DistrictCompleteness.lua:167-169`.
- The GC trial disables itself for the session after any collection over 2 s (`PerformanceCounters.lua:115,144-146,193`). The B139 T42 collection was exactly at that threshold (1,041 MiB heap; B129 report).

**Inference.** Late-game heaps approach the lock-out, after which nothing mitigates allocation volume, and nothing tells the user.

**Counterevidence.** The engine's incremental GC still runs. A non-mod late save also grows (B129 report).

**Remediation.** Closure-free `P.Field` (`pcall(get,o,k)`); memoize successful `IsTestPlayer` results only; cache the turn in `Count`; show a visible state after lock-out. The primary fix is reducing volume (AF-05/06/07). GC cadence is a user decision (B138).

**Regression risk.** LOW for helpers.

### AF-25 Instrumentation blind spots and performance-evidence gap — LOW / FBDF (prerequisite for validating AF-05/06/07)

**Slices.** A3-12, A3-13, A3-14.

**Facts**
- `PerformanceCounters.lua:64-72` omits real event names (Improvement/Feature/DistrictAdded, `BuildingConstructed`) but labels the non-firing `OnBuildingConstructed`, and silently drops unlabelled keys.
- Dispatch attribution covers only `RuntimeWork` hooks and stops after 6 turns (`:82`).
- `UI/RuntimeAudit.lua:19-21` needs `io.open`, which was natively unavailable (B072 result).
- Counters are inflated by failed foreign reads and by world probes.
- There is no per-Audit time measurement and no evidence for T>62, more than 13 cities, wartime churn, or turn wall time.

**Remediation.** Complete the labels; per-Audit `os.clock` accumulation under fixed keys; context tags; an arm list for probes; one bounded late-game benchmark (its definition is a user decision) plus local fixtures with about 20 own and about 200 foreign cities.

---

## 4. Native integration

### AF-03 Gameplay authority depends on UI-context closures hosted in a shared ProductionPanel replacement — HIGH / FBDF

**Slices.** A4-02, A1-10, A5-04, E2-03, E2-10, verifier-missed reader-budget and exporter-lifetime items.

**Facts**
- Gameplay synchronously calls functions exported by UI contexts through `ExposedMembers`:
  - `ExpeditionTraining.lua:22-29` ("GetAt is a UI surface")
  - `DialogueProjects.lua:20,50,146-157` — a completion-sample failure writes a permanent `Hold` at `:155`
  - `ClaimProjects.lua:20-29` (fallback)
  - `TimedProject.lua:105-107`
  - `ProjectTurnObservation.lua:24,74`
- All four exporters (`UI/ExpeditionTrainingUI.lua:15`, `UI/ClaimProjectUI.lua:30`, `UI/DialogueProjectUI.lua:27`, `UI/ProjectTurnRead.lua:5`) are constructed only inside `UI/CrewProjectOrder.lua:44-76`, the ProductionPanel replacement.
  - It has no `SetShutdown` and never clears the exports.
  - Adapter construction is not pcall-isolated.
  - `GetDataHelper` calls four adapters with no pcall (`:13-19`).
  - `SPC_ProjectTurnRead` is installed twice; `P0Panel.lua:610` wins last.
- `ExpeditionTraining.lua:141-148` counts 12 publish events without a reader and then persists HELD with capacity reserved. This is an event count, not a readiness handshake.
- `ExposedMembers.SPC_P0` is the whole Gameplay `shared` table (`Gameplay.lua:8-9`), and UIs read module internals directly (`UI/DialogueRefresh.lua:24-38`, `UI/BoostRefresh.lua:8-11`).

**Inference (structure HIGH; native ordering UNKNOWN).** A transient UI problem (a late, shadowed or erroring ProductionPanel, or a cold-load ordering race) becomes a durable Gameplay hold: a Claim timer stops, a Dialogue reward is held, or Expedition capacity is held. Every production-queue ability adds another tenant and another exporter in the same single-winner context.

**Counterevidence**
- The pattern is partly forced by the API (`OverflowStorageProbe.lua:15-18`: `GetSize` is UI-only), and HD uses it too.
- Returned values are validated fail-closed.
- B202 rows 1–2 show native training working (another agent's record).

**Remediation boundary**
- A dedicated UI native-read bridge context that publishes a readiness epoch, clears itself on shutdown, and returns READER_ABSENT versus READ_FAILED.
- Per-adapter pcall and a declared adapter order.
- Publish small read-only views instead of internals.
- Prefer native Gameplay facts where they exist.

Whether an outage becomes a hold or a deferral is **DDR**.

**Regression risk.** MEDIUM, because these paths carry persisted state.

### AF-04 Native panel replacements are hard-wired to HD private files; no declared HD dependency or LoadOrder policy — HIGH / FBDF

**Slices.** A4-01, A4-04, A4-06, A5-14, X-04, verifier-missed reparenting and composed-DB test items.

**Facts**
- There are 7 `ReplaceUIScript` contexts (`Mod/SpecializationP0.modinfo:14-16,30,32,33,357-362`). Each includes exactly one named HD file (`UI/ExpeditionSpyUnitPanel.lua:2` → `DL_UnitPanel`, `UI/TimedProjectCityPanel.lua:2` → `DL_CityPanel`, `UI/TimedTurnProbe.lua:2` → `HD_ActionPanel`, `UI/CrewProjectOrder.lua:2` → `DL_ProductionPanel`). Only `InstitutionOverview.lua:3-6` has a fallback.
- ProductionPanel is at LoadOrder 150100, only 100 above HD's 150000.
- `modinfo:618-621` declares only Rise and Fall and Gathering Storm as dependencies. HD is undeclared.
- Gameplay code asserts on HD's UI-published helpers (`ConstructionProbe.lua:17-18`; `UnitTargets.lua:43-44`).
- Controls are reparented across contexts by hard-coded paths (`UI/UnitPanelActions.lua:88-89`, `UI/Institutions.lua:22-30`, `UI/CityPotential.lua:24-26`, `UI/P0Panel.lua:316-317`).
- SQL LoadOrder has no policy. `Data/Lv2Housing.sql` (LoadOrder 1200) selects HD/JNR rows that HD defines at 12000 (`<Workshop289070>/2465378070/DL.modinfo:1511-1514`), so that table is dead (SD-12).
- `DevelopmentTests/test_lv2_housing.py:84-90` runs the SQL against the *already composed* DB, so ordering errors are undetectable by construction.
- `Data/StandardizationDiscount.sql:3-8` joins HD-private tables without guards.
- `tools/generate_boost.py:20-22` writes HD-private keys.

**Inference (MEDIUM-HIGH, HD-cadence dependent).** A Workshop update, which arrives outside the user's deployment cadence, can disable unit actions, End Turn, the city panel or the production panel game-wide (HD features included), and through AF-03 turn into durable Gameplay holds.

**Counterevidence**
- B196 recorded USER_GAME_TEST_PASS for the replaced chain with the installed HD.
- The recorded HD manifest SHA matches the installed `DL.modinfo`.
- `U1_Presentation_Prototype.md:17` explicitly accepts the HD dependency.
- The wrappers include rather than copy native files.
- The "Better Espionage Screen adds unguarded entry points" sub-claim was REFUTED.

**Remediation boundary**
- Decide whether HD (and District Expansion HD, Workshop 2701747165) are declared dependencies. This is a scope decision.
- After each include, assert the required symbols and fall back to the vanilla chain (the InstitutionOverview pattern).
- A read-only compatibility check for include targets, wrapped symbols and the HD fingerprint.
- A documented SQL LoadOrder band policy, with a manifest check that compares each SQL file's LoadOrder against the rows it selects.
- Retire `TimedTurnProbe` (SD-03).

**Regression risk.** LOW for guards and checks.

### AF-18 Cross-context bridges, transport and concurrency scaffolding are bespoke per feature — MEDIUM / FBDF (adopt for new work; DEFER migration)

**Slices.** A4-03, A4-05, A1-08, A1-13, A5-12, E2-11.

**Facts**
- Every UI-mediated bridge has its own pending/ack/retry/timeout logic: `UI/ExpeditionSpyActivity.lua:252-262` (10 s → FAILED → HELD), `UI/ExpeditionTrainingName.lua:105-118`, `SampleLifecycle.lua:69-78`, plus bespoke clients in `UI/DiscountEligibility.lua`, `UI/DialogueRefresh.lua`, `UI/GPPRefresh.lua` and `UI/BoostRefresh.lua`.
- Near-copies of the Audit scheduler have drifted in reentrancy semantics: `CultureMeaning.lua:166-169` drains under pcall, `CultureInspiration.lua:155-157` and `DialogueEffects.lua:175-177` do not (SD-17), and `CultureAesthetic.lua:141-142` drops rather than coalesces.
- Nine files implement their own last-turn dedupe, while `RuntimeWork.Hook` serves 14.
- Request ingress obligations (`RequestDepth`) are hand-copied (`Gameplay.lua:677`; `ExpeditionSpyGate.lua:541-543`; `ExpeditionTraining.lua:48-51`).

**Inference.** Each consumer copies about 40 lines of scheduler code plus bindings, and fixes such as B154 must be repeated in every copy. Each new UI-mediated ability re-invents pending/ack/timeout, and diagnosing stalls costs native sessions.

**Counterevidence.** Copies keep modules independently reviewable. Independence limits failure spread (`SampleLifecycle.lua:53`).

**Remediation boundary.** Shared helpers, adopted first by the next new consumer:
- a `CityReconciler` (scope merge, busy/pending, drain under pcall)
- an ingress helper (depth guard, pcall, per-channel token-keyed reply, explicit BUSY reply)
- a bridge primitive (lease/ack/retry/timeout/terminal mapping)
- `SampleLifecycle.Client` as the default transport

Which bridge failures become holds is **DDR**.

**Regression risk.** MEDIUM per migration.

### AF-19 Carrier ownership is peer-to-peer exclusion lists; building-event reentrancy is per module — MEDIUM / FBDF

**Slices.** A1-07, A5-08 (part), A5 verifier-missed.

**Facts**
- Exact-ID peer exclusion lists differ: `CultureMeaning.lua:205-207` names 4 peers; `CultureAesthetic.lua:211` names a different 3; `CultureMeaningProbe.lua:490` names 2.
- Adding one ability (94c964b) edited two peers' lists.
- Five live `CityBuildingsChanged` subscribers use three different self-guard styles.
- Four modules subscribe to `GameEvents.OnBuildingConstructed`, a name with 0 uses in base-game and HD Lua, while the real `BuildingConstructed` has 20 (SD-09).

**Remediation.** A shared owned-carrier registry populated at Start (keeping exact-ID semantics), with a test that every registered carrier is excluded by every building-event consumer. Split the invalidation counter (AF-06).

**Regression risk.** MEDIUM: the Culture writers have native PASS evidence.

---

## 5. Shared mechanisms and technical debt

### AF-08 Retirement and cutover have no single contract; retired modules remain load-bearing — HIGH / FBDF

**Slices.** A5-08, A1-09, A7-08.

**Facts**
- The Great Work sample producer depends on retired Dialogue: `UI/DialogueRefresh.lua:24-30` requires `s.Dialogue` and its seq for ACK, and `Gameplay.lua:308-341` sends each sample to both `GreatWorkFacts.Receive` and the retired `Dialogue.Receive`. The latter still parses the payload, scans every city and forwards to the retired GWAdjacency (`Dialogue.lua:298-326`).
- Retired Dialogue still carries the live governor path to DialogueEffects (`Dialogue.lua:125,356-362`; `Gameplay.lua:504`).
- Live writers assert on or call retired modules: `CultureInspiration.lua:7,67,208`; `CultureMeaning.lua:8,205`, which has no nil guard.
- At least eight retirement mechanisms are in use: Start option, flag after Start, request remapping, never-included files, nil-ed slots, UsesNewAuthority/BlocksLegacy, tombstone Start, and an early return.
- `D0032_Implementation_Plan.md:133-134` requires "a single versioned feature" selector and keeps old Type IDs "until cleanup is complete", with no end defined.

**Inference (high).** No retired module can be removed without editing live writers. A naive removal of Dialogue silently stops the Great Work input for every Culture ability. Each pending cutover (M, H, N3, P, J) will invent another mechanism.

**Counterevidence**
- Exact-ID withdrawal is deliberate save-compatibility safety.
- Reusing the old transport was accepted.
- A missed sibling filter costs extra audits, not wrong yields.

**Remediation boundary**
- One retirement contract: a RetiredFacade (exact IDs + Withdraw, registered via the Store exit registry, no live listeners), retired through the Start option.
- Before removing Dialogue, move its live duties (governor dispatch → DialogueEffects; sample transport, generation and ACK → GreatWorkFacts).
- A test-checked retirement table.

The sunset window is **DDR**.

**Regression risk.** MEDIUM: the transport move touches the path behind the Culture native PASS.

### AF-11 Module role and lifecycle are unclassified; probe-named modules carry production duties — MEDIUM / FBDF (prerequisite for any cleanup)

**Slices.** A5-01 (lowered from HIGH/FIX_NOW), A5-02, A1-11, A1-12, A3-12, A5-17.

**Facts**
- Production authorities carry probe names:
  - `EffectiveFacts.lua:15` → `CityFlowProbe.SupportFacts`
  - `CityProgressionStore.lua:1110` asserts `shared.BindingProbe`
  - `UnitActions.lua:24,126` → `ConstructionProbe.ReadSnapshot`
  - `TradeRouteProbe.lua:6,130,134` owns `RouteSignalRevision`, consumed by `NetworkBridge.lua:133,204`, `NetworkSender.lua:30` and `UI/BackgroundRoutes.lua`, while its header says "NEVER a GAMEPLAY_CURRENT provider".
- Consumers read `(shared.RouteSignalRevision or 0)`, so pruning the probe would make staleness undetectable (SD-10).
- Save-visible production identifiers carry DEV or probe names: `DEV-B013-P..` tokens, `SPC_DEV_BINDING_B013_TOKEN`, `BUILDING_SPC_MEANING_PROBE_*`, and properties from `Data/GovernorProbe.sql`.
- Dormant experiments start on every load with world-scope listeners (e.g. `HalfYieldProbe.lua:31-46,76-77`).
- DEV cheats remain wired to the request handler behind hidden buttons (`P0Panel.xml`; `Gameplay.lua:487`).
- About 1.4k shipped Lua lines are never included.
- `Runtime_Index.json` has no role field.

**Counterevidence**
- Architecture `:38`, `:445` already warn that names are not roles, and `:107` declines per-module manifests.
- Experiment exits are pcall-isolated.
- Cheats are confined to the local test player.
- Corrections: ConstructionProbe, TradeRouteProbe and TimedProject are *reachable*, so a removal list based on A5-02's "dormant" set would break production.

**Remediation boundary**
- The lightest step: a role/lifecycle field in the existing `Runtime_Index.json` (PRODUCTION / PRODUCTION_LIBRARY / DIAGNOSTIC_LIVE / EXPERIMENT_DORMANT / RETIRED_FACADE / TOMBSTONE_DATA / DEAD_SHIPPED) plus a test that every file has one. This is a user decision given Architecture `:107`.
- Later, extract production parts into neutrally named modules while keeping every save-visible ID.

Which DEV controls stay in playtest builds is a user decision.

**Regression risk.** None for classification; MEDIUM for extraction.

---

## 6. Design ↔ Architecture ↔ implementation consistency

### AF-17 No Design↔runtime conformance register; parameters hand-copied; confirmed drift — MEDIUM / FBDF (before P0-V and balance tuning)

**Slices.** A7-01 (lowered from HIGH), A7-02, A7-09, A7-12, A7-13, A1-14.

**Facts**
- Only 4 of 24 v0.1 ability IDs appear in Mod (as comments), and none in DevelopmentTests.
- `Specialization/Workflow/context.py:79` rejects any manifest whose `authority_versions` differ from Authority's. Those include `status` and `runtime` (`Authority.json:13-14`), so every manifest goes stale on any Status bump, and staleness carries no per-ability Design-drift signal.
- `P0-F1.json`/`P0-F2.json` select `Research_D0031 RES_L4_TRADITION` and are COMPLETE while Research authority is D0040. The code still sets the absorbing `OWNER_POLICY_UNRESOLVED` (SD-02).
- A single parameter source is specified (`D0032_Adaptation.md:97`) but absent. The Inspiration rate of 3 per era lives in four places: `Culture_D0049.json:371-376`, `CultureInspirationModel.lua:2`, hand-written `Data/CultureInspiration.sql:5-35`, and a test.
- Carrier capacity is sized from current Design maxima (`ResearchApply.lua:6` "M.Bits=5 -- max current Gold coefficient30"), and overflow is detected only at runtime (`:45`).
- The Architecture composition map has no Expedition row (`Specialization_v0.1_Architecture.md:36-49`), and its B174 claim (`:87`) is contradicted by SD-01.

**Counterevidence**
- Manifests give point-in-time traceability (`context.py:61-69`).
- Status records a sync note per Design revision.
- Runtime `validate()` catches SQL/Lua mismatches.
- REFUTED framing: Design `implementation_status` fields are frozen metadata, not a stale tracker.

**Remediation boundary**
- A Workflow-owned, machine-checked conformance register. Each ability row records: current Design pointer + hash, the hash the code implemented, writer modules, carrier families, tests, latest result, sanctioned deviations, and a state (NOT_STARTED / LEGACY_ACTIVE / PARTIAL / CONFORMANT / DRIFTED).
- Per-ability drift detection in `context.py`.
- Per-profession parameter modules with generated SQL and a carrier-capacity check against Design maxima.

Where conformance lives is a user governance decision.

**Regression risk.** None for runtime.

---

## 7. Testing and evidence

### AF-09 Test harness: one Lua state for all contexts, per-file mocks, synchronous single-slot events — HIGH / FBDF

**Slices.** A6-01, A6-02, A6-03, A6-07, A6 verifier-missed.

**Facts**
- `DevelopmentTests/test_expedition_spy_gate.py:11-12,80-81,105-109`: one LuaRuntime loads the Gameplay Store and Gate and then the UI Reader, and `include` is a no-op.
- `:84-87` installs UI-only off-map Spy APIs on a `Players[2]` that the Gameplay Gate also sees, contradicting `:54-55`.
- The mocked `UI.RequestPlayerOperation` calls Gameplay synchronously (`test_expedition_training_ui.py:84`).
- Recorded native failures after local PASS in this class (other agents' records): B025 (UI API in Gameplay), B064 (`table.unpack`, Lua 5.1 vs 5.x), B077 (manufactured `GetDistricts().Members()`), B182 (UI-only `IsCapital`).
- Tests run on Lupa `lua55` (`DevelopmentTests/README.md:8,18`), while 45 files use the default `lupa` import. Only two files sandbox 5.2+ library members. The base game uses 5.1 idioms (`Civ6Common.lua:758`).
- Event handling in the mocks:
  - Many mocks are single-slot (`test_expedition_training.py:10`): `Add` overwrites earlier listeners, so co-subscribed Gameplay and UI handlers of the same native event cannot both run (SD-15).
  - Multi-listener mocks dispatch in `pairs()` order.
  - `SetUpdate`/`SetInitHandler` are captured and invoked by hand (`test_expedition_training_ui.py:77,85,88`).
- B201, B202 and B203 each passed UI event/timing behaviour locally and then failed or stalled natively (other agents' records; native root cause UNKNOWN).

**Inference.** The per-context API surface lives implicitly in about 83 per-file mocks, and nothing makes an unknown API fail by default. "Handler registered" is modelled as "handler runs, in the test's order".

**Counterevidence**
- Deliberate API poisoning exists (`test_expedition_spy_gate.py:33,93-96`).
- B204 builds adverse cases per test (init withheld, frames withheld).
- No current assertion is shown to be wrong.
- Lua 5.5 strictness yields false failures more than false passes.

**Remediation boundary**
- Per-context runtimes (or sandboxed `_ENV` with no `_G` fallback) that share only `ExposedMembers` and a deferred operation queue.
- A curated per-context API allowlist with provenance, where unknown APIs error.
- A 5.1-profile runtime factory.
- A shared native-mock module with multi-listener events in registration order, deferred dispatch, and lifecycle profiles (init or frames delivered, delayed or withheld).
- A minimal adverse-profile matrix per UI observer.

**Regression risk.** Test-only; porting will surface latent assumptions noisily.

### AF-20 Executed test closure is not versioned; manifest-listed regressions lapsed unnoticed — MEDIUM / FIX_NOW

**Slices.** A6-04 (QUALIFIED HIGH/FIX_NOW by its verifier), A6-11, A6-15. The consolidation rated it HIGH for evidence integrity. The report owner rates it MEDIUM, because the 478 count is not inflated and no false PASS is demonstrated; the fix is cheap.

**Facts [owner-verified]**
- All 32 test files referenced by `Specialization/Workflow/P0-N1.json` are Git-tracked.
- The executable closure behind "478 targeted tests PASS" exists only in the ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B204/local/run_targeted.py` (`.gitignore:23`).
- `Specialization_B204_Expedition_Event_First_Local.md:23` names no module for its increment.
- `Batch.schema.json:16` requires `validation` but gives it no structure.
- Seven manifest-listed test files (170 methods) are outside the executed closure:
  - `test_expedition_gate` is an intentional frozen fixture provider.
  - `test_expedition_spy_name` (39 tests of Gameplay NAME-authority negatives), `..._activity_diagnostic` (21) and `..._activity_failure` (16) were last executed at B194. B202–B204 changed name confirmation in 8 commits since then. `P0-N1.json:220,230` still calls the latter two "Direct … regression".
  - `test_p0_panel_current_layout`, `test_unit_panel_action_layout` and `test_native_icon_aliases` are the other three.
- The static `def test_` sum over the 25 runner modules equals 478 exactly. The count is consistent, not inflated.

**Inference.** "Prior closure plus N" reads as cumulative but is not monotone (B194 276 → B196 145 → … → B201 383). Reviewers cannot reproduce a PASS from Git alone.

**Remediation boundary**
- A machine-readable closure in the manifest or a committed sidecar: modules, command, backend, DB requirement, and EXCLUDED entries with a reason.
- A committed generic runner.
- Counts reported as "N tests / closure id (hash) / K excluded".
- Run and classify the six non-frozen excluded files once.

Schema changes need user approval under W0005.

### AF-21 Cross-ability regression is structurally discouraged — MEDIUM / FBDF

**Slices.** A6-05, A6-08, A6-10, A6-13, A5-16.

**Facts**
- Literal version stamps mean historical package suites fail on every bump. `test_expedition_spy_gate.py:284` asserts `'231'` *before* the package invariants at `:285-290` (SD-14 neighbourhood).
- 85 of 262 test files use `exec(compile(...))`. `test_b058_boost_gw_basis.py:7-12` mutates another test's source.
- The six other suites that load `UI/CrewProjectOrder.lua` were not in the B202–B204 closures and carry stale stamps, although B202 added hooks to that shared file.
- There is no Mod-module→test reverse index.

**Remediation.** A generated reverse index: when a shared module changes, its consumer suites must be in the closure or recorded as NOT_RUN with a reason. Consistency invariants instead of literal stamps. Contract tests tying stubs to real readers. Editing frozen tests needs user policy.

### AF-22 Evidence environment is non-hermetic; save/load is simulated inside one VM — MEDIUM / FBDF

**Slices.** A6-06, A6-09, A6-12, A6 verifier-missed.

**Facts**
- The B204 runner hard-codes the live game-cache `DebugGameplay.sqlite`, which already contains deployed SPC rows (`test_expedition_spy_gate.py:262-275` deletes SPC rows from an in-memory copy). `SHA256.json` does not hash the DB.
- Lupa environments live in `/tmp` paths that have disappeared before (B182, B202 NOT_RUN).
- `project_paths.py:11,14` raise `RuntimeError` (reported as ERROR, not skip).
- Persistence tests `restart()` inside the same VM with a deep-copied property table (`test_expedition_spy_persistence.py:18-21`).
- Mock `P.SetProperty`/`CreateBuilding` drop the real `SPC_RuntimeUIRevision` side effect, so the UI cache-invalidation path (`UI/ExpeditionTrainingUI.lua:30-33`) is never exercised.

**Counterevidence**
- The DB is opened read-only and copied into memory.
- NOT_RUN is reported honestly.
- A native travelling-team cold load was USER_GAME_TEST_PASS within scope (B201, another agent's record).

**Remediation.** Record DB SHA256 and HD version plus a "doctor" output in each bundle; a pinned repo-local venv recipe; a clean base+HD DB baseline (needs a user game launch with SPC disabled); `skipTest` with a NOT_RUN tag; a shared `cold_load()` helper with 5.1-safe serialization and fresh per-context runtimes; wrap the real Probe helpers.

---

## Concrete standalone defects

These are not structural, but each has a specific failure scenario. All are STATIC_CONFIRMED; native frequency is UNKNOWN unless stated.

| ID | Defect | Sev / Timing | Failure scenario and evidence |
|---|---|---|---|
| SD-01 | **CrewPrecision decorator drops `UnitActions.Run`'s investment evidence** [owner-verified] | MEDIUM / FIX_NOW | `Mod/CrewPrecision.lua:22-46` returns only `result`, while `UnitActions.lua:159-161` returns `output,investment`. Start order is `Gameplay.lua:792-799`. `Gameplay.lua:490` receives `nil`, so `refreshInvestmentSupport` (`:21-37`) never takes the B174 scoped path and never calls `DialogueProjects.Refresh` after a normal Settler investment. The Dialogue entry for that city stays stale until another trigger. Every Settler confirm also writes a `CrewPrecision` error record and prints a B046 line. This contradicts Architecture `:87`. The B174 LOCAL_SIMULATION_PASS used a composition without CrewPrecision (`test_investment_update_propagation.py:112-113`). |
| SD-02 | **Academic Tradition still applies an absorbing `OWNER_POLICY_UNRESOLVED` on capture** | MEDIUM / FBDF (implementation authorization) | `CityProgressionStore.lua:617` sets it on loss; `ResearchTradition.lua:27` makes it absorbing; the return path never touches it. `Research_D0040.json:329` says "Follow city; unsupported owner freezes age/effect". A second terminal path: ticks skip non-ACTIVE cities, so recapture after more than one turn gives `UNKNOWN_INTERVAL` (`:29-30`). Tests assert the old behaviour (`test_b143_tradition.py:70-72`; `test_b144_tradition_effects.py:68`); P0-F1/F2 are COMPLETE against D0031. The A7 verifier judged D0040 to settle the rule. Because `Research_D0040.json:331` also carries a `closed` note mentioning `OWNER_POLICY_UNRESOLVED`, the user or Primary should confirm the reading before changing the code; escalate if ambiguous. |
| SD-03 | **TimedTurnProbe replaces HD's ActionPanel although nothing can arm it** [owner-verified: no sender] | MEDIUM / FIX_NOW (removal needs user authorization) | `modinfo:32`; `UI/TimedTurnProbe.lua:284` only subscribes, and the trigger was removed in 5f8f02f (B120). Every End Turn click, Enter press and hotkey goes through prototype overrides (`:203-213`, `:290-291`) that consume unshifted Enter KeyUp. Behaviour is equivalent today, but HD changes to End Turn handling are silently shadowed. |
| SD-04 | **Legacy Dialogue retirement fails open on partial startup** [owner-verified] | MEDIUM path / low likelihood / FBDF | `shared.Dialogue.retired=true` is set at `Gameplay.lua:877`, after five unguarded Starts (`:842-851`). If one throws, Gameplay stops and Dialogue has no retired default (`Dialogue.lua:5`), so its live governor hooks and `Receive` run the old dynamic carrier writer. GWAdjacency and the Inspiration probe retire through the Start option and fail closed. |
| SD-05 | **Overflow-sink test project buildable by every player** | LOW–MEDIUM / FBDF | `Data/OverflowSinkTest.sql:1-4` has no RequiredBuilding gate: a 1,000,000-cost, no-reward project appears in every city's production list. AI choice is UNKNOWN. |
| SD-06 | **One unresolvable district event permanently holds every not-yet-specialized city** [owner-verified] | MEDIUM / FBDF | `CityProgressionStore.lua:1151-1155` → `HoldCompletion` on every worker → `completionError` persisted on every UNASSIGNED ACTIVE record (`:319-321`). It is never cleared, and `active()` fails (`:148`), so those cities can never specialize and feed AF-14 at cold load. |
| SD-07 | **Unsupported acquisition breaks network capture at every cold load** [owner-verified code path] | MEDIUM / FBDF (DDR) | A Free City conquest, cession or loyalty-transferred city is not admitted (`CityProgressionStore.lua:1039,1066`; `P0_E2_Plan.md:834`). Its facts raise `FOUNDATION_EVIDENCE_PENDING`, so `NetworkInput.lua:38-41` fails `Capture` and Boost, Convergence and Lv3 Commerce withdraw empire-wide (AF-14). Untested. |
| SD-08 | **Commerce reads facts before the test-player check** | LOW–MEDIUM / FBDF | `CommerceConvergence.lua:14`: each world audit throws once per AI or city-state city inside pcall, records an error string per city and still pays about 96 presence checks. Reordering changes no semantics. |
| SD-09 | **Four modules subscribe to a non-firing event name** | LOW / FBDF | `Lv3Effects.lua:136`, `Lv3Support.lua:90`, `IndustrySupport.lua:80` and `CommerceConvergence.lua:169` subscribe to `GameEvents.OnBuildingConstructed`, which has 0 uses in base and HD Lua; the real name `BuildingConstructed` has 20. Building completion is picked up only through other hooks or the next turn. Whether the engine defines the name is UNKNOWN. |
| SD-10 | **Route staleness fails open if TradeRouteProbe is pruned** | LOW (trap) | `(shared.RouteSignalRevision or 0)` in `NetworkBridge.lua:133,204` and `NetworkSender.lua:30`. |
| SD-11 | **Clean rejections reported as uncertain HELD** | LOW | `UnitActions.lua:141,156` substring-match `HELD` before checking `destructive`. A `PROGRESSION_HELD` rejection is shown to the player as "结果尚未确认，请停止重试" (result unconfirmed, stop retrying). |
| SD-12 | **Lv2Housing tier table built before its HD rows exist** | LOW | LoadOrder 1200 vs HD 12000; the table is dead at runtime, and its test runs on the composed DB. |
| SD-13 | **Duplicate modinfo action id `SPC_B059_Dialogue`** | LOW (native effect UNKNOWN) | `SpecializationP0.modinfo:396-397`. |
| SD-14 | **Version assertion masks package invariants; Spy Gate load handler never exercised** | LOW–MEDIUM | `test_expedition_spy_gate.py:284` vs `:285-290`. `ExpeditionSpyGate.lua:576-578` registers `LoadScreenClose` only if the event exists, and no fixture invokes it. |
| SD-15 | **Single-slot event mock hides Training's load and publish handlers** | MEDIUM (test gap) | In `naming()` fixtures, `UI/ExpeditionTrainingName.lua:152` overwrites `ExpeditionTraining.lua:142,152`, so a Training load-recovery regression passes B204's wake-up tests (`test_expedition_training_name_events.py:39`). |
| SD-16 | **Stale Claim session key after a second loss** | LOW | `ClaimProjects.lua:206` clears `key(loss.origin)`, while the live ID after recapture is `root.current.cityID`. |
| SD-17 | **Drain without pcall can stick** | LOW (latent) | `CultureInspiration.lua:155-157`, `DialogueEffects.lua:175-177`: an escaping error leaves `draining=true` until reload. |
| SD-18 | **GC idle guard misses DialogueProjects and Expedition busy states** | LOW | `PerformanceCounters.lua:147-158`; `DialogueProjects.IsBusy` has no caller. Effect: a GC pause only. |

## Strengths worth preserving

- **Store exit/return registry.** Deterministic order, at most 3 attempts, per-module error isolation, exact-ID removal with readback, no prefix scans (`CityProgressionStore.lua:513-550`).
- **Store write path.** Validates before every write (`:165-169`); holds per city in production (`:806`); reads back even after a throwing setter.
- **`ExpeditionSpyStore` envelope.** CAS and validated readback are the authority; a writer exception is inconclusive; ABSENT/OLD/OTHER outcomes are classified (`:94-147`).
- **Write-ahead intent and no replay of uncertain native actions** (Investment, Claim, Expedition CREATE/END/DISPATCH/RESERVE).
- **Saved facts separated from derived state.** ACTIVE is re-derived from the governor; carriers are rebuilt, not replayed; UNKNOWN is never coerced to 0 (`CurrentSpecializationFacts.lua:3-8`; `NetworkInput.lua:33-41`).
- **Reusable templates for future consolidation:**
  - `GreatWorkFacts.RegisterConsumer`: per-consumer pending, epoch revalidation, failure isolation.
  - `RuntimeWork.Hook` and batch-scoped fact index.
  - `SampleLifecycle`: epoch/seq/ACK, single flight, UNCHANGED dedupe.
- **Idle discipline (D1/D2).** O(1) dirty-gated publish handlers, confirmed natively in B076 (scoped).
- **Newer modules scope by test player and city** (`ResearchApply.lua:84`, `CultureAesthetic.lua:145`, and others). Architecture `:111` forbids new world-scan defaults.
- **Clean module structure.** No include cycles; pure model modules (ResearchApply/Chair/Cross, CultureInspiration/Aesthetic, DialogueProject) with no engine references.
- **Fail-closed runtime self-validation** of SQL carriers (`CultureInspiration.lua:14-34`; `ResearchApply.lua:11-21`).
- **Context separation.** UI never writes game state; all mutation goes through `EXECUTE_SCRIPT`.
- **A central single-player/local-human gate** (`Probe.lua:36-49`).
- **Native panels are include-and-wrap, never copied.** City banners use the Firaxis wildcard include.
- **Engineering hygiene.** Generator `--check` drift tests, hash-verified deployment, dense fault injection in Expedition tests, forbidden-API poisoning, and disciplined LOCAL_SIMULATION_PASS / USER_GAME_TEST vocabulary throughout Status.

## DESIGN_DECISION_REQUIRED and user decisions surfaced (not decided here)

**Gameplay or save semantics (DDR)**
1. Store failure granularity and placement of new per-city ledgers (AF-01, AF-16).
2. Which effects must refresh synchronously after investment or unit actions (AF-02).
3. A uniform hold-resolution policy: a user-confirmed abandon that never grants, or "load an earlier save" only (AF-12; Expedition-specific variants in [Expedition_Review.md](Expedition_Review.md)).
4. Late return acceptance and inferred loss on load (AF-13).
5. Partial-network semantics and the per-ability hold/withdraw mapping, including whether unsupported acquisitions should disable national network effects (AF-14, SD-07).
6. Catalog drift handling for learned templates (AF-23).
7. Refounding and city-ID reuse semantics (AF-26).
8. Outage policy when a UI reader is absent: defer or hold (AF-03, AF-18).
9. Save-compatibility window for retired carriers, B055 rows and superseded unit types (AF-05, AF-08).
10. Release identity and participation scope: test civilization versus general rule set; HD as a declared dependency (AF-04, AF-28).
11. Which DEV and prototype controls stay in playtest builds (AF-11, SD-03, SD-05).

**Architecture and governance (user approval, not gameplay)**
12. Narrow shared primitives within the "no generic engine/bus" constraints (Architecture `:65`, `:87`, `:107`; D0032 `:25`): cause/consumer table, owned-carrier registry, 1T primitive, bridge primitive, CheckedRecord.
13. A role/lifecycle field in `Runtime_Index.json` (AF-11).
14. A conformance register location and per-ability drift detection (AF-17).
15. Contract changes: narrowing Architecture `:115` foreign reconciliation, relaxing B170 full presence, a drain-scoped facts snapshot (Architecture `:112`), and the evidence standard for verified native event signatures (`:111`).
16. A machine-readable test closure in batch manifests, and the policy for frozen historical tests (AF-20, AF-21).

## Unreviewed areas and UNKNOWNs

- **Native semantics that static review cannot settle:**
  - listener dispatch order
  - whether Lua `CreateBuilding` raises `BuildingConstructed`
  - whether `OnBuildingConstructed` exists in the engine
  - ExposedMembers lifetime across in-game loads
  - SetUpdate delivery to hidden contexts
  - equal-LoadOrder tie-breaks
  - duplicate action-id handling
  - city-ID reuse
  - `canceled` semantics on CityProductionCompleted
  - native property serialization limits
  - engine cost of about 1.7k internal buildings
  - save growth
- **Not read in depth:** business logic of the individual yield writers; NetworkBridge, BackgroundRoutes and NetworkSender internals; most UI (about 5.4k lines); the CityInheritance, InheritanceShadow and CityIdentityExperiment internals; `tools/` beyond the deploy and generator heads; most of the 262 test files; the Military, Harbor and Government Design bodies.
- **Not checked:** the user's enabled mod set (Mods.sqlite was not read); DB-derived carrier counts (no configured DB path); the HD version string.
- **Process notes.**
  - Two subagents disclosed creating small temporary files in the session scratch directory (outside the repository) while diffing lists, contrary to their no-write instruction. No repository, game, Workshop or protected file was modified.
  - One listing printed two `Reports/Audit/` filenames; neither was opened in Phase A.
