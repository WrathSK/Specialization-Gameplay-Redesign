# B380.407 — S9e7 / R04 Academic Tradition owner-return correction

## Design trace: already resolved, not a new gameplay decision

Research_D0058 RES_L4_TRADITION mechanical_contract/lifecycle and Research.md99 require city-owned age,freezing unsupported-owner time and resuming after reliable requalification. The accepted historical D0040 Long_Term_State review explicitly closes the old OWNER_POLICY_UNRESOLVED issue for Tradition;its A-category table says identity age resumes without owner sub-ledgers. Shared A_CITY_HISTORICAL_LEGACY agrees. The Research Content field named closed identifies that resolved old issue;it is not an instruction to preserve the old absorbing code state. No authority conflict or new owner policy is invented here;Design and frozen history remain unchanged.

The actual deviation had two parts:ResearchTradition.Advance returned the old state forever for OWNER_POLICY_UNRESOLVED,and Store.recapture never rebased it at the proved return boundary. Existing confirmed loss correctly preserved age,while this stale implementation prevented all future normal age credit after recapture.

## Implementation and impact

A pure ResumeOwner transform validates the existing record,retains start/age/receipt/qualification/version,and rebases cursor to the confirmed current turn. Research identity resumes COUNTING;other identity stays PAUSED_IDENTITY. It never credits the held interval,even if a legacy held record still says COUNTING. The legacy enum remains readable for compatibility;an authoritative active old hold also rebases without backfill instead of remaining absorbing. Its diagnostic no longer calls resolved ownership policy undecided.

Only the existing confirmed Store return calls this transform,for a nonisolated Tradition group,inside the original registration/reference/CAS guards and same atomic record save. New owner admission and excluded conquest semantics are untouched:the tested path is the existing lawful original-owner return. Invalid return facts,callback failure and corrupt isolated Tradition cannot fabricate an origin or reset payload. No Property key,record schema,version,new persistent field or new allowed state.

After that successful committed save,Store emits its existing HISTORY/TRADITION fact. The existing declared consumer marks its bounded owner work and projects at the existing publication boundary,from committed age/current qualification. No precommit effect apply,new listener,timer,poll,blind recovery or irreversible replay. This adds a scalar record transform and existing fact mark only on actual return;the current owner Tradition consumer may visit its indexed Tradition cities,not the world. The return uses the same number of Store writes as before.

## Evidence

T01/T02/T03/T04/T05/T06/T08,L3. Fifteen new test methods (including the routing correction and frozen profiles) cover the actual Store+age+effect loss/foreign hold/return/cold reload,all legacy model states,no-backfill and next full interval,invalid native return,independent callback failure,isolated bad payload,postcommit observer failure and committed-before-consumer ordering. The B379 comparison retains age10 across20 foreign turns;old code stays10 forever and its effect stays withdrawn until another unrelated refresh,while corrected return keeps10,restores the10% carrier at publication,and reaches11 on the next full turn. Receipt/start/qualification remain the same;1000idle publications do not write history. Native effect/real save-file/CPU behavior remains U5.

The cold fixture initially restarted Store without reattaching its mandatory effect exit participant,so it correctly refused return with RETURN_WITHDRAWAL_UNCONFIRMED. The corrected cold test reattaches the real effect owner/native doubles and runs the original confirmed-exit boundary before return;the runtime guard was not relaxed. The prior absorbing-owner assertion remains unchanged on exact B379/7c47fa5 source in FrozenBefore and is registered as superseded by the already-accepted lifecycle. Other D6/model/store/ordered-return/D7/research-applied/writer-barrier tests remain current,with duplicate test IDs removed from this selection,not assertions weakened.

User decision:none (existing D0040/D0058 deviation). User testing:U5 loss/return/save and projection. Primary next:accepted remaining R05/Store/UI/S9/U4/S10. No deployment,main promotion or game launch.

## Additional L3 correction and selection provenance

An expanded1131-case exploratory run is retained locally as FAIL at local/refactor/S9e7-B380-final/closure.json. It exposed eight errors,none ignored:three current terminal-zero expectations relied on the now-corrected permanent owner hold;their initial stale-write rejection/no-create assertions remain exact,while the final fresh current read now asserts the lawful10%/5% value. All original zero expectations also execute against B379 through explicit historical profiles. Four older whole-record rejection expectations already had accepted frozen replacements in S8b4/S8b5/S8b7b;they were accidentally reintroduced by loading raw old classes alongside the inherited selection. Their unchanged frozen checks and current ability-isolation checks are selected explicitly here,not deleted or weakened.

The eighth error was a real B376 kernel regression independently reproduced on unmodified B379:ordinary nil/non-table scope used Lua and to produce false,then lifecycleTransfer validated false as a transfer. An explicit early non-table return restores original broad audits;explicit malformed transfer=false still fails before native work. Three new direct/current-Infrastructure checks prove the distinction,plus the original sibling repair test and all current R09b tests. The lower foreign-event counts measured with valid typed transfer scopes remain separate from this failed unscoped path;failed audits are not counted as performance improvements. No prior frozen report is rewritten.

This final selection is compact symbolic test/class references,not another expanded cumulative snapshot in Git. Full exploratory/reviewed artifacts remain local only. The final tested source and measurements below supersede that exploratory failure for these scoped fixes;U4 still must classify every current module/profile and is not claimed complete.

The164-case interim artifact also remains FAIL locally because raw old Groups classes reintroduced three later-superseded whole-record guards. Final selection uses the already maintained inherited load_tests profiles,which run each accepted current replacement plus exact frozen predecessor checks. It adds the new R04/R09 regression module and current R09b suite;no parallel thousand-line expansion is committed. The current S7c boundary assertion now distinguishes the explicitly resumed Tradition state from Commerce dormant-owner handling,which remains unchanged;its original Tradition zero/cursor/hold expectation is still executed against B379. U4 remains a separate every-module/profile requirement.

The final maintained inherited selection executes1144 unique test IDs with0 failures/errors/unexpected results. An ad-hoc loader count without the required external DB configuration produced failed-loader placeholders;it was not the actual configured run. Full U4 coverage remains separate.

### Machine validation evidence

- Stage/status: `S9e7` / `LOCAL_SIMULATION_PASS`; tests=1144, passing=1144, registered-open=0.
- Source: base `7c47fa51af97f57fe57f9b90b55a4b8b5c917877`; dirty=True; input SHA256 `726220cc78cb59924988c2e28e68fd57ad63d511810676edc38c2b6b1480cdd3`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9e7 --output local/refactor/S9e7-B380-current-closure/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9e7-B380-current-closure/closure.json`; SHA256 `c13734fcbbc568d325261781ea916ba8342f9a6c145cc05acd1b7d5b428917db`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 218; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Current-batch measurement: `{"S9e7_Tradition_confirmed_owner_return": {"after": {"next_age": 11, "return_writes": 1, "returned": {"age": 10, "cursor": 30, "effect": 10, "state": "COUNTING"}}, "baseline": "B379", "before": {"next_age": 10, "return_writes": 1, "returned": {"age": 10, "cursor": 10, "effect": 0, "state": "OWNER_POLICY_UNRESOLVED"}}, "foreign_interval": 20, "foreign_interval_age_credit": 0, "native_effect_CPU_save": "USER_GAME_TEST_REQUIRED"}}`. Inherited workload measurements remain in the identified local artifact and their original batch reports; they are not repeated here.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 407}
