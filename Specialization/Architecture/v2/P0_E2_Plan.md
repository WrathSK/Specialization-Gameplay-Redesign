# P0-E2 — 进度保存适配：具体计划

Status: PARTIAL_IMPLEMENTED / B111_SCOPED_USER_GAME_TEST_PASS. B109 slice1 accepted; authorized B110 snapshot implemented locally; Claim/lifecycle/F remain unauthorized.
Baseline: B107.134 / modinfo134, implementation c5bb3d9, native evidence d3ab809. D0035/A0161; four-profession v0.1 only. Earlier B094–B106 sections below are chronological historical plans/results, not current task dispatch.

## Current slice — recovery and action routing

旁路验证：B112观测已限定验收；B113按钮/条件过回合已获用户授权，见[当前原型合同](../../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#12-b113140--guarded-next-turn-button-prototype)，不授权正式项目/Claim。此前B112[范围、实现、证据与最小测试](../../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md#11-b112139--native-blocker-observation-prototype)。只观察、不强制、不建项目；不扩大本E2保存/Claim切片授权。

**B109三城及冷加载已验收；用户已授权的首次AI征服快照完成B110本地实现，B110原生读取失败已由B111修复；双城分流与完整重启现已限定验收。** snapshot分流已授权；Claim操作、销毁/位置复用、未专业城夺回、F仍未授权。当前本地人类单人、四专业范围不变。文档维护授权不等于继续玩法实施。

本次[B108两图失败证据](../../Status/Validation/Results/Specialization_B108_E2_Initialization_Failure.md)保留原结论；[B109修复及当前支持范围](#b109136--start-enabled-initialization-repair)覆盖此前IsSavedGame门槛。支持从开局启用Mod的新局及其正常存档，不承诺中途加入Mod或旧开发存档兼容。[三城可见状态已确认](../../Status/Validation/Results/Specialization_B109_E2_Three_City_Result.md)；[用户现已确认三图拍于完整重启读档之后](../../Status/Validation/Results/Specialization_B109_E2_Coldload_Confirmation.md)，本次三城检查点关闭。E2报告左键读取，右键事件翻页，不要求右键重测。

### 默认恢复 / 验收

先看Status CURRENT与Authority，再读本节及下列完整B108合同/结果：

- [B108保存、旧writer切换、失败/回滚合同及三城测试](#b108-authorized-new-game-multi-city-cutover--contract-before-implementation)。包含新档资格、UNKNOWN/旧档不写、部分写入保持HELD、原生初始化未证实、最小三城一次冷加载流程。
- 当前验收只需要该流程、用户本次材料及相关Status；缺截图不能说已重看，用户陈述与图像证据分开。归档不自动授权修复。
- 已记录部署引用在Status/Authority；普通问答不读取外部包，涉及部署恢复才核receipt与实际包。

### 实施依赖与按问题展开

[P0-E2 manifest](../../Workflow/P0-E2.json)的context是**实施依赖上界**，不是每次恢复/问答必读全文。当前授权范围及完成结果见[B110检查点](#b110137--authorized-conquest-snapshot-checkpoint)；不自动进入后续Claim。下一授权若改变切片，先更新适用集合，不能永远追加历史。

| 触发 / 直接合同 | 阅读范围与用途 |
|---|---|
| 修改当前保存/投资/注册 | 完整B108合同＋正式Spec SCOPE/ELIG、PROG＋总计划Migration/cutover合同；manifest保留的完整直接源码/测试；精确核对writer入口及消费者，不以hash替代cutover审阅 |
| ownership退出/夺回或Native顺序异常 | [B096模块自有退出清单](#b096123--confirmed-ownership-loss-scoped-exit-checkpoint)、[B097逐类永久/派生state](#b097124--原玩家同城夺回-partial-checkpoint)，再读B101/B102/B103后续修正；这些阶段上限/待测状态可能已过时，不能反向覆盖B108 |
| founding或事件收尾问题 | [B105原生反证](../../Status/Validation/Results/Specialization_B105_E2_Event_Boundary.md)、[B106正面建城证据](../../Status/Validation/Results/Specialization_B106_E2_Found_City_Pass.md)、[B107实现](#b107134--authorized-positive-founding-registration-implementation)及其原生结果；不得恢复“首个Publish即事务结束”假设 |
| 既有测试fixture/兼容断言失败 | 对应历史阶段＋直接test依赖；历史adapter不是生产旧档支持承诺 |
| 讨论后续工作 | [B110当前检查点](#b110137--authorized-conquest-snapshot-checkpoint)；原快照计划已授权并完成本地实施，Claim及其它后续仅建议，不派工 |

跨Owner永久成果仍逐专业定义；未实现的学术传统、文化永久ledger、商业合同不补造。名字/单独坐标/猜CityID不能证明同城；失效与临时UNKNOWN分离。旧实验代码可保留作反证/fixture，正式入口是否启用以当前切片与源码为准。

## Historical plans and scoped evidence

以下按形成顺序保留；不是整体默认读取集合。旧实施状态与测试任务由上方当前切片覆盖，仍适用合同经上表可达。

## 当前单人范围澄清（用户确认，2026-09-21）

当前实施只有本地人类玩家参与；AI、自由城市不启用Specialization，也不支持多人。AI/多人不增加当前依赖、测试或计划工作。此为当前配置/scope，不改写ELIG-001～006保留的未来通用资格，不把系统永久设计成Human-only；本轮Design字节保持不变。

### 已有Authority，不重新发明规则

| 路径 | 当前明确规则 | 依据 / 技术待办 |
|---|---|---|
| 玩家城失去所有权：自由城、交易给AI、被AI征服 | Identity/Potential/明确永久投资成果保留；全部本Mod效果休眠，连Lv1也不生效；不能投资，无AI专业循环或网络 | ELIG-004/005、PROG-004；需要保存与失效技术实现，不是待定Gameplay |
| 玩家夺回自己的原专业城 | 恢复原Identity、Potential和明确永久投资事实；不重新花Settler、不进入Claim；ACTIVE按当前总督、Network按当前路线重新计算 | PROG-004、ELIG-005；原城市连续性仍需验证，不以城市名/坐标单独认领 |
| 玩家首次征服没有专业历史的AI城市，有合格已完成区域 | 转移完成时一次冻结四专业去重LegacySet；提供候选Claim，可一直不选；后建区域不追加候选/不自动锁专业 | PROG-006/007；完成任一Claim锁Identity/P1，其它Claim退出（PROG-008） |
| 同上，LegacySet为空 | 无Claim，从征服完成后监听首个合格区域完成，锁Identity/P1 | PROG-009；未完成区域不入snapshot，之后完成可生效 |
| 旧档已丢记录/未知历史 | 不可把UNKNOWN当“确定无专业历史”的AI城 | 旧档初始化独立OPEN；不得借Claim补造丢失专业 |

修正上一轮讨论：原城Identity/Potential恢复与无专业AI城征服初始化早已有Design，并非必须由用户重新决定。Claim精确成本仍TBD，未来实施该入口时单独处理，不阻塞同Owner保存首段。本次用户明确的交易场景是**玩家失城给AI**；不擅自把未专业AI城交易给玩家等其它取得方式扩展成已经冻结的征服snapshot规则。

各专业明确成果的scope依然独立：Culture Dialogue累计倍率/使用时代额度随城；文化见闻及考察记录属于原Owner+来源城，原玩家夺回可按条件重新生效。Industry自身模板与实际完成Wonder归属不同，不能把当前拥有的Wonder当历史完成信用。Research学术传统的离开Identity暂停规则不等于新的征服时间规则。当前外方持有不运行能力、投资、累积工作或后台专业更新；将来引入长期时钟/合同必须显式处理未启用期间，不凭加载时差补算未经批准的成长/收益。此处不替未来合同结算/Team遗产作决定。

### 对E2计划的实际调整

保留首段“一座同Owner完整旧城：迁移→继续投资→读档”的窄授权单元，它是技术依赖，不是最终只支持永不易主。其后的计划顺序明确为：

1. 当前E2首段：同Owner进度/投资保存切换。
2. E2后续收束：**玩家失城→外方休眠→玩家夺回**的保存/效果撤销/恢复；既定Design不再标为未决，只验证实际事件和支持存档。
3. 独立征服初始化批次：**首次征服AI城**的snapshot与Claim/普通完成互斥；不挤入首段，先提出具体UI与成本边界计划。新自建城接管也须单独完成总计划剩余项。

以上均需各自审核/授权，不自动实施；无需AI自主投资、AI能力收益、多enabled竞争或multiplayer协议测试。

### 失去所有权必须真正关闭效果

只让AI不跑Audit并不充分：已有technical Building/Modifier可能仍留在城里。未来实现必须建立一次性、定域的退出清理路径，按旧/new city reference检查本Mod旧效果，撤销Local、专家支持、Network source/receiver、折扣及相关carrier；不可删除普通建筑或永久账本。清理不因newOwner未启用而提前return，也不把AI城加入常驻扫描。确认清理失败须可诊断，不能仅返回UNKNOWN就声称“全部不生效”。具体writer/carrier目录在实施时按受影响模块核对；本轮未修改它们。

外方持有期间只保留可支持夺回的最少被动身份记录/定域生命周期观察，不维护外方ACTIVE、收益或专业网络。夺回时先证明同城，再恢复当前玩家读模型；不足则技术HELD，不能把永久成果删掉或把技术不支持写成新玩法。

当前runtime `Probe.IsTestPlayer`只检查测试文明/领袖，不检查Human/local资格；这不是当前范围已被代码完整保证。后续首段要核对本地单人玩家门槛并统一路由，拒绝AI/多人启用；禁止偷偷扩展AI实现。为对退出的外方城市做必要清理而访问它，不等于给它启用专业资格。

## 1. E1结论与本批切片

E1已验证：独立Game记录可保存；Gameplay直接识别所测单次自由城转移；B094冷加载恢复单城映射。仅此原型范围USER_GAME_TEST_PASS。正式多城cityKey、收复/连续易主/征服/解放/同地重建、转移中断恢复没有普遍原生保证。

因此不把E1实验编号直接升级为全局authority。本次推荐授权的E2首段为：**一座显式选择、原Owner/引用/旧凭据完整、已经建立四专业之一的城市，在同Owner范围迁移进度并继续既有移民投资，冷加载保持结果。** 其它城保持旧路径。

这是E2的受限首段，不等于总计划中完整新城/跨Owner保存适配全部完成。后续新城首次专业、全城登记、跨Owner技术适配仍需收束（夺回Gameplay已由PROG-004明确）；不因首段PASS自动进入F。既有能力计算不改，既有收益仍由原consumer写入。

## 2. 实际读取链与必须接管的边界

| 当前模块 | 实际职责 | 本段处理 |
|---|---|---|
| BindingProbe | Game每Owner总账+City token；CityBuilt分配DEV序号（上限32） | 未迁移城保持；已登记城/位置及转移待确认范围先由新保存路由拦截，禁止当新建城再分配 |
| CityJournalProbe | 首个合格专业区域锁Identity及基础Potential1；City记录 | 已迁移城的事件/加载/故障GAP写入跳过；保留冻结来源，不双写 |
| FreshBindingHook / CityFlowProbe | 串接新城Journal；三阶段提交、load resume、SupportFacts | 新城仍旧路径；已迁移城所有写入口/resume提前跳过，避免冻结旧记录触发player-wide halted |
| EffectiveFacts | Flow基础Potential + 已完成投资凭据数；Governor产生ACTIVE | 接入唯一保存路由：迁移后只读新记录；旧路径仍服务其它城；接口输出与收益语义保持 |
| InvestmentAction | Prepare/Confirm、INTENT→单位标记/销毁→CONSUMED_CONFIRMED→receipt；load finish | 对迁移城替换读写后端与revision校验，保留单位消耗和receipt语义；旧City ledger不再写 |
| CurrentSpecializationFacts | EffectiveFacts只读外观 | 复用，验证UNKNOWN/mode不会被解释成NONE |
| NetworkInput / SampleLifecycle | 直接读旧token，Network还有“无Flow=未追踪城”分支 | 使用新路由的引用/参与状态检查；迁移有效城不得因旧Flow缺失被判NONE，HELD不得走新城默认值 |
| SourceYieldProbe | 直接读取CityFlow.SupportFacts | 迁移城改读统一基础事实，未迁移城保持；不得继续越过路由 |
| Standardization/模板及其它永久成果 | 独立专业ledger，并非全在EffectiveFacts中 | 本段不迁移模板/Dialogue等；不得声称易主后完整保存。所有权不推导 |
| CityInheritance / InheritanceShadow | 被隔离旧继承writer | 保持隔离，不调用Start/继承projection |

已完整阅读Journal/Flow/Investment/EffectiveFacts/CurrentFacts/FreshBindingHook，核对Binding写入段与Gameplay启动/分发，搜索所有直接旧key读取点。正式实施前按W0001补读精确受影响消费者，不默认全库重审。

## 3. 新保存authority：小型专业进度记录，不建通用框架

拟一个独立版本化Game Property `SPC_CITY_PROGRESSION_V1`，由一个Gameplay模块持有。本段只允许一个显式登记的测试城；后续扩容另审，不创建每帧同步或第二份可写历史。

- root：schema、revision、单城record；new key不存在不等于迁移成功。
- stable record key：由已验证原DEV token在本存档命名空间确定；仅支持本段受控登记，不宣称任意城市永久ID。
- origin/current reference、迁移来源owner/token/关键revision与来源摘要；原锚点固定，当前寻址单独保存。
- progression：Current Identity、Permanent Potential、first事实、mode；UNASSIGNED/SPECIALIZED/REALLOCATING区分。首段只导入SPECIALIZED；REALLOCATING仅合法类型和拒绝错误分支的合同，无创建Action。
- historical maximum：只记录已有证据所支持的下界及provenance，过去更高值未知，不把当前P伪造成完整历史。未来投资更新当前专业已观察最高值。
- investment：原receipt→unitUID集合、revision、可选pending；无单位/UI/carrier作为唯一authority。Potential与凭据数量必须一致。
- migration state：PREPARED / ACTIVE / HELD，与Gameplay mode及事实validity独立。ACTIVE这里指存储接管状态，不是专业ACTIVE等级。
- 专业ACTIVE不持久化，仍由当前Governor和Potential计算；数据暂不可用≠等级0。

Game记录随save恢复，不用外部文件/城市名称作key。单位删除等引擎副作用不是一次Game Property写入所能原子覆盖的，保留现有失败暂停语义，不承诺任意崩溃exactly-once。

## 4. 明确导入合同和切换顺序

可导入：当前原Owner、当前引用/token/Binding唯一匹配，Journal TRACKING、Flow DONE且逐值一致、四专业Identity及基础P1、投资receipt有效且无pending。首测优先Research P1–P3，以便在同次测试继续投资；P4可本地验证导入。

拒绝：未专业化/无追踪旧城、City记录已因易主丢失、任何pending/GAP/冲突、缺失历史、原Owner改变。**E1记录/截图/当前建筑不能代替缺失旧账本。** 有模板不代表本段导入模板；原模板继续其原Owner路径，不复制/扩散。

顺序：
1. 手动请求，读取不可变来源快照，验证资格；没有新效果，也不消耗单位。
2. 写新key PREPARED（完整目标及来源锚点），读回确认；从PREPARED开始所有目标城旧进度writer必须暂停，避免来源在切换中继续变化。
3. 再验证来源未变、目标仍同一城、无单位事务；提交ACTIVE并读回确认。
4. 统一read route切到新记录，旧City值冻结留作证据，不删除、不写回、不作为自动fallback；不发布虚假的0或重复收益。
5. 重复导入返回已完成，revision不增。PREPARED读档仅在同Owner/来源完整一致、无任何副作用时允许完成原导入，否则HELD；记录损坏、schema不识别、来源改变不自动重建。

失败后不能自动回到旧writer。切换marker与目标记录必须在同一Game值内，避免多key提交顺序造成两个authority。Gameplay初始化必须在旧writer/旧load hook可以运行之前恢复路由；恢复未就绪时暂停目标写入，不将缺读解释为未迁移。

## 5. 迁移后继续投资 / 发布

Prepare读取路由提供的同Owner事实、record revision、receipt集合；不依赖冻结City ledger判断新投资是否变化。Confirm再次验证，沿用原INTENT/单位标记/销毁确认/receipt提交顺序；每步只写新后端，保持原消耗规则与Potential上限。

读档：已确认消耗凭据可幂等完成；INTENT无法证明消耗则HELD，不自动销毁第二次或增加Potential。不放宽原单位ID复用保护。旧load恢复循环必须跳过迁移城，不能双finish。

更新后复用既有事实变化通知，只有Identity/Potential/ACTIVE或相关输入实际改变才发布。迁移前后相同事实不产生额外carrier churn；Network继续共享derived view，引用加入保存generation/revision时只在需要的事实边界失效。无hover请求、无generic pulse保存/扫描。

## 6. 易主和未支持范围

当前AI/自由城Owner不获得本Mod效果或投资资格；永久成果按ELIG-005休眠保留。本段暂未实现玩家夺回时的自动恢复，不改变PROG-004恢复规则。迁移城发生已确认移除/易主后，Game记录保留，路由变为HELD_TRANSFER；旧source资格按真实owner/reference失效退出，不继续凭旧owner激活收益。当前读取失败不能冒充已确认失效。

只识别同一坐标不足以领回历史；新Owner/收复时均不自动重锚专业账本。E1V2保留为独立实验，不在正式读链作继承许可证。对于已登记位置出现CityBuilt（可能是易主），先暂停新旧首次建立入口，不把它当从未专业化城市；本段不解决该位置后续真正新城的自动登记。

必须本地证明：目标暂停不污染同player其它城市的旧bucket，不触发误清除无关城；确认失去owner/reference时不会残留其正式来源效果。若现有consumer不能区分临时UNKNOWN与已确认退出，实施时扩充必要的明确失效出口，不能靠统一抛错隐瞒。不得将已明确的PROG-004/006～009重新列为待定；仅超出这些规则的真实新Gameplay边界才报告，不替用户补Legacy。

## 7. 最小文件范围

当前单人/仅玩家资格需核对`Probe.IsTestPlayer`与现有调用入口；只收紧当前启用范围，不新增AI/多人实现。拟新`CityProgressionStore.lua`（或相同职责小模块）；ADAPT EffectiveFacts、InvestmentAction、Binding/Journal/Flow目标城门禁、SourceYieldProbe和NetworkInput的直接旧存储判断；SampleLifecycle只在引用语义确需时改。Gameplay负责正确初始化顺序和手动导入/摘要诊断；复用现有实验按钮位置、同步旧Tooltip，不新增诊断面板。

收益SQL/carrier/Research公式/Design不变，CityIdentityMapping实验仍独立。旧writer不是全局删除，而是对迁移目标先停后切；其它城市旧行为不变。完整E2新城接管不塞入本段。

## 8. 验证：W0004 L3，仅受影响链

| 本地定向项目 | 验收 |
|---|---|
| P1/P2/P3/P4真实旧fixture导入 | Identity/P/first/receipt逐值等价；ACTIVE按Governor重新计算 |
| PREPARED/ACTIVE重复、重入、冷load、读回失败 | 单authority；不覆写冲突、不丢凭据、不自动回退旧writer |
| 移民投资/重复确认/单位ID复用/两阶段中断 | 只正确消耗一次；不确定阶段暂停；旧City ledger零新写 |
| 同玩家一迁移城+一旧城 | 路由分离，旧城正常；所有写入口/load/GAP/恢复不可漏 |
| 直接旧key读取回归 | Network不伪造NONE，SourceYieldProbe不越过路由；旧样本版本安全 |
| SAME事实与idle/重复通知 | 无新增carrier写/全城扫描/周期请求；新key状态变化才写 |
| 真实投资/Governor/owner事件 | 输入正确发布；UNKNOWN保留边界与confirmed withdrawal分开 |
| History / REALLOCATING fixture | History不等于Current，REALLOCATING不能进入NONE首次建立 |

全Lua/manifest/context、受影响收益/Network/投资/部署安全检查。无需机械重跑所有历史；针对持久中断与重复操作做有限压力/故障注入。原生版本环境同时覆盖缺少table.unpack，避免B093重复。

## 9. 实施后一次最小用户测试

一个独立测试档，一座完整旧科研P2或P3城市，另有一座旧城作为对照：按需迁移→看同样Identity/P/ACTIVE和已运行收益→用既有移民投资一次→另存冷加载→同一简明诊断确认新P、凭据数、存储来源；对照城仍旧路径。一次流程涵盖保存切换与单位事务，不要求用户手算hash或全模块收益。

不默认重复自由城实验；实际易主后的正式玩法不在首段验收。若实现需要原生特定失效证据，本地先缩小后再提出，不能把范围扩成长期综合测试。

## 10. 退出 / 回滚 / 授权

首段退出：目标同Owner记录和投资读写正式由新Game记录承担、旧writer目标零写、收益逐值一致、冷加载成功；未迁移城不退化。报告明确USER_GAME_TEST与本地模拟边界。

回滚使用B094完整包和**迁移前独立存档**。新投资后旧City账本已冻结，不能用旧包继续该档并声称无损；不提供自动反迁移。新key保留不清理，保留所有证据。

无新的Gameplay设计问题阻塞这一个受限切片。需要用户审核的是上述**E2首段scope**；跨Owner/新城/全量兼容仍未包含。通过首段后先报告E2剩余边界与下一计划，不自动进入F。

本轮只计划，runtime/Design/main/运行包均不改，无部署或Gameplay regression。

计划检查：现有context.py CLI的batch枚举尚未包含E2；本轮直接调用同一工具的check(manifest)完成全部schema/hash/authority检查，PASS（151 runtime files）。未修改工具逻辑；实施时只需将E2加入既有CLI枚举，不建立新验证器。git diff --check通过；本轮无Gameplay测试。


## B095.122 — 首段实施检查点（未完成，不部署）

用户补充：v0.1只开放Research/Culture/Industry/Commerce四专业区域；领域词汇/分派结构允许未来扩展，但本批不启用其它专业、不实施其玩法。`P.Families`四项不变；新保存导入明确只接受这四种Identity。Design/A0161不变。

### 已完成部分 / STATIC_CONFIRMED

- 新`CityProgressionStore.lua`单城、版本化Game Property `SPC_CITY_PROGRESSION_E2_V1`：原Owner/reference、基础Identity/P1、投资ledger/receipts、导入绑定证明；PREPARED→ACTIVE读回确认。不是外部文件，不以城市名作key，不是全局永久cityKey。
- 最多一个目标；初始化先于旧Binding/Journal/Flow；手动导入检查完整旧凭据且无pending。重复导入no-op，未知schema/来源变更/写入失败暂停；不补历史、不回退旧writer。PREPARED可在同Owner完整来源不变时读档完成。
- 已导入目标的Binding/Journal/FreshHook/Flow写入、GAP和load resume全部旁路；Flow.SupportFacts转读新base（SourceYieldProbe也经此路由）；EffectiveFacts从新ledger求Potential，并沿用当前总督求ACTIVE。其它城继续旧后端。
- InvestmentAction保留INTENT→单位标记/销毁→CONSUMED_CONFIRMED→receipt；目标仅写Game记录。目标故障不污染其它城市，未迁移城保留原player错误桶。Network禁止将受新路由管理的缺失旧Flow当作NONE。
- 复用两按钮：迁移进度左键旧记录只读、右键导入；进度保存左键读取新摘要。旧E1请求仍保留为独立证据入口，不作迁移凭据。
- `IsTestPlayer`加单人/人类门槛；原版UI的PlayerConfigurations:IsHuman、GameConfiguration.IsAnyMultiplayer提供静态API依据；原生Gameplay-context可用性仍需实机。未知接口fail closed，不退回AI启用。
- 无SQL/carrier定义/收益公式修改；无新周期扫描/hover request；新保存模块只在明确操作、load及城市生命周期事件访问单条记录。

### 本地证据 / LOCAL_SIMULATION_PASS（不等于Civ VI实机）

`DevelopmentTests/test_p0_e2.py`运行真实Lua保存/旧writer/EffectiveFacts/投资执行器：四专业×P1–P4共16种导入；重复/冷load；总督重算；真实旧回调目标零写；一新后端城+一旧后端城；移除旧账本仍读新记录；投资只消耗一次及幂等；单位ID复用；各写入失败窗口；PREPARED恢复/来源变更拒绝；未知schema；不接受MILITARY/REALLOCATING/GAP；迁移前后完整Network输入签名相同；无关通知不新增写；实际诊断dispatch。全Lua compile、modinfo inclusion与人类/单人门槛模拟通过。

模拟城市移除/引用变化仅证明保存为HELD_TRANSFER、保留账本和阻止旧城重新登记；**没有证明其所有实际收益退出**。HELD原Owner再出现时的Network旧view排除也仍须随退出合同收束，不等同于已经实现夺回。

### 阻塞 / 未完成项

按前缀批量移除`BUILDING_SPC_*`的尝试被自动审批拒绝（没有执行），原因：批量删除可能超出同Owner首段并破坏游戏状态。没有绕过审批、没有采用该清理路径。

随后只读确认：`ResearchApply.Audit`、`ResearchCross.Audit`、`ResearchChair.Audit`当前以`P.IsTestPlayer`过滤整个player，在AI接城后跳过；不能仅靠资格收紧宣称旧载体已退出。部分其它模块已有自己的清理逻辑，但尚未完成四专业全部效果的逐项退出覆盖证明。

本段计划§6要求确认失去owner/reference时不得残留正式效果，因此不能把同Owner模拟通过当作整个E2 PASS。当前为**可恢复的partial implementation checkpoint**，不是可部署候选。

下一最小修补：逐模块明确其拥有的实际carrier/退出入口，对受本批记录管理、确认退出的单城执行模块自身退出；不按全库前缀批量删除、不清普通建筑、不清永久账本、不恢复新Owner资格、不实现夺回/Claim。补齐相关退出/重复/UNKNOWN保持/Network失效的定向模拟，再复核已有收益消费者。需先解决上述审批边界。新cityKey/全城迁移/夺回/Claim/F仍不在本轮已完成范围。

尚未运行完整affected-consumer/部署安全验收，因为退出实现尚未完成；没有USER_GAME_TEST，没有部署。B095.122/modinfo122仅为develop未完成候选编号，外部运行包保持B094.121。


## B096.123 — confirmed ownership-loss scoped exit checkpoint

本节取代上节“退出未实现”的当前状态；旧检查点保留为历史。用户已明确授权定域退出，仍为 E2 PARTIAL / NOT_DEPLOYED，不是整体E2验收。

### 合同

仅一座显式迁移城市；CityTransfered 的旧Owner、新Owner/CityID与保存原引用、当前实际对象同时匹配，才保存 `loss` 与 HELD_TRANSFER。UNKNOWN/缺失getter/无匹配事件不确认，不清空永久进度。按模块注册的明确载体清单退出，清单全部预检为InternalOnly再移除当前存在项，不枚举全城建筑或按前缀删除。每模块成功后不重复运行；失败隔离、每session最多3次事件驱动尝试，无timer/polling；诊断列暂停模块。保存的确认在读档后仍需匹配同一目标引用，才重新执行幂等退出。

NetworkBridge先使用原confirmed-invalid发布合同撤销原Owner的完整verified snapshot（不可分割），清除source/receiver projection并通知既有consumer；不是创建AI网络，也不是局部拼造有效view。原Owner剩余网络等待正常完整verified输入重新建立，其他玩家bucket不变。

### Module-owned coverage（精确InternalOnly ID，含旧载体tombstone）

| Module | IDs | 退出对象 |
|---|---:|---|
| ResearchSupport / IndustrySupport | 3 / 9 | 专家支持 |
| Lv2Housing / Lv2GPP / Lv3Support | 9 / 32 / 12 | 住房、GPP、旧支持载体 |
| Lv3Effects / Lv4Percent | 11 / 8 | 旧文化/商业本地效果 |
| ResearchInfrastructure / ResearchCross / ResearchApply / ResearchChair | 52 / 43 / 25 / 104 | 科研当前收益及各自退休载体 |
| CrewProjects | 1 | 施工项目临时准入；不删除已有队伍 |
| HalfYieldProbe / PurchaseProbe | 32 / 2 | 手动探针的已有收益载体 |
| CopyYields | 40 | 工业copy当前载体 |
| StandardizationDiscount | 596 | 折扣目录；只清目标 applied cache，不清模板 |
| NetworkBoost | 1126 | 既有正式/整数/测试Network载体 |
| GreatWorkProbe / Dialogue / GreatWorkAdjacency | 2 / 11 / 156 | 巨作探针、对话效果、旧邻接；不清历史记录 |
| CommerceConvergence | 48 | 旧商业汇聚效果 |
| NetworkBridge | — | 原Owner snapshot confirmed invalid |
| YieldCarrierProbe | — | 两个明确临时plot flags归零 |

21组共2322个唯一ID。只读当前DB核验ID存在、InternalOnly、无重复ownership；这是目录静态覆盖，不是实际游戏安装2322座建筑。ConstructionProbe的已结算Production不是持续buff，不能倒扣；UnitActions/InvestmentAction receipts、Standardization模板、Binding/Journal/Flow永久记录保留。DistrictPrecisionProbe未自动启用，其退休载体归ResearchCross；SpecialistSupport退休载体归Lv3Support。UI/diagnostics/只读facts不施加效果，无额外删除入口；单位、城市历史与其它专业永久ledger不迁移。

### 验证与边界

L3定向 `test_p0_e2_exit.py --db <readonly DebugGameplay.sqlite>`：真实模块退出闭包+实际保存协调器；全部2322个载体模拟撤销，普通Library/其他城/永久Game与City账本不变；UNKNOWN、错误事件、重复100次零额外副作用；真实Network失效发布（下游Audit在该集成模型中为通知断言替身）、其他玩家不变、无AI bucket；冷load确认/UNKNOWN保持、单模块故障隔离和3次上限通过。继承test_p0_e2.py的四专业×P1–P4导入、同Owner投资/读档/失败恢复/旧writer隔离；全Lua编译与modinfo通过。STATIC_CONFIRMED + LOCAL_SIMULATION_PASS；没有原生移除/引擎modifier撤销USER_GAME_TEST。

未扩展：没有已保存确认且原生转移事件到达时对象尚不可读时仍UNKNOWN，不通过位置猜测身份；事件排序完整性待后续确认。确认后的目标不可读会暂停，后续生命周期事件/读档可重试。无城市毁坏重建匹配、新cityKey、夺回恢复、首次AI城Claim、全城迁移或F。重启可重新尝试幂等退出，不在save中持久化“已删载体”以免绕过实际对象核验。现有held城不因重新归原Owner自动恢复。

没有发现需破坏永久账本才能退出的模块；原生RemoveBuilding失败会暂停该模块并明确报告，绝不扩大删除范围。当前checkpoint不部署；外部B094.121与main保持不变。


## B097.124 — 原玩家同城夺回 partial checkpoint

用户接受B096后授权的下一最小段；未部署，不含首次AI城snapshot/Claim、全城迁移、新cityKey或F。D0035与各专业Design Authority未修改。

### 身份与状态

仍只接受显式迁移的一城：已有HELD_TRANSFER/loss记录 + CityTransfered的旧Owner等于保存foreign owner、新Owner等于origin local human、新ID等于当前实际对象 + 原位置 + **当前City旧绑定token等于保存原token**。不以城市名、坐标、区域反推历史。token缺失、事件不匹配、区域引用不明/多个匹配、未结束投资、前次模块退出未全部确认均HELD。返回采用一条`current`与`currentFirst`引用投影；origin/base/investment anchor与receipt保持原始历史，新投资写回时仅转换当前引用到原锚点，不改receipt。`lastLoss`和returnEvidence保存一次最近证据，不建立无限历史。

原cityID可被别城复用，因此旧writer排他范围只覆盖登记位置；其它位置不会因复用旧ID被认领。登记位置无凭据的新城仍不能恢复。第一次取得无记录AI城不会进入本路径。外方→另一外方链、丢失token、销毁重建不猜测匹配。

ACTIVE继续由EffectiveFacts读取当前Governor事实，无旧ACTIVE存储/恢复。原专业区域的当前ID通过当前完整同type区域确认，保留历史first.turn；引用不明确暂停，不选一个猜测。正常consumer沿既有CityTransfered/后续相关事件重算收益，保存模块不创建carrier。

### 永久state逐项

| State | 本段处理 | 边界 |
|---|---|---|
| 四专业Identity/Potential/投资receipts | 原Game记录保留；按新current引用读回；后续投资使用同一历史账本 | pending debit不猜测完成 |
| Industry自身Standardization模板 | 显式导入复制现有模板，之后由Standardization自己的验证/写入路径路由至Game记录；旧City账本冻结 | 已在B096失城且未保存模板的历史不补造；只暂停模板读，不阻断基础身份恢复 |
| 模板后续学习 | 正常本城completion事件仍可增加；夺回城不使用BUILDING_ADDED_RECHECK按现存建筑补录，避免AI期间施工信用 | 原生completion事件覆盖需实机；非迁移城保持旧路径 |
| Industry工程传统/Wonder实际完成、source Team容量 | 当前对应D0032永久系统未实施；不从现存Wonder或单位创造历史 | 后续专业实现按实际完工归属，Team易主仍独立边界 |
| Research Academic Tradition | 当前F未实施，无可恢复时钟/age，不补算失城时长 | 以后遵循保留age/离开Identity暂停，不从征服时差推公式 |
| Culture Dialogue / 文化见闻 | 当前Dialogue.lua是旧瞬态馆藏倍率，不是D0029累计ledger；见闻系统未实施，本轮不伪造永久记录 | 未来Dialogue累计/era quota跟城；见闻original-owner/source-city，不能统一继承 |
| Commerce合同/信誉/pity | D0032长期系统尚未实施，保留明确deferred Legacy边界，不创建/激活 | owner/conquest/Identity-loss合同与信誉仍待对应专业审查 |
| Crew永久settlement receipts | 原模块保存，不删、不重发既有settlement | 不是恢复当前buff；无新单位 |

### 临时state与Network

模块自有RegisterReturn只使当前输入失效，不施加收益：Copy/Industry generation reset；Discount样本、报价、ACK等重置并dirty；Dialogue generation/test sample与GreatWorkAdjacency sample清空；投资preview取消；D缓存dirty；Standardization仅目标新引用pending清除，其它城pending保留。都是单次已确认事件，无新timer/hover/polling。

TradeRouteProbe既有dirty signal加入CityTransfered（保持该模块拥有信号）。NetworkBridge撤销旧view，等待带当前signal的完整路线样本；迟到旧signal响应被拒绝。没有把保存的旧routes/ACTIVE/收益作为恢复权威。新Network仍由既有Capture/derive产生；不建AI bucket。按现有player-wide sample合同清缓存，不永久删除其它城市账本或收益。

### 本地验证

L3相关范围，`test_p0_e2_recapture.py`：真实保存/EffectiveFacts/InvestmentAction，P3→失城→新CityID88/区域ID99夺回→当前总督ACTIVE1/3→冷load→继续投资P4→再次loss/return；原base/receipts/binding逐值保留；100重复夺回不增revision；错误Owner/ID/token/首次取得/未完成退出/未完成debit拒绝；旧ID被他城复用不认领。真实NetworkBridge新signal接受空当前路线、拒绝旧响应，旧城市引用不进入新view，无AI网络。真实Standardization读取保存模板、旧City Property消失不丢已存知识、不补录AI建筑、后续模板更新可保存；缺失历史只hold模板。

`test_p0_e2_exit.py`复测21组2322明确ID撤销、普通建筑/其它城/永久账本、UNKNOWN、失败隔离/3次上限；增加真实模块return hooks旧samples清空、无carrier重放；继承已有16导入、同Owner投资/保存/失败恢复回归。全Lua编译、modinfo/W0001引用检查通过。**LOCAL_SIMULATION_PASS / STATIC_CONFIRMED，不是USER_GAME_TEST_PASS。** 没有运行全部历史压力测试，没有部署。

### 未解决技术边界 / 下一门禁

- 当前绑定token在原生跨Owner/夺回时是否保留未验证；缺失则技术HELD，绝不复制token到新城强行通过。不承诺已覆盖全部征服/自由城/交易路径。
- 需在foreign持有阶段完成B096模块退出（同session或foreign存档load重验）；如果直接加载已夺回而未确认事件/退出完成，保持HELD，不重放猜测事件。正常已确认ACTIVE夺回存档可冷load。
- 原生RemoveBuilding撤销与正常consumer再施加、事件排序、工业completion路径需后续最小实机验证；本轮无部署，暂不要求用户测试。
- 缺少工业pre-loss snapshot只暂停模板；不统一迁移其它专业未实施/deferred成果。
- **尚不建议直接实施首次AI城snapshot/Claim。** 可另行准备独立manifest，但当前夺回闭环仍有原生身份/事件证据门禁；Claim不能作为解决这些问题的替代。本轮STOP，等checkpoint审阅。


## B098.125 — 单城 native ownership round-trip validation

仅最小按需诊断，B096/B097认领/退出/恢复规则不改。复用“E2往返”（原进度保存）左键请求，无需选城，读取登记位置；右键原UI证据保留。报告原/现引用和token、保存stage/revision、最近转移事件/候选/拒绝原因、永久Potential/receipts、当前ACTIVE、模块退出计数与移除读回、科研支持/住房/GPP实存载体、Network epoch/input/derived/current reference。按需输出相同文本到Lua.log `[SPC][E2_NATIVE]`。无新持久debug结构；每模块固定一份最近退出核验、一个最近转移/候选，冷load清空，保存的既有loss/current仍读取。报告的退出计数是本次加载内观察，不是完整历史；carrier presence/readback不是原生yield settlement证明。

### 最小用户流程（独立测试存档；不启动游戏代测）

1. 用一座**非首都科研城**，Potential≥2（建议3）、当前ACTIVE≥2，至少图书馆/大学及一名工作专家。可行时保留一条已知国内商路以观察Network变化。先另存`E2-before`；选城，右键“迁移进度”一次，再左键“E2往返”。记录报告+城市收益/专家读数。以后不再右键迁移。
2. 优先将该城交易给AI，再左键“E2往返”（不需选外方城）：必须HELD_TRANSFER，退出完成，目标科研载体0，旧Network不含已失城的source/receiver。另存`E2-foreign`，读档后再读同一报告，检查永久Potential/receipt数与token/实际owner；不迁移AI、不对外方投资。
3. 原玩家通过交易取得同城；不安排合格已就职总督。读取“E2往返”+城市收益：ACCEPTED、Identity/Potential/receipt原值，ACTIVE应1；Lv2住房/GPP载体应0（Lv1支持可正常回来）。确认当前Network样本/引用，不能恢复旧路由；如路线未发生可验证变化，Network新路线重建仍NOT_TESTED，不硬判PASS。
4. 若前三步通过，恢复合格总督并等正常就职一次：ACTIVE和对应现行收益应恢复，仍不得重新投资达到旧Potential。最后保留测试存档与报告/Lua.log即可。失城→外方save/load是本轮必需边界；可选夺回后再另存读档，不代替外方边界。

交易若无法取回，不要求耗大量回合或战争；暂停并报告，再决定替代路径。交易成功只覆盖实测交易事件链，不自动覆盖征服、解放、自由城。无路线fixture时明确Network仅观察失效/当前input，不能声称完整route-change PASS。已装Cheat只可用户操作准备fixture，不改Mods、不绕过身份token，不用Claim。

### Stop / 证据分级

token不连续或无法证明同城→TECHNICAL_IDENTITY_BOUNDARY；事件到达对象不可读/缺少匹配事件→EVENT_ORDER_BOUNDARY；退出报失败或外方仍有载体/本Mod收益→NATIVE_WITHDRAWAL_BOUNDARY；save/load证据缺失→SAVE_IDENTITY_BOUNDARY。看到UNKNOWN/拒绝立即保留报告与当次Lua.log，不自动复制token、改CityID、按名字/坐标认领，也不修Gameplay绕过。

本地：真实报告在foreign HELD读取两次，永久Game记录/载体写入计数不变；沿用B096/B097定向L3回归与全Lua编译、modinfo/dispatch/W0001检查通过。未跑全历史压力测试。新增诊断不改变验证Authority。

当前native observed facts、withdrawal、recapture identity、ACTIVE重算、Network重建、save/load：**全部PENDING_USER_GAME_TEST，既非PASS也非FAIL**。不得将本地模拟复制到native结果栏。尚不能据此批准首次AI城snapshot/Claim implementation。本批只准备/部署测试包，由用户执行原生游戏步骤，回传后逐项判断。

## 2026-09-22 — native test deferred / future enabled AI space review

用户将B098 native验证留待回家，见[PT009](../../Status/Playtest_Backlog.md)。本节是现有Authority/源码的静态审查与未来边界登记，不修改Design，不授权AI运行、多人、Claim或新的保存实现。当前四专业/仅本地人类玩家E2 checkpoint保持不变。

### Architecture intent versus current code

Spec ELIG-001–005已经区分Specialization-enabled资格与Human身份；未来明确启用AI不要求AI planner或行为重写。当前单人范围不是永久AI禁令；本轮也不开放多人。PROG-004/ELIG-005支持城市Identity/Potential/明确永久投资成果随城市保留。因此未来enabled AI若通过合法投资入口完成投资，原玩家夺回不应倒退为自己失城前的Potential快照。只有真实提交的投资才是成果；AI普通移动/生产不会因此自动调用自定义投资Action。

当前实现并未完成这一多Owner写入能力：`Probe.IsTestPlayer`要求Human/测试文明/非多人；`CityProgressionStore.active()`要求`pid == root.origin.owner`，`current.owner`同样限定origin；投资投影写回原始anchor，单城单账本没有支持多个enabled Owner依次写入的完整协议。外方持有统一HELD_TRANSFER，不为AI运行投资。`UI/BackgroundRoutes.lua`样本来自本地玩家，不能将现有按player分桶视作AI路线采样已支持。故不能只放开Human过滤便宣称AI可用。

### Permanent achievement scopes remain specific

| State | Existing authority / future boundary |
|---|---|
| Identity / Potential / valid permanent investment | City development; enabled-owner转移保留，当前ACTIVE/Network重算。未来需保留投资行为的owner/action provenance并允许合法现Owner提交，不能用原Owner旧副本覆盖后续投资 |
| Industry own learned templates | PROG-004城市永久成果；当前E2保存原模板，外方不学习。不等于接收方临时Network模板union可继承 |
| Culture observations / mission completion | D0029明确original-owner + source-city分账；A/B记录不混合，夺回恢复自己符合条件的账本。正式系统尚未实施 |
| Culture Dialogue | D0029明确city-scoped累计倍率与START-era quota随城；不能把所有Culture资产统一改成按Owner独立 |
| Research Academic Tradition | D0031明确Identity-loss暂停/保留/恢复年龄；多Owner征服时独立分账未冻结，A0160也明确不补造Conquest Legacy。用户提出的分别积累记为未来Design审查方向，当前没有实现该计时ledger |
| Industry Wonder credit | 实际完成文明归属，不因现Owner变化重写完成者；不能类推为普通城市投资 |
| Commerce contracts/reputation/pity | 既有ownership/Legacy deferred仍保留，不借此次讨论统一继承或分账 |

Architecture的city progression、per-domain achievement records及current derived state分离，为此保留空间；它不是已实现的通用多Owner系统。未来最小适配点是：enabled-player资格与human UI权限分离、合法现Owner的城市投资提交与provenance、各成果明确key/scope、enabled→enabled与enabled→disabled转移分流、AI可用事实来源。无需AI决策优化或通用Legacy框架。Research分账等未定Gameplay须另行确认；城市身份跨ownership原生证据仍受本次待测门禁约束。

证据：STATIC_CONFIRMED（上述代码门槛/权威定义）；没有新增LOCAL_SIMULATION或USER_GAME_TEST结论。本轮只记待办和调查，不改runtime/Design、不部署。

## B099.126 — authorized eligibility regression repair

Scope: use `Players[pid]:IsHuman()` (original Gameplay scenario/API-supported Player method) instead of configuration-object human detection. Keep test civilization/leader and explicit singleplayer gates; unknown APIs remain rejected, AI/multiplayer not enabled. Do not infer human identity from player0. No ownership/ledger/migration/claim/ability formula changes. Gameplay request ingress publishes a fixed latest ERROR+request token+reason when eligibility rejects; UI uses existing error renderer, with no new polling/history/requests. UI-side rejection also explains the failed check.

Evidence: STATIC_CONFIRMED original Player.IsHuman use and context API reference (linked in B098 failure review). Native API return from the failed Mac session not captured; the exact B098 failure remains a supported regression candidate until user retest. Targeted L2 plus directly affected E2 state regressions LOCAL_SIMULATION_PASS: actual Probe with configuration IsHuman absent/throwing; Player true/false/missing/invalid/error; nonzero human ID; multiplayer/unknown mode; actual request ingress and actual UI error rendering. Same-owner import/investment/coldload, owned-exit/UNKNOWN/permanent preservation and recapture/currentGovernor/currentNetwork tests pass. Full Lua compile/modinfo passed. No full historical regression or new stress campaign.

Minimal user check after deployment: confirm B099.126 header; select one own test city and read 城市专业/潜力、总督条件、专家与岗位. Reports should ACK with real data; observe existing ability effect. Do not repeat migration to repair missing reads. If basic checks pass, existing one-city E2 ownership test can resume; ownership/save/load/native withdrawal is still pending and not certified by this fix. If rejection persists, report its concise eligibility reason; do not silently open AI or guess Player0.


## B100.127 — authorized bounded ownership diagnostics

Only the diagnostic gap identified in the B099 cold-load/conquest report is changed. No binding copy, matching-rule relaxation, new cityKey, Claim, Legacy or Gameplay change. Existing recapture remains held if the native identity evidence is missing; this is **not a recapture fix**.

E2往返 now reports live binding MATCH/MISSING/MISMATCH/UNREADABLE; STILL_FOREIGN versus WAIT_MATCHING_TRANSFER_EVENT versus the existing RETURN_* rejection; the latest matched candidate; and each failed exit's module, bounded reason and attempt count. Network current input is shown only if live owner equals the queried owner and the exact NetworkInput reference matches. A foreign same-ID city cannot display an unrelated local city's input.

Five fixed session-only event slots record the latest CityTransfered, CityConquered, CityAddedToMap, CityRemovedFromMap and CityInitialized: sequence, turn, argument count and first six scalar parameters. No table payload/history/persistent writes; strings/objects become type labels. Sequence enables ordering comparison but is not a complete timeline. Diagnostic observation is protected by pcall and cannot prevent the existing lifecycle callback. CityConquered observes only; it does not invoke reconciliation/recapture. Reload clears observations. Reports remain on-demand; no new polling, hover requests, audits, writes or file logging.

W0004 L1 diagnostic scope; directly related E2 state regressions retained because observation wraps a transfer callback. STATIC_CONFIRMED: unchanged saved schema/identity predicates/withdrawal writer paths, exact-reference Network guard, all Lua syntax and modinfo inclusion. LOCAL_SIMULATION_PASS: test_b100_e2_diagnostics + test_p0_e2 (same-owner investment/recovery); test_p0_e2_recapture (current governor/routes and rejected ambiguity); test_p0_e2_exit with read-only native DB (21 owned sets/2322 IDs, UNKNOWN/retry/duplicate preservation). New cases include foreign same-ID isolation, stale same-owner reference, exact error text, no-write conquest observation, token rejection unchanged, fixed last-slot replacement, coldload reset and observation-error isolation. No full historical regression or large stress run. Native display/event availability remain USER_GAME_TEST_REQUIRED.

After authorized deployment, minimal test: cold-start the existing foreign-held save, conquer back once, immediately click E2往返 and capture its report. No re-import/investment, no repeat outbound trade, no in-session load required. This needs a new capture because session event evidence cannot be reconstructed from a save already taken after conquest. If only such a save is available, its on-demand report still confirms current token/HELD, but cannot prove earlier event delivery. Stop on any ambiguity; do not continue Claim/F. Build/header B100.127 distinguishes the new diagnostic package.


## B101.128 — authorized original-owner native transition adaptation

User authorized after B100 proved matching transfer with nil native binding. Scope remains one migrated persistent city, original-human-owner return only; no Claim/new cityKey/global migration/AI/Design change. No token copying or City ledger reconstruction.

### Proof and retained authority

Existing successful original-token path remains supported. For a missing (not conflicting) live token, require: saved confirmed loss; this session's exact live foreign reference observed; matching old owner/CityID removal; original owner's new reference added at the tracked location; same new reference initialized; final CityTransfered arguments matching new owner/ID and saved foreign owner. Removal/add/init/transfer must be strictly ordered in one game turn. Coordinates join the event endpoints but do not independently establish identity. Incomplete/unknown/conflicting/out-of-order/cross-turn chains and CityBuilt at the target reject. The tracker holds one bounded session chain, with no polling or generic retry. Reload mid-chain cannot synthesize missing evidence. Unrelated locations are ignored; identical duplicate notifications do not duplicate restoration.

A successful acceptance persists returnEvidence=NATIVE_TRANSITION_V1 plus bounded returnProof (version/from/to/turn/order) in the existing Game record, retaining lastLoss, original base/binding/investment/templates. Existing schema1 accepts old records; new proof is explicitly validated. The accepted current owner/ID/location plus validated proof allow future reads/reloads with token nil; a conflicting token still rejects. A matching removal of an ACTIVE reference durably sets referenceInvalidated, blocking reads even if an ID is reused, until a subsequently confirmed supported transfer/return. No token is written back. Consumer reference projection and existing current-facts resets remain B097-owned; no old ACTIVE/routes/sample/carrier snapshots are restored. Missing Industry historical templates remain held, not backfilled from foreign-period buildings. Deferred Legacy remains deferred.

Temporary proof assembly is not persisted; saving mid-transfer remains a conservative unsupported recovery boundary. A completed accepted return is saved and can be cold-loaded. Old B100 binaries cannot interpret the new accepted-return evidence: binary rollback uses the preserved B100 package **and a pre-B101-acceptance save**, never promise reverse schema compatibility. Foreign-held B099/B100 saves remain supported inputs. No save file is directly edited.

GameEvents.CityConquered diagnostic observation now matches the earlier E1 namespace; it is observation-only, not a new recovery trigger. Actual acceptance uses the CityTransfered chain observed in B100. TARGET_UNAVAILABLE after an unsuccessful return remains the old foreign exit-reference observation, not permission to clear the new local city.

### Validation / limits

W0004 L3, narrowly targeted because this changes saved identity acceptance. STATIC_CONFIRMED: unchanged Gameplay formulas/Design; no City token setter/new carrier/new migration system; Lua compile/package/context integrity. LOCAL_SIMULATION_PASS: test_b101_e2_transition (includes existing same-owner investment, legacy token return, current Governor/Network and Industry history regression), test_b100_e2_diagnostics, test_p0_e2_exit with read-only native DB (21 owned groups/2322 IDs). Covers four identities, retained original records, new investment after tokenless return, coldload of accepted proof, repeats/duplicates, persistent removal invalidation, unknown live object, malformed stored proof, missing/ordered/conflicting/cross-turn/foundation/removed-target evidence, mid-chain load rejection, missing foreign witness, withdrawal failure, current Network input and zero City-property rewrite. No broad historical regression/stress. Failure/UNKNOWN tests intentionally log held states; successful acceptance asserts actual nonzero Potential/current ACTIVE and stage ACTIVE.

Native status: USER_GAME_TEST_REQUIRED, not PASS. Smallest test: cold-start existing foreign-held save, conquer same city once, immediately read E2往返 and 城市专业/潜力. Expect ACCEPTED, NATIVE_TRANSITION_V1, retained P2/investment1, current ACTIVE (not assumed2), token may remain MISSING. Save accepted result into a separate slot, fully exit/restart and read again. Preserve the foreign-held save for rollback. No re-import/Claim or in-session load required. Network rebuild should be assessed against real current routes; no-route scenario does not certify all route topologies. Stop on any rejection instead of repeating investment/migration. After this checkpoint wait for evidence, do not proceed Claim/F.


## B102.129 — authorized conquest / CityBuilt classification repair

B101 native evidence showed23/23 exits, a matching GameEvents.CityConquered before removal, and RETURN_NEW_FOUNDATION. B102 no longer treats the name CityBuilt alone as proof of a new foundation. It keeps one exact conquest tuple and one CityBuilt endpoint in session memory (no history, no requests). At final CityTransfered, a tokenless chain containing CityBuilt is accepted only if both endpoints match the current original-owner city, conquest's former owner matches the saved foreign loss reference, all evidence is from the same turn, typed conquest precedes removal, and the existing removal→added→initialized→transfer order is complete. CityBuilt may occur at any position before final transfer; no specific unobserved timing is assumed. Conflicting duplicates, wrong owner/ID, cross-turn events, incomplete chains and founding without typed conquest still hold. Merely receiving CityConquered never activates anything. No token copy/Claim/new cityKey/Design changes.

Accepted evidence uses returnProof.version2 with conquest and foundation records, validated again on read/load; version1 accepted B101 records remain supported. Same Game key, original identity/receipts/templates and existing current Governor/Network recomputation remain. A rollback to B101 requires the saved pre-acceptance foreign-held game; B101 does not understand version2 proof. Incomplete chain recovery is still deliberately refused. CityBuilt is now a sixth fixed diagnostic event slot, recording scalar parameters on demand without disk writes.

W0004 L3 narrowly targeted: test_b102_e2_foundation runs the B101/E2 same-owner/legacy-return/current-state suite plus five possible CityBuilt positions, accepted proof coldload, repeated notifications, wrong old/new owner/ID/location, stale/late/conflicting conquest, conflicting CityBuilt, missing removal, mid-chain reload, malformed stored version2 proof, and read-only diagnostic checks. test_b100_e2_diagnostics and test_p0_e2_exit also PASS (21 owned sets/2322 IDs, UNKNOWN/idempotent/ordinary/permanent/control city protection). Exit test now explicitly checks B101's one persisted reference-invalidated revision and the subsequent loss revision, instead of expecting one total write. B100 diagnostic test's intentionally malformed conquest tuple now expects the strict conflict rejection. These are explicit changed expectations, not relaxed safety assertions. Lua compile/modinfo/context/diff checks PASS. No full historical/stress run. LOCAL_SIMULATION_PASS only; native acceptance remains USER_GAME_TEST_REQUIRED.

Minimum native test remains one cold-start of the existing foreign-held save, one conquest, then E2往返 and 城市专业/潜力. If accepted, save separately and cold-restart/reload to confirm retained proof/current facts. No need to repeat the outbound trade or earlier22/23 incident. Keep the original foreign-held save. If rejected, stop and provide E2 report; CityBuilt raw arguments are now visible. No automatic Claim/F continuation.


## B103.130 — authorized foreign-load hydration repair

The B102 native latest sequence was valid, but local reproduction exposed a pre-transition foreign CityAdded/Initialized fault latched during load. Exempt only the exact saved foreign owner/ID/location while no removal, conquest or foundation evidence exists. This does not prove identity, activate a city, create a transition, write a token, or clear any earlier fault. Once transfer evidence begins, existing strict ordering/reference gates remain.

One session-only first-fault scalar event slot supplements the existing latest-event slots; on-demand diagnostics retain the original reason/arguments after subsequent events. It resets at confirmed loss/accepted return or load, with no history, polling or new persistent schema.

L3 targeted LOCAL_SIMULATION_PASS (not engine PASS): four identities; both foreign load notification orders and repeated initialization; HELD coldload then screenshot-order conquest; accepted proof coldload; immutable base/investment; no token rewrite; duplicate return; wrong owner/ID, premature new owner, old endpoint after transfer begins, initialization-before-add and incomplete-chain reload reject. Existing B101/B102 proof, B097 recapture/current-fact, E2 investment, B100 diagnostics and owned-exit regressions pass; Lua compile/modinfo pass. Exact exit catalog remains 21 modules/2322 IDs plus existing non-carrier exits. No Claim/F/Design changes.

Native gate remains USER_GAME_TEST_REQUIRED. Minimal test after deployment: cold-start the existing foreign-held save, conquer back, read E2 return + city specialization; only if accepted, save separately and cold-start to check retained progress/current ACTIVE/Network. No re-import/investment/trade repetition. Pre-return save remains the rollback boundary.


## 2026-09-25 — E2 inventory and next-slice proposal (not authorized)

Baseline B103.130, source e238584, acceptance96a7d05, D0035/A0161. This is planning only, not authorization for multi-city cutover, Claim or F. Current native evidence: [B103 scoped acceptance](../../Status/Validation/Results/Specialization_B103_E2_Recapture_Pass.md).

### Implemented versus verified

| Capability | Actual runtime | Evidence / limit |
|---|---|---|
| Explicit existing-city import | One Game record, PREPARED/ACTIVE, original reference/base/receipts, no old-writer fallback | Actual Lua local regression; tested Research record persisted through ownership cycle |
| Settler investment | Migrated target uses Game ledger, existing debit/receipt lifecycle; others old backend | Local duplicate/recovery/new-investment tests; native one retained receipt, not a new post-return investment test |
| Ownership loss | HELD_TRANSFER, permanent record retained;21 owned carrier groups plus Network/probe exits, no ordinary-building deletion | Local full allowlist/UNKNOWN/idempotence; native23/23 and Research observations; not four-profession full yield certification |
| Original-owner recapture | Valid original token or strict saved foreign reference + native transition proof; new current reference persisted | Research conquest ACCEPTED with nil token, P2/receipt1, coldload PASS |
| Current ACTIVE | Derived from current Governor/eligibility, not old snapshot | Native ACTIVE1 before governor; user confirms Lv1/Lv2 after governor; local other states |
| Current Network | Invalidation/current facts and reset sample paths implemented | Native new reference MATCHED, source true/receiver false/routes0; nonzero-route effects only locally covered |
| Own Industry templates | Migrated-city Game-backed own ledger retained, missing history held | Local only for cross-owner template retention; no inference about unimplemented Wonder credit |
| Human eligibility / diagnostics | Actual Player.IsHuman, no player0 assumption; fixed latest events/first fault; on-demand reports | Basic reports/native and scoped acceptance; no AI/MP enablement |
| Multi-city new backend | NOT IMPLEMENTED: root is one record; import cannot add a second | Other cities still old storage; one city's PASS does not certify global save safety |
| New-city direct new-backend registration | NOT IMPLEMENTED | Existing new-city legacy flow remains; not a new Game-ledger registration system |
| First no-history AI conquest | Snapshot/LegacySet/Claim modes NOT IMPLEMENTED | Never infer known-empty history from UNKNOWN; no Claim projects/cost selected |
| General History / REALLOCATING | Architecture contract, NOT a completed runtime state machine | No restructuring actions or general historical maximum ledger |
| Profession future permanent systems | Academic Tradition, new Culture observations/Dialogue ownership, Commerce contracts/reputation not supplied by E2 | Existing legacy abilities are not evidence of frozen-design implementation |

### Recommended order within E2

1. **Two-record isolation slice (recommended next)**: explicit registration of two already-specialized, fully evidenced own cities; no automatic all-city migration.
2. **New self-founded city slice**: event-proven foundation/first completion into new storage, no load-time reconstruction; requires record routing first.
3. **First AI conquest snapshot slice**: prove no prior specialization history, one-time completed four-domain set, persist mutually exclusive modes; no Claim action yet. Pending Claim cities remain unassigned as Design allows. Empty-set future-completion path needs its own targeted acceptance.
4. **Claim action slice**: UI/project entry, authoritative one-choice completion, old first-completion exclusion; precise low-cost versus one-turn primitive/cost gate reviewed before implementation, no invented numeric balance.
5. **E2 support-boundary closure**: confirm supported new/test saves and explicit old-save migration/rollback policy, remaining relevant native gates; only then review P0-F eligible-age scope.

These are implementation slices of existing E2, not a new architecture program. Snapshot could be explored in isolation, but a usable implementation needs more than the existing occupied singleton root; solving routing first avoids disposable storage paths. No universal city identity or automatic whole-save migration is proposed.

### Next slice: two existing cities, independent saved progress

**Goal:** remove the singleton bottleneck with the smallest verifiable two-city experiment. Reuse current binding provenance and per-record recapture proof; never match by name, coordinates alone or guessed CityID. Existing validated token supplies identity for explicitly imported records; collision/ambiguous provenance holds. No new universal cityKey scheme.

**Scope:** within the existing Game storage responsibility, add a versioned record collection and current-reference routing; preserve B103 singleton as a lossless first record on supported load, validate before committing any conversion, no duplicate writable authority. Keep each record's lifecycle, exit/retry state, transition proof and sample invalidation isolated. Explicitly import a second intact own specialized city. Unimported cities retain legacy backend. No source formula/new carrier/Legacy rewrite. Unknown or corrupt record must not select another city's record or silently fall back.

**Likely modules:** CityProgressionStore; its startup/read/write routing in Gameplay, EffectiveFacts, InvestmentAction, NetworkInput, Standardization and existing Binding/Journal/Flow guards only where singleton assumptions require adjustment. On-demand diagnostic reports selected city's record, not the previous singleton regardless of selection. Exact file closure reviewed at implementation under W0001, not a full unrelated audit.

**W0004 L3 local acceptance:** lossless schema conversion and repeated load; two imports with distinct tokens/references; investment affects only target; one lost/returned city while the other continues current abilities and ledger; separate event/exit/retry states; duplicate/UNKNOWN/collision and same-ID-different-owner rejection; accepted return coldload; no old/new double writes; untouched third legacy city; existing B103 ordering/hydration protections; current Network input invalidation only where appropriate. No broad historical/stress run by default.

**Minimal future native test:** use a copy of the accepted B103 save, import one other intact own specialized city; invest once in that second city and verify first unchanged; separate save/coldload, read each city's concise state. Local tests cover transfer isolation; do not demand repeat conquest unless implementation introduces an unproven native event dependency. Missing intact second fixture is a test preparation boundary, not authority to reconstruct lost history.

**Exit:** two records coexist, selected-city diagnostics and investment route correctly, saved progress survives reload, singleton compatibility proven locally and native two-city check reported. The test support remains explicit migrated cities, not all legacy saves/cities. Rollback uses B103 package plus pre-conversion save; no automatic reverse migration.

**Explicit exclusions:** automatic full-city migration, new-city initialization, first AI snapshot/Claim, history/REALLOCATING actions, AI/MP, F/new abilities, Design and balance edits.

No new Gameplay decision blocks this proposed slice. User scope approval is required before implementation. Nonzero-route native reapplication and old in-session reload crash stay separate evidence gaps; they do not justify claiming E2 fully complete or running unrelated regressions now.


## B104.131 — authorized two-existing-city persistence slice

**Implemented, LOCAL_SIMULATION_PASS; scoped two-city USER_GAME_TEST_PASS ([evidence](../../Status/Validation/Results/Specialization_B104_E2_Two_City_Pass.md)).** User authorized the immediately preceding proposal. No new Gameplay/Design rule, new carrier, new-city registration, Claim, AI/MP, general cityKey, full-save migration or F. Canonical changes are CityProgressionStore, selected-city P0Panel request/tooltip, Probe/modinfo build identity and targeted tests. Existing consumers retain their method contracts.

### Storage and routing

Same Game Property `SPC_CITY_PROGRESSION_E2_V1`; new outer schema2 `{revision, records[existing validated token]}` holds at most two explicit registrations. Inner records retain schema1 and their original base/binding/investment/templates/return proof. This is not an external file or newly minted universal city ID. Unknown schema, duplicate token/location/current owner+ID, malformed records and unreadable collection fail closed, never route to another city/old writer. Collection corruption/readback uncertainty can hold the collection until reload; do not claim per-record recovery from corrupt shared storage.

B103 schema1 is validated and projected as one record **in memory without a load/diagnostic write**. The next real mutation atomically writes the whole schema2 value with that retained entry; adding the second city leaves the first inner record unchanged. Existing source-comparison, readback confirmation and PREPARED→ACTIVE import remain. A rejected pre-write import does not retain a phantom record/consume a slot. Collection write reentrancy/staleness is refused. Existing bounded Copy limits remain; oversized values hold, not truncate.

Each record reuses the B103 lifecycle with separate root, finished exits, bounded retry counts, foreign witness, transition/conquest/foundation, latest events and first fault. Manager forwards only reference/location-relevant events; a city location is an exclusion/routing guard, never enough to authorize restoration. Reads still require full current reference and proof. No new polling/full-city scans/hover requests. Explicitly unregistered cities retain legacy backend. The player-wide Network snapshot and sample protocols remain existing shared dependency domains: ownership changes can invalidate the entire verified player snapshot; this is not a promise that another city's transient Network view never changes. No sample protocol rewrite.

### Diagnostics

E2往返 now reads the selected own city and UI actually sends its CityID. No selection/foreign selection does not dispatch; an unregistered own city is labelled unregistered rather than showing the former singleton. Existing verbose native evidence stays available for the selected record, normal progress summary stays brief. Tooltip states the two-city test limit. This batch does not add a foreign-city selection/browser UI.

### Validation (W0004 L3, affected storage/lifecycle only)

`test_b104_e2_two_cities.py` includes existing E2/B097/B101/B102/B103 suites, then actual two-city store/investment routing: accepted tokenless B103 singleton load without writes; second Commerce registration; unchanged first Research inner record; second-only actual Settler debit/receipt and duplicate confirmation; third legacy city unaffected; two records coldload; selected/unregistered/no-selection diagnostic behavior; independent loss/return and one failing exit's3-attempt limit; repeated events; exact token/location/schema/record corruption rejection; failed second PREPARED/activation writes and recovery; sameID/foreignOwner read rejection; generic idle zero persistent writes. Actual P0Panel request function executed for two selections/no selection/foreign selection. Existing tests now explicitly unwrap one record and query copied per-city Status instead of reading singleton storage/session fields; original numerical/withdrawal/proof assertions remain.

`test_b100_e2_diagnostics.py` and `test_p0_e2_exit.py` with read-only native DB retain actual module exit/UNKNOWN/ordinary-building/permanent preservation and Network invalidation coverage (21 carrier groups/2322 exact internal IDs plus existing Network/probe exits). All Lua compiles, modinfo/context/diff checks pass. No whole historical regression or large stress run. These are STATIC_CONFIRMED / LOCAL_SIMULATION_PASS, not native certification.

### Minimal user acceptance / rollback

1. Preserve the accepted B103 save untouched; use a test copy in B104. Confirm header B104.131. Select first migrated Research city and read E2/专业: existing Identity/P/receipt intact. Do not re-import it.
2. Select another intact own four-profession city with Potential<4, right-click“迁移进度” once. Read its E2/专业; invest one Settler through the existing action. It alone gains one Potential/receipt; first city unchanged. If missing old history, stop and report; do not reconstruct it from buildings.
3. Save separately, exit/restart and reload. Read each selected city's report: two states retained. No repeat conquest required for this slice unless new native evidence contradicts the routing.

Rollback is B103 complete runtime plus **pre-schema2 save**. No reverse migration; do not promise B103 can read a save changed by B104. Still E2 partial, next proposal after acceptance is new self-founded-city registration, not automatic Claim/F.


## Next slice — new self-founded city registration (PLAN ONLY)

User requested continuation after B104 acceptance; this authorizes this plan, not implementation. Runtime baseline B104.131 / source bfe7003; D0035/A0161 unchanged. PROG-001/002/003/005 govern normal first completion and investment. PROG-006..009 conquest initialization is explicitly excluded. Four professions/local human only.

### Goal and narrow boundary

Prove one newly founded own city can enter the Game progression backend while genuinely unassigned, survive a reload before its first qualifying district, lock the first valid completed four-profession district at Potential1, then accept one ordinary Settler investment with an existing registered city unchanged. No new yield formula/carrier. This is not merely an automatic import after old writers have already established a specialization.

Keep the existing **two-record test cap** in this slice. Use a separate test save containing at most one registered existing control city before founding the new city. Do not delete either record from the accepted two-city save to make room. Full-cap attempts explicitly report outside this test slice and do not partially take ownership or silently claim registration; previously untouched legacy cities remain legacy. Removal of the test cap/general rollout is separate E2 closure work, not a permanent Gameplay city limit.

### Current code findings and intended cutover

| Path | Current B104 | Proposed work |
|---|---|---|
| BindingProbe / FreshBindingHook | CityBuilt → validated binding → foundation journal → Flow; finite original token allocation | Reuse existing binding identity, inspect exact source evidence and callback ordering; do not create universal cityKey or widen32-token limit |
| CityProgressionStore | Inner validation requires four-profession identity/baseP1; Import requires full old specialized history | Add explicitly discriminated fresh-unassigned record with foundation provenance, NONE/P0/no receipts; preserve B103/B104 specialized record acceptance without guessing history |
| CityJournalProbe / CityFlowProbe | Owns guard freezes registered-city writers; old normal completion writes City properties | Hand off only confirmed fresh target after foundation evidence; registered target's first-completion transition belongs to Game store, legacy completion/resume must skip it |
| EffectiveFacts / current facts / Network | Existing migrated specialized Base contract | Validate explicit known-unassigned output: no abilities/investment/source; distinguish unknown/held from NONE; specialized result uses unchanged current facts |
| InvestmentAction / consumers | Shared routed investment and current derivation | Reuse after first identity established; no second receipt backend, no temporary ACTIVE/Network snapshot restoration |
| P0Panel / diagnostics | Selected-city progress and native report | Show city, registration origin, unassigned/locked state, first completion, Potential/receipts and actionable failure only |

### Foundation classification — revised event-sequence plan

User approves updating the plan from the read-only sequence investigation, **not implementation**. Prefer collecting the affected lifecycle sequence and classifying at a verified completion boundary; do not require a special destruction event or a Settler witness as the only possible proof. CityBuilt alone, empty districts, names, coordinates and a momentary absence of later events still do not prove foundation.

#### Evidence and remaining technical check

- B102 native report records CityBuilt → CityConquered → CityRemovedFromMap → CityAddedToMap → CityInitialized → CityTransfered for the tested conquest. This is observed order, not a universal engine ordering guarantee. See [original evidence](../../Status/Validation/Results/Specialization_B102_E2_Chain_Order.md).
- Installed original `Base/Assets/UI/Choosers/ResearchChooser.lua:38,485` explicitly uses GameCoreEventPublishComplete to end a series of gamecore notifications; CityBannerManager uses the same flush pattern. STATIC_CONFIRMED for UI batch processing, **not** native confirmation that every Gameplay/GameEvents transfer fits one publish batch.
- [GCO author source](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_ModUtils.lua#L1176-L1235) correlates removal/addition/initialization to identify capture. Installed HD `2860503037/Lua/Assyria.lua:29–62` combines a current-turn conquest cache with removal/object absence for its own effect. These are STATIC implementation precedents, not universal identity contracts to copy.
- Current Standardization already registers a Gameplay-side PublishComplete flush. Registration is not proof of the proposed ordering guarantee. Verify delivery in the intended context, relation to CityTransfered, loading, and whether one operation can span multiple publish batches before enabling negative-evidence classification. No UI report becomes sole authoritative identity proof.

#### Bounded processing

1. Record only affected references and essential lifecycle evidence. CityBuilt starts a candidate; it does not immediately enroll it. Matching transfer/conquest evidence associates old/new endpoints. Preserve accepted B103/B104 recapture proof and module-owned withdrawal rather than replace them with a generic classifier.
2. An explicit, validated CityTransfered endpoint can close the corresponding transfer. Use PublishComplete as the **candidate** flush boundary for remaining cases, not as a presumed atomic transaction delimiter. If actual delivery cannot exclude a pending transfer, leave that candidate unresolved; do not assume a single flush or timeout proves no later events.
3. At a verified boundary inspect only the affected location/current references and loading state. No player-wide city scan. Coordinate is an event-correlation/location-check field, never sole authority for inheritance.
4. Empty pending set → immediate return. No timer, per-frame audit, fixed sleep, every-pulse Gameplay request or unbounded event history. Bound pending records and evidence per record; overflow/conflict produces a diagnosed hold without dropping evidence and manufacturing a clean new-city candidate.
5. Do not let old Binding/Journal/Flow write a fresh identity before classification, then treat those writes as proof that the city was fresh. Add the narrow pre-write guard/handoff needed for participating candidates. Unaffected legacy cities retain their existing path.

| Completed observation | Planned result |
|---|---|
| Matching old/new endpoints with confirmed transfer/conquest | Ownership transition; preserve existing same-city recapture checks; an unrecorded acquired AI city stays outside this slice, never fresh enrollment |
| Removal, verified lifecycle boundary, confirmed no city at affected location, no unresolved replacement/transfer | End the old live reference, preserve historical record, forbid later automatic revival from location alone; not permanent-history deletion |
| Genuine live build/add/init sequence, verified boundary, no associated acquisition/old active generation, local human ownership, outside load hydration | New unassigned record; reuse validated binding mechanism after classification |
| New founding after a separately confirmed earlier destruction | Different lifecycle generation, cannot inherit the terminated record; if current bounded store cannot retain history and admit the new reference safely, report unsupported capacity/generation boundary rather than delete or reuse history |
| Load hydration, incomplete/cross-batch sequence, inaccessible object, conflicting references | Restore known records or hold candidate; absence/UNKNOWN does not authorize destruction or foundation |

The immediate objective remains one self-founded city → NONE/P0 → first completion → investment/save. Destruction/rebuild is a classification and non-inheritance guard, not authorization for general raze recovery, new universal cityKey or unlimited historical generations. If the native flush boundary is insufficient, stop that negative-evidence path as EVENT_BATCH_BOUNDARY and propose the smallest scoped evidence capture; preserve successful work/records. Do not automatically expand into a permanent debug system or new gameplay design.

### State and write ordering

1. Classify the completed foundation sequence, then confirm initial state and persist the target record/takeover before consumers use it. Existing validated binding bootstrap may supply identity evidence only after the pre-write gate; never treat legacy writes caused by an ambiguous CityBuilt as independent proof. No parallel writable progression authority after takeover.
2. Record distinguishes normal first-completion eligibility from unknown old city, conquest candidate and REALLOCATING. NONE/P0 carries no specialization effects or investment eligibility.
3. Persist registration/eligibility before reload; load is restoration, never a fabricated district-completion event. No scanning existing districts on load to choose Identity.
4. If a district completion arrives while foundation classification is pending, retain its bounded event order/reference evidence and validate after admission; never discard it and reconstruct from a later district scan. Overflow/uncertainty holds explicitly. First live valid completion checks current city/reference, completed status and approved replacement family; lock identity/P1 and completion evidence in one confirmed Game mutation. Later/duplicate notifications cannot overwrite it. Preserve delivered event order, no end-turn aggregation or domain priority.
5. After lock, use existing investment backend and current Governor/Network derivation. Unknown/write failure holds this target rather than falling back to frozen City records. Document exact schema compatibility before coding; no implicit in-place reinterpretation of missing fields.
6. New unassigned city's ownership loss, destruction/re-foundation or ambiguous transfer must remain held/non-active, never enter Claim or be reconstructed from current districts. Do not claim full pre-specialization transfer support; recoverable diagnosed stop is an explicit slice boundary.

### Validation and acceptance

W0004 L3 because persistent authority and completion ordering change. Target only affected foundation/first-completion/store/investment lifecycle, plus B104 two-city and B103 recapture/withdrawal regressions where touched. No automatic full historical or10k stress suite.

Local cases additionally cover CityBuilt-before-conquest; transfer split across flushes (no premature fresh/destruction decision); repeated/idle flush; disappearance versus inaccessible object; confirmed destruction followed by separate same-location founding (no inheritance); load hydration; completion before enrollment; and bounded evidence overflow. Simulated ordering tests cannot prove the native flush boundary. Local cases: genuine fresh enrollment; duplicate founding; conquest/load/rebuilt/unknown/AI/foreign rejection; NONE/P0 save/load; placement versus completed district; four approved families/replacements; first of competing notifications wins; duplicate completion; investment blocked before identity and once afterward; existing record unchanged; full-cap refusal; failed write/readback and reload; old schema preservation; idle notifications cause no repeated scan/write. Confirm no old/new concurrent writer and no new carrier/Design changes. Preserve module-owned confirmed-loss semantics for existing specialized records.

Minimal native flow (after a separately authorized implementation/deployment): use a separate save with one registered control, found one new city, read brief unassigned report; save and restart/load **before** first district completion; finish one four-profession district, check P1, invest once for P2; compare unchanged control; separately save/restart/load and confirm. Cheat-assisted completion may be used as current workflow permits; do not claim natural-production timing beyond observed evidence. Two reload points test different states and cannot substitute for one another. No repeat conquest required for this slice.

Exit: native boundary evidence sufficient for the enabled path (otherwise an evidence-only checkpoint, not general registration PASS); fresh provenance gate justified; local checks pass; minimum native flow passes; no legacy double-write or cross-city mutation. If native foundation evidence contradicts assumptions, stop and preserve evidence. Local PASS alone is not E2/native completion.

Rollback: committed B104 runtime plus untouched pre-slice save; no promise that B104 reads saves containing a new unassigned schema. No automatic reverse conversion. No deployment during planning.

### Exclusions / next dependency

No first AI conquest snapshot/Claim, current two-city save record deletion, all-city migration, AI/MP, new cityKey, profession Legacy invention, Research Tradition/F or new gameplay effects. After scoped acceptance, separately plan remaining E2 enrollment/generalization and conquest snapshot/Claim gates. This plan is awaiting explicit implementation authorization.


## B105.132 — authorized event-batch evidence checkpoint

User authorized the revised next slice. Its explicit EVENT_BATCH_BOUNDARY stop condition applies: source establishes that PublishComplete is used after event series, but does not establish Gameplay delivery relative to the entire transfer chain. A mock cannot prove that a pending transfer will not arrive after a flush. **Do not enable automatic new-city enrollment on this assumption.** This checkpoint implements the smallest native evidence capture; the unassigned record/cutover/first-completion portion remains NOT_IMPLEMENTED, not a claimed successful registration slice.

### Implemented and excluded

- New `CitySequenceProbe.lua`, started before CityProgressionStore/Binding: opt-in single plot,48 primitive event/boundary rows,12 bounded owner/ID references. No event payload/object retention, persistent state, file logging, effect/write/scan/request API. Read/overflow errors stop only the observer; no mutation of E2 records. No new-city classification or destroyed-record retirement.
- Captures GameEvents CityBuilt/CityConquered plus Events removal/addition/initialization/transfer at the selected location/references. Captures only the first subsequent Gameplay PublishComplete and PlaybackComplete after relevant events, with a single targeted current-city lookup. Empty pending boundary flags return immediately, without strings or city queries. Marker rows can reveal interleaving; no claim that either marker closes an engine transaction.
- Arm before action: selected own Settler location or selected own city. Start records existing occupant (or EMPTY/UNKNOWN); exact references allow subsequent foreign-held removal to be observed without enabling AI specialization. Observation is session-only; re-arm replaces it, load resets it. Request token duplicate does not erase trace.
- Existing panel, no extra button: right-click 移民/施工队 starts observation; right-click E2往返 reads/pages it even without selected own city. Left-click functions remain. Prior UI-identity helper stays in source but this temporary right-click entry is repurposed.48 rows,10/page; original hook names/arguments in concise report. Missing hooks/errors/limit appear explicitly.
- Manual read is marked ReadRequest while boundaries are pending, because the diagnostic player operation itself could provoke a publish. A publish after that marker is not independent proof of an operation-only boundary. Describe formatting itself performs no engine lookups.
- B104 CityProgressionStore, Binding/Journal/Flow, all consumer writers, Game save schema and Design bytes unchanged. New cities still follow the existing legacy runtime path, **not** the planned Game-backend registration. Do not treat their old visible effects as proof of new enrollment. No Claim/F/AI/multiplayer/new cityKey/general migration or destructive history cleanup.

### Verification

W0004 risk: event-order/identity work is L3, narrowed here to passive observation plus touched request dispatch. `test_b105_city_sequence.py` executes actual collector and UI/Gameplay request functions: unarmed and idle zero lookups/writes; normal founding sequence; Build-before-conquest; flushes between transfer stages; removal without successor and later build; UNKNOWN never EMPTY; unrelated references ignored; duplicate begin; invalid targets; missing hooks; finite trace/stop; read-operation marker; no-selection reads/pagination; observer failure isolation. All Lua compile and modinfo132 inclusion checked.

Existing B104 actual two-city test imports E2/B097/B101/B102/B103 regression chain: investment/receipt isolation, old schema adapter, load recovery, held/return lifecycle, duplicate handling and UI selection all PASS. B099 actual eligibility/dispatcher regression PASS. Only E2 test's exact manifest version assertion changed131→132; no outcome assertions weakened. No large stress or whole historical regression. Evidence level STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; native event batch boundary remains USER_GAME_TEST_REQUIRED.

### Minimal native evidence, before registration work resumes

Use a disposable copy of a B104-compatible test save. No migration or investment required; the existing two-record cap does not restrict this passive observer.

1. Select an own Settler at the intended founding tile; right-click 移民/施工队 and confirm Start/position. Found there; right-click E2往返 and screenshot every indicated page. Do not reload before reading.
2. Before a convenient ownership transfer, select an own noncapital city (deselect any unit), right-click 移民/施工队 to replace the observation, then trade it to AI. Right-click E2往返 again without needing to select the now-foreign city; screenshot all pages. This tests gift transfer, not conquest/raze. Existing B103 conquest order remains prior evidence but lacks publish markers; if gift shows a split/missing boundary, stop rather than demand speculative additional cases.

No repeat investment, governor or full coldload validation at this evidence gate. A destruction/rebuild capture is conditional only if needed to enable that path later; do not ask for random disasters/AI razing now. Founding plus gift traces are scoped samples, not universal guarantees. If relevant publish hook is absent or occurs only after ReadRequest, report this and choose a supported boundary/evidence approach before authority cutover; do not add polling.

Rollback for this observer-only checkpoint: B104 runtime; it introduces no save schema change. Preserve normal separate test saves and existing receipt-bound B104 recovery. The future full registration slice may require pre-slice saves as already specified. Complete this checkpoint, commit/push and authorized test deployment, then stop for native evidence; do not enter Claim/F or certify the full next slice.


## B106.133 — authorized FOUND_CITY evidence checkpoint

User authorized proceeding from the [other-Mod investigation](../../Reports/Technical/Specialization_E2_Other_Mod_City_Lifecycle_References.md). Scope: extend the existing passive collector only, before any new-city authority implementation. B105 proved first Publish can split the notification chain; it is not revived as a completion condition.

- Same single location,48-row bound, opt-in/session-only observer. Add Gameplay Events.UnitActivate; store owner/unitID/raw finite numeric reason/visibility. Matching the actual EventSubTypes.FOUND_CITY value labels the row FoundCity; unavailable enum or other reasons remain UnitActivate. Missing hook and startup enum availability are explicit. No numeric enum guessed, no visibility filter.
- Arming with a Settler records its ID as a scalar. Activation never queries that unit (it may already have been consumed) and never puts unit IDs into the city-reference set. Location restricts observation, not persistent identity. Events may precede/follow city initialization; records preserve their observed order. Duplicate notifications remain visible evidence within the same limit, not extra authority applications.
- Unit activation sets the existing pending boundary flags, so the same first-following Publish/Playback and ReadRequest rules apply. No polling/UI bridge added; if Gameplay does not deliver this event, stop and report that context boundary rather than silently using a UI assertion. No CityProgressionStore, consumers, save schema, Gameplay dispatcher or UI source changes. No registration/Claim/F or new Gameplay benefit.
- Diagnostic adds one capability/starting-unit line and one argument legend; existing arm/read/right-click pagination remains. No extra buttons. Build B106.133/modinfo133.

Validation: targeted event-order L3 scope, no full historical/stress suite. Actual collector tests cover signed enum, missing enum/hook, nil reason, invisible activation, founding before/after city events, unrelated location, no unit lookup, transfer negative-control trace,48-row overflow, unarmed/idle no work; retained actual UI/Gameplay request tests and all Lua syntax. Existing B104 two-city/E2 regression chain passes. Only exact manifest version expectations change132→133. STATIC_CONFIRMED / LOCAL_SIMULATION_PASS only; native FOUND_CITY availability/timing remains USER_GAME_TEST_REQUIRED.

Minimal native test after safe deployment: (1) select an own Settler already on the intended tile; right-click 移民/施工队, found normally, right-click E2往返 and capture all pages; (2) save those images, deselect unit/select own noncapital city, re-arm and trade it to AI, then capture all pages as negative control. If first arm reports missing UnitActivate or FOUND_CITY不可用, capture that report and stop; no need to perform both actions. Do not reload between arm/action/read; no repeated migration/investment/governor/save test. This validates only the new event, not permanent registration or all engine paths. B105 results need not be re-proved; the two actions add the missing founding-specific evidence.

Rollback: tool-retained B105 runtime, no new save schema. Standing W0003 deployment only after clean committed source and confirmed game exit. Stop after evidence checkpoint; no automatic fresh enrollment or Claim/F.


## Post-B106 plan — positive founding evidence / fresh registration

Current proposal, prepared under the user's latest authorization to proceed with the registration plan. **PLAN_ONLY / implementation awaits review.** Baseline B106.133 source14b0681; native evidence commit9a55d05. D0035/A0161 unchanged. This section supersedes the earlier new-self-founded-city plan's foundation classifier, Publish boundary gate and baseline/rollback references; it does not replace B103/B104 ownership logic. B105/B106 remain historical evidence checkpoints.

### Evidence and goal

B106 natively delivered Gameplay Events.UnitActivate with reason equal to EventSubTypes.FOUND_CITY after Initialized, matching the preselected Settler in the observed founding; transfer control had Transfer without FoundCity. Use this **positive engine reason**, not an inferred absence of transfer. No fixed Publish count/delay/Playback-as-universal-boundary. Neither the observed numeric reason nor the observed callback order is hardcoded.

Goal: one ordinary self-founded local-human city automatically enters Game storage as NONE/P0, survives coldload, locks its first valid completed four-profession district at P1, then accepts one normal investment to P2; an existing registered control stays unchanged. No new yields/carriers, no need to press a migration/arm button for this path.

### Automatic evidence and ownership handoff

1. Add a small foundation coordinator within the existing progression responsibility, initialized before legacy Binding/Journal/Flow callbacks. The manual CitySequenceProbe remains diagnostic only and cannot authorize registration. Do not reuse its capture toggle as the gameplay switch.
2. After normal load readiness, correlate only local-human city Built/Initialized and UnitActivate/FOUND_CITY scalar events. The founding notification provides owner/unitID/location/reason; resolve the current city at that location and match its owner/ID to the city-initialization evidence. Require genuine positive founding evidence and no conflicting current recorded reference/history. Unit and city IDs are distinct. Do not require a surviving Settler object or preselect/scan all Settlers. Earlier manual Settler matching supports the native event's interpretation; automatic provenance relies on the engine's typed notification, not UI assertion.
3. Both delivery orders are supported: a matching Initialized can complete an earlier founding candidate, or FOUND_CITY can complete an earlier initialized candidate. Do not assume the B106 order is universal. Match current-session/turn and explicit references; duplicates cannot allocate a second token/record. Load hydration never fabricates a founding signal. Missing/conflicting/cross-turn/incomplete evidence holds that candidate without guessing; later save/load does not reconstruct missing session evidence.
4. Before old CityBuilt binding allocates a token or calls FreshBindingHook, consult an explicit fresh-candidate pre-write guard. Keep this separate from “durable store owns this city”: pending candidates do not yet have a readable authoritative record. Existing registered/held/recaptured records continue through their current workers. Unrelated legacy cities and old save restoration keep their existing paths. Unrecorded acquisition does not become a fresh candidate merely through Built; no Claim is added.
5. For admitted fresh targets, reuse the existing token allocator/binding ledger with a narrow verified-foundation entry. Do not invoke the old FreshBindingHook→Journal→Flow chain to establish new authority. Their guards must exclude this target before any permanent write. Token/binding allocation retains existing write/readback discipline and32-token limit; partial allocation/record failure becomes a diagnosed recoverable hold, not an invitation to retry blindly or fall back to old writers. It is not one engine-atomic transaction across Game/City properties.
6. Once the new Game record is committed/read back, the existing store read routes become authoritative and the candidate clears. Confirmed ownership loss before admission cancels admission and cannot create local specialization for a foreign city. An unassigned record transferred after admission remains held; full unassigned recapture is not silently inherited from specialized recapture code.

### State, schema and first completion

Current worker validate requires recognized specialization/baseP1; current Import requires existing specialized history. Neither is sufficient for new NONE/P0, and Import is not the new-city entry point.

Proposed compatibility contract: retain the outer schema2 collection/key/two-record limit and existing inner schema1 records unchanged. Use an explicitly versioned inner schema2 for newly admitted foundation records, including a compact founding provenance, origin/token, revision, and an explicit UNASSIGNED or SPECIALIZED progression phase. Lifecycle stage is separate: ACTIVE here means record service state, not specialization ACTIVE level. Missing fields on an old record never imply UNASSIGNED. Mixed old/new inner records are validated explicitly; no general migration or full archive rewrite. After first completion, the new record keeps its version/provenance and supplies the existing specialized fact shape.

- UNASSIGNED: specialization NONE, Potential0, no first completion, no investment receipts/pending debit; no abilities, investment eligibility or Network source. Confirm consumer behavior rather than representing this known state as read failure.
- First completion: existing GameEvents.OnDistrictConstructed path, current district complete/owner/reference checks and the four authorized replacement families. Placement does not lock. Persist specialization, baseP1 and first event together with readback; next/duplicate completions cannot replace the first.
- If a completion arrives during foundation admission, preserve its bounded scalar order/reference evidence for that target; validate/replay after admission in original delivery order. Do not discard then scan districts to choose identity. Reload cannot turn existing districts into new completion events. Missing evidence/overflow holds rather than selecting a convenient identity.
- Ordinary investment then reuses existing authoritative receipt/debit route; current Governor and Network remain derived. No old ACTIVE/route/sample restoration. Explicitly keep original-owner recapture and module-owned withdrawal for existing specialized records unchanged.
- Existing record at the location/reference, ambiguous token, full store, invalid binding or prior history prevents new admission. Do not delete/reuse former history or treat a razed-and-rebuilt location as the old city. This slice does not implement multiple historical generations per plot or destruction retirement.

### Bounds / participation

Keep the two-record test cap. Use at most one registered control before founding the new city; do not delete records from the accepted two-city save to make room. Capacity is checked before reserving a new writable registration, and rechecked before commit. Outside-cap cities are explicitly not part of this storage test; do not report them as registered or half-switch their writers.

Pending evidence/early-completion buffers have fixed small caps and no engine-object retention. Freeze exact caps in implementation constants and test overflow; they are diagnostic safety limits, not Gameplay restrictions. No per-frame/timer/hover/request-driven scans, no full-player city or unit scan to identify the new city. Generic Publish is not an admission trigger. With no candidates, related reconciliation does no work. Isolate candidate failure from already accepted records; do not invent a universal transaction engine or rewrite all existing collection-fault handling.

### Likely touched modules / retirement

| Module | Narrow responsibility |
|---|---|
| CityProgressionStore | Positive evidence coordinator, fresh entry/versioned validator, NONE/P0 read, first completion, persistence and per-target holds |
| BindingProbe | Reuse allocation after verified founding; prevent ambiguous CityBuilt pre-write for participating targets |
| FreshBindingHook / CityJournalProbe / CityFlowProbe | Pending/admitted target exclusion before old write/whole-player failure logic; keep unrelated legacy path |
| CityIdentityRead / EffectiveFacts / CurrentSpecializationFacts | Only if needed for explicit known-unassigned validation/read compatibility; no new rule/formula |
| Gameplay initialization / InvestmentAction | Verify listener ordering and existing routed eligibility; adjust only proven integration gaps |
| Existing diagnostics / P0Panel | Concise registration and first-completion result; no extra active request/polling/UI system |

Retire old Journal/Flow as writers **only for an admitted new Game-backed target**. Preserve their data and existing migrated-city rules; no global old-writer shutdown. B106 observer is not converted into permanent authority. No technical carrier added or removed by this registration batch.

### Validation and exit

W0004 L3, targeted affected persistence/event-order/first-completion routes only. Run actual Lua handlers with fixtures: both founding/init orders; missing enum/event; duplicate/invisible/foreign/unrelated reason; Built-before-transfer and split Publish; load hydration; full cap/reference/history conflict; pending failure and coldload; no legacy writes during admission; NONE/P0 save/load; early district completion; placement/incomplete/wrong-owner/non-v0.1; first valid notification wins; one investment/receipt only; existing B104 pair and B103 withdrawal/recapture regressions when touched. All syntax/manifest/integrity. No full historical regression or10k stress by default.

Minimal native scenario after implementation: separate test save with one registered control → found new city **without arming/migrating it** → report NONE/P0 → separate save/cold restart/load → complete one eligible district (Cheat allowed) → report P1 → invest once/report P2 → verify control unchanged → separate save/cold restart/load and verify. Two reload points cover distinct new states. No repeat trade/conquest unless implementation evidence justifies it. Diagnostic should show selected city, origin=normal founding, waiting/locked identity, Potential, receipts, and actionable reason; detailed event IDs remain optional.

Local completion requires exact mixed-schema/failure behavior documented and all relevant assertions passing. USER_GAME_TEST_PASS only after the above native flow. A missing or contradictory source event pauses the affected path, not silent fallback. This does not certify full E2 or all raze/rebuild/AI-city cases.

Rollback: B106 exact runtime plus untouched pre-implementation save. B106 is not promised to read inner schema2 records. No automatic reverse conversion. Future test deployment follows standing W0003 clean/exit/transaction/hash/recovery gates; **no deployment in this planning turn**.

### Authorization and exclusions

Plan ready for user review. No new Gameplay decision is required for this narrow slice. Runtime remains B106.133. Implementation is not started by the current planning authorization. No first AI-city snapshot/Claim, new cityKey, general migration, cap removal, AI/MP, Legacy invention, destruction-record cleanup, F or Design changes. After acceptance, propose remaining E2 work separately.


## B107.134 — authorized positive-founding registration implementation

User explicitly authorized implementation of Post-B106. This completes the narrow local implementation, **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED**, not all E2. D0035/A0161 and four-profession/local-human scope remain. B106 positive-event evidence is reused, not upgraded to native registration PASS.

### Implemented authority and boundaries

- CityProgressionStore automatically correlates Gameplay FOUND_CITY enum with current-session/turn Initialized/current city reference. Either delivery order works, including consumed/missing Settler objects and invisible notifications. No observer arm, Publish cutoff, timer, negative-event inference or UI claim. Built establishes an early pending guard before Binding; pending is separate from durable Owns.
- Existing BindingProbe allocation is reused after that proof;32-token limit and reserve→City token→confirm readbacks remain. No fresh-hook invocation. Coordinator does no player/unit scan. The allocator's pre-existing first-ever-ledger orphan-token safety scan remains only when the ledger is absent; it is not city identification or recurring reconciliation.
- Same Game property/outer schema2/two-record cap; existing inner schema1 is unchanged. Fresh inner schema2 stores founding provenance and UNASSIGNED/SPECIALIZED independently of ACTIVE/HELD lifecycle. NONE/P0/no first/no investment is readable known state, not unknown; no abilities or investment eligibility. Existing EffectiveFacts, CurrentSpecializationFacts and NetworkInput already accept this shape and need no formula changes.
- First valid completed four-profession/replacement district persists identity/baseP1/first event in one collection write/readback. Subsequent completions cannot change it. Pending early completions store primitive references in delivery order, then revalidate the first qualified event at admission. No load-time district scan or selection from present districts. First-completion read failure persists a hold, preventing a later district from silently winning after reload.
- Binding, Journal, Flow, FreshBindingHook and the old CompletionRecordProbe observation writer exclude pending/owned targets. The last is diagnostic rather than Gameplay authority, but must not keep writing an extra City record for the new path. Existing unrelated legacy writers remain. No new carrier/yield formula, Claim, cityKey, general migration, cap extension, AI/MP or F.
- Existing InvestmentAction operates on the Game-backed receipt ledger after P1; debit/duplicate protection is unchanged. Ordinary reads/diagnostics do not write. Specialized B103/B104 ownership workers are preserved. UNASSIGNED transfer becomes retained HELD and recapture is explicitly RETURN_UNASSIGNED_DEFERRED; no unapproved generalized recovery.

### Limits, failures and compatibility

Four pending candidates per session, eight distinct early completions per candidate, two durable records. Duplicates do not grow the buffers. Overflow holds fresh enrollment; existing accepted records continue. A full durable collection declines participation before allocating; outside-cap cities retain the pre-existing legacy path. Use a save with at most one registered control, never delete two-city evidence to make room.

Missing enum/hook, foreign/wrong/cross-turn/contradictory evidence, prior location/binding history, token conflict and partial allocation never trigger blind retry or legacy repair. Pending state is session-only; a save/load cannot reconstruct missing evidence. A confirmed token without an admitted record is diagnosed and requires the pre-foundation save/review, not automatic adoption. Errors with a known completion target hold that target; an unavailable district/city reference cannot safely identify a target, so it conservatively holds pending/fresh UNASSIGNED records only, not specialized/legacy records. A partial Game collection write keeps the inherited collection-wide fail-stop; this batch does not pretend an uncertain shared-property write can be isolated safely. Completed source and test saves remain available for recovery.

Readiness still requires normal LoadScreenClose; founding before that gate (including map/load hydration) is not retrospectively enrolled. This checkpoint's native fixture is a new city founded after entering the playable session. Exact event behavior outside the observed native path remains unproven.

Rollback: B106 runtime **plus a pre-B107 save**. Inner schema2 is forward-only in this checkpoint; no promise that B106 understands a B107 save. Binding/Game writes are verified sequential operations, not one native engine transaction.

### Local validation and native gate

Targeted L3 actual Lua handlers (`test_b107_e2_founding.py`): both orders, founding before city object, completion before Initialized/during binding callback, duplicate/invisible/foreign/wrong/missing event, split generic notifications, cross-turn, transfer negative control, prior history, cap/buffer limits, reserve/token/confirm/Game write failures, corrupt inner schema, failed completion retained across load, mixed schemas, known NONE Network facts, P0 and P2 coldload simulation, first completion/replacement/placement exclusion, actual investment debit/receipt/idempotence, unchanged control and no target legacy writes. B104 actual two-city test imports B103/B102/B101/B097/E2 regression: existing investment, loss/withdrawal, recapture, per-city isolation and load contracts pass. B105/B106 observer/actual request ingress plus all Lua compile/manifest checks pass. No full historical or 10,000-event stress suite; no new engine PASS is claimed.

Minimal user test: keep a separate pre-B107 save with ≤1 registered control → found normally without arming/migrating → select new city and left-click **E2往返**, expect normal-founding/NONE/P0 → separate save, fully exit/relaunch/load and recheck → complete one eligible district, expect chosen identity/P1 → invest once via the existing action, expect P2/one receipt and unchanged control → separate save, fully exit/relaunch/load and recheck. Do not use in-session reload for this test given the independently recorded crash. If held, capture the short report and stop; do not repeat migration. No repeat trade/conquest required here.

New report example: `新城进度 / 来源：正常建城 / 等待首个合格区域完成 / Potential0 / ACTIVE0 / 投资0`; after completion/investment: `专业已锁定：RESEARCH / Potential2 / ACTIVE[当前事实] / 投资1`. Old observer remains opt-in, not authority. Native gate covers automatic event/write timing, engine save persistence and real consumer activation. Stop for review; no Claim/F.

Historical validation tooling note (limitation repaired in current [Workflow helper](../../Workflow/README.md#schema-template-and-maintenance); original result below retained): W0001 `check P0-E2` PASS. Its generic `self-test` is not applicable to this manifest: existing helper requires an `expected_id` context entry and exits StopIteration when absent; no workflow code was changed and no self-test PASS is claimed. Runtime targeted tests above are independent.


## Post-B107 — remaining E2 plan / new-path isolation over migration compatibility

2026-09-26, documentation only under user request to organize remaining work. No runtime changes or deployment. This supersedes the remaining-work ordering proposed before B104/B107 and the mandatory status of the old/new mixed native test; historical evidence is not relabeled or deleted.

### Why the mixed migrated/fresh native test is not a required gate

The user correctly identifies the intended endpoint: future participating cities use the authoritative Gameplay save service, and normal progression no longer depends on the historical City Journal/Flow writers. A mixed inner-schema1-import/inner-schema2-fresh test principally tests a transition compatibility adapter. It is not the product's defining correctness requirement. Remove that test from the current required user-test queue and retain existing targeted local compatibility regression while the adapter remains. Do not claim a native PASS for a test that was removed.

The mandatory invariant is **city A's first completion/investment/loss must never mutate city B's identity, Potential, receipts or activation inputs**, followed by save/load retaining each independent record. Global storage alone does not prove this: lookup key/ref collisions, a shared pending slot, stale record replacement or collection-wide error handling can still mix or block cities. Test this using only new-path cities, not by searching for old migration saves.

Current code is still transitional: durable collection cap2; outside-cap fresh cities fall back to the legacy path; BindingProbe's allocator caps32 and indexes records by current CityID; per-record binding snapshots contain the whole former binding ledger; each write clones/readbacks the whole progression collection using the evidence-copy node/byte limits. Therefore simply removing cap2 is unsafe. With many newly founded records, repeated binding snapshots can grow approximately quadratically. The new-path scale and write boundaries must be made explicit before global cutover. These are static code findings, not a new measured runtime incident.

“Global authority” means authoritative saved Game-side state with explicit per-city routing. It does not require every profession's future ledger/contract to live in one ever-growing Game Property, nor does it authorize a generic database/transaction framework. Only progression authority and exact consumers are cut over here. Reusable allocation, validation, current-fact and investment logic can be adapted; old filenames do not by themselves make a module obsolete.

### Save support proposal

Recommend a **new-test-game-first cutover**, consistent with the existing implementation plan's save policy. No automatic full old-save conversion is required for this milestone; no demand that B094–B107 development saves stay playable across an incompatible schema change. Preserve all existing saves/evidence/runtime recovery points; never rewrite/reinitialize unsupported saves. The future implementation must explicitly identify its supported save/schema range, detect old/unknown state and stop with a readable explanation rather than falling back to old writers. This is a proposed support contract for the next authorization, not a change to B107's current behavior. Any B107 forward migration is a separate, proven opt-in scope, not a hidden requirement.

### Remaining slices in dependency order

These are slices of P0-E2, not new profession batches or implementation permission.

| Slice | Goal and scope | Dependencies / old paths | Local acceptance | Minimal native gate / exit |
|---|---|---|---|---|
| 1. New-game multi-city authority and old-writer cutover — recommended next | Make every supported normally self-founded local-human city use Game-backed progression; remove the experimental2-record fallback and replace/adapt the32-city DEV allocator restriction safely; compact each city's identity evidence; version/save boundary; route first completion, receipts and current facts through one authority. Keep record/ref collision checks, no new universal cityKey framework. | B103/B104/B107 evidence. Binding allocator/CityProgressionStore; exact old Journal/Flow/FreshHook/CompletionRecord and load/manual entry points; EffectiveFacts/Investment/Network/Standardization routes only as required. Disable normal legacy writers/fallback in the new supported save mode; isolate import as development compatibility, not default gameplay. | Targeted L3:1/2/4/8/33 cities (33 specifically crosses old32 limit); stable unique IDs, identical numeric IDs under different owners, no receipt/record cross-write, per-city pending, P0/P1/P2 reload, existing loss/return regression; inspect serialized size and actual copy/read/write counts rather than blanket stress. Validate finite/corrupt input bounds without retaining experimental gameplay caps. No generic pulse/hover scans. | One new test game with3 cities: leave A unassigned/P0, complete distinct legal districts in B/C, invest only B, then one coldload and check all3. This covers beyond2, no cross-city state, retained NONE and invested state in one flow. It replaces the old-migrated/new-city user test. Exit: new-mode cities never silently return to old writers. |
| 2. First no-history AI conquest snapshot | On confirmed conquest completion, distinguish retained own history from a genuinely never-specialized AI city; freeze the four-profession completed-district LegacySet once. Persist FIRST_COMPLETION versus LEGACY_CLAIM mode; empty set uses future completion, nonempty set waits without automatically choosing. No Claim action yet. | Slice1 routing; existing positive conquest/transfer evidence, local-human scope, PROG-006–009. Absence of a key alone is not proof of no history; fresh-save provenance and retained/HELD records must be checked. AI/Free City/unknown-history acquisitions are not all treated as the same case. | Snapshot once, incomplete district excluded, later district doesn't append, duplicate/load safe, old specialized return bypasses snapshot, known-empty vs UNKNOWN, no native-pulse completion inference. | Small controlled conquest fixture with completed candidates and a no-candidate target only where local facts cannot establish engine timing; one saved outcome. Reuse existing event evidence; don't repeat token investigation wholesale. Exit: reliable persisted mutually exclusive initialization modes. |
| 3. Claim completion | Offer only frozen candidates; completion locks one identity/P1 and removes other choices; preserve existing investment thereafter. Never use current districts to enlarge candidates. | Slice2; accepted PROG-007/008. Claim's extremely-low-cost vs1-turn realization and exact cost/primitive must be resolved before this slice, not invented by Architecture. | One winner, duplicate action/load safe, ordinary first completion excluded while awaiting Claim, noncandidate rejection, no reset of existing specialized Potential. | Choose one candidate and confirm alternatives disappear/P1 persists, integrated with the snapshot fixture if feasible. Exit: nonempty conquest path usable. |
| 4. Remaining lifecycle gaps, individually scoped | Resolve new-schema city loss/recapture compatibility and unassigned-origin return; actual destruction/retained history versus independently confirmed new founding at the same location; current reference indices must not attach former history to a new city. Keep permanent history and module-owned withdrawals distinct. | Existing proven B103 loss/return, slice1/2 mode persistence. Do not infer razing from removal/no successor. New historical-generation routing requires its own narrow technical plan; current B107 holds remain until implemented. Unknown diplomatic acquisition boundaries remain marked, not inferred from conquest. | Replay real event sequences, confirmed destruction vs transfer, old/new reference collisions, no historic resurrection, coldload; preserve original-owner and profession-specific Legacy restrictions. | Only newly unproven native paths get a short reproducible fixture. No random-disaster/AI-razing homework. If destruction cannot be induced/read reliably, document that exact support limitation instead of certifying it. Exit: supported lifecycle matrix explicit; remaining limits reviewed rather than silently treated as solved. |
| 5. E2 closure / review F readiness | Audit remaining direct old-property dependencies and supported save/mode contracts; ensure UNKNOWN/HELD/REALLOCATING are not ordinary NONE; remove temporary migration controls from the normal path. Review evidence and performance bounds. | Slices1–4 and accepted limitations. REALLOCATING action still belongs to Commerce; do not build it here. Profession-specific future permanent systems remain with their own batches. | Static writer/start/load/manual-route checks plus only affected regressions; relevant failures remain explicit. No release-grade all-history suite by default. | Reuse previous evidence; no automatic repeat test. Exit: review whether P0-F can safely begin. Not automatic authorization to implement F. |

### Next slice boundaries and stop conditions

Slice1 is the next recommended authorization, not immediate Claim or F. It has one coherent outcome: a supported new game uses the new progression authority for all normal self-founded cities, without dependence on migration UI. No new yield/carrier/Design, AI/MP, conquest snapshot/Claim, generic Legacy inheritance, profession gameplay, automatic old-save conversion or destruction-history cleanup in that implementation.

Before code, freeze the compact record/allocator and supported schema contract in this existing plan/manifest, using the actual affected writer closure. Do not merely raise Copy's evidence budget and caps. Preserve bounded serialization validation and distinguish session pending data from persistent records; do not retain full historical binding ledgers in every new city record. Reuse token provenance/event evidence where sufficient; no name/coordinate-only identity and no guessed CityID. Exact Game-property layout is an implementation choice to be justified by size/write and recovery checks, not a new design system.

If code review finds an unavoidable new identity assumption or unsupported old-save ambiguity, hold that branch and report. Claim primitive/cost is a later gate, not a reason to delay the normal multi-city slice. No new Gameplay decision blocks preparing/authorizing slice1 under the proposed fresh-save contract. Authorizing implementation of that plan would also accept its clearly stated new-save support/rollback boundary; this planning request alone does not change runtime support.

### Updated test economy / next action

Cancel the standalone old-import/new-fresh native compatibility task as a required product gate. Keep local compatibility assertions while that adapter exists. P0-only coldload is not retroactively marked PASS; combine it with the3-city new-path test above. Existing B103/B104/B107 scoped native results remain valid, not universal coverage. No user testing now, no request to locate old saves. Wait for authorization of slice1; then stop at its acceptance boundary.


## B108 authorized new-game multi-city cutover — contract before implementation

User authorized slice1 on 2026-09-26. L3 scoped persistence validation. Production Start uses a new versioned Game index plus one Game property per city record; index stores only immutable origin/allocated token, record owns progression/receipts/templates/current ownership. Reuse DEV-B013 token format as opaque compatibility identity, with monotonically allocated serial and compact one-city binding evidence (no player-wide ledger embedded). No new universal cityKey. Allocation reserves the index before token/record writes; incomplete reservation holds that city across load, never retries or falls back. Existing-record writes touch only that record, with stale/readback checks. Index changes only on registration; size bounded by native map plots, per-record existing evidence budgets retained. Historical destruction/reuse remains held.

New-save contract: existing new index loads read-only; absent index initializes only after LoadScreenClose when native IsSavedGame is explicitly false, local enabled human has zero cities, current turn equals configured start turn, and no old progression/binding authority exists. Missing primitive/old/unknown save holds without changing it. No old-save migration. Native initialization primitive remains USER_GAME_TEST_REQUIRED. Production BlocksLegacy covers every city; no old Journal/Flow/Completion/Binding allocation, import or fallback, including unregistered/unsupported cities. Historical adapter remains a test-only explicit entry, never dispatched by Gameplay/UI. Existing facts/investment/withdrawal/recapture workers reused. No new Gameplay effects/Claim/F.


### B108.135 implementation result / evidence boundary

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS**, not native PASS. New-game production Start now exclusively uses `SPC_PROGRESSION_INDEX_V3` and `SPC_PROGRESSION_CITY_V3_<existing token>`; index contains immutable origin + serial, each record stores only its own compact binding, first completion, investment receipts, template history and current ownership evidence. No new universal cityKey or profession Legacy policy. Existing history/tokenless-return validator and module-owned exits remain. Two-city/32-city experiment caps do not apply to this mode. Index and pending positions are bounded by native map plot count (historical location reuse remains deferred); each record retains existing8,192-node/65,536-byte copy limits, not a whole-empire budget. Per-record writes do not copy/write the other records/index; origin/reference conflict check is O(C) on meaningful writes only. Registry copy/write is O(C) only when allocating a new city; per-city binding size constant. Native lifecycle dispatch still visits registered workers on existing city events; no per-frame or hover work added.

Old path cutover: production disables Binding CityBuilt, CompletionRecord/Journal/Flow completion listeners and old Binding/Journal/Flow load scans. All legacy writer guards also reject the new mode's unregistered cities. CityFlow/EffFacts, investment and Standardization resolve through the new store; Network may not reinterpret missing old Flow as known NONE in new mode. Migration UI hidden; stale/manual import action returns a clear refusal. Source, test adapter and historical saves remain preserved; `StartLegacyTest` is used only by historical fixtures, never by Gameplay/UI dispatch. Other gameplay formulas/carriers are unchanged.

Allocation transaction: reserve compact index → write/readback city token → write/readback own record. Partial reservation is retained across save/load and held, not retried/reset. Existing-record failure holds that worker, leaving unrelated records untouched. Corrupt shared index / ambiguous references still stop the shared authority, intentionally. Existing conservative un-attributable first-completion failure may hold unassigned records rather than invent order; not advertised as independent fault recovery for every engine failure. UNASSIGNED recapture and destroyed-location reuse remain later lifecycle scope.

Native primitive evidence: installed vanilla `Base/Assets/UI/FrontEnd/LoadScreen.lua` uses `GameConfiguration.IsSavedGame`; installed Gameplay `DLC/PiratesScenario/Scripts/PiratesScenario_StartScript.lua` compares current turn with `GameConfiguration.GetStartTurn`. This is STATIC evidence of APIs, not confirmation of IsSavedGame in this Gameplay context/timing. Missing/unknown API is a no-write hold with a diagnostic. User test must confirm fresh-game initialization and persisted Game properties; if it fails, stop and capture the short report, do not use old migration.

| New-path cities | Aggregate test encoding chars (not native save size/RAM) | Index writes incl. initial empty index | Coldload writes | Idle writes |
|---:|---:|---:|---:|---:|
|1|526|2|0|0|
|2|1108|3|0|0|
|4|2216|5|0|0|
|8|4504|9|0|0|
|33|18802|34|0|0|

Actual production Start test: normal founded P0; distinct first completions; investment only one city; duplicate requests; stale cross-city preview;1/2/4/8/33 scaling; one-cell binding; no old City records/Game binding ledger; coldload P0/P1/P2; only target record writes; actual Industry template consumer and reentrant first completion; readback/corrupt-record isolation; index/old-save/missing API rejection; reservation/token/record failure; investment INTENT/CONSUMED/receipt failure windows; foreign identical numeric CityID; HELD coldload and retained-token/tokenless strict-chain recapture; current Governor ACTIVE and current Network capture. Actual21 module-owned exit lists /2,302 unique internal IDs and Network invalidation regression pass. Historical B103/B104/B107 adapter regression preserved; this does not grant old saves production support. All Lua compile and modinfo135 static checks pass. No broad unrelated gameplay/stress suite.

Minimal user test — **new test game required**, use current build visible in report:
1. Normally found3 cities. Leave A without a four-profession district (NONE/P0). Complete Campus in B and Theater in C; expect each own P1. No manual registration.
2. Invest only B once with the normal existing investment action. B=P2; C=P1; A=P0. ACTIVE follows actual Governor and need not equal Potential.
3. Save separately, fully exit/restart/load once, select each city and left-click **E2往返**. Verify A=P0, B=Research/P2/one investment, C=Culture/P1/no investment. Send these three short reports; stop on any hold. No trade/conquest/old migration save requested.

Rollback: exact B107 runtime recovery plus a pre-B108 save/new game; do not promise B108 saves load under B107. No Design/main/Claim/F changes. Next authorization only after native checkpoint review; no automatic next slice.

Deployment: B108.135 source `c056eae`, W0003 authorized temporary develop deployment,153/153 MATCH; B107 full outgoing recovery verified through the existing restore/switch transaction. Receipt `B108.135-c056eae-playtest.json`. Main unchanged; game verified exited, never launched. Native gate remains pending.

## B109.136 — start-enabled initialization repair

Authorized 2026-09-27 after B108 native failure. User explicitly clarifies: supported games enable this Mod from game creation; no compatibility/migration for saves started without it, and no old development-save compatibility project. This is save-support scope, not changed Gameplay Design. Normal saves produced by the supported new-game path must still load correctly.

B108 line623 called UI-side `GameConfiguration.IsSavedGame()` in Gameplay and failed natively. B109 removes that call. No UI bridge/provider, heuristic migration, or new state schema is added. The briefly explored UI reader was uncommitted and not retained. Existing valid index loads read-only. When absent, LoadScreenClose may initialize only at configured start turn, with exactly one enabled local human and zero cities, no old progression/binding ledger, confirmed absent index, and write/readback verification. Unsupported mid-game saves with cities/advanced turn are rejected; no claim to distinguish an unsupported empty start-turn save from a genuine new game. Corrupt index/partial reservations still hold. There is no unconditional absent-index initialization or legacy fallback. All remaining B108 independent-record, investment, ownership and event contracts remain.

Changed runtime: CityProgressionStore initialization plus shared short FailureReport; EffectiveFacts diagnostic uses that report before read; Probe/modinfo stamps109.136. No yield/carrier/AI/Claim/F/Design changes. No repeated UI requests, extra event hooks, polling or scans. Failure display is four concise lines with version/reason/action rather than nested stack traces.

W0004 L3 targeted evidence: `DevelopmentTests/test_b109_session_origin.py` executes actual B108 production cases with only build-stamp and two explicit origin-gate assertion adaptations. The removed IsSavedGame gate is no longer expected to reject nil; missing-index existing-city rejection is now tested instead of promising unsupported empty-start-save discrimination. Original B108 test remains byte-identical. Additional cases: missing/throwing IsSavedGame not called; Research/Culture first completion; one-city investment and coldload isolation; duplicate LoadScreenClose no writes; supported empty-index reload at later turn no writes; missing start API, advanced turn, existing city and old binding no adoption; concise failure from both E2 and specialization reports. All Lua compiles; modinfo136 parses. STATIC_CONFIRMED / LOCAL_SIMULATION_PASS only. No unrelated full historical regression/stress.

Native gate: new test game underB109, three normally founded cities A=NONE/P0, B=Campus ResearchP1, C=Theater CultureP1; invest only B once→P2; save separately, fully exit/restart/load and read three E2 reports. ACTIVE follows actual Governor. Stop on any hold; do not reuse the failed B108 city's uninitialized save. Initialization with current native GetStartTurn/timing and native persistence remain unverified until user test. No trade/conquest/Claim test added.

Rollback through existing exact runtime transaction; returning to B108 returns its known initialization defect, not a claim it is a working new-game baseline. Earlier B107 recovery remains preserved. No new save schema or promised old-save compatibility. Next work waits for native result; no automatic next slice.

Deployment: B109.136 source `2da80ce`, user confirmed game exited, W0003 exact B108 restore/stable bridge then activation;153/153 MATCH, receipt `B109.136-2da80ce-playtest.json`. B108 complete outgoing recovery hash verified. No game launch/main change; native gate pending.

Native evidence update 2026-09-27: [three-city reports](../../Status/Validation/Results/Specialization_B109_E2_Three_City_Result.md) show A=P0/ACTIVE0/investments0, B=ResearchP2/ACTIVE1/investments1, C=CultureP1/ACTIVE1/investments0; registry3, no initialization failure. Scoped visible-state USER_GAME_TEST_PASS; full exit/restart/load confirmation pending, not inferred from screenshots. Left-click E2 reporting confirmed; no right-click retest. Prior native-gate prose above records the original test requirement. No implementation/deployment or next-slice authorization.

## Next slice — first AI conquest snapshot (plan only)

2026-09-27: user confirmed B109 full restart/load, then requested next plan. [Scoped acceptance](../../Status/Validation/Results/Specialization_B109_E2_Coldload_Confirmation.md) closes slice1; this section supersedes its historical “next” dispatch only. **PLAN_ONLY / IMPLEMENTATION_NOT_AUTHORIZED**. No new build assigned, no deployment. Formal rules: current Spec ELIG-004/005, PROG-004–010; four-profession/local-human/supported-start-enabled scope unchanged.

### Goal and exact boundary

For a genuinely no-specialization-history AI city first conquered by the local enabled human, persist a single conquest-completion snapshot of completed eligible district families. Nonempty LegacySet waits for future Claim; empty LegacySet enters normal subsequent first-completion. No automatic profession selection. This slice makes these mutually exclusive states reliable; it does not make the nonempty route playable through Claim yet.

- Prior own persistent records, HELD/ambiguous references and reserved/incomplete records must be checked before enrollment. Missing City property/token/index entry alone never proves no prior history. Supported-session provenance, positive conquest/transfer evidence and absence of conflicting retained records are required together. Existing specialized recapture goes through its existing path unchanged.
- Correlate positive conquest evidence with actual completed ownership transition and currently readable local-human city. Reuse existing native sequence evidence; never assume first PublishComplete is a transaction boundary. A partial/cross-turn/contradictory chain or district-read failure holds the candidate with a reason rather than scanning at arbitrary later time or guessing an empty set.
- One snapshot of completed Campus/Theater/Industrial/Commercial families, including accepted replacements, deduplicated by specialization. Under-construction districts excluded. Do not manufacture building/Governor requirements or treat a completion/load pulse as prior history. Native completeness/ownership reads must be reviewed at implementation.
- Persist conquest provenance, frozen candidate set and explicit initialization mode with the existing independent Game record/index authority. Do not create a new cityKey, copy historical snapshots, or fall back to old City-property writers. Define record-version/readback/partial-write handling before mutation; valid B109 start-enabled saves must retain existing records unchanged. No pre-Mod/old-development-save migration.
- Nonempty: retain NONE/P0 with a clear “待认定” mode; later buildings/districts do not append candidates or lock Identity. Reject Settler investment until identity exists. No Claim UI/project/cost in this batch.
- Empty: retain NONE/P0; only a valid completion after the confirmed acquisition boundary can lock one Identity/P1 in native delivered order. Duplicate/load notifications do not replay. Existing investment thereafter uses the normal path.
- No AI activation, trade/gift acquisition generalization, Free City generalization, unassigned-origin recapture, destruction/location reuse, new Legacy policy, new yields/carriers, Claim or F. Deferred routes remain explicit; unsupported acquisition is not silently classified as conquest.

### Implementation touch points and dependency review

Current CityProgressionStore production founding admission requires FOUND_CITY+Initialized; conquest events currently route to existing workers. Adapt this exact store/admission/completion/save path rather than bypassing it with a new allocator. Inspect Gameplay request/start routing and existing EffectiveFacts, CurrentSpecializationFacts, InvestmentAction, NetworkInput and Standardization consumers of no-identity/unknown facts. Most should remain unchanged; add only explicit new-mode handling where required. Existing owned withdrawal/recapture routes remain intact. Confirm direct caller/old-writer closure and narrow the active manifest to this slice before authorized implementation; the prior manifest is not automatic authorization or a final reviewed dependency set for new code.

Diagnostic uses existing left-click E2 entry: selected city, acquisition confirmed/pending, mode, frozen candidate names (or empty), Identity/Potential, and one actionable refusal reason. Event details remain right-click/on-demand. No continuous verbose report, per-frame/hover requests, recurring world scans or AI city registration. Event-bound candidate work and snapshot once; persist mode, not stale ACTIVE/Network.

### Verification and exit

W0004 **L3**, limited to affected persistence/lifecycle consumers:

1. Static exact registration/writer/consumer routes, four-family mapping, build/version and save-schema checks.
2. Local actual-handler simulation: completed/incomplete/duplicate replacement candidates; empty versus unreadable; no later append/mode switch; valid completion order only after acquisition; duplicate/reload idempotence; interrupted write/readback fails closed; retained specialized/HELD/reserved histories bypass or reject enrollment; unrelated B109 cities/receipts untouched; existing withdrawal/recapture and B109 founding/investment regression.
3. Minimum native fixture after authorization/implementation: one controlled test game, two AI cities—one with a completed eligible district (ideally also one incomplete), one with no completed eligible district. Conquer using the actual conquest route, not trade. Left-click reports must show frozen candidates versus normal first-completion. In the candidate city complete a different eligible district: candidates unchanged/NONE; in the empty city finish one: corresponding P1. One full restart/load and both short reports verify persistence. If fixture creation is difficult, first review available controlled setup rather than asking for random AI behavior or redoing unrelated tests.
4. Exit: local checks plus the scoped native reports demonstrate reliable acquisition-time snapshot, mutually exclusive modes and persistence. Until native timing is proven, label LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Inability to prove transition completeness or no-history provenance is a technical stop, not permission to use name/coordinates or delayed guesses.

Rollback: existing deployment recovery transaction; preserve pre-slice save and previous runtime. A new record mode must not be promised readable by B109—roll back package together with its pre-slice save. No deployment in planning.

### Following slices and decision boundary

After this checkpoint, separately plan Claim selection/completion (PROG-007/008), then remaining lifecycle gaps and E2 closure/F readiness. Claim's exact low-cost versus one-full-turn realization remains TBD and must be made concrete before that implementation, not invented here. No new Gameplay decision blocks this snapshot-only plan; any evidence ambiguity is a technical gate. Waiting for explicit user implementation authorization.

## B110.137 — authorized conquest snapshot checkpoint

2026-09-27 user authorized the previous snapshot-only plan and reaffirmed PROG-007/008: **only completion of the corresponding city Claim Project establishes specialization, even with exactly one candidate; never auto-select**. This is existing-rule confirmation, not a new Design revision. Claim actions/cost/UI remain outside B110. Project-click/overflow investigation is [read-only and separate](../../Reports/Technical/Specialization_Project_Action_Interception_and_Full_Turn.md).

Runtime changes only CityProgressionStore plus Probe/modinfo stamps. New inner record schema3 carries acquisition evidence, frozen four-family LegacySet and FIRST_COMPLETION / LEGACY_CLAIM mode; existing schema2 founding records/index3 remain unchanged and readable. Existing record storage/reservation/readback and exact retained-location checks reused. No new cityKey, carrier, yield, AI activation, generic inheritance or City-property fallback. Existing consumers read NONE/P0 as before; InvestmentAction rejects NONE and Network gets ACTIVE0. No new benefits for pending Claim.

Admission requires a supported initialized index, current local-human target, original AI-major/nonhuman player, positive CityConquered → CityAdded → CityInitialized → CityTransfered ordered same-turn evidence, matching current reference, no existing/reserved/HELD position and no old Mod properties. CityBuilt alone never qualifies. Snapshot city districts once at confirmed transfer; only complete recognized families/replacements enter the set. Unreadable/incomplete/conflicting evidence holds without guessing. Trade/free-city/general acquisitions remain excluded. Timing reuses the observed conquest chain but first-no-history-city native timing is still unverified.

Nonempty set stays NONE/P0 with Chinese candidate names and “待完成对应认定项目（本批尚未开放）”; later completions cannot append or specialize. Empty set accepts only subsequent valid completion, with same delivered-order/P1/investment contract. Pre-transfer buffered completions are discarded in favor of the acquisition snapshot; valid reentrant post-boundary completions replay in order. Saved mode validated on load; no re-scan. Duplicate acquisition cannot reserve another identity; interrupted reservations remain held across reload. Unassigned recapture remains deferred.

W0004 L3: actual Lua-module `test_b110_conquest_snapshot.py`, inherited B109/B108 production tests with version-only adaptation, plus single/multi/empty/replacement snapshots, incomplete/unknown exclusion, no later append, investment rejection, subsequent P1/P2 persistence, unrelated-city isolation, duplicates, trade/human/nonmajor refusal, existing-history bypass, missing/cross-turn ordering, read failures, partial write/corrupt mode, reentrant post-boundary completion. All Lua syntax/modinfo137 checked. **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS**, not native PASS. Expected negative-case held logs are test fixtures, not observed native failures.

Current direct caller closure: Gameplay Start/left-click routing, CityFlow/Binding modern guards, EffectiveFacts/CurrentSpecializationFacts, InvestmentAction, NetworkInput, Standardization. Their formulas/ownership routes unchanged; schema3 supplies the same base/receipt shape. The reviewed prior module-owned withdrawal/recapture regression remains relevant. No unrelated full regression/stress.

Minimal native test after deployment: separate supported test save, two actual AI conquest targets, one with completed eligible district and another with none completed. Report left-click E2 immediately; nonempty remains NONE with fixed candidates even if singleton; later different district cannot enlarge it. Empty target later completes a legitimate district→P1. Save, fully restart/load once, two reports. No Claim project expected yet. Stop on a hold and retain the report; do not trade as substitute or manually register. Keep pre-B110 save: B109 is not promised to read new inner schema3. Deployment pending game-exit confirmation at implementation commit; follow Status/receipt for actual live state.

After scoped native acceptance: separate Claim plan and its exact cost/one-turn realization; no automatic implementation. No new Gameplay decision needed for this checkpoint.

B110 source commit `8bebf5a` pushed. Process inspection unavailable (sysmon/pgrep cannot list processes); awaiting user exit confirmation. No deployment occurred in this implementation turn; recorded live remains B109.136.

Deployment update: user explicitly confirmed game exited. B110.137 activated from clean HEAD `621d69c` (implementation `8bebf5a`) through exact B109 restore/stable bridge;153/153 source/runtime MATCH and retained B109 recovery hash MATCH. Receipt `B110.137-621d69c-playtest.json`. No game launch/main change; only scoped native test remains.

## B110 native failure — district enumeration repair proposal

[两图失败证据与原始hash](../../Status/Validation/Results/Specialization_B110_E2_District_Enumeration_Failure.md)：2026-09-27两城均在admit区域枚举Members调用失败。原本LOCAL_SIMULATION_PASS保留其历史范围，但fixture不符合原生CityDistricts接口，不能作为该接口有效证据。当前USER_GAME_TEST_FAIL。

待授权的最小修复：采用现有DistrictCompleteness indexed API，保留征服证据/一次快照/owner与完成性保护；fixture去掉Members并提供零起始indexed接口，定向覆盖候选与失败关闭并复用B109直接回归；报告仅显示相关阶段及原因。无identity/Design变更，无Claim/F或失败后补扫。用户已有征服两城前存档；未来修复/部署后从该存档重复两种分流及完整重启，当前不再测试。本次只归档证据，未实施修复或部署。

## B111.138 — indexed district snapshot repair

用户授权修复B110原生区域遍历失败。只改CityProgressionStore的征服候选读取与失败报告：Gameplay CityDistricts.GetNumDistricts/GetDistrictByIndex（零起始），保留数量合法性、条目、owner/reference、去重与完成性检查；错误仍暂停且不猜测空集。一次快照/保存schema/候选分流/单候选不自动确认等合同不变。阶段标记仅session诊断，无新永久state。失败报告保留阶段与单行原因，内部原始错误保留，不再把堆栈搬上面板。

STATIC_CONFIRMED：与现有DistrictCompleteness Gameplay读取API一致，Lua语法/modinfo138通过。LOCAL_SIMULATION_PASS：test_b111_district_snapshot.py使用无Members的indexed fixture，覆盖零/单/多/未完成/特色替换、非法数量/缺条目/读取异常/错误owner/重复ID、无写入fail-closed及简短错误报告；继承B110分流/保存/幂等/写失败用例和直接B109/B108生产回归（含现有loss/return）。未跑无关全历史或stress。本地不替代原生验证。B110失败原图/报告保留。

最小原生复测：从用户保留的征服两城之前存档开始，征服后分别左键E2，记录候选集/分流；非空（含单个）保持NONE/P0，不操作尚未实现的Claim；空集在后续完成首个合格区域时P1。保存到新槽，完整退出再启动读档，复查两城。原测试城市若不能覆盖某一分流，只报告未覆盖，不冒称PASS。任一错误立即暂停并截图。不可从失败后状态补扫历史，不要求重建局。

W0004：L3但仅直接保存/分流回归。无新Design/收益/carrier/Claim/F。用户已确认游戏退出并允许部署，需提交后完成安全部署与receipt核验；当前源包与live状态以Status/Authority为准。

B111部署结果：用户确认游戏已退出；从clean source `0ffbfdb`完成安全切换，153/153 MATCH，receipt `B111.138-0ffbfdb-playtest.json`；B110完整恢复点hash一致，main未变，未启动游戏。仅等待上述原生复测。

## B111 native acceptance — frozen candidates and empty-set completion

[六图验收](../../Status/Validation/Results/Specialization_B111_E2_Conquest_Snapshot_Pass.md)：城市1商业单候选→后建工业区仍待Claim/P0；城市2空候选→剧院完成文化P1；用户确认完整重启后两城保持。USER_GAME_TEST_PASS仅上述范围，城市2投资可用另有用户陈述，图中仍投资0。当前最小门禁关闭，无需重复。原生未覆盖的多候选/异常/其它生命周期不扩大PASS。

下一建议仅为Claim项目认定最小计划；用户审核后另行授权实施。现有候选资格不变，单候选也必须完成项目。E2仍partial，不自动Claim实施/销毁/未专业城夺回/F。本次只有证据归档与状态维护，没有runtime/Design/部署修改。

## Next slice — Claim project plan after B111 acceptance

Status: PLAN_ONLY / AWAITING_USER_REVIEW_AND_IMPLEMENTATION_AUTHORIZATION. 用户本轮授权准备计划，不是实施。基线B111.138，双城快照/后续完成/完整重启限定PASS；不重复该批测试。正式规则为当前Spec PROG-006～009，用户再次确认候选即使只有一个也须完成对应城市项目。

### 目标与已接受合同

仅对本地人类玩家的已确认ACTIVE记录、schema3 acquisition.mode=LEGACY_CLAIM、progression=UNASSIGNED、Identity NONE/P0且无保存/完成错误的城市开放。四专业候选只取保存的LegacySet；不按当前新建筑追加，不自动选单候选。玩家可以一直不选。空集城市、已有专业、自建城、UNKNOWN/HELD、AI/自由城均不能走Claim。

每个候选对应一个真实生产项目。**完成**任意一项才建立对应Identity与Potential1；其余项目撤下。之后重新派生ACTIVE/当前网络，走既有local consumer，不直接写收益快照、不发额外投资成果。不恢复旧时代/历史成果或为AI补造专业。

### 建议参数与操作呈现（待本计划批准）

建议首轮采用四项目各 **基础Cost=1 Production / NO_PROGRESSION_MODEL**；名称使用功能性“认定科研／文化／工业／商业专业”作为开发测试文案，不升级成新正式能力名。PROG-008允许极低成本或1-turn确认，本方案选择前者；不是固定完整回合方案。原生游戏速度及项目完成行为需验证，不承诺任意环境下精确一回合。

保留普通生产、既有溢出/收获等原生项目完成途径，不新增生产来源限制。若生产使项目同回合完成，仍以真实完成事件认定；点击/入队本身不写Identity。**Cost=1是待用户审核的实施/平衡建议，不修改当前Design TBD，不在本轮实施。** 不复用商业Project-as-trigger绕过生产，也不把时代对话完整回合门槛转嫁给Claim。

### 最小技术路径与直接依赖

| 模块 | 计划改动 / 必须核对的调用关系 |
|---|---|
| CityProgressionStore | 新增专用Claim提交入口，复用当前record-local保存/readback/revision及身份核验；保留旧acquisition与冻结set，不调用普通Complete冒充区域刚建成 |
| 新ClaimProjects小模块 + SQL/Text | 四项目定义与准确的项目ID→专业映射，原生项目完成事件入口；无generic project engine、无新收益modifier |
| Gameplay / modinfo | 接入单一完成监听及当前有界dirty audit；不增加轮询、hover请求或第二套保存authority |
| EffectiveFacts / InvestmentAction / CrewProjects / Standardization | 核对base.first、专业区域引用和永久写后重算的真实依赖；相同数据合同可复用，不能只设置Identity字符串就宣布兼容 |
| 精确退出 / 隐藏规则 | 若采用下述access marker，纳入module-owned撤销、呈现隐藏与ordinary-building排除，不能按前缀批量删建筑 |
| 定向测试 | 新Claim实际handler模拟，复用B111已冻结候选/空集分流及既有投资/保存相关回归；只改版本断言，不削弱旧断言 |

入口可见性的最小候选：复用CrewProjects已有 **Projects.RequiredBuilding + 无收益技术access marker** 路径，按四种冻结候选分别维护访问标记，避免单一总标记错误开放全部专业。标记只表达派生资格，不保存Identity/选择；不提供住房、岗位、普通建筑层级或其它收益。新建/加载/已确认ownership loss/Claim成功按scope核对并撤销；UNKNOWN停止允许操作，不能误删永久记录。实现前核对隐藏和ontology的精确名单及退出注册点。

原生队列对资格撤销/已排入其它Claim如何处理需要最小prototype；Gameplay完成端必须再次拒绝所有过期/已专业化/非候选事件，即使UI仍暂存一行也不能重写Identity。若不能可靠阻止无资格项目继续供玩家建造/清除其它Claim，不以“收益端拒绝了”冒充完整UI验收；暂停具体路径报告。不得修改普通项目队列或清空整城生产来绕过。

### 保存事务与区域引用

完成事件只接受精确四项目ID，读取当前city/token/record，不信任UI选择缓存。对当前owner、正常参与资格、ACTIVE record stage（不是专业ACTIVE等级）、UNASSIGNED/NONE/P0、无pending错误及冻结候选逐项验证。重复完成、另一Claim晚到、已专业化读档重放必须无收益、无第二次revision写入。

现有validate明确以CLAIM_NOT_IMPLEMENTED拒绝LEGACY_CLAIM下SPECIALIZED，必须改为验证明确Claim完成依据（project type、selected kind、completion turn、当前record/reference关联等最小字段），而不是删除保护。acquisition.mode仍记录征服时分流，progression转SPECIALIZED；冻结LegacySet保留。结构扩展使用明确可区分的record version或等价严格判别，实施时选最小方案并记录旧包不能读取新Claim成果的回退边界；不构造全城迁移。既有B111未认定记录和已通过的FIRST_COMPLETION记录继续可读。

现有InvestmentAction/CrewProjects依赖base.first的districtID/type。Claim须从当前城市找到与所选冻结领域一致的完整区域，用已验证indexed Gameplay API形成技术锚点；完成时间记录为Claim时间，不伪称其为原Owner的首次建设历史。当前四专业没有社区式多同类区域。若正常Claim候选找不到可靠对应区域/替换类型，保留候选及记录并暂停，不擅自删除候选、选别的领域或补造districtID；若需改变玩家资格则报告DESIGN_DECISION_REQUIRED。不重置建筑完成/模板/Wonder等专业历史。

一次record-local提交同时写Identity/P1及Claim依据，readback成功才发布OnPermanentCityWrite触发正常事实与收益重算。access markers及UI是可重建派生物；不能先发收益再写账本。失败保留已有保存的故障处理，禁止fallback到City旧journal。投资由既有入口执行，Claim不赠送投资receipt。

### 证据与技术门禁

STATIC_CONFIRMED：PROG-006～009上述规则；当前Store的阻断点与base.first依赖；CrewProjects.sql已有RequiredBuilding项目资格模式；本机HD Gameplay/Projects.lua的CityProjectCompleted(playerID, cityID, projectID)监听提供Gameplay先例。

PROTOTYPE / USER_GAME_TEST_REQUIRED：本Mod四Claim项目在实际HD项目列表的资格过滤、完成事件、一次性退出、队列残留处理、项目完成后正常收益进入。原生先例不是本项目实机PASS。无须为Claim实现商业面板拦截或时代对话生产隔离。

### W0004验证与最小用户测试

L3（持久Identity写入），仅相关范围：

- 本地：单候选/多候选/空集/已有专业/外方owner/UNKNOWN；点击入队无写入，只有合法完成P1；后建区域不扩候选；重复与乱序完成幂等；错误ID/非候选/失败保存不认定；两城隔离、冷加载、既有投资与loss/return路径；Claim区域锚点和no-replay；标记零收益、ordinary排除、owner loss退出。
- 静态：Lua/XML/SQL、四项目映射与本地化、精确事件/退出调用点、manifest/context；无全历史stress。
- 原生最小一次流程：复用城市1已有商业单候选存档。确认只有商业Claim（后建工业不出现）、点击/入队尚未完成时仍NONE、实际完成后Commerce/P1及项目退出；城市2文化不变；城市1正常投资可用。另用一个征服时已含两个候选的fixture验证“选一后另一个退出/不能重选”（不能由单候选截图替代）。在认定后保存并完整重启一次，复查专业/潜力/投资及不再出现Claim。可用Cheat准备第二fixture，但标明操作路径；真实项目完成必须由原生事件触发。
- 任何重复认定/身份串城/保存异常/无资格项目仍可反复操作，停止，不推进F。没有实现前当前无需用户测试。

### 完成条件、回滚与范围

只有本地直接回归＋上述原生关键行为均通过，才关闭Claim切片；不等于E2所有生命周期完成。实现完成先commit/push，再遵守游戏退出/receipt/恢复点部署门禁；用户执行游戏，不由Codex启动。

回滚代码来自B111已知commit，运行包由部署receipt恢复；使用Claim前独立存档，不承诺旧B111能读取新Claim完成记录。保留现有证据与备份，不为本计划制作新源码副本。

不含：商业操作UI、时代对话、销毁/重建/位置复用、未专业化城市丢失再夺回、AI启用、多人、其它专业Legacy、F、新Design revision。当前用户需要审核Cost=1的真实项目方案并另行授权实施；其余技术门禁在授权实现时按最小prototype核验，不能先写成原生PASS。
