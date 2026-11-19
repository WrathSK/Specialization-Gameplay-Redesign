# 文化后续模块：计划与调查入口

## 当前切片与停止点

[现行文化设计](../../Design/Culture.md)说明能力、见闻、任务和分发规则。[现行架构](../Specialization_v0.1_Architecture.md#current-authoritative-state)说明事实、收益与持久记录的分工。实际构建和下一步见 [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)。早期文化实施顺序及当时的待验清单见[原始计划](../../Historical/README.md#delivered-culture-preparation-and-playtest-plans-in-git-history)。

## 按模块阅读

| 要追查的行为 | 实施与验证入口 |
|---|---|
| 风雅熏陶的建筑业绩与馆藏更新 | [L1 实施](P0_L1_Aesthetic.md)、[B527 实机与冷读档](../../Status/Specialization_P0_Status.md#b527-hd-great-work-and-cold-load-evidence-reviewed--s1091) |
| 意义延展的领域产出和主题化 | [L2 实施与失败证据](P0_L2_Meaning.md#当前切片与停止点)，政府广场／外交区的文化追加已有设计规则，原生实现仍待定域验证。主题化见[现行文化设计](../../Design/Culture.md) |
| 巨作启迪的各类伟人点数 | [L3 选用的原生百分比接口及精确归因限制](P0_L3_Inspiration.md) |
| 时代对话的完整回合、额度、历史及旅游业绩 | [M 真实项目与累计投影](P0_M_Dialogue.md)、[B177 原生验证范围](../../Status/Validation/Results/Specialization_B177_Dialogue_Cumulative_Native_Result.md) |
| 考察团训练、旅行、任务和见闻 | [N 实施与原生异常记录](P0_N_Expedition.md)，[结项后保留的人文考察团问题](../../Reports/Proposals/Architecture_Convergence_Closeout_Review.md#结项后继续保留的事项) |
| 文化网络分发以及重新连通 | [N3 见闻与分发合同](P0_N_Expedition.md#n3culture-network与精确旧eureka退出)、[B232 当时的更新与退出](../../Status/Validation/Results/Specialization_B232_Native_Review.md)、[B527 无 HD 实际收益和环境范围](../../Status/Specialization_P0_Status.md#b527-no-hd-culture-network-and-load-readiness-verified--s1093) |
| 机构后续与馆藏时代展示 | [U2 保留的展示方案](P0_U2_Culture_Era.md) |

下方保留早期接口、技术分界与已记录的测试限制。具体实施和待办按其所属构建解读。

## 共同输入与真实缺口

- **D**是Shared绝对基础设施深度；**X**是本城合格作品历史时代种类数；**W**是合格件数；成功见闻历史、当前有效见闻、完整文明集合各自独立。不能互代或从载体反推。
- K当前`Summary/OnConfirmed`已有X/count/排除与未知计数/引用/确认状态。等count/X的时代组成、作品替换与国内来源变化仍可能没有compact callback；U2要小型呈现通知，L3只消费E和资格，等E组成变化不改变其倍率；无需新采集器。`Read`完整副本、`Domestic`时代索引仅在真实需要时构造，hover不请求。
- K的UI collector/Gameplay完整集合校验面向本地人类城市；N外国WORKS目标须按选中/活动任务定域采样及Gameplay复核，不冒充国内样本或广播全世界。
- 普通计算复用DistrictCompleteness的确认D与所需资格；UNKNOWN不当0，不补Tier或用名字猜同城。详细建筑/作品行仅按需诊断。
- 当前Store/E2可提供可靠城市映射与具名退出/恢复，已有投资、工业模板及Research传统业务；B175新增Dialogue累计/额度首段；对应新收益与考察/见闻业务仍须分别完成。城市历史、进行中事务、单位归档与派生收益分开，不套统一永久成果继承，不新建cityKey/通用Legacy框架。

## 本次纠正及仍保留的技术证据

| 项目 | 已定规则 / 本次纠正 | 不可扩大为 |
|---|---|---|
| Dialogue | 每次5%×完成X，历次加算无额外cap；提交前资格/身份/重组/Owner/生产中断取消，无额度无半进度；成功后城市历史保留 | 完整新累计yield writer已实现，或所有生命周期已通过；B175只覆盖首段所测项目/历史场景 |
| 见闻与考察团 | 见闻随城，不按原Owner分账；自身文明仅过滤当前使用。归档城易主中止任务、单位留原Owner、旧归档失效，按E3免费重挂靠 | 任何时候任意换归档，或把城市历史搬到新归档城 |
| 新首测值 | Spy当前成本等价、全国现存cap1、标准任务2T、整体本城K_T2、Network K_C1 | 最终平衡、接口可用或原生已验 |
| 真实1T项目 | [B123](../../Status/Validation/Results/Specialization_B123_Project_Pass.md)正常入口/显示/完成/无后续溢出及所测chop；[B126](../../Status/Validation/Results/Specialization_B126_Claim_Core_Pass.md)Claim限定核心证据 | M新额度/取消/累计/全部注入通过；异常强制completion接受决定仍按原记录保留 |
| GW百分比与追加 | 旧[B059.82](../../Status/Validation/Results/Specialization_B059_82_Percent_User_Result.md)为非主题化作品读数，整城Culture未变化；B161–B165各自scope另见L2结果 | 旧读数证明实际结算、主题化或native-only隔离；B166已在正常源码退役GWA；旧记录本身不证明新包已部署／原生通过 |
| GPP / 整城Tourism | 此前缓存有GPP Amount接口、PointsPerTurn整数字段；Tourism例多带类别过滤，未找到无过滤先例 | 引擎一定不支持小数/整体旅游；也不能据接口名宣布可行 |
| Spy静态线索 | 旧缓存有Cost/Spy/CanTrain/PurchaseYield字段，只用于技术定位；本次未重读外部DB/UI | 缓存60固定为考察成本，自动继承Spy容量/购买/敌对行为 |

旧报告保留原字节与版本；其静态/原生证据只在相同接口和范围内继承。此次是当前合同/直接代码与文档检查，没有新增玩法模拟或实机事实。

## 后续反馈如何影响计划

| 新发现 | 定域复审 | 无需自动重开 |
|---|---|---|
| L1区域Tourism失效 | 明确复用该投影的consumer | M项目、L3 GPP、N任务；N整城旅游是另一原语 |
| Shared D/目录修正 | 使用该目录的L2与普通建筑consumer（D0049 L3不再依赖D） | START Era额度、考察成功键等无关合同 |
| K资格/时代/位置问题 | L1/L2/L3/M/U2；N WORKS若复用目录也核对 | 已验独立E2/投资及其它任务类别 |
| L2追加/倍率/结算门禁失败 | L2与M实际复用的隔离路径 | L3 GPP和U2展示，不自行换城市补贴或改Design |
| M/N新业务保存问题 | 真正共享该字段/事务路径的调用方 | 无新增永久状态的K/U2，不默认全面暂停 |

## 下一步边界与验证

按[现行工作流](../../Workflow/README.md)和 [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)确定任务范围与待验内容。文化准备阶段的切片顺序和旧组合测试方案见[完整原件](../../Historical/README.md#delivered-culture-preparation-and-playtest-plans-in-git-history)。
