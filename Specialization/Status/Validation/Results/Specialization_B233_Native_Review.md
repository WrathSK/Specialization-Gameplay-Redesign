# B233 native review — Industry history and typed templates accepted

**USER_GAME_TEST_PASS for the tested IND-1 N/E, typed District knowledge and cold-restart restoration.** The user reports no problem in those checks. An adjacent first-turn Industry I specialist-support delay is retained for repair with the next Industry implementation batch; it is not a failure of the new historical records. No implementation or deployment is performed by this review.

## Baseline and retained evidence

Reviewed develop HEAD `f45163c`, implementation source `b82eabf`, source/live **B233.260 / modinfo260**. The prior deployment receipt `B233.260-b82eabf-playtest.json` establishes227/227 equality, digest `0530efdf3e1b3da3f153ed45aac8642a39c9e05a9356c5b12fae6c52eb3662e1`. This review does not repeat deployment verification. Main/stable B069.96 is unchanged. [B233 local result](Specialization_B233_Industry_History_Local.md) remains frozen; its104 offline tests are inherited, not rerun or relabelled as native evidence.

The original collector sessions below remain ignored in `local/diagnostics/B205/`. The B205 trace/directory label identifies the reused collector; B233 attribution uses the user's submission and existing deployment record. No screenshots were delivered for this review.

| Session / original | Bytes | SHA256 |
|---|---:|---|
| session-20261018T035601Z-c28ec3 / records.log | 8202 | dda96790c887bcc5a03e155d45f719ddfd0454ae949af85e79f8dc4ec7697c63 |
| same / events.jsonl | 1105 | 380602b33cbb63bc67760aaa16e772f51c38a7d2082f0f7970a9043ee4593f08 |
| same / summary.txt | 460 | 403dcb4466e8d969ae5d7969fea62bd548b09948a03f9957d64cec8bfaa3fdbc |
| session-20261018T040051Z-88e450 / records.log | 4671 | e7dd10700ae0f53321897b830f4b01ceaadb34911764406633cf7ba2c816ea85 |
| same / events.jsonl | 929 | 7c3a367d39dc8746ad89101b056f5aa61e1176247cfd0621eea25b2ad62f02ce |
| same / summary.txt | 387 | 20929c8bcdb4ebf3d8cbca7fb82c3a3d9b2f60a8ab28477fd339f7ecb87b53b1 |

The sessions contain27/27 and18/18 contiguous scalar sequence records, each with nine observer contexts. They end INTERRUPTED and GAME_EXITED respectively. Reconnect waits occurred; the second session has one `PARTIAL_FRAME_AT_DEADLINE` near shutdown. These transport events do not create a gap in the retained scalar sequences. Snapshot times are retrieval times, not event-latency measurements. Both summaries report no alerts; that is not a blanket gameplay PASS. Raw transport addresses/context identifiers are not republished.

## Native observations

Sequence numbers below are `seq` within each session. Building and District counts are separate knowledge sets, not newly delivered discounts or production effects.

| Session / turn / sequence | Recorded result |
|---|---|
| First, T1,10/14 | History initializes with COMPLETE coverage; city65536 reads N0/E0. |
| First, T1,15–16 | `BUILDING_ORACLE` completion is attributed to supported owner0, city65536 and its own `ERA_ANCIENT`; the next read is N1/E1. |
| First, T1,17–20 | Industry-entry reconciliation unions current Wonders with retained history; N/E stay1/1. Template knowledge initializes at1 building/1 District with FROM_IDENTITY coverage. |
| First, T1,21–27 | District knowledge becomes2; building knowledge grows2→3→4. Final report is4 buildings/2 Districts. |
| Restart, T1,3/13–14 | `INDUSTRY_HISTORY_RESTORED` reads COMPLETE revision3; N/E remain1/1. Template report restores4 buildings/2 Districts, building revision5 and FROM_IDENTITY coverage. |
| Restart, T3,17 | A later District completion commits4 buildings/3 Districts. Collection continues after restoration. |

The user confirms cold restart and correct template records. The new context/session and matching values corroborate that observation; they do not independently prove the operating-system process lifecycle or enumerate every template name. No N/E write, corrupt-history or template-read failure persists in these records. The initial `STD_FACTS_NOT_READY` at first-session13 is followed by successful same-turn initialization, writes and reports.

The first session also reports one early network READ_ERROR at12, without a later network-health record in that session. After restart it is VERIFIED/AVAILABLE, and T2 revalidation returns from pending to AVAILABLE. This is not evidence of a persistent topology failure or a new Culture regression. Because IND-2 will consume topology, its existing initialization/source-change checks must cover a newly created city becoming ready; do not reopen a separate network investigation from this one early record.

This closes only the tested history/template/restart gate. Foreign-completion exclusion, capture N-without-E, additional eras, duplicate/fault injection and other-city isolation retain local evidence; they are not newly claimed native PASS. No repeat B233 test is requested.

## Adjacent Industry I support delay

**USER_GAME_TEST_FAIL, narrow symptom:** on the first turn, Cheat Panel completion of the Industrial Zone established Industry I, but its base specialist support appeared only after ending the turn. User observed the issue; the collector does not record this writer's sample/eligibility/carrier transition, so it cannot determine that exact native callback order.

**STATIC_CONFIRMED:** [IndustrySupport](../../../../Mod/IndustrySupport.lua) needs both current specialization/anchor facts and a matching UI BASE adjacency sample. It audits on district/completion/turn events and on a changed accepted sample. [IndustryRefresh](../../../../Mod/UI/IndustryRefresh.lua) notices runtime UI revision changes, but [SampleLifecycle](../../../../Mod/SampleLifecycle.lua) deduplicates an unchanged payload; an UNCHANGED receive also does not call the writer. [Store](../../../../Mod/CityProgressionStore.lua) calls `OnPermanentCityWrite` after first identity commit; its current [Claim consumer](../../../../Mod/ClaimProjects.lua) only marks the claim view for this path. The separate completed-Claim path schedules support derivation, but fresh first-district identity does not use that path. There is no explicit Industry-support completion of deferred eligibility work from this commit notification.

**LOCAL_SIMULATION_REPRODUCTION:** actual, unmodified IndustrySupport/IndustryRefresh/SampleLifecycle/RuntimeWork/SpecialistSupport were run with native facts and event delivery mocked using the existing C2 fixture. In both scenarios below the native District and BASE sample were already readable. The test then made eligibility available without delivering another support-audit event:

| Initially unavailable input | Carrier after first sample | After eligibility becomes Industry I + UI revision notification | After next-turn audit |
|---|---|---|---|
| Identity still UNASSIGNED | absent | absent; identical sample sends remain1 | present |
| Effective facts temporarily unavailable | absent | absent; identical sample sends remain1 | present |

Control: delivering the existing `OnDistrictConstructed` audit after facts become ready applies the carrier immediately. Thus the ordinary completion handler is not universally broken. The reproduced defect is a missing eligibility/readiness propagation path, not wrong BASE arithmetic, a governor requirement for Lv1, or proof that B233 changed the specialist writer. It is a strong candidate for the reported delay; the native ordering remains unrecorded. A narrow fix must cover both commit-before-sample and sample-before-commit, rather than betting on one engine callback sequence.

Ignored local reproduction at `local/diagnostics/B233-review/` (no official test or gameplay file changed):

| Original | Bytes | SHA256 |
|---|---:|---|
| support_readiness_repro.py | 3385 | 29f01fa4fb5c66b88df89dce1e941c44f48988cf55ea44bafb2c2e7c82b92283 |
| support_readiness_result.json | 1000 | 782285ee8b1b156521a4a337caf9d90887ca75fd088bb6bc75b7285a08d59dbc |

It uses the existing local Python/Lupa runtime and repository-relative fixture/source locations. Initial harness setup loaded the production Probe over its mock, causing zero sends; correcting only that harness injection produced the two results and successful control above. No source or assertion was weakened to repair the game. These observations do not prove native performance improvement or a completed fix.

## Next checkpoint

[B234 / IND-2 proposal](../../../Architecture/v2/Industry_Preparation.md#b234-proposal--standardization-baseline-and-industry-i-readiness) combines the requested support repair with III standardization construction +10% / purchase0%, self/network template-holder planning and exact old-writer retirement. The new Industry feature batch still awaits explicit approval. Do not implement L, Crew, Culture HOLD, Balance or new timers here.

This is a documentation/evidence checkpoint: current Status/Authority/P0-GH1 and the relevant plan only, followed by scoped links/selectors/hash/diff/publication checks. Existing source, formal tests, Design, accepted Architecture contract, runtime, configuration, main and earlier frozen evidence remain unchanged. No new user test is required before approval of the next batch.
