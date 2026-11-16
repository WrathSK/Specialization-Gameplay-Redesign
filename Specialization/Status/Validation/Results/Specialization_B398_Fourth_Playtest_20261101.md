# B398 fourth playtest — Commerce, queue recovery and border displacement

2026-11-01. Primary; reviewed source `966069d`, runtime B398.425 from `73bf5b5`, Design D0058 / Architecture A0183. Evidence intake and scoped offline investigation only: no runtime/test source, gameplay, saved schema, Design/Architecture, deployment, game configuration or external Mod changes. Live/source remain343/343 MATCH with the already recorded package hash. This report does not close U5 or authorize the follow-up repairs.

## Main conclusions

- **PT016 remains open / USER_REPORTED_FAIL:** Dialogue recovers when the ordinary target finishes naturally, but the active→multi-item→reorder→sole case can still stall. Current actual modules reproduce that missing admission path locally for both Dialogue and Engineering Study. The earlier85 selected tests did not cover this interruption/cancellation round trip; their frozen result is retained.
- **Commercialization calculation/configuration has positive native evidence:** separate per-domain floors, changing local depth/source values, and specialist capacity1/2/3 give the expected configurations. This is not proof that all national Treasury differences are explained.
- **PT015 has progressed:** two real Capital contracts were signed and debited. Their captured due turn is68; this session stops at61. Maturity, once-only payout and durable contract readback after reload remain pending. Development Investment was not exercised.
- **PT017 / UNKNOWN cause:** actual Treasury gains include repeated+52 between END and the following STARTED; this is a balance observation, not just a stale label. No captured Capital payout accounts for it. Do not attribute it to this Mod, HD or native income timing without additional evidence.
- **PT018 / native recurrence:** Open Borders expires atT60 in both replay branches, each coinciding with an activity/move notification and `TEAM_DISPLACED_STOP`. The current prototype then holds the unit. Exact native ejection implementation and the old deleted-save cause remain unproved.

## Evidence and replay boundary

Raw files were read and copied with SHA256 readback to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B398_Fourth_Playtest_20261101/`:4collector files plus68latest native files,72files /8,565,223bytes. Manifest SHA256 `429930206c6b5bef2c7b0923f8daa054da8ff3be1466908d99c2fac96d39c8dd`. Source originals remain. This local private archive is not a permanent external backup and is not published.

Collector alias **C** = `collector/records.log` from `session-20261101T214446Z-594191`; **N** = archived `native/`. Citations below are physical line numbers in those snapshots. C contains1,399TRAIN records,exactly seq1–1399 without a sequence gap,plus metadata/gate lines. It covers four Gameplay contexts:

| Context segment | C lines | Observed turns | Meaning |
|---|---:|---|---|
| A |2–225|61|Initial already-existing state;not the missing original59→61 money experiment|
| B |226–369|52|Short earlier-save inspection|
| C |370–1081|58→60|Reperformed Commerce/signing/Dialogue and first border displacement|
| D |1082–1427|58→61|Reload branch;repeated balances/border displacement,then unit gate read/end|

Collector `events.jsonl` has a partial-frame deadline gap;the later snapshots cover all observed TRAIN sequence numbers. Normal connect-window waits are not proof of game failure. `TRACE_SINK_BUDGET_STOP` means the bounded passive sink stopped regular prints;it does not mean every possible engine action was recorded. Role budgets and missing diagnostic points remain limits. The original handwritten5012/1212/681/903/1143 sequence is not reproduced as those balances in the captured data;do not splice it into these branches or invent missing samples.

## Commercialization — what the captured numbers show

C715(seq705):culture D6 ×29.09765625 ×5%=8.729296875 →8. C743(seq732):Industry D6 ×79 ×5%=23.7 →23. The latter input is79,not the handwritten71,so21 is not the expected result for this replay. Later C764–765:Culture33.09765625→9 and Industry100→30,total39. C801–809:Culture35.09765625→10,Industry102→30,Harbor D3 ×total Food25 ×5%=3.75→3,total43.

C822/835/848/860 show workers2→1→2→3 and total configured Gold40→10→40→43:the later domains pause and resume with capacity. This proves the Mod's configured source/capacity responses in this scenario;it does not settle the HD automatic-worker/GPP semantics or independently measure the final national income delta. The user's missing-district exclusion,UI depth/source updates and capacity observations are retained as scoped user acceptance. LevelI support/IIHousing pass by user observation;II GPP is explicitly untested,not assumed PASS.

Source Industry value subsequently102→113 makes configured Gold43→46 atT59(C956–957). AtT60,branch C reads122→49(C1055–1056),whereas reload branch D reads116→47(C1352–1353). Source/native production really differs between branches;these are not identical numerical replays. D's raw total49.079296875 floors separately to10+34+3=47,not49. The authoritative rule/calculation are [Commerce D0058](../../../Design/Content/Commerce_D0058.json) and [CommerceCalculation.lua](../../../../Mod/CommerceCalculation.lua):12–44.

END58(C873/877) matches configured/carrier Gold43;END59(C982–983)46;END60(D,C1359–1360)47. Configured carrier agreement is evidence about applied building bits,not an engine-income-accounting proof. Network proofs catch up before each captured STARTED,and temporary `RETAINED` states preserve passive effects under D1 while transactions remain strict. Eleven `CAPITAL_COMMERCE_PENDING` rows are refresh guards during pending/mixed facts,not eleven failed debits.

## Treasury — an unresolved real interval, not a rounding explanation

The existing Commerce trace reads `GetGoldBalance`,`GetGoldYield` and `GetTotalMaintenance` ([Commerce.lua](../../../../Mod/Commerce.lua):477–497). Native Base TopPanel.lua146 and Expansion2 TopPanel.lua140 display Yield minus Maintenance. Their arithmetic does not itself specify when every native/other-Mod credit is posted.

| Captured boundary | Balance | Yield−Maintenance at that point | Change from prior listed point |
|---|---:|---:|---:|
| Segment C END58,C877 |545.8984375|319.703125−164=155.703125|—|
| STARTED59,C946 |597.8984375|326.6015625−164=162.6015625|+52|
| END59,C983 |760.5|323.6015625−165=158.6015625|+162.6015625|
| STARTED60,C1054 |812.5|323.6015625−165=158.6015625|+52|
| Segment D STARTED59,C1235 |597.8984375|162.6015625|reload branch|
| END59,C1276 |760.5|158.6015625|+162.6015625|
| STARTED60,C1344 |812.5|158.6015625|+52|
| END60,C1360 |981.1015625|331.1015625−163=168.1015625|+168.6015625|
| STARTED61,C1417 |1033.1015625|168.1015625|+52|

C's complete END58→END59 increase214.6015625 equals52+162.6015625. D END59→END60 increase220.6015625 contains the same52 plus168.6015625,which is10 greater than the STARTED60 displayed net;that is an accounting residual,not a proven separate10Gold transaction. N/Player_Stats.csv50 records balance971 atT60 before the later END sample981.1015625;its integer precision and different sampling phase cannot identify that further+10 source. Total END60→the finalT61 native statistics also cannot be reconstructed solely from the STARTED point.

Thus the handwritten681→903 jump222 is arithmetically consistent with the *pattern*169.9+52,subject to integer/decimal display,but it is not a measured causal explanation of that uncaptured run. Do not extrapolate the pattern to explain903→1143 or claim duplicate Commercialization payment. Current Commerce writes yield carriers;the captured Capital money mutations are two DEBITs,not credits. No native Treasury transaction ledger identifies the+52origin. The narrow read-only HD check did not establish one;bulk-product projects have no loaded `Project_YieldConversions` rows,and their visible helper accumulates production,not a demonstrated52Gold payout. This does not exclude other native/HD paths.

## Capital — signed now, maturity/reload test later

Captured signing isT58,not the handwrittenT59. C780–794(seq768–782):

| Contract | D/S/C | Principal | Actual debit | Balance after | Due | Locked quotation |
|---|---|---:|---:|---:|---:|---|
| Industry,STABLE |6/4/1.25|829.2890625|829.2890625|2487.8671875|68|r30%;total safe return1078.07578125|
| Culture,VENTURE |6/1/1.25|621.966796875|621.96875|1865.8984375|68|r7.5%;success probability46%;success return761.909326171875;failure return310.9833984375 at effectiveR0|

Initial signing Treasury is3317.15625. Each principal correctly uses25%of the then-remaining balance. The second native debit differs by0.001953125 from the requested amount,inside the existing0.01 readback tolerance;it is not a one-Gold overcharge. `expected` in CAPITAL_QUOTE is safe total return;`returnAmount` is probability-weighted expected return,not a settled payout ([CapitalInvestment.lua](../../../../Mod/CapitalInvestment.lua):330–334). The actual money/activation guards remain at72–86 and350–367.

One correction to the handwritten note:46%is **success** probability,so failure is54%before any future changed protection;Chinese text explicitly says成功率 ([Commerce text](../../../../Mod/Text/Commerce.sql):96,201;[model](../../../../Mod/CapitalInvestmentModel.lua):141–148). No credit/settled record appears byT61. No repeated debit is captured on the reload branch,but absence of that record is not complete contract-persistence acceptance. Respect the user's plan to keep the investments and inspect later;do not create another standalone maturity test.

## PT016 — residual admission defect in B398

User reports:append/remove may recover;reorder then remove still waits;naturally advanced Dialogue shows1turn. C157/582/962/1257 confirm four committed BEGINs;C163/588 observe safe failures atline13 after prior starts. [TimedProjects.lua](../../../../Mod/TimedProjects.lua):13 contains both UNKNOWN and MULTIPLE assertions;the sanitized error alone does not distinguish them. N/City_BuildQueue.csv79/86 records Dialogue production and its actual FinishProgress completion atT60 on branch C;branch D deliberately changes to an ordinary project. This is scoped success,not complete queue acceptance.

Offline read-only replay uses current actual UI/client/readers/independent owner/Store through the existing B398 fixture,with explicit native queue/event doubles. Six cases(two projects ×three sequences):four ordinary append/remove or natural-advance cases reach ACTIVE;two already-started→append Worker→Worker first→project first→remove Worker cases end AVAILABLE with no pending round and only the original BEGIN. They reproduce an unstarted legal sole project;no engine-event-order claim is made. Replay script/results remain ignored under `local/diagnostics/B398_Fourth_Playtest_20261101/`;execute `b398_fourth_queue_cases.py` with DevelopmentTests and Lupa2.8/Lua5.1 available. No existing assertions or runtime files were changed.

Concrete mechanism: [TimedProjectQueueIntent.lua](../../../../Mod/UI/TimedProjectQueueIntent.lua):17–19 builds a view signature that can return to its old value after confirmed cancellation. Lines197–199 latch turn+candidate serial+queue signature+view;related queue events at119–122 permit a read but do not distinguish a newly canceled/restarted round. A legitimate same-turn round trip can therefore equal the old attempted key and return before a new BEGIN. Explicit selection at95 clears the attempt;automatic reorder recovery does not. The previous `active_multi_same_turn_resume`case removes a tail without the intervening cancel/reorder and misses this counterexample.

Smallest proposed correction:distinguish confirmed accepted-round cancellation plus new sole-queue evidence from an unknown send outcome,and grant a new bounded admission only for the former. Do not clear the latch for arbitrary events,reset CALLING/HELD blindly,retry uncertain sends,credit interrupted time,change single-item timing or add polling. Add the actual reorder round trip for both owners and retain duplicate/reward/quota/window guards. This is a proposal,not implemented by this evidence intake.

## PT018 — Open Borders recurrence, narrow causal limit

N/DiplomacyDeals.log1–3 and4–6 independently recordT60 expiry of player4→0 Open Borders,along with the reverse2Gold-per-turn payment. C1060→1064 and1345→1349 show an activity/move event,then TURN guard `TEAM_DISPLACED_STOP` in both branches;C1420/1426 confirms later HELD. The diagnosticx23/y25 is the stored expected coordinate;the failed comparison proves disagreement but does not record the new coordinate. The user's observed adjacent southwest move is retained separately.

[ExpeditionSpyGate.lua](../../../../Mod/ExpeditionSpyGate.lua):466–467 finds the tracked exact unit and compares actual coordinates to stored coordinates. The fail-safe stops the prototype rather than accepting a displaced unit as a valid task state;the custom button loss is consistent with its HELD state. The loaded read-only database has `Spy=1,IgnoreMoves=1,DOMAIN_LAND,FORMATION_CLASS_CIVILIAN` for both this unit and UNIT_SPY. It is not simply a missing Spy flag. Whether native ejection checks exact unit type,an active Spy operation or another hidden state is UNKNOWN;do not guess or remove the guard as a fix. The old deleted save remains unproved,but this newT60 recurrence supplies a concrete investigation target. No extra deliberate border test is requested now.

## Coverage and next boundary

Accepted only within reported/measured cases:Commerce basic support/Housing,configuration UI/exclusion/depth/selected-order/capacity,and valid Capital entry/debit. Commercialization **national income**,Capital maturity/once-only/reload result,Development Investment,Reputation effects and Restructuring remain open. GPP is untested/deferred by the user. PT016 is partial,not closed;PT018 is reproduced symptom with native cause unresolved. No forced pillage,ownership or repeated no-P0/accepted-profession campaign is added.

User decision:review the small remaining queue-admission repair and whether to include a narrowly isolated Treasury-origin investigation;no gameplay choice is inferred. User testing:retain the planned two investments through their capturedT68 and ordinary save/reload;no repeat now. Primary next:stop after recording/publishing this evidence;no runtime modification or deployment in this intake.
