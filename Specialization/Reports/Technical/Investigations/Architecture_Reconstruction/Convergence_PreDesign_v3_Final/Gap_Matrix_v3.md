# Gap Matrix：v3-final逐项核对

调查材料／后继候选；不覆盖正式规范。

Status: Stable（可审阅的候选文档，不是工程或实机 PASS）。

维护者：Primary｜日期：2026-11-03｜实际 develop：`719eb61b410765fb6e8703a47840ce3cec3fa823`。正式记录仍为 D0058／A0183／S0866；B399.426 仅为既有部署记录，本轮未重新验包。

**NO IMPLEMENTATION AUTHORIZATION。** 本主题承接原 H3 中文交付；仅新增候选 Markdown，原 v3 九文件及代码／测试／工具／正式规范／治理／运行包均不改。

## 核对方式与基线差异

原九份v3保持冻结。本轮不是重做全仓审计：重新核对HEAD/正式版本、生产字节差异和受影响calls；未变条目继承原限定证据，通过原行和当前源码定位追溯。9addf8d→719eb61只新增13报告，故未变源码分析未因字节变化失效；新B/A取代的是候选目标占位，不是代码修复。

`STATIC`=当前源码／正式合同；`LOCAL_EXISTING`和`USER_NATIVE_EXISTING`只指原已记录具名范围、未本轮重跑；`UNVERIFIED`=拟接口／原生未知。以下所有新迁移／实验门禁均未执行。链接行存在不是语义／原生正确性PASS。

## G01–G30

| G | 本轮裁定／继承 | 当前责任／依赖 | 可核查证据 |
|---|---|---|---|
| G01 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O3依赖基线；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:24](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L24)；[Mod/NetworkSender.lua:32](../../../../../../Mod/NetworkSender.lua#L32) |
| G02 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O3；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:25](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L25)；[Mod/NetworkSender.lua:58](../../../../../../Mod/NetworkSender.lua#L58) |
| G03 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU01/O1；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:26](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L26)；[Mod/Commerce.lua:323](../../../../../../Mod/Commerce.lua#L323) |
| G04 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU04/O1；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:27](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L27)；[Mod/ResearchInfrastructure.lua:31](../../../../../../Mod/ResearchInfrastructure.lua#L31) |
| G05 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O1；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:28](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L28)；[Mod/ResearchApply.lua:26](../../../../../../Mod/ResearchApply.lua#L26) |
| G06 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU10/O1；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:29](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L29)；[Mod/Probe.lua:325](../../../../../../Mod/Probe.lua#L325) |
| G07 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O2；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:30](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L30)；[Mod/FactChanges.lua:182](../../../../../../Mod/FactChanges.lua#L182) |
| G08 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU03/O2；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:31](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L31)；[Mod/NetworkBridge.lua:133](../../../../../../Mod/NetworkBridge.lua#L133) |
| G09 | B已选：不接cold派生存储凑S9完成；NET01–06 current重建／warm见证／cold partial及负事实；工程开放 | O3；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:32](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L32)；[Mod/StandardizationEffects.lua:191](../../../../../../Mod/StandardizationEffects.lua#L191) |
| G10 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:33](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L33)；[Mod/StoreSubrecords.lua:100](../../../../../../Mod/StoreSubrecords.lua#L100) |
| G11 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU07/O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:34](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L34)；[Mod/CityProgressionStore.lua:823](../../../../../../Mod/CityProgressionStore.lua#L823) |
| G12 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:35](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L35)；[Mod/IndustryHistory.lua:180](../../../../../../Mod/IndustryHistory.lua#L180) |
| G13 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU09/O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:36](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L36)；[Mod/ClaimProjects.lua:144](../../../../../../Mod/ClaimProjects.lua#L144) |
| G14 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU05；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:37](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L37)；[Mod/CrewProjects.lua:265](../../../../../../Mod/CrewProjects.lua#L265) |
| G15 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O6；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:38](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L38)；[Mod/InstitutionPresentation.lua:59](../../../../../../Mod/InstitutionPresentation.lua#L59) |
| G16 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:39](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L39)；[Mod/CityProgressionStore.lua:1061](../../../../../../Mod/CityProgressionStore.lua#L1061) |
| G17 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O1/O5；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:40](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L40)；[Mod/RestructuringModel.lua:79](../../../../../../Mod/RestructuringModel.lua#L79) |
| G18 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O5；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:41](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L41)；[Mod/FactConsumerBindings.lua:19](../../../../../../Mod/FactConsumerBindings.lua#L19) |
| G19 | 默认严格不可逆不变，新增唯一信誉叶子A例外；其它UNKNOWN、partial network、ACK、旧效果均不授权新交易 | 全包；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:42](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L42)；[Mod/CapitalInvestment.lua:337](../../../../../../Mod/CapitalInvestment.lua#L337) |
| G20 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O2/O5/O7；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:43](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L43)；[Mod/ClaimProjects.lua:111](../../../../../../Mod/ClaimProjects.lua#L111) |
| G21 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O8；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:44](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L44)；[Mod/DistrictCompleteness.lua:182](../../../../../../Mod/DistrictCompleteness.lua#L182) |
| G22 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O7；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:45](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L45)；[Mod/Dialogue.lua:298](../../../../../../Mod/Dialogue.lua#L298) |
| G23 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | O7；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:46](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L46)；[tools/deploy.py:35](../../../../../../tools/deploy.py#L35) |
| G24 | FS03/04=B、FS06=A替代旧分支；现行D/A保持原件，审计Finding闭环＋Owner再次授权后才successor/freeze | 正式同步门禁；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:47](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L47)；[Specialization/Design/Network.md:47](../../../../../Design/Network.md#L47) |
| G25 | 数量不是活动实例／性能证据；只精准引用Carrier生产依赖，不合并优化；无新性能量化 | O8/PU11；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:48](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L48)；[Mod/PerformanceCounters.lua:155](../../../../../../Mod/PerformanceCounters.lua#L155) |
| G26 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU02；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:49](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L49)；[Mod/RestructuringUI.lua:38](../../../../../../Mod/RestructuringUI.lua#L38) |
| G27 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | 本计划边界；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:50](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L50)；[Specialization/Status/Specialization_P0_Status.md:14](../../../../../Status/Specialization_P0_Status.md#L14) |
| G28 | 原候选根因／未证边界／停止条件不变；不追加玩法或伪造关闭 | PU08/O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:51](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L51)；[Mod/CityProgressionStore.lua:1175](../../../../../../Mod/CityProgressionStore.lua#L1175) |
| G29 | A政策已获Owner批准，尚未实施；旧“是否允许R0/按模式禁止”占位退出；严重root、来源／报价确认／合同锁定待证 | PU06/O4；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:52](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L52)；[Mod/Commerce.lua:148](../../../../../../Mod/Commerce.lua#L148) |
| G30 | 补独立Carrier精确交叉引用：Governor生产定义、Meaning SQL、Inspiration清理／Dialogue传输；O7不删SQL或改编码 | O2/O5/O7；工程/原生开放部分不变 | [原 v3 Gap_Matrix_v3.md:53](../Convergence_PreDesign_v3/Gap_Matrix_v3.md#L53)；[Mod/NetworkBridge.lua:5](../../../../../../Mod/NetworkBridge.lua#L5) |

## 本轮新核对的关键差异

- 正常网络：[Mod/NetworkBridge.lua:103](../../../../../../Mod/NetworkBridge.lua#L103)仍通知pending；[Mod/NetworkInput.lua:70](../../../../../../Mod/NetworkInput.lua#L70)混用当前/保留角色；[Mod/NetworkBridge.lua:366](../../../../../../Mod/NetworkBridge.lua#L366)仍有MIXED可用性处理。正常可靠-only需真正迁移，不换标签。
- cold与物理结果：[Mod/Commerce.lua:281](../../../../../../Mod/Commerce.lua#L281)观察旧总Gold；[Mod/CultureNetwork.lua:298](../../../../../../Mod/CultureNetwork.lua#L298)恢复n但contributions为空；[Mod/StandardizationEffects.lua:191](../../../../../../Mod/StandardizationEffects.lua#L191)显式old.loaded整体保留。目标NET矩阵是行为变化提案；旧代码现状不能当新规则已完成。
- ACK：[Mod/FactChanges.lua:182](../../../../../../Mod/FactChanges.lua#L182)先替换queue，pcall计attempt；[Mod/FactConsumerBindings.lua:109](../../../../../../Mod/FactConsumerBindings.lua#L109)先清pending，invoke失败只有错误记录。O2必须以真实专业登记为接管。
- phase0／启动：[Mod/FactConsumerBindings.lua:11](../../../../../../Mod/FactConsumerBindings.lua#L11)固定RestructuringSync→NetworkBridge；[Mod/FactChanges.lua:164](../../../../../../Mod/FactChanges.lua#L164)只对active phase0 Bridge开放当前snapshot派生；[Mod/Gameplay.lua:837](../../../../../../Mod/Gameplay.lua#L837)先sealed后drain，[Mod/Gameplay.lua:1029](../../../../../../Mod/Gameplay.lua#L1029)最终Bindings/Complete/Readers.Seal次序保持。
- 信誉：[Mod/CityProgressionStore.lua:521](../../../../../../Mod/CityProgressionStore.lua#L521)支持信誉叶隔离、配置投影和原数据保留；[Mod/StoreSubrecords.lua:100](../../../../../../Mod/StoreSubrecords.lua#L100)临时检查不证明永久损坏。[Mod/Commerce.lua:148](../../../../../../Mod/Commerce.lua#L148)已有有效0，但[Mod/CapitalInvestment.lua:343](../../../../../../Mod/CapitalInvestment.lua#L343)尚无新的来源见证区分。当前数值路径不是全部资本功能坏掉；A要求补可信异常与锁定证据。
- P3：[Mod/Probe.lua:553](../../../../../../Mod/Probe.lua#L553)混生产写屏障；[Mod/PerformanceCounters.lua:204](../../../../../../Mod/PerformanceCounters.lua#L204)Flight参与现GC安全；[Mod/NetworkBridge.lua:41](../../../../../../Mod/NetworkBridge.lua#L41)的pcall求参前依赖trace global。删诊断需先正式owner提取，不改现GC政策。
- 双部署：[tools/deploy.py:50](../../../../../../tools/deploy.py#L50)拒runtime-only extras；[tools/temporary_playtest.py:37](../../../../../../tools/temporary_playtest.py#L37)有事务备份/回滚，但无同等受审removed-set合同。首次删文件发运前两条路径都补审查；本轮不改工具、不执行部署。

## 保留的限制

Crew唯一完成证据、native事件真实signature/窗口、实际物理写读回、失城/夺回端点权限、D1/diagnostic真实absence及双部署回滚均仍开放。旧测试名称/fixture存在不证明新目标通过；累计计数counterexample成功复现也不是Crew发放PASS。原科研/文化/商业/工业实机范围按现有记录复用，不新增随机掠夺、商人死亡、易主玩法或整轮全测要求。

## Carrier专项交叉引用登记

来源为独立[Specialization/Reports/Technical/Investigations/Carrier_Modifier_Footprint/Audit_Report.md](../../Carrier_Modifier_Footprint/Audit_Report.md)，未经本计划自动批准优化。

| 相交职责 | 当前源 | 只允许纳入本候选的内容 |
|---|---|---|
| ACTIVE生产定义 | [Mod/Data/GovernorProbe.sql:19](../../../../../../Mod/Data/GovernorProbe.sql#L19)→[Mod/Probe.lua:325](../../../../../../Mod/Probe.lua#L325)→[Mod/EffectiveFacts.lua:117](../../../../../../Mod/EffectiveFacts.lua#L117) | 可选诊断退出不得删生产fact定义；O1/O7先迁必要职责 |
| Meaning生产carrier | [Mod/CultureMeaning.lua:9](../../../../../../Mod/CultureMeaning.lua#L9)、[Mod/CultureMeaning.lua:17](../../../../../../Mod/CultureMeaning.lua#L17)，Data/CultureMeaningProbe.sql | Lua实验不启动≠SQL可删；本轮只保必要加载/cleanup门禁 |
| Inspiration/Dialogue退出／传输 | [Mod/CultureInspiration.lua:70](../../../../../../Mod/CultureInspiration.lua#L70)；[Mod/Dialogue.lua:298](../../../../../../Mod/Dialogue.lua#L298)；[Mod/UI/DialogueRefresh.lua:94](../../../../../../Mod/UI/DialogueRefresh.lua#L94) | Q1/Q7移交生产cleanup/ACK/ready，精确owned和来源proof保留 |
| SQL/save IDs | 原v3 O7、现行A0183:643 | 文件退出不等于SQL或保存ID可删；定义缩减／重编码均不纳入 |
