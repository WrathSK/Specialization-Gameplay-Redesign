# B213 — Expedition repair and Culture presentation

Status: LOCAL_SIMULATION_PASS / NOT_DEPLOYED / USER_GAME_TEST_REQUIRED
Scope: user-approved audit findings 1–7, selected-target cancellation and Culture UI/report/icon additions.
Inherited diagnosis: the old save contains cost 1 and undersized per-unit arrays; its population delta matches the Theater plot index. This strongly supports a native old-save mismatch, corroborated by the clean new-campaign runs, while the exact native memory path remains inferred. The original B205 record is unchanged; this batch does not reopen that investigation.

Baseline: source 09b2c65; live B212.239 from 05970d0 remains unchanged. B212 native acceptance is deferred.

## Repair boundary

1. Cancelled tasks receive fresh durable attempt keys, not a successful-task counter key reused by UI acknowledgements.
2. Mission validity is tri-state; selected native work identity is rechecked. UNKNOWN cannot award or masquerade as invalidation. Due-time UNKNOWN is held if no same-turn evidence resolves it; later facts cannot reconstruct past eligibility.
3. Eligible works inside Wonders are allowed; PLACES still targets the actual completed Wonder.
4. Trace-unavailable responses use bounded delayed retries; invalid frames stop. Legal escalating costs are not compared with base cost as an error.
5. P0-N1 uses current mission/history dependencies and a bounded current slice; obsolete exclusions/history are conditional.
6. Status CURRENT is separated from preserved stage history; Architecture current versus historical scope is explicit.
7. Commerce D0050 text now consistently permits absent S-source with S1 and states already-accepted owner-scoped protection. No Commerce implementation.

## UI and evidence

Culture uses the Research institution row style. P0 **文化见闻** shows the selected city's historical/effective entries and categories, independent of a surviving team; UNKNOWN is not zero. Explicit report requests emit bounded N1_INSIGHT records for the existing collector. Tourism and Network effects remain unimplemented. Relocation icons represent currently available mission types using native Great Work, civilization and actual Wonder assets.

## Validation

- **778 Expedition tests PASS:** actual Lua mission/Gate/Store/activity/reader/window integration, existing training and persistence regressions, and offline collector/reader protocol tests. Native-placement and engine facts are mocked; this is LOCAL_SIMULATION_PASS, not native acceptance.
- **66 additional tests PASS:** Culture institutions, selected-city Insight report, P0 layout, Store ordinary-write boundaries, Dialogue projects and context helper. Store per-value results match the inherited regression; visit-count reductions are not a new native CPU/memory claim.
- **Focused independent counterexamples:** unavailable civilization at the due turn → a same-turn READ with only location restored keeps UNKNOWN; restoring civilization next turn holds without reward. Full same-turn recovery permits one award. Unavailable capital facts do not suppress readable WORKS/PLACES; a known noncapital remains invalid for PEOPLE. A stale selected WorkID cannot start a task after a same-type replacement.
- **Collector protocol:** unavailable trace responses use a five-second retry delay (three connections/nine fixed sends over a simulated 15 seconds), malformed snapshots stop, and only LISTENING is reported connected. Native 75/90 over definition base 60 are not cost-floor alerts. The report stream is bounded and only emitted on explicit P0 reads.
- **Environment:** Python 3.14 and existing isolated Lupa.lua55; SQL fixtures read the configured external Gameplay database and operate in memory. Collector fixture tests required repository-local temporary-directory access; the sandbox-denied attempt was rerun with that access and all 778 passed. No dependency installation, game launch, live query, deployment or configuration change.
- **Not passed:** the additional historical `test_b128_progression_regression.py` wrapper stopped while loading its inherited `test_b108_e2_multicity` fixture (`include` unavailable), before assertions. It was not weakened or counted as PASS. Current Store/Dialogue and Expedition regressions above cover the directly touched paths; the old wrapper remains a recorded fixture limitation.
- **Document/integrity checks:** local Markdown paths/anchors, all current manifest selectors, context helper self-test, changed XML and reviewed source/context hashes are checked at the commit checkpoint. No native UI-layout, foreign-reader or mission-success claim is made.

## Reading and preserved boundaries

Status CURRENT shrank from 132 lines/16060 bytes to a bounded current summary; the prior block is preserved verbatim under historical progress. The new plan slice is 17 lines/4570 bytes. Older native reports and seven unchanged UI/SQL/test references are conditional. The default manifest still has 84 projections: it includes complete current mission/history contracts plus real CityProgressionStore, Gameplay, Probe and institution dependencies, so its total projected bytes increase rather than decrease. This is scoped completeness, not a token/quota saving claim. Final measurement is recorded below; byte counts are reading-volume observations only.

Final measurement: CURRENT 10 lines / 2577 bytes; manifest 84 projections / 1281641 bytes (baseline 84 / 1133473).

Original B205 evidence, Spec, frozen Design revisions and validation results, CityProgressionStore, training costs/capacity/source binding, GC, main and the external runtime are unchanged. Two optional fields in the existing Expedition envelope record selected work identity and unresolved due-time evidence; no separate store or migration framework is introduced. Culture's exact-target cancellation is the user's decision, while Commerce changes only align existing accepted wording.

## One future combined native session

After a separately permitted deployment, continue the B212 mission test with this repair package rather than testing the known defective B212 source separately. Select the archive city: inspect Culture institutions and **文化见闻**; inspect relocation icons where corresponding targets exist. Complete one mission and verify its category/history appears in P0 and collector. If an existing controllable target permits it, invalidate the selected work/site, confirm cancellation/no reward, then start another legal mission to verify it leaves preparation and runs normally. Do not manufacture UNKNOWN reader faults or repeat already-covered cold-load cycles merely for UI. A saved in-progress task is the only newly relevant persistence check if the user already has a convenient test save; otherwise local serialization evidence remains explicitly local.

User decision: selected concrete target loss cancels; no automatic replacement.
User testing: deferred; this record claims no native PASS.
Primary next: preserve this local checkpoint and await the deferred combined native check/deployment step; do not start Tourism/Network or another repair batch.
