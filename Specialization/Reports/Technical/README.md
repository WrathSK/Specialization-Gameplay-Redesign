# 按问题查找技术证据

从[架构系统说明](../../Architecture/Specialization_v0.1_Architecture.md#系统如何组成)了解结构；这里回答“依据在哪里、结论能用到哪一步”。当前任务/授权/待测只看[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)。文件较旧不代表结论无效，较新也不自动覆盖不同接口的证据。

## 城市身份、保存与事件顺序

| 问题 | 优先资料 | 仍须保留的边界 |
|---|---|---|
| 当前进度怎样保存、哪些档受支持 | [E2当前切片及完整合同](../../Architecture/v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing) | 当前实现与历史adapter分开；不能用旧City Property说明覆盖Game侧新记录 |
| 为何不能仅看事件“看起来连续” | [B105原生事件反证](../../Status/Validation/Results/Specialization_B105_E2_Event_Boundary.md)、[B106正面建城证据](../../Status/Validation/Results/Specialization_B106_E2_Found_City_Pass.md) | 首个Publish不保证事务已结束；后续FoundCity证据只限所测路径 |
| 其它Mod怎样处理生命周期 | [其它Mod参考](Specialization_E2_Other_Mod_City_Lifecycle_References.md) | STATIC证据，不是本项目所有原生事件路径PASS |
| 已证明的夺回、双城和新城范围 | [夺回结果](../../Status/Validation/Results/Specialization_B103_E2_Recapture_Pass.md)、[双城结果](../../Status/Validation/Results/Specialization_B104_E2_Two_City_Pass.md)、[新城结果](../../Status/Validation/Results/Specialization_B107_E2_Fresh_Registration_Pass.md) | 各检查点限定场景，不能合并宣称B108新局三城已验收 |
| 为什么缺失记录不能由区域补造 | [丢史反例](Specialization_Load_History_Ambiguity.md) | 缺失历史不等于确定无专业，不能猜旧首次完成 |

## 商路、传播与性能

- [B129征服/过回合内存调查](Specialization_B129_Event_Memory_Investigation.md)：当前内存调查入口：已确认的局部冗余修复、原生手动GC与副本生命周期证据、B137原生Network隔离结果与GC猜想核对（Lua净增长减小、进程增长未消除）；[B138有界稳定化试运行](Specialization_B129_Event_Memory_Investigation.md#b138165--bounded-stabilization-trial)增加单入口自动GC、更新接入约束与一次验收退出标准；根因仍OPEN，未宣称内存修复PASS。

- [后台UI来源用户决定](Specialization_Network_Background_Source_Decision.md)：允许不开贸易窗口取当前路线；[纯Gameplay第二轮审计](Specialization_Trade_Authority_Second_Audit.md)未找到可靠全集，不等于证明绝对不存在。
- [传播合同导航](../../Architecture/v2/README.md#事件传播与网络基础合同)：A–D2共享事实、样本/ACK、撤销和dirty传播；不同专业收益仍各自解释。
- [短时idle milestone](../../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)：不等于55GB长局问题根因已解决；[观测工具调查](Specialization_B072_Runtime_Audit.md)亦不证明所有原生文件能力可用。

## 收益精度与原生效果

- [已知限制/反证索引](Specialization_Implementation_Caveats.md)：住房/GPP延迟、旧档挂载、总督事实时序等均保留测试场景；其中旧任务状态不能派工。
- [每人口小数](Specialization_Fractional_PerPopulation_Evidence.md)、[HD政策0.3/0.2/0.7调查](HD_Policy_Fractional_PerPopulation_P0D1.md)：每人口路径不能推广为区域平坦收益或每专家任意小数。
- [区域精度实验](../../Architecture/v2/P0_D1_District_Precision_Probe.md) → [正式科研floor路径](../../Architecture/v2/P0_D1_Research_Cross_Cutover.md)及[用户结果](../../Status/Validation/Results/Specialization_B084_P0D1_User_Pass.md)；[每专家floor](../../Architecture/v2/P0_D2_Research_Apply.md)是另一计算层级。不能把一个接口的成功/失败变成全引擎精度定理。
- [标准化账本](Specialization_B052_Standardization_Ledger.md)、[原生购买实验](Specialization_B053_Purchase_Currency.md)、[自动折扣](Specialization_B054_Network_Discounts.md)：保留旧实际技术路径；新Industry生产加速目标不能由旧购买折扣证明完成。

- [意义延展文化追加定域调查](Specialization_B155_Meaning_Culture_Path.md)：当前S/G整数证据、Culture候选失败与B055单flat证据边界；市政／外交暂排为用户已授权条件后备，尚未改Design或运行包。

## 呈现与候选接口

[机构/能力/carrier调查](../../Architecture/v2/Presentation_Institution_Carrier_Model.md)定义分层；[科研展示原型](../../Architecture/v2/U1_Presentation_Prototype.md)限定HD hook、surface、缓存和隐藏范围。[目标技术spike](../../Architecture/v2/D0032_Technical_Spikes.md)是未来依赖接口，不是已实现清单，也不自动成为当前任务。

## 早期报告与取代关系（历史导航）

下方保留既有专项链接。表格和报告中的版本、待测、下一步只描述原时点；其中算法/API反证仍可按问题查阅。尤其旧科研复制、旧Culture对话、旧Commerce汇聚不代表当前冻结设计。接受规则看Design，当前实现看架构当前切片，验收看Status关联结果。

| 问题 | 优先资料 | 已知结论/不要重复 |
|---|---|---|
| 旧科研复制范围调查 | [D0014](Specialization_D0014_All_District_Copy.md)、[B051.66用户结果](../../Status/Validation/Results/Specialization_B051_66_User_Result.md) | [B051.67](../../Status/Validation/Results/Specialization_B051_67_User_Result.md)最小补测口头通过，非全部组合；旧四类白名单已废弃 |
| B051自动刷新 | [实现](Specialization_B051_Automatic_Copy_Yields.md)、[事件修正](Specialization_B051_Background_Fix.md) | 65失败、66收益用户通过；不能只凭只读计算值认定载体已挂 |
| 早期标准化目录/账本研究 | [目录快照：范围见D0015](Specialization_Standardization_Catalog_Candidate.md)、 [记录研究](Specialization_Standardization_Storage_Research.md)、[剩余研究](Specialization_v01_Remaining_Work_Review.md) | 该行描述早期研究时点；后续账本/折扣见下方B052–B054报告，当前任务不由此派发 |
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

- [B059.78事件刷新修复](Specialization_B059_Event_Refresh_Fix.md)：取消周期扫描，延迟ACK防重发；当时复验要求仅为历史。

- [B059.79初始化恢复](Specialization_B059_Initialization_Recovery.md)：无城市玩家guard、失败ACK与可见诊断；78性能已用户确认。

- [E2其它Mod城市事件处理参考](Specialization_E2_Other_Mod_City_Lifecycle_References.md)：GCO关联事件、AutoPlay/原版FOUND_CITY正面证据、HD定域缓存、Captive Leaders回合核对；仅静态调查，不关闭B105门禁。

- [项目点击拦截与完整生产回合](Specialization_Project_Action_Interception_and_Full_Turn.md)：原版/HD点击链、溢出修复Mod与AddProgress边界；商业入口可原型验证，时代对话占用合同仍待技术验证，未实施。
