# B068.94 可玩界面与诊断整理

Document Owner: Codex
Design: D0025 unchanged
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED for native layout/lens/log output

## 当前实现

保持B067.93核心能力、所有权隔离、32次上限、资格范围。未改变结算、数值、合法目标或投资条件。local/before-b068保留完整Mod/文档恢复点与sha256.json，不创建Git commit。

### Potential：采用安全UI替代

没有增加City Center游戏建筑。HD的DL_Buildings.sql约2234/2240行按市中心建筑集合生成效果；HD_BuildingTiers.sql排除HD_DUMMY_BUILDINGS，HD_Last.sql对dummy另作处理。仅0 yield不足以证明通用建筑计数/其它Mod枚举无副作用。内部建筑又不符合普通可见要求，故按用户允许的更安全mirror方式实现。

CityPotential.xml/lua在原生 /InGame/CityPanel/MainPanel 上附加显示条，位于城市操作按钮上方。选中自己的已建立专业城市后显示 专业城市/专业名城/专业都会/专业中心 + 科研/文化/工业/商业 + 潜力等级；tooltip含投资次数与Governor条件。无Identity时不显示；错误时隐藏不猜等级。名称只用于显示，不作逻辑key。

每2秒至多读取当前选中城市一次，不遍历帝国。Gameplay新增CITY_PRESENTATION_READ，仅调用既有EffectiveFacts.Read，使用独立CityPresentationView响应，token/owner/city三重匹配；不写Property、模板或调用Audit。没有任何建筑数、收益、槽位或ACTIVE改变。切城/取消选中清除显示，读档根据真实数据重新读取。

### HUD与诊断

诊断入口挂在 /InGame/WorldTracker/WorldTrackerHeader 右侧：读取容器宽度+8 UI单位；跟随原生UI缩放、宽度变化，不使用截图绝对坐标。若第三方彻底替换掉header，退回根左上8,120 UI单位并记日志，此为developer UI limitation；需要用户截图确认。原生WorldTracker.xml与Cheat Panel World Tracker的LookUpControl/ChangeParent先例已检查。

UnitSites独立HUD入口XML和refresh均隐藏；保留代码，主诊断“移民 / 施工队”直接执行只读UNIT_SITE_READ。施工与投资按钮/两步确认逻辑未改，仅旧超时提示改为新诊断入口名称。

主面板15个只读入口（加关闭共16，不含外部打开按钮）：
1. 城市专业 / 潜力
2. 总督条件
3. 专家与岗位
4. 巨作 / 时代对话
5. 巨作相邻
6. 四级区域收益
7. 当前商路（现有后台缓存）
8. 网络概况
9. 网络来源 / 接收（重复点击翻页）
10. 尤里卡 / 鼓舞
11. 商业四汇聚
12. 工业网络折扣（重复点击翻页）
13. 标准化模板（重复点击翻页）
14. 移民 / 施工队（选中单位）
15. 写入诊断日志

报告区增加滚动，避免长报告覆盖按钮。旧OFF/TEST/AUTO/生成/写入/影子控制全隐藏，所有回调和底层实验保留，没有添加Rebuild以免误触修改。历史UnitSites窗口仍保留DEV控件但没有常驻打开入口。

日志输出SPC_DIAGNOSTIC_REPORT_BEGIN/END，包含已读取分城市/分页报告、当前后台纯数据、选中城市/单位、单位提示、错误重复次数。只序列化缓存，不调用收集/刷新。跳过函数/引擎对象与循环，深度12/12000标量上限显式记录，不承诺无限长度。使用Lua.log，不依赖OS剪贴板；用户需在关闭/重开游戏覆盖日志前另存。六个后台UI模块仅增加局部日志过滤器，原始刷新回调不变；每来源保留128种消息首条全文及重复数/首末回合，超限记dropped。现有Gameplay错误日志保留，不全局覆盖print或隐藏引擎错误；原有正常UI没有新加错误弹窗。

### 紫色合法目标

仍使用既有UnitTargets.Refresh返回的合法tile集合，选择移民/施工队即进入提示，实际操作仍两步确认。移除WorldAnchor INVEST/CREW浮字；历史版本保存在恢复点。

原版MinimapPanel.lua的SetLayerHexesColoredArea + workshop More Lenses/Builder使用同类原生染色API。使用Hex_Coloring_Great_People层和独立COLOR_SPC_LEGAL_TARGET紫色，不占用Movement、Water或Appeal/More Lenses层，不调用SetActive切换全局镜头。不改变地图点击行为。相同集合不重画，移动/选择/模式改变清理，原有5秒只读目标核对保留，重复状态日志去重。新选伟人/自然学家时交还原生层，不清除其已绘制目标。

兼容性边界：引擎高亮层不是私有的，第三方若同时绘制GreatPeople层仍可能冲突；该层是否接受自定义紫色、显示顺序及单位切换均需实机。没有为避免此风险改动Gameplay，或假定UI mock能证明引擎渲染。

## 本地验证

DevelopmentTests/test_b068_ui.py：实际Lua验证Potential1–4显示、换城清理、只读响应、同目标不重画、失选清理、日志去重计数；全部Lua语法/XML结构/15入口/Design hash。
DevelopmentTests/test_b068_regression.py：前批机制/SQL/收集性能/隔离回归；仅适配版本94与用户允许的15入口+关闭=16，保留所有机制断言。原历史测试文件不改。
Fixtures/B068_UI_Delta.json记录20个新增/修改文件，94个既有文件不变；剥离新增只读分支后Gameplay与B067逐字相等。

无Civ VI启动，无USER_GAME_TEST_PASS，无Design/UUID/配置改变，无commit/push。

最小验收见 ../../Status/Validation/Specialization_B068_User_Tests.md。

## 部署与文件清单

源码/部署包114文件一致，版本94，SHA256 `784bee62c8707090eab02b9b2fae3dae93736bff694ce9d6b9b782cf0d961a6e`。B067运行备份位于外部SpecializationDeploymentBackups/.SpecializationP0-backup-_v6p7ekt。未启动游戏。

源码新增：DiagnosticLog.lua、UI/CityPotential.lua、UI/CityPotential.xml。
源码修改：Gameplay.lua（只读分支）、Probe.lua（版本）、SpecializationP0.modinfo、Data/Colors.sql；UI/P0Panel.lua/xml、UnitSites.lua/xml、UnitPanelActions.lua、UnitTargetMarkers.lua/xml；UI/BoostRefresh.lua、DialogueRefresh.lua、CopyYieldRefresh.lua、DiscountEligibility.lua、GPPRefresh.lua、IndustryRefresh.lua仅局部日志过滤。
工程新增：DevelopmentTests/test_b068_ui.py、test_b068_regression.py、Fixtures/B068_UI_Delta.json。
文档：README、Architecture A0146、Status S0165、本报告、B068用户验收清单、本地结果记录。Design及历史材料未改。
