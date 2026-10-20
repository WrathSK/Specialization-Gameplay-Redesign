# B254.281 — embedded institution levels and city-banner emblems

Date: 2026-10-19. Basis: clean develop e84c222, source/live B253.280 from72e7b15, D0057/A0177/S0677. The user accepted the final preview and explicitly authorized B254. Presentation only; gameplay semantics and persistent state are unchanged.

## Approved scope

- Use palette A and embedded serif outlines, without anisotropic compression. The approved preview has shortened serif overhangs/optical spacing and a uniform7% numeral reduction. Institution rows retain separate I–IV icons, stage text, gold current emphasis and existing ability metrics; no segment strip is added to them.
- Add one40-unit-wide emblem immediately outside the native local city banner's left edge. Main numeral is canonical ACTIVE. Four close segments encode filled ACTIVE, bright-outline/dark-fill unlocked Potential, and dim locked tiers. No permanent A/P labels or second hexagon. Chinese tooltip explains levels and states.
- The prior Development Investment sidebar requests (lower second/third columns, content-based detail layout, left titles, scroll/footer spacing, active-contract badge/sorting) remain pending. This accepted icon/banner handoff does not silently expand into them. All held gameplay/audit work stays held.

## Implementation and source of truth

`LevelBannerState` reads `EffectiveFacts.Read` through Gameplay's existing Store-aware canonical path. It publishes only detached identity/coordinate/kind/Potential/ACTIVE/status scalars. No new Property, save field, modifier, carrier, Gameplay operation or command is introduced. This is a disposable presentation projection, not a new authority.

The existing permanent-write observer is chained after all existing subscribers and only marks the affected city. Native governor/player-turn events mark that player's cities; add/remove events mark one city; rare transfer/load events rebuild current local projections. Publish/Playback boundaries flush pending keys once. Empty boundaries perform no facts reads; unchanged projected values do not increment revision. Load reconstructs; removed-city views are pruned. No timer, frame handler or repeated command.

Native Expansion2 `CityBannerManager` wildcard extension chains `UpdateName` and `Uninitialize`. A separate UI context creates an emblem under `m_Instance.Container`, outside its left edge. The native Anchor remains responsible for fog visibility, camera zoom and map placement. Existing name/production/other-Mod methods are preserved. Ready handshakes handle either context-load order; parent replacement, removal and context shutdown destroy old children. The UI checks the projection generation/revision at publish/playback, and revalidates owner/id/coordinates on render. Foreign, unassigned, malformed or UNKNOWN states hide the emblem rather than infer ACTIVE from Potential. Current supported scope remains the user's local test civilization; no foreign specialization information is exposed.

Read scope: current Authority/Status/P0-H, InstitutionPresentation and its UI bridge, EffectiveFacts, Store write notification path, RuntimeWork, native Expansion2 banner instances/manager and Base Colors/Box usage. Native source confirms the container, wildcard hook, shutdown and normalized color API. It does not certify actual positioning/overlap.

## Local validation

**LOCAL_SIMULATION_PASS:**32 selected methods:12 B254 tests plus20 institution/history/UI regressions. Actual Store/EffectiveFacts fixture proves Potential4/ACTIVE2 then ACTIVE4 and no Property writes or saved-record changes. Event tests prove100 notifications coalesce to one city read and100 empty publish boundaries add no reads; governor and turn fallback, removal, detached values, UNKNOWN withdrawal and coordinate mismatch are covered. These are access-count facts, not measured native CPU/memory improvement.

Actual Lua UI/model/wrapper tests cover all five accepted segment combinations, original callback chaining, initial attachment, duplicate attachment, replacement, stale detach, backend replacement, foreign exclusion, and handler/child release. Color arguments are constrained to0–1, icons select64px assets scaled to40 units. Lua5.1 syntax, XML, localization and icon SQL, package closure, exact DDS hashes/headers/cell counts pass. One existing culture test was updated only from native-text expectations to embedded-level icon expectations. An initial fixture assertion used city1 instead of its actual101 reference; corrected before final PASS. Existing frozen reports/results are unchanged.

Native icon loading/filtering, mouse tooltip/selection, placement at different zoom/UI scales and neighboring city overlap remain **USER_GAME_TEST_REQUIRED**. The prototype does not introduce collision avoidance or redesign banners.

## Minimal native check

In one normal session:

1. Open **城市详情 → 专业机构**: inspect I–IV, especially III/IV, at the usual UI scale. Existing institution names, current-stage emphasis and ability summaries should remain.
2. On the map, inspect an owned specialized city: left emblem numeral equals ACTIVE; filled/outlined/dim segments match ACTIVE/Potential. Hover for the two values. Ordinary city-banner selection and production display should still work. Unassigned/foreign cities have no emblem.
3. If convenient, use one normal specialization investment or governor change and check the emblem follows the new effective level without opening P0. Do not manufacture every combination; local tests cover the five mappings.
4. Zoom near adjacent cities; optionally compare one other UI scale. Report overlap or unreadable segments. No repeated lifecycle/yield/contract test is required.

## Publication and deployment

Two new lossless BGRA8 DDS atlases contain only the16 approved vector icons. Browser rasterization uses a temporary isolated profile; decode exactly matches source pixels. No external image, personal path, account data or embedded font file. Exact fixed blobs received explicit one-batch publication authorization; all source/SVG/test/document files use the unchanged normal staged gate. No lasting checker/hook exception. Old B251/B252 art and frozen evidence remain unchanged.

B254.281/modinfo281 DEVELOP_ACTIVE; source `655364337af6fde1acb835f28649ba0411c6e7ec`; receipt `B254.281-6553643-playtest.json`;277/277 MATCH; digest `b1d61b7de9f28036ac66c62fa889b329011fb6d023515b3e96e405f7341514cb`. Fresh game-exit checks, exact B253 restoration and B254 activation passed. Stable and outgoing recovery verified; no pending marker, game launch, configuration or main change.

37 source/text/SVG/test/current files passed the normal staged publication gate; the two exact authorized DDS blobs were committed separately.277 runtime/889 guarded Context check PASS. Main/stable B069.96 remains unchanged. Native acceptance is pending; stop for the minimal visual flow.
