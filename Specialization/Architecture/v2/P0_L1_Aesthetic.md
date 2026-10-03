# P0-L1 — Culture III「风雅熏陶」具体实施计划

Status: AUTHORIZED / P0_L1_PARTIAL_NATIVE_GATE_REQUIRED。B149.176已测可见旅游加值正确、用户报告冷加载保持；实际回合累计结算时序仍待最小核对。
Authority: Design D0037（Harbor未来基线不扩本批）/ Culture D0029 `CUL_L3_AESTHETIC` / Shared D0035 / A0161。正式Design不变。
Implementation baseline: develop `caa5ec3`；此前live B147.174 / modinfo174，源码 `87655e5`。B148为初版检查点，当前修复源码B149.176；实际部署以Status/receipt为准。

## 当前切片与停止点

[P0-K限定实机验收](../../Status/Validation/Results/Specialization_B147_P0K_Pass.md)已关闭最小事实门禁。本批只接入风雅熏陶，以及[总计划明确分配给L1的旧文化人口/专家百分比退出](D0032_Implementation_Plan.md#明确的旧效果切换责任)。不要求先完成工业G–J或商业能力。

本批已获用户明确授权。B148首次原生验收[正预期但配置为0](../../Status/Validation/Results/Specialization_B148_P0L1_Native_Fail.md)按失败范围保留；用户随后授权修复，并确认印刷术解释原馆藏倍率。B149最小就绪/诊断修复及17项本地验证保留；[最新五图/结算边界](../../Status/Validation/Results/Specialization_B149_P0L1_Native_Rate_Review.md)确认已测可见加值+4/+6/+3，冷加载正常按用户报告记录。用户观察回合间先回落、再恢复；源码与两个定向模拟不支持“稳定输入每回合拆建载体”的解释，实际累计结算尚未确认。下一步只读现有文化胜利提示中的累计旅游，做两回合最小核对；必要的新单城时序诊断须另获授权。本轮没有运行代码修改或部署，不要求旧长测。L2意义延展、L3巨作启迪、M时代对话项目、N人文考察/网络、U2/机构排版不在本批。

## 唯一玩法合同

Current Identity=Culture，Potential≥3且当前ACTIVE≥3；单人本地人类玩家。读取本城当前合格巨作覆盖的不同历史时代数 `X`，以及本城当前合格普通建筑集合 `B`：

`Tourism[b] = aesthetic_K × X`，对每座 `b ∈ B`；`ExpectedBaseTourism = |B| × aesthetic_K × X`。

`aesthetic_K=1`来自正式Content的INITIAL_BALANCE_VALUE，作为本次初版实现参数，不升级成最终平衡值。例：2个时代、4座合格建筑 → 每座+2基础旅游业绩、合计预期+8。4件同一时代仍是X=1；同件移动到其它城市后按双方当前馆藏重算；不是作品件数、D/Tier权重、人口、专家人数或历史最大值。Lv4继续继承这项三级能力。

- 合格作品严格复用P0-K：著作、音乐、雕塑、肖像、风景、宗教艺术、文物；遗物、商品、奇观和未知Mod作品排除。时代属于作品本身，不替换为当前玩家/取得时代。
- **只用本城X。** 国内来源索引用于展示/其它合同，不能提高本城风雅熏陶；不需要商路，不走共同Network。
- 每座实际存在、完成且未掠夺的合格普通建筑计一次；免费取得/合格特色替代不改变资格。依Shared普通建筑语义，包括可建造城墙和政府区普通建筑；Tier0不因D贡献0而被排除。不只限剧院，也不只限当前D目录覆盖的领域。
- 宫殿、奇观、专业机构、内部载体、补偿建筑、展示项、未完成/被掠夺建筑不受益；改良设施不适用。未知建筑语义不擅自扩张，也不以InternalOnly或HD Tier单字段自动批准。
- X是当前事实；移走最后一种时代、建筑掠夺/移除、ACTIVE不足、确认失城时撤销相应当前效应。修复/重新具备资格后正常重算。没有永久旅游账本或历史最高值。
- 预期基础贡献、载体配置和原生最终旅游业绩分开报告；游戏其它倍率/原生馆藏旅游保留。不得把预测值当原生实测增量，也不以城市总旅游变化单独证明逐建筑正确。

## 实施前基线与技术门禁

表内“旧writer”等描述为B147实施前基线；B148实际切换见下方检查点。

| 项目 | 实施前事实 | L1处理 |
|---|---|---|
| 巨作时代/位置 | B147 Gameplay `GreatWorkFacts.Read`保留已确认馆藏；`DIALOGUE_SAMPLE`共用一次UI槽位采集，独立校验新事实与旧Dialogue | 复用，不另建巨作枚举/桥；需补最小确认变化通知给新consumer |
| 普通建筑目录 | `OrdinaryBuildingCatalog`主要覆盖P0-A领域；当前Domain/known清单不能直接覆盖全城普通建筑，如市中心/城墙 | 定域补齐本能力所需的已审阅ordinary分类与当前存在/掠夺事实；普通身份与D领域/Tier贡献分开，不改变D公式或旧consumer范围 |
| 旧人口文化 | `Lv3Effects.desired`仍按文化工作专家编码8个`BUILDING_SPC_DEV_LV3_POP_CULTURE_0..7`；SQL每专家系数0.5×人口 | L1切换时禁用Culture生成分支、清除精确8项，保留Commerce connected-kind分支 |
| 旧专家文化倍率 | `Lv4Percent`当前仅Culture，8个`BUILDING_SPC_LV4_PERCENT_CULTURE_0..7`，每专家+5个百分点 | 改为精确退休/撤销路径，不再产生此项收益 |
| 旧三级+2F/+2P升级 | P0-B1已将`Lv3Support.Start`转为退休路径 | 保持退休；3F3P、Lv2住房/GPP继续保留，不重复cutover |
| 原生旅游接口 | 只读已配置DebugGameplay：Yields无YIELD_TOURISM；未发现逐建筑Tourism DynamicModifier；`MODIFIER_SINGLE_CITY_ADJUST_TOURISM`现有用例为类别/来源倍率 | 科研普通Yield接口不能直接外推，倍率不能当固定加值 |
| 候选原生加值 | `EFFECT_ADJUST_DISTRICT_TOURISM_CHANGE`及`MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE`定义存在；Conservation城墙先例使用区域类型+城市拥有特定建筑要求、Amount1/2/3 | **STATIC_CONFIRMED定义/先例；PROTOTYPE_REQUIRED城市限定、逐建筑贡献承载、掠夺与撤销。** 没有本Mod原生PASS |

实施内部先完成一个最小原生路径门禁：一城两座不同普通建筑与另一城同类建筑对照。优先沿城墙先例，验证本城限定、按实际合格建筑独立贡献的旅游加值；若原生只在所属区域汇总显示，必须明确逐建筑计划→区域投影的技术归属，保留每栋贡献可解释性并证明总量/资格/撤销一致，不能将“区域产出”假称原生逐建筑读数。

若无法忠实承载该合同，停止该技术路径并报告；不自动改成整城倍率、只限剧院、城市无条件平铺、Yield伪装或减少recipient范围。原生接口未知是技术门禁，不是已确认无法实现，也不授权改Design。最小原型可以作为授权L1内的可逆检查点，但必须明确PROBE状态、作用范围、退出/恢复包，不能提前宣布最终L1完成。

## 实施顺序与旧writer切换

1. **资格/recipient事实。** 核对当前目录真实覆盖，按现有普通建筑语义补必要定义。允许最小调整既有catalog/共享快照，使L1能获取ordinary与完成/掠夺/位置，不能让D的`DOMAIN_UNMAPPED`或缺Tier误当“不普通”。复用现有事实采集，不为L1复制全城扫描器；D的领域、cap、权重与旧consumer行为保持。
2. **纯计划与原生门禁。** `CultureAestheticModel`（暂名）生成逐建筑贡献；先验证原生加值及城市隔离、掠夺/恢复/撤销。实施参数集中于本能力定义；不发明X cap、floor或新平衡值。
3. **一次明确cutover。** 原型/静态/本地达到可验证门禁后，再关闭上述两个旧Culture生成路径；由它们自己的精确owned列表清残留、确认退出，再启用新writer。若某城旧退出未确认，不给该城叠加新效果。没有按BUILDING_SPC前缀批删；普通建筑/永久records不动。
4. **实际writer与易主闭环。** `CultureAesthetic`负责差异投影、明确失效/退出、冷加载重新派生。按现有E2 `RegisterExit`/定域确认loss/`RemoveOwned`合同接入；原玩家夺回只按当前ACTIVE、馆藏与建筑重算，不重放旧旅游快照。
5. **简明诊断与提交。** 复用现有P0Panel按需入口/本地化；本地相关验证、commit/push后，实施轮才按现有部署授权及安全门禁发布最小验收包。本计划轮不部署。

旧SQL定义可作为惰性清理ID保留，不再由writer生成；不能仅停止启动模块而把存档里的旧carrier留下。保持Gameplay显式刷新/诊断调用兼容，禁用退休收益分支。Research旧人口/百分比已退出，不能复活。旧Dialogue、GreatWorkAdjacency、Culture Eureka、Commerce payload不在L1退休范围。

## 输入更新与临时状态生命周期

- 依赖只有当前资格/引用、已确认本城X、普通建筑资格/位置。新consumer只读必要X/有效性与recipient事实，不默认构造整份作品明细或国内索引；P0-K当前Read复制完整记录，可只补一个小型只读计算接口或同次接收的最小确认变化通知，不建新事件总线/通用能力引擎。
- 巨作创建/移动或跨城交易后，在原接收路径**确认**事实再定域更新受影响城市；原始事件只标dirty，不据未确认事件payload发收益。X相同且资格/recipient相同不写；相同X但引用/可用性变化仍正确处理。
- 普通建筑增减/掠夺/修复、总督/资格、合法认领/投资后的显式刷新、确认ownership loss、load，以及本地玩家回合的有界兜底保持。只缩小有可靠原生参数的范围；UNKNOWN/必要foreign后补撤销不被“只看本地事件”误删。
- UNKNOWN不是0。仅同一有效引用可保留上次verified配置待复核；确认不合法/失城立即退出，陌生引用不得继承。已确认空馆藏X0→撤销，读取失败不得伪装成空。
- 模块拥有当前城市计划/已施加ID及有界错误状态；按当前世界城市基数、替换旧记录，不累计历史通知/每回合快照。load重新核对现存投影；loss/removal清本模块临时记录/订阅，重复事件幂等；不改城市永久identity或账本schema。
- carrier自己引发的建筑通知只过滤精确已知本模块内部对象；无变化不写，不给真实普通建筑变化加每城每回合一次限流。无per-frame扫描、hover Gameplay请求或新增GC入口。

## 计划阶段预计改动与直接依赖

候选新增：`Mod/CultureAestheticModel.lua`、`Mod/CultureAesthetic.lua`、`Mod/Data/CultureAesthetic.sql`、对应定向测试；形式由原生门禁确定，不现在创建空壳。

预计最小调整：`GreatWorkFacts.lua`确认通知/轻量读取，`OrdinaryBuildingCatalog.lua`及必要的`DistrictCompleteness.lua`事实，`Lv3Effects.lua`/`Lv4Percent.lua`及其SQL，`Gameplay.lua`/modinfo、P0Panel及Text。只有真实依赖要求时触及E2或其它共享模块，并扩大对应定向回归，不顺手重构。既有GW目录、桥、旧Dialogue/GWA原则上复用；如需触及，先读全部直接调用点。

[manifest](../../Workflow/P0-L1.json)以完整能力对象、共享普通建筑合同、K实际检查点、事件合同及直接writer/source为核心；旧原生证据、E2 exit/return实现、受影响回归按动作展开。恢复/只读/验收归档只读当前切片及对应结果，不默认加载全部L/M/N计划、E2历史或全部中文设计阅读页。

## 验证、诊断与退出条件

本批文档用链接/selector/context/helper定向检查。实施按W0004 **L2跨模块收益**验证；ownership/加载/幂等部分补相关L3状态边界用例，不默认full regression/stress或旧长测。

| 定向用例 | 断言 |
|---|---|
| X与公式 | X0/1/2、多件同一时代不加X、两时代移走其中最后一件、excluded作品不贡献；每栋K×X，总量B×K×X |
| recipient | 跨领域、City Center/城墙、政府区、Tier0/高Tier、免费/特色；Palace/Wonder/carrier/改良/未完成/掠夺/未知排除；不按D/Tier/专家过滤 |
| 资格/隔离 | Culture ACTIVE2/3/4与非Culture；两城不同X不串城；国内有该时代但本城没有不受益 |
| 生命周期 | same-turn真实增减、重复零写、UNKNOWN保持与恢复、confirmed loss退出、return按现事实、cold load不自增、不重放快照 |
| 旧效果退出 | 精确8+8旧carrier及Modifier贡献退出且不再重建；Commerce旧connected-kind不改；B1/B2、Research/旧Dialogue/GWA不回归 |
| 工作量 | 复用现有dispatch/scan/capture/write计数；稳定输入无收益写与额外GW全枚举，明细仅按需，记录基数有界；不声称原生内存下降 |

新增实际测试使用真实Lua模块与最小native stub。旧`test_lv3_effects.py`/`test_lv4_percent.py`中历史收益预期是历史fixture，不为全绿改断言；新增当前cutover回归，并按实际共享改动选择P0-A/B1/B2、科研逐建筑、K事实和公共更新的相关断言。

诊断左键：`风雅熏陶｜ACTIVE3｜2个巨作时代｜4座合格建筑｜每栋+2｜预期基础合计+8`；附已确认/待复核/旧残留异常。右键只列时代集合与相关建筑计入/排除、每栋贡献，分页。技术ID只在异常追查需要时出现；原生读数无法取得时明确UNKNOWN。

**当前一次最小实机验收（由用户执行）：** 按用户选择固定馆藏与建筑，以总督调离/建立使同城ACTIVE跨三级门槛，比较配置及原生旅游差值，再保存完全退出冷加载确认。具体流程见[B149结果](../../Status/Validation/Results/Specialization_B149_P0L1_Readiness_Local.md#一个最小原生验收流程)。原来两城移作方案不再是本次强制测试。用同一流程记录旧人口/worker%退出和其它基础能力；无需重复K旧10图或内存长测。掠夺/修复本地覆盖；若无法本地证明native暂停，才补一个可操作最小案例，不要求等待随机灾害。原生倍率混杂时记录来源拆分，不凭城市总数猜测。

Exit：定向静态/模拟通过，原生旅游门禁及最小实机收益/撤销/冷加载通过，精确旧writer无残留，相关前序回归通过，证据范围明确 → L1完成；停止，不进入L2。若仅prototype通过，仍标partial，不把L1完成。当前无新Gameplay决策；技术门禁未关闭，不能承诺接口已经实机可行。

## 来源与证据边界

- [当前Culture Spec](../../Design/Specialization_v0.1_Design_Spec.md#6-culture--theater-square--cul)、[Culture正式Content](../../Design/Content/Culture_D0029.json)能力/参数/作品池；[Shared正式Content](../../Design/Content/Shared_D0035.json)普通建筑/当前资格。
- [批次/切换合同](D0032_Implementation_Plan.md#实施批次合同)、[公共更新约束](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)、[传播合同](Batch_D2_Runtime_Propagation.md#shared-work-and-publication)。
- [K实际事实API/事件](P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)与限定实机结果；计划阶段的原生Tourism调查仅只读已配置数据库定义/先例，未运行原型或游戏；本批新增本地投影检查点，未启动游戏。

P0-K STATIC/LOCAL及限定USER_GAME_TEST证据按原范围复用。B148.175的STATIC/LOCAL证据见下方；**P0-L1原生旅游接口尚无USER_GAME_TEST_PASS**。Design D0036、A0161、GC、main及永久成果不变。

## B148.175 — implementation checkpoint

**PARTIAL / NATIVE_GATE_REQUIRED。** 用户授权L1后完成可逆收益检查点；代码/数据库与本地模拟门禁通过，完整L1仍须引擎实测。实际包、源码commit、receipt只从[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)取得。测试结果与一次最小流程见[本地验证](../../Status/Validation/Results/Specialization_B148_P0L1_Local.md)。

### 事实、计划与实际效果归属

- `GreatWorkFacts.Summary`仅返回当前确认状态/引用/X；同一接收路径`OnConfirmed(pid, changedCityIDs)`只在consumer输入变化时通知，不新建采集器或商路条件。
- `OrdinaryBuildingCatalog`补已审阅原版/HD/区域扩展的普通身份；`DistrictCompleteness`沿同一次快照发布`baseDistrict`、`ordinaryDistrict/ordinaryReason`、`depthEligible`。新增身份但未批准Tier的对象`depthEligible=false`；D领域、旧Tier和cap均不变。未知Mod对象仍排除，不宣称全Mod目录覆盖。
- 实际consumer核对发现`ResearchApply`原来对全城ordinary执行缺Tier保护，因此必须只排除明确`depthEligible=false`的新对象；旧深度对象缺Tier/位置错误继续HOLD。其它科研与B2只消费各自原锚点，未扩大其收益范围。
- `CultureAestheticModel`逐栋产生K×X的可解释贡献。`CultureAesthetic`把同一实际区域上的贡献相加，按actual district plot写临时bit flags；单个city-owned master carrier通过`MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE`施加固定加值。16位编码上界是显式报错的实现容量，不是Gameplay cap；不截断/夹值。
- **逐栋贡献→所属区域投影**；不是原生逐建筑读数。没有YIELD_TOURISM伪装、整城百分比、无条件城市平铺或全国时代union。Subject Plot Property在District集合中的实际解释、city限定和原生增量仍需测试；定义/城墙先例只属STATIC_CONFIRMED。

### writer与生命周期

- 旧Culture人口与worker%两个SQL效果附件停用，Types/Buildings保留惰性清理ID；由各模块自己的8+8精确列表撤销，确认退出后才启用新master。低ACTIVE城市也执行退休清理；无名称前缀批删。退出失败则撤销本城新master并报告，不叠加。
- 当前reference/token、ACTIVE、本地馆藏、建筑资格或actual plot变化时重新派生；同输入不写。mutation前先关master，bit写入确认后才重新启用，失败无混合贡献。
- UNKNOWN只保留同一当前引用的verified配置；新引用/冷加载未确认先撤销。confirmed loss接E2精确owned退出；return只按当前事实重算，不恢复旧旅游snapshot。Plot OWNER标记仅用于定域清理本模块移除区域上的投影，没有新增永久历史或cityKey。
- 例程每次只用一次Shared建筑快照；无诊断行/完整作品副本/国内索引构造。记录与错误随当前城市集合裁剪，load重置；没有无界通知历史。明确scope事件和确认馆藏变化更新相应城；签名不可靠的事件保留本地玩家有界fallback；turn有界兜底，真实同回合变化不限流。
- 仅过滤本模块确知master自身建筑事件；无per-frame、hover收益请求、专家/人口事件专用订阅或新增GC入口。诊断左键摘要、右键时代/建筑组成分页。

### 本地与原生边界

13项本批测试覆盖公式/实际SQL配置、跨城/多社区、ordinary/D分离、ResearchApply保护、旧16项退出/Commerce不变、UNKNOWN/失城/回归/load/重复/失败及临时记录清理；26项K采集/事实/旧consumer隔离回归通过。编译、XML/file set、文档/selector/context检查单独记录。未运行历史full/stress或新长测。

**停止点：** 等待一次最小原生旅游验收；首次正预期却无原生增量/错误城市或区域归属时，停止该原生路径并记录TECHNICAL_PRIMITIVE_BOUNDARY，不自动改玩法或扩展L2。通过完整本批流程后再收束L1，不把本地配置一致写成原生收益PASS。


## B148.175 — native configuration failure review

[10张图与只读调查](../../Status/Validation/Results/Specialization_B148_P0L1_Native_Fail.md)记录了ACTIVE3、X1/2、2栋、预期+2/+4但配置+0；本批首项USER_GAME_TEST_FAIL。K/recipient计划能读，不等于writer已就绪、master健康或原生Modifier生效。“已启用”当前只依赖纯计划，诊断语义需要修正。

源码只由`LoadScreenClose`开启writer；现有测试默认手动置ready并另测显式load通知，未证明本局就绪过程。它是静态风险，不是已证实的引擎因果；0配置也不能区分master/bit/健康检测。加载DB定义存在，尚无正配置下的原生加值失败对照，因此primitive保持待验，未登记不可用或TECHNICAL_LIMITATION。

本次B148失败审查当时停止在调查/证据归档；以下是当时建议，B149授权修复已推进，见下一节。建议定域修复可靠就绪与按需状态分层、补未手动ready的相关本地用例，再做一次同城配置/原生区域增量短验收；不改K1、普通建筑或时代合同，不复活旧writer，不进入后续批次。先前本地结果按原范围保留；本轮未运行新Gameplay模拟、改源码或部署。

## B149.176 — readiness repair checkpoint

用户接受印刷术/已有建筑倍率对巨作基础旅游的解释，并明确授权修复。此次没有改变K1、时代/普通建筑资格、SQL原生路径、旧writer退休、永久状态或GC策略。

- **就绪入口。** 保留LoadScreenClose；已有GreatWorkFacts确认通知只有在本地玩家、当前城市引用、KNOWN且hasConfirmed成立时才开启一次本地玩家初始化核对。漏掉加载通知时，已有本地PlayerTurnActivated提供就绪兜底；foreign/UNKNOWN/过期样本不能触发确认入口。就绪原因属于模块会话状态，load重置，不写Property。
- **更新范围。** 初次就绪按本地玩家有界核对一次；以后确认通知仍只更新变化城市。同回合总督/真实事实变化照常响应，重复相同输入不写。未增加每帧、hover请求、独立巨作扫描或新的全国触发入口。
- **只读诊断。** 资格/预期、逐plot配置、master是否建立/健康、就绪/错误分别判断；同总量但错误位置不算一致。“配置已进入”只证明当前配置匹配，不能写成原生收益PASS。正常摘要不额外堆技术明细，未就绪/失配/右键才显示更新原因和载体/原始标记。诊断不会启动writer或施加收益。
- **本地证据。** 真实Lua5.5旧writer在漏LoadScreenClose的fixture里可复现预期正值/配置0；这证明缺通知风险，不证明B148游戏里确实漏了该事件。当前17项真实Lua/SQL定向用例PASS：旧13项保留，加4项缺加载/确认样本、首个本地回合/UNKNOWN/同回合总督、无效通知不启动、诊断分层/零写入。此前26项K结果继承原范围，本次未重跑。
- **夹具修正。** 普通测试改走实际LoadScreenClose，不再手动ready；ResearchApply用例在人工加图书馆后通知共享缓存失效，保留原Gold/missing-Tier/HOLD断言。实际ResearchApply代码未改。

[本次结果](../../Status/Validation/Results/Specialization_B149_P0L1_Readiness_Local.md)记录STATIC/LOCAL和固定馆藏的短验收。当前原生城市限定、District subject Property解释、旅游加值/撤销仍USER_GAME_TEST_REQUIRED。配置正确但原生无对应差值则停止该路径，不改公式或扩大L2；完成本批验收前不能宣布L1完成。


## B149.176 — rate acceptance and settlement boundary

[最新结果](../../Status/Validation/Results/Specialization_B149_P0L1_Native_Rate_Review.md)记录5张原图与当前唯一新增时序门禁。2时代×2栋、2时代×3栋、1时代×3栋的全国旅游分别122/124/121，相对118为+4/+6/+3；已测可见加值PASS，用户报告冷加载保持，不能扩展为每回合累计结算PASS。

静态writer与两个小型fixture检查确认：稳定计划/健康master跨本地回合、重复确认和同引用UNKNOWN不额外写入/拆建；KNOWN低ACTIVE才合法退出。真实回合间六个总督Property、Modifier重评估或UI缓存变化未观测，不能将顶部回落自动归为carrier正常刷新，也不能确认能力永远不计收益。

下一只读验证复用原版文化胜利页的`GetTouristsFromTooltip`累计提示，同一外国主要文明在稳定输入下采C0/E0、C1/E1、C2/E2。累计是否获得增强贡献是判定对象，整数游客或顶部当前率不足以证明。外部旅游概览解析只作为入口证据，文字格式不明不得补0。如果现有入口不可用/结果歧义，再准备单城、两回合被动时序诊断，另等用户授权；不主动重算或延迟真实退出、不改变玩法。L1仍partial，不自动实施后续模块。
