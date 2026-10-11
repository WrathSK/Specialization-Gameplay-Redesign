# B189.216 — native name-pool prototype

Date: 2026-10-10. User authorized the [scoped name-pool proposal](../../../Reports/Technical/Specialization_Expedition_Spy_Identity_Naming.md#proposed-next-minimal-batch--needs-implementation-approval). **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** This replaces the failed mandatory NAME_UNIT preparation, not formal N1 persistence/reattachment or N2/N3/rewards.

## Implementation and evidence boundary

[Identity.sql](../../../../Mod/Data/Identity.sql) copies the existing Scotland CitizenName/Female/Modern rows only into CIVILIZATION_SPC_TEST using INSERT OR IGNORE. The configured read-only DB supplies40 rows; an in-memory execution confirms complete metadata preservation, repeatability and other civilizations/global rules unchanged. A missing source pool stays empty, with no invented fallback. This civilization-wide pool also supplies ordinary Spies of the test civilization; it is not an Expedition-exclusive list. Other civilizations, native Spy definitions, XP, naming thresholds and HD are unchanged.

[Reader](../../../../Mod/ExpeditionSpyRead.lua) and [window](../../../../Mod/UI/ExpeditionSpyWindow.lua) keep the bounded exact UI-unit readiness wait, then observe automatic naming for at most10seconds each, using publication callbacks and the existing0.25s active-window poll. No NAME_UNIT command or unit-name writer remains. Nonempty loaded pool, exact unit, nondefault name and initial visible/off-map name collision checks are required. An exact CitizenName key or a uniquely matching localized pool value is accepted; the original raw GetName string is retained without converting it into a guessed key. Missing/ambiguous evidence stops. Unreadable/default names wait only within the bound. Close, shutdown or timeout cancels observation, retaining the unit/capacity for explicit END; reopening does not auto-confirm a cancelled attempt.

The UI sends NAME with a current-turn off-map-check acknowledgement. [Gameplay Gate](../../../../Mod/ExpeditionSpyGate.lua) independently validates exact ID/owner/type, source reference and position, pool/default, raw name readback and visible duplicates. Off-map records remain a UI-owned observation: the known native call is GetNthOffMapSpy(player,index), not an assumed Gameplay API. This is the existing trusted UI/Gameplay prototype boundary, not protection against forged Lua packets or a global identity registry. Failed confirmation holds the session. Repeated valid confirmation is idempotent; READ alone cannot accept a name.

The retained session name is the continuity candidate for changed-ID arrival, with exact type/owner/current lookup, target and original source checks. Our existing cap1 prevents creating a second custom team while one is pending/off-map; the reservation remains until explicit cleanup. No new Property, persistent schema, source-city matching by label or saved-journey reconstruction is added. Name uniqueness/exhaustion/reuse and preservation are not asserted as engine guarantees. A cold session cannot recover binding from a name alone.

Unchanged: own capacity/source semantics, temporarily accepted native-slot cost, target restriction, independent no-reward2T task, exact END, native mission UI isolation, Design, GC and permanent records. New scans occur only within explicit bounded name preparation/confirmation; no new per-turn name-pool scan, recurring timer or AI listener. Native ordinary-Spy reward hooks are not called or modified.

Player diagnostics report loaded pool count, observed/default name, stage and precise failure; new keys are NAME_POOL, NAME_OBSERVATION and NAME_STAGE_READING under LOC_SPC_EXPEDITION_SPY_. Existing labels and window layout remain. Build stamps advance to B189.216/modinfo216.

## Targeted verification

**124 methods PASS:4 actual SQL pool tests,39 native-name/UI preparation,14 binding,26 task/UI,31 gate/package and10 panel. Missing/default/duplicate and localized ambiguity, UI-only off-map evidence, exact source/owner/type/ID, current-turn confirmation, delayed publication, cancellation/reentrant notifications, arrival/capacity/task/END covered. No native naming/travel PASS implied.**

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/spc-l2c-python:DevelopmentTests SPC_DEBUG_GAMEPLAY_DB=<configured-read-only-DB> /opt/homebrew/bin/python3.14 -m unittest test_expedition_spy_name_pool test_expedition_spy_name test_expedition_spy_binding test_expedition_spy_task test_expedition_spy_gate test_p0_panel_current_layout`. DB is resolved from existing ignored configuration; tests only mutate in-memory copies. Independent scoped review found no remaining actionable Gate issue. Native APIs are not executed by these local mocks.

Tests use actual current Lua/SQL/UI with independent fixture engine assignment and delayed publication. They do not prove that Civ VI assigns a name to our custom type or preserves it across travel. Existing local binding/source/cap/task/exit regressions are inherited within their scope; no full gameplay regression, stress, save/load campaign or game launch.

## One minimal native session

After B189 deployment, load a save before the failed team was created, or explicitly remove the old on-map team with **结束并移除验证团**. Use the existing test civilization and select an own Culture ACTIVE IV source city. Open **专业化诊断 → 人文考察·验证**. All steps use left-click.

1. **① 创建Spy验证团**. Keep the window open. Expect a loaded name pool (40 in the reviewed fixture), a personal native name rather than the default unit label, “已确认，可以派遣”, original source and1/1. This is the new native-assignment gate. If it stays generic/holds, capture the report and stop; do not manually rename or create repeatedly. A loaded pool with no usable name means the pool alone was insufficient, not that all custom Spy naming is impossible.
2. Select an eligible foreign capital; **③ 原生派遣**. After arrival, **刷新报告** must retain the same raw name, original source,1/1 and confirmed arrival/binding. Public Unit ID may change. This tests actual name continuity through native travel. Stop on unbound/HELD instead of proceeding to a task.
3. **④ 无奖励任务（2回合）**. Advance the two indicated player-turn boundaries and **刷新报告**. Expect exactly1 completion, original binding, no added intelligence-source turns, native mission or unintended reward. Avoid unrelated Spy missions during this short interval because the event diagnostic is player-level and attribution otherwise remains unknown.
4. **结束并移除验证团**. Expect ENDED,0/1 and removal of this returned unit; use **刷新报告** after UI publication if native classification has not caught up. This checks cleanup of the name-linked arrival, without a save/reload ritual.

No ordinary-Spy control is required if this flow succeeds. If naming fails with a populated pool, a later bounded control may distinguish assignment timing/type/creation-path; it is not automatically dispatched now. No promise of retroactive naming for old unnamed/off-map units. Formal N1, N2/N3/U2 and rewards remain held.

## Delivery

Current Status/receipt determines deployed state; source HEAD alone is not runtime proof. B188 native failure and all prior frozen evidence remain unchanged. User testing is limited to the session above; stop after review.
