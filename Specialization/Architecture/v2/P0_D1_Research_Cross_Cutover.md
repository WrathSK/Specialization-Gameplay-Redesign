# P0-D1 — B084.111 Research Cross cutover

Authority: D0035 / Research D0031 RES_L3_CROSS; A0161. User confirmed integer-only result in the tested B083 district modifier path and authorized temporary **floor**, continuing P0-D1. This is an explicit temporary implementation exception, not a Design revision. No D-based formula is implemented. Future consideration of Absolute Infrastructure Depth D is DESIGN_REVIEW_REQUIRED, not an accepted replacement. No P0-D2.

## Evidence and current rule

- USER_GAME_TEST: user reports only integer additions took effect in the recent district experiment; no new screenshot requested. This does not prove every Civ VI modifier truncates fractions. HD per-population decimal policies remain separate evidence.
- B084 formal rule: current Research Identity, Potential>=3, ACTIVE>=3, complete/unpillaged Campus. Sum six BASE adjacency yields across nine eligible other domains, multiply50%, **floor once after the full sum**, project integer Science to Campus district. IV inherits. No population, specialist, D, Gold-share conversion or policy/actual-yield input.
- LOCAL_SIMULATION_PASS and STATIC_CONFIRMED below are not native full-ability PASS. Formal district settlement, BASE-policy separation and save/reload await the compact user test.

## Modules and exact cutover

| Module | Responsibility |
|---|---|
| ResearchCrossModel | Pure nine-domain/six-yield eligibility and floor-after-total |
| ResearchCrossSample | Complete bounded BASE snapshot, current city/district reference, generation/epoch/sequence/turn validation |
| UI/ResearchCrossRefresh | Plot:GetAdjacencyYield producer; independent cross channel; native direct events plus once/local-turn fallback |
| ResearchCross | Sole current Research III writer, current facts and indexed Gameplay city district enumeration; exact old cleanup and idempotent signed integer carriers |
| Data/ResearchCross.sql | 32 internal signed binary carriers, ±1..32768, CITY_DISTRICTS Science effect restricted to Campus/native replacements |
| Lv3Effects + SQL | Remove only Research population branch and8 modifier definitions/arguments/attachments; retain inert8 Building/Type IDs; Culture/Commerce unaffected |
| Gameplay / panel | Startup/sample/read dispatch; explicit Chinese caption, left summary/right composition; no old precision write entry |
| PerformanceCounters | Ten fixed cross lifecycle counters; no new disk log |

B082 three experiment effects also retire; retain inert definitions and explicitly remove their instances. P0-C48 retired effects stay retired. Carrier cleanup completes before new creation. Source overflow abs(floored Science)>=65536 is a visible technical HOLD, not a silent Design cap. Negative encoding is locally tested/schema-supported but negative native settlement is not separately user-confirmed. Nested unknown replacement environments remain subject to catalog/native qualification review.

## Sample and event contract

Reuse unchanged C2 single-flight client; no existing copy/industry payload changes. Ten-field row: city,district,current reference,pillage,six BASE numbers; complete set at most512 rows/160000 bytes. Receiver validates whole sample before replacement. Duplicate signatures do not audit/apply; stale/old turn/epoch/ref packets reject. Temporary unavailable keeps last verified sample and applied result. Current confirmed inactive qualification or Campus loss withdraws even if another sample is missing. Source district completion/pillage/removal filters current facts; unmatched new sample remains HOLD until verified.

One request pending, maximum3 attempts per signature/turn, scalar5-second timeout clock; exhausted budget waits for a new logical input/turn. Load resets generation, samples and pending. No persisted UI/carrier authority. Direct district/plot/feature/resource/governor/research/civic changes mark UI work. Generic Publish/Playback/SystemUpdate only drain marked work or bounded pending state; clean calls stop before city enumeration. No hover requests, no every-second sampling, no Network queries. Scalar timer itself does not scan/send. Once/local-turn reconciliation remains the missed-event safety net. On-demand detail legitimately reads current selected-city facts.

## Local validation

`test_research_cross.py` executes actual Lua producer/receiver/writer and native-schema SQL in a disposable copy of a read-only gameplay database:

- 10000 pending notifications: actual send1, no write before response.
- Accepted sample: apply1; repeated response no apply/write.
- 10000 clean generic notifications +10000 timer callbacks: no extra BASE read, district scan, send or write.
- Changed BASE7: raw3.5 ->3, unchanged integer result no carrier rewrite.
- Temporary native failure preserves result; timeout/throwing transport bounded3 sends.
- Confirmed Campus pillage withdraws once even without a sample; inactive ACTIVE withdraws; repair waits for verified sample.
- Old request/turn/epoch/current city reference cannot overwrite; exact11 retired instance cleanup.
- Nine domains, six yields, unknown/unfinished/pillaged exclusions, unique normalization, III/IV gating, final aggregate floor.
- SQL:8 old Research attachments gone, all other Lv3 database rows identical;32 signed Campus-only new effects; probe inert. All Lua compiles, all manifest files exact, captions/actions and idle verified; Design tree unchanged.

| Cities (Campus+Theater each) | BASE getters | District scans across producer+receiver+writer | City checks | Initial carrier writes | Subsequent10k idle work |
|---:|---:|---:|---:|---:|---:|
|1|6|6|1|2|0|
|2|12|12|2|4|0|
|4|24|24|4|8|0|
|8|48|48|8|16|0|

`test_research_cross_regression.py`: existing P0-C/B2/B1/A and AV2 A/B/C1/D1/C2/D2 suites pass, including protected output matrices. Frozen tests unchanged; explicit adapter excludes only authorized Research III8 old output keys in addition to prior documented P0-C48. Surviving Culture population branch exercises the historic worker/turn test. Independent new SQL/writer checks require Research III retirement rather than merely ignoring output. Historical district experiment tests remain historical and are superseded by formal tests for current startup/SQL.

Deployment and temporary-playtest safety tests PASS. Full physical engine return/settlement/unknown mod environments are not proven by local mocks. This change makes no claim about the55GB incident.

## Diagnostic and minimal user test

Visible button **跨学科研究**: left summary, right per-district composition. Summary example: eligible BASE7;50% raw3.5;floor Campus Science3; configured carrier3;old/probe residual0. Configured is not measured native Science. Existing half-point experiment contamination is warned, not silently disabled.

One Research ACTIVE III city with Campus and two eligible other districts is enough (Cheat allowed). Read summary/details and compare Campus native Science change; verify total BASE then single final floor. Change a relevant adjacency input, or one adjacency policy: BASE-only rule should hold; confirm no repeated sound/writes while idle. Drop ACTIVE belowIII then restore (or existing governor test method), save/reload: withdraw/restore once, no duplicate effect. No manual pillage task required. User need not repeat the0.3/0.5/1 experimental buttons; they are retired.

Exit: implementation/local verification complete; formal USER_GAME_TEST_REQUIRED. Await user result, no automatic P0-D2.
