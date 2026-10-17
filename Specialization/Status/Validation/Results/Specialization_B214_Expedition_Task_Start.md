# B214 — Expedition task-start repair

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Source B214.241; deployed package is recorded separately below.

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

Not yet performed for B214; live remains B213.240 pending the guarded game-exit and deployment checks.
