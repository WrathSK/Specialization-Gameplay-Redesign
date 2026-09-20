# P0-D1 — 科研三级「跨学科研究」具体计划

Status: AUTHORIZED / PRE_CUTOVER_GATE_OPEN. 用户已授权实施；见[P0-D1门禁结果](P0_D1_Primitive_Gate.md)。以下为获准原计划；原生精度门禁未关闭，尚未正式cutover。
Authority: Design D0035 / Research D0031 RES_L3_CROSS及district_qualification；Shared D0035；Architecture A0161 / D0032_Implementation_Plan P0-D1。
Baseline: B081.108/modinfo108，runtime6736fc5；P0-C用户Pass见89020ae。v0.1仍仅科研/文化/工业/商业；Military不加入。

## 2026-09-20 用户增量（优先于下方历史市级承载措辞）

收益必须体现在区域；备用0.5/1是最终收益步长，不是转换系数。本轮[区域精度实验](P0_D1_District_Precision_Probe.md)先验证原值，不实施量化/正式cutover。旧writer保留；W0003允许已本地验证的实验包部署。正式区域落点与量化舍入若需要改变明确规则，不能自行补定。

## 目标

当前Research Identity、Potential及ACTIVE达到III时，本城合格非学院区域的BASE相邻产出总和×0.5，提供额外基础城市Science。IV继承此能力。不是每名专家收益，不乘人口、不乘专家、不乘D，也不采用Yield Share的Gold×3换算。

九类：工业区、军营、剧院、政府广场、外交区、商业中心、港口、圣地、社区；特色替代归一。仅已完成且未掠夺区域；未知类型排除并在详情说明。读取区域各yield的BASE相邻，不读建筑/专家/城市总产出，不含政策等相邻倍率。区域没有某项相邻可为verified zero，API不可用不能当0。例：合格BASE总和7 => +3.5基础Science，仍受正常城市Science倍率结算；不是城市总Science=3.5。社区多实例按本能力合格区域求和，不套D consumer的highest-single-district规则。

## 当前源码证据与范围

- Lv3Effects.lua仍给Research III/IV施加人口×工作科研专家×0.5 Science；Data/Lv3Effects.sql对应8个RESEARCH bit。必须退出此旧收益，Culture人口分支/Commerce connected-kind分支保持。
- UI/IndustryRefresh.lua用plot:GetAdjacencyYield读取BASE Production；仅Industry且整数0..255。可借用接口调查和C2运输，不可照搬其整数/范围断言作为新Design。
- UI/CopyYieldRefresh.lua读district:GetYield六项actual；不是本能力输入，Industry正式Copy不改。SampleLifecycle当前Live/Receive有industry布尔选择与两个数值槽；不是现成九域BASE合同，需窄适配/独立channel，避免改变旧通道payload意义。
- Gameplay启动/Action/worker诊断、NetworkBridge间接Audit、CityInheritance历史入口需实施时全量ID/caller复核；出现调用不代表启用继承模块，本批不恢复ownership实验。
- P0-A CurrentSpecializationFacts、领域归一、RuntimeWork及C2 single-flight原则复用。D0035仅澄清D，本能力不消费D；Lv2 Housing和P0-C不改。

## 实施顺序与technical gates

1. 先冻结8旧ID及所有动态writer/SQL attachment清单，复核完整相关源文件与调用者；准备B081完整恢复点及切换前独立存档。
2. 先纯计算与BASE producer：九域归一/完成/掠夺/当前城市引用；逐区域六项基础相邻组成；Gameplay拥有资格，UI只提供必要BASE样本。若Gameplay能可靠直接取得等价BASE，则避免新增跨context请求；不能未经证据假设可读。
3. 独立验证数值primitive：固定城市yield曾截断；旧半点和P0-C整数专家Science都不证明本能力任意小数可结算。验证BASE口径与政策倍率隔离、0/整数/半点及实际环境出现的更细小数。保持0.5×sum精度，不floor、不挪成专家收益、不用人口作为Design替代。没有等价可靠路径就报告TECHNICAL_INVESTIGATION_REQUIRED/限制，停在门禁，不先拆旧writer；不能以仅纯模型完成宣布本批完成。
4. 门禁通过后单一新writer与精确cutover同批：停止Research人口分支及8旧SQL效果附着，保留可识别旧Type/Building tombstone并清理实例；确认清理成功后启用新投影。不能整文件退出Lv3Effects，不能按SPC前缀大清理。新carrier ID/数量由primitive选择后明确锁定，不在规划阶段假定上限/cap。
5. 按需简明诊断、生命周期/性能回归、commit/push。仅在授权实施且W0003仍有效、游戏退出、恢复点/hash/干净提交等门禁满足时部署；本轮不部署。需原生prototype时用最小独立验证，不把半迁移包称完整候选。

精确旧清单：BUILDING_SPC_DEV_LV3_POP_RESEARCH_0..7及SPC_LV3_POP_RESEARCH_0..7附着/参数；新收益不可与旧人口Science叠加。P0-C退出的48旧Research IV不可复活；B050半点实验状态单独检查，混合实验不当验收结果。

## 生命周期与性能

复用C2合同：逻辑sample single-flight；pending重复通知不实际发送；epoch/request/current city+district reference匹配且完整验证才替换；相同样本no-op；暂不可用保留last verified，确认资格/区域失效准确撤销；load清旧pending，不误用旧epoch；retry有界（优先复用现行上限，实施测试记录准确次数）。不把一帧Publish当数据变化。

直接dirty来自区域完成/移除/掠夺修复、邻接地块/改良/地貌/资源/归属改变、真正改变BASE的规则事实、Research资格及load。政策事件可用于必要重核但BASE未变不写；无关worker/人口变动不改变公式。已知上下文尽量限定受影响城市；每玩家每回合最多一次低频兜底，样本过期/UNKNOWN不伪造空集合。

一次更新共享区域事实与样本，不逐城市重复全国capture；排除内部carrier自身事件；不增加每帧/每秒扫描、hover请求或逐事件日志。仅必要fixed counters：attempt/send/apply/reject、扫描/实际writes复用现有计数。

## 本地验收

- 九域、特色、未知类型、Campus排除、完成/掠夺/修复、多社区；BASE与actual/policy分离；多yield求和、0/奇偶/小数总和，公式逐值比较。
- Identity/Potential/ACTIVE II/III/IV，人口/专家变化不改本项；P0-C专家Science独立正常。
- 10000重复pending/无关generic通知：实际发送有界、无额外昂贵扫描和carrier写；重复响应apply一次、过期/乱序拒绝、UNKNOWN保留、确认失效撤销、重试上限、load新epoch。
- 预置8旧carrier准确清理，清理失败HELD，不执行新效果；旧load/晚到样本/手动诊断不能重建；48旧IV仍无效果。
- 1/2/4/8城统计fact reads/sample sends/city checks，线性增长；同输入重复审计零写；正常案例无隐藏module error。
- P0-C/B1/B2、Culture/Industry/Commerce及Network输出保持；历史回归用明确expected delta，仅排除本批旧Research人口效果；不能双方报错同0当PASS。
- 全Lua/SQL/modinfo、全部相关回归、部署安全、Design字节无变化。STATIC/LOCAL证据与USER_GAME_TEST分开。

## 最小未来用户测试

复用一座科研III测试城和两个已有合格领域。诊断读BASE组成及×0.5预期，对照原生Science；方便时切一张相邻倍率政策，确认actual变而BASE贡献不变；ACTIVE II→III和保存重载合并一次流程。优先准备总和为奇数的案例覆盖半点。专家变化只核对本项不依赖专家，不要求城市总Science不变（B1/P0-C仍生效）。不要求用户人为掠夺；相关边界先本地模拟，实机未测明确保留。若接口门禁需要更小prototype，先只请求该无法本地证明的行为。

默认诊断约五行：能力/ACTIVE；合格区域数与BASE总和；预期额外Science；配置值/旧8残留；READY或具体HELD。右键详情逐区域各yield BASE和排除原因。无关住房/GPP/工业报告不拼接；配置不冒称原生实测。

## Exit / rollback / next

Exit：仅RES_L3_CROSS完成、单writer、旧人口效果退出且其余模块保持，可靠BASE/小数路径有分级证据，本地回归通过并commit/push，用户测后独立登记。若primitive未通过，停止并明确未完成cutover，不改Design。无新Blocking Design Decision；有BASE口径与数值primitive technical gates。

整包回滚B081+切换前独立存档；新载体进入存档后不保证直接降级兼容。不做存档/ownership迁移，不实现学以致用(P0-D2)、主持/传统、Network重设计、其它专业、UI polish或Catalog大扩充。新批次建议P0-D2，完成D1后停止等待单独计划/授权。
