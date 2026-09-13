# Specialization协作约定

Document Owner: Codex
Design Authority: User
Governance Revision: G0003

1. Codex是项目唯一日常本地文件写入者，包括Design Spec、Design ChangeLog、Architecture、Status、Reports、Source、Tests及README/AGENTS。外部Design Chat仅提供proposal/review，没有本地文件写权限；用户转交其建议不等于接受设计。
2. 用户是最终Design Authority。Codex可讨论、整理、提出风险/方案，并按用户确认落盘；只有用户明确接受才能将Design标为ACCEPTED，不得自行升级proposal或draft。
3. 文件语义分离：Design Spec=WHAT；Architecture=HOW；Status=实际实现/验证。游戏意图权威顺序为Accepted Design Spec > Architecture > Status > Historical；写入规则不意味着implemented或任何STATIC/LOCAL/USER_GAME_TEST_PASS。
4. 实现较容易、API限制、Codex偏好或测试失败都不能静默改Design。遇到问题登记DESIGN_DECISION_REQUIRED或IMPLEMENTATION_LIMITATION，必要时DESIGN_CONFLICT，交用户决定。
5. 当前Accepted Spec为D0002，正式校验值见Design ChangeLog；Accepted Spec是游戏设计意图权威。Architecture A0011已同步D0002并记录技术限制，Future经验API尚未验证，Spec继续作为WHAT权威；用户已授权恢复离线多源计算和城市专业状态，B011只读事件探针的用户两案结果已按观察范围登记，用户已授权B012独立DEV表探针，目前等待实机结果；正式机制未启用。本次接受不自动落实TBD、PROVISIONAL或候选数值。
6. Dxxxx/Axxxx仍分别表示Design/Architecture版本，均由Codex按用户授权维护；正式sync记录accepted Spec SHA256及Sync Status。已同步仅表示评估与架构反映，不升级验证状态。
7. Historical及既有Backups冻结，不就地修改；结果原件纠正写新记录，由Status引用。新的必要备份允许另建快照，不覆盖旧备份。README/本AGENTS/路径规则变更须用户确认。
8. 工程路径约束不变：不移动运行源码、Tests、Backups、ScreenshotInbox；不建第二份Source/Runtime；不改UUID或游戏配置；不启动或操作Civ6。游戏内验证全部由用户执行，B010未测且暂停。
9. Status是唯一当前验证/任务入口。旧Batch不自行重发，PASS必须有用户证据；外部AI建议不得冒充用户结果。
10. 一个活动Codex写入任务；任务开始读取README、本约定及当前Design/Architecture/Status。源码在本目录之外，从外层执行时也须显式读取本约定。不要依赖Work with自动文件映射。

## 用户交付规则（G0003，用户明确要求）

用户不是Lua/Civ VI Mod实现人员。每次交付先提供独立中文“用户摘要”，用户不需要阅读Architecture、日志或源码才能理解结论。按顺序说明：

1. 这轮做了什么。
2. 发现/结果是什么。
3. 对实际游戏机制意味着什么。
4. 是否存在阻塞，以及为什么。
5. 用户现在需要做什么：设计决定标DESIGN_DECISION_REQUIRED；实机验证只列最少步骤；无需操作时明确写“用户现在无需操作”。
6. Codex建议的下一步。

先解释普通概念，再给必要术语；不单独堆砌provider、adapter、dirty、atomic replace、derived cache、lifecycle等。技术细节、文件列表、API/函数、测试输出、日志均放摘要之后。

验证状态在每份交付中第一次出现时解释证据等级：
- STATIC_CONFIRMED：代码/数据库静态证据，不等于游戏运行通过。
- LOCAL_SIMULATION_PASS：本地模拟通过，不等于Civ VI实机通过。
- USER_GAME_TEST_REQUIRED：需要用户在游戏中验证。
- USER_GAME_TEST_PASS：用户已在实际游戏中验证通过。
- USER_GAME_TEST_FAIL：用户实际游戏测试在已记录场景未达到判据，不能扩大到其它未测场景。
- BLOCKED：当前无法继续，需要技术突破或设计决定。

技术限制若导致必须改变Design Spec，不直接选择替代方案。先用普通中文说明原设计为何无法实现（不确定则明确证据边界）、替代方案会怎样改变玩法，再标DESIGN_DECISION_REQUIRED并交用户决定。

每轮最终交付结尾固定分开写：
- **用户需要决定：** 无则明确“无”。
- **用户需要测试：** 无则明确“无”。
- **Codex下一步：** 明确下一项或等待事项，不未经授权继续扩大工作。
