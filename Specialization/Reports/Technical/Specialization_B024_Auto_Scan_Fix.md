# B024：自动收益扫描隔离修复

Document Owner: Codex
Build: P0-B-024 / modinfo31

B023用户失败见结果记录。本轮STATIC_CONFIRMED是源码扫描异常边界过大及新缓存三类定义存在，不代表实机根因已确认。

修复：各玩家扫描独立捕获错误；单个未就绪玩家不再中止其它城市。完成事件直接定位本城对账，避免正常本城路径依赖全体玩家枚举。保留加载/回合全量核对、幂等、错误停止重试及事实门控。只读面板新增events与scan(cities/skippedPlayers或ERROR)，不把按钮改为补发操作。

LOCAL_SIMULATION_PASS：test_auto_support_scan_fix.py复用三专业真实Lua组合，额外令坏玩家先遍历，旧B023复现自动不创建，新版通过直接完成/全量修复/重载/防重复。Lua/XML/manifest检查通过；没有SQL变化或需要新局的定义。实际失败原因仍需新诊断确认。

USER_GAME_TEST_REQUIRED：沿用当前存档，回主菜单重新加载，确认面板B024。不要新建城市/重新造区域，先看三座现成城市岗位是否恢复+3F/+3P，再任选一城Read auto Lv1截图，expected与carrier应匹配。首次补齐会有changes>0，这是正确恢复；再次保存重载应为0且收益保留。若仍NONE，回传完整scan/events行，不要求复制日志。此次复验先验证现成城恢复，新增完成自动路径尚不凭此扩大PASS。

更改ResearchSupport.lua、Probe.lua、UI/P0Panel.xml、modinfo；新测试与本报告。Architecture A0053、Status S0055，Design/SQL/UUID/游戏配置不变，未启动游戏。网络桥接提案仍待决定，本轮未推进。
