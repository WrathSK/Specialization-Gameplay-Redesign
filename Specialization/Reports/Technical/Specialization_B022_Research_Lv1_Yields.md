# B022：Research Lv1原生专家收益载体

Document Owner: Codex
Design Reference: D0008 / RES-001（数值权威只在Spec）
Build: P0-B-022 / modinfo29

## 结果与范围

STATIC_CONFIRMED：本机HD 2465378070/SubMods/CityPolicies/CityPolicies.sql:245–252将内部城市政策建筑PrereqDistrict设为Holy Site，并用Building_CitizenYieldChanges调整专家产出。Gameplay/HD_Common.lua:83–96使用GetBuildQueue():CreateBuilding和GetBuildings():RemoveBuilding。缓存真实Buildings/Building_CitizenYieldChanges结构支持本次配置。没有找到可直接动态调整任意专家yield的现成DynamicModifier，因此先用原生表承载，不把城市补贴当岗位产出。

本轮部署仅Research普通Campus的显式ON/OFF实验，实际产生收益，但不声称完整专业资格/自动启用已实现。Culture/Commerce未部署；Industry动态Base adjacency与Crew另行适配。此限制是渐进测试范围，不是Design规则修改。新增建筑InternalOnly、CitizenSlots=0，无普通建筑收益、住房、维护和GPP；不修改现有区域或建筑定义。是否被HD其它建筑统计计入、岗位估值是否完整更新需实机确认，不静默接受附带行为。

## 身份与生命周期

CityFlowProbe新增只读SupportFacts：现有B021有效绑定、DONE、已恢复/本轮active、无停止、B015事实一致。ResearchSupport再核对RESEARCH及实际已完成同ID普通Campus。建筑仅为效果载体，不从它推断专业或创建永久成果。

ON仅在以上条件通过时创建，已有即不写；OFF仅移除本建筑，重复不写。Read也会核对资格，不合法时尝试移除旧载体并报告错误；不把它定义为严格无副作用审计接口。数据定义缺失明确报告B022_DATABASE_MISSING。UI返回workers与配置值，明确不是实测yield。

加载在B021恢复监听之后检查现存载体，有效保留，失效移除，不自动为未开启城市创建。PlayerTurnActivated与可用CityTransfered事件重新检查。尚不证明所有征服/休眠事件即时撤销；固定测试载体资格不是ELIG正式实现。跨owner身份原有边界仍保留。API失败记录AUDIT_ERROR/ERROR，不盲目重试。普通开关/保存优先，极端故障不新增测试批次。

## 本地验证

LOCAL_SIMULATION_PASS：test_research_support.py组合实际B013/B015/B021 Lua与本模块，覆盖已有B021恢复场景、ON/OFF重复无重复创建、载体随模拟重载保留、已知停止/非Research/非测试owner撤销或拒绝、Create失败与缺数据库提示；全部运行Lua编译与XML/manifest路径检查。真实缓存数据库只读复制到内存执行SQL，外键错误集合不新增、原生表配置检查通过。Make_Hash使用fixture函数，仅验证表关系，不等于引擎hash/实际收益证明。

另运行test_city_journal_probe.py、test_native_fresh_hook.py、test_city_property_bridge.py，三组通过。旧test_city_flow_resume.py原有manifest28断言保留，B022新测试复用其场景而不声称原脚本当前全量通过。没有启动游戏或写游戏配置；Design SHA256保持。

## 实机边界与下一步

USER_GAME_TEST_REQUIRED：[一个小批次](../../Status/Validation/Cases/B022_Research_Lv1_Yields.md)，仅一人差额/零人无额外收益/正常读档，重复与关闭在同批完成。新增数据库定义如旧档缺失则新局，若旧档已包含定义可沿用。原生引擎是否将内部学院建筑正确计入专家yield，必须由实际岗位UI确认。

通过后扩展常数型Lv1载体并接自动资格更新；Industry动态基础相邻另行设计实现层，不增加新的玩法。正式收益完整链、替代区域、通用资格仍未完成，B010延后。备份见DevelopmentBackups/Specialization-before-B022。

## 文件清单

新增运行文件ResearchSupport.lua、Data/ResearchSupport.sql；修改CityFlowProbe.lua（只读事实门控）、Gameplay.lua（请求与加载）、UI/P0Panel.lua与xml（3个按钮）、Probe.lua与modinfo（版本/文件注册）。新增DevelopmentTests/test_research_support.py、本报告及B022测试说明；更新Architecture A0050、Status S0052、README、AGENTS版本引用与技术索引。既有Tests和Design未改，UUID不变；运行源码仍在唯一原目录。
