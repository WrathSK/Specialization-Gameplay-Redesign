# D0040 — 长期状态生命周期 A–D 接受与替代记录

Document Maintainer: Codex
Design Authority: User
State: ACCEPTED / DESIGN_SYNC_ONLY
Date: 2026-10-03
Source: 用户确认的 Commerce / Long-Term State Lifecycle A–D Design Talk Handoff
Source SHA256: cde28bddf0c0083022e3ff8704b4c55963811e024725dc38d0ebf51984b6905d

## 接受范围与正式来源

四类是共同生命周期语法，不是统一继承、运行DSL或存档schema。记录归属不由本城／网络／全国效果范围决定；历史存在不等于当前能力生效。

[Shared D0040](../../../Design/Content/Shared_D0040.json)维护语法；[Research](../../../Design/Content/Research_D0040.json)、[Culture](../../../Design/Content/Culture_D0040.json)、[Industry](../../../Design/Content/Industry_D0040.json)、[Commerce](../../../Design/Content/Commerce_D0040.json)维护自身精确合同；[Spec](../../../Design/Specialization_v0.1_Design_Spec.md)引用。这里是接受与取代记录，不创建另一份公式权威。

| 类别／资产 | 本轮确认 |
|---|---|
| A 学术传统 | 年龄随城，无Owner分账；支持Owner且保有科研身份时累积，即使ACTIVE下降；身份退出暂停；非支持Owner冻结，不补算失城回合；当前科研IV利用 |
| A 时代对话 | 成功累计倍率及City×START Game Era额度随城；当前文化III利用，身份退出保留并暂停、不能开始新对话；易主不刷新额度 |
| A 标准化模板 | 随城，不限原Owner；沿D0036可靠历史∪当前合格事实，initialize／restore／reconcile／unavailable严格分开；当前利用按资格 |
| A 文化见闻 | sourceCity×foreignCivilization×category，不再原Owner分账；关于当前Owner自身文明的记录仅退出有效集合，不删历史／额度；独立3/3及并集都用过滤后集合 |
| A 工程实践 | 本城真实奇观完成历史，不限完成Owner／Identity／ACTIVE／总督；工业IV只是当前利用门槛；可并入当前可证明本城完成事实，不能猜历史 |
| B 工程传统 | 实际完成文明拥有Wonder／era信用；同一完成可以另写城市历史；城市易主不转移文明信用 |
| C 商业信誉 | 持续Commerce Identity关系；Owner变化不清零／分账／重置，非支持者冻结使用；ACTIVE下降保留及正常身份年龄增长，效果需IV；Identity退出立即R0 |
| D 资本合同 | 锁具体Commerce城＋S来源城和Owner关系，最高S同级选最早达到、再稳定tie-break；普通资格变化继续，任一关键城易主立即终止，不返本金／到期／风险失败返还，不触发或修改保护 |
| D 发展合同 | 普通资格及容量下降、目标Identity变但目标合法均继续；Commerce城或目标易主立即终止，不退款、撤+50%、立刻释放名额，不转交余期 |

资本异常终止不回滚此前确认时已经发生的hidden protection更新；交接只禁止本次终止再触发／修改保护，不创造逆向补账。S的稳定选择不解决合法池、ACTIVE/Potential或空池。

## 替代与保留

- Research跨Owner `OWNER_POLICY_UNRESOLVED`对学术传统本身关闭；其它科研长期记录未因类比获新规则。
- D0029 CUL-REVIEW-01/03的原Owner见闻键、不供新Owner利用，以及“见闻原Owner／Dialogue随城”二分，被明确替代。原Review冻结；外交／城邦边界、Dialogue随城额度与独立完整集合并集继续有效。
- Industry本城工程实践的“当前完成文明”过滤及“征服奇观不计”被替代；全国工程传统实际完成文明归属保留。D0036模板损坏保护及不追溯不可观察离线建筑保留，触发扩为任何合法enabled Owner重入。
- D0039商业一般Ownership未决中，信誉及两类合同关键城易主部分关闭；公式、首版数值、名称及REALLOCATING目标征服销毁例外不改。
- 此前各冻结Content及D0039 Spec原件不倒改；Military／Harbor及三处未衔接设计边界不改。

## 真正保留的未决与实施前提

本轮没有决定城市彻底摧毁／移除的资产与合同处理，或发展目标区域／建筑变得不合法后的暂停、终止、恢复规则；原Owner消失而尚未确认关键城转移的边界也不新增答案。它们不重新打开已明确的Owner变化政策。

资本候选池、等级口径、空池、同域并发作用域、变化基本面保护组合、发展参考态／无解及其它速度仍按Commerce精确Register保留。Dialogue cap、见闻K_T和其余Balance／Technical状态不变。

E进行中项目／任务、F当前配置／派生状态、G单位／来源绑定不在本轮补齐。原已接受条款（含D0039 REALLOCATING征服例外、来源ACTIVE下降不撤既有考察能力）继续有效；未决部分仍未决，不能把本轮排除理解为撤销此前决定。

## Architecture／运行证据边界

本轮未审计或修改Mod，不宣称新生命周期已实现。旧计划如[文化后续计划入口](../../../Architecture/v2/Culture_Preparation.md)中的P0-M／P0-N中的原Owner见闻分账不得直接复用：对应实施授权前按D0040重新审查。工程实践及科研跨Owner旧合同也需对应批次定域适配，非本次自动实现。

当前B154意义延展的直接能力对象、K、work_pool／domains、Shared四项直接事实与D0038/D0035逐对象相同；仅当前Spec章节与authority pins更新。B154仍待同城同回合C00/C10原生观察，C11/C01/OFF及完整cutover未通过／未授权。运行commit、部署receipt、GC、永久账本、main不变。
