# Migration Impact & Dependencies — candidate Option B slices

Investigation / Non-authoritative / No design decision implied

Status: Stable | Maintainer: Primary

Baseline: `920b4ed2a8da5dd394b95fe03f96c81dc2a8a069`; D0058/A0183/S0866.

[Gap matrix](Gap_Matrix_v1.md) · [Decisions](Decision_Register.md) · [Evidence](Evidence_Appendix.md)

These are finite candidate packages, not implementation or deployment authorization. Accepted Architecture Markdown remains authoritative. After decisions, v2 must map each approved contract to implementation, exception, test and exit. Do not migrate from this drawing alone.

## 1. Sequence and scheduling conflict

Latest user sequence: current evidence reconciliation → v1 → owner decisions → v2 → choose U5 prerequisites → migration-preceding U5 baseline → Option B slices → convergence acceptance → balancing/extensions.

Existing original S9/S10 duties remain valid obligations. Earlier B399 review prose proposed completing all before U5; that is a scheduling recommendation requiring reconciliation with the latest user sequence, not a reason to silently begin cleanup now. DEC-11 must identify each pre-U5 row and explicitly reschedule the rest. No claim that U5 necessarily means original refactor completion.

## 2. Dependency graph

The graph describes work dependencies, not runtime calls. Solid arrows mean “requires approved contract/evidence first.” A package may contain several separately reviewable commits.

~~~mermaid
flowchart TD
  V1["v1 audit - this package"] --> D["Owner decisions and formal v2 contracts"]
  D --> PRE["Selected small pre-U5 fixes and proof gates"]
  PRE --> U5["Migration-preceding baseline U5"]
  D --> BASE["Matched workload baseline preparation"]
  U5 --> F["O1 fact/use and ACTIVE boundaries"]
  BASE --> F
  F --> N["O2 notification duty and availability recovery"]
  N --> C["O3 actual cold-source recovery integration"]
  N --> H["O4 bounded history/lifecycle extraction"]
  H --> R["O5 explicit extension registration"]
  C --> P["O6 applied institution presentation"]
  F --> P
  P --> X["O7 move legacy duties and safe package retirement"]
  H --> X
  BASE --> W["O8 measured work reductions and integrated closure"]
  X --> W
  R --> W
  W --> END["Convergence acceptance - named exits satisfied"]
~~~

O1 and O2 may be split by fact/owner; do not install a universal service before its first proven consumer. O4's approved repairs may proceed independently of cold network integration. O6's applied view need not wait for every O3 capability when its specific owner is already reliable. Arrows bound the conservative integrated path, not a requirement to serialize unrelated local work.

## 3. Candidate package contracts

| Package / affected gaps | Included scope | Invariants and principal risk | Prerequisites / regression | Exit condition |
|---|---|---|---|---|
| PRE / G03,G26; selected G04,G08,G14 | Only owner-selected small defects/proof resolution, each separate from architecture migration | No business formula/save expansion; no callback swap guess; Crew delta never authorizes grant | DEC-11; actual Commerce worker-failure owner test, real A/B controls evidence, D5 proof as applicable | Exact pre-U5 list passed or specific supported limitations explicitly accepted; deploy separately approved |
| BASE / G25 | Record comparable input/workload and available scalar/native evidence | No raw memory→Mod attribution or fake speedup; removable observers remain independent | DEC-12, existing collector/fixtures first | Baseline identifies version, workload, commands, measurement layer and gaps |
| O1 / G04–06 | Per-fact/use contracts and passive facade; raw governor/ACTIVE choice; existing strict APIs unchanged | Retained input cannot authorize irreversible action; exact negative/reference exit wins; D-1 and Reputation exceptions | DEC-01/02/03; real Research/Culture/Commerce owner combinations and no-value/cold/second-change faults | Each migrated fact/consumer has explicit current/retained/unknown and first-read behavior; no parallel ambiguous read route |
| O2 / G07–08 | Duty handoff, owner result states, same-value availability wake, fallible emitter bookkeeping | Coordinator never computes rewards or replays native actions; new causes preserved; failed siblings only | DEC-04; throwing Emit/consumer, HELD/no-op, missing target, close/load, finite attempt/rearm | Every declared automatic consumer has owner/wake/disposal; “delivered” cannot mean unproved applied |
| O3 / G09 | Wire approved NetworkRecovery Model/Cell/Store through actual Commerce/Culture writes/readers | Strict quote/confirmation proof unchanged; no Standardization exception expansion; derived record never history | O1/O2 relevant scope; tombstone-before-write, exact shape/postread ticket, finalize/withdraw both failures; domain mix/sets/lifecycle | Warm and cold D-2 actual writers preserve valid sources, withdraw confirmed loss, recover on meaningful facts; no orphan apparent APPLIED witness |
| O4 / G10–12,G16,G28 | Profession schema/transition owner boundary, deterministic D7 cases, exact late lifecycle recovery | No blanket reset, guessed origin/payment/completion or new ownership semantics | DEC-05/06/07/14 as relevant; G11 is evidence-only pending DEC-13, not a mechanical D7 repair; existing production deferred lifecycle tests; per-ability old/new differentials | Named supported cases reconstruct/transition once; unresolved origin/outcomes explicit and bounded; no silent permanent HELD called complete |
| O5 / G17–18 | Finite vocabulary/family/presentation and explicit capability registration | No automatic transaction/GPP/network participation; existing four-level rules unchanged | DEC-09/10; four-kind diff and hypothetical extension edit review | Adding a supported simple kind has finite named data declarations and independent owner implementation; unsupported anchor shapes reject explicitly |
| O6 / G15 | Owner applied publication → typed reply → institution view | Desired, last-confirmed applied, current applied/gate and unknown remain separate; no new UI gameplay computation | D11 already approved; owner publication input/lifecycle fences; failed application/cold/unobserved tests | Current surface consumes actual owner result; preview formulas labeled only as previews; obsolete candidate path retired |
| O7 / G22–24 | Q1–Q8 actual duty migration; exact deployment deletion review; narrow formal text sync | Preserve transport ACK/generation, cleanup/save/SQL IDs, unit decorators and timing; do not delete by name | Migrated callers proven; both deployment paths get audited exact removal+rollback before deletion ships | No production dependency on retired probes; each retained exception has end condition; package deletion/recovery tested; formal Markdown matches accepted state |
| O8 / G21,G25 | Only measured scope/capture reductions; integrated compatibility and evidence closure | No recovery removal or merged business policies to lower counts; no global cache | Earlier correctness gates and comparable workloads, P01–P10/T01–T08 as actually applicable | Declared work/retention budgets met; targeted native changed-path evidence; remaining accepted exceptions/limits explicit; user convergence approval |

G11/G13 are evidence gates: do not smuggle a new first-completion or Claim rule into a behavior-neutral package. G12 lower-bound E would be an explicitly approved Design delta, kept distinct from mechanical extraction. PT018 Expedition and city-ownership policy stay separate programs.

## 4. Minimum changed-path regression map

| Changed boundary | Previously accepted paths to protect | Necessary local contrast | Later native delta, only if needed |
|---|---|---|---|
| Fact/passive reads | Research support/Application/Chair/Infrastructure/Cross/Tradition; Culture Aesthetic/Meaning/Inspiration/Dialogue/Network; Commerce ordinary Gold | Same complete inputs produce identical carriers; retained inputs with provenance; confirmed loss; strict actions still blocked | One representative changed combination, not all four-profession numeric tests repeated |
| Notification/availability | Same-turn governor/potential, workers, building/GW/source updates | Register every confirmed change; latest fact allowed; emit/consumer fail; sibling no-op; load pending reconstruction | Existing ordinary governor/source/load session where delivery cannot be locally established |
| Cold network recovery | Ordinary route creation/expiry/ACTIVE loss/return/identity exit/max-forwarding/Capital/Development | Real writer+Store mixed-domain/sets, strongest-source fallback, torn metadata and two-sided carrier failure | Ordinary save/load+source change only after implementation; never ask player to fabricate UNKNOWN |
| Histories/lifecycle | Tradition/Reputation aging through governor absence; Dialogue start-era quota; Study L/E; REALLOCATING load/configure | Same policy before/after extraction; invalid subrecord isolation; deferred episode once; ambiguous money/unit no replay | Specific native evidence only for an affected unresolved API; ownership gameplay not added |
| Applied display | Correct institutions/banner/tooltip styles and current qualification | Owner applied result differs from candidate under failed write/held gate; stale reply rejected | One selected-city view after known change; no art redesign |
| Retirement/deletion | Startup, GreatWork paired ACK, production project timing, exact former-holder exits, Crew decorators | All production call sites relocated; no new dangling include/import; exact delete/failpoint rollback in both tools | Final candidate loading/turn/idle smoke with existing collector |
| Performance | Current correctness/finite recovery | Warm working-set sizes near bounds, idle repeated pulses, foreign irrelevant causes, same-turn second changes | Matched native counters/CPU/heap where measurable; limits stated |

## 5. Stop and completion criteria

Stop only the affected slice for a new gameplay ambiguity, unapproved saved/shared contract, unsafe native outcome, contradictory formal obligation or unresolved engine fact that local proof cannot answer. Do not weaken assertions, relabel old failures as PASS, or re-open the whole project.

Convergence requires all **required v2 rows** closed or an explicitly accepted bounded exception, formal Markdown matching the approved responsibilities, actual producer/consumer tests, changed-path native evidence where necessary, and no old/new production paths coexisting without a retirement condition. A clean compile, successful publication, U5 baseline pass or a lower audit count is not that acceptance.

User decision: DEC-11 chooses prerequisites; other DEC entries define the actual target. User testing: none in this audit. Primary next: after decisions, produce v2/contract change proposal; no implementation starts from this document.
