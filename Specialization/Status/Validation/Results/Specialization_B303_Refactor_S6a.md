# B303.330 — S6a D business/report cache separation

Source base: evidence-management commit `d483eee`; runtime change only DistrictCompleteness plus build stamp. Evidence is LOCAL_SIMULATION / STATIC_CONFIRMED, never native PASS. W0004 L3 for shared fact consistency; choose T02/T03/T04/T05/T07/T08 and the actual affected consumer combinations rather than all historical tests.

## Runtime Impact Contract

- Path/owner: DistrictCompleteness remains the sole read-only native D owner; Calculate ontology and per-building fields remain unchanged. A lazy compact cache holds at most2048 city references, independently of the original8-entry raw/detail LRU. `CacheSize()` retains the original report meaning; business capacity has its own scalar accessor. No city enumeration or prewarming is added.
- Cause/scope: original verified native D hooks and consumer routing remain. Exact/owner/global invalidation touches compact entries even after raw eviction. Synchronous uncached overflow uses bounded8 in-flight reference/tickets; foreign known input remains zero local work. Overflow reads stay legal and uncached, without evicting existing business entries.
- Read/write: full reference, dirty ticket, cache identity, load epoch and write-generation certify captures. Same-reference reentrant reads are unavailable, never old READY. Raw/detail bind to successful sample serial, not merely equal D-value revision. A detail miss may explicitly reacquire only that city; failure preserves prior compact but reports unavailable, without fabricating detail or repeated idle attempts. Errors with broken tostring remain bounded/unavailable.
- Work/recovery: normal warm compact hit has no cache census or native capture; report eviction scans at most9 entries. Owner/global dirty and confirmed-location return cleanup are bounded by2048 detached entries. Confirmed removal/load release cache state; Store return matches original owner/location, without new exit receipts. New related evidence/required next-turn explicit read retain recovery; no timer/frame/poll/GC strategy change.
- Compatibility/exceptions: no persisted shape, qualification, money or irreversible operation changed; detailed report/body changes are presentation of the same validated sample. Full catalogue presence safety checks remain; not a claim of catalogue-independent work or measured native heap/CPU improvement. Larger bounded compact retention trades memory for avoiding systematic recapture. Necessary synchronous NewTargets transfers remain per S0752.
- Proof: frozen T03 assertion unchanged; B272/B302 before data retained in published history.15 independent cases cover2047/2048/2049,32-city report rotation, missing raw failure, equal-D new diagnostic sample, exact/owner/global scope, overflow dirty, load/ref replacement, native write barrier, removal/return, same-city reentry, unprintable error and idle. Impact selection includes real Apply/Chair/Infrastructure/Support/Housing/GPP/Industry/Commerce/CultureNetwork/Standardization and pending network rules. No weakening or broad historical rerun.

## Result and remaining boundary

The machine section below records the final selected run and changed measurements. Full artifact and transcripts stay ignored/local; important prior failure evidence remains retrievable from Git history. Local artifact/hash is not a permanent backup. No new user-game/deployment claim.

- User decision: none; cache mechanism is within accepted S6/D8/D15 scope.
- User testing: U5 integrated native yields/hidden-context/memory smoke; no new blocking native fact found.
- Primary next: continue S6 anchor/worker/shared snapshots/reverse dependencies/hot paths, then S7–S10.

### Machine validation evidence

- Stage/status: `S6a` / `LOCAL_SIMULATION_PASS`; tests=176, passing=176, registered-open=0.
- Source: base `d483eee6549146f95164daae9104b9c9319156ed`; dirty=True; input SHA256 `7783495ae92940711f17f1f07961ba0bc81d259b101b0d53060f633f0b2843ef`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6a --output local/refactor/S6a-B303/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "589ba3db7f4b927ab1ff478a9ccbb60ebadfb6fc9fb1cbfabf332955644054f2"}}`.
- Full artifact: `local/refactor/S6a-B303/closure.json`; SHA256 `83b447bb4d9e90e6aa4c96fa3ed216b16e1a85576733d3e180ff04685274db67`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 62; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6a_32_report_rotation": {"detail_capacity": 8, "later_business_recaptures": 0, "report_recaptures": 32}, "S6a_business_capacity": [{"business": 2047, "cities": 2047, "reports": 8, "warm_captures": 0}, {"business": 2048, "cities": 2048, "reports": 8, "warm_captures": 0}, {"business": 2048, "cities": 2049, "reports": 8, "warm_captures": 1}], "T03_warm_capacity": [{"captures": 0, "checks": 0, "cities": 8}, {"captures": 0, "checks": 0, "cities": 9}, {"captures": 0, "checks": 0, "cities": 16}, {"captures": 0, "checks": 0, "cities": 32}]}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 195, "XML": 25, "package_files": 317, "modinfo": 330}
