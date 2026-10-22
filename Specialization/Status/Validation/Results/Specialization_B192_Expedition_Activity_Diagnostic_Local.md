# B192.219 — bounded startup activity diagnostic

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** User-approved diagnostic-only patch following [B191 native startup failure](Specialization_B191_Expedition_Activity_Native_Review.md). B191 stopped at ACTIVITY_UNEXPECTED_STATE before native action lookup/eligibility/write. This patch observes that boundary; it does not fix or bypass it.

## Capture, ownership and retained behavior

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) captures one scalar startup snapshot per activity key, after the existing exact local owner/unit/type/name/position and native operation-1 checks succeed, before the unchanged initial activity guard. The snapshot records actual activity and Lua type; current AWAKE/HOLD/SLEEP/OPERATION enum values and types; IsReadyToMove; native Spy operation/end turn; exact GameInfo UNITOPERATION_SLEEP Hash; and CanStartOperation(unit, hash, nil, false, false) result. Only boolean true/false become ALLOWED/DENIED; nil, numeric1, strings or exceptions remain UNKNOWN. Missing/throwing optional readers are independently reported without suppressing other fields or changing the task result.

This is one additional read-only eligibility query, not permission for a writer. The original eligibility/write/readback path still runs independently when its original activity precondition permits. An unexpected activity still produces ACTIVITY_UNEXPECTED_STATE and zero native activity writes. Reentrant diagnostic readers cannot continue an obsolete attempt: the exact lease/job is checked again before reaching the existing guard/writer.

The UI bridge owns one session-only ExposedMembers.SPC_ExpeditionActivityDiagnostic slot. Values are short typed strings (100-byte bound for each observation) plus identity/time scalars; no retained unit object, history, Property, save schema, extra event registration, frame/city polling or repeated query on HELD refresh. It is discarded when the team/key/owner/unit/name/position changes, at END/no view, UI initialization or shutdown. HELD preserves the same attempt's evidence, explicitly historical rather than current. The [window](../../../../Mod/UI/ExpeditionSpyWindow.lua) only displays a matching sample; it never calls a native API for this block and never uses it to enable controls.

Capacity1, source binding, name-pool continuity, native travel, two-turn/no-reward task, existing activity guard, owned release, ordinary-Spy isolation and temporary native Spy-slot cost are unchanged. No Gameplay Gate/reader/UI adapter or unit data changes, no Design/GC/rewards/N2/N3 change. No new button or XML control. New bilingual LOC_SPC_EXPEDITION_SPY_ keys: DIAGNOSTIC_HEADER, DIAGNOSTIC_ACTIVITY, DIAGNOSTIC_ENUM_A, DIAGNOSTIC_ENUM_B, DIAGNOSTIC_SPY, DIAGNOSTIC_SLEEP_HASH, DIAGNOSTIC_ELIGIBILITY, DIAGNOSTIC_ALLOWED, DIAGNOSTIC_DENIED, DIAGNOSTIC_UNKNOWN.

## Targeted validation

**227 test methods PASS**, using existing Python/Lupa and the configured read-only external DB (SQL checks use in-memory copies). Exact suites: test_expedition_spy_name_pool4, name39, binding14, task26, gate31, activity18, activity_ui33, activity_integration13, activity_report9, activity_diagnostic21, activity_diagnostic_report9; test_p0_panel_current_layout10. Command: python -m unittest with those module names. No full gameplay/stress test or game launch.

The30 new methods cover actual-bridge typed observations, missing/throwing readers, strict boolean permission, third activity still blocked with ALLOWED or DENIED, diagnostic ALLOWED/DENIED/error unable to authorize/veto the separate writer check, repeated notifications, new key replacement, reentry/cancellation, stale/cross-team UI rejection and clear on END/load-context initialization/shutdown. Existing eligibility call-count assertions now allow the one diagnostic read; native writer counts and failure/ownership assertions remain. The checked-Hash fixture mutates during the real second eligibility query, retaining its original request-uses-checked-Hash assertion.

Independent narrow review found a diagnostic reentry edge, corrected before delivery; the counterexample now has zero stale writes/ACKs/sample. No further actionable defect found. These are local control and representation results, not native SLEEP support or rendered UI proof. The actual B191 activity value/readiness/native permission remain UNKNOWN until the next capture.

## One minimal native test

After verified B192 deployment, use one freshly created and bound arrived test team. If the previous team is HELD, load the pre-creation save or use **结束并移除验证团**, then **① 创建Spy验证团 → ③ 原生派遣**. Loaded sessions do not reconstruct the prototype's source binding; these are fixture setup steps, not another name/save-load acceptance campaign.

At confirmed arrival, click **④ 无奖励任务（2回合）** once. Capture the top report including the precise error (if any) and **启动时活动诊断** through **原生 SLEEP 资格**. If needed, **刷新报告** redisplays the same historical sample; it does not resample. Then stop. No manual Sleep/Wake, task-completion turns, save/cold reload or re-enable sequence is required for this diagnostic batch.

The sample distinguishes a raw type/enum mismatch, a legitimate different native activity, and native SLEEP eligibility/refusal independently from readiness. ALLOWED is not proof that a submitted request would succeed. DENIED/UNKNOWN is not grounds to bypass the engine. Capacity/binding/task behavior stays unchanged regardless of the result. Current deployment is recorded in [Status](../../Specialization_P0_Status.md#current-authoritative-state), not inferred from source HEAD.
