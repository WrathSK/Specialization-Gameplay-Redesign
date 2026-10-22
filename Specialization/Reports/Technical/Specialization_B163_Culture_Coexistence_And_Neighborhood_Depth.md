# B163 — Culture共存与社区D目录定域调查

**STATIC_CONFIRMED：HD的著作＋2直接附普通剧场；社区三条ordinaryOnly尚未开放D资格。USER_GAME_TEST_FAIL：B163所测Culture追加；其它产出只按[五图结果](../../Status/Validation/Results/Specialization_B163_Meaning_Final_Yields_Native.md)限定范围通过。** 本次只读，没有原型／实机测试、外部写入或接口不可行性的普遍证明。

## 本次来源与范围

复用[B155文化路径](Specialization_B155_Meaning_Culture_Path.md)、[B157实例反证](../../Status/Validation/Results/Specialization_B157_Modifier_Comparison_Native.md)、[B158社区缺口](../../Status/Validation/Results/Specialization_B158_P0L2C_Five_Yield_Native.md)。只核对本模块、目录／D直接调用、HD区域扩展`Database/theater.sql`与既有配置定位的内层`Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite`（SQLite mode=ro，mtime 2026-10-04 09:27:48，America/Vancouver）。扩展为Workshop289070/2701747165；安装路径不成为新的配置规范。未使用外层旧Cache，不扫描其它Mod或历史全集。

数据库证明本次加载的定义，不证明目标城市所有建筑实存、完成或未掠夺；游戏实例证据只来自五张截图和指定旧报告。

## Culture共存与外部效果接管风险

### HD实际附着与当前模块退出

| 来源 | 实际定义／范围 | 本次证据 |
|---|---|---|
| 古罗马剧场 | `BUILDING_AMPHITHEATER`直接附`HD_AMPHITHEATER_WRITING_CULTURE_BOOST`；Writing／Culture flat2 | 扩展theater.sql:152、195、231–233；当前DB一致 |
| 剧场旅游业 | 另附`HD_AMPHITHEATER_WRITING_TOURISM_BOOST`，单城Tourism primitive、ScalingFactor150 | 同文件153、196、234–235；不能与flat Culture混为同一效果 |
| 普通剧场本体 | InternalOnly0、Theater归属、Culture1、CitizenSlots1、WriterGPP2、两个Writing槽 | 当前Buildings／GPP／Slots定义；不是隐藏carrier |
| Meaning | final Culture与HD flat使用同`COLLECTION_OWNER / EFFECT_ADJUST_CITY_GREATWORK_YIELD`；Meaning按合格作品、ACTIVE IV、市政／外交D独立追加 | [Model](../../../Mod/CultureMeaningModel.lua)、[Probe](../../../Mod/CultureMeaningProbe.lua)、[SQL](../../../Mod/Data/CultureMeaningProbe.sql)及DB；同primitive不是堆叠算法的证明 |

HD flat2影响本城所有Writing，并非只限剧场槽内或Meaning已支持目录中的著作。Meaning读取的W和HD受益集合不保证相同。把两者简单合成“A＋2”给所有七类作品，会把HD的Writing收益扩展到不该获得它的类别；只按Meaning合格W补回HD，又可能损失其它Writing原有收益。

[Probe](../../../Mod/CultureMeaningProbe.lua)只创建／撤销92个精确自有InternalOnly建筑；[CityProgressionStore](../../../Mod/CityProgressionStore.lua)的定域退出同样要求module-owned名单。原生实例ID、owner、Active、subjects是[只读诊断](../../../Mod/UI/BoostGreatWorkRead.lua)信息，不构成可写控制接口。[Probe基础包装](../../../Mod/Probe.lua)提供建筑创建／移除；本次直接路径没有已验证的“只撤HD文化、保留普通剧场”的单实例detach先例。不据此声称Civ VI绝无该API。

### 为什么不采用移除再合并

- 删除普通剧场会同时碰建筑文化、专家／GPP、巨作槽、旅游业和普通建筑事实，不能作为撤销HD一项文化的办法。
- 修改全局BuildingModifiers附件／Modifier定义／requirements，会影响其它城市、AI、非文化专业、Probe OFF及加载状态。即使补偿建筑叫SPC，也已接管外部来源责任；现有“清自己的92项，再让HD维持原样”的退出证据不能覆盖它。
- 两种来源有不同资格与生命周期：剧场增建／掠夺／修复／移除、所有Writing、Meaning合格W、ACTIVE变化、易主及加载都需要新的控制／恢复合同。本轮不创建外部效果接管层。
- 合并flat后丢失来源标签，不能保证HD原有原生倍率关系与Meaning独立于Dialogue／主题化的固定追加各自保持；当前Probe只暂停自己的Dialogue，不证明该倍率边界。
- 本次同文件／DB还确认`HD_OPERA_MUSIC_CULTURE_BOOST`给Music flat3（157、200、240–242），艺术刊社四项给Art flat2（164–167、207–210、252–263）。解决剧场Writing并不解决全部作品共存。

因此风险足以采用用户条件后备：**市政／外交→Culture暂时隔离于当前Meaning实施，先完成七域五产出；HD原附件、原值和普通建筑全部保留。** 这是当前实施延期，不撤回D0046已接受机制，不改其它consumer／Government Design，不创设新产出。运行包隔离尚待下一修复落实。

### 已知失败与仍未知事项

B157已测HD2保持、Meaning3正确进入／退出、本城归属且旧GWA实验内撤出，但Culture4→4。B163改剧院宿主后仍Δ0。它们保留原生共存失败，支持隔离；未证明具体取首项、取最小、取最大、宿主竞争或所有同类flat必然不叠加。Production多片反证不可直接替代Culture根因证据。本轮不再请求关闭HD、重复四态、倍率或冷加载实验。

## 社区D的目录缺口

| 建筑 | 本次DB Tier | 当前Catalog | 当前D贡献（完整未掠夺时） |
|---|---:|---|---:|
| 农贸市场`BUILDING_FOOD_MARKET` | 3 | known，正常解析Tier | 3 |
| 别墅`BUILDING_HD_VILLA` | 1 | ordinaryOnly／depthEligible=false | 0 |
| 公交站`BUILDING_HD_BUS_STOP` | 2 | 同上 | 0 |
| 豪宅`BUILDING_HD_MANSION` | 1 | 同上；未确认目标城是否具有 | 0 |

[OrdinaryBuildingCatalog](../../../Mod/OrdinaryBuildingCatalog.lua):182–184／243–245给后三者ordinary=true、`ORDINARY_DEPTH_NOT_REVIEWED`、tier=nil，甚至未进入Tier解析分支。它们不是被解析成Tier0，也不是被相对完成度归一化。[DistrictCompleteness](../../../Mod/DistrictCompleteness.lua):27–49保留reason／Tier、累加后cap10、同域取最高单区域；[MeaningModel](../../../Mod/CultureMeaningModel.lua):6／30–37正确读`DISTRICT_NEIGHBORHOOD`→Food，每域Floor(0.5D)后再乘W；[Probe](../../../Mod/CultureMeaningProbe.lua):69直接取Shared D。

若社区为Villa1＋BusStop2＋FoodMarket3，当前目录结果D3／Food每件1；后续经精确目录适配，才应D6／Food每件3。这是Catalog覆盖，不能改Shared公式、Meaning系数／Floor或事件系统绕过。B163计划明确不扩目录，因此B158之后这个已知缺口没有被修复；不是本次单值承载突然丢失D。

保留已覆盖ShoppingMall、JNR ArtGallery／Hospital／Meditation／RecyclingPlant／TransitHub在当前DB的Tier3；不把它们强改成四层链。HD_INN／TAVERN本次DB不存在，不因此删除历史支持。Meenakshi的Neighborhood dummy仍在HD_DUMMY_BUILDINGS，应继续排除；Mbanza→Neighborhood归一、同Tier逐栋、缺低层不补、多个社区highest-single-district与cap10保持。

最小修复只审阅Villa／Mansion／BusStop三条ordinary→depthEligible目录升级，保留现有原生Tier／替代／internal/dummy／位置冲突保护；读实际直接consumer和现有Catalog回归，不建立AI建筑历史／全局新扫描。Shared事实会影响真实消费该域的模块，不能只在Meaning里私自加D；实施前核对直接依赖并按W0004定向验证。

## 下一步与证据边界

见[下一最小修复](../../Architecture/v2/P0_L2_Meaning.md#下一最小修复--文化隔离与社区d目录)。Culture隔离后备已由用户条件授权，目录补齐及整批实现仍待明确授权；没有新build／部署。本轮STATIC调查不代表修复已LOCAL_PASS，更不代表社区D6实机通过。现有五产出正面证据可复用，不因这两项失败重新派发全套生命周期。
