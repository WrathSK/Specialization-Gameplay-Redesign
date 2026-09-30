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

## B132 multiturn conquest results

2026-09-29用户新增11组/22图。顺序由用户明确：第1组载入；第2/3/4组同T39分别征服一座AI城；第5组静置，用户观察约0.1GB回落；之后逐回合截图。全部相关画面逐张视觉读取，诊断及Activity Monitor行另以原分辨率裁切核对。原图归档外部 `Specialization/Status/Validation/Evidence/B132_Multiturn_Conquest_Observation/`，22/22 SHA256一致、manifest保留分组；不覆盖前批六图。PID9241全程一致。没有运行游戏/修改源码/部署。

|组|时间|阶段|进程Memory GB|Gameplay调用处Lua MiB|累计城市扫描|累计建筑检查|D读取/重建/命中/标脏|
|---|---|---|---:|---:|---:|---:|---|
|1|10:56:09|T39载入后开始|10.28|272.41|0|0|0/0/0/0|
|2|10:56:45|T39征服1后|10.39|330.83|3041|230339|14/14/0/14|
|3|10:57:07|T39征服2后|10.54|432.80|8678|602760|42/42/0/42|
|4|10:57:34|T39征服3后|10.72|505.40|12903|895457|62/62/0/62|
|5|10:58:15|T39静置|10.62|508.47|12903|895457|62/62/0/62|
|6|10:58:40|T40|10.86|650.36|20852|1780257|91/88/3/88|
|7|10:59:03|T41|10.95|700.20|24826|2488318|101/95/6/95|
|8|10:59:24|T42|11.07|742.65|27580|3015484|107/98/9/97|
|9|10:59:44|T43|11.12|790.19|30872|3633294|117/105/12/104|
|10|11:00:18|T44|11.20|841.90|34424|4216126|127/112/15/111|
|11|11:00:45|T45/观察已停止|11.27|885.73|37643|4784607|134/116/18/115|

观察与限度：
- 三次征服对应Lua读数增量58.42/101.97/72.60MiB、进程+0.11/+0.15/+0.18GB；城市记录10→11→12→13与本玩家新取得城数一致，不等于世界城市数增长。认领视图3→3→4→4；其它所列条目D1/网络玩家1/确认10保持。只能说时间窗口相关，转移采样点不能隔离本Mod与其它引擎/Mod工作。
- 第4→5组41秒静置：进程10.72→10.62GB，Lua505.40→508.47MiB。城市/区域/facts/建筑分别12903/4392/8243/895457完全不变，D四计数不变，收益载体创建1/移除0、属性包装器写入9、网络派生3也不变。工业折扣入口2651→3995，其它显示入口不变；入口含早退，不能判为1344次完整扫描。进程Memory确有回落，但Lua没有同期回落；没有证据把0.1GB归为本Mod GC或解释具体OS/引擎回收机制。
- 第5→6组Lua+141.89MiB；T40→45随后5回合各+49.84/+42.45/+47.54/+51.71/+43.83MiB，平均47.07MiB/回合，只适用于此短窗口，不外推无限线性泄漏。T40→45进程10.86→11.27GB。载体1/0、属性9、网络派生3、所列缓存及13城市记录从第4组起均不增加；固定条目数不证明内部字节量固定，更不覆盖全部对象/其它Mod。
- 后续每回合仍约52.7万～70.8万建筑检查（T40→45），D重建每回合3～7次、命中每回合+3；征服窗口62读全重建。说明B132消除了部分重复请求，但大量扫描仍存在；不能由此将全部检查归因于D，也不能把检查数当作字节或耗时。
- 第2～5组GPP UI请求/接收均0，已可排除“这些征服窗口增长都由该UI刷新请求造成”。T40～44请求/提交/接收每回合各+1、异常0；收益模块GPP核对累计120/151/177/207/240远高于UI请求，另有事件与正常核对入口。不能把全部剩余增长继续归于已过滤的外国UI通知。
- 第11组T45显示已停止是六回合有界观察的既定行为。只读核对 `Mod/PerformanceCounters.lua:StartMemory`：自动事件快照在startTurn+6停止，归因桶到期停止；手动Read仍读取当前heap与常规累计计数差。因此T45的Lua/累计扫描可用，但其事件桶/请求桶不是完整T45观测，不能据请求仍5判断本回合未刷新。

证据判断：USER_GAME_TEST_OBSERVED多回合增长及静置进程回落；沿用此前所测收益响应PASS。性能问题仍MEMORY_CAUSE_OPEN，未证明模块独占内存、永久泄漏、GC关闭或周期存档可回收内存。没有提出强制GC或清永久数据的修复。本次多回合测试完成，暂不要求重复长测。

下一建议（未授权新实现）：定域只读定位 `building_check/city_scan` 的实际增加点及触发链，对征服的结构事件串与每回合重复事实读取分别建立调用范围；区分需要重新采集的城、其它城及共享目录重复构造，保留ownership退出/恢复/UNKNOWN门禁。先利用现有计数与本地可复现路径，再提出最小修改或必要的分配测量，不再仅按Audit入口排名优化。持有引用/临时分配/引擎其它工作仍是待区分假说。

## B133.160 — authorized removal of confirmed redundant work

用户授权先修已确认的浪费，再观察剩余性能问题；不以“尚未证明全部内存归因”阻止安全优化。W0004 L2；本段为当前源码的实施/验证记录，部署状态单独以Status/receipt为准。无Gameplay/保存schema/Design/F变更。

本批四项：
1. Lv2GPP完整预读32项后，不再无条件再次读取全部carrier；已一致的项直接跳过。需要改变的项仍读取最新状态、先移除后添加、写后核实；UNKNOWN先停写。没有跨事件carrier缓存。
2. DistrictCompleteness重用已经建立的完整ordinary目录数值索引，按Index排序一次，避免每capture再次枚举GameInfo.Buildings构造DB行。城市HasBuilding/location/pillage仍实时读取；非ordinary/unknown/Wonder/internal排除项、未完成对象、D计算及八城缓存不变。加载清掉索引，不缓存动态建筑状态。
3. BuildingAddedToMap/BuildingRemovedFromMap用现行RuntimeWork与Standardization已采用的第四参数owner，仅使已知合法owner缓存失效；非法/未知回退全范围。不猜CityID。其它结构事件、CityTransfered、Return、跨回合漏事件核对不变。
4. Probe.Family先返回直接命中的基础区域类型；原本也优先该结果，现在不必先构造seen/完整DistrictReplaces。特色/替换链/循环/重复记录优先级/缺表行为不变，无新持久缓存。

LOCAL_SIMULATION_PASS / STATIC_CONFIRMED：`DevelopmentTests/test_b133_redundant_reads.py`使用Lupa Lua55、Git c225aa0及P0A/B2/C fixture setup，不执行历史stress或版本整树断言。32组非零player7的四专业/ACTIVE/专家连续变化，carrier图、写入量及顺序与旧版一致；稳定检查64→32；完整预读、最后一项未知、facts/worker未知保留、失城退出与恢复通过。Family22组结果一致，基础区域替换表枚举1→0。D八组完整输出相同（深度、Tier、特色、掠夺、unfinished、Wonder/internal/unknown、最高单区域），建筑定义枚举9→1；owner隔离、未知回退、易主全失效、token/加载/跨回合/失败保持通过。实际Housing/GPP/Infrastructure的建筑修复/移除、ACTIVE变化、UNKNOWN、旧carrier清退通过。修改Lua语法、modinfo160及module-owned ownership callbacks逐字不变。

这证明重复工作减少，不是Civ VI总内存修复PASS。其余carrier核对仍有退出/验证职责，未盲目跳过；易主/不确定结构事件仍可广域扫描。无强制GC、永久记录清空、新收益或全系统重构。

最小实机对照（部署后）：沿用同一存档，左键开始观测，重复三次征服后读取，再过1～2回合读取，配活动监视器截图；可顺手调一次专家/建筑确认收益响应，不要求新局/全专业验收。先看此批改善，再决定其它路径；Native待测。

部署：B133.160 / modinfo160，source `d50029a`；OS确认游戏退出后按W0003既有工具完成稳定包中转与临时激活，170/170 MATCH，receipt `B133.160-d50029a-playtest.json`（DEVELOP_ACTIVE）。稳定/B132恢复点保留；未启动游戏，Native待测。

## B133 native comparison

2026-09-29：用户投递10组20图，表示操作几乎与上次一致。全部原图逐张视觉读取，显示P0-B-133.160、同一PID12278。按画面为T39开始、三次征服、T40–45逐回合；本批没有独立静置对照组，不把第5组误当上批的静置组。原图归档外部 `Specialization/Status/Validation/Evidence/B133_Multiturn_Conquest_Comparison/`，20/20 SHA256一致，manifest保留配对。仅证据归档，无源码/部署/Design修改。

|组|时间|阶段|进程Memory GB|Gameplay调用处Lua MiB|累计城市扫描|累计建筑检查|D读取/重建/命中/标脏|
|---|---|---|---:|---:|---:|---:|---|
|1|11:26:13|T39开始|10.27|272.10|0|0|0/0/0/0|
|2|11:26:32|T39征服1后|10.36|330.11|3041|220195|14/14/0/14|
|3|11:26:56|T39征服2后|10.51|431.22|8678|571592|42/42/0/42|
|4|11:27:21|T39征服3后|10.69|503.43|12903|849857|62/62/0/62|
|5|11:27:43|T40|10.91|642.62|20852|1710561|91/88/3/87|
|6|11:28:08|T41|11.01|693.37|24826|2410622|101/95/6/94|
|7|11:28:29|T42|11.09|734.13|27580|2969372|107/98/9/96|
|8|11:28:51|T43|11.18|782.93|30872|3543310|117/105/12/102|
|9|11:29:13|T44|11.25|832.60|34424|4117982|127/112/15/108|
|10|11:29:43|T45/观察已停止|11.32|878.48|37643|4680991|134/116/18/111|

按相同游戏阶段比较B132→B133（不是按相同组号）：
- 三次征服累计建筑检查895457→849857，减少45600（5.09%）；截至T45为4784607→4680991，减少103616（2.17%）。确认重复检查减少，符合本地已验证的优化方向；不能把所有差值逐项归给某一优化，也不是耗时/内存百分比。
- 各对应阶段城市扫描计数完全相同：3041、8678、12903、20852、24826、27580、30872、34424、37643。D读取/重建/命中也各阶段相同；T45标脏115→111，尚未转化为额外命中/更少重建。说明本批主要减少单次核对内部成本，没有降低这条实际操作链的城市遍历次数。计数为遍历城市条目，不是37643次全城扫描。
- 三次征服Lua增量232.99→231.33MiB，改善仅1.66MiB。T40→45平均增长47.074→47.172MiB/回合，基本不变；B133各回合为+50.75/+40.76/+48.80/+49.67/+45.88MiB。T45绝对Lua比旧版低7.25MiB，但起点也低0.31MiB；开始至T45累计增长613.32→606.38MiB，只少6.94MiB（约1.13%），不能将绝对差误报为明显斜率改善。
- 进程Memory：三次征服增长0.44→0.42GB；T40→45两次均+0.41GB。本次T45绝对值11.32高于旧11.27GB，但上次另有41秒静置、约0.10GB回落；本批没有同等静置采样，不能据终值断言优化使内存恶化。同样，没有进程增长明显缓解的证据。
- 城市记录10→11→12→13，随后稳定；D条目1、网络玩家1、确认10，认领视图3→4后稳定。第三次征服后所列建载体1/拆载体0/属性写入9/网络派生3直到T45均不增加。稳定条目/包装器计数不证明内部字节固定，不代表覆盖引擎全部写入。
- GPP请求/提交/接收：征服期0；T40–44各累计1→5、异常0。T45六回合观测已自动停止，事件/请求桶不能当完整T45；手动Lua和累计扫描仍可用。图中UI调用处Lua与Gameplay处非常接近，不相加或假设独立堆。未收到本批独立收益操作验收，不扩大为全功能PASS。

结论：USER_GAME_TEST_OBSERVED（本次实机观测）确认减少检查，但B133没有解决主要逐回合内存增长。修复应保留，不回滚已消除的浪费。无需再重复此轮长测。下一建议转向仍原样发生的城市遍历与事件串重复核对，按直接调用点找出同一事实/同一城市被重复处理的可合并工作；保留UNKNOWN、ownership withdrawal/recapture、当前事实失效与有界补查。先在本地形成明确窄范围修复与验证依据，不继续只盯Audit入口总数或向用户重复索取相同截图。不是所有扫描均可删除；没有授权本轮新增实现、强制GC、永久记录清理或F。


## B134.161 — manual full-GC diagnostic and scoped network capture

2026-09-29：用户以B133.160为基线明确授权两条独立工作线：手动完整GC用于区分未回收临时对象与回收后基线增长；以及已证实、不改语义的窄事件范围修复。保留B132/B133修复，不重新长测、不新增泛化计数体系，不调整引擎GC策略，不清Property/永久账本，不进入F。此授权替代上一节当时的“未授权新实现/GC”。

### 1. GC环境、范围和安全合同

STATIC_CONFIRMED：当前`PerformanceCounters.Heap`只执行`collectgarbage('count')`并除1024显示MiB。B130–B133截图证实该count入口可返回数值；它属于Gameplay调用所在Lua堆，不是本Mod独占、不等于进程RSS。UI另一次count是否共享同一堆未证，不能相加。没有按Mod归属分配的现成计数器。

本次对canonical Mod、现有观测/外部monitor工具，以及本机安装的原版/DLC、HD/Workshop和本地Mods可读Lua脚本定域搜索`collectgarbage/gcinfo/setpause/setstepmul/lua_gc`：除本Mod已有count外未找到GC控制调用；没有发现本Modstop、调参或未配对restart。该结论不覆盖引擎二进制内部策略、未加载可读脚本以外的代码或宿主注入。只读原生UI发现`GetTickCount`/`Automation.GetTime`用例，但不据此猜Gameplay可用性或计量单位。二进制strings没有给出可据以确认的Lua版本；测试Lupa lua55不是Civ VI环境证明。

Lua标准手册定义`collect`为完整循环、`count`为KB、`isrunning`为运行状态，`os.clock`为近似进程CPU秒而非墙钟；终结器可复活对象、增加分配或使释放延至后续循环。参照[Lua手册](https://www.lua.org/manual/5.3/manual.html#pdf-collectgarbage)、[clock](https://www.lua.org/manual/5.3/manual.html#pdf-os.clock)、[finalizers](https://www.lua.org/manual/5.3/manual.html#2.5.1)，不将其当作此游戏完整GC已实测。原生实际`_VERSION`和可用方法由本次诊断报告；若缺失/拒绝就停止本次尝试，不要求反复重启碰运气。

新增入口复用P0已有隐藏按钮：**手动GC诊断**。左键说明/读已有结果，右键明确执行一次。无需选城、无需启动旧6回合内存观测；默认零完整GC。调用经过现有本地人类资格校验和一次Gameplay request，先读count/可选isrunning，执行一次受pcall保护的collect，立即读后值。若`os.clock`可读则显示CPU耗时，缺失/错误/无效数值则明确“不可用”；不伪称墙钟耗时。记录最多3次标量结果，UI仅一个结果槽，本次加载有效、不保存；同请求重复不重复执行，接口失败后本次加载停止再试，无自动重试。

没有新回合/每帧GC、stop/restart、step、模式切换或参数修改；不主动清任何缓存、Property、账本或游戏记录。完整GC本身会运行宿主/其它Lua对象的终结处理，不能承诺只触及本Mod对象，因此用测试存档副本，调用可能短暂停顿。报告“调用成功”只证明调用返回，无引擎内部全堆释放保证。运行状态前后若变化则标异常并停止，不擅自恢复策略。

### 2. 城市访问口径及本轮修复

`city_scan`是不同消费者对城市条目的累计访问数：不是唯一城市数、不是全城遍历批次数，更不是分配字节数。`RuntimeWork.New`只在单次Audit内复用事实/区域；各模块的独立native listener及`LV2_GPP_DIRTY`直接调用仍可能重复读取。同一输入签名防止**发布/derive**，但NetworkBridge在判断同签名前仍先调用NetworkInput.Capture遍历城市、构造事实/签名表。

本轮仅修`NetworkBridge`三条已确认第一参数是玩家ID的事件：`PlayerTurnActivated / GovernorChanged / GovernorPromoted`。有效玩家参数只Refresh该玩家；非参与玩家早退；缺失/负/非整数/字符串等未知参数保留全Rebuild。本玩家仍扫描其全部城市，且同回合每次真实变化和重复通知都处理，不引入每城市每回合一次。`GovernorAssigned/Established`有城市Owner和总督Owner双参数，连同首都、建城、失城、移除、路线、战争、load、module-owned exit/return保持原范围。

签名证据：原版`Civ6.app/Contents/Assets/DLC/Expansion2/UI/Additions/GovernorPanel.lua`695/711与Base `Assets/UI/UnitFlagManager.lua`1469；HD Workshop `289070/2465378070/Gameplay/RegionalYields.lua`274–279。网络输入只含本玩家Identity/Potential/ACTIVE/anchor/capital及路线端点，不读取跨境总督光环产出；ACTIVE仍按本城正常总督门槛。Assigned/Established保留全范围，不由第一参错误排除跨Owner调任。

实际Bridge/Input Lua的五城定向模拟（相同输入、B133对照）：

| 输入 | B133城市条目访问 | B134 | 保留结果 |
|---|---:|---:|---|
| 12外方玩家×三类事件 |180|0|本玩家输入版本不变 |
| 同回合六次本玩家事实变化 |30|30|每次新的全国源等级可见 |
| 相同状态本玩家回合通知两次 |10|10|保持原重读机会 |
| 15次未知/无效参数 |75|75|保守完整重读 |
| 四次Assigned/Established（含跨Owner） |20|20|完整重读 |

预期减少的是这三类无关事件引发的**本玩家城市访问、事实读取及该Capture的临时表/签名构造**。原生事件投递数不变，未测对象字节/耗时；同输入原本就不写新结果，因此不宣称减少实际Property/carrier写入。不能外推总扫描降幅，也不能据此解释B133内存增长。

第二条已定位但未修改：`LV2_GPP_DIRTY`在纯worker/focus刷新时仍调用无worker输入的ResearchCross。应另核FactsChanged与独立UI样本接收边界再切换。自身写入方面，RuntimeWork已过滤可识别carrier事件，但`CityBuildingsChanged`仍可使D标脏；成功writer还会提升输出版本供跨城收益依赖读取。暂不能把这些一概去掉或跨回调缓存EffectiveFacts，不对UNKNOWN、Claim、失城和全国依赖作粗节流。

### 3. 本地证据与测试限制

定向L2诊断 + L3网络失效/加载边界；不是全玩法回归/stress。`test_b134_gc.py`验证真实诊断和早期request路径：默认关闭、只读零collect、foreign/非法/重复请求、无事件GC、三条上限、count/collect失败与停止重试、状态/计时不可用、停止状态不restart、回收后数值增加也如实报告、状态异常不修策略。修改Lua语法及modinfo161检查通过。

`test_b134_network_scope.py`用既有最小fixture和实际Bridge/Input比较B133：上表、全国多源、首都改变、UNKNOWN保留、失城撤销/有效新包恢复、商人移除，以及load新epoch拒绝旧包均LOCAL_SIMULATION_PASS。永久写入0；未改保存/Claim/能力writer。不新增泛化计数器。

尝试旧`test_arch_v2_batch_a.py`时，其先执行B069完整wrapper并在初始UI路由取`n.players[0]`阶段报nil，未进入该文件后半网络合同断言。对B133六个改动文件作只读Git源码替换后同样失败，属于既有历史夹具/当前初始化不匹配；**该旧入口未通过**，不改历史断言、不称其回归PASS，也未跑到旧stress循环。本轮采用独立定向fixture补齐直接边界；不是全E2验收。Civ VI实际collect、Lua版本、计时能力、UI显示、修复后的总扫描/内存效果均USER_GAME_TEST_REQUIRED。

### 4. 最小实机测试与判读

仅使用现有可复现存档的副本，完全冷启动；不重新征服三城，不关闭整个Mod读档，不进行30多回合长测。

1. 进入玩家回合并等加载/画面稳定，打开专业化诊断；左键“手动GC诊断”看说明，再右键一次，截图初始前→后、环境/状态/耗时。
2. 正常过一个玩家回合，稳定后右键一次；再过一个玩家回合，稳定后再右键一次。三个时间点均不连点、不开始旧内存观测。最后报告保留三次前后值；截图三次即可。若自然出现同回合真实变化仍正常操作，不用另加功能清单。
3. count/collect不可用、报错、状态异常或严重卡住：截图并停止；不反复尝试。无需为这次诊断覆盖保存/重载或重新长测。

若回收前增长明显而回收后趋稳，支持临时对象积压；若回收后基线持续上升，记录为**该Lua范围回收后保留增长**，还需排除初始化、合理新增状态及finalizer延迟，不能直接判本Mod泄漏。Lua回收后RSS未下降也可能是宿主分配器保留内存，不等于对象仍可达。不以三个点宣布长期稳定/根因关闭，也不把同时存在的三事件修复归因给GC。

若接口不可用或后基线继续增长且现有证据仍不能定位，下一步才提出同存档单一路径停用对照；DB/存档记录保留，并明确哪些正常consumer、UI request、ACK/重试和撤销仍运行。不得只切掉receiver导致积压；本轮不提前实现开关或要求另一轮长测。

部署记录：B134.161 / modinfo161，source `d9e69ba`；OS再次确认游戏退出，通过既有stable恢复中转/临时激活完成，170/170 MATCH，receipt `B134.161-d9e69ba-playtest.json`（DEVELOP_ACTIVE）。stable/B133恢复包保留，main/Design未改；未启动游戏，native GC与内存结果仍待测。


## B134 native GC results

2026-09-29：用户提交9组18张原图，逐张读取；B134.161，Activity Monitor中同一Civilization VI进程PID35569。用户说明本次没有征服，所有城市没有生产目标，前几次长测也没有生产目标；前两回合未见明显增长后自行延长观察，并观察到多次右键后数秒进程内存回落约0.2–0.4GB。全城队列状态和每次延迟回落按用户陈述记录，不从单城截图推定全部城市。是否完整冷启动没有本次独立确认，图示T39作为本轮初始采样点。

原图已按原名移入外部证据目录`Specialization/Status/Validation/Evidence/B134_Manual_GC_Observation/`，18/18 SHA256一致，`manifest.json`关联本节；截图不进入Git。只有证据/Status更新，无源码、部署、GC策略或Gameplay改变。

### 原图读数

Lua数值是当前Gameplay调用范围的MiB，进程列是Activity Monitor显示的GB；二者口径不同，不能相减或视为本Mod独占。GC报告滚动显示最近3次，跨图重复行不重复计数。

| 组 / 截图时间 | 当前回合 | 进程GB | 本组新增GC：前 → 后 MiB | 本次减少MiB |
|---|---:|---:|---|---:|
| 1 / 18:33:49 |39|10.23|尚无样本|—|
| 2 / 18:33:57 |39|10.22|275.20 → 250.98|24.22|
| 3 / 18:34:27 |40|10.40|390.81 → 306.35|84.46|
| 4 / 18:34:54 |41|10.43|371.67 → 317.13|54.54|
| 5 / 18:35:32 |42|10.44|384.93 → 319.25|65.68|
| 6 / 18:36:30 |43|10.44|385.34 → 318.56|66.78|
| 7 / 18:37:57 |44|10.47|386.64 → 319.64|67.00|
| 8 / 18:38:35 |45|10.52|无新增，仍显示T42–44历史|—|
| 9 / 18:38:55 |45|10.40|第一次385.92 → 316.49；第二次317.76 → 251.51|69.43；66.25|

共8次不同的GC调用；最后一组包含同回合两次，不能描述为每回合严格一次的同条件序列。进程最后两图同回合20秒内10.52→10.40GB（−0.12GB），并非每次点击即时成对的进程前后值。用户观察到的约0.2–0.4GB延迟回落另记，截图没有逐次量化全部这些幅度。

### 已证明与尚不能推出的结论

- **USER_GAME_TEST_PASS（仅本次手动诊断调用/显示范围）**：8次均报告collect调用成功，count前后均下降；右键并非只查看，`P0Panel`实际发出`MEMORY_GC_COLLECT`，Gameplay在早期诊断分支执行前读→一次collect→立即后读。左键才是只读。3条是历史显示上限，不是最多只能执行3次；旧六回合观测窗口不限制手动GC。
- **可回收分配积累是本次增长的重要组成，已有直接证据**。T41–44回收后317.13/319.25/318.56/319.64MiB，T45第一次316.49MiB，没有沿用此前约47MiB/回合的持续增长。T45第二次进一步回到251.51MiB，距T39初始回收后250.98仅+0.53MiB。这不支持把此前回收前的全部增长解释成等量永久账本/可达状态膨胀；因此后续优先定位临时分配和重复事实构造，现有证据不足以要求清永久记录。
- **不是“六回合保留增长精确等于0.53MiB”或长期无泄漏证明**。初始与末尾调用次数、初始化/当时可达对象及宿主收尾状态未统一。第二次collect仍释放66.25MiB，也说明一次调用返回后的值不能无条件当作不可回收底线。终结处理、延迟释放/引用变化或宿主实现均是解释候选，未定位具体原因。
- **本次观察到进程回落与手动GC的时间关联**，与Lua直接下降相互支持；但报告不是本Mod独占计数，进程还包含非Lua部分。不能把所有0.2–0.4GB归给本Mod、声称GC立刻归还同量物理内存，或据延迟判断宿主具体分配器机制。
- **B134网络修复的原生收益仍未单独测出**。本轮无征服、反复手动GC，B133为3次征服且无手动GC；两项变量和代码同时变化，没有城市扫描/分配计数对照。不计算修复百分比，不将进程增长变慢全部归功于三事件过滤；其减少特定无关城市访问的证据仍为STATIC/LOCAL_SIMULATION。用户确认两轮均无生产目标，因此“队列空了”不是已建立的区别；无在建对象也不等于回合/总督/网络/城市事实读取停止。

### 原生环境与接口边界

截图环境串为`2013.2.0 r13768`，不能由此写成标准Lua5.3或测试环境lua55。`isrunning`前后均“未知”，说明可选状态读数未取得有效boolean，**不证明GC被停止**，也未原生验证运行状态前后一致。显示CPU耗时只有0.000/1.000秒（T39/40/41/43为1，其余为0）；保留原读数，但精度/宿主计时语义未证，不将其当精确性能测量、墙钟等待或零开销。原生collect已能返回并降低count；底层完整性/范围、第二次额外释放原因及进程回落机制仍TECHNICAL_INVESTIGATION_REQUIRED。

### 当前判断与停止点

最小GC采样任务已有足够材料，**不再要求重复本次长测或立即追加征服测试**。PT001/MEMORY_CAUSE_OPEN保留，但调查方向收敛到“可回收分配的产生量/生命周期，以及回收后是否另有保留增长”，不再仅凭回收前曲线判泄漏。本轮未授权常规每回合GC、GC调参、周期清缓存或账本清理；诊断不能直接升级为正式修复。

下一建议：沿已定位NetworkInput.Capture与LV2_GPP_DIRTY→ResearchCross直接路径，只读区分临时构造/重复事实读取与持久引用，连同原生GC接口证据判断最小下一方案；这是建议，未实施新优化。若以后确需对照，只设计保留DB/账本和完整请求生命周期的单一路径同档对照，另给窄计划，不立即要求用户补测。B132收益响应及B129认领验收保持，E2不结项、不进入F。


## B134 allocation follow-up — scoped investigation and next proposal

2026-09-29：用户授权按当前进度继续调查。本节为B134.161源码的只读定域审阅及进程外小探针；没有修改Mod/测试源码/Design，没有部署、启动游戏、增加runtime计数器或改变GC策略。B134截图的回收后趋稳仍是原生证据；以下调用/分配结构结论不冒充原生分配量归因。

### 1. 重复工作已落实到一个可隔离的入口

`Gameplay.lua:339–350`的`LV2_GPP_DIRTY`仅用`FactsChanged`门控Network/Housing，却无条件调用`ResearchCross.Audit`。`UI/GPPRefresh.lua:9,31–45`初始置true、成功提交后置false；worker/focus只标待处理，总督事件置true。**false并不只表示工人/焦点**，之后的普通回合/Load通知也可能为false；这条通道目前会重复Cross自己的回合/加载核对。

`ResearchCross.lua:33–60`及`ResearchCrossModel.lua:11–37`的实际输入是Identity/Potential/ACTIVE、学院锚点、区域完成/掠夺/引用及UI送来的六种BASE邻接值，不直接读worker/focus/population/Network/D。因此纯worker/focus通知具有优化依据，但**仅判断false仍不够安全**，见下文晚到资格核对边界；不能关闭整个GPP通知，也不能顺带删除其它consumer。

一次冗余Cross Audit会遍历本玩家所有城市；每城先读取11个退休载体和32个现行载体（43次存在性读取），创建43个逐载体记录表，再读fresh facts；合格科研城还枚举区域、建立替换映射/引用/区域行、匹配独立样本、生成Plan与yield明细副本，最后核对载体并替换plans/errors。见`ResearchCross.lua:14–26,64–95`。这些表是真实构造路径，不是由扫描计数猜出的分配字节；43是成功完成该检查时的记录行数，不能外推引擎内存大小或每回合执行频率。

必须保留的独立入口：

- `ResearchCross.lua:98–99`：新有效UI样本Receive→Audit；`UI/ResearchCrossRefresh.lua:44–58`覆盖区域/建筑/地块/资源/政策/研究/市政与turn/load。样本可在同回合多次真实改变，不因worker通知被过滤而停止。
- `ResearchCross.lua:123–134`：原生governor/district/turn/load/transfer/remove/建城，以及E2精确owned-carrier退出；正常投资/Claim显式刷新照旧。
- `ResearchCrossSample.lua:9–47`：owner/reference、generation/epoch/seq/turn及完整集合验证仍在signature比较之前；不能以“数值没变”跳过资格校验。UNKNOWN不能变0，确认失效仍撤销。
- `FactsChanged=true`保留用于总督及事实变化，`nil`/未知标记保留安全回退。不以只接受true取代“不等于false”。原生总督属性较晚更新的时序未在本探针证明。Cross直接回调若早于属性稳定，而后续BASE样本签名未变，Receive返回UNCHANGED不会再次Audit；现有较晚GPP回合/加载通知可能承担补核对。不能因独立入口存在就证明这一路回退可删。

### 2. 极小本地探针（LOCAL_SIMULATION_PASS）

使用现有Lupa Lua55，提取真实Gameplay GPP分派分支，并运行真实Cross producer/receiver/writer；只在内存给候选Cross条件增加`params.FactsChanged~=false`。两城fixture依次提交false→true→nil，不改仓库源码或历史测试断言。

| 项目 | B134当前代码 | 内存中的候选条件 |
|---|---:|---:|
| 第一次false的Cross调用 |1|0|
| 三请求Cross调用合计 |3|2|
| 载体存在性读取合计 |258|172|
| facts读取合计 |6|4|
| carrier写入 |0|0|

其余六consumer各3次、Network/Housing各1次保持不变。实际GPP UI入口确认初始true、worker/focus合并false、总督+worker合并true；独立样本在同回合BASE10→14，真实Receive→Audit分别得Science5→7。直接总督撤销/恢复、load generation及旧样本拒绝通过。此处只证明分派、读取及局部计算的本地行为，不是完整Civ VI请求/事件时序、内存字节、所有权全部回归或实机性能PASS。**单行guard不是建议直接实施的最终方案**：fixture先更新facts再触发事件，未覆盖上述原生晚到窗口。

探针保存在临时目录（非长期项目依赖），从本轮已执行脚本忠实恢复后复跑输出一致。在develop仓库根目录执行：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python python3 /tmp/spc_b134_cross_current_probe.py`及`/tmp/spc_b134_cross_guard_probe.py`。SHA256分别为`d8ce2aca7c8aba624b531c049d3bb5587b6a131bf2ed10f1f0d004d539ae62ff`、`6852998b191fd16dd3186e4506a251b00cec610bc53b574363e6bd1815aa59d9`。正式实施需把相关定向验证放入现有测试体系；不依赖/tmp永久存在。

### 3. 网络与事实链：临时构造和长期持有分开

| 路径 | 已确认的构造与持有 | 判断 |
|---|---|---|
| NetworkBridge Refresh | `:135–143`先Capture，再判signature；同值新input不发布；`:65–78,190–232`只留当前input/view及至多一个candidate | 重复临时构造成立，未见此链逐事件追加完整历史 |
| NetworkInput Capture/Signature | `:11–18,23–66`每城事实/引用、每路线端点引用、排序数组、格式化和串接；同值仍发生 | 可优化构造；签名一样不代表事前可以跳过事实读取 |
| EffectiveFacts | `:26–45`校验anchor/first副本、投资去重表、最终facts副本；`Probe.CityRoleFacts:315–363`额外role表/keys/values，仅取总督资格 | 多份短命对象；需保留输入非修改/当前资格合同 |
| 现代Game进度 | `CityProgressionStore:143–149,614–637,670–677`按城市持有记录，Base/Investment读返回副本；`:592,736–754`定位/Check不重新读取整份Game账本 | 普通facts读不是每次重载/克隆全城永久账本；不建议为此清保存记录 |
| Cross results/samples | plans/errors每玩家替换；samples保留最新完整批，最多512行；同signature更新turn | 当前快照有必要保留；未见此链逐回合保留所有旧批 |
| 手动GC诊断 | `PerformanceCounters:116–165`最多3个标量结果、一个报告；`P0Panel:83,165–173`GC共用一个阅读槽、单个pending token；请求直接早退Gameplay | 不按点击次数积累GC历史；报告字符串有临时构造，不是已证的大型历史堆积 |

仍有一项小的独立保留边界：`NetworkBridge:326,355–365`明细翻页按`player:cityID`保存一条签名，普通摘要清该城条目，未见独立失城清理。它由实际点击明细的不同城市数增长，不是无人操作每回合增长的解释；记录为后续局部诊断生命周期维护，不混入本次主要修复。

不能直接用“本回合已看过”或路线revision不变来跳过Network Capture：同回合总督/投资/Claim/首都/多城源资格可变。现有UNKNOWN同reference暂保留、确认失城/路线失效独立撤销和load epoch必须继续有效。也不把私有网络view直接借给会修改结果的consumer。

### 4. 哪些优化现在值得做，哪些保留

**首选下一最小段：在现有GPP通知内明确纯worker/focus来源，再定域跳过Cross**，预计只涉及`UI/GPPRefresh.lua`与`Gameplay.lua`两处运行入口。沿用现有请求、合并和有限重试，不建立新调度器：

1. 使用一个明确来源标记，仅在全部待处理原因都是已知本玩家worker/focus时允许跳过Cross；初始化、turn/load、governor、缺失/非法owner、混合原因全部保持完整核对。合并原因只可变得更保守，不能被后来的worker事件覆盖；失败重试与发送中到达的新原因同样保留。
2. Gameplay仅在该标记明确成立、且FactsChanged明确false时跳过；旧调用者无标记、矛盾标记、nil/未知仍执行。其它六consumer、Network/Housing条件不动。不以把所有turn/load的FactsChanged改true来规避问题，否则会额外唤醒Network/Housing。
3. 保留Cross独立sample/真实事实变化/turn/load/退出及投资/Claim刷新。没有跨回合缓存、每城市每回合一次门槛、GC变化或永久状态变化。新增标记只是现有通知的定域原因，不是新的玩法合同。

预期减少的是**纯worker/focus这一路**的多余Audit、城市访问、43项载体预检及事实/区域/Plan构造，回合兜底明确不计入预计降幅。上述258→172来自更宽的单行实验，只证明路径成本，不能冒充最终两处方案已通过。实施时验证纯worker/focus、混合/Gov/turn/load、未知owner/旧请求、重试及发送中合并、其它consumer不变、同回合两次新样本、UNKNOWN/退出/返回/Claim/load；不扩大到全玩法历史回归。若实施后需原生确认，合并一次最小同回合收益响应，不重新长测。

低优先级、可另做：NetworkInput.Signature在单次调用内复用一个八字段数组（每城覆盖全部字段），保持排序、atom及最终字节完全相同；以及只读比较用的`anchor.first`不做额外clone。这些只减构造，保留全部事实检查，收益尚未量化，不应包装成主要内存修复。

不纳入首选段：把`EffectiveFacts out=clone(f)`直接改`out=f`。当前生产SupportFacts返回独立副本，但旧`test_effective_facts.py:12–18`明确检查借入foundation不被修改，mock也返回固定f。直接改会改变非修改边界；应先明确值所有权并验证真实Flow/Store隔离，不能为了少分配悄悄改合同或放宽断言。

### 5. GC接口证据与停止点

[Lua5.1官方接口](https://www.lua.org/manual/5.1/manual.html#pdf-collectgarbage)未定义isrunning，[Lua5.2](https://www.lua.org/manual/5.2/manual.html#pdf-collectgarbage)才列出该选项。因此“未知”可以是接口差异，不能据此认定自动GC停止；本机`2013.2.0 r13768`仍不映射为这些标准版本。公开Civ VI社区扩展的[HavokScript源码](https://github.com/Wild-W/CivilizationVI_CommunityExtension/blob/master/HavokScript.cpp)从Windows DLL导入接口，只是该项目的实现证据，未给出本机macOS构建的GC策略/第二次额外释放语义。没有据外部资料确认引擎具体回收预算。setpause/setstepmul是修改操作，不能当无副作用查询来探测默认值；本次未调用。

调查结论：已经有足够依据提出上述**纯worker/focus通知定域消除**，不用等所有内存来源完全归因。与此同时，回收后的微小保留增长及宿主GC行为仍未关闭。当前仅调查/方案记录完成，等待该最小段实施授权；无新用户测试、无自动GC/缓存清理/永久账本删除，也不进入其它玩法批次。


## B135.162 — authorized pure worker notification scope

2026-09-29用户明确“授权修复”，实施上节两入口保守方案。不是扩大单行FactsChanged门控，也不修改GC策略、Gameplay/Design或推进其它P0。W0004按L2定向验证，并覆盖直接相关的通知顺序/失败边界；不运行全历史或大规模stress。

### 实现与保留边界

- `UI/GPPRefresh.lua`在原待处理批次上增加一个瞬时`WorkerOnly`原因位。仅全部原因均为已知本玩家worker/focus时为true；初始化、总督、turn/load、UNKNOWN或混合均false。本地/外方判断要求非负整数；不猜player0。现有source观测标签没有改写，非法正小数等仍可能被旧标签记成foreign，但实际路由保守处理，不以该标签作为过滤权威。
- 发送前摘出FactsChanged/WorkerOnly快照，清空待处理原因以接纳同步回入；成功不清新批次，失败将旧原因OR FactsChanged / AND WorkerOnly合回。无新事件连续失败仍最多3次；真实新事件沿用原重试恢复。修复原成功发送后可能吞掉回入总督FactsChanged的窗口。
- 同回合turn/load去重仍保留；已有pending时降为保守，发送中到达时保留下一批。没有把所有turn/load的FactsChanged强制true，没有新增轮询、每帧事实扫描或hover请求。
- `Gameplay.lua`只在`WorkerOnly == true AND FactsChanged == false`时跳过这一条`ResearchCross.Audit`。缺失/错误类型/矛盾标记继续检查，其它六consumer及Network/Housing条件不变。Cross独立采样、当前资格、原生事件、投资/Claim刷新和精确退出均不动。
- 版本标记升B135.162/modinfo162。无新增carrier、Property、保存schema、计数器、账本清理或Network Capture优化。GC手动诊断仍仅明确右键触发，不转为自动回收。

### 验证（STATIC_CONFIRMED / LOCAL_SIMULATION_PASS）

新增`DevelopmentTests/test_b135_gpp_scope.py`；命令：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python python3 DevelopmentTests/test_b135_gpp_scope.py`。需要Lupa lua55及Git基线d26f3f9；只复用旧Cross fixture声明，不执行旧压力/DB/版本wrapper。

| 定向场景 | 结果 |
|---|---|
| 非零本玩家ID、纯worker/focus合并、外方、nil/字符串/负数/小数/NaN/∞ | 已知纯本地才skip，未知保守；空闲/关闭无发送 |
| worker与总督/未知/turn/load双向合并、同回合重复通知 | 保守原因不被覆盖，turn/load不额外唤醒Network/Housing |
| 发送中同步回入，两方向成功/失败、三次失败后真实事件恢复 | 新原因保留，失败批次合回，不递归发送 |
| 真实Gameplay分支与B134的10种请求形状对照 | 只有精确true/false组合少一次Cross；其它consumer调用相同 |
| 两城真实Cross writer fixture | 纯worker批次0次Audit/城市访问/载体预检/facts读；保守批次仍1 Audit、2城市、86载体预检、2facts读；同值无写入 |
| 同回合独立BASE10→14；UNKNOWN；总督退出/恢复 | Science5→7仍及时更新；UNKNOWN不误清；资格按当前事实重算 |
| 原生回调先到、BASE样本UNCHANGED、资格后到的模拟 | 较晚保守GPP通知仍重新核对，未丢失fallback |
| load generation / 当前reference变更 | 旧样本拒绝；不靠旧snapshot重放 |
| 精确文件diff、Lua编译、modinfo文件集 | 只有两入口+版本标记变化；其它action分支字节一致 |

E2退出/返回/Claim、Network、GC及永久writer未变，继承既有具名证据；**未重新执行整套E2或宣称其全部实机PASS**。静态diff与模拟不证明Civ VI宿主事件顺序和内存下降幅度。预期减少的是纯worker/focus路径的完整Cross Audit及对应城市访问/短命对象构造，保留turn/load检查，不把每回合总扫描下降作为已证明结果。

### 最小用户验证与停止点

待部署后，可在已有科研III/IV城同一回合增减工作专家、切换焦点，确认专家相关收益正常响应、跨学科研究效果没有丢失；正常过1回合确认仍正常。若当前局面方便改变一个合格区域的BASE邻接，可顺手确认学院跨学科收益更新；不要求另造测试城市或为此解锁政策。GC不需要点击，无需征服、再做长测或重复已完成的GC基线测试。异常时停止并提交该城收益/跨学科报告即可。

原生响应与实际分配/进程改善仍USER_GAME_TEST_REQUIRED；PT001 MEMORY_CAUSE_OPEN保留。Network重复Capture和其它构造候选仍后置，不自动继续下一优化或F。部署结果只按实际receipt记录于Status/Authority。


## B135 native worker and GC results

2026-09-29：用户反馈“收益正常”，学院增加建筑/槽位并派专家后进程增长，随后无新操作/在建目标地过数回合仍增长，最后手动GC明显回落。已逐张查看6组12张原图。按持续授权归档至外部`Specialization/Status/Validation/Evidence/B135_Worker_Response_Memory/`，保留原文件名；`manifest.json`登记对应组/类型/bytes/SHA256，移动前后12/12一致，收件箱目录保留。原图不进入Git。

### 本次实际观察

所有进程图均为Civilization VI PID40775，保留活动监视器原始GB单位；Lua诊断用MiB，两者不是同一统计口径。

| 组 / 图片时间 | 游戏回合与可见状态 | Civilization VI进程 | Lua手动GC |
|---|---|---:|---|
| 1 / 19:07:50 | T39；按用户说明已完成图书馆，并非测试前起点；所选Aberdeen无生产目标 |10.28 GB|未显示 |
| 2 / 19:08:34 | T39；学院tooltip列图书馆/大学/实验室，4公民工作；专家20科技/12生产/12食物，所选城无生产目标 |10.38 GB|未显示 |
| 3 / 19:09:07 | T40；用户说明后续只过回合，无新建造/操作 |10.58 GB|未显示 |
| 4 / 19:09:28 | T41 |10.67 GB|未显示 |
| 5 / 19:09:53 | T42，GC前 |10.69 GB|未显示 |
| 6 / 19:10:06 | 仍T42；报告明确P0-B-135.162，一条完整GC调用成功记录 |10.38 GB|618.63 → 298.57 MiB |

最后GC释放读数差320.06MiB（回收前读数约51.74%）；两张T42进程截图相隔13秒，读数减少0.31GB，回到组2所见10.38GB。本机Lua环境仍`2013.2.0 r13768`，GC状态未知→未知，显示CPU耗时1.000秒；不将此计时当精确耗时或将未知当GC停止。

### 接受范围与判断

- **USER_GAME_TEST_PASS（用户实机所述范围）**：学院建筑/槽位增加后专家收益正常，随后能正常过回合。本次收益响应待办关闭。组2直接显示4专家的20S/12P/12F。没有跨学科研究明细或明确科研III资格/独立BASE变化对照，不能扩大成所有Cross分支/公式/资格切换原生PASS；也没有证明这批原生通知的WorkerOnly实际比例。
- **MEMORY_CAUSE_OPEN**：组2→5三回合进程10.38→10.69GB，持续增长仍在。B135只减少已确认纯worker/focus的Cross冗余入口，并未消除其它consumer、回合/加载/资格检查、独立样本或Network Capture。本轮不记“内存修复PASS”，也不由进程曲线认定这一路优化无效。
- GC前后Lua读数下降及同期进程回落，再次直接支持大量可回收分配积累。所测进程增长可以明显回落，优先继续调查重复构造/短命对象，而非删除永久账本。它不证明全部增长来自本Mod、所有旧对象都已清空、自动GC未运行或长期无泄漏；单次collect后298.57MiB也不是已证的不可回收底线。
- 组1→2只能记同回合+0.10GB，不能细分图书馆/大学/实验室/每专家各自的开销。起始和各操作间截图缺失，操作方法未独立确认；没有各回合Lua或扫描统计，不能分配到某consumer。最终进程比组1仍高0.10GB不是永久泄漏量。本轮与B134的建筑/专家/采样状态不同，不把298.57与先前250.98等值直接相减当保留增长。

本次不要求补起始截图、重做长测或再点击GC。未修改Mod、Design、GC策略，没有部署/启动游戏；收益已接受不等于性能问题关闭。

### 有界本地后续定位（LOCAL_SIMULATION_PASS）

复核当前`NetworkBridge.Refresh`先完整`NetworkInput.Capture`后比较signature。同路线`Receive`在内部pcall函数提前return后，外层仍调用Refresh。这条路径已在前次调查指出，本次用实际Bridge/Input验证调用与引用生命周期，不以扫描数猜分配字节。

仅在/tmp建立`spc_b135_network_allocation_probe.py`（SHA256 `98a51f3a791938c1b4992c071fa42b5b0a0385617e7bbde4f3ff63b991a0cbee`）。命令：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python python3 /tmp/spc_b135_network_allocation_probe.py`。复用`test_arch_v2_batch_a.py`的FIXTURE字面量，不执行历史suite；每案独立Lua55解释器、2城市，零路线/一条路线各一组，无DB或运行包操作。临时文件不是未来任务的永久依赖，结果及限制在本节保留。

| 操作（零/一条路线结果相同） | Capture | facts fixture调用 | city_scan | derive / 新发布 |
|---|---:|---:|---:|---:|
| 重复Refresh 20次 |20|40|40|0 / 0 |
| 同路线新序号Receive 20次 |20|40|40|0 / 0 |
| 20组三种Current查询（共60次） |0|0|0|0 / 0 |
| 同回合ACTIVE3→4，再同路线Receive一次 |1|2|2|1 / 1 |

重复Refresh/Receive各产生20次input_duplicate；同路线Receive另有20次same_snapshot。三种查询为CurrentNational/CurrentConnectedKinds/CurrentRecipientSources，60次cache hit；不把它们等同会调用Refresh的旧National等入口。各案Property写入0。

弱引用跟踪：重复采集案含初始化共21个Capture输出根；本地显式回收后仅当前1根及它包含的4张表存活（根/cities/两城记录），旧20根消失；Current查询返回副本的被追踪表全部回收；无candidate残留。ACTIVE变化案也只留新当前根。这只证明所测输出未逐次留历史，同时确有重复事实采集/临时构造。

限制：EffectiveFacts和原生getter是mock，40次调用不是其实际分配量；弱引用未覆盖内部临时字符串/数组、私有派生view或原生内存。两次显式GC仅在进程外Lua55运行，未改变Civ VI。没有原生调用频率、MiB/回合、总内存归因或整体无泄漏结论。Bridge/Input源码SHA256分别为`1b1f3aa8dcb5321c13892cff0e3f5ed9a864736a4e2ba09ae4c90aa2ba8fd94c`、`e58e71de37a464e1d14a1a0facd00248054037bd908305d8f5f27ec02690379a`。

下一建议：沿Network Capture→实际EffectiveFacts/总督事实链确认哪些临时副本可避免，同时保留同回合真实变化、UNKNOWN、ownership及load。**不能直接因路线相同就跳过Capture**，上表最后一案已显示该路径仍负责发现资格变化。当前只完成证据/只读定位，未授权或实施新优化；不把手动GC转为自动补丁，不进入其它P0或F。


## B135 follow-up — fresh governor facts with less temporary construction

2026-09-29：用户授权推进上节的定向调查/窄方案，并询问GC为何不依赖分配来源定位也能回收。本轮仅在进程外Lua中比较候选，正式源码仍B135.162；以下为下一实施提案，不是已上线修复。未改Design、永久记录、运行包或GC策略，不派发重复长测。

### GC解释与证据边界

GC判断对象是否仍可通过程序引用访问；归因调查要判断哪个调用分配了它，两者所需信息不同。中间表/字符串失去引用后，即使诊断没有记录创建者，收集器仍可回收；被缓存/账本持续引用的对象不会因此消失。普通Lua采用自动回收，完整collect请求完成一个回收周期；增量回收则分摊工作。依据：[Lua 5.1内存管理](https://www.lua.org/manual/5.1/manual.html#2.10)、[collectgarbage接口](https://www.lua.org/manual/5.1/manual.html#pdf-collectgarbage)。这说明通用原理，不证明Civ VI内嵌`2013.2.0 r13768`的具体自动调度、参数或Lua版本等同该手册。

当前[诊断实现](../../../Mod/PerformanceCounters.lua)只在明确手动请求时保护调用collect；不停止/重启GC、不调参数、不清Property/永久账本/缓存。B135的618.63→298.57MiB显示当时至少有显著可回收分配；不是本Mod独占计量，不能证明全部增长来自本Mod、不存在仍被引用的增长，或自动GC没有运行。进程内存另含引擎/原生资源；Lua回收与OS显示下降不要求一一对应。手动完整回收可能集中造成停顿，因此保留诊断用途，不据有效就自动每回合执行。

### 已核对的实际链路与候选

Network Capture每次需要当前资格；相同路线也可能对应同回合不同ACTIVE，上节反例仍有效。[NetworkInput](../../../Mod/NetworkInput.lua)→[EffectiveFacts](../../../Mod/EffectiveFacts.lua)在Potential>1时调用[Probe.CityRoleFacts](../../../Mod/Probe.lua)，目前同时构造完整角色诊断。EffectiveFacts实际上只消费owner、cityID、governorGateStatus、governorLevelCeiling。

建议下一批只做：

1. Probe抽出一份共用的六属性总督判定逻辑，增加返回上述四项标量的窄读取入口。EffectiveFacts走该入口；CityRoleFacts/FocusProbe继续保留完整诊断及现有输出，二者共用判定逻辑，不复制两套规则。
2. EffectiveFacts的投资anchor只读比较借用`f.first`，省去该处深拷贝；保留anchor容器、精确键集递归比较和全部验证。最终输出`out=clone(f)`及嵌套隔离继续保留，不能把借入foundation直接返回或修改。

| 口径 | 预期变化 | 明确保留 |
|---|---|---|
| 身份校验通过、进入六属性判定的Potential>1读取 | 少role/keys/values三张临时表及cityKey拼接；六属性判定不建临时数组 | 六个总督Property每次fresh读取，P.Call错误保护、玩家资格/城市身份及UNKNOWN一致性判定 |
| 首都可正常读取的该路径 | 少5次无关诊断getter：旧legacy字段、GetCities、GetCapitalCity、capital GetID/GetOwner | 各种失败/缺失场景按实际路径计数，不能统一宣称每次都少5次 |
| 存在投资ledger时 | 少anchor.first深拷贝（若有嵌套则包含其副本） | receipt去重表、pending/revision检查、Store副本及最终facts深拷贝 |
| 事件、扫描、发布、写入 | 不以减少这些次数作为本批收益 | 同回合真实变化、Network freshness/UNKNOWN/owner/load、退出/返回/Claim不改 |

这是已识别的无用构造，值得按窄范围实施；尚不能量化MiB/回合，也不能宣称它是截图中全部增长的来源。CityFlow/Store内部其它复制未由本轮探针量化。Signature临时数组微优化、跨调用事实缓存、一次/城/回合限流、相同路线直接跳Capture、周期GC均不纳入此提案。

### 最小进程外候选验证

`/tmp/spc_b135_facts_candidate_probe.py`，SHA256 `bf94988ed01bc6c27a7e2a3e8c58402bf69d0738423b246419b9bc4b98e4780c`；命令：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python python3 /tmp/spc_b135_facts_candidate_probe.py`。脚本读取真实Probe/EffectiveFacts，在内存文本中替换候选后分别载入Lua55；不修改仓库模块。临时脚本不是未来恢复必需材料；本节保留结果、候选边界与复现条件。

**LOCAL_SIMULATION_PASS：774个对照检查点**，不是stress或实机性能测试：

- 729种六属性nil/0/1组合：旧/候选CityRoleFacts完整诊断、EffectiveFacts结果或错误一致。
- 24种非法类型/值或getter失败；9种owner/id/ledger错误；输入foundation/ledger不被修改、返回嵌套副本隔离。
- 同一实例连续KNOWN4→KNOWN1→UNKNOWN→KNOWN3→foreign拒绝→original立即ACTIVE3，共6点，无跨次缓存。
- first额外键/缺失/改值/嵌套缺失，以及foundation first异常，共6种一致拒绝；不弱化投资身份比较。
- fixture正常首都路径验证上述5个getter省去；六个总督Property各仍读取1次。

源码基线SHA256：Probe `586ecccca14aa9346dcdc50b8ffc6ece0bb80856a5d90d9847d37982b7032c38`；EffectiveFacts `ebf8eaa6a60dc6c5c13211553bbacafbe969d939fff2784923c92a675e086faf`。原生getter、foundation/ledger由fixture提供；未集成全Store/Network/真实事件顺序，未测原生分配字节、耗时或进程内存收益。所述三表减少另有代码结构依据，不把getter次数换算为字节。

### 下一实施范围与验收门槛（待授权）

- 正式行为修改限Probe/EffectiveFacts；必要版本标记、定向测试及现有文档/index同步随批次进行。不改Network生命周期或任何writer/保存schema。
- EffectiveFacts扇出涉及普通收益consumer、投资/进度读取、NetworkInput、CurrentSpecializationFacts及诊断。输出字段/错误/副本合同必须不变；正式实施再核对实际直接调用点并做相应定向回归，不把本轮fixture称为全部consumer已验收。
- 已发现9份测试引用CityRoleFacts，包括E2/recapture/transition的总督mock。实际选用fixture须改接新窄入口或真实六属性，保留原断言；不要在runtime加静默旧mock fallback，也不为本批全改历史wrapper。
- 按W0004针对共享资格读取选择L3相关验证：新增入口差分、P0/P1/P2–P4、正常/损坏投资记录、输入非修改及输出隔离；实际Network同路线同回合ACTIVE改变、临时UNKNOWN、ownership/reload引用边界；选定E2投资/退出/返回回归。只运行相关路径，不做全历史或泛化stress。
- 完成定义：行为/拒绝条件不变、上述临时构造和无关读取确实移除；没有新跨事件缓存、持久写入或自动GC。回滚只还原本批读取路径，无保存格式迁移。若无法保持未知/损坏记录语义则停止该优化，不降低保护。
- 本轮用户测试：无。正式实施后若需要原生复核，限制为一座已有Potential>1城的当前总督门槛/收益响应，合并正常验证；不要求重复内存长测。原生性能仍以实际后续证据判断，不用模拟宣告内存已修复。

本轮停止点：提案与本地候选证据已准备，等待该窄实现授权。B135既有验收有效；MEMORY_CAUSE_OPEN保留，不自动进入其它P0/F。


## B136.163 — authorized fresh governor facts optimization

2026-09-29：用户明确授权实施上一节两项窄优化。正式源码B136.163/modinfo163；本地验证完成，原生收益/内存影响未据此升级为PASS。Design D0035/A0161及玩法/保存合同不变。

### 实际修改与兼容边界

- [Probe](../../../Mod/Probe.lua)：共用六属性判定器；新的GovernorGate返回owner/cityID/status/ceiling四标量。每次仍fresh读取六属性，保留nil/0/1、getter失败、control缺失及不一致状态；没有跨调用缓存。CityRoleFacts/FocusProbe仍提供原有完整诊断。
- [EffectiveFacts](../../../Mod/EffectiveFacts.lua)：Potential>1走窄总督入口；投资anchor.first仅在只读精确比较中借用。最终facts深拷贝、receipt去重、pending/revision/身份验证均保留。
- modinfo只升163及说明文字，Probe标记B136.163；UUID/文件集合不变。没有UI/Data/Network/GC/退出writer/永久保存格式改动。

STATIC_CONFIRMED（代码证据）：合格Potential>1事实读取不再构造role/keys/values三表、cityKey字符串及局部prop闭包；正常首都可读路径少5次无关诊断getter。存在ledger时省anchor.first深拷贝。六属性仍每次读取，城市扫描、事件、发布与写入次数没有因此被限制；没有每城每回合一次或同路线跳检查。

精确调用审阅覆盖EffectiveFacts.Read的26处源码调用点/21文件（包含薄封装及历史入口，不等于26个当前活动consumer）：投资/进度/继承、普通收益consumer、Gameplay诊断、RuntimeWork、CurrentSpecializationFacts、NetworkInput和Dialogue UI。没有调用方依赖旧gate表；UNKNOWN与throw仍分别处理。RuntimeWork批内共享最终facts、CurrentSpecializationFacts再clone first、InvestmentAction复制自身anchor、NetworkInput仅相同reference暂时hold均不变。Store返回历史投资anchor与当前城市first的投影也经测试核对，不把省拷贝扩展到Store或最终输出。

### 定向验证与证据范围

W0004 L3仅针对共享资格与保存消费者，未跑全历史/泛化stress/DB或启动游戏。当前执行环境：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14`；需Lupa lua55及本仓库Git34b92cc。无需外部游戏数据库。

| 检查 | 结果与边界 |
|---|---|
| [test_b136_facts.py](../../../DevelopmentTests/test_b136_facts.py) | **847检查点LOCAL_SIMULATION_PASS**（本地模拟，不是实机）：真实新旧Probe/EffectiveFacts、完整Role/Focus诊断、六属性729组合及24异常、P0–P4/pending/坏ledger/输入隔离；含15个真实NetworkInput/Bridge同回合、UNKNOWN、owner、reference、load/旧epoch对照。原生getter、Flow/ledger/Store读取为fixture |
| 六属性与getter口径 | 729+24案每次六属性各读一次；正常首都路径仅少约定5getter，其余getter计数相同。三表/闭包减少由代码结构确认，不换算字节或耗时 |
| [test_b136_progression.py](../../../DevelopmentTests/test_b136_progression.py)旧adapter集成 | 只借旧fixture声明，实际当前模块：四专业P1/P2/P4共12组import/read/boot；投资P2→3、重复确认、三处写失败恢复；四专业退出/foreign hydration/缺token严序返回、当前总督/继续投资/boot；错误hydration、中途读档、退出失败仍HELD。此部分明确使用StartLegacyTest，不冒充新V3全生命周期 |
| 同一runner正式V3 | 另一个Lua实例运行正式Start：单城P2，当前总督1→UNKNOWN→4、输出修改不影响authority、boot不增写且记录逐值保留。不是所有V3生命周期或原生冷加载认证 |
| 语法/包/定域 | 两模块Lua语法、modinfo163精确170文件集合通过；Mod差异只Probe/EffectiveFacts/modinfo。其它源码字节与34b92cc一致 |

9份旧测试的CityRoleFacts引用已分类：两份真实诊断测试无需更改；其余被选用的mock在新runner中明确接真实六属性/GovernorGate，原断言不因优化被弱化。旧测试文件没有修改，runtime没有测试兼容fallback。未重跑的精确carrier清单/DB、Claim全套、B135通知响应等继承各自既有证据，不报告本轮全量重新PASS。

独立只读复核未发现语义/副本/调用方不兼容。GC诊断默认关闭且仍只有手动请求；本批没有collect、回收调参、清账本或新增计数器。内存根因继续MEMORY_CAUSE_OPEN：确认减少了所述构造，尚无原生MiB/回合收益量化。

### 最小原生确认与停止点

不派发重复长测。下次正常验证顺带用一座已有Potential>1城：确认包标记B136.163；调离总督时ACTIVE回到1而Potential/收据保留；总督重新建立且满足门槛后，ACTIVE和已有收益按当前资格恢复。无需再次征服、投资、手动GC或重复专门内存长测。若异常则保留报告停止，不猜测补历史。

代码回滚可从B135 Git提交/运行包恢复本批读取路径，未新增保存格式；实际运行包切换仍使用既有receipt与安全恢复流程。部署状态以Status/Authority及外部receipt为准，源码提交不等于已部署。完成本批后停止，不进入F或其它玩法。

部署记录：B136.163已按W0003完成安全切换，source `3b31173`，receipt `B136.163-3b31173-playtest.json` 为DEVELOP_ACTIVE；运行包与源码170/170 MATCH，digest `1a33f0fc4c3f46895de938084130600e6e520dfc51f90673000f8078e5906dbf`。两次切换前均由OS只读进程检查确认游戏退出，未启动游戏。B135完整包及stable恢复点保留，无pending transaction；main保持B069.96。原生确认仍待用户正常验证。


### B136 native governor response and memory results

2026-09-29：用户反馈“内存依旧增长，总督调离后报告可以确认ACTIVE回到1，新总督建立后能力恢复”。逐张查看四组八张原图，并按持续授权移动到外部`Specialization/Status/Validation/Evidence/B136_Governor_Response_Memory/`，保留原名；`manifest.json`记录组别、角色、bytes及SHA256，移动前后8/8一致。截图原件不进入Git。

| 组 / 截图时间 | 游戏回合 | Civilization VI进程内存（Activity Monitor） |
|---|---:|---:|
| 1 / 19:52:04 | 39 | 10.21 GB |
| 2 / 19:53:53 | 40 | 10.60 GB |
| 3 / 19:54:36 | 41 | 10.66 GB |
| 4 / 19:55:59 | 42 | 10.79 GB |

四张进程图PID均为46101；T39→42观察值增加0.58 GB。游戏图未展示完整专业诊断、build标记或Lua/GC读数；本次包关联依据上一节已验证部署及用户在B136测试后的反馈，不能称为截图独立确认版本。组3可见选中ABERDEEN (TEST)、科研2级入口和“没有生产任何东西”，不据此推断全过程操作、所有城市队列或具体总督切换时刻。

- **USER_GAME_TEST_PASS**（用户实机所述场景）：总督调离后ACTIVE回1，新总督建立后能力恢复；关闭B136最小总督响应待办。此结果依据用户明确确认，不冒充截图中已逐字段读取；Potential/收据逐值、Network、四专业全覆盖、ownership及save/load未由本次重新验收。
- **MEMORY_CAUSE_OPEN**：持续增长仍在，B136不能记为内存修复PASS。已有代码证据中的无用构造减少仍有效，但本批既不能证明实机增长率改善，也不能由进程曲线断言优化没有任何作用。无本次Lua回收前后数据，不能区分新增临时对象与持续保留，不能把0.58 GB归给本Mod或特定consumer；不要求补图或重复长测。
- 下一建议（未授权实施）：沿已确认的Network Capture→EffectiveFacts→CityFlow/Store路径，定域检查剩余副本的必要隔离与重复构造，先形成可证实的窄调查/对照方案。相同路线不能跳过当前资格采集；同回合ACTIVE变化反证保留。不得为降低计数牺牲UNKNOWN/owner/load语义，或将手动GC转为周期策略。当前只归档结果，不修改源码、不部署、不进入F。


## B136 follow-up — remaining copies and retained generations

2026-09-29：用户授权继续调查。基线Git `685ab30` / B136.163；本轮只读直接实现、运行进程外定向实验并记录发现。没有改Mod、Design、引擎GC策略或部署，没有重新派发用户长测。B136总督响应PASS及MEMORY_CAUSE_OPEN均保留。

### 实际读取与保留边界

1. [CityFlowProbe.SupportFacts](../../../Mod/CityFlowProbe.lua)正式V3路径直接进入[CityProgressionStore.Base/Investment](../../../Mod/CityProgressionStore.lua)。每次按positions索引定位，不重新load或深拷贝全国账本。普通成功的[EffectiveFacts.Read](../../../Mod/EffectiveFacts.lua)共4次索引查找，Base/Investment分别执行当前身份检查（两张临时reference表），分别复制base/ledger，再复制最终facts。两次TOKEN读取及每次fresh总督门槛保留；不能把这些检查简单压为每城每回合一次。
2. Store每城稳定保有envelope中的已确认记录和worker私有root。两份承担不同职责：root在可能发生引擎回调前推进，envelope在写入/readback成功后推进；普通Read不追加记录版本。实际新增城市或合法永久成果增长是保存合同，不因内存调查删除。合并双副本、借出永久记录、直接把输入作为输出均不列为安全小修。
3. [NetworkInput.Capture](../../../Mod/NetworkInput.lua)对各城读取facts，随后只保留8项标量的网络投影，不保存完整first/投资账本。[NetworkBridge](../../../Mod/NetworkBridge.lua)每玩家只有当前input、private view和当前兼容投影；相同signature不重建view。Current查询不Capture；Refresh及旧fresh查询仍会采集。相同路线也必须发现同回合ACTIVE变化，不能用路线相同跳过事实采集。

以上为STATIC_CONFIRMED（直接代码证据），不等于已找到真实增长来源。

### 实际V3副本的定向回收实验

临时脚本`/tmp/spc_b136_store_allocation_probe.py`，SHA256 `42d4833a90e62295f1590936e9a27f18ace3ca78d4b368ff5043fd0c0394509d`。读取实际Probe/CityIdentityRead/CityProgressionStore/CityFlowProbe/EffectiveFacts/InvestmentAction模块；从现有E1/E2/B108测试仅提取fixture声明，使用正式Store.Start，未执行旧wrapper或规模测试。环境命令：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 /tmp/spc_b136_store_allocation_probe.py`。脚本为临时调查材料；本节保留复现来源、方法、结果和边界，不成为新增runtime诊断体系。

方法：在worker捕获Copy函数前包装M.Copy，仅弱引用追踪返回表和嵌套表；也追踪最终facts。每档20次读取，释放返回值后只在独立Lua55进程做两次完整GC；游戏未运行这些操作、未停GC或修改参数。原生对象/GetProperty为fixture，并非Civ VI实现。

| Potential | 20次读取中的Store表复制调用 | 空ledger Copy(nil) | 追踪到的复制/最终输出表总数 | 完整回收后追踪表存活 |
|---|---:|---:|---:|---:|
| 0 | 20 | 20 | 40 | 0 |
| 1 | 20 | 20 | 80 | 0 |
| 2 | 40 | 0 | 160 | 0 |
| 4 | 40 | 0 | 160 | 0 |

这是所测普通自建城、无额外嵌套first的输出表口径，**不是总分配量**；不含Copy内部seen、临时reference/anchor/去重表、字符串、闭包和原生内存。fixture的TOKEN getter另有每档40次标量Copy，单独计数，不能冒充原生Property开销。输出丢弃后全释放；有意只保留最后一份facts时只留其root+first两表，释放后为0。记录逐值及写入计数保持不变；同一实例总督1→UNKNOWN→4即时响应，未产生额外永久写入。

另以真实两次投资替换记录，通过debug仅取得弱引用观察三代worker root/envelope：前两代均0/0存活，最新一代13/13表存活。说明本fixture中旧版本没有持续挂住；不等于所有ownership/失败/存档或原生Property资源均已验证。

源码SHA256：CityIdentityRead `93f34ee2da9f16c0455ac6a4b9e9c5ab750ed06673e8b924f6f3d202cb601e7c`；CityProgressionStore `573298ba2824cea1d785c2375b1965d374e5f657b336f9d09fa7b63d7d87bd0a`；CityFlowProbe `fafc371fb55c64763025a43ffcf46b91d4c76b44f831eff0092faa57d9961a99`；EffectiveFacts `969b4ab656c6cb59de0d343438d3d0c42eb9a563f6ed96353ebbe9b81ef4283d`。

### Network private view补充实验

临时脚本`/tmp/spc_b136_network_view_audit.py`，SHA256 `c471eabfc7422948247000c872820d7a3fc3c9b828b56b73f0c6ee92f5b166fa`；同一Python/Lupa环境执行。实际Bridge/Input，两城一条路线，facts和native getter为fixture。只做ACTIVE3→4→2三次发布，补B135尚未追踪的private view/兼容投影；没有重复大规模Capture实验。

两次进程外GC后前两代view/兼容投影均0/0，最新代19/8；修改公开兼容投影不改变private Current结果。源码hash仍为B135已登记值。一次手动Network.Read则确认Capture2次、city_scan4次，源于先Refresh，再经currentView再次Refresh；这属于点击诊断的重复工作，不能解释无人点击时持续增长。

两项实验均为**LOCAL_SIMULATION_PASS**（本地模拟）。未发现所测副本/旧代持续保留；仍未测原生分配字节、真实调用频率、其它consumer持有关系或引擎资源，不能由0残留宣称整个Mod没有泄漏，也不能把表数量换算成截图中的GB。

### 候选处理与下一调查门槛

已确认的小冗余继续登记，但不建议仅为这些小项另发一次长测包：

- Copy(nil)目前仍创建seen表和递归闭包；nil早退可省普通P0/P1每次读取的一组分配，已有ledger的P2–P4无此收益。非nil类型/预算校验不应顺手重写。
- Network.Signature每城建立八字段临时数组，可考虑仅在同次调用中复用一张完整覆盖的数组；不是跨事件事实缓存。
- 手动Network.Read重复Refresh可以单独整理；detailPage按点过的城市保留分页签名，但它依赖人工点击，不作为静置/纯回合增长解释。
- active的reference表若改为标量比较，仍须保留额外键拒绝、全部getter读取顺序及异常边界，不能直接以四字段短路判断替换same。公共Base/Investment输出隔离和最终facts隔离保留。

鉴于上述路径未找到持续挂住的旧代，**下一推荐是准备同一存档的窄Network分支停用对照，而非宣称继续省几张表即可解决增长**。当前尚无安全Network OFF，不能直接部署一处return：

1. `ready=false`只挡Refresh，Verified、退出/返回仍可withdraw→publish，LoadScreenClose会重新开启。Current查询及商业汇聚直接routes读取还可能使用旧结果。
2. 故意制造UNKNOWN不是效果退出：CopyYields/StandardizationDiscount保留旧载体/计划，其他consumer部分会清除，形成不一致对照。必须保持DB、永久进度/投资/模板/Claim不变，以明确实验状态和各模块自有退出路径撤销此次涉及的派生效果；撤销未确认则不开始测量，不能伪造失城。
3. UI NetworkSender只有一个flight，并非无限排队；但只停接收端会留下等待/超时/重新发送。须同时收口BackgroundRoutes的Network发送及failure-proof请求，处理既有flight/awaiting及晚到包；保留的其它UI采集范围要明示。Claim、Gameplay直接入口和旧fresh查询也不能绕过。
4. 稳定观察窗应确认Capture/derive/publish不再执行，无新的retry积压；仍运行的城市进度、总督事实、本地能力、其它采样必须列清，不能说“整个Mod关闭”。预期改变的是Network分支及其下游活动，不能单独归因一张表或Capture。
5. 未来测试从同一未改写的存档副本冷启动，只取初始和随后少数回合；不保存实验后的撤销状态。恢复正常包后重新读取原存档，并按新epoch拒绝旧包。具体进入/退出/恢复的定向模拟须先通过，才提出一次最小用户测试；本轮不要求测试。

这是一组下一对照的必要门槛，**尚非READY implementation方案**；需要先收窄完整退出与请求边界，不扩展成通用停用框架。当前结论：保留B135/B136修复，MEMORY_CAUSE_OPEN；不自动GC、不清永久账本、不部署、不进入F。


## B137.164 — authorized session Network isolation control

2026-09-29用户授权实施。基线bb1bab3 / B136.163；B135/B136已验收的响应与优化保留。本批不是内存修复，而是同一原存档的最小Network分支停用对照。按W0004 L3验证相关退出/桥接/加载边界，不跑玩法全回归、规模stress或重做用户长测。Design、保存schema与永久writer不变，不进入F。

### 模式、退出范围与恢复

默认NORMAL。现有诊断面板“Network 隔离对照”：左键只读，右键明确进入一次、不可在同会话重开的实验。UI先停止三个独立后台（商路、工业复制样本、折扣购买资格），清除flight/pending/retry和它们的临时快照；各自返回匹配本次Gameplay epoch的退出确认。Gameplay只在三份确认、模块就绪/非busy后开启会话标记。随后Bridge清除本玩家私有view/兼容投影/routes/candidate，不伪造UNKNOWN或ownership loss，也不发布假Network收益。

| 自有writer | 本次撤销的精确对象 | 明确保留 |
|---|---|---|
| Lv3Effects | 三个商业连接类型carrier | 同模块Culture本地人口/专家效果，及其它本地能力 |
| NetworkBoost | 自有旧Boost catalog、整数catalog、B057临时测试carrier | 科技/市政当前进度；没有逆改历史已触发boost |
| CopyYields | 工业PRODUCTION的POS/NEG/POP 40个定义 | 已退出的Research tombstone不作为新收益；Industry本地支持 |
| CommerceConvergence | SCIENCE/CULTURE/PRODUCTION各16bit carrier | Commerce支持、住房/GPP，永久Identity/Potential/investment |
| StandardizationDiscount | 自有有效目标catalog×4级discount carrier | Standardization永久模板、学习和保存路径 |

各模块只枚举明确拥有的ID，逐本玩家城市核对原生存在性，移除后要求`HasBuilding==false`。包括尚未进入内存applied表的存档载体；不用前缀批量清除，不删除普通建筑或Property。五项均成功才报READY；任一未知/移除失败则FAILED并保持停用，**不自动重试，不将部分退出当可测状态**。重复右键只读已有结果。暂停期间其他本地能力/进度/模板/Claim/总督事实与其它UI采样照常；它们的成本与原生引擎分配仍在。本批不证明整个Mod无网络以外成本。

Bridge的Refresh/Verified/Receive、旧fresh/Current查询、Rebuild/CheckEvidence及E2失效调用均受会话门控；晚到包不能恢复旧view。四个纯Network consumer在batch构造/扫描之前停用，混合Lv3模块只阻止Commerce分支。UI context单独重建时读取当前Gameplay会话标记并再次停止；原存档冷启动重建Gameplay则默认NORMAL、新epoch、正常重采集。没有新每帧请求/扫描；现有UI脉冲停用后早退。

恢复只使用**原始未覆盖的存档副本冷启动**，不在同会话重新启用。本模式不写保存Property，但撤销的原生carrier和正常过回合仍会被游戏自动存档：实验存档/自动存档不能当正常恢复点，不承诺重载实验档等价于原档。不要覆盖原档；不要把实验局作为正式进度继续。原包回滚也使用原存档。

### 诊断和归因限制

报告仅显示NORMAL/READY/FAILED、UI退出3/3、模块撤销5/5、退出后已有计数器的route_scan/net_send/derive_executed/input_publication/copy_send/discount_send是否新增、Lua调用处用量与恢复提示。复用固定计数，不新增泛化计数器或历史样本。Lua用量不是本Mod独占；没有执行GC、调GC参数或清永久成果。UI退出不完整/计数不可读/出现新工作则停止对照。

开始退出时会有一次catalog核对、native撤销及引用释放；这个瞬时下降或初始化成本不能解释持续增长。比较初始稳定点后两个玩家回合的增量，不把停用改善单独归因Capture/某张表，也不把无改善解释成所有Network路径零分配。

### 本地验证与原生待办

本地定向runner：`DevelopmentTests/test_b137_network_isolation.py`；使用Lupa lua55及Git基线bb1bab3，只抽取旧fixture声明，不运行旧wrapper/stress。LOCAL_SIMULATION_PASS：五模块冷加载exact carrier集合（3/1126/40/48个；折扣fixture一个目标×4级）、重复撤销、未知存在性/移除未确认/缺城市拒绝、普通建筑/不相关carrier/永久写保护；24项正常模式对比基线bb1bab3一致。真实Bridge所有入口/晚到包/事件/exit/return停用后Capture、derive、publish、notify均0；三UI pending清除、context重建、默认新会话、七类前置拒绝、五模块逐项失败无重试、五真实consumer联合退出均通过。实际Gameplay dispatch与P0Panel请求握手也覆盖；未用测试stub代替被测withdraw逻辑。发现并修复Lv3混合Audit在退出失败后再次清COM的路径，Culture本地重算保留。折扣真实环境catalog存在性/原生效果释放仍须实机。更改Lua编译、modinfo164精确171文件及文档/context检查通过。原生Modifier释放、跨UI context回调/真实事件顺序、引擎和进程内存趋势均仍USER_GAME_TEST_REQUIRED。

最小测试（同一个现有可复现原存档，**不开启内存观测或手动GC，不征服/建城/调专家，不继续长测**）：

1. 冷启动原档，等载入稳定，左键“Network 隔离对照”，记录NORMAL报告及活动监视器进程内存。正常过两个玩家回合，各读一次同报告并记录进程内存。
2. 完全退出游戏，再冷启动同一个原档（不要选刚生成的自动存档）。右键一次“Network 隔离对照”；必须看到READY、UI3/3、撤销5/5、可观察/无新增，否则截图停止。等退出引起的一次性更新稳定后记初始报告与内存，再过两个玩家回合，各左键读报告并记录内存。
3. 不必截图所有其它诊断；两组各初始/+1T/+2T即可。任何错误/停用后出现网络工作即停止；不反复右键、手动GC或自行延长。测试后完全退出，重载原始存档即可恢复NORMAL；不保存实验进度。

等待本次短对照，不发放memory-fix PASS。若仍无法缩小来源，先分析此同档分支对照，再另提最小下一路径；不自动开始下一实验。

部署：source `7b11908` → B137.164 / modinfo164，receipt `B137.164-7b11908-playtest.json`（DEVELOP_ACTIVE）；独立比对171/171 MATCH。两次切换前OS检查均确认Civ VI退出；B136完整恢复包及stable桥hash保持，无pending事务。没有启动游戏、没有main/promotion。静态/本地PASS不升级为原生退出或内存改善PASS。


## B137 native isolation results and GC hypothesis

2026-09-29：用户投递本次对照截图，并提出“AI/城邦回合增长、进入玩家回合没有明显回收，是否本Mod影响原版/HD GC”的观察猜想，明确尚非确凿证据。本轮只做逐图审核、归档、定域源码核对和状态记录；没有修改Mod、GC策略、Design或运行包，没有启动游戏、执行玩法测试或追加长测。

### 原生观察与比较口径

14张原图（7组游戏/进程配对）已逐张阅读，保留原名移入外部`Specialization/Status/Validation/Evidence/B137_Network_Isolation_Comparison/`；manifest记录原路径、时间、bytes、SHA256与本节关联，14/14移动前后相同，收件箱目录保留且无重复图。游戏图均明确B137.164。两组PID不同，证明不同进程；相同T39城市/资源起点与规定的同原档对照相符，但截图本身不是存档文件身份或全部操作历史证明。

| 组 / 时间 | 模式 / 回合 | Gameplay调用处Lua MiB | Activity Monitor进程GB | PID |
|---|---|---:|---:|---:|
| 1 / 20:45:33 | NORMAL / T39 | 279.26 | 10.28 | 52726 |
| 2 / 20:46:06 | NORMAL / T40 | 417.25 | 10.41 | 52726 |
| 3 / 20:46:36 | NORMAL / T41 | 474.92 | 10.50 | 52726 |
| 4 / 20:48:54 | READY / T39，首次退出读数 | 275.57 | 10.18 | 53066 |
| 5 / 20:48:59 | READY / T39，第二起点 | 276.08 | 10.18 | 53066 |
| 6 / 20:49:23 | READY / T40 | 351.31 | 10.33 | 53066 |
| 7 / 20:49:49 | READY / T41 | 397.50 | 10.40 | 53066 |

四张隔离图均为READY、UI退出3/3、收益撤销5/5、“可观察：退出后网络采集/发送/派生/发布无新增”。核对`Mod/NetworkIsolation.lua`：这要求三个UI当前epoch退出确认、五个module-owned退出返回成功、inflight=0及六项已有Network累计计数相对退出基线不增加。报告只读`count`，不会调用完整GC。

- **USER_GAME_TEST_PASS（本次隔离握手/模块退出报告/两回合计数静默范围）**：原生UI→Gameplay实验可进入READY并保持到T41。5/5是模块对自有carrier枚举/原生存在性核对的成功，不等于截图已分别证明五类效果原先全部存在、每一种原生Modifier都独立撤销；没有各类收益前后面板，因此不扩大PASS。
- NORMAL T39→41：Lua **+195.66 MiB**，进程 **+0.22 GB**。隔离采用第二T39起点：Lua **+121.42 MiB**，进程 **+0.22 GB**；若用首次退出点则Lua+121.93 MiB，结论不变。
- 两回合Lua净增量相差**74.24 MiB**，这是所测调用范围的净变化，包含期间分配和回收，不是累计分配量或本Mod独占量。隔离组基线进程已经低0.10GB，终点仍低0.10GB，不能把这个终点差额当两回合改善。两组进程增长在显示精度下相同；**Network隔离没有消除进程增长**，MEMORY_CAUSE_OPEN。
- 隔离同时停用路线采集、桥接、五类consumer并撤销载体，不能将Lua差额单独归给Capture/某张表，也不能从短对照断言Network没有成本或排除其它路径。没有完整回收后的点，本轮不能判定剩余增长是可回收积压还是持续保留。没有逐AI/城邦/人类回调时间线，用户关于回收时机的印象仍单独标记为待证线索。

### “是否打断GC”的定域核对

**STATIC_CONFIRMED**：当前`Mod/`的117个Lua中，直接GC接口只在[PerformanceCounters](../../../Mod/PerformanceCounters.lua)的`count`、可选`isrunning`、明确手动`collect`。完整回收只由[P0Panel](../../../Mod/UI/P0Panel.lua)右键`MEMORY_GC_COLLECT`经[Gameplay](../../../Mod/Gameplay.lua)早期诊断分支调用；有token去重/busy/失败阻断。未发现stop/restart/step/setpause/setstepmul、collector别名重绑定、相关全局环境替换、`__gc`或不配对恢复。六回合观测器只读count。事件移除未见RemoveAll/改写Events或GameEvents；所见为自己的UI shutdown/已保存hook。没有建立“本Mod移除了HD回收事件”的调用链。

本机HD Workshop `2465378070` 的180个Lua作GC关键词定域搜索：未命中`collectgarbage/gcinfo/lua_gc/setpause/setstepmul/garbage/独立gc`。直接核对`Gameplay/RegionalYields.lua:239–254`：玩家开始/结束回合根据pending重算区域收益后置0；`Gameplay/BinaryCompress.lua:133–148`：每整回合更新城市宜居度/政策Property。它们不是Lua GC或内存压缩。此结论只覆盖所查可读Lua，未覆盖引擎二进制内部、所有其它Mod或宿主注入。

[Lua官方内存管理说明](https://www.lua.org/manual/5.1/manual.html#2.10)区分对象可达性、增量回收与回收参数；仍被引用的对象会保留，失去引用的对象可以在后续回收中释放。普通表/Property数据的存在本身不等于停止GC；新增分配、仍保留的引用、宿主调度或原生分配器行为，都可能改变可见曲线。回合结束/存档写盘不是“把内存倒空”的合同，自动存档也不能替代内存管理。

本机此前原生环境串为`2013.2.0 r13768`、`isrunning=未知`，不能视为标准Lua55，也不能写成已停止GC。[Lua5.1接口](https://www.lua.org/manual/5.1/manual.html#pdf-collectgarbage)未列isrunning，[Lua5.2](https://www.lua.org/manual/5.2/manual.html#pdf-collectgarbage)才列此选项；这些手册解释通用机制，不确定本机宿主预算或参数。既有B134/B135手动回收确实降低Lua读数，说明当时有可回收对象，不证明自动GC关闭。本次进程和Lua净增量也不直接揭示回收发生时点。**暂不支持“本Mod直接打断GC”的具体说法；Mod增加分配、改变引用寿命或间接影响回收表现的可能仍保留。**

### 下一调查边界

[B137实验范围/恢复合同](#b137164--authorized-session-network-isolation-control)继续适用。最小对照已经收齐，不再要求重复长测/手动GC，不把诊断改成每回合清理。保留B135/B136优化；隔离仅实验，不覆盖原存档，正常使用需完全退出并重载原档。

下一建议仅为定域只读调查：先沿隔离后仍运行的`PlayerTurnActivated`统一分发、非Network本地consumer与事实采样路径，核对local/foreign归属门控和实际分配/保留来源；区分AI期间收到事件与给AI施加能力，不能仅凭发生时机认定AI专业化。复用既有计数/证据，不重新增加泛化计数器。仍无法归因时再提出单一路径的最小对照及安全退出条件，**另行授权实施**；本轮不直接停用余下整个Mod、不添加周期GC、不进入F。

## B138.165 — bounded stabilization trial

用户授权一次有退出条件的性能稳定化：受控自动GC、公共更新接入约束及最多一条有证据且安全的公共冗余修复，然后一次整合实机验收。不是自动进入F/新Gameplay；解除此前“暂不自动GC”的阶段限制。沿用B129–B137与原生B134/B135手动GC证据，不重做全部分配调查。

### 运行缓解：唯一协调器

`PerformanceCounters.StartMemory`拥有本次加载的GC开关、阈值起点、回合标记、失败锁存和最近8次结果；不进入Game/City Property或保存schema。B134已经实测的`pcall(collectgarbage,'collect')`仍为唯一完整回收调用。UI左键只读，右键发明确ON/OFF请求；关闭清pending，开启等下一本地玩家回合；失败锁存不能通过开关清掉。新加载恢复试运行默认ON；永久退出此试运行需后续源码关闭/恢复B137运行包，不把会话开关冒充全局配置。

| 固定试运行参数 | 验收前依据与边界 |
|---|---|
| 增长128 MiB | 相对加载起点或最近完整回收后的值；B137正常模式两回合净增195.66MiB，故可观测地覆盖增长，又不对小幅波动回收。不是本Mod独占内存预算 |
| 最少间隔2个游戏回合 | 首次从加载回合算；自动/保留手动API共用间隔，避免每回合/每AI事件调用。手动API不再挂右键；验收不调用手动GC |
| CPU或可取得的墙钟耗时>2秒锁停 | B134只取得粗粒度0/1秒CPU读数，2秒是保守试运行停止阈值，不是精确pause上限；调用同步，不能中断已经开始的GC。缺/倒退CPU计时、出现墙钟失效也锁停 |
| 8次结果＋24条日志/加载 | 结果包含原因、回合、before/after MiB及可用耗时；日志用现有Lua.log的`[SPC][GC_TRIAL]`，到24条明确标记后停止写日志，结果环继续滚动。不另建遥测/长期文件 |

阶段：LoadScreenClose仅建立起点；当前本地人类PlayerTurnActivated登记单次评估，在后续GameCoreEventPublishComplete检查。先消费pending再执行；同回合重复通知不重评，玩家回合离开/foreign activation清pending；旧coordinator回调失效。没有每帧轮询/城市遍历/诊断面板依赖。保留原计数观察器，即使GC hook不可用也不撤掉它。

跳过范围：脚本请求处理中、Network隔离/未就绪/refresh/inflight、各已公开模块busy、Claim私有Flush的只读IsBusy、route/UI请求未完成。跳过当回合后不追着Publish重试。只新增RequestDepth诊断护栏和Claim只读getter，**不改变请求处理、Claim写入或业务事件派发**。本轮不宣称这些guard可证明所有原生事务完成；B105“首个Publish不等于事务结束”反证继续有效。原生首个评估若持续早于UI ACK，按PHASE_NOT_READY失败处理，查看具体SKIP，不扩大重试窗口掩盖。

已知GC停止则不调用，不重启；isrunning未知保持未知（符合B134环境），不是“确认自动GC正常”。失败/后读数缺失/状态改变/耗时超预算后停止自动尝试。不得调stop/restart/step/setpause/setstepmul、清缓存/账本、循环追某个固定旧堆值。回收后增长也原样记录，不钳制结果。

### 公共路径：保留行为，固定接入约束

本轮未找到符合全部语义的安全公共业务删减，**没有为满足数量而修改业务更新算法**。定域实际Lua fixture给出的反例：GPP已有6点配置，易主时载体读取UNKNOWN，先保留；随后外国玩家回合读数恢复，旧配置才被撤为0。简单跳过foreign turn会丢掉这个必要恢复路径。空外国回合确有Housing/GPP共2次城市访问/41次carrier检查、Infrastructure1次/52次检查，但不能把局部事实读取减少或扫描次数直接称为字节/进程内存改善。

新模块接入要求和六组实际模块定向测试独立提交，见[Architecture公共更新约束](../../Architecture/Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)。计算/完整诊断分离、影响范围/依赖、同步Audit内复用以及缓存/pending退出职责均保留；不迁移所有旧模块、不建立新事件总线。GC变化与约束/测试分开记录；B137→B138没有混入业务性能修复可供混合归因。

### 本地证据与原生边界

- `DevelopmentTests/test_b138_gc.py`：实际StartMemory、Gameplay早期分发、UI开关、语法/manifest；非0本地玩家、阈值/间隔、重复/重入、busy/pending/隔离、失败/时钟、结果/日志上限。使用Lupa lua55模拟，不代表Civ原生GC调度。
- `DevelopmentTests/test_b138_update_contract.py`：实际RuntimeWork/批次facts缓存/区域枚举、GPP UNKNOWN易主撤销及同回合变化、B135 UI/Gameplay原因传播和重试。只提取历史fixture声明，不运行历史wrapper/stress。
- 未修改保存结构/收益公式/SQL/Design；B132/B136相关功能实机证据保留，不强求重做所有既有验收。B138原生自动阶段、暂停成本、回收基线及进程缓解均为USER_GAME_TEST_REQUIRED。

### 一次整合验收与预先退出标准

固定原有可复现存档副本，完整重启后以正常Network模式加载；不启用隔离、不手动GC、不改世界规模/征服/建设，不覆盖原存档。最多10个玩家回合或4次AUTO_GROWTH（先到者停止）；不要求每回合截图。第1次自动回收后及第4次后，在同样的玩家回合空闲阶段等进程读数稳定约30秒，各记录一次进程内存；最后左键GC试运行报告一图，日志自动保留最多24条。若头4回合一直只有SKIP/WAIT，提前停止并交一张报告，不浪费剩余回合。

在最后内存观察完成后，同回合把一名学院专家移出/移回，确认既有收益即时变化/恢复即可（B136总督验收继续复用；没有修改总督/所有权路径，不重做征服与长测）。右键关闭GC，报告应显示关闭且不会立即再收；不必为此多过两回合。

预先固定判据（工程短测门槛，不是永久无泄漏证明；不事后放宽）：

1. 调度/安全：至少4次自动触发，间隔≥2T，全部在本地进入后的阶段；无失败/超时锁停、重复调用、原生错误或明显不可接受暂停。缺触发按报告区分阈值未达和PHASE_NOT_READY，不记PASS。
2. Lua缓解：丢开第1次初始化点，后3次回收后基线最大差≤64MiB；其中至少2次单次释放≥64MiB。64MiB为触发增长阈值一半，用于拒绝“回收几乎无收益”或明显持续抬升；不把未释放对象自动判成泄漏。
3. 进程缓解：相同世界状态，第4次回收后稳定读数相对第1次增加≤0.20GB；这是长于B137两回合+0.22GB观察窗的暂定接受门槛，进程测量并非Mod独占。无可比读数则只缺这一个证据，不以Lua结果替代进程结论。
4. 正确性：专家同回合变化/恢复正常；已有所有权/保存测试不回归的本地证据仍成立。业务算法未改，不扩大本次native PASS范围。

四项通过才记“**稳定化完成，剩余分配效率问题开放**”，解除性能对下一功能计划的阻塞；下一功能仍需既有计划/授权，不自动进入F。当前交付代码不等于native验收完成。

失败的下一项有辨别力动作：始终SKIP→只校准所报阶段/pending生命周期；GC失败/耗时锁停→保持OFF、查看一次具体调用状态；基线持续升高/进程不缓解→仅做同一存档、同一包ON/OFF的2次回收间隔对照（复用本次ON数据），不再移除Mod读档或新建泛化计数器。10T不足4次但因增长低于阈值，只报告观测不足；是否延长由具体缺口决定，不自动开长测。

### 剩余问题与重启调查条件

| 事项 | 现有证据/受影响路径 | 重新调查触发 | 是否阻塞下一功能 |
|---|---|---|---|
| 临时分配效率与重复foreign核对 | B133次数未降；上述UNKNOWN撤销反例；RuntimeWork→local consumer/carrier核对 | 新consumer显著放大访问/实际卡顿，或本次缓解不通过；先拆明确的待撤销owner责任再谈缩范围 | 缓解通过后不阻塞；不要求定位全部分配来源 |
| 回收后保留/引擎调度及其它Mod | B134大量可回收；B137进程增长相同；未证明engine/HD GC被本Mod打断 | 相似世界连续回收后基线超本次固定门槛，或原生失败 | 当前只由上述验收决定，不无限延伸 |
| GC阶段、计时能力与暂停 | native full collect有证据，但自动phase新；isrunning未知、0/1秒计时 | 持续SKIP、缺clock、错误/超时、用户可感暂停 | 失败只阻塞本缓解；下一动作定域，不改Gameplay |

回滚：面板右键先关闭本加载自动调用；需要恢复包时由既有deployment receipt恢复B137（不手改运行目录）。无新永久数据格式，不删除旧恢复点。

### B138 deployment checkpoint

GC实现独立提交`95c0893`；公共更新约束/定向回归/固定验收合同提交`ec1c69d`（没有业务更新算法改动）。OS进程检查确认游戏/启动器退出后，经既有工具恢复stable桥再激活B138；source `ec1c69d48aac67844a51d67903661642834be5e2`，receipt `B138.165-ec1c69d-playtest.json`，DEVELOP_ACTIVE，**171/171 MATCH**。B137完整恢复包与stable恢复点核验保留，无pending事务，无main/Design变化。当前仍USER_GAME_TEST_REQUIRED；没有运行游戏或宣称原生稳定化通过。

### B139.166 — WAIT_LOAD native failure and bounded fallback

本次24张截图逐张审阅并原名归档至外部`Specialization/Status/Validation/Evidence/B138_AutoGC_WAIT_LOAD/`，manifest记录24/24 SHA256一致。22:52:50 / T48报告明确显示B138.165、自动开启、`WAIT_LOAD`、本次加载调用0次、Lua2013.2.0r13768。用户报告没有卡顿；**这次自动GC触发 USER_GAME_TEST_FAIL（加载就绪门槛），不是已执行GC但无释放收益**。同一PID61565，T39→49进程10.17→11.23GB；T48两个读数11.11→11.10GB。进程读数不属于本Mod独占，不能由此量化Lua分配/泄漏。现有Logs没有Lua.log，不能伪称已从日志取得GC记录。

代码中只有LoadScreenClose建立loaded/anchor，故WAIT_LOAD直接阻断之后所有评估；截图证明该observer没有取得这个起点，尚不能区分事件未向此context送达或安装时已错过。B138模拟始终主动发送load事件，未覆盖这个原生失败序列。

用户已授权稳定化中的窄修复，不另开Gameplay决策。B139保留LoadScreenClose计数起点，同时在**首次合格本地人类PlayerTurnActivated**补建一次起点（仅count，不collect、不城市扫描）；晚到/重复load不能重置起点或冷却。后续仍经原发布阶段、全部busy/Network/请求护栏、128MiB/2T/2秒锁停。OFF、未知local player、外国回合不触发补建。面板增加起点来源/回合；无UI轮询、永久属性/缓存清理、业务更新算法改变。不修改Network.ready或猜测后续SKIP原因。

STATIC_CONFIRMED / LOCAL_SIMULATION_PASS：复用`test_b138_gc.py`实际模块/Gameplay/UI fixture，补未送达与晚到load、local player4/foreign/unknown、OFF/ON、基线失败锁停、Network未就绪护栏；原17组busy、18组失败、边界/重复/重入/上限均通过。版本B139.166/modinfo166，唯一行为变更在PerformanceCounters；Probe/modinfo仅版本。B138公共业务约束未改，不重跑无关玩法套件。native fallback及内存缓解仍待验，阈值/接受标准没有放宽。

最小下一检查：冷启动原固定存档副本；进入后最多推进3个玩家回合，左键“GC试运行”交一张报告。应有LOAD或LOCAL_TURN起点，不能仍是WAIT_LOAD；若SKIP/STOP/等待持续，立即停在该报告，不跑长测。若已AUTO_GROWTH，则复用B138最多10T/4次及固定整合标准，不追加独立长测。没有证明全部事件/安全阶段的native表现，出现下一级具体失败仅处理该原因。

B139部署核验：实现提交`1104bde`，receipt `B139.166-1104bde-playtest.json` DEVELOP_ACTIVE，171/171 MATCH；OS两次只读确认无游戏/启动器进程，先用B138 receipt恢复stable再激活B139，完整B138/stable恢复点保留，无pending事务。main/Design不变，native修复与缓解尚待用户验证。

### B139 native automatic collection observations

2026-09-30：28张原图（14组游戏/Activity Monitor）逐张读取，原名移入外部`Specialization/Status/Validation/Evidence/B139_AutoGC_T39_T54/`；manifest记录28/28移动前后SHA256相同，收件箱无残留图。用户主动延长测试，并报告“似乎后面稳定下来了”；随后明确“没有卡顿，未操作/未观察收益”。不把此陈述升级为专家收益验收。

同一PID87534，截图覆盖T39→T54；报告B139.166，起点LOCAL_TURN/T40，自动开启。共6次AUTO_GROWTH/COLLECTED；T44/T49显示INTERVAL，T47显示BELOW_THRESHOLD，无失败/超时锁停。报告记录为AUTO_GROWTH，而非手动调用；只读面板不执行回收的静态合同保留，截图本身不证明完整的面板开关历史。原生证据支持B139加载补建及重复自动触发修复USER_GAME_TEST_PASS，限本次可见路径，不证明全部原生事务时序。

| 自动调用回合 | 回收前MiB | 回收后MiB | 释放MiB | CPU/墙钟秒 |
|---|---:|---:|---:|---|
| T43 | 579.01 | 562.09 | 16.92 | 0.00 / 1.00 |
| T45 | 694.75 | 399.13 | 295.62 | 0.00 / 1.00 |
| T48 | 568.82 | 463.92 | 104.90 | 0.00 / 0.00 |
| T50 | 619.81 | 432.51 | 187.30 | 0.00 / 0.00 |
| T52 | 589.44 | 435.53 | 153.91 | 0.00 / 0.00 |
| T54 | 571.23 | 407.40 | 163.83 | 0.00 / 0.00 |

计时间隔2/3/2/2/2T符合冷却；五次释放超过64MiB。0秒来自有限分辨率时钟，不能解释为零暂停；“没有卡顿”是用户体感证据。Lua为调用处整个堆的统计范围，不是本Mod独占内存；释放量不能归属某个模块。

| 配对截图时间 | 回合 | 进程GB |
|---|---:|---:|
| 06:39:41 | 39 | 10.23 |
| 06:40:10 | 40 | 10.46 |
| 06:40:38 | 41 | 10.55 |
| 06:41:40 | 42 | 10.70 |
| 06:42:29 | 43 | 10.78 |
| 06:43:17 | 43 | 10.78 |
| 06:43:53 | 44 | 10.88 |
| 06:44:40 | 45 | 10.73 |
| 06:45:37 | 47 | 10.77 |
| 06:46:16 | 48 | 10.83 |
| 06:46:29 | 49 | 10.83 |
| 06:46:57 | 50 | 10.82 |
| 06:47:47 | 52 | 10.82 |
| 06:48:41 | 54 | 10.82 |

**固定判据与额外观察分别记录：** 最初4次中丢开第1次，后三点399.13/463.92/432.51的范围64.79MiB，**略超过原定≤64MiB，原窗口该项未通过**；不能通过四舍五入或提高阈值记PASS。用户自主继续后，最后3点432.51/435.53/407.40范围28.13MiB，最后值比T45仅高8.27MiB，没有持续单调抬升。这是额外后段收敛证据，不回写初始窗口结果。

T43→T50进程+0.04GB，T50/T52/T54连续显示10.82GB；T45→54范围10.73–10.83GB。支持本次后段进程积累缓解。截图未独立证明每点均空闲30秒或世界完全不变（AI继续行动），因此不将其标为严格同状态实验或全部增长归因GC。相较B138 WAIT_LOAD零调用，本次原生调用及释放已直接确认；不宣称根因关闭、无泄漏或其它Mod/引擎GC被修复。

**收束建议：** 本轮运行缓解已有明确原生有效性与后段稳定证据，无需再作同样长测、提高阈值或新增泛化计数器；不因64.79MiB的非单调早期波动启动新一轮分配追踪。完整稳定化结项仍保留原窗口例外，待用户认可此观察范围，以及唯一未做的既定正确性检查：同回合移出/移回一名学院专家，确认收益相应减少/恢复；可合并下一次使用游戏，不要求现在启动或重新测内存。GC右键会话关闭的native证据仍未提供，本地开关测试保留，不单独重发一轮测试。功能计划可以准备，实施不自动授权；本次不标四项固定判据全部PASS或自动进入F。

公共接入约束与已确认优化保留，剩余分配效率问题开放；只有后续出现回收后基线持续抬升、进程重新积累、超时/错误或功能回归，才按上方具体受影响路径重新调查。本轮仅证据与当前导航更新，无代码、参数、Design、运行包、部署或main变化。

### B139 operations long test — GC release and process growth

2026-09-30，用户继续实际征服/操作长测。26张图逐张读取并原名归档至外部`Specialization/Status/Validation/Evidence/B139_AutoGC_Operations_T39_T62/`，manifest核对26/26 SHA256一致，投递图清空。PID89277，与前一组87534不同；版本仍B139.166。不能把两组拼成一个进程曲线。

用户补充：一直有建筑在建造，后期加入4条商路；开始时调整专家/总督，约五六回合时投资，当时收益正常、没有明显卡顿，之后未仔细观察收益、未继续调整专家。截图T53显示4/4路线、T57起4/5，与所述相符。不是固定世界/无操作验收；不能把建造/商路后的全部增长自动归为正常，也不能把早期功能正常扩为全程各能力PASS。

| 时间 | 回合 | Activity Monitor进程GB | 可见事件/最新GC |
|---|---:|---:|---|
| 06:57:36 | 39 | 10.24 | 起点，未展示GC报告 |
| 07:02:32 | 39 | 10.52 | 比布拉克斯征服消息 |
| 07:02:57 | 39 | 10.67 | 安杜阿图卡征服消息 |
| 07:06:34 | 39 | 11.03 | WAIT_LOAD，0次，尚无起点 |
| 07:08:37 | 42 | 10.62 | LOCAL_TURN/T40，首次AUTO |
| 07:11:44 | 44 | 10.87 | 第2次AUTO |
| 07:13:47 | 46 | 10.98 | 第3次AUTO |
| 07:15:07 | 50 | 11.06 | INTERVAL，第4次为T49 |
| 07:15:46 | 51 | 11.01 | 第5次AUTO |
| 07:18:22 | 53 | 11.09 | 第6次AUTO，4条商路可见 |
| 07:19:54 | 57 | 11.17 | 第8次AUTO |
| 07:21:08 | 60 | 11.26 | 第9次AUTO |
| 07:22:06 | 62 | 11.21 | 第10次AUTO |

| 回收回合 | 前MiB | 后MiB | 释放MiB | CPU/墙钟秒 |
|---|---:|---:|---:|---|
| 42 | 1041.05 | 285.47 | 755.58 | 1 / 2 |
| 44 | 567.36 | 461.28 | 106.08 | 0 / 0 |
| 46 | 652.61 | 509.91 | 142.70 | 0 / 0 |
| 49 | 718.59 | 533.11 | 185.48 | 0 / 0 |
| 51 | 710.43 | 469.76 | 240.67 | 0 / 0 |
| 53 | 647.46 | 473.74 | 173.72 | 1 / 0 |
| 55 | 748.76 | 682.26 | 66.50 | 0 / 0 |
| 57 | 870.24 | 500.17 | 370.07 | 1 / 1 |
| 60 | 755.35 | 614.37 | 140.98 | 0 / 0 |
| 62 | 802.40 | 484.07 | 318.33 | 0 / 0 |

10次全部COLLECTED，间隔2/2/3/2/2/2/2/3/2T；全部释放≥64MiB，无锁停。T42墙钟读数2秒达到预算边缘，但既定锁停条件是>2秒，并未触发；时钟粗粒度，CPU/墙钟不保证精确暂停长度。用户报告本次无明显卡顿。

**三个独立结论：**

1. **回收调度/释放有效的既有原生结论保留。** T39同回合操作期间10.24→11.03GB，尚无首个合格本地回合起点；随后T40补建，T42回收。与B138跨多回合仍WAIT_LOAD的失败不同：这次不是B139补建失效，而是现行仅玩家回合阶段触发的覆盖边界；不会仅因同回合征服继续积累而追加自动回收评估。首次回收Lua下降755.58MiB，配对进程由此前11.03降至10.62GB；期间还发生过回合等动作，不能精确把0.41GB全部归给这一调用。
2. **操作场景的进程增长未关闭。** T44→T62 Lua回收后461.28→484.07MiB，净+22.79；进程10.87→11.21GB，+0.34。T51→T62对应+14.31MiB/+0.20GB。Lua有峰值682.26/614.37，末三点范围130.30MiB，不能称为与上一轮相同的窄幅稳定；但这些峰值随后下降，不能仅靠峰值认定持续存活泄漏。进程T60→62下降0.05GB，也不是单调增长。总T39→62净+0.97GB，包含初始化、征服、建设、商路与世界变化，不能全算Mod泄漏。GC结果记录时点早于打开截图，两个统计范围也不同，不能用相减精确得到“原生泄漏量”。
3. **证据足以改变定位层级，不足以认定某模块根因。** GC确实缓解可回收积压，但不能据此结项整个操作负载的进程稳定性；此前较静态T50–54平台证据仍有效，仅限定当时场景。固定世界原验收门槛不被改写，本次变化世界不套用成严格控制PASS/FAIL。保留缓解、已有业务修复和后续模块接入约束，不加频率、不清永久记录、不打开全库调查。

定域源码复核（STATIC_CONFIRMED）：`Gameplay.lua`安装`PerformanceCounters.StartMemory`，唯一完整回收仍在Gameplay调用点；`PerformanceCounters.Heap`明确engine heap sharing未证。P0Panel为请求/读数桥，不在UI执行另一轮collect。当前只能确证调用所在Lua环境及前后读数，不能说所有UI/其它Mod/全部原生内存均已被清理，也不能称该数字为本Mod独占。仍被引用的对象不会因为一次GC而消失；[Lua官方内存管理](https://www.lua.org/manual/5.1/manual.html#2.10)只提供一般可达性/回收语义，不证明Civ宿主实现。原生Modifier/UI/渲染资源、其它Lua环境、分配器释放后保留空间都是候选解释，**本次未取得原生分类，均未证实**。

下一最有辨别力的动作是已有[外部monitor](../../../tools/external_monitor/README.md#optional-snapshots--cost-controls)的短窗口原生内存分类可行性核对，再考虑同PID两点vmmap/footprint，而不是更多Gameplay扫描计数或又一次截图长测。复用其5秒timeout/输出上限/失败即停和手动采集冷却；这些工具仅在合成进程验证过，Civ权限/成本未知，分类也未必可归属具体Mod。先判定heap/VM/图形类别等哪一类增长，再决定是否值得定域追踪；不要求移除Mod读档，不自动开全量Allocations追踪。现有数据已足以决定这个方向，无需用户立即重复操作；本轮没有运行外部monitor或修改工具。

状态：GC运行缓解有效性已有USER_GAME_TEST证据；操作负载的进程残余增长OPEN，完整稳定化不宣称结项。用户所述早期专家/总督/投资收益正常为限定功能证据，持续后段未观察仍未知；可继续规划功能，未授权新功能实施。若后续原生分类无法取得，则明确该限制、只提出一条可区分的替代动作，不无限扩大调查。

本次仅归档和报告/当前导航更新；不改runtime/Design/main、不部署、不跑玩法回归，不调整GC参数。

### Non-Specialization late-save control and stabilization closure

2026-09-30：用户提供一个以前从未开启本Mod的后期存档，正常进行操作、建筑/项目生产，最后两回合强制结束回合。16张图（8组游戏/Activity Monitor）全部读取，原名移至外部`Specialization/Status/Validation/Evidence/B139_NoSpecialization_LateSave_T148_T152/`，manifest确认16/16 SHA256一致。无Mod条件来自用户明确陈述；画面未见本Mod诊断入口，但截图不是完整启用Mod清单审计。不是从Specialization存档卸载Mod，也没有要求用户改变支持存档边界。

| 时间 | 可见回合 | Civilization VI进程内存GB | 读图备注 |
|---|---:|---:|---|
| 07:40:50 | 148 | 11.30 | 后期旧档起点 |
| 07:43:41 | 148 | 11.50 | 同回合，等待阶段 |
| 07:44:29 | 148 | 12.00 | 同回合，等待阶段 |
| 07:45:45 | 149 | 11.93 | 出现0.07GB回落，城市生产面板打开 |
| 07:55:11 | 150 | 12.46 | 世界继续变化 |
| 08:50:52 | 150 | 12.50 | 仍同回合，画面含战斗/占领消息；长时间间隔不可当作已证静置 |
| 08:54:23 | 151 | 12.66 | 用户称最后两回合强过，既有生产仍在进行 |
| 08:56:03 | 152 | 12.83 | 最后读数 |

八组均为PID92167，单位为Activity Monitor进程Memory列的GB（0.01精度），不是Lua或本Mod独占内存。T148首点→T152净增**1.53GB**；同T148首尾+0.70GB，随后回落0.07GB；T149→T152仍+0.90GB，最后两次过回合12.50→12.66→12.83合计+0.33GB。因此未启用Specialization时也能出现操作/过回合增长，并且回落后仍有后续积累。这不是只有一次初始化峰值的截图；但没有连续采样，不能推断每次回合内峰值、回收时机或长期固定斜率。最后两回合强过不冻结AI、建造或世界变化。

**归因边界：** 这组直接支持“观察到进程增长，并不需要Specialization运行”。不能再把先前所有未知增长默认归为本Mod，也不能将此认定为HD、其它某个Mod或游戏本体已定位的泄漏。旧档T148后期世界与B139的T39测试不同，PID/初始化/操作均不同；不得相减GB或增长速率来计算本Mod成本，也没有证明本Mod零额外占用或永无泄漏。原生内存类别和各Mod贡献仍未知。

**工程结项与证据分别记录：** 用户据此认为当前Mod优化已经可以，结合B139自动触发/释放有效、较静态后段平台、操作测试无明显卡顿及早期相关收益正常的既有证据，接受现有缓解并收束本轮有界性能稳定化工作。**稳定化工程阶段完成；剩余分配效率/进程内存归因开放，解除其对功能规划的阻塞。** 这不是原四项固定验收判据全部PASS：原窗口64.79MiB超过64MiB、操作场景后段变化及未独立完整验证的专家移出/移回和会话关闭原生检查照实保留，不改阈值、不补造验收。早期功能证据不扩大为全程/全部能力PASS，E2既有范围仍为partial。

当前不执行上一节建议的vmmap/footprint采集，不再派发重复长测，不新增计数器/监视器或提高GC频率。保留B129–B139已实施修复、可撤销GC与[公共更新接入约束](../../Architecture/Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)。剩余事项限定为：

| 未关闭事项 | 当前证据/路径 | 重新调查触发条件与开发影响 |
|---|---|---|
| 进程残余增长的构成/归属 | B139操作长测与本次无Mod旧档均有增长；非同档，未取得原生分类 | 出现明显卡顿、崩溃或影响游玩的内存压力，再决定短窗口分类；单次进程上涨不自动重开，不阻塞下一功能计划 |
| 事件/事实采集的剩余分配效率 | 既有定域修复保留，临时表可回收证据不能量化全部分配成本 | 新模块接入发现具体重复触发/读取或性能回归时按受影响路径处理；不用全库重构作为前置 |
| 自动GC的其它原生时序及限定功能证据 | 当前两组自动调用成功；严格功能动作/关闭会话检查未独立完整覆盖 | 实际出现GC失败/锁停、明显暂停或功能异常再定域验证；不扩大PASS，不立即追加用户测试 |

本次只做证据归档/分析与当前状态同步；B139.166/modinfo166、source1104bde及参数不变。没有修改Design/main/runtime，没有部署、游戏操作或玩法回归。后续可恢复功能计划审阅，**不因此授权新功能实施或进入F**。
