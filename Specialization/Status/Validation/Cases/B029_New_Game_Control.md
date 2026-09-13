# B029新局整数对照（取代旧档优先安排）

Document Owner: Codex
Status: USER_GAME_TEST_REQUIRED

目的：排除新Trait效果未在旧存档实例化。保持B029/modinfo36不变，不启动其它新功能。

1. 先在旧测试城点Carrier OFF清掉开关，然后回主菜单。新建Scotland (Specialization Test)测试局，Mod组合保持原样。建立首都即可；不需要学院、总督、商路或高级专业。
2. 选首都，确认P0-B-029。点Carrier +1 / +1.5一次，再点Read source totals，回传一张整面板截图。不要改市民、政策、建筑或结束回合。
3. 点Carrier OFF，再读一次，文字回报三项delta是否回到0即可；若没有回0再截图。先不要继续半点档。

判断：configured=1且三项delta均有对应整数增量，说明本测试路径可应用city yield；无倍率时预期各+1，有额外倍率按实际数值分析。OFF应恢复0。若新局仍configured=1且delta全部0，旧档初始化假说不足，需要进一步查挂载/条件刷新。此结果不证明小数或任意汇聚收益有效。

无需重测B028，不在本批推进旧网络撤销测试。不要求覆盖原有存档。
