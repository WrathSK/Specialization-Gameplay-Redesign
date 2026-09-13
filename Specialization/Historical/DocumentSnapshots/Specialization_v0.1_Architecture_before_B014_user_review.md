# Specialization v0.1 Architecture — A0016

Document Owner: Codex
Architecture Revision: A0016
Design Spec Synced Through: D0002
Design Spec SHA256: 22c5023528aa1d0380ca96e89a8551d55d73d87bcfad8bb4a21e5ef29f4efa32
Sync Status: SYNCED_WITH_LIMITATIONS
Latest Accepted Design Revision: D0002
Latest Accepted Design SHA256: 22c5023528aa1d0380ca96e89a8551d55d73d87bcfad8bb4a21e5ef29f4efa32
Implementation Build: P0-B-014 / modinfo21

## CURRENT AUTHORITATIVE STATE

游戏设计意图只以[Accepted Design Spec](../Design/Specialization_v0.1_Design_Spec.md)为权威。本文负责实现方法、接口契约和技术限制，不再维护第二份数值表。此前D0001的SYNCED_WITH_LIMITATIONS表示完成该版规则映射并记录限制，不表示实现完成或游戏验证通过。当前已同步D0002的Rule适配与技术限制；Future经验API尚未验证，见[D0002差异同步](../Reports/Technical/Specialization_D0002_Architecture_Sync.md)。

完整Rule ID覆盖、同步检查与遗留差异见[同步报告](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)。唯一验证矩阵和待办见[Status](../Status/Specialization_P0_Status.md)。当前已完成离线多源强度和城市专业事实状态模型；运行新增B011只读完成探针，Mod UUID不变，B010仍未测；不启动游戏。

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

## A0004：当前全集来源复核

[第二轮静态调查](../Reports/Technical/Specialization_Trade_Authority_Second_Audit.md)确认HD CityYield有Gameplay GameEffects先例，但可见原生商路collection仅联盟/紧急事件范围，尚不能导出普通己方路线全集与端点。不能从Modifier subjects局部集合推断全国当前路线。未产生足够依据的新探针，不重复B005坐标或B010测试。原Gameplay权威约束保持；后台UI桥接若未来作为正式来源，必须另案说明改变及由用户决定。此限制阻塞正式Network运行结算，不阻塞独立本地能力研究。

## A0005：离线城市专业事实与ACTIVE

新增DevelopmentTests/CitySpecializationState.lua，按PROG-001至004处理显式MOCK_ONLY输入；不注册modinfo，不读写引擎Property，不生成真实城市UID或消耗单位。NewCity只接受已观测新建城市的显式事实。Restore不从已有区域/旧marker推断专业；缺失记录、所有权变化分别返回OPEN-04设计未决，失效城市/UID代际不符或损坏账本返回UNKNOWN。拒绝是离线适配保护，不决定征服后实际玩法。

永久schemaVersion=1包含cityUID、owner、revision、specialization、potential、firstCompletion(eventID/districtUID/family)、investments(receiptID→unitUID)。未选专业时不填Potential；Derive的active=0仅表示无专业能力，不增加设计Lv0。校验Potential与投资账本一致，恢复时投影永久字段，丢弃旧ACTIVE。每次操作返回新副本，错误不改输入。

Complete接收调用者提供的完整有序完成批次、已审计区域family映射与明确完成布尔值；只支持v0.1四族，已确认非v0.1用NON_V01忽略，未审计类型拒绝。首个有效完成锁定；已有专业不被后续区域替换；同一实例重复通知去重；未锁定时多候选同时完成不自行排序。这里的完整/有序是未来事件适配层必须证明的契约，不宣称现有游戏事件能直接满足，也不把同回合顺序自行定为设计规则。

PlanInvestment先只读检查专业、上限、己方在城Settler资格及已消耗凭据，返回expectedRevision，不消费单位；CommitInvestment只接受显式已提交MOCK消费凭据，核对预期revision、重复receipt/重复unit与上限后形成新事实。真实单位消费+持久账本如何原子提交尚未实现；未来必须在交易边界重新核对资格并保障帝国级单位一次性消费，不能先消耗再任意失败。当前receipt不是可直接从UI信任的命令。

Derive消费原P0总督探针的KNOWN门槛上限及明确城市UID映射，计算min(Potential, ceiling)。总督缺席/未建立/调离的原生上限1不改变永久投资；无法读取、跨城或不一致门槛返回UNKNOWN，不把错误默认为缺席。使用现有Probe.CityRoleFacts的离线桥接测试不代表B010通过；真实UID映射与事件读取未接入。

[本地结果](../Status/Validation/Results/Specialization_City_State_Local_Result.md)区分模型读档、Property游戏保存和真实Settler动作。后两项本轮未实现/未测；标准化账本、收益写入、Government未来头衔均不在本模块范围。

## A0006：区域族与完成通知候选

[接入调查](../Reports/Technical/Specialization_District_Completion_Adapter.md)确认官方/HD Gameplay的OnDistrictConstructed与CityBuilt先例。完成事件的类型索引需转换为Type，不可当实例ID；候选对象需独立核对IsComplete及owner/city/位置。HD的IsDistrictComplete还排除pillaged，不作为首次完成历史判断器。

离线DistrictFamily从Districts/DistrictReplaces构建可验证替代链；已知范围外为NON_V01、未知/坏图为UNKNOWN。DistrictCompletionCandidate仅产出候选，不承诺完整有序批次，不接永久事实写入。Property单表新副本写回可作为待测方向，但实际持久化/单位消费原子性、城市UID和事件重放时序仍未解决；未来先部署只读新事件探针，B010不重发。

## A0007：B011运行只读完成事件探针

CompletionProbe.lua仅订阅GameEvents.CityBuilt、GameEvents.OnDistrictConstructed、Events.DistrictAddedToMap与LoadScreenClose。仅记录测试文明；自动捕获后存ExposedMembers.SPC_P0.CompletionProbe，不写存档Property。每玩家最多64条，计数/序列与load阶段独立，丢弃旧条目明示。加载创建新记录集，不回填历史；完成通知与加入事件分别计数，绝不认作正式专业事实。

OnDistrictConstructed第二参数按类型解析，再CityManager.GetDistrictAt读取实例并核对owner/type/所属城市/IsComplete；异常和缺失值显式显示。DistrictAddedToMap只用前六个字段，不猜progress参数位置。Family沿当局DistrictReplaces有界遍历，仅诊断。原离线状态模块未注册进游戏，两个按钮只读缓存且支持两条/页，无RequestPlayerOperation、剪贴板或可见UI初始化依赖。

[本地结果](../Status/Validation/Results/Specialization_B011_Local_Result.md)与[用户两案](../Status/Validation/Cases/B011_Completion_Events.md)明确范围。本批成功也不证明真实CityBuilt建城、修复/征服时序、永久UID或正式状态写入通过；B010仍延后。

## A0008：B011实机事件顺序与加载边界

[用户结果](../Status/Validation/Results/Specialization_B011_User_Result.md)记录本次新城学院放置、完成和保存重载的实机观察。放置只有Added/NOT_COMPLETE，完成产生一次Constructed/COMPLETE_OBSERVED；本次重载只有加载期Added，不重放CityBuilt/Constructed。PASS限本次路径，不能泛化到自然跨回合生产、修复、征服或全部替代区域。A0007交付时未覆盖的真实建城，本次用户额外操作已提供有限场景证据。

建城时实测顺序为市中心Constructed → CityBuilt → 市中心Added。后续正式适配先排除NON_V01，不能让市中心抢占PROG的专业首次完成资格；不能假定CityBuilt先于任何区域通知。初始化与写入需幂等且不可覆盖已提交事实。加载期Added即使IsComplete=true也不得生成首次完成事实，已有区域的遍历顺序不代表历史完成顺序。当前仍只读，尚未实现永久UID/专业Property写入，OPEN-04保持原状态。

本轮校验发现当前Spec/ChangeLog已登记ACCEPTED D0002（Future Military II/III），且磁盘hash与ChangeLog一致；本轮未编辑Design。D0001同步hash对应[冻结原文](../Design/Revisions/Specialization_Design_Spec_D0001.md)。本次仅登记同步差距，不对D0002进行技术可行性背书或扩大v0.1实现范围。

## A0009：D0002同步与离线写入计划

D0002差异只影响Future Military与版本记录，当前v0.1规则不变；MIL-001/002/005–008、OPEN-10的适配见[差异同步](../Reports/Technical/Specialization_D0002_Architecture_Sync.md)。正常XP modifier与独立Insight保持不同结算路径；实际晋升、训练来源、战斗时采样和去重所需接口留待未来研究，不标可行性通过，不复制数值规则或启用军事机制。A0008末尾的待同步为当时记录，现由本节与header取代。

[写入准备](../Reports/Technical/Specialization_City_Fact_Write_Plan.md)新增MOCK_ONLY CityFactWritePlan，计划生成与提交分离；重复FOUNDATION只恢复已有有效记录，不清空投资；加载期不生成完成写入，RESTORE不补缺失历史。完整有序批次、持久身份仍是调用前提，原生事件不能自封为权威批次。计划的版本比较只在fixture提交器验证；真实SetProperty写入、读回确认和跨对象失败恢复未实现。运行保持B011，无新Property或正式收益。

## A0010：身份账本和故障恢复实验

[身份存储研究](../Reports/Technical/Specialization_City_Identity_Storage.md)核对HD Game/City表Property先例，新增MOCK_ONLY CityIdentityRegistry：分配序列和身份records组成单一envelope；复制后写、写前核对、单实例防重入、写后读回，setter报错仍不盲重试。相同已验证对象返回原编号，坏账本不重置；UNKNOWN禁止用于正式机制。

外部instanceProof和空账本首次创建资格仍是fixture前提，没有找到可直接替代它们的永久城市API。编号在存档分支内作用，不作跨存档ID。当前无Game/City Property adapter，单值原子性与持久性仅模拟假设；专业事实尚未纳入envelope，不能宣称解决跨Property事务。下一步独立DEV表存储探针先验证序列化，不用合成ID绑定真实城市，不决定OPEN-04，不新增正式收益。

## A0011：B012独立DEV表存储探针

StorageProbe仅由Gameplay处理STORAGE_READ/WRITE窄命令，测试文明门控，无需选城；Game Property键按玩家隔离，固定合成表不关联真实城市。空值才写一次，完整相同不写，读失败/不一致不覆盖；setter抛错仍读回判断，不自动重试。UI通过既有token ACK显示，不读写Property。加载不自动创建数据；因此重载后先Read可以检测丢失，不能由自动补写掩盖。

本轮只验证单值表往返，尚非身份分配/专业事务实现；不提供原子保存、多人或崩溃恢复保证。详见[B012本地结果](../Status/Validation/Results/Specialization_B012_Local_Result.md)及[两案](../Status/Validation/Cases/B012_Table_Storage.md)。运行B012/modinfo19，UUID不变，B010延后。

## A0012：B012表存储实机证据

[用户结果](../Status/Validation/Results/Specialization_B012_User_Result.md)证实本次合成Game Property表的写后完整比较、重复操作不写及保存重载后只读恢复。该结构的字符串键、嵌套数值与布尔值在实测环境保持；不能外推任意结构/大小、多人同步、崩溃原子性或真实城市代际。后续可使用此证据继续身份/事实持久化准备，仍需独立解决instanceProof、初始账本资格及OPEN-04，不把DEV-1/2绑定到真实城市。

## A0013：城市双侧绑定恢复准备

[恢复方案](../Reports/Technical/Specialization_City_Binding_Recovery.md)将总账预留、城市token与确认分开，缺一侧UNKNOWN不自动补写；双侧匹配才计划确认。新增MOCK_ONLY恢复判定及测试，不把ComponentID/owner/cityID/坐标当永久UID。运行仍B012，无新Property；真实代际与跨Property恢复仍需后续探针。

## A0014：B013 DEV新城绑定探针

BindingProbe运行记录仅服务于DEV验证，不是正式UID或专业事实。加载后CityBuilt核对当前城市，预留Game账本→城市token→确认Game账本；旧城不补写，部分失败拒绝自动修复。加载审计与BINDING_READ均只读Property，不依赖UI初始化事实。最多32座DEV新城，总账/城市分别计尝试次数，重载清零。

缺总账时扫描现有城token仅防可见残留；不证明所有痕迹丢失时仍能识别旧账本，亦未确认征服/毁城/引用复用全部语义。原有OPEN-04及正式身份前提保留。详见[B013本地结果](../Status/Validation/Results/Specialization_B013_Local_Result.md)；运行B013/modinfo20，等待两案，不接专业或收益。

## A0015：B013正常新城与重载证据

[用户五图](../Status/Validation/Results/Specialization_B013_User_Result.md)确认被测旧城不补写、新城Game账本/City token一致，正常保存重载后同token/CONFIRMED保持且写入0/0。可继续研究与完成事实关联，但不将DEV token自动提升为正式UID，不扩大到征服/毁城/首都初建/全部生命周期或崩溃原子性。下一步先限定正常新城与已明确的PROG规则，OPEN-04仍保留。

## A0016：B014绑定城市的完成观察持久化

新增CompletionRecordProbe将live OnDistrictConstructed经对象/完成/替代族/有效绑定核对后保存City DEV观察表，加载与Added不生成，已有有效观察不覆盖；BindingProbe只读Resolve验证双侧token。FIRST_OBSERVED_COMPLETION明确不代表历史首个完成，不构成正式专业或完整有序批次。OPEN-04、首次初始化仍保留；详见[B014本地结果](../Status/Validation/Results/Specialization_B014_Local_Result.md)。运行B014/modinfo21，等待用户两案，无正式收益。
