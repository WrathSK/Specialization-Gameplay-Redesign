# 城市成果与恢复记录统一存储：离线适配

Document Owner: Codex
Architecture Revision: A0039
Design Reference: Accepted D0007（不修改设计）
Verification: LOCAL_SIMULATION_PASS
Runtime: P0-B-018 / modinfo25（本轮未改）

## 结论与范围

新增 `DevelopmentTests/UnifiedCityEnvelope.lua`，将既有 CityOperationGate、PendingCityRecovery 和 CityFactWritePlan 接到同一个注入存储单元。不是另一个平行提交器。仅 MOCK_ONLY，一城市一通道；没有 Civ VI API、事件注册或正式收益。

统一表包含 schema、kind、owner、cityUID、storageRevision、facts、record。facts保留永久成果；record保留最近操作的before/target及PENDING/DONE。storageRevision是每次整表保存的序号，不是Potential或事实revision。record不是完整历史账本，不保证跨城市/跨存档全局操作ID唯一。

| 保存阶段 | facts | record | 重新加载后的处理 |
|---|---|---|---|
| 记下计划 | 原值（初建可nil） | PENDING，含目标 | 保持暂停，不自动重做/删除 |
| 写入成果 | 目标值 | 同一个PENDING | 新许可与同城核对后可显式写DONE |
| 完成对账 | 目标值 | DONE | 核对后开放下一笔；不重写成果 |

第二笔用新PENDING替换上一笔DONE，before必须等于当前facts。每阶段整表写一次，之前重读完整表比较，之后读回完整表确认。setter抛错不等于未写入；精确读回决定结果，不盲重试。空值仅在调用方提供已观察到新建城证据时可创建；nil不证明旧城从未参与。现有B012–B015数据不自动迁移。

## 本地结果

`test_unified_city_envelope.py`实际组合六个Lua模块，覆盖初始化与学院完成连续两笔、六个保存截点经JSON进入全新Lua VM、三个阶段分别丢写/写后抛错、重复操作不写、坏表/身份改变/读取失败拒绝，以及写前发现整表变化后不覆盖。另五组提交/恢复回归通过，合计六个脚本exit=0。

LOCAL_SIMULATION_PASS表示本地模拟通过，不等于Civ VI实机通过。精确输出与保护范围校验见 `DevelopmentBackups/Specialization-before-unified-city-envelope/`。未产生任何新的USER_GAME_TEST_PASS。

## 技术限制

单表消除了两个Property之间的配对依赖，但不证明引擎的崩溃原子性或落盘耐久性。写前比较不是引擎级compare-and-swap；读与写之间没有真实引擎锁，仍需单写入入口和事件时序验证。外部同值重写及恶意伪造合法表不在模型保证内。深度/可序列化检查也不替代完整游戏事实语义校验，目标由现有planner产生。

原值PENDING仍暂停，未自动设计ABORT/重做策略。永久城市UID、跨owner识别、事件期间资格撤销、真实资源消耗都未解决。本轮无需新增设计决定；若后续恢复策略改变游戏投资语义，必须先报告。

## 下一次最小DEV接入范围（尚未部署，不要求现在测试）

下一项应为独立合成DEV记录的单Property分阶段保存/重载探针，复用本轮转换校验，不冒充真实城市身份，不复制运行目录，不触碰B015表。由专用按钮分别停在“计划已记”和“成果已写”，加载完成后自动只读判定并显示中文阶段、记录号、写入次数；显式对账后保留DONE。计划两案，使用现有测试存档即可；不要求造区域、花资源或异常退出游戏。测试重点是中间阶段的恢复分类和后续连续提交，而非重复B012普通表序列化。

上述实际Game Property适配与UI尚未编写，因此本轮没有可派发游戏测试。最小探针通过也只证明正常保存重载，不承诺游戏崩溃安全。
