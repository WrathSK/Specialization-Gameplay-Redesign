# B041：目标枚举与独立地图标记
Document Owner: Codex
Build: B041 / modinfo53
Architecture: A0095
Status: S0098

## 范围与选择
用户授权继续合法位置提示。新UnitTargets.lua在Gameplay枚举本方城市目标，投资排除Potential4/无专业/投资pending，按Identity完成区域定位；施工取当前queue建筑/区域/奇观。不是把当前单位脚下当唯一候选。只读，没有新SQL/单位/项目/消费。
采用独立WorldAnchor标签，暂不写Hex_Coloring_Great_People共享图层，不清除任何UILens层，不改变接口模式。这是明确的视觉实现选择：目标地块上INVEST / BUILD TEST，不是原伟人的整格纹理。原版Base/Assets/UI/WorldView/PlotInfo.xml:2–24与PlotInfo.lua:729–730提供WorldAnchor/Instance和UI.GridToWorld(plotIndex)+SetWorldPositionVal先例。不会声称已实现原版同款高亮或自动寻路。

## 数据
Gameplay仅接UnitID与显式BuilderPreview开关，不信任UI位置。施工builder为DEV代理，正式Crew类型尚未定义。目标记录{plot,cityID,cityName}，以plot去重。逐城失败单独unknown，不能把未读到当作确认无目标；全局失败空列表/error。不持久化。
奇观遍历Map.GetCityPlots():GetPurchasedPlots(city)后验证当前奇观Index、plot owner/城市、DISTRICT_WONDER、HD地基标记、建筑未完成；缺失/歧义不猜。Gameplay静态先例HD Gameplay/Temp_Interface.lua:377，真实全集读取仍待本批用户验证。区域/普通建筑仍精确DistrictType/PrereqDistrict匹配，replacement未覆盖时unknown。
投资只依据永久Potential和pending，不受当前总督ACTIVE阻塞。
响应有version/token/owner/unitID；UI只绘制当前可见地块。当前实现不检查移动路径或水域可达，标记不等于立即可执行。
目标函数今后还需与消费入口统一使用；现有B040脚下函数仍保留，未宣称两者已完全去重或写入验证已接好。

## 生命周期
独立AddUserInterfaces，选移民自动读取；工人必须从Unit sites显式开启测试模式，模式非持久化，读档后默认关闭。
选中/移动/模式改变清自己Instances，不影响其它Mod；选择模式外隐藏。选择相同单位时5秒一次只读核对队列/投资变化，不在每帧发送Gameplay请求；新请求先撤旧列表，目标切换有最长约6秒显示延迟，消费不依赖标记。
读取timeout10秒，错误/unknown输出控制台和现有Unit sites底部状态。无shared Snapshot污染，使用UnitTargetSnapshot单独响应；多token排除旧响应。
后续如需优化刷新改为明确dirty通知，但不在本批靠事件历史推导当前目标。

## 验证
test_unit_targets.py实际运行UnitTargets和UnitTargetMarkers模块：投资远处枚举/满级排除、工人显式门控、建筑/区域/奇观标记匹配与缺失、非法队列剔除，独立UI选择/显示/清除/模式切换；LOCAL_SIMULATION_PASS。复用B040测试的mock初始场景，不执行其旧manifest版本断言。
全部Lua语法、XML和modinfo53文件存在STATIC_CONFIRMED。无游戏运行，不声明实机PASS。
备份DevelopmentBackups/Specialization-before-B041-target-markers含运行及文档；UUID/配置/D0010不变。
当前只有B041三案待测；B039/B040既有PASS不重发。下一步独立Crew外观/固定1charge与投资动作接入，不把标记当正式施工队完成。
