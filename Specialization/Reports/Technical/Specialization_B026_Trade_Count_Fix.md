# B026：Gameplay商路数量API修正

Document Owner: Codex
Build: P0-B-026 / modinfo33

根因：NetworkBridge.lua B025第34行把UI GetNumOutgoingRoutes用于Gameplay，截图报nil；本机TradeRouteProbe.lua第29行已有已测CountOutgoingRoutes先例。修正为CountOutgoingRoutes，不移除数量校验，不改变后台UI collector的GetNumOutgoingRoutes。旧mock误同时提供UI方法，未覆盖上下文差异；新test_network_gameplay_count_fix.py只提供Gameplay方法，复用发送/接收、首都自源与分发、撤销/重放等场景。面板仅输出首行错误，完整堆栈打印日志。

STATIC_CONFIRMED：API先例与报错位置一致；LOCAL_SIMULATION_PASS：新Gameplay-only方法测试、既有后台自动发送适配测试两组通过，Lua/XML/manifest检查通过。没有新增实机PASS。首都GetCapitalCity等后续调用仍需实际运行，不提前断言全部API正确。

USER_GAME_TEST_REQUIRED：沿用当前存档，回主菜单重载，确认B026。不打开贸易总览，先读科研首都：READY_BACKGROUND_UI、source=RESEARCH、center=YES、connected含RESEARCH@本城ID。再读首都实际商路目的城：Research selectedReceives=YES。两图即可，不必重建商路或先测商业城。首都自接入是source资格，首都selectedReceives不要求YES，除非另有有效入站分发来源。全帝国N可能含其它接收城市，不要求固定为1。

若仍UNKNOWN，保留短错误即可。先完成这两步，再继续商业中心、多源分发与撤销；本轮不重开局、不增加收益或改Design。

改动NetworkBridge.lua、Probe.lua、UI/P0Panel.xml、modinfo，新增一个测试和本报告；Architecture A0057、Status S0059。运行B026/33，备份DevelopmentBackups/Specialization-before-B026。UUID/SQL/Lv1/Design保持，未启动游戏。
