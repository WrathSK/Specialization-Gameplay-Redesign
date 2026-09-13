> 最新结果：B4-1/B4-2用户均已执行。任务列表与存读档子项通过，四组端点参数均nil，不能判全项PASS；无需重复下方旧步骤，见Specialization_P0_B005_User_Result.md。

# P0-B-005：修正 Gameplay 单位类型读取

## CURRENT AUTHORITATIVE STATE

用户B4-1截图 `Screenshot 2026-09-11 at 11.42.55 AM.png`（系统实际文件名含窄空格）显示：P0-B-004、LoadScreenClose、turn=2、seq=2；错误为TradeRouteProbe.lua:13 GetUnitType:ABSENT。报错在单位类型识别处，不是GetOperationType/GetOperationParameter处。

USER_GAME_TEST_FAIL：B004使用unit:GetUnitType()导致自动扫描中断。USER_GAME_TEST_PASS（仅此子项）：本次LoadScreenClose自动采样已执行并生成可查看的诊断缓存。没有读取到路线任务参数，不能据此判定operation来源方案成功或失败；路线全集/撤销继续BLOCKED。

## STATIC_CONFIRMED

官方PiratesScenario_StartScript.lua:891、1269、1554在Gameplay使用unit:GetType()；HD Gameplay/Misc.lua:612也使用GameInfo.Units[unit:GetType()]。B005将新自动探针改为GetType，不回退UI接口、不改路线权威约束。

改动：TradeRouteProbe.lua类型getter与简短错误显示；Probe.lua、modinfo、面板标题版本同步P0-B-005（modinfo 12，UUID不变）。面板错误保留第一行接口原因，完整异常仍print供可用日志渠道；不再让堆栈路径占满面板。运行包备份DevelopmentBackups/SpecializationP0-P0-B-004。

## LOCAL_SIMULATION_PASS

test_trade_route_probe.py：fixture改为Gameplay GetType，并把GetUnitType设为一调用即报错，确保不再误用。验证缺失GetType仍明确失败、错误显示不含堆栈，以及初始化/读档/回合/dirty既有路径。

test_specialization_p0.py：Lua编译、XML与manifest、既有隔离探针/按钮行为通过。没有启动游戏、没有SQL或正式网络收益改动。

## USER_GAME_TEST_REQUIRED

仅重试B4-1被接口错误挡住的部分：由用户重新加载原四商路存档，使脚本更新到P0-B-005；进入地图前不打开贸易UI。随后看Route state (Game)已经生成的缓存，截图即可。无需新局、新商路、分页或总督/专家重测。

预期不再出现GetUnitType:ABSENT，并能继续显示引擎计数、匹配任务、未知任务及参数；是否满足4/4/0仍待实测。其它ABSENT或匹配失败时直接停止回传，不执行B4-2，不靠过回合掩盖初始化失败。B4-2暂缓，先返回修正版B4-1结果。
