# Refactor program — S0/S1 review at U1

Date: 2026-10-24
Maintainer: Primary, explicitly assigned by the user under W0005
Review basis: develop `25327e7808f39da692b0270727047d1a3988e958`; runtime B271.298; Status S0718; accepted A0181 / D0057
State: **U1_REVIEW_REQUIRED — S0/S1 delivered; S2 not started**

## 1. Scope and status

The user's handoff authorizes S0–S10 in the order of the [Advisor plan](../Advisory/Refactor_Program/Refactor_Program_Plan.md), with U1/U2/U3/U4 and the plan's six stop conditions. The handoff does not accept the recommended D-1–D-15 answers. S11/U5 is user native acceptance; main promotion remains a separate decision after U5.

This checkpoint records the already explicit decisions in Status and the existing [follow-up scheduling record](Audit_Followup_Priorities.md#refactor-program-intake--2026-10-24). That record contains the current-HEAD intake, not a second finding registry. The decision sheet below and the [text diff](Refactor_Program_U1_Text.patch) are review artifacts only. No patch has been applied to AGENTS, README, Design or Architecture. No runtime, tests, tools, deployment, main or Advisor files change in S0/S1. Publishing these review artifacts is not acceptance of their proposed rules.

The user's five explicit decisions are recorded there: D4 already implemented; constraints before refactor; B271's treasury/retry/GC defects folded into S4 rather than hotfixed; pending-network hold direction accepted with exact semantics awaiting U1; A8 and ownership gameplay semantics excluded. All other stages remain behavior-neutral except the DDR choices explicitly confirmed at U1.

## 2. U1 decision sheet

Every answer is **PENDING_USER_CONFIRMATION**. The following prefilled answers reproduce the Advisor's recommended defaults, with current-source qualifications made explicit. The user may accept all defaults together or replace individual numbered answers, but the cold-load partial-loss exception below still requires an explicit choice; it has no implied default. Qualifications that preserve existing contracts are not new gameplay choices.

| Decision | Recommended answer for approval | Player-visible consequence / guard |
|---|---|---|
| **D-1 — Pending network** | Hold the last actually applied network-derived carriers, without withdrawal or rewrite, during route-topology pending/UNKNOWN. The combined local/network Standardization carrier is held as a whole in this state. Recompute on new confirmed facts, including confirmed route loss. Existing confirmed identity, ability-specific ACTIVE, owner and REALLOCATING exits take precedence. Network-dependent input changes wait. At cold load, valid saved carriers are the temporary last-applied output. Apply to every live network-dependent carrier writer, including Commerce, CultureNetwork and StandardizationEffects. | Commercialization does not disappear during transient revalidation. Unknown does not mean empty, but confirmed ineligibility does not gain an indefinite hold. No new ACTIVE/source gate is imposed. Transactions keep their existing confirmed-input and receipt requirements; already signed contracts do not gain a new route prerequisite. |
| **D-2 — One unreadable city** | Isolate its capture failure; retain its reference-valid last-known contribution, or no contribution if never reliably known, while other readable cities proceed once route topology is confirmed. New confirmed node contributions may update effects alongside that retained contribution. Preserve explicit per-node unknown/retained provenance; hold an undecomposable saved aggregate until needed facts are available. | One city no longer freezes the entire network. Confirmed owner/reference/qualification loss overrides retention. Mixed retained/new data must not masquerade as wholly fresh evidence for transactions. |
| D-3 — Failed startup dependency | Record FAILED; skip actual dependents as SKIPPED_DEPENDENCY and report. No degraded running; preserve current startup order. | Normal behavior unchanged; failures are contained and visible. |
| D-4 — Three full-turn projects | Preserve common behavior; for differing paths use the conservative existing policy: UNKNOWN retains access markers, queues with more than one item give an explicit reason without auto-start, and a project no longer current is abandoned as the existing Dialogue/Engineering paths do. | Clearer blocked-state messages. This does not erase ambiguous CALLING/native-outcome receipts or authorize replay; unexpected irreversible-state conflicts stop the affected work. |
| D-5 — Crew completions | Grant every completion proved by the aggregate counter. Exit stale HELD only after proving no unbound Crew; resolve CALLING by re-observing one unbound Crew. | Prevent loss of paid Crews. Aggregate evidence must still attribute each unit/order/source uniquely; ambiguity remains held, not guessed or duplicated. |
| **D-6 — Missed ticks / unknown Reputation** | Pause without credit for the unreadable gap, then resume Tradition/Reputation. Unknown Reputation at ACTIVE IV means no Reputation bonus, not withholding all otherwise valid Commercialization Gold. | A transient fault does not permanently disable growth or all Commercialization. This is an explicit DDR to record in accepted Design, not a claim that the present missed-gap code already resumes. |
| D-7 — Invalid profession sub-record | Hold only that ability; identity and other valid abilities continue. Envelope/reference/identity corruption retains its existing wider safety boundary. | Ability-level fault isolation; no fabricated historical data or silent repair of invalid fields. |
| D-8 — Anchors and pillage | Share the sample once; retain each ability's current eligibility and pillage policy. | No unified new gameplay rule. |
| D-9 — Ordinary-building ontology | Defer unification to the fifth-profession program. | Existing eligibility remains. |
| D-10 — Development target rules | Move UI target selection rules to Gameplay without changing their results; revise the B246 responsibility split. | No intended player-visible behavior change. |
| D-11 — Institution display | Read applied values, gates and reasons published by effect owners. | Tooltips distinguish retained/applied effects from candidate calculations. |
| D-12 — Retirement and package deletion | Permit S10 quarantine/removal only after Q1–Q8 duties migrate. Add and validate the reviewed package deletion path before any removal ships; retain SQL IDs until a separately approved clean break. | No intended behavior change; no raw-copy/delete bypass. |
| **D-13 — Touchpoints and deployments** | Continue between touchpoints; grant standing develop-test deployment permission at U2/U3/U4 only, with all existing exit/hash/receipt safeguards. U5 deployment and post-U5 main promotion need separate explicit approval. | Includes the plan's bounded current-campaign U2/U3 comparison where save shapes remain compatible; general old-save support and migration remain excluded. U4 uses a new campaign if S7/S8 changes persistence; U5 always new. The draft makes this limited exception explicit instead of relying on stale W0003 ACTIVE prose. |
| D-14 — Exclusions | Keep ownership gameplay semantics, Expedition repairs, new features, A8, fifth-profession vocabulary/ontology, and promotion-policy expansion outside this program. | Technical prerequisites may move; deferred gameplay is not implemented by analogy. |
| D-15 — Shared consistency contract | Approve declared change registration and the direction of an explicit read-phase/write-barrier snapshot contract. Primary specifies exact fields/lifetime in S5; Advisor review at U3 when requested by the user. | No automatic discovery bus or global permanent cache. The current per-Audit safety contract remains the default until its narrower replacement is specified and verified. |

### Primary clarification to approve with D-1/D-2

The original defaults leave the boundary between global pending and per-city isolation implicit. The proposed text resolves it as follows; this clarification is **also pending user approval**, not an implementation choice made on the user's behalf.

| State | Proposed carrier behavior |
|---|---|
| Route topology pending/unknown | Hold the entire network-dependent carrier set; confirmed eligibility exits still act. Standardization's combined local/remote maximum is one physical result and is held as a whole. |
| Route topology confirmed; one node's facts unreadable | Hold that node's last reliable contribution; recompute readable nodes from their confirmed new facts and combine with the retained contribution. Keep uncertainty visible; it is not fresh transaction evidence. |
| Cold-load installed aggregate cannot yet be decomposed safely | Hold while required facts are unknown and no confirmed source loss conflicts with retention; never invent a decomposition. Confirmed receiver owner/reference/qualification loss still exits. Mixed confirmed source loss plus another unreadable source requires the explicit exception decision below. |
| Confirmed topology and required facts available | Recompute normally, including exact withdrawal on confirmed loss and updates on same-turn facts. |

### D-1/D-2 unresolved exception — cold-load partial source loss

**DESIGN_DECISION_REQUIRED.** Current Standardization cold load has installed aggregate values but `sources={}` (`Mod/StandardizationEffects.lua:175–179`). If one source is confirmed lost while another remains unreadable, those aggregate values do not prove the remaining legal contribution. “Withdraw the lost part immediately”, “retain the legitimate part” and “do not invent a decomposition” cannot all be guaranteed from that evidence. This is a specific gap in the combined defaults, not a new ownership policy.

Choose one fallback for this case, or explicitly defer it and keep the affected S4 path stopped:

| Choice | Consequence |
|---|---|
| A — Temporarily retain the aggregate until necessary facts recover | Keeps the intended continuity, but may temporarily retain a confirmed-lost **source** contribution. This is a narrow exception to source-loss withdrawal precedence, only while the same receiver/reference remains eligible. |
| B — Withdraw the undecomposable aggregate until necessary facts recover | Guarantees the lost source supplies no effect, but may temporarily remove another legitimate source's contribution. This is a narrow exception to preserving unrelated contributions. |

Neither choice is assumed. Receiver owner/reference/qualification loss always follows its existing immediate exit under either choice. Retention never proves transaction eligibility, and this review does not propose new persistent per-source history to avoid the decision. S4 must exercise whichever fallback the user selects in cold-load tests; unresolved means stop this affected path, not silently selecting zero, hold or guessed reconstruction.

### Current-source qualifications for this review

- **The network change is broader than Commerce.** CultureNetwork's first audit clears installed carriers before capturing a first confirmed view (`Mod/CultureNetwork.lua:237–247`). StandardizationEffects holds source references but may still rewrite effects while pending (`Mod/StandardizationEffects.lua:131–183`). Both need D-1 cold-load/no-write coverage.
- **Recovery notification exists but is incomplete.** `Mod/NetworkBridge.lua:220–224` already handles an AVAILABLE transition on a duplicate snapshot. Revalidation/signal catch-up with unchanged values is the missing coverage; S4 must not replace working notification with a second unrelated mechanism.
- **Shared mechanisms must preserve policy differences.** Store requires successful setter execution plus matching readback (`Mod/CityProgressionStore.lua:1089–1099`); ExpeditionSpyStore accepts matching validated readback after a throwing setter (`Mod/ExpeditionSpyStore.lua:135–145`). S7b must make these caller policies explicit rather than silently selecting one. Binary32 numeric handling likewise cannot replace Capital's existing DECIMAL17_V1 codec.
- **B240 citation correction.** `Commerce_Preparation.md:170` says unreadable source Identity holds; it does not precisely state the separate pending-network Gold withdrawal branch. The actual conflicting behavior is `Mod/Commerce.lua:225–253`. The proposed supersession distinguishes those cases and leaves frozen B240 evidence unchanged.
- **No premature performance conclusion.** B270/B271 logs are before evidence with different workloads and C settings. Their difference is not a controlled measurement of SPC-attributable memory, and different saves cannot be subtracted to prove causation. U2–U5 report work/heap/footprint with those limits; attribution stays UNKNOWN where the evidence cannot separate engine/HD/SPC. Extra attribution experiments remain optional/user-directed, not an automatic new gate.

## 3. Reviewable text differences

[Refactor_Program_U1_Text.patch](Refactor_Program_U1_Text.patch) contains exact context diffs against the reviewed HEAD. It is **not an apply instruction or an accepted revision artifact**. It deliberately leaves revision/acceptance metadata unchanged until the user's decision; acceptance must use the ordinary D/A process below rather than applying this patch alone.

| Target | Proposed change |
|---|---|
| `AGENTS.md` | One navigation paragraph to the Architecture integration contract and Workflow Runtime Impact Contract. No extra task registry or mandatory historical reading. |
| `Specialization/Architecture/Specialization_v0.1_Architecture.md` | Compact P01–P10, scoped exceptions, and the precise network pending/confirmation contract. Existing per-Audit isolation remains the default; future S5 sharing must specify the barrier. |
| `Specialization/Workflow/README.md` | One-page runtime impact template; trigger-selected T01–T08; baseline counterexamples and static alarms; dependency-based re-review. No blanket all-history regression requirement. |
| `Specialization/Architecture/Playtest_Workflow.md` | Replace stale general ACTIVE wording with explicit U2/U3/U4-only D-13 authorization, U5/main approval boundary, and bounded current-campaign smoke scope. |
| `Specialization/Design/Network.md` | Distinguish temporary unreadability from confirmed loss; hold cold-load effects, immediate confirmed eligibility exits, D-2 isolation and transaction exclusions. |
| `Specialization/Design/Specialization_v0.1_Design_Spec.md` | Clarify NET-004 confirmed loss and introduce proposed NET-005 as the authoritative common rule. |
| `Specialization/Design/Commerce.md`, `Culture.md`, `Shared.md` | Cross-reference that rule at the affected current-effect descriptions; do not duplicate formulas or turn retained output into permanent history. |
| `Specialization/Architecture/v2/Commerce_Preparation.md` | Explicitly supersede the B240 implemented pending withdrawal, preserving source-Identity UNKNOWN and signed-contract rules. |

The scheduling record now uses the user's authorized dependency sequence. Report B P1 is interpreted as **before the next dependent use**: new consumer, automatic invocation, frequency/work-set expansion, recovery path or reference lifetime. It is not merely “before the next profession” and not permission to rewrite unrelated modules. Historical scheduling sections remain intact below the new current section.

### Formal Design acceptance work after U1

Do not overwrite accepted `Shared_D0045.json` or earlier Content/Spec snapshots. On acceptance, freeze the current D0057 Spec byte-for-byte, allocate the next available D revision (expected D0058; verify then), and record the user's exact D-1/D-2 and any accepted D-4/D-5/D-6/D-7 choices in Design_ChangeLog/Spec and affected successor Content objects. Declined or altered defaults are excluded. Update reading pages, Content navigation, Authority versions, reviewed hashes and the accepted A revision as one coherent docs batch before S2.

For Shared's successor, replace `/concepts/LONG_TERM_STATE_LIFECYCLE/F_CONFIGURATION_AND_DERIVED_STATE/recompute` at the verified current path. Proposed value:

> Recompute derived state from current authoritative facts after relevant changes. Pending/unknown route topology retains last-applied network-derived carriers without rewriting (including inseparable local/network combinations); confirmed qualification/reference/owner exits override retention. Cold-load installed carriers may temporarily represent last-applied output, not permanent history or confirmed topology. Per-city unreadability retains only a valid prior contribution, or unavailable/no contribution when never known, while readable cities proceed once topology is confirmed, combining new confirmed contributions with retained ones and preserving provenance; an undecomposable cold-load aggregate is held until necessary facts exist. For the cold-load mixed confirmed-loss/unknown-source case, insert only the expressly selected U1 exception; no default is implied here. Apply the accepted NET-005 rule; do not infer transaction eligibility from retained effects or add network requirements to already signed contracts.

The Shared successor may add an explicit NET-005 reference at the same configuration contract; formulas, categories A–G and ordinary-building vocabulary are copied unchanged. D-6 also requires the accepted gap/no-bonus wording in Research/Commerce's successor contracts; D-4/D-5/D-7 record only the chosen fault policies, without changing ownership outcomes or native no-replay protections. This list is a synchronization obligation, not acceptance or permission to resolve new semantic conflicts silently.

## 4. Stage and stop handoff

S2 builds the faithful harness and baseline counterexamples first. S3 preserves startup order while isolating failures. S4 applies only confirmed D-1/D-2 and its listed repairs, then stops at U2. S5a→S5b→S5c→S5d precedes S6/U3. DialogueEffects receives its own hooks **before** GPPRefresh's relay and old Dialogue hooks retire; later Q7 transport/ACK/generation duties must also move before file removal. S7 mechanism extraction separates behavior-neutral batches from accepted DDR changes. S8 delivers technical lifecycle prerequisites only. S9 stops at U4. S10 moves Q1–Q8 duties and validates package deletion before removing files. S11/U5 remains user acceptance.

Each code batch must include runtime impact, selected T gates, executed closure/results, save compatibility, commit/push to develop and actual evidence labels. Stop the affected work for a new unapproved behavior change, unexplained failure/assertion weakening, smoke failure/missing confirmation/unexpected work increase, out-of-scope work, early campaign incompatibility, or ownership/concurrent-edit uncertainty. No promotion before U5; no automatic request to Advisor or game launch.

At each native checkpoint the stage result must provide exact Chinese UI operations and fixed pass conditions before deployment. U2 focuses on nonzero Commercialization at sampled accrual, retry budget, readiness and eligible GC; U3 on real consumer locality/shared work and unchanged effects; U4 on multi-city same-type Crew completions, all three full-turn projects/nonempty queue, investment panels and adapter coexistence. New evidence cannot retrospectively turn S0 static review into native PASS.

## 5. S0/S1 validation and evidence

**STATIC_CONFIRMED** means current source/configuration review; **LOG_OBSERVED (Advisor)** means the cited analysis of the captured session, not a new native run by Primary. No gameplay simulation was executed for this documentation batch and no new USER_GAME_TEST_PASS is asserted. Source references in the intake were rechecked at the pinned HEAD, including changed B271 files. Raw logs remain local and unpublished.

The initial context check failed because the pre-existing P0-H status `STABLE_DEPLOYED_USER_TEST_REQUIRED` is outside Batch.schema's enum. A read-only in-memory check using an allowed status passed all 312 runtime and 975 existing context hashes. This checkpoint updates P0-H to the valid `IMPLEMENTATION_COMPLETE_AWAITING_USER` state for S0/S1; it does not relax the schema or refresh unrelated hashes. Only this checkpoint's reviewed documentation entries are added/refreshed in Context_Lock.

Document checks: **PASS** for the exact seven-path documentation scope, all 14 reviewed Advisory input hashes unchanged, 17 current review/proposed-text links and virtual target anchors, JSON parsing, document whitespace (excluding literal unified-diff context markers), and review-only patch applicability/content whitespace (`git apply --check --whitespace=error`, not applied). `context.py check P0-H` passes **312 runtime / 977 guarded context entries** after the scoped update. Mod, tools, tests, accepted Design/Architecture, AGENTS and README are unchanged. These checks establish document/integrity correctness only. The staged publication gate passed for the seven owned files (secret and added-content privacy checks), and must be rerun after final edits; final text acceptance still needs the revision/synchronization step above.

### Reviewed input provenance

Read in the requested order: index → crosscheck → governance 01–04 → scan review → conformance audit → Report B/register → B270/B271 logs → Memory Growth §§1,6 → full program. These local Advisory inputs are **not published by this checkpoint**, are not modified, and do not become default mandatory context. Accepted instructions and the actionable stage map are recorded in the tracked U1/scheduling records; source/input equality is not acceptance of every advisory conclusion.

Paths below are relative to `Specialization/Reports/Advisory/`. Hashes identify the exact reviewed bytes; other sections of the Memory Growth report were not independently re-audited.

| Input | Reviewed SHA256 |
|---|---|
| `External_Reviews/README.md` | `2b710c5e89bda95c52c1e184ae05f0423c16c1e5663f56822fd1d186f9306880` |
| `Architecture_Conformance/External_Review_Crosscheck.md` | `03790e34aad149959449d457a77deabea6753ee61150298a93e1ece004dd789e` |
| `External_Reviews/2026-10-23_Governance_Root_Cause/01_开发约束失效与架构偏离根因审查.md` | `5ccd7d8e3a4a6830b5cb5d962b0c8afa086f25e4896c63bea71fbff5a5be581d` |
| `External_Reviews/2026-10-23_Governance_Root_Cause/02_Architecture_Development_Principles_DRAFT.md` | `07f2c4056887cd820bd90e893c579437788e971972a5bb607ce41e9a1fb9625d` |
| `External_Reviews/2026-10-23_Governance_Root_Cause/03_Development_Validation_Gates_DRAFT.md` | `447cf04b7420a19b8fdf5dcc11d7aa2c9a047d4ec242c8c05a14b9ead68ef1a5` |
| `External_Reviews/2026-10-23_Governance_Root_Cause/04_证据索引.md` | `3f5858464cf0c19609301105619aa7a0191860f5f34c4d39e463b8f0ab46fdc5` |
| `External_Reviews/2026-10-23_Scan_Shared_Architecture/Specialization_v0.1_扫描与共享架构审查.md` | `e33b9b96e463f038518af1a82ff6eb160e4815aa4132fb919eeaef2912d5942e` |
| `Architecture_Conformance/Architecture_Conformance_Audit.md` | `83d179c8ffd0c0a17d79805f18a8c4560e5e568300433065739389fa2d0a4764` |
| `V01_Readiness/V01_Architecture_Plan.md` | `feb06c2381f9e93e7776f4c1dd9cfc33ccabbe083ac94ec226b80da71afeb97e` |
| `V01_Readiness/V01_Architecture_Register.md` | `7826e4b63498b75549fcf2f07a38fd491c909c6ccda8d458f99aaad05e3c76c0` |
| `V01_Playtest_Evidence/B269_B270_Log_Review.md` | `e05f4bc998af7df22872bc71c566c23c9cdfd22461067b7b9ee07de46e6c5d3f` |
| `V01_Playtest_Evidence/B271_Log_Review.md` | `6c95dec5ab6579636981365dfbc490efdf2f99236d44d3af030c660c2e9f71b9` |
| `Memory_Growth/Memory_Growth_Audit.md` | `d05d5986dca7032fb0641814e7ef9bcd3825118428cd1fdb544986c3a3c2eead` |
| `Refactor_Program/Refactor_Program_Plan.md` | `7bba9becb33523d73acad19b730a01d32423c6ce9587973659be5c6e67151c10` |

## 6. Handoff

- **User decision:** approve or amend D-1–D-15 and the proposed text differences together at U1, explicitly selecting or deferring the D-1/D-2 cold-load partial-loss exception. D-13 is the only proposed standing deployment permission; it is not active yet.
- **User testing:** none at U1. The next native smoke is U2 after S4 and the applicable deployment approval.
- **Primary next:** stop here. After U1 acceptance, formalize only the accepted text/revisions, then proceed S2→S10 within the approved boundaries. No S2 implementation, deployment or main promotion before this review.
