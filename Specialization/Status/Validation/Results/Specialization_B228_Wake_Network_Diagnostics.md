# B228 — Native wake alignment and Culture Network waiting diagnostics

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B228.255 / modinfo255. Verified deployment recorded below; native acceptance remains pending.

## Authorized scope and findings

User authorized the two narrow investigations/fixes following the B227 collector repair. No new timer, forced native action, task rule, capacity/source/history/schema, GC or unrelated network rewrite.

B227 native follow-up: [collector and submitted evidence](Specialization_B227_Collector_Native_Followup.md). Redispatch followed by ARMED/ASLEEP/completion/release succeeds; recurring native eligibility failure remains. A persistent global lock is not the leading explanation. The post-release AWAKE/Skip-denied/Sleep-denied/Wake-allowed signature is retained as evidence, not an inferred engine cause.

STATIC_CONFIRMED: installed Civ VI Base `Assets/UI/Panels/UnitPanel.lua` generic command enabled check (line471) uses CanStartCommand(unit,hash,false,true). The existing Mod UnitPanel adapter uses the same shape. The Activity release bridge omitted the final result-request argument. B228 aligns it. This signature difference alone does not establish a permission difference in the native engine or prove the recurring fault fixed.

## Changes and boundaries

- Activity: align the WAKE query and record ACTIVITY_WAKE_REQUEST immediately before its one allowed request. Ownership, exact team/key/position checks, later-event readback, ambiguous-write protection and clean pre-request rejection remain. An awake unit is not forcibly woken merely because another native query allows Wake. No automatic redispatch, retries or global UI reset.
- Existing bounded diagnostic ring: IDLE_UI after arrival/load/release, ACTIVITY_START/FAILURE/RELEASE and WAKE_REQUEST add optional IsReadyToSelect and native Wake visibility/eligibility, including the old argument shape as an observation only. IDLE_UI also reads Sleep visibility/eligibility. Missing/throwing APIs remain UNAVAILABLE/READ_ERROR. No new listener, timer, scan, persistent state or authorization from diagnostic fields. Existing budget/ring caps remain.
- CultureNetwork.Describe: distinguish CITY, MODULE, NETWORK, NO_RECORD and CURRENT_FACTS failure layers. Show a concise Chinese reason and input/derived revision. Emit bounded NETWORK_WAIT and NETWORK_INPUT lines through the already allowlisted collector, including validity, availability, revalidation and retained bridge error. Extract only bounded error codes; never print arbitrary errors/paths. Reporting reads retained state, never Refresh, topology reconstruction, carrier writes or a new network bucket.
- The current waiting message did not prove missing topology: it also covered city/carrier errors and worker/reference reads. Network production/qualification remains unchanged. A full foreign civilization still requires PEOPLE+WORKS+PLACES; incomplete history ordinarily yields zero, not a generic waiting error.

## Local verification

246 targeted offline tests PASS: actual Activity UI, pending/integration/recovery/failure/diagnostic paths, B227 event differential tests, retained trace, Culture Network projection and reader/collector. Eight new B228 tests cover argument-sensitive wake, denied wake protection, legacy/current diagnostics, no speculative wake, specific network layer/input reporting, absent bucket without mutation, privacy and collector acceptance. No live socket/game execution.

The broader initial network suite encountered its existing package-version assertion pinned to253 (already stale at B227). It is not rewritten to manufacture a PASS; runtime packaging is checked by current context integrity. No gameplay assertion failed in the final targeted set. Native eligibility, readiness and Culture Network yield remain user gates.

## Minimal next native evidence

Start the existing collector manually. One ordinary task → completion → another task or relocation is sufficient; if a rejection appears, stop repeated clicks and retain the log. The new fields distinguish old/current Wake eligibility and actual readiness at the existing lifecycle boundaries. Do not repeat saved-state/old long tests.

For the affected culture city, open the existing **文化见闻** report once while the network says waiting. NETWORK_WAIT identifies the failing layer; NETWORK_INPUT records whether topology input is absent, stale or verified. A screenshot is optional unless UI layout itself is wrong. No claim that the network bonus is repaired before this reason is known.

User decision: none for this approved batch. Primary next: review the resulting bounded records; no speculative native recovery or network-rule change.

## Verified deployment

B228.255/modinfo255 DEVELOP_ACTIVE; source 5cacaa03d4e9b4e3c522a10ea3d840f4458371dd; receipt B228.255-5cacaa0-playtest.json;226/226 MATCH, digest b37790789f0f6b6510bdb59f6c5cb06603c7f4fc70eac58a28e001203c942ad6. Automatic game-exit checks at both guarded switches; B227/stable recovery retained, no pending transaction. No main/configuration changes or game launch.
