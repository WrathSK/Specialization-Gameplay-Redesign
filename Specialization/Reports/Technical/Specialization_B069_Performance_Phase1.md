# B069.96 Performance Phase 1

Document Owner: Codex
Status: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED; PERFORMANCE BLOCKER OPEN
Design: D0025 unchanged

## 本轮范围与行为

仅修最强的网络dirty→空→恢复链，并记录性能计数。未改任何SQL/玩法值；无shared derive缓存、Commerce全世界循环/Copy/标准化重构、所有权恢复或收据清理。

- TradeRouteProbe的UnitOperation/Removed只有live unit明确MakeTradeRoute=false时忽略；单位已删除、字段未知、API失败时不能猜非商人，保留重新核对信号。无即时Lv3 Audit。
- UI collector仍用当前已批准GetOutgoingRoutes完整集合+总数前后校验、端点校验和规范化。NEEDS_REVALIDATION不清空public.snapshot，不触发正式空包。仅初始化尚无快照时UNKNOWN。
- 新完整集合按排序后的owner/trader/origin/destination复合key比较。相同内容不增加正式revision、sender不发包；receiver也重复核对内容，重复包不derive或Audit。
- 取消10秒无依据主动失效定时器。仍以事件和本地turn边界完整核对，不换成轮询provider。保留3次采样批次上限；新真实事件/下一回合可再核对。
- 新包先在局部变量中验证/derive，成功后一次替换；坏包不覆盖旧集合。有效新增允许在下一完整读取前维持旧有效路线。
- 端点缺失/易主、关联商人不存在、已证交战可确认旧路线失效；失败3次后只发送一次证据核对请求，Gameplay可用原生数量下降确认旧集合已不再有效。该请求不含伪造路线，不是新Gameplay provider。无法定位所有剩余路线时会将旧集合标CONFIRMED_INVALID，等待完整源恢复；不把它宣称成权威零路线。完整替换后revision增加。
- incoming包仍需当前turn/signal；消费者不再仅凭turn/signal变动拒绝最近完整集合。只对明确原生失效证据撤销。ACTIVE/身份变化的原有重算保留，未缓存掉它们。
- Sender先占用单个in-flight再请求；ACK后释放。明确失败同回合停止重发；下一回合重新核对可恢复。普通idle且ACK完成不再调用sender。未证明native实际队列行为，实机短测观察峰值/收敛。

## 计数合同

PerformanceCounters固定28项（实际以names数组为准），每项current/total/previous/peak；只有回合切换时重置固定数组，不随回合建立历史表。高频Count只查固定key、读回合及整数加法；无字符串/IO/事件/大表/城市扫描。Flight只更新两个标量。Counter关闭不影响原方法调用和游戏规则。

直接Lua写入点通过P.CreateBuilding/RemoveBuilding/SetProperty转发，先计数后保持原参数/返回/异常；HasBuilding检查也计数。是调用尝试数，不伪称成功次数或引擎全局操作数。原生Modifier的内部Property更新和其它Mod写入不可直接观测。已隔离的三个所有权模块不添加计数、不启动。

city/district计数记录已标注原生Members/collector循环访问；不估算原生API内部枚举。Unit callbacks针对本轮路由Game/UI监听，可能同一次任务两个context各计一次。Audit按Lv3、Boost、StandardizationDiscount、Commerce、Copy入口计；busy计数包含未ready门控。读取面板纯读共享标量，不发Gameplay请求。Network、city count等完整缓存生命周期下一阶段再处理，不为诊断扫描更多数据。

## Runtime audit log安全回退

**本轮不启用自动log。**本机原版Lua搜索未找到可直接沿用并验证的独立文件写入+session/大小限制API；现有可靠路径仅print原生日志，无法由本Mod安全独立控制文件大小/轮转，且现环境此前未取得稳定Lua.log证据。未采用io.open路径猜测、DB/Property存日志，也不把print到全局日志说成有界session文件。

依用户J10/J12“风险过高优先Counters”，不增加自动逐事件/逐turn输出或失败retry；没有session log需用户提交。手动Snapshot一次生成详细计数文本并print，只有明确按钮操作发生；当前没有做独立session趋势回看承诺。未来可另研究受控host日志收集，不在这次性能修复引入新常驻进程或配置。

## 本地验证

`DevelopmentTests/test_b069_performance.py`直接加载真实Probe/counter/TradeRouteProbe/BackgroundRoutes/ShadowRouteState/NetworkSender/NetworkBridge/CommerceConvergence，而非只测试重新编写的模型。

- 已有Research→Commerce收益8；10次已知普通单位任务+通用publish/playback/System通知：route_scan、derive、publication及原生Create/Remove/Property增量均0，正式网络始终可用。
- 10次无法识别单位：可以补读，相同集合不发送/derive、不建拆；没有空发布。
- 真新增/删除完整集合分别增加一次revision；删除A不重建未变B的收益。
- 临时读取异常最多3次/批，之后通用通知不无限重试；旧有效集合保留。
- 明确端点删除、失败读取后原生计数下降会撤销，不永久保留旧路线。
- 无ACK的同步重入只发1个请求；拒绝ACK不在同回合无限重发。
- turn本身不删除verified topology；10000个模拟turn后计数器表节点数不增，无自动print/IO，禁用counter后不累加。
- 全部Lua可编译，modinfo文件引用存在，UUID不变。
- 104个非核心目标文件去掉机械计数/转发后与备份内容一致；全部Data SQL逐字节不变。当前测试不冒充此前所有历史脚本的全量PASS（其旧revision/失效语义断言已经过期）。

当前只证明局部事件模型与调用语义，非实机事件频率/声效/长期原生内存。End Turn其它模块的旧turn采样和扫描热点仍待counter证据；本轮不关闭70GB问题。

## 恢复点与短测

恢复点：`local/before-b069-96/Mod` + `hashes.json`，原B068.95完整保留。部署通过tools/deploy.py已验证hash的事务，另保留运行包备份；不commit/push。

短测见[用户步骤](../../Status/Validation/Specialization_B069_User_Tests.md)。三张Counter截图即可。UIpolish、小标识调整及所有非性能工作继续暂停。

## 修改文件

下列Mod修改多数仅为计数原调用转发；没有将稳定玩法重写为新模块。

- `Mod/BindingProbe.lua`
- `Mod/CityFlowProbe.lua`
- `Mod/CityJournalProbe.lua`
- `Mod/CommerceConvergence.lua`
- `Mod/CompletionRecordProbe.lua`
- `Mod/CopyYields.lua`
- `Mod/CrewProjects.lua`
- `Mod/Dialogue.lua`
- `Mod/DialogueModel.lua`
- `Mod/EffectiveFacts.lua`
- `Mod/EnvelopeProbe.lua`
- `Mod/Gameplay.lua`
- `Mod/GreatWorkAdjacency.lua`
- `Mod/GreatWorkAdjacencyModel.lua`
- `Mod/GreatWorkProbe.lua`
- `Mod/HalfYieldProbe.lua`
- `Mod/IndustrySupport.lua`
- `Mod/InvestmentAction.lua`
- `Mod/Lv2GPP.lua`
- `Mod/Lv2Housing.lua`
- `Mod/Lv3Effects.lua`
- `Mod/Lv3Support.lua`
- `Mod/Lv4CopyRead.lua`
- `Mod/Lv4Percent.lua`
- `Mod/NetworkBoost.lua`
- `Mod/NetworkBridge.lua`
- `Mod/NetworkSender.lua`
- `Mod/PerformanceCounters.lua`
- `Mod/Probe.lua`
- `Mod/PurchaseProbe.lua`
- `Mod/PurchaseProbeRead.lua`
- `Mod/ResearchSupport.lua`
- `Mod/SpecializationP0.modinfo`
- `Mod/Standardization.lua`
- `Mod/StandardizationDiscount.lua`
- `Mod/StorageProbe.lua`
- `Mod/TradeRouteProbe.lua`
- `Mod/UI/BackgroundRoutes.lua`
- `Mod/UI/BoostGreatWorkRead.lua`
- `Mod/UI/CopyYieldRefresh.lua`
- `Mod/UI/DialogueRefresh.lua`
- `Mod/UI/GreatWorkBasis.lua`
- `Mod/UI/IndustryRefresh.lua`
- `Mod/UI/P0Panel.lua`
- `Mod/UI/P0Panel.xml`
- `Mod/UnitActions.lua`
- `Mod/UnitSiteProbe.lua`
- `Mod/UnitTargets.lua`
- `Mod/YieldCarrierProbe.lua`

此外：新增Performance事件测试；更新Status S0167、Architecture A0148、README版本路由；旧文档冻结快照；新增本报告及短测步骤。Accepted Design/hash保持不变。

## 部署核对

B069.96 / modinfo96，115 files，canonical与runtime逐文件一致。部署摘要SHA256：`7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`。原部署B068.95摘要：`f64f47159cf361d65784e791a3e2342a8aed49c3afa409f2c4d3d601bc1dada8`。事务保留副本目录尾名`.SpecializationP0-backup-jcna_u9l`（外部SpecializationDeploymentBackups）。部署后再次check identical=true；没有启动Civ VI、修改游戏配置、commit或push。
