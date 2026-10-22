# B197 — relocation stopped; original UI adaptation required

**USER_GAME_TEST_FAIL for submitted relocation; presentation not accepted.** All four originals were visually reviewed. No mission/arrival PASS is inferred. The user identifies images2/3 as the intended original presentation and confirms creating an ordinary Spy after the Expedition to inspect its UI, selecting a city for preview without issuing orders.

## Evidence

| Image | Observation | Boundary |
|---|---|---|
| 1, T86 | Expedition艾莉森, sourceEdinburgh(Test), 待派遣; left sidebar lists four capital targets with斯巴达 selected and confirmation available | Rendering/opening/initial selection reached; not evidence of travel submission. |
| 2/3, T86 | Ordinary Spy阿梅尔; selected-city header, compact city rows/travel/district strips, adjacent mission drawer, confirm/cancel footer | User-designated visual references. They are not our mission execution or native reward leakage. |
| 4, T86 | Expedition艾莉森 still at source, 亚历山大 selected; 已暂停 and `ISOLATION_OR_REQUEST_STOP`, confirmation disabled | Terminal guard failure observed. The sidebar hides the underlying detail; no completed dispatch/arrival/task gate. |
| User recollection | Ordinary Spy created between Expedition creation and failed relocation; no orders issued | This is sufficient to change the ordinary-Spy audit fingerprint. No mission order or city preview is needed to reproduce the recruitment-triggered change. |

## Relocation cause and confidence

A **confirmed existing guard defect**, strongly corroborated as this run's trigger:

- [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua):345 captures `before=R.Audit(...)` only at UI CREATE;230–233 keeps comparing against it;353–355 issues STOP on any later CHANGED/UNKNOWN.
- [Reader](../../../../Mod/ExpeditionSpyRead.lua):71–105 includes ordinary-Spy ID/type/current operation and native capacity in that comparison. An additional ordinary Spy is enough; no mission order is required.
- [Gate](../../../../Mod/ExpeditionSpyGate.lua):361–364 converts STOP to HELD / `ISOLATION_OR_REQUEST_STOP`. This is an over-broad isolation check, not evidence that source binding or native travel itself failed.
- The code predates B197; Gate/Reader/UI wrappers and this comparison are unchanged from B196. The new sidebar still passes the selected owner/city ID to the existing adapter.

Bounded reproduction uses current actual Gate/Read/Window Lua plus existing isolated native fixtures, creating via the real UI button:

| After UI CREATE | Result | Native travel calls |
|---|---|---:|
| No unrelated change | TRAVELLING | 1 |
| Change ordinary Spy operation | HELD / ORDINARY_SPY_PREFLIGHT_CHANGED | 0 |
| Change native Spy capacity | Same | 0 |
| Create another ordinary Spy | Same | 0 |

The four cases were executed without editing repository source/tests. Reproduction script/raw output are retained with the ignored local evidence. User-reported ordinary-Spy creation matches the last case. The exact native error-detail suffix was not captured, so this is source/local proof plus corroborating native sequence, not a raw native trace proving every operand. Available configured UI/GameCore/UnitOperations logs contain no underlying STOP detail; no extra test is requested solely to obtain it.

**Test gap:** `normal_window()` in [existing UI tests](../../../../DevelopmentTests/test_expedition_spy_actions_ui.py):132–138 creates through direct `req('CREATE')`, bypassing Window CREATE and leaving its `before` unset. The prior145 local passes remain factual but do not cover this stateful guard. The next regression must exercise actual UI creation and unrelated Spy changes.

## Why the visual result differs

There is **no demonstrated engine barrier to adapting the original visual hierarchy**. B197 reused textures/ChooserAnim but simplified the composition into summary + instructions + plain city rows + a large feedback footer. It omitted the selected-city slot, layered banner, compact district/travel information, adjacent preview drawer and confirm/cancel pair. This was an implementation choice, not necessary gameplay isolation.

The existing [native UI investigation](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#b196-follow-up--native-relocation-and-mission-presentation) already supports XML/presenter reuse. Installed Base XML has selected-city/list/card/drawer components; installed Better Espionage Screen keeps the left list visible with a neighboring mission panel at x296. Images2/3 are consistent with that BES composition; actual resolved provider is not proven by resemblance alone.

The real boundary is the **controller callbacks**: raw native mission population/briefing/acceptance can execute espionage; raw travel confirmation bypasses our Gate permit. Reuse layout, textures, geometry, banner/card presentation and neutral display helpers, while routing selection/confirmation through our existing adapters. Do not import native espionage missions to obtain their visual style. Keep ordinary Spy UI untouched.

## Next scoped repair proposal

1. Retain creation-time isolation and exact team/source/target/current-turn/permit/native eligibility guards. Remove the lifetime ordinary-Spy snapshot as dispatch permission authority; bound any dispatch comparison to its own action, with unrelated later changes diagnostic-only. Do not blindly reset the snapshot to make every comparison pass; actual native submission rejection/unknown outcome remains protected.
2. Add actual UI-create regression cases for unrelated Spy recruitment/mission/capacity changes, plus existing stale unit/target and native failure guards. Improve the normal failure reason to distinguish audit change from travel rejection; keep raw detail in P0 diagnostics.
3. Faithfully adapt the original selected-city header, compact city-row hierarchy, adjacent preview/task drawer and confirm/cancel controls in our independent context. Move diagnostic/prototype explanations out of the main visual hierarchy. Existing target scope remains capital-only; native all-city list is a visual reference, not target expansion. Any time/district preview must use bounded explicit-open/selection reads, never new turn/frame scans or native mission enumeration.
4. Keep explicit **派遣到新城市 / 任务**, our no-reward2T task, capacity, source/name binding, travel adapter and task/activity lifecycle. No new rewards, repeatability, formal training/persistence/reattachment, N2/N3 or era UI.
5. After separate implementation approval, one combined continuous session: relocation while the ordinary Spy exists, then arrival/task-card confirmation and existing task completion. Check the reference layout and ordinary-Spy delegation incidentally; no shared save/load/name/capacity campaign or repeated unchanged B197 test.

## Archive and package

Four originals moved without renaming/overwriting to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B197/2026-10-10/`; pre/post SHA256 matched. Local manifest includes roles, user recollection and reproduction hashes. No raw screenshots or external logs are committed.

Last verified live remains **B197.224/modinfo224**, source `daaa97ff2f6320bd8c04401f8ce17ec9dd7e8588`, receipt `B197.224-daaa97f-playtest.json`;213/213 equality and B196/stable recovery are inherited from deployment, not re-inspected here. Documentation/evidence review only: Mod, Design, tests, main, external runtime and frozen prior results unchanged. No repair or redeployment in this checkpoint.

- Image1 (B197_TEST): `Screenshot 2026-10-10 at 11.38.57 PM.png`, 14120910 bytes, SHA256 `6ccd5209be59d279324c4c25bd8573bea46326e6945e100f7f302da728358741`.
- Image2 (UI_REFERENCE): `Screenshot 2026-10-10 at 11.39.34 PM.png`, 13194291 bytes, SHA256 `342676f78aa27b592afb71e90281e8593905d09215889768f43cdd0345345949`.
- Image3 (UI_REFERENCE): `Screenshot 2026-10-10 at 11.39.40 PM.png`, 12109837 bytes, SHA256 `0f5e3be23ca3ada7fe82868e87b3bfbeea9b2cd86452fb89bc4806835fb2547f`.
- Image4 (B197_TEST): `Screenshot 2026-10-10 at 11.40.32 PM.png`, 14020444 bytes, SHA256 `87f1458061c99520a4c9813e3fb5ad751dd08064e9d8817e993ec3b3b1b03eaa`.
