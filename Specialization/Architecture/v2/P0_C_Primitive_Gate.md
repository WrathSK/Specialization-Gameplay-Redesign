# P0-C — 已授权实施，原生专家收益门禁未关闭

Date: 2026-09-20. Baseline: B080.107/modinfo107; develop20e0588. Design D0035 / Research D0031 unchanged.
Status: AUTHORIZED / PRE_CUTOVER_TECHNICAL_GATE_OPEN. **P0-C NOT COMPLETE / NOT PASS**.

## 结论

已执行实施前的共享事实与SQL候选验证；尚未切换正式收益。现有原生专家收益路径具备单学院实施基础，但本轮未取得它覆盖同城多个学院实例的原生证据。不能把这个证据缺口写成“Civ VI不支持”，也不能用本地mock代替引擎验证。旧48个Research IV载体/writer保持原样；无半迁移、无部署、无build提升。

[已授权计划](P0_C_Plan.md)的primitive门禁要求先核对特色/多学院覆盖，不得静默只覆盖锚定学院或改为全城平坦收益。本轮在门禁关闭前保留旧包；这是技术证据待补，不是新的Design问题，也不是用户撤回实施授权。不要重新要求用户批准整个P0-C。

## 本轮实际证据

|检查|结果|限制|
|---|---|---|
|真实CurrentSpecializationFacts + DistrictCompleteness + ResearchInfrastructureShadow|D0/1/3/6/10 × workers0/1/2/5 × ACTIVE0..4：100组合输出正确，写入0|LOCAL_SIMULATION_PASS；未增加正式writer|
|两学院：D3/7、workers2/3|最高D7 × 全部5人=35；高D学院被掠夺后3×2=6；workers未知不假装0|同上；不证明原生载体覆盖|
|离线Science载体候选|四位1/2/4/8可表达D0..10；CitizenSlots0/InternalOnly；真实表结构可执行|LOCAL_SQL_PASS；不在modinfo，不是已生效效果；Types.Hash仅测试替身，未模拟引擎hash/全数据库依赖|
|本机DynamicModifiers查询|没有命中EffectType含CITIZEN+YIELD或SPECIALIST的直接条目|限定查询结果，**不是**穷尽原生API后证明不存在替代路径|
|本机学院/特色学院|Campus/Observatory/Seowon的OnePerCity=1|每Type限制，不足以推断整个normalized领域最多一个实例|
|当前P.CreateBuilding|Mod/Probe.lua:525只传building ID；HasBuilding/GetBuildingLocation也按building ID读|说明当前封装未证明逐实例配置，不证明引擎没有位置参数|

可复现入口：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_p0_c_primitive.py`。
只读数据库定义摘录：[primitive_evidence.json](../../../DevelopmentTests/Fixtures/P0C/primitive_evidence.json)；离线候选：[research_science_candidate.sql](../../../DevelopmentTests/Fixtures/P0C/research_science_candidate.sql)。

## 替代路径调查：未判定引擎不支持

本机HD CityPolicies.sql与DL_Wonders.sql的Building_CitizenYieldChanges、ResearchSupport.sql证明这一表的既有用法；只证明配置存在。原版WorldBuilderCity的CreateBuilding有plot参数，但WorldBuilder接口不是正式Gameplay接口，不直接移植。

[Hemmelfort原作者Lua手册](https://github.com/Hemmelfort/Civ6ModdingNotes/blob/master/%E6%96%87%E6%98%8E6_Lua%E6%89%8B%E5%86%8C.md#创建移除建筑)给出`GetBuildQueue():CreateBuilding(building.Index, pPlot:GetIndex())`候选。它使“封装没传plot → 引擎不能指定plot”的推断无效；尚需本机确认普通内部建筑是否遵守指定学院位置、是否影响其它学院、同一BuildingType多实例如何处理。不能照搬WorldBuilder签名或为同名Type重复创建后假定成功。

## 关闭门禁的最小下一步

1. 独立、手动一次性primitive probe：只用明确标记的测试ID，指定目标学院plot，核对创建后的GetBuildingLocation、对应专家Science变化、删除后的恢复。不得增加轮询，不得修改普通建筑/HD。
2. 同城第二学院分别放专家，区别“只附着一个实例”和“覆盖所有同域实例”；再检查特色学院。D可用固定已知测试值隔离；不需要完整新能力或多个长局。原生创建/删除、按专家增量须由用户实机确认，不能用本测试countermodel判定引擎行为。
3. 若单个载体仅覆盖一个实例，评估带plot参数的独立载体配置；不要未证实即增加大规模固定slot池。不把多学院固定平坦科技作为替代。
4. 路径明确后继续同一P0-C授权：正式writer、精确48旧效果退出、完整回归、简明诊断、W0003安全部署。未来probe包要明确是probe而非正式P0-C PASS；当前未创建可运行probe，不要求用户现在启动游戏。

本轮未执行正式cutover的UNKNOWN/withdraw/load/late-response/非目标差分全矩阵，也未宣称通过；那些仍是计划内必须完成的门禁。当前源码未改，无必要重跑整套旧Gameplay回归来冒充本批完成。

## 诊断可读性合同（用户本轮明确要求）

所有后续新增/修改诊断优先按“结果 → 关键依据 → 异常/操作”排列，默认只含当前所选城市和当前能力相关信息。成功状态不逐行输出内部ID/完整carrier清单/其它模块报告；异常只显示具体原因与下一动作，详细数据按需展开。不能省略会改变结论的UNKNOWN、旧效果残留、实验污染等状态。

P0-C未来默认报告不超过约6–8行，示意（不是当前已部署界面）：

```text
科研基础设施｜已配置（原生收益待核对）
科研 IV：Potential 4 / ACTIVE 4
基础设施深度 D=7；工作科研专家=5
预期新增基础科技：35（7×5）
载体配置：每名+7；旧科研四残留：0
异常：无
基础设施组成 → 按需查看
```

异常时用“暂不可确认，保留上次配置”替换成功状态；B050实验开启必须单独提醒，不算入新效果。配置和实测不能混称。详细D仅展开学院域的计入/排除、Tier、贡献、掠夺、cap前后及最高单区域选择；不要自动拼接Lv2住房/GPP、工业Copy等报告。完整ID用于排错详情，不挤占默认报告。

## 完整性与退出状态

Mod/全部126文件及Design与20e0588逐字节一致；离线测试SQL不属于Mod。main不改，当前运行包保持B080.107。没有部署/游戏操作。当前状态是“已授权、实施前技术门禁待关闭”，不是P0-C实现PASS。下一工作仍为TS02最小原生primitive验证，不进入下一P0批次。

## Subsequent user clarification / closure

用户确认同城不会有多个同一区域（社区除外），因此上述多学院门禁不再阻塞当前P0-C。不能将此前UNKNOWN写成引擎缺陷。B081实施与用户待验收范围见[P0-C完成报告](P0_C_Research_Infrastructure.md)；本页离线预检记录保留为历史证据，不是当前未完成状态。
