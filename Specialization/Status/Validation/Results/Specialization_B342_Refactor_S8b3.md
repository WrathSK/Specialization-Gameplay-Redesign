# B342.369 — S8b3 Research Tradition isolation

## Plan and Runtime Impact Contract

Accepted U1/D7 and S8/C005; base B341.368/6823150e2cde53ec4e6fc499875104351fcff25c. Extend only the fixed reviewed leaf list from Insights to Insights/ResearchTradition. On failed restoration, independently classify each reviewed leaf CHECK_FAILED, omit only these in a bounded validation copy, and require the entire remaining parent/all other abilities to pass unchanged strict validation. Either or both may isolate; a core or unreviewed second ability failure still holds the worker. No write/revision/repair on load.

The existing save gate normalizes the complete candidate, requires every isolated field to equal its old committed field including unknown extensions, then validates the full remaining parent before any optimistic publication. Actual CAS/readback keeps every original field. Session sidecars remain fixed two-field diagnostic summaries per worker, never archive replicas. Healthy validation/writes have no new CheckOne/copy path. Isolated writes and failed restore add only bounded copies/two fixed pure checks, no native scan/event/timer or growing cache.

ReadTradition rejects isolation. TickTradition returns before native site reads/Advance. P4 investment cannot initialize/replace invalid age history. InstitutionHistory skips only the bad start fallback and retains independently proved establishment timestamps. Begin/FinishRestructuring skip only invalid age Advance; confirmed loss does not mutate the bad field's owner-policy state. Core lifecycle, original transaction, other ability cancellations/commit barriers and sidecar lifetime remain. No current-turn/P4-date inference, backfill or age reset.

VisitTradition keeps its original city routing. The effect owner independently processes reliable identity/ACTIVE loss before it asks for history: confirmed ACTIVE<4 can remove old yields; an otherwise qualified city whose age getter fails remains UNKNOWN and keeps the existing guarded effect behavior. Early candidate review exposed that placing an isolation assertion in Visit would suppress this confirmed withdrawal. That uncommitted candidate was corrected; a fixed actual Store/EffectiveFacts/ResearchTraditionEffects counterexample contrasts the rejected early-Visit guard with the preserved route. No effect gameplay rule changes.

InstitutionSummary publishes traditionKnown=false with no tradition value, while other metrics stay known. Presentation uses PENDING rather than NOT_STARTED/zero and includes availability in its signature; Gameplay's existing conditional skips Shadow when no age value exists. Legacy healthy summaries remain compatible.

T04/T05/T06/T08: actual Store verifies single/two-leaf isolation, complete preservation across normal investment/P4,20 turns, loss/return and full restructuring, rejected destructive writes/metatable replacements, remaining core/ability guards, and qualified UNKNOWN versus confirmed effect withdrawal with1000 idle publications. All16 original healthy restructuring tests run unchanged with explicit Lua5.1 native doubles. The prior B341 matrix asserting that Tradition was outside the first leaf scope runs unchanged against exact B341 source; the new current matrix keeps all core/unreviewed failures strict. No assertion weakened.

Remaining D7 recovery limitation: current turn, P4 receipts/date and surviving carriers cannot reconstruct exact accumulated age across past pauses or unknown intervals. If identity/ownership changes during isolation, a future authorized reconstruction must also honor those confirmed lifecycle facts; blindly releasing an old COUNTING payload would be unsafe. This slice offers no repair setter/reset and does not claim permanent HELD is a completed normal recovery policy. Other abilities and permanent-recovery proof remain OPEN, as does D5 native completion attribution. No deployment/main/game launch or native PASS.

### Machine validation evidence

- Stage/status: `S8b3` / `LOCAL_SIMULATION_PASS`; tests=652, passing=652, registered-open=0.
- Source: base `6823150e2cde53ec4e6fc499875104351fcff25c`; dirty=True; input SHA256 `67df073a48b1e652547dca867f15ecccbeeb7c62117bd4b06dbd691aeddf0bff`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b3 --output local/refactor/S8b3-B342-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b3-B342-final/closure.json`; SHA256 `3bfaed5125470f510de0ecbe54a8c3008948d6cf735d4cc2400cc1bfe1f45c41`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 162; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b3_actual_Tradition_effect_routing": {"confirmed_ACTIVE_drop": "withdraws", "history_writes_from_effect": 0, "isolated_qualified_history": "UNKNOWN_retains", "modules": "Store/EffectiveFacts/ResearchTraditionEffects"}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 369}
