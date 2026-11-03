# Claude Code 独立外部审计包（短交接）

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


## 角色、阶段、先不要执行

你是独立只读Reviewer，不是设计权威或实现者。**本包只准备材料，尚未启动外部审计。** 当前两项重大决定未闭环；Owner处理ODP01/02并认可最终候选后才进入正式独立审计。可反驳Codex结论，不能被计划中的建议约束。

审批链：v3候选→Owner决定/最终计划→Claude独立只读审计→Finding逐条处理/重大问题实施前重审→Owner再次放行并明确实施授权。审计PASS、Git发布、既有S2–S10历史授权都不是自动实施许可。禁止代码/测试/正式规范/配置/部署包/Status写入、游戏/探针/迁移/main操作。

## 最小阅读路线

1. [Owner门禁与两项决定包](Owner_Gate_Stop_Report.md)，先确认是否已有后继closed版本。
2. [七责任图](Executive_Architecture_Map.md)、[Decision Closure](Decision_Closure_Register.md)。
3. [Fact/Subscription](Fact_Subscription_Contract.md)、[O1–O8最终候选](Option_B_Final_Candidate_Plan.md)、[PU01–11](Pre_U5_Final_Candidate.md)。
4. [Formal Sync Delta](Formal_Authority_Sync_Delta.md) 与当前D0058/A0183/SAFE004核对，不能以报告替代正式权威。
5. [Gap/S01–S16源码定位](Gap_Matrix_v3.md)，按疑点跟实际calls/Start/SQL/native写与既有测试，不必全量通读历史。
6. 冻结v1/v2只作沿革；未读独立Carrier/ModifierFootprint专项，本审计不依赖它。

基线应重新核对：develop `9addf8d01dcbcb46d28e59ffa5625950f4540e57` 为本候选源码；新报告发布不改运行代码。正式D0058/A0183/S0866，记录B399.426，非本轮重新验包。不要把版本/数据数量当永恒事实。

## 请优先反证的假设

- 正常事实层能可靠完成与发布，而不是把UNKNOWN正常化或仅把hold搬中央；确认负事实不会等待unknownsibling。ACTIVE保持统一，Potential非法下降不是正常fallback。
- ACK确实在专业登记责任后，旧ACK不吞新变化，central不回放业务；四专业自声明不破坏phase0、failedStart隔离或独特native完成。
- 获批纯被动last-confirmed不跨ref/lifecycle，不混不同GW版本；其它F行没有被批量默认授权；永久Dialogue和Insights、E/L与native receipts严格区分。
- D1退役不是删if：normal/cold/signal/丢ACK/secondchange/negative与真实禁用/删除差分均有可执行证明；Standardization self不长期被无关net卡住，仍max，不两个全额相加。
- **ODP01**最终D2分支能保留必要连续性/确认退出，或明确批准其行为变化；旧派生归因不是新永久历史，不能未经批准接线/删除。
- **ODP02**信誉root严重错误与统一R0极端例外范围已明确；不抹原record/旧terms，不把STABLE数学无依赖变成实现资格；其它strict未知不被例外扩张。
- 当前旧Probe/trace仍可能生产必需：Bridge direct include/New、Pwritebarrier、Flight/GC不能直接删。测试必须absent file/global，不只ENABLED=false；GC策略不随清理改变。
- Crewuniqueproof真的足够；playercountdiff/lastreceipt/位置不能替代uniquecompletion。Claimtrueearly合法，Narrative取消参数不冒充Gameplaysignature。
- 首次completion/lateexit root没有被新恢复掩盖；foreignloss.target返回后不再合法，不能盲replay。
- 双部署精确删除/receipt/failpoint/rollback、SQL/saveID、restrictedLua及真实producer/consumer测试覆盖实际迁移；旧scopedPASS不自动覆盖新路径。

## 输出与证据要求

区分`STATIC`、`LOCAL`、`USER_NATIVE`、`UNVERIFIED`；引用baseline、实际函数/行/分支、对应正式条款与新Owner目标。不要仅按文件名/计数判缺陷，不要求为形式统一中央Push或大型插件框架。

每Finding给：严重度／可达场景／当前formal+目标／源码反证／影响包／最小验证／建议／是否Owner决定。可以说“计划尚不足以实施”，不必给整体高分或采纳Codex分类。未执行不声称PASS，不读raw私人日志/存档作为默认上下文。

## 实施前处置门禁

Primary维护 **Audit Finding Disposition**：ID／接受、证据反驳或Owner决定／具体证据／修改契约和包／验证或重审要求／关闭状态。重大问题不能以“实施后看”关闭；需修计划并在实施前重审。Owner认可闭环版后另行明确授权实施。当前此表尚无审计发现，不伪造一份“全部通过”。

本包测试计划尚未执行。已知工程缺口/Owner问题不得被“审计材料齐备”掩盖；本轮终点是候选与决定准备，不是代码或游戏操作。
