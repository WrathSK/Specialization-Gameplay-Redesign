# B008：事件批次结束后重建后台路线

> 本批已完成：B6-3-CITY USER_GAME_TEST_PASS，见[用户结果](Specialization_P0_B008_User_Result.md)。实际剩余Aberdeen→Stirling，符合删除Edinburgh的差分；下文推测删除Aberdeen仅为旧测试假设。无需重复本批。

## CURRENT AUTHORITATIVE STATE

运行P0-B-008 / modinfo15。仅UI_SHADOW_ONLY诊断，未接入正式RouteState、网络或收益。B007初始化/读档PASS保留；B6-3-CITY失效后未重建的失败保留，不扩大为所有撤销都失败。

## STATIC_CONFIRMED：本机原版先例

相对于Civ6.app/Contents/Assets：
- Base/Assets/UI/MinimapPanel.lua:983 OnFlushChanges检查dirty，1100注册GameCoreEventPublishComplete，原注释说明该事件在一组GameCore事件之后发出。
- Base/Assets/UI/Choosers/ResearchChooser.lua:398 FlushChanges、485注册同事件。原窗口带可见性判断；本后台诊断不复制可见性门控。
- Base/Assets/UI/InGame.lua:258、358使用GameCoreEventPlaybackComplete；它作为另一实际事件边界的候选，不据此推定所有商路数据一定已稳定。

B007实机三图中SystemUpdateUI/Context更新均0；不再只靠两者消费dirty。新注册publish-complete/playback-complete，先核对Gameplay dirty revision，再在dirty或待重试时全量读取当前Outgoing。城市/路线原始事件仅mark，不根据事件payload增删路线。

## 实现与限制

保持已经通过的初始化、LoadScreenClose及回合直接刷新。新增批次结束回调合并重复dirty；采样失败保留UNKNOWN，最多跨事件边界尝试3次（含首次），无同步循环、无限重试或睡眠。成功后干净边界不再采样；新的dirty/回合重新允许尝试。旧SystemUpdateUI和Context计时仍是可选路径，不能声称其实际可用。

面板新增发布完成次数、播放完成次数、本批尝试与采样入口。按钮仍只读取缓存。计数/端点/商人冲突校验保持原样；完整快照整体替换，lastGood只用于诊断差分。

若两个新事件也不触发，或者引擎在3次边界尝试后仍不一致，状态仍可能UNKNOWN，需用户截图定位；未宣称自动撤销已解决。Gameplay全集provider仍BLOCKED，不升级UI shadow为正式权威来源。

## LOCAL_SIMULATION_PASS

- test_background_routes.py：完全不调用SystemUpdateUI或Context更新，10个重复城市事件合并；publish阶段端点已消失但路线未清理→UNKNOWN；随后playback阶段源数据稳定→完整集合且仅相关路线移除；干净边界不重复扫描；持续计数异常最多3次、不恢复旧缓存；新信号允许恢复。既有去重/归属/错误/关闭/读档伪缓存覆盖用例继续通过。
- test_specialization_p0.py：Lua/XML/manifest、只读按钮与既有窄探针回归通过。
- test_trade_route_probe.py：既有Gameplay任务诊断回归通过。

测试均为本地mock/静态验证，不是游戏测试。未启动Civ6。

## USER_GAME_TEST_REQUIRED：单项B6-3-CITY重试

1. 手动加载上次删除城市之前的三路线测试存档。确认P0标题B008即可，不要求重新提交已通过的B6-1/B6-2截图。
2. 关闭P0窗口，使用相同Cheat Panel操作删除同一座城市。不要额外新增路线、过回合或打开贸易界面/Read routes (UI)。
3. 操作完成后打开P0 → Background routes，保存一张截图。

若沿用上次三路线状态并删除Aberdeen，预期删除两条Aberdeen出发路线，剩余Edinburgh → Stirling；但上次未直接提供删除城市名称，此名称为根据前后场景的推断。请优先复现同一城市；如果所删城市不同，在回传时说明名字，无需抄ID。

PASS：COMPLETE_UI_SHADOW、当前路线3→1、最近变化+0/-2，唯一剩余路线不连接已删城市。刷新次数增加，采样入口显示实际触发路径；Gameplay PENDING可单独保留，不要求强求MATCH。

FAIL/停止：UNKNOWN持续、数量/方向错误或旧路线仍出现。若首次UNKNOWN，约1秒后只再查看一次；保留两张状态截图。不用过回合补成功，不等待未证实的10秒定时器。截图须含发布/播放次数、本批尝试、采样入口与错误行。

如果没有删除前存档，请直接说明；不要为复现重建整局。不要求删除商人。通过也仅覆盖此次Cheat Panel删城，不包括正常征服/夷平或商人被掠夺。

## 文件

修改UI/BackgroundRoutes.lua、Probe.lua、UI/P0Panel.xml、SpecializationP0.modinfo、DevelopmentTests/test_background_routes.py；更新Architecture/Status；新增本报告。B007运行包备份DevelopmentBackups/SpecializationP0-P0-B-007。SQL未改。
