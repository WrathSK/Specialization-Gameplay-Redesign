# P0-L3 — 巨作启迪自动能力

State: B172原生百分比API已获用户范围验收；B173通知修复LOCAL_SIMULATION_PASS，邻接能力联合实机观察未单独确认。当前Authority为Spec／Culture D0049 `CUL_L4_INSPIRE`，Shared D0045；实际部署与授权只查[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)。本页是实现合同，不另立Design。

## 当前切片与停止点

用户明确取消独立技术原型，授权直接复用花园／HD平伽拉的本城百分比原语并实施正式自动能力，再验收。B172.199本地完成；2026-10-09用户接受General/Prophet所示原生百分比响应与小数累计（scoped USER_GAME_TEST_PASS），精确叠加/来源归因不阻塞该API验收；[本地结果及一次最小验收](../../Status/Validation/Results/Specialization_B172_Inspiration_Automatic_Local.md)。用户随后授权B173馆藏通知定域修复，与启迪同一轮验收；[B173结果](../../Status/Validation/Results/Specialization_B173_Great_Work_Notifications_Local.md)。投资提交后传播修复仍独立未授权，M/N/U2及其它审计项不顺带推进。

### 现行合同

- Culture Identity、Potential IV且ACTIVE IV；沿用K已确认作品池。E为**当前**不同合格时代0–7，所有本城伟人类别+3%×E，E0不建载体，E7为21%。不依赖D、专家数、作品件数，不排除文艺类别；不新增项目、计时器、永久Property或点数账本，不启用旧Floor备用。
- 复用`MODIFIER_CITY_INCREASE_GREAT_PERSON_POINT_BONUS`：`COLLECTION_OWNER / EFFECT_ADJUST_CITY_GREAT_PERSON_POINTS_MODIFIER`，与Garden/HD Pingala定义相同。7个精确内部City Center载体各挂一个最终百分比，无class参数；不复制花园10人口条件或总督Promotion作为额外门槛，不修改HD、不直接ChangePointsTotal。
- 先撤旧再加新；移除/读取不明不混写，创建异常定域撤销并保留错误。same-reference UNKNOWN只保留本session确认投影；新引用/冷加载不从旧载体反推权威。旧B168四个测试ID由原模块自己的退役Withdraw处理，手动NEXT/END入口全部改只读，不能复活旧writer。
- K `Summary/RegisterConsumer`提供时代数与reference，沿用现有馆藏采集与验证，无第二套扫描。普通更新只读CurrentSpecializationFacts+小型Summary+7个owned存在性；不调用Shared D/完整作品副本/原生Modifier枚举。确认样本只更新changed城市；GovernorEstablished、投资、明确district/city通知定域；GovernorAssigned核受支持玩家旧/新城；签名不确定事件保留受支持玩家核对；原有本地回合边界一次fallback，不屏蔽同回合真实变化。
- 模块拥有派生记录、错误、待清理集合和一次合并pending范围；full audit裁剪消失城市，startup一次有界清理（复用被退役Probe的2048城防护），无诊断历史/独立GC。own写入只抑制本模块已知同步回声；Aesthetic/Meaning只忽略精确7个新内部载体的建筑事件，不忽略普通建筑。K使用具名独立通知及有限失败补投，见[通知合同](P0_K_Great_Work_Facts.md#馆藏消费者通知b173)。
- confirmed loss沿Store `IsExitTarget/RemoveOwned`撤本模块和旧测试精确ID；return/load按当前资格及新馆藏样本重建，不恢复旧百分比快照。UNKNOWN不能作失城确认。永久资产、其它城市/普通建筑和现行保存schema不变。
- P0“巨作启迪报告”左键简报、右键原生明细；没有启用/结束测试步骤。普通报告列当前E和**配置**百分比；UI按需列各类别原生**全国**率/累计6位小数，不能称本城贡献。右键复用有界实例枚举并包含city/player百分比来源、旧测试残留、未知归属；不相加推导有效总倍率。

### 验证与停止

B172按W0004 L2；B173为L3的通知顺序/会话引用定域修复，不运行无关历史全回归。B173当前测试入口`DevelopmentTests/test_great_work_notifications.py`：81方法44 subTest PASS，含真实三消费者/K与失败补投；通知成功不等业务/native成功。

以下为继承的B172结果：当前入口`DevelopmentTests/test_culture_inspiration_automatic.py`共43方法/46 subTest：24新自动路径，19直接依赖回归；实际Lua/SQL、K样本/请求、替换/撤销、冷重建、UNKNOWN/失城/失败隔离、40城定域计数及只读UI均LOCAL_PASS。计数不证明原生CPU/内存改善。

用户已接受现有General/Prophet的原生百分比响应、时代变化及小数累计证据，按所测范围记录USER_GAME_TEST_PASS。Scientist/Merchant基数归属、原生百分比叠加次序和普遍舍入算法仍为UNKNOWN，但不再要求先完整对账全国GPP才能验收该API；不据此调整玩法或添加补偿。原始观测/推算保留在[当前Status链接的结果](../../Status/Specialization_P0_Status.md#current-authoritative-state)。

B173通知修复仍保留对应LOCAL_SIMULATION_PASS；本次移动作品时风雅熏陶/意义延展的联合原生观察未单独确认，不将既有本地结果升级为新实机PASS。本条不追加人工流程，也不重复旧Probe保存→END→冷加载→再启用仪式。只有出现可重复的实际响应失败，或未来修改相关Modifier/来源路径，才按新增风险提出一次定域差分测试；精确引擎运算次序未知本身不阻塞后续开发。停止等待下一范围授权，不自动推进新能力。

## 来源与证据边界

- [Culture D0049](../../Design/Content/Culture_D0049.json)：能力、work_pool、inspiration合同；[Shared](../../Design/Content/Shared_D0045.json)：资格及一般生命周期。
- 本轮配置的只读DebugGameplay核对：Garden `GARDEN_ADJUST_GREAT_PERSON_POINT_BONUS` Amount20、`HD_CITY_HAS_10_POP`；Pingala `HD_GOVERNOR_EDUCATOR_LEFT_1_GPP_BONUS` Amount100；同city GPP百分比Effect。静态定义不是本批实机收益证明。
- [B168零档证据](../../Status/Validation/Results/Specialization_B168_Zero_Control.md)保留原结论；旧小数基础方案已由D0049替代，不是本批前置门禁。

## 历史：B167/B168旧基础GPP路径

以下保留当时计划及旧selector标题用于追溯；其中“当前/下一步/未授权”、0.1D×W、六class与Floor备用均属当时上下文，**不得作为D0049的新合同或当前派发指令**。旧调查结果与冻结记录不重写。

## B168当前修复合同

继承下方B167固定四ID／正常基础GPP／资格及owned退出合同。末档NEXT改为正常撤销并结束，独立END不变；失败不遗忘目标或假报OFF。只读原生接口和报告范围详见B168结果，UNKNOWN/归属/倍率不能猜测。

UI枚举只随READ／END／末档退出请求，32768定义／64Subject边界，测试与倍率各展开8、Subject最多2；只缓存一个token/reference/turn报告，不保留原生数组或增加周期/每帧扫描。正常小档推进不枚举原生实例。

原生计数限本玩家／Owner未知范围，城市原始对象保留不推断。倍率候选依据精确Effect与Scientist/未限定class，外国Subject未知不排除；有效总倍率继续UNKNOWN。本批不改SQL四值、原生来源或直接发点；外部API不可读不阻塞退出、不冒充零残留。

## B167当前原型合同

- 读取当前受支持玩家、当前可靠城市reference与Culture Potential/ACTIVE IV资格；固定测试值不依赖作品池或D，避免把接口失败与公式输入混在一起。正式六class公式仍复用K／Shared D，未在此原型假装落地。
- 原生路径：4个精确内部City Center建筑分别附加`MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT`，`Amount=0.1/0.3/0.6/1`，仅Scientist。加载定义检查类型、金额、类别及attachment；没有直接加全国总点数、没有替换HD来源。
- 单目标／单session，先撤旧再加新；重复token幂等，错误保留可诊断终态，移除失败不混写，UNKNOWN资格不清确认投影。确认失城由Store module-owned退出；reference改变清本模块并结束，不恢复原型；正常Governor/当地回合事件只核对当前fixture，无默认全城收益扫描。
- startup/load只对精确4ID做一次有界清理，外国城只清自己测试载体、不运行AI能力。缺load事件可由本地回合／请求完成；失败锁停，禁止无界重试；状态不保存、无新Property/ledger/GC。该新增原型生命周期由本地定向覆盖，不派重复OFF冷加载仪式。
- P0复用空闲测试按钮加独立END：左键准备/下一值，右键只读刷新；显示阶段、配置、载体数。UI只读原生全国Scientist/turn并显示回合，基线只在同城同session同回合比较；报告不得把配置或全国率称为本城实测基础率。原生可延迟一回合，保留读数与操作记录，延迟本身不是FAIL。
- 合计策略评估：同城同类一份最终量避免每作品实例／重复更新，数学上不舍入时等价；这不证明特定原生carrier精度或非叠加问题已解决。备用`floor(D×W/10)`如D3/W4为1，逐件Floor为0；只在原生门槛结果明确后进入正式接入方案，不在本轮暗改Gameplay。

## 下一最小批次 — L3-A 单城单class原生门禁

**L3-A已获用户授权；完整六class自动能力仍未授权。** B166自动接入验收后，用户授权先测试小数，并允许按本城每类总量Floor作为备用。只验证原生基础GPP接口，不直接交付完整六class能力，不因Design接受自动启用全国writer。

- 选已有Culture ACTIVE IV城与Scientist一类；先复核当前city/district基础GPP Modifier，保留HD／原生基础来源。最小可逆probe依次配置0.1、0.3、0.6，按需读取本城per-turn基础贡献／速率及实例；必要时用当前可观察的正常GPP百分比核对倍率。数据库字段接收小数、carrier存在不算原生生效。
- 门禁原型的固定值是接口对照；正式能力仍0.1×对应D×合格W，不能用Gold份额、专家或时代数替代。本轮不启用Floor，备用条件见下方当前合同。未知原生字段明确UNKNOWN；不能用全国点数总值冒充该城基础率，不能直接发点数或建小数余量账本。
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

0.1是正式Design值但技术待确认。用户本轮另外授权每城每类总量Floor作为备用，先测试小数，不直接启用或改正式来源。科研floor、Boost round、旧GreatWork量化及HD per-population小数先例不能跨接口当证据。

## 已核对的接口

- 当前`Lv2GPP.lua`+`Building_GreatPersonPoints`以每工作专家+2的整数基础来源工作，之后让原生GPP百分比生效。这是可复用的资格/载体/退出结构，**不是0.1路径已通过**，也不能把新能力塞入专家人数编码。
- 此前准备调查只读已配置DebugGameplay缓存：PointsPerTurn声明INTEGER；`MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT`和city district GPP路径有`Amount/GreatPersonClassType`示例，两项相关Effect查询未发现小数Amount先例。SQLite类型声明/未找到先例均不足以证明引擎不支持小数。
- 候选先验证原生city/district `Amount`基础来源是否忠实接收0.1/0.3/0.6并吃倍率；再判断building GPP字段是否存在可行路径。不能用player全国一次性点数代替city基础来源。
- K `Summary`及B150以后的确认通知已包含count、排除数与类别未知，当前`GreatWorkFacts.sameInput`完整核对这些字段。同一时代W1→2通知可复用，不新建collector；L3接入仍应定向验证消费者重算与L1未变零写。

## 分步实施建议

1. 下一轮获得授权后先做真实Lua纯模型/小数SQL配置与一个最小原生GPP probe；单城单class隔离，记录预期base与native per-turn rate/正常倍率。探针有独立退出，不把未知配置当正式能力。
2. 原生门禁通过再接正式ACTIVE/D/W模型与module-owned派生writer；参数集中为GPP_K，禁止多个Lua/SQL各硬编码。没有新永久成果或每回合奖励事务。
3. 复用现有事实和E2 RegisterExit/Return，load重新派生；Lv2GPP原有owned列表不与L3混用。测试看增量，不能因HD原有基础/其它城市点数叠加把全国总率当选中城市贡献。
4. 如果原生精度/正常倍率不满足，停止该接口，报告TECHNICAL_INVESTIGATION_REQUIRED；要求改值或量化才向用户提DESIGN_DECISION_REQUIRED。本次测试不启用Floor；若确需启用已授权总量Floor备用，须在随后正式接入批次显式同步合同，不能静默套用逐作品Floor、跨类合并、累计发点或额外Faith转换。

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
