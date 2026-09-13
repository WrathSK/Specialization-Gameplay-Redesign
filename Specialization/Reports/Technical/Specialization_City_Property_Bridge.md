# 限定新城City Property连接：本地准备

Document Owner: Codex
Architecture Revision: A0042
Design Reference: D0007（未改）
Runtime: P0-B-019 / modinfo26（未改）
Verification: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS

## 本轮结果

新增DevelopmentTests/CityPropertyBridge.lua，直接组合既有CityOperationGate、UnifiedCityEnvelope、PendingCityRecovery和CityFactWritePlan；注入具有GetCity/GetOwner/GetID/GetX/GetY/GetProperty/SetProperty形状的mock对象及Binding.Resolve。不是运行代码，未登记modinfo，构造器严格要求MOCK_ONLY。

每城市独立通道/独立表；每次读写重新查询城市和绑定，校验owner/cityID/token/坐标。进入通道前必须取得资格许可，写前仍核对同一许可代次；失效后即使再次启用也不能沿用旧通道。读回用于判定已发生结果，不激活收益。初建空表必须有调用方提供的FRESH_BOUND_HISTORY_COMPLETE证据；读档无此证据只能恢复已有表，nil旧城不自动补写。

测试实际组合七个Lua模块，覆盖两城独立初始化、学院完成及重复通知、错城batch拒绝、JSON新VM对账、无历史旧城拒绝、资格失效时不访问城市、owner/token/坐标/城市删除改变、读取失败、写入丢失与写后异常。写PENDING期间资格失效后停止，保留PENDING且不写目标。新测试及六组回归共七脚本exit0。

LOCAL_SIMULATION_PASS仅为本地模拟。SOURCE中现有GetCity/Property/Binding回调路径属于STATIC_CONFIRMED静态证据，不是本连接层已通过游戏运行。此轮不新增USER_GAME_TEST_PASS，不要求用户测试。

## 实际源码调查与接入限制

1. B013 BindingProbe在确认新绑定后调用单个shared.OnFreshCityBinding。B015 CityJournalProbe赋值该槽；直接再赋值会覆盖已有处理。未来先建立有序事件分发，保留原处理与失败传播，不能悄悄抢占回调。
2. B015已对加载阶段、完整市中心、无已完成专业区域、区域替代族和事件对象做检查。本桥不重新实现这些检查；FRESH_BOUND_HISTORY_COMPLETE在本地由fixture提供，尚无真实adapter为它背书。不能把BOUND_MATCH单独当完整新城历史证据。
3. B013绑定仍受IsTestPlayer门控，B018许可仍为私有诊断对象。本桥注入的是本地EligibilityLifecycle，未使用UI共享诊断bool当正式许可。DEV可以限定测试载体；正式多玩家必须单独接通用资格与事件失效。
4. DONE仅证明上次成果与凭据匹配，不证明自上次保存以来所有完成事件都被观察。失去资格、加载顺序或回调异常造成漏通知时，不能凭DONE恢复历史连续性。真实事件adapter需有明确观察范围/暂停记录，尤其是未专业化城市，不能用当前区域列表猜首次通知。
5. token+owner/cityID/坐标只适用于本次限定同owner候选通道，跨owner永久UID未解决。读取后再查身份和写前许可复核不构成引擎锁或崩溃原子性。没有资源消费、Settler投资或任何专业收益。

## 下一步范围

下一项先准备实际新城事件与连接层之间的有序分发/完整历史证据入口：保留B015、加载事件不建新城、不能回补旧城，失败时不继续把较晚通知当首个通知。将其与本桥在本地组合后，才准备新的最小DEV运行批次。B019/B015已通过的普通保存和截图无需重测，B010继续延后。不是新增游戏设计待决；若技术fallback会改变PROG-005或ELIG规则，另行报告用户。

备份/执行输出/保护hash：DevelopmentBackups/Specialization-before-city-property-bridge。运行包、既有Tests及Design均未改；未启动游戏。
