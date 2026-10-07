# B167.194 — 巨作启迪小数基础GPP原型

Date: 2026-10-06
State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
Scope: 授权L3-A原型；完整巨作启迪未实施。B166人工PASS不变。

## 技术证据与本地结果

只读当前加载数据库确认：`MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT`为`COLLECTION_OWNER / EFFECT_ADJUST_GREAT_PERSON_POINTS`；HD普通建筑存在BuildingModifiers同路径实例，Amount/GreatPersonClassType为其参数。已有整数Lv2使用Building_GreatPersonPoints，不能证明本路径小数。官方GreatPeoplePopup读取player:GetGreatPeoplePoints():GetPointsPerTurn并把展示舍入一位；未据此推断底层精度，也未发现/冒充城市专属基础率接口。

原型选择City Center内部建筑→单city modifier，每次仅一项0.1/0.3/0.6/1；不更改原生或HD普通建筑。SQL在加载DB内存副本执行，外部数据库未写。小数存入Value成功仅STATIC配置证据。

定向入口：`DevelopmentTests/test_culture_inspiration_probe.py`，依赖现有Lupa(lua55)及显式SPC_DEBUG_GAMEPLAY_DB；用现有只读DB→内存fixture执行实际Lua。23项新测试＋6项既有Meaning回归，29项PASS。覆盖替换/END、重复token与只读、城市隔离、未知ACTIVE/HOLD、确认失城退出、reference变化、load清理/漏load兜底、移除/创建/未知失败、创建期间Owner变化、清理失败锁停、原生读取token/回合/全国范围、SQL/包/语法、现行自动Meaning与旧Dialogue互不覆盖。没有改旧断言、跑全回归/stress或宣称原生已通过。

## 最小实机流程

选择已有Culture ACTIVE IV城。无需建新作品或配D，此批是固定值接口测试；尽量保持其他城市／政策／总督不变。

1. P0“巨作启迪测试”左键第一次：阶段0、配置0、载体0，右键读取原生全国科学家/回合，留下基线。
2. 左键下一阶段：依次+0.1、+0.3、+0.6；每次右键读取。检查配置载体始终1，观察原生率增量是否跟随替换，而非相加残留。当前正常百分比存在时，记录倍率来源，预期增量相应放大；没有可隔离倍率就保留倍率未验，不宣称通过。
3. +1为可选整数对照；小数无明显结果时可用它区分小数精度与整条接入问题，不强迫正常小数已清楚时再多一步。
4. “结束启迪测试”：载体0，刷新后原生率回到可比基线。

用户指出原生伟人率可能延迟一回合，允许等待刷新或过回合记录，不要求即时FAIL；跨回合报告不自动给因果差值，以人工控制条件的前后读数及回合记录核对。不要求本轮保存ON→OFF→冷加载→再开启。若全国其它来源变化无法隔离，结论为待区分，不猜测小数生效。

## 聚合及备用

不Floor时，按城按伟人类别一次计算0.1×D×W与逐件相加数学等价，预计减少效果实例／写入；实际正式承载方式仍待原生结果。用户授权备用为每城每类总量Floor，D3/W4→floor(1.2)=1；不合并不同GP类别、不逐件Floor。本轮未启用备用，不新增永久小数余额，不直接发点。

## 交付边界

本轮只交付原型；不接完整自动L3、M/N或新UI方案，不改GC、永久保存模型、HD及主分支。部署记录与实际源/live见[Status](../../Specialization_P0_Status.md#current-authoritative-state)。通过对应原生精度/正常倍率门槛后，另提正式六类自动接入；失败定域调查，不阻塞已通过B166。
