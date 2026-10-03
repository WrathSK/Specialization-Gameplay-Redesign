# P0-L2 —「意义延展」计划与接口调查

State: P0_L2A_ENTRY_REPAIR_LOCAL_COMPLETE / USER_GAME_TEST_REQUIRED。用户授权B151最小入口修复，注册/请求定向LOCAL通过；原生精度仍待验。L2B未授权，NATIVE_PRECISION_GATE_OPEN。
Authority: Culture D0029 `CUL_L4_MEANING`、`contracts.work_pool/domains`；Shared D0035 `DISTRICT_DEVELOPMENT/YIELD_SHARE`。L1前置门禁见[B149结算验收](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md)；当前source/live与授权仅见[Status](../../Status/Specialization_P0_Status.md#current-authoritative-state)。

## 当前切片与停止点

计划核对基线：develop `f02e4e8`，现有B149.176运行源码`637f97b`；原计划为只读核对。当前L2A实施基线2f1304f；实际source/live以Status及receipt为准。Spec D0037的Culture覆盖范围、完整`CUL_L4_MEANING`、作品池/九领域及Shared D0035份额/深度/ordinary合同已核对；没有采用旧GWA公式或旧Floor许可。L1已按已测范围PASS，不要求再拍旧截图。

分两段；**用户本轮只授权P0-L2A**。L2B完整能力不因此获授权。

| 切片 | 目标 | 停止点 |
|---|---|---|
| P0-L2A — 单城接口验证 | 真实Shared D→逐件理论值；用已审阅GreatWork加值原语验证0.5/1.5/4.5与原生收益归属 | 一个最小实机接口验收后提交结果；不正式启用全城L2，不全局退休旧GWA |
| P0-L2B — 完整意义延展 | 解决已支持作品限定及native-only隔离，接全九领域/六产出、事件/退出/加载、精确旧GWA cutover | L2A结果后更新最终方案、另审阅/授权；不进入L3/M/N |

L2A是本能力内部的原生门禁，不新增Gameplay规则或永久账本；失败时保留原规则并停止对应效果路径，不能自行floor/补贴。L2A现有W0001 manifest已登记，见[本批读取/验证范围](../../Workflow/P0-L2A.json)；没有新调度或状态系统。

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
4. 原生路径不满足时登记TECHNICAL_INVESTIGATION_REQUIRED；备选不同primitive可以调查，**不能自行floor、改系数、造补偿永久账本或采用整城补贴**。真正需要改Gameplay才交用户决定。

在全部门禁可表达前只做后续获授权的可逆接口probe，不宣称L2完成。此前计划轮没有运行原型；当前B150 L2A仅完成受控实现及LOCAL验证，native待验。

## 实施切片与旧writer退出

- 第一步纯模型：同一次Shared快照→每领域D与份额→每件各yield值；记录资格/UNKNOWN，模型不用旧DialogueModel的作品时代判断。测试精度保留，不在模型提前舍入。
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

Exit：精度/recipient/native-only门禁、精确cutover和本地范围通过，再由用户确认原生对应场景。当前规则已定义，技术门禁开放；未获Culture量化许可，无新决策要求用户现在回答。

来源：[Culture正式Content](../../Design/Content/Culture_D0029.json)、[Shared](../../Design/Content/Shared_D0035.json)、[总cutover合同](D0032_Implementation_Plan.md#明确的旧效果切换责任)、[旧加值实现/限制](../../Reports/Technical/Specialization_B060_GW_Adjacency_Implementation.md)、[B055整数实机范围](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)、[精度待办](Yield_Precision_Backlog.md)。
