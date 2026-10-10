# B177.204 — cumulative Dialogue automatic integration: native result

Date: 2026-10-09. Four original screenshots visually reviewed. All identify **B177.204 / modinfo204** and **EDINBURGH (TEST)**. Recorded deployed source: `3bb10790f32256ad20d339a62cc24de3c3269c82`; receipt: `B177.204-3bb1079-playtest.json`. Deployment provenance is inherited from the existing record; this review did not compare or modify the external runtime.

**USER_GAME_TEST_PASS within the observed automatic-integration scope:** existing earned history is projected, current qualification pauses/restores the carrier without erasing history, and a subsequent project completion updates the earned total and carrier together. This closes the [bounded B177 integration check](Specialization_B177_Dialogue_Cumulative_Local.md#one-minimal-user-integration-check), not every P0-M lifecycle or native-yield combination. The implemented path remains the already accepted **Tourism-only fallback**.

## Observed sequence

Values below are displayed by the actual B177 report. Work Culture/Tourism are combined for the city's sampled works, not each work or nationwide income.

| Image | Turn | Current qualification | Earned total / current carrier | Project / opportunity | Current collection | Work Culture / Tourism |
|---|---:|---|---|---|---|---|
| 1 | 76 | Culture ACTIVE IV | +5% / +5% | Medieval used; previous successful completion sampled one era, +5 points | 2 works, 2 eras | 9 / 15 |
| 2 | 76 | Culture ACTIVE I | +5% / 0% | Medieval still used; completed history retained; report says current qualification insufficient | 2 works, 2 eras | 9 / 15 |
| 3 | 82 | Culture ACTIVE IV | +5% / +5% | Renaissance unused; Dialogue started T82 and is counting the full turn; city queue shows 1 turn | 3 works, 3 eras | 15 / 23 |
| 4 | 83 | Culture ACTIVE IV | +20% / +20% | Renaissance used; completed and saved; completion sampled 3 eras, +15 points; city queue now empty | 3 works, 3 eras | 15 / 23 |

Image1's background collector reason is `LOAD_SCREEN_CLOSE`; image2 has `GovernorAssigned`; image3 has `WORK_INPUT_CHANGED`; image4 has `PlayerTurnActivated`. These corroborate the reported event context, not a complete event trace. All four show an accepted native-reader response and no displayed projection hold/error. The sequence does not establish whether the initial load followed a full process restart; no such new claim is needed or made.

## Findings and evidence limits

- **Load/current-state reconstruction:** image1 shows the saved +5% automatically represented by the current +5% carrier. B177's normal **时代对话** button is read-only. The displayed projection follows earned history, not the retired two-era +25% formula. B175's separately recorded user-confirmed cold-restart history evidence remains unchanged.
- **Qualification withdrawal and restoration:** images1→2 show ACTIVE IV→I and current +5%→0%, with +5% history and the used Medieval opportunity retained. Image3 shows ACTIVE IV and +5% restored before another completion. Exact intermediate Governor travel/establishment timing was not photographed.
- **Successful commit propagation:** T82→83 changes unused→used and +5%→+20%, exactly `5 + 3 × 5 = 20`. The current carrier matches the new total in the completion report; no manual activation path is needed. This is the newly required after-commit integration evidence.
- **Carrier versus yield:** the report's carrier value is the projection's confirmed building write/readback state ([implementation](../../../../Mod/DialogueEffects.lua)), not an independent enumeration of every native Modifier instance. The screenshots do not isolate a positive credited Tourism delta: work Tourism remains15 at +5%/0% and23 at +5%/+20%. Small percentages may round away under the accepted native-floor contract; these readings alone prove neither the exact rounding/order nor a missing benefit. The earlier [B176 accepted comparison](Specialization_B176_Acceptance_Clarification.md) supplies the scoped 0/100/200 Tourism primitive evidence. Do not multiply the already-buffed15 or23 as a subtotal or reintroduce the withdrawn city-Culture settlement gate.
- **Meaning and scope:** these four reports do not show Meaning's five individual additions. Their independence remains supported by unchanged implementation, local coverage and the prior B176 fixture; it is not newly measured here. Tourism-only applies no Culture or other yield percentage. All-native-yield separation remains unimplemented. No broad claim about every city, work type, theme, ownership transition or performance follows from this session.

## Checkpoint and next boundary

The approved B177 automatic-integration batch is complete within this native scope. The prior [B175 project/history result](Specialization_B175_Dialogue_B174_Native_Result.md), [B177 local result](Specialization_B177_Dialogue_Cumulative_Local.md) and frozen B176 records retain their original scopes. The existing historical localization-count assertion mismatch remains recorded; no assertion was changed or gameplay test rerun for this evidence review.

No additional B177 test is requested. No Design decision, implementation repair, N/U2 work or all-native prototype follows automatically. Await the user's next batch decision. Gameplay source, tests, Design, GC, main and runtime are unchanged; this checkpoint records evidence/current documentation only.

## Original evidence archive

All four PNGs were visually read, then moved without renaming or re-encoding from ignored `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B177/2026-10-09/`. **4/4 SHA256 equality verified**, 51,011,976 original bytes. No image is committed. This table is the evidence manifest for the report.

| Image | Original filename | SHA256 |
|---|---|---|
| 1 | `Screenshot 2026-10-09 at 10.20.09 PM.png` | `73f689cf00908084cff690402717a5da49d66b04b763ee6765193f328db9b78e` |
| 2 | `Screenshot 2026-10-09 at 10.20.46 PM.png` | `7a7428d723251c4897fe8ba7c4be5cb41844a418e218baa27820b1652b4c5f47` |
| 3 | `Screenshot 2026-10-09 at 10.25.07 PM.png` | `809d08696680f5f59a2b9d920e19478f0b3fe6dc180cd83ce08fb0caf6150d4e` |
| 4 | `Screenshot 2026-10-09 at 10.25.42 PM.png` | `acddb4c2cfc4737e305462d3fa27963fadfc3db42b05f228c46d0f167a327f17` |
