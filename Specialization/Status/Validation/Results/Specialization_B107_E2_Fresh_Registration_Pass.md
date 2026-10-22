# B107.134 E2 — fresh registration / scoped native PASS

Reviewed 2026-09-26. Implementation c5bb3d9; deployed checkpoint d6e5ed0, modinfo134. Three original screenshots visually reviewed and moved to external app-support `Specialization/Status/Validation/Evidence/B107_E2_Fresh_Registration_20260926`; manifest.json records original filenames/bytes/SHA256, 3/3 hashes unchanged. No source, Design, main or deployed-runtime change in this review.

## Observed evidence

All three images show P0-B-107.134, Turn1 and Stirling (Test), city65536; the first identifies owner0.

| Original screenshot time | Visible result |
|---|---|
| 10:18:26 | E2 report: 来源正常建城; 等待首个合格区域完成; Potential0 / ACTIVE0 / 已完成投资0; 独立Game记录已保存; 所选城0/65536; 已登记1/2. |
| 10:21:09 | City specialization report: city65536 / NONE; Potential0 / ACTIVE0 / KNOWN; completed investments0, pending=false; Ledger=ABSENT_NO_WRITES. This is the absent investment ledger at P0, not evidence that the Game progression record is missing. |
| 10:23:47 | Same city: RESEARCH; Potential1 / ACTIVE1 / KNOWN; completed investments0, pending=false; Ledger=ABSENT_NO_WRITES. UI also displays 科研1级. Cheat Panel is visible; exact construction trigger is not established solely by the image. |

User additionally states: **“已投递，重启游戏后P2保留”**. Record this as explicit native confirmation of P2 persistence after restarting the game. These three images do not themselves show P2, the post-restart investment receipt count, or a restart boundary. Do not invent another screenshot or infer ACTIVE2/Governor/Network from Potential2.

## Acceptance and remaining scope

**USER_GAME_TEST_PASS** = user actually verified the tested native behavior, rather than local simulation. B107's simplified new-game single-city path is scoped PASS: automatic normal-founding registration, readable known NONE/P0, first Research specialization at P1, and P2 retained after restart (last item user report). No manual migration is needed for this observed Game-backed fresh record. This does not certify all E2 boundaries.

The preceding conversation simplified the fixture because locating old saves was burdensome. The old migrated control + new record mixed-schema coexistence check was explicitly deferred; retain it as native TODO, with the existing local regression still valid. Do not require the user to find old saves now.

P0-only coldload is not independently confirmed: the second screenshot still shows P0, but its timestamp alone does not prove a restart. Keep this narrow assertion unconfirmed without reopening/repeating the whole successful flow. Post-restart P2 is explicitly confirmed. Duplicate/early-event/failure-path protections remain LOCAL_SIMULATION_PASS, not newly native-certified. Four-profession coverage, changed-Governor ACTIVE recomputation, changed-route Network rebuild, unassigned recapture, destruction/rebuild and first AI-city Claim are not tested here.

## Disposition

Keep runtime B107.134; no fixes or redeployment requested/needed from these results. E2 remains partial; the fresh-city happy path has native evidence. No new Design decision, no immediate repeat test, no automatic Claim/F or cap expansion. Future remaining-E2 planning needs its own user direction/approval. Preserve B107-P0/B107-P2 test saves if available; no save contents were read or modified.
