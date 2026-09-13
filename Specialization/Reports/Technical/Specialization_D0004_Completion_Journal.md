# D0004同步与新城专业记录准备

Document Owner: Codex
Architecture Revision: A0019
Design Spec Synced Through: D0004
Design Spec SHA256: a3fd779fdcb166ecd3d39e1560fabe26ef3d26cb67c499ab632c9dac7eeebbab
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-014 / modinfo21（未变）

## 本轮结论

用户确认PROG-005，按有效完成通知交付顺序锁定；排序待决已解决，旧城初始化和征服继承仍见OPEN-04。D0003冻结原文、D0004正文与ChangeLog均已登记，Community框架保留。本轮没有改变运行包、UUID、配置或启动游戏。

STATIC_CONFIRMED：文档规则/hash与本地调用契约已核对；不是引擎运行通过。
LOCAL_SIMULATION_PASS：下述四组本地脚本exit=0，不等于Civ VI实机通过，没有新增USER_GAME_TEST_PASS。

## 已实现的离线逻辑

- CitySpecializationState.Complete显式要求orderBasis=ENGINE_DELIVERY，按原列表先后取第一个已完成四族候选，不按区域类型/ID/回合排序。旧完整列表接口仅作为兼容离线入口，不再需要等引擎提供“同时完成批次结束”来决定专业。缺少顺序依据的列表仍UNKNOWN。
- CityCompletionJournal在同一个拟写入表中保存新城资格、通知序号、历史缺口、专业事实。Foundation只允许MOCK_ONLY已验证建城/绑定/监听就绪/完整扫描且零已完成四族候选；已有记录只恢复，不重置。
- 每个有效通知独立生成单事件写入计划，顺序游标与专业事实一并提交。后续通知不能覆盖专业或重置Potential；相同序号相同内容幂等，冲突/跳号/过期拒绝。序号是未来单一Gameplay处理器自行维护的内部投递序号，不宣称引擎提供持久event ID；重放判定仍需真实适配器。
- Gap生成持久历史缺口计划。缺口记录读档后继续阻止新的专业初始化，后续成功不清除缺口。旧B014观察没有建城资格，不能Restore或Foundation迁移；只读操作返回副本。

## 四组实际本地验证

命令前缀 `PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/`：

| 脚本 | 结果与有意义的范围 |
|---|---|
| test_city_completion_journal.py | PASS：资格缺失逐项拒绝；学院/剧院相反顺序；重复/冲突/跳号；旧DEV拒绝；拟写入前不改原值；过期提交拒绝；历史缺口；JSON往返后新Lua VM恢复 |
| test_city_specialization_state.py | PASS：四族、通知顺序改变专业、非交付顺序拒绝、投资防重复及上限、总督ACTIVE、读档永久事实 |
| test_city_fact_write_plan.py | PASS：新城/加载隔离、重复建城保留投资、多个有序候选取首个、模拟过期计划拒绝 |
| test_completion_history_boundary.py | PASS：旧B014历史不可反推的反例仍成立；不因D0004改变既有实机证据 |

## 尚未完成的真实提交器

CityCompletionJournal仍是DevelopmentTests离线准备，不注册事件或调用Property，没有持久化游戏事实。本地MOCK资格不是引擎证明，Gap也需要调用者主动提交：遇UNKNOWN/写入未确认时，未来实际处理器必须立即停止该城市继续处理、重读提交结果，并尝试记录缺口；不能像B014那样继续下一通知。

若连缺口标记也无法保存，当前会话应维持停止状态，不能承诺崩溃/读档后仍可检测该失败；写入成功但setter报错需要通过读回判定，不能盲重试。跨两个Property的绑定准备与专业记录不是原子事务，本模块不声称解决。缺少完整新城历史、Mod停用再启用、征服与城市引用复用限制保留；正式旧档策略不自行选择。

下一步是使用已有B013/B014实测接口准备受限的新城提交器及诊断，先核对真实建城时完整扫描和错误停止，再部署最小测试包。只有有新代码可验证时才派发实机批次，本轮无新批次，B010延后。

## D0003 / D0004架构同步差异

D0003整体技术适配此前待审；本轮仅完成架构层规则映射，不对Future接口开展调查或实现。沿用D0002其它映射（见既有同步报告），差异对应如下：

| Rule | HOW及限制 |
|---|---|
| COMM-001 | Future特殊候选单独分类，不混入v0.1四族；锁定优先级仍TBD，不套PROG-005解决所有Community边界 |
| COMM-002/003 | 分离国际新增人口与国内搬运事务；撤销旧国内sqrt迁移模型适配方向；实际人口API/事务未验证 |
| COMM-004/005 | 保护基盘与recipient合法性先检查，国内输出不能扣至基盘以下；基盘/排序TBD不硬编码 |
| COMM-006 | 实际专家额外产出按等级替换，避免同叠；不复制HD Gold；岗位产出层仍待实现 |
| COMM-007 | Housing余量、正宜居、建筑tier、真实专家分别采样；虚拟专家不默计，分类/数据读取待研究 |
| COMM-008 | 进度与国际累计账本独立，人口增加与进度扣除需事务恢复；C_met/C_map定义及大额多次结算TBD，不实现计数 |
| COMM-009 | 三种政策状态持久保存，暂停期间不追补；项目成本/解锁未定，不添加状态 |
| COMM-010 | 以国际成功吸引累计与奖励余额为依据，国内移出不冲减；生成Settler的去重/失败恢复另案，暂定阈值不是最终平衡 |
| COMM-011 / OPEN-14 | 接受框架不解决TBD，不因同步而变成已实现 |
| PROG-004/005 / OPEN-04 | 通知先后采用，完成批次并列排序不再阻塞；旧档/征服继续待决；本文单事件离线计划不冒充真实历史资格 |

SYNCED_WITH_LIMITATIONS只表示上述差异已反映在架构，Future Community不进入当前v0.1，没有API或游戏验证升级。
