# Specialization v0.1 Architecture — A0137

Document Owner: Codex
Architecture Revision: A0137
Design Spec Synced Through: D0024
Design Spec SHA256: 4f7d0169a3a8abce67501010a9c8ca600e345ce8b1ae23f3af6c28be069144f1
Latest Accepted Design Revision: D0024
Latest Accepted Design SHA256: 4f7d0169a3a8abce67501010a9c8ca600e345ce8b1ae23f3af6c28be069144f1
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-060.85 / modinfo85

## CURRENT AUTHORITATIVE STATE

用户明确要求回滚/隔离商业四并提交之前成果。当前源码恢复商业四实现前的完整B060.85（modinfo85，106文件），SHA256 a0e0fd75e87872612ab61a7354882ca7081767890149917efa688a60412216d4，与独立部署备份逐文件一致。B061.86/87商业汇聚及对NetworkBridge/NetworkSender/BackgroundRoutes的后续修改不在当前运行源码内。商业四停止开发，不能把历史B061测试计划当作当前任务。

用户已口述巨作相邻全部USER_GAME_TEST_PASS，基础3P→每件1P的原生小数截断接受、不修复。B060.85此前没有商业四正式收益。D0024继续保留用户确认的GW小数边界、未来商业汇聚总量备选和最终floor设计；保留设计不代表商业四已实现。

完整撤回前工作树679个非忽略文件及SHA256清单、tracked diff保存于忽略目录local/Isolated-CommerceIV-B061-20260913/。B061报告保留审计，B061可执行测试/新fixture随完整隔离副本保存，不再混入当前回归入口。恢复B061前test_b055_regression.py，不修改冻结旧fixtures。

B061.87最新两图：商业与通用网络均报BATCH_LIMIT_OR_SHAPE，UI路线COMPLETE_UI_SHADOW、商路显示0/5；空集合Data空串跨界面可能缺失是未证实假说。不能声称已修复根因，也不能把失败状态归因于旧存档。B061只增加1的异常仍未解决。先恢复基线，不继续叠加修补。

### HISTORICAL NOTES：已撤回的B061开发与测试

B061.86首批USER_GAME_TEST_FAIL：用户AUTO城市Science6→7、OFF6；截图只有OFF，source28.4219→20%5.6844→floor5，不能据此确认AUTO实际配置曾为5。第二图turn22 NETWORK_REFRESH_PENDING。未标商业四收益PASS。数据库已确认48载体定义存在，SCIENCE Amount为1/2/4等正确整数，不归因为旧组件缺失。

B061.87修复两项静态缺口：NetworkSender原先只按API调用成功去重，没有按Gameplay接收确认重试；BackgroundRoutes增加独立当前回合观察，漏回合事件时在已有UI脉冲中仅标记一次重采样。发送只对同包最多重试两次，不放宽当回合/来源有效性要求、不用旧网络继续发收益。收益报告增加每类实际存在载体总数值及bit组成，网络未就绪用简短状态/前后回合/发送状态代替长堆栈（完整日志保留）。

LOCAL_SIMULATION_PASS（不等于实机）：真实sender首次丢包恢复/最多两次/空闲零请求/新批恢复、真实turn observer一次触发，以及既有商业择优/撤销/SQL和旧批回归。实际只加1原因仍未确定；不猜测是倍率/刷新或成功。Design D0024、SQL/20%/floor/结算规则不变。

USER_GAME_TEST_REQUIRED：读原存档B061.87，原商业四城OFF后读一次，AUTO后Read Commerce IV截图，报告若目标5应显示配置5/载体5[1+4]；过一回合再Read截图。若仍未就绪，报告包含后台回合/发送信息，立即停止不重复。此次无新增组件，重载即可；若版本未刷新则完全退出重启。结果回来前暂缓多源/分发测试。

### B061.86实现基线与初始测试计划（暂缓）

D0024已同步：用户口述GW002全部USER_GAME_TEST_PASS（用户实际游戏验证），原生逐件半点截断接受不修复，未提供新截图；不扩大到未知类别/其它接口。B061.86开始商业IV正式自动汇聚：直接R/C/I来源，各yield按实际城市总量择最高，20%后floor一次。条件总量备选已明确采用，不假称精确纯本地。城市层整数载体，与Industry区域输出/Research区域复制隔离；Commerce不能作源，先计算本轮全部计划再应用、绝对替换不累加。

STATIC_CONFIRMED：48个整数城市载体、无区域yield写入，已检查当前专业身份约束；LOCAL_SIMULATION_PASS：真实NetworkBridge与计划/结算Lua，最高产出不等于最高等级、多源并列不相加、distribution不冒充direct、重复100次无写入、floor、OFF/降级/断源/过期/重载/端点失效、SQL和既有回归。静态/模拟不等于实机通过。

USER_GAME_TEST_REQUIRED：完整退出应用重启B061.86读取原存档（新增Lua/SQL），一座Commerce ACTIVE4中心已有R/C/I直接路线；Read Commerce IV，OFF/AUTO固定条件比较城市实际S/C/P，重复AUTO不叠加；增加/移除最高源检查回退；中心往另一Commerce4仅分发不得再次汇聚原源。最小3例见Validation/Specialization_B061_User_Tests.md。

限制：整数载体0..65535/每yield是技术目录非Design cap，超范围明确错误并尝试撤销，不clamp；城市倍率/同回合原生缓存刷新需实测；其它Mod把商业总量传回源的间接回路仍开放风险。无无限扫描/通用UI事件审计；加载、真实城市/总督/作品/建筑事件与网络新快照触发，空闲不扫描。读取按钮只读；OFF/AUTO是全玩家测试开关、重载恢复AUTO。

### 历史：B060组件加载与验证过程（已通过）

B060.85仅修复相邻报告请求链路，不改D0023/SQL/收益公式。用户B060.84三图：前两图仍旧Dialogue OFF报告，后一图停READING GWA_AUTO，故本批报告交付记USER_GAME_TEST_FAIL，不能由此判定BASE getter失败。静态确认GWA早返回分支未绑定RequestToken且异常未生成ACK；修复为每次返回成功/明确失败报告。UI仅对待回复的GWA读取/幂等开关使用事件脉冲最多两次重试，不扫描；增加后台模块、最近收到请求、本次接收匹配及相邻采样异常信息。根因仍需新报告定位，不宣称已确定引擎丢请求。

LOCAL_SIMULATION_PASS：真实Gameplay请求分支+真实Panel请求/渲染，正常未就绪、模块缺失、Describe异常、城市失效、首次丢包且计时器不运行时恢复、全丢包只重试两次、空闲零请求，以及B060模型/SQL和前批回归。USER_GAME_TEST_REQUIRED：旧存档重新加载B060.85，选Culture4巨作城，只点一次GW adjacency Read；截图完整报告，若仍READING可点一次Show/Copy，不需过回合反复测试。结果回来前暂停收益验收。

### B060.84实现基线

D0023已按用户明确确认接受：GW002七类作品含Artifact不含Relic/Product；全部已完成专业区域含Theater/特色替代，按原yield各50%BASE。B060.84实现自动逐作品基础相邻能力，后台复用Dialogue事件样本，新增六yield区域向量，Gameplay重验端点/类别/完成/全集。与时代对话独立开关，原生GreatWork YieldChange载体，非城市补贴。

STATIC_CONFIRMED：每个piece七类六yield定义、±0.5及二进制目录；RequiresPopulation分类覆盖已确认本机专业区域。LOCAL_SIMULATION_PASS：真实Lua/内存SQL、完工/特色/非专业排除、BASE独立于Actual、作品数不平方、负/半点配置无丢精、重复/空作品/ACTIVE降级/OFF/无效端点/过期样本/重载清理及前批回归。配置不是实际收益PASS。

USER_GAME_TEST_REQUIRED：原存档主菜单重载B060.84，GW adjacency Read/Off/Auto。建议当前Culture4城两著作放非主题化槽，先Dialogue OFF隔离上一能力；Adj Off/Auto两图包含偶数/奇数BASE对照；相邻翻倍卡不改BASE/单件配置；总督调离撤销，原生整城更新允许下回合。详细步骤见[本批测试](../Status/Validation/Specialization_B060_User_Tests.md)。无新局要求，缺数据库/采样报告一图即停。

IMPLEMENTATION_LIMITATION：本批每yield BASE须为整数且绝对合计≤8191，目录上限仅当前技术支持，不是Design cap；超范围/非整数报告错误并清除本项，不静默clamp/floor。原生0.5与普通/时代对话/主题倍率的关系待用户数据，不自行改城市补贴。当前测试优先验证前者，用户已要求停止主题化深挖。

### 历史：B059城市率验证准备

B059.83只读对照已准备：Record GW baseline保存本UI会话中选中城的turn/作品C/T/城市C与收藏所在建筑/主题状态签名；后续读数自动显示差值及条件变化警告。增加主题化建筑作品C/T小计，隐藏已完成的两个Boost按钮，现有25/50/100/OFF/AUTO保留。基线读取不切换实验状态、不写游戏Property/收益，读档丢弃基线。D0022和收益/SQL/后台传输不改。

LOCAL_SIMULATION_PASS：真实UI读取计算同回合/跨回合差值，收藏/主题变化警告，原请求/实验档/SQL回归。USER_GAME_TEST_REQUIRED：当前两著作城先OFF并过一回合，再Record GW baseline截图；100并过一回合Read截图；OFF再过一回合Read截图，固定人口/专家/建筑/政策，若变化按报告仅作观察不强归因。这是城市产出率更新验证，不等同全国市政进度/对外累计旅游入账验证。现成主题化集合可另作固定收藏OFF baseline/100比较，若无不强求。详见Validation/Specialization_B059_Settlement_User_Tests.md。

### 已确认：B059.82非主题化作品读数

B059.81截图已显示Culture ACTIVE4、合格2件、creator D2、配置15%、后台IDLE；用户确认AUTO可读，初始化/配置链路在该存档USER_GAME_TEST_PASS。两图均AUTO、原生作品5C/20T、整城108.2656C、theme0，不能当OFF/AUTO对照或收益PASS。

B059.82按用户要求新增本城临时TEST +25/+50/+100按钮；互斥替换AUTO载体，不累加，仍Culture ACTIVE4及合格类型门控。OFF清除实验、AUTO恢复D0022公式，读档清理实验并恢复AUTO。D0022、正式SQL D档、后台事件机制不改。LOCAL_SIMULATION_PASS：14修正/测试档、125/150/200参数、真实请求、幂等/切档/资格撤销/读档清理及回归。实机百分比结算仍USER_GAME_TEST_REQUIRED。

下一用户批次见[大百分比对照](../Status/Validation/Specialization_B059_Percent_User_Tests.md)：固定当前两著作及建筑，OFF→100→OFF先确认大差值；再25/50，每档读取一图。若100无变化只过一回合复读一次并停止；不继续盲测，需区分刷新/作用域/原生倍率合并。

### 历史：B059.81待复验（初始化已恢复）

B059.80实机仍未初始化，用户创建新著作也未恢复。截图Game ACK0/NO_PACKET，UI scan1 send1 retry0、API=true、reason GreatWorkCreated；当前作品3/文化8/旅游32，theme0。发送返回true不等于Gameplay送达；空后台Context计时回调未产生重发，80模拟覆盖不足，不能称根因已修复。

B059.81取消SetUpdate依赖，通用引擎事件仅对pending原包做最多两次重发（每三次事件一次），不扫描收藏；空闲/超时停止。真实收藏事件在超时后可重建最新样本，读档/回合恢复保留。公共Gameplay请求入口在校验前登记接收计数/Action/玩家和收藏包Seq/字节数，报告区分未进公共入口与未进Receive。D0022/SQL/倍率未改。

LOCAL_SIMULATION_PASS（不是实机通过）：不执行任何计时回调，通过实际Gameplay request函数而非绕过入口直接Receive；首包丢失恢复、两次重发上限、百次空闲事件零扫描/发送、超时后新作品事件恢复、GW_READ入口及既有初始化/收益回归。实机传输具体失败原因仍待新入口证据，USER_GAME_TEST_REQUIRED：同存档主菜单重载81，点击Read Great Works；若仍失败只回传一张，无需再创作或移动作品。

### 历史：B059.80计时重试（已替换）

B059.79用户截图确认Game ready=false、ACK=0、received=NONE/NO_PACKET，而UI扫描1/发送1/WAIT_ACK：数据尚未进入Receive，不能把上轮Init保护当作已修复根因。记录USER_GAME_TEST_FAIL（仅初始化）。B059.80为等待确认的同一包增加两次、间隔两秒的有界重发；复用原payload/seq，零额外收藏扫描；ACK或两次用尽即清除计时器，失败保留ACK_TIMEOUT并等待下一回合。API返回值展示，nil不冒充送达；具体引擎丢包原因尚未证实。既有事件采集、公式、SQL/D0022不变。

LOCAL_SIMULATION_PASS：首次静默拒绝后自动恢复、两次上限、无额外扫描/超时空闲、迟到ACK不叠加、同步发布重入，以及79初始化故障与既有回归。USER_GAME_TEST_REQUIRED：主菜单重载原存档，确认B059.80，等待约5秒后Read Great Works；只需一张报告。恢复后才继续OFF/AUTO收益测试。详见[传输恢复记录](../Reports/Technical/Specialization_B059_Transport_Recovery.md)。

### 历史：B059.79初始化保护（保护保留，实机未解决接收）

B059.79初始化恢复：Init跳过GetCities返回nil的玩家，与已存在NetworkBoost清理约束一致。合法seq先记录接收ACK，再pcall Init；失败留明确DIALOGUE_INIT_FAILED并等待后续具体事件，不每帧重发。记录received/stage/generation，Describe在无城市结果时报告Game ready/ACK/错误；Gameplay外层异常亦写诊断。异步事件刷新策略与D0022收益不变，真实初始化恢复待用户验证。详见[修复记录](../Reports/Technical/Specialization_B059_Initialization_Recovery.md)。

### 历史：B059.78事件刷新（仍适用，初始化保护按上文补齐）

B059.78性能修复：DialogueRefresh移除SetUpdate两秒周期扫描。GreatWorkCreated/GreatWorkMoved、城市/总督变化、加载与回合事件标记dirty；通用SystemUpdateUI/Publish/Playback只处理确认和已标记任务，空闲零扫描。事件合并，城市/作品稳定排序；发送前置in-flight锁，同回合等待ACK期间不扫描/不重发，丢确认只在下一回合回退重试。资格投资/既有GPP通知直接Dialogue.Audit，不需扫描收藏。收益公式/SQL/D0022不变。报告显示扫描/发送/状态，便于实机排查。

B059.77的通用通知扫描和两秒后备方案已废弃；原生事件先例见GreatWorksOverview.GreatWorkMoved、DiplomacyRibbon/CityPanelOverview.GreatWorkCreated。保留初始化/读档和每回合核对，不依赖玩家开UI。细节见[性能修复报告](../Reports/Technical/Specialization_B059_Event_Refresh_Fix.md)。

### 历史：B059.77周期刷新方案（已被上文取代）

B059.77已按D0022实现自动时代对话：UI/DialogueRefresh后台采集所有当前己方城市/作品；DialogueModel共用creator era解析、文物历史时代例外与D去重；Gameplay Dialogue复核完整城市集合、唯一work ID、元数据、当前turn/seq并以EffectiveFacts门控Culture ACTIVE4。当前D→单一隐藏建筑，七类Culture/Tourism共14个原生ScalingFactor修正。数据目录依据加载Eras数量，不设D7 cap，D≤1不挂加成。旧B055手动巨作载体初始化清理、旧逐件补差报告停止调用。

读档清理派生载体后后台重新采集，旧样本不是永久事实。作品移动、城市归属变化、总督等级/专业变化触发刷新；同目录档位不重复挂载。诊断OFF暂停本玩家时代对话（不是改Design），AUTO恢复按资格应用，读档回AUTO。报告区分理论/已配置和原生作品Culture/Tourism；theming只读取原生布尔状态，无自建倍率模型。所有原生实际百分比及theming仍待用户验证。见[B059报告](../Reports/Technical/Specialization_B059_Dialogue_Implementation.md)。

### 历史：D0022同步时尚未实现的调查（下文当时状态已被上文取代）

D0022取代D0021固定yield：时代对话按15×max(0,D−1)百分比，Culture与Tourism原生ScalingFactor候选为100+该百分比，D≤1移除载体。不得继续固定旅游总量/CityCenter追加路线，不改变GW002。运行仍B058.76，本轮仅同步设计/技术路线，旧GreatWorkBasis补差显示非当前机制。

时代：普通合格作品GreatWorks.GreatPersonIndividualType→GreatPersonIndividuals.EraType；Artifact按用户明确例外使用GreatWorks.EraType，两者统一去重。本机28条著作两种Era不同，不能继续一律取作品Era；25种Artifact无伟人关联，已由例外解决。原生CreatorName可作诊断，但不能通过本地化名字盲猜creator ID；关联异常要报告。

Culture：MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD + GreatWorkObjectType + YieldType=YIELD_CULTURE + ScalingFactor；Tourism：MODIFIER_SINGLE_CITY_ADJUST_TOURISM + GreatWorkObjectType + ScalingFactor。D2/3/6分别115/130/175；一城对七个合格object types采用同档，件数不乘百分比。原生与theming关系待验证，不硬编码乘算/相加补偿；不额外封顶。详见[D0022研究](../Reports/Technical/Specialization_D0022_Dialogue_Percent.md)。

### HISTORICAL NOTES：D0021及更早（固定yield路径已被当前段取代）

D0021时代对话正式取代逐件补齐。停止GreatWorkBasis旧差额计划后端和单件setter调查；现有B058.76面板仍可显示旧计划，仅是过期探针，下一实现替换为时代集合/数量/每件统一bonus，本轮不把它当当前玩法。当前运行包未修改。

目标流程：当前城市works→按D0020资格过滤→从work type映射GreatWorks.EraType→时代去重D→k×max(0,D−1)→每件统一Culture/Tourism。Culture沿用已验证的GreatWorkObjectType+YieldChange；Tourism先验证固定追加接口，不把ScalingFactor百分比误作固定点数。若独立追加不吃theming，按D0021记录原生行为，不做逐件模拟。EraType与玩家/招募/发掘时当前时代不同；缺失不默认计为某一时代，采样标不完整并报告。详见[时代对话研究](../Reports/Technical/Specialization_D0021_Dialogue_Across_Eras.md)。GW002保持原样。

### HISTORICAL NOTES：D0020及更早（旧逐件路线不再派发任务）

D0020追加：遗物与产品排除GW保值，文物仍在文化组。B058.76只读计划同步排除；文化/旅游独立最大与作品倍率/主题化要求保留。以下D0019遗物组说明是本轮较早方案，已被此修正取代。

B058.75在B057整数原生通过后正式接入D0018末端量化。NetworkBoost.Plan保留Raw/FinalRaw，最终Quantize一次，按整数Applied值选择独立载体；同整数不同N不改写，旧B055/B057载体初始化清理。当前90个整数载体（两类1–45），覆盖k=1/L≤4/N≤129；未来效率或k扩展必须扩大目录，不能clamp。旧浮点表仅保留数据库与清理兼容，不再发放。

D0019确认逐yield最大值、遗物Faith/Tourism，以及补齐部分必须适用作品倍率和主题化。UI/GreatWorkBasis是逐件基础值采集/差额计划，无收益写入。只读GreatWork_YieldChanges/GreatWorks.Tourism，不读最终产出反推基数。当前缺口是单件差额和作品倍率原生实现：已知Effect按GreatWorkObjectType作用于整类，没有静态证据证明可限定单件；不得退回普通城市固定补贴。详见[B058报告](../Reports/Technical/Specialization_B058_Boost_GW_Basis.md)。GW002未扩展。

### B057及更早实现记录（下述当时未集成/待决被当前段取代）

D0018已同步：NET-RC-005要求FinalRawBoost在全部浮点修正完成后仅执行一次math.floor(x+0.5)。B057.74先实现隔离整数写入验证，不提前切换正式网络；默认自动路径暂沿用B056，这是用户要求“正式集成前最小实测”的明确过渡状态，不能宣称符合新量化契约的正式网络已上线。实验覆写本Mod两类Boost为0/2/4，稳定整数载体按AppliedBoost选择；旧载体先移除，重复相同整数不重建叠加，重载清理实验后恢复自动路径。原生2/4实际效果USER_GAME_TEST_REQUIRED。

GW-001已改为本城文化组/遗物组最高基础值补齐，产品排除；时代曲线不再是阻塞。GW探针仍为旧city/object手动比较，尚未实现新GW玩法。多yield排序冲突、遗物yield维度、补贴倍率与GW002遗物范围保留未决。详情见[B057](../Reports/Technical/Specialization_B057_Integer_Boost_Contract.md)，当前状态/测试由Status维护。

### 此前实现说明（被上述新契约覆盖的行为保留为过渡/历史）

B056.73恢复NET-RC-005正式权重1/2/3/4，保留独立k_R/k_C、浮点L√N与既有B055载体ID；不做Lua取整或补偿。B055实机截断结论见Status；正式权重表本轮仅本地验证，不能据此扩大原生PASS范围。巨作仍为手动对照，自动时代补贴/GW002尚未接入。HD类别时代标准表可读，但GW-001/003未决规则仍须用户决定；见[B056实现及巨作研究](../Reports/Technical/Specialization_B056_Formal_Boost_GW_Standards.md)。

本版同步Accepted D0017，新增B055自动Research/Culture网络Boost与手动巨作实现接口对照；B054折扣保持既有行为。规则引用Accepted Spec；验证/下一任务由[Status](../Status/Specialization_P0_Status.md)统一维护。真实收益已运行，许多旧文件名/注释仍带Probe/DEV，这是部署边界而非“全部只是读取”。

## 运行结构

模块路径相对于仓库Mod/源码根；加载关系以SpecializationP0.modinfo及Gameplay.lua实际include/Start为准。

| 层 | 实际入口 | 职责与当前边界 |
|---|---|---|
| 测试载体/门控 | Data/Identity.sql、Frontend、Probe.lua:IsTestPlayer | 独立测试文明/领袖；当前消费者仍固定测试资格，不是已完成ELIG通用多玩家适配 |
| 新城与首次完成 | BindingProbe、CityJournalProbe、FreshBindingHook、CityFlowProbe | 双侧绑定与City Property阶段写入；普通新城按有效完成通知锁定，已有匹配正常存档恢复；不凭现有区域猜缺失历史 |
| 统一当前专业事实 | EffectiveFacts.lua | 合并foundation与投资账本；读取当前总督门槛得到ACTIVE；身份锚点含owner，完整征服继承尚未支持 |
| 移民投资 | InvestmentAction、UnitActions、UI/UnitPanelActions | Prepare不消耗；Confirm复核后INTENT→单位消费确认→提交；重复/上限/失效处理，旧未确认INTENT不盲重扣 |
| 工作专家/本地效果 | ResearchSupport、IndustrySupport、Lv2Housing、Lv2GPP、Lv3Support、Lv3Effects、Lv4Percent | 原生隐藏建筑/Modifier及基于工作人数的绝对状态；部分实际率可延迟到下回合刷新 |
| 商路来源 | UI/BackgroundRoutes、ShadowRouteState、NetworkSender | 后台City:GetTrade():GetOutgoingRoutes完整集合；无需打开贸易窗口；名称含shadow不意味着当前未桥接 |
| 游戏侧网络 | NetworkBridge、TradeRouteProbe | seq/epoch/turn/signal、端点归属与CountOutgoingRoutes核对；当前source/center/recipient重建；不是历史事件当路线事实 |
| Lv4固定复制 | UI/CopyYieldRefresh、CopyYields、Lv4CopyRead、Data/CopyYields.sql | 背景Actual采样→Gameplay复核→绝对city层收益；界面独立复核与实际配置分开显示 |
| Crew | CrewProjects、ConstructionProbe、UnitActionSitePolicy、UnitTargets、UnitActions、CrewPrecision及对应UI | 五项目原生完成产队；实际合法区域/建筑/奇观地块；限额生产力、消费和超额浪费，单位面板确认与地图目标标记 |
| 标准化记录 | StandardizationCatalog、Standardization | HD分类目录与折扣启用策略分离；城市Property一次初始化/增量学习；只读报告，不接价格或网络模板结算 |
| 保留实验 | YieldCarrierProbe、HalfYieldProbe及旧P0读取 | 与正式自动机制区分；Half ON额外实验会污染本轮对照，测试前Half OFF |

## 持久事实与派生状态

CityFlow使用SPC_DEV_CITY_FLOW_B020；EffectiveFacts/投资使用SPC_DEV_INVESTMENT_LEDGER_V1。底层仍依赖BindingProbe与B015 journal，不重命名Property或把旧DEV表无条件迁移成可信历史。阶段读回/停止模型可在DevelopmentTests找到，但不等于崩溃恢复、跨OwnerUID和全部历史连续性已解决。

专业/潜力/投资是持久事实；当前总督、来源/中心/接收集合、输出及载体是派生状态。B052标准化ledger保存城市永久掌握记录，当前网络模板并集留待独立计算。不得以旧内部建筑或过去商路事件补造当前连接。

## 后台商路与网络

用户已接受后台UI/BTS同源读取；禁止的是需要手动打开UI。正式运行来源是UI中的CityTrade当前列表，Gameplay可确认数量/任务但未找到完整可靠端点枚举；不要重新强求纯Gameplay作为开发前置。

传输行含op/oc/dp/dc/trader，边界128条、16384字符；当前按trader去重，端点用当前owner/cityID映射，非永久跨Owner城市UID承诺。发送包验证epoch、seq、回合、dirty signal及Gameplay CountOutgoingRoutes，再derive。计数相同不证明路线端点相同，因此仍需完整源快照。事件只促刷新；UNKNOWN不能当有效空网或保留旧奖励。

NetworkBridge派生direct中心来源与distribution recipient；D0009 direct即接收，首都self特殊来源；仅分发接收不形成递归direct relay。ConnectedKinds服务Commerce III，RecipientSources服务Industry IV。B055通过National()读取当前有效来源的ACTIVE最高值及recipient去重集合，自动配置原生Boost；B055实际差值已有用户同目标测试证据，范围以Status为准。

## 收益与精度

Base用于Industry I/III；Actual复制采用district:GetYield六yield口径，不是仅政策后相邻，不是city:GetYield。B051.67按D0015枚举所有已完成区域，科研排除Campus，不再按四专业或RequiresPopulation过滤；市中心也在枚举。Industry IV仍只从有效IV源锚定IZ取实际生产力，按输出金额max。未完成不计、无产出贡献0，缺失数据明确拒绝。

CopyYields.Plan支持0..65535.5范围内整数/半点，半点人口1..255。整数正负二进制位+per-population系数补偿，80个独立InternalOnly建筑；先撤旧再加新、重复不写相同状态。更细小数明确技术限制，不套Crew取整。消费者使用当前ACTIVE及真实网络；后台事件发布/播放/加载/回合入口和初始化fallback，计时器仅补充。读报告不写入收益。

城市百分比由引擎作用。B051.67扩展范围及固定条件下无持续增长的最小测试已获用户口头PASS，见Status结果；无逐区域数据，不视为市中心/所有Mod组合输入隔离的普遍证明。不静默排除类型，也不假定绝对覆盖足以防止所有反馈。详细证据见[技术索引](../Reports/Technical/README.md)。

## 下一实现策略与边界

标准化：Accepted IND-NET-004/005已经确认范围，不再把区域允许目录列为未决。实现应分为全量合格建筑目录（用于永久记录）、可版本化的折扣启用策略（用于当前资格）以及独立模板匹配组。保留BuildingType和HD分类证据；市中心三个组仅作为本项目映射，不修改HD表。当前禁用模板同样保存，后续打开策略时可重用记录。金币当前合法购买资格必须独立复核，不能把PurchaseYield字段或已记录模板等同已解锁购买；Faith隔离仍待原生调查。先实现账本、首次初始化及事件增量，不先接折扣。现有Owner/UID、旧已Industry城市初始化与征服支持边界须明确。

Commerce IV尚无正式汇聚。保留Eligible Local Basis策略接口；用户允许困难时研究总量备选、前提防递归，是条件授权，未采用为Accepted Spec替代。不能简单从含倍率最终总量减名义跨城输入。B055已接原生Boost配置，GW只有明确手动对照，尚未自动补贴。内部浮点直接传入引擎，按D0017接受引擎舍去，不推断Tourism/theming已解决。

Conquest三分支/ELIG通用系统已有离线模型，未接完整原生流程；多个已启用玩家/多人确定性及非参与者扫描成本仍待集成。部分旧模块周期遍历所有玩家，不符合最终ELIG-004成本目标，不将其合理化为设计变更。复制模块已限制周期参与者，仅生命周期做休眠载体清理。

## B055：网络Boost与巨作接口测试

`BoostConfig.lua`/`Data/NetworkBoost.sql`由`tools/generate_boost.py`同源生成。现有桥接上限128条路线：每个recipient均为某条路线的目的地或首都self，因此当前上限129城。为每种网络、ACTIVE档与N保存一个原生Amount，避免分片Modifier各自截断改变总值；不是按来源/中心累加。超出上限明确报错并撤销该轮配置，不clamp N。独立k_R/k_C在生成器配置；改值须重生成SQL/Lua，非热修改。临时权重按Spec NET-RC-005，正式权重尚待测试结束后恢复。

`NetworkBoost.lua`在首都放置每类型至多一个内部建筑，沿用Great Library的`MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST`/civic对应物。匹配HD的可撤销player property Modifier，只为兼容其额外Boost提示，不直接改写共享Property。来源/路线/总督/投资改变重新推导，旧载体先移除再加新；初始化清理保存的派生建筑并重建，读报告不启动收益。`UI/BoostRefresh`后台主动握手，避免只依赖一次LoadScreenClose。现行native科研/市政进度不由本Mod写入，不补发已触发Boost；最终封顶沿用引擎观察，仍非最终设计已确认。

`GreatWorkProbe.lua`/`Data/GreatWorkProbe.sql`是互斥手动CITY/OBJECT/OFF。CITY固定整城+2基础文化；OBJECT每件七类标准文化作品+2文化，排除Relic/Product/未知类别。两者不增加旅游业，初始化和所有权变化清理。不是GW001当代标准，也不是已实现GW002；仅比较city subsidy与native object修正的实际展示/倍率行为。`UI/BoostGreatWorkRead.lua`只读原生Boost进度与建筑巨作收益/旅游业/作品分类。七类仅是实验范围，未替用户决定最终GW003列表。

详见[B055实现报告](../Reports/Technical/Specialization_B055_Boost_GreatWork.md)；当前验证矩阵/测试由Status统一管理。旧“Boost/GW未接收益”只适用于历史版本，不覆盖本节。

## HISTORICAL NOTES

[此前A0110全文](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_fresh_agent_handoff.md)保留全部旧调查/阶段与来源链接；其中A000x等待、纯Gameplay阻塞、无正式收益、四区域复制限制等不再代表当前。精确原字节另存本轮DevelopmentBackups。既有Historical及结果原件未改。

## 可移植源码与部署

仓库Mod/是唯一可编辑源码；外部runtime只由已授权部署产生。测试入口与7个基准均在仓库；游戏数据库只读外部配置。部署检查/事务边界见../../tools/README.md；旧截图/备份/历史路径见../Reports/Proposals/Phase1_External_Materials.md。

## B052运行适配

详见[标准化记录实现](../Reports/Technical/Specialization_B052_Standardization_Ledger.md)。`SPC_STANDARDIZATION_LEDGER_V1`保存具体建筑和HD分类收据；LoadScreenClose/城市首次完成/玩家回合只发现尚无账本的Industry，已有账本不扫描城市建筑。建筑通知适配分开处理：GameEvents的player/city/building与Events的x/y/building/player不能混用。后者只对玩家城市检查通知指向的单个建筑。延后复核不构造缺失拥有事实；读取不触发写入。当前foundation token仍含既有身份约束，保存永久收据不等于已实现跨Owner继承；冲突保留旧账本并停止写入。

运行catalog直接读取HD表，分类改变需迁移，不采用旧JSON快照作白名单。启用分组引用IND-NET-005；不把范围内记录数或PurchaseYield等同实际Gold资格。历史StandardizationLedger离线原型不是本次运行入口，不把它的Tier>=1限制应用到本批市中心Tier0记录。

## B053货币适配调查

Accepted D0017 IND-NET-002允许Gold隔离困难时Faith同步打折；不扩大建筑或购买资格。PurchaseProbe/Data/PurchaseProbe.sql是独立手动实验，使用现有COLLECTION_OWNER指定建筑购买折扣，未添加无先例YieldType参数。临时双币条件只在测试按钮启用的城市生效，OFF/LoadScreenClose清除；没有接网络或账本匹配。PurchaseProbeRead在UI侧读取原版ProductionPanel使用的GetGold():GetPurchaseCost(yieldIndex,buildingHash)，不是当前购买许可判定。实际Gold/Faith行为仍须用户测试。详见[B053测试](../Status/Validation/Specialization_B053_User_Tests.md)。

## B054自动折扣运行适配

StandardizationDiscount独立于永久账本；当前来源并集和最高ACTIVE→候选计划→后台原生金币购买许可→完整版本化回传→绝对载体。NetworkBridge只新增刷新通知，不改路线语义。Standardization只新增复核后的ReadLedger读取接口，不改学习规则。新SQL依HD范围生成单建筑四档内部载体，不修改原建筑。当前采用原生指定建筑购买成本Effect及D0017双币条件授权，保留引擎尾数，不做货币退款。详情见[B054](../Reports/Technical/Specialization_B054_Network_Discounts.md)。此前B053“未接网络”段落只描述独立历史实验，当前正式状态以本段及Status为准。

## B054.71启动补偿

后台DiscountEligibility在Gameplay模块已存在但ready=false时发送DISCOUNT_INIT；游戏侧按测试文明授权调用幂等EnsureReady，清理失效载体并生成计划，不依赖打开面板。正常LoadScreenClose路径仍保留。Describe无副作用，仅补充ready/busy/generation定位。缺失一次加载事件及重复初始化已做真实Lua模拟；引擎实际漏事件原因尚未确认，不把推断写成实机已证明。
