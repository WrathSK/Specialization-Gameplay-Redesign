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


---
以下为历史记录，当前结论以上文为准。

# B002结果更正：通过的是Gameplay事件捕获，不是UI枚举

用户已明确纠正之前反馈所指按钮是Route events (Game)。撤销先前误记的Read routes (UI)端点/多路线USER_GAME_TEST_PASS，恢复USER_GAME_TEST_REQUIRED。游戏原生贸易路线界面及时刷新不等于我们按钮的getter已经验证。

四张截图按时间：
- 23:28:50：city=131073，turn=1 actor=0 FROM 0:131073 TO 0:65536。
- 23:28:59：city=65536，同一事件可在另一端查看。
- 23:30:42：city=65536，新增FROM 0:65536 TO 0:196610，并保留前一条事件。
- 23:34:52：读档后city=65536，NO_MATCHING_EVENT_OBSERVED；用户说明过回合仍无记录。

USER_GAME_TEST_PASS：Gameplay TradeRouteActivityChanged在本次新建路线操作中提供方向与城市/玩家端点，单条及第二条事件均被捕获，并可按涉及城市筛选。截图extra为空，不能推断更多状态字段或Trader ID。

STATIC_CONFIRMED：Gameplay.lua初始化shared.TradeEvents={}；历史只在ExposedMembers临时表中，没有SetProperty持久化、也没有读取现有路线重建。读档会清空这份诊断历史。本次观察与实现一致，不是保存文件把真实商路丢掉，也不能从无事件推出无商路。跨回合没有新事件不构成getter失效。

BLOCKED：完整Gameplay当前有效网络的读档恢复仍缺可靠方案。将事件历史简单持久化只能保留“过去观察过”，不能证明路线仍有效；必须解决终止/掠夺/商人删除/城市易主/重复线路/稳定身份，以及已有存档未观察路线初始化。不能用历史记录直接计算recipient N。该限制不是新的版本回归，B002原本明确NOT an active-route list。

当前只补一个此前未执行的读取测试：在已经读档、原生贸易界面仍有路线的现有存档中，选实际出发城市，点击我们面板里的Read routes (UI)（上排中间），必要时Next district / route浏览。这个按钮即时枚举，不依赖之前是否收到事件；无需新建路线或过回合。应显示UI OBSERVATION / mode=TRADE / FROM / TO；若城有两条出站则两条均可翻阅。注意一座城的一条入站加一条出站不是两条Outgoing。截图即可。若无出站则选另一真正出发城。

该测试即使通过也只证明UI快照路径；正式Gameplay权威网络恢复另设计，不将打开面板作为游戏机制生效条件。当前不修改代码、不要求再重复Route events的新建测试，也不再要求尝试等待回合恢复历史。

NativeDistrictCopyBasis最新设计保持；其它已用户通过项目保持。此次更正已同步Status、Findings、Architecture。
