# B198 — Expedition dispatch guard and faithful native layout

Source checkpoint: **B198.225 / modinfo225**. Scope: user-approved repair of the [B197 failure and rejected presentation](Specialization_B197_Expedition_Sidebar_Native_Review.md). **LOCAL_SIMULATION_PASS; native UI/travel integration USER_GAME_TEST_REQUIRED.** Deployment identity comes from [Status](../../Specialization_P0_Status.md#current-authoritative-state) and the actual receipt, not this local report.

## Repair and ownership boundary

B197 stored the ordinary-Spy/capacity snapshot at UI CREATE, then used any later difference/UNKNOWN to stop DISPATCH. User creation of an ordinary Spy therefore blocked a valid Expedition before a native request. B198 retains the creation-time before/after isolation check and keeps later comparison as diagnostic evidence only. Exact current team/name/source/target/turn/native-eligibility/one-shot permit checks remain. No arbitrary ordinary-Spy state is treated as Expedition permission.

Normal TRAVEL/TASK adapt the native `EspionageChooser` presentation: layered selected-city banner, compact city rows with district strips and total travel-plus-establishment preview, adjacent drawer, native icon/stat containers, explicit confirm and Cancel. TASK uses the same drawer at the left position, with one no-reward2T card. Normal information is concise; source/team detail stays in the header tooltip/P0 report. Native mission enumeration, rewards, probabilities and automatic acceptance callbacks are not imported. Long city names are truncated with tooltip; footer/card size recalculates after display updates.

Read-only native/BES source basis: `Base/Assets/UI/Choosers/EspionageChooser.lua/.xml`; installed Better Espionage Screen's matching chooser. The selected-city banner, completed non-Wonder district filtering, seven-icon paging, travel+establishment display and adjacent drawer follow those existing presentation patterns. This does not prove the effective native provider or actual rendered fit. Ordinary Spy source/UI and HD are untouched.

`ExpeditionSpyRead.Presentation` samples only an existing eligible target on explicit open (TASK after its READ reply). It writes no Property, capacity, binding, operation or permit; unavailable optional data does not block travel. Selection/paging use the open's cached display facts; actual confirm still performs fresh exact preflight. Each window owns its pooled city/card/district controls and callback generations; close resets pools, retires callbacks and discards snapshots. Resize/render/turn publication add no presentation scans. Pending dispatch/task acknowledgements still prevent close/Cancel from losing the accepted transaction.

Unchanged: own cap1, source/native-name binding, target eligibility, native travel adapter, Gate/task/activity implementation, task clock, no-reward/one-shot boundary, ordinary Spy behavior, save schema, Design and GC. Formal training/reattachment/persistence, repeat missions, N2/N3/U2 and rewards remain held.

## Local evidence

**160 focused tests PASS**, using actual Gate/Reader/Window Lua with isolated native fixtures and the existing configured read-only gameplay database. Fifteen new tests plus the previous145 relevant tests. Suites: `test_expedition_spy_relocation_ui`, `test_expedition_spy_sidebar_ui`, `test_expedition_spy_actions_ui`, `test_expedition_spy_task`, `test_expedition_spy_gate`, `test_expedition_spy_activity`, `test_expedition_spy_activity_report`, `test_expedition_spy_activity_diagnostic_report`, `test_expedition_spy_activity_failure_report`, `test_expedition_spy_name_pool`.

- Actual UI CREATE regression: unchanged control dispatches once; later ordinary-Spy creation, operation, capacity change and unavailable historical audit no longer veto valid dispatch. Prior B197 source fails exactly those later-change cases. Creation-time changed/UNKNOWN isolation still stops before name confirmation.
- Wrong owner/type/name/source, stale turn/target and native eligibility/request failures retain their protection. Ambiguous/false requests remain held and are not retried. Own capacity/source and ordinary Spy instances remain unchanged in the successful test.
- Native presentation fixtures cover travel+establishment sum, complete non-Wonder districts, unavailable optional data, unrevealed/stale targets, long-name truncation, cached paging and no render/resize/turn preview reread. Existing stale row/arrow, selected-unit, pending confirm/Cancel/Escape and shutdown cleanup checks remain.
- XML structure/control IDs and custom bilingual SQL pass. Two existing native localization keys are explicitly separated from this Mod's SQL; custom keys still require both languages. Review corrected a long city-name overflow risk and an obsolete “unknown; dispatch stopped” diagnostic. Native visual rendering remains untested.

No broad gameplay/stress or new save/load campaign. Local tests prove these sampled branches, not native UI rendering, engine memory improvement or universal isolation. B189 binding/task/END, B194 activity and B196 explicit-input evidence are inherited where unchanged; B197 remains a recorded failed test, never rewritten as PASS.

## One combined minimal native test

One continuous session on deployed B198. Setup: if the failed B197 team is still HELD, use P0 **人文考察·验证 → 结束并移除验证团**, then select the usual Culture IV source and **① 创建Spy验证团**. Wait for preparation to finish and close P0. A held old team cannot be repaired by simply clicking dispatch again.

1. After preparation, create one ordinary Spy as in B197 (no order required). Select the Expedition and **派遣到新城市**. Check the selected-city banner, compact city/district list and neighboring preview; select a destination and **确认派遣**. Selection alone must not send travel. It should no longer stop because the ordinary Spy was created. This validates the repaired native trigger and new layout together.
2. After arrival, **任务 → 开始任务**. The **无奖励验证任务** card must show2turns, fit its location/text and permit confirmation. Let the unchanged task complete without manual Sleep; task-time actions remain absent. This checks the new task drawer against the existing timer/action path.
3. Finish with P0 **人文考察·验证 → 结束并移除验证团**. Capture one useful travel/task view or any error; no repeat save/cold-load/capacity/naming/Settler test. If the error recurs, the normal message now distinguishes readable causes and P0 retains the exact detail.

User decision: none for this approved repair. User testing: the combined native UI flow above. Codex next: review submitted evidence; no automatic next mechanism.
