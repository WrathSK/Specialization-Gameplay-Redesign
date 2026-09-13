# B008用户实机结果：B6-3-CITY通过

## USER_GAME_TEST_PASS

证据：ScreenshotInbox/Screenshot 2026-09-11 at 2.03.43 PM.png，用户按删除城市变体回报。

- 运行P0-B-008；COMPLETE_UI_SHADOW，turn=1，seq=4。
- 首次自动完成INITIALIZE / 3条；当前1条；最近变化+0/-2。
- 已移除示例Aberdeen (Test) → Edinburgh (Test)，商人327684。
- 唯一剩余Aberdeen (Test) → Stirling (Test)，商人458758。
- 触发GAMEPLAY_DIRTY_SIGNAL；采样入口GameCoreEventPublishComplete。
- 刷新次数4；发布完成1088；播放完成3；本批尝试1/3。
- 系统通知0；Context更新0。
- Gameplay对照PENDING，因样本未就绪/已变旧，不登记对照MATCH。

与B007三路线基线比较，两条涉及Edinburgh的路线消失，Aberdeen→Stirling保留。因此本次被删除端点应为Edinburgh（由路线差分推断，用户未单独报告城市名）。先前B008测试说明对Aberdeen的推测不正确；不据此判本测试失败，当前剩余路线符合删除Edinburgh的结果。

确认范围：本次Cheat Panel删除城市后，后台UI当前全集由3条重建为1条，撤销两条相关路线并保留其它路线。发布完成事件实际触发并完成重建，不依赖已观察为0的两个更新回调。播放完成计数非零仅证明事件送达，不单独证明它的重试恢复分支。大量发布通知对应总共4次采样，与只在dirty时扫描的实现一致。

## 尚未确认

原商人删除案例未执行；自然结束、取消、掠夺、战争、正常征服/夷平仍USER_GAME_TEST_REQUIRED。跨边界失败后重试仅LOCAL_SIMULATION_PASS，本次最后一次尝试1/3不能验证重试分支。纯Gameplay权威全集provider仍BLOCKED；UI影子读取未接入正式收益，也没有自动改为正式权威来源。

## 当前工作

B007初始化/读档和B008删城重建三项现已有各自的用户PASS。无需重复本批。运行代码与版本未改；本轮仅记录证据并同步Architecture/Status。
