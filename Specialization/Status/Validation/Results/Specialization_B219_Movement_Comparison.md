# B219 — Ordinary Spy / Expedition movement comparison

State: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B219.246/modinfo246. W0003 deployment is verified below. This is the user-authorized minimal comparison following [B218 native evidence](Specialization_B218_Native_Review.md), not a repair of mission placement.

## Exact scope

Compare `PlaceUnit` and `MoveUnit` using an existing idle ordinary Spy or the exact bound idle Expedition, against the same civilian-occupied land plot in a disposable saved world. Do not run native espionage missions, replace units, clear other units, retry placement, accept a neighboring plot as mission success, or award/replay Insights. No timers or polling. Capacity, source binding, permanent records, training costs, GC, Design, main and game configuration are unchanged.

Ordinary native travel/mission operation coexistence is separate evidence. This experiment tests generic movement primitives only; it does not claim to implement an engine Spy operation. A positive adjacent MoveUnit result will not establish arbitrary-distance movement or permission to replace the formal transport path.

## Implementation and ownership

- `Mod/ExpeditionMovementProbe.lua`: default-inactive explicit request handler. Revalidates selected identity/type/name/position/current-turn idle sample, supported player, revealed land target, a non-Spy civilian occupant and a deterministic empty adjacent pad. Targets containing another Spy are rejected so the test subject cannot change the comparison's occupancy condition. At most eight target occupants are read; unreadable or oversized sets stop before movement.
- The existing Gate exposes an exact read-only idle-binding check and an in-memory experiment lock. Admission requires CREATED/ARRIVED, no owned/pending task activity and a reliable source reference. A HELD or travelling team is not silently repaired/adopted. The lock suspends formal Gate requests, turns and transfer handling until reload, without saving the deliberately changed coordinates. Training and capacity readers retain their original saved record. Do not continue playing or save the experiment state.
- Before the tested call, `PlaceUnit` stages the selected unit on a deterministic **empty adjacent pad** and verifies exact readback, unchanged identity and unchanged target occupants. This setup call is logged separately. Both methods then receive the same one-tile geometry with restored native movement. A setup failure consumes the trial and never reaches the candidate. This avoids treating long-distance pathfinding failure as an occupancy result.
- Exactly one candidate call per load. Immediate outcome is EXACT / NOT_EXACT / STOP. There is no automatic return, corrective teleport or unit recreation. Returning to the original occupied centre would reuse the primitive under investigation and compromise the control. A request with an uncertain send outcome is not resent.
- One scalar diagnostic watch observes only the tested unit's UnitMoveComplete and UnitTeleported, capped at eight matching events; turn/load/removal closes it. Critical immediate samples survive a synchronous event-limit closure. No permanent or growing history is introduced. UI publication/manual-read events contribute up to four fresh native position/Spy-operation/activity samples and never issue another movement request.
- `Mod/UI/ExpeditionMovementProbe.lua` / `.xml`: small separate comparison window. Right-click the existing P0 **人文考察·验证** button; the original left-click is unchanged. Select an existing unit before opening, hover the target and press **M**, then use **PlaceUnit 对照** or **MoveUnit 对照**. **读取结果（不重试）** reads only. Existing localization and collector channels are reused; no new asset, collector or configuration change.
- Package/Gameplay wiring and the current build assertion are updated. Formal `relocate`, mission rewards and activity confirmation are unchanged. Existing B218 conclusions remain frozen.

Logs use the existing collector's `[SPC][B191][N1_TASK] movementProbe=` records: BEGIN (kind, original/pad coordinates, source city/team, event availability), SUBJECT flags, PRE_STAGE/STAGED/PRE_CALL/POST_CALL, target occupants, unchanged-occupant check, actual move/teleport events, immediate RESULT and bounded UI_READ. Gameplay API gaps stay UNKNOWN; UI operation readback is recorded separately. Logs compare actual coordinates, never just a successful API return. No raw evidence is committed.

## Local validation

**219 targeted tests PASS**, including **22 new probe tests** with parameterized cases. Actual Gate/probe/UI Lua runs against isolated fixtures; existing mission/task/persistence/activity/relocation regression remains included. The configured external gameplay DB is read-only and copied in memory for existing SQL checks. Loaded definitions confirm ordinary Spy and Expedition both Spy1/Stackable1/CIVILIAN; this is not a native collision guarantee.

Coverage: both unit types and both primitives against the same pad/occupied target; no-op/offset/throw; setup offset/occupancy change; identity/type loss; unavailable native read/API; non-idle/unbound/stale source; duplicate token and second request; event bounds and late events; preserved per-value saved state and existing Insight record; unchanged capacity admission and no spawn/destroy/reward writes; actual UI marking, pinning, one-shot send, close/late reply, unknown-send no-retry, dynamic localization keys and package wiring. A malformed lifecycle is not made valid by the probe. Existing gameplay works without activating the experiment.

LOCAL_SIMULATION_PASS proves these control-flow/isolation assertions only. Native collision/operation behavior, keyboard routing and rendered UI remain USER_GAME_TEST_REQUIRED. No gameplay full regression, memory/stress test or game launch was run.

## One bounded native comparison session

Use the existing supported campaign's disposable test copy, with one **healthy idle bound Expedition**, one **idle on-map ordinary Spy**, and a revealed **civilian-occupied land tile containing neither test subject nor another Spy**. At least one neighboring land tile must be empty. Prefer the previously failing wonder plot if available. Save this unchanged preparation baseline once. Do not start missions or train another team for the comparison itself.

Start the existing collector manually from the develop root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/collect_expedition_trace.py --idle-exit 300
```

For each row below, load that same baseline, select the specified unit, open P0 and **right-click 人文考察·验证**. Hover the same occupied target and press **M**; click the indicated interface once. Wait for the result and normal event publication (or click **读取结果（不重试）**). Then load the baseline for the next row; do not save the moved state or end the turn. No restart is required by this test. The reloads control starting geometry/occupancy and avoid unsafe restoration; they are not a repeated save/load acceptance gate.

| Row | Subject | Button | New information |
|---|---|---|---|
| 1 | Ordinary Spy | PlaceUnit 对照 | Does generic placement offset a native Spy too? |
| 2 | Expedition | PlaceUnit 对照 | Same world/pad/occupants: ordinary vs custom type |
| 3 | Ordinary Spy | MoveUnit 对照 | Does the adjacent movement primitive differ for a native Spy? |
| 4 | Expedition | MoveUnit 对照 | Can that candidate place our exact unit without disturbing the occupant? |

If an ordinary/Expedition subject or a matching occupied destination is unavailable, stop with the available rows, not guessed equivalence. A preflight STOP means no candidate evidence; a post-staging STOP requires reload. If an occupant disappears/moves, an error occurs or an unexpected active operation appears, stop the session and retain logs. No forced retries. Logs normally suffice; one screenshot only if UI input/selection itself fails. After row4 reload the baseline and stop.

## Interpretation and stop

- Both PlaceUnit cases offset: supports a generic placement restriction, not a custom Spy-flag diagnosis by itself.
- Only Expedition offsets under identical input: a custom-type dependency remains; investigate exact differing flags/tags, do not copy them blindly.
- MoveUnit exact with unchanged occupants/identity and idle operation: a candidate for the separately authorized relocation repair, only over tested adjacent geometry.
- MoveUnit offsets/no-ops/activates an unintended operation or changes another unit: not a safe substitute. Preserve evidence and propose the next narrow decision.

User decision: none for this approved prototype. User testing: four controlled one-call rows, no turns or rewards. Primary next: inspect captured evidence, propose a repair only if justified, then stop. No formal movement replacement, N3, rounding or other development is authorized by a positive prototype.

## Deployment and completion checks

B219.246/modinfo246 DEVELOP_ACTIVE; source 7dede6ee777fa2db6568932900cb655369f9b17f; receipt B219.246-7dede6e-playtest.json;224/224 MATCH. Fresh automatic OS exit checks before both guarded switches; B218/stable recovery retained; no pending transaction, configuration or main change.

Context check PASS (224 runtime / 668 guarded context files), context self-test PASS,374 local document links/anchors checked without issues, diff review/check PASS and staged publication check PASS. Source commit `7dede6e`; documentation checkpoint follows separately. No native outcome is claimed by deployment.
