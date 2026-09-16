# Specialization Gameplay Redesign — Design Spec

Document Owner: Codex
Design Authority: User
Design Revision: D0026
Document State: ACCEPTED
User Acceptance: ACCEPTED
Acceptance Date: 2026-09-15
Acceptance Evidence: 用户授权冻结Research，并明确区域资格/同yield相加/逐建筑计值/传统速度floor/全等级3F3P。
Previous Accepted Revision: [D0025冻结原文](Revisions/Specialization_Design_Spec_D0025.md)
Latest Accepted Design Revision: D0026
Maturity Notice: 其它既有PROVISIONAL/candidate/TBD状态不变

## 1. 文档范围与确认边界 — SCOPE

**SCOPE-001** D0026仅替换Research本地等级设计并冻结规范化机构/能力/Tooltip内容，详见RES节；Research Network及其它专业不变，implementation/balance validation pending。以下为修订历史背景（旧RES描述由当前RES节取代）：D0025仅将GW-001时代对话系数从15%提高到25%，其余机制与范围不变。本文为Specialization Gameplay Redesign的WHAT。D0023确定GW002作品/专业区域范围及保留原yield的50%基础相邻复制。D0022时代对话采用创作者时代多样性百分比15%×max(0,D−1)，取代D0021固定yield；明确文物历史时代例外。旧最高基础值逐件保值已退出当前设计，沿用D0020合格分类与原生theming行为。D0018以NET-RC-005的最终一次显式量化取代D0017接受原生截断；当时的GW本城最高基础值方案现已被D0022完全取代。公式/topology及其它未决边界不变。D0016新增IND-NET-002货币隔离困难时允许Faith同步折扣的条件授权，不扩大建筑或购买资格范围。D0015确认标准化永久记录与当前折扣开放范围分离，详见IND-NET-004/005；不改变D0014科研复制范围或其它专业机制。D0014明确RES-004不区分区域类型，所有非Campus区域的Actual复制基数均纳入，不要求其为专业化区域或消耗人口名额。D0013明确IND-NET-004标准化模板获取与一次初始化，其余继承D0012。D0012明确施工队生产力按游戏速度缩放后向下取整，并以同一整数显示与执行；项目成本仍由原生引擎按游戏速度计算。其余继承D0011（五档从工业Lv1全部开放）。D0010正式确定征服无Identity城市的一次snapshot及互斥初始化模式，直接影响当前v0.1 Development与Conquest测试；更新后交Development正常sync评估Architecture/Status/Tests，旧统一first-completion假设不得继续沿用。其它设计与成熟度继承D0009，Design本轮不调查或修改实现。

**SCOPE-002 — CURRENT IMPLEMENTATION SCOPE — v0.1** Research/Campus、Culture/Theater Square、Industry/Industrial Zone、Commerce/Commercial Hub，以及共同成长、Trade Center、网络核心、Construction Crew和这些专业的跨系统规则。范围不等于实际完成度。

**SCOPE-003 — ACCEPTED FUTURE DESIGN — OUT_OF_V0.1** Landscape/Preserve、Religion/Holy Site、Military/Encampment、Harbor、Government Plaza、Diplomatic Quarter、Community/Metropolis、Entertainment/Water Park、Aqueduct、Dam、Canal、Aerodrome/Airport、Spaceport、Alliance Diplomatic Missions。此标签表示用户已经确认列入未来设计的范围/明确机制，不表示Future进入v0.1实现范围；各条PROVISIONAL、candidate、TBD状态不得被本标签覆盖。

**SCOPE-004** 用户是最终Design Authority。Codex负责整理落盘；外部设计顾问内容在用户接受前仅是proposal/review。没有用户明确确认，不得把后续修订或候选数值升级为ACCEPTED。

### Universal System + Opt-in Player Eligibility — ELIG

**ELIG-001 — Specialization-enabled Player / ACCEPTED** Specialization Gameplay Redesign是player/civilization-agnostic通用系统，只对被明确赋予Specialization-enabled资格的Player启用。资格不是Human身份，也不永久绑定某文明、领袖或测试Trait。全文涉及建立或运行Specialization的“玩家／己方／本城／首都”等，均受本节资格前提约束；未启用玩家完全不参与系统，但可按ELIG-005持有此前已存在、当前休眠的永久城市成果。

只有Specialization-enabled Player建立城市Identity和Potential、使用Settler specialization investment、计算ACTIVE、建立Trade Center及专业网络、获得Local及Network效果、运行Community Immigration、Military体系、其它Specialization及Auxiliary机制。资格只决定谁参与，不修改既有投资、总督、专业等级、网络公式、多来源、专业及辅助区域规则。

**ELIG-002 — 当前载体与未来复用 / ACCEPTED** 当前测试／首个玩法载体可以是白板测试文明、对应Trait或Development最终选择的其它明确eligibility carrier；载体不是系统本体。当前仅启用一个玩家属于当前scope/configuration，不是永久限制。核心设计不得写成Human-only、固定LEADER_SPC_TEST、只有白板文明可用或AI永不可用。

保留未来给原版、Harmony in Diversity、Mod文明／领袖启用，以及多个玩家同时启用、多人参与、进一步抽离为通用Gameplay System/Gameplay Mode的可能性。本轮不承诺实现这些配置，不要求兼容性验证，也不在Design硬编码排除。未来已有文明原Civilization/Leader abilities原则上可与Specialization共存；叠加后的强度属于未来balance/configuration问题。

**ELIG-003 — AI资格与行为边界 / ACCEPTED** AI不是特殊禁止对象；被明确启用的AI允许使用同一套规则。当前不要求额外AI planner或AI行为重写，不因AI可能不善使用Settler、商路、总督或人口政策而削弱投资、改变网络／ACTIVE或简化Community，不增加隐藏AI bonus/penalty。未来启用AI实际表现过差或过强时，另立AI/balance问题，不提前解决。

**ELIG-004 — 参与者成本原则 / ACCEPTED** `Pay runtime/state cost only for participating players.` Specialization机制只需对enabled Players运行。未启用者不因Mod存在而建立新的Specialization city state、维护网络拓扑／recipient sets、计算ACTIVE、运行Community Immigration、Military训练／带教、Auxiliary support或其它专业周期更新。ELIG-005要求保留的既有永久城市数据属于休眠保存，不构成对未启用Owner运行系统的授权。

这是Design scope requirement，不指定过滤API、缓存、事件或其它实现。Eligibility carrier及有效过滤标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`。若Development发现所有AI承担明显周期成本，应依据本规则限定到eligible players，而非反向把系统永久改为Human-only。本轮不进行API／性能调查或benchmark。

**ELIG-005 — Conquest × Eligibility / ACCEPTED** 保持PROG-004的城市永久发展成果定义，以当前Owner是否启用决定运行或休眠：

| 征服／取得情形 | 永久成果 | 当前运行规则 |
|---|---|---|
| 无Identity、原Owner未运行/建立该城专业 → enabled Player | 不自动虚构Identity/Potential；按征服完成时一次snapshot确认既有发展候选 | 依PROG-006至009互斥进入Legacy Claim或Normal First Completion；不再统一从零监听后续完成 |
| enabled专业城市 → 未启用Player | Identity、Potential和明确城市永久投资成果保留，不删除 | 系统休眠；不运行Local、ACTIVE效果、网络、Community、Military或其它专业机制；不因保留Identity而给Lv1效果 |
| 有休眠成果的城市再次被enabled Player取得 | 已有Identity/Potential及永久成果恢复可用 | ACTIVE按当前Owner总督状态重算，网络按当前Owner实际网络重新派生，其它派生状态重算 |
| 两个enabled Players之间征服 | 保留Identity、Potential和城市永久专业成果 | 依新Owner的Governor、Trade Centers、Trade Routes、Network和eligibility context重算派生状态 |

正常未专业化征服城与旧档缺失历史是不同问题；本规则不解决旧档首次加载的迁移初始化，也不删除此前已形成、虽由未启用Owner持有的休眠成果。当前Owner资格门槛适用于所有专业运行，永久成果本身不因此改变。

**ELIG-006 — Development / Future Compatibility边界** Human-only、AI是否可参与、测试文明是否是永久唯一载体、无专业历史AI城是否自动生成专业均已明确，不再作为核心玩法未决。Old-save initialization保留为Implementation/Future Compatibility事项；多个enabled玩家的multiplayer determinism、AI实际行为质量、carrier技术实现与参与者成本过滤也留给Development／未来兼容工作，不承诺本轮解决。跨Owner城市识别继续沿用PROG-004的技术审查标记，不据此修改玩法。本轮不修改测试文明或Architecture/Status/Source/Tests，不恢复Development，不进行实现、性能测试、P0测试或游戏验证。

## 2. 测试文明与基本术语 — ID / TERMS

**ID-001** 以独立新文明和独立领袖承载测试，不修改或覆盖原版Scotland。暂时复用Scotland的文明/领袖视觉、名称风格和可用展示资产，不复制其原有游戏能力。玩家可见名称采用Scotland (Specialization Test)、Robert the Bruce (Test)等明确测试标记。暂不制作原创美术与历史设定。 当前白板载体没有额外传统Civilization/Leader gameplay bonuses，以Specialization作为主要玩法和平衡基准；这是当前载体配置，不是通用系统的永久身份定义，资格与未来复用遵循ELIG。

**ID-002** Industrial Zone保持正常科技位置，不作为提前解锁的特色区域。

**TERMS-001** Specialization是城市专业身份；Potential是该城永久投资形成的潜力；ACTIVE是当前实际激活的专业等级。三者不得互相替代。Working specialist指实际工作的对应专家，空槽不算。

**TERMS-002** Base adjacency只指基础相邻，不包含政策等相邻倍率。Actual在本设计中指与煤炭发电厂/大酒店“按区域产出复制”机制相同口径的区域产出基数，不是城市总产出，也不要求先建成这些建筑；不等同于“只取政策翻倍后的相邻数字”。具体非传统收益/区域适用范围待澄清时，不擅自扩大或删减。

**TERMS-003** F=Food，P=Production，S=Science，C=Culture，G=Gold。百分点是对百分比数值直接相加，不是相乘增幅。

## 3. 共同成长与永久投资 — PROG

**PROG-001** 普通First Completion模式城市在第一个符合条件的专业区域完成建造后锁定专业，不在放置时锁定。v0.1四专业及正式认定replacement family适用；征服无Identity城市先按PROG-006分流，Legacy Claim模式不适用后续first-completion。未来Community候选仍见COMM-001，不提前改变v0.1规则。

**PROG-002** 专业确定后默认Potential Lv1。在己方城市消耗一个Settler，永久Potential +1，最高Lv4。Potential不由source数量、网络强度或网络积累产生。不凭空给没有专业的城市发专业能力。

**PROG-003** Lv2/3/4分别要求Potential至少2/3/4，并有已建立的总督满足2/3/4头衔门槛。ACTIVE取当前满足全部条件的最高等级；无已建立总督或总督调离时，已有专业仅保留Lv1，Potential投资不丢失。门槛不是要求额外消耗同样数量的Settler或额外重复支付头衔。

**PROG-004 — Conquest Inheritance / ACCEPTED** 已有Specialization Identity/Potential的城市被征服后不进入Legacy Claim初始化，Specialization Identity、Potential、Settler investment history或等价永久投资事实，以及source城市自身永久掌握的标准化模板等明确城市成果保留。这些是城市长期发展成果，不是旧Owner临时全国buff。Potential Lv4 Research城被征服后仍为Research / Potential Lv4，不重置身份或潜力，不要求重新消耗Settler。

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

## 4. v0.1共同Lv2规则 — SHARED

**SHARED-001** ACTIVE Lv2起，对应专业区域本体及该区域每一级建筑各+1 Housing。

**SHARED-002** 每名实际工作的对应专家增加+2基础GPP，之后正常接受其它GPP百分比加成：Research→Great Scientist；Industry→Great Engineer；Commerce→Great Merchant；Culture每名Theater专家同时获得Great Writer、Great Artist、Great Musician各+2。不能将基础GPP改为不受倍率影响的直接点数奖励。

**SHARED-003** 下列Lv3“提升至”取代低等级对应专家食物/生产力档位，不把3F3P与5F5P重复叠加。Housing、GPP及其它独立已解锁能力继续保留。

## 5. Research / Campus — RES

**D0026: DESIGN_FROZEN — implementation / balance validation pending.**

唯一新规则与文案正文：[Research规范化Content](Content/Research_D0026.json)。[Schema](Content/README.md)；[边界确认与自审](Research_D0026_Review.md)。机构永久随Potential累积，ACTIVE仅控制对应阶段能力；机构为presentation-only，不进入普通建筑体系。

| Rule ID | 当前权威content条目 |
|---|---|
| RES-001 | RES_BASE_SUPPORT：各等级基础专家支持；RES_INST_1学者结社，无named ability |
| RES-002 | RES_L2_TRAIN：RES_INST_2研修院的人才培养，引用SHARED住房/GPP合同 |
| RES-003 | RES_L3_CROSS / RES_L3_APPLY：RES_INST_3学术联合会的跨学科研究/学以致用；替换旧人口Science与旧支持提升 |
| RES-004 | RES_L4_INFRA / RES_L4_CHAIR / RES_L4_TRADITION：RES_INST_4学术总署；替换旧专家百分比和全区域Actual复制 |

SHARED-003的旧Research支持提升不再适用，Research仅按RES_BASE_SUPPORT；其它专业的SHARED与Local规则不变。具体公式、映射及第一版Tooltip只在content维护，旧D0025正文见冻结快照，不将新设计视为B076.103已实现。

**RES-005** Research Network增加Inspiration完成比例的额外百分点；强度统一按NET-RC规则，不按路线线性叠加。本次不变。

## 6. Culture / Theater Square — CUL

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| CUL-001 | Lv1 | 每名Theater工作专家额外+3F、+3P |
| CUL-002 | Lv2 | 获得SHARED-001住房；每名专家同时获得三种文化伟人基础GPP |
| CUL-003 | Lv3 | 专家支持提升至+5F、+5P；本城增加`0.5 × Population × working Theater specialist count`基础Culture |
| CUL-004 | Lv4 | 每名Theater工作专家使本城Culture增加5个百分点；获得GW-001时代对话及GW-002巨作基础相邻能力 |

**CUL-005** Culture Network增加Eureka完成比例的额外百分点；使用NET-RC，不交换Research/Culture对应的Boost种类。

### Great Works — GW

**GW-001 — 时代对话 / Dialogue Across Eras** Culture Lv4以跨创作者时代收藏为主题。`D`为本城合格Great Works覆盖的不同巨作创作者时代数量；普通合格作品使用其关联伟人的EraType，文物没有伟人创作者，按用户明确例外使用文物自身原生历史时代。合并后统一按时代去重，不区分“文物时代”与同名“伟人时代”另计两次。不是当前游戏/城市时代、作品获得/激活时代或建筑时代。`BonusPercent = 25% × max(0,D−1)`，本城全部合格作品的Culture与Tourism统一提高此百分比。D=1/2/3/4/5/6/7分别+0%/+25%/+50%/+75%/+100%/+125%/+150%；12件覆盖6时代，每件均+125%，件数不直接进入百分比公式。25%为D0025当前正式系数（取代原15%）；不新增cap、不把7时代当上限、不添加复杂曲线。著作、音乐、艺术、文物保持合格，Product/Relic排除，未知自定义类别不自行扩大。此规则取代D0021固定每件+Culture/+Tourism，以及更早最高基础值/逐件差额保值；不再开发单件setter或补差模拟。关联缺失/时代未知或运行创作者与数据库关联冲突须报告，不擅自代入玩家时代。

**GW-002** Culture ACTIVE Lv4每件合格文化Great Work额外获得本城全部已完成专业区域Base Adjacency Yields的50%。包含剧院广场及特色替代区域；专业区域按本机Districts.RequiresPopulation分类。作品采用Writing/Music/Sculpture/Portrait/Landscape/Religious art/Artifact七类，排除Relic、Product及未知自定义类别。各yield保留原种类：学院Science、工业Production、商业Gold等，不统一转Culture。明确使用BASE，不使用Actual复制基数，不将政策翻倍或建筑非相邻产出算入；每件按本城对应基础相邻合计的50%取得，作品数量不再乘入单件Modifier。

**GW-002A — Native fractional behavior / ACCEPTED D0024** 用户已实机确认巨作基础相邻效果，并接受原生逐件小数截断：例如基础Production 3，理论每件1.5，实际每件1。当前不补偿、不改城市补贴、不把余数跨作品合并；此许可仅针对GW002，不外推其它接口。

**GW-003** GW-001沿用D0020合格文化分类：Product、Relic排除；Artifact保留，宗教题材艺术不等于Relic；未知自定义类别不自行纳入。时代对话不再以精确恢复单件补差及所有作品专属倍率/主题化为前提。优先采用整类/城市Great Work百分比Modifier，按正常Modifier体系与theming自然叠加即采用。若发现意外结算顺序，报告实际表现，不自行设计补偿层或逐件模拟。Culture/Tourism各自的原生结算关系需实测，不假定一致。GW-002基础相邻能力与其它Culture IV能力不因本变更而改变，其范围已由D0023明确。

## 7. Industry / Industrial Zone — IND

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| IND-001 | Lv1 | 每名IZ工作专家+3F，并增加相当于本城IZ Base Production adjacency的Production；从Lv1固有可用Construction Crew |
| IND-002 | Lv2 | 获得SHARED-001住房与Engineer基础GPP |
| IND-003 | Lv3 | 专家Food提升至+5F，保留100% Base Production adjacency的Production，并增加其2倍的Gold；不改为通用固定5P |
| IND-004 | Lv4 | 本城IZ Production的Actual复制基数50%经工业网络输出；同一接收城市取当前有效来源实际可提供的最高Industry IV Production output，不叠加；见IND-NET-003 |

### Industrial Network / Standardization — IND-NET

**IND-NET-001** 接收Industrial Network的城市可获得建筑Gold购买折扣：Industry I/II/III/IV为10%/20%/30%/40%。目标建筑模板须在当前有效工业来源模板并集中；模板提供者与最高折扣提供者可以不是同一城市。优先按相同District和Building Tier匹配；若需固定同Tier建筑组，必须明确范围，不暗中扩大适用对象。

**IND-NET-002** 优先仅影响Gold购买；若技术上排除Faith折扣较难实现，用户已授权同一合格建筑的既有合法Faith购买也可享受折扣。采用时须报告实际货币行为，不再为这一兼容选择重复请求授权；不因此扩大到其它未启用/仅可Faith购买的建筑。不得以退款、放宽解锁或改变购买资格等方式默默改变实际玩法语义。标准化账本保持，但断开/消失的源不再提供当前资格。

**IND-NET-003 — Industry多来源 / ACCEPTED** 对同一接收城市，以下三项分别按当前有效工业网络来源计算，不以历史连接代替当前资格：

1. **Industry IV Production Output**：`Received Industry IV Production = max(valid source Industry IV Production outputs)`。比较各有效Lv4来源实际能提供的产出，不求和、不按来源数量增加倍率，不套Research/Culture的`L=max(...)`后生成虚构来源。保留建设更强工业核心的价值，避免多个高级工业城令输出线性爆炸。
2. **Standardization Template Set**：`Available Template Set = union(all templates from valid connected Industry sources)`。当前网络共享有效工业来源掌握模板的并集；不同中心可贡献不同合法模板。来源断网、摧毁、征服或失去source资格即停止贡献旧网络当前集合；不是曾接通过就永久全国解锁。来源城市自身已掌握的永久模板记录仍保留，征服后依PROG-004归新Owner并按真实网络重新判断资格。
3. **Standardization Discount**：`Discount = max(valid Industry source discounts)`。目标建筑存在于当前模板并集时，可使用当前最高有效等级的Gold折扣，即10%/20%/30%/40%；模板资格与折扣不要求同源，不逐模板限定独立折扣提供者。全国共享成熟模板，最先进的工业专家体系指导最高水平的标准化生产。货币适用遵循IND-NET-002的条件授权，不改变其它购买资格。

多个工业中心仍有模板并集价值；来源失效时三项按剩余有效来源重新计算，不保留旧来源贡献。

**IND-NET-004 — Template Acquisition / ACCEPTED D0015** Industry专业城以任何方式合法获得或完成建筑时，记录所有合格建筑的标准化模板，不以当前是否开放折扣作为记录条件。这里承接HD明确分类的真实建筑目录（包括特色、宗教、当前不可金币购买和当前未开放折扣的建筑）；不把奇观、内部/HD虚拟建筑或缺失/不明确HD分类自动视为合格。首次成为Industry专业时，对本城已经存在的合格建筑做一次初始化补录；此后使用事件式增量记录，不持续进行全城扫描。具体BuildingType及其分类证据永久保留，记录与当前网络贡献仍遵循IND-NET-002/003和PROG-004。未开放建筑的模板不丢弃，未来经用户批准可开启其标准化折扣资格，无需因当前禁用而重新获得建筑。

**IND-NET-005 — v0.1 Discount Activation / ACCEPTED D0015** 模板记录范围与当前折扣启用范围独立维护。v0.1开启学院、剧院广场、工业区、商业中心、军营、港口、圣地、航空港、水渠、堤坝、社区、娱乐中心、水上乐园、保护区、外交区的建筑，包含特色建筑；只有目标建筑在当前游戏状态下本来就可合法使用Gold购买时，才可在满足有效工业网络与模板条件后使用Gold折扣。仍按相同区域+HD Tier匹配，除下述明确市中心分组。记录模板或开启折扣都不会新增Gold购买资格、解锁特色/宗教建筑、改变科技/市政/互斥条件；Faith价格适用IND-NET-002的条件授权。当前不能合法Gold购买的建筑仍可记录，当前不获得金币折扣；不以Faith字段推导放宽购买权限。

市中心不直接按整个HD Tier0共享。v0.1只开放以下三个模板匹配组：

| 组 | 具体建筑 | 共享规则 |
|---|---|---|
| 市中心基础组 | 纪念碑 BUILDING_MONUMENT、粮仓 BUILDING_GRANARY、磨坊 BUILDING_WATER_MILL、测量仪 BUILDING_NILOMETER_HD、法表 BUILDING_HD_TABLES_OF_LAW | 五者视为同一标准化Tier，相互匹配 |
| 会展中心独立组 | BUILDING_EXHIBITION | 仅自身匹配 |
| 警署独立组 | BUILDING_HD_POLICE_STATION | 仅自身匹配 |

这些是本项目标准化分组，不改写HD原始Tier表。市政广场与上述七栋以外的市中心建筑，当前仅记录而不开放标准化折扣；明确列名的市中心组不自动扩充未列出的特色替代建筑。以后可以由用户批准增加开放范围或组成员，不删除既有模板、不自动将未来范围提前启用。

### Construction Crew — CREW

**CREW-001** Industry Lv1起的默认固有能力。固定成本城市项目产生固定Production施工队；以下五档是项目/施工队规格，**不是专业Lv1–Lv5**。

| 项目Production成本 | Crew可转移Production |
|---:|---:|
| 280 | 250 |
| 460 | 420 |
| 820 | 750 |
| 1100 | 1000 |
| 1500 | 1360 |

**CREW-002** 效率约为110投入换100可转移生产力，现档位为适应奇观成本而整数调整；不增加1800/2000档，避免单个最高级施工队直接完成后期大型奇观。

**CREW-003** 施工队移动到目标己方城市并消耗，向当前合法在建District、Building或Wonder注入该队固定Production。只应用目标所需部分，多余施工力直接浪费，不流入下一队列，不递归overflow。750施工力、剩余300的目标：完成目标，450消失，下一项获得0。

**CREW-004** 空队列或非法目标拒绝动作，不消耗单位。五档项目从Industry Lv1全部开放，不新增科技/市政/专业等级档位门槛。项目Production成本和Crew可转移Production均按游戏速度缩放，设计表数值作为基准；项目成本保留原生引擎计算，不修改基础Cost。Crew可转移Production = floor(基准Production × 游戏速度CostMultiplier / 100)，即缩放后向下取整。施工按钮、预览及确认提示显示同一整数金额。明确接受每支队伍相较精确比例舍弃不足1点Production；不得四舍五入或向上取整。五档标准速度数值、1点劳动力、合法目标与超额浪费规则不变。

## 8. Commerce / Commercial Hub — COM

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| COM-001 | Lv1 | 每名Commercial Hub工作专家+3F、+3P；该商业专业城市具有Trade Center身份 |
| COM-002 | Lv2 | 获得SHARED-001住房与Merchant基础GPP |
| COM-003 | Lv3 | 专家支持提升至+5F、+5P；每接入Research/Culture/Industry网络类型，专家分别额外+2S/+2C/+2P。同类型多源不重复提供该类型奖励 |
| COM-004 | Lv4 | Convergence／专业汇聚：对直接接入本中心的Research、Culture、Industry分别选Actual Source City Yield Basis最高的有效source，获得其对应Science／Culture／Production的20%；同类型不求和，不跨yield转换；见COM-005至008 |

**COM-005 — Convergence / ACCEPTED** Commerce IV向内汇聚帝国最强专业核心，与Industry向外输出形成不同主题。当前v0.1分别处理Research→Science、Culture→Culture、Industry→Production，三个类型独立选择最高有效direct source，不跨yield转Gold。`Convergence_Y = 20% × max(actual city Y basis of valid direct sources of corresponding specialization)`；没有该类型有效direct source则无对应汇聚收益。20%是正式初始Design/balance value，未来调整须新Design Revision，不是未接受候选。

最高source按对应eligible yield比较，不按最高ACTIVE选择或虚构来源，不把多来源求和。例如直接接入的科研源为2000/900/700 eligible Science时，选择2000，额外获得400 Science，而非三者相加后乘20%。保留多source冗余和其它网络价值，避免同类铺城线性放大；Research/Culture/Industry分别选择自己的最高source。

**COM-006 — Actual Source City Yield Basis / ACCEPTED D0024** v0.1采用用户此前有条件授权的来源城市实际总产出备选：目前未找到可靠的精确本地/外来收益分解接口，故读取对应来源城市实际Science/Culture/Production总产出，允许包含外来输入。取代此前要求剥离全部Specialization transfer的纯本地产出基数。仅直接有效Research/Culture/Industry源可参与，Commerce不得作为汇聚源；汇聚输出施加在城市层，不加入区域复制基数；不按各源分别求和。该选择不证明任意第三方Mod的跨城反馈均无环；出现实际回边需独立调查，不靠反复累加或未知来源保留旧值。

**COM-009 — Final integer grant / ACCEPTED D0024** 每yield分别计算`Raw = 0.20 × max(valid direct source actual city yield)`，仅在最终城市基础追加接口执行`Applied = floor(Raw)`。三类独立取整、不先截断来源基数，不将各来源分别取整相加。之后正常受接收城原生倍率影响。刷新绝对替换旧Applied，不累加；无有效来源或商业ACTIVE低于4时撤销。

**COM-007 — Direct sources only / ACCEPTED** Convergence只看直接接入本Trade Center的有效专业sources。A科研源→B商业IV→C贸易中心时，B接收A网络、汇聚A实际城市产出并可向C分发；C仅接收网络，不因此将A视为自己的direct source，即使C是Commerce IV也不能仅凭该distribution再次汇聚A。来源/连接失效不继续贡献；动态更新/撤销的具体处理留Development，不改变有效来源限定。

**COM-008 — 首都战略与继承能力 / ACCEPTED** Commerce IV首都可由其它科研/文化/工业核心通过direct routes接入，自己接收网络、保留Commerce III对应专家+2S/+2C/+2P、分别汇聚各类最高有效来源的20%，并继续分发，无须Capital→Capital路线。Research IV首都则天然direct self-connect、自身接收并可分发；其它Commerce IV城市若要汇聚该科研首都，仍须合法Research Capital→该商业中心direct connection。科研首都偏本地专业核心，商业首都偏全国汇聚与组织，不要求数学等价。Commerce I–III不变，Lv4为追加能力。

20%参考之一为用户提供的后期样本：最强科研首都约2000 Science、全国约8000，汇聚400约占全国5%；再考虑文化和工业可同时汇聚，作为相对保守的起测值。样本不是游戏规则，也不声明本轮验证。旧COM-004“免费成为已接入网络recipient”已由D0009废弃，接收现在是所有directly connected Trade Center的基础网络资格。

## 9. Trade Center与Network核心 — NET

**NET-001 — Capital self-connection / ACCEPTED（D0009纠正）** Trade Route Capacity本身就是网络带宽；不额外创建每路线载荷分配、round-robin或手动网络选择界面。首都与商业专业城市为Trade Center。当首都拥有Specialization Identity，其自身专业天然direct self-connect到本首都Trade Center，同时使首都成为该网络合法recipient并获得效果；可沿合法outgoing distribution routes继续分发。不要求虚构Capital→Capital或额外自接收资格。天然自身专业接入仍是首都规则，不泛化为所有中心自身专业自动接入；任何中心一旦直接接入网络，均适用NET-002的自然接收规则。

**NET-002 — Direct connection = receive + may distribute / ACCEPTED** 己方专业源S→己方Trade Center H的有效direct connection，使H接入该类型network set、自动成为该类型合法recipient并获得network effects，同时可作为分发中心。首都天然self-connection同样适用。无须H→H路线、Commerce IV或额外self-reception资格。H→己方城市D的每条有效distribution route自动携带H当前全部直接接入网络。H自身按city UID去重，只计一次。

**NET-003 — Distribution reception = receive only / ACCEPTED** 一条distribution route可同时使目的城进入Research/Culture/Industry等接收集合；外贸、道路或贸易站本身不等于这种己方direct接入。目的城即使也是Trade Center，也不会仅因收到distribution取得原source的direct connection、继续转发该网络或对原source进行Convergence，保持non-recursive relay。Direct接入、distribution接收及其它明确合法资格共存；失去一种而仍有其它有效资格时保留接收，但不会据接收资格反推直接来源。

**NET-004** 路线结束、取消、战争/征服/端点失效等使路线不再有效时，相关接入/接收资格撤销，不能仅因过去曾建立过路线而继续享受网络。读档后应反映当前真实集合，无需玩家打开贸易界面恢复网络。

### Research / Culture共享强度 — NET-RC

**NET-RC-001** `Network Strength = k × L × sqrt(N)`。Research使用独立可调k_R，Culture使用k_C，初始测试均为1。结果是Research额外Inspiration百分点、Culture额外Eureka百分点。

**NET-RC-002** `N`是当前实际接收该类型网络的己方城市UID去重数量，包含直接接入的Trade Center及天然自接入的首都；不是source数、raw路线数、全帝国城市数或中心总路线数。同城direct接入、distribution、多中心或其它免费资格重叠均只计一次。未来其它合法接收方式进入同一去重集合。

**NET-RC-003** 多个当前有效接入的同类型来源，`L = max(all valid source ACTIVE specialization levels)`；使用ACTIVE而非Potential。来源数量本身不增加N。统一选L后只计算一次强度，禁止分别按来源求强度后相加，禁止`Σ(k × L_i × sqrt(N))`或逐中心求和。

**NET-RC-004** 最高等级源失效后立即回退到剩余有效源的最高ACTIVE。无有效来源时Strength归零，不保留stale Strength；N=0时Strength也为零。Research/Culture规则不自动扩展到其它机制：Military共享pool另按MIL-004的PROVISIONAL模型；Industry按实际source output取最大及模板并集；Community国内网络只分发人口。

**NET-RC-005** Research/Culture内部保持完整浮点：RawStrength=k_R或k_C×L×sqrt(N)，所有合法Network modifiers与未来Entertainment效率修正均在浮点上执行。仅在最终整数Boost接口边界量化一次：`AppliedBoost = floor(FinalRawBoost + 0.5)`（Boost非负）；显式使用此式，不使用默认round/banker's rounding，不提前量化、不重复量化。1.49→1、1.50→2、3.50→4；L4/N2原值约5.657→6个百分点。不同Raw值映射同整数时仅保持该AppliedBoost，不重复叠加；网络失效回零。正式权重1/2/3/4、独立k_R/k_C=1、L为有效来源最高ACTIVE、N为recipient UID去重不变。此规则取代D0017“浮点原样交引擎并接受截断不修复”。正式集成前以Raw1.5→接口2、Raw3.8→接口4最小原生测试确认；不再尝试让引擎保留fractional percentage points。不改变原生基础Boost规则，不假定固定40%；已触发Boost不补发、额外进度不得溢入下一科技/市政；最终封顶仍待确认。Entertainment具体效率参数未由本决定设定。

## 10. Future专业 — OUT_OF_V0.1

本章记录已确认未来范围及本次明确提供的机制；不因为记录进Spec就纳入v0.1实现。

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

**MIL-001** Lv1每名working Encampment specialist获得+3F/+3P基础支持。Lv2军营及对应建筑继承SHARED-001住房；每名working Encampment specialist提供**+2 base Great General GPP**，之后正常接受GPP百分比加成；每名实际工作专家另外提供正式接受的**+15% Combat XP**，完整定义见MIL-005。

**MIL-002 — Military III / Advanced Experience / Insight XP — ACCEPTED** Lv3专家支持提升至5F5P；不继续增加统一Combat XP百分比。高级单位根据已经掌握的Promotions，从每次符合条件的战斗中获得少量独立Bonus XP。

用户确认公式：`Insight XP = min(E, floor(P / 2))`。

- `E` = 本城当前实际工作的Encampment specialist数量；只计算真实工作专家，空槽不计算。Military Academy不增加E。
- `P` = 单位在战斗发生时实际拥有的Promotion数量；不使用XP level、总累计XP或由XP反推的理论晋升等级。
- Corps/Army合并继承的实际Promotions合法计入P。XP与实际Promotions可能脱钩；合并获得的真实战术知识属于预期互动，不是需要阻止的技巧。

用户确认的晋升档位表：

| 实际拥有Promotions（P） | 理论Insight上限（实际仍受E限制） |
|---:|---:|
| 0–1 | +0 |
| 2–3 | +1 |
| 4–5 | +2 |
| 6–7 | +3 |
| 8–9 | +4 |
| 更高P | 按floor(P / 2)继续增加，实际仍受E限制 |

**D0002边界澄清 — ACCEPTED** 保持原公式，不增加额外+3或其它人工硬上限。当前Encampment实际工作专家槽最多4个，即`E <= 4`，因此当前设计结构下Insight XP实际最高天然为+4；这是实际专家数量的约束，不是独立固定奖励上限。

P为6–7时，E为1/2/3/4分别奖励+1/+2/+3/+3；P至少8且E为4时奖励+4。第四名实际工作专家在极端高级单位上仍有Military III价值。普通6–7 Promotion老兵仍最多+3，此前正常晋升树的平衡结论不变。P仍计战斗时实际拥有的Promotions，包括合法军团/军队合并继承；E仍只计真实工作军营专家，Military Academy不提供额外虚拟专家。

**MIL-003 — Military IV / Professional Standing Army / 职业常备军体系 — ACCEPTED** 包含两个相互独立的能力：后方和平Garrison Training与前线实战Frontline Mentorship。Mentorship不绑定后方训练，不要求返回Military IV城市或驻扎城市中心／军营。Military II负责正常Combat XP效率；Military III按单位自身Promotions提供Insight XP；Military IV负责正规训练与老兵传帮带。详细规则见MIL-009至MIL-013。

**MIL-004 — Military Network Mobilization / PROVISIONAL BALANCE MODEL** 每个参与玩家全国共享一个Military Mobilization Progress pool，多Military sources不各自建立独立免费单位生产线。

- 第一版每回合进度：`Mobilization Progress per turn = L * sqrt(N)`。L为当前所有有效Military sources的最高ACTIVE；N为实际接收Military Network的己方城市UID去重数。全国计算一次，不逐source求和。
- 第一版阈值：`Mobilization Threshold = 100`，为PROVISIONAL BALANCE VALUE。达到阈值生成一个合格动员单位、Progress减100并保留overflow；不是最终locked参数。目标为成熟Military IV网络约6–10个recipient时，大约8–10回合一单位。
- 单位为当前玩家可以合法动员的最高级Melee Land Combat Unit，不随机军种。编制同时受所选Military source城军营建筑tier与当前正常游戏合法解锁限制：tier1最多single、tier2最多Corps、tier3最多Army；`Formation = min(building-supported formation, currently legally unlocked formation)`，不提前解锁编制。Military Academy与Military Political Department只按building tier判断。
- 生成于最高ACTIVE的有效Military source city，优先Encampment，必要时City Center；多个同级最高source的稳定tie-break仍TBD。无合法放置位置不得丢失已完成进度，具体处理为IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT。无对应建筑层级等未明确资格边界仍TBD，不自行补规则。
- 平衡时间轴仅为建模假设：Lv4理论上较早可达、约T70；军营/港口tier1/2/3约T50/T80/T110，不是硬性解锁回合。

本模型替代此前Military多源归属、阈值和生成位置整体未定的骨架，保持PROVISIONAL；不自动决定Naval Mobilization。

**MIL-005 — Military II / Combat XP — ACCEPTED** 每名实际工作的Encampment specialist提供**+15% Combat XP**，适用于本Military专业城市训练出的对应陆地军事单位。空专家槽不计算。这是正常Combat XP modifier，与HD现有Barracks/Stable、Military Academy及其它正常经验modifier正常叠加，与经验政策卡按游戏正常规则互动。不修改单次8 XP Combat XP cap，不通过额外奖励绕过该cap。

设计目标是允许玩家以人口/专家投入购买训练质量。Military Academy、更多working specialists、XP policy分别代表建筑选择、人口投入和政策槽投入。主要按不装备额外XP政策卡的环境平衡；允许玩家付出军事政策槽机会成本，将正常Combat XP更快推向8 XP cap，不为政策卡环境反向削弱Military II。

**MIL-006 — 三级建筑与平衡原则** 已确认槽位设计背景：军营区域基础1槽，tier3建筑后合计最多4槽。Barracks/Stable、Military Academy及XP政策仍按HD/游戏原有规则提供收益。本系统不重新平衡Military Academy与Military Political Department本身的生产、编制、战斗力、经验差异，不要求两条路线严格数学等价或50/50选率。

Military Academy已有经验训练、直接训练更高级编制及其它质量路线价值；Military Political Department具有数量路线价值。明确不采用“Military Academy额外virtual instructors / virtual specialists”方案。玩家可以选择Military Academy+较少专家、Political Department+更多专家、Military Academy+大量专家、使用XP policy，或Political Department配合单位合并培养部队。Specialization提供相对中立的专家体系，目标是有意义的资源配置选择。

**MIL-007 — Insight XP与正常Combat XP的边界 — ACCEPTED** 正常Combat XP完全遵守游戏正常计算与单次8 XP cap。Military III的Insight XP在正常Combat XP结算之外独立追加；例如8 normal Combat XP + 3 Insight XP = 11 total XP gained，不是把Combat XP cap改为11，不修改或移除8 XP cap。当前极端情况P≥8且E=4时，可获得8 normal Combat XP + 4 Insight XP = 12 total XP gained，这是已接受的高级军事教育收益，正常Combat XP cap仍为8。普通新兵P=0或1时Insight为0；真正拥有高级战术知识的单位可从同一场实战额外获得少量经验理解。实现可行性状态：`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`；本设计修订不进行技术调查或实现承诺。

**MIL-008 — 有效专家范围与修订边界** 当前Military II/III仅计实际工作军营专家；Entertainment Local Support未来形成的Effective/Virtual Specialists是否参与两者，仍属于ENT有效专家适用范围的独立Design Decision，本轮不决定。Military IV按D0006的MIL-003/009至013更新；Military I、Military II/III及5F5P、Mobilization、Harbor naval mirror和Aerodrome扩展保持既有设计状态，不因本次接受而补全其它未来模块的未定参数。Military继续属于OUT_OF_V0.1。

**MIL-009 — Military IV-A / Garrison Training — ACCEPTED** Military IV城市提供City Center与Encampment两个正规训练位置。符合条件的己方陆地战斗单位连续驻扎满一个完整回合后，每个有效训练回合获得`+1 Training XP`。

完整驻扎周期定义：单位在一个回合结束时已位于合格训练位置，下一次训练结算时仍连续位于同一合格位置，才获得经验。刚移动进入、移动力耗尽停留或仅于回合结束时路过均不立即奖励；离开训练位置即清除连续状态，返回后重新完成完整周期。不能只凭两次结算位置相同而忽略中途离开，也不能在City Center与Encampment之间移动却沿用原连续状态。

Training XP是直接增加单位经验的独立训练奖励，不属于Combat XP，不受Military II、Barracks/Stable/Military Academy等建筑Combat XP modifiers或XP policy放大，不修改正常8 XP Combat cap。单靠训练，第一次15 XP晋升约需15个有效训练回合，后续晋升越来越慢，不能替代实战。不自行添加用户未指定的训练晋升等级上限。

**MIL-010 — Military IV-B / Frontline Mentorship — ACCEPTED** 属于该Military IV体系的己方陆地战斗单位完成一次符合条件的实际战斗时，只检查fighter周围1格的相邻己方合格陆地战斗单位，选择实际Promotion数量最高者作为潜在mentor。多mentor不叠加、不求和；无合格mentor时无Mentorship XP。fighter与mentor无需驻扎训练位置，mentor无需回到Military IV城市。

`P_fighter`为本次战斗单位当前实际Promotion数量；`P_mentor`为相邻合格己方单位中的最高实际Promotion数量。

`DeltaP = P_mentor - P_fighter`

`Mentorship XP = max(0, floor(DeltaP / 2))`

| Promotion差值DeltaP | Mentorship XP |
|---:|---:|
| 负数或0–1 | 0 |
| 2–3 | +1 |
| 4–5 | +2 |
| 6–7 | +3 |
| 8–9 | +4 |
| 更高差值 | 继续按公式，自然受实际Promotion数量限制 |

不增加额外hard cap；不以专家数E限制Mentorship。Mentorship XP是正常Combat XP之外独立追加的Bonus XP，不提高正常8 XP cap，不受Military II、建筑Combat XP modifiers或XP policy放大。

P始终是战斗时单位实际拥有的Promotions，不是XP Level、accumulated XP或据经验值推算的理论等级。合法Corps/Army合并、成员Promotion继承及其它实际授予Promotion的机制均参与比较，延续Military III定义。

**MIL-011 — Insight与Mentorship互补 / ACCEPTED** 新兵自身Insight少或为0，但可从相邻高级mentor获得较强Mentorship；中级单位同时获得自身Insight及与更高级mentor之间的部分Mentorship；高级老兵Insight较强、难以找到晋升差足够大的mentor，Mentorship自然趋近0。正式成长意图：`新兵主要靠老兵教 → 中级单位两者兼有 → 高级老兵主要靠自己的Insight`。

- 0 Promotion新兵相邻6 Promotion老兵：DeltaP=6，Mentorship=3；若normal Combat XP=6、Insight=0，总经验为9，但normal Combat XP仍为6，正常cap仍为8。
- 4 Promotion单位相邻6 Promotion老兵：Mentorship=1，同时可按军营真实专家数获得自己的Military III Insight。
- 6 Promotion老兵没有更高级邻近单位：Mentorship=0，主要依靠自身Insight继续成长。

**MIL-012 — 触发作用域与建筑中立 / ACCEPTED** Mentorship只在符合条件的实际战斗发生／结算时进行一次局部判定：当前fighter、周围1格、相邻己方合格陆军及最高实际Promotion count。Design不要求每回合扫描全国单位或所有单位周围六格，不要求持续维护全国mentor关系或所有单位间晋升差。这是玩法作用域要求，不规定具体代码或事件实现。

Military IV不给Military Academy额外virtual mentor、virtual specialist、bonus Mentorship或bonus Training XP，也不额外修改Military Political Department。HD两栋建筑已有的数量、直接训练Corps/Army、战斗力、XP、Production等差异继续由HD负责，Specialization不重新平衡两栋建筑选率。

**MIL-013 — Future镜像与剩余边界** Harbor Naval Military branch的默认平移已由D0008登记为ACCEPTED DIRECTION，位置与规则见HARB-005至009；具体Naval eligibility、特殊建筑额外互动与Naval Mobilization仍独立细化。Aerodrome既有扩展不变。

Military IV尚未明确的细节继续TBD：单位“属于该Military IV体系”的取得与保持资格（如来源城ACTIVE变化后如何处理）、fighter/mentor及训练单位的精确合格陆军分类、合格实际战斗范围，以及战斗发生／结算之间位置和Promotion快照的精确玩法口径。训练+1/有效回合、完整连续驻扎规则、Mentorship公式与无额外hard cap均已确定，不再列为待定。技术问题仅标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`；本轮不调查Combat event、Promotion读取、邻近判定性能或实现方式，不写代码、不修改Architecture/Status/Source/Tests、不启动游戏或P0工作。

### Harbor：完整双线 — HARB

**HARB-001** Harbor定位为**100% maritime commerce + 100% naval military**，不是各半的两套能力。

**HARB-002** 商业线包括Great Merchant与Great Admiral、marine improvement/resource收益。未指明的等级分配、GPP及改良产出系数TBD，不截掉任一条线。

**HARB-003** Lv3：本城全部海洋资源，无论是否紧邻Harbor，都提供Harbor正常资源Base adjacency，以减少沿海奇观覆盖资源导致的港口相邻崩坏。“本城海洋资源”归属范围及改良资格等细节TBD，不自行改为只邻接资源。

**HARB-004** Lv4：Export Value。接入城市其它专业区域的Base/相关adjacency进入出口价值；本城自身Export Value采用更高效率的Actual/local比例；国际路线将Export Value转成收益。接入方向/资格、纳入哪些相关adjacency、具体比例、收益类型与去重规则TBD，不能擅自统一成本地或远端同系数。

**HARB-005 — Naval Military branch / ACCEPTED DIRECTION** Harbor保持完整Maritime Commerce + 完整Naval Military双线；Military II–IV默认平移至海军，规则见HARB-006至009。既有Harbor商业、专家/GPP及海洋资源、Export Value设计保留，不由本次平移覆盖。具体Naval unit eligibility、Harbor特殊建筑与Military建筑额外互动仍TBD。Naval Mobilization仍以最高级合法naval melee为方向，模型/阈值/生成细节另行细化，不自动采用MIL-004的陆军pool与编制方案。

**HARB-006 — Harbor II / ACCEPTED DIRECTION（默认平移）** 每名实际工作Harbor专家为本城训练的合格Naval combat units提供+15%正常Combat XP，遵守正常modifier互动与正常Combat XP cap；空槽不算。不添加或替换尚未明确的Harbor GPP数值。

**HARB-007 — Harbor III / ACCEPTED DIRECTION（默认平移）** `Naval Insight XP = min(E, floor(P / 2))`；E仅实际工作Harbor specialists，P为Naval unit实际拥有的Promotions（沿用Military实际晋升/合法合并继承口径，不用XP Level）。正常Combat XP之外独立追加，不修改正常8 XP cap，不擅自套用军营E≤4为港口槽位上限。

**HARB-008 — Harbor IV Naval Garrison Training / ACCEPTED DIRECTION（默认平移）** 合法训练位置为Harbor district，以及该Harbor城市中Naval unit可合法进入的City Center。Canal即使可通航也不是额外训练位置，不增加训练槽。沿用完整连续驻扎周期、初次进入不奖励、离开清除后重新计周期；每有效回合+1独立Training XP，按Military IV训练经验性质处理，不受正常Combat XP倍率放大。

**HARB-009 — Harbor IV Naval Frontline Mentorship / ACCEPTED DIRECTION（默认平移）** 合格海军战斗单位发生符合条件的战斗时，只检查相邻1格己方合格Naval combat units，取实际Promotion数量最高者。`DeltaP = P_mentor - P_fighter`；`Mentorship XP = max(0, floor(DeltaP / 2))`，多mentor不叠加，沿用Military IV独立奖励、非后方驻扎绑定、无额外hard cap及正常8 XP Combat cap不变的性质。仅记录设计，不调查技术可行性。

### Government Plaza — GOV

Government是特殊国家治理专业，不采用普通“专家→胜利yield”逻辑。Government Plaza建筑Tier 1/2/3主题分别为建立帝国、发展帝国、支持最终胜利路线。属于Future；Canal与外交state visit联动分别见CAN-001、DIP-MISSION。

**GOV-001 — Government building completion** Government专业城市完成某一Tier的一栋Government Plaza building后，自动完成/获得同Tier另外两栋。以专业的前期机会成本换取完整制度学习，而不局限于三选一。建筑互斥、免费完成时事件及一次性效果如何处理属于implementation feasibility，不改变此WHAT。

**GOV-002 — Governor Titles** Governor Titles绑定Government specialization的永久Potential投资，不绑定ACTIVE。建立Government专业、Potential Lv1时永久获得+1 Governor Title；Potential首次提升至Lv2、Lv3、Lv4时各再永久获得+1，累计最多+4。已经获得的头衔永久保留；Governor调离、未established或ACTIVE下降均不收回，也不会因重新激活而重复授予。永久投资代表帝国已经建立的治理能力，当前驻扎只决定高级Local能力是否ACTIVE；不能撤销已经获得并可能已经花费的全国头衔。本规则与GOV-003按ACTIVE计算的Wildcard slots是两个不同机制。

**GOV-003 — Government policy capacity** 额外Wildcard slots为`W = min(L, Government Tier)`，L为Government专业ACTIVE level，Government Tier为当前政府等级。Government IV在Tier 1/2/3/4政府分别增加1/2/3/4槽，不是在Tier 1直接+4。专业代表治理准备程度，政府等级限制制度当前能利用的能力。

**GOV-004 — Network** 向接收城市提供弱/辅助Loyalty支持，具体数值TBD；不是本专业核心，不额外发明大型网络能力。

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
| OPEN-03 | TBD | Government Network Loyalty具体数值；GOV-004 |
| OPEN-04 | IMPLEMENTATION / FUTURE_COMPATIBILITY / TBD | 旧档初始化仍独立OPEN，不自动沿用Conquest snapshot；永久UID及LegacySet冻结保存、Claim提供/移除、模式互斥与完成事件隔离留Development审查；Claim精确成本待定但受极低/短确认约束。无Identity征服城分流已由PROG-006至010正式解决，已有Identity继承不变 |
| OPEN-06 | TBD / DESIGN_DECISION_REQUIRED | Boost最终封顶等细节；最终一次floor(x+0.5)量化契约已按D0018确认；整数写入的实机验证属于Implementation，不是未决设计；不更改已定max规则 |
| OPEN-08 | IMPLEMENTATION_VALIDATION / TBD | GW-001百分比公式/创作者时代及文物历史时代例外已由D0022确定；固定yield与旧逐件补差路线均退出。百分比Modifier与theming结算待实机验证；异常创作者关联、未知自定义类别独立保留；GW002范围已由D0023确认 |
| OPEN-09 | RESOLVED / D0012 | 五档从工业Lv1全部开放；两侧按速度缩放，Crew生产力缩放后向下取整并显示整数，项目成本保留原生计算。 |
| OPEN-10 | PROVISIONAL BALANCE MODEL / TBD | Military IV归属/持续资格、合格陆军/战斗及快照口径见MIL-013；Mobilization已形成共享pool、L最高ACTIVE、N接收城去重、L√N/回合与阈值100的暂定模型，tier/合法编制双限制及最高ACTIVE源生成方向已记录；最终平衡、同级source tie-break、未明示资格及无位置处理待定；ENT适用范围仍独立；MIL-004 |
| OPEN-11 | ACCEPTED DIRECTION / TBD | Harbor商业等级/GPP与收益系数、Export接入/收益；Naval II–IV默认平移已登记（Harbor/合法City Center训练，排除Canal），具体Naval eligibility、特殊建筑额外互动和Naval Mobilization独立细化；HARB-005至009 |
| OPEN-12 | DESIGN_DECISION_REQUIRED / TBD | 永久保护国额度作用域/降级、多个外交来源、Spy经验/周转/死亡减幅；DIP |
| OPEN-13 | MIXED: PROVISIONAL / PREFERRED DESIGN CANDIDATE / THEME CANDIDATE ONLY / TBD | 外交/联盟等级解锁、任务周期/奖励/晋升适用；交流概率与未来fallback、Import Fair duration/selection/repeat、Migration Agreement duration/multiplier、军演函数/k、Pilgrimage资格/X等见DIP-MISSION-003至014；Infrastructure Coordination仅首选候选，Civilian Conversion仅主题候选，公共外交奖励暂定，外交区/市政广场仍Future骨架；不统一升级 |
| OPEN-14 | PROVISIONAL BUT ACCEPTED FRAMEWORK / TBD | Community Local Lv2/IV细节、资格锁定、专家槽cap/递减、Attractiveness权重及建筑分类、国际移民系数/C_map边界/结算细节、国内分发频率/等级边界/recipient资格和排序、Protected Floor依据和数值、人口政策项目细节、Lv4 Settler阈值（暂定8）及计数边界；详见COMM-001至011；旧国内Migration进度公式已被分发机制取代 |
| OPEN-15 | TBD / DESIGN_DECISION_REQUIRED | Local/Regional选择、公式/范围/叠加，有效专家对应机制；ENT |
| OPEN-16 | TBD | Dam的X；DAM |
| OPEN-17 | TBD | Canal叠加/归属/Community分支；CAN |
| OPEN-18 | TBD | Air训练未定参数、Airport Gold/Tourism系数及重复范围；AIR |

### 已确定作用域的后续兼容事项（非核心玩法未决）

**COMPAT-001 — IMPLEMENTATION / FUTURE_COMPATIBILITY** 旧档初始化见OPEN-04；多enabled玩家的多人确定性、AI实际行为质量、eligibility carrier和只对参与者运行的过滤方式留待Development／未来兼容处理。技术问题标记`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`，不能把通用资格设计、AI可参与、白板非永久唯一载体或征服休眠语义重新列为未决。

**COMPAT-002 — Commerce IV / IMPLEMENTATION_VALIDATION** D0024采用来源实际总产出与最终floor。动态择优/撤销、同回合刷新和第三方间接反馈仍需实测；不是任意Mod无环保证。

## 13. 设计审阅边界

本文保留当前可获得的v0.1等级规则及Future具体机制。Landscape、Religion、Government既有设计已按用户本次补充恢复；OPEN-01至03只记录剩余参数和规则边界，不再表示缺少整套专业设计。Future的TBD和PROVISIONAL不因整份文档将来被接受而自动成为确定数值。

Research/Culture共享强度、MIL-004暂定全国动员pool、Industry实际输出max和Community人口分发各按自身规则处理，不能互相覆盖。永久保护国与ACTIVE下降、Community资格与首次完成锁定、Virtual Specialists与实际工作专家等相互作用已列为显式审阅问题，不为实现便利默选答案。

本文件为D0010当前游戏设计意图权威，正式区分征服城市Legacy Claim、空候选Normal First Completion和已有Identity永久继承；其它设计继承D0009，历史冻结保留。Design仅维护WHAT，随后交Development自行sync并检查Conquest实现/测试，不在本对话修改Architecture/Status/Source/Tests或调查API。
