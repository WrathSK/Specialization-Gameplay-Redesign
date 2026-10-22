# B245 local result — bounded native Capital receipts

Date: 2026-10-18. Source basis: develop `a16cc99`; build **B245.272 / modinfo272**. The user explicitly accepts at most **0.01 Gold per native debit or credit**, authorizes this implementation and the existing guarded deployment, and requires unchanged principal, return formulas and no-double-debit protection. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.**

## Implementation boundary

[B244 native evidence](Specialization_B244_Native_Review.md) remains unchanged: the requested 4501.2314453125 debit produced an actual 4501.234375 debit and correctly stopped under the former tolerance. B245 applies the accepted allowance only to immediate native Treasury observations. A successful call requires readable finite nonnegative balances, a nonzero change in the requested direction, and `abs((after-before)-requestedDelta) <= 0.01`. The original requested amount is sent once. No Floor, amount correction, compensation call, cumulative error account or assumption about an engine quantization unit is introduced.

Contract principal and safe/success/failure returns remain the original quote values. B245 stores the actual debit (`debitAfter`, `debited`) and credit (`creditActualAfter`, actual `paid`) separately from theoretical `balanceAfter` and `creditAfter`. The model validates their arithmetic against the observed balances and the approved bound. The existing `DECIMAL17_V1` codec covers these three additional fields, thirteen in total; raw Store readback equality remains exact. Actual settled net shown in the existing panel is actual paid minus actual debited.

The Capital extension business version becomes 2 so a missing receipt cannot masquerade as a valid current contract. This is not a general Store schema change or a migration of old Capital attempts. Existing failed/unknown B244 attempts remain unavailable; do not clear, retry or reconstruct them from current Treasury. Use a save from before the first Capital confirmation. Other city history and extensions are untouched.

Intent → CALLING → native transfer → verified final receipt ordering, private outcome/protection rules, reference/Owner checks, and unresolved CALLING/no-replay handling remain in place. An exception, unreadable balance, zero/wrong-direction result, discrepancy over 0.01 or strict receipt-save failure holds the affected operation. A proven final receipt can survive a later error; an unknown transfer is never inferred from a later Treasury balance. There is no automatic retry or refund.

The existing bounded diagnostic projection and collector stream report requested/actual deltas, before/after balances, signed error, tolerance, call/read status and acceptance. Monetary observations use round-trip formatting. No new sampler, collector mode, external configuration, timer, scan, cache, queue or GC behavior is introduced; trace bounds remain 64 retained / 96 budgeted. Store owns the receipts, native Treasury owns current balances, and quote/UI copies remain derived, replaceable views.

## Local verification

**142 selected methods PASS, zero remaining failures/errors/skips in that set:** 23 new B245 methods and 119 directly relevant retained Capital/Store/UI/diagnostic methods. Actual Lua Model, Store and service execute against explicitly simulated Treasury and Property behavior; no native monetary or save-file PASS is inferred.

- The coherent B244 module closure rejects the captured debit under the 1/256 signed-delta simulation. B245 accepts exactly that observed pair, preserves the quote and records 4501.234375. The simulation is a reproducer, not an asserted universal engine unit.
- Actual positive credit, stable and both venture outcomes, independent per-call errors, three domain slots, another city's isolation, changed ACTIVE/network facts and confirmed source loss are covered. Original principal, payout and probability formulas remain unchanged.
- A fresh Lua VM restores only persisted fixture Properties and the native balance, retains actual debit/locked terms and private outcome, makes no duplicate debit/roll, then credits once. This is local reconstruction evidence; the requested cold-load gate still needs the user.
- Boundary/non-finite/wrong-direction/zero actual cases, before/after-call exceptions, unreadable results, over-bound debit/credit, receipt-save exceptions before/after persistence, malformed/missing receipts and old business versions remain guarded. Repeated reconcile/reload never retries an unknown transfer. A 0.001 change to persisted quoted return still fails exact Store verification before any debit.
- New receipt strings survive the existing simulated Capital-only binary32 Property conversion. The unchanged collector parses exact requested/actual/error values; settled UI uses actual net. Public UI supplies no authority.

| Coherent immediate-baseline comparison | B244 | B245 |
|---|---:|---:|
| Signing + maturity Property reads |14|14|
| Successful Property writes |7|7|
| Native money calls |2|2|
| Cross-record uniqueness visits |0|0|
| Original quote, locked contract terms and final Treasury |reference|exact match with exact native-double fixture|

Actual receipts/version are intentionally additional state; `paid` now means observed credit rather than the theoretical request. Existing affected tests were updated only for the new Activate receipt argument, a valid interrupted CREDIT_CALLING fixture, observed payment arithmetic and package version. Six historical assertions remain unchanged and outside this gate: four already documented in B244; its old service/model-byte freeze; and the B242/B243 mixed-old-service/current-model comparison. The new coherent B244/B245 comparison replaces that invalid mixed-version comparison. The existing non-Capital 8/20/40-record value/work checks remain in the selected gate. These counts establish local work equivalence, not native CPU/memory improvement.

Eight changed/direct Lua files compile, four changed/new Python test files parse, and the 250 unique modinfo entries plus modinfo form the 251-file version 272 package. Current context selectors, named reviewed hashes, Markdown targets, diff and staged publication are checked before commit. Raw runner/results remain ignored under `local/diagnostics/B245/`. Original B244/frozen evidence, generic Store, Design, main, deployment tools and game configuration remain unchanged.

## One combined native session

Use Standard speed and the usual Commerce ACTIVE III+ city, from a **pre-confirmation save with no previous Capital contract/failed intent**. Start the existing manual collector. No P0 prototype switch or repeated screenshot series is needed.

1. **城市生产列表 → 资本投资 → 科研 → 确认稳健投资**, once. The contract should be running with its locked principal and due turn. This tests the accepted native debit receipt; logs record its exact requested/actual amount and error.
2. While running, save, fully exit Civilization VI, then cold-load that save. Restart the manual collector if it has exited. Reopen **资本投资**: principal, return and due turn should remain, with no second debit. This tests the changed actual-receipt persistence and the still-unaccepted native B244 codec path together.
3. Reach the displayed due turn (ten Standard turns from signing). Reopen **资本投资** and confirm settlement. Reopen once more in the same turn: no second payout. Logs distinguish requested return from actual credit and record the final receipt; normal turn income need not be manually subtracted from the Treasury total.

If held, stop at that point and submit the collector output; do not keep confirming the same failed contract. One screenshot is useful only for an unclear display/error. No extra Venture, unrelated-city, whole-mod or repeated lifecycle test is requested.

## Checkpoint

Source: **B245.272 locally complete, native pending**. Live deployment is recorded only after the clean committed source, automatic game-exit, exact receipt/backup/hash and per-file checks. The user has resolved the monetary allowance; no further Design decision is needed for this batch. Stop after delivery for this combined native test; do not begin COM-C/D or unrelated repair.
