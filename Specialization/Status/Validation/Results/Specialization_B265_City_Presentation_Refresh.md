# B265 — Event-driven city presentation and ACTIVE shortcut

## Scope and evidence

The user explicitly approved B265, including profession-colored live institution metrics. The [B264 investigation](Specialization_B264_Acceptance_and_City_UI_Investigation.md) reproduced stale selected-city presentation and Expedition admission caches after governor facts changed without a new turn or owned-effect write. P0 read the current facts correctly. B265 fixes the consumer refresh gap; P0 diagnostics are retained.

No gameplay rule, cost, capacity, source binding, reward, permanent history, timer/frame mechanism, configuration, main promotion or PR change. Existing held Expedition mission problems and other post-v0.1-playtest priorities remain outside this batch.

## Implementation

- `UI/CityPotential.lua/xml` retains its registered context but replaces the visible WorldTracker profession/Potential entry and 0.5-second update loop. The selected-city bridge now reacts to selection/load/governor/turn signals and existing core publication/playback boundaries. It checks only the selected city's detached `LevelBanners` facts, existing owned-write revision and turn. Changes request the existing read-only `CITY_PRESENTATION_READ`; exact token and owner/city/coordinates bind consumption. Independent reads can supersede stale reads only on new semantic signals. Busy core defers dirty work to a later event; unavailable backend, idle boundaries and lost responses cause no polling/retry loop. No city enumeration or saved state is added.
- `UI/ExpeditionTrainingUI.lua` includes selected-city profession/Potential/ACTIVE/status in admission invalidation. Existing native governor signals invalidate the view; publish/playback consumes a fresh SYNC for an interested selected city. `CrewProjectOrder.lua` preserves native queue handling and all other project adapters. The mutation handshake remains separate: no new BUILD/RESERVE retry, cost, queue reservation or source-binding rule.
- The new ACTIVE shortcut joins the native `CityPanel/ActionStack`, using its recessed backing and native 44x53 button/32x32 symbol proportions. It reuses existing institution artwork; no new binary asset. It opens the native Buildings tab containing institutions/districts/wonders. Repeated clicks do not toggle the page closed. Native open/close/lens/input behavior remains in the HD/native functions. Only the local supported specialized city with known ACTIVE receives the shortcut; a city switch or unavailable facts cannot borrow another city's icon.
- `InstitutionPresentation.lua` colors live information by profession using native colorsets: Research `ResScienceLabelCS`, Culture `ResCultureLabelCS`, Commerce `ResGoldLabelCS`, Industry `ResProductionLabelCS`. This supersedes B264's uniform Gold choice for these lines only. Research Tradition, Dialogue, Culture Insights, Commerce Reputation, Standardization and Engineering Study retain their existing values/placement/unknown behavior. Insights remain a count only; current-row emphasis is unchanged.
- Existing bounded trace gains scalar `specialization`, `potential`, `active`, `activeStatus` and `projectionRevision` fields. `INSTITUTION_UI_REQUEST`, `INSTITUTION_FACTS`, `INSTITUTION_UI_APPLIED`, `TRAINING_SYNC_FACTS` and `TRAINING_UI_APPLIED` correlate request keys, current facts and consumer admission without requiring P0 opening. Failed sends are recorded. Diagnostic code adds no native reads, names, arbitrary errors or saved state; existing ring and per-producer budgets remain. Collector configuration is unchanged.
- Package/build stamp: B265.292 / modinfo292. The runtime remains 288 files. No P0 diagnostic entry/report removal and no change to City Banner geometry.

## Static source basis

Installed read-only sources, using repository aliases rather than machine paths:

- `CIV6_ASSETS/Base/Assets/UI/Panels/CityPanel.xml` and HD 2.2 Workshop 2465378070 `UI/Replacement/CityPanel.xml`: native ActionStack/backing/button dimensions.
- Native `CityPanelOverview.lua`: `OnShowOverviewPanel`, `Close`, `GetSelectedTabButton`, `OnToggleBuildingsTab`, and deferred `LateInitialize` event registration. Its stock same-tab toggle closes the panel; the new open-only adapter avoids that branch. HD `DL_CityPanelOverview.lua` retains the CityPolicies/Suk/Expansion include chain.
- Native `Civ6_ColorAtlas.xml` and `Civ6Common.lua:GetYieldTextColor`: all four reused colorsets. Existing Image icon call path supplies exact cell and control sizes.

These are **STATIC_CONFIRMED** references, not native visual acceptance.

## Validation

Risk depth: **L2** consumer invalidation/ownership and admission handshake; **L1** native layout/colors/package.

**LOCAL_SIMULATION_PASS: 94 targeted tests** using actual current Lua with isolated native boundaries:

- 19 new `test_b265_city_presentation` cases: consecutive same-turn promotions without effect writes; promotion/demotion; late fact publication; Potential-only change; busy/unavailable/reloaded backend; late/foreign replies; 1,000 idle boundaries with no requests or layout rebuilding; existing mutation handshake isolation; real production-adapter event wiring/native queue replacement; shortcut idempotence and cleanup; per-profession color containment and native geometry; actual diagnostic facts/admission with zero persistent/native writes.
- 35 existing cases: `test_culture_institutions`, `test_b251_institutions.Presentation`, `test_b251_institutions.StoreSummary`, `test_expedition_training_ui.UI`. Includes archive/preview/current rows, unknown/zero/read isolation, actual Store summary reads, Standardization, normal training/reservation/cancel and uncertain native outcomes.
- 18 `test_expedition_training_trace_integration` and 22 `test_expedition_training_diagnostics` cases: enabled/disabled diagnostic equivalence, deduplication, budgets, redaction, callback ordering and unchanged gameplay state.
- The older standalone `ProductionAdapter` fixture predates five independent panel adapters and fails during setup before reaching this change. B265's new fixture supplies only their inert interfaces and executes the actual current production adapter; both native queue guard/replacement scenarios and new event wiring pass. Old assertions/files are unchanged. The temporary Lupa environment's namespace package requires exposing its existing Lua 5.5 runtime to the older diagnostics import in the runner; no dependency installation or repository test-framework change.

All nine changed Lua sources compile as Lua 5.1. XML and both shortcut localization rows parse; 288-file package registration has exact closure and no duplicate entries; whitespace check passes. No gameplay schema, assets or external sources changed. Context and staged publication gates are recorded with the final checkpoint.

**USER_GAME_TEST_REQUIRED:** native event delivery, shortcut placement at the user's UI scale, exact tab opening and profession-color readability. Existing B263/B264 accepted presentation and prior gameplay evidence are inherited only within their unchanged scopes.

## Deployment

B265.292/modinfo292 DEVELOP_ACTIVE; source 25b812fa5ab2d21feb1a4e7e6e2b4925f73867d0; receipt B265.292-25b812f-playtest.json; 288/288 MATCH; digest 82a841b616a8f6b7ea904e70d4d7f81150c2d0b35ab99f5bfc58ed8f65d0a114. Fresh automatic game-exit checks, exact B264 restoration and B265 activation passed. Stable/outgoing recovery verified; no pending marker, game launch, configuration or main change. Native review pending; no PR. Main remains B069.96 at e901a22. Context check PASS (288 runtime / 922 guarded files); staged publication and pre-commit gates PASS.

## Minimal combined user check

1. Run the existing manual collector. In a Culture Potential-IV city with free Expedition capacity, let a governor establish and promote consecutively to level IV in one turn. Before opening P0, check that the institution row becomes current and the Expedition training option appears. No need to train/travel/complete a mission for this batch.
2. Select a specialized city and click the new badge in the bottom-right action row. It should open city details directly on institutions/buildings/districts/wonders; a second click keeps that page open. Switch from another details tab and switch cities once. The old profession/Potential entry below P0 should be absent; P0 itself remains.
3. Hover available dynamic lines in the four professions: Research blue, Culture purple, Commerce Gold, Industry production color. Check one Standardization line and the Culture Insights count. Do not repeat unchanged reward/balance tests.

The collector is primary evidence for facts/admission. A screenshot is needed only for a layout/color issue or a mismatch that the recorded fields do not explain.

- User decision: none.
- User testing: the combined check above after verified deployment.
- Primary next: wait for scoped native review. No new development batch, PR or main promotion.
