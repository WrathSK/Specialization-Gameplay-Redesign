# P0-K — 巨作事实层实施计划

Document Owner: Codex
State: PLANNED_NOT_AUTHORIZED
Planning baseline: develop 9aaa831；源码/已记录运行包B146.173，部署source652c0fc。2026-10-01。
Authority: Spec D0036 Culture节 → Culture_D0029.contracts.work_pool；A0161/D0032事实层合同；Hybrid D展示方向D0032。Design未变，本计划不授权实施。

## 当前切片与停止点

用户要求先整理P0-K计划。B146机构显示可继续使用，但用户对视觉效果不完全满意；登记非阻塞优化，不把截图当成所有字体/缩放/ACTIVE刷新PASS。P0-K只交付一个可被后续文化能力和展示使用的权威巨作事实层、国内时代索引及简明按需诊断。没有新Culture收益、项目、永久成果或旧writer退出；实现须另获明确授权。

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

静态核对证明上述源码职责，不证明P0-K已经实现。旧文化人口/专家百分比、Eureka及其它载体不在本批退出。真实切换按P0-L/M/N各自范围执行，不能为接事实层提前关效果。

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

回滚：B146.173已知源码commit652c0fc及既有整包恢复点，测试使用复制存档；本批仅会话事实和诊断，预期不写新保存schema，仍需检查无持久副作用后才能声称此范围。运行包替换遵守W0003退出/target/hash/staging/恢复合同，不在本轮部署。

依据：[总计划K行](D0032_Implementation_Plan.md#实施批次合同)、[Shared facts](D0032_Adaptation.md#shared-facts-and-services)、[输入版本](Batch_A_Input_Contract.md#1-版本模型与owner)、[传播/生命周期](Batch_D2_Runtime_Propagation.md#shared-work-and-publication)、[当前性能接入原则](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)、[Hybrid D](../../Historical/Design/Records/Culture_Era_Presentation_D0032.md)、[旧creator时代差异证据](../../Reports/Technical/Specialization_D0022_Dialogue_Percent.md)。旧报告不是当前作品规则。
