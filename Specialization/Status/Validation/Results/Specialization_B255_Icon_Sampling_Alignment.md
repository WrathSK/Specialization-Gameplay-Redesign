# B255 — Icon sampling and banner alignment

## Approved scope

The user approved the two-item follow-up to B254: explicitly sample the existing64px institution atlas without enlarging institution rows; reduce the map badge from40 to32 layout units and align its four status segments with the native city-name banner bottom. No artwork, gameplay, state publication, event or timer changes. Development Investment sidebar feedback and all held work remain pending.

## B254 native evidence

USER_GAME_TEST_PASS (user report only): map emblems follow map zoom, ordinary banner selection works, and the main ACTIVE numeral updates after governor relocation. Four-segment dynamic updates are explicitly pending for the combined B255 check. User feedback: the map emblem is too large/low; institution icons before city-panel names look soft.

Two original3840x2160 screenshots and the SHA256 review manifest are archived under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B254/`. Original bytes remain frozen. The institution outline occupies approximately50x53 physical pixels while its control uses32x32 layout units. Existing atlases contain32px and64px cells, uncompressed BGRA8; compression is not the cause. B254 institution SetIcon did not explicitly select a size. Upsampling is a plausible contributor; the native automatic atlas choice and exact display-scale/filtering chain were not traced. This evidence does not prove a specific OS DPI defect.

## Implementation and source of truth

Institution icons explicitly select64px, then restore32x32 layout size. Existing SVG/DDS bytes, serif proportions, opacity, colors, row spacing and ability text remain unchanged.

Map badge rendering is32x32 with the same64px atlas. Its root is32x37, anchored outside-left and inside-bottom (`L,B` / `O,I`) to the existing native banner container. Four6x4 segments at y33 terminate at y37 exactly, with dark4x2 interiors retaining the filled/outlined/dim distinction. Native Expansion2 `CityBannerInstances.xml` defines the city-name button/frame as parent-sized under the41-high container. Bottom anchoring therefore follows that frame rather than vertically centering the formerly46-high emblem. Exact visible texture-edge alignment remains a native visual check.

Canonical facts, disposable projection, callback chaining, tooltip and child lifetime are unchanged. No new persistent fields, gameplay commands, timer/frame updates or collision system.

## Local validation

LOCAL_SIMULATION_PASS:32 selected existing methods. Updated UI assertions verify64px sampling with32x32 controls; XML geometry verifies all segments terminate at the root bottom and remain within its width. Existing segment mapping, update/lifetime, UNKNOWN handling, institution summary and read-only canonical-state checks pass. Both DDS hashes and package closure remain verified. No native crispness or alignment PASS is inferred from these checks.

## Minimal native check

1. Open **城市详情 → 专业机构** at the usual display setting. Compare I–IV sharpness, especially III/IV, and confirm the row/icon size is unchanged.
2. Inspect the map emblem: smaller main badge, four-segment bottom aligned to the city-name flag. Normal banner clicking and map zoom should remain usable.
3. During one convenient governor relocation/return, compare the main numeral and four segments with current ACTIVE/Potential. This completes the held four-segment dynamic check; no new gameplay or save/load retest is requested.

## Publication and deployment

B255.282/modinfo282 DEVELOP_ACTIVE; source `6e64d96831978049b98726bbe463133a8e9fc0ca`; receipt `B255.282-6e64d96-playtest.json`;277/277 MATCH; digest `f3ee4d3a7864a52a1b6bc253f44ad7890edf5572185ae75b5f33b2fce49f63bb`. Fresh game-exit checks, exact B254 restoration and B255 activation passed. Stable and outgoing B254 recovery verified; no pending marker, game launch, configuration or main change.

13 batch-owned files passed the ordinary staged publication gate.32 selected local methods and277-runtime/890-guarded-file context checks PASS. No binary changes or new publication exception. Native visual/segment acceptance remains pending. Stop at this batch boundary.
