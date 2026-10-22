# B178.205 — Expedition N1 travel/protection gate

Date: 2026-10-10 (America/Vancouver). Authority: Culture D0049 / Shared D0045. User authorizes N1; U2/N2/N3 remain held. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. N1 partial, not a completed Expedition ability.**

## Findings and implementation

- Official `Base/Assets/Gameplay/Data/Units.xml:759–770` gives `CanRetreatWhenCaptured=true` to the non-Spy Archaeologist and Great People. The explicitly configured current HD database confirms this flag independently of `Spy=1`. This is STATIC_CONFIRMED, not proof our custom unit retreats. An older outer Cache database was identified as stale and excluded from current-rule conclusions.
- Official `Base/Assets/UI/Choosers/EspionageChooser.lua:404–406` reads native travel and establishment durations. Its `606–618` handler separately requests `SPY_TRAVEL_NEW_CITY`; the new gate does **not** call it. The non-authoritative local Spy/UI investigations correctly leave non-Spy helper applicability unknown. No external source, mod or investigation original was modified or published.
- The exact configured current Spy DB base is 60, previous-copies progression 15. This does not establish final city production cost; no copied fixed price, normal training or production charge is introduced.
- New Gameplay gate and independent UI use one explicit request channel, no central request-dispatch edit. One test unit, uncertain-create reservation, last response and optional position watch remain bounded. No periodic collector, city/mission ledger, Property write, carrier, yield, ordinary unit cleanup, diplomacy operation or GC change.
- Existing Builder presentation is reused for the clearly named test unit. Its non-Spy/retreat fields are isolated from Crew definitions. The final Expedition appearance and management UI are not claimed complete.

## Validation

- 34 new test methods PASS: explicit/duplicate/reentrant creation, nonzero human player, wrong Owner, UNKNOWN qualification, pending investment, live cap, occupied center, missing DB flags, native grant nil/throw/third-owner protection, bounded watch, exact cleanup, hostile/missing/changed references, target eligibility and native helper error/invalid-number handling, actual window callbacks, timeout/no auto-retry, close/reopen request completion and END.
- 29 selected related methods PASS: existing cumulative Dialogue behavior, actual Store commit/notification ordering and applicable P0 UI behavior. One historical modinfo 204 stamp check replaced by current 205 file-set/syntax checks. Two retained panel assertions expect the retired manual Inspiration UI; they fail unchanged against byte-identical baseline panel files and are not counted PASS. No historical assertion changed.
- The external DB already contains B177 definitions. The unchanged Dialogue fixture initially reports `SPC_DialogueTotals already exists`; the disposable in-memory regression fixture removes exactly the known B177 total/carrier/Modifier IDs before reapplying source SQL. No external database write. New unit SQL uses the established in-memory Make_Hash fixture, not a claimed native hash test.
- The existing context CLI batch allowlist now includes P0-N1; no selector, validation or workflow behavior was changed. Current context/integrity and independent-selector self-test PASS; three existing helper tests PASS. All 44 scoped document links/anchors and diff checks PASS; CURRENT remains 10 lines.
- Lua syntax, XML parsing, manifest file equality/unique registration, both localization locales and all referenced text keys checked. 202 runtime files. Five existing Crew art entries retain their content; one test entry appended. Existing P0 and Dialogue code/SQL remain byte-identical to the baseline. New window filenames differ from the Gameplay module to avoid VFS basename collision.
- Native rendering, custom-unit retreat, helper suitability, actual remote placement, war continuity, formal production price/queue cap, training receipts and archive lifecycle are **NOT_YET_VALIDATED / not implemented in this gate**. No synthetic fixture result is native PASS.

Targeted reproduction: `PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_expedition_gate.py` with the existing Lua55/Lupa dependency and explicit `SPC_DEBUG_GAMEPLAY_DB` configuration described by the test README. Local runner used the existing temporary Lupa installation. No new package installation or game launch.

## One minimal native session

Use a copy of an existing Specialization-enabled test save. No need to save an enabled probe, restart or retest prior abilities. A known enemy/barbarian able to contact the test civilian is useful; if unavailable, finish the timing read and report **protection NOT_TESTED**, rather than waiting many turns.

1. Select an owned **Culture ACTIVE IV** city with no civilian in its center. Open the new left-side **人文考察·验证** entry, below **专业化诊断**, and left-click **① 创建验证考察团**. It is intentionally free and visibly marked 验证. Check one team appears and note the displayed original Spy capacity. Normal city production lists do not yet offer it.
2. Choose a revealed capital of a met foreign Major with the arrows; left-click **② 读取远程耗时**. Report the displayed travel/establishment numbers or exact UNKNOWN message. One screenshot is enough. The unit should remain in place: this tests the non-Spy duration interface, **not remote deployment**. A second already available destination is optional only if needed to distinguish constant/zero results, not a required history sweep.
3. Close the window, place this disposable test team where an enemy can contact it, reopen, and left-click **③ 标记接敌前位置**. After **actual enemy contact**, click **刷新／读取保护结果**. Check the same team remains owned by you and has safely retreated. Report the observed contact plus before/after position; manual movement alone does not establish protection. If it disappears, changes Owner or is destroyed, stop and report—do not recreate it to replace the evidence.
4. When done, left-click **结束并移除验证团**. Only the owned test-unit type is eligible. This is fixture cleanup, not a second gameplay exit/lifecycle gate. If creation is HELD or cleanup fails, stop/reload the original test copy and report; no repeated grant attempts.

Each substantive step answers a new native question: can the custom non-Spy unit exist with the intended flags; do travel helpers return usable values without a Spy operation; does native enemy contact preserve the unit/Owner through retreat. No mission success, history, city Tourism or Network acceptance follows from these observations.

## Remaining authorized N1 boundary

After the native gate, choose the independent remote-state/placement route based on evidence, then implement formal current-Spy-cost training, reliable source and archive binding, live nationwide cap/queue handling, remote deployment and required source-transfer/reattachment behavior. The current gate does not invent a travel formula, safe-return destination or information-reveal rule. Insufficient native support is a technical boundary, not permission to change Gameplay. N2/N3/U2 remain on hold.

## Deployment

Source `34e0d1f6f35a69e1ba3004ded6886afae8880c00` / B178.205 / modinfo205 deployed using existing W0003 tools after clean/pushed-source and OS game-exit verification. Receipt `B178.205-34e0d1f-playtest.json` is DEVELOP_ACTIVE; **202/202 source/runtime MATCH**, exact B177 and stable recovery retained, no pending transaction. Main remains unchanged. No game launch or native acceptance follows from deployment.
