# B007 用户实机结果：初始化/读档通过，城市删除后重建未完成

## CURRENT AUTHORITATIVE STATE

用户以全新测试存档执行，再保存/加载；本次基线为三条商路，不沿用旧批次四条假设。运行包仍P0-B-007 / modinfo14，本轮仅核对证据与更新文档，不修改运行代码。

## CONFIRMED — USER_GAME_TEST_PASS

B6-1：Screenshot 2026-09-11 at 1.41.36 PM.png。
B6-2：Screenshot 2026-09-11 at 1.43.00 PM.png。
两图均COMPLETE_UI_SHADOW，turn=1、seq=2、触发LoadScreenClose、当前3条、Gameplay MATCH（仅数量/商人ID）。首次自动完成INITIALIZE / 3条，最近变化+3/-0，刷新次数2，系统通知0，Context更新0。

路线均为：
- Aberdeen (Test) → Edinburgh (Test)，商人327684。
- Edinburgh (Test) → Stirling (Test)，商人393221。
- Aberdeen (Test) → Stirling (Test)，商人458758。

结合用户对执行B6-1/B6-2的说明，确认该三路线存档的后台读取和读档重建通过。不要求重新执行旧四路线场景。UI影子读取通过不等于纯Gameplay权威全集provider成立。

## USER_GAME_TEST_FAIL / 部分成功：B6-3-CITY

第三图Screenshot 2026-09-11 at 1.43.46 PM.png。用户说明Cheat Panel无法删除商人，改为删除城市。此项独立命名B6-3-CITY，不计入原B6-3（删除商人）。

截图状态UNKNOWN，原因CityRemovedFromMap，无可用当前快照；刷新次数仍2、系统通知0、Context更新0。顶栏商路显示1/2，而此前3/3；不能用顶栏代替当前路线记录或推定已保留正确端点。

USER_GAME_TEST_PASS（窄范围）：城市删除事件已送达，旧snapshot被失效，不继续发布旧三条路线。
USER_GAME_TEST_FAIL（所观察结果）：城市删除后未生成新的完整路线集合。未展示撤销两条并保留剩余一条，不能登记完整撤销通过。截图也没有证明永远不恢复或回合兜底失败。

## 调度结论与下一步

两种更新计数在三图均0；本场景没有观测到SystemUpdateUI或Context更新回调。加载直接dispatch路径已通过；依赖上述回调消费dirty的路径仍不能视为可靠。计数0不等于API在所有context都不存在。

下一轮应处理城市/路线变更后的独立刷新路径与引擎状态稳定时序，保留UNKNOWN隔离，避免同步事件中读到过渡状态后永久停住。不得将事件日志变成路线事实，不由查看按钮触发刷新；不接正式收益。

## USER_GAME_TEST_REQUIRED

原B6-3商人删除未执行；无需用户寻找新的cheat工具。城市删除后的完整重建需修复后单独复测；本轮不追加测试。自然结束、取消、掠夺、战争、征服等仍未确认，Cheat Panel删城不等于正常征服/夷平。

## 文件与审计

截图保留默认名称于ScreenshotInbox。本文保存必要数值，日后无需靠文件名推断结果。Architecture / Status已同步，B006失败和B007修复前待测记录保留历史。
