# Specialization content schema v1

Document Maintainer: Codex
Design Authority: User

Design记录与决策边界见[W0005](../../Workflow/README.md#w0005--authority-and-repository-knowledge)。本索引只导航内容权威，不授予新玩法决定或实施权限。

[Research D0040](Research_D0040.json)是当前Research Lv1–Lv4的唯一结构化内容正文（D0026/D0028原表冻结为历史），保存已冻结的机械合同、第一版中文Tooltip及领域映射。状态为 **DESIGN_FROZEN / implementation and balance validation pending**。Accepted Spec的RES节引用此表，不复制另一套新公式。仅Design冻结，不代表运行包实现。

[Industry D0045](Industry_D0045.json)沿同一结构扩展`parameters`（值与BALANCE_REQUIRED分离）、`contracts`（模板/历史/施工队范围）、`review_markers`（已确认但以后复审）、`superseded_old_rules`。Industry为DESIGN_FROZEN，候选命名和待平衡参数保留独立成熟度。

## D0047 — 当前市政基线与全系统载体范围

[Government D0047](Government_D0047.json)是市政完整结构化正文：[中文阅读版](../Government.md)解释治所／内政司／典制院／国策府及1／1／2／3七项能力。旧自动补建筑、永久总督头衔、旧Wildcard公式与Loyalty网络正式取代；内政司／政制择用工作名、费用折扣、k首测候选、生命周期与技术分别保留，不声称全部细节冻结。

全系统当前只向专用白板文明开放，资格与未来复用边界以[Spec ELIG](../Specialization_v0.1_Design_Spec.md#system-scope--opt-in-player-eligibility--elig)为准；不默认全原版／Mod文明与领袖能力叠加兼容。Government仍未来范围，当前v0.1只实施四专业；不修改Mod或当前待验任务。Culture现行D0046恢复九域六产出，Shared／Industry／Commerce D0045、Research D0040、Military／Harbor D0037原件不变。以下旧修订段是接受来源追溯，不覆盖本段当前入口。[接受与取代](../Design_ChangeLog.md#accepted-d0047--2026-10-04)。

## D0028共享入口

[Shared_D0045](Shared_D0045.json)是当前区域基础设施深度、产出份额、普通建筑资格、领域映射及Network层概念的唯一权威（D0028保留历史）；[Culture](Culture_D0046.json)与Research通过引用使用。领域存在映射不意味着每个能力适用全部领域，各能力显式列出适用域。已有冻结历史表不得倒改。

未来Civilopedia只从Shared生成一份术语说明，Tooltip正式用语为“区域基础设施深度”“一份产出”；历史“区域完善度”为同一D的旧称，runtime文字尚未迁移；UI实施未授权。Culture新增missions、state_tooltips、observations/network contracts与动态状态字段；D0029确认Culture完整考察文明集合并集；D0040明确取代其见闻原Owner分账，见闻与Dialogue为各自城市历史并分开当前有效资格；D0028内容与Review保留历史，不再代表这些边界的当前状态。

## 规范化表与本地化

- `institutions`：specialization、level、稳定institution_id、中文名、英文参考、RP简介、Potential门槛、状态及ability_ids。每个机构只记录一次。
- `abilities`：稳定ability_id→institution_id；名称、Tooltip、mechanical_contract、input_facts、output_effects、ACTIVE/Potential门槛、状态、notes_compatibility与待决引用。
- `base_effects`：无named ability的基础效果。Lv1不强造能力名称。
- `yield_mapping`：学以致用的统一领域→产出映射及价值换算；不从Tooltip反推映射，不把它隐式当其它能力的区域白名单。
- `district_qualification` / `decisions_resolved`：共同区域资格与本轮已关闭边界；未知类型按已确认默认排除并报告。

中文是正式语言目标，英文名仅reference；`null`表示TBD，不是空白发布文本。未来增加en_US Tooltip或语言键，不改变Mechanical Contract。内容ID不依赖显示名称，也不是游戏数据库Building Type。

本表目前仅设计数据，不加入modinfo、不作为运行输入。机构与能力一对多；既有0/1/2/3是专业安排而非通用硬上限。Harbor III/IV各有商业与海军两个同时成立的机构。每个Tooltip解释本阶段新增能力，永久机构存在与当前能力启用分开。技术载体不出现在玩家文案里。

## 人类阅读入口

[Design中文阅读导航](../README.md)集中提供Shared、Network、四专业及已有实质记录的未来专业／辅助区域正文，不在本索引重复整张目录。

共同定义集中在Shared／Network；专业正文直接写全自身效果、数值、特殊条件与例外，不退化为ID和链接索引，也不重复整套共同教程。合同锁定、结算、隐藏保护、重组等影响决策的规则仍属于专业玩法。共同页从正式来源维护，不由某一专业反推全局规则。

用户通过Design Talk提供决定和反馈，由Codex维护正式Spec／Content等来源，并原则上在同一设计变更批次同步受影响阅读页；阅读版不是独立Design authority。Shared改变只检查实际受影响的专业说明，普通代码／测试／部署变更不触发整套Design重写。阅读页不自动加入所有任务强制读取集合：Codex仍按W0001从正式来源作任务范围读取，不每轮加载全部正文。中文阅读结构沿用用户认可的商业样板；其它新页待阅读审核，不重开已接受玩法。

## 单一权威与修订

已经纳入Content的专业，其公式、文案、映射以JSON为唯一编辑位置；未纳入的未来规则仍由Spec保存。[审阅记录](../../Historical/Design/Reviews/Research_D0026_Review.md)引用ID，不复制第二套权威公式。Accepted Spec的RES条目已指向content；D0025历史原文冻结不倒改。Industry及Culture已加入；其余专业后续沿同schema分别维护，不强制命名能力数量。各专业JSON是自身内容权威，Spec引用，Review只作审阅记录。

## D0045 — 工业、Shared与商业当前增量；文化接受基线由D0046恢复两域

[Industry D0045](Industry_D0045.json)保留D0044首测职责，正式每模板实际有效持有来源择优、已有合法Gold/Faith、完整1T研习取消／重做但历史L不变、最终整数Floor。[Culture D0045](Culture_D0045.json)收口无额外Dialogue cap、Spy等价成本、全国现存考察团cap1、K_T=2个百分点；风雅1／Meaning0.5／启迪0.1／K_C1／标准任务2T与D0042归属保持。不是数值最终平衡或实现验收。

[Shared D0045](Shared_D0045.json)增加具名未提交研习与专业单位不可捕获／转Owner保护，专属生命周期优先；`ORIGINAL_CAPITAL_SPECIAL_REFORM`为完整**FUTURE／DESIGN_RECORDED／NOT_V0.1_IMPLEMENTATION**记录，不进当前计划。[Commerce D0045](Commerce_D0045.json)只同步专业单位保护，公式与旧窄未决保持。Research D0040、Military／Harbor D0037原件及其它未来条款不变；旧D0044／43／42原件不改。[本轮接受](../Design_ChangeLog.md#accepted-d0045--2026-10-03)／[覆盖、取代与真实剩余](../../Historical/Design/Reviews/Industry_Culture_Future_D0045_Review.md)。当前B159待验不变，无Mod／实施／部署。

## D0044 Industry职责与首测值 — 历史接受基线，现行D0045增量

[Industry D0044](Industry_D0044.json)正式采用标准化基础10%／Gold0%、四级研习L每层两项各2个百分点、四级工程实践降低组建损耗、III／IV按等级开放施工队、巨构10／20／30%只加速自行生产及固定注入隔离。三级成本150%，四级才按N1／3／6降至140／130／120%；五档标准速度施工力与成本已给首测表，非最终平衡。名称候选／占位、技术及未提交研习边界仍分别登记。[Shared D0044](Shared_D0044.json)仅新增成功研习L为A城市历史，E仍B文明历史，易主E<L不截断已有L。D／目录／份额／其它A–G不变；[本轮接受](../Design_ChangeLog.md#accepted-d0044--2026-10-03)及[审阅](../../Historical/Design/Reviews/Industry_D0044_Review.md)。Culture D0043／Commerce D0042／Research D0040保持原件，本轮不实现／不部署，不改变B158单城待验。

## D0043 Meaning七域 — 已由D0046九域恢复取代，原件仅追溯

[Culture D0043](Culture_D0043.json)仅将意义延展政府广场／外交区来源暂排，当前为七域五产出；`contracts.meaning_domains`是本能力白名单，`contracts.domains`仍保留其它consumer使用的完整映射。K／份额／逐领域Floor／作品资格／独立追加／A–G生命周期保持。Shared／其它专业原件不变；[接受记录](../Design_ChangeLog.md#accepted-d0043--2026-10-03)。文化追加技术及负面证据保留供未来恢复，不阻碍本版v0.1；剩余yield／recipient／倍率／结算仍需实际实现与证据。此次仅Design同步与计划，不改运行包或部署。

## D0042 long-term lifecycle A–G — 保留的具名生命周期来源

[Shared D0042](Shared_D0042.json)、[Culture D0042](Culture_D0042.json)、[Industry D0042](Industry_D0042.json)、[Commerce D0042](Commerce_D0042.json)为本轮生命周期来源；现行Commerce／Shared／Industry／Culture为D0045，保留本段具名生命周期及后续D0043七域／D0044工业职责；本段只记当时来源，不覆盖D0045增量；[Research D0040](Research_D0040.json)已符合本轮重申、保持原件。E未提交对话／任务、F选择栈与派生、G单位来源及Settler确认原子性按具名合同关闭；A–D及D0041固定追加保留。LIFO暂停不删除，来源易主不等于单位转交，训练source不等于重组target。精确未决与[T1–T11对照](../../Historical/Design/Reviews/Long_Term_State_D0042_Review.md)独立记录；[接受记录](../Design_ChangeLog.md#accepted-d0042--2026-10-03)。该轮只有Design同步、B155测试继续，无运行适配或部署；这是当时的进度描述，当前任务仅由Status／Authority派发。

## D0031 boundary amendment

Research学术传统身份暂停与Industry有限施工队库存要求见新content；旧D0030/D0027冻结。Culture Gameplay仍D0029；[时代馆藏展示需求与未批准UI建议](../../Historical/Design/Records/Culture_Era_Presentation_D0031.md)独立记录，不修改Shared。

## D0041 Culture fixed additions — retained multiplier decision

[Culture D0041](Culture_D0041.json)保留D0038逐领域Floor与D0040生命周期，按用户最新决定明确Meaning追加不受Dialogue／theming放大；市政／外交追加文化不因同yield成为native。较早主题化包含追加的设想只留未来选项与技术档案；不承诺primitive已能隔离，不改K／资格或补差。当次其它四份D0040正文保持；现行D0042只增量更新生命周期，Culture D0040/D0041冻结；[接受记录](../Design_ChangeLog.md#accepted-d0041--2026-10-03)。

## D0040 long-term lifecycle A–D — retained decisions, E/F/G updated by D0042

[Shared](Shared_D0040.json)新增具名A城市历史／B文明历史／C机构关系／D成立合同语法；[Research](Research_D0040.json)、[Industry](Industry_D0040.json)、[Culture](Culture_D0040.json)、[Commerce](Commerce_D0040.json)分别维护精确生命周期。数字、名称与无关能力对象保留；不是统一Legacy engine或新存档schema。文化见闻Owner键和本城工程实践Owner限制被明确取代，商业合同关键城易主及信誉Owner规则关闭。E/F/G未讨论边界保持，当前B154 Meaning direct contracts不变；不实现、不部署。[接受／替代及真正未决](../../Historical/Design/Reviews/Long_Term_State_D0040_Review.md)。此前D0031／35／36／38／39原件冻结保留；下列修订段落是来源历史；D0040生命周期继续有效，Culture追加倍率边界见D0041。

## D0039 Commerce v0.1 closure — historical base

[Commerce D0039](Commerce_D0039.json)为D0039时商业机械内容权威，现行生命周期由D0040增量替代；五领域商业化、资本/风险/发展主要公式与首版数值、信誉身份清零、已签合同身份变化连续执行及重组征服退出已接受。机构/能力名与D0032结构保持；精确剩余定义与一般Ownership只按新content登记，不把已关闭TBD继续当前化。[收口审阅](../../Historical/Design/Reviews/Commerce_D0039_Review.md)。不是实现或最终Balance通过。

## D0032 Commerce freeze / historical baseline

[Commerce_D0032](Commerce_D0032.json)为当时Commerce冻结内容，现行增量由D0039取代，DESIGN_FROZEN不等于balance/implementation完成。Lv1/II既有基础规则保留，III5F5P已由用户取消；旧III网络专家与IV20%汇聚退出。合同/mapping/参数/Legacy的待决成熟度显式保留，不能由实现者默认补齐。

schema-v1复用institutions/abilities/base_effects/contracts/parameters；新增supersession、legacy_review_required、architecture_requirements作为设计登记，不是运行save schema。Industry_D0032只关闭来源容量2及关联文字；Research_D0031、Culture_D0029、Shared_D0028字节不变。[Hybrid D](../../Historical/Design/Records/Culture_Era_Presentation_D0032.md)为当前批准展示方向，D0031推荐与边界文件保留历史。[Freeze review](../../Historical/Design/Reviews/Commerce_D0032_Review.md)。共同REALLOCATING隔离要求见Spec PROG-011；不机械升级Shared。

## D0033 Military freeze

[Military_D0033](Military_D0033.json) is DESIGN_FROZEN with [review](../../Historical/Design/Reviews/Military_D0033_Review.md). Five candidate blockers resolved; units keep permanent birth ability snapshots, formation max per ability, full upgrade-line mobilization and separate commanders for disconnected networks. Naming placeholders/Balance/Technical/Legacy remain explicit. Other profession and Shared authority unchanged. Military implementation is not authorized; old candidate/source records remain historical.

## D0034 Military amendment — historical mechanism provenance

[Military_D0034](Military_D0034.json) replaces D0033 for Military only: 综合训练 now combines breadth→permanent unit quality and absolute Shared D→local training efficiency, within the same named ability. [Review and explicit deferred conversion details](../../Historical/Design/Reviews/Military_D0034_Review.md). No relative normalization, no invented Production coefficients; Shared and other professions unchanged. D0033 links above are historical freeze provenance.

## D0035 Shared clarification — retained semantic base

[Shared D0035](Shared_D0035.json)明确D为Absolute Infrastructure Depth，正式中文“区域基础设施深度”，无Relative Completeness。公式与各consumer玩法不变。[引用覆盖、consumer矩阵、独立catalog待办](../../Historical/Design/Reviews/Shared_D0035_Review.md)。既有profession文件引用Shared_D0028时，当前解释按Spec的D0035覆盖声明；历史文件不倒改。当次Military保持D0034；当前D0037只更新两处名称，其双层机制不重复修订。

## D0036 Industry template reconciliation — retained base

[Industry D0036](Industry_D0036.json)在D0032基础上只加入IND-TEMPLATE-006：模板为城市经验；首次合法工业身份及确认夺回时可靠历史∪当前合格建筑；显式区分初始化、恢复、同步与缺史保护。原D0032冻结保留；Shared与其它专业不变。不扩大目录、折扣或AI范围。

## D0037 Harbor baseline / Military naming — current authority

[Harbor D0037](Harbor_D0037.json)是港口当前结构化正文：完整双线、III/IV同级双机构、商业海运/出口/进口/经营积累，以及当前Military海军镜像；无独立Harbor Network或司令城。accepted机制与可冻结/强候选/暂定名字、占位机构、Balance/Technical/Legacy各自标示，不称全部细节冻结。未来范围，不扩大v0.1。

[Military D0037](Military_D0037.json)取代D0034作为当前文件，仅正式名称行伍编制/战地勤务及Harbor明确镜像引用更新；其它Military机制逐对象保持。D0034及更早原件不改。[接受与旧条款冲突映射](../../Historical/Design/Reviews/Harbor_D0037_Review.md)；[港口阅读版](../Harbor.md)、[军事阅读版](../Military.md)。新内容不加入runtime或文化任务必读集合。

## D0038 Culture Meaning Extension Floor — retained base

[Culture D0038](Culture_D0038.json)在D0029基础上仅明确意义延展：每领域先换算为实际产出并分别Floor，之后同yield相加，最后乘合格巨作件数W。系数0.5、金币份额3、领域与作品资格、原生产出倍率隔离保持；不外推GPP。D0029原件与旧Shared引用保留，按当前Spec的D0035覆盖声明解释；其它primitive及完整运行切换未接受。

D0046仅恢复意义延展政府广场／外交区的文化输入；其它专业／Shared仍D0045，Culture原生共存门禁未自动通过。
