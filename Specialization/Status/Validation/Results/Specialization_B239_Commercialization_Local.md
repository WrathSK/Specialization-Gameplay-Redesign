# B239 — Crew occupancy, Commercialization and Commercial Reputation

Date:2026-10-18. Build:B239.266/modinfo266. Review basis:develop `edf1416`, accepted user B239 scope plus the subsequent **per-domain Floor then sum** decision (Commerce D0054). Evidence is **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS** only; actual city Gold, clean native Gold sampling and presentation remain **USER_GAME_TEST_REQUIRED**. No Capital, Development, Restructuring or Culture HOLD implementation.

## Delivered boundary

- Paid PAUSED Crew orders keep one source slot. Resume reuses the original admission/serial/capacity/price/progress; actual queued orders are counted separately. Completion exchanges the reserved slot for a living unit. Existing over-admitted work is retained: no new admission, safe existing continuation only while living+actual queued remains below two. Unreadable or unmatched native queues hold admission without deleting progress.
- One production-list **商业化 / 商业信誉** action opens the five-domain dashboard before native enqueue. Explicit row buttons select/close; no production round or queue mutation. The P0 button with the same label provides a concise read-only report.
- Commercialization uses local eligible D, actual working Commerce specialists, self+direct domestic partners in either direction, and the strongest current total mapped city yield. Only the local Commerce city needs the mapped district; a remote source needs neither that district, a specialization, nor a progression record. Five domains are Campus/Science, Theater/Culture, Industrial/Production, Holy/Faith, Harbor/Gold.
- Each effective domain produces `Floor(.05 * D_local * X * (1 + .005 * R_effective))`; add these integer domain outputs. Preserve raw values and named sources in the report. Existing city Gold modifiers may affect the actual native delta. The encoding range guard is technical/unavailable, not clamping or a new balance cap. Principal/returns/other abilities do not inherit this Floor.
- Selection order is the persistent authority. Current capacity/eligibility derive effective and suspended rows; latest selections pause first and recover automatically. ACTIVE loss retains choices; Owner change clears choices. Reopening appends newest. Effective rows, D/X, Gold, UI and route caches are not persisted.
- Reputation is a separate optional city-record extension. A confirmed third investment begins it atomically; complete Standard-speed Commerce-Identity turns add1 up to40, independently of current ACTIVE. Only ACTIVE IV uses R. Owner loss retains R and freezes unsupported time; return rebases the cursor without foreign backfill. Store owns age writes; configuration writes cannot fabricate/change/delete reputation. Identity exit has a model reset; the future Restructuring transaction is not implemented here.
- Existing P4 without a reliable new reputation start remains explicitly unavailable; no guessed historical age or compatibility migration. Native acceptance should begin at Commerce III and invest to IV.

## Runtime and update ownership

[CommerceModel](../../../../Mod/CommerceModel.lua) validates the bounded five-domain stack and reputation; [Store](../../../../Mod/CityProgressionStore.lua) owns readback/fault isolation and existing turn/loss/return writes. [CommerceCalculation](../../../../Mod/CommerceCalculation.lua) is pure; [Commerce](../../../../Mod/Commerce.lua) owns current sampling, native effects, reverse source dependencies, readable views and exact cleanup. The existing [network bridge](../../../../Mod/NetworkBridge.lua) provides a copied direct-partner projection from its verified private input.

Named events and permanent-city/investment notifications mark affected cities/dependents. Existing publication events coalesce pending work; they do no idle scans. Construction does not mistake district-type arguments for city IDs. Other professions' native effect changes notify the actual source city; only this module's own32 IDs are filtered. No global-output-revision audit, timer/frame polling, new GC or UI-open dependency.

Each audit owns one temporary facts/depth/yield batch. Definition caches belong to the Gameplay context; dirty sets coalesce rather than retain event history. Dependency memberships are replaced with new verified partners and removed on confirmed exit; current views are temporary and clear on loss. Configuration is bounded5, reputation40. Existing shared D's eight-entry policy remains unchanged; this batch removes remote D captures rather than opening that audit item.

Harbor X excludes this module's Gold by withdrawing its owned Gold, sampling clean native source totals, planning all affected cities, then applying outputs. Sources outside the receiver set regain their verified old encoding. No configured-amount subtraction or guessed inverse modifier. **Immediate native getter freshness after withdrawal is a remaining native gate**; local mocks establish ordering and modifier-aware intent, not engine refresh timing. Failures hold the affected path, report residual/unconfirmed cleanup and never claim that a failed removal succeeded.

The exact three old Commerce connected-kind effects and48 old Convergence effects retire; definitions remain for cleanup. The old Convergence startup/request/output subscription cannot forward-write. Startup withdrawal is limited to supported, Store-confirmed cities. Unproven/unsupported objects are untouched. Research/Culture/Industry current effects, basic Commerce support/housing/GPP and shared topology remain. Network transport limits128routes/16384bytes now explicitly publish unavailable reasons without partial inputs or enlarged limits; a complete sample can recover in the same turn.

Standard-only scope is explicit: the current GameSpeedType must reliably resolve to Standard. Other or unknown speed holds Commercialization and does not start/tick Reputation; existing configuration/history and ordinary investment/Potential commits remain intact. No inferred speed scaling.

## Local verification

**336 distinct targeted test IDs PASS**, using the existing Lua55/Lupa environment.17 affected modules cover the actual Crew writer, actual Commerce model/consumer/UI/adapter, actual Store writes/loss/return, current Bridge/Sender, read-only configured DB copied into memory, exact SQL/retirement, and affected Industry/Culture regression. No game, live query, gameplay full regression or memory long test was run.

Two unmodified historical methods are explicitly excluded: Culture B226's fixed modinfo253 packaging method and Engineering B235's fixed modinfo262 packaging method. Their results are not recast as PASS. Current B239 package/actions/imports/SQL/localization are independently checked. Contemporary notification fixtures now name Commerce, and the Industry wiring assertion requires both the retired legacy entry and the new entry; behavior protections were not weakened. The two B237 assertions adopting pause-frees-capacity were corrected to the user's unfinished-work contract.

The actual-Store boundary regressions retain unchanged-reference uniqueness visits0 and per-value/write-count equivalence. That inherited check is not native CPU or memory improvement evidence. Raw local output remains ignored at `local/diagnostics/B239/local-checks.json`.

Final static checks PASS:17 changed Lua files compile;2 XML/modinfo documents parse;244 payloads plus modinfo form245 runtime files without missing/duplicate package entries.12 active documents resolve456 local links,104 Markdown anchors and2 JSON pointers; frozen snapshots and unchanged historical suffixes are excluded. D0054 acceptance hashes match; old D0050/Industry D0053 and frozen Spec byte equality hold. Context check/self-test PASS; CURRENT remains8 lines, default3 projections84 lines. Only named reviewed Runtime_Index/Context_Lock entries changed. Main remains clean at its unchanged commit. Publication gate and final staged diff review precede commit; integrity is not native acceptance.

## Minimal combined native acceptance

Use one continuous session, the current Industry campaign and a Commerce III city with two working specialists and eligible local domains (prefer Campus and Harbor so the new Gold-input exclusion is visible). Run the existing collector manually. Reports/logs carry D/X/raw/Floor; screenshots are needed only for an unexpected UI or actual native yield discrepancy.

1. Crew: keep one living unit and the old paid paused order. If the previous zero-progress312 order is still queued, cancel that zero-progress order first. New formation must be unavailable; old **续建** must retain its price/progress and resume without another slot. It may be paused again for the shared save check; paid progress stays reserved. No repeated full Crew construction/old Industry gate.
2. Commercialization: production list **商业化 / 商业信誉** opens the dashboard without enqueuing. Enable Campus then Harbor. Compare printed raw/Floor with the native city Gold change. For a Harbor source that is itself a Commerce city, X must exclude its Commerce-generated Gold and remain stable on repeated reads. If another source wins, report that limit rather than claiming self-recursion was directly tested.
3. Remove/re-add one working Commerce specialist: the newest domain pauses and returns without reselecting. Make one ordinary local D or source-yield change; the report and configured output update in the same turn. Existing direct-route evidence is inherited; if a useful route already exists, inspect its named highest source without building a special network test.
4. Invest III→IV in this build, finish one player turn and confirm Reputation1 (no40-turn grind). Save/fully exit/cold-load once; domain order/effects, known R and the retained Crew occupancy recover. This checks the new business persistence, not another Probe-default-OFF ritual.

If the local setup lacks a Harbor, the other domains can be accepted, but clean native Gold-input exclusion remains pending until a legal Harbor case. No new unlogged enemy-contact case is invented. Production multiplier balance, rare District-body purchase, other speeds and named exceptional lifecycle edges retain their prior deferred scope.

## Checkpoint and stop

Implementation is complete locally and the guarded deployment is now verified below. Main is not promoted.

User decision: per-domain Floor is accepted; no further Design question for this batch. User testing: the single combined session above after deployment. Primary next: await the user's one combined test and review only its results. COM-B/C/D and unrelated audit findings remain unimplemented.

## Verified deployment — 2026-10-18

Source `972e911cd7635f212ceeffde2280395dda67b9cd` was clean and pushed before switching. The existing tool restored the exact B238 receipt to stable, then activated B239 using `B239.266-972e911-playtest.json`; a reliable OS game-exit check passed immediately before each switch.245/245 files MATCH, digest `ba9af421a89fbc3907f6046d33555f927027132c620496dfaed39c888cfd3b22`; phase DEVELOP_ACTIVE, no pending marker. B238/stable recovery retained, main unchanged, no game launch/configuration edit. Manual staged publication and the commit hook both passed. No USER_GAME_TEST result is inferred from deployment. Stop for the combined session above.
