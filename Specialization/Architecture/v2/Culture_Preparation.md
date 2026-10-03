# 文化后续模块：计划与调查入口

State: L1_NATIVE_SCOPED_PASS / L2A_LOCAL_COMPLETE_NATIVE_REQUIRED。L2B/L3/M/N/U2仍IMPLEMENTATION_NOT_AUTHORIZED。
Preparation baseline: 原只读准备`9d75ff8`保留；本次定域计划核对`f02e4e8`。实际source/live只查Status，未重新核验外部运行包。
Authority: Spec D0037 / Culture D0029 / Shared D0035 / Presentation D0032 / Architecture A0161。

## 当前切片与停止点

用户授权逐步准备文化模块计划和只读调查。[L1最新结算验收](../../Status/Validation/Results/Specialization_B149_P0L1_Settlement_Pass.md)已关闭本批门禁；用户随后授权[L2A单城接口验证](P0_L2_Meaning.md#当前切片与停止点)，B150已LOCAL完成；仅单城可逆Science/Gold probe待原生，不等于完整L2。L2B及其它模块仍待各自审核/授权；实际部署只查Status/receipt，不继续L1时序调查/旧长测。

此入口保存准备结果，不成为第二份Design或状态台账。实际授权、部署与证据等级仍查[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)。除本次已授权L2A外，其它计划未获实施授权，也不加入所有任务的必读集合；对应切片获批时再建立/收敛其现有W0001 manifest。

## 按模块阅读

| 模块 | 准备资料 | 可复用基础 | 实施前仍需关闭的门禁 |
|---|---|---|---|
| 风雅熏陶L1 | [当前完成范围](P0_L1_Aesthetic.md#当前切片与停止点) | 已实现逐栋计划、区域旅游投影、精确旧16项退出 | 已测加值/累计及用户报告的变化后结算/冷加载PASS；未测组合不扩大 |
| 意义延展L2 | [逐巨作附加产出计划](P0_L2_Meaning.md) | Shared绝对D、产出份额、K作品目录；旧GW加值路径 | 0.5精度、已支持作品限定、未来Dialogue不放大追加值；旧BASE writer精确退出 |
| 巨作启迪L3 | [基础伟人点数计划](P0_L3_Inspiration.md) | Shared D、K件数、既有基础GPP与正常倍率模式 | 0.1基础点数的原生结算；同一时代作品件数变化通知 |
| 时代对话M | [项目、次数与累计倍率计划](P0_M_Dialogue.md) | 已验一回合项目、Claim的持久计时和E2城市保存 | 新城市账本、START时代/完成时X、native-only隔离；cap仍待平衡，执行中边界另列 |
| 人文考察N1/N2/N3 | [交互→记录→网络计划](P0_N_Expedition.md) | E2引用、Shared资格、国内路线桥；已有Spy字段静态参照 | 非敌对远程交互/战争、外国目标事实、source绑定、整城旅游接口与K_T；最后才退出旧Eureka |
| Hybrid D U2 | [馆藏界面计划](P0_U2_Culture_Era.md) | K本城馆藏/国内索引，已批准紧凑摘要+Tooltip | 原版/HD hook、缓存失效、布局/缩放；独立于机构排版优化 |

L1本批门禁已关闭，L2A已实施、单城原生精度/归属仍待验；通过后才更新/授权L2B正式cutover。L3、M、N、U2可以继续准备，但不能因已有计划就连续实施。若L2某接口失败，只暂停依赖该接口的路径；不自动实施别的批次，也不将所有文化模块判为阻塞。

## 共同输入及真实缺口

- **D**＝Shared绝对区域基础设施深度，不是完成百分比；只用已批准Tier与最高单区域。**X**＝本城合格馆藏时代种类数；**W**＝合格件数。**文化见闻**及**完整考察文明集合**又是独立永久记录，不能互代。
- B148的`GreatWorkFacts.Summary`可提供X/件数及确认状态；当时`OnConfirmed`比较的是reference、X、availability、hasConfirmed；该旧缺口已在B150 L2A补上**合格件数/同类排除与类别未知**比较。时代内件数变动现在可通知；L3/U2仍按真实consumer检查是否需要更细组成摘要，不复制槽位采集，也不让L1因为新字段就重复写收益。
- 当前K collector在UI读取本地人类玩家城市，Gameplay重验完整本地城市集合。因此外国艺文采撷目标不能直接冒充现有国内样本。N1/N2需要按部署/当前任务限定目标的只读候选事实及Gameplay复核，不长期监听全部AI城市。
- `DistrictCompleteness.Read`已有确认快照；普通计算复用所需D/资格，不为小型判断默认构造诊断明细。无法确认的D/馆藏/城市引用是UNKNOWN，不当0、不补Tier、不从名字猜身份。
- `CityProgressionStore`已保存E2城市、投资、工业模板及科研传统，**尚未保存新Dialogue/文化见闻/考察任务**。它提供的可靠城市映射和定域退出/恢复可以复用，业务字段及验证仍须分别增加；不复制Claim账本或建立通用事务框架。

## 本轮只读调查的证据边界

| 观察 | 证据与范围 | 不可推导的结论 |
|---|---|---|
| 旧GW writer挂逐类GreatWork `YieldChange`；旧Dialogue挂Culture/Tourism `ScalingFactor` | 当前Lua/SQL与旧B055/B059/B060报告，STATIC_CONFIRMED；B055整数文化与撤销、B059特定非主题/主题化读数有各自实机证据 | 新L2小数、未知Mod作品排除、所有产出和native-only隔离均已通过 |
| 本机配置的DebugGameplay缓存有city/district GPP `Amount`接口；`Building_GreatPersonPoints.PointsPerTurn`声明INTEGER | 本轮只读SQLite查询，STATIC_CONFIRMED；两个相关Effect的已存Modifier中未找到小数Amount先例 | 引擎一定不支持0.1；整数schema也不能单独证明所有路径不支持 |
| 同缓存有GreatWork Culture/Tourism倍率；未找到仅ScalingFactor参数的single/player-city Tourism例 | STATIC_CONFIRMED限定查询；多数实例另有作品/奇观/改良等过滤 | 无过滤参数就一定能覆盖整城所有旅游；也不能据此判定原生不可实现 |
| Spy当前缓存Cost=60、CanTrain=1、Spy=1、PurchaseYield=Gold | STATIC_CONFIRMED缓存定义；不是本轮重新生成的B148数据库，也不是本Mod考察团配置 | 可直接继承Spy购买、容量、失败/战争行为；只允许取当前Spy生产成本参考 |
| 一回合真实项目已过队列/旗帜/面板、普通回合与所测chop场景；后续Claim补持久续接 | [B123限定证据](../../Status/Validation/Results/Specialization_B123_Project_Pass.md)、[Claim核心证据](../../Status/Validation/Results/Specialization_B126_Claim_Core_Pass.md)及当前Claim源码 | 新Dialogue配额/累计倍率已经实现，全部注入/跨时代/易主路径原生通过 |

数据库是本机已有的只读配置缓存，未重建游戏数据库；静态查询不等于本轮实机。旧报告保持原字节/设计版本；只复用接口证据，不采用旧玩法公式。原只读准备轮未运行玩法模拟、原型或游戏；其后L1及L2A的实际实施/验证由当前切片链接记录，其它新consumer仍待实施。

## B148及后续结果如何影响计划

| 发现 | 必须复审 | 可以保留 |
|---|---|---|
| L1 district Tourism加值/Plot条件失效 | L1投影及所有明确复用该原语的候选 | L2 GreatWork加值、L3基础GPP、M计时和N任务模型；N2整体旅游是另一接口，不能跟着判PASS/FAIL |
| Shared ordinary/D目录或引用被修复 | 涉及D的L2/L3、实际引用/退出consumer；L1 recipient | 与该目录无关的START时代quota、任务唯一性；不自动重新审全部Design |
| K作品资格/时代/移动读取出现问题 | L1/L2/L3/M/U2，N的Works目标若用同目录也复审 | 可靠E2城市/投资账本、独立任务类别规则；只作影响范围分析 |
| L2精度或附加收益隔离失败 | L2效果路径、M native-only倍率候选及两者组合测试 | L3独立GPP接口、U2只读展示；不得自动floor或换城市补贴 |
| M城市保存/项目续接失败 | M及真正复用相同新字段/计时的N任务 | 只读K/U2、无新增永久数据的被动consumer |

每次新结果进入对应计划/Status，保留旧失败证据；不将B148通过扩写为其它原语通过。各实施批次变更前检查最新HEAD/dirty diff/Authority和直接依赖，未变化规则与证据按W0001复用。

## 范围、性能与后续授权

当前v0.1仍只有科研、文化、商业、工业；领域引用不授权实施未来专业。AI/自由城市休眠、单人范围、E2身份安全及已接受GC策略不变。

各计划按[公共更新与临时状态合同](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)列原因、范围、必要事实、owner/失效/退出；不添加每帧/hover扫描、每城每回合一次限制或独立GC。验证沿W0004定向选择，不默认旧长测/full stress。

目前用户需要决定：无。未来M的cap、N2的K_T在正式收益实施前需按Balance流程确定；技术失败需要改玩法时才提出具体DESIGN_DECISION_REQUIRED。用户需要测试：已授权L2A包就绪后的一个最小流程见其结果；其它模块仍只准备，不自动实施。

正式规则见[Culture Content](../../Design/Content/Culture_D0029.json)、[Spec Culture节](../../Design/Specialization_v0.1_Design_Spec.md#6-culture--theater-square--cul)、[Shared](../../Design/Content/Shared_D0035.json)；人类设计阅读见[文化](../../Design/Culture.md)。切换责任见[总实施合同](D0032_Implementation_Plan.md#明确的旧效果切换责任)。
