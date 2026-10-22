# B216 — Partial native evidence and PLACES activity stop

State: USER_GAME_TEST_FAIL (PLACES start); Tourism native tooltip confirmed, settlement/update UNKNOWN. Documentation/evidence only; no repair, deployment or next implementation authorization.

## Reviewed evidence

Three images were read individually and moved unchanged to the ignored local B216 evidence directory. SHA256 verified before/after; local manifest retains exact filenames. Raw images/logs remain unpublished.

- Image 1: SHA256 `b9ae169c4ed8fc9108fba6f0ff6876ac560b15762bcc487285bed3f83edc92eb`.
- Image 2: SHA256 `1754da43de023ed090bde784618bc77052f78981b779ce4626407002b8f4fae9`.
- Image 3: SHA256 `773dd728154cf32de436798d71d6c45335efc199449b3ba5e491285eeb269356`.

Image2 shows the native Tourism lens tooltip for Christ the Redeemer: base +5 Tourism and +4% towards the listed civilizations that reached Ancient era. This confirms the modifier appears on a non-Great-Work source in native UI, beyond our configured readout. It does not establish fractional accumulation, exact settlement, every source type or dynamic replacement after another Insight. User explicitly defers rounding/fractional behavior and further Tourism update observation; no fix requested.

Images1/3 show process memory10.69GB and11.20GB. Retain as user-requested observations only; no attribution, performance investigation or new gate. WORKS has no eligible target and remains untested.

Collector session: `local/diagnostics/B205/session-20261017T045627Z-c71286/`. INTERRUPTED;4 training/context records and6 Gate lines. Five PARTIAL_FRAME_AT_DEADLINE events constrain completeness. Summary `alerts: none` is not absence of gameplay errors. No INSIGHT/Tourism record or completed mission appears in the captured lines.

## Confirmed failure sequence (UTC)

- 04:59:31: READ, owner0/unit1441792, ARRIVED.
- 05:09:07: READ, same unit, ARRIVED.
- 05:09:09: TASK → TASK_PREPARING, error=nil.
- 05:09:10: ACTIVITY_READBACK_STOP with ACTIVITY_POSITION_CHANGED; ACTIVITY → HELD.
- 05:10:31: READ remains HELD. A READ error=nil does not clear the held phase.

User identifies this task as 奇观巡礼 (PLACES); the captured generic TASK line does not itself encode category. It stopped at activity preparation before sleep confirmation/timer start, not at Tourism reward settlement. Loading and an arrived team are observed; source/cap restoration from the deliberately saved travel state is not independently established by these sparse lines.

## Direct source trace and confidence

STATIC_CONFIRMED: `Mod/ExpeditionSpyGate.lua` relocate calls PlaceUnit and immediately verifies Gameplay coordinates; TASK stores those coordinates and publishes them to the activity mirror. `Mod/UI/ExpeditionSpyActivity.lua` read requires exact identity/name and then exact UI coordinates; mismatch raises ACTIVITY_POSITION_CHANGED before reading activity/requesting SLEEP. Failure acknowledgement places the Gate in HELD. The task timer starts only after ASLEEP.

Confirmed: UI position disagreed with the published expected position after Gameplay's placement check succeeded. Unknown: actual/expected coordinate values and whether the discrepancy was transient UI replication lag, a subsequent native move, or another publication/placement boundary. Do not label async lag as a proven engine cause. PEOPLE commonly stays at the city centre; its success does not cover off-centre wonder/building placement. WORKS can encounter the same shared boundary, but no native failure is claimed for it.

## Proposed next narrow repair (approval required)

Reproduce differing Gameplay/UI position timing in an isolated actual-module fixture before editing. Capture expected versus actual positions with task identity, phase and bounded elapsed time. If confirmed as initial placement visibility, allow only that task's pre-SLEEP position convergence within the existing bounded handshake deadline; never start the timer or request SLEEP until exact identity and position agree. Persistent mismatch still stops with useful evidence; wrong owner/unit/name and unexpected displacement during a running task remain failures. Cover initial lag, convergence, timeout, stale attempt and ongoing-task displacement locally. No blanket removal of position protection, new persistent fields or changes to capacity/binding/timing/rewards.

Native follow-up would retry one available 奇观巡礼 through preparation, completion and return; observe Tourism updates if it earns a new Insight. No separate performance/rounding test, and no requirement to manufacture WORKS targets. This proposal is not implementation authorization.
