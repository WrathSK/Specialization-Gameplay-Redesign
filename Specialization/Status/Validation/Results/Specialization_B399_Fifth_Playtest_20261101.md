# B399 fifth playtest — Commerce settlement, continuity and remaining UI limits

2026-11-01. Primary evidence intake at source baseline `0a59886`;live B399.426 from `4915170`,344/344 files and package hash unchanged. D0058/A0183 remain current. This records **USER_GAME_TEST_PASS within the described scenarios**,separates user observations from instrumented native readbacks,and retains UNKNOWN causes. No runtime,Design,Architecture,test implementation,game configuration or deployment change.

## Evidence and archive

Private local archive:`local/legacy-workspace/Specialization/Status/Validation/Evidence/B399_Fifth_Playtest_20261101/`. **78files /38,559,558bytes:**12collector files,64updated native logs and2visually reviewed original screenshots. Logs are copied;screenshots are moved from ScreenShots with unchanged filenames and SHA256 verification. All78archive hashes match;no PNG remains in the inbox. Manifest SHA256 `b71cefd91d4234291ed8f233cb8ed713ac57725ff291022b9bf46bd57102b3cb`. Raw evidence stays ignored/private;this local archive is not a permanent external backup.

| Alias | Collector session suffix | TRAIN records | Observed contexts/turns |
|---|---|---:|---|
| A |20261102T004757Z-f42f40|2,125(seq1–2125)|A1:T58→63;A2:reloadT60→64|
| B |20261102T013807Z-6423aa|706(seq1–706)|B1:cold loadT63→67|
| C |20261102T015236Z-2aee79|704(seq1–704)|C1:cold loadT67→72|

Total **3,535TRAIN records/four Gameplay contexts**. Citations below are physical records.log lines;use TRAIN seq for ordering because live/snapshot collection can append earlier sequence numbers later. Each session's captured sequence set is continuous. A/C have explicit partial-frame deadline gaps later covered by captured sequence snapshots;this does not prove every engine action was instrumented. Passive sink budget stops remain explicit. Boundary change sampling truncates once in A;GetSpyOperation/activity/border reads can be UNAVAILABLE. Readiness still reports TPR/DP UNKNOWN;CA changes from PENDING to READY by the first local turn. Those status labels do not prove all production paths are covered. The64latest native files cover the final cold run,not overwritten earlier native production logs;early production figures therefore remain user observations plus Mod-effect evidence.

Screenshots:`Screenshot 2026-11-01 at 6.53.53 PM.png` =67T,Gold6,926,GPT+96.5;`Screenshot 2026-11-01 at 6.54.39 PM.png` =68T,Gold19,653,GPT+96.5. Both3840×2160originals were inspected before moving.

## Accepted scope and boundaries

| Area | User observation | Corroborating evidence / limit |
|---|---|---|
| Dialogue |Complicated queue changes recover when only Dialogue remains;cross-era completion pays reward without consuming next-era opportunity|Sole-project recovery accepted. A157/2109 contain committed starts;the reward/era-slot outcome is user-confirmed,not independently fully serialized by this trace. Multi-item timing remains a nonblocking future consideration by user direction.|
| Commercialization |61T shows58;leaving governor stops it;reload/return behaves|A1323–1326/A1897–1900 show58 and exact domain inputs. A1602/A1634–1635 then B/C show0with ACTIVE_III_REQUIRED. B410–422 resumes58on return;B721/C114withdraws again. No national counterfactual isolates only this income from every concurrent change.|
| Capital |Re-signed this run,then cold load with governor absent;68T paid|Three new58Tcontracts,three verified native credits/settled receipts at68T,not the previous smaller two-contract replay. No duplicate debit/credit observed through72T. Both venture contracts succeed;failure/protection and a new reload after settlement are not independently exercised here.|
| Development |Three contracts survive fewer experts;switching to another domain gets no wrong bonus;completion removes the old effect;capacity frees;governor absence/reload preserves existing contracts|Four signed contracts including replacement;verified50→0carrier changes and cold reapplication. Production progress is user-confirmed in the early run,not reconstructed from final-run native logs. Police eligibility is explicitly parked by the user.|
| Reputation |58Tstart,61T3,66T8,72T14;counts without governor and across cold restart|COMMERCE age samples match exactly,including inactive periods. Effective bonus is still gated by ACTIVE4;no40-turn cap or failed-venture refund scenario is inferred.|
| Standardization |Overlapping Monument templates take the stronger5-layer purchase discount;route loss removes it|User-confirmed purchase behavior;C133reports two sources/max20,then C195zero targets after route loss. Specific native production progress was not tested this time.|
| Restructuring |Potential1cannot liquidate;−75%non-Food/surplus effect;5-turn gate;no automatic configure;newly built Campus selectable;Research3abilities work|B463/472:trained/liquidated66T;C30restores REALLOCATING after cold load;C577confirms manual Research configuration72T from start66/due71. Result log follows native consumption/readback. Button identity issue remains separate below.|

No new GPP,pillage,city-ownership or repeated no-P0 test is requested. User notes one P0 use at61Tto remove the displaced Expedition;A reload branches each contain a corresponding END,not a requirement to keep P0 open.

## Capital: exact68T reconciliation

[A432/440/448] signatures use25%of the then-current Treasury. All due68T. Quoted probability is **success** probability;outcome and amounts are locked on signing. [CapitalInvestmentModel.lua](../../../../Mod/CapitalInvestmentModel.lua),135–175:stable=`principal×(1+r)`,successful venture=`principal×(1+3r)`. [CapitalInvestment.lua](../../../../Mod/CapitalInvestment.lua),235–265:one guarded credit and verified settled receipt,without ACTIVE qualification at maturity replacing existing valid references.

| Contract | Signed principal | r / success probability | Locked due payout | Actual credit at68T |
|---|---:|---|---:|---:|
| Industry stable,#1|4,499.2890625|30%;stable|5,849.07578125|5,849.07421875|
| Culture venture,#2|3,374.466796875|7.5%;46%;SUCCESS|4,133.721826171875|4,133.71875|
| Research venture,#3|2,530.849609375|1%;41%;SUCCESS|2,606.77509765625|2,606.7734375|
| Total|10,404.60546875|—|12,589.572705078125|**12,589.56640625**|

Actual debit total10,404.609375;sub-cent differences are within the existing0.01native readback tolerance. C217–222 contains exactly one CREDIT and one SETTLED for each contract,in Research→Culture→Industry order. Balance immediately before credits is7,064.359375,then9,671.1328125→13,804.8515625→19,653.92578125. This explains the large screenshot jump;it is not three copies of one payout.

The complete67→68balance bridge is exact:

`6,926.80078125 + 41 + (290.55859375 − 194) + 12,589.56640625 = 19,653.92578125`.

C171/188/207–223:the first41is already present at LOCAL_BEGIN/STARTED;ordinary net96.55859375is posted before the three credits. The screenshots' integer Gold and96.5GPT agree with these precise native balances/net. Attribution of the separate41remains UNKNOWN;settlement arithmetic itself closes without an unexplained residual. Subsequent C69–72records contain no additional captured CAPITAL_MONEY/SETTLED rows.

## Commercialization, reputation and Treasury probe

At61T R3,three D6domains use factor1.015. A1323–1326 and its A2repeat show Culture58.09765625→17.690736328125→17Gold,Industry105→31.9725→31,and Harbor total Food35→10.6575→10. Sum **58**,not floor(total raw60.320736328125). This follows [CommerceCalculation.lua](../../../../Mod/CommerceCalculation.lua),31–44. A1494records applied carrier58at END61. Source changes explain55at early62before the governor's departure;A1602thenwithdraws to0. B/C maintain0while unqualified,even as reputation grows.

Age progression is directly sampled:A1323T61age3,A1683/B115T63age5,B256T64age6,B351T65age7,B422T66age8,B576/C114T67age9,C230T68age10,C573T72age14. [Commerce.lua](../../../../Mod/Commerce.lua),151–155,separates preserved age from currently effective ACTIVE4bonus. Development contracts continue separately;they are not new Commercialization income.

The new observer locates repeated extra credits **before LOCAL_BEGIN**,not just before GameEvents.PlayerTurnStarted. A868→921→938→943 shows END58=6,712.296875,LOCAL_BEGIN/STARTED59=6,753.296875(+41),ACTIVATED59=6,950.8984375(+197.6015625,exactly that start-point Yield−Maintenance). C67→68has the same41before ordinary net and Capital settlement. A2's63→64interval is52instead. Building/district/unit/WMD maintenance rows and exact balances are now captured,but do not name the posting source. PT017 therefore remains UNKNOWN;do not call it duplicate Commercialization,rounding,or a fixed universal52. No Treasury setter or foreign-Mod rule was changed.

## Development: contract-specific continuity

A463contract1:CityCenter/Granary quotation32.25,target393221. A563contract2:Industry/Factory240,target196610. A571contract3:Culture/ArchaeologicalMuseum108,target65536. All emit50%effects. A1148–1149withdraws contract2on a newly completed eligible Industry building(`BUILDING_JNR_CHEMICAL`),without requiring that exact original quotation building. A1214contract4thenuses freed capacity for a CommercialHub quotation240in the same target;A1213applies only that domain. This matches the user's domain-switch/no-leak and slot-reuse observations.

A2cold reload removes/reapplies three physical effects atA1815–1820. B63restores all three50%effects despite absent governor;C67retains Culture and CommercialHub after contract1ends atB560–561when Granary completes. [DevelopmentInvestment.lua](../../../../Mod/DevelopmentInvestment.lua),104–147,owns eligible newly completed-building detection,withdrawal,receipt and freed reservation. These are configured effect/readback proofs plus the user's observed production increments,not a new claim about all build categories.

The user's Police experiment is retained **without deciding legality or changing Design**. The signed CityCenter baseline is Granary;the observed Police progress is a different current production target. Contract1's captured close is67TGranary,so the62Treset-to0progress must not be relabeled as that contract's confirmed close. Reported early progress and later completion are kept in their actual evidence scopes.

## Standardization, Dialogue and restructuring details

C133(67T)reports26building templates/eight district templates,two source entries,max20;C195(68T)reports zero templates/max0after New York→Baltimore expires in native Game_TradeManager.csv2(67T),followed by San Francisco→Baltimore4(68T). Source count alone does not prove every counted source is eligible. The user's purchase comparison is the per-template native observation;[StandardizationEffects.lua](../../../../Mod/StandardizationEffects.lua),189,merges each target by max,and [EngineeringStudy.sql](../../../../Mod/Data/EngineeringStudy.sql),19–25,defines5layers as20%construction/10%building purchase. No extra production test is inferred.

Dialogue's source stores consumed era at `used[p.era]`,the accepted start era([DialogueProjectModel.lua](../../../../Mod/DialogueProjectModel.lua),68–75). This corroborates the reported cross-era opportunity result but does not replace user-game evidence. The present sole-project check deliberately rejects MULTIPLE([TimedProjects.lua](../../../../Mod/TimedProjects.lua),7–13);user asks to retain multi-item automatic timing as a **nonblocking later item**,not a separate progress-blocking repair batch. No timing rule is expanded by this intake.

Restructuring66→71wait and manual72configuration survive cold loading. New specialization RESEARCH/Potential3,history display,support,Housing,CrossDiscipline and AppliedLearning after IndustryD3are accepted from the user's observation. The initial D1AppliedLearning expectation is corrected by that observation,not recorded as a remaining bug. Non-Food/surplus disruption and new Campus choice are also user-confirmed;no city-loss semantics are inferred.

**PT019,new UI observation:**user reports the left confirm button inert while the action labeled liquidation performs the confirmed operation. Current [RestructuringUI.lua](../../../../Mod/RestructuringUI.lua),38–47,assigns distinct PREPARE/CONFIRMcallbacks but reuses the same icon;[Restructuring.lua](../../../../Mod/Restructuring.lua),203–225,only allows irreversible work through a valid confirmation plan. The trace proves one liquidation and one configuration,with no REST_REQUEST_HELD;it does not record clicked button/entry action or prove the visual button mapping. Keep the user-reported mismatch open for scoped UI investigation;do not silently declare a bypass,root cause,or repair.

## Expedition and remaining limits

A942/998samples unit2097167at expected/actual(23,25). A1071(seq1029)receives **UnitTeleported** with actual(23,24);A1072ActivityChanged andA1087next gate sample agree. A1088thenrecords TEAM_DISPLACED_STOP;A1319shows HELD. This is direct new evidence of the one-tile position change before the guard,not a display-only issue or a movement caused by that later assertion. [ExpeditionSpyGate.lua](../../../../Mod/ExpeditionSpyGate.lua),473–474,compares exact stored/actual coordinates. Activity/Spy-operation/open-border getters remain UNAVAILABLE in this Gameplay context;the overwritten final native diplomatic log does not independently replay the earlier60Texpiry. PT018's specific native/other-Mod ejection mechanism remains UNKNOWN. No guessed relocation,ignored guard or forced border test is added.

Existing size22raw-unit-icon misses remain in UserInterface.log,and non-SPC localization/configuration SQL warnings remain in Modding.log;these are preserved without editing external Mods or claiming the entire log is clean. No runtime-error/stack-trace/assertion-failed text was found in the64final native snapshots. All20CAPITAL_FAILURErows are COMMERCE_PENDING refresh/qualification guards,not failed credit calls;no DEVELOPMENT_FAILURE/REST_REQUEST_HELD/REST_SYNC_HELD row is captured. Diagnostic absence and registration/readiness limits prevent a blanket no-errors or all-scenarios PASS.

User decision:none required for evidence intake;multi-item queue timing deferred/nonblocking,Police semantics parked. User testing:none newly required;existing long-game opportunities may cover unexercised branches. Primary next:record scoped acceptance/PT017/PT018/PT019and the user's deferrals,publish only reviewed documentation,and stop. Runtime remains B399.426;no implementation,deployment or main promotion in this intake.
