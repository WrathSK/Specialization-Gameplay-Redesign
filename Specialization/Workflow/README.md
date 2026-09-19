# Codex Workflow v1 — W0001

Owner: Codex. Scope: development navigation/context only; user authorization 2026-09-18.
Design / Architecture always override Workflow. No Gameplay rule, implementation authorization or new Architecture revision is created here.

Entry: [Authority](Authority.json) → requested [batch manifest](P0-B1.json) → relevant rules/contracts → direct source → conditional dependencies → triggered full audit.

## Start protocol

1. Read repository AGENTS, Specialization AGENTS/README. Read Authority.json, current Spec/Architecture metadata and Status CURRENT block. Applicable nested instructions still apply. Old README D0025 and test README B051 introductory text are stale pointers, not current authority.
2. Confirm authorized Batch ID, branch, HEAD/upstream, staged/unstaged/untracked changes; preserve existing work. `PLANNED_NOT_AUTHORIZED` is not permission to implement. P0-B1 has only a context dry-run in this batch.
3. Run `python3 Specialization/Workflow/context.py check P0-B1`. It reads hashes/file sets/Git; never rewrites hashes, stages, deploys, launches game or runs runtime tests. Failure blocks trusting the index, never authorizes reset.
4. `python3 Specialization/Workflow/context.py plan P0-B1` lists ordered context and reproducible byte counts. `read P0-B1 N` emits one reference (zero-based N); use `all` only with adequate output budget. Do not treat truncated tool output as a completed read.
5. Read whole selected JSON objects with revision/state metadata, gates/notes and stable IDs. Follow normative references to enclosing qualification/ownership sections. Ambiguity expands to whole canonical section/file; no historical same-ID fallback. A formula alone is insufficient.
6. Read direct runtime source even if unchanged when adapting it. Unchanged indexed transitive modules may use reviewed summary pointers. Changed exported input, DB/config, dependency or behavior forces consumer review even if consumer hash matches.
7. Apply conditional/full-audit triggers; record expansion and reason in result. Only then implement separately authorized scope. Never skip writer/save/Shared boundaries to save tokens.

## End protocol

Review changed modules, effect IDs, callers and dependency changes. Run selected validation level; distinguish STATIC_CONFIRMED, LOCAL_SIMULATION_PASS and USER_GAME_TEST_PASS. Update Status, batch result, changed-module inventory/provenance, hashes and technical gates. Architecture revision changes only when its contract changes, not every batch. No full Architecture regeneration.

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

Old entry routing repeatedly exposes stale D0025/B051 and large Status history. Existing inventory is B076 (121 files); B077 adds4 and changes7 existing files. Runtime_Index preserves both provenance layers; this is not a claim all B077 source was freshly audited for W0001.

## Hash and summary trust hierarchy

1. Current accepted Design object + metadata and current Architecture contract are authority; actual source establishes implementation, tests establish only recorded scope.
2. Reviewed inventory/contract summary with matching hash/provenance navigates unchanged dependencies. Read referenced summary as needed; hash alone is not summary or correctness proof.
3. Completion/spike reports retain build/context/evidence limits. P0-A native events remain untested; unchanged source plus changed external DB/config still needs revalidation.
4. Pointers have no mechanical authority. Generated/unverified summaries, conversations/compaction and historical Status cannot supply current rules. Conflict → canonical sources, never guessed implementation.

Runtime hash change invalidates that inherited summary and affected consumers. New/deleted file blocks file-set validation. Dynamic/unknown dependencies require targeted full-runtime search and graph correction. Matching hashes never waive mandatory cutover writer audit. Lock files are maintained in reviewed Git diffs, not self-refreshing caches.

## Full audit triggers and scope

- Design revision / major Architecture change: complete current-authority impact review plus affected runtime; not every unrelated historical revision.
- Old writer cutover (B1 included), unknown carrier/writer, unexplained effect: search ALL Mod for exact identifiers/callers, inspect startup/load/manual/bridge/SQL attachment paths, full runtime regression. This is not necessarily full text of all unrelated assets.
- Network foundation / save schema / cross-profession shared semantic change: all consumers, state/load/epoch and full regression.
- Integration/release: full runtime, carrier/modinfo, save/deployment integrity audit.
- New/missing file, hash mismatch, incomplete dependency graph: stop summary reuse, inspect diff and connections; full runtime audit if closure cannot be bounded. Never simply rehash until green.

Historical entry allowed only for explicit current citation, Legacy review, regression explanation, unclear Design intent or user request. Historical rules never overwrite current canonical content.

## Validation levels

Local: isolated pure module. Dependency: direct producers/consumers + lifecycle. Shared: every impacted profession. Full: writer retirement/cutover, Network/save foundation, integration/release.

**P0-B1 requires full runtime regression because it retires Lv3Support**, despite narrow scope. Use a new wrapper recording intended B1 output deltas; keep unrelated maps, no-hidden-module-error assertions and historical files. Do not run every old standalone suite against incompatible version stamps or weaken tests until green.

`GAME_TEST_LOCAL` = static/mock, never engine PASS. `GAME_TEST_COMPUTER_USE` = UNRESOLVED / DEFERRED; requires reliable capability and explicit game/test authorization, does not override prohibition. `GAME_TEST_USER` covers remaining native behavior only; compress assertions into one minimal test after local verification. No game test for W0001.

## Failure-mode review

| Failure | Detection | Fallback / escalation |
|---|---|---|
| stale manifest / authority changed | version/hash + unique selector | current sources, refresh dependent manifests after review |
| stale hash / new file | Mod file-set and byte hash | inspect diff/new module, never auto-bless |
| hidden transitive dependency | direct import/shared-call inspection, writer search, regression | expand closure; full audit if unbounded |
| omitted old writer | full Mod ID/caller/SQL/load/control search at cutover | no cutover until exact allowlist complete |
| incorrect summary | contradiction with source/test/behavior | discard summary, read source, correct provenance |
| Shared change only local-tested | changed path/exported-contract review | Shared/full regression before commit |
| context too narrow | unresolved reference/gate or conflicting rule | enclosing section, then whole canonical file |
| external DB changed, source unchanged | evidence/config/catalog provenance mismatch | revalidate external evidence, no compatibility inference |
| compaction lost scope | Authority+manifest+git diff/current result | continue existing work, never restart/reset |
| old Status treated current | current-block/historical boundary | current source of authority; history evidence only |

## Schema, template and maintenance

[Batch.schema.json](Batch.schema.json) defines structure; [P0-B1.json](P0-B1.json) is the worked template. Replace all batch-specific references/gates; never inherit approval. Supported references: full file, metadata head, exact unique Markdown heading, exact unique row prefix, JSON Pointer + stable expected ID. No new Design DSL or copied formulas.

`context.py` uses only Python standard library. It validates supported schema fields, selectors, hash/file-set and version pins; cannot prove dependency completeness or Gameplay truth. `self-test` injects faults in memory, never modifies repo. Hash indexes are data, not executable update scripts; no write/refresh mode exists.

Contract routing reuses D0032_Adaptation: Canonical state / Permanent achievements / Shared facts / Network / Presentation / Performance; Implementation_Plan: Migration; P0_A report: actual implementation caveats. Do not duplicate these contracts here.

Official reference: [OpenAI AGENTS.md documentation](https://developers.openai.com/zh-Hans/docs/agent-configuration/agents-md). Existing required Status/Architecture entry now links W0001, so no governance rewrite or Codex configuration change is needed.
