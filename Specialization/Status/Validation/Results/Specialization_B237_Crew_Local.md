# B237 — Crew continuation, tier-I260 and fixed-injection hold

Evidence: **LOCAL_SIMULATION_PASS** for the delivered repair and hold; **STATIC_CONFIRMED** for the inspected native wrapper; **BLOCKED** for exact fixed injection; **USER_GAME_TEST_REQUIRED** for new continuation behavior. Baseline develop `72dc64f`, source/live B236.263 `8942cf5`. User approved the [B237 proposal](Specialization_B236_Native_Review.md#b237-repair-proposal) plus tier-I260 and corresponding Design/cost updates. No whole-batch or native fixed-injection PASS.

## Delivered changes

- D0052 changes only tier-I capacity250→260 and Standard150/140/130/120% formation prices to390/364/338/312. TiersII–V420/750/1000/1360 and their prices are unchanged. [Formal content](../../../Design/Content/Industry_D0052.json), Spec, reading page and acceptance provenance agree. Industry D0045 and all previous frozen evidence are unchanged; the new D0051 Spec snapshot is byte-identical to the previous accepted Spec.
- The existing native IDs retain the suffix250; it is an identifier, no longer a value. CrewModel separates IDs from capacities. New formations bind260 at Standard speed; completed units continue using their saved locked capacity. No old-build save migration or catalog rename.
- CrewProjects reads native per-project progress through the existing UI reader. It keeps one PAUSED admission per unfinished project bucket, reuses its original ID/price, and shows its native progress in transition logs. Positive progress is retained even after a target switch; no progress setter/refund is used. Zero/unknown/missed completion remain distinct. Player-global completion counters do not turn another city's positive local paused progress into a grant or corruption.
- PAUSED records do not occupy the two actual living/queued slots. Resumption reserves a slot, reuses the order serial and rebases the global completion counter; failed UI admission returns it to PAUSED. The existing property remains version1, bounded at20 paused buckets plus2 active reservations. Source validation, loss cleanup, ambiguous-write/grant hold and no replay remain. Native access is added before obsolete unstarted access is removed.
- Production UI retains an old queued/resumable row, marks paused entries“续建”and displays their locked price. Fresh orders use current prices. The existing bounded log adds project/price/progress/queue-phase fields; the existing precision observer is forwarded without changing investment receipts. No new polling/timer, dispatcher, GC policy or global ledger.
- Exact fixed injection has **not** been solved. The approved stop condition applies: UnitActions rejects before receipt/reservation/unit debit; no native production write occurs. A Chinese button tooltip and Industry report explain the hold. Saved units and capacity remain intact. No amplified fallback or approximate compensation is shipped.

## Native primitive boundary

Read-only loaded sources: Mac Civ VI app1.4.6 / build376653.178; Expansion2 GameCore, HD UI/Gameplay helpers and the configured loaded Gameplay DB. No process attach, game launch, external writes or new prototype. Offline object-file disassembly was used only for the named production wrappers and one-shot production effect.

`<CIV6_APP>/Contents/MacOS/GameCore_XP2.dll`: 42170144 bytes, SHA256 `3ad7b6d897489001e913f58b3a7a2d9c46bf407a6b198458edf58f2fcfd4c774`. Native addresses below are arm64 virtual addresses in this exact object, not stable API contracts. The ignored local evidence folder `local/diagnostics/B237/local-20261018/` retains the bounded inspection scripts, output, source manifest and local results; raw output contains machine paths and is not published. The [API index](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CityBuildQueue) provides names/context only; it does not establish bypass semantics.

| Route inspected | Evidence and limit |
|---|---|
| Lua AddProgress | Wrapper0x759114 reads Lua argument2, converts number to integer (`fcvtzs`) before fixed-point scaling, then reaches the common production routine0x2aa188 through0x2aa720. No optional ignore-multiplier argument is read. B236 native amplification supplies the behavioral counterexample. Dividing by a guessed/current multiplier is not an exact general correction after this truncation. |
| GetCurrentProductionTypeModifier | HD `UI/Replacement/CitySupport.lua:237` uses it as military formation type, not a production bonus. It is not a normalization factor. |
| CreateIncompleteBuilding | Wrapper0x758b50 and implementation0x2b92b0 use an integer percentage of full cost (100 completes), and create/place the building. This is not an arbitrary exact accumulated-progress setter. Recreating an existing Wonder is not an established safe replacement. |
| FinishProgress | Wrapper0x759184 / implementation0x2ace08 calculates remaining cost and reaches the common production routine. It is not a partial fixed-value setter or proof of multiplier bypass. |
| Great Engineer one-shot production | Loaded `MODIFIER_SINGLE_CITY_GRANT_PRODUCTION_IN_CITY` / `EFFECT_GRANT_PRODUCTION_IN_CITY`; factory0xe4673c, effect0xcd8b24, apply0xcd8c98→0xcd8d7c→0x2aa188. Amount and KeepOverflow are read. The inspected effect reaches the same common production path; KeepOverflow controls overflow allowance, not demonstrated ordinary-bonus isolation. No native claim that this carrier solves fixed injection. |
| HD percentage helper | `Gameplay/HD_Common.lua:307–354` computes a capped integer then calls AddProgress. This inherits the relevant primitive limit. |

**Conclusion:** no exact partial final-progress writer/bypass has been established in this inspected surface. This is not proof that every possible engine route is impossible. No infinite search, repeated negative writes, third-party modifier withdrawal or Gameplay reinterpretation. Further work must establish a different bounded primitive, or obtain an explicit user Design decision; this batch does neither.

## Local validation

223 targeted tests PASS, including100 loaded-speed×tier×price matrix subcases. Actual writer/Store/production UI fixtures cover continuous and paused old-price entries, N/ACTIVE changes, cold reconstruction, same-bucket duplicates, another city's global counter, zero/unknown progress, failed resumption writes/cancel, native quote mismatch, source loss and unchanged-event no-write behavior. The fixture records real native progress separately from queue membership; assertions check it is untouched. No tests claim native prerequisite persistence from local simulation.

The B236 consumption tests incorrectly treated a linear AddProgress mock as fixed-output evidence. They now verify the intentional pre-debit hold against multiplier-bearing fixtures1/1.54/2, with no receipt/property mutation, no unit consumption and no production call. This is a tested safety boundary, **not** a fixed-injection success. The old B236 result and reproduction remain frozen. Unaffected target-only, formation/receipt/source and typed investment receipt checks remain.

Selected suites: Crew25, new continuation/observer20, entry/receipt3, production UI9, Engineering38, Standardization38, Industry history25, Store18, Dialogue21+UI7, investment publication19. Three inherited package/retired ordinary-building transport tests are excluded explicitly (old build stamp and superseded target contract); they are not edited to pass. Current package264 and Wonder-only hold are checked directly. The excluded IDs are `test_investment_update_propagation.InvestmentPropagation.test_syntax_package_and_unchanged_contracts`, `test_investment_update_propagation.InvestmentPropagation.test_actual_construction_team_transport_remains_unscoped` and `test_b235_engineering.Package.test_project_and_exact_files`. No gameplay full regression, stress or native CPU/memory improvement claim.

42 additional existing collector/diagnostic tests PASS after the fixture-only write permission was available; the initial restricted run failed to create its disposable `local/` directories, not on diagnostic assertions. Context check/self-test,10 changed-Lua parses, package237-file equality, final localization SQL and749 active Markdown links/anchors PASS. The D0052 JSON semantic diff is limited to the two tier-I arrays, first cost-matrix row and provenance; all older Status sections, Industry D0045 and previous frozen results remain byte-identical. No new timer/update subscriptions; the existing UnitPanel gains the hold tooltip, and the legacy site diagnostic uses a tier label instead of assuming every saved tier-I asset has capacity250. Final diff review and `git diff --check` pass.

## Minimal native acceptance for the delivered subpath

Use the current agreed test-base policy; begin a **new** tier-I order under this package, not a pre-update quoted order. Keep the existing collector running manually.

1. In an Industry IV source at N0, start“组建一级施工队”at390 and accumulate some native progress. Temporarily select another target; cross N0→1 (or another known Practice threshold). The old row should remain“续建”, with the same progress/old locked price; the fresh tier-I quote should be364. This distinguishes retained native progress/eligibility from merely retained metadata.
2. Resume the old entry; save once while it is in progress, then cold-load. Confirm the old price/progress and source reservation survive, finish it and confirm one bound260 Crew. Its saved source counts against the same two-slot limit. This is the modified admission reconstruction boundary, merged with the deferred Crew cold-load.
3. When conveniently available, include the deferred enemy-contact check: a surviving protected Crew keeps its binding and slot. Do not repeat accepted Standardization/IV-entry/Practice tests. No construction-injection test is requested: it is deliberately unavailable before debit. Contact may remain pending if no target is available; do not manufacture another long test.

The native continuation check can be deferred to a later combined package; local results alone do not close it. Full Crew playability remains blocked by fixed injection.

## Checkpoint

Source **B237.264 / modinfo264**; local continuation/value repair ready, fixed injection held. Live remains B236.263 until a clean committed W0003 deployment passes its gates. Main B069.96, Store core, other professions, GC, frozen evidence, external configuration and original logs remain unchanged. Context/reference/package checks and the31-file staged publication gate PASS. Deployment still requires clean committed source and a fresh game-exit check.

User decision: no new decision is needed for the delivered subpath; any Gameplay alternative to exact fixed injection requires separate explicit approval.
User testing: one minimal continuation/cold-load/contact session, optionally merged later; do not retry the blocked injection.
Primary next: finish checks, commit/push; deploy only through existing exit/hash gates, then stop. Fixed-injection follow-up remains a bounded technical blocker, not authority for another batch.
