# B245 native review — signing, cold-load and bounded monetary receipts

Date: 2026-10-18 (America/Vancouver; collector filenames use 2026-10-19 UTC). Reviewed develop HEAD `b519702`; unchanged implementation/deployment **B245.272 / modinfo272**, source `006bf9c`. **USER_GAME_TEST_PASS for the submitted signing, running-contract cold-load and maturity cases.** Every captured native debit/credit is within the user-accepted 0.01-Gold bound. No repeated debit or credit is observed for a contract within any captured loaded timeline.

## Accepted results

The user confirms that at least one T43 contract load followed a complete Civilization VI exit and restart. The logs independently show two T43 reconstructions of the same three running contracts, no new signing/debit, and their matching T44 settlements. This closes the combined native gate in the [B245 local result](Specialization_B245_Capital_Receipts_Local.md), including the previously unaccepted Capital-only numeric codec path. Cold restart is user-confirmed evidence, not inferred from the collector's socket status or context IDs.

All 251 source/runtime files still match, digest `58201248325c9430ccada071ca242211400c394eb1830d6d950edfe496f19a0b`; receipt `B245.272-006bf9c-playtest.json` is DEVELOP_ACTIVE, without a pending deployment marker. Main remains `e901a22` / B069.96. This review changes no runtime, configuration, gameplay Design, Architecture, tests or deployment.

The main T34 run signed three contracts across two cities. A means city ID 393221; B means 524295. The initial earlier A/Research signing is a separate loaded timeline and has the same successful debit result.

| Contract | Requested principal | Actual debit | Absolute debit error | Requested maturity return | Actual return | Absolute credit error (approximately) |
|---|---:|---:|---:|---:|---:|---:|
| A / Research / Stable |4501.2314453125|4501.234375|0.0029296875|4670.0276245117193|4670.02734375|0.000280761719296|
| A / Culture / Venture, success |3375.9228515625|3375.92578125|0.0029296875|3502.5199584960942|3502.51953125|0.000427246094205|
| B / Research / Stable |2531.94140625|2531.94140625|0|2557.2608203125001|2557.2578125|0.003007812500073|

Maximum observed debit error: **0.0029296875 Gold**. Maximum observed credit error: **0.0030078125000727596 Gold**. All **13** captured transfer observations (4 debits and 9 credits across separate loaded timelines) report READABLE / RETURNED / moneyAccepted=true. Independent recomputation from before/after/requested values matches every actual delta and signed error. Direction and nonzero movement are correct; both floating-point and decimal-text comparisons remain below 0.01.

Each debit is immediately followed by CAPITAL_SIGNED/ACTIVE; each credit is immediately followed by CAPITAL_SETTLED with the same observed amount. These are after the existing strict final-receipt write, not merely a UI success message. T44 matches the locked due turn. The two requested stable returns equal principal times their locked 1.0375 and 1.01 multipliers; the requested successful venture return equals principal times 1.0375 (three times its 1.25% quoted profit rate). B245 has not changed those formulas.

## Loaded timelines and repeat-payment check

Labels below identify diagnostic Gameplay contexts, not asserted operating-system process identities. A contract key includes city, domain and contract sequence; a numeric sequence alone is not globally unique.

| Timeline | Captured sequence / turns | Signing / debit | Credit / settlement | Interpretation |
|---|---|---|---|---|
| G1 |25–99 / T34|1 /1|0 /0|Initial successful A/Research signing; UI_SHUTDOWN follows.|
| G2 |119–450 / T34–44|3 /3|3 /3|Fresh explicit confirmations from the original opening balance, followed by all three due settlements.|
| G3 |471–580 / T43–44|0 /0|3 /3|Saved running contracts restored; one credit per contract at T44.|
| G4 |601–711 / T43–44|0 /0|3 /3|Another T43 reconstruction; the same one-time results at T44.|

G2 debit observations are seq185/190/197, lines142/147/154 in the first log; settlements are seq435/437/439, lines392/394/396. G3 settlements are seq555/557/559, lines85/87/89 in the second log. G4 settlements are seq685/687/689, lines195/197/199. Each settlement is preceded by its monetary observation at the previous sequence/line.

The G1 and G2 A/Research debits both start from 18004.92578125 Gold, and G2 has a new explicit confirmation. They are not two debits against one continuously reduced balance. Likewise, all three T44 credit chains (G2/G3/G4) start from **9359.5625** and end at **20089.3671875**, with each prior after-balance equal to the next before-balance. The repeated credits therefore belong to replaying a pre-maturity save, not nine accumulating payments in one timeline. Each loaded contract has at most one recorded DEBIT and one CREDIT; neither T43 reconstruction has a confirmation or debit.

## Coverage and diagnostic limits

- The 628 captured records are unique within their sessions. Internal gaps are seq100–118 and 581–600; seq451–470 is outside the two session ranges. These surround load/session boundaries. The signing and settlement pairs themselves are present and adjacent. Missing records are not guessed or treated as proof of absence.
- All 98 CAPITAL_FAILURE records are dependency waits: 62 CAPITAL_COMMERCE_PENDING and 36 CAPITAL_NETWORK_PENDING. The quote-preparation path requires current Commerce/network facts; the inspected [Capital service](../../../../Mod/CapitalInvestment.lua) distinguishes those waits from monetary/Store failures. Every timeline ends with the two observed Commerce cities READY and the common network CN_READY. No captured money-unconfirmed, receipt-save failure, held transaction or termination appears; the waits did not prevent the observed settlements.
- The collector was run with idle_exit=30; a temporarily unavailable socket during loading can end a session. Its GAME_EXITED label alone does not prove a cold restart. The user's explicit confirmation supplies that fact; no extra game run is needed for this review.
- No second transfer appears in the captured post-settlement interval. The trace does not explicitly show the planned repeated panel reopen, a later-turn settled-save reload, interrupted native calls, or a native losing venture. Those are not newly claimed native PASS. Existing [142-method targeted local coverage](Specialization_B245_Capital_Receipts_Local.md#local-verification), including no replay and failure protection, is inherited unchanged. No repeated lifecycle test is requested.
- The observations do not establish a universal native Gold unit, all amounts, all contract outcomes, or all Commerce lifecycle behavior. They do establish the requested bounded receipt/signing/cold-load/maturity gate. No new gameplay defect or implementation need is identified in this batch.

## Evidence retention

Original logs remain unchanged and ignored at `local/diagnostics/B205/<session>/`. These are local evidence locators, not public downloadable links. No new screenshot was present in the inbox and none was needed for the monetary result.

| Session / file | Bytes | SHA256 |
|---|---:|---|
|session-20261019T031914Z-9a1e66 / records.log|161088|`3e2ae995c59259cd845b67c1aeec0d7c5f9422f5349f9b2551aad69bf8800681`|
|session-20261019T031914Z-9a1e66 / events.jsonl|8545|`c696b94e16511e0f6a5f9bb8fd08f5c8377e078c73468cd72c3229a9bbad8beb`|
|session-20261019T031914Z-9a1e66 / summary.txt|536|`60b77068f3916c28df100c0362ef066db1c9e5bee8fd0ffa5341ef915e5afa91`|
|session-20261019T034728Z-93d37f / records.log|85931|`5bb2bc086971e9b0bf9f216de5982813077d5c89da3cb7817cbc22b990be0171`|
|session-20261019T034728Z-93d37f / events.jsonl|1461|`eab4840983c47838a34ff7b4d2504047efc3857a1554a4ec449f990570bac178`|
|session-20261019T034728Z-93d37f / summary.txt|480|`0b2a8af5114d71c4ca00e23ec1ac9f199d3cd04a27f84c850ef095ed2ae5b59c`|

The offline arithmetic/grouping script and its derived JSON result are retained under ignored `local/diagnostics/B245/native-review-20261018/`. They reuse the existing collector parser, verify exact delta/error and receipt pairing, compare restored terms/credit chains, and count phases by loaded timeline and contract. This is evidence analysis, not a new gameplay regression, live Tuner operation, or change to formal tests. Raw originals and prior B241–B245 results stay frozen.

## Checkpoint

B245 is complete within the tested scope. Current Status/Authority/P0-H and only their reviewed/new report hashes are updated; runtime provenance is unchanged. Normal document/context/publication checks and explicit commit/push apply. User decision: none for B245. User testing: no additional B245 retest requested. Primary next: stop and await direction for the next Commerce batch; no automatic COM-C/D, implementation or deployment.
