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

### B105.132 — EVENT_BATCH_BOUNDARY / minimal native evidence required
See [checkpoint](../Architecture/v2/P0_E2_Plan.md#b105132--authorized-event-batch-evidence-checkpoint). On a test copy, right-click 移民/施工队 to arm one location, perform founding, then right-click E2往返 to capture pages. Separately arm an own noncapital city before a convenient gift to AI and capture after. No migration/investment/reload loop. Evidence-only; fresh enrollment NOT_IMPLEMENTED. No random raze test requested. B104 existing two-city acceptance unaffected.

### B105 native evidence received — no repeat test
[Four-image result](Validation/Results/Specialization_B105_E2_Event_Boundary.md): observer paths PASS; first Publish demonstrably splits both founding and transfer notification chains. EVENT_BATCH_BOUNDARY remains for automatic enrollment; next scoped boundary proposal must use positive evidence, not timeout/Publish-count inference. Playback is candidate only. No immediate user test; existing B103/B104 results unchanged.

### B106.133 — FOUND_CITY native delivery pending
[Minimal test](../Architecture/v2/P0_E2_Plan.md#b106133--authorized-found_city-evidence-checkpoint): same arm/read controls, one ordinary Settler founding plus one transfer negative control. Capture all pages. Missing hook/enum at arm: screenshot and stop. This adds founding-reason evidence absent in B105, not a repetition of full E2 acceptance. No registration/Claim/F.

### B106 minimal native gate closed — 2026-09-26
[Two-image result](Validation/Results/Specialization_B106_E2_Found_City_Pass.md): actual Gameplay FOUND_CITY delivered with selected Settler identity after Initialized; transfer control has Transfer without FoundCity. Scoped USER_GAME_TEST_PASS; no repeat requested. Registration remains unimplemented; revise the narrow registration plan, not universal Publish boundary or Claim/F.


## B107 fresh-city native follow-up — scoped acceptance (2026-09-26)

[Evidence](Validation/Results/Specialization_B107_E2_Fresh_Registration_Pass.md): automatic normal-founding NONE/P0 and Research P1 pictured; P2 retained after restart explicitly user-confirmed. Old migrated control + fresh inner-schema2 coexistence remains deferred at the user's simplified-new-game test boundary; local regression is retained. P0-only coldload has no separate confirmation (two P0 images alone do not prove restart). Neither item requests immediate retesting or searching old saves. No cap expansion/Claim/F authorization is implied.


## Post-B107 test-priority update — 2026-09-26

The standalone migrated-old + fresh-new native compatibility test is removed from the required user-test queue, following the user's question and the [remaining-E2 plan](../Architecture/v2/P0_E2_Plan.md#post-b107--remaining-e2-plan--new-path-isolation-over-migration-compatibility). It was a transitional adapter check, not the final product invariant; existing local compatibility regression remains while the adapter exists. This is cancellation/deprioritization, not native PASS. Future mandatory isolation test uses3 new-path cities and one coldload, including one NONE/P0 control; this also covers the currently unconfirmed P0-only load assertion without a separate repeat. No user test or search for old saves requested now. Runtime remains B107 with existing test limits until separately authorized implementation.


## B108 new-game multi-city gate — USER_GAME_TEST_REQUIRED

New game only. [Current exact test](../Architecture/v2/P0_E2_Plan.md#b108135-implementation-result--evidence-boundary):3 normally founded cities, A remains NONE/P0; B Campus→P1→one investment P2; C Theater→P1; one separate save + full restart/load; read3 selected-city E2 reports. ACTIVE follows current Governor. No manual migration, old-save search, conquest or Claim. Native initialization/API and persisted independent record behavior remain unconfirmed; local tests do not certify them. Preserve B107 saves for rollback; no downgrade guarantee for B108 saves.


## B120 project observation deferred

PT010 — 2026-09-28 USER_GAME_TEST TODO：用户回家后再测B120.147；目前LOCAL_SIMULATION_PASS，原生事件顺序PENDING，非FAIL或PASS。[最小流程](../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#26-b120147--authorized-project-turn-observation-and-completion-decision)：唯一承接项目→开始项目观察→正常过一回合→结束观察/报告。无即时测试要求，不重新部署，不自动进入B/Claim/F，不设置定时提醒。

PT010 update 2026-09-28 evening：[B120截图](Validation/Results/Specialization_B120_Project_Turn_Observation.md)确认正常回合采集限定PASS，待办关闭，无需重复；Started/StartComplete缓存7→生产更新15→Activated/终点15。自动完成、1T、注入/存读仍未测，不由本次放行实施。

## B121 automatic project cycle — pending native test

PT011 — B121.148 USER_GAME_TEST_REQUIRED：单城开启1回合→正常过回合自动退出→同回合新Q为0→再过回合正常增长。85项本地测试不是原生无溢出证明。仅本次自动时点及实际显示位置；[完整流程与停止条件](../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#28-b121148--authorized-single-city-automatic-completion-prototype)。B120采集PT010保持关闭，不重复纯观察。

PT011 update 2026-09-28：[B121三图](Validation/Results/Specialization_B121_Automatic_Project_Pass.md)与用户反馈确认正常周期限定PASS，机制测试待办关闭。城市旗帜/Tooltip及底部CityPanel高工期残留继续作为UI待办，建议下一最小L1显示修补，未授权实施；不重测已通过正常周期。

## B122 direct selection and HUD timing — native entry failed

PT012 — B122.149新入口/城市显示待实机：不打开P0，直接选择唯一当前实验项目，检查生产栏/旗帜及Tooltip/底部面板1T→正常一回合退出→普通目标显示与初始0正常。[完整范围](../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#29-b122149--native-production-entry-and-remaining-city-time-displays)。B121/PT011正常周期保持通过，不扩大chop/harvest等范围。

PT012 update 2026-09-28：[自动入口失败](Validation/Results/Specialization_B122_Selection_Failure.md)，队列检查拒绝启动。暂停测试，等待入口修复授权；B121限定PASS保留，不要求重复失败流程。

PT012 B123 update：[启动确认修复](../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#30-b123150--bounded-selection-confirmation-repair)112项LOCAL通过，已部署替代失败包，待实机重测。直接选择→1T→一次退出→普通目标0；失败截队列数量/原因。无P0启动操作，未验收前不关闭待办。

PT012 closure：[B123用户文字验收](Validation/Results/Specialization_B123_Project_Pass.md)确认三处1T、正常完成、后续无溢出；附加砍树场景通过。关闭本条，无需重测其它待办/旧空队列实验；不扩大到收获、多城、保存及正式奖励。

PT013 — B124.151正式一回合认领待实机：冻结候选→两城独立启动→计时中冷加载→正常完成Identity/P1→入口退出/普通目标无带入→认领后冷加载；另一次单城改选重开。无需重测旧空队列或其它待办绕过。[完整最小流程](../Architecture/v2/P0_E2_Plan.md#最小用户验收-pt013)。本地PASS不等于原生PASS。

PT013暂停：[B124入口失败](Validation/Results/Specialization_B124_Claim_Entry_Failure.md)，商业候选项目灰；城邦来源被major-only拒绝。等待窄修复授权，不重测失败步骤。

PT013 B125：入口/城邦修复本地通过，待原生复测。[最小步骤与边界](../Architecture/v2/P0_E2_Plan.md#b125152--authorized-claim-entry-and-city-state-repair)。日内瓦从征服前档开始，不事后重建snapshot。

PT013 B125复测：商业入口用户确认PASS；城邦ACQUISITION_SOURCE_KIND_UNKNOWN，双城流程暂停。[接口证据与下一窄修复](Validation/Results/Specialization_B125_City_State_Type_Failure.md)。

PT013 B126：城邦类型改为原Owner配置＋Gameplay文明类别，缺IsMinor用例本地通过；从日内瓦征服前档复测，再双城一起续测。商业入口无需重复专项验收。

PT013 B126主流程USER_GAME_TEST_PASS（用户称B124任务，实际截图B126）。[验收与UI待办](Validation/Results/Specialization_B126_Claim_Core_Pass.md)：冷加载1T刷新、认领/施工队无资格项目隐藏仍OPEN；下一窄修复待授权，不进入F。

PT013 B127：冷加载同步与Claim/Crew列表修复STATIC/LOCAL通过；用户要求不独立UI验收，合并下次实际测试，重点不先打开生产列表的加载计时与精确可见性。[实现与下一步计划](../Architecture/v2/P0_E2_Plan.md#b127154--claim-load-and-project-visibility)。

PT014 — B128未专业城原Owner夺回原生待验；优先科研候选单城交出→foreign冷加载→征服取回→原候选认领→投资/冷加载，合并B127显示与项目隐藏。工业模板缺历史暂停单列，不扩成收益PASS。[完整流程](../Architecture/v2/P0_E2_Plan.md#最小用户测试--pt014)。

PT014更新：商业候选替代科研fixture；夺回/同session认领投资所测通过，重启续接FAIL，暂缓重测，等待窄修复授权。[结果与计划](Validation/Results/Specialization_B128_Claim_Reload_Failure.md)。

PT014 B129：同步确认/有限重试本地通过，待失败档冷加载；过期计时应暂停并明确重新选择，不能补发。见E2计划B129最小复核，不重做征服，不另测UI。

PT014 B129所测商业夺回/认领读档修复USER_GAME_TEST_PASS，用户明确验收，1图归档；本轮门禁关闭，不扩大E2范围。[结果](Validation/Results/Specialization_B129_Claim_Reload_Pass.md)。

性能B130：内存观测左键开始、右键读取；开始/过1回合/静置/再过1回合截图，征服可选。只读接口不可用也保留计数，最多6回合停止。见技术报告B130段，无需重做Claim。

B131.158：替代B130后续归因待测；同一入口左开始、正常过1回合右读取、静置约20秒右读取，截图配进程内存。仅诊断，根因未定，无GC/清理/玩法推进。

B131归因观测已收：2026-09-29六图归档，含同回合27秒对照；本轮短测试已完成，不再重复派发。内存原因仍OPEN，非性能修复PASS；见B129_Event_Memory_Investigation之B131 native results。

B132.159：foreign事件过滤与D复用待实机；同档左开始→过1T右读取配活动监视器截图，可顺手切换本城专家/焦点检查收益响应。不要求造局/额外掠夺。未宣称内存修复PASS。

B132短测试已完成：六图归档，用户确认专家/建筑收益正常；GPP请求1/接收1、对话入口67、D命中3，窄优化观测通过。进程本回合仍+0.23GB，主要内存增长OPEN，不记内存修复PASS。后续操作图非静置对照；无需立即重测，先定域调查剩余扫描路径。见技术报告B132 native results。

B132追加多回合验证完成：11组22图归档，三次征服＋静置＋T40–45。静置进程回落0.10GB但Lua不回落；后续Lua仍增，记录/所列缓存稳定，MEMORY_CAUSE_OPEN。第六回合自动观察停止，手动读数仍有效但归因桶不完整。无需继续长测，先定域定位剩余实际扫描/分配路径。见技术报告B132 multiturn conquest results。

B133.160已部署、170/170 MATCH（source d50029a），本地通过、待实机：四处确认的重复工作已修，GPP64→32、基础区域替换表1→0、八次D采集定义枚举9→1。同档三次征服＋1～2回合短对照，可顺手检查收益；非内存修复PASS。见技术报告B133段。

B133对照完成：10组20图已归档。T45累计建筑检查−2.17%，城市遍历数不变；T40–45 Lua平均增长47.07→47.17MiB/回合，进程均+0.41GB，主要内存增长未解决。本批没有独立静置组；无需重复长测，下一建议查事件串重复遍历/事实核对，未授权新实现。见技术报告B133 native comparison。


### PT001 B134 — manual GC baseline test only
用户授权最小手动完整GC与已证实网络范围修复，见[合同/三点测试](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b134161--manual-full-gc-diagnostic-and-scoped-network-capture)。定向本地通过，实际GC仍未测；先现有存档副本冷启动初始＋两个玩家回合，比较回收后Lua基线。失败停止再试，不要求重打长测，不把Lua算作本Mod独占。B133修复保留；没有GC调参、定期清理或定域停用开关。


### PT001 B134 native GC evidence received — no repeat test
[9组18图结果](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b134-native-gc-results)：T39–45共8次手动GC均成功并降低count；T41–44回收后约317–320MiB，T45第二次降至251.51，初始250.98。诊断调用/读数所测范围USER_GAME_TEST_PASS，可回收分配已获直接证据；非全局内存修复PASS。无征服、同回合额外GC与B133条件不同，不归因三事件优化。环境串/状态未知/计时边界见报告。三点采样待办已满足，无需再长测或现在补测；PT001根因继续OPEN。只建议定域追踪分配与引用，不授权自动GC或清账本。


PT001后续定域调查完成：[最小优化候选](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b134-allocation-follow-up--scoped-investigation-and-next-proposal)为明确标记纯本玩家worker/focus，再只跳过该Cross检查；false本身包含turn/load，晚到资格复核不得误删。两城单行候选探针3→2 Audit、258→172预检、独立同回合样本仍5→7，只证明局部路径成本；最终保守方案未实施/验证，不报原生内存比例。等待实施授权，当前不新增用户测试/长测，不修改GC策略。


### PT001 B135 — pure worker notification scope
[授权实施与定向验证](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b135162--authorized-pure-worker-notification-scope)已完成，B135.162本地PASS；只跳过纯本地worker/focus的Cross检查，turn/load等保守fallback及重入/失败合并保持。部署后一次现有科研城同回合增减专家/切换焦点→确认收益→正常过1T即可；若方便顺手改变合格区域BASE看跨学科更新，不为此造局。无需GC/征服/长测；原生响应和内存改善未宣称PASS。B134诊断采样待办不重开。


### PT001 B135 native response recorded — memory remains open
[6组12图与本地引用定位](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b135-native-worker-and-gc-results)：用户确认建筑/专家收益正常，所述响应USER_GAME_TEST_PASS；不扩展Cross III独立BASE覆盖。T39→42进程10.38→10.69GB，末尾GC618.63→298.57MiB、进程10.38GB。大量可回收分配仍在，非全局性能PASS；无需补起点/长测/GC。下一步在本地追踪重复Network事实构造，具体修复另审，不自动GC或清账本。


### PT001 B137 — same-save Network isolation
[14图原生对照及GC猜想核对](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b137-native-isolation-results-and-gc-hypothesis)已收齐。READY/UI3/3/退出5/5及T39→41计数静默为所测范围USER_GAME_TEST_PASS；并非逐类Modifier收益验收。NORMAL/隔离Lua净增195.66/121.42MiB，进程均+0.22GB，MEMORY_CAUSE_OPEN。无需立即补测/长测/GC；下一建议为隔离后余下回合路径的定域只读调查，新实验另授权。正常恢复使用未覆盖原档冷启动，不保存实验结果。


### PT001 B138 — bounded stabilization / one integrated acceptance

[B138参数、一次测试与固定退出标准](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b138165--bounded-stabilization-trial)。GC运行缓解本地通过，native阶段/暂停/回收基线/进程改善待验。正常Network同存档最多10T或4次自动回收，起末进程读数＋最终GC报告；不要求重复旧长测/征服。公共业务路径未改，UNKNOWN失城补撤销反例已有定向回归。通过后“稳定化完成，剩余分配效率问题开放”，恢复功能计划；不等待定位所有分配来源、不自动实施F。剩余事项及重开条件集中在该合同末表；不得事后放宽阈值。


## B168 — 巨作启迪原生精度调查

[零档补证](Validation/Results/Specialization_B168_Zero_Control.md)已补齐T69对照：0/0.1/0.3/0.6均51.199，整数1为52.199。所测整数增量+1，小数无可见率增量；取整层次、实际累计与百分比候选仍未知。无需重做零档/四档，END未单独观察但不附加重复生命周期流程。交给调查Agent只读研究小数精度，花园仅作百分比实现参考；不启用Floor/完整L3。B169限定保存验收PASS保持。


## B172 / B173 — 巨作启迪与馆藏通知修复合并验收

新本城百分比能力及馆藏通知修复均本地完成；[一次合并session与证据边界](Validation/Results/Specialization_B173_Great_Work_Notifications_Local.md#与巨作启迪一次验收)。同次时代/作品移动顺便观察三项文化能力，不分别重复两批测试。这取代B168旧基础小数方案的后续派发，不改写上面的旧观察。无启用/END按钮、无重复默认OFF冷加载流程；实际安装版本见Status/receipt，原生未验。其它待办状态不因此自动改变。

## B175.202 — combined Dialogue first slice / B174 acceptance

Completed in the observed scope: [B175 native result](Validation/Results/Specialization_B175_Dialogue_B174_Native_Result.md). Dialogue cancellation, normal T70→T71 completion with collection changed after start, +5%/used era and user-confirmed restart persistence pass. B174 investment/Lv2 Housing are user-reported correct; Scientist −24/+24 matches the declared worker change. Engineer −4.4/+6.6 leaves +2.2 unexplained, non-blocking; no package-refresh cause or exact all-class GPP PASS established. No extra GPP test or repeat lifecycle flow. New cumulative yields/cutover remain unimplemented and need separate authorization; this does not reopen old B168 diagnostics.
