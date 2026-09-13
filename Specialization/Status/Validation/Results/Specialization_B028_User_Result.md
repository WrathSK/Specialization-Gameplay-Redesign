# B028：城市产出只读与刷新两图复验

Document Owner: Codex
Date: 2026-09-12
Runtime: P0-B-028 / modinfo35
Verification: USER_GAME_TEST_PASS（用户实机，仅本批观察范围）

用户明确人工检验pass，两张图逐张复核。均为city=65536、specialty=RESEARCH、Stirling (Test)，B028 ACK，未见UNKNOWN/ERROR。

| 时间 | Gameplay科技 | Gameplay文化 | Gameplay生产力 | 右下城市栏 |
|---|---|---|---|---|
| 01:41:23 | 5.500000 | 1.296875 | 10.000000 | 科技5.5、文化1.2、生产力10 |
| 01:41:36 | 7.500000 | 1.296875 | 11.000000 | 科技7.5、文化1.2、生产力11 |

科技增加2、生产力增加1，前后均与城市栏一致；文化保持1.296875，城市栏截断为1.2，差值0.096875符合既定小于0.1的显示精度边界，不是错误。两张都是第1回合，同回合重新读取已更新。具体市民点击过程不在图中，操作依用户人工通过回报，不把截图当成全部操作日志。

通过：当前科研城Gameplay GetYield的S/C/P数值读取、与城市UI对照、变化后的重新读取。文化getter有效且稳定，本批没有主动改变文化；不扩大到所有城市/Mod/倍率情境、重载专测、精确纯本地basis、汇聚20%发放或防循环。当前探针明确READ ONLY / NO Lv4 activation / NO yields granted。

原件已移动至[Evidence/B028](../Evidence/B028/)，文件名与前后SHA256见manifest.json，无需补测。运行、SQL、Design及Tests未修改，无新增本地模拟。下一步商业IV收益承载/精度与反馈研究；旧可读性/断路测试仍延后。
