# 人文考察团 UI 计划

State: N1_PARTIAL / B182_SPY0_DISPATCH_BLOCKED_REVIEW. N2/N3 and era UI remain ON_HOLD. [Current boundary](P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) governs; full management UI below remains a proposal.
Current entry: **专业化诊断 → 人文考察·验证**. This is the temporary Spy0 fixture with readable target navigation, not the formal management system. The [movement/coexistence plan](../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md) records the user's mission-only movement and exact map-location requirements. No new route is implemented here.
Date: 2026-10-06。Authority: Culture D0048 `CUL_L4_EXPEDITION`、missions、expedition／observations／network_effect及Shared D0045；原Gameplay不改。B165补测资料已审阅，正旧AUTO所测共存通过，精确结算归因仍开放；本计划不解除门禁、不部署、不产生native UI PASS。

## 推荐入口与整体结构

采用一个独立“人文考察”管理窗口，避免替换原版间谍总览。名称与以下布局是UI提案，不成为新增能力名或冻结玩法。

- **常规入口**：独立HUD／LaunchBar按钮打开全国管理；选中考察团的单位操作区提供“管理考察团”；城市文化机构／见闻摘要可直接打开该城档案。常规操作不依赖P0面板。
- **三个页面**：考察团、文化见闻、文化网络。派遣／任务是考察团页里的双栏选择流程；重新挂靠是绑定失效时的城市选择弹窗，不另占永久页签。N3尚未实现时，不把空网络页包装成已有功能，最终入口随真实consumer接入。
- **首屏**：全国现存数量／上限、当前团状态、当前归档城、位置／目标、部署或任务剩余回合、下一可执行操作。单位行按数据生成，当前cap1不硬编码为永远只能一个控件。
- **视觉**：沿用Civ VI字体、行高、滚动、选中与禁用风格，三类任务以中文短名＋状态标识显示。初版不新增美术资源；reference／receipt等仅高级诊断展开，不进入正常操作主文案。

## 1. 训练入口

在正常城市Production单位列表提供考察团条目：Culture ACTIVE IV、当前间谍Production成本、当前全国0/1或1/1，以及不可训练的具体理由。所有存活团都计数，包括来源降级、转出、重组和等待重挂靠；不能删除现存团腾槽。

只规划已接受的训练渠道，不增加Gold／Faith购买。排队／完成并发cap检查属于后端；训练中资格丢失后的退款／取消若需要额外玩法规则，单独提出，不从“已完成团保留”推导。

## 2. 考察团页与单位操作

每行显示当前状态、原训练来源与当前归档城（两者分开）、部署位置／目标、任务类别、剩余回合和下一动作。点击行打开详情，也能从单位入口定位该行。

| 当前状态 | 面向玩家的摘要 | 操作范围 |
|---|---|---|
| 待命／部署完成 | 已有有效归档，可选择外国目标或当前可做任务 | 打开目标选择／任务预览 |
| 部署中 | 目的地及部署剩余回合 | 查看；不凭UI新增改道或自动任务 |
| 考察中 | 类别、目标、任务剩余回合；预计成果与已获得分开 | 查看进度，不自行增加手动中止 |
| 待事实确认 | 当前信息尚待核验，暂不发起新操作 | 刷新／只读详情，不把UNKNOWN当取消或无目标 |
| 任务成功 | 已确认归档成果、该文明类别完成情况，单位保留 | 下一合法考察／重新部署 |
| 目标失效 | 原因、未获得见闻、未占成功额度、单位保留 | 重新选择合法目标 |
| 等待重新挂靠 | 原归档因易主失效，未完成任务已中止 | 选择新归档城；没有合法城时等待 |
| 共存／派遣位置 | 正式考察团按最新用户方向仅通过派遣／任务变更位置 | 共存原语未确认；不把旧接敌撤退展示成最终玩法 |

现存团不因来源Governor／ACTIVE下降、转出Culture或REALLOCATING而禁用，其合法任务与报告能力保持；归档城当下Tourism／Network效果另外按资格显示。Source易主则立即中止未完成任务、旧绑定失效、原Owner保留团，不能继续向已转移来源写新成果。

## 3. 目的地与任务双栏选择

左侧：已遇见、存活外国Major列表、所选归档城对该文明的三类完成标识与0/3至3/3。右侧：该文明的当前候选城市、选择详情和三张任务卡。

| 任务卡 | 当前资格 | 必须解释 |
|---|---|---|
| 风土考察 | 对方当前实际控制的首都 | 首都迁移会使原目标失效；不是旧首都 |
| 艺文采撷 | 目标城至少一件共同目录合格文化巨作 | 接触文化，不盗取／复制／消耗作品 |
| 奇观巡礼 | 目标城至少一个已完成奇观 | 不计在建奇观，不虚构完成史 |

每卡显示“未完成／可考察／已完成／目标不合格／待核验”及必要理由；成功额度按归档城×外国文明×类别，不能改成每目标城市一次。

部署时间与任务时间分列；任务标准2T，实际按`floor(2×速度倍率)`，不加未经授权的min1。先选择城市、预览可做任务，确认“部署到该城”；到达后由用户确认“开始考察”。不默认自动连续任务／自动派遣，若希望合并指令再单独审查对应事务。

任务预览和部署不占成功额度，提交成功成果时才记录该类别；部署时合格不保证到达时仍合格，开始与提交前重新核验。

确认摘要：归档城、外国文明／城市、类别、部署耗时、任务耗时、首次成功1份文化见闻、当前归档城效果是否已启用。不显示间谍成功率／被发现／俘获风险，因为合法考察确定成功且非敌对。

关闭窗口或取消尚未提交的选择只是退出视图，不取消已确认任务。已确认目标资格失效、现任首都改变、目标城易主或文明灭亡按已有合同取消；暂时读不到事实显示待核验并沿已有HOLD规则处理，不能误取消。战争本身允许部署、开始、继续与成功，不加开放边界、使馆、联盟或商路门槛。

外国未揭示城市／地图位置／具体馆藏的可显示信息粒度尚未单列明确：先规划必要的资格摘要，不能为了仿间谍页面公开全部细节，也不能偷偷增加“必须地图可见”的任务门槛；实施前按实际所需信息确认该局部边界。

## 4. 重新挂靠弹窗

仅在已有归档因来源易主失效后开放，不作为任意时候自由切换来源的按钮。

借鉴总督分配的“城市行→选中→预览→确认／取消”，但使用自有归档action，不调用ASSIGN_GOVERNOR。候选为任意己方Culture Identity城市，不要求ACTIVE IV；显示该城已有三类完成情况与当前效果资格。免费、不限次数，确认后未来新成果写新城并遵守新城额度；旧城既有见闻不迁走。无合格城时团继续存在，不能开始新任务。

## 5. 文化见闻页

按归档城市→外国文明显示风土／艺文／奇观三格，支持已完成／未完成与0/3至3/3。每个来源城必须自身3/3才算完整文明，不能跨城拼凑。

城市摘要分开：历史见闻、当前有效见闻、因当前Owner自身文明而暂排的数量、完整外国文明数量，以及当前已生效的整城Tourism百分点与暂停理由。例如“历史7份／有效6份／当前+12个百分点”只在本城资格成立时显示；资格不足则明确“历史保留，当前效果暂停”，不把理论值称作已生效。

见闻不是可消费／交易资源；Owner过滤只影响当前有效数，不删除历史或重置额度。文明后来灭亡不删除已成功成果。网络接收者没有取得这些历史，不能列成自己的新见闻。

## 6. 文化网络页

N3接入后显示选中接收城的有效来源、各来源独立完整文明集合、接收去重并集、匹配本城专业的实际工作专家数及当前每专家额外Culture。

- 同文明从多个来源只计一次；来源各有一部分不能拼成完整3/3。
- 每名匹配专家`+1×并集文明数`Culture，不放大其它专家；无Identity没有对应受益专家。
- 来源需Culture ACTIVE IV及当前有效成果；路线／中心资格、来源资格、当前Owner过滤和接收专家分别解释。
- 接收不创建见闻，不递归输出；UNKNOWN显示待核验，不能把暂时等待写成断路。

不做全世界网络地图或复杂关系图；摘要与可展开来源明细足够首版使用。

## 技术路线与调查证据边界

本地Stable非权威调查支持“独立窗口＋借成熟交互模式”的候选。UI样式可借，但旅行／建立native helpers对非Spy适用性尚未证，真实Spy身份／SPY_*管线可能继承容量、排除盟友、检测及外交惩罚，不能作为默认实现；换名、非offensive或平民外形均不能证明脱钩。

| 可借鉴模式 | 取用范围 | 不直接继承 |
|---|---|---|
| BTS／BES | 列表、筛选、选中行＋详情／任务预览 | 商路tracker、Spy合法目标全集、offmap／captured权威 |
| Quick Deals | 独立context／入口、页签、查询→确认→回应 | working-deal／外交会话automator与交易行为 |
| GovernorAssignmentChooser | 城市选择、预览、确认／取消与不可用理由 | Governor资格及原生任命操作 |
| 原版任务弹窗 | 简报、分阶段进度与结果卡片 | 原生Spy失败／逃脱／检测及外交后果 |
| HD技能树 | 视觉状态可参考 | 固定4×5树、技能与升级不是本考察设计，不新增升级页 |

最低分层：视图 → 只读查询／资格适配 → 本地待选状态 → 用户确认 → 自有业务action → 实际结果／重新读取。UI不成为任务、成果、归档或奖励权威；处理中锁重复提交、按结果确认成功，失败显示可读原因。

只在开窗、选文明／目标、相关事实变化时定域读取；普通列表用轻量单位／任务摘要，巨作／奇观详情按需。关闭时释放本窗口待选／展示引用、实例及新增订阅；已提交请求由action owner继续持有并收尾，重开时读取当前结果，不丢ACK。业务任务由自身模块继续维护，不因关窗消失。不复制全城采集、每帧Gameplay请求、原生间谍管理器或独立GC。

结构借鉴不意味着可以搬用整个第三方代码／资源；调查未完成许可审查。当前仅规划自己的窗口，不添加BTS／QD／BES为运行依赖，也不改外部Mod。

## 分批实施建议与验收

| 切片 | 范围 | 最小新增验证 |
|---|---|---|
| N-UI1 外观样板 | 自有独立窗口、示例数据的入口／三页面／派遣及重挂靠选择／空与UNKNOWN状态；真实写动作不接入，网络页仅标布局样例／未接入，正式入口N3前隐藏 | 后续获授权才做一次可读性、长中文、缩放、焦点／Esc检查；不跑真实任务或保存仪式 |
| N1 单位与远程交互 | 真实训练来源／cap1、合法目标、独立非敌对部署、三类资格、必要归档／保护路径 | 非Spy远程接口、战争不召回及保护回归的实际差异；UI不能替技术门禁作保证 |
| N2 任务与见闻 | 真实计时／成功提交／取消、城市历史、当前有效数／整城Tourism，接真档案 | 新任务／绑定／历史块才做一个必要保存边界；不复测成熟probe默认OFF |
| N3 网络 | 接真来源集合／接收摘要与专家效果，精确旧Culture Eureka退出 | 原生专家Culture及实际接入／退出；集合组合主要本地，保留Research |

每段独立授权。B165补测已审阅、剩余精确门槛仍按当前Status处理；本计划不因此提前批准任何UI原型或代码。

## 不补设计的边界

- 玩家主动中止、在途改目标、立即返回、任意时刻改归档未明确：首版只放已有合法操作；需要新增时提出具体Design决定。
- 训练中ACTIVE／Owner变化的取消及退款、Gold／Faith购买未授权；不能由原生Spy字段类推。
- 外国未揭示信息的展示粒度；非Spy travel helpers、保护回归位置／时序、极快速度floor0执行点均需对应确认。
- 城市真正摧毁／原Owner消失仍按既有E2／Shared未定边界，不把普通易主重挂靠变成通用恢复。

## 来源与停止点

正式规则：[Culture D0048](../../Design/Content/Culture_D0048.json)、[Shared D0045](../../Design/Content/Shared_D0045.json)、[N1/N2/N3主计划](P0_N_Expedition.md)。

本地调查资料（Non-authoritative、尚未由Main Task提交，不复制／修改／登记为强制context）：`Specialization/Reports/Technical/Investigations/UI/UI_Framework_Reuse_Investigation.md`（独立context／模式／异步边界）；`Specialization/Reports/Technical/Investigations/Diplomacy/CityState_Control_Protection_and_Diplomat_Spy_Semantics.md`（Spy身份与后果）。当前版本仅STATIC，未证明我们的新窗口、最终VFS加载、非Spy部署或新业务可用。

The original page was planning-only. B182 now implements only the existing gate window's create/read/independent-dispatch/refresh/END controls, not the full layout above. [B182 native review](../../Status/Validation/Results/Specialization_B182_Expedition_Spy0_Native_Review.md) records API_UNAVAILABLE before observed arrival and the unresolved coexistence gate; no automatic repair or retest; N2/N3/U2 remain held.
