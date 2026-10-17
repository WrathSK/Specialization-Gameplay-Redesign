# B214 — Expedition task-start repair

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_PASS (PEOPLE task start/completion and observed Insight scope); WORKS/PLACES native evidence deferred. Source B214.241; deployed package is recorded separately below.

## Approved boundary and cause

The user authorized the narrow repair after the [B213 native failure](Specialization_B213_Expedition_Repair_Culture_UI.md#native-failure-review--2026-10-16). Successful mission validation returns a native city object. B213 passed that object as the second argument of `assert`, and the observed game rejected it even when the condition was true. This is a B213 regression, not evidence that the earlier Primary's mission implementation never worked.

Gate now raises the existing string reason only on INVALID/UNKNOWN. VALID continues without passing its city object through an error-message slot. Capacity, binding, persistence, target cancellation, timer, rewards, GC, institutions, collector and other Mods are unchanged. Probe/package labels advance to B214.241 only for build identification.

## Local evidence

- Added the observed native message-type restriction to the actual-Gate mission fixture. The existing PEOPLE success test failed before the fix with the same table-message signature; it passes after the fix.
- 88 targeted tests PASS: `test_expedition_missions`, `test_expedition_spy_task`, `test_expedition_spy_gate`. Coverage includes all three valid mission categories, invalid and unavailable facts, cancellation, independent activity/completion and native package registration. The existing external database fixture was supplied read-only from configured local settings; the initial unconfigured run had one dependency error, not a gameplay failure.
- Stock Lupa accepts `assert(true, {})`; this fixture models the observed game restriction. It does not identify the game's Lua version or prove every native behavior.
- No new user-game PASS. Frozen B213 failure evidence and raw logs remain unchanged and private.

## Steam launch-options investigation (read-only)

The screenshot shows the per-game Launch Options field. The proposed `cd ... && python3 ...` is shell syntax, not a Civ VI argument. Valve documents executable/argument launch configuration and macOS app-bundle versus binary launch behavior, but this does not establish shell-wrapper support in this user's macOS field. Do not prescribe Linux `%command%` recipes as verified macOS behavior. Sources: [Steam Support](https://help.steampowered.com/en/faqs/view/7D01-D2DD-D75E-2955), [Steamworks platform notes](https://partner.steamgames.com/doc/sdk/uploading?l=english).

The collector waits for Tuner and reconnects across loads. `--idle-exit 300` is a post-connection socket-unavailability exit threshold; it is not an automatic-launch trigger or direct proof of game exit. The 12-hour maximum still applies. No single-instance guard currently prevents duplicate collector launches.

Recommended future option: a user-invoked local launcher starts one collector in the background with a known Python executable and then asks Steam to launch the game. Preserve Steam's normal launch path; handle duplicate collectors and collector exit explicitly. If the Steam Play button itself must remain the sole entry, a separate watcher or a verified macOS wrapper requires its own small implementation/validation scope. Neither is implemented here. Steam, game configuration and the collector remain unchanged; the game was not launched.

## Minimal native continuation

Start the existing collector before testing. With an already-arrived bound team, start **风土考察** (or the same eligible mission that previously failed), confirm it enters the task, and advance through the displayed duration. Confirm return/completion and open **文化见闻** for the source/archive city: history should gain the corresponding civilization/category once. Existing B212 target-specific gates remain pending where not yet observed; no repeat training, cold-load or full lifecycle campaign is added for this assertion fix. Logs should capture TASK/activity/outcome plus the explicit Insight report; screenshots are needed only for a remaining visual issue.

## Deployment

B214.241/modinfo241 DEVELOP_ACTIVE; source 29391974f1ac887565f4ea8563a73b023acde4cd; receipt B214.241-2939197-playtest.json;219/219 MATCH. Automatic OS exit checks before both guarded switches; B213/stable recovery retained; no pending transaction. Configuration unchanged. No game launch or new native PASS.

## Native continuation — 2026-10-16

The user reports 风土考察 working and no available AI Great Work/Wonder targets. The existing collector session `session-20261017T042355Z-deee61` independently records:

- 04:25:11 UTC: TASK_PREPARING → TASK_RUNNING, no error; 04:26:50 PEOPLE SUCCESS for Khmer, Insight NEW; subsequent ARRIVED.
- 04:27:06 UTC: explicit source-city Insight report KNOWN, historical=1, effective=1, Khmer/PEOPLE effective=true.
- 04:28:14–15 UTC: another task starts/runs; 04:28:44 PEOPLE SUCCESS for Hungary, Insight NEW, returned=CENTRE, ACTIVITY → ARRIVED.

These support the narrow assertion repair, observed PEOPLE completions, return and the explicitly sampled ledger view. The second success has no later Insight report in this session; do not claim a sampled total of2. No new cold-load evidence. Legacy `[B191]` prefixes are inherited component tags, not build identifiers.

WORKS and PLACES share the repaired request/activity path, but their target readers and district/Wonder placement remain distinct native gates. User explicitly defers those two checks to future combined batches when targets exist; this does not block the next bounded batch and does not mark them native PASS. No request to create artificial targets or repeat PEOPLE.

Collector limitation: one PARTIAL_FRAME_AT_DEADLINE event occurs near the end, then INTERRUPTED. No task-error line is captured; this is not proof of gapless logging. The successful records above suffice for their stated scope. Raw logs stay at their existing ignored location. One inspected Builder screenshot is archived with SHA256 under the ignored B214 evidence folder; it is a UI reference only. Collector startup remains manual by user choice.

## Proposed next batch — B215 idle actions and bounded Tourism preparation

Not implementation authorization. Restore native **跳过回合 / 休眠** for an idle, exact owned Expedition through the existing UnitPanel action builder and native availability/request primitives. Current `ExpeditionSpyUnitPanel.lua` deliberately avoids the base builder (which registers Spy mission hotkeys), builds only TRAVEL/TASK, and suppresses native action clicks for teams. Thus adding icons alone is insufficient.

- Inspect the direct native/HD handlers and use an explicit action allowlist; do not re-enable native espionage missions/hotkeys or ordinary movement. Ordinary Spies/Builders stay unchanged.
- Recheck exact selection, owner, current activity lock and native eligibility at click time. Keep PREPARING/RUNNING/recovery/release locked. Manual idle sleep remains engine-owned, separate from task-owned SLEEP; determine the existing native wake route before release so the unit cannot be stranded. No saved field, capacity or binding change.
- Local tests: idle/locked/stale selection, native request arguments, manual sleep versus task-owned cleanup, ordinary-unit isolation. Native delta: skip once, sleep/wake once on an idle team; confirm normal dispatch/task remains accessible. No full save-load campaign. Merge available WORKS/PLACES evidence opportunistically, not as a mandatory prerequisite.
- In the same planning boundary, inspect the already identified whole-city Tourism modifier and direct loaded HD/native definitions for the accepted `+2 percentage points × effective Insights` rule. Verify truly city-wide scope rather than Great Work-only filtering. Reuse the existing city Insight ledger/current ACTIVE facts, preserve historical records when inactive, and avoid a second global scanner or persistent derived bonus.
- Do not automatically implement an unverified Tourism writer. If a matching native primitive is established, present the minimal implementation/native comparison before proceeding; otherwise report the exact technical gap. Planned following slice: local Tourism application with two distinguishable Tourism sources and ACTIVE on/off, then N3 separately. No new Design, auto-launch collector or unrelated audit repair.
