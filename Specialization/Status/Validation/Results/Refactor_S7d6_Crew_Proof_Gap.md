# S7d6 — Crew completion proof assessment (D5 remains OPEN)

## Scope and outcome

User-authorized S7d/D5 investigation on B329.356/c55b484. Read-only production-code assessment; this checkpoint adds tests and records only. No runtime, gameplay, receipt format, deployment or main change. S7d4 and S7d5 remain independently validated; D5 multi-city formation is **not complete**. A passing characterization test means the stated deficit or conditional ambiguity was reproduced, not that the desired behavior works.

## Confirmed current defect

Two actual industrial-city admissions of the same native Crew project, both queues completed and one observed player count already2 before either callback: current CrewProjects rejects each with CREW_COMPLETION_SEQUENCE_AMBIGUOUS and creates0 units instead of2. Exact current Store/Crew controllers run under the Lua51 native-shaped fixture. This is a LOCAL_COUNTEREXAMPLE_CONFIRMED; whether this exact native cache/event timing occurs is USER_GAME_TEST_REQUIRED. It is not a replay of a real game log.

## Conditional information gap

After a prior completed A order, admit new A and B orders at player count1. Consider (1) A completes/B cancels and a new A completion arrives, versus (2) A cancels/B completes and a late duplicate of old A arrives. Both may expose player count2, zero A/B queue entries and progress, identical saved orders/receipts/living units and the same (player,city,project) event tuple before processing. Current code grants A in both, whereas the second history would require no A grant. Tests construct equal available inputs; they do not prove the engine permits the second delivery history.

Therefore a request serial/source plus the aggregate counter difference and post-state alone cannot establish uniqueness under that delayed-event assumption. Do not merely change ==prior+1 to >prior or loop over the difference, infer origin from one unbound unit, use elapsed time to rule out duplicates, or reconstruct CALLING without new evidence. Existing strict behavior is retained while evidence is missing. No broader rule about native event duplication is invented.

## Local primary-source inspection

Source roots are textual locators, not published copies of game files. CIV6_ASSETS denotes the installed application Contents/Assets; CIV6_MACOS denotes Contents/MacOS; HD denotes Workshop289070/2465378070. Read-only inspection, no native invocation/game launch/configuration change:

- CIV6_ASSETS/Base/Assets/UI/PartialScreens/WorldRankings.lua1236 and adjacent uses call player:GetStats():GetNumProjectsAdvanced(projectIndex), matching our current player-wide UI reader. Current Mod/UI/CrewProjectUI.lua26–35 confirms the actual wrapper.
- CIV6_ASSETS/DLC/Expansion2/UI/Loaders/TutorialLoader_Expansion2.lua211 uses Events.CityProjectCompleted(playerID,cityID,projectID); HD/Gameplay/Commemorations.lua598/640 and HD/Gameplay/Projects.lua7–16 use the same three fields. These examples do not establish the full emitted argument list, native delivery order or duplicate semantics.
- CIV6_ASSETS/Base/Assets/UI/Panels/ProductionPanel.lua2698 consumes GetAt(index) for queue rendering; inspected uses do not establish a stable completion-instance ID.
- CIV6_MACOS/GameCore_XP2.dll exports inspected strings GetProjectProgress, GetProjectCost and GetNumProjectsAdvanced. The bundled Windows Expansion2 GameCore_XP2_FinalRelease.map5304/20706 and Lua binding49732 identify GetNumProjectsAdvanced under Player::Stats. Symbols are corroboration, not proof of a callable Mac signature or of the absence of other APIs. No suitable per-city completion ordinal was verified; API absence is not claimed.

## Minimum native evidence and continuation

Before the dependent D5 implementation/cutover, verify a completion-specific witness or a sufficiently strong native event-delivery contract. Minimal user-run investigation should capture two industrial cities completing one same-tier order each, raw callback argument count/scalars, local queue observations and player counts at actual delivery; also cancellation/reselection around completion and repeated/late delivery protection. It should inspect whether a stable native queue/completion instance ID or a per-city monotonic completed count is exposed in Gameplay/UI, distinguishing symbol presence from actual invocation. No periodic probe or automatic action retry is proposed. The existing2–3-turn final smoke alone cannot prove arbitrary late-event impossibility; unresolved semantics must remain explicit.

This is a concrete engine/interface proof dependency, not a request to restart the refactor or change D5. Independent S7e retirement and S7f city-reference extraction do not depend on the missing proof and may continue. D5 must remain in the existing intake and final unresolved/U5 gate; it cannot be silently marked complete. Any necessary temporary native diagnostic/deployment follows the existing separate approval boundary. No source tree is promoted/deployed to investigate it automatically.

- User decision: no gameplay waiver requested; preserve the accepted D5 proof rule.
- User testing: targeted native proof above is required before dependent D5 cutover; no new native PASS.
- Primary next: continue independent S7e/f, retaining this open D5 dependency in the existing schedule.

### Machine validation evidence

- Stage/status: `S7d6Proof` / `LOCAL_SIMULATION_PASS`; tests=2, passing=2, registered-open=0.
- Source: base `c55b48406d1c504d5174e6ba27d950f3e9b4fc36`; dirty=True; input SHA256 `13e47b535aaa76b6d649fe2cdaa3fcac1c43e3de66f0d66a9a4b4c35f8fc29bc`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7d6Proof --output local/refactor/S7d6-proof-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7d6-proof-first/closure.json`; SHA256 `167308f6c2df8af29d3eb914464a5edea157a48e6bb0c04c17f6de55e3fbc68c`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 25; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (selected run): `{"S7d6_D5_OPEN_conditional_ambiguity": {"actual_new_A_grants_in_both": 1, "native_late_event_possibility": "UNKNOWN", "no_live_game_or_native_callback_injected": true, "required_A_grants": [1, 0], "same_observed_facts": true, "status": "CURRENT_SURFACE_INSUFFICIENT_IF_LATE_EVENT_IS_POSSIBLE"}, "S7d6_D5_OPEN_two_cities": {"actual_grants": 0, "desired_grants": 2, "engine_timing": "UNKNOWN", "native_pass": false, "same_observed_player_count": 2, "status": "COUNTEREXAMPLE_CONFIRMED_OPEN"}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 204, "XML": 25, "package_files": 326, "modinfo": 356}
