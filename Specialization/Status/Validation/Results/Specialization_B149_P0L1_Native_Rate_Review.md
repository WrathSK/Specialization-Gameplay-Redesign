# B149.176 — 风雅熏陶可见加值验收与结算时序边界

Date: 2026-10-02
Evidence: USER_GAME_TEST_PASS（已测可见配置/旅游率）；LOCAL_SIMULATION_PASS（下列两个定向检查）；实际累计结算 USER_GAME_TEST_REQUIRED。
State: P0_L1_PARTIAL_NATIVE_GATE_REQUIRED；不是完整L1 PASS。
Runtime: B149.176 / modinfo176，源码 `637f97b`；本轮没有源码修改、部署或游戏启动。
Contract: [当前L1切片](../../../Architecture/v2/P0_L1_Aesthetic.md#当前切片与停止点)。[既有17项本地结果](Specialization_B149_P0L1_Readiness_Local.md)及[B148首次失败](Specialization_B148_P0L1_Native_Fail.md)按原范围保留。

## 原图与本次验收

5张原图已逐张查看，移动至Git忽略目录 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B149_P0L1_Rate_20261002/`。同目录manifest记录原名、顺序、字节数和移动前后核对的SHA256；截图不进入Git。

| 图 | 回合 | 本城事实 / 配置 | 全国当前旅游业绩 | 相对118 |
|---|---:|---|---:|---:|
| 1 | 58 | 巨作页5件、旅游合计30；未显示本项配置 | 125 | 不用于本项验收 |
| 2 | 59 | 同巨作页合计30；用户接受的对照基线 | 118 | 0 |
| 3 | 60 | ACTIVE3，2时代×2栋；预期/配置+4 | 122 | +4 |
| 4 | 62 | ACTIVE3，2时代×3栋；预期/配置+6 | 124 | +6 |
| 5 | 63 | ACTIVE3，1时代×3栋；预期/配置+3 | 121 | +3 |

已测三种组合的**可见旅游率及当前配置**符合K1、逐栋×本城当前时代数的预期；不是作品数量、D或全国时代集合。用户另报告完全重启后正常，作为USER_REPORTED冷加载保持记录；截图本身不独立证明冷启动过程。125→118本次有图1/2，原因未确定，用户不要求本轮追查；不写成已证明来自外部系统。

用户报告过回合中先回到118，再于本地回合开始恢复加值。没有对应事件时序、载体实例变化或累计旅游读数；因此尚未证明是UI刷新、引擎重评估或真实效果撤销，也不能据顶部回落宣布本能力永久不结算。掠夺/他城隔离等未在这五图中独立验证，不扩大PASS。

## 源码时序核对

- [CultureAesthetic](../../../../Mod/CultureAesthetic.lua)：`reconcile`比较已确认城市引用、binding token、逐plot金额以及master健康。相同计划/健康配置直接返回（114行附近），并非每回合先撤销再恢复；引用不包含回合号。`PlayerTurnActivated`提供就绪/核对，不是预定撤销阶段；模块没有PlayerTurnDeactivated/TurnEnd撤销入口。
- 只有实际配置变化、载体缺失/异常或明确不合法等路径才改变投影。变化时在同次同步reconcile中先撤master、改flags再建立，防止混合金额；这仍不能证明原生引擎何时将金额计入累计旅游。
- [GreatWorkFacts](../../../../Mod/GreatWorkFacts.lua)普通回合不清空已确认事实；UI本地回合采集不等于撤效。同一引用暂时UNKNOWN保留已核实配置，不能以UNKNOWN当0。加载或陌生引用另按原有保护处理。
- [总督门槛](../../../../Mod/Probe.lua)：六个原生Property一致但门槛降低时会得到KNOWN的较低ACTIVE；不一致则UNKNOWN。若回合间曾短暂出现一致的低门槛并触发Audit，会合法走撤销分支。**这是尚未观察到的候选原因**，不是确认根因；不据此延迟真实总督退出或改变Gameplay。
- 对照[科研基础设施](../../../../Mod/ResearchInfrastructure.lua)、[学以致用](../../../../Mod/ResearchApply.lua)、[学术主持](../../../../Mod/ResearchChair.lua)实际reconcile：删除不需要/位置错误/被掠夺bit，只补缺少的所需bit；相同健康配置不每回合全撤全建。未把该结论泛化为所有旧模块。

## 两个最小本地检查

复用既有`DevelopmentTests/test_culture_aesthetic.py`真实Lua/SQL fixture，在临时脚本追加两个检查；只读配置数据库复制到可丢弃副本，未修改源数据库、仓库测试或运行代码。Lupa2.8 / Lua5.5仍只是本地模拟环境，不是游戏Lua版本证明。

1. 连续三个本地PlayerTurnActivated、重复馆藏确认通知，再加入同引用UNKNOWN：两城既有+12配置保持；额外Property写入、master创建、删除均为0。**LOCAL_SIMULATION_PASS**。
2. 显式KNOWN ACTIVE3→2→3：目标城退出/恢复，各一次master删除/创建；另一城保持+12。**LOCAL_SIMULATION_PASS**。它证明候选分支可产生退出，不证明实机门槛真的短暂变化。

原17项结果继承，未重跑full/regression/stress。以上不能模拟C++旅游结算顺序，也不能以零Lua写入证明原生Modifier不会重新评估。

## 原生累计值入口与证据边界

实际安装的原版`Base/Assets/UI/TopPanel.lua`及Expansion2相应代码以`Player:GetStats():GetTourism()`显示当前旅游率；TurnBegin等UI刷新钩子不证明C++收益在其之前还是之后结算。

原版`Base/Assets/UI/PartialScreens/WorldRankings.lua`文化胜利列表将`PlayerCulture:GetTouristsFromTooltip(targetPlayer)`直接设置在来自该文明的游客数字/图标提示上。已经安装的Sukritact Tourism Overview（Workshop 2953909938，`UI/Suk_TourismOverview.lua`）也读取该tooltip，将前两个数字解释为当前对该文明的旅游率与累计旅游，并在外国游客转换提示中保留原文。这提供了可复用的只读观测路径；不是一个已确认的独立`GetTourismLifetime`接口。

该Mod解析器取本地化文字的前两个数、缺值补0；**本项目不能照搬该补0规则当证据**。实测必须看原提示中明确标注的累计值，保留原文；文字缺失/顺序不明则报告不可用，不伪造读数。安装不证明本局启用了该Mod；本轮未安装、启用或修改它，优先使用现有原版入口。

作者[旅游概览说明](https://steamcommunity.com/sharedfiles/filedetails/?id=2953909938)提供界面位置；作者维护的[PlayerCulture方法表](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerCulture)及[事件表](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/Events)没有给出Tourism累计的内部结算点相对于Lua事件的顺序。已查UI/公开记录不足以确认精确C++阶段，保留USER_GAME_TEST_REQUIRED，不能把PlayerTurnActivated、TurnBegin或Tourists整数变化当作证明。

## 一个最小结算核对

保持B149现有文化城ACTIVE3与馆藏/建筑/政策不变，不要求新测试包或旧长测。选一位已接触且关系稳定的外国主要文明，使用文化胜利页来自该文明的游客提示（如现有旅游概览已启用，也可用其对应转换提示）。只读**累计旅游C**和**对该文明当前旅游率E**；整数游客数和全国顶部当前率不能替代C。

1. 当前本地回合稳定后记C0/E0及本项配置；过一个完整回合，在相同阶段记C1/E1；再过一回合记C2/E2。不改变馆藏、总督、政策或商路，相关关系倍率应保持；如有其它世界变化使E不同，保留事实，不强算。
2. 同输入下检查两个实际累计增量是否与该文明已含本项加值的E一致。若需要对照，可复用同一开始存档的ACTIVE不足分支；不要把相邻回合不同世界状态直接相减，不能用全国118替代对该文明经过关系倍率的E。
3. 累计符合增强旅游率，才支持已测两回合真正结算；未计入增强贡献则停止并定域调查。提示没有明确累计值，或倍率/取样阶段变化无法区分时，只反馈一个原提示与原因，不继续泛化长测。

如现有UI不能回答，下一项应为另行授权的**单城、两回合被动时序诊断**：在已有生命周期/实际Audit入口记录ACTIVE/六个总督标记、master存在/健康、配置变化原因和原生累计提示；不主动Audit、不额外撤建、不建新永久账本/扫描器，记录有界并可关闭。目标区分实际withdraw/reapply与纯显示/原生重评估，不猜C++阶段。此处只是具体建议，本轮没有实施授权或运行代码改动。

## 当前停止点

记录已测可见加值PASS与用户报告的冷加载正常；实际每回合累计是否得到增强贡献仍是本项的唯一新增关键歧义。无新Gameplay决定，Design/K1/SQL/永久数据/GC保持。没有部署或新build，不开始L2/L3/M/N/U2；先用上述最小观测关闭时序门禁，必要时才授权定域诊断。
