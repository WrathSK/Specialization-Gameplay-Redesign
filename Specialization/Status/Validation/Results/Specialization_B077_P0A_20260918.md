# B077.104 P0-A native read failure / idle sound observation

Evidence: USER_GAME_TEST_FAIL for District Completeness capture only. P0-A LOCAL_SIMULATION_PASS remains historical local evidence, not engine PASS. Source/runtime B077.104/modinfo104; no source fix or deployment in this investigation.

## Screenshots and native evidence

Two reviewed screenshots: 2026-09-18 18:03:53 and18:05:18, Turn1 Stirling(TEST). User identifies first as Campus only, second as Library+University. Both display P0-B-077.104 and D validity UNKNOWN / TEMPORARILY_UNAVAILABLE / revision nil, with `DistrictCompleteness.lua:67: function expected instead of nil`. Capture fails at `for _,d in districts:Members() do` after city:GetDistricts(), before building enumeration. This proves the native iteration assumption does not hold in this Gameplay context; whether the unavailable function is Members itself or the returned iterator needs native/API confirmation. Not a tier mapping, cache staleness or D=0 result.

Local fixture test_p0_a.py line32 manufactures City.GetDistricts().Members(), so local success did not validate this engine contract. Existing RuntimeWork/older effect readers use player district enumeration filtered to city; candidate repair must verify context/iterator and preserve one bounded index, not reintroduce per-city national scans. Do not change Design or interpret failure as empty.

Both screenshots show Research Potential4 / ACTIVE1, facts VERIFIED, ACTIVE status KNOWN. Badge科研4级 represents Potential. INACTIVE shadow is independently expected at ACTIVE1; future IV shadow test needs established governor eligibility, while D reading should work regardless ACTIVE4. First/second images are not proof IV was enabled.

Current City_BuildQueue.csv independently records Campus, Library and University completions at Turn1. It contains12 rows after header, not evidence of continuing carrier writes. No Lua.log available in current Logs. UserInterface.log ends ForgeUI shutting down; current files are not a live Lua trace. UIWarnings includes repeated layout warnings (including production panel) without enough timestamp/counter evidence to link them to sound; do not label those memory/event root cause.

## Separate idle sound incident

User reports very frequent refresh sounds while no actions, no visible refresh flashes and no observed memory growth. Sound source UNKNOWN. No counter pair, sound trace or Lua dispatch trace supplied. Absence of memory growth does not prove no event storm; sound alone does not prove Building churn.

Static P0-A capture: only explicit COMPLETENESS_READ; direct events mark at most8 cached entries dirty; no automatic capture timer, effect/Property write or auto retry. Gameplay handler returns before unrelated dispatch. P0Panel response timer checks the ACK, not resends COMPLETENESS_READ. Thus a perpetual P0-A auto-read/write loop is not supported by current source evidence; unrelated old modules/other Mods/native audio remain unassigned, not exonerated.

Read Performance Counters is currently a local UI read (SPCPerformance.Describe(false)), no Gameplay Request/full-city scan. If sound recurs in a future authorized test, one counter pair30seconds apart can separate scans/writes/send activity; no need to restart now or move units/end turns. User could not determine sound/diagnostic chronology and plans to establish a governor to activate Research IV. Explained that ACTIVE4 does not repair the district iterator failure; if sound recurs, capture counters twice30seconds apart, no repeated building tests. No speculative sound fix.

## Evidence archive / integrity

Original screenshots read then moved with before/after SHA256 validation to external `Specialization/Status/Validation/Evidence/B077_P0A_20260918/` under game-support workspace. Six relevant logs copied (originals untouched): City_BuildQueue.csv, UserInterface.log, UIWarnings.csv, GameCore.log, Modding.log, Database.log. manifest.json holds hashes/provenance. No bulk log folder upload or configuration edits.

B077 deployment receipt is external `SpecializationDeploymentBackups/B077.104-901e552-playtest.json`;125 runtime files matched source digest4b868bb8feed5486903c36298efe8ed73cccc9c0859d979290934dcca1c8a630. Previous B076 complete backup remains verified. main remains B069.96. No P0-B1 implementation.

Next: fix native P0-A district capture with contract-realistic mocks and scoped API evidence; investigate sound separately using user chronology/counters. Do not claim either issue fixed or deploy without authorization. User need not repeat failed building/repair tests yet.
