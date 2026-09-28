# B114 — 通知目标与单次过回合实机验收

2026-09-27，B114.141 / modinfo141，源码a281590。**USER_GAME_TEST_PASS（仅所测单城按钮原型）**。两张原图已实际查看，移动前后SHA256一致；不要求重复测试。

## 截图可见事实

- 19:55:50：Edinburgh (Test)，回合21。生产阻塞1、其它空城0、通知匹配true；目标有效true，玩家0、对象131073、类型2（CITY=2）。其它阻塞无，单位/城攻击/政策提醒false；扫描1。城队列为空，右下角显示下一回合。
- 19:56:21：游戏已到回合22。诊断保留回合21的最后请求快照，扫描2，显示已发送一次测试结束请求，以及“测试关闭：回合/玩家改变；本次测试结束，未发放收益”。这是关闭后的历史快照，不是声称回合22仍在放行。右下角恢复选择生产项目，A仍无生产目标。

## 用户明确人工确认

用户确认PASS：过回合后测试关闭；处理其它待办后正确显示选择生产图标，点击打开A生产队列，不触发过回合。截图未包含实际点击过程，这部分证据来自用户陈述，不伪称图像展示了点击。

## 结论与边界

本场景确认原生有效CITY target能定位该测试城、仅A空队列时正常按钮可提交结束、回合变化关闭临时豁免、后续原生生产待办及点击行为恢复。B113坐标归属失败由B114目标路径在本场景解决；旧失败原件保留。

28项LOCAL_SIMULATION_PASS继续只覆盖本地测试断言；本次不扩大为所有阻塞/政策弹窗组合实机PASS，也不证明固定完整生产回合、砍树/溢出隔离、正式项目入口、奖励、保存恢复或Claim已实现。下一建议另拟最小生产占用/计时与生产力隔离验证计划，需授权；本次仅归档，不实施、不部署、不推进Claim/F。

## 原始证据清单

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B114_Target_Turn_Pass_20260927/Screenshot 2026-09-27 at 7.55.50 PM.png`
  - SHA256：`a86417a4cdbf991f5331a05516c8a9ecf27ccfcd633a0c32662cad21a2c35306`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B114_Target_Turn_Pass_20260927/Screenshot 2026-09-27 at 7.56.21 PM.png`
  - SHA256：`de47a8c2b35d50d866c89f56deee41dd9dd47361204eb23b06074d4a485d4f1e`
