> 最新结果：B4-1/B4-2用户均已执行。任务列表与存读档子项通过，四组端点参数均nil，不能判全项PASS；无需重复下方旧步骤，见Specialization_P0_B005_User_Result.md。

> 当前执行修订（B005）：B4-1发生GetUnitType:ABSENT，已修正Gameplay getter为GetType，运行版本P0-B-005/modinfo 12。现在仅重试B4-1并回传截图，B4-2暂缓。详见Specialization_P0_B005_Unit_Type_Fix.md；下文B004版本号是初始批次记录。

# Test Batch B004 — 自动 Gameplay 候选来源（最多2项）

状态：USER_GAME_TEST_REQUIRED。**这是新来源的可行性测试，不是重复UI起终点/分页测试，也不是正式网络验收。** 本轮只做以下两项；先不测试战争、征服、夷平、自然结束或删除商人。即使两项候选通过，也不能宣布完整路线生命周期可靠。

## 准备

使用你已有、包含四条商路的 Test Civilization 存档；不需要新游戏、不需要再开新商路。脚本版本已更新为P0-B-004（modinfo 11），无SQL改动。由你手动按平常方式重新进入游戏并载入；不要只在上一版本已经运行的局内继续点按钮。

新增的 **Route state (Game)** 位于P0窗口顶端。它只显示Gameplay事先采样的缓存，不触发枚举、不读取UI路线列表；不用选择城市，不用Copy。此前的Read routes (UI)和Route events (Game)本批都不需要点。

实际采样自动发生在Gameplay初始化、LoadScreenClose、测试玩家回合开始/结束。dirty事件只标记原因，不构造路线。日志前缀为 `[SPC][P0-B-004][TRADE_STATE_PROBE]`。

## B4-1：完全不打开贸易UI的初始化

1. 载入原来的四商路存档后，不打开原生贸易路线界面、商路选择器或P0面板，不创建/删除路线，也不结束回合。
2. 正常进入地图后即可查看P0里的 **Route state (Game)**。这个点击只看缓存，因此不能使一个失败的自动初始化“补成功”。
3. 记录/截图以下几行即可：采样原因（INITIALIZE / LoadScreenClose / PlayerTurnActivated）、引擎路线计数、匹配建商路任务数、未知任务数。本机当前没有发现Lua.log，因此本批以缓存显示截图为主，不依赖日志文件一定生成。

**候选PASS判据**：自动记录在点击按钮前生成；正确存档下engineCount=4，matchingOperations=4，unknownOperations=0；面板四名商人的四个命名参数均为可解释数值。面板会显示最多6名商人的task与X0/Y0/X1/Y1参数；你只需截图，由我判断这些候选坐标，不让你手算ID或坐标。

**FAIL / 停止判据**：UNAVAILABLE/ABSENT、没有自动记录、engineCount与已知四条不符、matchingOperations不是4、参数UNKNOWN。尤其“引擎4，匹配0”表示当前operation不按这个候选假设表达路线；不要因此重建四条商路或继续后面的测试。回传面板截图即可；如产生Lua.log也可保留。

即使数字相等，也只是候选可以继续研究；同数量不代表已经验证一一对应或当前性。面板的`authoritative=BLOCKED`和“未启用收益”是预期提示，不是测试失败。

## B4-2：无UI干预的再次存读档恢复（只在B4-1无错误时执行）

1. 在不改变任何路线、不结束回合的前提下，另存为一个测试存档（名字随意）。
2. 退出到主菜单，再加载刚保存的存档。
3. 同样先不打开贸易UI/P0面板。进入地图后，查看Route state (Game)已有记录。
4. 应仍为engineCount=4、matchingOperations=4、unknownOperations=0；不需要新增路线、点Read routes或过回合来恢复。四个商人任务参数由我在两次截图中对比。

**候选PASS判据**：没有操作路线或UI补采样，加载后的自动记录重新列出四名商人的候选任务参数，并与读档前一致。

**FAIL判据**：空/旧缓存、自动采样不存在、计数变化、任务/参数丢失，或必须人为开路线/过回合后才出现。回合fallback能读到也不能当“载入即恢复”PASS；请如实报告出现在哪个阶段。

## 需要回传的材料

优先：两次Route state (Game)缓存截图，系统默认名放DevelopmentReports/ScreenshotInbox即可，不需上传或重命名。本机检查时没有Lua.log，不能让你寻找一个未生成的文件。任务参数和自动采样原因已直接放到面板上。

如果本次实际生成 `Firaxis Games/Sid Meier's Civilization VI/Logs/Lua.log`，可以保留作为补充；准备继续游戏时可复制到ScreenshotInbox，保留原名。无需为本批更改游戏日志设置。

无B004标题/无自动记录时另保留Modding.log（本机存在）；Game_TradeManager.csv可辅助核对实际路线变化，但绝不会作为权威路线状态。你无需手抄任何ID或坐标。

完成后停止，等待分析。本批暂不要求删商人：先证明自动来源值得继续，再针对结束/删除/战争等安排下一小批。
