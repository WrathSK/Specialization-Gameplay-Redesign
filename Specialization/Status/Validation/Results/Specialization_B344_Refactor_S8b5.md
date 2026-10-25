# B344.371 — S8b5 opaque Capital/Development history isolation

## Plan and Runtime Impact Contract

Accepted U1/D7 and S8/C005; base B343.370/5701d4a. Extend only the fixed reviewed groups to Capital/Development, including both known marker and payload fields. Existing pure marker-candidate proof and full remaining-parent validation apply unchanged. No new schema/property, money transaction, quote/eligibility rule, listener, timer, retry manager or runtime module.

State/Write APIs reject the isolated group before Decode, old-value comparison or mutation. Visitors report isolation after owner filtering, before checking an empty payload or decoding it; CapitalKnown=true with missing payload must not silently become no contracts. The existing outer visitors protect each worker and still visit healthy siblings. CapitalReference is shared core identity and remains available. Skip only interpretation of invalid Capital protection reset during restructuring and each invalid contract group's Terminate during confirmed loss; full original fields persist through lifecycle. Healthy transactions and lifecycle behavior remain unchanged.

Capital always re-reads State for confirmation; settlement consumes only proved visitor values. Development re-reads State for confirmation/reconcile, and its existing readIndex propagates visitor failure into indexError. Preserve this global occupancy protection: an opaque source may contain an open contract, so even a healthy other source cannot make a new Development contract while occupancy is unconfirmed. Existing known records can still be visited/reconciled; no scope-wide false empty result. This is the existing capability dependency, not a new gameplay restriction or a reason to relax duplicate-target protection.

Actual money-service tests use structurally valid model CALLING records with deliberately invalid source authority, then reload the actual Store/service. Neither debit nor credit nor RNG/contract payload is replayed. Capital in another healthy city can still sign. A healthy P4 Development source is independently readable but correctly held by unknown occupancy. Existing access-marker and Development cold-load cleanup policies remain; no new refund, reset, current-balance inference or held-result replay.

Work scope: two more fixed checks only after failed restoration, six groups/ten declared fields total; healthy path unchanged. Isolated writes use the existing bounded copy/per-field equality/full remaining-parent/native CAS gate. Sidecars remain fixed scalar observations, not monetary archives or native objects.

T04/T05/T06/T08:12 focused actual Store/Capital/Development cases cover nil payload+known=true, full-field preservation, valid-marker reconstruction alongside a bad group, protected temporary decoder failure/no1000-idle retry, independent sibling visitors, remaining core/unreviewed errors, loss/return/restructuring, both Capital CALLING stages, healthy Capital signing and healthy Development source occupancy gating. Money/contract counters are separate from legitimate ongoing Commerce age writes. Test fixture corrections retained the fake Bridge/D dependencies across reload and constructed model-valid CALLING receipt shapes; no production guard or transaction assertion was weakened. Four prior scope/failure matrices execute unchanged on exact pre-extension B343 source; all other strict inherited tests remain.

D7 recovery remains OPEN: current treasury balance and existing buildings cannot prove old debit/credit outcomes or reconstruct contract ownership/receipts. If lifecycle Terminate/protection reset was skipped during isolation, a later structurally valid old payload alone is insufficient to resume execution; reliable lifecycle and transaction evidence are still needed. This batch provides no repair setter/zero baseline/replay and does not claim permanent HELD as the final normal recovery policy. Commerce/reputation, templates/claim and D5 native attribution continue. No deployment/main/game launch/native PASS.

### Machine validation evidence

- Stage/status: `S8b5` / `LOCAL_SIMULATION_PASS`; tests=672, passing=672, registered-open=0.
- Source: base `5701d4a0232478ce16ecdd6b9740eece78d4e5bd`; dirty=True; input SHA256 `5bd7c024c0019dbfdf0dd3ad342260b6151c74f0a2f616b8ba8f38a48e43a2ef`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b5 --output local/refactor/S8b5-B344-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b5-B344-final/closure.json`; SHA256 `cdb7f126a3d6977e1195757abe0e3a2a3b268f1472ad6b65c00a08bd60458495`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 164; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b5_actual_opaque_money": {"Development_new_signing": "held_by_existing_global_occupancy_UNKNOWN", "healthy_Capital_source": "independent_signing", "native_operations_replayed": 0, "raw_contracts_preserved": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 371}
