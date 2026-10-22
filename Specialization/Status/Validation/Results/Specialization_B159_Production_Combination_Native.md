# B159.186 — Production单片成功、双片不加算的原生证据

Evidence: **USER_GAME_TEST_PASS**（本城单Writing、单片＋2即时读数）；**USER_GAME_TEST_FAIL**（同fixture双片＋1／＋2要求3、实际1）。完整意义延展／L2 NOT_PASSED。叠加选择算法、正常回合结算、END及冷加载退出未确认。

## 四图实际观察

逐张读取2026-10-03 21:10:00／21:10:24／21:10:46／21:10:49四张原图。用户明确图2单片、图3双片，随后停止测试。**图4是PAIR12报告下半段，不是END/OFF。** 四图均为游戏顶部T62／500；左侧Cheat科技／市政的73／83不是当前游戏回合。

同城：Edinburgh(TEST)，player0／City393220；同一Writing `GREATWORK_QU_YUAN_1`，ID1，宿主`BUILDING_AMPHITHEATER`，slot0，themed=false。当前完整reference在两阶段报告一致；不凭名字建立identity。

| 图 | 阶段 | 预期／载体配置 | 原生宿主作品Production | 同回合差值 | 可确认范围 |
|---|---|---:|---:|---:|---|
| 1 | BASELINE | 0／0，owned0 | 0.00 | 0.00 | 基线已记录 |
| 2 | SINGLE2 | 2／2，owned1 | 2.00 | ＋2.00 | 单片＋2即时读数一致 |
| 3／4 | PAIR12 | 3／3，owned2 | 1.00 | ＋1.00 | 两片不按1＋2得到3，FAIL |

图2：`BUILDING_SPC_MEANING_PROBE_PRODUCTION_1`存在且未掠夺；Writing原生实例12307，`YieldChange=2`、`ScalingFactor=nil`、Active=true。本城Meaning Writing实例1／Active true1，旧GWA Production实例0、城市UNKNOWN0。

图3／4：两building均存在且未掠夺；读取完整，本城Meaning Writing实例2／Active true2，旧GWA Production实例0、城市UNKNOWN0。具体为：

| Native instance | 精确Modifier ID | 参数 | Owner／subject已核验城市 |
|---:|---|---|---|
| 12314 | SPC_MEANING_PROBE_PRODUCTION_0_WRITING | YIELD_PRODUCTION；flat1；scale=nil | p0／City393220，District1048589 |
| 12321 | SPC_MEANING_PROBE_PRODUCTION_1_WRITING | YIELD_PRODUCTION；flat2；scale=nil | p0／City393220，District1048589 |

两者各有一个District subject，raw SubValue分别559589181／1448974251。它们证明本城映射，不是精确作品recipient证明；Active=true也不证明两份底层收益都已入账。此处实际yield来自原生宿主getter，不能以Active计数代替它。

## 定域源码核对与结论

**STATIC_CONFIRMED。** [SQL](../../../../Mod/Data/CultureMeaningProbe.sql)中两片是不同Building、不同Modifier ID，分别YieldChange1／2；均为`MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD`、同Writing对象类别／Production，Production无额外ScalingFactor、Requirement或prep子链。每个building另有其它作品类别附件，本次实例诊断只核对Writing，不宣称其它类别全已验证。

[Probe](../../../../Mod/CultureMeaningProbe.lua)从SINGLE2进入PAIR12先精确撤上一阶段＋2，再按owned顺序创建＋1→＋2，每次创建确认HasBuilding。[Model](../../../../Mod/CultureMeaningModel.lua)没有把不同Building误合并。[reader](../../../../Mod/UI/BoostGreatWorkRead.lua)调用真实宿主`GetBuildingYieldFromGreatWorks(YIELD_PRODUCTION, buildingIndex)`；它没有按两片逐项覆盖一个累计值，实例collector也不按Definition／owner／subject去重。两原生实例及参数可见，排除本次“第二片根本没创建”／“重用同一ID”／“报告漏列第二片”的解释。

**本场景的多片加算假设已失败，应停止依赖这套编码进行正式接入。** 用户提出的同yield不叠加与0→2→1实测一致，并与[B158](Specialization_B158_P0L2C_Five_Yield_Native.md)S3/P3/G9实际均1的组合失败相互支持。

仍不能确认引擎是按效果键覆盖、内部去重、首项／优先级、缓存或刷新顺序处理；本次固定创建顺序也不足以证明“取最小”或“永远只接受第一片”。不能外推为所有yield、所有作品、所有Modifier effect都不能叠加。旧[B157 Culture＋3与HD＋2](Specialization_B157_Modifier_Comparison_Native.md)是同族共存的相关反证，仍保留其自身背景和证据范围，不因此重开已延期的两域。

公开作者[YAGM SQL](https://github.com/Feofilakt/YAGM/blob/main/Moksha.sql)有单一Relic／Culture YieldChange3定义；它不是Production／Writing原生证据，也没有给出多实例的引擎选择算法。此次检索未找到可据以宣布精确内部算法的原始实现证据。

## 下一最小对照建议（未实施／未授权）

用户提出“单片1→撤销单片1→重新配置”有辨别力：**单片＋1→撤销至0→单片＋2→双片＋1／＋2→只撤＋1、保留＋2→结束**。每步按需读真实yield、精确building／native ID／参数／Active；同城同Writing、旧writer hold和Dialogue0%不变。撤销至0时若仍非0，优先查退出／缓存；若两片仍为1、撤＋1后变2，支持未加算但剩余实例能接替；若剩余实例确认却值错误，保留刷新边界。不同结果只定位本场景，不能提前宣布唯一引擎算法。

这是一项新的诊断状态／控制修改，现B159左键流程不能单独撤＋1并保留＋2；不得让用户改源码、手删载体或在现有入口盲试。保持默认OFF、单fixture、有界session、显式读取、UNKNOWN／loss／load／reference和旧writer退出保护；不加轮询、永久Property或全城事件扫描。先由用户授权最小诊断改动，本轮不实施。

若目标是验证实际替代承载，建议在同一最小诊断里再加**一个独立单片Production＋3**。当前`PRODUCTION_3`是bit3＝＋8，不是可直接使用的＋3。单＋3使用同primitive／Writing／YieldType，只改变一个YieldChange参数。成功后才有依据提出每yield一个最终值载体的方案；将来值仍是各领域分别Floor后相加的`each[y]`，不是已乘W的`total[y]`，不能再乘一次W。仅把多个旧Modifier放进同一building也没有解决同效果多实例的实证问题。

新对照可顺带覆盖已留下的END／启用副本冷加载清理歧义，复用同一fixture；不立即要求用户重复失败的旧五yield／长测。单片＋3、全部金额／五yield、精确recipient、Dialogue／theming隔离、正常结算和正式cutover仍各自未过门禁。D、K、逐域Floor、W、Catalog和Gameplay规则不改；不补差、不移为整城发放。

## 归档与运行边界

四图原名原字节移至ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B159_P0L2C_Production_Combination_20261003_2110/`，manifest关联本结果，4/4 SHA256 MATCH。原图不进Git，收件箱.DS_Store未动。用户称停止测试，未提供结束原生报告或冷加载图，不将此写成退出PASS。

source/live沿既有B159.186／modinfo186、source `59e686feb5e66dde7429c3e44a457cb6a826ace8`及receipt `B159.186-59e686f-playtest.json` DEVELOP_ACTIVE记录；本轮未重核外部运行包、部署或启动游戏。仅新原生结果／Status／当前切片／对应已审阅导航hash维护；Mod、测试、正式Design、永久状态、GC、main与既有冻结结果不变。未运行新玩法模拟。本轮停止，等待下一最小诊断实施授权，不进入正式L2或L3/M/N/U2。
