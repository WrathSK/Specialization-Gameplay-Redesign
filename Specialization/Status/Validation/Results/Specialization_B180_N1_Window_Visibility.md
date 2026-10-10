# B180.207 — N1 hidden-parent correction

Date: 2026-10-10. **L1 UI-only correction within authorized N1. LOCAL_SIMULATION_PASS; native window/helpers/protection still pending.** No new Design, Gameplay, N2/N3 or era UI scope.

## Observed failure and diagnosis

One B179.206 screenshot visually reviewed: turn83, Edinburgh selected; the nine-button P0 layout and **人文考察·验证** entry are visible, with the seven requested diagnostics absent. The user reports that clicking closes P0 without opening a window. The click aftermath is user-reported, not independently visible in this still image. No test unit, travel or protection result is established.

The installed game's `Base/Assets/UI/InGame.lua:343–349` explicitly calls `LoadNewContext(..., isHidden)` with `isHidden=true` for InGame add-ins. B179 only calls `Controls.Window:SetHide(false)`; it never calls `ContextPtr:SetHide(false)`. A visible child cannot override its hidden parent. Existing working P0/CityPotential contexts explicitly unhide their root. This is a concrete source-level cause consistent with both B178's missing standalone entry and B179's invisible window; no native event trace or hit-test capture is claimed.

B179 also closes P0 immediately after checking an initialized-version flag, before proving that opening succeeded. The old local Window fixture modeled child visibility only and omitted root visibility; the P0 fixture used an assumed-success event. Their PASS did not cover this native loader condition. Current Modding.log records the N1 component applying; no Lua.log is available, and unrelated UI warnings were not attributed to this failure. Frozen B178/B179 results remain unchanged; this record corrects their coverage limit.

## Repair and scope

- N1 explicitly unhides root and child on open; close, Escape, unsupported-player exit and shutdown hide the whole context.
- The same UI event now publishes one version-scoped, transient open acknowledgement only after both controls report visible and initial READ setup succeeds. It is cleared before each request, on close and on shutdown. It is UI state only, never a Property or permanent record.
- P0 catches an opening error and waits for that acknowledgement before closing. Missing listener, stale acknowledgement, still-hidden context or exception keeps P0 visible with a short Chinese failure message. No automatic retry, unit creation or periodic visibility poll.
- Added localization key `LOC_SPC_EXPEDITION_GATE_UI_OPEN_FAILED` in the existing Chinese-first text table (both configured locales). All XML layouts, the seven hidden controls, N1 Gameplay/reader/unit SQL, ability code, Store, GC, Design and main remain unchanged. Modinfo/version stamp advances to207.

## Validation

- **41 N1 tests PASS; 10 current-panel tests PASS.** No gameplay full regression or stress run.
- Before the fix, the five added test methods exercised the original B179 sources: four methods failed (six failing/error cases including three open-failure subcases); the unchanged close-boundary case passed. After the fix all pass.
- Fixtures now start the N1 parent hidden, matching the inspected native loader. A new integration test executes the actual P0 and N1 scripts in separate Lua environments with shared event/state bridges: click → visible N1 root/child → close P0; only one READ, no CREATE. Fault cases preserve P0 for missing/throwing listener, stale acknowledgement and failed visibility.
- Existing explicit create/read/mark/END, pending-request continuity, qualification, isolation and exact test-unit cleanup checks remain passing. The configured external DB is opened read-only and replayed only into an in-memory copy, as before.
- Named context/hash and selector self-test, 44 scoped links/anchors, Lua/XML/localization, exact202-file registration and diff checks PASS; CURRENT remains10 lines. These verify source and local behavior; native rendering still requires observation.

## Minimal native continuation

After the corrected package is deployed, open **专业化诊断 → 人文考察·验证**. A separate window should appear with **① 创建验证考察团**. If it fails, P0 should remain open with a Chinese error; stop and send that screen.

If it opens, resume the same [N1 create/read/contact/END gate](Specialization_B179_N1_Entry_Repair.md#minimal-continuation). No new save/load or historical ability tests. N1 stays partial; no city production project, N2/N3, era UI or automatic next phase.

## Evidence archive

Original image moved byte-identically, unchanged filename, to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B179/2026-10-10/`. **1/1 SHA256 MATCH**, 12,252,129 bytes; no image committed.

| Original filename | SHA256 |
|---|---|
| `Screenshot 2026-10-10 at 9.13.44 AM.png` | `de3b72369415db8cf5339539a5b1fba71544cc9402b1d36a3dae650f4dee39f0` |

## Deployment

Source `42a66afc0aef8db2f30d84c2272919ce7cecd394` / B180.207 / modinfo207 deployed through existing W0003 tools after clean/pushed-source and repeated OS game-exit verification. Receipt `B180.207-42a66af-playtest.json` is **DEVELOP_ACTIVE; 202/202 MATCH**. Exact B179 and stable recovery retained; no pending transaction. Main unchanged; no game launch or native PASS.
