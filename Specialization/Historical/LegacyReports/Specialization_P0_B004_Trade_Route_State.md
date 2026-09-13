# P0-B-004 Trade Route State：调查、实现与证据

## CURRENT AUTHORITATIVE STATE

2026-09-11。结论：**未找到已确认可用的纯Gameplay当前路线全集接口**。不能回答“已经可靠自动重建”。本轮交付的状态层及拓扑层是可替换provider的离线原型；运行包增加自动只读candidate instrumentation，不授予任何收益、不写路线Property、不读取UI快照、不把事件变成路线。

最佳已证实的全集读取是UI城市出站枚举，但不符合用户本轮权威要求。优先调查的新纯Gameplay候选是玩家单位全集→商人当前operation/参数；其一一对应、端点保留与生命周期未证实，只能标USER_GAME_TEST_REQUIRED。没有在getter失败时静默切换UI或事件账本。

## CONFIRMED / STATIC_CONFIRMED：本机证据

| 对象/路径 | 实际找到什么 | 不能据此推断什么 |
|---|---|---|
| 官方Pirates AddGameplayScripts | [PiratesScenario.modinfo:167](</Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/DLC/PiratesScenario/PiratesScenario.modinfo:167>) 注册StartScript；[PiratesScenario_StartScript.lua:802](</Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/DLC/PiratesScenario/Scripts/PiratesScenario_StartScript.lua:802>) 调用pPlayer:GetTrade():CountOutgoingRoutes()，GetOutgoingRouteCapacity()；828行Game.GetTradeManager():CanStartRoute(...) | Count是标量，不给路线ID/方向；CanStartRoute是潜在创建合法性，不是已有路线存在性 |
| 官方TradeOverview | [TradeOverview.lua:70](</Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI/TradeOverview.lua:70>) 遍历城市GetOutgoingRoutes；玩家计数使用GetNumOutgoingRoutes（与Gameplay CountOutgoingRoutes不同） | UI method不可推定Gameplay存在 |
| 官方TradeSupport | [TradeSupport.lua:1](</Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI/TradeSupport.lua:1>) 判定商人是否闲置仍遍历城市出站表并匹配TraderUnitID | 官方UI并没有展示一个可直接替代城市枚举的商人当前路线getter |
| 官方TradeRouteChooser | [TradeRouteChooser.lua:215](</Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI/Choosers/TradeRouteChooser.lua:215>) GetLastOriginTradeCityComponentID/GetLastDestinationTradeCityComponentID用于重复上次路线；849行附近PARAM_X0/Y0为目标、X1/Y1为起点坐标的请求参数 | Last endpoints是历史；operation请求参数不保证运行中/读档后仍保留，也不能把CanStartRoute当active |
| HD Temp_Interface | [DL.modinfo:1895](</Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/DL.modinfo:1895>) 是AddUserInterfaces/ImportFiles，[Temp_Interface.lua:303](</Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/Gameplay/Temp_Interface.lua:303>) GetFreightAmount调用城市Outgoing/Incoming | 虽在Gameplay目录，实际属于UI执行桥接，撤销旧“官方/HD Gameplay枚举先例”理解 |
| HD事件 | [Buildings.lua:147](</Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/Gameplay/Buildings.lua:147>) 新增/活动回调前五参数；官方Pirates 1223/1616行GameEvents.TradeRoutePlundered | 已测新增事件能给端点；不能推定覆盖全部终止/取消/加载/撤销，不能推定附带stable route ID |
| Treasury | 本机Lua用其读取余额/收入/维护费；未发现路线全集方法 | 不能从商路收入反推路线集合 |
| Game_TradeManager.csv | 当前文件有Route Started及城市名/产出列 | 是日志历史，无完整稳定身份/当前性契约，不作为runtime来源 |

UI路径已经追到Lua调用边界：`TradeOverview/TradeSupport → City:GetTrade() → GetOutgoingRoutes()`，不是再调用某个可见Lua wrapper的全集函数。Getter实现位于编译引擎，磁盘上未提供对应C++实现。引擎内部当然维护真实路线，但没有证据其集合可在Gameplay Lua直接枚举。

只读扫描本机GameCore_XP2.dll字符串，发现Cache_Lua_ICityTrade附近GetOutgoingRoutes/GetIncomingRoutes；Cache_Lua_IUnitTrade附近两个GetLast...；Lua_IPlayerTrade附近CountOutgoingRoutes；Lua_IUnit附近GetOperationType/GetOperationParameter。Cache与非Cache绑定名称支持“两个context暴露不同接口”的判断，但字符串位置不是完整方法注册表或运行验证。

扫描中没有发现可用的Gameplay GetTradeRoutes/稳定route ID完整枚举先例。TradeManager可见方法以CanStartRoute/IsRouteAllowed、潜在收益/路径计算为主；这些结果不证明实际已派出路线。未做注入、反编译修改或游戏进程访问。

### 生命周期能确认到哪一层

| 生命周期 | 可见读取/通知证据 | 本轮处理与缺口 |
|---|---|---|
| load | UI重新枚举可读取现有路线（用户PASS）；HD Gameplay CityYield.lua:177使用LoadScreenClose做缓存初始化 | B004分别在Gameplay初始化和LoadScreenClose自动采样，事件上下文/就绪仍实测 |
| route start | 用户确认TradeRouteActivityChanged端点可用 | 仅dirty，不创建正式route |
| completed/cancelled | UI既有全集在刷新时重新枚举；单位operation相关通知可作为候选dirty | 未找到完整官方Gameplay删除/枚举Lua，不假定某个event等于完成 |
| war | HD Gameplay使用DiplomacyDeclareWar；潜在路线合法性有外交检查 | 状态原型有战争核验；具体路由删除/通知时序待实测 |
| capture/raze | HD Gameplay CityConquered、CityAdded/Removed等事件先例；端点ID/owner可能改变 | 旧owner/失效端点撤销，不能偷偷重新指向新主人；稳定UID迁移另案 |
| trader destroyed/plundered | UnitRemovedFromMap、官方TradeRoutePlundered先例 | dirty后必须重新读真实源；事件本身不是唯一删除依据 |

上表不是引擎内部实现说明：没有本机可读C++源码可证明其具体调用链和先后顺序。

## 本轮实现

### 离线TradeRouteState（不注册modinfo）

`DevelopmentTests/TradeRouteState.lua`提供New/MarkDirty/Refresh/Read。未来已审计provider必须返回完整、稠密、标量字段的snapshot，附COMPLETE + GAMEPLAY + GAMEPLAY_CURRENT与sourceID。测试用MOCK明示该身份；任何真实candidate在确认前不得标此契约。

刷新成功时normalize+原子替换；消失路线自动移除。空全集是READY/count=0；错误/部分列表/未知端点解析是UNKNOWN，不复用lastGood。明确端点不存在、owner变化、战争或current=false则剔除。dirty期间Read也不暴露旧集合为有效。

记录字段：key、identityKind、可选engineRouteID/traderUnitID；两个端点的player/cityID/稳定UID；domestic、current、validity。正常列举只保留业务必需标量，无UI名称、路径、yield对象。

尚无稳定engine route ID证据。若provider以后提供稳定ID，优先使用；否则使用owner+traderID+两端稳定UID的复合snapshot key。同城对多个商人不合并；同一个商人对应不同路线或同routeID内容冲突时报错。该key不是永久任务ID，不能防止所有未来ID复用；派生缓存无需继承旧任务历史。

CityUID由独立resolver输入；当前引擎owner/cityID与UID映射不等价。没有擅自把所有权变化当成城市UID稳定通过。本轮不创建/迁移永久CityUID，相关测试用fixture明确模拟新世代。

### NetworkState（不注册modinfo）

`DevelopmentTests/NetworkState.lua`每次从READY routes和显式roles/sources重新计算：

- sources[sourceUID]：kind、owner、activeLevel、templateRevision；
- centers[centerUID]：connectedSources及每个来源的接入资格，distributionRoutes；
- recipients[kind][cityUID]：source并集、center并集、按center/source细分的接收资格；
- routeRevision与contextRevision分开，ACTIVE/中心/模板变化不篡改路线事实；
- recipientCounts只按集合去重；没有Boost、L合并、折扣或产出。

输入可以显式表达本地接入或Commerce IV免费接收资格，仅用于离线去重/撤销模拟，不启用运行机制。不同来源完整保留：以后无论讨论统一代表源、按源分配覆盖、或另定义合成规则，都不需重做路线存档。它不选max/average/sum，不进行逐中心sqrt求和。Industry保留模板版本及来源，不合并折扣/生产。

### B004运行探针（候选，非正式provider）

`TradeRouteProbe.lua`仅在Gameplay执行：Game.GetPlayers→测试玩家GetTrade.CountOutgoingRoutes→GetUnits.Members→MakeTradeRoute单位→GetOperationType；只对匹配MAKE_TRADE_ROUTE的任务读取PARAM_X0/Y0/X1/Y1，所有取值均视为candidate。没有调用历史last endpoints，没有城市GetTrade重试，也没有读取UI。

初始化、LoadScreenClose、测试玩家PlayerTurnActivated/Deactivated自动扫描；活动/删除/战争/城市/掠夺事件只设置合并dirty原因，不解析payload成路线。此probe的回合调度只是调查用；如果以后provider成立，正式效果结算前需要可靠安全边界的dirty flush，不把“等下一回合”当最终即时撤销方案。

只枚举已知单位集合及命名标量字段，不遍历engine对象/元表；有玩家、单位、商人上限，异常报告UNKNOWN/UNAVAILABLE；不截取部分列表当全集。不启动任何游戏。日志每次输出采样原因，明细只在变化或load/initialize打印。新增Route state (Game)按钮只查看ExposedMembers里的诊断文本，无请求/refresh调用；它不是状态初始化开关。

## LOCAL_SIMULATION_PASS

两个新增测试与既有三个测试均已通过。空/单/多起点/多终点/同城对独立商人/重复刷新/单独撤销/易主/毁灭/无效端点/load清空重建/错误缓存覆盖/重复dirty/中心身份变化/ACTIVE变化均有fixture。另测未知源不能伪装空集、UI与事件源拒绝、冲突ID、不同接收资格撤销、非递归转发及多源保留。详见Status与测试文件。

这些是模型契约和探针调度的模拟，不证明实际operation与active route的一一映射。

## USER_GAME_TEST_REQUIRED / BLOCKED

B004最多一个小批，详见Batch_B004：先在已有四商路存档读取自动初始化与读档日志；如果候选缺失/匹配失败即停止。本次只判定candidate是否值得继续，不能直接给正式Route State登记USER_GAME_TEST_PASS。

若单位operation不提供可用端点，严格纯Gameplay来源继续BLOCKED。次优研究方向：原生动态collection/Requirement是否能提供实时成员事实（目前没有路线ID/端点导出的证明）；若仅能表达连通性，也不等价于Route records。独立后台UI桥接可免开面板，但依然依赖UI snapshot，**违反本轮约束，未实现**。事件持久化+计数也不能识别同数量路线替换，因此不采用。

## HISTORICAL NOTES / superseded

Architecture/Status旧全文保存Historical目录。原来把HD Temp_Interface当Gameplay先例的描述已纠正；所有旧线性/逐路百分点/Commerce IV固定增加/多中心求和、以及旧工业加总与最高折扣提案，不能覆盖当前未定多源规则。已通过基础接口不再列为当前待测。

日志交付补充：本机目前未发现Lua.log，因此B004面板同时显示最多6名商人的原始task/坐标参数（匹配项优先）。用户以默认文件名截图即可；不要求启用未知日志选项。打印仍保留，但不承诺Mac将print写成Lua.log。
