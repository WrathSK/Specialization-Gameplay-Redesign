# B238 native review — paused Crew occupancy and Commerce handoff

Date:2026-10-18. Basis: develop `519dbac`; source/live B238.265, implementation `c97117a`, receipt `B238.265-c97117a-playtest.json`. Read-only comparison:237/237 tracked Mod files match runtime. Main remains `e901a22` / B069.96.

Evidence: scoped **USER_GAME_TEST_PASS** for the user's normal results and corroborated continuity; **USER_GAME_TEST_FAIL** for paused Crew occupancy; **STATIC_CONFIRMED** and **LOCAL_SIMULATION_COUNTEREXAMPLE_REPRODUCED** for its cause. No implementation or deployment in this review. The requested combined next batch is [proposed B239](../../../Architecture/v2/Commerce_Preparation.md#proposed-b239-combined-slice), not an implemented build.

## Evidence retained

The B205 path/prefix is the existing collector name, not the tested build. Attribution follows user submission and verified deployed source. Raw sessions remain unchanged and ignored:

- `local/diagnostics/B205/session-20261018T150530Z-6612d6/`:96 records, contiguous seq1–96, T25–26; GAME_EXITED.
- `local/diagnostics/B205/session-20261018T151510Z-8cd821/`:127 records, contiguous seq1–127, T26; INTERRUPTED. Includes a later same-process reload with a new Gameplay context; compare branches separately.

One screenshot was read and moved, without alteration, from `ScreenShots/` to `local/legacy-workspace/Specialization/Status/Validation/Evidence/B238/`, keeping its original filename. The ignored `manifest.json` records before/after SHA256. It shows a new312-cost order at0 progress while the disabled old **续建** retains14/338. Screenshot bytes12824187; SHA256 `b946c8b9f9adf3567b0087c2595d5876c31473670488db7c6a33de6dba8b1e69`.

Local reproduction script/result and the file-hash manifest remain ignored under `local/diagnostics/B238/native-review-20261018/`. No raw images/logs/saves are published. Previous B236/B237/B238 local results remain unchanged.

| Session | File | Bytes | SHA256 |
|---|---|---:|---|
|150530Z|records.log|31689|`4c1ec9bba7e901ce2799c7e12ec5d7d625ad78543ec96eabe1160362dcb6898c`|
|150530Z|events.jsonl|1960|`1aa3986c42c1ceaf8a6cca6f10b78cea209d4ffec56605f0887cff3b1f4e3503`|
|150530Z|summary.txt|621|`d471439bafd0c62f2ef2b077d5189da918c60b9f7a5e27b119bd20c04c84eaaa`|
|151510Z|records.log|40993|`adaaa4b5e2f854ccc2f87ac2282228c0b8bf37de4dee2059a1f76706e608e7a3`|
|151510Z|events.jsonl|1356|`866dadcae2117fc6607be02c1dda4aa5318422e84d01873a1be545de53d53680`|
|151510Z|summary.txt|482|`5bc14ad4c6a4820c1078fb027ad63aeb4c1967c4a6be99e9c7049297429bef1a`|

## Results and diagnosis

| Item | Evidence | Conclusion |
|---|---|---|
| Old price/progress through Practice change | First session68/70:338 admission;88:PAUSED14/338;91:new ratio120;92/94:resume the same reservation7 at14/338 | Continuity works in this path; progress was not deleted |
| Cold-load continuation and new260 binding | Second session22/55/57 retains old reservation7;58 grants one verified260 unit. Its initial new context follows the first session's full exit | Scoped continuation/load/binding accepted; not every untested Owner transition |
| Later new order adopts312 | Second session61/63 and119/121 show new admission at312 | New-price behavior works |
| Paused occupancy | Second session122/123:one living, one paused, zero queued, `wanted=true`;125/126:new admission accepted, then living1+queued1+paused1 and `wanted=false`; screenshot confirms old continuation disabled | Confirmed defect; not a stale display-only issue |
| Restored construction and other observed checks | User reports other parts normal; first session58–65 records two returned use calls and live count2→1→0 | Accept user's observed scope. These uses have saved250 capacity; do not relabel them as new260-unit injection tests. One precision read is UNKNOWN, another synchronous delta0; neither proves eventual production loss or exact arithmetic |
| Another city's price guard | Six `CREW_NATIVE_COST_MISMATCH` records for city65536; tested city131073 continues | Keep the guard and record the separate held path. Logs lack both compared prices, so do not invent its precise cause or reprice that city's old order. No broad old-save migration |
| Enemy-contact protection / rare channels | No specific contact sequence in these logs | Retain earlier deferred/conditional evidence; user's general normal-result statement does not create a new contact test |

The cause is explicit in [CrewProjects](../../../../Mod/CrewProjects.lua): `reserved(v)` ignores `PAUSED`; `audit` computes free room from living+non-paused reservations; `Request(RESERVE)` requires that same free room even for resumption. [CrewProjectUI](../../../../Mod/UI/CrewProjectUI.lua) correctly renders the resulting false `startable`. The report even says pause does not occupy capacity. [B237 regression](../../../../DevelopmentTests/test_b237_crew_continuity.py) `test_pause_does_not_occupy_two_actual_slots_but_resume_reserves_one` encoded this assumption. Thus earlier local green results did not cover the user's intended unfinished-order occupancy; the fixture did not merely miss an engine race.

One read-only reproduction uses the actual current Crew writer/Store and existing native-queue fixtures. It yields:

| State | Living | Queued/reserved | Paused | New start | Old resume | Saved progress |
|---|---:|---:|---:|---|---|---:|
| Paused order |0|0|1|true|true|14|
| Another order completed |1|0|1|true|true|14|
| Another new order admitted |1|1|1|false|false|14|

This reproduces the admission defect locally, not native timing/performance. It uses fixture prices390→364 because that existing fixture contains four Wonder definitions; the native338→312 trace independently establishes the same path. Initial harness attempts with an out-of-fixture Wonder and a temporary import-shadow issue were corrected in the standalone reproduction only; production code and formal tests were not edited.

## Proposed repair and Industry boundary

Count paid unfinished admissions, including PAUSED, once; resumption reuses its slot, and completion exchanges it for a living unit. Keep actual queue cardinality separate from total occupancy, preserve all old price/progress/source/capacity data, and retain failure/UNKNOWN protection. Gameplay and UI must use one decision. Previously over-admitted states block new work without deleting paid progress; safe continuation still obeys the living ceiling. The [combined plan](../../../Architecture/v2/Commerce_Preparation.md#proposed-b239-combined-slice) defines the regression closure.

This is the remaining confirmed repair on the implemented Industry main chain, suitable for the user's requested merge with COM-A. It does not erase named protection/rare-price/speed/exceptional-Owner gaps or claim all native combinations PASS. No separate Industry feature batch, balance work, modifier isolation or District-body purchase is required before Commerce. Native retest should focus on full-occupancy continuation and new-order rejection, combined with Commerce's genuinely new functionality.

## Advisor review and next batch

Primary read the Stable Commerce audit, checked its D0050 comparisons and current relevant sources, and retained its four-batch grouping: Commercialization → Capital → Development → Restructuring. Its B231 basis predates the current network recovery and Industry implementations. The [refreshed preparation](../../../Architecture/v2/Commerce_Preparation.md) corrects obsolete rules, isolates Capital's earliest-attainment question and Commerce-specific precision gates, and scopes prerequisites from existing audits. In particular, retire the old global-write Commerce audit instead of copying it, expose only verified route facts, and make existing transport-limit failures visible without a general network rewrite. No Advisor recommendation is automatically adopted as Gameplay.

The Advisor original and unpublished dependency reports remain unchanged and ignored; this checkpoint publishes Primary's reviewed plan, not an incomplete report-link chain. No new raw-evidence public links or personal machine paths are introduced.

User decision: review the concrete B239 combined scope; precision changes, if needed, require an explicit choice. User testing: no additional B238 test requested now. Primary next: after approval, implement Crew occupancy + COM-A, run targeted local closure and prepare one combined native session. This review stops without code, Design, test-assertion, runtime, configuration, GC or main changes.
