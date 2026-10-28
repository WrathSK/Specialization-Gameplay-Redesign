# B392.419 — restricted Lua object identity compatibility

2026-10-27. User reports B391 cannot establish specialization after district completion and authorizes investigation, implementation and automatic safe develop deployment. No main promotion, game launch or gameplay change.

## Evidence and scoped plan

The B391 collector session 20261028T040221Z records14 INSTITUTION_UI_FAILURE rows at CityPotential97/169 (raw equality calls),14 unavailable presentation reads and6 development failures across cities. It does not preserve the full exception text. Removing rawequal in the actual Store/EffectiveFacts local fixture reproduces both failures at CityProgressionStore246. Missing native rawequal is a strong cause candidate, not yet a directly sampled native capability fact; the game had exited before investigation. Keep USER_GAME_TEST_REQUIRED for resolution.

Runtime Impact Contract: replace only eight modules' raw object-identity comparisons with one pure helper using Lua table-key identity for table/userdata values and ordinary scalar equality. No global polyfill, registry, retained objects, native getters, listeners, retries, scans, gameplay or save changes. One short-lived one-key table per object comparison; no cross-call cache. Preserve rejection of distinct objects with equal __eq results. Existing guarded calls remain guarded. Local restricted-profile and unchanged actual consumer tests cover Store/Facts, training, selected-view observer, action/target/presentation requests and Tradition. Package references/compilation and deployment rollback gates remain required. No widened diagnostics or B271 probe enablement.

User decision: 2026-10-27 resumes development deployment authorization; verified completed develop batches may deploy after automatic game-exit and transaction checks, without another approval. Running/unknown game state blocks deployment; never terminate or launch the game. Main promotion remains separate.

User testing: new-current-build campaign, district completion→specialization, then investment and institution display; local simulation does not certify native recovery.

Primary next: run scoped validation, commit/push develop, verify game exit and deploy using existing receipt-bound restore→activate path. Preserve B391 outgoing and stable recovery packages. Continue original refactor only after this repair batch boundary.

## Local validation

LOCAL_SIMULATION_PASS:237 cases (six restricted-profile tests plus231 unchanged scoped regressions),Lua5.1/Lupa2.8. Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<local-lupa>:DevelopmentTests python3 DevelopmentTests/test_b392_identity.py`. Existing temporary deployment authorization/hash/rollback/restore regression also passes. The real pure dependency is explicitly loaded by the shared test harness because frozen UI fixtures stub include;old assertions and historical differential sources are unchanged. No claim of direct native capability observation or successful user-game recovery.

Full local outputs: `local/refactor/B392-identity/`;local-only regenerable artifacts,not permanent backup.

STATIC_CONFIRMED:218 Lua5.1 files compile,25 XML files parse,340 modinfo file references exactly cover341 runtime files including the manifest;version419. Context check passes341 runtime/1274 guarded files. No other Mod or game configuration changed.
- local/refactor/B392-identity/deployment-tests.txt: SHA256 `262460364984bf1f6fc3c12d40857ab110c75e34b3de050db5aa83ba6d1d2e03`.
- local/refactor/B392-identity/tests.txt: SHA256 `7946dbe53f3fd833ac9798f182f1ec816cf0ebbddcb38f44873fd33ca7ff4b5c`.

## Deployment — 2026-10-27

Automatic OS process checks before both swaps confirmed the game exited. Existing temporary_playtest restore→activate transactions completed,with no game launch. Source `3d8468c6ed5a5d248586912f3d160ad58a32a254` is committed and pushed develop. Live341/341files match;digest `339857a4d73773acd4858b5e996cc7686a3e74d1cf152559c0b97ed1195a75ed`. Receipt `B392.419-3d8468c-playtest.json` is in the external deployment archive;phase DEVELOP_ACTIVE,no pending marker. B391 outgoing backup and B307 stable backup both match their prior exact digests. Main remains unchanged;no PR/promotion. Runtime source is unchanged by this final documentation commit.

User decision:none pending;standing safe develop deployment authorization recorded. User testing:new-current-build district→specialization→investment→institutions;native recovery not yet PASS. Primary next:collect this bounded recovery result;original S9/S10 scope remains incomplete.
