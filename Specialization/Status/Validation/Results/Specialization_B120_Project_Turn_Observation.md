# B120 — 单城正常回合观察限定PASS

2026-09-28；实际查看一张19:14:24截图，标题P0-B-120.147。城131073，观察起始T21，终点T22；报告为“观察结束／只读观察结束；没有自动完成/发奖”。USER_GAME_TEST_PASS仅指本次事件采集窗口及读数，不是自动完成系统通过。

## 可见顺序

| 顺序 | 回合／通知 | UI缓存进度 |
|---|---|---:|
| 1 | T21 开启 | 7 |
| 2 | T21 玩家回合结束 | 7 |
| 3 | T22 Started | 7 |
| 4 | T22 StartComplete | 7 |
| 5 | T22 生产更新(66,0,66) | 15 |
| 6 | T22 Activated | 15 |
| 7 | T22 手动报告终点 | 15 |

全部行GP目标为承接项目、UI队列1、目标true，无UNKNOWN、超限或中断提示。生产更新参数按图原样保存，不把66解释为产量或某个已确认ID。差值8是UI进度变化，不推断城市精确生产力或隐藏overflow来源。

## 判断与范围

- 观察持续越过首个Started和StartComplete，覆盖生产更新、Activated及手动终点：本次采集门禁PASS，无需原样重复。
- StartComplete样本仍为7，随后生产更新样本为15。不能以事件名字认定所有生产读数已结算/发布；但UI缓存也不能证明底层Gameplay生产写入一定发生于StartComplete之后。这是事件/样本顺序证据，非跨context同步证明。
- Activated是本次观察中位于生产更新后的候选时点，至手动终点未出现进一步可见变化；不足以保证所有城市/Mod组合/零产能/延迟路径通用安全，也未试过在该回调内FinishProgress。
- 下一建议：据此收窄P-B120B自动完成与1T呈现方案，保留当前目标重查、一次调用和未知停止；在原生自动完成测试前不能宣称其可靠。不自动实施。
- B119手动原生完成限定PASS保持；B117盲扣FAIL、B118扣除INCONCLUSIVE保持。自动完成、显示1T、chop/harvest、取消/存读、正式奖励均未在本图测试。用户已接受强制同回合完成，不重新加入防提前完成奖励门禁。

## 原图归档

`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B120_Project_Turn_20260928/Screenshot 2026-09-28 at 7.14.24 PM.png`

SHA256：`7c2ff2550bda30c7edf46341168f43e1ba4c109cf527b5be1ed2b335833e5b1a`。

1/1原图移动前后hash一致；未改图。只更新证据与状态，无runtime/Design/部署/游戏启动。
