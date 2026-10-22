# B256 — Restore complete icons at matched sizes

## Approved scope

The user authorized the narrow B255 regression repair: use the existing32px atlas with32x32 controls for institution and map icons. Preserve B255 bottom anchoring, four-segment geometry and all event-driven state behavior. No art, gameplay, timer or unrelated sidebar changes.

## Native evidence and cause

**USER_GAME_TEST_FAIL:** the B255 screenshot shows enlarged, clipped hexagons/numerals in both institution rows and map emblems. The original screenshot and SHA256 review manifest are archived under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B255/`. B254 zoom/click/main-ACTIVE acceptance remains scoped; four-segment dynamics remain untested.

B255 selected64px atlas cells and then called SetSizeVal(32,32). The screenshot contradicts the assumption that this resamples the complete icon. The corrective boundary is to match the selected cell size to the control size. Exact native UV/filter internals are not asserted. Previous local UI mocks recorded calls but did not reproduce native raster sampling, so their PASS did not establish native visual correctness. B255's frozen report is retained; this record supersedes its pending visual status with the observed failure.

## Implementation and validation

Only the two SetIcon size arguments change from64 to32, with a corrected explanatory comment and build stamps. The existing32px DDS is used unchanged; all SVG/DDS bytes and XML layout remain unchanged. High-resolution sampling research is deferred; this repair promises correct size/complete artwork, not a new sharpness improvement.

**LOCAL_SIMULATION_PASS:**32 selected existing methods, including matching32px selection/control dimensions, unchanged bottom/segment geometry, atlas hashes, package closure, event/lifetime and institution regressions. These are source/local checks, not a raster-engine simulation or native PASS.

## Minimal native check

Open **城市详情 → 专业机构** and inspect one map emblem. I–IV and hexagonal outlines should be complete, with normal institution size and the smaller bottom-aligned map badge. Stop if clipping remains. Once appearance is normal, the held four-segment update check may be combined with a convenient governor change; no additional gameplay/save/load test is requested.

## Publication and deployment

B256.283/modinfo283 DEVELOP_ACTIVE; source `3259a50e982a2e8349e8a00ba936f8319a97fd6a`; receipt `B256.283-3259a50-playtest.json`;277/277 MATCH; digest `6f4ade5802d1f80d2c88208e1afbaac40f898e162d52ab64d4d4a754aeb3a688`. Fresh game-exit checks, exact B255 restoration and B256 activation passed. Stable and outgoing recovery verified; no pending marker, main/configuration change or game launch.

11 batch-owned files passed the ordinary publication gate;32 local methods and277-runtime/891-guarded context checks PASS. Main/stable B069.96 and held work unchanged. Native complete-icon/size confirmation remains pending.
