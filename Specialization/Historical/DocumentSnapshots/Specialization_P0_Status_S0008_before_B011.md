# Specialization P0 Status

Document Owner: Codex
Status Revision: S0008
Implementation Build: P0-B-010 / modinfo17
Architecture Revision Reviewed: A0006
Design Revision Reviewed: D0001
Work State: COMPLETION_ADAPTER_PREPARED_RUNTIME_UNCHANGED

## CURRENT AUTHORITATIVE STATE

本文件是唯一当前验证矩阵与待办队列。当前源码仍B010，UUID不变；B010用户尚未测试。用户已明确接受D0001，接受凭据和Spec SHA256见Design ChangeLog。A0005新增离线城市专业事实/Potential/ACTIVE模型；多源强度离线模型保留，正式商路来源仍阻塞，运行功能本轮未扩展。
游戏设计意图以[Accepted D0001](../Design/Specialization_v0.1_Design_Spec.md)为权威；[Architecture A0006](../Architecture/Specialization_v0.1_Architecture.md)已记录适配与技术限制。设计接受不改变下方任何验证证据等级，本轮Research/Culture max仅离线实现/模拟通过，不代表引擎应用通过。

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

## LOCAL_SIMULATION_PASS

下表记录本地结果，具体执行轮次见各结果报告；本地模拟不等于Civ VI实机通过。

| 本地检查 | 已覆盖范围 |
|---|---|
| test_specialization_p0.py / test_specialization_identity.py | Lua/XML、窄请求、身份SQL/资源引用；部分环境为fixture |
| test_city_role_facts.py | 本轮回归通过；B010只读角色、未知专业/潜力、总督条件上限；不是实机PASS |
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
| B010首都/非首都ROLE | DEFERRED_USER_PAUSE | USER_GAME_TEST_REQUIRED | 用户明确尚未测试；[案例入口](Validation/Cases/B010_Deferred.md)，本轮不执行 |
| 标准缓存其它生命周期、自然结束/取消/掠夺/战争/征服/夷平 | DEFERRED | USER_GAME_TEST_REQUIRED | 不把Cheat删城当所有情形通过；另批最小案例，当前不派发 |
| Gameplay当前商路全集来源 | BLOCKED | STATIC_CONFIRMED（研究证据，非可用接口） | [第二轮复核](../Reports/Technical/Specialization_Trade_Authority_Second_Audit.md)；无新可验收候选，不派发测试 |
| 完成事件/区域族接入准备 | COMPLETE_OFFLINE_RESEARCH | STATIC_CONFIRMED / LOCAL_SIMULATION_PASS | 官方/HD事件先例和离线候选通过；下一步只读探针，未派发实机批次 |
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
