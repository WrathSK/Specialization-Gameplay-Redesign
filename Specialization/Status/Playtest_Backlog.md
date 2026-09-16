# v0.1 Playtest Backlog

Document Owner: Codex
Baseline: B069.96 / modinfo96
This is the issue intake linked by the current Status; validation results remain in Status/Validation. Unknown turns are not invented. A baseline designation is not bug-free certification.

| ID | Category | Found build | Turn | Issue / evidence | Current long game impact | Stable hotfix | Develop only / next step |
|---|---|---|---|---|---|---|---|
| PT001 | PERFORMANCE | B068/B069.96 | Unknown | Prior movement storm and memory growth; B069 local fix, full user counters pending | Unconfirmed residual risk | Only if confirmed severe recurrence | Counters, shared caches, event maps first |
| PT002 | BLOCKER (triage) | Reported during B069 period | Unknown | Native pure-virtual abort; cause not attributed to this Mod | One crash reported, recurrence unknown | If attributed/reproducible; no speculative fix | Preserve evidence, triage on next report |
| PT003 | UX | B068.95/B069.96 | Unknown | Diagnostic labels/position and Potential display refinements | Nonblocking | No | Yes, pending user scope |
| PT004 | BUG / limit | Existing baseline | Unknown | Cumulative 32 new-city binding limit | May affect very large games | User decision if reached | Future handling; do not silently lift |
| PT005 | DESIGN IDEA | B067 onward | N/A | General eligibility and ownership/inheritance deferred | Unsupported ownership cases | No automatic enable | Isolated; separate approval |
| PT006 | PERFORMANCE | B069.96 | N/A | Bounded runtime audit log; receipts/cache lifetimes/scans | Investigation, no confirmed new regression | No speculative refactor | Architecture v2 |
| PT007 | UX / DESIGN IDEA | B069.96 | N/A | Existing carrier inventory and safe visible institutions | Nonblocking | No | Inventory before adding facades |

New entries: ID, category (BLOCKER/BUG/BALANCE/UX/DESIGN IDEA/PERFORMANCE), found build, turn, evidence, current-save impact, stable hotfix decision, develop disposition. No balance change is implied by an issue entry. User may continue long play without completing a new test batch.

## B076.103 runtime milestone follow-up

PT001 update: [short idle evidence](Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md) passes for tested expensive-work suppression; memory held at9.28GB/9.24GB in respective idle windows. This is develop evidence, not a main hotfix or long-session root-cause closure.

| ID | Category | Found build | Turn | Issue / evidence | Current long game impact | Stable hotfix | Develop only / next step |
|---|---|---|---|---|---|---|---|
| PT008 | BUG / diagnostic uncertainty | B076.103 |1| Five short-test reports show net_receive0, discount_ack0, inflight1; actual sends remain bounded | Functional initialization not demonstrated; cause UNKNOWN | None authorized | Preserve evidence; verify bridge readiness in later functional testing before claiming full network PASS; no automatic fix |
