# B197.224 — native-style Expedition sidebar

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED for native layout/input.** The user approved the [B196 sidebar direction](../../../Architecture/v2/P0_N_Expedition_UI.md#b196-feedback--native-style-sidebar-reference). This batch changes presentation only within the existing one-shot prototype.

## Implemented boundary

- [Window Lua](../../../../Mod/UI/ExpeditionSpyWindow.lua) and [XML](../../../../Mod/UI/ExpeditionSpyWindow.xml) replace the normal central panel with a left-docked native `ChooserAnim` frame, scrollable destination rows and a compact mission card. Existing native header, close, destination/mission textures, selection braces, confirmation drawer and Spy icons are reused; no new asset or copied espionage controller.
- **派遣到新城市** shows city/civilization rows and selection feedback. Selecting a row never dispatches; **确认派遣** submits the existing guarded DISPATCH. Only the existing revealed/met foreign-major-capital fixture is listed. Native eligibility/time is still checked on confirmation, not speculated per row.
- **任务** shows the existing **无奖励验证任务** card, description and two-turn duration. Card click previews; **开始无奖励任务（2回合）** sends the existing TASK. No rewards, probabilities, extra mission or repeatability are introduced.
- Exact selected unit/current view guards and pending-ack close protection remain. Retired pooled callbacks check generation, selected unit, view and target snapshot. Close clears callbacks/references and resets pools; shutdown removes the single resize listener. Rows rebuild only on explicit opening; resizing performs layout only. No new turn/frame polling, native fact scan, permanent state or GC path.
- Native animation opens the panel; guarded close hides immediately. The generic `AnimSidePanelSupport` close callback is deliberately not imported: it can hide before our pending-request acknowledgement guard and leave late close callbacks. The existing P0 diagnostic panel stays separate and centered.
- City/civilization/footer names truncate with tooltips; summary/card text wraps. Screen-height resizing, native-width scrolling and a bounded feedback area protect the footer. These are static layout decisions, not proof at every UI scale.

The Gate, native travel reader, capacity, source/name binding, independent activity controller, task timing, completion/release and ordinary Spy adapters are byte-identical to B196. Only Window Lua/XML, localization, Probe build and modinfo change in `Mod/`. No Design change, save migration, formal training/reattachment/persistence, N2/N3 or era UI.

## Localization

Six bilingual `LOC_SPC_EXPEDITION_SPY_SIDEBAR_*` keys: `TRAVEL_HINT`, `TASK_HINT`, `TASK_NAME`, `TASK_DETAILS`, `TASK_LOCATION`, `CIV_UNKNOWN`. Existing action/confirmation labels and icons remain. No independent icon assets.

## Validation and evidence boundary

**145 unique focused tests PASS:** 140 passed in the initial run; five external-DB cases initially lacked configuration, then all five passed against the existing configured read-only database. No assertions were removed to hide the dependency. Thirteen new sidebar cases exercise actual Lua, pooled row callbacks, selected destination/explicit confirmation, stale callbacks, changed unit/view, task preview, pending DISPATCH/TASK close and Escape protection, native InputStruct Escape, empty targets, resize/cleanup, listener removal, XML and bilingual SQL.

Suites: `test_expedition_spy_sidebar_ui`, `test_expedition_spy_actions_ui`, `test_expedition_spy_task`, `test_expedition_spy_gate`, `test_expedition_spy_activity`, `test_expedition_spy_activity_report`, `test_expedition_spy_activity_diagnostic_report`, `test_expedition_spy_activity_failure_report`, `test_expedition_spy_name_pool`. Existing Gate fixture adds native UI/instance controls and current build224; one actions test replaces removed previous/next control assertions with destination/mission stack visibility. Business assertions remain unchanged.

Independent source review found no remaining blocking issue. XML/locale, changed links/anchors, task selector/context integrity and diff boundaries are checked at checkpoint. No broad gameplay/stress or new save/load campaign. Native layout/provider, Chinese wrapping, scrolling and click behavior at the user's scale remain unverified. Inherit [B194 activity evidence](Specialization_B194_Expedition_Pending_Activity_Native_Review.md) and [B196 input/Settler acceptance](Specialization_B196_Expedition_UI_Native_Review.md), without re-certifying those paths.

## One minimal UI test

Use one continuous session after verified deployment. Setup only if needed: select the usual Culture IV source, open P0 **人文考察·验证 → ① 创建Spy验证团**, wait for the existing preparation to finish, then close diagnostics. End an old prototype first only if it occupies the slot.

1. Select the team and click **派遣到新城市**. A left sidebar should show destination rows. Select a row, close/reopen once if convenient, then **确认派遣**. Check readable Chinese text, selected highlight, footer/close placement and scrolling if the list overflows. Selection alone must not submit. This verifies the new row controls and guarded sidebar in the native UI.
2. After the existing arrival, click **任务**. Check the compact **无奖励验证任务** card and two-turn duration; click **开始无奖励任务（2回合）**. Continue the existing two-turn task without manual Sleep. The panel must not obstruct normal play; the existing empty task-time action bar and disabled one-shot completion actions should remain. This checks the new mission/confirmation presentation against the unchanged backend.

Cleanup, when done: P0 **人文考察·验证 → 结束并移除验证团**. No separate naming, capacity, Settler, save/cold-load or END campaign. Screenshot only a useful view or unexpected result; stop on a blocked/error state. Actual deployment is recorded in [Status](../../Specialization_P0_Status.md#current-authoritative-state), never inferred from this source report.
