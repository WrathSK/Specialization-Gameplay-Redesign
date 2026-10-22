# B078.105 temporary development-test deployment — 2026-09-18

User authorized this deployment and temporary standing deployment permission until a USER-declared long-play node. Workflow W0003; this is not main promotion. No new implementation, no game launch, no P0-B1.

- Implementation commit: 5c3b254ebfc310d3c997fb36361eb75c957c159a.
- Clean deployment commit: 2a3689ee51670c1986f8d59142be731781ff6b19 (workflow docs only after implementation).
- Develop/source/live: B078.105 / modinfo105,125 files.
- Exact source/live file map equality: PASS; SHA256 package digest `555187afadf59c6153874488210511d43732345a0a4f27da2f92ca1b52ee3b32`.
- Main remains e3651f9b7c90110f3a8890a7b12ca299996b306b / B069.96. No merge/tag/promotion.
- OS process inspection before restore and activation found no Civilization/Civ6 process; no process terminated.
- Existing temporary_playtest restore→activate transactions used; no raw copy bypass. No pending transaction remains.

External archive (outside Mods):
`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/`

- Active receipt: `B078.105-2a3689e-playtest.json`, phase DEVELOP_ACTIVE.
- Outgoing B077 recovery: `.temporary-develop-backup-wdxbja_q`,125 files, digest `4b868bb8feed5486903c36298efe8ed73cccc9c0859d979290934dcca1c8a630`; recorded in B077.104-901e552-playtest.json (now STABLE_RESTORED).
- Stable recovery for active receipt: `.temporary-stable-backup-wld8zkjc`, digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`.
- All previous recovery packages retained. Restore via reviewed receipt/hash transaction with game exited; do not manually mix files or put backups inside Mods.

## Minimal combined acceptance

Open game manually; diagnostic build must show P0-B-078.105. Select prepared Research city and read 区域完善度 / 科研影子: Campus empty D0, Library+University D3, University pillaged D1, repaired D3 (skip already superseded preparation). ACTIVE4 needed only for shadow D×working Campus specialists, not D itself. Applied new yield remains0.

If refresh sound recurs: read existing Performance Counters, close diagnostics, idle ~20 seconds, read once more and report whether sound persisted with panel closed. No repeated turns/moves or long session required. Sound remains UNKNOWN, not declared fixed. Return screenshots with original time filenames.

Deployment hash PASS is not USER_GAME_TEST_PASS. Native reads and refresh sound await this unified user acceptance. Stop.
