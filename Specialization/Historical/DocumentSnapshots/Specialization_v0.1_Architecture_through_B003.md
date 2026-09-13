> HISTORICAL / SUPERSEDED — 审计快照，不作为当前规则。

> **最新 B003 / B002 用户验收**：Read routes (UI) 已获 USER_GAME_TEST_PASS：三条现有路线端点、保存读档后读取；新增第四条后，同城两条出站可分页。此前 Gameplay 新建路线事件捕获另项通过，临时历史不跨读档。B003 只优化显示（城市名优先、明确本城条数、ID 次要），本地模拟通过；正式 Gameplay 权威网络恢复仍未解决，不将 UI 快照通过外推为网络结算通过。当前记录见 Specialization_P0_B003_Readability.md。以下版本说明按历史理解。

> **B002事件证据更正**：用户实测通过的是Gameplay新建商路活动事件的起终点捕获；不是UI出站枚举。读档清空临时日志已观察到，不能把事件历史或其简单持久化视为当前有效关系。完整网络恢复需有效性/撤销/稳定身份与初始状态方案。UI快照单独待测；不依赖用户打开面板才运行网络。NativeDistrictCopyBasis等最新设计不变。

> **最新用户设计澄清**：Actual指煤电厂/大酒店原生区域产出复制口径；以NativeDistrictCopyBasis命名，不能用GetAdjacencyYield定义替代。Base能力不变。此前B002对固定行业收益的预先排除已撤销，按原生复制行为验收。B002运行包与商路测试不变。

> **B002边界更新**：UI Base/Actual及相邻政策区分已用户通过；行业固定区域产出ADJUST_YIELD_CHANGE不是相邻，不擅自纳入公式。大酒店/燃煤电厂的Building_YieldDistrictCopies属于独立复制产出通道，具体复制基数仍需单测。Gameplay city:GetTrade缺失已用户确认，现分别验证UI出站列表与Gameplay TradeRouteActivityChanged；尚无已验证全量权威路线恢复，网络结算不能依赖打开UI。详情Specialization_P0_B002_Findings.md。

> **当前运行包P0-B-001**：已有Governor/Specialist通过项保留，新增UI相邻候选与Gameplay商路原始端点两条独立只读路径。UI相邻采样不派发Gameplay、不作为权威结算输入；其Gameplay可用性仍待独立验证。每次单区/单路分页、标识上下文、缺失值Unknown、不展开引擎对象。商路rawCount不能代替去重recipient N，所有sqrt及future scope约定不变。当前用户步骤见Specialization_P0_Batch_B001.md。

> **用户确认补录**：城市原生总督2/3/4阈值随晋升正确激活，调离后为0/0/0，登记USER_GAME_TEST_PASS；不再重复测试。属性判定必须显式比较数值（本探针为1），不能用Lua真值判断0；nil和0均是已观察到的未激活表现。结合新局存在/建立测试，可作为后续城市Active门控依据；正式专业/网络机制尚未实现。

> **A007新局实机结果**：用户确认control=1，无总督其它字段nil；派遣后present激活、未建立时established=nil，建立后established=1。上述子项USER_GAME_TEST_PASS。旧存档未加载新增效果的解释得到新旧对照支持，暂不做强制迁移。新局头衔门槛与迁移撤销另验，尚不宣称完整Active机制通过。后续步骤见Specialization_P0_A007_NewGame_Result.md；运行包仍A007。

> **A007证据边界更新**：已观察本城Req2/3随升级响应；新增control缺失时不判定present/established。优先排查旧存档对新增trait效果的实例化。全国高阶总督计数不得作为城市Active Level依据；印加事件账本仅备用，需要另维护城市驻扎与建立状态、迁移撤销及历史初始化。详情Specialization_P0_A007_Result_Analysis.md。

> **A007当前Governor实现约定**：Gameplay不再调用城市/玩家GetAssignedGovernor（均用户确认ABSENT）。优先通过原生HAS_GOVERNOR（Established=0/1）、WITH_X_TITLES（2/3/4，Established=1）驱动独立城市属性供显示与后续Active门控；加载control缺失时Unknown。确切晋升历史不由这些阈值反推。帕查库特事件账本仅作历史记录先例，不当作存档通用查询。原生效果刷新/撤销仍需用户实测；详情Specialization_P0_A007_Native_Governor.md。

> **当前A006**：A005区域/专家读取已用户确认通过；城市对象GetAssignedGovernor缺失，改测玩家Governor管理器的GetAssignedGovernor(city)。官方UI先例不等于Gameplay验证，Governor仍需用户实测。其余最新平衡规则和实现范围不变。

> **运行包A005**：根据A004用户错误截图修正区域枚举，单次Read自动显示已返回结果；不恢复全量采样。当前用户步骤见Specialization_P0_A005_Reading_Fix.md，其余最新平衡设计不变。

> **当前运行包A004**：恢复的是独立、手动触发的Governor与Specialist只读探针，见Specialization_P0_Batch_A004.md；完整快照和自动采样继续停用。A1/A2已用户通过；新接口仍USER_GAME_TEST_REQUIRED。标题计数为候选值，原生Req2/3/4必须实测对照，不据此提前宣布高级等级机制完成。以下A003暂停说明保留为历史。

> **A003结果更新**：用户已确认单城marker读写及重新加载后不变，登记USER_GAME_TEST_PASS；Clipboard交付失败单独记录。城市Property继续作为状态存储首选；隐藏建筑仅作为可选数据库效果适配/备用实现，不引入双重权威状态。具体取舍见Specialization_P0_Marker_Storage.md。下方A003待测说明属于更新前历史。

> **P0-A-003运行范围修订（A2用户故障回报后）**：A1为USER_GAME_TEST_PASS；旧Mark卡住为USER_GAME_TEST_FAIL。为隔离故障，当前运行包只连接单城marker读写，停用完整快照、自动采样和首次专业历史标记；Governor/Specialist面板采样暂停。宽泛Probe函数仅保留研究用途，恢复前需分模块修订。此变化不修改R3最终机制设计。A003实机状态为USER_GAME_TEST_REQUIRED；当前测试以Specialization_P0_Batch_A.md为准，旧流程不得继续。

# 城市专业化文明 v0.1：架构 R3（R2机制＋独立测试文明＋用户实机验证）

初查日期：2026-09-09（America/Vancouver）。状态：R3；机制沿用已确认R2，新增Scotland展示模板与用户负责实机验证的工作方式。

本版本以用户最新16项要求为准。旧报告留存 DevelopmentBackups/Specialization_Architecture_R1.md，仅为历史。已确定：一条分发商路传播所有接入网络；折扣10/20/30/40%；五档项目生成施工队；超额施工力丢弃；文化三类GPP各+2；旧作采用隔离的城市基础补贴。所有需要实机且尚无用户结果的接口标 USER_GAME_TEST_REQUIRED。P0只分批建立探针、最小实验和日志，不一次实现全部机制。


## 实机责任与证据状态（R3，覆盖旧流程）

所有Civilization VI启动、GUI操作与实机验收由用户手动完成。代理只做本地静态/Lua/SQL/XML/数据库验证、mock、源码先例、最小探针与测试说明；本轮完成交付即停止，不等待用户测试。

- STATIC_CONFIRMED：本地文件/数据库/资源引用支持该结论，不等于游戏运行正确。
- LOCAL_SIMULATION_PASS：模拟或隔离数据库测试通过，不等于引擎语义正确。
- USER_GAME_TEST_REQUIRED：尚需用户实机证据，默认运行状态。
- USER_GAME_TEST_PASS：仅用户明确返回该项通过结果/日志后登记。
- USER_GAME_TEST_FAIL：仅用户返回失败结果后登记，并保留配置与日志。
- BLOCKED：缺少具体前置条件无法执行，必须写原因；不把静态未知一律当BLOCKED。

当前没有任何USER_GAME_TEST_PASS或USER_GAME_TEST_FAIL记录。每次只交付3–5项单变量测试；可复用存档就不新开；测试面板输出ID和前后摘要，避免人工复杂计算。

## 0. 工程与证据

初查时工作区没有文明Mod，R3现已新增独立测试文明。保留的历史诊断工程为 `Sid Meier's Civilization VI/Mods/CityGPPProbe/`：

- `CityGPPProbe.modinfo`：只读诊断，ImportFiles + AddUserInterfaces，AffectsSavedGames=0。
- `UI/CityGPPProbe.lua/xml`：读取城市、区域、专家、全国 GPP 和运行时效果。
- `UI/GPPAccounting.lua`、`GPPDiscovery.lua`：效果分类、参数/对象解析、数据库指纹。
- `DevelopmentReports/Generic_GPP_Inventory.md`、`DevelopmentTests/`、`DevelopmentBackups/`：先前调查、模拟测试与备份。
- 初查搜索未发现AGENTS.md；当时没有自定义文明数据库，R3已在SpecializationP0/Data与Config中补建。

已有工具可继续用于观测，但不作为新文明的依赖，不把 UI 估算器改造成规则引擎。旧报告中的 Expert VERIFIED 仅适用于旧指纹；其城市百分比等结论本来就有未验证项。

本轮只读查询的较新数据库：

`Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`

- 修改时间：2026-09-09 18:31:51 -07:00。
- Modifiers：16,623 条；旧报告为 13,980 条，规则集已变化。
- SHA-256：`ce1bb69809c61acd63272db4b98182b51ddad8b64694a45fb5490109aecf3f92`。
- 根目录另有 2023 年缓存，14,972 条 Modifier；未将它混入当前规则结论。
- 缓存反映某次加载结果，不能保证等于下一次启动的配置；实现前必须输出新局规则指纹与启用 Mod 列表。

本地源码根目录：

- GAME：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/`
- HD：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/`

证据索引（路径相对上述根目录；是调查对象，不是需要 include 的依赖）：

| 编号 | 源码/数据 | 直接支持的结论 |
|---|---|---|
| S1 | GAME `Base/Assets/Gameplay/Data/Schema/01_GameplaySchema.sql`；实际 sqlite schema | 专家 yield/GPP、建筑专家收益、巨作、建筑相邻复制等表的结构 |
| S2 | GAME `DLC/Expansion2/Data/Expansion1_Policies.xml:1896`；缓存 RequirementArguments | 存在 `REQUIREMENT_CITY_HAS_GOVERNOR_WITH_X_TITLES`，现有用法有 Amount、Established |
| S3 | GAME `DLC/Expansion2/UI/Additions/GovernorPanel.lua:56,324`；GovernorSupport.lua | 全国已花头衔接口与按 GovernorPromotionSets 查询 HasPromotion 的区别 |
| S4 | GAME `Base/Assets/UI/CitySupport.lua:648`、`AdjacencyBonusSupport.lua:198` | District:GetAdjacencyYield 与 Plot:GetAdjacencyYield 两种调用 |
| S5 | HD `UI/Additions/HD_Utils.lua:422`、`UI/Replacement/RealModifierAnalysis.lua:994` | HD 使用区域相邻接口；报表实现区分 modified 与 plot raw 候选值 |
| S6 | GAME `Base/Assets/Gameplay/Data/Civilizations.xml:810,2297`；缓存 Modifiers/Arguments | 原生中国特性绑定科技/市政 boost；缓存仍有两个 +10 的定义，但对应中国 trait 关联已被当前规则改动 |
| S7 | GAME `Base/Assets/UI/TradeSupport.lua:17`；HD `UI/Additions/HD_Utils.lua:1234` | 实际出站商路列表；不能用交易站存在替代活动商路 |
| S8 | GAME `DLC/BlackDeathScenario/Scripts/BlackDeathScenario_StateUtils.lua`；HD `Gameplay/HD_StateUtils.lua:51` | 官方剧本的 UI 请求 Gameplay 执行模式，以及对象 Properties 状态模式 |
| S9 | HD `Gameplay/HD_Common.lua:307–350`；`UI/Additions/HD_Utils.lua:7,25` | 当前建设目标、实际成本/进度读取、AddProgress，现有实现会裁到剩余成本 |
| S10 | HD `UpdateDataBase/DL_GreatWorks_YieldChanges.sql:5,76`；实际 GreatWorks/YieldChanges | HD 有作品类型×时代产出曲线，最终写入原生巨作表 |
| S11 | HD `Gameplay/BinaryCompress.lua:6`；`UpdateDataBase/HD_Last.sql:51` | Lua 写 plot property + 原生 property requirement + 常量 Modifier 的动态桥接先例 |
| S12 | 实际 DynamicModifiers、Building_YieldDistrictCopies、ModifierArguments | 科技/市政 boost、城市加法百分比、指定建筑购买折扣、煤电厂相邻复制能力 |

另查阅了作者公开的 [Better Report Screen 源码](https://github.com/Infixo/Civ6-Better-Report-Screen/blob/main/RealModifierAnalysis.lua)，其区域读取实现也区分 District 与 Plot 相邻值；它是实现参考，不是对所有 Mod 环境的语义保证。

## A. 整体架构

以Gathering Storm为v0.1规则目标，Scotland展示资源还要求Rise and Fall。核心不硬依赖HD。当前包名为 **Scotland (Specialization Test) + P0**；独立ID已固定为CIVILIZATION_SPC_TEST / LEADER_SPC_TEST，trait为TRAIT_CIVILIZATION_SPC_TEST。玩家可见名为Scotland (Specialization Test)、Robert the Bruce (Test)，城市名/能力/加载文本均标Test。

模板只复用官方Scotland文明图集、Robert领袖图集/静态加载前景与背景、白蓝配色。自建最小Config Players、Gameplay Civilizations/Leaders、LoadingInfo、图标别名和文本；不改原版文件/记录，不复制原版LeaderTraits/CivilizationTraits/PlayerItems，不继承LEADER_ROBERT_THE_BRUCE（仅LEADER_DEFAULT）。没有原创美术或独立外交3D ArtDef；3D动画与完整语音不作为这一最小身份验收的承诺。

此前只有DEV探针，没有可选文明，因此新身份验收需要首次新局，不能将旧Scotland存档改名充当新文明。之后复用测试文明存档。UI入口、读取快照、Gameplay请求和后续能力均校验双ID；非Test文明拒绝运行，原Scotland保持原状。

本地SQL已在隔离数据库执行并对照官方asset引用；菜单可见、开局、图像渲染、存档身份均USER_GAME_TEST_REQUIRED。详细证据和用户步骤见Specialization_P0_Status.md、Specialization_P0_Batch_A.md。

四层分工：

1. **Database**：文明定义、参数、四专业映射、Requirement、常量 Modifier、施工队项目与单位、建筑 tier 适配表。
2. **Gameplay Lua**：唯一权威状态；处理区域首次完成、Settler 行动、专业潜力、网络、施工队消费与效果刷新。
3. **引擎效果层**：住房、基础 yield/GPP、城市百分比、boost、购买折扣由原生效果结算。Lua 算“应有多少”，引擎算“怎样受现有规则影响”。
4. **独立 UI context**：两个行动入口和简单城市/网络状态面板。UI 发送动作与对象 ID，Gameplay 重验；不替换 UnitPanel、CityPanel、TradeOverview。不依赖打开面板才结算。

重要的前置技术验证：多个只读接口在本地样例中出现在 UI 环境，HD 通过 ExposedMembers.Utils 桥接。必须分别探测 Gameplay/UI 的对象方法和结果，不把 UI 可读当成 Gameplay 必然可读。优先纯 Gameplay；不得以本地玩家画面状态驱动全国模拟。自己的只读桥接若确实必要，应独立实现、显式区分已加载/失败/未知；多人同步另设验收门槛。

### 动态数值写回方案

运行时数据库不是任意改数值的实时存储。`AttachModifierByID` 只能引用已定义效果，不能假设能给实例任意传 Amount，也未找到可依赖的通用 RemoveModifier API。

首选：事先定义常量效果，通过自己的 plot property 位和 Requirement 切换；用城市中心 plot 作效果门控输入，城市 Property 作永久事实。新建自己的 DynamicModifier 组合并核对 Collection/owner/subject，不依据 ModifierType 名字猜作用域。应先做一个 +1 Science 开/关最小实验。

动态量可拆成固定精度二进制位，效果按 0.5、1、2、4…组合；GPP/百分点用整数通道。每个效果只挂一次，反复刷新只切位，既能增加也能归零。父级尽量从 trait 自动建立，避免每回合 Attach 形成永久重复。plot→city→player 的关联必须在 P0 实测，不能复制 HD ID 作为实现。

有限位宽只是工程表示范围，不能变成平衡硬上限。记录范围与精度、检测超范围并明确报错，绝不截断/绕回/沿用旧值；在压力测试中按目标规则实际规模扩展。boost 超过100的无效部分可以由完成成本自然裁切，但要核验引擎 overflow。

若 property requirement 对所需作用域不可靠，备选是少量内部建筑承载可移除的效果；新增建筑会被其他 Mod 的“每建筑”统计误计，故不能轻率用数百个 dummy building 作为默认方案。

## B / C. 逐项实现与难度

Easy = 已有直接数据/效果，局部工作；Medium = 常规 Lua 状态和桥接；Hard = 多机制/上下文/数学语义需要试验；Possibly impossible = 原设计的完全通用精确语义尚无可靠公开接口路线。下表难度不等于已通过运行验收。

| 机制 | Database / Modifier 路线 | Lua | UI | 难度与主要风险 |
|---|---|---|---|---|
| 独立文明/领袖、trait 生效范围 | 原生配置与 Civilization/Leader/Trait 关联 | 初始化玩家范围 | 原生选文明入口、占位图文 | Medium；美术配置与他文明能力隔离 |
| 首个四类区域锁定专业 | DistrictReplaces 归一化；四类映射 | 完成事件后检查 IsComplete，第一次写入 | 显示类型 | Medium；放置不算完成、征服/开局历史 |
| 默认潜力1、烧Settler提升至4 | 参数与单位类型识别 | 验证己方城市中心、单位存活/所有者/行动条件、潜力<4；消耗一次 | 必须有行动入口 | Medium；重复命令、单位ID复用 |
| 总督激活高级等级 | `REQUIREMENT_CITY_HAS_GOVERNOR_WITH_X_TITLES`，Established=1 | 读取驻城、建立状态、晋升；派生有效等级 | 潜力/激活分开显示 | Medium；头衔与晋升树层数不是同一概念 |
| 首都/商业专业贸易中心身份 | 首都集合可辅助 | 当前首都与专业派生 | 身份标记 | Easy；迁都规则待采用当前首都 |
| 科研/文化/商业Lv1 +3F3P；Lv3提升到+5F5P | 优先独立内部区域建筑 + `Building_CitizenYieldChanges`；Lv3仅增加+2F2P | 按专业/等级创建移除承载建筑 | 显示每专家加成 | Medium；不能全局改 District_CitizenYieldChanges；内部建筑计数副作用 |
| 工业Lv1 +3F；Lv3提升到+5F | 同上，只写 Food | 同上 | 同上 | Medium |
| Lv2区域本体与每级建筑+1住房 | `EFFECT_ADJUST_DISTRICT_HOUSING`、`EFFECT_ADJUST_BUILDING_HOUSING`；按有效等级门控 | 建筑组/健康状态辅助 | 简单明细即可 | Medium；同tier多建筑如何计数见下文 |
| Lv2每专家+2 base GPP | `EFFECT_ADJUST_DISTRICT_GREAT_PERSON_POINTS` 的城市/区域限定组合 | 读取真实专家数，输出额外2×S | 独立诊断 | Hard；基数位置、城市/全国GPP百分比、旧规则倍率 |
| 科研/文化Lv3 0.5×人口×专家基础yield | `EFFECT_ADJUST_CITY_YIELD_PER_POPULATION` 或 `EFFECT_ADJUST_CITY_YIELD_CHANGE` | 专家系数或直接基础量；保留0.5精度 | 显示公式 | Medium/Hard；参数小数与人口刷新时机 |
| 科研/文化Lv4 每专家+5个百分点 | `EFFECT_ADJUST_CITY_YIELD_MODIFIER` | 5×S门控动态值 | 显示百分点 | Medium；必须进入同一城市加法层 |
| 科研Lv4 其他专业区域实际相邻多yield总和×50%→Science | 城市基础Science效果 | 对每个合格区域、每个原生Yields条目读取实际相邻候选 | 调试对照表 | Hard；任意Mod完整来源归因可能无法保证 |
| 科研网络额外Inspiration百分点 | `MODIFIER_PLAYER_ADJUST_CIVIC_BOOST` | 按实际接收城市集合去重，k_R×ACTIVE L×sqrt(N)，效果适配另验 | 网络状态即可；原生提示兼容需测 | Medium/Hard；触发时机与100% overflow |
| 文化网络额外Eureka百分点 | `MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST` | k_C独立；同样使用接收城市集合与sqrt公式 | 同上 | Medium/Hard |
| 文化Lv4旧巨作基础值随时代升级 | 表可读；R2已选择按城市基础差额补贴 | 作品枚举、目标曲线、差额统计 | 差额说明 | 城市补贴 Hard；不要求修改物件intrinsic值 |
| 文化Lv4每件巨作获得各类base adjacency×50% | 基础城市yield效果可以实现数值补贴；不能直接等价于作品底值 | 本城作品数×各类base adjacency×0.5 | 说明归属与主题化差异 | 城市补贴 Hard；不要求修改物件intrinsic值 |
| 施工队项目/生成/消耗 | 五档固定城市项目＋项目生成的平民单位；工业Lv1可执行 | 项目完成一次生成；固定规格Property；AddProgress(min(charge,remaining)) | 行动显示注入与浪费 | Hard；项目重复完成、事件重入、真实成本、超额不得进入下一项 |
| 工业Lv1/3每专家获得IZ base adjacency锤 | 基础Production效果 | 100%×B×S，Lv3仍不增加系数 | 公式明细 | Hard；base读取与专家来源语义 |
| 工业Lv3每专家获得2×IZ base adjacency金币 | 基础Gold效果 | 2×B×S | 同上 | Hard；同上 |
| 工业Lv4实际IZ相邻锤50%输出 | 接收城市基础Production效果 | 精确源相邻值、网络接收关系 | 接收来源 | Hard；不读城市总锤，不产生区域相邻回写 |
| 工业Lv1开始标准化建筑 | 自有BuildingTier表与可选HD数据映射 | 建筑完成写入源城已学会tier | 模板清单 | Medium/Hard；不存在通用Buildings.Tier列 |
| 已联网城市指定建筑金币折扣 | `EFFECT_ADJUST_BUILDING_PURCHASE_COST`，BuildingType+Amount；保留原购买资格 | 对该城该建筑选择已接入模板的有效折扣等级 | 使用原购买按钮 | Medium/Hard；金币/信仰区分、其他折扣叠加需测 |
| 商业Lv3每种已接入网络每专家+2对应yield | 基础城市yield或内部专家建筑组合 | 对Research/Culture/Industry去重，只计种类 | 三种网络标记 | Medium；不按来源城市数量倍率 |
| 商业Lv4自动接受所有已接入网络 | 复用网络效果 | 每种网络增加中心自身接收记录；不授予本城专业能力 | 免费接收标记 | Medium；与真实路线重复计数的规则需明确 |
| 完整有向贸易网络 | 条件效果按中心与接收城门控 | 活动商路枚举、中心network set、来源去重、撤销 | 中心网络集合及接收城市表 | Medium/Hard；无需逐路线assignment，事件与多人确定性仍需验收 |

### 专家收益的两种落地方式不能混淆

`Building_CitizenYieldChanges` 确实存在，当前工厂/大学/研究实验室都有条目。它让引擎按实际就业人口结算，优于每回合补粮补锤。但局部启停需要内部建筑或另一种实测通过的载体；内部建筑必须0槽位、0成本收益、不可正常购买/生产、不入标准化与住房计数。即便如此，第三方无条件统计所有建筑时仍可能受影响。

备选“Lua统计S→城市基础补贴”可保留大部分城市数值，却可能不影响市民AI对专家岗位的边际估值，也不能保证被专家专用倍率再次作用。若采用此方案，必须写清楚，不能称为完全原生专家增益。工业专家的动态相邻锤也有同一来源语义问题。

禁止每回合直接 ChangeGoldBalance / ChangePointsTotal / 添加科技文化进度来冒充基础产出；这些绕过正常倍率层与每回合面板。

### Theater伟人关系：已查到当前数据

当前 District_CitizenGreatPersonPoints 中，Theater 同时有 Writer / Artist / Musician，各名义2点/专家；Campus Scientist、IZ Engineer、Commercial Merchant亦各2点。

建筑自己的伟人基础点是另外一层：当前圆形剧场Writer+2，艺术博物馆Artist+4，广播中心Musician+4；电影制片厂Writer/Artist/Musician各+2；额外HD/JNR建筑也有条目。不能按专家在哪级建筑的槽位工作，再把建筑点与专家点混算。

文化Lv2已正式确定为每专家给Writer、Artist、Musician各额外+2基础点，总额外6点。新局用0→1→2专家、无倍率/有总督/有政策对照验证。旧报告出现过名义2、实际增量4的情况；不能直接把新增2统一乘2，必须验证新增效果本身的基数位置。

## 总督与永久等级的准确口径

推荐持久状态：`PotentialLevel` 初值1，上限4；`SpecializationType` 在首次完成目标区域时从未定变为四种之一。尚无专业区域也可以投资Settler，只存潜力，不凭空授予任何专业能力。

有效等级：无已建立总督时为1；否则为满足潜力与头衔门槛的最高等级。建议把门槛参数化为 `GOVERNOR_TITLES_L2=2 / L3=3 / L4=4`，任命算1；这些是初始建议，不是已经确认的最终门槛。总督树上的 Level/Column 表示布局与晋升层级，不是累计花费。

引擎 Requirement 是优先事实依据，Lua的显示/网络等级需要与之对照。用 GovernorPromotionSets 找该总督的所有晋升，并以 HasPromotion(Hash)判断；任命只算一次，多个BaseAbility不得累加成多个头衔。不能使用全国 `player:GetGovernors():GetGovernorPointsSpent()` 当作驻城总督等级。也不能照抄旧报表按 GovernorPromotions.GovernorType筛选：实际该表没有这个列。

免费晋升、重做晋升树、秘密结社与自定义总督会使“拥有的晋升数”和“历史真正支出的Title数”不一致。推荐以原生Requirement认定的拥有头衔/等级为规则含义；若坚持历史净支出，必须从新局起记任命/晋升交易账本，且仍不能自动识别任意Mod免费赠送的来源。这属于语义取舍，不应承诺通用精确花费追溯。

调任/解职/失效时立即关闭Lv2–4门控；潜力与专业不变。重新建立后恢复。只检测“已指派”不够。事件遗漏用回合全量核对兜底，但不能允许结算前长期持有旧高级效果。

## Base与原生区域复制基数：用户确认的收益口径

用户明确修正：设计中写Actual的地方，意图是煤炭发电厂/大酒店的原生复制算法，不是由district:GetAdjacencyYield(yield)定义的狭义API返回。先前“固定行业收益当然排除”的推论撤销，不能因getter没返回就排除用户目标。原生算法是否纳入某分量，由原生复制实测对照决定，也不能反过来假定它包含全部城市产出。

- `BaseAdjacency(city,district,yield)`：仍为基础相邻，候选plot:GetAdjacencyYield(ownerId,cityId,districtType,yieldIndex)；已测UI政策前后通过记录保留。
- `NativeDistrictCopyBasis(city,district,yield)`：设计中Actual的明确内部名称；以Building_YieldDistrictCopies用于煤电厂/大酒店的原生复制基数为行为参照。它不是原建筑已获得的最终产出，也不是将原建筑产出再加进区域；不要求实际先建煤电厂/大酒店才拥有专业能力。
- `ObservedAdjacencyAPI`：原district:GetAdjacencyYield数值降为诊断候选，不能作为NativeDistrictCopyBasis已实现的证明。B001面板BASE_CANDIDATE/ACTUAL_CANDIDATE暂保持原标签以免打断商路测试，后者只是API观测。

Research Lv4：`0.5 × Σ(除Campus及其替代区域外的合格专业区域) Σ(各yield) NativeDistrictCopyBasis` 转为本城Science。Industry Lv4：`0.5 × NativeDistrictCopyBasis(源城,IZ,Production)` 沿既定工业网络向接收城市输出Production。比例、源区域范围、转换目标、网络接收规则均不改变。Industry I/III与Culture IV巨作相邻仍用Base，不受此修订影响。

煤电厂PRODUCTION→PRODUCTION与大酒店CULTURE→CULTURE使用同一原生表；大酒店的独立相邻旅游Modifier不是此次复制参照。优先研究复用原生复制机制，必要时用隐藏载体/等价计算适配，但不得承诺一个表项即可满足全部专业规则。

STATIC_CONFIRMED：当前Building_YieldDistrictCopies只有BuildingType、OldYieldType、NewYieldType，无Amount/比例字段，无显式源城、源区域或目标城市字段。因此50%、多区域合并、跨城分发无法靠在此表新增参数直接表达；需要独立适配。模拟/实测确认之前不擅自改成100%，不使用影响整城的-50%补偿，也不回退到旧getter。

后续隔离原生复制基数测试：同一原生复制建筑、同一城市/区域，比较行业固定产出关闭/开启、相邻翻倍政策前后、真正cross-yield、掠夺/恢复时复制贡献。数据必须隔离其它建筑供电/区域辐射/专家/旅游和城级百分比。若getter与原生复制不等价，应报告缺失项并换适配器，不修改用户收益口径。当前不让用户同时做这批测试，先完成B002商路。

Base系列以相同方法验证政策前后不变。专业区域分类以核实的原生专业区域族、DistrictReplaces和显式审计表为基础；RequiresPopulation仅作诊断依据；具体Government Plaza/Diplomatic Quarter/Entertainment等处理见下方R2分类规则。水渠、社区、市中心、奇观和内部dummy不直接纳入。特殊Mod可改变RequiresPopulation，未知项报出待适配，不能把该字段当绝对定义。Research排除所有Campus替代类型。

防循环：自己的科研转换、文化作品补贴、工业网络只写城市层，不写被采样区域相邻层；先采集全部来源再统一应用效果。若别的Mod建立“城市产出→区域相邻”的回授，单凭排除Campus不能证明无循环，应检测漂移并标明不支持的组合，不用任意截顶隐藏。

若测试证明候选API不覆盖NativeDistrictCopyBasis用户目标，先报告接口、操作条件、缺失分量与对照证据，该功能维持USER_GAME_TEST_REQUIRED；不以Base替代Actual，也不把部分分量冒充完整相邻产出。GameEffects可辅助观测活跃效果、参数与Requirement状态，但不是通用“所有Mod相邻来源求和器”。

## 贸易网络 R2：中心集合，一路全传播

Trade Route Capacity本身就是天然带宽。国内网络分发与国际/城邦/其他国内贸易竞争同一商路容量；不引入额外带宽资源、逐路专业载荷、轮分算法或逐路选择UI。

1. 己方科研/文化/工业专业源城S→己方贸易中心H的活动路线建立直接接入；来源始终保留，以便总督变动、断线和模板变化后重算。
2. 每个H维护派生 `connectedNetworks[type]`，内容为该类型接入源集合及有效等级。Research/Culture的L来自源专业ACTIVE level。多源不同L的代表源/合并规则尚待设计确认，不能沿用逐中心求和或擅自取全国最高L；拓扑保留来源但暂不执行多源Boost合并。
3. 每条有效H→己方城市D分发路线，同时使D接受H当前已接入的Research、Culture、Industry。没有逐路线assignment可保存；同一目的城市可同时进入三种网络的接收集合；Research/Culture的N按每种网络的城市UID去重，不按路线计数。
4. 不递归转发。H→另一个中心也可分发，但接收得到的网络不会因此再次成为下一中心的直接源。科研首都等同时具备源城/中心身份时，同一路线可同时满足直接接入关系与分发关系；每一角色内按真实路线身份去重，不因同一规则重复采样而加倍。
5. 仅活动、端点当前同属该玩家的路线有效；交易站/道路/外国路线不建立网络。枚举Outgoing一次即可，Incoming只作交叉对照，不相加。
6. 首都本身若有科研/文化/工业专业，保留原架构建议的本地自接入；不是一条虚构商路。首都身份按当前首都派生。此处与多源口径均以测试日志显式展示。
7. 失去接入源后，从中心集合删除该来源并重算类型；分发路线不必重分配，接收效果随集合更新。路线结束、掠夺、端点征服、总督调任都需触发重算。

Research/Culture额外Boost百分点统一为 `DeltaBoost = k × L × sqrt(N)`。L为来源专业ACTIVE level（1–4），N为当前实际接受该类型网络的己方城市去重数量。k_R=1、k_C=1，两个系数独立可调。不存在按路线追加百分点或逐中心线性求和。Culture IV、16接收城为+16个百分点；8城为约+11.313708499个百分点。Research IV与Culture III各有相同7个接收城时，分别为4√7与3√7，不是旧28/21。

城市UID必须带所有权/稳定身份语义；同城通过重复商路、多个中心、免费自接收或未来合法provider接入同一网络只算一次。线路数、接入源数、全帝国城市数只作诊断，不能代替N。没有接收城市时N=0、强度=0；断线、失去所有权、源ACTIVE变化、源退出和加载重建都重算。不能把任意拥有路线的城市直接计入。

多中心/多源不同ACTIVE level下如何选L、新公式按何种权威网络合并，是尚未定义的边界。旧Σ中心(routeCount×L)已撤销；也不能改成Σ中心(kL√N)绕过递减。纯数学prototype只接受已解析的单个L和接收集合，正式多源Boost适配在规则明确前BLOCKED。

Research/Culture修改玩家全局boost，接收城市是有效网络关系与计数的依据。没有连接的城市不会据此获得本地专业能力或工业效果。

Commerce IV中心无需额外路线，自动接受自己已接入的全部网络。作为合法recipient并入该类型城市集合；已经在集合则不增加N。其贡献是新旧sqrt强度之差，不固定追加L个百分点。商业降为III只撤销这条免费接收资格；若仍经其他有效途径接收，该城市保留。日志分开显示真实路线与freeSelfReceiver。

所有接收仅调用NetworkEffects，绝不调用LocalSpecializationEffects：不得授予源专业专家粮锤、人口收益、专家城市百分比、住房或GPP。商业III本城按不同网络种类给每专家+2S/+2C/+2P，不按来源数或路线数扩大。

工业多源暂沿用原架构提案：同一接收城市同源去重，不同接入工业源的Lv4半实际相邻锤相加；模板按接入源并集，各建筑取掌握该tier的有效源中最高折扣，不叠加折扣百分比。此口径与“中心每类一个网络”分开记录来源，便于后续改成单一代表源而不改存档。未经实际测试不宣称此多源细节已验收。

持久事实仅保留专业潜力、模板账本等；中心network set、来源列表、路线诊断计数、去重接收集合、内部浮点Network Strength都是load后由实际路线重建的缓存。

## Eureka / Inspiration

原生中国使用 `MODIFIER_PLAYER_ADJUST_CIVIC_BOOST` 和 `MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST`，效果为同名Effect；原生+10是百分点。当前缓存有Boost、额外Modifier，也有Babylon式+60等定义，基础比例绝不能硬编码40。

首选动态打开/关闭预定义额外boost效果，使引擎在触发当刻结算；不修改全局Boosts表，不在触发后盲目再补一次进度。由Gameplay Lua先计算未取整Network Strength，再交给独立BoostAdapter；不把sqrt表达式写入Amount。固定基础40不可假定。浮点Amount解析与动态撤销未确认前不接线结算，也不自行round/floor/ceil。已触发项目不因后来接通商路自动补发，也不因断网扣回历史进度。

必须测试：N=0→1→8→16→0；重复路线/多中心同城不增N；Commerce IV免费接收与实际路线重叠；ACTIVE变化与独立k；已触发/未触发；中国及其他boost效果叠加；总比例达到/超过100；目标已有部分进度；目标已完成；存读档；同一时刻商路变化/触发。验收要求仅完成当前科技/市政，不把多余奖励灌入下一项。引擎是否自行正确裁切尚未实测。

若原生效果在超100时不满足成本边界，再研究基于触发事件、当前实际cost/progress、已处理标记的一次性补充路径；需可靠读取引擎已发部分与事件时序。它容易与其他Lua boost互相覆盖，故属于后备试验，而不是当前承诺可行的默认实现。

## Great Works：可以读什么，不能先承诺什么

原生 `GreatWorks` 包含GreatWorkObjectType、EraType、Tourism；基础六yield在 `GreatWork_YieldChanges(GreatWorkType,YieldType,YieldChange)`。该表按作品类型定义，并非按“城市里的作品实例”定义。运行时编辑SQL也不能可靠令特定城市的单实例重算并遵守存档/多人规则。

当前HD确有按类别×时代的曲线。最终原生数据中，Landscape Culture从古典2到信息12，Music从古典4到信息18；Artifact现有多时代均为18。不存在一个可对所有作品直接使用的统一“当代+12”。

推荐通用目标表：从最终原生数据按ObjectType×Era×Yield分组；组内一致则自动提取标准值。组内不一致就要求配置明确参考曲线，不能取玩家最好一件，也不能擅自取最大值。时代缺档建议沿用不晚于目标时代的最近标准；EraType为空的圣遗物/产品不能凭空推断年代。可提供HD兼容数据文件，但核心不查询HD私有表即可运行。

“当前时代”建议用拥有者文明时代；也可按世界时代，需确认。时代比较使用Chronology/标准时代顺序，不按随机数据库Index大小。作品枚举必须区分实例index与GameInfo.GreatWorks类型，处理移槽/交换/征服；不能把实例ID直接作为表类型ID。

A现采用隔离的城市基础补贴模块：每城每yield加 `Σ旧作品 max(0,当代标准−作品基础值)`；它可以吃城市yield%，不降级较高原值，但不会自然成为作品基础值，可能不吃主题化、作品专属倍率或旅游加成。Tourism是独立系统，不从Culture补贴自动推导。

B按每件符合条件的标准文化作品获得多yield基础相邻，城市补贴候选为 `作品实例数×0.5×Σ各专业区域BaseAdjacency(yield)`，不区分原作品的原有yield；Science/Production/Gold/Faith等均保留。基础相邻示例6S/7C/5P/11G/6Faith时，每件补3S/3.5C/2.5P/5.5G/3Faith。仍存在作品层/主题化语义差异。

v0.1标准文化作品白名单建议：Writing、Music、Landscape、Portrait、Religious艺术、Sculpture、Artifact；排除Product、Relic（圣遗物不同于宗教艺术）及未知自定义类型，日志逐项标明包括/排除。这是可修改的明确类型表，不按本地化名称猜测。A只有存在可解释时代标准的类型才补差，缺失标准标USER_GAME_TEST_REQUIRED，不取玩家最好作品。B先使用同一白名单。

Specialty District分类不能简单排除全部“非传统产出区域”：City Center排除；Government Plaza、Diplomatic Quarter、Entertainment Complex及Water Park按原生区域族定义与当前最终数据库变化共同审计（不能只看RequiresPopulation），不能因为没有专家就排除。Holy Site、Harbor、Encampment可以被相邻扫描纳入，但不因此获得新专业。Preserve没有v0.1专业，作为相邻来源是否符合标准仍按同一分类器判定。本机当前娱乐中心RequiresPopulation=0而政务/外交区=1，必须把免人口限制与区域分类分开。使用DistrictReplaces归一化；内部区域排除；覆盖表只修正已核实的例外。实际分类清单由P0输出，未核实项标USER_GAME_TEST_REQUIRED。

## 施工队与标准化

施工队已确定为“固定城市项目→固定规格单位”。工业Lv1起可执行全部五档项目，不附加时代门槛，不提前解锁IZ，不提供更高1800/2000档。项目占用真实建设队列，不用城市当前Production计算单位储量；项目成本不是Wonder完成比例。

| 项目Production成本 | 单位固定施工力 |
|---:|---:|
| 280 | 250 |
| 460 | 420 |
| 820 | 750 |
| 1100 | 1000 |
| 1500 | 1360 |

自有规格表保存项目类型、单位规格、Cost、Charge。项目完成事件生成一队并冻结规格/charge，重复运行同一项目允许再次生成；不能按“城市+回合+项目”粗暴去重而吞掉同回合多次合法完成。用真实完成序列与请求账本防事件重复，生成失败明确记录，不能先标成功。v0.1先按用户给定固定值验证，不默认偷偷增加游戏速度缩放；如引擎对项目自动缩放，必须记录实际成本并单独报告，统一速度口径后再调整。

只能对目标己方城市当前合法开工的District/Building/Wonder使用；不替玩家放置目标，不注入Unit/Project。执行前重读实际锁定成本、进度、目标类型和位置。`applied=min(charge,max(0,cost-progress))`，`wasted=charge-applied`，成功消耗单位；剩余施工力完全消失，不递归读取下一个队列项目。750队面对剩余300：注入300、浪费450，后一目标进度保持不变。空队列/非法目标/实际剩余0拒绝，不消耗。

技术先例优先调查当前HD的Great Engineer、Wonder Architect/Mughal以及普通一次性单位脚本。本机已找到HD固定伟人工程效果MODIFIER_SINGLE_CITY_GRANT_PRODUCTION_IN_CITY，Amount=680、KeepOverflow=0（DL_GreatPeople.sql:377–378），优先作为原生固定注入候选；另有HD_Common.CityAddProgressPercentage使用真实成本/进度并调用AddProgress(min(...))的路径。前者Wonder有先例，District/Building支持仍须逐类实测；具体引用列入Specialization_P0_Status.md。复用通用技术模式，不include HD.Utils。成本/进度方法分别在Gameplay和UI探测，不能用GameInfo.Cost假装实际目标成本。District/Building/Wonder分别验收，任一类型失败单独报告USER_GAME_TEST_REQUIRED/UNSUPPORTED。

建筑标准化“曾建成”用源城永久tier账本，掠夺/出售建筑不抹去已经学会的模板；但无来源接入路线就不能继续获得模板折扣。城市被毁，作为来源不可用；跨所有者是否继承模板同专业潜力一起定义。对源城已完成的所有普通建筑做一次初始化扫描，使先建建筑、后成为工业专业也能标准化。

Buildings没有通用Tier列。用 `SPC_BuildingTiers(BuildingType,DistrictFamily,Tier)` + BuildingReplaces映射，原版显式分组；HD/JNR分支以最终已存在的建筑加入。BuildingPrereqs可辅助建议分层，不能把其最长路径直接当语义tier（例如无前置替代建筑、多分支、特殊解锁）。未识别组用“同一BuildingType”作为较窄回退并报告，不能暗给整区全建筑折扣。

折扣参数已定：INDUSTRIAL_PURCHASE_DISCOUNT_L1=10、L2=20、L3=30、L4=40，全部在一个配置表中。只有正在接受工业网络且接入工业源实际先建成同District+Tier建筑时才启用，没模板或没网络即0。当前 `EFFECT_ADJUST_BUILDING_PURCHASE_COST` 已有BuildingType/Amount例子，Amount正25/50是现有折扣用法，不猜负号。需验证对Gold/Faith是否都作用；若不能仅限金币，必须提供严格金币路径或明确提出折中，不悄悄给信仰折扣。

原购买科技、市政、区域、互斥、宗教等前提保持由引擎判定；模板不是解锁不合法建筑或允许买奇观。若用户希望原本不可购买的普通建筑也能购买，需要另做资格门控。原生按钮折扣优先于“全价购买后退款”，后者要求玩家先有全价金币，不等价。

住房建议按区域本体1 + 已存在有效tier数计算，同tier两个替代建筑只算一级；若用户原意是每一座建筑各+1则调整计数。内部承载建筑、奇观不计入tier。掠夺是否停供住房遵循选定原生载体并实测，不能单方面承诺所有情况下住房常驻。

## D. 存档与一致性

永久事实使用游戏对象Property，保存普通数值、布尔、类型字符串和经验证可序列化的小结构；不持久化userdata、函数、Lua对象引用或仅有的临时table。

| 对象 | 建议字段 | 行为 |
|---|---|---|
| Game | SPC_SCHEMA_VERSION、SPC_NEXT_CITY_UID | 版本迁移与全局稳定UID计数 |
| City | SPC_CITY_UID、SPC_SPEC_TYPE、SPC_POTENTIAL、首次专业事件信息、标准化tier账本 | 投资和专业唯一事实 |
| City / Plot | 派生效果数值、property门控位、派生版本 | 可重建，禁止当独立权威事实 |
| Unit | SPC_CREW_CHARGE、源城UID、单位生产身份、消费/请求状态 | 防读档刷新施工力、防重复消费 |
| Player | 请求序列/有限去重账本；必要时boost处理记录 | 同命令不能重复付费或奖励 |

征服、解放、归还可能重建城市对象并改变cityId。增加Game级城市UID记录，包含原中心plot、建城世代、当前拥有者与镜像永久事实；在转移事件迁移。中心plot单独不足以作ID：夷平后原地重建必须新UID、新潜力。保留/继承专业与投资建议跟城市走，非本文明拥有者时停用效果；这项属于待确认的占领规则。

存读档顺序：读取/检查schema→建立城市UID映射→恢复永久事实→读取真实总督/区域/专家/路线→重建全部派生效果→校验旧门控已归零→开放UI动作。断网/降级不是只加新值，必须清除失效效果。临时dirty队列可丢失，load后全量重建。

动作是受控状态转换：UI只发动作/单位/城市/请求序号，Gameplay按当前所有权、位置、潜力和队列重新验证；重复请求幂等，失败不消耗。消费与奖励不得分散成多个可重复事件处理器。引擎不提供数据库事务保证，必须测试完成事件重入、快速双击、命令队列、存档重载；日志中的“已发送”不能当作“已成功消费”。

首次区域完成历史：新局从事件准确记录；现有多区域城市如果没有可靠的首次完成时间，无法恢复历史。v0.1首选新局；旧存档导入需要显式选型/确定性迁移方案，不把遍历遇到的第一个区域谎称历史第一个。

## E. 大型机制Mod共存风险

1. **数据库加载顺序**：使用最终存在的类型、自己的ID与表；不批量覆盖他Mod原表。派生映射生成必须在相应规则之后运行，LoadOrder不代表永远能排在所有Mod后。
2. **专家与倍率**：现有GPP指纹已变，新增效果另做基数/城市百分比/全国百分比测量；UI数值可能与实际积累不同。
3. **UI覆盖冲突**：独立界面，避免修改HD替换的核心面板；仍需验证UI加载先后及桥接就绪。
4. **上下文与联机**：UI/Gameplay方法不对称；ExposedMembers不等于网络同步。v0.1先验收单人，未做双客户端一致性前明确不宣称多人兼容。正式Gameplay能力按玩家身份/trait判定，不能依赖Game.GetLocalPlayer过滤生效玩家；UI只展示本地测试玩家。
5. **内部建筑**：影响“建筑数量/同区所有建筑/区域产出”等通用统计；优先property门控，专家承载建筑单独做兼容试验。
6. **相邻二次复制**：建筑复制、区域base yield、城市yield、专家yield四者不能混用；实际接口缺失时必须报Unknown而不是0或旧值。
7. **总督重做**：基准任命、免费晋升、秘密结社不能靠裸晋升行数判定历史花费。
8. **隐藏规则变化**：前置条件、建筑tier、独特区域、金/信仰购买与生产折扣均可能变化；未知条目显式报告。
9. **事件顺序**：换总督/调专家/移巨作/断商路后即时刷新，回合全量校验为补漏；所有读取先快照，更新阶段防重入。
10. **AI**：原生AI不会自动理解烧Settler与网络建设。首个原型面向玩家操作；AI使用该文明的投资/施工队决策要另写小策略并测试，不能宣称已有竞争性AI。

## F. 分阶段实现与验证

架构已获认可；按R2每阶段只提交一个可测试模块，先静态验证再游戏内验收。没有运行测试的模块标USER_GAME_TEST_REQUIRED，不能把模拟器测试记作游戏机制通过。

| 阶段 | 实现范围 | 必须通过的验收 |
|---|---|---|
| P0 能力验证 | 独立只读探针＋最小可撤销+1效果测试；规则指纹；上下文方法表 | 同城UI/Gameplay专家、总督、路线、Base/Actual相邻对照；属性保存/读档；+1开关无重复；0.5精度 |
| P1 状态骨架 | 文明入口、专业锁定、潜力、Settler按钮、总督激活、独立状态UI | 放置未完成不锁专业；首个完成后永久锁定；双击只消费1单位；潜力4拒绝；投资3次后读档、调任、重新建立 |
| P2 本地MVP | 四类Lv1、Lv2住房/GPP、科研/文化Lv3与Lv4专家百分比、工业专家、商业基础收益 | 专家0/1/2；建筑tier；掠夺；政策/总督对照；级别退出清零；8/12/16城不加额外惩罚 |
| P3 网络MVP | 接入/分发、Research/Culture boosts、商业Lv3/4、工业模板与购买折扣 | 纯一种/混合/多个来源；商路结束与掠夺；中心迁移；Culture IV N=16额外16pp、N=8约11.3137pp；重复接收去重；小数/撤销；100边界；断网恢复原价 |
| P4 工业运输 | 五档项目生成施工队、超额浪费；IZ实际相邻的远程基础锤 | District/Building/Wonder分别完工；队列变更；残余/overflow；100相邻→每接收城+50而非总锤50%；断网撤销 |
| P5 高风险扩展 | Research实际多yield相邻、文化两个巨作能力及必要兼容曲线 | 相邻转换/复制无重复；作品迁移/主题化/时代更替；隔离城市补贴与作品本体收益，逐项验证交互 |

P1–P4通过即可形成城市专业化＋投资＋网络的可玩原型；P5未完成时发布说明必须明确标出未实现能力，不能宣称原始v0.1清单已全完成。施工队在P4开发只是工程顺序，游戏中仍为工业Lv1可用。

具体数学测试：人口12、科研专家3且Lv3，人口额外Science=18；5专家Lv4在原+152%城市得到+177%，不算成1.25×2.52；IZ Base8、2专家Lv1额外16P/6F，Lv3为16P/10F/32G；商业3专家、Research与Industry接入时额外6S/6P，无Culture；作品示例一件与两件逐项翻倍。

持久化测试：连续读档3次不重复效果/投资/施工力；快速同请求重发；城市征服→解放；夷平→原地重建；源工业城丢失；巨作调城；最后一个专家被撤下；总督仍在建立途中；重启游戏后仍无需打开面板即可生效。

日志格式建议：`[SPC][version][turn][player][cityUID][module][reason] old=... new=... status=...`。只在状态变化输出常规日志；诊断模式记录worker、base/actual各yield、GPP增量、来源路线ID、模板tier与折扣、动作结果。统计错误Unknown/Unsupported/OutOfRange，缺失接口不沉默。日志不承担存档功能；Mac直接写文件曾失败，优先引擎日志＋按需复制快照的现有可行通道。

## G. R2已确定与尚需验证的边界

已确定并覆盖R1：所有接入网络随每条分发商路同时传播；没有轮分/载荷/额外带宽；科研文化分别按实际接收城市去重，采用k×ACTIVE L×sqrt(N)；商业IV免费自接收且仅获网络能力；工业折扣10/20/30/40；施工队五档项目生成且超额浪费；Industry Lv1/3用Base、Lv4用Actual；文化专家三类各+2；旧作采用隔离城市基础补贴；文化相邻用Base、科研相邻用Actual；仅四种专业、IZ正常科技位置。

仍需验证而非预先改设计：UI/Gameplay接口差异，城市Property存读档，区域首次完成事件，总督建立/头衔含义，专家真实人数，Base与Actual准确边界，GPP基数百分比，boost100%上限，Gold-only折扣，项目完成生成与固定注入，巨作实例位置/类别及补贴交互。

默认实现口径需在测试日志中显式体现：总督门槛2/3/4且任命计1；同类型科研/文化来源取最高有效级；商业IV免费接收增加一个boost计数；工业不同源相加/同源去重；拥有者文明时代；标准文化作品白名单；原生Specialty District分类审计。若游戏接口不能准确区分Base/Actual，先报告该具体接口/测试失败，不回退替换公式。

市民/作品的城市基础补贴不自动等价于改变岗位/作品intrinsic yield；特别保留主题化、Tourism、GreatWork-specific modifiers和UI显示的独立验证项。当前不把静态SQL、模拟测试或接口存在当作游戏内PASS。

## H. 推荐文件结构（仅建议，尚未创建）

```text
CitySpecializationPrototype/
  CitySpecializationPrototype.modinfo
  Config/Players.sql
  Data/Civilization.sql
  Data/Parameters.sql
  Data/Requirements.sql
  Data/Effects.sql
  Data/SpecialistCarriers.sql
  Data/ConstructionCrewProjects.sql
  Data/ConstructionCrewUnits.sql
  Data/BuildingTiers.sql
  Compatibility/HD_BuildingTiers.sql
  Gameplay/Bootstrap.lua
  Gameplay/State.lua
  Gameplay/Capabilities.lua
  Gameplay/Specialization.lua
  Gameplay/Governors.lua
  Gameplay/Specialists.lua
  Gameplay/EffectBridge.lua
  Gameplay/TradeNetwork.lua
  Gameplay/BoostNetwork.lua
  Gameplay/Industry.lua
  Gameplay/GreatWorkInventory.lua
  Gameplay/GreatWorkEraSubsidy.lua
  Gameplay/GreatWorkAdjacencySubsidy.lua
  UI/SpecializationPanel.xml
  UI/SpecializationPanel.lua
  UI/ReadBridge.lua
  Text/zh_Hans_CN.sql
  Text/en_US.sql
  Tests/StateTests.lua
  Tests/NetworkTests.lua
  Tests/ManualCases.md
  Docs/Progress.md
```

Gameplay使用AddGameplayScripts；数据库用UpdateDatabase；UI用独立AddUserInterfaces，公共读取模块ImportFiles。配置数据库与Gameplay数据库分开。AffectsSavedGames应为1，与现有只读Probe区分；新局初始化与schema版本明确，不自动移植无法判断首个区域的旧城市。

下一步：交付第一批4项用户实机测试后停止，等用户返回结果再安排下一批；不启动游戏、不操作GUI、不等待加载。以上目录是目标结构，不一次性生成全部文件。

## 平衡修订：效率扩展与Spaceport辅助（当前权威）

Entertainment Complex / Water Park Regional Support属于未来系统，应修正k或最终Network Strength效率参数，绝不使用effective network level+1，也不追加per-route百分点。当前只保留计算层与效果层分离，不实现Support。内部强度保留浮点，显示可格式化但不得将显示舍入值回写用于结算。系数、精度和任何未来量化规则应分别版本化。

Spaceport是Auxiliary District，绝不是第五种专业。future auxiliary design / architecture note only，当前v0.1不实现、不注册事件/建筑/额外Modifier。触发必须是玩家完成Launch Earth Satellite（不是解锁或开始项目）：之后仅拥有Spaceport的己方城市双向自动联网：其自身专业源自动视为接入Trade Center；其自身自动接受中心当前所有已接入专业网络。无需实际商路且不消耗Trade Route Capacity，非Spaceport城市不因此自动接入。

实现时可把卫星连接作为独立provider，与路线和Commerce IV接收资格合并、按城市去重；先汇集直接源（含Spaceport城市自身专业），再生成接收集合，接收到的网络不重新当成自身源递归传播。卫星完成状态的存读档、区域建成/掠夺/城市易主/失去Spaceport后的资格、多中心模型需未来单独定义和验收。源码prototype当前不识别Spaceport或卫星。

设计目的仅是终局网络调度自动化。不新增Space Project Production、Science、Production或Laser Station效率。自动增加的合法接收城通过sqrt(N)产生递减边际收益。sqrt仍不是硬上限，其他Boost叠加及超100边界测试不能删除。

Modifier可行路径、技术边界和延后测试见Specialization_P0_Network_Sqrt.md。A004总督/专家用户测试保持不变，不要求现在额外实测Network。
