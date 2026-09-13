# D0007架构同步（包含D0006差异）

Document Owner: Codex
Architecture Revision: A0023
Design Spec Synced Through: D0007
Design Spec SHA256: 15e011b665c6a53232673f8195d88acca954f80aa0d18efcdd256d1995cd3d88
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-015 / modinfo22（未改）

## 结论与证据等级

当前设计为D0007 ACCEPTED，hash与ChangeLog一致。架构原整体同步至D0005，本次补齐D0006 Military IV及D0007 Eligibility/征服交互，未修改Design。

STATIC_CONFIRMED：设计差异、源码中现有门控与文档引用已静态核对；不等于实际资格过滤、AI、多人或游戏通过。本轮不运行模拟或游戏测试，不新增LOCAL_SIMULATION_PASS或USER_GAME_TEST_PASS。此前B015三图PASS范围保持。同步仅表示HOW与实现缺口已明确，不表示新规则已部署。

## D0007 Rule映射

| Rule | HOW / 实现约束 |
|---|---|
| ELIG-001 | 正式层引入独立PlayerEligibility入口，输出明确启用/未启用/无法确认及原因；不可用Human、local player或测试文明名字替代。资格未知时不发收益或新建事实，也不删除已保存事实。具体carrier/API尚未选择。 |
| ELIG-002 / ID-001 | 将当前白板文明、领袖、Trait与展示资源视为一种载体配置；核心机制只消费资格，不硬编码该载体。现有Mod UUID/选人配置保持；本轮不启用其它文明或新模式，不修改其原有能力。 |
| ELIG-003 | Gameplay入口不按Human排除AI；UI仅负责人类交互，不能成为AI运行前提。既有Settler/项目/商路等合法行为走同一规则；无额外planner、补偿、阉割或效果承诺。 |
| ELIG-004 | 初始化建立参与者集合；周期处理、城市枚举、网络派生、军事/人口更新只面向该集合，事件先判断所属玩家资格再深读对象。不为未启用者建立新专业表或维护派生缓存；资格变更边界必要的旧效果撤销与永久成果保存不等于对其持续运行。入口筛选仍有轻量开销，不宣称性能已测或绝对零指令。 |
| ELIG-005 / PROG-004 | 分离永久城市成果、当前所有权、Owner资格和派生效果。新增“正常取得未专业化城市”接入路径，不能伪造CityBuilt或把现有区域排序当首次专业；休眠只保存成果，恢复先核实同城/新Owner资格再重算。四种情形见下表。 |
| ELIG-006 / COMPAT-001 | 多玩家/AI资格、载体可复用及征服休眠是已确定scope。具体carrier、多人确定性、AI行为质量、过滤成本及旧档迁移为实现/未来兼容事项；不重新列为核心玩法待决。 |
| PROG-005 | 保持有效完成通知顺序。新建城与取得无专业成果城市采用不同资格来源；不把缺失记录自动当成从未参与，也不扩充旧DEV记录的历史证明。 |
| OPEN-04 | 旧档迁移与永久UID列IMPLEMENTATION / FUTURE_COMPATIBILITY。此分类不授权猜测或自动迁移缺失历史，不等于迁移已解决。 |

### 征服 × Eligibility：适配流程与验收目标（未部署）

| 观察情形 | 未来处理 | 不能做什么 |
|---|---|---|
| 有证据从未启用、无永久成果 → enabled | 以未专业化状态进入系统，后续有效专业完成/投资走正常规则 | 仅凭AI身份或Property为空断言从未参与；从现有区域推专业 |
| 已有成果 → disabled | 保留Identity/Potential/投资/自身模板，撤销旧owner派生资格和效果；停止周期运行 | 保留Lv1效果、清空永久成果，或持续更新disabled的ACTIVE/网络 |
| 休眠成果 → enabled | 核实同城，恢复已有成果，按当前总督与真实网络计算 | 当新城重置Potential，或沿用旧network/ACTIVE |
| enabled → enabled | 保留成果并转移当前owner关联，重建派生状态 | 沿用旧owner全国接收模板/网络强度/折扣 |

同城识别失败应标技术UNKNOWN并保留原数据，不冒充完成了转移。实际撤销已附着Modifier和写入Owner关联的顺序/恢复需要单独验证。禁用时效果停止必须落实，不能只停止未来更新而留下已附着效果。

## D0006 Military IV补同步（Future，仍不实现）

| Rule | HOW与仍存边界 |
|---|---|
| MIL-003/009 | 后方训练与战斗经验分离。按单位身份维护同一合格训练位置的连续驻扎记录；中途移动即失效，不能只比较两次结算坐标；每次结算凭据去重。实际移动/回合时点接口未研究，不承诺加载后能重建缺失中途历史。训练量和完整周期以Spec为准，不再整体列TBD。 |
| MIL-010 | 独立Mentorship结算，战斗局部取相邻合格己方单位的最高实际Promotion count；不维护全国导师关系，不按经验推算，不把E用于限制。与正常Combat XP和Insight分别记一次性结算凭据；位置/Promotion快照遵循MIL-013待明示口径。 |
| MIL-011 | normal Combat XP、Insight和Mentorship独立组成奖励，正常cap只约束normal部分；不复制公式成为另一权威数值表。 |
| MIL-012 | 只做战斗局部候选检索；先判玩家enabled和单位体系资格，不扫描全国单位两两关系。Military Academy无额外奖励，不改HD建筑平衡。 |
| MIL-008/013 / OPEN-10 | 保留体系取得/持续资格、精确单位/战斗分类和快照边界；移除训练频率/公式/额外硬上限整体未定的旧假设。Harbor镜像未定细节不自动补全。 |

Military仍OUT_OF_V0.1，本轮无XP代码、API研究或性能测试。其玩家资格也受ELIG统一约束。

## 已发现的实现差距（不是本轮悄悄修复）

1. 运行Probe.lua:23的IsTestPlayer同时匹配固定文明及领袖；Gameplay.lua、CityJournalProbe及其它探针调用它。它是B015测试作用域，不是D0007通用资格实现，不能直接将其改名后宣称适配完成。未在所查门控中发现IsHuman限制；这不等于AI兼容验证。
2. 初始化有pairs(Players)后按测试身份过滤、周期探针只刷新匹配对象。仍需未来替换为资格入口并审查访问成本；本轮不benchmark或声称已满足全系统参与者成本。
3. CitySpecializationState.identity要求isTestCivilization，旧档nil返回DESIGN_DECISION_REQUIRED；按D0007正式接入前须改为资格/兼容状态。TransferOwnership的preservationID绕过测试身份仅是D0005离线保留实验，不是eligibility证明，不可用于启动未启用者效果。
4. CityCompletionJournal仅有Foundation，没有“有证据从未启用的征服城市”接入，也没有完整休眠/恢复/效果撤销路径；B015扫描“无已完成专业区域”的条件只适用其新城实验，不得套到ELIG-005取得的未专业化城。
5. 当前网络离线模型假定调用者提供同一owner的合格来源/中心，并未统一应用enabled集合；读到休眠Identity也不能把它算成有效source。

以上列为IMPLEMENTATION_LIMITATION / IMPLEMENTATION_PENDING，不是已经证实原设计不可实现。保留B015及原测试以便证据连续，本轮不改Source/Tests；旧测试输出不代表D0007资格验收。

## 后续最小验证规划（未派发）

先独立准备资格入口与持久事实/运行许可分离，然后本地验证：enabled人类与AI同规则；disabled新城不创建表/不进入更新；四种征服情形；未知资格不删除事实；禁用撤销全部旧效果；多enabled玩家来源隔离。真实carrier和同城识别具备候选后再给最少实机步骤。当前没有新测试包，不要求用户测试。

## 审计

修改前文档及protected_hashes.json位于DevelopmentBackups/Specialization-before-D0007-document-sync；涵盖全部Design、当前运行包、DevelopmentTests。最终核对hash不变，UUID、Civ6配置不改，未启动游戏。当前正文改过期假设，旧报告/历史段落冻结保留；Status为唯一当前队列。
