# B241 native review — first Capital confirmation failed

Date: 2026-10-18 (America/Vancouver; raw session folder uses UTC). Review basis: `cf6befd`; implementation/deployment `66a94b9`, B241.268/modinfo268. The user stopped at test step 1. This is evidence review and a narrow diagnostic proposal, not implementation or deployment.

## Review summary

**USER_GAME_TEST_FAIL: first Capital confirmation.** The ordinary panel obtained a quote, then the confirmation was rejected with `CAPITAL_STATE_UNKNOWN` and the city view entered HELD. There is no `CAPITAL_MONEY`, `CAPITAL_SIGNED` or settlement record in the contiguous captured interval. Source order and the local counterexamples point to the pre-debit contract-save/readback boundary; the existing log does not identify the exact failed native call or persisted partial record.

The quotation itself is valid. Replaying its logged balance/D/S/C/R inputs against the actual local service and Store succeeds. No monetary rounding decision, new source-selection rule or repeated user test is justified by this evidence. The native Gold writer and maturity/reload acceptance remain untested.

The first confirmed implementation defect is lost failure detail: Capital's code filter retains only CAPITAL/COMMERCE prefixes. Store errors become `CAPITAL_STATE_UNKNOWN`, and the request handler drops the original failure without recording its stage. The refresh catch also discards its original error. A second reporting defect is that OPEN/REFRESH returns `CAPITAL_READY` even when Refresh returned a HELD view. Later accepted refresh requests in this log therefore do not prove recovery.

## Original evidence

Raw files remain unchanged and ignored under `local/diagnostics/B205/session-20261019T014544Z-7b437d/`. The B205 trace prefix identifies the collector family, not the deployed build. Source/live bytes for CapitalInvestment, its model/panel, CityProgressionStore and modinfo were rechecked equal; this review does not claim a fresh full-runtime comparison. No new screenshots were in the inbox.

| File | Bytes | SHA256 |
|---|---:|---|
| records.log | 25251 | `57987b960ea965e5c58ed13a43ced94e38e2eadcac9f11bb61eb5ff1f7150722` |
| events.jsonl | 844 | `8eef25b556c8ce8a78bf7c683f0c12d153be7d9f943a04118b61bc3292950272` |
| summary.txt | 456 | `32498c62ed1b694706790bbea056472cb82bcee58df3291a26c6b42a15ece081` |

There are 71 distinct records, seq20–90 with no gaps. All are turn34, one Gameplay context. The collector ended INTERRUPTED and had transport reconnects; seq87–90 remain captured. Earlier initialization before seq20 is not reconstructed. `alerts: none` is a collector summary, not a gameplay PASS.

| Sequence | Observed result |
|---|---|
| 56/57,65/66 | Initial Commerce/network readiness wait; not the confirmation error |
| 77–82 | Both Commerce cities recover READY; existing Commercialization publications continue |
| 84 | City393221, Research quote: Treasury18004.92578125, principal4501.2314453125, D3/S1/C1.25/R2, rate0.0375, safe return4670.0276245117, dueT44 |
| 85/86 | OPEN/REFRESH accepted, before confirmation |
| 87 | CAPITAL_CONFIRM rejected: CAPITAL_STATE_UNKNOWN |
| 88 | Same city's Capital view HELD with the same generic code |
| 89/90 | REFRESH/OPEN accepted, but no new quote/money/signed record; current handler labels cannot establish recovery |

The lack of a concrete S source and S1 fallback does not invalidate this quote. The no-source local control succeeds. The log does not carry a confirming Treasury balance after failure, nor the contents of the attempted Store record. Accordingly, no lost principal, successful contract or repaired save is claimed. The observed path stops before a verified money operation; the native action itself has not produced a test result.

## Direct source and local discrimination

Relevant source: [Capital request/refresh and error filter](../../../../Mod/CapitalInvestment.lua), [Store guarded commit/readback](../../../../Mod/CityProgressionStore.lua), [pure quote and contract shape](../../../../Mod/CapitalInvestmentModel.lua), and [existing actual-Lua test fixture](../../../../DevelopmentTests/test_b241_capital.py).

- CapitalInvestment.lua:14 retains only CAPITAL/COMMERCE error prefixes; unknown Store/Lua errors collapse.
- Lines149–154 discard the caught prepare error after publishing HELD. Lines283–285 discard the original confirmation error before logging the request result.
- Lines272–274 write DEBIT_INTENT and DEBIT_CALLING before calling the Treasury mutation.
- CityProgressionStore.lua:213–219 marks a failed committed record read-only in that session. Lines898–914 distinguish stale input, native setter failure and failed readback, but Capital's outward report loses that distinction.
- OPEN/REFRESH at CapitalInvestment.lua:243–250 treats returning a view as success without checking whether it is HELD. This is an acknowledgement/reporting problem, not evidence that signing resumed.

Five bounded offline scenarios used the actual unchanged service/Store with the logged quote inputs. Only explicit fixture behavior was varied; no repository test, game Property, source or configuration was changed. The local reproduction and JSON result are retained under ignored `local/diagnostics/B241/native-review-20261018/`.

| Local scenario | Result | Native calls / saved state |
|---|---|---|
| Unmodified exact-value fixture | Accepted, ACTIVE | One debit; balance13503.6943359375 |
| Property setter throws before writing | STATE_UNKNOWN, HELD | Zero money calls; no saved capital |
| Property readback rounds fractional scalars to float32 | STATE_UNKNOWN, HELD | Zero money calls; DEBIT_INTENT saved |
| Property setter ignores the write | STATE_UNKNOWN, HELD | Zero money calls; no saved capital |
| Treasury writer rounds its delta | MONEY_UNCONFIRMED, distinct from observed error | One money call; DEBIT_CALLING saved |

**LOCAL_SIMULATION_PASS for discrimination only.** These show why the current generic error cannot distinguish materially different save outcomes. Float32 storage is an injected hypothesis, not a finding about Civ VI. The current native cause remains UNKNOWN between an actual write exception, changed readback or another pre-debit Store failure; do not claim engine quantization, corruption or Treasury truncation from these local counterexamples.

## Narrow next proposal

1. Preserve an allowlisted Store error code, module/line and the exact confirmation phase: quote validation, intent write, calling write, native debit or final receipt. Retain the current local hold and no-retry behavior.
2. On a failed Capital write only, record bounded readback facts for the affected contract: read succeeded, absent/present, stage, and first differing field/type/value when safely numeric. Never dump an entire Property, city name, path or arbitrary exception; never treat the optimistic cached candidate as persisted evidence.
3. Make OPEN/REFRESH distinguish a successfully delivered HELD report from an actually signable quote; show a concise Chinese failure stage instead of false READY. No extra retry, timer, forced refund, silent Floor or automatic record replacement.
4. Locally cover the native-shaped failure variants above and assert that error details survive, money is never retried, other cities remain isolated, and published status reflects HELD. Native testing, once authorized diagnostics are available, needs only one original confirmation until that gate works; do not request the full ten-turn session now.

This is a diagnostic/feedback proposal, not permission to change financial semantics or the persistence framework. Fixing the underlying failure should follow its concrete readback evidence. Existing B241 local completion, B240 acceptance, source/live deployment and frozen results stay intact.

User decision: authorize the narrow diagnostic/reporting repair if desired. User testing: paused; no immediate repeat or extra screenshot requested. Primary next: wait for authorization; no COM-C/D, deployment or unrelated repair.
