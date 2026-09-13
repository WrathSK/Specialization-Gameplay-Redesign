# Specialization Gameplay Redesign — Design Spec

Document Owner: Codex
Design Authority: User
Design Revision: D0001
Document State: ACCEPTED
User Acceptance: ACCEPTED
Acceptance Date: 2026-09-11
Acceptance Evidence: 用户明确回复“D0001接受”
Latest Accepted Design Revision: D0001

## 1. 文档范围与确认边界 — SCOPE

**SCOPE-001** 本文是整个Specialization Gameplay Redesign的WHAT，覆盖当前v0.1及已确认的未来设计；不是实现说明或验证报告。规则ID用于后续引用，不表示该规则已经实现。D0001已由用户明确接受；未决项仍保留其原有状态。

**SCOPE-002 — CURRENT IMPLEMENTATION SCOPE — v0.1** Research/Campus、Culture/Theater Square、Industry/Industrial Zone、Commerce/Commercial Hub，以及共同成长、Trade Center、网络核心、Construction Crew和这些专业的跨系统规则。范围不等于实际完成度。

**SCOPE-003 — ACCEPTED FUTURE DESIGN — OUT_OF_V0.1** Landscape/Preserve、Religion/Holy Site、Military/Encampment、Harbor、Government Plaza、Diplomatic Quarter、Community/Metropolis、Entertainment/Water Park、Aqueduct、Dam、Canal、Aerodrome/Airport、Spaceport、Alliance Diplomatic Missions。此标签表示用户已经确认列入未来设计的范围/明确机制，不表示Future进入v0.1实现范围；各条PROVISIONAL、candidate、TBD状态不得被本标签覆盖。

**SCOPE-004** 用户是最终Design Authority。Codex负责整理落盘；外部设计顾问内容在用户接受前仅是proposal/review。没有用户明确确认，不得把后续修订或候选数值升级为ACCEPTED。

## 2. 测试文明与基本术语 — ID / TERMS

**ID-001** 以独立新文明和独立领袖承载测试，不修改或覆盖原版Scotland。暂时复用Scotland的文明/领袖视觉、名称风格和可用展示资产，不复制其原有游戏能力。玩家可见名称采用Scotland (Specialization Test)、Robert the Bruce (Test)等明确测试标记。暂不制作原创美术与历史设定。

**ID-002** Industrial Zone保持正常科技位置，不作为提前解锁的特色区域。

**TERMS-001** Specialization是城市专业身份；Potential是该城永久投资形成的潜力；ACTIVE是当前实际激活的专业等级。三者不得互相替代。Working specialist指实际工作的对应专家，空槽不算。

**TERMS-002** Base adjacency只指基础相邻，不包含政策等相邻倍率。Actual在本设计中指与煤炭发电厂/大酒店“按区域产出复制”机制相同口径的区域产出基数，不是城市总产出，也不要求先建成这些建筑；不等同于“只取政策翻倍后的相邻数字”。具体非传统收益/区域适用范围待澄清时，不擅自扩大或删减。

**TERMS-003** F=Food，P=Production，S=Science，C=Culture，G=Gold。百分点是对百分比数值直接相加，不是相乘增幅。

## 3. 共同成长与永久投资 — PROG

**PROG-001** 城市在第一个符合条件的专业区域**完成建造**后锁定专业，不在放置区域时锁定。v0.1四种专业及对应替代区域适用；未来Community特殊候选见COMM-001，不能提前改变v0.1规则。

**PROG-002** 专业确定后默认Potential Lv1。在己方城市消耗一个Settler，永久Potential +1，最高Lv4。Potential不由source数量、网络强度或网络积累产生。不凭空给没有专业的城市发专业能力。

**PROG-003** Lv2/3/4分别要求Potential至少2/3/4，并有已建立的总督满足2/3/4头衔门槛。ACTIVE取当前满足全部条件的最高等级；无已建立总督或总督调离时，已有专业仅保留Lv1，Potential投资不丢失。门槛不是要求额外消耗同样数量的Settler或额外重复支付头衔。

**PROG-004** 专业、Potential及已经完成的标准化投资属于保持的事实；接入、接收与强度随当前有效资格重算。征服后身份/投资是否继承、旧城市缺失首次完成历史如何处理、同时完成多个候选区域的顺序规则为DESIGN_DECISION_REQUIRED，不从现有区域猜测。

## 4. v0.1共同Lv2规则 — SHARED

**SHARED-001** ACTIVE Lv2起，对应专业区域本体及该区域每一级建筑各+1 Housing。

**SHARED-002** 每名实际工作的对应专家增加+2基础GPP，之后正常接受其它GPP百分比加成：Research→Great Scientist；Industry→Great Engineer；Commerce→Great Merchant；Culture每名Theater专家同时获得Great Writer、Great Artist、Great Musician各+2。不能将基础GPP改为不受倍率影响的直接点数奖励。

**SHARED-003** 下列Lv3“提升至”取代低等级对应专家食物/生产力档位，不把3F3P与5F5P重复叠加。Housing、GPP及其它独立已解锁能力继续保留。

## 5. Research / Campus — RES

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| RES-001 | Lv1 | 每名Campus工作专家额外+3F、+3P |
| RES-002 | Lv2 | 获得SHARED-001住房及SHARED-002 Scientist基础GPP |
| RES-003 | Lv3 | 专家支持提升至+5F、+5P；本城增加`0.5 × Population × working Campus specialist count`基础Science |
| RES-004 | Lv4 | 每名Campus工作专家使本城Science增加5个百分点；本城其它合格非Campus专业区域的Actual复制基数各类产出总和的50%转为Science |

**RES-005** Research Network增加Inspiration完成比例的额外百分点；强度统一按NET-RC规则，不按路线线性叠加。

## 6. Culture / Theater Square — CUL

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| CUL-001 | Lv1 | 每名Theater工作专家额外+3F、+3P |
| CUL-002 | Lv2 | 获得SHARED-001住房；每名专家同时获得三种文化伟人基础GPP |
| CUL-003 | Lv3 | 专家支持提升至+5F、+5P；本城增加`0.5 × Population × working Theater specialist count`基础Culture |
| CUL-004 | Lv4 | 每名Theater工作专家使本城Culture增加5个百分点；获得GW-001时代保值及GW-002巨作基础相邻能力 |

**CUL-005** Culture Network增加Eureka完成比例的额外百分点；使用NET-RC，不交换Research/Culture对应的Boost种类。

### Great Works — GW

**GW-001** Culture Lv4的旧Great Works随时代获得补贴，使其达到当前时代对应的基础Great Work yield level。目标是补足基础水平，不擅自以帝国最高产作品替代当代标准。时代口径、作品类别对应曲线及缺失标准时的规则TBD。

**GW-002** Culture Lv4每件符合条件的文化Great Work额外获得本城专业区域Base Adjacency Yields的50%。明确使用BASE，不使用Actual复制基数，不将政策翻倍算入这部分基础相邻。

**GW-003** 优先排除Product及其它非标准文化Great Works。Relic、未知自定义类别和非传统区域的最终适用清单仍DESIGN_DECISION_REQUIRED，不把宗教题材艺术与Relic混为一类。Culture、Tourism、theming和作品专属加成如何影响补贴的最终玩法边界需用户确认；不假定所有倍率当然适用。

## 7. Industry / Industrial Zone — IND

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| IND-001 | Lv1 | 每名IZ工作专家+3F，并增加相当于本城IZ Base Production adjacency的Production；从Lv1固有可用Construction Crew |
| IND-002 | Lv2 | 获得SHARED-001住房与Engineer基础GPP |
| IND-003 | Lv3 | 专家Food提升至+5F，保留100% Base Production adjacency的Production，并增加其2倍的Gold；不改为通用固定5P |
| IND-004 | Lv4 | 本城IZ Production的Actual复制基数50%经工业网络输出；多来源输出的接收/叠加规则仍待决定，不套用NET-RC的max规则 |

### Industrial Network / Standardization — IND-NET

**IND-NET-001** 接收Industrial Network的城市可获得建筑Gold购买折扣：Industry I/II/III/IV为10%/20%/30%/40%。工业源必须已完成该建筑的标准化。优先按相同District和Building Tier匹配；若需固定同Tier建筑组，必须明确范围，不暗中扩大适用对象。

**IND-NET-002** 仅影响Gold购买，不能同时改变Faith购买。不得以退款、放宽解锁或改变购买资格等方式默默改变实际玩法语义。标准化账本保持，但断开/消失的源不再提供当前资格。

**IND-NET-003** 多工业源模板资格并集、折扣选择与Lv4输出叠加仍DESIGN_DECISION_REQUIRED；保留所有来源信息，不默认求和、最高值或均值。

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

**CREW-004** 空队列或非法目标拒绝动作，不消耗单位。游戏速度如何缩放项目成本/可转移量、档位可用时点等未明确细节TBD，不自行加门槛。

## 8. Commerce / Commercial Hub — COM

| Rule ID | ACTIVE等级 | 当前设计 |
|---|---|---|
| COM-001 | Lv1 | 每名Commercial Hub工作专家+3F、+3P；该商业专业城市具有Trade Center身份 |
| COM-002 | Lv2 | 获得SHARED-001住房与Merchant基础GPP |
| COM-003 | Lv3 | 专家支持提升至+5F、+5P；每接入Research/Culture/Industry网络类型，专家分别额外+2S/+2C/+2P。同类型多源不重复提供该类型奖励 |
| COM-004 | Lv4 | 本中心免费作为已接入网络的接收城市，仅获得network effects；并入接收集合去重，不是固定追加Boost百分点 |

## 9. Trade Center与Network核心 — NET

**NET-001** Trade Route Capacity本身就是网络带宽；不额外创建每路线载荷分配、round-robin或手动网络选择界面。首都与商业专业城市为Trade Center；首都的本地专业如何自接入仍DESIGN_DECISION_REQUIRED，不能由“中心身份”自动推导。

**NET-002** 己方专业源S→己方中心H的有效路线形成直接接入。H维护当前接入的专业网络集合。H→己方城市D的每条有效distribution路线自动携带H当前全部已接入网络。

**NET-003** 一条路线可同时使目的城进入Research、Culture、Industry等接收集合；外贸、道路或贸易站本身不等于这种己方接入。收到网络的另一个中心不因此变成直接源，不递归转发。合法免费资格与路线资格共存，失去其中一种时，只要仍有其它有效资格就保留接收。

**NET-004** 路线结束、取消、战争/征服/端点失效等使路线不再有效时，相关接入/接收资格撤销，不能仅因过去曾建立过路线而继续享受网络。读档后应反映当前真实集合，无需玩家打开贸易界面恢复网络。

### Research / Culture共享强度 — NET-RC

**NET-RC-001** `Network Strength = k × L × sqrt(N)`。Research使用独立可调k_R，Culture使用k_C，初始测试均为1。结果是Research额外Inspiration百分点、Culture额外Eureka百分点。

**NET-RC-002** `N`是当前实际接收该类型网络的己方城市UID去重数量，绝不是source数、raw路线数、全帝国城市数或中心总路线数。同城多路线、多中心、免费资格重叠均只计一个recipient。未来其它合法接收方式也进入同一去重集合。

**NET-RC-003** 多个当前有效接入的同类型来源，`L = max(all valid source ACTIVE specialization levels)`；使用ACTIVE而非Potential。来源数量本身不增加N。统一选L后只计算一次强度，禁止分别按来源求强度后相加，禁止`Σ(k × L_i × sqrt(N))`或逐中心求和。

**NET-RC-004** 最高等级源失效后立即回退到剩余有效源的最高ACTIVE。无有效来源时Strength归零，不保留stale Strength；N=0时Strength也为零。该max规则只适用于Research/Culture等共享强度模型，不自动扩展到Industry、Mobilization或Migration的source-specific结算。

**NET-RC-005** Culture IV、16个接收城市为+16个百分点；8城约+11.31个百分点。小数/量化规则TBD，不自行round/floor/ceil；不假设所有环境的基础Boost比例固定为40%。已触发Boost不补发，额外进度不能溢入下一科技/市政；最终封顶等未明示细节须另行确认。

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

**MIL-001** Lv1每名working Encampment specialist获得+3F/+3P基础支持。Lv2军营及对应建筑继承SHARED-001住房；每名working Encampment specialist提供**+2 base Great General GPP**，之后正常接受GPP百分比加成，并提高本城训练陆军的combat XP gain。XP增幅仍TBD，+15%仅为MIL-005候选；共同支持、住房和基础GPP不再是资料缺口。

**MIL-002** Lv3专家支持提升至5F5P；按单位已有晋升数量提供越来越高的XP补偿，而不是简单再叠一层统一XP倍率。补偿曲线TBD。

**MIL-003** Lv4提供驻扎训练与高等级老兵带教；训练频率、目标资格、上限和系数TBD。

**MIL-004** Military Network积累Mobilization Progress，规模采用类似`k × L × sqrt(N)`的边际递减。达到阈值生成当前可训练的最高级近战陆军，扣除阈值并保留overflow。系数、阈值、多来源归属、生成位置及“当前可训练”资格边界TBD；不默认移植Research/Culture的max合并。

**MIL-005 — BALANCE_CANDIDATE_NOT_ACCEPTED** 每名working Encampment specialist +15% XP仅是待计算候选，不是accepted数值。

**MIL-006** 已确认槽位设计背景：军营区域基础1槽，tier3建筑后合计最多4槽。后续平衡需同时考虑Barracks/Stable +25%、Military Academy +25%、XP政策卡与combat XP breakpoint；这些是需纳入模型的背景输入，不把+15%候选提前落实。

### Harbor：完整双线 — HARB

**HARB-001** Harbor定位为**100% maritime commerce + 100% naval military**，不是各半的两套能力。

**HARB-002** 商业线包括Great Merchant与Great Admiral、marine improvement/resource收益。未指明的等级分配、GPP及改良产出系数TBD，不截掉任一条线。

**HARB-003** Lv3：本城全部海洋资源，无论是否紧邻Harbor，都提供Harbor正常资源Base adjacency，以减少沿海奇观覆盖资源导致的港口相邻崩坏。“本城海洋资源”归属范围及改良资格等细节TBD，不自行改为只邻接资源。

**HARB-004** Lv4：Export Value。接入城市其它专业区域的Base/相关adjacency进入出口价值；本城自身Export Value采用更高效率的Actual/local比例；国际路线将Export Value转成收益。接入方向/资格、纳入哪些相关adjacency、具体比例、收益类型与去重规则TBD，不能擅自统一成本地或远端同系数。

**HARB-005** 海军线原则上平移Military的XP、高晋升补偿、驻扎训练和老兵带教。Naval Mobilization生成当前可训练的最高级naval melee；阈值/系数与其它细节TBD，Military未定数值不因“平移”变为accepted。

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

**DIP-MISSION-001 — Future Advanced Module** 对非盟友作为Spy，对盟友作为Diplomat。优先延续现有按区域选择任务的交互方式，使和平任务与熟悉的间谍任务操作框架一致；不进入v0.1。

**DIP-MISSION-002** 和平任务：

| 目的区域 | 任务 | WHAT |
|---|---|---|
| Campus | Academic Exchange | 随机触发当前合法且尚未触发的Eureka；不是偷盟友已研究的科技 |
| Theater | Cultural Exchange / Touring Exhibition | 不移动Great Works；根据己方Great Works产生Tourism burst；不同文化流派任务为未来候选 |
| Commercial Hub | Business delegation | 产生Gold，不从盟友扣除；数值TBD |
| Industrial Zone | Industrial/technical cooperation | 具体效果TBD |
| Holy Site | Religious/cultural dialogue | 具体效果TBD |
| Harbor | Maritime/trade cooperation | 具体效果TBD |
| Encampment | Joint military exercises | 具体效果TBD |
| Diplomatic Quarter | Summit/embassy | 偏Influence、Alliance Points、Favor；精确奖励TBD |
| Government Plaza | State visit | 偏Era Score、Influence等；精确奖励TBD |

**DIP-MISSION-003** 成功Diplomatic Mission仍提供Spy XP与Era Score；现有Influence类Spy晋升尽量继续有效。Diplomatic专业等级与Alliance LvI/II/III如何控制任务解锁/收益尚未设计。所有任务周期、奖励系数及具体晋升适用范围TBD，不能提前填统一数值。

### Community / Metropolis — COMM

**COMM-001 — PROVISIONAL: thematic framework accepted, gameplay strength not yet proven.** HD中的Community/Neighborhood不是普通specialty district，不占普通区域容量且解锁较早，允许特殊Community专业候选。暂定在其它专业身份确定前完成一个Neighborhood即可取得资格，一个暂定足够；Lv2–4仍正常消耗Settler并要求Governor。取得资格是否立即锁定及与共同锁定规则的优先关系仍须明确。

**COMM-002** 核心身份为population carrying capacity + automatic population redistribution，不是单纯提高出生率。本城Lv1–4尚未完成，重点为Neighborhood专家产出、Food、Amenity carrying capacity，以及无限Neighborhood/大量专家槽的cap或递减。具体表TBD。

**COMM-003 — PROVISIONAL** `Migration Progress += k × L × sqrt(N)`；达到阈值后source Community city人口−1、eligible receiving city人口+1、扣除阈值、保留overflow。N的接收集合沿用网络去重概念；k、L多源选择、累计周期、阈值、移民资格与无合法目标时的处理TBD。

**COMM-004** 目的地加权偏向较低人口、剩余Housing更多、Amenities较高的城市，不做manual migration UI。权重具体公式TBD。

**COMM-005** source population protected floor随Neighborhood building tier提高。概念标尺tier1约>10、tier2约>15、tier3约>20，具体值TBD；这些不是已接受的精确门槛。

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
| OPEN-04 | DESIGN_DECISION_REQUIRED | 征服继承、旧档专业初始化、同时完成候选区域顺序；PROG |
| OPEN-05 | DESIGN_DECISION_REQUIRED | 首都本地自接入与源/中心重合资格；NET |
| OPEN-06 | TBD / DESIGN_DECISION_REQUIRED | Boost精度、量化、最终封顶等细节；NET-RC，不更改已定max规则 |
| OPEN-07 | DESIGN_DECISION_REQUIRED | Industry多源模板/折扣/输出合并；IND-NET |
| OPEN-08 | TBD / DESIGN_DECISION_REQUIRED | Great Work时代/曲线/类别、theming/Tourism倍率、非传统区域与Actual范围；GW/TERMS |
| OPEN-09 | TBD | Crew游戏速度、档位时点；CREW |
| OPEN-10 | TBD / BALANCE_CANDIDATE_NOT_ACCEPTED | Military XP增幅、Lv3晋升数补偿曲线、Lv4训练/带教、Mobilization参数；+15%非accepted。Lv1支持、Lv2住房与+2 base Great General GPP已恢复；MIL |
| OPEN-11 | TBD | Harbor商业等级/系数、Export接入/基数/收益、海军参数；HARB |
| OPEN-12 | DESIGN_DECISION_REQUIRED / TBD | 永久保护国额度作用域/降级、多个外交来源、Spy经验/周转/死亡减幅；DIP |
| OPEN-13 | TBD / DESIGN_DECISION_REQUIRED | 联盟/专业等级任务解锁、九类任务精确奖励和晋升适用；DIP-MISSION |
| OPEN-14 | PROVISIONAL / TBD | Community全部本城等级、资格锁定、槽位递减、Migration多源/周期/阈值/权重/人口底线；COMM |
| OPEN-15 | TBD / DESIGN_DECISION_REQUIRED | Local/Regional选择、公式/范围/叠加，有效专家对应机制；ENT |
| OPEN-16 | TBD | Dam的X；DAM |
| OPEN-17 | TBD | Canal叠加/归属/Community分支；CAN |
| OPEN-18 | TBD | Air训练未定参数、Airport Gold/Tourism系数及重复范围；AIR |

## 13. 设计审阅边界

本文保留当前可获得的v0.1等级规则及Future具体机制。Landscape、Religion、Government既有设计已按用户本次补充恢复；OPEN-01至03只记录剩余参数和规则边界，不再表示缺少整套专业设计。Future的TBD和PROVISIONAL不因整份文档将来被接受而自动成为确定数值。

Research/Culture最高ACTIVE规则与source-specific未来进度/工业输出不互相覆盖。永久保护国与ACTIVE下降、Community资格与首次完成锁定、Virtual Specialists与实际工作专家等相互作用已列为显式审阅问题，不为实现便利默选答案。

用户已明确接受D0001，本文件现为游戏设计意图的权威。Architecture正式同步尚待开展，既有Architecture不得覆盖本文件。文档所有WHAT均不承诺实现或验证结果；TBD、PROVISIONAL和未接受候选仍保持原状态。
