# B341.368 — S8b2 Insights-first subrecord isolation

## Plan and Runtime Impact Contract

Accepted U1/D7 and S8/C005; base B340.367/4da6a1a. First vertical slice only: preserve strict identity/reference/envelope validation and all original ability assertions, but allow independent Insights failure to stop that ability without making every other city capability unavailable. All original malformed history remains saved. No saved schema/key, automatic recovery event, timer, user repair UI, Expedition feature change, permanent damage verdict or zero-baseline reset is introduced.

Restoration first obtains the established complete bounded native copy. If full validation fails, a fixed CheckOne independently checks the Insights owner and only a CHECK_FAILED observation plus unchanged full-parent validation with that leaf omitted may establish a session-only ISOLATED sidecar. Other core/ability failures still hold the worker. Copy cycles, unsupported types,8192-node/depth12/65536-byte limits, missing/throwing native reads and temporary decoder errors never become isolation or reset evidence. Prior deterministic known-flag recovery keeps its full validator/CAS path.

Every normal write still passes the existing worker save. In isolation, a bounded normalized candidate copy must contain exactly the original Insights field, including unknown extensions, before any optimistic root publication; only the validation copy omits it. Normal actual commit, old-value comparison and native readback retain the whole original field. Normalizing before comparison prevents a metatable fallback from disguising an empty replacement. No save path automatically isolates a new bad value. All existing independent writes, loss/return and revisions retain the sidecar; a new worker/load reassesses actual source instead of treating a previous observation as saved authority. No duplicate archive is retained in the sidecar.

Getter and Add explicitly reject isolated Insights rather than returning an empty archive or permitting a new first-success key. InstitutionSummary returns known=true for independently valid data, insightsKnown=false and no numeric insights. Presentation includes this availability in its signature and shows the existing PENDING for Culture IV only. Legacy summaries without the added flag keep previous display behavior. Error formatting retains only bounded plain strings for isolation; no native object is retained.

Work impact: one fixed pure leaf check plus one full masked-parent validation only after failed restoration; isolated writes add a bounded copy and deep equality over the preserved leaf. Healthy writes retain their prior validation path. Sidecar is one fixed scalar diagnostic per affected worker, no growing histories/cache/listeners or automatic work. Independent strict validation is not a permanent irrecoverability test.

T04/T05/T06/T08: actual Store and existing native doubles verify original bytes/extensions and zero load writes, independent APIs, investment/ticks/revision, loss/return, rejected mutations including metatable forgery, exact native CAS/uncertain setter behavior, cold reload reassessment, ordinary bad input rejection, sibling city and full base protection, and pending presentation. Test-only private save capture verifies the real save barrier, rather than incorrectly using the fixture storage.Write bypass. Focused test construction corrections: avoid Lua5.1 empty double-semicolon and read potential from EffectiveFacts rather than the raw investment ledger; no runtime guard or assertion was weakened to fix the fixture. All prior strict regressions remain selected, plus institution presentation/summary scenarios.

D7 boundary remains OPEN: current tasks, tourism carriers, current buildings and a structurally valid table do not prove a complete first-success archive. There is no independent authoritative full archive replica to deterministically rebuild all keys. A single failed read/validator or an invalid copied leaf does not prove permanent irrecoverability. This slice preserves evidence while subsequent ability-specific work and the remaining permanent-recovery boundary continue; it does not claim permanent HELD as a normal finished recovery policy. D5 native completion proof remains OPEN. No deployment/main/game launch or native PASS.

### Machine validation evidence

- Stage/status: `S8b2` / `LOCAL_SIMULATION_PASS`; tests=622, passing=622, registered-open=0.
- Source: base `4da6a1a01d7ac1f01e1a193684d55043dc05cc8d`; dirty=True; input SHA256 `b1e5c9605b3898c82f981c1e7f884283e467c6f22ed41a172c8b05e6cd6145de`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b2 --output local/refactor/S8b2-B341-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b2-B341-final/closure.json`; SHA256 `10c022f0c8020b76fa6f7e1113aeb37ae47c44ef0f1ba5a56477f1259fc3746b`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 160; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b2_Insights_isolation": {"base_and_other_abilities_usable": true, "invalid_leaf_preserved": true, "load_property_writes": 0, "permanent_corruption_or_reset_claim": false}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 368}
