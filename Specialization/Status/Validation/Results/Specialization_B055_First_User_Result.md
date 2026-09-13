# B055 first screenshot verification — 2026-09-13

Document Owner: Codex
Runtime: P0-B-055.72 / modinfo72 (unchanged)
Evidence: 8 user screenshots, chronological order; user operation descriptions
Conclusion: PARTIAL_EVIDENCE / USER_GAME_TEST_REQUIRED for exact boost and clean GW comparison

## Confirmed basis

STATIC_CONFIRMED means local code/database evidence, not native runtime pass. Read-only DebugGameplay.sqlite shows Boost=34 for the tested known tech/civic rows. HD UpdateDataBase/DL_Boosts.sql:288 executes `update Boosts set Boost = 34 where Boost = 40;`. Thus this loaded ruleset uses34 rather than unconditionally40. It is a configured base, not a promise that measured progress/cost equals34 after all engine processing.

## Boost transcription and arithmetic

All listed initial progress=0. Image3 retains history/Buttress from image2; they must not be counted again at the new level. N1/2 and configuration L1/2/4 are visible; L3 not supplied. User reports same-turn culture upgrade then Vaults trigger, Research governor downgrade then Humanism trigger.

| Image | Target | Current cost | Configured extra pp | Observed delta | Observed ratio | cost×(34+extra)% | cost×(34+floor(extra))% |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 封建主义 | 780 | 1.100000 | 269 | 34.487179% | 273.780000 | 273.000000 |
| 1 | 砌砖 | 80 | 1.100000 | 27 | 33.750000% | 28.080000 | 28.000000 |
| 2 | 历史记录 | 312 | 3.111270 | 114 | 36.538462% | 115.787162 | 115.440000 |
| 2 | 扶壁 | 600 | 3.111270 | 221 | 36.833333% | 222.667619 | 222.000000 |
| 3 | 拱券 | 600 | 6.363961 | 239 | 39.833333% | 242.183766 | 240.000000 |
| 4 | 人文主义 | 1440 | 1.555635 | 498 | 34.583333% | 512.001143 | 504.000000 |

Two600-cost technologies show239−221=18=600×3%, consistent with integer3→6 extra rather than full3.252691pp change. This supports effectiveness/change direction and truncation hypothesis, but different technologies are not a same-target controlled experiment. Exact additive formula is not established: even floor(extra) then floor(progress) does not explain all6 rows (Humanism504 predicted vs498 observed). Do not describe the discrepancy as entirely accepted truncation or silently compensate. No pre-emptive rounding fix; retain D0017 and current test weights. A later same-target saved-state control/native detailed observation is more informative than repeating unrelated targets. No game/source edits this review.

Observed source-level/N/configuration changes are USER_GAME_TEST_PASS for the pictured state transitions only. Actual higher/lower boost trend has user evidence; full exact numerical contract remains USER_GAME_TEST_REQUIRED. No claim of B055 reload, complete disconnect, all4 tiers or B055-4 pass.

## Great Work transcription

All4 screenshots: city327684, one qualifying Writing, Metamorphoses/ERA_CLASSICAL, Tourism3. User specifiesCultureIV, one specialist (+5%Culture), amenities0, amphitheater only, no policies.

| Image | Mode | Work Culture | Report city Culture | City bar Culture (rounded) |
|---|---|---:|---:|---:|
| 5 | OFF | 4 | 19.1055 | 14.9 |
| 6 | OBJECT | 4 | 19.1055 | 19.1 |
| 7 | CITY | 2 | 19.1055 | 17 |
| 8 | OFF | 2 | 17.0078 | 17 |

19.1055−17.0078=2.0977, near2×1.05=2.1; small remainder alone is not a reason to alter design. However, first/finalOFF differ in workCulture4→2 and reported city19.1055→17.0078. OBJECT does not increase reported workCulture relative to firstOFF; CITY changes workCulture and report differs from city bar. Consequently these are not clean synchronized before/after controls. Possible refresh timing or native modifier removal interaction remains a hypothesis, not confirmed cause. Do not mark B055-3 fullyPASS or claim native object+city semantics decided. Work count/type and constantTourism3 are directly observed, not all Tourism/theming interactions tested.

Small next test, only if continuing validation: stable OFF after one turn/read; OBJECT after one turn/read; CITY after one turn/read; endOFF for cleanup. Keep works/expert/governor/policy/population stable. No need repeat setup or more than3 report images. Boost needs no immediate repeated unrelated sample; first prepare a same-target control if further exactness is required.

## Evidence archive / scope

8 originals moved only after visual reading; before/afterSHA256 matched. External legacy workspace `Specialization/Status/Validation/Evidence/B055-FirstResults/manifest.json` contains ordered filenames and hashes; no duplicate PNG imported to Git repository. Historical/source/design/runtime unmodified. Status updated to reflect partial results, not blanketPASS.
