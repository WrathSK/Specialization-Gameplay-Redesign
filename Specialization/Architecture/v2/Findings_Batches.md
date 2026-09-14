# 第一轮调查结论与建议批次

Document Owner: Codex
State: REVIEW_REQUIRED — no refactor authorized by this report
Evidence: STATIC_CONFIRMED only; no new gameplay validation, no source changes

## authority最大的三个问题

1. **永久城市成果缺统一跨owner身份合同**：当前token来自原owner下32条DEV registry，多个City records严格绑定owner/cityID。不是成果会在正常自产城市凭空丢失的证据，但不满足完整Design继承语义；inheritance已隔离，不能在本轮恢复。
2. **Journal/Flow同时是持久真实性门槛**：Flow不是随时可丢弃的单纯cache；读者要求与Journal副本逐字段一致，first完成依赖listener顺序。以后“统一authority”必须含保存迁移/恢复协议，不能只删重复表。
3. **派生缓存合同不统一**：Route有lastverified，Copy/Discount/Dialogue按turn/sample有效性处理空状态；Network revision只覆盖routes不覆盖所有输入；Discount移除集合依赖旧applied。不能盲目把任何现有revision/cache当统一权威。

## dependency最大的三个问题

1. 每个National/ConnectedKinds/RecipientSources query可重新derive全部本玩家网络，多个消费者/城市重复同一输入计算。
2. EffectiveFacts→district/worker查询没有共享一批读结果，多城嵌套玩家全district遍历；晚carrier比较节省写但不节省读。
3. 收益模块间有粗粒度Audit链：Industry→Lv3/Crew，Lv3Effects→Lv4/Copy，UI GPP dirty→多模块。通知的是“有人跑过Audit”而非“明确输入变了”。

## event/dirty最大的三个问题

1. Copy/UI Industry/UI Discount在Publish/Playback直接扫描，Gameplay Discount在Publish全量Audit；包括只读UI请求产生的pulse也可能激活它们。
2. Copy/Discount/GW的样本过期/未就绪与真实失效语义混杂，可能先清再重建；Dialogue+GWA同包分阶段Audit。B069 Route dirty往返已针对性修正，不应重新实施同一个旧修复。
3. direct事件、turn reconciliation和UI dirty重复到达同一消费者；部分定时只读目标查询本身又是全城工作。busy保护同步重入，未抑制后续重复pulse。

## 差异与健康部分

AM01–06详见State_Ownership_Save。Design未修改：通用参与资格/跨owner继承是已批准但延期的实现限制，不重新征求设计决定。实际源合同仍批准后台UI当前routes；UI_SHADOW_ONLY旧字段只属于标签不一致。

优先保留：最终Boost量化/Copy半点/Dialogue分类等纯函数；投资确认重验和有上限receipt；Crew当前consume/AddProgress顺序；Standardization一次补录+事件增量；B069 Route相同快照抑制与单inflight；Dialogue idle不scan+有限重传；固定Performance Counters。保留不等于所有周边调度不需优化。

## 按依赖排序的候选批次（均仅develop）

| Batch | 先做原因 / 范围 | 上下游影响 | 风险 | 独立验证与未来实机需要 | Milestone适合性 |
|---|---|---|---|---|---|
| A — 事实版本与发布合同 | 明确route validity/source identity/ACTIVE/capital/样本各revision，确保明确撤销发布一次；保留B069来源/dirty保护；先不要直接缓存旧revision | NetworkBridge / EffectiveFacts与下游查询协议 | 中；漏某输入会把正确即时计算变成stale | 本地事件模型：同输入no-op，源升级/撤销、首都/身份变化、route增删/unknown；之后最小实机确认事件传达，需要用户另行同意develop切包 | 是：version contract + tests，可恢复 |
| B — Shared Network derived state | 在A覆盖输入后每revision derive一次，National/RecipientSources/ConnectedKinds消费同批视图 | Boost/折扣/工业copy/CommerceIII；CommerceIV保持direct routes语义 | 中；recipient/source/ACTIVE区分不可变 | 新旧纯模型全矩阵比对、query次数counter；未来1组route+Governor短测 | 是：共享网络读里程碑 |
| C — UI样本生命周期与ACK | Copy/Discount先处理暂未就绪vs确认失效、单flight、bounded retry；Dialogue/GWA同包应用顺序；独立小子批次不要一起重写 | UI采样→receiver→carrier更新；依赖A版本，使用B网络视图 | 中高；缓存stale、错留收益风险；必须保留真正撤销 | 本地延迟ACK/重复包/错turn/坏payload/真移除，不动数值；未来少量新增实机生命周期测试 | 子批次各成milestone，不一大包 |
| D — Direct dirty consumers | 去掉泛化Audit扇出与Publish即全scan；先网络consumer再worker/building；保留有限reconciliation | 效果模块/启动/目标UI；按城市定位 | 中；遗漏有效事件可能迟刷新 | 每项输入变更对照旧输出、无关单位零writes/有限scans；未来代表性专家/建筑/网络短测 | 是，按dependency切小批 |
| E — 保存/生命周期专项（可先研究，实施靠后） | Crew receipt无界/历史city caches/32-city/Journal-Flow迁移须独立合同；不借性能缓存实施永久数据迁移 | save compatibility、幂等凭据、未来inheritance | 高；不可逆操作/旧档数据 | 离线旧schema/中断stage/reload/dedupe模型；部署前必须用户明确恢复与实机测试计划 | 单独save-contract milestone，不并入当前stable |

这里A不是重新编写商路provider；B不是把old route revision直接拿来cache；C不能以长期保留坏路线/坏资格掩盖性能；D不改Gameplay设计与数值。E的风险登记不代表用户应暂停现有长局。

## 本轮交付 / milestone gate

Ownership/Persistence、Dependency/Bridge、Event/Dirty地图与源码索引齐备；没有未实现的代码改动混入。文档一致性、引用、事件名称及源码不变检查记录在[Validation](Validation.md)。只有提交后develop clean并push同步才报告 **Architecture v2 Investigation Milestone Candidate**。不自动创建tag；若用户需要标记，可考虑 `arch-v2-investigation-01`，本轮不要求做此决定。

本轮不新增用户实机测试，用户继续stable B069.96。下一步等用户审阅上述候选范围，不能以这份TARGET表作为已经批准实施的任务列表。
