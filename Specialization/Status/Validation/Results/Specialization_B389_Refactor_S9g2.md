# B389.416 — S9g2 / explicit invalidate–verify–finalize mechanism

The approved network recovery contract requires safe ordering before actual persistence is connected. NetworkRecoveryCell is packaged import-only with explicit injected read/write/current-receiver callbacks. No Store,Commerce,CultureNetwork or Gameplay inclusion,Game Property key or native slot is implemented yet. The actual native namespace/setter/barrier/workload composition is the next gate.

Changed data first replaces old evidence with a small version/family/sequence/receiver INVALIDATED tombstone containing no candidate source facts. One attempt and exact postread are required before a private single-use carrier ticket exists. Only the caller's explicit actual carrier/source proof,current receiver and tombstone CAS permit APPLIED publication. A retained source must equal a source in the previous APPLIED bundle apart from its usage label;UNKNOWN/unconfirmed aggregates/invalidated records cannot supply it. The mandatory caller input gate still owns reliable facts and old physical-shape verification. A decoded label is never that proof or a transaction credential.

Identical immutable payload apart from proposed sequence skips both metadata writes,retains the existing sequence and still verifies actual shape plus final CAS. Other successful updates use2 callback writes. Begin/Finish keep only transient operation buffers;idle cells retain no encoded bundle. Old read/schema/version,proof,drop/throw/stale readback,context change,stale/forged/reentrant capability and CAS failure never yield success or automatic replay. Aborting discards private capability only. Typed reads during a call/ticket expose no candidate;pending/stale-reference/shape-mismatched slots supply no recovery facts. This assumes the future adapter's explicit sole writer;it is not hardware-atomic CAS or a generic exactly-once transaction.

Runtime Impact/T01/T02/T03/T04/T05/T08,L2 and implementation-contract intake are recorded before code.44 local cases include inherited codec tests and24 cell scenarios,real mutation followed by stale postread in both phases,callback proof/receiver reentry,sequence exhaustion,cold pending reads,same-value work and10000idle status reads with zero callback work. Injected callbacks are explicit native doubles;they do not prove an engine Property write/save,normal frame cost,CPU or heap. A final same-value proof callback that mutates the slot is rejected by the post-proof CAS;changed writes retain both pre/post proof checks. Existing permanent Copy limits and all gameplay stay unchanged.

The future writer must address metadata-failure negative withdrawal/cleanup and later coincidentally equal physical encodings,not just positive success. It must review the existing Probe setter's global UI/fact feedback before selecting a scoped technical setter;this pure batch bypasses nothing. Source/carrier/native-store ordering and strict transaction separation remain required composition tests.

User decision:none pending. User testing:U5 after real integration. Primary next:actual scoped native adapter and carrier failure ordering,then Commerce/Culture restoration and remaining S9/U4/S10. No deployment/main/game launch.

### Machine validation evidence

- Stage/status: `S9g2` / `LOCAL_SIMULATION_PASS`; tests=44, passing=44, registered-open=0.
- Source: base `07991a5104c5078aa2503b4eff63a5ee238c9546`; dirty=True; input SHA256 `a33d2b76c1546eb9278422f1fe9a54ba1906d99aa62d013190f5ce666c880099`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9g2 --output local/refactor/S9g2-B389-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9g2-B389-final/closure.json`; SHA256 `8a9cdee65db9805343d81207a25e16a7fb7e27160d2e603c3e915cc24a4c65e3`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 2; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9g2_new_cell_commit": {"actual_carrier_proof_required": true, "automatic_calls": 0, "callback_writes": 2, "candidate_facts_in_pending": false, "invalidated_before_ticket": true}, "S9g2_same_value_budget": {"callback_reads": 3, "callback_writes": 0, "final_shape_proofs": 1, "idle_encoded_cache": false}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 216, "XML": 25, "package_files": 338, "modinfo": 416}
