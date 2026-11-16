# B365.392 — S9a3a pure Store training input stamps

## Plan and Runtime Impact Contract

Accepted S9/F16,D15; base B364.391/1c4df82. Preparatory publisher only: Training UI still uses its original global/turn/Activity/LevelBanner signature. No dependency is removed and no extra SYNC/RESERVE/BUILD is added. This does not yet solve Gate capacity or Training.eligible's final independent binding read; those remain following slices.

CityProgressionStore.TrainingInputStamp(owner,cityID,x,y) reads only existing session positions/workers and fixed record scalars. Production uses the existing coordinate index,O(1); no new city index/cache,record copy,storage.Check,EffectiveFacts,ReadTemplates,native getter or scan. Explicit frozen legacy adapter keeps its existing two-record in-memory lookup,not a production fallback. Invalid scalar reference,unregistered/mismatched site,collection/worker unavailable and local commit return distinct provenance. This string is only a refresh input,never eligibility or native availability authority. Token/reference,lifecycle/removed/completion-held,restructuring phase,current investmentPending and observed binding state are represented; unrelated history/record revision is excluded.

Per worker,only six scalar binding observation fields are added. active reuses its original reference and single binding Property read; it keeps the original IsTestPlayer→origin owner→native reference short circuit. That existing read gains one protected Lua call so a thrown native read can be observed UNAVAILABLE,and rethrows the original exception object at level0. No extra native read/copy/write or swallowed failure. The hot binding path stores four reference scalars,not a newly formatted reference string; explicit stamp queries build the bounded signature. Missing/failed observation never means repaired binding or reset history. Recovery requires an actual subsequent existing read; the accessor itself cannot discover recovery.

Only the writing worker reports COMMITTING. The collection writing flag is intentionally not treated as every city's dependency: an unrelated worker write does not affect the selected city's stamp. A genuine collection fault is shared because all authoritative reads already fail. The getter explicitly chooses rest.investment when a restructuring record exists,otherwise the original ledger; it never falls back from a nil current epoch to old investment history.

T02/T04/T05/T08,L3 because active's protected native boundary is shared:10 new Inputs tests and21 directly affected actual Store/Summary/Investment/Tradition assertions PASS. New tests prove2000 pure queries with0 native/fact/scans/writes;pending-only INTENT/clear changes;CONSUMED_CONFIRMED stays same pending eligibility;unrelated revision/history and other cities stay stable;single binding absence/throw/read recovery preserves original exception;worker/collection faults;foreign/reused reference;loss;per-city commit isolation;and actual Begin→Configure→SETTLED current-epoch pending. All existing transaction/debit/history guards remain. No gameplay/save/amount/GC/listener/timer change.

During focused invocation an old S8b3 test that predates later Dialogue/Claim isolation was mistakenly selected directly and failed its obsolete whole-worker assumption. The accepted S8b4/S8b6 successors and frozen predecessor are already in the inherited stage selection; no assertion/source was weakened. Another new fixture initially used the old global a (a city rather than InvestmentAction) before T.invest; corrected its explicit fixture action binding. Independent final read-only review reran10 Inputs and diff check:PASS. It caught the current restructuring ledger omission before final source freeze; the real settled-epoch regression now covers it.

No UI switch,automatic native poll,new native event,permanent data repair,deployment/main/game launch or native PASS. Next Gate capacity scalar/event signals and remaining binding observations,then actual producer/UI composition before removing Training's global dependency; owner-applied display/adjacency,S10 and exact D7/D5 limitations remain OPEN.

### Machine validation evidence

- Stage/status: `S9a3a` / `LOCAL_SIMULATION_PASS`; tests=1005, passing=1005, registered-open=0.
- Source: base `1c4df826bb141123b7cc83bbea93663e1576b5d3`; dirty=True; input SHA256 `a967393433da2019b179af5aee3a64ad98fd25fed26308aec698a01b74e1f111`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9a3a --output local/refactor/S9a3a-B365-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9a3a-B365-final/closure.json`; SHA256 `372f74d3a6f5727ee28213eb35fa8cad3ec55656e994c09883891b527a3b41cd`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 205; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9a3a_pure_Store_training_stamp": {"UI_global_dependency_removed": false, "fact_reads": 0, "native_reads": 0, "new_cached_city_rows": 0, "queries": 2000, "scans": 0, "writes": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 392}
