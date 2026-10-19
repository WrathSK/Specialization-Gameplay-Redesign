# B251.278 — institution icons, previews and live summaries

Date:2026-10-19. Basis: develop `fce2526`, source/live B250.277 `d6bb190`, D0057 / A0176 / S0671. The user authorized supplied institution icons, all four current-profession levels, inline ability values, count-only Culture Insights, native-style spacing and clearer ACTIVE highlighting; Standardization was explicitly included. This is presentation work with a necessary read-only Store projection, not a gameplay, save-schema, balance or held-feature repair.

## Scope and presentation

- Import16 user-supplied icons under descriptive names. Native `Image:SetIcon` consumes two4×4 DDS atlases,32px and64px. Original SVGs are retained in [Art/Institutions](../../../../Art/Institutions/README.md).
- Every current profession displays its four configured levels. Unestablished levels say **尚未建立** and explain that they are previews; no institution, Property or ability is created. Previously established other-profession institutions retain their existing history-only behavior. Row data still permits siblings at the same level.
- Preserve32px row height, add3px spacing, reserve32px for the icon and64px on the right for state. The name is independently truncated before the state column. The highest effective institution and **当前** use the native `Gold` color; other established rows remain readable and previews are lighter. No new background or icon system beyond the supplied assets.
- Attach the summary immediately below its own ability description. Values are retained history or a source offer, not proof that an inactive ability is currently applying an effect.

| Ability | Displayed summary |
|---|---|
| 学术传统 | Retained turns, existing speed-adjusted percentage, turns to the next threshold and paused accumulation when applicable. |
| 商业信誉 | Retained progress out of40 and existing Commercialization percentage. |
| 时代对话 | Retained earned Great Work Tourism percentage. |
| 人文考察团 | **文化见闻：N份** only; no civilization-by-mission records or receipts cross this projection. |
| 标准化 | This city's retained building/District template counts and its own currently offered construction percentage and eligible-building Gold discount. It does not aggregate other Industry sources or promise the deferred precise District purchase discount. |
| 工程传统 | Completed study layers and the corresponding percentage-point increase conditional on ACTIVE IV. |

For example, an ACTIVE IV Industry source with two study layers shows construction+14% and eligible-building Gold discount4%; at ACTIVE III it shows+10% and0%; below III it preserves known template counts while saying the source currently provides no Standardization. The template list and other-source comparisons remain in the existing detailed report.

## Read and lifetime contract

Existing selected-city `CITY_PRESENTATION_READ` reads EffectiveFacts, the institution archive and one new `CityProgressionStore.InstitutionSummary` projection. The projection uses the already guarded city record and exact token/Owner/city/coordinates; it returns detached scalar history and counts. It does not call `ReadTemplates`, whose compatibility path can initialize a ledger, or invoke enrollment, reconciliation, native building enumeration, effect application or another consumer refresh.

Template provenance must validate and reconciliation must be complete before publishing counts. Missing/old/uncertain template history remains **待确认**; it is never silently converted to empty or initialized by a tooltip. Partial summary failure does not erase independently confirmed institution identity. An unavailable city mirror preserves established rows with UNKNOWN state but drops stale numbers. A different city cannot inherit the previous summary.

Store remains authoritative for history. Research percentage/threshold reuse the existing pure `ResearchTradition.Shadow`; the other displayed fixed formulas match their current consumers. No new saved field, cache, queue, subscription, timer or scan scheduler is added. The existing selected-city request/revision mechanism is unchanged. Work is limited to the selected city's stored template/insight collections, not all-city or native world facts; UI receives scalar counts instead of the collections. Tooltip hover performs no request. Display signatures include values that are actually shown and ignore unrelated record revisions.

## Native references and local validation

**STATIC_CONFIRMED:** installed Civ VI `Base/Assets/UI/Panels/CityPanelOverview.lua` uses `Image:SetIcon` for building/District rows and `SetColorByName` for UI colors. `Base/Assets/UI/Civ6_ColorAtlas.xml` defines `Gold` and `White`; the native city-detail XML uses3px list spacing. These read-only sources establish the API/layout convention, not successful rendering of this new package.

**LOCAL_SIMULATION_PASS:**23 selected test methods:15 new B251 checks plus8 directly affected retained display checks. Coverage includes:

- Actual Lua all-four previews, ACTIVE fall/recovery, historical/sibling rows, localized numeric placement, zero and UNKNOWN, selected-city/Owner isolation and1000 duplicate notifications without rebuilding.
- Actual Store/request projection, detached scalar isolation, zero Store writes and zero cross-record uniqueness visits for the read, no lazy template capture, wrong-Owner rejection, uncertain history, failure isolation and reconstruction in a fresh fixture. This is no new native save/load claim.
- Lua5.1 compilation of six changed files; SQLite icon/text definitions;16unique icons, two DDS headers/dimensions/payloads, import closure and267-file package; reserved name/state widths and no new gameplay write/update hooks.

Command from repository root, using the existing local Lupa runtime:

```text
python -m unittest test_b251_institutions test_culture_institutions test_b236_entry_ui.IndustryInstitutions test_b247_ui_package.UI.test_current_and_legacy_institutions_render_without_old_active -v
```

Only directly affected UI expectations changed: future rows are now visible; Roman controls become icons; an obsolete Culture “not implemented” text assertion becomes the current Culture Insights description check. Unrelated package/version assertions and gameplay tests are not relaxed. Source and dependency review found no changes to writers, calculations, gameplay events or saved schema. No native CPU/memory improvement is claimed.

## Publication boundary

Two fixed DXT5 blobs were structurally and visually reviewed; their sizes/checksums and source mapping are in the [asset note](../../../../Art/Institutions/README.md). The user explicitly approved their one-time publication exception. They are committed separately with only those two paths staged; the checker reports NOT_RUN for binary content, not a false PASS. Binary-only commit: `d3582cf` (two indexed blobs rechecked against the approved SHA256 values). A command-local hook override applied only to that exact commit. All remaining source, SVG, test and document content must pass the unchanged normal staged gate. No persistent hook, rule, configuration or allowlist change; no raw screenshot/log/save is published.

## One minimal native UI flow

During the next normal session, open **城市详情 → 专业机构** in one lower-level and one advanced professional city: check all four icons/rows, preview versus established state, right-side current highlight and scroll/name spacing. Hover available **学术传统／商业信誉／时代对话／人文考察团／标准化／工程传统** entries to confirm the numbers sit below the right paragraph; Insights shows only the total count. Where normal play changes ACTIVE or an accumulated value, reopen the same city details and check the displayed value/state follows it. A narrow window or changed UI scale should keep names out of the right status column.

The new uncertainty is native atlas loading and layout/readability. No special progression grind, yield remeasurement, new lifecycle sequence or separate cold-start acceptance is requested. Local fixture reconstruction is sufficient for the unchanged persistence path. **USER_GAME_TEST_REQUIRED** for the new visuals; earlier gameplay acceptance and limits are inherited.

## Deployment and continuation

Local B251.278 source is ready for the normal reviewed commit/push and W0003 process/hash/receipt gate. Live remains B250 until the guarded switch is verified. Stable/main B069.96 is untouched. All S0669 playtest/deferred decisions remain; this patch neither advances nor closes held gameplay/audit work. Stop after deployment/current checkpoint for the user's next session.
