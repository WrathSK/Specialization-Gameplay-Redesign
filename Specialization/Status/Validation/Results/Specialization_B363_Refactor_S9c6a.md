# B363.390 — S9c6a fixed institution presentation replies

## Plan and Runtime Impact Contract

Accepted S9/F25,D15; base B362.389/2ee79ed. Add only fixed CITY_PRESENTATION scope and independent8-slot Presentations endpoint alongside ACTION/VIEW/TARGETS,total32 retained positions. Its identity is CityID,not UnitID; envelope explicitly omits unsolicited UnitID/native objects. Parent session allocation/order/shutdown remain fixed. No generic serializer or automatic consumer. UI still uses its old path until the next slice; dual-consumer global overwrite risk is not claimed fixed yet.

Projection copies only existing14 top-level display fields,4 archive keys and17 summary fields,plus4 reference/5 tradition/2 reputation fields. Successful payload is at most6 fixed tables/45 key-value pairs; no history/template/insight detail arrays or receipts. Request token and Store summary.token remain distinct. nil,false,zero,empty archive,unknown active,building-only districtTemplates=nil and summary={known=false} retain their meanings. Finite numbers preserve precision and do not add gameplay limits. Strings have individual bounds(request/Store token256,status128,error20000),and32KiB cumulative text budget; no truncation or partial success. Invalid projection sends fixed PRESENTATION_UNAVAILABLE only; cannot evict retained same-key evidence. Capacity is fixed,Take/Discard/shutdown release references,and no native objects are retained.

Gameplay admits the explicit role/epoch before original reads,then builds the same values once. The existing Tradition Shadow/history calculation remains unchanged pending the separate applied-owner display work. Archive,summary isolation and zero-write behavior remain. x/y now come from the same selected city inside the existing protected read; two unsafe post-pcall GetCities/FindID calls disappear,and final GetOwner/GetID add two scalar native checks. Compared with the old success path this is -2 exact-city lookups,+1 owner getter,+1 ID getter,unchanged coordinate getters. Native reference/read failure becomes an explicit unavailable city result. This is a sequential safety fence,not an engine-atomic snapshot. Same parent/child required for publication; failure never resamples facts or summary. Legacy global DTO and bounded diagnostic mirror remain.

T04/T05/T08,L3 for fixed-role transport/reference boundary:18 focused tests pass:6 projection,6 actual Gameplay producer and all6 original B251 StoreSummary assertions unchanged on explicit Lua5.1. Cover detached fixed nested tables,all false/nil/zero distinctions,large valid historical scalar counts,metadata/nonfinite/plain/text failure,CityID vs extra UnitID,independent ring eviction/shutdown,legacy/typed same values,one facts/archive/summary read,summary failure isolated from Potential/ACTIVE,reference exception/owner change inside protected read,service reentry and negative publication without replay. Original B251 dynamic source extraction still executes the actual branch; no assembler mock replaces it.

An initial direct invocation of old B251 tests used that legacy fixture's default Lua5.5 and failed on Lua5.1 global unpack. The new profile wraps its existing runtime in TrackedLua51 (as the established ActualProfile does),retaining all six assertions; no production workaround or weakened assertion. Independent review is recorded below when complete. No deployment/main/game launch/native PASS. Next migrate CityPotential as sole Take and Overview as accepted DTO consumer,then owner-applied fields/training/adjacency and S10. Exact D7/D5 limitations remain OPEN.

Independent read-only review found no blocking runtime/fixture issue. It corrected the measurement boundary: normal successful producer45 keys; projection also permits error alongside ordinary fields,so its absolute whitelist maximum is46 keys/6 tables. First943 PASS artifact remains local; final2 corrects that measurement without runtime or assertion changes.

### Machine validation evidence

- Stage/status: `S9c6a` / `LOCAL_SIMULATION_PASS`; tests=943, passing=943, registered-open=0.
- Source: base `2ee79ed13f84bc1160c41c97c10c370758de0c49`; dirty=True; input SHA256 `1acde928c400a272ac583681c8fc0daa8957711c96e311455622adb886e14a6c`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c6a --output local/refactor/S9c6a-B363-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c6a-B363-final2/closure.json`; SHA256 `a8c43b04905196a7810ff0c2684a32c03bf26ccff27e4882bfdb4f58a5e239d4`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 200; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c6a_fixed_presentation_transport": {"UI_migrated": false, "max_fixed_payload_keys": 46, "max_fixed_payload_tables": 6, "native_reads_in_projection": 0, "normal_successful_producer_keys": 45, "ports": 4, "slots_per_port": 8, "text_budget": 32768, "total_max_slots": 32}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 390}
