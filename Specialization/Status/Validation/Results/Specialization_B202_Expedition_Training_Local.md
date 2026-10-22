# B202.229 — Expedition normal training and source registration

Date: 2026-10-11. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.** Source checkpoint only; last verified live remains B201.228. No deployment, game launch, main promotion or native PASS in this batch.

## Implemented boundary

- Culture ACTIVE IV admission through normal city production. Native Unit cost/progress and distinct UnitType copy accounting are retained; no replacement project, manual production subtraction or spawned duplicate unit.
- One player-owned `TRAINING` phase extends the existing Expedition Game Property envelope. Save/readback of source reference, token and generation precedes a transient access building and one native BUILD request. A queued team reserves cap1 against another city or P0 CREATE; travelling/HELD/unbound surviving teams remain counted. Other unit entries retain native behavior.
- Completion requires the saved source reservation, confirmed queue, matching city/type completion event, and exactly one newly observed exact-type birth at that reserved endpoint. Both event orders and duplicate notifications are supported; multiple births, wrong city/reference, missing/corrupt readback and unknown outcomes hold capacity. This is an explicit normal-training causal contract, not adoption by nearest city/name/current location alone. An externally injected exact custom unit concurrent with matching native completion remains outside the normal-operation proof; extra candidates are rejected rather than deleted.
- Queue removal or replacement is an explicit native UI operation followed by fresh empty-queue/no-birth/no-completion checks. Empty queue alone does not release capacity. Unknown native order or interrupted half-receipt remains held; no refund/replay/duplicate spawn.
- Registration enters the existing NAMING state. An independent bounded UI observer checks native name pool/visible and off-map uniqueness, then asks the existing Gameplay NAME validator to confirm it. No P0 opening or rename command required. Existing source binding, travel ID replacement, task and END paths remain unchanged.
- Queue recovery checks the saved exact source and current queue; a missing UI reader gets at most12 publish opportunities. A saved incomplete birth/completion pair remains HELD. Existing B201 states retain schema1 compatibility; new TRAINING fields are additive and are not promised compatible with older packages.
- Auto-opening unchanged and non-blocking. Use **派遣到新城市 / 任务**. Test-civilization/name-pool restriction, temporary native Spy slot, revealed-capital target fixture and one-shot2T no-reward task remain; reattachment/repeat tasks/N2/N3 are not implemented here.

Ownership/work: Gate/Store owns the sole durable reservation/team record; Training owns one native queue/completion/birth correlation and one access marker; Production UI owns one pending handshake and selected-city view; name observer owns one10-second job. No new per-frame world/city scan, permanent building-history system or GC change. Relevant production events dirty only the reserved city; a player-turn/load/transfer fallback rechecks that single endpoint. Names are polled only during new-team registration. Admission checks current Culture IV; completed teams retain existing ACTIVE-loss semantics.

## Cost-source correction

The earlier preflight queried an obsolete outer cache (mtime2023-03-19), where Spy was80/10. That was **not current HD**. The installed Workshop HD `UpdateDataBase/DL_Units.sql:60–70` sets `Cost=60`, `COST_PROGRESSION_PREVIOUS_COPIES`, parameter15, Gold purchasing and Maintenance1. The current nested `Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite` (mtime2026-10-11) independently reads60/15. This agrees with the user-supplied wiki excerpt. No reliance on a wiki interpretation or vanilla constants.

HD DL_Balance loads at16010; our unit SQL at10001051 copies the resolved Spy **production** fields to a distinct Expedition UnitType. Native `GetUnitCost` supplies the current game-speed/ruleset quote. Ordinary Spy history does not become Expedition history. Gold240/+60 and Maintenance1 describe the quoted Spy; this batch does not enable Expedition purchases or invent an upkeep rule. Ordinary Spy definitions and HD files are unchanged.

## Verification

**437 distinct targeted tests PASS**: the21 direct B201 suites plus `test_expedition_training` and `test_expedition_training_ui` (54 new methods). Actual Lua Store/Gate/Training/production adapter/name observer are exercised. Coverage includes both event orders, long training and delayed UI queue publication, duplicate/competing requests, late/multiple/unrelated births, changed source, cancellation/no-guess behavior, failed/third-value saved state inherited tests, queue cold reconstruction, interrupted receipts, missing-reader fallback, stale ACKs, one-shot native ordering and automatic name binding without a panel. Existing travel/task/exit/UI tests retained.

Read-only current DB copied into memory for SQL tests: copied production fields equal UNIT_SPY, PurchaseYield remains null, exact building prerequisite registered, ordinary Spy/operations/modifiers unchanged. Package/SQL/localization checks cover new files/entry points and revised229 registration. Existing tests changed only the intentional CanTrain1/version229 expectation plus cost/prerequisite assertions. No gameplay-wide regression or native CPU/memory claim.

Raw result and SHA256 are retained under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B202/local/`. Run the two new suites with the existing Python3.14/Lupa lua55 setup; full module list is the B201 local-result list plus the two new suites. No dependencies installed. Context/schema/selectors, Markdown links and reviewed source diff are separate static checks; native queue timing/serialization remains unproven locally.

## One minimal native session after deployment

Use the supported test civilization, one Culture ACTIVE IV city and no surviving test team. If necessary use **人文考察·验证 → 结束并移除验证团** once to clear the old fixture; do not press 创建原型.

1. In normal production choose **人文考察团**. Check its native cost and that another eligible city cannot queue a second team. This tests the new admission prerequisite/queue path, not old travel.
2. While still queued, save and cold-load once; complete production normally. Verify exactly one team and the correct source in **人文考察·验证 → 刷新报告**. This one load tests the new TRAINING reservation plus native queue reconstruction; it does not repeat the already accepted travelling-team load test.
3. Use **派遣到新城市**, then **任务**, completing the existing no-reward task. Confirm source/cap stay correct. Explicit buttons are the acceptance path; selection auto-opening is not a gate. Stop if training/registration reports an error; preserve that report rather than creating another team.

User decision: no new decision needed. User testing: this one new native training/queued-load integration remains pending. Codex next: deploy only through existing authorization/safety gates when appropriate, then review evidence; do not start later Expedition missions.

## Deployment checkpoint

B202.229 / modinfo229 **DEVELOP_ACTIVE**, source `c61524e8d00735bc5b467929152e8c3350f2442f`, receipt `B202.229-c61524e-playtest.json`. Automatic OS process inspection confirmed game exit immediately before both existing-tool B201→stable→B202 switches. Source/runtime **218/218 MATCH**; B201 and stable recovery packages retained, no pending transaction. Main, game configuration and source unchanged; no game launch or native PASS. The source-only statement above describes the prior local checkpoint. Next: the single native training/queued-load session above. Automatic process inspection remains the normal gate; a running-game result defers that attempt rather than revoking standing authorization.
