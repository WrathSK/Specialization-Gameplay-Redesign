# B188.215 — UI readiness before controlled naming

Date: 2026-10-10. User approved the [B187 bounded readiness repair](Specialization_B187_Expedition_Name_Preflight_Native_Review.md). **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** Only the prototype naming/UI boundary changes. This does not authorize formal N1 training/persistence/reattachment, N2/N3/U2 or rewards.

## Repair and ownership

[Reader](../../../../Mod/ExpeditionSpyRead.lua) now checks the exact created ID in the UI context separately from name readback. Missing/unreadable unit evidence is PENDING; definite wrong ID/owner/type, missing player or missing DB definition stops with a distinct reason. No collection/name/selection fallback adopts a substitute. SubmitName repeats the exact check before the single native command. Capability/native command permission checks and raw name comparison remain mandatory.

[Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) owns one temporary naming attempt: up to10seconds for UI unit readiness, followed by up to10seconds for an already-submitted name to read back. It reuses publish notifications and the existing0.25s bounded active-window poll. Readiness checks only the exact unit; the post-creation ordinary-Spy audit runs once when readable. No new ongoing scans, events, queue or global cache. State clears on completion, timeout, close or shutdown. Definite mismatches and native refusal stop rather than retrying commands. Gameplay independently confirms name/source/current ID/placement before dispatch as before.

A SUBMITTING guard prevents a nested publication from sending the name command twice. Independent review additionally reproduced a synchronous CREATE reply overwriting the naming timer with the outer request timer. The repair scopes request continuation/timer callbacks to their exact pending token. A consumed reply, newer request or cancelled window cannot install an obsolete wait or cause a later rename after timeout. Both pre-fix counterexamples are covered by actual-module tests.

Chinese/English diagnostics distinguish waiting for UI, submitting the command, name readback, Gameplay confirmation, confirmed and cancelled-on-close. On failure the report retains the specific read reason and existing detailed error; no new report panel. New keys: `LOC_SPC_EXPEDITION_SPY_NAME_STAGE` and its `_READINESS`, `_COMMAND`, `_READBACK`, `_GAMEPLAY`, `_CONFIRMED`, `_CANCELLED` variants. Closing cancels observation, not the reserved team; reopening can confirm an already-completed command but never submits another automatically. If still unconfirmed, explicit **结束并移除验证团** remains the cleanup route.

Unchanged: Spy=1 definition, own cap1/off-map reservation, exact source reference, expected name/team key, arrival identity checks, independent no-reward2T task and END, ordinary Spy/HD behavior, permanent state, Design and GC. Gameplay Gate is byte-unchanged. Build stamps advance to B188.215/modinfo215; gameplay/reward scope does not advance.

## Targeted verification

**110 methods PASS:**29 name (47 subTest cases),14 binding,26 task/UI,31 gate/package and10 current P0 panel.12 new name methods include18 new subTest cases: separate Gameplay/UI visibility, transient read failures, exact mismatch diagnostics, delayed readiness then delayed name, ordinary audit timing, one-command/no-auto-dispatch,10s deadline, timeout/no late rename, close/reopen/stale callbacks, synchronous CREATE publication, close during request and publication within NAME_UNIT. Existing arrival/source/cap/UNKNOWN/task/cleanup checks pass. The package test now expands all six dynamic stage-localization variants; no assertion was weakened.

Two synchronous-request cases failed against the intermediate patch, then passed after the token-scoped continuation fix. Independent review reran its original failure and successful/cancelled paths with no remaining bounded-scope finding. These local timing models do not identify B187's exact native failing operand or prove custom name eligibility/preservation.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/spc-l2c-python:DevelopmentTests SPC_DEBUG_GAMEPLAY_DB=<configured-read-only-DB> /opt/homebrew/bin/python3.14 -m unittest test_expedition_spy_name test_expedition_spy_binding test_expedition_spy_task test_expedition_spy_gate test_p0_panel_current_layout`. Resolve the DB placeholder from existing local configuration; no new dependency installation. External DB is read-only and used in an in-memory test copy. No gameplay full regression/stress or game launch.

## One minimal native session

Use a save before the failed prototype was created, or use **结束并移除验证团** once to remove it. With an own Culture ACTIVE IV city selected, open **专业化诊断 → 人文考察·验证**. All buttons below are left-click.

1. **① 创建Spy验证团**. Keep the window open. It may briefly show “等待界面读到新考察团”, then should show “已确认，可以派遣”; expected/observed names match, original source remains and count is1/1. This checks the repaired native creation/UI/name boundary. If it stops, capture the report and stop; do not repeatedly create or manually rename.
2. Choose the same eligible foreign capital and press **③ 原生派遣**. At arrival **刷新报告**: expect 已绑定/ARRIVED, the same complete controlled name/key, original source and1/1. This is still the pending native name-survival test; changed public Unit ID is allowed only through the exact validated name/source path.
3. **④ 无奖励任务（2回合）**, advance its two indicated player-turn boundaries, then **刷新报告**. Expect exactly one completion, same source/count, no added source intelligence or reward, no task-attributed native espionage completion. Then **结束并移除验证团**: expect ENDED/0/1 and the test unit gone. This reaches the previously untested independent task and cleanup of the returned unit.

Stop before the next step on HELD/unbound/source mismatch or unintended intelligence/reward. Unrelated ordinary Spy actions can contaminate isolation observations. No extra save/load, re-enable or ordinary-Spy fixture is requested. Existing unchanged lifecycle evidence is inherited only within its original scope.

## Delivery boundary

Source B188.215 is locally complete. Current Status/receipt govern whether it is deployed; source HEAD alone never proves runtime identity. B187 originals/reproduction and frozen local/native records remain unchanged. Formal saved journeys, source reattachment and full mission targeting remain later work.
