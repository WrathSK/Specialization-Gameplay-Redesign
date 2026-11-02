# Architecture Convergence Gap Matrix v1

Investigation / Non-authoritative / No design decision implied

Status: Stable | Maintainer: Primary

Baseline: `920b4ed2a8da5dd394b95fe03f96c81dc2a8a069`; D0058 / A0183 / S0866; recorded runtime B399.426.

[Overview](Executive_Overview.md) · [Decisions](Decision_Register.md) · [Evidence](Evidence_Appendix.md)

## Interpretation

A = approved formal contract; H = direction stated by the current handoff, with implementation details not yet formally settled. H does not silently replace A. STATIC means source-reachable, not native reproduction. Existing LOCAL/native results are attributed to their frozen records; nothing was rerun here.

Classification is deliberately not a defect count. A single underlying concern may have a planned mechanism and an undecided business boundary; the primary classification below determines its disposition. Local G/DEC/E IDs organize this report, not an additional authoritative backlog.

## 1. Target, current state and classification

| ID / domain | Target and authority | Current implementation | Classification | Evidence / confidence | Affected boundary / risk |
|---|---|---|---|---|---|
| G01 Network signal | A: same-value proof catch-up wakes consumers | Sender duplicate requires three-way signal equality | JUSTIFIED_EXCEPTION — corrected historical defect | E03; STATIC + recorded local/native normal recovery; high | Sender/Bridge/Commerce; do not reopen NET-1 |
| G02 Load proof | A: bounded recovery without opening trade UI | Named LoadScreenClose/local-begin opportunities, finite flight budget | JUSTIFIED_EXCEPTION — corrected historical defect | E03; high within tested scope | UI transport; actual lost engine request stage remains unknown |
| G03 Commerce unknown workers | A: unknown qualification is not confirmed exit | WORKERS_UNKNOWN omitted from hold allow-list; zero plan may be applied | CONFIRMED_DEFECT — static reachable | E04; high static, not native reproduced | Commercialization carriers; transient withdrawal |
| G04 Confirmed exit priority | A: known eligibility loss outranks unrelated UNKNOWN | ResearchInfrastructure asserts ACTIVE before inspecting D/anchor | IMPLEMENTATION_GAP | E05; high order evidence, manifestation unproved | Research IV exit; stale effect under combined fault |
| G05 Passive fact use | H/A direction: retained fact distinct from current validity | D/GW retain values but current consumers normally require READY/KNOWN | DESIGN_DECISION_REQUIRED | E06/E07; high | Research/Culture/passive combiners; retained-input recomputation is a behavior change |
| G06 ACTIVE composition | H: decide raw governor vs derived ACTIVE retention | EffectiveFacts is phase-local; UNKNOWN ACTIVE not durable old ACTIVE | DESIGN_DECISION_REQUIRED | E06; high | All professions/transactions; retaining derived ACTIVE can overqualify after changed Potential |
| G07 Notification completion | H: confirmed change owns update duty | FC/Bindings count attempts, discard drained queue, ignore callback result states | DESIGN_DECISION_REQUIRED | E08; high | All consumers; delivery success can mask HELD/failure |
| G08 Proof emission failure | A: proof availability recovery must notify | Bridge stamps lastNotifiedProof before fallible emission | IMPLEMENTATION_GAP — static failure path | E08; high code, no native incident | Network->consumer wake; identical proof may not re-emit after failure |
| G09 Cold source attribution | A0183: bounded applied source witnesses for D-2 | Model/Cell/Store exist; no Commerce/Culture production consumers | PLANNED_INCOMPLETE | E09; high | Partial-read cold network effects; ordinary reload PASS is insufficient |
| G10 D7 recovery completion | A: isolate, reconstruct, then lawful baseline only with proof | Real deferred lifecycle and deterministic repairs exist; generic lawful-origin/outcome gaps remain | PLANNED_INCOMPLETE | E10; high for implemented paths | Ability history/paid receipts; unsafe reset loses authority |
| G11 Completion admission hold | A: strict completion evidence, recover only lawfully | completionError persists and blocks active admission; no current clearing assignment located | UNKNOWN_NEEDS_EVIDENCE | E11; high code, cause/recovery policy uncertain | Unassigned-city admission; possible durable lock, not observed in native records |
| G12 Industry E history | A: reliable completion history gates study | coverage can become UNAVAILABLE durably; no general upgrade; E is still a lower bound | DESIGN_DECISION_REQUIRED | E12; high | All Industry Study eligibility after historical gap; cannot invent missing eras |
| G13 Claim completion proof | A: independent full-turn outcome/receipt rules | Internal FinishProgress is timer-guarded; native completed handler also accepts direct candidate event | UNKNOWN_NEEDS_EVIDENCE | E13; high code, cancellation delivery unknown | Permanent identity; old direct-event tests intentionally permit path |
| G14 Crew unique attribution | A D5: each grant needs unique evidence | Player cumulative count + per-project last receipt does not alone resolve every same-tier multi-city case | PLANNED_INCOMPLETE — proof boundary | E14; high | Irreversible unit creation; no count-based extra grants |
| G15 Applied institution view | A D11: owner-published applied amount/gate/reason | Tradition Applied exists; UI request still derives percent from age; other preview formulas remain | PLANNED_INCOMPLETE | E15; high | Display may imply desired value is installed; accepted normal UI not invalidated |
| G16 Business history ownership | H: profession policy, shared commit mechanics | Store owns central validation/explicit ability transitions; Industry history has independent owner | DESIGN_DECISION_REQUIRED | E16; high | Store/profession coupling; cannot infer arbitrary generic lifecycle policy |
| G17 City vs district identity | H/A: city owns identity/history; instance supplies eligibility | Store refs and admitted first district are intertwined; replacement/multi-instance assumptions remain | DESIGN_DECISION_REQUIRED | E17; high ordinary path, future compatibility inferred | Moves/removal/capture-specific districts; new gameplay remains excluded |
| G18 Fifth-profession registration | H: finite explicit registration, no plugin framework | Four-kind vocabulary appears in multiple runtime/UI/SQL and validation sites | DESIGN_DECISION_REQUIRED | E18; high | Extension cost; avoid registry that hides unrelated policies |
| G19 Store/native transactions | A: CAS/readback/no replay; protected unknown outcomes | Existing protected cells, contract stages and deferred lifecycle are real production paths | JUSTIFIED_EXCEPTION | E10/E19; high | Cross-record/native operations cannot be reduced to a shared fact update |
| G20 Direct event listeners | A/H: retain distinctive completion/history/recovery inputs | Shared notifications coexist with legitimate native completion/turn/history listeners | JUSTIFIED_EXCEPTION | E20; high static | Deleting by registration count would drop native evidence |
| G21 Scope and scanning | A P02/P05/P09: bounded cause/scope/cost | Whole-catalog captures, owner-wide fallback and UI GW turn recollection remain | PERFORMANCE_OPPORTUNITY | E21; high work shape, no CPU attribution | D/GW/local-turn work; no promised optimization percentage |
| G22 Retirement duties | A P08/D12: migrate duties before removing modules | Binding/CityFlow/Construction/Dialogue/timing paths remain load-bearing; Half positive loop already retired | PLANNED_INCOMPLETE | E22; high | Startup, receipts, cleanup, unit actions; names are not deletion proof |
| G23 Deployment deletion | A D12: reviewed exact removals and rollback in both tools | Stable deploy rejects extras; temporary switch has transaction protection but no analogous removal-diff review | PLANNED_INCOMPLETE | E23; high | Only blocks shipping deletions, not this audit or all existing deployments |
| G24 Formal precision | A document must describe accepted implementation accurately | D cache <=8 prose stale; Store-exclusive-history wording narrower than approved Industry owner; runtime contract spread across accepted batches | IMPLEMENTATION_GAP — documentation precision | E24; high | Future design guidance; do not “fix” code to stale cache prose |
| G25 Performance/evidence closure | A: scoped proof, no native attribution from local counts | No comparable current/native B307 CPU/heap growth study established here; generic failure counters incomplete | UNKNOWN_NEEDS_EVIDENCE | E25; high limit | Final claim strength, not proof code is slow |
| G26 Restructuring A/B UI | User: repeated prepared A inert; B alone confirms | A has no prepared guard; native visual B-inert/A-confirm mapping not locally reproduced | CONFIRMED_DEFECT — guard static; mapping user-reported | E26; high guard / unknown UI cause | Short independent repair candidate; not Option B architecture migration |
| G27 Deferred feature boundaries | Existing accepted deferrals remain | PT017 extra credits bounded exclusion; PT018 displaced expedition HELD; multi-item project recovery deferred | JUSTIFIED_EXCEPTION — deferred/nonblocking scope | E27; recorded evidence | No broad foreign-Mod, Expedition or ownership work imported |
| G28 Late return recovery | A: existing return only after all exact exits; H: meaningful recovery duty | Matched return waits behind unfinished exit; late completion lacks established automatic return wake | UNKNOWN_NEEDS_EVIDENCE | E17; high barrier, eventual convergence unproved | Existing lifecycle recovery; do not bypass exit or invent ownership |

## 2. Disposition, dependencies and acceptance

“Pre-U5 candidate” is a recommendation for DEC-11, not a newly imposed prerequisite. The handoff's latest sequence supersedes this report's ability to decide scheduling unilaterally. Original S9/S10 duties remain traceable even if rescheduled.

| Gap | Recommendation / decision | Dependencies | Minimum acceptance / preserved behavior | Suggested timing |
|---|---|---|---|---|
| G01–02 | Keep repairs; no retained-fact workaround | Existing Sender/Bridge strict proof | Existing 87-method result + scoped B399 recovery; failure budget/ACK/replay remain strict | Baseline retained |
| G03 | Narrow UNKNOWN hold correction; add real owner fault test | Existing binding/reference; no new A service required | Prior Gold held on worker read failure; confirmed exit still zero; new reliable workers recompute; no extra Treasury calls | Pre-U5 candidate |
| G04 | Prioritize independently established exact exit; do not map UNKNOWN ACTIVE to0 | DEC-01/02 scoped input precedence | Real confirmed anchor loss + unrelated governor fault; no stale cross-ref effects; unchanged normal Research values | Small candidate or early Option B by DEC-11 |
| G05–06 | Approve per-fact/use table and raw/derived boundary | DEC-01/02/03 | Current/no-value/retained/recovered/confirmed-negative; same-turn Potential+governor changes; strict actions reject stale | Option B first foundation |
| G07–08 | Explicit duty state and emission acknowledgment, not generic replay | DEC-04; existing P06 | Inject emitter/callback failure; preserve exact owner/ref; successful siblings idle; recovery on new relevant cause; finite load reconstruction | Early Option B; G08 narrow fix timing DEC-11 |
| G09 | Wire existing approved recovery to actual writers/readers | G07/08 + precise lifecycle scope; no new save approval implied | Cold mixed sources, domain splits, known loss+unknown sibling, torn record/write both directions, strict transactions; Standardization-only exception stays narrow | DEC-11 partition; original S9 obligation |
| G10–11 | Finish deterministic cases; explicit evidence gate for origin/outcome gaps | DEC-06 and DEC-13 separately; strict envelope/ref/CAS | UNKNOWN not corrupt; affected-only isolation; deferred witness once; irreversible ambiguous receipts untouched; no permanent generic HELD claimed as finished | Option B bounded history slice |
| G12 | Choose strict hold vs proven lower-bound E eligibility | DEC-07, explicit gameplay approval if changed | Missed completion, N-only write failure, reload, known era receipts and quota; no fabricated E | Separate decided slice, not silent refactor |
| G13 | Verify completion event contract before changing admission | DEC-08 evidence gate | Direct real completion/canceled signature, saved timer and unique receipt; preserve valid normal native completion | Local evidence first; minimal native only if actually blocking |
| G14 | Resolve unique source/request/unit evidence; do not replay count delta | Already accepted D5, no re-vote | Two cities/same tier/same turn, delayed/duplicate events, cold HELD, unique units/receipts; current OpenProof tests are characterization, not PASS | Candidate engineering precondition for claiming this scene; DEC-11 |
| G15 | Connect existing applied publication through reply to institution | D11 already decided; no new UI gameplay | Current vs last-confirmed applied, unknown gate, failed write, cold unobserved; normal labels/colors retained | Original S9, timing DEC-11 |
| G16–18 | Choose finite owner boundaries and explicit registration scope | DEC-05/09/10; no future profession gameplay | Hypothetical simple fifth kind integration diff; unchanged four-kind behavior; owner/ref and multi-instance rejection explicit | Post-U5 Option B/extension preparation |
| G19–20 | Preserve independent policies and irreversible protocols | Existing A/D rules | Direct events retained where evidence-specific; strict native outcomes not reclassified as passive duty | Throughout |
| G21 | Measure before choosing local scope reductions | G25; shared freshness dependency | Real producers+consumers, warm capacity boundaries, same-turn changes, scoped native signatures; no drop of owner-wide proof duty without replacement | After correctness foundation, finite opportunities |
| G22–23 | Migrate Q1–Q8 actual duties; reviewed deletion set for both tools | G09/G15 where coupled; G23 before first removed package | Cleanup/ACKs/readers still work; exact removed path review, failpoints/recovery; SQL/save IDs preserved | DEC-11 decides partition; not delete now |
| G24 | Amend only genuinely stale formal text through normal approval | Relevant accepted implementation evidence | Correct cache/lifetime/owner contracts; diagrams remain subordinate; historical wording stays frozen | With target v2 formalization |
| G25 | Agree meaningful like-for-like work/native evidence | DEC-12 | Work counts vs CPU vs process memory separated; comparable scenario and limits; observation removable | Baseline before affected migration, delta afterward |
| G26 | Repair A guard + diagnose actual control routing independently | Existing explicit user A/B contract | Prepared A inert; B exact matching plan; stale plan refusal; both operations native clickable smoke after repair | Pre-U5 candidate, small separate batch |
| G27 | Preserve accepted deferrals | Existing records, no new permissions | No false PASS, no uncontrolled forced testing; changed paths later get scoped regression | Outside convergence implementation unless separately approved |
| G28 | Local late-exit→evidenced-return composition first | DEC-04/05/14 | Original episode once, stale token rejection, no polling or guessed return | Affected Option B recovery slice |

## 3. Fact/reader coverage and decision ownership

The appendix contains the per-fact and per-consumer inventory F01–F09. Retained values are not transaction credentials. D-1 pending topology continues freezing the complete installed network-derived output, including Standardization's combined physical result. Only readable topology plus separately unreadable sources enters D-2. The cold aggregate exception remains Standardization-only.

Primary can select helper names, test harnesses and local implementation details after contract approval. DEC entries concern unresolved semantics, shared responsibility/lifetime or schedule/evidence boundaries; they are not requests to approve routine code choices.

No code fixes, optimized loops, new interfaces, authoritative record updates or U5 tests were performed for this matrix.
