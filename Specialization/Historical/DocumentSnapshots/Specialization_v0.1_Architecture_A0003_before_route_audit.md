# Specialization v0.1 Architecture — A0003

Document Owner: Codex
Architecture Revision: A0003
Design Spec Synced Through: D0001
Design Spec SHA256: 10323a0350ff5b97be179b25c1c315b42aa7c6a41cb4cf6d55b9c7a34aee2ae6
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-010 / modinfo17

## CURRENT AUTHORITATIVE STATE

游戏设计意图只以[Accepted Design Spec](../Design/Specialization_v0.1_Design_Spec.md)为权威。本文负责实现方法、接口契约和技术限制，不再维护第二份数值表。SYNCED_WITH_LIMITATIONS表示已完成规则映射并记录限制，不表示实现完成、技术限制已解除或游戏验证通过。

完整Rule ID覆盖、同步检查与遗留差异见[同步报告](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)。唯一验证矩阵和待办见[Status](../Status/Specialization_P0_Status.md)。当前已恢复离线多源强度实现/模拟；运行代码和Mod UUID未改，B010仍未测；不启动游戏。

## 身份、存储与能力门控

适配SCOPE、ID、TERMS、PROG。运行身份为CIVILIZATION_SPC_TEST、LEADER_SPC_TEST、TRAIT_CIVILIZATION_SPC_TEST；数据库/展示资产继续由现有modinfo加载。机制按玩家文明身份门控，不用本地UI玩家作为全国结算条件。区域族需数据库审计；不能仅靠RequiresPopulation判断。

永久保存专业、Potential、首次完成事实、标准化模板及不可重复动作凭据；专业写入必须由完成事件确认，不能从已放置区域猜测。商路、总督条件、网络来源/接收/强度均为可重建派生状态。城市UID映射层尚未实现，owner/cityID仅为当前引用，中心plot不是永久UID。跨征服继承、旧档初始化、同时完成顺序依Spec OPEN-04，不自行补规则。

总督使用原生Requirement→城市Property门控：1为激活，nil/0不激活，不能用Lua truthiness误判0；不重试已失败的GetAssignedGovernor。门槛数值和ACTIVE计算只引用PROG-003。原生条件不能反推出全部Mod免费晋升历史。当前CityRoleFacts只读诊断，不是专业/潜力写入层；多人确定性未验证。

### Trade Route State：强制契约

流程：`Gameplay authoritative full source → normalize → deduplicate → atomic replace → source connections → distribution recipients → per-network recipient sets`。

当前 **没有已确认的 Gameplay 全集 provider**。B004 单位 operation 探针只是候选诊断，不连接正式状态层。UI city:GetTrade():GetOutgoingRoutes() 虽已实测通过，也不能满足本轮 Gameplay 权威源要求。HD Temp_Interface 实际注册为 AddUserInterfaces，文件夹名不代表执行上下文。

离线 `DevelopmentTests/TradeRouteState.lua` 接受明确 COMPLETE/GAMEPLAY/GAMEPLAY_CURRENT 契约，只允许未来经过审计的 adapter 提供该契约；测试中 MOCK 是唯一来源。接口返回失败、部分列表、Unknown、UI snapshot、历史事件或 operation candidate 时，Read 返回 UNKNOWN，不返回假空集合或旧有效路线。lastGood 仅供诊断，不能结算。

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
| NET、NET-RC、COM-003/004 | 保留source/center/recipient资格，接收城市按UID去重；离线强度计算层已适配NET-RC-001至004，保留005精度边界。max选择只对有效ACTIVE源执行，空集显式归零；独立k参数不与路线数耦合。不把max套给Industry或Future来源结算。NetworkState保留来源；NetworkStrength.FromState执行聚合。 |
| NET-RC-005 | Lua先算未取整浮点，独立BoostAdapter负责引擎应用。数据库TEXT只证明能存，不证明Modifier支持动态表达式/小数。精度与量化按OPEN-06待决；先调查引擎，不能静默整数化或退回线性模型。 |
| IND-NET | 模板按完成事实记账，使用当前有效来源资格匹配区域/tier；未识别建筑不能扩成整区折扣。Gold-only作用域须独立验证，若只能同时影响Faith，报告IMPLEMENTATION_LIMITATION并交用户决定。多源合并仍见OPEN-07。 |
| CREW | 固定Project→单位规格数据只引用CREW。生产注入先核对合法当前目标/剩余量，按min应用，拒绝非法目标且不消耗；队列切换、重入和消耗凭据需防重放。AddProgress/原生生产Modifier/HD先例仍需实测比较，不能假定无溢出。 |
| GW | 隔离GreatWorkSubsidy适配，优先城市基础补贴；不要求直接改对象。类型/时代曲线依OPEN-08，不能以最高作品猜标准。城市补贴的Tourism、theming、作品专属倍率/UI不等价于作品内在yield；保值与Base相邻补贴分开计算，白名单审计不靠本地化名称。 |

## Future适配边界（只记录，不实现）

完整Future Rule IDs及逐组适配见同步报告。所有Future均OUT_OF_V0.1，不能因接口预留而注册正式收益。

- GOV-002：未来以永久投资事务+已授予档位账本防止重复发放，授予与ACTIVE效果刷新分离；读档/总督移动不能重复支付或收回。头衔增加API和保存原子性尚待研究，不宣称已可用。GOV-003另由ACTIVE/当前政府事件重算可撤销槽位。GOV-001的建筑互斥、自动完成重入、一次性效果需专项可行性验证，不能以少给建筑作为默认fallback。
- ENT：工作专家和有效专家计数分离；只在Spec明确允许的自制机制入口使用虚拟计数，避免污染基础产出/GPP。网络效率扩展留独立参数，不改变ACTIVE。
- SPACE：未来卫星完成资格与城市Spaceport状态分别读取，资格进入同一来源/接收集合，按原因维护撤销；不依赖可见UI，不为自动连接伪造商路。
- LAND/REL/MIL/HARB/DIP/COMM与辅助系统尚无完整技术验证；未定参数引用Spec OPEN，不在Architecture补全或擅自套用NET-RC合并算法。

## 当前技术适配与边界

- Gameplay事件只提供dirty/历史诊断；完整权威provider仍缺失。B005的端点参数nil是失败候选，不因UI已通过而变为可用。
- UI/BackgroundRoutes读取当前全集，校验数量、端点与商人冲突，完整替换。LoadScreenClose/回合可直接采样，GameCoreEventPublishComplete/GameCoreEventPlaybackComplete消费dirty；最多跨边界3次尝试。SystemUpdateUI与Context更新在用户截图中未观测到，不能依赖其10秒兜底。
- ShadowRouteState为READY_UI_SHADOW、复制读取、revision幂等、dirty即UNKNOWN；owner:cityID只是快照身份，没有永久UID。
- DevelopmentTests/NetworkState仅离线原型：原Derive拒绝UI，DeriveShadow接受明确UI影子格式+MOCK_ONLY角色。拓扑继续只保留来源，strengthStatus=NOT_CALCULATED；Industry单独保持DESIGN_DECISION_REQUIRED。新离线NetworkStrength.FromState已完成Research/Culture max聚合，不接游戏效果。
- Probe.CityRoleFacts只读选中城市，专业/潜力写入者不存在，因此ACTIVE未知；首都候选与总督条件上限独立。B010实机待办已暂停，不能因模块存在判PASS。
- 以上均未接正式网络收益、Boost、折扣、施工队或巨作。


## IMPLEMENTATION_LIMITATION / DESIGN_CONFLICT

本次未发现必须修改D0001的已证实设计矛盾；未实现与尚未验证不等于不可实现。已知阻塞和潜在不等价如下，均未选择改变玩法的替代方案。

| 项目 | 限制及处理 |
|---|---|
| NET-004与纯Gameplay全集契约 | 当前后台UI能自动读取不等于Gameplay权威源已找到；保留原约束。若以后提出后台UI桥接作为正式事实，必须说明上下文/多人/时序影响并单独取得用户决定。 |
| PROG / OPEN-04、NET / OPEN-05 | 永久UID尚未实现；继承/旧档/首都本地资格有未决设计，不能从缓存推断。 |
| NET-RC / OPEN-06 | 浮点动态Modifier能力未证实；量化和封顶未定，不自行选择。 |
| IND-NET / OPEN-07 | 多源资格/折扣/输出尚待设计；Gold-only需接口实证。 |
| TERMS/GW / OPEN-08 | 原生复制范围、时代标准与theming/Tourism适配需确认，城市补贴不能默认为完全等价。 |
| Future GOV/REL/DIP | 全建筑/信条/永久保护的引擎控制边界需后续专项调查；不以实现方便削减设计。 |

## 同步与审计

后续设计变化由用户确认，Codex维护Dxxxx；每次架构同步核对accepted Spec hash，按Rule ID报告覆盖与限制后递增Axxxx。同步不改Status已有证据等级。当前D0001自身保留的“架构尚待同步”句子是接受时记录，当前同步进度以本文header和Status为准；不修改已接受Spec造成hash漂移。

[A0001原样快照](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_A0001_before_D0001_sync.md)保留过渡WHAT及调查；[早期完整架构](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_phase1_B010.md)保留旧设计审计。旧线性/逐源求和/Actual getter及写入者措辞不覆盖D0001。专项技术入口见[研究索引](../Reports/Technical/README.md)。

## A0003：离线多源强度接口

`NetworkStrength.FromState(state, player, coefficients, contextSource)`只接受显式MOCK_ONLY调用和已完成的单玩家拓扑。混合玩家来源/中心、UNKNOWN拓扑、非法ACTIVE/k或断裂接收资格返回UNKNOWN，不返回旧强度或伪造零结果。来源必须出现在当前中心connectedSources中；未接入高级源不参与。每类型全局选有效ACTIVE最高值，接收城市通过当前中心/来源资格去重，保留sources和maxSources供审计。连接到没有分发路线的中心的源仍属于有效接入源，按NET-RC-003参与全局L；N独立取实际接收集合。

输出包含routeRevision/contextRevision、player、networks.RESEARCH/CULTURE的L/N/k/networkStrength/sources/maxSources/recipients。缺少该类型来源或接收城市时给显式零强度；不存永久缓存。保留浮点，不提供Modifier Amount或取整方案。UI影子输入的输出仍标UI_SHADOW_ONLY，整体仅READY_OFFLINE_STRENGTH，不能变成Gameplay权威事实。真实角色/UID/路线可用性仍是外部前置。

[本轮本地结果](../Status/Validation/Results/Specialization_Network_Multisource_Local_Result.md)记录测试和限制。未来其它合法接收方式可通过同一中心/源资格结构表示；本轮不实现Spaceport、Entertainment或Industry合并。
