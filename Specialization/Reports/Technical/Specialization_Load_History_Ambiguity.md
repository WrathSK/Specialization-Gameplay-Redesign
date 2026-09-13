# 跨加载历史恢复：丢写反例

Document Owner: Codex
Architecture Revision: A0047
Runtime: B020/modinfo27（未改）
Verification: LOCAL_SIMULATION_PASS（反例复现，不是恢复通过）

新增test_load_history_ambiguity.py，执行实际B013/B015/B020代码。新城记录正常形成后，对一次学院完成通知模拟所有City Property setter不落值：B015成果写入和GAP标记均丢失，B020暂停；两份持久记录与完成前完全相同。随后模拟该区域被移除，当前区域枚举也不再透露它曾经完成。重建Lua脚本状态/加载后，实例内halt消失，B015旧表仍TRACKING/NONE，B020表仍DONE/NONE。

再交付剧院完成：旧B015可能选择CULTURE；B020因LOAD_READ_ONLY不写，避免在缺失历史时猜测。反例、实际B020回归及B015回归三脚本exit0。此脚本仅模拟失效与对象移除，不证明Cheat/正常游戏会发生这种异常；不是USER_GAME_TEST_FAIL，也不撤销用户B020四图通过。

## 推论与边界

DONE证明某次写入后的表一致，不证明之后不存在保存失败或未交付事件；B015 TRACKING、两表相等或当前无已完成区域都不足以消除反例。若所有可用持久信息丢失，不存在仅靠同一旧快照就能区分两种历史的可靠算法。增加第三张同样可能丢写的表不自动解决；正常保存测试不证明耐久性。

当前不改变设计，不开启自动补写，不迁移B020旧表，不修复冻结结果。运行只读限制保持。B015仍为独立DEV探针，不作为正式恢复权威。跨加载未专业化城市自动恢复写入列为BLOCKED（缺少可区分历史的可靠证据），不是整个v0.1被阻塞。

下一步应区分正常受支持保存/事件路径与异常持久化失败路径：先明确所需持久观察凭据及可保证的错误处理，再准备恢复代码。异常记录是否允许用户显式放弃/重置会影响设计，若要采用必须DESIGN_DECISION_REQUIRED；本轮未选择该方案，因此不要求用户决策。不要通过一遍无错误游戏测试声称所有丢写已解决，也不要求用户人为破坏存档。

执行输出与保护hash：DevelopmentBackups/Specialization-before-D0008-load-review。本轮Source/Design未改，无新增用户测试。
