# Decision Register v2 — accepted direction and remaining details

Investigation / Non-authoritative / No implementation authorization

Status: Stable | Maintainer: Primary

2026-11-02. Source baseline: `0c9c60ec8e6a769461cfaaa801ffbb3f07a25804` (develop); D0058 / A0183 / S0866. Recorded runtime B399.426 from `4915170`; deployment not reverified here.


[Overview](Executive_Overview_v2.md) · [Ability matrix](Per_Ability_Fact_Use_Matrix.md) · [Evidence](Evidence_Addendum.md)

## 1. Provenance and authority

H2 is the owner-provided Architecture_Convergence_v2_Handoff.md, supplied with the explicit instruction to prepare v2. Its accepted decisions govern this target report. They are not Codex recommendations. D0058/A0183 remain the unchanged formal baseline; v3 must propose the necessary formal synchronization before implementation. In particular, new DEC-06C supersedes v1's proposed comprehensive baseline-recovery target, not the historical bytes of SAFE-004.

“Direction approved” does not approve every retained-read cell, concrete interface or Pre-U5 patch. Ordinary function spelling, container selection and test wiring are Primary's engineering work, not extra user votes.

## 2. DEC-01–14 disposition

| DEC | Approved by H2 | Current implementation / v1 change | Remaining status, G and O |
|---|---|---|---|
| 01 | Ability × input × purpose decides use; strict failure is not0/exit; D1/Reputation exceptions stay | Current readers mostly demand current inputs; D/GW retain values. Withdraw any fact-wide opt-in interpretation | **Direction approved; cells open**, R1; G03/05/29, O1/O3 |
| 02 | A: retain raw governor ceiling for opted-in passive uses, derive with current reliable Potential/identity; root first | No cross-event ceiling service; no routine native UNKNOWN established. No-governor is normally KNOWN1 | **Direction approved; evidence first**, T1/R1; G06,O1 |
| 03 | A: reconstruct cold raw facts, no generic persisted fact layer; first absence not invented | Existing network-recovery/history/receipts retain their narrow approved scope | **Concrete persistence boundary settled**; lifetime per consumer in R1, G05/09,O1/O3 |
| 04 | A: coordinator owns delivery until explicit profession takeover; profession owns completion/recovery | Current attempted callbacks do not supply takeover. Best-effort/central-business-retry options withdrawn | **Direction approved; minimum handoff contract proposed**, R2/T7; G07/08,O2 |
| 05 | A: profession schema/transforms vs shared detection/validation/CAS/readback/commit; independent owners allowed | Store still contains explicit business transitions; current outcomes preserved | **Boundary approved; extraction mechanics + evidence**, R4; G16/19/28,O4 |
| 06 | C: explicit error/root cause/affected-only protection; no guessed history/reset/silent permanent HELD | v1's comprehensive legal-zero-baseline completion recommendation superseded. Existing deterministic/deferred cases need individual review, not deletion | **New target accepted; formal synchronization needed**, R4/T3/T4; G10/11,O4 |
| 07 | A: complete E history required; repair acquisition/persistence root | Current strict Credit/Study gate matches. Lower-bound alternative withdrawn | **Semantic choice closed**; root evidence if failed, G12,O4 |
| 08 | A: genuine native early Claim completion legal without internal timer; candidate/ref/receipt checks remain | Direct native completion is justified, not missing-timer defect. bCanceled on Narrative event cannot be transferred by guess | **Semantic choice closed; exact event evidence only**, T2; G13,O4 |
| 09 | A: finite kind/family/display registration; profession declares subscriptions, central matching/delivery | Existing central phase1 declaration list; startup failure/duplicate validation contract required | **Direction approved; proposed minimum contract**, R3; G18,O5 |
| 10 | A: city history, instance eligibility; current single-instance boundary; no generic selector | Keep present fences. M1 earliest qualified, M2 maxD then earliest are **future unapproved candidates** | **Current boundary closed; future candidates not a current vote**, G17,O5 |
| 11 | A: only approved necessary Pre-U5 fixes; remaining S9/S10 carried into OptionB, not erased | Exact worklist now prepared; v1 “finish all before U5” recommendation no longer current target | **Schedule direction approved; precise list pending**, R5; G03/04/08/14/26/29 and O1–O8 |
| 12 | A: necessary work/minimum waste/native acceptable, no arbitrary percent/CPU/RAM KPI | Existing source/counter evidence useful; no measured speedup manufactured | **Evidence standard closed**; Primary targeted comparison, G21/25,O8 |
| 13 | A: expose first-completion registration errors, inspect signature/ref/timing; no guessed clearing/new witness | Sticky completionError current; event resolves object before profession relevance | **Root evidence first**, T3; G11,O4 or narrow fix only if proved |
| 14 | Conditional A: root first; legal delayed exits may continue on explicit proven event | Foreign-target fence may reject old cleanup after actual return. Missing wake alone is insufficient diagnosis | **Conditional boundary approved; endpoint proof open**, R4/T4; G28,O4 |

## 3. Six follow-up groups — five owner reviews and one evidence-first boundary

### R1 — Select the concrete ability/use cells

**One-sentence question:** Which candidate rows in the ability matrix may recompute from retained inputs, and should ResearchCross retain its existing adjacency sample rather than introduce D?

**Approved:** services may retain; ability/use opts in; confirmed loss wins; strict actions cannot borrow old values. ResearchApply-D and passive Lv2GPP-worker are permitted directions, not a reason to approve all anchor/building/GW/governor cells.

**Options:** approve the matrix's named candidate rows in small ability groups, or leave selected rows strict-current with same-reference output hold and explicit error until later. Neither option may change formulas, withdraw on UNKNOWN or override D1/D2/unknown-Reputation policy.

**Recommendation:** first confirm the Cross clarification and approve only named rows whose qualification/retained lifetime are complete; medium confidence. Culture GW numeric count, category eligibility, ordinary building presence and age history remain separate. Preserve existing D2 source contributions despite a general preference for strict Commercialization; a change to that specific approved exception would need an explicit new decision.

**Risk / dependency:** mixed stale qualification with fresh amount, cross-reference reuse, fabricated first value. O1/O3; local current/retained/no-value/negative/second-change tests. Does not itself block baseline U5.

### R2 — Minimum reliable handoff contract

**One-sentence question:** Accept a bounded, versioned scope acknowledgment only after profession-owned responsibility is recorded, with later business recovery remaining solely professional?

**Approved:** DEC04A, no central business retry. The candidate below specifies that direction, rather than offering best-effort B again.

**Minimum candidate:** coordinator tracks pending-delivery versus taken-over; errors/attempts are metadata. `AcceptChange(scope,ticket)` first records/coalesces its own bounded pending, or completes/no-ops synchronously, then returns a matching acknowledgment. Ticket carries session/consumer/scope/reference/revision, no fact values/native handles. Central FC→Bindings collection is not profession takeover. Reentry/newer revision survives an older ACK. An ACK says “responsibility accepted,” never “effect confirmed” or “transaction authorized.”

**Alternative granularity:** keep per-city tickets or bounded owner-scope batches; recommend existing explicit owner/city coalescing with revision-fenced acknowledgment, medium confidence. Field names/internal storage are ordinary implementation details.

**Failure/load:** no ACK means coordinator retains duty with visible failure; no idle infinite retry. Relevant new fact/availability/lifecycle/init re-arms delivery. A taken-over business failure stays with owner. Lost ACK may redeliver the same ticket idempotently. Rebuild necessary session duty at existing owner initialization; save only already approved irreversible/history evidence, not a generic event log.

**Evidence / acceptance:** T7, E2; real producer→binding→owner tests, failed emitter/owner, missing target, ACK loss, duplicate, same-turn reentry, close/load, successful siblings idle. O2 contract must be settled before its migration.

### R3 — Minimum explicit subscription contract

**One-sentence question:** Accept successful-start profession exports declaring their fact interests and takeover entry, centrally validated/bound in the existing final startup slot?

**Approved:** DEC09A, profession self-declaration and central matching; no inferred network/GPP/investment/history eligibility and no plugin discovery.

**Candidate:** stable owner/consumer ID, existing kinds/topics, accepted scope and takeover callback; only needed mechanical options. Collect from the explicit successful profession list, validate once in current FactConsumerBindings startup slot, then seal composition. Keep phase0 RestructuringSync→NetworkBridge and its specific EmitDerived ordering; profession subscriptions are not an unordered replacement for infrastructure phases.

**Alternative:** explicit registration calls instead of returned descriptors; both must isolate failed starts. Recommend successful-start exports for the first slice, medium confidence, because current RuntimeComposition registration wrappers do not automatically protect a new API.

**Validation:** duplicate ID, unknown kind/topic, missing callback, FAILED/SKIPPED owner are visible errors, not silent success. Preserve unique native completion/history listeners. Exact Lua/SQL layout is Primary work under the approved contract, not a new capability decision.

**Acceptance:** T7 plus registration/order/isolation differential; G18,O5 depends on O2 takeover where applicable. No U5 prerequisite or fifth-profession implementation now.

### R4 — Root-cause/error and legal lifecycle boundary

**One-sentence technical question:** Which observed failures are lawful delayed transitions, implementation errors, or no-longer-authorized old endpoints under the already approved boundary? No new owner choice is pending until evidence demonstrates a genuinely missing contract.

**Approved:** DEC05A/06C/13A/14conditionalA. This is contract review after T3/T4, not permission to build a comprehensive recovery policy.

**Candidate:** profession pure delegates receive detached validated old ability payload and confirmed lifecycle context and propose next payload/notification; shared Store retains parent identity/envelope, opaque-sibling preservation, CAS/readback and commit ordering. No delegate changes city token, performs native money/unit actions or decides another profession's record.

**Options after evidence:** keep an actually legal delayed transition using its exact reference episode and explicit successful-exit wake; or classify the failure as an implementation defect and fix its cause. If owner/reference after return is no longer authorized for old cleanup, first propose a new exact cleanup contract if necessary. Retaining a return event alone is not sufficient.

**Recommendation:** evidence first, high safety confidence. Do not delete existing legitimate deferred recovery; do not keep silent indefinite HELD as a final feature. Existing clear errors/status can be reused. Lightweight error-code UI is an unapproved optional surface, not a new framework.

**Formal sync:** DEC06C must be reconciled explicitly with SAFE-004/A0183 recovery wording in the later authorized v3/formal stage; no code may silently pick one. New durable witness for first completion remains separately approvable only after necessity proof.

### R5 — Exact Pre-U5 inclusion

**One-sentence question:** Approve the specific worklist after its evidence gates, keeping the rest of original S9/S10 in named OptionB packages?

**Approved:** DEC11A; do not re-offer “all S9/S10 first.” Worklist items are recommendations, not executed repairs.

**Recommendation:** include G03/G26/G08 narrow fixes; validate G04's independent confirmed-negative path before choosing its narrow correction; resolve G14 unique completion evidence before claiming the supported multi-city scene; handle G29's actually R-dependent venture gate. T1/T2/T3/T4 are evidence-first, not automatic baseline blockers. Medium confidence where native interfaces remain unresolved.

**Options:** approve named narrow changes with exact local/native deltas, or request targeted evidence before accepting each affected candidate. Deferring a supported D5 defect cannot mean silently weakening D5; the baseline's limited evidence must be explicit and the underlying obligation remains.

**Acceptance:** [Pre-U5 Worklist](Pre_U5_Worklist.md); package-specific checks, no repeated full-profession/forced-pillage/ownership campaign. v3 fixes the final list; deployment still separate.

### R6 — Capital modes when Reputation is unknown

**One-sentence question:** Keep STABLE signable when its independent terms are current while disabling R-dependent VENTURE quotes/confirmation until Reputation is reliable?

**Current new evidence:** G29/E8. Passive D6 can produce Commerce READY with reputationKnown=false and effective0; Capital imports R0 without a separate known check. Prepare/confirm comparing the same fallback does not confirm R. No native occurrence established.

**Approved constraints:** irreversible inputs require reliable authority; D6 zero bonus is a Commercialization exception, not permission to fabricate a venture refund. ACTIVE III's effective R0 is a known level gate, distinct from an unknown ACTIVE IV history.

**Options:** mode-specific readiness (STABLE independent terms remain usable, VENTURE unavailable/error), or temporarily block both modes through the common quote until that projection is separated. Recommend mode-specific readiness, medium confidence; it avoids disabling a safe independent action. Do not use retained R, invent age0 or rewrite an already signed contract.

**Acceptance:** reliable/unreliable Reputation × ACTIVEIII/IV × STABLE/VENTURE; reconfirmation cannot lock unknown term; known signed receipts settle under original terms. R6 is a narrow dependency/mode boundary, not a new investment formula.

## 4. Evidence work — eight groups, Primary-owned

| Group | Question to resolve before any dependent patch | Smallest next work; not executed here |
|---|---|---|
| T1 Governor | Does a real Gameplay UNKNOWN occur, and why? | Existing actual fact/error vs UI-placeholder records; six native properties/control/trait path and publish timing; only propose bounded new sampling if existing evidence insufficient |
| T2 Claim event | What does exact Gameplay CityProjectCompleted deliver on completion versus cancellation? | Existing source/examples then actual event boundary if indispensable; never copy Narrative bCanceled signature |
| T3 First completion | Wrong signature, missing object window, irrelevant district or registration bug? | Actual constructed/completion with verified args, relevant/irrelevant inputs, missing/late city target and frozen evidence; no reset/witness by guess |
| T4 Late exit | Legal foreign-target window, consumer/write failure, or already-returned unauthorized endpoint? | Real Store+exit-owner local composition for each timeline, reentry/ref/token; no replay across endpoint fence |
| T5 Crew | Can each completion be uniquely attributed under actual event delivery? | Existing counterexample + exact native witness/signature investigation, then actual two-city owner composition; no count-difference grants |
| T6 A/B controls | Why do native click positions differ from helper replay? | Actual action IDs/hitboxes/instance/async plan delivery; guard test first, then one short clickable smoke after repair |
| T7 Delivery/registration | Is duty retained until explicit takeover through failures and second changes? | Real Bridge/FC/bindings/owner fail injection and successful-start/duplicate registration tests; no central replay |
| T8 Capital terms | Does passive UNKNOWN enter a new irreversible term and can modes separate safely? | Actual Commerce+Capital prepare/confirm cases and signed contract invariants; no new money formula |

Native observation is proposed only for a specific interface or timing fact source/local evidence cannot answer. T2/T5/T6 are likely candidates; T1/T3/T4 retain conditional needs. No experiment, probe, test or deployment is authorized merely by this proposed evidence path.

User decision: remaining contract/cell review R1/R2/R3/R5/R6; R4 is evidence-first, not a re-vote on DEC01–14. User testing: none now. Primary next: await discussion, then prepare v3 with exact approved contracts and acceptance boundaries.
