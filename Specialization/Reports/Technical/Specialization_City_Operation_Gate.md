# 城市操作入口与提交前复核：离线准备

Document Owner: Codex
Design Reference: D0007 / ELIG / PROG
Architecture Reference: A0034
Scope: MOCK_ONLY / NO_ENGINE_WRITER

## 结果

LOCAL_SIMULATION_PASS：新增CityOperationGate.lua与test_city_operation_gate.py，组合实际离线EligibilityLifecycle、CityFactWritePlan及CitySpecializationState验证通过；不等于游戏实机通过。既有模块、运行B018及Design不改。

Prepare仅接受MOCK_ONLY/AFTER_LOAD_CLOSE与FOUNDATION或COMPLETION_BATCH。先取得当前玩家许可，才能调用城市解析器；解析后再核对许可，要求当前owner、有效cityUID和present证据。门控将已确认的MOCK许可映射到State所需资格输入，不信任解析器自行提供的ENABLED。

计划仍由现有CityFactWritePlan及State规则生成；没有绕过新城历史资格、完成通知顺序或旧档保护。仅PLAN_ONLY结果存入私有计划表，外部只获句柄。重复/无变化或错误结果直接返回，不产生可提交句柄。

CheckForCommit是一次性的计划复核，先检查许可再重新解析城市，比较owner/代际/完整身份证据以及原始永久事实全部内容，再确认许可。不能只比较revision；相同revision但内容变了也拒绝。旧、伪造、其它实例或已使用句柄不通过。失败也消费该计划尝试，需要重新规划。

返回CHECKED_PLAN_ONLY及计划副本，不调用任何setter。模型不存在城市事实保存或清空入口；未启用Owner的休眠成果仍由独立永久事实层保留，不能靠“拒绝参与”删除。

## 测试范围

未就绪/disabled无城市读；有效新城计划复核；失效后不读城市；一次性句柄；易主/毁城/引用复用代际变化；事实出现或同revision模板变化；读取期间资格失效；与真实离线Completion规划组合。原始facts不改，没有模拟为已成功写入。

## 实际入口审计与限制

现有运行CityJournalProbe.lua的read/write函数以DEV Binding token、owner/cityID、位置/schema为约束；write前比较原表、写后确认。它仍由测试文明门控，B018私有诊断许可没有接到该写入器，不能将本轮离线模块直接宣称已保护真实写入。DEV身份不是正式永久UID。

当前新模块的resolve是调用方MOCK证据，不是新发现的引擎跨owner城市识别。事实副本限制嵌套深度，不用于通用引擎对象编码。这里只限制单个计划的提交尝试，并不解决多计划并发事务。

CheckForCommit返回到真正setter之间仍存在边界：生产实现必须在同一受控提交路径内重核/写入/读回，不能把返回结果作为可无限延迟的写入授权。实际事件失效、写后不确定性、重入、失败停止、崩溃恢复与已附着收益撤销尚未接入。尤其不能声称“setter调用后报错”一定没写成功。

## 下一步

准备与计划复核紧邻的提交/读回恢复路径，先本地验证写前失败、写后抛错和并发变更，再决定最小DEV运行接入；正式专业收益仍关闭。本轮没有新用户测试，不重复B018或B010。

备份及保护hash：DevelopmentBackups/Specialization-before-city-operation-gate。未启动游戏、未改配置或UUID。当前任务与证据见[Status](../../Status/Specialization_P0_Status.md)。
