# B123.150 — native timed-project scoped acceptance

Evidence: USER_GAME_TEST_PASS, explicit user report. No new screenshots supplied or claimed inspected for this acceptance. Existing 112-test LOCAL_SIMULATION_PASS remains separate.

## Accepted observations

- Production queue, city banner and city panel all correctly show one turn.
- After a normal turn, the project completes correctly.
- User reports no production overflow into the following target.
- User additionally tested chopping: it did not complete the project immediately and did not spill production into the following target. This is PASS for that observed chop scenario; injection amount, exact turn/order and target were not supplied. Do not extrapolate to every resource harvest, arbitrary injection, huge forced completion or overflow-mod configuration.

PT012 entry/display/normal-cycle task is closed. Earlier requirements to resolve other turn blockers were tests for the empty-queue/end-turn bypass route, not prerequisites of the current real-project route. Normal game turn blockers retain their normal behavior; no blocker scan/bypass is required for this project.

## Reuse boundary

This real high-cost project plus next-turn native completion and timing display is a validated prototype for a one-turn confirmation project. It does not yet implement identity Claim or award any gameplay reward. Present implementation remains single active city/session-only; load does not resume timing. Formal multi-city scheduling, save/load, interruption and completion reward transactions require their own scoped work and validation.

Current Spec PROG-008 permits either very low production cost or one-turn confirmation. The existing E2 Claim plan proposes the former (Cost=1, normal overflow/chop completion). Reusing this prototype would select the latter and requires an explicit plan update rather than silently treating the old plan as approval. Preserve frozen candidate set, no singleton auto-claim, completion-only Identity/P1 write, other Claim withdrawal, duplicate protection, current ownership validation and persistent readback.

Next recommendation: prepare/review the minimum Claim plan using this proven project primitive; no Claim implementation authorized by this acceptance. No runtime, Design, deployment or main changes.
