# D0014 / B051.67：科研IV所有非学院区域

Document Owner: Codex
Build: P0-B-051 / modinfo67
Design: D0014 ACCEPTED

## 当前规则与实现

按用户明确说明同步RES-004：不区分专业类型，不要求消耗人口名额，本城所有已完成非Campus区域的Actual复制基数各类产出合计50%转Science。军营/圣地/政府区/社区/娱乐及新Mod类型均按相同规则；市中心作为区域也在枚举内，不静默另设白名单。未完成区域继续不计；Campus仍只作为科研身份锚点，不加入复制基数。无产出区域贡献0，不导致其它区域收益被清零。

后台UI采样、Gameplay完整集合核对、只读报告同时取消P.Families/RequiresPopulation限制。保留六种原生yield的district:GetYield，接纳行业等确实进入该getter的产出；不读整城总量、住房、宜居度，不套用Base adjacency。新增类型不建立对应专业化机制，也不推进Future scope。

工业网络max、50%、ACTIVE要求、整数/半点组合、SQL载体、准备/确认与施工队完全不改。更细于半点的目标值仍是技术限制，不擅自取整。原始报告的COPY_DISTRICT_SCOPE_UNRESOLVED检查已从正式计算移除。

## 证据等级

[用户结果](../../Status/Validation/Results/Specialization_B051_66_User_Result.md)：工业4.5、科研区域50%与半点USER_GAME_TEST_PASS限用户回报场景。新范围不可沿用为已通过。

STATIC_CONFIRMED为代码静态证据，不是游戏通过：三处范围一致，无RequiresPopulation筛选。LOCAL_SIMULATION_PASS为真实Lua/mock，不是Civ VI实机：test_b051_all_districts.py覆盖军营、圣地、政府区、社区、娱乐、市中心的跨产出、无产出、无人口名额区域；未完成/Campus排除；新增/移除/ACTIVE撤销/半点、报告与正式合计一致，原事件驱动回归通过。SQL未改，全Lua/XML/manifest检查通过。

## 最小补测

只用截图中的旧科研IV城市，重新加载并确认报告B051.67。Read Lv4 copy应列出全部非学院区域，预期=合计50%、已配置相等，不再有范围错误；真实科技应恢复增加。按现有规则吃宜居度等百分比，截图本城−2宜居度，不能直接将原始3/4点与最终总量增量等同。

顺手用一个已有社区/娱乐或其它非人口名额区域：没有产出时不能阻断复制；有区域实际产出时应计入。没有现成条件不用重开局，先回传原城报告，扩展类型中未实测部分另记。

关闭面板等片刻再读取一次，基数和固定复制额不得持续增长；这是扩展到市中心等新类型后的输入隔离观察，不能用mock断言原生getter一定不会含本项城市层加成。若增长，回传连续两图，停止扩展而不暗中排除类型或改公式。

用户无需重测工业4.5或原整批；未启动游戏。Spec D0013已冻结为Design/Revisions原件，D0014/hash在ChangeLog登记。

## 后续结果：最小补测已关闭

用户对上述最小补测口头确认PASS，未附图或数值；见[B051.67结果](../../Status/Validation/Results/Specialization_B051_67_User_Result.md)。上方步骤保留为案例记录，不再作为当前待执行任务。具体区域覆盖未列明，不将可选类型或全部生命周期组合自动登记通过；设计/源码/版本不变。
