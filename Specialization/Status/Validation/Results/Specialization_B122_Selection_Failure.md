# B122.149 — automatic selection start failed

Evidence: USER_GAME_TEST_FAIL for the automatic entry. Runtime remains B122.149 / modinfo149; no repair or deployment in this review. B121 normal-cycle scoped PASS is unchanged.

## Native observations

1. 20:39:28, T21: production list offers the experimental project with `1*`; this is a prospective display, not an accepted timer.
2. 20:39:48, T21: after selection, production row, city banner and bottom city panel show 未启动. The new display adapters are reached, but active timing and ordinary-production restoration have not passed.
3. 20:43:17, T21, user-reported reload/retry: project tooltip says 本批项目必须为唯一当前目标，不能排队计时. This is the selection controller's queue-size rejection. The P0 panel is displaying unrelated default research information, not a timer diagnostic. No numeric queue size is captured.

User additionally reports no completion after advancing the turn; there is no next-turn screenshot in this submission. Do not classify this as FinishProgress failure: no accepted timer is demonstrated.

## Static and local findings

`TimedProjectSelection.Pulse` permanently clears its pending selection when the project hash matches but queue size differs from 1. It sends no begin request. A targeted existing-fixture reproduction with target=project,size=0, then size=1 gives ERROR, zero requests, nil Gameplay timer. This proves a code vulnerability to an intermediate queue snapshot, not that the engine produced size=0 in these screenshots. A real size greater than 1 is another possibility; the current diagnostic omits that value.

Recreating the UI selection controller leaves the previous ExposedMembers selection ERROR untouched in the fixture. This can explain stale presentation if the field survives an in-session reload; actual native persistence is not established by the fixture. Reload itself must not silently resume a session-only timer.

The original B122 tests assume a coherent target/size=1 snapshot at selection. They did not cover the intermediate 0→1 sequence. No available Lua.log was located under the external workspace during this review; there is no logged native ordering proof.

## Next repair scope — requires authorization

Separate unconfirmed/transitional queue reads from a confirmed incompatible queue; keep event-driven, bounded waiting and one begin request. Include the observed queue size and rejection stage in concise diagnostics. Clear or scope stale UI-only selection presentation on initialization without restarting gameplay on load. Preserve exact-project/owner guards, single-city and session-only boundaries, no rewards, and existing completion behavior. Add targeted ordering/reload tests; do not weaken a genuine multi-item queue rejection by guessing.

User testing is paused pending repair; no repeat of the failing sequence requested now. Claim/F remain closed.

## Archived screenshots

External directory: `Specialization/Status/Validation/Evidence/B122_Project_Selection_20260928/` under the configured legacy workspace. Originals moved after visual review; SHA256 verified unchanged.

| Original filename | SHA256 |
|---|---|
| Screenshot 2026-09-28 at 8.39.28 PM.png | `11b00bb5d12e7e3b820a0e9f3a50384f56ab446c905034c9860deef896b04f56` |
| Screenshot 2026-09-28 at 8.39.48 PM.png | `f0f0f8dc8b4518fec589b2a42bbcb641d47726a2a816fd06cf8481eb6ead4010` |
| Screenshot 2026-09-28 at 8.43.17 PM.png | `70c7f8d159542f70aacda507b688565c76bbd45f3880d2f32adedb3d72113615` |
