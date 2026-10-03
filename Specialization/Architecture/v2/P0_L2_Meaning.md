# P0-L2 —「意义延展」计划与接口调查

State: P0_L2A_NATIVE_PRECISION_RECORDED / FLOOR_DIRECTION_ACCEPTED。B151所测S/G半点不保留，整数追加可用；用户接受Floor方向，取整位置待确认。下一门禁原型仅为计划，L2B未授权。
Authority: Culture D0029 `CUL_L4_MEANING`、`contracts.work_pool/domains`；Shared D0035 `DISTRICT_DEVELOPMENT/YIELD_SHARE`。L1前置门禁见[B149结算验收](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md)；当前source/live与授权仅见[Status](../../Status/Specialization_P0_Status.md#current-authoritative-state)。

## 当前切片与停止点

B151.178十图原生结果已归档：[所测精度与边界](../../Status/Validation/Results/Specialization_B151_P0L2A_Native_Precision.md)。D1/W1实测0S/1G；D1/W2为0S/2G且下一正常回合保持；D3/W2为2S/8G。所测半点精度FAIL、整数追加可用；不据此宣布六yield、完整结算/native-only/作品排除/加载全部PASS。不再重做S/G小数实验。

用户明确采用Floor，只针对意义延展；**精确位置待确认**。推荐每件作品先将同yield领域贡献相加，再Floor，最后乘W：`per_work_y = floor(Σd∈y(0.5 × D_d × share_y))`，`total_y = per_work_y × W`。这是待确认提案，尚未写入正式Content/运行模型。

| 可改变结果的边界 | 推荐每件同yield合计后Floor | 每件逐领域Floor | 整城合计后Floor |
|---|---:|---:|---:|
| Campus D1，W2的Science | 0 | 0 | 1 |
| Commercial D1＋Harbor D1，W1的Gold | 3 | 2 | 3 |

确认位置后按既有Design同步流程记录本项例外并同步实际受影响来源/阅读正文；K0.5、Gold份额3、D/资格不改，不外推GPP或其它能力。此前测试授权要求不舍入是当时原规则的门禁，不与本次用户明确新方向混淆。

当前source/live仍B151.178，精确commit/receipt只看[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)。本轮只有证据/计划文档及归档，无新Implementation/部署。L2A接口问题已形成清楚结论；接下来先[最小L2B门禁原型](#推荐下一切片--p0-l2b门禁原型)，**等待具体范围及实施授权**。不自动启用六yield、不全局退休旧GWA，不进入L3/M/N/U2。

## 推荐下一切片 — P0-L2B门禁原型

**Goal / scope。** 在确认Floor口径后完成整数模型及两个现有接口门禁的最小原型：①同类别但不在支持目录的作品不获本项收益；②Meaning新增Culture不被旧Dialogue的Culture倍率放大。先只读核对精确primitive/附件/需求及已有反证，再作最小原型，不开展无界API调查。单城可撤销、默认关闭，复用L2A入口/既有事实和读数；已测Science/Gold不再造一批重复精度probe。

**前置。** L1所测PASS及K已确认作品事实、Shared D轻量读取、B151原生S/G整数证据。Floor位置必须用户确认并完成必要Design例外同步；Floor不能当作自动解除资格和native-only门禁。未获本切片实施授权前不写模型/SQL或部署。

**资格门禁。** 明确区分‘Lua合格W正确’与‘native writer命中具体作品正确’。核对能限定已支持定义的原生subject/requirement；同类别已支持与未知定义共存必须分别正确。当前probe整城拒绝只是实验保护，不是完整能力规则；不得自动扩容支持目录、给排除作品发放、改成整城补贴或凭UI过滤宣称通过。

**倍率门禁。** 对同一合格作品建立原生产出→旧Dialogue正常倍率→Meaning整数追加的对照，理论应仅原生产出被Dialogue放大；追加值保持固定。只定域隔离该追加路径，不在L2提前实现新版时代对话/永久modifier，不允许移除全部旧Dialogue规避测试。theming等组合按实际原语保留证据边界，不假定S/G成功就证明Culture。

**可能涉及文件 / 精确旧效果。** `CultureMeaningModel.lua`及必要的Meaning原型writer/Data、`GreatWorkFacts.lua`/Catalog（仅有真实接口需要时）、`Dialogue.lua`/SQL与旧GWA附件的直接调用点、Gameplay/modinfo/P0Panel/Text和对应定向测试。先复用现有模块，不强制新增模块；既有GWA156项只在选定fixture由该模块owned路径暂停，原型退出后按当前事实恢复。正常L1、其它城市、K producer/ACK与旧Dialogue持续；不全局cutover。

**更新 / 生命周期。** 原型操作及本城馆藏资格/位置/D/ACTIVE/当前引用变化；同输入零写、同回合真实变化保留。复用既有confirmed事实、dirty入口和加载兜底，不增加全城采集/per-frame/hover请求/独立GC。只拥有本城临时模式、当前配置及有界错误；UNKNOWN不当0，confirmed loss/加载/结束精确撤销，不写永久账本/补偿数据，不重放旧快照。

**本地验收。** W0004 L2 + 直接触及loss/load的相关L3断言：九领域同yield合计、D0/1/3/6/10、同yield两个领域、W0/1/2、整数编码；支持/同类别排除定义、Culture倍率与追加来源边界；旧新互斥、两城隔离、重复零写/同回合变化、UNKNOWN、退出/加载。继承B151未变S/G证据，采用必要SQL/真实Lua/打包负例；不跑历史full/stress，不以模拟证明原生组合。

**最小实机与退出。** 若本地无法确认组合行为，只交付一个单城、少量对照的门禁流程：支持作品与同类排除对象（真实可构造时）＋固定Culture追加，仅在选定fixture作既有倍率关闭/启用的定域对照，其他城市旧Dialogue不变，再退出检查。具体步骤由真实原型能力固定，不让用户寻找不存在的fixture或重复旧长测。路径能可靠满足→提交最终六yield正式L2B实施范围/manifest供审核；原型需实机确认→提交检查点后停止；无法按作品限定或无法隔离追加→报告具体primitive/Design差异，停止对应路径。不会以整城拒绝/误命中/忽略倍率宣布完整能力通过。

**明确不包含。** 正式全城市/六yield运行、全局旧GWA退休、新M/DialogueGameplay、L3/GPP、人文考察/文化网络、目录扩展、AI/MP、永久schema、GC调参或通用框架。正式cutover只有在两个门禁均有可靠路径之后再单独审阅/授权，不将本计划当作已授权任务。

## L2A既定实施与历史检查点

以下保留原L2A的完整授权范围、失败依据和当时no-rounding要求；进度已由上方原生结果取代，技术合同仍按所涉范围可追溯。

### B151入口修复 — 已授权LOCAL完成，原生待验

[修复与续测](../../Status/Validation/Results/Specialization_B151_P0L2A_Entry_Repair.md)：仅两ImportFiles、请求阶段/有界错误/本次View发布和单次读取；25项定向通过。完整实际request函数及导入名单负例覆盖，未把模拟加载当原生VFS证明。打包漏项已补，B150原生具体异常行仍未知；小数primitive未被判失败。

开始清旧View，成功View与Describe后才发布token；操作失败与读取失败分开，配置未知/操作错误不记成功基线，错误只属于当前展示。没有新增Gameplay通知/永久数据/GC。按Status/receipt执行W0003门禁，冷启动先读正常基线再续原单城流程；不授权L2B。

### B150原生入口中止 — 历史漏项依据

[一图、静态漏项与局部复现](../../Status/Validation/Results/Specialization_B150_P0L2A_Entry_Blocked.md)：ACK后外围通用报错，没有精度结果。两个Meaning Lua只有总Files、漏ImportFiles；旧模拟include直接读磁盘，本批验证遗漏action可见性。实际原生异常行仍未确认，不把小数primitive判FAIL。

当时建议两ImportFiles、外围阶段/有界错误、本次View及导入/真实请求测试，修复待授权。用户现已授权并由上方B151完成LOCAL修复；本图实验模式仍不能倒推，B150原LOCAL检查点及失败原件保留其证据范围。

### B150.177 — L2A实施检查点

新`CultureMeaningModel/Probe`及Science/Gold十片段SQL已完成；[本地证据与最小流程](../../Status/Validation/Results/Specialization_B150_P0L2A_Local.md)。左键基线→启用→结束，右键只读；默认关闭、一个fixture。exact旧GWA撤销未确认不进入probe，probe退出未确认不恢复旧writer；同token重复不切换阶段。

新fact摘要比较W及同类排除/类别未知数量，同一时代增减也通知；L1相同投影零写，且只额外忽略十个明确的非ordinary测试载体。未知作品整城拒绝只限受控probe，不是L2B资格解决方案。OFF常规事件不读D/馆藏；ACTIVE仅本城事实读取，无新GC。冷加载一次精确十载体清理含foreign，不重放测试模式。

18项新定向、15项直接L1、26项K与分发检查LOCAL PASS；native精度未确认。实机以报告D为准：本机HD集市T1、市场T2，不把“有市场”写成D1。不改Tier/目录、K0.5或舍入；两个旧L1版本/通知assertions未改，当前对应合同另有新覆盖。

完整L2仍需原生精度/归属、六产出、未知作品限定及native-only组合门禁；本批结束等待用户，不自动进入L2B。后续原有目标合同与计划保留如下。

### P0-L2A — 已授权具体范围

**Goal。** 用一个受控Culture ACTIVE4城市，证明每件合格巨作的半点加值是否实际结算，并区分逐件截断与多件汇总。不是把Lua配置能够表示0.5写成原生支持0.5。

**Scope。** 先建立/适配小型纯模型：读取当前专业资格、同次Shared领域D和K已确认合格W/资格摘要，按0.5份额精确计算，不舍入、不提前乘W再配置逐件效果。原生probe只在用户明确选定的单城启动，默认不自动覆盖其它城市；先测Science与Gold这条GreatWork加值接口，覆盖0.5/1.5/4.5。模型可验证全部映射，但不因此创建整套正式收益目录。

**旧效果隔离。** 已存在GWA仍按BASE六向量运行，不能同时作为probe收益。只允许由该模块按自己的精确156个signed pieces提供目标城撤销/有界抑制，probe退出后恢复旧路径；现有`off[pid]`是玩家级，不能冒充单城退出。未确认旧效果撤销，则不施加probe。其它城市旧GWA、L1、旧Dialogue、K采样继续；不退休整个模块或关共享producer。以Science/Gold验证先避免改动旧Dialogue的Culture/Tourism倍率；native-only问题仍留正式L2门禁。

**资格边界。** probe只接受已确认资格、已支持馆藏的受控fixture；若存在会被原生同类别Modifier一并命中的未知作品，拒绝该probe并报告。受控fixture通过不代表未知作品排除已经解决；L2B必须忠实处理已支持与排除作品共存，不把整城拒绝当正式规则。

**依赖/可能文件。** `GreatWorkAdjacency.lua/Model`及原SQL定义家族（owned退出/原语）；`CurrentSpecializationFacts`、`DistrictCompleteness`、`GreatWorkFacts`及其当前接口；最小`CultureMeaningModel/Effects`或现有模块适配、必要Data、Gameplay/modinfo、P0Panel/Text和定向测试。实施前读精确attachment/控制/调用点及实用E2入口；不是现在全仓重审。若不触及producer，`DialogueRefresh`仅为已有事实桥依赖，不顺便重写。

**更新/性能。** 主动probe操作与本城已确认馆藏/D/ACTIVE/引用变化才重算；复用当前确认入口和有界load/本地回合兜底。同一时代增减作品也要正确观测：B150已在OnConfirmed比较中补count及同类排除/类别未知数量；没有增加第二套槽位扫描。L1收到额外相关确认仍应相同投影零写；不复制全城槽位/领域采集、不加per-frame/hover请求、每城每回合限流或独立GC。

**临时状态。** 模块只拥有一个当前fixture引用、probe模式/最近计划及有界错误；同Owner当前事实校验，UNKNOWN不当0，foreign/loss明确退出，重复幂等；结束/更换fixture/加载处理撤销自己的测试效果，不能残留或扩散。永久专业/投资/作品不写；不记录收益补偿/跨回合小数账本。

**本地验收（W0004 L2）。** D0/1/3/6/10/cap与最高单区域、Gold份额3、W0/1/2且理论总量只乘一次；六映射/排除事实；同回合同一时代件数变化、重复零写、ACTIVE/UNKNOWN/两城隔离；精确旧GWA互斥、probe退出/失败/受影响loss/load边界；保留K与L1直接相关断言。只选所涉及的回归，不运行全历史或stress，不以模拟证明native精度。

**一个最小实机流程（待包就绪才执行）。** 用一座Culture4城市放一件合格著作，已存在的T1 Campus/Commercial可形成D1，读取理论每件Science0.5/Gold1.5并核对原生追加。放入第二件同一时代作品，区分逐件floor与汇总floor；必要时将相关领域增到D3，核对每件Science1.5/Gold4.5。结束probe确认加值撤回/旧路径恢复；同一城完成必要正常结算读数，不要求长测。界面显示不充分时优先采原生城市/作品明细和实际结算证据；第一个不可忠实结算的值出现即停，不要求继续凑完整矩阵。精确步骤与按钮以最终测试包为准。

**Exit。** 静态/定向本地通过、该受控原生接口精度/归属/退出结果清楚，交付L2A结果及L2B条件。0.5失败登记具体接口证据，只有需要改玩法时提出DESIGN_DECISION_REQUIRED；不自动沿用科研Floor。即使Science/Gold通过，也不宣布全六yield、theming/未知作品隔离/native-only或完整L2PASS，不自动实施L2B。

## 范围与完整规则

以下为D0029尚未同步Floor的正式规则与原始理论值；新Floor方向/待确认位置见CURRENT，不将旧no-rounding写成新的实施授权。

只接Culture ACTIVE4的意义延展；每件合格巨作，逐领域追加：

`shares_d = meaning_K × D_d`；`yield_per_work_d = shares_d × share_value(yield_d)`。

meaning_K=0.5为初版参数；金币一份=3，其它普通产出一份=1。同产出领域分别计算相加；同领域多个区域按Shared最高单区域D，不合并D；D是绝对深度cap10，不按规则环境归一化。不要求该领域成为本城Identity，不以工作专家数/人口/作品时代数代替D或件数。

| 领域 | 代表产出 | 对L3的GPP映射（不在L2发放） |
|---|---|---|
| Campus | Science | Scientist |
| Industrial Zone | Production | Engineer |
| Commercial Hub | Gold | Merchant |
| Harbor | Gold | Admiral |
| Encampment | Production | General |
| Holy Site | Faith | Prophet |
| Government Plaza | Culture | 无 |
| Diplomatic Quarter | Culture | 无 |
| Neighborhood | Food | 无 |

不包括Theater自身。完整作品资格只复用K的已支持七类/历史时代目录；Relic、Product、Wonder及未知定义排除。普通建筑完工/未掠夺、免费/特色及缺Tier规则按Shared；不使用旧BASE相邻、旧Actual复制或额外填值。例：Campus D10→每件5Science，Industry D6→3Production，Commercial D3→4.5Gold；Gold并非1.5。

Meaning是追加产出，未来Dialogue只放大作品原生产出，**不得放大本项**。未知原生theming/其它倍率不能被假定为已接受叠加规则；需要对实际路径做组合核对，不能借配置读数替代回合入账。

## 已有实现与可复用部分

`GreatWorkAdjacency.lua/Model`当前读取全部完成专业区域的BASE向量，借Dialogue样本挂`BUILDING_SPC_B060_{yield}_{P/N}{0..12}`，SQL为七类GreatWork的±0.5二进制YieldChange。它仍是旧效果，不符合D输入。模块有精确owned撤销及E2 exit/return，能复用writer/退出结构；旧公式不能保留补空缺。

`GreatWorkFacts`已有confirmed作品/件数，`DistrictCompleteness.Read`已有D及单区域选择。新例程取必要小型输入；不构造整份诊断、国内来源或第二套区域/槽位枚举。

原生分类Modifier只按GreatWorkObjectType限定，不直接按K支持的具体work type限定；**未知同类Mod作品可能误受益**，需处理到一致，不能将UI排除当成效果排除。

## 最小接口门禁及停止条件

1. **精度：** 使用真实GreatWork加值路径分别探0.5、1.5及Gold4.5；一件作品与两件作品区分逐件截断/汇总截断，确认普通城市结算。B055整数文化加值/撤销通过可以复用；B059百分比floor及科研district/per-specialist floor均不授权L2取整。
2. **资格：** 一件已支持作品与同类别未支持定义作本地/native必要对照；禁止“目录数正确但全类Modifier仍影响排除作品”。路径若无法限定，停止并报告具体primitive边界。
3. **隔离：** 同城同时配置作品native倍率与本项附加值，验证Dialogue百分比不放大追加。先静态/模拟划清attachment与origin，再给一次最小原生对照。所测Culture一类不扩大为六yield/所有theming。
4. 原生路径不满足时登记TECHNICAL_INVESTIGATION_REQUIRED；备选不同primitive可以调查，**没有本能力明确许可与取整位置确认时不能自行floor；不能改系数、造补偿永久账本或采用整城补贴**。真正需要改Gameplay才交用户决定。

在全部门禁可表达前只做后续获授权的可逆接口probe，不宣称L2完成。此前计划轮没有运行原型；B150/B151 L2A现已取得上方所列原生精度结果，不把S/G范围扩大为资格/native-only通过。

## 实施切片与旧writer退出

- 第一步纯模型：同一次Shared快照→每领域D与份额→每件各yield值；记录资格/UNKNOWN，模型不用旧DialogueModel的作品时代判断。原L2A测试保留精度；未来正式模型按本次明确确认后的Floor口径处理，不自行选择取整位置。
- 第二步原生门禁：隔离旧Adjacency，仅该probe范围由旧模块自己撤销；未通过不进行正式新旧切换。不能把探针收益与正式L2叠加。
- 第三步明确cutover：读全Mod内上述精确carrier、SQL附件、旧READ/OFF/AUTO、load/Start/Audit及AdjData消费者调用点；旧模块撤销成功后新writer施加。旧退出不确认则本城不启用新效果。carrier定义可留惰性清理ID，生成/恢复入口必须退出。
- **只退出旧GreatWorkAdjacency。** 保留旧Dialogue到M，Culture Eureka到N3，保留L1、Lv1支持/Lv2住房/GPP、科研和商业。`DialogueRefresh`是K/旧Dialogue共用producer：只在最后AdjData消费者退出后停止该投影，不能关整条巨作采集/ACK路径。
- 最后按需诊断→相关本地回归→提交；L2B实施/部署须其单独授权；L2A按W0003现有安全门禁部署，实际receipt见Status，不自动启动L3。

候选责任落在`CultureMeaningModel/Effects`或有明确职责的原模块适配，不强制新文件数量。真实影响范围：旧GWA Lua/SQL、Shared轻量读取、K通知/输出、Gameplay/modinfo、P0Panel/Text及定向测试；M仅作收益隔离接口约束，不在L2建立其永久账本。

## 更新、生命周期与回滚

事件原因：本城馆藏资格/位置、领域D/掠夺修复、ACTIVE/引用、明确失城/恢复、load。按确认事实定域更新；同一输入零写，同回合真实变化保留。无专家变化依赖，不为纯资格判断全国重算。

UNKNOWN同一可靠引用可保留最近verified配置待核对；确认空馆藏/资格失效/loss由模块owned path撤销。陌生引用和cold load不能重放旧配置。模块保存当前计划/已施加片段及有界错误，按当前城市集合替换/退出，不保存收益快照为永久成果。自身已知carrier事件精确隔离，不过滤真实建筑变动。

回滚边界为Git中的本批前已验包及部署receipt；撤销新owned effects再恢复前包，不能留下old+new。无需新增永久schema；不删除普通建筑或E2记录。运行补丁失败不会用Design变更补洞。

## 验证与退出

W0004 L2；实际触及E2/引用时补相关L3状态断言，不默认历史full/stress。

| 本地定向矩阵 | 核对 |
|---|---|
| D0/1/3/6/10、cap前后、特色/免费/掠夺/同领域多个区域 | Shared事实被忠实消费，金币份额3、同yield加总 |
| W0/1/2、同一时代多作品、支持/排除类型 | 逐件值不被再次乘件数；最终理论合计只乘一次W |
| ACTIVE3/4、UNKNOWN、两个城市、same-turn修改/重复通知 | 无串城、无变化零写、明确失效退出 |
| native-only组合与精确退休 | 旧BASE作用不残留/重建；K/旧Dialogue及Research、L1直接相关回归不破坏 |
| load/loss/return、writer错误/技术编码容量 | 按当前事实派生；失败不混合、不静默clamp或floor |

后续一个最小实机流程：同一Culture4馆藏城，选能得到半点的D领域，一件→两件→移走一件，观察原生追加及一次ACTIVE撤销/冷加载；组合隔离仅补同一城必要的native倍率对照。接口失败第一项即停。具体流程在probe包就绪时固定，不现在要求用户另做。

诊断先显示`合格W件｜每件Science/Gold…｜D来源｜预期/实际配置｜已确认/待核对`，组成分页；不以“已挂carrier”宣称原生收益通过。

Exit：精度/recipient/native-only门禁、精确cutover和本地范围通过，再由用户确认原生对应场景。当前用户已接受意义延展Floor方向，精确口径待确认并同步正式来源；资格/native-only技术门禁仍开放，不因此获得完整L2实施授权。

来源：[Culture正式Content](../../Design/Content/Culture_D0029.json)、[Shared](../../Design/Content/Shared_D0035.json)、[总cutover合同](D0032_Implementation_Plan.md#明确的旧效果切换责任)、[旧加值实现/限制](../../Reports/Technical/Specialization_B060_GW_Adjacency_Implementation.md)、[B055整数实机范围](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)、[精度待办](Yield_Precision_Backlog.md)。
