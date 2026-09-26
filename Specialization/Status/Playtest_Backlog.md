# v0.1 Playtest Backlog

Document Owner: Codex
Baseline: B069.96 / modinfo96
This is the issue intake linked by the current Status; validation results remain in Status/Validation. Unknown turns are not invented. A baseline designation is not bug-free certification.

| ID | Category | Found build | Turn | Issue / evidence | Current long game impact | Stable hotfix | Develop only / next step |
|---|---|---|---|---|---|---|---|
| PT001 | PERFORMANCE | B068/B069.96 | Unknown | Prior movement storm and memory growth; B069 local fix, full user counters pending | Unconfirmed residual risk | Only if confirmed severe recurrence | Counters, shared caches, event maps first |
| PT002 | BLOCKER (triage) | Reported during B069 period | Unknown | Native pure-virtual abort; cause not attributed to this Mod | One crash reported, recurrence unknown | If attributed/reproducible; no speculative fix | Preserve evidence, triage on next report |
| PT003 | UX | B068.95/B069.96 | Unknown | Diagnostic labels/position and Potential display refinements | Nonblocking | No | Yes, pending user scope |
| PT004 | BUG / limit | Existing baseline | Unknown | Cumulative 32 new-city binding limit | May affect very large games | User decision if reached | Future handling; do not silently lift |
| PT005 | DESIGN IDEA | B067 onward | N/A | General eligibility and ownership/inheritance deferred | Unsupported ownership cases | No automatic enable | Isolated; separate approval |
| PT006 | PERFORMANCE | B069.96 | N/A | Bounded runtime audit log; receipts/cache lifetimes/scans | Investigation, no confirmed new regression | No speculative refactor | Architecture v2 |
| PT007 | UX / DESIGN IDEA | B069.96 | N/A | Existing carrier inventory and safe visible institutions | Nonblocking | No | Inventory before adding facades |

New entries: ID, category (BLOCKER/BUG/BALANCE/UX/DESIGN IDEA/PERFORMANCE), found build, turn, evidence, current-save impact, stable hotfix decision, develop disposition. No balance change is implied by an issue entry. User may continue long play without completing a new test batch.

## B076.103 runtime milestone follow-up

PT001 update: [short idle evidence](Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md) passes for tested expensive-work suppression; memory held at9.28GB/9.24GB in respective idle windows. This is develop evidence, not a main hotfix or long-session root-cause closure.

| ID | Category | Found build | Turn | Issue / evidence | Current long game impact | Stable hotfix | Develop only / next step |
|---|---|---|---|---|---|---|---|
| PT008 | BUG / diagnostic uncertainty | B076.103 |1| Five short-test reports show net_receive0, discount_ack0, inflight1; actual sends remain bounded | Functional initialization not demonstrated; cause UNKNOWN | None authorized | Preserve evidence; verify bridge readiness in later functional testing before claiming full network PASS; no automatic fix |

## E2 native validation — deferred by user (2026-09-22)

PT009 — USER_GAME_TEST TODO, B098.125: 用户暂不方便实机测试，回家后再执行[P0-E2单城ownership round-trip](../Architecture/v2/P0_E2_Plan.md#b098125--单城-native-ownership-round-trip-validation)。保留失城退出、同城夺回、当前Governor/route重算及foreign save/load验证；全部仍PENDING_USER_GAME_TEST，非失败或验收通过。不启动游戏、不重复部署、不自动推进Claim/F。无需现在测试或另建监控/提醒。

PT009 update 2026-09-22 evening: 用户尝试B098，但基本诊断停在READING；见[失败调查](Validation/Results/Specialization_B098_E2_Read_Failure.md)。现改为BLOCKED_BY_DIAGNOSTIC_REGRESSION，先修入口，不要求继续ownership测试；原生往返判据不升级PASS/FAIL。

PT009 B099.126: eligibility修复本地通过，待部署/基本读取实机确认；确认后再续原ownership流程，永久记录不重导入。

PT009 update 2026-09-24: 用户将已部署B099.126的基本读取/收益复测及后续E2 native往返验证暂存待办。B099仍PENDING_USER_GAME_TEST，不记PASS；先确认专业/潜力、总督、专家读取恢复，再续ownership流程。当前无需用户测试，不重新部署，不推进Claim/F。

PT009 update 2026-09-25: B099基本读取实机恢复；E2交易后token nil、退出22/23及游戏内载入崩溃，详见[证据审阅](Validation/Results/Specialization_B099_E2_Transfer_Crash.md)。待调查，暂不要求重复测试；recapture/冷启动仍未测，Claim/F不放行。

## B099 E2 cold-load / conquest follow-up — 2026-09-25

[Two-image evidence](Validation/Results/Specialization_B099_E2_Coldload_Recapture.md): cold restart loads the foreign-held save and retains progression; exits23/23 after load. Conquest return remains PROGRESSION_HELD. Separate TECHNICAL_IDENTITY_BOUNDARY (live binding survival unproven) from EVENT_ORDER_BOUNDARY (matching conquest notification unobserved). Native immediate removal and post-return ACTIVE/Network remain unverified. No Claim/F, token copying or inferred city identity; next narrow diagnostic/event evidence scope requires authorization. In-session load crash remains unresolved.

PT009 B100 follow-up: [conquest evidence](Validation/Results/Specialization_B100_E2_Recapture_Token.md) confirms matching CityTransfered/candidate with nil live token; RETURN_IDENTITY_UNCONFIRMED blocks return. No further repetition needed before an authorized bounded identity-proof adaptation. TARGET_UNAVAILABLE is the departed foreign exit reference, not23/23 withdrawal regression. Events versus GameEvents CityConquered diagnostic namespace requires scoped correction if changed later.

PT009 B101: [foundation-guard evidence](Validation/Results/Specialization_B101_E2_Foundation_Guard.md) shows23/23 completed, RETURN_NEW_FOUNDATION before withdrawal gate, typed GameEvents.CityConquered plus exact transition chain. CityBuilt semantic classification needs narrowly authorized correction; no need to rerun pre-trade exit. No implementation/deployment in evidence review.

PT009 B102: [chain-order evidence](Validation/Results/Specialization_B102_E2_Chain_Order.md) latest native chain is valid, exits23/23; a pre-transition foreign-object add deterministically latches RETURN_CHAIN_ORDER in actual-store simulation. Fix hydration/transition phase separation before another native test; earliest native fault event not retained. No repair/deployment in this evidence review.


### B103.130 E2 hydration repair — native pending
Exact saved foreign load notifications no longer poison later transfer order. Targeted L3 PASS; first-fault diagnostic retained. After verified deployment use the existing foreign-held save → recapture → E2/city report → accepted-only separate save/coldload. No repeat migration/Claim/F; earlier B102 evidence remains historical.


### B103 native gate closed within observed scope — 2026-09-25
See [three-image acceptance](Validation/Results/Specialization_B103_E2_Recapture_Pass.md). Original-owner Research-city recapture, P2/receipt retention, coldload and user-confirmed governor-enabled Lv1/Lv2 PASS. Prior B103 pending test is fulfilled; do not repeat. Nonzero-route rebuild and wider native module/Legacy cases remain unproven; in-session load crash remains independent. E2 partial; wait for next-slice planning authorization, no Claim/F implementation.


### B104.131 — two explicit city records / USER_GAME_TEST_REQUIRED
Authorized implementation locally verified; [contract and minimal test](../Architecture/v2/P0_E2_Plan.md#b104131--authorized-two-existing-city-persistence-slice). Preserve B103 save; select second intact own city and import once, invest there only, verify first unchanged, save separately/coldload and read both selected cities. No re-import of first city, no repeat conquest. Runtime switch subject to existing W0003 gates. New self-founded-city/Claim/F remain separate unauthorized slices.

### B104 two-city native gate closed within tested scope
[Five-image review](Validation/Results/Specialization_B104_E2_Two_City_Pass.md): Industry P3→P4/receipt2→3; Research P2/receipt1 unchanged; user confirms restart/load retention. USER_GAME_TEST_PASS for this pair, not full E2. No repeat B104 test. Next: new self-founded-city registration plan only after user request/approval; no automatic Claim/F.
