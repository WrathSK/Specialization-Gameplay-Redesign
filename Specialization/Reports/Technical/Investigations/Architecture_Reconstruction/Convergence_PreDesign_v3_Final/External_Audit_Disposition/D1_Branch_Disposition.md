# D1与共享hold：逐分支去向及可执行退出证据

Status: Stable — `v3.1-review` 调查候选；可审阅，不代表审计关闭、正式接受或实施授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅新增本目录 Markdown；不改旧报告、生产、测试、工具、正式规范或状态；不运行验证／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 边界

D1在本议题指“网络证明待确认时保最后实际应用”的跨层实现，不等同某一个Lua模块或开关，也不等同历史同名Discount D1批次。**本轮不删除。O3独占网络D1职责迁移/分支删除；O8只验收，不再安排第二次删除。** 正常冷重建尚无可靠新计划而不写载体是OD-1要求，不因不叫hold就自动证明退役。

| 分支 | 当前职责／精确位置 | 后继owner与去向（计划） | 必须满足的退出证据 |
|---|---|---|---|
| D1-01 pendingProof fanout | Bridge103–111将effect=PENDING并立即notify专业＋UI重采样 | O3网络owner留同步严格失效／采集ticket；普通未准备不再作为专业重算输入，消费者通知改可靠新事实；保UI请求 | dirty后事务立即拒绝；无未准备正向重算；采集/同值恢复交付最终完成 |
| D1-02 proof水位 | Bridge133–143先lastNotifiedProof再pcall EmitDerived | O2首片PU03先补交付责任；O3沿用可靠proof通知，不重复实现 | 失败不吃水位；旧ACK不清新scope；phase0同步派生仍进入当次phase1 |
| D1-03 queuedWork | Bridge146–174/402–429/514–519重入待办；Input121/124伪装pending | O2/O3保必要有界工作单，但明确调度状态，不再无限业务hold；每单cause/ref/ticket/预算 | 同回合第二真变化不丢；无cause闲置零尝试；overflow/失败显式 |
| D1-04 negativeHeld+dormant | Bridge242–261，负投影失败后存dormant，Refresh405再次enqueue | O3新负事实责任：保未完成scope和新证据唤醒，不靠全owner turnRefresh猜恢复；无止境dormant退出 | 真负事实先于unknown sibling；旧carrier权限未知不乱删；受影响责任最终完成或显式错误 |
| D1-05 prune/continuityOnly | Bridge215–235/384–398以旧已证拓扑移除确证loss；其它来源RETAINED | O3保确证退出必要功能，改明确可靠负事实/来源scope，不把旧正向proof伪装新网络 | 先验证本会话已建立input的必要前提；ref/route失效不可复活；混合不交易 |
| D1-06 effectAvailability旁路 | Bridge371–374/619–628允许effects用mixed/continuity，而transaction严格 | O3按用途可靠度表达；未知角色范围可见，独立结果可区分；旧泛AVAILABLE旁路退出 | UNKNOWN role不能变完整READY；交易仍严格，不以已有输出放行 |
| D1-07 Commerce continuation+hold | Commerce183–198、238–289、330/338–356；cold I读取、W混合、capacity/reputation减项 | O3以NET02恢复屏障＋NET03来源W替代旧generic hold/错误白名单；确认本地资格退出保留 | per-domain独立；max→domainFloor→sum；cold未就绪0写，正常完成幂等；DEPTH/worker错误不走0清除 |
| D1-08 Culture retained/negativePlan | CultureNetwork157–165、185–244、249–278/298–314 | O3分初始化/来源W/真实loss；不把UNKNOWN source空集直接写入冷I；旧泛retained分支退出 | union/count、重复文明不叠加；无W输入恢复不会短暂降n；真实loss及时撤下 |
| D1-09 Std wholehold | StandardizationEffects191–205含self新值冻结及old.loaded | O3正常cold屏障保留必要不写入职责，完成后targetmax；warm合法独立self/target更新另按来源可靠度 | 完整F恢复时idempotent，无无终点loaded；不先削I再验证 |
| D1-10 旧冷例外A | StandardizationEffects197/206；任意warning也可触发 | O3在正式后继同步与证据通过后撤旧失效来源特权分支；**不预选severe cold部分支付替代** | OD-1正常cold不被误判为例外；若确有不可避免aggregate取舍，先Owner Packet |
| D1-11 turn级Refresh | NetworkBridge925–930；StdEffects/Commerce/Culture的现有turn入口 | 按[逐原因责任矩阵](Completion_Wake_Responsibility.md)逐项替换；OD-3仅窄已登记工作，非整城audit | 每项必需职责有接班人、完成信号及错误终态；替代前不删 |
| D1-12 未接派生持久层 | NetworkRecoveryModel/Cell/Store仅modinfo入包；Store318–323/1751–1755 Stamp；s9g1–4及selection alarm | O3确认不接线；O7同一账本安全移除无实际职责入口/导入/静态断言；保truehistory、deferred lifecycle、当前SQL IDs | 当前读/写call无生产消费者；既有same-build实际职责逐项核销；无跨版本迁移门禁 |

以上路径均在Mod下。精确源码链接：[Mod/NetworkBridge.lua:103](../../../../../../../Mod/NetworkBridge.lua#L103)、[Mod/NetworkBridge.lua:242](../../../../../../../Mod/NetworkBridge.lua#L242)、[Mod/Commerce.lua:281](../../../../../../../Mod/Commerce.lua#L281)、[Mod/CultureNetwork.lua:230](../../../../../../../Mod/CultureNetwork.lua#L230)、[Mod/StandardizationEffects.lua:191](../../../../../../../Mod/StandardizationEffects.lua#L191)、[Mod/CityProgressionStore.lua:318](../../../../../../../Mod/CityProgressionStore.lua#L318)。未找到生产接线不等于证明历史上从未写过；OD-4让跨版本旧数据不成为本次兼容任务，仍不得无证删运行SQL或实际cleanup。

## 可执行差分：取代不存在的disable臂

1. 固定当前HEAD完整源码为T0，以独立相同初始fixture跑现有真实模块组合；可沿用 [DevelopmentTests/test_refactor_s9e6.py:13](../../../../../../../DevelopmentTests/test_refactor_s9e6.py#L13)–22 的历史字节注入方法。记录baseline整闭包来源，不能只换一个文件忽略依赖变化。
2. 与已审目标切片跑T1，正常cold/route重建/同值/第二次变化/严格交易资格/真实负事实/四专业公式对照。T0已有错误以具名counterexample记录，目标预期来自Owner规范；**不要求缺陷前后完全等价，也不削断言让旧缺陷通过**。
3. T1中逐D1行核查旧分支/导出/导入/声明实际退役或有明确合法保留职责；保留“尚无可靠新计划不写”不是虚假失败。不存在现成全局D1开关，因此不做源码任意comment出不可运行的中间“disabled”产品。
4. 诊断enabled/disabled/真实missing是另一条独立三臂，见P3；不能用它冒充D1三臂。

## 原测试职责处置（不是本轮执行）

| 现有定义／范围 | 今后处理 |
|---|---|
| test_refactor_s4b.py cold_pending81、cold_topology98、std105–115；test_refactor_s9e6.py93 | 原历史基线保留可重跑；正常cold目标改为初始化期间0写、完整后等价，不用旧K-only预期定义Design |
| test_refactor_s6d.py 旧冷例外；test_refactor_s5d4c11.py及其它依赖s4b模块 | 枚举真实import/测试调用后逐断言分类“安全负事实/正常cold/旧A特权”；前两项保持，旧A在正式cutover后以新Owner目标测试替代并记录预期变更 |
| test_refactor_s9g1–4.py/静态产权alarm | O7退出未接适配器时保历史证据、撤当前必要性断言；相应actualproducer/consumer冷恢复测试必须已接管，不靠删测试清绿 |

## D1-E1–E7 修订门禁

E1 可靠正常发布＋正常cold恢复已证；E2 dirty严格资格失效及接管最终完成；E3真负事实/ref/episode边界；E4 self/remote各公式和独立target；E5上述T0/T1可运行对照；E6本表每条有实际去向/删除证据，零空泛“如有可撤”；E7正式后继、必要原生证据及Owner退役批准。severe cold未决不得用(b)长期hold或(a)部分支付先行绕开。未达到的行保留为OPEN，不按目录少文件判断清偿。
