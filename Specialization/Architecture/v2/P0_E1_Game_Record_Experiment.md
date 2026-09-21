# P0-E1 supplemental experiment — B089.116

Status: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. User explicitly authorized this reviewed one-city spike. E1 overall gate remains HELD; no E2/F. W0004 L3 risk-relevant tests only.

## Scope and storage

`CityIdentityExperiment.lua` is opt-in, separate from CityIdentityRead and all gameplay consumers. It writes only `Game:GetProperty/SetProperty("SPC_E1_IDENTITY_EXPERIMENT_V1")`, not an external disk file. One watched city per save, schema=1, original owner/id/x/y + original DEV token (experiment identifier only), requester, revision, start turn, saved observed reference, four native getter observations and at most 16 deduplicated event records. No copied professional ledger, name-based identity, ownership migration, carrier, new yield or old inheritance Start.

Game storage is intended to follow the save/branch; actual persistence across Free City transfer and reload still needs native evidence. Returning to B088 ignores this independent key. Start a new experiment from the pre-experiment save; never overwrite a long-play save. Existing keys and writers remain byte-identical. This does not establish a permanent cityKey or any profession's conquest policy.

## Evidence and failure contract

Start is explicit right-click on 记录城市身份; requires an owned test-player city and valid old readonly preview. Use a noncapital branch city so the existing Free City cheat can transfer it. Start records one baseline; repeated starts never replace it. Left-click 实验对照 reads/checkpoints evidence; no selected owned city required.

Events only observe the watched origin/ref/plot; no periodic scanner, UI hover requests or callback Property writes. Transfer may make one watched-plot lookup. Buffer is fixed16; exhaustion is reported and blocks a mapping candidate. Four optional Gameplay getters use pcall: GetOriginalOwner, GetOwnerBeforeOccupation, GetJustConqueredFrom, GetLastTransferType. Their UI precedents are STATIC_CONFIRMED only, Gameplay availability/meaning USER_GAME_TEST_REQUIRED. Unknown transfer-type numeric values are not interpreted.

MAPPING_CANDIDATE requires this-load, current-turn removal of the origin and transfer/conquest matching the new reference plus native prior-owner corroboration. It remains experimental, never authorizes migration. Missing/ambiguous/late/overflow evidence = HELD. Same reference alone does not prove permanent generation identity; raze/refound and multi-hop transitions are outside this spike's proof. Coordinates locate an object, never establish identity alone.

B090: each fresh Gameplay context starts with empty transient observations. LoadScreenClose or the first explicit request initializes saved state once; a late/duplicate callback cannot reset evidence or clear a storage failure. Old saved events cannot authorize a new mapping. Saved state and current observation are shown separately. On-demand checkpoint is idempotent; comparison against stored revision/content rejects unexpected concurrent changes. Malformed record, read/write failure stop the experiment without repairing any old ledger or repeated write attempts. No gameplay output depends on this record.

## Local evidence

`DevelopmentTests/test_p0_e1_experiment.py`: actual Lua + original E1 fixture; opt-in/new-key-only writes, event callbacks zero writes, duplicate notifications and16-entry bound, transfer candidate/unknown native/late events, cold load, malformed record, failed readback, concurrent modification and missing baseline; actual Gameplay dispatch/UI callbacks,128 idle notifications zero requests; all Lua syntax/XML/modinfo116; protected runtime writers and Design identical to277b3b6. This targeted L3 suite does not rerun full historical gameplay/stress tests or claim native PASS.

## One minimal user test

1. Load an independent pre-transfer test save, select an owned specialization noncapital city. Confirm B089.116. **Right-click 记录城市身份**; expect 单城实验已建立. Screenshot.
2. Use the same Free City transfer as B088. Before ending the turn, **left-click 实验对照**. Screenshot; candidate or HELD are both useful native evidence. No need to reconquer.
3. After that checkpoint, save to a new slot and load it. Do not establish another experiment. Left-click 实验对照 and screenshot. Expect saved revision/events preserved and current-load events0; same current reference if still present. Report UNKNOWN getter values rather than guessing.

This tests Game record persistence and native evidence only. It does not restore specialization effects lost on conquest or complete E1's full identity gate. Stop pending user evidence.

## W0003 deployment

B089.116 / modinfo116, source `1c8b92e3f23773973c440bb8c8f6054a66ee4870`. Game process exited (OS checked); existing transaction tool preserved B088 and stable recovery, staged replacement completed, **149/149 source/runtime files MATCH**. Receipt: external `SpecializationDeploymentBackups/B089.116-1c8b92e-playtest.json`; no abnormal recovery. Main unchanged, no game launched.

## B090.117 authorized startup fix

B089 native start failure is recorded in Status. Exact failed combined operand was not exposed; the load-only initialization dependency is now removed. First valid explicit Begin/Describe can initialize the Game experiment record. No auto polling, no background retry or old-ledger writes. Missing/foreign city, non-test player, missing baseline and temporarily unavailable Game read return separate concise messages without poisoning the session; a later manual action can retry. Corrupt saved experiment, concurrent change or failed write/readback still latch failure. Report shows first error line, not stack/path noise. Late LoadScreenClose cannot clear the latch or discard watched events. Schema/key unchanged.

LOCAL_SIMULATION_PASS: original targeted experiment suite plus absent load callback (Begin and saved-record Describe), duplicate/late callback, invalid selection→valid retry, temporary read failure→manual retry, missing baseline→valid retry, and write failure latch surviving load notification. Full Lua syntax/XML/manifest117; unchanged old writers and Design. No full gameplay/stress suite. USER_GAME_TEST_REQUIRED: repeat the same short one-city experiment after loading B090; B089 failure occurred before its first write, so no manual cleanup is needed. E1 remains HELD, no E2/F.

B090 W0003 deployment: source `1992d75b34c03701c5d06a16c4af9e7f0bccf6e7`, game exited (OS verified),149/149 MATCH;B089/stable transaction recovery retained. Receipt `SpecializationDeploymentBackups/B090.117-1992d75-playtest.json`. No game launch/main change.

## B091.118 — authorized UI transfer evidence supplement

STATIC_CONFIRMED: [Sukritact City API](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/City) marks GetOwnerBeforeOccupation/GetJustConqueredFrom/GetLastTransferType UI-only; OriginalOwner also Script. Native RazeCity UI uses them. HD CivilizationTraits PersiaCityConquered uses GameEvents.CityConquered(newOwner,oldOwner,newCityID,x,y); native Expansion2 TutorialLoader uses CulturalIdentityCityConverted(player,cityID,fromPlayer). Neither proves Cheat Free City event semantics. [GCO ModUtils](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_ModUtils.lua) correlates district removal and city creation by turn/position/original owner, a precedent with repeated-conquest limitations, not a ready-made identity authority.

New `UI/CityIdentityEvidence.lua`: right-click 实验对照 reads the existing experiment origin from Game Property in UI, then probes four getters with distinct ABSENT/LOOKUP_ERROR/CALL_ERROR/value-and-type. No cross-context request, Property write, gameplay application or change to HELD. UI events CityTransfered/CulturalIdentityCityConverted/CityLiberated observed after the first manual UI read, restricted to watched old/current endpoint, deduplicated fixed8 entries. Zero periodic scans; at most one watched-plot lookup per relevant subscribed event. New Gameplay observers add the latter two event names to existing fixed16 evidence only; resolver unchanged. Raw extra transfer args remain uninterpreted. UI evidence is ephemeral; screenshot before reload. Cold UI context starts empty. No claim UI prior-occupation owner equals immediately previous owner.

LOCAL_SIMULATION_PASS: existing risk-scoped experiment checks plus actual right-click zero requests, absent/error/nil/numeric differentiation, buffer8, cold context reset, loyalty event observation. Lua/XML/manifest118 and old writer/Design equality. USER_GAME_TEST_REQUIRED remains for UI getter values and event availability.

Minimal test (no reconquest or repeat save/load required): load pre-transfer independent save on B091.118; right-click 记录城市身份 to establish if needed, then **right-click 实验对照 before transfer** and screenshot. Transfer same branch city to Free Cities; same turn right-click 实验对照 and screenshot. Optional left-click keeps the existing Gameplay checkpoint, not needed for this UI evidence comparison. Two screenshots suffice; do not weaken identity requirements based only on an original-owner match. No E2/F.

B091 W0003 deployment: source `42b7625fedbe888dd8c590f6cba6e0eccb91a4e3`, game exited (OS verified),150/150 MATCH;B090/stable recovery retained. Receipt `SpecializationDeploymentBackups/B091.118-42b7625-playtest.json`. Main unchanged; no game launched.

## Event-first research conclusion after B091 supplemented evidence

See [paired native evidence](../../Status/Validation/Results/Specialization_B091_P0E1_Transfer_Chain_Review.md). The Free City UI event now supplies oldOwner directly. Do not keep requiring a UI-only previous-owner getter in every Gameplay path. Storage and identity evidence remain separate: B090 tested the independent Game record; B091 now demonstrates a usable typed transfer signal in UI.

Recommended next bounded **shadow resolver** (planning only, not implemented):

1. Start from saved validated experiment origin/current reference and one known location; no city-name key.
2. For a loyalty transfer, correlate CulturalIdentityCityConverted(newOwner,newID,fromOwner) with exact watched prior-owner, current new reference at watched plot and prior-reference removal evidence in the same live transition. Use prior snapshot to supply oldCityID; event does not supply it. For conquest, CityConquered(newOwner,oldOwner,newID,x,y) is a separate candidate path; do not label it native-tested yet.
3. First verify whether the already registered Gameplay callback supplies these values. Prefer direct Gameplay evidence. If only UI has them, a later narrow UI sample bridge needs explicit epoch/ref/request validation and corroboration; never turn a screenshot or arbitrary UI payload into authority. No per-frame fallback or world scan.
4. Reject conflicts/multiple candidate transitions, missing baseline/removal, stale saved events, buffer overflow or intervening destruction/refoundation. Coordinates locate; they do not establish generation. CityBuilt/Added/Initialized alone cannot mean a new physical city because transfers also emit these.
5. Output would be an experimental shadow candidate with concrete reasons; no binding/Journal/Flow/Investment/template rewriting. Idempotent duplicate events, A→B→C chain scope, same-turn refound ambiguity and load interruption require targeted model cases before any resolver implementation. Ambiguous histories remain HELD; do not solve them by name or founder equality.

No need to repeat the identical Free City UI test. Next implementation proposal should expose recorded Gameplay event names/arguments and an event-based shadow conclusion together, reusing the existing fixed buffer. Full E1/P0-E2 gate remains closed until its intended support scope and rollback/ambiguity limits are reviewed. This research does not authorize cutover, automatic migration, new ledger schema or E2/F.
