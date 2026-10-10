# P0-M —「时代对话」项目与持久倍率准备计划

State: FIRST_SLICE_SCOPED_NATIVE_PASS / B175_PROJECT_HISTORY_RESTART_CONFIRMED / NATIVE_ONLY_MULTIPLIER_NOT_IMPLEMENTED。
Authority: Spec D0049 / Culture D0049 `CUL_L3_DIALOGUE`、`contracts.dialogue/work_pool` / Shared D0045具名A/E/F；用户已授权并实施首段项目/历史；后续倍率与cutover未授权。实际基线与顺序见[文化准备入口](Culture_Preparation.md)。

## Current slice — B175.202 project and history

User-approved M1 is locally complete: real **时代对话** production entry, one-turn timer, START Game Era quota, completion-time X, +5×X city history, cancellation and duplicate/readback protection. [Scope, evidence and one combined B174 test](../../Status/Validation/Results/Specialization_B175_Dialogue_Project_Local.md). Source/deployment/native status is maintained in [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state), not inferred from this plan.

This first slice stores actual accepted city history but **does not yet project the new cumulative yield multiplier**. Old Dialogue yield/transport remains in place. The project/ledger native gate and later native-only effect gate are separate. No N/U2, old-writer retirement or general project framework is included.

The Store owns the optional Dialogue extension and a missing-history witness; the pure model validates it. Gameplay owns exact entry marker, saved pending attempt and completion. UI owns only intent/read/display. Normal turn work visits pending attempts; only load/Game Era change reconciles all local entries, and fresh completion sampling is target-city only. A held completion cannot later substitute a changed collection; loaded CALLING is not replayed. No additional GC or general event bus is introduced.

Inherited Claim/high-cost-project evidence is retained; combined local coverage remains 63 methods/66 subtests. [B175 native feedback](../../Status/Validation/Results/Specialization_B175_Dialogue_B174_Native_Result.md) now supports normal entry/1T, cancellation without quota and completion using the collection changed after start (X=1, +5%). The user confirms +5% and the used era survive restart; that load observation has no new screenshot. Other local/inherited boundaries are not promoted to native PASS. B174 investment/Housing and Scientist response are recorded separately; Engineer attribution remains non-blocking UNKNOWN. No repeat Probe lifecycle/GPP test. Stop for review before the separately authorized multiplier/cutover slice.

## 完整Gameplay合同

当前Culture Identity且ACTIVE≥3，通过同名项目连续占用一个完整城市生产回合。已接受高成本真实项目路线；正常结束与下述异常强制completion例外分开，不拿普通低成本项目近似。

每座城市×**启动时Game Era**最多成功一次，不按完成时代、不按Owner重置，不囤积过去未用机会。完成时取当前合格馆藏时代数X，增加`5×X`永久百分点；5为初版系数。X0允许成功且消耗机会。启动不锁馆藏，期间移动作品会改变完成时X。

累计历次加算，**无额外累计cap（NO_ADDITIONAL_CAP）**；5%×X是v0.1首测值，不是最终平衡。累计倍率、used START Era和成功去重凭据是**城市历史**，不按原Owner分区，随城市保留。ACTIVE<3、退出Culture或REALLOCATING暂停当前收益但不丢已成功历史；任何受支持Owner恢复Culture且ACTIVE≥3后按当前事实使用，非支持Owner冻结使用/增长。新作品获得本城倍率，移走作品不带走倍率。

合格作品采用当前共同work_pool：明确支持的著作、音乐、雕塑、肖像、风景、宗教艺术及文物；Relic、Product、Wonder、未知Mod作品/不可靠时代排除。同类别不自动等于目录已支持；时代取可靠作品历史时代，创作者关联需经验证，文物取自身时代，不以玩家/取得时代代替。

优先只提高合格巨作**原生产出（含旅游）**。Meaning追加基值独立且不得被Dialogue放大；D0048允许原生主题化作用于追加，作为v0.1暂行首测规则／Balance待验，不在本M计划另建主题倍率。相同YieldType仍不能让Dialogue合并放大追加。若只能可靠实现Tourism-only，正式Content允许报告并区分后采用该fallback，不能本计划默认为最终路径。百分比效果接受原生floor、无补偿；即使整数收益没变，UI仍显示累计百分比。这项许可不适用于L2/L3小数。

## 已验项目路线可以复用什么

真实高成本项目→正常结束生产回合→下一次本地回合阶段调用`FinishProgress`→原生completion确认，是已验原型。后续`ClaimProjects`还提供每城persisted timer、开始前/完成前城市引用验证、CALLING先落盘以防重入、cold-load续接/1T显示等实现结构。它不要求空生产队列，也不需要处理其它回合blocker或Shift+Enter绕过。

旧empty-queue、负AddProgress清overflow等失败路线不重新打开。已有项目接口的测试只按[B123所测范围](../../Status/Validation/Results/Specialization_B123_Project_Pass.md)及[Claim核心结果](../../Status/Validation/Results/Specialization_B126_Claim_Core_Pass.md)复用；不宣称全部Production injection、队列顺序或Dialogue业务已通过。

`TimedProject`仍是session单城实验；`ClaimProjects`有正式持久续接，但其UNASSIGNED资格、Claim receipt与失城时清claimTimer都是Claim业务。**不能直接把Dialogue写成Claim项目，或复制Claim清空语义来决定文化历史。** 用户为高成本项目原型接受了奇特方式强制同回合完成不做额外保护、原生completion用于发奖的明确决定；保留其真实适用范围，不另加防Cheat体系。新Dialogue的同回合强制completion与quota/reward边界在实施前对照该接受记录及完整生产回合合同核对；本计划不把强制completion当成已证明完整生产周期，也不自行覆盖既有用户例外。

## 业务保存与读模型

B175首段已在现有可靠E2 city record增加小型Dialogue专业块，分别保存：城市累计百分点、已成功START Era集合、当次项目身份/当前引用、启动回合与Game Era、连续占用/已完成调用阶段、唯一completion凭据。字段按直接合同在本批确定，不新建cityKey/通用Contract对象。

- **城市owned历史：** cumulative＋used era＋completion dedup，不按原Owner分割；不得从旧动态25%载体推导累计或给旧值迁移奖励。
- **当次计时：** 属于E未完成事务，不是永久倍率。完整连续生产回合且永久成功提交前，ACTIVE<III、Identity退出、REALLOCATING、Owner改变或正常生产中断，均取消本次轮次：无奖励、无成功START Era额度、无可恢复半进度。恢复合法资格后，若额度仍可用，重新完整执行一回合。load只恢复尚合法且可靠保存的事务，不能复活已取消轮次或因打开列表才“开始”。
- **派生effect：** 当前资格＋可靠ledger＋native-only路径。载体、Tooltip、UI选择状态不能单独发奖或保存次数。
- 发奖前验证current owner/ref、完整周期和completion证据、未用START Era、完成时confirmed X。一次保存累计＋quota＋凭据，先确认永久写入再派生modifier；重复事件/load不重奖。
- Completion阶段若馆藏UNKNOWN，不猜X0，不消耗机会；保留可证明的待结算事务。必须取得能归属于**完成边界**的confirmed X/版本，不可等待到后续馆藏变化后用新的当前X替代；若不能可靠证明该时点，停止该结算路径并记录TECHNICAL_INVESTIGATION_REQUIRED。不能无界重试、超时当成功或将重载变第二次项目。待结算尚未永久提交时，同样执行上述取消条件；HOLD不能绕过已确认取消。
- 损坏/缺失历史显式HOLD，不用当前馆藏或旧carrier“重建完整历史”。在现有Store专属validate/read/write中维护，不用独立本机文件保存。

## 已定语义与真正技术门槛

D0045已关闭累计cap决策，D0042已关闭未提交项目取消语义；不再把它们列为DESIGN_DECISION_REQUIRED。Dialogue与文化见闻都是各自独立的城市历史，不能继续用“见闻归原主人”解释差异。完整连续周期、completion、取消与永久提交的可靠事件顺序仍需技术证明，尤其不能把未提交前的资格丢失当普通收益去重。

当前`DialogueModel`仍按25%×max(0,D−1)动态投影，旧`Dialogue`资格仍是Culture ACTIVE4；**不是新M**。旧D档表达当前时代多样性，不能直接承担永久累计倍率。新累计的原生表达不得自行夹断或加一个方便实现的cap；做不到时报告具体技术限制。

B165已有加载集合STATIC证明、五项即时固定值与所测END原生证据；主题化×2已暂接受并按D0048同步，Balance待验；正旧AUTO／精确追加结算仍开放，Culture追加暂隔离。M继承这些实际范围，再验证新累计载体，不将旧动态倍率probe等同新M，也不重复共享harness仪式。旧B059.82只有非主题化作品读数，整城Culture未变，不证明真实结算或native-only隔离。

E2已有可靠同城映射可复用，不能靠名字/单独坐标/猜CityID。城市彻底摧毁等Shared尚未涵盖边界保留为局部待定，遇到直接依赖才提出；不扩成当前M整体阻塞，也不以AI休眠为由清掉城市历史。

## 建议小切片与精确退休

| 切片 | Goal / 依赖 | 不包含 | Exit |
|---|---|---|---|
| M计时/ledger门禁（B175本地完成） | 复用真实项目、可靠city mapping；START Era quota、完成X和dedup持久记录；实现已接受的取消/提交顺序，原生待验 | 正式新倍率、旧Dialogue退休、所有Production来源全追踪 | 开始/中断/下一回合/cold-load、多城、重复及保存错误明确 |
| M native-only门禁 | 核对所有原生作品yield路径、支持类型过滤，联用L2追加值作隔离 | 自动採用Tourism-only/改L2语义 | 原生作品增幅、追加不被放大、当前城市限定被证实 |
| M正式cutover | 上述技术门槛通过，使用已定无额外cap/取消规则与正常资格读模型 | 考察见闻/Network/其它专业Legacy | 业务本地通过＋一次最小原生；停于M |

每切片实施前单独固定范围/授权，不一次部署三个未知变量。可以合用现有文件职责，但禁止把旧单城实验当完整永久系统。

cutover只清旧Dialogue的动态D档、TEST25/50/100及其保留的旧B055测试owned列表，核对实际SQL附件/Start/load/manual/ACK路径；不前缀清建筑。新ledger不由它们初始化；旧writer确认撤销后启新倍率。

**K仍依赖DIALOGUE_SAMPLE和共享后台槽位collector。** 将旧收益writer与采样/ACK分离，保留确认事实与有界pending；旧`Dialogue.Receive`转兼容传输职责或明确最小替代，不简单停Start使ACK重试积压。当前GWA仅在单城probe期间hold，global cutover尚未完成。按实施时实际L2状态保留传输与writer隔离，不能提前假定GWA已退休；不动L1/L3或旧Culture Eureka。

预计涉及`ClaimProjects/TimedProject`可复用小接口、专属Dialogue model/Store专业块/consumer/SQL，选择确认与项目1T UI，Gameplay/modinfo、诊断、本地测试。真正共享改动须核对Claim直接调用点并做其回归，不创建通用项目引擎。

## 事件、性能和回滚

普通采集只取X/validity/引用，作品明细仅按需。待计时项目维护有界active集合，玩家回合阶段只处理这些事务；没有计时则不扫描每城项目，不按每帧/hover启动/发奖。项目选择是意图，Gameplay确认队列后才开始；UI display从confirmed timer读取。

Production changed/completed、目标切换、城市生命周期、load、quota/累计写入分别声明原因；顺序转换不能被收益去重合并。原生completion可能重入：持久CALLING先写，不能异常后再次无条件FinishProgress。未知引用HOLD，confirmed loss先退出owned effect，历史保留。

回滚需检查本批新增专业块schema是否被旧包认识；能保留惰性新记录则保留，不删永久历史来回退。若旧包不能安全读取则使用实施前存档副本＋对应Git/receipt恢复点，明确不兼容边界；不承诺任意旧版本互读。

## 最小验证与门禁

W0004 L3，但仅相关项目/Store/重复/保存及native-only回归，不默认全历史stress。

本地矩阵：跨START/完成Era、同城第二次拒绝、X0/X变化、低/高Production、overflow/chop/native强制完成区别、切走再回、多个并行城市、duplicate/reentrant/存盘失败、cold load、UNKNOWN完成样本、owner/ACTIVE变化、旧writer退出及Claim不回归。明确覆盖永久提交前取消无额度/无半进度、成功后暂停不删历史；不能靠fixture发明Shared未覆盖处置。

未来native按新增差异分配：同一馆藏城开始→移作品改变完成X→正常一回合成功→同START Era拒绝重复，证明新取样/额度；一次未提交取消后完整重做，证明新取消路径。新增专业持久块需一次有明确保存状态的load边界，证明累计/额度或进行中事务恢复；不机械同时重跑二者及probe默认OFF/END/re-enable。新增累计载体的真实收益与Meaning隔离只补B165未覆盖差异；跨Owner仅在该子批实际接入时安排最小历史/quota验证。每子批实施前固定一段连续session及必要持久性边界，本批仅派发上方结果中的合并最小流程。

诊断显示启动时代/已用、计时状态、当前X/待确认、累计%/无额外cap、优先/技术fallback、native实测范围。不要堆Property/令牌；异常再展开。Exit不将计时probe成功或旧百分比实测升级为完整M。

来源：[正式Culture](../../Design/Content/Culture_D0049.json)、[项目调查](../../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md)、[既有E2保存合同](P0_E2_Plan.md#current-slice--recovery-and-action-routing)、[旧百分比实现](../../Reports/Technical/Specialization_B059_Dialogue_Implementation.md)、[旧非主题化读数及结算限制](../../Status/Validation/Results/Specialization_B059_82_Percent_User_Result.md)。

生命周期依据：[Shared D0045](../../Design/Content/Shared_D0045.json)、[D0042接受记录](../../Historical/Design/Reviews/Long_Term_State_D0042_Review.md)。仅首测强度仍需Balance观察，本轮无新Gameplay决策请求。
