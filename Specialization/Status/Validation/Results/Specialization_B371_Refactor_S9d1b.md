# B371.398 — S9d1b Tradition lifecycle write barrier / safe checkpoint

## Plan and Runtime Impact Contract

Accepted P01–P10/D15 and existing confirmed-owner-loss withdrawal; base B370.397/190eba8. Scoped plan recorded before edits. This is the technical repair of the demonstrated old Remove905→confirmed city loss→later Create910 window,not a city-owner gameplay policy. Only Research Tradition enables the new write guard. User requested the next reliable stopping point during this batch;finish validation/commit/push,then stop without starting another slice.

Store.CarrierReferenceStamp is pure:existing scalar position/worker routing,collection/worker ready/fault/writing/committing,ACTIVE,removed/completion hold,exact current owner/id/xy/token,ownerChanges,restructuring serial/phase and identity. It adds no Property/native read,save field,cache or general profession permission. Each ability retains its own qualification. Store.Base keeps its first value unchanged and supplies an optional synchronous second witness from that same committed record,so native governor/history reads occurring later cannot silently move the witness to a newer lifetime.

EffectiveFacts privately captures that scalar alongside the existing base and carries it in the same bounded phase slot. Invalidation/write/reference/cache lifetime remains identical;no second facts sample or new cache. Explicit ReadWithCarrierReference returns facts+witness. Default Read still returns one identical facts value;Inspect/custom multiple returns preserve arity and nils. No new field leaks into facts or save/DTOs. Existing production Base consumers consume the first value or tail-forward both through SupportFacts;they do not interpret a third pcall value as an error.

Tradition creates an independent request-local reference guard from that same-read witness. Each actual write verifies current Store/EF/effect service and relevant methods/native helper functions plus the same reference/lifecycle stamp. It is independent of the2048-slot presentation cache;missing presentation never denies legal effect work. Modern authority with missing witness fails closed through the existing Update error path,without plain-Read fallback. Explicit isolated legacy adapters keep their original contract. The guard restores before business busy releases,including failure/reentry.

NativeHealth accepts one optional pure beforeWrite. Only the Tradition caller supplies it. After all original location/witness/buildings-or-queue getters,the helper invokes the guard immediately before the captured original P.Remove/Create function. Original function lookup→getter→native argument order and counts remain;the guard sits in the existing pcall/finally so removing/creating suppression witnesses always release. Other NativeHealth consumers keep the original path. Stop only old subsequent calls;do not replay,scan,compensate or add timers. One already-entered native operation cannot be canceled by this boundary.

Normal behavior/native work is preserved:0 additional native getters,fact/carrier samples,unit/city scans or save writes. Added Lua work is a fixed lifecycle string per base sample/phase slot and pure scalar comparisons per actual Tradition write. No business working-set cache or automatic consumer loop is added. ownerChanges rejects loss→return even with identical owner/id/xy/token. General history revisions are excluded so unrelated history changes do not invalidate the reference.

T02/T04/T05/T08,L3.12 new tests plus104 focused affected checks pass:default Read/Inspect arity and complete values,fresh/cached witness with one phase capture,1000 pure queries with native forbidden,commit barrier/unrelated revision,loss-return inside GovernorGate before facts return,history-getter lifetime change,Remove→loss→Create,location/witness-owner/final buildings/final queue getter loss,source/method/native function replacement and missing witness. Existing Tradition native-work/history differential remains exact. Shared EF/worker/anchor regressions and original NativeHealth/Tradition behaviors remain inherited in the selected cumulative run.

Previous S9d1 fault injection now targets the explicit production reader via inputReader;all prior behavioral assertions stay unchanged. Dummy publication-capacity testing explicitly supplies its isolated witness/stamp protocol rather than granting modern fallback. An initial new test called a nonexistent fixture Same helper;replaced it with the existing deterministic full-facts encoding equality. Independent read-only review ran12 new cases and38 prior Tradition cases,confirmed default arity/cache/final native boundary,found no blocker and wrote no files. The first cumulative run passed1116/1117;the frozen pre-D6 fixture mixed its old Store with the current strict writer. Its history closure now also pins ResearchTraditionEffects to the same exact historical commit,with all original assertions retained.17 frozen/current focused checks passed after this harness correction;the final cumulative run is separate and the earlier artifact remains local.

### Scope and restart point

The B370 demonstrated later-write window is closed for Tradition;other effect writers are not implicitly migrated. A native call already entered before ownership changes remains a separate engine/atomicity boundary:keep unknown evidence if observed,never invent a compensation/replay loop. No UI DTO or additional owner publisher is started in this batch.

Safe-stop handoff:resume approved S9 other owner applied provenance,then institution DTO/display,shared adjacency and S10 responsibility migration/deletion safety. Read current Authority/Status/P0-H;do not restart S0 or repeat completed training migration. Existing source records need scrutiny:Commerce reputation.effective is prepared candidate,Standardization applied map can be partial,Dialogue/Insights need explicit Store token/zero/unknown publication. Exact D7 permanent-history/money and D5 native-attribution limits remain OPEN.

Full artifacts are local/ignored,not permanent backups. No deployment/main promotion/game launch/native PASS. User decision:none. User testing:final U5 unless a specific blocking native fact appears. Primary next:wait for user continuation at this verified checkpoint.

### Machine validation evidence

- Stage/status: `S9d1b` / `LOCAL_SIMULATION_PASS`; tests=1117, passing=1117, registered-open=0.
- Source: base `190eba87d269cb1f1cb1be90587d6b360a375e8f`; dirty=True; input SHA256 `0917ecb78f43f01791edff72658ecb216c1c1ad195626fcbd34c3b5ce26287b4`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9d1b --output local/refactor/S9d1b-B371-reviewed/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9d1b-B371-reviewed/closure.json`; SHA256 `f95d66f4e8030838f5152481c752dfe86f1b6d5b0ad9eda6b7b21634a6fadd1d`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 212; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9d1b_reference_witness": {"fact_or_Property_reads": 0, "native_reads": 0, "new_cache": false, "queries": 1000, "saved_schema_changed": false, "shared_phase_lifetime": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 398}
