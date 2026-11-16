# B394.421 — Culture diagnostic native review, 2026-10-28

Read baseline:`d4b58993d3d6f0216c87f4bfef8f54a3dca46fe3`;deployed source remains `ec3d6136361de91c47b0e83fa95606b65dc0d7bc`. This batch reads logs, records user acceptance and investigates current code. No runtime, tests, Design, Architecture, deployment or game configuration changes;no game launch or live commands. [B394 implementation evidence](Specialization_B394_Culture_Diagnostics.md) and [earlier Culture review](Specialization_B393_Culture_Playtest_20261028.md) remain frozen.

## Evidence scope

Collector `local/diagnostics/B205/session-20261029T025413Z-d62cae/` contains692 TRAIN rows,seq1–692 continuous with no gaps/duplicates,including212 CULTURE_DIAGNOSTIC rows,two load segments and T19–T28 observations. No LIMIT_REACHED/truncation row occurred. INTERRUPTED is the collector stop reason,not evidence of a game crash. TRACE_SINK_BUDGET_STOP concerns the separate native-error fallback,not loss of these continuous TRAIN rows. Continuity does not mean every game event was logged.

Times printed in records are UTC;the session is the user's2026-10-28 evening in America/Vancouver. Relevant second-load points occur at03:00:30 UTC/T25 and03:05:33 UTC/T27. All native CSV citations below use the matching captured final logs.

Sixteen source files totaling506,731bytes were copied without deleting originals to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B394_Culture_Diagnostics_20261028/`. Copy/source SHA256 matched and sources stayed unchanged during each copy. Manifest SHA256:`9058f6f6120be3db18f63021537f3d6cd79cf86e9976db8c625db9585a22135a`. This is local evidence preservation,not independent permanent backup;raw logs are not published. It includes collector records/summary/events/memory,production/governor/GreatPeople/UI/unit-operation logs,and directly related diplomatic logs.

## Additional user acceptance

- **USER_GAME_TEST_PASS:** Meaning Extension's Holy Site,Industrial Zone,Commercial Hub and Encampment were tested. The user specifically confirms combined Industry+Encampment behavior. Earlier Campus coverage remains;no unreported numeric sample is invented.
- **USER_GAME_TEST_PASS:** multiple eligible works of the same era do not add an extra covered era.
- Harbor was geographically unavailable and not directly tested. The user does not request extra Harbor coverage or consider it a current blocker. Both Harbor and Commercial Hub use the same Gold conversion/application machinery in [CultureMeaningModel.lua](../../../../Mod/CultureMeaningModel.lua#L4),which supports the user's inference. Their district/building identification inputs remain distinct,so the inference is not relabeled as a direct native PASS.
- Prior clear-all-works withdrawal PASS,no-deliberate-pillage requirement,and planned Culture-network deferral remain unchanged. No repetition or forced pillage is requested.

## 1. Dialogue: the immediate blocker is now confirmed

| Load/scenario | Observed chain |
|---|---|
| T19 |seq30 reader service ready;33/35/36/37 registration/wake/connect;155 selection;156 queue still OTHER;157–159 correct city events;160 correct Dialogue target,size1;161 transport returned;**162 BEGIN_GUARD ready=false,NOT_READY**;163 handler returned.|
| T26 after another load |seq304/307/309/310/311 readiness/registration/wake;556 selection;557 OTHER;558–560 correct city events;561 Dialogue target,size1;562 transport returned;**563 BEGIN_GUARD ready=false,NOT_READY**;564 handler returned.|

Neither attempt has BEGIN_COMMITTED or DIALOGUE_SAFE_FAILED. The native request reaches its handler and exits at [DialogueProjects.lua132–134](../../../../Mod/DialogueProjects.lua#L131),before qualification/queue validation,history write,timing or reward. Thus these failures are not caused by an unreadable target,wrong city event parameters or an unwoken UI reader. Native production accumulating against the deliberately huge native cost is the result of never creating the independent timer,not a reason to lower that cost.

The controller's private ready flag starts false. [Sync126–129](../../../../Mod/DialogueProjects.lua#L126) or [its load callback291–294](../../../../Mod/DialogueProjects.lua#L291) can set it true. Reader-service READY is a separate state. Global load observations exist at seq134/414,with corresponding readiness AFTER_LOAD rows135/415,but the new trace does not observe this controller's own Sync/load entry or instance identity. **Confirmed:**the actual BEGIN handler instance remains uninitialized. **UNKNOWN:**why its specific initialization path did not establish readiness;callback delivery,Sync delivery and instance association are not yet distinguished. Do not replace this with the unrelated TPR:UNKNOWN diagnostic-field issue.

The earlier ordinary-unit selection-intent cleanup gap remains a separate static finding. Strongest next direction is to close Gameplay initialization at a reliable existing Store/load availability boundary,then retain the existing related-event queue flow and explicit start outcome. This review does not authorize forcing ready=true on arbitrary requests,bypassing Store checks,adding polling,or synthesizing missed rewards.

## 2. GPP: the observed sample-to-carrier chain works;automatic assignment remains unresolved

| TRAIN seq | Boundary | Culture source city65536 |
|---|---|---|
|75→76|T19 audit|3 sampled specialists;required base6;observed carrier plan6;no other-profession residual.|
|352→353|T25 after loading|3 sampled specialists;required6;observed6.|
|570–581|T26|Six pairs of native worker-change and UI worker-dirty deliveries were recorded. No new distinct sample row followed;do not infer each audit succeeded from change-only silence.|
|628→629→630→633|T27|Native worker cause→AUDIT sample2→required4/observed4→UI dirty.|

For Culture,the2points per working specialist apply independently to Writer/Artist/Musician base GPP. These are configured base amounts,not the final empire Great People UI totals. [Lv2GPP.lua](../../../../Mod/Lv2GPP.lua#L48) uses Gameplay GetWorkerCount;[CarrierSet.lua](../../../../Mod/CarrierSet.lua#L33) supplies the original presence preflight and changed-bit readback. This evidence rules out a missing event or missing carrier update **for the T27 change**. It does not prove the original early-game automatic-assignment scenario was repaired.

There are only three GPP_SAMPLE rows,all AUDIT;no READ_ONLY samples. The trace has no automatic-versus-manually-locked assignment label or simultaneous authoritative population-management occupancy. Consequently it cannot discriminate whether the early discrepancy lies in native sample visibility/timing or final native GPP refresh. Manual locking is not a Design requirement. The next scoped technical comparison must pair actual assignment/lock state,the exact current getter result and installed/final benefit;do not ask the user to redo the full Culture suite or assert that Getter means locked workers without evidence.

### A diagnostic label defect,not52 proven gameplay failures

The52 GPP_FAILED rows must not be counted as52 business failures. [Lv2GPP.lua81](../../../../Mod/Lv2GPP.lua#L81) unconditionally labels its target-report callback as failure. [RuntimeWork.lua226–231](../../../../Mod/RuntimeWork.lua#L226) also calls that callback after success,with why=nil,to clear the prior error. Successful seq76 is followed by such an UNCLASSIFIED row77,and success353 by354. The observer converts nil into generic error metadata.

This is an introduced diagnostic-accuracy defect;the callback's actual business error clearing and carrier writes are unchanged. Fixing the label later is a narrow diagnostic correction,not a new gameplay repair or reason to relax safety. Other rows with insufficient metadata remain uninterpreted rather than automatically declared failures or successes. No logging code is changed in this analysis batch.

## 3. Expedition: early recovery acknowledgement and later displacement are separate

| TRAIN seq | Evidence |
|---|---|
|316,T25|UI RECOVER read is READ_OK;native activity38434027,the previously established Sleep hash;actual and expected position both57,8. This occurs before this load's readiness/load-close observations412/414.|
|449,T26|Gameplay still reports RECOVERING for the saved TASK_RUNNING/ASLEEP task,start25,due27.|
|616,T27|Still RECOVERING at the next turn boundary.|
|618–622,T27|Actual position56,7 differs from expected57,8;position protection and activity-release read fail;the team ends HELD/BLOCKED.|

No RECOVERED GATE_RESULT is present. The initial read is not an unreadable unit or the Operation-state waiting branch in this observed sample. [Activity acknowledgement88–109](../../../../Mod/UI/ExpeditionSpyActivity.lua#L88) first marks that mode's one-shot slot and cancels its job,then calls UI.RequestPlayerOperation. A false return is not inspected;an exception is printed as ACTIVITY_ACK_UNKNOWN. The fixed [collector reader pattern](../../../../tools/read_expedition_trace.py#L35) does not collect that tag. Therefore the strongest present candidate is an early load-time one-shot acknowledgement that never reaches the relevant Gameplay handler and is not sent again. The actual transport return/throw/ingress is not sampled,so this is a candidate,not a proven lost request.

Even before the later displacement,the persisted task's recovery was not closed. Finding the displacement source alone would not establish that task completion had become healthy. The relevant next boundary is exact recovery send→receive→commit proof on a reliable existing initialization boundary,without replaying Sleep or reward and without adding periodic retries.

UnitAdded seq393–394 is the saved unit1572875 being republished during loading,with TASK_RUNNING and preserved training evidence. It is not a new training success or proof of another granted Expedition. No new diplomatic-building completion/granted-unit reproduction is present in this session;that identity issue retains its prior candidate status.

## 4. Border closure: retain the lead without inventing causality

**User observation:** Babylon appeared to close borders in the same turn,and the game reported a unit removed from foreign territory. This is relevant evidence and must not be discarded because it lacks a matching log row.

**Captured native evidence:**DiplomacySummary's only Open Borders row is a T25 proposal from owner1 to0,followed by HUMAN_REFUSE_DEAL in DiplomacyManager. The Expedition target is owner2;the proposal does not establish Babylon's border closure or an active border agreement. T27 also records a city-state11 suzerain-war event. Neither event proves the Expedition's movement cause. There is no recorded owner2 border-expiry/closure row and no notification body naming the expelled unit.

No EXPEDITION_MOVE_EVENT or EXPEDITION_OPERATION_EVENT was captured;native UnitOperations has no movement order for this team. This means the displacement was not observed through those selected hooks,not that no native relocation occurred. The owner of56,7 was not logged. A one-tile offset alone does not prove whether it was actually outside the target's territory,ordinary expulsion,city-center occupancy adjustment or another native relocation.

[Our definition](../../../../Mod/Data/ExpeditionSpyGate.sql#L3) and the read-only loaded DB show Spy1,DOMAIN_LAND,CIVILIAN,IgnoreMoves1,Stackable1,PromotionClass SPY and TeamVisibility0;the ordinary Spy has TeamVisibility1. The implementation uses native travel plus a custom task that requires GetSpyOperation=-1 and a real unit at the target center ([Gate688–714](../../../../Mod/ExpeditionSpyGate.lua#L688));the [activity path](../../../../Mod/UI/ExpeditionSpyActivity.lua#L337) uses native Sleep and an independent task timer. It is a hybrid path,so Spy1 alone is insufficient evidence that every native Spy border/stationing exemption applies identically. Conversely,native travel did occur and C++ stationing state is unobserved;do not claim it definitely lacks native registration.

The accepted [Culture diplomatic rules](../../../Design/Culture.md#外交资格与目标失效) require no Open Borders and allow war. If border-driven expulsion is later confirmed,it is an implementation/adaptation problem;it does not authorize requiring Open Borders,cancelling on war or silently changing mission legality.

## Handoff and scope

- **User decision:** no new gameplay decision. Additional Meaning and same-era acceptance is recorded;Harbor remains untested but not a current blocker;no deliberate pillage or immediate network expansion.
- **User testing:** no repeat of the accepted Culture cases requested by this review. Current evidence has narrowed the failures;any additional collection should target only the remaining initialization/ACK or assignment-read boundary after the next authorized engineering step.
- **Primary next:** no runtime changes in this batch. Recommended bounded next work is Dialogue initialization plus the already identified intent cleanup,Expedition recovery-ACK proof before displacement adaptation,and GPP assignment/sample/final-output comparison. Correct the false GPP failure label separately within that scope. Preserve optional observer removal,safety guards,permanent records and no-polling constraints. Existing S9/S10 and final U5 remain open.
