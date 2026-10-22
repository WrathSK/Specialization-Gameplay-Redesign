# B232 — Event-driven network proof recovery and Insight propagation

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source/live B232.259/modinfo259; verified deployment is recorded below.

## Approved boundary and cause

The user authorized shared network revalidation, coherent availability publication and recovery notification, explicitly requiring Culture Insight changes to notify the network. This batch changes no Design rule, Expedition task/activity/travel/capacity/source binding, reward/history schema, Research formula, GC, game configuration, deployment tool or main source. No timer or new frame callback is introduced.

[B231 native review](Specialization_B231_Native_Review.md) remains the original evidence: initialization/public reports and initial bonus work, then Gaul's third Insight is saved but the Culture projection remains held by NEEDS_REVALIDATION. Its raw logs and old actual-source counterexamples are unchanged. The first native invalidating event is not retrospectively identified; the following defects are STATIC_CONFIRMED and reproduced locally:

1. Gameplay can request route revalidation while the UI ignores the corresponding non-trader event. There was no explicit revalidation request to its collector.
2. Sender dedup suppresses equal route content even when new proof is required. Merely seeing a packet is not evidence that the packet was accepted.
3. Equal-input recovery did not notify consumers, and changed-input publication computed availability before committing its accepted candidate proof. Both can leave a correctly saved new Insight unprojected.

## Changed path and ownership

- `ExpeditionSpyGate` already calls `CultureNetwork.SourceChanged` after the successful Insight write. That writer/call site stays unchanged. SourceChanged retains its same-event scoped Audit and explicitly requests outstanding route proof when needed. With AVAILABLE topology, new history immediately updates dependent recipients without a topology scan or version change. Source history is not a route fingerprint.
- `NetworkBridge` marks route proof pending and calls the current UI collector's epoch/player-checked RequestRevalidation callback. The callback only marks existing dirty work; it performs no inline native scan or operation. Existing publish/playback/turn events flush it. The pre-existing SystemUpdateUI flush remains unchanged; it is not a new polling/recalculation mechanism. Multiple requests before a flush coalesce.
- `NetworkSender` sends equal content when route proof is pending, still using one in-flight packet, generation/turn/signal validation and the existing failed-turn limit. A disposable acceptedSeq distinguishes a successfully committed candidate from a merely received/rejected sequence. No Property or persistent field is added. Invalid equal-content acknowledgments cannot produce an unbounded same-turn resend loop.
- `NetworkBridge.Refresh` captures and derives first, commits the accepted proof, and then computes AVAILABLE versus pending. Unknown city facts still block availability. Equal logical input retains its version and derived view; a transition from pending to AVAILABLE notifies the existing six named consumers once. Repeated unchanged AVAILABLE refreshes do not notify. Confirmed losses still withdraw immediately, even if other facts are unreadable.
- Successful recovery makes Culture read the latest city-owned Insight history; it does not replay a stale payload. UI failure keeps the previous confirmed effects with explicit pending status. The existing three-read bound remains; the failure notification itself does not reset that budget. A later real event, including a new Insight, can request fresh proof.

Temporary state belongs to the existing UI collector/sender and Gameplay bridge epoch. Context shutdown/recreation discards it; isolation remains terminal for that session. Culture owns only its disposable projection, and Store remains the permanent history authority. No new queue, history revision, recurring task or global fact cache is introduced.

Files: `Mod/NetworkBridge.lua`, `Mod/NetworkSender.lua`, `Mod/UI/BackgroundRoutes.lua`, `Mod/CultureNetwork.lua`; package labels in `Mod/Probe.lua` and `Mod/SpecializationP0.modinfo`; the new targeted test and current contract/status/manifest/review metadata.

## Local validation

L3 scoped shared-infrastructure validation: **163 unittest tests PASS** (18 new B232 tests plus145 existing tests), and the existing B134 actual-bridge scope regression PASS. Local simulation is not native transport/yield/CPU/memory evidence.

The new suite runs the actual UI collector, sender, bridge and Culture writer with separate event registries and native mocks. It covers non-trader event propagation; immediate Insight updates; unchanged/changed proof recovery; all six consumer notifications; reentrant read safety; unknown city facts; burst coalescing; one-flight behavior; rejected packets; a new event between receipt and acknowledgment; bounded UI failure; owner/epoch/shutdown/isolation guards; callback failure; confirmed route loss; stale/partial input; derive failure; candidate expiry and read-only reports. Five malformed/stale packet subcases belong to one of the18 tests, not five additional tests.

Measured local deltas:12 dirty events before publication produce one UI route scan and one proof packet; equal-input proof recovery produces zero new topology derivations/version increments. An AVAILABLE Insight update scans no routes and reads only relevant source/recipient facts. Repeated unchanged refreshes write no new Culture carriers. These observations do not establish a native performance improvement.

Existing selected regressions include actual Gate completion notifying only after Insight success, source unions/UNKNOWN/exits/returns, initialization/public reports, bounded diagnostics, P0 callbacks and offline collector parsing. B134 preserves same-turn local changes, required foreign fallback/governor paths, confirmed owner/trader loss and new-context rejection of old packets, with no permanent writes.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<LOCAL_LUPA>:DevelopmentTests python3 -m unittest test_b232_network_revalidation test_b231_network_initialization_reports test_b230_culture_network_ready test_culture_network.Projection test_culture_network.GateIntegration test_b229_retained_diagnostics test_b228_native_network_diagnostics test_p0_panel_current_layout test_expedition_trace_reader test_expedition_trace_collector`. Additional script: `DevelopmentTests/test_b134_network_scope.py`. `<LOCAL_LUPA>` is the existing local Lupa dependency directory; this placeholder must be resolved before running.

The optional historical B137 isolation wrapper fails its first old-versus-current Culture III output comparison at line179. The same failure is reproduced using all runtime sources from pre-B232 HEAD `0ee4dc9`; current Culture rules have diverged from its `bb1bab3` baseline. It is not counted as PASS, and its historical assertions are unchanged. The prior B231 AV2-B wrapper limitation also remains recorded, not silently accepted or repaired here. No gameplay-wide regression or new save/load acceptance is claimed.

Changed Lua/Python syntax, modinfo XML and449 file references, current context/schema/selectors and496 links in the changed Markdown documents PASS. Status CURRENT remains8 lines (1315→1232 bytes); the N3 contract grows26→28 lines for the explicit recovery boundary. Staged publication safety and final diff review remain commit gates. Only named reviewed changed/new hashes are maintained. No raw logs/screenshots or frozen evidence are added or rewritten.

## One minimal native flow

Use the existing test campaign and manual collector; preserve the already accepted B231 initialization/initial-yield evidence. No repeated cold-load/END/re-enable lifecycle suite or new team is required.

1. Prefer an existing save just before the third Gaul Insight completes. Keep the known Culture source ACTIVE IV and its existing route/receiver unchanged. Let that one task finish through normal play, with P0 closed. The new uncertainty is whether a successful Insight actively reaches the current network and survives any pending route-proof recovery; no need to repeat all three missions.
2. Select the previously checked recipient and read **网络概况** once after completion. The distinct complete-civilization coefficient should increase1→2 (assuming no other source/eligibility change); W matching working specialists then contribute2×W Culture instead ofW. Check ordinary specialist Culture, and let the collector retain NETWORK_HEALTH/NETWORK_PUBLIC/NETWORK_CITY data. The report does not trigger recomputation. **网络来源 / 接收** is needed only if a route/recipient differs from expectation.
3. Advance through the next ordinary turn only if already continuing play; confirm the coefficient remains2 rather than returning to a persistent wait. This checks the ordinary event revalidation that preceded the B231 failure, without an extra mission or cold restart. If pending persists, keep the log and stop that path.

If no pre-completion save/eligible unfinished set is available, verify readiness with the existing complete sets and defer only the new-Insight delta to the next available task. Do not ask the user to manufacture another long sequence. Native engine yield requires the user's observation; logs report expected coefficients/writes and cannot independently prove native settlement.

User decision: none. User testing: the single network delta above. Primary next: review its logs/results and stop at B232; no speculative Expedition repair or later batch is authorized by this change.

## Deployment

B232.259/modinfo259 DEVELOP_ACTIVE; source a0e1d4ece94bac690c6a2018add37b96c37c145c; receipt B232.259-a0e1d4e-playtest.json;226/226 MATCH, digest 4830284febe3731cb9d0b0de0970613cf5358a9c98575934e163dc23a91036cb. Automatic game-exit checks before both guarded switches; B231/stable recovery retained, no pending transaction. Stable main B069.96 remains unchanged; no game launch or configuration change. Native gate remains pending.
