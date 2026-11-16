# Direct Event Listener Audit

Investigation / Non-authoritative / No design decision implied

Status: Stable

Maintainer: Primary

Recorded: 2026-10-30

Source baseline: develop `abcc2b0a221d151e45c405548ab725a6a88b4af1` (clean tracked tree during investigation).

Runtime metadata: B396.423; Design D0058 / Architecture A0183 / Status S0856. This source baseline is not the deployment receipt: the recorded B396 runtime was deployed from `4ec32e136ec5aa04f6135f819d6a1c3de5a8477d`.

## 1. Purpose, scope and conclusion

This records the user-requested, read-only audit of direct native event subscriptions in the four current professions, their effects, actions and projects, and the UI sampling/operation bridges that support those paths. It supplements the [logical overview](Logical_Architecture_Overview.md), [As-Is reconstruction](As_Is.md), [event atlas](Event_Chains.md) and [scan inventory](Scan_Inventory.md). Those earlier reports retain their own B393 baseline; this audit rechecked the named source paths at the newer commit above.

The user accepts event-driven invalidation, shared facts read on demand, and independent profession processing. This report does not propose replacing that architecture with centralized data push. Approved Architecture Markdown remains authoritative; neither this report nor its classifications authorizes implementation.

Main findings:

- Many direct listeners carry evidence that generic fact invalidation cannot replace: completion/birth receipts, production interruption order, historical learning, unit activity confirmation and exact carrier recovery.
- Several turn, governor and ownership paths overlap shared notifications. Dirty queues and idempotent writes protect some work, but do not prove that consumers execute only once or avoid repeated reads.
- The clearest inactive-callback residue is the retired Dialogue governor group and the retired adjacency branch in DialogueRefresh. Commerce also explicitly retains three broad construction sources pending scoped review.
- Standardization still performs owner-city discovery at turn activation and can retry retained template work on successive publish events within its existing lifetime. The turn-lifetime bound is not a per-publish execution-count bound. Its necessity is not established by this static audit.
- No current approved Architecture requirement was found that mandates moving every direct listener into FactChanges. Assess a listener's responsibility, scope and recovery coverage before treating it as a migration defect.

Evidence is **STATIC_CONFIRMED** for the cited registrations, guards and control flow. Classification is the audit's interpretation of that evidence. Event availability, actual native delivery/order, duplicate invocation frequency and performance attribution remain **UNKNOWN**. No tests, profiler, engine probe, game launch, deployment, gameplay change or formal Architecture change was performed.

A registration is counted when the current successful production startup/context path reaches it, including registrations hidden behind helpers. Optional event fields can be absent natively; source reachability is not native delivery proof. ImportFiles alone is not activation. Pure development experiments and the complete subscription inventory of common identity/network producers are outside this profession-consumer inventory; relevant common producers were traced to establish overlap.

## 2. Reading the inventory

Native event aliases below are only notation for this report, not new runtime or governance groups:

- `E` = `Events`; an unqualified event uses E. `G` = `GameEvents`.
- `L` = `LoadScreenClose`; `P` = `GameCoreEventPublishComplete`; `PB` = `GameCoreEventPlaybackComplete`.
- `T+` = `PlayerTurnActivated`; `T-` = `PlayerTurnDeactivated`; `X` = `CityTransfered` (native spelling).
- `Gov` = `GovernorAssigned`, `GovernorEstablished`, `GovernorChanged`, `GovernorPromoted`.
- `Queue` = `CityProductionChanged`, `CityProductionQueueChanged`; `Queue+` adds `CityProductionUpdated`.
- `Activity` = `UnitActivityChanged`, `UnitOperationAdded`, `UnitOperationDeactivated`, `UnitOperationsCleared`, `UnitCommandStarted`, `UnitMovementPointsChanged`.
- `Money` = `TreasuryChanged`, `PlayerTreasuryChanged`, `PlayerGoldChanged` (optional aliases checked for availability).
- `Role` shared notifications = IDENTITY / POTENTIAL / ACTIVE. D means DistrictCompleteness; GW means GreatWorkFacts; EF means EffectiveFacts; FC means FactChanges and, where applicable, FactConsumerBindings. A consumer can also receive D/network/GW provider notifications directly rather than through FC alone.
- `Init`, `Drain` and `H` refer to the three helper registrations in the first three rows. They are additive: a module's explicit P or L callback does not replace its helper callbacks.

Classifications:

- **A — Reasonable direct listener:** distinct required evidence, operation, state ordering, producer, lifecycle or pending-drain responsibility.
- **B — Potential overlap with protection/recovery value:** a shared path also reaches related work; removal is not justified without proving necessary recovery and work scope.
- **C — Suspected historical residue / incomplete migration review:** an empty retired callback or explicitly retained broad legacy edge. This is not proof that deleting the surrounding module is safe.
- **D — Insufficient evidence:** source explains what runs, but not why its remaining frequency or recovery trigger is necessary.

Rows group listeners with related responsibilities; a row is not a subscription count. Scan notes describe downstream work too, rather than only the small event callback. Precise owned-carrier checks are distinguished from ordinary-building/catalog enumeration.

### Complete UI adjacency sampler event set

`AdjSampler`, cited in the table, expands to these registrations in [SampleLifecycle:206](../../../../../Mod/SampleLifecycle.lua#L206):

1. `ImprovementAddedToMap`, `ImprovementRemovedFromMap`, `ImprovementChanged`, `FeatureAddedToMap`, `FeatureRemovedFromMap`, `ResourceAddedToMap`, `ResourceRemovedFromMap` -> anonymous callback -> `s.Plot(x,y)`.
2. `DistrictAddedToMap`, `DistrictRemovedFromMap`, `DistrictBuildProgressChanged`, `DistrictPillaged` -> `s.District(pid,did,cid,x,y)`. The sampler uses owner/geometry; the declared did/cid do not themselves guarantee single-city sampling.
3. `CityProductionCompleted`, `CityAddedToMap`, `CityRemovedFromMap`, Gov, `GovernmentChanged`, `GovernmentPolicyChanged`, `ResearchCompleted`, `CivicCompleted` -> `s.Owner(pid)`; only the first argument is consumed.
4. `CityTransfered`, `CityTileOwnershipChanged` -> `s.All`; arguments are not used to guess geometry.
5. `BuildingAddedToMap`, `BuildingRemovedFromMap` -> `(x,y,id,owner)` callback; filter known SPC buildings, then `s.Owner(owner)`; x/y are not used for narrowing.
6. IndustryRefresh only: `CityWorkerChanged`, `CityFocusChanged`, `CityPopulationChanged` -> `s.Owner(pid)`. ResearchCrossRefresh passes `workers=false` and does not register these three.

## 3. Direct listener inventory

| Module / registration evidence | Native events -> callback / work | Parameters, facts, enumeration and overlap | Classification |
|---|---|---|---|
| [RuntimeWork StartReady:493](../../../../../Mod/RuntimeWork.lua#L493) — **Init** | L / P / T+ -> `attempt` -> module startup callback | Event arguments ignored; reads Store readiness, latches once. Used by the research rows below, DialogueProjects and the shared TimedProjectReaders readiness service. Does not repeatedly initialize after success. | **A**, readiness recovery. |
| [RuntimeWork NewAudit:89](../../../../../Mod/RuntimeWork.lua#L89) — **Drain** | P -> `flush`; L -> clear pending | Drains retained player/city/transfer scopes. Does not deduplicate two Audits that already executed separately. Used by research, Aesthetic, Meaning, Inspiration, InsightsTourism and DialogueEffects below. | **A**, pending lifecycle. |
| [RuntimeWork NativeHealth:530](../../../../../Mod/RuntimeWork.lua#L530) — **H** | `BuildingRemovedFromMap` -> guarded `removed`; `G.BuildingPillageStateChanged` -> guarded scoped mark | Removal uses x/y/index/owner and resolves city; pillage uses pid/cid/index/state. Exact module-owned IDs, self-write witnesses and conservative unknown-location fallback. D intentionally filters internal carriers. | **A**, exact carrier health; not duplicate ordinary D. |
| [ResearchSupport:48](../../../../../Mod/ResearchSupport.lua#L48) | Init + Drain + H; T+ / X -> `Audit` via TargetHook | Uses pid or verified lifecycle scopes; EF/anchor reads and precise carriers. Turn can visit owner cities; Role/D also arrive through bindings. | Helper duties **A**; turn/lifecycle **B**. |
| [Lv2Housing:90](../../../../../Mod/Lv2Housing.lua#L90), [Lv2GPP:134](../../../../../Mod/Lv2GPP.lua#L134), [ResearchInfrastructure:144](../../../../../Mod/ResearchInfrastructure.lua#L144) | Init + Drain + H; T+ / X / `CityRemovedFromMap` -> `Audit` | pid/cid or transfer participants; shared eligibility/D and ability-specific worker facts. City scope can be narrow; turns can visit owner cities. Role/D/WORKERS overlap FC. Former-holder/UNKNOWN withdrawal recovery remains significant. | Helper duties **A**; extra audit routes **B**. |
| [ResearchCross:151](../../../../../Mod/ResearchCross.lua#L151), [ResearchApply:127](../../../../../Mod/ResearchApply.lua#L127), [ResearchChair:111](../../../../../Mod/ResearchChair.lua#L111) | Init + Drain + H; T+ -> `Audit` | pid; shared gates, D/workers as required. Cross also consumes confirmed UI BASE samples and inspects relevant districts. Owner-turn work overlaps FC. | Helper duties **A**; turn **B**. |
| [ResearchTraditionEffects:206](../../../../../Mod/ResearchTraditionEffects.lua#L206) | Init + Drain + H; T+ -> `Mark`; P -> `Flush` | pid; visits registered Tradition records, history/qualification and exact effects, not an ordinary-building census. HISTORY/TRADITION also notify through FC. | Initialization/health/drain **A**; turn **B**. |
| [CultureAesthetic:205](../../../../../Mod/CultureAesthetic.lua#L205), [CultureMeaning:187](../../../../../Mod/CultureMeaning.lua#L187), [CultureInspiration:171](../../../../../Mod/CultureInspiration.lua#L171) | Drain + H; L -> reset/Audit; T+ -> Audit; X / `CityRemovedFromMap` -> mark/audit | pid/cid or lifecycle owner scope; EF/D/GW and ability-specific building/carrier checks. Owner audits enumerate cities. Role/D bindings and GW consumers reach the same effects. Turn guards are not proof of one audit per publish. | Load/health/drain **A**; turn/lifecycle **B**. |
| [CultureInsightsTourism:146](../../../../../Mod/CultureInsightsTourism.lua#L146) | Drain + H; L / T+ -> Audit | pid; insight history, EF and exact carriers; owner-city visits, no ordinary-building list census. FC HISTORY/INSIGHTS overlaps. | Load/health **A**; turn **B**. |
| [DialogueEffects:199](../../../../../Mod/DialogueEffects.lua#L199) | Drain; L -> Audit; X -> mark; `BuildingRemovedFromMap` / `G.BuildingPillageStateChanged` -> local health handlers | X consumes new owner/cid/old owner; health consumes exact index/location and suppresses own removal. Reads Dialogue history/EF/GW. Role/history/GW also notify. | Health/load **A**; X **B**. |
| [CultureNetwork:477](../../../../../Mod/CultureNetwork.lua#L477) | H; L -> Audit; P -> flush; T+ -> Mark | pid; Bridge/source qualification/insight history. Warm source/recipient indexes; initialization still scans cities and old carriers. Role/D/NETWORK/HISTORY notification overlap. | Load/health/drain **A**; turn **B**. |
| [IndustrySupport:166](../../../../../Mod/IndustrySupport.lua#L166) | H; L -> reset/Audit; P -> `drainCauses/FlushPending`; T+ / X -> Audit | pid/lifecycle scope; EF and verified UI adjacency samples. D and sample notifications also arrive. Publish does not reread failed cities without an armed cause. Initial/owner paths can visit cities. | Health/load/drain **A**; turn/lifecycle **B**. |
| [IndustryHistory:263](../../../../../Mod/IndustryHistory.lua#L263) | `WonderCompleted` -> completed; L / P -> ensure | Completion retains x/y/building/owner/cid, verifies attribution/era and deduplicates permanent history. Ensure checks Property/Store readiness, no city/building enumeration. | **A**, unique historical completion evidence. |
| [IndustryWonderEffects:115](../../../../../Mod/IndustryWonderEffects.lua#L115) | H; `CityRemovedFromMap` -> mark; L -> all/Flush; `PlayerEraChanged` -> mark/Flush; T+ -> era comparison/error recovery; P -> Flush | Mostly pid; reads era, EF and precise carriers. Owner scope enumerates cities. Role consumer also marks work; era is an additional input. T+ retries existing errors even without a changed era. | Era/health/drain **A**; lifecycle/turn recovery **B**. |
| [Standardization:284](../../../../../Mod/Standardization.lua#L284) | `G.OnDistrictConstructed` -> verify/queueReconcile; `G.BuildingConstructed/G.OnBuildingConstructed` -> Queue/Flush; `BuildingAddedToMap` -> Queue; `CityProjectCompleted` -> industrial-Claim reconciliation | District uses pid/type/x/y to resolve city; building callbacks use pid/cid/bid. BuildingAdded receives coordinates but queues the same bid across owner cities. Reads Store/EF/catalog/real structures and learns permanent templates, not just D. Claim/identity refresh overlaps. | Historical learning **A**; broad BuildingAdded/Claim recheck **B**. |
| [Standardization readiness/discovery:275](../../../../../Mod/Standardization.lua#L275) | L -> startReady; T+ -> Discover/Flush; P -> startReady/Flush | Each supported-owner T+ enumerates cities. Complete histories can early-return; first/incomplete initialization checks catalog buildings/districts. Retained pending work may reread on successive P within its existing two-turn event lifetime. FC identity Refresh overlaps discovery. | Discovery **B**; necessity of publish rereads **D**. |
| [StandardizationEffects:345](../../../../../Mod/StandardizationEffects.lua#L345) | H; L / T+ / P / X -> mark/flush | X consumes new/old owner/cid with fallback. Reads EF/templates/Bridge and applies carriers. Owner paths enumerate cities before changed-scope filtering. Role/NETWORK/HISTORY bindings overlap. | Health/drain **A**; lifecycle/turn routes **B**. |
| [Commerce:495](../../../../../Mod/Commerce.lua#L495) | L -> Audit; P -> flush; T+ -> Mark; `CityPopulationChanged/CityRemovedFromMap/CityTileOwnershipChanged` -> TargetHook Mark; `GovernmentPolicyChanged/GovernmentChanged/ResearchCompleted/CivicCompleted` -> Mark; X -> Mark all | Scoped pid/cid for supported signatures; policy/technology use pid; X ignores parameters and conservatively marks supported owners. Reads EF/network/native yields; indexed warm work, initial census. Role/D/WORKERS/HISTORY/network notifications overlap. | Extra yield inputs/drain **A**; turn/ownership overlap **B**. |
| [Commerce cross-profession output:543](../../../../../Mod/Commerce.lua#L543) | H; `BuildingAddedToMap/BuildingRemovedFromMap` -> guarded outputAt; `G.BuildingPillageStateChanged` -> guarded Mark | Uses x/y/index/owner or pid/cid/index; excludes own carriers. With D available, ordinary known buildings go through D, but other professions' internal carriers remain explicit inputs to Commerce totals. Unknown metadata stays conservative. | **A**, a real dependency omitted by ordinary D filtering. |
| [Commerce optional construction:555](../../../../../Mod/Commerce.lua#L555) | `G.CityBuilt/G.OnBuildingConstructed/G.OnDistrictConstructed` -> owner Mark | Uses only pid; can overlap D/identity/network. Source explicitly retains these original optional inputs pending signature/producer-closure review. No current clause was found mandating their individual deletion. | **C**, unfinished scoped review; not proven removable. |
| [Commerce embedded observation:455](../../../../../Mod/Commerce.lua#L455), [registrations:496](../../../../../Mod/Commerce.lua#L496) | T- / `G.PlayerTurnStarted` -> diagnosticTurn | Enabled/test-player guards; reads Treasury and enumerates owner cities/carriers when enabled. Observes, does not decide settlements. | **A**, diagnostic responsibility with real scan cost. |
| [CapitalInvestment:417](../../../../../Mod/CapitalInvestment.lua#L417) | L / T+ / X -> Reconcile; P -> flush; Money -> treasuryChanged | pid/newOwner/oldOwner; reconciles existing contract slots, not a building/world census; reads qualified views/network as needed. Same-balance suppression protects Money aliases. FC Role/NETWORK/HISTORY also marks views. | Settlement/money input **A**; lifecycle overlap **B**; optional alias delivery unknown. |
| [DevelopmentInvestment:379](../../../../../Mod/DevelopmentInvestment.lua#L379) | L / P -> flush; T+ -> initialize/Reconcile/Mark; `G.BuildingConstructed/G.OnBuildingConstructed/BuildingAddedToMap` -> building; X -> Reconcile/Audit; Money -> Audit | Building pid/cid/bid or coordinate resolution proves target completion. Uses indexed contracts; first initialize visits supported cities. X uses oldOwner. Money clears owner quotes without Capital's same-balance filter. Role/history/network also notify. | Target completion **A**; recovery/alias overlap **B**. |
| [ClaimProjects:175](../../../../../Mod/ClaimProjects.lua#L175) | `CityProjectCompleted` -> completed; Queue -> immediate current-target check; `CityProductionUpdated/CityInitialized/X` -> wake; T+ / T- -> turn; P -> Flush; L -> initialize | pid/cid/project; queue/Store/qualification and relevant district enumeration for claim. Load visits cities; normal turn work is registered runnable rounds. Role shared wake overlaps lifecycle, not native completion proof. | Completion/order/timing **A**; lifecycle wake **B**. |
| [DialogueProjects:282](../../../../../Mod/DialogueProjects.lua#L282) | `CityProjectCompleted` -> completion; Queue -> production; T+ / T- -> advance; Gov -> immediate qualification audit then markPlayer; `CityInitialized/X` -> wake; L / P / Init | pid/cid/project; completion obtains fresh collection evidence for that city. Gov uses pid, immediately preserves qualification-loss cancellation, then enumerates owner cities for access refresh. Normal timing uses runnable rounds; era changes can widen access work. FC RefreshAccess overlaps only part of this responsibility. | Completion/ordered cancellation/timing **A**; access refresh overlap **B**. |
| [EngineeringStudyProjects:201](../../../../../Mod/EngineeringStudyProjects.lua#L201) | `CityProjectCompleted` -> completion; Queue -> production; T+ / T- -> Flush/advance; Gov -> immediate qualification-only audit then markPlayer; `CityInitialized/CityRemovedFromMap` -> wake; L -> initialize; P -> Flush | pid/cid/project; relevant active rounds/queue/Store/history. Gov immediately handles loss before same-publish restoration; owner access marking still enumerates cities. Role and historical credit notifications are also registered. | Completion/order/timing **A**; later access refresh **B**. |
| [CrewProjects:370](../../../../../Mod/CrewProjects.lua#L370) | `CityProjectCompleted` -> completion; Queue / `CityInitialized/CityRemovedFromMap` -> mark; `UnitAddedToMap/UnitRemovedFromMap` -> inventory mark; Gov -> markPlayer; `WonderCompleted` -> mark; L / P | Completion uses pid/cid/project and unique order/source/completion proof. Unit uses pid/unitID; Wonder uses tail owner/cid. Flush can enumerate one owner's units; Gov markPlayer enumerates cities before dirty merge. Role consumer overlaps. Unlike Engineering, this Gov branch has no immediate cancellation audit. | Settlement/inventory **A**; governor/lifecycle **B**. |
| [ExpeditionTraining:275](../../../../../Mod/ExpeditionTraining.lua#L275) | `UnitAddedToMap` -> Birth; `CityProductionCompleted` -> Complete; Queue -> affected; P / T+ -> Pulse; L / X -> current/recovery | Birth uses pid/unitID; completion uses pid/cid/kind/index/cancelled. Independent proof pairing, source-city queue/eligibility reads; no all-city census. Publish has a finite reader-wait budget of 12. | Birth/completion **A**; bounded recovery **B**. |
| [ExpeditionTraining embedded observation:266](../../../../../Mod/ExpeditionTraining.lua#L266) | `G.OnCityPopulationChanged` / `CityPopulationChanged` -> popWatch; T- -> turnMark | pid/cid/delta or new population; matching source-city scalar observations only, no enumeration or business decision. | **A**, observer. |
| [ExpeditionSpyGate:998](../../../../../Mod/ExpeditionSpyGate.lua#L998), [placement observer:310](../../../../../Mod/ExpeditionSpyGate.lua#L310) | L -> recover/publish; T+ -> Turn; X -> team/target revalidation; `UnitRemovedFromMap` -> exact-unit cleanup; `UnitMoveComplete` -> placement observer | pid/unitID; move observer also x/y, finite watch/tile-unit budget. X ignores exact city but checks current team reference. Pending travel can enumerate player units, not cities. Generic city FC cannot replace unit/task evidence. | Unit/task evidence **A**; conservative X recovery **B**. |
| [Restructuring:259](../../../../../Mod/Restructuring.lua#L259) | `UnitAddedToMap/CityProductionCompleted` -> birth/completion pairing; P -> admit/Flush; `UnitRemovedFromMap` -> clear plans/views; T- -> clear unpaired batch; `UnitMoveComplete/UnitMovementPointsChanged` -> Read; Gov / T+ / L -> refresh | Exact unit/production arguments and unique attribution; never infer nearest city. Owner events synchronize cities and enumerate owned restructuring units to refresh action views. FC phase-zero city synchronization overlaps the city part, not all unit views. | Evidence/unit availability **A**; city synchronization overlap **B**. |
| [InvestmentAction:171](../../../../../Mod/InvestmentAction.lua#L171), [UnitActions:141](../../../../../Mod/UnitActions.lua#L141) | Both: `UnitRemovedFromMap` -> clear matching prepared plan. InvestmentAction also L -> recover pending ledger work | pid/unitID protects against numeric-ID reuse. Load visits supported cities, reads ledger and only finishes already-pending work under existing safeguards. Not ordinary FC recomputation. | **A**, transaction/plan lifecycle. |
| [UI GPPRefresh:73](../../../../../Mod/UI/GPPRefresh.lua#L73) | `CityWorkerChanged/CityFocusChanged` -> mark; L / T+ -> recovery mark; P / PB / `SystemUpdateUI` -> flush | Worker uses pid/cid; Focus trusts only pid. No worker-count read or UI city census. Sends invalidation to NativeFacts; Gameplay also subscribes directly. Owner recovery can widen downstream work. Dirty/reentry/three-attempt guards; no ACK latch here. | Dual producer/turn recovery **B**; dirty drain **A**. |
| [UI ResearchCrossRefresh:51](../../../../../Mod/UI/ResearchCrossRefresh.lua#L51), [IndustryRefresh:37](../../../../../Mod/UI/IndustryRefresh.lua#L37), [BindSampler:206](../../../../../Mod/SampleLifecycle.lua#L206) | AdjSampler (full set in section 2); L -> Reset/safe; T+ / P / PB / `SystemUpdateUI` -> safe/refresh | Event-specific scope described above. Produces native UI BASE facts unavailable through the corresponding Gameplay getter, not a duplicate D value. Full sampling enumerates completed local-player districts; known foreign plot changes can use ring indexes. Local/unknown membership changes can invalidate all. Shared sampleRevision and new game turn also cause census; T+ callback ignores its pid. ACK/epoch/generation protect transport. | BASE production **A**; broad invalidation/turn census **B**. |
| [UI DialogueRefresh:128](../../../../../Mod/UI/DialogueRefresh.lua#L128) | `GreatWorkCreated/GreatWorkMoved/DiplomacyDealEnacted`; `CityAddedToMap/CityRemovedFromMap`; X / T+ / Gov; `DistrictAddedToMap/DistrictRemovedFromMap/DistrictBuildProgressChanged`; L / P / PB / `SystemUpdateUI` -> mark/pulse | Created resolves x/y; Moved uses both owner/cid pairs; Deal has no participant args. Traverses local cities to collect dirty slots and sends GW samples. Gov changes eligibility signatures without recollecting slots. This is an active shared producer, not just the old Dialogue writer. | Collection/transport **A**; turn recollection **B**. |
| [UI DialogueRefresh retired adjacency:163](../../../../../Mod/UI/DialogueRefresh.lua#L163) | `ImprovementAddedToMap/ImprovementRemovedFromMap/FeatureRemovedFromMap/FeatureAddedToMap/CityTileOwnershipChanged` | Each callback only marks when old GreatWorkAdjacency is not retired. Current composition retires it, so callbacks return without useful work. | **C**, empty old-consumer subscriptions; surrounding GW producer remains required. |
| [UI CrewProjectOrder:78](../../../../../Mod/UI/CrewProjectOrder.lua#L78), [hook installation:113](../../../../../Mod/UI/CrewProjectOrder.lua#L113) | P -> adapter Publish/Pulse; L / `LocalPlayerTurnBegin` -> Claim/Dialogue/Engineering WarmStart; Queue+ -> their QueueEvent; training separately P -> Pulse, PB -> RefreshFacts, Gov / T+ -> Invalidate | Host registers distinct callbacks per adapter. P consumers: Capital, Development, Commerce, Crew, Engineering; Pulse consumers: TimedProjectSelection, Claim, Dialogue. Queue uses pid/cid; warm enumeration only in an uninitialized availability generation. Reads/acknowledges native selection, not profession benefit settlement. | **A**, production-operation/readback bridge. |
| [UI ExpeditionSpyActivity:551](../../../../../Mod/UI/ExpeditionSpyActivity.lua#L551), [Window:731](../../../../../Mod/UI/ExpeditionSpyWindow.lua#L731), [TrainingName:157](../../../../../Mod/UI/ExpeditionTrainingName.lua#L157) | Activity: P / L / `LocalPlayerTurnBegin` / Activity / `UnitMoveComplete`; Window: L / `LocalPlayerTurnBegin` / P / `SpyMissionCompleted/SystemUpdateUI`; Name: P / L / `LocalPlayerTurnBegin` / `UnitSelectionChanged` | Exact published owner/unit activity/position/naming and ACK. Window Mission event is observational, not reward proof; SystemUpdateUI handles resize. Name has an existing finite pending update clock, outside native-listener enumeration. | **A**, native-operation confirmation/UI lifecycle. |
| [UI ExpeditionSpyChooser:23](../../../../../Mod/UI/ExpeditionSpyChooser.lua#L23), [UnitPanel:157](../../../../../Mod/UI/ExpeditionSpyUnitPanel.lua#L157) | Chooser replaces native `UnitSelectionChanged`; Panel: P / `UnitSelectionChanged` -> refreshSelected; `UnitSelectionChanged` also -> Restructuring.SelectedChanged; `UnitMoveComplete` -> selected restructuring refresh; Activity -> unitChanged | Selected owner/unit filters; ordinary spies delegate to native base. Panel requests refresh on every P with a team selected, without its own dirty latch. No shared city-fact replacement for routing/activity. | Routing **A**; repeated selected-team refresh **B**. |
| [UI UnitPanelActions:273](../../../../../Mod/UI/UnitPanelActions.lua#L273), [UnitTargetMarkers:185](../../../../../Mod/UI/UnitTargetMarkers.lua#L185) | Both: `CityProductionChanged/CityProductionUpdated/CityProductionCompleted/CityBuildQueueChanged`, `DistrictBuildProgressChanged/DistrictRemovedFromMap`, T+ / X / `LocalPlayerTurnBegin`, `UnitMoveComplete/UnitRemovedFromMap/UnitTeleported/UnitSelectionChanged`, `InterfaceModeChanged/LocalPlayerChanged`, L / P / PB. Buttons additionally GovernorAssigned/Established/Promoted and `BuildingAddedToMap/BuildingRemovedFromMap` | mark/signal/unitChanged/selectedChanged/pump; supported pid/selected-unit/revision/dirty guards. Coordinate events do not misinterpret x as pid. Normal read is selected actor; requested target construction can enumerate candidate cities. | UI projection **A**; broad overlapping refresh causes **B**. |
| [UI CommercePanel:139](../../../../../Mod/UI/CommercePanel.lua#L139), [CapitalPanel:155](../../../../../Mod/UI/CapitalInvestmentPanel.lua#L155), [DevelopmentPanel:248](../../../../../Mod/UI/DevelopmentInvestmentPanel.lua#L248) | P -> publish; L / `LocalPlayerChanged` -> close; `SystemUpdateUI` -> resizeEvent | No business event arguments; open-panel city/reply/revision checks before rendering. Card iteration is not a world/building census; no business Audit is added here. | **A**, presentation lifecycle. |
| [LevelBannerState:40](../../../../../Mod/LevelBannerState.lua#L40), [UI LevelBanners:53](../../../../../Mod/UI/LevelBanners.lua#L53), [CityPotential:215](../../../../../Mod/UI/CityPotential.lua#L215) | State: Gov / T+ / `CityAddedToMap/CityRemovedFromMap` / X / L / P / PB. Banner UI: P / PB / L / `LocalPlayerChanged`. CityPotential: Gov / T+ / `CitySelectionChanged/LocalPlayerChanged` / L / P / PB | State uses pid/cid, owner-city enumeration on governor marks; Role also comes through FC. Banner/UI callbacks read published projection/selected city and maintain visual instances, not gameplay effects. | State duplicate routes **B**; UI projection **A**. |
| [Old Dialogue:357](../../../../../Mod/Dialogue.lua#L357), [retirement cutover:995](../../../../../Mod/Gameplay.lua#L995) | Gov -> anonymous callbacks; X -> lifecycle callback | All four governor callbacks return immediately when retired, as current composition enforces. X still clears samples/paired session state in the retired branch; no old positive effects resume. | Gov **C**; retained X cleanup **A**. |
| [Lv3Support:111](../../../../../Mod/Lv3Support.lua#L111), [Lv3Effects:155](../../../../../Mod/Lv3Effects.lua#L155) | Both L / T+ / X; Effects additionally `CityPopulationChanged` and `G.OnDistrictConstructed/G.OnBuildingConstructed/G.CityBuilt` | Current facades retire exact old effects. Load runs cleanup; other callbacks only retry failed/exit candidates, not old positive yields. FC also calls facades. Effects' extra broad events do not carry a demonstrated distinct policy duty here. | Exact cleanup/recovery **B**; extra Effects causes **C**, not yet proven safe to remove. |
| [NetworkBoost:169](../../../../../Mod/NetworkBoost.lua#L169), [CommerceConvergence:36](../../../../../Mod/CommerceConvergence.lua#L36), [PurchaseProbe:27](../../../../../Mod/PurchaseProbe.lua#L27) | NetworkBoost L / P / T+ -> initialize; others L -> exact old-carrier cleanup | NetworkBoost retired mode still installs these three hooks: success becomes no-op, P only before first attempt, failed cleanup retries on a real turn. Cleanup enumerates cities/fixed old IDs, not network recomputation. Convergence/Purchase retain actual load cleanup. | Cleanup/init **A**; bounded turn recovery **B**. |

## 4. Shared delivery paths and local event chains

### 4.1 Source and consumer overlap

[FactConsumerBindings:20](../../../../../Mod/FactConsumerBindings.lua#L20) declares the research, culture, network, investment and retired-facade consumers. Its [provider selection:69](../../../../../Mod/FactConsumerBindings.lua#L69) can subscribe directly to D/network providers; remaining domains use FC. [Gameplay:837](../../../../../Mod/Gameplay.lua#L837) flushes FC then the bindings in the declared read phase. A binding, a direct native callback, a GW callback and a module-local dirty queue are separate routes; none alone proves all earlier work has coalesced.

Relevant common producers were checked without turning this into a whole-repository producer audit:

- [NativeFacts:50](../../../../../Mod/NativeFacts.lua#L50): worker/focus invalidation; [governor registrations:59](../../../../../Mod/NativeFacts.lua#L59): ACTIVE invalidation.
- [DistrictCompleteness:265](../../../../../Mod/DistrictCompleteness.lua#L265): structural native changes -> D; known internal buildings are filtered.
- [GreatWorkFacts:360](../../../../../Mod/GreatWorkFacts.lua#L360): city/Great Work changes invalidate collection facts, with UI sample transport supplying confirmation.
- Store history, lifecycle/exit/return callbacks and direct provider consumers also notify ability owners; they are not all native event subscriptions.

### 4.2 Worker/focus: two invalidation producers

```text
E.CityWorkerChanged / E.CityFocusChanged
  -> Gameplay NativeFacts -> WORKERS invalidation
  -> FC / FactConsumerBindings -> affected ability Audit

same native change in UI
  -> GPPRefresh mark -> existing LV2_GPP_DIRTY request
  -> Gameplay NativeFacts -> WORKERS invalidation -> affected consumers
```

[GPP ingress:643](../../../../../Mod/Gameplay.lua#L643) is invalidation transport, not an authoritative worker-count payload. UI does not duplicate the gameplay count getter. Dirty merging and idempotent effect writes protect correctness, but two deliveries separated by a drain can still cause separate Audits. Native duplication rate is not measured here.

### 4.3 Governor: final eligibility versus ordered project transitions

```text
E.Gov -> NativeFacts ACTIVE -> FC/bindings -> effects/access refresh
E.Gov -> Dialogue / Engineering immediate qualification audit
       -> cancel an actually disqualified running project before later restoration
       -> mark access work for later flush
```

The immediate cancellation branch has information that a coalesced final-state eligibility refresh can lose. Crew governor callbacks, by contrast, mark owner cities without that same immediate qualification audit. Restructuring additionally updates unit action views. These listeners must not be grouped as equivalent merely because they share the event name.

### 4.4 Project completion: evidence, committed history, then effects

```text
E.CityProjectCompleted(pid,cid,project)
  -> matching independent controller
  -> queue/timing/eligibility/unique completion checks
  -> Store receipt or historical commit
  -> HISTORY / topic notification
  -> effect owner rereads confirmed history and reconciles carriers
```

UI queue adapters read/acknowledge selection and production state on a separate side of this chain. They do not replace Gameplay completion settlement, and their presence does not prove duplicate rewards. Unit-based training similarly needs independent birth and production evidence.

### 4.5 Internal carrier changes: a deliberate separate edge

```text
internal carrier removed/changed
  -> D ignores known internal building
  -> owner's exact H listener -> scoped recovery work
  -> Commerce's other-profession-output listener -> mark native total-yield input
```

The two consumers have different duties. H handles only its own exact carrier IDs; Commerce excludes its own IDs but must observe other professions' output changes. The approved Pillage=0 carrier policy does not make unexpected removal/health handling automatically redundant. This report requests no deliberate pillage test.

## 5. Architecture comparison and classification boundaries

The current [P01-P10 integration contract:160](../../../../Architecture/Specialization_v0.1_Architecture.md#L160) requires one fact/effect owner, preserved cause/scope, bounded work and meaningful recovery. P03 says to coalesce redundant recomputation, **not ordered transactions or real same-turn changes**. P06 requires eligible pending work rather than endless publish retries. P08 requires responsibility migration before deleting retired/probe code.

The [shared update contract:179](../../../../Architecture/Specialization_v0.1_Architecture.md#L179) preserves necessary former-holder/foreign recovery, including GPP withdrawal after an UNKNOWN read. It does not authorize treating all foreign or turn events as irrelevant.

[U1 D4:637](../../../../Architecture/Specialization_v0.1_Architecture.md#L637) preserves independent Claim/Dialogue/Engineering policy and forbids introducing polling, unrelated-event checks or no-progress project retries through their abstraction. [D5:638](../../../../Architecture/Specialization_v0.1_Architecture.md#L638) requires unique Crew completion proof. [D12:643](../../../../Architecture/Specialization_v0.1_Architecture.md#L643) requires Q1-Q8 duties to migrate before removal. None is a blanket instruction to route all native events through FC.

The Authority marks `Architecture/v2/Events_Dirty.md` historical-only; it is not used here as a current mandatory migration instruction. Existing code demonstrates implementation, not that a dependency is necessarily desirable. Likewise, C means a scoped question/residue, not an approved deletion plan.

## 6. Inactive branches, exclusions and unknowns

The following are not counted as normally active production listeners:

- Several research/culture/Commerce/Industry fallback event lists only register if D or relevant shared consumer APIs are absent. Successful normal composition has those providers. Missing-provider startup is a distinct conditional configuration, not evidence of duplicate active listeners.
- CrossRefresh's BindSampler call has `workers=false`; the helper's Worker/Focus/Population branch is not active for Cross.
- CopyYieldRefresh and DiscountEligibility are packaged imports without a production AddUserInterfaces/include activation path found in this audit.
- Retired CopyYields, StandardizationDiscount, HalfYieldProbe and CultureInspirationProbe return before their old positive-path hook lists. Old Lv3Support historicalStart is not the current Start implementation. Lv4Percent is a no-op facade. These differ from NetworkBoost/CommerceConvergence, which retain live cleanup hooks.
- Old ExpeditionGate/ExpeditionMovementProbe paths are not the current started SpyGate implementation. CultureMeaningProbe is not normally started. Include/import presence alone is insufficient.
- Custom `GameEvents.SPC_*`, LuaEvents, UI control callbacks and `ContextPtr` update/init/shutdown handlers are not native Events/GameEvents subscriptions. The embedded training diagnostic sink uses `LuaEvents.SPC_B205TrainingTrace`; it is not an additional native Publish listener.
- Inherited native Popup/Panel listeners are not all newly added by the Mod. SpyChooser explicitly removes/replaces its captured native selection callback. Dedicated P0 production/overflow experiments and standalone timing diagnostics are outside the four-profession consumer scope; their separate production duties are not declared dispensable.

Unresolved evidence boundaries:

1. Which optional native aliases exist and fire in the user's exact engine/ruleset, and in what order across Gameplay/UI.
2. How often overlapping causes collapse into one dirty flush versus arrive after an earlier audit has already run.
3. Whether each broad turn/owner safety census still covers a necessary native omission; the static audit does not prove it can be removed.
4. Whether Standardization's bounded successive-publish rereads are required by an actual availability gap, or retain avoidable retry work.
5. Workload and engine cost attributable to each route. Enumeration is identified, not timed; no claim that these listeners explain a particular live slowdown is made.

No new game test is requested by this report. Existing user-owned acceptance remains separate. If a later task narrows one of these questions, its evidence/implementation scope must be defined then; this report is not a large refactor proposal or a new backlog-clearing mandate.

## 7. Read Ledger and handoff

Stage A: current root/project/topic guidance, Workflow role/checkpoint/language rules, Authority/Status current metadata, existing Architecture Reconstruction reports and the user's direct-listener scope. Stage B: named composition Start/guards and modinfo activation, helper-installed hooks, four-profession effects/actions/projects, corresponding UI samplers/operation bridges, FC/binding/provider paths, and current Architecture P/D clauses. Delegated bounded reviews covered Research/common, Culture, and Industry/Commerce; Primary resolved helper activation and retired-vs-live cleanup distinctions.

No new Stage C topic, external HD/game scan, live runtime frequency measurement, gameplay testing, code repair, formal document migration, Design/Architecture/Authority/Status/Context Lock edit or deployment was undertaken. Recording this report and adding its topic navigation are the only requested repository-content changes.

User decision: none required to preserve this investigation; classifications are not implementation approval.

User testing: none newly required; native delivery/frequency questions remain UNKNOWN.

Primary next: preserve the reviewed report/navigation checkpoint and stop. Reopen only the relevant scoped question if separately requested.
