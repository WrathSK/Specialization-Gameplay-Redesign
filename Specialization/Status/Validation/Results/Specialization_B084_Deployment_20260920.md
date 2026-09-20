# B084.111 / modinfo111 — P0-D1 deployment

W0003 standing development-test authorization active. Read-only OS process check confirmed no Civilization VI process before transaction; game not launched. Both Git worktrees were clean. Implementation commit: 33dc5cd05fa5abb589059e769a167727a89a91a2. Main remains e3651f9b7c90110f3a8890a7b12ca299996b306b, no promotion/tag.

Current source/runtime:137 files individually SHA256 identical; package digest `9607d29df06776d55d099a97ebac2f5f89b5c96e91de2a2b95800522b51e6083`.

Runtime:
`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Mods/SpecializationP0`

Backups/receipts root (outside Mods):
`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/SpecializationDeploymentBackups`

- B083 recovery: `.temporary-develop-backup-tt3xf2ww`,131 files, digest `a508c6def28d40ce18e95df67edfd39bd261b5703ddac33fc9a833fc9836e9af`, verified matches pre-switch package.
- B084 transaction: `B084.111-33dc5cd-playtest.json`, DEVELOP_ACTIVE.
- Stable recovery: `.temporary-stable-backup-mfh_37gf`, digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`.
- B082/B081 older recovery remains retained, untouched.

Used existing temporary_playtest restore then activate safety transaction; no raw package copy. No game config, save, external mod, Design or main source edited.

## User test (formal P0-D1, not precision experiment)

Confirm panel header `P0-B-084.111`. One Research ACTIVE III city with Campus and two eligible other domains: left **跨学科研究** gives BASE total,50% raw,final floor,configured district Science and residual count; right gives readable per-district composition. Verify native Campus Science, not just configured carrier. Example BASE7 => raw3.5 => +3 Campus Science.

Lower ACTIVE belowIII then restore; confirm single withdrawal/restoration. Save/reload once, no duplication. Brief idle should not repeat refresh sounds. No manual pillage required. If adjacency policy is readily available, compare unchanged BASE despite policy multiplier. Only send related summary/detail/native yield evidence if mismatched; no huge log requirement.

Status: local simulations and static SQL PASS; formal ability USER_GAME_TEST_REQUIRED. User integer-only primitive result is recorded separately and is not blanket native acceptance. No automatic P0-D2.
