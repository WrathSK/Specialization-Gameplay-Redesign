# B116 — 手动/自动溢出模式实机对照

2026-09-27；B116.143 / modinfo143。四张原图均已实际查看。USER_GAME_TEST_CONFIRMED仅指以下所测模式与进度读数；未升级正式固定生产回合或生产力隔离为PASS。

## 逐图事实

1. 21:29:27：城131073，回合21开始，ACTIVE，BEGIN目标NONE，UI队列0。顶部M，城市生产力显示+8.3。
2. 21:29:47：回合22，ENDED；21 BEGIN NONE → 21 PlayerTurnDeactivated NONE → 22 PlayerTurnStarted NONE；队列0，顶部仍M。
3. 21:30:16：回合22，队列1，粮仓=0；顶部M，生产力+8.3。历史观察已ENDED，不是活动中断测试。
4. 21:31:17：顶部A；第二次观察开始回合22，23回合ENDED；22 BEGIN NONE → 22 PlayerTurnDeactivated NONE → 23 PlayerTurnStarted NONE；队列1，磨坊=8；右侧生产面板同样显示8/60，城市生产力+8.3。

用户补充步骤：图1–3按此前流程，但关闭自动溢出；粮仓0后使用Cheat完成粮仓，再开启自动溢出、开始新观察、过回合、选磨坊。Cheat完成及模式切换的过程不是连续截图，按用户陈述记录，不伪称捕捉到全部操作。

## 结论与范围

本次原生读数确认M段选择粮仓0、A段选择磨坊8；与上一轮A模式粮仓8和已读源码“CityProductionChanged→AddProgress(0)”相互支持。自动应用溢出参与即时目标进度变化具有充分依据，工作判断优先采用这条已定位路径，不要求重复相同A/M现象。

这不是同一存档/同一目标的严格单变量实验，也不是M模式下点击手动应用按钮的0→8实测。第二段包含Cheat完成粮仓，尚未审查其对城市生产存储的影响；不能仅凭8与显示8.3接近，就断言该引擎路径floor(8.3)或证明8点全部来自第二次空队列回合。第一轮无Cheat的A模式粮仓8证据仍成立，不被本轮Cheat步骤撤销。

对原型的直接含义：当前环境下，空队列跨回合后选择新目标仍可立即取得生产进度；“空队列足以保证该回合生产全部作废、后续目标不能兑现”的保证尚不能成立。关闭自动只是不立即应用，不能当作清除原生存储的证据。固定完整一回合方案的生产机会成本/额外生产隔离门禁保持未通过；按钮与NONE开始等此前限定PASS保持。

不修改或禁用第三方Mod，不把用户关自动设为本Mod使用前提，不擅自扣生产力，不修改Design。下一建议仅调查本项目如何可靠界定并隔离这一回合生产，以及现有原生生产存储/结算接口；需要代码原型时另行授权。当前无需重复同类实机测试。收获隔离、正式项目、Claim/F未推进。

## 原图与SHA256

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Overflow_Mode_20260927/Screenshot 2026-09-27 at 9.29.27 PM.png`
  - `bcdf1fd71495a9f4dd3b2099a69e56366886e0bdee8b50af4b70ab8821131d4b`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Overflow_Mode_20260927/Screenshot 2026-09-27 at 9.29.47 PM.png`
  - `391f6c83f5f4c5b40805861bba00193b9ef3e3be6c6f638a8a6cd388151f29c6`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Overflow_Mode_20260927/Screenshot 2026-09-27 at 9.30.16 PM.png`
  - `ee77203b5e6a14d0de1069c7ed37cb428b52c39d4660294ecd225a3e45a7150c`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Overflow_Mode_20260927/Screenshot 2026-09-27 at 9.31.17 PM.png`
  - `a1c7f4c1e317da1d0fc2ca7ec682adb75e3ca9fec464652e7db008632a09568d`

4/4移动前后SHA256一致；原图未修改，外部存储，不复制入Git。
