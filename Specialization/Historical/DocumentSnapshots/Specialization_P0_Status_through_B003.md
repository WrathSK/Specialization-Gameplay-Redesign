> HISTORICAL / SUPERSEDED — 审计快照，不作为当前规则。

# B002 商路 UI 用户验收与 B003 显示调整（最新）

## 已确认结果

USER_GAME_TEST_PASS：用户本轮明确确认 Read routes (UI) 能读取三条现有商路，保存并重新加载后仍可读取；随后全国加入第四条，其中同一城市分别前往两个目的城市，Next district / route 可以分别读取两条路线。三条后的截图是 UI OBSERVATION，不再与此前 Route events (Game) 事件测试混淆。

截图（ScreenshotInbox，按时间）11.40.47 / 11.40.51 / 11.40.55 PM：Stirling (Test) → Aberdeen (Test)、Edinburgh (Test) → Stirling (Test)、Aberdeen (Test) → Edinburgh (Test)，各城 rawCount=1。读档与第四条同城分页以用户文字反馈为证据；未要求额外截图。第四条新增后的再次读档没有单独回报，不扩大证据范围。

rawCount 表示所选城市出发路线数，不是全国路线总数，也不是网络 recipient N。此前 Gameplay 新路线事件捕获的 USER_GAME_TEST_PASS 保留；其临时事件历史读档清空与 UI 当前路线枚举是两个不同问题。

## B003 本地修改

STATIC_CONFIRMED：仅调整 Probe.lua 商路显示与版本标记（modinfo version=10，UUID 不变）。先显示本城出发条数、当前页、出发/到达城市名称；原始玩家/城市/商人 ID 和检查字段保留在下方排错区。无法解析的端点明确显示未知。沿用 UI city:GetTrade():GetOutgoingRoutes()，不改变分页、Gameplay 事件、SQL 或网络算法。修正旧代码注释中“trade runs in Gameplay”的过期描述。

LOCAL_SIMULATION_PASS：test_specialization_p0.py，包含 Lua 编译/XML、UI 路线方向、分页、空列表、未知端点、缺失接口、禁止递归引擎对象及不派发 Gameplay 的既有检查。B003 中文排版尚未实机确认，标为 USER_GAME_TEST_REQUIRED；不要求为纯显示修改重复已通过的基础测试，下次正常重新加载脚本时查看即可。

BLOCKED：正式 Gameplay 权威网络全量恢复尚无完成方案。UI 快照通过不等于 Gameplay 能直接调用该 getter，也不允许以打开面板作为网络运行前提。终止/掠夺/易主等有效性撤销、稳定身份和初始重建仍待后续独立设计；不能把持久化事件历史直接当作当前路线集合。

当前无需继续重复商路起终点/同城分页/三条场景读档测试。不启动游戏，不等待用户测试。原生区域复制口径 NativeDistrictCopyBasis、sqrt(N) 与其它既定设计不变。


---
以下为历史记录，当前结论以上文为准。

# B002结果更正：通过的是Gameplay事件捕获，不是UI枚举

用户已明确纠正之前反馈所指按钮是Route events (Game)。撤销先前误记的Read routes (UI)端点/多路线USER_GAME_TEST_PASS，恢复USER_GAME_TEST_REQUIRED。游戏原生贸易路线界面及时刷新不等于我们按钮的getter已经验证。

四张截图按时间：
- 23:28:50：city=131073，turn=1 actor=0 FROM 0:131073 TO 0:65536。
- 23:28:59：city=65536，同一事件可在另一端查看。
- 23:30:42：city=65536，新增FROM 0:65536 TO 0:196610，并保留前一条事件。
- 23:34:52：读档后city=65536，NO_MATCHING_EVENT_OBSERVED；用户说明过回合仍无记录。

USER_GAME_TEST_PASS：Gameplay TradeRouteActivityChanged在本次新建路线操作中提供方向与城市/玩家端点，单条及第二条事件均被捕获，并可按涉及城市筛选。截图extra为空，不能推断更多状态字段或Trader ID。

STATIC_CONFIRMED：Gameplay.lua初始化shared.TradeEvents={}；历史只在ExposedMembers临时表中，没有SetProperty持久化、也没有读取现有路线重建。读档会清空这份诊断历史。本次观察与实现一致，不是保存文件把真实商路丢掉，也不能从无事件推出无商路。跨回合没有新事件不构成getter失效。

BLOCKED：完整Gameplay当前有效网络的读档恢复仍缺可靠方案。将事件历史简单持久化只能保留“过去观察过”，不能证明路线仍有效；必须解决终止/掠夺/商人删除/城市易主/重复线路/稳定身份，以及已有存档未观察路线初始化。不能用历史记录直接计算recipient N。该限制不是新的版本回归，B002原本明确NOT an active-route list。

当前只补一个此前未执行的读取测试：在已经读档、原生贸易界面仍有路线的现有存档中，选实际出发城市，点击我们面板里的Read routes (UI)（上排中间），必要时Next district / route浏览。这个按钮即时枚举，不依赖之前是否收到事件；无需新建路线或过回合。应显示UI OBSERVATION / mode=TRADE / FROM / TO；若城有两条出站则两条均可翻阅。注意一座城的一条入站加一条出站不是两条Outgoing。截图即可。若无出站则选另一真正出发城。

该测试即使通过也只证明UI快照路径；正式Gameplay权威网络恢复另设计，不将打开面板作为游戏机制生效条件。当前不修改代码、不要求再重复Route events的新建测试，也不再要求尝试等待回合恢复历史。

NativeDistrictCopyBasis最新设计保持；其它已用户通过项目保持。此次更正已同步Status、Findings、Architecture。


以下是历史记录，先前“UI商路通过”属于已纠正的误记：

# B002用户结果：UI商路端点与多路线显示通过

用户明确回报：可以看到商路从哪个城市到哪个城市；之后增加一条路线，两条路线都能显示出发/目的城市。登记USER_GAME_TEST_PASS，范围为B002 Read routes (UI)的端点读取与新增路线后多条列表显示。没有要求用户上传截图，没有读取图片。

用户未明确说明Route events (Game)是否捕获到新增路线，因此该Gameplay事件子项仍USER_GAME_TEST_REQUIRED。不从“新增路线后可显示”推断事件回调已执行，也不从UI枚举成功推断Gameplay权威网络恢复完成。完整有效性（终止/掠夺/易主）、存读档重建、重复目的城市去重仍保留待验；不要求重测已确认的起终点显示。

已有通过项：独立测试文明；marker存读档；新局原生总督存在/建立、升级阈值及原城调离阈值撤销；区域类型/完成状态/专家人数；UI基础相邻及政策后相邻API区分；本次UI商路端点与多路线显示。Actual业务定义仍以煤电厂/大酒店NativeDistrictCopyBasis为准，旧getter的通过不代表该复制算法已验收。

本轮只更新结果与状态，无运行代码/SQL变化，不启动游戏。后续可先核对新建路线对应的Gameplay事件观察结果，再安排权威网络恢复或原生复制基数的独立验证，避免重复UI测试。


以下为历史记录：

# Actual收益口径修订：以煤电厂/大酒店原生复制为准

用户明确授权采用该行为口径。已更新Architecture相应正文与Research IV/Industry IV公式：Actual内部改称NativeDistrictCopyBasis，保留50%比例、原有区域排除、转换目标和网络关系；Base能力不变。未擅自扩大到所有城市产出，也不要求先建原建筑。

STATIC_CONFIRMED：Building_YieldDistrictCopies只有BuildingType/OldYieldType/NewYieldType；煤电厂PRODUCTION→PRODUCTION，大酒店CULTURE→CULTURE。没有比例、显式跨城目标等字段，完整适配需要继续验证，不能直接填Amount=50。

USER_GAME_TEST_REQUIRED：原生复制对行业固定产出、cross-yield和百分比的实际基数边界，以及50%/多区/跨城适配。既有UI相邻getter测试PASS只证明其已测行为，不等于满足新确认的原生复制语义。

本轮只修改Architecture、Status、B002 Findings的当前约定；不改运行Lua/SQL，不增加同时测试任务。用户继续B002商路测试，无需因本修订重启。没有启动游戏，没有声称原生复制或后续专业能力已实现。


以下为历史记录，收益口径以本条为准：

# 当前B002：UI相邻通过，Gameplay商路getter失败后拆分观察路径

USER_GAME_TEST_PASS：基础/实际相邻及翻倍政策在已测UI场景正确区分。固定行业区域产出未包含不视为相邻读取失败；真正cross-yield adjacency仍USER_GAME_TEST_REQUIRED。USER_GAME_TEST_FAIL：B001 Gameplay city:GetTrade:ABSENT。B002新增UI现有路线观察与Gameplay活动事件原始采样，均待用户测试。完整Gameplay网络恢复仍BLOCKED（活动事件不能替代读档全量状态），不把UI数据当权威。当前步骤与建筑源码核对见Specialization_P0_B002_Findings.md。已有Governor/Specialist通过项不重测。

# 当前P0-B-001：两项独立读取待实测

A007用户通过的总督存在/建立/晋升阈值/原城调离撤销与区域/专家读取保留，不重复。当前用户步骤以Specialization_P0_Batch_B001.md为准，只有相邻政策对照和原始商路端点两项。

STATIC_CONFIRMED：和而不同UI/Replacement/RealModifierAnalysis.lua:994–998区分district:GetAdjacencyYield(yield)与Plot:GetAdjacencyYield(owner,city,districtType,yield)；这是UI源码先例，B001相邻明确只在UI采样。Gameplay/Temp_Interface.lua:306起使用city:GetTrade():GetOutgoingRoutes()和OriginCityPlayer/DestinationCityPlayer。代码先例不代替实机语义。

B001改动：Probe.lua新增NetworkProbe，独立区域枚举、按yield读取基础/实际候选，逐路线只提取端点和TraderUnitID；UI/P0Panel.lua/xml新增Read adjacency (UI)、Read routes (Game)、Next，相邻本地显示不派Gameplay动作；Gameplay.lua只增加TRADE只读请求；modinfo版本8、UUID不变。SQL未修改，已验证的Governor/Specialists分支未改变。备份DevelopmentBackups/SpecializationP0-P0-A-007/。

LOCAL_SIMULATION_PASS：test_specialization_p0.py（新增UI相邻不派发Gameplay、8/8→8/16、跨yield0/5、UNKNOWN不替0、空区域、空路线→国内/国际路线、方向/分页/清空、缺失getter、禁止递归route对象、只读零写入）；test_specialization_identity.py；test_specialization_network.py，均通过。mock政策数值与跨yield由fixture显式改变，不模拟引擎Modifier。

USER_GAME_TEST_REQUIRED：UI候选Base/Actual与具体政策语义；Gameplay原始出站端点。相邻Gameplay API、完整cross-yield支持、商路结束/掠夺有效性和网络去重仍留后续；运行包没有实现网络或Boost。当前rawCount绝不是N；sqrt设计不变。Trade endpoint UNRESOLVED保持未知，不能建立合法网络关系。

本轮文件：上述5个运行文件、DevelopmentTests/test_specialization_p0.py、本Status、Architecture、Batch_B001；无游戏启动/操作，无存档修改。本地完成后停止，等待用户两项结果。


以下为历史记录：

# 当前用户验证结论：总督阈值升级及调离撤销已通过

## 用户确认补录：头衔阈值与迁走撤销

用户明确说明此前已验证：Established title thresholds 2/3/4随总督升级正确显示1或nil；总督移走后显示0/0/0。不要求截图，不读取图片。

USER_GAME_TEST_PASS：本城头衔阈值随升级响应；总督移走后本城三项阈值全部撤销为0。nil与0都可作为未激活原始表现；仅值1视为本探针已激活，不把Lua truthiness用于判定（Lua中0为真）。不再安排同样的升级/原城阈值撤销测试。

合并已有结果：新局control加载、无总督、派遣后present、未建立/已建立的established，以及区域/专家读取均已用户确认通过。P0总督基础条件验证可作为下一阶段依据。当前未实现正式专业Active计算或网络效果；不将这些探针通过外推成整个v0.1通过。此消息未另外提供目的城市迁移途中Req门槛表现、旧存档新增Modifier回填或多人验证，保留这些边界，不阻止后续独立P0工作。

本轮仅更新状态与实现约定，无代码改动，无图片读取，无游戏操作。


以下为历史记录，重复测试已取消：

# A007新局用户结果：存在与建立条件通过

用户明确回报：新存档control=1、其他=nil；通过cheat panel获取一个总督头衔并派遣后present正确显示，established=nil；建立后established=1。

USER_GAME_TEST_PASS（限定子项）：新局无条件control加载、无总督初始值、派遣后存在条件、未建立时established未激活、建立后established激活。未要求截图才能记录，用户明确测试回报即为证据。获取头衔通过cheat panel，未据此推定任意免费晋升的计数语义。

旧存档control缺失而同版本新局正常，支持新增trait效果未回填旧存档的解释。记录为旧存档增量兼容问题，不归因原生总督条件失效；未经存档内部实例分析，不声称完全查明引擎装载原因。后续总督测试以这个A007新局存档为准，保留旧存档，不实现强制Attach或伪造control。

仍为USER_GAME_TEST_REQUIRED：在新局中核对1→2头衔门槛、迁移后的原城撤销及目标城建立前阻断、Req4；完整城市专业Active机制尚未实现。此前旧局Req2/3随升级响应证据保留，不外推全部语义。区域与专家读取通过状态保持。

下一小批仅两项，已有条件就做，不必再新建：
1. 当前已建立且仅任命的总督，Read governor记录control/present/established和Req2/3/4；给同一总督一个普通晋升后重新Read。预期control/present/established保持1，Req2从nil/0到1，Req3/4不激活。前后各截图。若作弊工具直接添加晋升而非仅提供可用头衔，请注明；优先用正常晋升按钮。
2. 若已有第二座己方城市，将该总督迁过去：读取原城，present/established/Req2/3/4应撤销为nil/0；读取目标城，到任途中present=1、established及Req2/3/4未激活；建立后established=1、Req2=1。两个城市control始终1。缺少第二城则暂不做，不为此重开局。

PASS按各子项记录；有错误或数值不符则截图并停止该项。截图仍使用ScreenshotInbox默认文件名。不需要重测存在/建立的基础过程或专家。本轮只更新文档，不修改运行代码/SQL、不启动游戏。


以下为历史记录：

> 用户已明确确认：本次加载A007之前的旧存档。新增效果未回填仍是待验证解释，下一项仅需A007临时新局control对照。

# A007最新用户证据：部分阈值响应，新增效果校验失败

同城升级后Req2/Req3从nil→1，有限响应子项USER_GAME_TEST_PASS；不等于完整建立/迁移/隔离验证。control/present/established五张图均nil：control加载校验USER_GAME_TEST_FAIL，存在/建立语义尚无法判定。缓存6个定义/绑定均在（STATIC_CONFIRMED），是否旧存档未实例化新增效果待确认。当前不发新包、不改运行代码。分析与单变量后续步骤见Specialization_P0_A007_Result_Analysis.md。印加全国/逐总督升级账本不能直接替代本城驻扎且建立的判定。

# 当前：A007 原生Governor Requirement桥接

A006玩家管理器GetAssignedGovernor:ABSENT由用户截图确认USER_GAME_TEST_FAIL；停止该Lua查询路线。A007改为原生存在/建立/2、3、4头衔条件→城市Property→只读面板。新增无条件control加载校验；缺失不能解释为无总督。STATIC_CONFIRMED：四个先例及原生参数已检查；LOCAL_SIMULATION_PASS：SQL/绑定/属性只读模型；USER_GAME_TEST_REQUIRED：实际条件激活、撤销与既有存档加载。当前步骤只看Specialization_P0_A007_Native_Governor.md。专家读取USER_GAME_TEST_PASS保留，不重测。其他最新设计与scope不变。

# 当前：P0-A-006 Governor lookup修订

- USER_GAME_TEST_PASS：用户明确确认A005专业区域存在与否、区域类型、完成状态、专家读取及数量正确。范围限已测试场景，不外推全部Mod区域或产出机制；不要求重测。
- USER_GAME_TEST_FAIL：A005总督读取，截图显示At: BEFORE_GetAssignedGovernor / GetAssignedGovernor:ABSENT，城市对象接口不可用。
- STATIC_CONFIRMED：A006改为player:GetGovernors():GetAssignedGovernor(city)，参数形式参考官方Expansion1/UI/Additions/GovernorAssignmentChooser.lua:90；官方先例是UI，不证明Gameplay可用。Specialist函数分支未修改。
- LOCAL_SIMULATION_PASS：现有test_specialization_p0.py通过；fixture删除city.GetAssignedGovernor，验证玩家管理器收到准确city对象，覆盖无总督、有总督、未建立/建立、晋升，以及管理器方法缺失明确报错，未静默解释成无总督。
- USER_GAME_TEST_REQUIRED：A006玩家管理器查询及后续Governor字段。若此接口也缺失，下一步应隔离为UI只读Governor信息＋Gameplay原生Req2/3/4属性核对；不将UI数值当作Gameplay权威，不盲猜API参数。

当前唯一复测：用户手动重启加载原存档，确认P0-A-006，选有总督城市点Read governor一次，把自动结果截图放ScreenshotInbox。不需要过回合、重新Mark或重测专家；仍有ERROR就暂停总督状态变化测试。总督头衔/建立条件整项未验收。

本轮修改：Mod的Probe.lua（仅FocusProbe的Governor查询）、UI/P0Panel.xml与modinfo版本；DevelopmentTests/test_specialization_p0.py；本Status、Architecture、Specialization_P0_A006_Governor_Fix.md。备份DevelopmentBackups/SpecializationP0-P0-A-005/。未改SQL、Specialist、网络sqrt设计或存档。未启动游戏。

以下为历史记录：

# 当前：P0-A-005 读取错误修订

A004 Specialist枚举为USER_GAME_TEST_FAIL（用户截图Probe.lua:340）。Governor尚无返回画面，保持USER_GAME_TEST_REQUIRED；结果展示流程已修订。当前仅执行Specialization_P0_A005_Reading_Fix.md的两次读取，暂停旧A004变化测试。A005本地模拟通过、实机USER_GAME_TEST_REQUIRED。A1/A2通过与sqrt设计均保留。

# Specialization P0-A-004 — 独立 Governor / Specialist 验证

用户回报：“A1成功，没有问题，但是A2，建立首都后，点击Mark selectd City，游戏目前卡住”。未收到 Lua 调用栈；根因尚未确认。未启动、操作、等待或结束游戏进程，未修改存档。

## 当前状态

| 项目 | 状态 | 证据 / 下一步 |
|---|---|---|
| A1 独立文明选择与开局 | USER_GAME_TEST_PASS | 用户明确回报A1成功；范围限A1，不外推到存读档或机制 |
| A2 / P0-A-002 Mark | USER_GAME_TEST_FAIL | 用户报告建立首都后点击即卡住；尚不能确认停在UI采样、请求派发或Property写入 |
| A2-R / P0-A-003 轻量读取、写入与存读档 | USER_GAME_TEST_PASS | 用户回报ACK city=65536 marker=P0-A-003:1:1，并明确确认重新加载且未再Mark，读值不变 |
| A003系统剪贴板交付 | USER_GAME_TEST_FAIL | 用户无法粘贴；不影响屏幕ACK和持久化通过。提示已改为delivery UNVERIFIED，并尝试print导出；尚未确认剪贴板修复 |
| A3 Governor / A4 Specialist | USER_GAME_TEST_REQUIRED | A004独立只读探针已完成本地验证，按Batch_A004执行 |
| Adjacency / Trade / 后续机制 | USER_GAME_TEST_REQUIRED | 保留依赖顺序，暂不安排用户执行 |

## STATIC_CONFIRMED

- 旧Mark在请求派发前调用完整UI Snapshot和Summary；Gameplay收到后又完整Snapshot。涉及区域、商路、巨作、建造队列和数据库遍历。
- 旧Encode会递归展开任意table，未限制深度/节点/输出量，可能展开引擎包装对象。以上是已确认的风险路径，不是冻结根因的实机证明。
- A003按钮仅派发选城ID、Action、Token；Gameplay只查城市归属和SPC_P0_MARKER，一个首次SetProperty；不再采集全量快照、枚举区域、监听自动采样事件或写首次专业标记。
- Scalar仅输出nil/boolean/number和最多512字符的string，其他对象不遍历、不调用其__tostring。阶段记录最多32条。尚未返回ACK也可复制诊断，旧快照不冒充当前结果。
- 完整Snapshot/Summary/Encode暂保留为未接线的研究代码，不能通过本版按钮或回合事件调用；恢复分模块采样前需单独修订和验证。
- 文明、领袖、SQL、图标/配色定义未改；原生Governor调试Property modifiers仍在，本轮不验证其行为。Mod UUID保持，版本升3。
- 本地找到当前Modding/Database/GameCore日志，未找到Lua.log；它们不能定位本次按钮卡住的位置。日志已备份。

## LOCAL_SIMULATION_PASS

已运行：

```text
PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/test_specialization_p0.py
python3 DevelopmentTests/test_specialization_identity.py
```

覆盖：Lua/XML/manifest；将Snapshot、Summary、Rows、区域/总督/商路/队列接口设为抛错陷阱，验证轻量UI→请求→Gameplay路径不会调用它们；只读零写入、首次仅一次写入、重复Mark不覆盖、保留mock属性重载、写入失败不返回成功ACK、pending诊断复制、请求匹配、非测试文明拒绝；危险table不会被Scalar展开。

数据库测试在只读缓存的内存副本中先清除测试命名空间的fixture行，再重放SQL，解决用户已加载Mod后重复插入的问题。未改用户实际缓存。其他记录保留、无新增外键错误、Scotland资源引用对照通过。Make_Hash仍是stub；SQLite成功不能替代引擎验证。历史的纯数据/全快照小fixture仍测试，但不代表已解决旧全量采样风险。

## 文件变化

- Mod：Gameplay.lua、UI/P0Panel.lua、UI/P0Panel.xml、Probe.lua、SpecializationP0.modinfo。
- 测试：DevelopmentTests/test_specialization_p0.py、test_specialization_identity.py。
- 文档：本文件、Specialization_P0_Batch_A.md、Specialization_v0.1_Architecture.md。
- 备份：DevelopmentBackups/SpecializationP0-P0-A-002/；旧Status和Batch_A的_P0-A-002.md；P0-A-002-freeze-logs/。

当前唯一需用户执行的步骤见Specialization_P0_Batch_A004.md。A2旧版卡住失败记录保留；A003 marker通过范围限本次用户测试局、城市及普通存读档，不外推到城市易主、多人同步等行为。

## 用户回报后的本地修订

确认marker测试通过，当前无需重跑A2。P0Panel仅修正剪贴板提示并print小型导出，保留A003版本号，未改变Gameplay/SQL；下一次正常启动时加载，不要求为提示修订专门重启。新增mock验证剪贴板false/nil返回均不宣称交付成功且仍显示ACK。日志文件是否实际落盘仍未确认；屏幕截图是当前可用的回传方式。Property与隐藏建筑比较见Specialization_P0_Marker_Storage.md。

## A004 当前增量（优先于上方A003历史实现描述）

STATIC_CONFIRMED：新增Read governor / Read specialists，两者仅按按钮读取Gameplay选中城市，不写Property，不连接完整Snapshot/Summary。Governor仅遍历GovernorPromotionSets（上限256行），重复promotion去重，多个BaseAbility仍只对应一次任命；显示assigned/established/base/extra/owned/titleCandidate及原生Req2/3/4属性。Specialists仅遍历本城区域（上限32个、最多显示6个专业区域），读取专业区域地块worker count及完成状态，缺失API/定义或超限返回ERROR，不能算零值/完整成功。对象不序列化，不读商路/相邻/巨作/生产队列。ACK仅是一次请求完成，不是实机语义通过。

官方本机源码先例：Expansion1/UI/Additions/GovernorDetailsPanel.lua:192使用HasPromotion(kPromotion.Hash)；CityPanelCulture.lua:202/210使用GetAssignedGovernor/IsEstablished；Base/Assets/UI/CitySupport.lua:743读取区域地块GetWorkerCount。这些主要是UI上下文先例，Gameplay是否同样完整仍需实测。

LOCAL_SIMULATION_PASS：两条原有测试命令均通过。新增无总督、多个BaseAbility、重复晋升行去重、额外晋升、established=false保真、Req2原样显示、缺失API不ACK、专家0→1→0、显示超限不ACK、只读零写入、UI按钮到Gameplay联通。mock中的Req2由fixture显式赋值，不模拟引擎Modifier刷新；未验证真实专家槽、总督回合延迟或UI最终渲染。

新增/修改文件：Probe.lua（FocusProbe）、Gameplay.lua（按Action分派）、UI/P0Panel.lua/xml（独立按钮、Show / Copy直接显示多行）、SpecializationP0.modinfo（版本4，UUID不变）、DevelopmentTests/test_specialization_p0.py、本状态/Architecture/Batch_A004文档。A003包备份在DevelopmentBackups/SpecializationP0-P0-A-003/。SQL/身份/现有marker未变；未启动游戏。

A1与A2的USER_GAME_TEST_PASS保留。当前Governor/Specialist都是USER_GAME_TEST_REQUIRED；剪贴板交付旧失败保留，本批用截图，不依赖复制。专业选择、potential/active实际机制未实现，面板不伪造对应等级。完成本地工作后停止等用户结果。

## Research/Culture sqrt平衡修订（2026-09-10，当前设计）

- STATIC_CONFIRMED：已搜索当前SpecializationP0、DevelopmentTests与P0报告。旧线性Boost没有进入运行代码或原有模拟；存在于architecture路线示例、多中心求和、Commerce IV和P3验收假设，已全部替换。历史DevelopmentBackups仅保留审计，不作source of truth。
- LOCAL_SIMULATION_PASS：新DevelopmentTests/NetworkStrength.lua + test_specialization_network.py验证k×ACTIVE L×sqrt(N)、接收城市去重、独立k_R/k_C、N=0/8/16、边际递减、撤销和输入检查；缓存真实schema的内存副本能保存小数甚至sqrt文本，后者也说明SQL存储成功不能证明引擎计算。
- USER_GAME_TEST_REQUIRED：Boost Amount小数解析、动态开关/精度/撤销、触发时序；尚未建立相应游戏探针，此轮不安排测试，不选择取整规则，不退回线性。
- BLOCKED：正式多源不同ACTIVE level的全局Boost合并，需明确选源/合并语义；禁止延续旧逐中心求和。单源数学与接收集合prototype不受此影响。
- A004运行包及现有Governor/Specialist测试不变；无新增安装文件，无需因本次文档/模拟修订重启游戏。P0后续Network计划改为去重接收及小数测试；P1的状态层预留接收集合、独立系数、浮点强度，效果适配单独验证。
- Spaceport仅记录future auxiliary，当前v0.1 scope没有增加。Architecture末节和Network_Sqrt报告可定位；Entertainment未来仅调整效率参数。

本次文件：Specialization_v0.1_Architecture.md、Specialization_P0_Status.md、新Specialization_P0_Network_Sqrt.md、新DevelopmentTests/NetworkStrength.lua、新DevelopmentTests/test_specialization_network.py；修订前报告备份DevelopmentBackups/Network_sqrt_pre_revision/。测试命令：PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/test_specialization_network.py。未启动或操作Civ6；等待用户A004测试结果。
