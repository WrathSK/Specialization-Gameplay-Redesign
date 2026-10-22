# B170.197 — Shared D 普通事实与按需诊断分离

Date: 2026-10-08。State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED。source commit `343868e8bcd23efddb629b12b8bedf134334cb67`，对照 `df0cc39`；本地完成时外部包仍B169.196。用户已授权[独立计划](../../../Reports/Proposals/Shared_D_Fact_Read_Repair_Plan.md)，只处理P13a-F02的Shared D部分，不关闭GW扫描子项。

## 实际合同与修改面

`DistrictCompleteness.ReadFacts`返回紧凑、独立副本；`Read`保留详细读取结构。二者同一catalog、原生采样、ref/token、epoch、availability/error和≤8 cache。保留D、uncapped、区域/type/plot、普通资格、tier、depthEligible、位置/域冲突、完成/掠夺和原有UNKNOWN保护；紧凑版省略建筑name/tierSource及excluded展示树。

正常capture仍检查全部Building presence；已存在的每项仍读取location/pillage，保留旧failure→HELD语义。没有证明内部定义可在不弱化旧安全检查下省略，因此采用计划允许的保守方案：不改OrdinaryBuildingCatalog，不新增前缀忽略或native枚举假设。

cache保存最小原生raw与compact；需要时才从同一raw生成full，无第二次native采集。成功刷新废弃旧detail；失败保留旧raw/value，availability为TEMPORARILY_UNAVAILABLE，不能当当前READY。detail/compact均clone，外部修改不污染权威。revision现在表示业务事实；名称、当前未完成目标和off-district排除说明的变化仍刷新详细内容，但不触发业务publish。

正常消费者ResearchApply、ResearchChair、ResearchInfrastructure、CultureAesthetic、CultureMeaning切换ReadFacts；科研Describe保留Read，Aesthetic按detail参数选入口；Probe/Shadow诊断原入口保留，纯model公式未变。并未取消完整record/目录/失城保护。

修改源码：DistrictCompleteness＋五consumer；Probe/modinfo仅B170.197标识。新增[定向测试](../../../../DevelopmentTests/test_shared_d_fact_read.py)。没有Gameplay/Design、save schema、Store、GW、事件传播、缓存容量、GC、SQL/资产、部署工具或main变更。

## 本地证据

**19 unittest方法／50 subTest PASS**。冻结Git基线实际D/五model逐值对照；三个实际科研writer八个连续状态的carrier集合及累计写入MATCH，Apply缺tier在新ReadFacts准确报原错误并保持旧效果。涵盖tier0/nil/unsupported、replacement、域/位置冲突、完成/掠夺、社区最高单区域及同值tie、ACTIVE/UNKNOWN、同回合变化、新回合兜底、ref/owner/load/return、其它城市、mutation隔离、非普通建筑三类读取失败与≤8缓存。

| 测试fixture口径 | 原完整路径 | 新正常路径 |
|---|---:|---:|
| 五次共享读取的native capture | 1 | 1 |
| Building presence检查 | 120 | 120 |
| 完整Calculate | 1 | 0 |
| 返回建筑name行的clone | 15 | 0 |
| 返回excluded树的clone | 5 | 0 |

增加100／1000内部定义或未知定义：presence仍220／1120；未把扫描次数下降写成收益。普通miss/hit及detail→normal都不构造完整展示结果；首次明确detail每confirmed capture构造一次，无额外native读、写收益、revision/publish。

另外运行CultureAesthetic/Meaning实际writer的**43项相关既有回归PASS**，用已有Meaning数据库fixture在只读DB的内存副本精确重建定义，原数据库无写入。没有运行历史stress。

执行限制明确保留：直接旧Aesthetic数据库setup先遇到已加载SQL重复，未开始case；使用既有reset fixture后，完整47方法中的两项旧modinfo176/193断言、一个仍拦截旧Read入口的注入case及一个旧GW callback断言不纳入43项。旧version断言不改；ReadFacts正确入口的实际缺tier反例已加入新runner；GW callback失败在未改的df0cc39同样复现，与本次D切片无关，未修复、不报旧全wrapper通过。全套历史绿色不是本批完成条件。

修改Lua语法／modinfo197与完整Files清单检查通过；Design、冻结Audit、tools及旧tests逐字节对照不变。后续context/link/static结果随检查点记录，不把机械检查升级成原生收益PASS。

## 可重跑入口

```sh
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_shared_d_fact_read.py
python3 Specialization/Workflow/context.py check Shared-D-Facts
python3 Specialization/Workflow/context.py self-test Shared-D-Facts
```

新runner需既有Lupa lua55与完整Git对象df0cc39；自身不需外部DB。43项文化回归需按已有配置提供只读DB，使用已有reset-in-memory fixture并选择上述直接业务case；不能把缺依赖或历史wrapper未通过报PASS。

## 剩余成本与归因边界

仍有全定义presence O(B_loaded)、located非普通业务行、Chair模型既有p.rows；cache保留raw＋compact，显式诊断后额外detail，条目仍≤8但实际保留字节未测。此次减少正常展示树构造/复制，不宣称nativeCPU、内存或总扫描已改善，也不调整GC来隐藏成本。GW动态slot和P13a-F03传播等仍需独立授权。

## 一次最小实机

安全部署后，选现有Culture ACTIVE IV城（意义延展正常、已有合格巨作）：

1. 查看意义延展的当前D/每作品追加值及巨作实际收益；先不打开完整D报告。
2. 同回合完成一个可提高D的合格建筑，确认正常追加值与作品收益按既有逐域Floor变化。
3. 再打开相关详细报告，确认D组成正确；反复普通／详细查看，收益不重复增加。

需要所选变化跨过既有Floor档位。例如学院D3→6时，每件额外科技由floor(0.5×3)=1升至floor(0.5×6)=3；其它来源不变时每件+2。使用已有fixture，不要求人为制造多个高级城、保存ON/OFF、冷加载或原生内存长测。已有B169保存/其它成熟生命周期证据继承；此测试只验本批普通读取自动接入及详细切换。没有合适文化城时可用科研IV正常D×工作专家入口的同类对照，测试一类即可。

## 停止点

本地检查点完成，后续部署受有效W0003与真实game exit/clean-source/receipt/hash/恢复点门禁约束。原生结果仍待用户；不自动处理GW、广播、下一审计修复或正式L3。B168小数GPP精度调查独立，不受本批变化。

## 安全部署与最终文档检查

按有效W0003授权，OS再次确认游戏完全退出、main/develop clean/sync、原B169 receipt及stable备份hash相符；精确stable桥接后激活B170.197。部署checkout `a05a072`，实现commit `343868e`；receipt `B170.197-a05a072-playtest.json`为DEVELOP_ACTIVE，186/186与源码MATCH、无pending事务，B169完整恢复副本与stable恢复点保留。没有启动游戏或修改main。

文档351个本地链接/锚点无失败，context/schema/selector及self-test PASS，helper三项PASS；Context Lock仅同步本批已审文件，Runtime Index只更新八项源码（含包标识）provenance。最终原生待一次上述D变化/详细切换，不重复保存/冷加载，不进入其它finding。
