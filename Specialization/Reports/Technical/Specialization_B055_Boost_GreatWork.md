# B055 — Native network Boost and Great Work backend comparison

Document Owner: Codex
Architecture Reference: A0119
Design Reference: D0017 NET-RC-001/003/005, GW-001/002/003
Build: P0-B-055.72 / modinfo72
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED

## Scope

用户要求不预调查Boost小数，直接构建后实测，若引擎舍去不修复。运行自动网络Boost，临时精度权重来自NET-RC-005；两个k独立。GW提供可撤销实现对照，不编造当前时代标准或把实验当完整Culture IV。当前验证/下一步唯一入口见[Status](../../Status/Specialization_P0_Status.md)。

## Local source precedents

外部依赖根由忽略的local/config.json或Phase1路径说明解析；未复制、修改HD/原版文件。

- HD `UpdateDataBase/DL_Wonders.sql:598–610` Great Library：BuildingModifiers → `MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST`, Amount=3；另附player property `HD_Player_Extra_Tech_Boost` Amount=3。
- HD `UpdateDataBase/DL_GreatPeople.sql:172` JNR Great Scientist Eureka Strength：同一原生Boost及同样记录机制。Research使用已在DB中的civic对应类型；不会交换Research/Culture方向。
- HD `UI/Loaders/ToolTipLoader_TCP.lua:76–95`读取上述Tech/Civic额外Boost Property供tooltip。B055使用自己可撤销的property modifier，不覆盖HD其它来源，也不把该property数字当引擎实际进度证明。
- HD amphitheater `HD_AMPHITHEATER_WRITING_CULTURE_BOOST`：single-city greatwork yield，WRITING / CULTURE / YieldChange=2。旅游业另以 `MODIFIER_SINGLE_CITY_ADJUST_TOURISM`, ScalingFactor=150。
- Kongo `TRAIT_GREAT_WORK_*`：player-cities greatwork yield，分SCULPTURE/ARTIFACT/RELIC，Food/Production/Gold/Faith增量。这证明按类别修正的先例，不证明本项目应包含遗物。
- 用户所指商场对应本机`BUILDING_SHOPPING_MALL`的产品效果：`HD_SHOPPING_MALL_PRODUCT_GOLD_BOOST`/`...FAITH_BOOST`使用greatwork yield / PRODUCT / ScalingFactor=150；`HD_MARKET_PRODUCT_TOURISM_BOOST`另用Tourism ScalingFactor=200。Product仍不进入B055实验对象，更不自动加入GW003。
- 原版 `Base/Assets/UI/Screens/TechTree.lua:1112–1114`、`CivicsTree.lua:1287–1289`：cost/progress/HasBoostBeenTriggered；仅在UI读数层使用。
- 原版 `Base/Assets/UI/GreatWorksOverview.lua:195–210,298–308`与HD `UI/Additions/HD_Utils.lua:1150–1205`：已拥有建筑槽位、作品类型、建筑巨作yield/tourism。实机Getter存在性仍待本批验证，不混称Gameplay与UI同可用。

## Boost implementation

`NetworkBridge.National()`先验证当前turn/signal/CountOutgoingRoutes与端点，再沿既有derive结果过滤当前有效ACTIVE源。按实际recipient城市去重，L取所有有效源最大值；多中心重叠与多来源不各自结算。

`tools/generate_boost.py`为当前可达1..129个recipient、两类型、四档生成1032个内部定义，以及对应Lua金额表。当前128路线桥接上限使所有recipient包含于“路线目的城市集合 ∪ 首都self”，所以129不是擅自截断正常规模。未来Spaceport或扩大route上限须同步扩展此生成范围。超界停止本轮配置并显示错误，不用cap或旧线性回退。

每种网络仅一个原生Boost modifier在首都存在（其伴随HD记录modifier不授予第二份Boost）。读取配置浮点，但使用整张单一Amount，避免将其拆成多个modifier而在引擎逐项取整时产生另一种值。Native Amount是否截断由用户实测；Python浮点序列化是普通数值表示，并非业务round/floor。更改k需重生成并部署同一套SQL/Lua；目前不是运行中热改开关。

启动主动后台握手，先撤销保存的派生载体，再从当前网络重建；不依赖打开面板。来源等级、投资、路由更新触发Audit。撤销旧后添加新，重复刷新不写；迁都/所有权变化清理。没有SetResearchProgress、TriggerBoost、直接研究/市政进度注入；只影响引擎将来正常触发的Boost。引擎最终封顶不能据此称已设计确认，首批避开完成边界。

## Great Work experiment

CITY是**固定整城+2基础文化**（不是每作品+2的动态城市账本）；OBJECT是七类标准文化作品**每件+2文化**。固定数字只是控制变量。CITY/OBJECT互斥，OFF撤销，读档/所有权变更归OFF。七类为Writing/四类Art/Artifact/Music，Relic/Product/未知类排除。不会添加作品、解锁槽位、改变时代、触发theming或直接增加Tourism。

一件作品时对比两个后端对城市/作品明细的影响；移入第二件后CITY仍固定2而OBJECT按2件配置，验证类别与原生对象计数。城市总量会含既有宜居度、专业专家等倍率。能看到作品收益不等于theming或作品专属倍率最终已认可。

GW001缺时代口径、各类别曲线、缺失标准方案；GW002尚需按最终范围采集Base与每件复制再确定倍率语义。本轮**未自动实现**两项完整收益。这里不存在“因为难就改变玩法”的fallback；是进入用户测试的接口对照。两后端隔离，可按后续决定替换。

## Local checks and limits

`test_b055_boost_gw.py`执行真实生成器、SQL（外部DB只读复制入内存）、NetworkBridge、NetworkBoost、GW控制和UI读数Lua：1034个定义、Modifier引用存在、小数文本、Lmax/N去重、最高源降级、失效撤销、故意错误保存载体重建、迁都、重复幂等、GW互斥/排除/清理、研究进度差。SQL不修改其它Mod记录。

`test_b055_regression.py`在冻结旧测试上只适配当前manifest版本与白名单NetworkBridge增加方法/通知，旧标准化/折扣/复制的数值断言保留。新方法文本冻结为B055 fixture，避免跳过NetworkBridge保护检查。部署仍用hash守卫工具，UUID/其它Mod/配置不改。

本地模拟不执行原生Modifier效果；源Getter、原生Boost小数、HD记录撤销、Tooltip与Tourism/theming实际组合都不能据此PASS。全量初始化载体检查只在加载/所有权变化进行，正常更新只改两种实际载体；完整多人资格/征服UID适配仍继承既有边界。

## 执行记录 — 2026-09-13

- `test_b055_boost_gw.py`：通过（含未收到LoadScreenClose时后台启动、UI作品计数/类型排除）。
- `test_b055_regression.py`：通过B054折扣、B052账本、B051固定复制/完整区域范围及受保护文件对照。输出中的拒绝日志是刻意注入的失败场景，不是新游戏故障；旧测试结尾USER_GAME_TEST_REQUIRED是其历史措辞，当前用户已通过范围以Status为准。
- 回归封装首次因新增字符串转义失败，修正本轮封装后重跑通过；没有删除/放宽旧数值断言。
- Design D0016原文字节冻结；D0017 SHA256=`5132c9a300853d0107ad84cf4adebadd5f7c173dbc0c72943a4b3e241deb2d06`。
- 未启动Civ VI，未提交或推送Git；原生效果等用户回报。

部署记录：已通过受限部署事务安装到现有SpecializationP0，94个运行文件；source/runtime SHA256=`e021d6a4bbed39c9eefd1d8c3a1537a18f3e3ed5c77db175b5d6567271eefb1d`。旧版完整备份保存在Mods扫描目录之外的SpecializationDeploymentBackups，后缀`0yck9q4l`。UUID不变，不改其它Mods或游戏配置。
