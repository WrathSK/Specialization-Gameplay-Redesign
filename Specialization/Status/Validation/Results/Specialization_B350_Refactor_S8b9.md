# B350.377 — S8b9 provable template metadata reconstruction

## Plan and Runtime Impact Contract

Accepted U1/D7,S8/C005; base B349.376/6471b6d. This narrow deterministic-rebuild path follows the remaining proof inventory,independent of the completed neutral S9a1 registry. It does not classify permanent irrecoverability or reset an ability. NeedsTemplateMetadata observes concrete redundant-field absence/type/state contradiction; a legal metadata record with a throwing validator is not a repair trigger. An explicit unknown lifecycle version is preserved without downgrade.

Only a complete current typed saved ledger (knowledgeVersion1 plus actual building/district receipts) independently passing existing ValidateTemplates against trusted parent base.token/origin coordinates can supply proof. Strict parent must establish Industry history and preserve every existing base/reference/UNASSIGNED/remaining-owner check before publication. No current catalogue,building scan,City legacy property,age,elapsed time or retry count supplies history. Missing/invalid/old ambiguous/building-only ledgers do not produce a candidate.

For captured-only repair,set the redundant marker true and preserve valid lifecycle exactly,including pending and extensions. For demonstrably broken/missing lifecycle,copy its existing table extensions where present and rebuild only existing v1 initialized/pending/district-known metadata from the complete ledger; pending=true requires the original normal reconciliation. templates and its learned,districts,extensions and byte representation are untouched. No new saved schema or arbitrary repair API.

Restore evaluates a pure candidate even when old full validation already passes with missing capture metadata. Candidate owner plus complete remaining parent must pass before writing. Only approved changed metadata fields are taken from it; other still-isolated Known markers and payloads remain exact. Redundant Known and metadata repair merge into one revision/CAS/readback. Failed setter/readback or an unrepresentable next revision cannot publish recovery. Bounded diagnostics retain changed field,prior type and bounded prior state; local status is not a permanent backup. The old root remains native CAS authority.

No new event,timer,poll,consumer,native input or cache. Healthy complete metadata uses a constant scalar check and no extra read/write. A deficient record gets bounded saved-copy/pure validation work once at load. Store restore performs at most one merged repair CAS; subsequent original Standardization initialization may separately scan/reconcile and clear pending,which is not included in the one-CAS claim. No normal periodic recovery is added.

T04/T05/T08:14 focused Lua5.1 cases cover five metadata contradictions,capture nil/false/wrong types,extension and ledger preservation,current-catalog independence,coalesced Known+template repair with a bad Insights sibling,explicit future versions,missing/corrupt/building-only histories,no Industry/core proof,temporary validator failures,uncertain setters/readback,revision limit and repeat-load zero writes. Actual Store+Standardization+IndustryHistory full restart proves two distinct Store writes (metadata restore then normal reconcile),unchanged template history and E0. Two old no-repair assertions are executed unchanged against exact B349; current tests separately require the new D7 deterministic behavior. No historical assertions are edited.

Safe already-completed Claim cleanup is a separate pending proof slice. Remaining cumulative histories and unmatched native transactions still lack independent complete recovery authority; no guessed baseline,manual player repair or permanent-HELD completion claim. D5 native attribution remains OPEN. No deployment/main/game launch or native PASS.

Independent review reproduced a candidate-only reporting error: after candidate proof,a second validator call failed and only a sibling Known flag was applied,but the diagnostic kind still said template metadata rebuilt. Actual history/CAS stayed safe. The kind now depends on actual field application,with a dedicated transient-second-check regression. The prior739-PASS artifact remains local at local/refactor/S8b9-B350-final/closure.json; final evidence below comes from the corrected source and a new artifact path.

Proof vocabulary: COMPLETE_SAVED_LEDGER denotes the validated currently saved typed structure and its self-consistent receipts. It does not prove every historical event or catalogue entry was recorded. Existing PRESENT_AT_ADOPTION limited coverage remains unchanged; no formerly unseen building/district is invented by this metadata repair. Independent read-only review passed the original13 focused cases and supplied the added diagnostic counterexample; corrected14-case current validation and full740 regression pass.

### Machine validation evidence

- Stage/status: `S8b9` / `LOCAL_SIMULATION_PASS`; tests=740, passing=740, registered-open=0.
- Source: base `6471b6d1389a7a453685d2245edcc78801c20906`; dirty=True; input SHA256 `20bacb5245720c7fa669c4759366c82db7d7507b09b6974c2629947178fe0e2a`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b9 --output local/refactor/S8b9-B350-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b9-B350-final2/closure.json`; SHA256 `9e769702b85b6c11c45867b415d875f7f04dbb26fcef69146bced089aae0727f`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 175; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b9_template_metadata_proof": {"authoritative_saved_ledger": "typed building+district receipts", "history_rebuilt": false, "permanent_irrecoverability_claim": false, "restore_CAS": 1, "second_restore_CAS": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 377}
