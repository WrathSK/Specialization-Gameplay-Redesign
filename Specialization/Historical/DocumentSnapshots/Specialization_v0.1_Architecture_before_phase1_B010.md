# Specialization v0.1 Architecture — B010

## CURRENT AUTHORITATIVE STATE

更新：2026-09-11。本文是当前机制与实现边界；历史材料不再覆盖本文。用户负责全部 Civilization VI 实机验证。助手不启动、操作或等待游戏；本地静态/模拟通过不等于游戏通过。

### 当前交付范围

运行包 P0-B-010（modinfo version 17，UUID 不变）仍是独立测试文明与诊断工具。本轮在已有离线Trade Route State/拓扑原型上，安装独立后台UI影子读取与Gameplay交叉对照探针；没有接入正式专业、Boost、折扣、生产力、Settler、施工队或巨作能力。

Scotland (Specialization Test) / Robert the Bruce (Test) 使用独立 CIVILIZATION_SPC_TEST、LEADER_SPC_TEST、TRAIT_CIVILIZATION_SPC_TEST；复用 Scotland 展示资源，不复制原 Scotland gameplay traits，不改原版文件。正式作用范围按玩家文明/领袖身份验证，不能以本地玩家 UI 作为全国结算条件。原型先验收单人；多人确定性另验。

四种专业：Campus→Research、Theater Square→Culture、Industrial Zone→Industry、Commercial Hub→Commerce；包括核实的替代区域族。IZ 按原科技位置，不改为提前解锁的特色区域。其它专业不进入 v0.1。

### 永久事实与派生状态

首次完成四类中的一个区域后锁定专业，不以放置区域为完成；默认潜力1，上限4。Settler 在己方城市的合法动作永久增加潜力并消耗单位；此动作尚未实现。高级能力由潜力与已建立总督的城市原生头衔门槛共同控制；当前门槛参数2/3/4，未建立或调离后只保留已选专业的 Lv1。没有专业时不凭空获得能力。

总督读取使用已实测的原生 Requirement→城市 Property 门控。值1为激活；nil/0不激活，不使用 Lua truthiness 判断0。不重试已失败的城市/玩家 GetAssignedGovernor。原生门槛不能反推出所有 Mod 免费晋升的历史净支出。

永久保存：专业、潜力、首次完成事实、标准化模板账本及将来动作幂等凭据。派生：当前总督条件、商路缓存、Trade Center network set、来源、接收集合、Network Strength、效果门控。派生状态加载后由真实游戏状态重建，绝不能仅凭旧事件恢复。

城市稳定 UID 将由独立身份映射层提供，owner/cityID 是当前引擎引用而非永久 UID。征服可能改变 cityID；原地重建必须新 UID。跨征服的专业/投资继承规则、UID迁移尚未实现，不能用中心 plot 冒充唯一永久身份。

### Trade Route State：强制契约

流程：`Gameplay authoritative full source → normalize → deduplicate → atomic replace → source connections → distribution recipients → per-network recipient sets`。

当前 **没有已确认的 Gameplay 全集 provider**。B004 单位 operation 探针只是候选诊断，不连接正式状态层。UI city:GetTrade():GetOutgoingRoutes() 虽已实测通过，也不能满足本轮 Gameplay 权威源要求。HD Temp_Interface 实际注册为 AddUserInterfaces，文件夹名不代表执行上下文。

离线 `DevelopmentTests/TradeRouteState.lua` 接受明确 COMPLETE/GAMEPLAY/GAMEPLAY_CURRENT 契约，只允许未来经过审计的 adapter 提供该契约；测试中 MOCK 是唯一来源。接口返回失败、部分列表、Unknown、UI snapshot、历史事件或 operation candidate 时，Read 返回 UNKNOWN，不返回假空集合或旧有效路线。lastGood 仅供诊断，不能结算。

成功全量刷新原子替换集合，集合中消失的路线撤销；重复刷新不累计。额外核对端点存在、当前owner/cityID、战争状态；明确不存在或易主撤销，解析失败则整次UNKNOWN。事件仅标dirty，重复dirty合并；初始化/读档不依赖事件历史。未来provider必须有安全就绪时点、同回合dirty处理和回合核对。本轮探针只在初始化、LoadScreenClose、测试玩家回合开始/结束读取，不宣称达到正式即时撤销时序。

Route record：key、identityKind、可选engineRouteID/traderUnitID、originPlayer/originCityID/originUID、destinationPlayer/destinationCityID/destinationUID、domestic、current、validity。没有 UI 名称、路径 plot、yield 表。优先实际引擎 route ID（若以后证实）；目前未发现暴露的稳定 route ID。备用key为带长度前缀的 owner+traderID+originUID+destinationUID，只保证当前快照内识别与刷新去重，不宣称跨单位ID复用/新旧同端点任务拥有永久身份。所有字段重新读取，不用key继承旧current状态。同城对不同商人分别保留；同一商人冲突记录拒绝整次刷新。

NetworkState 原型保存每中心 connectedSources[sourceUID][qualification]、distributionRoutes；每类型 recipients[cityUID] 保存 source集合、center集合及中心→源→接收资格。源信息含owner、kind、activeLevel、templateRevision。routeRevision 与 contextRevision 分开：中心身份、ACTIVE、模板变化无需修改路线事实，但需重新派生。原型不计算权威L、不发收益、不注册到modinfo。

### 虚拟建筑作为网络标志：候选，不作为权威事实

用户提出每类型网络一个虚拟建筑的构想。保留为效果载体/可重建标志候选，暂不实现。真实路线与多来源资格集合先计算，再对账建筑；失去最后资格才移除。单个建筑布尔值不能表达方向、源城市、多个等级/模板与支撑路线，不能只靠建立/结束事件建拆来解决漏事件、旧档初始化。源或中心网络变化时，即便路线不变也需重算。内部建筑可能影响第三方建筑统计，需专项验证。详见B005_User_Result。

### 网络规则

- Trade Route Capacity 就是带宽；没有额外资源、逐路载荷、round-robin或手动分配。
- 己方专业源 S→己方中心 H 的有效路线形成直接接入；当前首都与商业专业城市有中心身份。
- H→己方城市 D 的每条有效分发路线自动携带 H 当前全部接入类型。外贸、道路、贸易站不当作这种接入。
- 不递归转发：另一个中心收到网络，不因此变成该网络的直接源。源/中心重合的本地接入资格由单独显式输入处理；不会虚构路线。原首都本地自接入提案保留待规则核定。
- Research/Culture 强度唯一公式为 `k × L × sqrt(N)`；k_R/k_C 独立，初值各1。Research增加 Inspiration，Culture增加 Eureka。
- N是该类型实际接收的己方城市UID去重数。重复路线、多中心同城、免费接收资格重叠不增加N。N=0则强度0。
- Commerce IV把本中心作为免费接收资格并入集合，只获得network effects。已经接收就不重复计数；失去免费资格但保留其它有效资格时仍接收。没有固定额外百分点。
- 多中心/多源不同ACTIVE的权威L **DESIGN DECISION REQUIRED**。禁止逐中心求和、Σ(kL√N)、擅自max/average/sum。Industry也只保留源、模板与等级信息，不把旧“不同源锤相加/取最高折扣”当作已定结算规则。

### 已确认数值设计（本轮不实现）

| 专业 | Lv1 | Lv2（追加） | Lv3 | Lv4（追加） |
|---|---|---|---|---|
| Research | 每专家额外3F3P | 区域本体/每级建筑各1住房；每专家2基础Scientist GPP | 专家粮锤提升到5F5P；0.5×人口×工作专家数基础Science | 每专家城市Science加5个百分点；其它合格非Campus区域原生复制基数总和50%转Science |
| Culture | 每专家额外3F3P | 同住房；每专家Writer/Artist/Musician各2基础GPP | 5F5P；0.5×人口×工作专家数基础Culture | 每专家城市Culture加5个百分点；旧作保值与巨作基础相邻补贴 |
| Industry | 每专家3F+IZ Base生产相邻；固有施工队项目 | 同住房；每专家2基础Engineer GPP | 5F+原100% Base生产相邻，另2×Base生产相邻Gold | IZ Production原生复制基数50%经网络输出 |
| Commerce | 每专家3F3P；中心身份 | 同住房；每专家2基础Merchant GPP | 5F5P；每接入Research/Culture/Industry类型，专家分别2S/2C/2P，同类型多源不翻倍 | 免费自接收已接入网络，仅网络效果 |

新增GPP必须进入基础层后再吃正常百分比。不能用直接ChangePointsTotal/金币余额/科技进度冒充基础产出。专家承载建筑方案需验证岗位估值、倍率与其它Mod建筑统计；城市基础补贴不自动等价于岗位本身变化。

### Base 与 Actual 的当前语义

Base：Industry I/III专家锤/金、Culture IV巨作相邻使用基础相邻。政策翻倍对照的UI getter已通过已测场景；跨yield完整性和Gameplay适配不因此通过。

Actual统一内部命名 **NativeDistrictCopyBasis**：按煤电厂/大酒店原生区域复制算法，不以district:GetAdjacencyYield定义替代。Research IV按合格非Campus区域各yield复制基数之和×0.5；Industry IV仅IZ Production复制基数×0.5。不以城市总产出替代，也不要求已建原复制建筑。行业固定产出是否纳入按原生复制实测决定，不能提前排除。大酒店独立相邻Tourism modifier不是此次基数定义。

Building_YieldDistrictCopies只有BuildingType/OldYieldType/NewYieldType；没有50%或跨城目标参数。需要独立适配，不擅自改比例。写回城市层并先采集后统一应用，避免把自身补贴再次算入源。区域族需审计，不能只靠RequiresPopulation判定。

### Boost、工业模板、施工队、巨作

Boost：Lua算sqrt与未取整浮点，再交独立BoostAdapter；动态实例不能假定接受任意Amount。数据库Value是TEXT只证明存储，不证明小数或表达式可被引擎执行。整数/固定精度量化须先报告并获规则，不自行round/floor/ceil；不硬编码基础40%。触发时结算、已触发不补发，超额不得流入下一科技/市政，实际引擎行为待测。

Industry Gold折扣按I/II/III/IV为10/20/30/40%；目标必须接受工业网络，接入源曾完成同District+Building Tier模板。可明确hardcode tier组，不能把未识别建筑扩成整区折扣。只影响Gold，Faith变化不可默许。模板永久记录，但源断开/毁灭不能继续作为当前资格。多源组合保留信息待定，不结算。

施工队从Industry I起，固定Project→Crew五档：280→250、460→420、820→750、1100→1000、1500→1360；不加1800/2000档。己方城市合法当前Building/District/Wonder按min(charge,remaining)注入，剩余浪费、不递归overflow；空/非法目标拒绝不消耗。项目速度缩放、真实成本、事件重入、单位生成消费仍待验证。

Culture IV旧作保值优先隔离的城市基础补贴：按类型/时代标准补差；时代曲线不能凭空取最大值，时代口径/缺档与自定义类型待明确。城市补贴不自动拥有theming/Tourism/GreatWork-specific modifier语义。巨作相邻另算每件合格作品×0.5×本城合格区域各Base yield。优先标准文化作品，排除Product；Writing/Music/艺术/Artifact白名单及Relic/未知分类的最终审计另案，不以本地化名称猜测。

### Future auxiliary（不在本轮/v0.1实现）

Spaceport不是专业。玩家完成Launch Earth Satellite后，仅拥有Spaceport的己方城市双向自动接入：自身专业接入中心，同时接收中心所有已接入网络，不占路线容量，不要求实际分发路线；不是全帝国自动联网。不加飞天生产、Science、Production或激光效率。未来资格同样进入去重集合。

Entertainment Regional Support未来调整k或最终Strength效率，不提高effective level，不恢复每路线线性百分点。

## CONFIRMED

B005修复记录：B4-1截图显示LoadScreenClose自动回调已执行；GetUnitType在Gameplay缺失导致后续扫描中断。按官方/HD Gameplay先例改用GetType。旧接口失败保留历史；后续用户B4-1/B4-2两图确认GetType、CountOutgoingRoutes、四名商人任务枚举及存读档同样列表USER_GAME_TEST_PASS。但四组X0/Y0/X1/Y1均nil，当前端点参数路径USER_GAME_TEST_FAIL；完整路线恢复仍BLOCKED。详见Specialization_P0_B005_User_Result.md。

USER_GAME_TEST_PASS：独立测试文明选择开局；City marker写读/真正读档；新局总督present/established、2/3/4阈值与调离撤销；区域类型/完成/专家人数；UI Base与政策后相邻区分；UI商路端点/同城分页/三条场景读档；Gameplay新增路线端点事件。确认范围不扩展到正式网络/收益。

STATIC_CONFIRMED：独立数据库/资源关系；原生总督门控先例；官方Pirates Gameplay可读取CountOutgoingRoutes和使用TradeManager判定CanStartRoute；HD Temp_Interface由UI加载；原生区域复制表结构。具体来源见B004_Trade_Route_State报告。

## LOCAL_SIMULATION_PASS

既有探针/身份数据库/sqrt计算测试；新增TradeRouteState全量替换、空集、重复、撤销、易主、错误缓存覆盖、失败隔离；NetworkState去重与来源资格、中心/ACTIVE独立变化；B004自动探针初始化/LoadScreenClose/回合调度与未知API保护。所有权威源均为MOCK，不能登记实机PASS。

## USER_GAME_TEST_REQUIRED

B010本轮只测首都/非首都的ROLE只读信息，见B010_City_Role_Facts。正式专业/潜力写入者尚不存在，UNKNOWN是预期，不能据现有区域猜测。

B009的B9-1已USER_GAME_TEST_PASS：新增Stirling→Edinburgh，3→4、+1/-0，标准缓存rev 1→2；模块装载与本次新增输出通过，见B009_User_Result。不重复本批或旧初始化/读档/删城测试。

B4-1/B4-2已经返回，不重复。只读任务枚举/读档子项已通过，端点参数nil需先研究新候选；B007新三路线存档初始化/读档已通过，不重复；B007城市删除变体未重建的历史失败已由B008修复；当前B6-3-CITY完整重建已通过，见B008_User_Result；原删除商人案例未执行；不重复Gameplay任务读取。

已测初始化/读档可以列举任务，但端点未获得；后续只测试新的端点方案及未验证撤销，不重复本批读取。完整route完成/取消/战争/征服/夷平撤销与安全事件时序需等provider候选成立后另案。B003显示调整可顺带观察，不重测已通过UI功能。

后续其它P0：原生复制基数、可撤销效果写回、GPP基础层、Boost精度、Gold-only折扣、施工队四案、巨作类别/补贴交互。当前均未实现正式能力。

## B008：后台UI初始化/读档与本次删城重建已通过

用户认可此研究方向后，新增无控件的独立InGame context。初始化与load/回合直接采样，SystemUpdateUI消费路线dirty；Context更新另提供约10秒兜底，但仅在该回调实际运行时有效。读取本地Test玩家当前Outgoing全集；标UI_SHADOW_ONLY，不接正式RouteState/网络收益，不调用BTS或打开窗口。完整快照原子替换，错误/未就绪清除可用snapshot并报UNKNOWN。读前后计数、端点owner、商人冲突检查；Gameplay只读对照数量与商人ID，已知样本过期时PENDING。数量/ID相同不证明UI端点的权威性。

P0的Background routes按钮只看缓存，不采样。独立context关闭时清理事件与导出；临时派生数据不保存到Property。该方案只消除玩家打开窗口的需要，不消除UI上下文/客户端调度依赖，正式权威来源规则与多人范围仍未改。新本地模拟已通过。用户最新三图确认初始化/读档USER_GAME_TEST_PASS；B007城市删除后UNKNOWN且刷新次数不增长为历史USER_GAME_TEST_FAIL；B008用户截图现确认3→1、+0/-2并保留Aberdeen→Stirling，完整重建USER_GAME_TEST_PASS。系统通知与Context更新计数均0，两个回调在本场景尚未观测到，不能视为可靠兜底。B006截图仅显示UNKNOWN / LoadScreenClose，标USER_GAME_TEST_FAIL；不能据此断言路线getter失败。B007新增刷新/系统通知/Context更新计数，本地无Context更新的加载与dirty回归已通过。修复背景见Specialization_P0_B007_Background_Dispatch_Fix.md；最新实机结论以Specialization_P0_B008_User_Result.md为准。不将Cheat Panel删城等同商人删除或正常征服/夷平。

B008调度增量：采用原版MinimapPanel/ResearchChooser的GameCoreEventPublishComplete批次dirty刷新先例，并监听GameCoreEventPlaybackComplete；失败最多跨边界尝试3次，新信号/回合可恢复。新增计数与采样入口用于定位。无Context/SystemUpdateUI回调的本地恢复与重试上限模拟通过，发布完成路径本次删城重建实机USER_GAME_TEST_PASS；失败重试分支仍USER_GAME_TEST_REQUIRED。读取源及UI_SHADOW_ONLY约束不变，细节见Specialization_P0_B008_Batch_Flush.md。

## B009：标准UI Shadow Route State

独立纯Lua缓存位于ShadowRouteState.lua。输出READY_UI_SHADOW与明确UI_SHADOW_ONLY标签，标量路线记录不含display/path；owner:cityID仅快照身份，不替代永久UID。全量替换、同集合revision幂等、dirty/错误即UNKNOWN、读取复制、context重建清空；新增ReadNormalizedRoutes只读出口，没有正式消费者。原GAMEPLAY_CURRENT状态层准入不放宽，NetworkState不接此输入。四组本地回归通过。B9-1用户两图已确认模块装载和新增路线后标准count/revision更新USER_GAME_TEST_PASS；副本隔离/错误/reset仍为本地模拟范围。详见Specialization_P0_B009_Shadow_State.md及Specialization_P0_B009_User_Result.md。

## 标准路线到来源拓扑：离线衔接

NetworkState新增DeriveShadow单独入口，接受B009标准UI影子记录与显式MOCK_ONLY城市角色上下文，输出READY_SHADOW_PROVENANCE_ONLY。原Derive的READY准入不变，不把UI伪装成Gameplay；不假造永久UID。共用拓扑算法保留全部来源资格、按城市去重N、不递归转发；不合并多源L或结算收益。标准schema衔接、多源撤销、中心身份/ACTIVE/模板变化等本地模拟通过，当前无运行消费者，本轮无新实机测试。详见Specialization_P0_Shadow_Network_Integration.md。

## B010：真实城市角色的部分只读事实

Probe.CityRoleFacts在Gameplay既有Read governor请求中只读选中城：首都候选、旧诊断专业值（不采纳）、原生总督条件上限。正式专业/潜力/首次完成写入者尚不存在，因此均标未知，ACTIVE不由总督条件独自确定。首都确认时center=YES_CAPITAL，非首都专业未知时center=UNKNOWN。输出PARTIAL_ROLE_FACTS，不提供NetworkState的READY角色上下文；无属性写入或历史补造。三组本地测试通过，首都候选实机待验。详见Specialization_P0_B010_City_Role_Facts.md。

## BLOCKED / DESIGN DECISION REQUIRED

- BLOCKED：未找到已确认的纯Gameplay当前路线全集接口；状态原型无法连接正式机制。B006已实现仅诊断的UI影子读取；若用于正式权威来源仍需明确改变原约束并验证，目前未接线。不能改用日志/历史事件。
- BLOCKED：多源Boost数值合并，等待设计；本轮不强迫用户决定。可讨论统一代表源、每源覆盖归属、覆盖分组再定义单一合成规则，但不采用任何一种。
- DESIGN DECISION REQUIRED：Industry多源模板资格/折扣/Lv4输出合并；城市UID跨征服/重建与继承；首都本地自接入具体规则；Boost量化（仅必要时）；若干后续建筑tier/作品分类边界。

## HISTORICAL NOTES / superseded

完整旧Architecture与Status逐字保存在Historical/*_through_B003.md；旧版本报告只用于审计。废弃：routeCount×L、per-route百分点、逐中心求和、Commerce IV固定追加；旧“科研文化取最高有效等级”和“工业不同源加总/最高折扣”不能当作当前已定规则。旧Actual getter口径已由NativeDistrictCopyBasis替代。

A001–A004与B003旧“尚无实机PASS/待测基础接口”均已由上方证据矩阵替换；曾失败的Governor/getTrade接口仍保留历史失败证据，不重新启用。历史模糊UI/Game商路PASS误记已更正，当前UI与Gameplay事件各有独立用户证据。
