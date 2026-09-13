> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# P0-B-001：相邻候选与商路端点（两项）

USER_GAME_TEST_REQUIRED。运行包B001；新建A007并已验证control/总督/专家的存档继续使用。此版没有SQL增量，不需要新局。用户手动重启一次加载新Lua，确认面板P0-B-001。不要重测已通过的Governor/Specialists。

## 界面与证据

选中己方测试文明城市：
- Read adjacency (UI)：同步读取UI侧单个专业区域；自动显示UI OBSERVATION。每行是BASE_CANDIDATE / ACTUAL_CANDIDATE。目前两个名字仅是待实测的API语义假设。
- Read routes (Game)：Gameplay侧读取所选城市Outgoing列表；自动返回ACK。该列表不被本版认定为正式有效网络。
- Next district / route：浏览当前城市的下一专业区域/路线；末项后回首项。重新点Read从首项开始。区域顺序按ID排序，路线按API返回顺序；如果状态改变请以显示的district ID/Trader ID和端点识别对象，不依赖页码不变。

城市ID、区域类型/ID、路线双方ID/名字自动显示。默认名截图直接放ScreenshotInbox即可，不需要复制。UNKNOWN表示缺失/非数值，绝不是零；NO_SPECIALTY_DISTRICT/NO_OUTGOING_ROUTES表示前置不足，不代表完整语义通过。

## B1 — Base / Actual政策对照

前置：测试文明的一座城市，有已完成且基础相邻非零的Campus或Industrial Zone（也可选已有明确相邻翻倍政策对应区域），并可切换一个明确只增加该区域相邻百分比的政策。不要使用只有建筑产出加成的政策。可以用现有Cheat Panel获取必要解锁，但测试取样之间只能改变那张政策，不同时增加建筑、地形、人口或晋升。

1. 在尚未插入该相邻加成政策时选城，Read adjacency (UI)，Next找到目标区域。截图B1-before，需能看到该行类型/ID、complete=true以及目标yield两列值。额外截一张政策说明即可，无需抄ID。
2. 插入政策，保持同一城市、区域和其它状态，重新Read并翻至同一区域，截图B1-after。例：没有其它相邻百分比时，+100%政策使 `YIELD_SCIENCE: 3 / 3` 变成 `3 / 6`。第一列应保持基础3，第二列应随政策改变。
3. 如果能方便撤下，再撤下重读验证恢复（不要求为了撤卡专门等待多回合）。若相邻加成已来自其他政策/文明机制，回传其说明与前后数值，由开发者核对，不让用户自行推算。

PASS：已知单变量相邻政策改变第二列，第一列保持基础值，具体数值与效果一致。FAIL：UNKNOWN、READ FAILED、第一列被相邻百分比放大、第二列完全不随政策变化或数值无法解释。若没有适用政策或非零相邻，先回报前置不足，不要求新局。

这个PASS仅确认当前组合/该yield的UI候选语义。Gameplay对同样接口的可用性仍USER_GAME_TEST_REQUIRED；跨yield、替代区域、建筑相邻复制、掠夺和复杂Modifier不自动算通过。本批不采集城市总产出，也不把UI结果写入Gameplay。

## B2 — 一条商路的有向端点

前置：有一条正在运行的商路最好直接用它。优先选测试文明两座己方城市之间的商路；没有现成路线但有商人时可建立一条，不要求再开局。选真正出发城市，不是商人当前经过的城市。

1. 原版/Mod商路界面确认路线城市A→B，截图其起终点。
2. 选A，Read routes (Game)，有多条则Next找到目标。截图B2-origin。应FROM为A、TO为B，owner/city字段对应，originMatchesSelection=true。双方己方时sameOwnerRaw=true；现成国际路线则false。UNRESOLVED表示端点解析未完成，回传，不能默认为合法接收城市。
3. 选B再Read routes。A→B不应因B是目的地而出现在B的Outgoing中；B有其它出发路线可以正常显示。截图B2-destination。不要求为了此项终止长期商路。

PASS：起终点、方向、玩家归属与实际路线一致；目的地Outgoing没有把入站路线反算为出站。空表只能通过“当前无出站路线”子项，不能通过存在路线的端点检测。FAIL：端点颠倒/错误、UNKNOWN/UNRESOLVED、originMatchesSelection=false、缺失getter/READ FAILED；停止该项并回传截图。

仅检测原始端点，不实现Trade Center身份、network set、合法distribution筛选或N。rawCount不是Network N，不能参与Boost计算。未来会根据确认过的有效关系构建按城市UID去重的recipient set，再使用k×ACTIVE L×sqrt(N)。

## 异常与后续

卡住不反复点击；能响应时保留错误文字和最后阶段。没有结果超过10秒只说明请求未返回，可点Show看迟到结果，不要靠不停过回合猜测。图中版本与城市字段需保留。

跨yield相邻另批：等B1结果后，根据用户存档已经拥有的转换效果，单独对照转换前后各yield；没有证据不能宣称API完整包含大型Mod交叉yield。断路/撤销/重复路线城市去重也在端点先通过后安排。本轮只有B1和B2。
