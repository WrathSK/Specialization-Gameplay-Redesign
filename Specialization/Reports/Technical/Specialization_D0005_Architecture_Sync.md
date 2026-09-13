# D0005同步与本地模型适配

Document Owner: Codex
Architecture Revision: A0020
Design Spec Synced Through: D0005
Design Spec SHA256: ca5af83f6ab722e80199c47add0dae781a1d06d34c74404a6666af08028c80a0
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-014 / modinfo21（不变）

## 结果与设计适配

本轮按用户确认的D0005执行。Design两文件及所有设计快照未修改；当前规则只引用Spec，不在报告建立第二份数值表。

STATIC_CONFIRMED：D0005/hash与ChangeLog一致，差异为下列规则及OPEN索引；仅静态/文档证据，不表示游戏通过。其余D0004映射沿用[上一轮报告](Specialization_D0004_Completion_Journal.md)。

| Rule | 当前HOW | 取代旧假设 |
|---|---|---|
| NET-001/002 | NetworkState依据调用者已验证的当前isCapital角色添加CAPITAL_SELF_CONNECTION原因；不造商路，不创建recipient。角色变化后重新派生撤销旧原因 | 首都source自接入不再设计待决；普通中心仍不自动取得该例外 |
| IND-004 / IND-NET-001/003 | IndustryNetwork从每个recipient的center/source资格取有效源，分别计算实际IV output最大值、模板并集、最高Gold折扣；保留各项来源用于撤销与诊断 | 不再DESIGN_DECISION_REQUIRED；不把Research/Culture最高L当工业实际output，不要求模板与折扣同源 |
| IND-NET-002 | DiscountFor只提出Gold候选折扣，Faith/无模板/非recipient返回0；正常购买资格仍由未来引擎层核对 | 本地Gold过滤不是Gold-only Modifier实机证据，不使用退款fallback |
| PROG-004 | State.TransferOwnership需显式MOCK VERIFIED_SAME_CITY凭据、旧/新owner、UID及预期revision一致；只复制永久事实，递增revision并要求重算新Owner派生状态 | owner不同返回技术UNKNOWN，不再返回继承设计待决；未经验证不能仅改owner |
| PROG-005 / OPEN-04 | 完成顺序保持D0004；旧档初始化仍设计待决，跨owner UID识别为技术审查 | 不重新开放同时完成规则；不将技术识别困难变成不继承设计 |
| OPEN-05/07 | 从当前待决映射撤下，历史原报告保留 | 当前正文以D0005覆盖旧未决，历史文件不回写 |

## 新/修改的本地模型

- DevelopmentTests/NetworkState.lua：首都source原因及工业状态NOT_CALCULATED；仍不发放收益。
- DevelopmentTests/IndustryNetwork.lua：显式MOCK_ONLY入口，拒绝UI_SHADOW为正式计算依据；模板细节版本必须匹配来源templateRevision；Lv4 output由调用者提供经过验证的实际输出，不自行用相邻getter替代Actual。逐recipient来源避免把未接入该城市的其它工业中心收益泄漏进来。
- DevelopmentTests/CitySpecializationState.lua：新增TransferOwnership与ownedTemplates永久字段。旧离线schema1缺ownedTemplates时为空；这是本地fixture兼容，不是将旧游戏存档模板缺失解释为真实空集的迁移策略。保留投资receipt、首次完成与Potential；不复制ACTIVE、receivedTemplates或Network Strength等缓存。允许经过验证的事实在非测试文明持有及再征服中保留，不为其它文明注册游戏能力。
- 原城市状态/写入计划测试更新owner不一致的预期：等待验证转移，非DESIGN_DECISION_REQUIRED。

## LOCAL_SIMULATION_PASS

本地模拟通过，不等于Civ VI实机通过。实际执行七组脚本，均exit=0；前缀 `PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/`：

| 脚本 | 本轮检查 |
|---|---|
| test_d0005_models.py | 首都无路线可接源但不能自接收；分发有效；首都角色改变/owner不匹配撤销；普通中心无例外；工业output取31而非18+31；低级源模板享高级源折扣；另一recipient不能借用不连通模板；重复/断源/ACTIVE降低重算；Faith候选0；版本冲突及UI/GAMEPLAY错误入口拒绝；征服与再征服保留Lv4投资和自身模板、清旧缓存、防旧凭据重放 |
| test_city_specialization_state.py | 四族、通知顺序、永久投资/上限、ACTIVE与恢复回归 |
| test_city_fact_write_plan.py | 新城/加载/重复/旧档拒绝回归 |
| test_city_completion_journal.py | 新城资格、错误缺口、单表拟写入、新VM恢复回归 |
| test_network_multisource.py | Research/Culture原max/sqrt、去重及源撤销不受影响 |
| test_shadow_network_state.py | UI影子与正式权威隔离；原拓扑回归 |
| test_trade_route_state.py | MOCK当前全集、撤销、恢复、幂等回归 |

输出中的旧测试脚本“no merger”只描述各自覆盖模块；本轮新工业合并由test_d0005_models单独验证。没有新增USER_GAME_TEST_PASS。

## 阻塞与下一步

纯Gameplay路线权威全集、实际IV output读取、Gold-only Modifier仍未确认；本地计算通过不能用于解锁正式收益。跨owner/current cityID的可靠永久UID没有实现；TransferOwnership的凭据是测试输入，不是引擎API发现。真实新城资格与事件写入器也尚未部署。

后续新城提交器必须保留持久事实与当前owner关联的分层：正常建城初始化独立进行；owner变化时停止旧owner事件处理，等待可靠同城证据执行事实转移，不能重置专业或报“继承设计未决”。CityCompletionJournal目前未接TransferOwnership，不能只替换内层facts造成外层owner/UID不一致；未来提交需同时核对整体记录并重建网络资格。此边界作为下一轮实际提交器的前置约束。

本輪不部署B015，不重复B011–B014，不重发暂停的B010；用户现在无需操作。设计已明确的三项无需再次询问。

## 文件保护

修改前副本及运行/Design校验清单保存于DevelopmentBackups/Specialization-before-D0005-sync。完成后逐项核对运行包与Design文件hash未变，UUID/游戏配置未改；未启动游戏。当前文档A0020/S0022，冻结历史报告保留旧结论及审计痕迹，当前规则由本次同步覆盖。
