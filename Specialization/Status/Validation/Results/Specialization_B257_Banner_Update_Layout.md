# B257 — Potential-only banner updates and reversible layout trial

## Approved scope and evidence

The user accepts B256 icon size as approximately correct, defers slight institution-icon softness, and reports that filled segments update when investment raises ACTIVE. **USER_GAME_TEST_FAIL:** without a governor, Potential I→II does not immediately brighten the second outline; governor reassignment refreshes it. The map segments still appear below the flag bottom. Two screenshots and SHA256 records are archived under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B256/`.

User authorizes analysis and direct implementation: fix the update omission, and trial a larger whole map emblem spanning the city-defense strip top to the city-name flag bottom. Record an easy layout rollback. Institution artwork/size stays unchanged; softness is a deferred UI follow-up, not a v0.1 blocker.

## Cause and repair

STATIC_CONFIRMED: Store.WriteInvestment saves the investment ledger without calling OnPermanentCityWrite; InvestmentAction deliberately omits that generic notification for Store-owned cities. The established Gameplay refreshInvestmentSupport dispatcher receives a readback-proved COMMITTED result and updates named consumers, but B254 LevelBannerState was absent. It listened only to the generic notification and native governor/city/turn events. Unchanged ACTIVE therefore has no guaranteed route to republish increased Potential. Incidental native events can mask this omission.

Add LevelBanners to the existing COMMITTED-only city refresh list. Its Refresh marks that city and flushes the detached canonical projection before returning, independently of cross-context publish callback ordering. It re-reads EffectiveFacts, never copies levels from the request. No new timer, global investment scan, persistent field, payment/consumption rule or general Store notification is added. Existing governor refresh remains unchanged.

## Reversible map layout trial

Institution icons remain32px atlas/32-unit controls. Only map emblem geometry/rendering changes:58x58 badge,58x62 group,12x4 segments, bottom inset6. The native frame container is41 units high and CityDetails extends26 units above it; the trial places the visible badge top near that defense-strip top and insets segments to match the visible flag rather than its transparent texture padding. The6-unit inset is a screenshot-based visual calibration, not proof of every scale's opaque edge.

Use native Grid with zero slice corners and a complete64x64 source rectangle, drawing it at58x58. IconManager.FindIconAtlas supplies the existing64px cell origin/sheet via SetTexture(x,y,sheet). This differs from B255 Image resizing: the Grid declares the full source rectangle to stretch. Native references: Expansion2 UI/CityBanners/CityBannerInstances.xml (frame/status geometry), Expansion2 UI/Additions/HistoricMoments.xml/.lua (whole-image zero-corner Grid), Base/Assets/UI/WorldView/CityBannerManager.lua (atlas lookup and offset SetTexture). These are static API precedents; actual clipping, scale and overlap remain native checks. No new texture/binary exception.

**Rollback checkpoint:** B256 clean checkpoint `6548c45`, runtime source `3259a50`, receipt `B256.283-3259a50-playtest.json`. To revert only this visual trial in a later approved batch, restore `Mod/UI/LevelBanners.xml` and `Mod/UI/LevelBanners.lua` from that checkpoint, adjust the corresponding render/geometry assertions, then maintain the new batch metadata and deploy normally. Keep the B257 Gameplay notification, LevelBannerState.Refresh and Potential-only regression. Do not reset the branch or restore the entire runtime, which would discard the update repair. Existing Git history and deployment recovery already preserve the baseline; no duplicate source backup.

## Local validation

LOCAL_SIMULATION_PASS:41 selected methods. New pre-fix counterexamples fail on both normal and DEV investment paths, then pass after the repair: real InvestmentAction/request code, Store-shaped adapter with no generic callback, ACTIVE I and Potential I→II, immediate outlined second segment, one-city publication, unchanged other view, no duplicate debit or notifications for rejected/unknown/already-committed results. This adapter is not a complete Store simulation; actual Store notification omission was inspected directly. Existing actual-Store/canonical-read checks remain included.

Existing atlas hashes, Lua syntax, package closure, native callback lifetime, institution UI and investment propagation checks pass. Two unrelated historical tests were encountered and not rewritten: old package assertion pins modinfo201; old construction transport test uses retired CREW_250 and also fails with unchanged HEAD Gameplay. The41-method scoped run excludes those two; no whole-suite PASS claim. UI mocks validate calls/model/geometry, not native raster behavior.

## Minimal native check

1. With no governor, invest one P1 city toP2. Without governor reassignment/P0, main numeral remainsI and the second segment becomes bright outline immediately.
2. Inspect that same map emblem: complete badge, top near defense-strip top, segment bottom at city-name flag bottom. Check one ordinary zoom/click. This is a reversible visual trial.
3. If convenient, observe one existing governor change for filled/outlined transitions. Do not retest gameplay yields/save-load. Institution softness remains deferred.

## Publication and deployment

B257.284/modinfo284 DEVELOP_ACTIVE; source `adeae34b4ddf8f2fe768a90be0e6c8ef700a2081`; receipt `B257.284-adeae34-playtest.json`;277/277 MATCH; digest `3293e333700b85b275cb59f8b32f5d8bcfe5a0b912e6e12444b55a2a1dabc937`. Fresh game-exit checks, exact B256 restoration and B257 activation passed. Stable/outgoing recovery verified; no pending marker, game launch, main or configuration change.

14 batch-owned files passed the ordinary publication gate.41 scoped methods and277-runtime/893-guarded context checks PASS, with the two historical exclusions recorded above. Native update/layout review pending. Main/stable B069.96 and held work unchanged.
