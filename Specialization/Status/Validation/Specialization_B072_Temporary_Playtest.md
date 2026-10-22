# B072.99 temporary runtime deployment

Document Owner: Codex
Deployment: DEPLOYED_TEMPORARY
Validation: USER_GAME_TEST_REQUIRED (native file capability/turn delivery not verified)
Authorization: 用户“临时部署”，随后确认游戏已完全退出并要求开始部署。

- Source: develop 8b2ca3a305b79951419077301cd459d3cf69a62f, B072.99/modinfo99.
- Runtime digest: 4370c02e8944c2e109f1194542d7fa7055d9ef2a416bbd9c1531a375427f11fe; exact snapshot equals source.
- Stable main: e3651f9b7c90110f3a8890a7b12ca299996b306b, B069.96/modinfo96, unchanged/clean.
- Stable digest: 7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df, recovery package verified.
- Existing bounded deployment tool restored stable using B071 receipt, retaining outgoing B071.98; then activated B072 with a new receipt. No script modification, game start, configuration or save changes.
- Active receipt: external SpecializationDeploymentBackups/B072.99-20260914-playtest.json, phase DEVELOP_ACTIVE. Its stable_backup is the restore source; do not delete. Previous B071.98-20260914-playtest.json is now STABLE_RESTORED and retains develop_backup.
- No pending transaction. No main promotion.

## Minimal user gate

Start/load a separate test save; confirm B072.99, read Performance Counters. Runtime audit must show ACTIVE and file path. End one turn; verify header and one TSV summary. If DISABLED, return the reason; do not spend a long session assuming automatic logs exist. No OFF/TEST or network mutations needed. Native file capability remains uncertain; local tests do not prove game permissions.

Restore only after user authorizes and confirms game exited, using tools/temporary_playtest.py restore and the active receipt/reviewed hashes. Keep previous stable and B071 backups outside Mods.
