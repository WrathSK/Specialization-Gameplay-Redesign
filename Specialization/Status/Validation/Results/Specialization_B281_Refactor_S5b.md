# B281.308 — S5b guarded synchronous fact reuse

Basis9ec07fa. S5b complete; S5c/d, S6 and later stages remain separate. No gameplay or save-schema change.

## Runtime Impact Contract

EffectiveFacts owns one explicitly bounded synchronous FACT_PROPAGATION window around the existing Gameplay changes/consumer drain. Entries contain detached facts and scalar witnesses only,≤2048owner/city keys per window; capacity falls back to fresh reading. Window exit and exceptions discard it. RuntimeWork's former unguarded memo is replaced by a guarded NewReader scope: each short-lived Audit batch retains local reuse outside the shared drain, but every lookup revalidates the same authority/governor/write witness. No registry retains batches; native district/live-object indexes remain local and are not shared. Direct EffectiveFacts.Read outside either explicit scope remains fresh. Legacy Flow lacking the modern Store stamp stays uncached.

The real Store stamp executes existing active/storage.Check/not-committing, fault, reference and permitted recapture-token guards, then returns token/revision. Identity key also includes current owner/id/position/turn. Governor-dependent hits sample the actual existing six-property GovernorGate on every lookup; nil/invalid/inconsistent/UNKNOWN retains its old semantics. Neither facade VERIFIED alone nor a turn number authorizes reuse. Known non-pending results only are cached; copies isolate consumers. A failed/UNKNOWN witness drops old successful entries so recovery recaptures. Capture and reuse compare the final identity witness after governor reads and then check the write generation, preventing the tested getter reentry from returning the old identity.

Probe's owned SetProperty/CreateBuilding/RemoveBuilding wrappers invalidate before an attempt and after return or throw, preserve nil/multiple results and error objects, and only advance UI revision on normal return as before. Store begins its own barrier before replacing the in-memory root, and closes only after storage/readback/fault state settles. During writes, readers bypass reuse and retain original Store commit/HELD errors; they cannot read cached pre-commit success. An actual failed mutation cannot resurrect the old memo. No retry, timer, event subscription, player/city/building scan or persistent field is added. One fixed scalar facts_reuse counter is registered and included in existing memory-boundary totals; facts counts actual captures.

Safe-phase limitation: Lua cannot manufacture an atomic engine snapshot if an arbitrary final native getter silently mutates an earlier field with no observable write/event. Bounded witness comparisons catch the tested one-shot changes; there is no polling/retry loop or universal atomicity claim. Existing native synchronous read/owned-write contract remains the boundary. Normal production native Audits keep local batch reuse; cross-consumer reuse is specifically the declared Gameplay drain, not every unrelated native callback.

## Evidence

**LOCAL_SIMULATION_PASS:**16 independent new cases. Actual Store→Flow→EffectiveFacts and actual Housing/GPP yield one foundation capture for an unchanged shared window, two when real Housing removal intervenes; actual native definitions/presence are explicit doubles. Store two investments in one window see1→2→3, commit reentry rejects cached success, mutate-then-throw keeps Store HELD. Actual six-property governor reader changes without events reflect4→3→UNKNOWN→3→UNKNOWN→4. Token/owner/position/new-VM, first/last governor getter reentry, unknown recovery, copies, nested/throwing phases, nil/multiple results, same RuntimeWork batch after mutation, direct outside reads,2048capacity and fixed counter schema are checked.

Full selected167cases:164 properties PASS/3 laterOPEN; [closure](Specialization_B281_Refactor_S5b_Closure.json). Original T04 exact-one assertion is preserved; its workload now explicitly enters the same production phase, with an identified native authority stamp double. Independent new tests additionally use actual Store authority. The old counterexample was retired only after those independent13tests and a separate17-case run including the unchanged exact-one assertion passed; the resolved entry retains this evidence and frozen B272 before results remain untouched. Startup fixture now uses the real EffectiveFacts module rather than a generic no-op WithPhase double. No required assertion weakened. Final package194 Lua51/25XML/316files+modinfo308.

**Remaining:** scoped D invalidation, NetworkBridge busy merge/RouteSignal ownership, native consumer scope and cache working-set capacity retain3 strict counterexamples for S5c/d/S6. No new native/live PASS, deployment or main promotion; B271.298 remains deployed.

- **User decision:** none.
- **User testing:** final U5 unless a concrete blocking native fact appears.
- **Primary next:** S5c→S5d→S6→S7/S8→S9/S10.
