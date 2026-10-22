# B098.125 E2 diagnostic entry failure — 2026-09-22

Evidence: USER_GAME_TEST_FAIL for requested diagnostic replies; reported ability loss not independently quantified. Ownership withdrawal/recapture/ACTIVE/network/save-load remain NOT_TESTED in this run. No runtime repair or deployment in this investigation.

## Observed

Three reviewed screenshots: 22:06:46 T8 `READING PROGRESSION_READ`; 22:08:14 T9 `READING GOVERNOR`; 22:08:15 T9 `READING SPECIALISTS`. All show B098.125 and selected own Aberdeen (Test), with no returned detail. They do not show a HELD_TRANSFER/recapture result or prove permanent records erased. User reports all effects unavailable. Source/runtime exact equality: 152/152, no missing/extra/mismatched file.

External originals archived with before/after SHA256 at `Specialization/Status/Validation/Evidence/B098_E2_Read_Failure_20260922/` in the app-support workspace; manifest plus current Modding/Database log snapshots preserved. No current Lua.log was available in the active log directory, so no native stack/API-return capture is claimed.

## Regression candidate and accountability

B095 commit `6bd903e` changed the global `Mod/Probe.lua:34` IsTestPlayer gate: added `PlayerConfigurations[pid]:IsHuman()` and GameConfiguration.IsAnyMultiplayer() checks. All human/mode reads must succeed; unknown returns false. Gameplay diagnostic dispatch returns before acknowledgement when this gate fails (`Gameplay.lua:305`), and many effect audits use the same gate. B098 inherited this change; the two latest AI-discussion commits changed documentation only.

UI screenshots reached READING, meaning UI-side qualification/dispatch did not immediately reject. A Gameplay-only gate failure explains the simultaneous missing replies and inactive Lua consumers, but initialization failure is not excluded without native evidence. Do not declare every native SQL effect disabled or the save corrupted from these screenshots.

Installed original Gameplay scenario scripts (Alexander/Australia) call `Players[pid]:IsHuman()`; configuration IsHuman usages found in original UI. The API reference lists Player.IsHuman in Script and UI: https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/Player . GameConfiguration.IsAnyMultiplayer is also listed in both contexts, so do not assert it is UI-only: https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/GameConfiguration . This establishes a better-supported candidate human-read path, not a captured absence of config.IsHuman on this Mac.

A small read-only Lua simulation executed the actual gate: config.IsHuman present/true => accepted; config.IsHuman absent while Players[pid].IsHuman=true => rejected. Conditional failure reproduced, not native API proof. Existing test_p0_e2.py mocked the newly assumed config method as available and tested missing => rejection; it failed to validate actual context availability. Prior local PASS therefore missed this integration risk.

## Next repair scope (not implemented)

Keep human-only and no-multiplayer scope; verify/use context-valid player facts rather than guessing eligibility or enabling AI. Add a bounded readable diagnostic rejection reason so an unavailable gate does not leave READING indefinitely. Test distinct UI/Gameplay API surfaces, human/AI/multiplayer/unknown, and the actual request acknowledgement path. Do not modify permanent investment/history, ownership matching, or Claim. First restore basic diagnostic/effect operation; only then resume E2 native round-trip. User need not repeat migration or continue ownership testing now.
