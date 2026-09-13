# B040：共用单位地块读取与独立入口
Document Owner: Codex
Architecture: A0093
Status: S0095
Build: P0-B-040 / modinfo51
Design: D0010 unchanged

## 范围
用户澄清复用工人主要为外观，劳动力/按钮作为参考。施工队仍计划独立UnitType，不继承工人全部功能。
本轮将候选地点判定接入真实Gameplay只读读取；独立AddUserInterfaces入口跟随己方工人/移民，无需P0、无UnitPanel覆盖、无HD源码修改。工人仅代测施工地点，不假装成Crew，无劳动力消费/项目/新单位。本次尚未调查出HD任意扩展注册接口，选择独立界面避免共享文件覆盖，并不宣称已嵌入原生单位动作栏。
新位置规则仍是诊断候选，原市中心投资和B039免费注入保持。Spec未变；无新SQL，现有存档可用。

## 数据与验证
UI只发送所选UnitID，不发送CityID/合法性事实；Gameplay重新取unit当前坐标、plot owner、Cities.GetPlotPurchaseCity，然后扫描同owner同city区域。
投资按EffectiveFacts.first.districtID/type找已完成Identity锚点，匹配单位坐标、Settler类型、Potential<4。
建筑按当前queue Building.PrereqDistrict找所属区域；区域按当前queue DistrictType找对应地基。当前仅精确type匹配，replacement区与普通PrereqDistrict映射不完整时UNKNOWN，不能静默匹配其它区域。
奇观按单位当前plot的DISTRICT_WONDER与HD_UNCOMPLETED_WONDER、当前队列Index、未完成状态共同核对。HD Property缺失拒绝验证，不据旧记录独自认定。本轮是接口观察而不是最终消费授权，后续写入操作需同请求重新检查，不能复用旧报告。
施工行传入“假设一劳动力Crew”的候选参数，只输出location only；无真实Crew资格/charges验证的PASS。
海上区域可达性、所有存档的HD奇观标记、原生选择界面表现仍USER_GAME_TEST_REQUIRED。
点击返回有token/version匹配；移动/改选隐藏旧报告；报告不自动持续请求Gameplay。0.2秒UI本地检查选择，只有点击发一次请求。

## 本地结果
test_unit_site_probe.py执行实际UnitSiteProbe及UI模块，覆盖建筑/区域/奇观、错位、投资满级、非移民、错误奇观标记、非建设目标、无效owner/unit，UI显示/请求/匹配/移动清除。LOCAL_SIMULATION_PASS。
全部runtime Lua语法、XML、manifest51文件存在STATIC_CONFIRMED。没有运行游戏。
老B039测试固定manifest50，本轮未改其历史预期；B039内核未修改，不重复已通过实机注入。
备份：DevelopmentBackups/Specialization-before-B040-unit-sites，RuntimeSnapshot及文档/hash。
下一步根据三个新读数case确认接口后接独立Crew外观/1charge、单位执行及项目；不借机重测既有收益。
