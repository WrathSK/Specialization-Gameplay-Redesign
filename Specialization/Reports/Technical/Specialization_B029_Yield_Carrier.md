# B029：可撤销固定城市收益承载实验

Document Owner: Codex
Architecture Revision: A0064
Runtime: P0-B-029 / modinfo36
Design: D0009，未启用Commerce IV；条件总产出授权不等于精度/倍率已定。

## 新证据与路线

HD Gameplay/RegionalYields.lua:228使用Utils.BinaryCompress将当前区域输入写入城市中心plot属性；UpdateDataBase/HD_Last.sql:49起定义REQUIREMENT_PLOT_PROPERTY_MATCHES + PropertyMinimum=1；HD_Regional_Yields.sql:114–129按位给城市收益。此先例比持续Attach新modifier更适合作为重复刷新候选：固定定义、属性开关选择，关闭旧资格即撤销。此处只借鉴结构，不调用HD内部缓存或改其属性。

新增Data/YieldCarrierProbe.sql，独立SPC_B029_ONE/HALF两组plot属性门控六个MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_CHANGE，只挂测试Trait。两档Amount=1/0.5，初始无属性时不激活。不擅自给任意业务产出选二进制小数精度或取整；0.5仅辨别引擎是否接受小数的实验值。

YieldCarrierProbe.lua：STEP首次开启ONE、下次开启HALF，之后重复保持两开关为1，不增加Modifier数量；OFF将两属性清零。首次开启前保留本加载会话的S/C/P基线，READ输出配置值和实际getter差值。全程限owned test city，通过既有Gameplay窄请求入口，不写专业/潜力。基线仅内存，开关是持久plot属性，必须在测试结束OFF；跨owner/旧打开存档没有baseline不能伪造原值。OFF不要求SQL定义存在，STEP必须先检查六定义，缺失则不写。

本包Read source totals显示实验状态与总值/delta，原SourceYieldProbe.lua保留。新增按钮放已有空位，不进行延后的网络报告重做。City级加产出是否反馈到district copy，以及目标城市percent加成是否放大仍未实机确认。

## 验证

STATIC_CONFIRMED：只读打开当前DebugGameplay.sqlite，复制到内存执行SQL；六Modifier、测试Trait作用域、三个0.5文本值及无新增外键错误；所有Lua解析、XML唯一ID及manifest路径/UUID核对。数据库能存0.5不证明引擎使用小数。

LOCAL_SIMULATION_PASS：test_yield_carrier_probe.py覆盖真实控制模块STEP/重复/OFF、缺定义拒绝、owner拒绝、只读报告和真实Gameplay请求分发；mock分别演示无倍率和1.5倍下的delta，不能作原生倍率证据。test_background_network_sender.py回归通过。现有网络/Lv1源码未修改。

USER_GAME_TEST_REQUIRED：[一组固定增量测试](../../Status/Validation/Cases/B029_Fixed_Yield_Carrier.md)。测原生整数/小数、重复与清零。百分比若放大，不自动接受最终20%被放大为正式玩法，先分析测量再按Design冲突规则处理；本轮没有需要用户预先决定的数值。

## 未完成项

此承载仍只有六固定定义，不能应用任意Convergence数值；若后续采用量化位集合，需要先决定精度/范围，不能静默floor。若引擎支持Amount小数，也不意味着支持Property作为动态Amount表达式。循环保护仍依direct source/唯一专业身份及实际复制层隔离；本测试不证明全部间接反馈无环。高级ACTIVE和正式汇聚均未接入。
