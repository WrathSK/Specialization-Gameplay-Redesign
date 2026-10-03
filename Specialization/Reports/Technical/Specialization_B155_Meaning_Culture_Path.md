# 意义延展文化追加：定域调查与暂行范围

Date: 2026-10-03
Source: develop bd5b823；runtime代码441b85f / B155.182
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
