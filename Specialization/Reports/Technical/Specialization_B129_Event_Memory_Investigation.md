# B129 — 征服与过回合内存增长调查

2026-09-29。只读源码/资料调查与截图归档；没有运行包修改、部署、游戏操作或玩法回归。当前B129认领功能PASS保持独立范围；长期性能问题OPEN。

## 用户证据

用户分组1=开启本Mod，2=关闭。用户补充：为避免从启用Mod的存档直接卸载造成损坏，关闭组另开新局，并在第一回合用Cheat创建约10座以上城市；数量为用户估计，不伪称已逐城统计。关闭组不是单城轻量对照；该做法符合支持存档边界，不能要求以卸载旧档来制造同档实验。38原图按时间配对查看：19游戏画面+19活动监视器。原件归档外部工作区Specialization/Status/Validation/Evidence/B129_Event_Memory_Comparison/1、2，manifest.json记录38/38匹配hash。临时拼图仅用于读取，不替代原件。

活动监视器Civilization VI“Memory”列（GB，显示精度0.01，不冒称Lua heap/RSS）：

|组|时间|游戏回合|内存GB|
|---|---|---:|---:|
|1|09:39:47|39|10.43|
|1|09:40:01|39|10.53|
|1|09:40:22|39|10.65|
|1|09:40:40|39|10.86|
|1|09:41:26|40|10.96|
|1|09:41:43|41|11.06|
|1|09:42:03|42|11.12|
|1|09:42:21|43|11.22|
|1|09:42:40|44|11.29|
|1|09:43:08|45|11.37|
|1|09:43:26|46|11.45|
|2|09:48:42|1|10.54|
|2|09:49:43|1|10.55|
|2|09:49:57|2|10.56|
|2|09:50:09|3|10.57|
|2|09:50:18|4|10.57|
|2|09:50:33|5|10.58|
|2|09:50:51|6|10.61|
|2|09:51:09|7|10.61|

开启组第39回合操作段+0.43GB；此后39→46约+0.59GB，约84MB/回合（仅描述7个间隔，不预测长期斜率）。关闭组第1回合后1→7约+0.06GB。组间不同文明/局面/回合与前序会话，不能计算严格Mod净增量；已足够支持事件相关增长需要定位。静置不增长、回合过程峰值与进入玩家回合回落属于用户观察，离散截图不是连续曲线，不独立证明具体回收时点。开启组首图还显示16GB物理内存、较高压缩/交换，进程列不等于所有数据都常驻物理RAM。

## 自动存档与回收

保存是将当前状态写入存档；不负责删除继续运行需要的数据。Game Property由引擎随存档保存，无需本Mod另写每回合落盘机制。Lua按可达性自动管理临时对象；失去引用的对象可回收，仍被表/回调引用的对象不会因为保存而被回收。进程footprint还包括原生引擎/渲染/UI/分配器等，不能直接当Lua用量。回合开始观察到下降，不能据此认定其它Mod有专属写入/清理流程。未调查所有其它Mod或Civ VI引擎内部GC调度。

依据：[Lua官方内存管理](https://www.lua.org/pil/17.html)、[Lua5.2 GC参考](https://www.lua.org/manual/5.2/manual.html#2.5)、[Apple内存footprint说明](https://developer.apple.com/library/archive/technotes/tn2434/_index.html)、[Apple heap分配分析](https://developer.apple.com/videos/play/wwdc2024/10173/)。这里只引用通用语义，不假定Civ VI精确Lua版本/GC配置。

## 直接代码调查（STATIC_CONFIRMED，非根因证明）

1. CityProgressionStore使用Game索引+每城记录；真实变更时复制校验并覆盖对应key，读取Base/Investment会复制派生值。未发现每回合追加整城历史版本的路径。征服一座原AI城即使世界城市总数不变，也会增加本玩家登记记录、模块缓存和效果核对；这是工作量变化，但不能据此解释几百MB涨幅或宣称正常。
2. RuntimeWork为每次Audit创建独立facts/district索引。ResearchSupport、Lv2Housing/GPP、ResearchInfrastructure、ResearchCross、CopyYields、CommerceConvergence等注册turn/transfer事件；多个模块分别扫描、构造plan、读取原生建筑/区域。全范围事件可能触发重复核对，P.Rows/Family与永久状态投影也创建临时表。优先测这些路径的分配量、调用量，不能仅因有临时表就定性泄漏。
3. 已查收益写入多以实际have/wanted差异执行；不能说每回合必然拆建全部carrier。但真实引擎是否出现反复失效/重建、原生Modifier增长，缺运行计数证明。
4. NetworkBridge每玩家仅保留一份派生view、相同signature不重复发布；DistrictCompleteness缓存最多8城；Gameplay事件/商路诊断各最多32条；PerformanceCounters固定94项、每项标量。未发现这些结构按回合无限保留历史。
5. 部分errors/last/views/ack等以owner:CityID保存会话项，转移改ID可能留下旧项，值得清点；这最多是候选保留路径，尚不能解释无征服时每回合的增长。未声称完成全Mod泄漏审计。
6. Mod中搜索未发现collectgarbage调用或主动停止GC；这不证明引擎全局GC状态。不要据此添加每回合强制全GC，可能掩盖分配热点且引入卡顿。

## 确定的诊断缺口

当前PerformanceCounters.New构建94项；RuntimeAuditCore.New仍断言最多64。用实际两个模块、最小Game时钟stub本地调用，返回94 / false / COUNTER_SCHEMA_UNSUPPORTED，属于LOCAL_SIMULATION_CONFIRMED（诊断组件复现，非玩法回归）。即使游戏开放文件API，现有日志也不能接受当前counter表。UI/RuntimeAudit还硬编码旧B094.121标签，不能作为实际包身份。

只读检查配置对应Logs目录，没有SpecializationRuntimeAudit文件。旧调查已有FILE_API_UNAVAILABLE边界；没有游戏内实际状态，不能认定这次首个失败必然是64上限。该缺口影响观测，不是内存增长已证根因；没有日志也不意味着游戏状态没有保存。现有性能按钮已改作计时报告，不能要求用户按旧指南点击得到计数。

历史依据：[B069事件热点](Specialization_B069_Performance_Phase1.md)、[B072日志边界](Specialization_B072_Runtime_Audit.md)、[外部监视工具](Specialization_External_Monitor_Validation.md)。旧55GB/70GB事件不自动视为本次同因。

## 建议下一最小定位批（尚未实施）

复用固定计数器，修正诊断兼容性/版本标签，恢复一个简短按需读数入口；记录一次征服前后和相邻玩家回合边界的Lua可用heap读数（若引擎允许）、原生建拆/Property写入、扫描/Audit次数、关键缓存条目数。无强制GC、不修改玩法、不清永久状态、不建无限日志。Lua heap只反映对应context，必须区分Gameplay/UI与进程总量。

先利用上述结果区分：Lua临时分配与回收延迟、Lua被持续引用的数据增长、原生引擎分配/Modifier对象增长。若Lua存量稳定而进程持续增长，再使用已有外部工具在用户同意的短窗口采集原生内存分类；不要一开始扩大成全库重构或新遥测系统。

最终隔离可在分别从开局启用/关闭Mod的可比新局进行少量固定动作；不从已启用存档直接卸载Mod做正确性对照。本轮不要求重做截图或立即运行测试。当前没有足够证据指定一个可直接修复的内存根因。

## B130.157 — authorized minimal observation checkpoint

用户同意先观测，补充关闭组回合内约10.52→10.88→10.54→静置10.52的示意（不是精确测量）。固定时点清理仅保留为思路，本批不实施GC控制、缓存清除或玩法改动。

复用PerformanceCounters，增加按需6回合窗口、最近6条环形读数。采样仅当前本地人类的回合进入/离开、涉及该玩家的城市转移及对应下一次publish（消耗一次pending）；未开启直接返回，无frame/hover/定时扫描。每回合相同边界去重，不把publish次数用作玩法或身份判定。开始/手动读取也采样；Gameplay与诊断UI分别pcall collectgarbage('count')，不可用明确显示；不是Civ VI总内存，不能相加推导进程用量。观测本身也有小量临时分配，非无扰测量。

报告读取固定计数器的基线差分（扫描、事实、建筑检查、建拆、Property写入、Network派生），并浅数D缓存/Network玩家/Claim视图与确认项；CityProgressionStore仅新增只读RecordCount。无历史全账本遍历或Property写入。窗口/数据随加载消失。旧“完成承接试验”按钮临时改为“内存观测”：左键开始/重置本次窗口，右键读取；其底层实验代码保留，不改变正式认领项目。

旧日志上限64→128可容纳当前94项，超过128仍失败，原8文件/每个4MiB及I/O失败停用策略不变。身份来自运行shared.Version；modinfo未知标NA、源码参见receipt，不继续写旧B094假标签。文件API可能仍不可用，因此核心观察不依赖日志。

LOCAL_SIMULATION_PASS：test_b130_memory_observation.py小规模确定性fixture直接加载实际模块；未启动不采样、不同玩家不采样、回合去重、一次publish消费、6条/6回合上限、只调用count不操控GC、缺接口/异常可读、94项日志可用/129项拒绝/写失败停止；修改Lua语法/modinfo157。没有玩法全回归或stress；native heap可用性和内存原因仍UNKNOWN。

最小实机：选己方城，左键内存观测并截图作为开始；正常过1回合进入玩家操作，右键报告并与活动监视器同时间截图；静置约20秒后右键再读（不点左键）；再过1回合重复。若方便，在同一次窗口内征服一城后右键报告即可，不要求重新造局。最多2回合+可选征服，六回合自动停止只是上限。collectgarbage不可用也保留调用量/缓存数据，不为此反复测试。不要切换Mod、不清内存、不要求额外自动存档操作。定位结果出来前不宣称性能修复或泄漏已解决。

Deployment: B130.157 / modinfo157, source 0d547eeed2037236b4b772f140656910d02c578a; receipt B130.157-0d547ee-playtest.json DEVELOP_ACTIVE. OS process check confirmed game exited; official restore/activate transaction retained stable and B129 recovery; source/runtime 170/170 MATCH, digest 89593f6d60998056862febd14df2dfac6f4ef5eae923c4fea40cb29bd1d3adc7. Native observation remains USER_GAME_TEST_REQUIRED.

## B130 native observation and scoped event follow-up

2026-09-29用户投递6图（三组同时间进程/诊断画面），已逐张查看并归档外部 Evidence/B130_Memory_Observation，6/6 SHA256一致；旧1/2组38图再次核对无损。原图、manifest与Observation.md保留在外部，不复制进Git。

| 回合/时间 | 进程Memory GB | Gameplay调用处count MiB | 累计城市扫描 | 累计建筑检查 |
|---|---:|---:|---:|---:|
|T39 10:22:02|10.28|277.90|0|0|
|T40 10:22:58|10.51|420.86|7773|811797|
|T41 10:23:53|10.53|486.77|11726|1435815|

T39离开/发布279.01/279.10，T40进入/发布417.71/418.00；T40离开/发布421.34/421.39，T41进入/发布482.02/482.29。所显示缓存条目始终D1/网络玩家1/认领视图3/确认10/城市记录10；建拆载体、受计数包装器覆盖的属性写入、网络派生计数均0。计数不是所有原生/其它Mod活动，零值不能排除未覆盖路径。没有单独同回合静置采样，不从这些图片推断静置完全不回收。

证据等级：USER_GAME_TEST观察确认count接口可用、这些边界读数上涨及固定条目数；不是内存修复PASS，也不是已证泄漏。count包含尚未回收对象，不等于仍被引用的存量，且并非本Mod独占用量。Gameplay/UI调用处读数几乎相同，当前“独立context”文案不能证明它们统计独立Lua堆；下一诊断应改为调用位置标签，继续禁止相加。此前报告的context归属说法在这一点上需要收窄。

### 已确认的调用放大路径（不是内存根因定论）

- RuntimeWork.Hook将CityWorkerChanged/Focus只缩到player，不保留city；各模块Audit随后遍历该玩家城市。DistrictBuildProgressChanged等未识别布局保留全范围安全核对。不能直接猜参数缩城；需先核对事件合同。
- ResearchInfrastructure/Apply/Chair、Lv2GPP、Lv3Effects等分别注册事件，分别建临时facts/plan/installed行；ResearchChair.installed即使能力未生效仍检查其全部定义载体（为了撤销旧效果）。不能简单跳过非科研城而破坏withdrawal。
- Lv2Housing.expected对符合资格城市每次MarkDirty再Read；DistrictCompleteness.Capture每次读取遍历GameInfo.Buildings整个目录。缓存只有1条仍可不断重建；条目数稳定不是分配量稳定。当前截图未报告dc_capture，不能量化它对81万/143万检查的实际份额。
- UI/GPPRefresh未过滤worker/focus事件的玩家，任何此类事件均可mark，再由publish/playback/UI pulse发送本地玩家LV2_GPP_DIRTY。Gameplay该请求会核对GPP、Lv3Effects、Lv4Percent、Infrastructure、Cross、Apply、Chair七模块，即使FactsChanged=false也运行这七项。一个窗口内dirty可合并，但不同publish间再次mark可再次发送。
- CommerceConvergence等旧writer仍核对AI城以撤销其owned效果；不把不参与专业解释成可以无条件删除其安全退出路径。no-write截图也不能证明没执行大量检查。
- P.Field每次新建pcall闭包，P.Info调用两次P.Field；大量carrier查表、installed临时行与facts克隆提供分配热点候选。尚未取得分模块字节/时间归因，不宣称其中任何一项已证为主要内存来源。

LOCAL_SIMULATION_PASS（小型只读探针，实际RuntimeWork.lua与UI/GPPRefresh.lua，临时Python/Lupa Lua55环境，无runtime修改、无玩法回归/stress）：
1. 同城3次worker事件 -> 3次player范围Audit，scope不含city。
2. 一次district progress事件 -> 无scope Audit。
3. 同玩家同回合2次turn事件 -> 1次Audit，原有去重有效。
4. 外国玩家worker事件 -> 一次本地玩家GPP dirty request。
这些证明回调代码行为，不证明真实游戏事件频率或具体MiB贡献。

### 下一最小建议（待授权实施）

先增加有界、按需的事件来源/模块工作量归因：本次窗口内各Audit调用数、D capture/hit/dirty、GPP dirty请求数与事件来源玩家；只保留固定计数及最重几项，不保存逐事件历史。复用B130窗口和入口，修正堆归属标签。局部前后count仅作分配线索（可能受GC影响，不能直接相加视为独占内存）。

拿到归因后优先评估城市级dirty合并、重复facts/目录capture复用；逐个保留当前所有权退出、UNKNOWN保留、保存重载与收益失效重算语义，不在本次调查中改writer。固定时点释放确定无用的引用仍可作为方案，但没有证据支持清理永久账本或每回合强制全GC。无需用户现在重测；不推进F、不部署。

## B131.158 — authorized bounded event and module attribution

用户“继续”授权上一节提出的最小诊断；W0004 L1，诊断不修改收益/资格/保存/事件派发。沿用B130左开始、右读取与6回合/6条边界，归因状态只在ExposedMembers会话内，重新开始重置、重新加载不恢复；固定白名单，不接收动态模块/城市key、不累积逐事件日志。未开启立即退出，超过6回合拒绝继续归因计数。

15个收益模块Audit入口各一条可选P.Observe调用，统计调用次数（包括busy/not-ready/无效资格早退，不冒充实际执行次数）。RuntimeWork在原过滤与回合去重之后统计派发，含义为每注册回调派发次数，不是去重原生事件数。UI GPPRefresh记录worker/focus/governor/turn/load的local/foreign/unknown固定桶，以及请求尝试、提交未抛异常、异常和Gameplay接收；完全不改变mark/flush/request资格和次数。提交成功不等于消费完成。

D读取/重建/命中/标脏复用原固定计数器相对开始时差分，不额外读取目录。报告按需只显示Audit前6、派发前3与有限UI分类；排序只在手动读报告时发生。Lua标签改为调用位置，独立堆未经证实，不相加、不归为本Mod独占。未采集耗时或每模块字节；本轮不尝试通过非独占Lua读数推导精确allocation attribution。

STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：test_b131_memory_attribution.py延续B130的有界采样、94项日志/129项拒绝/IO失败保护；固定key拒绝未知、新窗口清零/六回合失效/加载重置；实际RuntimeWork的原scope/回合去重/载体过滤不变；实际UI回调local/foreign/unknown、多个dirty合并、无dirty不发送、governor FactsChanged、请求异常可见；15个consumer与B130源逐字比较，除唯一诊断调用外完全相同；改动Lua编译及modinfo158。测试需要Lupa Lua55及Git历史0d547ee；没有实机PASS、玩法全回归或stress。

最小用户验证：选己方城左键内存观测开始；正常过一回合，右键读取并截图（同时保留活动监视器）；静置约20秒右键再读。若方便再过一回合，不要求造城/征服/新局。不要重复左键重置基线。若报告被裁切请投递当前画面，不要求多轮盲测。当前尚不实施dirty合并、缓存清理、GC或F。

B131 deployment: source ae8acf6f0db845adf4c219c0e3b03b6dfbca87b7; receipt B131.158-ae8acf6-playtest.json DEVELOP_ACTIVE; OS-confirmed game exit, official restore/activate, stable/B130 recovery retained; 170/170 MATCH, digest a71e93d2637b3a49e2564745837d7f028df592ee0f59f5c3775cd5019be9e8d5. Native attribution USER_GAME_TEST_REQUIRED.

## B131 native results

2026-09-29六张截图逐张读取（含原分辨率诊断细节）；外部Evidence/B131_Memory_Attribution已归档6/6 SHA256一致。未部署/改源码。

|时间|回合|进程Memory GB|Lua调用处 MiB|
|---|---|---:|---:|
|10:36:16|T39 开始|10.27|274.55|
|10:36:43|T40 手动读取|10.50|418.64|
|10:37:10|T40 再次读取|10.49|419.42|

T39离开275.98、发布276.11；T40进入416.41、发布416.61。后两组相隔27秒、同一回合：城市扫描7773、区域扫描3101、facts4342、建筑检查811797保持完全相同；建拆载体/包装器属性写入/网络派生0。所列缓存D1/网络玩家1/认领视图3/确认10/城市记录10不变。D读取29/重建29/命中0/标脏29也不变。

Audit入口计数：工业折扣579→1352（+773）；对话577、旧商业汇聚78、GPP58、学以致用58、学术主持58不变。派发前3：回合196/总督变化96/区域移除44，均为逐监听回调计数，不能当作196次游戏回合或44座区域实际被拆。
UI本人/其它/未知：工人0/0/0、焦点0/3/0、总督2/6/0、回合1/13/0、加载0。GPP请求6/提交6/异常0/已接收1，两次T40报告均如此。提交没有抛异常不等于收到或执行；缺少链路证据，不能宣称5次请求丢失、已排队或造成重复执行。

USER_GAME_TEST观察：报告入口/固定归因可读；重复手动读取没有增加已列扫描/建筑检查。性能原因未定，非修复PASS。
静置窗口进程略降而Lua略升，二者不能等同；不能证明完全无GC，也不能据0.78MiB变化归为本Mod。回合窗口Lua+144.09MiB，仍非模块独占分配。

直接源码复核：
- StandardizationDiscount.Audit入口后先检查dirty；为空只计discount_skipped_clean并返回。publish每次调用它，足以解释入口计数持续增长而城市/建筑计数不变的候选路径；本图未显示skipped_clean，不能将773次全部严格判为clean。绝不能据排名第一认定它为最大分配源。
- Dialogue.auditAll在总督事件遍历Players，但Audit内部先检查本地玩家；577也不是577次完整城市扫描。
- D 29次读取全部重建，提供重复capture线索；没有当时建筑目录规模和各capture范围证据，不能把811797次全归D。
- 本批真正的UI来源热点是其它玩家焦点/总督与回合通知，工人事件本次为0；此前worker模拟是潜在路径，不冒充本次实测原因。

下一建议：只读收敛到实际执行路径（已有discount_skipped_clean/audit_standard等计数、总督事件scope、D invalidation责任和GPP提交/接收边界），形成一个保留ownership withdrawal/UNKNOWN/重载合同的窄优化计划，再获授权实施。不再按Audit入口次数盲目清缓存或强制GC；无需用户当前重复测试。不推进F。

## B132.159 — authorized narrow event and cache optimization

用户授权实施，并确认预期为事件驱动定域更新+必要周期核对。当前runtime是混合实现：有事件标脏/差分/缓存/每玩家每回合核对，但部分native事件仍player/full范围扫描。静置publish调用可以是O(1)clean早退，不等于每帧扫城；本次B131同回合27秒扫描无增长就是该边界证据。没有宣称全系统已达单城精准派发。

本批W0004 L2，实际改动：
- UI GPPRefresh对已知其它玩家worker/focus/governor/turn事件保留观测计数，但不mark/send本玩家请求；未知参数保持原保守路径。foreign turn不再抢占本玩家lastTurn标记；LoadScreenClose/init发送与本玩家回合核对保留，不假定player0。
- Dialogue总督事件已知本玩家只核对该玩家及其GreatWorkAdjacency；已知foreign返回，UNKNOWN回退原auditAll。CityTransfered及永久/退出/恢复合同完全不动。
- Lv2Housing不再每次读取前MarkDirty；向D传入事实中的同一persistent token，避免nil/token交替使缓存失效。
- ResearchInfrastructure不再重复执行D生产者已做的invalidations。D服务早于消费者注册，补齐BuildingRepaired/DistrictRepaired；其余结构/掠夺/易主/加载失效及新回合第一次读取重新capture均保留。没有扩大缓存上限8，没有跨所有权沿用旧快照。
- 工业折扣publish clean早退不改；没有删除监听器、关闭writer、改变公式、清理永久记录、GC、F或Design变更。

LOCAL_SIMULATION_PASS：test_b132_event_cache.py使用已有P0-A/B2/C真实fixture构造（不运行其历史stress或旧版本整树断言），实际SQL+Lua验证四专业代表ACTIVE结果与B131相同；同token重复核对/cross-reader命中且不重capture；普通建筑加入、掠夺/修复、区域掠夺/修复、UNKNOWN保持、漏事件次回合核对、身份token改变、加载、确认owner失效退出；科研旧carrier退役、真实D变化与ACTIVE撤销仍正确。实际UI回调用本地player4证明foreign忽略/local合并/unknown保守/提交异常重试/foreign turn不吞local turn；Dialogue实际注册回调作用域；四模块ownership退出/恢复代码逐字对照B131未变；修改Lua语法/modinfo159。
不运行全历史回归、stress或自动游戏。不把本地分配/调用减少当作native内存修复PASS。原历史测试文件/断言未改，新测试只加载其fixture setup，新增当前合同断言。

最小实机：沿用同一测试存档，左键内存观测，正常过一回合后右键并与活动监视器截图。看D是否出现命中、请求及扫描变化；可顺手切换一次本城专家/焦点确认收益仍响应，不要求造局/掠夺。静置读数可作为补充，不重复要求多轮测试。诊断中的外国事件收到数可能仍非零（在过滤前统计），不应误读为已请求更新。需与相同存档/动作B131对照，实际总内存改善仍待观察。

部署：OS进程核对游戏已退出，官方工具先恢复稳定包再激活B132.159；receipt `B132.159-c225aa0-playtest.json` 为DEVELOP_ACTIVE，source `c225aa000c323a03c837019156654f474bca00c9`，170/170 MATCH，digest `8a3d6a2251f7cfc71ecfa05283ed56684413dc8ae3f4e9f0fb28e8df6062ae19`。稳定及B131恢复点保留；没有启动游戏，USER_GAME_TEST仍待完成。

## B132 native results

2026-09-29六图逐张读取，诊断正文另用原分辨率裁切核对；原图已移至外部 `Specialization/Status/Validation/Evidence/B132_Event_Cache_Observation/`，manifest记录6/6 SHA256移动前后一致。用户明确确认“调整专家和建筑，收益正常”；属USER_GAME_TEST_PASS（仅本次所测操作），不扩大为所有专业/ownership/全部建筑目录验收。

|时间|回合与阶段|进程Memory GB|Gameplay调用处Lua MiB|
|---|---|---:|---:|
|10:50:43|T39开始|10.26|272.55|
|10:51:15|T40过回合后读取|10.49|414.51|
|10:52:00|T40后续操作后读取|10.53|446.05|

T39离开274.13/发布274.25；T40进入412.77/发布413.02。最后一图显示此前手动读取414.68→414.73→414.77→414.81→414.81→446.05；此为6条有界环，不据覆盖早期行判断数据丢失。第三组本人worker事件增加8，用户报告专家/建筑操作；不能称作无操作静置窗口，也不能给其中任一操作独占归因。

T40首读：城市扫描7653、区域3095、facts4242、建筑检查793896；D读取29/重建26/命中3/标脏26。工业折扣入口749、旧商业汇聚78、对话67、GPP/学以致用/学术主持各58。UI本人/其它/未知：worker0/0/0、focus0/3/0、governor2/6/0、turn1/13/0；GPP请求1/提交1/异常0/接收1。外国事件被记录不等于被执行。

对照B131同T39→T40窗口：GPP请求6→1（两次接收均1）；对话入口577→67；D重建29→26且命中0→3。城市扫描7773→7653、建筑检查811797→793896（仅约2.2%降低）；入口调用不是完整重算次数，非受控benchmark，不把比例写成全局性能承诺。Lua增长144.09→141.96 MiB；进程两次都约+0.23GB。可确认窄过滤和缓存复用已发生，但主要内存增长未解决，MEMORY_CAUSE_OPEN；Lua读数非本Mod独占，也不等同进程Memory，不能推断永久泄漏或无GC。

末图：城市8997/区域4034/facts5519/建筑863046，较首读分别+1344/+939/+1277/+69150；D31/28/3/28；工业折扣入口2426，旧商业汇聚88，GPP/学以致用/学术主持/科研基建各76；worker派发56为监听回调数，不是56次玩家操作；UI本人worker8，GPP请求/提交/接收各9、异常0。两张T40图所列缓存均D1/网络玩家1/认领视图3/确认10/城市记录10；建拆载体/属性包装器写入/网络派生计数均0，不据此否定用户实际收益或未覆盖的原生/直接写入路径。

结论：B132本次专家/建筑收益响应及窄优化观测通过；内存问题仍OPEN，本轮短测试完成，不要求立即重测。后续建议仅定域调查剩余实际城市/建筑扫描来源、重复事实读取与失效派发，特别是同回合操作后的路径；先形成可审阅方案再授权修改。不得按Audit入口排名猜内存来源，不自动GC/清账本/F。本轮只归档证据和状态，无代码/Design/部署改变。
