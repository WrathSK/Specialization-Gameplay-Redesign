# B200 — interruption checkpoint: Expedition selection and card layout

**RESOLVED — resumed by the user on 2026-10-11.** Integrated209-test verification and source documentation are complete in the [B200 local result](Specialization_B200_Expedition_UI_Local.md); [Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state) governs the present boundary. No B200 deployment was performed. The following is the preserved interruption record, not active stop instructions.

At the interruption, the user requested stopping for quota and no commit/push. Their later instruction explicitly resumed B200 verification and finalization under the normal workflow.

## Exact source and runtime

- develop HEAD/origin: `396f534000996309a24c5e75103c464f2965cda0`; clean at this batch start. main remains `e901a224faae1274563fae07012116543bee6759`.
- Last deployed runtime remains **B199.226**, source `b4126a4628d4f2cdedbf4c9761c853b99a2d4946`, receipt `B199.226-b4126a4-playtest.json`. This turn performed no deployment or runtime modification.
- Working source labels are now **B200.227 / modinfo227**, uncommitted and not a deployed result. No staged changes intended. No Design, Gate, capacity, binding, persistence, task/activity backend, GC, ordinary Spy source, main or deployment-tool changes.
- Authority/P0-N1/Runtime_Index/Context_Lock still describe the committed B199 checkpoint. Their hashes have deliberately NOT been refreshed for this unfinished batch. Expected dirty mismatches are not corruption or permission to blind-rehash. Complete review/testing and update only named reviewed files on resume.

## B199 evidence already handled

User reports “Everything works fine” for the B199 flow; retain this as scoped USER_REPORTED_PASS, with a remaining card-layout defect. Two screenshots show T90 Sparta before and after explicit task selection; the task becomes selected/Start enabled, and the gold selector extends far below the content. Images do not independently demonstrate completion/END or every Wonder/foreign-inventory case.

Both originals were viewed, moved without renaming and SHA256-verified into ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B199/2026-10-11/`. Its manifest currently points to the planned `Specialization_B199_Expedition_UI_Native_Review.md`, **not created yet**. Create that concise review on resume; do not rearchive/rewrite originals. No new images require reading now.

## User-requested B200 scope and implemented changes

1. Fix overlong selected task frame: explicit content-measured row height replaces the auto-height/parent-height feedback loop. Row height = max(76, measured DetailsStack height +14); existing24px stats spacer retained. No current-facts query in layout.
2. Latest user clarification: task top overlaps drawer gold header and idle test instruction is unwanted. Scroll top43→56 clears header by7px; height decreases13px to preserve footer clearance. Removed idle “请选择任务，再确认开始。” on normal TASK open/READ; real error feedback and confirmation guards remain. Card and preview copy shortened to duration/no-reward information.
3. Native-like unit selection opens relocation in an owned city, task panel in a foreign city. Only a positive matching local selection event enters this path; actual native city lookup and live city reference determine ownership. Current phase, coordinate, readiness/AWAKE, activity lock and selected-unit checks are retained and rechecked after mode transition. Unknown/unavailable facts do not guess a menu. Completed one-shot/task-controlled teams do not gain new actions.
4. Existing open P0/manual/pending panel blocks automatic reopening via the existing UI-open marker. Generic native activity/mode/debug callbacks still only suppress our native Spy menus; they cannot auto-open ours. Ordinary-unit selection delegates native handler. Native captured selection listener is replaced explicitly; shutdown removes ours and calls original shutdown.
5. Opening a page does NOT select/dispatch/start anything. Existing manual buttons remain. No formal missions/rewards, repeatability, N2/N3/U2 or target expansion.

## Owned dirty files

- `Mod/ExpeditionSpyUI.lua`, `Mod/UI/ExpeditionSpyChooser.lua`: selection-only route.
- `Mod/UI/ExpeditionSpyWindow.lua/.xml`: measured card height, header gap, removal of idle prompt.
- `Mod/Text/ExpeditionGate.sql`: shorter bilingual prototype copy; no new keys.
- `Mod/Probe.lua`, `Mod/SpecializationP0.modinfo`: B200.227 labels.
- `DevelopmentTests/test_expedition_spy_task.py`: native selection fixture only.
- `DevelopmentTests/test_expedition_spy_gate.py`: GetSizeY fixture + modinfo227 assertion.
- `DevelopmentTests/test_expedition_spy_actions_ui.py`: clarify generic callback test name/docstring; assertions unchanged.
- New `DevelopmentTests/test_expedition_spy_auto_open.py` (14 tests) and `test_expedition_spy_card_layout.py` (6 tests).
- This checkpoint, Status CURRENT and current N1 slice: interruption navigation only.

## Completed checks versus remaining work

- Selection work: **60 focused tests PASS** (14 new auto-open + existing actions/task46). Includes actual Window no auto-choice, duplicate-open preservation, accepted task close, ordinary callbacks/unknown/locks/shutdown.
- Final layout work: **25 focused tests PASS** (6 new layout + B199 selection19), including existing failure-feedback checks. Earlier36 layout/selection/sidebar tests also passed before the added header-gap/idle-text delta; do not count these as independent broad coverage.
- Layout tests use simulated text measurements: oversized previous height440, repeated refresh, long-text grow/shrink and header/footer geometry. Native visual fit is still unverified.
- Parent reviewed diffs. Independent bounded helper/Chooser review found no blocking/actionable issue. Base and installed BES native chooser both define the chained OnShutdown; relevant native selection/activity/city-routing behavior was read. Native event ordering is not locally proven.
- No final combined suite, package/context/link checks, final full diff review, task metadata/hash synchronization, commit/push or deployment has been performed. Do not mark B200 fully validated.

Existing selection logs are preserved under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B200/checkpoint/` with SHA256 manifest. Layout25 PASS was returned by the worker, no raw log claimed. Source/new tests are the durable reproduction; temporary scripts are not required.

## Exact continuation

1. Read this note and `git status/diff`; preserve all dirty files. Do not restart native API investigation or repeat B199 screenshot review.
2. Review the final integrated B200 diff, especially the latest header/idle-copy changes and selection-only callback. Run one relevant combined suite: the12 modules in the B199 runner plus `test_expedition_spy_auto_open` and `test_expedition_spy_card_layout` (expected209 distinct tests, verify actual count). Use canonical DevelopmentTests first on sys.path; configured read-only database and existing Lupa. Known interpreter: `/opt/homebrew/bin/python3.14`; `PYTHONPATH=/private/tmp/spc-l2c-python:DevelopmentTests`, `PYTHONDONTWRITEBYTECODE=1`. Database path comes from existing main `local/config.json`/project_paths; do not copy or print configuration secrets. Do not run broad gameplay/stress.
3. Complete B199 native review, B200 local result/current UI plan/backlog and current Authority/manifest/runtime index. Register only the two new direct tests and reviewed changed-file hashes. Reconcile this paused note with final outcome; preserve previous frozen reports. Run links/selectors/context and diff checks.
4. This stop request explicitly says no commit/push now. A resumed task must follow the user's resumed scope before committing/pushing. Deployment only after completed checks, clean committed source and a NEW game-exit check under W0003; the earlier exit observation is not reusable later. Never launch/kill the game.
5. Minimal future native delta: select fresh idle team at home→relocation opens with no choice; arrive/explicitly select team abroad→task page opens with no choice; click task→frame fits card/header gap clean/no idle instruction; Start→closes, selecting during task does not reopen. Inherit B199 completion/close and earlier lifecycle evidence where unchanged; no save/load campaign.

Original stop point: finish this UI batch, not new gameplay development. This recovery work is now complete; use the linked local result and Status for the remaining native gate.
