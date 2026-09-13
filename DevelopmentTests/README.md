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
