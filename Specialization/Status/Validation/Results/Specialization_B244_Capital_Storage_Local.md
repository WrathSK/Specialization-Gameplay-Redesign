# B244 local result — lossless Capital numeric storage

Date: 2026-10-18. Source basis: develop `d33fe78`; build **B244.271 / modinfo271**. Explicit user authorization: repair only Capital contract numeric storage, retain monetary rules, strict save verification and no-double-debit protection, then perform the existing guarded deployment. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.**

## Implementation boundary

[B243 native evidence](Specialization_B243_Native_Review.md) identifies a readable intent record whose safe return changes4670.0276245117193→4670.02783203125 before any debit. Its original report and raw evidence remain unchanged.

The existing Capital model now owns an explicitly tagged `numberEncoding=DECIMAL17_V1` wire representation. Principal, balanceBefore/balanceAfter, safe/success/failure, probability, and optional creditBefore/creditAfter/paid are canonical17-significant-digit decimal strings in native Property storage. Encoding checks exact numeric round trip; decoding rejects absent/unknown encodings, wrong types, non-finite or noncanonical numeric text and invalid business records. Existing version1 business values remain numbers to consumers. References, phases, integer counters, C=1/1.25, hidden protection and all other city extensions retain their representation.

Store's CapitalState/WriteCapital/VisitCapital and record-validation adapters decode only this extension. Confirmed Owner loss terminates decoded business state and re-encodes it. This is a direct dependency of the changed format, not a new ownership rule. The raw Store envelope remains encoded: prewrite stale checks and complete postwrite equality still compare every stored value exactly. A failed candidate remains guarded; no tolerance, dropped field, automatic hold clearing, replay or refund is introduced. Old numeric Capital records are not guessed/migrated; the native test starts before any prior contract attempt.

The fixed failure projection recognizes only allowlisted canonical numeric strings and the encoding marker, while reporting raw field types and exact mismatch status. It never publishes arbitrary saved strings, names, requests or hidden outcomes. It uses the existing observation, trace fields and bounds; no collector or UI change.

**Unchanged:** CapitalInvestment service, all quote/return/probability formulas, Treasury debit/credit and its readback tolerance, intent→calling→receipt order, strict generic Store writer/reservations, stale/reference/UNKNOWN guards, public UI, native call counts, event wiring and all other abilities. No general serializer, extra ledger, cache, pending queue, timer/frame update or GC change. Only temporary bounded numeric copies are created at Capital API boundaries (at most three contract slots), with the same existing caller ownership and lifetime.

## Local verification

**121 selected test methods PASS, zero remaining failures/errors/skips in that set.**26 new B244 methods plus95 relevant retained Capital/Store/UI/diagnostic checks. Tests use actual Lua model, Store and service; native Treasury remains an explicit double. SQL package checks use the existing read-only configured database in memory.

- The old B243 Store under the Capital-only binary32 conversion model reproduces the native safe pair, COMPLETE diagnostic, diffCount4 and zero money calls. The same inputs with B244 sign and settle with exact decoded amounts. The conversion is intentionally scoped to Capital; it does not claim that all native numeric Properties, structural integer hashes or Treasury APIs use binary32.
- Ten stored numeric fields round-trip fractional and extreme finite values. Invalid/noncanonical/unknown formats hold. Actual Store covers three domain slots, stable and both venture outcomes, optional credit/paid receipts, no-op/stale writes, private snapshot isolation, Owner loss, hidden-protection preservation/reset and unrelated-city isolation.
- A separately constructed Lua VM receives only persisted Properties/native-shaped fixture state and restores the locked contract without debit or RNG replay. Maturity credits once. This models reconstruction, not a native save-file PASS.
- Ignored/throwing/missing/unreadable writes, one-ULP/string/type changes, unrelated-field corruption, failed ACTIVE/SETTLED receipts and broken diagnostic projection remain held. Same-session and reconstructed paths do not duplicate debit/credit. Treasury rounding still fails under the unchanged monetary guard; the storage repair does not hide it.
- The business service and UI are byte-identical to B243; original model math/lifecycle functions and generic Store commit/reservation code are unchanged. Decoded whole-record and business values match the immediate baseline.

| Immediate-baseline comparison | B243 | B244 |
|---|---:|---:|
| Signing + maturity Property reads |14|14|
| Successful Property writes |7|7|
| Native money calls |2|2|
| Cross-record uniqueness visits |0|0|
| Decoded business/record values |reference|exact match|

Independent non-Capital age-write comparisons at8/20/40 records and40-record/one-writer scope retain exact values, writes and zero cross-record uniqueness visits; duplicate turn and reconstruction do not write. These counts establish local work equivalence, not native CPU/memory improvement.

Four historical assertions are outside the selected current gate, without editing them: two frozen model/Store-byte assertions; the B241/B242 raw-record-format comparator (wire format intentionally changes); and the old Store-age comparator against a pre-institutionTurns baseline. The latter's four institutionTurns mismatches were reproduced on unchanged `d33fe78` Store. B244 adds immediate-baseline decoded equality/work and non-Capital age comparisons instead. Original failure/control output is retained locally; no unrelated assertion was weakened.

Eight changed/direct Lua files compile; two Python files parse. All250 unique modinfo entries exist and, with modinfo, match the251-file package/version271. The maintained UI package assertion changes only270→271. Current selectors, reviewed hashes, links, diff and staged publication passed before commit. Ignored raw local output is under `local/diagnostics/B244/`.

## One combined native session

Use the usual Standard-speed Commerce ACTIVE III+ city and the **pre-confirmation baseline without a prior Capital contract or failed intent**, in a separate test save slot. Start the existing manual collector; it is unchanged. No P0 prototype toggle or screenshot series is required.

1. **城市生产列表 → 资本投资 → 科研 → 确认稳健投资** (left-click), once. Confirm one running contract, its principal/maturity and a single25%-of-current-Treasury debit. This tests native Property round trip and the previously unreached debit boundary.
2. While it is still running, save once, fully exit Civilization VI, then cold-load that save. Restart the manual collector if it exited. Reopen **资本投资**: the same locked principal, return and due turn should remain, without another debit. This specifically tests B244's changed persisted representation.
3. Continue to the displayed due turn (10 Standard turns from signing). The contract should show **已结算** and its locked return. The bounded CAPITAL_MONEY/SETTLED records distinguish this payment from ordinary turn income; no manual reconstruction of all income is needed.
4. Continue one more turn or reopen/refresh the settled panel once: no second payment. Submit the two collector sessions covering before and after the restart.

If any stage becomes paused, stop that contract and submit its log; do not retry confirmation or use an already failed intent to test recovery. Native Treasury precision remains separate: a concrete mismatch would require its own evidence/decision, not automatic Floor or relaxed validation. No second domain, forced venture reroll, repeated cold loads or unrelated ability regression is requested.

## Handoff

User decision: none within this approved representation-only repair. User testing: the combined session above after verified deployment. Primary next: await the combined native session after the verified deployment below; stop further implementation. Capital native acceptance remains pending; COM-C/D, Culture HOLD and other audit/Gameplay batches remain unauthorized. Design, main, configuration, original logs and frozen prior evidence are unchanged.

## Verified deployment

B244.271/modinfo271 is DEVELOP_ACTIVE from clean/pushed `bc69c947a6442d7bab7a09762905265021e3d844`. Receipt `B244.271-bc69c94-playtest.json`;251/251 source/runtime files MATCH, digest `3ea15237bc52f0f7af9900906870f6dacc6a283838b8879d5d4b3c21d6e684db`. Both receipt-bound B243 restoration and B244 activation passed fresh automatic game-exit checks and check-only hashes. B243/stable recovery retained; no pending transaction. Main/configuration and frozen evidence are unchanged; no game launch. Stop for the single combined native session; local success is not native acceptance.
