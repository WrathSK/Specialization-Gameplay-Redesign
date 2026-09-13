# D0012 / B047 — 施工队缩放后整数化

用户接受：“接受，并且显示整数。”

规则已登记D0012 / ACCEPTED，冻结D0011原文，Architecture A0102同步。只改变Crew缩放金额的末步：`floor(base × CostMultiplier / 100)`，并让既有按钮、预览、确认、诊断继续读取共同的CrewAmount。不存在分别计算/分别取整的UI与执行口径。

快速速度五档：167 / 281 / 502 / 670 / 911。标准：250 / 420 / 750 / 1000 / 1360。其它速度同公式。仅对Crew生产力采用floor，不扩展到GPP、人口加成、其它专业或其它小数系统。单位百科里的标准档位数值仍为原有整数。

项目基础成本、原生项目速度计算、五档生成、合法目标、1劳动力、消费/注入顺序、溢出限额逻辑均不改。完整UnitActions、ConstructionProbe、CrewProjects、Data/Crew、Data/CrewProjects及单位按钮Lua/XML与本轮前逐字节一致；运行金额唯一改动位于Probe.CrewAmount，另更新build元数据。

STATIC_CONFIRMED：上述静态比较/共同读取路径，不等于游戏运行验证。
LOCAL_SIMULATION_PASS：test_crew_integer_speed.py验证25种速度×档位整数结果、实际执行模块50组完整/限额消费及重复确认拒绝；实际UI在Quick下显示167、预览溢出显示67、重复点击/移动/目标失效回归通过。Lua/XML/manifest完整检查通过。不冒充实机PASS。

既有用户实机确认：一级实际167、五级实际911，五级完成鲁尔山谷、五个项目整数成本及排序。[补充结果](../../Status/Validation/Results/Specialization_B046_User_Clarification.md)。B047改版后的显示仍属USER_GAME_TEST_REQUIRED，可在后续正常测试顺带查看；不新开局、不重测完整项目/施工批次、不额外派验证任务。

无未决取整设计、无本项阻塞。当前运行P0-B-047 / modinfo60。未启动游戏、不改UUID/配置。备份DevelopmentBackups/Specialization-before-D0012-integer-crews。
