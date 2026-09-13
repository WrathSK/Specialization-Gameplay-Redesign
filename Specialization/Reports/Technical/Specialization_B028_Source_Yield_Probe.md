# B028：商业IV前置只读产出探针

Document Owner: Codex
Architecture Revision: A0062
Runtime: P0-B-028 / modinfo35
Design: D0009（条件总产出研究授权见前一报告，未改Spec）

新增SourceYieldProbe.lua，Gameplay中对已验证owned test city执行GetYield，分别显示S/C/P六位小数，仅用于诊断展示；内部直接读引擎数值，不把显示舍入作为实际应用规则。优先YieldTypes，缺失时查询GameInfo.Yields的Index；每yield独立pcall与有限值检查，异常显式UNKNOWN。显示真实专业记录或UNKNOWN，不伪造Lv4/ACTIVE。

SOURCE_YIELDS使用既有窄请求、选中cityID/owner/测试玩家过滤、Token ACK。新增Read source totals按钮位于Read auto Lv1左侧空位，无需贸易面板。没有持久Property/Modifier/收益写入，仅更新既有诊断快照；不把来源读取成功等同于直接网络来源或合法Convergence资格。

LOCAL_SIMULATION_PASS：test_source_yield_probe.py验证真实模块三yield读数、重复读取与状态改变、部分读取失败/NaN、owner过滤、枚举fallback、真实Gameplay请求分发，全部Lua语法、XML和manifest include/import。test_background_network_sender.py回归通过。游戏上下文Getter数值/刷新仍需用户确认。

当前实现边界回答：运行已有标准Research/Culture/Commerce的自动Lv1 3F3P，以及限定DEV专业身份/网络拓扑。高级Potential投资、正式总督ACTIVE门控及Lv2–4收益未集成为可玩系统；总督条件读取等已做过探针验证不等于高级能力落地。Commerce IV仍是离线计划；本次只是原值读取，没有20%应用。Industry Lv1/施工队、Boost、购买折扣、Great Work未由本轮启用。

[一个用户测试](../../Status/Validation/Cases/B028_Source_Totals.md)：现有科研城读前后两次，市民调配改变科技后对照；无需升级专业。Design、SQL、自动Lv1模块、NetworkBridge与NetworkSender保持不变。下一步依读数证据继续basis和产出承载研究，不能把getter通过扩大为防循环或倍率正确。
