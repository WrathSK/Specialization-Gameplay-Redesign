# B243 native review — Capital Property numeric precision

Date: 2026-10-18 (America/Vancouver; collector folder uses UTC). Review basis: develop `3ab7121`; deployed source `c696104`, **B243.270 / modinfo270**. Evidence review and a proposed repair only; no implementation, formal test edit, deployment or Design change.

## Review summary

**The B243 readback diagnostic and paused-refresh gate work in this captured session. Capital signing still fails before debit.** The save setter returns normally, the saved contract is present and readable, but its first reported numeric difference is:

| Field | Expected before save | Actual readback |
|---|---:|---:|
| contract.safe |4670.0276245117193|4670.02783203125|

The difference is about0.0002075195307 Gold. The actual value is exactly the IEEE754 binary32 conversion of the expected value. This is direct evidence of precision loss at this Property round trip. It is no longer merely an injected hypothesis as in B242. It does not establish the representation of every engine API or the native Treasury mutation behavior.

`diagnosticStatus=COMPLETE`, `POSTWRITE`, `RETURNED`, `READABLE`, all record/capital/contract types `table`, saved phase `DEBIT_INTENT`, `savedMatches=false`, and `diffCount=4` are present. The diagnostic itself did not fail. The comparison reports the first differing value and a count within its fixed projection, not all four native value pairs.

**Root cause:** the Capital business record passes arbitrary Lua calculation results directly into native numeric Property storage. Store then requires exact equality against the original number. The engine returns a lower-precision value, so the current representation violates that exact-readback assumption. Store intentionally pauses before the separate Treasury operation. The safety ordering is doing its job; the numeric persistence representation needs repair.

## Original evidence

Original files remain unchanged and ignored under `local/diagnostics/B205/session-20261019T023220Z-2bcb3e/`. No screenshots were present in the inbox.

| File | Bytes | SHA256 |
|---|---:|---|
| records.log | 26237 | `85919192a52d634d451be0887c5dafe3f3ab5077c902b5c88ec2a7c424867518` |
| events.jsonl | 905 | `6cc923fa2d9e5358ae41fe3ba664aaf347e96036232eaa64aa462c1197166663` |
| summary.txt | 458 | `b3e905e2fdff6fa256fd0cbf34ed8c5a721fad1f43c7a1ac40c6ef878fee2995` |

There are71 contiguous records, seq20–90, all T34. One passive capture ends with PARTIAL_FRAME_AT_DEADLINE and the collector subsequently labels its exit GAME_EXITED. The observed confirmation and manual-refresh interval is complete; earlier records before20 and later activity are not reconstructed. No missing native step is inferred from `alerts: none`.

Eight directly relevant source/live files match byte-for-byte: CapitalInvestment, its Model and Diagnostics, CityProgressionStore, ExpeditionTrainingDiagnostics, CapitalInvestmentPanel, Probe and modinfo. The existing B243 receipt remains DEVELOP_ACTIVE with no pending transaction; this review makes no runtime replacement.

| Sequence / log line | Observation | Meaning |
|---|---|---|
|65–66 /46–47|CAPITAL_COMMERCE_PENDING during initial refresh|Readiness wait before the later usable quote; not the confirmation blocker|
|84–85 /65–66|D3/S1/C1.25/R2, Treasury18004.92578125, principal4501.2314453125; OPEN READY/canSign=true|Quote and network/source prerequisites reached usable state|
|86 /67|COMPLETE diagnostic, contract.safe difference above, diffCount4; STORE_WRITE_UNCONFIRMED at DEBIT_INTENT_WRITE|First intent save is readable but numerically different; no debit call reached|
|87–88 /68–69|PROGRESSION_HELD; CONFIRM rejected, HELD/canSign=false|Write protection holds the affected city|
|89–90 /70–71|REFRESH accepted as a read request; reason PROGRESSION_HELD, HELD/canSign=false|Refresh does not clear the guard or misreport READY|

No CAPITAL_MONEY, CAPITAL_SIGNED or settlement record appears. The reported phase and [actual request order](../../../../Mod/CapitalInvestment.lua) place this failure before `ChangeGoldBalance`. The UI's published paused state is verified; no rendered screenshot was required or inspected.

## Where the transaction stops

The intended business operation is straightforward: lock the contract, debit its principal, and credit the locked return on maturity. Because native Treasury mutation and saved receipts are separate operations, the implementation records progress to prevent replay after an interrupted operation:

1. Build the contract from the current quote.
2. Save **DEBIT_INTENT** and verify readback — **this is the failing step**.
3. Save **DEBIT_CALLING**, then invoke the native Treasury debit once.
4. Save the ACTIVE receipt; existing turn/load processing later reaches credit intent, calling and settled receipt.

The precise-equality check in [Store](../../../../Mod/CityProgressionStore.lua) rejects the changed number at step2. Changing refresh/event timing, replaying the command or fixing the payout callback would not address this failure. Earlier local fixtures returned numeric table values unchanged and therefore missed the native conversion; B242 then obscured the failure detail through its restricted-Lua diagnostic defect. B243 now provides the required distinction.

## Bounded local discrimination

The unchanged actual Store/service was exercised with the native quote inputs and rawget absent. Only fixture Property behavior varies. Reproduction and output remain ignored under `local/diagnostics/B243/native-review-20261018/`; formal tests, assertions and source are unchanged.

| Property behavior | Result | Diagnostic / money calls |
|---|---|---|
|Exact numeric round trip|ACTIVE|One debit; balance13503.6943359375|
|Only safe return converted to binary32|HELD before debit|Same first expected/actual pair, diffCount1, zero money calls|
|All numeric Property values converted to binary32|HELD before debit|Same first pair and diffCount4 as native, COMPLETE; zero money calls; held after refresh/repeat|

The all-numeric local model changes safe, success, failure and probability; the principal and initial Treasury happen to be exactly representable for this quote. Those four field identities are a matching **local model**, not four individually captured native readbacks. Three scenarios pass their discrimination checks. An arithmetic check also shows17-significant-digit decimal strings round-trip these six original numbers exactly; no storage codec was implemented or wired into Store during review.

## B244 proposal — lossless Capital numeric persistence

**PLANNED_NOT_AUTHORIZED.** Repair the Capital extension's persistence representation; retain exact guards and the existing transaction lifecycle.

1. Add a small, explicitly versioned Capital-only encoding boundary. Store the finite fractional contract amounts/probability/monetary receipts as canonical round-trip decimal strings, and decode to numbers for the existing business API. Cover principal, balanceBefore/balanceAfter, safe/success/failure, probability, creditBefore/creditAfter and paid; leave structural references, phases, integer counters and other extensions alone. Do not introduce a second authoritative ledger or global serialization framework.
2. Integrate through the existing CapitalState/WriteCapital/VisitCapital and Capital record validation boundaries. Keep the Store envelope in its encoded representation so its prewrite and postwrite exact comparisons remain meaningful. Business callers receive decoded values only. Validate encoding version, field types, finite values and round-trip form; malformed/unknown data remains held. Maintain stale-snapshot, source ownership, phase and no-replay checks. Check only direct consumers, including the fixed diagnostic projection, for the representation difference.
3. No Floor, cent rounding, silent binary32 conversion of the business contract, global epsilon or tolerant whole-record equality. The new representation preserves the existing Lua amount; it does not change principal percentage, duration, returns, probabilities or hidden protection. Do not guess the pre-rounding contents of a previously failed record, automatically clear its hold, refund/replay money or build old-save migration. Native verification uses the existing pre-confirmation baseline with no Capital contract.
4. Extend targeted actual-Store coverage to simulate the observed native numeric conversion. Verify exact decoded amounts through signing, maturity and a fresh reconstructed Store; all three domain slots/modes and optional credit receipts; malformed strings, changed values, throwing/ignored writes, failed final receipts and zero duplicate debit/credit. Ensure unrelated city/extensions and normal uniqueness-visit costs remain isolated. Reuse existing shared lifecycle tests instead of a full gameplay regression.
5. Keep diagnostics bounded and readable. If a native Treasury debit/credit later cannot represent the intended amount, report its before/expected/actual result under the existing no-replay protection. **Property persistence precision and Treasury mutation precision are separate boundaries**; this proposal does not silently authorize a money-rounding rule or alter Treasury tolerance.

Expected code surface: Capital-specific encoding/model support and the directly related Store read/write/visit/validation adapters, with only a necessary diagnostic projection adjustment; focused tests and normal build/result/context records. No general Store rewrite, other Commerce ability, timer, GC or UI redesign.

## Next native gate after approval and local checks

No new test is requested now. After the repair, resume the previously incomplete Capital acceptance in **one session**: start the usual collector, sign one stable contract from the pre-confirmation baseline, save and cold-load once during its term, then observe its one-time maturity payment. The cold load now specifically validates the changed persistence representation rather than an unchanged test harness. Logs carry expected/actual values; no repeated screenshot series, second domain or forced venture reroll is required. Local deterministic coverage handles the other branches.

If confirmation still holds, stop at that stage and return the log. If Treasury precision becomes the next concrete blocker, stop that monetary path and present the required decision; do not repeatedly retry or extrapolate from the Property result. Deployment and exact Chinese button steps follow separately authorized implementation.

User decision: review/authorize the proposed B244 representation repair; no gameplay amount change requested. User testing: none now. Primary next: preserve this evidence/current navigation, then stop. Source/runtime, Design, Architecture, formal tests, main, configuration and frozen prior evidence remain unchanged.
