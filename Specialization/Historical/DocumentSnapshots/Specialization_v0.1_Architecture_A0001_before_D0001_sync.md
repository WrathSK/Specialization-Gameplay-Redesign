# Specialization v0.1 Architecture — A0001（过渡权威）

Document Owner: Codex
Architecture Revision: A0001
Design Spec Synced Through: NONE
Design Spec SHA256: NOT_APPLICABLE_NO_ACCEPTED_SPEC
Sync Status: PENDING_INITIAL_DESIGN
Implementation Build: P0-B-010 / modinfo17

Design Spec目前仅DRAFT_SHELL；接受D0001前，下方已确认WHAT继续作为过渡权威，不提前删除。
用户本次明确确认的Research/Culture多源规则已登记在“网络规则”；等待Design Chat写入D0001，尚未实现或验证该合并算法。
验证状态和唯一待办见[Status](../Status/Specialization_P0_Status.md)。历史报告不能覆盖此文。

## CURRENT AUTHORITATIVE STATE

更新：2026-09-11。本文是当前机制与实现边界；历史材料不再覆盖本文。用户负责全部 Civilization VI 实机验证。助手不启动、操作或等待游戏；本地静态/模拟通过不等于游戏通过。

### 当前交付范围

运行包 P0-B-010（modinfo version 17，UUID 不变）仍是独立测试文明与诊断工具。已有离线Trade Route State/拓扑原型、独立后台UI影子读取与Gameplay交叉对照探针；当前仅整理文档，功能开发暂停；没有接入正式专业、Boost、折扣、生产力、Settler、施工队或巨作能力。

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

成功全量刷新原子替换集合，集合中消失的路线撤销；重复刷新不累计。额外核对端点存在、当前owner/cityID、战争状态；明确不存在或易主撤销，解析失败则整次UNKNOWN。事件仅标dirty，重复dirty合并；初始化/读档不依赖事件历史。未来provider必须有安全就绪时点、同回合dirty处理和回合核对。Gameplay任务探针在初始化、LoadScreenClose、测试玩家回合边界读取；UI影子采样另在事件发布/播放完成边界处理dirty。两者不混作Gameplay权威全集。

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
- **已确认设计，等待D0001正式登记（2026-09-11用户结构整理授权补充）**：Research/Culture等共享全局Network Strength的同类型网络，`L = max(all valid source ACTIVE specialization levels)`，再统一计算`Network Strength = k × L × sqrt(N)`。使用ACTIVE而非Potential；来源数本身不增加N；N仍为当前实际接收该类型网络的己方城市去重数。禁止分别算各源后求和，禁止`Σ(k × L_i × sqrt(N))`。最高级源失效后立即回退到剩余有效源的最高ACTIVE；无有效源时不得保留旧强度，空集边界的具体适配须显式处理。
- 上述max规则不自动适用于Industry Lv4等按来源分别输出的机制。Industry模板资格/折扣/输出合并仍独立待定；不采用旧“不同源锤相加/最高折扣”假设。
- 正式Spec Rule ID由Design Chat在D0001中分配，当前不伪造已接受Rule ID。

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

## 当前技术适配与边界

- Gameplay事件只提供dirty/历史诊断；完整权威provider仍缺失。B005的端点参数nil是失败候选，不因UI已通过而变为可用。
- UI/BackgroundRoutes读取当前全集，校验数量、端点与商人冲突，完整替换。LoadScreenClose/回合可直接采样，GameCoreEventPublishComplete/GameCoreEventPlaybackComplete消费dirty；最多跨边界3次尝试。SystemUpdateUI与Context更新在用户截图中未观测到，不能依赖其10秒兜底。
- ShadowRouteState为READY_UI_SHADOW、复制读取、revision幂等、dirty即UNKNOWN；owner:cityID只是快照身份，没有永久UID。
- DevelopmentTests/NetworkState仅离线原型：原Derive拒绝UI，DeriveShadow接受明确UI影子格式+MOCK_ONLY角色。现代码只保留来源，**尚未实现本次确认的共享强度max合并**；旧注释“合并未定”属于已落后于设计的实现说明，源码本次不改。
- Probe.CityRoleFacts只读选中城市，专业/潜力写入者不存在，因此ACTIVE未知；首都候选与总督条件上限独立。B010实机待办已暂停，不能因模块存在判PASS。
- 以上均未接正式网络收益、Boost、折扣、施工队或巨作。

## IMPLEMENTATION_LIMITATION / 待决索引

| 项目 | 当前分类 | 处理 |
|---|---|---|
| Research/Culture多源L | 已确认设计，等待D0001登记 | max有效ACTIVE、统一一次公式；代码未实现，暂停开发 |
| 纯Gameplay当前路线全集 | IMPLEMENTATION_LIMITATION / BLOCKED | 不将UI影子来源伪装成权威；未来若改变来源约束须明确用户决定 |
| Industry多源资格/折扣/Lv4 | DESIGN_DECISION_REQUIRED | 不套用Research/Culture max规则 |
| 永久UID、征服继承、旧档专业初始化 | DESIGN_DECISION_REQUIRED / 未实现 | 不据现有区域补造首次完成历史 |
| 首都本地自接入、Boost量化、建筑tier/作品分类边界 | DESIGN_DECISION_REQUIRED | 保留既有未决范围，不自行改设计 |

## 文档sync约定

Dxxxx只由Design Chat登记；Axxxx由Codex递增。接受D0001后，Codex核对完整Spec与SHA256，按正式Rule ID评估适配/冲突，最后推进Synced Through。CONFLICTS_RECORDED不表示已实现；设计冲突用DESIGN_CONFLICT或IMPLEMENTATION_LIMITATION明示。当前空壳不计算为已同步设计。

## 技术与历史入口

当前[技术索引](../Reports/Technical/README.md)仅保留HOW和证据引用；[验证/待办](../Status/Specialization_P0_Status.md)是唯一当前状态入口。
迁移前完整[Architecture快照](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_phase1_B010.md)保留所有过程；旧逐源求和、线性per-route与旧Actual getter定义均不可覆盖当前规则。此前“max未定”的历史说法已由本次用户设计确认取代。
