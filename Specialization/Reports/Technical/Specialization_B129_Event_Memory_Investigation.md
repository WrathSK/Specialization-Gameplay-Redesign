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
