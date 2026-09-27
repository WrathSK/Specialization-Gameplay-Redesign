# B109.136 E2 — three-city native evidence

Reviewed 2026-09-27. Runtime visible in all three screenshots: P0-B-109.136. Source checkpoint `2da80ce`; no source/deployment change in this review. Original images visually reviewed, moved with original names to external app-support `Specialization/Status/Validation/Evidence/B109_E2_Three_City_20260927`; manifest.json records bytes/SHA256, 3/3 unchanged.

## Observed results

All images show Turn1 and three registered cities. Each reports normal founding and an independent saved Game record, without reconstructing history from existing districts.

| Original screenshot time | Selected city / reference | Specialization | Potential | ACTIVE | Completed investments |
|---|---|---|---:|---:|---:|
| 16:31:49 | STIRLING (TEST), 0/65536 | Waiting for first eligible completed district | 0 | 0 | 0 |
| 16:31:55 | EDINBURGH (TEST), 0/131073 | RESEARCH | 2 | 1 | 1 |
| 16:32:00 | ABERDEEN (TEST), 0/196610 | CULTURE | 1 | 1 | 0 |

**USER_GAME_TEST_PASS (scoped)**: the submitted native reports show readable, distinct P0/Research P2/Culture P1 records and the expected investment counts. The B108 initialization failure is absent in these reports. Research Potential2 with ACTIVE1 is not itself an error: current activation is distinct from permanent investment. The screenshots do not independently demonstrate a changed-Governor recomputation or every effect's native application. Exact construction event provenance is not inferred from the visible Cheat Panel.

## Input and remaining gate

User confirms E2 reporting uses **left click**, not right click. Current P0Panel binds left click to PROGRESSION_STORE_READ and right click to read-only CITY_SEQUENCE_READ paging. Both the B108 minimal test and visible tooltip already specify left click. No UI correction or right-click retest is needed.

**Coldload confirmation pending:** the three report images alone cannot prove a full exit/restart/load boundary. User has been asked whether they were captured after that step; no repeat test requested while awaiting the answer. Therefore this is not yet closure of the complete three-city persistence checkpoint.

Existing STATIC_CONFIRMED / LOCAL_SIMULATION_PASS evidence remains as recorded in the [B109 repair](../../../Architecture/v2/P0_E2_Plan.md#b109136--start-enabled-initialization-repair). Duplicate notifications, failure/recovery, larger city counts and current-fact rebuilding are not newly certified by these three images. Earlier scoped ownership evidence remains unchanged. First AI-city snapshot/Claim, destruction/location reuse, unassigned recapture and F remain outside this acceptance and unauthorized.

B108's [historical failure](Specialization_B108_E2_Initialization_Failure.md) is preserved. E2 remains partial. No new Design decision, runtime change, deployment or automatic next slice.
