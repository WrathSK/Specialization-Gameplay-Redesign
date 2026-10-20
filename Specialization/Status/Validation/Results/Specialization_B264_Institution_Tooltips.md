# B264 — Native-style institution tooltips

## Scope and evidence

The user approved B264 following the four-profession tooltip plan and the Civil Engineering Directorate text preview. Reformat all 16 institutions using the native tooltip hierarchy, bullet points and inline icons. Use native Gold text color for existing dynamic information, positioned under its own ability. Keep Culture Insights as a count only. The user will combine native acceptance with the preceding batch.

Presentation only: D0057/A0177 and all profession effects, conditions, formulas, saved histories, event-driven refresh and held issues remain unchanged. No gameplay writer, test framework, timer/frame mechanism, icon asset, main change, configuration change or PR. B263's new Roosevelt shell still awaits its own native acceptance.

## Implementation

- [Shared presentation](../../../../Mod/InstitutionPresentation.lua) retains row selection, established/preview/history status, selected-city guards, signatures, factual reads and metric arithmetic. It adds profession/tier subtitles and a footer with activation requirements/current state. Research descriptions now use the same localization path as the other professions.
- [Institution text](../../../../Mod/Text/TestText.sql) and [Commerce text](../../../../Mod/Text/Restructuring.sql) provide a brief introduction and separate ability headings/bullets. Existing eligibility, rounding, caps, interruption/history distinctions and current supported ranges are preserved. Industry IV also states the already-established start-locked Crew price and civilization-era study context from the accepted preview. No future balance commentary is shown.
- Dynamic values retain their current inputs. Research Tradition, Commerce Reputation, Dialogue, Insights, Standardization and Engineering Study use `[COLOR:ResGoldLabelCS]`, followed by `[ENDCOLOR]` before subsequent abilities. Pending values do not become zero. Standardization retains template counts and current source efficiencies, including the building-only Gold purchase limitation. Insights do not expose civilization/category details.
- Source basis: installed `CIV6_ASSETS/Base/Assets/UI/Civ6Common.lua:GetYieldTextColor` uses this exact Gold color token. `Civ6_ColorAtlas.xml:ResGoldLabelCS` defines the native Gold colorset. Native `ToolTipHelper.lua`, `GreatPeople.xml`, `Yields.xml` and Chinese base text establish the 15 reused bullet/yield/housing/Tourism/Great Person tokens. This is static source evidence, not native rendering acceptance.
- Native tooltip controls, width/font, institution rows, badges and City Banner geometry are untouched. No new runtime files or binary publication exception.

## Validation

Risk depth: **L1 presentation only**.

- **LOCAL_SIMULATION_PASS:** 12 existing methods from `test_culture_institutions.CultureInstitutionDisplay` and `test_b251_institutions.Presentation`. Covers all-tier preview/history, ACTIVE changes, city/owner guards, stale/unknown/zero values, correct per-ability metric placement, Standardization efficiencies and duplicate notification behavior.
- **STATIC_CONFIRMED / local rendering checks:** both supported display-language rows for all 16 descriptions load in SQLite and match the intended Chinese copy; actual Lua renders all 16 headings/requirements/state labels and all six metric locations with balanced Gold tags, without untranslated keys or unresolved placeholders. Lua 5.1 compilation succeeds.
- Existing fact selection/signature/filter/metric code is byte-equivalent after normalizing the three added presentation-only line breaks. No gameplay calls or writers are added. All 15 icon tokens were found in installed native sources. The 288-file package has exact manifest closure, no duplicate entries; whitespace checks pass.
- Tests use the existing temporary Lupa dependency environment, without installing tools or editing historical test fixtures. No full gameplay regression is warranted for this text-only change.
- **USER_GAME_TEST_REQUIRED:** native line wrapping/height, inline icon alignment and Gold readability at the user's UI scale. B263 shell presentation and access remain pending; no new gameplay PASS is asserted.

## Deployment

Source is B264.291 / modinfo291. At this implementation checkpoint, live remains B263.290. Commit/push clean develop, then use W0003's fresh process checks, exact previous receipt restoration, new receipt activation and source/live equality checks. If the game is running or its status cannot be established, leave the existing package unchanged.

## Combined user check and stop

During the user's combined B263/B264 review, hover institution entries in the four professions. Inspect one long level-IV tooltip, one unestablished/inactive entry, and available dynamic values (especially Standardization). Expect left-aligned sections/bullets, working native inline icons and Gold dynamic lines under the right ability; no clipping or raw formatting tags. Existing Insights shows only a count. No separate gameplay or cold-load retest is added for unchanged behavior.

- User decision: none.
- User testing: combined B263 shell and B264 tooltip visual review.
- Primary next: finish guarded deployment if possible, then wait. No PR or next batch.
