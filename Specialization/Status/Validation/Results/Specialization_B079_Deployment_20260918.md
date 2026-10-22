# B079.106 development-test deployment — 2026-09-18

Authorization: user W0003 standing development-test deployment. Not promotion.
Implementation/deployment commit: b420a967f9b9ae468c5829a8de192dd443e9c6ea.

- Clean committed develop and main; origin/develop pushed before deployment.
- OS process checks before both restore and activate: no Civilization/Civ6/Aspyr process. No process terminated or game launched.
- Existing temporary_playtest restore→activate used, no raw copy or tool changes.
- Runtime B079.106 / modinfo106, 126 exact files equal source.
- Package SHA256: `c4b54513bf1b7becd7b7836743703d7532361bd617577f8278cca1f04f23fc5f`.
- No pending transaction remains.
- Main unchanged at e3651f9b7c90110f3a8890a7b12ca299996b306b, B069.96.

External archive outside Mods:
`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups/`

Active receipt `B079.106-b420a96-playtest.json` (DEVELOP_ACTIVE).
B078 recovery `.temporary-develop-backup-mp_dlg14`: 125 files, digest `555187afadf59c6153874488210511d43732345a0a4f27da2f92ca1b52ee3b32`, independently verified, referenced by old B078 receipt (STABLE_RESTORED).
Stable recovery `.temporary-stable-backup-5jhba75t`: 115 files, digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`, independently verified.
Keep receipts/backups intact; restore through reviewed tool/hash contract with game exited.

User opens game manually, verifies diagnostic header P0-B-079.106, checks repaired D/shadow caption and reads existing 专家与岗位. One prepared ACTIVE3/4 city + one worker reassignment is sufficient for the first native support check; Industry separately if already available. Extra basic support must be3F3P (Research/Culture/Commerce), Industry3F+BASE P with no retired III Gold. Other native/old ability yields are not part of this delta. No forced pillage/natural disaster/AI-war test.

Hash verification is not engine PASS. Implementation report: ../../../Architecture/v2/P0_B1_Specialist_Support.md. Stop for user feedback; P0-B2 not started.
