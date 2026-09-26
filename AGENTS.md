# Specialization repository guidance

The user is the final semantic authority. Codex may record explicit user decisions, approved Design handoffs and non-semantic maintenance; writing Design does not grant authority to invent or resolve gameplay rules. Genuine ambiguity or a technical limitation requiring changed gameplay → `DESIGN_DECISION_REQUIRED`, for the user to decide. See [W0005 authority boundaries](Specialization/Workflow/README.md#w0005--authority-and-repository-knowledge).

## Start and scope

- Read [project map](Specialization/README.md), [local guidance](Specialization/AGENTS.md), then follow [W0001 task-scoped loading](Specialization/Workflow/README.md#start-protocol): Authority → Status current block → requested manifest → relevant Design/Architecture/source. Do not read all history by default or infer authorization from a hash match.
- Check branch, worktree and existing changes before editing. Ordinary work is on develop; main is the last explicitly promoted trusted source. Separate worktrees remain independent; no hand-copying fixes or implicit promotion. Preserve user/uncommitted/unreviewed changes; do not stage unrelated files.
- `Mod/` in the canonical repository is the sole editable runtime source. External `Mods/SpecializationP0` is a deployment copy. Filesystem access is not project ownership: do not modify other Mods, HD, Workshop, game assets/configuration or launch Civilization VI. The user performs game tests.
- Plan → user review → explicit implementation authorization; stop at the approved batch boundary. Design presence does not authorize implementation. Tests use repository fixtures and explicit read-only external DB configuration; never weaken assertions for portability.

## Validation, Git and deployment

- Follow [W0004 v1](Specialization/Workflow/README.md#w0004-v1--quota-efficient-validation-policy): normal Medium/Fast mode, minimum sufficient L1/L2/L3 risk-matched checks. Local simulation is not user-game PASS. Preserve frozen evidence and accepted revision provenance.
- Coherent, verified batches (including docs/Design and implementation awaiting user tests) default to commit + push on the matching origin branch; read-only work produces no empty commit. Review diff/untracked/secret/generated-file boundaries before staging; verify HEAD/tracking after push and explain any remaining changes.
- No force push, published amend/rebase/history rewrite, destructive reset/clean, remote branch/tag deletion or baseline tag replacement without explicit user authorization. Stop on conflicts; repair published work with new commits.
- [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md) governs main hotfix/promotion and runtime transactions. Stable fixes remain minimal and approved; forward-port through Git. Never bulk-merge develop into main for one fix.
- W0003 standing develop-test deployment permission remains subject to that contract and any narrower task prohibition. It authorizes no implementation, promotion or game launch. Use the existing deployment tools, verified game exit, clean committed source, target/hash/staging/recovery safeguards; no raw-copy bypass. Uncertain/running game → defer replacement, never terminate it. The user decides when standing permission ends.
- [W0004 v2](Specialization/Workflow/README.md#w0004-v2--git-era-responsibility-boundaries): Git/GitHub protect source history; deployment tools protect external runtime recovery. Preserve existing backups, saves and frozen history; no routine duplicate source backups or automatic pruning. Consume deterministic check summaries, investigate mismatches.
