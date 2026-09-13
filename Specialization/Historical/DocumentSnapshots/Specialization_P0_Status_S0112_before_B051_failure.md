# Specialization P0 Status

Document Owner: Codex
Status Revision: S0112
Implementation Build: P0-B-051 / modinfo65
Architecture Revision Reviewed: A0108
Design Revision Reviewed: D0013
Latest Accepted Design Revision: D0013
Design Sync State: SYNCED_WITH_LIMITATIONS
Work State: USER_GAME_TEST_REQUIRED

## CURRENT AUTHORITATIVE STATE

用户已授权恢复实施；当前运行B051/modinfo65。先完成原研究清单A组，两项50%自动复制，标准化仍是下一工作包，不声称本轮全部v0.1完成。

| 当前项目 | 验证状态 | 范围/下一步 |
|---|---|---|
| B050独立半点实验 | USER_GAME_TEST_PASS | 用户3/4人口及−1宜居度五图范围；不重发原批次 |
| B051自动复制源码/80载体/加载引用 | STATIC_CONFIRMED | 静态证据，不等于游戏通过 |
| B051真实Lua+后台mock | LOCAL_SIMULATION_PASS | 重复/重载/撤销/max/255人口数学/丢请求重试；不等于实机 |
| B051科研本地/工业跨城实际收益 | USER_GAME_TEST_REQUIRED | 仅[当前三案](Validation/Cases/B051_Automatic_Copy_Yields.md) |
| 任意细小数/非标准区域范围 | IMPLEMENTATION_LIMITATION | 不取整、不发放部分科研小计；若遇到需单独处理 |
| 标准化账本与Gold-only折扣 | 后续待办，未实现 | D0013触发/补录已决定；允许范围与原生价格隔离继续处理 |
| Boost / Great Work / Commerce IV / 通用资格与征服 | 后续待办 | 见既有剩余研究；B051不扩大完成状态 |

本轮报告：[B051实现与边界](../Reports/Technical/Specialization_B051_Automatic_Copy_Yields.md)。未启动游戏；B010不恢复，不派旧通过批次。

### HISTORICAL NOTES / 以下原“当前”描述仅为阶段记录

**B050已通过：** [五图精确读数与口述](Validation/Results/Specialization_B050_User_Result.md)，USER_GAME_TEST_PASS限3/4人口半点组合；−1宜居度最终约0.45，4人口OFF完全回落。无新增测试，原B050批次关闭。全人口/自动人口切换/任意小数不升级为实机通过。

**D0013已确认并同步A0107：** IND-NET-004学习触发/首次补录已解决，不再待设计决定；HD明确分类+允许范围、事件增量、不持续扫描。标准化尚未运行接入，Gold-only原生效果和具体允许清单仍需后续处理。

**当前仅研究：** [剩余9机制+3集成工作包](../Reports/Technical/Specialization_v01_Remaining_Work_Review.md)，无Source/Tests/运行包改动。保留B050/modinfo64。用户无需操作；恢复实际实现需后续指示。以下此前实验待测/学习触发未决段落为历史。

**B050当前：** [固定半点独立实验](../Reports/Technical/Specialization_B050_Half_Yield_Experiment.md)，显式ON/OFF，不接正式Lv4网络收益；数学/真实模块mock/SQL为STATIC_CONFIRMED与LOCAL_SIMULATION_PASS，需[人口3与4两项](Validation/Cases/B050_Half_Yield.md)原生验证。不是恢复已失败的固定小数Amount路线，不量化设计。

**标准化研究：** [城市永久Property账本、HD Tier分类、当前网络并集](../Reports/Technical/Specialization_Standardization_Storage_Research.md)与离线契约完成。自动学习触发/旧建筑补录/范围仍需接入前设计确认；Gold-only原生价格尚未确认。没有写永久模板、没有启用折扣，不新增标准化用户测试。D0012不变，旧B049批次已关闭。

**B049批次通过，modinfo63提示整理：** [口述/截图与修正](Validation/Results/Specialization_B049_User_Result.md)。水力作坊非相邻产出读取、工业最高来源及总督调离撤销USER_GAME_TEST_PASS；不是行业实测，也不是50%正式发放通过。截图NETWORK_REFRESH_PENDING仅表示等待新鲜快照，现改简短中文，区分未接收/无四级来源/暂不可判断；不改网络逻辑。LOCAL_SIMULATION_PASS，新提示后续顺带观察，无独立测试。当前B049两项不再待用户重测。下一项精确小数承载调查。下方B049原待测安排为阶段记录。

**B049当前：** [移民UX与Lv4复制准备](../Reports/Technical/Specialization_B049_Settler_UX_Lv4_Copy.md)。移民固定原按钮位置、左侧确认，文案完成，STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；不改投资事务，用户后续顺带观察，无独立UX测试。Lv4新Read Lv4 copy是只读候选基数/50%/工业多源max，**没有启用复制收益**，需[最多两项](Validation/Cases/B049_Lv4_Copy_Basis.md)。正式固定小数承载IMPLEMENTATION_LIMITATION；不取整、不改设计。

**B048已通过：** [用户明确“B048 pass”](Validation/Results/Specialization_B048_User_Result.md)，USER_GAME_TEST_PASS限科研/文化每专家5个百分点组件，不重复该批次。以下原B048“待实机”及更早是阶段历史。

**B048：** [科研/文化Lv4每专家5个百分点](../Reports/Technical/Specialization_B048_Lv4_Percent.md)已接自动收益，本地STATIC_CONFIRMED / LOCAL_SIMULATION_PASS，原生效果需[最多三项](Validation/Cases/B048_Lv4_Percent.md)。只实现Lv4的百分比组件，相邻复制/巨作/Industry输出/Commerce汇聚/网络Boost未由本轮实现。D0012不变，施工队不重测。

**D0012接受，B047落实整数：** [报告](../Reports/Technical/Specialization_D0012_Integer_Crews.md)，STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；用户已接受floor，不再待设计决定。一级167、五级911及空花260→174由[用户补充](Validation/Results/Specialization_B046_User_Clarification.md)确认。金额和按钮显示统一为整数，项目成本/执行规则不改。新版显示USER_GAME_TEST_REQUIRED但并入后续普通测试，无新增独立批次；不得将本地改版自动标游戏通过。下方B046未决和147/五级未知项已由本段取代。

**B046口述回报：** [详细结果](Validation/Results/Specialization_B046_User_Result.md)。项目排序USER_GAME_TEST_PASS；一级167.5→实际167，精确小数投入预期在本案USER_GAME_TEST_FAIL。五档项目成本187/308/549/737/1005符合向下取整；五级只有提示911.2、实际未知；空花260→147待澄清。建议明确Crew缩放后floor，标DESIGN_DECISION_REQUIRED，尚未采用。D0011/运行B046/modinfo59均未改；没有新增测试批次，下方原三步计划不自动重发。

**当前B046：** B045按[用户明确通过](Validation/Results/Specialization_B045_User_Result.md)登记USER_GAME_TEST_PASS。[五档连续排序与精度读取](../Reports/Technical/Specialization_B046_Project_Precision.md)已本地通过；排序按用户要求不单独验收。当前仅[快速速度三步](Validation/Cases/B046_Crew_Precision.md)：五成本、最低项目重复、167.5实际注入。成本/小数引擎精度USER_GAME_TEST_REQUIRED，未擅定取整，D0011不变。原金额/生成/消费函数均未改。以下B045及更早为阶段历史。

**当前B045：仅施工队UX。** [命名/tooltip/固定确认位置](../Reports/Technical/Specialization_B045_Crew_UX.md)完成；STATIC_CONFIRMED与LOCAL_SIMULATION_PASS，原生动作栏位置/显示USER_GAME_TEST_REQUIRED（报告末尾三小步）。成本、生成、五档金额、合法范围与完整结算函数校验未改。D0011未改。用户表示Crew基本正常，本轮不扩展B044各边界的PASS、不继续项目/速度研究。以下B044及更早是阶段记录。

**当前B044/modinfo57：** B043已按[用户口述与四图](Validation/Results/Specialization_B043_User_Result.md)登记USER_GAME_TEST_PASS，提示排版单独修正。[五档项目](../Reports/Technical/Specialization_B044_Crew_Projects.md)已接运行包；源码/数据库STATIC_CONFIRMED、本地LOCAL_SIMULATION_PASS，原生项目完成生成及重载需[三项实机测试](Validation/Cases/B044_Crew_Projects.md)。D0011不变。非标准速度成本精度/浮点注入USER_GAME_TEST_REQUIRED，后续小批次；不自行取整，无新设计待决。

| 当前项 | 状态 | 范围 |
|---|---|---|
| B043单位面板与准备/确认 | USER_GAME_TEST_PASS | 用户全部正常；四图支持当前准备/拒绝，排版单独修正 |
| B044五档定义/门槛/执行 | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 五映射、25速度组合、实际Lua到mock注入；不是引擎验证 |
| B044项目生成/重复/重载 | USER_GAME_TEST_REQUIRED | 仅三项当前用户批次 |
| 非标准速度原生精度 | USER_GAME_TEST_REQUIRED | 延后专门验证，不擅自round/floor/ceil |

**以下B043及更早为历史阶段记录，不覆盖上方当前状态。**

**B042全部通过：** [口述与单图](Validation/Results/Specialization_B042_User_Result.md)。**B043** [单位面板与中文提示](../Reports/Technical/Specialization_B043_Unit_Panel.md)已部署，本地通过，[两小项](Validation/Cases/B043_Unit_Panel.md)待实机。D0011五档开放/双侧速度缩放已确认，不再作为用户待决；正式项目与精度接入下一项。

**B041奇观已通过：** [用户回报](Validation/Results/Specialization_B041_Wonder_User_Pass.md)，不重复标记测试。**当前B042/modinfo55** [独立Crew与投资入口](../Reports/Technical/Specialization_B042_Crew_Unit_Actions.md)本地通过，[三案](Validation/Cases/B042_Crew_And_Investment.md)待实机。新Crew250是DEV免费生成，真实一次消费；五项目未接。

**B041部分通过，奇观单独修正：** [用户人工结果](Validation/Results/Specialization_B041_Partial_User_Result.md)确认移民/区域/区域建筑/市中心建筑等正常，53奇观未标记。54采用[HD UI城市地块helper并由Gameplay复核](../Reports/Technical/Specialization_B041_Wonder_Bridge_Fix.md)，本地通过；根因未有错误文本确认，只派原奇观一个复验。

**当前B041/modinfo53：** [目标枚举与独立地图标签](../Reports/Technical/Specialization_B041_Target_Markers.md)已部署，本地通过，实机待[三案](../Status/Validation/Cases/B041_Target_Markers.md)。移民自动INVEST，工人显式BUILD TEST；不使用共享伟人图层、不消费、不改投资。奇观从城市地块枚举，不再只验脚下。以下B040及更早是阶段记录。

**B040已用户通过：** [单图与人工回报](Validation/Results/Specialization_B040_User_Result.md)关闭当前批次；错位奇观NOT VERIFIED正常，不要求补测。新[单位合法地块高亮调查](../Reports/Technical/Specialization_Unit_Action_Highlighting.md)找到原版/HD自算列表+UILens绘制先例，未部署。下一步目标枚举/独立Crew及动作；无新用户测试。以下待测描述为此前历史。

**B040入口不可见已修正待复验：** [modinfo52显示修正](Validation/Results/Specialization_B040_Visibility_Fix.md)。51入口USER_GAME_TEST_FAIL，不扩大为位置读取失败；52补InitHandler/LoadScreenClose根显示，入口常显并提供未选单位提示，本地通过，实机待回报。

**B040/modinfo51当前批次：** [共用单位地块读取与独立入口](../Reports/Technical/Specialization_B040_Unit_Sites.md)已部署，STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；[三小案](Validation/Cases/B040_Unit_Sites.md) USER_GAME_TEST_REQUIRED。不用P0面板，无消费/新单位/新SQL。保留旧投资动作；工人只代测施工位置，不是Crew。以下B039/本地候选说明是此前过程，B039 PASS继续有效。

**B039用户人工通过：** [结果](Validation/Results/Specialization_B039_User_Result.md)关闭建筑/区域/奇观/超额浪费与重复检查，USER_GAME_TEST_PASS限于DEV探针，无需补图或重测。运行仍B039/modinfo50，正式Crew项目/单位尚未部署。

**当前共同动作准备：** [施工队与投资地块/按钮调查](../Reports/Technical/Specialization_Unit_Actions_And_Sites.md)找到HD工人站奇观地基的直接先例；离线共用位置判定LOCAL_SIMULATION_PASS。新文件未加载，投资仍在市中心。精确位置限制为调查候选，未自动修改D0010；劳动力1模板与HD加成隔离、UI挂接、真实目标位置/消费仍待接入。本轮无新增用户测试。


**文化3人口已复核：** [三图计算](Validation/Results/Specialization_B038_Culture_User_Result.md)原生文化2.609375→6.66015625→10.7109375，每步+4.05078125，符合(原专家3+人口1.5)×宜居度90%。本场景半点人口收益USER_GAME_TEST_PASS，未发现半点丢失；1/256粒度只记观察、不定取整策略。当前设计/实现仍0.5，系数1仅未来备选。城市面板滞后另记，无需重复该测试。


**B038/modinfo49五图结论：** [科研人口收益复核](Validation/Results/Specialization_B038_Population_User_Result.md)：4人口0/1/2专家，后台原生科技11.1875→16.1875→21.1875，carrier0→2→4，按此范围USER_GAME_TEST_PASS。旧异常实际为右下角面板读数落后，旧载体残留猜测被五图否定。显示延迟记录为观察限制，本轮不修改。商业类型奖励通过保留；文化奇数人口半点现已按最新三图范围通过，科研本场景无需重复。

**B037晋升修正已用户确认通过：** [用户“更新正常”](Validation/Results/Specialization_B037_Promotion_User_Pass.md)，无需再测该顺序。


**当前B037/modinfo47：** [三图与人工结果](Validation/Results/Specialization_B037_User_Result.md)确认其余Lv3支持行为正常；旧46的先投资后晋升同回合未触发为限定USER_GAME_TEST_FAIL。已[补充GovernorPromoted监听](../Reports/Technical/Specialization_B037_Governor_Promotion_Fix.md)，静态/本地模拟通过；新监听已获用户人工USER_GAME_TEST_PASS，不重做整批。B035已接受的GPP延迟不改。

**GPP延迟已接受：** [用户备注](Validation/Results/Specialization_B035_GPP_Refresh_Note.md)：carrier4→2当回合正确，全国GPP与UI仍18、过回合变12；不定位具体缓存层，不修复、不改进、不补测。B035 PASS保留。


**当前B035用户结果：** [人工通过与投资上限截图](Validation/Results/Specialization_B035_User_Result.md)登记USER_GAME_TEST_PASS。四类GPP批次全部正常依用户人工；另确认平伽拉100%、古典共和15%、文艺赞助人效果。25%+15%=40%只记该组合实测，不推广内部算法，不追加测试。Potential/ACTIVE进阶至4及上限拒绝、不消耗移民通过；不是Lv3/4未实现能力通过。modinfo45精简面板截图已确认，收益源码未改。

**当前B036 / modinfo44结果：** [八图复核与人工回报](Validation/Results/Specialization_B036_User_Result.md)按范围USER_GAME_TEST_PASS。基础相邻1→4→6，专家总产出3F3P→3F6P→3F8P；政策使区域6→12但专家保持8P。额外2P是数据库原有工业专家基础值，本Mod仅新增BaseP；[用户已明确确认此解释并判定PASS](Validation/Results/Specialization_B036_User_Confirmation.md)。读档与网络接入/分发正常依用户明确人工回报。施工队未实现。

**待办顺序已按用户调整：** B035原延后事项现已由用户明确人工验证通过，当前无待派发B035复测；旧[B035三案](Validation/Cases/B035_Lv2_GPP.md)不再作为当前派发批次。B010与小数研究仍延后。

**D0010 sync完成：** [征服分流报告](../Reports/Technical/Specialization_D0010_Architecture_Sync.md)。已停止旧离线无专业取得shortcut，A/B/C模式契约及三组回归本地通过；原生Conquest尚未接入，不派发新游戏测试。住房与其它既有玩法未变，运行B034/42不改。

**当前结果：B034 / modinfo42。** [五图与人工回报](Validation/Results/Specialization_B034_User_Result.md)确认Research住房6→7→8→9，调离后carrier当回合归0、城市面板过回合9→6；生产操作触发刷新另依人工。按观察范围USER_GAME_TEST_PASS；同回合显示延迟用户明确接受，不阻塞。重载等未回报内容不扩大PASS，不追加补测；此B034结果不要求补测；新增GPP批次见上。

**当前结果：** [B033三图与人工补充](Validation/Results/Specialization_B033_User_Result.md)：投资1→2/正常重载、重复不扣、原Lv1及总督动态ACTIVE按范围USER_GAME_TEST_PASS；新建商路身份正确依人工，原商路跨升级保持未测。两个英文网络按钮标签已在截图确认。此为B033既有通过结果，无需补测投资；B034住房结果见上。

**当前结果：** [B031两图](Validation/Results/Specialization_B031_User_Result.md)商路3→2，分发1→0，科研N3→2、文化N2→1，中心接入各1且继续接收；目的端失效撤销USER_GAME_TEST_PASS。两处英文标签已由B033截图确认显示正常。小数与Commerce IV仍后续研究。

此前B029/modinfo36结果保留如下，当前Design D0009同步至A0076。新增显式固定收益开关实验，不是商业IV；[旧档两图+1未生效](Validation/Results/Specialization_B029_Old_Save_Failure.md)，[新局整数对照三图已通过](Validation/Results/Specialization_B029_New_Game_Result.md)，[半点实测仅+1、OFF恢复](Validation/Results/Specialization_B029_Fractional_Result.md)，本轮不重发测试。只读来源城S/C/P探针两组本地通过，现已[两图实机通过](Validation/Results/Specialization_B028_User_Result.md)：科技5.5→7.5，生产10→11，文化1.296875保持；符合城市UI显示精度。B027直接接收两图PASS保留，未修改网络实现。B031恢复可读性/撤销；B010继续延后。

已部署：标准Research/Culture/Commerce的DEV自动Lv1专家3F3P，以及限定DEV专业身份/网络状态；四类共同Lv2住房已部署，其中Research两层开启/撤销按B034范围实测通过；共同Lv2基础GPP已按B035人工批次通过。已按范围验证：限定DEV移民Potential1→2投资与ACTIVE读数；新增工业Lv1专家收益已按B036范围通过，施工队未实现。未完成：通用资格的正式门控、Lv4玩法及尚未验证边界、Commerce IV汇聚发放、Industry及其施工队/网络收益、Boost与Great Work。此前总督/专家/API探针通过不等于高级能力已实现。

商业IV已有离线计划及条件总产出研究授权，现有Spec未被自动改写；本次Getter不证明精确本地basis、20%最终增量或防循环。游戏设计意图以Accepted Spec为准，验证状态不随文档同步升级。

面板标题已在modinfo45修正；本批文档明确expected/carrier为新增量。工业诊断正文后续可进一步改为Added，当前收益不变。

待办提示优化：Lv4投资的POTENTIAL_CAP_4是预期拒绝，移民不消耗已通过；以后把堆栈移至日志，面板用普通语言说明上限，不追加测试。

## CONFIRMED

B035：USER_GAME_TEST_PASS（当前四类联合批次，证据为用户人工；百分比组合范围见结果记录）。


B034住房：USER_GAME_TEST_PASS（Research、两层、总督调离撤销及最终住房正确）；显示延迟保留用户接受的限制，见五图结果。

| 项目 | 状态 | 范围 |
|---|---|---|
| B030第二槽贡献/OFF | USER_GAME_TEST_PASS | [三图](Validation/Results/Specialization_B030_User_Result.md)：1→2→0；目标2.5中的半点未通过 |
| B029新局整数开启/关闭 | USER_GAME_TEST_PASS | [三图](Validation/Results/Specialization_B029_New_Game_Result.md)：三项+1→0；半点、UI即时刷新与旧档修复未证明 |
| B028 Gameplay城市总产出读取 | USER_GAME_TEST_PASS | [两图结果](Validation/Results/Specialization_B028_User_Result.md)：S/C/P及同回合刷新；非纯本地basis/收益应用证明 |
| B027 D0009 direct接收 | USER_GAME_TEST_PASS | [纽约/阿伯丁两图](Validation/Results/Specialization_B027_User_Result.md)：科研N3、文化N2、接收YES；非收益PASS |
| B026首都/商业中心接入、分发与读档（D0008历史范围，不符合D0009接收判据） | USER_GAME_TEST_PASS | [八图结果](Validation/Results/Specialization_B026_User_Result.md)；图6文化已接入，图7科研N=2为纽约与阿伯丁；撤销未覆盖 |
| B024自动Lv1恢复/新城 | USER_GAME_TEST_PASS | [两图及明确人工回报](Validation/Results/Specialization_B024_User_Result.md)：旧城与新城carrier正确；建筑/多专家/第二区域不改专业依人工证据 |
| B022原生Research专家收益 | USER_GAME_TEST_PASS | [三图与人工回报](Validation/Results/Specialization_B022_User_Result.md)：专家2科技/3P/3F，ON读档修改0；对照证据分层记录 |
| B021正常读档恢复 | USER_GAME_TEST_PASS | [三图结果](Validation/Results/Specialization_B021_User_Result.md)：恢复NONE/0写0→完成RESEARCH/1写3→再读档保持写0；仅正常Cheat测试范围 |
| B020真实新城DEV流程 | USER_GAME_TEST_PASS | [四图结果](Validation/Results/Specialization_B020_User_Result.md)：放置NONE/0写3，同回合Cheat完成RESEARCH/1写6，重载只读写0；非自然生产/跨加载续写 |
| B019合成单表阶段保存/重载 | USER_GAME_TEST_PASS | [四图结果](Validation/Results/Specialization_B019_User_Result.md)：阶段1/2重载写0，最终6/DONE写4且不再写；非正式城市/崩溃验证 |
| 独立测试文明 | USER_GAME_TEST_PASS | 用户A1选择开局确认；本地独立ID与资源引用另有静态检查 |
| City Property | USER_GAME_TEST_PASS | marker读写与重新加载后保持，未再Mark |
| 总督 | USER_GAME_TEST_PASS | 新局present/established、2/3/4阈值随升级、调离原城撤销 |
| 区域/专家 | USER_GAME_TEST_PASS | 类型、存在、完整建造、实际工作人数 |
| UI相邻 | USER_GAME_TEST_PASS | 基础与政策翻倍后相邻区分；不是原生复制算法验收 |
| UI商路 | USER_GAME_TEST_PASS | 端点、三条时读档、第四条加入后同城两条分页 |
| Gameplay任务计数/枚举/读档 | USER_GAME_TEST_PASS | 两次自动采样均4条计数、4名商人、4个匹配任务，同样ID；不包括端点 |
| B007后台UI初始化/读档 | USER_GAME_TEST_PASS | 新存档三条路线，两次COMPLETE_UI_SHADOW、Gameplay数量/ID MATCH；并非Gameplay权威端点 |
| B009后台新增/标准缓存 | USER_GAME_TEST_PASS | 两图3→4、+1/-0；新增Stirling→Edinburgh，旧三条保留；标准count=4、rev 1→2 |
| B008城市删除完整重建 | USER_GAME_TEST_PASS | 后台3→1、+0/-2，保留Aberdeen→Stirling；publish-complete采样；Gameplay对照PENDING |
| B007城市删除缓存失效 | USER_GAME_TEST_PASS | CityRemovedFromMap后旧snapshot清除；不包括重新生成完整集合 |
| Gameplay商路事件 | USER_GAME_TEST_PASS | 新建路线端点捕获；事件历史读档丢失，不能代表现有路线 |
| B011学院放置/完成 | USER_GAME_TEST_PASS | 本次新城学院放置无完成通知，完成时1→2；具体完成手段未说明，不泛化自然跨回合生产 |
| B011重载隔离 | USER_GAME_TEST_PASS | 保存重载后建城0/完成0/Added8；加载Added不冒充完成 |
| B011附加新城观察 | USER_GAME_TEST_PASS | 市中心完成→CityBuilt→市中心Added；市中心NON_V01，不等于正式专业写入 |
| B012合成Game Property表 | USER_GAME_TEST_PASS | 首次写1次、重复不写；保存重载后只读MATCH/写0，重复Write仍0；不等于城市身份或事务通过 |
| B013新城DEV绑定 | USER_GAME_TEST_PASS | 旧城0/0无绑定，新城双方一致/写2/1，重载同token且写0/0；不是正式专业或所有生命周期通过 |
| B014 DEV完成观察持久化 | USER_GAME_TEST_PASS | 三图未完成0→完成1→重载0，记录保持；完成手段未说明，非历史首次或正式专业 |
| B018当前名单/诊断许可 | USER_GAME_TEST_PASS | 两图名单0–14/62–63共17，获准仅0、未知无，54–61名单外，内部自检PASS；非真实事件撤销/正式收益 |
| B017未知明细显示 | USER_GAME_TEST_PASS | 一图54–61均CIV_NOT_READY，页1/1共8条；仅显示通过，不能判定为未获资格AI或空槽 |
| B016自动资格/重载 | USER_GAME_TEST_PASS | 两图玩家0 INIT/LOAD均ENABLED，汇总1/55/8稳定；未知8原因未明，不扩大为全槽位/AI/正式门控通过 |
| B015 DEV新城记录 | USER_GAME_TEST_PASS | 新城NONE/0写1→学院RESEARCH/1写2→重载保持写0；非正式收益或故障/继承验证 |
| 数据库/资源/原生Requirement | STATIC_CONFIRMED | 隔离SQLite/资源引用/源码，不扩大为所有Mod组合兼容 |
| 既有源码研究 | STATIC_CONFIRMED | Pirates Gameplay计数/潜在合法性API；HD Temp_Interface实际是UI；引擎内存在operation读取符号，不能证明其实际返回语义 |

## 结果证据索引

- Property与隐藏建筑：[Marker调查原件](../Historical/LegacyReports/Specialization_P0_Marker_Storage.md)。
- 总督：[A007新局及用户补录](Validation/Results/Specialization_P0_A007_NewGame_Result.md)。
- 早期UI/Game澄清：[B002结果](Validation/Results/Specialization_P0_B002_User_Result.md)、[B003历史](../Historical/LegacyReports/Specialization_P0_B003_Readability.md)。
- Gameplay任务列表/端点nil：[B005](Validation/Results/Specialization_P0_B005_User_Result.md)。
- 后台初始化/读档及旧删城失败：[B007](Validation/Results/Specialization_P0_B007_User_Result.md)。
- 删城3→1：[B008](Validation/Results/Specialization_P0_B008_User_Result.md)。
- 新增3→4、标准缓存rev1→2：[B009](Validation/Results/Specialization_P0_B009_User_Result.md)。
- 更早专家/相邻/用户文字确认范围完整保存在[迁移前Status](../Historical/DocumentSnapshots/Specialization_P0_Status_before_phase1_B010.md)，不为缺少独立新版截图重复测试或扩大PASS。

- B011新城/学院/重载：[14张截图结果](Validation/Results/Specialization_B011_User_Result.md)。

## LOCAL_SIMULATION_PASS

B035：test_lv2_gpp.py实际Lua/SQL、四类人数、文化三类、撤销/重载、错误数值拒绝、后台合并通知及UI只读率通过；旧投资/EffectiveFacts含Lv1网络回归、B034住房Lua回归通过。没有把fixture百分比乘法当作原生倍率验证。

D0010：test_conquest_initialization.py三类路径/冻结候选/Claim退出/普通完成边界/新VM恢复通过；eligibility、D0005继承及区域族回归通过。仅MOCK_ONLY契约，不是游戏征服/项目通过。

B034：test_lv2_housing.py实际Lua生命周期模拟、内存SQL/当前HD层级、manifest/Lua/XML通过；既有投资与统一事实/Lv1/网络回归通过（旧test只在内存适配版本与提示文本）。不等于实机通过。

最新B027：test_d0009_network_runtime.py、test_background_network_sender.py两组通过；实际模块新语义，不将旧模型fixture视为D0009结果。

下表记录本地结果，具体执行轮次见各结果报告；本地模拟不等于Civ VI实机通过。

| 本地检查 | 已覆盖范围 |
|---|---|
| test_network_bridge.py / test_background_network_sender.py | 实际发送/接收模块mock、后台无窗口传递、全量替换/去重/来源撤销；原生传递待测 |
| test_auto_constant_support.py及两组回归 | 三类完成自动应用、读取不写、重载/撤销/错误持有，SQL/Lua/XML；实际自动行为待测 |
| test_research_support.py及三组回归 | B021实际记录接载体API模拟、重复/撤销/加载、内存SQL外键与Lua/XML；原生yield待测 |
| test_eligibility_carrier.py | 只读API候选、配置/表缺失与中断、无缓存恢复、实际Identity.sql资格表内存验证；非Gameplay实机 |
| test_envelope_probe.py及六组回归 | 真实请求/按钮mock、六阶段JSON重载、load只读、过期请求/异常防写、既有恢复契约交叉核对；非游戏 |
| test_load_history_ambiguity.py及两组回归 | 实际B015/B020丢写后同快照反例；B020只读拒绝猜测；非恢复成功/游戏失败 |
| test_city_flow_resume.py及四组回归 | 正常未专业化城重载续写、重复/再重载、已知冲突拒绝；不证明全丢写恢复 |
| test_city_flow_probe.py及七组回归 | 实际旧/新运行模块组合、3/6写入、读档只读、监听反序/故障隔离与实际按钮请求；非游戏 |
| test_native_fresh_hook.py及七组回归 | 实际B013/B015源码、此次写入证据、失败/旧表拒绝，AfterLegacy接Gate/统一表不重复旧处理；非游戏 |
| test_city_event_flow.py及七组回归 | legacy/检查/提交顺序，两城首次交付锁定、加载忽略、失败/重入暂停；不证明未交付事件可检测 |
| test_city_property_bridge.py及六组回归 | API形状城市/绑定接既有Gate，两城隔离、完成/重复、JSON重载、身份/资格/读写异常；真实事件未接 |
| test_unified_city_envelope.py及五组回归 | 同表连续两笔、六截点JSON新VM恢复、六种写入故障、坏表/身份/读失败与写前冲突拒绝；引擎未接 |
| test_city_terminal_record.py及四组回归 | DONE确认/保留、显式加载对账、连续两笔、冲突/重入暂停；单城市mock通道 |
| test_recorded_city_commit.py及三组回归 | PENDING确认先于城市写、启动记录拦截、新VM持有记录拒绝；尚无完成终态 |
| test_pending_city_recovery.py | JSON/新VM中原/目标/冲突/未知对账，所有恢复保持暂停；未接提交器或引擎持久化 |
| test_city_commit_readback.py及入口回归 | 11种提交/读回场景，一次mock写入，写后报错/冲突/未知停止；无引擎setter或持久故障恢复 |
| test_city_operation_gate.py | 实际离线规划器组合，许可先于城市读，owner/代际/完整事实复核，句柄防重用；未调用写入 |
| test_eligibility_lifecycle.py | 失效/失败拒绝旧许可、重授权、跨玩家/实例隔离、重入与过期刷新；非实际收益撤销 |
| test_current_player_roster.py | 当前名单/资格分离、失败不沿用旧授权、名单移除/重现、高编号、组合载体；仅本地候选 |
| test_player_eligibility.py及四组回归 | enabled人类/AI同规则、四种取得、休眠/恢复、重复入口拦截、JSON新VM；只证明离线模型，非游戏资格/效果撤销 |
| test_city_journal_probe.py及六组回归 | B015实际模块与窄请求本地通过，见[结果](Validation/Results/Specialization_B015_Local_Result.md)；不等于实机通过 |
| test_d0005_models.py及六组回归 | 本轮七组通过；首都自接入、工业分项合并/撤销、验证同城后继承/再征服；不代表真实转移或Gold-only Modifier通过 |
| test_city_completion_journal.py及状态/计划两组回归 | D0004按通知顺序锁定，资格缺失拒绝、旧DEV拒绝、持久缺口、JSON/新VM恢复；真实提交器未实现 |
| test_completion_history_boundary.py | 实际B014代码的5组反例/边界检查通过；不同历史同表、通知顺序、写入失败、重载、重复读；不是正式初始化通过 |
| test_specialization_p0.py / test_specialization_identity.py | Lua/XML、窄请求、身份SQL/资源引用；部分环境为fixture |
| test_completion_record_probe.py与六组回归 | B014本地通过，见[结果](Validation/Results/Specialization_B014_Local_Result.md)；不等于正式专业写入或实机PASS |
| test_binding_probe.py与五组回归 | B013本地通过；[结果](Validation/Results/Specialization_B013_Local_Result.md)，未升级实机证据 |
| test_city_binding_recovery.py | 本轮离线恢复决定通过；总账预留/城市token部分成功不猜测修复，不等于引擎绑定通过 |
| test_storage_probe.py与四组回归 | B012本地通过；[结果](Validation/Results/Specialization_B012_Local_Result.md)，不等于实机通过 |
| test_city_identity_registry.py | 本轮新增故障模拟通过；编号去重、报错后读回、丢弃/损坏/重入/过期拒绝、新VM恢复；不证明引擎原子性 |
| test_city_fact_write_plan.py | 新增通过：B011顺序、初始化保留、加载隔离、fixture重复/过期计划拒绝；不是存档写入通过 |
| test_city_role_facts.py | 本轮回归通过；B010只读角色、未知专业/潜力、总督条件上限；不是实机PASS |
| test_completion_probe.py及五组相关回归 | 本轮通过；[B011本地结果](Validation/Results/Specialization_B011_Local_Result.md)，不等于游戏通过 |
| test_district_family.py | 本轮新增通过：缓存36区域/16替代关系、10种v0.1类型、替代图检查与只读完成候选过滤；[报告](../Reports/Technical/Specialization_District_Completion_Adapter.md) |
| test_city_specialization_state.py | 本轮新增通过：四族完成锁定、Potential投资防重、ACTIVE、JSON/新Lua VM恢复、未决生命周期拒绝；[结果](Validation/Results/Specialization_City_State_Local_Result.md) |
| test_background_routes.py / test_trade_route_probe.py | 后台批次、错误/重试、加载与Gameplay任务诊断 |
| test_shadow_route_state.py | 标准缓存全量替换、复制读取、revision、UNKNOWN/reset |
| test_trade_route_state.py / test_shadow_network_state.py | 已通过：MOCK来源、角色/模板/ACTIVE变化、去重/撤销、UI来源隔离 |
| test_specialization_network.py | 已通过：给定L的sqrt/独立k/城市去重及内存数据库TEXT存储，不证明引擎精度 |
| test_network_multisource.py | 已通过：全局max、多中心去重、最高源失效回退、ACTIVE变化、空集、k、无效输入和影子来源隔离；[结果](Validation/Results/Specialization_Network_Multisource_Local_Result.md) |

## 唯一当前待办队列

Task State与Verification分列，暂停不是失败，也不建立新的验证状态枚举。

| ID/任务 | Task State | Verification | 前置/下一步 |
|---|---|---|---|
| B048 科研/文化Lv4专家百分比 | DEPLOYED | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED | 当前唯一新批次：两类收益及计数/撤销，见上方案例 |
| B047 Crew整数与显示 | IMPLEMENTED | LOCAL_SIMULATION_PASS；新显示后续顺带观察 | D0012已接受，不新派旧Crew测试 |
| Lv4其余组件 / 网络效果 | PENDING | 技术调查与部分设计边界待完成 | 按独立组件推进，不把百分比完成当完整Lv4完成 |
| D0010 Conquest分流sync | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | [同步报告](../Reports/Technical/Specialization_D0010_Architecture_Sync.md)，三类设计已确认，旧入口停止使用 |
| D0010真实转移快照/Identity origin/Claim项目 | ENGINE_ADAPTER_PENDING | USER_GAME_TEST_REQUIRED（尚未具备测试包，不派发） | 先确认同城与边界；非空冻结Claim、空集普通完成、已有Identity继承分开验收；Claim成本精确值仍TBD |
| B034共同Lv2住房 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [五图结果](Validation/Results/Specialization_B034_User_Result.md)：Research总督开启、两层增加、载体即时撤销/显示延迟接受；重载未回报，不追加补测 |
| B034住房面板即时刷新 | DEFERRED_ACCEPTED_LIMITATION | 同回合显示未更新；用户接受 | 载体归0已确认，回合/生产刷新后住房正确；具体UI/引擎缓存时点未完全定位，不阻塞GPP |
| B035共同Lv2基础GPP | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [用户人工结果](Validation/Results/Specialization_B035_User_Result.md)已通过；旧待派行已纠正，不重测GPP |
| D0009架构同步 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED | hash、全文diff、旧源码冲突核对；不是新机制通过 |
| D0009 direct中心自然接收 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [B027两图](Validation/Results/Specialization_B027_User_Result.md)；旧离线原型另待统一 |
| D0009 Commerce IV / 固定小数承载 | DEFERRED_BY_USER | B029/B030小数USER_GAME_TEST_FAIL | 后续研究；内部浮点保留，不取整，不阻塞其它机制 |
| B031目的端失效撤销 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | 两图通过；明细分页未独立实测，战争/自然到期/掠夺未覆盖 |
| B031空白按钮标签 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | B033三图英文标签均显示，限定当前环境 |
| D0001接受 / A0002同步 | COMPLETE | 文档核对，不是游戏验证 | [同步记录](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)；未决设计和技术限制保留 |
| D0006/7架构差异同步 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED（规则/hash/源码门控检查） | [同步报告](../Reports/Technical/Specialization_D0007_Architecture_Sync.md)；未部署资格或Military |
| 通用资格与休眠/恢复适配 | COMPLETE_OFFLINE / ENGINE_PENDING | LOCAL_SIMULATION_PASS | [资格模型](../Reports/Technical/Specialization_D0007_Eligibility_Model.md)；五组通过；只读carrier候选已完成；B016两案按两图范围通过；B018已确认54–61在本局当前名单外，准备正式资格入口；生命周期仍待接入，网络入口及实际效果撤销未接入，测试暂不派发 |
| D0005差异/本地模型 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | [同步报告](../Reports/Technical/Specialization_D0005_Architecture_Sync.md)；真实身份/收益接口未接入 |
| D0003/4差异映射 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED（文档/hash） | [同步](../Reports/Technical/Specialization_D0004_Completion_Journal.md)；Future API未验证，未扩大v0.1 |
| D0002规则/架构同步 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED（文档差异与hash） | [同步报告](../Reports/Technical/Specialization_D0002_Architecture_Sync.md)；Future经验API尚未验证 |
| B011放置/完成及重载事件 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [实机结果与范围](Validation/Results/Specialization_B011_User_Result.md)；不重发本批 |
| D0008架构同步 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED | [差异索引](../Reports/Technical/Specialization_D0008_Architecture_Sync.md)；Future不扩展当前范围 |
| 自动Lv1恢复及新城（B024） | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [结果](Validation/Results/Specialization_B024_User_Result.md)；两图+人工建筑/多专家/第二区域回报；无补测 |
| 三类常数Lv1自动收益（B023） | FAILED_OBSERVED | USER_GAME_TEST_FAIL | [B023三案](Validation/Cases/B023_Automatic_Constant_Lv1.md)；自动完成/映射/重载，无ON/OFF |
| Network后台桥接B026 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [八图复验](Validation/Results/Specialization_B026_User_Result.md)；下一项可读性与撤销，不重复本批 |
| Network后台桥接B025 | FAILED_OBSERVED | USER_GAME_TEST_FAIL | [来源决定](../Reports/Technical/Specialization_Network_Background_Source_Decision.md)；不依赖打开窗口，先连接/分发/撤销，无正式收益 |
| Research Lv1原生收益实验 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [B022结果](Validation/Results/Specialization_B022_User_Result.md)：岗位/读档有图，OFF及零专家对照依用户人工通过回报 |
| 正常读档恢复 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [B021三图结果](Validation/Results/Specialization_B021_User_Result.md)；正常恢复/完成/再读档通过，极端故障不在范围 |
| 所有持久写入同时丢失的历史恢复 | DEFERRED_EDGE_CASE | BLOCKED | [反例](../Reports/Technical/Specialization_Load_History_Ambiguity.md)仍成立；按用户优先级不再阻塞正常Cheat路径，不派故障实验 |
| B020真实新城DEV流程 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [四图结果](Validation/Results/Specialization_B020_User_Result.md)，同回合Cheat路径；无需补测 |
| 实际新城回调适配 | COMPLETE_OFFLINE / DEV_PENDING | LOCAL_SIMULATION_PASS | [实际接口验证](../Reports/Technical/Specialization_Native_Fresh_Hook.md)；未注册运行，无新实机批次 |
| 有序事件/历史检查入口 | COMPLETE_OFFLINE / NATIVE_ADAPTER_PENDING | LOCAL_SIMULATION_PASS | [事件流](../Reports/Technical/Specialization_City_Event_Flow.md)；真实检查与跨加载历史凭据未接，无实机批次 |
| City Property连接 | COMPLETE_OFFLINE / EVENT_ADAPTER_PENDING | LOCAL_SIMULATION_PASS | [连接层](../Reports/Technical/Specialization_City_Property_Bridge.md)；下一项有序新城分发/完整历史证据，未派实机测试 |
| B019合成分阶段存储 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [四图结果](Validation/Results/Specialization_B019_User_Result.md)，无需补测 |
| 同表成果/恢复记录 | COMPLETE_OFFLINE / FORMAL_ADAPTER_PENDING | LOCAL_SIMULATION_PASS | [统一存储](../Reports/Technical/Specialization_Unified_City_Envelope.md)；合成DEV B019两案按四图范围通过；正式城市适配未部署 |
| 新城初始化/完成事实写入计划 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | [写入准备](../Reports/Technical/Specialization_City_Fact_Write_Plan.md)；没有引擎提交器 |
| 编号账本/写入故障恢复实验 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | [故障模拟](../Reports/Technical/Specialization_City_Identity_Storage.md)；真实代际凭据和持久性未验证 |
| 完成历史资格 / 顺序记录 | COMPLETE_OFFLINE / ENGINE_ADAPTER_PENDING | LOCAL_SIMULATION_PASS | [统一记录准备](../Reports/Technical/Specialization_D0004_Completion_Journal.md)；PROG-005已接受，实际资格/写入和错误停止待接入 |
| B015新城记录实际提交 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [三图结果](Validation/Results/Specialization_B015_User_Result.md)；新城/学院/重载通过，旧城和重复操作未独立确认 |
| B014 DEV完成记录 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [三图结果](Validation/Results/Specialization_B014_User_Result.md)；学院完成记录与重载保持，非正式专业 |
| B013 DEV新城绑定 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [五图结果](Validation/Results/Specialization_B013_User_Result.md)；普通新城/重载通过，不重测 |
| B012 DEV表存储 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [五图结果](Validation/Results/Specialization_B012_User_Result.md)；不重复本批 |
| 真实城市代际凭据/首次账本资格 | OPEN_TECHNICAL | BLOCKED（正式身份接入） | fixture不能当引擎证据；征服保留事实已定，跨owner同城识别与旧档初始化待实现/未来兼容处理 |
| B010首都/非首都ROLE | DEFERRED_USER_PAUSE | USER_GAME_TEST_REQUIRED | 用户明确尚未测试；[案例入口](Validation/Cases/B010_Deferred.md)，本轮不执行 |
| 标准缓存其它生命周期、自然结束/取消/掠夺/战争/征服/夷平 | DEFERRED | USER_GAME_TEST_REQUIRED | 不把Cheat删城当所有情形通过；另批最小案例，当前不派发 |
| 纯Gameplay全集（可选研究，不再阻塞主线） | OPTIONAL_RESEARCH | STATIC_CONFIRMED（研究证据，非可用接口） | [第二轮复核](../Reports/Technical/Specialization_Trade_Authority_Second_Audit.md)；无新可验收候选，不派发测试 |
| 完成事件/区域族接入准备 | COMPLETE_OFFLINE_RESEARCH | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 官方/HD事件先例和离线候选通过；B011只读探针已部署 |
| B033实际移民投资 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | 三图及人工1→2/重复/保存重载；3/4级投资、异常恢复未测 |
| B033动态总督/新建网络 | COMPLETE_REPORTED_SCOPE | USER_GAME_TEST_PASS | 人工ACTIVE随建立/等级/调离变化、1级仍1；新建路线身份正确；原路线跨升级保持未测 |
| B032原生只读账本/统一消费者 | DEPLOYED / B033_ACTION_INTEGRATED | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 已由B033接真实投资；新增住房消费者，旧Lv1/网络回归通过 |
| 投资账本/基础事实衔接 | COMPLETE_OFFLINE / NATIVE_PENDING | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 新账本存凭据，保留基础专业记录；HD按钮/奖励/删除路径核对；下一步原生Property和Lv1/网络统一读取 |
| 移民永久Potential投资执行层 | COMPLETE_OFFLINE / STORAGE_ADAPTER_NEXT | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 顺序消耗/确认/提交与恢复模型完成；下一步适配B020/B015存储及升级后Lv1/网络连续性，尚无实机动作 |
| 城市专业/Potential/ACTIVE离线状态 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | 完成事件与Property/单位事务未接游戏；UID和OPEN-04保留 |
| Research/Culture多源max离线适配 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | 尚未接正式路线来源或游戏Boost |
| 原生复制基数、Gold-only折扣、Boost精度 | DEFERRED | USER_GAME_TEST_REQUIRED | 尚无完整实验包，不执行旧报告按钮 |
| Crew注入前置B039 | DEV_PROBE_DEPLOYED | USER_GAME_TEST_REQUIRED | 四案接口验证；正式项目/单位未实现，巨作仍待实现 |

## BLOCKED / 技术及设计边界

- D0010三类玩法已确定，不再列为设计分流待决。Conquest正式接入仍BLOCKED于可靠同城/转移边界及持久模式适配；当前DEV第一完成锚点不支持Claim来源，不能伪造事件绕过。旧档初始化独立OPEN，Claim精确成本在实际项目落地前再确认。此限制不阻塞B034住房测试。

- 纯Gameplay全集仍未确认但不再是前置阻塞；后台当前UI来源已获用户认可，当前运行UI_SHADOW_ONLY尚未完成桥接及正式网络接入。B005端点参数nil保留USER_GAME_TEST_FAIL候选记录。
- Industry多源、首都自接入、征服继承语义已由D0005确定；永久UID与真实接口仍待技术验证，旧档首次初始化归实现/未来兼容，量化/分类按Spec剩余未决处理。不能把技术UNKNOWN改称继承语义未决。
- 旧总督Lua getter、Gameplay city:GetTrade缺失、B006/B007调度失败均保留历史范围；后续修复的PASS不倒写旧报告。

## 文档整理验证

迁移与文件校验详见[第一阶段交付报告](../Reports/Proposals/Specialization_Phase1_Migration_Report.md)。该迁移轮Source/Tests未改；本轮离线Tests变更/重跑另见结果记录，运行源码仍未改。

A0002同步已完成：[规则映射与校验](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)。A0003已完成离线多源max适配；下一步仍是正式网络权威来源研究，B010保持用户延后，不自行派发测试。

A0004第二轮来源复核未找到可覆盖普通己方商路的GameEffects集合/端点。正式Network继续受技术阻塞；无新增实机批次，B010不重发。可独立继续本地专业能力适配研究，不能默认升级后台UI为权威。

A0005城市状态模型已在本地通过，运行仍B010。下一步建议只读核对完成事件/区域替代族与新城身份，设计Property写入及投资事务适配；不先接收益、不自行决定OPEN-04、不要求用户重测B010。

A0006已核对原生完成/建城Gameplay事件与替代族，离线候选不接正式写入。下一步有依据准备CityBuilt/OnDistrictConstructed只读探针；当前没有新用户测试，B010继续延后。

当前行动以本队列B011为准：上方A0005/A0006阶段备注中的“未派发/运行仍B010”是阶段记录，已由B011交付取代。B011用户结果现已登记（S0010）；本轮未写入专业事实或发放收益。

## S0010：本次实机结果登记

14张截图逐张核对，B011两案按结果报告限定范围通过，并额外确认一次真实新城CityBuilt。当前无需用户补测；B010仍暂停。只更新证据/文档，未修改或重跑运行源码和Tests；上方各“本轮本地通过”属于对应报告原执行轮次。本次没有新增本地模拟结论。下一步可独立准备新城初始化与完成事实的防重复写入边界；商路权威源、永久UID及OPEN-04未因本批通过而解决。

当前Spec已为ACCEPTED D0002，hash与ChangeLog一致，本轮未改Design。Architecture仅同步至D0001；本次登记D0002待审差距，不宣称已完成该版技术同步。

## S0011：D0002同步和写入计划本地验证

D0002 Rule差异与hash已核对，A0009同步完成并保留Future经验API限制；取代S0010的待同步状态。新增离线CityFactWritePlan及测试，城市状态/区域族两组回归通过，共三项exit=0。具体证据见[写入准备](../Reports/Technical/Specialization_City_Fact_Write_Plan.md)。本轮不新增实机PASS，不派发新测试；运行仍B011。下一步研究持久身份和实际写入失败恢复，B010继续延后。

## S0012：身份存储故障模拟

新增CityIdentityRegistry.lua及test_city_identity_registry.py，最终测试与CityFactWritePlan回归通过。详细证据/前提见[身份存储研究](../Reports/Technical/Specialization_City_Identity_Storage.md)。运行仍B011/modinfo18，本轮无用户测试、无新游戏PASS；下一项是独立DEV表存储探针，尚未部署，不要求用户执行。真实身份绑定与存储耐久性仍未确认。

## S0013：B012交付

运行已更新B012/modinfo19，新增独立Game Property合成表探针；无正式城市身份、专业或收益。五组本地检查通过，等待用户两案。此前“尚未部署/无用户测试”属S0012及更早阶段记录，当前以本节和待办队列为准。B010保持暂停，不重复B011。

## S0014：B012用户结果

[五图结果](Validation/Results/Specialization_B012_User_Result.md)确认B012两案在本次存档通过，取代S0013的等待状态；用户无需补测。源码仍B012/19，下一步准备真实城市身份/事实持久化适配，既有代际及OPEN-04边界未解除。

用户已清空旧截图再投递；B011原图当前不在收件箱，原判读报告和hash保留，旧图链接不可用，不要求重拍。未来关键图按批次归档是建议，尚未授权实施。

## S0015：归档和绑定准备

用户已批准G0004读后归档；[B012五图原件](Validation/Evidence/B012/)已移动并逐文件验证hash，取代S0014的未授权建议。ScreenShots保留为投递目录。新增[双侧绑定恢复](../Reports/Technical/Specialization_City_Binding_Recovery.md)离线决定和本地测试，编号模块回归通过。运行仍B012；下一步准备DEV新城双侧绑定探针，当前无新增用户测试，不补旧城、不决定OPEN-04。

## S0016：B013交付

运行B013/modinfo20，新增DEV新城绑定及只读审计；六组本地检查通过，等待用户[两案](Validation/Cases/B013_New_City_Binding.md)。上方“待准备/运行仍B012”为此前阶段记录，当前以本节为准。正式城市专业、Potential与收益未写入，B010仍延后；不重复B011/B012。

## S0017：B013实机结果

[五图结果](Validation/Results/Specialization_B013_User_Result.md)确认两案按观察范围通过；[原图](Validation/Evidence/B013/)已按G0004归档且hash一致，替代S0016等待状态。用户无需补测，B010继续暂停。下一步准备完成事实与已绑定新城的连接；本轮运行仍B013/20，未改源码或测试。

## S0018：B014交付

运行B014/modinfo21，将绑定与完成事件连接为DEV观察表；七组本地检查通过，等待用户两案。当前不接正式专业或Potential，首次观察不冒充首次历史。B010继续延后，旧批次不重复；前段运行旧版本/下一步准备文字为阶段历史，以本节及当前队列为准。

## S0019：B014实机结果

[三图判读](Validation/Results/Specialization_B014_User_Result.md)确认本次未完成→完成记录及保存重载保持，取代S0018等待状态。[原图](Validation/Evidence/B014/)按G0004归档并核对hash。完成方式未说明、同为T1，不扩大到自然跨回合生产。FIRST_OBSERVED_COMPLETION仍非正式首次完成权威。无新增用户测试，B010延后；下一步准备新城历史完整性与正式初始化资格边界，本轮不开发。

## S0020：历史资格反例与待决

新增test_completion_history_boundary.py，五组检查exit=0，详见[报告](../Reports/Technical/Specialization_Completion_History_Boundary.md)。B014正常存储PASS不变；反例证明不能据观察表补出历史。当前需用户决定OPEN-04同时完成顺序，不把建议登记为接受。新城资格与持久错误边界仍待实现；当前无新实机批次、无新运行包，B010延后。

最终校验发现当前Design已登记ACCEPTED D0003（hash与ChangeLog一致）；本轮未写Design。PROG-001至004逐条与冻结D0002相同，因此本次结论仍适用；整体sync保留D0002，D0003标PENDING_D0003_REVIEW。

## S0021：用户确认顺序，D0004与统一记录准备

用户接受PROG-005，顺序不再待决。D0003已冻结、D0004/hash已登记；A0019完成D0003/4差异映射。新增统一记录离线模块，连同状态/计划/旧探针反例四组脚本exit=0，详见[结果](../Reports/Technical/Specialization_D0004_Completion_Journal.md)。运行文件与备份manifest逐项hash一致，无新实机PASS或批次；下一步真实新城提交器准备，不迁移B014记录，B010延后。

## S0022：D0005同步与模型结果

[本轮报告](../Reports/Technical/Specialization_D0005_Architecture_Sync.md)记录七组本地通过、三项规则映射和文件列表。运行/Design逐项hash保持，A0020同步至D0005。真实新城提交器的owner变化必须保留事实并等待同城证据，不初始化为新城；尚未接入游戏，B010继续延后，无新用户测试。

## S0023：B015交付

运行B015/modinfo22，实际DEV单表写入/错误停止已接入；[七组本地结果](Validation/Results/Specialization_B015_Local_Result.md)通过，等待用户[三案](Validation/Cases/B015_City_Journal.md)。只有当前版本新建城市可建立本批资格；无需新局，旧B013/B014城不迁移。正式专业收益、征服转移、永久UID和故障持久性边界保留。用户测试前不再扩展，B010继续延后。

## S0024：B015实机结果

[三图判读](Validation/Results/Specialization_B015_User_Result.md)按新城、学院完成、重载观察范围通过，取代S0023等待状态；[原图](Validation/Evidence/B015/)已归档且hash一致。旧城/重复操作无独立证据，不扩PASS，不重发整批。运行仍B015/22，无新增测试或开发。当前Accepted为D0006，PROG与D0005一致；整体架构仍同步至D0005，D0006映射待审。

## S0025：D0007文档同步

A0023补齐D0006军事IV及D0007资格/征服休眠规则，见[差异及实现缺口](../Reports/Technical/Specialization_D0007_Architecture_Sync.md)。本轮STATIC_CONFIRMED仅指设计/hash/静态门控核对；未新增LOCAL_SIMULATION_PASS或USER_GAME_TEST_PASS。保留B015三图结果；运行、Tests和Design逐项hash未变。旧模型isTestCivilization、旧档DESIGN_DECISION_REQUIRED及缺少休眠分支已登记待适配，不作为D0007符合性证明。无新实机批次；下一步先资格/事实分层准备，B010延后。

## S0026：D0007资格离线模型通过

[本轮报告](../Reports/Technical/Specialization_D0007_Eligibility_Model.md)记录五组脚本exit=0。State不再绑定测试文明；读取永久事实与当前启用资格分离，disabled没有Lv1运行效果，unknown不新建/激活/删除成果。独立取得入口要求历史证据，不推断旧档。此处只指离线返回值，未接入任何游戏效果。

当前无新实机测试、无新增实机PASS，B015/22和Design逐项hash不变。下一步研究真实资格载体与事件入口，再衔接城市生命周期；Network统一筛选、实际撤销及永久UID仍是实现边界。B010延后，用户现在无需操作。

## S0027：资格载体静态调查及只读候选

[载体报告](../Reports/Technical/Specialization_Eligibility_Carrier_Research.md)记录HD/原版Gameplay先例、候选与生命周期边界。新增test_eligibility_carrier.py本地通过；既有State模型未改，不重复回归。当前绑定不变，不因HD夺取Trait属性自动启用系统。

运行仍B015/22；既有Source/Tests与Design保护hash保持，无新实机PASS或派发批次。下一步可接最小Gameplay只读资格诊断，验证自动初始化/重载；跨owner同城与其它取得方式仍待研究。用户现在无需操作，B010延后。

## S0028：B016交付，等待两案

新增自动资格诊断，运行B016/modinfo23。五组本地检查最终通过，见[结果](Validation/Results/Specialization_B016_Local_Result.md)。唯一当前新测试：[B016自动采样/重载两案](Validation/Cases/B016_Eligibility.md)，USER_GAME_TEST_REQUIRED。使用现有存档，无需城市/商路操作。现暂停继续扩展，等待用户两张结果；B010继续延后，旧B015实机证据不变。Design未改。

## S0029：B016用户两图复验

[结果](Validation/Results/Specialization_B016_User_Result.md)登记两案按回报/截图范围USER_GAME_TEST_PASS，取代S0028等待状态。玩家0初始化及加载后ENABLED，汇总1/55/8前后相同。未知8的原因截图无法确认，后续只读检查日志/玩家槽位，UNKNOWN不启用；不要求重测本批。

原图已归档至Evidence/B016且hash一致。运行仍B016/23，Design/Source/Tests未变，没有新增本地测试或功能。B010继续延后。下一步正式资格入口准备前厘清未知槽位，用户当前无需操作。

## S0030：B017等待未知槽位补充

当前日志没有B016逐槽位原因。B017新增只读明细按钮，实际采样未改；两组本地检查通过，见[结果](Validation/Results/Specialization_B017_Local_Result.md)。唯一当前测试为[B017单案](Validation/Cases/B017_Unknown_Slots.md)：加载现有存档后点Eligibility unknowns，回传一页预计8条；无需保存重载或重复B016。B016两案PASS保持，未知8原因仍未定。正式资格入口不在本轮接入，B010延后。

## S0031：B017明细用户结果

[一图结果](Validation/Results/Specialization_B017_User_Result.md)确认明细显示通过，取代S0030等待单案。未知8均为player 54–61 / CIV_NOT_READY：文明类型返回值未通过检查，尚未进入Trait判断；不得等同55个DISABLED，也不推断一定是预留槽位。后续只读核对名单/槽位定义，当前不要求用户重复测试。

原图归档且hash一致，运行B017/24、Source/Tests/Design未变。B016两案通过保持，B010延后。用户现在无需操作。

## S0032：名单入口离线准备

[报告](../Reports/Technical/Specialization_Current_Player_Roster.md)记录GetAliveIDs真实Gameplay先例及本地候选通过。未找到54–61固定身份的可靠定义；本局实际名单未采样，仍不判定为空槽。未知原因身份不再作为离线入口准备的前置，按名单和资格分别处理即可。

运行B017/24不变；Design、原Source/Tests保护hash保持。无新实机测试或PASS。下一步准备名单失效/重建后的运行许可边界，再合并必要实机验证；不再单独要求相同截图。用户现在无需操作，B010延后。

## S0033：资格生命周期离线通过

[结果](../Reports/Technical/Specialization_Eligibility_Lifecycle.md)记录新增许可模型与组合测试通过。已有模块/运行/Design不变，无新增实机PASS或测试要求；永久成果与实际收益撤销边界保持。下一步将名单与许可组合为最小只读Gameplay运行对照，之后才给合并的新实机步骤。B010延后，用户现在无需操作。

## S0034：B018交付等待两案

[六组本地结果](Validation/Results/Specialization_B018_Local_Result.md)通过；新运行组合资格诊断不接正式收益/写入。当前唯一新测试[B018两案](Validation/Cases/B018_Runtime_Eligibility.md)，USER_GAME_TEST_REQUIRED：加载后查看Runtime eligibility，保存重载再查看。54–61只按实际名单记录，不设预期身份。暂停继续扩展等待结果，B010延后；Design未改。

## S0035：B018用户两图通过

[结果](Validation/Results/Specialization_B018_User_Result.md)确认两案按截图/回报范围通过，取代S0034等待。当前名单17个引擎玩家，仅0获准；54–61不在本局存活名单，关闭“当前AI未知资格异常”的追查，不宣称永久槽位身份已知。

两图已归档且hash一致。运行B018/25、Design/Source/Tests未改，无新测试要求。下一步准备把已验证的名单/资格入口接入限定城市处理流程，先核对事件失效与实际提交边界，不接正式收益；不再重复槽位诊断。B010延后，用户现在无需操作。

## S0036：城市入口复核离线通过

[报告](../Reports/Technical/Specialization_City_Operation_Gate.md)记录CityOperationGate与组合测试通过。实际运行仍B018/25，旧源码/Tests/Design hash不变；不增加实机PASS或派发测试。下一步本地准备复核紧邻的提交/读回与不确定写入处理，再决定DEV接入。永久UID、真实事件失效、正式收益仍未实现。用户无需操作，B010延后。

## S0037：提交/读回本地边界通过

[结果](../Reports/Technical/Specialization_City_Commit_Readback.md)记录两组通过。只修改离线CityOperationGate并新增测试，运行B018/25与Design不变。当前停止仅实例内有效，重载恢复尚未解决；下一步先本地准备未确认提交的持久恢复记录，不先接游戏写入。无新实机测试或PASS，用户无需操作，B010延后。

## S0038：未确认记录离线恢复通过

[报告](../Reports/Technical/Specialization_Pending_City_Recovery.md)记录新增PENDING模型及JSON新VM测试通过。现有提交器/运行/Design未改，没有新游戏验证结论或用户测试。下一步将记录保存/读回确认接到提交前，并实现加载先查未确认记录的入口；跨Property保存顺序仍是技术边界。B010延后，用户无需操作。

## S0039：记录/提交集成本地通过

[四组结果](../Reports/Technical/Specialization_Recorded_City_Commit.md)通过。记录未确认不写城市，已有PENDING跨新VM阻止新计划；成功仍保留PENDING并停止，下一步补终态/加载判定以支持连续操作。运行B018/25、Design不变，没有新实机要求/PASS。用户无需操作，B010延后。

## S0040：终态与连续操作本地通过

[五组结果](../Reports/Technical/Specialization_City_Terminal_Record.md)通过，支持单城市初始化→学院完成两笔、DONE保留与加载后显式对账。PENDING原值/冲突不自动清除。运行B018/25与Design未改，无新用户测试/实机PASS。下一步审查统一存储结构再准备最小DEV接入，跨Property原子性不作保证。B010延后，用户无需操作。

## S0041：统一存储本地通过

[六组结果](../Reports/Technical/Specialization_Unified_City_Envelope.md)通过，既有Gate/恢复模型共用单表；六个保存阶段经JSON新VM恢复。PENDING原值保持暂停，目标已写才可显式DONE，连续两笔不重复写成果。运行B018/25、Design与既有Tests未改，无新实机PASS或用户测试。下一项为独立合成DEV分阶段保存/恢复探针，尚未部署；B010延后，用户现在无需操作。

## S0042：B019已部署，等待两案

[七组本地结果](../Reports/Technical/Specialization_B019_Envelope_Probe.md)通过，运行B019/modinfo26。用户只需[两案](Validation/Cases/B019_Envelope_Recovery.md)，使用旧测试存档；不重发B010或既有探针。正常分阶段重载、自动只读和实际UI尚无用户证据，不增加游戏PASS。完成本轮后停止等待结果。

## S0043：B019两案四图通过

[用户结果](Validation/Results/Specialization_B019_User_Result.md)确认计划/目标两次重载只读保持，终态6写入4且COMPLETE_NO_WRITE。取代S0042的等待状态。四图已归档Evidence/B019且hash一致；运行B019/26、Design/Source/Tests未改，无新增本地测试。下一项建议准备限定真实新城的资格/身份/完成事实存储衔接；本轮只登记证据，不接收益。用户无需补测，B010延后。

## S0044：限定城市存储连接本地通过

[七组检查](../Reports/Technical/Specialization_City_Property_Bridge.md)通过，新增CityPropertyBridge和对应测试。运行B019/26、Design、既有Source/Tests未改；无新实机结论/测试。下一项准备B013新城事件有序分发及完整历史证据，不能覆盖B015单回调或把DONE当无漏通知证明。用户无需操作，B010延后。

## S0045：事件流组合本地通过

[八组结果](../Reports/Technical/Specialization_City_Event_Flow.md)通过；新增CityEventFlow与测试，未改B015回调。暂停仅实例内，未交付事件不可自动检测，已有DONE不证明跨加载历史完整。运行B019/26、Design、既有Source/Tests保持，无新增实机结论或用户测试。下一步映射B013/B015实际检查并准备有序挂接；正式历史恢复仍待实现，不接收益。用户无需操作，B010延后。

## S0046：实际新城回调组合本地通过

[八组结果](../Reports/Technical/Specialization_Native_Fresh_Hook.md)通过，实际B013/B015在mock环境接证据与现有存储模型。只修改离线CityEventFlow并新增候选/测试，运行B019/26、Design与其它Tests不变。当前无新实机结论/测试；下一项限定DEV集成准备，完成事件及跨加载历史仍待接，不启用收益。用户无需操作，B010延后。

## S0047：B020部署，等待两案

[八组本地结果](../Reports/Technical/Specialization_B020_City_Flow.md)通过，运行B020/27。用户执行[两案](Validation/Cases/B020_City_Flow.md)：新城/学院本次加载提交与读档只读保持。不新增游戏PASS，不重发B019/B010；Design、SQL及既有Tests不变。完成本轮后等待三张关键截图。

## S0048：B020两案四图通过

[用户四图](Validation/Results/Specialization_B020_User_Result.md)确认新城、学院放置未完成、同回合Cheat完成以及正常重载只读。用户明确使用“完成当前城市项目”，不泛化自然跨回合生产。取代S0047等待状态；四图归档Evidence/B020且hash一致。运行B020/27、Design/Source/Tests未改；无新增本地验证或实机要求。下一项跨加载历史检查/恢复准备，不接收益。用户无需操作，B010延后。

另：Design/ChangeLog已登记Accepted D0008，hash核对一致；本轮只登记发现，架构仍同步至D0007。下一次开发前补差异审阅，Future登记不自动进入v0.1，也不改变本批测试判定。

## S0049：D0008已同步，恢复反例已复现

D0008/hash与Future成熟度[同步完成](../Reports/Technical/Specialization_D0008_Architecture_Sync.md)，取代S0048待审阅。三组本地检查确认[丢写历史反例](../Reports/Technical/Specialization_Load_History_Ambiguity.md)，并非恢复成功或用户游戏失败；B020四图PASS保留，运行B020/27与Design不变。下一项明确正常恢复与异常持久化边界，不直接解锁旧城写入。无新用户决定/测试，B010延后。

## S0050：B021正常恢复待测

用户明确Cheat机制测试优先、极端异常不作为前置。B021/28已接正常恢复，五组本地通过，[一组测试](Validation/Cases/B021_Normal_Load_Resume.md)等待回报。旧全丢写反例保留但降为延后边界；无新实机PASS。Design与既有Tests未改；下一项Lv1真实收益，不扩大到Future。

## S0051：B021三图正常恢复通过

[用户结果](Validation/Results/Specialization_B021_User_Result.md)取代S0050待测：三图均RESUMED_NORMAL且未停止，revision/写入为3/0→6/3→6/0。原图归档并校验一致，无新增用户测试。运行B021/28、Source、Tests和Design保持；下一项实际Lv1收益，极端组合故障延后，B010继续暂停。

## S0052：B022 Research Lv1收益待测

四组本地检查通过，部署B022/29显式原生收益开关。新SQL定义旧档可能缺失，可先Read确认，缺失则新局。仅派[一组三案](Validation/Cases/B022_Research_Lv1_Yields.md)，不重测B021专业事实，不重复B010。Design不变，无新设计决定。下一步依实际岗位收益回报接常数型Lv1自动应用，不扩展极端故障或Future。

## S0053：B022人工通过与三图复验

取代S0052待测。[结果](Validation/Results/Specialization_B022_User_Result.md)区分岗位/读档直接截图与用户人工对照回报。桌面附件复制归档、原件不动，hash一致。无新用户测试；下一项常数型Lv1自动应用。本轮没有改Source/Tests/Design，B022/29保持，B010延后。

## S0054：自动Lv1待测，Network提案待决定

B023/30部署三类标准专业自动收益，三组本地检查通过；只派B023一组测试。另三组Network模拟回归通过，但真实Gameplay路线来源仍未解决。[桥接提案](../Reports/Proposals/Specialization_Network_Connection_Distribution_Plan.md)待用户授权候选实验，不接网络收益，不重发B010。Design未改；下一重点为连接/分发网络。

## S0055：B023失败，B024候选修复待复验

[六图结果](Validation/Results/Specialization_B023_Failure_Result.md)证明三城专业正常但无载体，取代B023待测。新缓存定义齐全；扫描异常边界缺陷本地复现，实际事故根因尚不能完全确定。[B024修复与最小复验](../Reports/Technical/Specialization_B024_Auto_Scan_Fix.md)：加载现有三城看自动补齐，不重开局。B024为USER_GAME_TEST_REQUIRED，非PASS。网络提案仍待决定。

## S0056：B024用户通过，Network待决定

[结果](Validation/Results/Specialization_B024_User_Result.md)取代S0055复验待测。两图原件已归档，第三图未在收件箱找到；其对应测试按用户明确回报登记，不要求重做。B023失败历史保留；修复后的额外再次重载写0未单独确认，不新增补测。Source/Tests/Design不变，运行B024/31保持。下一重点Network桥接提案，仍未接受来源约束放宽；B010延后。

## S0057：后台UI来源接受，取消方向待决

用户澄清禁止的是先打开窗口，不禁止后台UI数据。此前因纯Gameplay来源约束产生的BLOCKED/DESIGN_DECISION_REQUIRED不再适用，旧章节保留历史。下一步按[来源决定](../Reports/Technical/Specialization_Network_Background_Source_Decision.md)接后台当前集合与网络重建，来源可靠性不再反复争议；自身链路仍需验证。当前无新增用户决定/测试，B010延后；运行B024/31保持。

## S0058：B025后台网络小批次待测

[实现与范围](../Reports/Technical/Specialization_B025_Background_Network.md)：两个本地检查通过，部署无收益桥接/DEV Lv1网络诊断。[三个测试](Validation/Cases/B025_Background_Network.md)覆盖接入分发、读档、单来源撤销，沿用现有存档；不重测分页、不启动游戏。全AI/多人/高级ACTIVE/正式收益未实现，不因来源认可升级这些证据。Design不变，B010延后。

## S0059：B025计数API失败，B026首都优先复验

[两图失败](Validation/Results/Specialization_B025_Failure_Result.md)取代B025待测：请求抵达但Gameplay计数接口名错误。B026修正并两组本地通过，[沿用现存两城复验](../Reports/Technical/Specialization_B026_Trade_Count_Fix.md)，USER_GAME_TEST_REQUIRED。首都天然source自接入不等于免费recipient；无需先测商业城。网络收益未启用，B010继续延后。

## S0060：B026八图连接/分发/读档通过

[结果](Validation/Results/Specialization_B026_User_Result.md)取代S0059等待状态。第六图已连接文化；接入不等于本城接收。第七/八图全国科研接收城为纽约和阿伯丁，不是两个科研源。没有刷新错误证据。八图原件归档并校验一致，运行B026/33、Design、Source及Tests未变，无新增本地模拟。下一项改善诊断可读性并准备源/分发路线撤销小批次，当前不要求重复测试，不启用收益，B010仍延后。

## S0061：D0009同步，旧后续改动延后

[同步报告](../Reports/Technical/Specialization_D0009_Architecture_Sync.md)取代S0060关于当前recipient语义的解释。direct中心/首都自然接收已定，Commerce IV不是免费自接收而是Convergence。Source/Tests仍旧规则，已明确登记适配差距；未新增模拟/PASS。可读性与旧撤销批次DEFERRED_BY_USER，下一重点D0009接收适配与basis调查。本轮无需用户操作。

## S0062：B027直接接收已部署，Commerce IV初查

[报告](../Reports/Technical/Specialization_B027_Direct_Reception.md)记录两组本地PASS和HD名义yield来源账本先例。只派[纽约一个新判据](Validation/Cases/B027_Direct_Reception.md)，不是B026重复验收。Design/SQL/自动Lv1不变，旧NetworkState和旧fixtures的D0009统一尚待完成；Commerce IV精确basis与量化仍待技术研究。旧可读性/撤销批次DEFERRED_BY_USER，B010仍暂停。

## S0063：B027通过，商业IV总产出条件备选研究

[两图结果](Validation/Results/Specialization_B027_User_Result.md)取代待测，原件归档hash一致。用户允许精确本地basis困难时使用来源城市总产出，前提避免递归；[条件授权与研究](../Reports/Technical/Specialization_CommerceIV_Basis_And_Cycles.md)不自动改Accepted D0009。ConvergencePlan与新test本地通过，只是计划层；实际Getter上下文/精度/倍率及间接反馈未验证。下一步只读总产出诊断准备，无新用户测试/决定。运行B027/34、Design及既有Source/Tests未改，旧可读性/撤销批次继续延后。

## S0064：B028只读产出测试待回报

[报告](../Reports/Technical/Specialization_B028_Source_Yield_Probe.md)记录真实Gameplay getter探针及两组本地验证，USER_GAME_TEST_REQUIRED。只派现有科研城改变专家前后两图，不要求升级专业；没有新增高级收益或运行网络变化。

## S0065：B028两图复验通过

[结果](Validation/Results/Specialization_B028_User_Result.md)取代S0064待测。截图归档hash一致，未改运行/Design/Tests，没有新模拟或实机批次。下一重点汇聚收益承载的精度、倍率及反馈；高级Lv2–4仍未实现，旧可读性/断路批次继续延后。用户无需补测。

## S0066：B029固定收益承载待测

[报告](../Reports/Technical/Specialization_B029_Yield_Carrier.md)：HD property-gated城市收益先例、内存SQL验证及两组本地通过。只派整数/半点/重复/OFF一组测试，无需新高级专业。原生小数/倍率结果未定，不自动接受量化或最终收益被放大。Design、现有Tests、自动Lv1和网络模块不变，B010与旧网络批次继续延后。

## S0067：B029旧档整数档失败，排除初始化前提

[结果](Validation/Results/Specialization_B029_Old_Save_Failure.md)记录configured0→1但S/C/P无增量；重复不累加仅用户人工回报。用户确认旧存档，当前缓存六定义齐全但未证明运行实例。原GameInfo存在检查不足，不归咎小数、不强行Attach补挂。保持B029原代码，仅派新局首都+1/OFF对照；无需区域/商路。无新游戏PASS，B010和旧网络批次继续延后。

## S0068：B029新局整数通过

[三图](Validation/Results/Specialization_B029_New_Game_Result.md)确认新局+1三项读数与OFF恢复。旧档OFF无产出变化依用户补充保留；旧档失败不删除。新局对照支持初始化差异但未枚举实例。只补当前新局的半点/重复保持两图，不重开局、不测高级专业。原生UI在开启图仍旧值，精确区分Getter与UI证据。运行/Design/Tests保持，旧批次延后。

## S0069：B029半点未体现，不能按人工总体pass覆盖数值

[两图](Validation/Results/Specialization_B029_Fractional_Result.md)明确configured1.5但三项delta1，OFF归0。额外半点USER_GAME_TEST_FAIL，整数/关闭既有PASS保留；重复依人工回报。SQL 0.5文本存在不能证明引擎精度/实例激活。下一项本地调查，不擅自floor或重新派相同测试；运行/Design/Tests未改，旧待办继续延后。

## S0070：B030精度对照已准备

[本地调查及验证](../Reports/Technical/Specialization_B030_Precision_Control.md)通过，第二槽1.5取代诊断0.5；累计读数2.5/2/1帮助区分数值与激活问题。当前运行B030/37；只派一组新局两图，OFF正常口头回报。没有新实机PASS，不接受取整，不部署正式网络收益。Design、网络、自动Lv1及既有Tests保持；B010和旧网络批次继续延后。

## S0071：B030结果已复核

[三图](Validation/Results/Specialization_B030_User_Result.md)确认两档delta1/2、OFF0，当前实机测试已结束，取代S0070待测。精度限制待研究，不等于第二槽未激活或整个Getter整数化。未改运行/Design/Tests，不重发测试，不自动采用量化，B010及旧网络批次继续延后。

## S0072：按用户优先级暂缓小数、恢复网络待办

B031/38仅网络中文概况、城市名分页和计数失配拒绝旧报告；实际拓扑/后台发送器/收益无改动。两组本地验证通过，派现存商路删目的城一案。自然结束/战争/掠夺未测，不扩大结论。B010暂停，Commerce IV与小数承载后续研究，无设计改动。

## S0073：两图撤销通过、标签修复

[结果](Validation/Results/Specialization_B031_User_Result.md)及两图已归档、SHA256核对。当前只改两个XML标签及manifest39，网络Lua/收益/Design/既有Tests不变；不要求新局，不派单独标签测试。下次使用顺便确认即可，小数研究与B010继续暂停。

## S0074：共同成长前置执行层

新增离线executor和test，两组通过；正常1→4与重复不扣、已确认恢复不再消耗、未确认停止，Governor变化不丢Potential。静态找到HD Destroy先例，未声称本项目实机可用。当前运行存储只接受0/1且双记录一致，下一轮先解决兼容，不派新的总督或移民测试；小数承载/B010继续暂停。

## S0075：用户指定HD先例与存储衔接

奖励函数本身不删除单位，删除由通用UI后续请求执行；不能误认为已具备单请求事务。新InvestmentStoreBridge及测试完成，原执行器回归通过。运行/Design未改、不新增游戏测试，不把HD使用经验算作Specialization通过。下一轮原生Property及消费者接入，小数研究继续后置。

## S0076：B032只读接入完成

EffectiveFacts读取真实City Property、验证既有foundation，自动Lv1与网络共享该入口。无新账本自动写入；合成账本只在本地测试，未伪造实机投资。下一项写入及单位请求执行，旧标签下次顺便确认，小数/B010继续暂停。

## S0077：真实投资待用户验证

新增InvestmentAction并接Property/单位消耗。Prepare零写；Confirm同请求复验、INTENT、消耗确认、提交；normal load无重扣，CONFIRMED只补提交。真实API时序未测，失败不自动重试。本地UI/Gameplay分发、存储/单位边界和Lv1/网络回归通过，旧test与Design保持。唯一B033三步，不派其它批次。

## S0078：B033三图复核与人工补充

三图已按时间归档且hash一致；投资/重载通过。ACTIVE第三图2与人工总督操作一致；1级总督ACTIVE1正确。原网络无路线所以连续性未测，新建路线正常单独登记。无源码/测试修改或新模拟结论，不要求重复截图。下一步共同Lv2，未擅自接收益。

## S0079：B034共同Lv2住房交付

真实住房载体和自动门控已部署，50种当前HD建筑映射经静态核对，同层替代去重、隐藏标记排除；一组实际Lua/SQL检查及两组既有回归通过。只派B034一组三步；不重复投资或商路验收。GPP原生基础路径尚在研究，未改变SHARED-002。Design/既有Tests不改，变更前备份见B034报告。

## S0080：D0010正常sync

核对accepted hash与冻结D0009 diff；旧无专业取得模型曾统一first-completion，现明确拒绝旧入口，新增独立D0010模式契约与测试。已有Identity的休眠/转移/投资保留回归通过。当前无Conquest实机包，不编造待测按钮；运行/Design/住房案例不改。唯一活动实机批次仍B034。

## S0081：B034用户结果

五图已复核归档，hash一致。初始Potential2、总督建立触发ACTIVE2为原投资测试的有效门控变体；住房7/8/9，调离carrier0但UI9，下回合UI6。changes10→10排除下一回合才执行新的载体删除，仍不证明同回合原生Housing内部值。用户接受刷新延迟，按观察范围关闭本批；保存重载未回报，不扩大PASS或重发测试。只更新文档/证据，运行和Tests不变，下一项基础GPP。

## S0084：B035共同Lv2基础GPP交付

新增原生基础点数载体、Gameplay人数核对、独立后台dirty通知和UI全国率诊断。HD原有每人2应与新增2区分；新SQL在HD翻倍处理之后加载并复验最终定义。本地四组运行范围通过，原生倍率等仅USER_GAME_TEST_REQUIRED；一组三案，不重发其它批次。D0010/hash、UUID、配置、既有Tests不改；备份见B035报告。
