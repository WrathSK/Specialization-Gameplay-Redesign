# B044 五档施工队项目与单位提示

Design: D0011 / Architecture: A0098 / Build: P0-B-044 / modinfo57

## 当前结果

B043用户明确“全部正常”；四图已复核并归档，见[结果](../../Status/Validation/Results/Specialization_B043_User_Result.md)。B044只改善玩家提示排版，原始响应仍写日志与单位诊断；不再把cityID、unitID、B033编号和英文准备报告拼入按钮提示。

五档正式项目进入运行包，但原生项目完成/单位生成组合尚为USER_GAME_TEST_REQUIRED。标准速度映射280→250、460→420、820→750、1100→1000、1500→1360；规则权威为D0011 CREW-004，不新增档位。

## 实现与静态依据 — STATIC_CONFIRMED

此状态仅为源码/数据库证据，不等于实机。

- `Data/CrewProjects.sql`：五Projects、固定Cost、NO_PROGRESSION_MODEL、无科技/市政/高阶投资门槛。RequiredBuilding指向无产出InternalOnly市中心标记，PrereqDistrict为工业区。
- `CrewProjects.lua`：从当前EffectiveFacts与已完成Identity工业区重建标记；无需专家人数、相邻数据、二级总督。加载、完成、转移/回合以及已有后台刷新后核对，重复核对不重复建造。读取不明时撤销入口并报错，不补历史专业。
- 项目完成使用原生ProjectCompletionModifiers → MODIFIER_SINGLE_CITY_GRANT_UNIT_IN_CITY（UnitType/Amount=1/AllowUniqueOverride=0，RunOnce/Permanent=1）；没有Lua项目完成发奖缓存、没有回放完成事件。
- 本机HD `UpdateDataBase/HD_Last.sql:598–611` 使用同一单城送单位Modifier及参数；原生重复核装置项目使用ProjectCompletionModifiers+RunOnce/Permanent，证明数据结构有先例。两者组合在本Mod每次重复项目是否正确发放仍需用户验证，不能因静态先例直接判PASS。
- 本机DebugGameplay.sqlite确认DynamicModifier为COLLECTION_OWNER/EFFECT_GRANT_UNIT_IN_CITY；Projects包含RequiredBuilding与NO_PROGRESSION_MODEL。
- 四种新增UnitType和原250共享已经通过的builder美术与1劳动力、禁常规训练/购买；无CLASS_BUILDER tags、无改良地块权限。单位类型精确查表，不接受任意前缀类型。
- UnitTargets、独立地图标记、单位面板及诊断都识别五档；旧DEV免费250入口保留，不能拿它代替项目完成验收。

## 游戏速度与精度边界

Probe.CrewAmount=标准施工力×GameSpeeds.CostMultiplier/100。UI提示和Gameplay执行共享查表；不使用floor/ceil/round。施工确认复核准备金额、当回合目标与进度，注入min(施工力,剩余需求)，余量不传给队列。

原生项目仍交GetProjectCost计算，本地基础UI CitySupport.lua:275–276、ProductionPanel.lua:2221读取引擎Getter，而非可见Lua公式。HD Gameplay/HD_Common.lua:165–166读取同一GameSpeeds.CostMultiplier。原生引擎成本实际精度并未由这些源码证明。

本机速度系数50/67/100/150/300。快速速度280理论成本187.6、250理论施工力167.5；当前保留Lua浮点传入AddProgress。引擎若量化/取整，必须记录精度，不能宣称同比已经实机确认；如需改设计取整，标DESIGN_DECISION_REQUIRED。本轮优先标准速度，非标准速度单列后续小批次。也未证明所有项目生产加成的作用范围。

## LOCAL_SIMULATION_PASS

此状态仅为本地模拟，不等于Civ VI通过。`DevelopmentTests/test_crew_projects.py`执行实际Lua模块与只读数据库的内存副本：五项目/单位关系、25组速度金额及真实执行函数到mock AddProgress、门槛添加/删除/不重复/读档重建、错误撤销、中文提示分离、旧施工一次消费/限额/重复/过期与移民投资回归。全运行Lua语法、XML与manifest文件引用检查通过。拒绝/HELD日志来自预设反例，不表示测试失败。

## USER_GAME_TEST_REQUIRED 与边界

[三项批次](../../Status/Validation/Cases/B044_Crew_Projects.md)：资格、原生生成/重复、最高档重载与施工。速度小数引擎验证后续，不要求现在加开多个速度局。排队后失去资格、征服中的项目队列处理、堆叠出生点均不在本次PASS范围；native RequiredBuilding是否阻止这些极端完成保持未证实，不伪造保证。正常生产与Cheat完成分开记录，允许Cheat优先。

备份：DevelopmentBackups/Specialization-before-B044-crew-projects。未改Design、UUID、配置，未启动游戏。
