# P09b — 跨Context事实发布与消费者边界

Audit IA20261007 / W04；2026-10-07。审查baseline `8e2dcb7`，Mod与W02/P06a一致。**Audit-only；本报告不是正式Architecture合同，不授权修复。** P09b逻辑slice覆盖完成，不表示整个Network/所有消费者或原生效果通过。

## 回答的问题

完整输入何时成为已接受事实，谁可以改写它，ACK与消费者更新有什么关系；新增消费者会不会把局部异常扩大成互相阻断。沿W02已有传播图核证，没有重新做全Mod扫描或每能力save/load验收。

结论：两个事实owner都有epoch/引用/UNKNOWN保护，正常查询也有副本隔离；无需重写所有桥接。但是GW消费者依靠串联回调，异常隔离弱于Network；Network的公开控制bucket仍暴露实际accepted input。这两处应在更多消费者依赖它们前明确边界。ACK已明确是处理／传输事实，不能要求它同时证明收益成功，也不能为了修消费者失败而反复重新采集全部原生事实。

## 实际传播与ownership map

以下源码路径相对于仓库根`Mod/`；数字为本baseline行号。

| 路径 | owner／持有内容 | 接受与通知次序 | 失效、退出和失败边界 |
|---|---|---|---|
| UI Great Works producer | `UI/DialogueRefresh`拥有slot cache、dirty cities、单pending、sent key；不拥有Gameplay权威 | 31–46核epoch/generation/inputRevision；55–84采完整支持玩家范围、dirty城市才重读slots；87–93发同一DIALOGUE_SAMPLE包 | generic pulse只drain；同包最多2次重发104–115；Shutdown159–163解绑并清session；回合/真实事件可产生新样本 |
| GreatWorkFacts | 闭包cities/index/signature保存当前确认事实；对外Read复制、Summary/ Domestic另构造值 | 90–95先验证epoch/seq，再推进processed ack；98–141验证完整引用/作品范围后安装candidate或复用；159–169随后通知消费者 | 坏current包使UNKNOWN；旧epoch/重复包不污染新事实；同ref未知保留旧确认值；Reset/Exit/Return不恢复永久收益快照 |
| GW consumers | Aesthetic/Meaning分别拥有本模块派生配置、错误和精确carrier出口 | Aesthetic231–246先赋单回调；Meaning233–239保存previous并先调用它；Facts165只有整条链的一次pcall | 通常的单城reconcile错误在各自Audit捕获；向外逃逸的前置异常会跳过后置consumer。已有事件/回合fallback不等于本次通知必达 |
| Gameplay样本分发 | `Gameplay`260–278接同一请求，分别调用Facts和旧Dialogue；不成为第三个事实库 | Facts/Dialogue各pcall；272调用自动Meaning.CollectionConfirmed；两端实际接受后才ConfirmSamplePair，旧probe另有确认入口 | Facts失败不阻断Dialogue；processed双ACK仅供UI结束等待；pair也不等于native效果结算 |
| UI routes producer/sender | BackgroundRoutes owns当前完整snapshot；Sender拥有单flight、seq、failedTurn/epoch | Sender19–24核seq/fingerprint；27–42只发送完整/current样本；Gameplay Receive201先推进processed seq，234留最多一份candidate | epoch变更清flight；同turn失败抑制重复发送；超128或16384字节直接return，见容量边界 |
| Network accepted input | NetworkBridge唯一接受owner；实际bucket在`shared.NetworkBridge.players`公开；input/routes/control与private view不同 | Receive校验全集；Refresh139–170 Capture当前逻辑事实→buildView→安装routes/input/view/version→notify | 同refUNKNOWN沿用最近输入，真实端点/trader/战争/引用失效有独立withdraw；alias缺口见F01 |
| Network派生视图／消费者 | `views[player]`闭包私有；Input值副本、Current查询副本或新数组；debug sources/centers/recipients另复制 | notify56–64逐consumer pcall，后续consumer不受前一个抛错阻断；Current*不重新Capture | consumer异常不回滚accepted事实；后续既有事件恢复。不是全桥收益事务；错误状态目前仅最近字符串 |

公共成本沿用W02，未新增原生耗时结论：producer一次dirty flush仍枚举支持玩家城市并序列化完整包；Gameplay验证完整范围和native references；“相同输入不发布”不等于不验证或不构造对象。Network Refresh仍Capture当前城市事实，Current*读取已安装view。不能把ACK等待或同步busy当成可丢弃有序ownership转换的许可。

### Store返回前／后的边界（P06a-Q02补核）

`CityProgressionStore:581–584`在ACTIVE/current提交**之前**执行return回调，目的是使样本/报价失效。NetworkBridge445–446撤旧网络，GreatWorkFacts255 Reset；Standardization169–170只排reconcile，GameCoreEventPublishComplete194或其它正常Flush在提交后读账本。Aesthetic253/Meaning246立即Audit，此时EffectiveFacts仍不能读取HELD记录，另有CityTransfered和回合监听补算。

实际启动顺序Store在Gameplay655–656，业务模块随后注册；当前已核路径未证明漏恢复。下一模块不能假设RegisterReturn意味着“新的ACTIVE已经可读”，也不能在任意return callback中恢复旧收益。保留LOW / FIX_BEFORE_NEXT_PROFESSION的接口阶段说明建议；没有把所有回调改成事务或要求用户重跑夺回。

## 已有finding的强化证据：IA-P13a-F04

**MEDIUM / FIX_BEFORE_NEXT_PROFESSION**，保持既有ID与时机，不计为新的重复finding。新增STATIC + LOCAL_STRUCTURAL_REPRODUCTION，精确回答“前置异常后，同值输入能否补发”。

真实Facts、真实UI producer/sender、实际Gameplay DIALOGUE_SAMPLE分支、逐字Aesthetic/Meaning注册及实际Meaning.CollectionConfirmed参与复现。效果Audit与旧Dialogue ACK是明确stub；只注入一次会向外逃逸的Aesthetic异常。

| 步骤 | Facts/ACK | UI／重发 | Aesthetic / Meaning调用 |
|---|---|---|---|
| 首次采样，Aesthetic抛错 | VERIFIED，ACK1；事实已经接受 | IDLE，结束等待 | 1 / 0 |
| 移除异常，12次idle pulse，再直接送同内容新seq | ACK2；同一事实仍接受 | 无重发；retries=0 | 1 / 0 |
| 当前馆藏真实变化的新包 | ACK3；新摘要 | 正常一次发送 | 2 / 1；consumerError清除 |

`GreatWorkFacts:126–128,160–167`不为同一事实重发通知；`CultureMeaning:174–177`已ready时直接true，不是丢失通知重试。Mod内consumerError没有sender或恢复消费者。**这不是永久失效证据**：新事实、相关事件或玩家回合Audit仍可能恢复。一般AE reconcile错误在149被捕获，不会逃出链；本次没有证明真实异常概率、native投递时序或实际少发收益。

候选边界：明确注册现有消费者、逐消费者异常隔离和错误归属；若确需补发，只保留有界未完成consumer/城市范围，不能把收益失败转成采集ACK失败或无限重试。无需通用事件总线。现在主要涉及Facts通知与两处注册；继续链式包装会让更多消费者依赖启动顺序、前置成功及恢复fallback，未来迁移与回归面增加。

未来验证：前置逃逸失败后其他消费者仍执行；失败责任可见；同值新seq不进行不必要全量采集；真实变化和跨城移作保留；bounded busy/恢复策略及新epoch退出；现有normal错误隔离不回归。应测通知协议，不机械重复每个能力的冷加载仪式。

## 新confirmed finding：IA-P09b-F01 — accepted input的公开别名

**MEDIUM / FIX_BEFORE_NEXT_PROFESSION**。STATIC + LOCAL_STRUCTURAL_REPRODUCTION确认接口边界；**没有找到当前业务caller主动改写它**，不称现实状态污染或安全攻击漏洞。

`Gameplay:8–9`将shared放在ExposedMembers；`NetworkBridge:5,45–47,68,165`通过players公开真实bucket/input/routes。private views和Current查询副本确实隔离，但`NetworkInput:31–34`在当前getter UNKNOWN时直接使用`b.input.cities`作为最近已确认来源。

实际Lua反例：合法接受ACTIVE3；刻意通过公开表把accepted input改4，原生fixture仍3。修改当时private CurrentNational仍3；随后仅使原生事实读取UNKNOWN并Refresh，派生级别变4、availability=NEEDS_REVALIDATION、inputVersion1→2。恢复getter后回3，version2→3。数据不是由原生ACTIVE4验证而来。

边界准确落在**accepted input/control bucket**，不是“所有查询都借出缓存”。现有Batch B95–100测试只修改查询副本和debug三投影，不能证明整个ExposedMembers对象隔离。已查CopyYields、StandardizationDiscount、CommerceConvergence、NetworkIsolation、Sender等current caller仅作读取，因此不升级为当前收益bug。

候选修复：accepted input/routes/control保持唯一owner内部可写；跨Context只暴露必要metadata/ACK／只读投影，保留现有查询返回副本与UNKNOWN hold合同。不需要冻结整个Lua世界或删除兼容字段。新consumer/UI若继续读取更多bucket内部字段，会使将来封装改动面增加。

未来验证：正式查询及公开兼容投影的修改不能进入后续UNKNOWN fallback；seq/epoch/候选/旧route撤销不回归；同路线但当前ACTIVE变化仍能发布；下游无需自行持有新权威副本；不得通过将UNKNOWN当零来“修复”。

## 容量边界：IA-P13a-Q04补核，实际可达性仍未确认

**MEDIUM / MONITOR**。此前producer/transport限额不一致现已复现具体行为；当前真实存档是否达到该规模仍UNKNOWN，不作为全项目阻塞。

实际NetworkSender/Bridge/Input，原生城市/trader/routeCount和完整UI snapshot由fixture提供：128条样本发送一次且被接受；随后129条完整样本，两次pump新增请求0，`awaitingNetwork=false`，无explicit error，UI保持COMPLETE_UI_SHADOW/VERIFIED，旧128条accepted routes/inputVersion保留。`NetworkSender:26–36`在上限直接return，**不是Bridge收到了129后明确拒绝**。

BackgroundRoutes/ShadowRouteState允许更大采集范围，这不证明真实游戏能有129条。16384字节分支只做静态确认，没有单独构造超字节case。本slice不调查原生贸易容量、不提高限额。

在Harbor或其它确实扩大路线规模的获授权功能前，共同核producer→transport→accepted input→派生→consumer容量与用户可见失败，不能只放大某个常量。未来定向验证上限、超限状态不冒充新样本已经送达、回到范围后恢复、旧值UNKNOWN/确认失效策略。当前无需用户堆129条路线。

## Provisional、已知约束与反证

| 项目 | 分类／timing | 已知及未证明内容 |
|---|---|---|
| IA-P09b-Q01 Aesthetic busy直接跳过 | LOW / MONITOR | AE141不同于Meaning131–138/167–171，没有合并pending。若真实新Facts在其busy中重入，可跳过本次重算；native正常路径是否可达未证实，不扩成本次实机要求 |
| IA-P09b-Q02 publication metadata共用 | LOW / FIX_BEFORE_NEXT_PROFESSION | Network notify57只建一份publication，各consumer共用，Discount111可能保存。当前未见consumer mutation；新增消费者时明确只读/保留期限，不为理论风险给所有调用加深复制 |
| Network consumer错误诊断 | LOW / DEFER | notify仅保存最近consumerError、不含具名身份且成功不清旧值。未用于Gameplay authority，不称错算；触及通知边界时改善即可 |
| K采集依赖旧Dialogue双ACK | 现行NO_ACTION；cutover前约束 | 已由[P0-M精确退休计划](../../Architecture/v2/P0_M_Dialogue.md#建议小切片与精确退休)57–59明确记录；旧AUTO Dialogue当前仍合法。不能直接停旧Start，须保留/最小替换collector、Receive、ACK。不是本次新发现，也不能以M旧GWA阶段描述复活已retired的writer |
| 摘要变化不含具体era/work ID | 现行NO_ACTION | sameInput143–147覆盖当前AE/Meaning需要的计数/资格；未来按时代查国内来源的consumer要声明自己的变化依赖，不能默认当前摘要通知覆盖全部业务 |

已排除／NO_ACTION（只限本slice）：

- ACK不是native收益承诺：K合同和代码明确processed semantics；把UI结束等待视为收益PASS是误读。严格pair另核两端实际接受，不只比较ACK。
- Network独立consumer隔离：新增最小对照在首个Lv3Effects stub抛错后，5个consumer均被调用，且都读到已提交version1/view；效果本体stub，不能视为5个能力原生通过。
- 同路线没有阻止专业事实更新：Receive229–237仍Refresh完整input；既有B136300–375包含实际Governor gate、同回合同路线ACTIVE变化的定向断言，本次只读未重跑。
- UNKNOWN保留与确认失效撤销各有独立职责；不能删除外国事件核对、旧值保护或current reference校验来省工作量。
- 私有Network派生view、GW Read/Summary/Domestic的副本隔离有源码及既有测试反证；不建议为DRY合并所有事实owner。
- 没有因为本次条件性例外就重开GC调参、内存长测、B168人测或新native测试。

## 测试证据、复现与实际阅读

本slice只运行四个内存场景：GW逃逸回调；Network公开输入别名；128→129 sender；Network逐consumer隔离。均使用真实相关Lua边界与声明过的native/effect stub。没有执行历史wrapper、gameplay全回归、stress、游戏或部署；没有修改正式测试断言。

- [GW复现](Evidence/W04/callback_isolation_reproduction.py)／[结果](Evidence/W04/callback_isolation_result.json)
- [Network复现](Evidence/W04/network_boundary_reproduction.py)／[结果](Evidence/W04/network_boundary_result.json)

脚本默认从自身位置定位repo，也支持`--repo`；需要现有Python与`lupa.lua55`，不自动安装。stdout为JSON，源码/fixture SHA256记录在结果中。GW script动态加载`test_p0_k.py`的Fixture/PRODUCER，不运行unittest；Network仅AST提取Batch A的FIXTURE声明，不执行旧wrapper/Git历史测试。引用片段的行/assert用于防止源码变化后静默测试错块，不是公共测试框架。

现有测试只读覆盖与缺口：K292–334/426–438验证副本/重复/UNKNOWN；531–591验证ACK/失效/重试，647–660只验证整端Facts失败不阻断Dialogue，不能替代链内隔离。Meaning probe582–674有PAIR和同值重试，automatic已ready路径不同；automatic97–98及159–184有正常通知/本模块重入，没有本次前置逃逸反例。Batch A60–165、B87–151覆盖提交/UNKNOWN/查询副本/同步重入，本次补独立通知异常对照。旧AE187–193的早期通知断言未被当前automatic选择，不当作新count语义PASS，也不修改它求全绿。

实际阅读（直接入口及主任务/只读审阅合并，未声明全仓覆盖）：

- NetworkBridge1–449、NetworkInput1–67、NetworkSender1–47、BackgroundRoutes1–216、ShadowRouteState1–68；Gameplay共享公开/样本分发/Start、TradeRouteProbe115–142、具体Network消费者bucket读与Audit参数、PerformanceCounters相关flight、P0Panel缓存入口。
- GreatWorkFacts50–282、DialogueRefresh1–164；Aesthetic95–172/186–256、Meaning完整当前路径、Dialogue31–68/225–265、Standardization90–141/169–195、Store571–632及相关return注册。UI细节和每个carrier原生效果不在本slice。
- 合同：Batch A16–77、Batch B16–67、C2 60–90、K87–126、L1 104–123、L2 CURRENT/自动接入/通知边界、M47–61。历史progress语句不当当前授权。
- 测试：上述具名范围，B06992–132有界sender故障与B136300–375 facts网络集成；其它仅定位不算全文审阅。三路只读审阅均已收束；主任务独立核关键行、脚本、复现结果及反证。

## 下一准确slice与未覆盖

下一为**P08a：精确effect ownership与通用投影算法边界**。问题是当前多个模块是否真的共享相同的“读owned → 撤旧 → 加新 → 验证 → 清session”语义，哪里能共用、哪里必须保持专属；异常/busy/UNKNOWN如何影响后续扩展成本。

入口：`CultureMeaning.lua:24–57,88–128`；`ResearchApply.lua`、`ResearchChair.lua`的installed/reconcile/Audit；`CityProgressionStore.lua:RemoveOwned/IsExitTarget`；再沿Owned名单和实际writer读取一个代表SQL及现有定向断言。复用W02 facts/performance和P06/P09 maps。只有确认语义、ownership、生命周期一致才建议公共化；不为了DRY做全模块清理、不改测试或代码、不逐能力补native冷加载。

NOT_YET_AUDITED：全部consumer恢复完备性、所有跨Context协议、原生投递/耗时、真实路线规模、每专业全部carrier与永久资产、完整独立audit总范围。P09后续仅在新证据或具体协议边界需要时展开。本slice完成没有产生总审计PASS。
