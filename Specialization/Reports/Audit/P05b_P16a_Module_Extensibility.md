# P05b / P16a — 模块依赖与新增专业接入成本

Audit IA20261007 / W06；2026-10-07。审查baseline `64adae9b53bf284edb2dae1aa210ed9d5d94e929`。**Audit-only；不是正式Architecture合同、Design决定或修复授权。** 本slice核接入边界，不是全Mod可达性或全部未来专业实现审计。

## 回答的问题与结论

如果以后加入第五、第六专业，哪些现有公共接口可以复用，哪些中央分支会迫使新模块重复处理？本轮沿实际Identity、Claim、保存、Network、composition与机构展示路径核对，复用[P06a](P06a_State_Ownership.md)、[P09b](P09b_Propagation_Boundaries.md)、[P08a](P08a_Effect_Ownership.md)，没有重新逐能力验证冷加载。

**最值得在新增专业前收窄的，是分散的Identity词汇校验、mutation后的consumer通知名单，以及保存核心中的专业业务依赖。** 它们会随着专业和永久资产增加而扩大修改面。当前四专业名单符合v0.1范围；没有发现本轮所核名单之间已经存在当前四专业不一致，也不把未来专业未开放报成现行玩法故障。

本轮补强既有 `IA-P06a-F03`、`IA-P13a-Q02`、`IA-P13a-F03`，均维持 **MEDIUM / FIX_BEFORE_NEXT_PROFESSION**；不按多处同类名单新增一组重复finding。P06a-F01每写全记录唯一性检查仍是既有 **FIX_NOW**，本轮没有改变它的证据或实施任何修复。普通include、数据库注册和明确的Start顺序本身不是缺陷；不建议建立自动发现模块、通用事件总线或统一资产状态机。

## 新专业的最小接入面

下表假设新专业沿用现有“合法首个区域／候选Claim、Potential 1–4、开拓者投资、当前ACTIVE”合同。**只是用于测量架构成本，不是为未来专业确定这些玩法。** 独有机制另需自身合同，不能由下表自动推导。

源码路径默认相对于仓库根；行号以本baseline为准。前两行是已证实的**5个Identity文件＋3个Claim文件下限**，不是整个新专业全部文件数量或工时估计。

| 接入职责 | 必改／条件性修改及实际位置 | 可复用部分与边界 |
|---|---|---|
| 识别、接受和读取新Identity | `Mod/Probe.lua:5–6`的district→kind；`CityProgressionStore.lua:24,52–110,938–948`；`CityIdentityRead.lua:62–79`；`EffectiveFacts.lua:5,24`；`NetworkInput.lua:43–48` | 五处不是同一份定义。Store的`family`另有四专业过滤，单扩`P.Families`仍被拒绝；Network即使只作接收方，也先校验每城Identity |
| 复用已有Claim方式 | `ClaimProjects.lua:9–10,100–147`、`UI/ClaimProjectUI.lua:4–10`、`Data/ClaimProjects.sql:2–13`各有具体专业／项目集合 | timer、receipt、candidate不可变语义和one-turn路径可沿用；还需本专业合法文本及必要marker展示。不能只新增SQL就声称Claim已接通 |
| 普通事实与投资 | `CurrentSpecializationFacts.lua:3–7`、`InvestmentAction.lua:16–59,88–133`无自己的四专业名单；Binding/Flow已有Store读取adapter | 在上游Identity被合法接受且投资语义不变的前提下，无证据要求为每专业复制投资事务、CityKey或事实读取层 |
| Lv2住房／GPP等共同效果 | `Lv2Housing.lua:8`、`Lv2GPP.lua:8–10`有kind/domain/GPP class映射及对应SQL | 是否共用效果由正式Design决定。`SpecialistSupport.lua:22–44`可复用anchor/资格读取；住房按自身建筑tier口径，不能替换为Shared D公式 |
| D与普通建筑域 | `OrdinaryBuildingCatalog.lua:189–220`已列10个域；`DistrictCompleteness.lua:17–48`不是四Identity名单 | “可提供基础设施事实”不等于“可成为专业身份”。新增专业不当然需要新增D域，也不能由D catalog自动开放Identity |
| 新专业永久资产 | 当前Research、Industry直接进入Store的validation、投资、恢复和tick路径，见下文 | 如只有新Identity，未发现必须改变现有record schema的依据；如有新资产，仍需各自状态schema、初始化／损坏／ownership合同。不能宣称未来存档迁移成本为零 |
| transient退出／返回 | Store `RegisterExit/Return:838–844`，当前和以后创建的record worker均接入 | 新writer声明自己的exact effect集合和withdrawal；复用已存在出口，不复制全城删除器。Return是提交前失效通知，不能误当已恢复收益的post-commit事件 |
| Network角色与收益 | 新Identity至少需前述Input校验；source/center/national/consumer则按下表分别接入 | 普通接收城市、新source和新中心并不是同一要求；不为每专业默认增加所有Network角色 |
| composition与更新传播 | modinfo对应action/File，Gameplay include/Start、新操作窄路由；mutation后的名单另见下文 | 引擎注册与显式组合是必要工程工作。真正扩展债务是调用方反复保存consumer业务依赖，不是每个新模块多一行Start |
| 玩家展示 | `CityPotential.lua:6`、Store `:381–384`显示映射；具体Claim文本；机构model与两处UI刷新signature | 当前机构model仅Research，UI行循环已经支持同阶段siblings。多专业展示需按Identity选model及使cache key包含对应model/Identity；不需要先重写行布局 |

### 为什么旧命名的validator不能当作可删除兼容层

Store `:105–110`把当前record构造为JOURNAL/FLOW形状交给 `CityIdentityRead.Preview` 验证；这是**当前生产写入**的结构保护，不只是旧导入入口。后者仍有四专业、基础P1和最多三份投资receipt约束。未来只改Store表、不改Preview或EffectiveFacts会留下真实拒绝点。

BindingProbe `:53–68`、CityFlowProbe `:126–135`已有新authority读取adapter和旧writer退出保护。复用它们不等于新增一套历史兼容实现；要退役这些入口需要另证调用闭包，本轮没有这样的结论。

## Typed dependency map：先区分边的职责

| 调用链／类型 | 当前依据 | 架构判断 |
|---|---|---|
| Gameplay先Start Store，再Start Binding/Journal/Flow与EffectiveFacts；初始化顺序 | `Gameplay.lua:655–683` | Store先取得持久authority；显式顺序有安全作用，不能用任意加载顺序替代 |
| consumer → EffectiveFacts → CityFlowProbe.SupportFacts → Store.Base；运行时读取 | `EffectiveFacts.lua:15–24`、`CityFlowProbe.lua:126–135`；EffectiveFacts另读Store.Investment | 读取沿adapter回到保存权威；不是Store主动把整份事实推送给所有consumer。必须与上一行启动顺序分开 |
| Store → ResearchTradition；纯模型、原子初始化和周期mutation | Store `:1,95,166–186,249–261,813–830` | 保存核心还知道科研业务和调度；继续复制会随永久资产增多扩大核心修改面。保留首次P4原子起点，不把验证随意挪到保存后 |
| Standardization → Store.Read/WriteTemplates；Store → Standardization.ValidateRetained；不同方向的调用 | `Standardization.lua:17–40`、Store `:572–579` | 双向文件依赖确实存在，但ValidateRetained仅验证ledger/catalog，不回写Store，**不能仅画出环就断言无限递归**。可考虑纯模板validator边界，保留历史损坏保护 |
| Store → RegisterReturn callbacks → commit；有序lifecycle | Store `:581–584`、`:838–844` | 回调先使sample/quote失效，提交后再由正常事件重算。此边不是“立刻重新发效果”；复用P06a-Q02/P09b证据 |
| NetworkBridge → publish view → notify consumers；先发布后通知 | `NetworkBridge.lua:56–82` | 逐consumer有pcall隔离；现有5个consumer名单是显式接入点。继承P09b异常隔离证据，不重做相同复现 |
| consumer → Current* query；只读已发布view | Bridge `:295–307`；Lv3Effects `:33`、NetworkBoost `:49`、CopyYields `:41` | 查询不重新Capture/derive，不能因双向调用称每个consumer都会递归全scan |
| StandardizationDiscount → DiscountBatch → Refresh → publish；可刷新查询 | Bridge `:275–293`、Discount `:124–132` | 与Current*不同；已有busy/验证边界。具体重入见先前审计，不能把全部API统一当缓存读取 |
| Store.Describe → Network；诊断 | Store `:400–424` | 不属于永久状态计算依赖，不能计成每次record保存必跑Network |
| Probe → native facade；共享服务 | `Probe.lua:99–117,130–145,314–341,547–554` | Field/Call/Rows/Info、Family、GovernorGate、mutation wrapper用于普通运行；本轮未发现Probe反向调用Research/Culture writer |

`Probe`还包含目录、支持玩家、施工力换算和诊断。命名／“probe only”注释不能代表它只在实验时运行，但同一文件里有诊断也**不证明完整诊断进入普通hot path**。职责清晰化可作为小范围后续工作，不能凭行数称god module或要求立刻拆文件。

启动顺序还有已知合同：D失效监听先于其consumer；GreatWorkFacts→Aesthetic→Dialogue→retired GWA→Meaning的包装顺序；正常Meaning与旧probe互斥。P09b已经记录GW通知链的实际脆弱性；本轮不通过“自动排序”建议抹去这些依赖。

## 传播接入：真正会随能力数量扩大的名单

补强 **IA-P13a-F03，MEDIUM / FIX_BEFORE_NEXT_PROFESSION**。已经Start并注册native事件，不足以证明新consumer能收到一次投资提交后的最终Potential／receipt变化。

| 现有中央入口 | 它实际知道什么 | 新consumer的遗漏／过宽更新风险 |
|---|---|---|
| `Gameplay.lua:426–442` UnitActions返回后 | 手列Network、各类收益writer、Dialogue等 | 多专业复制后，新增／退休consumer需逐入口核；某些调用带player，某些无scope |
| `Gameplay.lua:453–468` LV2_GPP_DIRTY | 名称虽是GPP，实际承担facts、worker、科研、文化和Network传播；有WorkerOnly/FactsChanged筛选 | 该筛选是已确认输入差异，不能为了统一名单把所有consumer变成全player重算 |
| `Gameplay.lua:507–518` InvestmentAction返回后 | 又一份收益名单；PREPARE、CONFIRM及拒绝分支之后也进入刷新 | 部分是保守兜底；本轮未量测实际频率，不能直接将所有刷新判为冗余或native热点 |
| `ClaimProjects.lua:80–87` Claim后派生更新 | 九个精确consumer＋Network | Claim首次P1，不必叫醒所有Lv3/Lv4能力；新模块只加入实际依赖，不把较短名单误判漏掉全部高级能力 |
| `NetworkBridge.lua:56–64` publication | 五个当前consumer | 新网络效果需接出版通知及自己的额外输入事件；Bridge输入不变不意味着所有独有收益输入不变 |

建议候选：**让模块明确它消费哪一种已确认变化，共同入口传递原因和player/city范围。** 先在现有三条Gameplay mutation/dirty入口核对依赖闭包，不要求迁移所有native listeners或建立通用总线。ordered ownership/receipt transition仍交原owner顺序处理，不作为可以随意合并的普通收益重算。

现在主要是这几条producer链＋相关consumer；以后若增加多种投资、长期任务和专业，会同时改每个producer与中央名单，容易漏接或误复制worker过滤。改善目标应是可靠的提交后事实传播、减少重复读取；**不是按“每城每回合一次”限流**。本slice只有静态接入证据，没有新event次数、分配量或native性能结论。

## Network不是一个统一专业名单

补强 **IA-P13a-Q02** 的已确认接入表；保留其既有ID和timing，不把各角色语义差异本身当重复实现。

| 角色 | 现行位置与规则 | 第五专业需要什么 |
|---|---|---|
| accepted city input | `NetworkInput.lua:43–48`接受NONE/四专业；失败进入Bridge重验证状态 `:173` | 即使仅本地能力也需让新Identity能通过捕获；否则可能使本player input不可更新。是未来遗漏风险，不是目前发生的故障 |
| source | Bridge `:245–246`为R/C/I、Potential≥1；后续consumer有自己的ACTIVE资格 | 只按接受Design增加，不从“是专业”自动推导source |
| center | Bridge `:247–249`Commerce与首都 | 新专业不自动成为转发中心；首都特殊规则继续独立 |
| receiver | Bridge `:258–269`来自连接关系 | 接收方本身不需要source专业；不要强迫每专业定义新receiver类别 |
| national aggregate | Bridge `:31–42`只计算R/C且公式不同 | 仅有新全国聚合合同才扩；不把全部专业按一种聚合公式处理 |
| signature | `NetworkInput.lua:12–16`已含Identity/Potential/ACTIVE/ref/first | 单加新kind无需新增signature字段。新独有事实应声明输入，不把全部yield/diagnostic塞入公共拓扑signature |
| writer通知／实验隔离 | Bridge `:59`；`NetworkIsolation.lua:5–8,60–71` | 新网络writer应接正常通知、独有输入、退出及仍保留的定域隔离名单；本地能力不必加入Network隔离 |

CommerceConvergence从已接受route input计算自身incoming/max规则（`:23–55`），不能替换成通用recipient列表。Input读取 `SPCBoostConfig.k`（`:24`），配置经NetworkBoost include加载；正常启动在捕获前、fallback与当前值一致。此为隐含配置依赖，未发现现行错误，不据此另建registry。

`NetworkInput.Reference`是中性reference编码，其他文化/巨作模块使用它不等于“商业专业拥有公共身份”；TradeRouteProbe的RouteSignalRevision是变化信号，不是永久路线权威。不能按文件名自动判依赖方向错误。

## 保存层与展示层的候选边界

**保存核心／IA-P06a-F03：** 可候选提取专业纯验证／转换模型，保存层继续控制当前record、compare/revision、原子提交和有序owner转换。Research首次P4起点、Industry可靠空账本与损坏缺失的区别必须保留；工业首次Identity与UNINITIALIZED凭据、模板账本与INITIALIZED确认分别保持同一次record提交（Store `:278–286,308–317,334–347`）；不提供任意WriteRawRecord逃过保护。专业自己的周期业务不宜随着每项资产新增而继续塞入Store，但怎样拆调度须另行设计与验证。本轮不统一城市历史、文明历史完成信用、Identity、合同、in-flight或单位来源资产的归属；Shared D0045 lifecycle分类仍是约束。

**机构显示／低优先级接入提醒：** `InstitutionPresentation.lua:4–12`的数据和Matches仅Research；`UI/Institutions.lua:40–57`按Rows及entry.level循环，已经允许同level两行。两处signature（Institutions `:34`、InstitutionOverview `:28–30`）不含Identity。当前仅科研不会据此证明bug；以后若让同城在相同P/ACTIVE下换专业model，必须同步key/刷新。行布局 **NO_ACTION**；多专业model及key在实际展示扩展时处理，**LOW / DEFER**。这不是提前实施Harbor双机构。

## 未来修复时的验证边界

这是修复建议，不是本轮测试任务，也不恢复B168实机门禁。

- 用独立fixture检验一个假想新Identity经过first completion、保存校验、EffectiveFacts与Network input；不得靠正式Design添加假专业。现有四专业与NONE、未知kind拒绝同时保留。
- 如果将身份目录共享化，定向验证Claim gameplay/UI/SQL枚举的一致性。Identity集合、D域、Network角色、GPP类别分别有职责，不能一个表自动授权所有角色。
- 已提交投资／Claim真实变化能到达依赖consumer；无变化与worker-only差异不扩大传播；UNKNOWN、确认失城、跨城／全国依赖和ordered transition不丢弃。
- 模块失败隔离、注册到以后创建的record worker、提交前return与提交后recompute保留。新资产需自身初始化／缺失／损坏测试，不为每个收益复测全部成熟生命周期。
- Network新kind不是source时仍可正常读；source/center/national只按已批准role启用；独有输入变化不能只等待topology publication。

现有测试只作静态参考：`test_arch_v2_batch_a.py:68–188`覆盖输入／发布／Current查询等；`test_arch_v2_batch_b.py:95–120`覆盖副本/k/signature；`test_b136_facts.py:353–370`用真实Effective gate；`test_b137_network_isolation.py:227–271`覆盖当前五writer隔离。它们**不证明第五专业接入**。本轮没有运行这些套件、修改断言或伪造新专业实例。

## 实际读取与本轮验证

三路定域只读审阅分别为Identity/Claim/持久接口、Network角色、Gameplay composition/Probe facade；主任务独立核对上述关键拒绝点、三条fan-out、Return次序和UI行循环。子审阅没有写项目或运行正式测试。完整Authority/Status历史不在本slice重新读取。

| 文件组 | 实际范围／用途 |
|---|---|
| root/project AGENTS、项目README、Workflow README | 当前指引、恢复/Git/audit-only边界；沿既有入口读，不修改治理 |
| Authority、P0-L3A、Status CURRENT | 当前metadata/状态/直接选择范围；context检查读hash不等于模型逐文件通读 |
| Gameplay、modinfo | include/Start及直接操作路由；Gameplay `:18–70,179–280,388–528,611–617,635–824`；modinfo action/import/file注册元数据，非全Mod源码 |
| Probe、CurrentSpecializationFacts、EffectiveFacts | Probe facade/Family/Governor/mutation与实际caller定向检索；后二者全文 |
| Store、CityIdentityRead | Store `:1–118,150–189,245–365,381–424,550–610,637–652,692–715,742–763,800–850,935–1043`及注册callee；CityIdentityRead全文；复用P06a已读其它边界 |
| ClaimProjects、UI Claim、Claim SQL、InvestmentAction、Binding/Flow | Claim状态/项目表/Sync/consumer flush；UI/SQL识别；InvestmentAction `:1–164`；Binding/Flow adapter直接段，不重审所有旧实验 |
| Standardization、Tradition、Catalog、D | Standardization `:1–49,137–179`；Tradition模型入口/Effects直接接口；Catalog `:187–270`；D领域/返回结构。既有D cache复现不重跑 |
| NetworkInput/Bridge/Sender/Isolation/RuntimeWork | 全文（定域审阅）；root重读Input身份校验、Bridge发布/derive/Current与Isolation名单 |
| Network consumers及信号 | Boost/Discount/Copy/Lv3Effects/Convergence的正常查询、额外输入、exit接口；TradeRouteProbe及BackgroundRoutes直接signal；BoostConfig header/使用点，未通读生成数据 |
| Lv2Housing/GPP、SpecialistSupport、Institution model/UI、CityPotential | 前二者资格/映射入口；Support/model/两机构UI全文；Potential显示映射与读取段 |
| 直接合同与测试 | Architecture系统说明/公共更新约束，Adaptation当前事实段，E2恢复与F传统起点；Shared_D0045 lifecycle/Network直接对象；上列测试具体断言及Meaning owner/Inspire路由/composition相关片段。未审所有规则/全部测试 |

本slice为静态依赖问题，没有创建虚构第五专业运行实例、没有必要新增reproduction脚本。前序W02–W05的原始证据和finding保持不变。文档链接/路径、diff与当前context完整性检查用于本次产物可靠性；**不产生新的LOCAL_SIMULATION_PASS或USER_GAME_TEST_PASS**。没有读取新的外部运行包、部署、修改GC或请求用户测试。 本轮report＋ledger共21条本地链接/锚点检查无错误；`context.py check P0-L3A`为PASS（186个runtime文件、469个guarded context文件，implementation_authorized=false）；旧confirmed/provisional/rejected正文与起始HEAD逐段相同。

## 未覆盖与下一准确入口

本slice只完成新增专业的中央接入问题。全Mod/SQL实际可达闭包、所有启动异常、全部永久资产、native事件时序、真实20–40城负载及间接保留仍 **NOT_YET_AUDITED**，不把本报告写成完整P05/P16 PASS。

下一 **P12a — 规模风险的现有断言与fixture真实性**：

1. 从本ledger及W02 Dcache、W03 Store复杂度、W04传播、W05writer反例恢复；不重跑这些已经留存的复现。
2. 先读 `DevelopmentTests/README.md`、`Test_Catalog.json`的相关条目；再定向读 `test_b138_update_contract.py`、`test_b136_facts.py`、`test_b136_progression.py`、`test_b132_event_cache.py`、`test_b133_redundant_reads.py` 与实际引用fixture；Network仅按需复用batch A/B和B137入口。
3. 问题是：现有1/2/4/8城断言是否覆盖真实consumer工作集、失效边界、逐record写入与传播范围；哪些20–40城代表负载仍缺证？先审断言/fixture，不默认跑全部或搭建stress平台。
4. 若已有断言足够，记录反证；若只剩一个影响结构结论的具体缺口，再做最小audit fixture并区分真实Lua、stub与native。之后才进入既定P13b间接保留/GC职责。

用户需要决定：本slice无。用户需要测试：无，B168继续原待办。Codex下一步：在本逻辑边界保存checkpoint；下轮从P12a续接，不实施建议。
