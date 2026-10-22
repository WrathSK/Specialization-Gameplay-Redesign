# B185.212 — Expedition continuity and independent no-reward task

Date: 2026-10-10. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The user authorized this bounded batch and accepts the prototype occupying one native Spy slot. Formal N1 training/persistence/reattachment, N2/N3, rewards and era UI remain outside this checkpoint.

## New B184 screenshot evidence and accepted cost

Four images were individually reviewed and archived, with byte/SHA256 verification, to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B184/2026-10-10-capacity/`. The local `manifest.json` holds full original filenames, sizes and hashes. Prior B184 results/images are unchanged.

| Image time | Observed fact | Limit |
|---|---|---|
| 12.19.30 PM, T86 | Created ID3276829 at(62,33), source Edinburgh(Test)/393220; own cap1/1; maximum5→5, ordinary0→0, trainable yes→yes; immediate native classification0 | No normal Spy fixture; UI publication can lag |
| 12.19.37 PM, T86 | Same source/team, Sparta travel2+0T, allowed; sources0T, raw undetected1/escape0; classification1 | Gain Sources is only read, never requested |
| 12.20.00 PM, T86 | Native overview **间谍(1/5)** lists the custom probe; native destination chooser is reachable | Positive evidence of native slot usage; user accepts this temporary cost, not full espionage isolation |
| 12.22.03 PM, T88 | ARRIVED at(23,15), ID3342365, count1/1, co-located1, but unbound/source omitted; completion events0 | Repeats the continuity/report boundary; no END or task completion in this group |

The acceptance is limited to this prototype. Its own cap1/source binding remains independently enforced; native maximum/used slots are separate. No accepted Design text is silently changed to make Spy capacity the formal Expedition contract.

## Implemented delta and ownership

- [Gameplay gate](../../../../Mod/ExpeditionSpyGate.lua): creation writes one namespaced `SPC_N1_SPY_PROBE_ID` string to the exact owned unit and verifies readback. Session state owns the original source reference, creation ID, current native ID, dispatch and task timer. There is no player/city ledger write or native mission completion/reward call.
- Arrival requires a surviving exact marker, supported Owner/type, current destination/source references, exact returned-ID lookup and a unique prototype. Names, coordinates, a lone unit and arithmetic ID transformations are insufficient. A bounded destination-occupant read finds candidates; the marker proves continuity. One uniqueness scan runs on arrival, not every ordinary task turn. No marker is copied to a replacement.
- Missing, wrong, duplicate or unreadable markers retain source/capacity and stop at `NATIVE_IDENTITY_UNCONFIRMED`/the specific failure. This is a safe native gate, **not proof that Civ VI preserves unit Properties during Spy travel**. A marked but unbound loaded probe is not silently attached; explicit exact-unit END remains available.
- **④ 无奖励任务（2回合）** starts only after verified arrival and a fresh UI native-idle sample (`GetSpyOperation == -1`). Gameplay checks that getter additionally if exposed, without assuming the UI API exists there. Two player-turn boundaries complete one bounded session task exactly once. READ/foreign turns do not complete it. Closing the window does not own or stop the timer.
- Source/target loss, identity uncertainty, displacement or a readable active native mission hold completion. ACTIVE decline alone does not erase the source. No insights, Tourism, Era Score, Gold, native sources, experience or fabricated `SpyMissionCompleted` is granted. The fixed2T value is this test fixture, not a change to the formal speed formula.
- [UI reader/window](../../../../Mod/UI/ExpeditionSpyWindow.lua) report verified source, old/current IDs, due turn/completion count, source turns, current native operation and bounded **player-level** mission-event delta. Events are not attributed by name. Post-publication audit refresh is one-shot; UNKNOWN stays UNKNOWN. The accepted slot/off-map/trainability cost is displayed rather than misclassified as a failure of our cap.

## Spy UI reuse and isolation

**STATIC_CONFIRMED:** the native interface is reusable at its Lua/control boundary, but the original mission callbacks invoke native executors. A timer-only task can use the same presentation vocabulary without invoking those executors. This batch routes the exact custom type through existing native entry points into our current small window; it does not claim the full formal management UI is finished.

| Entry | Scoped change | Ordinary-unit behavior |
|---|---|---|
| [Unit panel](../../../../Mod/UI/ExpeditionSpyUnitPanel.lua) | Includes installed HD panel, uses native action-row builder; custom unit gets management + ordinary skip-turn only. Avoids building/registering native mission hotkeys first. | Original HD builder/callbacks are used unchanged for other types |
| [Spy chooser](../../../../Mod/UI/ExpeditionSpyChooser.lua) | Includes Expansion chooser; exact-type open/selection/confirmation/counterspy/mission and hot-reload entry redirect | Native destination filtering/rendering/callbacks preserved |
| [Mission popup](../../../../Mod/UI/ExpeditionSpyPopup.lua) | Filters custom briefing/cancel/renew before native private mission state is populated; captured mouse callbacks rebound | Ordinary mission/completion handling stays native; no shared listener removed |

Only our `Mod/` wrappers and registration change; native/HD files, normal Spy definitions, global parameters and reward listeners are untouched. The inspected native overview selects/routes the unit rather than executing its task itself. `WorldInput` does not supply a separate Spy mission executor in the inspected entry.

Native travel and skip-turn remain native operations; the **custom task** never requests `SPY_GAIN_SOURCES`, Listening Post, Counterspy or other native Spy missions, and never emits native mission completion. Therefore it does not deliberately enter HD's mission-completion reward hook. **That does not prove absence of every engine-side passive Spy effect, diplomacy/visibility effect, or third-party script action.** The inspected HD `Temp_Interface` completion bridge and `UnitAbilities` reward switch are evidence for the submitted-mission boundary, not universal immunity. UI filters are not a security sandbox against external cheats/scripts.

Future UI work can reuse the native destination rows, mission-card layout and remaining-turn presentation, replacing data and callbacks with our own task IDs/durations/rewards. Ordinary mission history/probability/escape/renew execution must not become the backend. That fuller UI and formal rewards require their own authorized slice; no external mod file is copied or edited here.

## Local validation

**67 methods PASS:**31 current Spy-gate/reader/window/package regressions +26 new identity/task/UI tests +10 existing P0 layout tests. Actual Lua modules are executed with Lupa; external loaded DB is opened read-only and copied to memory for the unchanged Spy SQL comparison. An initial run lacked the explicit DB configuration and failed that test; rerunning with the actual configured DB passed. No assertion was relaxed to bypass a missing dependency.

Coverage includes changed/aliased IDs with valid markers; absent/wrong/duplicate marker refusal; source/Owner/target/UNKNOWN isolation; cold-session refusal to invent binding; exact END and ordinary Spy protection; duplicate task/start/turn behavior; no city/player/reward/native-mission writes; timer progression while UI is closed; UI-only getter absence in Gameplay; no per-turn all-unit traversal after arrival; native primary/secondary action layout; exact UI routing and ordinary callback pass-through.

The inherited fixture now supplies real unit Property getter/setter behavior and counts **one exact owned-marker write** instead of the old no-unit-write assertion. No unrelated test or frozen result is changed. Gameplay DB definitions, normal Spy operations/modifiers/global parameters compare unchanged. Package/XML/localization/syntax, links/selectors/context and diff review are checked separately. These results do not certify native Property retention, rendering, idle rewards or timing.

## One minimal native session

Run only after B185.212 has been deployed. No save/restart ritual is requested: this batch does not implement saved task reconstruction. Start from the existing Culture IV fixture; if an old prototype remains, use **结束并移除验证团** first. Keep other Spy missions idle for this short comparison, because the event count is player-level.

1. **专业化诊断 → 人文考察·验证 → ① 创建Spy验证团**. Choose Sparta/the same available target, then **② 读取派遣与情报隔离 → ③ 原生派遣**. On arrival, **刷新报告**: source remains visible, marker verification succeeds, own cap1/1; a changed native ID is acceptable only with verified binding. If held/unbound, stop—this distinguishes surviving identity evidence from an unsupported engine transfer.
2. Select the team or its native **间谍** entry: it should route to our management window, without native mission choices. If a native mission list is offered, stop instead of executing one. Click **④ 无奖励任务（2回合）**, close the window, advance the two shown player turns; ordinary **跳过回合** is available if the team needs an order. This proves custom timing works without a native Spy mission or an open diagnostic panel.
3. **刷新报告**: completion1/1, reward none, current native operation-1; source turns remain0 if starting at0; native mission-event delta0 and no native/HD reward notification. Then **结束并移除验证团**, refresh after publication: own count0 and native used count returns to baseline. This checks the new task/identity cleanup boundary, not an unrelated full lifecycle suite. If an ordinary Spy is already available, its normal mission interface should remain accessible; do not create one or run a second campaign just for this check.

Any missing getter stays UNKNOWN; any marker loss, native mission UI escape, unexpected reward or ordinary-Spy disruption ends the gate and supplies the next specific boundary. Do not execute Gain Sources to prove a timer path.

## Checkpoint and stop

Source: **B185.212 / modinfo212**. External runtime remains last-verified **B184.211**, source3e9092c, receipt `B184.211-3e9092c-playtest.json`. A live Civ6 process was detected during this batch; **no deployment, game termination or launch** occurred. Existing recoveries/main/Design/Store/GC remain unchanged.

Next: after game exit, use the existing W0003 transaction for this committed source; then the single session above. Wait for its evidence before formal N1/N2/N3, rewards or another route. No automatic new phase.
