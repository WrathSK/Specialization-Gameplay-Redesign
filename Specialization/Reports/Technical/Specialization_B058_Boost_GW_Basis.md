# B058：正式整数网络与D0019巨作基础计划

Document Owner: Codex
Design: D0020
Build: P0-B-058.76 / modinfo76

## 当前D0020追加

用户根据遗物固定基础产出，将遗物与产品共同排除保值。实现/测试已按D0020排除，文物ARTIFACT保留。以下D0019遗物分组讨论是较早过程，不作为当前范围。

## 完成与边界

B057截图明确整数Boost通过，结果另见Validation/Results。正式NetworkBoost当前计算完整Raw=k×L×sqrt(N)，保留FinalRaw位置供未来合法修正，末端math.floor(x+0.5)，按Applied值附着一个载体。独立k_R/k_C、max ACTIVE、recipient集合不变。90个整数载体覆盖两类1–45（当前最大4√129量化45）；不把45当玩法封顶，超出目录报错撤销而不clamp。未来k或Entertainment配置改变需扩表。SQL原生Boost与HD提示Property均写整数；保存旧B055表供清理，不再使用其浮点载体发放。

新增tools/generate_boost_integer.py、Mod/BoostIntegerConfig.lua、Mod/Data/NetworkBoostInteger.sql；修改NetworkBoost、版本/manifest/面板。B057实验入口暂保留可复用，不要求重测。

## 巨作计划

新增Mod/UI/GreatWorkBasis.lua；挂入已有Read Great Works，不新增面板按钮。Collect读取当前城市各building/slot/work index和数据库基础Culture/Faith/Tourism。Plan逐项最大、逐件补差、文化/遗物隔离，产品/未知类别排除。读数改变会重新计算，不写永久“曾经最高”或修改基础值；旧city/object探针加成不反馈到计算输入。报告明确“未发放、倍率/主题化未接入”，最多显示四件明细但计算全部作品。这个模块不负责Culture IV资格或发放，因此能在任意测试城市观察计划；正式消费者必须使用EffectiveFacts.active==4，未接入不冒充正式机制。

## 原生后端调查

本机DebugGameplay只读查询：与Great Work相关既有ModifierArguments包含GreatWorkObjectType、YieldType、YieldChange、ScalingFactor、Religious等，没有找到GreatWorkType/GreatWorkIndex的单件目标参数先例。已知MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD对应EFFECT_ADJUST_CITY_GREATWORK_YIELD，作用层为整类作品。HD古罗马剧场/Kongo/Mall都是类型修正，不能据此断言可针对同类单件补差。

反例：同城著作基础2和12，目标12，正确差额10和0。整类+10会变成12和22，抬高最高作品；用平均+5虽然基础总量相同，但每件并未补齐，若所在建筑主题化/作品专属倍率不同还会算错，不能使用。简单城市+10同样不满足用户明确的作品倍率/主题化，已拒绝此fallback。

官方Base/Assets/UI/GreatWorksOverview.lua:267/330/581使用IsBuildingThemedCorrectly，可读取建筑主题化；仅此布尔值不足以恢复所有特殊Modifier及倍数叠加。当前未找到可信单件native yield setter，未证实不存在。后续须验证单件/建筑作用域途径，或完整捕捉作品倍率后精确结算且验证各层；不得猜参数或直接全局修改GreatWork_YieldChanges来实现城市限定效果。

HD当前数据库遗物均基础4Faith/8Tourism，因此同组通常无差额；算法仍支持其它合法遗物基础，不捏造差异来要求开局。文化类HD特殊作品可有其它Food/Science等yield；D0019当前保值只处理文化/旅游，原额外yield保持原状。

## 验证

DevelopmentTests/test_b058_boost_gw_basis.py使用真实Lua与只读外部DB内存副本：整数目录90行、同整数不同N无重写、降级/清理旧目录/重载、超出目录不clamp；D0019不同作品分别贡献最大值、遗物隔离、产品排除、移走最高后回落、空集合、重复ID拒绝、基数不读含buff的实际yield。B055/B054/B052/B051相关回归通过。STATIC_CONFIRMED/LOCAL_SIMULATION_PASS非原生新行为PASS。D0018冻结hash验证；D0019当前hash见ChangeLog。未启动游戏、无commit/push。

## 最终部署

B058.76 / modinfo76，98文件，源/运行hash同为`efb2363a44ef151f95989da8ea080775f03d7f33fe02aa4495336482c7616719`。旧运行备份留在外部SpecializationDeploymentBackups/.SpecializationP0-backup-t8xanbum；本轮中间75也有独立备份。D0018/D0019原文已冻结；未启动游戏/commit/push。
