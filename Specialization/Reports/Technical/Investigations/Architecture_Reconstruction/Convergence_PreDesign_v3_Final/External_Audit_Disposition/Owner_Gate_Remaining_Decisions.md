# Owner Gate — 三阶段窄范围授权申请

Status: Stable candidate application, 2026-11-04. **Owner已明确批准本三阶段申请；Step1执行中，Step2／Step3须等待前置门禁完成。** Primary；develop954dc67aca007082a5a164becdbafbacbad1403a；D0058/A0183/S0866；记录中的运行包B399.426未改。

## 已确定的前提，不重复表决

Claude [C1–C5短复查](../../../../../Advisory/Architecture_Engineering_Audit/C1_C5_Short_Recheck.md)已将五项全部标记PLAN_CLOSED，Owner明确接受；无新增重大Pre阻碍。N1–N3已纳入[原Finding](Audit_Finding_Disposition.md)与[唯一统一计划](../Architecture_Convergence_Integrated_Roadmap_DRAFT.md#4-ordered-slices-gates-and-rollback-boundaries)，不新开批次：

- Tier只沿实际同一区域建筑升级链递增；已证实的非升级解锁门槛不加级，工业水磨坊为T1；真正缺失／不完整链仍报错，不能按“不在Tier表”直接跳过。
- HD旧Tier仅作迁移对照；数据中心、静修院、花园差异逐项解释，不以匹配旧值为规则；D公式及数值不改。
- O5完成环境/UI基底装配后固定一次无HD加载冒烟；O6负责具体UI行为／交互验收，可复用环境和证据。

## 本次请求：一次授权，按前置门禁依次执行三步

| 步骤 | 窄范围操作 | 完成条件，未满足不进入下一步 |
|---|---|---|
| **1．可靠发布／保全** | 对下列明确候选及Stable审计文件作归属、隐私／敏感信息、引用和差异审查；以普通新提交推送develop，不改历史、不force、不删原件。必要独有决定保留在当前处置／计划内；不是把所有历史加入默认上下文。 | 记录发布提交及各文件SHA256；**从远端独立重新取得已发布版本并逐文件核验**，而非仅本地git show或推送成功提示。所需决策、审计原件和引用可定位，无隐私/归属/材料缺口。若任何必要材料无法可靠发布／取回，暂停Step2，报告确切缺口；未经批准不改用虚称永久的本地副本。 |
| **2．首次正式规范同步＋最小工作流／现行信息收敛** | Step1完成后，按现有D/A接受流程同步既已接受内容及PU01前必须一致的现行副本，取消过时S9派生网络接线、旧cold-partial及跨构建兼容义务；记录Tier来源/N1–N3及正常恢复、交付、退出边界。**同时在PU01前完成下方A类最小集合**，复用现有Workflow、根／项目AGENTS、Status和技术导航；长期防御性工程原则只在Architecture留一个规范来源。 | 现行规则／状态、接受链、必要引用／哈希检查通过；A类门禁全部通过：角色／权威明确、原生证据按需路由、最少读取、常规结果有现行落点、负责人摘要／安全短交接可执行、长期工程原则已正式落地。已替代候选退出默认阅读而保留历史定位；不要求先清理历史文件，不批量解除原保护。冻结历史／审计不改，独立提交推送develop；**未完成不进入Step3**。 |
| **3．仅PU01首片** | Step2正式后继和当前授权已准确同步后，使用**现有HD提供者**实现Commerce／共享事实的状态分类与按用途投影；只提取该路径已证实必需的生产kernel／共享读取阶段／写屏障职责。沿用后续O1/O3的最终接口，不写临时hold框架。 | 真实producer→consumer组合，UNKNOWN不当0／可靠负事实／D和workers不可读／独立domain／同ref及同回合第二变／写后失效；严格交易证明及max/Floor公式保持；受限Lua／实际打包与受影响回归通过。按现有证据策略写简洁结果、独立提交并推送develop；LOCAL不写成USER_GAME_TEST_PASS。 |

Step1是Step2的硬前置；Step2是Step3的硬前置。批准本申请后可依次连续执行，无须每步再次例行询问；但没有该明确批准前，三步都不自动开始。遇到真实新语义、核心职责／持久化／不可逆权限扩张或无法安全解决的限制，只暂停受影响部分，说明原因，不以本申请扩大范围。

### Step2有限补充：本轮Owner要求的A类最小集合

本次是文档职责补齐，**不重新设计工作流或改变玩法**。对照现有条款后，只需在[现有FS提案的Step2补充](Formal_Authority_Sync_Delta.md#step-2-limited-workflowcurrent-information-supplement--proposal-only)应用精确的局部修改：

- **证据查找与最少读取：**原生事件、Modifier、冷读档、SQL/UI等问题先查项目已有相关证据和Engine_Reference对应问题小节，再按实际缺口查外部资料。新增原生验证请求必须说明尚未解决的具体问题、现有证据／本地验证为何不足及最小区分结果；保留已有固定验证门禁。Engine_Reference不强制全文读取，旧计划／审计也不默认全量加载。
- **权威与现行落点：**Design定义已接受玩法，Architecture定义相容的技术合同，Workflow定义工程操作；Status记录当前实现／证据／授权边界，Reference提供有范围的证据，均不据此重定义玩法。历史不能覆盖现行已接受规则。普通任务优先更新受影响现行规则和状态，保留足够的简洁验证结果；不默认新建永久过程报告，独有失败／原生证据和既有保全义务不削弱。
- **负责人摘要与短交接：**重要汇报先用中文说明当前阶段／目标、实际完成、实质问题及影响、下一步、是否需要决定或测试，再附技术编号。完整模块或迁移责任片段验收且现行信息同步后，在安全边界给出短交接再转新对话；不在未完成不可逆事务中强切，不强制每次新增交接文件。
- **长期防御性工程原则：**按已接受的统一计划§10.1写入现有Architecture运行合同；正常初始化／可用性恢复／读档对账与额外恢复机制区别清楚，不削弱UNKNOWN、不可逆凭据或已有安全保护。Workflow／AGENTS只引用，不建立第二套规范来源。

**Step2 A类验收：**新会话能按当前入口回答规则、实现状态、证据范围和可执行边界；能定位原生问题的相关证据小节；普通收尾与短交接有明确现有落点；负责人摘要要求已进长期规范；基于证据的防御性工程原则已落Architecture；受影响现行文本／导航／保护校验一致。这里只检查文档和引用，不额外产生游戏测试或全仓审计。

**B类继续随迁移逐步处理：**旧方案、重复报告、快照等历史文件整理不作PU01前置；默认入口更换不等于物理删除。清理／删除仍须路径级引用、独有信息、恢复定位等依据及对应明确授权；本申请不包含历史批量整理或删除。Step1的19份材料、可靠重取门禁，Step3的PU01代码范围与验证门禁均保持原样。

### Step1拟发布的明确材料（19份，不是19份默认必读文件）

- 当前候选根目录2份：`Architecture_Convergence_Integrated_Roadmap_DRAFT.md`；Technical下`Engine_Reference.md`。
- 本External_Audit_Disposition目录13份Markdown：`README.md`、`Audit_Finding_Disposition.md`、`Claude_Targeted_Reaudit_Package.md`、`Completion_Wake_Responsibility.md`、`D1_Branch_Disposition.md`、`Decision_Closure_Revised.md`、`Evidence_Debt_Coverage.md`、`Formal_Authority_Sync_Delta.md`、`NET_Cold_Load_Contract.md`、`Owner_Gate_Remaining_Decisions.md`、`Owner_Handoff_20261104.md`、`P3_Production_Dependency_Inventory.md`、`PU_Option_B_Revised_Plan.md`。
- 现有Advisory/Architecture_Engineering_Audit目录4份Stable原件：`Independent_Audit_v3_Final.md`、`Independent_Audit_v3_Final_Evidence.md`、`Targeted_Reaudit_Integrated_Roadmap.md`、`C1_C5_Short_Recheck.md`。只经审查发布其原字节，不改Advisor内容。

既有已跟踪历史不重复制造新副本；发布前若发现上述任何材料状态不明确、所需审阅未完成、并行改动、敏感信息或引用缺口，按受影响文件处理，不擅改他人冻结文档。引擎／HD源文件、数据库、原始日志截图和私有路径留在Git外；引用使用来源ID、版本、必要证据及已有外部定位。本地Raw／哈希不是永久备份；正式化必须保全的独有结论与审计依上述可重取发布链保存。

## PU01范围与停止边界

PU01保持现有专业规则、金额、资格／严格交易、max/Floor、历史／存档权威、原GC策略及已有NET-1/NET-2保护。只允许为该首片所需的有限技术状态／共享阶段／写屏障职责迁移；若最小真实闭包比预期大，先说明具体扩张，不借提取kernel启动O1全包。

**不包含**：Tier新算法或建筑目录映射实施；O1官方provider、O5/O6 HD解耦／UI端口；PU02–11或其他O包；新探针；游戏启动／配置切换；部署；U5；main/PR晋升；历史清理或删除。先前未来HD-free捕获／固定加载冒烟授权保留，但本申请不提前安排执行。A21–A26及PU05b/S7d6原生证据继续OPEN。

## 当前完成与申请状态

本轮在已接受的短复查／N1–N3基础上，完成了现有Workflow／AGENTS的定域对照、Step2职责与验收条件补齐、候选文档检查及最终申请更新。没有执行发布、正式同步、生产测试／代码、部署或新实机验收。

User decision：是否批准上述**Step1→Step2→Step3**窄范围申请（含各步完成后提交／推送develop）？
User testing：本轮无；未把后续HD验证或U5提前。
Primary next：等待明确授权；获批后按顺序执行，只在真实阻碍或授权范围扩张处暂停。

## Execution authorization checkpoint

The Owner explicitly authorized this final staged request in the continuing Primary session. Authorized order: reviewed publication and remote retrieval verification → first formal sync including the finite A set → current-HD PU01 only. Approval does not start later HD packages, deployment, game tests, U5 or main promotion. Earlier request/pending wording above is proposal history, not a requirement to ask again.
