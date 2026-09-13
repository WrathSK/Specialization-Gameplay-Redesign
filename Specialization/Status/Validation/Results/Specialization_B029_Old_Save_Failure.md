# B029：旧存档开关有值、收益未生效

Document Owner: Codex
Date: 2026-09-12
Verification: USER_GAME_TEST_FAIL（旧存档+1收益观察范围）
Runtime: B029 / modinfo36（未改）

用户确认加载此前旧存档，未在B029后创建新游戏。两张截图均逐张读取。

| 图/时间 | city | configured | Science/Culture/Production | delta |
|---|---|---|---|---|
| 1 / 01:53:58 | 65536 | 0 | 7.5 / 1.296875 / 11 | NO_BASELINE_THIS_LOAD |
| 2 / 01:55:15 | 65536 | 1 | 7.5 / 1.296875 / 11 | 0 / 0 / 0 |

开关状态更新与基线记录有效，但+1档实际产出没有增加。重复点击不累加依用户人工回报；没有1.5档/关闭的截图，不把未观察内容标通过。整数档已不生效，当前不能归因于小数截断。

STATIC_CONFIRMED：实际DebugGameplay.sqlite mtime为2026-09-12 01:53:10，本次只读查询确认六个Modifier、测试Trait六个挂载表行、两组RequirementArguments齐全。主体类型/PropertyName/PropertyMinimum与HD RegionalYields所用结构一致，城市中心plot写入位置同源。缓存数据存在只证明数据库层，不证明旧存档中创建了对应Modifier实例或条件已运行。

目前优先假说是旧档玩家Trait新增效果没有实例化；未证实，不能宣称根因已定位。也不能通过直接Attach同一效果强行修复，因为若原Trait实例存在可能造成重复。原测试只凭GameInfo定义存在允许继续，遗漏了实例生命周期前提，应修正测试方案而非立即更改收益算法。

下一步[新局整数对照](../Cases/B029_New_Game_Control.md)，保持完全相同运行代码，改变初始化条件。若新局也为0，再调查实例/requirement/刷新，不继续堆叠新效果。旧档最后请OFF，不把未增产当开关已撤销。

[原件](../Evidence/B029-Fail/)已归档并前后hash核对。运行、Design、Tests未改；没有新本地模拟或新实机PASS。
