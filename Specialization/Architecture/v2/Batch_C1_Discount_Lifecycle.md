# Architecture v2 C1 — Standardization Discount request / sample lifecycle

Document Owner: Codex
Build: develop B073.100 / modinfo100
Design: D0025 unchanged
State: LOCAL_SIMULATION_PASS; not deployed; user runtime verification not performed
Scope: original Batch C, Discount sub-batch only. No parallel memory-fix roadmap.

## Mainline and evidence

A complete → B complete → C1 implemented/local regression → D1 pending → C2 pending → D2 pending → E deferred.
C1/C2 split original C (sample protocol); D1/D2 split original D (direct dirty consumers). C1 does not complete all of C. D1 is Discount scan scheduling / Network facts reuse; C2 remaining Copy/Industry/collection protocols, D2 remaining consumer fan-out; detailed scope needs separate authorization.

55GB, HD toggle, approximately59 Discount entries/sec and C² reads remain runtime evidence. Not a proven memory cause. First-turn `inflight=1`/send_inflight counters were NetworkSender counters, not Discount; they do not prove Discount request backlog. Old UI code independently shows unbounded-by-ACK initialization retries and eligibility seq advancement whenever ACK lags. C1 fixes this contract without claiming the runtime incident solved.

## Before

UI Publish/Playback/Turn/sample-init pulses scan the plan, build rows and compare signature only afterwards. `signature != sent OR ACK != seq` sends a new sequence, so pending is not a send barrier. INIT has a synchronous busy guard but no asynchronous pending. Gameplay Receive runs Audit, drops old sample, validates the packet, then runs Audit again. Turn mismatch, failed candidate or invalid packet can produce empty desired effects. `busy` only covers the synchronous stack.

## After: request owner and response

UI/DiscountEligibility owns exactly one logical pending request, one last acknowledged signature and one retry budget. INIT and ELIGIBILITY use the same barrier. Install pending and the latest issued identity BEFORE calling RequestPlayerOperation. Calls while pending only check fixed fields/counters/ACK/deadline; they do not resample or send. Existing non-pending scanning triggers remain (D1).

Packet identity: ClientEpoch + Gameplay Generation + Seq; eligibility also includes Plan Revision, Turn, complete Count/Data/Valid. UI context init, LoadScreenClose or observed Gameplay generation change retires pending and creates a new client epoch. No protocol state is saved to Property. Shutdown invalidates issued identity and removes this UI's listeners/timer.

Gameplay owns one bounded response per player. It checks current issued identity, current epoch/generation and monotonic response sequence before processing. Exact ACK match clears UI pending; duplicate/older/client-stale delivery cannot apply or overwrite a newer ACK. Fully valid same-content rows update receipt freshness but do not publish/apply another sample. INIT ACK or generation transition completes initialization; late old INIT cannot initialize a new load.

Timeout is5 seconds of UI dt, or next game-turn opportunity if this empty context does not receive dt. Timer only increments a scalar; no timer I/O/scans/requests. Same logical signature has max3 API invocations (initial+2 retries). Unknown/failed ACK also consumes this budget. A new turn/revision/content or epoch can begin a new logical request; repeated pulses alone cannot reset budget. Exhaustion stops sends until a changed request. This does not promise a5s wall-clock retry in native contexts with no dt callbacks.

A timeout cannot cancel an already queued native engine request. It retires its issued identity, so late delivery is rejected; at most3 native invocations per unchanged request may exist. Thus one logical pending is not an assertion that the engine queue supports cancellation. No queue history retained.

## Sample and withdrawal owner

StandardizationDiscount keeps the last fully validated permission rows and city reference (owner/id/coordinates). Validation parses into temporary bounded-by-current-plan rows and checks all target entries before replacing accepted sample. Partial/invalid/unavailable/stale packets do not clear it. Old turn is not itself evidence of invalid qualification. No permanent data schema changes.

Candidate-read failure retains the previous city plan only when its reference still matches. Known source absent/transferred, ACTIVE0, non-Industry identity, verified empty source set, or Network CONFIRMED_INVALID produces an actual reduction. Known false native Gold permission rows withdraw. Removed target/reference retires old permission entries; restoring topology does not resurrect retired permission before fresh native verification. Counter discount_withdraw counts actual carrier removals, not one semantic source-loss event.

On load accepted samples/responses/plans/pending are discarded. Existing native carriers are held only as temporary projections while facts are unavailable. With a confirmed plan but no sample yet, reconcile preserves only already-present still-planned entries (at the current level), removes confirmed-invalid entries and does not grant new entries from the absence of permission data. Fresh sample takes over. This avoids load unknown→zero→restore without storing old samples as authority. Indefinite native unavailability remains a visible degraded state; C1 does not fabricate failure evidence to force zero.

The existing pre-Audit and accepted-changed post-Audit stay. Duplicate/rejected packets skip unnecessary final apply. Generic Publish/Playback listeners, candidate loops, catalog checks, per-city Network Refresh/Capture and approximately59/s entry frequency are NOT optimized here.

## Fixed counters

Added discount_attempt (refresh entries), discount_send (actual RequestPlayerOperation invocations including throwing calls), discount_pending, discount_ack, discount_retry, discount_timeout, discount_receive, discount_duplicate, discount_stale, discount_apply (accepted changed samples), discount_withdraw (actual removals). Existing fixed turn/total/peak storage and manual report; no per-event print/disk/history added. These are separate from NetworkSender counters. The prior automatic audit FILE_API_UNAVAILABLE limitation is unchanged; no new file logging claim.

## Local validation

Run DevelopmentTests/test_arch_v2_c1.py with Lupa lua55. Actual production UI/Gameplay/Counters, mocked engine/transport. No game process or external DB required.

- INIT100000 repeated pulses:1 actual send; eligibility100000 pending pulses:1 actual send; combined2 sends, no extra sends until response/timeout. Test leaves existing Gameplay Audit pulses active.
- Same content / duplicate sequence do not repeat accepted sample application or carrier writes.
- Unavailable network/ACTIVE/native permissions, stale turn and malformed partial packets retain verified effects.
- Confirmed permission false and network invalidation remove affected carriers once; repeated invalidation no writes.
- Old client/epoch, out-of-order, expired and shutdown deliveries rejected; timeout/failure capped3 invocations.
- Load with existing valid carriers does not clear; confirmed loss still withdraws; source restored requires fresh retired permission.
-12 normal verified level1–4/permission true-false-true cases,4 cities each, match B071 actual Discount Lua from Git407717c. Intentional transient semantics differ and are separately tested.
- A/B/B069 and runtime audit ON/OFF regression retained via historical version-only wrapper:168 three-way Network outputs,9 transient cases,24 A comparisons; warm Discount derive0, cold1;102 Audits retain1 derive/408hits. All Lua syntax and XML references pass.

Native callback order/ExposedMembers visibility/timeout cadence require eventual user validation; no test or deployment requested this batch. Local regression does not establish USER_GAME_TEST_PASS or resolve55GB.

## D1 next (not started)

Move no-op checks before scans, make one fact capture available to a Discount batch, replace generic audit work with dependency-aware dirty drains and bounded reconciliation. Preserve real qualifier events. Do not confuse fewer derives from B with fewer Capture calls; current C² remains. C1 provides the transport/sample prerequisite, so D1 is the recommended next authorized sub-batch.
