# B274.301 — S4a diagnosed local recovery paths

State: S4a_COMPLETE / S4b_AUTHORIZED; basis `612015a`. Approved S4 subset only, no deployment/main/native PASS.

## Runtime Impact Contract

- Great Work UI: per-city optional specialization signature reads are protected and encode UNKNOWN explicitly; real slot availability, reference protocol, whole-scope coverage and authoritative Gameplay facts stay unchanged. A bad specialization signature cannot poison another city's valid slot packet.
- IndustrySupport: distinguish producer changed/confirmed-unchanged proof from stale/rejected/unavailable delivery while preserving SampleLifecycle's first boolean API for other consumers. Generic publish may consume genuinely marked work once, never re-arm work because the previous attempt failed. Same-turn relevant native/permanent/sample facts can still retry. No new timer/native getter/scans or persistent fields.
- GC coordinator: UI_PENDING uses the existing one-retry same-turn deferral. Wait reads fixed public scalar pending/inflight flags only; heap/idle reevaluation occurs once at an existing publish boundary after blockers clear. Threshold/cooldown/locks/explicit GC policy unchanged; other skip reasons remain final for that turn.
- Housing: existing ReadFacts compact projection of the same D capture replaces detailed Read in business eligibility; same anchor/buildings/qualification/output. Diagnostic Describe remains separate.
- Gates: original S2 Industry/GreatWork/GC assertions, relevant-event recovery/no-progress budgets, invalid/duplicate/unchanged sample distinctions, all simultaneous UI blockers, foreign/turn/cooldown cancellation, current actual positive effect regressions, compilation/package references. Frozen evidence remains; older polling-dependent fixtures are explicitly superseded without weakening output assertions.
- Remaining scoped limitation: a getter silently becoming readable without any related event or source availability proof is not a recovery trigger. S5 declared propagation adds actual producer notifications; no periodic scan is introduced to guess recovery.

## Results

**LOCAL_SIMULATION_PASS:** three unchanged S2 gates now pass: Industry no-progress attempts20→0 on repeated publishes, GC UI pending→safe same-turn window, nil ACTIVE no longer aborting a valid two-city work packet.13 new cases test missing/nil/throwing signature service, true slot failure staying unknown, real Industry producer/receiver, duplicate/stale/unavailable versus availability-recovery proof, equal-value restore and second same-turn adjacency change, dormant failure versus a real governor event, failure/native event/sample reentry, multi-UI/network blockers,10,000 scalar-only waiting publishes, cancellation/other safety gates, and real compact D/Housing without any detailed read.

Full Lua5.1 program63 cases:57 passing properties/6 later OPEN counterexamples, zero unexpected. [Executed closure](Specialization_B274_Refactor_S4a_Closure.json) records exact source/test/backend scope.44 selected inherited methods and the actual positive-effect fixture bodies pass, including four B234 producer/commit cases. Older frozen B234 polling-only recovery and B138 no-UI-retry expectations are explicitly superseded by this approved contract; their source/assertions remain untouched and current successor cases preserve effect and safety assertions.

**STATIC_CONFIRMED:**192 Lua5.1 compilations,25 XML parses and exact314-file modinfo301 package pass. No new package file or SQL/save schema/formula changes. SampleLifecycle first boolean meaning remains; additional outcome metadata is read by Industry only. Client same-value availability recovery is explicit Industry opt-in; other consumers retain prior behavior.

Industry keeps separate dormant failures, armed city causes, coalesced scalar busy scopes (maximum2048, diagnostic overflow, no broadened fallback) and player sample causes. A failed attempt cannot arm itself. A genuinely new native event/sample arriving inside an active visit survives until an existing publish drain; no native city/player object, timer or arbitrary pending retry is added. Real same-turn changes still apply. Unknown sample/history is not zero. GC thresholds/cooldown/failure locks and non-retryable blockers remain.

Remaining limitation: silent getter readability recovery without any related event or availability notification remains unobservable. It stays diagnosable/pending; current relevant event/sample recovery works. S5 producer propagation must expose actual availability transitions where available; it must not invent a timer. This does not block the scoped network work.

**USER_GAME_TEST_REQUIRED:** native recovery frequency, treasury timing and final integration still need user evidence at U5. No new native PASS, game launch, deployment or main action. S4 network hold/provenance/cold-load changes are not claimed complete here.

## Handoff

- **User decision:** none for normal continuation.
- **User testing:** none now; U5 or a concrete blocking native fact only.
- **Primary next:** S4b network proof/provenance, all three actual network writers, confirmed exits and recovery; then internal U2 checkpoint and separate approved eight-era correction. No automatic deployment.
