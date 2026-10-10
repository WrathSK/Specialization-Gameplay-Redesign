# B183.210 — Expedition Gameplay-context correction

Date: 2026-10-10. **LOCAL_SIMULATION_PASS; native arrival and harmless coexistence remain USER_GAME_TEST_REQUIRED.** The user authorized the API-context repair and useful failure reporting, explicitly retaining Spy0, independent capacity and source binding. This is an isolated N1 prototype correction, not formal N1 or a Design revision.

[Current slice](../../../Architecture/v2/P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) · [B182 native counterexample](Specialization_B182_Expedition_Spy0_Native_Review.md) · [Unchanged prototype scope](Specialization_B182_Expedition_Spy0_Local.md).

## Cause and narrow correction

The Gameplay target validator invoked UI-only `City:IsCapital()`. Its local mock incorrectly supplied the method, so the old green tests did not expose this context mismatch. B182 native screenshots reported API_UNAVAILABLE without an exact stack trace; the source defect and local reproduction are confirmed, while the exact screenshot exception is not retrospectively invented.

Gameplay now uses `player:GetCities():GetCapitalCity()` and validates that returned capital's current Owner/ID/coordinates against the selected current city. Missing/unreadable capital or a changed endpoint rejects the action before starting the timer. The UI-only reader legitimately keeps `City:IsCapital()`; no native Spy operation is submitted.

Failure reports show a Chinese failure stage and bounded technical detail (maximum220 bytes, control characters and UI markup removed), alongside whatever unit/count/source readback actually succeeded. A held source is explicitly a recorded source, not a fresh validation or reassignment. Failed snapshot readback is UNKNOWN, never a fabricated zero-team count. A failed mutating arrival stays HELD with its original diagnostic visible after refresh; it never retries placement automatically. Error details are one session record/last reply, not an accumulating log in saved state.

Unchanged: Spy0/IgnoreMoves/Stackable unit definition, our cap1, exact source reference/token, native timing getter, own session timer, departure-tile wait, exact PlaceUnit route, occupant protection, mutation reservation, END and loaded-unbound cleanup. No Property/Store writes, new listeners, city/player scans, reward, Spy capacity changes, Spy1 fallback, GC or external Mod edits. Normal training, persisted journeys, reattachment and N2/N3/U2 remain out of this batch.

## Local evidence

**71 N1 methods +10 existing P0 panel methods PASS (81 total)** using actual Lua modules in Lupa, in-memory SQL replay from the configured read-only DB, XML/localization/registration checks and the two real UI contexts. No game launch or gameplay-wide regression. Documentation validation passes: 55 scoped local links/anchors, P0-N1 context/schema/selectors, 202 runtime review entries and 541 guarded files; CURRENT stays10 lines. Diff review confirms unchanged Design, frozen evidence, unit definition, native reader, shared facts/reference, Store, GC, tools and main.

| Check | Result / evidence boundary |
|---|---|
| Same context-faithful fixture, with no Gameplay `City:IsCapital` | Old B182: CREATED/API_UNAVAILABLE, dueTurn absent, count1/source1/placeCalls0. B183: TRAVELLING, dueTurn83, no error, same count1/source1/placeCalls0 |
| Normal timer/arrival with corrected API | Same unit40 reaches exact target at due turn, source1/count1 retained, one placement; local simulation only |
| Missing getter, no capital, different capital | Rejected at CAPITAL before timer/placement; known source/unit/count retained |
| Unclassified API exception | Failure stage, reason and bounded original detail retained without claiming native API success |
| Placement exception then repeated turn/refresh | HELD, one placement attempt, no retry/recreation/property write; source marked recorded |
| Snapshot failure | Count unknown in reply/UI; never displayed as0 |
| Existing safety regressions | Cap, exact source token/Owner/endpoint, target change, duplicates, occupant mutation, no native operation, explicit END and loaded-unbound behavior retain their existing local checks |

The counterexample loaded baseline source from Git in memory; no old source checkout or runtime edit. The committed context-faithful regression preserves reproducibility. These tests establish code behavior under explicit fixtures, not native immunity or successful foreign-center placement.

New localization uses the existing `LOC_SPC_EXPEDITION_GATE_` namespace: `FAILURE_STEP`, `FAILURE_DETAIL`, `READBACK_UNKNOWN`, `SOURCE_RECORDED`, plus `STEP_REQUEST/READ/CREATE/DISPATCH/TARGET/CAPITAL/ARRIVAL_CHECK/RESTORE_MOVEMENT/PLACE_UNIT/ARRIVAL_VERIFY/END/TURN/REFERENCE`. No new control, icon or visual framework.

## One minimal native session

只用一座已有文化ACTIVE IV来源城、一支验证团和一个已遇见、存活、已揭示的外国主要文明首都。沿用B182已有环境；不重复旧能力、保存启用态／冷重启流程。

1. **准备与派遣：** 选来源城，打开 **专业化诊断 → 人文考察·验证**。如果旧档带着“未绑定”或旧验证团，先点 **结束并移除验证团**，再点 **① 创建原型**；这是会话原型重新建立，不是要求测试保存机制。用 **上一目标 / 下一目标** 选目标，点 **② 检查原生接口 → ③ 开始独立派遣**。预期显示在途和到达回合，来源城不变、数量1/1、Spy容量不变。原生Spy派遣“拒绝”仍是独立诊断，不应阻止本原型的独立派遣。
2. **到达：** 按报告的实际剩余回合过回合，可关闭窗口。到期点 **刷新报告**：同一团应出现在所选城市中心、显示已到达，来源/Owner和数量1/1保持。等待中留在出发格是当前原型行为。新增信息：修复后是否真正通过原生精确放置，而不只是getter/timer成功。
3. **无害共存：** 在同一次测试中观察实际军事单位和普通平民单位同格（可利用已有占用或Cheat布置；标明实际是己方、外国和平或敌对）。确认团和另一单位均不消失、捕获、转Owner、撤退或被挤到邻格。报告同格数量只能辅助判断，不能代替这些观察；未能制造的关系/单位类型记“未测”，不为补齐而开长测。新增信息：Spy0/Stackable在实际遇到的原生接触中是否满足无害共存。
4. **结束：** 点 **结束并移除验证团**。数量回0，刚才同格的其它单位仍在，Spy容量不变。此处检查本次新到达/重叠位置上的定域清理，不要求再次启用或冷加载。

若出现失败、无法读取、放置到邻格、团或其它单位消失/易主/撤退，立即停止该路径，提供地图与本窗口同一张截图（必要时滚动看“失败环节／技术详情”）。不要重复点击派遣、改成Spy1或强行修正位置。正常结果可直接描述，无需逐回合截图。到达未通过时，不把共存标记为失败或通过。

## Source and deployment

Source **B183.210 / modinfo210** locally complete. Recorded live package remains **B182.209**, source03a1072/receipt `B182.209-03a1072-playtest.json`, until a separately verified W0003 transaction is recorded below. Main and frozen B182 evidence are unchanged. No new native acceptance is recorded by this implementation.
