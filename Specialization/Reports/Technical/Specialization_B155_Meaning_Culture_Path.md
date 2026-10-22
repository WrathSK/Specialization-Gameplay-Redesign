# 意义延展文化追加：定域调查与暂行范围

Date: 2026-10-03
Source: 初次调查develop bd5b823；本次建筑／诊断准备基于b958909；runtime代码441b85f / B155.182
Evidence: STATIC_CONFIRMED；复用具名USER_GAME_TEST结果，无新增实机或本地玩法模拟
Fallback: CONDITIONALLY_AUTHORIZED；用户接受无可靠路径时暂排市政／外交；当前D0042与B155保持，尚未采用或实施

## 调查结论

不能说“其它产出全部正常，唯独文化不可实现”。当前证据为：

| 产出 | 当前Meaning实际状态 | 能支持的结论 |
|---|---|---|
| 科研 | 已有整数writer；B155本fixture增加1 | 已测作品读数成立，非全部作品／倍率／结算PASS |
| 金币 | 已有整数writer；B155本fixture增加4 | 同上 |
| 文化 | SPLIT、SINGLE3、SINGLE3_SCALE100均有writer；后两者4→4，预期4→7 | 当前路径不可靠；不能证明所有原生文化追加永久不可行 |
| 生产力 | 只有计算模型，没有本原型writer | 尚待实现／原生验证 |
| 食物 | 同上 | 尚待实现／原生验证 |
| 信仰 | 同上 | 尚待实现／原生验证 |

同回合T62、单件Writing、古罗马剧场、非主题、旧Dialogue0%的两候选结果见[单一3](../../Status/Validation/Results/Specialization_B155_P0L2B_Single3_Native_Stopped.md)及[显式100](../../Status/Validation/Results/Specialization_B155_P0L2B_Scale100_Native_Stopped.md)。原配置与原生读数必须区分；配置Culture3不是收益3。基线4=原生2+HD2，没有依据说HD被直接取消。

## 源码与数据库复核

- [Meaning模型](../../../Mod/CultureMeaningModel.lua)逐域Floor，再同yield相加、最后乘W；当前运行仍九域，writer只投影S/G/C。[Probe](../../../Mod/CultureMeaningProbe.lua)三yield共用project创建／移除／损坏核对，没有culture专属清除。错误也不会伪装配置成功；事件重入采用既有busy/deferred边界，不因carrier数量改变ACTIVE或D。
- [Dialogue](../../../Mod/Dialogue.lua)0%映射为无carrier，移除自身D/TEST项，并要求owned全不存在；没有安装ScalingFactor0。原生移除后的内部状态未读出，不能由HasBuilding证明完全退场。
- [GWA](../../../Mod/GreatWorkAdjacency.lua)hold仅清156个自身B060项，不触碰Meaning或HD。退出仍是Meaning→Dialogue→GWA自身恢复，未发现玩家全局关停或广泛建筑删除。
- 当前实际内层Firaxis Cache的DebugGameplay以mode=ro核对：HD Writing+2、Meaning Science1／Gold4及两个Culture3候选的flags均0、Owner/Subject requirement均NULL；BuildingModifiers附件与参数齐全。DynamicModifier为COLLECTION_OWNER / EFFECT_ADJUST_CITY_GREATWORK_YIELD。HD附着普通AMPHITHEATER，探针附着各自隐藏CityCenter building。数据库定义相同不证明运行实例活动。
- 外层旧Cache没有本候选，未用作本次证据；未修改配置／数据库。当前测试helper未配置外部DB，本轮没有运行该helper或声称其PASS。

没有发现可直接解释仅CultureΔ0的Lua缺陷。Culture已有原生与HD同yield平加、旧Dialogue同effect倍率，S/G没有已知相同基础／HD叠加背景；这是候选差异，**不是覆盖／优先级／相加算法已确认**。

## 历史成功与外部先例能证明什么

[B055成功](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)四原件已逐张看并4/4 SHA核对：T7/8/9/10，单件Writing的Culture2/4/2/2。没有槽位建筑或HD实例，不能证明HD+2与另一flat共存，更不能区分全部相加或只生效一项。它只证明当时单flat追加／退出成功，因此也不能从B155推导文化平加全不可行。

当前[GreatWorkProbe.sql](../../../Mod/Data/GreatWorkProbe.sql)仍为隐藏CityCenter building→BuildingModifiers→同primitive，Culture YieldChange2；最早可访问Git3382d7d是B060 checkpoint，不冒称B055部署源码。当前包装API仍调用原生CreateBuilding／RemoveBuilding，没有换成AttachModifierByID。

[作者Moksha SQL](https://github.com/Feofilakt/YAGM/blob/main/Moksha.sql)只是同primitive Relic Culture YieldChange3，非多flat、mixed参数或Dialogue/theming隔离实机证据。换相同effect的attachment/collection目前没有可靠替代语义证明。

## 用户已接受的条件后备与未来待办

政府广场、外交区是当前Meaning九域清单中仅有的Culture来源。用户已接受条件后备：**若无法形成可靠文化追加路径，暂将这两个领域排除于意义延展，标记未来处理**。本轮没有找到可靠可直接采用的替代，但原生实例活动／组合算法仍未知，不能把两个候选失败升级为引擎永久不支持。此处记录条件授权，不静默激活为新Design。若后续采用，Meaning会从九域／六产出改为七域／五产出；剧院本来不参与，Meaning本来也没有Tourism。后备方案不删Shared映射，不影响其它能力／专业，不转换为其它yield，不补差、不改K或Floor。

**现行正式Design仍D0042九域；B155模型、SQL、writer与运行包未变。** 采用后备前先按用户已授权范围同步正式Culture／Spec及阅读版，避免plan与JSON双重权威；运行适配仍需其实施授权。当前SINGLE3候选要求Culture恰3，原四态还要求正Culture；将来七域原型需另行适配，不能只改输入就宣布既有流程PASS。本轮不授予新原型或正式cutover。

## 保留的门禁与未来恢复条件

- 剩余Production/Food/Faith writer尚无原生证据；精确支持作品recipient仍未解决，按对象大类命中不能等同受支持定义白名单。
- native-only Dialogue、主题化独立追加、正常结算／冷加载／完整退出及global旧GWA切换仍各自验收。去掉Culture来源不自动关闭这些门禁，也不将旧Dialogue Culture/Tourism路径宣称为全native-yield完成。
- 未来文化定域调查优先按需读取精确Modifier实例、owner及可可靠取得的活动／对象状态，与成功S/G和HD对照；现probe没有这类证据。[已有GameEffects先例与限制](Specialization_Trade_Authority_Second_Audit.md#新证据与边界)只证明局部Gameplay读取先例，不保证subject/tracked接口或schema可用。
- 该诊断若需要新代码，应另行提出单选城／按需／精确ID只读范围，不建常驻全局扫描、不继续猜系数。附着错误则修确切附着；活动正确却无增量再比较组合／读取／结算口径。可靠固定追加在现有Culture及Dialogue/theming组合下成立后，才重新审阅恢复两域，不能自动启用。

本轮不要求用户重测，不运行玩法回归，不部署或启动游戏；结论止于这次调查和所引用的已测场景。


## 古罗马剧场：建筑与著作收益来源复核

2026-10-03追加，仅STATIC_CONFIRMED。名称对应通用`BUILDING_AMPHITHEATER`（Amphitheater），当前`TraitType=NULL`、非Wonder、BuildingReplaces双向无记录；不是罗马专属建筑。原版名称标签也译为“古罗马剧场”。当前实际Name为`LOC_BUILDING_AMPHITHEATER_NAME_UC_JNR`，其中文名称／描述由已加载区域扩展提供；不是仅由未含Mod标签的Localization缓存推断。

| 当前来源 | 定义／计算对象 | 本次含义 |
|---|---|---|
| 建筑本体 | 剧院广场普通建筑；Building_YieldChanges Culture1 | 建筑自身收益进入城市产出，不是作品小计中的HD+2 |
| 专家 | 1槽；专家Culture1、Gold−1；Writer GPP2 | 专家／GPP另算，不计作作品基础文化 |
| 馆藏 | 两个Writing槽；主题倍率／条件均0 | 本建筑本身不建立艺术馆式主题奖励，不外推其它建筑 |
| HD区域扩展著作文化 | `HD_AMPHITHEATER_WRITING_CULTURE_BOOST`；Writing／Culture／YieldChange2 | 本城每件著作额外Culture2，非只限定这两个槽 |
| HD区域扩展著作旅游业 | `HD_AMPHITHEATER_WRITING_TOURISM_BOOST`；Writing／ScalingFactor150 | 文字说明为＋50%旅游业；不是本次Culture平加primitive |

对已测基础Culture2的那件作品，基线4的正常解释是**作品基础2＋区域扩展著作2**。不能把它拆成作品2＋建筑自身2；原版建筑自身Culture2在当前加载后的定义已是1。作品、建筑、专家的来源必须分开。现数据库93个Writing定义的基础Culture从1至18，且少数含其它yield，因此诊断打印实际`GreatWorkType`及其`GreatWork_YieldChanges`，不能将所有著作基础值写死为2。

### 加载源与覆盖证据

以下路径相对于Steam的`steamapps/workshop/content/289070/`；外部文件只读、不复制进仓库：

- 主HD `2465378070/UpdateDataBase/DL_Buildings.sql`与`Gameplay/CityYield.lua`由当前内层Modding.log第7315／7396行确认加载／注册。主包本身未检出上述著作＋2 ID，不代表当前定义没有来源。
- 后加载的`2701747165/DistrictExpansionHD.modinfo`为District Expansion (Harmony in Diversity Edition)，版本2.2、组件LoadOrder18000。内层Modding.log第7529–7533行应用`DistrictExpansion_Theater`并加载`Database/theater.sql`、`Text/theater_texts.sql`。
- `2701747165/Database/theater.sql:8/17/43`改Name／成本110／维护1／文学传统HD／专家槽1、建筑Culture1、Writer GPP2；第152–153行附着两项HD Modifier，第195–196行定义类型，第231–235行定义Writing＋2Culture／Tourism150。
- `2701747165/Text/theater_texts.sql:83–84`给当前UC_JNR标签名称“古罗马剧场”，描述“本城所有著作＋2文化、＋50%旅游业绩”。原版`Base/Assets/Gameplay/Data/Buildings.xml:113/338/416/468`则是成本150、戏剧与诗歌、建筑Culture2、Writer GPP1、两个Writing槽。
- 内层`Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`以只读模式所得BuildingModifiers／ModifierArguments与该扩展逐项一致；DB时间08:49:20、日志08:51:19，所涉外部SQL均早于它们。**STATIC_CONFIRMED：已加载区域扩展覆盖**；没有源码晚于DB、目录错误或缓存过期的证据。外层旧Cache仍不采用。

Culture＋2与Meaning候选使用相同`MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD`／`COLLECTION_OWNER`／`EFFECT_ADJUST_CITY_GREATWORK_YIELD`。附件对象分别是实际AMPHITHEATER与隐藏CityCenter building；两者没有owner／subject requirement。静态相同只能提出“实例／组合行为需要区分”，不能宣布互相覆盖，更不能认为HD收益被本Mod主动撤销。

## 原生Modifier只读接口：先例与城市匹配边界

已安装UI代码的真实调用，比二进制名称或猜测方法更具体：

| 接口 | 当前源码先例 | 诊断可记录，不能外推 |
|---|---|---|
| GetModifiers / GetModifierDefinition | HD、BRS、DMT；实例数组，Definition.Id／Arguments | 一次全局枚举；未找到按城市枚举接口 |
| GetModifierOwner / GetObjectsPlayerId / GetObjectType | BRS UI | owner对象ID／玩家ID／类型；内部owner ID不是CityID |
| GetObjectString | HD、BRS、DMT | 原始描述；本次实际City格式尚未读取 |
| GetModifierActive | BRS／DMT UI按boolean使用 | 活动API值，不等于收益已入账或所有requirements通过 |
| GetModifierSubjects | BRS／DMT UI；对象ID数组或nil | nil、空数组、不可读分别记录；不由空列表证明无效果 |

精确位置：`1312585482/BRSPage_Yields.lua:84–103/131–163`，`2428969051/ui/dmt_modifiercalculator.lua:95–108`，其`dmt_modifierrequirementchecker.lua:54–56`还独立检查owner requirement；HD`2465378070/Gameplay/CityYield.lua:139–158`用于Gameplay加载重建，而Active／Subjects当前仅有UI先例。`GetModifierTrackedObjects`只发现注释，首版不调用；不发明IsActive字段、GetCityFromObjectString或GameEffects.IsCity。

**TECHNICAL_IDENTITY_BOUNDARY。** HD注释示例为`City (65536), Owner: 0, Name: ...`，实现宽松抓前两个数字；BRS城市归组按名称。两者均不能直接作为本诊断的可靠同城证明。首版分开记录“所选城市的owner／CityID／完整reference”与“实例owner对象的玩家／类型／限长raw描述”，实例城市归属先标UNKNOWN。城市名称仅展示，不匹配；不凭单坐标、内部对象ID或首两个数字猜城市。真实格式确认后，严格字段解析仍须与所选城市当前owner／ID、可取得的CityManager对象及完整reference交叉核对；任何不符停止该归属结论，不修改身份架构。

[具体诊断计划与最小原生流程](../../Architecture/v2/P0_L2_Meaning.md#modifier实例诊断)已准备，**尚未实施／部署**。首轮仅一次当前状态读取，确认schema与城市匹配证据；不重复已失败四态、猜系数、暂停HD或创建新Modifier。Active=true且城市明确，仍不能证明flat累加／正常结算。条件后备保持未采用；本轮没有新实机、LOCAL模拟或Design变化。
