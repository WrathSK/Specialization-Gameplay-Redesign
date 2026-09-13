# Specialization P0 Status

Document Owner: Codex
Status Revision: S0019
Implementation Build: P0-B-014 / modinfo21
Architecture Revision Reviewed: A0017
Design Revision Reviewed: D0002
Latest Accepted Design Revision: D0002
Design Sync State: SYNCED_WITH_LIMITATIONS
Work State: B014_RESULTS_REVIEWED

## CURRENT AUTHORITATIVE STATE

本文件是唯一当前验证矩阵与待办队列。当前运行包B014/modinfo21，UUID不变；B010用户尚未测试且继续延后。用户已明确接受D0001，接受凭据和Spec SHA256见Design ChangeLog。A0005新增离线城市专业事实/Potential/ACTIVE模型；多源强度离线模型保留，正式商路来源仍阻塞；当前B014已接入DEV完成观察持久化，三图实机证据已登记，没有正式机制。
游戏设计意图以[当前Accepted D0002](../Design/Specialization_v0.1_Design_Spec.md)为权威；[Architecture A0017](../Architecture/Specialization_v0.1_Architecture.md)已记录适配与技术限制。设计接受不改变下方任何验证证据等级，本轮Research/Culture max仅离线实现/模拟通过，不代表引擎应用通过。

## CONFIRMED

| 项目 | 状态 | 范围 |
|---|---|---|
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

下表记录本地结果，具体执行轮次见各结果报告；本地模拟不等于Civ VI实机通过。

| 本地检查 | 已覆盖范围 |
|---|---|
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
| D0001接受 / A0002同步 | COMPLETE | 文档核对，不是游戏验证 | [同步记录](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)；未决设计和技术限制保留 |
| D0002规则/架构同步 | COMPLETE_WITH_LIMITATIONS | STATIC_CONFIRMED（文档差异与hash） | [同步报告](../Reports/Technical/Specialization_D0002_Architecture_Sync.md)；Future经验API尚未验证 |
| B011放置/完成及重载事件 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [实机结果与范围](Validation/Results/Specialization_B011_User_Result.md)；不重发本批 |
| 新城初始化/完成事实写入计划 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | [写入准备](../Reports/Technical/Specialization_City_Fact_Write_Plan.md)；没有引擎提交器 |
| 编号账本/写入故障恢复实验 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | [故障模拟](../Reports/Technical/Specialization_City_Identity_Storage.md)；真实代际凭据和持久性未验证 |
| B014 DEV完成记录 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [三图结果](Validation/Results/Specialization_B014_User_Result.md)；学院完成记录与重载保持，非正式专业 |
| B013 DEV新城绑定 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [五图结果](Validation/Results/Specialization_B013_User_Result.md)；普通新城/重载通过，不重测 |
| B012 DEV表存储 | COMPLETE_OBSERVED_SCOPE | USER_GAME_TEST_PASS | [五图结果](Validation/Results/Specialization_B012_User_Result.md)；不重复本批 |
| 真实城市代际凭据/首次账本资格 | OPEN_TECHNICAL | BLOCKED（正式身份接入） | fixture不能当引擎证据；缺失旧档/征服继承依OPEN-04 |
| B010首都/非首都ROLE | DEFERRED_USER_PAUSE | USER_GAME_TEST_REQUIRED | 用户明确尚未测试；[案例入口](Validation/Cases/B010_Deferred.md)，本轮不执行 |
| 标准缓存其它生命周期、自然结束/取消/掠夺/战争/征服/夷平 | DEFERRED | USER_GAME_TEST_REQUIRED | 不把Cheat删城当所有情形通过；另批最小案例，当前不派发 |
| Gameplay当前商路全集来源 | BLOCKED | STATIC_CONFIRMED（研究证据，非可用接口） | [第二轮复核](../Reports/Technical/Specialization_Trade_Authority_Second_Audit.md)；无新可验收候选，不派发测试 |
| 完成事件/区域族接入准备 | COMPLETE_OFFLINE_RESEARCH | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 官方/HD事件先例和离线候选通过；B011只读探针已部署 |
| 城市专业/Potential/ACTIVE离线状态 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | 完成事件与Property/单位事务未接游戏；UID和OPEN-04保留 |
| Research/Culture多源max离线适配 | COMPLETE_OFFLINE | LOCAL_SIMULATION_PASS | 尚未接正式路线来源或游戏Boost |
| 原生复制基数、GPP基础层、Gold-only折扣、Boost精度 | DEFERRED | USER_GAME_TEST_REQUIRED | 尚无完整实验包，不执行旧报告按钮 |
| Crew四案与巨作补贴 | NOT_IMPLEMENTED | BLOCKED | [延后案例](Validation/Cases/Deferred_Mechanics.md)，先具备实现 |

## BLOCKED / 技术及设计边界

- 纯Gameplay当前全集provider仍未确认，当前运行UI_SHADOW_ONLY没有成为正式权威网络。B005端点参数nil保留USER_GAME_TEST_FAIL候选记录。
- Industry多源合并、永久UID/继承、旧档首次完成初始化、首都本地资格与部分量化/分类问题见Architecture待决索引；Research/Culture多源L不再列为未决。
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
