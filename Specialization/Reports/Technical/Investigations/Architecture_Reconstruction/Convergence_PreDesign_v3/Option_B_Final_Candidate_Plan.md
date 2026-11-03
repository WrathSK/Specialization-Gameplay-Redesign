# Option B 全面收敛：final candidate，未批准执行

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[Owner门禁](Owner_Gate_Stop_Report.md)｜[正式差异](Formal_Authority_Sync_Delta.md)｜[PU](Pre_U5_Final_Candidate.md)｜[Gap证据](Gap_Matrix_v3.md)

## 1. 审计必须在实施前

~~~mermaid
flowchart TD
  V["v3候选"] --> D["Owner决定包闭环/最终计划认可"]
  D --> A["Claude Code独立只读审计"]
  A --> F["Finding逐条处置/严重问题实施前重审"]
  F --> G["Owner再次放行/明确实施与规范授权"]
  G --> P["获批正式同步与Pre-U5"]
  P --> U["U5迁移前行为基线"]
  U --> O1["O1事实与统一ACTIVE"]
  O1 --> O2["O2可靠交付/专业责任"]
  O2 --> O3["O3可靠网络/cold/D1/D2"]
  O2 --> O4["O4历史规则/Store/root"]
  O2 --> O5["O5四专业自声明"]
  O1 --> O6["O6实际应用UI"]
  O3 --> O7["O7生产职责/诊断/旧模块退出"]
  O4 --> O7
  O5 --> O7
  O6 --> O7
  O7 --> O8["O8无效工作/整合验收"]
  O8 --> E["Owner收敛验收"]
~~~

图是依赖合同，不是运行调用或全包串行硬限制：O4纯转换、O5机械词汇和O6独立owner可按各自前提拆分。P3从O2/O5新增路径时就生效，不等O7才补。每片独立可审查、可回退，不做大提交。

Pre-U5最小是为保留行为基线；**OptionB必须尽量还清已识别底层债**。具体引擎限制/例外要有证据和Owner裁定，不以“还能运行”或“以后再做”结项。平行footprint专项不阻塞编制，也未被当本包证据。

## 2. O1–O8 入口／工作／出口

| 包 | 入口 | 必须完成的真实责任 | 出口与最小回归 |
|---|---|---|---|
| O1共享事实/ACTIVE | 最终F表/formal合同、U5基线、root证据路径 | 统一ACTIVE，底层来源独立；修正常读取/时机/ref错误；共享D/worker/anchor/GW采集；获批同reflast-confirmed+新事实重算；Potential非法下降严重错误；不建专业Governorcache | 正常链可靠而非fallback常态；真实owner current/retained/first/cold/negative/同回合第二变差分；无私有重复采集；未批准格子不放行 |
| O2协调/接管 | O1相关事实、phase0/ACK合同 | 直到专业登记责任才解除交付；revision/ref/reentry/ACK丢失；专业负责失败/恢复；G08全链；错误状态不只在trace，诊断不驱动drain | 真producer→central→owner throw/missing/noACK/duplicate/HELD/newchange/load/close；成功sibling不重跑，静置不补预算，交易独立严格 |
| O3可靠网络/cold | 可靠正常发布合同；**ODP01具体分支与异常处置闭环**；O2 | 共享层完成topology/source采集root和cold接线；确认负事实优先；D2按A/B/C真实实现/缩减/退出；本城标准化不长期被无关网络阻塞，仍max；D1退出证明 | create/expire/reestablish/signal-only/cold首发丢失/ACK/空网vs失败/负事实/secondchange；不偷造旧归因；D1保留/禁用/真实移除差分；strict凭据同步失效 |
| O4专业历史/Store/root | root-first正式文本、ODP02、合法转换清单 | 专业schema/纯业务转换，Storeparent/token/CAS/readback/order/opaque保护；修历史采集/计龄/首次登记/退出root；合法确定性和deferred保留；信誉严重错误可见；无全面reset | old/new payload/error/结果差分；foreign合法窗口vsreturned端点；原字节不猜改，无奖钱unit重放，E完整、Dialogue/Insights独立；具体无法支持则报边界，不silent长期HELD |
| O5有限注册/四专业自声明 | 接管入口、成功Start事务、明确composition | 四专业专属owner声明；共同能力owner只注册一次；kind/family/展示机械资料；最终slot验证，phase0保留、failed无半注册；独特native监听保留 | 四专业声明前后等价；duplicate/type/missing/FAILED/SKIPPED/exit/order；无插件发现/业务资格推断；未来容量/M1/M2未实施 |
| O6实际应用展示 | ownerapplied与typedreply/ref合同 | 原S9D11完整owner→reply→机构UI，applied/gate/provenance/error和preview区分；banner统一ACTIVE；UI采集仅事实来源 | 失败写/cold未观察/retained/退出不冒充current；正常已验收图标比例/颜色/布局不扩大改造；无新UI业务公式/额外深扫 |
| O7生产职责/旧层退出 | 相关O3/O4/O5/O6职责移交；双部署删除和P3计划 | Q1–Q8实际reader/writer/ACK/清理/decorator移走；提取Pengineadapter/写屏障、必要Flight、现GC政策owner；可选trace无生产依赖；精确退出imports/replacement；保留SQL/saveID | 真absent file/global与开关差分只少诊断；无dangling生产caller；两个工具精确删除/failpoint/receipt/rollback；不按名字/前缀删，不隐式改GC |
| O8无效工作/整合清偿 | 实际接口稳定、现有负载证据，无需等专项 | 消除已证重复采集/无关wake/冗余scan-write/容量放大/无理由retry；必要通知/历史发现保留；每项修复或具体证据例外；正式文本与实现一致 | 真实producer-consumer、容量边界、静置、foreign无关、同回合第二变、受控恢复；少量changed/load/turn/idle原生；无CPU/RAM/%KPI；必须G行关闭或Owner批准具体例外 |

O3分支不默认选：A完成旧warm/cold真实归因；B仅会话极端保护与cold重建、异常cold处置先明确；C先批准替代异常/负事实规则再退出D2。任何分支都不删真实永久Insights/模板/L/交易收据。O1/2/4/5/6无关分析不被ODP01阻塞。

PU先关闭的窄问题在O包只处理剩余责任，不重做；Crewproof不因公共Carrier/helper抽取而自动解决。

## 3. D1退役 gate

当前D1不删。最终不能只是把hold移到中央而掩盖无完成路径。

| Gate | 必须证实 |
|---|---|
| D1-E1 正常可靠 | ordinary创建/到期/重建/cold/signal-only均在共享owner可靠就绪后发布；不是每专业处理UNKNOWN |
| D1-E2 完整责任 | dirty立即invalidatestrict/登记；首发丢失、同值恢复、同回合第二变有真实唤醒；旧ACK不清新责任 |
| D1-E3 负事实 | 确认route/source/ACTIVE/identity/owner/ref退出及时，不能等unknownsibling或把失败当空 |
| D1-E4 本城与max | self可靠事实正常生效，remote只有选定合法凭据；max不变；两个全额相加和组合长期冻结都不是解法 |
| D1-E5 禁用对照 | 同初始状态独立夹具保留vs禁用consumerD1，在普通load/route/role/negative场景业务一致；异常显式错误、隔离、有界责任 |
| D1-E6 真删除 | 旧D1分支/模块/import真实不存在仍正常；不是只ENABLED=false；无暗production依赖 |
| D1-E7 正式/原生 | ODP01和FormalSync闭环，少量changed原生；旧效果不授权交易，无重复发放/Carrierchurn；Owner批准退出 |

Gate失败就不删，不靠旧效果没动宣布成功。共享层有pending责任但正常不能完成也不算root已修。具体引擎限制需证据、边界与Owner允许例外。

## 4. 原S9未完成义务

| 原责任 | 当前基础 | 最终义务 |
|---|---|---|
| adapter注册/隔离 | SafeAdapters/生产面板/timed机制在用 | O5/O7迁实际受影响接口，失败sibling/顺序差分；不整体重开已完成模块 |
| typedrequests/replies、Gameplaytargets | PlayerActionReplies、DevelopmentInvestmentTargets在用 | O6/O7保持currentness/选城绑定/业务归Gameplay；新错误/applied投影触及则测 |
| D11 InstitutionView | 部分ownerpublication，UI仍age/L候选算术 | O6真实全链；同名API存在不是完成 |
| adjacency/共享采集 | SampleLifecycle/CrossSample基础存在 | O1/O8处理已证重复；必要完整proof与历史发现不默认浪费 |
| coldnetwork归因 | Model/Cell/Store有，生产consumer未接 | O3**依ODP01重定**，不自动接也不擅删旧保护 |
| deferred/subrecords | 生产实际恢复已存在 | O4按合法证据保留/迁移/修root，不全删或全reset |
| U4/集成 | 局部记录与USER_NATIVE主线 | Pre/U5基线和changedO路径回归；不加总局部PASS伪装全绿 |

## 5. 原S10／P3职责账本

| 义务 | 当前真实依赖/核查对象 | 删除前移交与证明 |
|---|---|---|
| Q1 InspirationProbe | Inspiration有Withdraw调用 | 迁生产exactcleanup，无probe仍退出 |
| Q2计时UI | ProjectTurnRead/Selection/Display与TimedTurn ActionPanelreplacement，可能overflow引用 | 迁productionadapter/reader，所有实际caller退出才撤replacement |
| Q3 Construction/CrewPrecision | UnitActions cost/progress snapshot/decorator | 明确生产owner，保持原native不可逆证明，D5独立gate |
| Q4 MeaningProbe | file/binding不证明active | 查Start/guard/cleanup/export，实际无依赖再删 |
| Q5 ExpeditionGate | 当前SpyGate与旧文件/SQL/save别混 | 只撤retiredpath，必要行保留，不做Expedition功能修复 |
| Q6 identity/inheritance | IdentityMapping/NetworkIsolation确有Start | 搬实际职责，inactive实验分别核验，不整组删 |
| Q7 Dialogue | positivewriter退役，ACK/generation/ready/ownedcleanup仍在 | transport/fact/effectowner接管，真pairedreceipt和cleanup差分 |
| Q8 Half/GreatWorkProbe | Halfpositive已earlyreturn，其它reader/cleanup个别核验 | DEV/observeronly后可移除，必要生产不随观测消失 |
| G30加载/kernel | Bridge直接include/New诊断；P含写屏障；Counters含Flight/GC | O2/O5/O7稳定生产接口分离，缺file/global仍能run，trace只观察 |
| TOOL-04 | stable拒unreviewedextras；temporary有hash/rollback但无同等removed-diffreview | 两工具受审exactremovedset/receipt/failpoint/rollback，未知文件不静默删 |
| SQL/saveID | Lua退出不等于可删定义 | 无单独compatibilitybreak批准则保留，不承诺旧档迁移 |

## 6. Disable／remove differential

同初始状态的独立fixture三组：观测正常、诊断关、诊断file/global真不存在。比较startup、统一ACTIVE/资格、完整record/receipts、ownedCarrier、Treasury/Unit、通知/恢复、typed业务UI；只准诊断数据/计数/监听不同。不可在live重复不确定交易来做对照。

writebarrier、Flightbookkeeping、业务错误和受批GC不是可丢观测数据：先独立明确生产owner并保留策略。absence改变业务就是G30/O7未过，不能“以后修”。

## 7. 实施前外部审计与完成条件

每包RuntimeImpact、真实producer/consumer闭包、normal/negative/first/cold/error/reentry/irreversible测试与精确证据；未执行不能写PASS。已验收科研/文化只changed最小delta，不重开campaign；不要求随机掠夺/商人死亡/易主玩法。

Claude外部审计在实施前；每Finding接受/反驳/需Owner决定附证据，重大问题先改计划重审；Owner再次明确实施授权后才能代码。审计PASS或报告发布不授权部署/main。

新增重大规则/保存/端点/引擎限制→停依赖包Ownerpacket。完成不是“写过包”“UNKNOWN被保留”“文件减少”：必须G行关闭/具体获批例外、职责实际退出、正式文本一致、D1/P3差分和changed原生足够、Owner验收。禁止无结束条件新旧并存。
