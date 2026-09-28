# B116 — 空目标修复通过，生产机会成本仍未证实

2026-09-27，B116.143 / modinfo143；三张原图已实际查看并归档。**USER_GAME_TEST_PASS限NONE开始识别、空队列诊断、观察跨玩家回合结束；固定完整生产回合/生产力隔离不判PASS。**

## 逐图事实

- 21:17:27：城131073，开始回合21，ACTIVE。事件1条：21 BEGIN 目标=NONE。按钮门禁可请求，UI队列0、无目标，右下角下一回合。B115开始断言失败已在本场景解决，纪念碑假读数消失。
- 21:17:49：游戏回合22，ENDED。3条记录为21 BEGIN NONE → 21 PlayerTurnDeactivated NONE → 22 PlayerTurnStarted NONE。队列仍0，右下角选择生产。报告明确完整生产结算未证实。
- 21:18:05：仍为回合22，观察仍ENDED且3条历史事件不变。队列1，当前目标进度“粮仓=8”。非空目标读取成功；截图证明此时已有8点，不单独证明它从0增长或具体来源。

## 证据限制与下一判断

原型在首次本玩家新回合Started/Activated回调将观察标ENDED，后续事件不再采集。因此“3条中没有CityProductionUpdated”只能描述此采集窗口，不能推断城市从未结算、引擎不发该事件或回调必然位于生产结算之后。下一技术调查须区分观察提前关闭与空队列事件缺失，不可将本次turn+1升级为完整生产回合证据。

粮仓=8引入PRODUCTION_OPPORTUNITY_COST_UNRESOLVED：原始三图单独不足归因；结合用户面板确认后，粮仓既存进度和期间收获/砍树/Cheat输入已排除。城市级旧溢出与空队列该回合正常产能随后兑现仍需区分。用户随后明确纠正：选择粮仓前已查看生产面板，没有已有进度（若有会显示），不是记忆不确定；选择后才出现8点。期间没有收获、砍树或Cheat输入。此为用户直接观察确认，不伪称起始面板出现在已投递截图中。粮仓旧投入已排除，不再作为待核实项。尚未确定的是城市级既有溢出、空队列正常产能的存储和应用时机；城市显示的生产力不能直接作8点来源证明。原型没有AddProgress/FinishProgress/生产写入。

下一建议先查清8点来源及采集终止顺序，再决定是否需要最小对照；不直接进入收获实验、不清空生产、不给生产力退款或扣除。选择Q发生在观察结束之后，不是活动观察中断的验收；中断实机仍未覆盖。完整保存恢复、低/零生产、收获/溢出以及正式项目仍未验证。

本次仅证据/状态更新，无runtime、Design或部署改变。B114限定PASS保留。

## 原图及SHA256

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Production_Baseline_20260927/Screenshot 2026-09-27 at 9.17.27 PM.png`
  - `17977a754527ff8319285ddd20e48dacfbe4291b1fe21b14203c837eafa23627`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Production_Baseline_20260927/Screenshot 2026-09-27 at 9.17.49 PM.png`
  - `8e83d8026c50c72c9a90a043c8fbc48eefd2343bc61e8401f69d9caab4e9ffc3`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B116_Production_Baseline_20260927/Screenshot 2026-09-27 at 9.18.05 PM.png`
  - `88ed565de9e3ee0ae3ab73b8da13c9368284a7ee04f63f1371aaf71d81280997`

3/3移动前后hash一致，未改图片内容。
