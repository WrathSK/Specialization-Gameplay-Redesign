# B246 native review — Development quotation, debit and contract lifecycle

Date: 2026-10-18 (America/Vancouver; collector filenames use 2026-10-19 UTC). Reviewed develop HEAD `8aa10f8`; unchanged implementation/deployment **B246.273 / modinfo273**, source `6398be1`. **USER_GAME_TEST_PASS for the submitted quotation/debit, selected-district effect, specialist reduction, running-contract cold-load and completion/slot-release cases.** Simultaneous Standardization plus Development remains **NOT_EXERCISED**, without a newly identified defect or an immediate retest request.

## Accepted results

The user confirms actual +50% Production, no bonus to other buildings during the contract, continued effect after removing Commercial Hub specialists, withdrawal and slot release after building completion, and a complete game exit/restart. Logs corroborate the matching contract transitions. Effect traces describe configured modifiers; the actual native Production result comes from the user's observations, not a conversion of configured values into measured yields.

The 69 quotation observations all satisfy `cost = theoretical Gold price * 0.15`; they represent 11 distinct target/domain/building/price combinations. The selected native prices include 200, 240, 880, 900, 1200, 1800 and 2000. The following four confirmations each have one readable native debit followed by a strictly saved ACTIVE receipt and owned effect application:

| Contract / target city | Quote building | Theoretical price | Requested / actual debit | Before -> after Gold | Absolute error |
|---|---|---:|---:|---|---:|
|1 /131073, Entertainment|HD Salon|1200|180 /180|9220.0625 ->9040.0625|0|
|2 /327684, Commercial Hub|JNR Merchant Quarter|900|135 /135|9040.0625 ->8905.0625|0|
|3 /524295, Commercial Hub|JNR Merchant Quarter|900|135 /135|8905.0625 ->8770.0625|0|
|4 /589832, Theater|HD Art Publishing House|1800|270 /270|19788.8671875 ->19518.8671875|0|

Total Development debit: **720 Gold**. Maximum observed absolute error: **0**, within the accepted **0.01 Gold per call**. Independent decimal recomputation of before/after/requested values matches every reported delta/error. All four observations report RETURNED / READABLE / moneyAccepted=true. Each is followed two sequence positions later by DEVELOPMENT_SIGNED/ACTIVE, after the final receipt save; the intervening event is the owned +50% application. There is no repeated Development debit for a signed contract in either captured timeline.

All four contracts originate in Commerce city393221. IDs and quote buildings identify observations only; the accepted contract continues to bind target city plus district, not the selected quote building. The trace contains the selected quote and candidate count, not every alternative's price. Native availability and the15% calculation are observed; minimum selection among all alternatives inherits the exact selection/read-failure regressions in the [B246 local result](Specialization_B246_Development_Investment_Local.md#local-verification), rather than claiming a new independent comparison of unseen prices.

## Completion, capacity and cold load

G1 and G2 below are diagnostic Gameplay-context aliases, not operating-system process identities.

| Timeline | Captured sequence / turns | Development debit / signed | Completion | Interpretation |
|---|---|---:|---:|---|
|G1|21–308 /T43–45|4 /4|1|Three contracts fill the source slots; one completes; a fourth then signs in the freed slot.|
|G2|27–125 /T45–46|0 /0|0|Three still-active contracts restore from the save; the completed contract stays closed.|

- **Signing:** G1 seq100/102,164/166,184/186,305/307 are monetary/signed pairs, raw lines80/82,144/146,164/166,289/291. The first three debits form one continuous treasury chain. Later treasury changes are not attributed to Development.
- **Completion and release:** G1 seq271 (line251) removes the owned effect from target131073; seq272 (line252) records contract1 COMPLETED after `BUILDING_HD_SALON` appears. Source UI was CAPACITY_FULL at seq235/236, becomes READY at seq301, and accepts contract4 before returning to CAPACITY_FULL at seq308. This demonstrates withdrawal, release and actual reuse of the slot. It does not claim all four contracts completed.
- **Reconstruction:** G2 seq57–59 (lines323–325) remove the three owned loaded effects; seq60–62 (lines326–328) reconstruct +50% for targets327684,524295,589832. No effect is restored to completed target131073. There is no new DEVELOPMENT_MONEY or DEVELOPMENT_SIGNED in G2, and OPEN reports the remaining occupied capacity. The user's explicit cold-restart confirmation supplies process-level evidence; socket/context changes alone do not.
- **Specialist decline:** confirmed Commerce observations in G2 show source workers3 at seq86,2 at seq92, and2 at T46 seq122. No Development closure or additional effect withdrawal follows. This agrees with the user's continued native effect after removing specialists. Temporary pending reads reporting0 are not treated as proof that every specialist was removed.

## Standardization and remaining evidence boundaries

All **40** captured Standardization observations for the four Development targets have `expected=0` and `sourceCount=0`; verified STD_READY observations are present for each. The separate Industrial city65536 has an earlier14% projection, but is not one of these investment targets. Therefore this session does **not** establish native additive stacking, such as14%+50%=64%, on the same building. The existing separate-owner Production implementation/local checks remain intact. Carry this one combination forward to a convenient later test, without repeating the completed signing/cold-load flow or blocking an unrelated next batch.

No DEVELOPMENT_FAILURE or readback failure is captured. The 23 CAPITAL_FAILURE entries are existing COMMERCE_PENDING/NETWORK_PENDING quote-dependency waits, not Development monetary failures. They do not prevent the observed signatures or existing Capital settlements; no Capital repair is opened here.

The trace contains387 unique TRAIN records with continuous sequences inside both captured windows. Their initial prefixes are unavailable. Two collector partial-frame deadlines and socket waits occur around collection/reconnection; complete monetary/receipt chains and the six reconstruction effect records are present. The session ends INTERRUPTED; that label is not a gameplay failure or evidence of a cold restart. Missing prefixes are not invented.

This review does not add native acceptance for all alternative quote buildings, new Owner-change cases, interrupted native calls, destroyed cities, non-Standard speed, or all possible Gold amounts. Those retain their existing local coverage/deferred boundaries. The137 selected local methods (57 new,80 retained) are inherited unchanged, not rerun or relabeled as native tests. No new user session is requested for this review.

## Evidence retention

Original files remain unchanged and ignored under `local/diagnostics/B205/session-20261019T042612Z-c77476/`. This is a local evidence locator, not a public download link. No new screenshot was present; the submitted logs and explicit user observations suffice for the accepted scope.

| File | Bytes | SHA256 |
|---|---:|---|
|records.log|158399|`a209fe6e1eb00bfb2f0f1815c5d5e0be037a73d82986cc1462b2cd1ad4c4777c`|
|events.jsonl|4504|`80b7014ce3959d81ad241ceb0139f2dd95172678bf512de22662b9b2a0ef9693`|
|summary.txt|1025|`8aadbaae3735a55caf20e12ff5849cc62808b33050dd6d856686c3d46df5ebad`|

The offline parser/arithmetic script and derived JSON are retained under ignored `local/diagnostics/B246/native-review-20261018/`. They check unique/continuous captured sequences, all69 quote calculations, four exact debits and saved-receipt pairing, completion/reuse, restored targets, no reconstructed debit, and the absence of a positive Standardization projection on investment targets. This is offline evidence analysis, not a formal gameplay test or live Tuner operation. Original logs and previous validation reports remain frozen.

## Checkpoint

B246 is accepted within the observed scope; no implementation defect is identified here. All260 source/runtime files still match, digest `62d72cfdb6c3986de9c6e7199967dae2106d3d96ef60a777598236a8cf36d020`; receipt `B246.273-6398be1-playtest.json` remains DEVELOP_ACTIVE without a pending marker. Main stays `e901a22` /B069.96. This review updates only its result, existing planning/current navigation and reviewed hashes; no source, Design, formal tests, runtime, configuration or deployment changes.

User decision: review the [B247 Asset Restructuring proposal](../../../Architecture/v2/Commerce_Preparation.md#b247-proposal--asset-restructuring); implementation remains unauthorized. User testing: no immediate repeat; retain the single additive Standardization case for a later convenient combined session. Primary next: normal documentation checks and commit/push, then stop.
