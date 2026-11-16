# B335.362 — S8c2 bounded held cleanup on existing local turn boundaries

## Plan and Runtime Impact Contract

Accepted S8/F08/C009 expressly includes a HELD_TRANSFER turn retry; base B334.361/07aa64c. This slice uses only the existing Store PlayerTurnActivated registration and its existing registered-worker loop. No new timer, publish retry, city/world enumeration, project poll or all-event hook is introduced. LoadScreenClose keeps its original age path and existing reconcile cleanup; it does not enter the new automatic retry.

Three bounded session values per worker track the current S8c1 loss generation, total automatic attempts (maximum3), and latest reliable site-check turn. They are not saved or permanent recovery evidence. Every existing ExitConfirmed stamps a reliable current turn before its site lookup, with busy already held and generation rechecked after the protected clock getter. Thus the initial ownership cleanup and cold-load cleanup suppress additional automatic work on the same turn. Unreadable clocks do not block the existing cleanup; if no reliable clock exists yet, the next reliable activation only establishes a baseline. A newer reliable local activation, original test-player owner, HELD_TRANSFER, available Store/worker barriers, and at least one unfinished exit below the existing callback budget are all required. The automatic turn/count permits are consumed before entering cleanup and never refunded on false, UNKNOWN, getter or callback failure.

The existing total3 attempts per registered callback remains separate and unchanged. The additional maximum3 automatic site attempts bounds unavailable-site cases that otherwise would never consume a callback attempt. Both are per load/current loss, not a persisted lifetime limit. Exhaustion neither confirms UNKNOWN nor changes history: existing related native events/explicit cleanup can still act under their original rules, and a later genuine S8c1 cleanup ACK can complete the current loss. Ordinary record revision and repeated activation never reset permits. A genuinely new loss changes the private generation and starts its own bounded work. Completed siblings never rerun.

Native work: a protected GetLocalPlayer is sampled lazily at most once in an activation that actually has an eligible registered held worker; no local-player call for healthy/completed/budget-exhausted workers. GetCurrentGameTurn is read protected at an existing exit pass, then the exact S8c1 generation/barriers are checked again. Only the existing exact-site and per-owner cleanup/native readback may follow. There are no new positive effect, money, reservation, saved key/schema or irreversible operations. Qualification and ownership gameplay remain unchanged. The three session scalars have the same per-worker lifetime as existing attempt/ticket state; no global unbounded cache or history is added.

T04/T05/T06/T08 use actual Store/RuntimeWork: same-turn/duplicate suppression, newer-turn recovery, three-site UNKNOWN cap, original callback budget/sibling preservation, no idle publication work, cold-load suppression, absent/nonlocal/throwing local-player getter with ordinary age continuing, revision/generation boundaries, reentrant site/clock/local getters and write barriers, two independent held cities, and genuine async ACK after automatic exhaustion. Existing S8c1 composition and scoped Store/consumer regressions remain. Test/static evidence is local only; U5/native transfer/save-load remain USER_GAME_TEST_REQUIRED. D5 unique Crew-completion proof and full D7 isolation remain OPEN. No deployment, main promotion or game launch.

### Machine validation evidence

- Stage/status: `S8c2` / `LOCAL_SIMULATION_PASS`; tests=465, passing=465, registered-open=0.
- Source: base `07aa64cad150a3f84a3f025dc8ee836095393799`; dirty=True; input SHA256 `f439f89e6ecf782ddf579c3dbb0389df7174091aab0d59f9c86bad682f9b3da9`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8c2 --output local/refactor/S8c2-B335-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8c2-B335-final/closure.json`; SHA256 `2eebedea1571d95052cc3d80f7ef30f57cd2e24ba20f535aba37e5ffa70ba7d0`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 129; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8c2_bounded_held_turn": {"additional_saved_writes": 0, "automatic_site_budget": 3, "new_timer_or_listener": false, "next_turn_permits": 1, "original_callback_budget": 3, "same_turn_extra_cleanup": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 207, "XML": 25, "package_files": 329, "modinfo": 362}
