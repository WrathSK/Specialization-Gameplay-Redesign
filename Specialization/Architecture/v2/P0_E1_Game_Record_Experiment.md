# P0-E1 supplemental experiment — B089.116

Status: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. User explicitly authorized this reviewed one-city spike. E1 overall gate remains HELD; no E2/F. W0004 L3 risk-relevant tests only.

## Scope and storage

`CityIdentityExperiment.lua` is opt-in, separate from CityIdentityRead and all gameplay consumers. It writes only `Game:GetProperty/SetProperty("SPC_E1_IDENTITY_EXPERIMENT_V1")`, not an external disk file. One watched city per save, schema=1, original owner/id/x/y + original DEV token (experiment identifier only), requester, revision, start turn, saved observed reference, four native getter observations and at most 16 deduplicated event records. No copied professional ledger, name-based identity, ownership migration, carrier, new yield or old inheritance Start.

Game storage is intended to follow the save/branch; actual persistence across Free City transfer and reload still needs native evidence. Returning to B088 ignores this independent key. Start a new experiment from the pre-experiment save; never overwrite a long-play save. Existing keys and writers remain byte-identical. This does not establish a permanent cityKey or any profession's conquest policy.

## Evidence and failure contract

Start is explicit right-click on 记录城市身份; requires an owned test-player city and valid old readonly preview. Use a noncapital branch city so the existing Free City cheat can transfer it. Start records one baseline; repeated starts never replace it. Left-click 实验对照 reads/checkpoints evidence; no selected owned city required.

Events only observe the watched origin/ref/plot; no periodic scanner, UI hover requests or callback Property writes. Transfer may make one watched-plot lookup. Buffer is fixed16; exhaustion is reported and blocks a mapping candidate. Four optional Gameplay getters use pcall: GetOriginalOwner, GetOwnerBeforeOccupation, GetJustConqueredFrom, GetLastTransferType. Their UI precedents are STATIC_CONFIRMED only, Gameplay availability/meaning USER_GAME_TEST_REQUIRED. Unknown transfer-type numeric values are not interpreted.

MAPPING_CANDIDATE requires this-load, current-turn removal of the origin and transfer/conquest matching the new reference plus native prior-owner corroboration. It remains experimental, never authorizes migration. Missing/ambiguous/late/overflow evidence = HELD. Same reference alone does not prove permanent generation identity; raze/refound and multi-hop transitions are outside this spike's proof. Coordinates locate an object, never establish identity alone.

On LoadScreenClose transient observations reset, saved experiment is read once; old saved events cannot authorize a new mapping. Saved state and current observation are shown separately. On-demand checkpoint is idempotent; comparison against stored revision/content rejects unexpected concurrent changes. Malformed record, read/write failure stop the experiment without repairing any old ledger or repeated write attempts. No gameplay output depends on this record.

## Local evidence

`DevelopmentTests/test_p0_e1_experiment.py`: actual Lua + original E1 fixture; opt-in/new-key-only writes, event callbacks zero writes, duplicate notifications and16-entry bound, transfer candidate/unknown native/late events, cold load, malformed record, failed readback, concurrent modification and missing baseline; actual Gameplay dispatch/UI callbacks,128 idle notifications zero requests; all Lua syntax/XML/modinfo116; protected runtime writers and Design identical to277b3b6. This targeted L3 suite does not rerun full historical gameplay/stress tests or claim native PASS.

## One minimal user test

1. Load an independent pre-transfer test save, select an owned specialization noncapital city. Confirm B089.116. **Right-click 记录城市身份**; expect 单城实验已建立. Screenshot.
2. Use the same Free City transfer as B088. Before ending the turn, **left-click 实验对照**. Screenshot; candidate or HELD are both useful native evidence. No need to reconquer.
3. After that checkpoint, save to a new slot and load it. Do not establish another experiment. Left-click 实验对照 and screenshot. Expect saved revision/events preserved and current-load events0; same current reference if still present. Report UNKNOWN getter values rather than guessing.

This tests Game record persistence and native evidence only. It does not restore specialization effects lost on conquest or complete E1's full identity gate. Stop pending user evidence.

## W0003 deployment

B089.116 / modinfo116, source `1c8b92e3f23773973c440bb8c8f6054a66ee4870`. Game process exited (OS checked); existing transaction tool preserved B088 and stable recovery, staged replacement completed, **149/149 source/runtime files MATCH**. Receipt: external `SpecializationDeploymentBackups/B089.116-1c8b92e-playtest.json`; no abnormal recovery. Main unchanged, no game launched.
