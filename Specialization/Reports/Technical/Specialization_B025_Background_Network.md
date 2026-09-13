# B025：后台当前路线桥接与Lv1网络诊断

Document Owner: Codex
Design Basis: D0008 / NET-001至004；G0006用户认可后台UI来源
Build: P0-B-025 / modinfo32

## 实现

保留既有BackgroundRoutes采样，不打开/自动操作任何窗口。NetworkSender从完整快照复制五个整数：origin player/city、destination player/city、trader ID，编码为有界字符串，通过现有UI.RequestPlayerOperation(EXECUTE_SCRIPT)传给Gameplay。接收早期独立分流，不污染普通面板请求ACK；不通过ExposedMembers调用Gameplay写函数。

初始限制128路线/16384字符，超过上限发送不可用状态，不截断伪造全集。包带epoch、seq、turn、游戏路线signal、count、完整/失效标志。Gameplay检查epoch与递增seq、当前回合/signal、字段、重复trader、端点owner/存在、实际路线数量，全部通过才替换。来源明确READY_BACKGROUND_UI，不改标GAMEPLAY_CURRENT。旧纯Gameplay-only离线模块保留历史契约，本次新增独立运行桥接，尚未统一其接口。

来源失效时撤掉可读当前集合；Gameplay信号/回合改变时读取立即UNKNOWN，等待新批次。序号防旧批覆盖，加载无永久Property，后台与Gameplay重新握手。用户未打开P0面板时已自动发送。跨上下文参数是否支持本批字符串大小、启动实际时序仍需实机；不以本地mock宣布通过。

网络派生：真实当前首都与DEV Commerce城为中心，B021有效Lv1 RESEARCH/CULTURE/INDUSTRY事实为source。S→H直接接入，首都自身source另自接入；H→D携带所有来源，按类型和接收城市去重，不递归。接收结果保存source依据集合；中心保存直接来源，routes保留原始支撑路线可重新推导。更详细center/source/route资格账本沿用离线模型，当前运行诊断未完成全部正式schema。接收包即派生；城市建造/区域完成/回合入口重算，Read也按当前角色核对，不触发路线采样。没有Network Strength、Boost或任何收益。

仅本地测试玩家、现有有效DEV Lv1记录；未跟踪旧城不虚构专业，但可当普通recipient。未部署通用资格、永久跨ownerUID、Potential升级或Commerce IV免费接收；现有DEV只产生Lv1，未来必须接ACTIVE适配，不能将Potential当ACTIVE。当前城市键是owner+cityID快照引用，不宣称永久UID。全体AI/多人未支持也未据此修改Design，后续实现事项。

## 本地结果

LOCAL_SIMULATION_PASS：test_network_bridge.py运行实际Sender/Bridge，完整替换、两种来源同路线分发、接收去重、撤销Culture保留Research、同数量换目的地、旧序号/部分包/重复商人、空集合与signal失效，以及无面板请求的自动传递。

test_background_network_sender.py复用既有后台采样全部测试，加载实际Sender；桥接未就绪时保持原采样，桥接就绪后实际后台collector自动提交完整空批次，无可见UI/按钮。Lua语法与XML/manifest路径检查通过。临时Python包入口缺失，测试直接使用现存lupa.lua55扩展，无下载依赖、未改游戏配置。

STATIC_CONFIRMED：manifest仍同UUID，新增模块为ImportFiles；既有Lv1源码/SQL不变。此次并未宣称全部旧测试脚本的冻结版本断言通过。

USER_GAME_TEST_REQUIRED：[一批三个案例](../../Status/Validation/Cases/B025_Background_Network.md)。可用现有B024存档，约4图，普通结束若不方便可使用明确标注删城变体，不能合并证据。B010继续延后。BTS数据可信不是当前争议，测试仅针对本Mod新增桥接/更新链路。

## 文件及下一步

新增NetworkBridge.lua、NetworkSender.lua；修改Gameplay.lua、UI/BackgroundRoutes.lua、UI/P0Panel.lua与xml、Probe.lua、modinfo。新增两个测试、本报告与B025案例。更新Architecture A0056、Status S0058、README及AGENTS版本引用。Design D0008/hash不变，运行B025/32，无新SQL、无收益写入、无游戏启动。备份DevelopmentBackups/Specialization-before-B025。

用户结果返回后先修复实际传递问题，再补当前支持范围内真正未验证的撤销行为、角色ACTIVE/来源账本接口；不先接Boost/折扣，不反复要求批准已接受的后台来源。
