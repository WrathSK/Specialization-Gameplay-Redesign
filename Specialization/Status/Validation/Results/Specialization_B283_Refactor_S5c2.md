# B283.310 — S5c2 bounded Bridge busy work

Basis010c2f1. Completes S5c, not S5d or the program. Behavior-neutral infrastructure within accepted pending-network continuity. No deployment, native PASS, gameplay/save/GC change.

## Runtime Impact Contract

Per-owner private pending work retains the newest detached bounded wire packet, refresh request, FAILED/NATIVE evidence and union of exact source-reference/route negative proofs. Enqueue does not advance seen/accepted sequence. Wire fields are whitelisted scalars, Data≤16384bytes/Failure≤64, owner/negative collections≤2048; no native object, timer, frame callback or persistence. Busy Refresh, Receive validation and evidence causes merge rather than disappear. Source references, not reused city IDs alone, authorize negative projection.

The existing publish boundary drains one snapshot and runs normal epoch/turn/signal/current-owner/current-count validation at processing. Actual new reentry belongs to the next snapshot. One urgent negative attempt follows the outer refresh; no recursive positive resample loop. Exceptions always release busy/receive flags. Failed negative projection retains the entire unprocessed batch, including wire/refresh causes, dormant and transaction-ineligible until a real new cause. An idle boundary never rearms it. FAILED full-read evidence cannot allocate another UI request budget; a new native cause can. Negative-only projection remains available for withdrawal while unrelated UNKNOWN facts preserve continuity. Store's existing unfinished-exit proof/retry policy is unchanged.

Queued/failed-negative proof masks network effect/transaction availability and advances the scalar proof guard immediately. Actual Commerce Audit cannot calculate a positive replacement against stale topology; confirmed ineligibility/negative continuity still has priority. Capital sources likewise require current strict proof. ExperimentalStop clears this owner's new transient work so isolation cannot cause later publication/dispatch.

## Namespace correction to B282

B282's statement that B271 observed absent GameEvents.CityConquered/TradeRoutePlundered was incorrect. The measured absent list is Events.*, not GameEvents.* (B271 diagnostic catalogue and raw TRAIN sequence210/380). Existing optional GameEvents hooks moved from TradeRouteProbe are restored in Bridge. HD Gameplay/Misc.lua767–770 establishes GameEvents.CityConquered(newOwner,oldOwner,newCity,x,y); GameEvents.TradeRoutePlundered delivery remains UNKNOWN. This preserves the prior guarded subscription, not a new delivery claim. Frozen B282 report is not rewritten. The bare-name static scanner's two restored signal alarms are individually reviewed in refactor_selection, with exact namespace/provenance and tests, not globally suppressed.

OnPillage's first player is the acting unit owner (HD Misc.lua645/Boosts.lua666–680), not necessarily the victim. DistrictCompleteness retains bounded unknown-victim fallback rather than discarding a foreign actor's possible local damage. Scope refinement requires a verified plot resolver in S5d.

## Evidence

LOCAL_SIMULATION_PASS:20 new actual Bridge/Commerce/Sender cases. Latest detached packet/normal validation/no early ACK; sender IN_FLIGHT until receipt; bounded refresh union; real reentry survives a second boundary; rejected replay/oversize/object payload; stale turn/signal; capture errors; confirmed source and trader loss priority; failed negative plus wire/refresh survives; no busy flag latch; mixed confirmed loss/UNKNOWN; actual Commerce Audit holds old gold; FAILED/NATIVE order; exact GameEvents signal union; foreign pillage actor; isolation.1000idle boundaries add zero capture/negative retry or UI request in their respective scenarios.

Full201 selected cases:199 passing properties, strict T01 consumer-city-scope and T03 warm-capacity counterexamples remain OPEN for S5d/S6. No failures/errors/unexpected. Existing assertions unchanged. Static194 Lua5.1,25 XML, exact316 package references and modinfo310 pass; context/publication gates recorded by closure. Raw native event delivery, hidden-context ordering and real engine economics remain USER_GAME_TEST_REQUIRED. No partial/native scenario extrapolation.

## Handoff

User decision: none. User testing: final U5 unless a concrete native fact blocks further safe work. Primary next: S5d scopes/live hooks/Dialogue independence and indexed invalidation, then S6–S10. Stable/main/live remain B271.298.
