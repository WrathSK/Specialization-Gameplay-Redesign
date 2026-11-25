# 工业后续模块：调查与实施准备

## 当前范围与正式来源

[现行工业设计](../../Design/Industry.md)规定标准化、工程能力与施工队的玩法。[现行架构](../Specialization_v0.1_Architecture.md#current-authoritative-state)说明共享事实、载体、保存和消费职责。[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)记录实际构建与验收。旧检查点中的版本、待测项和资格表都对应当时的实现。

标准化的本城与网络来源共用一组载体时，网络待确认期间保留上一次实际应用的整组载体。已确认接收方退出按[现行待确认与恢复合同](../Specialization_v0.1_Architecture.md#network-pending-hold-and-confirmation-recovery)处理。

## 当前落地矩阵与直接依赖

| 要追查的行为 | 实施与验证入口 |
|---|---|
| 奇观历史、时代信用、区域和建筑模板 | [B233 历史和模板合同](#b233-implementation-contract) |
| 标准化来源、逐模板取优与旧效果退出 | [B234 实施与验收](#b234-implementation-and-validation)、[两种环境的限定实机记录](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047) |
| 工程传统研习与旧时代奇观产出 | [B235 实施与验收](#b235-implementation-and-validation) |
| 施工队来源、费用、暂停续建与施工 | [B236 发放和绑定](#b236-implementation-and-validation)、[B237 续建](#b237-continuation-and-fixed-injection-boundary)、[B238 原生生产加成](#b238-modifier-acceptance-and-industry-closeout)、[B239 暂停项目占位](#b239-occupancy-implementation) |

早期工业分批实施、测试准备及旧版模块矩阵见[固定发布版本](../../Historical/README.md#delivered-commerce-and-industry-implementation-plans-in-git-history)。区域本体的逐模板购买、原生加成的精确数值及完成归因的覆盖范围分别沿用下方所记证据。

## Current planning review and batch grouping

The Stable Advisor report `Specialization/Reports/Advisory/Industry_Plan_Review/Industry_Plan_Audit.md` was reviewed as advisory input (SHA256 `be53a41d9936e44a4bce6c5ac764eeb95ccb6e4ec2379c883419bf4718ebdd6a`; local, not yet published). Its basis was `94ce45b` / B230.257. Direct Industry source dependencies are unchanged at the current review baseline. The accepted Industry rules and G/H/I/J dependency order remain sound; the stale waiting point, one-turn-project claim and missing native leads are corrected here. This page preserves the actionable basis without making an unpublished report a recovery dependency.

Primary qualifications:

- N/E coverage must have a trustworthy starting point. An older save with no collector history cannot prove complete historical N/E by scanning held wonders. It can still support unrelated/limited checks; do not declare every old-save test invalid or require a long replay. Use a new short test campaign after IND-1 is deployed for the complete-history gate.
- Dialogue's one-turn execution and saved transaction now have scoped native evidence: [B175](../../Status/Validation/Results/Specialization_B175_Dialogue_B174_Native_Result.md) and [B177](../../Status/Validation/Results/Specialization_B177_Dialogue_Cumulative_Native_Result.md). Reuse the relevant execution pattern; Engineering Study still owns its distinct L/E eligibility, cancellation and commit semantics.
- Reuse the event-first initialization, publication and recovery lessons from [B232](../../Status/Validation/Results/Specialization_B232_Native_Review.md). No new timer/frame polling, repeated command requests, diagnostic-required activation, or initialization available only through one past load callback. Do not rewrite unrelated old modules merely because a new consumer follows this rule.
- The configured read-only gameplay DB exposes `MODIFIER_SINGLE_CITY_ADJUST_WONDER_ERA_PRODUCTION` / `EFFECT_ADJUST_WONDER_ERA_PRODUCTION`, district-specific construction and building-type purchase examples. They are STATIC_CONFIRMED candidates, not native acceptance of our new writer. The observed district-purchase effects are **all-district** effects with `Amount`; no per-`DistrictType` purchase instance was found. This does not prove impossibility and must not silently become an all-district discount. It affects the later positive per-template purchase path, not N/E, H1 or III's 0% purchase baseline. Gold/Faith eligibility remains channel-specific.

The four implemented slices and their observations are linked above. The original grouping, dependency table and proposed native steps are available in the [full published plan](../../Historical/README.md#delivered-commerce-and-industry-implementation-plans-in-git-history).

## Wonder-source reference: Detailed Wonder Reminder Enhanced

Read-only reference requested by the user. Source label `DWR_ENHANCED` means the installed Workshop item **2794603014**, Mod ID `48219711-51e7-4d25-bf91-0d557e754fd2`, declared modinfo version **1**, author Konomi. A precise upstream release beyond this installed snapshot is not established. Source-relative locators below are local evidence locators, not public source links.

| Path / symbol | Observed interface and purpose | Relevance / limitation |
|---|---|---|
| `Scripts/DetailedWonderReminder_Gameplay.lua:18–31`, `OnWonderCompleted` | Gameplay `Events.WonderCompleted(x, y, buildingIndex, playerIndex, cityID, ...)`; resolves `GameInfo.Buildings[buildingIndex]`; saves building type, completion PlayerID, plot and turn via `Game:SetProperty` | A direct completion-event lead for G. It records the event-time player, rather than deriving the completing player from today's holder. Its CityID field is commented out; coordinates are not our durable city identity. |
| Same file:11–14 and39–49, `ReadWonderData` / `Initialize` | Restores via `Game:GetProperty`; subscribes after `LoadGameViewStateDone`; exposes a read through `GameEvents.ReadWonderData` | Shows persistent history plus a UI read projection. Do **not** consume its Property, depend on the Mod, replace `ExposedMembers.GameEvents`, or copy the single-load-event initialization assumption. |
| `UI/Additions/DetailedWonderReminder_Panel.lua`, `InitializeWonderEra` | `Buildings.IsWonder`; `PrereqTech → Technologies.EraType`, otherwise `PrereqCivic → Civics.EraType`; sorts with `Eras.ChronologyIndex` | Useful for the wonder's own era, independent of the completing civilization's current era. Its default Ancient era and national-wonder filters are presentation conventions, not our accepted historical-credit rule; unresolved metadata stays UNKNOWN. |
| Same UI file, `GetWonderProgress` | Alive-major/city traversal; `GetBuildQueue():GetCurrentProductionTypeHash()`, `GetTurnsLeft()`, `GetConstructionPlot()`, `GetBuildingProgress()` | Current construction/display facts, not proof of completed history. G does not need to inherit this all-city UI traversal. |

Installed-file SHA256: modinfo `ed719aed8a8975ab20114be1731488f673f446fb6d8dfdcd00d2255292eceab0`; Gameplay `937b062a8137b869b291758c3d7087cb09dd831adf9c07b9ba0c1c252164dea8`; panel `fdbab9fd45d813dff709f8eb663c958447077bfdba762d658d9d718988601ada`. Only source inspection was performed. The event is a strong implementation lead; callback timing, repeat/load behavior and our city-reference resolution still require scoped validation. No third-party historical data is imported or treated as authoritative.

## B233 implementation contract

[Local result and one new-save native flow](../../Status/Validation/Results/Specialization_B233_Industry_History_Local.md) record the authorized IND-1 implementation; current deployment remains in Status. `IndustryHistory` owns one verified Game Property containing supported-player completion receipts and token-bound local reconciliation observations. N/E are projections, not duplicate writable counters. Initialization is tied to confirmed pristine Store startup; unknown prior history is not complete zero. Reentrant events drain synchronously; readback precedes publication. No timer, frame polling, all-city Wonder scan or third-party dependency.

The existing Store supplies supported-owner city references only. Foreign Wonder events are ignored before city lookup or recording. Lawful Industry initialization/claim, return and load readiness use the existing single-city template reconciliation entry: N is reliable retained history UNION presently existing Wonders. Unknown foreign construction/removal history is not pursued; possession never supplies civilization E. No foreign token reader, AI city identity enrollment or global building-history framework is introduced. Corrupt saved authority remains held; a current scan cannot erase or disguise it.

H1 adds typed District receipts inside the existing city template transaction; a confirmed component cannot become silently uninitialized. First initialization/re-entry unions current eligible complete Districts; later completion reads only the signalled city/District. Unique replacements normalize to accepted base families. Building knowledge, building revision and the old discount interface remain separate. AF23's structural/provenance validator now gates Store recovery; current catalog mismatch holds only effect interpretation, without remapping/deleting history. No new construction/purchase benefit, L study or Crew behavior is implemented.

The new P0 **工业历史 / 模板** report and existing bounded collector expose N/E/own eras/coverage/typed counts. Report opening is never required for initialization. The new-campaign completion → Industry/District knowledge → save/cold-load flow is accepted in [B233 native review](../../Status/Validation/Results/Specialization_B233_Native_Review.md); inherited B140/B142/Store/collector local evidence covers unchanged paths. Hold the dependent history path on uncertain save/readback; never use current possession to invent a completion owner.

## B234 implementation and validation

- **Ownership:** Store and Standardization still own permanent typed knowledge. `ReadKnowledge` validates structure/provenance without requiring every historical row to remain in today's catalog. StandardizationEffects maps each qualified current row; unclassified history is retained and reported, never erased or silently remapped. No schema/L/credit field is added.
- **Facts and propagation:** one current Industry network projection per consumer batch; each relevant source's result is reused across receivers. Template commit and successful investment explicitly notify the changed city; shared network publication/recovery, governor/owner transitions, load readiness and the existing turn reconciliation provide other boundaries. Self does not require a route; remote UNKNOWN retains only previously proved contributions from the same reference. Confirmed loss withdraws. No new timer or frame callback.
- **Temporary lifecycle:** one pending support entry per affected reference; success, confirmed reference/owner exit and load clear it. New projection records belong to the consumer, are replaced on reference change, pruned after confirmed city loss and reconstructed from current knowledge. Native carriers are effects, never permanent authority. Failure to withdraw exact old Industry effects blocks the replacement. Reentrant notification queues work for the next native publish event.
- **Cutover:** old Discount/Copy Starts enter withdrawal-only facades; their UI contexts are removed from modinfo actions while frozen definitions remain. Research NetworkBoost has no normal plan/audit writer in runtime and rejects its former test activation. Its exact initialization/ownership cleanup preserves the already-retired Culture Eureka exit; current CultureNetwork is untouched. Cleanup does not reset persistent Properties.
- **UI/evidence:** left-click **工业历史 / 模板** for retained history; right-click that same button for **工业标准化** (repeat right-click to page). The read-only report and bounded scalar trace identify current sources, matching targets, waits and, when readable, current production progress. The report never activates effects. No new standalone button or collector protocol.
- **Validation:** [B234 local result/test contract](../../Status/Validation/Results/Specialization_B234_Industry_Standardization_Local.md) and [scoped native acceptance](../../Status/Validation/Results/Specialization_B234_Native_Review.md). User steps1–3 PASS;151 contiguous records corroborate same-turn support, template propagation and recovery. Construction arithmetic and source withdrawal/recovery include explicit user observation, not an invented full log reconstruction. Native floor is observed and retained without compensation. No repeated B233 cold-load gate, unrelated Culture tests or performance claim.


## B235 implementation and validation

- **History/transaction:** [EngineeringStudyModel](../../../Mod/EngineeringStudyModel.lua) and [EngineeringStudyProjects](../../../Mod/EngineeringStudyProjects.lua) use the existing [Store](../../../Mod/CityProgressionStore.lua), with a narrow Engineering commit-visibility fence. Reliable E gates new full-turn study; completed city L survives loss/return and may exceed E. Missing established history is not initialized from current facts. Exact completion/readback, cancellation and CALLING no-replay boundaries are in the [local result](../../Status/Validation/Results/Specialization_B235_Engineering_Local.md).
- **Projection:** [StandardizationEffects](../../../Mod/StandardizationEffects.lua) remains the single per-template actual-holder MAX/cleanup owner; III10/0, IV10+2L/2L. [IndustryWonderEffects](../../../Mod/IndustryWonderEffects.lua) derives own-city ordinary Wonder production from current ACTIVE and civilization/Wonder eras, independent of N/E/L. [Definitions](../../../Mod/Data/EngineeringStudy.sql) add no purchase right or arbitrary L cap.
- **Partial writer boundary:** positive building purchase uses the existing target-specific effect; native Gold quotes now match the tested discounts, while Faith remains untested where unavailable. Target-specific District-body purchase is **UNIMPLEMENTED / USER_DEFERRED_NONBLOCKING_V0_1** (2026-10-18): only all-District cost effects are established, so no substitute is installed. District construction enhancement is delivered. Do not claim complete IV purchase coverage.
- **Events/lifecycle:** E/L commits, exact queue and current-fact/owner/era events drive scoped work, reusing native publish/load/turn boundaries. No timer/frame polling, new foreign/world-city scan or GC change. Future REALLOCATING must explicitly cancel the unfinished round when that presently unimplemented transition is introduced. Crew injection remains unchanged; its future revised integration has a separate gate.
- **Evidence:**188 scoped local tests PASS, inherited suites retained; [native review](../../Status/Validation/Results/Specialization_B235_Native_Review.md) confirms L0→1→2, L2 cold restore and Gold quotes, with user acceptance of the tested Wonder acceleration. Incremental12/14% construction arithmetic and cancellation were not independently isolated in this session. Same-turn IV-entry failure is retained for B236. Normal production selection is the intended entry; P0 remains read-only.

## B236 implementation and validation

[Actual-source evidence and minimal test](../../Status/Validation/Results/Specialization_B236_Crew_Local.md). CrewModel owns pure definitions; CrewProjects owns city admission/player grant proof/derived inventory, and CrewProjectUI bridges fresh native queue/cost/counters to one ordinary project request. Native grant returns the exact unit for persistent source/locked-capacity binding; no spawn-position inference. Existing UnitActions/UnitTargets enforce Wonder-only one-use injection and distinct investment receipts. Native CanRetreatWhenCaptured supplies the protected-unit gate. Industry institutions reuse the existing presentation rows.

User clarification: formation price locks at start; new orders use fresh qualification/N price. The new city admission and grant proof do not rewrite CityProgressionStore or existing historical ledgers. Events notify only affected own sources, with a per-flush shared native unit inventory; unchanged publications do no work. Failed/ambiguous grant is not replayed. III/IV, N-cost, two-slot, owner/return, cold source recovery and actual unit-use boundaries have212 scoped local tests, not native acceptance. Existing B235 same-turn IV delay is traced to CrewPrecision dropping the second COMMITTED receipt and repaired at that wrapper. No timers, GC changes or Culture HOLD work.

Native requires one combined formation/source/cost/occupancy/Wonder-use/protection session, with one cold-load for the new saved ownership. Current source/live/receipt and pending acceptance remain in Status/Authority. District-purchase support remains a separate technical gap; no broad substitute and no new B235-only test.

## B237 continuation and fixed-injection boundary

User approval covers the B236 two-path repair and D0052 tier-I260 /390–364–338–312 prices. Prior B236 plan/results above remain historical; current execution evidence is in [B237 result](../../Status/Validation/Results/Specialization_B237_Crew_Local.md).

CrewProjects retains an admitted native project ID, locked capacity/price and positive native per-project progress when it leaves the queue. PAUSED belongs to the same city order property; one record per native project bucket, at most20 paused plus2 active entries. Only actual queued/pending entries reserve the two slots. Resumption reuses its admission and price, reserves a slot and rebases the player-global completion counter; unrelated city completions cannot turn positive local unfinished progress into a missing grant. Confirmed zero progress may cancel; unknown progress never becomes zero. Existing source/owner validation, ambiguous-grant receipts and loss cleanup remain.

UI exposes current and retained variants separately; a paused row says“续建”and shows the locked price. Required access remains while queued/paused. New access is installed before obsolete unstarted access is removed. The writer never rewrites native progress, changes an in-flight project ID, refunds production or adds a timer.20 bounded native progress reads join the existing event-driven queue reader; no new whole-world scan. Stable DB IDs retain their old numerical suffixes; new values come from CrewModel, and completed unit capacity stays the saved asset value. Native cost must still match the saved admitted price; a mismatch is held without rewriting production. No old-build save migration is introduced.

**Historical B237 limit, superseded for current development by D0053/B238.** Fixed injection was blocked. The loaded Mac AddProgress wrapper truncates its Lua input to an integer before the ordinary native production path; an exact target-specific bypass is not established. Great Engineer production reaches the same common native path; its overflow flag is not proof of modifier isolation. No approximate normalization, repeated negative correction or third-party effect withdrawal is shipped. UnitActions rejects before reservation, receipt or debit; existing completed Crews stay intact. This safety hold is an implementation limit, not an accepted change to fixed-construction Gameplay. The result documents inspected alternatives and the remaining decision boundary.

## B238 modifier acceptance and Industry closeout

D0053 accepts applicable native Production modifiers on locked Crew base input; isolation is no longer a release condition. B238 restores the existing guarded one-use `AddProgress(min(base, remaining))` call. It keeps source binding, two slots, prices, admission/PAUSED records, receipt/debit order and no-replay boundaries. No new storage, event subscription, timer or GC work. Preview shows base capacity/input/unused base, never a fabricated exact final progress. The existing bounded observer records base input and an actual delta only while the same target remains readable; completion/target changes are not subtracted across targets. Observation failures do not change the business return or the typed investment receipt.

Future balance: compare effective amplified output with formation cost under representative Macro/policy/city modifiers. No numerical retuning, complete stacking formula, compensating negative write or universal no-overflow proof is claimed. This is a nonblocking future balance item, not player-facing text. B236 observed amplified use/no-overflow is inherited only within its tested scenario; prior B237 negative evidence stays unchanged.

| Closeout item | Current evidence / remaining action |
|---|---|
| Industry I/II support, typed templates/N/E, III baseline, study/L and IV/Macro | B233–B236 scoped user acceptance; retain the stated local/native boundaries. No repeat of old long tests. |
| Start-locked incomplete formation, new tier-I260 | B238 native continuation at14/338, post-restart resume and verified260 binding accepted. PAUSED does not reserve capacity: confirmed defect; B239 local repair reuses the old slot on resume; combined native pending. |
| Restored Crew construction, slot release and player text | User reports other checks normal; two returned uses and count2→1→0 recorded. Exact actual-delta reads are incomplete; no universal overflow or multiplier proof. Do not repeat the full construction test for the occupancy-only repair. |
| Completed-unit binding/cap after cold load; non-capture retreat | New260 binding and paused-order reconstruction observed; do not invent an unlogged enemy-contact case. Protection remains opportunistic/deferred; new COM-A persistence can share one future reload with Crew occupancy. |
| Industry institution UI | Existing B236 implementation; glance at its III/IV text during this session. No separate UI acceptance session. |
| Purchase discount on the District body itself | Unimplemented: established candidate affects all Districts, not the specific known template. User explicitly deems this rare path nonblocking for v0.1; no further investigation/test requested. Accepted Design remains recorded. |
| Faith price channel / other speeds | Native evidence absent where no legal opportunity exists; inherited model/local coverage is not native PASS. Not a new mandatory scenario for this Standard-speed closeout. |
| Standardization + future Commerce Development Investment | Additive contract retained; verify the combination when that Commerce writer is introduced, not before it exists. |
| Original unit Owner extinction / total city destruction | Existing genuinely undefined, separate boundaries; no new lifecycle policy or speculative repair here. |

Industry's main ability chain is implemented. The confirmed paused-occupancy repair is locally complete in B239 together with Commercialization; no separate Industry feature batch is needed. Named deferred/conditional items remain visible. [B238 native evidence](../../Status/Validation/Results/Specialization_B238_Native_Review.md) supersedes the pending acceptance list in the frozen local result; [B239 implementation](Commerce_Preparation.md#b239-implementation-and-validation) awaits combined native acceptance. Do not call every purchase/ownership/speed case complete.

## G：本城经验N与文明信用E不是同一账本

现行规则从游戏开始记录实际奇观完成，不要求工业身份/ACTIVE/Governor。每次可靠完成可产生：A本城真实完成记录N，以及B实际完成文明的Wonder自身Era去重集合E。城易主N随城，E留实际完成文明；征服、持有或当前时代均不等于过去完成信用。

B233 now implements the supported-player collector and local Industry-entry reconciliation described above, using existing Store references and verified save/readback. The tested native completion/restart gate is accepted. Foreign completion events are ignored; current present Wonders at lawful Industry entry can join retained city N, never supply E. Existing active/return identity limits remain; no claim of arbitrary new-Owner support, foreign identity enrollment or AI historical monitoring is made.

对于已经运行但从未收集N/E的测试存档，没有“过去已完整记录”的凭据。当前持有奇观不能反推全历史/实际完成Owner；不能初始化E=0冒充已知从开局无完成，不能用当前Building扫描伪造N完整。优先用可信创建起点的测试局验证从开局collector；若现有原生接口能可靠证明部分本地完成，只将其与可靠N历史并入，不据此补文明E。无法确认收集覆盖或历史恢复时，保持UNKNOWN/HELD，停止依赖路径，不发猜测奖励。

Local L3：未工业时完成、不同Owner的城市N/文明E分离、同Era去重/同事件幂等、转移不转E、缺失/损坏/可靠空账本及保存失败。Native最小delta：一座非工业城真实完成一座奇观→验证N/E与own Era→合法成为工业城后读取；新增持久collector需一次保存重载，但不是重跑E2所有交易/认领场景。Exit只证明历史事实，不宣称工程收益已实现。

## H：历史知识、合法来源与效率三个层次

### H1知识增量

建筑账本沿IND-TEMPLATE-006：合法首次初始化、已有可靠历史恢复、当前合格建筑并入、历史损坏四种情况分开；保留当前缺失/掠夺/拆除的可靠历史，非支持Owner建后消失且未记录的对象不猜。继承B140–B142的有限证据，不每次重验完整旧建筑生命周期。

增加typed District记录与特色base归一，在已批准区域完成/合法初始化时增量写入；不能把区域完成回调目前的建筑Discover当成已记录区域。保持模板记录范围与启用目标目录分离；City Center分组仍为建筑，不新增City Center district template；不拿Shared D目录直接替换标准化目录，不扩当前市中心组/宗教或特色权限。

Local L3：新旧typed数据、可信首次与initialized-empty/缺史、已完成区域/replacement、重复通知、合法reconcile并集不反删。Native只测新增区域记录/相应重载，旧建筑记录继承B142；这是新保存schema差异，不需要再次从头做所有E2。

### H2/H3来源与目标计划

来源包括合格工业本城self，以及共同topology实际能接收的工业来源；只在consumer过滤ACTIVE>=III。每模板T收集实际holder，再分别construction MAX与合法purchase MAX；不同模板UNION。无模板来源再高L也不能放大T。self不要求伪造路线，center/reception由NET负责，receiver不因此成为永久知识owner或递归source。

D0045原例：A L7持大学/研究所，B L2持大学/银行，C L5持工厂→大学/研究所24%、银行14%、工厂20%。旧“模板来源与全国最高效率可不同”的算法被正式取代。III来源输出建设10%/购买0%；IV建设10+2L%、购买2L%；ACTIVE不足III仅保留知识/成果、不输出。L>E仍利用全L，E只管以后研习。

construction只作用于当前合法的普通建筑/区域目标，Wonder排除；purchase只作用于该目标本来合法的Gold/Faith各渠道。已有CanStartCommand仅Gold，需要Faith对应实际资格；价格字段不证明权限。如果原生同一成本modifier可靠影响两种合法价格且不新增许可，可以复用，但须证明而非假设。归一/group/catalog不改变科技、市政、互斥、特色、宗教资格。

与Commerce R共用普通建筑Production primitive和加算证据即可：同目标20%+50%=70%，不乘算、不共享模板authority，不要求R等待全部工业。当前R未实现，H3可以先测自身真实正常Production；R落地时只补组合delta，不要求H3提前伪造正式合同。 首段可靠L0应无购买折扣；2L真实价格增强在Tradition产生可靠L后合并确认。纯fixture的L只用于模型/原语验证，不冒充正式城市成果。

Local L2/首次cutover定域L3：holder例、最高来源退出后的回退、self/network去重、非holder、非法渠道、特色目标/区域、UNKNOWN不误清、confirmed loss撤销、普通Production与成本区别。Native只补真实价格、建设progress、来源变化及新增组合，不默认旧长测/全历史。

### H正式切换的exact所有者

- StandardizationDiscount owns实际加载`SPC_B054_Targets`生成的`BUILDING_SPC_B054_<BuildingType>_<1..4>`及附件；需按加载目标导出具体allowlist。其Start/Audit/Receive/load/return/exit必须互斥，不能只换SQL留下旧selector重建。
- Retired CopyYields owned only Production：`BUILDING_SPC_B051_PRODUCTION_POS_0..15`、`NEG_0..15`、`POP_0..7`共40精确ID。退出其Gameplay.Start、COPY_YIELD_SAMPLE、Bridge fanout、load/audit/return和[CopyYieldRefresh](../../../Mod/UI/CopyYieldRefresh.lua)producer；不恢复已退Research Copy。
- 最后旧Copy consumer退出后再关闭其actual sample发送/旧控制；保留IndustrySupport的BASE producer、其它独立诊断、NET topology与无关专业。实验HalfYieldProbe的Science/Production64项及`SPC_B050_HALF_ENABLED`只在本批真实涉及时检查，不能前缀删全库。
- 原Type定义保留到确定退出，未知清理HELD；确认退出后才能正常启用新投影，普通样本延迟不反复做cutover。旧入口/load不能复活，非相关建筑/账本不受影响。

## I：三项工程能力分别接入

| 能力 | 事实与正式效果 | 保存/退出与原生差异 |
|---|---|---|
| 工程传统 | 全国E供新研习；本城IV且L<E完整1 Production Turn成功永久提交L+1；输出建设10+2L与合法购买2L | L为A城市历史、身份/ACTIVE/Owner变化保留；III仅10/0，不研习；低III不输出。未来合法Owner E<L也不截断L |
| 工程实践 | 当前IV按本城真实N0/1–2/3–5/6+成本150/140/130/120%；III始终150% | N长期保留，但收益按当前IV；只改组建成本，不强化模板/施工力，不新增槽位 |
| 巨构工程学 | 当前IV本城自行普通生产旧时代Wonder，当前文明Era−Wonder自身Era差1/2/3+给10/20/30%；当前Era无加成 | 当前派生效果、资格下降精确退出；不看N/E/L，不修改已训练队伍的锁定基础capacity；适用时原生倍率可放大投入 |

研习未完成时，Governor导致ACTIVE不足IV、Identity退出、REALLOCATING、Owner变化或正常生产中断取消本轮，不增L/不存半进度；再次合格完整重做，已提交L不变。该规则D0045已定，不再标“中断Design TBD”。

The session-only [TimedProject](../../../Mod/TimedProject.lua) prototype is not the current reusable transaction contract. [Claim](../../../Mod/ClaimProjects.lua) has scoped recovery evidence, and [Dialogue B175/B177](P0_M_Dialogue.md#current-slice--b177204-earned-projection) now has implemented project/history and scoped native evidence. Reuse the proven full-turn execution path, while validating Engineering Study's own L commit, interruption and persistence; do not import Dialogue era quotas or reward multipliers.

Tradition L3本地：L<E/L=E/L>E、完整回合/中断/Owner与重复成功、提交失败、不重复/跨加载计功、恢复只派生当前效果。Native一轮成功＋一轮真正中断后重做，新增L持久重载有具体信息价值。Practice L2本地成本阈值全矩阵，native只补一个实际成本跨档；Macro L2普通Wonder增量与固定Team隔离，原语证据不同不能一项通过算三项完成。

## J：训练成本、永久队伍、基础施工分开

### J1来源、2槽与新成本

当前[项目SQL](../../../Mod/Data/CrewProjects.sql)定义付费档位；[CrewProjects](../../../Mod/CrewProjects.lua)独占完成与返回单位绑定，原生modifier直接grant已退出。来源token／原Owner与unit保存绑定，不能按单位名或相邻坐标猜。B237补齐原项目续建，证据边界见上文。

III开放I–III，IV额外IV–V，无E4/5门槛。每训练source当前Owner的存活本城出身队伍总2槽，所有档各1；完成队伍属于独立原Owner资产，source总督/ACTIVE/Identity/Owner变化不删、不停止使用。旧Owner队伍不占新Owner来源容量，原Owner夺回重新计其旧存活队；消费/合法移除释放，活着保护撤退不释放。

| 档 | 锁定基础施工力 | III或IV N0成本150% | IV N1–2成本140% | IV N3–5成本130% | IV N6+成本120% |
|---|---:|---:|---:|---:|---:|
| I | 260 | 390 | 364 | 338 | 312 |
| II | 420 | 630 | 588 | 546 | 504 |
| III | 750 | 1125 | 1050 | 975 | 900 |
| IV | 1000 | 1500 | 1400 | 1300 | 1200 |
| V | 1360 | 2040 | 1904 | 1768 | 1632 |

均为标准速度首测值；其它速度保留已接受scaling方向，capacity锁为`floor(reference*speed CostMultiplier/100)`，最终Production/Gold/Cost需整数时按D0045 Floor，不做无必要中间Floor。Practice只改投入不改锁定capacity。native其它速度成本载体仍需验证，不能改成另一套玩法舍入。

实际修改依赖包括CrewProjects、项目/单位/动作SQL、[Probe](../../../Mod/Probe.lua)Specs、训练完成handler、Gameplay/modinfo/Text/UI直接caller；当前数字由CrewModel、对应SQL与展示共同维护，不能只改一个SQL表。`BUILDING_SPC_CREW_PROJECT_ACCESS`、五项目及`SPC_PROJECT_GRANT_CREW_<capacity>`授予附件需要逐项cutover。旧排队项目满槽/资格下降时仍能grant，是实际技术门禁；不能静默删队列、扣锤、退款或删除已完成队伍来绕过。DEV Spawn不得越新来源/库存成为正式资产，未知来源显式隔离。

Local L3：档位门槛、同回合多完成/重复通知、队列满槽、保存、Owner切换/夺回、活着撤退与合法消耗、其它城隔离。Native一个source完成两队→第三受限→合法消耗释放；新的unit-binding/source-owner路径需要定域失城/恢复或重载，不再重复E2城市身份全流程。无法证明grant/容量门禁则只停止J，不影响H或Macro。

<a id="j2目标固定注入与保护"></a>

### J2目标、基础施工与保护

正式目标只Wonder，Megaproject仅future；停止UnitTargets/UnitActions普通Buildings/Districts授权，保留Settler investment分支。[ConstructionProbe](../../../Mod/ConstructionProbe.lua)仍供正式链必要事实，不能整模块删除。

B238按D0053恢复B236的一次destroy→`AddProgress(min(base,remaining))`；B237曾因旧固定最终量规则在消费前阻断，其原结果不改；新消费确认前重验单位/目标Owner与ref、目标tile/当前Wonder/remaining/1charge及永久训练provenance/unit绑定完整性，成功才精确释放slot一次。不重新要求训练source当前Industry/ACTIVE或Owner与单位相同；来源降级、退出工业或易主均不阻止已有队伍使用。请求取锁定基础capacity与目标剩余值的较小值，允许原生适用Production倍率放大；不猜测全倍率、不归一化、不撤其它效果、不重复补差。基础投入与实测进度分开记录；余量不结转规则保留。

敌方直接capture/Owner转换已被D0045禁止，必须证明保护撤退/安全回归；`CanCapture=0`只禁本单位主动capture，不证明自身受保护。源城变化不取消已有队伍；活着回归仍占库存。未定义的是原unit Owner完全消失等具名处置，不把普通source转移又写成Design TBD。

Local L2＋涉及unit保存L3：合法/非法目标、预览到确认变化、恰好/超量、失败不消费、未知执行不重放、重复消费/slot只释放一次。Native一个带正常Wonder百分比的目标确认恢复施工及下一目标无溢出，另一个敌方交互证明不转Owner且回归；这些是新增原语，不用旧Cheat完成或CanCapture字段替代。正式可玩Exit须同时有训练/库存/使用/保护及实际入口，不能只做P0面板手动开关就称落地。

## 已确定规则、技术未知与真正未决

| 分类 | 内容 | 影响范围 |
|---|---|---|
| 已定，非TBD | 每模板holder内MAX、III10/0及IV2L、Gold/Faith合法渠道、N/E/L归属、研习中断、III/IV开放队档、2槽/Owner计槽、可受原生加成的基础施工、非捕获与Floor | 按上述当前规则实施，不重开Design |
| TECHNICAL | Wonder完成证据/创建起点/外国时期连续性、N/E/L业务保存与恢复、typed District增量、self resolver、逐渠道资格/成本效果、1T提交/中断、项目grant满槽门禁、动态成本/速度、unit绑定与安全回归、基础施工的原生加成与余量处置 | 各依赖切片；局部失败不阻塞全部工业或其它专业 |
| DESIGN未覆盖 | 原unit Owner完全消失等非普通source变化处置；城市彻底摧毁等未涵盖历史/绑定处理 | 只相应路径；不得借本计划建立统一永久资产清理规则 |
| 成熟度/Balance | 机构/队伍/研习项目候选或TBD名称，首测数值与施工受加成后的综合强度待未来实测平衡（非阻塞，不进入UI） | 不擅自冻结名称，不把首测认作最终平衡 |

模板可靠性不需要D归一化；标准化本身不是D consumer。Shared普通建筑/D目录覆盖与标准化typed目录是不同责任，不借工业准备扩HD Catalog。三处未衔接future设计边界及AI/MP范围保持，不做全城迁移/new cityKey。

## 后续验证、性能与授权

每段按直接source/consumer/state闭包读取；仅H/J正式cutover搜索全部Mod exact相关ID/callers，不通读全仓历史。共同基础hash未变可复用，新增账本与grant路径不能因为旧E2已PASS免掉本地保存/失城/重复验证。只对新增native风险追加最小实机；普通yield切片不默认保存启用态→END→冷载OFF→重新启用仪式。

普通事实复用现有EffectiveFacts与模板summary，诊断明细按需。N/E collector只在明确完成事件写增量；来源资格、模板/holder/L版本或真实路线变化才更新相关receiver。队伍registry由J负责单位退出/消费和source容量失效；pending1T由Tradition负责完成/取消/加载。缓存/队列有明确owner/失效/替换/结束，不把L或N历史为性能清掉，也不添加每帧/hover、粗粒度每城每回合一次或独立GC。

The preceding planning review was STATIC_CONFIRMED only: accepted contracts, directly relevant source and configured read-only DB, plus the installed DWR_ENHANCED reference. Only documentation/reference/context checks run in this planning task; no new gameplay simulation or native test. Future H/Macro/Practice use scoped L2; new history/template schema/L/unit inventory use the relevant L3 boundaries. B233/B234/B235 local implementation and scoped native acceptance are recorded above. B236 is now approved and locally complete; no additional B235-only test. Primary next: the single combined B236 native gate below. Held Culture work and Balance do not block it. Do not implement the whole Industry plan in one batch.

## B239 occupancy implementation

Paid paused work now reserves its original source slot; resume consumes no new admission. Actual queue cardinality remains separate. Legacy over-admitted work keeps its paid progress/cost, blocks fresh orders, and resumes only within living+queued completion capacity. UNKNOWN/unmatched queues hold rather than guessing. Existing completion receipts, source binding, Production modifiers and no-overflow behavior are unchanged. [Local result and combined COM-A flow](../../Status/Validation/Results/Specialization_B239_Commercialization_Local.md); native occupancy is pending in the one combined acceptance. No new Industry ability or purchase branch.
