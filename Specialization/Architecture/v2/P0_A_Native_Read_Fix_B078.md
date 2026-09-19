# P0-A native Gameplay read repair — B078.105

Owner: Codex. Contract: A0161, Design D0032 unchanged. Source base: eb8f2a1 (B077.104).
State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Not deployed. No P0-B1.

## Finding and repair

User B077 screenshots show DistrictCompleteness.lua:67 failing before buildings are read. Gameplay city:GetDistricts() does not supply the UI-shaped Members API assumed by P0-A and its initial mocks. ACTIVE1 is a separate observation: D must still read; only the Research IV shadow is inactive. A governor cannot repair the failed native call.

Read-only installed HD evidence, Workshop 2465378070:
- Gameplay/RegionalYields.lua:155–161: city-local GetNumDistricts + zero-based GetDistrictByIndex, district IsComplete/IsPillaged.
- Gameplay/RegionalYields.lua:64–65: HasBuilding / IsPillaged / GetBuildingLocation for existing buildings.
- UI/Replacement/CitySupport.lua uses Members/GetBuildingsAtLocation in UI context. Its presence did not establish Gameplay availability; this was the initial evidence/mocking error.

DistrictCompleteness now enumerates only the selected city's indexed districts; one GameInfo.Buildings catalog pass checks existing buildings and groups their native locations into those districts. No player-wide enumeration, per-district catalog pass, new event listener, requests or writes. Known ordinary buildings with unresolved positions reject the whole sample and retain last verified facts; incomplete district entries likewise reject. Non-ordinary objects off district plots or without a valid location remain explained exclusions. Current queued unfinished buildings remain zero-contribution diagnostics. Unknown/ordinary classification and all D rules are unchanged.

The native fixture deliberately has neither CityDistricts.Members nor GetBuildingsAtLocation. Executing B077's actual module with that fixture reproduces UNKNOWN; the repaired actual module reads Library+University as D3. This is stronger local evidence, still not an engine test. Diagnostic errors now distinguish no verified sample from a retained previous sample.

## Local results

- D0/1/3/6/10, cap13→10, same-tier sum, missing lower tiers, unique/free/pillaged/unfinished buildings, highest single district: PASS.
- ACTIVE1 still reads D3; Research IV D3×6 specialists = shadow18, D10×5=50, applied0. ACTIVE below4 stays INACTIVE; no new carrier.
- Native mock: indexed districts, location grouping; missing district entry, unknown ordinary location held; off-district Wonder and unlocated internal carrier excluded: PASS.
- 10,000 cached successful reads: no native reads/revision changes/writes. 10,000 unrelated pulses: zero capture/send/write; 10,000 direct dirty events: zero immediate reads, one capture on next explicit read.
- 1/2/4/8 queried cities: captures1/2/4/8; district reads1/2/4/8; building checks120/240/480/960 with 120-row fixture. B077 counted only returned building entries; B078 counts all HasBuilding checks honestly. Cost O(C×B + total districts), B = fixed loaded database catalog size, not C². Only explicit dirty/first-turn reads pay this cost; idle cost unchanged.
- Duplicate snapshots, temporary failure hold, bounded retry, confirmed removal, missed-event next-turn read, reference change/load epoch, cache≤8: PASS.
- Actual Gameplay dispatch + P0Panel click once/send once, 10,000 idle UI events no resend: PASS.
- A/B/C1/D1/C2/D2 composite regression, 1,728 normal carrier-map comparisons, 30,000 shared Network queries, 3 actual UI timers×10,000 callbacks: PASS. Fault-injection errors are expected; normal scenarios retain no-hidden-error assertions.
- All Lua compile, manifest105 references, old effect writers/Data byte equality; deployment safety suites in temporary directories: PASS.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_p0_a.py --regression`; deployment suites `test_deployment.py`, `test_temporary_playtest.py`. Lupa path is local tooling only.

## Idle sound investigation — unresolved

User reports very frequent idle refresh sounds, no observed flashes/memory growth. Archived B077 evidence has no Lua.log or before/after counters; City_BuildQueue has ordinary construction rows, not evidence of carrier churn. UI layout warnings cannot establish the sound source.

P0-A capture is reachable through explicit COMPLETENESS_READ; native failure has no background retry. Its dirty callbacks only mark at most8 cached entries. P0Panel waits for acknowledgement without resending this action. Existing CityPotential's 0.5-second UI callback checks selected-city/turn/write revision and only sends when dirty; D2's actual timer tests remain zero-send while unchanged. No direct PlaySound call exists in these P0-A paths. These observations do not exclude runtime engine/other-mod/old-writer activity; do not claim the sound fixed or harmless.

No speculative old writer changes, event suppression, logging expansion or gameplay OFF experiment added. Unified next user test should capture existing read-only Performance Counters before/after a short idle interval only if sound recurs. Actual sounds/engine behavior cannot be proved by mocks.

## Unified minimal acceptance (after separately authorized deployment)

1. Confirm P0-B-078.105 in diagnostic report. In the same city read Campus alone D0, then Library+University D3 with Tier1/2 and contribution1/2. Existing prepared cities may skip the empty stage.
2. If Research ACTIVE4 is established, verify shadow D×working Campus specialists, applied0. ACTIVE<4 is valid for D testing; no need to promote merely to fix reading.
3. Same city pillage University/read, repair/read: D3→1→3. Report UNKNOWN text if any; no repeated attempts needed.
4. If idle sound recurs, record Counters once, close diagnostic, idle about20 seconds, read again, note whether closing stopped sound. No extra unit moves, turns, reloads or long session for sound testing. Do not claim this routine will repair the sound.

Implementation repair PASS locally, native acceptance still pending; B077 USER_GAME_TEST_FAIL remains historical evidence. No claim about 55GB incident. Main B069.96 and live B077.104 stay unchanged. Stop; neither deployment nor P0-B1 authorized by this repair.
