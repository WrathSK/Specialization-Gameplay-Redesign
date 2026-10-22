# B193.220 — exact failure-time activity diagnostic

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The user approved the narrow follow-up to [B192 native evidence](Specialization_B192_Expedition_Activity_Native_Review.md): record the actual failing activity and whether SLEEP was already requested. This patch does not repair or bypass the task guard.

## What changed and what did not

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) captures a separate scalar snapshot immediately before its existing ACTIVITY_UNEXPECTED_STATE failure in the pending SLEEP path. It records the exact activity value already read for that evaluation, the AWAKE/HOLD/SLEEP values used by the guard, OPERATION for comparison, types and equality booleans, the current job requested flag and the activity key's recorded SLEEP attempt. No second GetActivityType, readiness, eligibility or writer call is added. This avoids presenting a later fresh getter as the value that actually failed.

The stage is PRE_REQUEST_GUARD when neither request flag is set, or POST_REQUEST_READBACK after an attempt was recorded. These are local control-flow facts, **not proof that the native engine accepted or completed SLEEP**. The actual native failure-time activity remains unknown until tested; do not assume OPERATION from the prior mock reproduction.

The original one-shot startup sample remains separate and unchanged. The bridge owns one additional ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic slot, captured once per activity key. Its content is scalar, bounded and session-only. Both samples clear when exact identity/key changes, at END/no view, context initialization or shutdown. HELD retains the same attempt's historical evidence. Capture is protected; even a diagnostic formatting exception leaves the original failure acknowledgement intact. It adds no event handler, polling, Property, saved field or retry.

[Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) places **失败时活动诊断** above **启动时活动诊断**. Both are report headings, not buttons. Exact owner/unit/team/key/name/position filtering rejects stale samples; missing current identity fields cannot validate older evidence. No native reads/writes or new XML controls are introduced in the renderer.

Capacity, source binding, name-pool continuity, native travel, two-turn/no-reward timer, native activity guard, request/writer count, owned release and ordinary-Spy isolation remain unchanged. Mod/ExpeditionSpyGate.lua, task adapters, unit data, Design, GC and saved state are untouched. Unrelated failure branches are not relabeled as this unexpected-state failure; no invented failure-time sample on identity/read/eligibility errors.

Nine new bilingual LOC_SPC_EXPEDITION_SPY_ keys: FAILURE_DIAGNOSTIC_HEADER, FAILURE_DIAGNOSTIC_PHASE, FAILURE_DIAGNOSTIC_PHASE_PRE_REQUEST_GUARD, FAILURE_DIAGNOSTIC_PHASE_POST_REQUEST_READBACK, FAILURE_DIAGNOSTIC_PHASE_UNKNOWN, FAILURE_DIAGNOSTIC_ACTIVITY, FAILURE_DIAGNOSTIC_REQUEST, FAILURE_DIAGNOSTIC_EQUAL_A and FAILURE_DIAGNOSTIC_EQUAL_B. Existing enum labels are reused.

## Targeted validation

**254 methods PASS** using existing Python/Lupa and the configured read-only external DB (SQL checks use in-memory copies). Exact suites: test_expedition_spy_name_pool4, name39, binding14, task26, gate31, activity18, activity_ui33, activity_integration13, activity_report9, activity_diagnostic21, activity_diagnostic_report9, activity_failure16, activity_failure_report11; test_p0_panel_current_layout10. No full gameplay/stress run or game launch.

The27 new tests exercise the actual bridge/window: a PRE_REQUEST unknown activity with zero writers; initial AWAKE/allowed followed by one mocked SLEEP request and a different activity; later pending poll; retained startup versus failure samples; exact activity/eligibility/write counts; no new Wake; repeated-notification bounds; new-key replacement; identity/END/load-context clearing; formatting failure still acknowledging the original error; ordered report presentation and no report-side writes. Previous behavior assertions remain unchanged. Package tests only add version220 and the new localization variants.

Independent narrow review found no actionable source/UI defect and ran all27 new tests. The local counterexamples prove sample separation and unchanged control behavior; they do not prove a native intermediate state, Sleep acceptance, ready-unit suppression, task completion or release.

## One minimal native test

After verified B193 deployment, prepare one fresh, bound team and dispatch normally. If the previous team is HELD, use **结束并移除验证团 → ① 创建Spy验证团 → ③ 原生派遣**, or start from the pre-creation save. This is the existing session-only fixture setup, not a save/load or naming acceptance campaign.

At arrival, click the existing wide blue **④ 无奖励任务（2回合）** once. If the error repeats, screenshot the top **失败时活动诊断** block, including **失败阶段**, **失败时实际活动**, **本次已请求 SLEEP / SLEEP 尝试标记**, and equality rows, then stop. It appears above the retained startup block. **There is no new diagnostic button.** If no failure appears, report the current task status instead; do not force an error or extend into a full task test.

No manual Sleep/Wake, completion turns, save/cold-load or re-enable sequence is required. This one capture distinguishes failure before any recorded attempt from a later readback after an attempt and identifies the failing value. Native acceptance remains a separate question; no automatic bypass/repair follows either result. Current source/live and receipt are in [Status](../../Specialization_P0_Status.md#current-authoritative-state).
