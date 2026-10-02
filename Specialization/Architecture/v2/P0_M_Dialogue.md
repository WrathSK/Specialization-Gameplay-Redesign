# P0-M —「时代对话」项目与持久倍率准备计划

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED / PERSISTENCE_AND_NATIVE_ONLY_GATES_OPEN。
Authority: Culture D0029 `CUL_L3_DIALOGUE`、`contracts.dialogue/work_pool`；Shared D0035；基线与顺序见[文化准备入口](Culture_Preparation.md)。

## 完整Gameplay合同

Culture ACTIVE≥3，通过同名项目连续占用一个完整城市生产回合。中断后需要重新连续一回合；高Production/overflow不能令正常项目瞬间完成，不能拿普通低成本项目近似。

每座城市×**启动时Game Era**最多成功一次，不按完成时代、不按Owner重置，不囤积过去未用机会。完成时取当前合格馆藏时代数X，增加`5×X`永久百分点；5为初版系数。X0允许成功且消耗机会。启动不锁馆藏，期间移动作品会改变完成时X。

累计按未来cap约束；cap当前null/BALANCE_REQUIRED，不代表0或已批准无上限。累计倍率和used START Era是**城市历史**，随城市转移保留，ACTIVE<3暂停当前效果但不丢历史；符合资格后恢复。新作品获得本城倍率，移走作品不带走倍率。

优先只提高合格巨作**原生产出（含旅游）**，不提高意义延展附加值。若只能可靠实现Tourism-only，正式Content允许报告并区分后采用该fallback，不能本计划默认为最终路径。百分比效果接受原生floor、无补偿；即使整数收益没变，UI仍显示累计百分比。这项许可不适用于L2/L3小数。

## 已验项目路线可以复用什么

真实高成本项目→正常结束生产回合→下一次本地回合阶段调用`FinishProgress`→原生completion确认，是已验原型。后续`ClaimProjects`还提供每城persisted timer、开始前/完成前城市引用验证、CALLING先落盘以防重入、cold-load续接/1T显示等实现结构。它不要求空生产队列，也不需要处理其它回合blocker或Shift+Enter绕过。

旧empty-queue、负AddProgress清overflow等失败路线不重新打开。已有项目接口的测试只按[B123所测范围](../../Status/Validation/Results/Specialization_B123_Project_Pass.md)及[Claim核心结果](../../Status/Validation/Results/Specialization_B126_Claim_Core_Pass.md)复用；不宣称全部Production injection、队列顺序或Dialogue业务已通过。

`TimedProject`仍是session单城实验；`ClaimProjects`有正式持久续接，但其UNASSIGNED资格、Claim receipt与失城时清claimTimer都是Claim业务。**不能直接把Dialogue写成Claim项目，或复制Claim清空语义来决定文化历史。** 用户为高成本项目原型接受了奇特方式强制同回合完成不做额外保护、原生completion用于发奖的测试便利；保留其真实适用范围，不另加防Cheat体系。新Dialogue的同回合强制completion与quota/reward边界在实施前对照该接受记录及完整生产回合合同核对；本计划不把强制completion当成已证明完整生产周期，也不自行覆盖既有用户例外。

## 业务保存与读模型

建议在现有可靠E2 city record增加小型Dialogue专业块，分别保存：城市累计百分点、已成功START Era集合、当次项目身份/当前引用、启动回合与Game Era、连续占用/已完成调用阶段、唯一completion凭据。字段在实施时按直接合同确定，不新建cityKey/通用Contract对象。

- **城市owned历史：** cumulative＋used era＋completion dedup，不按原Owner分割；不得从旧动态25%载体推导累计或给旧值迁移奖励。
- **当次计时：** 属于本次项目操作，不是永久倍率；切换生产中断，旧项目进度/旧timer不得在下次开始补算连续时间。load只恢复可靠保存事务，不能因打开列表才“开始”。
- **派生effect：** 当前资格＋可靠ledger＋native-only路径。载体、Tooltip、UI选择状态不能单独发奖或保存次数。
- 发奖前验证current owner/ref、完整周期和completion证据、未用START Era、完成时confirmed X。一次保存累计＋quota＋凭据，先确认永久写入再派生modifier；重复事件/load不重奖。
- Completion阶段若馆藏UNKNOWN，不猜X0，不消耗机会；保留可证明的待结算事务。必须取得能归属于**完成边界**的confirmed X/版本，不可等待到后续馆藏变化后用新的当前X替代；若不能可靠证明该时点，停止该结算路径并记录TECHNICAL_INVESTIGATION_REQUIRED。不能无界重试、超时当成功或将重载变第二次项目。
- 损坏/缺失历史显式HOLD，不用当前馆藏或旧carrier“重建完整历史”。在现有Store专属validate/read/write中维护，不用独立本机文件保存。

## 必须在对应切片处理的边界

cap值/策略是Balance gate：不阻塞纯计时、配额模型及技术probe；正式累计奖励需要明确参数，不将null写0或自行无cap。

正式合同明确ACTIVE下降暂停已有收益、城市倍率/quota易主保留，但**未明确执行中的未结算项目在ACTIVE下降或confirmed owner-loss后如何处理**。计划保留为执行中生命周期待核对项：能证明的历史和事务保留，AI不继续运行/发奖，不能把“暂停已有倍率”自行解释成“项目继续且成功”，也不借Claim清timer决定它。实施该路径前提具体DESIGN_DECISION_REQUIRED；该局部问题不阻塞L1/L2/L3或计时/存盘probe。

城市记录跟城的持久scope与原主人见闻不同；E2已有可靠同城映射可复用，不能靠名字/单独坐标/猜CityID。当前v0.1仅本地人类运行，AI owner全部效果休眠；不要求新增AI投资或城市建筑监听。

## 建议小切片与精确退休

| 切片 | Goal / 依赖 | 不包含 | Exit |
|---|---|---|---|
| M计时/ledger门禁 | 复用真实项目、可靠city mapping；START Era quota、完成X和dedup先用fixture/影子；处理上述执行中边界 | 正式新倍率、旧Dialogue退休、所有Production来源全追踪 | 开始/中断/下一回合/cold-load、多城、重复及保存错误明确 |
| M native-only门禁 | 核对所有原生作品yield路径、支持类型过滤，联用L2追加值作隔离 | 自动採用Tourism-only/改L2语义 | 原生作品增幅、追加不被放大、当前城市限定被证实 |
| M正式cutover | 以上通过、cap/执行中规则足够明确，正常资格读模型 | 考察见闻/Network/其它专业Legacy | 业务本地通过＋一次最小原生；停于M |

每切片实施前单独固定范围/授权，不一次部署三个未知变量。可以合用现有文件职责，但禁止把旧单城实验当完整永久系统。

cutover只清旧Dialogue的动态D档、TEST25/50/100及其保留的旧B055测试owned列表，核对实际SQL附件/Start/load/manual/ACK路径；不前缀清建筑。新ledger不由它们初始化；旧writer确认撤销后启新倍率。

**K仍依赖DIALOGUE_SAMPLE和共享后台槽位collector。** 将旧收益writer与采样/ACK分离，保留确认事实与有界pending；旧`Dialogue.Receive`转兼容传输职责或明确最小替代，不简单停Start使ACK重试积压。不复活已退休GWA，不动L1/L3或旧Culture Eureka。

预计涉及`ClaimProjects/TimedProject`可复用小接口、专属Dialogue model/Store专业块/consumer/SQL，选择确认与项目1T UI，Gameplay/modinfo、诊断、本地测试。真正共享改动须核对Claim直接调用点并做其回归，不创建通用项目引擎。

## 事件、性能和回滚

普通采集只取X/validity/引用，作品明细仅按需。待计时项目维护有界active集合，玩家回合阶段只处理这些事务；没有计时则不扫描每城项目，不按每帧/hover启动/发奖。项目选择是意图，Gameplay确认队列后才开始；UI display从confirmed timer读取。

Production changed/completed、目标切换、城市生命周期、load、quota/累计写入分别声明原因；顺序转换不能被收益去重合并。原生completion可能重入：持久CALLING先写，不能异常后再次无条件FinishProgress。未知引用HOLD，confirmed loss先退出owned effect，历史保留。

回滚需检查本批新增专业块schema是否被旧包认识；能保留惰性新记录则保留，不删永久历史来回退。若旧包不能安全读取则使用实施前存档副本＋对应Git/receipt恢复点，明确不兼容边界；不承诺任意旧版本互读。

## 最小验证与门禁

W0004 L3，但仅相关项目/Store/重复/保存及native-only回归，不默认全历史stress。

本地矩阵：跨START/完成Era、同城第二次拒绝、X0/X变化、低/高Production、overflow/chop/native强制完成区别、切走再回、多个并行城市、duplicate/reentrant/存盘失败、cold load、UNKNOWN完成样本、owner/ACTIVE变化、旧writer退出及Claim不回归。执行中未决路径不能靠测试fixture“选择一种规则”。

一次最小原生：同一高生产馆藏城开始→移作品使完成X不同→正常一回合完成→同启动时代不能再成功→冷加载记录和1T续接。追加收益隔离用同城L2对照；ownership quota仅在实施覆盖该路径时补最小流程，既有E2 PASS不能替代新增文化块验证。不是现在要求用户跑。

诊断显示启动时代/已用、计时状态、当前X/待确认、累计%/cap待定、优先/技术fallback、native实测范围。不要堆Property/令牌；异常再展开。Exit不将计时probe成功或旧百分比实测升级为完整M。

来源：[正式Culture](../../Design/Content/Culture_D0029.json)、[项目调查](../../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md)、[既有E2保存合同](P0_E2_Plan.md#current-slice--recovery-and-action-routing)、[旧百分比实现](../../Reports/Technical/Specialization_B059_Dialogue_Implementation.md)、[特定native/theming结果](../../Status/Validation/Results/Specialization_B059_82_Percent_User_Result.md)。
