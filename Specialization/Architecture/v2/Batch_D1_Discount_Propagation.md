# Architecture v2 D1 — Discount event / scan propagation

Document Owner: Codex
Build: develop B074.101 / modinfo101
Source baseline: C1 B073.100 / affe4c8 (user accepted)
State: LOCAL_SIMULATION_PASS; awaiting review; NOT DEPLOYED
Design: D0025 unchanged
Mainline: A → B → C1 → D1 → C2 → D2 → E

## 用户摘要

本批将无关通知挡在折扣扫描之前，并将一次折扣更新的全国Network确认由每城一次改为全批一次。常规有效输入的最终载体结果与B073一致；C1请求编号、pending、ACK、超时和重试预算未改。两城10,000组通用通知没有新增完整Audit、Network确认、UI资格扫描或建筑写入。本地测试不是实机通过；55GB内存原因仍UNKNOWN。不部署，不要求现在切换测试。建议审阅后进入C2。

## 原入口审计 / STATIC_CONFIRMED

STATIC_CONFIRMED指代码证据，不等于实机事件频率归因。

| 入口（B073） | 原职责/成本 | D1 |
|---|---|---|
| Gameplay GameCoreEventPublishComplete | 无条件d.Audit，扫描所有测试玩家/城市 | 保留回调，只排空已有dirty；clean在init/Players循环前返回 |
| Gameplay PlayerTurnActivated | 每通知Audit全部玩家 | 只处理该测试玩家，每game turn最多一次兜底（重复activation抑制） |
| GovernorAssigned/Established/Promoted/Changed | Discount直接Audit，另有NetworkBridge Rebuild | 删除Discount重复监听；通过上游完整Network input publication传播 |
| NetworkBridge.notify → Discount.Audit(publication) | 上游事实真正变化时通知；旧接收端仍扫全部玩家 | publication只标对应玩家；重复epoch/inputVersion/validity不新增工作 |
| LoadScreenClose / EnsureReady(INIT) | 初始化/恢复 | 保留，重置D1状态并显式mark |
| CityTransfered | 已有非本玩家载体清理及Audit | 保留原清理，显式owner dirty；不恢复继承模块 |
| Receive pre-Audit / accepted sample post-Audit | 每个新请求前后可能完整Audit | 前段只排空dirty；changed sample后apply-only，重用现有plan，无Network Capture |
| UI PublishComplete / PlaybackComplete / PlayerTurnActivated | C1 pending时不发送；非pending仍扫描CanStartCommand | 保留协议调度；相同generation/plan revision/turn/permission revision在native扫描前停止 |
| UI SystemUpdateUI | pending/初始化/epoch恢复 | C1条件和ACK/超时逻辑保留；新增扫描门禁同样适用 |
| UI SetUpdate | 只加标量时钟 | 不变：不扫描、不发送、不记录日志 |
| Read discounts / Describe | 只读当前报告（dispatch会经过既有Gameplay request） | 不变：不会mark dirty或强制审计 |

没有Gameplay Discount Playback监听，也没有Discount每帧Gameplay timer。其它模块普通Audit不会主动调用Discount；NetworkBridge的正式变更发布会调用它。Standardization自身Publish→Flush仍是原有pending知识处理，不在本轮改写。

实机18,602 checks /317秒约59/s，和旧通用Publish全量工作路径相符；旧counter没有逐触发原因分桶，不能断言其中精确多少来自Publish、UI回应或其它事件，也不能归因HD。无HD也有高频Audit的历史证据保持。audit_standard现在统计实际处理的玩家批次；旧值统计每次函数入口，跨版本不能直接等口径比较。

## Dirty ownership与独立输入

- Network source/ACTIVE/Identity/qualification/Capital/Trade Center/current reference：沿A/B完整input发布，Discount不再重复监听Governor。Network本身的listeners/其它consumer不动。
- Templates：Standardization成功验证Property写入后MarkDirty(owner,'template')；普通Discover/未变化账本不发布。没有改变知识记录、初始化或事件式增量学习规则。
- Building/category/prerequisite：原生BuildingAddedToMap及可用时BuildingRemovedFromMap标该玩家。排除BUILDING_SPC_内部建筑，避免自己的载体写入回流。
- Purchase eligibility：UI保持原Gold CanStartCommand路径；research/civic/government/policy/production/district与普通building变化更新独立permission revision，随后C1传输。Network version从来不是全部Discount输入。
- Accepted sample：仅值变化才mark sample；只应用已经确认plan × sample，不重读Network/source/ledger。
- Direct marks可以合并；busy期间新mark留到下一次publish。批次自身Network确认同步产生的那份network publication已被本批包含，不再额外重跑。没有无限循环drain。

Native signature先例：本地原版ProductionPanel使用相同CanStartCommand参数；原版PlotInfo/CityBannerManager的DistrictRemovedFromMap首参playerID；已安装GovernmentScreen/WorldTracker/OverflowBugFix的policy/research/civic/production首参playerID；HD/既有Standardization的BuildingAddedToMap为x,y,bid,pid。BuildingRemovedFromMap的可用性/完整签名缺少同等原生先例，按条件注册；未覆盖、未触发或HD私有购买条件变化靠下述回合兜底。不假装已经验证所有引擎事件。

## Bounded reconciliation / validity

- 每测试玩家每turn最多一次完整折扣兜底；UI资格以turn key最多一次正常新采样（pending重试仍遵守C1最多3次）。不新增秒级timer或持续poll扫描。
- 漏掉direct事件时最迟下一次该玩家turn核对恢复；同回合mod私有条件无已知事件可能延迟至此，须作为实机兼容性边界保留。
- 正常pure publish/Playback只是排队/ACK机会，不能制造dirty。10,000重复activation同turn仍有界。
- 暂时Network/ACTIVE/ledger读取失败沿C1保留同ref旧plan/permission及收益；不会猜confirmed empty。confirmed route/source/permission失效仍撤销。
- 批次初始化异常不在每次publish重试；等待新direct事件或回合兜底，重复同错误不反复print。C1传输retry、pending、seq、epoch、响应验证不改变。
- reload重置dirty/lastTurn/lastNetwork；没有保存新的Property或迁移。

## Shared batch contract / C²移除

NetworkBridge.DiscountBatch(pid)调用一次既有currentView（完整A确认+B key验证），返回Input metadata与Industry recipient-source映射的深拷贝。owner仍是NetworkBridge；只在同步Discount Audit局部使用，不跨批次保存，不允许修改私有shared view。

完整匹配条件仍是contract/epoch/player/inputVersion/derivedFor/signature/VERIFIED；不使用route revision替代。其它公开Network query完全不改。若Network正在正式publication内，既有reentrancy保护允许读取刚发布视图，不重做Capture。

每工业source的EffectiveFacts与ReadLedger结果（包括失败）在此批次最多读取一次，逐recipient仅合并集合/max，不重复全国Capture。source knowledge/permission未塞入Network cache。样本apply-only无全国Capture。实际已连接source仍有账本验证成本；集合交集/合并复杂度取决于source/recipient边数，不宣称所有工作总量永远严格O(C)。

## 本地工作量 / LOCAL_SIMULATION_PASS

LOCAL_SIMULATION_PASS是实际Lua模块+模拟引擎事件通过，不等于Civ VI实机通过。

使用实际NetworkBridge、NetworkInput、Discount及fixed counters；无工业来源的对照用于隔离全国Capture成本。每行是一次必要完整检查，不是逐帧：

| 城市C | 旧facts | D1 facts | 旧Network queries | D1 queries | 旧city_scan | D1 city_scan | D1 processed |
|---:|---:|---:|---:|---:|---:|---:|---:|
|1|1|1|1|1|3|3|1|
|2|4|2|2|1|8|6|2|
|4|16|4|4|1|24|12|4|
|8|64|8|8|1|80|24|8|

另测8城全部接入一个工业source：完整检查8次全国facts +1次source facts +1次真实ReadLedger内部facts=10，账本读取1，Network query1。原source验证契约未削弱。

- 两城10,000组Publish+Playback+SystemUpdateUI+普通unit通知+其它clean Audit：新增完整Audit0、Network确认0、UI资格扫描0、Building write0。
- 同turn10,000 activation：reconcile仅1；无direct通知的ACTIVE变化下一turn恢复正确20%载体。
- 39组两source/两template-group全城载体map与B073逐值一致（max、union、permission、移除、qualification、reference）；真正Network发布ACTIVE3→4→0→4、temporary UNKNOWN、确认route消失另测。
- actual Standardization初始化/增量learned写入驱动刷新；重复Discover不dirty；普通building更新刷新，内部carrier回调无反馈。
- C1全部历史Lua lifecycle断言重跑（显式mock fact mutation改为D1 direct mark），20万pending通知仅INIT+sample两请求；超时、stale、partial、重复、load、确认撤销仍通过。
- A/B/B069历史网络矩阵168+24及9组transient保持。历史B中的旧Discount计数断言仍使用B073 consumer，D1性能断言独立，不偷偷改旧期望。历史测试文件未修改。
- 全Lua语法、manifest引用通过；没有game/DB/runtime writes。

入口：`DevelopmentTests/test_arch_v2_d1.py`，需要Lupa lua55。当前本机示例：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_arch_v2_d1.py`。这些路径是外部本地测试依赖，不进入运行包。

## Counters

新增fixed keys：discount_dirty_mark、discount_direct_refresh、discount_reconcile、discount_skipped_clean、discount_fact_capture、discount_city_processed、discount_ui_scan。dirty_mark按首次合并reason计；fact_capture计批次Network确认尝试（已在publication内时可能不实际Capture），真实facts/city_scan用于判断实际读取。skipped_clean包含Gameplay/UI早停；direct_refresh包括sample-only。C1attempt/send/pending等口径保留。无逐事件日志、无Lua文件日志、无无界历史。

## 未完成 / 下一步

C2：其它Copy/Industry/GreatWork/Commerce样本生命周期；D2：其它consumer generic listeners、上游Network facts重复Capture、跨模块dirty传播；E：保存生命周期后置。本批不更改这些模块，不优化HD，不做memory根因判断。55GB仍是独立runtime incident，性能改善不等于内存已修复。

D1本地里程碑候选；建议审阅后授权C2。不自动tag/promotion。main与当前运行包不改，不部署；暂无用户立即实机测试任务。条件事件覆盖与实机CPU/内存趋势留给以后获准短测。
