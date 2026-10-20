# B266 — Institution refresh recovery after new-city selection

## Authorization and scope

The user reports that the loaded Culture city retains institutions, while cities founded later do not display them, and explicitly authorizes investigation followed by direct repair. Culture dynamic text color is accepted. Research/Industry color checks remain pending because the institution surface was absent. The prior consecutive-governor-promotion case is deferred to ordinary future play; no repeated forced reproduction is requested.

Narrow UI refresh/lifecycle repair only. No gameplay rules, permanent state, capacity, costs, source binding, rewards, held Expedition mission behavior, timers/frame updates, external configuration, main promotion or PR changes.

## Evidence and local investigation

The B265 collector session `session-20261020T150138Z-4aae4c` contains a single 64-record snapshot, seq 60–123, and stops immediately after connection. It proves current Research/Industry/Commerce facts at Potential/ACTIVE I (seq 95, 107/109, 119) and Industry support reconciliation (seq 108). It does not contain the early institution request/error sequence. The screenshot shows the Industry I banner, no institution category, and internal Industry support carrier rows. These are consistent with the selected-city presentation bridge failing independently of gameplay facts.

The installed native and HD 2.2 CityPanel XML both define `ActionStack → Grid → outer Stack`. Native UI uses `CalculateSize` for stacks and `DoAutoSize` for auto-sized grids. B265 unconditionally invokes `CalculateSize` on all three ancestors. Its test double incorrectly gave all controls the Stack method. More seriously, an exception anywhere within `pump` leaves its local reentrancy guard true permanently.

**LOCAL_SIMULATION_PASS / defect reproduced before repair:** executing actual B265 Lua with the Grid exposing `DoAutoSize` rather than `CalculateSize` raises a nil-method error during initial attachment or deselection. Subsequent new-city selection, publication and playback send zero requests. This is a concrete defect and a strong explanation for the user's old-city/new-city split. The exact native exception was not retained in the submitted ring and is not claimed as a captured stack trace.

## Evidence preservation

One reviewed original moved from `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B265/`, with identical SHA256 before/after: `9c1189472f02350c10f4f93b2a045a7fedecec05309dae09efb73a7905f725a3`. The local `B266_review_manifest.json` associates it with this result. The collector session remains at its existing ignored location; `records.log` SHA256: `b6b415304dc16f4d37a07342e047244153ac1e5f2a8cd2a0fe3daa5c5dcf0e7e`. Unrelated evidence and originals are untouched.

## Implementation

- `CityPotential.lua` now calls `CalculateSize` for the native action/outer stacks and `DoAutoSize` for the intervening auto-sized Grid, followed by anchoring. No geometry, icon artwork or carrier changes.
- The event callback always releases its reentrancy guard through a protected refresh boundary. Exceptions cannot permanently stop later city selections or fact/governor notifications. No automatic request retry, new timer, frame callback or saved state is introduced.
- Failures enter the existing bounded trace as `INSTITUTION_UI_FAILURE`, with a fixed error code, phase (`viewStage`), known numeric owner/city and existing redacted error metadata. Diagnostic failure itself cannot disable refresh. No raw exception/path/name is published.
- Reparenting and icon-display caches are committed only after their native calls succeed. Replies still require the exact request identifier and city reference. Existing semantic invalidation checks remain.
- B266.293 / modinfo293; 288 runtime files. Only one functional runtime source changes; `Probe.lua` and modinfo carry the build stamps. Training, facts/Store, institution content/colors, banners, gameplay writers and schemas are unchanged.

## Local validation

**LOCAL_SIMULATION_PASS: 64 scoped tests.** The actual current Lua runs against isolated native boundaries:

- 10 new B266 tests cover the loaded Culture city followed by newly founded cities of all four professions, unclaimed → claimed identity, both overview/selection event orders, no selected city at load, busy core, delayed replies, foreign-city rejection, return to the old city, native carrier filtering, shutdown, and layout/subscriber/icon/diagnostic failures. A 1,000-boundary check preserves zero idle requests/layout work. The new lifecycle regression failed against B265 before the repair.
- 19 B265 tests retain same-turn governor invalidation, admission behavior, unknown/backends, shortcut opening/cleanup, color containment and no timer/frame API. Its fixture now distinguishes Grid from Stack instead of granting every control every method; previous assertions remain intact.
- 35 existing institution, B251 presentation/Store summary and Expedition training UI tests retain their covered scopes. An expected negative training test emits its pre-existing multiple-birth diagnostic; the suite passes.

Both changed Lua files compile as Lua 5.1. XML parses, package registration has exact 288-file closure with no duplicates, and whitespace checks pass. Final context/publication gates accompany the checkpoint. No game execution is part of these tests.

**Native boundaries:** culture live-metric color is USER_GAME_TEST_PASS from the user's report. New-city institution visibility is USER_GAME_TEST_FAIL on B265 and USER_GAME_TEST_REQUIRED on B266. Research/Industry colors remain pending. The precise native exception was not captured, so its attribution remains a source-backed, locally reproduced explanation. Gameplay bonuses are not newly accepted from a carrier log alone. Consecutive governor promotions stay a deferred observation, not a required retest.

## Deployment and minimal check

Local B266 is complete; live remains B265.292 until W0003 verifies the committed build, game exit, restoration/activation and per-file equality. Main remains B069.96; no PR.

1. Start the manual collector before the relevant city operations. Use an existing testing save with the reported new Research/Industry cities; reselect them and open city details directly. Four institution rows should appear, with the current/preview states matching each city's actual Potential/ACTIVE. Internal support carriers should no longer replace the category.
2. Click the ACTIVE shortcut once; it should open institutions/buildings/districts/wonders. Switch between one new city and the loaded Culture city. Hover available Research/Industry dynamic values to finish their color review.
3. If a new city is founded during normal play, glance at the same surface after specialization is established. Do not repeat the difficult governor-promotion sequence solely for this batch. Keep it as future ordinary-play observation.

- User decision: none.
- User testing: the focused UI check above; use the collector for read/failure stages and screenshots only for a remaining visual issue.
- Primary next: guarded deployment, then wait for scoped native review. No new batch, PR or main promotion.
