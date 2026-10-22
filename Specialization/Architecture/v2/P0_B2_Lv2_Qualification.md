# P0-B2 — Lv2 Housing / base GPP qualification

Build: B080.107 / modinfo107. Authority: D0035 scoped Shared/Lv2, Research D0031, Culture D0029, Industry/Commerce D0032; Architecture A0161 unchanged. User explicitly authorized P0-B2 after W0001 revalidation. Runtime baseline: 845cda1 (B079.106 implementation b420a96).

Status: LOCAL_SIMULATION_PASS — actual Lua with deterministic native mocks and actual carrier SQL; NOT engine PASS. Await one user test. Four professions only; no Military, P0-C, new named abilities, new carriers, ownership restore, Design change, or permanent Property/schema writes.

## Implementation and authority

- `Lv2Housing.lua`: shared `SpecialistSupport.Anchor` + ephemeral RuntimeWork player district index; `DistrictCompleteness` supplies reviewed ordinary-building rows, actual location, completion and pillage. Select the actual specialty anchor ID, NOT highest-D district. Count one base district housing + each distinct positive normalized Tier. Never use D.value/sum(Tier) or per-building count. Read failure/conflicting tier preserves existing housing; complete confirmed ineligibility removes exactly once.
- `Lv2GPP.lua`: reuse same anchor/ACTIVE contract; actual working specialist count => unchanged native 2 base points per worker/class. Culture has Writer/Artist/Musician each2. Validate all32 carrier reads before removing/adding bits. UNKNOWN no longer means workers0. Native percent modifiers remain engine-owned; no ChangePointsTotal.
- `OrdinaryBuildingCatalog.lua`: add ONLY five reviewed legacy Housing candidates: FAIR, HD_ART_PUBLISHING_HOUSE, HD_DATA_CENTER, HD_ELECTRONICS_FACTORY, HD_INTERNET_COMPANY. Existing classifier/replacement conflict rules remain. P0-A D/shadow can now recognize these ordinary entries, an intentional catalog-coverage correction; formula unchanged. No Harbor/Neighborhood expansion.
- `Gameplay.lua`: existing action refreshes scoped to requesting player; governor-fact bridge also refreshes housing. Combined COMPLETENESS_READ appends both real read-only reports. UI keeps existing slot/layout, label `基础设施 / Lv2住房与专家`, and reuses native empire-GPP UI renderer. GPPRefresh protocol unchanged.
- No new module or yield definition. Existing9 housing IDs and32 GPP IDs retained verbatim, including housing slots5..8 for removal of old projections. No parallel legacy writer. `SPC_Lv2HousingTiers` SQL remains a historical compatibility definition but has NO runtime reader in B2. SQL/Data unchanged.

## Validity, lifecycle and events

All desired facts and installed carrier reads are checked before first write. Remove stale before add; unchanged input writes0. UNKNOWN ACTIVE/worker/native building state/unsupported ordinary tier holds installed projection, exposed as diagnostic error. Confirmed ACTIVE<II, NONE, missing/unfinished/pillaged anchor remove once; workers0 removes GPP only. No stored sample/request/history introduced. Existing D cache max8 and context/load epoch remain; no old pending state. Last error map is current-city/player diagnostic state, reset on full audits/load/removal scope; no error history or per-event logging.

Housing direct events: governor assignment/establishment/change/promotion; building add/remove/pillage/repair; district removal/progress/pillage/repair; city transfer/removal; GameEvents construction/city creation/pillage; explicit specialization actions. GPP additionally worker/focus changes. Known player signatures scoped; unknown plot/transfer signatures conservatively audit current players. Existing building event adapter ignores SPC carriers. **CityBuildingsChanged is deliberately not a full-audit trigger** because own carriers may emit it; structural events plus turn fallback cover changes. No Publish/Playback/SystemUpdateUI/unit-move audit listeners. GPP UI may flush already-dirty notification under existing <=3-attempt rule; it does not mark dirty on idle pulses.

Fallback: once per player per turn via RuntimeWork turn guard; missing direct native events can recover next turn. Direct real events can perform more than one audit per turn; equality stops writes, not all necessary input reads. Housing explicitly dirties the selected city's bounded shared sample before its event/manual read, avoiding same-turn stale reuse. Manual diagnostics can scan the selected city, never write carriers. No per-frame/hover requests or timers added.

## Catalog preflight — evidence limits

Read-only installed HD source `2465378070/UpdateDataBase/HD_BuildingTiers.sql` computes tiers0..4; its SHA256 and exact50-row database snapshot are in `DevelopmentTests/Fixtures/P0B2/housing_catalog.json`. The database's active-set/session provenance is unproven: static evidence, NOT current-game confirmation. Runtime uses its own loaded GameInfo tier/replacement data, not this snapshot or a Data Center constant.

49 historical rows retain observed tier and pass actual old/new nonempty housing-output comparison; DATA_CENTER old table5 vs observed HD4 is an explicit adapter reclassification, **not Tier5 clamped to4**. Lab+Data Center in the observed environment share Tier4 and grant one housing tier increment. If another environment actually reports Tier5/conflict, the current catalog yields unavailable: preserve installed housing and diagnostic error, do not silently drop/clamp the building. This is an environment adapter limitation requiring investigation, not new Design or normalization. All five added rows are ordinary, non-Wonder, non-internal in this snapshot. Broader catalog completeness remains open; earlier P0-A PASS never meant every HD building.

| Historical housing building | Old Tier | Observed shared Tier | Disposition |
|---|---:|---:|---|
| BUILDING_AMPHITHEATER | 1 | 1 | RETAIN |
| BUILDING_BANK | 3 | 3 | RETAIN |
| BUILDING_BROADCAST_CENTER | 4 | 4 | RETAIN |
| BUILDING_COAL_POWER_PLANT | 4 | 4 | RETAIN |
| BUILDING_FACTORY | 3 | 3 | RETAIN |
| BUILDING_FAIR | 1 | 1 | RETAIN |
| BUILDING_FILM_STUDIO | 4 | 4 | RETAIN |
| BUILDING_FOSSIL_FUEL_POWER_PLANT | 4 | 4 | RETAIN |
| BUILDING_GRAND_BAZAAR | 3 | 3 | RETAIN |
| BUILDING_HD_ART_PUBLISHING_HOUSE | 3 | 3 | RETAIN |
| BUILDING_HD_DATA_CENTER | 5 | 4 | RECLASSIFY_DYNAMIC_HD_TIER |
| BUILDING_HD_ELECTRONICS_FACTORY | 3 | 3 | RETAIN |
| BUILDING_HD_INTERNET_COMPANY | 4 | 4 | RETAIN |
| BUILDING_IZ_WATER_MILL | 1 | 1 | RETAIN |
| BUILDING_JNR_ACADEMY | 1 | 1 | RETAIN |
| BUILDING_JNR_ARCHITECTURE | 3 | 3 | RETAIN |
| BUILDING_JNR_ASSEMBLY | 1 | 1 | RETAIN |
| BUILDING_JNR_CABINET | 2 | 2 | RETAIN |
| BUILDING_JNR_CHEMICAL | 3 | 3 | RETAIN |
| BUILDING_JNR_COMMODITY_EXCHANGE | 4 | 4 | RETAIN |
| BUILDING_JNR_EDUCATION | 4 | 4 | RETAIN |
| BUILDING_JNR_FREIGHT_YARD | 4 | 4 | RETAIN |
| BUILDING_JNR_GRAND_HOTEL | 3 | 3 | RETAIN |
| BUILDING_JNR_GUILDHALL | 3 | 3 | RETAIN |
| BUILDING_JNR_LABORATORY | 3 | 3 | RETAIN |
| BUILDING_JNR_LIBERAL_ARTS | 3 | 3 | RETAIN |
| BUILDING_JNR_MANSION | 2 | 2 | RETAIN |
| BUILDING_JNR_MANUFACTURY | 2 | 2 | RETAIN |
| BUILDING_JNR_MARKETING_AGENCY | 4 | 4 | RETAIN |
| BUILDING_JNR_MEDIA_CENTER | 4 | 4 | RETAIN |
| BUILDING_JNR_MERCHANT_QUARTER | 3 | 3 | RETAIN |
| BUILDING_JNR_MINT | 2 | 2 | RETAIN |
| BUILDING_JNR_OPERA | 3 | 3 | RETAIN |
| BUILDING_JNR_REAL_ACADEMY | 3 | 3 | RETAIN |
| BUILDING_JNR_SCHOOL | 2 | 2 | RETAIN |
| BUILDING_JNR_WAYSTATION | 1 | 1 | RETAIN |
| BUILDING_JNR_WIND_MILL | 1 | 1 | RETAIN |
| BUILDING_LIBRARY | 1 | 1 | RETAIN |
| BUILDING_MADRASA | 2 | 2 | RETAIN |
| BUILDING_MARAE | 1 | 1 | RETAIN |
| BUILDING_MARKET | 2 | 2 | RETAIN |
| BUILDING_MUSEUM_ART | 3 | 3 | RETAIN |
| BUILDING_MUSEUM_ARTIFACT | 3 | 3 | RETAIN |
| BUILDING_NAVIGATION_SCHOOL | 2 | 2 | RETAIN |
| BUILDING_POWER_PLANT | 4 | 4 | RETAIN |
| BUILDING_RESEARCH_LAB | 4 | 4 | RETAIN |
| BUILDING_STOCK_EXCHANGE | 4 | 4 | RETAIN |
| BUILDING_SUKIENNICE | 2 | 2 | RETAIN |
| BUILDING_UNIVERSITY | 2 | 2 | RETAIN |
| BUILDING_WORKSHOP | 2 | 2 | RETAIN |

## Local acceptance

Run with configured Lua55/Lupa environment:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_p0_b2.py`

`... DevelopmentTests/test_p0_b2_regression.py`

- Actual Lua+P0-A capture +actual41 SQL carriers/48 native GPP definitions. Four professions × ACTIVE1..4 × workers0/1/3 compare old/new valid outputs; normal scenarios assert no module errors.
- Housing empty/T1/T1T2/T1T2T3/T1..T4/onlyT3 =>1/2/3/4/5/2. Same-tier duplicates, free ordinary, unique building/district, missing lower tiers, unfinished, building/district pillage/repair, non-anchor higher D, internal/Palace/Wonder/unknown exclusion.
- ACTIVE/facts/pillage/building/worker/carrier read UNKNOWN: no writes. Confirmed loss/zero: withdrawal once. Reference disappearance/load: no stale reapplication. Unsupported actualTier5 holds. True relevant events restore.
- Actual combined diagnostic request reaches shadow/Housing/GPP Describe without writes. Existing panel click sends1;10k idle sends0. Native GPP rate remains empire-wide, not city final-rate proof.
- Full B1/P0-A/A–D2 wrapper PASS: B1 retirement12, Copy/Industry lifecycle/stress, Discount direct-event/scaling, Network shared view30k reads, A/B version/output contracts, earlier B069 route suppression. Frozen tests unchanged. Wrapper explicitly adapts version/caption, permits the reviewed B2 byte deltas and supplies old diagnostic fixtures' new read-only dependencies. B2 tests separately execute real combined modules.
- All Lua compile; modinfo107 valid; every non-B2 runtime byte and all tracked Design bytes match845cda1. Data SQL unchanged. Deployment and temporary-playtest safety tests PASS (temporary directories only).

Measured one Housing+GPP update, one specialty district/city, fixture DB161 buildings:

| Cities | Effective fact reads | District reads | Building checks | City visits |
|---:|---:|---:|---:|---:|
|1|2|3|161|2|
|2|4|6|322|4|
|4|8|12|644|8|
|8|16|24|1288|16|

Housing uses one player district index plus per-city local capture; GPP uses its own batch index. These are separate O(C) batches, not one shared cross-writer cache. Building checks scale O(C×catalog size), not repeated national C² scans. Actual DB size affects the constant.10k unrelated Publish/Playback/UI/unit/CityBuildingsChanged notifications: added reads/scans/writes0;10k same-turn reconciliation notifications: after first audit added reads/writes0. Carrier callbacks during writes do not recurse. No Network query/request/property writes introduced.

## Runtime writer audit / retained paths

Full-Mod exact-family search: only Lv2Housing/Lv2GPP write these41 families. Gameplay starts each once; actions and LV2_GPP_DIRTY call existing Audit; hidden LV2_*_READ and combined read are Describe only. CityInheritance is still quarantined, not started; no ownership restore enabled. B1 retired support stays inert. Other old III/IV/Network/Standardization writers remain unchanged for their future cutover; this is not full D0035 Gameplay implementation. No claim about55GB memory cause or repair.

## Rollback and minimal native test

Rollback is the complete B079.106 package via existing receipt/restore contract, not mixed files. No new save schema; carrier projections recompute on load/events. This does not promise arbitrary develop saves are stable-compatible. Deployment follows W0003 only after clean commit/push, game-exit inspection and whole-package backup/hash. Actual deployment recorded separately in Status.

One prepared current-Identity ACTIVE>=II city: use existing `基础设施 / Lv2住房与专家` button. Check housing expected/carrier matches1+distinct eligible tiers in specialty anchor; move working specialists0→1→2 and read base GPP0→2→4 for that profession (Culture each of three classes). Compare native city housing and Great People rate while holding other sources fixed; empire rate can include other cities and native modifiers. If an existing governor change is convenient, ACTIVE1 withdraw/restore is optional. Do not force pillage via disasters/AI; local simulation covers it, native pillage event timing remains unconfirmed. No need to create four separate test games.

P0-B2 LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Next recommended work after review: P0-C planning/authorization, not automatic implementation. Stop.
