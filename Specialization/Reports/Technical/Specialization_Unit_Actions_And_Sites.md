# 施工队与移民投资：单位按钮及目标地块调查
Document Owner: Codex
Design Basis: D0010 + 当前用户调查请求
Implementation: B039 / modinfo50不变
State: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS（仅以下限定范围）

## 用户请求与设计边界
B039用户确认完全正常。继续推进施工队，工人模板与固定1劳动力作为实现方向。用户要求共同调查施工队和移民投资的单位按钮以及类似伟人的合法区域/地块限制。本轮未发布新单位/项目/按钮，没有将调查建议自动写入Accepted Spec。
D0010 CREW-003/PROG-002只要求己方城市；现有InvestmentAction实现额外限定市中心。候选改为：Crew站当前目标奇观地基/区域地基/建筑所属区域，Settler站本城已锁定专业的已完成区域。不能在第二个无关专业区域投资，也不靠区域放置取得专业。这是待后续确认的精确位置语义，现有市中心操作保持有效。CREW-004速度与五档开放时间继续TBD，不以调查自行决定。
当前不需新实机测试，不重发B039。

## 静态证据（本机HD）
源根：/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070

- UI/Replacement/DL_UnitPanel.lua:498–575遍历m_HDUnitCommands，支持CanUse / IsVisible / IsDisabled、图标和提示；EXECUTE_SCRIPT发送Gameplay事件。默认在发送后额外删除单位（537–546）；我们的动作若接此路径必须DoNotDelete=true，由Gameplay校验和消费，不照搬UI无条件删除。
- UI/Additions/HD_UnitCommandDefs.lua:178–224为奇琴伊察，核对plot:GetWonderType；124–172为回收中心，在所属区域检查城市及条件。
- 同文件:564–636秦始皇后期奇观工人动作是更直接先例：UNIT_BUILDER、己方plot、DISTRICT_WONDER、HD_UNCOMPLETED_WONDER、当前队列奇观Index匹配、尚未完成；DoNotDelete=true。
- Gameplay/Misc.lua:585–600在OnDistrictConstructed时记录HD_UNCOMPLETED_WONDER。它是事件Property，不可独自证明当前目标；旧存档缺记录/陈旧记录/切换目标必须拒绝不明状态或另找实时位置来源。不能将该Property直接当永久真实地基。
- UI/Additions/HD_Utils.lua:1349–1373用plot districtID及city:GetDistricts():FindID取得区域、IsComplete、当前目标、成本进度。区域建造位置有静态先例，但桥接到我们的Gameplay仍需实机。
- Gameplay/HD_Common.lua:149–152及Gameplay/RegionalYields.lua:65使用GetBuildingLocation，已完成建筑位置有先例；不能据此声称未完成奇观必能返回位置。
- UpdateDataBase/DL_GreatPeople.sql:289使用GreatPersonIndividuals.ActionRequiresIncompleteWonder；另有ActionRequiresCompletedDistrictType。它们属于伟人定义，不是可直接添加到普通工人/移民的通用Units字段。普通单位宜用自定义判定模拟同样的可用/不可用表现。
- Gameplay/HD_Common.lua:1075–1090的ConsumeUnitBuildCharges通过负劳动力Ability实现，不等于任意单位通用的固定一次消费事务。

## 模板方案及风险
当前只读DebugGameplay.sqlite的UNIT_BUILDER为4劳动力（HD），带CLASS_BUILDER及其它tags；不应整行/所有tags盲拷贝。
建议独立Crew UnitType，复用builder外观/图标/陆地平民移动基础，显式BuildCharges=1，不继承CLASS_BUILDER、改良/砍伐操作授权或其它文明专属tag。五档Production属于单位规格，不能从实际劳动力数相乘得出；即使发生外部加劳动力，也不能导致再次注入。CanTrain/购买、项目产出和视觉映射需要分别定义。
是否有按“所有有劳动力的单位”作用的Modifier、是否能安全保持显示1，需要后续最终数据库审计及新局验证；本轮不声称已隔离全部第三方加成。陆地模板在港口/水上奇观的可达性也须按真实登船权限核对，不能偷偷取消地块要求作为fallback。

## 接入方式
HD代码包含固定名称的命令defs，不是跨Context公开注册服务。当前尚未证明本Mod可以从独立AddUserInterfaces直接修改它的局部命令表。不能写HD文件或覆盖整个UnitPanel来图省事。
下轮优先调查UnitPanel同Context安全扩展；若无稳定挂接点，考虑本Mod独立、跟随当前选中单位的动作小面板（无需P0面板）。这是按钮位置实现候选，不改变单位的Gameplay合法性。暂未部署任何方案。
两种动作应共用：当前选中单位→解析所属城市/目标plot→可用性提示→Gameplay重新读取并核对→已有投资事务或施工消费执行。UI不能决定消耗成功，也不能传“合法=true”后绕过Gameplay。施工消费+生产注入不是引擎原子操作，正常重复拒绝必须保留；不确定失败不自动重试/发放，恢复不能凭UI回报。

## 本轮完成的本地准备
唯一源码目录新增UnitActionSitePolicy.lua，纯数据候选判定，未加入modinfo/import、无运行调用。DevelopmentTests/test_unit_action_site_policy.py执行实际Lua模块：
- 三类施工目标；不在目标plot、外城owner、非当前目标、已完成、未知来源、非1charge拒绝；
- 投资已完成Identity区域可用；非Identity区域、未完成、Potential4、未知位置拒绝。
结果LOCAL_SIMULATION_PASS，仅证明规则函数，不证明游戏API/路径寻路/真实劳动力/按钮/消费。
实际adapter必须自行取得可靠目标cityID/plot；verified是adapter内部可信标记，绝不能直接来自玩家UI参数。

## 下一步顺序
1. 接真实只读target定位，同时用于Crew与投资的候选按钮提示；保持旧消费操作直到新位置语义确认。
2. 独立一劳动力Crew最小单位、可选单位动作UI；先开发测试生成，正式五项目待速度/开放策略明确后接入。
3. Gameplay消费和限额注入组合，复用已通过B039内核与投资重复保护；再给一个小批次：合法位置执行、错位不消耗、读档/重复保护。
4. 正式五项目及完整单位表现验收。不会把本轮离线PASS扩大到这些步骤。
