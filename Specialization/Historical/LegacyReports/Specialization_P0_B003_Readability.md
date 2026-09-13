> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# B002 商路 UI 用户验收与 B003 显示调整（最新）

## 已确认结果

USER_GAME_TEST_PASS：用户本轮明确确认 Read routes (UI) 能读取三条现有商路，保存并重新加载后仍可读取；随后全国加入第四条，其中同一城市分别前往两个目的城市，Next district / route 可以分别读取两条路线。三条后的截图是 UI OBSERVATION，不再与此前 Route events (Game) 事件测试混淆。

截图（ScreenshotInbox，按时间）11.40.47 / 11.40.51 / 11.40.55 PM：Stirling (Test) → Aberdeen (Test)、Edinburgh (Test) → Stirling (Test)、Aberdeen (Test) → Edinburgh (Test)，各城 rawCount=1。读档与第四条同城分页以用户文字反馈为证据；未要求额外截图。第四条新增后的再次读档没有单独回报，不扩大证据范围。

rawCount 表示所选城市出发路线数，不是全国路线总数，也不是网络 recipient N。此前 Gameplay 新路线事件捕获的 USER_GAME_TEST_PASS 保留；其临时事件历史读档清空与 UI 当前路线枚举是两个不同问题。

## B003 本地修改

STATIC_CONFIRMED：仅调整 Probe.lua 商路显示与版本标记（modinfo version=10，UUID 不变）。先显示本城出发条数、当前页、出发/到达城市名称；原始玩家/城市/商人 ID 和检查字段保留在下方排错区。无法解析的端点明确显示未知。沿用 UI city:GetTrade():GetOutgoingRoutes()，不改变分页、Gameplay 事件、SQL 或网络算法。修正旧代码注释中“trade runs in Gameplay”的过期描述。

LOCAL_SIMULATION_PASS：test_specialization_p0.py，包含 Lua 编译/XML、UI 路线方向、分页、空列表、未知端点、缺失接口、禁止递归引擎对象及不派发 Gameplay 的既有检查。B003 中文排版尚未实机确认，标为 USER_GAME_TEST_REQUIRED；不要求为纯显示修改重复已通过的基础测试，下次正常重新加载脚本时查看即可。

BLOCKED：正式 Gameplay 权威网络全量恢复尚无完成方案。UI 快照通过不等于 Gameplay 能直接调用该 getter，也不允许以打开面板作为网络运行前提。终止/掠夺/易主等有效性撤销、稳定身份和初始重建仍待后续独立设计；不能把持久化事件历史直接当作当前路线集合。

当前无需继续重复商路起终点/同城分页/三条场景读档测试。不启动游戏，不等待用户测试。原生区域复制口径 NativeDistrictCopyBasis、sqrt(N) 与其它既定设计不变。
