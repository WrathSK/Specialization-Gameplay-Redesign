# B221 — Reconnect-readable Expedition activity diagnostics

State: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. B221.248/modinfo248. Diagnostic-only authorization; no functional repair or root-cause closure.

## B220 evidence and remaining distinction

User reports that normal missions fail after B220. Existing collector session `session-20261017T131726Z-3859d9` records ARRIVED and idle-action signatures, then LOCKED. The socket disconnected before the lock and reconnected afterwards; no TASK failure/activity record was captured. An empty collector alert list is not gameplay PASS. The all-false idle signature also collapses denied permissions and reader exceptions; it cannot prove native denial.

The B220 removal of mission-site placement is a plausible trigger, not a demonstrated cause. Historical [B194 native evidence](Specialization_B194_Expedition_Pending_Activity_Native_Review.md) already covers a successful AWAKE → SLEEP → task completion/release path without a task placement call. Actual B219/B220 Gate/bridge local comparison reproduces failure in both versions when SLEEP is denied or pre-request activity is OPERATION; only an explicitly hypothetical placement-normalizes-activity model separates them. This is not evidence that native PlaceUnit actually performs that normalization. Existing integration fixtures default to an eligible AWAKE unit and therefore do not settle this native question.

## Narrow implementation

- Reuse `ExpeditionTrainingDiagnostics` schema205 ring (64 entries, existing 96-record per-context budget). Add one ACTIVITY_UI producer; fixed ACTIVITY_START and ACTIVITY_FAILURE labels. The existing fixed reader and collector recover these records as ordinary ENTRY snapshots after reconnect. No collector command, API surface or independent history system added.
- Startup records preserve activity/enums, readiness, SLEEP eligibility and UNKNOWN reader status from the existing diagnostic reads. Failure records preserve the actual guard result (ALLOWED / DENIED / UNKNOWN_VALUE / READ_ERROR / NOT_QUERIED), safe error category, phase/key, current-read status, last successful activity and sample turn, coordinates, requested/attempted flags. They do not relabel a prior sample as a fresh native read. Unexpected-state failure before the guard is explicitly NOT_QUERIED; correlate with the separately labelled startup observation.
- Capture before the existing failure acknowledgement; diagnostic exceptions cannot suppress it. Existing sampling/writer counts and decision branches are retained. No extra eligibility query at failure, no native-state normalization, movement, wake, retry, timer or frame subscription added. The pre-existing B194 post-request activity watcher is unchanged, not introduced by B221.
- Records remain scalar, bounded and nonpersistent. No names, arbitrary native error text, paths or tokens are added to the trace. Context identity, load sequence and activity keys distinguish sessions/attempts. Shared ring retention is finite: reconnect within retained entries is recoverable, not an unlimited audit log; saturation remains explicit in META suppressed/errors.
- Capacity, city binding, training, saved schema, Insights, Tourism, GC and ordinary Spies unchanged. Diagnostic UI globals may still be cleared by normal lifecycle; retained ring records do not authorize any task.

## Local validation

307 targeted tests PASS: activity trace (9 new), activity UI/diagnostic/pending/failure/integration, task, persistence, existing training diagnostics, fixed trace reader and collector, plus 31 current package/Gate checks with the configured DB opened read-only. Actual Lua executed through Lupa; transport and native APIs are fixtures, no live socket or game call. New tests distinguish denial from reader error, pre-request OPERATION from owned pending timeout, unavailable activity, unchanged successful writer/ACK counts, capture failure isolation, bounded retention and snapshot recovery after the transient activity view is cleared.

Initial invocations failed due to an incorrect working directory and restricted temporary fixture writes; the corrected run with the existing local-fixture permission passed. No assertions were relaxed. Context/schema/hash and selector self-test PASS (224 runtime files / 671 guarded files); 13 current links/anchors PASS; diff review/check PASS; local evidence is not native task acceptance.

## One diagnostic test

Start the existing manual collector. With a healthy ARRIVED team and an available mission, click 开始任务 once. If it fails, stop there and leave the game/collector connected briefly so its ordinary reconnect/snapshot can finish; no repeated attempts, P0 report, save/reload or screenshots required. If it starts, allow the existing task to complete normally. The log distinguishes pre-request activity rejection, actual SLEEP denial/reader exception and owned post-request pending timeout. This is collection of the missing distinction, not a claim that B221 repairs missions.

User decision: no new decision required. User testing: one attempt after verified deployment. Primary next: attribute the failure from the paired records and propose a narrow event-based repair; no automatic next batch.

## Deployment

Source locally validated. Live remains B220 until a separately verified guarded deployment; no native PASS claimed.
