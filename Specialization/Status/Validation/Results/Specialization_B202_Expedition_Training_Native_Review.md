# B202 — normal-training acceptance and panel-dependent name confirmation

Build B202.229 / modinfo229. Review date 2026-10-11. Four original screenshots inspected; unchanged originals moved with SHA256 verification to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B202/2026-10-11/`. No screenshots enter Git.

## Native evidence

| Image | Observed facts | Evidence boundary |
|---|---|---|
| 1, 10.30.02 AM, T89 | Newly trained team selected at home; 派遣到新城市 tooltip says currently unavailable; unit panel shows 待分配. | Explicit action availability FAIL, not merely optional selection auto-opening. Exact Gate phase/error before opening diagnostics is not captured. |
| 2, 10.30.09 AM, T89 | P0 report shows restored generation2, name 西蒙 confirmed, team1/1, unit3407901, source Edinburgh (Test), city393220, source MATCH; dispatch button available. | User explicitly reports opening P0 alone restores functionality, without clicking any diagnostic action. Source binding exists after confirmation; no evidence that the source record was lost. |
| 3–4, 10.33.22/24 AM, T93 | Same name/source, created3407901→current3473437 at (3,27), source MATCH; task T91→T93, completion1/1, no reward; activity released; Gain Sources0→0, native operation-1, native completion events0. | Scoped arrival identity/source continuity and independent two-turn no-reward completion/release PASS after panel-assisted recovery. No general immunity or all-lifecycle claim. |

User reports everything else works. Retain that as scoped USER_REPORTED_PASS for the submitted flow. The screenshots show restored state but do not independently show the queued save boundary, cost progression or second-city queue rejection. END is not shown. Do not demand repeats of inherited lifecycle tests or expand this to full N1 completion. The diagnostic string “免费原型，不是正式训练” remains stale for normally trained teams; it does not establish how this unit was obtained.

## Bounded source trace — STATIC_CONFIRMED

- [Training finish](../../../../Mod/ExpeditionSpyGate.lua): exact queue/completion/birth receipts save source and unit, enter NAMING, and publish the scalar transition. NAME later independently validates the native name and allows CREATED controls. These are separate stages; unavailable dispatch alone does not prove missing source binding.
- [Background confirmation](../../../../Mod/UI/ExpeditionTrainingName.lua): publish/load pulses start a ten-second observer only for NAMING with trainingToken. `stop(reason)` sets `finished=teamKey` for success, timeout, invalid read and transition interruption. `pulse()` rejects that same finished key permanently for the session. Therefore a transient unsuccessful attempt cannot resume merely because native name readiness later improves. Error is stored in an ExposedMembers field, not surfaced in the normal player report.
- [Diagnostic window](../../../../Mod/UI/ExpeditionSpyWindow.lua): opening calls READ; a NAMING reply invokes prepareName, then NativeName and NAME automatically. No diagnostic button click is necessary. This is a real side effect of opening the panel, consistent with the reported recovery.
- [Unit action eligibility](../../../../Mod/ExpeditionSpyUI.lua) allows TRAVEL only for CREATED/ARRIVED. The diagnostic path can therefore unlock dispatch by completing confirmation; it is not simply repainting a disabled button.

The specific native trigger remains UNKNOWN: timeout/readiness, missed event/update delivery, request availability or another failure. No pre-open error or current Lua log was available at the inspected standard log locations. Do not claim a timeout was observed. Existing B202 local tests model immediate readiness or intentionally terminal timeout; they do not prove recovery after late readiness. An attempted additional in-memory counterexample was NOT_RUN: Lupa lua55 was unavailable in the current Python environment and the previously documented temporary dependency location. No package installation or test/source edits were made;437 prior local PASS remain historical local evidence, not invalidated or upgraded.

## Proposed narrow repair — NOT_IMPLEMENTED / awaiting approval

1. Give the independent background observer explicit pending/success/terminal states; only confirmed successful NAME completion is success. Permit bounded event-driven retry of transient native readiness at appropriate local-player/publish/selection boundaries, with exact team/unit/source identity checks and a finite retry budget. No permanent polling, per-city scan or blind request replay.
2. Preserve permanent capacity/source authority and existing independent NAME validator. Expose a concise pending/error reason on the ordinary action path, including last attempt result; keep detailed diagnostics optional. Check request acknowledgement and context readiness, not just the ten-second timer.
3. Make P0 opening read-only for normal-training name completion once background ownership is established; retain any explicitly required legacy prototype creation behavior separately. Fix the stale free-prototype wording for trained teams.
4. Add targeted actual-Lua tests for delayed name readiness, event ordering, timeout/recovery, acknowledgement ambiguity, duplicate callbacks, cold-loaded NAMING and panel-independent action enablement. Recover the existing compatible local test environment before claiming these checks.
5. One native delta check: train a fresh team without opening P0, use 派遣到新城市 directly and verify source retained on arrival. No repeated unchanged queued-save/travel/task campaign unless the repair changes those paths. Optional auto-opening remains non-blocking; explicit buttons must work.

No gameplay/Design/Store schema/capacity/binding/travel/task duration change proposed. No implementation, runtime replacement, game launch or new native test performed during this review.
