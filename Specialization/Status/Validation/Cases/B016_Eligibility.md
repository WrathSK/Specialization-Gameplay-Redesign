# B016：自动启用资格诊断（两案）

Document Owner: Codex
Build: P0-B-016 / modinfo23
Verification: USER_GAME_TEST_REQUIRED（等待用户游戏内结果）

使用现有Specialization测试文明存档，无需新局、选城市、建城或过回合。不要先操作其它探针。B016新增诊断只读；旧B015功能保留。按钮只显示已有Gameplay记录，不会请求采样。所有游戏操作由用户执行。

## B016-1：加载现有存档后读取

1. 加载现有测试文明存档，等正常进入可操作地图。
2. 打开Specialization P0，确认标题P0-B-016。
3. 点击Read eligibility，截图整个面板。

比较字段：`LoadScreenClose=REGISTERED`；`INITIALIZE`有记录；`LOAD_CLOSE | ENABLED | EXPLICIT_TRAIT_BINDING`；LOAD_CLOSE汇总COMPLETE。初始阶段如为UNKNOWN，保留原因，不能宣称初始时点已就绪；本案主要验证加载结束时自动恢复。

PASS：上述LOAD_CLOSE字段符合，且正常多文明测试局中“未启用”至少1（有一个未绑定载体玩家）；不要求“未知”一定0，因为非普通玩家槽位可能没有配置，出现时保留截图供分析。UNKNOWN个别槽位不等于可启用。不要据此宣布所有AI或所有槽位验证通过。

FAIL：加载结束仍无记录、当前玩家UNKNOWN/DISABLED、汇总UNKNOWN、钩子ABSENT/ERROR或点击报错。若标题仍B015则为旧包加载，不能判断新接口失败。不要靠点击其它按钮或过回合掩盖首次读取结果。

## B016-2：保存并重新加载

1. 在同一局保存；返回主菜单，重新加载该存档，中间不改变局面。
2. 直接打开面板，点击Read eligibility，再截图。

PASS：当前玩家仍LOAD_CLOSE ENABLED/EXPLICIT_TRAIT_BINDING，汇总COMPLETE，钩子REGISTERED，启用/未启用数量与上一张一致。按钮不负责恢复，所以这证明当前批次后台采样在读档后存在；不证明正式状态或收益系统已启用。

FAIL：恢复后无LOAD_CLOSE记录、当前玩家失去资格、异常数量变化或错误。INITIALIZE是否早于配置就绪单独记录，不用手算或修复。

## 回传

两张按顺序投递到Specialization/ScreenShots，使用默认文件名即可。不必复制文本。失败时保留完整面板和当前Logs/Lua.log；若是Mod加载/数据库错误另附Logs/Modding.log与Database.log（以实际生成路径为准）。用户不需要手抄ID；日志含[SPC][P0-B-016][ELIGIBILITY]及每个player结果。无需重测B010/B015。
