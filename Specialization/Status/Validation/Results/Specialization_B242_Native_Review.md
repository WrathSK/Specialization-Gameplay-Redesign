# B242 native review — pre-debit failure and missing readback diagnostics

Date: 2026-10-18 (America/Vancouver; collector folders use UTC). Review basis: develop `4f32cec`; deployed source `7dda421`, **B242.269 / modinfo269**. This is evidence review and a proposed narrow repair, not implementation or deployment.

## Review summary

**USER_GAME_TEST_FAIL: Capital confirmation still fails.** The new stage/code identifies **DEBIT_INTENT_WRITE / STORE_WRITE_UNCONFIRMED**, before the calling receipt and Treasury debit. The refreshed published view correctly stays **HELD / canSign=false**; refresh acknowledgement no longer claims CAPITAL_READY. However, every intended readback-difference field is absent. B242 therefore supplies useful failure-stage and paused-state evidence, but does **not** complete its readback diagnostic goal or repair signing.

The missing fields are a concrete defect in the diagnostic failure boundary. The new projection calls `rawget` without a capability guard, while the existing Mac GameCore_Tuner evidence already records that function as unavailable. The Store catches and discards observer exceptions, and the projection assigns its result only after completion. A missing function can consequently erase the entire readback observation. The unchanged actual Store/service reproduces this exact diagnostic shape locally with `rawget=nil`. This is strong evidence for the missing-diagnostics cause, not proof of the underlying Property discrepancy or a direct B242 Gameplay-global capability observation.

No amount, formula, save record, game configuration or runtime was changed during this review. No further native test is requested before the diagnostic defect is repaired under separate authorization.

## Original evidence

Original files remain unchanged and ignored under `local/diagnostics/B205/session-20261019T021241Z-313951/`. The preceding `session-20261019T021230Z-55ecbc` has zero records and supplies no gameplay evidence. The B205 prefix identifies the collector family, not the build.

| File | Bytes | SHA256 |
|---|---:|---|
| records.log | 25904 | `d06c42199f21fd52fa5183afc8e3065651c68a19880e3acd1e8fa922bf4a4577` |
| events.jsonl | 844 | `45d6df22e6a6f8e9697510affd59fcdf345c86c36996c7bc25ad0080ef71ab44` |
| summary.txt | 458 | `5d750c1af903bda7480d62458a71337412c022273c5025592a82efd58f4f5407` |

There are **71 contiguous records, seq20–90**, all T34 in one captured Gameplay context. Transport reconnects occurred and collection ended INTERRUPTED, but the confirmation and refresh interval is complete. Earlier records before20 are not reconstructed. `alerts: none` does not mean gameplay PASS. Seven directly relevant source/live files were rechecked byte-identical: CapitalInvestment, CapitalInvestmentDiagnostics, CityProgressionStore, ExpeditionTrainingDiagnostics, CapitalInvestmentPanel, Probe and modinfo. The previous251-file deployment receipt remains the full-package provenance; this review did not redeploy or claim a new full-package check.

| Sequence | Evidence | Interpretation |
|---|---|---|
| 65/66 | CAPITAL_COMMERCE_PENDING during REFRESH_READ | Initialization wait, followed by Commerce READY; separate from signing failure |
| 77–83 | Commerce publications and CN_READY | The later Capital quote is not blocked by unresolved network initialization |
| 84/85 | Research quote; OPEN accepted, READY/canSign=true | Treasury18004.92578125, principal4501.2314453125, D3/S1/C1.25/R2, safe4670.0276245117, dueT44 |
| 86 | DEBIT_INTENT_WRITE; STORE_WRITE_UNCONFIRMED | First saved intent cannot be confirmed; the execution path has not reached native debit |
| 87/88 | REFRESH_READ/PROGRESSION_HELD; CONFIRM rejected, HELD/canSign=false | Store failure protection remains active |
| 89/90 | Manual REFRESH accepted; reason PROGRESSION_HELD, HELD/canSign=false | Read request succeeded, signing did not recover; no misleading READY acknowledgement |

There is no CAPITAL_MONEY, CAPITAL_SIGNED or settlement record in the captured interval. The observed failure phase and source order establish that this confirmation did not enter the Treasury mutation. A final native Treasury balance was not captured; no unrelated balance claim is made. The paused **published state** is verified; rendered text/pixels were not separately inspected.

## Readback evidence gap and direct cause review

The seq86 line is complete and short, with neither readPoint, readStatus, writeStatus, recordType, savedPhase, savedMatches, diffPath nor expected/actual values. Those fields are already allowlisted by [the trace emitter](../../../../Mod/ExpeditionTrainingDiagnostics.lua); the source/live copies match. This is not evidence of an equal readback or a resolved Store error.

Direct paths inspected:

- [CapitalInvestment.lua](../../../../Mod/CapitalInvestment.lua), lines36–42: the callback assigns `attempt.readback` only after `D.Readback` returns. Lines283–298 order INTENT → CALLING → native debit → ACTIVE receipt. Lines151–164 and303–327 retain HELD views and distinguish request acknowledgement.
- [CityProgressionStore.lua](../../../../Mod/CityProgressionStore.lua), lines213–219/237–242/1055: the observer is forwarded. Lines898–920 perform modern-record prewrite/postwrite checks, invoke the observer under pcall and preserve failure protection. Its pcall result is discarded. The legacy collection branch also has no observer; it must not be confused with a successful observation. Current Gameplay starts the modern Store and Capital service in the same Gameplay initialization path, so there is no evidence here of a separate Capital-to-Store context bridge.
- [CapitalInvestmentDiagnostics.lua](../../../../Mod/CapitalInvestmentDiagnostics.lua), line8: unguarded `rawget` is the first table-field read inside the projection. An exception loses the already known point/read/write/type facts because the caller receives no partial result.
- [Existing native reader evidence](Specialization_B205_Expedition_Reload_Diagnostics_Local.md), Reader defect section: GameCore_Tuner has no rawget. [Reader](../../../../tools/read_expedition_trace.py):114 and [existing offline coverage](../../../../DevelopmentTests/test_expedition_trace_reader.py):377–384 already avoid it and test its absence. B242's new tests use a standard Lupa environment, and its observer-throw test proves safety but does not require visible diagnostic-failure metadata. That omission let a known environment hazard reappear.

The B242 session does not include the suppressed observer error or a direct check of rawget in its specific Gameplay context. Accordingly, **missing observer-failure reporting and the unguarded dependency are STATIC_CONFIRMED defects; rawget absence is the leading explanation for the native field loss**. This does not identify whether the actual Property write was ignored, reshaped, quantized, unreadable or otherwise mismatched. Do not loosen equality, Floor amounts or reconstruct a contract from its cached candidate on this basis.

## Bounded local discrimination

The actual unchanged B242 Store/service was run with the logged quote inputs. Five scenarios alter only fixture Property behavior and the availability of a standard-library function; no formal test, runtime or external data was edited. Reproduction and JSON output are retained ignored under `local/diagnostics/B242/native-review-20261018/`.

| Property double | rawget | Result | Money calls / diagnostic result |
|---|---|---|---|
| Exact write/readback | Present | ACTIVE | One debit; balance13503.6943359375 |
| Ignored write | Present | INTENT_WRITE failure, HELD | Zero; POSTWRITE/RETURNED, diffPath=capital |
| Ignored write | Absent | Same failure/HELD | Zero; all readback fields disappear, matching native symptom |
| One safe-return scalar rounded to float32 | Present | INTENT_WRITE failure, HELD | Zero; POSTWRITE/RETURNED, diffPath=contract.safe with expected/actual values |
| Same injected rounding | Absent | Same failure/HELD | Zero; all readback fields disappear again |

All failed scenarios remain HELD/canSign=false after refresh. **LOCAL_SIMULATION_PASS for five discrimination cases only.** The two different Property failures becoming indistinguishable demonstrates why the log currently cannot justify a monetary or storage repair. Float32 remains an injected alternative, not a native engine finding.

## B243 proposal — reliable failure observation

**PLANNED_NOT_AUTHORIZED.** Repair the observation boundary before changing financial persistence.

1. Remove the projection's unguarded rawget dependency. Use the established checked ordinary access on already copied plain record tables. Capture minimal point/read status/setter status/types/equality metadata **before** detailed comparison, so a projection exception cannot erase these facts.
2. Catch projection errors explicitly and retain a bounded diagnostic-status/error-class/module/line result, separately from the original STORE error. A callback not observed must remain explicit, never interpreted as matching data. No raw Property dump, names, request tokens, hidden risk outcomes or arbitrary error strings. Keep the original Store failure and no-replay guard unchanged; do not add retries, extra Property reads, polling or a second logger.
3. Preserve enough finite numeric precision to distinguish expected/actual scalars without changing the values. Compare only the fixed safe schema; an unlisted difference remains explicit. Keep the first useful confirmation failure through refresh, alongside truthful HELD/canSign=false.
4. Add targeted actual-Store tests with rawget absent, an intentionally throwing projection, ignored/altered/unreadable readback and successful unchanged writes. Require diagnostic visibility as well as zero pre-debit money calls, unchanged amounts/write counts, no retry and other-city isolation. Reuse existing tests; do not repeat whole gameplay regression or old native lifecycle tests.

Expected implementation surface: CapitalInvestmentDiagnostics and its CapitalInvestment callback, any strictly necessary safe scalar trace fields, one focused test file and normal build/result/context metadata. Touch Store only if needed to expose the existing observation status without changing commit semantics. Collector transport and economic model should remain unchanged. Underlying save/precision repair follows actual readback evidence; a required monetary rule change remains DESIGN_DECISION_REQUIRED.

After authorized local repair, the only native delta should be one original-save confirmation plus one paused refresh with the existing collector. No 10-turn wait, second domain, cold-load sequence or repeat now. Success means a complete bounded readback or an explicit diagnostic error, with the same safety boundary; it is not automatically contract acceptance.

User decision: review/authorize this narrow diagnostic repair. User testing: paused; none now. Primary next: record this evidence and plan, then stop. COM-C/D, Culture HOLD, unrelated audits, gameplay changes and deployment remain outside this review.
