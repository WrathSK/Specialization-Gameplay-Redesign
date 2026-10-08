# P04a/P11a — Culture当前能力、旧writer与城市历史

独立审计 IA20261007 / W18；基线 `1cd5e07060325677c67cba1061be3caefef6a5ab`。项目本体只读；slice覆盖完成不等于全部Culture/native或总审计PASS。

## 结论

现行L1风雅熏陶和L2七域五产出意义延展正常自动运行；L3只启动默认OFF的单城Scientist probe，新M时代对话项目、N人文考察和U2尚未实施。旧Dialogue仍动态运行，旧GreatWorkAdjacency已以retired模式只保留退出职责。它们与正式设计的差距均在[文化准备](../../Architecture/v2/Culture_Preparation.md)和直接计划明示，不伪装成已完成，也不因设计已定自动切换writer。

没有新高返工风险finding。既有公共callback、事实扫描、owned协议和持久核心耦合仍按原ID/timing保留；这次完善Culture使用面，不重复制造同类问题、不恢复B168待办、不运行新原生测试。

## 正式合同与当前支持矩阵

完整[Culture D0048](../../Design/Content/Culture_D0048.json)、[Spec CUL](../../Design/Specialization_v0.1_Design_Spec.md#6-culture--theater-square--cul)是规则来源；准备/计划/源码/具名结果负责技术和证据，不从晚更新的报告反推Design。名称、首测参数、待平衡和实施范围各自保留。

| 能力 | 已接受合同 | 当前source / 未落地范围 |
|---|---|---|
| 基础/II | 实际Theater专家基础支持、住房和三类文化GPP；旧III人口收益/IV专家城市百分比已取代 | Shared支持和精确旧Culture退出已接，不能将每种收益统称Culture能力已完成 |
| 风雅熏陶 L1 | ACTIVE III；每个合格普通建筑贡献当前合格不同作品时代数X的Tourism；不是W/历史最大值 | [Aesthetic](../../../Mod/CultureAesthetic.lua)＋[模型](../../../Mod/CultureAestheticModel.lua) normal AUTO；当前事实变更可重投影，输入不变零拆建；UNKNOWN不冒充0 |
| 意义延展 L2 | ACTIVE IV；逐域floor(0.5×D×份额)，再同yield合计×W；Gold份额3；无Tourism；Dialogue不放大追加；主题化暂许可、Balance待验 | [Meaning](../../../Mod/CultureMeaning.lua)＋[模型](../../../Mod/CultureMeaningModel.lua) normal AUTO。当前七域五yield；正式九域六yield的市政/外交Culture仍隔离，不接管HD载体。原生主题化观测×2不是固定普遍公式 |
| 巨作启迪 L3 | ACTIVE IV；每个合格非文化class基础GPP=0.1×D×W，无专家/X要求，吃正常GPP百分比 | [InspirationProbe](../../../Mod/CultureInspirationProbe.lua)仅固定0.1/0.3/0.6/1 Scientist原语；未接正式六class/D/W、未启用总量Floor备用；[L3](../../Architecture/v2/P0_L3_Inspiration.md) native待验 |
| 时代对话 M | ACTIVE III完整1T；每城每START GameEra最多一次成功；完成当前X×5个百分点永久加算无额外cap；本来作品产出，不放大Meaning追加 | 新项目/成功账本/额度/native-only writer均未落地。[旧Dialogue](../../../Mod/Dialogue.lua)是ACTIVE IV当前馆藏25%×max(0,X−1)，不含历史，正式[P0-M](../../Architecture/v2/P0_M_Dialogue.md)应替换，不可当新规则实现 |
| 人文考察 N | ACTIVE IV组建，当前Spy成本/全国现存cap1；任务2标准T；不同外国文明PEOPLE/WORKS/PLACES报告按城市历史去重；当前有效见闻每个本城2ppTourism | 单位/任务/报告/归档/整体Tourism/新Network尚未落地，[P0-N](../../Architecture/v2/P0_N_Expedition.md)及[UI](../../Architecture/v2/P0_N_Expedition_UI.md)只是接受后的技术计划 |
| N Network | 各ACTIVE IV来源先独立形成完整三类文明，再对完整集合UNION；每个有效完整文明每receiver实际专家+1 Culture，不跨来源拼残片/递归 | 当前旧Culture network不是新见闻network；不能把普通K国内时代索引用于外国成功报告，也不能恢复被取代娱乐支持规则 |

三处未衔接Shared/未来专业边界保持原样；完整网络拓扑复用[P02b](P02b_Network_Contract_Layers.md)，不凭Culture网络设计改共同合同。

## 状态ownership与切换边界

| 状态 | authority / owner / 生命周期 |
|---|---|
| 当前馆藏K | [GreatWorkFacts](../../../Mod/GreatWorkFacts.lua) session当前native作品/目录确认；Summary171–190重新检查Owner/reference，仅返计数/X等标量；Read完整复制和Domestic索引按需，不是永久见闻账本 |
| L1/L2效果 | 当前事实→纯模型→module-owned精确carrier/plot flags。保存carrier不是权威；normal load按当前事实重建。confirmed loss由Store定域撤销，UNKNOWN保留规则不变 |
| L2 legacy | Gameplay777 retired=true启动GWA，正向Init/Audit/Receive有retired门禁，退出入口仍保留。Meaning持精确92符号，先退出自己/旧writer再构造需要的单值载体，不按前缀删外部建筑 |
| L2 Probe | 正常Gameplay不启动旧MeaningProbe；旧请求由正常Meaning只读Describe截断。P0按钮双侧STATUS不是玩家需开启能力。独立probe代码存在不等于当前默认运行 |
| L3测试 | 单目标/session/stage/last token为临时harness；固定4ID精确替换、失败不遗忘目标，load清理自己的测试carrier，正常默认OFF。不是永久能力历史/六class自动consumer |
| M成功/进行中 | 尚无当前持久字段。未来累计与START Era额度属城市历史；进行中资格、reference、start turn/era、成功receipt必须独立，不复制旧动态X/cache或Claim UNASSIGNED合同 |
| N历史/任务/单位 | 尚无当前持久字段。完成报告留旧档案城市；已有考察单位属原Owner，sourceOwner loss中止无新报告并使旧归档失效，免费重挂靠own CultureIdentity、不要求高ACTIVE；新报告归新档案城市，不搬旧历史 |

ACTIVE下降不等于身份退出：未来N已有单位/任务可在归档城市ACTIVE/Identity下降或REALLOCATING时继续，只要Owner/binding有效；本城当前Tourism/Network另按各自gate。Owner loss有明确不同处理。M提交前的gate/中断取消与成功历史保留又是另一合同，不统一“永久资产全恢复”。

Gameplay768–781实际启动链、Meaning旧请求185–196、GWA retired入口及K轻量Summary已独立核关键分支。B166 normal世界旧GWA退休是一次有界精确退出，不是AI专业循环或每回合全世界清理。M计划中的旧“GWA全局cutover尚未完成”说明需由已完成B166资格化；未来只处理剩余旧Dialogue/本次新writer责任，不复活retired GWA。

## 证据、测试与反证

| 来源 | 真正证明 / 不能证明 |
|---|---|
| [B149结算](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md) | 原记录图1/2累计1316−1194=122证明所测稳定输入入账；变化后结算/冷重启为用户报告。不是所有C++事件结算时序或未测等X作品替换普遍PASS |
| [B165五图](../../Status/Validation/Results/Specialization_B165_Meaning_Native_Review.md) | 五yield当时值/退出与主题化×2有明确范围；132进度≠精确Production贡献归因，旧正Dialogue+0%不能证明正倍率隔离 |
| [B165正旧AUTO对照](../../Status/Validation/Results/Specialization_B165_Positive_Auto_Production_Native.md) | 所测Writing＋旧AUTO25%时追加五项保持原值，城市Production同回合+13与基础10及普通30%相容；不是新M永久倍率/全部作品或两段队列精确差值归因 |
| [B166人工PASS](../../Status/Validation/Results/Specialization_B166_Meaning_Automatic_User_Pass.md) | 正常七域五yield自动/currentD或W/ACTIVE与用户冷重启确认；无截图，不虚构读数，不扩大九域/全部作品/正Dialogue或精确nativeProduction结算 |
| [B168本地](../../Status/Validation/Results/Specialization_B168_Inspiration_Diagnostics_Local.md) | 39项定向native接口stub/末档退出/UNKNOWN/响应缓存等；部署MATCH不是小数、有效倍率或全国读数的本城归属nativePASS |

当前[InspirationReadout](../../../Mod/InspirationReadout.lua)56/65已将foreign Owner而Subject不可读记INCOMPLETE并保留候选，诊断无实例文案明确本玩家范围。定义≤32768、Subjects≤64、展示每类8/Subject2、标量192，只READ/END请求枚举并缓存一个token/reference/turn；每请求token更新，不应拿旧版本的未知Subject漏过滤或同token阶段缺键推导当前缺陷。GetObjectsPlayerId不能直接解出city，倍率来源不求和成有效倍率，原生接口不可读不阻塞owned退出。

Aesthetic carrier存在性有boolean断言，健康度IsPillaged则以==false判断；Meaning拥有更严格健康布尔校验。nil健康可能额外重配是静态保护差异，未观察native nil/成本，不单列高优先级缺陷。收紧须保持UNKNOWN HOLD和实际掠夺修复，不为理论点重测全生命周期。

未来M/N不是当前local测试缺失事故：本次未批准实现。它们确实引入新的永久record/单位归档/成功事务，届时应定域核load/owner/cancel，不能沿用未变probe默认OFF反复仪式，也不能拿Claim验证覆盖不同归属/奖励合同。

## 已有结构风险与后续边界

- IA-P13a-F04：K单callback包装顺序；更多文化consumer前先明确异常隔离/已确认样本通知。其actual反例和timing沿用[P09b](P09b_Propagation_Boundaries.md)，不重跑。
- IA-P13a-F02/F03及P08a：D/building事实重复采集、独立player scans、精确投影失败/readback协议差异；L1/L2使用面已核，不以减carrier检验破坏退出。
- IA-P06a-F01/F03：新M/N永久writer将扩大保存层每写全record唯一性检查和专业业务耦合；先澄清局部提交/业务纯模型边界，仍不实施。
- U2等count/X但组成变化可能需要新紧凑呈现通知；L3只W的变化通知现已补，不将旧缺口复制为新问题。外国N collector按活动任务定域，不能广播全世界或复用国内K为foreign authority。

实际读取：完整Culture D0048/CUL、K/L模型和writer及当前reader直接段；K/L/M/N/U2直接计划，B149/B165五图与正旧AUTO/B166/B167/B168相关具名结果和正式fixture/断言定向审阅。Shared/Network/Store/GW callback/perf/core事实按已核报告复用。未重看原截图、外部DB、真实runtime/receipt或全历史；本slice无新reproduction/native/玩法tests。

下一P04b/P11b：完整Commerce_D0045/Spec COM、Commerce准备与C1–C8计划→Convergence/Stock/Capital/旧consumer/当前合同状态。重点区别签约与尚未签约、长期信誉与hidden protection、ACTIVE/Identity/REALLOCATING/Owner的不同ownership，沿既有事务/Network证据扩读直接依赖，不自行补商业设计或实施。
