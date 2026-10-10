# B180 native gate result / B181.208 panel repair

Date: 2026-10-10. B180.207 observed package; B181.208 is the authorized presentation-only correction. **N1 remains partial.** The user requests research and a modification plan for mission-only movement and non-interacting coexistence, not implementation of that new route. Era UI, N2 and N3 remain held.

## Native evidence

All six screenshots were visually reviewed. The subsequent user answer explicitly confirms that enemy contact caused the marked unit's displacement, without manual movement or teleportation.

| Images | Observed facts | Conclusion and limit |
|---|---|---|
| 1 | T83, Edinburgh selected, independent N1 window visible, test count0/1, target Sparta | B180 root visibility / P0-to-window handoff **USER_GAME_TEST_PASS** in this scene |
| 2 | T83, one own team ID3080221 at(62,33), Spy capacity5→5 | Explicit non-Spy creation and unchanged reported capacity **USER_GAME_TEST_PASS**; not formal production/cap accounting |
| 3 | T83, Sparta travel2 + establishment0 = total2; unit remains(62,33) | Native helper **READ_OK** on this actual non-Spy fixture/target; no remote dispatch or timer executed |
| 4 | T83, ID3080221 marked at(66,24), movement0/4 | Before-contact reference; not independently a capture event |
| 5–6 | T84, team near Stirling, ID3080221 still original Owner at(68,33), Spy capacity5→5 | Together with the user's explicit contact confirmation: **USER_GAME_TEST_PASS for this native retreat case**. No universal destination, war, religious immunity or all professional-unit guarantee |

END was not observed. Save/load was not part of this delta and is not retroactively claimed. No additional END, retreat or cold-load test is requested now. The retreat evidence is retained for future relevant units; it is **not acceptance of retreat as the clarified formal Expedition behavior**. B180 does not implement mission-only movement, same-tile immunity, formal training/source binding, missions, Insights or rewards.

## Window defects and narrow repair

The screenshots show blank arrow buttons and the right target control protruding outside the window. The XML used glyph-only ◀/▶ labels and40×30 controls styled as `MainButton`; installed `Base/Assets/UI/Civ6_Styles.xml:588–600` sets that style's minimum to80×41. This directly conflicts with the allocated arrow slots. The exact missing-glyph/font cause was not separately instrumented.

B181 uses the existing `MainButtonSmall` style, explicit100×32 target controls at x18 and502 inside the620-wide window, and a centered360-wide target label with12px clearance on both sides. All eight buttons use the small native style appropriate to their declared height. Visible localized **上一目标 / 下一目标** replace the glyphs. The only new localization keys are `LOC_SPC_EXPEDITION_GATE_PREVIOUS` and `LOC_SPC_EXPEDITION_GATE_NEXT`, in the two existing locales.

Copy is shorter: **创建验证团 / 刷新报告 / 读取派遣耗时（不移动） / 记录原型位置 / 结束并移除验证团**. It explicitly identifies the existing walking/retreat unit as the old prototype and stops prescribing another enemy-contact test. UNKNOWN, failed creation/removal, exact unit/reference observations and read-only timing scope remain visible. Existing request dispatch, root acknowledgement, callbacks, pending timeout, helper reads and exact END behavior are unchanged.

Changed runtime files: `UI/ExpeditionGateWindow.xml`, `UI/ExpeditionGateWindow.lua`, `Text/ExpeditionGate.sql`; `Probe.lua` and modinfo carry the B181.208 stamp. `ExpeditionGate.lua`, `ExpeditionGateRead.lua`, unit SQL, permanent state, gameplay effects, GC and Design are byte-unchanged.

## Local validation

**42 N1 methods + 10 P0 methods PASS.** The new target-layout/caption regression fails against the original B180 layout and passes with the correction. It checks native-style sizing, inside-window bounds, label clearance and actual Lua caption initialization. Existing actual two-context opening, explicit create/read/mark/END, failure/UNKNOWN, bounded request and owned cleanup tests remain passing. Database replay uses a read-only external DB copied into memory; no live DB changes.

The passing package checks include XML, localization and source registration. Scoped review checked 52 document links/anchors across the 17-file batch; Status CURRENT remains 10 lines (1,526 bytes). Named context/hash/selector checks PASS (202 runtime files / 538 guarded documents); helper self-test PASS (15 cases). These checks establish repository consistency, not new native behavior. No full gameplay regression, game launch or new native PASS for B181 rendering. Visual scale/font behavior still needs an incidental glance when the user next opens **人文考察·验证**, not another N1 lifecycle session.

## Research and next boundary

[Movement/coexistence investigation and proposed sequence](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md). Existing Culture already rejects map walking, but its direct-capture reference and Shared D0045 explicitly prescribe retreat. The latest user clarification replaces that protection mechanism for Expedition alone. The plan records the exact formal-sync boundary; current Design files are not silently rewritten and the new route is not implemented. No generic religious/Spy flag is declared sufficient.

## Evidence archive

Original filenames retained under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B180/2026-10-10/`. **6/6 SHA256 MATCH**; no screenshot committed, no duplicate retained in the inbox.

| Original filename | Bytes | SHA256 |
|---|---:|---|
| `Screenshot 2026-10-10 at 9.23.00 AM.png` | 13314405 | `fcd8366827cc5c6b8bcebeaccf4858b9abdaea825b35a4cfbf856e31095140ee` |
| `Screenshot 2026-10-10 at 9.23.12 AM.png` | 13296753 | `effcd82466944725c7ab3a4838615482c31bfd26c5d4ee77ea048e99c843ecfc` |
| `Screenshot 2026-10-10 at 9.23.50 AM.png` | 13851897 | `84db0f9717aca90b05d53b561384550f694cf0b4639b1e5a3e65e4ca2463744c` |
| `Screenshot 2026-10-10 at 9.25.16 AM.png` | 13480814 | `444fa3d56910387986b5f41af0398b4e0d2ed633b11009bd2aa6912e7d8a3c35` |
| `Screenshot 2026-10-10 at 9.26.03 AM.png` | 15112693 | `6b7acb9d06c7db7668a155bfc9d2a5cb00c8fec1041a6d05248fce1129d6fa3c` |
| `Screenshot 2026-10-10 at 9.26.24 AM.png` | 13454175 | `362d8446907aa08e4c8276a68b77acbcf3ba5ac55e3a23b6fa98d91767595763` |

## Deployment

B181 source is locally validated; deployment is separate and requires the existing W0003 clean/pushed-source, process-exit, receipt/hash/staging/recovery checks. Until a new verified receipt exists, live remains B180.207, source42a66af, receipt `B180.207-42a66af-playtest.json`. No deployment follows merely from editing this report.
