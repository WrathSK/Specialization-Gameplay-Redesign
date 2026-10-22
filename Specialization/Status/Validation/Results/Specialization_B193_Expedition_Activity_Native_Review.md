# B193 — SLEEP requested; failure-time activity is OPERATION

**USER_GAME_TEST diagnostic evidence received; task remains FAIL / HELD.** Both uploaded T88 screenshots were visually reviewed. The requested failure-time observation is complete; no unchanged B193 retest is needed. This review proposes a repair but does not implement or deploy one.

## Native observation

| Field | Screenshot 1 |
|---|---|
| Failure phase | POST_REQUEST_READBACK — SLEEP 请求后的活动读回 |
| Actual activity at failure | 1225574625 (number) |
| SLEEP requested / attempt recorded | true / true (boolean) |
| Exact equality with OPERATION | true |
| Exact equality with AWAKE / HOLD / SLEEP | false / false / false |
| AWAKE / HOLD | 1797587246 / 75236491 (number) |
| SLEEP / OPERATION | 38434027 / 1225574625 (number) |
| Retained startup sample | AWAKE1797587246; ready=true; native Spy operation=-1; end turn=0 |
| Startup diagnostic native eligibility | allowed=true; SLEEP hash=-41338758 |
| Task error | ACTIVITY_UNEXPECTED_STATE |

Screenshot 2 retains own capacity1/1, tracked team3342365 at(23,15), source Edinburgh(Test)city393220, native name 艾莉森, original native capacity5→5, ordinary Spies0→0 and completion events0. The task is HELD and the report asks for a fresh binding check: retained source/name fields do not independently prove a fresh current binding validation. No newly observed capacity loss or source overwrite is shown, but this is not another full binding/ordinary-Spy acceptance test.

## Cause and evidence boundary

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) reads the actual activity at each evaluation. In SLEEP mode it accepts observed SLEEP, otherwise demands AWAKE or HOLD before reaching its request/pending logic. The first sample is AWAKE, but after the recorded SLEEP request a later evaluation reads OPERATION and immediately fails that guard. The observed error is therefore explained by the bridge rejecting a post-request activity, not by equal numeric values comparing incorrectly or an absent request.

Both request flags were true in the failed evaluation. They establish the local request-attempt phase, **not native completion or successful SLEEP**. OPERATION is an activity enum; it is not by itself proof of a native espionage mission. The same evaluation's read path still requires the exact unit/name/position and GetSpyOperation()==-1 before recording activity. The screenshot prints -1 in the separate startup sample; the failure-time mission rejection remains source-based evidence, not an extra displayed failure-time getter.

The bridge already has bounded pending polling (0.25 seconds, 10-second timeout). Its current guard prevents OPERATION from using that wait. [Gameplay Gate](../../../../Mod/ExpeditionSpyGate.lua) starts its two-turn/no-reward timer only after an explicit ASLEEP acknowledgement, so stopping here explains why the custom task does not begin.

**Still UNKNOWN:** whether this native OPERATION state is transient, whether it will reach SLEEP within the existing bound, readiness suppression, task completion and owned release. The images do not show duration or a later settled state. Do not label OPERATION as successful Sleep, general Spy incompatibility, native refusal, or a native espionage task. The [B192 startup/failure distinction](Specialization_B192_Expedition_Activity_Native_Review.md) is now resolved for this observed run, without rewriting earlier evidence.

## Proposed next repair — not authorized by this review

1. In the existing SLEEP request path only, treat exact ACTIVITY_OPERATION as **pending** when this same job has requested=true, owned=true and seen.attempted=true. Keep exact owner/unit/type/name/position/activity-key and native-mission checks before every read. Pre-existing OPERATION with no owned request remains rejected.
2. Reuse the existing 0.25-second polling and 10-second deadline. Do not reset/extend the deadline, resend SLEEP, repeatedly query eligibility, acknowledge success, start the task timer or alter capacity/binding while pending. Only a later exact SLEEP read can use the existing ASLEEP acknowledgement.
3. Preserve ASLEEP monitoring and conservative cancellation/release. If OPERATION persists to timeout, fail and retain uncertainty; do not force WAKE or claim successful release without observing owned Sleep. A possible late native completion after timeout remains unknown.
4. Keep one bounded diagnostic for the terminal pending outcome, including last checked activity, phase/request flags and elapsed time. B193 currently captures only ACTIVITY_UNEXPECTED_STATE; merely waiting would otherwise lose the failure-time block on timeout. Capture at an actual checked sample, label its timing, and retain the primary timeout reason even if release subsequently fails. No unbounded history, global scan or new native mission.
5. Expected code boundary: activity bridge, existing report/localization if needed, and directly related tests/package metadata. Gameplay task timer, own capacity/source binding/name pool, ordinary Spies, native mission/rewards, persistence and Design remain unchanged. No N2/N3, formal training/reattachment or UI redesign.

Targeted local checks should prove post-request OPERATION→SLEEP starts only after observed Sleep; persistent OPERATION times out without retry/false success; pre-existing OPERATION remains rejected; repeated events do not duplicate requests; identity/native-mission changes stop; pending cancellation does not wake an unknown state; ASLEEP monitor behavior and normal owned release are retained. Keep B193's frozen diagnostic result; update only directly affected current test expectations during the separately approved repair.

## Bounded local review

An independent reviewer exercised the actual bridge with one hypothetical pending branch substituted **only in process memory** through the existing fixture. Seven **LOCAL_COUNTERFACTUAL_PASS** cases cover delayed SLEEP, persistent OPERATION timeout, pre-existing OPERATION rejection, post-ASLEEP OPERATION rejection, pending cancellation, native mission change and repeated notifications. No repository source/test/assertion was modified and no native call occurred. This supports the candidate control boundary; it does not validate native OPERATION→SLEEP timing or the complete future patch/diagnostic. Script/result retained with the ignored evidence archive. The previous254 implementation tests are inherited evidence, not rerun or newly claimed here.

## One next native flow, only after approved repair

Prepare one fresh arrived bound team, then click existing **④ 无奖励任务（2回合）** once. Do not manually Sleep/Wake. If preparation settles to running, handle unrelated turn blockers normally and advance the two task turns: check the team no longer demands manual action during the task and that completion releases it. This newly tests the pending→Sleep→timer/release path that has not yet passed. If timeout/HELD occurs, capture the terminal activity report and stop; this distinguishes a transient OPERATION from a persistent state that the current Sleep model cannot yet accept. No repeated name/save/cold-load campaign or unrelated yield checks. No unchanged B193 test is requested now.

## Archive and scope

Originals moved without renaming/overwriting to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B193/2026-10-10/`; pre/post SHA256 matched. The manifest includes the local counterfactual script/result. Raw screenshots and local evidence do not enter Git.

- `Screenshot 2026-10-10 at 10.07.51 PM.png`: 13035270 bytes; SHA256 `2d0604c9479d6d77d4a589563efc0ba1c0241817fe936b1a5368aa1ec4f6589e`.
- `Screenshot 2026-10-10 at 10.07.55 PM.png`: 13102017 bytes; SHA256 `27ed572450d1fbbdea6f8b9e5768f7cd00779418d97551f62d1090dab76eb991`.

Read-only source/live comparison matches the activity bridge, window, localization and Gameplay Gate (four files); this is not a new full deployment audit. Only reviewed documentation/context metadata changes in this checkpoint. Mod/tests/Design/GC/main/deployment tools/runtime and frozen results remain unchanged. No game launch, deployment or automatic repair.
