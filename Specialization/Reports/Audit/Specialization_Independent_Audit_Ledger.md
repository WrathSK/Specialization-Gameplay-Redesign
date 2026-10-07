# Specialization 独立长期审计 Ledger

Audit ID: IA20261007；启动日期2026-10-07（America/Vancouver）。
State: USER_STOP_CHECKPOINT；P01与P13a公共hot-path slice覆盖完成；P06a未开始。用户即将合盖，已停止调查扩张。尚无总审计结论。
性质：用户授权的独立审计记录，不是Design Authority、Architecture合同、Status替代品或新开发授权。主任务仅写审计产物，统一维护此ledger；定域只读审阅可并行。severity与refactor timing独立，未确认合法工作集/触发频率时保留条件而不制造必改项。

## 快速恢复与本轮停止点

- 起始develop HEAD：`7de45dddba1f874ae21d2f1335bf911b485f8ab4`，启动时clean且与本地origin/develop一致。
- 当前已登记开发状态：S0444，source/live B168.195；L3-A原生测试由用户暂缓。审计不能把它恢复成必测任务或通过。
- 已完成阶段：**P01：权威／Workflow／Status／当前manifest与证据入口一致性**。这是覆盖完成，不是项目PASS。
- 当前检查点：P01三组独立只读复核已收齐，关键候选由主任务重读/内存反例复核；confirmed/provisional/rejected与实际覆盖已写入。只改本文件，原Authority/Status/Design/Mod保持。
- 上轮停止点：P01覆盖完成并提交437bb3b；既有阅读、证据与finding全部保留。B168实机继续待办。
- 当前窗口W02已完成：按用户方向修正建立公共event→dirty→recompute→publish、hot-path/主要state初版map及有界缓存反例；baseline437bb3b的Mod与P01一致。只查新相关source，不重做P01或局部native gate。
- 本轮停止点：用户要求立即收束；三个本轮子任务均completed，结果已收齐。P13a公共map、confirmed/provisional/timing及准确P06a入口已保存；P06a没有开始。没有重构、新worker、长测或用户测试。
- 下一准确入口：**P06a主要持久/会话state ownership与mutation边界**：`Mod/CityProgressionStore.lua`的StartCollection:630–811、CreateProgressionRecord的root/save/active:100–169，再按实际read/write callers扩展；配合`Architecture/v2/P0_E2_Plan.md`CURRENT/实际保存合同。追查index/envelope/workers/Game slots、pending/receipt、RegisterExit/Return及读回来源；不逐能力重复完整native生命周期。随后P09b验证GW/Network跨Context更新与依赖闭包。
- 原P02a详细入口保留为后续按需合同核对：P02a，先`Design/Content/README.md`确认主从，再完整读取current Spec的SCOPE/ELIG（第1节）、ID/TERMS（第2节）、PROG（第3节）、SHARED（第4节），并读取`Shared_D0045.json`中ORDINARY_INFRASTRUCTURE、BUILDING_CURRENT_ELIGIBILITY、DISTRICT_DEVELOPMENT、YIELD_SHARE及其完整引用。对应`D0032_Adaptation.md`的Canonical state model／Shared facts and services；当前接受增量仅按直接revision/lifecycle引用扩读。Network另作P02b，不凭文件编号判断权威。

路径默认相对于`Specialization/`；`Mod/`、`DevelopmentTests/`、`tools/`相对于仓库根。

恢复时只读：ledger → Git branch/HEAD/dirty diff → Authority及真实CURRENT → 当前阶段指定入口。若HEAD变化，比较其与本检查点的相关文件diff；仅使受影响结论重新待核，不清空已完成审计、不盲目rehash或reset。没有新diff且来源不变时复用已核证据。不因最终聊天报告缺失重复执行部署、测试或提交。

## 审计总范围

覆盖用户A–L，重点是规则／实现／证据一致性及错误、数据与部署风险。包含四专业当前v0.1范围；未来专业只检查接受规则/元数据/边界是否污染当前范围，不把未来功能缺实现当作当前缺陷。

| 用户范围 | 审计问题 | 阶段 |
|---|---|---|
| A Authority/Workflow/Status | 权威、版本、授权、当前切片、状态/证据、selector/hash职责是否一致 | P01、P15 |
| B Accepted Design/Architecture | 合同、接受/取代、资格/数值/成熟度/长期资产是否正确反映 | P02–P04 |
| C Architecture/Mod | 注册、Start、实际writer、正常/测试模式、旧实现退出是否与合同一致 | P05、P08–P11 |
| D Tests | 断言/fixture fidelity、风险闭包、native gap、重复人测及依赖是否合理 | P12及各业务阶段 |
| E Lifecycle/persistence | identity、save/load、owner转移、夺回、Claim、REALLOCATING/未结算事务 | P06、P07、P10、P11 |
| F Carrier/Modifier | 精确ownership、撤销、UNKNOWN、引用/样本失效、原生承载限制 | P08、P09 |
| G Performance | 触发/范围、事实构造、cache/queue/订阅退出、GC与剩余增长证据 | P13 |
| H Deployment | main/develop/stable/test隔离、target/staging/hash/receipt/recovery | P14；P01只核身份 |
| I History/navigation | 冻结证据、迁移映射、旧派工、仍有效反证与主从关系 | P15；P01先查活动入口 |
| J Debt/complexity | 重复实现、防御/兼容层是否有独立职责，过度防御成本 | P16及直接业务阶段 |
| K Accepted gaps | 已接受且当前范围需要、但Architecture/实现仍遗漏；区分有意延期 | P02–P05、P10、P11 |
| L Unsupported completion | 完成/通过宣称能否回溯到实际来源、版本、场景和证据等级 | P01、P12、P17 |

启动时Git跟踪文件盘点（只证明范围数量，**不是已阅读覆盖率**）：Mod186（128Lua/40SQL/15XML/modinfo及ArtDefs）；DevelopmentTests270；Design116；Architecture62；Workflow25；Status315；Reports146；Historical125；tools8。后续按实际注册/依赖划分当前代码、兼容撤销与历史fixture，不能凭文件名Probe/DEV判断地位。

外部游戏/HD/Workshop只在具体native/API/目录/事件问题需要时定域只读，明确加载环境/版本；不扫描整个用户磁盘。截图/存档/日志/DB/backup不复制进Git；未实际重看截图不声称重看。并行Investigation主题原件默认排除，发现问题只记录，不修改或自动发布。

## 2026-10-07方向修正：先查会随扩展放大的返工风险

用户明确调整审计目标，不重启审计、不删除P01。核心问题改为：“继续大量增加能力/第五第六专业前，哪些公共架构与性能方向值得先解决，否则返工面会扩大？”所有阶段ID/既有范围保留，只调顺序和投入深度；不建立平行plan。

当前优先顺序：**P13a公共hot path（结合P05/P09直接依赖）→P06a主要状态ownership/source-of-truth→P09b传播/跨Context→P08a相同语义的effect/lifecycle公共边界→P05b/P16a模块依赖与新专业接入成本→P12a规模风险断言/20–40城代表负载→P13b缓存间接保留/GC职责**。P14部署基础安全按直接风险插入。P02只先读支撑上述判断的Shared/资格/UNKNOWN完整合同；P03/P04/P10/P11逐能力正确性/数值/native深入与P15清理降优先级，除非揭示公共根因。

输出在同一ledger逐步建立：hot-path map（频率×C/B/D/W/R×近似复杂度×保护×worst case）；主要state ownership map（永久/native/derived/cache/carrier/pending/UI/reconstruction）；新增第五/第六专业的复制/中央修改/事件/生命周期成本。地图有明确未覆盖，不用源码数量替代工程证据。已有1/2/4/8城例不足的地方可用有界实际Lua临时fixture核结构成本，不当作原生耗时/分配或泄漏结论；不新建常驻计数器或默认长测。

### 独立维度：refactor timing

severity与timing分别记录，不能互相代替：

- FIX_NOW：已证明继续加功能会扩大公共返工面，明确最小调整范围与未来倍增路径；不是本轮实施授权。
- FIX_BEFORE_NEXT_PROFESSION：当前四专业可继续，新增专业前宜处理公共边界。
- MONITOR：有具体观察/最小区分办法，尚不值得重构。
- DEFER：问题存在但局部、收益低、不随功能扩展显著扩大。
- NO_ACTION：核对后结构/职责合理；只对已核边界，不表示模块整体PASS。

公共化仅在语义、ownership、生命周期确实相同且很可能被新专业继续复制时建议；不为DRY合并不同资产/合同或UNKNOWN职责。共享成熟生命周期不逐能力重验；审其公共合同和扩展成本。每个新finding同时写“现在修改面／扩展后修改面／实际杠杆／证据限制”。

| 已有finding | severity保留 | timing | 判断依据 |
|---|---|---|---|
| IA-P01-F01 | MEDIUM | DEFER | JSON稳定ID保护是局部manifest/tooling修补，不是运行公共状态/传播方向；不因此抢占core审计 |
| IA-P01-F02 | LOW | MONITOR | 部分schema/reference校验缺口目前未误路由；后续按真实工具变更检查，不新增验证平台 |
| IA-P01-F03/F04/F05 | LOW | DEFER | 当前导航文字可局部修补，已有Authority反证；新增能力不会迫使重写大量运行模块 |
| IA-P01-Q01/Q02/Q03/Q04 | 原暂定等级保留 | DEFER | 先保留证据，不继续把主要时间投入局部导航；若影响公共authority再提升 |
| P01 rejected concerns | 已排除解释 | NO_ACTION | 对原核查范围保留反证，不为已排除解释重构/重测 |

## 分阶段审计计划

每轮优先完成一个约25–30分钟的独立slice，预留5–10分钟核证/ledger/提交及中断缓冲；不要求读满40分钟。较大阶段拆成明确子slice，每个有独立入口、检查点和未覆盖项。阶段完成表示**审计覆盖完成**，不自动表示功能PASS。

| 阶段 | 完整slice/主要入口 | 完成条件 | 状态 |
|---|---|---|---|
| P01 | 根/项目AGENTS、README、Workflow/Authority、CURRENT、当前manifest/结果，必要receipt | 权威版本/来源/授权/selector、当前证据分层与源/live事实核对；候选反证检查 | COVERAGE_COMPLETE |
| P02 | 当前Shared Content/Spec、Network合同、Shared目标Architecture | 枚举共同完整规则及例外、取代关系、技术合同对应和真正TBD；大阶段按Shared/Network拆slice | NOT_YET_AUDITED |
| P03 | Research_D0040、Industry_D0045及对应Spec/当前计划 | Research与Industry分别完成rule→合同矩阵，数值/门槛/长期资产/首测区别不遗漏 | NOT_YET_AUDITED |
| P04 | Culture_D0048、Commerce_D0045及生命周期接受记录/计划 | Culture与Commerce分别完成矩阵；排除旧能力混入、未決条款伪定案 | NOT_YET_AUDITED |
| P05 | modinfo、Gameplay/include/Start、SQL注册、writer切换矩阵 | W02核direct公共dispatch/14RuntimeWork caller；全Mod可达/依赖分类未完成 | PARTIAL_W02 |
| P06 | CityProgressionStore、E2 current合同、CityFlow/identity/Evidence/helper及定向测试 | identity/initialize/held/recapture/claim/load及损坏/UNKNOWN真实状态与写入边界闭合 | NOT_YET_AUDITED |
| P07 | InvestmentAction、单位/项目action、待结算/REALLOCATING生命周期合同 | receipt/重复/中断/Owner变化/出入系统的每类事务核对，不套统一永久语义 | NOT_YET_AUDITED |
| P08 | 各module owned lists、SQL Modifier/requirements、载体创建/退出direct callers | 清单ownership、旧writer退出、remove失败/重入/stale reference/未知与原生边界闭合 | NOT_YET_AUDITED |
| P09 | NetworkInput/Bridge/BackgroundRoutes/Sender及消费者 | W02核公共路由/版本/成本map；完整跨Context/GW/native语义闭包未完成 | PARTIAL_W02 |
| P10 | ResearchSupport/Cross/Apply/Tradition、Standardization/Construction/Industry | Research、Industry各一slice：效果/模板/奇观/历史/队源绑定与Design/证据对应 | NOT_YET_AUDITED |
| P11 | Culture facts/Aesthetic/Meaning/Inspire/旧Dialogue、Commerce现行/旧consumer | Culture、Commerce各一slice：当前/待接入/试验边界、长期记录/合同/hidden protection对应 | NOT_YET_AUDITED |
| P12 | Tests README/Catalog、每条当前路径实际测试源码/fixture与Validation结果 | 风险→断言→local/native证据矩阵；只为缺口选定必要复现，不机械跑全部历史 | NOT_YET_AUDITED |
| P13 | RuntimeWork/Performance/MemoryGC/public fact/dirty路径及结项限制 | P13a公共hot-path/规模成本已核，P13b再查完整间接保留与GC；不重开已收束长测 | P13a_COVERAGE_COMPLETE / P13b_NOT_YET_AUDITED |
| P14 | tools/deploy/temporary_playtest、Playtest合同、main/develop/receipt/recovery | target/路径/UUID/staging/中断/恢复/授权机制及必要临时目录测试核对；不实际部署 | NOT_YET_AUDITED |
| P15 | Historical/Design目录、legacy mapping、当前索引/真实脚本路径引用 | 活动与冻结角色、重要反证可达、旧派工/断链/路径迁移是否误导；不改历史 | NOT_YET_AUDITED |
| P16 | P05依赖/可达图与前述发现、废弃模块/防御/兼容层 | 有证据地区分独立安全职责与重复复杂度，列具体债务/成本而不猜性能 | NOT_YET_AUDITED |
| P17 | 全部已核矩阵与findings | 交叉验证严重问题、去重、优先级/真实阻塞、覆盖与剩余native限制；此时才形成总报告 | NOT_YET_AUDITED |

## 审计执行纪律：全生命周期 audit-only（2026-10-07用户澄清）

**audit authorization ≠ implementation authorization。** 从本次澄清到最终独立审计报告完成，项目本体始终只读。完整流程为“调查 → 记录 → 复现 → 分析 → 汇总 → 最终审计报告”；审计结束也不自动进入修复，须由用户另行决定并授权。

- **允许写入**：`Reports/Audit/` 下的现有ledger、阶段报告、finding、dependency/ownership/hot-path map、证明finding所需的最小reproduction script、raw result/evidence，以及必要的审计索引/元数据。复现使用隔离fixture与审计/临时输出，不借复现改正式实现、测试断言、配置或运行数据。审计产物可按既有流程审阅、普通commit/push；只显式提交本轮审计文件，保留其它任务改动。
- **始终只读**：`Mod/`、`Design/`、正式`Architecture/`、`Status/`、`Workflow/Authority`及相关权威索引、当前manifests、正式`DevelopmentTests/`及断言、deploy/runtime implementation、main/develop玩法源码、外部运行包、游戏目录、正式配置、frozen historical evidence。不得因审计发现而修改这些内容，也不得为审计PASS补hash、改规则、调GC、部署或重构。
- **严重finding不触发自动修复**：即使为CRITICAL、HIGH或`FIX_NOW`，也只记录finding、证据与证据强度、影响面、独立的severity/refactor timing、建议的refactor boundary/candidate solution，以及未来修复所需验证。timing表示建议处理时机，不是当前实施许可。既有finding正文与已完成阶段结论保持原样；上述要求用于后续发现与审计汇总，不追改原证据。
- **继续与停止**：在有效前提下可自主完成既定logical slice；缺陷本身不要求停审。只有继续调查会因基础前提已经失效而产生错误结论时，才停止受影响审计并说明失效前提、影响范围与待用户决定事项。用户明确暂停/停止的指令仍优先。
- **可恢复交付**：每个slice完成后更新同一ledger的实际阅读、发现、未覆盖范围与准确续接点，验证并commit/push审计产物；不另建平行plan，不推进玩法。此次仅补充执行纪律，保持`USER_STOP_CHECKPOINT`、P01/P13a已完成覆盖与P06a未开始的停止位置。

## 高强度审查与证据规则

- 不以既有报告、测试数量、防御代码或hash相等为正确性结论；从权威完整合同、实际source、具体断言及原生场景交叉核对。主任务亦曾维护此源码，本审计采用独立只读复核与反证检查；不宣称外部机构审计。
- 每条发现记录：ID、confirmed/provisional、severity、事实/影响、文件/行/版本、证据强度、反证/限制、待解问题和下一定域动作。重复描述归并到同一ID，不为了数量拆分。
- severity：CRITICAL（错误玩法/数据污染/损坏/部署风险）；HIGH（实质架构/lifecycle风险）；MEDIUM（明显实现/验证缺口/技术债）；LOW（维护/命名/文档）；OBSERVATION（不足以构成缺陷）。严重性须有证据和真实影响。
- STATIC_CONFIRMED只证明所读文件/数据库；只读工具的HASH/SCHEMA结果只证明相应机械事实；LOCAL_SIMULATION只证明真实断言及fixture范围；USER_REPORTED与实际截图/日志重检分开。不能把local/runtime equality当native PASS。
- 没看到问题写“所查范围未发现具体冲突”，其它区域NOT_YET_AUDITED。既有成熟生命周期证据仅按相同source/path/ownership范围继承；新增风险才提出最小native建议，本轮不要求用户恢复B168测试。
- 可执行既有只读context/文档/完整性检查；后续必要本地复现使用临时fixture，并记录能证明的范围。无默认历史全回归/stress/新用户长测、部署或游戏启动。
- 审计不能补Design、修code/断言、重写冻结结果、调整GC、强制promotion或自动推进下一玩法批次。发现需要修复只列建议及依赖影响；genuine语义问题留用户决定。

## 已完成阶段与本轮实际证据

### P01 — 权威链、当前任务与证据入口（覆盖完成）

日期2026-10-07；被审计baseline为`7de45dddba1f874ae21d2f1335bf911b485f8ab4`。主任务分配三组**独立只读**审阅（权威/工具保护、导航、source/live与证据），统一要求severity/反证/实际阅读记录，主任务重读关键位置并独立执行F01/F02内存反例。没有把子任务“未见问题”当作全项目PASS；没有修复发现。

**核实的事实（限定范围）：**

- root/project AGENTS与Workflow明确用户最终语义权威，Codex获授权记录/实施；读取范围、正常Git、W0004分级、native delta/继承及W0003安全边界没有在本轮变更。
- 当前Authority、活动P0-L3A、Status CURRENT、L3当前切片、Backlog均一致表达S0444／B168.195、39项**原记录的本地结果**与native未验／用户暂缓。没有在本轮重新执行39项，也没有恢复必测要求；自选多档读档仅补充。
- 全部13个Authority path存在；各专业独立revision pin与对应Content元数据相符，不是所有文件强制同号。当前所选JSON实际为`CUL_L4_INSPIRE`。
- 只读`context.py check P0-L3A`返回机械检查PASS：186个Mod文件及469个guarded文件、当前selector／版本检查。`self-test`返回15类检查PASS、0文件写入/0gameplay tests。另运行现有`DevelopmentTests/test_context_helper.py`，3方法PASS（临时fixture/工具检查）；不修改断言。**它们不证明Gameplay、完整schema、真实依赖闭包、接受证据本身或native行为正确。**F01/F02说明两项实际保护缺口。
- 初始main HEAD `e901a224faae1274563fae07012116543bee6759`，main/develop均clean，各自本地remote-tracking refs ahead/behind0/0；审计前未fetch，不称远端当时实时同一状态。
- develop工作Mod、baseline HEAD的Mod、部署source `c3de1140ea4504d8fe4d247211b8af5a4527975e`的Mod、配置指向的外部runtime四者**逐文件相同，186文件／modinfo195**。digest `cdeff00ccb7614905240ed844b238e2ba97df508ab3d62a0898b5b04d55d6739`。这是部署目录完整性，不证明引擎当前加载或原生结算。
- 仅读取精确`B168.195-c3de114-playtest.json`：phase DEVELOP_ACTIVE，target/root/commit/hash与配置及Authority相符，pending marker不存在。main包115文件／modinfo96，digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`，与receipt的stable元数据相符。没有扫描/核验恢复包内容或执行恢复，因此其今天可恢复性仍NOT_YET_AUDITED。
- B166结果明确USER_REPORTED/NO_SCREENSHOTS与七域五产出限定；B167保留全国率/跨回合混杂、0.6缺证及END缺证；B168区分参数、实例、有效总倍率与native入账。没有本轮重看截图、检查游戏进程、重跑玩法模拟或写外部DB。
- 8个活动导航文档的321条本地链接/锚点静态检查未发现具体断链。范围见读取表；没有检查全历史、远端链接、所有阅读版内部交叉引用或实际GitHub渲染。

### 本轮实际读取范围

“全文”仅在确实未截断读取时使用；结构/字节读取不等于语义审计。三组审阅去重后记录如下。

| 文件/范围 | 阅读深度及目的 |
|---|---|
| 仓库根`AGENTS.md`、`README.md`；`Specialization/AGENTS.md`、`README.md` | 全文；路由、语义与工程责任、范围、Git/并行约束 |
| `Workflow/README.md` | 全文（独立审阅）；主任务重点启动/恢复/W0004/证据继承/schema合同 |
| `Workflow/Authority.json`、`P0-L3A.json`、`Batch.schema.json` | 全文/结构；当前任务、版本、授权/延期、引用及实际declared schema |
| `Workflow/context.py`、根`DevelopmentTests/test_context_helper.py` | 全文（工具审阅）；主任务重读context.py:34–127及实际内存反例。只审工具，不审玩法测试 |
| `Design/Content/Shared_D0045.json`与current Spec／Adaptation标题 | 为准确P02入口仅核top-level/concept keys、直接authority_ref及节标题；不是Shared语义已审 |
| `Workflow/Context_Lock.json`、`Runtime_Index.json` | 全项结构/字节/hash检查；只读首部/current provenance与相关条目。长历史review_basis截断处不声称全文语义核对 |
| `Status/Specialization_P0_Status.md` | metadata/CURRENT及S0444–S0435直接证据段；不通读历史阶段 |
| `Status/Playtest_Backlog.md` | B168延期段:177–185；根表角色/旧材料标题仅定位，未审全部旧条目 |
| `Architecture/v2/P0_L3_Inspiration.md`、`Workflow`当前manifest引用 | 全文（导航审阅）及当前/B168/B167合同重点；未以本批gate等同正式能力实现 |
| `Status/Validation/Results/Specialization_B168_Inspiration_Diagnostics_Local.md`、`Specialization_B167_Inspiration_Native_Feedback.md`、`Specialization_B166_Meaning_Automatic_User_Pass.md` | 全文；证据等级/范围/原始反证/人报/optional流程。未重看图片、未重跑对应玩法测试 |
| `Design/README.md`、`Design/Content/README.md` | 全文；当前正式入口与阅读版/结构化来源职责；不等于审全部Design |
| `Design/Specialization_v0.1_Design_Spec.md` | metadata:1–12及直接SCOPE/ELIG前段；其余正文NOT_YET_AUDITED |
| Authority所指Research/Industry/Culture/Commerce/Shared/Military/Harbor/Government Content | 元数据/结构；Culture能力:250–263核对身份。完整机制/所有合同留P02–P04 |
| `Historical/Design/Records/Culture_Era_Presentation_D0032.md` | metadata:1–18；未审冻结正文 |
| `Architecture/README.md`、`Architecture/v2/README.md` | 全文；当前合同/计划/历史导航职责 |
| `Architecture/Specialization_v0.1_Architecture.md` | metadata/CURRENT/系统说明/约束:1–117；历史标题/摘要:118–195仅显示定位，未展开旧阶段 |
| `Architecture/v2/P0_F_Research_Tradition.md` | :1–9、103–123；解决“计划待授权”与已接受F2范围冲突，未审其全部机制 |
| `Architecture/v2/P0_L2_Meaning.md` | :1–30；当前B166范围、旧writer退役与下一L3状态 |
| `Reports/Technical/README.md` | 全文；证据地位及stale dispatch/nav候选 |
| `Reports/Technical/Specialization_B129_Event_Memory_Investigation.md` | 标题定位与:959–988结项/重开条件；未重读全性能历史或图片 |
| 根`Mod/Gameplay.lua`、`Mod/GreatWorkAdjacency.lua`、`Mod/Probe.lua`、`Mod/SpecializationP0.modinfo` | exact retired启动/guard搜索及版本/注册metadata；Mod186文件只做字节盘点，未语义审计全Mod |
| `Architecture/Playtest_Workflow.md` | 全文（source/live审阅），主任务:18–61反证复核 |
| 根`DevelopmentTests/README.md` | 主任务读取当前选择与依赖/历史职责说明；没有运行全测试 |
| 根`tools/README.md`、`tools/deploy.py` | 配置说明及snapshot只读路径。事务/安全实现完整性留P14 |
| main本机配置与精确B168 receipt | 仅runtime_dir字段、精确receipt/marker及目标目录只读；不在ledger公开个人路径或认证材料，不审其它配置/备份 |
| Git working tree/branch/localtracking与两个Mod commit blobs | 路由、身份、字节差异核对；不fetch/merge/rebase或部署 |

### 执行的检查及限制

- `git status / rev-parse / worktree list / rev-list`；sourcecommit→HEAD的`Mod`diff；read-only Git blobs与`deploy.snapshot`逐文件比较。
- `PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Workflow/context.py check P0-L3A`与`self-test P0-L3A`；不更新任何hash。
- 主任务运行现有helper定向3方法，PASS；只用临时fixture，不跑玩法regression/stress、不改真实Design/状态/代码。
- 内存反例：显式正确expected_id可投影、错误ID抛`stable ID mismatch`；仅在传给实际helper的manifest内存副本将batch改整数23或goal_reference改不存在路径，实际check仍PASS。持久manifest/Content/锁完全未改；不是伪造当前仓库错误。
- 321条活动导航相对链接/锚点检查、首部/selector边界检查。只读工具成功记作对应机械事实，不给整体功能打PASS。

## W02 / P13a — 公共更新与扩展性能（覆盖完成）

日期2026-10-07；读审baseline437bb3b，仅审计ledger是dirty。原P01及其five findings保留。此slice覆盖公共路径/主要state初版/未来接入成本，**不是P05/P06/P08/P09/P13全部审计完成**。三个独立只读子审阅分别核RuntimeWork/GPP、Network、Shared facts；主任务重读关键分发、cache/normal-diagnostic、callback与来源路径，并独立重跑实际Lua缓存反例。

### 优先判断（可供审核，不是实施授权）

当前最值得在新增专业前处理的公共方向：**正常事实与诊断采集分离＋D缓存工作集策略；声明事件原因/范围/依赖并复用同一可靠输入；GW通知从隐式callback链改为明确多消费者契约**。主要是下面F02–F04，MEDIUM / FIX_BEFORE_NEXT_PROFESSION；F01为已复现但当前可达工作集待核的MONITOR项。含义是当前四专业可继续；新增消费者应避免复制这些模式，正式公共改动另由用户审核。没有仅因未测native时延就忽略结构证据，也没有为了给出FIX_NOW而声称已有数据故障。

本slice尚无足够依据将某项指定为必须立即打断所有功能的FIX_NOW；下一P06a可能改变优先级。Network扩展角色散落与接口容量另列Q02/Q04，在具体新专业接入前必须核对，但不同专业的source/center/receiver语义不能强行DRY。

### Hot-path map

符号：C=本轮访问的参与玩家城市，C_all=保守全范围时世界城市；B_loaded=全部加载Building定义（含carrier）；D_total=本轮区域总数；W_total=合格/排除作品总数；R=商路；N=相关消费者；K_i=消费者精确自有carrier数；F=一次有界当前事实验证/复制；C_D=该窗口实际调用D的不同city工作集（不等于全C，受ACTIVE/作品等资格限制）；S=缓存完整detail大小；U=每条分发路线展开的直连source次数之和；E_net=去重后的recipient–source对。单次native getter的耗时/分配未知。

| 调用/频率 | 已核成本/增长 | 已有保护 | 20–40城/burst worst case与限制 |
|---|---|---|---|
| UI GPP Publish/Playback/SystemUpdateUI→flush | clean为O(1)；dirty一个跨Context通知，不传worker/facts全包 | dirty/busy、版本/ready/player、同步新原因留下一batch、最多3次抛错发送、Shutdown解绑 | 不能把每帧pulse次数当全城Audit次数。源码`UI/GPPRefresh:31–49,54–80` |
| native worker/focus→RuntimeWork.Hook→各Audit；再收到pure-worker UI补偿 | 此已核slice直接6个扫描consumer＋UI5个：条件下11C城市访问/约11C Facts；每模块自己的batch只共享内部事实/区域 | player scope、internal building过滤、独立turn marker、同回合真实变化保留；Lv4Percent为空兼容Audit，不计扫描 | 两条路径均实际执行时C20/40为220/440访问，burst乘实际事件/flush数。**未证明引擎每次一定双投递，也未证明第二路径无用**。`Gameplay:453–468`／RuntimeWork:33–55 |
| RuntimeWork.New每次同步Audit | 每模块约O(C×F+D_total+相关edges)，Facts每城1、District索引每player1、Live每(pid,industry)1 | 完整枚举成功后发布、Audit结束释放、不跨写入/event共享 | 消除了模块内典型C×D重复；仍不是跨N模块的共享更新snapshot。`RuntimeWork:3–26` |
| 一次GPP正常Audit | C×32稳定owned-carrier prechecks＋F/D；Δ改变另2Δ读/Δ写 | 完整preflight、UNKNOWN hold、精确remove-before-add、无变化零写 | C20/40单Audit为640/1280检查，非毫秒/分配量。32不是可再次机械砍半的“冗余”；`Lv2GPP:39–87` |
| Shared D cache miss/hit | miss遍历B_loaded＋当前districts/存在建筑排序、比较/全量clone；hit也clone完整S | 引用/owner/token/turn、dirty、load epoch；当前LRU cap8；失败标暂不可用保留同ref值 | C_D>8且相同顺序模块轮巡可使后续全部miss，见actual Lua复现。最坏近似N×C_D×(B_loaded+D+S)，不是全20城必触发；`DistrictCompleteness:63–149` |
| UI GW collector/packet | dirty仍遍历C＋当前缓存作品格式化W_total；slot采集仅workDirty/newref城市。local turn设allWorks，collector每城遍历全部B_loaded | city-slot缓存/current-ref、dirty范围、epoch/generation、一个pending、有限重试、seen city prune、Shutdown | fallback本地每turn约C×B_loaded+W_total；不等于每帧扫描。已缓存城市也做每城EffectiveFacts与整包字符串。`DialogueRefresh:48–96,103–164`／`GreatWorkFacts:30–50` |
| UI Routes pulses→dirty collect/sender | clean为O(1)；dirty约C+RlogR；sender parse/encodeR | 局部unit/turn过滤、dirty/单flight/duplicate、失败有界；无周期全scan timer | 采集cap512城/4096raw行；transportcap128条/16384payload字节。实机达到边界未知；`BackgroundRoutes:43–80,157–209`／`NetworkSender:15–44` |
| Network.Refresh→Capture | 每次授权Refresh约C×F+R引用/单位/战争核验＋C/R排序；签名相等只阻止**后续**derive/pub | busy、旧ref/UNKNOWN区分、candidate/current最多各1；有diff才发布 | 相同facts的频繁本玩家事件仍重复C确认；UnitRemoved等全scope evidence事件会触发。不可凭未知已删unit直接过滤。`NetworkBridge:125–169,407–429`／`NetworkInput:20–66` |
| Network derive→publish→5consumer通知 | O(C+R+U+E_net)＋值副本；U≤R×sources但是真实拓扑展开 | private完整view、input/epoch/signature guard；每consumer pcall；Current*不Capture | 不把真实多来源edges笼统记O(C²)扫描错误。新增消费者没有自动接入；`NetworkBridge:24–82,239–307` |
| 当前源/存在preflight中的报告构造 | Apply/Chair amounts表，Infrastructure oldCount/coefficient；Commerce bits/tostring/concat正常apply不使用 | 模块拥有读写/验收职责；保留native验证 | 成本确实存在但数量低，只LOW/DEFER；不以微优化替代公共方向。源行见F05 |
| 明确诊断/手动Network.Read | 当前健康无candidate条件：2次C Capture＋约7个R遍历及格式化 | 仅显式读取；正常Current接口不走此分支 | 低频可局部减量，DEFER。`NetworkBridge:278–280,333–342`，不是normal hotpath |

carrier量推导的条件核查：前五个normal模块一轮稳定`C×(32+11+52+25+8T)=C×(120+8T)`；Commerce直接native round另96C。native＋一次pure-worker UI均执行时总`C×(336+16T)`。Chair source候选T≤13、实际加载T未读取；T13时20/40城上界10880/21760次稳定carrier presence检查，不含其它模块/变化后验证。**这是源码条件计数，不是所有20城存档都如此，也不是耗时/heap测量**。真实业务Δ写与native late-facts补偿不能删。

### 有界实际Lua复现：D工作集从8到9的边界

证据：LOCAL_STRUCTURAL_REPRODUCTION。使用未改`DistrictCompleteness.lua`（SHA256 `cdbf2c9be2213b01f7483df4d149ff9c598671ab66a8b45178d25f5654e2e03c`）及`test_p0_a.py`的runtime fixture，**仅AST提取imports/functions及R/M/NEW/FIX常量，不执行旧顶层测试**。每城市1Campus＋Library、D1、fixture B=120、同turn1/owner0/ref，按1…C遍历三次，无dirty/写入。主任务独立重跑结果相同。

| C | 三次累计capture | 三次累计HasBuilding | 三次累计cache hits | 结果 |
|---:|---|---|---|---|
| 8 | 8 / 8 / 8 | 960 / 960 / 960 | 0 / 8 / 16 | 第2/3次全部hit |
| 9 | 9 / 18 / 27 | 1080 / 2160 / 3240 | 0 / 0 / 0 | 第2/3次全部重新采集 |
| 20 | 20 / 40 / 60 | 2400 / 4800 / 7200 | 0 / 0 / 0 | 同上 |
| 40 | 40 / 80 / 120 | 4800 / 9600 / 14400 | 0 / 0 / 0 | 同上 |

所有Read保持VERIFIED/READY、D1，cache≤8，writes0；HasBuilding由临时mock原生getter计数，clone内部未instrument（NOT_AVAILABLE）。120是fixture定义数，**实际游戏B_loaded UNKNOWN**；项目外部DB没有SPC_DEBUG_GAMEPLAY_DB/当前develop配置，分类计数NOT_RUN，不猜路径。没有新常驻counter或native测试。**当前正常caller有ACTIVE门槛（Housing2、Aesthetic3、Apply3、Infrastructure/Chair/Meaning4）；总督等可能约束合法C_D。未核当前加载Governor数量/全部资格可达性，不能用帝国20城直接推定有20个正常D工作集；这不是当前卡顿复现。**

复核配方：在临时脚本AST选择上述fixture定义，`runtime()`每个C建立独立Lua；`newCity(i)`＋`addDistrict(...,'DISTRICT_CAMPUS')`＋`setBuildings(...,{'BUILDING_LIBRARY'})`；临时包装GetBuildings().HasBuilding计数；清counters后，3×循环调用实际`svc.Read(0,city,city.token)`，断言每view D1/READY、turn不变/writes0。读取现有dc_capture/dc_hit/CacheSize即可，不镜像LRU算法。历史test_research_apply:45–50只覆盖1/2/4/8，并明确facts=2C，无法覆盖此边界。

**持久复现证据（已保存，原/tmp不再是恢复依赖）：**

- [复现脚本](Evidence/W02/district_cache_reproduction.py)，SHA256 `3cb816b6e2288984c77156cb98515e7c22c5cd08cce8bc96ed1dea0d5237647c`。由原临时脚本归档，仅将repo root改为相对位置，并去除本次未运行的可选DB分类尾段；实际Lua/fixture/core三轮逻辑保持。只做AST语法检查，归档改写后没有再启动测试。
- [主任务独立复跑的原始结果](Evidence/W02/district_cache_result.json)，SHA256 `e4e555aeca57759e55797a5a8702ee103a60c1b5249d1e5ca2237b08c40eece4`；从已取得JSON原字节保存并校验。原结果中的UNAVAILABLE_CONFIG只是当时可选分类缺配置，缓存复现本身完成；120仍fixture数。
- 原临时脚本SHA256 `4c49ccbd37480d1874553666968ab6ded88d8e30c123f0cbad984d9f2b9ae0f8`仅用于原执行来源追溯。依赖Python/Lupa lua55，现有fixture/actual Mod；没有复制外部DB/配置或加入新测试平台。

用户2026-10-07合盖stop要求到达时，不再扩张范围。以上保存只涉及已完成证据归档，没有开始新调查、代码路径或重构。

### 主要state ownership map（初版，完整P06a待续）

| state类别 | owner/source of truth | mirror/cache与失效 | 当前已核界限 |
|---|---|---|---|
| Identity/Potential/investment/已存历史 | CityProgressionStore的index/逐city record + Game saved slots；现代positions→worker定位 | worker/envelope是运行镜像；Base/Investment返回copy，active验证当前ref | 只核getters与定位/接口，不证明save事务/所有永久资产语义。现代find为O(1)表查，不是每读全国district。Store:649,794–811 |
| native/current资格 | P.GovernorGate读取6个current scalar properties＋owner/id；EffectiveFacts组合保存foundation和≤3投资 | 每次fresh、未知/不一致不当ACTIVE0；CurrentSpecializationFacts只是facade | 与永久ACTIVE分离；是否可安全共享snapshot需定义真实mutation边界，不能缓存过期Governor。Probe:314–341／EffectiveFacts:13–57 |
| Shared普通建筑/D | DistrictCompleteness owner；Catalog为本session静态定义 | cap8完整detail cache，ref/dirty/turn/load；复制结果不外泄可变cache | 架构方向合理但有F01/F02规模问题；不是缓存全局永久D |
| accepted route/input | UI BackgroundRoutes只供shadow当前事实；Gameplay NetworkBridge验证并拥有accepted input | seq/epoch/route refs/candidate/版本；UNKNOWN同ref保持、确认失效撤销 | 只核公共分层和门禁，未做全部native事件路径验收 |
| derived topology | NetworkBridge private views[pid] | 一份完整view/玩家、key=epoch/inputVersion/signature；compat b.sources/centers/recipients为copy | 当前不按历史version累积；public b.players/input边界及全alias闭包P06a/P09b再查 |
| batch facts/districts | RuntimeWork.New创建模块一次同步Audit上下文 | Facts/District/Live一次批内；Audit退出释放 | 不跨写入或下一事件共享，也不是国家级统一facts owner |
| current GW事实/汇总 | GreatWorkFacts Gameplay验证并拥有cities/index；UI collector只供slot事实 | epoch/ref/catalog/confirmed subset；Summary标量，Read完整copy | normalMeaning用count不每件重算；OnConfirmed单链有F04隐式顺序，collector全B成本见F02 |
| per-ability projection/carrier | 各writer自己的records/owned IDs；native实例为当前效果 | load/confirmed loss通过具名出口重新派生；UNKNOWN保护各自拥有 | 只核代表性API，不统一不同资产／所有per-module lifecycle；owned ID列表不是saved authority |
| pending/token/ACK | producer/sender/Gameplay bridge各自持1flight/candidate，引用/epoch绑定 | 完成/确认拒绝/超时/隔离/Shutdown释放或替换 | 所查GPP/routes/GW非无界队列；没有按重试历史累积列表 |
| UI/diagnostic | P0/专门readout仅呈现，不能反推永久state；Network detailPage为诊断cursor | report按需；detailPage历史clicked key未见prune | cursor风险MONITOR，未认定大内存来源；其它UI mirrors未完整覆盖 |
| GC/session测量 | 合同指明PerformanceCounters单入口owner，不是state清理owner | 已部署开关/阈值/锁停/加载保护保持 | 本slice没完整读StartMemory/间接保留或执行GC；P13b NOT_YET_AUDITED，稳定化结项不重开 |

### 新专业接入的当前修改面（有限直接图）

新增一个有当前事实、derived carrier与网络/作品依赖的专业，当前要同时面对：

1. `EffectiveFacts.lua:5,24`与`NetworkInput.lua:45–46`的四专业白名单；CityProgressionStore和first-domain/资格校验还需P06a/P05b完整搜闭包，**当前未数完所有if/switch**。
2. Gameplay正常action成功后的多个手工fan-out：unit action:426–443、investment:501–519、GPP dirty:453–468，以及include/Start/registration。它们不都属于同一种事件/数据语义，不能盲目用一条通用Audit取代。
3. 各writer复制 native hook列表、fallback、pending/busy、owned preflight/withdraw；RuntimeWork可复用player/batch粒度，但未提供city scope/依赖发布契约。相同primitive可公共化，业务formula/不同资产历史仍保留专业owner。
4. 若参与现有共同网络：NetworkBridge source/center:244–247、national:31、display kinds:323、notify名单:59及NetworkInput signature:12分别明确角色。不能给Harbor等未来专业自动加独立Network Ability或把所有kind都加入所有role。
5. 若消费GW确认：目前必须知道Aesthetic/Meaning startup顺序、保存previous并包装OnConfirmed；不是简单订阅一个稳定多消费者API。

上述给出了未来扩张需触碰的实际位置，不代表已证明需要全仓重构。优先在下一接入前明确稳定source/ownership/变化原因/范围/依赖和退出接口；保持独立模块职责，避免新增“共享层”又复制一套状态权威。

### 本slice实际阅读与检查

全文：RuntimeWork、EffectiveFacts、CurrentSpecializationFacts、DistrictCompleteness、NetworkInput/Bridge/Sender、UI GPPRefresh/BackgroundRoutes/ShadowRouteState/DialogueRefresh（主任务），以及direct shared facts/consumer源码的定域结构。14个RuntimeWork real callers均定位currentStart与实际Audit/hook，不按Probe文件名/历史Start误计；只读上述相关函数，不逐个重验完整ability/save-load。

精确函数：Gameplay正常分发/Start:417–525,675–822；Probe GovernorGate:314–341、Create/Remove/SetProperty:551–564；CityFlow SupportFacts:126–135；Store active/projected:138–159、现代check/find/getters:649,794–851；GreatWorkFacts Collector:30–50、Receive/OnConfirmed:149–169及Summary/Read；Aesthetic/Meaning callback及其Audit/records；Catalog Build/归类numeric entry:232–255；ResearchCrossSample inventory/静态DistrictReplaces来源；Research Apply/Chair/Infrastructure installed与正常reconcile；Commerce observed/apply。

合同/断言只读：主Architecture:77–103、D2公共batch/dispatch合同；test_b138_update_contract:67–230（含foreign UNKNOWN补撤销）、b135_scope:41–88,129–164、b133_redundant_reads:39–62；test_research_apply:45–53；网络D2/B/B069/b134相关scope/query/epoch断言。没有执行这些历史stress/旧套件，没有改断言。性能报告只读B138:809–844、结项:974–986；不重读全部截图/历史，也不把统计猜成每Mod独占。

执行：4个C×3sweep实际Lua临时结构复现，主任务独立重跑；当前context/hash检查。外部DB分类NOT_RUN（缺当前配置），无native/GC/部署/游戏操作。实际getter耗时、原生事件双投递率、分配体积/间接Lua堆、20–40城真实世界负载仍UNKNOWN。

## Confirmed findings

### IA-P01-F01 — MEDIUM：当前能力选择器缺少声明中的稳定ID保护

Refactor timing: **DEFER**。时机依据见方向修正表，原severity/证据/反证保留。

证据强度：STATIC_CONFIRMED＋实际helper内存反例。`Workflow/P0-L3A.json:49–52`宣称“verify stable id”，但只有`/abilities/4`而无`expected_id`；`Workflow/context.py:65–69`仅在提供字段时校验，`Workflow/README.md:187`定义JSON Pointer＋stable expected ID。当前实际选中的`Culture_D0048.json:256`确为CUL_L4_INSPIRE，**没有当前错选或错误玩法证据**。

影响：未来数组重排且完成review/hash同步后，数字位置没有独立保护“所读仍是同一能力”。这是明确自动校验缺口，不是现有授权失守。反证：hash未同步时仍会报差异，人工完整对象读取仍应核ID。最小建议（本轮不修）：为这项JSON引用补真实expected_id并定向验证，不改玩法或schema系统。其它活动manifest是否同类缺口留后续，不从单项推广。

### IA-P01-F02 — LOW：helper执行部分schema/reference检查

Refactor timing: **MONITOR**。时机依据见方向修正表，原severity/证据/反证保留。

证据强度：STATIC_CONFIRMED＋实际helper内存反例。`Workflow/Batch.schema.json:24–25`要求batch字符串；`Workflow/context.py:76–87`只检查部分字段／枚举／reference投影，内存batch=23仍由check返回PASS。不存在的goal_reference也不被validate_manifest/check覆盖。

影响：机械PASS不能被称为完整schema与全部引用校验；后续畸形但已review/锁同步的manifest可能绕过类型/goal导航检查。当前持久化manifest类型与目标均正确，lock存在，工具始终返回implementation_authorized=false；没有证明runtime风险。`Workflow/README.md:189`也限定“supported schema fields”，因此不是所有schema都曾被承诺验证。建议将检查能力准确说明或补最小类型/goal引用校验；不引入新验证平台。本轮不改工具。

### IA-P01-F03 — LOW：Design入口的当前修订导航已过时

Refactor timing: **DEFER**。时机依据见方向修正表，原severity/证据/反证保留。

证据强度：STATIC_CONFIRMED。`Design/README.md:59`仍写当前SpecD0047、CultureD0046，实际`Design Spec:5,11`、Authority design/culture pin及`Content/README.md:14,20`均为D0048。

影响：新读者可能漏掉D0048主题化暂行接受／Balance范围。反证：同页专业摘要已提到主题化，正式来源链接仍正确；未发现其因此形成另一套玩法权威。建议后续只修当前修订导航，不改accepted正文。本轮保留原件。

### IA-P01-F04 — LOW：科研传统当前技术索引仍标待授权

Refactor timing: **DEFER**。时机依据见方向修正表，原severity/证据/反证保留。

证据强度：STATIC_CONFIRMED。`Architecture/v2/README.md:12`写F1/F2“计划待授权”；其直接目标`P0_F_Research_Tradition.md:105`明确F2已授权，`:123`给限定原生通过及门禁关闭。

影响：fresh-thread可能重复索取已完成授权/重启旧验收。反证：根入口要求实际授权/进度查CURRENT，已定合同/限定结果未失效。建议当前索引改为合同/既定验收范围的导航，后续新范围仍另授权；不把有限PASS扩大。本轮不修。

### IA-P01-F05 — LOW：已完成L2当前切片仍派出旧L3授权建议

Refactor timing: **DEFER**。时机依据见方向修正表，原severity/证据/反证保留。

证据强度：STATIC_CONFIRMED。`Architecture/v2/P0_L2_Meaning.md:12`仍称L3-A“等待授权”，而当前Status:10,18、Authority、L3与manifest均为B168已实施/部署、用户暂缓测试。

影响：旧“当前/下一建议”可使恢复代理重复计划或重新派测。反证：B166验收本身有效，Authority/CURRENT仍能正确路由，M/N/UI未授权边界正确。建议完成切片只保留到当前状态入口的链接，不另外维护过期任务队列。本轮不改。

以上**1项MEDIUM、4项LOW**是P01确认问题；未确认CRITICAL/HIGH。此句不覆盖P02–P17，不能据此称项目安全或功能完成。

### IA-P13a-F01 — MEDIUM：D cache的固定8城工作集与多consumer轮巡冲突

Refactor timing: **MONITOR**；当新consumer将合法C_D扩大到8以上／不受现有资格上界约束时，升级为FIX_BEFORE_NEXT_PROFESSION或该consumer接入前处理。证据STATIC_CONFIRMED＋LOCAL_STRUCTURAL_REPRODUCTION，直接服务读取同turn同ref同值9/20/40城三轮均全部miss；见W02表。`DistrictCompleteness:128–149`限制LRU8；已有Infrastructure:39、Apply:26、Chair:36及Meaning:101等正常D caller，但它们会先筛资格，**当前真实可达C_D>8仍UNKNOWN**。

现在可先明确D服务工作集/输出保证；若下一consumer带来更多合法D城市、或未来接受新的ACTIVE容量gate，再核cache策略，更多caller接入后引入紧凑snapshot/按城执行的修改面会扩大。新增专业数本身不必然扩大C_D，不能仅据此强迫改cache。**当前只改cache容量可以局部做，但不是完整共享采集方案，也不能扩大成无界cache或跨真实变更复用。**先选有界当前world/ref工作集、city-major同输入消费或明确更新内snapshot之一，配合失效/prune边界；方案仍需P06a/P08 mutation审阅。已证重复工作，不是错误D、native延迟/泄漏或必须立刻全停工证据。

### IA-P13a-F02 — MEDIUM：正常事实采集成本与全部建筑/carrier定义耦合

Refactor timing: **FIX_BEFORE_NEXT_PROFESSION**。`OrdinaryBuildingCatalog:238–254`保存全部Building；DC:68–73,92–110为保留diagnostic exclusions，每次miss遍历numeric全表。GW Collector:30–50同样遍历全部Building，DialogueRefresh:137在local turn全slot重采。新增专业即使只增加internal carrier也提高B_loaded，影响所有相关城市的正常采集。

证据STATIC_CONFIRMED；当前B_loaded实际数未测。DC hit仍clone完整detail `:147–149`，只需domain总值的caller承担诊断结构。现在先在Catalog/DC/GW事实层厘清正常必要primitive与按需完整诊断；更多消费者接入前固定轻量API可减少未来caller修改面。**不同D/GW语义不可合并，也不能简单过滤所有unknown/non-ordinary/非静态slot行**，保留ordinary location/tier未知、动态slots/未审建筑事实的保护。替代native presence枚举可用性UNKNOWN，不能凭API名承诺。

### IA-P13a-F03 — MEDIUM：公共更新粒度仍是多个独立player-wide扫描

Refactor timing: **FIX_BEFORE_NEXT_PROFESSION**。`RuntimeWork.New:3–26`只批内共享，Hook:33–55已核scope只有player；Gameplay:453–468逐consumer硬编码通知，现有normal native hooks另运行。相同当前资格分别通过CurrentFacts→EffectiveFacts验证/复制；部分consumer另采district metadata、静态replacement表。W02条件场景11C/固定carrier计数支持增长方向，**不是所有这些读取都能去重**。

现在需声明共同cause/scope/dependency与可靠input/mutation边界；新模块继续复制监听/fallback会把返工面从公共入口＋当前caller扩成每个专业/能力。可先共享相同primitive/静态metadata、保留必要副本隔离与原生late facts，不建万能事件总线。不能每城每turn一次、丢foreign UNKNOWN补撤销、跨写入缓存或删除全部native preflight。今日无具体wrong-yield/原生卡顿证据；不强制当前四专业全部迁移。

### IA-P13a-F04 — MEDIUM：GW多消费者通知依赖隐式单callback包装顺序

Refactor timing: **FIX_BEFORE_NEXT_PROFESSION**。Aesthetic:230–245直接赋值OnConfirmed；Meaning:233–238保存previous后先调用它；publisher GreatWorkFacts:165仅pcall整链。当前Gameplay:768–779的Start顺序維系两者。前一callback抛异常会阻止链中后续callback，ready后的Meaning.CollectionConfirmed:174–177不补偿该通知。**当前Audit已捕获多数业务异常，未观察到实际漏收益；不能把理论异常当发生过。**

共同语义确实是“确认fact changed city subset通知”，适合明确named subscriber/顺序与逐consumer错误隔离。现在约producer＋两个订阅点；未来L3/M/N/UI等如复制previous链，注册覆盖/失败传播更难回改。无需建设全新通用事件系统或强加当前不存在的动态卸载框架。业务owned收益、history与UNKNOWN仍由各subscriber保留。

### IA-P13a-F05 — LOW：普通reconcile构造未使用的诊断汇总

Refactor timing: **DEFER**。Apply installed:47–61、Chair:47–59建amounts，而正常reconcile只取rows；Infrastructure:59,63,72累计oldCount/coefficient，:84–94不用；Commerce observed:59–62造bits/tostring/concat，apply:75只取total。证据STATIC_CONFIRMED，是真实无用构造，未量化原生分配或时延。当前是小范围清理；新增writer应沿轻量normal/按需report边界，不复制该模板。保留必须的HasBuilding/location/pillage/写后验证；不把此微优化作为公共架构结项。

## Provisional findings

| ID / 暂定程度 | 实际疑点与反证 | 下一核对位置 |
|---|---|---|
| IA-P01-Q01 / OBSERVATION | 主Architecture:7–8无范围限定的Latest Accepted Design仍D0032，容易与D0048混淆；但:5,14明确A0161保留D0032目标、后续按定域合同适用，pin本身有用途 | P02确认旧字段下游依赖与目标baseline/current增量分工，不盲目把Architecture整体升到D0048 |
| IA-P01-Q02 / LOW候选 | Technical README:21导航停在B138试运行/root-cause OPEN，未直接指向B129报告:978–986工程收束与重开条件；归因仍OPEN完全正确，缺链接不证明今天仍阻塞开发 | P13/P15审结项约束可达性；不重开性能长测或因未知归因停工 |
| IA-P01-Q03 / LOW候选 | Playtest Workflow:54的“current long play unchanged package”源自旧阶段且未显式标历史；单独阅读易误会stable就是live。:20 W0003覆盖与Authority/CURRENT/receipt足以解决真实状态 | P14审部署合同中的current/historical边界；不判断当前develop部署违规 |
| IA-P01-Q04 / OBSERVATION | v2 README:43“正式L2…逐批审核授权”可能使读者以为未正式落地；也可能指仍延期的九域六yield。B166只完成七域五yield | P11/P15复核完整范围与导航表达，不把有意延期认成整体失败 |


### W02结构性候选（影响尚待定）

| ID | severity／timing | 已核结构／未决与下一动作 |
|---|---|---|
| IA-P13a-Q01 | MEDIUM候选／MONITOR | NetworkBridge:407–415的UnitRemoved等fullscope事件直接CheckEvidence→Verified/Refresh/Capture，可能普通单位大量死亡也触发C事实确认；实际频率/可安全filter依据未知。先验证精确移除签名及saved route-unit关联；已删unit读不到不能直接当non-trader。密集新profession事件接入前需定域处理 |
| IA-P13a-Q02 | MEDIUM扩展边界／FIX_BEFORE_NEXT_PROFESSION | EffectiveFacts/NetworkInput whitelist、NetworkBridge source/center/national/display/notify及signature roles散落。当前四专业明确scope所以不判现行玩法错误；P05b/P06a补完整新kind校验/consumer graph，形成单一明确接入契约，**不把不同network角色DRY为统一Ability** |
| IA-P13a-Q03 | LOW候选／MONITOR | NetworkBridge detailPage:332,362–365按历史clicked pid:cityID存signature，同key替换但未见loss/remove prune；只是诊断按点击保留，不按每版本累积，不归为大内存根因。可在对应report退出边界再处理 |
| IA-P13a-Q04 | MEDIUM容量候选／MONITOR | UI route采集4096行而sender/bridge限128路线/16384字节，超界sender直接return；当前是否达到UNKNOWN。Harbor等提高路线容量前要共同核producer/transport/derived/downstream，不只抬一个常量 |
| IA-P13a-Q05 | MEDIUM方案待核／FIX_BEFORE_NEXT_PROFESSION | 降低unchanged carrier复核/合并fallback/共享facts或city scope可能有价值，但未完成跨城、late input、pending withdrawal、mutation closure；P06a/P08核证后才建议具体切换，不机械删验证 |

候选不算confirmed defect，也不由审计猜测新玩法。

## Rejected concerns

- **当前HEAD晚于部署commit＝运行包漂移：已排除当前实例。** 四份Mod逐文件相同，增量只是文档；不推广到将来部署。
- **main的stable baseline＝当前游戏包：已排除。** main96与runtime195分别核对；receipt明确DEVELOP_ACTIVE。没有检查引擎实际当前加载。
- **当前B168 local39／carrier0被当native PASS：所查记录反证明确。** native未验及用户暂缓保持，实例/入账/倍率不混合；未审全历史结果。
- **manifest implementation_authorized=true自动授权下一阶段：已排除该解释。** 它记录已完成窄修复，CURRENT/stop/non_scope与helperfalse共同限制。审计更窄的禁止仍优先于W0003。
- **所有Design pin必须同号／A0161的D0032目标baseline必错：已排除。** 专业各自保留有效版本，架构目标与后续适配合同分工明确；精确机制正确性仍留P02–P04。
- **Runtime_Index旧B166 provenance含native pending＝当前状态冲突：已排除该解释。** role明确继承的文件审阅来源；runtime/runtime_commit/当前Status另列。
- **主Architecture:71列GWA“尚启动”＝旧正向writer仍在运行：已排除该推论。** `Mod/Gameplay.lua:777`确实Start(...,{retired=true})，GWA各正向入口有retired保护；启动可承担withdraw。完整退出/guard闭包仍留P05/P08，不因此判全部carrier安全。
- **性能归因仍OPEN＝整个项目必须继续停工：已排除。** B129结项:978–986明确工程收束/非阻塞及重新调查条件；不升级成零泄漏或全部增长外部来源。
- **用户自选多存档测试＝新的必做门禁：已排除。** 当前manifest/结果/待办明确optional，B168延期仍有效。

### W02保留结构 / NO_ACTION或DEFER

- **NO_ACTION，限已核边界：** RuntimeWork批内缓存完整成功后发布并退出释放，当前未见无界batch引用；不是跨写入共享缓存。Effective/Current/DC的必要clone维持隔离，未发现当前borrowed样本被写回。
- **NO_ACTION：** GPP/routes/GW generic pulse clean时不产生全城采集；没有“每帧默认全scan”证据。BackgroundRoutes没有30s循环full scan timer；已排除旧印象，使用当前209行证据。
- **NO_ACTION：** 正常Network Current查询不Capture/derive；privateview/input/candidate/flight按player保留当前一份，非历史版本数组。正常world edges可能真实R×source展开，不据此指控O(C²)冗余算法。
- **NO_ACTION：** foreign回合补UNKNOWN撤销有现有真实Lua断言，不能统统过滤。单turn限流/简单删listener不是合法优化方案；native direct＋后续publication也可能分别满足不同输入。
- **NO_ACTION，限当前启动模式：** 所查UI有Shutdown/解绑，Gameplay按启动单次注册；没有具体重复Start证据，不为动态热卸载另造体系。
- **DEFER：** 手动Network.Read重复确认可局部减量，但不是normal热点；不抢占公共基础风险审计。诊断cursor/bit文本暂不作全局性能阻塞。
- **NO_ACTION：** GC维持已接受缓解与结项边界，本slice没有依据调频或宣称原生内存成本；不能用GC计数替代上面工作量模型。

## Unresolved questions / NOT_YET_AUDITED

- P01覆盖保留；W02/P13a公共hot-path slice覆盖完成，P05/P09仅direct map部分覆盖；其余P02/P03/P04/P06/P07/P08/P10/P11/P12/P13b/P14/P15/P16/P17仍NOT_YET_AUDITED。未确认风险不能因局部map关闭。
- P01没有完整审阅accepted规则、Spec/Content逐条取代、正式阅读版完整一致性、全部Mod/SQL可达writer、save/owner损坏、REALLOCATING/未结算合同、Network退出、缓存间接保留、GC策略正确性或所有测试断言/fixture。
- 当前native小数/GPP倍率/退出仍待B168用户测试；审计仅核其记录，不制造新实机要求。是否适用每城每类Floor仍未在正式运行接入，本轮无决定。
- receipt存在/目录相同不证明今天恢复包内容或崩溃中途恢复正确；P14再检查具体transaction/failure/recovery路径，不能从“有backup”猜安全。
- 321条链接检查仅8个活动入口；远端GitHub页面、冻结材料全部引用、其它文档/工具内旧路径及迁移映射未完整审计。
- 下一准确slice：**P06a主要runtime state ownership与mutation边界**。从CityProgressionStore:630–811现代index/positions/worker/逐record保存，:100–169 worker root/active/save开始，追Base/Investment/native mirror/具名exit-return/未完成事务的权威与失效；结合E2 current合同，只为公共架构边界读Shared/资格/UNKNOWN完整规则。目标是可扩展公共ownership接口，不逐能力重做save/load/exit/re-enable测试。之后P09b/08a/05b按方向修正优先顺序推进。原P02a入口保留供相关合同核对。
- 进入下一轮前只需检查baseline相关文件是否变更；本轮没有修复授权、没有修改正式状态或实现边界。用户需要决定：当前无；用户需要测试：当前无（B168待办继续）。

## 窗口结束与checkpoint纪律

每完成一个可核证单元及时更新本文件；接近窗口结束先停止扩张，保存已读范围/结果/未决/下一入口。突然中断留下dirty ledger也优于丢失工作；恢复从Git diff确定哪些内容已完成，不reset求clean。必要时在完整审计slice边界普通commit/push本报告；只stage本审计产物，不顺带修改Authority/Context_Lock/Status/Design/runtime/测试或调查主题。

本轮checkpoint：W02公共更新/扩展成本及实际Lua缓存反例已收束；按用户合盖指令停止。方向调整/timing/maps/findings/未覆盖/下一P06a入口及2份持久复现证据已保存。仅提交原ledger和这两份证据；P01不重置，B168待办不变，下一phase未开始，审计文档提交不改变游戏运行基线。
