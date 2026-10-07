# P13b — 会话状态间接保留与 GC 职责

Audit IA20261007 / W08；2026-10-07。审查baseline `dc5f672a9c7558a2cabedd40b7ab2ccf9934dec6`；所查Mod与B168.195源码未变。**Audit-only / Non-authoritative**；本报告不改变性能专项结项、GC策略、现行合同、B168待办或玩法授权。

## 本slice回答与证据边界

问题：**有界的cache/pending/ring内部，是否仍能保留过期对象或未完成任务；GC是否被用来替代语义退出？**

已核主要链没有按每次发布/回合追加完整旧城市、馆藏或路线对象图。多数对象是当前一份状态、同引用UNKNOWN时最近一份已确认状态、一个待确认包，或固定大小的标量记录。永久历史的运行镜像跟已登记历史而非当前在手城市数增长，有独立保存职责，不能当垃圾删除。

发现一个低优先级的具体边界：GW待确认dirty集合在完整采样持续失败时保留历史移除city ID；Reset也不清它。实际模块的8-ID内存反例已保存，合法完整样本会清除。它不保留旧城市/作品对象，也不是已发生原生泄漏证据。其余补强已有pending/诊断观察，未形成新的FIX_NOW或阻塞。

三路定域只读审阅已收齐，主任务复核关键赋值/退出/失败分支。静态证据与唯一最小结构复现分开；**没有执行原生GC、玩法回归、stress或用户长测**。没有证明全Mod零泄漏、跨Context销毁正确性或进程内存归因。

## State ownership / reachability map

路径以下默认仓库根；主要来源为[Store](../../../Mod/CityProgressionStore.lua)、[NetworkBridge](../../../Mod/NetworkBridge.lua)、[Sender](../../../Mod/NetworkSender.lua)、[BackgroundRoutes](../../../Mod/UI/BackgroundRoutes.lua)、[GW facts](../../../Mod/GreatWorkFacts.lua)、[GW producer](../../../Mod/UI/DialogueRefresh.lua)。

| owner／对象 | 内部内容与规模 | 替换、失败、退出边界 | 结论 |
|---|---|---|---|
| Store index／positions／workers | index/reservation逐城；positions只存token；worker闭包持有当前root和公共服务/callback。`Store:637–641,708–750` | load按index恢复；失城/缺record保留防重复登记；不是按当前归己方城市数prune。manager统一监听`:1170–1178`，并非每城新增原生listener | 永久权威的运行镜像，NO_ACTION；不能用GC或失城清空历史 |
| worker.root／envelope.records | 当前record的隔离副本，历史资产体积按自身合同增长 | `:160–164`替换root，`:694`成功后替换manager副本；写失败可保留候选root＋旧envelope各一份；无previous版本链 | 复制不等于双永久authority；P06a未提交值问题仍单独保留，不因本次未见历史链而关闭 |
| Store pending | production上限为map plot容量，旧adapter才是4；每候选≤8个completion；reference/序号/ID/错误/事实表，无City/District句柄 | `:897–935,1090–1092`；成功`:1057`移除，失败/城市移除只标错`:1050–1055,1143–1144`；重复LoadScreenClose`:1113`不清候选 | 补证P06a-Q03；失败可留小型payload至context结束，无无限自动retry证据 |
| Store事件/退出诊断 | 6类事件各最后一条、每条≤6个标量；transition/conquest/foundation单槽；exitReads每module只有checked/removed | `:14–22,517,585,603`；原生对象记录为类型字符串。回调共享引用不是每worker复制consumer对象图 | 有界诊断；没有事件历史链 |
| Network accepted input／private view／公开投影 | 每player一份routes/input/candidate及派生view；三份公开投影是当前值副本。Input UNKNOWN fallback取旧标量再构造新row，不挂previous input | Bridge`:45–93,134–173,201–234`；成功替换、过期candidate删除、confirmed invalid与隔离清除。失败保留最近确认值，不追加失败版本 | UNKNOWN hold必要；P09b公开input alias问题不因此消失；无版本历史链 |
| Network sender flight | 单份seq/turn/fingerprint，不持有snapshot/routes/packet | Sender`:4–7,18–24,38–44`：ACK、epoch、跨turn、发送失败、stop清理；payload是同步调用局部值 | 无界队列疑点在所查路径不成立；引擎内部请求队列未审 |
| UI routes snapshot／normalized shadow | lastGood与public.snapshot指同一当前对象；normalized为另一种标量表示，其current/lastGood也可共用同一对象 | Background`:139–162`成功替换、失败保留最近值；ShadowRouteState`:40–60`Reset清空/Read复制；stop/shutdown见下节 | 多种当前表示有职责，不是每版本保留；静态未证销毁后整个Context可达性 |
| GW UI cache／sent／pending | 每city当前ref、raw/legacy两个解释；sent一个内容key；pending一个packet。Collector闭包只留building IDs | DialogueRefresh`:31–46,60–93,104–115,133,155–163`：新ref/dirty替换，完整遍历prune，epoch/generation/load清cache；ACK或跨turn清pending；最多2次重发；Shutdown清cache/pending并移除hooks | ACK_TIMEOUT可以留一包，不是无限自动重发。遍历中途失败时prune可能尚未运行 |
| GW Gameplay cities／era index | 当前完整样本与era→city计数；接受端≤512城/4096作品、refs≤200000字节/data≤500000字节 | Facts`:90–141`完整接受整体替换，`:72–82`删目标/Reset标UNKNOWN，`:245–255`确认loss/return；同ref UNKNOWN保留最近确认record | 不按epoch保存多代样本；GC不能替代UNKNOWN退出语义 |
| GW dirtyScope.cities | city ID→true，不持有work/City对象 | Facts`:75,263,267–270`加入；完整接受`:128,141`清空；Reset不清。详见F01 | 条件性历史键累积，LOW / MONITOR |
| 直接consumer持有值 | Discount每player最近publication标量/签名；Convergence同步batch借route rows；Dialogue每player当前sample和本次plan | Discount`:111,130,252,280`覆盖/清除；Convergence`:28–38,98`结束batch；Dialogue`:129,233,259,297,304`重建/替换/转移与return清样本 | 所查引用不回挂完整旧view/input；未推广到全部consumer |

单槽不保证绝对小：GW UI采集上限为每城4096作品且≤512城，串包前没有与Gameplay总4096作品/字节上限完全一致的统一预算。packet/sent和当前cache仍随输入规模增长。这是当前输入/transport容量边界，不是历史版本泄漏；真实规模未测，本次不提高限额或复活retired GWA。

## GC ownership与hot-path边界

[PerformanceCounters](../../../Mod/PerformanceCounters.lua)`:110–279`是唯一协调入口，生产调用只在[Gameplay](../../../Mod/Gameplay.lua)`:822`；`:179`只有一个full-collection原语。`Count/New`:3–25使用固定counter名，Flight只存数值。GC本身没有保存Property、账本或清carrier操作。

| 路径 | 频率 × 数据／近似成本 | 保护／保留 |
|---|---|---|
| GC回合请求→Publish评估 | 本地合格玩家activation排单个turn；多次Publish先取走pending并核assessedTurn。idle检查O(M＋固定UI门槛)，M为shared模块数；不遍历城市/建筑/作品 | `:147–166,237–264`；不是全引擎事务已完成证明。busy/UNKNOWN状态不由GC擅自修正 |
| full collect | 满足增长128MiB、间隔≥2回合及已知quiet条件才调用一次；耗时取决于调用处整个Lua堆，不能从源码推导为本Mod成本 | `:168–195`；不循环追旧baseline、不stop/restart/改全局参数；失败/异常耗时>2秒锁停，无自动重试。2秒是异常保护，不是日常卡顿许可 |
| GC结果／日志 | 最近8条，每条只有turn/reason/数字/boolean/status；本session最多打印24行，达到上限仍维护当前状态 | `:115–145,171–193`；没有保存堆对象列表或完整诊断快照 |
| 手动计数观测 | 仅armed期间事件记录，最多6回合；最近6条，每条12个counter总数，baseline一份，seen为固定事件标签 | `:280–335`；只count不触发GC，报告字符串调用时构造；停止后有限记录保留供读取 |
| 显式GC诊断接口 | 与自动入口共享busy、token、failure、cooldown；token≤100字符，单个last/switch token | `:197–225`；ReadGC是展示/当前heap count，不能称完全没有分配或读取。它不运行full collect |

[当前Architecture约束](../../Architecture/Specialization_v0.1_Architecture.md)`:78–103`已明确临时状态由模块owner收尾、GC不可替代语义清理/归因，所查GC代码没有越权清永久状态。既有专项结项及剩余非阻塞风险保持；本slice没有重检旧截图/进程读数。

既有[GC定向测试](../../../DevelopmentTests/test_b138_gc.py)静态审阅：`:96–110`验证旧GC接口/回调不能再次collect；`:136–168`验证B139缺LoadScreenClose兜底；`:174–244`覆盖busy/失败锁停；`:247–258`覆盖8条结果/24日志。fixture的GC、clock、native events均为mock，这些断言不证明旧闭包已释放或原生回收耗时。当前wrapper还含旧modinfo166断言，本轮未运行、未改断言求绿。

## 新confirmed finding：IA-P13b-F01 — dirty范围的失败期历史键保留

**LOW / MONITOR。证据：STATIC_CONFIRMED + LOCAL_STRUCTURAL_REPRODUCTION。**

GreatWorkFacts的changed/invalidate将city ID加入dirtyScope，完整合法接受才清空。若完整采样长期失败，期间移除的不同city ID仍保留，集合大小按“上次完整接受以来不同事件ID数”增长，不严格等于当前城市数；Reset改变epoch也不清它。同一ID重复不会增长，外国Owner被过滤。没有旧作品/原生对象间接链，不是按回合追加日志。

[最小脚本](Evidence/W08/reproduce_dirty_scope.py)执行未修改的实际GreatWorkFacts；catalog、原生事件、玩家资格和当前空城市集为stub，Lua5.5而非Civ VI VM。只用8个合成城市ID，不是规模压力测试。[原始结果](Evidence/W08/dirty_scope_result.json)：

| 操作 | retained dirty keys | 可证明的事实 |
|---|---:|---|
| 8个本地城市ID依次加入/移除；当前城市集为空 | 8 | 已移除ID仍保留 |
| 重复相同8个通知＋外国Owner事件 | 8 | 去重/Owner过滤有效 |
| 当前epoch坏样本（FactsData为表而非字符串），GW_SAMPLE_SIZE拒绝 | 8 | 验证失败不会清集合 |
| Reset切新epoch | 8 | epoch变化不是该集合退出 |
| 合法空全集接受 | 0 | 完整接受可以收敛，无永不释放证据 |

这不证明当前用户存档持续触发错误、不测字节或native内存、也不证明engine city ID无限增长。监测触发是持续采样失败且不同city ID继续出现，而非单次进程上涨。

候选修复边界：若未来触及本服务失败恢复，可以在dirty.all已能保守表达完整重采时合并/收缩重复ID，或设明确的全范围失效表示；不得把未知当空样本、随意丢掉并发变化、删除最后确认馆藏。现在不实施，不新建dirty管理平台。

未来定向验证：重复/foreign不增，持续失败的scope有界表达不漏更新，Reset和真实loss保持保守语义，合法完整接受清空，同回合collector重入新增dirty仍保留。既有native已成熟部分不要求重走完整save/load仪式。

## 既有观察补证与条件性限制

- **IA-P06a-Q03保持OBSERVATION / MONITOR：** 标错pending不再admit/replay，旧completions最多8份可留到context结束。它承担防再登记保护；失败也可能发生在record已建立之后，不能统一删除。以后修候选收尾时可压缩不再使用payload，属于LOW / DEFER维护，不新报无界泄漏。LoadScreenClose只置ready/reconcile，不等于新建整个context。
- **IA-P13a-Q03保持LOW / MONITOR：** Bridge`:332,362–372,396`分页表存历史点击城市的signature/page。同key覆盖、同城普通摘要清key、隔离整表清；正常loss没有对应prune。只持有字符串，没有route/City/旧view回指。不能写永不清除，也不能据此归因大内存增长。
- **IA-P13b-Q01，LOW / MONITOR，条件性协调风险：** BackgroundRoutes`:159–173`发现Gameplay对象替换时清snapshot，却没有同时reset Sender；Sender epoch清flight只在send执行。若此前有flight、对象被替换且后续采集持续失败，flush要求snapshot存在才处理ACK，旧awaitingNetwork可能保留到成功采集、显式隔离stop或Shutdown，进而使Counters`:160–161`跳过自动GC。仅保留seq/turn/fingerprint；无native可达/长期阻塞证据，本轮不复现或调整GC。未来若正式支持UI与Gameplay独立重启，再针对epoch-reset＋采集失败核一条定向恢复，不因此请求用户长测。
- **重启/Shutdown的范围：** BackgroundRoutes关闭sender/normalized、移除hooks并解除当前公开入口，但没有显式nil所有局部值；lastGame是整个shared的强引用。不能仅凭未nil就判泄漏，仍依赖Context真正释放。Facts Shutdown清主要cities/index/OnConfirmed/hooks，不保证仍被Store callback引用的旧对象已释放。StartMemory也没有Remove旧hooks，GC callback有current guard，旧count-observer没有；只找到一个生产StartMemory调用，故不报现行重复注册问题。未来引入动态restart时须明确teardown，当前DEFER。

以上条件不改变P06a-F01、P13a-F02/F03/F04等已有较高返工优先级；本slice没有新增FIX_NOW，不重开整个性能专项。

## 阅读、验证及准确续接

实际读取/复用：根/项目AGENTS与项目导航、W0001 start/recovery规则；Authority关键元数据、Status真实CURRENT、当前context检查；P06a/P09b ownership/pending表、P12a边界和ledger。主查PerformanceCounters全文、GC实际caller、B138测试上述片段；定域并行审阅Bridge/Sender/BackgroundRoutes/ShadowRouteState全文、GW facts/producer全文；Store本slice关键状态/事件闭包；直接扩读Input`:20–67`、Discount/Convergence metadata与batch、P0Panel直接reader、Isolation入口、Dialogue当前sample替换、CityIdentityRead.Copy`:7–24`、E2保存合同`:766–779,804–810`。没有重读全部专业或历史。

审计产物只有本报告、ledger及W08复现/JSON。复现源hash和脚本hash在JSON，Git记录其它静态来源baseline；不维护第二份全源码hash清单。不运行正式玩法套件；文档/context机械检查不代表native PASS。

**P13b此逻辑slice覆盖完成。** 未覆盖：所有模块对象图、单位/合同事务、native Context销毁/跨Context对象代理、实际分配字节及用户当前规模。整体P13和独立审计尚未完成。

下一logical slice **P14a — 部署事务的authority与失败恢复边界**：先复用ledger P01的source/live/stable/receipt事实，再读`tools/README.md`、`Architecture/Playtest_Workflow.md`相关部署/恢复合同、`tools/deploy.py`与`tools/temporary_playtest.py`中的target校验→stage→切换→receipt/pending→中断恢复路径；按实际引用再选对应工具测试。回答是否每个破坏性步骤都有唯一事务owner、明确可恢复状态及不触及其它Mod的边界。本轮未开始；不核验外部运行包/恢复包、不实际部署或触碰游戏目录。若需要隔离故障复现，只使用审计临时目录，项目工具保持只读。原生生命周期其它问题分别留后续P06/P07，不重新扫描已核D/Store复杂度、callback或writer反例。
