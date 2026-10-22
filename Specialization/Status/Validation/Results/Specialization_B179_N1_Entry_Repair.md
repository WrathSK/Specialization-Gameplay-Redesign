# B179.206 — N1 entry repair and temporary diagnostic visibility

Date: 2026-10-10. User requested correction of the missing N1 entry and hiding the seven red-boxed controls. **L1 presentation repair; LOCAL_SIMULATION_PASS, native entry/gate observation pending.** Gameplay, accepted Design, N2/N3 and era UI scope unchanged.

## B178 observation and cause boundary

One screenshot visually reviewed: P0-B-178.205, turn83, Edinburgh selected, Culture4 badge. The P0 panel is visible; no N1 entry is visible. User reports no matching button/project. **ENTRY_BLOCKED**: no travel/helper or unit-protection observation occurred; B178's local checks do not prove native UI rendering.

The new HUD entry had fixed screen offset8,156. In contrast, the two visible existing entries reparent next to WorldTrackerHeader at header-width+8. This establishes an inconsistent anchoring path and likely occlusion in the reported layout, not a captured native hit-test trace. The test unit is present with CanTrain0/Spy0/CanRetreatWhenCaptured1 in the configured current read-only DB, and the five relevant deployed entry/package files match source. Modding.log records the N1 components applied. No Lua.log is available in either established log directory; no claimed Lua-exception diagnosis. Unrelated database/UI warnings were not attributed to N1.

No ordinary city project was intended in B178: its unit is explicitly created by the test window. The old handoff's entry path was unusable in the reported layout.

## Minimal repair

- Entry is now **专业化诊断 → 人文考察·验证**, bottom right of a compact three-by-three panel. It opens the same independent N1 window; opening does not create a unit. The separate fixed-position HUD entry is removed.
- The window initializes through ContextPtr's init handler, registers one UI event, and publishes a version-scoped UI-ready flag only after initialization. P0 shows a readable error if the window is not ready. Shutdown removes the exact listeners/readiness flag and closes only UI; it does not destroy a unit or cancel an accepted Gameplay request.
- Eight window controls use explicit white child-label captions, matching the working P0 style. The old style-owned button String was not relied upon for rendering. No new art, project, native operation or travel formula.
- Hidden on request: **跨学科研究、科研基础设施、学以致用、标准化模板、主持／学术传统、移民／施工队、写入诊断日志**. Their XML controls, captions and callbacks remain; only visibility changes. They can be restored when needed without recreating module logic.
- Retained visible: 城市专业／潜力、总督条件、专家与岗位、巨作事实、风雅熏陶、意义延展、巨作启迪报告、时代对话、人文考察·验证. Report area increases from380 to460 logical pixels without resizing the existing panel.

## Local verification

- **38 N1 tests PASS**: existing gate/reader protections plus actual XML controls, single initialization, UI-ready lifetime, shutdown, supported-player visibility, explicit captions, request timeout and accepted-request continuity.
- **8 current panel tests PASS**: exact nine visible entries after the entire initializer; all seven hidden handlers retained; three-row rectangles/report do not overlap; read-only Inspiration/Dialogue/Meaning callbacks; unavailable/ready N1 routing without Gameplay mutation.
- Current-panel tests now assert the current read-only Inspiration/Dialogue UI, replacing two obsolete expectations for the retired manual Inspiration buttons. This is a reviewed update of this task's current UI contract, not a change to frozen historical tests or previous results.
- SQL replay uses the configured external DB read-only, copied to memory. Only the exact existing gate-unit rows are removed inside that disposable copy before replay; all other Units rows remain compared. No external DB change or new Gameplay SQL.
- Lua/XML/localization and exact 202-file registration PASS; current context/integrity, independent-selector self-test, all 44 scoped links/anchors and diff review PASS. Native rendering remains USER_GAME_TEST_REQUIRED; local rectangles cannot certify font/UI-scale or engine behavior.

## Minimal continuation

Use the same test-save copy; no repeated ability, save/restart or unrelated lifecycle gate.

1. Open **专业化诊断**, then bottom-right **人文考察·验证**. If a not-ready error appears or the new window fails to open, stop and provide that screen.
2. Select Culture ACTIVE IV with an empty civilian slot in its center; **① 创建验证考察团**. Then choose a revealed met foreign Major capital and use **② 读取远程耗时**. Report numbers or UNKNOWN; the unit intentionally stays in place.
3. If an enemy-contact fixture is available, position the unit and use **③ 标记接敌前位置**. After actual enemy contact, **刷新／读取保护结果** checks retention of the same owned unit and its retreat. Missing suitable contact remains NOT_TESTED; do not prolong the session just to manufacture it.
4. **结束并移除验证团** cleans up the one test unit. Disappearance/Owner change/uncertain-create errors stop the gate; do not recreate it to hide evidence.

Steps2–4 are the still-unexecuted [B178 gate](Specialization_B178_Expedition_N1_Gate_Local.md#one-minimal-native-session), not extra tests. There is no city production-list project in this gate. Formal training/remote deployment/source/archive binding remains later authorized N1 work after route evidence; N2/N3/era UI remain held.

## Evidence archive

The original PNG was moved without renaming or re-encoding into ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B178/2026-10-10/`. **1/1 SHA256 MATCH**, 11,292,869 bytes. No screenshot is committed. This table is the evidence manifest.

| Original filename | SHA256 |
|---|---|
| `Screenshot 2026-10-10 at 8.56.46 AM.png` | `39cb77db09ef1a682e9e36172451cc186a9cf6205cef90795c65d6e133dedd88` |

## Deployment

Source `579593581a1cca0480baf4e570da558bb34d6852` / B179.206 / modinfo206 deployed using existing W0003 tools after clean/pushed-source and OS game-exit verification. Receipt `B179.206-5795935-playtest.json` is DEVELOP_ACTIVE; **202/202 MATCH**, exact B178 and stable recovery retained, no pending transaction. Main unchanged; no game launch or native PASS.
