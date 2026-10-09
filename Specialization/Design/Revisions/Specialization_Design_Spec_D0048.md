# Specialization Gameplay Redesign — Design Spec

Document Owner: Codex
Design Authority: User
Design Revision: D0048
Document State: ACCEPTED
User Acceptance: ACCEPTED
Acceptance Date: 2026-10-05
Acceptance Evidence: 用户B165反馈暂接受Meaning主题化放大、要求Balance实测，并明确授权第一批合同同步与剩余证据收口；不授权自动writer或新机制。
Previous Accepted Revision: [D0047冻结原文](Revisions/Specialization_Design_Spec_D0047.md)
Latest Accepted Design Revision: D0048
Maturity Notice: 其它既有PROVISIONAL/candidate/TBD状态不变

## 1. 文档范围与确认边界 — SCOPE

**SCOPE-001** D0048仅将Meaning追加受到原生主题化作为v0.1暂行首测规则接受，Balance待实测；仍不得被Dialogue放大。K0.5、逐域Floor、份额／W、九域六产出Design、资格／城市历史及其它能力不改，Culture运行隔离保持。未决定新倍率／cap／补偿，不授权全城writer、M或部署。以下为历史修订背景：D0047接受市政／Government国家治理中枢的新基线：四机构、七项具名能力及逐项未决，取代旧GOV-001至004；当前计划只向专用白板文明开放，不承诺普通Civilization/Leader能力叠加兼容。Government仍FUTURE／OUT_OF_V0.1，不扩大当前四专业、单人本地人类实施范围；本轮不实现、不部署。其它专业、Shared结构化正文、当前B163原生待验保持。以下为历史修订背景：D0046按用户决定恢复意义延展Government Plaza／Diplomatic Quarter→Culture；当前九域六产出，D0043暂排已被取代。逐域Floor、K0.5、份额、作品资格、倍率隔离、其它能力与Shared保持；恢复Design不等于Culture原生共存已通过，旧失败证据保留。以下为历史修订背景：D0045增量同步工业每模板实际持有来源择优、合法Gold/Faith渠道、完整1T研习中断和最终整数Floor；文化收口无额外对话cap、Spy等价训练成本／全国现存1团、见闻每份本城Tourism+2个百分点，既定系数与D0042归属不变。Shared具名专业单位不可捕获／转Owner、保护回归，特殊事务退出优先；原始首都三阶段改制仅FUTURE／DESIGN_RECORDED／NOT_V0.1_IMPLEMENTATION。D0044三项工业职责与首测值不重复改变；不扩当前四专业／单人范围。B159诊断与其待验边界不变，本轮不实现／部署，不向当前计划加入未来改制。以下为历史修订背景：D0044只同步Industry v0.1职责与首测值：三级标准化10%／Gold0%，四级本城研习L每层强化两项各2个百分点；工程实践仅四级降低施工队组建损耗，三级固定150%；III开放I–III、IV额外IV–V，不再有E门槛；巨构工程只加速自行生产旧时代奇观，不放大任何施工队注入。Shared仅新增具名城市历史L，不改D／普通建筑／其它A–G合同。首测值不等于最终平衡或运行实现，当前B158原生待验与四专业范围不变。本轮不实现、不部署。以下为历史修订背景：D0043只将意义延展的政府广场／外交区文化来源暂排，当前为七域五产出；不修改Shared完整领域映射、其它能力、系数、逐领域Floor、作品资格、倍率隔离或A–G生命周期。文化追加技术及负面证据留作未来恢复，不再阻塞本版v0.1；新Design不等于运行包已适配，也不授予下一批实施。以下为历史修订背景：D0042接受具名A–G生命周期与Settler确认原子性：未提交Dialogue取消、考察团归档重挂靠、商业化配置暂停／恢复及退出清除、施工队当前Owner容量与重组目标绑定。A–D已定归属保留，不统一所有永久资产，不扩大单人四专业范围；当前B155测试不变，只有Design同步。以下为历史修订背景：D0041按用户最新决定明确意义延展追加独立计算，时代对话／主题化均不放大，同yield的市政／外交追加文化亦排除。较早主题化包含追加的建议保留技术档案，非现行规则。逐领域Floor、系数／份额／资格与D0040生命周期及其它专业不变；先验证单城技术原型，不假装接口已实现隔离。以下为历史修订背景：D0040同步用户已确认的长期状态A–D语法及精确资产生命周期，Shared／Research／Industry／Culture／Commerce正文按其条款增量更新。城市历史随城、文明信用不转移、信誉随Commerce Identity、已成立资本／发展关键城市易主异常终止；S具体来源与稳定选择／UI锁定补齐。只关闭本轮决定项，E/F/G未讨论部分不补，单人本地人类范围与当前B154测试不变，不实现、不部署。以下为历史修订背景：D0039仅同步用户本轮Commerce v0.1公式、首版Balance及明确Legacy决定，商业机构/能力名称和主体结构保持。商业化五领域与收益、资本本金/回报/风险、信誉、发展报价/容量/加算及重组团队/征服退出已定；精确剩余资格、口径、其它速度与一般Ownership边界单列，不擅自补值。不实现、不部署，不扩大四专业或当前文化测试授权。以下为历史修订背景：D0038仅明确意义延展的取整位置：每领域换算为实际产出后分别Floor，之后同yield相加，最后乘合格巨作件数W。仅本能力适用，其它能力、Shared、作品资格及原生产出倍率隔离合同不变；不接受其它primitive或扩大实施范围。以下为历史修订背景：D0037接受Harbor完整双线新基线；同级双机构不是二选一，新海军镜像Military D0034机制，Military仅改名为行伍编制/战地勤务。商业参数、候选名称、技术与Legacy未决保持；不新增独立Harbor Network，不扩大四专业v0.1。以下为历史修订背景：D0036只修订工业模板首次初始化/恢复/当前事实同步与历史损坏边界；可靠历史∪当前合格建筑，不扩展目录或AI运行范围。其它专业、Shared、参数及未决项不变。以下为历史修订背景：D0035为Shared semantic clarification / consumer confirmation：D为区域基础设施深度，不是相对完成百分比，不归一化不同环境；公式/consumer机制不变。Military保持D0034。以下为历史修订背景：D0034仅为综合训练补充绝对基础设施深度→本城训练效率层，同一能力内不新增slot；具体转换/汇总/购买适用等后置，Shared与其它专业不变。以下为历史修订背景：D0033冻结Military候选，见Military_D0034及review；不扩大当前四专业v0.1 implementation范围。其它专业与Shared正文不变。以下为历史修订背景：D0032冻结Commerce主体及0/1/2/3能力结构，明确旧规则取代关系；确认Industry每来源容量2和Culture Hybrid D展示方向。公式/mapping/Balance/Legacy及技术原型未决见Commerce content与Review，不等于已实现。Research_D0031、Culture_D0029、Shared_D0028正文不改。以下为历史修订背景：D0031只新增Industry有限施工队库存（范围/数值待决）、Research学术传统身份暂停合同及Culture展示需求。Culture Gameplay与其它机制不改；UI调查建议不是已批准架构。以下为历史修订背景：D0030仅将Research III学以致用输入替换为各领域区域完善度、K暂定0.5；其它机制不改。以下为历史修订背景：D0029仅补充Culture永久记录归属、多源Network并集与外交资格，见CUL节；Shared、Research、Industry不变。以下为历史修订背景，不覆盖当前CUL：D0028冻结Culture本体、Shared区域完善度/产出份额/建筑当前资格，并按用户明确要求将Research基础设施输入改为区域完善度；Culture旧Eureka网络退出，新网络多源合并后置，Research网络标记需要重设计但本轮不修改。以下为历史背景：D0027仅冻结Industry新机构/能力合同及关联标准化/施工队规则，见IND节；数值BALANCE_REQUIRED、候选命名和暂沿用复审标记不升级为最终定值。以下为历史修订背景：D0026仅替换Research本地等级设计并冻结规范化机构/能力/Tooltip内容，详见RES节；Research Network及其它专业不变，implementation/balance validation pending。以下为修订历史背景（旧RES描述由当前RES节取代）：D0025仅将GW-001时代对话系数从15%提高到25%，其余机制与范围不变。本文为Specialization Gameplay Redesign的WHAT。D0023确定GW002作品/专业区域范围及保留原yield的50%基础相邻复制。D0022时代对话采用创作者时代多样性百分比15%×max(0,D−1)，取代D0021固定yield；明确文物历史时代例外。旧最高基础值逐件保值已退出当前设计，沿用D0020合格分类与原生theming行为。D0018以NET-RC-005的最终一次显式量化取代D0017接受原生截断；当时的GW本城最高基础值方案现已被D0022完全取代。公式/topology及其它未决边界不变。D0016新增IND-NET-002货币隔离困难时允许Faith同步折扣的条件授权，不扩大建筑或购买资格范围。D0015确认标准化永久记录与当前折扣开放范围分离，详见IND-NET-004/005；不改变D0014科研复制范围或其它专业机制。D0014明确RES-004不区分区域类型，所有非Campus区域的Actual复制基数均纳入，不要求其为专业化区域或消耗人口名额。D0013明确IND-NET-004标准化模板获取与一次初始化，其余继承D0012。D0012明确施工队生产力按游戏速度缩放后向下取整，并以同一整数显示与执行；项目成本仍由原生引擎按游戏速度计算。其余继承D0011（五档从工业Lv1全部开放）。D0010正式确定征服无Identity城市的一次snapshot及互斥初始化模式，直接影响当前v0.1 Development与Conquest测试；更新后交Development正常sync评估Architecture/Status/Tests，旧统一first-completion假设不得继续沿用。其它设计与成熟度继承D0009，Design本轮不调查或修改实现。

**SCOPE-002 — CURRENT IMPLEMENTATION SCOPE — v0.1** Research/Campus、Culture/Theater Square、Industry/Industrial Zone、Commerce/Commercial Hub，以及共同成长、Trade Center、网络核心、Construction Crew和这些专业的跨系统规则。范围不等于实际完成度。

**SCOPE-003 — ACCEPTED FUTURE DESIGN — OUT_OF_V0.1** Landscape/Preserve、Religion/Holy Site、Military/Encampment、Harbor、Government Plaza、Diplomatic Quarter、Community/Metropolis、Entertainment/Water Park、Aqueduct、Dam、Canal、Aerodrome/Airport、Spaceport、Alliance Diplomatic Missions。此标签表示用户已经确认列入未来设计的范围/明确机制，不表示Future进入v0.1实现范围；各条PROVISIONAL、candidate、TBD状态不得被本标签覆盖。

**SCOPE-004** 用户是最终Design Authority。Codex负责整理落盘；外部设计顾问内容在用户接受前仅是proposal/review。没有用户明确确认，不得把后续修订或候选数值升级为ACCEPTED。

### System Scope + Opt-in Player Eligibility — ELIG

**ELIG-001 — Specialization-enabled Player / ACCEPTED** 当前计划只向专门的白板文明开放Specialization，并须明确赋予Player启用资格；不默认适配所有原版／HD／其它Mod Civilization与Leader Ability叠加。专业间系统平衡以无额外传统文明／领袖Gameplay bonuses为基准，现行单人本地人类范围不变。资格载体的内部技术标识不等于永久玩法身份，也不授权未来AI／多人配置。全文“玩家／己方／本城／首都”均受本节资格前提约束；未启用者不参与运行，但可按ELIG-005保留休眠的永久城市成果。

只有Specialization-enabled Player建立城市Identity和Potential、使用Settler specialization investment、计算ACTIVE、建立Trade Center及专业网络、获得Local及Network效果、运行Community Immigration、Military体系、其它Specialization及Auxiliary机制。资格只决定谁参与，不修改既有投资、总督、专业等级、网络公式、多来源、专业及辅助区域规则。

**ELIG-002 — 当前白板载体与未来边界 / ACCEPTED** 当前计划的玩法载体为专用白板文明，不是任意既有文明＋专业系统；具体文明／领袖／Trait技术ID不作为永久语义。此前“当前载体可任意选择其它文明”“不得写成只有白板文明可用”及默认原文明／领袖能力共存的承诺，由D0047明确取代。无需为了所有历史文明的独特能力改写专业规则或承担叠加平衡。

未来另行复用到其它文明、启用AI或多个玩家的可能性未永久禁止，但须单独获用户范围授权并处理对应Design／兼容边界；本轮不实现、不保证这些配置。中文机构名可遵循中文语言习惯，未来英文可用朴实、普适的功能性译名，不要求逐字对应，也不自动生成或锁定英文名。

**ELIG-003 — AI资格与行为边界 / ACCEPTED** AI不是特殊禁止对象；被明确启用的AI允许使用同一套规则。当前不要求额外AI planner或AI行为重写，不因AI可能不善使用Settler、商路、总督或人口政策而削弱投资、改变网络／ACTIVE或简化Community，不增加隐藏AI bonus/penalty。未来启用AI实际表现过差或过强时，另立AI/balance问题，不提前解决。

**ELIG-004 — 参与者成本原则 / ACCEPTED** `Pay runtime/state cost only for participating players.` Specialization机制只需对enabled Players运行。未启用者不因Mod存在而建立新的Specialization city state、维护网络拓扑／recipient sets、计算ACTIVE、运行Community Immigration、Military训练／带教、Auxiliary support或其它专业周期更新。ELIG-005要求保留的既有永久城市数据属于休眠保存，不构成对未启用Owner运行系统的授权。

这是Design scope requirement，不指定过滤API、缓存、事件或其它实现。Eligibility carrier及有效过滤标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`。若Development发现所有AI承担明显周期成本，应依据本规则限定到eligible players，而非反向把系统永久改为Human-only。本轮不进行API／性能调查或benchmark。

**ELIG-005 — Conquest × Eligibility / ACCEPTED** 正常非重组城市保持PROG-004的永久发展成果定义，以当前Owner是否启用决定运行或休眠；进行中商业重组目标被征服的事务销毁与后续分流例外见PROG-011：

| 征服／取得情形 | 永久成果 | 当前运行规则 |
|---|---|---|
| 无Identity、原Owner未运行/建立该城专业 → enabled Player | 不自动虚构Identity/Potential；按征服完成时一次snapshot确认既有发展候选 | 依PROG-006至009互斥进入Legacy Claim或Normal First Completion；不再统一从零监听后续完成 |
| enabled专业城市 → 未启用Player | Identity、Potential和明确城市永久投资成果保留，不删除 | 系统休眠；不运行Local、ACTIVE效果、网络、Community、Military或其它专业机制；不因保留Identity而给Lv1效果 |
| 有休眠成果的城市再次被enabled Player取得 | 已有Identity/Potential及永久成果恢复可用 | ACTIVE按当前Owner总督状态重算，网络按当前Owner实际网络重新派生，其它派生状态重算 |
| 两个enabled Players之间征服 | 保留Identity、Potential和城市永久专业成果 | 依新Owner的Governor、Trade Centers、Trade Routes、Network和eligibility context重算派生状态 |

正常未专业化征服城与旧档缺失历史是不同问题；本规则不解决旧档首次加载的迁移初始化，也不删除此前已形成、虽由未启用Owner持有的休眠成果。当前Owner资格门槛适用于所有专业运行，永久成果本身不因此改变。

**ELIG-006 — Development / Future Compatibility边界** 当前专用白板文明、单人本地人类实施范围与征服休眠语义已经明确。AI未来可另行启用但不要求行为重写；原版／Mod文明叠加、多enabled玩家及多人仍非当前支持承诺。Old-save initialization、carrier技术实现、参与者成本过滤及跨Owner可靠识别保留既有Development／Future Compatibility边界，不据此修改Gameplay。本轮只同步设计与必要导航／状态元数据，不修改测试文明、源码、测试、部署或GC。

## 2. 测试文明与基本术语 — ID / TERMS

**ID-001** 以独立新文明和独立领袖承载测试，不修改或覆盖原版Scotland。暂时复用Scotland的文明/领袖视觉、名称风格和可用展示资产，不复制其原有游戏能力。玩家可见名称采用Scotland (Specialization Test)、Robert the Bruce (Test)等明确测试标记。暂不制作原创美术与历史设定。当前计划只向专用白板文明开放，以Specialization为主要玩法和平衡基准；不默认兼容普通文明／领袖Gameplay bonuses叠加。未来复用须另行授权，遵循ELIG。

**ID-002** Industrial Zone保持正常科技位置，不作为提前解锁的特色区域。

**TERMS-001** Specialization是城市专业身份；Potential是该城永久投资形成的潜力；ACTIVE是当前实际激活的专业等级。三者不得互相替代。Working specialist指实际工作的对应专家，空槽不算。

**TERMS-002** Base adjacency只指基础相邻，不包含政策等相邻倍率。Actual在本设计中指与煤炭发电厂/大酒店“按区域产出复制”机制相同口径的区域产出基数，不是城市总产出，也不要求先建成这些建筑；不等同于“只取政策翻倍后的相邻数字”。具体非传统收益/区域适用范围待澄清时，不擅自扩大或删减。

**TERMS-003** F=Food，P=Production，S=Science，C=Culture，G=Gold。百分点是对百分比数值直接相加，不是相乘增幅。

## 3. 共同成长与永久投资 — PROG

**PROG-001** 普通First Completion模式城市在第一个符合条件的专业区域完成建造后锁定专业，不在放置时锁定。v0.1四专业及正式认定replacement family适用；征服无Identity城市先按PROG-006分流，Legacy Claim模式不适用后续first-completion。未来Community候选仍见COMM-001，不提前改变v0.1规则。

**PROG-002** 专业确定后默认Potential Lv1。在己方城市消耗一个Settler，永久Potential +1，最高Lv4。Potential不由source数量、网络强度或网络积累产生。不凭空给没有专业的城市发专业能力。 D0042确认前只有查看／准备，无消费／潜力增加／待继承投资资产；确认后Settler消费、receipt成立和Potential更新视为原子完成。内部事件交错由技术原子性／可靠恢复解决，不存在Gameplay半份receipt、部分退款或跨Owner pending继承。

**PROG-003** Lv2/3/4分别要求Potential至少2/3/4，并有已建立的总督满足2/3/4头衔门槛。ACTIVE取当前满足全部条件的最高等级；无已建立总督或总督调离时，已有专业仅保留Lv1，Potential投资不丢失。门槛不是要求额外消耗同样数量的Settler或额外重复支付头衔。

**PROG-004 — Conquest Inheritance / ACCEPTED** 适用于正常非重组城市；进行中资产重组被征服的显式例外见PROG-011。已有Specialization Identity/Potential的城市被征服后不进入Legacy Claim初始化，Specialization Identity、Potential、Settler investment history或等价永久投资事实，以及source城市自身永久掌握的标准化模板等明确城市成果保留。这些是城市长期发展成果，不是旧Owner临时全国buff。Potential Lv4 Research城被征服后仍为Research / Potential Lv4，不重置身份或潜力，不要求重新消耗Settler。

当新Owner为Specialization-enabled Player时，ACTIVE不继承旧Owner状态，按新Owner的总督任命、established状态、头衔要求及共同等级条件重新计算；无新Owner合格已就职总督时，已有专业按共同规则仅保留ACTIVE Lv1，Potential Lv4不丢失。

旧Owner的Trade Center连接、source资格、recipient资格和distribution routes不作为永久成果继承。征服后ACTIVE、Network connection、recipient status、从其它来源接收的当前Industry Template Set、Network Strength、当前折扣和跨城输出均依新Owner真实状态重算。永久掌握模板不等于永久接收全国模板并集。若新Owner未启用，则按ELIG-005休眠，仅保留永久成果，不运行ACTIVE（包括Lv1）、网络或专业效果；重新由enabled Owner取得时再按上述规则重算。

本规则仅决定游戏继承语义；跨owner/cityID变化识别同一城市的永久UID问题标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`，不在Design调查或设计实现，也不能因识别困难改变继承决定。旧档首次加载Mod时已有城市的身份/Potential初始化仍保留为Implementation/Future Compatibility事项，不从现有区域猜测，不再将其与已确定的参与资格或征服语义混为核心玩法未决。完成通知先后沿用已接受的PROG-005。

**PROG-005 — 完成通知顺序 / ACCEPTED** 对具有可靠普通first-completion历史资格的城市（新建城，以及PROG-006空LegacySet后从征服完成时开始记录的城市），按游戏交付的有效专业区域完成通知先后顺序，首个有效通知锁定专业；之后的通知，包括同回合其它候选，不覆盖已锁定专业。有效通知必须通过当前城市身份、区域类型与完成状态以及历史资格检查，加载通知不能作为新完成。多个候选同时完成也采用该通知先后规则，不按区域类型优先级排序、不将整个回合合并为同时完成。规则可能依赖游戏及其它Mod的通知交付顺序；它不授权用缺失历史的旧DEV观察替代正式首次完成；Legacy Claim城市明确排除，征服分流见PROG-006至009，旧档初始化仍独立。

**PROG-006 — Unspecialized Conquest Snapshot / ACCEPTED** 当城市没有既有Specialization Identity、原Owner没有运行/建立该城Specialization，且由Specialization-enabled Player征服时，在ownership transition完成时只扫描该城市一次，记录当时完整建成的合法专业区域对应的去重`LegacySet`。v0.1为Campus→Research、Theater Square→Culture、Industrial Zone→Industry、Commercial Hub→Commerce，包括已正式认定的replacement district family。已放置未完成、之后才完成或之后新建的区域不进入该snapshot。已有Identity/Potential的城市直接按PROG-004继承，禁止误入本初始化流程。

| 一次snapshot结果 | 模式 | 后续身份取得 |
|---|---|---|
| LegacySet非空 | Legacy Claim Mode | 仅从冻结候选经Claim Project选择；不再适用后续first-completion |
| LegacySet为空 | Normal First Completion Mode | 无Claim Projects，从征服完成时开始按PROG-005处理第一个后续合法完成，锁定Identity、Potential=1 |

两种初始化模式互斥，确定后不因后续城市建设切换；完成Claim进入已专业化状态不属于切换到另一初始化模式。一次性snapshot不是反推原Owner历史Identity，而是记录接管时客观存在的发展方向。

**PROG-007 — Legacy Claim Mode / ACCEPTED** LegacySet非空时，为集合中的每种专业提供对应一次性Specialization Claim Project，例如Establish Research Specialization、Establish Commerce Specialization。候选仅取conquest-time snapshot，之后不重扫、不追加，不因长期未选择扩大候选。玩家可无限期不执行项目，永久保持No Specialization Identity；系统不强迫自动选择。

进入Legacy Claim后，normal first-completed-specialization-district规则不再适用于该城。后续完成的新合法专业区域既不自动锁定Identity，也不新增Claim或修改LegacySet。例如征服时只有Campus，之后完成Commercial Hub仍只能Claim Research或保持无专业；征服时已有Campus+IZ则可选Research或Industry。公平性目标是继承接管时既有发展方向，不让征服城比自建城市获得更大的自由重选权。

**PROG-008 — Claim Project / ACCEPTED，精确成本TBD** Claim是确认既有发展成果，不是重新投资建设区域。成本须极低，或采用1-turn确认型设计；精确Production cost留后续balance/implementation，但不能使低Production城市需很多回合才能确认。执行任一Claim后锁定对应Identity、Potential=1，其它Legacy Claim Projects失效/移除，退出Legacy Claim进入正常已专业化状态。不能据本规则重置已有Identity城市的Potential。

**PROG-009 — 空候选与旧档边界 / ACCEPTED** LegacySet为空时不生成任何Claim、不进入Legacy Claim，从征服完成时开始普通first-completion。之后第一个完整建成合法区域自动锁定，例如首先完成Commercial Hub则Commerce/Potential 1，与普通自建城市规则一致。不得把此空候选处理泛化到征服时已有合法区域的城市。旧档首次加载已有城市初始化仍保留OPEN；可参考snapshot思路，但本轮不认定与征服初始化相同。已有Identity的enabled玩家间征服继续永久继承，不进入Claim。

**PROG-010 — Development影响与独立设计案例** 本次影响当前v0.1 Conquest实现及即将进行的测试；Development需按新accepted Design正常sync并评估Architecture/Status/Tests调整，不能继续沿用所有无Identity征服城统一监听后续first-completion的假设。至少拆分三种设计案例：

- Case A：征服时已有合法完整区域→冻结snapshot、进入Legacy Claim，仅可选择snapshot专业；后续新区域不能自动专业化或扩大候选，允许一直不选。
- Case B：征服时无合法完整区域→无Claim、普通first-completion，之后首个合法完成锁定Identity/Potential 1；未完工区域在snapshot中排除，但之后完成可按此模式处理。
- Existing Identity：原Identity/Potential继承、按新Owner重算ACTIVE/Network，不进入Legacy Claim。

技术问题统一标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`：ownership transition完成时可靠读取已完成区域、一次冻结LegacySet的保存、Claim Projects提供/移除、Legacy模式屏蔽first-completion、只在空集合模式启用普通完成处理、已有Identity不误入初始化。Design仅登记规则和预期，不调查API或修改Architecture/Status/Source/Tests。

**PROG-011 — D0039资产重组例外 / ACCEPTED** Commerce资产重组付出Potential损失，完整合同见Commerce_D0039.contracts.restructuring。事务存在时REALLOCATING不是NONE，不可再次触发PROG-001/002首次建立或PROG-006至009 Claim；不得通过Settler首次流程绕过配置，历史机构不提供Current Identity。

**明确征服例外：** REALLOCATING目标在配置前被其它玩家取得，立即销毁本次重组状态与未完成资产账本、清除旧Current Identity、解散绑定团队，城市无专业身份，双方均不能继续半成品。原玩家以后重新取得，按PROG-006至009无自身专业历史AI城snapshot/Claim分流，不按PROG-004恢复半成品；此时原REALLOCATING事务已经消失，原禁止Claim不再适用。销毁范围不是所有专业永久历史，未授权清空其它成果或补定其Potential/Legacy；非重组城市仍按正常继承。具名A–G状态按SHARED-LIFECYCLE-001及对应Content；其它未讨论资产边界不能类推。

## 4. v0.1共同Lv2规则 — SHARED

**SHARED-001** ACTIVE Lv2起，对应专业区域本体及该区域每一级建筑各+1 Housing。

**SHARED-002** 每名实际工作的对应专家增加+2基础GPP，之后正常接受其它GPP百分比加成：Research→Great Scientist；Industry→Great Engineer；Commerce→Great Merchant；Culture每名Theater专家同时获得Great Writer、Great Artist、Great Musician各+2。不能将基础GPP改为不受倍率影响的直接点数奖励。

**SHARED-003** 下列Lv3“提升至”取代低等级对应专家食物/生产力档位，不把3F3P与5F5P重复叠加。Housing、GPP及其它独立已解锁能力继续保留。

### Shared Mechanical Vocabulary — D0028

唯一当前共享定义：[Shared_D0045](Content/Shared_D0045.json)。`DISTRICT_DEVELOPMENT`、`YIELD_SHARE`、`ORDINARY_INFRASTRUCTURE`、`BUILDING_CURRENT_ELIGIBILITY`、`NETWORK_LAYER`及领域映射由此维护；专业引用，不在各专业复制不同定义。

**D0035语义及引用覆盖：** D正式中文名“区域基础设施深度”，即Absolute Infrastructure Depth。不是完成百分比，不要求建满=10；三层链D6、四层链D10均为允许的额外投资差异。当前不引入Relative Completeness。已有专业冻结文件中Shared_D0028引用及“区域完善度”用语，当前解释统一遵从Shared_D0045保留的D0035语义澄清；旧文件字节不变、历史解释保留。公式、稳定concept ID及其它Shared合同不变。[Consumer/目录/术语审阅](../Historical/Design/Reviews/Shared_D0035_Review.md)。

被掠夺建筑默认不贡献也不接受收益；这是当前效果资格，不删除明确永久的模板/历史记录。免费取得不改变普通建筑性质。区域基础设施深度有硬上限10，同领域多区域取最高单区域；不追补缺失Tier。Network独立于Ability slots，不统一专业公式或强制0/1/2/3结构。

**SHARED-LIFECYCLE-001 — ACCEPTED D0042／D0044／D0045具名增量** A城市历史、B文明历史、C持续机构关系、D已成立合同、E进行中事务、F配置／派生、G专业单位／来源绑定，彼此不混同，不设统一继承。Shared_D0045.LONG_TERM_STATE_LIFECYCLE保留[D0042具名合同](../Historical/Design/Reviews/Long_Term_State_D0042_Review.md)及D0044已完成研习L；本轮明确研习以IV资格采用完整1T取消／重做合同，历史L不清零。施工队／考察团／重组团队不能被捕获或转Owner，敌方原可能捕获／消灭的交互保护撤退／安全回归；重组目标易主解散与考察来源易主取消任务／保留原Owner单位／重挂靠的专属规则优先。原生接口属Technical，不再有捕获Owner Gameplay TBD。纯派生ACTIVE／Network／carrier按当前事实重算；不扩AI／多人。首都未来例外单列，不纳入当前A–G runtime。

## 5. Research / Campus — RES

**D0040 Research增量：DESIGN_FROZEN — implementation / balance validation pending.**

唯一新规则与文案正文：[Research当前Content](Content/Research_D0040.json)。[Schema](Content/README.md)；[当前边界审阅](../Historical/Design/Reviews/Boundary_D0031_Review.md)；[D0030历史审查](../Historical/Design/Reviews/Research_D0030_Review.md)。机构永久随Potential累积，ACTIVE仅控制对应阶段能力；机构为presentation-only，不进入普通建筑体系。

| Rule ID | 当前权威content条目 |
|---|---|
| RES-001 | RES_BASE_SUPPORT：各等级基础专家支持；RES_INST_1学者结社，无named ability |
| RES-002 | RES_L2_TRAIN：RES_INST_2研修院的人才培养，引用SHARED住房/GPP合同 |
| RES-003 | RES_L3_CROSS / RES_L3_APPLY：RES_INST_3学术联合会的跨学科研究/学以致用；替换旧人口Science与旧支持提升 |
| RES-004 | RES_L4_INFRA / RES_L4_CHAIR / RES_L4_TRADITION：RES_INST_4学术总署；替换旧专家百分比和全区域Actual复制 |

SHARED-003的旧Research支持提升不再适用，Research仅按RES_BASE_SUPPORT；其它专业的SHARED与Local规则不变。具体公式、映射及第一版Tooltip只在content维护，旧D0025正文见冻结快照，不将新设计视为B076.103已实现。

**RES-LIFECYCLE-001 — ACCEPTED D0040** 学术传统合格年龄为城市历史，无原Owner分账；原起算／速度门槛保持。支持Owner且仍有科研身份时ACTIVE下降不暂停年龄；身份退出暂停保留；未支持Owner冻结且不补失城年龄。任何enabled Owner重新满足科研ACTIVE IV按同一保留账本利用；不推导其它科研长期记录。

**RES-005** Research Network仍按NET-RC增加Inspiration，当前数值与公式不变；标记NETWORK_REDESIGN_REQUIRED，不在本轮重做。D0028仅将RES_L4_INFRA输入替换为Shared区域完善度及其10上限；主持仍逐普通建筑生效，遵守共享被掠夺资格，不反向增加完善度。D0026 content作为历史冻结保留。

## 6. Culture / Theater Square — CUL

**D0048当前适用范围：** Meaning追加允许原生主题化，作为v0.1暂行首测规则、Balance待实测；只取代D0041的主题化排除，Dialogue仍不得放大本项。D0046九领域／六产出恢复、D0045参数、D0042城市历史及逐域Floor保持；原生文化共存与实际自动接入各自待验证。

**D0048: DESIGN_FROZEN主体保持；主题化许可为USER_ACCEPTED_V0.1_PROVISIONAL／BALANCE_REQUIRED。保留九域六产出、D0045参数、D0042生命周期、Dialogue隔离与D0038逐域Floor；implementation / balance validation pending.**

唯一规则、公式、首版Tooltip与Mission内容：[Culture_D0048](Content/Culture_D0048.json)。D0029边界接受原件：[Amendment Review](../Historical/Design/Reviews/Culture_D0029_Review.md)。各能力原Shared_D0028引用按D0035覆盖声明解释，不复制第二套区域基础设施深度/产出份额。

| Rule ID | 当前content条目 |
|---|---|
| CUL-001 | CUL_BASE_SUPPORT / 文艺同好会；无named ability |
| CUL-002 | CUL_L2_PATRONAGE / 赞助人行会 |
| CUL-003 | CUL_L3_DIALOGUE、CUL_L3_AESTHETIC / 人文联合会 |
| CUL-004 | CUL_L4_MEANING、CUL_L4_INSPIRE、CUL_L4_EXPEDITION / 博雅总院 |
| CUL-005 | contracts.network_effect；新见闻传播取代旧Eureka；不继承NET-RC公式，多源按各来源独立完整考察文明集合并集 |
| GW-001 | contracts.dialogue；同名项目替换旧动态时代多样性百分比 |
| GW-002 | CUL_L4_MEANING；区域完善度产出份额替换旧基础相邻；D0038明确逐领域换算后Floor，再同yield相加，最后乘W |
| GW-002A / GW-003 | contracts.work_pool与dialogue.precision/target/fallback；意义延展仅采用D0038明确Floor例外，旧逐件固定yield截断许可不自动迁入其它能力 |

中文机构、能力、Mission名称CONFIRMED。时期次数、记录归属、源城绑定、目标合法性、战争及成功后保留单位详见content。CUL-REVIEW-01至04已正式确认：D0040明确取代见闻原Owner归属：见闻及Dialogue累计倍率／启动时代额度均为独立城市历史，Owner不是见闻归属或去重键；当前Owner自身文明记录只从有效见闻及完整3/3来源集合排除，不删历史／额度。当前能力按各自Culture Identity/ACTIVE门槛利用，非支持Owner冻结，多源完整考察文明集合并集，外国已遇见存活Major允许且战争本身不中断。城邦排除并列Future Candidate，自由城市排除；不新增外交许可或商路要求。未知Mod作品默认排除。意义延展追加基值独立计算，时代对话不得放大；D0048允许原生主题化作用于追加，作为v0.1暂行首测规则，Balance仍待实测，不把观测×2写成普适固定倍率。D0046九域及政府广场／外交区追加文化保持。Shared与其它consumer不改，同yield仍不能让Dialogue把追加视为作品原生产出。较早主题化候选仅在本次许可范围成为暂行规则。实际原生组合仍需验证，不自行扩展为其它城市／文明公共倍率豁免。本轮已关闭的cap／成本／K_T待决由D0045取代；真实Balance Validation和Technical flags继续保留，不把冻结当实现。

D0032批准[Culture时代馆藏Hybrid D方向](../Historical/Design/Records/Culture_Era_Presentation_D0032.md)；当次Culture_D0029玩法正文不变，D0038加入意义延展逐领域Floor例外，D0040新增城市历史生命周期，D0041澄清追加倍率隔离；D0048仅取代主题化排除，保留Dialogue隔离并登记Balance。布局/HD hook/缓存事件仍需原型，UI实施未授权；D0031调查保留历史。

**CUL-LIFECYCLE-002 — ACCEPTED D0042** Dialogue完整生产回合且永久成功提交前，文化ACTIVE<III／身份退出／REALLOCATING／易主／正常生产中断取消，无倍率、无START Era成功额度、无半进度；再合法须完整重做。已训练考察团不因来源总督／ACTIVE／Identity／重组变化而退出；来源易主中止未完成任务、不转交或删除单位，旧归档失效，免费不限次重挂靠任意己方Culture Identity城，无高ACTIVE要求；无合法归档城则存续但不能开新任务。新报告只进当前有效归档城，已成功历史不迁移或删除。 D0045专业单位不可捕获／转Owner保护适用，特殊来源生命周期优先。

**CUL-FIRST-TEST-001 — ACCEPTED D0045** 对话每次+5%×X加算，无额外累计cap；风雅每时代每合格普通建筑1Tourism；Meaning0.5D及Gold份额3／其它1、逐领域Floor保持，领域范围由D0046恢复为九域；巨作启迪0.1D×合格作品数为每回合基础GPP，Design不新增逐项Floor。考察训练成本严格等于当前Spy Production cost，当前玩家全国现存最多1支（含待重挂靠／退出来源的存活单位），不是每source／城／任务1支，不授权删除既有多团；标准每任务2T，部署另算。K_T=2个百分点／份，仅来源文化城市整城Tourism，33有效见闻为该城+66%，非全国乘1.66；K_C=1，receiver自身单一身份工作专家按独立完整文明来源集合并集获得文化，不拼不完整记录、不递归。全部为首测，非最终平衡或已实现证据。

## 7. Industry / Industrial Zone — IND

**D0045: DESIGN_FROZEN — 在D0044职责／首测值上追加每模板来源绑定、正式Gold/Faith、研习中断、专业单位保护与最终Floor；模板可靠性及历史合同保留，implementation / balance validation pending.**

唯一Industry新公式、范围、参数和中文Tooltip正文：[Industry content](Content/Industry_D0045.json)。[本轮接受与取代](../Historical/Design/Reviews/Industry_Culture_Future_D0045_Review.md)／[D0044既定职责](../Historical/Design/Reviews/Industry_D0044_Review.md)、[早期冻结审阅](../Historical/Design/Reviews/Industry_D0027_Review.md)。四机构累计永久存在；名称仍STRONG_CANDIDATE，机构不是普通engine Building。

| Rule ID | 当前权威content条目 |
|---|---|
| IND-001 | IND_BASE_SUPPORT / IND_INST_1匠作坊；无named ability |
| IND-002 | IND_L2_DIVISION / IND_INST_2百工会馆 |
| IND-003 | IND_L3_STANDARD、IND_L3_MOBILIZE / IND_INST_3工程局 |
| IND-004 | IND_L4_MACRO、IND_L4_PRACTICE、IND_L4_TRADITION / IND_INST_4土木工程总局 |
| IND-NET-001至005 | contracts.template_knowledge / standardization_scope / network，保留目录及已有合法Gold／Faith购买渠道；旧等级折扣数值、旧IV直接生产力输出被替代 |
| CREW-001至004 | contracts.teams及parameters；取代旧Lv1全档开放和普通区域/建筑施工目标，其余未推翻合同保留 |

**IND-TEMPLATE-006 — City Experience Reconciliation / ACCEPTED D0036** 模板属于这座城市可可靠确认的建设经验，不是当前玩家个人建造记录。合法首次取得工业身份，或已有工业城市进入／回到任意受支持Owner并恢复工业身份时，局部同步“可靠保存模板历史 ∪ 当前存在的合格建筑”。AI/非支持Owner时期建成但此时仍存在的合格建筑可补入；可靠历史不因当前缺失、拆除、掠夺或临时失效删除。明确区分首次初始化、已有历史恢复、当前事实同步与历史缺失/损坏：曾有历史但缺失/不可读时，不得把当前扫描伪装成首次初始化或完整恢复；保护继续生效。非支持Owner期间建成又消失、系统从未可靠记录的对象不追溯、不猜测，不要求AI监听或新全局建筑历史。目录、折扣、建造数值与其它专业Legacy不变。

**IND-HISTORY-001 — ACCEPTED D0040** 模板与工程实践的本城真实Wonder completion属于A城市历史，随城、与实际完成Owner无关；当前利用依Industry资格，工程实践需IV，Identity退出保留／暂停。本城实践可并入当前可证明完成事实，不猜历史。全国工程传统属于B实际完成文明历史，城市转移不转移信用；同一完成分别记录城市经验和文明信用。D0044工程实践仍IV门槛，N只降低施工队成本，不再强化标准化；全国E供本城L研习，不再解锁高档队。历史技术保护保留；Teams来源／容量生命周期见IND-TEAM-LIFECYCLE-001。

IND-REVIEW-01/02保留已接受暂行复审状态；03“模板与全局最高效率完全分离”由D0045正式取代。机构／能力候选名、五档队名和研习项目名保持成熟度。D0044既定首测值、III150%／IV按N折减、高档队按ACTIVE开放与固定注入不重复修改，不再把已给值标成公式TBD；实际强度待Balance Validation。

Research及其它未列条款不变；本轮Culture首测值和Commerce专业单位保护增量见其当前Content；共同Network topology保留。旧Industry条文在D0026冻结原文，不能与新能力叠加。其它段落若仍描述旧Industry向外直接输出，以本节新content取代该Industry含义；不据此自行重做Commerce收益。当前Mod尚未实现此新设计。

D0031有限库存问题已关闭：每具备工程动员资格的Industry来源城容量2，各档已完成队伍占1，四级不加；来源绑定、消耗/合法移除释放名额，离开Industry后已有队伍保留但不能补充。D0042已关闭来源易主／夺回计槽；单位本体不可捕获／转换Owner、保护回归原生接口待查，原Owner完全消失仍未定义。完整规则以content为准。

**IND-TRADITION-STUDY-001 — ACCEPTED D0044 / D0045中断增量** 全国E为B文明实际完成奇观自身时代去重历史，从游戏开始计、不要求工业；本城成功研习L为A城市历史。Industry ACTIVE IV且L<E可做完整1 Production Turn，成功提交L+1。IV来源输出建造10%＋2%×L、已有合法Gold／Faith购买折扣2%×L；III保留L／不研习，只输出基础10%／0%；低III或退出身份不输出；恢复IV直接恢复全部L。易主E<L不删除／降级／截断L，E只限制新增，不设五层／人工cap。明确采用与Dialogue相同完整1T事务、以Industry IV资格：ACTIVE不足IV（含总督离开）、Identity退出、REALLOCATING、Owner变化或正常生产中断取消本轮，无L、无半进度；重新合格且L<E重做完整1T，已提交历史L不变。不导入Dialogue时代额度／倍率。

**IND-PRACTICE-COST-001 — ACCEPTED D0044** 工程实践仍为当前ACTIVE IV能力，N为本城真实历史奇观数、不看完成Owner／Identity／ACTIVE／Governor。III成本统一150%；IV N0／1–2／3–5／6+为150／140／130／120%×锁定基础施工力，累计门槛1／3／6。只改组建投入，不强化标准化或队伍施工力。III开放I–III、IV额外IV–V，不要求E4／5或其它传统门槛。五档施工力250／420／750／1000／1360，标准速度首测成本完整表见content。

**IND-MACRO-INJECTION-001 — ACCEPTED D0044** 工业IV自行生产旧时代奇观：文明当前时代与奇观自身时代差1／2／3+对应+10／20／30%封顶，当前时代无加成。施工队严格只注入min(锁定基础施工力,目标剩余Production)，不接受巨构工程、奇观政策、城市modifier、宜居度或其它未授权生产倍率；余量浪费、不溢出或保存。原有劳动力／目标／容量／来源生命周期不变。

**IND-TEAM-LIFECYCLE-001 — ACCEPTED D0042** 完成施工队为独立原Owner资产，来源总督／ACTIVE／Industry Identity／Owner变化不删除或停止使用；永久训练来源只承担provenance与容量。合法来源当前Owner的存活本城出身队伍占2槽，消费／合法移除释放，存活撤退不释放；易主后旧Owner队伍不占新Owner容量，原Owner夺回重新计入其旧存活队伍。直接单位捕获／Owner转换明确禁止，敌方相关交互用保护撤退／安全回归；原生接口为Technical，非归属TBD。

**IND-STANDARD-SOURCE-001 — ACCEPTED D0045** 不同模板仍取并集；针对模板T，只从当前有效且实际掌握T的工业来源中，分别取最高建造效率与最高合法购买折扣，不跨无模板来源取全局max。A L7持大学／研究所、B L2持大学／银行、C L5持工厂，分别大学24%、研究所24%、银行14%、工厂20%；C不能放大银行。Gold或Faith都只作用于目标本来合法的购买价格，不增加许可、不绕过资格、价格字段不等于合法渠道。

**IND-PRECISION-001 — ACCEPTED D0045** 需要最终落整数的Industry Production／Gold／Cost使用Floor；不四舍五入／ceiling／补差，避免不必要中间Floor，不外推未授权的Commerce或GPP精度。

## 8. Commerce / Commercial Hub — COM

**D0045: DESIGN_FROZEN；保留D0039公式／首版值、D0040 C/D及S锁定、D0042 F配置与G来源，仅同步具名专业单位不可捕获／转Owner；不等于实现／平衡验收／技术通过。**

唯一机械合同：[Commerce D0045](Content/Commerce_D0045.json)；[A–D关闭与真实剩余边界](../Historical/Design/Reviews/Long_Term_State_D0040_Review.md)；[D0039公式接受](../Historical/Design/Reviews/Commerce_D0039_Review.md)；[D0032历史冻结审阅](../Historical/Design/Reviews/Commerce_D0032_Review.md)。机构与能力名全部LOCKED，四机构presentation-only累计展示，0/1/2/3仅为商业结构。

| Rule ID | 当前权威content |
|---|---|
| COM-001 | COM_BASE_SUPPORT：各级每工作专家额外3F3P；共同Trade Center保留 |
| COM-002 | COM_L2_GUILD：同业制度，沿用SHARED-001/002 |
| COM-003 | COM_L3_COMMERCIALIZE + COM_L3_INVEST |
| COM-004 | COM_L4_DEVELOP + COM_L4_RESTRUCTURE + COM_L4_REPUTATION |
| COM-005至009 | SUPERSEDED：旧Convergence20%/Actual/floor/incoming-only不叠加 |

商业化v0.1五域Campus→Science、Theater→Culture、Industrial→Production、Holy Site→Faith、Harbor→Gold；排除Commercial Hub与未映射Future。本地D×任意方向直接国内商路或本城合法最高X：每域0.1×D×X×(1+0.005×有效信誉)，信誉当前效果需Commerce ACTIVE IV，商业化Gold不得递归成为X。

资本投资仍一项两模式；每次本金=确认瞬间剩余国库25%，标准速度10回合，r=0.01DSC（C为商业化时1.25，否则1）。稳健P(1+r)、风险成功P(1+3r)，失败P(0.5+0.005×有效信誉)；p_base=min(0.8,0.4+0.01DS)，C不改概率。失败保护同来源城跨域共享，失败追回距80%上限25%，成功或Commerce Identity消失清零；确认时抽取/锁定/更新保护，到期只揭晓结算。UI显示总预期返还及扣本金后预期净收益，负净收益提示预期亏损但允许选择。同领域最多一笔未结算，作用域及S精确资格见剩余条目，不另设全国总数上限。D0040确认锁定具体S来源城与双方Owner关系；最高S相同选最早达到该等级，再稳定ID/key，存读档不随机换源。报价必须显示S城名／等级，保存P/D/S/C/r、mode/probability/outcome、maturity及settlement。

发展投资签约要求ACTIVE IV来源→目标直接国内出发路线，之后断路不改合同；初版10回合/目标域普通建筑+50%Production。P_ref=P_low+0.75(P_high−P_low)，只据人口与合法地块Food/Production，不据瞬时锁定/focus或非地块Food；标准报价0.75×4×(P_ref×0.5×10)=15P_ref金币。每工作商业专家1并行容量，降容量不撤旧约；全来源目标城+域至多一份，不同域可并行。与标准化Production百分比加算。已签资本/发展合同不因Governor/ACTIVE/Identity、商路或专家容量等普通变化取消；发展目标Identity变而目标仍合法亦继续。D0040关键城市Owner变化异常终止：资本Commerce城或锁S城任一换主，不返本金／不maturity／不走风险失败或修改保护；发展Commerce城或目标任一换主，不退款、撤+50%、立刻释放slot，不转交新Owner。

首次Commerce IV长期机构开始信誉计龄，标准速度保有Commerce Identity每完整回合+1，cap40；ACTIVE下降不暂停年龄，但当前两项信誉效果需ACTIVE IV。商业化每点+0.5%，风险失败本金返还每点+0.5个百分点；不影响稳健、成功利润、成功率、保护公式、发展投资或重组。信誉为持续Commerce机构关系，Owner变化不清零／分账／重置，非支持者冻结使用。失去Commerce Identity立即清零，重新建立从0，不机械套Research暂停保留规则。

重组团队首版500Production、仅生产训练，明确不可捕获／转Owner，敌方原可捕获／消灭的交互保护撤回且无主动删除；沿用P→P−1及至少5完整混乱回合（其它速度缩放待精确定义）、非Food产出/净余粮各−75%。配置前目标被征服立即销毁本次事务/未完成账本/旧当前身份并解散团队；原玩家后续夺回按PROG-011例外重新snapshot/Claim，不恢复半成品。

五域及主要公式/初值已定，不再沿用D0032对应TBD；初值仍可Balance调整。资本领域/S候选与等级/空池、同域并发作用域、改变基本面时隐藏保护组合、发展参考态/无解、X聚合、非标准速度及城市消失／目标非法、保护本身跨Owner等真实剩余项只按content登记。无新floor/上限/未来域映射。旧5F5P、网络类型专家加成、20%汇聚、单双向50/100等持续退出；共同中心接收分发不变。

**COM-LIFECYCLE-002 — ACCEPTED D0042** 商业化选择域及activation order是持久配置：容量减少LIFO暂停而非删除，容量恢复按原顺序前N项自动恢复；主动关闭删除，重开最新。保有Commerce Identity时总督／ACTIVE下降保留配置；Identity退出或易主清空；同Owner同身份读档先恢复配置、再按当前事实派生效果，信誉Owner保留规则独立。已训练重组团队不因训练来源总督／ACTIVE／Identity／Owner变化删除或转交；绑定后随目标REALLOCATING事务，训练来源仅provenance，其易主不能取消另一目标事务。目标易主仍执行既定销毁。

## 9. Trade Center与Network核心 — NET

**NET-001 — Capital self-connection / ACCEPTED（D0009纠正）** Trade Route Capacity本身就是网络带宽；不额外创建每路线载荷分配、round-robin或手动网络选择界面。首都与商业专业城市为Trade Center。当首都拥有Specialization Identity，其自身专业天然direct self-connect到本首都Trade Center，同时使首都成为该网络合法recipient并获得效果；可沿合法outgoing distribution routes继续分发。不要求虚构Capital→Capital或额外自接收资格。天然自身专业接入仍是首都规则，不泛化为所有中心自身专业自动接入；任何中心一旦直接接入网络，均适用NET-002的自然接收规则。

**NET-002 — Direct connection = receive + may distribute / ACCEPTED** 己方专业源S→己方Trade Center H的有效direct connection，使H接入该类型network set、自动成为该类型合法recipient并获得network effects，同时可作为分发中心。首都天然self-connection同样适用。无须H→H路线、Commerce IV或额外self-reception资格。H→己方城市D的每条有效distribution route自动携带H当前全部直接接入网络。H自身按city UID去重，只计一次。

**NET-003 — Distribution reception = receive only / ACCEPTED** 一条distribution route可同时使目的城进入Research/Culture/Industry等接收集合；外贸、道路或贸易站本身不等于这种己方direct接入。目的城即使也是Trade Center，也不会仅因收到distribution取得原source的direct connection、继续转发该网络或对原source进行Convergence，保持non-recursive relay。Direct接入、distribution接收及其它明确合法资格共存；失去一种而仍有其它有效资格时保留接收，但不会据接收资格反推直接来源。

**NET-004** 路线结束、取消、战争/征服/端点失效等使路线不再有效时，相关接入/接收资格撤销，不能仅因过去曾建立过路线而继续享受网络。读档后应反映当前真实集合，无需玩家打开贸易界面恢复网络。

### Research当前网络 / Culture旧网络历史 — NET-RC

**D0028适用范围覆盖声明：** 下列NET-RC条款继续用于Research；其中Culture/Eureka、k_C等描述只保留旧合同审计，不再是当前Culture规则。Culture以CUL-005为准，新网络按CUL-005合并完整考察文明集合；不得叠加旧Eureka奖励。Research标记NETWORK_REDESIGN_REQUIRED而未改公式。

**NET-RC-001** `Network Strength = k × L × sqrt(N)`。Research使用独立可调k_R，Culture使用k_C，初始测试均为1。结果是Research额外Inspiration百分点、Culture额外Eureka百分点。

**NET-RC-002** `N`是当前实际接收该类型网络的己方城市UID去重数量，包含直接接入的Trade Center及天然自接入的首都；不是source数、raw路线数、全帝国城市数或中心总路线数。同城direct接入、distribution、多中心或其它免费资格重叠均只计一次。未来其它合法接收方式进入同一去重集合。

**NET-RC-003** 多个当前有效接入的同类型来源，`L = max(all valid source ACTIVE specialization levels)`；使用ACTIVE而非Potential。来源数量本身不增加N。统一选L后只计算一次强度，禁止分别按来源求强度后相加，禁止`Σ(k × L_i × sqrt(N))`或逐中心求和。

**NET-RC-004** 最高等级源失效后立即回退到剩余有效源的最高ACTIVE。无有效来源时Strength归零，不保留stale Strength；N=0时Strength也为零。Research/Culture规则不自动扩展到其它机制：Military统一动员按Military_D0037分网络司令与当前生产兵种线规则；Industry按D0045不同模板并集、每模板仅在实际持有它的有效来源内择优；Community国内网络只分发人口。

**NET-RC-005** Research/Culture内部保持完整浮点：RawStrength=k_R或k_C×L×sqrt(N)，所有合法Network modifiers与未来Entertainment效率修正均在浮点上执行。仅在最终整数Boost接口边界量化一次：`AppliedBoost = floor(FinalRawBoost + 0.5)`（Boost非负）；显式使用此式，不使用默认round/banker's rounding，不提前量化、不重复量化。1.49→1、1.50→2、3.50→4；L4/N2原值约5.657→6个百分点。不同Raw值映射同整数时仅保持该AppliedBoost，不重复叠加；网络失效回零。正式权重1/2/3/4、独立k_R/k_C=1、L为有效来源最高ACTIVE、N为recipient UID去重不变。此规则取代D0017“浮点原样交引擎并接受截断不修复”。正式集成前以Raw1.5→接口2、Raw3.8→接口4最小原生测试确认；不再尝试让引擎保留fractional percentage points。不改变原生基础Boost规则，不假定固定40%；已触发Boost不补发、额外进度不得溢入下一科技/市政；最终封顶仍待确认。Entertainment具体效率参数未由本决定设定。

## 10. Future专业 — OUT_OF_V0.1

本章记录已确认未来范围及本次明确提供的机制；不因为记录进Spec就纳入v0.1实现。

### 原始首都一次性特殊改制 — CAPITAL-REFORM

**CAPITAL-REFORM-001 — FUTURE / DESIGN_RECORDED / NOT_V0.1_IMPLEMENTATION** 完整共同正式合同见Shared_D0045.concepts.ORIGINAL_CAPITAL_SPECIAL_REFORM及[阅读正文](Shared.md#未来记录原始首都一次性特殊改制)。原始首都城市实体每局一次，迁都不转移；保留Potential，无普通P−1／REALLOCATING5T／Team。三阶段各完整1T，前两阶段纯RP无奖励；第二阶段成功锁当前合法候选，后建区域不追加；第三阶段选目标、成功再核验真实合法区域后切Identity／保留Potential／重算ACTIVE／消耗一次权利。普通中断仅当前阶段重做，已成功前置保留；完成前Owner变化清空全部阶段／候选／事务但未成功第三阶段不消费权利。目标真正消失／非法时第三阶段失败，不切身份、不消费权利且保留前两阶段；掠夺／暂损不等于消失。默认所有合法专业，Civic／市政允许，Diplomatic暂排待未来重构复审；名称占位。无P0/P1／milestone／runtime任务／当前测试，不扩大四专业实施。

### Landscape / Preserve — LAND

**LAND-001** Landscape主动经营高Appeal景观，而不是要求地块一律保持未开发。属于Future；Canal联动见CAN-001，不用Great Work的Landscape类别代替本专业。

**LAND-002 — Lv1** 对通常降低Appeal的资源改良进行环境友好化：消除/抵消其负面Appeal影响。战略资源、加成资源方向提供Science型补偿；Luxury资源方向提供Culture型补偿。具体每资源数值TBD，不禁止改良资源。

**LAND-003 — Lv2** 提前获得/使用植树等主动提高Appeal的能力；符合条件的资源改良、农渔类改良等可积极参与Appeal建设，不限于未改良地块。具体improvement资格、Appeal数值及提前可用时点TBD。

**LAND-004 — Lv3** 建立`Appeal → Gold → Tourism`景观经济链：符合条件的高Appeal改良先根据Appeal产生Gold，再根据该Gold产生Tourism。不是每点Appeal直接换固定Tourism。资格/高Appeal门槛及两阶段系数TBD。

**LAND-005 — Lv4** 提前获得Naturalist，在正常晚期窗口前主动建立National Parks，并进一步强化National Park与高Appeal景观改良之间的联系。提前可用时点和强化公式TBD。

**LAND-006 — Network** 提供/改善Amenities，并强化正Amenities带来的非Food yield bonus，不是城市固定增加全产出百分比。用户给出的Great Scientist全国“positive Amenity bonus to non-Food yields +40%”是机制参考，**不是Landscape已接受倍率**。Amenities供给、专业等级/Network Support到强化倍率的映射TBD；未来Entertainment Regional Support可提高其效率，见ENT-003。

### Religion / Holy Site — REL

**REL-001** 以宗教教育、宗教稳定、神学战争和对被击败宗教思想的主动吸收为主题。属于Future；外交Holy Site任务和Canal联动见DIP-MISSION、CAN-001。

**REL-002 — Lv1** 实际工作的Holy Site专家获得common specialist support，当前模板方向为+3F/+3P，减轻安排专家的产出代价；目的不是强化Great Prophet竞争，不由此推导Prophet GPP奖励。

**REL-003 — Lv2** Holy Site及其建筑继承SHARED-001住房支持。每名working Holy Site specialist提高本城训练宗教单位的**Theological Combat Strength**，不是普通combat strength；每专家数值TBD。Great Prophet基础GPP未有明确接受数值，不为对称而自行添加+2或其它奖励。

**REL-004 — Lv3** working Holy Site specialists支持提升至+5F/+5P，替代Lv1档位，不重复相加。本Religion专业城市自身高度稳定/锁定为玩家创立的宗教；working Holy Site specialists按人数降低其它己方城市受到的foreign religious pressure。不是全国人口无条件永久锁教。本城锁定的玩法/技术边界、外国压力减免公式及多来源作用方式TBD；外国传教+200 pressure后按比例削减仅为概念例子，不是确定参数。目标是减少反复洗教微操并支持每信徒收益的belief。

**REL-005 — Lv4** 洗掉/征服其它宗教Holy City并满足最终资格后，玩家从该被击败宗教实际拥有的beliefs中**主动选择吸收**，不自动复制全部，也不限于祭祀建筑能力。允许选择有战略价值的思想，例如Feed the World、Choral Music；Follower/Founder/Enhancer等类别是否全部开放仍待最终规则。每个被击败宗教可选数量、类别范围、重复/冲突处理和触发资格TBD，不退化为Saint Basil/Hagia Sophia式自动复制祭祀建筑能力。

**REL-006 — Network** 通过贸易路线大幅强化己方宗教传播压力，使宗教贸易传播具有战略意义。具体pressure multiplier/value TBD；强度与专业等级、接收/连接规模相关，但不自动套用Research/Culture公式，除非用户另行确认。

### Military / Encampment — MIL

**MIL-D0037 — DESIGN_FROZEN / NAMING_ONLY_AMENDMENT** 唯一当前内容正文：[Military D0037](Content/Military_D0037.json)。仅行伍制度→行伍编制、后勤编制→战地勤务，玩法合同保持D0034；[冻结机制审阅](../Historical/Design/Reviews/Military_D0034_Review.md)、[本轮接受与冲突登记](../Historical/Design/Reviews/Harbor_D0037_Review.md)。旧MIL-001至013原文保留于D0032及更早snapshot，不与新能力叠加。

| Historical rule | Current authority |
|---|---|
| MIL-001/005 | 全级3F3P、II住房和+2baseGeneralGPP保留；+15%CombatXP退出 |
| MIL-002/007 | III5F5P退出；Insight公式移至IV，E改为出生时锁定，P仍读取当前实际晋升 |
| MIL-003/009 | 旧驻扎训练退出，IV仅战阵传授/沙场领悟/军略传承 |
| MIL-010–013 | 旧Mentorship公式重用并限同PromotionClass；单位永久出生buff/合并同能力max取代动态来源城依赖 |
| MIL-004 | 旧全国pool/自动送兵退出；统一动员按每个不相连网络选司令，匹配整个归一化升级兵种线 |

综合训练同一能力内：五领域合格T1各提供永久出生+1CS（最多5）；相同五领域的Shared绝对D还支持本城训练效率，T1-only不提供深度收益、T2阶段开始贡献，转换公式/汇总/精确门槛/购买适用后置。不以区域100%完成或D10为启动条件，不新增相对完善度指标。

Military设计冻结不等于implemented/balance complete/实机通过；当前P0计划未授权实现Military。命名占位、后勤资源覆盖、Balance、Technical与Legacy见content登记。Harbor经D0037明确授权镜像当前Military机制，排除统一动员；Harbor数值TBD不由Military数值自动补齐。Aerodrome旧扩展仍未自动适配。

### Harbor：完整双线 — HARB

**HARB-D0037 — ACCEPTED FUTURE BASELINE** 唯一当前完整内容：[Harbor D0037](Content/Harbor_D0037.json)；[中文阅读版](Harbor.md)；[接受、取代及未决审阅](../Historical/Design/Reviews/Harbor_D0037_Review.md)。机制接受不升级候选名称、Balance、技术或Legacy，不代表已实现。

100%海运商业＋100%海军同时成长；Lv1/II共用机构，Lv3/IV商业与海军同级并存，非二选一。Lv1保留基础支持；II船员编制；III港际联运、通商万邦、综合训练、远洋勤务；IV集货出洋、舶来采长、久航成业、舰阵传授、怒海真知、海略传承。名称成熟度见content；不按其它专业0/1/2/3排列强行删减。

出口只读Base Adjacency，先加入路线价值再组合市场广度倍率；进口按每外国文明关系0→1锁类型、1→0消失；经营时间仅ACTIVE IV且有有效海上路线时每回合+1，不按路线数或完成次数。失去ACTIVE IV只暂停经营进度；已得航线容量不因调走总督或暂失ACTIVE IV撤销。其他owner/身份/城市摧毁Legacy未定。

旧HARB-001双线及HARB-003本城海洋资源基础相邻范围保留；HARB-004自身Actual高比例出口退出。旧HARB-005至009的海军动员、II+15%XP、III动态E领悟、驻扎训练和旧传授由当前Military镜像替换；历史原文见D0036快照，不叠加。不设额外Harbor Network Ability，也不镜像统一动员/司令城。旧HARB-002未定大商人点数/改良产出措辞未被补成新能力，待明确范围，不作为暗含收益。

### Government Plaza — GOV

**GOV-CONTENT-001 — ACCEPTED FUTURE BASELINE / OUT_OF_V0.1** 市政／Government是国家治理中枢（Meta-specialization），成长为基础行政→常设内政体系→制度整合→国家政策中枢。完整机械内容、参数与逐项未决以[Government D0047](Content/Government_D0047.json)为本专业结构化权威；中文完整阅读见[市政](Government.md)。不进入当前四专业实施范围；共同Identity/Potential/ACTIVE与机构展示遵循Shared，不强制其它专业的无名Lv1结构。

| 等级／机构 | 本级能力 | 已接受机制与参数成熟度 |
|---|---|---|
| I 治所 | 基础市政支持 | 每个合格本城市政建筑＋G Food／＋G Production；G为当前Government Tier，I–IV对应1／2／3／4 |
| II 内政司（Placeholder） | 政令通达 | 显著减免主动政策重新配置的Gold费用，折扣TBD；不增第二能力 |
| III 典制院 | 兼采诸制 | 先拥有同Tier一栋Government Plaza建筑，逐栋项目「建制考论」学习其它制度；标准速度每栋I／II／III为完整1／2／3生产回合，补全另外两栋共2／4／6T，总12T；其它速度缩放，不被高Production压缩；只获长期／持续效果，不重复一次性奖励 |
| III 典制院 | 政制取鉴 | ACTIVE III完整1T「政制择用」（项目名Placeholder），选择当前Tier及以下其它政体的一项Legacy；同时最多1、不占槽、直接生效、可重选，不与当前政体自身Legacy重复；政体变化后非法／自身重复效果不得生效 |
| IV 国策府 | 多元统筹 | ＋N Wildcard Slots，N为当前不同非市政ACTIVE IV专业类型数；同类多城只算1，Potential IV不足；资格消失撤销、恢复重算，不保存历史槽位 |
| IV 国策府 | 因时制宜 | 每回合第一次玩家主动完整政策重新配置免费；非每卡／无限重配，不影响原生Civic完成／政体变化等免费机会，不自行加cooldown |
| IV 国策府 | 治理效能 | 全国All Yields按当前Government Tier G增加k×G；k初测候选每Tier1个百分点（I–IV为1／2／3／4%），非永久冻结值；All Yields精确集合另行明确 |

**GOV-STATE-001 — 具名状态与未决边界** 已完成制度学习属于城市长期制度积累，临时Governor／ACTIVE失效不得清除成果；具体Identity退出、Owner变化／夺回、当前效果启用及未完成多回合项目处置未冻结，不套用其它专业。当前吸收Legacy属于制度配置，保存／暂停／Identity退出／易主等生命周期仍TBD；政体变化后保留配置暂停或其它表现未选定。Wildcard、免费重配与全国产出均为当前派生能力，不是历史资产；各自资格按本级及Shared规则。

**GOV-SUPERSESSION-001 — obsolete** 旧GOV-001自动免费补齐其它同Tier建筑→逐栋制度学习；旧GOV-002按Potential累计永久＋4 Governor Titles取消；旧GOV-003 `W=min(ACTIVE,Government Tier)`→当前非市政ACTIVE IV专业多样性N；旧GOV-004忠诚度Network及其数值待决退出。旧原件仅历史，不作为附加效果保留。本轮不新增市政独立Network Ability；Canal与国事访问既有独立未来交互仍见CAN-001／DIP-MISSION，不借本轮重构它们。

**GOV-OPEN-001 — 分层未决** 内政司／政制择用保留Placeholder；政令通达折扣未定、k仅首测候选。建筑资格／长期效果承载／一次性奖励分离、完整多回合项目与速度缩放、Legacy目录／无槽直接作用、动态政策槽／完整配置交易与原生免费机会区分、All Yields精确范围及承载均待Technical／Design detail；不展开兼容表、不补公式。Wildcard边际价值及少量具体HD即时政策套利留后续实测，不据此增加机制限制。

### Diplomatic Quarter — DIP

**DIP-001** 保留三条完整设计线：City-State/protectorate、Spy/visibility、Alliance/Diplomatic Missions。具体跨级保留与下述未定收回行为须区分。

**DIP-002** 永久保护国名额Lv1–4分别为1/2/3/4。其宗主权不可被替换；与玩家和平的主要文明不能向这些保护国宣战。“允许宣战，然后自动把玩家拉入战争”不是可接受fallback。名额作用域、取得/更换资格以及ACTIVE下降或来源丧失时永久保护与额度的关系DESIGN_DECISION_REQUIRED。

**DIP-003** 使者奖励强化：Lv2将1-envoy tier +100%；Lv3再将3-envoy tier +100%；Lv4再将6-envoy tier +100%。不是直接倍增复杂Suzerain ability。

**DIP-004** Global Diplomatic Visibility随Lv1–4分别+1/+2/+3/+4。多个外交来源如何作用仍TBD，不擅自加总。

**DIP-005** Lv1 +1 Spy Capacity；Lv2 failed-but-surviving任务仍获得经验，并减少无意义周转；Lv3降低任务失败时死亡概率，不提高成功率；Lv4任务仍可失败/被捕，但不会死亡。经验量、周转变化与Lv3死亡减幅TBD。

### Alliance Diplomatic Missions — DIP-MISSION

**DIP-MISSION-001 — Future Advanced Module / ACCEPTED FRAMEWORK** 非盟友使用Spy，盟友使用Diplomat；优先复用Spy unit和现有district-targeted mission交互框架，不进入v0.1。本章各任务的具体成熟度分别保留，不因文档接受而把PROVISIONAL或candidate升级。

**DIP-MISSION-002 — 统一原则 / ACCEPTED** 不要求敌对Spy任务逐一有和平镜像；一个区域可有多个外交任务，也可暂时没有accepted mission。各任务服务不同玩法与区域主题，不全部转成flat Gold/Science/Production。Campus偏知识，Theater偏文化宣传，Commercial偏商业/产品/商品，Neighborhood偏移民，Industrial偏基础设施，Harbor偏海贸，Encampment偏军事合作，Holy Site偏宗教交流，Spaceport偏高级研究。保留高质量候选，不为填空加入能力。

**DIP-MISSION-003 — 成功与奖励 / ACCEPTED FRAMEWORK，参数TBD** 成功任务原则上继续给Spy XP及Era Score，尽量保留现有Influence相关Spy promotion价值。任务成功不保证secondary reward触发，例如成功交流也可不产生Eureka/Inspiration。外交专业等级/Alliance等级解锁、任务周期、基础奖励与晋升适用范围仍TBD；不统一填数值。

| 目标区域 | 任务 | 成熟度／玩法 |
|---|---|---|
| City Center | Gain Sources | 保留概念，提高本城后续外交任务成功率/执行能力，参数TBD |
| City Center | Public Diplomacy／公共外交 | PROVISIONAL REWARD：主要Alliance Points，Favor为次要候选 |
| Commercial Hub | Business Delegation／商业代表团 | 按玩家与目标盟友实际国际商路及其产出，给予一次Gold；倍率TBD |
| Commercial Hub | Product Expo／产品博览会 | 按己方Product Great Works产生即时Tourism burst；不移动/转让产品，倍率TBD |
| Commercial Hub | Import Fair／商品引进会 | 限时获得盟友有、玩家没有的奢侈资源类型供应资格；细节TBD |
| Campus | Academic Exchange／学术交流 | 成功后有概率随机触发合法未触发Eureka；概率TBD |
| Theater Square | Promote Great Works／宣传巨作 | 按己方巨作即时Tourism burst，不移动巨作；倍率TBD |
| Theater Square | Promote Attractions／宣传景点 | 按己方产生Tourism的景观/改良即时Tourism burst；分类及倍率TBD |
| Theater Square | Cultural Exchange／文化交流 | 成功后有概率随机触发合法未触发Inspiration；概率TBD |
| Neighborhood/Community | Migration Agreement／移民交流协议 | 临时强化目标盟友这一份国际移民压力；约10回合仅候选 |
| Industrial Zone | Infrastructure Coordination／基础设施协调 | PREFERRED DESIGN CANDIDATE，技术可行性待Development审查 |
| Industrial Zone | Civilian Conversion／军工民用化 | THEME CANDIDATE ONLY，无最终reward |
| Spaceport | Joint Space Research／联合航天研究 | 晚期Eureka合作方向；概率、时代范围TBD |
| Harbor | Maritime Trade Agreement／海运贸易协定 | 临时强化双方商路持续收益；参数TBD |
| Encampment | Joint Military Exercise／联合军演 | 以双方较弱军力及强递减函数决定少量军队XP；公式PROVISIONAL方向 |
| Holy Site | Pilgrimage／朝圣 | 兑现目标盟友信徒对应的合格belief yield，不施加宗教压力；系数TBD |
| Diplomatic Quarter | Summit/Embassy Activity | Future骨架：Alliance Points/Favor/Influence组合TBD |
| Government Plaza | State Visit／国事访问 | Future骨架：Era Score/Alliance Points/Influence及高层外交收益TBD |

**DIP-MISSION-004 — City Center** Gain Sources继续服务后续外交行动，无须因和平任务而删除。Public Diplomacy主题为公开采访、媒体活动、外交访问与公共交流；主要奖励倾向Alliance Points，Diplomatic Favor为次要候选，状态PROVISIONAL REWARD。Influence倾向主要服务外交专业City-State/Suzerain线，不优先作为公共外交核心收益。Foment Unrest、Neutralize Governor暂不需要和平镜像。

**DIP-MISSION-005 — Commercial Hub三任务** Business Delegation根据玩家与目标盟友真实存在的国际商路及其产出形成一次金币奖励，不扣盟友金币，商业联系越强任务价值越高，倍率TBD。Product Expo服务Corporation/Product文化胜利路线，仅根据己方Product Great Works即时产生旅游业绩，不移动或转让产品，倍率TBD。

Import Fair从目标盟友拥有而玩家没有的Luxury Resource types中引进一种，不要求对方第二份、不扣对方库存。获得有时限的import/supply资格，不永久创造地图资源。必须防止无限刷同一Luxury；首选限制方向为同一(Player, Ally, Luxury Type)成功引进次数有限，甚至一局一次；duration、selection、repeat limit均TBD，次数方向未锁死。

**DIP-MISSION-006 — Campus** Academic Exchange成功后有概率随机触发一个当前合法且未触发的Eureka，不保证每次成功都有突破。未触发仍可作为任务成功获得Spy XP/Era Score。概率TBD。“未随机触发则从盟友已研究而我未研究科技获取Eureka”仅为未来balance fallback candidate，第一版默认不启用；取代此前成功必定随机触发的描述。

**DIP-MISSION-007 — Theater三任务** Promote Great Works按己方Great Works产生即时Tourism burst，不移动巨作；作品适用范围/倍率待明确，不擅自等同Product Expo。Promote Attractions按己方产生Tourism的景观/改良形成即时Tourism burst，支持improvement tourism路线，合格分类与倍率TBD。Cultural Exchange有概率随机触发合法未触发Inspiration，任务成功可无灵感；未触发后从盟友已完成而我未完成市政获取Inspiration仅为未来balance fallback candidate，不默认启用。旧文化交流/巡展的巨作宣传作用归入Promote Great Works，避免同名效果冲突。

**DIP-MISSION-008 — Migration Agreement** 成功后一定时间仅提高目标盟友对应那一份Attractiveness-based International Immigration Pressure，不强化全球所有文明贡献。基础Community每个已接触文明贡献一份压力的框架保持；任务只作该盟友份额的临时修正，不改变其它份额。RP为签证便利、劳动力流动、移民协议、人员交流。约10 turns仅balance candidate，duration/multiplier TBD；Community原PROVISIONAL状态不升级。

**DIP-MISSION-009 — Industrial候选** Industrial是重要区域，但不强塞第二Eureka、flat Production或与玩家Industry IV Template Ledger高度绑定的任务。

Infrastructure Coordination为**PREFERRED DESIGN CANDIDATE**，并标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`：任务成功后一段时间，玩家与目标盟友边境/范围内城市临时跨Player共享合格Regional Building radiation effects。仍遵守HD原radiation range、same-name uniqueness、same-tier/same-category限制及建筑正常资格，不人为扩大范围。主题为工业基础设施、区域服务、电网/物流、公共设施标准协调。若以后Development判断只需较小Requirement/Owner条件调整，优先采用；若需每回合扫描双方所有城市、人工重模拟整个辐射体系或大量高维护状态，可返回Design寻找替代任务。本轮不调查HD代码，候选不升级为accepted任务。

Civilian Conversion为**THEME CANDIDATE ONLY**：保留`R = |Strategic Types_us union Strategic Types_ally|`（双方已解锁战略资源类型并集）支撑民用工业收益的主题，尚无干净独特且成本合理的最终reward，不强行赋Science/Production/Amenities。

**DIP-MISSION-010 — Joint Space Research** 目标盟友已有Spaceport时开展极晚期catch-up/joint advanced research，方向为触发后期Eureka，优先Information/Future Era，可比普通学术交流更稳定。是否100%、精确时代范围和无合法Eureka时处理TBD，不直接增加Space Race Production，也不修改SPACE自动联网规则。

**DIP-MISSION-011 — Maritime Trade Agreement** 一段时间强化玩家与目标盟友之间Trade Routes收益；区别于Business Delegation一次Gold，本任务是持续海贸收益。Duration、eligible routes、yield types、multiplier TBD，不提前决定具体数值。

**DIP-MISSION-012 — Joint Military Exercise / PROVISIONAL公式方向** 根据双方Military Strength给玩家军队一次少量XP；先取`S = min(Player Military Strength, Ally Military Strength)`，再用sqrt(S)、log(S)等强边际递减函数。`XP = floor(k * sqrt(S))`仅概念示例，k与最终函数TBD；目标是两个强盟友能办更大军演，但不能按AI高军评线性转成全军几十/上百XP，奖励必须克制。具体受奖军队范围和其它未指明边界TBD。

**DIP-MISSION-013 — Pilgrimage** 不直接施加宗教Pressure，不把盟友关系转成宗教攻击。按目标盟友文明中信仰玩家宗教的Followers，集中兑现合格foreign-follower-based belief yields：`Pilgrimage Reward = X * eligible follower-based belief yield`，X TBD。只兑现可表达为信徒数量→yield的收益；按外国信徒/信教城市产生可量化收益的belief可纳入后续资格确认，例如Tithe、Cross-Cultural Dialogue类。不得自动复制Combat modifiers、purchase permissions、building unlocks、pressure或其它非yield规则。主题为已有外国信徒的大型朝圣所带来的宗教经济、文化、知识交流；belief白名单与精确计量TBD。

**DIP-MISSION-014 — Diplomatic Quarter/Government Plaza / Future骨架** Summit/Embassy Activity保留Alliance Points、Diplomatic Favor、Influence方向，具体组合TBD。State Visit保留Era Score、Alliance Points、Influence及高层国家外交收益方向，具体机制TBD，不在本轮强行定稿。

### Community / Metropolis — COMM

**Framework Status: PROVISIONAL BUT ACCEPTED FRAMEWORK.** 用户已接受以下核心玩法框架及第一版公式，尚非最终数值定稿。Community仍属于Future / OUT_OF_V0.1；Local细节、权重与最终平衡继续保留PROVISIONAL/TBD，不因D0003接受而变为最终参数。

**COMM-001 — 特殊专业候选 / PROVISIONAL** 保留HD中的Community/Neighborhood不是普通specialty district、不占普通区域容量且解锁较早的设计背景，允许特殊Community专业候选。暂定在其它专业身份确定前完成一个Neighborhood即可取得资格，一个暂定足够；Lv2–4仍正常消耗Settler并要求Governor。取得资格是否立即锁定及与共同锁定规则的优先关系仍须明确。

**COMM-002 — Metropolis / Population Hub** 核心是人口枢纽，不是生育专业或单纯Population Growth加成。职责分为Local承载人口、International Immigration从外部世界吸引新人口、本国Domestic Distribution Network自动分配超过本城人口基盘的可输出人口。核心循环：`Foreign World → Metropolis → Domestic Network → Empire`。国际移民增加帝国总人口；国内分发只重新分配已有己方人口，不制造人口。不从具体AI城市扣人口，也不追踪移民来自哪个外国城市；移民叙事允许未来大幅调整数值，不把它解释成短期出生成年人。

**COMM-003 — Domestic Distribution Network / PROVISIONAL BUT ACCEPTED FRAMEWORK** 取代旧Domestic Migration进度模型：不再以`k × L × sqrt(N)`作为主要国内人口网络公式或人口生产速度。网络只分发本城已有人口／International Immigration形成的可输出Population。

只要Domestic Distribution当前开启、Source Population > Protected Population Floor，且至少存在一个合法network recipient，就尽量把超过本城人口基盘的可输出人口分发出去。国际移民先使Metropolis +1 Population，然后进入国内分发判定；符合资格时Metropolis −1、一个合法recipient +1；不符合则人口留在Metropolis。分发不仅服务新到移民，也可疏散现有超出基盘的人口。具体分发频率／每次批量仍TBD，不擅自限定为每名新移民触发一次或增加人口生产进度门槛。不创建Migrant单位，不需玩家每回合逐次选城，不增加额外人口单位UI。

**COMM-004 — Recipient自动选择 / 第一版原则** 先满足合法网络接收资格、足够Housing、Amenities不处于明显不宜接收人口的状态。合格目的地优先较低Population；同人口优先更多Housing余量；再相同优先更高Amenities；完全相同时可随机或稳定tie-break。精确权重／排序、Housing充足标准、Amenities资格界限和最终tie-break仍TBD。目标是人口自动流向边际人口价值较高且确有承载能力的城市，玩家无需逐次操作。

**COMM-005 — Protected Population Floor / TBD** 保留人口保护基盘作为自动分发安全阀，不能无限抽空都会。early/basic Community约10、more developed约15、fully developed metropolis约20仅是平衡参考，不锁定最终数值。Floor由Community建筑等级、Specialization level或两者组合决定仍TBD，取代旧稿仅按建筑tier提高的确定性表述。Population ≤ Floor时国内分发停止，国际移民仍可继续。若城市原在Floor，新移民使其达到Floor+1，且分发开启并有合格recipient，可将新增人口再次分发出去。

**COMM-006 — 专家支持与Local等级结构 / PROVISIONAL BUT ACCEPTED FRAMEWORK** 原生Community专家基础约1F+1P，HD建筑另提供较多Gold，作为设计背景而非本次新增收益。Community I每名实际工作专家额外+3F/+3P；Community III提升为额外+5F/+5P，替代Lv1档位，不重复叠加。因此Lv3专家大致为6F+6P及HD建筑Gold。目标是专家至少能养活自身、大量服务业人口不成为纯粮食负担；不额外复制HD已有Gold体系。

| 等级 | 当前暂定结构 |
|---|---|
| Lv1 | 专家额外3F3P；建立Attractiveness及International Immigration基础能力 |
| Lv2 | 强化Housing／人口承载，Housing与Amenities成为更重要的吸引力基础；具体额外Local能力TBD |
| Lv3 | 专家支持提升至5F5P；Domestic Distribution进入成熟状态；其它Local能力可后续补充 |
| Lv4 | 世界都会，高Attractiveness／国际移民体系充分发挥；累计国际移民生成Settler，阈值暂定8 |

不为等级条目数量对称强加能力。大量Neighborhood／专家槽的cap或递减仍TBD；“Lv3成熟”不擅自解释成低级别必然禁用国内分发，精确等级边界待后续细化。

**COMM-007 — City Attractiveness / 第一版PROVISIONAL公式** `A = H + 2M + D + 2E`。

| 项 | 定义与贡献 |
|---|---|
| H | `max(0, Housing − Population)`，使用空余住房，不是总住房；人口增加自然减少余量，形成负反馈 |
| M | `max(0, Positive Amenities)`；每1点正宜居度贡献2吸引力，负宜居度不会令该项或移民压力变负 |
| D | `B1 + 2*B2 + 3*B3`；B1/B2/B3是已完成对应Tier区域建筑的数量，每栋分别贡献1/2/3；具体区域／建筑分类TBD |
| E | 实际工作Community专家人数，每名贡献2；空槽不算 |

D奖励已完善的就业、教育、商业、工业、文化及城市服务，不奖励裸拍区域数量。ENT Local Support虚拟／有效专家是否计入A仍为独立Design Decision，本轮不决定。系数是第一版，不代表最终实测平衡。

**COMM-008 — International Immigration / 第一版PROVISIONAL公式** 借鉴Tourism向已接触文明输出的结构：

- `Immigration Progress per turn = A * C_met`。
- `C_met`为当前已遇见且仍存在的其它主要文明数量。
- `Immigration Threshold = 100 * C_map`。
- `C_map`为本局主要文明总数的地图／开局基准值；是否包含玩家自身、已灭亡文明等精确计数边界TBD，不直接等同当前C_met。

进度达到阈值时，本Community城市+1 Population、International Immigrant Count +1、扣除Threshold并保留overflow，再进入Domestic Distribution判定。大额进度的同回合多次结算细节TBD。前期接触文明少则移民慢，中期接触世界自然加快，后期可高频吸引人口；地图文明更多时阈值同步扩大，避免地图规模使收益直接线性爆炸。系数100及整套公式保持第一版平衡状态。

**COMM-009 — Population Policy Projects / PROVISIONAL BUT ACCEPTED FRAMEWORK** 项目完成后切换持续状态，不需持续运行项目维持效果，供玩家低频调整人口策略。

| 项目／状态 | International Immigration | Domestic Distribution | 用途 |
|---|---|---|---|
| Open Metropolis／开放大都会（默认） | 开启 | 开启 | 国际入口与国内枢纽的正常循环 |
| Restrict Immigration／限制入境 | 暂停 | 继续开启 | 暂停吸引国际人口，同时向国内疏散本城已有可输出人口 |
| Population Retention／人口留存 | 继续开启 | 暂停 | 先养大本城，达到人口节点、增加工作人口／区域槽及其它人口收益 |

限制入境时当前Immigration Progress保留、不累积；恢复后从保留值继续，不补发暂停期间进度。人口留存期间新移民继续进入本城，不自动分发；之后完成开放大都会可恢复分发。当前只有三个模式，保留名称和RP方向，不强制新增完全关闭模式；项目成本、开放时点等未指定细节TBD。

**COMM-010 — Community IV / Settler reward** 正式保留累计吸引International Immigrants生成Settler的机制。计数依据是成功吸引的国际移民累计数，不是本城人口净增、国内分发后剩余人口或实际留存人口。移民入城后立即国内迁移仍计数。

第一版`8 International Immigrants → 1 Settler`为**PROVISIONAL BALANCE VALUE**，不是最终锁死值。达到阈值生成1 Settler、Count减去阈值（当前候选8）、保留overflow；长期累计吸引量与奖励扣除后的余额语义需区分，已分发人口不撤销已获得计数。Lv4以前吸引的人口是否追溯用于奖励等未明确边界TBD。

目标是补偿此前多个Settler的专业投资，让成熟都会通过长期国际移民重新形成扩张人口；产出应明显但不成为高频无限爆铺。未来阈值可调6/8/10/12等，不改变机制，不在本轮擅选替代数值。

**COMM-011 — 未定范围与设计边界** Community保持PROVISIONAL BUT ACCEPTED FRAMEWORK：Local Lv2/IV细节、吸引力权重与最终数值尚未完成平衡；COMM-001资格锁定、专家槽递减、建筑计入分类、C_map边界、目的地资格／排序、保护基盘、分发与等级细节、项目细节及Settler计数边界继续TBD。旧迁移主题、目的地偏好和保护基盘已吸收进新循环，旧Migration进度模型被COMM-003取代。所有技术疑问仅标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`；本轮不调查已接触文明、人口增减、项目切换、Settler生成或吸引力UI，也不修改Architecture、Status、Source、Tests。

## 11. Future辅助系统 — OUT_OF_V0.1

### Entertainment / Water Park — ENT

**ENT-001** 三个等级建筑逐栋区分Local Support或Regional Support，允许3L/0R、2L/1R、1L/2R、0L/3R。具体选择/替换方式TBD。

**ENT-002** Local Support由positive Amenities与Local building count形成Virtual/Effective Specialists。不是真专家，不占人口/槽，不给native specialist yields，不给3F3P/5F5P，不给GPP；只增加本设计自制专业机制读取的specialist count。各机制是否读取该有效计数须明确映射，不能绕过这些排除项。

**ENT-003** Regional Support由positive Amenities与Regional building count形成Network Support；不提高effective specialization level。Research/Culture未来强化k或最终Network Strength，不恢复每路线线性百分点；其它专业按各自network efficiency解释。公式、区域范围和多建筑/来源叠加TBD。

### Aqueduct — AQ

**AQ-001** 每人口Food消耗减免=`0.1 × ACTIVE L × Aqueduct building level`。当前两级为tier1 Aqueduct building、tier2 Sewer。Lv4且两级时每人口减免0.8 Food，20人口合计每回合节省16 Food；不改成Food产出倍率。

### Dam — DAM

**DAM-001** 有Hydroelectric Plant后，额外Power=`X × ACTIVE L`。X TBD，不自行给值。

### Canal — CAN

**CAN-001** 相邻已改良地块按本城ACTIVE专业等级L获得对应yield：

| 专业 | 每级L额外yield |
|---|---|
| Research | +1 Science |
| Culture | +1 Culture |
| Industry | +1 Production |
| Commerce | +3 Gold |
| Landscape | +1 Food |
| Religion | +1 Faith |
| Military | +1 Production |
| Harbor | +3 Gold |
| Government | +1 Food |
| Diplomatic | +1 Food |

**CAN-002** 本能力粗略换算为`1S = 1C = 1P = 1F = 1Faith = 3G`，只适用于该能力，不扩为全项目通用平衡兑换率。原则上替代HD原相邻改良+6Gold，不叠加；原Canal贸易/Product机制保留。多Canal重复邻接、跨城市地块归属与Community对应yield尚未说明，TBD。

### Aerodrome / Airport — AIR

**AIR-001** Hangar使Military专业训练/XP体系扩展到air units；不创建Air specialization。未定训练数值不自动补全。

**AIR-002** Airport覆盖/移除Aerodrome负Appeal，相邻地块+1 Appeal；相邻已改良地块根据positive Appeal产生Gold，再由Gold产生Tourism。工业改良也可参与。系数及多机场重叠计数TBD。Airport不自动接入专业网络。

### Spaceport — SPACE

**SPACE-001** 玩家完成Launch Earth Satellite后，仅拥有Spaceport的己方城市自动双向参加国家专业网络：其自身专业自动接入Trade Center，同时自动接收Trade Center当前全部已接入网络。不占Trade Route Capacity，不要求实际distribution route。

**SPACE-002** 不是全帝国所有城市自动联网。它主要服务very-late-game network automation/QoL，不增加Space Project Production、Science、Production或Laser Station效率。自动接收城市进入NET-RC的同一去重N集合。

## 12. 未决、候选与资料缺口清单 — OPEN

以下保留为可审核问题，不由Codex给出隐含答案。确认一个Future范围不等于确认其中未提供的数值。

| ID | 状态 | 未定内容 / 相关规则 |
|---|---|---|
| OPEN-01 | TBD | Landscape资源补偿、改良资格/Appeal、提前可用时点、Gold→Tourism系数、公园强化、Amenities/网络效率参数；LAND-002至006 |
| OPEN-02 | TBD / DESIGN_DECISION_REQUIRED | 神学战斗力数值、本城宗教锁定边界、foreign pressure公式/多源、belief吸收资格/数量/类别/冲突、贸易宗教压力规模公式；REL-003至006 |
| OPEN-03 | BALANCE / DESIGN DETAIL / TECHNICAL REQUIRED | Government D0047折扣／k平衡、具名生命周期、All Yields精确范围、项目速度与直接效果技术；GOV-OPEN-001，旧Loyalty未决已退出 |
| OPEN-04 | IMPLEMENTATION / FUTURE_COMPATIBILITY / TBD | 旧档初始化仍独立OPEN，不自动沿用Conquest snapshot；永久UID及LegacySet冻结保存、Claim提供/移除、模式互斥与完成事件隔离留Development审查；Claim精确成本待定但受极低/短确认约束。无Identity征服城分流已由PROG-006至010正式解决，已有Identity继承不变 |
| OPEN-06 | TBD / DESIGN_DECISION_REQUIRED | Boost最终封顶等细节；最终一次floor(x+0.5)量化契约已按D0018确认；整数写入的实机验证属于Implementation，不是未决设计；不更改已定max规则 |
| OPEN-08 | SUPERSEDED_BY_D0028 / HISTORICAL | GW-001百分比公式/创作者时代及文物历史时代例外已由D0022确定；固定yield与旧逐件补差路线均退出。百分比Modifier与theming结算待实机验证；异常创作者关联、未知自定义类别独立保留；GW002范围已由D0023确认 |
| OPEN-09 | CURRENT AUTHORITY: D0045 / INITIAL_BALANCE_TECHNICAL_PENDING | D0044首测职责保留；每模板实际有效持有来源max、正式合法Gold/Faith、研习完整1T取消／重做、单位不可捕获／Owner转换及最终Floor已定。原单位Owner完全消失等未覆盖边界未定义；原生承载／安全回归／可靠保存仍Technical。 |
| OPEN-10 | DESIGN_FROZEN / BALANCE_TECHNICAL_LEGACY_PENDING | Military_D0037（机制沿D0034）五项阻塞已关闭；单位出生锁定buff、同能力合并max、分网络司令、升级兵种线、ACTIVE更新已定。后勤资源覆盖/数值/技术/Legacy后置；不实现Military。 |
| OPEN-11 | ACCEPTED FUTURE / NAMES_BALANCE_TECHNICAL_LEGACY_PENDING | Harbor_D0037双线基线已接受；船政局强冻结候选，其余机构占位；能力名按可冻结/强候选/暂定分别保留。海上资格、出口/进口/经营参数及Legacy见content；无独立Network或Naval Mobilization。 |
| OPEN-12 | DESIGN_DECISION_REQUIRED / TBD | 永久保护国额度作用域/降级、多个外交来源、Spy经验/周转/死亡减幅；DIP |
| OPEN-13 | MIXED: PROVISIONAL / PREFERRED DESIGN CANDIDATE / THEME CANDIDATE ONLY / TBD | 外交/联盟等级解锁、任务周期/奖励/晋升适用；交流概率与未来fallback、Import Fair duration/selection/repeat、Migration Agreement duration/multiplier、军演函数/k、Pilgrimage资格/X等见DIP-MISSION-003至014；Infrastructure Coordination仅首选候选，Civilian Conversion仅主题候选，公共外交奖励暂定，外交区/市政广场仍Future骨架；不统一升级 |
| OPEN-14 | PROVISIONAL BUT ACCEPTED FRAMEWORK / TBD | Community Local Lv2/IV细节、资格锁定、专家槽cap/递减、Attractiveness权重及建筑分类、国际移民系数/C_map边界/结算细节、国内分发频率/等级边界/recipient资格和排序、Protected Floor依据和数值、人口政策项目细节、Lv4 Settler阈值（暂定8）及计数边界；详见COMM-001至011；旧国内Migration进度公式已被分发机制取代 |
| OPEN-15 | TBD / DESIGN_DECISION_REQUIRED | Local/Regional选择、公式/范围/叠加，有效专家对应机制；ENT |
| OPEN-16 | TBD | Dam的X；DAM |
| OPEN-17 | TBD | Canal叠加/归属/Community分支；CAN |
| OPEN-18 | TBD | Air训练未定参数、Airport Gold/Tourism系数及重复范围；AIR |

### 当前未决与技术适配

- Commerce D0045保留D0039公式／首版值、D0040信誉／合同及D0042配置／来源，只同步单位保护；精确design_detail_required、城市消失／目标非法、hidden protection跨Owner仍未定，不重开已定Owner政策。
- Industry D0045保留D0044首测职责，关闭独立全局效率／Faith fallback／研习中断／单位捕获Owner Gameplay TBD。原Owner完全消失、城市彻底毁灭的未覆盖处置与候选命名保留；逐模板价格承载、完整1T、固定注入、普通Production modifier、保护回归、最终Floor／速度／保存为技术验证。Culture Hybrid D方向已确认，实机状态见Status。

- D0040取代CUL-REVIEW-01/03原Owner见闻键／不继承；见闻与Dialogue均城市历史、独立资格与有效Owner过滤。CUL-REVIEW-02外交／城邦及04独立完整集合并集保留。City-State inclusion仍Future Candidate。
- Research Network：NETWORK_REDESIGN_REQUIRED，现有Research规则保留；Culture已替代旧Eureka。
- 意义延展政府广场／外交区Culture输入已按D0046恢复至九域六产出；当前六产出单城候选仍待原生共存验收。B155/B157负面证据保留，不能由Production多片反证推定文化根因已关闭。其它yield精度、recipient、倍率／结算门禁仍按各自实际证据，不因Design恢复而自动通过。
- 固定完整生产回合、native-only巨作倍率、0.1基础GPP、城市整体Tourism及非敌对独立Spy-style流程：TECHNICAL_INVESTIGATION_REQUIRED，不能因此自行降级Design。
- Dialogue无额外累计cap、考察成本＝当前Spy Production cost、全国现存cap1、K_T=2百分点、K_C=1及标准任务2T已定首测，不再是这些数值Gameplay TBD；真实平衡／原生验证仍开放。

### 已确定作用域的后续兼容事项（非核心玩法未决）

**COMPAT-001 — IMPLEMENTATION / FUTURE_COMPATIBILITY** 当前专用白板文明、单人本地人类与非支持Owner休眠范围以ELIG为准，不要求全原版／Mod文明及领袖叠加兼容。未来原文明复用／AI／多人需独立授权；既有旧档初始化、成本过滤与城市识别技术边界保持。技术问题标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`，不得反向改写已接受玩法或征服休眠语义。

**COMPAT-002 — Commerce D0045 / ARCHITECTURE_REQUIRED** 旧Convergence的D0024总产出/floor规则已退出当前Commerce Design。新合同持久化、锁定随机结果、REALLOCATING、源城容量绑定、Production-only、防止余粮惩罚变总Food惩罚及UI拦截见Commerce D0045与A–G Review；本轮没有实现或部署。

## 13. 设计审阅边界

本文保留当前可获得的v0.1等级规则及Future具体机制。Landscape、Religion、Government既有设计已按用户本次补充恢复；OPEN-01至03只记录剩余参数和规则边界，不再表示缺少整套专业设计。Future的TBD和PROVISIONAL不因整份文档将来被接受而自动成为确定数值。

Research/Culture共享强度、Military_D0037分网络统一动员、Industry逐模板有效持有来源max和Community人口分发各按自身规则处理，不能互相覆盖。永久保护国与ACTIVE下降、Community资格与首次完成锁定、Virtual Specialists与实际工作专家等相互作用已列为显式审阅问题，不为实现便利默选答案。

本文件为D0047当前Design入口；各专业content revision见对应章节。历史修订不覆盖新canonical规则。Design接受不等于Architecture已sync或Mod已实现；文档接受本身不授权实现、部署或promotion；实际实施与验证范围另见Status。
