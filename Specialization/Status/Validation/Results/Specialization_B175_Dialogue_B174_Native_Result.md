# B175.202 — Dialogue first-slice native result and B174 observations

Date: 2026-10-09. Package: **B175.202 / modinfo202**; source `886484a69189ac6c5cdacfd409f065f66957387f`, recorded receipt `B175.202-886484a-playtest.json`. Eight originals reviewed; the user's operation and restart confirmations are identified separately below. This is an evidence/documentation update only. No source change, deployment, new gameplay test or engine launch by Codex.

**Dialogue project/history: USER_GAME_TEST_PASS within the observed first-slice scope.** Investment completion and Lv2 Housing: scoped user-reported PASS. Scientist specialist response matches the expected displayed delta. Engineer GPP retains an unexplained national-rate residual; neither a B174 defect nor a package-refresh cause has been established. No repair or additional GPP test is requested.

This result supplements the frozen [B175 local result and combined flow](Specialization_B175_Dialogue_Project_Local.md#一次合并验收流程) and [B174 local result](Specialization_B174_Investment_Propagation_Local.md). It does not replace their local evidence or imply full P0-M acceptance. **The new cumulative Dialogue yield multiplier remains unimplemented; +5% below is saved history, not a measured new yield bonus.**

## Dialogue: screenshots and operation evidence

The selected Culture city is EDINBURGH (TEST); the panel identifies B175.202 and Culture ACTIVE IV.

| Image | Visible facts | Supported conclusion |
|---|---|---|
| 1, T70 | Cumulative +0%; Medieval opportunity unused; current eligible era count 2; last result says production interrupted, attempt cancelled without consuming the era. Cinema is the ordinary current target. | Observed cancellation retains zero total and unused opportunity. |
| 2, T70 | Dialogue is current production with a 1-turn display; report says full-turn timer running, start T70 / Medieval; current eligible era count 1; total remains +0%, opportunity unused. | Normal project entry and running timer observed. |
| 3, T71 | Production UI says Dialogue completed and queue is empty; report says full-turn completion saved, completion X=1 → +5 percentage points, cumulative +5%, Medieval opportunity used. | Normal next-turn completion, correct recorded amount and used-era state. The report does not identify this as exceptional forced completion. |

The user explicitly confirms the second-era work was moved out **after restarting the Dialogue project**. Thus the tested attempt changed from two eras to one during execution and credited `5 × 1 = 5`, not a stale start-time `5 × 2 = 10`. Timing is user-confirmed; images 2–3 independently show the reduced collection and the completion result. Image 1's two-era display is from the preceding cancelled attempt, not a screenshot of the second attempt's exact start instant.

The user initially had not checked the era record after reboot, then stated they would start the game and check, and subsequently confirmed **both +5% and the used era are correct**. Record this as **user-reported post-restart persistence PASS**, with no new post-load image. The reported total also supports no duplicate award on that load. Do not claim Codex observed the restart, inspected the save, or independently captured a post-load production-selection attempt.

Coverage remains bounded: one city, one Game Era, one successful normal turn, the observed cancellation and changed completion-time collection, and the user's restart confirmation. Cross-Game-Era starts, X0, all ownership/UNKNOWN/failure paths and other-city isolation retain their existing local/inherited evidence; they are not newly native-tested here. Used-era state is observed/confirmed; explicit attempted same-era re-selection was not separately reported. No repeat shared lifecycle ceremony is added.

## B174: investment, Housing and specialist response

The user confirms normal investment performed correctly and Lv2 Housing is correct. Image 5 at T76 shows the Research city record with Potential=2, ACTIVE=2, KNOWN, one completed investment, no pending investment and a present ledger. Image 4 shows the same city with four working Campus specialists; the city panel shows population/Housing 6/19. The Housing **delta** is the user's observation; the images do not supply a before-investment Housing comparison. Image 7 also shows an Industry Lv2 city badge, without independently documenting its investment sequence.

The user describes image 6 as the baseline, image 7 after removing four Science specialists and one Industry specialist, and image 8 after restoring them. These native Great People screens show **national rates**, displayed to one decimal, on consecutive turns T76/T77/T78:

| Class | Image 6 baseline | Image 7 removed | Image 8 restored | 6→7 | 7→8 | 6→8 |
|---|---:|---:|---:|---:|---:|---:|
| Great Scientist | 88.9 | 64.9 | 88.9 | −24.0 | +24.0 | 0.0 |
| Great Engineer | 35.9 | 31.5 | 38.1 | −4.4 | +6.6 | +2.2 |
| Great Merchant, contextual comparison | 33.5 | 35.9 | 35.9 | +2.4 | 0.0 | +2.4 |

- **Scientist:** the observed −24/+24 matches the user's expected four-specialist response at displayed precision and returns to the baseline. These images do not support the initial suspicion that this Scientist removal failed.
- **Engineer:** +6.6 after restoration is compatible with a base +6 subject to +10%, but the actual modifier pool/source has not been established. Removal was −4.4, not the same magnitude, and the final rate is +2.2 above baseline. Retain that discrepancy as **UNKNOWN attribution**, not a confirmed stale carrier or a rounding explanation.
- Merchant also changes despite not being part of the declared specialist adjustment. Together with the different turns and the lack of a complete controlled source inventory, this prevents assigning every national-rate change solely to the selected city's specialist update. It does not itself identify the cause of the Engineer residual.
- These are displayed **rates**, not measured credited stocks or an isolated I→II GPP before/after pair. No exact all-class investment-GPP PASS, independently verified unaffected-city PASS, native performance improvement or universal stacking formula is inferred.

The B174 implementation changed the scope of confirmed-investment propagation, not its GPP amount definitions or the ordinary worker-change formula, as recorded in its reviewed local result. The native observations support successful investment/Housing and the observed Scientist worker response; they do not establish a B174-specific failure. Existing local equivalence/fault coverage remains valid at its stated evidence level.

The user's suggestion that a changed test package left an old carrier unrefreshed is retained **only as a hypothesis**. Supporting games begun with the Mod does not establish that every later package-update anomaly is harmless; package updates and enabling the Mod for the first time in an existing vanilla save are different situations. This observation does not justify reopening broad GPP attribution, declaring every GPP path passed, or implementing a repair. Keep the residual non-blocking unless a comparable reproducible current-path failure supplies a concrete reason to investigate.

## Next boundary

The first Dialogue project/history slice has the requested scoped native support, including the new saved record. The later cumulative native-only yield projection and old Dialogue writer retirement still require their own approved implementation slice. No N/U2, other profession, audit repair, GC change, extra user test or deployment starts here. Earlier B173 accepted API behavior and non-blocking numerical unknowns remain unchanged.

## Original evidence archive

All eight images were visually reviewed, then moved without renaming/re-encoding from ignored `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B175/2026-10-09/`. **8/8 SHA256 equality verified**, 91,797,076 original bytes. No screenshots are committed; the inbox directory and unrelated files remain. This table is the evidence manifest for this result.

| Image | Original filename | SHA256 |
|---|---|---|
| 1 | `Screenshot 2026-10-09 at 8.12.46 PM.png` | `ecaf5a5a303e335d04bec1b56e64399d7715b98d9dfe46d71f6805f36847df56` |
| 2 | `Screenshot 2026-10-09 at 8.13.25 PM.png` | `e50df065766f6220698105a5ec74ac985db9353306fe3900e82ab556d43c21f5` |
| 3 | `Screenshot 2026-10-09 at 8.14.06 PM.png` | `2ba3a9aa0082516f07bb1cfded60dea342c3fa30c0f27a3bcee1d37d302a7ba3` |
| 4 | `Screenshot 2026-10-09 at 8.18.31 PM.png` | `36424c26185381c91e765b5d53eef624e36751ed98d501cbeecf4c09f93c9bf1` |
| 5 | `Screenshot 2026-10-09 at 8.18.38 PM.png` | `ac408e171864cc504ab617b3a26b88770fff6ce3d606158ca5e583dd1b6dc976` |
| 6 | `Screenshot 2026-10-09 at 8.22.31 PM.png` | `59d6246f65fa6647c3799b972abc529b4aa3138cbe73ad10d15d604474bc43a2` |
| 7 | `Screenshot 2026-10-09 at 8.23.26 PM.png` | `d4dfcf3ad39d692fcb1f690b0b9ce3887e60d0a1e779d43abdc6770616c93e19` |
| 8 | `Screenshot 2026-10-09 at 8.24.59 PM.png` | `99ea7baab6617a8fedf513ac8c72b1d79aa9617f28f9fce8a5a40440afee4e51` |
