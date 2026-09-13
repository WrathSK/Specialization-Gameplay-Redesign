# D0009架构同步与实现差距

Document Owner: Codex
Design Spec Synced Through: D0009
Design Spec SHA256: 07920f9e87bd7cb08089bdb5bfd1aa6f74ed6483a02fb6167db61cecd76c31d8
Architecture Revision: A0059
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-026 / modinfo33（本轮不变，网络仍为D0008实现）
Evidence: STATIC_CONFIRMED（文件hash、D0008→D0009全文diff及现有代码静态核对，不等于引擎通过）

## 当前设计与适配契约

WHAT唯一权威为[Accepted Spec](../../Design/Specialization_v0.1_Design_Spec.md)，本报告只记录HOW与差距。差异集中SCOPE-001、COM-004至008、NET-001至003、NET-RC-002、COMPAT-002；其它专业和Future成熟度未变。

- NET-001/002：完成direct source集合后，先为每中心的每个有效source加入本中心recipient资格（包括首都天然source），再合并distribution与其它合法资格。同一城市按身份去重。
- NET-003：保留directSources和receivedNetworks两个独立集合，禁止从recipient反推direct source。接收资格保留原因，如DIRECT_SOURCE、CAPITAL_SELF_CONNECTION、DISTRIBUTION_ROUTE；同类多原因并存，撤销一个原因不删除其它有效原因。中心接收与可转发来源必须分别展示。
- NET-RC-002：强度计算仍消费去重recipient集合；L仍最高有效ACTIVE，k独立、sqrt不变。更改的是进入N的资格，不是公式。
- COM-004至008：计划独立Convergence计算模块，输入每中心有效direct source及来源本地产出证据，输出每yield所选source、basis、未量化amount和有效性。按eligible yield选最高，不能复用NetworkStrength按ACTIVE选源的结果。无有效来源时输出零；依据读不到时明确UNKNOWN，不能以零或最终城市yield冒充准确值。
- COM-006/COMPAT-002：单独的LocalSourceYieldBasis接口必须说明本地自产与跨城Specialization输入的归属。可研究对本Mod跨城输入逐项记账与原生yield分解，但“最终yield减去发放的名义值”未证明足够：城市百分比可能放大这些输入，采样时序也可能含上一轮输出。必须验证被排除输入及其后续影响，不假定简单相减等价。不能用煤电厂/大酒店的区域Actual基数替代城市本地产出。
- 更新顺序计划：获取同一轮来源资格和可验证basis→分别选源→计算新输出→替换旧输出。禁止边写入边读其它source造成回馈；来源失效、ACTIVE离开IV、资格消失均需撤销。具体引擎承载、倍率影响、小数/取整、同回合刷新尚待调查，无默认fallback。

## 已存在的旧假设（本轮保留源码，明确不符合D0009）

| 文件/范围 | 发现 | 后续适配 |
|---|---|---|
| 运行NetworkBridge.lua derive | 只有distribution加入recipient，首都direct self-connection不加入recipient | 加direct接收原因及去重，不修改路线事实 |
| DevelopmentTests/NetworkState.lua | 首都不加recipient；freeSelfReceiver/COMMERCE_IV_SELF旧能力分支 | direct自然接收替代旧IV专属分支；Convergence独立实现 |
| test_d0005_models.py、test_network_bridge.py及B026 wrapper | 旧首都/中心N期望与D0009不同 | 另行适配后跑新版测试，不用旧PASS证明D0009 |
| IndustryNetwork / NetworkStrength消费者 | 消费recipient集合，旧上游漏direct中心 | 验证集合变化传导；不更改工业来源合并或sqrt规则 |
| Commerce IV Convergence | 当前没有正式实现 | basis可行性优先，不把已确定玩法重新列为未决 |

## B026证据解释已被新版设计取代

原八图和结果冻结，仍证明旧实现的背景传输、连接、分发、正常读档路径。它们不是D0009符合性PASS，也不追改为当时软件错误。

按相同路线情景应用新规则：
- 图1首都已接科研/文化：两类N至少包含首都，不应继续显示0/0。
- 图2至5首都和纽约均接收科研/文化：这两个城市构成两类recipient；多科研源不额外加城。
- 图6（仅科研首都→纽约、文化城→纽约）：科研N=2（首都、纽约），文化N=1（纽约）；纽约两类接收均YES。
- 图7/8再加入纽约→阿伯丁：科研N=3（首都、纽约、阿伯丁），文化N=2（纽约、阿伯丁）。
图1全国3条路线而用户只描述2条相关入站，完整未知路线不推断。以上期望依明确拓扑，不是新实机结果。

## 工作顺序与验证边界

用户要求将前轮诊断可读性/断路撤销小批次放入待办，待当前问题解决后恢复。本轮只同步，没有运行测试、部署、游戏操作或新增USER_GAME_TEST_PASS。

1. 当前下一重点：D0009 direct自然接收适配准备，与Convergence本地产出basis可行性调查。
2. 在本地完成新版首都/普通中心direct接收、direct+distribution去重、receive-only不可递归、资格撤销保留及重新计N的模拟后，再提供必要的新实机小批次。
3. 汇聚后续模拟需包括按yield而非ACTIVE选源、三yield独立、无源归零、最高源移除回退、排除输入及环路、重载重算；无引擎basis证据前不应用收益。
4. 旧报告可读性和撤销测试延后，B010继续暂停。没有新用户测试或设计决定；如果调查证明原basis无法等价取得，再报告IMPLEMENTATION_LIMITATION / DESIGN_DECISION_REQUIRED，不静默换定义。
