# P0-E1 — 只读城市身份核对 / B088.115

Authority: A0161 / D0035，四专业范围不变。用户已授权E1实施。
Status: **LOCAL_SIMULATION_PASS；首都原范围读档/分城UNKNOWN保护已有用户实机证据；跨Owner永久城市连续性门禁仍 TECHNICAL_INVESTIGATION_REQUIRED。**

最新[三图实机复核](../../Status/Validation/Results/Specialization_B088_P0E1_Native_Review.md)：分城转自由城市后五项City记录原有现无；不能依赖这些City Properties自动跨Owner保留。两张首都读档图与分城易主图分开记证据。以下实现范围/原测试计划保留，不要求用户立即重复。
本批可交付观察工具，但不是E1全部门禁PASS；E2/F不开放。没有正式迁移、持久marker、旧继承writer启动或新收益。

## B089授权补充

已获用户明确授权的[独立Game实验](P0_E1_Game_Record_Experiment.md)新增一个显式启用的测试key；下面B088只读合同继续适用于CityIdentityRead，不能解释成新实验也零写入。原生门禁未通过，未迁移任何专业记录。

## 1. 实际实现

`Mod/CityIdentityRead.lua`为独立纯预演＋只读采集器，Gameplay只新增三种手动诊断分发。复用面板两项隐藏入口“记录城市身份”“身份对照”，显式Label防止文字缺失；右键对照才展示凭据、旧新引用、各记录有无/是否一致及最后8条城市事件。暂隐藏巨作相邻/旧四级区域收益按钮，原逻辑保留，不增加面板总密度。U1机构原型不改。

正常摘要示例：

> 城市身份只读核对
> 原范围记录一致（迁移候选）
> 原验证范围内记录一致；仅可作后续迁移候选
> 当前引用：0/7 @ 4,5
> 跨易主／读档永久身份：尚未通过原生验证；未写入任何记录。

“迁移候选”仅表示旧记录结构及原锚点相容，**所有输出migrationAllowed=false**；不是正式可迁移或永久ID验证。

## 2. 旧保存记录及检查范围

| 记录 | Property / scope | 本批核对 |
|---|---|---|
| Binding | Game `SPC_DEV_BINDING_B013_P{owner}` + City `SPC_DEV_BINDING_B013_TOKEN` | schema/原owner/计数≤32/serial唯一/CONFIRMED/坐标；从token取原Owner只读总账，不按现owner重锚 |
| Journal | City `SPC_DEV_CITY_JOURNAL_B015` | 原锚点、TRACKING、基础专业/首次区域记录结构、foundationTurn/revision；不重跑历史区域事件 |
| Flow | City `SPC_DEV_CITY_FLOW_B020` | DONE，target=facts=journal；部分提交HELD，不调用resume |
| Investment | City `SPC_DEV_INVESTMENT_LEDGER_V1` | anchor/first一致、无pending、receipt→unitUID唯一≤3、revision=count+1；无记录不补造 |
| Templates | City `SPC_STANDARDIZATION_LEDGER_V1` | STD:token/原foundation/位置/schema/revision/learned结构；**未重新确认历史建筑目录**，明确NOT_VALIDATED |

不调用EffectiveFacts的writer/resume或旧继承模块。未认定历史最大Potential、所有权继承、当前目录下模板可用性或全世界token唯一性。不存在完整历史时不造空账本掩盖。未知/损坏/过大/循环记录均停止预演，原对象不修改。

## 3. 小型身份合同（候选schema 1；不是新增存档schema）

| 字段 | 当前authority / 行为 | 后续门禁 |
|---|---|---|
| cityRef | 本次原生对象owner/cityID/x/y | 只用于寻址，不能变成永久ID |
| candidateToken | 原Owner DEV绑定账本中的原凭据 | 仅原范围映射候选，不是新cityKey |
| cityKey | 本批不分配、不持久化，nil | 原生连续性证据＋单独授权保存适配 |
| generation | UNKNOWN | 夷平同地新城、ID复用不得靠位置接续 |
| evidence state | LOCAL_CANDIDATE / HELD / UNKNOWN | 任何状态均不允许本批迁移 |
| history | UNKNOWN，无历史最大值推算 | 未来per-city/per-specialization有证据History；不同专业Legacy各自决定 |
| future mode | NONE / SPECIALIZED / REALLOCATING应独立 | 仅架构类型约束；本批不创建状态，不把REALLOCATING当NONE |

原引用一致也不能证明经历过易主/夷平后仍同一generation。不同token明确不得合并；缺token/总账/部分记录不修复。token保留但owner/id改变→HELD_CROSS_OWNER；回原ref最多恢复原范围候选，不升级为原生连续性PASS。重复/旧/乱序事件只有证据，不更新权威身份。冷load清空观察基线，需手动重记；原持久账本仍只读。

## 4. Native静态证据与缺口

STATIC_CONFIRMED（代码先例，不是实机连续性证明）：
- 原版Expansion2 `UI/Loaders/TutorialLoader_Expansion1.lua:282` 的CityTransfered参数为playerID/cityID；没有永久ID或完整old→new配对。
- 原版AlexanderScenario `Scripts/AlexanderScenario.lua:174` / NubiaScenario:937 的CityConquered接收capturerID/ownerID/cityID/x/y；不能仅凭事件名证明Properties保留或cityID含义跨环境恒定。
- 已安装Cheat Menu `1528155583/Base/UI/Script/Cheat_Menu_Panel_Script.lua:116` 提供TransferCityToFreeCities；对应按钮受R&F限制。没有确认“指定Owner接管/立即夺回”入口，不能要求用户等待AI。安装文件不等于当前已启用。

未验证：City/Game Properties在转自由城/征服/夺回及读档后的保留、顺序、坐标同城generation区别。本批不增加可写标记；若只读证据不足，必须另报最小显式实验，不悄悄修复旧存档。

## 5. 性能 / 内存

只在手动点击读取5个City Properties和至多1个原Owner Game ledger；不扫描城市/区域/建筑/单位。Record为建立基线后立即核对，会读取两次；Compare/Detail一次。事件自身零Property读取。仅监听CityTransfered/CityAddedToMap/CityRemovedFromMap/CityInitialized/CityBuilt/CityConquered和load；没有unit/generic pulse/turn/per-frame observer。

一个观察基线；单快照上限8192节点、64KiB字符串、深度12；一条固定32槽事件环，每条至多8个64字符标量。报告仅末8条。不存无限历史，不写文件。load清空基线/事件；捕获失败不覆盖基线。缺失事件仅记录hook状态，不以fallback扫描补证据。

## 6. 本地验证

`DevelopmentTests/test_p0_e1.py`执行实际Lua：原锚点、改名、易主/夺回候选、同地新token/ID复用、缺失/冲突/partial、重复unit receipt、pending、模板结构、坏包/循环/大小边界、coldload；Property/扫描writer设为抛错，证明只读。

观察前20,000通知无取数；观察后30,000城市事件仅固定32条，无新增Property reads/scans/writes；10,000 UI idle通知零request。实际Gameplay dispatch及面板：每次手动操作1 request；失去城市选择后仍可对照原位置。原位置只用于寻找当前对象，不用于身份认定。

`test_p0_e1_regression.py`显式只适配新增诊断文件/版本，复用U1→D3→D2→D1→C→B2/B1/A→AV2全部旧断言。所有Lua编译、modinfo115完整文件/ImportFiles、SQL/旧writer/Design逐文件字节保护、部署临时目录保护通过。不是引擎SAVE/LOAD PASS。

## 7. 最小实机观察与退出

独立测试存档，一座原先正常工作的己方专业城：
1. 点击“记录城市身份”，右键“身份对照”保留第一张报告。
2. 另存并读档，重新记录同城、右键对照保留第二张；只用于核对冷load持久字段，旧session基线正确丢弃。
3. **只有现有Cheat面板已具备“转为自由城市”时**，先重记基线，再转移该城，直接右键“身份对照”（无需选择外国城）。保留第三张。原生产/收益不是本批验收对象。测试结束载入步骤1的独立档恢复即可。

本轮不要求盲目等AI/完整夺回；上述不是整个transfer→regain证明。若第三步不可控，跳过并报告，后续先补可控观察方案。原生证据不足时E1仍待核验；不因本地PASS进入E2。部署遵循W0003退出/完整备份/hash门禁，不启动游戏。
