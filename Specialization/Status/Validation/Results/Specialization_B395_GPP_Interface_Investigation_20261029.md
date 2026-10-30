# B395 follow-up — specialist interfaces and removable diagnostics

2026-10-29. User authorized investigation only. Baseline9c54965;runtime B395.422/0681991,main B307.334 unchanged. No code/probe implementation,game launch,configuration change or deployment. Source/database reads and in-memory native-double counterexamples are not user-game proof.

## Confirmed interface distinction

| Use | Current interface | What is established |
|---|---|---|
| GPP gameplay worker count | `plot:GetWorkerCount()` in Lv2GPP.lua49 | This is the real input to each class's base2N calculation;it does not explicitly read LOCKED_CITIZENS |
| Research Chair gameplay worker count | `Map.GetPlotByIndex(plot):GetWorkerCount()` in ResearchChair.lua43–45 | Same Getter family;shared sampling does not change each ability's policy |
| Original population UI | `CityManager.GetCommandTargets(city,CityCommandTypes.MANAGE,params)` | PlotInfo.lua366,372–375 reads same-key PLOTS,CITIZENS,MAX_CITIZENS,LOCKED_CITIZENS separately |
| Current optional P0 comparison | CultureDiagnostics.lua86–105 | Reads CITIZENS(actual),LOCKED_CITIZENS(locked),capacity,and a separate UI GetWorkerCount;it is not a gameplay input |

The code does not mistakenly reference LOCKED_CITIZENS for GPP settlement. Conversely,the UI's explicit actual/locked result is not the source currently used by Gameplay. Static source cannot establish which count Gameplay GetWorkerCount returned for this user's automatic-assignment moments or when the engine commits it. A same-token/same-anchor native comparison is still missing. Do not rename Getter semantics from its name or the observed lock dependency.

## Three proved diagnostic gaps

1. P0Panel's include closure does not supply ExpeditionTrainingDiagnostics in its own UI context. CultureDiagnostics39 executes its builder before47–48 checks the missing logger,so reads can occur without output. Actual observer/B205 serialization in memory:missing logger gives one CommandTargets read,one Worker read,zero commands/records;loading real B205 gives the same reads/zero commands and CONTEXT_START plus GPP_EXPLICIT_UI;ENABLED=false gives zero reads/context/records. The existing collector correctly transports token/anchor/actual2/locked1/capacity3/UIGetter1. This proves local wiring/protocol,not native numerical values.
2. CultureDiagnostics65 and80 restrict the comparison to CULTURE. Even after fixing logging,RESEARCH produces no UI comparison. The minimum next diagnostic scope should explicitly include these two tested professions and match the selected valid kind's unique anchor;do not expand to future professions.
3. NativeFacts46 observes WORKER_CAUSE before existing player eligibility filtering. SessionA contains96cause rows:73test-player and23AI;sessionB has58:43test-player and15AI. A loses at least23/192role slots(12%) to unrelated AI. P.IsTestPlayer performs native identity/human/MP reads,so adding a second check solely for diagnostics is unnecessary. An in-memory candidate moved the optional observation into mark's existing enabled-player emit branch:identity checks4,invalidations2,business notifications2 remain identical;irrelevant output drops. No increase of the192role or256shared-ring limit is justified.

Recommended optional dependency ownership:CultureDiagnostics lazily/protectively loads a missing transport only after ENABLED/role/budget checks,and confirms transport before executing native UI sampling. Attempt once per context,do not loop after missing/include/construction failure. Preserve an existing logger instead of re-including its globally assigning file. Keep all module loading/trace roles/bounds inside the removable observer;business startup/readiness,carrier updates and saves never depend on it. Existing B205 has other consumers and is not deleted with this observer.

Observer cost includes a protected turn-clock read and existing LuaEvents notification per emitted record;no new event listener/timer or native write. Off/missing/throwing observer must leave business outputs unchanged.

## Worker propagation — excluded claim and conditional gaps

No proved long-lived stale-worker cache was found. Lv2GPP85–102 creates a reader per audit;EffectiveFacts131–166 validates worker reuse against current phase,owner/city epochs,anchor and write generation. NativeFacts20–23 invalidates before emitting WORKERS;Probe559–568 wraps carrier mutations in BeginWrite/EndWrite. Actual composed native doubles handle same-turn3→1→2 and carriers6→2→4. This excludes that exercised local sequence only,not all engine timing failures.

Two conditional paths require evidence before changing behavior:

- NativeFacts49–57 and UI/GPPRefresh64–82 subscribe to Worker/Focus plus existing turn recovery,but not population. If a real assignment emits Population without Worker,normal update waits for the next turn. In-memory population-only input reproduces that condition. The captured A234/seq231 and239/seq236are not such proof:they are T17 Expedition training observations with population4and delta0. A280–289/seq270–278subsequently has the same city's Worker→workers3→carrier6and UI dirty notifications.
- GPPRefresh45–55 consumes dirty before RequestPlayerOperation and checks only pcall success. A deliberately false/un-delivered transport returns with no resend across1000idle events;the next real Worker event wakes it. This is an explicit local transport assumption,not evidence the native engine dropped a request. Do not introduce blind retries or an arbitrary-event recovery loop. Optional existing-send return/Gameplay-ingress observations can distinguish it without changing delivery.

These findings do not justify replacing Gameplay's count with UI data,adding recurring scans or weakening UNKNOWN. The diagnostic comparison should precede a business fix.

## Research Chair — latest user steering

The user confirmed the9/4/5/5figures came from **the city-details building list**,not P0's configured report,then asked to treat this as a likely known panel-refresh issue without reason to suspect the ability module. Record it as DISPLAY_SUSPECTED / USER_DEFERRED:stop expanding Chair investigation,no business repair or forced retest. Neither a proven native defect nor a new blanket PASS is asserted. This decision supersedes the prior next-step priority without rewriting the frozen playtest review.

Already-read evidence:HD CitySupport.lua703 calls `pCity:GetBuildingYield(buildingType,yieldType)`;Suk_CityPanelOverview_Instances.lua128–135 formats that into the row. University's population×0.5Science modifier is a city effect,not a fixed University building-base row. ChairModel21–28 gives every qualified building the same input count;SQL12–20 independently maps each target and binary amount. No University-specific minus-one was found. Before the user's deferral,a real Chair/Model/CarrierSet/FactChanges/NativeFacts in-memory sequence2→3→5→4→5→1→5kept all four configured amounts equal;native-double correctness is not proof of the real UI refresh cause. If it recurs naturally,the existing P0 per-building configured report and the native row can be compared at one point;no new Chair probe is presently proposed.

## Proposed smallest implementation batch — not yet implemented

- Keep the gameplay Getter,formula,qualification,carrier/save structure,event recovery and final native modifier rules unchanged.
- Repair optional logger loading before sampling;support Culture and Research explicit GPP comparisons with the same validated anchor;reuse existing player qualification for cause-log filtering.
- Optionally add fixed bounded observations at the already-existing dirty send/return/Gameplay ingress,without changing requests/retries. Preserve automatic scans/event frequency and existing bounds.
- Prove actual cold P0 include composition without pre-injected logger;ON/OFF/deleted/include/constructor/sink failure;zero disabled or unavailable native samples;both profession arrays/same token/anchor;recent-token and192cap/marker;unchanged player checks/invalidations/business notifications. Existing real B205 serialization/collector checks cover transport.
- Any later population hook or count-source change is a separate evidence-based proposal,not bundled into a logging fix. No deliberate pillage,old displacement or Chair expansion.

User decision:Chair display issue and deleted displacement remain parked;no new gameplay decision requested. User testing:none now;after a separately authorized diagnostic repair,one controlled automatic/locked comparison can supply the missing engine fact. Primary next:hand back exact interface conclusion and this minimum diagnostic plan;stop at investigation boundary. Runtime and main remain unchanged.
