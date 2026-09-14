# B069.96 第一阶段性能短测

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED（需用户实机确认；性能阻塞尚未解除）

使用已有商路网络的简单测试存档即可，不要求新局或继续长局。存档里的正常收益保留；完整退出后再启动以加载B069.96。

1. 载入，选一个己方城市，打开左上专业化诊断，点 **Read Performance Counters**。截图①。顶部应B069；revision至少1、routes与已知当前路线数量相符；若一直未初始化或卡顿加剧，停止回传。
2. 选择普通战士/侦察兵等非商人，移动约10次。不改商路、总督、人口或城市；可以用多个普通单位凑10次，尽量同一回合完成。
3. 点同一 **Read Performance Counters**，截图②。报告直接读固定计数，不触发Gameplay请求或路线重建。
4. 只过一个回合，再读Counters，截图③。到此停止短测，不要求长时间游玩。

回传：三张Counter报告 + 移动时是否还有城市建筑光效/声音 + 是否明显停顿。异常另截图；无需抄内部ID或复制原生大日志。

## 判据

截图②与①比较累计Total（每个字段斜杠后的值）：
- building_create、building_remove、property_write差值均0。
- publication、revision不变，正式网络不被清空。
- 已识别非商人时route_scan不增加；无法识别导致补核对时允许same_snapshot增加，但不能引起收益建拆。
- 没有伴随移动的城市建筑光效/声音或明显停顿。
- in-flight应回到0；不应闲置时不断发送/发布。

截图③用来定位End Turn仍有多少Audit/扫描/建拆，不能把自然人口/建筑变化与普通移动混为一谈。它也不构成70GB内存问题已解决的证明。

任一核心判据不符即本阶段未通过；不重复长测。非商人识别若返回未知导致有限重读，单独记录，不把它当建拆允许条件。

## 日志与计数范围

自动独立runtime audit log本版未启用：无已验证安全的写文件/轮转API，按用户允许的安全回退，仅固定计数。没有要求提交的session log路径。

**Performance Snapshot**为可选手动详细快照，在面板显示current/total/previous/peak并打印一次`[SPC_PERF_SNAPSHOT]`到原生日志；不是自动写文件。本轮只提交截图即可，不依赖剪贴板或Lua.log可用性。

Counters不统计其它Mod写入，也不能直接观察原生Modifier内部Property变更；统计本Mod发出的Create/Remove/SetProperty调用（包含可能失败的调用尝试）。因此0能证明这些Lua写路径未调用，但不能宣称捕获整个引擎的所有写入。
