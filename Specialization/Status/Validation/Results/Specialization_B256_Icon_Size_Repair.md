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

B256.283/modinfo283 locally verified; live remains B255.282 pending the existing clean-source/game-exit/receipt gates. No binary exception is needed. Main/stable B069.96 and held work remain unchanged.
