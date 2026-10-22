# AV2-B — Shared Network Derived State

Document Owner: Codex
State: IMPLEMENTED_IN_DEVELOP / LOCAL_SIMULATION_PASS / USER_REVIEW_PENDING
Develop build: P0-B-071.98 / modinfo98
Base: accepted Batch A, d1ac666 (B070.97)
Stable: B069.96 / modinfo96 — unchanged, NOT DEPLOYED
Design: D0025 unchanged

## 用户摘要与范围

只实现Batch B：同一已确认完整Network输入，每玩家派生一次正式视图，查询共享结果。真实Discount Audit四城市回归由旧版4次派生降到已缓存时0次；首次接受完整输入1次。没有修改UI轮询、样本生命周期、consumer listener、存档或玩法。

今天stable事件提供了重复计算的实机证据：同一59T两份报告中，Discount Audit +3917、derive +15668，期间商路扫描和本Mod直接Building/Property写计数不增；用户报告后台无操作时内存继续增长，系统取样到55.2G。它支持优先处理重复计算，但不证明55GB来源。Batch B不声称解决该内存异常，也不以本地derive减少代替独立实机内存趋势验证。原件仍在外部截图收件箱，本批不移动或改写。

LOCAL_SIMULATION_PASS是实际Lua模块在mock引擎内通过；STATIC_CONFIRMED是源码/文件边界证据，都不是Civ VI实机PASS。本轮不自动切包，不新增立即实机操作。

## 1. Cache owner / key / lifetime

唯一owner为NetworkBridge.Start闭包内私有views[player]。每玩家至多一份当前视图，不以revision累计历史；启动新epoch创建新表，CONFIRMED_INVALID清掉视图，VERIFIED新输入替换旧视图。无Property/存档写入，无新事件listener。

严格匹配：contract=1、epoch、player、inputVersion、validity=VERIFIED、derivedFor=inputVersion，并检查Bridge的derivedFor及完整signature一致。routeRevision不是cache key。

查询先走Batch A Refresh/Verified，再读取匹配视图。NEEDS_REVALIDATION是availability，保留此前VERIFIED输入及其视图；初始UNKNOWN没有空视图，确认失效拒绝正式查询。读取失败不造零值。新输入被接受前先构建视图，成功后连同版本安装，再notify消费者；同步重入查询读取已安装视图而不再derive。

若完整版本元数据不匹配，查询明确失败，不偷偷为同一版本反复重建。正常路径由publication保证视图存在。公开查询返回值副本，旧bucket sources/centers/recipients保留独立诊断投影，调用者改返回表不会破坏private cache。

## 2. Derived view

| 字段 | 内容 |
|---|---|
| sources | source city ID → specialization |
| centers | Trade Center ID → direct source set（含既有首都自身规则） |
| recipients | specialization → recipient city → source set；保持来源并集/去重与分发规则 |
| connected | center → 已直连network kinds |
| national | Research/Culture的N、max ACTIVE L、source→ACTIVE与recipient去重集 |
| contract/epoch/player/inputVersion/derivedFor/validity/signature | 正式输入与派生结果的对应关系 |

National不重新遍历来源计算L/N；ConnectedKinds复制对应城市的kind set；RecipientSources从该城市已有来源集合生成排序数组；诊断Read也使用共享视图，仅额外格式化名字和路线文字。返回小集合副本不是完整Network derive。

不包含：Copy实际yield、购买资格、永久标准化模板、Commerce IV城市产出、Great Work样本、下游最终收益。Research/Culture配置属于Batch A signature，即使此视图本身只输出L/N，配置变化仍产生新输入/一次派生。没有修改系数、公式或最终量化。

## 3. Batch A输入覆盖与边界

NetworkInput.lua字节未改。既有完整签名覆盖route/current端点引用、Identity/qualification、Potential、ACTIVE、Trade Center身份、Capital、城市current reference、kResearch/kCulture。未发现本轮共享拓扑/National输出缺少的必要输入。

不能将此结论扩展为所有消费者最终收益已具备完整缓存合同。未来效率配置或拓扑规则若引入新输入，仍须扩展NetworkInput；不能只改消费者后继续复用旧key。

## 4. 固定Performance Counters

新增6个固定key，总40项；保留current/total/previous/peak，无payload/history或逐事件日志：

- derive_requested：新输入构建尝试与共享查询入口次数。被拒绝的UNKNOWN查询也可计请求，不保证等于hit+miss。
- derive_executed：实际运行完整拓扑derive；旧derive计数保持同义，便于跨版本比较。
- derived_cache_hit：通过完整key验证的共享读取。
- derived_cache_miss：新输入需要构建或发现视图key不匹配；不是商路读取失败。
- input_version_change：成功发布新完整输入/正式撤销，兼容旧fact_change。
- derived_invalidation：已有视图因新输入替换或CONFIRMED_INVALID被废弃。首次初始化无旧视图不计。

事实Capture、端点核验、查询返回副本、consumer自己的Audit仍消耗时间；derive=0不表示全部工作=0。

## 5. 本地验证

入口：DevelopmentTests/test_arch_v2_batch_b.py；复用现有Lupa lua55。历史Batch A/B069脚本保持原样，本轮runner只在内存适配manifest98断言。

1. 保留全部Batch A A–I与B069行为回归：同输入no-op、ACTIVE升降、资格丢失恢复、capital/center、route增删、UNKNOWN保留、确认撤销、顺序/旧epoch/重入、固定Counters跨10000回合。
2. 168组有效状态三方逐值比较：B069旧Bridge（79281ff）、Batch A（d1ac666）、Batch B。覆盖7类route图×4档ACTIVE×3种capital×Commerce/NONE；比较National完整N/L/source/recipient、每城connected kinds与3类recipient source数组。多源、多中心、直连、分发、同城对重复route、空集合、路线替换均在矩阵中。
3. 9步Batch A/B未知状态及metadata一致性：资格失效恢复、临时source UNKNOWN、待核对期间capital变化、k配置、reference替换和空全集。B069不作为UNKNOWN语义oracle，避免把Batch A已修正合同倒退。
4. 真实StandardizationDiscount模块四城市：首次完整输入在Audit中成功接受，cold=1 derive/1 miss/4 hits；warm Audit=0 derive/4 hits；连续102次顶层Audit累计1 derive/408 hits。初始化notify有busy skip，不构成重复派生。无Building Create/Remove或Property写。
5. 同一真实Discount模块与旧Bridge对照：B069=4、Batch A=4、Batch B=0次warm derive。
6. 返回值与兼容投影修改隔离、不同player同数值inputVersion、metadata错配拒绝、配置失效、确认撤销/重建、通知内查询复用、load新epoch。
7. Lua编译及manifest引用随B069回归；部署工具只在临时目录安全回归，无实际部署。源码边界检查：NetworkInput、所有consumer及UI、SQL、Design均未改；main/live Mod逐文件核对保持一致。

## 6. 保留给C/D的工作

- Batch C：Copy/Discount/Dialogue sample过期/ACK、后台采样调度、暂空恢复；本轮不更改。
- Batch D：重复consumer监听和直接dirty传播；查询前Capture仍可全城扫描，EffectiveFacts仍有读取/复制成本，Discount仍逐城检查。共享派生只消除重复topology/National计算。
- UI后台轮询、隐藏控件更新、内存保留/原生分配归因另行授权；不借本批顺手修复。
- Batch E/save/ownership、carrier、compatibility、balance均未推进。

## 7. Milestone / gate

建议 Architecture v2 Batch B Milestone Candidate：arch-v2-batch-b-b071.98。完成coherent commit并push develop；不自动打tag，不promotion/main merge，不部署。用户审阅后再决定是否授权临时develop短测及恢复stable；任何内存改善结论必须独立验证。
