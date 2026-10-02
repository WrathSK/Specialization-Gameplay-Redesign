# P0-K — 巨作事实层实施计划

Document Owner: Codex
State: IMPLEMENTATION_COMPLETE_AWAITING_USER
Planning baseline: develop 9aaa831；源码/已记录运行包B146.173，部署source652c0fc。2026-10-01。
Authority: Spec D0036 Culture节 → Culture_D0029.contracts.work_pool；A0161/D0032事实层合同；Hybrid D展示方向D0032。Design未变；用户在计划审核后明确授权本批实施。

## 当前切片与停止点

用户已审核本计划并授权P0-K实施。B146机构显示可继续使用，但用户对视觉效果不完全满意；登记非阻塞优化，不把截图当成所有字体/缩放/ACTIVE刷新PASS。P0-K只交付一个可被后续文化能力和展示使用的权威巨作事实层、国内时代索引及简明按需诊断。没有新Culture收益、项目、永久成果或旧writer退出；本批已获明确授权；后续能力仍须另审计划/授权。

依赖是现有城市引用/owner读取、已验证的跨context传输与失效合同、当前人类玩家参与资格。无需先完成未落地的工业G–J、商业O–T或完整U1。P0-L/M/N/U2可使用本批结果，但不在本批实施。

## 已核对的实际链路

| 当前模块 | 已有职责 / 本批处理 |
|---|---|
| UI/DialogueRefresh.lua | 后台枚举人类玩家城市/槽位，DIALOGUE_SAMPLE携带作品和旧BASE相邻；单pending、seq/ACK和最多两次重发。ADAPT：复用producer/transport，增加独立事实分支；不可复制一套同功能扫描器 |
| DialogueModel.lua | 七类作品、非文物creator时代、文物自身Era；还计算旧25%×max(0,D−1)。KEEP旧收益模型；新的资格/时代事实不得调用旧百分比公式 |
| Dialogue.lua + Data/Dialogue.sql | Gameplay验证旧样本并按旧规则挂BUILDING_SPC_B059_D* / TEST25/50/100；仍在Gameplay.Start执行。KEEP，不改倍率、ACTIVE4门槛或module-owned失城退出 |
| GreatWorkAdjacency.lua/Model + Data/GreatWorkAdjacency.sql | 复用旧collection及AdjData，挂BUILDING_SPC_B060_{yield}_{P/N}{bit}。KEEP：本批不切换为意义延展，也不关闭旧writer |
| Gameplay.lua / UI/P0Panel.lua/xml | 样本请求入口与诊断；ADAPT只做精确路由及一个事实报告入口，不扩张其它按钮或能力 |
| UI/GreatWorkBasis.lua | 旧D0020最高基础值补差的只读报告，非当前work_pool权威。保留作历史参考，不接入新事实计算 |

计划基线的静态核对仅证明上述旧源码职责；本批实际实现与证据见下方B147 checkpoint。旧文化人口/专家百分比、Eureka及其它载体不在本批退出。真实切换按P0-L/M/N各自范围执行，不能为接事实层提前关效果。

## 事实合同与已支持目录

1. 独立、版本化的supported-work目录：明确支持的原版/DLC及有可靠来源的HD定义，记录type、category、历史Era和来源依据。不因GameInfo有记录或大类相同自动接纳未知Mod作品。实现时只读核对当前配置数据库/来源；无法可靠归属的条目排除并显示理由，不猜。
2. 合格类别：WRITING、MUSIC、SCULPTURE、PORTRAIT、LANDSCAPE、RELIGIOUS、ARTIFACT。排除RELIC、PRODUCT、Wonder、未知定义及不可靠时代元数据。
3. 当前规范使用作品所属历史时代，优先已支持GreatWorks.EraType；creator关联只在验证等价时作等价来源，文物用自身时代。历史D0022调查已经发现部分著作work/creator时代不同，旧creator-only resolver不能直接沿用。元数据冲突不静默择值；按当前来源合同排除不可靠条目并报告。禁止使用当前玩家时代、获得时代、名字或创作Turn猜时代。
4. 枚举所有当前本地受支持人类玩家城市中的实际馆藏，国内索引包括非Culture城市；本批不监听AI长期馆藏，也不开放AI专业化。文化身份/ACTIVE控制后续能力，不改写作品自身资格。
5. 一件实例只属于一个已确认城市/建筑/槽位：workID、workType、owner/current cityRef、building、slot、historicalEra。跨城重复ID、位置冲突、旧引用、格式错误不是两个有效作品。
6. 每城提供合格件数、各时代件数、不同历史时代数、集合版本/validity/availability；国内提供era→当前有作品的城市及件数。时代数明确使用eraCount/X，不与Shared基础设施D混用。
7. “本城无作品”只在完整成功读取后确认为0；UNKNOWN不等于空。缺失时代仅相对于有可靠目录依据的可收藏时代集合，不硬编码8/9、不保证未来时代可收藏；不能确认全集时只显示覆盖数及未确认说明。

建议责任落点为小型GreatWorkCatalog.lua与GreatWorkFacts.lua；可复用现有模块承载同等职责，不创建通用catalog引擎或Network公式。目录属于Gameplay/UI共用定义；UI拥有引擎槽位采集，Gameplay是验证和发布确认事实的唯一owner。UI只消费发布结果。

## 数据流、更新范围与生命周期

- UI现有采集→独立事实候选→Gameplay验证epoch、seq、当前owner/ref及完整范围→一次发布每城事实与国内索引→按需诊断；原旧样本/AdjData仍走原路径。新事实不会反馈旧writer，也不会产生收益。
- 尽量共享一次实际槽位读取，保留旧样本投影的语义/格式及transport边界。新事实校验失败不能伪装旧样本成功，反之独立资格差异不能无故清理旧收益；逐消费者验算隔离。
- 创建定位到目标城；移动/交易定位来源和目标；确认易主使旧owner索引撤销并拒绝旧包。城市引用核对沿现有E2可靠模型，不凭名字/单独坐标判断同城。事件签名未知时才使用一次当前受支持玩家范围核对；不是无条件世界扫描。
- 初始化/冷加载重建会话epoch与事实，不从旧carrier或存档收益推断馆藏。未知缺事件时保留一次本地玩家回合的有界对账，不能用“每城每回合最多一次”挡同回合真实移动。
- 相同逻辑输入不增加事实版本、不发布、不构造完整诊断。创建/移动合并dirty cities；需要全国来源提示变化时只更新国内索引依赖，不重算他城本地时代数。
- UI producer拥有有限pending/dirty集合，沿现有有界ACK/重试；Gameplay拥有当前accepted事实及最多一份候选。同引用读取暂失败保留最后确认值并标待复核；确认引用失效撤销。确认离开支持owner后清会话事实，不清永久记录。
- 目录初始化一次；槽位/建筑索引按实际变更失效。同批城市共用必要索引，不每城构建全玩家数据；普通计算不构造Tooltip或旧基础补差明细。
- 缓存按当前城市/作品/时代上界持有，不保存事件历史/每版本副本。关闭UI/重载卸载订阅并清pending；重试耗尽可诊断，不无限积压。

## 诊断与未来展示边界

复用P0面板一个入口“巨作事实”，默认只显示选中城：确认/待复核、合格N件、覆盖X时代、时代件数；有排除项时显示数量和关键原因。深层/分页再列作品名→类别→时代及国内其它来源城。真实0、国内没有、尚未确认明确区分；重复打开读缓存，不请求Gameplay重新扫描。

示例（仅格式示意，数值非测试结果）：合格3件｜覆盖2时代；古典2、文艺复兴1；排除1：未知作品定义。国内来源查询列城名和件数，不显示无关投资/收益/carrier信息。

不实现Great Works管理页的Hybrid D布局、机构润色、自动移动/主题化/买作品；但事实合同必须能直接支持后续U2，Gameplay与UI不可各写资格公式。

## 验证与退出条件

W0004 L3仅相关范围：跨context事实、owner/reference、事件顺序与加载风险；没有新永久schema。无需默认全历史回归或内存长测。

| 本地测试组 | 断言 |
|---|---|
| 目录/时代 | 七类、遗物/产品/未知；同大类未知type仍排除；work与creator不同、文物自身时代、缺失/坏Era；不猜当前时代 |
| 城市/国内聚合 | 同时代多件只增件数、跨时代数正确；非Culture城市参与国内来源；重复ID/冲突拒绝；可靠空城与UNKNOWN区分 |
| 生命周期 | 同回合多次真实移动、两城更新、创建/交易、支持owner失去/夺回、旧ref/epoch/seq拒绝、冷加载重采、重复通知幂等 |
| 业务隔离 | 同一原始馆藏和旧输入下旧Dialogue/GWA计划、carrier写入及退出完全相同；新事实不同/失败不调用新效果；投资/Store永久记录不变 |
| 工作量 | 静置generic pulse不增加采集/发送；重复逻辑值不发布；一次可定位移动只影响两城/国内来源依赖；pending/订阅有界且卸载退出 |

实施时新增一个定向test_p0_k.py验证真实Lua/transport，复用B059/B060相关fixture与B135后公共路径约束；旧runner有固定旧build和继承大套件，不原样执行全部、不改原断言凑PASS。目录/来源核对需要已配置只读DB；Lua模型可用独立小fixture。缺依赖准确报告。

最小实机只在实施完成后执行一次：准备有可移动合格作品的A/B两城（B可非文化）；打开诊断核对作品时代/件数，移动一件后看两城和国内来源同时更新；另存→完全退出→冷加载再读，确认事实重建。用现有Cheat方便准备，不要求完成四个文化能力、不重复收益/长局/失城完整测试。若事件未知导致不能正确更新，单图/日志报告后停止，不反复长测。

Exit：资格/时代/位置/国内索引与UNKNOWN/ref/load在本地通过；旧收益隔离通过；一次最小原生移动/冷加载验证。STATIC/LOCAL通过不替代USER_GAME_TEST。之后仅提出P0-L1（风雅熏陶）计划；不自动实施。

## 未决、回滚与文件范围

没有新的BLOCKING_DESIGN_DECISION。已知目录来源覆盖、事件参数及Artifact接口可靠性是本批定域技术核对；发现当前规范无法确定元数据时排除/报告，不改Design。后续0.1 GPP、native-only倍率、Dialogue cap、人文考察或机构布局优化不阻塞K。

预计涉及：新事实/目录Lua；既有DialogueRefresh.lua、Gameplay请求与Start、P0Panel Lua/XML、本地化、modinfo/版本；必要的旧样本兼容适配。Dialogue/GWA与其SQL仅核对/回归，不预先关闭或改变公式。无新收益carrier、永久Game/City Property或存档schema。若必须改旧收益算法/永久记录，停止该路径并报告。

回滚：B146.173已知源码commit652c0fc及既有整包恢复点，测试使用复制存档；本批仅会话事实和诊断，预期不写新保存schema，仍需检查无持久副作用后才能声称此范围。运行包替换遵守W0003退出/target/hash/staging/恢复合同；原计划轮不部署，本实施轮按持续测试部署授权执行。

依据：[总计划K行](D0032_Implementation_Plan.md#实施批次合同)、[Shared facts](D0032_Adaptation.md#shared-facts-and-services)、[输入版本](Batch_A_Input_Contract.md#1-版本模型与owner)、[传播/生命周期](Batch_D2_Runtime_Propagation.md#shared-work-and-publication)、[当前性能接入原则](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)、[Hybrid D](../../Historical/Design/Records/Culture_Era_Presentation_D0032.md)、[旧creator时代差异证据](../../Reports/Technical/Specialization_D0022_Dialogue_Percent.md)。旧报告不是当前作品规则。


## B147.174 — facts-only implementation checkpoint

用户明确授权后实施，A0161与D0036/Culture D0029语义不变。新`GreatWorkCatalog`与`GreatWorkFacts`均为会话事实；没有新Property、收益carrier、永久成果或AI/多人系统。旧Dialogue/GWA主模块、模型及SQL原字节保留。

### 目录与事实 authority

目录v1显式311 types：191原版Base/Babylon（含25文物）、120有明确来源的HD；当前配置只读DB的七类311/311对应来源。类别件数：著作93、音乐80、雕塑27、肖像28、风景40、宗教18、文物25；24遗物、966产品不准入。目录记录来源别名，不复制外部素材。来源：Base GreatWorks.xml、Babylon_GreatWorks.xml；HD DL_GreatWorks.sql、DL_GreatPeople.sql、HD_China.sql、HD_SEJONG.sql。它是已审阅定义目录，不承诺未来所有Mod作品兼容。

使用已审阅作品EraType；28处作品与creator时代差异均按作品自身时代处理。缺自身Era的原版非文物，仅在原始creator关联和时代均匹配时走验证等价fallback；文物不能猜creator时代。未知类型、不可靠类别/时代明确排除。当前已支持、实际存在定义的时代全集动态形成（此配置8种），不是硬编码8/9；目录有不可靠元数据时不能声称全集完整。纯原版191定义/原始creator元数据是本地模拟，不是原版实机PASS。

Gameplay `GreatWorkFacts.Start/Receive`唯一发布确认事实。`Read(player,city)`返回隔离副本；`Domestic(player,era?)`返回时代→当前城市件数/引用及整体availability。N与eraCount分开；每件含work ID/type、建筑/槽位、历史时代与来源。可靠空城为0；首读UNKNOWN无数值，曾确认的同ref暂失败只保留最后确认值并标待复核。国内索引包含非Culture城市；任一范围未确认时不把无来源写成确定没有。

### 接线、失效与更新范围

现有DialogueRefresh同一次实际槽位读取产生旧`Data`及独立`FactsData/FactsRefs`。旧格式/排序/EMPTY、Count及AdjData保留；两个Gameplay接收分支独立pcall。新facts失败/资格不同不替代旧writer成功，不反馈旧收益；旧creator-only时代和25%算法继续留到其授权cutover。

新包校验session epoch、processed seq ACK、馆藏inputRevision、当前回合、完整人类城市范围、NetworkInput.Reference、唯一实例/槽位与格式。ACK表示处理完成，不等于事实已接受。原生create/move及城市加入/移除使Gameplay事实定域待复核；移动前在途包拒绝。UI按dirty城市重读：创建一城，移动两城；未知签名一次本地范围回退。原生创建第2参数是creator，不是CityID；区域事件第3参数才是CityID。外国城市/区域事件仍保留旧本国BASE adjacency重采，不采外国馆藏。

总督/相邻环境变化复用槽位cache，只更新已有旧依赖。初始化/冷加载与每本地玩家回合一次有界馆藏对账，真实同回合变化不被限流。generic UI pulse只drain已有dirty/ACK；没有SetUpdate采集或hover请求。单pending，最多2次相同包重发；generation/epoch/input改变可在同回合替换旧包；卸载清订阅/pending/cache。目录/建筑ID索引初始化一次；没有事件历史/每版本副本。

confirmed E2 Exit只撤销已确认目标的会话馆藏与国内来源，不能用永久origin旧CityID清当前缓存；Return只使会话失效，回到正常采集后确认，不在Store恢复commit前施加能力。失城UNKNOWN不删除永久记录或普通建筑；GC策略不变。

### 证据与最小验收

`DevelopmentTests/test_p0_k.py`：26个定向真实Lua测试 LOCAL_SIMULATION_PASS（Lupa lua55），包含目录/时代、可靠0/UNKNOWN、完整范围与格式、引用/epoch/seq/input、重复与copy、移动/交易/加载、第二次失城ID变化、有限订阅/重试、同回合恢复、当前来源索引以及真实Dialogue/GWA计划+carrier map+写入次数三分支相等。1500 generic idle pulses零新增采集/发送；这是模拟计数，不是原生内存改善。新模块实际Property/carrier写入为0；现有permanent store fixture保持。

Lua语法、modinfo174全部文件/ImportFiles与XML、双语诊断key检查 STATIC_CONFIRMED。目录源码/DB解析核对及26模拟均不证明原生槽位/事件/冷加载行为。USER_GAME_TEST_REQUIRED；不重跑巨大历史wrapper，不作内存长测。

诊断复用“巨作事实”入口：左键本城摘要；右键作品组成/国内来源，重复右键翻页（每页最多6项）。只读已确认缓存，不启动重采。例：合格3件/2时代，古典2、文艺复兴1；排除1件（未知定义）。实际数字由馆藏决定，不由专业ACTIVE决定。

唯一最小用户流程：复制既有支持存档，准备A/B两城的合格可移动作品（B可非文化）；读取A/B摘要与右键来源 → 移动一件 → 重读两城和来源（件数改变，时代按作品metadata） → 另存、完全退出、冷加载后重读。无需征服或完整文化收益/长测；若停在UNKNOWN，回传一份报告/截图后停止。文物原生类型返回尚未单独验证，若 fixture已有文物可顺手读，不另要求准备整套文物。

停止点：本地事实层完成，等待该最小实机验收；通过后仅提出P0-L1风雅熏陶计划。机构视觉优化仍非阻塞待办。不自动进入L/M/N/U2。
