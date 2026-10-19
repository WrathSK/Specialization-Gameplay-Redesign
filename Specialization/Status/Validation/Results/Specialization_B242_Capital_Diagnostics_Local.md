# B242 local result — Capital confirmation diagnostics

Date: 2026-10-18. Source basis: develop `8e8b5eb`. Build: **B242.269 / modinfo269**. The user explicitly authorized failure-stage/readback diagnostics and correct paused feedback while preserving no-double-debit protection and all economic amounts. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The underlying B241 native write/readback cause remains UNKNOWN; this is not a claim that native signing is repaired.

## Implementation boundary

The [B241 native review](Specialization_B241_Native_Review.md) remains frozen. Its original first confirmation loses the Store cause behind CAPITAL_STATE_UNKNOWN, and a subsequent read request misleadingly reports CAPITAL_READY despite a HELD view. This batch corrects those observations and feedback only.

| Changed surface | Responsibility / lifetime |
|---|---|
| CapitalInvestment | A request-local attempt tracks validation, contract construction, DEBIT_INTENT write, DEBIT_CALLING write, native debit and ACTIVE receipt. Existing reconciliation/credit exits use the same diagnostic shape. Failure preserves its original sanitized code and phase before conversion |
| CityProgressionStore | Optional failure observer for WriteCapital, using the existing prewrite/postwrite readback. Called under pcall on failure only; no new Property read, retry, persistent field, reverse index or changed write guard. Other writers omit the observer |
| CapitalInvestmentDiagnostics | Pure fixed-field projection of observed versus expected data. Reports read point, setter return/throw, record/capital/contract types, saved phase, equality result and first differing schema field with finite numeric values. Read errors remain distinct from nil/missing records. Comparisons are bounded to known fields; unlisted/private differences remain explicit, never claimed equal |
| Existing bounded collector | CAPITAL_FAILURE and CAPITAL_REQUEST add safe scalar fields to the existing whitelist. KEEP64/BUDGET96, record format and collection script remain unchanged. No timer, frame callback, new logger or GC change |
| Panel / published view | HELD is visibly paused. A successful OPEN/REFRESH acknowledgement means the read request was handled, not a usable contract. The first useful failure remains in that city's replaceable view until actual recovery; close/reopen and refresh cannot clear Store protection |

Diagnostic values exclude city/player names, full paths, request/token values, hidden risk results and failure-protection counts. Error filenames are allowlisted basenames. A full-readback mismatch outside the fixed projection is reported as OTHER_RECORD_OR_UNLISTED; a throwing setter with an identical persisted record reports savedMatches=true but still retains the original failure/hold. No diagnostic result is an authority to retry or repair saved data.

The six new Chinese localized pause messages distinguish intent-save failure, pre-debit recording failure, uncertain native debit, final contract receipt failure, maturity receipt failure and unavailable saved state. They use the existing panel/error control and localization fallback. No layout, unrelated panel or economic UI rewrite.

CapitalInvestmentModel is byte-identical to B241. Principal, fractional amounts, D/S/C/R, rates, duration, risk/protection, Treasury tolerance, write/call ordering, ownership and no-replay semantics are unchanged. No automatic refund, re-sign, truncation, new save migration or next Commerce ability.

## Local verification

**194 targeted tests PASS; 0 failures/errors/skips**:22 B242 checks +46 B241 checks +109 current B239/B240 checks +17 relevant actual-Store boundary checks.

- Actual logged fractional quote remains4501.2314453125 principal from18004.92578125 Treasury; local success makes one debit and ends at13503.6943359375. This is a native-shaped double, not a native precision result.
- Throw-before, throw-after, ignored setter, altered float32 scalar, missing/scalar/unreadable readback, prewrite revision mismatch, second pre-debit write failure and final receipt failure have distinct phase/readback evidence. Failed pre-debit cases make zero native money calls.
- Native debit mismatch preserves CALLING/HELD and never retries. Final credit-receipt failure remains no-replay after reconstruction. Other cities stay independent. An observer that throws cannot bypass the write failure boundary.
- A direct B241/B242 comparison preserves every saved value, Treasury result, native call count and Property read/write count for normal signing/settlement. Both retain **zero cross-record uniqueness visits**. This proves local access/behavior equivalence, not native CPU or memory improvement.
- Actual UI ack, refresh and reopen keep pause text and disabled confirmations. Existing collector parsing accepts the real emitted diagnostic fields; its64-entry/96-record bounds remain effective. Hidden values and arbitrary error text do not enter the diagnostic projection.
- Current SQL/package/control/localization checks pass. B241 package assertion only advances to269. The existing SQL fixture now removes the two exact B241 access definitions from its **in-memory copy** before reapplying current Commerce SQL, because the loaded native cache now contains them. Assertions and the external read-only DB remain unchanged.

One extra historical test was inspected rather than silently made green: the pre-B169 frozen-schema whole-record comparator has four existing subcase failures because B241 added institutionTurns. All four were reproduced using pre-B242 Store source from8e8b5eb. Its assertions/frozen baseline were left unchanged; the new B241/B242 per-value comparison covers this batch's actual delta. The194-case result excludes that separately recorded stale comparator.

Changed/direct Lua syntax, XML/package imports, document targets/anchors, current selectors/Context Lock, diff and staged publication are checked before commit. No whole gameplay regression, game launch or native PASS is claimed. Prior B241 result/raw logs/reproduction, Design, other runtime modules, main and configuration are preserved.

## One minimal native diagnostic session

Use the same **pre-confirmation** test save and the existing manual collector. This is one first-confirmation observation, not the earlier10-turn acceptance flow.

1. **城市生产列表 → 资本投资 → 科研 → 确认稳健投资**: click confirmation once.
2. If paused, read the short stage message and click **刷新报价** once. It must remain honestly paused with confirmation unavailable; refreshing must not send another debit. Return the collector log and stop.
3. If it unexpectedly signs successfully, return that same session's log and stop; no second domain, waiting10 turns or repeated confirmations is requested in this diagnostic batch.

No new screenshot series, cold load, timer, special P0 button or configuration change is required. The log should distinguish prewrite conflict, setter failure, readback shape/value difference and post-debit receipt failure. A native precision limitation requiring a changed amount is a user Design decision, not permission to Floor it here.

## Handoff

User decision: no new decision needed for this diagnostic scope. User testing: the single short session above. Primary next: perform W0003 guarded deployment when the game is confirmed closed, then stop for evidence. COM-C/D, Culture HOLD and unrelated audits remain outside this batch.

## Verified deployment

B242.269/modinfo269 from clean/pushed `7dda4211280a95102115a943f4194de2e2afa27a` is DEVELOP_ACTIVE. Receipt `B242.269-7dda421-playtest.json`;251/251 source/runtime files MATCH, digest `c02e65a174a5878fb141c0bc02f97c1b33ff043a676aa23cd0f931b0b663f094`. Fresh automatic OS game-exit checks passed immediately before the exact B241 restore and B242 activation. Both recovery packages are retained; no pending transaction, game launch, configuration change or main promotion. Primary next: await the one short diagnostic log; underlying native confirmation cause remains UNKNOWN.
