# B191.218 — native activity lookup repair

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The user approved the narrow repair proposed after the [B190 native failure](Specialization_B190_Expedition_Task_Activity_Native_Review.md). That frozen record and its two images remain unchanged. The original combined guard failed before eligibility or submission; which individual alias was unavailable remains UNKNOWN.

## Repair and retained boundaries

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) now resolves exactly `GameInfo.UnitOperations.UNITOPERATION_SLEEP.Hash` and `GameInfo.UnitCommands.UNITCOMMAND_WAKE.Hash`, following native UnitPanel's row lookup. It accepts table/userdata adapters and finite integer hashes, including signed/zero values, without hardcoded numeric IDs or enum fallback. Missing table, row or valid Hash receives its own error code. Sleep eligibility uses the native `CanStartOperation(unit, hash, nil, false, false)` form; Wake retains `CanStartCommand(unit, hash, false)`. Each request reuses the exact hash checked for eligibility, even if the lookup row changes during that call.

The native evidence was directly rechecked read-only: installed `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua:227–233,407–409,548–550` resolves action rows and Hash;609/615 uses false/false eligibility;677 uses NO_TARGETS only as an optional hint;2513/2535 submit command/operation hashes. `CIV_ASSETS` means installed Civ6.app/Contents/Assets. UnitOperations.xml:103 and UnitCommands.xml:35 define the exact keys. SQLite confirms the rows, but does not expose the native GameInfo Hash column; no SQLite hash inference. These local source coordinates are not public links or engine execution evidence.

[Gameplay Gate](../../../../Mod/ExpeditionSpyGate.lua) exposes the precise activity failure separately from ACTIVITY_READBACK_STOP and stamps each diagnostic reply with the published activity revision. [Management window](../../../../Mod/UI/ExpeditionSpyWindow.lua) shows a concise cause near the top. A HELD task no longer automatically claims that binding was lost. It reports matching identity only when the HELD snapshot's revision and turn match the current exact-team mirror and its unit/name/source checks match. Otherwise it says the source record is retained and asks for refresh; cached matching details are suppressed. These fields are diagnostic only and do not enable held task controls.

New Chinese/English localization keys under LOC_SPC_EXPEDITION_SPY_: HELD_MATCH, HELD_RECHECK, HELD_SOURCE, ACTIVITY_FAILURE, ACTIVITY_CAUSE_DATA/API/DENIED. Unknown errors retain their exact code.

The [B190 activity ownership contract](Specialization_B190_Expedition_Task_Activity_Local.md#change-and-ownership) is unchanged: one request, exact unit/type/raw name/position, local owner/native operation -1, observed SLEEP before timer start, owned release only, bounded transition polling, no idle poll, no repeated writes on failure, retained ambiguous pending outcome and separate bounded reply channels. Capacity1, source reference, native name, independent two-turn/no-reward task, temporary native Spy-slot cost and ordinary Spy isolation remain unchanged. No new Property/schema, mission/reward, Design, GC, N2/N3 or formal saved-team reconstruction.

## Targeted validation

**197 test methods PASS** with existing Python/Lupa and configured read-only external DB (SQL tests use in-memory copies). Suites: test_expedition_spy_name_pool4, name39, binding14, task26, gate31, activity18, activity_ui33, activity_integration13, activity_report9 and test_p0_panel_current_layout10. Command: `python -m unittest` with those exact module names. No full gameplay/stress run or game launch.

New checks cover alias/NO_TARGETS absence, obsolete alias ignored, table/userdata rows, signed/zero hashes,30 malformed table/row/hash subcases, cached checked hash, denied/missing API with no write, preserved precise error and timer stop, fresh/stale HELD identity presentation, unrelated-team isolation and bilingual strings. Existing delayed/reentrant publication, cancellation ownership, timeout, pre-existing sleep, stale release and ordinary-Spy tests still pass. Independent scoped review ran55 bridge/integration/report tests and found no actionable defect.

These checks establish local control behavior only. Actual custom-Spy SLEEP/WAKE eligibility, needs-orders suppression, event order and rendered report remain native-unknown. The previous179-method result did not prove the aliases existed; its frozen evidence is retained without upgrading that claim.

## One minimal native session

Use B191 after verified deployment. Prepare the already-tested named/bound arrived team in one session: load the pre-creation save or use **结束并移除验证团** for an old on-map prototype, then **① 创建Spy验证团** and **③ 原生派遣**. A loaded session cannot reconstruct source binding; this is fixture setup, not a repeat naming/save-load campaign.

1. At confirmed arrival, click **④ 无奖励任务（2回合）** once. Do not manually sleep or skip. Expect task running with its deadline. If it stops, capture the precise top error and stop; this tests the repaired lookup and actual eligibility/readback.
2. Close the window, handle other units normally and advance the two indicated player turns. The team must not require manual orders; selecting it must retain management but no Wake/Skip/native mission action during the task. This tests actual readiness suppression rather than a hidden button alone.
3. Open **人文考察·验证 → 刷新报告**: expect exactly1/1 completion and activity released, with original source/capacity1/1 retained and no native mission reward. Use **结束并移除验证团** to remove it. This tests the owned Wake/release path and leaves no fixture.

No new cold-load ritual, reward test or N2/N3 continuation. Stop for denied activity, stuck preparation/release, unexpected wake or mission/reward. Current source/live and receipt are tracked in [Status](../../Specialization_P0_Status.md#current-authoritative-state); a source commit alone does not prove deployment.
