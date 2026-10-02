# P0-N1/N2/N3 — 人文考察、文化见闻与网络准备计划

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED。N1原生交互、N2持久记录/整城旅游、N3网络各为独立门禁。
Authority: Culture D0029 `CUL_L4_EXPEDITION`、missions、contracts.expedition/observations/network_effect；Shared D0035与现有Network基础合同。当前运行基线见[准备入口](Culture_Preparation.md)。

## 不可混淆的三个系统

人文考察团是来源永久绑定的单位和远程任务。文化见闻是原Owner/来源城的永久成果。Culture Network仅传播各来源自己完成的文明集合价值，不给接收者见闻所有权。三者不能用旧Eureka Strength替代，也不能由单位或UI独占持久authority。

## 已接受的完整任务规则

Culture ACTIVE4训练；成本以**当前Spy Production cost**为初版参考，远程部署距离/时间参考Spy，非地图步行。没有已批准容量上限，不继承Spy slot/capture/failure。source降ACTIVE4以下，已有单位仍可继续任务/获得记录；本地旅游及Network输出按当前正常资格另门控。

目标为已遇见、存活的外国Major，城邦/Free Cities排除；不要求开放边界、使馆、同盟或商路。战争允许部署/开始/继续/成功，宣战本身不取消。每个合法任务确定成功，没有间谍失败、死亡、俘获或外交惩罚；成功后单位保留，可再次部署执行未完成任务。

| 类别 / Mission | 目标资格 | 首次成功成果 |
|---|---|---|
| PEOPLE 风土考察 | 对方当前实际控制的首都 | 该source/原Owner/文明的PEOPLE记录与1见闻 |
| WORKS 艺文采撷 | 目标城至少1件当前合格巨作，严格同一work_pool | WORKS记录与1见闻；不偷、复制或消耗作品 |
| PLACES 奇观巡礼 | 目标城至少1座已完成Wonder | PLACES记录与1见闻；不反推实际建造者/模板历史 |

任务时间`floor(2 × game-speed turn-duration multiplier relative to Standard)`；2为初版参数，部署另算。不得擅自round或加min1；极快速度出现0的精确执行阶段须原型说明，不偷偷改公式。Spy成本与部署关系要按本次最终数据/引擎读取，不能固定沿用本机缓存60或猜距离公式。

目标失去必要作品、首都迁移、目标城易主或文明淘汰→取消，无奖励/不消耗成功机会，单位保留。战争不是上述失效。UNKNOWN不得当目标失效、无作品或已完成；到期确认不足时HOLD并有界复核，不无条件成功。部署及任务过程无自动化派遣。

## 唯一性与ownership合同

唯一键为`原Owner × source persistent city × foreign civilization × category`。每键首次成功+1不可消费/交易见闻；每source最高3N来自三类×N文明，无时代刷新、无限重复或新增cooldown。外国文明后来死亡不删除已可靠记录历史。

三类都在**同一个source/原Owner账本**完成，该文明才进入S_source。source本城当前合格且ACTIVE4：整城Tourism百分比=`K_T × owned observations`；K_T仍null、候选1–3%，不能选值/填0。记录在不激活时保留；原主人失城记录休眠，新的Owner不继承，原主人取回对应source可按正常资格再用。此scope与跟城转移的Dialogue累计/quota不同，不统一永久成果继承。

unit reference只是任务执行对象；source/unique成功凭据及记录由Gameplay持久层拥有，不能随单位销毁或UI关闭丢账本。单位被外部机制删除时不得凭空补成功或清已完成记录；任务退出/重建策略按实际生命周期合同核对，不新增Gameplay死亡惩罚。

## N1：交互与来源绑定原型

Goal：最小训练来源证据→一个合法外国目标→远程部署状态→任务交互；没有见闻、旅游、新Network或正式奖励。应先静态调查原生Spy command/UI和HD替换，再选择忠实的最小实现。

本轮现有缓存确认Spy字段，但当前Mod没有新考察团训练/远程mission writer；前期Spy-like候选调查不是原生兼容PASS。**直接复用Spy=1可能继承容量、敌对任务、战争召回；Spy=0也不能据字段存在假定可用同一部署命令。** 候选为能隔离敌对机制的原生路径，或本Mod单一单位/任务的受控远程选择UI＋既有阶段计时；两条都需要prototype，不能退化为地图行走或固定距离。

训练/完成事件需证明source，复用现有项目/production receipt技术时只采用已证来源，不用单位站在哪城、名字或最近城市猜来源；一次登记、重复unit event幂等。不能借本轮强制实现Industry未来capacity/source体系。Spy PurchaseYield=Gold不是考察团购买授权，涉及该入口时先核对正式训练范围。

外国Works事实只能对选中/执行中的目标定域请求：沿同一已支持作品目录与已确认位置/owner读取，Gameplay复核；不把本地K完整scope协议改为全世界广播。PEOPLE/PLACES分别提供current capital/completedWonder事实，UNKNOWN保持明确。

原型最小验证：远程目标选择/部署时间、三类资格静态fixture、战争前后部署/保持、目标易主/作品丢失/首都迁移取消、source ACTIVE下降不回收既有unit；成功后单位保留。不可隔离原生capture/强制战争召回等则停止对应路径，登记TECHNICAL_INVESTIGATION_REQUIRED/IMPLEMENTATION_LIMITATION，不变Design。

N1之后才审核N2具体实现；UI prototype仅用一个目标/单位，不能据“界面打开了”宣称任务持久或正常战争行为可行。

## N2：source任务、永久见闻与整城旅游

N1远程交互/source证据通过后增加专属持久块：unit→source＋original owner绑定、当前部署/mission/目标文明和ref/起止阶段；source→已成功类别集合/凭据。用现有E2可靠映射和Game保存模型，**不创建新cityKey、全世界建筑历史或统一Legacy框架**。Claim timer的业务规则不直接复用。

开始验证target/current owner/source绑定和未完成键；完成重新确认目标事实，唯一成功事务一次写账本/凭据，再派生见闻数、S_source及本地旅游。重复completion/load不重奖，失败/cancel不占success key。ACTIVE下降的source仍可收记录，但本地effects和Network输出不激活；unsupported新owner不运行专业。

先做任务/ledger影子与纯集合模型，再做整体Tourism native gate；K_T未定不妨碍本地fixture/交互调查，但正式收益不能自行选择。`MODIFIER_SINGLE_CITY_ADJUST_TOURISM`现有用例多过滤作品/奇观/改良；本轮限定查询未找到只有ScalingFactor的先例。**“整城全部旅游”与L1区域固定加值、M作品原生倍率是三个接口，证据不得互换。** 不擅自改只加作品旅游或给固定点数。

模块own当前unit/session/任务队列及derived effects；成功完成删除当前任务，保留唯一永久成果。source失城明确退出当前effects，永久原Owner记录保留；return从相同记录和当前事实重建。UI只读current confirmed状态/意图，不发奖，不保存唯一权威。

N2最小实机流程在原型就绪时固定：一个有GW/Wonder的外国首都，来源Culture4训练一团，完成一种任务→source降级仍执行下一任务但本地旅游暂停→冷加载记录/任务继续；战争或目标失效只补本地不能回答的关键路径。不让用户现在重造该fixture或测试所有专业。

## N3：Culture Network独立payload与精确旧Eureka退出

前提：N2可靠source ledger及completed-civ集合，现有domestic route/资格view，专业接收专家事实。共同topology和首都/中心规则仍来自[共同Network设计](../../Design/Network.md)，不另加对外商路。

`S_receiver = union(S_source for valid connected Culture ACTIVE4 sources)`。
`Culture_per_matching_working_specialist = network_culture_K × |S_receiver|`，K=1为初版值。

- 每来源先独立3/3；一个来源2类、另一个1类**不能拼成完整文明**。重复文明只算一次，不sum counts、不取max source。
- 接收只作用于该城单一Identity对应实际工作的专家；无Identity没有受益专家，不是本城所有专家。接收不授见闻，不作为新source二次出口；授权Trade Center分发属于共同topology，不是成果转移。
- source降级/loss、真实商路/中心失效、receiver资格/专家变化、source可靠成功记录变化分别触发，只按受影响来源/接收者更新。未知路线按既有桥确认/withdrawal合同，不拿空包当disconnect。
- 现有`NetworkBridge.CurrentRecipientSources`可提供已确认source列表，typed payload单独计算。当前bridge signature没有见闻版本，publication没有新Culture consumer；**无商路变化时source新成功也必须触发payload更新**，不能只等路线signature改变。拓扑/ledger/receiver worker三个输入版本保持各自职责。

当前`NetworkBoost`仍同时生成RESEARCH/CULTURE旧`k×L×sqrt(N)`整数Boost，carrier在首都。N3才退休Culture部分：精确Culture legacy/integer/test owned IDs、SQL附件、生成/Audit/test入口及HD Property/后台Boost writer全部核对；Research Inspiration公式和目前效果保留。**没有源码存在＝全部旧输出已审清的声明**，实施前须按完整exact ID搜索所有Mod调用点。

退休还要拆开共享TEST入口，否则旧testRaw为两种Boost写值会复活Culture Eureka。旧清理ID可惰性保留；新Culture consumer不能与旧Eureka同时出效，不先停整个NetworkBoost导致Research也退出。

N3本地重点：A/B来源各自partial不合并；完整相同文明去重/不同文明union；center授权路径及首都自接入；source ACTIVE/ownership/route确认撤销；matching worker same-turn变化；重复零写、load旧carrier清理、Research不回归。集合模型主要本地验，不要求用户重复三类×多国大量任务；native只用已就绪source/receiver最小一个商路变化验证。

## 风险、回滚与退出

N1以W0004 L2交互验证为主；N2/N3涉及持久状态/网络，按L3运行**相关**回归与失败恢复，不默认全历史stress或内存长测。普通计算仅用owned数/完整集合，详细文明清单按需；任务集合按活unit/目标维护，退出不累积通知历史，不复制全国事实采集、不新增GC。

N1 rollback为可撤销probe/对应包；N2新增ledger回退不得删永久记录，先确定schema保留/存档副本支持边界；N3关闭新owned效果并恢复上一独立Network包，保留N2成果，不用清账本恢复旧系统。

Exit：每子批独立本地/最小native gate通过，才对其范围标PASS。N1不证明N2；N2整城旅游不证明N3。K_T待平衡、战争部署/整体旅游/外国目标采集/source确认均未关闭；当前不要求用户决定，不进入任何实施。

来源：[正式Culture](../../Design/Content/Culture_D0029.json)、[Spec Culture/network覆盖](../../Design/Specialization_v0.1_Design_Spec.md#6-culture--theater-square--cul)、[Network基础](Batch_B_Shared_Network.md)、[生命周期](Batch_C1_Discount_Lifecycle.md)、[技术spike](D0032_Technical_Spikes.md)、[E2现有保存](P0_E2_Plan.md#current-slice--recovery-and-action-routing)。
