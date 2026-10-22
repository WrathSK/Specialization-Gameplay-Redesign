# B192 — startup diagnostic received; failure-time state still unknown

**USER_GAME_TEST evidence received for the diagnostic display; task still FAIL / HELD.** Both T88 screenshots were visually reviewed. The user could not identify the requested button, but both images visibly contain the full-width **④ 无奖励任务（2回合）** above the report. **启动时活动诊断** is a report heading, not a separate button. The first image already supplies the requested startup sample; no repeat of B192 is needed.

## Observed values

| Field | First screenshot |
|---|---|
| Actual startup activity | 1797587246 (number) |
| AWAKE / HOLD | 1797587246 / 75236491 (number) |
| SLEEP / OPERATION | 38434027 / 1225574625 (number) |
| IsReadyToMove | true (boolean) |
| Native Spy operation / end turn | -1 / 0 (number) |
| Native SLEEP Hash | -41338758 (number) |
| Diagnostic CanStartOperation | true (boolean), displayed 允许 |
| Reported task error | ACTIVITY_UNEXPECTED_STATE |

The same report confirms current unit/name/source match, own capacity1/1 and original Edinburgh(Test) sourcecity393220. Created ID3276829 versus tracked/visible3342365 remains recorded; name 艾莉森 matches. Screenshot2 retains native capacity5→5, ordinary Spies0→0, completion events0 and the same activity error. These images do not demonstrate actual Sleep/readiness suppression, task completion or owned release.

## Important correction: startup sample is not the failing evaluation

[Bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) captures the startup sample only once per key, but evaluates the activity precondition again on later publications/pending polls. Therefore an initial AWAKE sample with native eligibility true can coexist with a later ACTIVITY_UNEXPECTED_STATE. The screenshot is not evidence that Lua compared two equal numbers incorrectly. It also does not establish whether RequestOperation was submitted before the eventual error.

This narrows an overstatement in the frozen [B191 review](Specialization_B191_Expedition_Activity_Native_Review.md): that error code alone did **not** prove failure occurred before any earlier eligibility/request. It identifies the guard in the failing evaluation. B191 screenshots lacked attempt-time instrumentation; its native request history remains UNKNOWN. Frozen evidence is retained rather than rewritten. Likewise, B192's startup eligibility observation does not prove permission at a later writer check or successful Sleep execution.

A bounded local counterexample used the actual B192 bridge with the existing read-only test fixture: initial AWAKE equals1797587246, diagnostic eligibility true, then one mock Sleep request changes mock activity to OPERATION1225574625 and publishes. The bridge produces ACTIVITY_UNEXPECTED_STATE with Owned=true while retaining the initial AWAKE snapshot. **LOCAL_COUNTEREXAMPLE_PASS, zero real native calls.** OPERATION is deliberately injected here; it is not the measured native failure-time value. Independent review confirmed the source timing distinction. Existing delayed-Sleep regression covers AWAKE→SLEEP, not this intervening third-state counterexample. No test/source/assertion change was made.

## Next boundary — no implementation in this review

The minimum missing evidence is the activity at failure and whether this lease already attempted a request. A proposed diagnostic follow-up would retain startup evidence separately, record failure-time activity and enum-equality booleans, and mark PRE_REQUEST_GUARD versus POST_REQUEST_READBACK using the actual request/attempt flags. It must not accept OPERATION by assumption, force Wake, retry commands, change capacity/binding or use a native espionage mission. No new test is requested until that narrow change is separately approved and prepared.

No evidence currently supports a type mismatch, numeric-comparison defect or general native Sleep impossibility. Task suppression/completion/release remain unverified. The initial sample has served its purpose; do not ask the user to repeat naming, save/load or unchanged B192 tasks.

## Archive and checks

Originals moved, without renaming/overwriting, to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B192/2026-10-10/`; pre/post SHA256 matched. The local manifest also retains the reproduction script/result. No screenshot/raw artifact enters Git.

- `Screenshot 2026-10-10 at 9.54.06 PM.png`: 12608053 bytes; SHA256 `96d0bb45bbb0c26c8c2c4d2c46602af9015ccb2cc2f0eee4df43f15b9dbe3cc0`.
- `Screenshot 2026-10-10 at 9.54.08 PM.png`: 12677208 bytes; SHA256 `2f66eb450365026f35e0c624dc430ca968b2ec9390c167b1dea1ff687362757f`.

Read-only source/live comparison matched the activity bridge, window, localization and Gameplay Gate files. This is not a new full runtime deployment audit. Changed-document link/anchor, selector/context/hash and exact diff-scope checks apply. Mod/tests/Design/GC/main/deployment tools/runtime unchanged; no game launch or native call by Codex.
