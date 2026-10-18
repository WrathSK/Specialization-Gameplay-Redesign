# B236 native review and B237 repair proposal

Evidence: **USER_GAME_TEST_PASS — scoped results**, **USER_GAME_TEST_FAIL — fixed Crew injection and unfinished formation continuity**. Review baseline: develop `48172d8`; source/live **B236.263 / modinfo263**, implementation `8942cf56b93214a6aeacf67b590801eee1ca83be`, receipt `B236.263-8942cf5-playtest.json`. Read-only comparison confirms237/237 tracked Mod files match the deployed runtime. Main remains `e901a22` / B069.96. This review changes records only; B237 is **PLANNED_NOT_AUTHORIZED**.

## Evidence retained

Original collector output remains ignored under `local/diagnostics/B205/session-20261018T132310Z-0724f1/`. B205 is the reused collector label, not the tested build. Attribution uses the user submission and deployment provenance. All261 records are present, seq1–261, T20–25, with15 observer contexts. The collector ends INTERRUPTED and reports no alerts; that does not imply gameplay PASS. Transport reconnects do not leave a gap in this retained scalar sequence. No new screenshots were submitted in the current inbox.

| File | Bytes | SHA256 |
|---|---:|---|
| records.log |91846|`020e7bd72947704ad8779aee3f1f9ded34f226c2aa9656526851d83835bbb55a`|
| events.jsonl |8825|`c9867144942f5d2dc0a4a1e9a811e56e3a9cffd9ce67e490b7c03601244d24f7`|
| summary.txt |621|`edaf05ae0718fe85095d4865c12eca999569de587d7517dc454393573e90c3ee`|

The existing [local result](Specialization_B236_Crew_Local.md), earlier native evidence and raw originals remain unchanged. The startup INDUSTRY_HISTORY_RESTORED record is not a cold-load test of newly formed Crew assets. The user explicitly defers Crew cold-load persistence and enemy-contact protection to the next combined batch.

## Accepted and failed scope

| Item | Evidence | Result |
|---|---|---|
| Paid formation and source binding | Six CREW_BOUND records: seq139/143/150/154/256/260, two source cities, capacities250/1360 and verified unit IDs | Scoped native formation/binding works; not proof of untested owner transitions |
| Two slots and consumption release | seq150/151 count2/wanted=false; seq156–159 count1/wanted=true; seq180–182 count0; seq256–261 ends count2/wanted=false. User explicitly accepts cap/release | USER_GAME_TEST_PASS for observed living/reserved capacity and release |
| Surplus not transferred | User confirms no overflow; seq156 requests615 for remaining615 against capacity1360 and then the Wonder completes | Scoped no-overflow observation accepted; keep as a regression check when replacing the injection primitive |
| Industry IV same-turn entry | seq161 Study AVAILABLE, seq162 Wonder ACTIVE4, seq163 price140, all T23; user explicitly accepts the immediate update | USER_GAME_TEST_PASS; no separate repeat of B235 entry test |
| Engineering Practice tiers | Observed new tier-I quotes375/350/325/300, current ratios150/140/130/120; user accepts all three Practice discount tiers updating | New-order price selection PASS; does not make unfinished-order continuity PASS |
| Standardization holders | User confirms recipient distinguishes source cities and different levels. seq167–179 shows sourceCount2 and verified projection after template updates | User-observed holder distinction PASS; logs provide aggregate inputs, not each holder's full target table |
| Fixed Crew injection | User observes amplification by Megaproject Engineering and Wonder-production policy; seq145 requests250 from progress0, seq156 later reads385 for the same city/cost in T23 | USER_GAME_TEST_FAIL: locked capacity is not the native final addition |
| Formation progress on Practice change | User reports unfinished progress resets; seq183/184 admits325, seq201 loses the queued reservation before subsequent Wonder updates, seq219/220 exposes new300 quote | USER_GAME_TEST_FAIL: start-lock/unfinished-project continuity is incomplete; exact old native progress is not logged |
| Crew cold load / enemy contact | Explicitly deferred by user | USER_GAME_TEST_REQUIRED, merged into next batch |
| Institution visual details | No distinct UI acceptance statement or new screenshot in this submission | Delivered; no separate visual PASS inferred |

There is no CREW_HELD/error record in this session. Standardization's52 VERIFIED records and final network AVAILABLE states follow temporary pending states. The two reported defects remain failures even though the current diagnostic did not emit an alert.

## Injection diagnosis

[UnitActions](../../../../Mod/UnitActions.lua) validates source/target, consumes the unit once and calls `AddProgress(min(capacity, remaining))`. It does not bypass or normalize native Production multipliers. Capping the input only caps the argument; it does not cap the engine's transformed output. The observed385 after a250 request corroborates the user's finding. The log does not capture the complete modifier stack or an immediate after-read, so385/250 must not become a hard-coded correction factor or a claim of an exact stacking formula.

The present CREW_USE_RETURNED record repeats the **pre-call** progress and requested amount; it confirms API return only. [CrewPrecision](../../../../Mod/CrewPrecision.lua) has a separate after-read, but its B046 print is outside this collector's retained TRAIN stream. Therefore the next patch must record the actual same-target post-progress/completion in the existing bounded stream, not label the requested number as actual Production.

The prior local fixture in [test_b236_crews](../../../../DevelopmentTests/test_b236_crews.py) implements AddProgress as plain addition. Its no-multiplier test cannot prove an engine bypass. A bounded actual-writer counterexample replacing only that native fixture with an illustrative1.54 multiplier returns requested250/actual385 and consumes the unit while reporting success. This is **LOCAL_SIMULATION** evidence of missing isolation, not an independent measurement of native multiplier ordering. The earlier local result remains frozen; its native boundary is now resolved as a failure in the tested scenario.

## Formation diagnosis

[SQL](../../../../Mod/Data/CrewProjects.sql) represents prices with different project IDs sharing the same visible tier name. [CrewProjects](../../../../Mod/CrewProjects.lua) lines101–116 deletes an admitted order when it is absent from the current queue and has not completed. Its native reader does not read stored per-project progress, so it cannot distinguish a genuinely abandoned order from an unfinished project temporarily outside the queue. Lines128–136 retain an old admitted prerequisite while queued, but publish only the new-price variant as selectable. [CrewProjectUI](../../../../Mod/UI/CrewProjectUI.lua) then filters out the old variant even if the item is marked IsCurrentProduction.

The log establishes that the325 reservation disappears before the observed price change to300. This matches losing the old order and offering a new ID with a separate progress bucket. It does not establish that the engine erased the original bucket. There is no explicit progress setter/zeroing operation in these price-refresh paths. Preserve the user's visible failure; do not replace it with a claim that native stored progress has been proved deleted.

Actual-source counterexamples were run without editing Mod or formal tests:

| Scenario | Observed local result |
|---|---|
| Keep old order continuously queued, then change N | Saved order and old prerequisite remain; old variant hidden in selection, new variant visible |
| Remove unfinished old variant from queue, retain modeled native progress100, then change N | Saved orders1→0; old progress100 untouched by writer; old variant hidden, new variant visible |
| Present old item with IsCurrentProduction=true to actual UI filter | Old item is removed; only new-price item survives |

The reproduction script/result are retained locally at `local/diagnostics/B236/review-20261018/`, ignored and uncommitted. Native per-project progress, exact queue entry and prerequisite changes need the next patch's bounded transition readback. The repair must cover temporary target switches/resumption as well as continuously queued formation; a test that checks only retained price metadata misses the visible failure.

## B237 repair proposal

**Scope:** the two failed Crew paths, with the already deferred cold-load/contact checks in one session. Preserve accepted cost/capacity/source rules, two slots, one-use safety, ordinary Wonder bonuses and all completed permanent assets. No new timers, broad dispatcher rewrite, other profession work, GC change or new Gameplay rule.

1. **Fixed final construction.** Inspect the actual loaded native/HD construction APIs for a target-specific final-progress writer or an exact current-target multiplier input. Select a route only after its context and semantics are established. If normalization is needed, derive it from the native current target, not a manually summed list of known policies or the observed1.54. Validate rounding, completion and overflow with unchanged one-use receipts. Do not temporarily remove third-party policy effects, loop with negative AddProgress, or consume a unit when the required input is unavailable. If no route proves the accepted fixed result, stop this subpath and report the specific primitive limit; do not silently accept amplified construction.
2. **Preserve unfinished orders.** Read the exact native queue and per-project progress at admission/resumption and relevant events. Distinguish completion, real cancellation and paused unfinished progress. Keep a started Crew on its original project ID/price; new prices apply to the next Crew. Expose the old current/resumable entry correctly, keep its required access, and separate actual queued capacity reservations from stored unfinished progress. Avoid switching project IDs, writing compensating progress or broadly clearing queue state. If evidence shows a prerequisite write itself invalidates native progress, repair that exact transition rather than guessing a refund.
3. **Close the local gaps.** Use actual writer/UI tests with multiplier-bearing native fixtures, incomplete per-project progress outside/inside the queue, N/ACTIVE price changes, cancellation/reselection, duplicate completion, source isolation and one-use failures. Include replacement-before-removal ordering and cold reconstruction of the affected order/binding. Extend the existing bounded log with old/new project ID, progress, price, queue/admission state and actual injection before/after; no new diagnostic system or polling.
4. **One combined native acceptance, after approval and local checks.** Start a partially paid Crew, cross a Practice threshold, resume it at the old price/progress, then check the next Crew's new price. Use one known-capacity Crew on an unfinished Wonder with ordinary production bonuses and check the final delta; check completion/no spill on the remaining-cost boundary. Include one saved Crew/order cold restart and one enemy contact when available, as already deferred. Do not repeat all accepted Industry/Standardization tests or reopen held Culture work.

Expected implementation surface: CrewProjects, CrewProjectUI/order adapter, UnitActions/ConstructionProbe/CrewPrecision and their direct tests; a project-definition change only if necessary to the selected price/progress solution. Source binding/capacity values and Design semantics stay unchanged. Detailed native primitive selection is a prerequisite within the proposed repair, not a claimed existing solution. No B237 code, build or deployment is created by this review.

## Review checkpoint

Current/runtime remains B236.263; main, source, tests, Design, formal Architecture, configuration, frozen reports and raw evidence are unchanged. The review updates only this result, Status/Authority/current manifest and relevant review hashes/provenance. Reference/selector checks and helper self-test PASS (237 runtime files,743 guarded context files);358 scoped Markdown links/anchors resolve. The exact six-file diff and unchanged prior Status/runtime hashes were reviewed. Original log SHA256 values remain unchanged; the staged publication gate is run separately before commit. No gameplay-wide regression or user retest is requested for this documentation checkpoint.

User decision: approve or revise the proposed B237 two-path repair; no new Gameplay decision is requested.
User testing: deferred cold-load/contact join the next approved batch; no extra B236-only session.
Primary next: finish documentation/context/publication checks, commit/push develop, then stop for implementation approval.
