# B396 / B397 third playtest — Industry evidence review

2026-10-31. Primary; review baseline `07d2741`, live B397.424 from `aa51feb`; main remains B307.334. Design D0058 / Architecture A0183. This batch reads submitted evidence and records acceptance; it changes no runtime, tests, gameplay, architecture, deployment or external Mod. Industry business sources are unchanged between the tested B396 and B397 packages; the intervening runtime delta is the two network transport files and build identity.

## Outcome and evidence scope

The user's tested ordinary Industry abilities pass within the cases below. Engineering Study has a reproducible queue re-entry gap, also observed by the user in Dialogue. The original first-turn Standardization anomaly has a plausible **pre-B397 missing-proof** explanation; later B397 same-turn application is positively evidenced. Visible building effects coincide with genuine batches of native carrier calls, but their exact frame cost is not measured. This is not final U5 or commercial transaction acceptance.

`USER_GAME_TEST_PASS` here refers to the user's explicit observation in the stated scenario. `STATIC_CONFIRMED` describes source/rule verification; log transitions corroborate state, not unlogged final yields. No new `LOCAL_SIMULATION_PASS` is claimed. Historical results remain frozen.

## Evidence inventory

Local raw evidence: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B397_Industry_Playtest_20261031/`. All 56 source files were read and copied with matching SHA256: seven collector folders × four files, plus 28 latest native log files; 4,070,137 bytes, excluding manifest. Manifest SHA256: `f6ed34b7773bb92363229bc9a8752f409244aadc69f24d25cb2c6755530ee0db`. This ignored local archive is not a permanent external backup; raw private logs are not published. Originals are retained.

The following aliases refer to each archived `collector/<session>/records.log`; line numbers below address those originals. `memory:Lx` means that session's `memory.jsonl`, not records.log.

| Alias / session suffix | Build / turns | Limits |
|---|---|---|
| G1 `20261030T131055Z-c29f68` | B396, T33–36 | Preceding GPP context; 559 TRAIN rows; passive partial-frame gap |
| G2 `20261030T135125Z-79fc1c` | B396, T36–37 | Preceding GPP context; 216 TRAIN rows; passive partial-frame gap |
| A `20261031T033731Z-ee5153` | B396, T36–37 | 507 TRAIN rows |
| B `20261031T035013Z-ed22b7` | Same B396 load, T36–41 | 720 rows, seq252–971; seq252–507 overlap A; initial ring gap1–251 is covered by A |
| C `20261031T173347Z-52bc40` | B397, T41–47 | 925 rows; snapshot deadline gap at end |
| D `20261031T180540Z-e3427d` | B397, T47–53, then reload T52–58 | 1,936 rows across two loads; memory counters reset at second load; snapshot deadline gap at end |
| E `20261031T190813Z-26b21d` | B397, T58 cold load | 152 rows; short segment, no full-turn workload boundary |

All sessions reach `TRACE_SINK_BUDGET_STOP`: the native print sink stops; collector ring capture continues. This is not proof that all later diagnostics disappear, nor complete native-event coverage. Context-specific finite diagnostic budgets and capture gaps still limit negative claims. Session suffixes are UTC; a reused older diagnostic request label does not establish runtime downgrade. Count overlapping records once and separate reload branches.

Latest native files also contain SPC missing-size22 icon warnings and unrelated configuration/localization errors. They do not establish a project-timer or hitch cause. No complete native Lua error channel was present in that snapshot; absence of a captured exception is not proof of no exception. No unrelated asset/Mod investigation is opened.

## User acceptance ledger

| Ability / scenario | Recorded outcome | Precise boundary |
|---|---|---|
| Lv1 support | USER_GAME_TEST_PASS: follows Industrial Zone base adjacency | No inferred new adjacency formula |
| Lv2 housing | USER_GAME_TEST_PASS | Industry/Commerce GPP deliberately not repeated; no independent GPP PASS manufactured |
| Lv3 Standardization | PASS for learned city-centre group/Industrial tier1, new Commerce tier3 template propagation, and non-template exclusion | Original first Monument15 is explained below, not silently discarded |
| Multi-source Standardization | Partial native coverage: second source's existing Theatre district is imported, template union and A3 contribution operate | Not a fully isolated two-A4/different-L per-template maximum test; no mandatory extra campaign |
| Crew training | PASS: A3 immediate I–III access, paused I continuation after III completion, capacity accounting | Same-turn multiple source-city completions not demonstrated by this single-source run |
| Crew spending | PASS: III base750, one consumption and slot release; applicable 25% wonder policy observed | Other tiers need no repetitive native test; exact all-modifier order not inferred |
| Engineering Practice | PASS: A3 costs390/630/1125; A4 first-wonder costs364/588/1050/1400/1904; second wonder unchanged | N is local completed wonder count; thresholds1/3/6 |
| Engineering Study | PASS for ordinary one-turn completion, qualification loss without reward, saved active timer recovery, one reward despite manipulations, E limit/new-era reopening | Queue reordering/natural advancement remains a confirmed failure below |
| Tradition-enhanced network effects | PASS for 2%/4%/6% purchase discounts, exclusion, forwarding, removal after governor departure; isolated normal single-source production increments agree | Construction-speed withdrawal was inferred from shared exit plus observed price withdrawal, not separately measured |
| Wonder Engineering | User accepts era gaps2 and3+ as PASS | Native production varies; approximate comparison is not an exact modifier-stacking proof |
| Dialogue | User observes new game-era unlock and same queue symptoms | Start immediately before era transition / quota attribution deferred by user |
| Research Academic Tradition | User PASS: age36,20%, retained after reload | T22 age0 → T58 age36 agrees with chronology; these logs do not independently record age/percentage |

## Verified formulas and histories

`Specialization/Design/Industry.md:82–98,133–163` and `Mod/CrewModel.lua:4–6,33–44` distinguish **N** (local completed wonders), **E** (civilization's different completed-wonder eras) and **L** (this city's successful studies).

A3 always uses150% and unlocks tiersI–III. Actual base capacities are260/420/750/1000/1360; the stable identifier containing250 is not its current capacity. A4 N0 remains150%; N1–2=140%, N3–5=130%, N6+=120%. Thus both quoted cost sets are correct and the second wonder cannot lower cost again. These costs are not determined by civilization E or local study L; A4 with N0 also retains150%.

Standardization takes each template's maximum **only among eligible sources actually holding that template**: A3=10% construction/0% purchase discount even with retained L; A4=`10+2L` construction and `2L` purchase discount. `Mod/StandardizationEffects.lua:119–150,172–189`. A high-L first source cannot raise a second source's exclusive template. The diagnostic at209–220 reports template counts and maximum amount, not every template's own amount. Do not explain20→21 as a proven native rounding rule or infer a global coefficient from that row.

C:600/621 records Oracle/Ancient and Sydney Opera/Atomic;602–629 shows E2→3→4. D:750 (seq713,T52) has L4/E4, `EST_KNOWLEDGE_REACHED`;871/878 (seq825/832) records medieval Potala Palace then L4/E5 AVAILABLE. D:1078 (seq1014,T53) reaches L5/E5; E:89 (seq88,T58) cold-loads L5/E5. The latest actual history is therefore **five**, not merely the four studies first described. D's return to saved T52 replays that branch's L4→5; it is not duplicate reward in one timeline.

`Mod/IndustryWonderEffects.lua:51–74` implements era differences1/2/3+→10/20/30%. Its `eraCount=9` diagnostic field is a chronology index, not E or nine supported eras. C:352 confirms A4 applied qualification, not precise final production. `Mod/ResearchTradition.lua:42–48` and `Design/Research.md:87–99` give20% at standard-speed age30–39. Prior [Research review](Specialization_B395_Culture_Research_Playtest_20261029.md) records the user's T22 age0; no new age telemetry is invented.

## Engineering Study queue gap

STATIC_CONFIRMED, consistent with USER_GAME_TEST_FAIL for reorder/natural-advance cases:

1. `Mod/UI/EngineeringStudyUI.lua:30–35` creates a pending BEGIN only from explicit ordinary selection; queued selection returns without creating it.
2. `Mod/UI/TimedProjectSelectionClient.lua:104–111` lets a same-city queue event wake an **existing** pending request, but does not create a new one.
3. `EngineeringStudyUI.lua:44–47` requires current project and total queue size1 before sending BEGIN. `Mod/TimedProjects.lua:5–14` rejects MULTIPLE with `EST_SINGLE_PROJECT_REQUIRED`.
4. `Mod/EngineeringStudyProjects.lua:175–190` observes interruption when another target becomes current. Returning Study to the head or advancing naturally from a completed Worker does not establish the replacement explicit BEGIN. UI:16 consequently shows “确认中” for native current Study without an ACTIVE timer.

Appending then removing a tail item can recover an existing timer; interrupting/reordering can invalidate that round and leave no replacement. They are different paths. D:457–478 (seq441–458,T50) records related-fact/unique-project protection with L2 unchanged. Clearing and reselecting gives D:484 ACTIVE →524 CALLING →530 L3 (T51), one reward. Logs do not contain every mouse movement, so individual drags are not assigned invented timestamps.

Further positive chains: C:674→716→722 gives L0→1;761→767 loses qualification with L1 unchanged;971 saves start47/due48. D:87→188→195 restores that timer and reaches L2. The same technical queue symptom is user-observed for Dialogue, but its rewards/qualification remain independent.

**Disposition:** PT016 records the gap; no implementation here. The user's whole-queue-clear/reselect workaround is documented as a present backup, not accepted as the permanent design or a substitute PASS. A future minimal repair should use verified same-city queue facts and reliable selection/interruption evidence to re-establish a legal complete-turn round; retain UNKNOWN, qualification and unique completion guards. No timer, polling, full-city scan or unconditional current-project auto-start is authorized. Whether an unchanged multi-item queue should actively count is a separate rule choice if a repair requires changing the current single-project contract.

## Crew corroboration

B:277/283/289/290 (seq524/530/536/537,T37) reserves III at1125, pauses I with progress55, binds III, and counts bound1+paused1. B:299/310 resumes I at its locked390/progress55 and later binds it. This supports continuation/capacity rather than losing paid progress.

C:165/168 (seq163/166,T41) spends III with baseCapacity/baseInput750 and changes source count2→1. C:224 (seq219) later reads native progress750 before the next use. Immediate `CREW_PRECISION actualDelta=0` is a same-stack native readback limitation, not proof of failed spending (`Mod/CrewPrecision.lua:38`). The user's actual progress and later pre-read corroborate750.

## Route proof and the first Standardization turn

A:117 (seq116,T36) LOAD_CLOSE is followed by END/next STARTED still UNAVAILABLE/IN_FLIGHT (476/481). First NETWORK_VERIFIED arrives only A:511 (seq492,T37); receiver262147 then first gets9 building/6 district templates from2 sources at10%, A:515. B memory2→3 retains net_send1/net_receive0 through the T36 END→T37 BEGIN boundary.

This **pre-B397** unreceived load proof fits the original Monument15 observation. No per-building progress row binds that particular production amount to this interval, so it is a supported explanation, not exclusive causal proof or a new B397 failure.

On B397 D:893→909 (seq843→859,T52), routes1→2 are confirmed;913/914 (seq863/864) apply18% to Commerce262147 and forwarding327684 in that same turn. D:953→969 (seq897→913) confirms routes2→3;975 applies18% to new receiver393221. This supports the later user test production8→progress9 on its first connected turn.

Four B397 load boundaries recover within the loaded turn: C121→128(T41), D121→128(T47), D1211→1218(reloadT52), E122→129(T58). D334/364/365 shows routeCount1/inputRevision2 with signal pairs49/49→52/52→55/55. No new captured FAILED_TURN or boundary IN_FLIGHT latch appears. These are scoped native recovery/catch-up positives, **not deliberate first-packet-loss coverage** or byte-identical-payload proof. PT015 remains open for actual Commerce READY, nonzero revenue and Capital/Development transactions.

## Update effects, hitches and T39 unit deletions

These are deltas of cumulative **all-Mod** work counters within one load. Creation/removal counts mean wrapped native calls, not unique objects or independently confirmed success; neither counts nor checks directly measure CPU share.

| Interval | Create/remove calls | Building checks | Net send/receive | Memory evidence |
|---|---:|---:|---:|---|
| B396 T36 END→37 BEGIN |22/0|17,698|0/0|B2→3|
| T37 BEGIN→END |31/3|91,240|1/1|B3→16|
| T37 END→38 BEGIN |5/0|17,750|1/0|B16→20|
| T38 END→39 BEGIN |0/0|17,526|0/0|B25→28|
| T39 BEGIN→END |0/0|52,259|0/0|B28→33|
| B397 T44 BEGIN→END |5/5|55,352|1/1|C37→46|
| T44 END→45 BEGIN |0/0|22,723|1/1|C46→49|
| T45 BEGIN→END |52/123|58,382|0/0|C49→61|
| T46 END→47 BEGIN |58/0|22,844|1/1|C70→72|
| T51 BEGIN→END, first load |78/52|73,940|2/2|D41→54|
| T52 BEGIN→END, route reconnection |111/33|131,342|3/3|D57→84|

C721/772/945 shows the commercial receiver10%→12%→no templates on source qualification loss→12% restoration with18 building/8 district templates. Genuine strength/template changes explain why many carrier bits can change; this is not proof that every proof confirmation unconditionally rebuilds every carrier. Other confirmed intervals have zero carrier writes. The table supports real bursts near the user's light effects; it cannot attribute the entire subsecond hitch or an exact visual frame to Standardization.

GC is a separate candidate: B memory29 records complete collection atT39 (about1004→408MiB, coarse CPU1/wall2seconds), not T37/38 (baseline/skip, collections0). C memory38 records collection atT44 (about941→348MiB, CPU1/wall1);T45 only INTERVAL. D's T52 GC was18:28, route recreation18:36: these are different moments. No GC strategy is changed. Module-attributed scans, route_scan, per-native-call timing and unit-filter callback counts are absent; current evidence cannot safely allocate the full check cost or prescribe an optimization.

B records587/604 (seq802/816,T39) retain VERIFIED signal37/37 through STARTED→END; that turn has net0/0 and carrier0/0. Only after END does606 (seq817) mark pending from `TRADEROUTEREMOVEDFROMMAP`. Thus Worker/Warrior deletion has **no observed** route invalidation/resend. Their individual event/filter outcomes were not logged; source filtering exists at `Mod/NetworkBridge.lua:873–889,915` and `Mod/UI/BackgroundRoutes.lua:226–227`, but its actual invocation is not directly proven here.

## Remaining work and review boundary

The queue permutations already distinguish the technical gap; no more equivalent manipulations are requested before a repair. Future useful observations, when naturally available: Dialogue start across era transition (already deferred by user), two eligible A4 sources with different L and exclusive/overlapping templates, and two source cities completing crews in the same turn. These are untested boundaries, not reasons to reject the demonstrated ordinary abilities or demand a separate test campaign. No deliberate pillage, ownership transfer, all Crew variants, renewed HD GPP investigation or native UI/rounding investigation is requested.

User decision: none needed for this evidence review; queue repair implementation and any changed queue contract remain separate. User testing: no repeat of passed cases; continue planned Commerce testing when desired, retaining collector evidence. Primary next: review the scoped queue re-entry repair before implementation; retain PT015 and the performance evidence under existing entries. No main promotion, game launch, runtime change or deployment in this batch.
