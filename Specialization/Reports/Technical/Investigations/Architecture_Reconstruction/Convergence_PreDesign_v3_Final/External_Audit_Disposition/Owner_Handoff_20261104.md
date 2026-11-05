# Codex Handoff — Claude Code v3-final 外审接收、问题处置与实施前计划修订

> **本任务是调查、审阅和计划修订；不是实施授权。** 你目前尚未阅读本轮 Claude Code 外部审计，**第一步必须完整阅读审计正文及证据附件**，不得根据本 handoff 的摘要假定审计内容或直接开工。
>
> 目标：在任何 Pre-U5、U5、Option B、正式规范同步或部署开始之前，全面处置审计发现，纠正候选计划，向 Owner 提交可复审的计划及决定状态。不得把尚未验证的技术猜测自动当成新的玩法规则。

## 0. 输入、权限与第一步阅读（强制顺序）

1. **先完整阅读（不是只看摘要）**：
   - `Independent_Audit_v3_Final.md`（Claude Code 的独立外审主报告；含 A01–A20、OD-1～OD-4、审计建议的分组与证据限制）。
   - `Independent_Audit_v3_Final_Evidence.md`（外审证据、九组审查、源码引用与已验证/未验证界线）。
   两份原件应通过仓库实际路径、Owner 提供附件或当前工作区定位读取；不能找到时说明缺失并停止依赖这些材料的结论，不能自行重建一份“Claude 审计”。
2. 阅读仓库当前 `Convergence_PreDesign_v3_Final/` 的完整候选材料，及其引用的 v3 事实／订阅契约、决定闭环表、Gap、Pre-U5、O1–O8、FS 正式同步差异、外审包和冻结正式 Design/Architecture/Workflow/Status。核对实际 HEAD、分支、正式版本、所读材料版本，列出差异。新报告和旧报告只是调查材料，不能替代正式规范。
3. 阅读本 handoff 的 Owner 决定。**Owner 决定高于 Codex 或 Claude 的建议**；有冲突需要明确列出，不能默默解释成已批准方案。
4. 对 A01–A20 和附属发现追溯源码、已有测试与正式规则；根据证据逐项处置。外审中静态确认不代表运行实证，审计建议不等于 Owner 批准。

## 1. Owner 已确认的四项新决定（OD-1～OD-4）

### OD-1 — 正常冷读档是状态恢复，不是新的业务变化；先调查，不选外审部分重算方案

- 对**同一受支持构建、合法存档**，冷读档应恢复保存时等价的游戏事实、Mod 永久历史及原生 Carrier/隐藏建筑效果。Lua 层重启、缓存消失、订阅/来源索引重新建立，**不构成商路/身份/资格/收益真实变化**。
- 不能把“来源 A 已确认退出、B 未就绪”直接作为正常加载时应即时降低收益的前提：必须先追问 **A 何时、依据什么确认退出**。保存前已退出则保存的效果理应已反映；仅因 Lua 未初始化完成而读不到，不是已确认退出；若读取后与保存时真实事实不符，调查加载顺序、原生恢复、Mod 写入与存档问题，不发明正常降级玩法。
- 在相关 Lua 事实/历史/拓扑尚未完成可靠重建时，**不得凭不完整输入撤除、部分重算或覆盖已恢复的 Carrier**；恢复后用可靠、完整事实核对，预期幂等无变化。真实加载后的新事件与明确可靠负事实仍须正常处理，不能以初始化为由无限拖延。
- 此原则**不假定已实证**所有原生 Carrier 在 Civ VI 的保存与读档中的恢复时点。调查：①原生隐藏建筑/效果/引用恢复；②哪些 Lua 事实不持久化、如何从原生＋Store 重建；③可靠初始化完成边界与阶段顺序；④ Commerce/CultureNetwork/Standardization 是否在未就绪时提前清除/写入；⑤是否有真实、不可避免且无法用正确时序解决的例外。证据不足时将 OD-1 标为 `ENGINEERING_EVIDENCE_OPEN`，不得替 Owner 选 Claude 的局部收益(a)或旧全额保持(b)作为新业务政策。
- 如果实机/源码证据最终证明同版本合法冷读档不可避免地产生需要业务取舍的状态，再提交最小 `Owner Decision Packet`；不能以现有代码的冷读档写入行为反向定义玩法。

### OD-2 — 已确认的合法商业身份退出，按正式玩法执行信誉重置

- 当真正的资产重组/身份转换确认城市**合法退出 Commerce**，其 Reputation 按既定设计重置为 0，即使旧信誉叶子暂时不可读；这是合法业务历史转换，**不是**“UNKNOWN 即猜零/重置损坏历史”。
- 前提必须严格：城市身份、parent/envelope、reference、事务授权与受控提交可信。若这些基础不可靠，不能盲写；明确错误并调查根因。只修改该合法转换要求的字段，不波及未损坏的兄弟记录。
- 未知信誉记录属于本 Mod 权威历史严重异常。重置成功不能宣告根因已修，诊断证据应保留；明确旧版本的异常 leaf + Identity exit 漏重置路径与最小局部验证。

### OD-3 — 有条件允许本地回合开始补完**已登记**责任，不批准通用重试

- 首选真实原生完成/可用性/初始化边界。仅当证实特定事实存在合法短暂未就绪窗口且缺更直接的完成通知时，允许在**本地回合开始**处理已登记、有界的 pending 范围；必须记录原因→触发边界→次数/范围→完成/错误处置。
- 不因此全城扫描、不无界轮询、不静默每回合错误重试、不将 Mod 自有历史 UNKNOWN 当作“等一回合会好”。异常必须显式报错并修根因。
- 删除旧 turn audits、Bridge Refresh 或 D1 前，逐项证明必要工作有可靠替代、已接管责任不会丢、同值恢复/次回变化/失败发射仍可完成。

### OD-4 — 不支持跨版本旧存档，保持**同版本**冷读档正确性

- 继续执行已批准的 Playtest_Workflow 范围：只支持**由当前 Mod 构建开启**的游戏及其同版本存档。持久化形状不兼容变更时使用新游戏，不新增跨构建旧存档迁移、旧版向前/向后兼容代码和无限期 LEGACY 门禁。
- 删除因假定旧版兼容才保留的规划义务、无终点的兼容门槛；调查未接生产的 NetworkRecoveryModel/Cell/Store、Stamp、配套测试是否可在**正式职责与依赖**退出后安全清理。
- **代码/部署回滚**仍须精确文件清单、哈希、备份、失败恢复，不代表旧/新版本存档交叉兼容。生产需要的 SQL ID、已安装当次构建实际 Carrier、启动/清理职责不能因“不兼容旧档”而无证删除。

## 2. 此前已确认目标，不因外审重新投票

- **ODP-01=B**：D-2 只保留有界会话级按来源极端保护；正常网络与正常冷加载以可靠引擎事实和正式历史重建，不默认持久化旧派生归因。若读取异常，显式错误、合法来源引用边界、真负事实优先；不得把未知当 0、空网或已退出。OD-1 对正常冷加载写入时机的约束优先澄清，避免误把“未初始化完成”当作异常来源业务变化。
- **ODP-02=A**：Reputation 是本 Mod 的权威历史，正常 UNKNOWN 不合法。仅在信誉叶子独立异常、parent/身份/配置/引用及其他交易依赖可靠时，可显式严重报错、保留原历史，以**暂时 R=0** 一致供信誉相关被动计算和新的 VENTURE 条款；新合同按当次条款锁定，旧合同绝不追改；STABLE 无真实 R 依赖则不人为增加门槛。例外不能扩到未知余额、未决 native 结果或别的历史；不得把 `or 0` 伪装成来源证明。
- **UNKNOWN 根因优先**：正常 Mod 自有历史/ACTIVE/正常可靠拓扑不接受 UNKNOWN 作为稳定业务状态；极端保留/降级不是问题关闭证据。
- **Option B 全面还债**：U5 前仅必要修复以保留迁移前行为基线，但 Option B 必须完成底层职责、依赖、网络发布、历史边界、UI、旧模块与必要工作量收敛；不能以“今天能玩”永久延后。
- **生产/诊断/实验隔离**：Probe/Collector/trace 应是可选观察者；正式事实、write barrier、Flight/GC、历史、事件交付和清理必须由生产 owner 负责；迁职责后做关闭与真实缺文件/缺 global 差分。
- **统一 ACTIVE**：专业不缓存各自 Governor Ceiling；未来管理容量只是接口预留，不在本次开发；合法资产重组开启新进度 episode 的 Potential −1 不能误判为普通非法下降。
- **D-1 暂不立即删除**，但目标架构正常网络事实准备完毕才向专业发布可消费更新；Option B 需对旧 D1/中央 hold 分支逐条说明去向、可靠根因和可验证退出，不能改名保留后虚称清偿。
- 既定 DEC-01～14、R1～R6 与原四专业公式、巨构工程学无奇观历史、工程研习 E 严格完整、Claim 真原生提前完成、Crew 唯一真实发放证明均不因 Claude 提议自动变化。

## 3. 外审 A01–A20：逐条登记，不得漏项或机械全盘采纳

建立 `Audit Finding Disposition`，**每项**至少：Finding ID；审计主张与依据；Codex 复核源码/正式条款；`ACCEPT` / `REBUT_WITH_EVIDENCE` / `OWNER_DECISION` / `EVIDENCE_PENDING`；问题严重度/真实可达性/验证层级；影响 G/PU/O/FS；具体修改计划；最小 LOCAL/必要原生证据；复审范围；关闭状态。

重点覆盖但不限于：

- **A01/A04**：冷加载正常不完整输入与当前 T0 三网络消费者真实行为不一致。**以 OD-1 为契约**重建时序/原生恢复模型，而非直接采用“低收益部分重算”的审计推荐；Cold Carrier 真实恢复尚需验证。
- **A02**：按每个合法未就绪原因提供完成事件/边界/有界责任，OD-3 有条件回合待办；Bridge `failedTurn`、同值恢复、ACTIVE/D 恢复与发行失败唤醒。
- **A03**：列清每个 D1 旧分支与共享层 hold 的精确职责：删除、转为正常事实待完成责任或确有合法用途的保留；指定 O3 owner 和退出证据，避免“如有可撤者”成为空验收；不机械要求不存在“无新写入、原有 Carrier 保持”的正常加载行为。
- **A05/A12**：未知角色来源不能被静默过滤成全 READY；effect availability/partial 真实性；写入失败不得自动全清；商业按 domain、标准化按 target/self 的独立资格；保留 `max` 与既定 Floor。
- **A06/A08**：应用 OD-4；移除不必要跨版本兼容承诺；正式 FS 相关位置（含 NET-005/Content/Status/S9）全面列举并同步提案，不提前实际改正式权威。
- **A07/A11**：OD-2 合法退出信誉重置；ODP-02=A 的 R0 来源标记、leaf/parent 错误分类、合同 quote/confirm/locked terms、STABLE 独立、CREDIT_INTENT/CREDIT_CALLING 严格门槛；PU06 做成 O4 的首片避免二次实现。
- **A09/A10**：R2/ACK 真实接管、FAILED/SKIPPED/false/flush 丢事件、owner pending 粒度、GreatWorkFacts 既有先例；R3 保留 unique governor/native listeners、phase0 时序，并把 fail-closed mandatory exit gates 与普通可撤订阅区分。
- **A13/A14**：PU 为对应 O 包可延续的第一片；原生验证集中在少量有确定问题的触点，不叠加每包全套实机。
- **A15/A16/A17**：施工队 Crew 多城市同类完成的唯一证据和每 completion receipt、异常影响范围；Claim/Dialogue UNKNOWN marker 不致误取消；Claim early 完成真实性；首次完成错误是否毒化所有未指派城市、退出/夺回与多 owner gate 范围。
- **A18/A19**：补全实际 DEV/Probe→生产依赖图（CityFlow/FreshBindingHook/BindingProbe/UnitSiteProbe/PerformanceCounters/trace、错误分类、PurchaseProbe/BoostRefresh、GC/Flight）；真实 absence harness；原 GC 策略保持；SQL Probe 名称不等于可删。
- **A20**：永久损坏能力明确受影响范围内阻止并报错，不以静默 HELD 或猜恢复；实际中等规模运行观察、双部署移除凭据、上限与版本字段等按证据处理。

外审有些项目是计划改进，有些是**当前代码的已证缺陷**，还有些仅为 UNVERIFIED 原生问题；不得把全部20项标成“已验证运行时 Bug”，也不能以未复现实机为由忽略静态可达的正确性缺口。

## 4. 要求修订的输出

在 `Convergence_PreDesign_v3_Final/` 的后继调查资料中（实际路径依仓库现行组织确定），提供：

1. **Audit Finding Disposition**：A01–A20 全部逐项处置，连同附属债务清单与证据限制；有高危新问题需增补且报告 Owner。
2. **Revised Executive/Decision Closure**：OD-1～4 和此前 ODP-01/02、DEC/R 的权限及状态；OD-1 标明必要原生/加载证据，别冒称已经证实所有 Carrier 恢复。
3. **Revised NET / Cold Load Contract**：清楚区分保存业务状态、引擎恢复、Lua 初始化、首次可消费事实、真正的新负事实与错误；按 Commerce/CultureNetwork/Standardization 列出现状/T0、目标、禁止的提前写入、原生时间边界、需要证明的实例。
4. **D-1 Branch Disposition**：逐分支定位、旧责任、新 owner、移除/保留理由与明确退出 gate；纠正不能执行的虚假三臂 disable 测试，改为可执行的现状对照和目标差分。
5. **Completion/Wake Responsibility Matrix**：每个事实 pending 原因→确切完成事件/边界→责任 owner→失败可见性→有界次数/范围→对旧 turn audit/refresh 的替代关系；不能无限重试。
6. **P3 Production Dependency Inventory**：所有诊断/DEV/Probe 的必要生产职责与提取 owner；真实移除对照、测试夹具设计及 GC/Flight 不变量。
7. **Updated PU and O1–O8 Plan**：Pre-U5 与完整债务的精确范围、入口/出口、依赖、唯一真实原生需要、与不支持跨版本存档的部署边界；每 PU 尽量成为对应 O 包首片，不安排重复实现。
8. **Formal Authority Sync Delta（提案）**：穷举受影响的受保护正式位置与必要 successor 语义，不编辑当前已冻结正式文本；同步哪些旧任务撤销／改排期要清楚，避免先执行已撤销的 S9 冷归因接线。
9. **Claude targeted re-audit package**：向独立审计提供完整 Owner 原始决定（包括本 handoff）、审计原文和修订版，明确需要复核的 NET 矩阵/D1 表/P3 依赖、必要附属项。审计不能仅从 Codex 的二手总结推断 Owner 意图。
10. **Owner Gate / Remaining Decisions**：若源码实证表明仍需改变玩法语义、权威、持久化或不可逆事务政策，立即提交简明决定包，暂停依赖该决定的部分；**不可为凑“final”擅自选择**。

给每项交付写出明确已证、待本地试验、待原生验证、待 Owner 批准的状态。可保留 `v3-final-candidate`／`v3.1-review` 类名称，**不因生成文件而宣布最终审计闭环**。

## 5. 严格停止与授权边界

**本轮只读调查、报告/计划材料整理与证据对照。** 除明确获准的调查报告外，禁止修改生产 Lua、SQL、ModInfo、工具、测试、已冻结 Design/Architecture、Status/Authority/Context Lock、部署包或游戏存档；不得启动新探针、原生实验、U5、Option B、GC 策略改变、main 晋升或自动提交。需要验证应提出最小范围及申请授权，不能把验证计划写成已 PASS。

最终路径：**Codex 完整阅读外审 → 独立复核并逐项处置 → 更新实施前候选计划 → Owner 检查未决问题并认可送审 → Claude Code 对重大修订做定域复审 → 逐项闭环审计 Finding → Owner 再次明确授权实施 → 才开始获批的正式同步、Pre-U5、U5 和 Option B。**

**交付给 Owner 时先写一页执行摘要**：已关闭哪几项审计意见、哪些仍待证据、哪些真正要 Owner 决定、哪些模块/测试/正式条款需要改、以及为什么当前仍未开始实施。
