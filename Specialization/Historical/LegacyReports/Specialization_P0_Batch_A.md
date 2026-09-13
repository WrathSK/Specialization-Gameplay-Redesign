> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

> **用户最新回报：A2-R已USER_GAME_TEST_PASS**。确认重新加载且未再Mark，city=65536、marker=P0-A-003:1:1不变。以下步骤保留为历史，不要求重复执行。剪贴板交付为USER_GAME_TEST_FAIL；下一批可用面板截图回传。A3/A4仍待独立探针准备。

# P0-A-003：只重测 A2-R，暂停旧 A3/A4

A1已由用户确认成功，不必重做。P0-A-002点击Mark卡住记USER_GAME_TEST_FAIL；以下新版测试状态是USER_GAME_TEST_REQUIRED。

## 恢复与准备（用户操作）

如果游戏仍无响应，请自行退出；必要时使用系统强制退出。不要覆盖唯一测试存档。重新启动游戏后才会加载修改过的Lua；在当前已加载游戏中继续点击不会切换到新版。

加载原来的测试文明存档/自动存档，优先选Mark前已建立首都的存档；没有可用存档才新建同样测试局。无需重做A1。保持原Mod组合不变。打开Specialization P0，标题必须为 **P0-A-003**。如果仍显示002，停止并回传标题截图。

## A2-R1：仅读取（不写入）

1. 选中测试文明首都，点击 **Read marker** 一次。
2. 游戏保持响应时点击 **Copy latest**，把剪贴板粘贴保存为 `A2-R1-read.txt`。
3. 预期：`matched=true`，`ACK city=<数字> marker=nil`。若此前已成功写过，marker也可能是已有字符串，不要求清空。ID自动记录，不用手抄。

PASS：操作后游戏仍可响应，返回当前请求的ACK及marker。FAIL：卡住/报错，或没有匹配ACK；仅DISPATCH_RETURNED不算通过。失败立即停止，不点Mark。

## A2-R2：写入与存读档（R1通过后）

1. 同城点 **Mark selected city** 一次；若正常响应，点 **Copy latest**，保存为 `A2-R2-mark.txt`。
2. 预期 `matched=true`、ACK marker为字符串。初始marker=nil时，它应等于本次`request=`值；已有marker时必须保持原值。点击 **Baseline + Copy** 也可保存当前结果。
3. 另存为 `SPC_A003_marker`，由你手动返回主菜单再加载这个存档。
4. 选同一城市，只点 **Read marker**，再点 **Copy latest**，保存为 `A2-R2-reload.txt`。读档后不要再Mark。无需比较request/response新值，只对比两份记录的city和marker。

PASS：Mark后和重载后都不卡住、都有匹配ACK，同一city的marker字符串完全一致。FAIL：任一步卡住、ERROR、没有ACK，或重载后marker缺失/改变。只有读写正常而没完成重载时，记录“读写正常，存读档未测”，不要整项判PASS。

## 失败回传

- 哪一步、哪个按钮、是否仍能移动鼠标/关闭面板；P0-A-003标题及最后面板状态截图（能截图时）。冻结时UI可能尚未来得及绘制最新阶段，截图不是精确调用栈。
- 所有已保存的上述txt。若游戏还响应但没有ACK，Copy latest仍会导出PENDING_OR_ERROR和当前阶段，可直接回传；不要反复Mark。
- 如有Lua.log，退出后、下次启动前保存整份；同时保存Database.log、Modding.log、GameCore.log。当前日志目录：`Firaxis Games/Sid Meier's Civilization VI/Logs/`（相对本工作目录）。没有Lua.log就说明没有，不需要为此重跑故障。
- 日志阶段：BEFORE_DISPATCH、DISPATCH_RETURNED；Gameplay RECEIVED、BEFORE_GET、AFTER_GET、BEFORE_SET、AFTER_SET、ACK/ERROR。pcall不能终止卡在原生接口内的调用，因此本版仍需用户验证。

这一轮只做以上两小步；不测Governor、Specialist、Adjacency或Trade。回传后再决定恢复哪个独立采样模块。
