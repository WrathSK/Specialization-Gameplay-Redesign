# Specialization P0 Status

Document Owner: Codex
Status Revision: S1165
Implementation Build: develop B550.577 / modinfo577. Installed temporary B549.576 / modinfo576. Stable B528.555 / modinfo555.
Architecture Revision Reviewed: A0192
Design Revision Reviewed: D0067
Latest Accepted Design Revision: D0067
Design Sync State: D0067_MANAGEMENT_CAPACITY_DESIGN_ONLY
Work State: MANAGEMENT_CAPACITY_LAYOUT_PREVIEW

## CURRENT AUTHORITATIVE STATE

| Area | Current state |
|---|---|
| Source and installation | Develop B550.577 / modinfo577 [契约审计第 5 批：去掉自产数据复查](#contract-audit-batch-5-own-payloads-not-re-validated--s1165)（第 2–4 批见 [S1159](#contract-audit-batch-2-legacy-compatibility-retired--s1159)、[S1161](#contract-audit-batch-3-internal-asserts--s1161)、[S1163](#contract-audit-batch-4-dead-checks-removed--s1163)）。本机[已临时安装 B549.576](#contract-audit-batch-4-installed--s1164)，main 稳定包是 B528.555。 |
| Recovery | 本次临时安装回执绑定了已核对的 B528.555 原包。更早的 B489、B527 回退凭据见[稳定版部署记录](#b528555-stable-playtest-package-deployed--s1123)。 |
| Validation | B544 实机：负责人接受激活状态颜色与窗口宽度，要求标题改用城市面板的带底色等级徽章，并指出部分标题偏上。B545 已修改，原生渲染待复验。考察团归档仍沿用[先前的证据边界](#expedition-archive-city-choice--s1138)。 |
| Next action | B549.576 已临时安装（含第 2–4 批），做一次短测（建城、投资、存档读档，看采集日志有无 `[SPC][ERR]`）。契约审计后续：夹具替身迁移（收掉 S1163 保留的四处回退）、诊断显示路径去留，待 Owner 决定。容量窗口：检查带底色徽章与标题垂直居中。本轮之后界面外观冻结，其余打磨见 [Playtest Backlog](Playtest_Backlog.md#pre-release-polish)。 |

Use [Authority](../Workflow/Authority.json) for the active task and version pointers and the [resumption guide](../Workflow/README.md#action-scoped-reading-and-interruption-recovery) when picking up after a pause.

2026-11-05 Owner明确授权按现行统一计划持续推进，普通片段完成后不再逐片请求授权；遇到规定的外部审计检查点、新的玩法／核心职责／保存或不可逆操作取舍、无法安全解决的问题或现有明确门禁时停止并报告。每片保留定域调查、Runtime Impact Contract、本地验证、独立commit/push develop和当前状态记录。此授权不自动部署、不晋升main、不启动游戏，也不把本地结果当实机通过。

## Recent checkpoints

### Contract audit batch 5: own payloads not re-validated — S1165

Owner 2026-11-26 批准第 5 批计划。原则：自产数据只在存档边界（存储写入与读档）校验一次；保留新鲜度、身份、引擎读数和读档校验。

B550.577 实施内容：

- **CA-A03**：存储的训练观察只核对发起会话身份，不再复查序号、状态、输入长度与令牌长度。
- **CA-A07**：区域采样的跨界面缓存只在计数器未发布时跳过，不再复查自家行与计数器类型；来自引擎的区域类型和产出索引保留标量检查。运行期回收不再复查自家界面的开关与令牌参数。
- **CA-A09**：考察见闻存储写入时不再重新校验 `Read` 已校验的旧值，不再判断 `Game`/`P.SetProperty` 是否存在；候选值在存档边界校验一次。
- **CA-C02**：资本、发展、对话、工程研习模型不再校验所拷贝的存档旧值，只校验新结果；商业模型七个状态转换同样处理；商业信誉用途只在 ACTIVE 真未知时给“未知”；网络桥去掉 `RouteSignalRevision or 0`、`P.RouteUnitRelevant` 与 `NetworkCityGeneration` 存在判断和来源等级的类型复查；网络输入直接使用 BoostConfig；运行工作遇到畸形转移范围报错（`RUNTIME_TRANSFER_SCOPE_INVALID`），不再扩大成全量审计。
- **CA-B11、D02、D10、D15（部分）**：机构展示、城市潜力、视图观察器、商业界面可用判断、发展投资与标准化效果的界面读数、计时项目客户端、对话刷新，只保留身份与新鲜度检查。

**未改**：D15 的 `UI/BoostGreatWorkRead`——它读取的 `totalScience` 等字段在生产代码中没有产出方，这条诊断显示路径疑似只服务夹具，与诊断路径去留一并决定。

实施中发现并修复了一个本批自己引入的问题：计时项目客户端一行末尾的注释吞掉了计数器写回，已在提交前修正，相关 s7d3b 用例恢复与 HEAD 一致。

本地验证（`LOCAL_SIMULATION_PASS`）：

- 新增 `DevelopmentTests/test_contract_batch5_own_payloads.py`，5 项通过；前四批专项 25 项仍通过。
- `CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-28a7f51387bc4dc3a2564472a5d1d120/closure.json`，SHA256 `d33f1a1998c15e991f07434120e5c52139a37b4f3565d143dd146ca026386806`，已测源码快照 `9fe5f6399dd2642021822599c78840b78fc574c23b937998ecaebd208e0543c7`。
- 175 份 Lua 编译、26 份 XML 解析、304 个包文件引用检查通过。
- 与 HEAD 全量逐模块对比（495 个测试模块，两侧同一固定数据库配置）：451 个一致。修正后剩下的新增失败均属以下几类，按 DevelopmentTests README 保留原断言并登记为“已被 B550 取代”：
  - 专测本批删除的复查：考察见闻存储传入非法旧值（expedition_spy_store、s7b1 及累积套件）、有效事实给出畸形 ACTIVE/潜力（pu06b）、发展投资界面读数的协议/世代号（s9d1b）、商业模型对被改坏的内存状态调用不产生新状态的 `EffectiveSelections`（s8b7a 及累积套件）、有效事实读取返回 nil（s4a 一个子例）。
  - 夹具没有加载 BoostConfig（s9e3 1 项）。
  - `test_b244_capital_storage` 的一个用例在 HEAD 上同样时好时坏，不计为回归；`test_refactor_s9e6` 一个用例在 HEAD 上已失败，只是失败形式改变。

实机：正常情况下行为不变，无需专门测试；B547 起的短测仍待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 4 installed — S1164

B549.576 / modinfo576 temporary, 305/305 MATCH at 91c748df944791c9cb8c7d5452bfde119b4ef640ad3c2a71b0a88a506d82cea3. Receipt B549.576-3a272e7-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 3a272e7f5aa1e40f2d3f6308fc73b39eea3fa743。先按 B548 回执还原 B528.555 原包，再安装 B549；包文件仍为 305 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。玩法不变；B547 起的短测仍待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 4: dead checks removed — S1163

Owner 2026-11-26 批准第 4 批计划，含 CA-D14。原则：启动失败的模块不导出 `shared.X`，声明依赖它的模块会被跳过，所以对已声明依赖、已 include 模块和必有方法的存在性检查永远不会失败，予以删除；对非声明依赖的检查是真实的可用性判断，保留（例如 GreatWorkFacts 对存储、DevelopmentInvestment 对商业）。

B549.576 实施内容：

- **CA-D05**：商业、资本投资、发展投资、施工队、行业历史、投资动作、标准化、标准化效果、文化启发、考察训练、资产重组中约 25 处对已声明依赖的检查改为直接调用；`if shared.FactChanges then 注册` 不再悄悄跳过注册。
- **CA-D01**：投资动作、单位动作、单位目标去掉 “UnitSiteFacts 不存在” 分支；引擎读取失败时的全量扫描保留。
- **CA-D04、D12、B02、B09（部分）、A04**：Gameplay 接线直接调用导出方法；GreatWorkFacts 不再关闭不可能存在的旧实例；有效事实去掉事实世代和写入栅栏周围的冗余检查；存储的 `publishFact` 去掉走不到的回退记录，登记时不再重新校验内存索引。
- **CA-A06（部分）**：延迟生命周期恢复不再断言存储必定 include 的模型。重复 `Validate` 未改。
- **CA-C04（部分）**：运行工作去掉 `P.Count`/`P.Observe`/`SPCRuntimeComposition` 存在判断和“存储前夹具”退出确认分支，并显式 include `RuntimeComposition`；“legacy” 注释改正。
- **CA-D06、D09、D03、C03、D11、D14**：商业/发展投资直接用 `Inspect` 和 `CurrentEffectPartners`；文化网络去掉永不成立的兼容条件；三个投资界面适配器要求观察者；文化意义模型删除 `bitParts`、`DiagnosticParts` 和无用参数；五个模块直接 include 训练诊断；考察训练删除读取前后的模块/方法替换检查。

**保留（代码中已注明，留作“夹具替身迁移”后续项）**：`CityReference.Read` 的无存储分支、运行工作的 `NewReader`/`Inspect` 回退——几十个夹具替身没有 `ReferenceToken` 或只定义 `Read`；CA-B07 与区域完整度的 `facts.Version` 回退——当前玩法用例 `test_shared_d_fact_read` 用冻结的旧版有效事实重放。

测试夹具（只改夹具，不改断言）：共享存储夹具启动 `FactChanges`；商业、资本、组合、标准化、文化网络夹具的替身补上真实模块必有的方法（`WithPhase`/`Inspect`/`NewReader`、`TransactionCurrent`、`ProofRevision`、`HistoryStartStatus`）；`test_pu04_negative`、`test_b239_commerce` 在启动前创建 `FactChanges`；`test_refactor_s5d4c5` 一个用例补上空存储。

本地验证（`LOCAL_SIMULATION_PASS`）：

- 新增 `DevelopmentTests/test_dead_checks_retirement.py`，5 项通过；前三批专项 20 项仍通过。
- `CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-74f5df76b4ed431fae5c2d5214a21096/closure.json`，SHA256 `709cfbea6a909bd1215542ceaa158099db0be4935473e46546252e04d6b63055`，已测源码快照 `e3c71d7b0b3d0c4085192e9f042c88006ff18f3a5cca6ffa0e2aa2cbedabe744`。
- 175 份 Lua 编译、26 份 XML 解析、304 个包文件引用检查通过。
- 与 HEAD 全量逐模块对比（494 个测试模块，两侧同一固定数据库配置）：438 个一致。夹具修正后剩下的新增失败用例（去重约 22 个，另有 s8/s9 累积套件重复计入）均属以下几类，按 DevelopmentTests README 保留原断言并登记为“已被 B549 取代”：
  - 夹具替身缺少生产必有的方法：`P.Count`/`P.Observe`（文化启发/意义探针、attribution、s5d4c2 的跨城转移用例）、`ExitCompleted`（s7a6、s8c4、s8c5c 的 B339 用例）。并入夹具替身迁移后续项。
  - 专测本批删除的路径：训练诊断文件缺失（o7 商业/网络追踪 4 项）、同一会话重启 GreatWorkFacts（great_work_notifications、p0_k）、无观察者构造界面适配器（b239/b241/b246 界面与 s9a2）、读取中替换方法（s9d1b 1 项）。
  - 用历史探针源码重放诊断阶段（culture_meaning_diagnostic 等，调用已删的 `DiagnosticParts`）。

实机：正常情况下行为不变，无需专门测试；B547 起的短测仍待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 3 installed — S1162

B548.575 / modinfo575 temporary, 305/305 MATCH at ff70ebe4b8e9dd1a7190b3b83d7fb54150067e8c90e3b144ac664e3cda91a837. Receipt B548.575-940dec6-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 940dec6cf9503af4cc505f153670d065ff686575。先按 B547 回执还原 B528.555 原包，再安装 B548；包文件仍为 305 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。合法状态下玩法不变；B547 起的短测仍待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 3: internal asserts — S1161

Owner 2026-11-26 批准第 3 批计划。B548.575 实施内容：

- **CA-B03 有效事实**：总督状态为“已确认”时，城市与 1–4 级上限是 `Probe.GovernorGate` 的约定，违约就报错（`GOVERNOR_GATE_CONTRACT`）；状态不是已确认时仍记为 `UNKNOWN_GOVERNOR`。
- **CA-B05 事实传播绑定**：目标模块启动失败或不存在时仍然跳过；模块存在但缺少声明的方法时报错（`FACT_BINDING_METHOD_MISSING`），错误进入现有绑定错误记录。网络桥直接调用 `RoleFactsChanged`，不再依次尝试三个名字。
- **CA-B06 事实用途投影**：保留未就绪、ACTIVE 未知、投资挂起、深度错误（未审核等级）这些真实“未知”；身份、ACTIVE、深度值、锚点字段形状不对时报错（`FACT_USE_*_CONTRACT`）。
- **CA-B08 反向依赖索引**：非法城市编号、来源或参数直接报错；只有超出容量才关闭索引，调用方按原设计回退全量重算。
- **CA-B10 区域完整度**：计算时目录查不到建筑改为断言（`DC_CATALOG_ENTRY_MISSING`）；采集时已检查过的布尔值不再在计算里复查；只给夹具用的 `unplaced` 输入删除。

测试夹具（只改夹具，不改断言）：共享存储夹具的总督替身改为与真实 Probe 相同的约定（只有 1–4 才回报已确认）；`test_refactor_s5propagation` 的网络桥替身改名为 `RoleFactsChanged`；`test_shared_d_fact_read` 的纯计算用例改用真实的场外建筑观察输入。

本地验证（`LOCAL_SIMULATION_PASS`）：

- 新增 `DevelopmentTests/test_contract_batch3_asserts.py`，6 项通过；第 1、2 批专项 14 项仍通过。
- `CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-77537c85130949d299860b4b276cafd6/closure.json`，SHA256 `53e4dfe084f84b20f47321af6a9817ff6986b12871d0dc4df66413726339c5c8`，已测源码快照 `3bdc25cded9e23b838265dc3c816c46348e99ce56d07564d7b7e0d77e33bc2cf`。
- 175 份 Lua 编译、26 份 XML 解析、304 个包文件引用检查通过。
- 与 HEAD 全量逐模块对比（493 个测试模块，两侧同一固定数据库配置）：夹具修正后，只剩 5 个用例新增失败，均为本批有意改变的行为，按 DevelopmentTests README 保留原断言并登记为“已被 B548 取代”：`test_refactor_s6d` 与 `test_refactor_s6g` 各 2 项（断言非法输入会关闭索引），`test_pu01_fact_use` 1 项（人为把深度值改成 NaN 来模拟“未知”）。

实机：正常情况下行为不变，无需专门测试；日常游戏顺带观察采集日志有无新的 `[SPC][ERR]` 或绑定错误。B547 短测仍待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 2 installed — S1160

B547.574 / modinfo574 temporary, 305/305 MATCH at baae506a3539c9a2cc104c77d9d64f4c813a30a98e1fd962287c4b714cd7df54. Receipt B547.574-fde6902-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 fde69022d7626833139860aed59dcfb65a8e2f69。先按 B546 回执还原 B528.555 原包，再安装 B547；包文件仍为 305 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。新游戏玩法不变；旧版本存档不再支持。实机短测待做（`USER_GAME_TEST_REQUIRED`）。

### Contract audit batch 2: legacy compatibility retired — S1159

Owner 2026-11-26 批准第 2 批计划，并同意 CA-A05 一起退役。依据是 2026-11-25 的决定：发布前不做任何旧版本或旧存档兼容。

B547.574 实施内容（旧代码保留在 Git 历史）：

- **CA-A01 城市进度存储**：删除 `StartLegacyTest` 双记录测试模式及全部 `legacyTest`/`modern` 分支、`UsesNewAuthority`、双城上限、旧版描述文本；删除 schema 1 / PREPARED 记录形状、旧进度导入（`Import`）、`BlocksLegacy` 和 `BindingProbe` 分配分支。生产入口只有 `Start(P,shared)`。
- **CA-D13 投资动作**：删除城市属性上的第二套投资账本、按玩家分桶和走不到的写入通知；账本只认存储。启动恢复只扫描已登记城市，避免对登记中的城市误报。
- **CA-B01 有效事实**：删除 `CityFlowProbe` 分支和属性账本回退，读取前断言城市归存储管理。
- **CA-C06 网络输入**：删除“未跟踪城市”分支。
- **连带**：商业来源判定对未登记城市直接给 `COMMERCE_SOURCE_UNADMITTED`；标准化模板账本只走存储；学术传统效果始终使用严格载体引用；ReadFailure 名单去掉两个已不存在的模块名。`CityReference` 与 `RuntimeWork` 只删掉 `UsesNewAuthority` 断言，给假存储夹具用的回退留到“存在性检查”批次。
- **CA-A06（schema 1 部分）**：延迟生命周期父记录不再接受 schema 1。
- **CA-A08**：区域采样直接调用 `FindID` 与 `Map.GetAdjacentPlot`，不再回退全量重扫。
- **CA-A05**：删除读档时的三个重建器（已知标记、模板元数据、已完成认领计时器）及其报告文本。子记录异常时的隔离（SAFE-004）保留。Architecture 已注明 SAFE-004 的重建在同版本下没有可作用的形状。

测试夹具迁移（只改夹具，不改断言）：`test_store_write_boundaries` 共享存储夹具不再启动已退役探针；`test_pu01_fact_use`、`test_pu04_negative`、`test_refactor_s5b`、`test_refactor_s6b`、`test_refactor_s6c`、`test_refactor_s6f` 的假存储补上 `Base`/`Investment`；`test_investment_update_propagation` 增加存储接口替身；`test_arch_v2_c2` 的模拟对象补上 `FindID` 与 `GetAdjacentPlot`。

本地验证（`LOCAL_SIMULATION_PASS`）：

- 新增 `DevelopmentTests/test_legacy_compat_retirement.py`，6 项通过；第 1 批专项 8 项仍通过。
- `CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-402fcacd37924724b7ef12ea8d74ac18/closure.json`，SHA256 `cc9a29a29cb842e1b019f2b94e79200042dfccb4dbb0c5b2f03a234e10ea84df`，已测源码快照 `2e70ef4280e3bb9605924f1be10d472e5f97150931c932a38b03b9fff15e5ead`。
- 175 份 Lua 编译、26 份 XML 解析、304 个包文件引用检查通过。
- 与 HEAD 全量逐模块对比（492 个测试模块）。初跑有差异的 116 个模块在两侧使用同一固定数据库配置后重跑：60 个与 HEAD 一致，其余经夹具迁移后剩下的新增失败用例均为以下几类，按 DevelopmentTests README 保留历史阶段原断言，登记为“已被 B547 取代”：
  - 专测已退役路径或字段：A05 已知标记与模板元数据重建（s8b1、s8b9 及包含它们的 s8/s9 累积套件、pu06b、pu09、s8a 的模板隔离字段）、`UsesNewAuthority` 断言（s7f、s8c1、o7 四个退役测试共用的冷加载夹具）、无存储旧流程（s5b、s6b 各 1 项）、`BlocksLegacy` 排除（s9e6）、无 `Map` 的采样器（s9e2 1 项）。
  - 用冻结旧版本源码重放（git 基线的存储/模块配当前子记录模块）：s9g3、s9f4、pu06a、b245、b398 的基线反例。
  - 夹具仍以 `CityFlowProbe` 供给事实：culture_meaning_probe 1 项。

实机：`USER_GAME_TEST_REQUIRED`。新游戏和同版本读档的行为应不变；旧版本存档不支持，读到会直接报错。建议一次短测：建一座城、投资一次、存档后读档，确认采集日志里没有 `[SPC][ERR]`。

### Contract audit batch 1 installed — S1158

B546.573 / modinfo573 temporary, 305/305 MATCH at d46d6b2fb3adbbd99852d5156bd3e4cd54f71acfe62710710f6b83a5ab52aaaa. Receipt B546.573-43120e1-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 43120e16d5434a5777edd4ebcbc2ce696309a526。先按 B545 回执还原 B528.555 原包，再安装 B546；新增错误探针使包文件增至 305 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。玩法数值不变；探针输出能否进入 FireTuner 采集待日常游戏顺带观察。

### Contract audit batch 1: visible errors — S1157

Owner 2026-11-25 读完[契约与快速失败审计](../Reports/Technical/Contract_Audit/Contract_FailFast_Audit_2026-11-25.md)后决定：

- **工程原则**：不过度防御，自己代码之间违约就直接报错（“炸了说明有 bug”）；同时要有足够的探针和错误日志查根因。探针必须与生产模块隔离，可以直接删除而不影响生产。
- **兼容**：发布前不做任何旧版本或存档兼容。
- **CA-C05**：采用方案甲，删除回复的格式复查。
- **CA-A01、CA-D13**：退役。按不做兼容的原则，CA-A05、CA-A06 的 schema-1 部分和 CA-A08 并入同一退役批，尚未实施。
- **第 1 批**：Owner 授权按计划实施。

B546.573 实施内容：

- **错误日志**：新增 `SPCSafeCallbacks.Record`（`Mod/SafeCallbacks.lua`），把生产代码接住的错误写进 `shared.ErrorLog`。日志最多 32 条，相同标签和文本只计数不新增，文本截断到 400 字，不影响执行流程。
- **独立探针**：新增 `Mod/UI/ErrorProbe.lua/.xml`，只读取该日志，用 `[SPC][ERR]` 前缀打印新条目。生产代码不引用它，删除其 modinfo 条目和这两个文件即可移除。FireTuner 采集脚本已加入该前缀的允许名单。
- **CA-A02**：Store 的商业信誉和学术传统回合推进、事实发布观察者、训练引用观察者，接住错误后改为写入错误日志。原先没人读的 `commerceError`/`traditionError` 字段已删除；测试仍读取的两个字段保留。
- **CA-C01**：非隔离记录的信誉校验不再包保护，失败直接报错，由上层原有保护挂起城市并记录原因。
- **CA-D07**：商业、标准化、施工队、资产重组、发展投资五处原因映射，遇到未编码的错误时写入原始文本。资产重组不再把任意大写单词当作原因。
- **CA-C05**：回复发布只检查请求身份与传输上限，格式错误直接抛出。Gameplay 四个回复点在失败时记录具体原因。

本地验证（`LOCAL_SIMULATION_PASS`）：

- 新增 `DevelopmentTests/test_contract_batch1_errors.py`，8 项通过。
- `CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-d29f8a723ce4487e8cd214c563df9ca7/closure.json`，SHA256 `b1ed4ec128198fdb5ae0788cb6f385826208b1c32e166ae63cfea182c98ac5d7`，已测源码快照 `80a2be80f9771046ef691a5c1dbce3807cc1165711c60a0b0a999f7f701cabd1`。
- 175 份 Lua 编译、26 份 XML 解析、304 个包文件引用检查通过。
- 与 HEAD 逐模块对比 27 个相关测试模块：其余结果不变。s9c 系列历史阶段测试（在 HEAD 已大面积失败）新增 6 个失败，全部是专门断言被删格式检查的用例（表代替字符串、`legal=1`、元表、NaN 等）。按 DevelopmentTests README 保留历史阶段测试原断言，未修改它们；身份检查与传输上限用例仍拒绝。

实机：探针打印能否进入 FireTuner 被动输出尚未在原生环境确认（`USER_GAME_TEST_REQUIRED`，可在日常游戏中顺带观察）。玩法数值不变。

### Management capacity title badges installed — S1156

B545.572 / modinfo572 temporary, 303/303 MATCH at 60ba588e917acda985fbe0c5658b3f9e3c4a8d4e35c06767d2620d6c49ddd89b. Receipt B545.572-03cc09c-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 03cc09c25109068395008110dcbb28ff033430c2。先按 B544 回执还原 B528.555 原包，再安装 B545；新增 24 像素等级徽章图集使包文件增至 303 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。实机外观待复验。

### Management capacity title badges — S1155

B544 实机截图已归档至 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B544_Capacity_Level_Titles_20261125/`，移动前后 SHA256 一致（城市面板参考图 `d0d8618b…`，容量窗口 `4d89ae97…`），附 manifest。

Owner 2026-11-25 对 B544 的意见：激活状态颜色与窗口宽度没问题；标题图标应改用城市面板里带专业底色的等级徽章；部分标题（如金色的“学者结社”）偏上。Owner 同时决定：本轮修好后容量窗口界面暂停，除非之后发现大问题，打磨挂到[发布前润色待办](Playtest_Backlog.md#pre-release-polish)。

截图测量：标题带占格子顶部约 0–30 单位。文字比深色标题带中心高约 0.8 单位；金色状态的顶部金边约占 3 单位，文字比可见区中心高约 1.9 单位；图标居中。B545 将标题文字整体下移 1 单位，已激活（金色）格的标题容器再下移 1 单位。图标改用 `ICON_SPC_LEVEL_<专业>_<等级>`，与城市面板相同。

Owner 批准新增一张图集 `Mod/Textures/SPC_Level_Icons_24.dds`：由已审核的 B254 64 像素等级图集逐格缩放（预乘 alpha Lanczos），无损 BGRA8，96x96，36992 字节，SHA256 `f6ce8291cff46e88b3e227bf534a18d43d39a11cb5b926384fd7b16f6f524158`。按一次性二进制发布例外单独提交，见[机构美术说明](../../Art/Institutions/README.md#b545-capacity-title-badges)。B544 的 `SPC_Institutions_24.dds` 不再使用，留待发布前润色时退役。

本地验证（`LOCAL_SIMULATION_PASS`）：专项 5 项及 B251 机构图集 19 项通过；`CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-f058c91dca7c4adaa6704df297621b9b/closure.json`，SHA256 `dc5a6dede06dcb8dcd9df33dc91a6a8c11657bd8bcce3e595e3773c6a5ef60bf`，已测源码快照 `f49e89b3762ba93240a724cb4a11e33a5ed38081c63b1ae0880e150a97868a14`。174 份 Lua 编译、25 份 XML 解析、302 个包文件引用检查通过。

### Management capacity gold means active installed — S1154

B544.571 / modinfo571 temporary, 302/302 MATCH at 44a9f9e228ddb559c688bb4b3d70312e6317611043c855328c33bce8b8865eb7. Receipt B544.571-464efa5-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 464efa5aa73eff56da7ee7e32a66f28a81738e03。先按 B543 回执还原 B528.555 原包，再安装 B544；新增 24 像素图集使包文件增至 302 个，12 个已退役开发版路径按既有清单移除，事务标记已清除。实机外观待复验。

### Management capacity gold means active — S1153

B542 与 B543 实机截图已归档至 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B542_Capacity_Governor_Tree_20261125/` 和 `B543_Capacity_Institution_Slots_20261125/`，移动前后 SHA256 一致（`b81bea71…`、`10e0589c…`），各附 manifest。截图显示晋升格的普通、获得、选中三种状态在原生渲染中都是金色，只有不可取得是深色。

Owner 2026-11-25 指出 B543 的问题：机构图标越过标题带分隔线，标题文字没有垂直居中，“容量已到位但机构未建立”不清楚，选中状态让未建立的待到位等级也呈金色，窗口左右空白过多。Owner 同意 B544 的方案：金色只表示已激活，其余等级一律深色，标题右侧注明“[回合图标] N 回合”“容量已到位”或“确认后撤回”，能力列写已激活、未激活或未建立；机构未建立且未分配的等级另加总督界面未任命时用的暗化遮罩。标题放进 26 单位高的居中容器，机构图标改用 24 像素。窗口宽度贴合行宽加 64（最小 1024，不超过屏宽）。

Owner 同时批准新增一张图集 `Mod/Textures/SPC_Institutions_24.dds`：由已审核的 64 像素机构图集逐格缩放（Lanczos），无损 BGRA8，96x96，36992 字节，SHA256 `8cba53829ee7265d85fd9da83ed65b0df1af5aaba4af77d908235c8a040d4a93`。该文件按一次性二进制发布例外单独提交，32 和 64 像素图集不变，记录见 [机构美术说明](../../Art/Institutions/README.md#b544-capacity-title-size)。

本地验证（`LOCAL_SIMULATION_PASS`）：专项 5 项及 B251 机构图集 19 项通过；`CurrentGameplay` 固定 HD 数据库 42 项通过，记录 `local/refactor/CurrentGameplay-e16e80a913224c328c6d43222f08f9b0/closure.json`，SHA256 `eddf19622eb54c8cf2b79537db2b172d5a109243122a0e0d7340bf464a52cf2b`，已测源码快照 `e267a101e922518cdbf05666bf9cce91987b94e88c5f48e517eae8b87d55674a`。174 份 Lua 编译、25 份 XML 解析、301 个包文件引用检查通过。

### Management capacity institution slots installed — S1152

B543.570 / modinfo570 temporary, 301/301 MATCH at 1fc9908a589cdd642c1d084dedd7af037d80d380ec6dc1c0100fef0b08ac258a. Receipt B543.570-15bf669-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 15bf669e4b2892e1f981837dc285c4bf494cd61a。先按 B542 回执还原 B528.555 原包，再安装 B543；12 个已退役开发版路径按既有清单移除，事务标记已清除。实机外观待复验。

### Management capacity institution slots — S1151

B542 实机调配行为正常。Owner 2026-11-25 提出外观修改：连接线伸进城市卡，城市卡拥挤；等级格标题改为该级机构图标和名称，到位回合放在标题右侧；格内列出该级能力及激活状态。Owner 同时确认面向玩家的说法：潜力是内部工作名，玩家看到的是该级机构是否“建立”，激活看容量是否到位。

B543 窗口改用原版宽窗口的满屏宽度（最小 1024）。屏宽 1280 以上时城市卡 300、机构格 204（原版晋升格宽度），较窄时缩到 240 和 174；连接线只画在间隙里。城市卡分四行：区域图标、城名与右上角调配框，“某专业”，“已建立 N 级机构 · 已激活 N 级”，容量状态。机构格标题为机构图标与名称，右侧显示“[回合图标] N 回合”或“确认后撤回”，机构名按右侧宽度截断。格内每项能力右侧显示已激活、未激活或未建立；未建立的格子用原版不可取得外观并调暗图标。能力名直接取自各机构说明文本中的小标题，16 个机构 1～3 项，中英文一致；鼠标提示显示完整机构说明。仍是界面内示例数据。

本地验证（`LOCAL_SIMULATION_PASS`）：专项 5 项通过，使用真实中文机构文本，覆盖四个专业的能力数、各等级状态、到位与撤回提示、标题截断，以及 1512 与 1024 两种屏宽下连接线不与卡片或格子重叠。`CurrentGameplay` 固定 HD 数据库（d483b5f2）42 项通过，记录 `local/refactor/CurrentGameplay-e85c0cd7618f43d7aa0ce6e759a56b90/closure.json`，SHA256 `856bd9be4af0ec8fade47cf6958c2a0c7b1d2ee4ad4a277a5a51de95b2089f9e`，已测源码快照 `aad55d6633a40cbd3380cf7df1dcdb8762b503985f7dc50232dae69ede717f90`。174 份 Lua 编译、25 份 XML 解析、300 个包文件引用检查通过。原生贴图与字宽只能实机确认。

### Management capacity Governor tree installed — S1150

B542.569 / modinfo569 temporary, 301/301 MATCH at 2a39b1b9fda847af7f3547ac831e2985b97763f5dbf7d8233e11e26a91d3a6fb. Receipt B542.569-dd37d33-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 dd37d331405568a3bde02c2ac87a6c1e5655602c。先按 B541 回执还原 B528.555 原包，再安装 B542；12 个已退役开发版路径按既有清单移除，事务标记已清除。实机排版待复验。

### Management capacity Governor tree layout — S1149

Owner 2026-11-25 确认 B541 的层级和底纹正确，要求重做中部并参考市政树、科技树和总督界面。B542 每座城市占一行：左侧城市卡显示区域图标、城名、专业与潜力、当前启用等级，以及外交交易界面的左右箭头调配框（0～4 点）。右侧一至四级用总督晋升格表现，按科技树虚线相连。四种外观分别对应已启用（晋升完成）、已分配待到位（选中并显示到位回合）、未分配，以及潜力未达且未分配（不可取得）。容量到位但潜力不足的等级和确认后撤回的等级另有文字说明。底栏改用总督详情页的装饰与原版主按钮、确认按钮。仍是界面内示例数据，不接入回合或保存。

本地验证（`LOCAL_SIMULATION_PASS`）使用 Python 3.14、Lupa 2.8 的 Lua 5.1。专项 4 项通过，覆盖四种等级状态、到位回合、撤回、潜力未达、额度上限、撤销、确认与关闭复原。`run_refactor.py --stage CurrentGameplay` 使用固定 HD 数据库（SHA256 前缀 d483b5f2）42 项通过，记录 `local/refactor/CurrentGameplay-a9cefce854c44dad87aa4eba8f1de79d/closure.json`，SHA256 `16745ed2ab8a4d749c789e56dd0e9148dbff4b742babfb0c9ce27b28962f2674`，已测源码快照 `583110ca68d43c23e4cf3a4448a7113555f6885c736bf59cfa6fe7135337e367`。174 份 Lua 编译、25 份 XML 解析、300 个包文件引用检查通过。原版贴图状态与排版只能实机确认。

### Management capacity native screen installed — S1148

B541.568 / modinfo568 temporary, 301/301 MATCH at 1ac8ff78dd2b0ee87f8fab59d31229bdb4c4aa45f64159bb29af60a7996b72b5. Receipt B541.568-9c62772-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 9c62772b3d96ee91d67d0e925cec625cdc0fb9c2。实机窗口样式与关闭行为待复验。

### Management capacity preview screen layer — S1147

B540 实机层级通过。快速交易使用原版 ModalScreenWide，奇观提醒复用原版外框但使用自己的背景贴图。B541 使用 ModalScreenWide 及其原版标题和关闭控件，底纹取原版总督页。四项专项 Lua 5.1 检查通过，实机渲染待复验。

### Management capacity native screen installed — S1146

B540.567 / modinfo567 temporary, 301/301 MATCH at 172264a4985511cdfc4746dcc5ac662579f3cb8ca4bc66852c5ee7d51fcc20c5. Receipt B540.567-adc6b64-playtest.json DEVELOP_ACTIVE. Stable B528.555 backup verified. 安装源码 adc6b64637821f39feeb8f4c141681e236b27028。实机层级与关闭行为待复验。

### Management capacity preview screen layer — S1145

B539 实机确认开启面板和顶栏试调更新。用户以总督和世界气候页说明目标层级。B540 将预览挂至原生 Screens 父节点，使用与总督页相同的弹窗队列参数及原生暗幕，内容居中并支持 Esc 和关闭按钮。试调使用独立示例数据，真实回合推进属后续容量实施。四项专项 Lua 5.1 检查通过，含挂载、队列、暗幕、关闭重开、示例数据与包引用。原生层级待复验。

### Management capacity click preview installed — S1144

B539.566 / modinfo566 temporary, 301/301 MATCH at 2d03822eee842e8f5051ecc91e6d98b640c8661430f3be6389345c4629fd068b. Receipt B539.566-9de3f36-playtest.json DEVELOP_ACTIVE. B528.555 backup verified. 安装来源 9de3f36cc3b24b57fdd264b218a3aca32ec9e72a。游戏内点击待复验。
### Management capacity preview panel opening — S1143

B538 实机显示两处入口，点击下排按钮时没有面板。原回调只显示子窗口，挂载时也没有显式显示其原 UI 上下文。B539 挂载和打开时均显式显示该上下文，关闭通过子窗口完成。Lua 5.1 夹具以隐藏父界面复现，覆盖点击及重复开启。实机显示待复验。
### Management capacity preview installed — S1142

开发包 B538.565 / modinfo565 已临时安装。安装包 301 个文件与源码 `b33e7284bb68dfe756e723ae81b2ce4acb446e8b` 一致，SHA256 `46faf4af6eb94d54381266e79316db7e1a9fdc15be27d245cf0471e5239da952`。回执 `B538.565-b33e728-playtest.json` 记录了本次换包、12 个先前已退役的开发版路径及可还原的 B528.555 原包（310 个文件，SHA256 `1722ed6e5e93b4d320345248cb29778c1a108e3fc51b515ad2eff3aef0cb3095`）。事务标记已清除。游戏内显示由负责人接下来核对。

### Management capacity layout preview — S1141

顶端商路名额旁显示示例用量 6/10。下排使用原版启动栏按钮打开专业管理侧栏，四座示例城市允许试调、撤销和确认。徽记暂用原版市政广场图案。调配只存在于界面内存，重载后回到示例。真实容量授点、城市数据、回合和保存均未接入。玩法继续采用当前总督门槛。[设计规则](../Design/Shared.md#开拓者投资与专业管理容量)

运行影响限于受支持玩家的界面。读档界面完成时挂载两个控件，同一界面的重复加载通知不会增加控件，卸载时归还顶栏与启动栏空间。四行固定示例与按钮响应没有城市扫描或持续轮询。

本地验证（`LOCAL_SIMULATION_PASS`）使用 Python 3.14 和 Lupa 2.8 的 Lua 5.1。运行 `python3.14 -B -m unittest discover -s DevelopmentTests -p test_management_capacity_preview.py`，4 项通过，覆盖控件位置、重复挂载、卸载、测试文明范围、试调与双语装配。按现行固定 HD 数据库输入运行 `python3.14 -B DevelopmentTests/run_refactor.py --stage CurrentGameplay`，42 项通过。174 份 Lua 编译、25 份 XML 解析及 301 文件包的清单引用检查通过。实机排版待负责人查看。

完整本地回归记录 `local/refactor/CurrentGameplay-939a9ae40dcd440d97bad570618cf2cf/closure.json`，SHA256 `89e664d42e4b9c1e08f4434730684bf714c01f15b7a75de4586c0b1ab6251701`。已测源码快照 `98671372481c0a1372c20b7ec0c49d77692fba03041c29ab26467314eb9a54f4`。

### Expedition archive city choice — S1138

归档城确认易主后，原主人选中存续的人文考察团，可从行动栏选择新的己方文化城。目的地可以没有总督。旧见闻留在原城，未完成任务结束，下一次任务按新城自己的见闻名额判断。没有合格城市时，保留原团与全国名额。[玩家规则](../Design/Culture.md#来源易主与重新挂靠) · [城市和单位各自的责任](../Architecture/Specialization_v0.1_Architecture.md#已成团的考察团更换归档城)

**运行影响。** 复用已有的交割退出回调和单位存储。确认同一归档城时写一次单位记录。只在玩家打开选择器时遍历本方城市，确认时重读选中的城市与单位。单城读数不可用时提示列表可能不完整。保留现有到达与活动释放协议，旧请求不能代另一支团或替已经易主的城市确认。没有新增引擎监听、轮询、保存字段或玩家付款。

**本地验证。** Python 3.14、Lupa 2.8。运行 `python3.14 -B DevelopmentTests/run_refactor.py --stage CurrentGameplay`，42 项通过。定域套件 183 项通过，与前者有重叠。新加的 9 项以 Lua 5.1 测试真实城市存储交割、同构建冷读、原团身份、无总督与低潜力、未决城市、失效的选择、任务取消与名额、已派遣单位到达及行动栏。原行动栏夹具补载随界面使用的重组助手，任务图标断言对齐已发布的素材，两种 Lua 测试环境各自加载隔离的作品读取器。173 份 Lua 在 5.1 编译通过，24 份 XML 解析通过，298 个包文件的清单引用可解析，新增 7 个文本键均有简体中文与英文。

定域复现时在 `DevelopmentTests` 下运行 `python3.14 -B -m unittest test_expedition_archive test_expedition_spy_actions_ui test_expedition_spy_sidebar_ui test_expedition_training_source_loss test_expedition_missions.Missions test_expedition_spy_binding test_expedition_spy_store test_expedition_spy_recovery_activity test_expedition_spy_auto_open test_expedition_spy_selection_ui test_b414_crew_unit_panel`。外部数据库及依赖配置见[测试环境](../../DevelopmentTests/README.md#environment-and-dependencies)。

本地完整运行记录位于 `local/refactor/CurrentGameplay-3c4aff7191f84a139c6e477df0c5517a/closure.json`，SHA256 `87ceb9af3f9ea1719c35b163ad54fc77b5cede8b51e0d5fbbeb0df7f8763848a`。输入文件摘要为 `160f7438b90a2fbc60e51daf540a3d724d5adb10a14ee8e3fd76aa745bf45fbe`。

**实机范围。** 本地通过（`LOCAL_SIMULATION_PASS`）。归档城交割的原生事件顺序与原版／HD 界面仍待实机。永久毁城的独立证据入口和边境位移沿用现有待办。安装仍为稳定 B528.555。

### B528.555 stable playtest package deployed — S1123

On 2026-11-18 the Owner approved the bilingual README and the promotion of B528.555, then separately authorized stable installation. [PR #9](https://github.com/WrathSK/Specialization-Gameplay-Redesign/pull/9) merged at `0beca3138b58595bfa02749e4f5ba3662736b9e9`. Its parents are prior main `8a6aaa29` and approved head `e82f20bb`. Its tree matches the reviewed head and its Mod files match B528 source `e42caca0`.

**STATIC_CONFIRMED deployment.** With the game closed, the B527 receipt `B527.554-1495cbd-playtest.json` reached `STABLE_RESTORED` before local main advanced. The stable tool then deployed the 310-file B528 package with the 29 reviewed outgoing paths. All installed files match main at SHA256 `1722ed6e5e93b4d320345248cb29778c1a108e3fc51b515ad2eff3aef0cb3095`. Receipt `.SpecializationP0-backup-f1x7zfau.receipt.json` reached `DEPLOYED`. The retained B489 rollback package matches its original 337 files at `fe601208d9fcdc359c3f8b46a017f5caa19b1284f952c9f7b60e986899b6de30`, and the outgoing B527 matches its 314 files. The final check found no pending transaction.

**Playtest scope.** [B489](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047) covers the recorded HD and official Gathering Storm scenarios. The official game used two testing aids. [B527 HD](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b527-hd-great-work-and-cold-load-evidence-reviewed--s1091) covers city-local Great Works and cold loading. The positive [B527 no-HD Culture Network observation](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b527-no-hd-culture-network-and-load-readiness-verified--s1093) used 69 loaded targets. The pinned 28-target B527 cold check, continuation across reload after that positive benefit, and the precise HD Study uplift remain open. The B528 cleanup has 35 recorded local checks and inherits native evidence only in its prior scopes. This release ran no new game test. Supported saves start and reload on the same build.

[历史全文](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md)
