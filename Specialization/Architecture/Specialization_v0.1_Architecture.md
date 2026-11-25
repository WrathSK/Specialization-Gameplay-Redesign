# Specialization v0.1 Architecture — A0192

Document Owner: Codex
Architecture Revision: A0192
Design Spec Synced Through: D0065
Design Spec SHA256: feea441aafe38687c38d55604ac27ef3c2b4433306e18afa6a51f4cb7ee30d15
Latest Accepted Design Revision: D0065
Latest Accepted Design SHA256: feea441aafe38687c38d55604ac27ef3c2b4433306e18afa6a51f4cb7ee30d15
Sync Status: D0065_SYNCED_EXPEDITION_ARCHIVE_ACTION
Implementation / live evidence: see Status CURRENT and Workflow/Authority.json; this document defines target contracts, not a parallel deployment ledger.

## CURRENT AUTHORITATIVE STATE

A0184 records the Owner-accepted convergence successor and finite workflow/current-information synchronization (2026-11-04). The reviewed evidence was published at `fcf61e2bbbd74394490cbd40af033c3e3529bf3a`; independent remote retrieval matched all 19 SHA256/byte counts. Current normative contracts below replace candidate routing. Source implementation and native acceptance remain separate in Status. That initial authorization covered PU01. Current slice and validation gates are recorded in Status.

A0186 records the Owner's engineering closeout approval on 2026-11-17 after the Stable B527 scoped audit. It synchronizes the implemented responsibilities and identifies superseded experiment descriptions; it introduces no new gameplay, save contract, recovery policy or environment promise. The closed scope is the approved convergence program on B527.554, not every future Design capability or historical document-cleanup task. Evidence and retained observations remain in [Status CURRENT](../Status/Specialization_P0_Status.md#current-authoritative-state) and the [accepted closeout record](../Reports/Proposals/Architecture_Convergence_Closeout_Review.md). Main promotion and deployment retain separate authorization.

A0187 records the subsequent narrow retirement of those three unloaded city files and the inert NetworkIsolation controller/request entries. Current network/effect owners, retained turn checks, owner-local withdrawal seams and GC protections are unchanged. This does not reopen the accepted convergence scope or authorize new save compatibility.

### 和平交割与城市身份

A0189 同步[三座 HD 港口建筑的资格](../Design/Shared.md#普通建筑与当前资格)。现有普通建筑目录提供资格和实际 Tier，区域深度与风雅熏陶沿用既有读取路径。投资面板可呈现当前商路证据中已知的阻塞原因；提示不参与签约判定。

A0188 承接[城市易主规则](../Design/Shared.md#和平受让多次转手与同址重建)。进度存储仍独占城市身份写入。首次和平受让使用交割事件提供的新主人、新城市 ID 和明确原因，核对前主人、该城的加入／初始化顺序以及对象与地块两种查询。只在交割时读取一次该城已完工的区域；认领项目沿用原有候选和结算。已登记位置优先交给原城市记录处理。

直接归还时，原标记缺失且出现 CityBuilt 的路径，需要完整的旧端点移除、新端点加入与初始化、同回合交割和已经确认的退出。和平交割还要求 CityBuilt 指向同一新端点并先于移除，交割原因由具名引擎枚举确认。现有保存字段分别记录来源与凭据版本，冷读档重新核对。三类和平原因共用该窗口，原生覆盖范围见[事件证据](../Reports/Technical/Engine_Reference.md#er09--城市换手身份与永久毁城)。外方间连续交割与永久毁城的实现边界见[当前状态](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#peaceful-city-acquisition-and-direct-return--s1125)。

### 考察团训练城易主

城市 Store 负责确认交割、原城市绑定及训练准入标记的撤除。训练控制器将它们与同一张已入队订单核对。单位侧沿用现有玩家记录保存这一结果，来源丢失通知和外方队列均不能单独解除名额。随后在事件发布结束或同构建读档边界核对该玩家的单位名册及离图间谍数量。没有出生、完成或存续凭据、名册可识别且离图数为零时，才结束预留。正向凭据、身份不明的离图间谍或取样期间出现的新通知保留名额。后续相关单位或读取接口变化可重新核对。独立单位的归档城变更沿用[既有边界](v2/P0_N_Expedition.md#v01-scope-decisions-user-2026-10-16)。[文化设计](../Design/Culture.md#四级人文考察团)

### 已成团的考察团更换归档城

城市存储确认交割后，沿现有训练退出回调核对原主人、归档城位置及城市记录标识。已成团时由单位记录保存归档失效，结束未完成任务，按原有活动协议释放本团占用的休眠。只有一次读取失败时，继续区分未确认的来源与正式易主。既有单位身份和在途抵达仍按原有证据核实。

单位面板根据已发布的状态显示“选择归档城市”。打开时才读取本玩家的城市身份，确认时重新核对所选城市、单位及这次选择所依据的记录版本。只修改该团的归档绑定；已获得的见闻及其成功名额保存在各自的城市记录。已签投资的两个未决情形与本入口无关。[玩家规则](../Design/Culture.md#来源易主与重新挂靠)

### Accepted convergence boundaries — 2026-11-04

- **Normal cold restoration:** same-build saved engine state, true history and native effects restore normally. Lua cache/index loss is not a new business event. Incomplete required facts/history/topology cannot clear, partially recompute or overwrite restored installed effects. Reconcile idempotently at the first complete consumable reliable snapshot. Reliable negative facts immediately revoke strict qualification and register passive withdrawal; an inseparable aggregate without reliable source witnesses is reconciled at that first complete snapshot, never guessed apart. Receiver invalidation retains exact priority exits. See the current network contract below.
- **Session witnesses, not derived save authority:** ODP01=B supersedes A0183's 2026-10-25 derived Commerce/Culture source-persistence permission and the old S9 wiring target, and replaces the old Standardization-only cold exception A. Use bounded reference-valid per-source session witnesses for proved warm partial failure. Do not connect old derived adapters to satisfy a retired checklist. Genuine deferred lifecycle/history persistence remains: Store retains exact opaque bytes with bounded confirmed transition evidence and executes only the original lawful transition under parent/CAS/readback protection; no idle retry or money/native replay.
- **Scoped recovery and Reputation:** D0059 SAFE-004 supersedes D0058's general irrecoverable-to-baseline permission. Isolate unsafe abilities, deterministically rebuild only from reliable authority, preserve valid siblings and visibly block an irrecoverable unsafe operation; do not silently normalize it into permanent HELD or guess history. Lawful confirmed Commerce exit resets only its required reputation fields, even if the isolated old leaf is unreadable. Distinguish confirmed R, currently inapplicable R, explicit narrow policy-zero and unsafe UNKNOWN. ODP02=A permits projection-only R0 solely for an isolated severely failed reputation leaf with reliable parent/reference and all other purpose-required facts. STABLE adds no irrelevant R dependency; new VENTURE terms lock their confirmed source/policy provenance, signed terms never change. Unknown balances/network/occupancy/payment outcomes/receipts stay strict.
- **Completion/ownership:** unique Crew request/order/source/reference/completion/unit proof remains mandatory; cumulative differences never grant. Source/order-scoped unresolved-receipt repair (PU05a) is distinct from native S7d6 attribution (PU05b). Claim Store sticky completionError/root recovery (PU07) precedes Claim admission repair (PU09). Shared queue timing never merges project eligibility, cancellation, quota or reward. Use native reliable completion first; only a proved availability gap lacking a direct signal permits a bounded already-registered local-turn pending drain, not a new poll or all-city retry. Ownership gameplay remains excluded.
- **Tier and environments:** SPC owns the meaning of loaded same-district upgrade-chain depth, not a fixed cross-environment mapping or HD-table value. Real upgrade edges/replacements increment; outside-district/virtual/non-upgrade gates do not. Industrial Water Mill is T1. A missing Tier row does not make a prerequisite ignorable; genuine missing/incomplete/cyclic/ambiguous chains report errors, with not-applicable separate. HD old values are comparison evidence. D0060 sets Hospitium and Garden to T4, records weight5 for effective T5 Data Center, and retains cap10 and the existing Research Chair T1–T4 scope. O5a assembles building definitions and Tier overrides before O1 resolves and publishes current facts. O5b runtime wiring follows O2. HD/UC companions belong to the pinned compatibility profile.
- **Delivery/start/exit:** phase0 completes synchronously; ordinary owners ACK only after registering their scoped responsibility/ticket. FAILED/SKIPPED, false, missing and throw do not consume delivery. Old ACK cannot erase a newer same-turn change; successful siblings stay idle. Successful Start declares ordinary subscriptions; explicit phase0 ranks/Bridge window and Seal/drain order remain. Mandatory fail-closed exit/return duties must be registered outside ordinary successful Start, or the unproved exit stays blocked; failed startup is not permission to leave effects or silently allow exit. Do not create an automatic discovery bus.
- **Production/diagnostic retirement:** migrate real kernel/read barriers, Flight/current GC, bindings/facts, errors, ACK and exact cleanup before genuine absence tests. Cross-profession carriers follow actual source/receiver/effect/history/reference ownership, not the city's current profession alone. Retain exact SQL/save/cleanup duties, including LegacyCleanup's real groups. Busy/throw/unconfirmed ExpeditionTraining return is not completion. No S9/S10 removal, GC policy change or historical deletion is included in PU01.
- **Support and evidence:** current-build new games and same-build saved games only; no cross-build migration promise or unbounded LEGACY decoder. Code/package rollback is not saved-history or native-money rollback. Preserve the exact full HD U5 profile for later comparisons; reduced HD is separate certification. O5 owns environment/UI-base assembly and the fixed subsequent no-HD load smoke, O6 owns concrete UI behavior/interaction and may reuse evidence. Independent no-HD DB and load-smoke evidence remain distinct; targeted final acceptance covers affected effects/UI/exits/load/irreversible paths, not merely loading/carrier readback. Native touchpoints retain separate permission.

### Environment assembly and shared depth — A0185

The approved O5a slice establishes SPC-owned, versioned definition inputs and explicit Gathering Storm profile selection. The two mutually exclusive modinfo criteria use the active HD Mod ID. The HD component contributes documented virtual-building exclusions. The common projection reads final Buildings and Districts, then records the D0060 Holy Site overrides for loaded buildings. It publishes one assembly marker only after exactly one profile and a nonempty projection. The marker describes data assembly. Ability eligibility and runtime readiness retain their existing gates.

The manifest orders schema and wrapper definitions at 10003000, the selected component at 10003010, and the common projection at 10003020. Generators at 10003100–10003150 follow the projection. Standardization base targets precede the Engineering Study levels. Development Investment project/access definitions remain independent of effect target generation. InternalCarrierPillage runs at 10004000, after the last carrier. The three SPC-owned ModifierTypes retain the existing Collection/Effect pairs and attachment arguments. Current owners continue to withdraw their exact carrier IDs.

O1 owns effective-chain resolution and the shared D fact. Resolve real upgrade edges, replacements, explicit non-upgrade gates and the two named overrides in one shared catalog. Compute depth and its cap at the fact producer. D consumers read the confirmed shared fact through its existing availability/reference boundary, with range and encoding limits handled at the appropriate effect interface. Each ability retains its own Tier eligibility or grouping when it needs that separate fact. O5a supplies inputs and preserves the existing HD Lua readers until O1 cutover.

The supported independent baseline uses official Gathering Storm content with the existing official prerequisites. The fixed HD/UC configuration remains the comparison profile. The Restructuring Team uses the base game's modern Great Merchant member/audio and official icon fallbacks, with the SPC icon overrides and gameplay unit identity. The earlier retained-Leugi requirement is superseded. The O5b startup/exit and UI-base gates precede the fixed user-run no-HD smoke. Native behavior and O6 UI checks are recorded separately in Status.

## Early convergence and pre-playtest checkpoints

These checkpoints explain the first HD Commerce slice, the original implementation contracts and B267 diagnostics. Apply their still-relevant details alongside the [current Architecture contracts](#current-authoritative-state) and [current implementation responsibilities](#系统如何组成). Check [Status](../Status/Specialization_P0_Status.md#current-authoritative-state) for the outcome and active work.

### PU01 — authorized current-HD first slice

Use the current HD provider to deliver environment-independent fact status and purpose-specific projections to the real Commerce consumer. Keep authoritative facts, current availability, per-field/domain status and actual applied output separate. A confirmed zero/negative differs from unavailable D/workers/eligibility/yield; unneeded domains must not block independent readable domains, while a required unknown cannot silently become zero. A read-only projection does not itself write carriers, history, native effects or dispatch events. Keep value and availability/ref/generation distinctions, copied values and no retained native objects. Use the existing shared synchronous read phase and real-write invalidation owner; extract only the production seam proved necessary here, not the whole O1/HD port or a temporary parallel hold framework.

**Runtime Impact Contract:** EffectiveFacts/current HD native sampling is the fact producer; Commerce owns policy/max/Floor/applied Gold. Review actual NetworkInput/Bridge and RuntimeWork/NativeFacts callers at the seam. Preserve meaningful same-reference/same-turn second changes and post-write freshness; do not add events, timers, city scans, derived persistent fields or loosen TransactionCurrent. Test actual producer plus Commerce, required D/workers unreadability, reliable negatives, independent domains, return isolation and write barriers (T02/T04/T08 plus scoped T01/T05 where affected). Run restricted Lua/package and affected regressions, record exact commands/environment/counterexamples/limits in current Status. LOCAL is not native PASS. A cold-ready contract gap or wider core/persistence/irreversible need stops that affected part for Owner review.

The full later PU/O order is preserved as [published historical planning evidence](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/fb7be65b664b78f2c692cdc9d661511f37823b2e/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/Architecture_Convergence_Integrated_Roadmap_DRAFT.md#4-ordered-slices-gates-and-rollback-boundaries), not a second current authority or permission to implement later packages. Runtime current state and the next authorized boundary belong to Status/Authority.


A0178保留D0032目标架构；D0035 Shared/Lv2澄清及[D0036模板生命周期补充](v2/P0_E2_Plan.md#b140167--industry-template-lifecycle-and-reconciliation)按当前Authority和定域合同适用，不宣称整个目标架构已实现。v0.1仅科研、文化、商业、工业；未来专业Design不扩大实施范围。

- [状态/Shared/Network/保存/展示/性能目标合同](v2/D0032_Adaptation.md)；[依赖与cutover合同](v2/D0032_Implementation_Plan.md)。
- [E2保存实现与历史检查点](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)：当前Game索引＋逐城记录，旧writer隔离；旧City Property模型不是当前production authority。
- [B232 shared network recovery contract](v2/P0_N_Expedition.md#n3culture-network与精确旧eureka退出): event-driven route proof, coherent availability-before-notification, and recovery notification without a new logical input version. Culture history changes actively notify their projection; no persistent state or Gameplay change.
- [B234 Industry projection and exact retirement](v2/Industry_Preparation.md#b234-implementation-and-validation): Store knowledge and current effect eligibility remain separate; event-driven support readiness, self/network III baseline, exact old Industry exit and user-approved v0.1 Research-network isolation preserve the common topology.
- [B235 Engineering city history and effects](v2/Industry_Preparation.md#b235-implementation-and-validation): Store owns L/receipts, study owns the full-turn transaction, existing Standardization owns actual-holder enhancement, and a derived city consumer owns older-Wonder production. Target-specific District purchase remains a technical gap.
- [B241 Capital state/transaction contract](v2/Commerce_Preparation.md#b241-implementation-and-validation): Store owns bounded contracts/n and reliable institution/owner continuity; native Treasury owns balances; current network owns source membership, UI owns no business state. Guarded reads, exact receipts and unresolved-call holds preserve no-replay semantics. Native money/settlement evidence pending.
- [B244 Capital persistence representation](v2/Commerce_Preparation.md#b244-lossless-capital-storage): model-owned DECIMAL17_V1 stores fractional terms/receipts as canonical text; Store exposes numeric copies while retaining strict raw-envelope comparisons. Confirmed-loss termination uses the same codec; no monetary, replay or generic Store guard change.
- [B246 Development contracts](v2/Commerce_Preparation.md#b246-development-investment): Store owns district-bound contracts/actual debit receipts; native UI reads current theoretical prices on explicit quotation/confirmation only. Direct outgoing network proof, real working specialists, difference-only owned Production carriers and building/Owner exits remain separate from Capital. No new timer or monetary rounding.
- [B245 bounded native money receipts](v2/Commerce_Preparation.md#b245-bounded-native-money-receipts): user-approved <=0.01 Gold per debit/credit, observed actual receipts and settled net; original terms, strict Property equality and no-replay protection remain. No old-attempt reconstruction; native acceptance pending.
- [B240 Commerce source/effect ownership](v2/Commerce_Preparation.md#b240-implementation-and-validation): D0055 matching-Identity direct partners and Harbor total Food; no recurring Gold sampling. Store selection/reputation, event-driven real changes, exact cleanup and per-domain Floor are retained; source/live/native evidence remain separate.
- 实施/验证/下一授权边界只在[Status CURRENT](../Status/Specialization_P0_Status.md#current-authoritative-state)维护；部署另需receipt，源码存在不证明已部署。
- [A–D2事件驱动传播合同](v2/README.md)及[机构/能力/carrier分层](v2/Presentation_Institution_Carrier_Model.md)继续适用；下面旧阶段状态不重启旧任务。
- 仍有效约束：后台UI当前商路桥接是已接受路径，不强求纯Gameplay枚举；UNKNOWN不等于空网；持久成果不等于当前ACTIVE/路线/载体；不能从旧临时效果补造永久历史。具体接口与证据沿E2保存记录查阅。

科研传统：Store拥有可靠年龄，F2独立consumer仅从当前身份/ACTIVE与年龄重建五档瞬时科技百分比；module-owned退出不清年龄。实际合同及证据见[P0-F科研传统](v2/P0_F_Research_Tradition.md#b144171--f2-implementation-and-validation)。本地模拟不是原生验收；当前部署/授权仍以Status为准。

巨作事实：[P0-K会话事实合同](v2/P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)复用旧UI采集/transport，Gameplay校验当前引用并发布目录资格、历史时代/馆藏与国内索引；事实层不施收益，具体新旧consumer切换见各批次合同。实机/部署门禁仍只从Status取得。

风雅熏陶：[L1投影合同](v2/P0_L1_Aesthetic.md#b148175--implementation-checkpoint)分离逐栋普通建筑贡献与实际区域原生旅游投影；ordinary身份和D/Tier资格分离。master/plot flags仅为当前效应配置，Gameplay事实是权威；原生门禁仍以Status为准。

意义延展：[B166自动接入合同](v2/P0_L2_Meaning.md#b166已授权--意义延展自动接入)复用K确认馆藏、Shared D与现有单值原语，正常writer拥有当前每城投影；旧GWA仅保留具名撤销和冻结定义，正常旧BASE采样／正向入口关闭。Probe不在正常Start启动；五产出范围／Culture延期、加载与原生证据以定域合同／Status为准。

- [B247 current Identity and restructuring](v2/Commerce_Preparation.md#b247-implementation-and-validation): original city admission/history remains intact; an explicit Store transaction projects current Identity/Potential, owns one-time liquidation and separately confirmed native consumption, and publishes committed changes to existing consumers. No general save-framework rewrite. Each profession history and signed contract keeps its own lifecycle. Event-driven native training/UI/disruption; five game turns enable explicit same-city configuration, without wall-clock timers. Native gate pending.
- [B248 training access follow-up](v2/Commerce_Preparation.md#b248-training-access-follow-up): committed investments notify the affected city; bounded read-only diagnostics separate derived access from native list eligibility. Investor art is presentation only. The reported load-time absence remains a native gate.
- [B249 event-driven readiness](v2/Commerce_Preparation.md#b249-event-driven-readiness): existing Store readiness gates one context-local initialization and reference-bound recovery. Normal Start/publication/player/city events do not require LoadScreenClose delivery; duplicate load notifications preserve live training pairs/previews. Native entry and original transaction acceptance remain separate from local regression.

### B267 pre-playtest diagnostic boundary

B267 adds read-only readiness and fixed carrier-health observers, plus Commerce turn/network/sender evidence. Initialization receipts are registered early; readiness is sampled at subsequent publish boundaries and startup is explicitly sealed. Store exposes only a scalar FreshReady getter. Existing effect writers, UNKNOWN/withdrawal rules, requests, persistence and retries remain authoritative and unchanged. Ready flags describe initialization only, never effect PASS. Missing load delivery remains observable; the carrier observer can provide a first-local-turn diagnostic baseline without repairing any gameplay service.

Meaningful records are separate from bounded optional native sampling. Identity-aware state deduplication and an explicit per-turn runaway breaker replace lifetime output loss; the collector preserves metadata and reports transport/ring gaps. Buffering is bounded and disconnected history is not guaranteed complete. The overflow prototype retains definitions and readers, but an ungranted internal building gates ordinary production availability. See the [B267 result](../Status/Validation/Results/Specialization_B267_Preplaytest_Diagnostics.md) for tests and native limits.

## 系统如何组成

这是一套同时使用Gameplay Lua、UI Lua和原生数据库效果的系统。Gameplay维护可信城市进度、验证行动并协调收益；UI读取引擎在该context公开的当前事实、呈现结果；SQL定义原生Modifier与内部载体。UI、单位和载体都不能单独充当永久专业历史。

下述为当前develop源码的定域结构核对（STATIC_CONFIRMED：代码证据，不等于实机通过），依据入口、保存/事实路由及对应实施合同。没有重新逐个审计所有能力。实际完成与验证范围由[Status](../Status/Specialization_P0_Status.md#current-authoritative-state)维护；外部运行包必须由部署记录确认。

### 运行入口与职责

[modinfo](../../Mod/SpecializationP0.modinfo)通过AddGameplayScripts启动[Gameplay.lua](../../Mod/Gameplay.lua)，通过AddUserInterfaces启动各UI context，并对城市详情等原UI作特定替换。ImportFiles只表示可载入文件，不证明模块已启动。Gameplay的include/Start建立共享模块引用；模块自己的Start/guard决定实际订阅与写入，不能用文件名中的Probe/DEV判断“只读”或“未启用”。

| 职责 | 当前直接入口/模块 | 实际边界 |
|---|---|---|
| 参与资格和引擎读数 | Probe | 测试文明/领袖、人类身份、单人模式核验；不假定人类一定是player0 |
| 持久进度与行动 | CityProgressionStore、InvestmentAction | Game侧逐城记录与投资收据；保存失败保持可诊断状态，不补造成功 |
| 当前专业事实 | CityProgressionStore.Base → EffectiveFacts → CurrentSpecializationFacts | Production reads the owned Store foundation and committed investments, then derives ACTIVE from current governor facts. The old CityFlow branch is limited to explicit legacy-test mode; its module is not packaged. |
| 普通建筑与深度 | OrdinaryBuildingCatalog、DistrictCompleteness | 单一目录/深度计算、缓存与按需明细；目录覆盖和D语义是两个问题 |
| 网络输入与共享结果 | BackgroundRoutes/NetworkSender → NetworkBridge、NetworkInput | 当前路线快照、版本/引用验证、共享派生视图；专业consumer各自解释收益 |
| 巨作事实 | DialogueRefresh → GreatWorkFacts / GreatWorkCatalog | DialogueRefresh transports current work samples; GreatWorkFacts owns receipt, acknowledgement, sample pairing and confirmed collection facts. Its shared.Dialogue slot is a retired transport record, not a separate live effect projection. DialogueProjects / DialogueEffects retain earned project history and reward application. |
| 原生收益 | ResearchSupport/IndustrySupport、Lv2Housing/GPP及各能力consumer | 模块拥有各自carrier和退出路径；保存记录不是收益快照 |
| 玩家呈现与诊断 | CityPotential、P0Panel、InstitutionOverview/Institutions | 读取已确认结果；四个当前专业的机构行读取已确认事实；B247另区分历史机构与当前能力，不代表所有玩法已通过实机验收 |

### 事实、保存与当前资格

[当前E2合同](v2/P0_E2_Plan.md#b108-authorized-new-game-multi-city-cutover--contract-before-implementation)落地为一个紧凑Game索引和逐城Game记录。索引保存分配序号/原始身份依据；每城保存自身绑定证据、首次完成、投资收据、模板历史和所有权证据。既有记录更新只写该城；它不是把所有未来专业资产塞入一个通用数据库。

[CityProgressionStore](../../Mod/CityProgressionStore.lua) production Start uses the current authority; StartLegacyTest is limited to explicit fixtures. The former Binding/Completion/Journal/Flow shells have left the runtime package. The remaining unloaded CityInheritance, InheritanceShadow and CityInheritanceRead files were removed in post-closeout B528 maintenance. Their original code remains in fixed Git history for explicit historical tests; it is not an additional production authority. Strict identity, committed permanent history, new-game initialization, partial writes and HELD/rollback boundaries retain the accepted E2 contract. Missing records do not authorize reconstructing a specialization from existing districts or adding old-version save compatibility.

[EffectiveFacts](../../Mod/EffectiveFacts.lua)从基础进度与已确认投资得到Potential，再从当前总督门槛求ACTIVE；读取失败保留UNKNOWN语义。[Standardization](../../Mod/Standardization.lua)在新模式将自身模板读写路由至进度store，仍由该模块验证模板目录和学习证据。Identity/Potential/明确永久收据与当前总督、路线、收益载体分开。

失城是确认后由各consumer撤销自身临时效果，永久记录保留；夺回需要同城证据，再派生当前ACTIVE和Network，不重放失城前快照。完整覆盖、尚未支持的销毁/重建与未专业城返回等边界见[E2保存与所有权历史记录](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)，不是无条件的全生命周期保证。

### Industry history and typed knowledge (B233)

[IND-1 contract](v2/Industry_Preparation.md#b233-implementation-contract) adds one Game-owned source for supported-player Wonder completions and local reconciliation observations. City N and completing-civilization E are distinct projections. Foreign completion events are ignored. Lawful Industry initialization/claim and return union reliable city history with presently existing Wonders, using the existing Store identity and single-city entry; this never grants conquest E credit or invents unseen foreign history. Initialization/empty/unavailable remain distinct; corrupt authority is not rebuilt from current possession.

Typed District knowledge is a separate component of the existing per-city template transaction, normalized through native District replacements. Store recovery validates historical structure/provenance independently of the current effect catalog. B234 adds a transient StandardizationEffects consumer: current ACTIVE>=III holders, local self plus verified network sources, per-template union/max and typed construction+10%/purchase0%. The legacy strict reader remains for historical fixtures; the normal Discount/Copy writers are retired. Current classification only controls effect eligibility, never deletes knowledge. B235 adds an optional city-owned L/receipt extension through the same Store transaction, a narrowly fenced reader, and cancellation/no-replay semantics. It extends the existing projection rather than adding a competing writer; no new save framework. Native limits remain in Status and the scoped contract.

### Crew formation and source assets (B236)

[Crew contract](v2/Industry_Preparation.md#b236-implementation-and-validation) keeps irreversible formation separate from presentation: city-owned admission (two active reservations plus bounded paused progress records), player-owned completion proof, returned-unit immutable source/locked capacity, and a fresh native living/queue inventory. Native completion is never inferred from a unit appearing at a city. Ambiguous creation/binding is held across load without replay; confirmed loss cancels pending source admission but does not transfer completed units. [B237](v2/Industry_Preparation.md#b237-continuation-and-fixed-injection-boundary) preserves native paused progress and locked price. [B238](v2/Industry_Preparation.md#b238-modifier-acceptance-and-industry-closeout) restores the guarded one-use Wonder grant under D0053 acceptance of native Production modifiers. Base input and actual same-target delta are distinct; completion cannot be measured by subtracting different targets. D0052 tier-I260/costs remain; no new permanent schema. Amplified strength is a future balance point, not a player-UI disclaimer or blocker. Ordinary native events and existing publication drive updates; no timer/frame poll or new Store framework. The existing observer must preserve the typed investment commit so Study/Wonder/Crew consumers receive same-turn changes. Industry institution rows consume current presentation facts only.

### Dialogue project and saved history (B175)

The first [P0-M slice](v2/P0_M_Dialogue.md#current-slice--b175202-project-and-history) adds an optional city-owned Dialogue extension to the existing per-city Store. `DialogueProjectModel` validates receipts/quota/pending transitions; `DialogueProjects` owns the exact entry marker and one-turn completion transaction. UI selection/display is not saved authority. Completion uses the existing Great Work collector/catalogue for a fresh, single-city observation with matching reference/turn, not a cached background sample.

Only pending attempts participate in normal turn work. Known pre-commit qualification/owner/production loss cancels the attempt while retaining successful history; UNKNOWN or ambiguous completion holds. CALLING is persisted before native completion, and an uncertain completion cannot be replayed or resampled after load. No new city key, AI history listener, GC strategy or generic contract framework is added. The new cumulative yield writer and old Dialogue retirement are still unimplemented; [result](../Status/Validation/Results/Specialization_B175_Dialogue_Project_Local.md) and Status carry validation/deployment evidence.

### Shared D业务事实与按需明细（B170）

DistrictCompleteness是唯一D采集/计算owner。正常收益使用`ReadFacts`：保留区域/建筑资格、tier/位置/掠夺、domainD及availability/UNKNOWN；省略name/tierSource/excluded展示树。现有`Read`从同一已确认raw延迟派生完整明细，切换模式不重复采native、不发收益或增加业务revision，返回副本独立。

raw＋compact及按需detail由同一≤8城cache拥有，dirty/ref/token/owner/new-turn/load/return规则保持；成功刷新使旧detail失效，失败保留旧确认样本且标TEMPORARILY_UNAVAILABLE。revision是业务事实版本，不是完整诊断内容identity；诊断独有变化刷新内容但不触发业务publish。

全部presence/location/pillage/queue安全读保留；因此全Building规模成本仍开放，不因拆分明细宣称原生性能改善。正常五consumer已接紧凑入口，Research/Aesthetic详细描述及Probe/Shadow仍可读完整说明。具体差分/残余成本与原生门禁见[B170结果](../Status/Validation/Results/Specialization_B170_Shared_D_Fact_Read_Local.md)，当前部署/验收只查Status。

### Store普通写与故障占用（B169）

Store仍唯一拥有提交权，完整record校验、manager旧snapshot和Game旧值比较、写锁、setter/readback及成功后复制都保留。有效引用按字段存在性选择`loss.target → current → origin`；损坏字段不静默回退。普通写在已提交引用与候选引用相同时不遍历其它record；恢复、新登记、有效引用改变仍检查唯一性。登记在index/token写前预检，record提交再次复核。无新save字段／schema／全量反向索引。

损坏record保留index、位置及原件并hold本worker；可靠端点（即使业务字段损坏）仍占用，可靠缺record保留登记端点。不可解析或读取失败的占用标UNKNOWN，只拒绝无法证明安全的新登记／引用变更；其他正常城的不变引用写可继续。加载时真实引用碰撞仍hold collection，candidate碰撞仅拒绝目标。

所有写失败（包括普通写和写前stale）以实际读回决定有限session reservation。可靠原端点不扩大保护；可靠候选端点被保留但不晋升成功；第三端点／不可解析／读取或有界Copy失败为UNKNOWN。setter抛错后仍读回一次；不盲重试。失败城的旧snapshot、永久记录不删除，重新加载依据实际可靠存储重建。session条目按held/incomplete token有界，成功确认即清除；没有新增持久账本或全城每回合限频。

[实施与验证](../Status/Validation/Results/Specialization_B169_Store_Write_Repair_Local.md)记录访问计数、逐值对照和保护反例；该计数不是原生CPU／内存证明。目标record读回现在经有界Copy，复制／校验及业务写成本仍在。提交期间候选root可见性、return回调顺序和专业业务耦合仍是原审计保留项，本批不改；部署／实机状态只从Status获取。

### Scoped investment publication (B174)

The actual Settler transaction now returns call-local final-readback evidence through both Gameplay/UnitActions entrances. A named composition function uses only COMMITTED to scope Lv2Housing and Lv2GPP to the proved city; other outcomes keep their existing player fallback. Each writer checks current reference/binding and owns its own facts batch, carriers and failure record. One consumer failure does not stop the other or replay a debit. Native hooks, cross-city Network scope, Store schema and player-wide district enumeration remain unchanged. This establishes one bounded publication contract, not a general bus or complete migration of the central consumer lists. [Implementation and measured limits](../Status/Validation/Results/Specialization_B174_Investment_Propagation_Local.md); source/live/native status remains in Status.

### 网络与跨context数据

已接受的[后台UI来源合同](../Reports/Technical/Specialization_Network_Background_Source_Decision.md)允许不开贸易窗口读取当前路线。Gameplay计数核对不是完整端点枚举的替代。路线事件使输入失效/重采，事件历史本身不是现在的网络。

[NetworkInput](../../Mod/NetworkInput.lua)结合当前城市引用与EffectiveFacts形成逻辑输入；NetworkBridge发布共享视图。版本、epoch、引用、dirty signal和样本生命周期用于拒绝旧响应，重复读取不重新捕获整城事实。UNKNOWN、暂时等待、确认失效分别处理；source/recipient资格不是永久保存成果。

[版本发布](v2/Batch_A_Input_Contract.md)、[共享视图](v2/Batch_B_Shared_Network.md)、[请求/撤销生命周期](v2/Batch_C2_Copy_Industry_Lifecycle.md)、[事件传播](v2/Batch_D2_Runtime_Propagation.md)是可复用技术合同。不同专业payload不强制套同一公式。Current Commerce, CultureNetwork and StandardizationEffects own their independent passive-effect calculations; exact old-carrier withdrawal no longer depends on the retired writers. B226已接入[文化完整文明集合并集与专家投影](v2/P0_N_Expedition.md#n3culture-network与精确旧eureka退出)，并精确退出旧文化尤里卡。B234按用户决定隔离旧科研网络鼓舞至v0.1之后；共同拓扑与科研本城能力保留，原生验收见Status。Commerce uses the direct domestic-partner projection; Capital uses proved recipient sources; Development uses proved direct outgoing destinations. Their separate qualifications and irreversible-operation gates remain in their owners.

A0190 的当前构建从数据库、启动及城市退出清单中一并移除 B055、B057、B058 三组旧科研／文化网络鼓舞建筑。公共网络的两个系数仍进入 NetworkInput 的输入签名。另属巨作试验的两座 B055 建筑继续由巨作清理负责：读档关闭或受支持玩家的回合激活可触发撤除，完成以写后读回为准。城市退出继续按该城逐组确认，正式文化网络的专家收益由原模块处理。

### Network pending hold and confirmation recovery

This accepted successor replaces B240 UNKNOWN-as-withdrawal and A0183's cold exception/derived-persistence target. D0059 [Network](../Design/Network.md#未确认不等于失效) owns gameplay; existing native receipts and formulas retain their owners.

- Topology PENDING/UNKNOWN is not empty. Preserve actual installed passive output while required reliable inputs are incomplete; do not create, remove or reconfigure from missing facts. Standardization's combined local/remote carrier is held as one applied result. Known owner/reference/identity/ACTIVE/REALLOCATING exits retain their exact scope and priority; unknown qualification is not confirmed loss.
- Same-build normal cold load restores saved equivalent engine facts/history/effects. At the first complete consumable reliable input, reconcile idempotently. Before then, reliable negative facts revoke strict eligibility and register withdrawal; if the cold physical aggregate is inseparable and no source witness exists, execute its subtraction at the first complete snapshot, without invented decomposition. No installed carrier means no synthetic old output. Old output never proves current topology or new transaction qualification.
- With confirmed topology during a warm session, readable sources contribute current facts; unreadable sources may contribute only bounded reference-valid reliable session witnesses, with confirmed/retained/unknown provenance. Confirmed source loss invalidates the respective witness. No default derived-network persistence; genuine named history and deferred lifecycle remain separate. This replaces the Standardization-only D0058 cold exception A, not the accepted formulas or true history.
- Publish coherent availability before notification. Same-value confirmation/signal recovery must wake affected consumers; availability/ref/generation differs from logical value revision. Dirty synchronously blocks strict use and leaves collection/delivery owned. Preserve same-turn second changes and exact confirmed loss; never mark a partial capture globally fresh.
- If required inputs remain unrecoverable beyond normal initialization (NET05), use the explicit no-write interim: installed output unreconciled, visible severe error, strict transactions prohibited. This selects neither permanent old payout, K-only nor clearing. Repair normal phases/facts/completion first; a genuinely unavoidable business-policy choice requires Owner decision, not idle retries or new derived saving.
- Capital/Development quote, confirmation and settlement preserve their fresh purpose-required proofs, balances, locked terms, readback and no-replay receipts. Pending passive hold cannot authorize new debit/credit or add a network condition to an already signed contract whose terms survive ordinary route/ACTIVE loss. Getters/UI remain read-only; work stays bounded by relevant reference/generation/lifecycle changes, with no polling or GC-policy change.

### 收益应用与玩家呈现

Research Infrastructure, Interdisciplinary Research, Applied Learning and Academic Chair retain their formal consumers and [cutover contracts](v2/README.md#收益应用与精度). Exact SQL and each owner govern native writes and withdrawals; no broad BUILDING-prefix deletion is permitted. StandardizationCatalog / StandardizationEffects now identify, withdraw and read back the exact B051/B054 industrial carriers before applying current effects. LegacyCleanup owns the transferred purchase, old Great Work, Commerce, level-three and Dialogue cleanup groups; current Culture owners retain their assigned exact withdrawals. CopyYields, StandardizationDiscount and NetworkBoost are absent as Lua writers, while required SQL definitions and permanent histories remain. See the [responsibility matrix](v2/D0032_Implementation_Plan.md#明确的旧效果切换责任) and current Status for scoped verification.

“每人口可产生小数”不证明“区域/每专家平坦收益可任意小数”；科研两条floor实现分别是汇总后取整、每专家取整，不能推广成全系统精度规则。具体原生路径与用户接受范围见[技术精度证据](../Reports/Technical/README.md#收益精度与原生效果)。

The [Institution/Ability/Carrier separation](v2/Presentation_Institution_Carrier_Model.md) remains the contract. The [Research display prototype](v2/U1_Presentation_Prototype.md) describes its historical HD-only checkpoint. Current modinfo selects environment-exclusive official / HD UI bases for UnitPanel, CityPanel, CityPanelOverview and ProductionPanel; institution, timed-project and unit-action adapters read current module results. Presentation does not own gameplay state or remove real buildings. Coverage and language-layout observations remain scoped in Status; an old prototype limitation is not a current implementation matrix or proof that every UI path is polling-free.

B251 extends the selected-city institution surface: all configured levels of the **current** profession are visible, with unestablished rows explicitly treated as previews rather than persisted institutions. Historical other-profession rows retain actual established levels. A guarded Store scalar projection supplies retained history/counts to the existing presentation request, without lazy template initialization, native fact scans or writes; UI summaries and signatures remain disposable mirrors. Unknown reads do not become zero, and Standardization distinguishes this city's source offer from recipient effects. No new update scheduler or save schema. See [B251 contract and checks](../Status/Validation/Results/Specialization_B251_Institution_UI.md#read-and-lifetime-contract).

### Runtime integration contract — P01–P10

This contract supplements the existing event-driven, ownership and exact-exit obligations. It governs new or widened automatic paths and scoped repairs; it does not declare the legacy implementation compliant or authorize unrelated migration. Use the [Runtime Impact Contract and T gates](../Workflow/README.md#runtime-impact-contract-and-targeted-gates) in the existing batch plan.

| Rule | Required contract |
|---|---|
| P01 — One owner | Declare one authoritative owner for each fact and effect. Reuse its public projection; distinguish semantic reuse, collection reuse, snapshots and caches. Shared sampling does not unify ability eligibility or pillage policies. |
| P02 — Cause and scope | Preserve verified cause, owner, city/reference and fact domain through the actual consumer. Reject irrelevant work before deep reads. Explicitly bound UNKNOWN fallback; retain foreign former-holder exits and cross-city dependencies. A scoped wrapper around a whole-player implementation does not satisfy this rule. |
| P03 — Invalidation and delivery | Review producer mutation/invalidation together with every affected consumer's scheduling and exit. Coalesce redundant recomputation, not ordered transactions or real same-turn changes. Internal-carrier prefix filters alone do not prove that all resulting native notifications are harmless. |
| P04 — Usage compatibility | Re-review on a new consumer, manual-to-automatic use, wider working set/frequency, a new recovery path or longer reference lifetime, even if shared bytes are unchanged. Bound the affected closure; do not require an unrelated platform rewrite. |
| P05 — Work and retention | State bounds for retained state AND executions: dispatches, audits, city visits, captures, native reads, allocations/report trees, effect writes and diagnostics. Test warm working sets around capacity boundaries; an eviction bound alone is not a work bound. |
| P06 — Recovery | Give pending work an owner, reference/generation, size and attempt budget, meaningful wake conditions and success/failure/load/exit disposal. Availability recovery may wake work even when values do not change. Publish drains eligible pending work; it does not create endless retries. Successful siblings do not rerun without a new cause. Irreversible transactions retain their own readback/no-replay rules. |
| P07 — Consistent sharing | The existing default remains one synchronous Audit with isolated return copies and no native-object retention. Cross-consumer reuse requires an explicitly accepted read-phase/write-barrier contract: reference/epoch, value and availability versions, relevant invalidation and post-write freshness. Do not cache partial/UNKNOWN reads as success or cross mutation boundaries silently. U1 D-15 authorizes Primary to specify the exact S5 fields/lifetime and prove them with real producer/consumer tests; a new major tradeoff still requires user decision. |
| P08 — Retire responsibilities | Review writers, readers, collectors, transport/ACKs, diagnostics and cleanup independently. Move production duties before removing a Probe/retired module; retain exact owned-ID/former-holder cleanup and uncertain native readback. File names and disabled positive effects do not prove a module dispensable. |
| P09 — Observer cost | Include diagnostic native reads, copying and formatting in the work model. Normal reports consume published results; deeper inspection is separately bounded. Log deduplication does not eliminate the reads used to produce identical logs. |
| P10 — Executed proof | Inspect direct, aliased and forwarding callers and execute real producers plus representative real consumers. Preserve same-turn changes, UNKNOWN, recovery and exits. A stub that accepts a scope parameter is not proof of locality, and local work counts are not native memory attribution. |

**Evidence-driven defensive engineering.** Implement the supported native contract and its normal path first. A defensive error branch or a theoretically possible failure is not evidence that the failure occurs in supported normal engine operation. Normal initialization, availability recovery and post-load reconciliation are part of the normal path, not the additional recovery machinery constrained here. Add extra recovery machinery, persistence, fallback or retry only for a concrete source defect, a version/context-qualified engine limitation, a reproducible case or other reliable evidence; record the hazard, affected scope, owner, minimal protection, recovery trigger and exit condition. Preserve unique irreversible-operation evidence, idempotent receipts and historical integrity, including the accepted S7d6 late-duplicate/attribution proof gate; do not relax that evidence standard merely because native incidence is unmeasured. Do not infer successful unit creation with a randomly lost result from an InitUnit nil/error branch, or add unit-count/set snapshots, automatic regrant or a generic recovery state machine without supporting evidence. UNKNOWN/root-cause and production/diagnostic-isolation obligations remain unchanged.

**Scoped exception, in the existing batch record:** rule and exact path; reason/accepted precedent; allowed cause and owner/city scope; work and retention bounds; safety and targeted test evidence; dependency/lifecycle re-review trigger; disposition and authority. An exception does not transfer automatically to new consumers. Primary resolves ordinary implementation choices within the approved contract; widening a contract, exception or gameplay/persistence rule requires the applicable user decision.

### 公共更新与临时状态接入约束

B138稳定化补充既有事件驱动合同，不重建事件总线。新/修改运行路径在本轮方案中简述以下三类信息；已有清晰接口/约束可直接引用，不要求每批重写架构说明，不新建每模块manifest或长期记忆系统。

| 职责 | 接入要求 |
|---|---|
| 变化原因、范围与依赖 | 区分worker/focus、普通建筑、总督、路线、ownership、load/回合核对；仅使用已核实原生参数缩小player/city范围。全国/跨城输入必须显式传播；UNKNOWN不能当空值、无变化或确认foreign。来自内部carrier的通知只按模块已确认的定域过滤。保留同回合真实变化，禁止每城市每回合一次粗限流；必须顺序处理的状态转换不得按普通收益重算去重，不因方便默认扩成全玩家/世界扫描 |
| 计算事实与展示 | 正常计算只取能力所需的权威事实；完整建筑明细/文本按需生成。RuntimeWork的事实/区域索引仅在同一同步Audit内复用；不能跨收益写入、ownership通知、下一事件/batch复用。失败不缓存部分枚举或UNKNOWN为成功；重读资格不得复用过期ACTIVE，不删除必要的副本隔离。新增consumer优先复用公共事实路径，不另复制一套全城采集；只扩展本批必需能力 |
| 临时状态生命周期 | 每个cache/pending/session由创建模块拥有；明确key、上限或当前世界基数、覆盖/失效、完成/失败、load/退出条件。成功ACK、失败、超时和隔离/退出释放本模块待处理引用。旧epoch拒收；派生快照、UI或carrier不是永久authority。没有明确失效和退出合同，不跨事件增加缓存。队列/订阅同样明确拥有者、替换与退出；检查内部内容及间接引用，防止重复注册、无变化写入、无界诊断历史和无法完成的重试积压。永久账本/必要历史不为内存表现清除 |

现有`RuntimeWork`保留保守foreign回合核对：GPP易主时原生carrier读取UNKNOWN会保留待撤销配置，之后foreign回合读数恢复才能补撤销。把所有foreign事件丢弃会破坏此路径。B135只对明确pure-worker/focus原因跳过无关Cross通知，mixed/UNKNOWN/turn/load及发送失败保留；不能将false泛化成所有consumer均不需更新。

[六组定向测试](../../DevelopmentTests/test_b138_update_contract.py)覆盖实际RuntimeWork范围、同步batch隔离/失败重试、实际GPP失城UNKNOWN→外国回合撤销、同回合变化及UI原因重入/失败重试。证据为LOCAL_SIMULATION_PASS，不是引擎分配量测量。本轮未改这些业务算法；后续接入若涉及相同路径，应复用相关断言，而非默认全历史stress。

[GC试运行](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#b138165--bounded-stabilization-trial)是独立可撤销缓解：`PerformanceCounters`单协调器拥有session开关、pending、阈值和有界结果。请求深度与Claim只读busy仅阻止已知重入；Publish不是全引擎事务完成证明。没有永久Property清理/全局GC参数改动，也不能用GC代替上述生命周期职责。原生结果、部署及恢复开发门禁只由Status/该验收记录管理。

#### 结项后的实现与回归边界

以[d147faf专项结项记录](../Reports/Technical/Specialization_B129_Event_Memory_Investigation.md#non-specialization-late-save-control-and-stabilization-closure)为证据起点，实际运行基线查Status所引部署receipt，不从文档HEAD猜测。保留已处理的静置、重复工作和GC触发问题及所测缓解证据；未启用本Mod的旧档也有增长，但不同存档不能相减，本Mod零泄漏/零额外成本及剩余增长全来自外部均未证明。剩余未归因增长不再作为专项验收门禁，不以补旧长测、截图或全面归因为功能开发前置。已确认旧问题按本批涉及路径处理，不要求先迁移全部旧模块。

- **GC变更边界：** 维持当前部署策略的默认状态、阈值、冷却、唯一执行入口、错误/超时锁停及加载就绪兜底。业务模块不得另加完整GC、每帧/每事件回收、全局GC参数修改或强制清缓存。调整必须独立说明症状、证据、预期代价与最小验证；不能提高频率掩盖重复工作，也不能无证据移除有效缓解。耗时锁停阈值是异常保护，不等于可接受的日常卡顿预算；GC读数不是效率的唯一指标。
- **按风险验证：** 沿用[W0004 L1/L2/L3](../Workflow/README.md#w0004-v1--quota-efficient-validation-policy)。不涉及公共事件/生命周期/高频计算的局部修改不默认做进程内存长测。运行路径改动复用相关回归，核对所涉及的同回合变化、重复通知及退出/加载边界，只补可能变化的工作量观测；不默认跑全部历史测试，不改无关失败断言。上文六组测试按受影响范围复用，本地计数/行为一致性不升级为原生内存改善或完整玩法验收。
- **最小原生验收：** 只有本地不能回答的关键问题交用户实机，默认合并为本批一次最小验收，优先现有有界日志/自动记录而非逐回合截图。追加测试须指出上一轮的具体歧义、区分方法及不同结果会改变的决定；“多观察一下”不是长测理由。
- **比较口径：** 先说明计数范围、采样阶段、GC策略和负载，按改动选少量已有指标：触发/执行、城市访问/事实采集/写入、可比回收前后读数/频率/耗时或用户停顿。不要求每批全指标，也不建高开销常驻诊断。新增功能允许有与新增工作对应的必要成本；不能以局部步骤降幅掩盖整轮工作量未变。不把不同存档阶段的进程内存直接当版本成本；不相加共享/范围不明Lua读数或称其为本Mod独占，不用进程增量减Lua增量计算原生泄漏。不设未经验证的统一零增长标准；门槛提前说明，失败后保留原结果。
- **定域重开与退出：** 可比基线下可重复的明显回归、相近负载初始化后多次回收基线持续恶化、具体无界保留/重复执行/任务积压/退出缺陷、GC触发/耗时/失败恶化，或崩溃/严重卡顿/明显内存压力，可触发定域调查。已确认可安全修复的缺陷不必等全部根因证明。先说明问题、主要假设、最小区分动作及停止条件；一批结束须归为已修复、升级到明确的定域动作或非阻塞保留，不以“继续调查”自动开启泛化排查。单次进程上涨、不同阶段占用不同、未归因增长或少量可优化分配不单独触发全项目停工；具体风险尽量只阻塞依赖该路径的功能。

剩余事项继续使用原报告/Status，只记录具体证据、相关路径、重开条件和下一批影响，不将所有猜测变成必清待办。相关技术债随已授权批次定域处理，不扩大无关重构；按既有审批边界完成批内必要调查、实施和验证，不逐小步重新请求实施许可。扩大范围、新Gameplay决策、永久数据/保存语义变更仍须明确用户决定。本节只补齐后续接入/验证约束，不是新Gameplay或性能调查授权。

### 目标合同与尚未落地部分

> 此处保留早期目标合同及当时的实现范围。四专业的已落地职责见[系统组成](#系统如何组成)，现行支持边界见[现行合同](#current-authoritative-state)。

[目标状态模型](v2/D0032_Adaptation.md#canonical-state-model--target-contracts-not-implemented-schemas)包含Historical State、REALLOCATING、专业永久成果与长期合同；这是依赖这些能力时必须满足的职责，不是当前已存在的全部保存schema。新通用cityKey、资产重组及Commerce长期合同，不能从旧模块同名或Game存储存在推断完成。Culture城市见闻已由CityProgressionStore保存；B226仅复用该历史派生当前网络，不新建长期记录。B175仅完成上方Dialogue项目/历史首段；科研传统实际实现见本页专属入口。各专业Legacy保持独立，未决项不由架构类推。

[总实施计划](v2/D0032_Implementation_Plan.md)解释依赖与切换策略；[E2检查点](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)记录当时的保存实施和验证边界；[技术spike](v2/D0032_Technical_Spikes.md)记录未来必须验证的接口。目标文件中的旧“推荐下一批”是当时规划，授权只从Status及用户明确决定取得。

## 仍适用的限制与重要反证

- [事件批次反证](../Status/Validation/Results/Specialization_B105_E2_Event_Boundary.md)：首个Publish不能代表完整建城/转移事务结束；[FOUND_CITY证据](../Status/Validation/Results/Specialization_B106_E2_Found_City_Pass.md)只覆盖所测路径。
- [身份/丢史限制](../Reports/Technical/Specialization_Load_History_Ambiguity.md)：现有区域、名字或单独坐标不是旧专业历史；当前严格身份策略见E2合同。
- [精度、UI延迟与接口限制](../Reports/Technical/Specialization_Implementation_Caveats.md)保留原场景；科研后续精度结果沿技术索引读取，不用旧局部成功覆盖新路径失败。
- [性能milestone证据](../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)支持所测短时idle改善，不证明55GB长局问题根因已解决。事件驱动、重复事实不重复发布、按需诊断继续适用。

[已接受的 U1 重构边界](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Architecture/Specialization_v0.1_Architecture.md#u1-refactor-fault-and-mechanism-boundaries--a0182)

[历史全文](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Architecture/Specialization_v0.1_Architecture.md)
