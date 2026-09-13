<!-- Frozen handoff snapshot. Historical assertions only; current README/Status supersede. Relative links rebased; exact original bytes in DevelopmentBackups/Specialization-before-fresh-agent-handoff. -->
# Specialization协作约定

Document Owner: Codex
Design Authority: User
Governance Revision: G0006

1. Codex是项目唯一日常本地文件写入者，包括Design Spec、Design ChangeLog、Architecture、Status、Reports、Source、Tests及README/AGENTS。外部Design Chat仅提供proposal/review，没有本地文件写权限；用户转交其建议不等于接受设计。
2. 用户是最终Design Authority。Codex可讨论、整理、提出风险/方案，并按用户确认落盘；只有用户明确接受才能将Design标为ACCEPTED，不得自行升级proposal或draft。
3. 文件语义分离：Design Spec=WHAT；Architecture=HOW；Status=实际实现/验证。游戏意图权威顺序为Accepted Design Spec > Architecture > Status > Historical；写入规则不意味着implemented或任何STATIC/LOCAL/USER_GAME_TEST_PASS。
4. 实现较容易、API限制、Codex偏好或测试失败都不能静默改Design。遇到问题登记DESIGN_DECISION_REQUIRED或IMPLEMENTATION_LIMITATION，必要时DESIGN_CONFLICT，交用户决定。
5. 当前Accepted Spec为D0014，正式校验值见Design ChangeLog；Accepted Spec是游戏设计意图权威。Architecture A0110已同步D0014；D0010征服分流完成本地契约，原生Claim/转移尚待接入（运行B027限定DEV direct接收两图按范围通过，Commerce IV待研究；旧B026 PASS仅限D0008）并记录技术限制，通用资格/休眠模型已本地通过，B016只读资格两案按两图范围通过，B017明细单案已通过，54–61已确认在本局当前存活名单外，B018组合只读诊断两案按两图通过，正式适配尚未部署，PROG-005已确认通知顺序，B015实际DEV新城提交实验已接入，新城/学院/重载三图已按观察范围通过；正式提交器仍未启用，Future经验API尚未验证，Spec继续作为WHAT权威；用户已授权恢复离线多源计算和城市专业状态，B011只读事件探针的用户两案结果已按观察范围登记，用户已授权B012独立DEV表探针，两案实机结果已按观察范围登记；用户已授权继续准备B013，DEV新城双侧绑定两案现已按观察范围实机通过；用户授权继续后的B014已接入DEV完成观察持久化，两案已按三图观察范围实机通过；正式机制未启用。本次接受不自动落实TBD、PROVISIONAL或候选数值。
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

## 截图归档（G0004，用户明确批准）

用户只向Specialization/ScreenShots投递，保持默认文件名。Codex逐张读取并登记结果后，将该批原图移动到Status/Validation/Evidence/<Batch>/，核对移动前后SHA256，写manifest与结果关联，不留重复副本；收件箱目录本身不移动。仅归档已读且批次明确的文件，目标同名冲突不覆盖。归档后原件冻结，不擅自删除或压缩；未读/不明文件留在收件箱。本轮B012五图全部归档，之后同样按批次办理；无需逐次申请。规则取代先前“归档仅建议”的状态，其它工程路径约束不变。

## G0005：Cheat机制测试优先（用户明确）

当前目标为可通过Cheat Panel验证机制的开发版。正常操作/保存读档及真实收益优先；保留身份冲突停止、重复不发放、不覆盖旧成果、不凭空补历史等必要保护。极端丢写/多故障组合记录支持边界，不要求每项机制前先彻底解决；不得把正常路径PASS扩大到这些边界。自然生产与Cheat、同回合与跨回合证据分别登记。用户此项调整不授权改变Design玩法或静默fallback。

## G0006：后台商路数据来源（用户澄清）

不要求玩家先打开贸易UI；允许后台直接读取BTS/原版UI可用的当前路线数据。认可此来源，后台桥接与网络重建可继续，不再以“必须纯Gameplay全集”或“UI来源待授权”阻塞。准确区分上游来源与本Mod桥接可靠性，验证自身初始化/重载/撤销链路，不伪造实机PASS。无需更改网络玩法；仅在确实不可行时再讨论替代。详见Reports/Technical/Specialization_Network_Background_Source_Decision.md。
