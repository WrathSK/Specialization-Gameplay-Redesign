# Decision Closure Register：批准、证据、决定与正式同步

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[执行摘要](Executive_Architecture_Map.md)｜[决定包与门禁](Owner_Gate_Stop_Report.md)｜[正式同步差异](Formal_Authority_Sync_Delta.md)

## 状态语义

- `APPROVED`：Owner在H3明确批准的目标，不重新开票；不表示已实施。
- `ENGINEERING_EVIDENCE_OPEN`：技术根因／接口／验证尚未完成，不伪装成新玩法选择。
- `OPEN_OWNER_DECISION`：真实重大语义尚未选定，只有对应决定包可关闭。
- `FORMAL_SYNC_PENDING`：目标与当前D0058/A0183尚未同步；本轮只提供文本提案。

同一行可有多个状态；它们不是项目Status的新注册表。源码／正式权威与v2一致；本包中文按H3交付要求，不改仓库语言治理。

## DEC01–14

| 项 | 已批准的目标和相对v2修正 | 状态 | 证据、差异与依赖 |
|---|---|---|---|
| DEC01 | 逐能力／输入／用途；合法纯被动优先同ref最后确认输入+新事实重算，真实负事实优先；不可逆独立严格 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | H3科研／文化／商业补充；F01–60分别登记，不把方向当全表特权；S03，O1 |
| DEC02 | 统一ACTIVE接口，底层Ceiling细节不泄漏到专业；异常先root；不建各专业／复杂跨事件总督缓存 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S01；正常无总督=KNOWN1；六属性未证实正常异常率；旧Potential下降常规示例撤回 |
| DEC03 | raw事实cold重建，无通用事实持久化；窄历史／承诺／交易证据保留 | APPROVED；FORMAL_SYNC_PENDING | D2派生冷归因是否仍需保留是ODP01，不能借DEC03擅删；S04 |
| DEC04 | 中央可靠交付到专业接管；ACK不是应用成功；专业自身完成／错误／恢复；最新责任不丢 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S02；字段与函数名由Primary工程设计，不新增Owner投票；O2 |
| DEC05 | 专业schema／合法业务转换，Store身份／CAS／读回／提交次序；独立owner保留 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S07；O4按既有结果差分，不造PolicyEngine |
| DEC06 | root与显式错误；保留有证据确定性／deferred，不建设全面零基线重置程序 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | SAFE004/A0183:21/640仍旧文本；S07；FS05是替换候选，不改冻结决定 |
| DEC07 | 工程研习E完整历史严格；不以当前拥有或E下限补造发奖资格 | APPROVED；ENGINEERING_EVIDENCE_OPEN | S08；gate本身已匹配，采集／持久化错误root仍需证据；不再讨论低保E |
| DEC08 | 真原生Claim提前完成合法；唯一候选/ref/receipt；只核实完成／取消事件真实性 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S09；不存在缺内部timer即拒绝的目标；Narrative bCanceled不移植 |
| DEC09 | 四专业成功启动后自声明订阅，中央校验分发；phase0与独特直接监听保留 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S02；O5最小明确清单，无自动插件发现，不推断业务资格 |
| DEC10 | 城市身份／历史，实例资格／位置；未来M1/M2只候选 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S07；不提前选择多实例／未来管理容量制度 |
| DEC11 | PU优先总体范围已批准，但未批准任何实际PU；原S9/S10与新增底层债由OptionB完整收敛 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | [PU清单](Pre_U5_Final_Candidate.md)和[O计划](Option_B_Final_Candidate_Plan.md)；Owner最终计划→Claude→发现闭环→Owner再授权 |
| DEC12 | 必要工作、最少浪费、实机可接受；无任意百分比／CPU／RAMKPI，必要通知不算浪费 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING | S14；源代码工作形状、LOCAL计数、USER_NATIVE感受分层；不借性能删正确恢复 |
| DEC13 | 首次完成登记查事件／目标／读取时机；不猜顺序、清error或新增见证 | APPROVED；ENGINEERING_EVIDENCE_OPEN | S07；新增持久见证必须先证必要再另批；正常可达错误须窄修 |
| DEC14 | 退出/夺回root先行；合法延迟才明确事件接续；严格端点授权，不盲重放 | APPROVED；ENGINEERING_EVIDENCE_OPEN | S07；旧清理仅foreign loss.target，已回归城市不当然仍是合法目标 |

## R1–R6 补充闭环

| 项 | v3处理 | 状态 |
|---|---|---|
| R1 | Cross D歧义关闭：只读基础相邻。科研相关D／workers／集合、商业D／workers、文化共享一致GW按H3细分；其它具体异常格子维持现规则到证据／明确批准，不全表默认放行 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| R2 | `AcceptChange(scope,ticket)` 候选最小合同已可编计划；先可靠登记责任再ACK、revision防重入、owner保留失败；不再问字段名或A/B | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING |
| R3 | 成功Start导出声明、最终Binding槽校验、sealed后drain；四专业全部迁移；失败／重复／非法类型显式报错 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING |
| R4 | 专业历史转换/Store提交、错误root、合法deferred审查；不把silentHELD作为完成，不机械删除现有恢复 | APPROVED；ENGINEERING_EVIDENCE_OPEN；FORMAL_SYNC_PENDING |
| R5 | 精确PU01/02/03/05/06优先；PU04证实后窄修；其它证据若正常缺陷妨碍U5再精确纳入；没有代码授权 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| R6 | 信誉是自有权威；若极端继续则统一R0包括风险，旧模式选择撤回；是否启用、及其严格交易例外范围需ODP02闭环 | APPROVED（一致性）；OPEN_OWNER_DECISION（启用/边界）；FORMAL_SYNC_PENDING |

## 新网络／诊断门禁

| 目标 | 已批准部分 | 还未决定／未证明 |
|---|---|---|
| 可靠网络正常发布 | 共享层完成可靠拓扑后才交正常更新；dirty立即登记／严格凭据失效；确认负事实不等unknownsibling | 当前pending/mixed通知尚须迁移；同值、cold、首发丢失与合法窗口工程证据开放 |
| D1过渡退役 | 现在不删；正常目标不依赖其consumerhold，须禁用／真删除差分 | 退出证据未执行；“只是上次效果没动”不算root修复或退役完成 |
| D2必要性 | 先分清current重建、永久历史、旧应用归因；不能自动接线或自动删除 | **OPEN_OWNER_DECISION：ODP01**；A0183／Network旧合同仍在，O3按选择分支 |
| 标准化本城不长期被无关网络阻塞 | 公式仍max，已确认本城／负事实要有效处理 | 单一物理载体不代表必须两全额相加；remote异常处理依赖ODP01，不批准未证必要的拆分 |
| P3可移除诊断 | 生产职责先提取，观测只读稳定接口，四专业与所有相关路径通过disable/remove差分 | 新G30实际诊断加载耦合、P内写屏障、Flight／GC混合职责须迁移；不是数量专项结论 |

## 重大未决与非Owner编码事项

已知两项重大未决就是ODP01／02。具体ticket字段、索引容器、函数名、纯delegate布局、四专业声明列表代码位置，由Primary按本候选合同与证据制定，不再制造投票。若后续证据表明必须改变事实权威、持久化范围、生命周期政策、当前max公式或不可逆门槛，再追加精简Owner Packet并停止依赖包。

没有把`ENGINEERING_EVIDENCE_OPEN`写成“已通过”，也没有因某条记录可保留就说异常已解决。本轮不执行任何工程／实机验证，只准备将来可审计的门禁。
