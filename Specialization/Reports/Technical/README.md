# 技术研究索引

Document Owner: Codex

这是按问题检索的HOW索引，不维护第二份验证矩阵；当前状态只看[Status](../../Status/Specialization_P0_Status.md)。旧报告标题/版本/当时待测文字是历史，先读最新结果和下列取代关系。

| 问题 | 优先资料 | 已知结论/不要重复 |
|---|---|---|
| 最新科研复制范围 | [D0014](Specialization_D0014_All_District_Copy.md)、[B051.66用户结果](../../Status/Validation/Results/Specialization_B051_66_User_Result.md) | [B051.67](../../Status/Validation/Results/Specialization_B051_67_User_Result.md)最小补测口头通过，非全部组合；旧四类白名单已废弃 |
| B051自动刷新 | [实现](Specialization_B051_Automatic_Copy_Yields.md)、[事件修正](Specialization_B051_Background_Fix.md) | 65失败、66收益用户通过；不能只凭只读计算值认定载体已挂 |
| 标准化下一工程任务 | [目录快照：范围见D0015](Specialization_Standardization_Catalog_Candidate.md)、 [记录研究](Specialization_Standardization_Storage_Research.md)、[剩余研究](Specialization_v01_Remaining_Work_Review.md) | D0015记录/启用范围已定；账本接入和Gold-only仍待实现/验证 |
| 商路来源与桥接 | [用户来源决定](Specialization_Network_Background_Source_Decision.md)、[B025](Specialization_B025_Background_Network.md)、[计数修正](Specialization_B026_Trade_Count_Fix.md)、[D0009](Specialization_D0009_Architecture_Sync.md) | 后台UI已接受；B026旧接收语义被D0009取代 |
| 纯Gameplay调查 | [第二轮审计](Specialization_Trade_Authority_Second_Audit.md) | 未发现可靠全集，不能推断绝对不存在；不再阻塞后台UI主线 |
| 永久存储与城市身份 | [Property/建筑](Specialization_P0_Marker_Storage.md)、[正常恢复](Specialization_B021_Normal_Load_Resume.md)、[丢史反例](Specialization_Load_History_Ambiguity.md) | 不用历史事件/当前建筑猜旧专业；极端丢写延后 |
| 原生精度 | [负面知识索引](Specialization_Implementation_Caveats.md)、[每人口证据](Specialization_Fractional_PerPopulation_Evidence.md)、[B050](Specialization_B050_Half_Yield_Experiment.md) | 平坦小数失败≠所有Modifier整数化，B051半点成功≠任意小数已解决 |
| 总督/高级本地能力 | [晋升刷新修正](Specialization_B037_Governor_Promotion_Fix.md)、[Lv3其余效果](Specialization_B038_Lv3_Remaining_Effects.md)、[Lv4百分比](Specialization_B048_Lv4_Percent.md) | 早期待测已由Status关联用户结果取代；不重发 |
| 投资/Crew动作 | [单位面板](Specialization_B043_Unit_Panel.md)、[Crew项目](Specialization_B044_Crew_Projects.md)、[UX](Specialization_B045_Crew_UX.md)、[整数速度](Specialization_D0012_Integer_Crews.md) | 单位视觉复用不等于通用建造者玩法；快点确认须保持原按钮位置 |
| Commerce IV | [basis与环路](Specialization_CommerceIV_Basis_And_Cycles.md) | 总量是用户条件备选，非已部署；同步读写/绝对覆盖不是充分防环 |
| Boost | [sqrt](Specialization_P0_Network_Sqrt.md) | 浮点Lua强度≠Modifier表达式/小数百分点支持 |
| Conquest/ELIG | [D0010](Specialization_D0010_Architecture_Sync.md)、[D0007](Specialization_D0007_Architecture_Sync.md) | 玩法已定、适配未完整；不要把原owner不匹配“修复”为清空成果 |

[旧完整索引](../../Historical/DocumentSnapshots/Technical_Index_before_fresh_agent_handoff.md)保留早期专项定位；不要求新代理先读每个历史探针。Great Work线索在剩余研究中，不是已经实现完整作品效果。

- [B052标准化永久账本](Specialization_B052_Standardization_Ledger.md)：D0015运行分类/一次补录/事件增量；无购买效果，实机待用户。

- [B053购买货币实验](Specialization_B053_Purchase_Currency.md)：当前手动实验，D0016允许隔离困难时双币折扣，原生效果待用户。

- [B054自动网络标准化折扣](Specialization_B054_Network_Discounts.md)：当前来源/模板并集、最高等级、后台Gold许可及撤销；待用户实机。

- [B055 网络Boost / Great Work接口](Specialization_B055_Boost_GreatWork.md)：自动原生Boost配置与手动巨作对照，本地证据不等于实机通过。

- [B057最终整数Boost量化](Specialization_B057_Integer_Boost_Contract.md)：D0018设计、隔离整数写入实验；正式自动量化待实机结果。

- [B058正式整数网络与巨作基础计划](Specialization_B058_Boost_GW_Basis.md)：D0019逐件差额，作品倍率后端仍在研究。

- [D0021时代对话](Specialization_D0021_Dialogue_Across_Eras.md)：取代旧逐件补差；EraType依据、统一文化/固定旅游候选和最小主题化对照。

- [D0022时代对话百分比](Specialization_D0022_Dialogue_Percent.md)：取代固定yield；creator时代及文物例外，ScalingFactor映射。

- [B059时代对话实现](Specialization_B059_Dialogue_Implementation.md)：自动创作者时代百分比；原生Culture/Tourism/theming待用户实测。

- [B059.78事件刷新修复](Specialization_B059_Event_Refresh_Fix.md)：取消周期扫描，延迟ACK防重发；用户先复验性能。

- [B059.79初始化恢复](Specialization_B059_Initialization_Recovery.md)：无城市玩家guard、失败ACK与可见诊断；78性能已用户确认。

- [E2其它Mod城市事件处理参考](Specialization_E2_Other_Mod_City_Lifecycle_References.md)：GCO关联事件、AutoPlay/原版FOUND_CITY正面证据、HD定域缓存、Captive Leaders回合核对；仅静态调查，不关闭B105门禁。
