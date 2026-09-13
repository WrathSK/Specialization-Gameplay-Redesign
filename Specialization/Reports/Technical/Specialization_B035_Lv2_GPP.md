# B035：共同Lv2专家基础伟人点数

Document Owner: Codex
Design Reference: D0010 / SHARED-002；四类v0.1专业
Implementation: P0-B-035 / modinfo43
State: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 实现范围

`Lv2GPP.lua`消费EffectiveFacts，要求对应完整标准专业区域及ACTIVE≥2，以该区域plot:GetWorkerCount读取实际工作人数。Research/Culture/Industry/Commerce均接入；文化同时对应三种伟人。无Identity、不满足总督门槛、无工作人员不增加点数。尚未支持通用Conquest/Claim身份来源与全部独有区域，沿用当前DEV范围；D0010未被改写。

SQL使用`Building_GreatPersonPoints`原生基础来源，不调用ChangePointsTotal或每回合直接奖励。32种内部建筑，按对应专业区域放置，二进制权重表示工作人数；每份权重贡献2基础点数，文化各类同时贡献。先去掉多余权重/错误专业载体，再补缺。重复刷新不重复添加点数；不保存新永久事实，载体只表示当前派生状态。当前支持0–255名专家，超界明确报错并撤销本模块载体，不截断/静默改变数值；该工程上限远高于当前测试配置的岗位数量。

新增建筑Housing=0、CitizenSlots=0、无CitizenYieldChanges，不改变已通过的Lv1岗位支持和B034住房。其PrereqDistrict为对应区域，而不是市中心，保留原生所属区域关联。原生基础点数能否完整接受所有城市/玩家百分比效果，必须由实机确认；本轮没有声称倍率已通过。

## HD数据库与加载顺序

当前只读DebugGameplay.sqlite中，HD已为本轮四专业专家提供每类2基础GPP（Culture各三类均2）。因此无其它倍率时0→1工作人员的总增量应为4，其中HD原有2、本项目新增2；不能错误地把总增量4当成双发。

HD UpdateDataBase/DL_GreatPersonPointsDouble.sql含全局`Building_GreatPersonPoints *= 2`，DL.modinfo中DL_GPPDouble为LoadOrder16008。本模块SQL放在10001000（高于本次本机HD所有LoadOrder的最大值10000000），定义准确增量；运行首次检查32种建筑及48条点数记录，数值/类别不匹配时报B035_BASE_GPP_DATABASE_MISMATCH，不接受意外加倍。后续其它Mod加载顺序仍须依最终数据库核对，当前不宣称任意Mod组合保证。

## 自动刷新与UI分工

Gameplay监听工作人员/城市focus、总督、回合、转移及建造事件；load-close重建，投资动作后也重核。内部busy保护避免创建/删除建筑事件重入。持有旧载体但新事实无效时移除；单城错误不阻断其它城市，后续真实事件允许重新读取恢复。

`UI/GPPRefresh.xml/lua`为独立InGame后台context，没有控件和打开窗口要求。它将工作人员/focus/总督变化合并为dirty通知，在publish/playback complete或SystemUpdateUI发送`LV2_GPP_DIRTY`，load/回合也可发送。请求只带Action/Token，不携带人数、产出或专业事实；Gameplay重新完整读取。此路径借用已使用的后台UI调度方式，但B035自身时序仍须实测。

该后台动作在普通诊断请求之前分流，不能覆盖当前Snapshot/LastToken，非测试玩家不能触发。无dirty不重复发送；关闭context解除监听。不是依靠打开Great People UI来启用收益，也没有把UI数据升级为专业事实权威。

## 诊断

面板增高44以保留全部旧按钮，新增`Read Lv2 GPP`。读取不触发Audit、不修复状态。报告分开显示：实际工作人员、expected新增基础点数、按HasBuilding计算的carrier基础点数、其它专业残留载体计数、刷新/变更次数。

Gameplay的全国点数Getter只作可失败诊断。面板收到匹配ACK后，GPPReadout在UI Context以`player:GetGreatPeoplePoints():GetPointsPerTurn(class.Index)`重新采样全国每回合点数，标记`UI EMPIRE GPP/turn`，不将其传回Gameplay结算。此UI Getter在独立CityGPPProbe源码中已有使用先例；没有修改或依赖该Mod。UNKNOWN不当0；如无读数则用原生伟人界面观察。全国读数包含其它城市/效果，不能称为选中城市贡献。

## 本地证据

STATIC_CONFIRMED（代码/数据库证据，不是游戏PASS）：实际HD schema内存副本执行SQL，32建筑/48点数行；配置类别/数值/岗位/住房隔离；加载顺序、manifest路径、UUID、全Lua语法和XML唯一按钮ID。Make_Hash为本地stub，不能当真实引擎hash验证。

LOCAL_SIMULATION_PASS（模拟，不是实机）：test_lv2_gpp.py执行实际Lua与SQL定义，覆盖四专业0/1/2/3/4人数、文化三类、同类重复/异类移除、总督撤销、重载重建、无效事实清理/恢复、超界拒绝、加载顺序误加倍拒绝、只读诊断、实际Gameplay动作分发、无控件后台发送及去重/关闭、UI只读全国率。

倍率算术断言只是fixture预期，不证明Civ VI的真实Modifier叠加。

旧投资/EffectiveFacts回归通过（只在内存适配版本及提示文本），含原Lv1生命周期和网络回归；B034实际住房Lua部分回归通过。旧Tests文件未改。没有为本轮label变化反复跑已完成的全部老SQL测试，住房旧SQL也未改。

USER_GAME_TEST_REQUIRED：实际基础GPP增减、工作人数事件/后台时序、Culture三类、百分比作用及正常读档。仅派[B035一组三案](../../Status/Validation/Cases/B035_Lv2_GPP.md)，不重测整个住房/征服/商路。住房已接受的刷新延迟不扩大成对任何GPP错误的接受。

## 保护与后续

备份DevelopmentBackups/Specialization-before-B035-gpp。D0010/hash、UUID、游戏配置、旧Tests/冻结证据保持；未启动Civ VI。本次只接共同Lv2 GPP，未接其它高级收益或重新开展小数/Commerce IV。若倍率未通过，调查原生基础来源/结算路径，不改为不吃倍率的直接点数奖励。
