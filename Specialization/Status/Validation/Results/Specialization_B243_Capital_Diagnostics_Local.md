# B243 local result — reliable Capital failure observation

Date: 2026-10-18. Source basis: develop `380688d`. Build: **B243.270 / modinfo270**. The user explicitly authorizes removal of the diagnostic rawget dependency and visible diagnostic exceptions, preserving economic amounts, save verification and no-double-debit protection. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The underlying native signing failure remains unresolved.

## Implementation boundary

The [B242 native review](Specialization_B242_Native_Review.md) is preserved. It shows an intent-save failure before debit and correctly held refresh, but no detailed readback observation. B243 repairs that missing evidence without treating a diagnostic failure as a successful save.

| Surface | Narrow change |
|---|---|
| CapitalInvestmentDiagnostics | Replace rawget with guarded ordinary reads of the Store's copied plain tables. Preserve the same fixed-field comparison, equality result and privacy exclusions |
| CapitalInvestment write callback | Before detailed projection, retain the already-obtained read point, readable/error status, setter returned/threw status, observed type and full equality result. Protect both projection and merge; report COMPLETE or ERROR separately from the original Store failure |
| Unreached observer | NOT_OBSERVED explicitly means no observation was delivered. It does not invent a read error, equal record or recoverable state |
| Existing bounded trace | Add five diagnostic-status/error fields. Only expectedNumber/actualNumber use round-trip numeric formatting so a small difference remains visible; stored values, computation and comparisons are unchanged |
| Package | Advance the build stamp/modinfo to270; no new runtime files |

The callback reuses the existing failure-only Store observation. It adds no native Property query, retry, scan, event registration, timer or frame update. Request-local metadata and the existing per-city replaceable failure view retain their owners and exit conditions. Error output remains allowlisted codes/classes/basenames/line numbers; arbitrary messages, paths, names, tokens and hidden outcomes are excluded. KEEP64/BUDGET96 and existing record-size limits remain.

CityProgressionStore, CapitalInvestmentModel and both Capital UI modules are byte-identical to the source basis. Money calculations, fractional values, Treasury tolerance, write/readback guards, intent/calling/receipt order, reservations, HELD behavior, per-city isolation and no-replay rules are unchanged. No automatic refund, re-sign, save migration, schema field, gameplay rounding or new Commerce ability. Design, other professions, GC, main, configuration and frozen evidence are unchanged.

## Local verification

**123 targeted test methods PASS, no remaining failures/errors/skips:**13 B243 restricted-Lua checks,68 retained B241/B242 business/UI/diagnostic checks,22 shared bounded-trace checks and20 offline collector checks. The13 new methods include seven actual-Store fault subcases and four invalid diagnostic-result subcases.

- With rawget absent, the actual service/Store successfully handles the fractional local signing/settlement control; ignored/altered/throwing writes and unreadable/missing/scalar readback retain their distinct failure evidence. Prewrite conflicts still call no setter. These are simulated faults, not identification of the native Property discrepancy.
- Projection, result-type and merge exceptions retain base readback facts and a separate diagnostic error. They preserve the original Store code, held refresh, zero pre-debit money calls and independent normal-city operation. Non-string errors cannot invoke arbitrary object stringification.
- A failed settlement receipt with a broken diagnostic projection still does not replay the native credit after reconstruction. Repeated refresh keeps existing bounded records and never authorizes another debit.
- One-ULP expected/actual differences survive the unchanged collector parser; both values round-trip through the log. The actual collector itself and its command behavior are unchanged.

The actual B242/B243 service comparison preserves each saved value and Treasury result as well as Property work, with rawget absent in both fixtures:

| Scenario | Property reads | Setter calls | Successful writes | Native money calls | Cross-record uniqueness visits |
|---|---:|---:|---:|---:|---:|
| Successful signing and settlement |14|7|7|2|0|
| Ignored intent write and rejected repeat |2|1|0|0|0|

This is local behavioral/access equivalence, not proof of native CPU, memory, save precision or financial acceptance. The prior restricted-library defect was absent from older fixtures; this result closes that local coverage gap only.

Eight changed/direct Lua files compile. All250 unique modinfo entries exist and, together with modinfo, equal the251-file package; XML/version checks pass. One DB-dependent fixture initially lacked its existing external-DB configuration, and20 collector tests initially lacked permission to create ignored local fixtures; those environment issues were corrected and the unchanged cases rerun successfully. No assertion was weakened. The ignored summary is `local/diagnostics/B243/local-validation.json`.

Current selectors, reviewed hashes, changed document links/anchors and diff checks pass; the staged-publication gate passed before commit. Only reviewed changed/new entries are updated; no all-history rehash. No broad gameplay regression or native PASS is claimed.

## One minimal native diagnostic session

Start the existing manual collector and load the same **pre-confirmation** test save. This observes the repaired diagnostic boundary only; the full native contract test remains deferred.

1. **城市生产列表 → 资本投资 → 科研 → 确认稳健投资**: confirm once.
2. If paused, click **刷新报价** once. The view must remain honestly paused with confirmation unavailable; stop and return the collector log. It should now include readback facts plus COMPLETE, or a distinct diagnostic ERROR/NOT_OBSERVED instead of silent field loss.
3. If signing succeeds, stop and return that log. No repeated confirmation, second domain,10-turn wait, new cold-load sequence or screenshot series is needed here.

The next decision depends on the captured difference: missing record, numeric discrepancy, another structural mismatch or an explicit diagnostic error. No amount correction is pre-approved; a native limitation requiring a gameplay change remains a user decision.

## Handoff

User decision: none for this approved diagnostic scope. User testing: the short session above after deployment. Primary next: await the single diagnostic log after the verified W0003 deployment below. The build can still pause because B243 does not bypass the unresolved save failure. COM-C/D and other deferred work remain outside scope.

## Verified deployment

B243.270/modinfo270 from clean/pushed `c696104d3718a2dcd0f1423fea1b3e3961341a2a` is DEVELOP_ACTIVE. Receipt `B243.270-c696104-playtest.json`;251/251 source/runtime files MATCH, digest `9163784f4cf855974e2bd9a9d5d46f0bd436b958f0e14e85c4ebdd92900d0a43`. Fresh automatic game-exit checks passed immediately before exact B242 restoration and B243 activation. B242/stable recovery is retained, with no pending transaction. Main/configuration and frozen prior evidence are unchanged; no game launch. Native signing remains unaccepted; stop for the single diagnostic session.
