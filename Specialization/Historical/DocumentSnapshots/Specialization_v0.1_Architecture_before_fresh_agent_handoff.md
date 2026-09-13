<!-- Frozen handoff snapshot. Historical assertions only; current README/Status supersede. Relative links rebased; exact original bytes in DevelopmentBackups/Specialization-before-fresh-agent-handoff. -->
# Specialization v0.1 Architecture — A0110

Document Owner: Codex
Architecture Revision: A0110
Design Spec Synced Through: D0014
Design Spec SHA256: 759365dd68c3b4a166b0f05e250b72f14e33dcc145c3889f6afefa16f999005c
Sync Status: SYNCED_WITH_LIMITATIONS
Latest Accepted Design Revision: D0014
Latest Accepted Design SHA256: 759365dd68c3b4a166b0f05e250b72f14e33dcc145c3889f6afefa16f999005c
Implementation Build: P0-B-051 / modinfo67

## CURRENT AUTHORITATIVE STATE

**D0014 / B051.67当前：** [所有非Campus区域复制](../../Reports/Technical/Specialization_D0014_All_District_Copy.md)。用户已明确范围，不再以四专业或人口名额白名单限制，后台/Gameplay/报告同步扩展。无产出区域0贡献，不中止整项；继续Actual getter及原50%承载。工业4.5与科研半点已按用户回报通过，扩展类型需原城最小复验。原66及此前范围未决/窄限制描述仅保留历史，不覆盖D0014。

**B051.66调度修正：** [事件驱动与分段诊断](../../Reports/Technical/Specialization_B051_Background_Fix.md)。自动计算与UI只读候选分开显示；加入已用的引擎发布/播放/回合/加载事件与初始化fallback，不依赖单一空context逐帧更新。仍后台运行、当前资格重核、未知撤销；不改变数学/SQL/目标范围。modinfo65实机未发放，修正仅本地通过，具体失败阶段待用户新报告确认。

**B051 / 恢复实施：** [自动科研IV本地复制与工业IV网络输出](../../Reports/Technical/Specialization_B051_Automatic_Copy_Yields.md)已接后台区域Actual读取、Gameplay当前资格重核、绝对city层载体、人口重算及撤销。整数/半点采用B050路径，不支持更细值时明确限制而非取整。四专业以外区域范围不静默猜测；来源不读城市总量。静态与本地模拟通过，原生自动发放/反馈隔离/读档需用户三案。D0013标准化学习规则仍有效，尚未实现；本轮不修改Spec。

### HISTORICAL NOTES / 以下为此前阶段记录

**D0013 / 研究暂停实现：** IND-NET-004确认任何合法获得/完成、首次Industry一次补录、后续事件增量、HD Tier与允许范围双门槛。架构适配为一次初始化事务+事件目标复核，永久城市账本/当前网络并集分离；尚未实现，具体允许清单不自行扩展。[剩余工作与方案研究](../../Reports/Technical/Specialization_v01_Remaining_Work_Review.md)列9个机制与3个集成工作包。B050两种半点组合已用户通过；仅支持本批，不外推任意小数。运行仍B050/modinfo64，本轮不改Source/Tests。

**B050：** [二进制每人口系数+整数扣除实验](../../Reports/Technical/Specialization_B050_Half_Yield_Experiment.md)独立ON/OFF；只验证固定半点，不作为正式复制或任意小数承载。人口变化/重载重算，原生精度/倍率待测。[标准化记录研究](../../Reports/Technical/Specialization_Standardization_Storage_Research.md)采用城市永久账本候选+带版本district/tier目录+当前来源并集；学习授权由外层明确提供，不猜触发，尚未接游戏。D0012/hash不变。

**B049/modinfo63：** [读取已实测与提示整理](../../Status/Validation/Results/Specialization_B049_User_Result.md)。水力作坊非相邻产出及工业最高来源撤销按用户范围通过。展示层区分新鲜空集合、接收但无ACTIVE4源、未知/等待；原始异常仅日志保存。不更改网络新鲜度要求、不将unknown转0。固定50%小数收益仍未接入；D0012不变。

**B049：** [移民展示层与Lv4复制准备](../../Reports/Technical/Specialization_B049_Settler_UX_Lv4_Copy.md)。展示复用既有资格核对，投资/Crew结算不变。NetworkBridge新增只读接收source accessor；Gameplay输出新鲜身份，UI区域GetYield计算科研标准区域小计与工业实际输出max。当前无复制收益/持久缓存，未知不充0；固定50%精度与非传统区域范围保持边界。B048百分比已用户通过；D0012及hash不变。下方早期阶段不覆盖当前状态。

**B048 RES-004/CUL-004百分比组件：** [原生city yield modifier与自动carrier](../../Reports/Technical/Specialization_B048_Lv4_Percent.md)。ACTIVE4对应专家人数×5个百分点，科研/文化独立；沿用已验证的计数/背景刷新链路，原生Tooltip作效果观察。其它Lv4组件分开推进，未宣称已完成。D0012设计/hash不变，当前A0104更新HOW。

**D0012 / B047：** 用户已接受Crew缩放后向下取整并显示整数；[共同金额函数与验证](../../Reports/Technical/Specialization_D0012_Integer_Crews.md)。快速五档167/281/502/670/911，项目成本继续原生计算。原执行函数、消费/限额顺序不改；其它系统不套用floor。A0102已同步D0012，关闭此前取整DESIGN_DECISION_REQUIRED。下方D0011/B046待决属于历史。

**B046精度边界：** [用户观察与候选整数适配](../../Status/Validation/Results/Specialization_B046_User_Result.md)登记一级提示167.5/实际167，不能再假定本路径完整保留浮点。项目成本观察符合floor；HD百分比注入有floor先例，但不证明引擎所有内部量化机制。候选floor(档位×速度)待用户设计确认，非已部署fallback。D0011原文与运行包未改；五级实际及空花例外待澄清。以下阶段性“待回传”不覆盖此结果。

**B046：** [HD列表归组适配与只读精度观察](../../Reports/Technical/Specialization_B046_Project_Precision.md)。保持HD所有项目对象，只调整Crew列表位置；观察器包裹原确认函数，不改变结算，不自动补发。原生GetProjectCost/确认前后进度分别读取，跨目标不能相减。快速速度精度待用户回传；D0011未更改。以下B045及更早为阶段历史。

**当前B045 UX：** [固定90像素槽位与临时预览读取](../../Reports/Technical/Specialization_B045_Crew_UX.md)：施工按钮固定右侧，确认显示于左侧；重复预览无请求。后台View复用原fresh/queue读取以更新展示与撤销过期预览，不改Run执行、目标/生成/金额。D0011不变。原生像素布局待用户复验，以下B044为阶段历史。

**当前B044：** [五档项目与提示](../../Reports/Technical/Specialization_B044_Crew_Projects.md)：原生项目完成Modifier生成独立Crew；资格为从Identity工业专业重建的无产出标记，非相邻/专家载体。五档共享查表与速度浮点金额，保留现有限额消费，不添加事件发奖或永久缓存。B043用户通过；原生项目生成/重复/重载与非标准精度未实机。已同步D0011，未擅定取整。下方B043及更早是阶段历史，不覆盖本段。

**当前B043/D0011：** [单位面板与提示](../../Reports/Technical/Specialization_B043_Unit_Panel.md)已本地通过，原面板挂接待实机；B042全部用户通过。D0011确认五档工业Lv1全开放、成本/施工力随速度同比缩放，五正式项目待实现，精度另核对。下方D0010/B042等是历史阶段，不覆盖本段。

**当前B042：** [独立Crew250与共同单位动作](../../Reports/Technical/Specialization_B042_Crew_Unit_Actions.md)部署。DEV免费生成、真实消费和限额生产力，独立builder外观/1charge；新投资入口站Identity区域，复用旧账本，旧中心入口保持。非原子异常停止不自动补发。五正式项目未实现，游戏美术/执行待实机；B041奇观已用户通过。

B041.54奇观候选列表改由HD UI GetCityPlots helper读取，Gameplay仍核对当前目标/地基/归属；修正上下文风险，不以UI列表直接授权。其它类型已用户通过，奇观修正待单项复验，见[记录](../../Reports/Technical/Specialization_B041_Wonder_Bridge_Fix.md)。

**当前B041/modinfo53：** [目标枚举与独立地图标签](../../Reports/Technical/Specialization_B041_Target_Markers.md)已部署，本地通过，实机待[三案](../../Status/Validation/Cases/B041_Target_Markers.md)。移民自动INVEST，工人显式BUILD TEST；不使用共享伟人图层、不消费、不改投资。奇观从城市地块枚举，不再只验脚下。以下B040及更早是阶段记录。

B040位置读取已按[用户结果](../../Status/Validation/Results/Specialization_B040_User_Result.md)通过。[单位高亮调查](../../Reports/Technical/Specialization_Unit_Action_Highlighting.md)采用自算目标列表+绘制方向；需解决全集目标枚举与共享图层清理时序，尚未部署、不改Spec。

B040/modinfo52仅修正独立界面的初始化与根显示；入口对测试文明常显，选择条件移到点击提示。位置读取/旧投资不变。见[可见性修正](../../Status/Validation/Results/Specialization_B040_Visibility_Fix.md)，尚待用户复验。

当前[B040单位地点读取](../../Reports/Technical/Specialization_B040_Unit_Sites.md)已部署：独立选中单位入口，Gameplay重新核对位置，投资Identity区域/施工当前目标候选诊断。只读无消费，工人仅代测位置；原投资/注入行为不变。本地通过，实机三案待回报。下方B039及更早条目为过程记录。

B039/modinfo50生产力注入已获用户人工通过，范围见[结果](../../Status/Validation/Results/Specialization_B039_User_Result.md)。正式Crew仍未实现。[施工队/移民共同单位动作调查](../../Reports/Technical/Specialization_Unit_Actions_And_Sites.md)与未加载的候选地块判定已本地完成；HD秦始皇按钮提供地基核对先例。施工站目标plot、投资站Identity区域是待接入/确认的候选位置规则，不覆盖D0010或当前市中心投资。独立UnitType复用builder表现、显式1charge；不能盲拷贝builder tags，不能照搬HD UI请求后无条件删除。下轮先定位及单位按钮，正式项目成本速度/开放仍TBD。


[B038文化小数证据](../../Reports/Technical/Specialization_Fractional_PerPopulation_Evidence.md)支持0.5每人口奖励在3人口城市保留并正常参与已观察宜居度倍率；本局Getter在1/256网格，精确内部取整算法未定，不推广到其它路径。D0010仍0.5，未启用用户愿意考虑的1。运行modinfo49不改。


[B038五图](../../Status/Validation/Results/Specialization_B038_Population_User_Result.md)确认Research4人口的实际原生总科技与人口奖励正确，自动/锁定人数始终匹配；问题是城市面板滞后，并非旧载体残留。此前假设由新证据取代。无代码更改；文化/奇数人口半点仍未验证，不扩大PASS。


modinfo49只增加[人口收益诊断](../../Reports/Technical/Specialization_B038_Population_Diagnostics.md)。科研自动分配/锁定序列失败，起始基准残留载体为候选解释，尚未确定；不归为已接受的GPP延迟。商业固定类型奖励按用户观察通过，7P为5+2，与工业来源相邻无关。文化待测暂停，公式/刷新未修改。


B038/modinfo48：[Lv3人口与网络专家效果](../../Reports/Technical/Specialization_B038_Lv3_Remaining_Effects.md)。按人数挂载原生per-population 0.5系数；商业类型集合去重，网络dirty先撤旧、完整批次后恢复。新效果待实机，晋升刷新修正已获用户确认PASS。所有既有延迟接受项不变。


modinfo47：[总督晋升刷新补充](../../Reports/Technical/Specialization_B037_Governor_Promotion_Fix.md)。增加GovernorPromoted即刻与后台发布后核对；旧先投资再晋升载体不刷新的缺陷有用户证据，修正本地通过但未实机。其它B037支持能力按用户人工通过。GPP过回合读数接受备注不受影响。


B037/modinfo46新增[Lv3专家支持差额模块](../../Reports/Technical/Specialization_B037_Lv3_Specialist_Support.md)：原生专家载体+2升级既有3为5；Industry金币2×基础相邻，复用后台样本。ACTIVE下降只撤销Lv3补差；仅本部分Lv3，其它能力仍待实现。静态/本地通过，实机待测。GPP全国率过回合刷新为用户明确接受行为，无修复/额外测试要求。


modinfo45仅[面板布局整理](../../Reports/Technical/Specialization_B035_Compact_Panel.md)：9常用按钮，其余Hidden容器保留定义与回调；GPP等Gameplay/SQL不变。[B035四类联合批次用户人工通过](../../Status/Validation/Results/Specialization_B035_User_Result.md)；25%与15%相加只记已观察组合，不据此统一所有收益算法。Lv4投资拒绝是现有安全边界，提示堆栈待优化。

当前B036/modinfo44：[工业Lv1专家收益适配](../../Reports/Technical/Specialization_B036_Industry_Lv1.md)。后台UI用Plot基础相邻getter，Gameplay验证城市/区域/专业锚点，9个原生专家收益载体提供3F与整数BaseP；无永久数值缓存、不复制actual、失败撤销并报告。Gameplay同名getter不作为前提。[B036八图与人工回报](../../Status/Validation/Results/Specialization_B036_User_Result.md)确认基础相邻1/4/6动态新增与政策不污染；原有工业专家2P保留，报告carrier只表示附加量。读档、网络接入/分发依人工通过；施工队未实现。共同Lv2 GPP B035保持部署，实机批次按用户要求延后至四类区域一起测试。

当前设计已同步Accepted D0010：[征服分流适配与缺口](../../Reports/Technical/Specialization_D0010_Architecture_Sync.md)。非空LegacySet、空集普通完成、已有Identity继承三类互斥，旧AcquireUnassigned通用完成入口已停用；新契约本地通过，原生snapshot/Claim/跨owner身份尚未部署。运行仍B034/42；住房五图结果见下。后文D0009及更早段落为对应版本历史，不覆盖本段。

当前B034/modinfo42：[五图及人工结果](../../Status/Validation/Results/Specialization_B034_User_Result.md)确认Research门控与两层住房开启、调离时载体撤销；城市面板9→6有事件刷新延迟，用户明确接受。changes在过回合前后均10，未再次删载体；没有同回合原生Housing Getter证据，具体缓存层仍未定。住房按观察范围通过，无补测要求；基础GPP未启用且为下一项。以下旧待测表述仅为历史。

当前B033/modinfo41：[三图及口头结果](../../Status/Validation/Results/Specialization_B033_User_Result.md)确认实际投资1→2、正常存读档、重复不消耗；Potential2总督动态门控与升级后新路线身份依人工通过。原有商路跨升级保持未测。Lv2–4收益未启用。

当前B032/modinfo40：[只读账本和统一事实](../../Reports/Technical/Specialization_B032_Effective_Facts.md)已接游戏初始化及Lv1/网络消费者，本地回归通过；无账本零写、旧专业记录不改。实际投资写入/移民消耗未开放，实机兼容验证与下一批升级合并。以下“运行不变”属历史阶段。

[HD先例与投资账本衔接](../../Reports/Technical/Specialization_HD_Sacrifice_Investment_Bridge.md)已完成本地候选；保留基础专业记录，新增凭据推导Potential，不复制可写总等级。下一步原生存储和统一消费者接入，运行不变。

[永久投资执行层](../../Reports/Technical/Specialization_Settler_Investment_Executor.md)新增离线有序消耗/确认/提交及恢复，未注册引擎；下一步衔接B020/B015持久记录，运行仍B031/39。

当前B031/modinfo39：[两图结果与标签修复](../../Status/Validation/Results/Specialization_B031_User_Result.md)。目的端失效撤销按范围实机通过；两个空白按钮改回英文，正文保留中文，显示待下次使用确认。网络Lua和设计未改，小数承载研究继续暂停。

当前设计为Accepted D0009，已完成[差异同步与实现差距](../../Reports/Technical/Specialization_D0009_Architecture_Sync.md)。运行B027已在限定DEV Lv1拓扑加入direct中心/首都自然接收，两组本地通过，纽约/阿伯丁两图实机按范围通过；新Commerce IV Convergence尚未实现。以下历次段落保留过程，不覆盖本段；B026旧N及自接收判据已由D0009取代。B031已按用户新优先级恢复可读性与撤销任务。

上一版Accepted D0008的记录：[D0008同步](../../Reports/Technical/Specialization_D0008_Architecture_Sync.md)保留Future各项成熟度，不扩大v0.1。此前已补齐D0006/7规则映射，见[本次同步与实现差距](../../Reports/Technical/Specialization_D0007_Architecture_Sync.md)。参与资格/永久成果分离已完成离线模型与五组模拟，见[资格模型](../../Reports/Technical/Specialization_D0007_Eligibility_Model.md)；真实资格系统尚未部署；已准备基于显式Trait绑定的只读API候选，见[载体调查](../../Reports/Technical/Specialization_Eligibility_Carrier_Research.md)。运行B018组合只读诊断两案按用户两图通过；B016两图已验证当前测试玩家自动资格读取/重载，B017明确54–61为CIV_NOT_READY但槽位身份未定。名单/资格生命周期已有离线候选，正式门控未接入。

游戏设计意图只以[Accepted Design Spec](../../Design/Specialization_v0.1_Design_Spec.md)为权威。本文负责实现方法、接口契约和技术限制，不再维护第二份数值表。此前D0001的SYNCED_WITH_LIMITATIONS表示完成该版规则映射并记录限制，不表示实现完成或游戏验证通过。当前已同步D0007的Rule适配与技术限制；Future经验API尚未验证，见[D0002差异同步](../../Reports/Technical/Specialization_D0002_Architecture_Sync.md)。

完整Rule ID覆盖、同步检查与遗留差异见[同步报告](../../Reports/Technical/Specialization_D0001_Architecture_Sync.md)。唯一验证矩阵和待办见[Status](../../Status/Specialization_P0_Status.md)。当前已完成离线多源强度和城市专业事实状态模型；运行B015 DEV新城记录，用户证据见Status中的B015结果，Mod UUID不变，B010仍未测；不启动游戏。

## 身份、存储与能力门控

适配SCOPE、ELIG、ID、TERMS、PROG。正式机制按独立PlayerEligibility参与资格门控，人类/AI同规则；不能固定文明、领袖或GetLocalPlayer。当前CIVILIZATION_SPC_TEST/LEADER_SPC_TEST/TRAIT为B015测试载体，展示与modinfo不变，IsTestPlayer不是通用资格实现。深度枚举与周期更新仅运行于enabled集合；休眠永久成果与运行状态分开。具体carrier、成本过滤及多人确定性待实现。区域族仍需审计，不能仅靠RequiresPopulation判断。

永久保存专业、Potential、首次完成事实、标准化模板及不可重复动作凭据；Identity取得必须携带有效来源证据：普通模式为完成通知；D0010 Legacy模式为冻结候选内Claim完成，不伪造首次区域完成。不能从已放置区域猜测。商路、总督条件、网络来源/接收/强度均为可重建派生状态。城市UID映射层尚未实现，owner/cityID仅为当前引用，中心plot不是永久UID。征服保留永久事实已由PROG-004确定；跨owner永久UID为技术限制，旧档初始化为OPEN-04实现/未来兼容事项；普通完成通知先后按PROG-005；征服接管时的一次快照按PROG-006建立候选，不是反推历史Identity，也不适用于旧档补初始化。

ELIG-005四种取得情形必须分流：从未启用且无成果进入未专业化；enabled→disabled保留成果但无Lv1效果；休眠→enabled恢复重算；enabled间转移保留并重算。Property缺失不证明从未参与，取得未专业化城不伪造新建城事件，现有区域不能推断历史专业。

总督使用原生Requirement→城市Property门控：1为激活，nil/0不激活，不能用Lua truthiness误判0；不重试已失败的GetAssignedGovernor。门槛数值和ACTIVE计算只引用PROG-003。原生条件不能反推出全部Mod免费晋升历史。当前CityRoleFacts只读诊断，不是专业/潜力写入层；多人确定性未验证。

### Trade Route State：强制契约

流程：`后台当前路线完整读取 → 传递Gameplay → normalize → deduplicate → 全量替换 → source connections → distribution recipients → per-network recipient sets`。

用户已明确接受后台读取UI/BTS当前数据，限制仅为不得依赖玩家先打开窗口；[来源决定](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md)取代旧纯Gameplay前置要求。采用BTS/原版同源的City:GetTrade():GetOutgoingRoutes，独立后台上下文自动执行。既有后台初始化/读档/新增/删城证据保留；B026桥接、首都/商业中心连接与分发及正常重载已按用户八图范围验证，当前桥接的撤销链路仍待验证，不因BTS可靠就自动升级本Mod的验证结果。

离线DevelopmentTests/TradeRouteState.lua当前仍只接收COMPLETE/GAMEPLAY/GAMEPLAY_CURRENT，是待适配的旧代码契约，不再是设计限制。下一步显式支持已授权的后台当前数据来源，保留完整批次、来源/加载代次/城市身份检查，不把UI来源伪装成Gameplay。失败、部分列表、未知或历史事件仍不能提供可结算网络；纯Gameplay枚举不再阻塞后台路线主线。

成功全量刷新原子替换集合，集合中消失的路线撤销；重复刷新不累计。额外核对端点存在、当前owner/cityID、战争状态；明确不存在或易主撤销，解析失败则整次UNKNOWN。事件仅标dirty，重复dirty合并；初始化/读档不依赖事件历史。未来provider必须有安全就绪时点、同回合dirty处理和回合核对。Gameplay任务探针在初始化、LoadScreenClose、测试玩家回合边界读取；UI影子采样另在事件发布/播放完成边界处理dirty。两者不混作Gameplay权威全集。

Route record：key、identityKind、可选engineRouteID/traderUnitID、originPlayer/originCityID/originUID、destinationPlayer/destinationCityID/destinationUID、domestic、current、validity。没有 UI 名称、路径 plot、yield 表。优先实际引擎 route ID（若以后证实）；目前未发现暴露的稳定 route ID。备用key为带长度前缀的 owner+traderID+originUID+destinationUID，只保证当前快照内识别与刷新去重，不宣称跨单位ID复用/新旧同端点任务拥有永久身份。所有字段重新读取，不用key继承旧current状态。同城对不同商人分别保留；同一商人冲突记录拒绝整次刷新。

NetworkState 原型保存每中心 connectedSources[sourceUID][qualification]、distributionRoutes；每类型 recipients[cityUID] 保存 source集合、center集合及中心→源→接收资格。源信息含owner、kind、activeLevel、templateRevision。routeRevision 与 contextRevision 分开：中心身份、ACTIVE、模板变化无需修改路线事实，但需重新派生。拓扑原型本身不计算L；独立NetworkStrength.FromState消费一次派生结果，在MOCK_ONLY契约下计算Research/Culture强度，不发收益、不注册到modinfo。

### 虚拟建筑作为网络标志：候选，不作为权威事实

用户提出每类型网络一个虚拟建筑的构想。保留为效果载体/可重建标志候选，暂不实现。真实路线与多来源资格集合先计算，再对账建筑；失去最后资格才移除。单个建筑布尔值不能表达方向、源城市、多个等级/模板与支撑路线，不能只靠建立/结束事件建拆来解决漏事件、旧档初始化。源或中心网络变化时，即便路线不变也需重算。内部建筑可能影响第三方建筑统计，需专项验证。详见B005_User_Result。


## 专业效果适配

| Spec规则 | 实现方向与边界 |
|---|---|
| SHARED、RES、CUL、IND、COM | 工作专家计数读取已有基础证据；正式收益层未接入。基础GPP必须进入可受百分比影响的层，不能以ChangePointsTotal替代。承载建筑需验证岗位估值/第三方建筑统计；城市补贴不自动等价于岗位产出。升级替换与独立能力保留按SHARED-003。具体数值只查Spec。 |
| TERMS-002、RES-004、IND-004、GW-002 | 分开提供BaseAdjacency与NativeDistrictCopyBasis。后者追踪煤电厂/大酒店原生复制基数，不以GetAdjacencyYield或城市总产出替代。Building_YieldDistrictCopies仅有BuildingType/OldYieldType/NewYieldType，无比例或跨城目标字段；需独立适配。先读取全部源再统一应用，防止把补贴反馈进源。行业固定收益、跨yield与特殊区域范围尚待验证。 |
| NET、NET-RC、COM-003 | 保留source/center/recipient资格，接收城市按UID去重；离线强度计算层已适配NET-RC-001至004，保留005精度边界。max选择只对有效ACTIVE源执行，空集显式归零；独立k参数不与路线数耦合。Industry按IND-NET-003独立比较实际output，不从Research/Culture的最高L虚构工业源；Future独立规则保留。NetworkState保留来源；NetworkStrength.FromState执行聚合。 |
| COM-004至008、COMPAT-002 | 独立Convergence计划；按有效direct source的eligible本地产出选最高，不能按ACTIVE选源。独立basis接口排除跨城Specialization输入；精确读取、承载、刷新/撤销、小数待技术调查，不用最终城市yield或区域Actual替代。见D0009同步报告。 |
| NET-RC-005 | Lua先算未取整浮点，独立BoostAdapter负责引擎应用。数据库TEXT只证明能存，不证明Modifier支持动态表达式/小数。精度与量化按OPEN-06待决；先调查引擎，不能静默整数化或退回线性模型。 |
| IND-NET | 模板按完成事实记账，使用当前有效来源资格匹配区域/tier；未识别建筑不能扩成整区折扣。Gold-only作用域须独立验证，若只能同时影响Faith，报告IMPLEMENTATION_LIMITATION并交用户决定。多源按IND-NET-003分别取模板并集、最高折扣与实际IV输出；模板和折扣可不同源。 |
| CREW | 固定Project→单位规格数据只引用CREW。生产注入先核对合法当前目标/剩余量，按min应用，拒绝非法目标且不消耗；队列切换、重入和消耗凭据需防重放。AddProgress/原生生产Modifier/HD先例仍需实测比较，不能假定无溢出。 |
| GW | 隔离GreatWorkSubsidy适配，优先城市基础补贴；不要求直接改对象。类型/时代曲线依OPEN-08，不能以最高作品猜标准。城市补贴的Tourism、theming、作品专属倍率/UI不等价于作品内在yield；保值与Base相邻补贴分开计算，白名单审计不靠本地化名称。 |

## Future适配边界（只记录，不实现）

完整Future Rule IDs及逐组适配见同步报告。所有Future均OUT_OF_V0.1，不能因接口预留而注册正式收益。

- GOV-002：未来以永久投资事务+已授予档位账本防止重复发放，授予与ACTIVE效果刷新分离；读档/总督移动不能重复支付或收回。头衔增加API和保存原子性尚待研究，不宣称已可用。GOV-003另由ACTIVE/当前政府事件重算可撤销槽位。GOV-001的建筑互斥、自动完成重入、一次性效果需专项可行性验证，不能以少给建筑作为默认fallback。
- ENT：工作专家和有效专家计数分离；只在Spec明确允许的自制机制入口使用虚拟计数，避免污染基础产出/GPP。网络效率扩展留独立参数，不改变ACTIVE。
- SPACE：未来卫星完成资格与城市Spaceport状态分别读取，资格进入同一来源/接收集合，按原因维护撤销；不依赖可见UI，不为自动连接伪造商路。
- MIL-009至013：连续驻扎记录须观测中途离开；独立训练与战斗局部Mentorship分别结算/去重，不按全国单位关系扫描，公式已定不再整体列TBD；体系资格/分类/快照仍待明确，接口未验证。
- LAND/REL/MIL/HARB/DIP/COMM与辅助系统尚无完整技术验证；未定参数引用Spec OPEN，不在Architecture补全或擅自套用NET-RC合并算法。

## 当前技术适配与边界

- Gameplay事件只提供dirty/历史诊断；完整权威provider仍缺失。B005的端点参数nil是失败候选，不因UI已通过而变为可用。
- UI/BackgroundRoutes读取当前全集，校验数量、端点与商人冲突，完整替换。LoadScreenClose/回合可直接采样，GameCoreEventPublishComplete/GameCoreEventPlaybackComplete消费dirty；最多跨边界3次尝试。SystemUpdateUI与Context更新在用户截图中未观测到，不能依赖其10秒兜底。
- ShadowRouteState为READY_UI_SHADOW、复制读取、revision幂等、dirty即UNKNOWN；owner:cityID只是快照身份，没有永久UID。
- DevelopmentTests/NetworkState仅离线原型：原Derive拒绝UI，DeriveShadow接受明确UI影子格式+MOCK_ONLY角色。拓扑只保留来源，strengthStatus/industryStrengthStatus=NOT_CALCULATED；旧实现首都角色只加source不加recipient，与D0009冲突，待适配；旧freeSelfReceiver不能再代表Commerce IV。IndustryNetwork独立离线合并，非游戏结算。新离线NetworkStrength.FromState已完成Research/Culture max聚合，不接游戏效果。
- Probe.CityRoleFacts只读选中城市，专业/潜力写入者不存在，因此ACTIVE未知；首都候选与总督条件上限独立。B010实机待办已暂停，不能因模块存在判PASS。
- 以上均未接正式网络收益、Boost、折扣、施工队或巨作。


## IMPLEMENTATION_LIMITATION / DESIGN_CONFLICT

本次未发现必须修改D0001的已证实设计矛盾；未实现与尚未验证不等于不可实现。已知阻塞和潜在不等价如下，均未选择改变玩法的替代方案。

| 项目 | 限制及处理 |
|---|---|
| NET-004与纯Gameplay全集契约 | 当前后台UI能自动读取不等于Gameplay权威源已找到；保留原约束。若以后提出后台UI桥接作为正式事实，必须说明上下文/多人/时序影响并单独取得用户决定。 |
| ELIG / PROG / OPEN-04 / COMPAT-001 | 参与、休眠/恢复及继承语义已定；通用资格carrier、运行过滤、跨owner UID和旧档初始化为实现/兼容事项，不能从缓存推断。 |
| NET-RC / OPEN-06 | 浮点动态Modifier能力未证实；量化和封顶未定，不自行选择。 |
| IND-NET-003 | 多源合并已定且离线适配；Gold-only、实际output与来源权威仍需接口实证。 |
| TERMS/GW / OPEN-08 | 原生复制范围、时代标准与theming/Tourism适配需确认，城市补贴不能默认为完全等价。 |
| Future GOV/REL/DIP | 全建筑/信条/永久保护的引擎控制边界需后续专项调查；不以实现方便削减设计。 |

## 同步与审计

后续设计变化由用户确认，Codex维护Dxxxx；每次架构同步核对accepted Spec hash，按Rule ID报告覆盖与限制后递增Axxxx。同步不改Status已有证据等级。当前D0001自身保留的“架构尚待同步”句子是接受时记录，当前同步进度以本文header和Status为准；不修改已接受Spec造成hash漂移。

[A0001原样快照](Specialization_v0.1_Architecture_A0001_before_D0001_sync.md)保留过渡WHAT及调查；[早期完整架构](Specialization_v0.1_Architecture_before_phase1_B010.md)保留旧设计审计。旧线性/逐源求和/Actual getter及写入者措辞不覆盖D0001。专项技术入口见[研究索引](../../Reports/Technical/README.md)。

## A0003：离线多源强度接口

`NetworkStrength.FromState(state, player, coefficients, contextSource)`只接受显式MOCK_ONLY调用和已完成的单玩家拓扑。混合玩家来源/中心、UNKNOWN拓扑、非法ACTIVE/k或断裂接收资格返回UNKNOWN，不返回旧强度或伪造零结果。来源必须出现在当前中心connectedSources中；未接入高级源不参与。每类型全局选有效ACTIVE最高值，接收城市通过当前中心/来源资格去重，保留sources和maxSources供审计。连接到没有分发路线的中心的源仍属于有效接入源，按NET-RC-003参与全局L；N独立取实际接收集合。

输出包含routeRevision/contextRevision、player、networks.RESEARCH/CULTURE的L/N/k/networkStrength/sources/maxSources/recipients。缺少该类型来源或接收城市时给显式零强度；不存永久缓存。保留浮点，不提供Modifier Amount或取整方案。UI影子输入的输出仍标UI_SHADOW_ONLY，整体仅READY_OFFLINE_STRENGTH，不能变成Gameplay权威事实。真实角色/UID/路线可用性仍是外部前置。

[本轮本地结果](../../Status/Validation/Results/Specialization_Network_Multisource_Local_Result.md)记录测试和限制。未来其它合法接收方式可通过同一中心/源资格结构表示；本轮不实现Spaceport、Entertainment或Industry合并。

## A0004：当前全集来源复核

[第二轮静态调查](../../Reports/Technical/Specialization_Trade_Authority_Second_Audit.md)确认HD CityYield有Gameplay GameEffects先例，但可见原生商路collection仅联盟/紧急事件范围，尚不能导出普通己方路线全集与端点。不能从Modifier subjects局部集合推断全国当前路线。未产生足够依据的新探针，不重复B005坐标或B010测试。原Gameplay权威约束保持；后台UI桥接若未来作为正式来源，必须另案说明改变及由用户决定。此限制阻塞正式Network运行结算，不阻塞独立本地能力研究。

## A0005：离线城市专业事实与ACTIVE

新增DevelopmentTests/CitySpecializationState.lua，按PROG-001至004处理显式MOCK_ONLY输入；不注册modinfo，不读写引擎Property，不生成真实城市UID或消耗单位。NewCity要求当前enabled和新建城市证据；AcquireUnassigned使用独立取得历史凭据。Restore不从已有区域/旧marker推断专业；缺失记录返回UNKNOWN / OLD_SAVE_COMPATIBILITY_REQUIRED，所有权变化要求验证同城转移。失效城市/UID代际不符或损坏账本返回UNKNOWN。固定测试文明门控已从此模型移除；资格不限制永久事实保存，详见A0024。

永久schemaVersion=1包含cityUID、owner、revision、specialization、potential、firstCompletion(eventID/districtUID/family)、investments(receiptID→unitUID)。未选专业时不填Potential；Derive的active=0仅表示无专业能力，不增加设计Lv0。校验Potential与投资账本一致，恢复时投影永久字段，丢弃旧ACTIVE。每次操作返回新副本，错误不改输入。

Complete仅接受显式ENGINE_DELIVERY顺序、已审计区域family映射与明确完成状态；只支持v0.1四族，NON_V01忽略，未审计类型拒绝。按D0004 PROG-005取首个有效通知，之后不覆盖。CityCompletionJournal可逐个通知生成计划，不等待整回合结束；完整有序列表保留为离线兼容入口，不能以排序后的枚举结果替代通知。新城历史资格与真实处理器顺序仍需适配，详见A0019。

PlanInvestment先只读检查专业、上限、己方在城Settler资格及已消耗凭据，返回expectedRevision，不消费单位；CommitInvestment只接受显式已提交MOCK消费凭据，核对预期revision、重复receipt/重复unit与上限后形成新事实。真实单位消费+持久账本如何原子提交尚未实现；未来必须在交易边界重新核对资格并保障帝国级单位一次性消费，不能先消耗再任意失败。当前receipt不是可直接从UI信任的命令。

Derive消费原P0总督探针的KNOWN门槛上限及明确城市UID映射，计算min(Potential, ceiling)。总督缺席/未建立/调离的原生上限1不改变永久投资；无法读取、跨城或不一致门槛返回UNKNOWN，不把错误默认为缺席。使用现有Probe.CityRoleFacts的离线桥接测试不代表B010通过；真实UID映射与事件读取未接入。

[本地结果](../../Status/Validation/Results/Specialization_City_State_Local_Result.md)区分模型读档、Property游戏保存和真实Settler动作。后两项本轮未实现/未测；标准化账本、收益写入、Government未来头衔均不在本模块范围。

## A0006：区域族与完成通知候选

[接入调查](../../Reports/Technical/Specialization_District_Completion_Adapter.md)确认官方/HD Gameplay的OnDistrictConstructed与CityBuilt先例。完成事件的类型索引需转换为Type，不可当实例ID；候选对象需独立核对IsComplete及owner/city/位置。HD的IsDistrictComplete还排除pillaged，不作为首次完成历史判断器。

离线DistrictFamily从Districts/DistrictReplaces构建可验证替代链；已知范围外为NON_V01、未知/坏图为UNKNOWN。DistrictCompletionCandidate仅产出候选，不承诺完整有序批次，不接永久事实写入。Property单表新副本写回可作为待测方向，但实际持久化/单位消费原子性、城市UID和事件重放时序仍未解决；未来先部署只读新事件探针，B010不重发。

## A0007：B011运行只读完成事件探针

CompletionProbe.lua仅订阅GameEvents.CityBuilt、GameEvents.OnDistrictConstructed、Events.DistrictAddedToMap与LoadScreenClose。仅记录测试文明；自动捕获后存ExposedMembers.SPC_P0.CompletionProbe，不写存档Property。每玩家最多64条，计数/序列与load阶段独立，丢弃旧条目明示。加载创建新记录集，不回填历史；完成通知与加入事件分别计数，绝不认作正式专业事实。

OnDistrictConstructed第二参数按类型解析，再CityManager.GetDistrictAt读取实例并核对owner/type/所属城市/IsComplete；异常和缺失值显式显示。DistrictAddedToMap只用前六个字段，不猜progress参数位置。Family沿当局DistrictReplaces有界遍历，仅诊断。原离线状态模块未注册进游戏，两个按钮只读缓存且支持两条/页，无RequestPlayerOperation、剪贴板或可见UI初始化依赖。

[本地结果](../../Status/Validation/Results/Specialization_B011_Local_Result.md)与[用户两案](../../Status/Validation/Cases/B011_Completion_Events.md)明确范围。本批成功也不证明真实CityBuilt建城、修复/征服时序、永久UID或正式状态写入通过；B010仍延后。

## A0008：B011实机事件顺序与加载边界

[用户结果](../../Status/Validation/Results/Specialization_B011_User_Result.md)记录本次新城学院放置、完成和保存重载的实机观察。放置只有Added/NOT_COMPLETE，完成产生一次Constructed/COMPLETE_OBSERVED；本次重载只有加载期Added，不重放CityBuilt/Constructed。PASS限本次路径，不能泛化到自然跨回合生产、修复、征服或全部替代区域。A0007交付时未覆盖的真实建城，本次用户额外操作已提供有限场景证据。

建城时实测顺序为市中心Constructed → CityBuilt → 市中心Added。后续正式适配先排除NON_V01，不能让市中心抢占PROG的专业首次完成资格；不能假定CityBuilt先于任何区域通知。初始化与写入需幂等且不可覆盖已提交事实。加载期Added即使IsComplete=true也不得生成首次完成事实，已有区域的遍历顺序不代表历史完成顺序。当前仍只读，尚未实现永久UID/专业Property写入，OPEN-04保持原状态。

本轮校验发现当前Spec/ChangeLog已登记ACCEPTED D0002（Future Military II/III），且磁盘hash与ChangeLog一致；本轮未编辑Design。D0001同步hash对应[冻结原文](../../Design/Revisions/Specialization_Design_Spec_D0001.md)。本次仅登记同步差距，不对D0002进行技术可行性背书或扩大v0.1实现范围。

## A0009：D0002同步与离线写入计划

D0002差异只影响Future Military与版本记录，当前v0.1规则不变；MIL-001/002/005–008、OPEN-10的适配见[差异同步](../../Reports/Technical/Specialization_D0002_Architecture_Sync.md)。正常XP modifier与独立Insight保持不同结算路径；实际晋升、训练来源、战斗时采样和去重所需接口留待未来研究，不标可行性通过，不复制数值规则或启用军事机制。A0008末尾的待同步为当时记录，现由本节与header取代。

[写入准备](../../Reports/Technical/Specialization_City_Fact_Write_Plan.md)新增MOCK_ONLY CityFactWritePlan，计划生成与提交分离；重复FOUNDATION只恢复已有有效记录，不清空投资；加载期不生成完成写入，RESTORE不补缺失历史。完整有序批次、持久身份仍是调用前提，原生事件不能自封为权威批次。计划的版本比较只在fixture提交器验证；真实SetProperty写入、读回确认和跨对象失败恢复未实现。运行保持B011，无新Property或正式收益。

## A0010：身份账本和故障恢复实验

[身份存储研究](../../Reports/Technical/Specialization_City_Identity_Storage.md)核对HD Game/City表Property先例，新增MOCK_ONLY CityIdentityRegistry：分配序列和身份records组成单一envelope；复制后写、写前核对、单实例防重入、写后读回，setter报错仍不盲重试。相同已验证对象返回原编号，坏账本不重置；UNKNOWN禁止用于正式机制。

外部instanceProof和空账本首次创建资格仍是fixture前提，没有找到可直接替代它们的永久城市API。编号在存档分支内作用，不作跨存档ID。当前无Game/City Property adapter，单值原子性与持久性仅模拟假设；专业事实尚未纳入envelope，不能宣称解决跨Property事务。下一步独立DEV表存储探针先验证序列化，不用合成ID绑定真实城市，不决定OPEN-04，不新增正式收益。

## A0011：B012独立DEV表存储探针

StorageProbe仅由Gameplay处理STORAGE_READ/WRITE窄命令，测试文明门控，无需选城；Game Property键按玩家隔离，固定合成表不关联真实城市。空值才写一次，完整相同不写，读失败/不一致不覆盖；setter抛错仍读回判断，不自动重试。UI通过既有token ACK显示，不读写Property。加载不自动创建数据；因此重载后先Read可以检测丢失，不能由自动补写掩盖。

本轮只验证单值表往返，尚非身份分配/专业事务实现；不提供原子保存、多人或崩溃恢复保证。详见[B012本地结果](../../Status/Validation/Results/Specialization_B012_Local_Result.md)及[两案](../../Status/Validation/Cases/B012_Table_Storage.md)。运行B012/modinfo19，UUID不变，B010延后。

## A0012：B012表存储实机证据

[用户结果](../../Status/Validation/Results/Specialization_B012_User_Result.md)证实本次合成Game Property表的写后完整比较、重复操作不写及保存重载后只读恢复。该结构的字符串键、嵌套数值与布尔值在实测环境保持；不能外推任意结构/大小、多人同步、崩溃原子性或真实城市代际。后续可使用此证据继续身份/事实持久化准备，仍需独立解决instanceProof、初始账本资格及OPEN-04，不把DEV-1/2绑定到真实城市。

## A0013：城市双侧绑定恢复准备

[恢复方案](../../Reports/Technical/Specialization_City_Binding_Recovery.md)将总账预留、城市token与确认分开，缺一侧UNKNOWN不自动补写；双侧匹配才计划确认。新增MOCK_ONLY恢复判定及测试，不把ComponentID/owner/cityID/坐标当永久UID。运行仍B012，无新Property；真实代际与跨Property恢复仍需后续探针。

## A0014：B013 DEV新城绑定探针

BindingProbe运行记录仅服务于DEV验证，不是正式UID或专业事实。加载后CityBuilt核对当前城市，预留Game账本→城市token→确认Game账本；旧城不补写，部分失败拒绝自动修复。加载审计与BINDING_READ均只读Property，不依赖UI初始化事实。最多32座DEV新城，总账/城市分别计尝试次数，重载清零。

缺总账时扫描现有城token仅防可见残留；不证明所有痕迹丢失时仍能识别旧账本，亦未确认征服/毁城/引用复用全部语义。原有OPEN-04及正式身份前提保留。详见[B013本地结果](../../Status/Validation/Results/Specialization_B013_Local_Result.md)；运行B013/modinfo20，等待两案，不接专业或收益。

## A0015：B013正常新城与重载证据

[用户五图](../../Status/Validation/Results/Specialization_B013_User_Result.md)确认被测旧城不补写、新城Game账本/City token一致，正常保存重载后同token/CONFIRMED保持且写入0/0。可继续研究与完成事实关联，但不将DEV token自动提升为正式UID，不扩大到征服/毁城/首都初建/全部生命周期或崩溃原子性。下一步先限定正常新城与已明确的PROG规则，OPEN-04仍保留。

## A0016：B014绑定城市的完成观察持久化

新增CompletionRecordProbe将live OnDistrictConstructed经对象/完成/替代族/有效绑定核对后保存City DEV观察表，加载与Added不生成，已有有效观察不覆盖；BindingProbe只读Resolve验证双侧token。FIRST_OBSERVED_COMPLETION明确不代表历史首个完成，不构成正式专业或完整有序批次。OPEN-04、首次初始化仍保留；详见[B014本地结果](../../Status/Validation/Results/Specialization_B014_Local_Result.md)。运行B014/modinfo21，等待用户两案，无正式收益。

## A0017：B014完成观察与重载证据

[三图结果](../../Status/Validation/Results/Specialization_B014_User_Result.md)显示同一绑定城市学院未完成无记录、完成写一次、重载记录不变且本次加载写0。该证据支持DEV观察持久化正常路径，不证明历史首个专业区域或有序完整事件批次。完成手段未说明，不泛化自然跨回合生产。正式初始化仍需可靠新城资格与完整历史边界，OPEN-04保留；不自动将DEV记录升级为正式事实。运行B014/modinfo21未变，无新增功能。

## A0018：正式初始化历史资格审计

[历史完整性报告](../../Reports/Technical/Specialization_Completion_History_Boundary.md)以实际B014代码的合成反例确认：同一观察表可以对应不同历史，绑定成功/重载成功均不构成完整历史。正式层须单独保存新城资格及错误缺口，不能迁移DEV记录或由现有区域猜测。OPEN-04同时完成顺序需用户选择；报告提出按有效通知先后锁定的候选，但未采用、未改Spec。没有新运行包或新实机测试。

## A0019：D0004顺序规则与统一记录准备

[本轮报告](../../Reports/Technical/Specialization_D0004_Completion_Journal.md)完成D0003/4差异映射。CityCompletionJournal离线统一新城资格、历史缺口、顺序游标与事实；单个有效通知即可计划锁定，无需等待整回合或未知并列批次结束。旧DEV不迁移，真实写入器、持续历史证明与故障停止尚未接入。前面A0018等段落的顺序待决已由PROG-005取代，冻结报告保持原样。四组本地通过，无新实机批次。

## A0020：D0005三项适配

[同步及七组本地结果](../../Reports/Technical/Specialization_D0005_Architecture_Sync.md)：工业逐recipient max/union/max、首都仅source自接入、带同城凭据的永久事实转移。征服继承、首都自接入、工业多源不再设计待决；上方旧版段落属于阶段历史。真实新城提交器需将owner转移与整体记录一致性纳入，不能按旧owner不匹配直接抹除事实。运行包未变，无新增实机测试。

## A0021：B015实际DEV城市记录提交

[本地结果](../../Status/Validation/Results/Specialization_B015_Local_Result.md)：BindingProbe新建成功直接回调，玩家区域集合扫描确认空专业新城，独立City表保存候选事实，后续通知不覆盖；错误停止与可保存GAP，加载仅审计。旧城/旧DEV不迁移，身份冲突保留原表。不是正式UID/征服转移或完整历史的全生命周期证明；若GAP写入也失败，不能保证重载后检测。运行B015/modinfo22，七组本地通过，等待最小三案。

## A0022：B015正常路径实机证据

[三图结果](../../Status/Validation/Results/Specialization_B015_User_Result.md)确认本次新城自动初始记录、学院候选写入及重载保留，写入1→2→0。此证据支持现有存档新增城市的正常DEV路径，不推广到全生命周期、错误恢复、正式UID或收益。旧城/重复操作没有独立图像结果，本轮不补测。当前D0006的PROG与D0005相同，整体技术映射仍待审；未改运行包。

## A0023：D0007整体同步（含D0006）

[同步报告](../../Reports/Technical/Specialization_D0007_Architecture_Sync.md)覆盖ELIG-001至006、COMPAT-001、ID/PROG/OPEN变更以及MIL-003/008至013。正式核心转为显式参与资格，非Human-only或测试载体专属；未启用者的已有成果仅休眠保存。当前运行及离线模型仍有固定测试门控和旧兼容状态，列为待适配，不改已有测试证据。文档同步不是部署；本轮无Source/Tests改动或新实机批次。旧版段落中的资格/训练/旧档未决措辞由当前正文和本节覆盖。

## A0024：离线参与资格与休眠分离

[资格模型报告](../../Reports/Technical/Specialization_D0007_Eligibility_Model.md)记录独立PlayerEligibility输入、enabled调度、永久事实恢复/转移与当前能力门控。State、Journal和WritePlan已先判断资格；disabled/unknown不建立新事实或形成投资计划，Derive提前返回且不读总督。取得无成果城新增独立离线入口，不由空Property推断历史。五组本地通过，运行未变。

真实carrier、同城识别、取得历史资格、现有Modifier撤销、Network全入口筛选尚未接入；旧身份/绑定实验仍需适配。不能把模拟active=0当成已经撤销游戏收益。A0023报告中的State固定门控/旧档状态差距已在本轮模型范围修正，其余差距保持；旧报告作为当时调查记录保留。

## A0025：真实资格载体的只读候选

[源码调查与候选](../../Reports/Technical/Specialization_Eligibility_Carrier_Research.md)确认HD Gameplay使用PlayerConfigurations + GameInfo.CivilizationTraits，当前测试Trait可作显式绑定配置。候选接受Trait参数，不依赖文明/领袖硬编码或Human，不直接调用含_CAPTURED语义的HD helper。数据库中断/未就绪返回UNKNOWN；候选尚未注册运行，不能作为已验证游戏资格。

CityConquered在原版及HD Gameplay有先例，但只作新旧owner重核信号，不足以证明永久同城或覆盖所有取得方式。初始化、建城、取得、删除的处理边界详见报告；真实征服转移与效果撤销仍未实现。

## A0026：B016只读资格诊断

EligibilityProbe在Gameplay启动后与LoadScreenClose各读取一次显式Trait绑定，分别保留INITIALIZE/LOAD_CLOSE结果。UI Read eligibility仅显示缓存，不触发采样，不要求选城；不替换IsTestPlayer或接入正式参与资格。结果ENABLED/DISABLED/UNKNOWN只作诊断，读取中断不采用旧成功值。Player roster仅做有界轻量配置查询，不深枚举未启用玩家城市；无周期扫描。

[本地检查](../../Status/Validation/Results/Specialization_B016_Local_Result.md)及[用户两案](../../Status/Validation/Cases/B016_Eligibility.md)。未知槽位和初始化未就绪保留原样，无自动过回合掩盖。读档恢复、实际上下文仍需用户结果；永久同城、转移、收益撤销未接入。

## A0027：B016用户证据边界

[两图结果](../../Status/Validation/Results/Specialization_B016_User_Result.md)确认本次玩家0在INITIALIZE及LOAD_CLOSE均ENABLED/EXPLICIT_TRAIT_BINDING；两次汇总1/55/8一致。支持本局配置查询与按两案回报的后台重载重建，不等于全部槽位、AI玩法、动态资格、正式运行门控或征服成果验证。未知8应继续拒绝启用；原因需后续日志/配置只读核对，不能默认空槽位。运行代码未变。

## A0028：未知槽位诊断补充

本地日志未发现B016逐槽位原因，暂不归因为空槽位。B017仅新增UI缓存明细按钮，实际采样不变；[本地结果](../../Status/Validation/Results/Specialization_B017_Local_Result.md)。不能把完整roster遍历等同所有资格已知，UNKNOWN禁止运行且不删除永久成果。等待单案补充后再决定正式名单读取与资格入口实现，不先把未知当未启用。

## A0029：B017原因明确、槽位身份待核对

[用户明细](../../Status/Validation/Results/Specialization_B017_User_Result.md)确认54–61均CIV_NOT_READY。该assert表示文明类型不是非空字符串，不表示NO_TRAIT_BINDING，也不证明是活跃AI或预留槽位。正式入口继续区分资格UNKNOWN与明确DISABLED；下一步只读检查有效玩家名单/槽位定义，不能用清零诊断数字为目的自动禁用。未改变运行代码。

## A0030：当前名单与资格分离候选

[本轮研究](../../Reports/Technical/Specialization_Current_Player_Roster.md)确认原版/HD Gameplay的GetAliveIDs先例。CurrentPlayerRoster本地候选将当前成员关系与资格分开，名单外NOT_CURRENT不等于DISABLED或没有永久历史；名单内未知不授予许可。全刷新失败不用旧授权结果，高编号不硬排除。正式名单就绪/失效/实际返回尚未接入。

54–61仍只有CIV_NOT_READY用户证据，没有可靠源码固定身份定义；不把它们当空槽。运行包未改，无新实机批次，可继续独立准备资格生命周期而不等待编号命名。

## A0031：运行许可的离线生命周期

[入口模型](../../Reports/Technical/Specialization_Eligibility_Lifecycle.md)将名单/资格结果转换为实例内、代次绑定的许可；刷新开始先撤销旧许可，读取失败不保留旧授权，失效/内层更新后旧刷新不能提交。许可按玩家核对，重建实例拒绝旧对象。无永久事实读写，无实际收益撤销，正式提交边界仍需重新检查并接真实事件。

## A0032：B018组合Gameplay诊断

[本地结果](../../Status/Validation/Results/Specialization_B018_Local_Result.md)记录CurrentPlayerRoster/载体/许可的私有诊断封装。新GetAliveIDs真实接口在初始化观察、LoadScreenClose重建，UI只显示自动结果；54–61仅展示成员关系。内部自检撤销/重取诊断对象，非真实玩家资格变更或收益撤销。没有正式授权API、Property写入或周期结算。等待[B018两案](../../Status/Validation/Cases/B018_Runtime_Eligibility.md)，不扩大原B016/B017证据。

## A0033：B018实际名单/诊断证据

[两图结果](../../Status/Validation/Results/Specialization_B018_User_Result.md)显示本局GetAliveIDs为0–14/62–63，获准0、未知无；54–61均名单外。当前名单与全槽位资格查询差异得到实机支持，无需给54–61硬编码身份。支持限定正常加载/重载的诊断组合，不证明实际资格变更事件及时撤销或正式收益安全。下一步准备限定城市处理入口的门控接入及事件/提交边界，不新增本批功能。

## A0034：城市处理入口离线复核

[本轮接口](../../Reports/Technical/Specialization_City_Operation_Gate.md)组合许可、城市身份解析和现有事实规划。资格先于城市读；计划后提交前重新核对许可、owner/代际和完整原事实，句柄只允许一次复核尝试。返回CHECKED_PLAN_ONLY，无setter、无生产授权。实际写入/读回与错误恢复必须紧邻复核接入，B018诊断许可仍未用于运行CityJournalProbe。

## A0035：MOCK提交/读回与停止

[本轮结果](../../Reports/Technical/Specialization_City_Commit_Readback.md)记录CityOperationGate.CommitMock及11种场景。计划复核后只调用一次mock writer，按同城读回区分目标存在、旧值、冲突、未知；写后抛错但目标匹配不盲目重写。不确定/重入/失效停实例，不回滚或自动恢复。未确认状态尚无持久恢复协议，新实例不保证继续停；真实setter、原子性、永久UID与跨存档恢复仍未实现。

## A0036：未确认提交的记录/只读恢复

[恢复记录模型](../../Reports/Technical/Specialization_Pending_City_Recovery.md)保存PENDING、操作/城市身份和原/目标事实，JSON新VM检查通过。所有恢复结果保持暂停，不自动写入、清记录或激活。尚未接CommitMock或游戏Property；后续须保证先保存确认记录再写城市事实，且启动先查记录再开放提交。跨Property原子持久化未被证明。

## A0037：PENDING先行与启动拦截集成

[本地集成](../../Reports/Technical/Specialization_Recorded_City_Commit.md)将恢复存储接到Gate：明确无记录才能准备；提交先保存/确认PENDING，重核城市/许可后才一次mock写。已有记录或读取失败先停，JSON新VM保持拦截。成功仍TARGET_OBSERVED_PENDING，无终态/连续提交。真实存储原子性、最终事件边界与完成/恢复协议仍待实现。

## A0038：DONE终态与显式重新开放

[本轮模型](../../Reports/Technical/Specialization_City_Terminal_Record.md)仅在同城目标和DONE均确认、资格仍有效、无重入时开放下一笔；新实例先暂停再显式对账。DONE保留最近凭据，不删除PENDING掩盖结果。单城市顺序通道连续两笔本地通过，非全历史操作账本或引擎原子性证明。PENDING原值/冲突仍暂停，不自动ABORT。

## A0039：成果与恢复记录统一存储

[统一适配](../../Reports/Technical/Specialization_Unified_City_Envelope.md)将既有Gate与恢复模型接到同一整表，保存阶段为原值/PENDING→目标/PENDING→目标/DONE。六个截点新VM恢复及故障模拟通过；不再依赖两份Property配对，但不声称引擎原子性或锁。运行仍B018；下一项限定合成DEV分阶段保存/恢复，不接正式城市收益，不迁移旧DEV记录。上节“统一存储待审查”已由本节离线结果取代，真实存储适配仍待完成。

## A0040：B019有限合成存储探针

[实际接入与边界](../../Reports/Technical/Specialization_B019_Envelope_Probe.md)：专用Game Property六阶段，自动加载只读，显式Next推进并防旧请求重复写。七组本地检查通过，两案等待用户；不部署正式Gate/城市UID或收益，不把合成BEFORE后推进当正式事务重试政策。此前“DEV未部署”由本项替代，正式引擎适配仍待完成。

## A0041：B019正常重载实机证据

[四图判读](../../Status/Validation/Results/Specialization_B019_User_Result.md)支持固定合成表在计划/目标中间阶段保存重载保持且加载写入0，连续完成到6后不再写。本结果取代B019两案待测，不扩大为真实城市Gate、跨owner身份或崩溃原子性通过。下一步准备限定新城存储衔接，正式收益未接入。

## A0042：City Property连接本地组合

[连接层与源码边界](../../Reports/Technical/Specialization_City_Property_Bridge.md)将API形状的城市对象接到既有Gate/统一表；两城、完成/重复、重载和身份/资格中途变化通过本地检查。BOUND_MATCH不证明完整新城历史，B013单回调不能覆盖B015，DONE不证明漏通知不存在。下一项准备有序事件分发及历史证据入口，正式部署仍待完成；运行B019不变。

## A0043：有序事件流本地组合

[事件流结果](../../Reports/Technical/Specialization_City_Event_Flow.md)将legacy→结果/历史检查→CityPropertyBridge提交按序组合；完成通知按交付先后锁专业，处理异常/重入暂停后续提交。八组本地通过，未挂接实际回调。无法发现未交付事件；实例暂停不替代持久GAP，跨加载旧通道不自动采纳DONE作为完整历史。运行B019保持，正式历史连续性仍待适配。

## A0044：实际新城回调接口本地验证

[挂接验证](../../Reports/Technical/Specialization_Native_Fresh_Hook.md)捕获旧回调并核对本次FOUNDATION_SAVED和写计数，不从旧TRACKING表推断新建。AfterLegacy入口避免旧处理重复执行；实际B013/B015在mock环境与存储模型组合通过。未部署，完成通知与跨加载历史凭据仍待接，B019保持。

## A0045：B020限定DEV集成

[部署与边界](../../Reports/Technical/Specialization_B020_City_Flow.md)：旧回调后核对新城，真实完成事件与B015first逐项对照，独立City表三阶段保存。只处理本次加载新城，重载已有表只读；不是正式MOCK Gate部署或跨加载历史解决。八组本地通过，用户两案待测，运行B020/27，无正式收益。

## A0046：B020同回合Cheat路径实机证据

[四图复验](../../Status/Validation/Results/Specialization_B020_User_Result.md)确认放置不锁定，Cheat同回合完成后写入6/RESEARCH1，正常重载保持并只读写0。此路径支持旧/新回调顺序与真实City表集成，不证明自然生产、全部事件顺序或跨加载续写。B020待测已由本结果取代，正式历史恢复边界保留。

同步提示：本轮发现Design已接受D0008（Future设计登记），尚未完成架构差异审阅。Design Spec Synced Through仍为D0007；不声称已同步D0008，不影响本批B020证据登记，不暂停或扩大v0.1开发。

## A0047：D0008同步与恢复边界

[D0008同步](../../Reports/Technical/Specialization_D0008_Architecture_Sync.md)完成，取代上节待审阅提示。Future方向/暂定参数分别保留，v0.1不扩展。[丢写反例](../../Reports/Technical/Specialization_Load_History_Ambiguity.md)证明既有DONE/TRACKING不足以恢复未专业化城的历史完整性；当前自动恢复写入缺少可靠证据，保留B020只读，不影响用户已通过范围。

## A0048：按用户测试优先级恢复正常读档路径

[B021实现](../../Reports/Technical/Specialization_B021_Normal_Load_Resume.md)在既有身份、DONE、B015一致、无已知错误和可见冲突的条件下恢复内存active，不写永久记录；普通未专业化城可继续完成。该支持范围依用户明确的Cheat测试优先级，不代表已解决A0047全丢写反例。必要停止保护保留，运行B021/28，下一项真实Lv1收益。

## A0049：B021正常恢复实机证据

[三图复验](../../Status/Validation/Results/Specialization_B021_User_Result.md)确认正常读档恢复为RESUMED_NORMAL，未完成学院保持NONE/0且写0；随后完成为RESEARCH/1、revision6、写3；再读档保持并写0。取代本批待测，不扩大为自然跨回合生产或全部丢写历史恢复。正式收益仍未接入，下一项实际Lv1收益。

## A0050：Research Lv1原生载体实验

[B022实现与边界](../../Reports/Technical/Specialization_B022_Research_Lv1_Yields.md)使用内部Campus建筑的Building_CitizenYieldChanges直接承载RES-001，显式开关用于测量，不采用城市补贴替代。B021有效记录门控、重复不创建、正常重载保留与失效清理已本地验证；通用资格与自动启用仍未部署。运行B022/29首次包含可显式开启的实际专家收益，取代上文“完全没有收益”的当前描述；三案等待用户，其他专业/高级收益未启用。

## A0051：B022原生Research专家收益实机证据

[三图与用户人工回报](../../Status/Validation/Results/Specialization_B022_User_Result.md)确认原生专家提示显示2科技/3生产力/3食物，正常重载面板ON、1专家、修改0。开关/零专家对照依用户人工通过回报登记，未冒充截图直接对照。取代B022待测；原生载体可继续作为常数型Lv1收益实现基础，自动应用与通用资格仍待接入。

## A0052：自动Lv1与网络下一阶段提案

[B023实现](../../Reports/Technical/Specialization_B023_Auto_Constant_Lv1.md)自动对账三类标准区域的原生专家收益，取消手动开关；现有DEV门控与标准类型为测试范围，正式通用资格/替代类型适配未完成。自动完成/重载本地通过，用户小批次待测。

[Network连接/分发方案](../../Reports/Proposals/Specialization_Network_Connection_Distribution_Plan.md)复核Gameplay全集仍BLOCKED，建议用户批准无收益后台UI桥接候选实验；这是放宽既有来源约束的DESIGN_DECISION_REQUIRED，并未部署或改Accepted Spec。纯Gameplay继续需新证据，显式连接槽位仅最后玩法替代，不接受即不实现。

## A0053：B024自动扫描修复

B023实机三城expected正确但carrier缺失，自动应用未通过。[修复](../../Reports/Technical/Specialization_B024_Auto_Scan_Fix.md)隔离每玩家扫描异常，完成事件直接处理本城，并显示扫描诊断；本地反例复现与修复通过，实机仍待复验，不改Design或网络来源约束。

## A0054：B024自动收益实机通过

[两图与人工结果](../../Status/Validation/Results/Specialization_B024_User_Result.md)支持旧城恢复、新城区域完成自动应用；一级建筑/多个专家收益及后建第二专业区域不改专业按用户明确回报通过。缺少第三张图不伪造截图证据。B023失败保留，B024待复验由本结果取代；实际旧故障根因仍不由本次PASS倒推。下一重点Network候选，通用资格/替代区域范围不扩大。

## A0055：后台来源已获用户明确认可

[来源澄清](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md)取消此前“桥接方向待决定”，不是改变NET玩法。历史章节的纯Gameplay限制与待批准描述已被本节取代；实现下一步为后台批次交接和网络重建，无新运行部署或实机PASS。

## A0056：B025后台商路与诊断网络接入

[实现](../../Reports/Technical/Specialization_B025_Background_Network.md)新增明确UI来源的完整标量批次传递，Gameplay核对后替换，收到包自动派生Lv1连接/接收；不依赖打开窗口，不发收益。当前仅测试玩家/有效DEV Lv1与128条上限，正式ACTIVE、全参与者与完整来源账本仍待接。两个本地测试通过，三案待实机，不改纯Gameplay旧模块标签冒充兼容。

## A0057：B026 Gameplay计数接口纠正

[B025失败与B026修正](../../Reports/Technical/Specialization_B026_Trade_Count_Fix.md)：Gameplay使用CountOutgoingRoutes，UI保留GetNumOutgoingRoutes。请求接收证据不等于网络派生通过。新mock区分两种上下文，首都→目的城为下一最小复验，网络规则不变。

## A0058：B026用户证据边界与报告语义

[B026八图](../../Status/Validation/Results/Specialization_B026_User_Result.md)验证有限DEV Lv1连接/分发/正常重载，不更改NET规则或运行实现。connected列当前中心可分发的直接来源；selectedReceives列本城recipient资格；N是全国去重recipient数。科研首都→商业中心同时可构成科研接入与分发，不能按路线只允许一个角色。商业中心source=NONE是输出源筛选标签，不是无专业。后续显示应分离专业身份/来源/接收名单以降低误读；撤销与高级等级仍未由本批证明。

## A0059：D0009正式sync（尚未部署适配）

[同步报告](../../Reports/Technical/Specialization_D0009_Architecture_Sync.md)定义direct接收资格合并、Convergence来源与basis边界。此前A0058/B026解释仅在D0008下有效；不作为当前设计判据。Design hash已静态核对，不新增本地模拟或游戏PASS。

## A0060：B027限定运行适配

[实现与调查](../../Reports/Technical/Specialization_B027_Direct_Reception.md)：先合并中心direct recipient，再合并distribution，保持非递归。旧离线NetworkState仍待统一，当前新测试直接加载运行模块。HD CityYield账本提供来源记账先例，不等于准确纯本地产出接口；不选择替代basis。两组本地通过，D0009游戏结果待用户回报。

## A0061：B027证据及汇聚条件备选

[B027两图](../../Status/Validation/Results/Specialization_B027_User_Result.md)已确认新接收判据。用户条件允许总产出basis，见[研究与授权范围](../../Reports/Technical/Specialization_CommerceIV_Basis_And_Cycles.md)。纯LOCAL与TOTAL候选接口分离；source必须R/C/I、target为Commerce IV，不能把接收网络当来源或把工业输出改成城市总yield。先读后写不保证跨轮无反馈；原生倍率/应用精度/第三方反馈未证明。离线计划通过，不注册收益，未修改Accepted Spec或运行包。

## A0062：来源总产出只读探针

[B028](../../Reports/Technical/Specialization_B028_Source_Yield_Probe.md)只读选中城市S/C/P，按项失败显式UNKNOWN，不覆盖accepted local basis、不升ACTIVE、不发Convergence。两组本地通过，实际Getter需用户确认。高级专业Lv2–4正式玩法仍未集成，已有Lv1实际收益与只读网络诊断分别保留。

## A0063：B028用户证据

[B028两图](../../Status/Validation/Results/Specialization_B028_User_Result.md)确认科研城GetYield读取S/C/P和同回合变更刷新，文化UI截断精度差符合预期；不证明精确local basis或Convergence实际发放/倍率/防反馈。运行B028/35未变，下一步继续承载研究，不启用高级专业能力。

## A0064：固定收益承载实验

[B029](../../Reports/Technical/Specialization_B029_Yield_Carrier.md)通过独立plot属性门控固定city yield效果，STEP不累加，OFF撤销。只在显式测试操作时启用，不接Commerce IV或高级资格。六固定定义与0.5 Amount用于测试精度而非选择业务量化。原生倍率、精确增量和district反馈仍待验证；基线内存、开关持久，测试结束必须OFF。

## A0065：B029实例初始化边界

[旧档失败证据](../../Status/Validation/Results/Specialization_B029_Old_Save_Failure.md)区分数据库定义、Trait挂载表、存档运行Modifier实例及实际yield四层。GameInfo存在不足以证明后两层。优先同代码新局+1对照；旧档未挂载只是待排除假说，不宣称已修复，不用可能重复的Attach作补丁。整数不生效时不能判小数能力。

## A0066：新局整数承载证据

[B029新局三图](../../Status/Validation/Results/Specialization_B029_New_Game_Result.md)：同代码新局整数+1与OFF三项恢复已通过Getter观察范围，支持旧档初始化差异假说但不证明精确挂载内部状态。不要用城市UI未刷新否认Getter变化，也不声明UI同步通过。半点、百分比倍率与district反馈另待验证；运行未改。

## A0076：固定city yield半点失败边界

[B029半点两图](../../Status/Validation/Results/Specialization_B029_Fractional_Result.md)显示配置1.5实际delta1，不能认为小数承载已通过。OFF可恢复，但Amount精度与HALF条件/实例需分辨；不泛化全部Effect不支持小数，也不据此选择业务取整规则。下一步研究精度或替代承载，当前不改变Design。

## A0076：B030精度与激活区分

[调查](../../Reports/Technical/Specialization_B030_Precision_Control.md)保留内部浮点、禁止静默取整。第二槽含整数部分用于诊断，不是玩法数值。每人口小数先例不等同固定城市小数支持；测试结果返回前不选fallback，不修复旧存档实例。

## A0076：B030第二槽激活与小数限制

[实机结果](../../Status/Validation/Results/Specialization_B030_User_Result.md)支持第二槽有效但1.5只贡献1。当前固定城市收益小数路径存在IMPLEMENTATION_LIMITATION，不等于全部Modifier不能处理小数；内部浮点计划不变，先调查可保留设计的承载路径。没有新设计决定或运行修改。

## A0076：网络报告与撤销边界

[实现报告](../../Reports/Technical/Specialization_B031_Network_Report_Withdrawal.md)区分来源数与去重接收城市数，明细不改变拓扑。读取数量不匹配拒绝旧显示；真正后台撤销仍需实机，不由本地通过升级。固定小数/Commerce IV暂列后续研究，Advanced Lv2–4没有新增收益。

## A0076：B031撤销证据与显示修复

目的端失效后中心直连保留、全国接收城市撤销已按两图通过，不能扩展到战争/自然到期/掠夺。空白按钮仅XML文字修复，无新网络算法；详见结果报告，避免将原生显示修复标为已通过。

## A0076：永久投资执行准备

见[执行层报告](../../Reports/Technical/Specialization_Settler_Investment_Executor.md)。通过旧规则reducer计算，不复制设计；INTENT不自动推导成功，已确认消耗只恢复提交。引擎身份和单位删除时序仍需接入验证，不能宣称完整原子性。当前存储0/1限制以及与B015一致性需先适配，不直接注入新的Potential属性。

## A0076：献祭先例与非侵入投资账本

HD奖励请求与删除请求分开，Specialization拟采用单Gameplay请求并关闭通用UI自动删除。满血/移动力等HD专属限制不移植。投资账本仅保存凭据/阶段和一致性anchor，基础专业记录不改；有效Potential/ACTIVE由统一入口推导，消费者尚未接入。详见专项报告，无新实机结论。

## A0076：EffectiveFacts原生读取接入

统一Potential计算、已完成凭据与pending区分，总督未知不伪造ACTIVE；Lv1继续不要求总督。网络仅身份/拓扑接入高Potential，不称为强度结算。新模块无写入，原生writer/消费executor仍待注册。详见B032报告。

## A0076：B033移民投资入口

首版市中心+标准移民+测试文明范围，Prepare只读，Confirm复验并消耗；这是支持范围而非永久Design新增条件。原始城市记录不改，已确认消耗才提交；未知结果停止、不自动重扣。无跨单位/Property原子性保证。详见报告和唯一三步测试。

## A0076：B033正常路径实机证据

[结果报告](../../Status/Validation/Results/Specialization_B033_User_Result.md)区分三图与人工观察；第三图ACTIVE2、Potential2正确。旧路线连续性、3/4级投资及异常恢复不扩大PASS。下一项共同Lv2收益，当前未部署。

## A0077：B034共同Lv2住房

有效事实只读→对应专业完整区域及实际建筑层集合→可撤销原生Housing载体。后备回合核对不冒充即时事件通过；面板只读，错误或未知事实不保留高级住房。此轮启用住房部分，不扩大为SHARED-002/GPP或Lv3/4完整实现。见B034报告的映射范围、验证证据及用户三步测试。

## A0078：D0010征服初始化适配

PROG-006至010已同步；当前旧schema1 AcquireUnassigned拒绝调用，避免未部署模式分流时继续生成普通完成记录。新增离线模式契约独立于运行，模式/冻结候选是持久初始化事实，Claims与网络/ACTIVE是由有效状态生成的可撤销结果。Identity origin/区域锚点、同城转移及snapshot时点是正式接入前置；已有Identity永不进入Claim。详见D0010报告，实机批次尚未派发。

## A0079：B034实机结果与刷新边界

[结果](../../Status/Validation/Results/Specialization_B034_User_Result.md)区分HasBuilding载体读数、右下角UI与用户附加操作。原版CityPanel生产事件刷新/HD基础刷新调用为静态先例；不能由carrier=0宣称同回合原生住房Getter已归零。用户接受显示延迟，本轮不修改运行或强制触发生产人口事件；保存重载未回报。下一步共同Lv2基础GPP。

## A0097：B035原生基础GPP

按工作人数编码内部建筑，原生点数绑定相应区域；核验数据库防止HD全局翻倍误作用。零人/ACTIVE低于2/事实失效时撤销，重复刷新不积累。独立后台dirty信号不携带收益事实，诊断读取不触发应用；CityGPPProbe只作源码参考，不修改或依赖它。实机倍率/事件时序尚未通过，详见报告。
