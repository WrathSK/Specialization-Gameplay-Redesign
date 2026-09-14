# B069.96 playtest workflow setup — 2026-09-14

Document Owner: Codex

Preflight: main at 3382d7d9291052790a08e35b27e74c916316f17a; origin/main confirmed same through ls-remote; only main worktree; no local unpushed commits. 115 changed/untracked normal project files were pending from later development. All 725 candidate files (8,174,277 bytes) checked for excluded tree/symlink/obvious secret patterns. B061 isolated executable experiments remain ignored under local/; tracked B061 historical reports are intentional audit evidence. Current B062 Commerce retains some B061-named database identifiers: names alone do not identify failed implementation.

Existing Git credential authentication confirmed GitHub WrathSK/Specialization-Gameplay-Redesign private=true, default main. No new credentials or global identity changes. Resolved existing identity used.

Original source/docs saved unchanged as ca540456ff1d0610281085ba6026b21f636933e9. Infrastructure is a separate commit: root/nested governance, README, current architecture/status, deploy gate/tests, workflow/backlog/v2 plan. Tag v0.1-playtest-b069.96 is assigned to the infrastructure-complete commit, both initial branches share that node. Both commits have identical Mod and Design trees.

STATIC_CONFIRMED: 115 canonical/runtime files equal; modinfo96; source package digest 7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df. D0025 SHA256 81dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b retained. No deployment/game configuration/gameplay changes, no game launch.

LOCAL_SIMULATION_PASS: DevelopmentTests/test_deployment.py uses disposable actual main/develop Git fixtures; rejects absent authorization, develop branch and dirty main; still checks duplicate UUID, source/runtime hash mismatch, safe transaction, injected rollback, independent backups, unknown runtime files, symlinks and unrelated files. These are local tests, not a new Civ VI validation claim.

Prior instructions did not contain automatic coherent commit/push; active README said the opposite. G0009/root AGENTS now persist the approved policy. Earlier historical reports are frozen. Performance evidence remains unconfirmed in game; user's long-play designation supersedes the former pause, not its evidence level.
