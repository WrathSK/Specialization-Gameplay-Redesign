# B271.298 — 回合时序诊断与内部载体不可掠夺

实施记录：2026-10-24；用户决定与批准：2026-10-23。用户批准计划，并指定 A/B 默认开启、C 独立开关默认关闭；部署另行批准。本批只改诊断和用户已决定的内部载体数据策略。

## 实现与观察边界

- `Mod/EventTimingDiagnostics.lua`：A/B 按加载后的前6个已观察本地回合（当前游戏回合号去重）启用；第7个回合边界停收。加载中途开始的首个窗口、到期边界的末个窗口可能不完整，摘要明确列出缺失点，不补猜。每次加载重置；不写 Property/存档、不调用 Audit/Mark、不读取城市/建筑集合、不建删载体、不改 GC。
- A：本地 Deactivated、首个后续外方 Activated、本地 GameEvents.PlayerTurnStarted、本地 Activated、LocalPlayerTurnBegin、其后首个 PublishComplete。每点只采一次，即使相邻点余额相同也保留；同点重复回调不重读。余额/可用的 GetGoldYield 以17位有效数字保存；不可用与调用失败明确标记。采样记录网络 availability/revalidation 及最近确认序号。
- NetworkBridge 的 NETWORK_VERIFIED 出口只增加受保护观察调用，不改变网络状态、通知或重新验证流程。共享 epoch＋单调 observationSeq 表示本 Mod 观察回调次序，**不是引擎内部提交顺序或跨线程时钟**。首次余额变化只能定位到两个采样之间；不能排除其他金币交易，也不能把未记录的入账时机写成事实。
- B：现有 PerformanceCounters 回调/audit 标量进入独立有界累积器，在本地开始/结束输出相邻边界差值；dispatch前8项、audit前32项（目前足够覆盖全部登记模块）、TOTAL/OTHER_TOTAL/REST。既有手动观测不被重置。CultureAesthetic/Lv3Support 登记，未知 audit/dispatch 进入 OTHER。**dispatch 是被现有埋点计数的监听回调次数，并非原生事件总数**；模块没有埋点时不臆造计数。
- C：右键现有“专业化诊断”入口开关；左键仍打开原面板。仅本次加载有效，默认关闭。Gameplay 与 BackgroundRoutes UI 各追加独立监听，原监听不包裹、不替换、不重新排序。观察当前订阅的原生事件名称并保护可选事件；未知签名的 owner/city 为 UNKNOWN。已核实的回合玩家、CityWorkerChanged/CityPopulationChanged 参数才解码；LocalPlayerTurnBegin/End 使用本地玩家。
- C 从本地结束至下一 LocalPlayerTurnBegin，每侧最多400条；每12条批量输出。PublishComplete只累计并刷新已积累批次，不逐条输出。**不新增 SystemUpdateUI/帧监听或定时器**。关闭时没有 EVENT_ORDER 记录。未提供/注册失败的可选事件列入 HOOKS，监听异常计入 observerErrors。到上限、窗口到期、结束记录缺失或记录数量不符均不得标为完整。
- 采集器仍使用既有 TRAIN 协议、256条环、4096字符行上限、既有读取上限；新记录进入 records.log。summary.txt 增加入账时点/余额/网络对照、回调榜单、事件窗口完整性/截断。摘要自身最多4096条新记录，溢出显式报告。环覆盖、打印限额、关闭游戏时未刷出的批次仍可能丢失；不据此报告完整或实机 PASS。

## 用户决定：D4 内部载体不可掠夺

内部载体没有玩家可用的生产/修复入口，载体自身被掠夺可导致真实区域完好而效果丢失。用户决定：所有 `InternalOnly=1` 且字面前缀 `BUILDING_SPC_` 的建筑，包括效果载体、访问标记和保留的内部测试/退休定义，都采用 `Buildings_XP2.Pillage=0`。真实建筑/区域的状态仍由原能力输入负责；不扩展玩法规则。

`Mod/Data/InternalCarrierPillage.sql` 为一条查询生成 INSERT（已存在行不重复），LoadOrder=10002000，晚于所有 SPC 建筑定义。实际引擎数据库副本核对：Pillage 为 BOOLEAN NOT NULL、默认1；4557个目标，原XP2目标行0个，执行后4557个均为0；非目标XP2行所有列不变；重复执行不变。现有目标行不存在是本批核实的前提，未来若其他数据文件先定义 SPC XP2 行，应重审其冲突处理，不能把本次结果外推到不同规则集。

数据定义在加载时应用；不保证恢复旧存档已掠夺载体。仍按当前版本新开存档支持规则，不迁移旧存档。ResearchApply/ResearchInfrastructure/ResearchChair 的掠夺重建逻辑本批保留，作为后续可清理项；CarrierHealthTrace 保留，预期不再出现 CARRIER_PILLAGED_PRESENT，但须实机验证。

## 能力依赖核对（STATIC_CONFIRMED）

| 能力/载体家族 | 原真实输入或有效性约束；本批不改 |
|---|---|
| 一级专家支持、工业支持、二级住房/GPP | `SpecialistSupport.lua:Anchor` 检查准确锚点、所属、完成和真实区域 IsPillaged；ResearchSupport/IndustrySupport/Lv2Housing/Lv2GPP 仍通过它撤销。B270当前正向回归覆盖锚点掠夺、修复与重复无写入。 |
| 科研基础设施、学以致用、学术主持 | `DistrictCompleteness.lua:Calculate` 排除被掠夺建筑和区域；`ResearchInfrastructure.lua`检查学院状态；`ResearchApplyModel.lua:Plan`消费有效领域D；`ResearchChairModel.lua:Plan`逐真实建筑排除掠夺。载体健康检查不替代这些输入。 |
| 跨学科研究 | `ResearchCrossModel.lua:Plan`排除未完成/被掠夺真实区域，原UI采样及当前源收益仍有效；不以虚拟载体损坏表达区域状态。 |
| 审美、艺术内涵 | `CultureAestheticModel.lua:Plan`逐普通建筑检查完成/掠夺；`CultureMeaningModel.lua:Plan`消费同一真实D快照，保留既有文化产出隔离限制。本批新测试覆盖完好→建筑掠夺→区域掠夺→修复。 |
| 文化网络专家收益 | `CultureNetwork.lua`接收锚点检查完成/IsPillaged，并保留网络当前可用性与历史来源证明；原载体损坏重建保留。 |
| 商业化金币、资本投资报价与发展投资 | `Commerce.lua:depth` / 当前领域D排除真实掠夺；资本/发展报价仍消费既有模型输入。`DevelopmentInvestment.lua`明确排除被掠夺锚点的有效建造候选；合同/资格/金额不重写。 |
| 学术传统 | `ResearchTraditionEffects.lua:desired`使用当前ACTIVE与Store年龄/当前回合游标；它是历史计时能力，不新增真实建筑掠夺归零规则。已有载体损坏会重建。 |
| 时代对话 | `DialogueEffects.lua:reconcile`使用当前资格和已完成项目历史；源码明确普通建造不是输入。保留原累计效果/资格规则，不凭载体不可掠夺补新暂停条件。 |
| 灵感迸发、人文见闻旅游 | `CultureInspirationModel.lua:Plan`使用当前巨作时代集合与ACTIVE；`CultureInsightsTourism.lua:Desired`使用既有历史记录与ACTIVE。保留各自输入和载体损坏重建，不追加建筑存在门槛。 |
| 标准化、工程研习增益、巨构工程学 | `StandardizationEffects.lua:source`使用已学模板、ACTIVE及L；`IndustryWonderEffects.lua:reconcile`使用ACTIVE和文明时代/奇观时代。历史知识不因真实建筑被掠夺而删除；本批不新设掠夺暂停。 |
| 访问标记、认领/施工/商业/资本/发展/重组/人文培训/时代对话/研习入口 | 原各入口模块继续维护资格；内部标记不可掠夺不放宽动作资格、不直接授予收益，不绕过原确认时检查。 |
| 历史B050/B051/B053/B054/B055/B057/B058/B059/B060/B061/B082、旧DEV/LV4/PROBE等 | 全部定义统一不可掠夺，但不重启退休/隔离writer、不创建历史收益。`Gameplay.lua`明确 retired 模块与现行替代；保留精确退出清单。 |

核对未发现现行能力把“载体自身被掠夺”当作唯一的**设计上**停效依据；一些历史/时代能力本就不依赖真实建筑掠夺，本表显式区分而非宣称所有能力都随建筑掠夺清零。若原生测试显示上述依赖不生效，报告证据/必要的 DESIGN_DECISION_REQUIRED，不擅改规则。

## 本地验证

- `test_b271_diagnostics.py`：15项通过，实际 Lua5.1、六点/去重/精度、关闭C、双侧400上限、Publish计数、六回合截止/重载、异常隔离、未知参数、OTHER、采集落盘/摘要/缺失、真实输入掠夺模型、实际引擎数据库内存副本SQL与加载顺序。
- 原 B269 内存13项、B270事件10项/恢复8项、B267范围回归243项（原12项历史排除保留）、B138六组更新合同通过；B270当前收益配置与恢复矩阵通过（既有532配置范围）。GC差分测试保持既有策略。
- 全部189份Lua通过Lua5.1编译；25份XML解析；modinfo311个唯一引用全部存在（另含modinfo本身的312文件包）。
- 额外尝试的旧 `test_culture_aesthetic.py` 在已装载数据库上重复插入定义失败；旧 `test_culture_meaning_l2c.py` 27项中10项历史断言/fixture错误。已在未改动HEAD `d078a77` 的临时只读导出源码上复现相同错误，**不计PASS、不削弱旧断言**；本批使用当前实际模型的独立掠夺用例及上述既有现行回归覆盖改动范围。
- 尚无新的 USER_GAME_TEST_PASS；引擎实际入账、事件投递、灾害掠夺效果均为 USER_GAME_TEST_REQUIRED。

## 交付边界

User decision：确认是否另行部署B271；本轮不部署、不创建main PR。两份README预览稿保留，不进入本批提交。

User testing：部署获批后，新版本支持的新开存档；右键“专业化诊断”开启C，保持采集器运行，打2–3个本地回合，提供日志；如遇洪水/掠夺，检查真实状态及载体追踪。余额相等不是未入账的充分证明，缺失事件保持UNKNOWN。

Primary next：在部署审批边界停止；获批后按原有事务工具与游戏退出检查部署，再依据日志交由Advisor分析。当前live/main仍为B270.297。
