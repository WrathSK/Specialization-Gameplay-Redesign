# Repository Workflow v1 — W0001

Maintainer: Primary. Scope: engineering operation and context navigation. Gameplay rules remain in user-accepted Design; technical contracts remain in Architecture.

## W0005 — Authority and repository knowledge

**W0005_AUTHORITY_SIMPLIFICATION_ACTIVE.** The user is the final semantic authority: accepted gameplay, scope, interpretation and ambiguity resolution, implementation approval, user-game acceptance, priorities/defer decisions and acceptance of major architecture tradeoffs.

Primary is the repository engineering, investigation, implementation, validation automation, documentation and Git operator. Primary may write Design only to record explicit user decisions, user-approved Design Talk/handoffs, or non-semantic formatting/link maintenance. Write permission does not imply semantic ownership. Proposals remain proposals until the user accepts them; forwarding advice is not by itself acceptance.

External discussion/advisory tools can explore alternatives, review plans and prepare handoffs, but have no independent repository authority. External discussion → user approval → repository record; no particular product, direct-write integration or conversation access is required. Existing `Document Owner: Codex` metadata means document maintenance responsibility, never ownership of gameplay meaning.

Do not invent missing gameplay, choose between genuine design alternatives, or silently change accepted rules to accommodate implementation/API limits. Report `DESIGN_DECISION_REQUIRED` and obtain the user's decision. Record technical limitations honestly; neither an Architecture recommendation nor a passing test grants semantic approval. Plan → user review → explicit implementation authorization remains unchanged.

### Roles and current assignment

| Role | Responsibility | Current project assignment |
|---|---|---|
| Primary | Authorized implementation, repository maintenance, technical investigation, validation automation, Git and deployment under existing gates | Codex |
| Advisor | Bug finding, architecture/Design review, bounded read-only source investigation, evidence and implementation proposals; no implementation | Claude, when assigned an explicit advisory task |
| Investigation | Long-running, topic-scoped research under the existing [Investigation protocol](../Reports/Technical/Investigations/README.md) | The separately user-authorized Investigation session under that protocol |

Only the user may change these assignments. They are recorded here, not in Authority.json or a role registry. All roles use the existing develop worktree; only one implementation agent is active. No additional clone, branch, worktree or synchronization mechanism is introduced. Session permission is resolved by R9 below. These are behavioral rules, not a claim of configured tool or operating-system enforcement.

### Shared advisory boundaries

These restrictions apply to both Advisor and Investigation, in addition to their task and area-specific limits. Existing W0001 reading scope, W0004 evidence/validation rules, user authority and `DESIGN_DECISION_REQUIRED` remain shared; neither role repeats or replaces them.

- Write only Markdown within the role's own explicitly authorized topic/report area, in files it owns or the user explicitly hands over. Do not edit the other role's files or move, delete or rename existing files. Area governance is maintained only by Primary under explicit governance authorization.
- Mod/source, tests/tools, Design/acceptance records, Architecture, Status, governance, Authority/manifests/hash metadata, configuration, runtime and external game/HD/Mod sources are read-only. No implementation prototypes, gameplay/test execution, deployment or game launch. Findings and candidate fixes go into the report; they do not authorize edits elsewhere.
- Git queries are read-only (`status`, `diff`, `log`, `show`, `rev-parse`; optionally `GIT_OPTIONAL_LOCKS=0`). No stage/add, commit/push, pull/fetch, branch creation/switch, checkout/restore, reset/clean, stash, merge/rebase, worktree operations or Git configuration changes. Primary's default commit/deployment instructions do not apply to these roles.
- Reports are advisory, even when Stable. The user reviews evidence and makes decisions; Primary records accepted decisions and implements only separately authorized scope. Checkpoint acceptance for Git is not gameplay acceptance or implementation authorization. Use the checkpoint process below; do not change shared indexes concurrently.

The existing Investigation Stage A/B/C protocol, report states and handoff remain in force. [Advisory guidance](../Reports/Advisory/AGENTS.md) defines its separate review area. Neither area's reports become mandatory reading for every task.

### R9 — Session Role Resolution

1. A product-level assignment does not authorize every session using that product.
2. Each session obtains its active role through the user's explicit task or conversation-level instruction, consistent with the current assignment above. No fixed phrase is required: “implement the approved B205” or “review this diff and write an Advisory report” can assign the corresponding role.
3. Once assigned, the role remains valid within that continuing task unless the user changes or revokes it.
4. Role persistence does not grant unlimited implementation authorization. Primary must still follow the approved batch, Authority, manifest and existing implementation gates.
5. A new or ambiguous session without an identifiable role defaults to read-only.
6. A session must not infer write authorization solely from the project assignment, repository access, historical conversations or the presence of an approved batch.
7. If a claimed role conflicts with the current W0005 assignment or another explicit restriction, stop the affected write operation and ask the user to resolve the conflict. Do not silently choose the more permissive interpretation.
8. After compaction or fresh-thread recovery, if role assignment is no longer visible in the session, ask the user to reconfirm it before any write. Do not reconstruct it from repository records or inference. Compaction alone does not require reconfirmation when the explicit assignment remains visible.
9. Adoption transition: the user's approval of this governance change confirms the existing main task session as Primary and the existing investigation session as Investigation; adoption does not downgrade either to read-only. This transition is not standing authorization for new sessions.

### Language convention

- **Conversation with the user is in Chinese** (user decision, 2026-10-16), for every session role: chat replies, plans, explanations, reports given in conversation and user test instructions. Understand Chinese or mixed-language user input normally; never require the user to write English.
- Written repository artifacts use clear, professional English: audits, investigation, advisory and validation reports, Status and other new technical documentation, code comments and commit messages. Preserve technical depth and evidence boundaries.
- Chinese remains the primary language for authoritative gameplay Design and player-facing content. Preserve the complete Chinese Design and the existing Spec/Content authority and acceptance process. Any separately authorized English Design reading page derives from the same accepted decisions, identifies its source revision and scope, and stays synchronized with affected accepted changes; it is not a second authority. Established Chinese names and localization identifiers require separate authorization to change.
- In user test instructions, refer to P0 panel buttons by their actual current Chinese labels, even when the surrounding instructions are English. Verify a label when uncertain; do not substitute an English translation or internal identifier. Specify left-click or right-click when the action depends on it.
- Apply English-first conventions to new technical writing without requiring duplicate Chinese technical reports or wholesale translation of existing documents. Existing edits remain task-scoped; frozen historical records stay unchanged. Historical translation and portfolio case studies require separate authorization.

These conventions change language only: existing document contracts, schemas, W0001 reading scope, user approval, evidence levels and Investigation Agent write permissions remain unchanged.

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

Fresh threads and post-compaction recovery follow these pointers with task-scoped reading. These sources recover project facts, not lost session authorization; apply [R9](#r9--session-role-resolution) before writing. Preserve unique durable information in the appropriate existing source; no conversation transcript, new memory system or mandatory handoff document. Frozen history stays unchanged. Historical tool restrictions do not override this active authority model; History is evidence, not the next-task queue.

### Advisory and Investigation local checkpoints

New topic Markdown/README files in [Advisory](../Reports/Advisory/README.md) and [Investigation](../Reports/Technical/Investigations/README.md#并行文件与git边界) remain ignored locally by default. The user grants Primary standing permission to commit/push Stable reports from explicitly authorized topics after the checks below; separate approval for each report/checkpoint is not required. This is publication permission only, not acceptance of findings, Design changes or implementation. Ordinary batches neither incidentally stage reports nor require publication to proceed. Root area guidance stays tracked. Later changes to tracked reports retain normal review and clean-source rules; ignore patterns do not hide them or relax source, deployment, hash, transaction-recovery or game-exit gates.

The report owner identifies exact Stable files, completed scope and unresolved questions, and pauses writes to those files → Primary reviews privacy, citations, evidence labels, ownership and the final diff → Primary explicitly force-adds only the reviewed ignored paths, obtains PASS from the [develop staged publication gate](../../tools/README.md#develop-publication-gate), commits/pushes and releases the checkpoint. Preserve all other work; never use `git add .`, `git add -A` or `git commit -a`. Unclear ownership, active concurrent writes or a failed check pauses only the affected publication, not unrelated work. Corrections return to the report owner unless the user explicitly grants Primary a narrowly scoped editorial handoff; that exception does not grant general ownership of another role's files. Already cited/review-hashed Stable files require coordination before further edits. Maintain only genuinely affected references/hashes after review; publication does not add reports to default context.

Authors prepare publishable reports before Stable handoff; Primary checks again before staging. Use repository-relative citations. External evidence retains source/mod identity, known version or Workshop ID, source-relative file/symbol/line or DB query, and relevant UI/Gameplay/ruleset context. Use existing configuration keys or clearly defined source-root labels instead of real home directories, machine-specific absolute paths, `file://` links or encoded equivalents. No reusable credentials, authentication cookies/session/token values or private configuration. External local-source locators are textual citations, not pretend public links or executable placeholder commands. Keep raw game files, logs, screenshots, saves and packages outside report areas; frozen originals remain unchanged. Author/Primary review remains behavioral; the develop staged publication gate adds bounded technical checks, not role enforcement or a guarantee that all sensitive content is detected. Unpublished reports cannot be the sole durable basis for authoritative recovery: adopted constraints belong in existing formal sources under the relevant authorization. Inspect reports only within the authorized topic; do not expand ordinary context.

## Current entry

[Authority](Authority.json) identifies current revisions, source/live status and requested batch manifest; [Status](../Status/Specialization_P0_Status.md) provides current progress/evidence/next boundary. Do not duplicate a current task or version ledger here. v0.1 implementation remains Research/Culture/Commerce/Industry only; Military/future Design does not expand runtime dependencies. Integrity PASS never authorizes implementation.

## Start protocol

1. Read repository AGENTS, Specialization AGENTS/README. Read Authority.json, current Spec/Architecture metadata and Status CURRENT block. Applicable nested instructions still apply. Resolve the session role under R9 before any write; reading current assignments is not session authorization. Historical introductory versions in test/report documents do not override current Authority/Status.
2. Confirm authorized Batch ID, branch, HEAD/upstream, staged/unstaged/untracked changes; preserve existing work. `PLANNED_NOT_AUTHORIZED` is not permission to implement.
3. Run `python3 Specialization/Workflow/context.py check <batch-id>`. It reads hashes/file sets/Git; never rewrites hashes, stages, deploys, launches game or runs runtime tests. Failure blocks trusting the index, never authorizes reset.
4. Choose the action-scoped reading path below first; a manifest context list is the implementation dependency envelope, not mandatory full ingestion for every action. `python3 Specialization/Workflow/context.py plan <batch-id>` lists ordered context and reproducible byte counts. `read <batch-id> N` emits one reference (zero-based N); use `all` only with adequate output budget. Do not treat truncated tool output as a completed read.
5. Read whole selected JSON objects with revision/state metadata, gates/notes and stable IDs. Follow normative references to enclosing qualification/ownership sections. Ambiguity expands to whole canonical section/file; no historical same-ID fallback. A formula alone is insufficient.
6. Read direct runtime source even if unchanged when adapting it. Unchanged indexed transitive modules may use reviewed summary pointers. Changed exported input, DB/config, dependency or behavior forces consumer review even if consumer hash matches.
7. Apply conditional/full-audit triggers; record expansion and reason in result. Only then implement separately authorized scope. Never skip writer/save/Shared boundaries to save tokens.

## Action-scoped reading and interruption recovery

| Action | Minimum sufficient reading | Expand when |
|---|---|---|
| Read-only question | Authority pointers, actual CURRENT, question-specific full section/object | Qualification, exception or source conflict needs enclosing/direct contract |
| User acceptance archive | CURRENT, current slice's full test/stop contract, submitted evidence and affected result/Status | A discrepancy requires the exact implementation or prior counterexample; archiving does not authorize a fix |
| Investigation | Relevant contract, direct implementation, existing negative evidence | Uncertain call path or evidence scope |
| Authorized implementation | Current slice, complete direct rules/source/test closure in manifest and conditional consumers | Writer switch, save/ownership or exported changes require exact caller/old-writer audit; never remove dependencies just because hashes match |
| Interruption/fresh-thread recovery | Git state, CURRENT, current slice, dirty diff and direct results | Deployment action requires actual receipt/runtime; unfinished transaction requires its own recovery contract |

`context.py plan` reports the dependency envelope without emitting source text. Read selected items, not `read all` by default. Hash integrity still reads all guarded bytes automatically; successful file lists need not become model context. Human Design reading pages are not added to mandatory agent reading.

Recovery procedure:

1. Confirm worktree, branch, HEAD/upstream and staged/unstaged/untracked changes. Preserve partial work; never reset to manufacture a clean tree.
2. Read CURRENT and its current-slice links, then direct results. Distinguish recommendation, explicit authorization, work in progress, local completion, recorded deployment and pending native validation.
3. Compare diff/commits with those records; consult the actual receipt only if deployment matters. A missing final message is not evidence that work or deployment failed; do not repeat completed actions blindly.
4. If authorization, provenance, an incomplete transaction or dirty edit is unclear, investigate read-only and ask only for genuinely missing information. Missing session authorization follows R9; repository recovery cannot supply it. A lock mismatch can be legitimate unfinished work or unexpected change; neither auto-accept nor discard it.
5. Review/validate the affected edits before updating only their review hashes. Record a short boundary/decision/negative finding in existing Status/plan only when needed for safe continuation. No per-tool journal, Memory.md or new hook.

Cross-machine handoff: clone complete Git history when selected regression uses `git show` baselines (a shallow clone may be insufficient); install the interpreter/Lupa versions required by selected tests. Real local config and external read-only Civ VI/HD databases must be supplied separately only for paths requiring them. Screenshots/native evidence, deployment receipts and recovery packages remain external; retrieve them when native evidence or deployment recovery is in scope. No screenshots means no claim of reinspection; no receipt means HEAD cannot identify the deployed package. Do not copy game files, saves or backups into Git. See [test dependencies](../../DevelopmentTests/README.md) and [deployment contract](../Architecture/Playtest_Workflow.md).

## End protocol

The write, metadata, Git and deployment steps below apply only to authorized Primary work. Advisor/Investigation finish through their own report and the [checkpoint handoff](#advisory-and-investigation-local-checkpoints); they do not update formal project state.

Review changed modules, effect IDs, callers and dependency changes. Run the W0004 v1 risk-selected validation depth below; distinguish STATIC_CONFIRMED, LOCAL_SIMULATION_PASS and USER_GAME_TEST_PASS. Update Status, batch result, changed-module inventory/provenance, hashes and technical gates. Architecture revision changes only when its contract changes, not every batch. No full Architecture regeneration.

Refresh hashes ONLY after source/references are re-read and reviewed. Carry unchanged evidence from named baseline; never auto-accept mismatches. Authority changes require review of the active/requested manifest before use, including unchanged filenames. Completed historical manifests retain their reviewed version pins; do not rehash or update all history to match today. A historical manifest cannot be reused as a current implementation gate without revalidation. Keep historical inventories frozen; current Runtime_Index holds inherited references plus explicit deltas. Checksum is not semantic review.

Primary: before commit inspect diff/branch/untracked/secret/temp boundaries and use only explicit approved paths. On develop, after staging and before commit, run `python3 tools/check_publication.py` (also invoked by the locally installed pre-commit hook); staged content requires PASS, and missing tools or incomplete scans are not PASS. Preserve the index and stop the affected commit on failure; do not bypass the gate or rewrite frozen evidence merely to pass. Coherent completed batch → commit develop → push origin/develop → verify matching HEAD/clean tree. Awaiting engine validation is committed separately from later validation. Deployment, main, promotion, tag and published-history rewrite require their existing explicit authorization. Stop at batch boundary.

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
- If validation expands to full regression or large stress, give the concrete risk reason in one sentence in the existing final report. No separate mandatory report, tier manifest, persistent tier state, telemetry, quota CSV/JSON/dashboard or historical snapshot mechanism. Account usage is recorded externally by the user, not maintained by the agent.
- Keep mechanical source/runtime hashes, file manifests, deployment equality, Git clean/sync and schema/reference consistency checks. Reliable scripts perform them; consume their summary (e.g. `143/143 files match`), not manual per-file re-analysis. Investigate mismatches; never silently refresh hashes to hide them. Hash equality is not gameplay proof.
- Docs-only work uses document/reference/schema checks and diff review, not gameplay regression. Once sufficient checks pass, do not broaden/repeat without new changes, failure or an unresolved concrete concern.
- Design Authority and DESIGN_DECISION_REQUIRED, plan → user review → explicit implementation authorization, W0001 loading, main/develop and canonical/deployed separation, commit/push, USER_GAME_TEST gates, LOCAL_SIMULATION_PASS ≠ USER_GAME_TEST_PASS, stable/temporary deployment, deterministic safety/rollback/backup and stop-at-batch boundaries remain unchanged.

`GAME_TEST_LOCAL` = static/mock, never engine PASS. `GAME_TEST_COMPUTER_USE` = UNRESOLVED / DEFERRED; requires reliable capability and explicit game/test authorization, does not override prohibition. `GAME_TEST_USER` covers remaining native behavior only; compress assertions into one minimal test after local verification. No game test for W0001.

### Runtime Impact Contract and targeted gates

This is Primary’s internal engineering responsibility, not an additional routine user-approval step. New Design, major shared-contract tradeoffs or scope expansion still need user decision. For a new or widened automatic runtime dependency, add this compact statement to the existing batch plan/result; reference unchanged accepted contracts instead of creating a parallel per-module manifest. Select L1/L2/L3 above and the relevant gates below before implementation. Changed usage assumptions require review even when a shared file's hash is unchanged.

**Runtime Impact Contract (normally one page):**

1. **Path and owner:** entrypoints, actual producer/consumer closure, authoritative inputs and availability; current versus permanent state; observable behavior that must remain identical and any separately approved DDR.
2. **Cause → scope → dependencies:** verified native signature/context, owner/city/reference/domain, cross-city/former-holder propagation, UNKNOWN fallback and its bound. List obsolete or unverified event names rather than silently relying on them.
3. **Read/write phases:** capture and reuse boundary, lifetime, invalidation/write barriers, copied returns and confirmation-time fresh reads; no retained native objects.
4. **Work and recovery:** relevant dimensions (cities, districts, buildings, D-needing cities, edges, former holders, reports); retained-state AND execution/attempt bounds; meaningful wake, deduplication, success/failure/load/exit; observer cost and residual uncertainty.
5. **Exceptions and compatibility:** inherited scoped exceptions with re-review triggers, save-shape/new-campaign requirement, affected dependent features, allowed fallback and stop condition. Unrelated historical debt stays deferred.
6. **Proof and native delta:** chosen T gates, actual modules versus stubs, before counterexample and after result, executed source/fixture closure and command; applicable inherited evidence, remaining user-game uncertainty and pass criteria fixed before testing.

| Gate | Select when | Required discrimination |
|---|---|---|
| T01 — Scope locality | Changing event routing/automatic consumers | Actual producer and real consumers, two local cities plus foreign/UNKNOWN/former-holder cases. Local-only irrelevant events do zero local city visits; necessary exits/cross-city propagation remain. |
| T02 — Invalidation closure | Changing facts, mutation or scheduling | A relevant mutation both invalidates the producer and reaches affected consumers; an unrelated mutation does neither expensive capture nor unrelated audit. |
| T03 — Capacity boundary | Changing bounded caches/working sets | Warm K−1/K/K+1 and the relevant 8/9/16/32-city D cases. Separate supported workloads from structural eviction risk and count native reads/allocations, not merely cache length. |
| T04 — Shared capture | Adding consumers or read-phase reuse | One cause through the real producer and 2–3 real consumers shares only a legal snapshot; mutation forces fresh post-barrier reads and return-copy isolation holds. |
| T05 — Recovery budget | Changing pending/retry/GC scheduling | No-progress repetition exhausts a bounded attempt budget; availability recovery with identical values and real same-turn changes wake the right work; successful siblings stay idle; no busy latch remains after exceptions. |
| T06 — Retirement and exits | Moving/removing ownership or cleanup | Exact owned IDs, former/ineligible/foreign/reused references, failures before/after native write, retained UNKNOWN and eventual exact withdrawal. Do not grant positive effects while a required withdrawal remains unconfirmed; preserve permanent history and irreversible-action receipts. |
| T07 — Catalogue/report cost | Changing building/catalogue/detail readers | Vary catalogue size independently from owned cities/present buildings; separate enumeration, presence, location, report allocations and diagnostic work. Prove the claimed reduction while documenting safety-required full checks and residual catalogue dependence; do not assume total work is catalogue-independent. Local counts alone do not establish CPU/heap/footprint benefit. |
| T08 — Freshness and ordered changes | Changing snapshots, confirmations or lifecycle | Two real changes in one turn, stale references/epochs, pending hold→confirmed loss, mutation invalidation, and fresh money/unit/project checks at confirmation. No one-update-per-city-per-turn shortcut. |

Use a faithful Lua 5.1 profile, ordered multi-listener events, hidden contexts without frames by default and explicit cold-load behavior where relevant. Each real defect needs a baseline counterexample that fails before and passes after; gates already satisfied at baseline are retained positive evidence, not forced failures. Frozen assertions are not weakened to accommodate a refactor. Record actual executed closure, not merely every imported filename. Risk-matched regression follows W0004; these gates are not a mandatory all-history suite for every edit.

**Static alarms, reviewed with the actual caller:** unavailable native event names in the measured build/context; scope accepted then discarded by a player scan; business calls through aliases into detailed/diagnostic readers; publish/frame retries without a progress budget; producer writes missing declared invalidation/exit ownership; uncounted observer reads/new labels. Mechanically provable violations can fail a check; ambiguous patterns require human review and scoped exceptions. Do not ban every city enumeration or silently rewrite an unverified native signature. Missing-event fallbacks need live-trigger coverage tests.

**Dependency-triggered re-review:** new consumer; manual-to-automatic transition; enlarged working set or frequency; new recovery path; longer retained-reference lifetime; changed native availability/lifecycle; observed regression. "Before the next profession" is only one possible trigger, not a grace period for widening current four-profession usage. Use the existing scheduling record for disposition; Report B's P1 means before the next dependent use, not automatically before every feature or completion of the whole backlog.

### Verification evidence storage — accepted 2026-10-24

User-approved evidence management; validation and proof obligations above are unchanged. Git retains a concise batch result: build/stage, tested source identity and recoverable version where available, exact command/environment/prerequisites, test outcomes/open counterexamples, important before/after measurements, unique failure evidence, limits and evidence locator. Do not commit cumulative expanded module→test matrices by default. Actual executed versus read-only/fragment evidence must still be captured; a compact summary does not waive tests or permit a new coverage claim.

The versioned refactor runner saves a unique complete run under ignored `local/refactor/`, including input manifest/fingerprint, failures/tracebacks and transcript hashes; it prints a compact review section. Never overwrite an earlier failed attempt. Keep only meaningful measurement changes in routine Git reports (use the prior local artifact as baseline), while independently preserving important first failures and corrections. Parent HEAD with dirty=true is not the tested source snapshot: verify the recorded input digest against the containing source commit before claiming recoverability. External DB/environment fingerprints identify inputs but do not archive them.

Local artifacts and hashes are **not permanent backups**. Re-running produces comparable new evidence, not the original historical execution. Irreplaceable or long-lived independent evidence requires an explicitly recorded durable archive (approved published Git evidence or a separately verified persistent archive with location/retrieval/checksum); do not finalize that claim with only local retention. Raw logs/screenshots/private inputs retain their existing publication review boundaries. Ordinary repeated PASS matrices remain local; this is not a new mandatory source-backup system.

The approved 31-file cleanup preserves original Git history and frozen result bodies. [Historical Closure index](../Status/Validation/Results/Refactor_Closure_History.md) records exact original paths, published commits/hashes and 11 narrowly enumerated obsolete relative links. Use that index for retrieval; do not claim all historical links work or exempt other missing inputs. Current Context Lock tracks current required files; original locks remain unchanged in their historical commits. No history rewriting or automatic historical cleanup follows from this rule.

### Refactor program execution boundary — accepted U1

The user authorizes S2–S10 after formal U1 synchronization, in the accepted dependency order and with separately traceable stage/batch commits and local results. Continue after normal stage completion; U2/U3/U4 are engineering checkpoints, not routine user-game or deployment stops. Request minimal native evidence only when a specific unresolved engine fact blocks dependent work. Do not deploy automatically, promote main or launch the game. U5 remains final user integration acceptance, with separate deployment and later main approval.

D4 project recovery must be driven by verified relevant events/fact or availability changes/existing necessary initialization, not new polling, per-turn city sweeps, unrelated events, unchanged pending retries or elapsed time. D5 aggregate counts do not replace unique completion proof. D7 automatic recovery requires an ability-specific distinction between transient unreadability and proved irrecoverable sub-record corruption before implementation. A8 entered bounded assessment and the user subsequently approved the exact eight-era correction; this approved delta is a separate batch, and unrelated era semantics still require decision. Preserve the accepted exclusions and stop only the affected path on new ambiguity, unexplained failures/assertion weakening, unsafe limitations or unclear ownership.

### Native delta and inherited evidence

USER_GAME_TEST targets the batch's new or changed native uncertainty, not every theoretical lifecycle risk. In the existing plan, distinguish (A) changed native behavior, (B) unchanged shared paths with applicable evidence, and (C) genuinely uncovered boundaries. Do not create a separate policy manifest/report. Every requested step must briefly identify what its PASS/FAIL would newly distinguish; repeat confirmation of unchanged, already-covered infrastructure is not sufficient information value.

Inherit named USER_GAME_TEST/LOCAL_SIMULATION evidence only for its actual source/path, fixture, ownership and observation scope. Keep targeted local regression and error protections; inheritance does not turn an untested native boundary into PASS. Confirm relevant implementation/configuration differences before reuse. Local mocks do not prove native persistence, instance withdrawal or event ordering.

Gameplay ability identity, persistent assets and current activation are distinct from a Probe's temporary ACTIVE/OFF, UI baseline, native-reader token and default-OFF control session. State explicitly whether a step tests gameplay or the test harness. OFF alone is not proof that owned native effects withdrew or the old consumer restored. Saving an enabled Probe copy, loading it to confirm OFF and re-enabling is not a default gate for every new yield.

Reintroduce a scoped native lifecycle assertion only for a concrete reason: changed lifecycle source; different state ownership/persistence/carrier/cleanup path; a native difference local tests cannot faithfully model; earlier evidence missing the relevant difference; an observed anomaly reasonably suggesting regression; or an explicit integration/cutover checkpoint. Explain the precise changed or anomalous path, the prior evidence gap, the two outcomes being distinguished and why existing local checks cannot answer. A theoretical possibility of save/load failure alone does not qualify. A known unresolved or failed boundary remains unresolved/failed; shortening a test must never erase it.

| Change / risk | Default user-game budget |
|---|---|
| Incremental ability/yield | One continuous session: new native primitive, decisive transition/reconfiguration, and its scoped withdrawal where relevant; no automatic save → END → exit → cold-load → re-enable loop. |
| Shared lifecycle unchanged and covered | Inherit scoped evidence + targeted local regression; no repeated native ritual. |
| Persistence, ownership, save schema or load reconstruction changed | Only the relevant save/load or transfer boundary. |
| Exit/cleanup/reference ownership changed, or concrete residual observed | Targeted withdrawal/recovery check; unrelated already-passed yield transitions need not repeat. |
| Important integration milestone / formal cutover | A broader integration test with explicit scope and purpose. |

Keep W0004's L1/L2/L3 local risk classification, USER_GAME_TEST gate, evidence levels, exact owned withdrawal, UNKNOWN/confirmed-loss distinction and deployment/save safeguards. This policy supersedes mechanical test recipes in earlier plans without rewriting frozen results. A failure blocks its dependent path; it does not by itself reopen all historical testing or halt unrelated development.

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
| compaction lost scope | Authority+manifest+git diff/current result; visible session authorization under R9 | recover project facts without restarting/resetting; missing role requires user reconfirmation before writing |
| old Status treated current | current-block/historical boundary | current source of authority; history evidence only |

## Schema, template and maintenance

[Batch.schema.json](Batch.schema.json) defines structure; [P0-B1.json](P0-B1.json) is the worked template. Replace all batch-specific references/gates; never inherit approval. Supported references: full file, metadata head, exact unique Markdown heading, exact unique row prefix, JSON Pointer + stable expected ID. No new Design DSL or copied formulas.

`context.py` uses only Python standard library. It validates supported schema fields, selectors, hash/file-set and version pins; cannot prove dependency completeness or Gameplay truth. `self-test` checks generic selectors using independent in-memory fixtures even when a task has only full references, then validates the real manifest/integrity. Targeted helper tests use temporary fixture files for missing-file and hash failure checks; neither edits Design/runtime. Run `PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_context_helper.py` (stdlib only). No selector is added to a real manifest merely to exercise a test. Hash indexes are data, not executable update scripts; no write/refresh mode exists.

Contract routing reuses D0032_Adaptation: Canonical state / Permanent achievements / Shared facts / Network / Presentation / Performance; Implementation_Plan: Migration; P0_A report: actual implementation caveats. Do not duplicate these contracts here.

W0005 changes active guidance only; W0001 selectors/hash checks, W0004 validation and deployment safety retain their existing responsibilities. No new persistent state is introduced.
