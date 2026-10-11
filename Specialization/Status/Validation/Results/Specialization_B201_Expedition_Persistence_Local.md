# B201 — persistent Expedition team and source recovery

Source checkpoint: **B201.228 / modinfo228**. **LOCAL_SIMULATION_PASS; native serialization/travel reconstruction and B200 rendered UI USER_GAME_TEST_REQUIRED.** Implements the user-approved [persistent-team/source slice](../../../Architecture/v2/P0_N_Expedition.md#next-proposed-slice--persistent-team-and-source-recovery). Includes the unchanged [B200 selection/card delta](Specialization_B200_Expedition_UI_Local.md). Last verified live before this source checkpoint is B199.226; deployment is a separately verified transaction.

## Applied boundary and source of truth

One bounded Game Property per supported player owns the cap1 team's logical identity, verified native name evidence, exact source reference, confirmed travel/task intent and generation/revision. `ExpeditionSpyStore` strictly validates a copied scalar envelope and reads back every changed write. No city-history schema or CityProgressionStore change. Native units, travel and activity remain current engine facts; cached samples, native permits, callback tokens, diagnostics and UI state are not saved.

Creation reservation precedes native creation; confirmed travel intent precedes its one-shot permit; a confirmed ARMED activity intent precedes one native SLEEP attempt; END intent precedes destruction. Failed/malformed/third-value readback quarantines the single team and keeps its capacity reservation. No automatic retries, duplicate creation, convenient-unit adoption or loss of ambiguous occupancy. END retains a bounded generation tombstone, preventing logical key reuse when the engine reuses UnitID. Unrecorded pre-batch units remain explicit-cleanup-only.

Loading restores created/naming/travelling/arrived/controlled task state. Arrival may replace UnitID only through the existing combined owner/type/verified native-name/unique-team/exact-endpoint evidence; name alone never establishes source or city identity. Source ACTIVE or Identity decline does not revoke the completed team. Changed source ownership/reference holds the task with old binding retained; free reattachment is a separate future slice.

Saved activity is masked as RECOVER until an independent UI context reads the exact current unit, position, native operation and activity. No request is replayed from saved ARMED intent. Observed SLEEP may confirm that intent; an uncertain outcome is held. A restored running task preserves its original due turn and cannot complete before fresh activity acknowledgement. Release needs fresh exact identity plus confirmed ownership; pre-existing unowned SLEEP is never woken. B194's bounded OPERATION-to-SLEEP observation remains; no native espionage mission or reward is started.

The Window correlates task acceptance using logical activityKey/teamKey plus its existing exact request token; it reports restored/unavailable persistence in the P0 diagnostic. New bilingual keys: `LOC_SPC_EXPEDITION_SPY_ACTIVITY_ARMED`, `...ACTIVITY_RECOVER`, `...PERSISTENCE`, and `...PERSISTENCE_ABSENT/CONFIRMED/RESTORED/UNAVAILABLE`. B200 layout and selection-only opening remain unchanged.

## Work and temporary-state lifecycle

Existing creation/explicit requests, own-player turn, load-ready and city-transfer observations inspect the recorded team/source/target. No new all-city/world scan, periodic UI diagnostic scan or GC change. Pending travel retains the existing owned-player unit collection check for arrival. Normal scalar publication skips unchanged views; persistence compares the bounded saved projection and skips unchanged writes. Gate owns one live record and bounded reservation; Store owns validation/readback; native engine owns physical state; UI owns disposable bridge/rows. Success, END or terminal hold retires pending actions; fresh context observation cannot replay a side effect.

## Local verification

**383 distinct targeted tests PASS**, using actual Gate, Store, activity bridge and Window Lua with independent mocked contexts. Existing read-only configured gameplay DB/package/SQL/XML checks are retained. Python3.14 and existing Lupa lua55; no dependency installation or external runtime writes. No broad gameplay/stress regression or native CPU/memory claim.

New coverage: Store20 strict schema/coherence/readback cases; actual Gate+Store47 reconstruction/fault/isolation cases; actual UI recovery21 cases; eight actual Gameplay-to-UI durable-ARM/cold-running/pending-OPERATION/recovery-failure counterexamples. Existing direct travel/name/source/task/activity/UI regressions are updated to the new confirmed ARM protocol, not weakened. Phase/mode coherence rejects a malformed saved running record instead of bypassing recovery. Independent final review found and corrected two new-path defects before deployment: terminal activity-recovery acknowledgement could stay consumed while still publishing RECOVER, and source binding could change during precreation/readback readers. Targeted actual-context counterexamples now verify terminal hold/fresh exact release and pre-side-effect source revalidation; final Store/Gate/Window review found no remaining blocking defect.

Checks include exact-value round trips, missing/corrupt/unreadable/third-value persistence, no-op/throwing writes, ambiguous interrupted create/END, native UnitID replacement, UNKNOWN/source loss, ACTIVE decline, owner/city/unit isolation, duplicate notifications, cap reservations, saved timers and one-shot completion, unowned sleep, fresh ownership before release, stale acknowledgements and no repeated native order. Full save-file serialization and real off-map native identity remain unproven locally.

Reproduce new tests with the existing dependencies in [test setup](../../../../DevelopmentTests/README.md):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s DevelopmentTests -p 'test_expedition_spy_store.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s DevelopmentTests -p 'test_expedition_spy_persistence.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s DevelopmentTests -p 'test_expedition_spy_recovery_activity.py'
```

Combined modules: the fourteen B200 direct suites plus `test_expedition_spy_store`, `test_expedition_spy_persistence`, `test_expedition_spy_recovery_activity`, `test_expedition_spy_activity_ui`, `test_expedition_spy_activity_integration`, `test_expedition_spy_activity_pending`, `test_expedition_spy_binding`. Raw combined result and SHA256 manifest are retained in ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B201/local/`. Document links, selectors, package registration, Runtime Index/Context Lock and reviewed diff complete this source checkpoint; they do not upgrade native evidence.

## One combined native session

After verified deployment, use the current test save/test civilization and one valid Culture ACTIVE IV source. This is the one genuinely new travel/cold-load boundary, combined with B200's deferred UI check; no second harness save/load ritual.

1. If an older one-shot probe remains, use P0 **人文考察·验证 → 结束并移除验证团**. Select the valid source and **① 创建Spy验证团**. Wait for normal preparation/source confirmation, then close the diagnostic window. Selecting the idle team at home should open **派遣到新城市** with no destination chosen. Choose a revealed foreign capital and **确认派遣**.
2. Save **while travelling**, fully exit and cold load. Use P0 **人文考察·验证 → 刷新报告**: the same source/name and cap1 reservation should be restored (persistence says restored), without a second team or replayed dispatch. Close the diagnostic window and continue to arrival; the source remains the original city even if native UnitID changes. A hold/error or missing evidence stops this path; preserve the report rather than creating a replacement.
3. Select the arrived team: **任务** opens with nothing selected. Choose **无奖励验证任务**. Check the card top stays inside/below the gold header and the old idle test instruction is absent. **开始任务** closes the sidebar; selection during its controlled activity does not reopen it.
4. After two player turns, completion should be1/1, activity released and no reward issued. P0 **结束并移除验证团** removes that team. This closes the newly persistent transaction; no repeat-mission test is implied.

## Held scope / evidence limits

Cap1, Spy=1, own source binding, test-civilization name pool, revealed-capital fixture and fixed2T one-shot no-reward task remain. The temporary native Spy-capacity cost remains accepted for the prototype; final own-cap-only behavior is not solved here. Normal training/current Spy cost, broader civilizations, source-loss reattachment, repeat missions/game-speed duration, N2/N3/U2/rewards are not implemented by this batch. Design, general Store, carriers, GC, main, deployment tools and frozen evidence are unchanged. No game launch or native PASS.
