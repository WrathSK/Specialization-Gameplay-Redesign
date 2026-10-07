# P0-L3 —「巨作启迪」计划与小数GPP调查

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED / FRACTIONAL_BASE_GPP_GATE_OPEN。
Authority: 当前Spec D0048／Culture D0048 `CUL_L4_INSPIRE`及domains/work_pool；Shared D0045。基线与授权见[文化准备入口](Culture_Preparation.md)。

## 下一最小批次 — L3-A 单城单class原生门禁

**PLANNED_NOT_AUTHORIZED。** B166自动接入验收后的下一建议，用户审核后才实施／部署。只验证原生基础GPP接口，不直接交付完整六class能力，不因Design接受自动启用全国writer。

- 选已有Culture ACTIVE IV城与Scientist一类；先复核当前city/district基础GPP Modifier，保留HD／原生基础来源。最小可逆probe依次配置0.1、0.3、0.6，按需读取本城per-turn基础贡献／速率及实例；必要时用当前可观察的正常GPP百分比核对倍率。数据库字段接收小数、carrier存在不算原生生效。
- 门禁原型的固定值是接口对照；正式能力仍0.1×对应D×合格W，不能用Gold份额、专家、时代数或Floor替代。未知原生字段明确UNKNOWN；不能用全国点数总值冒充该城基础率，不能直接发点数或建小数余量账本。
- 复用本城reference／资格／K／Shared D与精确module-owned退出，单一会话／有界错误状态，END／换引用／confirmed loss／load退出，UNKNOWN按既有保护。无每帧／hover Gameplay请求、AI、永久成果或GC变更；不重构通知框架。
- 本地：小数配置与实际SQL／Lua、同城可逆替换与重复零写、读数独立于配置、退出失败／UNKNOWN及两城隔离；只补直接路径回归。若修改共享生命周期源码，再按真实delta补相应验证，不机械派发冷加载。
- 用户：一次连续session，基线→0.1→0.3→0.6→正常倍率（若当前可隔离）→END。每步分别确认小数精度、值替换、倍率及本模块撤销；无法区分基础率则停止并保留具体技术门禁，不自行舍入。
- 社区D不新增独立验收步骤。仅当现有fixture正好具备时，可顺带只读查看正常Meaning报告；不再要求已退役Probe的启用／END操作，也不为此重建社区或长测。

**退出／下一边界。** 小数基础率和正常倍率取得对应原生证据后，再单独提出六class正式consumer计划。失败只阻塞依赖该primitive的L3；B166七域五yield自动接入已人工通过；未来Culture追加恢复与主题化Balance保持独立边界，不自动关闭或推进。

## 完整能力边界

Culture ACTIVE4，逐本城合格非文化GPP领域：

`baseGPP_d/turn = 0.1 × D_d × W`。

W是当前合格作品**件数**，不同时代数X不参与该公式；不要求专家工作。D按Shared绝对深度、cap10/最高单区域/普通建筑掠夺资格。领域映射为Campus→Scientist、Industrial→Engineer、Commercial→Merchant、Harbor→Admiral、Encampment→General、HolySite→Prophet。Government/Diplomatic/Neighborhood没有对应GP，不发点数；Theater不在此能力映射，**不产生Writer/Artist/Musician**。Lv2文艺赞助原有三类GPP继续独立存在。

新增的是正常基础GPP每回合来源，受现有百分比倍率；不直接ChangePointsTotal、每回合发固定点数、不创造小数余量账本或自定义Prophet溢出Faith。例：D3、W1→0.3 base；W2→0.6；D10、W1→1；100%合法GPP加成作用于基础来源，不是把所有城市GPP替换成该公式。

0.1是正式Design值但技术待确认。没有Design舍入；科研floor、Boost round、旧GreatWork量化及HD per-population小数先例不能跨接口当许可。

## 已核对的接口

- 当前`Lv2GPP.lua`+`Building_GreatPersonPoints`以每工作专家+2的整数基础来源工作，之后让原生GPP百分比生效。这是可复用的资格/载体/退出结构，**不是0.1路径已通过**，也不能把新能力塞入专家人数编码。
- 此前准备调查只读已配置DebugGameplay缓存：PointsPerTurn声明INTEGER；`MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT`和city district GPP路径有`Amount/GreatPersonClassType`示例，两项相关Effect查询未发现小数Amount先例。SQLite类型声明/未找到先例均不足以证明引擎不支持小数。
- 候选先验证原生city/district `Amount`基础来源是否忠实接收0.1/0.3/0.6并吃倍率；再判断building GPP字段是否存在可行路径。不能用player全国一次性点数代替city基础来源。
- K `Summary`及B150以后的确认通知已包含count、排除数与类别未知，当前`GreatWorkFacts.sameInput`完整核对这些字段。同一时代W1→2通知可复用，不新建collector；L3接入仍应定向验证消费者重算与L1未变零写。

## 分步实施建议

1. 下一轮获得授权后先做真实Lua纯模型/小数SQL配置与一个最小原生GPP probe；单城单class隔离，记录预期base与native per-turn rate/正常倍率。探针有独立退出，不把未知配置当正式能力。
2. 原生门禁通过再接正式ACTIVE/D/W模型与module-owned派生writer；参数集中为GPP_K，禁止多个Lua/SQL各硬编码。没有新永久成果或每回合奖励事务。
3. 复用现有事实和E2 RegisterExit/Return，load重新派生；Lv2GPP原有owned列表不与L3混用。测试看增量，不能因HD原有基础/其它城市点数叠加把全国总率当选中城市贡献。
4. 如果原生精度/正常倍率不满足，停止该接口，报告TECHNICAL_INVESTIGATION_REQUIRED；要求改值或量化才向用户提DESIGN_DECISION_REQUIRED。不自动使用整数、floor、累计到整数再发或额外Faith转换。

本批没有旧同名writer要关闭；不提前退休Dialogue/旧Culture Eureka，不重复退出L1/L2已处理对象。预计涉及一个小型模型/consumer/SQL及定向测试，复用K现有count通知、Gameplay/modinfo/按需诊断；按真实primitive复用现有文件，不创建泛化能力引擎。L3不以L2原生精度成功为证据，L2失败也不直接证明L3失败。

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

probe就绪后只要求一个单城最小流程：使一类D3、W1，核对0.3→同一时代W2的0.6，再利用一个现有GPP百分比变化核对base被放大，最后撤销。全国getter包含其它城市；无法隔离时说明观测限制，不能以模拟倍率写原生PASS。该流程属于正式consumer阶段建议，当前先看上方单class接口门禁；不默认重测未改共享save/load。

诊断`W件｜领域D｜预计base/class｜配置｜可取得的原生读数/UNKNOWN`，右键映射/排除分页。Exit为小数基础率和原生倍率门禁、本地状态/通知回归、最小原生对应范围通过；否则仍partial，不宣布已实现。

来源：[正式Culture](../../Design/Content/Culture_D0048.json)、[Shared](../../Design/Content/Shared_D0045.json)、[旧基础GPP实现证据](../../Reports/Technical/Specialization_B035_Lv2_GPP.md)、[K检查点](P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)、[精度待办](Yield_Precision_Backlog.md)。
