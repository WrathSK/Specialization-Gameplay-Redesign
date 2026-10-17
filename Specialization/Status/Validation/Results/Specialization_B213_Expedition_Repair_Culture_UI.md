# B213 — Expedition repair and Culture presentation

Status: LOCAL_SIMULATION_PASS / DEPLOYED / USER_GAME_TEST_FAIL_TASK_START
Scope: user-approved audit findings 1–7, selected-target cancellation and Culture UI/report/icon additions.
Inherited diagnosis: the old save contains cost 1 and undersized per-unit arrays; its population delta matches the Theater plot index. This strongly supports a native old-save mismatch, corroborated by the clean new-campaign runs, while the exact native memory path remains inferred. The original B205 record is unchanged; this batch does not reopen that investigation.

Implementation baseline: source 09b2c65; live B212.239 from 05970d0 was unchanged during implementation. The separately authorized deployment is recorded below; native acceptance remains pending.

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

Implementation-checkpoint measurement: CURRENT 10 lines / 2577 bytes; manifest 84 projections / 1281641 bytes (baseline 84 / 1133473).

During implementation, original B205 evidence, Spec, frozen Design revisions and validation results, CityProgressionStore, training costs/capacity/source binding, GC, main and the external runtime are unchanged. Two optional fields in the existing Expedition envelope record selected work identity and unresolved due-time evidence; no separate store or migration framework is introduced. Culture's exact-target cancellation is the user's decision, while Commerce changes only align existing accepted wording.

## Deployment — 2026-10-16

The user explicitly authorized deployment and automatic game-exit detection. A restricted process query was unavailable; the OS query with process access returned no Civ6 executable. Both actual switches repeated the successful check. Existing receipt-bound tooling restored the exact stable bridge, retaining outgoing B212, then activated committed source `d1ea679368d0e12f905360ba86b76787f525abe1` as **B213.240/modinfo240**. New receipt: `B213.240-d1ea679-playtest.json`, phase **DEVELOP_ACTIVE**. Per-file equality **219/219 MATCH**; no pending marker. Stable recovery retained. Main, game configuration and Tuner unchanged; no game launch. Deployment is not native acceptance.

## One combined B212/B213 native session

Evidence priority: use the existing unattended collector for dispatch/task/outcome and explicit **文化见闻** reads. Screenshots are only needed for visual layout/icon issues or a result not represented in logs. Do not require per-turn images or an unrelated lifecycle replay.

From the develop checkout, before starting the game:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/collect_expedition_trace.py --idle-exit 300
```

Keep the terminal running. Output remains ignored under `local/diagnostics/B205/session-*/`; B205 is the inherited folder name, not the loaded package version. Wait for the collector's connected message after loading. On completion use Ctrl-C to flush the summary. If collection fails, retain its reported error; absence of a log is not a gameplay failure or PASS.

1. Use the approved new-campaign test base, never the historical pre-Expedition campaign. Begin with no task already running. Use one bound Expedition and its archive/source Culture city. Inspect the city **专业机构** rows and read P0 **文化见闻** for the baseline. This checks Culture rendering and that the report does not depend on selecting a surviving team. No new reward is expected merely from opening the report.
2. **派遣到新城市**: choose a met foreign major capital. Check mission opportunities show the civilization icon for **风土考察**, Great Work icon for eligible **艺文采撷**, and the actual Wonder icon for **奇观巡礼** where available. Arrive, start **风土考察**, and allow its displayed Standard-speed two-turn timer to complete. It must return to the target centre. Select the source city and read **文化见闻**: the previously unrecorded civilization/category gains exactly one entry; repeating that completed category is unavailable. This proves the real first-success/history path and duplicate gate.
3. In that city or another convenient eligible target, complete **艺文采撷** and **奇观巡礼** once each. Observe mission location (work-hosting building / selected Wonder) and return to centre, then read the source city's **文化见闻**. Each previously unrecorded category adds one entry. If all three are for the same civilization and none existed before, the total rises by three. A Wonder hosting an eligible work can cover the WORKS-in-Wonder repair naturally. If a suitable target is absent, report that category NOT_TESTED; do not manufacture a long target-hunting exercise.
4. Only if the existing test tools make it easy to remove the selected work during an active mission, verify cancellation/no reward and then start another legal task. This distinguishes fresh attempt identity from reuse of the cancelled attempt's acknowledgement. Otherwise retain this as locally verified/native untested; do not require manipulation of a foreign inventory or owner changes just to force the case.

No full save/END/cold-load/re-enable sequence is required. This batch adds an exact selected-work ID to task persistence: a convenient in-progress save/load can provide that narrow additional evidence, but it is not needed to inspect the UI and must not be reported passed if omitted. Native foreign readers/placement, visuals and mission completion remain pending until this session. Insight-derived city Tourism and Culture Network rewards are not implemented and must not be used as this test's expectation.

## Documentation status requested by the user

The read-only Insight UI/log path and bounded collector are implemented and documented in the current Expedition slice. Existing W0004 delta/inherited-evidence rules and project guidance already reduce repeated manual/screenshot testing; this combined session explicitly makes machine-readable logs primary while retaining visual evidence where necessary.

The Advisor [Self-Healing Reconciliation Rules](../../../Reports/Advisory/Self_Healing_Rules/Self_Healing_Reconciliation_Rules.md) includes R2 (derive current native facts; retain unavailable history), but the complete R1–R20 proposal remains advisory. The [Primary qualifications](../../../Reports/Proposals/Audit_Followup_Priorities.md#primary-review-qualifications) explicitly reject automatic adoption. In particular, visible units plus queue entries are not yet a proven complete capacity oracle across off-map travel, queue-admission races or unreadable native state. Current B209/B210/B213 contracts retain a bounded durable reservation and release it only on the established evidence. This deployment adopts no new self-healing policy and changes no capacity/persistence behavior beyond the already implemented B213 batch.

User decision: none newly required; selected concrete target loss cancels, no automatic replacement.
User testing: combined session above; native acceptance pending.
Primary next: collect and review the submitted logs/visual exceptions; do not start Tourism/Network or another repair batch automatically.

## Native failure review — 2026-10-16

User reports the combined B212/B213 test stopped. Actual deployed source is B213.240, not unchanged B212. Three screenshots reviewed and archived byte-for-byte under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B213/native-20261016/`; its manifest records all three SHA256 values. Raw collector evidence stays in ignored `local/diagnostics/B205/session-20261017T040254Z-d2d730/`, with hashes referenced by that manifest. No raw images, logs or local reproduction file are published.

**Native observations.** Screenshot1 shows four Culture institution rows with I–III enabled and IV current. This establishes the shown Lv4 presentation only, not low-level/ACTIVE-change/other-scale acceptance. Screenshots2–3 show the old P0 Expedition diagnostics after READ, with arrival/name/source intact; they do not show the new **文化见闻** report. The log has26 training records and15 Gate records: creation/name, dispatch, arrival, then three TASK failures at21:07:56,21:07:58 and21:08:41 local time. All fail at MISSION with `bad argument #2 to 'assert' (string expected, got table)`, exposed under generic `API_UNAVAILABLE`. There is no successful task-start/completion or N1_INSIGHT report event in this run. Earlier initial TASK_COMPLETE/END precedes the new team's creation and is not evidence of a B213 successful task.

**Confirmed B213 regression.** `mission()` returns `VALID, cityObject, workID` on success. The new TASK caller passes that cityObject as the second argument to `assert(valid=='VALID', result)` (Gate line609 at this checkpoint). The native log shows that this environment validates the message argument even when the predicate is true. The failure occurs before task movement, activity ownership, timer start or reward. It does not indicate a missing gameplay API, failed binding or old-save corruption. B212's successful path called `mission()` without passing its returned city object into assert.

**Why local checks missed it.** Existing mocks use standard Lupa assertions, which accept a non-string second argument when the predicate succeeds; the same isolated expression also succeeds in the installed Lua51 and Lua54 runtimes. It would be incorrect to attribute this solely to a known stock Lua-version difference. Applying only the observed native message-type restriction to the actual Gate fixture reproduces ARRIVED/API_UNAVAILABLE and zero Insight writes. The small reproduction is retained with local evidence. Existing778+66 local passes remain scoped evidence, not native correctness proof.

**Collector assessment.** The existing log is sufficient to locate this failure without another screenshot/test. READ clears the request-local error from the displayed snapshot, while the recorded failure remains in the log. The fixed-length stack text is truncated, but its complete parameter error plus source comparison identifies this call. Logs do not establish visual layout, and the absence of N1_INSIGHT cannot prove the new report works or fails. Keep screenshot1 for visuals; screenshots2–3 were not needed for this root cause. No extra native diagnostic step is requested.

**Proposed narrow repair, not implemented.** Use a string-only error on the invalid/unknown branch; never pass a successful native object as assert's message. Add the observed native assertion-signature constraint to the targeted mission fixture and verify valid PEOPLE/WORKS/PLACES starts plus unchanged invalid/UNKNOWN rejection. Review equivalent calls in this changed path; no global assert replacement, capacity redesign, self-healing policy or new gameplay behavior. After approval, resume the same interrupted mission-start test with logs; no repeat training campaign or blanket cold-load ritual.

**User clarification.** The Advisor's self-healing rules are reference directions for later architecture decisions, evaluated case by case at implementation time. They are neither a request to adopt the full proposal nor a reason to reject every useful principle. Preserve the existing proposal and per-feature evidence/authorization boundaries.

Current stop: B213 native task start FAIL; no source/test/runtime/config change in this review. User decision: authorize the narrow repair if desired. User testing: none additionally requested now. Primary next: await repair authorization; Tourism/Network and unrelated work do not advance.
