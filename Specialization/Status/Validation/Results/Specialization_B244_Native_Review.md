# B244 native review — Treasury precision blocks activation

Date: 2026-10-18. Reviewed source: develop `30b6cd4`; unchanged runtime **B244.271 / modinfo271** from `bc69c94`. **USER_GAME_TEST_FAIL: signing does not reach ACTIVE.** The first intent and calling saves now pass; the native debit executes, but its immediate amount readback fails the existing tolerance. Cold-load and maturity acceptance remain untested.

## Confirmed evidence

All 251 source/runtime files match. Receipt `B244.271-bc69c94-playtest.json` remains DEVELOP_ACTIVE, digest `3ea15237bc52f0f7af9900906870f6dacc6a283838b8879d5d4b3c21d6e684db`; no pending deployment marker. Main remains `e901a22` / B069.96. This review makes no replacement or game/configuration change.

The collector captured 69 unique contiguous records, seq 20–88, all T34. The confirmation interval is present. Later socket/context failures and INTERRUPTED collection do not establish game exit or later contract behavior. The earlier CAPITAL_COMMERCE_PENDING records 65–66 are initialization waits: the later OPEN quote is READY and signing reaches the native money call.

| Sequence / line | Observation |
|---|---|
|84–85 /65–66|D3/S1/C1.25/R2; balance 18004.92578125; principal 4501.2314453125; due 44; OPEN READY/canSign=true|
|86 /67|One CAPITAL_MONEY at NATIVE DEBIT: balanceAfter 13503.69140625; actualDelta -4501.234375; readable result|
|87 /68|CAPITAL_MONEY_UNCONFIRMED at NATIVE_DEBIT|
|88 /69|CONFIRM rejected; view HELD and canSign=false|

| Monetary comparison | Gold |
|---|---:|
|Before debit|18004.92578125|
|Requested principal|4501.2314453125|
|Calculated expected balance|13503.6943359375|
|Observed balance|13503.69140625|
|Observed debit|4501.234375|
|Extra debit versus requested principal|0.0029296875|
|Existing absolute readback tolerance|0.000001|

The full expected balance above is recomputed from the logged before/principal values; the trace prints it as 13503.694335938. The discrepancy is much larger than trace formatting error. The trace's `readStatus=VERIFIED` means the read returned, not that the monetary equality check passed.

[CapitalInvestment.mutate](../../../../Mod/CapitalInvestment.lua) performs one ChangeGoldBalance call, reads the balance and requires absolute error <= 0.000001. Its caller first completes the two strict Store writes, then invokes mutate and only afterward writes ACTIVE. Reaching seq86 therefore establishes that **B244's two pre-debit encoded saves/readbacks succeeded in this native run**. This is no longer the B243 pre-debit Property failure. No CAPITAL_SIGNED or settlement record appears.

The screenshot independently shows the reduced Treasury, the locked 4501.231445 principal and T44 due turn, “需核对扣款”, disabled confirmation, and the paused warning. “等待城市与报价更新”/blank balance comes from the held view's intentionally omitted new quotes, not evidence that the old save failure returned. The absent S source is consistent with the existing S=1 fallback; it did not block the READY quote.

## Original evidence

Logs remain unchanged and ignored under `local/diagnostics/B205/session-20261019T025517Z-df0292/`. The one inspected screenshot is moved with its original name to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B244/`, with before/after hash verification. These are local evidence locators, not public downloadable links.

| File | Bytes | SHA256 |
|---|---:|---|
|records.log|25245|`9051d290c96bebeb463e7b89751df1df85d47a77abe13fd52c0c32aa4f97081d`|
|events.jsonl|654|`2c786ded519339350fafa6d1045327afd3997035d70e460aa1a43a8d7a4be76f`|
|summary.txt|475|`cd80017b7912d4b8824fb924e76f19a41d4f18a076850d3b2729a666ac64c900`|
|Screenshot 2026-10-18 at 7.55.46 PM.png|11521599|`8355b0e7c7d18d927e8a63930c0bba06f8e93b5afb8982cfa11b661aef8cf234`|

## Bounded local discrimination

Three scenarios use the **unchanged actual B244 Store/service**, current repository fixtures and the existing Capital-only Property-conversion model. Only the simulated Treasury result differs. Script/output are retained under ignored `local/diagnostics/B244/native-review-20261018/`; no formal test/assertion or runtime source is edited.

| Treasury double | Result | Calls / writes |
|---|---|---|
|Exact addition|ACTIVE; expected balance exactly|1 money call, 3 Property writes|
|Binary32 conversion of resulting balance|ACTIVE; same exact balance for these inputs|1 money call, 3 Property writes|
|Signed delta quantized downward to 1/256|Exact native balance/error; NATIVE_DEBIT failure; DEBIT_CALLING retained|1 money call, 2 Property writes|

All three checks pass. The matching quantization case also retains the other city's record and the DECIMAL17_V1 encoding, holds after refresh/repeated confirmation, and reconstructs to HELD without a second debit. This is LOCAL_SIMULATION evidence for the current protection, not an observed native cold-load result. A stale temporary fixture import initially produced an unrelated founding-reference mismatch; the final reproduction explicitly imports current repository fixtures and does not treat that setup error as a product finding.

**Inference:** the observed amount is compatible with 1/256-Gold quantization. Binary32 conversion of the final balance alone does not explain this debit. One observed debit does not establish the engine's complete representation, rounding direction for positive credits, or all magnitudes. No engine quantization constant is adopted by this review.

The earlier local suite explicitly kept native Treasury precision pending and tested that monetary mismatches hold. The existing guard now rejects a concrete very small native deviation. Repeating storage changes, polling or UI refresh would not repair that monetary boundary.

## B245 proposal — bounded Treasury receipts

**PLANNED_NOT_AUTHORIZED / PRECISION_DECISION_REQUIRED.** Recommended decision: preserve all 25%-principal, return/probability/duration rules and lossless contract storage, but explicitly accept **at most 0.01 Gold absolute difference per successful native debit or credit** as the engine's monetary precision allowance. This is a proposed user-visible acceptance policy, **not a proven engine unit or a silently authorized gameplay change**.

After that decision and separate implementation approval:

1. Change only the native monetary receipt boundary and its directly required model/diagnostic fields. Keep the requested principal and return unchanged; record the actual before/after/delta separately so the settled receipt does not pretend the theoretical amount was transferred exactly.
2. Continue requiring an unchanged starting balance, a successful single native call, finite/readable result and correct direction/nonzero movement. Wrong direction, ignored or throwing calls, unreadable results, errors outside the approved bound, invalid references or failed receipt saves remain held. Tiny amounts whose movement cannot be verified are not automatically accepted.
3. Never compensate with a second transfer, accumulate rounding differences, retry an ambiguous call, silently relax whole-record comparisons or infer success on load from CALLING alone. Existing failed test contracts remain held; no automatic refund/unlock/migration.
4. Reuse actual Store/service regressions for the captured debit, positive-credit quantization counterexamples, the precise bound and beyond-bound cases, tiny amounts, final-receipt failure and no repeat after reconstruction. Positive quantization simulations are tests, not native evidence.
5. Extend existing bounded CAPITAL_MONEY diagnostics only as needed to distinguish native read availability from receipt acceptance and expose requested versus actual amounts. Do not add timers, new monitoring or unrelated UI work.

No new user test is requested now. After repair/local checks/deployment, use the already planned **one combined stable-signing → midterm save/cold-load → maturity → no-repeat** flow from the pre-confirmation baseline. It then covers the currently unreached credit and save-file boundaries. Do not continue this already-paused contract or ask the user to repeat the failed debit without a changed hypothesis.

User decision: approve/change the proposed <= 0.01-Gold receipt allowance and the bounded B245 implementation. User testing: none now. Primary next: stop after recording this review; no implementation or deployment. Original evidence, Design, Architecture, Mod, tests/tools, Runtime_Index, main and configuration remain unchanged.
