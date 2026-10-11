# B194.221 — bounded post-request OPERATION wait

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** The user approved the narrow repair proposed after [B193 native evidence](Specialization_B193_Expedition_Activity_Native_Review.md). B193 observed OPERATION after our SLEEP request; it did not prove that native Sleep would eventually complete.

## Implemented boundary

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua) now treats ACTIVITY_OPERATION as pending only in SLEEP mode, for this same job with requested=true, owned=true and seen.attempted=true. Each evaluation still validates exact owner/unit/type/name/position and absence of a native espionage mission. Pre-existing OPERATION remains rejected; ASLEEP monitoring and RELEASE behavior are unchanged.

The existing 0.25-second pending poll and 10-second elapsed deadline are retained. Publications do not reset the job deadline. Pending OPERATION sends no additional SLEEP request or eligibility query and never acknowledges ASLEEP. Only an actual SLEEP read uses the existing acknowledgement. [Gameplay Gate](../../../../Mod/ExpeditionSpyGate.lua), unchanged, starts its two-turn/no-reward timer only after that acknowledgement; OPERATION cannot start or advance the timer.

Timeout remains terminal. No forced Wake, native mission, retry or guessed success is added. If Sleep has never been observed, conservative release may remain BLOCKED with ACTIVITY_RELEASE_STATE_UNKNOWN. A possible late native completion after the timeout is not assumed harmless or recovered automatically. The prototype can still fail if OPERATION persists.

## Timeout evidence and state ownership

The bridge replaces a single job-local last-read sample during its existing SLEEP-mode reads: activity, comparison enums, elapsed time and protected current-turn timestamp. It adds no extra unit activity/readiness/eligibility query or event subscription. This small sample lives only as long as the current pending job; it is not a persistent ledger, queue or growing history.

At a SLEEP timeout, the existing bounded failure snapshot records ACTIVITY_SLEEP_TIMEOUT, PENDING_TIMEOUT, request/attempt flags, deadline elapsed/turn and last-read sampledElapsed/sampleTurn. It does not issue a fresh native query. The sample can be slightly older than the deadline and is explicitly labeled that way. Formatting exceptions cannot suppress the original FAILED acknowledgement. Exact identity filtering and END/key/context clearing are retained. Subsequent release failure does not overwrite the original timeout snapshot.

[Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) displays **等待超时诊断**, a last-valid-read activity label and one timing line, above the separate startup sample. Existing immediate guard failures retain their prior diagnostic labels. No new button or XML layout is added. Four bilingual LOC_SPC_EXPEDITION_SPY_ keys: FAILURE_DIAGNOSTIC_TIMEOUT_HEADER, FAILURE_DIAGNOSTIC_PHASE_PENDING_TIMEOUT, FAILURE_DIAGNOSTIC_TIMING and FAILURE_DIAGNOSTIC_TIMEOUT_ACTIVITY. Existing conditional labels remain explicitly checked by package validation.

Capacity, source binding, native name continuity/travel, ordinary Spies, task duration/rewards, permanent state, Design and GC remain unchanged. No change to Mod/ExpeditionSpyGate.lua, task adapter, unit data or persistence; no formal N1/N2/N3/U2 work.

## Local validation

**276 methods PASS** with existing Python/Lupa and configured read-only external DB; SQL checks use in-memory copies. Suites: name_pool4, name39, binding14, task26, gate31, activity18, activity_ui33, activity_integration13, activity_report9, activity_diagnostic21, activity_diagnostic_report9, activity_failure16, activity_failure_report15, activity_pending18; P0 panel layout10. No full gameplay/stress run or game launch.

The 18 new pending tests cover the actual B193 numeric enums, no premature acknowledgement/repeated request or eligibility query, existing timeout, deadline-versus-last-read evidence, diagnostic exceptions, pre-existing/wrong-type activity, native mission and identity changes, duplicate/reentrant events, pending cancellation, late Sleep after stop and bounded cleanup. Actual Gate integration proves taskStart/taskDue remain unset during OPERATION, then one two-turn completion/owned release after observed Sleep; timeout/source loss starts no timer and creates no rewards or persistent writes. Four new presentation tests cover truthful timeout labels and retained primary cause.

Directly superseded B193 post-request fixtures now use a genuinely unsupported third activity instead of OPERATION, preserving the unexpected-state rejection assertions. Frozen B193 results remain untouched. Version/localization package assertions reflect modinfo221. Independent review found no actionable issue and passed 95 focused methods. These are local control-flow results, not native transition/readiness or completion/release proof.

## One minimal completion/release test

After verified B194 deployment, prepare one fresh bound arrived team using the existing fixture controls. If an old team is HELD, use **结束并移除验证团 → ① 创建Spy验证团 → ③ 原生派遣**, or the existing pre-creation save. Fixture setup is not a repeated name/save-load acceptance campaign.

1. On arrival, click **④ 无奖励任务（2回合）** once. Without manually sleeping/waking the unit, allow up to about 10 seconds for preparation. Expect **无奖励任务计时中** and **任务进行中：无需手动待命**. This distinguishes native OPERATION→SLEEP from a persistent operation state.
2. If running, handle unrelated turn blockers normally and advance two turns. The team should not require a manual idle action during the task. Expect **无奖励任务完成** and **任务活动占用已释放**; record the running and completed reports. This tests the newly reachable Sleep→timer→owned release path. No reward should be granted.
3. If any HELD/error occurs, capture the top **等待超时诊断** or failure report and stop; do not manually wake, repeat the request or force the task through. Both the original timeout and a subsequent release error can be relevant.

No save/exit/cold-load/re-enable sequence or unrelated yield checks. Do not claim success solely from OPERATION, the request flags or an allowed eligibility result. Current source/live and deployment receipt are in [Status](../../Specialization_P0_Status.md#current-authoritative-state).
