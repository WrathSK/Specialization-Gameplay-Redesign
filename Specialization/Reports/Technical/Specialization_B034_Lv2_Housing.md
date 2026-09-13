# B034：共同Lv2住房自动应用

Document Owner: Codex
Design Reference: D0009 / SHARED-001；SHARED-002仅研究
Implementation: P0-B-034 / modinfo42
Validation: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 本轮范围

只启用四种已接DEV专业（标准学院、剧院、商业中心、工业区）的共同Lv2住房。采用已验证的EffectiveFacts读取Potential/ACTIVE，不写回专业投资记录。基础GPP、Lv3/4其它收益与网络收益未启用；Industry Lv1仍未接入。不是完整高级专业验收。

## 原生效果与派生状态

`Lv2Housing.lua` 从当前城市事实、完整的首个专业区域和当前拥有的建筑计算应有集合：区域槽0；已拥有的每个对应建筑层级槽1–8。ACTIVE未知或低于门槛、非测试玩家、身份不一致均不能保留高级住房。同层替代建筑去重，第二区域不能贡献。

`Data/Lv2Housing.sql` 定义9个InternalOnly市中心建筑，每个通过原生`Buildings.Housing=1`提供住房，无产出、岗位或GPP。先移除多余，再补缺；重复刷新不写。建筑只承载可重建结果，不能反推专业/Potential；不新增永久Property事实。住房UI可能统一计入建筑住房，不承诺按原区域名称逐项显示。

生命周期：LoadScreenClose后完整重建；GovernorAssigned/Established/Changed、PlayerTurnActivated、CityTransfered、CityBuildingsChanged和GameEvents.BuildingConstructed/OnDistrictConstructed/CityBuilt触发重核对；投资请求返回后也重核对。重入保护避免生成内部建筑时重复处理。每次真实事件允许重试失败城市；读取按钮不刷新、不修复，只比较expected/carrier。读取不会使缺失收益突然生效。

实机尚需确认上述事件在当前Gameplay时点能读取到已更新的总督门槛，特别是调离后的即时撤销。回合核对是后备，不把“下一回合才好”登记成即时通过。

## 建筑层级适配

固定审阅当前本机HD数据库的50种真实建筑，以同区域BuildingPrereqs链层级确定并固化在SPC_Lv2HousingTiers。当前最高5层，不按“最高建筑存在”补发未拥有的低层；只计实际拥有的去重层集合。查询排除InternalOnly及DUMMY辅助建筑，避免本Mod及HD标记膨胀住房。

当前HD例：学院Library/JNR Academy=1、University/JNR School=2、Architecture等=3、Research Lab/Education=4、Data Center=5；工业Water/Wind Mill=1、Workshop/Manufactury=2、Factory等=3、发电厂等=4。剧院Grand Hotel与两种Museum同为3；商业Fair=1、Market=2、Bank=3、Stock Exchange=4。表中名称只在当前数据库存在且所属区域匹配时写入。

此为当前HD配置适配，不声称任意未来建筑Mod或独有区域全部兼容。升级HD后应重新静态审阅映射；未知新建筑不会自动猜层。区域被掠夺后的支持政策、通用征服继承不在此次验收范围，未擅自决定新玩法。

## 本地证据

- live DebugGameplay.sqlite以mode=ro打开，复制到内存执行SQL；Make_Hash为本地stub，只验证关系/结构，不证明引擎哈希。
- 原生Buildings.Housing字段及当前50种建筑/前置链：STATIC_CONFIRMED（静态证据，不等于实机通过）。HD Gameplay/Policies.lua使用GameEvents.BuildingConstructed；Gameplay/RegionalYields.lua使用GovernorEstablished/Changed。
- `DevelopmentTests/test_lv2_housing.py`运行实际Lua：四族、ACTIVE门控、同层去重、无关区域排除、建筑增加/移除、重复/重入、重载重建、错误缓存替换、未知/无效事实撤销及恢复、读取零写。LOCAL_SIMULATION_PASS（模拟，不等于游戏通过）。
- 既有test_native_investment与test_effective_facts重新运行：仅在内存适配manifest42与提示文本，原测试不改。涵盖投资、统一事实、原Lv1、新城/加载和网络撤销回归。
- manifest路径、XML唯一ID、全部Lua语法静态通过；UUID保持。实际住房数值与事件时序仍USER_GAME_TEST_REQUIRED。

## SHARED-002后续路径，不在B034启用

数据库有District_CitizenGreatPersonPoints，但它是按DistrictType全局定义，没有本次所需的城市ACTIVE条件列，不能直接把+2写进去影响全体文明。找到Building_GreatPersonPoints和EFFECT_ADJUST_DISTRICT_GREAT_PERSON_POINTS作为原生基础点数候选，下一轮研究按当前工作人数挂载/撤销，使城市/玩家GPP倍率仍能作用。

未使用ChangePoints式直接奖励，未认为名称含BASE就已证明倍率。工作人数变化的及时刷新、Culture同时三类、百分比加成须专门验证。没有结论称原设计不可实现，也没有选择改变玩法的fallback。

## 实机与保护

唯一新批次：[B034三步住房测试](../../Status/Validation/Cases/B034_Lv2_Housing.md)。不用重测商路/投资故障/总督全部等级。

变更前备份：DevelopmentBackups/Specialization-before-B034-housing。Spec D0009保持原hash；不修改UUID、Civ VI配置、旧测试及既有备份/证据。不启动游戏。
