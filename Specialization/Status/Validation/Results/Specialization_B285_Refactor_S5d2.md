# B285.312 — S5d2 namespace signatures and indexed retirement

Basisb022ef8. Behavior-neutral infrastructure; not full S5d. No deployment/main/native PASS.

## Runtime Impact Contract

TargetHook identifies the native Events/GameEvents namespace through RuntimeComposition.Native, including captured startup facades. Exact verified city signatures remain scalar; OnDistrictConstructed's district type is never a city ID. Unknown GameEvents names do not inherit Events layouts. Assignment uses cityOwner owner scope and a distinct governorOwner scope; establishment can narrow the receiving city but still notifies a different governor owner. Each owner is independently protected so one failing callback cannot suppress the other. Diagnostic errors cannot block the new adapter.

Verified source references: HD Gameplay/RegionalYields.lua259–261 BuildingPillageStateChanged(owner,city,building,state),265 DistrictRemovedFromMap(owner,district,city,x,y,type); Misc.lua164 CityBuilt(owner,city,x,y),645 OnPillage(actor,unit,improvement,building,district,plot); Boosts.lua666–680 derives victim owner from plot. Original UI GovernorPanel679–684 confirms third governorOwner; PlotInfo855–859 uses CityTileOwnershipChanged(owner,city). Building coordinates resolve district:GetCity before center lookup. Unreadable plot/owner stays UNKNOWN fallback; never assumes actor is victim.

RuntimeRetirement is an explicit composition entry before its seven actual consumers. Their historical relative Start order is unchanged. Startup failure skips only dependents, while Bridge remains independent. A failed consumer cannot own/quarantine the shared reset/removal hooks. One owner:city index points to tag/location/stamp scalars; removal visits only matching entries and deletes a clean marker only when its stamp still matches. Reused locations replace old reverse entries. Load clears both cache/index. Existing≤2048/tag caches, current3tags and≤8192scalar index slots are bounded; no native reads during invalidation or new timer/frame/poll/persistent state. Exact failed cleanup still cannot publish a clean marker. Native ID-only removal is an invalidation cause, not ownership/exit proof.

## Evidence

LOCAL_SIMULATION_PASS:15 new cases cover distinct namespace and wrapped facade identity, exact Gameplay building/city versus owner-only district completion, unknown namespace fallback, dual-owner assignment/establishment and first-owner callback failure, transfer without guessed former city ID, actor/victim and unreadable plot, district building coordinates/internal-carrier filter,20consumers with exactly one removal/reset listener, unrelated city zero cleanup, reused location/stale index guard, failed cleanup/load reset, downstream failure independence and actual owner late-start failure/dependency quarantine.

Full232 selected cases:231 properties PASS, strict T03 warm D capacity OPEN for S6; no failures/errors/unexpected/widened alarms.194Lua5.1/25XML/exact316package/modinfo312 pass. Two inherited current test adapters had aliased Events=GameEvents; that invalid native double caused false fallback/internal-trigger work under correct namespace handling. The explicit separate_legacy_event_namespaces fixture profile separates callback storage before runtime construction; frozen historical source and exact assertions remain unchanged, profile is included in closure. Existing strict investment city-scan and sibling-retention assertions pass.

GovernorChanged investigation (INFERRED): nine actual Hook/TargetHook subscriptions count dispatch before qualification; B271 callback totals387=9×43 and396=9×44 fit callback multiplication. The400-entry C trace truncates and payload is UNKNOWN, so this does not prove43/44 independent state changes or complete delivery frequency. Remaining S5d will reduce redundant subscriptions; no frequency claim is closed here. Governor Property readiness relative to publish, district repair delivery and hidden context ordering remain USER_GAME_TEST_REQUIRED.

## Handoff

User decision: none. User testing: final U5 unless a concrete native fact blocks safe work. Primary next: independent Dialogue hooks/work facts and exact carrier recovery before old relay retirement, then remaining S5d/S6–S10. Stable/main/live B271.298 unchanged.
