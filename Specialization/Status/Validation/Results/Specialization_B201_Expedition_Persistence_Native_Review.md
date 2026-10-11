# B201 — persistence evidence and selection-opening failure

Build: **B201.228 / modinfo228**. Review date: 2026-10-11. Three original screenshots were individually inspected; the user confirms images 2/3 were taken after restarting the game. This is a scoped native review, not formal N1 completion.

## Evidence

Originals are outside Git at `local/legacy-workspace/Specialization/Status/Validation/Evidence/B201/2026-10-11/`, with unchanged filenames and a SHA256 manifest.

| Image | Observed facts | Supported conclusion |
|---|---|---|
| 1 — 8.51.55 AM, T86 | Saved/readback-confirmed generation1; team1/1; source Edinburgh (Test), city393220; native name 艾莉森; unit3276829 at (62,33); source MATCH. | Created team has confirmed durable record and source binding. |
| 2 — 8.54.26 AM, T86, after reboot | Report explicitly says restored from save, generation1; native travel off-map; team1/1; same source/name/ID; destination Tokyo, expected T88. | USER_GAME_TEST_PASS for the tested travelling-save/cold-load identity/source/cap reservation. Off-map coordinates are native travel observations, not evidence of record corruption. |
| 3 — 8.57.05 AM, T90, after reboot | Returned unit3342365 at (3,27), created ID3276829; same name/source MATCH; task T88→T90, completion1/1; activity released; source bonus0→0, native operation-1, native mission completion events0. | USER_GAME_TEST_PASS for this restored travel's arrival/ID replacement and subsequent independent no-reward task completion/release. |

This does not test a cold load *during* an already-running task, every corrupt-record guard, or all ownership transitions. Existing targeted local coverage remains local evidence. END is not shown or separately confirmed in this submission; prior END evidence is not upgraded into a new B201 native result. No normal sidebar/card image establishes B200 layout acceptance.

## Selection-opening failure

**USER_REPORTED_FAIL** at both intended idle points. The user clarifies: immediately after creating the team, selecting it at home did not open relocation; after arrival abroad and before starting the task, selecting it did not open mission selection. P0 diagnostics were opened only for screenshots. This is not explained by selecting a completed one-shot team or intentionally leaving diagnostics open. Persistence success does not imply auto-opening works.

The screenshots do not contain the selection callback arguments, activity/readiness at the failing instant, or the precise predicate that rejected routing. Exact native cause remains **UNKNOWN**.

## Bounded source comparison — STATIC_CONFIRMED

- [Chooser adapter](../../../../Mod/UI/ExpeditionSpyChooser.lua) replaces only the native selection listener and requires `selected == true`, matching event/current unit IDs and an editable selection. Activity/mode/debug callbacks intentionally suppress native UI without retrying our page routing.
- [Routing helper](../../../../Mod/ExpeditionSpyUI.lua) additionally requires current published identity/coordinates, unlocked state, readiness, AWAKE, a resolvable current city, and no open-window marker. Failures return silently, including exceptions inside its protected read.
- Installed Base and BES `EspionageChooser.lua` both call `GoToProperInterfaceMode` on selection **and activity changes**. Their selection handler does not use the selected/editable arguments to gate this call. They still require readiness/AWAKE; therefore this comparison does not establish that those predicates are wrong or safe to remove.
- [Existing local auto-open tests](../../../../DevelopmentTests/test_expedition_spy_auto_open.py) supply stable ready/AWAKE selection facts; a test explicitly preserves suppression-only activity callbacks. They prove that modeled contract, not the native callback timing or runtime predicate values.
- [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) explicitly clears its marker on accepted close. This source behavior does not prove the live marker value during the failed selection.

The selection-only opportunity can be missed when selection precedes readiness/publication; this is a credible event-order hypothesis, **not a confirmed native root cause**. A consistently rejected eligibility/read or callback argument remains possible. Neither warrants weakening identity/source/task ownership checks.

## Proposed next repair boundary — awaiting approval

1. Keep the persistence Store, capacity, binding, native travel, independent task timer/release and one-shot boundary unchanged.
2. Make selection routing observable with one bounded reason/sample for the selected exact team: callback received, current unit identity, published phase/lock, activity/readiness, city lookup and window marker. Display a concise Chinese reason; retain technical detail only on demand. No per-frame trace or growing history.
3. Correct only the demonstrated UI callback/predicate mismatch. If readiness/publication arrives later, retain a bounded selection intent and reevaluate on the relevant readiness/activity/publication signal; retire it on deselection, close, success, task lock or expiry. Never reopen a deliberately closed window or open a task-running/completed team. Do not broadly route every activity event.
4. Targeted local checks: late-ready selection, missing/unreadable facts, stale/deselected unit, manual close, locked/completed task, ordinary Spy passthrough, and unchanged explicit buttons. Do not bypass source/identity protection to make a window appear.
5. One minimal UI session: with P0 closed, select the idle home team → relocation, then select it after arrival abroad → mission page; neither should preselect an option. Include card/header appearance in those same views. No repeated persistence cold-load campaign unless the repair changes a persistence path.

This review implements no repair and requests no unchanged-package retest. No Mod, Design, tests, runtime, main or deployment changes.
