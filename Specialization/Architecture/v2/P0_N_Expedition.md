# P0-N1/N2/N3 — 人文考察、文化见闻与网络准备计划

State: N1_PARTIAL / B182_SPY0_DISPATCH_BLOCKED / REVIEW_BEFORE_REPAIR. N2/N3 and U2 remain ON_HOLD; later formal N1 scope is not authorized by this prototype.
Authority: Spec D0049 / Culture D0049 `CUL_L4_EXPEDITION`、missions、contracts.expedition/observations/network_effect / Shared D0045 A/E3/G及NET-001–004。当前共同合同与最新用户补充的区别见当前切片；只对直接Spy/宗教/移动表面作定域调查，实际运行与授权见[准备入口](Culture_Preparation.md)。

[人文考察团UI计划](P0_N_Expedition_UI.md)基于现行Gameplay与本地Stable调查提出独立管理窗口、目标／任务、重挂靠、历史及Network呈现。完整UI布局仍为提案；旧N1 gate已取得所测证据，B182仅实现Spy0独立派遣与共存技术原型。UI借鉴不证明可复用真实Spy管线，N2/N3仍未授权。

## Current slice — N1 travel and protection gate

**B182.209 / modinfo209: native dispatch gate stopped with API_UNAVAILABLE.** [Three-image review and Design implications](../../Status/Validation/Results/Specialization_B182_Expedition_Spy0_Native_Review.md) is the current evidence. The unchanged [local result](../../Status/Validation/Results/Specialization_B182_Expedition_Spy0_Local.md) preserves the prototype scope and original test contract; its 62+10 local methods are not native travel proof.

Creation/readback shows one Spy0 fixture, the same own unit/source across T84→T85, Spy-capacity maximum5→5 and travel2+establishment0 for Sparta. Native Spy-operation eligibility rejects this fixture without identifying the reason. No arrival, same-tile contact, END or save/load observation is supplied. Source/count are hidden by the final error rendering, not proven deleted.

**Blocking implementation boundary:** Gameplay calls UI-only City:IsCapital; its local fixture incorrectly supplies that method. A read-only actual-module counterexample reproduces API_UNAVAILABLE before timer/placement while retaining count/unit/source. Exact native exception remains unconfirmed. Recommend a narrow context-correct target check and useful error evidence if separately authorized; no fix or fallback has been implemented by this review.

**Retained prototype scope:** own cap1 counts exact old/new types; source uses current owner/city/coordinates/token; session-only timer waits visibly at departure then attempts exact PlaceUnit. No native Spy operation, normal training, Property/Store write, persisted journey or rewards. Reloaded unbound fixtures are cleanup-only. Target is a met/living/revealed Major capital for this test, not a new Design restriction.

**Stop:** report to the user for route/Design discussion. Do not repeat the failing test before a repair; no automatic Spy1, religious/marker fallback, formal N1 or N2/N3/U2. Formal named Culture/Shared synchronization remains necessary before formal integration; the probe does not change Design. Source/live identity and further authorization remain in Status.

## 三种状态与已定数值

考察团是有当前归档绑定的单位和远程任务；成功文化见闻是**归档城市的历史**，不按原Owner分账；Culture Network传播各来源独立完成的文明集合价值，不把历史所有权交给接收城。单位仍归原Owner与成果随城市保留可以同时成立，不能混为一个归属规则。

| 项目 | 已接受规则 | 成熟度 |
|---|---|---|
| 新训练 | 当前Culture ACTIVE IV；Production成本严格等于当前规则下的Spy生产成本 | v0.1首测，不是缓存60或任意“参考价” |
| 容量 | 当前玩家全国现存最多1团，所有存活团均计入，包括来源降级/退出/重组及等待重挂靠 | 已定；不继承Spy容量，不删除旧团腾槽 |
| 任务时间 | `floor(2 × 相对标准速度的回合时长倍率)`；部署时间另算，距离/时间参考Spy | 标准2T首测；不擅加min1或round |
| 本城收益 | 当前合法Culture ACTIVE IV：整体本城Tourism附加百分点=`2 × effectiveInsights` | K_T=2首测；33份有效见闻即本城+66%，非全国 |
| 网络收益 | 接收城单一Identity对应实际工作专家，每名额外`1 × 完整文明并集大小` Culture | K_C=1首测；不放大所有专家 |

训练成本、cap1、K_T/K_C和2T不再是null/TBD；平衡待观察不等于未授权数值。极快速度floor为0的引擎执行阶段须技术确认，不能改公式。排队/完成并发的容量门禁需实现；若需要额外扣损/退款规则才提出具体Design决定。

## 目标、任务与成功条件

目标为已遇见、存活的外国Major，城邦与Free Cities排除。无开放边界、使馆、同盟或商路门槛；战争允许部署/开始/继续/成功，宣战本身不取消。合法任务确定成功，单位保留；不继承Spy失败、俘获、死亡或外交惩罚。远程部署不退化成地图步行，无自动派遣。

| 类别 / Mission | 当前目标资格 | 首次成功成果 |
|---|---|---|
| PEOPLE 风土考察 | 对方当前实际控制的首都 | 当前有效归档城的该文明PEOPLE记录，1见闻 |
| WORKS 艺文采撷 | 目标城至少1件当前共同work_pool合格巨作 | WORKS记录，1见闻；不偷/复制/消耗作品 |
| PLACES 奇观巡礼 | 目标城至少1座已完成Wonder | PLACES记录，1见闻；不反推实际建造者或工业历史 |

目标失去必要作品、首都迁移、目标城易主或文明淘汰→取消，无奖励、不占成功键、单位保留。UNKNOWN不等于失效/无作品/已完成；到期不足以确认时HOLD并有界复核，不能用后续变化猜完成证据。作品严格沿当前已支持目录/可靠时代规则；外国目标读取不借本地K样本伪造全集。

## 归档、单位存续与城市历史

初始归档城以可靠训练来源绑定。来源总督/ACTIVE/Identity下降或REALLOCATING不终止已经完成的团：可以继续部署、执行并向仍有效归档城报告；该城当前效果另按资格门控。

**归档城Owner改变：** 未完成任务立即中止，不给不完整成果；单位保留原Owner，旧归档失效，禁止新任务。可免费、不限次数重新挂靠任意己方Culture Identity城，不要求ACTIVE IV/原训练等级；没有合法归档城则保留单位等待。重新挂靠是E3失效后的路径，不授权任意时刻自由换归档城。后续成果只写新合法归档城，既有成果不搬迁/删除。

单位不得被敌方捕获或转换Owner。以下为旧D0045保护合同的技术背景；2026-10-10用户已明确人文考察团应无害共存而非接敌撤退，正式同步边界与待审核方案见当前切片。旧保护式撤退/安全回归仅保留为已验证原型及其它专业的参考，不作为新考察团实施目标。归档城易主的具名中止/重挂靠规则优先；安全目的地与原生执行是技术门槛，不自行造死亡惩罚。Shared未涵盖的城市彻底毁灭、原Owner完全消失等局部边界仍待定义，涉及时单独处理，不泛化为所有N无法准备。

成功唯一键为`persistent archiveCity × foreignCivilization × category`，Owner不参与键。每键首次成功1份，不可消费/交易，无时代刷新或额外cooldown。城市历史最多三类×被可靠记录的文明数；外国文明后来灭亡不删除已得记录。

派生必须分三层：

- `historicalInsights`：城市全部可靠成功记录，随城保留；不因单位退出、换归档或当前资格丢失清零。
- `effectiveInsights`：从历史中排除**当前Owner自身文明**记录，只过滤当前使用，不删除记录；后来又成为外国文明可恢复有效。非支持Owner冻结使用/增长。
- `S_source`：该城独立完成People+Works+Places的文明集合，同样排除当前Owner自身文明。任意受支持Owner按当前Culture ACTIVE IV资格使用历史，不限最初Owner。

## N1：训练、远程交互、来源与保护原型

Goal：一个单位的可靠训练来源/全国cap统计→合法外国目标→远程部署/任务交互→来源变化及重新挂靠/保护候选；不提交正式见闻、不施加旅游或新Network。

已有本地UI／Spy语义调查支持独立窗口和样式借鉴；真实Spy身份／SPY_*管线的外交后果与盟友筛选风险仍需定域技术确认。实施时核对实际command/UI与HD替换，不把参考样式等同原生任务引擎。`Spy=1`可能继承容量、敌对任务、战争召回；`Spy=0`不能凭字段就宣称相同部署可用。原生可隔离路径、受控远程选择UI和现有计时均只是候选，未选定、未获native PASS。B178只核对gate直接需要的原生UI调用点及当前配置DB；既有Spy静态线索保留，最终生产成本与实际部署关系仍待原型核实。

来源靠训练/完成事件及可靠receipt证明，不按单位位置/名称/最近城猜测；重复登记幂等。全国cap包含无归档团，同回合grant与队列并发都要核对。Spy的Gold购买字段不是考察团购买授权，涉及购买入口须核对正式范围。

外国目标只对选中/执行中的目标定域采样并Gameplay复核：WORKS沿同一支持目录和owner/location事实，PEOPLE取current capital，PLACES取completed Wonder；不把本地K协议改成全世界广播或长期AI城市监听。

本地先验cap/来源/资格和三类任务状态；native只补远程命令、战争不中断、目标失效、无害共存或重挂靠等候选实际触及且无法模拟的差异。无法隔离原生捕获/战争召回时停该路径，报告TECHNICAL_INVESTIGATION_REQUIRED，不改Design。N1通过只证明所测交互，不证明N2永久任务或旅游。

## N2：任务事务、城市历史与整城旅游

复用现有E2可靠城市连续性/保存模型，新增专属小型业务块；当前Store没有新见闻/考察业务字段。分开保存unit当前Owner、有效归档绑定、部署/mission/目标ref与阶段，以及城市唯一成功类别/凭据；不新建cityKey、原Owner分账、全世界建筑历史或统一Legacy框架。Claim timer只提供技术结构，其业务取消规则不直接复制。

开始及成功提交前重验当前有效归档/Owner、目标事实和未成功键；唯一事务一次写城市记录/凭据，再派生有效数、完整集合和本城旅游。重复completion/load不重奖；取消不占键。来源Identity/ACTIVE退出但归档仍合法可收记录；来源易主立即abort，不能延迟向已转移旧城补提交。UI只读确认状态/发送意图，不成为发奖权威。

新Owner/原Owner夺回均从同一可靠城市历史派生，并重新应用自身文明过滤与当前资格；不能恢复旧有效数、Network或carrier快照。单位丢失不清已成功历史；异常任务退出不得凭空补成功。成功后移除当前事务，永久成功键保留，等待重挂靠状态以存活单位为界有界维护。

先任务/ledger影子及集合模型，再整体Tourism原生门禁。既有`MODIFIER_SINGLE_CITY_ADJUST_TOURISM`线索多有作品/奇观/改良过滤，不能据名称证明无过滤时整体可用；也不能据缺少先例宣布不能实现。L1区域固定加值、M作品原生倍率与N2整城旅游是三个接口，证据不得互代；不擅改为作品限定或固定点数。

本地覆盖：三类唯一键、Owner过滤/夺回、归档易主与完成同窗口、重挂靠新城额度/原历史不迁、unsupported冻结、重复/取消/保存失败/load/UNKNOWN、其它城市隔离。N2新增任务/绑定/历史schema，因此确有新的持久性风险；未来只选一个对应保存边界验证，不重复所有共享probe默认OFF/重启/再启用。

最小native在候选就绪时固定：至少两类可识别旅游来源区分“整城”与“仅巨作”；一条实际新增任务/归档保存或转移路径证明新事务，不要求完成多国全部三类。每一步列出新增信息；现有同路径基础设施证据与local regression继承，本轮不请求用户造fixture或测试。

## N3：Culture Network与精确旧Eureka退出

前提：N2可靠城市历史与过滤后完整集合、现有共同路线/中心资格、接收城专业实际工作专家事实。

`S_receiver = union(S_source for valid connected Culture ACTIVE IV sources)`。
`Culture_per_matching_working_specialist = 1 × |S_receiver|`。

- 每source从自身历史独立3/3，排除其当前Owner自身文明；A城2类+B城1类不能拼完整文明。相同完整文明去重，不sum counts、不取max source。
- 接收仅该城单一Identity对应实际工作专家；没有Identity就无受益专家。接收不授见闻、不作为自身成果二次输出。
- NET-001–004共同规则不变：首都自身专业direct self-connect，source→中心可接收/分发，distribution不递归。无需外国商路或新外交条件。
- `NetworkBridge.CurrentRecipientSources`只是已确认**拓扑来源**。当前derive以Potential≥1构造来源，不替N按ACTIVE IV/历史过滤；新consumer必须自己重验本能力资格和`S_source`。
- 拓扑、source资格/Owner过滤、成功历史版本、receiver Identity/实际工作专家分别触发。`NetworkInput.Signature`无见闻版本，`NetworkBridge.notify`无新Culture consumer；即使路线不变，source新成果也须更新payload。
- 按受影响来源/接收者更新；UNKNOWN按已有桥确认/HOLD，confirmed loss可靠撤销。不把空包当断路，不世界扫描或粗略每城每回合一次。

现有`NetworkBoost`仍同时生成Research/Culture旧`k×L×sqrt(N)`并写首都carrier；共享TEST的testRaw可写两种类型，Culture SQL涉及原生Tech Boost与`HD_Player_Extra_Tech_Boost`。N3才退出旧Culture部分，保留Research既有公式/效果。

实施前精确核对Culture legacy/integer/test owned IDs、SQL附件、生成/Audit/TEST、初始化清理、isolation、owner exit及HD Property/后台writer；本轮只确认直接调用点，**未完成全Mod exact-ID退休审计**。不得停整个NetworkBoost、按前缀扫建筑，或让共享TEST复活旧Culture Eureka；旧清理ID可惰性保留，新旧收益不并行。

本地覆盖独立3/3后union、Owner过滤变化、首都/中心、同回合专家、无路线变动的新记录、source/receiver退出、重复零写、load清理及Research不回归。native只验新专家Culture投影、决定性接入/撤销与实际改动的旧Eureka退出；集合组合主要本地完成，不要求用户重复多国长测。

## 生命周期、风险与退出

N1按实际交互/单位状态风险选L2或涉及持久绑定时L3；N2/N3按L3做相关保存/网络/恢复回归，不机械全历史stress。普通计算只取有效数/完整集合；详细历史清单按需。队列按活unit/任务维护，完成/取消退出，缓存按绑定/目标/ledger版本失效；不复制全国事实采集、不增GC。

N1回退撤销原型；N2回退不得删城市历史/成功凭据，先说明schema和存档副本边界；N3退出新owned效果并保留N2成果，按已知独立网络包恢复，不清账本恢复旧系统。

真实门槛仍为远程非敌对/战争路径、外国事实、训练来源/cap时序、重挂靠与保护、专属持久事务、整城Tourism及新网络投影/精确旧writer切换。没有新的Gameplay决定请求；未涵盖的毁城等边界只在涉及时单独提出。当前停止在B182 Spy0派遣错误的证据审阅；未经新授权不修复或切换Spy1；正式N1续接及N2/N3仍需后续独立范围确认。旧B165待验描述不是当前活动门禁，见Status。

来源：[Culture D0049](../../Design/Content/Culture_D0049.json)、[Shared D0045](../../Design/Content/Shared_D0045.json)、[Spec Culture](../../Design/Specialization_v0.1_Design_Spec.md#6-culture--theater-square--cul)、[共同Network](../../Design/Network.md)、[既有网络合同](Batch_B_Shared_Network.md)、[退出合同](Batch_C1_Discount_Lifecycle.md)、[E2当前保存](P0_E2_Plan.md#current-slice--recovery-and-action-routing)。历史技术线索见[D0032 spikes](D0032_Technical_Spikes.md)，本页更新其文化归属/参数语义，不提升原生证据。
