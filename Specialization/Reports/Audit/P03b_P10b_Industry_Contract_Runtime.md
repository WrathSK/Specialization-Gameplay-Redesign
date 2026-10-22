# P03b/P10b — Industry知识、历史与当前旧效果

独立审计 IA20261007 / W17；基线 `4289d647f4bce5dc85c0ca28ea5534cd2a9f3431`。slice覆盖完成，项目本体只读，非工业全实现/native或总审计PASS。

## 结论与范围

建筑模板initialize/restore/reconcile已有实际实现，Tier0修复及限定原生验收保持；III/IV新标准化、N/E/L、Macro/Practice/Study及新Crew规则尚未落地，是[Industry准备矩阵](../../Architecture/v2/Industry_Preparation.md)已登记的H/G/I/J适配，不重开数值/归属TBD，不把旧PASS当新设计完成。

新增 **IA-P10b-F01：MEDIUM / FIX_BEFORE_NEXT_PROFESSION，具体H1 typed知识扩展前处理**。Standardization将HasBuilding=nil当不存在，首次初始化会提交可靠空/缺条目并确认INITIALIZED；恢复可读后Discover/boot不再扫描。实际Lua3场景支持该条件后果，native nil未观察，不是既有存档事故；禁止因此重建所有可靠空账本。

## 正式规则与实际支持

完整[Industry D0045](../../Design/Content/Industry_D0045.json)、[Spec IND](../../Design/Specialization_v0.1_Design_Spec.md)及已核Shared A/B/E/G分别负责规则；Code/现行准备/具名结果负责实现与证据。候选机构/能力/队伍名、首测值、Balance与technical成熟度独立。

| 包 | 当前真正落地 / accepted差距 |
|---|---|
| 基础/II | [IndustrySupport](../../../Mod/IndustrySupport.lua)每expert3F＋BASE P×K1，全级同公式；共同Housing/Engineer base GPP已接。不是Research3F3P，不再加旧III5F/Gold |
| 建筑知识 | [Standardization](../../../Mod/Standardization.lua)在Industry Identity初建/重入，Store同record初始化凭据；永久building ledger，当前缺失不反删，不需先ACTIVEIII |
| typed District知识 | 目前Catalog只建筑；OnDistrictConstructed调用Discover不是区域模板，H1未实现 |
| 当前标准化 | [Discount](../../../Mod/StandardizationDiscount.lua)旧≥I、groups并集＋global最高ACTIVE、旧Level×10%购买；无新建设writer/self/逐holder/L/Gold-Faith资格合同 |
| N/E/L | 没有工业可靠collector/正式字段/writer；ResearchTradition不是工业E/L，Claim原语不是研习成功账本 |
| Macro/Practice/Tradition | 已给10/20/30%、150/140/130/120%、完整1T L与2个百分点增强，I/G待实现；不再公式TBD |
| Crew | 旧训练/注入运行，P07c已核；III/IV新tier、2槽/source、成本/Wonder-only/保护归属尚未实现，J1/J2门禁 |
| 旧IV产出 | [CopyYields](../../../Mod/CopyYields.lua)仍50%sampled P，不是新标准化建造能力，正式H cutover要退出 |

当前source支持范围与accepted范围不能倒置：旧代码已运行不恢复旧Design，尚未adapt也不能否认已通过模板保存。相应cutover已分配责任，本轮不退出任何writer。

## Template ownership与四种历史状态

| 状态 | 当前真实行为 |
|---|---|
| 合法首次 / UNINITIALIZED | Complete/Industry Claim同record设初始化marker；ReadTemplates只准在此依据下nil初建 |
| INITIALIZED且空 | 有可靠初始化结果；验证后非pending不扫描伪装首次 |
| INITIALIZED已有历史 | validate原catalog/domain/tier/revision，合法return标reconcilePending；旧history clone∪当前可证建筑，完成ledger+marker同次保存 |
| 缺失/损坏/目录冲突 | 理应有历史但nil/坏结构/Tier迁移不凭current重建，保持TEMPLATES_HISTORY_UNAVAILABLE/STD_CATALOG_MIGRATION_REQUIRED |

[Store](../../../Mod/CityProgressionStore.lua)270–286持有保存与可靠空/缺史区别；Standardization解释/检验模板且stale/readback。可靠历史跟城，不属当前玩家个人；unsupported期间现存合法对象重入补录，未观察且已消失对象不追溯。pending未同步不能发布旧ledger作current source。

[StandardizationCatalog](../../../Mod/StandardizationCatalog.lua)是专属HDTier/dummy/internal/wonder和retained directory/matching groups，非Shared普通/D目录；City Center有明示组，普通D的0–4或positive Tier不限制template Tier0。recorded与enabled与本来合法Gold/Faith购买仍三层。

正常事件只增量复核signalled building，session重试至2T；永久reconcile marker由load/turn继续，过期队列不删永久知识。return callback只排队，不在current commit前读写。初始化知识不看ACTIVEIII正确：业务传播/可用才III。

学习已存在完整建筑不直接应用Shared当前收益predicate；新学习/reentry的pillaged对象与明确不遗忘的old history要区分。当前learn不查pillage；未在本slice确认此为独立规则冲突，不从它推出pillar所有effect生效或擅自换规则。对应知识扩展应保留construction experience与当前使用资格的分层。

## Confirmed — IA-P10b-F01：未知存在性被确认为空知识

Standardization51：`if not P.HasBuilding(...) then return false end`不校boolean；Probe.HasBuilding原样转发。nil因此与false合流，initialize59–68随后写ledger/ACK INITIALIZED，Store同次清reconcilePending。之后old validate且not pending即返回，不再backfill。

| actual Store/Std＋明确presence fixture | 初始记录 | 可读恢复后Discover | boot |
|---|---|---|---|
| true对照 | INITIALIZED / 1条 / pendingfalse | 1条 | 1条，无重扫 |
| nil | **INITIALIZED / 0条 / pendingfalse** | **仍0，累计presence读取1** | 仍0，scans0/额外写0 |
| 抛错 | UNINITIALIZED / 无ledger / pendingtrue | 1条，可靠完成初始化 | 1条，无重扫 |

[最小脚本](Evidence/W17/reproduce_template_unknown.py)／[原始JSON](Evidence/W17/template_unknown_result.json)使用真实未改Store/Std，one-entry Tier0 catalog及native presence/Property/event为明确stub；复用W03声明，Lua5.5，无安装/DB/game/runtime或正式tests操作。不是整目录完整性、真实存档字节或native nil事故。

**MEDIUM / FIX_BEFORE_NEXT_PROFESSION**：持久初始化确认可能漏当前可证知识；先在H1扩大typed知识/新初始化producer前收紧，修面限boolean可用性、可靠init ACK及定向测试，不要求全项目停工。

强反证：抛错正确保留pending；正常false应合法初始化空；后续新BuildingAdded或合法reentry可能补该对象，本例没有测试那些路径，不能说永远无法恢复。修复候选应拒绝UNKNOWN presence进入成功初始化，不得因这条反例扫描重建所有可靠已初始化空/损坏史。不按未观察foreign历史补造。

## 新标准化及N/E/L最低依赖

旧candidate只从Bridge recipient source取template；无localself，自身恰为首都recipient不证明任意无路self。来源≥I/group并集后global max给所有target，已被D0045actual-holder内分别MAX取代。UI权限仅Gold CanStartCommand，价格字段/nativeCost也许影响Faith不能证明合法双渠道。

H1 typed模板、H2/H3 self＋holder/III建设10/购买0、IV L增强和渠道都需真实输入/版本/native载体；不能只改SQL数字。III基础可以独立E/L推进，IV只有可靠L才增强，missing L!=0。例A L7大学/研究所、B L2大学/银行、C L5工厂，只允许其真实holders贡献；不以C效率放大银行。

| 记录 / 能力 | ownership / 依赖 |
|---|---|
| N | A城市真实Wonder完成经验，不限完成Owner/Identity/ACTIVE；供IV训练成本，当前持有量不能自动补历史 |
| E | B实际完成文明与Wonder自身Era去重，从可靠覆盖起点collect；城市转移不转信用，当前Era/征服不是证明 |
| L | A成功完整1T永久提交；不足IV/身份退出/REALLOCATING/Owner/正常生产中断取消当轮，完成L保留，L>E不截断 |
| Macro | IV正常自行生产旧EraWonder差1/2/3+加10/20/30，不依N/E/L、不放大Team |
| Practice | IV按N降低训练损耗，III固定150；不强化标准化/施工量，不按E解高档 |
| J provenance | native grant→新单位精确source identity/original Owner，当前Owner2槽/消费退出释放/保护回归；P07c安全边界复用 |

Collector须city/civ/own-era/完成dedupe及coverage，不把无collector字段填0。Store ACTIVE/origin路由不是任意foreign/未登记历史写API；轻量完成信用collector不等于启用AI专业循环。L不能照Research ACTIVE下降仍增龄或Claim真实提前完成例外，也不导入Dialogue START-era额度。

## 已有风险与证据限制

P06a-F03保存业务/模板反向validator（纯校验，不是递归）、Q01未提交root setter重入、P07c receipt读回、P13a-F03多writer/BuildingAdded逐城复核、P12工作集分别沿原编号/timing。Discovered非pending账本仍validate/read完整history；未来可明确immutable catalog/ledger revision与status API，但不能削弱损坏/未知检查或删历史求性能。

正式测试只读：B140 controlled3-building catalog真实生命周期/回归；B142 readonlyDB真实Catalog T0/T1、坏Tier/漏史/retry/并集/directconsumer；它们Network topology及购买资格包仍stub，不证明当前实际价格/双币或newholder。新F01才运行上述审计3场景，不改测试断言。

[B142具名验收](../../Status/Validation/Results/Specialization_B142_Template_Pass.md)仅所测粮仓T0/集市T1记录初始化与用户确认重启；旧Tier0失败已关闭，不重复报坏。旧B052–054人工接受限原学习/价格/等级网络，不能盖新D0045。未重看截图/外部DB，未新增nativePASS。

实际readscope：Industry675全Content/IND，Std/Catalog/Support全文；Store template/init/return/API与Discount current candidate/permission/dirty/sample/exit、Copy直接段；H/G/I/J计划、B140/B142实际fixture/核心断言与具名结果，P07c/P02b/P06/P12复用。无全部Mod/历史扫描。

下一 **P04a/P11a Culture当前合同→正常writer/Probe/旧效果/城市历史对照**：Culture_D0048/SpecCUL、现行K/L/M/N准备/证据→Aesthetic/Meaning/Inspiration probe/GreatWorkFacts与旧Dialogue/GWA精确状态。优先state ownership、BASE/追加/theming、normal/probe/legacy切换，前序callback/元数据/更新成本复用；B168仍deferred，不要求恢复实机，不自行实现M/N。
