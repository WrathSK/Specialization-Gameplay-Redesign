# Specialization content schema v1

Document Maintainer: Codex
Design Authority: User

Design记录与决策边界见[W0005](../../Workflow/README.md#w0005--authority-and-repository-knowledge)。本索引只导航内容权威，不授予新玩法决定或实施权限。

[Research D0031](Research_D0031.json)是当前Research Lv1–Lv4的唯一结构化内容正文（D0026/D0028原表冻结为历史），保存已冻结的机械合同、第一版中文Tooltip及领域映射。状态为 **DESIGN_FROZEN / implementation and balance validation pending**。Accepted Spec的RES节引用此表，不复制另一套新公式。仅Design冻结，不代表运行包实现。

[Industry D0036](Industry_D0036.json)沿同一结构扩展`parameters`（值与BALANCE_REQUIRED分离）、`contracts`（模板/历史/施工队范围）、`review_markers`（已确认但以后复审）、`superseded_old_rules`。Industry为DESIGN_FROZEN，候选命名和待平衡参数保留独立成熟度。

## D0028共享入口

[Shared_D0035](Shared_D0035.json)是当前区域基础设施深度、产出份额、普通建筑资格、领域映射及Network层概念的唯一权威（D0028保留历史）；[Culture](Culture_D0038.json)与Research通过引用使用。领域存在映射不意味着每个能力适用全部领域，各能力显式列出适用域。已有冻结历史表不得倒改。

未来Civilopedia只从Shared生成一份术语说明，Tooltip正式用语为“区域基础设施深度”“一份产出”；历史“区域完善度”为同一D的旧称，runtime文字尚未迁移；UI实施未授权。Culture新增missions、state_tooltips、observations/network contracts与动态状态字段；D0029已确认Culture完整考察文明集合并集及见闻/Dialogue分离归属；D0028内容与Review保留历史，不再代表这些边界的当前状态。

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

本轮的公式、文案、映射以JSON为唯一编辑位置；[审阅记录](../../Historical/Design/Reviews/Research_D0026_Review.md)引用ID，不复制第二套权威公式。Accepted Spec的RES条目已指向content；D0025历史原文冻结不倒改。Industry及Culture已加入；其余专业后续沿同schema分别维护，不强制命名能力数量。各专业JSON是自身内容权威，Spec引用，Review只作审阅记录。

## D0031 boundary amendment

Research学术传统身份暂停与Industry有限施工队库存要求见新content；旧D0030/D0027冻结。Culture Gameplay仍D0029；[时代馆藏展示需求与未批准UI建议](../../Historical/Design/Records/Culture_Era_Presentation_D0031.md)独立记录，不修改Shared。

## D0039 Commerce v0.1 closure

[Commerce D0039](Commerce_D0039.json)为当前商业机械内容权威；五领域商业化、资本/风险/发展主要公式与首版数值、信誉身份清零、已签合同身份变化连续执行及重组征服退出已接受。机构/能力名与D0032结构保持；精确剩余定义与一般Ownership只按新content登记，不把已关闭TBD继续当前化。[收口审阅](../../Historical/Design/Reviews/Commerce_D0039_Review.md)。不是实现或最终Balance通过。

## D0032 Commerce freeze / historical baseline

[Commerce_D0032](Commerce_D0032.json)为当时Commerce冻结内容，现行增量由D0039取代，DESIGN_FROZEN不等于balance/implementation完成。Lv1/II既有基础规则保留，III5F5P已由用户取消；旧III网络专家与IV20%汇聚退出。合同/mapping/参数/Legacy的待决成熟度显式保留，不能由实现者默认补齐。

schema-v1复用institutions/abilities/base_effects/contracts/parameters；新增supersession、legacy_review_required、architecture_requirements作为设计登记，不是运行save schema。Industry_D0032只关闭来源容量2及关联文字；Research_D0031、Culture_D0029、Shared_D0028字节不变。[Hybrid D](../../Historical/Design/Records/Culture_Era_Presentation_D0032.md)为当前批准展示方向，D0031推荐与边界文件保留历史。[Freeze review](../../Historical/Design/Reviews/Commerce_D0032_Review.md)。共同REALLOCATING隔离要求见Spec PROG-011；不机械升级Shared。

## D0033 Military freeze

[Military_D0033](Military_D0033.json) is DESIGN_FROZEN with [review](../../Historical/Design/Reviews/Military_D0033_Review.md). Five candidate blockers resolved; units keep permanent birth ability snapshots, formation max per ability, full upgrade-line mobilization and separate commanders for disconnected networks. Naming placeholders/Balance/Technical/Legacy remain explicit. Other profession and Shared authority unchanged. Military implementation is not authorized; old candidate/source records remain historical.

## D0034 Military amendment — historical mechanism provenance

[Military_D0034](Military_D0034.json) replaces D0033 for Military only: 综合训练 now combines breadth→permanent unit quality and absolute Shared D→local training efficiency, within the same named ability. [Review and explicit deferred conversion details](../../Historical/Design/Reviews/Military_D0034_Review.md). No relative normalization, no invented Production coefficients; Shared and other professions unchanged. D0033 links above are historical freeze provenance.

## D0035 Shared clarification — current authority

[Shared D0035](Shared_D0035.json)明确D为Absolute Infrastructure Depth，正式中文“区域基础设施深度”，无Relative Completeness。公式与各consumer玩法不变。[引用覆盖、consumer矩阵、独立catalog待办](../../Historical/Design/Reviews/Shared_D0035_Review.md)。既有profession文件引用Shared_D0028时，当前解释按Spec的D0035覆盖声明；历史文件不倒改。当次Military保持D0034；当前D0037只更新两处名称，其双层机制不重复修订。

## D0036 Industry template reconciliation — current authority

[Industry D0036](Industry_D0036.json)在D0032基础上只加入IND-TEMPLATE-006：模板为城市经验；首次合法工业身份及确认夺回时可靠历史∪当前合格建筑；显式区分初始化、恢复、同步与缺史保护。原D0032冻结保留；Shared与其它专业不变。不扩大目录、折扣或AI范围。

## D0037 Harbor baseline / Military naming — current authority

[Harbor D0037](Harbor_D0037.json)是港口当前结构化正文：完整双线、III/IV同级双机构、商业海运/出口/进口/经营积累，以及当前Military海军镜像；无独立Harbor Network或司令城。accepted机制与可冻结/强候选/暂定名字、占位机构、Balance/Technical/Legacy各自标示，不称全部细节冻结。未来范围，不扩大v0.1。

[Military D0037](Military_D0037.json)取代D0034作为当前文件，仅正式名称行伍编制/战地勤务及Harbor明确镜像引用更新；其它Military机制逐对象保持。D0034及更早原件不改。[接受与旧条款冲突映射](../../Historical/Design/Reviews/Harbor_D0037_Review.md)；[港口阅读版](../Harbor.md)、[军事阅读版](../Military.md)。新内容不加入runtime或文化任务必读集合。

## D0038 Culture Meaning Extension Floor — current authority

[Culture D0038](Culture_D0038.json)在D0029基础上仅明确意义延展：每领域先换算为实际产出并分别Floor，之后同yield相加，最后乘合格巨作件数W。系数0.5、金币份额3、领域与作品资格、原生产出倍率隔离保持；不外推GPP。D0029原件与旧Shared引用保留，按当前Spec的D0035覆盖声明解释；其它primitive及完整运行切换未接受。
