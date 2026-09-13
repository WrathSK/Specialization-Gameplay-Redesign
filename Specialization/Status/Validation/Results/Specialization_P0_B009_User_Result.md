# B009用户实机结果：B9-1通过

## USER_GAME_TEST_PASS

用户人工核对PASS，助手按时间检查ScreenshotInbox两图：

| 项目 | 2.18.40 PM（前） | 2.18.56 PM（后） |
|---|---|---|
| 版本 | P0-B-009 | P0-B-009 |
| 原始集合 | COMPLETE_UI_SHADOW，3条 | COMPLETE_UI_SHADOW，4条 |
| 标准缓存 | READY_UI_SHADOW，rev=1，count=3 | READY_UI_SHADOW，rev=2，count=4 |
| 刷新次数/seq | 3 | 4 |
| 最近变化 | +3/-0（初始化基线） | +1/-0 |
| 触发 | LoadScreenClose | GAMEPLAY_DIRTY_SIGNAL |
| 采样入口 | LoadScreenClose | GameCoreEventPublishComplete |
| Gameplay对照 | MATCH | PENDING（未就绪/已变旧） |
| turn | 1 | 1 |

原三条均保留：Aberdeen→Edinburgh [327684]、Edinburgh→Stirling [393221]、Aberdeen→Stirling [458758]。
新增Stirling→Edinburgh [524295]，方向正确，无重复或旧路线丢失。

发布完成次数1101→1889，播放完成1→2；系统通知/Context更新均0；本批尝试均1/3。高频通知只对应本次一次新增采样，标准缓存revision也只增加1。

确认B009标准模块实机装载、基线输出与本次新增路线后的count/revision更新，后台新增路径USER_GAME_TEST_PASS。PENDING不扩大为新样本Gameplay匹配通过，不妨碍本项UI shadow通过。

## 验收边界

UI来源仍为UI_SHADOW_ONLY。复制读取防污染、错误隔离和reset等未由两图单独实机验证，保留LOCAL_SIMULATION_PASS。新增标准模块自己的删城/读档全生命周期不由旧版本证据自动覆盖；旧B007初始化/读档与B008删城各自PASS继续有效，不要求重复本批。

原商人删除、自然结束、取消、掠夺、战争、正常征服/夷平仍未确认；纯Gameplay权威全集provider与永久城市UID仍BLOCKED/待设计。本轮仅更新记录，不修改代码、不升级版本、不接收益。
