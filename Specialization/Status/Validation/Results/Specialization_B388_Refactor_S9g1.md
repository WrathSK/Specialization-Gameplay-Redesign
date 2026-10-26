# B388.415 — S9g1 / pure bounded network evidence framing

This is the first prerequisite of the second approved A0183 extension. NetworkRecoveryModel is packaged import-only;Store,Commerce,CultureNetwork and Gameplay do not include it. There is no new saved field,Property read/write,event,callback,timer,cache or automatic consumer yet.

The strict v1 shape contains family/sequence,existing receiver/source reference and Store lifecycle-stamp scalars,the actual carrier shape,and detached source facts/provenance. Commerce uses its existing5 domains and nonnegative binary64 X values;Culture keeps overlapping complete-civilization sets through one sorted civilization dictionary. UNKNOWN cannot contain a fabricated value,eligibility or set. Decoding/provenance labels are not source qualification,confirmed carrier commit or transaction authority;the future Store/writer must prove those independently and retain old immutable facts only through exact prior witnesses.

Canonical length framing sorts source IDs/domains/civilizations,uses DECIMAL17 strings for source numbers and exact integer frames,rejects duplicate/unknown/future/oversized/noncanonical/trailing/truncated inputs and unsupported nested shapes. Bound:512 sources,64 complete civilizations per source,<256 dictionary entries,references/stamps≤512bytes,identifiers≤128bytes,wire≤1MiB. No silent truncation. Existing8192-node/65536-byte permanent Copy stays unchanged;this bundle must not be forced into that envelope by enlarging its budget. Its separate derived storage/ownership and invalidation-before-carrier/finalization-after-proof protocol still need implementation and failure-order tests before production wiring. Worst-case encoded/local work is separate from native Property capacity,CPU/heap and practical game limits;those are not proven by this codec.

Runtime Impact/T01/T02/T03/T04/T08,L2 is recorded before code.20 focused tests exercise exact/canonical roundtrip,all3 provenance states,overlapping sets,negative/NaN/future/unknown/meta failures,integer/double precision,byte-prefix truncation,new Lua context,no native/Copy access,actual maximum512-source/domain/civ shapes and package-only inclusion. An initial maximum-name fixture was129bytes;it was corrected to the documented128-byte boundary without changing the strict production limit. No gameplay,aggregate inversion,Std-only A expansion or old-save/native restoration is claimed.

User decision:none pending. User testing:U5 after actual integration,including native Property/save limits. Primary next:derived-slot/CAS/carry-proof and carrier failure ordering,then actual Commerce/Culture cold restoration and remaining S9/U4/S10. No deployment/main/game launch.

The1MiB codec ceiling is a reject boundary,not permission for an equally large per-receiver resident cache. Production storage/cache residency,normal event write cost and native payload limits must be reviewed before wiring;the measured worst-case framing deliberately uses maximum512-byte opaque witnesses,not a normal-game memory estimate.

### Machine validation evidence

- Stage/status: `S9g1` / `LOCAL_SIMULATION_PASS`; tests=20, passing=20, registered-open=0.
- Source: base `7597f63b0a7f070b6d31fa6e342f1d5e66347aa3`; dirty=True; input SHA256 `7e63010e0388387312ccb0cf33d187911e68c883fe4e150354ce112af85d0d29`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9g1 --output local/refactor/S9g1-B388-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9g1-B388-final/closure.json`; SHA256 `3686d99d330b0e41b1e520b120e85277e3410f3e87d2a4f192a572932d090141`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 1; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9g1_decimal17_network_values": {"binary32_fraction_counterexample": true, "double_roundtrip": true, "native_Property_writes": 0, "wire": "canonical string framing"}, "S9g1_maximum_commerce_bundle": {"automatic_calls": 0, "base_Copy_budget_changed": false, "domains_each": 5, "reference_and_stamp_bytes_each": 512, "sources": 512, "wire_bytes": 620017, "wire_cap_bytes": 1048576}, "S9g1_maximum_culture_bundle": {"civilizations_each": 64, "dictionary": 255, "native_storage_or_CPU_claim": false, "sources": 512, "wire_bytes": 723691, "wire_cap_bytes": 1048576}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 215, "XML": 25, "package_files": 337, "modinfo": 415}
