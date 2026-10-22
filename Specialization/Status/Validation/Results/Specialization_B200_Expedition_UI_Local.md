# B200 — selection-driven sidebar and measured mission cards

Source checkpoint: **B200.227 / modinfo227**. **LOCAL_SIMULATION_PASS; native visual/event behavior USER_GAME_TEST_REQUIRED.** Resumes the [interruption checkpoint](Specialization_B200_Expedition_UI_Checkpoint.md) and records the [B199 scoped acceptance](Specialization_B199_Expedition_UI_Native_Review.md). Deployment is separate: the last recorded runtime remains **B199.226**, source `b4126a4628d4f2cdedbf4c9761c853b99a2d4946`, receipt `B199.226-b4126a4-playtest.json`. No B200 deployment or game launch occurred in this source-finalization batch.

## Applied changes

- Mission row height comes from measured `DetailsStack` content: `max(76, height + 14)`. The selected outline follows an explicit row height and no longer feeds its previous height into an auto-sized parent. Content can grow or shrink with text. The existing stats spacer remains. This explains the local sizing feedback defect; the actual native rendering still needs observation.
- Mission scroll top moves from43 to56; its height reduces by13 to preserve the footer boundary. This leaves7px below the header. Normal idle TASK open/READ no longer shows “请选择任务，再确认开始。”; task and preview text retain only duration/no-reward information. Error feedback and confirmation guards remain. Two existing bilingual keys are shortened; no new localization key or icon asset.
- A positive, matching local unit-selection event opens **派遣到新城市** in a currently owned city or **任务** in a foreign city. Routing requires the exact current selected team, matching published coordinates, native readiness/AWAKE and a readable current city reference. Unknown facts do not guess a page. Phase/task locks and post-interface-transition checks remain.
- Automatic opening only presents the page: no city/task is preselected and no travel/task command is submitted. The existing open-window marker prevents duplicate events from replacing a choice or diagnostic/pending window. Generic native activity/mode/debug callbacks stay suppression-only. Ordinary units delegate to the native selection handler; shutdown removes this wrapper's listener and chains native cleanup.

The B200 selection behavior supersedes B196's previous silent-selection direction; explicit buttons still work. No changes to Gate, capacity, source/name binding, task/activity backend, one-shot completion, persistent state, ordinary Spy source, Design, GC, main or deployment tools. Formal training/reattachment/persistence, repeat missions, N2/N3/U2 and rewards remain held.

## Update and ownership boundary

Trigger: positive selection of this local team's unit. Scope: one selected unit/current city and one presentation open; no new world/player scan or periodic callback. Needed facts: current identity/phase/coordinates/readiness/activity/city owner. The existing Gate scalar view remains authoritative for phase/lock; the UI does not persist a second task state. Native predicates are rechecked around mode transition, with no new cache. Existing Window owns its bounded rows/snapshot and open marker; close releases them. The chooser owns one replacement selection subscription and removes it on shutdown. Layout/resize reads measured controls only, not city inventories.

## Local verification

**209 distinct targeted tests PASS** in one combined run:189 relevant B199 tests +14 selection-routing cases +6 card-layout cases. Actual Lua runs with mocked Civ VI controls/events; the configured gameplay database is opened read-only for existing package/SQL checks. Python3.14, existing Lupa lua55; no dependency installation or external runtime writes.

Coverage includes own/foreign routing; unknown/current-reference/readiness failures; task-held/complete/locked phases; mismatched and repeated notifications; mode-transition revalidation; ordinary-unit delegation and shutdown; actual Window no-auto-choice/request behavior; content growth/shrink and repeated resizing from an oversized old height; header/footer geometry and preserved errors. Relevant earlier travel/name/source/activity/ACK/task tests remain intact. Package files/entry points, XML and bilingual localization are checked. No broad gameplay/stress suite or native performance claim.

Reproduce with the configured `SPC_DEBUG_GAMEPLAY_DB`, Python and Lupa described in [test setup](../../../../DevelopmentTests/README.md):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s DevelopmentTests -p 'test_expedition_spy_auto_open.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s DevelopmentTests -p 'test_expedition_spy_card_layout.py'
```

Combined run modules: `test_expedition_spy_relocation_ui`, `test_expedition_spy_sidebar_ui`, `test_expedition_spy_actions_ui`, `test_expedition_spy_task`, `test_expedition_spy_gate`, `test_expedition_spy_activity`, `test_expedition_spy_activity_report`, `test_expedition_spy_activity_diagnostic_report`, `test_expedition_spy_activity_failure_report`, `test_expedition_spy_name_pool`, `test_expedition_spy_selection_ui`, `test_expedition_spy_locations`, and the two new files above. Raw combined log is retained under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B200/final-local/`, with a SHA256 manifest. Earlier partial logs remain unchanged.

Independent bounded source review found no actionable defect. Local simulated text measurements and event ordering cannot prove native fonts, UI scale/wrapping or real selection callback timing. Context/schema/integrity, changed-link/anchor and final diff checks complete the source checkpoint; they do not upgrade native evidence.

## One minimal native UI session

Only after a verified B200 deployment. If the prior one-shot team is finished/held, use P0 **人文考察·验证 → 结束并移除验证团**, then the usual source and **① 创建Spy验证团**. No save/reload campaign.

1. Select a fresh idle team in your own city: **派遣到新城市** opens, with no destination chosen. Choose a destination and **确认派遣**. This tests home selection routing without automatic input.
2. After arrival, select the team: **任务** opens with no task chosen. Click **无奖励验证任务**. Check that the gold outline fits the card, its top clears the header, and the idle instruction line is absent. This tests foreign selection routing and the changed native layout.
3. Click **开始任务**: the sidebar closes. Selecting the team while the task is controlled must not reopen it. This checks that the new selection hook respects the existing task lock; unchanged two-turn completion/END evidence need not be repeated as a separate campaign.

Keep real errors visible and stop that path if routing/layout is wrong. Native fit remains pending; no formal-N1/repeat-task/reward work begins automatically.
