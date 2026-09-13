# 城市专业状态本地结果

Document Owner: Codex
Design Revision: D0001
Architecture Revision: A0005
Verification: LOCAL_SIMULATION_PASS
Runtime Build: P0-B-010 / modinfo17 (UNCHANGED)

LOCAL_SIMULATION_PASS只表示本地Lua模型通过，不是Civ VI游戏验证。没有新Property写入、游戏事件注册或真实单位消费，没有把B010变成PASS。

## 本轮执行（均exit 0）

命令前缀：`PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/`；复用既有lupa，没有安装新依赖。

- test_city_specialization_state.py：四种v0.1区域族完成锁定；未完成/非v0.1不锁；重复通知不重复锁定，后建区域不改专业；多候选同时完成返回设计未决；稀疏/未审计/跨玩家批次拒绝；投资预检查、不消费输出、预期revision校验、receipt重复、单位重复、满级/无专业拒绝；各Potential与总督门槛组合；移走仅降ACTIVE；输入/输出副本隔离；JSON序列化后新建Lua VM恢复，故意注入旧ACTIVE后重新计算；旧档无事实、征服、重建新代际、城市失效、非测试文明、坏schema/坏账本拒绝；原Probe.CityRoleFacts总督absence/未建立/建立/晋升/调离/不一致/控制Property缺失的离线桥接。
- test_city_role_facts.py：原B010只读角色回归，无真实游戏调用。
- test_network_multisource.py：既有多源离线集成回归，不新增引擎效果。

## 证据限制

- freshFoundationObserved、完整有序完成批次、VALIDATED_FAMILY及城市/单位UID都是明确fixture输入；没有实现引擎身份、替代区域数据库解析或完成事件适配。
- JSON/新VM恢复只检验数据模型可恢复，不替代City Property实机存读。既有Marker实机PASS也不自动覆盖本账本。
- CommitInvestment接收的是模拟已提交消费凭据；PlanInvestment不是实机按钮。游戏中的单位消耗与Property持久化事务仍需设计/验证，不能宣称已能可靠消耗Settler。
- OPEN-04仍在Spec中：不补认旧城专业、不决定征服继承、不同步排序同时完成事件。模块返回未决是保护边界，不新增玩法处罚。
- Governor probe结果只在mock城市中桥接，并显式附加fixture UID；不扩展用户A007/B010验证范围。

## 文件和范围

新增CitySpecializationState.lua及test_city_specialization_state.py；更新Architecture A0005、Status S0007与入口说明，旧文档新增冻结快照。Accepted Spec、运行源码/UUID、既有Tests、备份、截图和既有验证结果不改；无游戏启动或新实机批次。
