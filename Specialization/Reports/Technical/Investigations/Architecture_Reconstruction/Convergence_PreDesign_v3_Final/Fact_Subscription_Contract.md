# Fact & Subscription Contract：v3-final精确后继

调查材料／后继候选；不覆盖正式规范。

Status: Stable（可审阅的候选文档，不是工程或实机 PASS）。

维护者：Primary｜日期：2026-11-03｜实际 develop：`719eb61b410765fb6e8703a47840ce3cec3fa823`。正式记录仍为 D0058／A0183／S0866；B399.426 仅为既有部署记录，本轮未重新验包。

**NO IMPLEMENTATION AUTHORIZATION。** 本主题承接原 H3 中文交付；仅新增候选 Markdown，原 v3 九文件及代码／测试／工具／正式规范／治理／运行包均不改。

## 继承与阶段

原v3第1、2、4、5、7节（事实正常/异常、统一ACTIVE、R2ACK、R3声明、生产/诊断隔离）继续有效为**候选目标**，见[原 v3 Fact_Subscription_Contract.md:12](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L12)。本文件替代原第3节中ODP01占位、第6节受影响F行及信誉例外；不是当前正式规则的即刻修改。未明确批准的F02/F03等格子不借本轮批量放行。

**T0：现行／Pre-U5。** 现行D1／冷例外A保持原合同，PU03不偷渡本文件cold行为。
**T1：后续获批O3 cutover。** FS03/04先按批准流程同步后，采用下面B目标矩阵；D1直到其退出门禁完整通过才撤。正常网络通知与严重异常通知分离，不把partial包装成普通READY。

## NET：证据对象与界限

- `K`：当前能独立证明receiver、source、ref/episode、路径／membership、资格和所需输入合法的贡献。确认的负事实先排除来源；仅“没有新失效通知”不自动证明当前交易资格。
- `W`：本Gameplay会话内确实确认过、同一有效owner/city/ref/source的来源贡献；每合法来源一个有界见证。仅在严重读取错误、未确认失效的窄条件下保留。生命周期/引用/角色退出清掉相关见证，不跨加载，不从O重建，不默认写Property。
- `O`：真实已安装、可读回的own输出；只证明实际应用，不证明来源、拓扑、历史或交易资格。
- `FULL_UNKNOWN` 与 `APPLIED_PARTIAL` 分别描述完整结果无法确认、实际仅由已证部分支持；不把未知源记录为0/空集合。K为空可有actual空，但不是FULL已确认0。
- 预算按现有受审工作集／容量／生命周期设界；越界显式报告，不静默截断合法来源。无进展重复通知不得增重试预算；恢复仅凭相关事实／可用性／生命周期／必要初始化新证据，不用TTL／定时器／逐回合全城扫。

## NET01–NET06：精确输出与恢复

**分支优先级：** 单纯冷启动、没有W、首次证明／初始化尚未完成，本身不是严重故障，仍走NET01；不能仅凭cold或缺见证触发NET03/04。只有已核实阶段／接口合同表明出现严重读取错误或无法可靠重建时，才进入NET03/04。确认负事实NET05独立优先。按真实原因及就绪证据分类，不靠经过时间、重试次数或一次pcall失败证明永久损坏；无法分类须报错并保具体权限边界，不能长期假称正常loading。

| 场景 | 允许的输出／操作 | 必须保留的证据与恢复 |
|---|---|---|
| NET01 正常短暂拓扑未准备 | dirty立即使strict proof失效并登记shared责任；不发UNKNOWN正常正向更新；T0按现行D1保O。目标新链在相关可靠阶段完成采集，既有applied不会因尚无新可靠计划被清零 | 确认空网独立；同值可用性恢复也交付；正常不能依赖长期hold或publish轮询结项 |
| NET02 拓扑可靠、单来源严重错误且有W | 当前可靠负事实先剔除W；仍满足有效同ref边界的W可与新K按原业务公式合并，标RETAINED_SOURCE_ERROR，不能称全部新鲜 | 生产owner限量严重错误／原因、source见证与待办；成功sibling不被失败者反复深读；只凭新相关证据恢复 |
| NET03 cold无W，有K | 不拆O；仅投影由K支持的部分。未知来源无值，FULL_UNKNOWN；实际成功才标APPLIED_PARTIAL。适用于有或无已确认来源负事实、但旧残差不可安全解释的严重故障 | 不把K-only视图当完整网络或新交易证明；事实补齐后重新计算，不重放旧聚合／旧账。receiver或current输入也未知时不能勉强造K |
| NET04 cold无W，K为空 | 若receiver/ref/资格及exact-owned家族可可靠确认，撤除该受影响家族的不具见证输出，标actual空＋FULL_UNKNOWN；其它可独立确定的ability/family/target不动。若receiver/权限/presence无法确认，停止该写入并保留真实残留/UNKNOWN | 严重错误不因画面归零关闭；不发布来源已确认0，不建首值、不改真历史。恢复由新可靠证据重建 |
| NET05 确认来源/路线或receiver退出 | 先撤相关membership/W。源退出：按剩余K/合法W重算受影响物理结果，不能借O不可拆继续支付已失效残差；保住独立已知self/siblings。receiver/owner/ref退出按现有精确授权清本owner效果 | 若当前端点不再授权（如旧loss.target已夺回），不跨新ref猜清；按合法Store/lifecycle路径保留错误责任。不能网络失败掩盖已确认退出 |
| NET06 写入／读回失败 | 计划不是APPLIED；记录实际可读结果或UNKNOWN。必要旧效果撤除未确认，不施加依赖该撤除的新正效果。不得假原子回滚或机械写0 | effectowner保存输入见证与outcome区别，相关新证据后读回并差异核对。钱/单位结果仍按独立收据no-replay，不因被动重算重复交易 |

NET03/04是Owner B“隔离不可安全解释部分、保护可独立确定合法其他来源”的精确化，不是把所有未知来源认定无收益。例：旧max20，A已退出，B不可读，self10可靠。应用10明确是partial；B可能真为20，也可能10，本轮不承诺继续无证支付。B恢复20再重算20。若未来要求连这种无法独立证明的潜在贡献也绝不能临时减少，那才需新的Owner取舍，不能暗加该要求。

### 三类物理编码各自处理，不造通用公式

| 家族／粒度 | K如何形成／保留哪些原语义 | 当前差异源码 |
|---|---|---|
| Commerce：每domain候选→单一总Gold编码 | 已确认配置、容量、D、合法X及R（含窄政策R0）后，每domain取合法source最大X；`D*X*(200+R)/4000`逐domain Floor再sum。无已证source的domain完整值UNKNOWN，不能给Finish假sourceX0；已证domain继续，受影响总Gold按其和投影。不能从旧Gold反拆domain | [Mod/Commerce.lua:240](../../../../../../Mod/Commerce.lua#L240)；[Mod/Commerce.lua:281](../../../../../../Mod/Commerce.lua#L281)；[Mod/CommerceCalculation.lua:31](../../../../../../Mod/CommerceCalculation.lua#L31) |
| CultureNetwork：recipient anchor family | K由真实Insights可靠产生的完整文明集合构成，先set union再去重count，不能加来源count。未知源无集合值，不是已证empty；cold旧n不构造文明身份。receiver沿既有identity/anchor，不加统一ACTIVE门槛 | [Mod/CultureNetwork.lua:110](../../../../../../Mod/CultureNetwork.lua#L110)、[Mod/CultureNetwork.lua:137](../../../../../../Mod/CultureNetwork.lua#L137)、[Mod/CultureNetwork.lua:298](../../../../../../Mod/CultureNetwork.lua#L298) |
| Standardization：每target最终值 | self和remote来源逻辑分开，仍每target max；模板/L为真历史。用K/有效W计算该target；某target异常不阻断独立已证target。保留单物理最终carrier，不把两份全额相加、不为形式统一强拆 | [Mod/StandardizationEffects.lua:111](../../../../../../Mod/StandardizationEffects.lua#L111)、[Mod/StandardizationEffects.lua:165](../../../../../../Mod/StandardizationEffects.lua#L165)、[Mod/StandardizationEffects.lua:227](../../../../../../Mod/StandardizationEffects.lua#L227) |

以上当前有效公式均对合法非负输入具单调性，因此K-only可作为已证应用下界；这不授权未来任意负数／非单调业务复用同规则。未来若native承载不等价，先停依赖切片，不能调整rounding/max掩盖。

### 旧冷例外与持久化职责

[Specialization/Design/Network.md:57](../../../../../Design/Network.md#L57)及[Specialization/Architecture/Specialization_v0.1_Architecture.md:145](../../../../../Architecture/Specialization_v0.1_Architecture.md#L145)现行明确允许Standardization暂留失效来源残差。**FS04后继拟撤离这项旧许可**，采用NET03–05；不是声称旧文本已经如此。D1迁移保留与该目标cutover分阶段，不能在当前程序里直接改。

[Mod/NetworkRecoveryStore.lua:15](../../../../../../Mod/NetworkRecoveryStore.lua#L15)的派生保存适配器不为完成原S9自动接线。未找到当前生产Open消费者不等于所有历史／手工／实验档不存在技术Property；保留旧decoder/opaque证据和必要SQL IDs至相容性门禁，不批量删存档数据。真实Insights、工程模板/L、延迟合法lifecycle见证、合同／单位收据保持既有权威。

## R0：窄例外接口／报价／合同

| 来源 | 候选接口含义 | 业务后果 |
|---|---|---|
| R_CONFIRMED | 历史、引用／版本可靠，正常有效R | 原公式；真实0与错误不同 |
| R_NOT_APPLICABLE | 正常资格门槛使R无加成（如有效ACTIVE III）；并非历史错误证明 | 有效0，不能因此新增R门槛；实际若历史错误仍另报，不能用此标签掩盖 |
| R_POLICY_ZERO | 只有独立信誉叶子不可可靠读取，parent/owner/city/ref/token/Commerce配置及按本次用途实际必需的其它输入可靠；新交易另须全部适用报价/余额/合同及相关native结果/收据可靠 | 严重错误、历史仍UNKNOWN，临时有效0；所有真实R依赖计算统一：商业化加成和新VENTURE失败退款 |
| R_UNSAFE | parent/身份/配置或其它必需事实不可靠、未证明仅叶子可分离，或相关原生结果未决 | 不得以`or 0`获得授权；相关不可逆路径拒绝，无盲重放 |

被动商业化不因R0新增Treasury／资本合同或其它无关交易门槛；实际发生的历史错误仍严重报出。生产结果必须携带历史可靠性、有效值来源、相关ref/版本、有限严重错误定位；字段拼写由Primary决定，不新建持久通用事件日志。错误不能只存在可选trace。

- 新VENTURE确认复核数值**及来源见证**。真实R0→政策R0即使数字相同也要使旧来源报价失效并重新确认；未付款前拒旧报价，不重复扣款。锁定合同保存当时有效R及政策来源和terms，`failure=principal*(0.5+0.005R)`，政策R0即本金50%。历史恢复不追改已签条款。
- STABLE payout=`safe`，不依赖R；共享风险预览／quote结构不变成其业务资格。其它输入仍严格；可不显示无法确认的无关风险预览，不能为展示强造历史或放行VENTURE。
- 旧合同没有新来源字段时沿旧锁定条款结算，标明LEGACY未记来源；不补造“当时信誉可靠”或“当时政策R0”。向后可读和旧版本安全运行须在相容门禁证明，不能仅切旧代码假称存档回退安全。
- 当前仅有数值R：[Mod/CapitalInvestment.lua:182](../../../../../../Mod/CapitalInvestment.lua#L182)、[Mod/CapitalInvestmentModel.lua:144](../../../../../../Mod/CapitalInvestmentModel.lua#L144)、[Mod/CapitalInvestment.lua:343](../../../../../../Mod/CapitalInvestment.lua#L343)。这些数值流已有，不是本轮重写全部资本投资；待补的是严重错误／可信来源／窄例外边界和锁定证据。
- 不可逆路径上所有相关未决原生结果（包括可能的CREDIT_CALLING，不仅旧guard三stage）均不被豁免；未证其当前可达漏洞，只规定目标严格边界。结算[Mod/CapitalInvestment.lua:235](../../../../../../Mod/CapitalInvestment.lua#L235)继续用原合同和native读回／receipt。

## F01–F60逐项核对（没有默认全表放行）

未变行保留原v3用途／批准和工程状态；当前源字节相同已核对。修订行精确替代旧ODP占位，均保留ENGINEERING_EVIDENCE_OPEN／FORMAL_SYNC_PENDING，不写工程PASS。

| F | 本轮处理／状态 | 原用途与当前源码 |
|---|---|---|
| F01 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:60](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L60)；[Mod/ResearchSupport.lua:9](../../../../../../Mod/ResearchSupport.lua#L9) |
| F02 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:61](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L61)；[Mod/IndustrySupport.lua:80](../../../../../../Mod/IndustrySupport.lua#L80) |
| F03 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:62](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L62)；[Mod/Lv2Housing.lua:20](../../../../../../Mod/Lv2Housing.lua#L20) |
| F04 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:63](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L63)；[Mod/Lv2GPP.lua:43](../../../../../../Mod/Lv2GPP.lua#L43) |
| F05 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:64](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L64)；[Mod/EffectiveFacts.lua:114](../../../../../../Mod/EffectiveFacts.lua#L114) |
| F06 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:65](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L65)；[Mod/ResearchApply.lua:26](../../../../../../Mod/ResearchApply.lua#L26) |
| F07 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:66](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L66)；[Mod/ResearchApply.lua:72](../../../../../../Mod/ResearchApply.lua#L72) |
| F08 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:67](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L67)；[Mod/ResearchCross.lua:4](../../../../../../Mod/ResearchCross.lua#L4) |
| F09 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:68](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L68)；[Mod/ResearchCrossSample.lua:20](../../../../../../Mod/ResearchCrossSample.lua#L20) |
| F10 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:69](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L69)；[Mod/ResearchCross.lua:46](../../../../../../Mod/ResearchCross.lua#L46) |
| F11 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:70](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L70)；[Mod/ResearchInfrastructure.lua:31](../../../../../../Mod/ResearchInfrastructure.lua#L31) |
| F12 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:71](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L71)；[Mod/ResearchInfrastructure.lua:31](../../../../../../Mod/ResearchInfrastructure.lua#L31) |
| F13 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:72](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L72)；[Mod/ResearchChair.lua:34](../../../../../../Mod/ResearchChair.lua#L34) |
| F14 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:73](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L73)；[Mod/ResearchChair.lua:34](../../../../../../Mod/ResearchChair.lua#L34) |
| F15 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:74](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L74)；[Mod/ResearchTraditionEffects.lua:68](../../../../../../Mod/ResearchTraditionEffects.lua#L68) |
| F16 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:75](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L75)；[Mod/CityProgressionStore.lua:1061](../../../../../../Mod/CityProgressionStore.lua#L1061) |
| F17 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:76](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L76)；[Mod/EffectiveFacts.lua:210](../../../../../../Mod/EffectiveFacts.lua#L210) |
| F18 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:77](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L77)；[Mod/GreatWorkFacts.lua:177](../../../../../../Mod/GreatWorkFacts.lua#L177) |
| F19 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:78](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L78)；[Mod/CultureAesthetic.lua:126](../../../../../../Mod/CultureAesthetic.lua#L126) |
| F20 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:79](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L79)；[Mod/CultureMeaning.lua:62](../../../../../../Mod/CultureMeaning.lua#L62) |
| F21 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:80](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L80)；[Mod/CultureMeaningModel.lua:37](../../../../../../Mod/CultureMeaningModel.lua#L37) |
| F22 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:81](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L81)；[Mod/CultureInspiration.lua:54](../../../../../../Mod/CultureInspiration.lua#L54) |
| F23 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:82](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L82)；[Mod/DialogueEffects.lua:12](../../../../../../Mod/DialogueEffects.lua#L12) |
| F24 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:83](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L83)；[Mod/DialogueEffects.lua:243](../../../../../../Mod/DialogueEffects.lua#L243) |
| F25 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:84](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L84)；[Mod/DialogueProjects.lua:1](../../../../../../Mod/DialogueProjects.lua#L1) |
| F26 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:85](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L85)；[Mod/ExpeditionSpyGate.lua:1](../../../../../../Mod/ExpeditionSpyGate.lua#L1) |
| F27 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:86](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L86)；[Mod/CultureInsightsTourism.lua:57](../../../../../../Mod/CultureInsightsTourism.lua#L57) |
| F28 | B：正常完整拓扑可靠后发布；dirty立即失效严格凭据；D1仅迁移保护，NET矩阵生效需正式cutover | [原 v3 Fact_Subscription_Contract.md:87](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L87)；[Mod/NetworkBridge.lua:103](../../../../../../Mod/NetworkBridge.lua#L103) |
| F29 | B：Insights真历史不动；warm完整文明集见证可有限保留；cold旧n不拆集合，未知源不记空集；只投影已证并集 | [原 v3 Fact_Subscription_Contract.md:88](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L88)；[Mod/CultureNetwork.lua:137](../../../../../../Mod/CultureNetwork.lua#L137) |
| F30 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:89](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L89)；[Mod/CultureNetwork.lua:110](../../../../../../Mod/CultureNetwork.lua#L110) |
| F31 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:90](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L90)；[Mod/EffectiveFacts.lua:114](../../../../../../Mod/EffectiveFacts.lua#L114) |
| F32 | B：self／remote逻辑独立、per-target max；cold受影响聚合按NET规则隔离未知残差，可靠self不长期等无关网络 | [原 v3 Fact_Subscription_Contract.md:91](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L91)；[Mod/StandardizationEffects.lua:165](../../../../../../Mod/StandardizationEffects.lua#L165) |
| F33 | B：模板／L严格历史保留；上次应用的来源分解不是永久历史，不默认接保存适配器 | [原 v3 Fact_Subscription_Contract.md:92](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L92)；[Mod/StandardizationEffects.lua:111](../../../../../../Mod/StandardizationEffects.lua#L111) |
| F34 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:93](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L93)；[Mod/IndustryWonderEffects.lua:30](../../../../../../Mod/IndustryWonderEffects.lua#L30) |
| F35 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:94](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L94)；[Mod/IndustryHistory.lua:180](../../../../../../Mod/IndustryHistory.lua#L180) |
| F36 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:95](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L95)；[Mod/EngineeringStudyProjects.lua:129](../../../../../../Mod/EngineeringStudyProjects.lua#L129) |
| F37 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:96](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L96)；[Mod/CrewProjects.lua:265](../../../../../../Mod/CrewProjects.lua#L265) |
| F38 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:97](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L97)；[Mod/UnitActions.lua:63](../../../../../../Mod/UnitActions.lua#L63) |
| F39 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:98](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L98)；[Mod/EffectiveFacts.lua:114](../../../../../../Mod/EffectiveFacts.lua#L114) |
| F40 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:99](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L99)；[Mod/Commerce.lua:123](../../../../../../Mod/Commerce.lua#L123) |
| F41 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:100](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L100)；[Mod/CityProgressionStore.lua:521](../../../../../../Mod/CityProgressionStore.lua#L521) |
| F42 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:101](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L101)；[Mod/Commerce.lua:123](../../../../../../Mod/Commerce.lua#L123) |
| F43 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:102](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L102)；[Mod/Commerce.lua:323](../../../../../../Mod/Commerce.lua#L323) |
| F44 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:103](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L103)；[Mod/Commerce.lua:249](../../../../../../Mod/Commerce.lua#L249) |
| F45 | B：合法当前X重建；warm同ref见证有限保留；cold旧总Gold不拆domain、不造X0，按已证max/Floor/sum投影 | [原 v3 Fact_Subscription_Contract.md:104](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L104)；[Mod/Commerce.lua:240](../../../../../../Mod/Commerce.lua#L240) |
| F46 | B：正常pending只由shared负责；D1保留／禁用／真删除验证前不删，不用旧效果授权新交易 | [原 v3 Fact_Subscription_Contract.md:105](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L105)；[Mod/NetworkBridge.lua:103](../../../../../../Mod/NetworkBridge.lua#L103) |
| F47 | A：仅信誉叶子异常时统一政策R0；严重错误／原字节保留；其它合法商业化收益不取消 | [原 v3 Fact_Subscription_Contract.md:106](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L106)；[Mod/Commerce.lua:148](../../../../../../Mod/Commerce.lua#L148) |
| F48 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:107](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L107)；[Mod/Commerce.lua:89](../../../../../../Mod/Commerce.lua#L89) |
| F49 | A：新VENTURE可锁政策R0，失败退款本金50%；报价与确认比来源见证，历史恢复不追改 | [原 v3 Fact_Subscription_Contract.md:108](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L108)；[Mod/CapitalInvestmentModel.lua:144](../../../../../../Mod/CapitalInvestmentModel.lua#L144) |
| F50 | A：STABLE数学无R依赖；不能因风险预览或共享结构新增R门槛；其它必需事实仍可靠 | [原 v3 Fact_Subscription_Contract.md:109](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L109)；[Mod/CapitalInvestmentModel.lua:175](../../../../../../Mod/CapitalInvestmentModel.lua#L175) |
| F51 | A：保存的合同条款／due／native结果／receipt结算，不用恢复后的R重价；旧合同不补造来源历史 | [原 v3 Fact_Subscription_Contract.md:110](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L110)；[Mod/CapitalInvestment.lua:235](../../../../../../Mod/CapitalInvestment.lua#L235) |
| F52 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:111](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L111)；[Mod/DevelopmentInvestment.lua:26](../../../../../../Mod/DevelopmentInvestment.lua#L26) |
| F53 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:112](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L112)；[Mod/DevelopmentInvestment.lua:1](../../../../../../Mod/DevelopmentInvestment.lua#L1) |
| F54 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:113](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L113)；[Mod/RestructuringUI.lua:38](../../../../../../Mod/RestructuringUI.lua#L38) |
| F55 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:114](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L114)；[Mod/ClaimProjects.lua:111](../../../../../../Mod/ClaimProjects.lua#L111) |
| F56 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:115](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L115)；[Mod/InstitutionPresentation.lua:59](../../../../../../Mod/InstitutionPresentation.lua#L59) |
| F57 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:116](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L116)；[Mod/UI/LevelBannerModel.lua:5](../../../../../../Mod/UI/LevelBannerModel.lua#L5) |
| F58 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:117](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L117)；[Mod/UI/InstitutionOverview.lua:25](../../../../../../Mod/UI/InstitutionOverview.lua#L25) |
| F59 | 继承原行；批准／未批准格子及工程开放状态不变 | [原 v3 Fact_Subscription_Contract.md:118](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L118)；[Mod/Probe.lua:553](../../../../../../Mod/Probe.lua#L553) |
| F60 | A：仅信誉叶子是已批业务例外；network partial、parent／余额／未决native／receipt未知均不被豁免 | [原 v3 Fact_Subscription_Contract.md:119](../Convergence_PreDesign_v3/Fact_Subscription_Contract.md#L119)；[Mod/NetworkBridge.lua:20](../../../../../../Mod/NetworkBridge.lua#L20) |

## 共用硬门禁

R2：中央搬运／attempt不是专业ACK；真正登记pending或同步证明无动作后才ACK，旧revision不吞新变化。R3：四专业成功Start后声明，共享能力只一次；RestructuringSync→NetworkBridge phase0、EmitDerived特许窗口、sealed后首次drain保持。生产writebarrier／Flight／GCowner先提取，可选observer不承载责任；disable与file/global真实absence均须差分。原v3具体条款继承，不新增插件发现、定时器或中央业务表。
