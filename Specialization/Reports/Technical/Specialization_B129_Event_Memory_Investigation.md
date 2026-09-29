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
