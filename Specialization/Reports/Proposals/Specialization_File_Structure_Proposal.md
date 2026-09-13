> 批准补充（当前有效）：首次D0001由Design Chat起草并经用户确认，Codex只建DRAFT_SHELL。Research/Culture共享强度多源L已确认为max有效ACTIVE，等待D0001登记，非设计未决；不适用于Industry。下文为原调查提案语境，“尚未执行/本轮不移动”等已由[第一阶段交付](Specialization_Phase1_Migration_Report.md)取代。当前文件位置以[路径映射](Phase1_Path_Map.json)为准。

# Specialization File Structure Proposal

Proposal Revision: FSP-0001  
Date: 2026-09-11  
State: APPROVED_WITH_SUPPLEMENTS / PHASE1_EXECUTED  
Owner: Codex（本提案）；最终结构由用户确认  
Scope: 只调查与提案；唯一新增文件为本文

## 0. 原提案冻结点与待办

- 暂停P0功能扩展。当前磁盘运行包P0-B-010 / modinfo17；UUID仍df9efdad-dd48-40a7-b868-87f0617bc16d。
- **TODO：P0-B-010首都/非首都ROLE只读验证，用户尚未执行。** Verification=USER_GAME_TEST_REQUIRED；Task State=DEFERRED_USER_PAUSE。暂停不是FAIL，也不撤销此前本地模拟结果。
- B007初始化/读档、B008删城、B009新增路线已有各自限定范围的用户PASS，不能升级为B010整包验证通过。
- 本轮不改Status；上述待办暂登记在这份获授权的新提案内。方案确认后再同步到正式待办位置。
- 不移动/重命名/删除/合并文件，不改UUID、manifest、配置、源码或测试，不运行游戏，也不运行可能产生新文件的测试/报告生成器。

## A. 当前真实结构与项目边界

以下W为实际工作区绝对路径：
`/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI`

```text
W/
  DevelopmentReports/                 # 混合权威文档、报告、测试步骤、别项目产物
    Specialization_v0.1_Architecture.md
    Specialization_P0_Status.md
    Specialization_P0_*.md
    Specialization_B004_Binary_Evidence.txt
    Historical/                       # through_B003两份全文快照
    ScreenshotInbox/                   # README + 本轮盘点时2张用户截图
    Generic_GPP_Inventory.md           # CityGPPProbe，不是本项目Design
    database_inventory.json           # GPP调查数据
    write_inventory_report.py         # 会重写Generic_GPP_Inventory.md
  DevelopmentTests/                   # Specialization和CityGPPProbe混合
    test_specialization_*.py
    test_trade_route_*.py
    test_background_routes.py
    test_shadow_*.py
    test_city_role_facts.py
    NetworkStrength.lua / TradeRouteState.lua / NetworkState.lua
    snapshot_fixture.lua              # GPP相关fixture，须独立保留
    test_gpp.py / test_discovery.py / collect_gpp_log.py
    __pycache__/                      # 生成文件
  DevelopmentBackups/                 # 两个项目、代码/文档/日志快照混合
    SpecializationP0-P0-A-001 ... A-007/
    SpecializationP0-P0-B-001 ... B-009/
    Network_sqrt_pre_revision/
    Before_native_copy_semantics/
    Specialization_Architecture_R1.md
    Specialization_P0_Status_P0-A-001.md / ...A-002.md
    Specialization_P0_Batch_A_P0-A-002.md
    P0Panel_A003_before_clipboard_feedback.lua
    P0-A-002-freeze-logs/
    CityGPPProbe-*/                    # 5个别项目版本快照
  Mods/                               # 外层空目录，不是当前Specialization路径
  Sid Meier's Civilization VI/
    Mods/
      SpecializationP0/               # 当前手工源码，同时是部署运行包
      CityGPPProbe/                    # 另一个项目
    Saves/、ModUserData/、HallofFame.sqlite
  Firaxis Games/、Cache/、Logs/、Saves/、Aspyr/等游戏数据
```

盘点计数（新增本文前，排除.DS_Store）：Reports 40文件，其中35 Markdown、2 PNG、1 TXT、1 JSON、1 Python；Tests 17文件，其中12 Python、4 Lua、1 pyc；Backups 218文件；Specialization运行包15文件（6 Lua、6 SQL、2 XML、1 modinfo）。截图约占Reports空间的大头；不要因“备份目录看起来很多”先删除小型代码快照。

本工作区未发现AGENTS.md、.code-workspace、ModBuddy .modproj/.sln；工作区根和SpecializationP0根未见.git。当前不是已配置好Source→build→Runtime部署的仓库，不应假设存在构建脚本或回滚提交。

### 分类判断

| 类别 | 实际文件/目录 | 判断 |
|---|---|---|
| 当前权威文件 | Architecture、P0_Status | 前者混合WHAT/HOW，后者当前验证汇总；尚无独立Design Spec |
| 历史备份 | DevelopmentBackups与Historical全文快照 | 用于回溯，不参与当前规则判定；各版本内容/完整性不一，不默认每份都是完整项目备份 |
| 测试报告 | *_User_Result、A007_*Result*、各Batch及版本Fix报告中的结果 | 用户证据与当时条件，不能等同最新实现整包通过 |
| 临时probe | Probe.lua、TradeRouteProbe.lua、Gameplay请求、UI/P0Panel、UI/BackgroundRoutes、GovernorProbe.sql | 都是实际运行源文件；“临时”不表示可随意删 |
| 正式source雏形 | Identity/Players/Icons/Colors/Text及manifest；ShadowRouteState | 已部署的独立文明基础和候选缓存；尚非完整v0.1机制实现 |
| 离线prototype | Tests下NetworkStrength、TradeRouteState、NetworkState | 尚未被modinfo加载，不当作生产源码或设计权威 |
| generated/runtime | __pycache__、游戏日志/数据库；GPP inventory数据及其生成报告 | 不手工维护生成产物作为本项目Design；游戏数据不纳入整理 |
| 过期但应保留审计 | A/B旧批次、修复记录、旧线性sqrt前报告、旧Actual口径备份 | 保留原版本语境与superseded关系；不得在当前待办中重复派发 |

## B–C. 当前事实权威与漂移风险

目前设计事实主要在Architecture的专业表、网络规则、Base/Actual、施工队、折扣、巨作与future章节；技术实现也在同一文件。用户本轮要求建立Design单写者后，不能继续让Codex长期编辑这份混合文档的设计段落。

P0_Status承担当前验证索引，但与版本报告互相复制，且历史“本轮”条目累积。真实代码是实现行为依据，测试/用户结果是证据；它们不反过来定义想要的游戏规则。

主要风险：
1. Network sqrt报告重复公式、k、Spaceport/Entertainment设计；Architecture也保存相同规则。复制越多，越容易旧线性规则或未来scope复活。
2. B002_Findings开头连续叠加几轮互相覆盖的UI/Game PASS更正；B002_User_Result与B003_Readability标题重叠。不能把多个“最新”当当前证据，应由Status唯一索引到最终纠正后的范围。
3. B008_Batch_Flush、B009_Shadow_State、B010_City_Role_Facts同时含实现说明、验收步骤和版本状态；读者难以区分待办与历史。
4. Deferred_Cases仍保留旧“本轮只执行Batch A四项”等表述；其施工队四案尚未具备可执行实现，不能当下一批测试。
5. Probe.lua含未启用的广泛采样函数和设计数值fixture；运行文件名不代表其中所有能力已启用。为整理文件而删代码或接线会改变P0行为。
6. 整个运行目录手工维护，另外复制一份Source/Runtime会立即形成两个源码真相；活跃Mods下重复同UUID包还可能造成加载混乱。
7. Tests用parents[1]和固定相对路径；移动会破坏模块、缓存数据库路径。/tmp/city-gpp-test-runtime是本地依赖位置，不是可移植环境定义。
8. Development目录共享CityGPPProbe。Generic_GPP_Inventory.md还会被write_inventory_report.py直接重写，不能改名后遗漏生成脚本，也不应当作Shared Lv2 GPP的设计权威。

## D. 建议目标：先整理文档，保留工程位置

推荐在W下新增一个**文档与协作入口**，而不是立刻建立第二份源码树：

```text
W/Specialization/
  README.md                             # 当前权威入口、实物路径、owner表
  AGENTS.md                             # Codex协作边界；不是系统权限
  Design/
    Specialization_v0.1_Design_Spec.md   # 唯一WHAT，Design Chat写
    Design_ChangeLog.md                 # 接受的设计变更历史，不复制完整规则
  Architecture/
    Specialization_v0.1_Architecture.md # HOW、同步revision、冲突登记
  Status/
    Specialization_P0_Status.md         # 当前矩阵与唯一待办队列
    Validation/
      Cases/                           # 可复用test case，含版本/前置条件
      Results/                         # 用户实测/本地验证报告快照
  Reports/
    Technical/                         # 专项技术调查，不作为规则权威
    Proposals/                         # 文件结构、技术变更建议
  Historical/
    LegacyReports/                     # 原版本混合报告，保留basename
    DocumentSnapshots/                 # 历史文档全文，非当前规范

W/DevelopmentReports/ScreenshotInbox/   # 第一阶段保留现有投递习惯
W/DevelopmentTests/                    # 第一阶段原地保留
W/DevelopmentBackups/                  # 第一阶段原地保留
W/Sid Meier's Civilization VI/Mods/SpecializationP0/  # 原地保留，唯一运行源码
```

README用链接指向现有源码、测试、备份、ScreenshotInbox；不要创建空Source/Runtime目录来暗示两份工程，也不建议用symlink伪装已迁移。未来若需要真正Source→Runtime部署，作为独立工程任务：先定义唯一本源、部署脚本和校验，再迁移；不属于本次建议的首阶段。

现有Markdown未来优先保持文件basename，仅改变文档分类目录，降低审计和引用成本。大量混合旧报告先归LegacyReports，不为追求每份“纯净”把历史证据拆散。用户常用ScreenshotInbox可以长期保留，除非以后明确选择迁移。

## E、I. Single-writer与VS Code协作

| 范围 | 唯一日常写入者 | 其他参与者 |
|---|---|---|
| Design/Design_Spec.md | Design Chat | Codex只读；明确授权的格式/明显错误修正才例外 |
| Design/Design_ChangeLog.md | Design Chat | Codex只读 |
| Architecture/ | Codex | Design Chat只读/Review，不直接修订HOW |
| Status/及Validation | Codex | 用户提供测试证据；Design Chat只读，不登记PASS |
| Reports/Technical、Proposals | Codex | Design Chat只读，设计回应通过自己的文件或用户交接 |
| Source、Tests、manifest | Codex | Design Chat只读 |
| README、AGENTS、路径/owner表 | Codex维护，用户确认规则变更 | Design Chat只读，不能自我扩权 |
| 截图原件 | 用户投递 | Codex读取/记证据；未经另行授权不改名/删除 |
| 历史快照/备份 | 归档后冻结 | 任何AI不就地改旧内容；新更正另记 |
| 游戏数据/配置及CityGPPProbe | 不纳入本项目权限 | 本轮不触碰 |

建议Design Chat在VS Code仅打开Design目录作为主要编辑工作区；需要上下文时只读Architecture/Status。给它的任务开头明确写入白名单为两个Design文件，禁止修改其它文件、运行脚本或自动“同步”Architecture。这不是建议现在创建workspace文件或更改编辑器配置。

将同一owner约定写入将来的README/AGENTS，并把简短Owner/Scope元信息放在权威文档头部。若Codex工作根仍为W（源码不在Specialization目录下），不能只依赖嵌套AGENTS自动覆盖所有代码：实际执行任务必须明确读取该协作约定，必要时经批准在真实工程根加范围限定指引。

AGENTS、Markdown头部和VS Code工作区都是协作约束，**不会自动强制另一个ChatGPT遵守，也不是访问控制**。不要承诺Work with会自动读所有文件。每次交接显式指定文件，要求对方先确认revision和允许编辑范围。一个角色也只保持一个活动写入任务，避免两个Codex实例同时改Status。

Codex发现设计问题时在Reports/Proposals提交设计变更请求，引用规则ID和证据；不改Design。Design Chat接受后改自己的Spec/ChangeLog，Codex随后改Architecture/Status。无需双方同时写共享收件箱。

## F. Revision / Sync机制

建议采用可读的单调序号，与游戏版本、probe版本彻底分开：

```text
# Design Spec（示例，不表示现在已创建）
Document Owner: Design Chat
Design Revision: D0001
Document State: ACCEPTED
Updated: YYYY-MM-DD

# Architecture
Document Owner: Codex
Architecture Revision: A0001
Design Spec Synced Through: D0001
Design Spec SHA256: <已读取的Spec内容hash>
Sync Status: ALIGNED | CONFLICTS_RECORDED | PENDING

# Status
Document Owner: Codex
Implementation Build: P0-B-010
Architecture Revision Reviewed: A0001
Design Revision Reviewed: D0001
```

D0001只有在首次Design迁出并由用户确认后才成立。此前依旧以当前Architecture的已确认设计为过渡权威；不能一创建空Spec就让它覆盖已确认规则。草稿提案明确DRAFT，不覆盖最近接受版。

稳定规则ID如NET-RC-001、IND-CREW-001，用于跨文档引用；规则不因移动章节换ID。Spec内保留当前完整规则，ChangeLog只写哪些ID变化及理由，不再维护另一份当前数值表。

每次设计内容变化递增D序号（建议连纯编辑性变更也递增并标editorial，避免维护两套语义版本）。ChangeLog写明变更ID、scope、本次是否用户确认。技术稿不得先自行推进同步字段：Codex先比较revision/hash、检查所有变化、更新技术适配或冲突，最后才推进Synced Through。

Synced Through表示“已评估并反映到Architecture”，**不表示代码已实现或实机通过**。若评估后存在不可实现项，可以同步到该revision但Sync Status必须CONFLICTS_RECORDED，并列规则ID、DESIGN_CONFLICT或IMPLEMENTATION_LIMITATION、证据、可选方案和等待哪方决定。不能无声改设计，不自行改sqrt取整或接受Faith折扣。

revision不变但hash变化时视为UNDECLARED_CHANGE，先核对，不能自动视为同步。hash由Codex写Architecture，Design Chat不需要改Architecture。

权威顺序仅针对WHAT：Design Spec > Architecture > Status > 历史聊天。技术证据和实测结果不受这个顺序篡改：设计要求某效果并不意味着USER_GAME_TEST_PASS。聊天提出新设计可成为变更请求；用户明确的新指令需要登记，但不让未落文件的历史聊天长期成为隐藏规则层。

## Design Spec建议章节（本轮不写正文）

推荐文件名：Specialization_v0.1_Design_Spec.md。

1. 文档身份、revision、状态、读写责任和规则ID。
2. v0.1范围、测试文明身份、明确非目标。
3. 术语：specialization / potential / ACTIVE / Base / NativeDistrictCopyBasis的游戏含义。
4. 城市专业选择与发展、专业/潜力保持及已确认的总督激活条件。
5. Research、Culture、Industry、Commerce各Lv1–4权威规则与数值。
6. Trade Center、接入方向、全网络分发、接收城市集合与Research/Culture公式。
7. 施工队档位/目标/溢出、工业标准化/金币折扣、GPP、Great Work等跨章节规则（每条只放一处）。
8. Future auxiliary：Spaceport与Entertainment，显式OUT_OF_V0_1，不混入当前验收。
9. DESIGN_DECISION_REQUIRED：多源L、Industry合并、尚未定的继承等，记录未定状态，不帮用户选规则。
10. 接受的设计决策索引，链接ChangeLog；不放API调用记录、截图纠错或P0测试流水。

“单规则单位置”不禁止代码常量与测试预期值存在；它们是实现/验证，标注对应Design Revision/规则ID，在设计变更时由Codex更新。禁止的是多个文档同时自称当前设计权威。

## G. 具体文件的未来处理建议（未执行）

| 当前材料 | 建议目的地/处理 |
|---|---|
| Architecture设计章节、数值表、future规则 | 由Design Chat负责迁入Spec；Codex只提供来源映射/差异清单。用户确认首次Design后，Architecture删去权威重复表，保留规则ID引用与技术适配 |
| Architecture当前接口/契约/风险 | 留Architecture正文；逐版修复过程移历史索引，指向版本报告，不整段复制 |
| P0_Status | 留当前build、验证矩阵、BLOCKED、唯一待办和下一批；文件变更流水与旧“本轮”归历史。B010加入暂停待办 |
| Network_Sqrt | Technical中的Boost适配报告：保留浮点/Modifier调查与限制；当前公式、k及Future意图改为引用Spec，旧公式保留为历史证据 |
| Marker_Storage | Technical中的城市持久状态调查，保留Property/建筑利弊；已通过状态只引用Validation |
| B004_Trade_Route_State、BTS_Background_Read、Binary_Evidence | Technical原始来源调查/证据；建立一份技术索引，不把旧候选当现役provider |
| B002_Findings | 旧版全文归LegacyReports；提炼相邻/原生复制技术结论到独立报告，引用原文证据，不携带矛盾的“当前待测”横幅 |
| A005/A006/A007与B005–B010修复/实现报告 | 旧版混合正文原样归LegacyReports；当前Architecture链接需要的结论即可；B010未执行步骤另外进入Cases/待办 |
| *_User_Result与A007结果分析 | Validation/Results；每份保留版本、动作、证据、PASS范围和修正关系。错误旧结论不覆盖删除，以superseded-by索引纠正 |
| B002_User_Result与B003_Readability | 审核后在Status确定唯一当前结论引用；保留两个历史原件，避免盲目merge丢失UI/Game澄清顺序 |
| Batch_A、A004、B001、B004、B006 | 已完成/过期计划归LegacyReports；只有仍有效的未执行案例经审核转Cases。不把所有旧Batch复制进待办 |
| Deferred_Cases | 施工队4案转Cases/Deferred，标NOT_IMPLEMENTED/BLOCKED；用Spec引用固定档位，删掉新当前版本中的过期“本轮Batch A”话术，原文留档 |
| Great Work相关 | 当前未见独立完整专项报告；主要在Architecture与原始probe/fixture中。未来真的调查后再建Technical报告，不创建空“已研究”文件 |
| Shared Lv2 GPP相关 | Design规则留Spec；Generic_GPP_Inventory属于别项目的参考材料，链接而非吞并 |
| Historical/*through_B003、旧R1与pre_revision快照 | DocumentSnapshots或备份索引；只保留全文审计，不在当前正文复制 |
| DevelopmentBackups中的版本包、单文件、freeze日志 | 第一阶段原地冻结并索引。将来可按项目分类，但不得把所有目录默认完整/可运行，不自动清理 |
| Tests与GPP工具 | 第一阶段不迁；以后先集中路径配置再分项目。snapshot_fixture和GPP三脚本留原项目范围 |

## H. 路径与依赖：第一阶段不移动

实际Mod根为 `W/Sid Meier's Civilization VI/Mods/SpecializationP0`，不是W/Mods。

| 加载关系 | 当前路径 |
|---|---|
| manifest / UUID / version | SpecializationP0.modinfo，UUID df9efdad-dd48-40a7-b868-87f0617bc16d，17 |
| ImportFiles与include | Probe.lua、TradeRouteProbe.lua、ShadowRouteState.lua；include使用现有basename |
| AddGameplayScripts | Gameplay.lua；其内部include Probe/TradeRouteProbe |
| AddUserInterfaces | UI/P0Panel.xml与UI/BackgroundRoutes.xml；保留同名Lua配对与Context定义 |
| InGame UpdateDatabase | Data/Identity.sql、Data/GovernorProbe.sql |
| FrontEnd UpdateDatabase | Config/Players.sql |
| 前后台文本/图标/颜色 | Text/TestText.sql、Data/Icons.sql、Data/Colors.sql |
| 资源依赖 | Rise and Fall与Gathering Storm dependency UUID、Scotland资产引用全部不变 |

这些路径并非永远不可改，而是改动必须同时更新manifest、VFS/include、XML/Lua配对和验证；仅为文档整理没有必要承担该风险。不得复制到另一个活跃Mods目录造成同UUID双包。

Tests中多个脚本从`Path(__file__).resolve().parents[1]`拼出运行根；test_specialization_network另拼DevelopmentTests/NetworkStrength.lua；test_trade_route_state和shadow测试从脚本相邻位置找模型。identity测试还读取W/Firaxis Games/.../Cache与本机Steam资产绝对路径。生成器固定读取/写入DevelopmentReports的JSON/Markdown；collect_gpp_log固定写W/Logs。这些依赖都说明先保留Tests/工具位置更安全。

游戏Cache/Logs/Saves/Mods.sqlite等不是项目源码；不移动、不改配置、不为了目录清洁顺带收编。外部Steam安装与Harmony in Diversity/BTS源码作为只读研究依赖保留原处。

## J. 获得确认后的安全执行顺序

1. 确认本提案的owner表、文档根和“工程路径不动”范围；暂停所有写入者。B010继续挂起。
2. 创建一次**包含当前B010代码、Tests、Reports的完整迁移前备份**并记录文件清单/hash；现有B009备份不能代表当前B010完整项目。备份不进入活跃Mods。
3. 创建README/协作指引与明确的旧→新路径映射；如需要版本管理，仅在单独批准范围内初始化，不把整个游戏用户目录纳入Git。
4. 建立Design草稿与来源映射，由Design Chat迁出WHAT并请用户确认；直到接受D0001前旧Architecture仍是设计过渡权威。不得同时维护两个“accepted”全文版本。
5. D0001接受后，Codex拆出HOW、收敛Status、登记同步revision/hash和冲突。先完成权威切换，再接入第二个写入者。
6. 移动文档时保留basename，处理相对链接/图片引用；历史证据不批量重写正文。需要旧入口兼容时只留一行跳转或路径映射，不留第二份完整权威正文。
7. 技术报告/Results/Cases分别分类，旧混合报告原样归档；ScreenshotInbox保留，当前结论链接文字证据，缺图不编造恢复。
8. 静态检查所有链接、owner/revision字段、待办与结果范围。比较源码、manifest、Tests、UUID和游戏配置hash；文档阶段应保持不变。
9. 若以后另批移动Tests，先改集中路径解析并运行相关本地回归；不能借本次文档整理悄悄做。Source/Runtime分离另立部署任务。
10. 交付唯一入口与Design Chat编辑白名单，解除指定写入者的暂停。文档整理不需要启动游戏，B010实机测试仍等用户决定何时恢复。

回滚依据为完整备份与迁移映射，不依赖不存在的Git历史，也不把旧版本整个复制进Mods进行“临时验证”。

## 本轮结论

建议采用“新建清晰的文档协作根 + 保留现有运行源码/测试/备份/截图位置”的分阶段方案。所有目录树、元信息和重构动作都只是提案。本轮未创建Design Spec、README、AGENTS或新workspace文件，未实际迁移。

## 附录：盘点时文件清单

下列相对路径均以W为根，作为后续映射依据；不表示已移动。

### DevelopmentReports

```text
Generic_GPP_Inventory.md
Historical/Specialization_P0_Status_through_B003.md
Historical/Specialization_v0.1_Architecture_through_B003.md
ScreenshotInbox/README.md
ScreenshotInbox/Screenshot 2026-09-11 at 2.18.40 PM.png
ScreenshotInbox/Screenshot 2026-09-11 at 2.18.56 PM.png
Specialization_B004_Binary_Evidence.txt
Specialization_P0_A005_Reading_Fix.md
Specialization_P0_A006_Governor_Fix.md
Specialization_P0_A007_Native_Governor.md
Specialization_P0_A007_NewGame_Result.md
Specialization_P0_A007_Result_Analysis.md
Specialization_P0_B002_Findings.md
Specialization_P0_B002_User_Result.md
Specialization_P0_B003_Readability.md
Specialization_P0_B004_Trade_Route_State.md
Specialization_P0_B005_Unit_Type_Fix.md
Specialization_P0_B005_User_Result.md
Specialization_P0_B006_Background_Routes.md
Specialization_P0_B007_Background_Dispatch_Fix.md
Specialization_P0_B007_User_Result.md
Specialization_P0_B008_Batch_Flush.md
Specialization_P0_B008_User_Result.md
Specialization_P0_B009_Shadow_State.md
Specialization_P0_B009_User_Result.md
Specialization_P0_B010_City_Role_Facts.md
Specialization_P0_BTS_Background_Read.md
Specialization_P0_Batch_A.md
Specialization_P0_Batch_A004.md
Specialization_P0_Batch_B001.md
Specialization_P0_Batch_B004.md
Specialization_P0_Batch_B006.md
Specialization_P0_Deferred_Cases.md
Specialization_P0_Marker_Storage.md
Specialization_P0_Network_Sqrt.md
Specialization_P0_Shadow_Network_Integration.md
Specialization_P0_Status.md
Specialization_v0.1_Architecture.md
database_inventory.json
write_inventory_report.py
```

### DevelopmentTests

```text
NetworkState.lua
NetworkStrength.lua
TradeRouteState.lua
__pycache__/collect_gpp_log.cpython-310.pyc
collect_gpp_log.py
snapshot_fixture.lua
test_background_routes.py
test_city_role_facts.py
test_discovery.py
test_gpp.py
test_shadow_network_state.py
test_shadow_route_state.py
test_specialization_identity.py
test_specialization_network.py
test_specialization_p0.py
test_trade_route_probe.py
test_trade_route_state.py
```

### Sid Meier's Civilization VI/Mods/SpecializationP0

```text
Config/Players.sql
Data/Colors.sql
Data/GovernorProbe.sql
Data/Icons.sql
Data/Identity.sql
Gameplay.lua
Probe.lua
ShadowRouteState.lua
SpecializationP0.modinfo
Text/TestText.sql
TradeRouteProbe.lua
UI/BackgroundRoutes.lua
UI/BackgroundRoutes.xml
UI/P0Panel.lua
UI/P0Panel.xml
```

### DevelopmentBackups顶层条目

```text
Before_native_copy_semantics
CityGPPProbe-P0-003
CityGPPProbe-P1-001
CityGPPProbe-P1-002
CityGPPProbe-P2-001
CityGPPProbe-P3-001
Network_sqrt_pre_revision
P0-A-002-freeze-logs
P0Panel_A003_before_clipboard_feedback.lua
SpecializationP0-P0-A-001
SpecializationP0-P0-A-002
SpecializationP0-P0-A-003
SpecializationP0-P0-A-004
SpecializationP0-P0-A-005
SpecializationP0-P0-A-006
SpecializationP0-P0-A-007
SpecializationP0-P0-B-001
SpecializationP0-P0-B-002
SpecializationP0-P0-B-003
SpecializationP0-P0-B-004
SpecializationP0-P0-B-005
SpecializationP0-P0-B-006
SpecializationP0-P0-B-007
SpecializationP0-P0-B-008
SpecializationP0-P0-B-009
Specialization_Architecture_R1.md
Specialization_P0_Batch_A_P0-A-002.md
Specialization_P0_Status_P0-A-001.md
Specialization_P0_Status_P0-A-002.md
```
