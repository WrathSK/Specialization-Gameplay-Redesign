# B121 — 自动项目正常周期通过；城市旗帜工期显示未覆盖

2026-09-28，逐张查看3张原图；标题B121.148。用户反馈“其他一切正常”，指出地图城市上方长条仍显示超长工期。USER_GAME_TEST_PASS仅用于本次正常周期，不扩大到注入、取消、零产能、保存续算或其它城市。

## 图示与证据边界

| 图／时间 | 可见结果 |
|---|---|
| 20:17:53，T21 | Edinburgh (TEST)，生产面板当前溢出承接实验显示1回合／计时已开启；地图城市旗帜、悬浮Tooltip显示119,180回合，底部城市面板也显示119180回合 |
| 20:18:26，T22 | 城131073，启动T21，结束回合确认“是”，调用1次，项目已退出；城市需选择生产 |
| 20:18:58，T22 | 同城纪念碑进度0，实验项目保留进度0，队列1；右侧0/50，普通目标工期6回合 |

自动完成、专用项目退出、随后普通目标初始为0：截图限定PASS。后续正常增长依用户“其他一切正常”的陈述接受，未收到T23截图，不伪称直接见到该回合数值。生产面板当前栏1T实测通过；未把列表中当时未显示的实验行单独记为实测PASS。

PT011正常周期门禁关闭，无需重复整套自动完成流程。城市旗帜及底部CityPanel显示残留属于已声明的UI_PROTOTYPE_BOUNDARY，尚未通过；不是项目自动完成失败。正常chop/harvest隔离、跨session、多城、正式奖励保持未测/未实施边界。

## 定位与下一最小建议（未实施）

本机Expansion2 `UI/CityBanners/CityBannerManager.lua` 的 `CityBanner:UpdateProduction` 在项目分支独立读取GetTurnsLeft，并写productionInstance.TurnsLeft及Button Tooltip；Base `UI/Panels/CityPanel.lua` 的ProductionNum/ProductionLabel使用自己的CurrentTurnsLeft。B121只包装ProductionPanel，两个独立context没有经过该包装，因此依真实百万Cost计算出高工期。STATIC_CONFIRMED是代码证据，不代表候选显示适配已实机证明。

建议下一段仅显示修补：城市旗帜数字/Tooltip和底部城市面板，只针对精确实验项目读取现有计时缓存；普通目标不变，不改原生GetTurnsLeft、成本、生产结算或计时writer。沿实际HD/原版替换链做薄适配；启动/暂停/完成时事件刷新，不hover请求或每帧扫描。按W0004 L1进行定向UI检查，一次截图确认即可，不重测已通过的整个机制。需单独实施授权；本轮只归档/定位，无runtime或部署变化。

## 原图归档

3/3原图移动前后SHA256一致，未改图；外部目录：

`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B121_Automatic_Project_20260928`

| 文件 | SHA256 |
|---|---|
| Screenshot 2026-09-28 at 8.17.53 PM.png | `82c2957de08054ddd1466e2c8f6cbb08f7e0bd56ce18c47d44f79df931755bc6` |
| Screenshot 2026-09-28 at 8.18.26 PM.png | `cd3761148b5b4c109084e6f2f2742cc87b3adb3b2df316cddf045015b97725aa` |
| Screenshot 2026-09-28 at 8.18.58 PM.png | `54703dd866e029e648f8e93941d5077db1c1738a294133837f81a05a427a5bb8` |
