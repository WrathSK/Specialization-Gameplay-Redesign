# B252.279 — institution backdrops and Development Investment sidebar

Date: 2026-10-19. Basis: develop `d650b85`, deployed B251.278 from `5be0345`, D0057 / A0177 / S0673. The user authorized complete Commerce institution help, district-style gradient backdrops with native Roman labels, and a city → district → details sidebar. B251 visual feedback identifies small/soft glyphs and incomplete Commerce text; it is not blanket acceptance of the earlier visual package.

## Scope and presentation

- Commerce I–IV help now includes the existing base support, 同业制度, 商业化, 资本投资, 发展投资, 资产重组 and 商业信誉 rules. Accepted D0057 source identity filtering, Harbor total Food, per-domain Floor, minimum eligible next-tier quotation and contract continuation are preserved. The existing reputation summary attaches below its own paragraph. Names and gameplay definitions are unchanged.
- Replace only the active institution row artwork with four gradient/beveled hex backdrops, one for each v0.1 profession. A native `CityPanelText` label renders Ⅰ–Ⅳ over the backdrop at the same font size as the institution name. The glyph is not part of the texture. Retain four-level previews, 3px spacing, separate name/status widths, Gold ACTIVE emphasis and the earlier read-only summaries, including Standardization.
- Development Investment uses three adjacent, independently scrollable columns: target cities; selectable district cards; quotation/contract/effect/help cards. Selecting a city or district never signs a contract and never selects the next level automatically. Confirmation remains explicit. Empty, unavailable, stale and held states remain visible. Contracts can be inspected even after current route/eligibility disappears.
- Reuse native window, destination-card, city-banner, drawer and confirmation-button textures. The sidebar uses the existing Development Investment controller and transaction protocol, not the Spy gameplay controller. Window resizing recalculates widths and wrapped card heights; below 800 available UI units, the same hierarchy becomes sequential pages with Back, Refresh and Close. Native visual fit remains unverified.

## Read and lifetime contract

The existing source-city OPEN/REFRESH request publishes the existing quotation snapshot. UI builds detached city/district groups only when this panel opens, receives a relevant revised/acknowledged snapshot, changes local selection or receives a **ScreenResize** event. No hover request, frame update, timer, gameplay recomputation or new native fact collector is added.

`FindID` is cached only within one render (one lookup per unique displayed target); grouping reads the target's current city identity/name/coordinates. Selection is keyed by Owner/city/coordinates and district, not row position. Reordered or added quotes retain the intended target; removed/replaced targets clear selection. Contract historical references remain distinct from a different city at the same ID. The UI never annotates the shared Gameplay snapshot.

Pending request tokens retain the existing single-confirmation latch and no-auto-retry behavior. Only confirmation sends target city/domain/revision to the existing revalidating writer. Close, load, local-player change and context shutdown discard local selection; callbacks are removed on shutdown. No save field, schema, currency precision, carrier, contract rule, capital calculation or gameplay subscription changes. Existing A0177 read-only presentation ownership remains applicable.

## Native references and artwork

**STATIC_CONFIRMED:** installed Civ VI `Base/Assets/UI/Icons/Icons_Districts.xml` registers flattened district icons; `Civ6_Styles.xml` and `Panels/CityPanelOverview.xml` provide the native font/container conventions. `Choosers/EspionageChooser.xml` and the already deployed `Mod/UI/ExpeditionSpyWindow.xml` provide the relevant banner/card/drawer composition. The bounded lookup found empty generic swatches but did not establish a reusable separately shaded district backing.

Under the user's fallback authorization, four SVG backdrops were redrawn against the provided district-icon screenshot, retaining a dark-to-light face gradient and beveled colored rim. No packed native texture, screenshot pixels or unrelated external assets are copied into the package. The [asset note](../../../../Art/Institutions/README.md#b252-backdrops) records generation, mapping and fixed checksums. The earlier 16 SVGs and two DDS atlases remain unchanged for compatibility. No new license or rights claim.

## Local validation

**LOCAL_SIMULATION_PASS:** 41 selected methods, including 13 new B252 methods. Actual Lua callbacks cover city/district selection, no selection-triggered request, scalar confirmation, double-click latch, stale/rejected/held results, reordering, target replacement, completed/active contracts, snapshot immutability, closing, resize-only reflow and narrow-page navigation. Retained B246 UI protocol and B251/Culture/Industry/Commerce institution checks also pass.

Static checks cover Lua 5.1 compilation of both changed UI scripts, XML/control/localization closure, real SQLite execution of the icon/text registrations, four ordered backdrop entries, both exact reviewed DDS headers/dimensions/payloads/gradient pixels, equal native label fonts, unique imports and 269-file runtime package closure. The local height fixture approximates text wrapping; it is not a native layout renderer. No claim of native rendering, economic output or CPU/memory improvement follows from these checks.

Run from the repository root with the existing Python 3.14/Lupa environment and `DevelopmentTests` on the module path:

```text
python -m unittest test_b252_sidebar test_b246_development_ui.UI test_b246_development_ui.Package.test_controls_and_localization_keys test_culture_institutions test_b251_institutions.Presentation test_b251_institutions.StoreSummary test_b251_institutions.Package.test_reserved_width_spacing_and_no_new_update_or_write_paths test_b236_entry_ui.IndustryInstitutions test_b247_ui_package.UI.test_current_and_legacy_institutions_render_without_old_active -q
```

The initial Python 3.10 runner could not import an existing dependency using newer f-string syntax; no checks were claimed from that attempt. Reusing the already installed Python 3.14/Lupa environment resolved the runner mismatch without changing unrelated source or installing tools. Only fixtures/expectations directly affected by the new controls were adapted; existing behavioral assertions remain. Historical build-pinned package tests were not run or rewritten to claim current-package success; the B252 package check verifies the current build.

## Publication boundary

The user explicitly approved a one-time publication exception for **only** `Mod/Textures/SPC_Institution_Backdrops_32.dds` and `_64.dds`, 82,176 bytes total, with the exact SHA256 values in the asset note. Structural/visual review and raw decoded-pixel comparison are complete. Binary-only commit `62154a3` contains only those two blobs. Both indexed SHA256 values matched approval; the unchanged checker returned NOT_RUN for binary content. A command-local hook exception was applied only to that commit, not an automated scanner PASS. All other changed text/SVG/source/test/current-document files use the unchanged staged publication gate. No lasting hook, scanner policy, ignore rule, frozen evidence, raw screenshot/log/save or main change.

## One minimal native UI flow

1. In **城市详情 → 专业机构**, inspect a Commerce city: all four rows/previews, readable Roman numerals, gradient badges, current-level Gold text and complete ability help. Check one other profession incidentally; no progression grind is needed.
2. In an eligible Commerce IV city's production list, open **发展投资**. Select a city, then a district; verify the third column identifies the matching target/quote building/price/15% cost. Change the selected city/district and use **刷新报价** once; inspect scrolling and long text, with no unintended signature or payment. At the user's ordinary resolution/UI scale the columns and footer must stay readable.
3. If a valid offer is available, use **确认发展投资** once and verify the displayed target, actual debit and active contract agree; otherwise existing-contract browsing and disabled reasons can be checked now, with the single signing click carried to ordinary play. Do not repeat contract maturity, save/load or yield testing solely for this presentation change.

**USER_GAME_TEST_REQUIRED** for native backdrop loading, font/gradient readability, native column/card fit and the presentation-to-confirmation click. Existing gameplay validation and S0669 held/post-playtest items remain unchanged.

## Deployment and continuation

Verified deployment on 2026-10-19 after clean committed/pushed source and fresh automatic game-exit checks before both guarded switches. B252.279/modinfo279 DEVELOP_ACTIVE; source efd54c0f353fcaa6751f0271c9a9461570ebb149; receipt B252.279-efd54c0-playtest.json;269/269 MATCH,digest ddd0d8bc6aec6ae9ff558586911494065c9f2498828d4d851cbc43a76537d281. Stable and outgoing B251 recovery verified; no pending marker, game launch or configuration change. The exact B251 receipt restored the stable bridge, then the new B252 receipt activated the reviewed package. Stable/main B069.96 remains untouched. Context integrity (269 runtime /861 guarded files), eight scoped document links/anchors, diff review and the normal staged publication gate passed for all24 non-binary batch files; the two fixed DDS blobs were the separately approved exception (`62154a3`).

The source/current checkpoint is complete. Stop for the single native UI flow; no gameplay, audit repair or balance batch follows automatically. Native visuals remain USER_GAME_TEST_REQUIRED and all S0669 deferred/in-playtest boundaries remain unchanged.
