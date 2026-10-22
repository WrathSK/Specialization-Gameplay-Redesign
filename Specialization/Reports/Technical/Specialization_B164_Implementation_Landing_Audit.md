# B164 — 当前玩法落地审查与下一步计划

本轮结论：科研主要本地收益与文化「风雅熏陶」已经自动运行；「意义延展」仍是手动单城原型。时代对话、工业及商业仍有旧运行效果，不能把它们当成当前新设计已经实现。先收口意义延展，再开展巨作启迪；本报告不授权任何实现。

## 范围、依据与判定口径

调查基线为develop `799a377`，运行源码提交`e09ba9b`、B164.191／modinfo191。外部运行包身份只引用[现有部署状态](../../Status/Specialization_P0_Status.md#current-authoritative-state)；本轮没有重新核验运行目录。正式来源采用当前[Authority](../../Workflow/Authority.json)：Spec D0047；Research D0040、Culture D0046、Industry／Commerce／Shared D0045；Architecture A0161。

仅覆盖v0.1科研、文化、工业、商业及其直接共用基础。Military／Harbor／Government等未来设计不计入本轮未落地清单。读取当前正式能力对象、相关规则、实际注册与直接消费者、指定验收记录；没有重新审计全部历史或其它Mod。

「自动落地」要求正常加载、事件和当前资格驱动真实收益／业务，不依赖P0按钮启用。玩家完成项目／使用专业单位属于正常操作，不等于测试开关。代码注册、模型正确、诊断显示、原生原语通过、正式cutover是不同层次；Content中概括性的`implementation_status`也不能代替实际入口核对。

证据分开：`STATIC_CONFIRMED`为本轮源码／注册／规则核对；`LOCAL_SIMULATION_PASS`与`USER_GAME_TEST_PASS`只继承已记录的相符范围。本轮没有运行玩法测试，也没有产生新的实机PASS。

## 共同基础：已接入的部分与保留边界

| 项目 | 当前实际状态 | 可复用范围／仍缺什么 |
|---|---|---|
| 首次身份、Potential／ACTIVE、投资 | 已自动接入；投资为正常单位动作 | EffectiveFacts／CityProgressionStore／InvestmentAction提供当前事实和永久记录；不由诊断按钮授予收益 |
| 四专业一级基础支持、二级Housing／GPP | 已自动接入 | ResearchSupport／IndustrySupport／Lv2Housing／Lv2GPP；[B1](../../Status/Validation/Results/Specialization_B079_P0B1_User_Pass.md)、[B2](../../Status/Validation/Results/Specialization_B080_P0B2_User_Pass.md)用户验收保留，未外推完整目录或所有异常 |
| Shared绝对基础设施深度D | 已为实际消费者提供事实 | Catalog／DistrictCompleteness；B164社区覆盖修复为STATIC／LOCAL，原生合并后续测试；不等于全部HD目录完整PASS |
| 易主退出、原Owner同城恢复、未认领候选与认领 | E2已接入既定支持路径 | 模块定域退出、可靠同城证据、冻结候选、真实1T认领与持久续接可复用；[夺回](../../Status/Validation/Results/Specialization_B103_E2_Recapture_Pass.md)、[候选](../../Status/Validation/Results/Specialization_B111_E2_Conquest_Snapshot_Pass.md)、[认领冷加载修复](../../Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)不证明所有新专业资产生命周期 |
| 后台贸易网络桥接 | 已存在自动基础设施及旧消费者 | NetworkBridge等并非未实现；每个新payload仍须按自身资格、合并和撤销合同适配 |
| 馆藏事实与时代／件数通知 | K已接入 | GreatWorkFacts及确认样本由正常路径提供；[K验收](../../Status/Validation/Results/Specialization_B147_P0K_Pass.md)及B150后count通知可复用，不需新建collector |
| 完整1T项目技术 | 原型已验，认领已正式接入 | TimedProject本身仍是手动实验；ClaimProjects正式业务不等于时代对话／工程研习已经存在，不能复制其清Timer逻辑来决定别的历史资产 |
| 机构显示／carrier隐藏 | 已有U1前置显示，版式仍待优化 | 不是完整U1/U2验收；用户已明确视觉优化暂不阻碍开发，不在本轮重做 |
| 自动GC及公共更新约束 | 保留已接受运行缓解 | 性能专项已收束，剩余未归因增长不自动阻塞新功能；本轮不调参、不重开调查 |

直接运行依据：[Gameplay注册](../../../Mod/Gameplay.lua)、[当前城市事实](../../../Mod/EffectiveFacts.lua)、[持久进度](../../../Mod/CityProgressionStore.lua)、[认领](../../../Mod/ClaimProjects.lua)、[后台网络](../../../Mod/NetworkBridge.lua)。

## 科研：主要本地收益已落地，生命周期不能一概宣称完成

| 能力／系统 | 当前实际状态 | 证据与缺口 |
|---|---|---|
| 跨学科研究 | 自动运行 | ResearchCross：BASE输入、50%及用户许可的临时最终Floor，收益体现在学院；[D1用户验收](../../Status/Validation/Results/Specialization_B084_P0D1_User_Pass.md)保留 |
| 学以致用 | 自动运行 | ResearchApply：同产出领域合并后每专家Floor，再乘工作人数；[D2验收](../../Status/Validation/Results/Specialization_B085_P0D2_User_Pass.md)保留。不得误套Meaning逐领域Floor；B164社区改动尚无新原生PASS |
| 科研基础设施 | 自动运行 | ResearchInfrastructure：D×实际工作专家；[P0-C验收](../../Status/Validation/Results/Specialization_B081_P0C_User_Pass.md)保留 |
| 学术主持 | 自动运行 | ResearchChair：每座合格学院普通建筑获得专家数对应科技；[D3验收](../../Status/Validation/Results/Specialization_B086_P0D3_User_Pass.md)保留 |
| 学术传统日常计龄／科技倍率 | 自动运行 | ResearchTradition＋Effects＋进度账本；[F1](../../Status/Validation/Results/Specialization_B143_F1_Pass.md)及[F2](../../Status/Validation/Results/Specialization_B144_F2_Pass.md)已有所测年龄、5→10%、撤销与重启证据 |
| 学术传统失城／夺回 | 当前Design已定，运行适配缺失 | D0040明确随城保留、非支持Owner冻结、重新具备资格后恢复且不补失城年龄；源码失城仍写`OWNER_POLICY_UNRESOLVED`，夺回未转换该状态；Advance保持暂停，Effects仅接受COUNTING。不能把F2日常PASS扩成这一新规则已落地 |
| 科研网络 | 保留的旧网络公式已自动运行 | NetworkBoost已有k×最高ACTIVE×√接收城数及最终整数Boost。当前Design保留该规则并待重设计，不能写“科研网络完全没代码”，也不能写“未来科研网络重设计已完成” |

正式来源：[Research D0040](../../Design/Content/Research_D0040.json)。直接源码：[Cross](../../../Mod/ResearchCross.lua)、[Apply模型](../../../Mod/ResearchApplyModel.lua)、[Infra](../../../Mod/ResearchInfrastructure.lua)、[Chair](../../../Mod/ResearchChair.lua)、[Tradition模型](../../../Mod/ResearchTradition.lua)、[Tradition收益](../../../Mod/ResearchTraditionEffects.lua)。

## 文化：风雅熏陶已落地，其余新主体尚未完成

| 能力／系统 | 当前实际状态 | 仍需落地的内容 |
|---|---|---|
| 风雅熏陶 | 自动运行，所测范围已验收 | CultureAesthetic读取馆藏时代和普通建筑并应用旅游；[B149结算验收](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md)关闭本批门禁，不要求重做 |
| 意义延展 | 手动单城原型，五产出已取得限定原生证据 | 模型／载体不依赖玩家手算，但目标城仅由P0 ADVANCE建立；默认OFF。尚无正式全城自动writer／旧GWA全局cutover |
| 时代对话 | 旧自动效果仍运行，新项目未实现 | DialogueModel当前按馆藏时代差异即时算`25×max(0,X−1)`，Dialogue按ACTIVE IV施加。现行规则是ACTIVE III完整1T项目、每启动时代一次、完成时`5×X`累计，无额外累计上限；没有新项目／倍率和额度账本 |
| 巨作启迪 | 尚未实现；已有准备计划 | 0.1×D×W基础GPP原生小数、正常倍率及最终writer仍缺；不能按Meaning的Floor默认改成整数 |
| 人文考察团、文化见闻 | 尚未实现；已有准备计划 | 新专业单位、任务、唯一成功记录、当前Owner过滤和城市历史账本、本城旅游倍率尚未接入 |
| 新文化网络 | 尚未实现；旧Culture Eureka仍运行 | 新规则为每source完整三类考察文明集合→接收端集合并集→匹配专业工作专家文化；旧NetworkBoost的Culture→Eureka不是此能力 |
| 馆藏时代Hybrid D界面 | 尚未完成正式U2 | K诊断及机构UI不等于馆藏列表、摘要、tooltip的最终显示 |

正式来源：[Culture D0046](../../Design/Content/Culture_D0046.json)。直接源码：[Aesthetic](../../../Mod/CultureAesthetic.lua)、[Meaning模型](../../../Mod/CultureMeaningModel.lua)、[Meaning原型](../../../Mod/CultureMeaningProbe.lua)、[旧Dialogue模型](../../../Mod/DialogueModel.lua)、[旧Dialogue](../../../Mod/Dialogue.lua)、[旧GWA](../../../Mod/GreatWorkAdjacency.lua)、[旧Boost](../../../Mod/NetworkBoost.lua)。

### 意义延展为什么仍不是正式能力

- `Gameplay`注册模块只代表模块被加载；`CultureMeaningProbe.advance`才建立唯一`target`、BASELINE与ACTIVE会话。正常事件更新的是该手动目标，不会自动遍历并为所有合格文化城建立能力。
- B164只投影七领域／五产出；D0046仍接受九领域。市政／外交Culture按已授权条件暂隔离，全部92精确owned定义保留清理；未接管HD。临时延期不能改写成Design取消或完整能力PASS。
- [B161](../../Status/Validation/Results/Specialization_B161_Production_Single_Value_Native.md)、[B162](../../Status/Validation/Results/Specialization_B162_Meaning_Load_Cleanup_Native.md)、[B163](../../Status/Validation/Results/Specialization_B163_Meaning_Final_Yields_Native.md)分别证明所测单值、更新／W、清理或五项即时getter；没有因此证明所有作品的精准recipient、Dialogue／主题化独立、正常结算及正式多城接入。
- Lua已支持作品名单不等于SQL已精准过滤同类未知作品。当前SQL按七种`GreatWorkObjectType`附着，而模型遇到不支持对象整城拒绝；该fixture保护不能作为正式作品资格的新规则。
- END恢复的是旧GWA／Dialogue按当前事实的投影；旧BASE相邻路线仍存在。不能把实验内定域hold称作旧writer已经全局退役。

## 工业：账本已补齐，最新效果合同尚未适配

| 能力／系统 | 当前实际状态 | 缺口／与当前规则的差异 |
|---|---|---|
| 标准化模板初始化／恢复／reconcile | 已自动接入 | Standardization＋CityProgressionStore明确首次初始化、可靠历史并集、空账本及损坏保护；[B142验收](../../Status/Validation/Results/Specialization_B142_Template_Pass.md)仅证明所测初始记录及重启，不外推A∪B与实际折扣全部原生PASS |
| 标准化收益与模板网络 | 旧自动折扣仍运行，当前新规则未落地 | StandardizationDiscount以ACTIVE≥1来源并集group、全来源最高等级决定折扣；SQL为Level×10%。新规则要求来源ACTIVE≥3、建造10%／购买0%基线、IV加2×L、每模板只在实际holder内独立取MAX；模板账本正确不等于收益规则正确 |
| 工程动员／施工队 | 旧项目与单位路径可用，当前完整规则未适配 | 旧项目五档成本280／460／820／1100／1500，施工力250／420／750／1000／1360；CrewProjects按工业身份及锚点开放，未按III→I–III、IV→IV–V分档。当前150%及实践折减、每城2支来源库存与最新专业单位保护不能由旧项目存在推为已实现 |
| 巨构工程学 | 新能力未实现 | 本城普通生产旧时代奇观的时代差1／2／3+→10／20／30%，没有对应已注册writer；固定施工队注入原语不能代替此能力 |
| 工程实践 | 新能力未实现 | 城市历史真实奇观数N、1／3／6阈值、IV组建成本150→140／130／120%及按城历史保存尚无完整对应路径 |
| 工程传统 | 新能力未实现 | 全国亲建奇观时代E、城市完整1T研习L、保存／暂停／恢复及标准化2×L增强未接入；ResearchTradition不是工业传统 |
| 旧工业网络生产复制 | 旧自动效果仍在 | CopyYields仍读取工业IV区域生产的50%给予接收城。当前工业网络只负责模板连接，没有独立生产payload；后续工业cutover须精确处理该旧writer |

正式来源：[Industry D0045](../../Design/Content/Industry_D0045.json)。直接源码：[模板](../../../Mod/Standardization.lua)、[折扣](../../../Mod/StandardizationDiscount.lua)、[折扣SQL](../../../Mod/Data/StandardizationDiscount.sql)、[施工队资格](../../../Mod/CrewProjects.lua)、[旧项目成本](../../../Mod/Data/CrewProjects.sql)、[施工力与速度](../../../Mod/Probe.lua)、[一次注入](../../../Mod/UnitActions.lua)、[旧网络复制](../../../Mod/CopyYields.lua)。最新工业调整为Design-only，未由本轮或B164转为运行实现。

## 商业：基础已接入，新独有体系尚未落地

| 能力／系统 | 当前实际状态 | 仍需落地的内容 |
|---|---|---|
| 商业化 | 新机制未实现；旧直接连接类型支持仍运行 | 专家容量、领域选择／LIFO暂停恢复、Absolute D及来自直连城市的领域价值、Gold0.1转换尚无当前writer；Lv3Effects的三类连接标记不是新商业化 |
| 资本投资（稳健／风险） | 尚未实现 | quote、锁定本金／D／S／期限／随机结果、到期结算、hidden failure protection、保存及已定合同终止规则 |
| 发展投资 | 尚未实现 | 定向外发路线、目标建筑域、锁定合同及建造50%加算、到期／失效／资本退还与标准化叠加 |
| 资产重组 | 尚未实现 | 组建／绑定团队、两个区域动作、REALLOCATING、扰动、P−1及易主事务规则；普通Claim不代表重组已实现 |
| 商业信誉 | 尚未实现 | 身份期间积累、ACTIVE IV输出、身份退出清零、易主冻结及恢复；学术传统不能直接类推为相同资产 |
| 旧Commerce IV 20%汇聚 | 旧自动效果仍在 | CommerceConvergence默认AUTO，从指向商业城的直连来源读SCIENCE／CULTURE／PRODUCTION最高总量×20%并Floor；当前Design不保留此payload，后续商业cutover须撤销 |

正式来源：[Commerce D0045](../../Design/Content/Commerce_D0045.json)。直接源码：[旧Lv3连接类型效果](../../../Mod/Lv3Effects.lua)、[旧IV汇聚](../../../Mod/CommerceConvergence.lua)、[全部实际注册](../../../Mod/Gameplay.lua)与[modinfo](../../../Mod/SpecializationP0.modinfo)。既有Investments是Settler专业潜力投资，不是上述Gold合同。

## 需要纠正的完成度与计划表述

1. 正确表述是「科研主要本地能力已自动实现并按已测范围验收」；不是「科研除网络外所有最新生命周期均已完成」。学术传统Owner规则已经由Design关闭，现代码保留旧暂停分支，是适配缺口，不再需要用户重新设计归属。
2. 「意义延展五项原语／单城原型通过」不能写成「意义延展正式落地」。后续报告固定区分自动接入、旧writer cutover和原生门禁，已通过原语证据不撤销。
3. 旧自动收益仍运行，是迁移状态，并不表示本轮发现它们就获得关闭授权。新合同落地时逐模块撤销自身exact owned效果，不按前缀批量删除。
4. [总实施计划](../../Architecture/v2/D0032_Implementation_Plan.md)保留批次目标，旧进度不能代替Status。后续模块已有计划需按当前Authority重新核对：例如[时代对话M](../../Architecture/v2/P0_M_Dialogue.md)的cap未定已被无额外累计上限取代；[考察N](../../Architecture/v2/P0_N_Expedition.md)的旧原Owner账本及K_T未定已与当前城市历史／K_T2%不同。本轮只登记差异，不静默实施或改写这些旧准备文件。

## 下一建议：先完成意义延展正式接入

状态为`PLAN_ONLY / IMPLEMENTATION_NOT_AUTHORIZED`。详细切片见[当前L2计划](../../Architecture/v2/P0_L2_Meaning.md#下一建议--意义延展正式接入)。建议分成两个有明确停止点的批次，而不是继续把每个新yield做成独立手动原型后就转去下一能力。

### L2正式接入前的剩余门禁

复用B164五产出单值、Shared D、K事实及现有诊断。只处理三个仍会影响正式writer的未知：

- **精准作品资格**：已支持作品与同class未知作品混合时，证明原生实际受益集合与Design一致；不能用整城拒绝或把未知作品悄悄纳入当作解决。先查现有DB／接口和实际附件，本地能确认的不上实机；确需引擎验证只补一个最小混合fixture。
- **追加独立**：B164实验强制旧Dialogue0%，尚不代表与正常倍率共存。使用一个已验yield，比较正常原生产出倍率／主题化前后追加值是否保持；倍率只改变原生产出。不要再次尝试接管HD Culture。
- **真实结算**：优先检查已验Production追加是否进入普通生产的正常进度，而不仅Great Work窗口getter；其它项只补仍不能由原生路径或现有证据支持的差异。两阶段尽量合并一个连续session；社区D6／Food3顺带确认，不另派一轮社区测试。

本地做定向模型／exact附件／资格、同回合D/W与重复通知、退出及直接消费者回归；已有shared load／reference／退出测试继承。原生步骤只验证新增差异，不再机械要求保存启用副本→END→冷加载→再启用。

**退出**：三个门禁有明确PASS或具体技术阻塞结论。若精准recipient或独立收益无法满足Design，停止对应正式cutover，报告不能满足的具体条款及选择；不补造作品资格或数值。Culture继续为已授权临时延期。不能因为五项即时getter正确就直接全城上线。

### L2五产出正式自动writer与旧GWA cutover

前述门禁关闭后单独授权正式接入：

- 正常加载／当前资格即派生收益；覆盖所有受支持玩家的合格文化城，不再需要P0手动目标。保留Culture延期标签，不能声称九域完整能力完成。
- 复用D、K confirmed事实与输入版本；同回合真实D/W变化更新受影响城市。旧／新producer逐个核对，跨城移动只更新实际来源／接收城市；全国影响才扩大范围。
- 明确一个module-owned派生writer与临时缓存生命周期；无新增永久成果账本。UNKNOWN不能当0，confirmed loss按模块退出。默认诊断只读，历史probe只能显式DEV进入并与正式writer互斥。
- 正式撤销旧BASE相邻GWA投影／正向入口，保留必要历史清理定义；移除实验Dialogue0%／100%hold，正常Dialogue共存不得混写。当前旧Dialogue项目迁移留M，不在L2偷做新倍率账本。
- 定向L2正确性／L3退出加载回归；一次最小native整合：不碰P0即自动生效、D/W替换、只在实际需要时用第二城核对隔离、真实结算与资格撤销。因为这里确实改变初始化／退出／load ownership路径，才补一个针对性冷加载；不重跑无关能力或长测。

**退出**：五项正式自动接入及旧GWA cutover经过本地与新增native差异验证；不要求玩家记得开测试按钮。Culture延期、未覆盖目录／对象和未测边界明确保留。

### 随后的顺序与独立事项

1. 巨作启迪：沿现有[L3计划](../../Architecture/v2/P0_L3_Inspiration.md)验证小数基础GPP，然后正式接入；不是本轮或L2自动授权。
2. 时代对话：先按当前D0046更新旧准备计划，再建立1T业务与城市历史倍率／时代额度，并退役旧即时25%路线。
3. 人文考察／见闻／新文化网络及U2：分别按依赖落地，更新旧Owner合同与已定K_T；不以旧Eureka当新网络。
4. 工业：模板基础保留，先补N／E／L与最新标准化收益／holder MAX，再适配施工队档位／成本／来源容量／保护及巨构；具体批次另行计划。
5. 商业：路线／领域事实→商业化／信誉→资本合同→发展合同→重组，分别制定最新合同和cutover边界，不在当前文化批次实现。

**可独立提前修复**：学术传统失城／夺回仍旧暂停分支。它是已定规则的窄适配，可单独计划；不要求先完成商业重组或工业全体系。不阻塞L2三个独立门禁，但在宣称科研最新生命周期完成前必须关闭。

本轮不产生新的Gameplay决定。除非后续技术结果要求改变玩法，当前用户仅需审阅实施顺序和具体批次授权；无需重复旧实机测试。

## 本轮检查与停止

工作区调查前clean且与origin/develop同步；当前context完整性检查PASS（182 runtime／445 guarded），实际模块注册和上述直接分支已核对。报告／计划／当前导航的90个本地链接／锚点及当前manifest选择器已检查通过；CURRENT与L2当前切片仍各8行，不扩大默认读取集合。最终context与diff检查随交付核对，不把机械PASS写成新Gameplay或native PASS。

不修改Design、Mod、测试逻辑、部署工具或GC；不部署、不启动游戏、不改main。本轮到审查报告与待审计划为止。
