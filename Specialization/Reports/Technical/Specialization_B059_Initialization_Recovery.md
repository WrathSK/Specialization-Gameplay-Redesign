# B059.79：初始化恢复与错误可见性

Document Owner: Codex
Design: D0022 unchanged
Build: P0-B-059.79 / modinfo79

用户已确认78性能正常，但单图WAIT_ACK/未初始化。Init在全Players循环中直接p:GetCities():Members()，未覆盖无城市集合的玩家。修复为先取cities并检查，再清理拥有城市；不改变其它Mod/玩家事实。旧逻辑在此抛错时尚未更新seq，UI永远只能等待，本轮将合法请求的ACK记录提前，pcall初始化并报告错误，后台不会因失败恢复高频发送。

Game侧received元数据和stage记录RECEIVED/INITIALIZED/ACCEPTED/REJECTED_SAMPLE/INIT_FAILED/REJECTED_GENERATION。无城市结果时面板显示ready、ACK、received seq、expected/received generation与errors；外层Receive异常也可见。正常D/收益报告不增加冗余。UI刷新实现未改，性能修复保护保持。

测试DevelopmentTests/test_b059_init_recovery.py构造Players[63].GetCities=nil，验证正常接收；故意Init抛错仍ACK并明确报告；恢复后新事件重新初始化；generation异常可见。复用78延迟ACK/空闲不扫描与B059/B058等回归。新测试最初嵌套版本字符串与Lua夹具引用适配失误已修正，未降低机制断言。

STATIC_CONFIRMED/LOCAL_SIMULATION_PASS不等于实机恢复已通过。无Lua.log；单张图不能确定唯一异常来源，若复验仍失败，按新诊断定位，不能一律猜旧存档不兼容。已有Modding.log包含Dialogue.sql加载记录，不证明Lua成功。

新增测试/本报告/截图结果；修改Dialogue.lua、Gameplay.lua、Probe/P0PanelXML/modinfo版本、Architecture/Status/索引。D0022/SQL/倍率公式不变；原图已SHA核对归档，其它投递文件未读取。源码备份local/before-b059-79，未启动游戏/commit/push。
