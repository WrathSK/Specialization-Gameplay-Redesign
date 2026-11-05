# Independent audit of the v3-final convergence candidate (Option B)

Advisory / Non-authoritative / No design decision implied
Status: Stable
Maintainer: Claude, Advisor session (attribution, not session authorization)
Written: 2026-11-03
Scope: Read-only independent audit requested by the user through `Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/External_Audit_Package.md`, with the user's stated goal: pay down as much technical debt as possible inside Option B and avoid later rework. Covers the package's nine falsification groups, the formal-sync texts (FS01-FS12) and the plan's sequencing. Excludes implementation, tests, probes, deployment, game launch, Design/Architecture/Status edits and gameplay decisions.
Basis: develop `954dc67` = origin/develop, tracked tree clean; production bytes identical to the v3 source baseline `9addf8d` (only reports added since). Formal D0058 / A0183 / S0866; runtime record B399.426 (not re-verified). Nothing was executed.
Companion: [evidence, worklist and per-group results](Independent_Audit_v3_Final_Evidence.md). Bracketed IDs below (G1-1, G4-2 …) point to its rows.

## How to read this report

| Label | Meaning |
|---|---|
| STATIC_CONFIRMED | Read in code or formal text at `954dc67`. Says nothing about native behaviour. |
| LOCAL / USER_NATIVE (existing) | Recorded earlier results, cited within their named scope, not rerun. |
| UNVERIFIED | Needs a runtime or native fact; a minimal verification is given. |
| DESIGN_DECISION_REQUIRED | Changes player-visible semantics or an accepted rule, so it is yours to decide. |

Severity: **Critical** = wrong irreversible outcome or unimplementable without changing approved gameplay; **High** = structural gap likely to force rework or wrong player-visible behaviour; **Medium** = missing gate or inventory that would be caught later at moderate cost; **Low** = clarity.

Method in one paragraph: seven read-only sub-audits (G1-G7), at most two at a time, each writing notes incrementally; G8 and G9 read directly. Every finding at High or above, and every fact used in section II, was re-read by the Advisor at the cited lines. Rows marked "as reported" in the companion were not re-read.

## I. Verdict

**The direction holds; the plan is not yet implementable without rework.** No Critical finding. The two Owner choices (ODP-01=B, ODP-02=A) fit the code: a K-only projection can be written with the existing carriers and no new SQL, the three network formulas are monotone so K-only is a valid lower bound, signed capital contracts settle on stored terms, durable receipts protect all six irreversible operations so re-delivery cannot re-execute money or units, and the approved formulas (eight collection eras, Wonder without N/E/L, Cross without D) are intact. The B396 pre-U5 transport items are fixed.

Six High findings would each be discovered during O1-O7 and force rework if the plan is synced and implemented as written:

1. **A01** The NET rules have a seam in the *normal* cold case, where the candidate's own D1-E5 gate forbids the result its NET05 produces. Needs your confirmation (OD-1).
2. **A02** No not-ready cause has a named completion trigger. Several recover today only through the per-turn Bridge refresh and owner turn audits, which the candidate bans as recovery and O8 plans to prune. Needs a one-line confirmation (OD-3).
3. **A03** "D1 retirement" has no deliverable; the weakened gate D1-E6 passes with nothing removed.
4. **A04** The candidate's description of current behaviour (T0) is wrong per family, so U5 and D1-E5 baselines are wrong.
5. **A15** Crew grants fail more broadly than G14 states: one ambiguous grant blocks that project type in every city.
6. **A18** The P3 ledger misses production startup prerequisites inside DEV/diagnostic files; removing them by name would skip almost every profession.

Count: 0 Critical, 6 High, 4 Medium-High, 9 Medium, 1 Low group (20 findings).

## II. Decisions for you (batched, with recommended defaults)

| # | Question | Options | Recommendation |
|---|---|---|---|
| **OD-1** (A01) | After a normal load, source A is confirmed gone and source B is only waiting for the first route proof or its role read. What does the receiving city get until B is ready? | **(a)** Only the provable part, labelled partial, rising again when B is ready. **(b)** Keep the whole installed value until B is ready (a normal-case exception A, which B otherwise withdraws). | **(a)**: it follows NET05 without a special case, matches "protect independently provable sources, do not pay unprovable ones", and leaves no extra branch to retire. The drop normally lasts until the first proof of that turn. D1-E5 must then accept it as a deliberate change. |
| **OD-2** (A07) | A city leaves Commerce while its reputation record is temporarily unreadable. Design resets reputation to 0 on Identity exit; SAFE-004 says a temporarily unreadable record must not be overwritten. | **(a)** Apply the reset anyway (it does not depend on the old value) and keep the error visible. **(b)** Record a deferred identity-exit duty, applied when readable (extends A0183:19's loss/return-only approval). **(c)** Block restructuring while the record is isolated. | **(a)**: the reset is the lawful transition and exit erases the history by rule, so there is nothing to protect. (b) adds persistent machinery; (c) adds a new gameplay gate. Same for the capital protection reset. |
| **OD-3** (A02) | Where no native event exists to complete a recovery (Governor ACTIVE UNKNOWN, source not yet admitted to the Store, D re-capture), may the local turn start drain **only the registered pending items**? | Yes, as a bounded lifecycle boundary / No: find a native event per cause, or keep the hold for these causes. | **Yes**: it is not a whole-city scan, every pending cause gets a bound, and it lets D1 and the generic per-turn refresh actually be removed. |
| **OD-4** (A06) | Does the save-scope rule of 2026-10-16 (only games started with the current build; no compatibility code; a new persisted shape means a new campaign) apply to Option B? | Yes / No: Option B must also support older saves or older builds. | **Yes**: then the LEGACY contract path, the undefined "compatibility gate" and the kept NetworkRecoveryStore decoder are unnecessary; shape-changing packages simply start a new campaign. |

Everything else is a plan correction Primary can make without a gameplay decision.

## III. Findings

Each finding gives the counterexample, current formal versus target, sources, affected candidate IDs, recommendation and, where useful, the minimal verification.

### A01 — NET01/NET05 seam in the normal cold case (High; Owner OD-1) [G1-1, G2-2]

- **Counterexample.** Receiver R gets Standardization from self (10) and sources A and B (20). On load, A's Industry identity is confirmed exited; B's role read or the first route proof is not yet available (normal, not a fault); no session witness W exists. NET01 keeps applied output and sends no UNKNOWN to professions (Fact contract `:28,:32`); NET05 processes the confirmed exit first and recomputes from K/W without the inseparable residual (`:36`); FS04 ¶3 and ¶5 (`Formal_Authority_Sync_Delta.md:56,:60`) do not say which wins. Following NET05, R drops to 10 until B is ready; Commerce falls to self-only Gold; Culture to the union of reliable remote sets. Exception A (`Specialization/Design/Network.md:57`) covered exactly this case with "keep 20".
- **Gap.** No rule labels the normal-case result as partial; D1-E5 (`Option_B_Final_Candidate_Plan.md:126`) accepts behaviour change only for severe errors; the only worked example (`Owner_Gate_Stop_Report.md:26-28`) is a severe fault and is labelled an engineering interpretation.
- **Affected.** NET01, NET05, FS03, FS04, D1-E3/E5, F29/F32/F45, O3.
- **Recommendation.** Decide OD-1; write the normal-case output and label into NET05 and FS04; amend D1-E5.
- **Minimal verification.** LOCAL fixture of this scenario per family, T0 and target.

### A02 — No completion trigger per not-ready cause; recovery depends on banned per-turn work (High; Owner OD-3) [G1-2, G1-5, G5-5, G5-6]

- **Counterexample.** A source city's Governor ACTIVE reads UNKNOWN after load, or the city is not yet admitted to the Store (`Mod/Commerce.lua:225-227`, `Mod/CultureNetwork.lua:148`). NetworkInput marks it MIXED; the only bounded recovery today is the Bridge's per-turn `Refresh` on `PlayerTurnActivated` (`Mod/NetworkBridge.lua:925-930`) plus owner turn audits. The candidate forbids "TTL／定时器／逐回合全城扫" as recovery and O8 plans to prune these paths; R2's same-value recovery assumes publishers that do not exist for ACTIVE and D. One rejected proof packet also blocks every proof send for the rest of the turn (`Mod/NetworkSender.lua:25-28,44`).
- **Gap.** D1-E1 lists create/expire/reestablish/cold/signal-only but not MIXED role facts; no row names the event or boundary that completes each cause; "登记待完成责任" has no bound, so it is functionally a central hold. An unclassifiable persistent not-ready has no prescribed output (L-03).
- **Affected.** NET01, D1-E1/E2/E6, F28/F46, PU03, PU10, O1, O2, O3, O8, G02, G06, G08.
- **Recommendation.** Before O2/O3 freeze, add a table: cause → completing event or boundary → bound → what the carrier shows meanwhile. Use OD-3 where no native event exists. Make the removal of the per-turn refresh and owner turn audits conditional on each consumer having passed O2 retention and a named wake. Put `failedTurn` into PU03 or O3.
- **Minimal verification.** LOCAL fixture per cause showing completion without turn audits; one native observation of cold first-proof order only if local cannot answer.

### A03 — D1 retirement has no deliverable; D1-E6 was weakened (High) [G3-1, G3-2, G3-6, G3-7, G1-3]

- **Counterexample.** v3 required "旧D1分支/模块/import真实不存在" (v3 plan `:68`); v3-final requires only "如有可撤者真不存在" (`Option_B_Final_Candidate_Plan.md:127`) and calls kept output natural continuity (`:130`). Consumers also run on non-network triggers while topology is pending (`Mod/FactConsumerBindings.lua:39-43` and consumer hooks), where NET01/NET05 still demand "do not write, keep O, apply confirmed negatives". So almost every D1 branch survives as NET01 handling: E6 passes with nothing removed and E5 passes by construction. The Bridge already holds centrally (`negativeHeld`/`dormant`, `queuedWork`, the prune continuity view, `Mod/NetworkBridge.lua:215-262`), and none of it is inventoried.
- **What is actually retirable.** The Bridge's pending fan-out to effect consumers (`Mod/NetworkBridge.lua:103-111`) and the exception-A pieces in Standardization (`Mod/StandardizationEffects.lua:197` `old.loaded` term, `:206`). Standardization also needs a **new** rule to apply a reliable own-city increase while topology is pending (forbidden today, `:194-196`; required by D1-E4/F32).
- **Other gaps.** Deletion is placed in both O3 and O8; E7's native evidence plus O8's exit imply two native rounds; the only fallback is "Gate失败就不删", i.e. permanent D1 with no recorded scope. The three-arm "keep / disable / remove" differential cannot be built: D1 branches are local closures with no switch, and "disable" has no defined meaning.
- **Recommendation.** In O3, a disposition table for every D1 branch and Bridge central hold (retire / keep as NET01 / convert to NETxx); deletion owned by O3; replace the three-arm test with keep-versus-target using the existing historical-source pattern (`DevelopmentTests/test_refactor_s9e6.py:13-22`); record an explicit scope if anything must stay.

### A04 — The candidate's T0 is wrong per family, so baselines are wrong (High) [G2-1, G2-1a, G2-5, G2-6]

- **Facts.** With topology VERIFIED and one source unreadable at cold, Commerce already writes K-only Gold labelled RETAINED (`Mod/Commerce.lua:244-279,356`) and CultureNetwork writes K-only n (`Mod/CultureNetwork.lua:157-165,249-270`). Standardization holds the cold aggregate on **any** reason, including non-blocking warnings (a learned template no longer in the catalog, a district ledger not yet established: `Mod/StandardizationEffects.lua:138-146,181,206`) and stays frozen (`:244`) while confirmed removals and reliable self gains are ignored. One Commerce domain with no readable source holds the whole city (`Mod/Commerce.lua:274,338-339`).
- **Consequence.** The candidate's T0 ("cold whole hold", `Gap_Matrix_v3.md:55`; Fact contract `:15`) and D1-E5's "same behaviour" baseline do not describe the code; Commerce and Culture already depart from the formal cold-aggregate hold (`Specialization/Design/Network.md:55`; A0183:145).
- **Recommendation.** Re-derive the T0 table per family before U5 and record these as known T0 deviations instead of fixing them pre-U5 (a fix toward the old formal rule would be undone by O3). Put the Standardization warning freeze and per-domain / per-target independence into O3's explicit scope.

### A05 — The Bridge drops unknown-role sources silently (Medium-High) [G2-3]

- A never-confirmed source is published as `specialization='UNKNOWN'`, `potential=0`, with an unread `roleUnknown` flag (`Mod/NetworkInput.lua:97-102`); `derive` admits only known professions with potential ≥1 (`Mod/NetworkBridge.lua:531-536`); `effectAvailability` becomes AVAILABLE from route freshness while `input.pending` only affects transaction availability (`:371-374`). Consumers compute K-only and label it fully confirmed. This contradicts the formal "保留／未知状态不得冒充全新确认" today and blocks NET03/NET04 labelling after O3.
- **Recommendation.** Name it in O3/FS03: unknown-role sources stay visible as UNKNOWN in effect views, and `input.pending` reaches effect availability.

### A06 — Save-compatibility promises contradict the accepted save scope (Medium-High; Owner OD-4) [G8-5, G3-4, G4-7, G4-8]

- **Facts.** Playtest_Workflow (user decision 2026-10-16): only games started with the current build are supported; "no compatibility, migration or protection code is added" for older saves; a new persisted shape requires a new campaign; U5 always uses a new campaign (`Specialization/Architecture/Playtest_Workflow.md:29,45-48`). The candidate requires LEGACY settlement of old contracts, "向后可读和旧版本安全运行须在相容门禁证明", and keeping the NetworkRecoveryStore decoder, opaque evidence and SQL IDs "至相容性门禁". The gate is never defined. The derived-save adapter was never wired, so a kept decoder protects nothing.
- **Recommendation.** Apply the save-scope rule (OD-4): drop LEGACY/compat paths; delete NetworkRecoveryModel/Cell/Store and `Store.NetworkRecoveryStamp` in O7 together with tests s9g1-s9g4 that assert their packaging and the static alarm justified by A0183:18; record per package whether the persisted shape changes; group shape-changing packages so a new campaign is started once. Keep SQL IDs only where production uses them.

### A07 — Identity exit during reputation-leaf isolation skips the Design reset (Medium-High; Owner OD-2) [G4-1]

- **Counterexample.** The reputation leaf is isolated at load (transient CHECK_UNKNOWN). The player restructures the Commerce city away: `commerceMerge` copies the isolated reputation back unchanged (`Mod/CityProgressionStore.lua:117-123,742-743`) and the protection reset is skipped (`:745`); no deferred duty is recorded. After a later load the leaf validates; when the city becomes Commerce again, re-establishment sees an existing reputation and does not restart it (`:678`), and `TickCommerce` continues the pre-exit age (`:541-551`). Commercialization Gold and VENTURE refunds are over-credited; Design requires R0 on Identity exit (`Specialization/Design/Content/Shared_D0058.json:114`).
- **Affected.** FS05, FS06, PU06, O4; not in G01-G30.
- **Recommendation.** Decide OD-2 and implement it in PU06 (same code).
- **Minimal verification.** LOCAL fixture: isolated leaf → restructuring exit → reload with readable leaf → Commerce re-established.

### A08 — Formal sync: location lists incomplete, withdrawal timing too late (Medium) [L-01, G3-3, G4-9]

- FS03/FS04 omit current formal carriers of the rules they replace: Spec NET-005 (`Specialization/Design/Specialization_v0.1_Design_Spec.md:283`) and SCOPE-001 (`:16`), `Shared_D0058.json` `cold_load_exception_A` (line 81) and line 352, the `pending_network_rule` copies in Commerce/Culture/Industry Content and Industry `pending_fact_policy`. FS06 omits the Commerce Spec/Content/Design-page carriers of the reputation and capital rules. The formal text is also inconsistent today: Network.md:57 and NET-005 state exception A generally, A0183:145 and Shared:81 limit it to Standardization.
- Formal records still schedule the withdrawn S9 cold adapter integration before U5 (Status CURRENT `Specialization/Status/Specialization_P0_Status.md:20`; `Specialization/Status/Validation/Results/Specialization_B399_Network_Project_Coverage_Reconciliation.md:24,45`; `Specialization/Reports/Proposals/Refactor_Recovery_Persistence_Proposal.md:84`), while FS04 removes it only "before O3". Primary following the formal record would either build withdrawn work or be blocked at U5.
- **Recommendation.** Give each FS an exhaustive, grep-based location inventory, and move the parts that withdraw obligations (S9 cold wiring, exception A as a target, compatibility promises) into the first formal sync, before Pre-U5.

### A09 — Delivery (O2): unsized owner retention, more silent drops, listeners that must stay (Medium) [G1-4, G5-2, G5-3, G5-4, G5-7, G5-8]

- PU03 names no wake: nothing re-arms the Bridge after a failed `EmitDerived` (`Mod/NetworkBridge.lua:135-142`); `proofPending` and the Bridge's `consumerError` are never read.
- Silent drops missing from O2's tests: FAILED/SKIPPED targets skip their rows and *clear* their error (`Mod/FactConsumerBindings.lua:6-9,76,119`); not-ready returns are ignored; error slots are overwritten by the next success; owner flushes clear their queue before running.
- Owner retention needs changes in `SPCRuntimeWork.NewAudit` (13 owners) and four owner flushes; phase0 consumers can only ACK synchronously; moving work out of the drain loses the shared read cache. GreatWorkFacts already ACKs only on callback success, an in-repo precedent R2 never cites.
- The Governor listeners in DialogueProjects and EngineeringStudyProjects are unique (ordered per-event audits; DialogueProjects' only owner-wide route, `Mod/DialogueProjects.lua:313-320`, `Mod/FactConsumerBindings.lua:87-92`); O5 folding or O8 pruning could remove them.
- R3 constraints: the EmitDerived window keys on the literal name `'NetworkBridge'`; phase0 order is registration order, so self-declaration in startup order would invert Bridge and Restructuring; tickets must be minted per callback because EmitDerived merges in-flight rows into the owner-wide key. FS08 does not restate P06's budgets or say whether it amends or replaces A0183 P03/P06.
- **Recommendation.** Size O2 against these, add the drops to O2's LOCAL list, add the listeners to an explicit keep list, and state phase0 order explicitly.

### A10 — FS09 would open fail-closed exit gates (Medium-High) [G5-1]

- LegacyCleanup registers its Store exit *before* Start so that a failed owner can never remove the mandatory exit gate (`Mod/Gameplay.lua:853-858`); the Store runs each exit up to three times and holds failure as PARTIAL_HELD (`Mod/CityProgressionStore.lua:1268-1287`). FS09's "失败启动不得残留半订阅" read literally removes such registrations on failure, so a city loss would proceed without mandatory cleanup.
- **Recommendation.** FS09/O5 distinguish mandatory fail-closed gates (exit/return registries, LegacyCleanup, GreatWorkFacts consumers) from ordinary subscriptions.

### A11 — Capital/Commerce mechanisms missing for ODP-02=A (Medium) [G4-2, G4-3, G4-4, G4-5]

- VENTURE contracts are already signed on an unmarked R=0 from an isolated leaf (`Mod/CapitalInvestment.lua:183`; `Mod/CapitalInvestmentModel.lua:144`). The numbers match A; provenance is missing; the `or 0` must go rather than remain a fallback.
- R_POLICY_ZERO vs R_UNSAFE is not mapped to the Store's actual states: CHECK_FAILED, CHECK_UNKNOWN (runtime or missing-dependency) and DEFERRED_LIFECYCLE share the leaf bucket, and `ValidateReputation` cross-checks parent fields (`Mod/CommerceModel.lua:45-50`), so a leaf/parent mismatch is booked as a leaf fault while the parent validates alone (`Mod/CityProgressionStore.lua:1125-1141`).
- The shared quote cannot express "refuse VENTURE, allow STABLE": an integer R is asserted for both modes (`Mod/CapitalInvestmentModel.lua:137`) and `canSign` is per domain (`Mod/CapitalInvestment.lua:188`).
- CREDIT_INTENT/CREDIT_CALLING are missing from the signing guard (`Mod/CapitalInvestment.lua:141`), so another domain of the same city can be signed while a credit outcome is unknown, until reconcile turns it HELD (`:246-247`). The candidate names this only as an unproven possibility.
- **Recommendation.** PU06: provenance in quote and contract (frozen as final so O4 does not touch it again), the Store status exposed in `CommerceState` with an explicit mapping, mode-specific signing, CREDIT_* in the guard.

### A12 — Write failures zero the output; partial has no representation (Medium) [G2-4, G2-7, G2-8]

- Commerce clears all Gold after a failed apply (`Mod/Commerce.lua:360-365`); CultureNetwork clears after a failed mutating write (`Mod/CultureNetwork.lua:274-276`). NET06 forbids mechanical zero writes; O3 does not list these lines.
- No FULL_UNKNOWN / APPLIED_PARTIAL representation exists (RETAINED covers NET01-NET03), and Capital's network gate checks the Commerce stage string `READY` (`Mod/CapitalInvestment.lua:147`), so O3's labels must be co-designed with that gate. Partial status lives only in the session: a saved K-only output reloads looking complete. `Finish` asserts every effective row has a source (`Mod/CommerceCalculation.lua:36`).
- **Recommendation.** Add all of these to O3's explicit scope.

### A13 — Plan structure invites double implementation (Medium) [L-05, G4-7]

- PU01 permits a temporary same-ref protection that O1 replaces; PU03 splits watermarks that O2 re-plumbs; PU06 adds provenance that O4 relists. **Recommendation:** each PU is built as the first slice of its O package (same interfaces and field names), so O packages extend instead of redo.

### A14 — Native testing is not batched (Medium) [L-04, G3-2]

- Every PU and most O packages carry their own USER_NATIVE line, plus U5 and the final acceptance; D1 alone implies two rounds. This exceeds your recorded preference (batched decisions, 2-3 short smokes, one final acceptance). **Recommendation:** fix the touchpoints in section V.

### A15 — Crew (施工队) grants are fragile beyond G14 (High) [G6-1, G6-2, G6-3]

- **Counterexample 1 (new).** In city A a grant's native outcome is ambiguous (`InitUnit` returns nil, or the binding readback fails): the per-player, per-ProjectType receipt stays CALLING (`Mod/CrewProjects.lua:272,282-291`). From then on every completion of that type in **any** city fails `CREW_PREVIOUS_GRANT_UNRESOLVED` (`:277`) and the production is spent without a unit, while other cities can still queue and pay because admission only checks receipts from their own source (`:160,:231`).
- **Counterexample 2 (G14, recorded LOCAL).** Two cities complete the same Crew project in one turn; the player-wide counter jumps by 2; the strict check `native==prior+1` (`:278`) fails both; zero units; the failed city's formation is blocked (`:158,:163`) until city exit clears it (`:387-395`).
- **Gap.** PU05 asks for a unique completion proof but says nothing about receipt keying or the end state of orders already HELD (SAFE-004: permanent HELD is not a normal end; SAFE-002: no grant without proof).
- **Recommendation.** PU05: a unique per-completion witness (candidate: `CityProductionCompleted`, already used in production code; needs the native check), receipts keyed per completion, an unresolved grant blocking only its own order, and a defined end for ambiguous grants (prefer a confirmed-absence check; escalate only if no lawful end exists).
- **Minimal native check (session N0).** Two cities complete one same-type Crew order in the same turn: log the raw arguments of `CityProjectCompleted` and `CityProductionCompleted`, the counter and each queue; remove a queued Crew project at 0 and >0 progress.

### A16 — UNKNOWN can cancel Claim and Dialogue rounds (Medium) [G6-4, G6-5]

- Claim and Dialogue remove the project's access marker (its RequiredBuilding) whenever the state read fails (`Mod/ClaimProjects.lua:39-47`; `Mod/DialogueProjects.lua:89-96`). If the engine then drops the queued project (UNVERIFIED), UNKNOWN cancels a round, contrary to SAFE-001 and A0182 D4. Engineering Study already keeps the marker on UNKNOWN (`Mod/EngineeringStudyProjects.lua:72-74`). Claim CALLING has no recovery. If `CityProjectCompleted` fires on project removal (UNVERIFIED), switching away from a Claim would commit a permanent specialization.
- **Recommendation.** PU09: copy Engineering Study's marker rule to Claim and Dialogue; define Claim CALLING recovery; answer both native questions in session N0.

### A17 — Lifecycle holds reach further than G11/G28 say (Medium) [G6-7, G6-8]

- One unresolvable `OnDistrictConstructed` holds every fresh unassigned city of the player, and `completionError` is never cleared (G11). `recapture()` requires all registered exits (about 45, including optional probe exits) to have finished, exits run only in the foreign window and their state is session-only, so one unfinished exit leaves the record HELD_TRANSFER permanently; exit retry is "once per turn, three times", a retry-count recovery the candidate forbids elsewhere (G28).
- **Recommendation.** PU07/PU08 state this reach and decide which exits are mandatory for recapture; optional diagnostic exits must not gate a production return.

### A18 — The P3 ledger misses production prerequisites inside DEV/diagnostic files (High) [G7-1, G7-2, G7-3, G7-4, G7-5, G7-8]

- **DEV probe chain.** CityFlowProbe's Start includes FreshBindingHook ("B020 DEV copy") and calls `Install` unguarded (`Mod/CityFlowProbe.lua:60`; `Mod/Gameplay.lua:874`); `Install` asserts `DEV_ONLY` context and that `shared.OnFreshCityBinding`, `shared.CityJournalProbe` and `shared.BindingProbe` exist (`Mod/FreshBindingHook.lua:5-8`), provided by CityJournalProbe ("B015 DEV submission experiment", `Mod/CityJournalProbe.lua:1,85`) and BindingProbe ("B013 DEV-only"). EffectiveFacts depends on CityFlowProbe (`Mod/Gameplay.lua:876`) and nearly every profession on EffectiveFacts. No Q row owns this chain.
- **Read-only diagnostic as dependency.** UnitTargets depends on UnitSiteProbe ("read-only Gameplay location diagnostics") (`Mod/Gameplay.lua:908-910`; `Mod/UnitSiteProbe.lua:1`); its absence skips UnitTargets, UnitActions, PlayerActionReplies and CrewPrecision (`:912-918`).
- **Counters at load time.** Probe.lua includes PerformanceCounters and binds `P.Count`/`P.Observe` to it (`Mod/Probe.lua:553-555`); without it Probe.lua stops before defining `P.HasBuilding` and the production write barrier `factWrite` (`:556-569`); about 150 unguarded `P.Count` call sites follow (as reported).
- **Trace factories and error classification.** Built unguarded at Start in about ten production modules and one UI file (only Bridge and IndustryWonderEffects are named); CultureNetwork and Capital derive HELD reasons through diagnostic modules (`Mod/CultureNetwork.lua:368`; `Mod/CapitalInvestment.lua:15-18`); PurchaseProbe performs production cleanup on every LoadScreenClose and BoostRefresh waits on `GreatWorkProbe.ready` (as reported).
- **Formal.** A0183's ownership table lists CityFlowProbe and Probe as production entries (`Specialization/Architecture/Specialization_v0.1_Architecture.md:73-75`); FS10's location list omits it.
- **Recommendation.** Complete the Q ledger with these rows before O1/O2 "提前提取"; adopt the existing tested optional-observer pattern (`Mod/Gameplay.lua:1-8`, B394) as the target; add a static alarm for unguarded diagnostic-global reads; rename or annotate misleading "DEV/Probe/read-only" headers so nobody removes production code by name.

### A19 — GC extraction facts and the true-absence harness are not specified (Medium) [G7-6, G7-7, G7-9]

- `M.Flight` ignores the counters' `enabled` flag while `Count` honours it (`Mod/PerformanceCounters.lua:16-30`); the GC idle gate reads `ExposedMembers.SPC_Performance.inflight` (`:213-214`), so removing the counters object (`Mod/Gameplay.lua:24`) lets GC run during an in-flight NETWORK_PUSH, contrary to A0183:632. NETWORK_INFLIGHT gets one same-turn retry while ROUTES_PENDING does not; the negative-heap latch is module-local; GC tests inject `SPC_Performance` themselves and would stay green after such a removal.
- The harness reads module files straight from disk with no modinfo VFS or absent set, and the whole-startup fixture stubs the trace factory, so "缺file+global" cannot be tested (as reported). Test-named SQL used by production cleanup/UI and the duplicated `SPC_B059_Dialogue` component are not inventoried.
- **Recommendation.** O7 states the GC facts as invariants with a dedicated test that does not inject counters; PU11/O7 size a harness layer (modinfo-driven include with an absent set, real Starts with native doubles, multi-context ExposedMembers, harness-level restricted profile, outcome comparison); inventory test-named SQL. Whether native `include()` throws on a missing file is UNVERIFIED (answer in session N2).

### A20 — Smaller items (Low)

- FS05 removes SAFE-004's narrow "proven permanent loss → lawful baseline" permission (consistent with DEC06C) without stating the end state of a permanently corrupted ability; say "explicitly blocked with error" so O4 does not decide it [L-06].
- B396's "one mid-game sample" for workload is not carried; include one larger save in the final acceptance [B396 cross-check].
- The stable deploy tool writes no persistent receipt; "receipt记删除" needs an artefact or a Status record [G8-4].
- More than 128 routes or a payload above 16384 bytes produce a persistent hold no NET row covers [G3 adjacent].
- Formal `quote_lock` asks for a quote/state version that contracts do not carry [G4-7].

## IV. Plan corrections before formal sync (for Primary)

1. **NET rules** (A01, A05, A12): normal-case output and label per OD-1 in NET05/FS04; unknown-role visibility and `input.pending` in effect views; no mechanical zero on write failure; a partial representation co-designed with Capital's gate.
2. **Completion triggers** (A02): per-cause table; OD-3 for causes without a native event; removal of per-turn refresh and turn audits conditional on O2 retention plus named wake; `failedTurn` repaired.
3. **D1** (A03, A04): per-family T0 table; disposition table for every D1 branch and Bridge central hold; deletion owned by O3; two-arm keep-versus-target differential; deliberate rewrite list for about 60 test functions in 14 files, two of which assert exception A directly, using the `test_refactor_s9e6.py` historical-source mechanism.
4. **Save scope** (A06): per OD-4, drop LEGACY/compat code and the compatibility gate; delete the derived adapter in O7; a per-package "persisted shape changes?" column.
5. **PU scope** (A07, A11, A15, A16, A17): PU05 receipt keying and ambiguous-grant end; PU06 provenance (final), status mapping, mode split, CREDIT guard, identity-exit reset per OD-2; PU09 marker rule and Claim CALLING; PU07/PU08 reach.
6. **Formal sync** (A08): exhaustive location inventories; withdrawals in the first sync, before Pre-U5.
7. **O2/O5** (A09, A10): sizing, silent-drop tests, unique-listener keep list, explicit phase0 order, fail-closed gates exempt from "no half subscription".
8. **P3/O7** (A18, A19): completed Q ledger; optional-observer target pattern; static alarm; GC invariants test; absence harness; SQL inventory.
9. **Structure** (A13, A14): each PU as the first slice of its O package; native touchpoints as in section V.

Severe or structural changes from items 1-3 and 8 merit a short re-audit of the revised NET matrix, D1 table and Q ledger before implementation, as the package itself requires for major findings.

## V. Proposed native touchpoints (matches your recorded preference)

| Touchpoint | When | What it answers |
|---|---|---|
| N0 evidence smoke | Before implementing PU05/PU09 | Two cities complete one same-type Crew order in one turn; remove queued Crew and Claim projects at 0 and >0 progress; raw `CityProjectCompleted` / `CityProductionCompleted` arguments; whether removing a RequiredBuilding drops a queued project; cold first-proof order. Collector on, 3-5 turns, listed actions. |
| U5 | After Pre-U5 | Migration baseline on a new campaign (already planned). |
| N2 | After O3+O4 | Network partial/negative behaviour, reputation/contract provenance on a new campaign (shape change); one build with an optional observer file deliberately absent to settle native `include()` behaviour before O7 deletes anything. |
| Final | After O7+O8 | Convergence acceptance, including deletions shipped through both deployment tools and one mid-game save. |

Everything else is LOCAL.

## VI. Technical-debt ledger for Option B

Items Option B would have to reopen that the candidate does not list, or lists only in principle.

| Item | Where | Package | In candidate? |
|---|---|---|---|
| Standardization warning-triggered cold freeze | `Mod/StandardizationEffects.lua:138-146,181,206` | O3 | No |
| Per-domain / per-target independence; Standardization self increase while pending | `Mod/Commerce.lua:274`; `Mod/StandardizationEffects.lua:114-154,194-204` | O3 | Principle only (F32) |
| Bridge drops unknown-role sources; `effectAvailability` ignores `input.pending` | `Mod/NetworkInput.lua:97-102`; `Mod/NetworkBridge.lua:371-374,531-536` | O3/FS03 | No |
| Write failure zeroes output | `Mod/Commerce.lua:360-365`; `Mod/CultureNetwork.lua:274-276` | O3 | No |
| `failedTurn` blocks proof sends for the rest of a turn | `Mod/NetworkSender.lua:25-28,44` | PU03/O3 | No |
| Bridge central holds (`negativeHeld`/`dormant`/`queuedWork`/prune view) | `Mod/NetworkBridge.lua:215-262` | O3 | No |
| Over-limit routes/payload hold | `Mod/NetworkSender.lua:53,59` | O3 | No |
| Dead code: `withdraw()`/CONFIRMED_INVALID branches, `proofPending`, Bridge `consumerError`, `roleUnknown`, CultureMeaningProbe Bindings row, unused includes/imports | Bridge, Culture, Standardization, Bindings, Gameplay | O3/O7 | No |
| Identity-exit reset skipped during leaf isolation | `Mod/CityProgressionStore.lua:117-123,742-745` | PU06 | No |
| CREDIT_* missing from signing guard; mode-specific signing; R provenance and status mapping | `Mod/CapitalInvestment.lua:141,183,188`; `Mod/CapitalInvestmentModel.lua:137` | PU06 | Partly |
| Silent delivery drops; owner retention in NewAudit and four flushes | `Mod/FactConsumerBindings.lua:6-9,76,111-119`; RuntimeWork | O2 | Partly |
| Unique Governor listeners | `Mod/DialogueProjects.lua:313-320`; EngineeringStudyProjects | O5/O8 keep list | No |
| Mandatory fail-closed exit gates vs FS09 | `Mod/Gameplay.lua:853-858`; `Mod/CityProgressionStore.lua:1268-1287` | O5/FS09 | No |
| Crew receipts per player+type; ambiguous-grant end | `Mod/CrewProjects.lua:160,231,272-291` | PU05 | Proof only |
| Claim/Dialogue access marker removed on UNKNOWN; Claim CALLING terminal | `Mod/ClaimProjects.lua:39-47`; `Mod/DialogueProjects.lua:89-96` | PU09 | No |
| Recapture needs all ~45 exits; optional exits gate production; retry-count exit recovery | CityProgressionStore recapture/exit paths | PU08/O7 | No |
| G11 reach across unassigned cities | CityProgressionStore admission paths | PU07 | Partly |
| DEV probe chain as fact-path prerequisite | `Mod/CityFlowProbe.lua:60`; `Mod/FreshBindingHook.lua:5-8`; `Mod/Gameplay.lua:874-876` | O1/O7 | No |
| UnitSiteProbe startup dependency | `Mod/Gameplay.lua:908-918` | O7 | No |
| PerformanceCounters load-time binding; unguarded `P.Count` | `Mod/Probe.lua:553-569` | O2/O7 (G30) | Partly |
| Trace factory built unguarded in ~10 modules + UI; error classification in diagnostics | Commerce, Capital, Development, EngineeringStudy, Crew, IndustryHistory, Bridge, IndustryWonderEffects, UI CityPotential; `Mod/CultureNetwork.lua:368` | O7 | 2 of ~10 named |
| GC gate invariants (Flight vs enabled, nil gate, latch) | `Mod/PerformanceCounters.lua:16-30,213-214` | O7 | "Keep GC policy" only |
| PurchaseProbe production cleanup; BoostRefresh waits on GreatWorkProbe | PurchaseProbe, `Mod/UI/BoostRefresh.lua:11` | O7 | No |
| Test-named SQL used by production; duplicated modinfo component | LegacyCleanupCatalog, Tombstones, modinfo | O7 | No |
| Derived-save adapter, Store stamp, tests s9g1-s9g4, static alarm | NetworkRecovery*; `Mod/CityProgressionStore.lua:316-323,1751-1755` | O7 | Kept "until compat gate" |
| D1/exception-A tests needing deliberate rewrite | `DevelopmentTests/test_refactor_s4b.py`, `test_refactor_s5d4c11.py`, ~14 files | O3 | No |
| True-absence harness layer | DevelopmentTests harness | PU11/O7 | No |
| Commerce UNKNOWN allowlist misses DEPTH/CAPACITY; `clear()` removes ACCESS marker; double ACTIVE/WORKERS subscription | `Mod/Commerce.lua:104,330,380` | PU01/O3/O5 | Partly |
| `Standardization.Refresh` drops work when busy | `Mod/Standardization.lua` | O2 | No |
| Store admission hook error poisons pending candidates | `Mod/CityProgressionStore.lua:2136-2140` | PU07 | No |
| Standardization adopts installed carriers after same-owner reference change | `Mod/StandardizationEffects.lua:229-233` | PU08/O3 | No |
| Misleading "DEV/Probe/read-only" headers on production files | Probe, GovernorProbe.sql, BindingProbe, UnitSiteProbe | O7 | No |

## VII. What holds (STATIC_CONFIRMED)

- K-only output is expressible with existing carriers; no new SQL IDs or save Properties; the formulas are monotone; Commerce per-domain Floor-then-sum is preserved [G2-8].
- Dirty invalidation is synchronous; Capital/Development confirm re-validate live; receiver exits never wait on pending topology [G1-6, G1-7].
- Signed contracts settle on stored terms with receipt checks; durable receipts protect Claim, Dialogue, Engineering Study, Crew, Capital and Development; FC re-delivery cannot re-execute money or units [G4-6, G5-3, G6-6].
- No path defaults or guesses Mod-owned history; Industry E requires complete coverage [G6-7].
- Phase0 order, the EmitDerived window, seal-then-drain and the final startup order are as stated [G5-7].
- Claim accepts genuine native early completion; no timer gate [G6-4].
- Eight collection eras, Wonder without N/E/L, Cross without D [G9].
- Both deployment tools behave as G23 describes [G8-1..G8-3].
- B396's route-proof latch and bounded load recovery are fixed [B396 cross-check].

## VIII. Disposition table for Primary

Suggested dispositions only; Primary records the actual Accept / Rebut / OwnerDecision in the package's own table.

| Finding | Evidence | Suggested disposition | Fix location / package | Minimal verification / re-audit | Status |
|---|---|---|---|---|---|
| A01 | G1-1, G2-2 | OwnerDecision (OD-1) | NET05, FS04, D1-E5, O3 | LOCAL per family; re-audit NET matrix | Open |
| A02 | G1-2, G1-5, G5-5, G5-6 | Accept + OwnerDecision (OD-3) | NET01, D1-E1, PU03, O1-O3, O8 | LOCAL per cause; re-audit trigger table | Open |
| A03 | G3-1, G3-2, G3-6, G3-7, G1-3 | Accept | O3, O8, D1-E5/E6/E7 | Re-audit D1 disposition table | Open |
| A04 | G2-1, G2-5, G2-6 | Accept | T0 text, U5 baseline, O3 | T0 table review | Open |
| A05 | G2-3 | Accept | O3, FS03 | LOCAL unknown-role source | Open |
| A06 | G8-5, G3-4, G4-7 | OwnerDecision (OD-4) | Fact contract R0, O3/O4/O7 | None beyond the decision | Open |
| A07 | G4-1 | OwnerDecision (OD-2) | PU06, FS05/FS06 | LOCAL isolation → exit → reload | Open |
| A08 | L-01, G3-3, G4-9 | Accept | FS01/FS03/FS04/FS06/FS10, sync timing | Grep inventory | Open |
| A09 | G1-4, G5-2..G5-8 | Accept | PU03, O2, O5, FS08 | LOCAL drop cases | Open |
| A10 | G5-1 | Accept | FS09, O5 | LOCAL failed-owner exit | Open |
| A11 | G4-2..G4-5 | Accept | PU06, FS06 | LOCAL per R class and mode | Open |
| A12 | G2-4, G2-7, G2-8 | Accept | O3 | LOCAL write-failure cases | Open |
| A13 | L-05 | Accept | PU01/PU03/PU06 vs O1/O2/O4 | Plan review | Open |
| A14 | L-04, G3-2 | Accept | Plan, section V | None | Open |
| A15 | G6-1..G6-3 | Accept | PU05 | LOCAL ambiguous grant; native N0 | Open |
| A16 | G6-4, G6-5 | Accept | PU09 | Native N0 | Open |
| A17 | G6-7, G6-8 | Accept | PU07, PU08 | LOCAL recapture with unfinished exit | Open |
| A18 | G7-1..G7-5, G7-8 | Accept | Q ledger, G30, O1/O2/O7, FS10 | Re-audit Q ledger | Open |
| A19 | G7-6, G7-7, G7-9 | Accept | O7, PU11 | GC invariant test; native N2 | Open |
| A20 | L-06, G8-4, G4-7 | Accept | FS05, final acceptance, tools | None | Open |

## IX. Limits

- The user handoff behind ODP-01=B and ODP-02=A is not in the repository; where the candidate's interpretation decides player-visible behaviour, this report asks rather than assumes (OD-1, OD-2).
- Nothing was executed; every verdict is static. Native unknowns with minimal checks: Crew same-turn counter behaviour and unique completion witness, project-removal events, RequiredBuilding removal, cold first-proof order, native `include()` of a missing file.
- Sub-audit claims marked "as reported" in the companion were not re-read by the Advisor; every High item and every fact behind section II was.

User decision: OD-1 to OD-4 (section II).
User testing: none now; native touchpoints are a proposal for the revised plan (section V).
Primary next: record a disposition for each finding in the package's table, revise the candidate and FS texts, and bring the revised NET matrix, D1 table and Q ledger back for a short re-audit before implementation. This report and its companion are Stable and ready for publication review.
