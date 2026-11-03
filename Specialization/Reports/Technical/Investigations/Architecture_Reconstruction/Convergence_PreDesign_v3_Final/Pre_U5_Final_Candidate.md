# Pre-U5：最终候选窄包与门禁

调查材料／后继候选；不覆盖正式规范。

Status: Stable（可审阅的候选文档，不是工程或实机 PASS）。

维护者：Primary｜日期：2026-11-03｜实际 develop：`719eb61b410765fb6e8703a47840ce3cec3fa823`。正式记录仍为 D0058／A0183／S0866；B399.426 仅为既有部署记录，本轮未重新验包。

**NO IMPLEMENTATION AUTHORIZATION。** 本主题承接原 H3 中文交付；仅新增候选 Markdown，原 v3 九文件及代码／测试／工具／正式规范／治理／运行包均不改。

本表全部是未来工作计划。固定外部审计／Owner再次实施授权未过，任何PU均不能执行。PU01/02/03/05/06仍是优先范围，PU04证实后窄修；PU07–10不自动扩批。准确源与原最小回归在原v3行，当前字节未变。

| PU / G | 入口 | 具体职责／等价边界 | 最小LOCAL（未执行） | 最小USER_NATIVE（未执行） | 失败停止 |
|---|---|---|---|---|---|
| PU01/G03 | 共享事实错误归类＋Commerce真实输入；不含完整O1迁移 | 修UNKNOWN→0与根因，获批同refD/worker重算；保留交易严格 | L3；T02/04/08；真Commerce+facts的current/first/negative/secondchange | 仅changed普通状态/读档；本地不能回答才加最小native | 若需新共享生命周期或私有cache则停；临时hold不算O1关闭；[原 v3 Pre_U5_Final_Candidate.md:16](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L16) |
| PU02/G26 | 当前A/B症状与真实UI/helper | A准备后inert、B唯一匹配确认；查routing/tag/hitbox/async，不盲swap | L2＋真实actionowner；重复A/B、stale plan/换单位、两操作一次性 | 清算／配置各一组A准备/A无效/B确认 | 不能证明click路径原因不称修复；native结果未决不重放；[原 v3 Pre_U5_Final_Candidate.md:17](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L17) |
| PU03/G08 | 保留NET1/2、D1当前正式行为 | 分尝试与成功登记水位，相关恢复有责；不夹带O3新cold行为 | L3；T02/05/08；真Bridge→FC→Bindings→owner，throw/同proof/旧ACK/reentry | 普通网络恢复delta，不让玩家造throw | 仅挪赋值无真实唤醒不验收；不得放宽TransactionCurrent；[原 v3 Pre_U5_Final_Candidate.md:18](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L18) |
| PU04/G04 | 先证明独立可靠的currentnegative | 窄修ACTIVE断言遮退出；旧D不证明当前负事实 | L3；T06/08；Infrastructure正值/负事实/UNKNOWN/ref/第二变 | 必要changed资格退出，不随机掠夺 | 没有独立负事实则不改；不UNKNOWN=0；[原 v3 Pre_U5_Final_Candidate.md:19](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L19) |
| PU05/G14 | 先建立唯一completion/source/request/unit凭据 | 修同回合多城合法完成；差值只发现漏失；HELD/CALLING有新证据才恢复 | L3；T06/08；真Crew+Store同/异级多城、重复乱序/晚到、cold/CALLING/写歧义 | 仅缺事实时最小两城同级delivery见证；新probe须单独受审退出边界 | 缺唯一proof停该切片；不计数补发/按位置猜source/盲重放；[原 v3 Pre_U5_Final_Candidate.md:20](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L20) |
| PU06/G29 | ODP02=A闭环；FS06后继先正式同步；其它strict可靠 | 补严重叶错误、来源区分、VENTURE报价确认及锁terms；STABLE无额外R门槛 | L3；T06/08；真实0/不适用0/政策0、III/IV、两mode、来源变更、其它UNKNOWN拒绝、旧结算 | 正常报价/确认与必要一份changed结算；不强造损坏档或刷RNG | R0不能豁免parent/配置/余额/network/未决结果；不追改旧合同；[原 v3 Pre_U5_Final_Candidate.md:21](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L21) |
| PU07/G11 | 证实正常firstcompletion缺陷影响U5才纳入 | 核constructed参数、相关性先后、missing/late target与stickyerror root | L3；真completion/admission、wrongowner/type、重复、firstproof | 只有本地不能回答的对象时序才观察 | 需新持久见证先证必要再授权；不猜first/清error；[原 v3 Pre_U5_Final_Candidate.md:22](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L22) |
| PU08/G28 | 先区分foreign窗口、writebug与已回归端点 | 只按实际授权端点/episode退出；不跨新owner/ref回放旧cleanup | L3；T06/08；真实Store+exit的loss/return/ref/token/parent三时序 | 不扩大易主玩法；缺具体接口事实另提最小验证 | 需新增清理权威则Owner Packet；不是通用回调恢复；[原 v3 Pre_U5_Final_Candidate.md:23](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L23) |
| PU09/G13 | 保持真实nativeearly Claim合法 | 只核实Gameplay完成/取消签名；不移植NarrativebCanceled或timer门槛 | L3；actualClaim/ref/unique receipt、真实early/重复晚到 | 不重做三项目共同计时；必要一次参数观察 | 未核实signature不得过滤合法完成；[原 v3 Pre_U5_Final_Candidate.md:24](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L24) |
| PU10/G06 | 正常无总督KNOWN1；实际UNKNOWN root待证 | 查六属性trait/ref/初始化/publish；统一ACTIVE；无四套cache | L3；T01/02/08；phase/ref/读中变化，注入不冒充native复现 | 现有证据不足且阻依赖时最小有界采样 | 正常缺陷才纳入Pre；不得用复杂fallback宣称根因关闭；[原 v3 Pre_U5_Final_Candidate.md:25](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L25) |
| PU11/G25 | 所有实际Pre改动闭包明确 | restricted Lua/package/闲置work和新observerremove检查；不改变GC | L2/L3按风险；真实模块组合；继承失败/未测保持，不拼全绿 | 最小load/turn/idle及changed路径；无CPU/RAM/%KPI | 完整P3留O7；未审新采集器不投产，不将局部PASS写全局PASS；[原 v3 Pre_U5_Final_Candidate.md:26](../Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md#L26) |

## 可回退与相容边界

每PU是独立小提交及对应结果记录，Runtime Impact写清事实真正复用、事件范围、最坏扫描/重复计算、cache容量寿命、依赖、恢复触发和针对性门禁。普通机械选择由Primary完成。

- 未触及保存/native结果时可在受审源码和相同初始fixture间回退比较；有持久提交／扣款／创建／收据后，不能单靠切旧代码宣称安全回退。
- 保留原exact SQL IDs、历史与已签条款；新R来源元数据需向后读取旧合同，不能补造旧 provenance；破坏式迁移须Owner决定。
- optional observer先明确shutdown／absence边界，生产错误不能只在trace。关闭／移除不改变返回值、写屏障、恢复责任或GC策略。
- 首次删部署文件之前两个工具完成受审removed-set与receipt/rollback；Pre无必要时不为了练习删除旧文件。

## U5与Option B

U5是**迁移前行为基线**，不是原S9/S10、可靠-only网络、R2/R3、D1/P3的结项。已有四专业／route／合同的具名用户结果只按其范围继承；补changed路径和明确尚缺证据，不重复全轮测试，不要求随机掠夺／商人死亡／易主玩法。D1及旧冷例外在O3正式cutover前按当前合同保留。

全链顺序见[Option B计划](Option_B_Final_Candidate_Plan.md)。所有代码、测试、正式同步和部署均尚未授权；本轮不运行上表任何LOCAL／USER_NATIVE。
