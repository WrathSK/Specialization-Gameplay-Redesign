# Audit follow-up priorities and Advisory publication review

Date: 2026-10-13
Maintainer: Primary (user-authorized main task)
Basis: develop `bae883a`; current B204 native gate unchanged.
Scope: record the user's scheduling decision and review Stable Advisory reports for publication. No implementation, new gameplay decision, native test, or reopening of the completed independent audit.

## User-confirmed scheduling

All outstanding findings from both the [independent audit](../Audit/P16b_P17_Final_Audit.md) and [Advisor architecture review](../Advisory/Architecture_Engineering_Audit/Final_Review.md) remain deferred follow-ups, not a blanket block on development. Previously completed repairs stay completed; historical findings are not silently reopened.

Before developing a module that would materially multiply an existing problem or make repair substantially harder, review the relevant finding against current code, propose a bounded repair and obtain the usual implementation authorization. Do that repair before building the dependent feature. This is sequencing, not standing permission to implement every finding.

Historical severity and timing labels, including FIX_NOW, remain evidence of the original recommendation. They do not override this scheduling decision. Local bugs, speculative native risks and cleanup items do not automatically block unrelated work. A newly confirmed concrete safety/correctness risk should be reported with its affected scope, rather than silently ignored or turned into a project-wide stop.

| Development trigger | Findings to re-check before that work |
|---|---|
| Expedition reattachment, repeated missions or N2 rewards | Expedition A/B/D/E/F/G/H; cap ownership, recovery, native-read availability and context-faithful tests |
| New persisted city asset or transaction | AF-01/12/13; independent audit P06a/P07 boundaries; commit visibility, exact receipts, history preservation and recovery policy |
| New investment-dependent consumer or central module integration | SD-01, AF-02/09/10; wrapper return values, actual Start composition and event delivery |
| New high-frequency state writer or carrier family | AF-06/07 and prior hot-path findings; actual notification cadence, facts collection and scoped invalidation |
| New network consumer or Harbor/Commerce route expansion | AF-14 and P13a-Q04; partial/UNKNOWN policy and explicit transport bounds |
| Industry template knowledge or Crew source/inventory work | AF-23 and P07c-F01; reliable presence before initialization and receipt readback |
| First additional profession | AF-28; kind vocabulary and persistence validation, followed only by the shared primitives that profession actually needs |

These are planning triggers, not an exhaustive duplicate finding register or a requirement to finish an entire platform rewrite. Use the linked reports for original evidence and limits. No new permanent registry, manifest or mandatory all-report reading set is introduced.

## Newly reviewed Advisory reports

- [Future specialization feasibility](../Advisory/Future_Specialization_Feasibility/Future_Specialization_Feasibility.md): useful planning inventory for seven future professions. Its strongest reusable themes are unit attribution/training snapshots, route facts, multi-turn projects, and profession-unit lifecycle. Difficulty/carrier-count estimates are advisory forecasts, not measured delivery schedules or native costs. Community and Landscape remain candidates; none enters v0.1 by publication.
- [Self-healing reconciliation proposal](../Advisory/Self_Healing_Rules/Self_Healing_Reconciliation_Rules.md): useful catalogue of stuck-state concerns and proposed recovery policies. None of R1–R20 or D1–D10 is adopted here. Per-feature ownership, irreversible outcomes and existing accepted protection rules remain authoritative.
- Their four [architecture-review dependencies](../Advisory/Architecture_Engineering_Audit/Final_Review.md#8-checkpoint--handoff) are included byte-for-byte at the author's Stable checkpoint, to keep their links and finding IDs accessible. Phase B/C qualifications in Final_Review take precedence over Phase A wording. Publication does not certify every claim.

## Primary review qualifications

### Recovery proposal: not an implementation-ready common policy

1. Returning capacity is not automatically harmless: it permits another admission. A late native birth or an off-map travelling Spy can make a false release produce over-capacity or lose ownership. The reports themselves leave off-map enumeration UNKNOWN. A deadline and an empty visible queue alone do not prove absence.
2. Generation changes only reject observations that can be reliably attributed to a generation. Current `ExpeditionTraining.Birth` and `Complete` native callbacks carry player/unit/city information, not the request generation. The existing Store generation is not proof that arbitrary late native events become safe (proposal R6).
3. A receipt written with a Store transition is not an atomic commit with a native unit destruction or reward operation. R7 needs an explicit per-operation readback/uncertainty contract; it does not remove the native-action crash window.
4. Saved history is authoritative for facts that the engine no longer retains. It must not be downgraded to a disposable belief and rebuilt from current observations. UNKNOWN remains distinct from absence and confirmed loss.
5. The proposed local-turn/load reconciliation must not replace foreign-event paths needed for loss exits or UNKNOWN recovery. `LoadScreenClose` and turn-start are candidate hooks, not proof that every required UI/native fact is ready.
6. R19's one-write-per-city-per-turn limit cannot suppress ordered transactions or real same-turn changes. Coalesce only redundant derived recomputation; define actual collection cost before claiming linear complexity.
7. Releasing a hold, choosing partial aggregate fallback, dropping an uncertain reward, or accepting older save shapes can alter accepted semantics. Decide these per feature before implementation, without adopting a universal release rule or adding an unapproved save-compatibility obligation.

### Feasibility report: preserve uncertainty and incremental sequencing

- Source-visible modifier/API examples are implementation candidates, not native PASS. Statements that no route exists mean no route found in the inspected sources, as qualified in the report's limits. External HD version remains UNKNOWN; current installed behavior was not independently re-tested here.
- Re-read current accepted Design when a feature is scheduled. Candidate names, unresolved formulas, and draft diplomacy/landscape/community directions remain at their existing maturity.
- Do not automatically schedule every proposed spike, an entire platform batch, a global turn scan, or GC changes. Inherit applicable existing evidence; request only the new native uncertainty for the actual batch.
- Static re-check of `CommerceConvergence.outputChanged` confirms an unscoped Audit after a changed global revision at a publish/playback callback, but multiple writes before that callback can coalesce. The report's shorthand “each write costs a world audit” is not a measured one-to-one invocation count, CPU cost or memory attribution.
- Source history since the architecture-review basis has no Mod change, but does include the new publication-gate test. “Source unchanged” must not be read as all DevelopmentTests being byte-identical.

## Review coverage and publication boundary

Primary read both new reports in full, revisited the architecture review's final priorities/limits and Stable handoff, checked Design maturity excerpts, and spot-checked `RuntimeWork.Hook`, `CommerceConvergence.outputChanged`, `CrewPrecision`'s wrapper, `ExpeditionTraining` queue/receipt callbacks, and `ExpeditionSpyGate`/Store load and generation boundaries. This is bounded publication review, not a second complete architecture audit. No external game-source rescan, gameplay regression, native experiment or new API availability claim was made.

The older local `Publication_Safety_Audit` report is not included in this publication. Its conclusions about zero deleted paths and expired credentials need author-side qualification before publication; its no-hook/path-remediation observations also predate `cb28bb6` and `bae883a`. It remains unchanged and ignored. Raw logs and frozen evidence remain untouched.

The six included Advisor originals are immutable for this checkpoint: no editorial rewrite, change of findings or hidden adoption. Primary's qualifications live here. Before staging and commit, verify their bytes still match the reviewed checkpoint; check local links/anchors, staged privacy/secrets, exact file scope, and current context integrity. A privacy PASS establishes only the scanner's covered patterns, not complete absence of sensitive information.

User decision: scheduling above confirmed; recovery/feature design proposals remain unaccepted.
User testing: none requested; existing B204 native test remains pending.
Primary next: resume normal authorized development; consult relevant findings before the dependent module, propose scoped repair where required, and wait for implementation authorization.
