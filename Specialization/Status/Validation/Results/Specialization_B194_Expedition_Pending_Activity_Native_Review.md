# B194 — observed Sleep acknowledgement, two-turn completion and release

**USER_GAME_TEST_PASS for the tested independent activity/timer/release path.** All five uploaded images were visually reviewed. The user reports the behavior looks normal. This closes B194's minimal task gate, not formal N1, persistence, N2/N3 or all input surfaces.

## Observed results

| Evidence | Native report observation | Conclusion |
|---|---|---|
| Images1–2, T88 | 无奖励任务计时中; 任务进行中：无需手动待命；完成后自动释放活动占用; independent timer T88→T90; completion0/1 | Task reached running with activity mode ASLEEP; no HELD/timeout shown |
| Images3–4, T90 | 无奖励任务完成; 任务活动占用已释放; timer T88→T90; completion1/1; reward无 | Two-turn task completed once and owned activity release was acknowledged |
| Images2/4 | Native Spy mission-1, source-turn0→0, player mission completion events0 | No native espionage mission/source reward/completion event is shown in this run |
| Images1–4 | Team3342365 at(23,15), original creationID3276829→current3342365, source Edinburgh(Test)city393220, native name艾莉森; explicit source/name/plot match | Source binding stayed consistent across the task; identity was not inferred from current selection |
| Images2/4 | Own capacity1/1, ordinary Spies0→0, native capacity5→5; custom unit remains counted as native Spy | Own cap unchanged; previously accepted native Spy slot cost is retained, not solved |
| Image5 | Selected Settler/开拓者, custom found-city-style investment button beside native action row; backing differs and left reserved area is visible | Presentation issue, not a failed Expedition task or evidence that this Settler is the Expedition |

## What the activity evidence proves

The report's **启动时活动诊断：回合88（历史采样，非实时状态）** still shows AWAKE1797587246 and ready=true. This is the retained pre-request sample, not evidence that the running task stayed awake or that release performed a new readiness query.

The unchanged [Gate](../../../../Mod/ExpeditionSpyGate.lua) only enters TASK_RUNNING and sets taskStart/taskDue on ASLEEP acknowledgement. The [activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) sends that acknowledgement only after exact ACTIVITY_SLEEP readback. Likewise, **任务活动占用已释放** corresponds to modeNONE following RELEASED; the bridge requires AWAKE/HOLD or the applicable unowned-release branch before acknowledgement. This run started an owned task, so the displayed running→completed/released sequence supports native Sleep and its owned release.

The screenshots do **not** contain a per-sample OPERATION→SLEEP trace or elapsed transition duration. B193 directly captured post-request OPERATION; B194 now demonstrates the successful destination and two-turn continuation under the patched wait. Do not invent an OPERATION dwell time or present the retained startup AWAKE as a failure-time/current sample. No new full raw readiness measurement after release or END deletion image is present; prior END evidence is not re-certified here.

No extra save/load, unchanged name-pool or END campaign is requested. Formal source reconstruction after loading, general name-pool coverage, repeatable production missions and complete ordinary-Spy isolation remain outside this prototype acceptance.

## User presentation feedback and scoped next work

The user requests a later native-style interaction: selecting the team should not automatically open the diagnostic window; explicit **派遣 / 任务** unit actions open their relevant views, reusing Spy artwork. During a controlled task, no unit-action buttons should be clickable. Current management action/callbacks remain available while only Skip is locked; native chooser hooks can redirect to the report. These are future UI changes, not claims that B194 already meets the final interaction contract. Reuse native presentation without forwarding custom tasks to native espionage callbacks.

Separately requested visual corrections: investment/construction custom buttons should use the native recessed slot, collapse the unused confirmation slot, retain separate prepare/confirm semantics, and use native Spy artwork for the Expedition. Five existing formal one-turn projects should use their corresponding district Great Person project icons. These changes do not authorize new missions, rewards, capacity/source/persistence changes or a repeatable formal task loop. The [existing UI plan](../../../Architecture/v2/P0_N_Expedition_UI.md) carries the concrete continuation boundary.

## Archive and evidence limits

Runtime under test: B194.221/modinfo221, deployed source d447ff53d0600f194330013bc4850a1211007ee2, recorded receipt B194.221-d447ff5-playtest.json. This review inherits the previous deployment verification; it is not a fresh full runtime audit. The original [B194 local report](Specialization_B194_Expedition_Pending_Activity_Local.md) and [B193 failure evidence](Specialization_B193_Expedition_Activity_Native_Review.md) remain frozen.

All five originals moved without renaming/overwriting to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B194/2026-10-10/`; pre/post SHA256 matched and a local manifest records this report. No raw image enters Git.

- Image1: `Screenshot 2026-10-10 at 10.25.37 PM.png`, 12829854 bytes, SHA256 `6f9c615a98b6ab725f20b1ab07a15a124c34534e831ee61e27bbb2217fe9a2fd`.
- Image2: `Screenshot 2026-10-10 at 10.25.39 PM.png`, 12918217 bytes, SHA256 `91b0f0071305bb3a6c31cd1a88e6e4971ca14c79f1b9f52b2f149e2891b8f330`.
- Image3: `Screenshot 2026-10-10 at 10.27.21 PM.png`, 12809632 bytes, SHA256 `113f263829506f410f213ddc99b38acbfb9dffe0d4dfed2bb157bceca2e80006`.
- Image4: `Screenshot 2026-10-10 at 10.27.23 PM.png`, 12886443 bytes, SHA256 `7c3eefa92a810b5988f8d0a7ebba599941377766788cc884d9e9e61984e61266`.
- Image5: `Screenshot 2026-10-10 at 10.32.05 PM.png`, 443493 bytes, SHA256 `099396bba563a82694292c89568a861c3b455bd5db14264e8a6d9776145af6a4`.
