# Proposed timed-project queue recovery and remaining non-Commerce playtest

2026-10-31. Primary proposal at `44f9958`; live remains B397.424 (`aa51feb`), main B307.334. **PLAN_ONLY / NOT_IMPLEMENTED / awaiting user review.** This records the user's request to prepare a plan and reconcile remaining tests. It does not approve new queue semantics, change formal Design/Architecture, authorize implementation or claim final U5. Original acceptance/evidence records remain frozen.

## 1. Intended result and accepted boundary

Repair Engineering Study and Era Dialogue entry/re-entry so a reliably selected, eligible project that becomes the **only** current queue item can start or recover without clearing the entire queue. Keep their independent qualification, cancellation, full-turn, receipt and reward rules. Preserve the present [single-item rule](../../Design/Shared.md#能力记录异常与项目机制边界): a project at the head with other items behind it does not count as a valid sole-project round. Allowing that different behavior would require a separate explicit rule change; it is not silently included here.

The user additionally raises stale queue eligibility: native queues do not predict that a prerequisite or quota will become legal by the time a later entry runs. Therefore **queued entry is never a reservation or future eligibility credential**. The plan must address repeated Study entries and exhausted knowledge, not merely remove a queue-size check.

[The reviewed Industry evidence](../../Status/Validation/Results/Specialization_B397_Industry_Playtest_20261031.md) and PT016 remain the failure basis. No repeat investigation of accepted profession formulas, Network Option B migration, ownership, GPP or GC is added.

## 2. Source clarification and existing protections

A clarification to the previous evidence report's “ordinary/queued selection” wording: the UI argument named `queued` comes from `CheckQueueItemSelected()`, meaning an existing queue/manager slot is selected. It does **not** mean queue mode is open. The native `GetBuildInsertMode()` separately decides append versus replace. A production-list click may append while queue mode is open.

Verified external read-only source: Civilization VI Base `UI/Panels/ProductionPanel.lua:276–287,410–420,2885–2914`; HD `UI/Replacement/DL_ProductionPanel.lua:67–74` delegates to that check except its Espionage view. Native `UI/ProductionHelper.lua:205–213` submits swaps directly. No external file will be edited or copied into Git.

Repository paths at this baseline:

- `Mod/UI/CrewProjectOrder.lua:84–92,109–121`: separate adapters, list-selection path and existing same-city queue hooks.
- `Mod/UI/EngineeringStudyUI.lua:30–47` and `Mod/UI/DialogueProjectUI.lua:59–89`: same-turn send intents, discarded on multi-item confirmation; drag/natural advance does not recreate them.
- `Mod/UI/TimedProjectSelectionClient.lua:104–118`: queue events wake an existing send intent; they do not establish one. Idle publishing is not permission to sample again.
- `Mod/TimedProjects.lua:5–14` and `Mod/TimedProjectModel.lua:3–11`: sole current, multiple, other, empty and UNKNOWN remain distinct.
- `Mod/EngineeringStudyProjects.lua:175–188`: interrupted production is distinct from a still-active round.

This correction narrows the diagnosis; it does not invalidate the observed missing re-entry path or rewrite its frozen report.

### The user's last-knowledge / repeated-Study example

E is civilization knowledge coverage, not a consumable currency. If E=5 and L=4, that city has one currently available successful study; another city has its own L.

| Situation | Confirmed present behavior / proposed safeguard |
|---|---|
| Several Study entries exist together | Present single-item rule blocks starting; they do not legitimately run as a batch. Recovery must not bypass this rule. |
| A single eligible Study starts | `EngineeringStudyModel.lua:34–37` requires L<E; native queue presence alone is insufficient. |
| Last legal round completes | `EngineeringStudyProjects.lua:130–137` rereads E and again requires L<E; `EngineeringStudyModel.lua:52–55` adds one L, writes its receipt and clears pending. |
| L becomes E | `EngineeringStudyProjects.lua:68–76,89–90` withdraws access when no round is pending and publishes KNOWLEDGE_REACHED. No new automatic BEGIN may be attempted. |
| Duplicate completion notification | `EngineeringStudyProjects.lua:127` does not award without a pending round. |
| Already queued leftovers | The Mod has no explicit Study queue-removal operation. Required-building withdrawal does not prove that the engine deletes existing entries. Native automatic removal is unverified. |

**Proposed UX addition for approval:** reject adding a second copy of the same owned timed project to that city's queue, after reliable fresh entry verification; guard a second click while the first native insertion outcome is unresolved. Apply to Study and Dialogue, not ordinary native projects. This prevents unusable duplicate queues without inventing predictive quotas or changing rewards.

For old queues that already contain duplicates, preserve the single-item guard and show the concrete reason. When eligibility is **confirmed exhausted**, retire our session candidate, stop further BEGIN attempts and display “已达到当前可研习知识” (Dialogue: the current start-era opportunity is already used). If a native leftover remains, explain that it must be removed. UNKNOWN is not exhaustion and must not erase records or entries. Do not use FinishProgress to discard a leftover.

**Automatic native queue deletion is excluded from this minimal proposal.** It would require an explicitly approved removal policy plus fresh city/reference/index/entry verification and isolation from unrelated entries. It cannot be promised as an engine side effect or smuggled into entry recovery. If the user instead wants repeatable timed projects with ordinary tail items, design exhausted-tail behavior together with that separate queue-rule change.

## 3. Smallest implementation sequence after approval

1. **Reproduce with actual components.** Use the real UI adapters, selection client/readers, each Gameplay controller and Store/notification chain. Preserve the baseline examples for reorder, natural progression, multiple-item pause, stale eligibility and duplicate completion. Verify real insertion/swapping metadata before selecting an entry-proof representation; an unverified queue API/signature is a stopping point for that path.
2. **Separate queued candidate from send intent/timer.** Retain bounded session-only scalar evidence that this exact city/project was selected and its native entry confirmed. It can wait across turns; it is not an old StartTurn, active round or reward credential. A fresh unconfirmed click, confirmed entry, active round and terminal receipt remain different states. Normal writes and interruptions invalidate the appropriate evidence, not unrelated cities.
3. **Recover only on related evidence.** Reuse the existing city production/queue events, coalesced at the existing safe publication boundary. A list selection, subsequent confirmed queue entry, or separately proved initialization recovery may admit a candidate. An arbitrary event or `current==project` by itself may not create BEGIN. Swaps/natural advancement require a fresh same-city read confirming actual entry/current/size. Duplicate or indistinguishable entries stay blocked with a reason.
4. **Start a fresh legal full turn.** Preserve an existing valid ACTIVE round rather than restarting it. After confirmed interruption/cancellation, a newly legal sole-current candidate starts a new round at the current reliable local boundary, without crediting waiting/interrupted turns. Do not backdate after an already-passed END boundary; retain only relevant deferred evidence until an existing safe local boundary can confirm a new start. CALLING/ambiguous HELD must not restart or replay an irreversible completion.
5. **Revalidate independent owners.** Study still checks industrial IV, current L/E and unique receipt; Dialogue still checks Culture qualification, start-era quota and completion-time collection. A candidate does not reserve knowledge, quota or yields. Stop candidates on confirmed ineligibility; UNKNOWN waits for a related fact/availability change, never elapsed time. Both branches keep Store readback, reference fences and original completion handling.
6. **Handle reload and display honestly.** Persisted ACTIVE resumes through its current saved controller. Session candidates do not become saved authority. Evaluate the existing necessary initialization boundary for bounded, provable queued-entry recovery; never guess historical start or silently add a Property. If entry/source identity cannot be proved, retain explicit reselection as a documented narrow fallback and report the limitation. UI distinguishes queued/not current, multiple items, unknown read, one-turn ACTIVE, native receipt pending, and exhausted opportunity.

Enable this only for Study and Dialogue. A small shared client helper may be used if appropriate; Claim stays opt-out with its own policy. Inspect the existing adapters/controllers before expanding the file list. No generic event bus, broad controller rewrite, service discovery or new saved queue system.

### Runtime Impact Contract for the proposed batch

- Facts: fresh scoped native queue entry/current/size and owner-published project qualification; reuse existing qualification/Store facts. No new building, district, player or empire enumeration on production events.
- Events: existing CityProductionChanged / CityProductionQueueChanged / UI CityProductionUpdated and necessary existing initialization/availability boundaries; local test player and matching city/reference only. A safe turn boundary may drain only already-related deferred work, not rescan all waiting cities every turn.
- Cost: one coalesced scoped queue observation per actual related change; any entry enumeration is bounded by the engine queue capacity, verified before use. No idle read or no-progress retry; preserve existing event-major registration order.
- Capacity/lifetime: bounded scalar candidates aligned with the current client's 2,048-city ceiling; no native objects or whole-city fact snapshots retained. Explicit removal/confirmed invalidity/reference/context retirement ends the relevant candidate. Capacity/identity ambiguity fails closed and is visible.
- Dependencies: two UI adapters, selection client/readers, current Gameplay owners/Store/views. Diagnostics remain optional observers; enabling/disabling them cannot enable business recovery or settle a project.
- Failures: native read failure is UNKNOWN; send return is not ACK. Do not blindly resend BEGIN/FinishProgress; distinguish unsubmitted candidate, sent attempt and committed active round.
- Scope: no formula, E/L definition, era quota, money, carrier policy, GC, network transport, save schema, main or external Mod change. Any genuinely necessary new persistent evidence or shared contract beyond this proposal requires a separate decision.

## 4. Verification plan

Local gates, after implementation authorization:

- Before/after counterexamples through actual UI→reader→Gameplay→Store composition for both owners; normal sole selection and original policy remain positive controls.
- Candidate waits behind Worker across turns; Worker completes and leaves the timed project as sole target. Reorder away/back, then remove the other item; restoration creates one valid new round and one reward. Head-plus-tail remains clearly paused under current policy.
- ACTIVE with a second item appended then removed; real interruption versus temporary blockage; repeated same-turn events/clicks/swaps and UI reconstruction; start near END/BEGIN boundaries; no partial-turn credit.
- Last opportunity: E=5/L=4, second-copy insertion refused; an externally/previously duplicated queue stays blocked, not rewarded; completing the one valid round reaches L5 and clears candidate/access. Stale BEGIN/late completion cannot award L6. Equivalent Dialogue used-era cases retain its independent quota.
- UNKNOWN, stale reference/owner, reentrant native changes, unresolved native send, CALLING/HELD and reload. No timers/polling or reset after a failed read. Queued cold recovery and active-timer cold recovery are distinct fixtures.
- No-candidate/unrelated-city/idle stress adds no native reads, starts or writes. Optional diagnostics on/off give identical business results. If shared code changes, actual Claim composition retains original behavior; no automatic Claim queue policy migration.
- Preserve protection assertions in `test_refactor_s7d2.py:70–99` and `test_refactor_s9e10.py:30–33`: no-source event/current display cannot start a project. New positive cases must include the new verified candidate source. Do not delete or invert assertions merely to pass the new behavior; legacy/opt-out and missing-proof cases remain protected.
- Select current affected tests and restricted Lua5.1/XML/modinfo/context gates under W0004; publish compact actual results, not expanded cumulative Closure. No local PASS is a native PASS.

Minimum later native delta, only after a verified repaired package: one Engineering Study natural-advance case, one Dialogue reorder-to-sole case, and one queued-before-start reload if that automatic recovery is implemented. Check full-turn display and one reward. Check duplicate refusal in the same small session; no whole ability retest. Claim native repetition is not required solely because a guarded shared helper changed; local actual-Claim regression is required, and a concrete new native uncertainty would need its own explanation.

No implementation or deployment has occurred. Approved implementation can use the existing standing safe develop deployment process after checks and reliable game exit; no new game launch or main promotion follows from plan approval.

## 5. What still needs testing outside Commerce

This is a current coverage reconciliation, not a replacement audit/backlog. B391's frozen checklist is an intermediate-version handoff and has been superseded in part by the user's B393–B397 results and explicit exclusions. Do not mechanically reissue it.

| Priority / owner | Remaining item | Minimal useful observation / disposition |
|---|---|---|
| Required after repair / user | PT016 queue recovery | The native delta above; do not repeat known failing permutations before repair. |
| Shared integration / user, combine with asset restructuring | Save while REALLOCATING → reload → complete configuration | Old effects do not revive during reallocation; the completed configuration restores appropriate access/effects once. No city transfer; this is the unclosed shared T6 case, not another four-profession numeric campaign. |
| Final engineering candidate / user + Primary | Ordinary background and performance observation | After the candidate's relevant engineering work is complete, use a few normal planned test turns with panels closed for part of the time. User notes idle/AI/local-action hitches; Primary interprets collector/native workload and does baseline attribution. No duplicate reload/network ritual or speculative performance percentage. |
| Opportunistic / user | Dialogue starts just before game-era transition | Successful round uses its **start-era** opportunity; a later new-era opportunity is not wrongly consumed. Already deferred by the user. |
| Opportunistic / user | Two A4 Industry sources with different L and exclusive/overlapping templates | Per-template union and highest coefficient only among actual holders; no globally borrowing the strongest source's L. Existing A3/mixed-source positives remain accepted. |
| Passive progression / user | Academic Tradition age40 cap; later Practice N3/N6 thresholds | Observe during natural play;36/20% and N1/N2 results already pass. No special wonder/population grind. |
| Known limitation, not current mandatory test | Same-tier Crew completes in two source cities in one turn | Accepted intake retains OPEN native attribution and default U5 same-tier one-city restriction; defer repair/retest under that arrangement. Do not turn the old optional checklist into a new pass gate. |
| Natural recurrence evidence only | Consulate-granted unit appears as Expedition with no actions | Earlier report remains unclosed, separate from normally trained teams and the parked displacement save. If it recurs, record grant/unit identity; not a demand to reconstruct the whole scenario. |
| Long-play observation only | Naturally larger empire/new cities, rare native displacement/UNKNOWN/flood/pillage | Collect when encountered. No deliberate pillage, corrupted save, Property edit or engineered packet loss. |

Evidence: [B391 checklist](../../Status/Validation/Results/Specialization_B391_Develop_Playtest_Checklist.md) T4/T6/T8; [B395 coverage](../../Status/Validation/Results/Specialization_B395_Culture_Research_Playtest_20261029.md) and [Chair deferral](../../Status/Validation/Results/Specialization_B395_GPP_Interface_Investigation_20261029.md#research-chair--latest-user-steering); [B397 Industry review](../../Status/Validation/Results/Specialization_B397_Industry_Playtest_20261031.md); accepted S8 R03/R22 disposition in [existing intake](Audit_Followup_Priorities.md); grant issue in [B393 Culture](../../Status/Validation/Results/Specialization_B393_Culture_Playtest_20261028.md) and B394 follow-up.

### Already covered or explicitly not demanded

- Culture/Research/Industry ordinary cases already accepted keep their scope. Culture's three-category Vietnam network and25→30 specialist Culture are **already covered**, superseding its earlier deferral. All trained Expedition task types and recorded reload chains have positives; this does not erase the separate grant or parked displacement issue.
- No repeated per-profession GPP testing: the user's later without-governor control localizes the automatic/manual discrepancy to the HD/native specialist path. Chair building-list refresh investigation is user-deferred. Harbor is not a required extra Meaning test; clear-all-works and same-era deduplication already pass.
- B397 four loaded-turn route recoveries, signal catch-up, new-route same-turn Standardization, forwarding, governor departure/return and the T39 ordinary-unit control have evidence; no duplicate transport campaign. Genuine nonzero Commerce/Capital/Development outcomes remain separate intended commercial tests.
- Ownership gameplay, deleted/nonreproducible Expedition displacement and forced rare pillage remain excluded/deferred. No full Crew-tier/modifier permutation campaign.

### Engineering or missing implementation — not solved by asking the user to test

- D2 Commerce/Culture source-attribution persistence has codec/Cell/Store groundwork, but actual cold-recovery consumer integration remains unclosed at this baseline (`Specialization_B391_Refactor_S9g4.md`). A normal successful reload is not proof of partial-source UNKNOWN recovery. Perform the approved engineering/local composition work before any necessary new native assertion.
- D7 exact recovery boundaries, applied-owner publication closure, full U4 regressions and S10 production-duty migration/safe retirement remain engineering obligations. Keep accepted Option B convergence after U5; this plan does not pull it or cleanup into the queue repair.
- Deliberately corrupted subrecords, dropped packets and UNKNOWN recovery permutations belong in local fault-injection/actual-module testing; not a player task. Existing diagnostics must remain removable and outside business authority.
- Meaning Extension's government/diplomatic Culture projection remains a known deferred implementation, not a failed positive-yield test. Research NetworkBoost is currently started retired at `Mod/Gameplay.lua:944`; do not demand gameplay tests of that retired path or silently call the full deferred Design implemented.
- Size22 asset warnings, panel refresh and performance/heap attribution are existing maintenance/measurement matters. The present proposal does not authorize unrelated art, UI, GC or performance refactoring.

## 6. User review and next boundary

User decision: review the scoped implementation plan, including the proposed duplicate-copy UI guard while retaining sole-project timing. Native automatic deletion and multi-item counting are not included; either would need an explicit additional policy decision.

User testing: none newly requested before repair; continue the intended Commerce test if desired. Later non-Commerce mandatory work is the small queue delta and the shared REALLOCATING recovery case, plus final-candidate normal observation at the appropriate engineering boundary. Everything labeled opportunistic/parked stays that way.

Primary next: wait for plan approval before runtime/test/Design/Architecture edits. After approval, prove the queue evidence and safeguards, implement only the accepted scope, run minimum sufficient checks and use the existing safe develop deployment workflow. Stop the affected path if reliable entry/initialization proof cannot be established without new persistence or changed policy. No main promotion.
