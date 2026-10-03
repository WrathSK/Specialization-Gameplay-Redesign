# P0-L2 —「意义延展」计划与接口调查

State: P0_L2C_PLANNED_NOT_AUTHORIZED；D0043已采用意义延展七域五产出，文化追加技术DEFERRED，不再阻塞本版v0.1；source/live B157仍旧九域原型，未适配。正式cutover／下一能力未授权。
Authority: Culture D0043 `CUL_L4_MEANING`、`contracts.meaning_domains/work_pool/meaning_multipliers`；Shared D0042 `DISTRICT_DEVELOPMENT/YIELD_SHARE`保持。实际source/live与授权见[Status](../../Status/Specialization_P0_Status.md#current-authoritative-state)。

## 当前切片与停止点

用户已明确采用暂排方案，[D0043接受](../../Design/Design_ChangeLog.md#accepted-d0043--2026-10-03)仅改变意义延展适用域：Campus／Industry／Commercial／Harbor／Encampment／Holy Site／Neighborhood；Science／Production／Gold／Faith／Food。Shared完整映射及其它能力保持。K／逐领域Floor／W／作品资格／ACTIVE与独立追加不变。

[B157三阶段](../../Status/Validation/Results/Specialization_B157_Modifier_Comparison_Native.md)已确认所扫Writing实例进入／退出及S/G读数1／4，Culture＋3实例虽映射正确却Δ0，失败保留。[文化技术档案](../../Reports/Technical/Specialization_B155_Meaning_Culture_Path.md)、B155两候选及下方诊断／主题化原型章节保留为未来调查；其中旧“尚未采用／待诊断”只描述当时，不是当前指令。本轮不继续该调查，不要求用户重测，不删除实验精确清理依据。

当前runtime未因Design记录改变，Model仍九域，Probe／reader／载体只S/G/C且要求正Culture；P/F/Faith没有Meaning writer。下一[P0-L2C计划](#下一批计划--p0-l2c-七域五产出门禁)必须正确适配零Culture流程，不能删两个输入后沿用旧四态。计划／manifest为PLANNED_NOT_AUTHORIZED；本轮不写Mod、不部署。精准recipient／倍率／正常结算与最终cutover仍按各自真实门禁，不把文化技术延期误当其它问题已解。

## 下一批计划 — P0-L2C 七域五产出门禁

**Goal／边界。** 一个默认OFF、单城可逆原型，验证七域模型及五产出的整数承载、实际读数和定域退出。先让剩余五yield进入可验证状态；不是全城正式接入，也不是整个L2完成。实施须用户另行授权；不实施Culture新候选或宿主诊断，不进入巨作启迪／时代对话正式改造／考察／Network／UI润色。

| 工作 | 具体范围与责任 |
|---|---|
| 七域输入 | 只在Meaning白名单排除Government／Diplomatic；沿用Shared D与K确认馆藏，不改Shared或其它consumer。每域换算后Floor，同yield再合并，W最后乘 |
| 五yield writer | 复用S/G已测整数primitive；补Production／Food／Faith的精确module-owned有界载体。合法每件最大S/Food/Faith=5、Production=10、Gold=30；不静默clamp、不补差，不借此判定新primitive已原生PASS |
| 零Culture流程 | 去掉SINGLE3／正Culture启动与③门槛；流程为基线→五yield追加→直接结束。旧Meaning16项owned（含Culture候选）的清理依据保留，旧候选不启用；旧实验加载／引用退出责任不丢 |
| 可读诊断 | 一张报告显示合格W、每件／总量五yield预期和原生实测、ACTIVE／配置状态；D组成按需展开。只显式读取，不加hover／per-frame请求、全局常驻扫描或GC入口 |
| 旧效果与退出 | 原型内只hold目标城GWA，由原模块撤精确156项；维持本城旧Dialogue0%控制。先清新owned，确认退出后释放旧模块按当前事实重算；其它城市不受影响、UNKNOWN不扩大清理 |

**Likely touched。** `Mod/CultureMeaningModel.lua`、`CultureMeaningProbe.lua`、`Data/CultureMeaningProbe.sql`、`UI/BoostGreatWorkRead.lua`及直接请求／UI／本地化／modinfo、`DevelopmentTests/test_culture_meaning_probe.py`和直接reader回归。旧GWA／Dialogue／K桥只在真实调用依赖要求时作最小适配；所有影响路径实施前仍读精确消费者，不因hash匹配略过writer／load／loss边界。

**触发／生命周期。** 本城明确验证动作、馆藏位置／资格／件数、七域D、ACTIVE／reference变化；复用当前Shared／K样本，不复制全城采集或构造全套诊断用于普通计算。相同可靠输入零写，同回合真实变化继续响应；同一session只保留单fixture／有界读数，结束、引用退出、失城、load按module-owned路径处理。load默认OFF，永久Property／E2历史／GC策略不改。

**Local acceptance。** W0004 L2＋直接触及退出／加载的L3断言，不默认full／stress。七域映射与两个暂排域变化无影响；D0/1/3/6/10、每域Floor后同yield合并反例、W0/1/2；五yield合法编码范围／精确附件／无Culture生成；零Culture可启用／结束、重复零写／同回合变化／两城隔离；UNKNOWN／引用错误不误清；创建或退出失败不混合旧新；load／loss精确撤除、直接请求及读数失效不回归。外部DB仅只读定义证据，不替代原生。

**Minimal game test（包就绪后给精确步骤）。** 复用当前Culture ACTIVE IV存档，一城已支持作品及已登记普通建筑，确保五yield输入有可观察非零值；可用既有Cheat补足已支持建筑，不扩目录。一次基线→启用报告比较五yield→同回合移动一件作品核对件数→保存实验仍启用的副本→直接结束并核对撤销→完全退出→冷加载该启用时副本，检查实验默认OFF、精确载体清理及旧路径按当前事实恢复。用户只需少量报告，不逐回合截图或旧长测；具体正常收益／结算仍按原生能提供的实际观察，不用carrier配置冒充入账。第一项失败停对应路径；没有某yield非零fixture就标未测，不凑PASS。

**Exit／后续。** 五yield各给STATIC／LOCAL／USER证据及原型生命周期范围；所测整数读数／变化／退出可靠后，再提出正式接入与旧GWA cutover计划。精确支持作品recipient、Dialogue／theming独立、正常结算未覆盖部分仍是各自下一门禁：同类未知作品的整城probe拒绝只是临时保护，不可作为正式精准排除方案；当前旧Dialogue只测C/T也不证明未来全native-yield倍率隔离。不得因此宣称完整L2 PASS。文化平加／宿主调查单列未来恢复，不再作为七域五yield前置；只具体未通过的相关路径阻塞其后依赖，不默认阻塞整个v0.1。

**Rollback。** 继续Git已验source＋既有部署receipt；清新owned后才恢复旧package。保持游戏退出、staging／target／recovery／equality门禁；本轮只有计划，无新build／deployment标识。

## Modifier实例诊断

**历史技术合同／未来恢复参考。** B156/B157已完成所测诊断；D0043已采用两域暂排，以下首次诊断／三态派发不是当前待办。原证据范围、一次token与有界读取限制继续保留，不自动授权新诊断。

**目的／范围。** 在现B155固定Writing fixture，区分HD著作＋2与Meaning Culture3的定义命中、附件／owner、活动API值和作品实际读数。先例与[建筑来源调查](../../Reports/Technical/Specialization_B155_Meaning_Culture_Path.md#古罗马剧场建筑与著作收益来源复核)已STATIC核对；原生实例schema、城市映射／活动、组合算法仍UNKNOWN。本节计划已由用户明确授权实施，B156完成；只读诊断不等于Meaning新收益路径。

### 入口、责任与只读边界

- 优先修改现有`Mod/UI/BoostGreatWorkRead.lua`、`Mod/UI/P0Panel.lua`及直接定向测试；版本登记按实施时实际检查点更新。不新建Gameplay writer、carrier／SQL定义、Property／账本、事件订阅、GC调用或常驻debug服务；不改原型阶段／HD／正式Design。
- 复用“意义延展验证”右键`CULTURE_MEANING_READ`，matching token／版本／所选local-owner city／当前完整reference后才执行独立UI helper。允许OFF／配置异常时报告可取得的原生实例，不依赖现Meaning四态reader成功；诊断失败不改carrier、hold或原型阶段。`Gameplay.lua`现READ只View／Describe，ADVANCE／CONFIG／END才控制原型；无需新Gameplay请求。
- **每个显式READ token最多一次枚举**；Show／Copy／迟到ACK只重显该token的字符串，不再扫描。ADVANCE／CONFIG／END回复不自动调用；新右键请求才刷新。只保留最近一份有界报告及token／城市／reference／回合等标量；新请求、关闭／shutdown／load时释放；换城／回合／引用变化在下一次展示或读取时失效，不跨请求保留native实例句柄、owner对象ID表或全局枚举表。正在等待ACK的现有有界update不变，不新增hover／per-frame／每回合Gameplay请求。

### 精确筛选、归属与证据

1. `GameEffects.GetModifiers()`目前只有**全局**枚举先例；每个请求至多调用一次，再按`GetModifierDefinition(id).Id`匹配精确allowlist，命中才取owner／Active／Subjects。不能声称原生只扫描一城，也不能声称外层处理cap能限制原生返回全局列表的初始物化成本。
2. 首轮Writing限定：`HD_AMPHITHEATER_WRITING_CULTURE_BOOST`／Tourism同伴；`SPC_MEANING_PROBE_SCIENCE_1_WRITING`（Science1）、`SPC_MEANING_PROBE_GOLD_3_WRITING`（Gold4）；两个`SPC_MEANING_PROBE_CULTURE_SINGLE3[_SCALE100]_WRITING`。为配置异常／SPLIT残留核对，从Meaning精确16 owned building对应的Writing附件形成有限集合；不使用名称prefix筛全库。0%／hold残留只加Dialogue与GWA精确owned目录中Writing／Culture的附件，不把其余object／yield未扫描说成完整退出已证实。附件选择同时检查`BuildingModifiers`与参数，不复制另一套公式或猜字段。
3. UI先例证实Definition表中的`Id`／`Arguments`，`GetModifierActive`真实API按boolean使用；owner需`GetModifierOwner`＋`GetObjectsPlayerId`＋`GetObjectType`＋限长`GetObjectString`。**B156首版实例城市归属UNKNOWN**：与所选城市header分开，foreign过滤只靠确认玩家ID，不靠名称。HD City字符串仅注释先例，本次未观测；禁止宽松抓数字、以内部objectID代替CityID。B156实测owner为District，B157按用户授权只解析该完整格式，交叉核对当前CityManager/该城FindID区域/区域父城/full reference；本城、其它城、UNKNOWN分别报告。新映射在B157所见三个District对象已native确认；其它格式仍UNKNOWN，不能据raw或名字单独归组，不引入新cityKey。
4. `GetModifierSubjects`按实证区分nil、空数组、有限对象数组和错误；只有实际数组才计数／取有限类型描述，不递归探测。B157每实例最多3个subject的玩家/类型/raw与同样District核对；非已观测格式保持UNKNOWN，余项标未展开，请求内标量缓存复用对象读取。不调用仅有注释的TrackedObjects。Active true只是该API结果，不自动等于owner／subject requirement满足、精准recipient、叠加或收益结算PASS；如诊断确需requirement层，先核对现源码的具体接口，再定域扩展，不能猜方法。
5. 成功S/G是正控制：与Culture用同一reader／归属规则；HD是同yield背景，不能诊断时关闭它。记录具体GreatWorkType／基础Culture、实际building type／Name tag／Locale结果、配置量、HasBuilding／pillaged与作品小计；复用本次已取得的UI事实。若当前OFF不能复用完整四态快照，只读本fixture实际槽位，不新增第二套跨城市采集。

### 有界输出与失败

先显示“API读取完整／不完整；实例城市归属已确认／UNKNOWN”，随后HD＋2、Meaning S／G／C及旧Writing Culture残留的摘要。展开记录精确ID、Arguments的GreatWorkObjectType／YieldType／YieldChange／ScalingFactor、Active true／false／UNKNOWN、owner玩家／类型／限长raw描述、Subjects状态。所有无城市映射的数目标“本玩家匹配实例”，不得写“本城已有／没有”。初版示意（**非实际结果**）：`HD著作＋2｜本玩家命中1｜Active=true｜城市UNKNOWN；Meaning文化＋3｜命中1｜Active=true｜城市UNKNOWN；作品实际Culture4`。

实际后处理上限32768枚举项、64匹配项／每项64 subjects；展示最多12详细实例、单raw字段最多240字节（UTF-8安全截断），其余给计数及截断标记，不倾倒其它Mods完整列表。上限只是处理／输出保护，不是引擎分配预算；溢出明确INCOMPLETE、停止该次读取，不能提高上限凑PASS。任何Definition未读、pcall失败、nil／非数组／稀疏／重复枚举ID或超限，均不作“0实例”；Active非boolean不转换false，Subjects nil不转换空数组。读取前后selected-city／owner／reference／回合／原型配置变化，报告STALE并不配对；没有自动重试、递归扫描或清理效果。

### 本地验证、最小实机与退出

**W0004 L1只读诊断**，附直接UI生命周期范围：syntax／import／exact附件引用、独立返回fixture（nil／异常／类型／稀疏／重复／cap／unknown owner／subjects）、同token Show/Copy零重复枚举、新READ一次、换城／引用变化拒绝、OFF／配置错误仍可只读报告、两城／foreign不误归属、诊断无Gameplay写入。复用直接相关现有测试，不跑旧full／stress；模拟schema只能检验防护，不证明接口原生可用。

**首次原生仅一次读取。** 用户保持现有固定城／著作／建筑／D／Dialogue0%／非主题状态，无需先重做C00/C10或过回合；右键READ并提供一份报告。首轮只验收实际API返回、精确定义／参数、正控制、raw owner字符串和城市映射证据。不可读或无严格同城证明：停止对应结论，记录API_READ_BOUNDARY／TECHNICAL_IDENTITY_BOUNDARY，不要求反复尝试或自动切换其它primitive。

仅当实际schema与严格同城映射通过审阅后，才值得用同城C00→C10→END／READ三态配对：HD应持续存在；Meaning所选候选／S/G进入与退出；旧Writing Culture残留按所扫范围报告。它仍不验收Dialogue100%、主题化、最终结算／冷加载、全部作品或完整L2。附件／活动不符则定位确切挂载；两项均可靠活动但CultureΔ0，只收窄到组合／读取／结算问题，不能宣称覆盖算法已确认或去改系数。所有门禁、条件后备与现B155保留。

B156.183已完成只读实现，18项诊断＋11项原reader定向LOCAL PASS；首次原生OFF读取见[B156两图](../../Status/Validation/Results/Specialization_B156_Modifier_Native_Read.md)，入口及所见schema通过，严格映射/Meaning共存未过；[证据与一次读取](../../Status/Validation/Results/Specialization_B156_Modifier_Diagnostic_Local.md)。当前source/live以Status/receipt为准。B157映射及三态已完成所测范围，生命周期PASS但Culture追加FAIL；下一仅最新原生记录中的宿主差异定域核对建议，尚未实施／授权。不自动重开四态、正式同步后备或进入下一能力。

## 平加共存与主题化技术原型

**历史原型／未来Culture恢复参考。** 两个获授权Culture候选已失败，D0043将两域暂排；以下方案不作为当前五yield的实施或验收要求。

### 定域静态证据

B155原型实施前只读含14 Meaning载体的DebugGameplay：`EFFECT_ADJUST_CITY_GREATWORK_YIELD`共1378 Modifier，1258仅YieldChange、120仅ScalingFactor，同时声明0；GameEffects相关字段NULL、GameEffectArguments0行。HD+2、Meaning1+2、Dialogue TEST100=200共用effect，静态不解释共存算法。当时数据源为配置实际指向的内层Firaxis Cache；外层旧Cache无Meaning，不作为当时依据。本次[显式100结果](../../Status/Validation/Results/Specialization_B155_P0L2B_Scale100_Native_Stopped.md)另只读核对当前内层DB两个候选／14精确附件与参数完整；本轮测试helper未配置DB且未运行。新增mixed参数定义是我们自己的待验证候选，不把原型前“无同族先例”误写成当前DB仍零行或原生算法已确认。

未主动清HD不证明无间接干扰；[B055 flat2→4→2](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)仅证明当时单flat成功；没有槽位建筑／HD实例证据，既不能证明多flat累加，也不能推导Culture平加全不可行。[作者SQL](https://github.com/Feofilakt/YAGM/blob/main/Moksha.sql)仅有单独YieldChange3，不能证明mixed参数。显式100没有同effect双参数先例，作为候选不得提前宣称可隔离。

普通艺术／考古馆当前yield/Tourism主题倍率各100，但资格分别不同artist／同art类型、不同civ／同era。Oxford两Writing、HD广播／电影／云韶条件不同，不能类推。[B059 Oxford主题实测](../../Status/Validation/Results/Specialization_B059_Theming_User_Result.md)仅当时C/T读数，不是Meaning。原B154 reader明确拒绝themed=true，不得将该入口限制写成native不支持。

### 最小原型与门禁

保留现有SPLIT1+2控制，新增单一Culture3省略ScalingFactor及单一Culture3显式100两候选；其它字段／七objects同范围，S/G编码不变，不造完整新目录。候选仅每件Culture3，非3提前拒绝且不hold旧收益。单一3若成功先测Dialogue，仅失败时用显式100排因；基线必须恢复，显式100压掉Dialogue不能native-only PASS。

fixed追加合同要求：Meaning在0%／100% Dialogue下均ΔA×W；Dialogue在有／无追加下原生增量相同且本身有响应。主题fixture同样ΔA×W，不乘theme；若读到2倍只登记该场景失配／未来可用事实，不推断唯一原因或正式改Design。不同配置、主题／作品／位置／D／回合等不能共享旧配对。

UI按需可靠theme boolean、分建筑小计与S/G/C实际差值；缓存最多4组，结束释放，错误／未知不记成功。普通计算不构造UI明细，不增加hover／per-frame Gameplay请求。单selectedvariant为session状态，OFF切换无收益写入、重复token幂等；配置按钮右键直接复用End撤销，不推进100%实验，原验证按钮右键仍只读；load默认SPLIT/OFF并清16精确项，confirmed loss由已有module-owned路径退出，UNKNOWN不扩大清除。永久Property／账本、其它城市／HD和现GC不动。

当前原型改Model/Probe/SQL及已有Gameplay请求、UI读取与一配置按钮、本地化、build标识；测试是对应直接L2与loss/load L3，不做全历史／stress。[B155结果／短测](../../Status/Validation/Results/Specialization_B155_P0L2B_Flat_Theming_Prototype.md)记录本地数量及真实原生结论；模型或carrier配置不是native证据。

### 停止与未来方向

用户较早提出theming放大全部作品追加，最新决定暂不采用；技术原型保留响应／参数／失败／退出档案，未来用户更改Design时再利用，不丢掉反证也不提前接受旧候选。当前候选失败先退出；两个获授权flat候选均失败时停止该primitive；Dialogue/theming无法隔离则只过确实成立的门禁，报告限制，不补差／减K／改Floor或以整城发放代替。

没有可靠source-origin过滤参数；同类型作品定义基值异质，不能正式把Dialogue统一改成同类+2。未知recipient、其它三yield及正常结算仍独立；单城受控拒绝未知作品不是正式精准排除方案。技术原型完成后停止等待用户验收；不自动接正式能力／其它批次。

## 已授权切片 — P0-L2B门禁原型

**D0042/B152–B157当时授权记录。** 当前D0043七域计划见上方P0-L2C；本节不授予新实现、不恢复旧Culture候选或全局cutover。

**Scope。** 逐领域整数模型及单城原生文化追加/倍率四态；默认OFF，仅一个fixture。已有Science/Gold整数复用；Culture原1/2/4/8片段保留，B155追加两个single3对照；不创建其它三yield writer。当前规范九领域计算，Shared/K接口不改。未知对象保护不升级为正式规则。

**精确旧效果。** GWA自身156项只暂停本城；Dialogue自身0/TEST100替换只绑定owner/city/full reference，不使用off[player]。四态C00(0/0%)→C10(追加/0%)→C11(追加/100%)→C01(0/100%)→OFF。结束先确认Meaning16项清除，再Dialogue自身实验退出及正常当前AUTO，最后GWA正常当前样本恢复；失败保持stopping/hold，禁止早恢复。没有全局关旧Dialogue或退休K producer/ACK。

**有效比较。** 本城ACTIVE4、已确认支持／主题状态可靠的馆藏、正整数Culture追加，领域D/作品/位置/其它修正固定；比较两次追加差值是否都为A×W。原生Culture定义读取与HD当前平加区别保留；不假定该primitive天然隔离。右键只读更新本阶段UI记录，旧阶段不回填；四态记录最多4组，随结束/引用/回合/人口/当前资格/集合/D变化释放或失效，不写Gameplay权威。

**更新、资源与边界。** 本城明确动作、当前馆藏/D/ACTIVE/ref变化；同输入零写、同回合变化响应。复用现有Shared/K输入，Dialogue scoped Audit只读本城。普通计算不扫描巨作槽位/构造诊断副本；UI原生扫描只在按需request，没有per-frame/hover请求或GC改动。明确动作期间重入只标记一个定域deferred，成功后一次核对；失败恢复意图，不重放native快照。UNKNOWN保存holder，配置/健康未确认不采成功读数。无关transfer/return可失效样本但不解除本城override；confirmed loss先owned退出，加载默认OFF、不重放永久/临时快照。非加载兜底不得清其它已ready城市。

**本地验收。** W0004 L2 +直接触及loss/load的L3定域断言；既有B154 61实际Lua/SQL及26K范围保留；B155新覆盖见结果，逐领域Floor反例和撤销失败/幂等/两城隔离/UNKNOWN/冷加载/延迟UI/native配置健康覆盖。只读DB副本，未跑历史full/stress；现有版本/外部事实不由模拟升级native PASS。

**退出与后续。** 本单城native对照完成后记录结果，或第一个失败停止对应路径。精确recipient未解决不伪造资格PASS；Culture若被放大不减系数/补差/整城补贴/全局关旧对话。只有可靠接口及另行完整计划授权后，才正式六yield/all-city cutover。当前检查点不授权L3/M/N/U2、AI/MP、永久schema、目录扩展或GC调参。用户此时无需新设计决定；native一次短流程见证据页。

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

当前D0043仅在D0042上暂排意义延展Government／Diplomatic；逐领域Floor继承D0038，固定追加继承D0041，其它资格／生命周期保持。上方L2A no-rounding与P0-L2B九域为当时历史合同。

只接Culture ACTIVE4的意义延展；每件合格巨作，逐领域追加：

`shares_d = meaning_K × D_d`；`yield_per_work_d = floor(shares_d × share_value(yield_d))`。

meaning_K=0.5为初版参数；金币一份=3，其它普通产出一份=1。每领域换算为实际产出后分别Floor，再同产出相加，最后乘W；同领域多个区域按Shared最高单区域D，不合并D；D是绝对深度cap10，不按规则环境归一化。不要求该领域成为本城Identity，不以工作专家数/人口/作品时代数代替D或件数。

| 领域 | 代表产出 | 对L3的GPP映射（不在L2发放） |
|---|---|---|
| Campus | Science | Scientist |
| Industrial Zone | Production | Engineer |
| Commercial Hub | Gold | Merchant |
| Harbor | Gold | Admiral |
| Encampment | Production | General |
| Holy Site | Faith | Prophet |
| Government Plaza | 本版暂不参与Meaning | 无 |
| Diplomatic Quarter | 本版暂不参与Meaning | 无 |
| Neighborhood | Food | 无 |

不包括Theater自身。完整作品资格只复用K的已支持七类/历史时代目录；Relic、Product、Wonder及未知定义排除。普通建筑完工/未掠夺、免费/特色及缺Tier规则按Shared；不使用旧BASE相邻、旧Actual复制或额外填值。例：Campus D10→每件5Science，Industry D6→3Production，Commercial D3→floor(4.5)=4Gold；不先按份额Floor，也不先合并Harbor。

Meaning是追加产出，未来Dialogue只放大作品原生产出，**不得放大本项**。D0041要求Dialogue／theming均不放大追加；其它倍率不类推，实际路径仍须组合核对，不能借配置读数替代回合入账。

## 已有实现与可复用部分

`GreatWorkAdjacency.lua/Model`当前读取全部完成专业区域的BASE向量，借Dialogue样本挂`BUILDING_SPC_B060_{yield}_{P/N}{0..12}`，SQL为七类GreatWork的±0.5二进制YieldChange。它仍是旧效果，不符合D输入。模块有精确owned撤销及E2 exit/return，能复用writer/退出结构；旧公式不能保留补空缺。

`GreatWorkFacts`已有confirmed作品/件数，`DistrictCompleteness.Read`已有D及单区域选择。新例程取必要小型输入；不构造整份诊断、国内来源或第二套区域/槽位枚举。

原生分类Modifier只按GreatWorkObjectType限定，不直接按K支持的具体work type限定；**未知同类Mod作品可能误受益**，需处理到一致，不能将UI排除当成效果排除。

## 最小接口门禁及停止条件

1. **精度：** B151所测S/G半点失败、整数追加可用；D0038明确逐领域Floor，不重复该小数实验，不外推其它能力。Production／Food／Faith须新原生整数证据；Culture组合延期，不再作为当前门禁。
2. **资格：** 一件已支持作品与同类别未支持定义作本地/native必要对照；禁止“目录数正确但全类Modifier仍影响排除作品”。路径若无法限定，停止并报告具体primitive边界。
3. **隔离：** 同城同时配置作品native倍率与本项附加值，验证Dialogue百分比不放大追加。先静态/模拟划清attachment与origin，再给一次最小原生对照。各yield／主题化证据不得互相外推；当前无Culture输出，不要求重复已失败Culture四态。
4. 原生路径不满足时登记TECHNICAL_INVESTIGATION_REQUIRED；备选不同primitive可以调查，**只有D0038明确的逐领域Floor许可；不得换取整位置或外推其它能力；不能改系数、造补偿永久账本或采用整城补贴**。真正需要改Gameplay才交用户决定。

在全部门禁可表达前只做后续获授权的可逆接口probe，不宣称L2完成。此前计划轮没有运行原型；B150/B151 L2A现已取得上方所列原生精度结果，不把S/G范围扩大为资格/native-only通过。

## 实施切片与旧writer退出

- 第一步纯模型：同一次Shared快照→每领域D与份额→每件各yield值；记录资格/UNKNOWN，模型不用旧DialogueModel的作品时代判断。原L2A测试保留精度；模型现按D0038逐领域Floor处理；正式writer仍待资格/native-only门禁及另行授权。
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

后续当前实机流程以上方P0-L2C为准：按已确认逐域Floor比较整数五yield，件数变化与退出／冷加载；不再选择半点重复旧精度实验。其余独立门禁仅按真实依赖补测。接口失败第一项即停。具体流程在probe包就绪时固定，不现在要求用户另做。

诊断先显示`合格W件｜每件Science/Gold…｜D来源｜预期/实际配置｜已确认/待核对`，组成分页；不以“已挂carrier”宣称原生收益通过。

Exit：精度/recipient/native-only门禁、精确cutover和本地范围通过，再由用户确认原生对应场景。逐领域Floor精确口径已由D0038正式同步并在D0041保持；资格/native-only/theming技术门禁仍开放，不因此获得完整L2实施授权。

来源：[Culture正式Content](../../Design/Content/Culture_D0043.json)、[Shared](../../Design/Content/Shared_D0035.json)、[总cutover合同](D0032_Implementation_Plan.md#明确的旧效果切换责任)、[旧加值实现/限制](../../Reports/Technical/Specialization_B060_GW_Adjacency_Implementation.md)、[B055整数实机范围](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)、[精度待办](Yield_Precision_Backlog.md)。
