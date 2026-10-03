# D0042 — 长期状态 A–G 生命周期收口

Document Maintainer: Codex
Design Authority: User
State: ACCEPTED / DESIGN_SYNC_ONLY
Date: 2026-10-03
Source: 用户本轮长期状态生命周期E/F/G及A–D补充Design Talk附件
Source SHA256: 8e958c274aead5b1491c6543bad0602f704781184cbe36acebc6ad61ad8a6a6e

## 正式来源与接受范围

[Shared D0042](../../../Design/Content/Shared_D0042.json)记录共同语法及Settler确认边界；[Culture](../../../Design/Content/Culture_D0042.json)、[Industry](../../../Design/Content/Industry_D0042.json)、[Commerce](../../../Design/Content/Commerce_D0042.json)保存各自精确合同。[Research D0040](../../../Design/Content/Research_D0040.json)已符合本轮重申，无需重复revision。[Spec](../../../Design/Specialization_v0.1_Design_Spec.md)为入口；阅读页同步，非第二套独立权威。

统一的是分类判断，不是继承结果。A城市历史、B文明历史、C机构关系、D已成立合同、E进行中事务、F配置／派生状态、G单位来源分别处理；记录存在、效果生效、能否增长、配置保留、单位存续、合同成立互不等价。仍仅本地人类单人，AI／Free City不运行专业；不因此把Design写成原Owner专属，不增加多人分账。

| 本轮条款 | 接受与精确落点 |
|---|---|
| A4／A5／B1 | D0040见闻当前Owner自身文明有效过滤、本城实际奇观完成不问当时Owner／Identity／ACTIVE／总督、全国信用归实际完成文明均保持；城市可用可靠历史∪当前可证明本城完成事实，不能凭拥有猜文明完成信用 |
| C1／D1／D2 | 信誉随持续Commerce Identity、易主不重置；资本锁具体S城、同S最早达级再稳定tie；UI锁定字段与预期返还保留；两种合同关键城易主立即异常终止，各自不退款／不走风险失败／发展撤效果释放槽，不转交新Owner |
| E1 | 全生产回合且永久成功提交前是事务；ACTIVE不足／身份退出／重组／易主／生产中断取消，无历史倍率、无成功额度、无半进度；重新合法须完整重做。成功后按A历史 |
| E2／E3／G4 | 已训练考察团在来源降级／身份退出／重组后继续；来源易主中止任务、不写未完成记录、原Owner保留单位、归档绑定失效。免费不限次挂靠任意己方Culture Identity城，无高ACTIVE要求；没有合法城不删单位但不能新开任务。新报告归新挂靠城，旧历史不搬迁 |
| E4 | 既有REALLOCATING P−1／至少5完整T／不自动配置保持；目标易主销毁未完成事务／账本、当前身份及绑定团队，后续按指定snapshot／Claim例外，不恢复半成品、不清所有永久历史 |
| F1 | ACTIVE／Network source、receiver、union／当前来源／carrier／签约资格容量纯派生，按当前事实重算，不把旧snapshot作永久恢复权威 |
| F2–8 | 商业化选择栈及ordinal持久；容量降只LIFO暂停，恢复按前N项自动启用；主动关删除、重开最新。保有身份时Governor／ACTIVE降保留；Identity退出或易主清栈。相同Owner／身份冷加载先恢复选择再派生效果；信誉不同 |
| G1–2 | 已成工业队保留原Owner与使用能力，来源资格／身份／Owner变化不删除；原训练源永久provenance。当前城主自己的存活本城出身队占2槽，旧Owner队不占新Owner容量，原Owner夺回复计；活着撤退不释放，消费／合法移除释放 |
| G3 | 已成重组队不因训练来源变化删除／转交；绑定后生命周期随目标事务，训练source仅来源历史。source易主不取消另一target事务；target易主仍特殊终止 |
| G5 | 来源城易主不等于单位本体捕获／转换；原生行为先调查，不自动授予新Owner专业单位，不建立统一捕获规则 |
| H | 确认前无消费／潜力／投资资产；确认后消费＋receipt＋Potential原子完成。内部窗口属技术原子性／可靠恢复，不是半投资Gameplay，不设计部分退款或跨Owner待决继承 |

资本异常终止不新增保护变动，也不撤回签约时已经完成的保护更新。此规则不决定hidden protection账本本身跨Owner的归属。

## 原审计 T1–T11 对照

依据一次性桌面审计 `Specialization_Long_Term_State_Audit_2026-10-02_225633.md` 的原T编号，点时基线D0039／B152、HEAD223503ec；原文不改、不当当前runtime审计。审计SHA256：`379c9f1a9f31d1748287d4271934b9616460178d3a71490b688ee7364a49e84f`。下表只评价Design问题关闭，不表示实现已适配。

| 项 | 本轮后结论 | 仍需区分 |
|---|---|---|
| T1 科研传统Owner／年龄 | **Design关闭（D0040）**：随城、不分Owner，身份退出暂停、非支持Owner冻结无追补 | 当前运行跨Owner适配不是本轮验收 |
| T2 未结算对话 | **Design关闭（D0042 E1）**：提交前取消无半进度；成功后A历史 | 完整回合与成功提交原子性／事件顺序是技术 |
| T3 考察团source变化／未完成任务 | **Design关闭（E2/E3/G4）**：正常资格变化继续，source易主中止并重挂靠 | 独立归档引用、UI、任务中止／保存技术 |
| T4 文化历史／模板退出与重组 | **具名历史Design关闭（D0040＋E4）**：保留各自城市历史，当前资格重算；毁未完成重组，不毁所有历史 | 新Claim后按具名合同读取；不推导未具名成果或新的潜力补偿，旧收据与当前P技术分离 |
| T5 工业source／单位所有权 | **source转手／夺回容量已关闭（G1/G2）** | 实物单位捕获／转换先查原生；原Owner消失处置仍未定义，不以source规则替代 |
| T6 合同易主／Owner消失 | **关键城市易主已关闭（D0040）**，不随城继承，不在夺回时复活 | 无已确认关键城转移的Owner消失、城市销毁、发展目标非法处置仍未定义 |
| T7 信誉与pity | **信誉关闭（D0040 C1）**；两者不是同一种资产 | hidden protection本身跨Owner保留／重置／分账仍未定义；合同终止不改保护不能回答此题 |
| T8 基本面变化与pity组合 | **仍未定义**，原COM-DETAIL-PITY-REBASE保留 | 不推断max／加法／重置，不重开固定基本面的已定递推 |
| T9 重组队训练source | **source资格／Owner变化已关闭（G3）** | 本体捕获／强制转Owner先技术调查；已接受安全撤回及目标终止不重开 |
| T10 商业化配置与order | **列明生命周期关闭（F2–8）**，LIFO暂停取代删除，身份／易主清栈 | 当前实际效果按当前事实派生；不保存旧carrier作为权威 |
| T11 投资中间窗口 | **Gameplay关闭（H）**，无半完成资产 | 消费／receipt／P一致性与P−1后保留历史如何表达是技术原子性／恢复，不另设跨Ownerpending玩法 |

## 被替代的当前表述

- Culture D0041 `contracts.expedition.source` 的永久训练城**报告绑定**被E3替代；不是把过去已写城市见闻迁到新城。Dialogue未完成生命周期的排除／未决表述关闭。
- Commerce D0040商业化capacity reduction的`cancels`改为保留配置的`suspend`；F6/F7主动身份退出／Owner变化清栈仍与暂停不同。旧非容量变化配置TBD关闭。
- Industry D0040来源城易主及容量总括未决关闭；新Owner独立容量不是全体跨Owner队伍共同占2槽。原单位Owner消失／实物捕获不伪称全定。
- 重组团队训练source退出Commerce的Legacy未决关闭；不得误用target终止清理source变化。
- 原审计Settlerpending Gameplay待决关闭，工程方案须原子化／可靠恢复。
- D0040已替代的原Owner见闻分账、工程实践完成Owner限制及科研年龄Owner未决不恢复；信誉Owner保留、合同关键城终止保持。D0036模板可靠历史保护不削弱。

## 真实剩余与技术问题

**Gameplay仅保留现有未答部分：** hidden protection跨Owner政策及变化基本面组合；城市彻底摧毁／移除的资产／合同处置；未确认关键城转移时原Owner消失；发展目标区域／建筑不再合法的合同处置。专业单位本体直接捕获／转换不统一决定，应先证明原生路径，确有未覆盖玩法再单独Design Talk。

**技术而非Gameplay TBD：** 对话完整回合／提交取消顺序、投资原子性与恢复、稳定city/source引用、当前Owner容量复算、归档重挂靠UI／任务取消／存读档幂等、纯派生重建。不能因它们未实现重新开放已定语义；也不能凭Design声明已有实现。

原有Balance、资本合法池／等级／空池／唯一作用域、X聚合、发展参考态／无解、速度等非生命周期细节按Content原Register保持。本轮不再作全系统审计、不假造每种未来情况的待办。

## 当前 B155 测试与实施边界

D0041的Meaning固定追加／Dialogue与theming不放大合同完全保留。当前P0-L2B共10个JSON选择对象中9个逐对象完全相同；只有完整Dialogue对象新增E1及对应active说明，其target／fallback／precision／quota／sample／accumulation／ownership／duration均不变。B155比较固定追加的原生测试可继续；它不是新E1取消／E3重挂靠或A–G生命周期验收。

本轮不读取全部Mod、不实现、不部署、不调整GC、不评估新生命周期已在B155运行。后续Dialogue正式项目／文化任务／商业配置合同／工业队伍批次，实施前必须按D0042重新核对直接生命周期合同，旧计划的未决或训练source假设不能直接复用。当前仅保持B155原生待验，正式六yield／全城cutover及后续能力未获本轮授权。
