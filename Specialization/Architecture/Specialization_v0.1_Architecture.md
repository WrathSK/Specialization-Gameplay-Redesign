# Specialization v0.1 Architecture — A0161

Document Owner: Codex
Architecture Revision: A0161
Design Spec Synced Through: D0032
Design Spec SHA256: d6abded36a2036b73d691ecdb5bf44432beb36875646a307ba25c117b98244b9
Latest Accepted Design Revision: D0032
Latest Accepted Design SHA256: d6abded36a2036b73d691ecdb5bf44432beb36875646a307ba25c117b98244b9
Sync Status: TARGET_ARCHITECTURE_ADAPTED_RUNTIME_PARTIAL
Implementation / live evidence: see Status CURRENT and Workflow/Authority.json; this document defines target contracts, not a parallel deployment ledger.

## CURRENT AUTHORITATIVE STATE

A0161保留D0032目标架构；D0035 Shared/Lv2澄清及[D0036模板生命周期补充](v2/P0_E2_Plan.md#b140167--industry-template-lifecycle-and-reconciliation)按当前Authority和定域合同适用，不宣称整个目标架构已实现。v0.1仅科研、文化、商业、工业；未来专业Design不扩大实施范围。

- [状态/Shared/Network/保存/展示/性能目标合同](v2/D0032_Adaptation.md)；[依赖与cutover合同](v2/D0032_Implementation_Plan.md)。
- [E2当前切片及实际保存合同](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)：当前Game索引＋逐城记录，旧writer隔离；旧City Property模型不是当前production authority。
- 实施/验证/下一授权边界只在[Status CURRENT](../Status/Specialization_P0_Status.md#current-authoritative-state)维护；部署另需receipt，源码存在不证明已部署。
- [A–D2事件驱动传播合同](v2/README.md)及[机构/能力/carrier分层](v2/Presentation_Institution_Carrier_Model.md)继续适用；下面旧阶段状态不重启旧任务。
- 仍有效约束：后台UI当前商路桥接是已接受路径，不强求纯Gameplay枚举；UNKNOWN不等于空网；持久成果不等于当前ACTIVE/路线/载体；不能从旧临时效果补造永久历史。具体接口与证据沿E2当前路由查阅。

科研传统：Store拥有可靠年龄，F2独立consumer仅从当前身份/ACTIVE与年龄重建五档瞬时科技百分比；module-owned退出不清年龄。实际合同及证据见[P0-F科研传统](v2/P0_F_Research_Tradition.md#b144171--f2-implementation-and-validation)。本地模拟不是原生验收；当前部署/授权仍以Status为准。

巨作事实：[P0-K会话事实合同](v2/P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)复用旧UI采集/transport，Gameplay校验当前引用并发布目录资格、历史时代/馆藏与国内索引；事实层不施收益，具体新旧consumer切换见各批次合同。实机/部署门禁仍只从Status取得。

风雅熏陶：[L1投影合同](v2/P0_L1_Aesthetic.md#b148175--implementation-checkpoint)分离逐栋普通建筑贡献与实际区域原生旅游投影；ordinary身份和D/Tier资格分离。master/plot flags仅为当前效应配置，Gameplay事实是权威；原生门禁仍以Status为准。

意义延展：[B166自动接入合同](v2/P0_L2_Meaning.md#b166已授权--意义延展自动接入)复用K确认馆藏、Shared D与现有单值原语，正常writer拥有当前每城投影；旧GWA仅保留具名撤销和冻结定义，正常旧BASE采样／正向入口关闭。Probe不在正常Start启动；五产出范围／Culture延期、加载与原生证据以定域合同／Status为准。

## 系统如何组成

这是一套同时使用Gameplay Lua、UI Lua和原生数据库效果的系统。Gameplay维护可信城市进度、验证行动并协调收益；UI读取引擎在该context公开的当前事实、呈现结果；SQL定义原生Modifier与内部载体。UI、单位和载体都不能单独充当永久专业历史。

下述为当前develop源码的定域结构核对（STATIC_CONFIRMED：代码证据，不等于实机通过），依据入口、保存/事实路由及对应实施合同。没有重新逐个审计所有能力。实际完成与验证范围由[Status](../Status/Specialization_P0_Status.md#current-authoritative-state)维护；外部运行包必须由部署记录确认。

### 运行入口与职责

[modinfo](../../Mod/SpecializationP0.modinfo)通过AddGameplayScripts启动[Gameplay.lua](../../Mod/Gameplay.lua)，通过AddUserInterfaces启动各UI context，并对城市详情等原UI作特定替换。ImportFiles只表示可载入文件，不证明模块已启动。Gameplay的include/Start建立共享模块引用；模块自己的Start/guard决定实际订阅与写入，不能用文件名中的Probe/DEV判断“只读”或“未启用”。

| 职责 | 当前直接入口/模块 | 实际边界 |
|---|---|---|
| 参与资格和引擎读数 | Probe | 测试文明/领袖、人类身份、单人模式核验；不假定人类一定是player0 |
| 持久进度与行动 | CityProgressionStore、InvestmentAction | Game侧逐城记录与投资收据；保存失败保持可诊断状态，不补造成功 |
| 当前专业事实 | CityFlowProbe.SupportFacts → EffectiveFacts → CurrentSpecializationFacts | 从保存authority取得基础与投资，结合当前总督派生ACTIVE；旧Flow写入路径在新模式受阻 |
| 普通建筑与深度 | OrdinaryBuildingCatalog、DistrictCompleteness | 单一目录/深度计算、缓存与按需明细；目录覆盖和D语义是两个问题 |
| 网络输入与共享结果 | BackgroundRoutes/NetworkSender → NetworkBridge、NetworkInput | 当前路线快照、版本/引用验证、共享派生视图；专业consumer各自解释收益 |
| 巨作事实 | DialogueRefresh → GreatWorkFacts / GreatWorkCatalog | 会话资格、时代、位置和国内索引；旧Dialogue独立投影保留；GWA在B166源码退役，新Meaning消费确认摘要 |
| 原生收益 | ResearchSupport/IndustrySupport、Lv2Housing/GPP及各能力consumer | 模块拥有各自carrier和退出路径；保存记录不是收益快照 |
| 玩家呈现与诊断 | CityPotential、P0Panel、InstitutionOverview/Institutions | 读取已确认结果；机构显示目前有科研原型，不能当成四专业完整UI |

### 事实、保存与当前资格

[当前E2合同](v2/P0_E2_Plan.md#b108-authorized-new-game-multi-city-cutover--contract-before-implementation)落地为一个紧凑Game索引和逐城Game记录。索引保存分配序号/原始身份依据；每城保存自身绑定证据、首次完成、投资收据、模板历史和所有权证据。既有记录更新只写该城；它不是把所有未来专业资产塞入一个通用数据库。

[CityProgressionStore](../../Mod/CityProgressionStore.lua)正式Start使用新authority；历史StartLegacyTest只供显式测试adapter。旧Binding/Completion/Journal/Flow仍有文件和调用外壳，但正常新模式的写入、加载扫描及迁移入口受guard隔离。未知/旧档不因“没有记录”就从现存区域反推专业；新档初始化资格、部分保留写入、HELD及回滚支持范围以完整E2合同为准。

[EffectiveFacts](../../Mod/EffectiveFacts.lua)从基础进度与已确认投资得到Potential，再从当前总督门槛求ACTIVE；读取失败保留UNKNOWN语义。[Standardization](../../Mod/Standardization.lua)在新模式将自身模板读写路由至进度store，仍由该模块验证模板目录和学习证据。Identity/Potential/明确永久收据与当前总督、路线、收益载体分开。

失城是确认后由各consumer撤销自身临时效果，永久记录保留；夺回需要同城证据，再派生当前ACTIVE和Network，不重放失城前快照。完整覆盖、尚未支持的销毁/重建与未专业城返回等边界见[E2当前切片](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)，不是无条件的全生命周期保证。

### Store普通写与故障占用（B169）

Store仍唯一拥有提交权，完整record校验、manager旧snapshot和Game旧值比较、写锁、setter/readback及成功后复制都保留。有效引用按字段存在性选择`loss.target → current → origin`；损坏字段不静默回退。普通写在已提交引用与候选引用相同时不遍历其它record；恢复、新登记、有效引用改变仍检查唯一性。登记在index/token写前预检，record提交再次复核。无新save字段／schema／全量反向索引。

损坏record保留index、位置及原件并hold本worker；可靠端点（即使业务字段损坏）仍占用，可靠缺record保留登记端点。不可解析或读取失败的占用标UNKNOWN，只拒绝无法证明安全的新登记／引用变更；其他正常城的不变引用写可继续。加载时真实引用碰撞仍hold collection，candidate碰撞仅拒绝目标。

所有写失败（包括普通写和写前stale）以实际读回决定有限session reservation。可靠原端点不扩大保护；可靠候选端点被保留但不晋升成功；第三端点／不可解析／读取或有界Copy失败为UNKNOWN。setter抛错后仍读回一次；不盲重试。失败城的旧snapshot、永久记录不删除，重新加载依据实际可靠存储重建。session条目按held/incomplete token有界，成功确认即清除；没有新增持久账本或全城每回合限频。

[实施与验证](../Status/Validation/Results/Specialization_B169_Store_Write_Repair_Local.md)记录访问计数、逐值对照和保护反例；该计数不是原生CPU／内存证明。目标record读回现在经有界Copy，复制／校验及业务写成本仍在。提交期间候选root可见性、return回调顺序和专业业务耦合仍是原审计保留项，本批不改；部署／实机状态只从Status获取。

### 网络与跨context数据

已接受的[后台UI来源合同](../Reports/Technical/Specialization_Network_Background_Source_Decision.md)允许不开贸易窗口读取当前路线。Gameplay计数核对不是完整端点枚举的替代。路线事件使输入失效/重采，事件历史本身不是现在的网络。

[NetworkInput](../../Mod/NetworkInput.lua)结合当前城市引用与EffectiveFacts形成逻辑输入；NetworkBridge发布共享视图。版本、epoch、引用、dirty signal和样本生命周期用于拒绝旧响应，重复读取不重新捕获整城事实。UNKNOWN、暂时等待、确认失效分别处理；source/recipient资格不是永久保存成果。

[版本发布](v2/Batch_A_Input_Contract.md)、[共享视图](v2/Batch_B_Shared_Network.md)、[请求/撤销生命周期](v2/Batch_C2_Copy_Industry_Lifecycle.md)、[事件传播](v2/Batch_D2_Runtime_Propagation.md)是可复用技术合同。不同专业payload不强制套同一公式。当前仍保留部分旧专业consumer；未来Culture集合并集、Commerce不同方向资格不能仅凭这些基础设施存在就宣称已接入。

### 收益应用与玩家呈现

科研基础设施、跨学科研究、学以致用、学术主持已有正式consumer和各自cutover合同，见[v2收益应用导航](v2/README.md#收益应用与精度)。原生效果通过精确SQL定义和模块自有写入/撤销落地；旧效果按所属切片退出，不按BUILDING前缀全城删除。当前尚启动的CopyYields、Dialogue、GreatWorkAdjacency、CommerceConvergence等旧consumer不能被误称为新冻结设计的全部实现，其退出责任见[迁移矩阵](v2/D0032_Implementation_Plan.md#明确的旧效果切换责任)。

“每人口可产生小数”不证明“区域/每专家平坦收益可任意小数”；科研两条floor实现分别是汇总后取整、每专家取整，不能推广成全系统精度规则。具体原生路径与用户接受范围见[技术精度证据](../Reports/Technical/README.md#收益精度与原生效果)。

Institution/Ability/Carrier的[分层目标](v2/Presentation_Institution_Carrier_Model.md)与[科研显示原型](v2/U1_Presentation_Prototype.md)分开：原型挂接HD城市详情、追加累计机构展示、过滤该surface已确认科研城的技术载体显示；不删除实际Building，也未完成所有专业、历史机构或所有Tooltip界面。hover使用展示内容，不建立新的Gameplay扫描请求。已有其他UI路径的轮询不能据此宣称全部消除。

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

[目标状态模型](v2/D0032_Adaptation.md#canonical-state-model--target-contracts-not-implemented-schemas)包含Historical State、REALLOCATING、专业永久成果与长期合同；这是依赖这些能力时必须满足的职责，不是当前已存在的全部保存schema。新通用cityKey、资产重组、Culture永久对话/考察记录、Commerce长期合同和Research学术传统，不能从旧模块同名或Game存储存在推断完成。各专业Legacy保持独立，未决项不由架构类推。

[总实施计划](v2/D0032_Implementation_Plan.md)解释依赖与切换策略；[当前切片](v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)限制现在做什么；[技术spike](v2/D0032_Technical_Spikes.md)记录未来必须验证的接口。目标文件中的旧“推荐下一批”是当时规划，授权只从Status及用户明确决定取得。

## 仍适用的限制与重要反证

- [事件批次反证](../Status/Validation/Results/Specialization_B105_E2_Event_Boundary.md)：首个Publish不能代表完整建城/转移事务结束；[FOUND_CITY证据](../Status/Validation/Results/Specialization_B106_E2_Found_City_Pass.md)只覆盖所测路径。
- [身份/丢史限制](../Reports/Technical/Specialization_Load_History_Ambiguity.md)：现有区域、名字或单独坐标不是旧专业历史；当前严格身份策略见E2合同。
- [精度、UI延迟与接口限制](../Reports/Technical/Specialization_Implementation_Caveats.md)保留原场景；科研后续精度结果沿技术索引读取，不用旧局部成功覆盖新路径失败。
- [性能milestone证据](../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)支持所测短时idle改善，不证明55GB长局问题根因已解决。事件驱动、重复事实不重复发布、按需诊断继续适用。

## 历史实施记录

保留原阶段合同与证据链接；下文“当前/未实现/下一轮”是当时状态。与新目标或后续切片相冲突的实现描述只作历史，不取代当前源码与Status。

P0-D3 B086.113：[学术主持逐建筑writer](v2/P0_D3_Research_Chair.md)已实现并本地验证；原生建筑归属/收益仍待实机。共享事实/Design不改，不进入下一批。以下旧进度为历史。

P0-D2 B085.112：[学以致用整数专家投影](v2/P0_D2_Research_Apply.md)，用户明确每名floor、原生工作科研专家结算；本地通过，实机待验收。A0161目标/Design未改，P0-D3不开始。以下旧实施进度为历史。

P0-C B081.108 [科研基础设施正式writer/cutover](v2/P0_C_Research_Infrastructure.md)已完成本地验证及用户整体实机验收（回复“Pass”；未单独报告边界不扩大）。用户明确单学院环境，先前多学院门禁不再阻塞；A0161目标合同未变。四新bit载体、旧48无效tombstone、简明按需诊断，非目标能力保持。以下实施前门禁段落为历史状态。

P0-C已授权，当前[原生专家收益门禁](v2/P0_C_Primitive_Gate.md)待关闭；仅离线计算/SQL候选验证，正式writer和旧48效果尚未切换。A0161目标不变、运行B080不变；以下“P0-C未开始”属于前次状态。

Current implementation delta: [P0-B2 Lv2 qualification](v2/P0_B2_Lv2_Qualification.md), B080.107 LOCAL_SIMULATION_PASS / native pending. D0035 Shared/Lv2 scoped review supersedes older header navigation without claiming full Military adaptation. A0161 target contract unchanged; P0-B1 user PASS, P0-C not started. Following B079 paragraphs are inherited pre-B2 history; actual live state is Status-owned.


P0-B1 B079.106已完成本地实现：[基础专家支持及精确retirement合同](v2/P0_B1_Specialist_Support.md)。现有A0160/A0161目标不改，Design D0032不改；本批将基础支持接入当前事实/BASE样本，旧III支持writer只保留清理门面，12旧ID成为无收益tombstone。其他旧能力不随本批退役。无新carrier/Property/存档schema。

P0-A B078用户确认D和专家读取正确、刷新声消失，掠夺未测。新按钮文字待B079视觉确认。Shared D与Research shadow继续只读，不是P0-C收益。P0-B2/C/E未实施。当前live B079.106、main B069.96；[安全部署记录](../Status/Validation/Results/Specialization_B079_Deployment_20260918.md)确认126文件hash及B078恢复点。

### Historical A0160 planning gate


D0032 Architecture Adaptation / A0160 已完成文档与静态审查，**GATE B — READY FOR P0-A**。这是目标架构，不代表B076.103已实现新Design。推荐第一批为区域完善度权威事实＋现有专业状态只读适配＋科研基础设施纯影子consumer＋按需诊断；不写收益，等待用户单独授权。

当前权威：Design Spec D0032；Commerce/Industry D0032，Research D0031，Culture Gameplay D0029，Shared D0028，Culture Era Presentation D0032。Design字节未改。Runtime保留B076.103，main B069.96；本批没有代码、部署或新实机验证。A–D2性能合同继续适用，原Batch E未实施。

- [状态 / Shared / Network / Presentation合同](v2/D0032_Adaptation.md)
- [实际runtime及KEEP/ADAPT/REPLACE/RETIRE](v2/D0032_Runtime_Archaeology.md)
- [实施依赖 / 批次 / cutover / save门禁](v2/D0032_Implementation_Plan.md)
- [技术spike门禁](v2/D0032_Technical_Spikes.md)
- [完整源码索引及hash](v2/D0032_Runtime_Inventory.json)
- [本轮静态验证](v2/D0032_Validation.md)

上述文件是D0032目标架构入口；以下旧条款保留为历史runtime合同/证据。与新Design目标冲突时，不以旧条款推翻Design；实际代码尚未切换时，也不能把目标文档当作已部署事实。PAC累计presentation-only原则继续有效，其旧能力映射由当前各专业canonical取代。

### Historical B076 / PAC record


B076.103为`av2-runtime-b076.103` Runtime milestone，已临时部署；A–D2完成，短时idle实机范围与桥接ACK未完成疑点见Status，E未开始，main保持B069.96。不能据此关闭55GB长局根因问题。

新Presentation原则：[Institution / Ability / Carrier调查 PAC-I001](v2/Presentation_Institution_Carrier_Model.md)。用户确认三层语义分离；用户进一步确认PAC-R0002：机构随永久Potential累积，ACTIVE只影响能力；每个机构解释本阶段新增能力。采用presentation-only条目，不是真实Building；具体UI接入待审阅/授权。不得默认一个Modifier载体对应一个可见建筑；机构排除普通Tier/Infrastructure Value/标准化，技术bits保持隐藏，Tooltip按能力而非Modifier组织。优先事件驱动缓存+按需显示，保护Runtime milestone。永久性、累计展示、presentation-only已定；命名成熟度、具体UI落点及状态样式仍见报告待审项。D0025与Mod字节不变。

### Historical C2 implementation


B075.102：[Architecture v2 C2](v2/Batch_C2_Copy_Industry_Lifecycle.md)完成Copy/Industry独立完整批次、single-flight/ACK、reference/epoch校验、temporary hold及确认撤销，本地通过、未部署。主线A→B→C1→D1→C2→D2→E；D1已获接受，C2待审阅，D2/E未做。63组正常载体map与B074一致，D1等回归通过。Design D0025及精度/公式不变，不宣称内存问题修复。

### Historical D1 implementation

B074.101：[D1](v2/Batch_D1_Discount_Propagation.md)无关通知早停、批次共享Network事实已获用户审阅通过。C2未修改Discount/Network，旧工作量断言仍通过。

### Historical C1 implementation

B073.100：[C1合同](v2/Batch_C1_Discount_Lifecycle.md)single-flight/ACK/样本完整替换与确认撤销已获用户审阅通过。此前留给D1的扫描工作见当前增量，历史报告不倒改。

### Historical B072 instrumentation batch

B072.99增量：[Runtime Audit合同](../Reports/Technical/Specialization_B072_Runtime_Audit.md)。独立UI观察器只在LocalPlayerTurnEnd读取固定Counters累计差值/已有Network metadata，输出8×4MiB TSV轮转；io/os能力缺失或写入失败即禁用，无Gameplay请求和扫描链。native文件sink未实机验证，不能承诺已可追溯整局。main B069.96不变；当前live为此前获准的B071.98，本轮未部署。Yield Precision仅加入[架构待办](v2/Yield_Precision_Backlog.md)，C/D/E不实施。

### Historical: Batch B完成时说明

develop Batch B共享Network派生视图已完成本地验证：[cache owner/key/query/lifetime及结果](v2/Batch_B_Shared_Network.md)。沿用已接受Batch A完整事实合同，每玩家/VERIFIED inputVersion一次派生，National/ConnectedKinds/RecipientSources/Read共享；返回副本。UNKNOWN保留与确认撤销不变。事实捕获扫描及consumer监听仍未缩减，不表示55GB根因已解决。没有部署，main/live仍B069.96。

### Historical: Batch A实施说明（已获用户接受；共享cache由B取代）

develop Batch A已实现并本地验证：[完整输入版本/发布/撤销合同](v2/Batch_A_Input_Contract.md)。仅Network合同层；共享cache、UI样本协议、消费者listener及保存迁移未实施。事实相等不发布，确认失效正式撤销，UNKNOWN保留最近确认输入。Design D0025不变；没有部署。

AV2-I001为B069.96调查快照，实施差异以Batch A增量为准。main仍A0149/B069.96；此A0151只属于develop。

2026-09-14 workflow：以[部署合同](Playtest_Workflow.md)与根AGENTS为准；下文历史“不commit/push/停止长局”不再派发当前任务。

### Stable B069.96既有验证记录（本轮未改变）

B069.96现为用户指定的v0.1 Playtest Baseline；用户继续长局，main冻结玩法，develop承接后续开发。此前性能短测没有回传完整计数证据，不能标为已解决或实机PASS；风险留在Playtest Backlog按严重程度分诊。普通非商人任务不再发商路dirty；无法可靠识别时只NEEDS_REVALIDATION，保留最近完整验证状态。完整快照内容相同不发布、不增加topology revision、不通知收益消费者。读取失败最多3次本批尝试；明确端点/商人消失、战争或读取失败后的原生数量下降仍会撤销。失败包不覆盖已验证完整集合，发送只允许单个in-flight，ACK后空闲UI通知不再调用sender。

STATIC_CONFIRMED（源码静态证据，非实机）：全部SQL/数值/Design不变；继承三模块逐字节保留且未启用；其它模块仅添加固定计数/原调用转发。未实现shared derive缓存或扫描重构。LOCAL_SIMULATION_PASS（本地Lua模拟，不等于游戏通过）：真实后台collector/sender/receiver与Commerce模块的10次已知/未知单位事件、相同输入零建拆/Property/发布/derive；真实路线增删、端点失效、读取失败有限重试、请求重入/拒绝ACK、跨回合；固定schema模拟10000回合不增加容器节点数。

Performance Counters为固定条目current/total/previous/peak；新增两个纯读取诊断入口。计数为本Mod直接Lua原生调用，不包括其它Mod或引擎内部Modifier的Property写。独立自动runtime log未启用：未验证安全的Civ VI文件写入/轮转接口，按用户J10/J12回退为Counters+手动Snapshot，禁止用永久Property或无限print替代。无自动日志文件要求。

USER_GAME_TEST_REQUIRED：仅短测[普通单位移动前后与一回合计数](../Status/Validation/Specialization_B069_User_Tests.md)；这是保留的未验证案例，不再要求用户暂停长局或现在重测。UI/性能/架构后续工作仅在develop按授权推进，ownership仍隔离。完整[实现说明](../Reports/Technical/Specialization_B069_Performance_Phase1.md)。

### HISTORICAL：B068.95 UI修订（暂停继续验收/微调）

B068.95为UI小修：用户已实机确认两种单位紫色滤镜、左上诊断入口位置通过（USER_GAME_TEST_PASS）；按钮文字为空为USER_GAME_TEST_FAIL。改为显式Label并初始化SetText，保留原回调；城市潜力移到同一WorldTrackerHeader诊断入口下方，仅显示“工业1级”等四字符短文本，仍代表永久Potential，悬停信息不变。

本机UserInterface/Localization日志未直接证明空白根因，未找到Lua.log，不将导出登记通过。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：6个UI/版本文件变化，108个运行文件不变，实际UI mock/语法通过。USER_GAME_TEST_REQUIRED仅新文字及短标识位置，已通过的滤镜不重测。[结果与最小验收](../Status/Validation/Results/Specialization_B068_95_Result.md)。

### HISTORICAL：B068.94初版界面

用户批准进入v0.1 playable UX polish。B068.94只修改展示与诊断，核心保持B067.93；无玩法、数值、Design、自动继承恢复或32次限制变更。

Potential未创建真实建筑：HD按建筑枚举存在副作用风险，按用户允许的安全替代方案采用原生城市面板只读标识。真实EffectiveFacts/Property仍为权威；选中城市显示四档名称与永久潜力。诊断入口移到WorldTracker header右侧，15只读主入口，长报告可滚动，旧实验控制和UnitSites常驻入口隐藏。原有投资/施工确认流程不变，合法目标改紫色原生高亮；日志直接输出Lua.log，重复UI错误保留首条与次数。

STATIC_CONFIRMED（静态证据，非实机）：94个既有文件不变，Gameplay仅新增独立只读展示分支；D0025 hash不变。LOCAL_SIMULATION_PASS（本地模拟，非实机）：Potential1–4/切城、目标去重/清理、日志去重、15入口以及既有机制/SQL/隔离回归。USER_GAME_TEST_REQUIRED：真实HUD位置、tooltip、紫色层颜色/切换兼容和Lua.log输出；不将本轮参考截图登记PASS。

[实现与兼容性报告](../Reports/Technical/Specialization_B068_Playable_UX.md)，[最小三项验收](../Status/Validation/Specialization_B068_User_Tests.md)。完整恢复点local/before-b068；不commit/push。当前等待用户顺手验收UI，不重发核心能力测试。原32次新城/通用资格/所有权仍隔离或未来事项。

### HISTORICAL：B067隔离完成时状态

用户确认当前可玩范围只考虑自行建立且不易主的城市；累计32次新城绑定列未来处理，通用ELIG暂缓，整体验收由用户游玩中进行，不追加测试批次。界面整理等待用户给要求，必须保留可进入的诊断入口或日志证据。此为实施/验收顺序，不修改D0025征服/资格玩法设计。

B067.93已隔离所有权实验：Gameplay不再Start CityInheritanceRead/InheritanceShadow/CityInheritance，清空对应shared入口与OnPermanentCityWrite，故不再注册这三模块监听、写影子账本或调用继承Resolve覆盖。源文件/manifest ImportFiles和既有Game备份不删；恢复辅助函数保留但没有运行调用入口。普通收益模块原有路线端点撤销事件不移除。SHADOW按钮暂保留布局但返回明确暂停提示，不报模块缺失；其它P0诊断继续可用。D0025时代对话25%、商业四及既有核心收益不变。

LOCAL_SIMULATION_PASS：实际Gameplay隔离段、暂停按钮ACK/无city与ledger访问、三模块未Start、shared回调/覆盖为空；核心前批回归和25%模型/SQL检查通过。不是新原生PASS；按用户要求不新增实机测试。整体验收由用户游玩中完成。

当前收尾只有：等待用户界面要求，整理玩家可读专业/网络/投资信息与可进入的诊断层；版本/已知限制说明；完成后复核默认AUTO和测试开关、建立经用户授权的checkpoint。日志可记录错误/主动读取/关键变化，不周期全扫描或每帧打印。32次和通用资格不重新插入当前任务；未来专业不扩大。见[诊断与收尾评估](../Reports/Technical/Specialization_B067_Isolation_and_Diagnostics_Plan.md)。无新Design Revision、commit/push。

### HISTORICAL：B066范围评估与继承过程（不再派发测试）

B065用户口述“没有问题，继续推进”，事件回调本批USER_GAME_TEST_PASS。无新截图或具体参数，不能把口述扩大为所有事件形状均已确认。见[结果](../Status/Validation/Results/Specialization_B065_User_Result.md)。

B066.92实现已有Identity的转移登记与返回恢复：加载结束后，仅CityTransfered(newOwner,newCityID)可定位实际新端点，或HD已有CityConquered(newOwner,oldOwner,newCityID,x,y)形状可校验时处理；未知形状/来源歧义不猜。Game登记当前Owner/CityID、转移revision和完整来源快照；未启用Owner为DORMANT，不恢复City记录/收益；启用Owner时验证已有Identity、FLOW完成、无pending投资和目的地无冲突，按明确字段重建City Property，保存原UID/first/投资凭据/模板，恢复现有读链并重算ACTIVE。重复事件不叠加，不复制路线集合。

Binding.Resolve新增对已确认继承绑定的读取入口，CityJournal/CityFlow增加严格恢复入口；Shadow允许仅已APPLIED的同UID新端点同步，下一次转移使用更新后的账本。CityBuilt遇原址不同端点注销旧关联；不在load仅凭坐标推断转移、不在CityRemoved立即删成果。尚未切换为全局新UID生成器/所有写入的单一权威账本；原32城DEV绑定限制、缺史旧城、无Identity Claim仍后续。部分投影失败保留PROJECTING与错误，不能宣称多次Property写入原子。

LOCAL_SIMULATION_PASS：真实继承模块+EffectiveFacts验证AI阶段无City写入，返回后3凭据→Potential4、Governor2→ACTIVE2、模板保留，重复事件/加载不写、连续转移/最新快照、原址新建注销、pending和冲突拒绝；前批回归保留。真实CityFlow恢复/游戏事件顺序及实际收益为USER_GAME_TEST_REQUIRED，不能用模拟代替。

USER_GAME_TEST_REQUIRED：[B066最小测试](../Status/Validation/Specialization_B066_User_Tests.md)：同工业城转给AI→取回→读档，最多3图。用更新前易主前存档；不自动追认此前未被本模块登记的历史转移。D0025/时代对话25%不变，无新设计决定，无commit/push。

### HISTORICAL：B065修复与待测记录（现已口述通过）

B064三图已复核：Game备份INDUSTRY/3笔投资/6模板在赠送AI及重载后保留，重载写入0，USER_GAME_TEST_PASS仅此范围。事件总序号始终0且InheritanceShadow.lua74报function expected instead of nil；注册成功但callback未执行。保存原因SELECT说明此前自动加载备份未被证明。见[结果](../Status/Validation/Results/Specialization_B064_User_Result.md)。

B065.91修复：去掉table.unpack依赖，safe(fn,...)直接通过pcall转发参数；兼容缺unpack且保留nil/false/0。完整堆栈只写Lua.log，面板显示短错误码。修正Probe/XML漏留B063.89的标题，当前明确B065.91。D0025和时代对话25%不变，不接正式继承或改收益。

LOCAL_SIMULATION_PASS（非实机）：禁用table.unpack和全局unpack后的真实加载/转移回调、nil/false/0参数、自动备份、事件持久/24条上限、重复/读档/错误隔离及前批回归通过。先前模拟用标准Lua而漏此运行库差异，已新增针对性回归。

USER_GAME_TEST_REQUIRED：只补一次转移后的事件报告，不重测备份保存读档。重载易主前存档、Select shadow city、赠送AI，Read shadow / events截图一张；错误=无，相关事件序号增加并显示参数。若仍为0/报错回传即可，不继续接正式身份迁移。

### HISTORICAL：B064准备记录（结果以B065顶部为准）

D0025已按用户明确决定接受：时代对话GW-001系数15%→25%，模型与14类C/T ModifierArguments生成式同步，D=1/2/6/7对应0/25/125/150%。不新增用户实机测试，不把新系数标实机通过。作品范围、创作者时代/文物例外、theming、GW002不变；D0024原文已冻结。

B064.90独立影子账本已加入：Game Property保存现有有效城市的五项完整原始记录及pending阶段；加载时一次读取已启用玩家合法绑定城市，并在现有身份/投资/模板写入确认后同步。失败只报告，不再次消耗移民；正式玩法仍读取原账本。新账本不自动恢复City Property、不关联易主身份、不授予收益。它是持久备份验证，尚非正式永久UID/继承切换。旧token仅作备份键，禁止不同Owner/ID覆盖同键。

事件仅记录相关已登记城市的CityTransfered/Added/Removed/Initialized和Game CityBuilt/Conquered原始参数、原位置当前端点；保留最近24条，面板最后6条、Lua.log完整当次事件。事件不用于自动认领，已知旧Owner/ID及实际端点/坐标过滤可能漏未知形状，需本次实机检查。未启用Owner不会获得新专业或收益。每条相关事件核对已登记位置，不是每帧/回合扫描；移除不删备份，原址新token另记不继承。

LOCAL_SIMULATION_PASS（本地非游戏）：真实Lua易主后五项City Property缺失而Game保留投资/模板，重建Lua环境后持久读取、pending阶段、重复100次无写、24条上限、无关/空闲事件无写、原址新城不同token不串账、备份写失败不改城市；B062/B063与前批回归、D0025模型及内存SQL通过。

USER_GAME_TEST_REQUIRED：仅[独立备份小批次](../Status/Validation/Specialization_B064_User_Tests.md)。用易主前有效存档，首次加载自动备份后选中观察城市，赠送/转自由城，读报告，再保存重载读报告；不验证正式继承收益，也不重测时代对话。运行B064.90/modinfo90，未commit/push。

### HISTORICAL：B063研究结论（下一实施已由B064取代）

B063赠送AI补图已复核：原Owner/CityID0/393221→1/196610，位置65,31，两区域仍在，五项Property仍原有→现无。此为用户所述赠送路径的追加证据，正式继承未实现，不扩大为军事征服/事件顺序实测。见[补充结果](../Status/Validation/Results/Specialization_B063_Gift_User_Result.md)。

静态研究推荐Game Property完整永久账本+稳定UID+经验证的转移关联；现有Game绑定表只保留编号，不含投资/模板，不能单独恢复。HD已有Game表格和Gameplay CityConquered(newPlayer,oldPlayer,newCityID,x,y)先例，但赠送/自由城覆盖、事件顺序/旧对象存活时点仍未知。下一小步为影子账本与有上限事件日志，再切换正式继承；不使用位置独自认定身份、不在CityRemoved时直接删成果、不每帧扫描。详见[研究](../Reports/Technical/Specialization_City_Inheritance_Ledger_Research.md)。本轮只研究/文档和归档，运行B063.89不变，暂无新用户测试。

### B063自由城市首批结果（补充见上）

B063用户两图已复核：Cheat Panel转自由城市，Owner/CityID由0/393221变62/65536；位置65,31及已完成市中心/工业区保留，TOKEN/FLOW/JOURNAL/INVEST/TEMPLATES五项均由有变无。原INDUSTRY、3笔投资、6模板不能从新City对象读取。B063观察入口USER_GAME_TEST_PASS，正式继承尚未实现，不能标通过；仅该转移方式有实机证据。

本机Cheat MakeFreeCity直接调用CityManager.TransferCityToFreeCities（STATIC_CONFIRMED源码证据）；不是已证明所有军事征服/赠送都相同，也不能断定引擎内部具体清除时点。需先建立独立持久账本与可靠转移映射，再恢复城市关联并重算ACTIVE/网络；不能只改Owner或依赖易主后读取旧Property。无新设计决定，当前无需追加用户测试。详见[本批结果](../Status/Validation/Results/Specialization_B063_User_Result.md)。运行仍B063.89；本轮仅记录/归档，不修改运行源码。

### B063准备记录（测试要求已由上述结果关闭）

商业四本批已按用户回报收口：截图科技6→11，源28.4219×20%最终floor5，实际载体1+4；第二源不叠加。零路线、反序更新/读档、分发不二次汇聚、总督撤销按用户证据通过。文化/工业未独立实测，用户接受暂缓，不冒充USER_GAME_TEST_PASS。城市面板同回合延迟接受不修复。详见[结果](../Status/Validation/Results/Specialization_B062_User_Result.md)。

B063.89新增只读城市继承观察：记录选中城市五项原始Property深拷贝，换Owner后按原位置定位并对照Owner/CityID、token、专业账本、投资、模板。仅主动点击读取，无后台扫描、不写Property/收益、不执行继承、不重置投资。坐标只是此次观察定位，不作为永久UID。内存基线读档即失效。

STATIC_CONFIRMED（源码静态证据，非实机）：新模块没有状态写入/生命周期扫描；已有Owner锚点确实需要正式迁移适配。LOCAL_SIMULATION_PASS（非游戏）：真实Lua深拷贝、Owner/CityID变化、Property保留/变化/消失、城市位置空缺、读档清空观察以及B062回归通过。

USER_GAME_TEST_REQUIRED：仅一项城市易主前后只读对照，见[最小测试](../Status/Validation/Specialization_B063_User_Tests.md)。当前不是完整征服继承已实现；四专业能力主线已接入，完整v0.1仍需征服/Claim、通用资格及发布收尾。无新Design修改、Git commit或push。

### HISTORICAL：B062实现与待测记录（现已由上述结果取代）

用户重新授权从已提交/推送3382d7d B060.85基线审查并重做商业四。B062.88（modinfo88）为新独立CommerceConvergence.lua，D0024保持不变；B061.86/87隔离目录不覆盖，不恢复旧重试和跨回合扫描。

问题审查：用户B061.86 OFF图source28.4219→floor5、实际S6；AUTO6→7只有口述，没有AUTO载体证据，仍不能解释实际+1。B061.87共用网络报BATCH_LIMIT_OR_SHAPE、0/5路线。真实3382d7d接收代码在Count/Data缺失的零路线模拟中同样失败；说明存在先于87的空值协议脆弱性，不是已经证明游戏原生如何序列化。B062发送WireCount=count+1、空数据EMPTY，接收严格decode/count冲突/实际路线数校验；旧非空协议仍兼容。不把UNKNOWN冒充有效空集合。

STATIC_CONFIRMED：BackgroundRoutes.lua与3382d7d逐字节相同；NetworkSender只改明确空包字段，没有87重试；NetworkBridge只改解码及商业模块新快照后通知，旧主体由精确diff回归。沿用此前48个整数载体的定义/ID便于清除旧档残留，并非恢复旧Commerce Lua。

LOCAL_SIMULATION_PASS（非游戏）：真实sender/receiver经过丢弃Count0/空Data边界fixture，非空→空清除网络和商业收益、重复空包/错误count/非空缺数据拒绝；直接源按对应总yield最高，不按等级、不求和、不通过distribution继承，最终floor；100次相同计划无额外写入；OFF/固定TEST5/AUTO共享apply，1+4载体核对、ACTIVE降级/重载清理及前批回归。全部来源计划先算完再写city层。只读报告分别显示预期、最后配置、实际载体组成、原生城市读数/OFF基线差值，不用配置冒充实测。

USER_GAME_TEST_REQUIRED：B062最小批次见Validation/Specialization_B062_User_Tests.md。完整退出再启动加载原档；先零商路验证共用网络空集合，再原商业4城OFF→TEST+5（不需要商路）检验同一承载层，再恢复AUTO接一条科研直连验证20%与跨回合。任何前项失败即停止。不要求重新做全部高级收益/多源矩阵。无新commit/push。

技术边界：缺当前网络时撤销本项而非沿用旧来源；城市UI/实际收益刷新时点、+5原生效果及第三方间接回路未实机确认。技术目录0..65535不clamp；报告错误。TEST5只作用选中Commerce4城，本玩家其它汇聚暂清除；OFF关闭本玩家汇聚且记录选中城读数；AUTO恢复所有合格城市，读档默认AUTO。控制均不改变Potential/身份/永久账本。

### HISTORICAL：B061隔离与B060.85 checkpoint（仍保留）

用户明确要求回滚/隔离商业四并提交之前成果。当前源码恢复商业四实现前的完整B060.85（modinfo85，106文件），SHA256 a0e0fd75e87872612ab61a7354882ca7081767890149917efa688a60412216d4，与独立部署备份逐文件一致。B061.86/87商业汇聚及对NetworkBridge/NetworkSender/BackgroundRoutes的后续修改不在当前运行源码内。商业四停止开发，不能把历史B061测试计划当作当前任务。

用户已口述巨作相邻全部USER_GAME_TEST_PASS，基础3P→每件1P的原生小数截断接受、不修复。B060.85此前没有商业四正式收益。D0024继续保留用户确认的GW小数边界、未来商业汇聚总量备选和最终floor设计；保留设计不代表商业四已实现。

完整撤回前工作树679个非忽略文件及SHA256清单、tracked diff保存于忽略目录local/Isolated-CommerceIV-B061-20260913/。B061报告保留审计，B061可执行测试/新fixture随完整隔离副本保存，不再混入当前回归入口。恢复B061前test_b055_regression.py，不修改冻结旧fixtures。

B061.87最新两图：商业与通用网络均报BATCH_LIMIT_OR_SHAPE，UI路线COMPLETE_UI_SHADOW、商路显示0/5；空集合Data空串跨界面可能缺失是未证实假说。不能声称已修复根因，也不能把失败状态归因于旧存档。B061只增加1的异常仍未解决。先恢复基线，不继续叠加修补。

### HISTORICAL NOTES：已撤回的B061开发与测试

B061.86首批USER_GAME_TEST_FAIL：用户AUTO城市Science6→7、OFF6；截图只有OFF，source28.4219→20%5.6844→floor5，不能据此确认AUTO实际配置曾为5。第二图turn22 NETWORK_REFRESH_PENDING。未标商业四收益PASS。数据库已确认48载体定义存在，SCIENCE Amount为1/2/4等正确整数，不归因为旧组件缺失。

B061.87修复两项静态缺口：NetworkSender原先只按API调用成功去重，没有按Gameplay接收确认重试；BackgroundRoutes增加独立当前回合观察，漏回合事件时在已有UI脉冲中仅标记一次重采样。发送只对同包最多重试两次，不放宽当回合/来源有效性要求、不用旧网络继续发收益。收益报告增加每类实际存在载体总数值及bit组成，网络未就绪用简短状态/前后回合/发送状态代替长堆栈（完整日志保留）。

LOCAL_SIMULATION_PASS（不等于实机）：真实sender首次丢包恢复/最多两次/空闲零请求/新批恢复、真实turn observer一次触发，以及既有商业择优/撤销/SQL和旧批回归。实际只加1原因仍未确定；不猜测是倍率/刷新或成功。Design D0024、SQL/20%/floor/结算规则不变。

USER_GAME_TEST_REQUIRED：读原存档B061.87，原商业四城OFF后读一次，AUTO后Read Commerce IV截图，报告若目标5应显示配置5/载体5[1+4]；过一回合再Read截图。若仍未就绪，报告包含后台回合/发送信息，立即停止不重复。此次无新增组件，重载即可；若版本未刷新则完全退出重启。结果回来前暂缓多源/分发测试。

### B061.86实现基线与初始测试计划（暂缓）

D0024已同步：用户口述GW002全部USER_GAME_TEST_PASS（用户实际游戏验证），原生逐件半点截断接受不修复，未提供新截图；不扩大到未知类别/其它接口。B061.86开始商业IV正式自动汇聚：直接R/C/I来源，各yield按实际城市总量择最高，20%后floor一次。条件总量备选已明确采用，不假称精确纯本地。城市层整数载体，与Industry区域输出/Research区域复制隔离；Commerce不能作源，先计算本轮全部计划再应用、绝对替换不累加。

STATIC_CONFIRMED：48个整数城市载体、无区域yield写入，已检查当前专业身份约束；LOCAL_SIMULATION_PASS：真实NetworkBridge与计划/结算Lua，最高产出不等于最高等级、多源并列不相加、distribution不冒充direct、重复100次无写入、floor、OFF/降级/断源/过期/重载/端点失效、SQL和既有回归。静态/模拟不等于实机通过。

USER_GAME_TEST_REQUIRED：完整退出应用重启B061.86读取原存档（新增Lua/SQL），一座Commerce ACTIVE4中心已有R/C/I直接路线；Read Commerce IV，OFF/AUTO固定条件比较城市实际S/C/P，重复AUTO不叠加；增加/移除最高源检查回退；中心往另一Commerce4仅分发不得再次汇聚原源。最小3例见Validation/Specialization_B061_User_Tests.md。

限制：整数载体0..65535/每yield是技术目录非Design cap，超范围明确错误并尝试撤销，不clamp；城市倍率/同回合原生缓存刷新需实测；其它Mod把商业总量传回源的间接回路仍开放风险。无无限扫描/通用UI事件审计；加载、真实城市/总督/作品/建筑事件与网络新快照触发，空闲不扫描。读取按钮只读；OFF/AUTO是全玩家测试开关、重载恢复AUTO。

### 历史：B060组件加载与验证过程（已通过）

B060.85仅修复相邻报告请求链路，不改D0023/SQL/收益公式。用户B060.84三图：前两图仍旧Dialogue OFF报告，后一图停READING GWA_AUTO，故本批报告交付记USER_GAME_TEST_FAIL，不能由此判定BASE getter失败。静态确认GWA早返回分支未绑定RequestToken且异常未生成ACK；修复为每次返回成功/明确失败报告。UI仅对待回复的GWA读取/幂等开关使用事件脉冲最多两次重试，不扫描；增加后台模块、最近收到请求、本次接收匹配及相邻采样异常信息。根因仍需新报告定位，不宣称已确定引擎丢请求。

LOCAL_SIMULATION_PASS：真实Gameplay请求分支+真实Panel请求/渲染，正常未就绪、模块缺失、Describe异常、城市失效、首次丢包且计时器不运行时恢复、全丢包只重试两次、空闲零请求，以及B060模型/SQL和前批回归。USER_GAME_TEST_REQUIRED：旧存档重新加载B060.85，选Culture4巨作城，只点一次GW adjacency Read；截图完整报告，若仍READING可点一次Show/Copy，不需过回合反复测试。结果回来前暂停收益验收。

### B060.84实现基线

D0023已按用户明确确认接受：GW002七类作品含Artifact不含Relic/Product；全部已完成专业区域含Theater/特色替代，按原yield各50%BASE。B060.84实现自动逐作品基础相邻能力，后台复用Dialogue事件样本，新增六yield区域向量，Gameplay重验端点/类别/完成/全集。与时代对话独立开关，原生GreatWork YieldChange载体，非城市补贴。

STATIC_CONFIRMED：每个piece七类六yield定义、±0.5及二进制目录；RequiresPopulation分类覆盖已确认本机专业区域。LOCAL_SIMULATION_PASS：真实Lua/内存SQL、完工/特色/非专业排除、BASE独立于Actual、作品数不平方、负/半点配置无丢精、重复/空作品/ACTIVE降级/OFF/无效端点/过期样本/重载清理及前批回归。配置不是实际收益PASS。

USER_GAME_TEST_REQUIRED：原存档主菜单重载B060.84，GW adjacency Read/Off/Auto。建议当前Culture4城两著作放非主题化槽，先Dialogue OFF隔离上一能力；Adj Off/Auto两图包含偶数/奇数BASE对照；相邻翻倍卡不改BASE/单件配置；总督调离撤销，原生整城更新允许下回合。详细步骤见[本批测试](../Status/Validation/Specialization_B060_User_Tests.md)。无新局要求，缺数据库/采样报告一图即停。

IMPLEMENTATION_LIMITATION：本批每yield BASE须为整数且绝对合计≤8191，目录上限仅当前技术支持，不是Design cap；超范围/非整数报告错误并清除本项，不静默clamp/floor。原生0.5与普通/时代对话/主题倍率的关系待用户数据，不自行改城市补贴。当前测试优先验证前者，用户已要求停止主题化深挖。

### 历史：B059城市率验证准备

B059.83只读对照已准备：Record GW baseline保存本UI会话中选中城的turn/作品C/T/城市C与收藏所在建筑/主题状态签名；后续读数自动显示差值及条件变化警告。增加主题化建筑作品C/T小计，隐藏已完成的两个Boost按钮，现有25/50/100/OFF/AUTO保留。基线读取不切换实验状态、不写游戏Property/收益，读档丢弃基线。D0022和收益/SQL/后台传输不改。

LOCAL_SIMULATION_PASS：真实UI读取计算同回合/跨回合差值，收藏/主题变化警告，原请求/实验档/SQL回归。USER_GAME_TEST_REQUIRED：当前两著作城先OFF并过一回合，再Record GW baseline截图；100并过一回合Read截图；OFF再过一回合Read截图，固定人口/专家/建筑/政策，若变化按报告仅作观察不强归因。这是城市产出率更新验证，不等同全国市政进度/对外累计旅游入账验证。现成主题化集合可另作固定收藏OFF baseline/100比较，若无不强求。详见Validation/Specialization_B059_Settlement_User_Tests.md。

### 已确认：B059.82非主题化作品读数

B059.81截图已显示Culture ACTIVE4、合格2件、creator D2、配置15%、后台IDLE；用户确认AUTO可读，初始化/配置链路在该存档USER_GAME_TEST_PASS。两图均AUTO、原生作品5C/20T、整城108.2656C、theme0，不能当OFF/AUTO对照或收益PASS。

B059.82按用户要求新增本城临时TEST +25/+50/+100按钮；互斥替换AUTO载体，不累加，仍Culture ACTIVE4及合格类型门控。OFF清除实验、AUTO恢复D0022公式，读档清理实验并恢复AUTO。D0022、正式SQL D档、后台事件机制不改。LOCAL_SIMULATION_PASS：14修正/测试档、125/150/200参数、真实请求、幂等/切档/资格撤销/读档清理及回归。实机百分比结算仍USER_GAME_TEST_REQUIRED。

下一用户批次见[大百分比对照](../Status/Validation/Specialization_B059_Percent_User_Tests.md)：固定当前两著作及建筑，OFF→100→OFF先确认大差值；再25/50，每档读取一图。若100无变化只过一回合复读一次并停止；不继续盲测，需区分刷新/作用域/原生倍率合并。

### 历史：B059.81待复验（初始化已恢复）

B059.80实机仍未初始化，用户创建新著作也未恢复。截图Game ACK0/NO_PACKET，UI scan1 send1 retry0、API=true、reason GreatWorkCreated；当前作品3/文化8/旅游32，theme0。发送返回true不等于Gameplay送达；空后台Context计时回调未产生重发，80模拟覆盖不足，不能称根因已修复。

B059.81取消SetUpdate依赖，通用引擎事件仅对pending原包做最多两次重发（每三次事件一次），不扫描收藏；空闲/超时停止。真实收藏事件在超时后可重建最新样本，读档/回合恢复保留。公共Gameplay请求入口在校验前登记接收计数/Action/玩家和收藏包Seq/字节数，报告区分未进公共入口与未进Receive。D0022/SQL/倍率未改。

LOCAL_SIMULATION_PASS（不是实机通过）：不执行任何计时回调，通过实际Gameplay request函数而非绕过入口直接Receive；首包丢失恢复、两次重发上限、百次空闲事件零扫描/发送、超时后新作品事件恢复、GW_READ入口及既有初始化/收益回归。实机传输具体失败原因仍待新入口证据，USER_GAME_TEST_REQUIRED：同存档主菜单重载81，点击Read Great Works；若仍失败只回传一张，无需再创作或移动作品。

### 历史：B059.80计时重试（已替换）

B059.79用户截图确认Game ready=false、ACK=0、received=NONE/NO_PACKET，而UI扫描1/发送1/WAIT_ACK：数据尚未进入Receive，不能把上轮Init保护当作已修复根因。记录USER_GAME_TEST_FAIL（仅初始化）。B059.80为等待确认的同一包增加两次、间隔两秒的有界重发；复用原payload/seq，零额外收藏扫描；ACK或两次用尽即清除计时器，失败保留ACK_TIMEOUT并等待下一回合。API返回值展示，nil不冒充送达；具体引擎丢包原因尚未证实。既有事件采集、公式、SQL/D0022不变。

LOCAL_SIMULATION_PASS：首次静默拒绝后自动恢复、两次上限、无额外扫描/超时空闲、迟到ACK不叠加、同步发布重入，以及79初始化故障与既有回归。USER_GAME_TEST_REQUIRED：主菜单重载原存档，确认B059.80，等待约5秒后Read Great Works；只需一张报告。恢复后才继续OFF/AUTO收益测试。详见[传输恢复记录](../Reports/Technical/Specialization_B059_Transport_Recovery.md)。

### 历史：B059.79初始化保护（保护保留，实机未解决接收）

B059.79初始化恢复：Init跳过GetCities返回nil的玩家，与已存在NetworkBoost清理约束一致。合法seq先记录接收ACK，再pcall Init；失败留明确DIALOGUE_INIT_FAILED并等待后续具体事件，不每帧重发。记录received/stage/generation，Describe在无城市结果时报告Game ready/ACK/错误；Gameplay外层异常亦写诊断。异步事件刷新策略与D0022收益不变，真实初始化恢复待用户验证。详见[修复记录](../Reports/Technical/Specialization_B059_Initialization_Recovery.md)。

### 历史：B059.78事件刷新（仍适用，初始化保护按上文补齐）

B059.78性能修复：DialogueRefresh移除SetUpdate两秒周期扫描。GreatWorkCreated/GreatWorkMoved、城市/总督变化、加载与回合事件标记dirty；通用SystemUpdateUI/Publish/Playback只处理确认和已标记任务，空闲零扫描。事件合并，城市/作品稳定排序；发送前置in-flight锁，同回合等待ACK期间不扫描/不重发，丢确认只在下一回合回退重试。资格投资/既有GPP通知直接Dialogue.Audit，不需扫描收藏。收益公式/SQL/D0022不变。报告显示扫描/发送/状态，便于实机排查。

B059.77的通用通知扫描和两秒后备方案已废弃；原生事件先例见GreatWorksOverview.GreatWorkMoved、DiplomacyRibbon/CityPanelOverview.GreatWorkCreated。保留初始化/读档和每回合核对，不依赖玩家开UI。细节见[性能修复报告](../Reports/Technical/Specialization_B059_Event_Refresh_Fix.md)。

### 历史：B059.77周期刷新方案（已被上文取代）

B059.77已按D0022实现自动时代对话：UI/DialogueRefresh后台采集所有当前己方城市/作品；DialogueModel共用creator era解析、文物历史时代例外与D去重；Gameplay Dialogue复核完整城市集合、唯一work ID、元数据、当前turn/seq并以EffectiveFacts门控Culture ACTIVE4。当前D→单一隐藏建筑，七类Culture/Tourism共14个原生ScalingFactor修正。数据目录依据加载Eras数量，不设D7 cap，D≤1不挂加成。旧B055手动巨作载体初始化清理、旧逐件补差报告停止调用。

读档清理派生载体后后台重新采集，旧样本不是永久事实。作品移动、城市归属变化、总督等级/专业变化触发刷新；同目录档位不重复挂载。诊断OFF暂停本玩家时代对话（不是改Design），AUTO恢复按资格应用，读档回AUTO。报告区分理论/已配置和原生作品Culture/Tourism；theming只读取原生布尔状态，无自建倍率模型。所有原生实际百分比及theming仍待用户验证。见[B059报告](../Reports/Technical/Specialization_B059_Dialogue_Implementation.md)。

### 历史：D0022同步时尚未实现的调查（下文当时状态已被上文取代）

D0022取代D0021固定yield：时代对话按15×max(0,D−1)百分比，Culture与Tourism原生ScalingFactor候选为100+该百分比，D≤1移除载体。不得继续固定旅游总量/CityCenter追加路线，不改变GW002。运行仍B058.76，本轮仅同步设计/技术路线，旧GreatWorkBasis补差显示非当前机制。

时代：普通合格作品GreatWorks.GreatPersonIndividualType→GreatPersonIndividuals.EraType；Artifact按用户明确例外使用GreatWorks.EraType，两者统一去重。本机28条著作两种Era不同，不能继续一律取作品Era；25种Artifact无伟人关联，已由例外解决。原生CreatorName可作诊断，但不能通过本地化名字盲猜creator ID；关联异常要报告。

Culture：MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD + GreatWorkObjectType + YieldType=YIELD_CULTURE + ScalingFactor；Tourism：MODIFIER_SINGLE_CITY_ADJUST_TOURISM + GreatWorkObjectType + ScalingFactor。D2/3/6分别115/130/175；一城对七个合格object types采用同档，件数不乘百分比。原生与theming关系待验证，不硬编码乘算/相加补偿；不额外封顶。详见[D0022研究](../Reports/Technical/Specialization_D0022_Dialogue_Percent.md)。

### HISTORICAL NOTES：D0021及更早（固定yield路径已被当前段取代）

D0021时代对话正式取代逐件补齐。停止GreatWorkBasis旧差额计划后端和单件setter调查；现有B058.76面板仍可显示旧计划，仅是过期探针，下一实现替换为时代集合/数量/每件统一bonus，本轮不把它当当前玩法。当前运行包未修改。

目标流程：当前城市works→按D0020资格过滤→从work type映射GreatWorks.EraType→时代去重D→k×max(0,D−1)→每件统一Culture/Tourism。Culture沿用已验证的GreatWorkObjectType+YieldChange；Tourism先验证固定追加接口，不把ScalingFactor百分比误作固定点数。若独立追加不吃theming，按D0021记录原生行为，不做逐件模拟。EraType与玩家/招募/发掘时当前时代不同；缺失不默认计为某一时代，采样标不完整并报告。详见[时代对话研究](../Reports/Technical/Specialization_D0021_Dialogue_Across_Eras.md)。GW002保持原样。

### HISTORICAL NOTES：D0020及更早（旧逐件路线不再派发任务）

D0020追加：遗物与产品排除GW保值，文物仍在文化组。B058.76只读计划同步排除；文化/旅游独立最大与作品倍率/主题化要求保留。以下D0019遗物组说明是本轮较早方案，已被此修正取代。

B058.75在B057整数原生通过后正式接入D0018末端量化。NetworkBoost.Plan保留Raw/FinalRaw，最终Quantize一次，按整数Applied值选择独立载体；同整数不同N不改写，旧B055/B057载体初始化清理。当前90个整数载体（两类1–45），覆盖k=1/L≤4/N≤129；未来效率或k扩展必须扩大目录，不能clamp。旧浮点表仅保留数据库与清理兼容，不再发放。

D0019确认逐yield最大值、遗物Faith/Tourism，以及补齐部分必须适用作品倍率和主题化。UI/GreatWorkBasis是逐件基础值采集/差额计划，无收益写入。只读GreatWork_YieldChanges/GreatWorks.Tourism，不读最终产出反推基数。当前缺口是单件差额和作品倍率原生实现：已知Effect按GreatWorkObjectType作用于整类，没有静态证据证明可限定单件；不得退回普通城市固定补贴。详见[B058报告](../Reports/Technical/Specialization_B058_Boost_GW_Basis.md)。GW002未扩展。

### B057及更早实现记录（下述当时未集成/待决被当前段取代）

D0018已同步：NET-RC-005要求FinalRawBoost在全部浮点修正完成后仅执行一次math.floor(x+0.5)。B057.74先实现隔离整数写入验证，不提前切换正式网络；默认自动路径暂沿用B056，这是用户要求“正式集成前最小实测”的明确过渡状态，不能宣称符合新量化契约的正式网络已上线。实验覆写本Mod两类Boost为0/2/4，稳定整数载体按AppliedBoost选择；旧载体先移除，重复相同整数不重建叠加，重载清理实验后恢复自动路径。原生2/4实际效果USER_GAME_TEST_REQUIRED。

GW-001已改为本城文化组/遗物组最高基础值补齐，产品排除；时代曲线不再是阻塞。GW探针仍为旧city/object手动比较，尚未实现新GW玩法。多yield排序冲突、遗物yield维度、补贴倍率与GW002遗物范围保留未决。详情见[B057](../Reports/Technical/Specialization_B057_Integer_Boost_Contract.md)，当前状态/测试由Status维护。

### 此前实现说明（被上述新契约覆盖的行为保留为过渡/历史）

B056.73恢复NET-RC-005正式权重1/2/3/4，保留独立k_R/k_C、浮点L√N与既有B055载体ID；不做Lua取整或补偿。B055实机截断结论见Status；正式权重表本轮仅本地验证，不能据此扩大原生PASS范围。巨作仍为手动对照，自动时代补贴/GW002尚未接入。HD类别时代标准表可读，但GW-001/003未决规则仍须用户决定；见[B056实现及巨作研究](../Reports/Technical/Specialization_B056_Formal_Boost_GW_Standards.md)。

本版同步Accepted D0017，新增B055自动Research/Culture网络Boost与手动巨作实现接口对照；B054折扣保持既有行为。规则引用Accepted Spec；验证/下一任务由[Status](../Status/Specialization_P0_Status.md)统一维护。真实收益已运行，许多旧文件名/注释仍带Probe/DEV，这是部署边界而非“全部只是读取”。

## 运行结构

> 历史baseline描述，非当前实现矩阵；仍适用的合同须结合上方CURRENT链接的后续切片读取。

模块路径相对于仓库Mod/源码根；加载关系以SpecializationP0.modinfo及Gameplay.lua实际include/Start为准。

| 层 | 实际入口 | 职责与当前边界 |
|---|---|---|
| 测试载体/门控 | Data/Identity.sql、Frontend、Probe.lua:IsTestPlayer | 独立测试文明/领袖；当前消费者仍固定测试资格，不是已完成ELIG通用多玩家适配 |
| 新城与首次完成 | BindingProbe、CityJournalProbe、FreshBindingHook、CityFlowProbe | 双侧绑定与City Property阶段写入；普通新城按有效完成通知锁定，已有匹配正常存档恢复；不凭现有区域猜缺失历史 |
| 统一当前专业事实 | EffectiveFacts.lua | 合并foundation与投资账本；读取当前总督门槛得到ACTIVE；身份锚点含owner，完整征服继承尚未支持 |
| 移民投资 | InvestmentAction、UnitActions、UI/UnitPanelActions | Prepare不消耗；Confirm复核后INTENT→单位消费确认→提交；重复/上限/失效处理，旧未确认INTENT不盲重扣 |
| 工作专家/本地效果 | ResearchSupport、IndustrySupport、Lv2Housing、Lv2GPP、Lv3Support、Lv3Effects、Lv4Percent | 原生隐藏建筑/Modifier及基于工作人数的绝对状态；部分实际率可延迟到下回合刷新 |
| 商路来源 | UI/BackgroundRoutes、ShadowRouteState、NetworkSender | 后台City:GetTrade():GetOutgoingRoutes完整集合；无需打开贸易窗口；名称含shadow不意味着当前未桥接 |
| 游戏侧网络 | NetworkBridge、TradeRouteProbe | seq/epoch/turn/signal、端点归属与CountOutgoingRoutes核对；当前source/center/recipient重建；不是历史事件当路线事实 |
| Lv4固定复制 | UI/CopyYieldRefresh、CopyYields、Lv4CopyRead、Data/CopyYields.sql | 背景Actual采样→Gameplay复核→绝对city层收益；界面独立复核与实际配置分开显示 |
| Crew | CrewProjects、ConstructionProbe、UnitActionSitePolicy、UnitTargets、UnitActions、CrewPrecision及对应UI | 五项目原生完成产队；实际合法区域/建筑/奇观地块；限额生产力、消费和超额浪费，单位面板确认与地图目标标记 |
| 标准化记录 | StandardizationCatalog、Standardization | HD分类目录与折扣启用策略分离；城市Property一次初始化/增量学习；只读报告，不接价格或网络模板结算 |
| 保留实验 | YieldCarrierProbe、HalfYieldProbe及旧P0读取 | 与正式自动机制区分；Half ON额外实验会污染本轮对照，测试前Half OFF |

## 持久事实与派生状态

> 历史baseline描述，非当前实现矩阵；仍适用的合同须结合上方CURRENT链接的后续切片读取。

CityFlow使用SPC_DEV_CITY_FLOW_B020；EffectiveFacts/投资使用SPC_DEV_INVESTMENT_LEDGER_V1。底层仍依赖BindingProbe与B015 journal，不重命名Property或把旧DEV表无条件迁移成可信历史。阶段读回/停止模型可在DevelopmentTests找到，但不等于崩溃恢复、跨OwnerUID和全部历史连续性已解决。

专业/潜力/投资是持久事实；当前总督、来源/中心/接收集合、输出及载体是派生状态。B052标准化ledger保存城市永久掌握记录，当前网络模板并集留待独立计算。不得以旧内部建筑或过去商路事件补造当前连接。

## 后台商路与网络

> 历史baseline描述，非当前实现矩阵；仍适用的合同须结合上方CURRENT链接的后续切片读取。

用户已接受后台UI/BTS同源读取；禁止的是需要手动打开UI。正式运行来源是UI中的CityTrade当前列表，Gameplay可确认数量/任务但未找到完整可靠端点枚举；不要重新强求纯Gameplay作为开发前置。

传输行含op/oc/dp/dc/trader，边界128条、16384字符；当前按trader去重，端点用当前owner/cityID映射，非永久跨Owner城市UID承诺。发送包验证epoch、seq、回合、dirty signal及Gameplay CountOutgoingRoutes，再derive。计数相同不证明路线端点相同，因此仍需完整源快照。事件只促刷新；UNKNOWN不能当有效空网或保留旧奖励。

NetworkBridge派生direct中心来源与distribution recipient；D0009 direct即接收，首都self特殊来源；仅分发接收不形成递归direct relay。ConnectedKinds服务Commerce III，RecipientSources服务Industry IV。B055通过National()读取当前有效来源的ACTIVE最高值及recipient去重集合，自动配置原生Boost；B055实际差值已有用户同目标测试证据，范围以Status为准。

## 收益与精度

> 历史baseline描述，非当前实现矩阵；仍适用的合同须结合上方CURRENT链接的后续切片读取。

Base用于Industry I/III；Actual复制采用district:GetYield六yield口径，不是仅政策后相邻，不是city:GetYield。B051.67按D0015枚举所有已完成区域，科研排除Campus，不再按四专业或RequiresPopulation过滤；市中心也在枚举。Industry IV仍只从有效IV源锚定IZ取实际生产力，按输出金额max。未完成不计、无产出贡献0，缺失数据明确拒绝。

CopyYields.Plan支持0..65535.5范围内整数/半点，半点人口1..255。整数正负二进制位+per-population系数补偿，80个独立InternalOnly建筑；先撤旧再加新、重复不写相同状态。更细小数明确技术限制，不套Crew取整。消费者使用当前ACTIVE及真实网络；后台事件发布/播放/加载/回合入口和初始化fallback，计时器仅补充。读报告不写入收益。

城市百分比由引擎作用。B051.67扩展范围及固定条件下无持续增长的最小测试已获用户口头PASS，见Status结果；无逐区域数据，不视为市中心/所有Mod组合输入隔离的普遍证明。不静默排除类型，也不假定绝对覆盖足以防止所有反馈。详细证据见[技术索引](../Reports/Technical/README.md)。

## 下一实现策略与边界

> 历史baseline描述，非当前实现矩阵；仍适用的合同须结合上方CURRENT链接的后续切片读取。

标准化：Accepted IND-NET-004/005已经确认范围，不再把区域允许目录列为未决。实现应分为全量合格建筑目录（用于永久记录）、可版本化的折扣启用策略（用于当前资格）以及独立模板匹配组。保留BuildingType和HD分类证据；市中心三个组仅作为本项目映射，不修改HD表。当前禁用模板同样保存，后续打开策略时可重用记录。金币当前合法购买资格必须独立复核，不能把PurchaseYield字段或已记录模板等同已解锁购买；Faith隔离仍待原生调查。先实现账本、首次初始化及事件增量，不先接折扣。现有Owner/UID、旧已Industry城市初始化与征服支持边界须明确。

Commerce IV尚无正式汇聚。保留Eligible Local Basis策略接口；用户允许困难时研究总量备选、前提防递归，是条件授权，未采用为Accepted Spec替代。不能简单从含倍率最终总量减名义跨城输入。B055已接原生Boost配置，GW只有明确手动对照，尚未自动补贴。内部浮点直接传入引擎，按D0017接受引擎舍去，不推断Tourism/theming已解决。

Conquest三分支/ELIG通用系统已有离线模型，未接完整原生流程；多个已启用玩家/多人确定性及非参与者扫描成本仍待集成。部分旧模块周期遍历所有玩家，不符合最终ELIG-004成本目标，不将其合理化为设计变更。复制模块已限制周期参与者，仅生命周期做休眠载体清理。

## B055：网络Boost与巨作接口测试

`BoostConfig.lua`/`Data/NetworkBoost.sql`由`tools/generate_boost.py`同源生成。现有桥接上限128条路线：每个recipient均为某条路线的目的地或首都self，因此当前上限129城。为每种网络、ACTIVE档与N保存一个原生Amount，避免分片Modifier各自截断改变总值；不是按来源/中心累加。超出上限明确报错并撤销该轮配置，不clamp N。独立k_R/k_C在生成器配置；改值须重生成SQL/Lua，非热修改。临时权重按Spec NET-RC-005，正式权重尚待测试结束后恢复。

`NetworkBoost.lua`在首都放置每类型至多一个内部建筑，沿用Great Library的`MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST`/civic对应物。匹配HD的可撤销player property Modifier，只为兼容其额外Boost提示，不直接改写共享Property。来源/路线/总督/投资改变重新推导，旧载体先移除再加新；初始化清理保存的派生建筑并重建，读报告不启动收益。`UI/BoostRefresh`后台主动握手，避免只依赖一次LoadScreenClose。现行native科研/市政进度不由本Mod写入，不补发已触发Boost；最终封顶沿用引擎观察，仍非最终设计已确认。

`GreatWorkProbe.lua`/`Data/GreatWorkProbe.sql`是互斥手动CITY/OBJECT/OFF。CITY固定整城+2基础文化；OBJECT每件七类标准文化作品+2文化，排除Relic/Product/未知类别。两者不增加旅游业，初始化和所有权变化清理。不是GW001当代标准，也不是已实现GW002；仅比较city subsidy与native object修正的实际展示/倍率行为。`UI/BoostGreatWorkRead.lua`只读原生Boost进度与建筑巨作收益/旅游业/作品分类。七类仅是实验范围，未替用户决定最终GW003列表。

详见[B055实现报告](../Reports/Technical/Specialization_B055_Boost_GreatWork.md)；当前验证矩阵/测试由Status统一管理。旧“Boost/GW未接收益”只适用于历史版本，不覆盖本节。

## HISTORICAL NOTES

[此前A0110全文](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_fresh_agent_handoff.md)保留全部旧调查/阶段与来源链接；其中A000x等待、纯Gameplay阻塞、无正式收益、四区域复制限制等不再代表当前。精确原字节另存本轮DevelopmentBackups。既有Historical及结果原件未改。

## 可移植源码与部署

仓库Mod/是唯一可编辑源码；外部runtime只由已授权部署产生。测试入口与7个基准均在仓库；游戏数据库只读外部配置。部署检查/事务边界见../../tools/README.md；旧截图/备份/历史路径见../Reports/Proposals/Phase1_External_Materials.md。

## B052运行适配

详见[标准化记录实现](../Reports/Technical/Specialization_B052_Standardization_Ledger.md)。`SPC_STANDARDIZATION_LEDGER_V1`保存具体建筑和HD分类收据；LoadScreenClose/城市首次完成/玩家回合只发现尚无账本的Industry，已有账本不扫描城市建筑。建筑通知适配分开处理：GameEvents的player/city/building与Events的x/y/building/player不能混用。后者只对玩家城市检查通知指向的单个建筑。延后复核不构造缺失拥有事实；读取不触发写入。当前foundation token仍含既有身份约束，保存永久收据不等于已实现跨Owner继承；冲突保留旧账本并停止写入。

运行catalog直接读取HD表，分类改变需迁移，不采用旧JSON快照作白名单。启用分组引用IND-NET-005；不把范围内记录数或PurchaseYield等同实际Gold资格。历史StandardizationLedger离线原型不是本次运行入口，不把它的Tier>=1限制应用到本批市中心Tier0记录。

## B053货币适配调查

Accepted D0017 IND-NET-002允许Gold隔离困难时Faith同步打折；不扩大建筑或购买资格。PurchaseProbe/Data/PurchaseProbe.sql是独立手动实验，使用现有COLLECTION_OWNER指定建筑购买折扣，未添加无先例YieldType参数。临时双币条件只在测试按钮启用的城市生效，OFF/LoadScreenClose清除；没有接网络或账本匹配。PurchaseProbeRead在UI侧读取原版ProductionPanel使用的GetGold():GetPurchaseCost(yieldIndex,buildingHash)，不是当前购买许可判定。实际Gold/Faith行为仍须用户测试。详见[B053测试](../Status/Validation/Specialization_B053_User_Tests.md)。

## B054自动折扣运行适配

StandardizationDiscount独立于永久账本；当前来源并集和最高ACTIVE→候选计划→后台原生金币购买许可→完整版本化回传→绝对载体。NetworkBridge只新增刷新通知，不改路线语义。Standardization只新增复核后的ReadLedger读取接口，不改学习规则。新SQL依HD范围生成单建筑四档内部载体，不修改原建筑。当前采用原生指定建筑购买成本Effect及D0017双币条件授权，保留引擎尾数，不做货币退款。详情见[B054](../Reports/Technical/Specialization_B054_Network_Discounts.md)。此前B053“未接网络”段落只描述独立历史实验，当前正式状态以本段及Status为准。

## B054.71启动补偿

后台DiscountEligibility在Gameplay模块已存在但ready=false时发送DISCOUNT_INIT；游戏侧按测试文明授权调用幂等EnsureReady，清理失效载体并生成计划，不依赖打开面板。正常LoadScreenClose路径仍保留。Describe无副作用，仅补充ready/busy/generation定位。缺失一次加载事件及重复初始化已做真实Lua模拟；引擎实际漏事件原因尚未确认，不把推断写成实机已证明。
