# P12a — 规模风险断言与测试 fixture 的真实性

Audit IA20261007 / W07；2026-10-07。审查baseline `700d1d2d717e58a1f7d2900fdd181ebb97b362bb`。**Audit-only**；只核本轮指定公共路径的测试边界，不是正式验证策略变更、全测试库审计或修复授权。

## 本slice结论

现有测试有真实且值得保留的范围：同回合更新、UNKNOWN后补撤销、批内失败不发布半成品、记录局部写入、查询不重新采集、某些独立模块的线性读数，都有直接断言。**问题不是测试太少，而是不能用这些指标代表未测的内部工作或多个模块合起来的成本。**

已有33城保存测试、1000城缓存上限测试和30,000次Network查询；它们分别回答记录隔离、缓存有界、查询不重新Capture，不能排除W03的每写全记录检查，不能证明超过8城的warm-cache复用，也不代表30,000次网络重建。重复数量和工作集形状是两个维度。

沿[前序ledger](Specialization_Independent_Audit_Ledger.md)、[W02缓存原结果](Evidence/W02/district_cache_result.json)、[W03保存原结果](Evidence/W03/progression_store_result.json)及[P06a报告](P06a_State_Ownership.md)，本轮补强既有 `IA-P06a-F01/F02`、`IA-P13a-F01/F02/F03` 的验证边界，不另报一组重复缺陷。没有新证据改变severity/refactor timing，也没有必要再跑同样的W02–W05复现或要求用户长测。所选文档明确区分historical/local/native，**未发现它们承诺这些未测结论**；不因未跑large stress而制造finding。

## 风险 → 当前断言 → 未覆盖范围

路径默认相对于仓库根，行号对应baseline；本轮静态阅读测试，**未重新执行下表套件**。表中“覆盖”指实际代码中的断言与fixture，不是本轮新增PASS。

| 风险与测试 | 真正执行的实现、工作集和断言 | 不足以证明／与既有finding的关系 |
|---|---|---|
| 公共事件作用域；`DevelopmentTests/test_b138_update_contract.py:69–110` | 真实`RuntimeWork.Hook/Player`；player4/7，重复回合fallback、同回合worker/governor通知、building owner参数、内部carrier过滤、transfer/load完整scope | record函数代替业务consumer；能限制投递scope，不能证明一次事件只采集一次全player事实。P13a-F03仍成立 |
| 同步batch事实／区域索引；B138 `:113–155` | 真实RuntimeWork；两个本地城＋一个foreign reference；Facts为stub，检查成功复用、新batch重读、错误后重试；区域枚举中途抛错不发布半份index | 不承诺跨模块batch共享、跨写入缓存或真实Store的读取成本；当前保留副本和batch边界合理 |
| UNKNOWN失城与同回合变化；B138 `:158–181` | 真实GPP＋P0-B2/SQL fixture；确认foreign后读carrier UNKNOWN先保留，foreign turn恢复读取后撤销；load listener撤销；同回合worker1→4收益系数2→8 | native对象/事件为mock，不能据此声称原生回调参数/时序重新通过。该测试确实反证“全部foreign事件都可丢弃” |
| UI原因合并／中央分发；B138 `:184–229` | 真实GPPRefresh UI，重入、失败重试、worker/facts/late turn/load；截取实际Gameplay的相关branch，八类consumer为计数stub＋Network stub | 不执行全Gameplay composition、真实writer组合或新文化consumer负载；不能将stub调用次数当总事实访问／allocation。明确截取fixture并不等于伪造测试 |
| 轻量Governor读取；`test_b136_facts.py:138–282` | 真实Probe/EffectiveFacts，对历史baseline作差分；729个六property组合、异常、Potential0–4、pending、输入不变/返回副本，精确getter计数 | 729是状态组合，不是城市数；CityFlow和Store读路由为stub。证明删掉特定诊断getter，未证明city_scan或总内存减少 |
| 真正ACTIVE→Network接入；B136 `:284–369` | 真实Probe/EffectiveFacts/Input/Bridge，**2城1路线**；同route同turn资格变化、UNKNOWN旧ref保持、新ref拒借、owner/epoch变更；同包核capture1、facts2 | 固定小图且无完整真实consumer群；不能反证更大工作集的重复读取。加载是process-local Bridge重建，不是Civ VI冷加载 |
| D producer与两个consumer；`test_b132_event_cache.py:10–60` | 实际D/Housing/GPP或Infrastructure；主要一城，后者另一个runtime；重复同城读取hit、同回合修复/掠夺/未知/引用/资格变化 | 不是多个模块在超过8个合法D城市间轮巡，未触及W02容量边界；没有重测必要 |
| D静态目录优化；`test_b133_redundant_reads.py:93–151` | 八个完整输出差分场景；包装`GameInfo.Buildings.__call`，断言定义枚举9→1；两owner缓存隔离/dirty/引用/load | **定义枚举次数不是每城HasBuilding次数。** 缓存后的buildingOrder仍每次miss逐定义presence检查，P13a-F02未被9→1反证 |
| D自身规模；`test_p0_a.py:96–123` | 1/2/4/8城冷Read各一次，断言capture=N、district_scan=N、building_check=N×建筑定义数；同城10,000读不新增native reads；1000个不同city各Read一次且CacheSize≤8 | 上限断言证明内存条目有界，不证明第2/第3轮可复用；输出clone仍有成本。N×B是原算法的检查，不是未来优化必须维持的性能目标 |
| GPP局部重复读取；B133 `:11–64` | 真实GPP old/current；四专业×8顺序状态，稳定carrier presence64→32，完整32项preflight、remove-before-add、UNKNOWN/foreign保持 | 是一个writer、固定精确carrier集合；不是城市遍历或整轮工作减少50%。旧保护应保留，不能为更低计数跳过preflight |
| 多城持久化；`test_b108_e2_multicity.py:69–98` | 真实production Store，1/2/4/8/**33城**，P0/P1混合、一城投资P2；index稳定，目标record局部写，其它record值不变，load/idle零写 | 没有多座P4传统城；计mock SetProperty，不计写前全record扫描。33城通过不能排除P06a-F01的N×T |
| 传统计龄与载体换档；`test_b143_tradition.py:21–38,74–84`、`test_b144_tradition_effects.py:38–59` | 单座P4科研＋一个Culture控制；真实Store/Investment/Tradition，首P4原子起点、ACTIVE1仍计龄、重复/load去重、写失败恢复；40回合只有四次carrier换档，共changes+8 | **40回合不是40城；carrier不逐回合写不等于永久年龄不逐回合写。** 内部全记录检查未设成本断言 |
| 单record损坏隔离；B108 `:108–115,125–129,197–200`、`test_b140_templates.py:94–104` | revision损坏、缺record、特定template损坏时控制城保持可读/不被修改 | W03已证明`current=true`形状会collection fault；存储值未变与authority仍可用是两件事。沿用P06a-F02，不新增同类finding |

### B136 progression的真实继承边界

`test_b136_progression.py:32–54,86–147`加载真实当前模块，主场景通过`StartLegacyTest`做单record导入／投资／返回；`:149–180`另用production `Start`，只有一座P2城。`:163–165`只提取B108 helpers，并**明确停在scale循环之前**。它不是“Store被stub所以没有价值”，也不是执行了B108全部多城测试。

B143经B140/B124/B108及return helpers组装真实Store环境，提取fixture不继承执行每个源文件的全部cases。native事件同步派发、Properties即时表复制、CityManager、单位为mock；写次数不代表磁盘save次数。继续保存这些精确fixture界限比增加一个泛化“全通过”数字更有用。

B132/B133同样仅截取P0-A/B2/C的fixture声明，没有执行源文件顶层1/2/4/8或1000城规模循环。fixture建筑目录来自静态catalog snapshot、边界合成row和相关carrier SQL，不是当前游戏全部加载Buildings。UI Request仅计发送，未串起完整Gameplay调用链。

## Network规模测试：已有保证与未测维度

| 测试入口 | 精确工作集／断言 | 可继承结论／限制 |
|---|---|---|
| `test_arch_v2_batch_a.py:12–74,190–201` | 真实Input/Bridge，5城，EffectiveFacts/native mock；Boost替代consumer；改变ACTIVE/首都/中心并比较旧新输出 | 小图拓扑差分，不是完整Boost或整包规模负载 |
| `test_arch_v2_batch_b.py:34–42,81–100` | 4城、一个TEST模板、空learned、模拟建筑；实际Discount（Batch B直接加载工作树源码），冷derive一次后100Audit不再derive，检查副本隔离 | 当时consumer调用合同；D1 `:200–203`显式换回历史Discount以保留旧断言，不能称未经适配的今日整包 |
| `test_arch_v2_d1.py:108–145` | 1/2/4/8城，全部NONE/ACTIVE0/空路线；真实Bridge/Input/Discount/Counters，事实/ledger为stub | 单次warm dirty Audit精确旧`[N²,N,N²+2N]`→新`[N,1,3N]`（facts、derive_requested、city_scan），processed=N；确实证明了该场景的重复Capture消除 |
| D1 `:161–174` | 8城、一个工业source、7条路线；ReadLedger故意额外读一次facts | 8 capture＋1 source＋1 ledger=10次facts，ledger一次、query一次；不是多source／大模板集 |
| `test_arch_v2_d2.py:21–101` | 九模块分别启动的192组状态，共1728 map差分；规模循环只七模块×1/2/4/8城，Network查询全stub；每城一个district | facts≤2N、district_scan≤N是独立模块边界，query只打印；不是九模块共同处理同一通知。Copy的RESEARCH scale场景不满足工业source，不覆盖最重非零复制 |
| D2 `:107–115` | Commerce专用3来源/5接收城/15直接入站边，非零yield与变化 | 有效验证商业专用公式；Bridge仍是stub，不能混成公共中心/分发的dense graph测试 |
| D2 `:116–138` | 真实Bridge，固定5城3路线；10,000轮三个Current查询，capture0/版本不变；一次Governor变更capture5 | 证明已发布view查询不重采；并不证明查询零成本。Current返回副本、来源数组排序随结果规模变化，未测bytes/GC/耗时 |
| `test_b137_network_isolation.py:198–214,380–401` | coordinator段为五stub；集成段是真实Bridge/Isolation＋五真实consumer、两城、手工seed载体 | 有价值的精确撤销/保留sentinel/重复零写；没有正常publication→五模块重算的共同工作集 |

`PerformanceCounters.lua:14–23`只累加指定标量。D1的3N city_scan包含不同遍历步骤，`derive_requested`也不同于`derive_executed`；这些不能相加当耗时或分配字节。干净10,000次pulse与持续真实变动同样不是可替代的负载。

README明确这些入口是historical、LOCAL_SIMULATION和按任务选取；Test_Catalog只是保留旧入口的角色目录，不是全部动态测试清单。B132/B133/B136/B138不在Catalog不构成新finding。当前P0-L3A仍是B168延期的定域测试，不能因本次审计把上述旧wrapper全部变成它的新gate。

## 对既有finding与处理时机的影响

| 既有ID | 本轮新增证据 | severity / timing保持 |
|---|---|---|
| IA-P06a-F01 | 保存次数/值隔离与内部访问次数分离；B108和B143不约束每写全records。W03真实Lua已有8×8=64、20×20=400、40×40=1600、40×1=40，ACTIVE1亦计龄 | MEDIUM / **FIX_NOW**。继续增加长期writer会放大；现有写入正确性断言不能当反证。不是本轮修复授权 |
| IA-P06a-F02 | 既有坏revision/template隔离有效，但没覆盖坏endpoint导致collection fault；W03已同时验证控制城字节不变与不可读 | HIGH / DEFER，局部形状风险，不因缺测试升级为全项目停工 |
| IA-P13a-F01 | 1城warm、1000城单遍上限、两owner隔离均不等于>8工作集warm轮巡；W02已有条件性结构反例 | MEDIUM / MONITOR；**当前合法C_D>8仍UNKNOWN** |
| IA-P13a-F02 | B133“9→1”只计定义枚举；D miss依旧扫描cached buildingOrder，返回仍clone诊断数据；B规模未独立变化 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION；需正常primitive/诊断边界，不是先加stress |
| IA-P13a-F03 | 每个模块线性、局部64→32、Current查询零Capture，均不能证明一次真实cause下所有consumer合计工作已收窄 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION；复用W06中央名单图，修复时覆盖共同cause而非仅再加城市数 |

**D资格限制不能跳过。** 所核正常Housing先ACTIVE≥2才Read；Infrastructure先Research/ACTIVE4；Apply先Research/ACTIVE3；Chair先Research/ACTIVE4；Meaning先Culture/Potential4/ACTIVE4且有作品。fixture直接赋ACTIVE并不证明原生同时有那么多合法D城市。20–40是总城市规模，不自动等于20–40个D cache key；本轮不展开Governor/Mod来源调查，也不升级W02的可达性疑问。D服务独立诊断读可以不受专业资格限制，同样不能当正常高频consumer工作集。

## 将来修改相关公共路径时的最小验证建议

这些是待用户审阅的建议，**没有修改现行Workflow、测试、阈值或授权**；也不要求现在补完所有矩阵。

1. **保存路径**：复用W03真实Store fixture，分别变化N（全部record数）和T（本回合确需更新记录数），保留写入结果/局部性/损坏保护，同时衡量相关内部访问。8/20/40已经能区分N×T，不需要几万次stress。旧N×T断言是反例，不是修复后必须保留的性能目标。
2. **D采集／cache**：独立区分总城C、合法D工作集C_D、已加载建筑定义B、每城district数量和消费者顺序。若改缓存，再测试8/9及同批重复轮巡、真实dirty/reference/UNKNOWN；若改静态目录，保持结果一致并检查不相关carrier定义增加是否扩大normal读取。先确认合法工作集，不用不可能的ACTIVE组合宣称收益。
3. **共同更新／Network**：若改传播，只在本批受影响模块上建立一个真实producer＋相关真实consumer的混合场景，分别观察必要变动、同值重发、干净通知；控制source/recipient/route数并保留确实必要的跨城依赖。单模块当前fixture继续作为快回归，不必合成全Mod模拟器。
4. **计数口径**：指明事件/函数调用、访问元素、native getter、写尝试/成功、投影条目或bytes/timing中的哪一项；未测的不能由另一项推导。不同存档、不同GC策略、不同城市结构不直接作性能归因。

上述1–3按未来实际修改选取，不是每个新ability必须重跑的测试包。成熟未改的共享生命周期证据照常继承；只有新的native不确定性才安排一次最小实机验证，不恢复重复save/load仪式或旧长测。

## 实际读取、验证与未覆盖

- 当前root/project AGENTS、项目入口/Workflow规则沿用前序已核版本；Authority/current manifest字段及Status CURRENT本轮重读。`context.py check P0-L3A`为186 runtime/469 guarded引用完整性PASS、implementation_authorized=false；不是原生验证。
- 主任务全文读B138 update contract、B136 facts；B135 `ui_runtime`与provenance/branch片段、真实RuntimeWork全文；独立复核B108规模、B143计龄、B144carrier断言，D1/D2关键fixture/断言、B137集成段、B132/B133关键counter、D正常consumer资格。未将截断输出计为全文。
- 三路只读审阅：D组读取B132/B133与直接P0-A/B2/C fixture、D/Catalog/consumer入口及W02原结果；Store组读取B136 progression、B108、B143、B140及直接E2/B124/B128/B111 fixture组装、B144相关段、W03脚本/JSON与保存循环；Network组读取A/B及D1/D2相关fixture/适配段、C2直接fixture、B137协调/集成、Counters计数段。均未运行历史wrapper、写项目或新建复现。
- 已读Architecture“公共更新与临时状态接入约束／结项后的实现与回归边界”完整相关段，D1/D2计数说明；旧Source/Git基线依赖按测试明示记录，不装依赖、不读外部游戏DB、不核外部runtime。
- 产物检查：report＋ledger共24条本地链接/锚点无错误；diff whitespace检查通过；旧confirmed/provisional/rejected正文与baseline逐段相同；变更仅两份审计文件。
- **本轮未运行玩法测试、stress、GC、引擎或新的Lua复现。** 现有W02/W03/W04/W05反例已能回答本问题；静态检查不新增LOCAL_SIMULATION_PASS或USER_GAME_TEST_PASS。没有修改正式断言去使历史套件在今日版本通过。

仍未覆盖：全部测试及native结果、20–40城的真实游戏负载、每一种建筑/作品/商路组合、原生时间/分配/GC压力、全部损坏形状、所有共享生命周期是否有充分native证据。**P12a覆盖完成仅表示此逻辑问题收束，完整P12仍未结束。**

## 下一准确入口

下一既定 **P13b — 会话状态的间接保留与GC职责**。先复用P06a ownership表和P09b publication/pending表，再沿：

- `Mod/PerformanceCounters.lua`：唯一GC协调入口、结果/flight/ring/session记录及失败退出；不调参数，不做原生回收实验。
- `Mod/CityProgressionStore.lua`：pending候选、workers/positions/root引用的创建、完成、失败、load边界；永久历史与可丢会话状态分开，复用P06a-Q03而不发明毁城规则。
- `Mod/NetworkBridge.lua`、`NetworkSender.lua`、`UI/BackgroundRoutes.lua`与`GreatWorkFacts.lua`／`UI/DialogueRefresh.lua`：已核当前槽位的内部内容、旧ref/epoch/sample是否仍被间接保留。只沿实际引用扩到相关consumer，不全仓枚举所有table。

逻辑问题是“有界外层槽位是否仍留住过时的大对象／无法完成的任务，GC是否只回收已不可达对象而被误认为cleanup”。先静态建立创建→替换→退出闭包，只有具体疑点才做临时fixture；不重做W04协议/容量反例、不重开用户性能长测。

用户需要决定：当前无。用户需要测试：无，B168继续待办。本轮在P12a自然边界提交审计报告/ledger后停止；下一slice未启动。
