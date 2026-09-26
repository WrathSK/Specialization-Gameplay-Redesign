# Codex Workflow v1 — W0001

Maintainer: Codex. Scope: engineering operation and context navigation. Gameplay rules remain in user-accepted Design; technical contracts remain in Architecture.

## W0005 — Authority and repository knowledge

**W0005_AUTHORITY_SIMPLIFICATION_ACTIVE.** The user is the final semantic authority: accepted gameplay, scope, interpretation and ambiguity resolution, implementation approval, user-game acceptance, priorities/defer decisions and acceptance of major architecture tradeoffs.

Codex is the repository engineering, investigation, implementation, validation automation, documentation and Git operator. Codex may write Design only to record explicit user decisions, user-approved Design Talk/handoffs, or non-semantic formatting/link maintenance. Write permission does not imply semantic ownership. Proposals remain proposals until the user accepts them; forwarding advice is not by itself acceptance.

External discussion/advisory tools can explore alternatives, review plans and prepare handoffs, but have no independent repository authority. External discussion → user approval → repository record; no particular product, direct-write integration or conversation access is required. Existing `Document Owner: Codex` metadata means document maintenance responsibility, never ownership of gameplay meaning.

Do not invent missing gameplay, choose between genuine design alternatives, or silently change accepted rules to accommodate implementation/API limits. Report `DESIGN_DECISION_REQUIRED` and obtain the user's decision. Record technical limitations honestly; neither an Architecture recommendation nor a passing test grants semantic approval. Plan → user review → explicit implementation authorization remains unchanged.

### Durable recovery through existing sources

| Responsibility | Existing source / recovery entry |
|---|---|
| Accepted gameplay and unresolved design boundaries | [Spec](../Design/Specialization_v0.1_Design_Spec.md), [content map](../Design/Content/README.md), [acceptance ChangeLog](../Design/Design_ChangeLog.md) |
| Technical structure and durable constraints | [Architecture v2](../Architecture/v2/README.md), task contracts and cited [technical findings](../Reports/Technical/README.md); retain rejected/constrained approaches when forgetting them risks costly rediscovery |
| Current stage, implementation, unresolved work and next authorized boundary | [Status CURRENT block](../Status/Specialization_P0_Status.md), [Authority](Authority.json) and its current batch manifest; do not treat old plans as new permission |
| What has actually been demonstrated | Status-linked [Validation Results](../Status/Validation/Results/), with STATIC / LOCAL / USER_GAME_TEST scope intact |
| Exact source history | Git/GitHub; main = last promoted trusted source, develop = current development (including pending user validation) |
| Canonical source versus deployed runtime | Authority/Status live references plus deployment receipts and [Playtest Workflow](../Architecture/Playtest_Workflow.md); a commit does not prove deployment |
| Engineering operation / context freshness | Root/local AGENTS, W0001/W0004 here, Context_Lock and Runtime_Index review provenance |

Fresh threads and post-compaction recovery follow these pointers with task-scoped reading. Preserve unique durable information in the appropriate existing source; no conversation transcript, new memory system or mandatory handoff document. Frozen history stays unchanged. Historical tool restrictions do not override this active authority model; History is evidence, not the next-task queue.

## Current entry

[Authority](Authority.json) identifies current revisions, source/live status and requested batch manifest; [Status](../Status/Specialization_P0_Status.md) provides current progress/evidence/next boundary. Do not duplicate a current task or version ledger here. v0.1 implementation remains Research/Culture/Commerce/Industry only; Military/future Design does not expand runtime dependencies. Integrity PASS never authorizes implementation.

## Start protocol

1. Read repository AGENTS, Specialization AGENTS/README. Read Authority.json, current Spec/Architecture metadata and Status CURRENT block. Applicable nested instructions still apply. Historical introductory versions in test/report documents do not override current Authority/Status.
2. Confirm authorized Batch ID, branch, HEAD/upstream, staged/unstaged/untracked changes; preserve existing work. `PLANNED_NOT_AUTHORIZED` is not permission to implement.
3. Run `python3 Specialization/Workflow/context.py check <batch-id>`. It reads hashes/file sets/Git; never rewrites hashes, stages, deploys, launches game or runs runtime tests. Failure blocks trusting the index, never authorizes reset.
4. `python3 Specialization/Workflow/context.py plan <batch-id>` lists ordered context and reproducible byte counts. `read <batch-id> N` emits one reference (zero-based N); use `all` only with adequate output budget. Do not treat truncated tool output as a completed read.
5. Read whole selected JSON objects with revision/state metadata, gates/notes and stable IDs. Follow normative references to enclosing qualification/ownership sections. Ambiguity expands to whole canonical section/file; no historical same-ID fallback. A formula alone is insufficient.
6. Read direct runtime source even if unchanged when adapting it. Unchanged indexed transitive modules may use reviewed summary pointers. Changed exported input, DB/config, dependency or behavior forces consumer review even if consumer hash matches.
7. Apply conditional/full-audit triggers; record expansion and reason in result. Only then implement separately authorized scope. Never skip writer/save/Shared boundaries to save tokens.

## End protocol

Review changed modules, effect IDs, callers and dependency changes. Run the W0004 v1 risk-selected validation depth below; distinguish STATIC_CONFIRMED, LOCAL_SIMULATION_PASS and USER_GAME_TEST_PASS. Update Status, batch result, changed-module inventory/provenance, hashes and technical gates. Architecture revision changes only when its contract changes, not every batch. No full Architecture regeneration.

Refresh hashes ONLY after source/references are re-read and reviewed. Carry unchanged evidence from named baseline; never auto-accept mismatches. Authority changes invalidate all referencing manifests, including unchanged filenames. Mark dependent manifests STALE until refreshed. Keep historical inventories frozen; current Runtime_Index holds inherited references plus explicit deltas. Checksum is not semantic review.

Before commit inspect diff/branch/untracked/secret/temp boundaries. Coherent completed batch → commit develop → push origin/develop → verify matching HEAD/clean tree. Awaiting engine validation is committed separately from later validation. Deployment, main, promotion, tag and published-history rewrite require their existing explicit authorization. Stop at batch boundary.

## Reading classification / cost audit

| Category | Class | Minimum / escalation |
|---|---|---|
| Authority + Git | ALWAYS_REQUIRED | governance, pointers/current headers/queue, branch/status/upstream/diff |
| Design | ALWAYS metadata; BATCH_REQUIRED rules | complete selected objects + qualifiers; not four full professions |
| Architecture | BATCH_REQUIRED | named State/Shared/Network/Persistence/Presentation/Performance/Migration contracts |
| Status | ALWAYS current block | historical body CONDITIONAL for evidence trace |
| Runtime source | BATCH_REQUIRED direct | unchanged reviewed transitive summaries; changed dependency expands consumers |
| Data/carriers | BATCH_REQUIRED if effect touched | definition family, attachment and writer/cleanup path |
| UI/diagnostics | BATCH_REQUIRED if bridge/entry touched | otherwise CONDITIONAL; no inference from filename/comments |
| Historical revisions/reviews | HISTORICAL_ONLY | current explicit citation, Legacy/intent/regression trace or user request |
| Civ VI / HD evidence | CONDITIONAL | unresolved primitive/catalog/event; read-only, explicit version/context |
| Whole runtime/integration | AUDIT_ONLY or safety trigger | hash/file-set verification is byte I/O, not text context ingestion |

Runtime_Index retains named review baselines and deltas. Read current provenance; an unchanged file is not a claim of a fresh full-runtime audit.

## Hash and summary trust hierarchy

1. Current accepted Design object + metadata and current Architecture contract are authority; actual source establishes implementation, tests establish only recorded scope.
2. Reviewed inventory/contract summary with matching hash/provenance navigates unchanged dependencies. Read referenced summary as needed; hash alone is not summary or correctness proof.
3. Completion/spike reports retain build/context/evidence limits. Native event coverage follows the current scoped evidence; unchanged source plus changed external DB/config still needs revalidation.
4. Pointers have no mechanical authority. Generated/unverified summaries, conversations/compaction and historical Status cannot supply current rules. Conflict → canonical sources, never guessed implementation.

Runtime hash change invalidates that inherited summary and affected consumers. New/deleted file blocks file-set validation. Dynamic/unknown dependencies require targeted full-runtime search and graph correction. Matching hashes never waive mandatory cutover writer audit. Lock files are maintained in reviewed Git diffs, not self-refreshing caches.

## Full audit triggers and scope

- Design revision / major Architecture change: complete current-authority impact review plus affected runtime; not every unrelated historical revision.
- Old writer cutover (B1 included), unknown carrier/writer, unexplained effect: search ALL Mod for exact identifiers/callers, inspect startup/load/manual/bridge/SQL attachment paths. Preserve this cutover review; select affected regression under W0004 rather than automatically running full runtime regression. This is not necessarily full text of all unrelated assets.
- Network foundation / save schema / cross-profession shared semantic change: review all affected consumers and state/load/epoch; use L3 relevant broad regression for foundation/state risk, not unrelated historical suites.
- Integration/release: full runtime, carrier/modinfo, save/deployment integrity audit.
- New/missing file, hash mismatch, incomplete dependency graph: stop summary reuse, inspect diff and connections; full runtime audit if closure cannot be bounded. Never simply rehash until green.

Historical entry allowed only for explicit current citation, Legacy review, regression explanation, unclear Design intent or user request. Historical rules never overwrite current canonical content.

## W0004 v1 — Quota-Efficient Validation Policy

**W0004_V1_ACTIVE** — user-approved validation-depth clarification; W0001 progressive/task-scoped context loading remains unchanged. Normal Medium/Fast development mode remains. This replaces generic automatic-full-regression defaults above and in older workflow examples; historical batch evidence and explicit user-required acceptance tests remain intact.

Choose L1/L2/L3 from the actual changed path and failure cost before implementation. Use the default minimum sufficient checks, expanding only for a concrete risk, failed check or anomaly. A UI touching persisted state is not L1 merely because it has a UI. Validation should catch likely implementation errors before user testing, not attempt to replace Civilization VI itself.

| Depth | Actual risk / examples | Default sufficient validation |
|---|---|---|
| **L1 — Local / observable / low-state-risk** | UI, tooltip, presentation, wording; isolated well-defined effects that are quickly observable, do not pollute lasting state and are cheap to roll back | Syntax/static, task-targeted tests, a few directly related regressions, necessary deployment integrity. No default full historical regression, 10,000/30,000-notification stress or unrelated large combinations. Remaining native correctness uses a minimal USER_GAME_TEST. |
| **L2 — Cross-module gameplay behavior** | Yield calculation, specialist/building/district interaction, multiple modules or existing abilities in the same subsystem | Syntax/static, targeted tests, affected-subsystem regression, representative edges, deployment integrity. Full regression or large stress only for a concrete identified risk. |
| **L3 — Persistent state / infrastructure / hard-to-observe risk** | Save/load, identity, ownership transfer, persistence/migration, Network/state foundation, event ordering or concurrency-like behavior; high-cost failures difficult to observe briefly | Usually broad relevant regression, risk-relevant stress, integrity, save/load/state-transition simulation and representative failure/recovery. L3 is not permission to mechanically run every historical test. |

- Prefer lightweight local checks + a short USER_GAME_TEST for observable, reversible, low-state-risk errors. Preserve heavy validation for hidden state corruption, ordering and costly failure risks. Do not downgrade explicit safety or user acceptance requirements.
- If validation expands to full regression or large stress, give the concrete risk reason in one sentence in the existing final report. No separate mandatory report, tier manifest, persistent tier state, telemetry, quota CSV/JSON/dashboard or historical snapshot mechanism. Account usage is recorded externally by the user, not maintained by Codex.
- Keep mechanical source/runtime hashes, file manifests, deployment equality, Git clean/sync and schema/reference consistency checks. Reliable scripts perform them; consume their summary (e.g. `143/143 files match`), not manual per-file re-analysis. Investigate mismatches; never silently refresh hashes to hide them. Hash equality is not gameplay proof.
- Docs-only work uses document/reference/schema checks and diff review, not gameplay regression. Once sufficient checks pass, do not broaden/repeat without new changes, failure or an unresolved concrete concern.
- Design Authority and DESIGN_DECISION_REQUIRED, plan → user review → explicit implementation authorization, W0001 loading, main/develop and canonical/deployed separation, commit/push, USER_GAME_TEST gates, LOCAL_SIMULATION_PASS ≠ USER_GAME_TEST_PASS, stable/temporary deployment, deterministic safety/rollback/backup and stop-at-batch boundaries remain unchanged.

`GAME_TEST_LOCAL` = static/mock, never engine PASS. `GAME_TEST_COMPUTER_USE` = UNRESOLVED / DEFERRED; requires reliable capability and explicit game/test authorization, does not override prohibition. `GAME_TEST_USER` covers remaining native behavior only; compress assertions into one minimal test after local verification. No game test for W0001.

## W0004 v2 — Git-era responsibility boundaries

**W0004_V2_GIT_ERA_SIMPLIFICATION_ACTIVE.** Git/GitHub provide canonical source history/recovery/provenance; deployment tools protect the external runtime transaction; automated tests follow W0004 v1; USER_GAME_TEST establishes native behavior. Keep Design, approval, isolation and batch-stop gates unchanged.

Stop routine full source backup trees, ordinary pre-edit “before” snapshots, extra source-history hash inventories and manual per-file hash narration. Known-good commits/main provide source recovery; Git push provides remote source backup. This does not authorize reset/clean/history rewrite or deletion of existing DevelopmentBackups/Historical. Accepted Design revision artifacts and frozen evidence retain independent semantic/provenance value; user saves are not source history.

Existing files retained after narrow inspection:

- Authority: accepted pointers/current task/live-vs-source distinction; not replaced by HEAD alone.
- Context_Lock: reviewed-context freshness, not source recovery.
- Runtime_Index: per-file review_source/provenance and new/deleted-file detection; a clean Git tree alone does not prove reviewed summary freshness. Keep its current hash check, do not add another inventory.
- Batch JSON: scoped rules, authorization boundary, old-writer and validation gates; not commit history.
- Status: actual user acceptance and unresolved technical gates; not inferred from commit existence.
- Deployment receipt: external state and recovery paths, which Git cannot observe. Existing reports remain frozen; future routine records are concise: build, source commit, result/equality, receipt reference and abnormal events only. Use existing Status/record locations; do not require a new separate report or copy receipt mechanics into multiple files.

No tooling/state architecture change: retained indexes still require reviewed hash updates under W0001. Runtime backup retention is **not** claimed simplified: current restore checks require the recorded stable backup; transaction failure recovery may require the outgoing complete runtime, including non-Git evidence. Preserve these until a separately verified bounded-retention change can keep those guarantees. Do not delete historical backups or introduce cleanup in this policy update.

## Failure-mode review

| Failure | Detection | Fallback / escalation |
|---|---|---|
| stale manifest / authority changed | version/hash + unique selector | current sources, refresh dependent manifests after review |
| stale hash / new file | Mod file-set and byte hash | inspect diff/new module, never auto-bless |
| hidden transitive dependency | direct import/shared-call inspection, writer search, regression | expand closure; full audit if unbounded |
| omitted old writer | full Mod ID/caller/SQL/load/control search at cutover | no cutover until exact allowlist complete |
| incorrect summary | contradiction with source/test/behavior | discard summary, read source, correct provenance |
| Shared change only local-tested | changed path/exported-contract review | affected-consumer regression at W0004 depth; broaden for identified state/foundation risk |
| context too narrow | unresolved reference/gate or conflicting rule | enclosing section, then whole canonical file |
| external DB changed, source unchanged | evidence/config/catalog provenance mismatch | revalidate external evidence, no compatibility inference |
| compaction lost scope | Authority+manifest+git diff/current result | continue existing work, never restart/reset |
| old Status treated current | current-block/historical boundary | current source of authority; history evidence only |

## Schema, template and maintenance

[Batch.schema.json](Batch.schema.json) defines structure; [P0-B1.json](P0-B1.json) is the worked template. Replace all batch-specific references/gates; never inherit approval. Supported references: full file, metadata head, exact unique Markdown heading, exact unique row prefix, JSON Pointer + stable expected ID. No new Design DSL or copied formulas.

`context.py` uses only Python standard library. It validates supported schema fields, selectors, hash/file-set and version pins; cannot prove dependency completeness or Gameplay truth. `self-test` injects faults in memory, never modifies repo. Hash indexes are data, not executable update scripts; no write/refresh mode exists.

Contract routing reuses D0032_Adaptation: Canonical state / Permanent achievements / Shared facts / Network / Presentation / Performance; Implementation_Plan: Migration; P0_A report: actual implementation caveats. Do not duplicate these contracts here.

W0005 changes active guidance only; W0001 selectors/hash checks, W0004 validation and deployment safety retain their existing responsibilities. No new persistent state is introduced.
