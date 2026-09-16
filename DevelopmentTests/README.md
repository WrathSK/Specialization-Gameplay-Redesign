# Specialization tests

Document Owner: Codex

Run from repository root with Python 3 and Lupa exposing `lupa.lua55.LuaRuntime`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_b051_all_districts.py
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_deployment.py
```

The first entry wraps `test_b051_background_fix.py` and `test_b051_copy_yields.py` in memory to retain their behavior assertions while selecting version 67. Do not run those older wrappers alone against version 67. Source is `Mod/`; the seven byte-comparison baselines are repository-contained `Fixtures/B051-before-copy/`, with provenance/hash. No DevelopmentBackups dependency remains in this current entry.

Provide the external Civ VI/HD-generated database through `SPC_DEBUG_GAMEPLAY_DB` or ignored `local/config.json` (see root template). It is opened mode=ro and backed up into memory; never edited or copied into this repository. SQL integration checks require this external database; Lua-only model tests and deployment tests do not. Install Lupa into a local environment as needed; no game assets or Python environment is vendored. `requirements-test.txt` records the expected distribution (2.8 from the existing installation directory); existing package metadata is incomplete, so fresh installation is not claimed validated. The tested backend is lua55.

## Historical tests and models

Other retained Python scripts are historical, version-specific regression evidence unless listed in the migration validation report. Their original paths/assertions are preserved; some require external historical snapshots and old manifests and are not portable current entry points. Do not batch-run and rewrite them until green. Their presence is not a promise that all historical suites pass against B051.67. Offline Lua models describe preparation, not implemented gameplay. `test_gpp.py`, `test_discovery.py`, `collect_gpp_log.py` belong to CityGPPProbe and are deliberately excluded.

Results mean LOCAL_SIMULATION_PASS (local simulation), never USER_GAME_TEST_PASS. No game launch or GUI automation. Use no-bytecode mode. Deployment tests operate only in temporary directories and never touch the game runtime.

## Historical Architecture v2 Batch B (B071.98, develop only)

`PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_arch_v2_batch_b.py`

Requires Lupa lua55; this runner preserves A/B069 assertions with an in-memory manifest-stamp adaptation, runs actual Discount/Bridge/Counters, and compares 168 full output cases against both Git baselines (79281ff, d1ac666). Keep that history available; no network/game access or deployment. Covers cold/warm derives, unknown/withdrawal, reentry, mutation and player/epoch isolation. Standalone A test retains its historical modinfo97 assertion; use this B entry for current develop.

## Historical B072.99 instrumentation (develop, no deployment)

Run `python3 DevelopmentTests/test_runtime_audit.py` and `python3 DevelopmentTests/test_runtime_audit_regression.py` with the same no-bytecode/Lupa environment. File tests use TemporaryDirectory only. Regression wraps B/A/B069 version assertions for99 without changing historical tests. Covers1M increments,10k turns,8×4MiB ring, capability/failure gates, duplicate turns and real Network output/counter ON/OFF equivalence. Does not verify Civ VI exposes standard Lua io/os; native gate remains required before a long-play logging claim.

## Architecture v2 C2 — B075.102 (historical entry)

`test_arch_v2_c2.py`: actual Copy/Industry UI+Gameplay transport, pending10k, duplicate/stale/reference/load, bounded timeout/throwing transport, temporary hold/confirmed retirement; 63 B074 carrier-map comparisons including Industry Lv3; Copy precision unchanged. Includes D1/C1/A/B/B069 regression with in-memory build stamp adjustment only. Lupa lua55; no DB/game/deployment. Example local dependency: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_arch_v2_c2.py`.

## Architecture v2 D1 — B074.101 (historical entry)

`test_arch_v2_d1.py`: Lupa lua55, actual Discount/Network/Standardization modules with mock native events. 10k generic pulses, 1/2/4/8 city scaling, 39 B073 output cases, C1 lifecycle and A/B/B069 network regression. C1 fixture explicit fact mutations are marked dirty for D1; historical B consumer count assertions run with the historical consumer. Historical test files remain unchanged. No deployment/DB, no memory-causation claim. See Architecture/v2/Batch_D1_Discount_Propagation.md for counter meanings and local interpreter command.

## Architecture v2 C1 — B073.100 (historical entry)

`PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_arch_v2_c1.py`

Requires Lupa lua55. Actual Discount UI/Gameplay mocked transport/native permissions,200k pending notifications,bounded retry/epoch/withdrawal and12 normal B071 comparisons. Runs A/B/B069 and runtime-audit equivalence via in-memory stamp-only adaptation to100; preserves historical tests. No DB/game/deployment. The local installed Lupa2.8 currently resides outside the repository; use an interpreter compatible with that installation. C1 does not optimize generic Audit/C² scans.

## Current Architecture v2 D2 — B076.103

Run `PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_arch_v2_d2.py` with Lupa lua55 (local validated environment: `PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14`). Actual current Lua, 1728 B075 carrier maps, nonzero Commerce source changes, Great Work scenarios,10k idle/UI stress,1/2/4/8 scaling,30k published-view queries. Includes C2/C1/D1/A/B/B069; in-memory historical build/scheduling adaptations are explicit, frozen test files unchanged. Git baseline5dc6221 and older regression commits must remain available locally. No DB/game/network/deployment needed. LOCAL_SIMULATION_PASS only. See Architecture/v2/Batch_D2_Runtime_Propagation.md.
