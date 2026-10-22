# B253.280 — native numerals and Development Investment layout refinement

Date: 2026-10-19. Basis: clean develop `1fe78ca`, deployed B252.279 from `efd54c0`, D0057 / A0177 / S0675. The user explicitly approved B253 after reviewing backdrop and typography alternatives. Keep native Roman labels and the existing B252 artwork; fix opacity and the previously requested sidebar layout. No gameplay, Design, money rules, save schema, timer or unrelated UI change.

## Feedback and approved scope

The user's B252 screenshots show the sidebar above the native bottom edge, unequal column widths, shifted city-name contents, an overcrowded source summary and a repeated target heading. They also show dark institution backdrops. These are scoped visual observations, not a new transaction or gameplay PASS.

Source review confirms widths capped separately at295/280/360 and height reduced by114 units. The old city banner omitted the native BannerNone layer and used a zero vertical name/icon offset instead of the native negative offset. Unestablished institution backdrops used0.60 alpha and other established rows0.85. This alpha contributes to darkening; it does not prove that every visual difference came from opacity alone.

## Scope and presentation

- Institution backdrops now use full opacity in every stage. The existing four DDS backdrops, SVGs, native `CityPanelText` Roman labels, name/status emphasis and ability summaries are unchanged. No new binary asset or publication exception.
- Sidebar uses the native27-unit top inset and extends to the viewport bottom. All three columns use one width, up to295 units; the existing narrow-screen sequential navigation remains. No auto-selection or automatic signature.
- Source city has the layered native city-name banner. Treasury and occupied capacity are separate lines. Treasury displays its whole-number floor; other monetary summaries use nearest-integer display formatting. Original quotation, debit receipts and confirmation inputs remain unmodified; these display values are not authoritative amounts or new rounding rules.
- Target cities use the existing native/Expedition-style banner, corrected name/icon offsets and a district icon strip. Icons come from the same detached quote/contract rows shown in the second column, including unavailable or historical contract rows with explanatory tooltips. No extra city/district scan is introduced. More icons than fit use native arrow buttons; pagination is temporary, bounded to current groups and pruned when a group disappears.
- Details omit the repeated city/district heading and occupy three equal-height sections: quotation/investment; effect/completion; signing/continuation. Each section has a light-blue native banner and independent clipped scrolling. Existing contract state and debit summary remain inside the third section, not a fourth card. Selection prompts, disabled reasons, request feedback, explicit confirmation and refresh remain accessible.

## Read and lifetime contract

Inherit the [B252 snapshot/selection contract](Specialization_B252_Commerce_UI.md#read-and-lifetime-contract) and A0177. Only explicit panel interaction, revised/acknowledged snapshots and ScreenResize reflow the UI. No frame callback, timer, new native reader, gameplay event, Store field or backend writer change. Per-render identity lookup caching, scalar confirmation, pending-token no-replay protection and close/load/owner shutdown handling remain. Paging never sends a gameplay operation or selects a city/domain.

## Local validation

**LOCAL_SIMULATION_PASS:**47 selected methods, including seven B253 checks. Actual Lua callbacks cover equal-width/bottom/section arithmetic over five viewport cases, non-mutating integer display, ten-domain icon paging/clamping, unavailable city reasons, inherited selection/refresh/stale/held/double-click/identity/load/shutdown behavior and all four institution presentations. XML controls/localization, Lua5.1 compilation and269-file package closure pass. Both B252 DDS hashes remain exact. The new XML geometry test initially matched a same-named district-instance control; it was corrected to inspect the intended city instance without changing runtime behavior.

Use the existing Python3.14/Lupa environment with DevelopmentTests on the module path. Selected suites: `test_b253_sidebar.Presentation`; `test_b252_sidebar.Sidebar`; B252 control/localization and Lua compilation checks; `test_b246_development_ui.UI` and its control/localization check; `test_culture_institutions`; B251 Presentation/StoreSummary/reserved-width checks; B236 IndustryInstitutions; B247 current/legacy institution rendering. Historical build-pinned package assertions are retained, not rewritten; B253 verifies current build280 and unchanged asset hashes.

Initial runner attempts lacked the matching Lupa import path; they produced no validation evidence. The existing matching Python3.14 dependency directory was then used without installation or environment changes. Local text-height stubs and arithmetic are not a Civ VI renderer: native font, clipping, bottom alignment and button hit areas remain **USER_GAME_TEST_REQUIRED**.

## Minimal native check

One continuous UI session, without repeated save/load or contract maturity:

1. In **城市详情 → 专业机构**, compare an established and an unestablished row if available: same backdrop colors/full opacity, native Roman glyphs, stage differences still conveyed by name/status.
2. Open **发展投资**. Check bottom alignment, three equal widths, native city banners and district strips, and the two-line integer Treasury/capacity summary. Select a city then a district; verify three equal detail sections, matching quote, long-text scrolling and no repeated target heading. Switch selection and click **刷新报价** once. Use icon-strip arrows only if present.
3. If ordinary play offers an eligible target, click **确认发展投资** once and verify the selected target/contract state. If no offer is available, defer only this click; do not manufacture a new economic/lifecycle test.

## Publication and deployment

All changes are text/source/test/current metadata and use the unchanged staged publication gate. No preview artwork, screenshot, local path, log or binary is added. B252 evidence, assets and other deferred work remain unchanged. Main/stable B069.96 is not promoted.

B253.280/modinfo280 DEVELOP_ACTIVE; source `72e7b15a816a79b953098fcbe1cf38a52b6debaf`; receipt `B253.280-72e7b15-playtest.json`;269/269 MATCH, digest `92641e178fc2d9c06e1e97abbf195bc8ea692bf183987b432e9004fbdfb92e9d`. Fresh game-exit checks, exact B252 receipt restoration and B253 activation passed; stable and outgoing B252 recovery are verified. No pending marker, game launch, configuration or main change.

All14 source/checkpoint files passed the ordinary publication gate. Context integrity (269 runtime/863 guarded), four scoped Markdown links and diff review passed. This deployment does not establish native visual acceptance. Stop for the minimal UI flow; no further batch starts automatically.
