# B317.344 — S7a3 D4 redundant repair cleanup

## Plan and Runtime Impact Contract

Authorized S7a/D4; base B316.343/a4226d4. Four reconcile conditions only: ResearchApply, ResearchInfrastructure, ResearchChair, ResearchCross. No gameplay definition, SQL, persisted data, deployment/main or game launch change. The explicit D4 user decision/configuration makes all InternalOnly SPC carriers unpillageable on supported current-version new campaigns.

Remove own-carrier damage as an active remove/recreate reason. Keep every real district/ordinary-building pillage input, the carrier presence/location/pillage read/UNKNOWN checks, wrong-location replacement and post-create unpillaged readback. Installed/read-only amounts still exclude genuinely damaged carriers; never report an ineffective carrier as actual benefit. CarrierHealthTrace D4 and exact NativeHealth remain intact, including damage notifications; there is no periodic retry. Already damaged old saves remain unsupported, without migration or guessed restoration.

T03/T05/T08: copied read-only engine schema/data and actual immunity SQL, real owner values under D4, ordinary/anchor pillage withdrawal/recovery, actual external carrier removal, same-turn sibling loss, UNKNOWN/failed create/idle budgets and retained health witness tests. Five old artificial-damage repair expectations are SUPERSEDED_FOR_UNSUPPORTED_CARRIER_DAMAGE for current source, not weakened or erased: execute those exact assertions against B316 source as historical proof, and test current source explicitly does not promise the removed repair behavior. All unchanged valid-state business outcomes remain equal. D4 native immunity still requires U5; static database configuration is not native PASS.

CarrierHealthTrace itself remains unchanged and currently covers basic support/GPP rather than these four full research families. Do not infer universal D4 trace coverage. Their existing Describe/readback still exposes ineffective/damaged state; this batch adds no background diagnostic scan.

### Machine validation evidence

- Stage/status: `S7a3` / `LOCAL_SIMULATION_PASS`; tests=103, passing=103, registered-open=0.
- Source: base `a4226d4422e18317c0249571187e74e968a45930`; dirty=True; input SHA256 `a9afc1ed0289b7fc305e5b02f3131a462001ec415245f6f59ab3e735bca35922`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a3 --output local/refactor/S7a3-B317-stamped/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a3-B317-stamped/closure.json`; SHA256 `83f5033c074d79292c28b785254b6764866be34ee29ef8e6ff2188ef917fddfa`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 64; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4c1_exact_health": {"D_recaptures": 0, "changed_cities": 1, "other_writer_audits": 0, "thousand_idle_extra_reads": 0, "writer_audits": 1}, "S7a3_D4_copied_engine_configuration": {"all_InternalOnly_Pillage0": true, "family_rows": {"APPLY": 25, "CHAIR": 104, "CROSS": 32, "INFRA": 4}, "native_immunity": "USER_GAME_TEST_REQUIRED", "non_SPC_unchanged": true}, "S7a3_frozen_artificial_damage": {"current_classification": "SUPERSEDED_FOR_UNSUPPORTED_CARRIER_DAMAGE", "reason": "D4 no-pillage current-version new campaign; original frozen evidence remains", "source": "a4226d4", "unchanged_assertions": ["test_live_pillage_repairs_without_dead_events_and_does_not_rearm_self", "test_confirmed_damage_during_creation_is_not_suppressed", "test_actual_cross_pillage_repairs_through_exact_health", "test_actual_cross_UNKNOWN_holds_then_reliable_sample_recovers", "test_refactor_s5d4c2.InfrastructureHealth.test_exact_loss_and_pillage_keep_existing_repair_policy"]}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 344}
