# B038 人口收益诊断（modinfo49）

Document Owner: Codex

只读检查当前HD DebugGameplay.sqlite：SPC_LV3_POP_RESEARCH_0 Amount=0.5、_1 Amount=1.0，BuildingModifiers链接存在，DynamicModifier使用COLLECTION_OWNER/EFFECT_ADJUST_CITY_YIELD_PER_POPULATION。静态未发现定义错误，不能证明当前存档挂载和实际结算。

本轮不改变公式、载体增减、事件或后台刷新。Lv3Effects.Audit额外记录当次读到的workers/pop/active；Describe只读实时人数、ACTIVE、应有bonus、实际存在载体系数×人口、上次审计人数、city:GetYield原生总量。最后一项包含原有专家/地块/倍率等，不是新增效果测量值。报告读取不调用Audit，不用点击报告掩盖自动刷新缺口。

STATIC_CONFIRMED：数据库系数/绑定、Lua语法。LOCAL_SIMULATION_PASS：真实Describe在live workers0、旧carrier2、last audit1、city total13.1时显示差异且不写入；原Lv3Effects fixture回归通过。新的诊断未实机。

目的：区分起始基准污染、实际人数/载体不同步、载体正确但引擎效果错误。modinfo49无SQL变化，不要求新局。GPP已接受延迟不修复。研究所需最小读数见B038_Population_Diagnostic.md。
