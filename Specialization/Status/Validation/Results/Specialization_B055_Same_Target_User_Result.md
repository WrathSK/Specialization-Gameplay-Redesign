# B055 同目标T1/T2/T3结果

Document Owner: Codex
Runtime: P0-B-055.72 / modinfo72 (unchanged)
Design: D0017 (unchanged)
Evidence: 3 user screenshots, user identifies order T1/T2/T3; all turn12
Status: USER_GAME_TEST_PASS for tested automatic boost / downgrade / recipient increase with accepted native fractional loss

USER_GAME_TEST_PASS是用户实际游戏证据，限本次同目标场景，不代表闭源引擎所有数值步骤已还原。

## Transcription

All6 initial progress=0. Law cost2160; Cartography cost600. Both target identities and current costs fixed across branches. UI READY and network setup exactly matches plan. T2/T3 follow the supplied reload-common-save procedure per user test labels; no separate video proof of load sequence.

| Branch | Research L/N/config pp | Culture L/N/config pp | 法学delta | 测绘学delta |
|---|---|---|---:|---:|
| T1 | 2 / 2 / 3.1112698372208 | 4 / 2 / 6.3639610306789 | 790 | 239 |
| T2 | 1 / 2 / 1.5556349186104 | 1 / 2 / 1.5556349186104 | 747 | 209 |
| T3 | 2 / 3 / 3.8105117766515 | 4 / 3 / 7.7942286340599 | 790 | 245 |

## Difference test

| Comparison | Observed | Full floating pp candidate | Integer pp first candidate |
|---|---:|---:|---:|
| Law T3−T1 | 0 | about15.1036 | (3−3)×21.6=0 |
| Cartography T3−T1 | 6 | about8.5816 | (7−6)×6=6 |
| Law T1−T2 | 43 | about33.6017 | (3−1)×21.6=43.2 before final quantization |
| Cartography T1−T2 | 30 | about28.8500 | (6−1)×6=30 |

Strong native evidence supports loss of fractional extra percentage points before multiplying by cost for this path/range. Example3.111… and3.810… yield identical Law790 despite cost2160, so merely floor after calculating full extra progress cannot explain the plateau. Positive floor/truncation are indistinguishable here; no claim about negative amounts or exact engine parser implementation. Ordinary nearest-integer percentage rounding is not supported by3.810… behaving as3.

Per D0017/user direction, accept this native fractional loss, do not compensate, rescale, recursively grant or modify progress. Internal sqrt strength remains floating. The game-effective extra reward therefore has plateaus even while diagnostic floats rise. Max-source and recipient identity formulas unchanged. Current temporary1.1/2.2/3.3/4.5 profile remains in runtime this review; restore formal1/2/3/4 only in an explicit subsequent development change.

## Absolute baseline remains separate

This does not fully explain why native base progress differs from a naive34%×current cost. Subtracting integer network contribution in Cartography yields the same203 in all3 branches (239−36,209−6,245−42), while600×34%=204. Law residuals790−64.8=725.2 and747−21.6=725.4 likewise are nearly invariant after final progress quantization, but not2160×34%=734.4. These are residuals, not measured zero-network baselines.

Thus the unexplained offset is separate from this network's tested level/N differences; do not label it entirely fractional pp loss, invent a new base percentage, or silently repair it. Exact base-cost/engine accounting can be deferred under current practical-testing preference; no further user test is required for this confirmed fractional-loss decision. Old reports remain frozen and are superseded only on this narrower uncertainty.

## Pass boundaries and archive

Tested automatic configuration after common-save reload, governor downgrade, and new distribution recipient produce corresponding native newBoost changes/plateau; no stale high-level reward in the tested downgrade. Both directions tested. Not all source/recipient lifecycle cases, final completion cap, explicit zero-network baseline, multi-player eligibility, or an independently testedLevel3 native amount.

3 originals archived after reading with matchingSHA256 under external legacy workspaceSpecialization/Status/Validation/Evidence/B055-SameTarget; manifest maps T1/T2/T3. Only this report andStatus changed. No source/Design/Architecture/deployment changes, no game launch, no Git commit/push.
