# P05a/P08b — 当前加载、精确effect归属与退出闭包

独立审计 IA20261007 / W20；基线 `06a7300010baae8dc8bfe2ffc7097af83497ec16`。项目本体只读。机械声明闭合不等于游戏执行、每个native收益/载体退出或全项目PASS。

## 结论与范围

modinfo实际只有一个Gameplay root、15个独立UI roots、4个原生context replacement。185个注册文件均存在、无重复Files；literal include候选图120个文件，8个registered Lua不在该图，40个唯一注册SQL，其中35个UpdateDatabase文件。脚本只做源码结构清单；分支、失败和外部HD/游戏loader不是该图能证明的事实。

固定1720项building声明均有精确owned退出归属（包括历史/备用/退休定义），未发现缺定义、非InternalOnly或固定family误撞。三种动态family仍须实际loaded目录判定，数量UNKNOWN。plot flags、Claim markers、永久业务记录和一次性native副作用分别处理，不用“所有BUILDING_SPC前缀”替代ownership。

新增 **IA-P08b-F01 LOW / DEFER**：巨作启迪开发Probe失城后精确4ID可撤，但会话清理使用不存在的loss.targetID；actual Lua3场景核本字段差异。局部原型控制state可能锁住，load cleanup可恢复；不是永久账本/载体泄漏，无native事故或新增用户测试。

暂定 **IA-P05a-Q01 LOW / MONITOR**：少数UI自加匿名hook/证据factory无显式Remove/Close；engine context销毁是否自动释放尚未证明。不据源码缺Remove判native泄漏/重复执行，也不因此重构全部UI。

## 注册与真实作用map

[modinfo](../../../Mod/SpecializationP0.modinfo)声明是可载入入口，不等于每个Start成功。[Gameplay](../../../Mod/Gameplay.lua)655–822是显式组合；前置未保护异常可能中断后续，只有Claim include/Start有独立pcall。当前没有观察到该启动事故，不创造新的HIGH理论问题。

| Gameplay组 | 当前作用与限制 |
|---|---|
| Store→Binding/CompletionRecord/Journal/Flow→EffectiveFacts | Store生产保存先行；旧名adapter/validator有当前职责，不能只按名字删除 |
| Catalog/CurrentFacts/InfrastructureShadow | 纯model/reader；DC Start建立当前事实服务，无Start不等于未使用 |
| Investment、support/Lv2、Network、Industry、UnitActions/Crew | 正常已登记实现；部分仍是旧适配，不由Start证明新Design完成 |
| Lv3Support/Lv4 Culture/GWA | Lv3Support公开Start是retirement facade；GWA Start retired=true，正向guard/控制拒绝；保留精确历史清理，不能复活旧收益 |
| Research当前、K/Aesthetic/Meaning | 正常自动writer；K→Aesthetic→旧Dialogue→retiredGWA→Meaning顺序真实，callback风险沿P09编号 |
| Copy/StdDiscount/Boost/Convergence/COM Lv3/旧Dialogue | 旧业务仍运行，P02/P03/P04各自已核target切换；不按旧名字报未加载，也不按当前source恢复旧Design |
| Claim | 正常计时/认领，保护启动；失败记录startupError、不改用历史实验作为权威 |
| Inspiration | 已Start默认OFF、NEXT才有target；load/turn精确cleanup，不是正式六class能力 |
| Half/Purchase/GreatWork等Probe | Half存档opt-in可在load自动重算；Purchase load清OFF；GW首次Run/BOOST_INIT才Clean，ready后transfer也清。不能统一称“Probe只手动、无自动副作用” |
| TimedProduction/Overflow/ProjectTurnObservation/TimedProject | 请求才建立实验状态；不构成新Dialogue/Study完成账本 |
| Performance | New counters＋StartMemory默认enabled的单协调GC运行缓解，按现行guard/预算；不是零side-effect纯诊断。本slice不改或重审已核GC算法 |

## E1/旧adapter不是第二套正式身份权威

[CityIdentityMapping](../../../Mod/CityIdentityMapping.lua)实际Start并设置shared.CityIdentityExperiment别名；GP请求97–101调用该Mapping而非旧Experiment.Start。它会为既有单城E1记录保存HELD/一次映射，属于独立技术实验，不是纯只读；Store不读取Mapping V2/Experiment V1 key或Shadow结果作为正式identity authority。

旧Experiment.Start未调用，但纯Shadow被Mapping验证/评估使用；CityIdentityRead.Copy/Preview被Store生产校验采用；FreshBindingHook经Flow.Install安装且BlocksLegacy阻止现代写，Binding/Flow是现代Store adapter。保留这些有独立职责的helper不是不必要双authority。

literal图外8个Lua：CityInheritanceRead/InheritanceShadow/CityInheritance（GP788–792明确隔离）、CultureMeaningProbe（未Start且与normal互斥）、DistrictPrecisionProbe/Read（历史实验未在Gameplay启动）、UI/GreatWorkBasis（无当前具名调用）、UI/CityBannerManager_SPC_TimedProject。最后一项有[原生wildcard线索](../Technical/Specialization_Project_Action_Interception_and_Full_Turn.md)，外部当前loader未重读，不能仅据缺AddUI判未执行。前七项也不由图证明其所有动态外部引用不存在。

## UI与诊断边界

| UI root职责 | 实际门控与owner |
|---|---|
| BackgroundRoutes | route dirty/epoch/ACK、有界重试，干净generic pulse不扫描 |
| GPPRefresh | 只发dirty原因，不发送专家数/facts；ready/version/local Owner/3次限制 |
| Industry/Copy/Cross Refresh | BASE采样由dirty/generation/turn/output revision驱动；SetUpdate只超时钟，Copy另有隔离门控 |
| DiscountEligibility | permission/turn/revision/generation缓存，3次发送限制；不是hover无条件CanStartCommand |
| DialogueRefresh | K/旧Dialogue producer，dirty与有限pending；GWA retired的adjacency事件不新工作 |
| BoostRefresh | 初始化补偿3次/回合，两模块ready后停止 |
| CityPotential / Institutions | 前者0.5s选中城检查、selection/turn/output dirty才请求；后者消费overview无Gameplay轮询 |
| UnitPanelActions / UnitTargetMarkers | 0.2/0.25s selection检查，dirty/token才请求；动作点击确认，marker完成/timeout不time-only重发 |
| P0Panel / UnitSites | 按需诊断/DEV会话，generic pulse推进现有pending，不建立新采集；关闭无pending时返回 |
| RuntimeAudit | Load/LocalPlayerTurnEnd observer，读counter并有界日志sink，不请求Gameplay/derive；8×4MiB、标量摘要，失败锁停 |

15个XML→同名Lua是当前注册结构；重复include仅定义功能不等于多次Start。普通计算没有在本slice发现新GameEffects全枚举hot path；Inspiration/Meaning reader只在具体请求且token/ref/turn缓存。UI事件失效/生产scope风险复用P09/P13，不机械去掉pulse、fallback、foreign退出或same-turn输入。

4个replacement真实Properties为LuaContext/LuaReplace：CityPanel→TimedProjectCityPanel→DL_CityPanel；ActionPanel→TimedTurnProbe→HD_ActionPanel；CityPanelOverview→InstitutionOverview→DL_CityPanelOverview（必要fallback Expansion2）；ProductionPanel→CrewProjectOrder→DL_ProductionPanel。各包装保留base正常行为，TimedTurn仅armed时读取blocker/强制结束原语。外部最终override赢家、context teardown与ready/LoadScreenClose全部时序未证；已有具名原生使用证据按原范围继承，不扩任意Mod组合PASS。

## 固定owned／声明矩阵

| 固定family（含历史/退休） | 唯一IDs |
|---|---:|
| ResearchSupport / Lv2Housing / Lv2GPP | 3 / 9 / 32 |
| Lv3Support退休 / Lv3Effects / Lv4 Culture退休 | 12 / 11 / 8 |
| IndustrySupport / CrewProjects | 9 / 1 |
| ResearchInfrastructure含退休 / Cross含退休与DP | 52 / 43 |
| Apply / Tradition / Copy / Half | 25 / 5 / 40 / 32 |
| Boost旧＋integer＋test | 1032＋90＋4=1126 |
| Dialogue tests / GreatWorkProbe / PurchaseProbe | 3 / 2 / 2 |
| GWA退休 / Meaning / Aesthetic / InspireProbe | 156 / 92 / 1 / 4 |
| Claim markers / Convergence | 4 / 48 |
| **固定并集** | **1720** |

[固定名单脚本](Evidence/W20/fixed_owned_inventory.py)／[原始结果](Evidence/W20/fixed_owned_inventory_result.json)／[schema与排除边界](Evidence/W20/fixed_owned_inventory_metadata.json)：父任务重跑相同静态清单与原JSON一致。只执行Types/Buildings的literal VALUES，SQLite内存schema没有native默认值/约束，仅按列名建表，非其它SQL/动态SELECT执行。35个数据库SQL literal Types1739、Buildings1720；固定owned并集1720，KIND_BUILDING/InternalOnly=1，缺项/重复Type/重复BuildingType/固定families碰撞/未归属literal Building均0。它包括注册但不正向创建的定义，不是1720正在生效或1720曾逐项native退出。

动态Chair=8×实际Buildings∩13 targets；Discount=4×enabled HD target；Dialogue=D2..nativeEraCount（3test已固定计入）。源码生成与对应exit同公式，但未取实际loadedDB，具体目录/数量/执行仍UNKNOWN。当前Meaning与未启动备用Probe共用92是同合同的互斥实现，不算双写；DP3由Cross43退休列表定域退出，GW2由GreatWorkProbe拥有且Dialogue load附带清理。其他被调查旧ID仍保留Types/cleanup，不借审计移除。

Aesthetic还有16plot flags＋OWNER；YieldCarrier两个plot flags控制六TraitModifier，撤flags不是漏建筑出口。Claim4是访问markers。TimedProject/TimedProduction没有奖励载体，OverflowSink是项目；unit grant/AddProgress/Gold等一次性副作用与永久receipts分属P07/未来合同，不能纳入“carrier清理成功”宣称。

## IA-P08b-F01 — Probe已撤载体但遗留会话

证据STATIC＋actual未改Probe最小Lua；**LOW / DEFER，下一次L3 Probe/退出接口维护前定域修补**。Store602 loss为origin/target/evidence；Probe146比较loss.targetID（不存在）。145先RemoveOwned4成功，Store529将回调finished；不能通过重试该成功callback解决会话。现有test_culture_inspiration_probe46造targetID，因而不能覆盖真实payload差异。

| 受控actual Probe | immediate退出 | 原Owner Audit / END / 另城NEXT | load cleanup |
|---|---|---|---|
| 真实Store字段形状 | carrier0、stage仍1、普通哨兵保留 | lost ID已不在原Owner集合→CITY_UNKNOWN；target未忘、END与新城被阻挡 | stage−1，另城可新启0 |
| 历史test造targetID对照 | carrier0、stage−1 | 无旧target阻挡 | 正常 |
| 未确认target对照 | carrier0.1、stage1、移除0 | 未派confirmed退出 | 显式load只清自身 |

[脚本](Evidence/W20/reproduce_probe_loss.py)／[原始JSON](Evidence/W20/probe_loss_result.json)：真实Probe，facts/native/Store RemoveOwned受控stub、不是full Store integration/native事件观察；3场景、无永久写/外部DB/修改正式tests。成功load以及同旧ID出现不同reference/明确inactive的可读原引用都有现行自清路径，所以不是永久锁死/无界历史、也不影响普通自动Meaning或正式GPP（尚未实现）。native可达未观察，不要求用户重测失城。

候选修复边界：使用真实callback合同及可靠的session→persistent-record归属，不能猜城市名/仅cityID或清其它城市session。另按真实loss形状测foreign引用与recapture ID变化；不把修正field名简单设target.city==loss.origin.cityID视为已覆盖复归后变ID。P08a-Q02的真实Store×consumer fixture限制补证，未来新writer应继承payload合同，不复制同一错误。整个审计没有修复。

## IA-P05a-Q01 — UI teardown边界暂定

CrewProjectOrder58–64、TimedProjectCityPanel16–18和若干扩展自加callback没有显式Remove；CityIdentityEvidence.New29–31注册3匿名hooks，P0Panel shutdown没有它的Close。当前factory一次初始化、未watch时立即return、事件最多8；多数background roots明确跟踪Remove，构成强反证。native context释放语义/重复创建频率未知，**LOW / MONITOR**，只有新增context rebuild或可重复多调用/旧context保留才定域调查。不据它要求新user save/load仪式。

## Evidence与余界

[静态清单脚本](Evidence/W20/registration_inventory.py)／[结果](Evidence/W20/registration_inventory_result.json)保存action/Include/Start/出口位置，不是调用trace；以Git source commit＋modinfo/script hash定位，没有新长期源码hash台账。原始数组不作为强制日常context。actual Probe复现采用已有Lua5.5；默认Python缺Lupa、旧README临时路径失效，复用现存临时依赖，无安装/正式配置修改；跨机器按测试README准备依赖，不声称默认Python已配置。

三路读scope：Gameplay root/Start及guards/adapters；15XML/同名Lua include/init/event/pulse/shutdown和4replacement关键链；所有实际writer exact生成/创建/退出段、Store492–534/588–632、35SQL机械Types/Buildings读取。前序逐专业/P06/P07/P08/P09/P13复用；机械读取不是逐行业务算法重新审阅。未读全部nativeEffect逻辑/HD实际catalog/游戏loader、未证明原生context释放或全模块同session行为，不运行全suite/stress/游戏或部署。

下一P15/P12b：活动技术导航与冻结/弃用材料的有效性、重要反证可达、旧派工误授权及测试/证据继承收尾。沿Authority/CURRENT→准确计划/来源/旧限制映射核，不读取全Historical、不修导航、不让局部native未知阻塞整个项目；随后才P16/P17跨finding返工优先级与最终覆盖合成。
