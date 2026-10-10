# B184.211 — isolated Spy=1 travel gate

Date: 2026-10-10. **LOCAL_SIMULATION_PASS; native travel/coexistence/ordinary-Spy isolation USER_GAME_TEST_REQUIRED. Gain Sources execution BLOCKED.** The user explicitly authorized this minimal Spy1/Gain Sources isolation prototype, with independent capacity/source and no ordinary-Spy changes. This is a partial technical gate, not formal N1, deterministic missions or a Design revision.

[Current slice](../../../Architecture/v2/P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) · [Prior native failure](Specialization_B183_Expedition_Spy0_Native_Review.md) · [Native/HD evidence](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#gain-sources-as-a-possible-task-template--user-follow-up).

## Implemented boundary

A dedicated non-trainable `UNIT_SPC_EXPEDITION_SPY` uses Spy1/Stackable1/IgnoreMoves1 and the Spy promotion class; it does not join CLASS_SPY or receive Spy abilities/promotions. Existing Builder art/icons are reused. Ordinary Spy rows, operations, probabilities, globals, HD callbacks, capacity and rewards are not edited. Spy1 still joins native classification: unchanged maximum capacity does **not** prove that used slots, native UI or all passive behaviors are isolated.

Gameplay owns one session's exact unit/source reference and own cap1, counting old fixtures too. A missing/off-map tracked unit reserves capacity. It validates current source/target and grants a one-shot travel permit. Only the UI calls the verified native `RequestOperation(SPY_TRAVEL_NEW_CITY)` API. No Gameplay PlaceUnit/FinishMoves fallback, guessed new identity, name adoption or automatic retry. Arrival requires the exact original Owner/type/ID at the target center; the estimated native travel+establish duration plus one publication/turn boundary is only an observation timeout, never proof of arrival. A changed/missing identity holds the experiment and preserves its binding record. END only destroys the exact visible owned prototype; it never guesses an off-map record or affects an ordinary Spy.

The UI explicitly reads native maximum, ordinary on-map Spy identity/operation fingerprints, off-map count and current source-city ordinary-Spy training availability before/after creation. Known changes or unknown maximum hold dispatch. Partial availability evidence is labelled PARTIAL, not full independence. These observations cannot reconstruct every native occupied/captured slot. Player-level completion events retain only a bounded count (99) and last operation, with attribution UNKNOWN; no name matching, reward reversal or permanent writes.

Source ACTIVE/Identity decline does not delete/rebind the team. Unknown/changed source reference or target stops continuation; there is no formal source reassignment. Exact source validation is inherited from `NetworkInput.Reference`, not a new city key. No production/mission reward, Store/Property write, persistent journey, GC change, N2/N3 or era UI. The prior Spy0 code/data and tests remain available but its runtime Start/UI registration are replaced; old fixtures are count/explicit-cleanup only.

## Gain Sources: why execution stays blocked

Native text describes automatic success/no mission risk; the native UI reads `GetSourceTurnsRemaining(city)` and raw outcome probabilities. Neither is a per-unit setter disabling the native intelligence effect. Current operations/global parameters belong to ordinary espionage too. HD's live completion bridge reaches a broad offensive-mission handler that excludes Listening Post/Counterspy, not Gain Sources, and includes Era Score plus conditional rewards. The popup's suppression of its rewards display does not suppress those effects.

This batch reads eligibility, current source duration and **undetected versus detected/escape** success separately. It never requests Gain Sources, changes global source strength, removes HD listeners, subtracts rewards after completion or clears another Spy's city-level sources. Even undetected=1 does not authorize execution. No safely verified per-prototype isolation path was found in the inspected surface; that is a bounded technical boundary, not a proof that all future methods are impossible. The user need not test an already-known unisolated mission. Reusing this mission as a future timer still requires a separately reviewed scoped route.

## Local evidence

**31 new methods +10 existing P0-panel methods PASS (41 total).** Actual Lua modules and window flow run in Lupa; SQL is replayed into an in-memory copy of the configured read-only gameplay DB. Unit/operation/global/modifier/ability rows outside the exact new unit remain unchanged. XML/art registration, bilingual keys, real source-to-UI routing and diff scope checked. Local simulations deliberately do not implement the closed engine's travel/collision behavior.

| Local counterexample / check | Observed result |
|---|---|
| Explicit create; duplicate token; old prototype already present; failed native spawn | Own cap/source maintained; no duplicate spawn; uncertain mutation holds |
| UI-only operation API; Gameplay lacks UI-only City:IsCapital | Native request is in UI after Gameplay's verified-capital permit |
| Native travel reject / request throws or returns false / repeated permit | No alternate move or retry; ambiguous request consumed and held |
| Unit absent during native travel; another ID appears | Cap remains reserved; no name/type-only reattachment or replacement creation |
| Same ID reaches exact target; ACTIVE falls | Original binding remains; ARRIVED; no Property/teleport/reward write |
| Source loss/token UNKNOWN; target changed | Hold; preserve unit and source record rather than invent recovery |
| Ordinary Spy/foreign unit submitted for END | Refused; only exact owned prototype cleanup succeeds |
| Ordinary-Spy training availability changes after create | Stop before dispatch; explicit prototype END remains available |
| Gain Sources raw undetected1 or missing getter/probabilities | Execution always blocked; missing data UNKNOWN, never fabricated0 |
| Closed UI, request timeout, shutdown, completion notifications | No automatic native request/retry; scoped callbacks removed; bounded diagnostic state |

Commands: `PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_expedition_spy_gate.py` (Lupa and configured read-only DB required), and `python3 DevelopmentTests/test_p0_panel_current_layout.py`. No unrelated gameplay/full/stress test or native PASS. Older package tests assert their frozen B183 version/art count; B184 package assertions above cover the new package rather than rewriting those historical assertions.

## One minimal native session

Use a test-save copy. After confirmed B184 deployment, open **专业化诊断 → 人文考察·验证**. This is the sole test control window; do not use the unit's ordinary Spy mission buttons. No new save/load cycle or normal Spy mission is requested.

1. 选中己方文化ACTIVE IV来源城。若窗口显示旧验证团，先点**结束并移除验证团**。可把一支普通平民留在市中心，然后点**① 创建Spy验证团**。确认同格单位仍在、容量1/1、来源城正确；查看普通间谍上限/数量/可训练状态。若出现变化或暂停，截图并结束，不继续派遣。新增信息：Spy1创建/我方共存及可读普通间谍边界。
2. 用**上一目标／下一目标**选一座已遇见且已揭示的外国主要文明首都，点**② 读取派遣与情报隔离**，再点**③ 原生派遣**。任务本身不会执行“获取情报源”。原生允许为否/未知或出现暂停时，保留报告并停止，不尝试其它间谍任务。新增信息：真实Spy1能否使用原生travel，读取情报状态是否可用。
3. 正常过到预计抵达时点，点**刷新报告**。确认原单位、目标市中心、原来源、容量1/1；若目标有其它单位，观察是否共存而无移动/俘获/伤害。不要为覆盖所有单位类型额外造复杂场景。再次点**② 读取派遣与情报隔离**保留到达后的只读状态；若接敌场景方便，可观察一次，否则敌军接触明确NOT_TESTED。新增信息：真正到达/同ID与所遇单位共存，未测组合不扩大PASS。
4. 到达且原单位可读时点**结束并移除验证团**，确认验证团消失、普通单位和原生间谍可读状态未受影响。途中离图/身份未知不能安全清理时停止并留报告，不猜新单位。新增信息：本次Spy1实体的精确退出；不重复共享保存/OFF验收。

截图仅需创建、到达（或首个错误）、END结果；用户可读报告足够时可直接反馈。若会话中普通间谍自己完成任务/改变状态，请注明；玩家级事件不能据此归因于本团。此前B180撤退PASS不替代本批无害共存证明。

## Deployment and stop

This report describes source B184.211/modinfo211. At local completion the last verified external package is B183.210 (202/202). Actual source/live identity and receipt are maintained only in [Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state); a source commit does not deploy. W0003 exit/clean-source/receipt/recovery gates still apply. Do not advance formal N1, N2/N3, rewards or another Spy route after this gate without user review.
