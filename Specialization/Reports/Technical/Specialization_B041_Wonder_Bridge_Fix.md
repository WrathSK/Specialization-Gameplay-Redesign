# B041.54：奇观地块枚举候选修正
Document Owner: Codex
State: USER_GAME_TEST_REQUIRED

用户人工部分通过见Status/Validation/Results/Specialization_B041_Partial_User_Result.md。
53在Gameplay直接Map.GetCityPlots():GetPurchasedPlots(city)；HD本机UI/Additions/HD_Utils.lua:222–229显式提供Utils.GetCityPlots(playerId,cityId)，在UI Context按CityManager.GetCity读取同一列表。
54改从ExposedMembers.DLHD.Utils.GetCityPlots取得候选index，Gameplay依旧逐一核对owner、购买城市、DISTRICT_WONDER、当前目标Index和HD_UNCOMPLETED_WONDER，以及未完成状态。候选重复index去重；helper缺失/非法列表清楚报告，不能猜位置。
这是上下文风险修正，不是已证实根因；HD地基Property缺失等仍可能导致失败。UI底部现在显示第一个unknown城市ID/原因，日志继续输出全部。
test_unit_targets_wonder_bridge.py在实际模块中移除Gameplay GetCityPlots，仅mock HD helper，测试合法奇观、重复index只一目标、helper缺失、错误标记及其它原目标/UI回归；LOCAL_SIMULATION_PASS。不等于Civ6通过。
没有变更其它目标逻辑、Design、单位或消费。备份DevelopmentBackups/Specialization-before-B041-wonder-fix。
最小复验：回主菜单重载原存档，Unit sites标题B041.54，选工人开启Builder preview，只看原来缺标记的当前在建奇观。应出现BUILD TEST。仍失败时只截Unit sites底部状态与当前奇观，不重测其它类型、不需新局。
