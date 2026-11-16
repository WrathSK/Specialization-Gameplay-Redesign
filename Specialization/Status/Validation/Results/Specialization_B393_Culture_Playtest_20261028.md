# B393.420 — Culture playtest follow-up, 2026-10-28

Evidence baseline: `3c3332475a172f2a9a69e332ad5498cc22d894c3`; current deployed runtime remains B393.420, sourced from `bca2c48`. This is a new evidence review, not a new runtime build or final U5 acceptance. The previous [partial playtest record](Specialization_B393_Partial_Playtest.md) remains frozen.

The user supplied an ability-by-ability Culture test record and a subsequent clarification about the deliberately deferred Culture network test. This document separates those observations from collector records, native CSVs, static source findings and unresolved causes. No gameplay code, tests, Design, Architecture, deployment or game configuration was changed; no game was launched and no native commands were sent.

## 1. Evidence and limits

- Latest substantive collector: `local/diagnostics/B205/session-20261029T002616Z-19ee60/`. It contains **1,910 TRAIN rows**, seq127–2036 with no internal gaps or duplicates, across T1–T27 and five observed Gameplay generations. Initial seq1–126 are missing because the ring had already advanced when collection began. Do not call the whole session complete.
- The preceding `session-20261029T001340Z-eed384/` contains37 TRAIN rows and was interrupted. It is a separate observation, not a substitute for the missing prefix.
- Four `LOAD_CLOSE` records occur at seq520/T3,1096/T16,1500/T19 and1957/T25. Collector summaries report `INTERRUPTED`; that is not proof of a game crash.
- Culture institution facts:184 READY records; specialized Culture UI replies:125 READY records. Relevant transitions are P1/A1→P4/A1 at T1, A2→A3→A4 within T3, A1 at T12 and A4 again at T14. These confirm the observed data path; visual correctness and exact ability yields still use the user's separate observations.
- Seven directly relevant deployed files were SHA256-matched against this checkout: DialogueProjects, ExpeditionSpyGate, ExpeditionSpyStore, Lv2GPP, CultureMeaningModel, UI/DialogueRefresh and UI/ExpeditionSpyActivity. No mismatch was observed. This is a scoped comparison, not a new full-package deployment verification.
- Sixteen raw files were copied, not moved, to ignored local evidence: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B393_Culture_Playtest_20261028/`. Each source/copy hash matched and each source remained unchanged during its copy. Total:1,747,964 bytes. Manifest SHA256:`4d2a3d83981036a6e1f1084c61c958786edc2d3b4f88f8b047a8b78caffcf685`. This is local evidence preservation, not an independent permanent backup. Raw logs are not published.
- Source labels below: `TRAIN seq` means the latest collector's records; `BQ` means the captured native `City_BuildQueue.csv`; `NATIVE_DB` means the current configured engine Gameplay DB, opened read-only. File line references refer to this source baseline.

Evidence labels: **USER_GAME_TEST_PASS/FAIL** are restricted to the user's stated scenario; **STATIC_CONFIRMED** describes code/DB facts; **UNKNOWN** is not success or confirmed invalidity. No local gameplay simulation was run for this read-only review.

## 2. User-observed coverage

| Area | This test establishes | Boundary or exception |
|---|---|---|
| Potential, ACTIVE and institutions | USER_GAME_TEST_PASS: investment updates institution/banner views; governor arrival and same-turn promotions activate each tier; III unlocks Dialogue, IV unlocks Expedition. | Not an all-lifecycle or all-UI-scale acceptance. TRAIN seq318/327/342 corroborate A2/A3/A4 at T3. |
| Tier I specialist support | USER_GAME_TEST_PASS: support works. | Do not invent an unrecorded numerical before/after sample. |
| Tier II housing | USER_GAME_TEST_PASS: housing works and is withdrawn when the governor leaves. | Full building-tier/pillage catalogue not independently covered here. |
| Tier II GPP / 文艺赞助 | USER_GAME_TEST_FAIL for automatically assigned specialists. Manually locking one/two specialists gives one/two shares; locking another plot does not repair it. Withdrawal works. | The working manual path does not accept the automatic path. Cause remains UNKNOWN; see section3. |
| Tier III / 风雅熏陶 | USER_GAME_TEST_PASS: benefit appears; selling the final work removes it; moving works out/back updates it. | The user's transient tourism-lens display defect recovered after reload. User explicitly requests no fix for that UI symptom. |
| Tier III / 时代对话 | USER_GAME_TEST_FAIL: waiting for timing, same-turn reselection blockage, no natural completion and no reward after forced native completion. | Startup/timer failure is supported; forced completion is not proof of a separate reward-formula defect. See section4. |
| Tier IV / 巨作启迪 | USER_GAME_TEST_PASS for the stated two-era, three-GPP-category comparison; other cities remain outside the percentage effect. | Does not prove every GPP class, all eight eras, stacking or full removal behavior. Arithmetic below supports the recorded values. |
| Tier IV / 意义延展: Campus | USER_GAME_TEST_PASS: effect and work transfers update promptly. | Other positive-yield domains remain separate tests. |
| Tier IV / 意义延展: diplomatic Culture | User observes no added Culture, matching the already deferred implementation. | Existing implementation limitation, not acceptance of the approved full nine-domain Design. Current code deliberately omits diplomatic/government Culture projection. |
| Tier IV / 意义延展: Neighborhood | User observes four Food per work after a passenger/transit building. | Not enough evidence to call this a defect: actual district depth/building set was not logged; see section3. |
| Expedition training, deployment and 风土考察 | USER_GAME_TEST_PASS in the normal-trained-unit scenario: first mission produces one archived insight; source-city tourism modifier shows2%; no spillover to other cities. | No visible integer tourism increase at that small base is consistent with the already accepted native-floor boundary. Does not accept every mission or restoration path. |
| Expedition / 艺文采撷 | USER_GAME_TEST_FAIL after save/load: no new insight and no actions. | Position/recovery protection stopped the process before reward; see section5. |
| Granted Spy/Expedition | USER_GAME_TEST_FAIL: diplomatic-building granted unit appears as an Expedition with no actions. | Grant identity/type is not independently logged; promotion-class collision is a strong candidate, not a proven engine selection algorithm. |
| Reload of other exercised abilities | User reports the other exercised abilities continue to work. | Expedition recovery specifically did not close; do not extend this observation to every persistent/history path. |
| Culture network | **BLOCKED / USER_PLANNED_DEFERRED**, explicitly clarified by the user. | Same foreign civilization needs all three insights. Works mission failed and early-game AI has no completed wonder. Test after Expedition repairs and a valid wonder target; not an accidental omission or a request to test now. |

### Two-era GPP arithmetic

Two distinct work eras imply+6% to this city's base GPP. Using the user's city baselines21/21/19 and other-city baselines3/1/1 gives:

| Category position in user record | Expected empire total | User display |
|---|---|---|
| First |21×1.06+3=25.26|25.3|
| Second |21×1.06+1=23.26|23.3|
| Third |19×1.06+1=21.14|21.1|

This explains the observed one-decimal display without inventing a gameplay rounding change or extending the test to all classes.

## 3. GPP and Neighborhood findings

**GPP:** [Culture Design](../../../Design/Culture.md#二级文艺赞助) requires actual working specialists, without a manual-lock requirement. [Lv2GPP.lua](../../../../Mod/Lv2GPP.lua#L35) reads Gameplay `plot:GetWorkerCount()` and derives carrier bits from that count at lines48–57. There is no explicit locked-specialist-count read. [EffectiveFacts.lua](../../../../Mod/EffectiveFacts.lua#L142) shares a sample only within the protected synchronous read phase; it is not a persistent per-turn worker cache.

Worker/focus notifications already exist in [NativeFacts.lua](../../../../Mod/NativeFacts.lua#L35) and [UI/GPPRefresh.lua](../../../../Mod/UI/GPPRefresh.lua#L64), with [FactConsumerBindings.lua](../../../../Mod/FactConsumerBindings.lua#L23) delivery; [Lv2GPP.lua](../../../../Mod/Lv2GPP.lua#L109) also audits at existing load/local-turn boundaries. Therefore neither “getter necessarily means locked workers” nor “there is no automatic-assignment event” is proven by this record. No current TRAIN row pairs actual specialist occupancy, sampled worker count, intended carrier bits and final GPP. The next investigation needs that narrow comparison on an already relevant change, without polling or broadening scans. Earlier accepted display-refresh delay does not explain away the user's automatic/manual distinction.

**Neighborhood:** `NATIVE_DB` identifies `BUILDING_JNR_TRANSIT_HUB` as Tier3, rather than the user's tentative Tier4. This is not enough to infer the tested city's full D. [Shared depth](../../../Design/Shared.md#区域基础设施深度) sums all current qualified building tiers within a single district, capped10; it is not just the highest tier. [CultureMeaningModel.lua](../../../../Mod/CultureMeaningModel.lua#L58) gives Food per work=`floor(0.5×D)`, so D8 or D9 yields4. The captured logs do not establish the exact Neighborhood building set, D or theming state; retain this as a calculation check, not a confirmed excessive-yield defect.

Diplomatic/government Culture remains deliberately deferred: [CultureMeaningModel.lua](../../../../Mod/CultureMeaningModel.lua#L4) lists seven active domains and lines38–39 exclude Culture writes. The user's negative result is compatible with that known limitation. It does not block independently supported Campus/Food outputs, nor close the outstanding approved Culture projection.

## 4. Dialogue: startup and selection findings

### Native and UI evidence

BQ602/T19 and633/T20 select `PROJECT_SPC_ERA_DIALOGUE`; BQ658/T21 adds only19 production against the deliberate1,000,000 native cost. BQ728–730/T23 show selection,1,046,855.1 forced production and exit to an ordinary project. These corroborate the user's failed timed-completion path; this is not merely a wrong countdown label.

[DialogueProjectUI.lua](../../../../Mod/UI/DialogueProjectUI.lua#L14) shows “待计时” when the native current target is Dialogue but there is no matching ACTIVE/CALLING/HELD view. It points first to start confirmation/timer ownership, not to the reward percentage formula.

### STATIC_CONFIRMED selection-cleanup gap

[DialogueProjectUI.lua](../../../../Mod/UI/DialogueProjectUI.lua#L51) clears the pending selection when its `Before` callback receives a different production target. It rejects another same-turn Dialogue click while that pending selection exists. [CrewProjectOrder.lua](../../../../Mod/UI/CrewProjectOrder.lua#L110) calls the shared `BeforeAll` for projects, but ordinary-unit `BuildUnit` at lines133–135 bypasses that notification. Replacement handling at lines151–155 only informs Expedition training.

Thus an unconfirmed Dialogue selection followed by an ordinary unit can retain its pending intent and refuse reselection until the next-turn drain at DialogueProjectUI64. This is a concrete path defect consistent with the observed project→ordinary-unit→next-turn reselection sequence. It does **not** by itself explain why the very first BEGIN failed.

### First-BEGIN blocker remains UNKNOWN

The following gates are not distinguished by existing logs:

1. [TimedProjectSelectionClient.lua](../../../../Mod/UI/TimedProjectSelectionClient.lua#L106) does not drain before the registered reader handshake is ready.
2. Its lines99–104 protect the queue read with `pcall` and consume the current read permission before the getter.
3. [DialogueProjectUI.lua](../../../../Mod/UI/DialogueProjectUI.lua#L65) sends BEGIN only for a current, successful read of the Dialogue target with queue size1.
4. [Gameplay.lua](../../../../Mod/Gameplay.lua#L101) does not independently publish the BEGIN failure result into this collected trace.

Minimum missing evidence is reader registration/epoch/wake status, one related queue-read result/size/error, and BEGIN receipt/pending-write outcome. Capture these scalar gates on existing events; do not add timer polling, arbitrary-event retries or a full-city fallback.

`TPR:UNKNOWN` in readiness summaries is not proof of a missing timed-project service: [TimedProjectReaders.lua](../../../../Mod/TimedProjectReaders.lua#L7) exposes epoch/readers/errors but no `.ready`; [ReadinessSummary.lua](../../../../Mod/ReadinessSummary.lua#L23) asks for that generic field. Treat this as a diagnostic-field mismatch, not as the established startup root cause.

### Forced native completion does not reconstruct a missing start

[DialogueProjects.lua](../../../../Mod/DialogueProjects.lua#L150) returns when no saved pending start exists. Consequently, if BEGIN was not committed, finishing only the native production item does not create a reward or consume the era opportunity; the project can remain eligible. This safety rule must remain. The current record does not prove that a properly started, uniquely completed Dialogue loses its reward.

Candidate next repair scope: correct ordinary-production replacement intent cleanup, add bounded observations at the three missing startup gates, then repair the demonstrated failing gate. Preserve full-turn timing, UNKNOWN protection and no reward replay.

## 5. Expedition: three distinct failures

### 5.1 Works task after reload: stopped before reward

| TRAIN evidence | Observed boundary |
|---|---|
|seq1866–1871,T25|After manual wake, Works reaches `TASK_RUNNING`, start25/due27, expected location57,8.|
|seq1906,loaded T25|Recovery starts with the saved task/unit identity. No subsequent `RECOVERED` or newly confirmed ASLEEP result closes that recovery in the captured records.|
|seq2020–2023,T27|Actual location56,7 differs from saved57,8; `TEAM_DISPLACED_STOP`, then `ACTIVITY_POSITION_CHANGED`, then persisted HELD/BLOCKED.|

[ExpeditionSpyGate.lua](../../../../Mod/ExpeditionSpyGate.lua#L459) verifies location before entering task processing, and line460 only enters the running-task completion path after recovery has cleared. The insight write at lines501–511 is later. Therefore this was not a successful task with a missing reward: the process stopped before the reward boundary. [ExpeditionSpyActivity.lua](../../../../Mod/UI/ExpeditionSpyActivity.lua#L45) also rejects the mismatched location during release. [ExpeditionSpyUnitPanel.lua](../../../../Mod/UI/ExpeditionSpyUnitPanel.lua#L52) returns an empty action table for missing/locked activity views; [ExpeditionSpyUI.lua](../../../../Mod/ExpeditionSpyUI.lua#L27) explains the BLOCKED lock. This accounts for the user's subsequent lack of all action buttons.

**Still UNKNOWN:** when and which component moved the unit, and why loaded activity recovery never produced a new confirmation. Native UnitOperations records travel/sleep/skip operations but no map-movement order for this unit. Do not assert that loading immediately displaced it or that the engine/HD is conclusively responsible. The first observed discrepancy is at T27. A scoped recovery sample must preserve actual position/activity and the pending lease without replaying a reward.

### 5.2 Skip/hold before starting Works

Seq1862–1864/T25 record native HOLD, `nativeReady=false`, Sleep permission denied and `ACTIVITY_SLEEP_NOT_ALLOWED`; no Sleep operation was attempted. The start safely returns to ARRIVED without a task timer/reward. Manual wake followed by seq1868–1871 produces AWAKE, allowed Sleep and TASK_RUNNING. This is an actual native-activity admission limitation, not an unresponsive click. Relevant checks: [ExpeditionSpyActivity.lua](../../../../Mod/UI/ExpeditionSpyActivity.lua#L295) and [ExpeditionSpyGate.lua](../../../../Mod/ExpeditionSpyGate.lua#L740). A future user-facing wake/start repair must retain fresh permission and activity-ownership checks.

### 5.3 Diplomatic-building grant: identity candidate versus proven UI handling

The configured read-only DB and the directly related HD `DLCSupport/DL_Ethiopia.sql:229–251` locate a diplomatic-building grant modifier `CHANCERY_ADD_SPY_WITH_PROMOTION`. Its dynamic effect is `EFFECT_GRANT_UNIT_OF_CLASS_AND_APPLY_ABILITY`, with `UnitPromotionClassType=PROMOTION_CLASS_SPY` as well as `UnitType=UNIT_SPY`. The actual DB attachment is `BUILDING_CHANCERY`; this identifies the grant chain without inferring the exact building clicked from the user's colloquial name.

[Our unit definition](../../../../Mod/Data/ExpeditionSpyGate.sql#L2) also has Spy=1 and `PROMOTION_CLASS_SPY`. That shared class is a strong candidate for native grant selection reaching the custom unit, despite the separate CLASS_SPY tag exclusion. The captured record does not identify the granted unit's exact native type/ID, so an erroneous display/recognition path is not excluded and the native selection algorithm is not proven.

The no-buttons result has a definite implementation explanation **if** the grant produced that custom type: [ExpeditionTraining.lua](../../../../Mod/ExpeditionTraining.lua#L167) only admits births under an existing TRAINING reservation, and [ExpeditionSpyGate.lua](../../../../Mod/ExpeditionSpyGate.lua#L878) binds a team only from its training completion proof. A native grant bypasses that proof. [ExpeditionSpyUI.lua](../../../../Mod/ExpeditionSpyUI.lua#L17) then has no matching ActivityView, and UnitPanel52 suppresses all actions. Do not silently adopt it into a culture city, expand the national cap, change HD or invent a grant-based insight owner.

### Scope and regression attribution

Relative to current main, ExpeditionSpyActivity, ExpeditionSpyUnitPanel, ExpeditionSpyUI and ExpeditionSpyGate.sql are unchanged; the affected strict-position, activity-admission and recovery mechanics also predate the refactor. The Gate's refactor changes concern history notification, entry selection extraction and capacity inputs. This is evidence of existing paths exposed by this test, **not proof that the entire current failure existed identically on main**; no paired native reproduction was performed.

Candidate repair order: obtain the missing recovery/activity/location evidence, repair the exact safe recovery path, separately verify grant isolation, then re-run Works across a save/load. Do not remove the position guard, guess a successful completion, blindly wake/replay irreversible operations or grant insights as compensation.

## 6. Remaining tests, without repeating demonstrated coverage

### Already planned or blocked

- **Culture network:** explicitly deferred by the user until Expedition repairs. Obtain all three categories for the same foreign civilization from one source city, including a valid completed AI wonder. Then verify delivery to another specialized city's own working specialists, source eligibility withdrawal/recovery, same-civilization deduplication and no merging of incomplete cross-source records. This is a planned follow-up, not an omission in the user's current run.
- **Dialogue:** a normal one-full-turn start/completion, one era opportunity, interruption/reselection, reward isolation and saved-history behavior depend on repairing the current start path. Forced native completion does not replace this test.
- **Expedition Works/reload and granted-unit handling:** currently failed. Wonder mission and successful three-category completion are downstream of the present constraints.

### Useful uncovered edges

1. **Meaning Extension's remaining active domains:** Industry, Commercial Hub/Harbor, Encampment and Holy Site; confirm per-domain flooring before same-yield aggregation. Government/diplomatic Culture is a known deferred implementation boundary, not a test-ready positive path. Neighborhood needs an actual D/building set before declaring its amount wrong.
2. **Current work diversity versus count:** add another work of an already represented era, remove the last work of an era, and remove all works; check Inspiration and Aesthetic without turning current coverage into historical-max behavior. Relics/products should not enter the qualified pool. Eight-era and percentage-stacking coverage remains optional later breadth, not a demand to reproduce every combination now.
3. **Scoped withdrawal/recovery:** one genuine building/district pillage→repair and ACTIVE withdrawal→return for the exercised dynamic effects. The already verified Tier II withdrawal need not be repeated solely for bookkeeping; other effects remain distinct.
4. **Expedition once-per-source/civilization/category and cap:** after a successful mission, a second equivalent target must not duplicate insight; the retained unit still counts toward the national cap. Do not require all cost/speed permutations for this narrow repair acceptance.
5. **No-window update:** close diagnostic/institution windows, change a relevant input, and inspect the actual result afterward. Opening a report should not be the necessary refresh trigger.

Longer lifecycle cases such as source loss/rebinding, ownership return, target invalidation and war remain broader integration coverage. They are not all upgraded to mandatory immediate repetitions by this investigation. Existing S9/S10/U5 limitations remain; this review changes no design or acceptance boundary.

## 7. Handoff

- **User decision:** no new gameplay decision inferred. The user's Culture-network deferral and no-fix request for the transient tourism lens are recorded. Technical findings do not authorize changes to rules or external Mods.
- **User testing:** do not repeat the demonstrated positive cases now. Network remains deliberately deferred; failed Dialogue and Expedition paths require targeted repair/retest before downstream acceptance. Automatic-specialist GPP remains FAIL with its causal boundary UNKNOWN.
- **Primary next:** use the bounded findings above for the next authorized repair batch; first-BEGIN and recovery-position gaps require explicit scalar evidence rather than speculative polling or weakened safety guards. Stop after this evidence/report batch; no runtime or deployment changes in this turn.
