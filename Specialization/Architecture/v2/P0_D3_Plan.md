# P0-D3 — Research IV「学术主持」具体计划

Status: IMPLEMENTATION_COMPLETE_AWAITING_USER。用户已授权实施；B086.113静态/本地完成，见[实施合同](P0_D3_Research_Chair.md)。下方未授权措辞为原计划历史，不派发下一批。
Authority: Design D0035 / Research D0031 RES_L4_CHAIR / Shared D0035 ordinary/current eligibility / A0161。
Baseline: B085.112/modinfo112，实现f149f8434a48419b11f618fe4cff857c274e2d8d，部署记录5021309。用户接受P0-D2；W0001旧上下文/140个Mod文件hash匹配复用。

## 1. 唯一规则与例子

Current Identity=Research，Potential4且ACTIVE4。W=本城正在工作的科研专家数。每座合格普通学院T1–4建筑b：
`ChairScience[b] = W`
`ExpectedCityBaseScience = W × eligibleBuildingCount`

两座合格建筑、3名专家：图书馆+3、大学+3，总基础科技+6。不是给每名专家再加6，不是把6平铺城市。原生最终城市科技可能另受城市倍率，不混淆基础增量与最终值。

逐栋计入：同Tier多座、缺低Tier直接存在高Tier均按实际普通建筑；不是Tier存在性，也不是ΣTier/D/cap10。T4与T1每座同样+W。免费获得不改变ordinary身份；特色替代归一仅用于资格，实际效果要落实到当前存在的具体BuildingType。完成且未掠夺；Palace/Wonder/Institution/internal/补偿载体/未完成对象排除。区域完成/未掠夺及当前引用按既有Shared事实合同；未知Tier/位置不是合法0。

用户已明确正常环境只有一个学院，社区才允许重复；不要求用户测试多学院。若异常环境出现多个学院，显式报告支持边界，不悄悄把最高D选择扩大为本能力规则。

D仅提供共享建筑事实入口，**本能力不消费D数值**。主持新增Science不得回写D、BASE adjacency或形成自身反馈。基础3F3P、Lv2、科研基础设施(P0-C)、跨学科研究(D1)、学以致用(D2)独立保留；D1/D2临时floor不外推到D3。W本身为整数，本能力无新增小数门禁。

## 2. 实施顺序与技术门禁

1. **锁定事实与recipient清单。** 复用CurrentSpecializationFacts、DistrictCompleteness的未丢失逐建筑记录及OrdinaryBuildingCatalog；复核Campus实际catalog/HD Tier/替代。Data Center已在B2目录，不把旧缺口清单当新事实。只补确有证据、此能力所需的最小Campus缺项；不展开全领域目录重构。
2. **验证真正的逐建筑基础Science路径。** 当前只读DebugGameplay存在EFFECT_ADJUST_BUILDING_YIELD_CHANGE：MODIFIER_BUILDING_YIELD_CHANGE及MODIFIER_SINGLE_CITY_ADJUST_BUILDING_YIELD的COLLECTION_OWNER定义；实际宗教建筑先例参数BuildingType/YieldType/Amount。这里只是STATIC_CONFIRMED（定义及用例存在），不是当前carrier owner语义或实机PASS。实施时追溯attachment与owner、single-city限定、特色替代、掠夺暂停及撤销、原生显示/结算。按实际BuildingType投影并用有界内部carrier或已证实可撤销modifier承载W为候选，不能把全球Building_YieldChanges改写当城市独立效果。
3. **门禁后唯一writer。** 纯计划→完整确认→差异投影；先读完整再写，避免部分未知先clear。若静态/本地不足以确定native归属，允许在已授权D3内部先出最小隔离primitive，单独标PROBE并清理；不能把probe称为完成。没有可靠建筑收益路径时停下报告，不默默换成城市平铺、区域固定或专家补偿。
4. **诊断、前序保护与发布。** 本地覆盖后commit/push；实际部署依W0003独立执行退出/备份/hash事务。当前本轮只是计划，W0003不触发部署。

不预定bit数、专家人数cap或Building范围。实现需证明有限编码覆盖当前合法专家范围；超出接口能力应诊断而不是发明Gameplay上限或截断W。native归属门禁是技术问题，不是新Design决定。

## 3. 预计改动与旧writer边界

- `ResearchChairModel.lua`（暂名）：每座合格建筑的基础Science计划，不创建新shared公式。
- `ResearchChair.lua`（暂名）：唯一writer、资格/worker/recipient与配置比较、撤销、按需说明。
- `Data/ResearchChair.sql`（路径/形式待primitive证实）：内部投影定义，收益必须属于合格普通建筑；载体隐藏且不进入ordinary/D/Lv2统计。
- `Gameplay.lua`：启动、已有显式progression刷新、只读诊断dispatch；panel复用已有位置，不新增高频桥。
- 仅必要shared事实/目录增量，若改动必须跑P0-A/B/C/D1/D2回归。

当前Mod中没有RES_L4_CHAIR或ResearchChair独立writer；不得因为旧文件名Research就整模块退休。ResearchIII人口8及ResearchIV旧复制/百分比48已经退出，持续断言不会复活。本批默认无新旧能力退休；若实施发现同语义旧effect，先登记精确ID/调用链再处理。P0-C、D1/D2及其它专业不变。

## 4. 有效性与调度

- 输入：当前专业引用/Identity/Potential/ACTIVE，学院可用性，逐座ordinary BuildingType/完成/掠夺/Tier资格，工作科研专家数。Network、其它城市产出、UI hover不是输入。
- UNKNOWN/未就绪保留上次verified配置并说明；确认worker0、ACTIVE不足、失去Research、建筑移除/掠夺则撤销对应贡献一次。建筑修复恢复，重复通知无重复发放。
- load用当前事实复核原生已保存投影，不新增永久成果或自增账本；当前引用变化不能沿用旧recipient列表。城市移除/易主沿既有CurrentReference隔离，不设计新的永久ownership政策。
- 直接建筑/区域/资格/worker变化驱动；新回合一次有界reconciliation；复用当前共享D快照，不因每栋query重新capture全城。保护内部carrier Building事件过滤，避免自触发。
- generic Publish/Playback、单位移动、UI timer不触发完整扫描。无hover Gameplay request，无periodic sampling、逐事件文件写或无限history。
- 受影响单位优先城市/玩家；无法精确城市定域时明确有限范围，不声称尚未实现的完美增量。

## 5. 诊断易读性

左键只列：资格、工作专家W、合格建筑数B、每栋+W、合计基础Science W×B、配置/待确认状态。例：`工作科研专家3｜合格学院建筑2｜每栋+3科技｜合计预期+6`。
右键列本城相关建筑：中文名、归一Tier、计入/排除原因、每栋配置/预期；不堆bit/Modifier ID。期望、配置、原生读数明确分开；若原生单建筑读取接口不可用，标UNKNOWN，不把数学结果伪装成读数。

## 6. 本地验证与退出条件

| 验证 | 必须证明 |
|---|---|
| 公式 | W0/1/2/3/合法较高值；B0/1/2/3/4及同Tier多栋；每栋同为W，不按Tier加权，不被Dcap10截断 |
| 资格 | ACTIVE0–4/非Research；免费、特色、未完成、掠夺修复、内部/Wonder/未知、区域失效 |
| 作用域 | 两城市相同BuildingType但不同W不串城；其它专业不变；目标收益为building base Science |
| 生命周期 | 相同输入零写；UNKNOWN保持；真撤销一次；新增/删除单建筑、worker改变、load/current reference、旧投影清理不重复 |
| 互不反馈 | 本能力不改变D；P0-C与D1/D2输出保持；旧8+48不复活；同Tier多栋与cap10反例明确 |
| 性能 | 1/2/4/8城报告facts/captures/recipient checks/writes；10k无关通知及UI timer0请求/0扫描/0写；回合fallback有界 |
| 静态/集成 | SQL owner/recipient/无全局污染、实际writer/完整正常场景无隐藏错误、Lua/manifest、前序回归、部署安全 |

LOCAL_SIMULATION_PASS不能替代native建筑归属/叠加验收。若需要用户测试，只在候选路径已尽量本地验证后，用同一城流程涵盖：ACTIVE IV＋两座合格学院建筑，0→1→2专家；检查每栋增量和合计，增加一座普通建筑、降ACTIVE/恢复与存读档（能合并即合并）。无需人为制造掠夺；特色和大多数排除边界本地覆盖。条件允许保留另一普通学院城作不串城对照，避免额外建测试世界。

完成定义：唯一writer/真正building归属、无旧效果叠加、静态及本地回归通过、相关文档/版本/manifest一致、coherent commit/push；实机未测则只标IMPLEMENTATION_COMPLETE_AWAITING_USER。回滚保留完整B085包＋切换前另存档，不保证新增carrier写入存档向后兼容。

## 7. 非范围与下一门禁

不包括：学术传统/下一批、其它专业、Research Network重设计、D1/D2公式/取整、全目录覆盖、Save migration、Institution正式化、UI polish、Design修改。

无新阻塞Design决定；逐建筑primitive是TECHNICAL_SPIKE_REQUIRED，不是已证实可用或失败。当前可授权D3，授权后先做其技术门禁；本轮停止等待单独实施授权。
