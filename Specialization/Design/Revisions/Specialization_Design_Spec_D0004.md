# Specialization Gameplay Redesign — Design Spec

Document Owner: Codex
Design Authority: User
Design Revision: D0004
Document State: ACCEPTED
User Acceptance: ACCEPTED
Acceptance Date: 2026-09-11
Acceptance Evidence: 用户针对按有效完成通知先后锁定的建议明确答复“是的，你的建议没问题，继续”
Previous Accepted Revision: [D0003冻结原文](Revisions/Specialization_Design_Spec_D0003.md)
Latest Accepted Design Revision: D0004

## 1. 文档范围与确认边界 — SCOPE

**SCOPE-001** 本文是整个Specialization Gameplay Redesign的WHAT，覆盖当前v0.1及已确认的未来设计；不是实现说明或验证报告。规则ID用于后续引用，不表示该规则已经实现。D0004按用户确认明确专业完成通知的先后锁定规则；继承D0003 Community暂定但已接受框架及其它设计，剩余未决项仍保留原状态。

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

**PROG-004** 专业、Potential及已经完成的标准化投资属于保持的事实；接入、接收与强度随当前有效资格重算。征服后身份/投资是否继承、旧城市缺失首次完成历史如何处理仍为DESIGN_DECISION_REQUIRED，不从现有区域猜测。完成先后规则已由PROG-005确定。

**PROG-005 — 完成通知顺序 / ACCEPTED** 对具有可靠新城历史资格的城市，按游戏交付的有效专业区域完成通知先后顺序，首个有效通知锁定专业；之后的通知，包括同回合其它候选，不覆盖已锁定专业。有效通知必须通过当前城市身份、区域类型与完成状态以及历史资格检查，加载通知不能作为新完成。多个候选同时完成也采用该通知先后规则，不按区域类型优先级排序、不将整个回合合并为同时完成。规则可能依赖游戏及其它Mod的通知交付顺序；它不授权用缺失历史的旧DEV观察替代正式首次完成，也不决定征服继承或旧档初始化。

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

**MIL-003** Lv4提供驻扎训练与高等级老兵带教；训练频率、目标资格、上限和系数TBD。

**MIL-004** Military Network积累Mobilization Progress，规模采用类似`k × L × sqrt(N)`的边际递减。达到阈值生成当前可训练的最高级近战陆军，扣除阈值并保留overflow。系数、阈值、多来源归属、生成位置及“当前可训练”资格边界TBD；不默认移植Research/Culture的max合并。

**MIL-005 — Military II / Combat XP — ACCEPTED** 每名实际工作的Encampment specialist提供**+15% Combat XP**，适用于本Military专业城市训练出的对应陆地军事单位。空专家槽不计算。这是正常Combat XP modifier，与HD现有Barracks/Stable、Military Academy及其它正常经验modifier正常叠加，与经验政策卡按游戏正常规则互动。不修改单次8 XP Combat XP cap，不通过额外奖励绕过该cap。

设计目标是允许玩家以人口/专家投入购买训练质量。Military Academy、更多working specialists、XP policy分别代表建筑选择、人口投入和政策槽投入。主要按不装备额外XP政策卡的环境平衡；允许玩家付出军事政策槽机会成本，将正常Combat XP更快推向8 XP cap，不为政策卡环境反向削弱Military II。

**MIL-006 — 三级建筑与平衡原则** 已确认槽位设计背景：军营区域基础1槽，tier3建筑后合计最多4槽。Barracks/Stable、Military Academy及XP政策仍按HD/游戏原有规则提供收益。本系统不重新平衡Military Academy与Military Political Department本身的生产、编制、战斗力、经验差异，不要求两条路线严格数学等价或50/50选率。

Military Academy已有经验训练、直接训练更高级编制及其它质量路线价值；Military Political Department具有数量路线价值。明确不采用“Military Academy额外virtual instructors / virtual specialists”方案。玩家可以选择Military Academy+较少专家、Political Department+更多专家、Military Academy+大量专家、使用XP policy，或Political Department配合单位合并培养部队。Specialization提供相对中立的专家体系，目标是有意义的资源配置选择。

**MIL-007 — Insight XP与正常Combat XP的边界 — ACCEPTED** 正常Combat XP完全遵守游戏正常计算与单次8 XP cap。Military III的Insight XP在正常Combat XP结算之外独立追加；例如8 normal Combat XP + 3 Insight XP = 11 total XP gained，不是把Combat XP cap改为11，不修改或移除8 XP cap。当前极端情况P≥8且E=4时，可获得8 normal Combat XP + 4 Insight XP = 12 total XP gained，这是已接受的高级军事教育收益，正常Combat XP cap仍为8。普通新兵P=0或1时Insight为0；真正拥有高级战术知识的单位可从同一场实战额外获得少量经验理解。实现可行性状态：`IMPLEMENTATION_FEASIBILITY_TO_BE_REVIEWED_BY_DEVELOPMENT`；本设计修订不进行技术调查或实现承诺。

**MIL-008 — 有效专家范围与修订边界** 当前Military II/III仅计实际工作军营专家；Entertainment Local Support未来形成的Effective/Virtual Specialists是否参与两者，仍属于ENT有效专家适用范围的独立Design Decision，本轮不决定。Military I、Military III的5F5P、Military IV、Mobilization、Harbor naval mirror和Aerodrome扩展保持既有设计状态；不因本次接受而补全未来模块的未定参数。Military继续属于OUT_OF_V0.1。

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
| OPEN-04 | DESIGN_DECISION_REQUIRED | 征服继承、旧档专业初始化；完成通知顺序已由PROG-005确认 |
| OPEN-05 | DESIGN_DECISION_REQUIRED | 首都本地自接入与源/中心重合资格；NET |
| OPEN-06 | TBD / DESIGN_DECISION_REQUIRED | Boost精度、量化、最终封顶等细节；NET-RC，不更改已定max规则 |
| OPEN-07 | DESIGN_DECISION_REQUIRED | Industry多源模板/折扣/输出合并；IND-NET |
| OPEN-08 | TBD / DESIGN_DECISION_REQUIRED | Great Work时代/曲线/类别、theming/Tourism倍率、非传统区域与Actual范围；GW/TERMS |
| OPEN-09 | TBD | Crew游戏速度、档位时点；CREW |
| OPEN-10 | TBD / DESIGN_DECISION_REQUIRED | Military IV训练频率/目标资格/上限/系数、Mobilization系数/阈值/多来源归属/生成位置/可训练资格仍TBD；Military II +15%及Military III Insight体系已ACCEPTED，不再为候选或整条曲线未定。MIL-002上限边界已由用户澄清并关闭；ENT虚拟专家适用范围仍独立待定；MIL |
| OPEN-11 | TBD | Harbor商业等级/系数、Export接入/基数/收益、海军参数；HARB |
| OPEN-12 | DESIGN_DECISION_REQUIRED / TBD | 永久保护国额度作用域/降级、多个外交来源、Spy经验/周转/死亡减幅；DIP |
| OPEN-13 | TBD / DESIGN_DECISION_REQUIRED | 联盟/专业等级任务解锁、九类任务精确奖励和晋升适用；DIP-MISSION |
| OPEN-14 | PROVISIONAL BUT ACCEPTED FRAMEWORK / TBD | Community Local Lv2/IV细节、资格锁定、专家槽cap/递减、Attractiveness权重及建筑分类、国际移民系数/C_map边界/结算细节、国内分发频率/等级边界/recipient资格和排序、Protected Floor依据和数值、人口政策项目细节、Lv4 Settler阈值（暂定8）及计数边界；详见COMM-001至011；旧国内Migration进度公式已被分发机制取代 |
| OPEN-15 | TBD / DESIGN_DECISION_REQUIRED | Local/Regional选择、公式/范围/叠加，有效专家对应机制；ENT |
| OPEN-16 | TBD | Dam的X；DAM |
| OPEN-17 | TBD | Canal叠加/归属/Community分支；CAN |
| OPEN-18 | TBD | Air训练未定参数、Airport Gold/Tourism系数及重复范围；AIR |

## 13. 设计审阅边界

本文保留当前可获得的v0.1等级规则及Future具体机制。Landscape、Religion、Government既有设计已按用户本次补充恢复；OPEN-01至03只记录剩余参数和规则边界，不再表示缺少整套专业设计。Future的TBD和PROVISIONAL不因整份文档将来被接受而自动成为确定数值。

Research/Culture最高ACTIVE规则与source-specific未来进度/工业输出不互相覆盖。永久保护国与ACTIVE下降、Community资格与首次完成锁定、Virtual Specialists与实际工作专家等相互作用已列为显式审阅问题，不为实现便利默选答案。

本文件为D0003当前游戏设计意图权威，按用户本轮明确确认更新Community暂定但已接受框架；其它设计继承D0002，D0001/D0002原文及其接受记录冻结保留。本文仅维护WHAT，不更新Architecture、Status、Source或Tests，不开展技术调查、P0测试或游戏验证。其它TBD、PROVISIONAL和未接受候选仍保持原状态；设计接受不承诺实现或验证结果。
