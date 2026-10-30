# B395 native Culture / Research playtest — 2026-10-29

Scope: all new logs since the B394 review,plus the user's current test notes. This is evidence reconciliation and bounded source/database analysis only;no runtime repair,new probe,Design/Architecture change,game launch or deployment. Current source HEAD before this review:9e4a9d7;live B395.422 runtime source0681991 remains342/342 MATCH,SHA256 a16b895a647f768fb54d7f6c93ed093b155f0b303bbfd6540b3edac0ad0f726f. Main stays B307.334.

## Evidence coverage and limits

A=`session-20261030T014505Z-163cda`,B=`session-20261030T025324Z-9cf1b7`;UTC names correspond to local October29. A has1413 captured TRAIN rows,seq1–1413,T16–28,one load. B has950,seq1–950,T28–33,three loads,including returns toT30. These are2363 unique captured rows and480 Culture diagnostic observations. Each captured sequence is contiguous;this does not prove every native event/print was collected. Both collectors end INTERRUPTED. A events449–450 report a partial frame/deadline capture gap near its end;do not infer a crash or complete source coverage.

A records1236/seq1135/T24 explicitly stops the Culture_GP observer at192 rows. Later absence from that role is truncated evidence,not absence of business processing. Other roles continue. No captured GPP_FAILED,DIALOGUE_SAFE_FAILED,TEAM_DISPLACED_STOP or ACTIVITY_POSITION_CHANGED in either session. READINESS_NOT_READY TPR|DP remains a diagnostic-model limitation:ReadinessSummary.lua20–26 checks public .ready,whereas DialogueProjects.lua17–26 keeps private readiness. Actual BEGIN_COMMITTED exists in the same run;UNKNOWN is not proof of failed startup.

All67 current native Logs files (including current database/UI/production/diplomacy/trade/great-person logs) and8 collector files were read and copied with source/copy SHA256 verification. The outer2023 Logs directory is stale and excluded. Frozen ignored archive:`local/legacy-workspace/Specialization/Status/Validation/Evidence/B395_Culture_Research_20261029/`;75raw files,8,441,332bytes;manifest SHA256 `4ca357cce0d2afa92a8038b83892c5704585c0d3c844c017b0370ffba4d50449`. Native sources and prior evidence are retained;this irreproducible raw archive is not a repeated generated Closure.

## Acceptance ledger

USER_GAME_TEST_PASS below means only the user's listed scenario,not the whole subsystem. Log-supported operations/configuration are separately described.

| Ability / scenario | Recorded outcome | Evidence boundary |
|---|---|---|
| Dialogue normal selection/full-turn flow | User reports normal;other states intentionally deferred | A130–138 confirms correct sole queue and BEGIN_COMMITTED seq136,T16;no complete final tourism snapshot in this capture |
| Expedition pre-existing Sleep → People / Works | User reports reward delivery;non-owned Sleep persists | A551–579 explains HOLD rejection then accepted pre-existing Sleep;first-run final reward print not fully captured |
| Saved People task → reload → original due → insight | PASS for this actual recovery chain | B112–121 preserves start27/due29;B155 T29 VIETNAM PEOPLE SUCCESS/NEW;B172–199 owned wake/release |
| Places task,including open borders then war closure | User PASS;successful original and reloaded branches observed | B395/435 and595/637 refer to distinctT31 branches;native diplomacy confirmsT30 deal/war |
| Works task → final Vietnam category | User PASS;T33 SUCCESS/NEW logged | B645–668 start31/due33;B701/742–743 completion/return |
| Same-civilization three-category Culture network | First positive propagation/yield scenario PASS from user | B685/729/737–738 and native trade row5 support source/topology/count;not final specialist Culture measurement |
| GPP automatic population assignment | Mixed;not closed | Some Culture automation works;user also reports lock/next-turn dependence in Culture and Research |
| Research Lv1 support / Lv2 housing / withdrawal | User's listed scenarios PASS | 5specialists'15Food/15Production is base3each,not unexplained district copying |
| Research Application | User's tested D/domain combinations PASS | Includes Industry/Encampment production merge,Faith,Gold and food explanation;not all unseen domains/edges |
| Research Cross-disciplinary | Listed vectors match;earlier mistaken Culture-line observation withdrawn | Total-versus-increment interpretation below;no new complete raw-vector snapshot |
| Research Infrastructure | D6/three specialists33Science and D10/three specialists48 match | User numeric observation plus current HD DB/formula;not a per-building Chair proof |
| Research Tradition inactive accumulation | User PASS for T22–26/T30/T33 checks | 0→4age while governor absent;5% atT30 and10% atT33 agree with10-turn threshold;no raw age/percent rows in these logs |
| Research Chair | Partial;building discrepancy remains OPEN | Library/late Laboratory/fourth-tier figures match,but University4 versus expected5 and earlier uneven rows remain unexplained |

The previous one-off displacement/disabled-unit save was deleted and cannot currently reproduce. The user explicitly parks it. Early Empire/State Workforce is only a user hypothesis,not an established cause or gameplay rule. Do not reopen a border/civic investigation or introduce movement/eligibility exceptions from it. Existing no-deliberate-pillage and no-mandatory-Harbor-retest constraints remain.

## GPP — real progress,remaining ambiguity,and a diagnostic defect

A representative actual path:

| Archive A records line / seq | Turn | Qualified city / kind | Gameplay workers → reported Mod base per class |
|---|---:|---|---|
|58 /57|16|65536 Culture|2→4|
|282 /272|17|65536 Culture|3→6|
|307 /297;328 /318|17|65536 Culture|0→0;3→6|
|602 /571|20|131073 Research|2→4|
|689 /653;696 /660|21|131073 Research|1→2;2→4|
|972 /913;1002 /938;1009 /945|22|131073 Research|3→6;4→8;5→10|
|1110 /1027|22|Research qualification withdrawal|0→0|

B59/seq58/T28 has Culture3→6. B242/228,251/237,260/246,288/273/T29 observes Culture2→4,3→6,2→4,3→6. B317/300/T30 has Research5→10;B500–502/471–473 and928–930/873–875 confirm Culture3→6 / Research5→10 after separateT30 loads. Do not combine those branches into continuous growth.

Across both sessions,all98 GPP_APPLIED rows have expectedNumber==actualNumber;none is GPP_FAILED. This confirms the observed carrier configuration relative to the Getter's count,not final native GPP or agreement with actual automatic occupancy. Some rows deliberately report UNKNOWN city and zero cleanup/ineligibility;they are not specific-city PASS evidence.

The user records18.9/16.9/14.8,then32.2/34.2/31.1,36.4/38.9/35.3,44.9/48.2/43.8 and51.3/55.2/50.1,with population/locking/reload and turn changes between observations. Keep these as observations,not a single controlled before/after experiment. The final delta6.4/7.0/6.3 is compatible with three recognized workers adding base6per class plus the stated percentages,but rounded empire totals cannot identify input semantics or modifier order.

Static current DB and Lv2GPP.lua35–36,49–54,61–76:one Culture specialist adds Mod base+2Writer,+2Artist,+2Musician (sum6 across classes,not6to each). Native Theater specialist base is separately2per class;Campus is native2Scientist plus Mod2. GPPReadout.lua1–17 reads EMPIRE points/turn;the Mod carrier is a city base component. Empire Artist10% and the Culture city's Inspiration6% must not be indiscriminately applied to every source.

The roughly+1 Artist/+1Musician residual is not explained by these logs. Read-only DB contains BUILDING_JNR_ASSEMBLY with Artist1/Musician1/noWriter;it is only an omitted-source candidate. The tested city's ownership/activation is not established by City_BuildQueue/native logs,so it is not accepted as the cause.

**The intended UI comparison did not reach the log.** Only three GPP_EXPLICIT_GP rows exist,A290/seq280/T17,A335/324/T17,A422/407/T18,all Culture3/expected6/carrier6. There are zero GPP_EXPLICIT_UI rows and no CULTURE_GPP_READ_UI context. P0Panel.lua1–9 loads CultureDiagnostics but its include closure does not supply the required ExpeditionTrainingDiagnostics in that UI context;CultureDiagnostics.lua39 builds the optional sample and47–48 returns when the logger is absent. A local in-memory counterexample using the actual observer produces one read,zero records,zero commands without the logger. This is a static wiring defect/local reproduction,not proof the native citizen API failed or the user did not click. The prior release's observer test supplied that logger and missed this composition. Record this as Primary's diagnostic integration gap;do not change GPP gameplay to compensate.

Minimal future repair order:fix the removable P0 logger dependency/absence tests;filter irrelevant AI diagnostic arrivals before they consume the192-row Culture budget (NativeFacts.lua43–47 currently observes before player filtering);then obtain same-token/same-anchor UI actual/locked/UI Getter versus Gameplay Getter/carrier. Only then distinguish native count semantics,pre-commit event timing,missed invalidation and final modifier sources. No new polling/global scan or UI settlement authority is authorized by this review.

## Research — normalized expected values

The user's original unexplained15Food/15Production is reconciled by base support5×3. A passenger terminal treated as tier4 was actually tier3;the user's1/2/3/3 → D9 correction is retained,not a new effect defect. Research Application merges matching yield domains before the per-specialist floor:IndustryD10 and EncampmentD6 give5×floor(5+3)+base15=55Production,matching the note.

For Cross-disciplinary research,the Campus is excluded from the copy set (ResearchCrossModel.lua5),but its native adjacency2 remains in total district output:

- First vector:Mod increment floor((Theater4+Harbor6)/2)=5.
- Later vector:Campus native2+floor((4+6+4+2)/2)=10.
- Final vector:Campus native2+floor((4+6+5+2+2+2)/2)=12.

ResearchCrossModel.lua37 floors the final aggregate. The earlier5read from the Culture line was corrected by the user;do not keep it as a bug. These comparisons support the listed user scenarios,not arbitrary untested layouts.

Read-only configured engine DB:Library fixed Science3;University/Laboratory/fourth ordinary Campus tier have no fixed Building_YieldChanges Science row. Native Campus specialists give2Science and each ordinary building adds1via Building_CitizenYieldChanges. University's UNIVERSITY_ADD_POPULATION_SCIENCE is city population Science,not a fixed University base. Thus:

- D6 with three ordinary buildings and three specialists:3×(2+3+D6)=33Science.
- D10 with four ordinary buildings and three specialists:3×(2+4+D10)=48Science.

This validates the user's Infrastructure arithmetic (ResearchInfrastructure.lua94–98),not Chair's building-row update. ChairModel.lua21–28 uses the same current worker count per qualified building;ResearchChair.sql12 applies building yield directly. With the user's Library base3 plus first-tier envoy1:

| Recognized workers | Library | University | Laboratory | Fourth tier,if built |
|---:|---:|---:|---:|---:|
|2|6|2|2|2|
|3|7|3|3|3|
|5|9|5|5|5|

Final observed9/4/5/5 leaves the University1short of the simple expected value. Earlier three-worker7/2/1 rows are also not explained merely by University base0. Read timing,worker sampling,per-building carrier configuration and native modifier/UI refresh remain alternatives;no corresponding per-building applied/native-yield snapshot exists here. Do not dismiss this as a known harmless UI delay or mark all Chair scenarios PASS. GPP/Infrastructure/Application/Chair share WORKERS notifications (FactConsumerBindings.lua23–31) but each applies separately,so success in one does not prove the others.

Tradition:the user observes initial5%/age0 atT22,age4atT26 while inactive,5% in theT30save and10% atT33;standard-speed10-turn threshold fits. A942/888–1009/945 supports activation and worker changes;A1110/1027 then institutional ACTIVE1supports withdrawal. B842–866 supports later ACTIVE4and final return toT30is a different branch. No native age/percent samples are inferred from those qualification rows.

## Expedition and Culture network — successful specific paths

A551–556/T20 reads HOLD (skip-turn),Sleep native permission denied,requested=false/attempted=false;REJECTED returns ARRIVED/NONE rather than HELD or a reward. A568–579 reads pre-existing SLEEP and accepts start20/due22. UI/ExpeditionSpyActivity.lua326–329,343–359 retains original permission checks;375–378 does not wake Sleep not created by this Mod. The user's task ending still asleep after pre-sleep initiation is consistent with that ownership protection,not automatically a new failure.

B112–121/T28:LOAD_CLOSE seq113 precedes RECOVERED send116,transportTRUE117,GameplayHANDLING119 and accepted result120. Original start27/due29 is preserved. B155/T29 logs PEOPLE SUCCESS,VIETNAM insightNEW;B172–199 records owned WAKE/RELEASED and ARRIVED/NONE. This is real positive evidence for the saved-task recovery path repaired in B395.

B208–231 starts PLACES29/due31;B395/435 completes on oneT31timeline. B554–563 reloadsT30and confirms the same29/31timer;B595/637 completes this reloaded branch. These are alternate saved timelines,not proof of duplicate rewards in one timeline. Native DiplomacyDeals.log1–4 records player4→0 Open Borders atT30;DiplomacyManager.csv22–31 records player0→4 surprise war inT30. The user's border-close scenario completes Places;it does not establish the cause of the deleted old displacement case. B645–668 starts WORKS31/due33;B701/742–743 records SUCCESS,VIETNAM insightNEW and return. Final T30reload also preserves Places timer.

AtT33 the third Vietnam category completes. B728/seq685 already projects capital65536count1before a domestic route;this is a local source contribution. B776/seq729 verifies routeCount1;B784–785/seq737–738 project capital65536and Boston131073 count1. Game_TradeManager.csv5records Washington→Boston,6also Washington→Philadelphia;later routeCount2leaves other ineligible cities at0. Thus the user's5specialists25→30and no gain on other districts is a USER observation PASS supported by source/topology/receiver-count evidence. Logs do not include the final Culture total or those specialist counts. The note's measured city is slightly ambiguous;do not claim the capital changed0→1only because of the route. CultureNetwork.lua430–433 logs workers only from an explicit Describe,which was not captured for this transition.

## Peripheral log observations and next scope

Current UserInterface.log has no discovered SPC Lua runtime exception/traceback. It still reports missing22px SPC icons:Expedition165entries,each of the five Crew variants and Restructuring3entries. This is an art/presentation backlog,not demonstrated cause of the GPP/Chair mismatch. Database.log contains other configuration/localization/Types/icon constraint errors:some explicitly belong to external Clickouts/RealGreatPeople;unattributed rows are not assigned to SPC merely by timestamp. Gameplay foreign-key validation passes at the observed gameplay boundaries. No external Mod was changed or audited broadly.

User decision:park the deleted/non-reproducible movement incident;defer additional Dialogue states;no new gameplay decision. User testing:none newly demanded by this review;accepted cases are not repeated. A future GPP comparison should follow repair of its missing diagnostic half. Primary next:review the minimum isolated diagnostic wiring/budget correction and Chair's applied-versus-native building figures before any behavior repair;current request authorizes analysis/recording only. B395runtime/deployment/main remain unchanged;original S9/S10/final U5 still open.
