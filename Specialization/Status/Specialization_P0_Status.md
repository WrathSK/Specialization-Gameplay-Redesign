# Specialization P0 Status

Document Owner: Codex
Status Revision: S0317
Implementation Build: develop P0-B-123.150 / modinfo150 SELECTION_CONFIRMATION; live B123.150 verified166/166 MATCH; stable B069.96
Architecture Revision Reviewed: A0161
Design Revision Reviewed: D0035 (scoped Shared/Lv2; A0161 target remains D0032)
Latest Accepted Design Revision: D0035
Design Sync State: TARGET_ARCHITECTURE_ADAPTED_RUNTIME_PARTIAL
Work State: B123_SCOPED_NATIVE_PASS; E2 Claim plan-only

## CURRENT AUTHORITATIVE STATE

[B123原生项目限定验收通过](Validation/Results/Specialization_B123_Project_Pass.md)：用户明确确认三处1T、正常过回合完成、后续无溢出，并补测砍树不提前完成、不流入后续目标。本次是用户文字证据，无新截图；PT012关闭。112项LOCAL测试与原生证据分开，未扩大到所有收获/注入/强制完成组合。

“处理其它待办”属于旧空队列过回合实验，不是当前真实项目方案的前置要求。可以用本原型继续规划真实1-turn项目；当前仍单活动城/会话级，无正式奖励，读档不续算。Claim专属资格、Identity/P1永久提交、重复/失效退出、多城与保存边界仍需实施和验证。

[一回合Claim计划](../Architecture/v2/P0_E2_Plan.md#next-slice--one-turn-claim-plan-after-b123)已按用户授权准备，替代未实施的Cost=1提案。包含冻结候选、真实完成才写Identity/P1、多城独立、持久计时/读档续算、改选重开、精确入口退出与一次联合实机验证。仅计划待审核，尚未授权Claim实施；不进入F。

源码/live仍B123.150，source 5868061；此前receipt B123.150-5868061-playtest.json记录166/166 MATCH，本轮无重新部署/运行包核验。main/stable B069.96与Design不变。

## 历史阶段记录

以下保留原阶段用语与证据；其中“当前／下一步／待测”仅描述当时。有效技术限制通过当前E2切片的合同/证据路由继续可达，不因进度过时而作废。

2026-09-26 [B107后剩余E2计划](../Architecture/v2/P0_E2_Plan.md#post-b107--remaining-e2-plan--new-path-isolation-over-migration-compatibility)已整理，仅计划、未实施。旧迁移＋新城混合实机检查退出必做队列，本地兼容回归保留；最终验收改为新体系多城隔离＋一次冷加载（含P0对照）。下一建议：新测试局全城进度authority/旧writer cutover，处理2城/32城实验限制和重复绑定快照/整集合复制边界；之后首次AI征服snapshot、Claim、剩余生命周期、E2结项/F门禁。新档优先为下一批推荐支持合同，未改当前B107旧档行为。无新Design/源码/部署，无立即测试；等待下一段明确实施授权。

2026-09-26 B107.134 [新城登记实机证据](Validation/Results/Specialization_B107_E2_Fresh_Registration_Pass.md)：3图确认同一城0/65536正常建城自动登记1/2、NONE/P0/ACTIVE0/KNOWN、随后RESEARCH/P1/ACTIVE1；用户明确确认重启后P2保留。简化新局单城路径 USER_GAME_TEST_PASS；P2读档为用户陈述，不伪称截图显示投资1/ACTIVE2。旧迁移城＋新城混合对照按对话暂列待办；P0独立冷加载未单独确认，不能仅凭两图时间判断。相关失败/重复保护仍为本地证据。原图3/3 hash一致归档；无runtime/Design/main/部署变化，无需立即重复测试，E2仍partial，不自动进入Claim/F。以下历史。

B107.134：[获授权新城登记实现](../Architecture/v2/P0_E2_Plan.md#b107134--authorized-positive-founding-registration-implementation)完成定向L3 LOCAL_SIMULATION_PASS，等待USER_GAME_TEST。自动FOUND_CITY＋Initialized证据→独立Game NONE/P0→首个合格完成P1→现有投资P2；目标旧writer受guard，既有B103/B104回归通过。内层schema2与旧schema1混合；两记录上限保持，未定义的未专业化夺回仍暂停。无新收益公式/carrier/Design/Claim/F；不扩大native PASS。最小测试为一个控制城＋新自建城，P0和P2各一次冷启动读档。回滚B106必须配建城前旧存档。已按W0003部署：实现commit c5bb3d9，部署HEAD d6e5ed0，153/153 MATCH，receipt B107.134-d6e5ed0-playtest.json；B106完整恢复点/stable桥已核验，游戏退出，main未改。以下历史。

[Post-B106新城登记计划](../Architecture/v2/P0_E2_Plan.md#post-b106-plan--positive-founding-evidence--fresh-registration)已完成，待实施授权。以已验证Gameplay FOUND_CITY＋当前城/Initialized匹配替代旧Publish收尾假设；自动采集不需手动arm，绑定前阻止目标旧writer，显式NONE/P0及首次完成Game权威；保留两记录测试上限与B103/B104路径。计划提出内层schema2新城记录、旧内层schema1原样兼容，不承诺旧包读取新档。最小一次流程含未专业化/已投资两处冷加载。无新Design问题；仅文档，B106运行包/main未改、未部署。以下历史。

B106两图：[FOUND_CITY原生验证](Validation/Results/Specialization_B106_E2_Found_City_Pass.md) USER_GAME_TEST_PASS（限定本次自建＋转移对照）。Gameplay枚举可用；自建Initialized后收到FoundCity，Owner0/单位1114117匹配起始移民，随后Publish/Playback；转移Owner0→2收到Transfer、未见FoundCity。最小采集门禁关闭，无需重复；不是自动登记已实现或所有城市生命周期PASS。下一步收窄新城登记计划，去除手动arm依赖，处理正面建城证据/当前城匹配及早到区域完成；不复用首个Publish假设。B103/B104范围内验收保持，无runtime/Design/main/部署变化。以下历史。

B106.133：[获授权FOUND_CITY采集检查点](../Architecture/v2/P0_E2_Plan.md#b106133--authorized-found_city-evidence-checkpoint)本地完成。仅现有有界观察器新增Gameplay UnitActivate原因/起始移民ID，明确枚举或监听缺失，不依赖回调时移民仍存在。针对性模拟/实际请求入口/Lua语法及既有B104/E2回归PASS；非原生建城证据PASS。待一例普通建城＋一例交易负对照；入口不变，缺监听/枚举则截图暂停。新城登记/Claim/F仍未开启，无永久状态/收益写入或Design变化。已按W0003部署source14b0681，153/153 MATCH，receipt B106.133-14b0681-playtest.json；B105恢复点/stable桥/游戏退出核验通过，main未改。以下历史。

[其它Mod事件处理调查](../Reports/Technical/Specialization_E2_Other_Mod_City_Lifecycle_References.md)：找到AutoPlay及原版UI采用UnitActivate/FOUND_CITY作为正面建城信号；GCO采用关联事件，HD采用征服缓存，Captive Leaders对已知pending操作回合核对。均STATIC_CONFIRMED，非本项目原生账本PASS。下一建议最小采集该建城信号及转移负对照，先确认Gameplay送达；不再依赖首个Publish，没有实施或新测试要求。B105新城自动登记门禁保持；以下为此前结果。

B105四图已归档：[原生事件顺序结果](Validation/Results/Specialization_B105_E2_Event_Boundary.md)。自建与转移均出现 Built→Publish→后续Added/Initialized；转移更明确为早到Publish→Removed/Added/Initialized→Transfer→Publish→Playback，早到快照已是新Owner。事件采集所测路径 USER_GAME_TEST_PASS；“首个Publish就是完整事务结束”被实机反证，EVENT_BATCH_BOUNDARY仍阻止新城自动登记。无ReadRequest干扰标记、无缺页/采集错误；不要求重复这两组。下一步仅收窄边界方案：正面转移完成证据＋新建来源/更强收尾依据；不以等待时长/Publish次数猜测。B103/B104验收保留，无runtime/Design/main/部署变化。以下为历史记录。

B105.132：[已授权事件批次证据检查点](../Architecture/v2/P0_E2_Plan.md#b105132--authorized-event-batch-evidence-checkpoint)完成。按计划EVENT_BATCH_BOUNDARY门禁，先用手动单位置/48条上限记录Gameplay事件与首个Publish/Playback；不假定批次原子性，不接管新城/写新保存schema。右键移民/施工队开始，右键E2往返读取翻页；旧左键保留。定向模拟、实际UI/Gameplay请求及B104→B103/E2相关回归PASS；非原生边界PASS。最小待测：一例自建＋一例交易事件序列，无需迁移/投资/读档重测。B103/B104已验收保持；新城NONE/P0接管与首次完成部分尚未实现，等待该门禁证据；不进入Claim/F。已按W0003部署source 29508c7；153/153 MATCH；receipt B105.132-29508c7-playtest.json；B104恢复点与stable桥核验保留，退出进程检查通过。Design/main未改。以下为历史计划/验收。

新自建城登记计划已按用户要求修订为“关联事件收集→明确转移完成／已验证批次收尾→局部分类”，仍PLAN_ONLY，未授权实施。PublishComplete为有原版依据的候选收尾点，尚非Gameplay转移原子边界实机保证；跨批次/未知不误判新建或摧毁。保留B103/B104夺回路径，补旧writer提前写入防护及早到区域完成通知处理，零pending立即返回。仅计划/导航更新；D0035、B104源码/运行包/main不变。等待修订计划实施授权；以下为此前记录。

[下一最小段：新自建城登记计划](../Architecture/v2/P0_E2_Plan.md#next-slice--new-self-founded-city-registration-plan-only)已提出，待用户明确实施授权。保留两记录测试上限，用独立测试档一座旧城+一座新城；先验证真正自建来源（CityBuilt不能单独作证），再接管NONE/P0→首次有效区域完成P1→投资→保存。来源不足则技术暂停，不猜测征服/Claim。W0004 L3仅相关持久化/完成顺序回归；无runtime/Design/部署变化，B104验收仍有效。

[B104双城验收](Validation/Results/Specialization_B104_E2_Two_City_Pass.md)：五图确认工业城131073由P3/ACTIVE3/投资2→P4/ACTIVE4/投资3，科研城327682仍P2/ACTIVE1/投资1；第二城迁移为独立Game记录。用户另确认重新启动读档后记录保持。本次双城登记/投资隔离/读取及保存恢复 USER_GAME_TEST_PASS（仅所测科研+工业场景），原图5/5 hash核验归档。B104最小实机门禁关闭，无需重复；E2仍partial，非所有权双城/非零路线/全专业完整验收。下一建议先审新自建城登记计划，未授权实施；不进入Claim/F。本轮仅证据/导航，无runtime/Design/部署变化。以下实现与待验文字均为历史记录。

B104.131：[获授权双城隔离实现](../Architecture/v2/P0_E2_Plan.md#b104131--authorized-two-existing-city-persistence-slice)本地完成。相同Game key的schema2集合，最多两城显式登记；B103单城无写读取适配、首次真实写入升级，旧内容保留。每城投资/退出重试/转移证据独立，诊断实际跟随所选己方城；第三城仍旧路径。定向L3 LOCAL_SIMULATION_PASS（非实机PASS），无新能力/Claim/F/Design变化。已按W0003部署source bfe7003，152/152 MATCH；receipt B104.131-bfe7003-playtest.json；B103完整恢复点及stable桥核验保留，游戏进程退出确认，main未改。等待一次两城投资+冷加载验证。回滚须B103包及转换前存档，不直接降级继续读schema2存档。以下为历史计划/验收。

[E2当前盘点及后续切片计划](../Architecture/v2/P0_E2_Plan.md#2026-09-25--e2-inventory-and-next-slice-proposal-not-authorized)已整理，仅计划。B103单城夺回/冷加载PASS保持；新后端仍singleton，其它城旧路径。建议下一最小批：两座完整已有专业城显式登记与保存隔离（含B103旧记录无损适配），不自动全城迁移/新cityKey，不混入首次AI城snapshot/Claim/F。之后另审新自建城、征服snapshot、Claim入口及E2支持范围收束。无新Gameplay决策阻塞两城切片，等待用户实施授权；本轮runtime/Design/部署不变。

2026-09-25 [B103三图验收](Validation/Results/Specialization_B103_E2_Recapture_Pass.md)：原Owner科研城夺回ACCEPTED；原0/262146→外方3/131073→当前0/327682，同记录rev4，token缺失仍由转移证明确认；RESEARCH/P2/投资1保留，ACTIVE1/KNOWN。用户确认第三图为保存冷启动读档后，且派遣总督后1/2级能力正常。单城夺回/永久进度/读档及所述能力恢复USER_GAME_TEST_PASS。Network当前引用MATCHED、routes0，仅确认无路线视图，不扩大到有路线收益或四专业全覆盖。成功后的退出0/23是会话计数重置，不是失败；旧23/23证据保留。截图3/3 hash归档。E2仍partial，Claim/F未授权，旧游戏内载入崩溃独立保留；本轮仅文档，无runtime/部署变化。无需重复本次测试，等待下一最小段计划授权。下方为历史实现/待验记录。

B103.130：[读档初始化修复](../Architecture/v2/P0_E2_Plan.md#b103130--authorized-foreign-load-hydration-repair)已获授权。仅忽略转移开始前精确匹配已保存外方引用的加入/初始化；不清除既有错误，真实乱序/冲突继续拒绝。新增固定单条首次拒绝证据。四专业、读档/重复初始化/截图征服顺序、接受后冷加载及既有E2退出/投资/恢复定向L3 LOCAL_SIMULATION_PASS，非实机PASS。无Claim/F/Design变化；已按W0003部署source e238584，152/152 MATCH；receipt B103.130-e238584-playtest.json，B102完整恢复点及stable桥保留。只读进程确认退出，未启动游戏/main未改。等待最小原生复核：现有外方持城档冷启动→夺回→E2/专业报告，接受后另存冷加载；无需重做交易/迁移。以下B102为历史失败证据。

2026-09-25 [B102两图与本地复现](Validation/Results/Specialization_B102_E2_Chain_Order.md)：本次最新CityBuilt/征服/移除/加入/初始化/转移顺序正确，仍RETURN_CHAIN_ORDER、退出23/23。实际代码可复现“读档外方CityAdded先到→错误锁存→之后合法链被拒绝”；原生最早触发通知未保留，不把推断当完整trace。缺少加载对象与转移阶段区分，待窄修复；永久P2/投资1保留，ACTIVE/Network/接受后保存仍未验证。无需再重复当前测试，本轮只调查/归档/文档，无源码或部署变化。

B102.129：获授权[CityBuilt/征服判定修复](../Architecture/v2/P0_E2_Plan.md#b102129--authorized-conquest--citybuilt-classification-repair)。CityBuilt不再独自决定新建；须严格匹配同回合征服旧/新Owner、新ID/位置及完整转移链才可接受。缺佐证/冲突/真正新建仍暂停；version2证明持久化，原记录及当前ACTIVE/Network规则不变。定向L3 LOCAL_SIMULATION_PASS、原生待验；无Claim/Design改动。只读进程复核游戏退出后按W0003部署source39fa0a9，152/152 MATCH，receipt B102.129-39fa0a9-playtest.json；B101完整恢复点及stable桥保留，main未改。最小测试仍为原外方持城档冷启动→夺回→E2/专业报告，接受后另存并冷启动复核；不重做交易/迁移。

2026-09-25 [B101两图失败定位](Validation/Results/Specialization_B101_E2_Foundation_Guard.md)：退出23/23，实际阻断RETURN_NEW_FOUNDATION；新观察到GameEvents.CityConquered(0,3,327682,28,34)后接移除/加入/初始化/转移。B101把同坐标CityBuilt无条件视为新建的保护过粗，导致该征服场景拒绝；并非此前22/23阻断。CityBuilt精确时序/来源未直接记录，不归因HD。永久记录保留，ACTIVE/Network/接受后读档未验；不必重测交易前退出。建议另授权最小事件分类修复，保留真实新建拒绝，不进入Claim/F。本轮仅证据/文档，无runtime/部署变化。

B101.128：获授权[单城原Owner转移链适配](../Architecture/v2/P0_E2_Plan.md#b101128--authorized-original-owner-native-transition-adaptation)，使用已保存外方引用+本次实际移除/加入/初始化/转移链，允许token缺失但拒绝冲突；确认结果保存在原Game记录，无token补写/Claim/new cityKey。ACTIVE/Network仍按当前事实重算。定向L3 LOCAL_SIMULATION_PASS，native待验；旧B100回滚必须搭配接受新证明之前的存档。用户已确认退出且只读进程复核通过；已按W0003部署source5699c84，152/152 MATCH，receipt B101.128-5699c84-playtest.json；B100完整恢复点及stable桥保留，main未改。最小验证：原外方持城档冷启动→夺回→E2往返/专业报告→另存后冷启动复核；不重迁移、不进入Claim/F。

2026-09-25 [B100夺回阻断确认](Validation/Results/Specialization_B100_E2_Recapture_Token.md)：旧3/131073移除→新0/327682加入/初始化→CityTransfered匹配；候选已到达，token nil导致RETURN_IDENTITY_UNCONFIRMED。永久RESEARCH/P2/投资1及rev3保留；非事件未达。TARGET_UNAVAILABLE指旧外方退出对象已变化，23/23仍完成。B097原生夺回本次FAIL，ACTIVE/Network重建未验；建议另审基于已保存引用+严格转移链的最小适配，不复制token、不进入Claim/F。发现B100征服观察namespace与E1不同，缺行不代表GameEvents未触发。本轮只证据记录，游戏运行中、不改代码/部署；无需重复当前测试。

2026-09-25 [B100首图](Validation/Results/Specialization_B100_E2_Foreign_Baseline.md)：当前仍3/131073外方持有，STILL_FOREIGN、token MISSING、退出23/23、永久P2/投资1保留；Network跨Owner引用已正确排除。仅诊断可见字段实机通过，未观察夺回事件；待征服后重新点击E2往返。游戏运行中，本轮只归档/记录，无部署。

B100.127：获授权补齐[定域诊断](../Architecture/v2/P0_E2_Plan.md#b100127--authorized-bounded-ownership-diagnostics)。五类事件各保留最后一次标量参数；显示binding匹配、恢复拒绝及退出失败模块；Network当前引用严格核对Owner/完整reference。无新恢复权限、无token补写/Claim/Design变化。定向诊断与既有E2投资/退出/夺回回归LOCAL_SIMULATION_PASS；native事件仍待验证。已按W0003部署：source8417ee1、152/152 MATCH、receipt B100.127-8417ee1-playtest.json；B099完整恢复点与stable桥保留，游戏未启动。最小测试：冷启动现有外方持城存档，夺回后立即读E2往返；无需重做迁移/交易。不把本批当作夺回修复完成。

2026-09-25 [B099冷启动与征服取回](Validation/Results/Specialization_B099_E2_Coldload_Recapture.md)：用户确认首图在征服前、次图在征服后。冷启动成功载入、RESEARCH/P2/投资1及HELD记录保留；退出检查23/23，旧Network成员false。征服后专业读取PROGRESSION_HELD，夺回恢复本次FAIL；未取得夺回后的token/事件拒绝详情，不把token缺失候选当已证实原因。ACTIVE/Network重建仍未验证，Claim/F保持关闭。此前游戏内读档崩溃独立保留。仅证据/状态更新，无runtime/Design/部署变化。

2026-09-25 [B099六图与读档崩溃](Validation/Results/Specialization_B099_E2_Transfer_Crash.md)：基本诊断回复实机PASS，交易后永久RESEARCH/P2/投资1保留、HELD_TRANSFER；当前token=nil，退出22/23 PARTIAL_HELD，科研carrier0/旧Network成员false。游戏内载入时SIGSEGV，save/load本次FAIL，原因未知；非冷启动，夺回未测。发现Network诊断跨Owner同ID错误引用，不代表旧snapshot重放。停止当前往返，保留证据，不进入Claim/F；本轮无源码/部署变化。

B099.126 已按授权修复人类资格读取及静默诊断拒绝；使用Player.IsHuman，不假定player0。定向资格/实际诊断入口与E2保存、退出、夺回回归LOCAL_SIMULATION_PASS，非实机PASS。永久状态/Design不改；用户已确认退出，已通过既有transaction工具部署，152/152 MATCH；source `1dc2ca4`，receipt `B099.126-1dc2ca4-playtest.json`；B098完整恢复包及stable恢复桥保留，main未改。先验收基本读数/收益，再恢复E2往返，不重复迁移。见[E2修复记录](../Architecture/v2/P0_E2_Plan.md#b099126--authorized-eligibility-regression-repair)。

B098.125 实机诊断入口失败：[三图调查](Validation/Results/Specialization_B098_E2_Read_Failure.md)。专业/潜力、总督、专家报告停在READING；用户报告能力失效。152/152部署一致。B095新增全局人类资格检查是主要回归候选，尚无native API返回值确认。先暂停ownership往返测试，修复基本入口后再恢复；永久记录未证明丢失。本轮仅调查归档，无源码/部署变化。

B098.125 已按授权临时部署：source `0927183`，152/152 MATCH；既有B094.121完整恢复包151/151核验保留，stable/main不变。receipt `B098.125-0927183-playtest.json`（既有外部SpecializationDeploymentBackups目录）。未启动游戏，native各项仍待用户回传。

B098.125：用户接受B097并授权最小native round-trip验证与必要测试部署；新增“E2往返”按需报告，不改B096/B097恢复规则。真实报告零写及相关生命周期回归LOCAL_SIMULATION_PASS；实机withdrawal/recapture/ACTIVE/Network/save-load均PENDING_USER_GAME_TEST。按[单城流程](../Architecture/v2/P0_E2_Plan.md#b098125--单城-native-ownership-round-trip-validation)由用户测试；不进入Claim/全城迁移/F。部署事务完成情况另记，下方旧“不部署”为历史批次约束。

B097.124：授权的原玩家单城夺回路径已实现，原token+已保存loss+匹配事件确认，永久进度引用适配、工业模板Game保存、当前ACTIVE/Network重新派生；缺失工业历史只hold模板。定向L3 LOCAL_SIMULATION_PASS；原生token/事件/实际carrier闭环尚未验证。详见[P0-E2最新检查点](../Architecture/v2/P0_E2_Plan.md#b097124--原玩家同城夺回-partial-checkpoint)。仍partial、不部署；无snapshot/Claim/全城迁移/F；live B094.121/main/Design保持不变。以下为历史checkpoint。

B096.123：已授权补齐单城confirmed ownership-loss模块自有退出，21组明确载体+Network旧view+两plot flags；UNKNOWN不清、重复幂等、永久记录保留。定向L3及同Owner回归LOCAL_SIMULATION_PASS，原生效果撤销尚未实机验证。详见[P0-E2最新检查点](../Architecture/v2/P0_E2_Plan.md#b096123--confirmed-ownership-loss-scoped-exit-checkpoint)。仍E2 partial，不部署、不实现夺回/Claim/F；以下B095退出阻塞为历史状态。

[P0-E2 B095.122 partial检查点](../Architecture/v2/P0_E2_Plan.md#b095122--首段实施检查点未完成不部署)：用户已授权四专业单城同Owner保存首段；新Game进度路由、旧writer隔离、投资/读档与诊断已实现并通过定向LOCAL_SIMULATION_PASS，非实机PASS。四专业开放范围不变，未来领域仅保留扩展能力。确认退出的carrier覆盖未完成：自动审批拒绝前缀批量删除；只读确认ResearchApply/Cross/Chair的AI-owner过滤会跳过旧载体处理。未采用被拒绝方案，不部署，不进入F/Claim/夺回实施；须完成逐模块、单城明确退出及相应回归后再交付测试。运行包保持B094.121；main/Design不变。以下“待授权”记录属于此前历史。

E2范围已按用户澄清收窄：[单人/仅玩家与所有权路径](../Architecture/v2/P0_E2_Plan.md#当前单人范围澄清用户确认2026-09-21)。AI/自由城持有时全部效果休眠、不投资；原城夺回沿用PROG-004恢复，首次征服无历史AI城沿用PROG-006～009 snapshot/Claim分流，二者不是未决Design。首段同Owner保存切换范围不变；后续处理失城/夺回及独立征服初始化，无AI/多人实施依赖。当前IsTestPlayer未检查Human门槛及旧carrier退出需实现时核对，不能仅靠不跑AI Audit保证无效果。本轮仅计划/索引，无runtime/Design/部署变化。

[E2具体计划](../Architecture/v2/P0_E2_Plan.md)已完成：建议先对一座原Owner/旧凭据完整的已专业化城市切换Game进度保存与既有移民投资；逐入口关闭目标旧writer，保留其它城旧路径。新城/跨Owner/专业Legacy/全量兼容不纳入首段，不自动进入F。E1只认定单次自由城持久映射原型PASS。当前仅计划，等待scope审阅与实施授权；无runtime/Design/部署变化，无用户测试。

[B094单城持久映射验收](Validation/Results/Specialization_B094_P0E1_Mapping_Pass.md)：读档后已保存映射恢复、Owner0→62、修订3、对象一致，USER_GAME_TEST_PASS（单城自由城市实验范围）。B093暂停本次未复现；不扩大为全路径永久身份或正式迁移。截图hash归档，无需重测。下一步建议收束E1支持范围并提出E2具体计划，未授权E2/F实施。旧Tooltip文案遗留登记；本轮runtime/Design/main不变，无部署。以下等待本次测试内容为历史。

[B094.121修复](../Architecture/v2/P0_E1_Persistent_Mapping_Plan.md#b094121--授权事件入口修复)已授权完成：直接varargs传参，未启用提前跳过，错误显示阶段。缺失unpack环境及原映射回归LOCAL_SIMULATION_PASS，原生闭环待验收。schema/判断/专业账本不改，不进入E2/F；已按W0003部署，151/151一致，B093/stable恢复点核验。

[B093实机暂停](Validation/Results/Specialization_B093_P0E1_Paused_Review.md)：function expected instead of nil，USER_GAME_TEST_FAIL（本次闭环阻断）。新事件入口table.unpack缺失的故障注入可复现未启用即锁存错误；原生具体调用点尚未确认，不归因为未选城。截图hash归档，建议移除该依赖并加简短阶段诊断，尚未修复/部署，不要求重复测试，不进入E2/F。旧B090/B092局部证据保留。

[B093.120单城持久映射](../Architecture/v2/P0_E1_Persistent_Mapping_Plan.md#b093120-实施记录)已授权实现，定向L3 LOCAL_SIMULATION_PASS：事件自动保存、冷加载恢复监听、10k重复零重复写、冲突/失败暂停。仅新实验key；不迁移专业、不改收益/Design，不进入E2/F。等待一次“转移后先保存读档、再左键对照”的原生验证；不沿用B092作为新闭环PASS。W0003已部署，151/151一致，B092/stable恢复点核验；未启动游戏。以下计划等待授权文字为历史。

[E1单城持久映射计划](../Architecture/v2/P0_E1_Persistent_Mapping_Plan.md)已完成：独立Game实验key、事件驱动保存、冷加载核对，保留单次自由城范围，旧账本/writer不切换。仅计划，待单独实施授权；无runtime/Design/部署变化。当前无需用户测试，不自动进入E2/F。

[B092四图配对验收](Validation/Results/Specialization_B092_P0E1_Shadow_Review.md)：T8 0/131073→62/65536，Gameplay直接收到6条事件并给出SHADOW_CANDIDATE，UI两条转移事件独立吻合。单次自由城转移shadow USER_GAME_TEST_PASS；旧保存HELD是独立getter结论，不是实验暂停。不需要为本路径新建UI桥；不扩大为完整E1/永久身份/正式迁移通过。截图4/4 hash归档，无需重复。下一步建议审阅E1支持边界与持久映射计划；本轮不实施、不部署、不进入E2/F。以下等待截图文字为历史。

B092.119：获授权实现[事件配对shadow及Gameplay事件诊断](../Architecture/v2/P0_E1_Game_Record_Experiment.md#b092119--authorized-event-shadow-implementation)。定向LOCAL_SIMULATION_PASS，等待一次原路径Gameplay左键截图；shadow不写入、不认领、不迁移，旧保存状态与预演分离。旧账本/Design/收益/UI未改，不进入E2/F。

[B091补充前后证据](Validation/Results/Specialization_B091_P0E1_Transfer_Chain_Review.md)：0/131073→62/65536，捕获CulturalIdentityCityConverted(62,65536,0,24576)及CityTransfered(62,65536,0,-738490196)。结合原版fromPlayer用法，该路径UI旧Owner佐证已确认；不再要求重复同一UI测试。研究建议按明确转移事件+保存旧引用建立shadow候选，先确认Gameplay同事件证据；未实施resolver更改，不迁移账本，E1整体仍HELD、不进入E2/F。runtime/main未改、无部署。

[B091两图UI复核](Validation/Results/Specialization_B091_P0E1_UI_Getters_Review.md)：四个UI接口均返回number（0/62/-1/-738490196），本场景读取USER_GAME_TEST_PASS。OwnerBeforeOccupation=62不是旧Owner0；不能据此映射。两图均为当前62/65536、UI事件0，未证明转移前监听已启用，不判断事件不存在。身份门禁仍HELD，无迁移/E2/F。截图已hash归档，runtime/main不改，无部署。

B091.118：获授权补充[按需UI易主证据](../Architecture/v2/P0_E1_Game_Record_Experiment.md#b091118--authorized-ui-transfer-evidence-supplement)，实验对照右键读取UI接口并观察固定8条相关事件；左键原保存核对保留。定向LOCAL_SIMULATION_PASS，等待转移前后两张UI截图；不修改认领规则/旧账本/收益，E1身份门禁仍HELD，不进入E2/F。

[B090三图实机复核](Validation/Results/Specialization_B090_P0E1_Game_Record_Review.md)：启动修复与独立Game实验记录在分城转自由城/读档场景USER_GAME_TEST_PASS；修订2及保存事件5保留，本次事件归零。OriginalOwner=0，其余三getter UNKNOWN，故身份配对仍HELD（不是实验暂停）。不扩大为正式继承/账本迁移PASS，不重复本次测试；下一步仅建议调查缺失的转移佐证，不进入E2/F。截图已hash归档，runtime/main不改，无部署。

B090.117：已授权修复[实验初始化/错误提示](../Architecture/v2/P0_E1_Game_Record_Experiment.md#b090117-authorized-startup-fix)。按需一次初始化，不依赖加载事件必达；可恢复入口拒绝不锁死，损坏记录/写入失败继续停止。定向LOCAL_SIMULATION_PASS，原生USER_GAME_TEST_REQUIRED；不改旧账本/收益/Design，不进入E2/F。下方B089入口失败为历史实机证据。

[B089两图复核](Validation/Results/Specialization_B089_P0E1_Start_Blocked.md)：己方分城选择与旧只读核对成功，新实验在入口组合断言处暂停，USER_GAME_TEST_FAIL（启动入口）。尚未测试新Game记录保存/易主/读档；最可疑为加载ready门禁但单项原因未被诊断暴露。截图已hash归档；本轮不改runtime/不部署，不要求重复原测试。E1仍HELD，不进入E2/F。

B089.116：用户明确授权的[单城Game记录补充实验](../Architecture/v2/P0_E1_Game_Record_Experiment.md)已完成LOCAL_SIMULATION_PASS（定向Lua模拟，不是原生PASS）。只写新的独立测试key；旧专业账本、收益、Design及隔离继承模块不改。加载恢复/易主getter仍USER_GAME_TEST_REQUIRED；E1整体门禁仍HELD，停止等待该页三步最小测试，不进入E2/F。下方B088“持久实验另审”等为前一阶段记录，已被本次窄授权补充。

[B088 E1三图实机复核](Validation/Results/Specialization_B088_P0E1_Native_Review.md)：首都测试1/2支持原范围读档后记录可核对；分城测试3转自由城市0/131073→62/65536时五项旧City记录均原有现无，正确UNKNOWN并停止认领。诊断保护行为USER_GAME_TEST_PASS（本例），永久城市连续性门禁仍TECHNICAL_INVESTIGATION_REQUIRED；不拼接两城证据，不进入E2/F。三原图已hash归档；无需用户立即补测。下一步仅建议调查原Game账本/转移事件可靠映射，任何持久实验另审。本轮仅证据/Status更新，runtime/main/部署不变。

P0-E1已获授权并完成只读实现：[B088.115证据/迁移预演](../Architecture/v2/P0_E1_Identity_Evidence.md)。LOCAL_SIMULATION_PASS（实际Lua/事件模型，不是Civ VI实机证明）；原Owner结构匹配仅候选，所有migrationAllowed=false。32条事件环、30k通知无读取/写入；完整前序回归通过。旧writer/Design/收益SQL/main不变，未迁移存档。原生跨Owner/冷load连续性TECHNICAL_INVESTIGATION_REQUIRED；E1整体未PASS，不进入E2/F。[W0003部署完成](Validation/Results/Specialization_B088_P0E1_Deployment.md)：148文件逐项一致，B087/stable完整恢复点核验，无启动游戏。以下旧计划阶段叙述为历史。

U1前置原型技术USER_GAME_TEST_PASS：[四图归档/验收](Validation/Results/Specialization_B087_U1_User_Pass.md)。布局、文字、其它surface和完整U1后置。回到D3后的[P0-E1城市身份保存门禁计划](../Architecture/v2/P0_E1_Plan.md)，仅计划未授权实施。B087.114源码/运行包、Design/main不变，无部署；下方旧等待U1验收状态为历史。

[U1展示原型B087.114](../Architecture/v2/U1_Presentation_Prototype.md)获授权并本地完成：科研累计机构、阶段文字、城市详情carrier显示过滤，完整U1未实施。147文件，前序收益回归/新显示生命周期/10k重复通知/部署保护通过LOCAL_SIMULATION_PASS；实际HD加载与显示待用户短测。Design、收益writer/SQL、main不变。W0003部署已完成：[147文件/恢复点核验](Validation/Results/Specialization_B087_U1_Deployment.md)，不启动游戏。以下旧计划状态为历史。

用户澄清U1提前目标仅为institution/ability说明/carrier隐藏的技术与显示验证，非完整U1实施。以[前置原型计划](../Architecture/v2/P0_U1_Plan.md)顶部范围为准：一个Research IV城市、一个主要城市详情surface；四专业铺开与历史机构等留后续。当前仍只计划，无runtime/Design/部署变化。下方较宽U1范围已被本条收窄。

P0-D3用户整体验收PASS：[记录](Validation/Results/Specialization_B086_P0D3_User_Pass.md)。现提前提出[P0-U1计划](../Architecture/v2/P0_U1_Plan.md)：四专业当前累计机构、阶段Tooltip、本Mod技术carrier显示过滤；历史机构等待Historical State，不增加玩法/保存依赖。仅计划，等待实施授权。B086.113/runtime/Design/main不改，无部署。下方等待D3验收措辞为历史。

P0-D3已获授权实施，B086.113：[学术主持合同/证据](../Architecture/v2/P0_D3_Research_Chair.md)。每座合格普通学院建筑+工作科研专家数Science；OWNER scope、非平铺/非专家收益，D不反馈。210配置、实际SQL/Lua生命周期、三consumer共享capture、10k idle和完整前序回归LOCAL_SIMULATION_PASS；不是实机PASS。Design、非目标writer不变。已commit/push并通过W0003退出/恢复/hash门禁部署，143文件一致，B085完整恢复点保留：[部署记录](Validation/Results/Specialization_B086_P0D3_Deployment_20260920.md)；等待用户测试；不进入下一批。下方旧计划状态为历史。

[P0-D2用户整体验收](Validation/Results/Specialization_B085_P0D2_User_Pass.md)已记录；未提供逐项边界证据，不扩大结论。[P0-D3学术主持计划](../Architecture/v2/P0_D3_Plan.md)完成，等待单独实施授权；逐座普通学院建筑收益，不按D加权，不做城市补偿。Runtime/live仍B085.112，main/Design不改，本轮无实施/部署。以下D2等待验收措辞为历史。

P0-D2已授权完成B085.112：[学以致用](../Architecture/v2/P0_D2_Research_Apply.md)。用户确认每名专家先floor，按人数由原生专家收益结算；不是城级平铺。120配置、实际writer生命周期/五产出编码、10k idle、1/2/4/8城共享读取及前序回归LOCAL_SIMULATION_PASS。Design字节不改；目录未审对象明确排除提示，不宣称全环境覆盖。等待一次用户最小实机验收；W0003部署已完成commit/退出/hash门禁，140文件逐项一致，B084恢复包已核验：[部署记录](Validation/Results/Specialization_B085_P0D2_Deployment_20260920.md)。不进入P0-D3。下方旧D2半点门禁/未授权描述均为历史。

[P0-D1用户整体PASS](Validation/Results/Specialization_B084_P0D1_User_Pass.md)已记录；无逐项边界证据，不扩大结论。[P0-D2学以致用计划](../Architecture/v2/P0_D2_Plan.md)已备，等待单独实施授权。专家0.5步长单独验证，不继承D1临时floor。Runtime/live仍B084.111，main/Design不变；本轮无部署。以下待D1验收措辞均为历史。

[B084部署确认](Validation/Results/Specialization_B084_Deployment_20260920.md)：137文件逐项hash一致，B083恢复点已验证。请做一次正式P0-D1最小验收；不再运行三档实验。

[本轮正式实现](../Architecture/v2/P0_D1_Research_Cross_Cutover.md)：用户报告所测区域接口仅整数生效，授权临时汇总后floor；B084.111完成跨学科研究正式写入及8旧科研III/3实验效果退出。本地生命周期、1/2/4/8城、10k空闲、SQL与受保护回归通过；正式能力仍需最小实机验收。Design未改；未来D替代仅登记。不进入P0-D2。以下B083等待精度实验的正文为历史记录。

[B083修正版已部署](Validation/Results/Specialization_B083_Deployment_20260920.md)：131文件逐项hash核对，B082/B081恢复点保留；等待同一短测。

最新B082用户测试未完成：[两图归档/原因/B083修复](Validation/Results/Specialization_B082_Failed_Probe_B083_Fix.md)。Gameplay Members不可用、无城市容器和按钮缺字；尚未施加三档实验收益，不能判定小数接口失败。B083完成局部修复/明确context mock/简明错误，LOCAL_SIMULATION_PASS，原生结果待同一短测。旧正式writer/SQL不改。以下B082部署及本地记录保留历史证据；最新部署记录优先。


B082已按W0003临时部署，131文件逐项hash一致，完整B081恢复包保留：[部署记录](Validation/Results/Specialization_B082_District_Precision_Deployment_20260920.md)。当前仅等待一次原生区域精度测试。

P0-D1仍获授权、未正式cutover。用户新增区域归属要求，备用0.5/1明确指收益步长；50%转换系数不变，量化未启用。B082.109完成[区域原生精度实验](../Architecture/v2/P0_D1_District_Precision_Probe.md)：默认OFF，手动0.3/0.5/1，按需区域/城市原生读数，OFF/load准确撤销；8旧Research人口效果与所有其它正式能力保持。LOCAL_SIMULATION_PASS只证明控制/SQL/隔离/性能合同，区域小数保留待用户实机。不要把实验包称为P0-D1完成。W0003仍有效；部署状态以本页最新部署记录为准，不启动游戏。


P0-C完成B081.108/modinfo108：[科研基础设施实施](../Architecture/v2/P0_C_Research_Infrastructure.md)。用户明确单学院环境，多学院顾虑不再阻塞；四原生专家Science bit承载D，精确退出48旧Research IV百分比/复制effect。Culture/Industry等保持；无Design改动。100配置、真实生命周期/清理/诊断、线性读取/10k idle及完整前序回归LOCAL_SIMULATION_PASS；不是引擎PASS。诊断左键简明摘要、右键学院组成；用户随后回复“Pass”，登记P0-C整体USER_GAME_TEST_PASS（用户实际游戏验收通过）：[验收记录](Validation/Results/Specialization_B081_P0C_User_Pass.md)。未单独报告的边界不升级，等待P0-D1具体计划授权。已按W0003部署，128文件逐项hash一致、B080完整恢复点保留：[部署记录](Validation/Results/Specialization_B081_P0C_Deployment_20260920.md)。main B069.96保持。下一批不启动。

### Historical pre-cutover gate (superseded by user single-Campus clarification)

P0-C已明确授权，完成实施前本地计算/SQL候选验证，**尚未完成正式收益切换**：[TS02门禁证据](../Architecture/v2/P0_C_Primitive_Gate.md)。100组实际shared Lua计算通过，多学院最高D/全部专家和掠夺排除的计算通过；原生载体是否覆盖多个学院实例仍UNKNOWN，不能据mock宣布支持或不支持。已找到带plot参数的外部调用线索，待独立原生验证。旧Research IV两个writer和48载体未关闭，无半迁移。Mod/Design未改，B080.107运行包不变，无部署。诊断易读性要求已持久化。下一步仍是P0-C primitive验证；不重问整个实施授权，不进入下一批。

以下P0-C未授权措辞属于此前计划阶段，由本段取代。

历史D0035 / W0001导航增量：[P0-B2 manifest复核](../Workflow/P0-B2_Revalidation.md)完成，PLANNED_NOT_AUTHORIZED；Shared语义不改II住房/GPP，四专业v0.1范围不扩展至Military。A0161原合同复用，不表示已适配未来军事设计。Runtime/已验收结果不变。

P0-B2已获用户明确授权并完成：B080.107/modinfo107，[实施与本地证据](../Architecture/v2/P0_B2_Lv2_Qualification.md)。仅四专业Lv2住房/GPP资格、UNKNOWN保留与有界刷新；住房仍按Tier存在性，不是D。复用41旧载体，无新收益定义/Property/Design变更；补齐五个旧住房候选目录，Data Center动态Tier差异有明确证据与不可用保留。LOCAL_SIMULATION_PASS（实际Lua/SQL及完整前序回归，不等于引擎PASS）。用户明确报告P0-B2 PASS，无截图亦可登记USER_GAME_TEST_PASS（用户实机验收）；不推断具体未报告边界：[验收记录](Validation/Results/Specialization_B080_P0B2_User_Pass.md)。P0-C本轮明确仅给[具体计划](../Architecture/v2/P0_C_Plan.md)，未授权实施；Military/Future不纳入实施。已按W0003部署B080.107，126文件逐项hash一致；B079完整恢复点已保留：[部署结果](Validation/Results/Specialization_B080_P0B2_Deployment_20260920.md)。

P0-B1已获用户授权并完成本地实现：B079.106/modinfo106，[报告及测试](../Architecture/v2/P0_B1_Specialist_Support.md)。科研/文化/商业全等级基础3F3P，工业3F+BASE P；只退出旧III额外支持及工业Gold，其他旧能力留各自cutover。LOCAL_SIMULATION_PASS（实际Lua+mock/SQL，不等于实机PASS）。完整前序回归、10k idle、线性批次读取与精确12载体清理通过。已按W0003安全部署；用户明确确认P0-B1及工业城验收PASS，登记为USER_GAME_TEST_PASS：[用户验收](Validation/Results/Specialization_B079_P0B1_User_Pass.md)。不自动推进B2/C/E。

[B078用户证据](Validation/Results/Specialization_B078_P0A_20260918.md)：D3→D10、工作专家读取通过；刷新声已消失。掠夺未测是缺少玩家可控操作，不是游戏卡死。原图已hash归档。按钮文字修正在B079，仅本地确认，等待实际显示反馈。P0-A仍不施加shadow收益。

W0003临时默认部署授权有效，需退出/恢复点/hash/clean commit门禁。历史B079部署：126文件逐项hash一致，B078完整恢复点已核验：[部署记录](Validation/Results/Specialization_B079_Deployment_20260918.md)。main B069.96不改。Architecture A0161目标合同与Design D0032未改；P0-B1是已批准目标的实现。Workflow W0001导航更新为本批完成；P0-B2用户PASS；P0-C具体计划/manifest已备，等待实施授权。

### Historical B077 implementation

原P0-A B077实现及当时本地门禁：[A0161报告](../Architecture/v2/P0_A_District_Completeness.md)。原生capture的实机FAIL及B078修复按上述当前记录为准。

### Historical A0160 planning status


D0032 Architecture Adaptation & v0.1 Implementation Planning 文档完成：[A0160合同](../Architecture/v2/D0032_Adaptation.md)、[考古矩阵](../Architecture/v2/D0032_Runtime_Archaeology.md)、[依赖与批次](../Architecture/v2/D0032_Implementation_Plan.md)、[技术门禁](../Architecture/v2/D0032_Technical_Spikes.md)、[验证](../Architecture/v2/D0032_Validation.md)。**None blocking P0-A / GATE B — READY FOR P0-A**，但尚未授权或实施任何P0批次。

推荐P0-A：单一区域完善度事实、当前专业事实只读适配、科研基础设施纯影子计算、按需诊断。它不施加新收益、不关闭旧收益、不迁移存档；第一次真实effect cutover另设门禁。后续跨owner城市标识、持久成果、合同/重组和高风险primitive都有明确依赖，不能合入第一批。

Runtime仍B076.103/modinfo103，保留已测试A–D2；Design Spec D0032及混合专业authority字节不变。main与live不修改，无部署、无游戏启动、无当前用户测试。规划不宣称55GB长局异常根因解决。既有ACK未完成证据继续保留。

下一步：停止，等待用户授权P0-A implementation；不自动开始历史Batch E或任何新玩法。

### Historical B076 / PAC status (prior Design-sync metadata superseded above)


当前工作：[PAC-I001机构/能力/载体调查](../Architecture/v2/Presentation_Institution_Carrier_Model.md)完成，STATIC_CONFIRMED仅源码/数据库证据，不等于新UI实机通过；完整1894定义分类见报告。PAC-R0002累计机构方案USER_CONFIRMED：Potential决定永久机构集合，ACTIVE只影响能力状态；分阶段Tooltip，presentation-only不进入建筑统计；具体UI接入PENDING_REVIEW；未改源码/玩法/Design/运行包，不启动新四专业玩法或BatchE，无当前测试要求。下一步等待Design/Architecture审阅，不能把机构候选自动公开。

Architecture v2：A/B/C1/D1/C2/D2已完成；B076.103已获准临时部署。用户五组截图复核：[Runtime milestone验证](Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md)。USER_GAME_TEST_PASS仅限本次零城101秒/四城35秒静置无昂贵扫描/写入增长、无显示内存持续增长；不扩展为全部玩法验收或55GB根因关闭。

Milestone：`av2-runtime-b076.103`。Mod仍为6a84027提交内容，本次只提交验证文档。main B069.96不变，实际运行包B076.103；不是stable promotion。D0025不变，E未开始，无新增强制测试。

保留待查：本次T1全窗net_receive=0、discount_ack=0、inflight=1、discount_send=2，不能把未完成初始化的网络/折扣视为功能PASS。抑制计数持续增加不等于实际请求队列增长。长局趋势与功能完整性仍需后续证据；不自动实施修复。原本地1728正常载体对照、10k idle、30k共享查询、前序回归仍有效。

### Historical C2 completion (accepted; its D2-pending wording is superseded above)


Architecture v2：A/B/C1/D1已获接受；[C2 Copy+Industry样本生命周期](../Architecture/v2/Batch_C2_Copy_Industry_Lifecycle.md)B075.102 LOCAL_SIMULATION_PASS（实际Lua+mock，非实机），等待审阅。各通道pending 10,000通知只发1次/无写；每逻辑输入最多3发送；坏包/暂不可用不clear；确认reference/资格失效撤销；63正常载体map与B074一致。D1/C1/A/B/B069回归通过，Discount/Network代码及旧测试字节不变。没有部署，main B069.96、当前live B072.99保持。D2为下一建议，等待用户授权；E后置，GreatWork/Commerce/precision等不在本批，不自动启动。55GB根因仍UNKNOWN。

验证入口：[C2实际Lua回归](../../DevelopmentTests/test_arch_v2_c2.py)。无立即用户测试要求，跨Context/HD真实时序仍属未来实机范围。Copy原每秒及通用通知扫描、Industry通用扫描、重复district/Network query仍留D2，不把本次single-flight当全面性能修复。

### Prior runtime evidence (historical test proposals below are paused)


HD无SPC十分钟窗：[4图](Validation/Results/Specialization_HD_Only_10min_20260915.md)。新PID71307，621秒9.03→8.98→8.99→8.99GB，5到10分钟显示持平；不是前场PID70353延长。本窗未复现持续增长，交互候选加强但根因UNKNOWN，配置按上下文、无游戏画面独立确认。不继续要求静置；下一步只读SPC×CORE交界调查，源码/运行包保持不变。

去SPC保留CORE测试已完成：[6图](Validation/Results/Specialization_HD_Without_SPC_20260915.md)。PID70353零城308秒8.78→8.92→8.97GB，净+.19但后半段增速减小；不能称完全不增长或确认同类持续泄漏。无SPC counter不填0。下一步仅必要时延长同配置观察，勿重复派发刚完成测试；源码/运行包不变，原件hash归档。

HD重新加入已复现增长：[8图/崩溃](Validation/Results/Specialization_HD_Rechallenge_20260915.md)。第二场PID69145零城316秒9.13→9.37→9.58GB；Audit约58/s但事实/扫描/派生/写入0。完成ON/OFF/ON关联，非根因证明。第一场PID68667的pure-virtual/9223148崩溃签名与前次一致，仍与memory分别记录。下一步仅保留CORE去SPC，原版Robert替代测试领袖（差异显式保留），0城5分钟。只更新develop文档，原件hash归档，源码/运行包不变。

独立进程0城HD开关对照：[14图结果](Validation/Results/Specialization_HD_Toggle_20260915.md)。ON307秒9.12→9.30→9.51GB；OFF315秒8.89→8.86→8.88GB，PID不同。两边Audit约58/s且事实/城/区域扫描及写入全0；城市C²路径不解释本窗口差异。支持CORE加入关联但非根因证明。下一步仅恢复CORE作ON/OFF/ON确认，不扩Mod、不改Discount。14图hash归档；只更新develop文档。

新两组非严格对照已复核：[12图结果](Validation/Results/Specialization_Mod_Isolation_2232.md)。Run1=BASE+CORE+TITLE+AREA，双城203秒+0.68GB；Run2去HD加Cheat三城1121秒+0.39GB，用户确认两项UI辅助均保留。所有截图PID45352，用户确认只回主菜单换Mod；不称独立重启ABA。无HD仍Audit+57440、district_scan+344640，但Network未ACK、事实查询路径不同；不认定HD是高频入口唯一来源。原T1没有按指定四Mod/0城执行，六Mod增长集合较FULL11缩小但未最小化。只记录证据，Discount优化继续暂停。

优先级改为Mod interaction isolation：[依赖图](../Reports/Technical/Specialization_Mod_Interaction_Dependencies.md)、[当前矩阵/短测决策树](Validation/Mod_Interaction_Matrix.md)。BASE=SPC+BTS+EMM在观察窗无持续增长；FULL11复现，非112历史组合。当前只派T1=BASE+HD Civ6 Plus，0城300秒，垄断模式保持ON（用户确认）。IND依赖CORE及两项Monopoly++；CIV/DIST分别依赖CORE。Discount OFF/计数扩展/优化暂停，C²证据保留；memory与crash分开。仅文档，无源码/部署变更。

城市规模调查：[Discount嵌套扫描与请求计数边界](../Reports/Technical/Specialization_Discount_Idle_Scaling.md)。双城窗口facts=4×Audit、city_scan=8×Audit与C²/C²+2C代码路径精确吻合；内存因果仍UNKNOWN。纠正此前宽泛“发送不增加”：net_send/receive仅Network桥接，不能排除Discount UI未计数的INIT/ELIGIBILITY重发。单/双城网络就绪与回合状态不同，不以约2.46倍内存斜率断定规模律。本轮只读研究、文档记录，未实施实验或修复。

五组新局/无城/双城对照已复核：[时间线与counter增量](Validation/Results/Specialization_Idle_City_Comparison_20260914.md)。同PID无城376秒Memory+0.36GB，双城静置317秒+1.14GB；后者Discount+18602、事实+74408、城市扫描+148816，但完整derive/建拆/Property/send/receive均不增。重复检查是真实热点，内存因果UNKNOWN。Turn1单个in-flight长期等待；抑制计数不是队列长度。10原图hash归档。只记录调查，不改代码、不部署，不重发本测试。

21:25:30缩减Mod新局崩溃已保存：[50项加载集合/11第三方/原生abort](Validation/Results/Specialization_Crash_20260914_212530.md)。用户称静置4–5分钟、缓慢增长；TBB线程__cxa_pure_virtual→abort，根因UNKNOWN，不等于OOM或已证明HD冲突。原日志/崩溃文本/Mod数据库一致性副本/UUID清单已在外部hash归档，可安全重启后核对。未改源码、配置或部署。

用户逐表确认原存档第三方Mod均存在、未提出剔除项；按本轮启用组合核对上下文登记为原基线成员，含Switch Civilization。[基线记录](Validation/Results/Specialization_Mod_Isolation_Baseline.md)。官方游戏模式实际开启状态不据此推断。后续禁用/新局是独立测试配置；不升级任何兼容性或内存修复PASS。

用户确认原存档组合含Switch Civilization；固定已归档112项为原基线，后续111/94项属于另行测试配置。[新局隔离边界与监听初查](Validation/Results/Specialization_Mod_Isolation_Baseline.md)。当前log与选中ModGroup不同步，不能声称立即刷新或用最新选择覆盖原基线。开始只读检查原列表脚本；未发现Switch空闲高频循环的直接证据，不等于排除交互问题。新局阴性不能排除成熟城市才触发的机制。

最新读档Mod集合已核实：[111项与证据边界](Validation/Results/Specialization_Loaded_Mod_Set_Verification.md)。相对默认112项仅移除Switch Civilization；日志后续确有组件应用/Gameplay初始化/反序列化。111 UUID唯一数据库映射，72绝对路径XML核对，39官方相对路径未独立解析。该加载晚于监控，不能追溯证明前一PID配置；不需要用户逐个截图，不据此判定冲突。

双footprint实机证据已复核：[分类增量/Mod配置边界](Validation/Results/Specialization_External_Monitor_Paired_Footprint.md)。同PID间隔630.895秒，MALLOC_TINY815→3513原生MB，graphics5308→5311MB；堆分配器是本窗口增长主项，不能归因某Mod或等同Lua泄漏。当前较晚Modding.log提取112 UUID/name条目（含官方内容），仅当前启用配置，不冒充被测存档加载集合。6原件11176字节hash归档；无源码/部署改动。

External Monitor1.0.1修复导出后重启失败：实地只读确认session-20260915T025957200955-3dfae769只剩.DS_Store，旧prune无条件读取session.json。现跳过空/Finder-only残留目录且不删除；缺元数据但仍有其它证据时明确拒绝，symlink保护保持。LOCAL_SIMULATION_PASS（临时目录/模拟进程，非游戏）：15测试通过，含移走后重新创建session、部分日志和悬空symlink保护。采样/600秒冷却/Mod B072.99/main/运行包均不变；未启动监控或自动连接游戏。

第三份外部session成功取得footprint分类：[结果](Validation/Results/Specialization_External_Monitor_Footprint_Session.md)。USER_GAME_TEST_PASS仅指此次采集：0.4096秒、exit0；原生图形5290MB，六类MALLOC合计约5734MB（保留工具单位/舍入），两类均需保留排查。90秒physical footprint11.856→12.380 decimalGB，但只有一张分类快照，无法判定增长属于哪类，根因UNKNOWN。五文件4731字节已外部hash归档；无代码/部署改动，不要求重复证明采集可用。

第二份外部session复核：[读档/静置与vmmap超时](Validation/Results/Specialization_External_Monitor_Load_Idle_Session.md)。用户先监控后读档，随后无操作；不能把4.23→12.44GB全部算作idle增长。末155秒仍+0.75GB，具体加载完成时刻未知。vmmap基线5秒超时、0字节，随后禁用且趋势继续；没有内存分类证据。五原件含空文件已hash归档。仅文档更新，根因UNKNOWN，不改源码/部署。

External Monitor首份用户实机session已复核：[结果](Validation/Results/Specialization_External_Monitor_First_Session.md)。15次30秒采样、同PID/启动身份、正常停止；USER_GAME_TEST_PASS仅指外部趋势采集。约7分钟physical footprint10.38→16.58GB（+6.20GB），RSS同时下降，不可混为一个内存口径。自动快照OFF、无marker/同窗Counters，根因UNKNOWN；不能与此前不同PID的19:07截图直接配对。四文件2743字节已外部归档/hash验证；无代码/部署变化。

External Runtime Monitor1.0已加入develop独立工具：[使用入口](../../tools/external_monitor/README.md)、[本地开销/边界证据](../Reports/Technical/Specialization_External_Monitor_Validation.md)。13项测试、10000采样、有界保留、仅自建测试进程OFF/ON及系统工具验证通过；未连接当前Civ VI、未启动监控、未部署或增加Mod版本。用户自行启动后可记录进程趋势；默认自动快照关闭，sample仅手动。不能替代尚不可用的游戏内日志或读取Turn/counters；不宣告内存问题解决。

B072.99实机日志门禁失败：三组截图均FILE_API_UNAVAILABLE；自动日志不能承担长局证据。USER_GAME_TEST_FAIL（用户实际游戏显示未达到日志验收标准）。同回合59、55秒Memory11.06→11.34GB；Discount Audit+2222、事实/城市/区域扫描持续增加，但完整derive保持1、建拆/Property/发送接收无增量。[逐项读数与归因边界](Validation/Results/Specialization_B072_Idle_Incident.md)。全部29份投递文件已外部归档并核对hash，无新代码/部署，main及live保持不变。此结果取代下文“原生接口待测”：当前io路径已确认不可用。下一步需要另行授权可行日志transport及定向重复检查调查，不宣告55GB问题解决。

B072.99已获用户临时部署授权并确认游戏完全退出，实际运行包现与8b2ca3a的Mod逐文件一致。此前B071.98与B069.96均保留可恢复整包，main不变。部署证据和最小原生日志验证见[本次切换记录](Validation/Specialization_B072_Temporary_Playtest.md)。下文“本轮未部署/live B071.98”是实现批次结束时历史状态，由本项取代。尚未获得原生文件接口实机结果，不宣告长局日志可用。

B072.99仅新增低频Runtime Audit、受限文件sink和既有Counters中的状态说明。[实现/字段/上限/测试/原生接口限制](../Reports/Technical/Specialization_B072_Runtime_Audit.md)。LOCAL_SIMULATION_PASS：100万counter事件零I/O，10000回合固定节点及4MiB轮转，8文件保留，失败停止，真实Network ON/OFF输出和计数一致。STATIC_CONFIRMED：没有新Gameplay请求/收益/Design变更。

**尚不能保证长局自动日志可用**：原生UI是否提供io.open/os.getenv尚无实机证据；不存在时明确DISABLED，绝不以print或Property伪装落盘。USER_GAME_TEST_REQUIRED：用户授权切包后，一次读取状态+一回合产生TSV，成功才可称long-play logging candidate。当前没有部署；live继续B071.98，main继续B069.96。用户无需现在停止当前游戏。55GB事件不宣告解决；小数精度仅登记[后续合同](../Architecture/v2/Yield_Precision_Backlog.md)。

### B071临时部署事实（当前live仍为此版本）

2026-09-14用户授权临时develop实机测试且确认游戏已退出，已切换实际运行包至B071.98/modinfo98；[切换证据、短测与恢复说明](Validation/Specialization_B071_Temporary_Playtest.md)。stable/main仍B069.96，完整恢复副本在Mods扫描目录外保留并与main逐文件hash一致。当前运行覆盖是有明确授权的一次测试，不是promotion；未启动游戏、未改配置或存档，USER_GAME_TEST_REQUIRED。下文“未部署/等待切包”是Batch B完成时历史状态，已由本项取代。

Batch A（d1ac666 / B070.97）用户已审阅通过。develop Batch B / B071.98本地实现完成：[共享Network视图及证据](../Architecture/v2/Batch_B_Shared_Network.md)。LOCAL_SIMULATION_PASS（本地真实Lua模拟，非实机）：168组三方完整输出、9步A合同metadata、真实四城市Discount cold1/warm0派生、102次Audit累计1派生408命中、玩家/epoch/修改隔离及原B069/A回归。STATIC_CONFIRMED：仅Bridge/Counters/版本标识改变，consumer、UI、SQL、NetworkInput、Design与stable包不变。无部署。

当前等待用户审阅及是否授权临时develop短测；不自动切换运行包。今日stable 44→55GB事件仍需独立内存趋势验证，本批只解决重复Network derive，不能标记内存BLOCKER已解决。C/D/E、UI轮询等保持未实施。

### Historical: Batch A完成时状态（已获用户接受）

develop AV2-A / B070.97完成，等待用户审阅；[合同与验证](../Architecture/v2/Batch_A_Input_Contract.md)。LOCAL_SIMULATION_PASS（真实Lua本地模拟，非Civ VI实机）：A–I、初始化UNKNOWN/已确认撤销/重入/旧候选/epoch、24组新旧输出、原B069行为回归及73个Lua编译。STATIC_CONFIRMED：SQL、D0025、main与实际B069.96包未改；未部署。

本轮不要求立即切develop测试。Batch B可评估Network共享视图；C/D样本与消费者自身暂空路径仍待处理，E保存迁移仍未动。不得把Batch A完成表述为全部性能风险解决。用户当前长局继续stable。

2026-09-14 workflow：以[部署合同](../Architecture/Playtest_Workflow.md)与根AGENTS为准；下文历史“不commit/push/停止长局”不再派发当前任务。

### Stable B069.96既有验证记录（本轮未改变）

B069.96现为用户指定的v0.1 Playtest Baseline；用户继续长局，main冻结玩法，develop承接后续开发。此前性能短测没有回传完整计数证据，不能标为已解决或实机PASS；风险留在Playtest Backlog按严重程度分诊。普通非商人任务不再发商路dirty；无法可靠识别时只NEEDS_REVALIDATION，保留最近完整验证状态。完整快照内容相同不发布、不增加topology revision、不通知收益消费者。读取失败最多3次本批尝试；明确端点/商人消失、战争或读取失败后的原生数量下降仍会撤销。失败包不覆盖已验证完整集合，发送只允许单个in-flight，ACK后空闲UI通知不再调用sender。

STATIC_CONFIRMED（源码静态证据，非实机）：全部SQL/数值/Design不变；继承三模块逐字节保留且未启用；其它模块仅添加固定计数/原调用转发。未实现shared derive缓存或扫描重构。LOCAL_SIMULATION_PASS（本地Lua模拟，不等于游戏通过）：真实后台collector/sender/receiver与Commerce模块的10次已知/未知单位事件、相同输入零建拆/Property/发布/derive；真实路线增删、端点失效、读取失败有限重试、请求重入/拒绝ACK、跨回合；固定schema模拟10000回合不增加容器节点数。

Performance Counters为固定条目current/total/previous/peak；新增两个纯读取诊断入口。计数为本Mod直接Lua原生调用，不包括其它Mod或引擎内部Modifier的Property写。独立自动runtime log未启用：未验证安全的Civ VI文件写入/轮转接口，按用户J10/J12回退为Counters+手动Snapshot，禁止用永久Property或无限print替代。无自动日志文件要求。

USER_GAME_TEST_REQUIRED：仅短测[普通单位移动前后与一回合计数](Validation/Specialization_B069_User_Tests.md)；这是保留的未验证案例，不再要求用户暂停长局或现在重测。UI/性能/架构后续工作仅在develop按授权推进，ownership仍隔离。完整[实现说明](../Reports/Technical/Specialization_B069_Performance_Phase1.md)。

### HISTORICAL：B068.95 UI修订（暂停继续验收/微调）

B068.95为UI小修：用户已实机确认两种单位紫色滤镜、左上诊断入口位置通过（USER_GAME_TEST_PASS）；按钮文字为空为USER_GAME_TEST_FAIL。改为显式Label并初始化SetText，保留原回调；城市潜力移到同一WorldTrackerHeader诊断入口下方，仅显示“工业1级”等四字符短文本，仍代表永久Potential，悬停信息不变。

本机UserInterface/Localization日志未直接证明空白根因，未找到Lua.log，不将导出登记通过。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：6个UI/版本文件变化，108个运行文件不变，实际UI mock/语法通过。USER_GAME_TEST_REQUIRED仅新文字及短标识位置，已通过的滤镜不重测。[结果与最小验收](Validation/Results/Specialization_B068_95_Result.md)。

### HISTORICAL：B068.94初版界面

用户批准进入v0.1 playable UX polish。B068.94只修改展示与诊断，核心保持B067.93；无玩法、数值、Design、自动继承恢复或32次限制变更。

Potential未创建真实建筑：HD按建筑枚举存在副作用风险，按用户允许的安全替代方案采用原生城市面板只读标识。真实EffectiveFacts/Property仍为权威；选中城市显示四档名称与永久潜力。诊断入口移到WorldTracker header右侧，15只读主入口，长报告可滚动，旧实验控制和UnitSites常驻入口隐藏。原有投资/施工确认流程不变，合法目标改紫色原生高亮；日志直接输出Lua.log，重复UI错误保留首条与次数。

STATIC_CONFIRMED（静态证据，非实机）：94个既有文件不变，Gameplay仅新增独立只读展示分支；D0025 hash不变。LOCAL_SIMULATION_PASS（本地模拟，非实机）：Potential1–4/切城、目标去重/清理、日志去重、15入口以及既有机制/SQL/隔离回归。USER_GAME_TEST_REQUIRED：真实HUD位置、tooltip、紫色层颜色/切换兼容和Lua.log输出；不将本轮参考截图登记PASS。

[实现与兼容性报告](../Reports/Technical/Specialization_B068_Playable_UX.md)，[最小三项验收](Validation/Specialization_B068_User_Tests.md)。完整恢复点local/before-b068；不commit/push。当前等待用户顺手验收UI，不重发核心能力测试。原32次新城/通用资格/所有权仍隔离或未来事项。

### HISTORICAL：B067隔离完成时状态

用户确认当前可玩范围只考虑自行建立且不易主的城市；累计32次新城绑定列未来处理，通用ELIG暂缓，整体验收由用户游玩中进行，不追加测试批次。界面整理等待用户给要求，必须保留可进入的诊断入口或日志证据。此为实施/验收顺序，不修改D0025征服/资格玩法设计。

B067.93已隔离所有权实验：Gameplay不再Start CityInheritanceRead/InheritanceShadow/CityInheritance，清空对应shared入口与OnPermanentCityWrite，故不再注册这三模块监听、写影子账本或调用继承Resolve覆盖。源文件/manifest ImportFiles和既有Game备份不删；恢复辅助函数保留但没有运行调用入口。普通收益模块原有路线端点撤销事件不移除。SHADOW按钮暂保留布局但返回明确暂停提示，不报模块缺失；其它P0诊断继续可用。D0025时代对话25%、商业四及既有核心收益不变。

LOCAL_SIMULATION_PASS：实际Gameplay隔离段、暂停按钮ACK/无city与ledger访问、三模块未Start、shared回调/覆盖为空；核心前批回归和25%模型/SQL检查通过。不是新原生PASS；按用户要求不新增实机测试。整体验收由用户游玩中完成。

当前收尾只有：等待用户界面要求，整理玩家可读专业/网络/投资信息与可进入的诊断层；版本/已知限制说明；完成后复核默认AUTO和测试开关、建立经用户授权的checkpoint。日志可记录错误/主动读取/关键变化，不周期全扫描或每帧打印。32次和通用资格不重新插入当前任务；未来专业不扩大。见[诊断与收尾评估](../Reports/Technical/Specialization_B067_Isolation_and_Diagnostics_Plan.md)。无新Design Revision、commit/push。

### HISTORICAL：B066范围评估与继承过程（不再派发测试）

用户B066回报Read shadow / events提示尚无确认转移记录，本次登记/报告路径USER_GAME_TEST_FAIL，未取得恢复PASS。该按钮按已保存watch UID读取，不要求选AI城；无记录分支未区分watch缺失与登记缺失，并隐藏底层日志，根因未凭一句提示确定。当前停止扩展，用户先评估排除城市易主/占领后的收尾范围，不新增测试。

[自建城市范围盘点](../Reports/Technical/Specialization_Self_Founded_v01_Readiness.md)：固定测试文明且全程自建不易主时，四专业核心能力基本实现，尚需处理累计32次DEV绑定限制、玩家入口/说明等；通用ELIG未实现，完整D0025仍含未完成Conquest/Claim。停止开发不等于禁用，B066仍有绑定读取与事件入口，建议可逆隔离后做自建城市可玩版，不整体回滚丢失商业四/25%成果。本轮未修改源码、Design或运行包。

### B066实现与原测试要求（本次评估期间暂不继续）

B065用户口述“没有问题，继续推进”，事件回调本批USER_GAME_TEST_PASS。无新截图或具体参数，不能把口述扩大为所有事件形状均已确认。见[结果](Validation/Results/Specialization_B065_User_Result.md)。

B066.92实现已有Identity的转移登记与返回恢复：加载结束后，仅CityTransfered(newOwner,newCityID)可定位实际新端点，或HD已有CityConquered(newOwner,oldOwner,newCityID,x,y)形状可校验时处理；未知形状/来源歧义不猜。Game登记当前Owner/CityID、转移revision和完整来源快照；未启用Owner为DORMANT，不恢复City记录/收益；启用Owner时验证已有Identity、FLOW完成、无pending投资和目的地无冲突，按明确字段重建City Property，保存原UID/first/投资凭据/模板，恢复现有读链并重算ACTIVE。重复事件不叠加，不复制路线集合。

Binding.Resolve新增对已确认继承绑定的读取入口，CityJournal/CityFlow增加严格恢复入口；Shadow允许仅已APPLIED的同UID新端点同步，下一次转移使用更新后的账本。CityBuilt遇原址不同端点注销旧关联；不在load仅凭坐标推断转移、不在CityRemoved立即删成果。尚未切换为全局新UID生成器/所有写入的单一权威账本；原32城DEV绑定限制、缺史旧城、无Identity Claim仍后续。部分投影失败保留PROJECTING与错误，不能宣称多次Property写入原子。

LOCAL_SIMULATION_PASS：真实继承模块+EffectiveFacts验证AI阶段无City写入，返回后3凭据→Potential4、Governor2→ACTIVE2、模板保留，重复事件/加载不写、连续转移/最新快照、原址新建注销、pending和冲突拒绝；前批回归保留。真实CityFlow恢复/游戏事件顺序及实际收益为USER_GAME_TEST_REQUIRED，不能用模拟代替。

USER_GAME_TEST_REQUIRED：[B066最小测试](Validation/Specialization_B066_User_Tests.md)：同工业城转给AI→取回→读档，最多3图。用更新前易主前存档；不自动追认此前未被本模块登记的历史转移。D0025/时代对话25%不变，无新设计决定，无commit/push。

### HISTORICAL：B065修复与待测记录（现已口述通过）

B064三图已复核：Game备份INDUSTRY/3笔投资/6模板在赠送AI及重载后保留，重载写入0，USER_GAME_TEST_PASS仅此范围。事件总序号始终0且InheritanceShadow.lua74报function expected instead of nil；注册成功但callback未执行。保存原因SELECT说明此前自动加载备份未被证明。见[结果](Validation/Results/Specialization_B064_User_Result.md)。

B065.91修复：去掉table.unpack依赖，safe(fn,...)直接通过pcall转发参数；兼容缺unpack且保留nil/false/0。完整堆栈只写Lua.log，面板显示短错误码。修正Probe/XML漏留B063.89的标题，当前明确B065.91。D0025和时代对话25%不变，不接正式继承或改收益。

LOCAL_SIMULATION_PASS（非实机）：禁用table.unpack和全局unpack后的真实加载/转移回调、nil/false/0参数、自动备份、事件持久/24条上限、重复/读档/错误隔离及前批回归通过。先前模拟用标准Lua而漏此运行库差异，已新增针对性回归。

USER_GAME_TEST_REQUIRED：只补一次转移后的事件报告，不重测备份保存读档。重载易主前存档、Select shadow city、赠送AI，Read shadow / events截图一张；错误=无，相关事件序号增加并显示参数。若仍为0/报错回传即可，不继续接正式身份迁移。

### HISTORICAL：B064准备记录（结果以B065顶部为准）

D0025已按用户明确决定接受：时代对话GW-001系数15%→25%，模型与14类C/T ModifierArguments生成式同步，D=1/2/6/7对应0/25/125/150%。不新增用户实机测试，不把新系数标实机通过。作品范围、创作者时代/文物例外、theming、GW002不变；D0024原文已冻结。

B064.90独立影子账本已加入：Game Property保存现有有效城市的五项完整原始记录及pending阶段；加载时一次读取已启用玩家合法绑定城市，并在现有身份/投资/模板写入确认后同步。失败只报告，不再次消耗移民；正式玩法仍读取原账本。新账本不自动恢复City Property、不关联易主身份、不授予收益。它是持久备份验证，尚非正式永久UID/继承切换。旧token仅作备份键，禁止不同Owner/ID覆盖同键。

事件仅记录相关已登记城市的CityTransfered/Added/Removed/Initialized和Game CityBuilt/Conquered原始参数、原位置当前端点；保留最近24条，面板最后6条、Lua.log完整当次事件。事件不用于自动认领，已知旧Owner/ID及实际端点/坐标过滤可能漏未知形状，需本次实机检查。未启用Owner不会获得新专业或收益。每条相关事件核对已登记位置，不是每帧/回合扫描；移除不删备份，原址新token另记不继承。

LOCAL_SIMULATION_PASS（本地非游戏）：真实Lua易主后五项City Property缺失而Game保留投资/模板，重建Lua环境后持久读取、pending阶段、重复100次无写、24条上限、无关/空闲事件无写、原址新城不同token不串账、备份写失败不改城市；B062/B063与前批回归、D0025模型及内存SQL通过。

USER_GAME_TEST_REQUIRED：仅[独立备份小批次](Validation/Specialization_B064_User_Tests.md)。用易主前有效存档，首次加载自动备份后选中观察城市，赠送/转自由城，读报告，再保存重载读报告；不验证正式继承收益，也不重测时代对话。运行B064.90/modinfo90，未commit/push。

### HISTORICAL：B063研究结论（下一实施已由B064取代）

B063赠送AI补图已复核：原Owner/CityID0/393221→1/196610，位置65,31，两区域仍在，五项Property仍原有→现无。此为用户所述赠送路径的追加证据，正式继承未实现，不扩大为军事征服/事件顺序实测。见[补充结果](Validation/Results/Specialization_B063_Gift_User_Result.md)。

静态研究推荐Game Property完整永久账本+稳定UID+经验证的转移关联；现有Game绑定表只保留编号，不含投资/模板，不能单独恢复。HD已有Game表格和Gameplay CityConquered(newPlayer,oldPlayer,newCityID,x,y)先例，但赠送/自由城覆盖、事件顺序/旧对象存活时点仍未知。下一小步为影子账本与有上限事件日志，再切换正式继承；不使用位置独自认定身份、不在CityRemoved时直接删成果、不每帧扫描。详见[研究](../Reports/Technical/Specialization_City_Inheritance_Ledger_Research.md)。本轮只研究/文档和归档，运行B063.89不变，暂无新用户测试。

### B063自由城市首批结果（补充见上）

B063用户两图已复核：Cheat Panel转自由城市，Owner/CityID由0/393221变62/65536；位置65,31及已完成市中心/工业区保留，TOKEN/FLOW/JOURNAL/INVEST/TEMPLATES五项均由有变无。原INDUSTRY、3笔投资、6模板不能从新City对象读取。B063观察入口USER_GAME_TEST_PASS，正式继承尚未实现，不能标通过；仅该转移方式有实机证据。

本机Cheat MakeFreeCity直接调用CityManager.TransferCityToFreeCities（STATIC_CONFIRMED源码证据）；不是已证明所有军事征服/赠送都相同，也不能断定引擎内部具体清除时点。需先建立独立持久账本与可靠转移映射，再恢复城市关联并重算ACTIVE/网络；不能只改Owner或依赖易主后读取旧Property。无新设计决定，当前无需追加用户测试。详见[本批结果](Validation/Results/Specialization_B063_User_Result.md)。运行仍B063.89；本轮仅记录/归档，不修改运行源码。

### B063准备记录（测试要求已由上述结果关闭）

商业四本批已按用户回报收口：截图科技6→11，源28.4219×20%最终floor5，实际载体1+4；第二源不叠加。零路线、反序更新/读档、分发不二次汇聚、总督撤销按用户证据通过。文化/工业未独立实测，用户接受暂缓，不冒充USER_GAME_TEST_PASS。城市面板同回合延迟接受不修复。详见[结果](Validation/Results/Specialization_B062_User_Result.md)。

B063.89新增只读城市继承观察：记录选中城市五项原始Property深拷贝，换Owner后按原位置定位并对照Owner/CityID、token、专业账本、投资、模板。仅主动点击读取，无后台扫描、不写Property/收益、不执行继承、不重置投资。坐标只是此次观察定位，不作为永久UID。内存基线读档即失效。

STATIC_CONFIRMED（源码静态证据，非实机）：新模块没有状态写入/生命周期扫描；已有Owner锚点确实需要正式迁移适配。LOCAL_SIMULATION_PASS（非游戏）：真实Lua深拷贝、Owner/CityID变化、Property保留/变化/消失、城市位置空缺、读档清空观察以及B062回归通过。

USER_GAME_TEST_REQUIRED：仅一项城市易主前后只读对照，见[最小测试](Validation/Specialization_B063_User_Tests.md)。当前不是完整征服继承已实现；四专业能力主线已接入，完整v0.1仍需征服/Claim、通用资格及发布收尾。无新Design修改、Git commit或push。

### HISTORICAL：B062实现与待测记录（现已由上述结果取代）

用户重新授权从已提交/推送3382d7d B060.85基线审查并重做商业四。B062.88（modinfo88）为新独立CommerceConvergence.lua，D0024保持不变；B061.86/87隔离目录不覆盖，不恢复旧重试和跨回合扫描。

问题审查：用户B061.86 OFF图source28.4219→floor5、实际S6；AUTO6→7只有口述，没有AUTO载体证据，仍不能解释实际+1。B061.87共用网络报BATCH_LIMIT_OR_SHAPE、0/5路线。真实3382d7d接收代码在Count/Data缺失的零路线模拟中同样失败；说明存在先于87的空值协议脆弱性，不是已经证明游戏原生如何序列化。B062发送WireCount=count+1、空数据EMPTY，接收严格decode/count冲突/实际路线数校验；旧非空协议仍兼容。不把UNKNOWN冒充有效空集合。

STATIC_CONFIRMED：BackgroundRoutes.lua与3382d7d逐字节相同；NetworkSender只改明确空包字段，没有87重试；NetworkBridge只改解码及商业模块新快照后通知，旧主体由精确diff回归。沿用此前48个整数载体的定义/ID便于清除旧档残留，并非恢复旧Commerce Lua。

LOCAL_SIMULATION_PASS（非游戏）：真实sender/receiver经过丢弃Count0/空Data边界fixture，非空→空清除网络和商业收益、重复空包/错误count/非空缺数据拒绝；直接源按对应总yield最高，不按等级、不求和、不通过distribution继承，最终floor；100次相同计划无额外写入；OFF/固定TEST5/AUTO共享apply，1+4载体核对、ACTIVE降级/重载清理及前批回归。全部来源计划先算完再写city层。只读报告分别显示预期、最后配置、实际载体组成、原生城市读数/OFF基线差值，不用配置冒充实测。

USER_GAME_TEST_REQUIRED：B062最小批次见Validation/Specialization_B062_User_Tests.md。完整退出再启动加载原档；先零商路验证共用网络空集合，再原商业4城OFF→TEST+5（不需要商路）检验同一承载层，再恢复AUTO接一条科研直连验证20%与跨回合。任何前项失败即停止。不要求重新做全部高级收益/多源矩阵。无新commit/push。

技术边界：缺当前网络时撤销本项而非沿用旧来源；城市UI/实际收益刷新时点、+5原生效果及第三方间接回路未实机确认。技术目录0..65535不clamp；报告错误。TEST5只作用选中Commerce4城，本玩家其它汇聚暂清除；OFF关闭本玩家汇聚且记录选中城读数；AUTO恢复所有合格城市，读档默认AUTO。控制均不改变Potential/身份/永久账本。

### HISTORICAL：B061隔离与B060.85 checkpoint（仍保留）

用户明确要求回滚/隔离商业四并提交之前成果。当前源码恢复商业四实现前的完整B060.85（modinfo85，106文件），SHA256 a0e0fd75e87872612ab61a7354882ca7081767890149917efa688a60412216d4，与独立部署备份逐文件一致。B061.86/87商业汇聚及对NetworkBridge/NetworkSender/BackgroundRoutes的后续修改不在当前运行源码内。商业四停止开发，不能把历史B061测试计划当作当前任务。

用户已口述巨作相邻全部USER_GAME_TEST_PASS，基础3P→每件1P的原生小数截断接受、不修复。B060.85此前没有商业四正式收益。D0024继续保留用户确认的GW小数边界、未来商业汇聚总量备选和最终floor设计；保留设计不代表商业四已实现。

完整撤回前工作树679个非忽略文件及SHA256清单、tracked diff保存于忽略目录local/Isolated-CommerceIV-B061-20260913/。B061报告保留审计，B061可执行测试/新fixture随完整隔离副本保存，不再混入当前回归入口。恢复B061前test_b055_regression.py，不修改冻结旧fixtures。

B061.87最新两图：商业与通用网络均报BATCH_LIMIT_OR_SHAPE，UI路线COMPLETE_UI_SHADOW、商路显示0/5；空集合Data空串跨界面可能缺失是未证实假说。不能声称已修复根因，也不能把失败状态归因于旧存档。B061只增加1的异常仍未解决。先恢复基线，不继续叠加修补。

### HISTORICAL NOTES：已撤回的B061开发与测试

B061.86首批USER_GAME_TEST_FAIL：用户AUTO城市Science6→7、OFF6；截图只有OFF，source28.4219→20%5.6844→floor5，不能据此确认AUTO实际配置曾为5。第二图turn22 NETWORK_REFRESH_PENDING。未标商业四收益PASS。数据库已确认48载体定义存在，SCIENCE Amount为1/2/4等正确整数，不归因为旧组件缺失。

B061.87修复两项静态缺口：NetworkSender原先只按API调用成功去重，没有按Gameplay接收确认重试；BackgroundRoutes增加独立当前回合观察，漏回合事件时在已有UI脉冲中仅标记一次重采样。发送只对同包最多重试两次，不放宽当回合/来源有效性要求、不用旧网络继续发收益。收益报告增加每类实际存在载体总数值及bit组成，网络未就绪用简短状态/前后回合/发送状态代替长堆栈（完整日志保留）。

LOCAL_SIMULATION_PASS（不等于实机）：真实sender首次丢包恢复/最多两次/空闲零请求/新批恢复、真实turn observer一次触发，以及既有商业择优/撤销/SQL和旧批回归。实际只加1原因仍未确定；不猜测是倍率/刷新或成功。Design D0024、SQL/20%/floor/结算规则不变。

USER_GAME_TEST_REQUIRED：读原存档B061.87，原商业四城OFF后读一次，AUTO后Read Commerce IV截图，报告若目标5应显示配置5/载体5[1+4]；过一回合再Read截图。若仍未就绪，报告包含后台回合/发送信息，立即停止不重复。此次无新增组件，重载即可；若版本未刷新则完全退出重启。结果回来前暂缓多源/分发测试。

### B061.86实现基线与初始测试计划（暂缓）

D0024已同步：用户口述GW002全部USER_GAME_TEST_PASS（用户实际游戏验证），原生逐件半点截断接受不修复，未提供新截图；不扩大到未知类别/其它接口。B061.86开始商业IV正式自动汇聚：直接R/C/I来源，各yield按实际城市总量择最高，20%后floor一次。条件总量备选已明确采用，不假称精确纯本地。城市层整数载体，与Industry区域输出/Research区域复制隔离；Commerce不能作源，先计算本轮全部计划再应用、绝对替换不累加。

STATIC_CONFIRMED：48个整数城市载体、无区域yield写入，已检查当前专业身份约束；LOCAL_SIMULATION_PASS：真实NetworkBridge与计划/结算Lua，最高产出不等于最高等级、多源并列不相加、distribution不冒充direct、重复100次无写入、floor、OFF/降级/断源/过期/重载/端点失效、SQL和既有回归。静态/模拟不等于实机通过。

USER_GAME_TEST_REQUIRED：完整退出应用重启B061.86读取原存档（新增Lua/SQL），一座Commerce ACTIVE4中心已有R/C/I直接路线；Read Commerce IV，OFF/AUTO固定条件比较城市实际S/C/P，重复AUTO不叠加；增加/移除最高源检查回退；中心往另一Commerce4仅分发不得再次汇聚原源。最小3例见Validation/Specialization_B061_User_Tests.md。

限制：整数载体0..65535/每yield是技术目录非Design cap，超范围明确错误并尝试撤销，不clamp；城市倍率/同回合原生缓存刷新需实测；其它Mod把商业总量传回源的间接回路仍开放风险。无无限扫描/通用UI事件审计；加载、真实城市/总督/作品/建筑事件与网络新快照触发，空闲不扫描。读取按钮只读；OFF/AUTO是全玩家测试开关、重载恢复AUTO。

### 历史：B060组件加载与验证过程（已通过）

B060.85用户截图已收到ACK，明确GWA_MODULE_NOT_LOADED，后台模块=false、本次已收到=true；不是学院BASE=0的证据。用户确认本城学院BASE Science +2。2026-09-13只读检查：当前Startup.log InitialInit 11:28:27；最新DebugGameplay.sqlite更新时间12:14:08，BUILDING_SPC_B060_%为0（应156）；12:14:18 Modding.log注册/应用B059但没有SPC_B060_Adjacency。磁盘manifest包含B060组件。证据支持当前进程组件清单未刷新，新Lua模块/SQL均未完整加载。先完全退出应用重启、读原存档再验证，不改代码、不删缓存、不新建局。

USER_GAME_TEST_PASS仅限85报告成功揭示模块缺失；相邻读取/收益仍USER_GAME_TEST_REQUIRED。最小测试：用户完全退出Civ VI后重启并加载原存档，选同Culture4城，GW adjacency Read。学院BASE+2应贡献SCIENCE BASE=2、每件=1（其它专业区域Science基础相邻若有则另计）；报告正常后才继续原收益批次。若仍失败只回传完整报告。上一轮“回主菜单重载”不足，已更正。

### B060.85报告修复记录

B060.85仅修复相邻报告请求链路，不改D0023/SQL/收益公式。用户B060.84三图：前两图仍旧Dialogue OFF报告，后一图停READING GWA_AUTO，故本批报告交付记USER_GAME_TEST_FAIL，不能由此判定BASE getter失败。静态确认GWA早返回分支未绑定RequestToken且异常未生成ACK；修复为每次返回成功/明确失败报告。UI仅对待回复的GWA读取/幂等开关使用事件脉冲最多两次重试，不扫描；增加后台模块、最近收到请求、本次接收匹配及相邻采样异常信息。根因仍需新报告定位，不宣称已确定引擎丢请求。

LOCAL_SIMULATION_PASS：真实Gameplay请求分支+真实Panel请求/渲染，正常未就绪、模块缺失、Describe异常、城市失效、首次丢包且计时器不运行时恢复、全丢包只重试两次、空闲零请求，以及B060模型/SQL和前批回归。USER_GAME_TEST_REQUIRED：旧存档重新加载B060.85，选Culture4巨作城，只点一次GW adjacency Read；截图完整报告，若仍READING可点一次Show/Copy，不需过回合反复测试。结果回来前暂停收益验收。

### B060.84实现基线（收益验证暂缓）

D0023已按用户明确确认接受：GW002七类作品含Artifact不含Relic/Product；全部已完成专业区域含Theater/特色替代，按原yield各50%BASE。B060.84实现自动逐作品基础相邻能力，后台复用Dialogue事件样本，新增六yield区域向量，Gameplay重验端点/类别/完成/全集。与时代对话独立开关，原生GreatWork YieldChange载体，非城市补贴。

STATIC_CONFIRMED：每个piece七类六yield定义、±0.5及二进制目录；RequiresPopulation分类覆盖已确认本机专业区域。LOCAL_SIMULATION_PASS：真实Lua/内存SQL、完工/特色/非专业排除、BASE独立于Actual、作品数不平方、负/半点配置无丢精、重复/空作品/ACTIVE降级/OFF/无效端点/过期样本/重载清理及前批回归。配置不是实际收益PASS。

USER_GAME_TEST_REQUIRED：原存档主菜单重载B060.84，GW adjacency Read/Off/Auto。建议当前Culture4城两著作放非主题化槽，先Dialogue OFF隔离上一能力；Adj Off/Auto两图包含偶数/奇数BASE对照；相邻翻倍卡不改BASE/单件配置；总督调离撤销，原生整城更新允许下回合。详细步骤见[本批测试](Validation/Specialization_B060_User_Tests.md)。无新局要求，缺数据库/采样报告一图即停。

IMPLEMENTATION_LIMITATION：本批每yield BASE须为整数且绝对合计≤8191，目录上限仅当前技术支持，不是Design cap；超范围/非整数报告错误并清除本项，不静默clamp/floor。原生0.5与普通/时代对话/主题倍率的关系待用户数据，不自行改城市补贴。当前测试优先验证前者，用户已要求停止主题化深挖。

### 历史：GW002范围待确认（已由D0023解决）

用户指示停止主题化深挖，转GW-002。两图按文件时间TEST100(T15)→OFF(T14)，同2著作/D2/theme1：作品20C/30T→10C/25T，支持本组Culture主题放大(+10)、Tourism基础追加(+5)的不同原生表现；不同游戏回合不作城市总量因果对照。只记录已有结果，主题化不再追加测试。

GW-002实现准备STATIC_CONFIRMED：Plot.GetAdjacencyYield基础读取已有工业实机先例；HD/JNR的MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD有著作Faith+4、七类Science+2先例，可逐作品/按原yield追加。公式按yield分别sum(base)*0.5，先保留浮点；不同于RES-004的全非Campus Actual范围，不复制城市总量或政策倍率。原生半点YieldChange及与GW001/主题化的实际关系尚未验证，不静默用城市补贴替代。

DESIGN_DECISION_REQUIRED：当前Spec GW003/OPEN08明确保留GW002范围，Architecture亦保留GW002遗物未决；需确认GW002采用同七类作品(含Artifact、不含Relic/Product)、专业区域范围是否所有已完成RequiresPopulation区域且含Theater/特色替代，以及保持原yield种类还是转Culture。尚未接收益、未改Design或Mod，运行仍83。准备报告见../Reports/Technical/Specialization_GW002_Implementation_Preparation.md。

### 历史：主题化测试准备（用户要求到此为止）

主题化下一小批次已准备，运行仍B059.83无需新部署。STATIC_CONFIRMED（静态而非实机）：本机Building_GreatWorks中Oxford为两个Writing槽，UniquePerson=1/SameObjectType=1/SameEras=0、C/T主题倍率100。现有奥维德/紫式部两著作可作为最小候选，移入原Culture4城市的Oxford后由原生UI/IsBuildingThemedCorrectly确认；不需新收集艺术作品。原版GreatWorksOverview.lua 267等调用同一主题判定API。

USER_GAME_TEST_REQUIRED：若原城可建Oxford，Cheat完成后同城移入两著作，确认主题化>=1/未知0；固定收藏OFF→Record GW baseline截图，TEST100→Read截图，最后AUTO。优先读取“其中作品C/T”主题化小计；若无现成Oxford且无法建造，不强求，留待其它现成合格主题化集合。仅两图，不重复非主题化/城市率测试。详细候选算法与判据见[主题化测试](Validation/Specialization_B059_Theming_User_Tests.md)。

B059.83四张实机图：T16 OFF人口5，作品5C/20T、整城122.5；T17 TEST100人口6，10C/25T、整城133.4961；T18 OFF人口6，5C/20T、整城127.2461；T19 AUTO15人口6，5C/20T、整城127.2461。USER_GAME_TEST_PASS限定：本组跨回合作品与城市产出率响应/撤销、AUTO恢复。T17→T18城市减少6.25，与作品减少5×隐含1.25倍率吻合；倍率来源未独立核对。T16→T17人口增长混入差值，不要求回落T16基线。

T17原生城市面板127.2与报告133.4961不一致，保留UI显示刷新差异，不能指定内部缓存机制。四图未显示Record基线对照行，本组人工计算足够，不要求补拍，不标基线按钮实机PASS。themed0，主题化、对外累计旅游/全国文化入账仍未验证。不追加本组重复测试；下一项仅现成主题化收藏对照。源码/运行保持B059.83，Design D0022不变。详见[结果](Validation/Results/Specialization_B059_83_City_Rate_User_Result.md)。

### 已完成本组：B059.83城市率验证准备

B059.83只读对照已准备：Record GW baseline保存本UI会话中选中城的turn/作品C/T/城市C与收藏所在建筑/主题状态签名；后续读数自动显示差值及条件变化警告。增加主题化建筑作品C/T小计，隐藏已完成的两个Boost按钮，现有25/50/100/OFF/AUTO保留。基线读取不切换实验状态、不写游戏Property/收益，读档丢弃基线。D0022和收益/SQL/后台传输不改。

LOCAL_SIMULATION_PASS：真实UI读取计算同回合/跨回合差值，收藏/主题变化警告，原请求/实验档/SQL回归。USER_GAME_TEST_REQUIRED：当前两著作城先OFF并过一回合，再Record GW baseline截图；100并过一回合Read截图；OFF再过一回合Read截图，固定人口/专家/建筑/政策，若变化按报告仅作观察不强归因。这是城市产出率更新验证，不等同全国市政进度/对外累计旅游入账验证。现成主题化集合可另作固定收藏OFF baseline/100比较，若无不强求。详见Validation/Specialization_B059_Settlement_User_Tests.md。

### 已确认：B059.82非主题化作品读数

B059.82四张截图已复核：OFF 5C/20T，TEST100 10C/25T，TEST25 5C/20T，TEST50 7C/22T。均同turn13/同城327684、Culture ACTIVE4、两著作、D2、theme0，后台scan3/send7/IDLE不变。USER_GAME_TEST_PASS仅覆盖这组非主题化作品原生读取的百分比生效/档位替换；不是整城最终文化、旅游结算、theming或读档全覆盖PASS。

四组严格吻合额外值floor(2p)+floor(3p)，C=5+额外、T=20+额外；25%额外0而非floor(5×25%)=1，支持逐件量化而非全城合计后floor。100%旅游25而非40，支持按基础追加、与现有旅游倍率加算，不乘现有20。具体引擎内部先后顺序无法仅凭这组读数唯一确定。AUTO15%的零变化与逐件截断吻合，不再视作接口不生效。无补偿、无改15%公式。

整城文化四图均108.2656：同回合整城总量未随作品读取变化，原因尚未验证，不静默归为已证实UI延迟。本轮不再要求重复百分比测试；后续正常跨回合时观察总量、现成主题化集合OFF/AUTO作为余项。若尚未恢复AUTO，用户点击恢复即可，无需截图。证据与计算见[结果](Validation/Results/Specialization_B059_82_Percent_User_Result.md)。运行仍82、源码/Design不变。

### 历史：B059.82百分比待测（本组读数已回报）

B059.81截图已显示Culture ACTIVE4、合格2件、creator D2、配置15%、后台IDLE；用户确认AUTO可读，初始化/配置链路在该存档USER_GAME_TEST_PASS。两图均AUTO、原生作品5C/20T、整城108.2656C、theme0，不能当OFF/AUTO对照或收益PASS。

B059.82按用户要求新增本城临时TEST +25/+50/+100按钮；互斥替换AUTO载体，不累加，仍Culture ACTIVE4及合格类型门控。OFF清除实验、AUTO恢复D0022公式，读档清理实验并恢复AUTO。D0022、正式SQL D档、后台事件机制不改。LOCAL_SIMULATION_PASS：14修正/测试档、125/150/200参数、真实请求、幂等/切档/资格撤销/读档清理及回归。实机百分比结算仍USER_GAME_TEST_REQUIRED。

下一用户批次见[大百分比对照](Validation/Specialization_B059_Percent_User_Tests.md)：固定当前两著作及建筑，OFF→100→OFF先确认大差值；再25/50，每档读取一图。若100无变化只过一回合复读一次并停止；不继续盲测，需区分刷新/作用域/原生倍率合并。

### 历史：B059.81待复验（初始化已恢复）

B059.80实机仍未初始化，用户创建新著作也未恢复。截图Game ACK0/NO_PACKET，UI scan1 send1 retry0、API=true、reason GreatWorkCreated；当前作品3/文化8/旅游32，theme0。发送返回true不等于Gameplay送达；空后台Context计时回调未产生重发，80模拟覆盖不足，不能称根因已修复。

B059.81取消SetUpdate依赖，通用引擎事件仅对pending原包做最多两次重发（每三次事件一次），不扫描收藏；空闲/超时停止。真实收藏事件在超时后可重建最新样本，读档/回合恢复保留。公共Gameplay请求入口在校验前登记接收计数/Action/玩家和收藏包Seq/字节数，报告区分未进公共入口与未进Receive。D0022/SQL/倍率未改。

LOCAL_SIMULATION_PASS（不是实机通过）：不执行任何计时回调，通过实际Gameplay request函数而非绕过入口直接Receive；首包丢失恢复、两次重发上限、百次空闲事件零扫描/发送、超时后新作品事件恢复、GW_READ入口及既有初始化/收益回归。实机传输具体失败原因仍待新入口证据，USER_GAME_TEST_REQUIRED：同存档主菜单重载81，点击Read Great Works；若仍失败只回传一张，无需再创作或移动作品。

### 历史：B059.80计时重试（已替换）

B059.79用户截图确认Game ready=false、ACK=0、received=NONE/NO_PACKET，而UI扫描1/发送1/WAIT_ACK：数据尚未进入Receive，不能把上轮Init保护当作已修复根因。记录USER_GAME_TEST_FAIL（仅初始化）。B059.80为等待确认的同一包增加两次、间隔两秒的有界重发；复用原payload/seq，零额外收藏扫描；ACK或两次用尽即清除计时器，失败保留ACK_TIMEOUT并等待下一回合。API返回值展示，nil不冒充送达；具体引擎丢包原因尚未证实。既有事件采集、公式、SQL/D0022不变。

LOCAL_SIMULATION_PASS：首次静默拒绝后自动恢复、两次上限、无额外扫描/超时空闲、迟到ACK不叠加、同步发布重入，以及79初始化故障与既有回归。USER_GAME_TEST_REQUIRED：主菜单重载原存档，确认B059.80，等待约5秒后Read Great Works；只需一张报告。恢复后才继续OFF/AUTO收益测试。详见[传输恢复记录](../Reports/Technical/Specialization_B059_Transport_Recovery.md)。

### 历史：B059.79初始化保护（保护保留，实机未解决接收）

用户确认78性能恢复，当前观察范围USER_GAME_TEST_PASS；截图仍Game未初始化/scan2 send2 WAIT_ACK，收益未测，见[结果及建筑加成条件](Validation/Results/Specialization_B059_78_Initialization_User_Result.md)。B059.79补齐无城市集合玩家Init guard，ACK在初始化前登记，初始化失败显示具体错误和接收状态，不再只给笼统pending。UI事件驱动/单请求防风暴保留，不改SQL/公式/D0022。

LOCAL_SIMULATION_PASS：新增无城市集合玩家初始化、故障注入失败有ACK/错误、后续事件恢复、generation拒绝诊断；78空闲零扫描/异步防重发和既有收益回归保持。实机具体根因尚无Lua日志确认，不能宣称已经游戏修复。

USER_GAME_TEST_REQUIRED：主菜单重载同存档，确认B059.79，不先点AUTO，Read Great Works应出现Culture ACTIVE、D、配置；成功后在现有高阶剧院建筑条件下继续OFF/AUTO两图，保持收藏/专家/建筑不变。若仍未初始化，只回传这一张完整报告，新增Game ready/ACK/received/stage/generation/error字段足以区分未收到/拒绝/初始化失败。不重开局、不拆建筑、不重测已恢复性能，除非再次出现异常。

### 历史：B059.78待测（性能已回报，当前是初始化恢复）

用户在未开始B059收益测试前报告卡顿/持续刷新声音，收益测试尚未执行。静态确认77后台确有通用事件+两秒全城扫描；异步ACK未到即按序号不一致重发的缺陷可在本地延迟确认条件下解释风暴风险，但未凭截图/日志确认声音必来自本模块。已修复B059.78：事件标dirty、无周期扫描、in-flight阻止重复请求，初始化/读档与回合恢复保留。

LOCAL_SIMULATION_PASS（非游戏通过）：数百通用刷新空闲零扫描/发送、延迟ACK期间不重发、事件合并、同收藏重复通知不写、总督变动、下一回合有界重试及B059全部回归。新当前入口DevelopmentTests/test_b059_event_refresh.py；旧同步UI测试冻结保留，不把旧周期模型当当前要求。D0022/SQL/收益不变。

USER_GAME_TEST_REQUIRED：先确认性能再继续原B059收益测试。退出到主菜单重载同存档（确保B059.78）；无操作停留约15秒，应无持续刷新声音；两次Read Great Works之间无作品/总督/城市/回合变化，事件后台扫描/发送计数应不持续增长。再移动一件巨作，确认D/配置正常更新；只需口述是否恢复顺畅，异常回传两次报告。原三项收益/theming测试暂缓到此修复正常后，不重复开局。

### 历史：B059.77初始待测（其刷新策略已被修复）

已部署B059.77 / modinfo77，103文件，source/runtime SHA256一致：`569dfb1ba6b6846be7eee5511dfef08b9c0f782b16d225e2b5b5dd97b51fa5f2`；未启动游戏。

B059.77 / modinfo77自动时代对话已实现，D0022不变。原始creator era去重→15×max(0,D−1)→七类原生Culture/Tourism ScalingFactor；只对Culture ACTIVE4，后台无需开面板/巨作界面，读档重建/作品移出/总督降级撤销。旧最高基础值报告停止使用，GW002/其它能力/Boost不改。

STATIC_CONFIRMED：SQL按加载Era总数生成，不设7时代上限；各D14项Modifier，115/130等为百分比系数。LOCAL_SIMULATION_PASS：实际Lua/SQL、creator与work时代冲突/文物例外、类别排除、D9=120%、后台自动初始化、同档幂等、移动降档、总督资格、OFF/AUTO、重载/过期/重复样本拒绝，以及B058/B055/B054/B052/B051回归。它们不是实机收益通过。

USER_GAME_TEST_REQUIRED：[B059三项小批次](Validation/Specialization_B059_User_Tests.md)：普通固定收藏OFF/AUTO、读档与最高时代移出/资格撤销、主题化固定收藏OFF/AUTO（若无现成收藏可后验）。不重发Boost测试。原存档优先；若报告明确DIALOGUE_DATABASE_MISSING，回传一张即可，不用对缺载体继续验算。完成本地工作后等待用户结果。

### 历史：B058/D0022同步阶段（以下当时描述不覆盖上文）

D0022已接受/同步：时代对话统一百分比15%×max(0,D−1)，D为创作者时代；文物按用户明确例外用自身历史时代。固定yield/CityCenter固定旅游追加及旧逐件补差均退出当前任务。运行仍B058.76 / modinfo76，source/runtime hash不变；新百分比能力尚未接入，旧Read Great Works差额报告已过期，不要求复验。

STATIC_CONFIRMED：本机286种非文物合格作品有伟人关联，25种文物无关联；28条著作作品Era与伟人Era不同，已改用正确关联口径。Culture与Tourism各自有ScalingFactor的原生先例，+15%映射115，不是15。此证据不等于本Mod新效果或theming实机PASS。

下一实现：按新Era集合计算D，七类统一百分比、ACTIVE4门控、事件/读档重建与降档撤销；只在末端配置一个当前百分比档，不按作品重复叠加。theming原生结算USER_GAME_TEST_REQUIRED，待新探针可运行时做固定收藏OFF/ON（非主题化/主题化）两组。当前用户无需开游戏，文物例外已决定无待答问题。GW002与其它能力未改变。

### HISTORICAL NOTES：D0021及更早（以下当时方案不覆盖上文）

D0021已接受并同步Architecture：时代对话每件k×max(0,D−1) Culture/Tourism，k=1，D为本城合格作品不同创作时代数；旧最高基础值逐件补差正式废弃，停止单件setter/强制主题化模拟研究。当前Mod仍B058.76 / modinfo76，源/运行hash不变。Read Great Works里的旧补差计划现为过期探针，不再要求用户测试；下一实现应替换，不把旧显示当新效果。

STATIC_CONFIRMED：原版GreatWorksOverview以GreatWorks.EraType展示时代/比较文物主题，本机311种合格文化work type均有EraType。Culture统一YieldChange接口已有B055单件实验依据；统一Tourism固定点数尚未证实，ScalingFactor不是固定点数。theming自然关系仍USER_GAME_TEST_REQUIRED（未来探针就绪后最小同一收藏OFF/ON比较），当前不要求用户操作未实现按钮。详见[研究及未来测试](../Reports/Technical/Specialization_D0021_Dialogue_Across_Eras.md)。

下一实现优先D读取与统一Culture，独立验证固定Tourism追加；可能用仅City Center的district tourism flat总量承接，必须验证只有一个目标且记录theming不参与的实际表现，不假装按作品内在数值写入。缺失/未知Era报告，不用玩家时代猜测。GW002与其它CultureIV不改，既有BoostPASS不重测。

### HISTORICAL NOTES：D0020及更早（以下旧技术阻塞已被新设计取代）

已部署B058.76 / modinfo76，98文件，源/运行SHA256一致：`efb2363a44ef151f95989da8ea080775f03d7f33fe02aa4495336482c7616719`。当前测试入口DevelopmentTests/test_b058_boost_gw_basis.py通过（本地证据）。

D0020本轮追加：遗物与产品排除保值；文物仍适用。B058.76计划读取只比较文化类Culture/Tourism，不再要求遗物测试。只读数据库遗物4Faith/8Tourism一致；不推导未来所有Mod遗物均相同。以下D0019遗物组描述保留为本轮较早过程，不覆盖此段。倍率/主题化后端问题仍待技术实现。

B057三张图复核为USER_GAME_TEST_PASS（用户实机明确整数写入0/2/4），见[结果](Validation/Results/Specialization_B057_Integer_User_Result.md)：测绘203/215/227、法学725/768/812，差值满足整数百分点，最终进度尾差不足1。不重发本项测试，不外推截图未覆盖的重复/OFF/重载。

B058.75正式网络已接最终一次floor(FinalRaw+0.5)，k/L/N/topology不变；Raw与Applied分别报告。LOCAL_SIMULATION_PASS：真实Lua去重、同整数复用、降级/旧载体清理/重载、整数目录、此前回归；不等于正式自动新组合全部实机通过。下一正常测试顺手观察Raw≈5.657→Applied6即可，不新增完整Boost数值批次。

D0019用户确认文化组Culture/Tourism及遗物组Faith/Tourism各取最大，作品专属倍率和主题化必须适用。旧GW时代与两项设计问题已关闭；当前技术问题是逐件不同差额如何保留作品原生倍率。已实现只读基础采集/逐件计划，Read Great Works可显示，无正式巨作补贴。STATIC_CONFIRMED只发现按类型的原生GreatWork加成先例，未证明单件参数可用，不能据此宣称绝对不可实现。正在研究，不以普通城市加产代替用户要求。

可选最小新增读取：原文化IV城放两件基础不同的文化巨作，Read Great Works截一张；若方便移走最高作品再读一次，目标应立即按剩余作品重算。这里仅验新基础/差额读取，不声称效果上线；不需要重复旧+2C实验。遗物不足两种基础时显示应补0正常，不强求额外开局。下一步继续单件补差与主题化后端研究，无新设计决定要求。

### HISTORICAL NOTES：B057及更早（以下当时状态不覆盖上文）

B057.74已部署：95文件，源/运行hash一致 `6db4eb5d2e10bab6acccae8d0e968788939707e0b1a10b72d0849fdac1d086f6`，不代表用户实机已通过。

D0018明确最终一次floor(FinalRawBoost+0.5)，取代D0017接受原生截断策略；实机观察历史不倒改。B057.74为最小整数接口实验，尚未正式切换自动网络量化。默认自动仍B056正式权重/原生小数处理，等待用户要求的整数实测后替换；实验入口临时替换两类网络Boost，不叠加。0/Raw1.5→2/Raw3.8→4/恢复自动共4新按钮，共12个工作按钮，巨作保留原手动对照。

STATIC_CONFIRMED：新SQL明确Amount整数2/4，镜像HD提示参数同值，D0017冻结hash一致。LOCAL_SIMULATION_PASS：显式半向上、末端量化反例、3.6/3.9同整数幂等、旧效果撤销/零/恢复/重载/缺表门控及既有回归。两者都不是实机。USER_GAME_TEST_REQUIRED：[B057同存档三分支](Validation/Specialization_B057_User_Tests.md)，含零对照与两项整数输入，只需三张报告；不调整拓扑，不再研究引擎保留小数。原存档优先；若新增SQL定义未载入，停止该次测量并回传提示，不默认必须新局。

GW-001新设计已登记：本城文化类组/遗物组各自最高基础值补齐，产品不适用。旧时代标准/曲线OPEN被取代；本轮没有实现或派发新的巨作收益测试，旧GW按钮不代表新玩法。多yield排序/遗物具体yield维度/倍率、GW002遗物范围尚待后续明确，不阻塞本轮整数测试。下一步先等B057原生整数结果，再将量化接入正式自动网络，不自行修改k/L/N/Entertainment参数。

### HISTORICAL NOTES：B056及更早记录（以下当时状态不覆盖上文）

B056.73 / modinfo73已恢复正式1/2/3/4权重并部署，k_R/k_C仍独立为1，内部浮点原样交给原生Modifier。1032组SQL/Lua配置、实际Lua网络状态与既有折扣/模板/复制回归为LOCAL_SIMULATION_PASS（非实机）；HD巨作标准表为STATIC_CONFIRMED（非实机）。D0017及其hash不变。没有扩大B055用户测试PASS范围；不再派已完成的小数截断测试。正式配置在旧存档中的数据库/既存Modifier更新行为未新增实机证据，不能仅凭新报告权重证明旧存档实际数值已变；后续收益测试使用明确匹配版本的新局或单独核对，不要求现在为此开局。

当前下一项：巨作自动保值的时代口径、无标准类别/时代、旅游业和主题化等倍率规则仍DESIGN_DECISION_REQUIRED（GW-001/003）。已找到HD专用标准表42行；不从特殊著作反推曲线。用户已收到“玩家当前时代＋HD表＋缺表暂不补贴”的候选问题，尚未收到选择，此候选未生效。古代/未来缺标准，尤其未来时代停补贴可能导致回落，须明确决定是否沿用最近已定义时代；文物18/18独立，遗物/Product不在表。GW002适用清单与倍率也未擅自决定。当前不新增用户实机测试。

本轮变更/研究与验证命令见[B056报告](../Reports/Technical/Specialization_B056_Formal_Boost_GW_Standards.md)。运行包94文件，SHA256 `d13b986f93d6b219c24a802525b29f1ddd8c96c446b710c3e4af58d0454c4a89`；部署前后hash核对，UUID不变。没有启动游戏、修改Design或提交Git。

### HISTORICAL NOTES：此前轮次说明（当时“当前/下一轮/待测”不覆盖上文）

B055同目标T1/T2/T3已复核：[计算与结果](Validation/Results/Specialization_B055_Same_Target_User_Result.md)。法学790/747/790、测绘239/209/245；实际差值支持额外百分点先舍去小数再影响进度。按D0017接受，不补偿，测试范围内自动应用/总督降级/新增recipient为USER_GAME_TEST_PASS。基础34%×当前成本的绝对偏差仍单独记录，不能全部归为截断；不再为已确定的小数平台重复派测试。当前用户无需操作。运行仍B055.72临时权重，下一开发轮显式恢复正式1/2/3/4并按GW后续边界推进，非本次验算自动部署。

已完成的用户测试为[现有网络同目标三分支](Validation/Specialization_B055_Same_Target_Tests.md)：测绘600/法学2160，共同预Boost存档S；T1当前N2、T2仅降级总督、T3恢复S后追加首都→D使N3。无需首都投资或重复随机科技测试；共3报告。该三分支现已回报，取整证据及PASS边界以上述最新结果为准，不强制凑绝对理论数值。巨作稳定单件对照已通过，不重发。仅新增测试计划/状态，运行B055.72不变。

B055巨作第二批4图已复核：[稳定对照结果](Validation/Results/Specialization_B055_GW_Stable_User_Result.md)。全程2专家、单件著作；OFF/OBJECT/CITY/OFF跨回合整城23.3164→25.5156→25.5156→23.3164，约+2.2符合+10%城市倍率，作品文化2→4→2→2，旅游业恒3。该单件后端加成/撤销为USER_GAME_TEST_PASS，不重发本项测试；多件移动/读档/theming仍未确认。用户提出Boost分项取整假设已复算：能解释砌砖，不能统一解释全部6项，精确数值仍待后续对照。该轮未新增操作要求；随后用户已指定可用目标，本轮测试以顶部同目标计划为准，源码/运行保持B055.72。

B055首批8图已复核，见[逐项验算](Validation/Results/Specialization_B055_First_User_Result.md)。HD本机基础Boost=34（STATIC_CONFIRMED）；L/N配置变化有用户实机证据，同成本科技升档多18进度，与整数3→6的假设吻合。但全部样本不能由34+floor(extra)统一解释，不把精度合同判为PASS、不补偿。巨作四图显示读数/城市栏不同步且首尾OFF基线不同，该首批B055-3当时未能判定，后续稳定单件对照已由上文通过；作品类型/数量与旅游业3已读。B055-4及Boost重载未获本次结果，保持待测。本轮只验算/记录/归档，运行仍B055.72、D0017不变。

B055.72已准备下一批原生测试：Research/Culture网络自动配置额外Boost，使用用户要求的临时1.1/2.2/3.3/4.5权重；巨作提供手动city/object对照。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS是本地证据；原生Boost数值、撤销与巨作展示均USER_GAME_TEST_REQUIRED，不能用配置读数判定实际生效。测试见[B055四项小批次](Validation/Specialization_B055_User_Tests.md)。本批部署后停止，无自动接受GW曲线/最终封顶。

B054.71用户明确确认全部批次通过：等级变化、自动选择最高等级、模板并集去重、撤销与重载均为USER_GAME_TEST_PASS，见[用户结果](Validation/Results/Specialization_B054_User_Result.md)。先前70的未初始化失败及71修复调查保留历史证据，不再作为当前待测/阻塞。无新增截图或完整双币价格对，不外推全部建筑、货币组合及商路生命周期。

B052用户口述人工PASS，见[结果](Validation/Results/Specialization_B052_User_Result.md)；按钮冲突后的重启与本批正常路径按用户确认关闭，无新增截图/数值，不外推所有获取方法或征服。B053已由用户人工确认通过，粮仓折后190的尾数可接受，见[B053结果](Validation/Results/Specialization_B053_User_Result.md)。当前B054已接入自动网络模板并集、最高ACTIVE折扣与后台Gold资格检查。D0017已允许货币隔离困难时同一合格建筑Faith同步折扣。B054当前批次已关闭，不重发；当前仅需本页B055新测试。

当前Git基准已建立；B052按Accepted D0015实现标准化永久模板记录、一次补录与建筑事件增量，新增只读报告；此记录层本身不改变购买资格；B054另行接入可撤销折扣。当前四专业Lv1–3主体、科研/文化IV专家百分比、科研/工业IV固定复制、投资与Crew已有运行实现；不是“全部P0仍只读”。整体v0.1未完成，不给虚构完成百分比。

B051.67最小补测已由用户口头确认通过，无图/数值，见[B051.67结果](Validation/Results/Specialization_B051_67_User_Result.md)。本轮派发的扩展非学院区域复制与固定条件下无持续增长验收已关闭；未列明区域、旧完整三案和所有组合不随之升级。[标准化候选目录](../Reports/Technical/Specialization_Standardization_Catalog_Candidate.md)已整理：167栋/17类区域，其范围已由D0015确认；候选导出仍保留为调查快照，不作运行白名单。B052运行时读取HD分类，自动折扣B054.71已按当前批次实机通过。

用户报告B052按钮未出现：Modding.log确认游戏加载Mods内的旧版备份（同UUID），不是B052账本已失败的证据。已将备份完整移出扫描目录并修复部署工具；B052包字节不变。用户随后口述PASS，此按钮阻断已关闭。见[部署冲突修正](../Reports/Technical/Specialization_B052_Deployment_Collision.md)。

## 验证等级

STATIC_CONFIRMED=源码/数据库静态证据；LOCAL_SIMULATION_PASS=本地模拟，均不代表引擎通过。USER_GAME_TEST_REQUIRED=待用户游戏验证；USER_GAME_TEST_PASS/FAIL=用户已实际验证的明确场景。BLOCKED=无法继续而需技术突破/设计决定；DEFERRED只是延后，不是假失败。配置载体正确不等于原生产出正确；截图与口述分别标注。

## 当前实现与验证矩阵

当前进度由上方CURRENT及[E2当前切片](../Architecture/v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)管理。B108新保存authority为STATIC_CONFIRMED / LOCAL_SIMULATION_PASS，原生三城检查仍待验收；其它能力进度沿用各自批次证据，不以早期矩阵重置。

## 历史实现与验证矩阵（早期baseline，非当前派工）

| 模块 | 当前实现 | 已有证据及局限 |
|---|---|---|
| 独立文明、City Property、总督/专家基础接口 | 运行 | A1/A2及新局总督present/established/2–4门槛、实际工作专家按用户确认通过；旧证据见历史快照 |
| 新城完成→身份、正常读档 | CityFlow/B020–21运行 | [B020](Validation/Results/Specialization_B020_User_Result.md)、[B021](Validation/Results/Specialization_B021_User_Result.md) USER_GAME_TEST_PASS，含Cheat同回合完成；不是无历史旧城自动初始化或极端丢写恢复 |
| 移民投资/ACTIVE | 运行至Potential4，单位面板准备/确认 | [B033](Validation/Results/Specialization_B033_User_Result.md)、[B035](Validation/Results/Specialization_B035_User_Result.md)、[B043](Validation/Results/Specialization_B043_User_Result.md)用户证据，含上限拒绝与总督门控；不宣称完整征服继承 |
| Research/Culture/Commerce Lv1 | 自动运行 | [B024](Validation/Results/Specialization_B024_User_Result.md)用户通过；新城、建筑、多个专家与不更改既有专业按回报范围 |
| Industry Lv1 | 自动Base相邻专家支持 | [B036更正](Validation/Results/Specialization_B036_User_Confirmation.md)用户确认通过：额外2P是原生工业专家基础，不应扣掉 |
| 共同Lv2住房、基础GPP | 自动运行 | [住房](Validation/Results/Specialization_B034_User_Result.md)、[GPP](Validation/Results/Specialization_B035_User_Result.md)用户通过；百分比组合只支持已测情况；已接受延迟见技术索引 |
| 四专业Lv3 | 支持档位、科研/文化人口奖励、工业BaseP/Gold、商业网络类型奖励运行 | [B037修复通过](Validation/Results/Specialization_B037_Promotion_User_Pass.md)、[科研](Validation/Results/Specialization_B038_Population_User_Result.md)、[文化](Validation/Results/Specialization_B038_Culture_User_Result.md)及用户其余正常回报；不擅改0.5 |
| 后台商路/网络拓扑 | 全集后台桥接、direct/recipient分开，无需开UI | [B026历史](Validation/Results/Specialization_B026_User_Result.md)、[D0009 direct接收](Validation/Results/Specialization_B027_User_Result.md)、[删目的城撤销](Validation/Results/Specialization_B031_User_Result.md)通过；自然完成/战争/掠夺等不据此全通过 |
| Crew五项目/单位/目标/确认/限额注入 | 运行，五档、速度整数、排序与UX已落实 | [B043](Validation/Results/Specialization_B043_User_Result.md)、[UX](Validation/Results/Specialization_B045_User_Result.md)、[快速速度澄清](Validation/Results/Specialization_B046_User_Clarification.md)等用户结果；B048用户通过。不能据一级/五级实测外推所有速度全部档位 |
| Research/Culture IV专家百分比 | 运行 | [B048](Validation/Results/Specialization_B048_User_Result.md) USER_GAME_TEST_PASS；不是Culture全部IV完成 |
| Research/Industry IV固定复制 | B051.67运行 | [B051.66结果](Validation/Results/Specialization_B051_66_User_Result.md)工业4.5P/科研标准区域半点通过；旧范围错误修复后的[B051.67最小补测](Validation/Results/Specialization_B051_67_User_Result.md)用户口头通过；无截图/数值，不外推全部区域组合 |
| 标准化模板 / 购买折扣 | B052账本；B054后台自动网络折扣 | B052/B053用户口述通过；B054.71 USER_GAME_TEST_PASS：等级变化、最高等级、并集去重、撤销/重载。D0017允许必要时双币折扣，不开放购买资格 |
| Research/Culture Boost | B058正式k=1、Lmax、sqrt(N)、最终一次floor(x+0.5) | 用户整数接口实测通过；保留最终封顶OPEN-06，不再使用B055临时权重或D0017旧隐式截断 |
| Culture IV两项Great Work效果 | B059时代对话百分比；B060逐作品BASE相邻均运行 | 已有原生C/T及主题化对照；用户停止主题化深挖。GW002用户全部PASS，逐件半点截断按D0024接受；旧逐件保值退出 |
| Commerce IV汇聚 | B062独立direct/max/total/20%/floor | 本批Science及拓扑/撤销USER_GAME_TEST_PASS，C/P用户接受暂缓实测；不重发固定5测试 |
| 通用ELIG / Conquest Claim与跨Owner继承 | B067所有权隔离；ELIG/Claim暂缓 | 用户确认自建不易主范围；B066无确认转移登记的历史失败保留，不派补测 |

## 下一任务（只有此队列有效）

等待CURRENT所列B108三城新局结果；按[E2当前切片](../Architecture/v2/P0_E2_Plan.md#current-slice--recovery-and-action-routing)核对、归档。下一玩法实施需单独授权，不自动进入snapshot/Claim/F。

## 历史下一任务（已被CURRENT取代）

1. 等待用户提供界面整理要求；保留可访问诊断入口，先不改布局。
2. 按UI要求完成玩家信息/诊断分层与日志策略，整理当前版本说明、已知限制、默认自动模式及实验开关可见性。
3. 用户在游玩中验收并回报具体问题；不追加大批整体验收。checkpoint/commit/push须单独授权。
4. FUTURE / DEFERRED：累计32次建城绑定限制、通用ELIG、所有权继承/Conquest Claim。B067已隔离所有权模块，不继续B066测试。所有Future专业不进入本轮。

## 历史 BLOCKED / DESIGN DECISION REQUIRED / DEFERRED

以下是早期baseline登记，当前未决及支持范围以CURRENT链接的切片和正式Design为准。

- DESIGN_DECISION_REQUIRED：Spec OPEN-06 Boost最终封顶、OPEN-04 Claim精确成本仍保留，不阻塞本次只读调查。Boost最终量化已由D0018解决，GW规则由D0022–24解决，不再列旧时代保值/范围待决。
- IMPLEMENTATION_LIMITATION：跨Owner稳定身份锚点/完整Conquest、旧档缺史初始化、通用资格与多人一致性未完成。固定复制整数/半点支持边界不变。
- DEFERRED：B010及未覆盖的自然结束/战争/掠夺，不把删除城市等同所有生命周期。商业C/P用户暂缓独立实测；第三方间接收益回路未普遍证明。
- NO_FIX / NO_ADDITIONAL_TEST：住房/GPP/商业城市面板刷新延迟已接受；GW002逐件半点截断接受。不能以此掩盖真正未生效。

## 交接与证据

[技术索引](../Reports/Technical/README.md)、[交接审计](../Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md)、[测试运行](../../DevelopmentTests/README.md)。测试原始结果冻结，纠正写新结果。ScreenShots仅待投递，不代替Evidence；用户无图但明确口述可按范围记PASS。

[此前S0115全文](../Historical/DocumentSnapshots/Specialization_P0_Status_before_fresh_agent_handoff.md)保存早期A001–B051矩阵、每批历史及完整证据索引；该文件所有“下一项/待测”均为历史，不与本队列并存。

## Phase 1停止点（历史）

Phase 1/2已由用户审核完成并建立GitHub initial baseline；以上迁移阶段文字为历史。当前B051.67最小补测已口头通过，下一任务以本页当前队列为准；B054当前批次已通过；新增实机要求仅见当前队列B063。旧Evidence、ScreenShots、DevelopmentBackups均为外部只读审计材料；路径映射见../Reports/Proposals/Phase1_External_Materials.md。
