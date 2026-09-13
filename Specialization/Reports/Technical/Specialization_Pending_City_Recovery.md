# 未确认城市提交：可序列化记录与只读恢复

Document Owner: Codex
Design Reference: D0007 / PROG / ELIG
Architecture Reference: A0036
Scope: MOCK_ONLY / RECORD_PLAN_ONLY

新增PendingCityRecovery.lua和test_pending_city_recovery.py。LOCAL_SIMULATION_PASS为本地模拟，不等于Civ VI实机。测试将Lua记录转换JSON，重新创建Lua VM后恢复检查，未写游戏Property。

记录schema=1、kind=MOCK_CITY_PENDING、state=PENDING，保存operationID、cityUID、owner、beforePresent、原事实、目标事实。beforePresent显式区分原值不存在与原表存在，避免Lua nil键在序列化中丢失歧义。校验同城owner和目标revision（初始化0，后续+1）；只支持有界普通字符串键表/有限标量，拒绝元表、超深结构等。不替代State对具体游戏事实规则的验证。

Create只生成RECORD_PLAN_ONLY；不生成真实operationID或持久写入。Inspect只读已保存记录和调用方MOCK同城观察，结果始终RECOVERY_HELD，细分BEFORE_OBSERVED、TARGET_OBSERVED、CONFLICT_OBSERVED、UNKNOWN。mayWrite/mayActivate/mayClearRecord均false。读到目标值也不能自行清记录或恢复收益；操作成功结束还需要明确提交协议。缺失/损坏记录不视为“无事发生”。

测试覆盖新VM中原值未写、已写目标未完成、第三方冲突、owner/代际/城市消失、读取失败、损坏schema/presence、重复检查不改变记录及revision非法。输入副本隔离，原记录保留。

## 与提交器的连接边界

本轮记录模型尚未接到CityOperationGate.CommitMock。下一步必须在任何城市数据写入前保存并读回确认PENDING记录；记录保存失败/未知时不允许城市写入。恢复读取必须先检查PENDING状态，再允许创建新提交器，不能先默认可写后才发现未确认操作。此排序尚未实现，不宣称当前重载已阻止真实写入。

恢复记录与城市事实若为两个Property，读回确认不等于跨Property原子持久化或崩溃保证；之后需评估同一envelope或可证明的保存顺序。不能自动将现有DEV Property升级为此schema。真实城市UID、事件边界、记录终结/清除策略、写入前后故障、部分持久化仍需接入与验证。记录不包含可重用运行许可；恢复后的许可仍须当前资格重建。

运行保持B018/modinfo25，无新实机测试/游戏PASS。Design、既有Source/Tests未改。备份与保护hash：DevelopmentBackups/Specialization-before-pending-recovery-record。未启动游戏、未改配置或UUID。[Status](../../Status/Specialization_P0_Status.md)为唯一当前任务入口。
