# B054.71 后台初始化握手

Document Owner: Codex
Evidence: B054.70 USER_GAME_TEST_FAIL（用户口述未初始化）；B054.71 LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

本次Startup.log为2026-09-13 00:58:51，Modding.log明确注册/加载SPC_B054_Eligibility及SPC_B054_Discounts。只读DebugGameplay.sqlite已存在SPC_B054_Targets和596个载体。因此先前旧组件清单的解释不再适用于本次。

用户Read discounts只见“后台折扣尚未初始化”。源码的ready只有单次LoadScreenClose能设true，而后台在ready前不发送任何操作，存在双向等待的启动缺口。原提示没有ready/busy，无法仅据此完全确认引擎具体哪个事件未送达；补偿覆盖该缺口，同时增强诊断，不声称已在游戏验证修复。

改动：Gameplay接DISCOUNT_INIT；后台在shared模块可用、未ready时主动请求；EnsureReady幂等启动，重复不增加generation或重复附加。正常加载事件路径保留，旧载体清理同样执行。读取仍不初始化，不要求贸易/P0/购买UI打开。数值、来源规则、SQL、模板永久记录与D0016不变。

本地测试直接省略折扣LoadScreenClose，保留已存在网络/模板，然后运行真实后台脚本；可初始化、应用、降级/断网撤销和读档恢复，重复初始化幂等。旧账本/复制/投资/Crew保护回归通过。测试只在内存DB删除B054前缀重建fixture，未写外部游戏DB。

最小复测：重启游戏载入原存档，保留A工业IV→B商业III商路。面板须B054.71。B点击Read discounts，应显示A、最高40%及候选配置；检查B尚未建成的粮仓等匹配建筑价格。成功可口述；失败回传整段报告（ready/busy/generation/状态，不必截图也可复制文字）。不需新建局、重新连路或先完成多源/断网批次。
