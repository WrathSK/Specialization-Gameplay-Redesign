# v0.1 Playtest / Development contract

Document Owner: Codex
Workflow Revision: W0001
Baseline: B069.96 / modinfo96 / accepted D0025
Baseline tag: v0.1-playtest-b069.96

main worktree: `/Users/xutingzheng/Projects/Specialization-Gameplay-Redesign`
develop worktree: `/Users/xutingzheng/Projects/Specialization-Gameplay-Redesign-develop`
These are machine-local locations, not hardcoded tooling dependencies. Git worktree owns isolation; no second manually maintained source/runtime tree.

The original unchanged source/document checkpoint is `ca54045`. A following infrastructure-only commit adds this contract and deployment gates; the annotated baseline tag and both initial branches point to that final infrastructure commit, with identical Mod/ contents. This is a playtest milestone, not a final release or balance/performance certification.

## Deployment

Runtime is external `Sid Meier's Civilization VI/Mods/SpecializationP0` under the legacy workspace. Exact machine path stays in ignored main `local/config.json`. Runtime hash at baseline: `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df` (115 files). UUID unchanged. Neither branch creation nor push deploys anything.

Default deploy command is check-only. Apply additionally requires user-approved stable update, `--authorize-stable-update`, clean committed main and both reviewed hashes. Pending transactions, duplicate UUID, symlinks and unreviewed runtime changes still reject. Develop cannot use apply, even with the flag. No config copied to develop; its normal tests/builds remain isolated. Read-only comparison may explicitly use main's config.

No develop live testing this phase. Before any later temporary develop switch: explain “这将暂时切换运行包到develop测试版本”, obtain user authorization, preserve/hash the stable package outside Mods, design a separate explicit deployment/restore transaction, and verify restored package against stable commit. Do not bypass the stable guard or place duplicate UUID packages inside Mods.

## Hotfix and promotion

Classify reports first. Crash/save damage/turn blocker/confirmed severe performance/core ability failure: isolate minimal main fix, validate appropriately, coherent commit, authorized stable deployment and push main. Forward-port with Git cherry-pick/merge; conflict stops for review. Never hand-copy or bulk-merge develop into stable for one fix. Nonblocking UX/balance/future ideas go to backlog/develop. Stable promotion remains an explicit user decision; default commit/push is not deployment permission.

## Evidence and current session

User's current long play continues on the unchanged package. Earlier crash attribution is unresolved; prior performance counters have local evidence, not a new user PASS. Record future reports in [Playtest Backlog](../Status/Playtest_Backlog.md). Do not retroactively accept untested balance, remove frozen evidence or rewrite published history.
