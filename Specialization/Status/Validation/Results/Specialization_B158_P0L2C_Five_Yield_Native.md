# B158.185 — 五产出首次原生结果与建筑变化失败

Evidence: USER_GAME_TEST_PASS（本次初始单片配置的五yield读数及W变化范围）；USER_GAME_TEST_FAIL（建筑变化后的多片配置收益）。冷加载控制状态OFF已观察，原生收益撤销／旧writer恢复仍未确认。完整意义延展／L2 NOT_PASSED。

## 本次观察

逐张读取2026-10-03 19:53:50–20:02:15十图。前六图是准备、基线、启用、W变化、结束和结束后巨作界面；用户确认后四图为冷加载后以及继续建造建筑的观察。图9／10已重新启用实验，不把它们的失败解释为load默认OFF。Culture ACTIVE4，图3 W2、图4／9／10 W1；图9／10为T63。未由截图取得最后新增建筑的精确类型或完整D组成，不反推具体新建筑。

| 图 | 阶段／W | 本城预期 S／P／G／Food／Faith | 原生实际 | 判定 |
|---|---|---|---|---|
| 2 | ①基线／2 | 0／0／0／0／0 | 0／0／0／0／0 | 当前基线已记录 |
| 3 | ②启用／2 | 2／2／8／2／2 | 2／2／8／2／2；有效同回合差值相同 | 初始配置所测五yield一致 |
| 4 | ②启用／1 | 1／1／4／1／1 | 1／1／4／1／1 | W变化后当前绝对值一致；旧比较失效，差值未确认是正确保护 |
| 9 | ②启用／1 | 1／3／4／1／1 | 1／1／4／1／1 | Production要求3、实际1，FAIL |
| 10 | ②启用／1 | 3／3／9／1／1 | 1／1／1／1／1 | Science／Production／Gold均FAIL，Gold还从4变为1 |

图9／10的实测差值分别与各自原生绝对值相同，巨作界面相应图标也显示这些数值；两处依赖同族原生巨作yield接口，不当作独立结算证据。报告已形成更高预期，没有配置异常提示。因此不是“D完全没有更新”，而是模型与当前承载配置形成后，原生读数没有兑现。初始配置通过不能扩大成全部取值、所有作品／主题化／回合结算或完整L2通过。

## 社区D6与当前目录覆盖是独立问题

图1社区有农贸市场、别墅、公交站。用户预期社区D6有本次扩展数据库依据。只读实际内层 `Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`（修改时间2026-10-03 19:57:56，America/Vancouver），核对Buildings与HD_BuildingTiers：

| 建筑 | 本次环境Tier | 当前Catalog责任 | 当前D贡献 |
|---|---:|---|---:|
| BUILDING_FOOD_MARKET／农贸市场 | 3 | known目录，读取合格HD Tier | 3 |
| BUILDING_HD_VILLA／别墅 | 1 | ordinaryOnly；ORDINARY_DEPTH_NOT_REVIEWED | 0 |
| BUILDING_HD_BUS_STOP／公交站 | 2 | ordinaryOnly；ORDINARY_DEPTH_NOT_REVIEWED | 0 |

三者Buildings定义和社区归属均存在。当前源[OrdinaryBuildingCatalog](../../../../Mod/OrdinaryBuildingCatalog.lua)对后两者明确ordinary=true、depthEligible=false；不是D公式把Tier1／2计算为0。本fixture中因此只计D3，每件食物floor(0.5×3)=1；若未来经目录适配纳入全部三者，则D6对应每件3。本轮只记录覆盖缺口，不修改Shared语义／Tier／Catalog，不自行将这些对象升级为depthEligible。

调查途中外层 `Cache/DebugGameplay.sqlite`给农贸市场Tier2且没有后两对象，是旧环境，不用于本次结论；先前口头D2判断据此纠正。原[B158本地流程](Specialization_B158_P0L2C_Five_Yield_Local.md)中的社区准备示例不意味着目录已覆盖其它扩展建筑，原始记录不重写。Catalog覆盖与多片收益失败分开登记，不以归一化／改Floor绕过。

## 多片承载是下一首要区分项

STATIC_CONFIRMED：模型仍为K=0.5，每域先Floor，同yield再相加，最后乘W。[Model](../../../../Mod/CultureMeaningModel.lua)与[Probe](../../../../Mod/CultureMeaningProbe.lua)将预期编码为各yield的有界整数片；[原生reader](../../../../Mod/UI/BoostGreatWorkRead.lua)先核验installed片之和等于每件预期，再读取实际收益。成功出报告只确认配置核验通过，不证明每个Modifier活动或原生可加算。

| 每件预期 | 当前编码（精确building后缀） | 对应Writing YieldChange | 本次结果 |
|---|---|---|---|
| Science3 | SCIENCE_1＋SCIENCE_2 | 1＋2 | 原生1 |
| Production3 | PRODUCTION_0＋PRODUCTION_1 | 1＋2 | 原生1 |
| Gold9 | GOLD_1＋GOLD_4 | 1＋8 | 原生1 |

当前内层DB只读确认三项高位Writing参数分别Science2／Production2／Gold8，均使用MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD；源码定义与模型目标相符。初始每yield单片S1/P1/G4/Food1/Faith1能生效，后续多片组合失败，支持优先调查**同yield多实例组合／刷新**，尚未证明引擎必然取最小、取首项或完全不支持加算。没有本次精确实例的活动／subject图，不能将installed配置当作原生实例PASS。

STATIC确认DistrictCompleteness与Meaning都有直接建筑变化订阅，前者先注册；Meaning也有有界目标城回合补核。图9／10模型已改变，不优先按“缺少D事件”修复。是否有native更新顺序／缓存边界仍需定域区分，不能无证据重写整个事件系统。

已有LOCAL测试验证编码、调用／生命周期和读数保护；部分native fixture按配置和提供模拟yield，不能证明真实多Modifier组合算法。本轮没有重跑玩法测试，也没有把模拟通过升级为原生加算通过。

## 第四步与冷加载的证据边界

第四步意图是：**启用时另存副本 → 结束验证 → 完全退出 → 载入刚才启用时的副本**。预期是新实验默认关闭、新owned撤销、旧模块按当前事实重新计算；不是让实验自动续接。

- 图5结束报告OFF；图6结束后巨作界面显示本城Writing P1／G2／S2／C4／Faith1／Tourism6，未显示Food。这是结束后的观察，未附全owned原生实例核对。
- 图7冷加载后的同城Writing为Food1／P1／G4／S1／C4／Faith1／Tourism6，与图6不同；图8控制报告OFF。**OFF只证明控制状态关闭，不能单独证明新收益完全退出和旧writer恢复正确。** 差异可能涉及旧模块加载重算、原生缓存／残留或未展示的当前事实，暂不猜原因。
- 因此本次不能给完整冷加载撤销／恢复PASS，也不要求用户立即重做整套步骤。下一定域诊断应同时取得精确owned实例／配置与作品读数，避免只用OFF文本验收。

## 下一最小建议（未实施／未授权）

单城、单件已支持Writing、单yield优先Production：使用现有整数片，比较清空基线、单片＋2与两片＋1／＋2；一次显式请求读取精确实例、城市归属、Active／subject、配置和实际yield，最后撤销。区分“高位单片本身失败”与“单片可用但多片不加算／刷新异常”，不改K、Floor、D或正式玩法。用同一精确退出读数覆盖END／冷加载歧义；若需要新增诊断入口或配置控制，先获实施授权，不恢复旧全局常驻扫描。

退出条件：只针对组合和本fixture清理给结论；失败停止对应承载候选并提出有依据的下一方案，不补差、不把配置当收益、不自动正式接入。社区两对象的Tier覆盖另作Catalog定域适配计划，不能混入该组合对照后把改善全部归因同一路径。

USER_GAME_TEST本次为部分通过／关键增长FAIL，完整L2 NOT_PASSED。正式all-city cutover、精准recipient、倍率独立／结算及L3/M/N/U2未授权。当前不需要用户重复旧四态、长测或补同样截图；停止等待下一最小定域原型授权。

## 归档与运行边界

十图逐张查看，原名原字节移入ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B158_P0L2C_Five_Yield_20261003/`，manifest关联本结果，10/10 SHA256 MATCH，原图不进Git；收件箱.DS_Store未动。

source/live沿B158.185／modinfo185、source daaef4b31ceb2e5858c5479c8b14ceaf9d3180fe及既有receipt `B158.185-daaef4b-playtest.json` DEVELOP_ACTIVE引用。本轮只读当前内层DB定义，没有重核外部运行包文件、部署或启动游戏。正式Design／Mod／测试／永久Property／GC／main未改；仅证据、状态、当前切片及对应已审阅索引维护。B158本地结果与此前失败证据原件保持。
