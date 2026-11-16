# B282.309 — S5c1 scoped D providers and official signal ownership

Basis9a42016. First S5c slice complete, not full S5c/d. No gameplay/save change, deployment or native PASS.

## Runtime Impact Contract

DistrictCompleteness normalizes the verified player/district/city payload once for added/progress/pillage/repair; both cache invalidation and typed D consumer scheduling retain that scope. Known city marking is one cache lookup; owner/unknown fallback remains a bounded scalar pass over the existing≤8entries. Foreign owners return before work. Transfer uses the receiving city only for its receiving owner and the former-owner fallback separately, never reuses the new city ID as the old owner's ID. Building added/removed retains the reviewed fourth owner argument and SPC-carrier filter. Unresolved removal/pillage/repair forms retain bounded fallback rather than guessed city IDs. Recapture marks the matching city when supplied. Larger working-set capacity is S6.

A monotonically changing per-entry invalidation ticket is sampled before capture and checked after final native reference reads. A mid-capture or final-getter change cannot overwrite dirty state with an older successful sample. No successful D event is emitted merely because a consumer reads/materializes the cache, avoiding self-audit loops. Existing failed capture/last value availability semantics remain intact; a new relevant mark recaptures, not an idle publication retry.

DistrictCompleteness.RegisterConsumer and NetworkBridge.RegisterConsumer delegate to the one existing FactChanges registry. Central binding declarations route D/NETWORK kinds through their provider, retain other kinds through the original registry, and coalesce duplicate row collection before execution. RuntimeComposition quarantines both facades as well as their underlying registry after failed startup. Unknown-owner D input increments a fixed scalar global Commerce authority epoch before deferred callbacks; no native lookup is needed to deny stale proofs. Global full-Audit fallback dominates its contained known owner/city Audits, while city-only methods preserve narrow work they can actually perform.

Bridge is the sole production writer of the compatibility RouteSignalRevision projection, including all existing live route/unit-operation/city/war triggers and the original foreign-unit/confirmed non-trader filtering. TradeRouteProbe remains diagnostic/read-only with respect to signals. Exact startup order is unchanged; diagnostic failure no longer falsely skips the official bridge. The two B271-observed absent GameEvents CityConquered/TradeRoutePlundered are not added as new official hooks: existing live CityTransfered/TradeRouteRemovedFromMap already signal those changes. This is removal of non-delivering dependencies, not a new native delivery assertion. No event/timer/frame/scan/persistent structure is introduced.

**Transitional overlap:** several real D writers still have their older native event callbacks in addition to the new typed D provider. This slice does not claim one Audit per native cause. S5d must migrate those hooks/consumer scopes before the integrated candidate; no transitional build is deployed. Busy Refresh/Receive/confirmed-negative merging is S5c2, explicitly not closed here.

## Evidence

**LOCAL_SIMULATION_PASS:**14 new Lua51 cases cover same-city invalidation/scheduling, zero native dirty work, unrelated warm sibling reuse, foreign-zero/malformed fallback, transfer owner scope, both mid-capture and final-reference tickets, warm building pillage/repair, same-turn second change, SPC-carrier filter, callback reentry/new snapshot, sibling exception/1000idle no retry, failed-start quarantine, global transaction epoch/global Audit dominance and narrow-city preservation. Actual Bridge without TradeRouteProbe proves sole signal ownership, complete tested live trigger union, non-trader/foreign filtering and transaction staleness; starting the actual diagnostic cannot reset or double-increment signals. Real composition proves diagnostic failure does not skip Bridge.

Unchanged strict T02 plus the independent provider/scope tests passed before its counterexample entry was retired with evidence; old B272 evidence remains frozen. Full selected181cases:179 properties PASS/2 strict laterOPEN (S5d Chair scope, S6 capacity), [closure](Specialization_B282_Refactor_S5c1_Closure.json). Package194 Lua51/25XML/316files+modinfo309; no new/widened static alarms. Legacy standalone test fixtures need no new import or weaker assertion.

- **User decision:** none.
- **User testing:** final U5 unless a concrete blocking native fact appears.
- **Primary next:** S5c2 busy/evidence merge→S5d→S6→S7/S8→S9/S10. Main/live remain B271.298.
