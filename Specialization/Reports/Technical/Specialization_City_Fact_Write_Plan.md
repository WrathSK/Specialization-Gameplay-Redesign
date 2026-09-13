# 新城与完成事实写入准备 — A0009

Document Owner: Codex
Design Reference: D0002 PROG-001..004 / OPEN-04
Runtime: B011 / modinfo18（本轮未改）

## 用户摘要

新增离线写入计划，用B011观察到的顺序检验：市中心通知不产生专业，建城重复通知不重置投资，读档不将已有区域视为刚完成。三组本地测试通过，尚未写入真实存档。用户现在无需操作；下一步需解决可持久识别城市的技术编号，以及引擎实际写入/读回边界。

## 分层与接口

DevelopmentTests/CityFactWritePlan.lua注入已有CitySpecializationState，只接显式MOCK_ONLY身份和模拟阶段。Plan返回拟写数据及expectedAbsent/expectedRevision/cityUID/owner，或不写入/未知/待设计；没有SetProperty、单位消费、事件注册或生成UID。

- FOUNDATION：必须在模拟AFTER_LOAD_CLOSE；有记录时先Restore并保留原投资，不调用NewCity覆盖；无记录仅允许freshFoundationObserved真实新城前提（当前为fixture提供）。
- RESTORE：允许加载阶段验证已有记录；缺失记录保留OPEN-04，不扫描现有区域生成历史。
- COMPLETION_BATCH：复用已有Complete，要求外部提供已确认完整/有序批次及永久身份。单个原生完成事件没有升级成这个契约，B011也未证明所有同时完成顺序。
- 原始DistrictAddedToMap/OnDistrictConstructed不是写入命令；原生候选由已有DistrictCompletionCandidate单独过滤NON_V01/对象不匹配，不跳过此边界。市中心不能初始化专业。

计划不是提交结果，PLAN_ONLY不能向游戏面板宣称专业已存在。模拟提交器比较计划前提，实际Gameplay writer尚不存在。expectedRevision本身不构成事务：真实写入前需重读、核对当前所有权/代际/版本，串行处理后再读回；写入异常或读回不符不得重复发放收益或把未知当空。引擎在写入期间保存/回调的行为尚待验证。

## 身份及生命周期准备

owner/cityID用于当前寻址，不用作永久UID；城市中心plot也不是永久UID。推荐研究首次合法建城分配持久代际token、城市Property保存同一个事实表的方式，但分配器与城市记录跨对象写入可能部分成功，必须先研究重试/恢复。现在不将这个建议当已实现机制。

新建正常城市可独立推进；征服是否继承、旧档如何初始化、同时完成如何排序仍属于OPEN-04。对这些情形暂停拟写，是防止实现猜测的保护，不是用户已决定丢失投资。读档扫描仅恢复存在且有效的记录，不根据已完成区域回填首次完成历史。

## 验证

LOCAL_SIMULATION_PASS仅指本地Lua模拟通过，不等于Civ VI实机。

- test_city_fact_write_plan.py：B011市中心→建城→放置→完成序列；重复初始化/完成；真实fixture投资后重复建城保持；加载期拒绝写入；已存记录恢复与副本隔离；缺失旧档、易主、代际冲突、损坏记录、非测试文明、未知上下文、同时候选拒绝；fixture提交器拒绝重复/过期计划。
- test_city_specialization_state.py：既有专业/Potential/ACTIVE、投资凭据及新Lua VM恢复回归通过。
- test_district_family.py：区域替代族与候选过滤回归通过。

执行：PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/<上述脚本>。三项exit=0。依赖复用本机已有lupa，没有安装工具或启动游戏。

USER_GAME_TEST_REQUIRED表示将来需要用户在游戏中验证：真实城市代际与Property表保存、重复写入、正常跨回合完成与恢复等；目前没有这部分运行代码，不派发空测试，也不重测B011/B010。

## 下一步验收门槛

先设计并本地验证代际分配/恢复及单城事实表写入失败路径，再准备窄范围存储探针；探针部署前明确是否新局、写哪些Property、旧档不回填。正式Settler事务/收益/网络不接入。未来存储探针通过也不自动解决OPEN-04或批次权威。
