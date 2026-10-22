# B088.115 P0-E1 deployment — 2026-09-20

W0003 standing development-test authorization; game process absent before swap. No game launched. Develop source clean/committed/pushed at `3136810dd37ea2035b1a8ef1538a38d90e55b733`.

148 files source/live maps and SHA256 individually equal. Aggregate `ac5f27e8a3499840de06926297ebe985e7116340227577bbac296597cbed6651`; modinfo115. Main remains clean `e3651f9b7c90110f3a8890a7b12ca299996b306b` / B069.96.

Archive (outside Mods): `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups`.

- B087 recovery: `.temporary-develop-backup-urp0tt_6`; exact old147 files, digest `1f2d753c8d186d7cc75cbb42f43e2715ea49a716707025dbbd4accc2de15fa14`. Old receipt `B087.114-8dc6118-playtest.json` now STABLE_RESTORED.
- B088 receipt `B088.115-3136810-playtest.json`: DEVELOP_ACTIVE.
- Stable bridge `.temporary-stable-backup-ymf89rn0`: exact main115 files, digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`.
- Transaction used `temporary_playtest.py restore` on B087 receipt then `activate` on new B088 receipt. No raw copy bypass. No promotion/tag/main changes.

Rollback: with game exited, use current receipt's guarded restore for stable; to return B087 use reviewed B087 Git source/complete retained package via approved temporary deployment workflow, never edit/copy individual files into live.

Implementation evidence: [E1 report](../../../Architecture/v2/P0_E1_Identity_Evidence.md). Read-only native observation pending; deployment is not continuity PASS. In game report header must show P0-B-088.115. Two current entries: 记录城市身份 / 身份对照 (right click details). No E2/F implementation.
