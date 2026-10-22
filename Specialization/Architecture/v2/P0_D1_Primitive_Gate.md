# P0-D1 — BASE与原生小数门禁 / 实施进度

## Gate update — user result and temporary exception

User reports only integer worked in B083 tested district path; authorizes floor. Formal cutover proceeds with floor after50% aggregate, Campus placement. No general float conclusion, no Design edit. See [P0_D1_Research_Cross_Cutover](P0_D1_Research_Cross_Cutover.md). Earlier UNKNOWN/blocking statements are historical.


Status: AUTHORIZED / PRE_CUTOVER_GATE_OPEN. P0-D1未完成，不标PASS。
Baseline: 86a67bc；runtime仍B081.108/modinfo108，P0-C用户Pass有效。Design D0035/Research D0031不改。

## 最新进度：区域归属硬约束与B082原生实验

用户确认最终收益步长0.5优先、必要时整数，50%转换系数不变。不得用城市人口补贴假装区域收益。已找到城市范围区域yield整数原生/HD先例，准备[默认OFF的0.3/0.5/1实验](P0_D1_District_Precision_Probe.md)。B082只添加手动实验，未正式切换D1。下文“无运行变化/无测试包”仅指此前阶段，已被本段取代。Design原文不改、量化未启用。

## HD政策补充证据（优先于下方先前停止依据）

[四政策专项调查](../../Reports/Technical/HD_Policy_Fractional_PerPopulation_P0D1.md)确认原生同一per-population Effect存在0.2/0.3/0.7正式参数。旧Copy编码器限制不能作为原生只能半点的证据；上一轮因此停止调查过早。后续在既有P0-D1授权内优先验证固定目标量的等价承载及人口变化/量化，不新增Design人口乘数。原生门禁尚未通过，旧writer保持完整。

## 本轮已完成

- 按用户实施授权检查实际Lv3Effects、SampleLifecycle、IndustryRefresh、CopyYieldRefresh及相关写入/派发入口；没有实施writer切换。
- 离线候选 `DevelopmentTests/Fixtures/P0D1/ResearchCrossModel.lua`：九域六yield BASE×0.5、资格/完成/掠夺/特色归一、多社区、逐区域组成，UNKNOWN不伪造零；不是运行模块，不进入modinfo。
- `DevelopmentTests/test_p0_d1_gate.py`实际执行候选Lua：数学、资格、无人口/专家/D/actual耦合通过；1785组整数/半点原有primitive分解通过；0.25/0.65等反例正确标出旧primitive未验证范围。8旧SQL效果仍原样保留；Mod及Design字节/文件集合与86a67bc一致。
- 这是LOCAL_SIMULATION_PASS（本地模拟），不是采样生命周期/正式writer/引擎结算PASS。10000通知、完整新writer回归未执行，因为尚无新运行模块；不能冒称D1压力验收完成。

## 可复用的证据

1. 本机HD `UI/Replacement/RealModifierAnalysis.lua:994–998`明确区分district:GetYield/GetAdjacencyYield为修正后值，Plot:GetAdjacencyYield为raw。原版AdjacencyBonusSupport.lua也调用Plot接口。本Mod工业和巨作BASE路径使用该接口。这是STATIC_CONFIRMED接口选择，不是九域新producer实机确认。
2. B050历史用户证据 `Specialization_B050_User_Result.md`验证3/4人口的固定0.5 Science/Production组合及OFF恢复，含原生倍率/细粒度误差。不能推断任意小数或全人口实机PASS。
3. CopyYields.Plan明确仅接受非负整数/半点至65535.5；半点人口范围1..255。P0-C采用专家整数Science，不能证明固定城市0.25/0.65。
4. 只读DebugGameplay.sqlite调查见static_evidence.json：YieldChange未见非整数、查询的相邻数值参数未见非整数；仍存在YieldChange1/TilesRequired2定义。该缓存不能代表所有当前/未来启用Mod组合。整数DB字段不能单独证明API整型返回/结算顺序。
5. EFFECT_ADJUST_DISTRICT_YIELD_BASED_ON_ADJACENCY_BONUS有原生/HD先例，但所读实例是YieldTypeToMirror/YieldTypeToGrant；当前没有从这些实例证明50%且排除倍率的等价合同，不能直接替换。

## 未关闭门禁，不偷换为已确认引擎限制

若BASE合计0.5，则Design目标0.25；若BASE合计1.3，则目标0.65。候选纯模型保留这些值，既有Copy primitive拒绝。**这是本地反例，不是声称当前游戏已实测出现这些BASE值。**目前缺少足以把本能力合法输入限定为整数的原生证据，也没有验证更细小数的正式投影路径。

结论是TECHNICAL_INVESTIGATION_REQUIRED，不是“Civ VI不能小数”。不能因为该未知就将Design增加整数限制、floor、替换专家收益、收到unsupported后清零，或接受永久少发收益的正式实现。

按用户已批准P0_D1_Plan“没有等价可靠路径则停在门禁，不先拆旧writer”，本次保留完整B081效果，不部署半迁移实现。既有实施授权继续有效；不是撤销授权，也不是要求重新批准同一范围。

## 精确退休边界（尚未执行）

8 IDs：BUILDING_SPC_DEV_LV3_POP_RESEARCH_0..7；SPC_LV3_POP_RESEARCH_0..7的Modifier/Arguments/BuildingModifiers附着。
Lv3Effects以specialization动态拼接Research/Culture IDs；Gameplay启动、投资/单位动作、LV2_GPP_DIRTY以及NetworkBridge间接Audit可到达。CityInheritance的历史调用需保留隔离，不启用ownership代码。后续cutover只退出Research分支，Culture人口、Commerce connected-kind不改；B081新科研IV和已退出48旧IV不改。

## 下一技术步骤与最小测试边界

继续在已授权D1范围内完成最小原生primitive调查：先证明Plot BASE在目标环境的返回域；若可充分建立整数域，可复用既有半点组合并做同城policy/BASE对照；否则独立验证更细小数投影，原生对照至少含0.25/0.65、不同人口及百分比。两条路径均不得据SQLite接受浮点就宣布引擎PASS。

未发布独立原生测试包，因此当前不要求用户操作旧按钮或猜测诊断入口。不能把本轮离线候选自动部署；技术门禁关闭前不进入正式cutover，也不进入P0-D2。没有新的Gameplay Design决定交给用户。
