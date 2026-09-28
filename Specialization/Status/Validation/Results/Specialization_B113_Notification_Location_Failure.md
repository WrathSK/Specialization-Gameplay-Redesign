# B113 — 单城生产通知位置核对失败

2026-09-27，B113.140 / modinfo140。已实际查看用户投递的19:30:37截图。**USER_GAME_TEST_FAIL：仅A空队列时未显示下一回合。** 不要求重复当前流程，不用Shift+Enter绕过。

可见：Edinburgh (Test)，回合21；生产阻塞1、其它空城0、其它阻塞无；单位/城市攻击/政策提醒均false；通知对应测试城=false；扫描次数1。右下角仍是选择生产项目。两个新按钮标题正常，标题修复在本图范围内USER_GAME_TEST_PASS。

对照当前源码：唯一生产通知经FindEndTurnBlocking读取，GetLocation返回值与测试城x/y比较，结果为false，足以使filter失败并保留原按钮。未出现类型未知/owner错误/已dismiss异常。截图未展示实际坐标、通知ID/type或其它operable子条件，不能断言唯一根因是坐标格式，也不能宣称其余未展示门禁全部通过。采样仅1，亦未验证后续事件刷新行为。

分类：NATIVE_NOTIFICATION_LOCATION_BOUNDARY。已定位阻止放行的一项检查，不是完整根因修复。当前不能把GetLocation必然对应城市地块作为已验证事实；本地fixture匹配坐标并未证明引擎合同。下一调查应核对通知实际位置/属性、城市位置、通知ID及原版选择城市路径，取得依据后调整归属合同；不单纯删除检查或用空队列数量冒充完整城市归属证据。

没有真实强制结束、固定一回合、生产占用、保存恢复或收益验收。B112原生观测范围内PASS保留。本次只归档/更新状态，不改runtime、不部署。修复与下一包待授权。

## 原始证据

文件：`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B113_Notification_Location_Failure_20260927/Screenshot 2026-09-27 at 7.30.37 PM.png`。原图已读，移动前后SHA256一致：`0b91fc1c8d59a03333fbe7b99eed0aba7e795699438435e4b22509e79f250c3e`。
