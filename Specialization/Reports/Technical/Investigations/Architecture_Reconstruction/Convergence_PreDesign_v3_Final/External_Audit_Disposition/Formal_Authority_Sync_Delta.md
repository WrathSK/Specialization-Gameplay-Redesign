# Formal Authority Sync Delta：穷举受影响位置的提案

Status: Stable candidate — C1–C5计划闭合已获Owner接受，N1–N3合入后继提案；已补Step2 A类最小集合；正式同步仍未获授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅修订候选／参考文档并作只读证据及文档完整性检查；不改冻结报告、生产、测试、工具、正式规范或状态，不运行生产测试／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 1. 应用边界与时点

这是下一次获批同步的精确工作单，不是patch，不分配新D/A/S号、accepted hash或修改冻结Authority。先Owner认可候选送审→定域复审Finding处置→Owner再次授权正式同步/实施→按现行D/A successor、接受记录与引用流程同步。**第一同步片在任何Pre-U5代码之前**撤销过时S9派生保存接线任务及旧candidate冷partial/跨版本兼容义务；此前须完成C4可靠保全：必要候选／原审主文与证据及本次Stable复审经隐私审查提交、推送并验证取回，或采用另一项获批可靠归档。不能把ignored本地副本／哈希称永久备份。首次同步完成时，已替代候选退出默认阅读路径，正式Markdown＋Status接管；其余接口在首次依赖代码前同步，不能到O3才处理旧排期冲突。

历史冻结Design版本、Advisory正文、Validation冻结结果和既有proposal不就地改写；新accepted记录/当前路由明确取代哪些未来任务。更新当前引用不把历史证据重写成新规则；正式Markdown仍是规范权威，报告和图无独立权威。

## 2. 逐FS正式载体清单

以下是当前权威链及受影响现行重复表述的定域清单（不是全库历史搜索）。同一FS中的Spec/Content/阅读正文/架构/当前任务路由必须同批一致；含旧版专业数字的历史溯源段不按字符串批量替换。

| FS | 当前精确位置 | 后继语义／动作 | 最晚时点 |
|---|---|---|---|
| FS01 状态/边界 | Design/Specialization_v0.1_Design_Spec.md9、16、24、26；Architecture/Specialization_v0.1_Architecture.md16–27、634–646；Workflow README当前授权/验证条款 | 正常UNKNOWN root-first、OD-1～4与已有ODP/DEC分开；Scope说明不再授权旧coldpartial或跨构建兼容；本轮无实施 | 首次同步/Pre前 |
| FS02 ACTIVE | Architecture71–88/172/186；Design/Shared.md资格段；Shared_D0058 concepts共同资格与重组约束（128等） | 统一ACTIVE当前事实/正常无总督KNOWN1、同值可用性；同episode增长与合法重组新episode P−1分开；不建专业cache | O1首片前 |
| FS03 网络 | Design/Network.md47–59；Spec NET-004281/NET-005283；Shared_D0058 NETWORK_LAYER（81及352的例外副本）；Commerce_D0058392；Culture_D0058543；Industry_D0058458/612；Architecture138–148 | 可靠发布/严格dirty失效/真实负事实、正常冷恢复屏障；未知role/provenance/用途availability与实际I分离；未完成不能新交易 | 首次同步解除旧义务；O3 cutover前新接口完整 |
| FS04 D2/cold | 上行全部cold例外副本；Industry_D0058595 pending_fact_policy、Culture_D0058483 pending_fact_policy；Architecture18（派生保存许可）、19（真实deferred仍保）、145/634–635 | ODP01=B+OD1：warm W有界；正常cold从F/真历史幂等恢复，不接派生历史；撤旧A失效来源特权的目标，但**不预选severe cold K-only/清除/全额** | 首次同步取消旧S9 cold接线；实现待工程证据 |
| FS05 子记录 | Spec SAFE-00426；Shared_D0058 sub-record恢复条目；Architecture21/640；Store相关正式保存/恢复合同 | root/真实确定性/合法deferred保留；严重错误范围化；不建全面猜baseline重置流程。OD2合法转换与坏历史恢复严格区别，不静默HELD当完成 | 首次同步目标边界；O4首片前 |
| FS06 信誉/交易 | Spec16/24、商业261/265；Commerce.md信誉与签约/已签条款段；Commerce_D0058263/281、288–312、372–377/390；Shared_D0058114；Architecture639；Architecture/v2/Commerce_Preparation.md200附近 | R四类来源、独立叶例外、VENTURE quote/confirm/locked条款、STABLE无需无关R；CREDIT_*等未决保护；合法身份退出reset；samebuild内已签不追改，不新增旧版本元数据解码任务 | PU06首片前 |
| FS07 职责/历史 | Architecture专业owner与保存段92–100及634–642；Spec PROG-011138、生命周期158、CREW/Claim/项目条款；Shared_D0058及三专业truehistory/项目内容；Architecture/v2/Industry_Preparation.md | Store控身份/CAS，专业schema/合法转换；Crew每completion唯一proof且异常仅相应order；Claim trueearly、UNKNOWN marker不当取消；现合法归属/易主范围不扩大 | 对应PU05/07/08/09或O4前 |
| FS08 交付 | Architecture P03:168、P06:171及public更新/临时状态段；Workflow Runtime Impact/targeted gates | **增补**P03/P06，不替代其容量/尝试/exit disposal：phase0同步完成，普通owner已登记再ACK；failed/false/missing不吞；成功siblings不重跑；共享phase边界清楚 | PU03/O2首片前 |
| FS09 声明/启动 | Architecture运行入口、P01/P02/P07及startup/Bindings说明；当前composition职责 | 成功Start普通订阅声明；phase0显式rank+literalBridge窗口；Seal后drain；FAILED/SKIPPED隔离；mandatory exit/return cleanup预注册fail-closed例外 | O5及接管相关首片前 |
| FS10 生产/诊断 | Architecture73–75与530（实际Binding/Journal/FreshHook/Flow链）、P08/P09:173–174、193、D12:643、GC边界632；相关Workflow RIC/T门禁 | 补P3-01–25全链；生产kernel/写屏障/Flight/现GC/错误/ACK/cleanup先接班；真缺文件差分；SQL名非删除证据，unused adapter安全退出 | 防御性工程原则及Step2 A类集合首次同步／PU01前；其余按最早相关依赖，最终O7 |
| FS11 工业独立 | Architecture92–100、Industry_Preparation巨构/研习/history章节；Industry_D0058相关条目；Spec IND-PRACTICE235等不变参数 | 巨构只current era+ACTIVE，无N/E/L/queue/network；工程研习E严格，组建成本锁定、倍率与完成proof独立。仅技术澄清，不改公式 | 关联owner变化之前 |
| FS12 UI/工作量/结束 | Architecture150–158/170/174/642；Workflow验证/证据门禁；Status当前完成定义 | 展示实际applied/retained/error，不以候选代收益；domain/target独立；现行证据政策；samebuild中规模样本；无重复native/任意性能KPI | Step2 A类工作流／汇报／交接集合首次同步／PU01前；其他对应O6/8前及最终收敛 |

正式主入口链接：[Specialization/Design/Specialization_v0.1_Design_Spec.md:283](../../../../../../Design/Specialization_v0.1_Design_Spec.md#L283)、[Specialization/Design/Network.md:49](../../../../../../Design/Network.md#L49)、[Specialization/Design/Content/Shared_D0058.json:81](../../../../../../Design/Content/Shared_D0058.json#L81)、[Specialization/Design/Content/Shared_D0058.json:352](../../../../../../Design/Content/Shared_D0058.json#L352)、[Specialization/Design/Content/Commerce_D0058.json:392](../../../../../../Design/Content/Commerce_D0058.json#L392)、[Specialization/Design/Content/Culture_D0058.json:543](../../../../../../Design/Content/Culture_D0058.json#L543)、[Specialization/Design/Content/Industry_D0058.json:595](../../../../../../Design/Content/Industry_D0058.json#L595)、[Specialization/Architecture/Specialization_v0.1_Architecture.md:168](../../../../../../Architecture/Specialization_v0.1_Architecture.md#L168)。词句含在长JSON字符串中，按key与章节语义核对，不能仅替换出现“冷”字的位置。

## 3. successor核心文字（仅供审阅）

### FS03/04 — 正常恢复与异常边界

> 同一受支持构建的合法保存加载是状态恢复，不是新的业务变化。相关原生引用／效果恢复和Lua事实／历史／拓扑重建未完成时，不得凭缺失输入撤除、部分重算或覆盖已恢复载体。可靠完整可消费输入完成后按正式公式幂等核对；旧输出不是当前网络事实或新不可逆交易资格。
>
> **初始化尚未完成时出现可靠负事实，立即撤销相应严格交易／资格并登记被动撤除责任；若当前原生整体不可拆且缺可靠来源见证，不虚构逐源减项，而在首个完整可消费快照执行对应撤除。** 接收城市本身已确认退出仍按合法exact退出处理；不得把缺getter当负事实，也不得无限以初始化为由不处理真实变化。
>
> 正常网络完整事实由共享owner可靠交付；dirty同步阻止严格资格并持有采集／交付责任。会话来源见证有界、逐来源provenance/ref，不跨cold成为派生保存权威。正常初始化、可用性恢复与读档后对账是正常路径，不因缺少旧派生快照另造持久化。
>
> **NET05超出正常初始化窗口仍无法恢复时，临时维持no-write：原已安装输出不改，标为未对账和可见严重错误，严格交易禁止。** 这不等于选择永久旧全额支付，也未批准K-only／清空。先修正确phase/事实/完成传播；若确证必须改变业务政策，提交最小Owner决定包，只停受影响部分。

### FS05/06 — 两种零不能混淆

> 独立信誉叶严重异常且其它基础/实际用途必需输入可靠时，按明示窄政策临时R0，只投影不改权威历史；错误与来源可见。CHECK_UNKNOWN来自缺依赖/父不一致/未决生命周期不自动符合政策。STABLE不人为增加无关R依赖，新VENTURE按当前确认来源锁terms且之后不追改；所有其它未知余额/证明/合同占位/付款入账receipt仍严格。
>
> 可信合法身份转换确认退出Commerce时，按既定规则重置信誉（合法初始schema），即使旧信誉叶暂不可读；受控提交只改转换要求的字段，保有效兄弟数据。不是为修坏历史猜0，也不把成功reset当根因已修；未知Capital/原生结果不一起清除。

已证永久不可恢复且缺可靠重建权威时，受影响不安全能力／结算应显式错误并阻止，未损坏兄弟继续；这不是将永久静默HELD认可为正常恢复，也不让玩家手工修记录。不建全面猜史／清零程序。若需新的损失、重建或不可逆结果政策，先Owner Packet；正式后继明确与原SAFE004窄baseline许可的取代范围，不能省略旧许可后让实现者自行选。

### FS08/09/10 — 接管和退出

> 普通消费者成功登记scope/ticket后ACK，phase0要求同步完成；FAILED/SKIPPED/false/missing和异常均有显式责任。重复变化、同值恢复、重入及旧ACK不能丢新单；容量/尝试/引用/退出规则补P03/P06而不替换。必要fail-closed exit/return cleanup与普通可撤订阅分离：模块FAILED／SKIPPED不得因尚未RegisterExit使已安装效果的必要退出责任漏登而放行。责任须在普通Start之外受控登记，或明确阻止未证明安全的退出；迁责后才退旧门禁。ExpeditionTraining的busy／throw／未确认返回不能被当作完成。诊断/DEV文件的生产kernel、写屏障、Flight/原GC、绑定/事实、错误、ACK、cleanup先迁正式owner，再以真实缺文件/缺global证明可退出。

## 4. 当前排期／接受链需要一并同步的具体位置

| 当前载体 | 后继动作（未来获批后） |
|---|---|
| Status CURRENT [Specialization/Status/Specialization_P0_Status.md:20](../../../../../../Status/Specialization_P0_Status.md#L20)；相关Primary next/remaining项 | 用新的current记录明确原S9冷派生接线撤销、OD1证据任务/O3替代；UI/合法deferred/S10职责迁移保留；不改旧批次历史正文 |
| [Specialization/Status/Validation/Results/Specialization_B399_Network_Project_Coverage_Reconciliation.md:24](../../../../../../Status/Validation/Results/Specialization_B399_Network_Project_Coverage_Reconciliation.md#L24)、45 | 冻结结果保持；当前route指向新后继说明取代“accepted cold integration仍需接线”的未来指令，既有实机覆盖不重写 |
| [Specialization/Reports/Proposals/Refactor_Recovery_Persistence_Proposal.md:84](../../../../../Proposals/Refactor_Recovery_Persistence_Proposal.md#L84) | 保原批准历史原文；新决定明确派生source extension不再要求接生产；真实owner deferred lifecycle扩展仍保，不整体撤销两项 |
| Architecture18/19、Refactor计划原S9/S10引用、旧v3/Final候选 | 现行正式接受/Status明确替代范围；旧候选仍只调查事实和冻结提案，不批量编辑 |
| Authority当前版本/accepted引用、Context Lock及manifest相关读取依据 | 正式successor接受后按实际受影响闭包更新；不只rehash旧冲突文本、不伪造新编号；本轮原字节保持 |
| Workflow相关运行影响/验证说明、根/项目AGENTS导航 | 必要最小合同/入口同步需对应明确权限；不另建治理体系，不重复把本报告全量加载为新权威 |
| Playtest_Workflow29、45–48 | OD4重申当前build新游戏＋samebuild load；移除候选超范围承诺，**不需新增兼容政策**；部署/代码回滚安全条款不削 |

当前手工定域读取已覆盖外审指出的所有正式重复位置；未来应用前须在当时HEAD重新核对受影响key/Current路由及accepted链，若有新同义现行副本也一并审查。历史版本/外审建议不作为要机械全改的现行文本。FS05/07的完整专业规则无语义改变处只更新技术引用，不借同步改其它能力数值。


## 2026-11-04 Addendum: precise additional successor locations (proposal only)

- **FS10 / Architecture after P01–P10:** adopt the corrected exact evidence-driven-defensive-engineering paragraph in [integrated §10.1](../Architecture_Convergence_Integrated_Roadmap_DRAFT.md#101-exact-future-normative-paragraph-and-single-authoritative-home). This is the single normative home; no new P11. Normal initialization/availability/post-load reconciliation is explicitly normal, and S7d6 irreversible-proof protections remain. Workflow RIC item4 only links to that rule; root AGENTS only navigates to it. No formal write is authorized in this reference phase.
- **FS07/09/10:** include [integrated §10.2–10.3](../Architecture_Convergence_Integrated_Roadmap_DRAFT.md#102-cross-profession-physical-carrier-and-lifecycle-matrix): installation/source/receiver, effect/history owner and legal reference/endpoint determine cleanup; current profession is not a whole cleanup selector. Nominal 29 direct handlers and LegacyCleanup's 11 internal groups have real duties, not proven optional logging gates. Mandatory duties move before genuine diagnostic absence.
- **FS07 / PU05/09:** separate project UNKNOWN root proof from marker protection; consume only verified completion fields, preserve true early Claim; synthetic InitUnit failure tests do not establish normal native failure. No speculative snapshots/regrant/state machine.
- **FS02/03/10/12:** use first-tranche [Engine Reference](../../../../Engine_Reference.md) for explicit same-core data/sampling/effect/UI assembly and the narrow Mac/GS support scope. Three HD wrapper names use official primitives, but scope/arguments/actual no-HD execution and effective-chain derivation and its consumer coverage remain gated. The latest Owner definition is recorded in integrated §6: Tier follows the loaded same-district upgrade chain, fixed cross-environment mapping withdrawn, HD tier table not authority. Preserve D formulas; this proposal does not silently make formal text obsolete.

These entries extend the existing FS list; they neither edit accepted authority nor create a second policy/implementation plan. Frozen original audit and prior evidence remain unchanged.

- **Protected Technical navigation:** `Reports/Technical/README.md` is a current Context Lock input. Keep it unchanged in this evidence phase. At authorized synchronization, add one short reference link after its introduction: “`[Engine Reference](Engine_Reference.md)` — bounded macOS/GS source and HD dependency evidence; Raw outside Git, static/community/native-unknown boundaries explicit; reference only.” Review/update the corresponding guard through the ordinary accepted sync process, not a blind rehash. The current candidate/re-audit entry already provides the reference route.

## 2026-11-04 scoped Owner disposition — remaining precise sync work

- **FS02/07, Shared source attribution:** record the latest Owner Tier correction in existing shared-fact/catalog contracts, not a new Design batch. Reflect only actual same-district building-upgrade prerequisite chains (Owner N1): outside-district buildings, virtual gates and other non-upgrade unlocks do not automatically increase Tier. Industrial Water Mill BUILDING_IZ_WATER_MILL is T1; its confirmed HD virtual gate is not a level. Do not ignore a prerequisite merely because absent from a Tier table; real missing/incomplete/cyclic/ambiguous chains remain errors. Keep ordinary eligibility separate, no silent T0/T1 or automatic HD-copy. HD old values are migration comparisons only (N2); explain Data Center/Hospitium/Garden deltas instead of fitting new rules to old caps/bumps. D min/sum/weights and three-tier D6/four-tier D10 stay. Resolve exact exceptional candidates before affected provider code, not by a universal hardcoded catalog.
- **FS07, C1/C2:** Crew unresolved receipt is source/order-scoped; per-type consumed high-water and irreversible one-shot proof remain. PU05a local scope repair independent from PU05b/S7d6 attribution. PU07 sticky Store completionError is a definite PU09 Claim prerequisite. Root-owner map and independent Dialogue Governor/era/isolation inputs in integrated §4 replace generic “current-production availability” wording.
- **FS09/10, C5/A23–26:** O5a data selection/final mapping precedes first O1 official provider; O5b ordinary runtime wiring follows O2. Separate HD JOINs, own assembly marker/selected components, final targets after mappings; every loaded ModifierType defined. O5 owns environment/UI-base assembly and verifies PU08-owned HD-independent exact exits; one fixed no-HD load smoke follows completed O5 assembly. O6 owns concrete UI callbacks/behavior/interaction acceptance and reuses that environment/evidence (N3), not a second full test.
- **FS01/12, fixed profiles/touchpoints:** U5 and post-migration HD comparison use the same pinned full profile, with actual HD/UC companions. Reduced HD profile is a separate certification. Future no-HD baseline DB capture and fixed adapted-SPC load smoke are Owner-authorized validation touchpoints; each keeps independent environment evidence. Final no-HD acceptance is targeted to environment-sensitive mechanisms/effects/UI/exits/load/irreversible operations, not a default second full playthrough. Third-party auto-update mid-campaign is outside same-environment support.
- **C4 final exit criterion:** once accepted Markdown and current routing contain the necessary contracts, old candidate plans/review bundles are history/reference on demand. Do not append this whole candidate set to mandatory Context Lock reading or leave two current plan tables. Exact history retrieval remains possible; no deletion authorized.

User decision: grant/withhold the staged publication→formal-sync→PU01 application; C1–C5/N1–N3 need no further planning vote. Step2 requires completed Step1; Step3 requires accepted completed Step2. User testing: none now. Primary next: no formal write before explicit permission and verified prerequisites.

## Step 2 limited workflow/current-information supplement — proposal only

Owner's current supplement is **planning permission only**. Apply this finite set during the first authorized formal sync, after Step1 reliable publication and **before PU01**. Reuse existing FS01/10/12; no new Finding/work-package IDs, independent audit, authority hierarchy platform or mandatory reference library. Step1 and PU01 scope/tests remain unchanged. Line numbers below are locators at develop954dc67, not permission to edit formal files now.

### Existing coverage, actual gaps and precise edit locations

| Existing source / scoped check | Disposition and minimum proposed edit |
|---|---|
| Workflow W0005 opening5–13; Durable recovery58–70; trust hierarchy143–150 | User authority, Design/Architecture and history limits already exist. Refine the technical-structure row to **accepted** Architecture/task contracts; separate technical findings into a Reference row with Engine_Reference. Add the short role/precedence paragraph below. No second authority and no new register. |
| Workflow Start84–92, action-scoped94–115 and reading classes126–141; root AGENTS start section | Task-scoped/manifest-as-envelope and no-read-all already exist: retain them. Insert the native evidence-routing paragraph below into the existing action-scoped section. Root AGENTS adds only a link to this route in its existing start paragraph; no library-wide reading mandate. |
| Workflow End116–124 and accepted evidence storage212–220 | Clarify “update Status, batch result” so ordinary completion is not interpreted as a required new permanent process report. Use the replacement below; preserve exact tested source, command/environment/outcome/limits and unique evidence/retention. Do not weaken tests, local run artifacts or required immutable evidence. |
| Workflow Language48–56; project AGENTS “用户交付与诊断” | Existing Chinese dialogue/self-contained summary is narrower than Owner's all-important-stage request. Add one Owner-summary bullet below; replace project AGENTS' generic summary instruction with a link to it. Existing player-facing report detail remains. |
| Workflow interruption recovery94–115 and End116–124; integrated §7 existing seven-line handoff | Recovery and “no mandatory handoff document” already exist and remain. Add the safe accepted-module/migration-slice handoff clause below; reuse the seven short fields from integrated §7, no new permanent file or transcript dump. |
| Architecture runtime integration P01–P10:162–177; existing FS10 / integrated §10.1 | The evidence-driven defensive-engineering paragraph is already agreed as a proposed successor and is not yet formal. **Apply exactly that paragraph after P10** in Step2, including normal-restoration and irreversible-proof carve-outs. Workflow RIC item4 only links there; root AGENTS integration paragraph links there, no duplicate normative wording/P11. |
| Technical README introduction1–3; Status CURRENT and existing FS01/current-routing rows | Insert the short conditional Engine_Reference link below. Status CURRENT names the actual stage, accepted source, what is implemented versus pending, evidence level and next authorized boundary. Route to affected current contracts; superseded candidates/history are on-demand. Update only genuinely affected manifests/guards by existing acceptance rules; no default full audit ingestion or bulk guard removal. |

**No unresolved semantic conflict.** The only current wording tension is End protocol's “batch result”, which can be misread as “new file every time”; the clarification remains fully compatible with the accepted evidence policy. A short safe-boundary handoff does not contradict “no mandatory handoff document”: it can be given in chat and current Status. Publishing reference/history is distinct from accepting rules or adding mandatory context. This is a targeted text comparison, not a whole-repository lifecycle audit.

### Proposed concise successor text (apply only after authorization)

**1. Workflow W0005 — refine the existing recovery table, then clarify roles.** Replace its technical row with accepted Architecture/task contracts and use a separate Reference row: “Engine_Reference and question-indexed project findings — source/version/context-qualified evidence, not accepted rules or implementation permission.” Follow the table with:

> Accepted Design owns gameplay semantics; accepted Architecture owns technical contracts consistent with Design; Workflow owns engineering procedure. Status/Authority report the current implementation, evidence and authorized boundary, not new gameplay or architecture. Reference supports technical conclusions within its stated version/context/evidence limits; neither it nor historical reports overrides accepted current rules. Record explicit Owner decisions through the existing acceptance process before dependent implementation; do not resolve a conflict by choosing a preferred historical explanation.

**2. Workflow action-scoped reading — add after the existing minimum-reading table.**

> For native behavior, events, Modifiers, cold load, SQL or UI questions, first check the relevant current contract, named project evidence and the matching Engine_Reference question sections. Then consult only external primary/qualified sources needed for the remaining gap, preserving version, context and evidence limits. Do not load the whole reference, old plans, audits or source library by default. Request new minimal native validation only for a necessary unresolved question that applicable existing evidence and local checks cannot answer; identify the gap, affected path and distinguishing outcomes. Keep already approved fixed integration/load-smoke gates and the user's game/probe/deployment authorization boundaries.

Root AGENTS needs only a reference to that existing Workflow action-scoped section. Retain the current Start protocol, dependency-envelope integrity and enclosing-rule/qualification requirements; “minimum” is not permission to omit affected write/save/native contracts.

**3. Workflow End protocol — replace only its opening completion-update sentences; keep later hash/Git/deployment safeguards.**

> After the selected validation, update affected current rules only where an approved contract changes, and update current state/next boundary. Preserve a concise validation result with tested source, command/environment, outcomes, important counterexamples/measurements, limits and evidence locators in the appropriate existing Status/result or recoverable commit/PR record; do not create a new permanent process report by default. A separate report is justified by a substantial decision, irreplaceable native evidence, unique failure/incident or important acceptance. Existing required records, tests, local run artifacts, failure preservation and durable-evidence obligations remain unchanged. Revise Architecture only when its contract changes, not every ordinary batch.

**4. Workflow Language convention — one additional bullet; project AGENTS points here.**

> Begin every important-stage report with a brief Chinese Owner-facing summary: the current stage and actual goal; work actually completed, separating plan/audit closure from code/local validation and user-game evidence; material issues and project impact; concrete next changes; whether the Owner must decide or test (explicitly say none when not needed). Technical IDs are optional traceability after the explanation, not the narrative or assumed prior knowledge. Keep the summary short; it does not require a new document.

**5. Workflow End / recovery — add the accepted safe-boundary handoff clause.**

> After an accepted complete module or migration responsibility slice and synchronization of its current rules/state, give a short handoff and continue in a new conversation at a safe boundary. Include task/scope, source and deployed identity, authorization/exclusions, pending duties/receipts and owners, three-to-six relevant reading entries, actual evidence/remaining native limits, and next step/stop condition. Reuse current Status and the chat; no mandatory new handoff file or full transcript. Do not force a switch during an incomplete irreversible transaction or leave pending work without an owner.

**6. Technical navigation — one link after the existing introduction.**

> `[Engine Reference](Engine_Reference.md)` — read the relevant question sections alongside existing project evidence for native events, Modifiers, cold load, SQL/UI and environment dependencies. Reference evidence is not accepted Design/Architecture or implementation permission; no full-library reading requirement.

**7. Architecture / Workflow RIC / AGENTS — use the already approved single-home text.** Apply integrated §10.1 exactly after P10, with its qualified failure evidence, normal initialization/availability/post-load reconciliation, scope/recovery/exit ownership and irreversible-operation protections intact. Add only a reference in RIC item4 and AGENTS; do not store this as Agent memory alone or duplicate the norm in each entry file.

### Step2 completion gate, and what remains outside it

Before PU01, all seven edits above must have their approved content in the proper existing long-term sources; accepted current rules, English technical/Chinese Owner language roles and authority/state/evidence pointers must agree. Verify relevant Markdown links, current-source/manifest/guard consistency, no blanket full-reference/history-reading requirement, no automatic new-process-report requirement, no weakened test/evidence retention, and a usable short handoff at a complete safe boundary. Status must distinguish plan acceptance, implemented code and actual user-game evidence. These are document/integrity checks, **not new runtime or native tests**.

History sorting/duplicate reports/snapshots are B work, accompanying the relevant migration slices. First-sync retirement from default reading is A routing, not file deletion. No full-history cleanup is prerequisite to PU01; physical deletion still requires exact paths, live-reference/unique-information/retrieval evidence and the applicable explicit permission. No such deletion or new platform is authorized here.
