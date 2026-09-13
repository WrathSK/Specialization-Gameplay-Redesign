# B010：选中城市的只读角色事实

## CURRENT AUTHORITATIVE STATE

运行P0-B-010 / modinfo17。新增Probe.CityRoleFacts，由既有Gameplay的Read governor请求调用；仅选中一城，没有自动全帝国扫描。未接NetworkState、专业锁定或收益，不写Property。

## STATIC_CONFIRMED

当前运行工程只有SPC_P0_FIRST_SPEC旧诊断读取，没有正式专业/潜力/首次完成账本写入者。SPC_P0_MARKER与正式专业无关。不能将缺失记录当默认Lv1、不能按现有区域推断首次完成顺序；即使旧诊断字段有值也只显示、不采纳。

CityRoleFacts读取当前owner/cityID和玩家GetCities():GetCapitalCity()返回城市的owner/ID，结果YES/NO/UNKNOWN。首都YES可确认center=YES_CAPITAL；非首都因Commerce专业未知，center仍UNKNOWN。capital getter缺失、返回nil或owner不匹配时不推定非首都。该组合的Gameplay实机行为是本次新增待验项，没有因旧广泛探针里出现同名调用而视为通过。

总督使用已验证的control/present/established/req2/3/4 Property。只接受数值1激活、nil/0不激活；control缺失、读取错误或非法类型则未知。阈值不连续、已建立却无present、有阈值却未建立，均标UNKNOWN_INCONSISTENT_PROPERTIES。连续有效时输出governorLevelCeiling=1..4，不称为真实头衔数或ACTIVE。专业和潜力未知时ACTIVE保持UNKNOWN。

输出为PARTIAL_ROLE_FACTS、GAMEPLAY_PROBE；cityKey仍owner:cityID快照标识。没有将不完整角色描述转成READY Network上下文，也没有放宽离线DeriveShadow的MOCK_ONLY限制。

## LOCAL_SIMULATION_PASS

新增test_city_role_facts.py：首都/非首都/缺失API、旧专业诊断值不采纳、无默认潜力/ACTIVE、门控1..4、0不激活、control缺失、矛盾阈值、非法类型、Property缺失、非测试玩家拒绝。SetProperty/GetDistricts/GetAssignedGovernor设为抛错，验证未调用。

test_specialization_p0.py与test_background_routes.py回归通过；只读扩展未影响已有请求或后台路线路径。所有结果为本地模拟，未启动游戏。

## USER_GAME_TEST_REQUIRED：一个小批次，两个城市

在现有Test存档加载B010，不要求改变总督、专家、区域或商路。

1. 选当前首都，点击Read governor。报告新增ROLE行应capital=YES、center=YES_CAPITAL。Specialization/Potential/ACTIVE均UNKNOWN是当前正确结果，不是读取失败。
2. 选一个非首都城市，再点Read governor。应capital=NO、center=UNKNOWN。无需判断其现有商业区域应不应该令它成为中心，因为尚无可信首次完成记录。

总督原有raw行只供对照，不重做升级/调离测试。Governor ceiling是条件上限，绝不等于ACTIVE。无需新建区域或写marker。

PASS：两座城市身份与上述结果对应、cityKey随选城变化、无error；没有凭空获得专业/潜力。FAIL：首都判断相反/未知、选城不更新或错误。正常最多两张截图；失败保留错误行与ROLE行，停止即可。无需内部ID手抄、剪贴板或不存在的Lua.log。

如果首都已被上次删城测试删除，请使用一个仍有明确首都的现有测试存档，不要为此重建整个测试局；若不方便则告诉我。

## 后续依赖

正式专业记录需单独设计有版本的持久事实和首次完成事件处理；旧存档无历史时的初始化策略不能自动猜测。本轮不实现这个策略、不要求用户现在确定。跨征服继承、永久UID和UI正式权威来源仍保持原待定状态。

## 文件

修改Probe.lua（角色读取与版本）、UI/P0Panel.xml（标题）、SpecializationP0.modinfo（version17）；新增test_city_role_facts.py及本报告；更新Architecture/Status。备份DevelopmentBackups/SpecializationP0-P0-B-009。Gameplay请求入口/SQL/后台路线实现均未改。
