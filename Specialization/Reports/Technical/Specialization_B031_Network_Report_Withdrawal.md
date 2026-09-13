# B031 网络可读性与撤销验证

Document Owner: Codex
Build: P0-B-031 / modinfo38
Design: D0009 unchanged
State: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 工作选择

用户要求小数承载列后续研究、先推进其它合适待办。本轮恢复此前网络可读性与撤销任务，不再继续B030，也不取整或更改Commerce IV；B010仍暂停。

## 实现

NetworkBridge.Read输出中文概况，分别列本中心接入来源数、全国去重接收城市数、本城是否接收。显示城市名称及ID、当前玩家路线总数、本城有效分发路线数；没有来源的中心出发路线不计有效分发。仅现有DEV Lv1网络模型，不声称已读正式ACTIVE等级。

网络明细按钮经NETWORK_DETAIL Gameplay请求调用同一只读重建，列接入来源、接收来源和相关商路方向，按文本稳定排序，每页3项，连续点击翻页。概况重置本城明细页；明细内容变化重置第一页。每个来源以城市名和ID识别，接收来源不能作为可转发来源。多条相同端点的路线明细可相同，路线总数仍按真实路线条目，城市N继续去重。

读取前额外核对Gameplay当前路线计数，不匹配时显示待刷新，不展示旧资格。原接收验证、全量替换、derived模型和后台发送器未改；本次读数保护不是完整事件回调撤销的实机证明。端点owner失效仍由derive拒绝；同数量换线依赖后台signal/全集更新，不能由数量相同证明快照新鲜。

UI将暂停的小数加档按钮改为网络明细，保留Carrier OFF清理已有测试状态；SQL和固定收益模块没有修改，旧CARRIER_STEP入口保留但不再有该UI按钮。运行UUID、Design、自动Lv1、NetworkSender/BackgroundRoutes不变，无正式网络收益，无新数据库定义，因此无需新开游戏。

## 本地验证

新增test_network_report_withdrawal.py执行实际NetworkBridge：D0009直接接收、首都自身、多个来源、重复目的地去重、receive-only不转发、重叠资格失去其中一路、分发撤销只删目的地且保留中心、全部来源消失、空集合、新load丢弃故意错误缓存、重复Seq拒绝、partial拒绝、计数失配/owner失配拒绝显示、城市名与分页循环/重置均通过。实际Gameplay新action分发验证通过。首次测试错误假设路线一定排在第二页，修正为跨两页查找方向后通过；运行排序未为测试改变。

所有Lua语法、XML及ID唯一性、manifest文件引用/UUID/version38通过。test_background_network_sender.py回归通过，验证实际后台collector在无可见面板操作时提交完整批次、删除替换等模拟。以上LOCAL_SIMULATION_PASS不等于实机撤销。

本轮唯一实机案例：[B031断路](../../Status/Validation/Cases/B031_Network_Withdrawal.md)。只验证新报告可读性及实际撤销，不重测已过的普通连接/分页API。截图结果返回前不增加USER_GAME_TEST_PASS。
