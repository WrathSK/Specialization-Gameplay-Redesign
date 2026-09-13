# Specialization P0 Status

Document Owner: Codex
Status Revision: S0155
Implementation Build: P0-B-060.85 / modinfo85
Architecture Revision Reviewed: A0137
Design Revision Reviewed: D0024
Latest Accepted Design Revision: D0024
Design Sync State: SYNCED_WITH_LIMITATIONS
Work State: COMMERCE_IV_ISOLATED_BASELINE_RESTORED

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

B060.85用户截图已收到ACK，明确GWA_MODULE_NOT_LOADED，后台模块=false、本次已收到=true；不是学院BASE=0的证据。用户确认本城学院BASE Science +2。2026-09-13只读检查：当前Startup.log InitialInit 11:28:27；最新DebugGameplay.sqlite更新时间12:14:08，BUILDING_SPC_B060_%为0（应156）；12:14:18 Modding.log注册/应用B059但没有SPC_B060_Adjacency。磁盘manifest包含B060组件。证据支持当前进程组件清单未刷新，新Lua模块/SQL均未完整加载。先完全退出应用重启、读原存档再验证，不改代码、不删缓存、不新建局。

USER_GAME_TEST_PASS仅限85报告成功揭示模块缺失；相邻读取/收益仍USER_GAME_TEST_REQUIRED。最小测试：用户完全退出Civ VI后重启并加载原存档，选同Culture4城，GW adjacency Read。学院BASE+2应贡献SCIENCE BASE=2、每件=1（其它专业区域Science基础相邻若有则另计）；报告正常后才继续原收益批次。若仍失败只回传完整报告。上一轮“回主菜单重载”不足，已更正。

### B060.85报告修复记录

B060.85仅修复相邻报告请求链路，不改D0023/SQL/收益公式。用户B060.84三图：前两图仍旧Dialogue OFF报告，后一图停READING GWA_AUTO，故本批报告交付记USER_GAME_TEST_FAIL，不能由此判定BASE getter失败。静态确认GWA早返回分支未绑定RequestToken且异常未生成ACK；修复为每次返回成功/明确失败报告。UI仅对待回复的GWA读取/幂等开关使用事件脉冲最多两次重试，不扫描；增加后台模块、最近收到请求、本次接收匹配及相邻采样异常信息。根因仍需新报告定位，不宣称已确定引擎丢请求。

LOCAL_SIMULATION_PASS：真实Gameplay请求分支+真实Panel请求/渲染，正常未就绪、模块缺失、Describe异常、城市失效、首次丢包且计时器不运行时恢复、全丢包只重试两次、空闲零请求，以及B060模型/SQL和前批回归。USER_GAME_TEST_REQUIRED：旧存档重新加载B060.85，选Culture4巨作城，只点一次GW adjacency Read；截图完整报告，若仍READING可点一次Show/Copy，不需过回合反复测试。结果回来前暂停收益验收。

### B060.84实现基线（收益验证暂缓）

D0023已按用户明确确认接受：GW002七类作品含Artifact不含Relic/Product；全部已完成专业区域含Theater/特色替代，按原yield各50%BASE。B060.84实现自动逐作品基础相邻能力，后台复用Dialogue事件样本，新增六yield区域向量，Gameplay重验端点/类别/完成/全集。与时代对话独立开关，原生GreatWork YieldChange载体，非城市补贴。

STATIC_CONFIRMED：每个piece七类六yield定义、±0.5及二进制目录；RequiresPopulation分类覆盖已确认本机专业区域。LOCAL_SIMULATION_PASS：真实Lua/内存SQL、完工/特色/非专业排除、BASE独立于Actual、作品数不平方、负/半点配置无丢精、重复/空作品/ACTIVE降级/OFF/无效端点/过期样本/重载清理及前批回归。配置不是实际收益PASS。

USER_GAME_TEST_REQUIRED：原存档主菜单重载B060.84，GW adjacency Read/Off/Auto。建议当前Culture4城两著作放非主题化槽，先Dialogue OFF隔离上一能力；Adj Off/Auto两图包含偶数/奇数BASE对照；相邻翻倍卡不改BASE/单件配置；总督调离撤销，原生整城更新允许下回合。详细步骤见[本批测试](Validation/Specialization_B060_User_Tests.md)。无新局要求，缺数据库/采样报告一图即停。

IMPLEMENTATION_LIMITATION：本批每yield BASE须为整数且绝对合计≤8191，目录上限仅当前技术支持，不是Design cap；超范围/非整数报告错误并清除本项，不静默clamp/floor。原生0.5与普通/时代对话/主题倍率的关系待用户数据，不自行改城市补贴。当前测试优先验证前者，用户已要求停止主题化深挖。

### 历史：GW002范围待确认（已由D0023解决）

用户指示停止主题化深挖，转GW-002。两图按文件时间TEST100(T15)→OFF(T14)，同2著作/D2/theme1：作品20C/30T→10C/25T，支持本组Culture主题放大(+10)、Tourism基础追加(+5)的不同原生表现；不同游戏回合不作城市总量因果对照。只记录已有结果，主题化不再追加测试。

GW-002实现准备STATIC_CONFIRMED：Plot.GetAdjacencyYield基础读取已有工业实机先例；HD/JNR的MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD有著作Faith+4、七类Science+2先例，可逐作品/按原yield追加。公式按yield分别sum(base)*0.5，先保留浮点；不同于RES-004的全非Campus Actual范围，不复制城市总量或政策倍率。原生半点YieldChange及与GW001/主题化的实际关系尚未验证，不静默用城市补贴替代。

DESIGN_DECISION_REQUIRED：当前Spec GW003/OPEN08明确保留GW002范围，Architecture亦保留GW002遗物未决；需确认GW002采用同七类作品(含Artifact、不含Relic/Product)、专业区域范围是否所有已完成RequiresPopulation区域且含Theater/特色替代，以及保持原yield种类还是转Culture。尚未接收益、未改Design或Mod，运行仍83。准备报告见../Reports/Technical/Specialization_GW002_Implementation_Preparation.md。

### 历史：主题化测试准备（用户要求到此为止）

主题化下一小批次已准备，运行仍B059.83无需新部署。STATIC_CONFIRMED（静态而非实机）：本机Building_GreatWorks中Oxford为两个Writing槽，UniquePerson=1/SameObjectType=1/SameEras=0、C/T主题倍率100。现有奥维德/紫式部两著作可作为最小候选，移入原Culture4城市的Oxford后由原生UI/IsBuildingThemedCorrectly确认；不需新收集艺术作品。原版GreatWorksOverview.lua 267等调用同一主题判定API。

USER_GAME_TEST_REQUIRED：若原城可建Oxford，Cheat完成后同城移入两著作，确认主题化>=1/未知0；固定收藏OFF→Record GW baseline截图，TEST100→Read截图，最后AUTO。优先读取“其中作品C/T”主题化小计；若无现成Oxford且无法建造，不强求，留待其它现成合格主题化集合。仅两图，不重复非主题化/城市率测试。详细候选算法与判据见[主题化测试](Validation/Specialization_B059_Theming_User_Tests.md)。

B059.83四张实机图：T16 OFF人口5，作品5C/20T、整城122.5；T17 TEST100人口6，10C/25T、整城133.4961；T18 OFF人口6，5C/20T、整城127.2461；T19 AUTO15人口6，5C/20T、整城127.2461。USER_GAME_TEST_PASS限定：本组跨回合作品与城市产出率响应/撤销、AUTO恢复。T17→T18城市减少6.25，与作品减少5×隐含1.25倍率吻合；倍率来源未独立核对。T16→T17人口增长混入差值，不要求回落T16基线。

T17原生城市面板127.2与报告133.4961不一致，保留UI显示刷新差异，不能指定内部缓存机制。四图未显示Record基线对照行，本组人工计算足够，不要求补拍，不标基线按钮实机PASS。themed0，主题化、对外累计旅游/全国文化入账仍未验证。不追加本组重复测试；下一项仅现成主题化收藏对照。源码/运行保持B059.83，Design D0022不变。详见[结果](Validation/Results/Specialization_B059_83_City_Rate_User_Result.md)。

### 已完成本组：B059.83城市率验证准备

B059.83只读对照已准备：Record GW baseline保存本UI会话中选中城的turn/作品C/T/城市C与收藏所在建筑/主题状态签名；后续读数自动显示差值及条件变化警告。增加主题化建筑作品C/T小计，隐藏已完成的两个Boost按钮，现有25/50/100/OFF/AUTO保留。基线读取不切换实验状态、不写游戏Property/收益，读档丢弃基线。D0022和收益/SQL/后台传输不改。

LOCAL_SIMULATION_PASS：真实UI读取计算同回合/跨回合差值，收藏/主题变化警告，原请求/实验档/SQL回归。USER_GAME_TEST_REQUIRED：当前两著作城先OFF并过一回合，再Record GW baseline截图；100并过一回合Read截图；OFF再过一回合Read截图，固定人口/专家/建筑/政策，若变化按报告仅作观察不强归因。这是城市产出率更新验证，不等同全国市政进度/对外累计旅游入账验证。现成主题化集合可另作固定收藏OFF baseline/100比较，若无不强求。详见Validation/Specialization_B059_Settlement_User_Tests.md。

### 已确认：B059.82非主题化作品读数

B059.82四张截图已复核：OFF 5C/20T，TEST100 10C/25T，TEST25 5C/20T，TEST50 7C/22T。均同turn13/同城327684、Culture ACTIVE4、两著作、D2、theme0，后台scan3/send7/IDLE不变。USER_GAME_TEST_PASS仅覆盖这组非主题化作品原生读取的百分比生效/档位替换；不是整城最终文化、旅游结算、theming或读档全覆盖PASS。

四组严格吻合额外值floor(2p)+floor(3p)，C=5+额外、T=20+额外；25%额外0而非floor(5×25%)=1，支持逐件量化而非全城合计后floor。100%旅游25而非40，支持按基础追加、与现有旅游倍率加算，不乘现有20。具体引擎内部先后顺序无法仅凭这组读数唯一确定。AUTO15%的零变化与逐件截断吻合，不再视作接口不生效。无补偿、无改15%公式。

整城文化四图均108.2656：同回合整城总量未随作品读取变化，原因尚未验证，不静默归为已证实UI延迟。本轮不再要求重复百分比测试；后续正常跨回合时观察总量、现成主题化集合OFF/AUTO作为余项。若尚未恢复AUTO，用户点击恢复即可，无需截图。证据与计算见[结果](Validation/Results/Specialization_B059_82_Percent_User_Result.md)。运行仍82、源码/Design不变。

### 历史：B059.82百分比待测（本组读数已回报）

B059.81截图已显示Culture ACTIVE4、合格2件、creator D2、配置15%、后台IDLE；用户确认AUTO可读，初始化/配置链路在该存档USER_GAME_TEST_PASS。两图均AUTO、原生作品5C/20T、整城108.2656C、theme0，不能当OFF/AUTO对照或收益PASS。

B059.82按用户要求新增本城临时TEST +25/+50/+100按钮；互斥替换AUTO载体，不累加，仍Culture ACTIVE4及合格类型门控。OFF清除实验、AUTO恢复D0022公式，读档清理实验并恢复AUTO。D0022、正式SQL D档、后台事件机制不改。LOCAL_SIMULATION_PASS：14修正/测试档、125/150/200参数、真实请求、幂等/切档/资格撤销/读档清理及回归。实机百分比结算仍USER_GAME_TEST_REQUIRED。

下一用户批次见[大百分比对照](Validation/Specialization_B059_Percent_User_Tests.md)：固定当前两著作及建筑，OFF→100→OFF先确认大差值；再25/50，每档读取一图。若100无变化只过一回合复读一次并停止；不继续盲测，需区分刷新/作用域/原生倍率合并。

### 历史：B059.81待复验（初始化已恢复）

B059.80实机仍未初始化，用户创建新著作也未恢复。截图Game ACK0/NO_PACKET，UI scan1 send1 retry0、API=true、reason GreatWorkCreated；当前作品3/文化8/旅游32，theme0。发送返回true不等于Gameplay送达；空后台Context计时回调未产生重发，80模拟覆盖不足，不能称根因已修复。

B059.81取消SetUpdate依赖，通用引擎事件仅对pending原包做最多两次重发（每三次事件一次），不扫描收藏；空闲/超时停止。真实收藏事件在超时后可重建最新样本，读档/回合恢复保留。公共Gameplay请求入口在校验前登记接收计数/Action/玩家和收藏包Seq/字节数，报告区分未进公共入口与未进Receive。D0022/SQL/倍率未改。

LOCAL_SIMULATION_PASS（不是实机通过）：不执行任何计时回调，通过实际Gameplay request函数而非绕过入口直接Receive；首包丢失恢复、两次重发上限、百次空闲事件零扫描/发送、超时后新作品事件恢复、GW_READ入口及既有初始化/收益回归。实机传输具体失败原因仍待新入口证据，USER_GAME_TEST_REQUIRED：同存档主菜单重载81，点击Read Great Works；若仍失败只回传一张，无需再创作或移动作品。

### 历史：B059.80计时重试（已替换）

B059.79用户截图确认Game ready=false、ACK=0、received=NONE/NO_PACKET，而UI扫描1/发送1/WAIT_ACK：数据尚未进入Receive，不能把上轮Init保护当作已修复根因。记录USER_GAME_TEST_FAIL（仅初始化）。B059.80为等待确认的同一包增加两次、间隔两秒的有界重发；复用原payload/seq，零额外收藏扫描；ACK或两次用尽即清除计时器，失败保留ACK_TIMEOUT并等待下一回合。API返回值展示，nil不冒充送达；具体引擎丢包原因尚未证实。既有事件采集、公式、SQL/D0022不变。

LOCAL_SIMULATION_PASS：首次静默拒绝后自动恢复、两次上限、无额外扫描/超时空闲、迟到ACK不叠加、同步发布重入，以及79初始化故障与既有回归。USER_GAME_TEST_REQUIRED：主菜单重载原存档，确认B059.80，等待约5秒后Read Great Works；只需一张报告。恢复后才继续OFF/AUTO收益测试。详见[传输恢复记录](../Reports/Technical/Specialization_B059_Transport_Recovery.md)。

### 历史：B059.79初始化保护（保护保留，实机未解决接收）

用户确认78性能恢复，当前观察范围USER_GAME_TEST_PASS；截图仍Game未初始化/scan2 send2 WAIT_ACK，收益未测，见[结果及建筑加成条件](Validation/Results/Specialization_B059_78_Initialization_User_Result.md)。B059.79补齐无城市集合玩家Init guard，ACK在初始化前登记，初始化失败显示具体错误和接收状态，不再只给笼统pending。UI事件驱动/单请求防风暴保留，不改SQL/公式/D0022。

LOCAL_SIMULATION_PASS：新增无城市集合玩家初始化、故障注入失败有ACK/错误、后续事件恢复、generation拒绝诊断；78空闲零扫描/异步防重发和既有收益回归保持。实机具体根因尚无Lua日志确认，不能宣称已经游戏修复。

USER_GAME_TEST_REQUIRED：主菜单重载同存档，确认B059.79，不先点AUTO，Read Great Works应出现Culture ACTIVE、D、配置；成功后在现有高阶剧院建筑条件下继续OFF/AUTO两图，保持收藏/专家/建筑不变。若仍未初始化，只回传这一张完整报告，新增Game ready/ACK/received/stage/generation/error字段足以区分未收到/拒绝/初始化失败。不重开局、不拆建筑、不重测已恢复性能，除非再次出现异常。

### 历史：B059.78待测（性能已回报，当前是初始化恢复）

用户在未开始B059收益测试前报告卡顿/持续刷新声音，收益测试尚未执行。静态确认77后台确有通用事件+两秒全城扫描；异步ACK未到即按序号不一致重发的缺陷可在本地延迟确认条件下解释风暴风险，但未凭截图/日志确认声音必来自本模块。已修复B059.78：事件标dirty、无周期扫描、in-flight阻止重复请求，初始化/读档与回合恢复保留。

LOCAL_SIMULATION_PASS（非游戏通过）：数百通用刷新空闲零扫描/发送、延迟ACK期间不重发、事件合并、同收藏重复通知不写、总督变动、下一回合有界重试及B059全部回归。新当前入口DevelopmentTests/test_b059_event_refresh.py；旧同步UI测试冻结保留，不把旧周期模型当当前要求。D0022/SQL/收益不变。

USER_GAME_TEST_REQUIRED：先确认性能再继续原B059收益测试。退出到主菜单重载同存档（确保B059.78）；无操作停留约15秒，应无持续刷新声音；两次Read Great Works之间无作品/总督/城市/回合变化，事件后台扫描/发送计数应不持续增长。再移动一件巨作，确认D/配置正常更新；只需口述是否恢复顺畅，异常回传两次报告。原三项收益/theming测试暂缓到此修复正常后，不重复开局。

### 历史：B059.77初始待测（其刷新策略已被修复）

已部署B059.77 / modinfo77，103文件，source/runtime SHA256一致：`569dfb1ba6b6846be7eee5511dfef08b9c0f782b16d225e2b5b5dd97b51fa5f2`；未启动游戏。

B059.77 / modinfo77自动时代对话已实现，D0022不变。原始creator era去重→15×max(0,D−1)→七类原生Culture/Tourism ScalingFactor；只对Culture ACTIVE4，后台无需开面板/巨作界面，读档重建/作品移出/总督降级撤销。旧最高基础值报告停止使用，GW002/其它能力/Boost不改。

STATIC_CONFIRMED：SQL按加载Era总数生成，不设7时代上限；各D14项Modifier，115/130等为百分比系数。LOCAL_SIMULATION_PASS：实际Lua/SQL、creator与work时代冲突/文物例外、类别排除、D9=120%、后台自动初始化、同档幂等、移动降档、总督资格、OFF/AUTO、重载/过期/重复样本拒绝，以及B058/B055/B054/B052/B051回归。它们不是实机收益通过。

USER_GAME_TEST_REQUIRED：[B059三项小批次](Validation/Specialization_B059_User_Tests.md)：普通固定收藏OFF/AUTO、读档与最高时代移出/资格撤销、主题化固定收藏OFF/AUTO（若无现成收藏可后验）。不重发Boost测试。原存档优先；若报告明确DIALOGUE_DATABASE_MISSING，回传一张即可，不用对缺载体继续验算。完成本地工作后等待用户结果。

### 历史：B058/D0022同步阶段（以下当时描述不覆盖上文）

D0022已接受/同步：时代对话统一百分比15%×max(0,D−1)，D为创作者时代；文物按用户明确例外用自身历史时代。固定yield/CityCenter固定旅游追加及旧逐件补差均退出当前任务。运行仍B058.76 / modinfo76，source/runtime hash不变；新百分比能力尚未接入，旧Read Great Works差额报告已过期，不要求复验。

STATIC_CONFIRMED：本机286种非文物合格作品有伟人关联，25种文物无关联；28条著作作品Era与伟人Era不同，已改用正确关联口径。Culture与Tourism各自有ScalingFactor的原生先例，+15%映射115，不是15。此证据不等于本Mod新效果或theming实机PASS。

下一实现：按新Era集合计算D，七类统一百分比、ACTIVE4门控、事件/读档重建与降档撤销；只在末端配置一个当前百分比档，不按作品重复叠加。theming原生结算USER_GAME_TEST_REQUIRED，待新探针可运行时做固定收藏OFF/ON（非主题化/主题化）两组。当前用户无需开游戏，文物例外已决定无待答问题。GW002与其它能力未改变。

### HISTORICAL NOTES：D0021及更早（以下当时方案不覆盖上文）

D0021已接受并同步Architecture：时代对话每件k×max(0,D−1) Culture/Tourism，k=1，D为本城合格作品不同创作时代数；旧最高基础值逐件补差正式废弃，停止单件setter/强制主题化模拟研究。当前Mod仍B058.76 / modinfo76，源/运行hash不变。Read Great Works里的旧补差计划现为过期探针，不再要求用户测试；下一实现应替换，不把旧显示当新效果。

STATIC_CONFIRMED：原版GreatWorksOverview以GreatWorks.EraType展示时代/比较文物主题，本机311种合格文化work type均有EraType。Culture统一YieldChange接口已有B055单件实验依据；统一Tourism固定点数尚未证实，ScalingFactor不是固定点数。theming自然关系仍USER_GAME_TEST_REQUIRED（未来探针就绪后最小同一收藏OFF/ON比较），当前不要求用户操作未实现按钮。详见[研究及未来测试](../Reports/Technical/Specialization_D0021_Dialogue_Across_Eras.md)。

下一实现优先D读取与统一Culture，独立验证固定Tourism追加；可能用仅City Center的district tourism flat总量承接，必须验证只有一个目标且记录theming不参与的实际表现，不假装按作品内在数值写入。缺失/未知Era报告，不用玩家时代猜测。GW002与其它CultureIV不改，既有BoostPASS不重测。

### HISTORICAL NOTES：D0020及更早（以下旧技术阻塞已被新设计取代）

已部署B058.76 / modinfo76，98文件，源/运行SHA256一致：`efb2363a44ef151f95989da8ea080775f03d7f33fe02aa4495336482c7616719`。当前测试入口DevelopmentTests/test_b058_boost_gw_basis.py通过（本地证据）。

D0020本轮追加：遗物与产品排除保值；文物仍适用。B058.76计划读取只比较文化类Culture/Tourism，不再要求遗物测试。只读数据库遗物4Faith/8Tourism一致；不推导未来所有Mod遗物均相同。以下D0019遗物组描述保留为本轮较早过程，不覆盖此段。倍率/主题化后端问题仍待技术实现。

B057三张图复核为USER_GAME_TEST_PASS（用户实机明确整数写入0/2/4），见[结果](Validation/Results/Specialization_B057_Integer_User_Result.md)：测绘203/215/227、法学725/768/812，差值满足整数百分点，最终进度尾差不足1。不重发本项测试，不外推截图未覆盖的重复/OFF/重载。

B058.75正式网络已接最终一次floor(FinalRaw+0.5)，k/L/N/topology不变；Raw与Applied分别报告。LOCAL_SIMULATION_PASS：真实Lua去重、同整数复用、降级/旧载体清理/重载、整数目录、此前回归；不等于正式自动新组合全部实机通过。下一正常测试顺手观察Raw≈5.657→Applied6即可，不新增完整Boost数值批次。

D0019用户确认文化组Culture/Tourism及遗物组Faith/Tourism各取最大，作品专属倍率和主题化必须适用。旧GW时代与两项设计问题已关闭；当前技术问题是逐件不同差额如何保留作品原生倍率。已实现只读基础采集/逐件计划，Read Great Works可显示，无正式巨作补贴。STATIC_CONFIRMED只发现按类型的原生GreatWork加成先例，未证明单件参数可用，不能据此宣称绝对不可实现。正在研究，不以普通城市加产代替用户要求。

可选最小新增读取：原文化IV城放两件基础不同的文化巨作，Read Great Works截一张；若方便移走最高作品再读一次，目标应立即按剩余作品重算。这里仅验新基础/差额读取，不声称效果上线；不需要重复旧+2C实验。遗物不足两种基础时显示应补0正常，不强求额外开局。下一步继续单件补差与主题化后端研究，无新设计决定要求。

### HISTORICAL NOTES：B057及更早（以下当时状态不覆盖上文）

B057.74已部署：95文件，源/运行hash一致 `6db4eb5d2e10bab6acccae8d0e968788939707e0b1a10b72d0849fdac1d086f6`，不代表用户实机已通过。

D0018明确最终一次floor(FinalRawBoost+0.5)，取代D0017接受原生截断策略；实机观察历史不倒改。B057.74为最小整数接口实验，尚未正式切换自动网络量化。默认自动仍B056正式权重/原生小数处理，等待用户要求的整数实测后替换；实验入口临时替换两类网络Boost，不叠加。0/Raw1.5→2/Raw3.8→4/恢复自动共4新按钮，共12个工作按钮，巨作保留原手动对照。

STATIC_CONFIRMED：新SQL明确Amount整数2/4，镜像HD提示参数同值，D0017冻结hash一致。LOCAL_SIMULATION_PASS：显式半向上、末端量化反例、3.6/3.9同整数幂等、旧效果撤销/零/恢复/重载/缺表门控及既有回归。两者都不是实机。USER_GAME_TEST_REQUIRED：[B057同存档三分支](Validation/Specialization_B057_User_Tests.md)，含零对照与两项整数输入，只需三张报告；不调整拓扑，不再研究引擎保留小数。原存档优先；若新增SQL定义未载入，停止该次测量并回传提示，不默认必须新局。

GW-001新设计已登记：本城文化类组/遗物组各自最高基础值补齐，产品不适用。旧时代标准/曲线OPEN被取代；本轮没有实现或派发新的巨作收益测试，旧GW按钮不代表新玩法。多yield排序/遗物具体yield维度/倍率、GW002遗物范围尚待后续明确，不阻塞本轮整数测试。下一步先等B057原生整数结果，再将量化接入正式自动网络，不自行修改k/L/N/Entertainment参数。

### HISTORICAL NOTES：B056及更早记录（以下当时状态不覆盖上文）

B056.73 / modinfo73已恢复正式1/2/3/4权重并部署，k_R/k_C仍独立为1，内部浮点原样交给原生Modifier。1032组SQL/Lua配置、实际Lua网络状态与既有折扣/模板/复制回归为LOCAL_SIMULATION_PASS（非实机）；HD巨作标准表为STATIC_CONFIRMED（非实机）。D0017及其hash不变。没有扩大B055用户测试PASS范围；不再派已完成的小数截断测试。正式配置在旧存档中的数据库/既存Modifier更新行为未新增实机证据，不能仅凭新报告权重证明旧存档实际数值已变；后续收益测试使用明确匹配版本的新局或单独核对，不要求现在为此开局。

当前下一项：巨作自动保值的时代口径、无标准类别/时代、旅游业和主题化等倍率规则仍DESIGN_DECISION_REQUIRED（GW-001/003）。已找到HD专用标准表42行；不从特殊著作反推曲线。用户已收到“玩家当前时代＋HD表＋缺表暂不补贴”的候选问题，尚未收到选择，此候选未生效。古代/未来缺标准，尤其未来时代停补贴可能导致回落，须明确决定是否沿用最近已定义时代；文物18/18独立，遗物/Product不在表。GW002适用清单与倍率也未擅自决定。当前不新增用户实机测试。

本轮变更/研究与验证命令见[B056报告](../Reports/Technical/Specialization_B056_Formal_Boost_GW_Standards.md)。运行包94文件，SHA256 `d13b986f93d6b219c24a802525b29f1ddd8c96c446b710c3e4af58d0454c4a89`；部署前后hash核对，UUID不变。没有启动游戏、修改Design或提交Git。

### HISTORICAL NOTES：此前轮次说明（当时“当前/下一轮/待测”不覆盖上文）

B055同目标T1/T2/T3已复核：[计算与结果](Validation/Results/Specialization_B055_Same_Target_User_Result.md)。法学790/747/790、测绘239/209/245；实际差值支持额外百分点先舍去小数再影响进度。按D0017接受，不补偿，测试范围内自动应用/总督降级/新增recipient为USER_GAME_TEST_PASS。基础34%×当前成本的绝对偏差仍单独记录，不能全部归为截断；不再为已确定的小数平台重复派测试。当前用户无需操作。运行仍B055.72临时权重，下一开发轮显式恢复正式1/2/3/4并按GW后续边界推进，非本次验算自动部署。

已完成的用户测试为[现有网络同目标三分支](Validation/Specialization_B055_Same_Target_Tests.md)：测绘600/法学2160，共同预Boost存档S；T1当前N2、T2仅降级总督、T3恢复S后追加首都→D使N3。无需首都投资或重复随机科技测试；共3报告。该三分支现已回报，取整证据及PASS边界以上述最新结果为准，不强制凑绝对理论数值。巨作稳定单件对照已通过，不重发。仅新增测试计划/状态，运行B055.72不变。

B055巨作第二批4图已复核：[稳定对照结果](Validation/Results/Specialization_B055_GW_Stable_User_Result.md)。全程2专家、单件著作；OFF/OBJECT/CITY/OFF跨回合整城23.3164→25.5156→25.5156→23.3164，约+2.2符合+10%城市倍率，作品文化2→4→2→2，旅游业恒3。该单件后端加成/撤销为USER_GAME_TEST_PASS，不重发本项测试；多件移动/读档/theming仍未确认。用户提出Boost分项取整假设已复算：能解释砌砖，不能统一解释全部6项，精确数值仍待后续对照。该轮未新增操作要求；随后用户已指定可用目标，本轮测试以顶部同目标计划为准，源码/运行保持B055.72。

B055首批8图已复核，见[逐项验算](Validation/Results/Specialization_B055_First_User_Result.md)。HD本机基础Boost=34（STATIC_CONFIRMED）；L/N配置变化有用户实机证据，同成本科技升档多18进度，与整数3→6的假设吻合。但全部样本不能由34+floor(extra)统一解释，不把精度合同判为PASS、不补偿。巨作四图显示读数/城市栏不同步且首尾OFF基线不同，该首批B055-3当时未能判定，后续稳定单件对照已由上文通过；作品类型/数量与旅游业3已读。B055-4及Boost重载未获本次结果，保持待测。本轮只验算/记录/归档，运行仍B055.72、D0017不变。

B055.72已准备下一批原生测试：Research/Culture网络自动配置额外Boost，使用用户要求的临时1.1/2.2/3.3/4.5权重；巨作提供手动city/object对照。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS是本地证据；原生Boost数值、撤销与巨作展示均USER_GAME_TEST_REQUIRED，不能用配置读数判定实际生效。测试见[B055四项小批次](Validation/Specialization_B055_User_Tests.md)。本批部署后停止，无自动接受GW曲线/最终封顶。

B054.71用户明确确认全部批次通过：等级变化、自动选择最高等级、模板并集去重、撤销与重载均为USER_GAME_TEST_PASS，见[用户结果](Validation/Results/Specialization_B054_User_Result.md)。先前70的未初始化失败及71修复调查保留历史证据，不再作为当前待测/阻塞。无新增截图或完整双币价格对，不外推全部建筑、货币组合及商路生命周期。

B052用户口述人工PASS，见[结果](Validation/Results/Specialization_B052_User_Result.md)；按钮冲突后的重启与本批正常路径按用户确认关闭，无新增截图/数值，不外推所有获取方法或征服。B053已由用户人工确认通过，粮仓折后190的尾数可接受，见[B053结果](Validation/Results/Specialization_B053_User_Result.md)。当前B054已接入自动网络模板并集、最高ACTIVE折扣与后台Gold资格检查。D0017已允许货币隔离困难时同一合格建筑Faith同步折扣。B054当前批次已关闭，不重发；当前仅需本页B055新测试。

当前Git基准已建立；B052按Accepted D0015实现标准化永久模板记录、一次补录与建筑事件增量，新增只读报告；此记录层本身不改变购买资格；B054另行接入可撤销折扣。当前四专业Lv1–3主体、科研/文化IV专家百分比、科研/工业IV固定复制、投资与Crew已有运行实现；不是“全部P0仍只读”。整体v0.1未完成，不给虚构完成百分比。

B051.67最小补测已由用户口头确认通过，无图/数值，见[B051.67结果](Validation/Results/Specialization_B051_67_User_Result.md)。本轮派发的扩展非学院区域复制与固定条件下无持续增长验收已关闭；未列明区域、旧完整三案和所有组合不随之升级。[标准化候选目录](../Reports/Technical/Specialization_Standardization_Catalog_Candidate.md)已整理：167栋/17类区域，其范围已由D0015确认；候选导出仍保留为调查快照，不作运行白名单。B052运行时读取HD分类，自动折扣B054.71已按当前批次实机通过。

用户报告B052按钮未出现：Modding.log确认游戏加载Mods内的旧版备份（同UUID），不是B052账本已失败的证据。已将备份完整移出扫描目录并修复部署工具；B052包字节不变。用户随后口述PASS，此按钮阻断已关闭。见[部署冲突修正](../Reports/Technical/Specialization_B052_Deployment_Collision.md)。

## 验证等级

STATIC_CONFIRMED=源码/数据库静态证据；LOCAL_SIMULATION_PASS=本地模拟，均不代表引擎通过。USER_GAME_TEST_REQUIRED=待用户游戏验证；USER_GAME_TEST_PASS/FAIL=用户已实际验证的明确场景。BLOCKED=无法继续而需技术突破/设计决定；DEFERRED只是延后，不是假失败。配置载体正确不等于原生产出正确；截图与口述分别标注。

## 当前实现与验证矩阵

| 模块 | 当前实现 | 已有证据及局限 |
|---|---|---|
| 独立文明、City Property、总督/专家基础接口 | 运行 | A1/A2及新局总督present/established/2–4门槛、实际工作专家按用户确认通过；旧证据见历史快照 |
| 新城完成→身份、正常读档 | CityFlow/B020–21运行 | [B020](Validation/Results/Specialization_B020_User_Result.md)、[B021](Validation/Results/Specialization_B021_User_Result.md) USER_GAME_TEST_PASS，含Cheat同回合完成；不是无历史旧城自动初始化或极端丢写恢复 |
| 移民投资/ACTIVE | 运行至Potential4，单位面板准备/确认 | [B033](Validation/Results/Specialization_B033_User_Result.md)、[B035](Validation/Results/Specialization_B035_User_Result.md)、[B043](Validation/Results/Specialization_B043_User_Result.md)用户证据，含上限拒绝与总督门控；不宣称完整征服继承 |
| Research/Culture/Commerce Lv1 | 自动运行 | [B024](Validation/Results/Specialization_B024_User_Result.md)用户通过；新城、建筑、多个专家与不更改既有专业按回报范围 |
| Industry Lv1 | 自动Base相邻专家支持 | [B036更正](Validation/Results/Specialization_B036_User_Confirmation.md)用户确认通过：额外2P是原生工业专家基础，不应扣掉 |
| 共同Lv2住房、基础GPP | 自动运行 | [住房](Validation/Results/Specialization_B034_User_Result.md)、[GPP](Validation/Results/Specialization_B035_User_Result.md)用户通过；百分比组合只支持已测情况；已接受延迟见技术索引 |
| 四专业Lv3 | 支持档位、科研/文化人口奖励、工业BaseP/Gold、商业网络类型奖励运行 | [B037修复通过](Validation/Results/Specialization_B037_Promotion_User_Pass.md)、[科研](Validation/Results/Specialization_B038_Population_User_Result.md)、[文化](Validation/Results/Specialization_B038_Culture_User_Result.md)及用户其余正常回报；不擅改0.5 |
| 后台商路/网络拓扑 | 全集后台桥接、direct/recipient分开，无需开UI | [B026历史](Validation/Results/Specialization_B026_User_Result.md)、[D0009 direct接收](Validation/Results/Specialization_B027_User_Result.md)、[删目的城撤销](Validation/Results/Specialization_B031_User_Result.md)通过；自然完成/战争/掠夺等不据此全通过 |
| Crew五项目/单位/目标/确认/限额注入 | 运行，五档、速度整数、排序与UX已落实 | [B043](Validation/Results/Specialization_B043_User_Result.md)、[UX](Validation/Results/Specialization_B045_User_Result.md)、[快速速度澄清](Validation/Results/Specialization_B046_User_Clarification.md)等用户结果；B048用户通过。不能据一级/五级实测外推所有速度全部档位 |
| Research/Culture IV专家百分比 | 运行 | [B048](Validation/Results/Specialization_B048_User_Result.md) USER_GAME_TEST_PASS；不是Culture全部IV完成 |
| Research/Industry IV固定复制 | B051.67运行 | [B051.66结果](Validation/Results/Specialization_B051_66_User_Result.md)工业4.5P/科研标准区域半点通过；旧范围错误修复后的[B051.67最小补测](Validation/Results/Specialization_B051_67_User_Result.md)用户口头通过；无截图/数值，不外推全部区域组合 |
| 标准化模板 / 购买折扣 | B052账本；B054后台自动网络折扣 | B052/B053用户口述通过；B054.71 USER_GAME_TEST_PASS：等级变化、最高等级、并集去重、撤销/重载。D0017允许必要时双币折扣，不开放购买资格 |
| Research/Culture Boost | B055原生自动配置，临时小数测试权重 | T1/T2/T3用户实机通过：同目标增量/降级/新增recipient支持整数百分点先截断，按D0017不修复；正式权重待恢复，绝对基数偏差/最终封顶另保留 |
| Culture IV两项Great Work效果 | B055手动后端对照；自动时代补贴/基础相邻尚未实现 | 本地互斥/清理/分类测试通过；作品/城市对照USER_GAME_TEST_REQUIRED，时代曲线及最终倍率仍有待决 |
| Commerce IV汇聚 | B061实现已隔离，当前无正式汇聚 | D0024设计保留；失败调查暂停，禁止继续旧批测试 |
| 通用ELIG / Conquest Claim与跨Owner继承 | 离线契约/候选，运行适配不完整 | 固定测试载体与owner锚点仍在；不能重置投资解决征服，也不能把Future全部提到v0.1 |

## 下一任务（只有此队列有效）

1. **B051.67当前最小验收已关闭。** 用户口头PASS见结果，不重发本次测试；如未来有反例，再按具体失败场景诊断。原三案的其它未明确实测边界保留。
2. **B054当前验收已关闭。** 用户确认完整批次通过，不重复派测试；保留源账本、现有原生尾数与D0017货币规则。

3. 已收到B055部分结果，巨作稳定单件对照已通过，同目标Boost增量/原生小数舍去已按最新结果通过，绝对基数边界仍保留；不将全批次关闭。小数截断按D0017记录不修复。回报后恢复正式1/2/3/4权重（显式下一版变更），再按GW接口结果、时代曲线设计决定推进GW001/002。Commerce IV/通用资格/Conquest仍待后续，不在B055展开。

## BLOCKED / DESIGN DECISION REQUIRED / DEFERRED

- CONFIRMED_DESIGN：标准化记录全目录与v0.1折扣启用范围/市中心三组已由D0015 IND-NET-004/005确定，不再列未决。新模组未知分类或未来新增范围不自动推断。货币隔离困难时双币折扣已由D0017授权；B054自动接入当前批次已由用户实机确认。
- DESIGN_DECISION_REQUIRED：Boost最终封顶（量化按D0017已解决，不再先调查），Great Work时代标准/类别/Tourism与theming语义，Claim精确成本等按Spec OPEN保留。Research全非学院范围已由D0014解决，不再列未决；GW范围不是自动同步扩展。
- IMPLEMENTATION_LIMITATION：固定复制仅整数/半点及当前人口/金额范围；跨Owner稳定UID、完整Conquest、旧存档缺史初始化、非参与者周期成本、多玩家/多人一致性未完成。无可靠纯Gameplay端点全集不再是主线BLOCKED。
- DEFERRED：B010原探针未测且用户明确延后；商路自然结束/战争/取消/商人掠夺等尚无完整对应实机证据，不把Cheat删除城市等同所有生命周期通过。不给用户重发旧大批测试。
- NO_FIX / NO_ADDITIONAL_TEST：已接受住房/GPP显示与getter刷新延迟；未来失败须区分载体状态和原生总量，不用该备注掩盖真正未应用。

## 交接与证据

[技术索引](../Reports/Technical/README.md)、[交接审计](../Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md)、[测试运行](../../DevelopmentTests/README.md)。测试原始结果冻结，纠正写新结果。ScreenShots仅待投递，不代替Evidence；用户无图但明确口述可按范围记PASS。

[此前S0115全文](../Historical/DocumentSnapshots/Specialization_P0_Status_before_fresh_agent_handoff.md)保存早期A001–B051矩阵、每批历史及完整证据索引；该文件所有“下一项/待测”均为历史，不与本队列并存。

## Phase 1停止点

Phase 1/2已由用户审核完成并建立GitHub initial baseline；以上迁移阶段文字为历史。当前B051.67最小补测已口头通过，下一任务以本页当前队列为准；B054当前批次已通过；新增实机要求仅见B055。旧Evidence、ScreenShots、DevelopmentBackups均为外部只读审计材料；路径映射见../Reports/Proposals/Phase1_External_Materials.md。
