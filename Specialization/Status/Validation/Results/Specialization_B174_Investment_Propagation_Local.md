# B174.201 — scoped post-investment updates

Date: 2026-10-09. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED (combined later).**
Source baseline: accepted B173 checkpoint `4a62deb6b0657569b2cf3660c409fb8a5d814506`.
Scope: approved [investment propagation repair](../../../Reports/Proposals/Investment_Update_Propagation_Repair_Plan.md), IA-P13a-F03 only. No new Gameplay rule, save schema, GC policy or general dispatcher.

## Result and ownership

`InvestmentAction.Confirm` keeps its existing text result and adds call-local evidence: COMMITTED, ALREADY_COMMITTED, REJECTED or UNKNOWN. Only a new receipt with exact final ledger readback, current authoritative facts and matching reference/binding can produce COMMITTED. Debit alone, an INVESTED string or raw saved bytes behind a held Store are insufficient. Readback is checked independently of report generation: a report exception does not erase a provable commit; a Store hold still prevents proof. Existing transaction writes, recovery and failure locks are unchanged.

`UnitActions.Run` preserves that second result through its existing protected Settler call and presentation formatting. The normal unit request carries no CityID; the authoritative result supplies the target. Construction Team operations do not manufacture an investment result, and their irreversible transaction is untouched.

One named Gameplay composition function replaces the two old Housing/GPP calls in each investment entrance. Network and all other consumers keep their existing order/scope. Housing and GPP resolve the target via FindID, revalidate reference/token/identity, and each reads its own current facts. No cross-writer cache is shared. Malformed/stale targets hold these scoped updates; preview, refusal, duplicate, UNKNOWN and non-investment actions retain the previous player fallback. No city-per-turn suppression or new retry queue is introduced.

Each writer retains exclusive ownership of its carriers, reconciliation and confirmed-loss exit. One consumer exception does not prevent the other from running. Existing bounded error tables record scope/notification failures without clearing another city's errors. Notification evidence expires with the synchronous call; it is not published to UI or persisted.

## Local validation

- [New actual-module suite](../../../../DevelopmentTests/test_investment_update_propagation.py): **21 methods / 59 explicit subtests PASS**. Uses actual producer, normal UnitActions transport, Gameplay entrances, Housing/GPP writers and their real SQL; compares against frozen B173 source. No legacy test/assertion was edited.
- Four professions × three Governor ceilings × three specialist counts produce identical ledgers/carriers; Housing's ordinary-building tiers and same-turn changes remain correct. The real Construction Team action also preserves its output, receipt and progress, with no fabricated investment result.
- Prepare/refusal/repeated confirm; getter/setter/readback/no-debit and throw-after-write faults; post-commit report failure; reentry; owner/token/position changes before and during reads; unrelated-city error isolation; repeated notification with no extra writes/debits all covered.
- Actual current Store cases preserve same-city investment and cold-load authority, isolate a failed record, and reject false COMMITTED classification when the Store has held even if raw bytes were written.
- Reused B138 checks cover native hook scope, per-Audit fact/index lifetime, incomplete enumeration, foreign-owner UNKNOWN→withdrawal, load cleanup, same-turn worker changes, and UI worker/mixed/late/reentrant/failure routing. Unchanged Network callbacks are compared for the same calls; no new native Network PASS is inferred.
- Four additional selected `test_store_write_boundaries` methods PASS: same-turn investment/templates/load; real loss/recapture/current facts; evidence-driven failed ordinary readback; actual worker failure/cold-load. The existing `test_investment_store_bridge.py` and `test_settler_investment_executor.py` also PASS at their existing offline-model evidence level.
- Changed Lua syntax, exact modinfo201 file set (189 files including modinfo), build stamp, unchanged LV2_GPP_DIRTY branch and Design bytes checked. Context/selectors/link/diff checks accompany the committed checkpoint.

Reproduction: use Python with `lupa.lua55`, `PYTHONDONTWRITEBYTECODE=1`, then `python3 DevelopmentTests/test_investment_update_propagation.py`. The exact Git baseline above must exist locally; no external gameplay DB or game process is needed. Test dependencies and fixtures remain under the existing test navigation.

## Work measurements and limits

All counts below use one confirmed investment after Prepare, same fixtures and unchanged carrier amounts. Other consumer callbacks are held identical; their internal work is not included. City visits count only the two migrated writers. Facts are instrumented EffectiveFacts calls across the included producer/writers. Native getter counts are mock counters, not timing/allocation measurements.

| Owned cities | Housing + GPP visits, old → new | DEV fact reads, old → new | Normal-unit fact reads, old → new | DEV district visits | Normal-unit district visits |
|---|---|---|---|---|---|
| 8 | 16 → 2 | 24 → 11 | 26 → 13 | 17 → 17 | 33 → 33 |
| 20 | 40 → 2 | 48 → 11 | 50 → 13 | 41 → 41 | 81 → 81 |
| 40 | 80 → 2 | 88 → 11 | 90 → 13 | 81 → 81 | 161 → 161 |

Housing/GPP city collection enumeration falls from two enumerations to zero. For this initial bare-district fixture, carrier writes remain 3→3 and mock getters are 495/987/1807→208. Additional final commit-proof reads are included in the new fact totals. Player-wide district indexes, normal-unit site validation, other consumers and native event-triggered work remain. This is not a claim that the entire investment is O(1), all scans disappeared, or native CPU/memory improved. No broad stress or gameplay full-regression run.

## Combined native acceptance and stop

The user agrees that this repair and 时代对话 can share one later package/session. **B174 is a source-only checkpoint; no separate deployment or native test is dispatched.** Recorded live remains B173.200 (`B173.200-bc54482-playtest.json`); runtime was not inspected or modified here. B173 Inspiration API acceptance and its non-blocking numerical unknowns remain intact.

Repair observation: once on that shared package, make a normal Settler investment I→II in a city with a sufficiently established Governor and working specialists; confirm its Housing/GPP and one unaffected city after the native refresh. GPP may require the next turn. No extra cold-load ritual is needed for this unchanged save path.

The same Culture city may then receive the next investment to reach ACTIVE III and exercise 时代对话, or an existing eligible Culture city may be used. A Dialogue-only success cannot prove the I→II support transition. Dialogue will need its own new project/ledger/native-yield observations, with a single justified load boundary for its new persistent state. These can be combined in one session without merging their PASS labels. No new Dialogue implementation is included in B174, and no new permanent project fields are introduced by this repair.

The approved repair is locally complete. The existing [Dialogue plan](../../../Architecture/v2/P0_M_Dialogue.md) remains the next bounded functional proposal; revalidate its stale B165/B172 progress against current Status before activating its first slice. Other audit repairs, N/U2 and other professions are outside this checkpoint. Audit originals and frozen evidence remain byte-preserved.
