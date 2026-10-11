# B187.214 — controlled-name continuity prototype

Date: 2026-10-10. User approved the controlled-name prototype after [B186 native marker loss](Specialization_B186_Expedition_Marker_Native_Review.md). **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** This is a bounded N1 prototype, not formal Expedition completion or new Design.

## Implementation and evidence

The returned B186 Spy lacked its custom Property, while the separate source reference remained valid. B187 replaces only that failed continuity carrier with a controlled raw name: localized Expedition/source-city label plus a short team key. The key combines owner, created public ID and a session creation serial; a replacement in the same session gets a fresh key even when an ID is reused. The complete expected string is retained in the existing session record. It never searches for or rebinds a city by name.

[Gameplay Gate](../../../../Mod/ExpeditionSpyGate.lua) creates the exact custom unit in NAMING. [UI reader](../../../../Mod/ExpeditionSpyRead.lua) checks rename capability and `CanStartCommand(NAME_UNIT,true)`, submits one `RequestCommand` to the exact verified unit object, then reads raw `GetName()`. [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) observes at most10seconds, using publish notifications or a0.25s bounded direct-name poll. A submitted command alone does not enable dispatch: Gameplay must independently read the expected name, same source reference, original current ID and placement before CREATED. No selection-based identity, copied Property or blind retry is used.

Native `Base/Assets/UI/Panels/UnitPanel.lua:447–451,2806–2814` establishes command/capability usage; `UnitPanel.xml:332` supplies MaxLength48 as a conservative presentation reference, not a verified universal engine encoding limit. Label truncation preserves whole UTF-8 characters and the complete ASCII identity suffix, conservatively counting supplementary characters as two units. A local Chinese-name counterexample caught locale-dependent `%c` sanitization damaging UTF-8; explicit ASCII control-byte removal fixes it. Native rename eligibility and arbitrary assigned-name survival are still unproved.

Arrival keeps the B186 player-collection/current-ID lookup route and accepts only one exact owned custom unit with the raw expected name, valid source and current target. Stale-ID aliases, changed names, unreadable names, duplicates and mismatched endpoints do not authorize adoption. Source/cap1/off-map reservation, temporary accepted native Spy-slot cost, independent2T no-reward task, exact END and normal-Spy isolation remain. No city/player/unit Property write, permanent schema, global registry, native Gain Sources or task reward is introduced.

The panel shows expected/observed name, pre-dispatch confirmation, arrival name matching and retained/bound source separately. It retains precise failure details. Closing during asynchronous naming cancels the UI poll: reopening READ may confirm a completed command; otherwise the unit stays reserved until explicit END. This is not a background timeout. Cold loading does not reconstruct a prototype session from a surviving name; load/reattachment/training remain later formal N1 work. Existing B186 teams can be explicitly removed, but are not automatically renamed or adopted.

## Targeted verification

98 test methods PASS:17 controlled-name +14 arrival binding +26 task/UI +31 gate/package +10 current P0 panel. Actual current Lua/SQL/window modules are exercised; the configured external DB is read-only and copied into memory. The fixture simulates NAME_UNIT and engine returns; this does not prove native command eligibility, travel preservation or rendering.

Coverage includes unready dispatch rejection, nil/mismatched/unreadable names, wrong owner/type/source/location/current ID, long Chinese names with intact key, fresh replacement key, delayed command completion, refusal/throw/timeout without resubmission, unrelated selected ordinary Spy, changed-ID arrival without any Unit Properties, exact lookup alias, duplicate name/cap reservation, source/target invalidation, repeated task start/completion, zero reward/native mission, exact END and cold-session non-adoption. Inherited tests now exercise controlled-name identity; frozen B184–B186 reports remain unchanged. A successful-name fixture is used only to establish inherited non-window prerequisites; the new preparation tests bypass it and window tests execute the actual asynchronous handshake.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/spc-l2c-python:DevelopmentTests SPC_DEBUG_GAMEPLAY_DB=<configured-read-only-DB> /opt/homebrew/bin/python3.14 -m unittest test_expedition_spy_name test_expedition_spy_binding test_expedition_spy_task test_expedition_spy_gate test_p0_panel_current_layout`. The DB placeholder must be replaced with existing local configuration; no dependency was installed.

Independent read-only delta review found no blocking defect. Package/localization checks, changed-link/selector/context integrity and Git diff review complete the checkpoint. Design, ordinary Spy/HD definitions, Store, GC, main and frozen evidence are unchanged. Source/deployment state is reported by current Status and receipt, never inferred from local PASS.

## One minimal native session

Use a test save before creating the earlier prototype, or explicitly remove the old test team once with **结束并移除验证团**. No save/reload campaign is requested. Open **专业化诊断 → 人文考察·验证** with an own Culture ACTIVE IV city selected; all following buttons use left-click.

1. **① 创建Spy验证团**: keep the window open until “派遣前确认：已确认”; expected/observed names must match and the correct source/cap1 must remain. Select the same eligible foreign capital and use **③ 原生派遣**. At arrival use **刷新报告**: ARRIVED/已绑定, same complete controlled name/key, original source and count1/1. Public Unit ID may change. This tests native rename and name continuity, not city-name matching.
2. **④ 无奖励任务（2回合）**: advance the indicated two player-turn boundaries, then **刷新报告**. Expect one completion, same source/count, native operation idle, no added source intelligence, no reward and no attributed espionage mission. Existing player-level event diagnostics remain non-attributed; unrelated Spy actions can contaminate this comparison. This tests the previously unreachable independent timer/isolation.
3. **结束并移除验证团**: expect ENDED/count0/1 and the prototype gone. Ordinary units remain. This checks cleanup after the new returned-ID binding; no extra re-enable or cold-load step.

If name preparation is rejected/unreadable/times out, stop before dispatch and capture the report. If arrival is unbound/HELD or source differs, stop before the task. Do not manually rename, teleport, copy markers or repeatedly create units. Native/HD intelligence or reward changes stop the isolation path rather than being suppressed globally.

## Remaining boundary

Only this prototype is authorized. Formal persistence, reattachment, training/cost, full mission targeting/rewards/N2/N3/U2 and icon reuse remain on hold. A successful result will support this session's continuity/task primitive; it will not certify all Spy diplomatic behavior or formal saved journeys.
