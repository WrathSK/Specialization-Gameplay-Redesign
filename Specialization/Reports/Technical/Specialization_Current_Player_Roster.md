# 当前玩家名单与启用资格分离

Document Owner: Codex
Design Reference: D0007 / ELIG-001..006
Architecture Reference: A0030
Scope: STATIC_RESEARCH_AND_LOCAL_CANDIDATE / NOT_DEPLOYED

## 结论

STATIC_CONFIRMED：原版和HD的Gameplay脚本使用PlayerManager.GetAliveIDs()返回玩家编号列表，再读取PlayerConfigurations/Players。它是当前运行参与者筛选的合适候选，不等于已取得本局返回值。

B017已经实测54–61返回CIV_NOT_READY。本轮在原版UI/脚本/常量使用及HD Lua/SQL/XML的相关检索中未找到可可靠断言“54–61固定是空槽/AI/预留对象”的定义；有限源码搜索不是证明不存在这种引擎定义。不能按编号硬排除，也不能把未找到定义改写成STATIC_CONFIRMED空槽。

当前Logs/Game_PlayerScores.csv仅见玩家0记录，得分日志不是完整玩家名单，不能据此证明其它玩家不存在。没有新Lua逐槽位证据。本轮不改日志配置，不要求用户重复截图。

## 本机静态证据

Assets根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets`。
HD根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070`。

- 原版`DLC/WarMachineScenario/Scripts/WarMachineScenario.lua:25`在Initialize遍历GetAliveIDs，然后用对应PlayerConfigurations读取文明类型；`WarMachineScenario.modinfo:38–40`确认AddGameplayScripts上下文。
- HD `Gameplay/Wonders.lua:756–760`在建筑处理使用GetAliveIDs，经Players读取玩家，随后另检查IsMajor；`DL.modinfo:1867–1883`明确Gameplay加载。不能据此把本项目锁为major-only或Human-only。
- `pairs(Players)`是B016全槽位诊断使用方式，与当前存活名单不是同一个契约。GetWasEverAliveIDs关注历史参与，不作为当前周期更新名单；两者均不能证明城市没有永久历史。

## 候选接口及本地结果

新增`DevelopmentTests/CurrentPlayerRoster.lua`，不注册运行包。`Collect(env, readEligibility)`先读取完整GetAliveIDs数组，校验/去重/排序，再调用既有资格读取候选。输出contextSource=GAMEPLAY_CANDIDATE，包含current、ordered、enabled、disabled、unknown。

分类明确分开：
- NOT_CURRENT：完整名单里没有该编号，仅表示本次无当前运行成员关系，不等于从未参与，也不更改永久事实。
- DISABLED：名单内，资格读取成功且明确没有绑定。
- UNKNOWN：名单失败、资格未就绪/失败/身份不匹配；不授予运行许可。
- ENABLED：名单内且本次资格读取明确启用。

每次Collect产生独立新结果；名单读取失败返回UNKNOWN和空授权列表，不返回部分成功或上一轮enabled名单。个别资格失败只记该玩家UNKNOWN，不阻塞其它明确启用玩家。调用者仍须在安全时点确认名单可用于运行；空数组本身不证明初始化已经完成，当前结果不是正式写入授权。

无城市/Property读取，不按编号上限54、文明名或Human硬排除。128只是候选输入防护上限，不是原生槽位分类；未来超过此界限返回UNKNOWN，不能截断后结算。

LOCAL_SIMULATION_PASS：test_current_player_roster.py通过。覆盖名单内外、未知与未启用分离、去重/高编号61可启用、空/稀疏/非法/异常名单、错误资格owner、名单移除/重新出现以及与EligibilityCarrierCandidate实际组合。只证明模型行为，不证明游戏淘汰/复活事件或本局54–61的身份。未重跑不受影响的旧测试。

## 正式接入边界与下一步

将当前玩家名单和Trait资格作为两个不同前置，永久事实保存仍独立。正式入口不能消费B017 UI显示缓存授权；应在Gameplay安全时点重新建立名单并清除旧派生运行许可，恢复后重新计算。名单失效不删除城市成果，名单外不能当AcquireUnassigned的从未参与凭据。

实际GetAliveIDs在当前组合Mod/初始化/重载的返回值尚需未来接入批次验证，但不为辨认固定编号单独反复发探针。本轮无新实机批次；下一步完善资格入口的失效与重新授权边界，再合并最小运行验证。现有B016/B017用户PASS仅保持原观察范围。

Design及运行B017/modinfo24不变。备份与protected_hashes在DevelopmentBackups/Specialization-before-current-player-roster；未启动游戏。当前任务/验证唯一入口：[Status](../../Status/Specialization_P0_Status.md)。
