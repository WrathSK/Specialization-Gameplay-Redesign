# P0-L3 —「巨作启迪」计划与小数GPP调查

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED / FRACTIONAL_BASE_GPP_GATE_OPEN。
Authority: Culture D0029 `CUL_L4_INSPIRE`及domains/work_pool；Shared D0035。基线与授权见[文化准备入口](Culture_Preparation.md)。

## 完整能力边界

Culture ACTIVE4，逐本城合格非文化GPP领域：

`baseGPP_d/turn = 0.1 × D_d × W`。

W是当前合格作品**件数**，不同时代数X不参与该公式；不要求专家工作。D按Shared绝对深度、cap10/最高单区域/普通建筑掠夺资格。领域映射为Campus→Scientist、Industrial→Engineer、Commercial→Merchant、Harbor→Admiral、Encampment→General、HolySite→Prophet。Government/Diplomatic/Neighborhood没有对应GP，不发点数；Theater不在此能力映射，**不产生Writer/Artist/Musician**。Lv2文艺赞助原有三类GPP继续独立存在。

新增的是正常基础GPP每回合来源，受现有百分比倍率；不直接ChangePointsTotal、每回合发固定点数、不创造小数余量账本或自定义Prophet溢出Faith。例：D3、W1→0.3 base；W2→0.6；D10、W1→1；100%合法GPP加成作用于基础来源，不是把所有城市GPP替换成该公式。

0.1是正式Design值但技术待确认。没有Design舍入；科研floor、Boost round、旧GreatWork量化及HD per-population小数先例不能跨接口当许可。

## 已核对的接口

- 当前`Lv2GPP.lua`+`Building_GreatPersonPoints`以每工作专家+2的整数基础来源工作，之后让原生GPP百分比生效。这是可复用的资格/载体/退出结构，**不是0.1路径已通过**，也不能把新能力塞入专家人数编码。
- 本轮只读已配置DebugGameplay缓存：PointsPerTurn声明INTEGER；`MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT`和city district GPP路径有`Amount/GreatPersonClassType`示例，两项相关Effect查询未发现小数Amount先例。SQLite类型声明/未找到先例均不足以证明引擎不支持小数。
- 候选先验证原生city/district `Amount`基础来源是否忠实接收0.1/0.3/0.6并吃倍率；再判断building GPP字段是否存在可行路径。不能用player全国一次性点数代替city基础来源。
- 当前K `Summary`已返回count，但确认通知比较**仅含时代数等L1输入，不含count**。L3接入必须补轻量件数变化通知：同一时代W1→2也重算；不另开后台collector。新通知不能让L1重复施加未变的时代收益。

## 分步实施建议

1. 下一轮获得授权后先做真实Lua纯模型/小数SQL配置与一个最小原生GPP probe；单城单class隔离，记录预期base与native per-turn rate/正常倍率。探针有独立退出，不把未知配置当正式能力。
2. 原生门禁通过再接正式ACTIVE/D/W模型与module-owned派生writer；参数集中为GPP_K，禁止多个Lua/SQL各硬编码。没有新永久成果或每回合奖励事务。
3. 复用现有事实和E2 RegisterExit/Return，load重新派生；Lv2GPP原有owned列表不与L3混用。测试看增量，不能因HD原有基础/其它城市点数叠加把全国总率当选中城市贡献。
4. 如果原生精度/正常倍率不满足，停止该接口，报告TECHNICAL_INVESTIGATION_REQUIRED；要求改值或量化才向用户提DESIGN_DECISION_REQUIRED。不自动使用整数、floor、累计到整数再发或额外Faith转换。

本批没有旧同名writer要关闭；不提前退休Dialogue/旧Culture Eureka，不重复退出L1/L2已处理对象。预计涉及一个小型模型/consumer/SQL及定向测试，K轻量count变化、Gameplay/modinfo/按需诊断；按真实primitive复用现有文件，不创建泛化能力引擎。L3不以L2原生精度成功为证据，L2失败也不直接证明L3失败。

## 更新和资源边界

依赖ACTIVE/当前城市引用、领域D、W。创建/移动/交易confirmed馆藏、普通建筑完成/掠夺修复、资格/总督、confirmed loss/return、load与已有有界fallback触发对应城市。工作专家无直接公式依赖，不给所有专家事件增加新全国计算。

当前小型输入可在一次可靠读取中复用；署名owner/引用/确认版本变化即失效。UNKNOWN同一可靠引用HOLD，确认空/失效撤销；冷加载不以保存carrier为权威。模块只拥有当前配置/错误、随城市集合裁剪，无每回合历史留存，无独立GC。真实同回合W/D变化继续响应。

## 最小验证和退出

W0004 L2；只对实际共享通知/ownership边界补定向回归。

| 用例 | 断言 |
|---|---|
| D0/1/3/6/10 × W0/1/2，六class | 保留0.1精度，无X/专家依赖；GOLD份额3不用于GPP |
| 相同时代增加作品、不同类型排除、移城、掠夺、两城 | count变化通知与D正确；不串城/不同城公式独立 |
| base＋原生百分比，HD基础来源 | 新base不一次性直发，不覆盖其它base，不重复倍增 |
| ACTIVE3/4、UNKNOWN、loss/return/load、重复、错误 | 只撤销本项，正常重新派生；Lv2三类、L1/L2及K通知不回归 |
| bounded state/dispatch | 无变化零写；无新增槽位/全国扫描或无界错误记录 |

probe就绪后只要求一个单城最小流程：使一类D3、W1，核对0.3→同一时代W2的0.6，再利用一个现有GPP百分比变化核对base被放大，最后撤销/冷加载。全国getter包含其它城市；无法隔离时说明观测限制，不能以模拟倍率写原生PASS。用户现在只测试B148，不增加新任务。

诊断`W件｜领域D｜预计base/class｜配置｜可取得的原生读数/UNKNOWN`，右键映射/排除分页。Exit为小数基础率和原生倍率门禁、本地状态/通知回归、最小原生对应范围通过；否则仍partial，不宣布已实现。

来源：[正式Culture](../../Design/Content/Culture_D0029.json)、[Shared](../../Design/Content/Shared_D0035.json)、[旧基础GPP实现证据](../../Reports/Technical/Specialization_B035_Lv2_GPP.md)、[K检查点](P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)、[精度待办](Yield_Precision_Backlog.md)。
