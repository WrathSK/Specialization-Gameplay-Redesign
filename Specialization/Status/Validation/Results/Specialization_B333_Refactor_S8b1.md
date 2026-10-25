# B333.360 — S8b1 deterministic redundant-flag reconstruction

## Plan and Runtime Impact Contract

User resumed on2026-10-25. Accepted S8/D7/D15, base B332.359/801a85a. Reconstruct only Dialogue/Engineering/Commerce/Capital/Development *Known metadata from complete valid preserved payloads. These flags are redundant: current production writers persist only true together with their payload; no false producer exists. This is deterministic reconstruction, not a permanent-corruption verdict, an empty-history reset or a gameplay exception. Full opaque isolation and other recovery remain subsequent S8 slices.

Fixed criteria before implementation: (1) initial storage read/bounded copy succeeds; (2) original strict validation fails at one of the exact five known/history availability guards; (3) preserved non-nil payloads independently validate after setting the corresponding flag true; (4) the entire unchanged parent validator, including base/schema/reference/receipts and every other ability, accepts the candidate; (5) revision increments representably once; (6) existing native prewrite equality and exact postwrite readback confirm one write. All qualifying metadata mismatches merge into one city-record write. Any missing payload, unsupported schema, other malformed field, temporary dependency/getter/copy failure, changed native prewrite or unconfirmed setter/readback yields no successful repair. No inference from elapsed time, retry count, current treasury, catalogue or project count.

The registry's candidate planner is pure, bounded to five fixed entries and not itself authority. Store restore invokes it only after the failed strict guard, before readiness/publication. The existing save path still performs full validation before exposing a candidate and the same CAS/readback under its fact-write barrier. A successful load repair records only a bounded copied session summary (field names, former types, new revision). No new saved field/schema/key, owner callback, amount, effect, timer, automatic consumer, native gameplay read or irreversible operation. Existing payload bytes, DECIMAL17 strings, serials, requests, pending stages, age, totals and receipts remain identical. An already valid subsequent load writes nothing. Current readiness order and supported-new-campaign boundary remain.

Targeted failure injection exposed an existing error-formatting hazard in this newly used restore write path: tostring of an unprintable native error could escape before EndWrite. Store now safely formats only these existing restore/write failure summaries; ordinary string errors are unchanged and the existing write barrier always reaches its release before the failed outcome is raised. Readiness remains false and no recovered summary is published after an uncertain write. This changes no success, money, receipt or retry policy.

T04/T05/T06/T08 and L3 Store consumer regressions: each of five flags missing/false; all five in one revision/write; healthy loads zero writes; unchanged complete histories; native setter drop/before/after errors and stale/throwing readbacks; native getter/copy failure and changed prewrite; no repeated work across1000 idle publishes; confirmed fresh-load recovery; guarded APIs during native setter; unrelated city remains usable; unprintable model/setter errors; original fact barrier release. Valid Capital DEBIT_CALLING/CREDIT_CALLING and Development DEBIT_CALLING payloads retain their exact requests and values, with zero treasury operations and no settlement callbacks. Original S8a corruption assertions remain frozen on exact801a85a; only their known-flag-only cases are superseded by accepted deterministic rebuilding, not weakened. Other strict base and ability predicates remain.

## Remaining D7 evidence boundaries

| Record | Reliable reconstruction presently available | Boundary retained for subsequent isolation/recovery |
|---|---|---|
| Templates/lifecycle | Complete valid stored learned history can prove initialized metadata. | Current buildings do not reconstruct demolished historical templates. No unproved uninitialized reset. |
| Research tradition | Preserved genuine P4 receipt/start/qualification can support a lawful rebuild. | Current turn or an arbitrary one of three investment keys cannot establish the original P4 time/receipt or lost age. |
| Dialogue / Engineering | Complete independently valid completion receipts can prove derived total/L and known metadata. | Current works/E/national counters cannot invent historical quotas, serials or uncertain pending completions. |
| Commerce | Valid preserved selections must remain independent of an unknown reputation under D6. | Unknown reputation supplies zero reputation bonus, not a reason to erase other confirmed lawful Gold. |
| Capital / Development | Complete valid encoded contract payloads prove redundant known metadata. | Current balance/buildings cannot establish lost debit/credit/request evidence. CALLING/HELD is never reset or replayed here. |
| Expedition Insights | Complete validated archive receipts are authority. | Current/last Spy state is not a complete replica of dissolved units' archive history. No Expedition feature repair. |
| Claim timer | Valid timer and strict completed identity/claim proof remain separate. | Empty queue/time alone cannot erase an uncertain native completion. |

These are precise engineering boundaries, not player repair instructions or a permanent-HELD final policy. D7 is not declared complete: subsequent work must isolate only affected abilities, rebuild from reliable evidence, and use a lawful full initial record only after the accepted irrecoverability/no-other-evidence criteria can actually be proved. Base/envelope unreadability remains strictly protected. No broad restore, payload reset or invented history is authorized by this narrow slice.

Compatibility: same existing record/property shapes, exact money and no-replay policies, history and native ownership semantics. Full artifacts remain ignored/local with compact Git evidence and are not permanent backups. Native save/load and game effects remain U5; no new USER_GAME_TEST_PASS. D5's native completion-attribution gap remains OPEN. No deployment, main promotion or game launch.

## Reviewed historical expectation

The first broad run passed395 properties and raised one unchanged historical Dialogue expectation: test_dialogue_projects.test_corrupt_history_is_held_not_reinitialized also treats an absent dialogueKnown marker with an otherwise complete valid ACTIVE round as unrecoverable. U1 D7 explicitly supersedes only that redundant-metadata case. Its complete four-mutation assertions remain executed on exact801a85a; current actual Dialogue tests separately preserve ACTIVE/CALLING payloads with zero native finishes and still hold missing payload, bad total and wrong pending reference. No assertion or native guard is weakened. First execution remains FAIL, preserved locally as local/refactor/S8b1-B333-first/closure.json (SHA256 0b5be45024bfee468a48910c80a411f8e457cff4957ea63bf5059973e62cef94); final evidence uses a separate artifact. This local file/hash is not a permanent backup.

### Machine validation evidence

- Stage/status: `S8b1` / `LOCAL_SIMULATION_PASS`; tests=398, passing=398, registered-open=0.
- Source: base `801a85a1775453bdb6a831de5279bb562c6990de`; dirty=True; input SHA256 `3c9ec2731c0b211401dd9c70708e9b3863bd6bde14a19131528e761a072b393b`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b1 --output local/refactor/S8b1-B333-reviewed/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b1-B333-reviewed/closure.json`; SHA256 `0835c31646f54937293ccc4b3531c64d359094e455f29c2a442218e11e9b3580`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 108; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b1_CALLING_preservation": {"Capital": ["DEBIT_CALLING", "CREDIT_CALLING"], "Development": ["DEBIT_CALLING"], "same_payloads": true, "settlement_replay": false, "treasury_operations": 0}, "S8b1_frozen_before": {"source": "801a85a1775453bdb6a831de5279bb562c6990de", "superseded": "redundant known flags with fully valid preserved payload only", "unchanged_assertions": "S8a strict corrupt-ability differential"}, "S8b1_known_flag_reconstruction": {"flags": 5, "mismatches": ["missing", "false"], "payload_changes": 0, "writes_each_first_load": 1, "writes_each_second_load": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 207, "XML": 25, "package_files": 329, "modinfo": 360}
