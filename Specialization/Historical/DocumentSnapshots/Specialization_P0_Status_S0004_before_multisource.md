# Specialization P0 Status

Document Owner: Codex
Status Revision: S0004
Implementation Build: P0-B-010 / modinfo17
Architecture Revision Reviewed: A0002
Design Revision Reviewed: D0001
Work State: PAUSED_AFTER_ARCHITECTURE_SYNC

## CURRENT AUTHORITATIVE STATE

本文件是唯一当前验证矩阵与待办队列。当前源码仍B010，UUID不变；B010用户尚未测试。用户已明确接受D0001，接受凭据和Spec SHA256见Design ChangeLog。A0002已完成D0001规则映射，Sync Status为SYNCED_WITH_LIMITATIONS；P0功能开发继续暂停。
游戏设计意图以[Accepted D0001](../Design/Specialization_v0.1_Design_Spec.md)为权威；[Architecture A0002](../Architecture/Specialization_v0.1_Architecture.md)已记录适配与技术限制。设计接受不改变下方任何验证证据等级，也不表示Research/Culture max合并已实现。

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

以下为迁移前已有结果；本次仅整理文档，没有重跑游戏或功能测试。

| 本地检查 | 已覆盖范围 |
|---|---|
| test_specialization_p0.py / test_specialization_identity.py | Lua/XML、窄请求、身份SQL/资源引用；部分环境为fixture |
| test_city_role_facts.py | B010只读角色、未知专业/潜力、总督条件上限；不是实机PASS |
| test_background_routes.py / test_trade_route_probe.py | 后台批次、错误/重试、加载与Gameplay任务诊断 |
| test_shadow_route_state.py | 标准缓存全量替换、复制读取、revision、UNKNOWN/reset |
| test_trade_route_state.py / test_shadow_network_state.py | MOCK来源、角色/模板/ACTIVE变化、去重/撤销、UI来源隔离 |
| test_specialization_network.py | 单一给定L的sqrt/独立k/城市去重；未验证D0001要求的多源max实现 |

## 唯一当前待办队列

Task State与Verification分列，暂停不是失败，也不建立新的验证状态枚举。

| ID/任务 | Task State | Verification | 前置/下一步 |
|---|---|---|---|
| D0001接受 / A0002同步 | COMPLETE | 文档核对，不是游戏验证 | [同步记录](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)；未决设计和技术限制保留 |
| B010首都/非首都ROLE | DEFERRED_USER_PAUSE | USER_GAME_TEST_REQUIRED | 用户明确尚未测试；[案例入口](Validation/Cases/B010_Deferred.md)，本轮不执行 |
| 标准缓存其它生命周期、自然结束/取消/掠夺/战争/征服/夷平 | DEFERRED | USER_GAME_TEST_REQUIRED | 不把Cheat删城当所有情形通过；另批最小案例，当前不派发 |
| Research/Culture多源max适配 | PAUSED_IMPLEMENTATION | 尚未实现/验证 | 设计已定且已同步；恢复开发后先改离线实现/测试 |
| 原生复制基数、GPP基础层、Gold-only折扣、Boost精度 | DEFERRED | USER_GAME_TEST_REQUIRED | 尚无完整实验包，不执行旧报告按钮 |
| Crew四案与巨作补贴 | NOT_IMPLEMENTED | BLOCKED | [延后案例](Validation/Cases/Deferred_Mechanics.md)，先具备实现 |

## BLOCKED / 技术及设计边界

- 纯Gameplay当前全集provider仍未确认，当前运行UI_SHADOW_ONLY没有成为正式权威网络。B005端点参数nil保留USER_GAME_TEST_FAIL候选记录。
- Industry多源合并、永久UID/继承、旧档首次完成初始化、首都本地资格与部分量化/分类问题见Architecture待决索引；Research/Culture多源L不再列为未决。
- 旧总督Lua getter、Gameplay city:GetTrade缺失、B006/B007调度失败均保留历史范围；后续修复的PASS不倒写旧报告。

## 文档整理验证

迁移与文件校验详见[第一阶段交付报告](../Reports/Proposals/Specialization_Phase1_Migration_Report.md)。现有Source/Tests未改，不能把文档链接检查称为功能回归通过。

A0002同步已完成：[规则映射与校验](../Reports/Technical/Specialization_D0001_Architecture_Sync.md)。建议恢复工作时先完成离线多源max适配，再处理正式网络权威来源；B010仍保持用户延后，不自行派发测试。
