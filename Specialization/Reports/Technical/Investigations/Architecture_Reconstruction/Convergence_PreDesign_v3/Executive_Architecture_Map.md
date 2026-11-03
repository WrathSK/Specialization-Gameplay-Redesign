# v3 执行摘要与架构责任图

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


## 先给结论：仍有两项必须由 Owner 决定

1. **ODP-01：D-2 最终保留到什么程度。** 当前事实、永久历史、上次实际应用的派生贡献不是同一类数据。已有冷归因存储适配器尚未接入生产，不能为了完成旧 S9 自动接入，也不能未经批准删除既有连续性规则。
2. **ODP-02：信誉历史异常时，是否启用统一 R=0 的极端继续政策，并将其明确列为新交易输入的业务例外。** 若启用，被动与新风险投资一律一致；不得继续采用 v2 的“稳健继续／风险暂停”作为已选政策。STABLE 不依赖 R，不能人为增加依赖。

精简决定包见 [Owner Gate／Stop Report](Owner_Gate_Stop_Report.md)。其它只读契约与依赖已可讨论；外部审计材料已准备，但**尚不具备作为无重大未决项的最终计划送审的条件**。没有修复、迁移、实机、探针或正式规范变更。

## 文件导航

| 材料 | 用途 |
|---|---|
| [Decision Closure Register](Decision_Closure_Register.md) | DEC01–14／R1–R6 的批准、证据开放、待决和待同步状态 |
| [Fact & Subscription Contract](Fact_Subscription_Contract.md) | F01–F60、统一 ACTIVE、可靠网络发布、ACK、自声明订阅 |
| [Gap Matrix v3](Gap_Matrix_v3.md) | G01–G30 的根因证据、责任、方案、停止条件与验收 |
| [Pre-U5 final candidate](Pre_U5_Final_Candidate.md) | PU01–11，精确边界与最小回归，不代表允许执行 |
| [Option B final candidate](Option_B_Final_Candidate_Plan.md) | O1–O8 全面收敛、S9/S10、D1退役、诊断退出及逐包门禁 |
| [Formal Authority Sync Delta](Formal_Authority_Sync_Delta.md) | 正式条款的逐项拟修订原文／替换候选，均未应用 |
| [External Audit Package](External_Audit_Package.md) | 给 Claude Code 的短审计交接，不已启动审计 |
| [Owner Gate／Stop Report](Owner_Gate_Stop_Report.md) | 两项决定包、原生证据、外部审计和实施停止状态 |

## 七类目标责任

箭头区分原生事件、通知、主动读取调用与受控提交。七个责任框不要求对应七个 Lua 文件；引擎和 UI context 内的事实采样不是新增业务权威。

~~~mermaid
flowchart TD
  E["文明6引擎与原生状态"] -->|"原生事件：原因与引用"| C["变化协调：失效与交付责任"]
  E -->|"原生只读采样"| F["共享事实服务"]
  S["可靠 Store：身份、CAS、读回、提交"] -->|"读取：已确认历史"| F
  F -->|"通知：确认变化／确认负事实"| C
  C -->|"通知：范围与版本"| P["专业解释与计算"]
  P -->|"ACK：已接管scope/revision，非效果成功"| C
  P -->|"主动读取：最新可靠事实"| F
  P -->|"期望计划／严格业务请求"| X["效果与业务拥有者"]
  P -->|"历史转换请求"| H["专业历史规则"]
  H -->|"受控提交：已验证转换"| S
  S -->|"通知：确认提交"| C
  X -->|"原生写入与读回"| E
  X -->|"读取接口：实际应用值／错误"| U["UI展示与交互"]
  S -->|"读取：历史展示"| U
  U -->|"行动请求，Gameplay重新核验"| X
  U -->|"UI独有原生只读事实桥接"| F
~~~

图中的“协调登记”不一定晚于采集：**已知相关变化立刻使严格凭据失效并登记采集／交付责任**；正常可消费事实在拥有者完成可靠采集后发布。协调器不带整包事实、不算专业公式。UI 的路线／巨作原生采集通道只是事实来源，展示镜像和按钮都不能独立批准业务。

| 责任 | 当前主要实现 | 目标差异 |
|---|---|---|
| 事实 | EffectiveFacts、D、GreatWorkFacts、NetworkInput／Bridge；UI BackgroundRoutes／DialogueRefresh 提供部分原生采样 | 明确单一维护者、确认负事实与读取错误；ACTIVE统一接口；正常网络只发布可靠拓扑 |
| 协调 | NativeFacts归一化原因、FactChanges、Bindings、publish drain | 当前尝试数不等于接管；四专业声明订阅，可靠交付到 owner pending |
| 专业 | 四专业各能力模型／consumer | 自行 Pull、独立公式、共享采集；纯被动按获批用途 last-confirmed recomputation |
| 效果／业务 owner | 各效果 reconciler、Capital／Development／Crew等 | 自有精确 Carrier、读回、收据；不得用 ACK 或旧效果批准不可逆操作 |
| 历史规则 | 各 model、IndustryHistory，以及仍嵌在 Store 的业务分支 | 专业拥有 schema 和合法转换；Dialogue累计与 Insights分开 |
| Store | CityProgressionStore、PropertyCell／窄独立 owner | 身份、包络、CAS／readback、opaque sibling及提交次序；不收编所有独立历史 |
| UI | typed replies、机构／banner、行动面板及事实桥接 | 显示实际应用／来源／错误，不自行补算ACTIVE或冒充实际收益 |

当前对应及源码定位见 Gap／Sync Delta。**NativeFacts 不拥有全部事实值**；NetworkBridge 也不拥有各专业历史与收益公式。

## 四条关键流

1. **普通事件：**原生原因→引用／范围校验→立即失效与登记责任→事实拥有者采集／确认→协调交付→专业先接管再 Pull→效果 owner 幂等核对。新变化不能被旧 ACK 清掉。
2. **永久历史：**项目／任务的真实完成证据→专业规则验证→Store 按 parent／CAS／readback 提交→确认后通知→投影效果。不能从 Carrier 或当前持有物猜漏记历史。
3. **易主／夺回：**已确认 episode→专业各自现有退出规则→精确 owner/ref 清理→已确认提交／回执。若旧退出失败，先查错误或合法原生窗口；不能在已夺回的新端点重放只授权给旧外国端点的清理。
4. **网络：**路线 dirty 立即作废严格凭据→共享层拥有可靠采集与交付责任→完整可靠拓扑后正常发布→专业读取。确认空网不是失败；确认负事实独立及时退出。D1 现阶段保护不删，最终必须证明可禁用／移除；D2 由 ODP-01 决定。

## 相比 v2 的实质修正

- ACTIVE 统一，不建立四份总督缓存；同一正常进度 episode 的 Potential 单调。既有合法资产重组 P−1 是独立 episode，不是普通下降示例。
- 学以致用 D、跨学科基础相邻、科研基础设施／学术主持相关输入和商业化 D／工作人口的被动重算方向已进一步批准；仍不把所有 F 行默认开通。
- 巨构工程学**没有奇观历史依赖**：Lua 读玩家当前时代，静态按时代定义 Carrier，原生按当前奇观时代筛选；不需新增 Lua 队列扫描。E 完整历史是工程研习的输入。
- 新增 G30：生产与可选诊断存在实际加载／调用耦合；Probe／Counters 还含生产写屏障、transport bookkeeping和既有GC控制。先提取生产职责再删诊断，不能按名删除或顺便改GC策略。
- Option B 是全面还债；Pre-U5 最小只为保留行为基线，不代表把底层债永久延期。

本轮未使用独立 Carrier & Modifier Footprint Audit 的结论，也不等待该专项。没有新增性能百分比、Carrier数量或内存归因结论。
