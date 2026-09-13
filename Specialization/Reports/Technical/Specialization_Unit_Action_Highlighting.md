# 移民投资与施工队合法地块高亮调查
Document Owner: Codex
State: STATIC_CONFIRMED（实现先例）；新高亮未部署
Design Basis: D0010 + 用户追加调查；不修改Accepted Spec

## 结论
可行方向明确：自行枚举合法目标，再用现有地图高亮绘制。不是把普通单位伪装成伟人，也不是给Units表加伟人专有字段。未声称自定义图层任意名字即可注册成功。

## 本机代码证据
原版根：
/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI
WorldView/SelectedUnit.lua:
- 21: UILens.CreateLensLayerHash("Hex_Coloring_Great_People")
- 109–153: RealizeGreatPersonLens先清旧层；GreatPerson:GetActivationHighlightPlots取位置；将plotIndex转换为{"Great_People",plotIndex}，UILens.SetLayerHexesArea(layer,playerID,areaPlots,activationPlots)，ToggleLayerOn。
- 167–240、374–399：选中/状态/移动点等相关刷新；424–426清除并关闭该层。
HD根：
/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070
UI/Replacement/DL_SelectedUnit.lua:108–138覆盖RealizeGreatPersonLens，优先HDGreatPersonGetActivationPlots，自算列表后调用同一绘制路径；无列表再回原实现。
UI/Additions/HD_GreatPeople_Common.lua:30–64枚举玩家区域、完成状态、当前生产目标和区域坐标，为米马尔·希南计算激活位置；73使用Map.GetCityPlots():GetPurchasedPlots(city)枚举城市地块。
这证明“列表自行计算，复用高亮显示”有HD静态先例。引擎GreatPerson getter不负责我们自定义的投资/施工规则。

## 建议数据管线
1. Gameplay根据当前资格和真实城市/目标枚举候选记录，保持与最终消费合法性函数一致；UI接收只读位置列表。界面高亮不是消费授权，点击仍由Gameplay重新验证。
2. 投资：所有本方可投资(Potential1–3、无未完成事务)城市的Identity已完成区域；不要求已经站上去，否则无法提示目的地。筛选目标与“到达目标”的判定必须拆开，不能直接用当前Check的单位坐标相等条件枚举。
3. 施工：本方当前在建合法Building/District/Wonder的位置去重。同城只能考虑当前生产目标，不高亮其它队列项。建筑落所属区域；区域落自身地基。
4. B040奇观只验脚下；高亮需新增从城市区域/plots枚举整个目标的位置，并交叉核对当前奇观类型、owner、未完成、HD地基记录。缺失时不猜位置，保留诊断。不能使用B040报告文本反推位置。
5. 不将这些高亮叫“本回合可达”：位置合规与移动点、登船/水上通行、单位占位/路线可达不同。最终单位按钮需要完整的当下可执行校验。

## 图层与交互风险
原版和HD在选中变化时都会清除同一Hex_Coloring_Great_People层。独立Context直接写此共享层可能被随后刷新清掉，也可能错误清除刚选中的真正伟人高亮；不能靠每帧强制重画争抢。
先研究在现有选择刷新之后协调写入、仅在当前本方Settler/Crew有效时使用，并在改选/取消、非选择模式、读档/回合/目标变化时撤销。选择真实伟人后不再写或清该层。
移民原有建城水源图层必须保留，不接管移动/建城输入模式；施工队不能影响原工人改良提示。若共享层时序无法可靠隔离，再比较独立已注册图层或自有世界坐标标记，说明视觉差异，不静默假定任意hash能新增层。
不修改HD或原版SelectedUnit文件；不得覆盖整个文件破坏其它Mod效果。

## 建议实现顺序
先完善与单位消费共用的目标枚举，再接选中提示；高亮只是可用性帮助，不阻塞已通过的位置/生产力逻辑。
等施工队独立单位及投资动作一起接时，给一组小测试：选中两种单位出现目标，切换/取消清除，真实伟人和移民建城原有提示仍正常。不在本轮要求用户测试未部署功能。
本轮仅源代码调查，没有新增模拟或高亮实机PASS；运行仍B040/modinfo52。
