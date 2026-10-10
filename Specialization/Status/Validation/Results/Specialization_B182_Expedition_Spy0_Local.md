# B182.209 — N1 Spy=0 independent dispatch prototype

Date: 2026-10-10. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.** User explicitly approved the minimal Spy0-first prototype, with our own capacity and source-city binding. This is an isolated N1 native gate, not formal training, persisted Expedition state, N2/N3, rewards or the era UI. [Current slice](../../../Architecture/v2/P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) / [research](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md).

## Implemented boundary

- New exact `UNIT_SPC_EXPEDITION_ZERO`: Spy0, IgnoreMoves1, Stackable1, CanRetreatWhenCaptured0, CanCapture0, CanTrain0; no Spy tag or promotion class. Existing `UNIT_SPC_EXPEDITION_GATE` stays byte-identical in the unit SQL; native Spy/HD/other-unit rows are unchanged. Both fixtures count against our cap1. Existing Builder art/icon reused, no new visual asset.
- Explicit creation requires own Culture ACTIVE IV/current reliable binding and no pending investment. One Gameplay-owned session reservation binds exact unit type/Owner/ID to the existing source reference (Owner, CityID, coordinates and binding token via `SPCNetworkInput.Reference`), never name/location guessing. Later ACTIVE or Identity decline does not delete/rebind the team. Source reference loss pauses this gate and retains the unit; formal reattachment is not implemented here.
- UI reads native travel + establishment times for one chosen target, and independently queries `CanStartOperation(SPY_TRAVEL_NEW_CITY)` using the stock chooser's signature. It **never calls RequestOperation**, Gain Sources, a Spy mission or a Spy-completion event. UNKNOWN permission is distinct from false; neither changes the usable time getter's result.
- Explicit independent dispatch carries a same-turn/origin sample to Gameplay. Gameplay validates exact current foreign city/Owner/position, then owns the due turn. At due local-player activation it attempts `RestoreMovement → PlaceUnit → exact unit/target/source/occupant verification → FinishMoves`. Zero returned duration completes immediately; no invented minimum. The probe rejects invalid/noninteger/unbounded time (>1000 total), as a diagnostic safety bound rather than a new Gameplay rule.
- Only met, living, revealed foreign Major **capitals** are offered by this existing narrow fixture; ally/war status is not filtered. Formal Expedition targets remain unchanged. The prototype **waits visibly at its departure tile** until due; off-map representation and actual mission positions are not implemented. IgnoreMoves plus FinishMoves is the candidate movement lock, not evidence of complete native command immunity.
- Placement must reach the exact target center with the same unit/Owner. A maximum64-current-occupant probe checks prior units' Owner/type/ID/coordinates; it does not change those units. Failure/displacement/capture/unknown mutation pauses without retry, resurrection, nearby-tile fallback or forced correction. Occupant presence and unchanged coordinates alone do not establish combat immunity or every side effect; native observation remains necessary.
- END explicitly destroys only the chosen, currently owned exact fixture after a one-fixture check, including an old or unbound loaded fixture. No city/unit/player Property or Store write, reward, capacity modifier or permanent record. Unknown native outcomes reserve the session; duplicate tokens do not repeat actions, distinct duplicate dispatch is rejected without cancelling accepted travel.

## Ownership and update cost

| State / path | Owner and lifetime |
|---|---|
| Prototype unit | Native save owns the unit. Our cap includes every extant owned old/new fixture; no saved city history is synthesized |
| Source binding / due turn / stop | One Gameplay session record, replaced only by explicit CREATE/END; a stopped journey is not automatically restarted |
| Load boundary | Native fixture may survive, but this prototype's timer/binding is intentionally not saved. It remains capacity-consuming and cleanup-only; no inferred reattachment. Formal persisted travel is a later N1 batch |
| Current position / target / other occupants | Read from current native objects; no long-lived occupant cache |
| UI mirror / pending request | Existing matched token/reply and ten-second wait; window close does not stop Gameplay travel or resend a request |
| Regular work | At own player-turn activation, O(1) exact unit/source/target checks; placement once when due. Transfer notification rechecks the bound endpoints. No city/world scan per turn |
| Explicit reporting | Existing own-unit cap enumeration and selected-tile read; target list reads met Major capitals on open/refresh only. One last reply and saturated removed-event counter; no growing history or new GC |

## What actually needs Spy=1

| Component | Evidence now |
|---|---|
| Stock Spy chooser / native Spy overview membership | **STATIC_CONFIRMED:** direct `.Spy` guards in the installed chooser/overview. Reuse requires that flag unless those UI entry points are adapted; our own window is independent |
| Travel-time getter | B180 **READ_OK** on one Spy0 fixture. B182 reuses the getter on its new exact type; target-specific native result still needs observation |
| Our capacity, city binding, timer, window | No Spy1 dependency in these implementations; local tests cover nonzero human player, duplicate/failure/exit boundaries |
| Ordinary movement input | Stock WorldInput checks IgnoreMoves independently. Other command paths/order blocking still need this gate |
| Native Spy travel execution / off-map identity | **UNKNOWN**. B182 only reads eligibility, and false can have reasons other than Spy0 (including unit/target/movement state). It is not an A/B proof that Spy1 is required |
| Non-Spy foreign-center placement and harmless overlap | **UNKNOWN until native gate.** Stackable and PlaceUnit availability are not immunity evidence. Failure identifies this route's boundary, not automatic permission to enable Spy1 |

Read-only source checks: installed `Base/Assets/UI/Choosers/EspionageChooser.lua:606–618,630–639`, WorldInput IgnoreMoves checks, HD `Gameplay/Wonders.lua` selected-plot unit enumeration; current configured read-only Gameplay DB. The author-maintained [Lua notes](https://github.com/Hemmelfort/Civ6ModdingNotes/blob/master/%E6%96%87%E6%98%8E6_Lua%E6%89%8B%E5%86%8C.md) describe `PlaceUnit(unit,x,y)`; an [author's placement experiment](https://forums.civfanatics.com/threads/mountain-climbing-mod-failure-to-climb-lua-code-need-ideas-help.613949/) motivates restoring moves before placement and finishing them afterwards. These are API clues, not current native PASS. No external files were edited.

## Local validation

**62 N1 methods + 10 P0 panel methods PASS**, running actual Lua modules through the existing Lua55/Lupa setup; current external DB is copied read-only into memory for package assertions. Covers:

- nonzero supported player; current token/qualification; independent cap including old/unbound fixtures; stale/UNKNOWN samples and invalid targets;
- duplicate/reentrant create and dispatch; closed-window timer; exact once-only arrival; own-turn versus foreign-turn separation; bound source retained through ACTIVE/Identity decline;
- source loss, target change, unit disappearance/type/Owner changes, failed/no-op/wrong placement, displaced other unit, failed finish/destroy and no automatic retry/respawn;
- occupied source/target with unrelated units preserved in the simulation; explicit exact cleanup; loaded unit stays cap-counted and cannot guess its source;
- getter/permission separately readable, denied or UNKNOWN; stock-style parameter construction; no operation execution/reward/Property setter;
- both DB definitions, unchanged unrelated unit rows, localization in both existing locales, existing panel handoff/root visibility and captions, version209, seven art entries and actual icon SQL (the incomplete new INSERT/SELECT/FROM was caught and corrected during diff review).

Scoped Markdown links/anchors (52), current manifest selectors and the202-file/539-document integrity envelope PASS. Diff review confirms accepted Design, other gameplay modules/Store/GC, deployment tools, frozen evidence and main unchanged. Only named reviewed hashes were synchronized.

This verifies our state handling and call boundary, **not native travel/collision/AI behavior or engine performance**. Prior B180 retreat evidence remains valid for its old fixture; it is not reused as Expedition coexistence evidence. No gameplay-wide regression or repeated lifecycle native ritual.

## One minimal native session

Use a test-save copy; one continuous session suffices. UI: **专业化诊断 → 人文考察·验证**. If a prior gate unit remains, first use **结束并移除验证团**. Do not reload in the middle: persisted dispatch is deliberately outside this prototype, and reload only leaves an unbound cleanup-only fixture.

1. Select your Culture ACTIVE IV source city. If convenient, leave one ordinary civilian on its center. Click **① 创建原型**. Check cap1, source city, both units still present, and that right-click cannot walk the new team. This distinguishes independent input locking/own-civilian overlap from the old walking/retreat route.
2. Use **上一目标 / 下一目标**, then **② 检查原生接口**. Record the travel+establishment total and native operation eligibility. A denied native Spy operation is compatible with proceeding to our independent route; UNKNOWN **timing**, paused state or changed units stops the gate.
3. Click **③ 开始独立派遣**. Close the panel if desired and advance the reported number of turns. Click **刷新报告**: same team/Owner and source binding, cap1, exact foreign city center and ARRIVED are expected. Waiting visibly at departure is intentional in this probe. Zero time needs no forced extra turn. This tests real native placement rather than a getter-only result.
4. At the destination, observe overlap with foreign military/civilian units if present; preferably use an already available hostile-contact fixture. Check neither side is displaced/captured/destroyed and no new unit-orders blocker. A peaceful empty tile alone is **NOT_TESTED** for hostile coexistence; do not manufacture a long war test. Note which unit/contact categories actually occurred. Then **结束并移除验证团**, confirm only the fixture disappears and ordinary units remain.

If the route rejects placement, unit/Owner/position changes, another unit is disturbed or a blocker appears, **stop and provide the report + map**, without rebuilding, manual teleport correction or a Spy1 fallback. One screenshot at a discriminating state is sufficient; no forced save/END/cold-load/re-enable sequence, extra ability test or old retreat retest.

## Current limits and continuation

User approved this technical prototype first. The explicit mission-only/no-retreat Expedition decision is preserved in the plan/research; named formal Culture/Shared synchronization is still required **before formal N1 behavior**, not a new Design revision inferred from this test. Existing protected unit rules, all accepted Content, frozen evidence and other abilities remain unchanged. No full mission, formal production/cap concurrency, off-map travel, save reconstruction, reattachment, Era Score, N2/N3 or era UI is declared complete. After native evidence, identify the exact remaining primitive and obtain/observe the next batch's authorization; no automatic Spy1 switch.

## Deployment

Source `03a10723197d76d0ec7729e30670c7b4a45b19b3` / **B182.209 / modinfo209** deployed through the existing W0003 transaction after clean/pushed-source and OS game-exit checks. Receipt `B182.209-03a1072-playtest.json`: **DEVELOP_ACTIVE; 202/202 MATCH**. Exact B181 and stable recovery packages retained; no pending transaction. Main unchanged; game not launched and no new native PASS. Only the approved Spy0 prototype is deployed; no Spy1 switch or formal N1/N2/N3 continuation.
