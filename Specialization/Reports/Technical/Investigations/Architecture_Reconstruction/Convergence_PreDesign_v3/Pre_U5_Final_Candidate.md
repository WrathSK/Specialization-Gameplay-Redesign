# Pre-U5 Worklist：final candidate，未批准执行

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[门禁／决定包](Owner_Gate_Stop_Report.md)｜[完整O计划](Option_B_Final_Candidate_Plan.md)｜[源码证据](Gap_Matrix_v3.md)

Owner批准的是总体优先范围，不是任何PU实施。固定次序：决定闭环→最终计划认可→Claude Code独立只读审计→Finding逐条处置／重大问题实施前重审→Owner再次放行并明确实施授权→获批正式同步与Pre-U5→U5。本表全部root调查／测试／原生步骤均未执行。

| PU／G | 当前证据／范围 | 最小候选动作及停止条件 | 真实模块最小回归 | 后续必要USER_NATIVE |
|---|---|---|---|---|
| PU01/G03 | STATIC workerUNKNOWN→零计划；原生读取失败原因未复现；本城D/worker被动重算方向已批 | 查读取／错误归类root，禁止UNKNOWN=0；优先共享owner最后确认D/worker+新事实重算，不建Commerce私有cache。若需完整O1共享扩展，不能偷偷把O1塞进pre；临时same-ref旧效果保护只作过渡，**不能是G03/O1最终关闭** | 真Commerce+共享facts：旧值→异常→新D/worker重算；first无值；真实count减少/role/ref退出；no额外money／重复写 | 普通商业变动/读档delta，不让玩家造API失败或全量重测 |
| PU02/G26 | STATIC缺preparedA inert，USER_NATIVE B无效/A再点确认；helper未复现整套click原因 | A准备后无动作、B匹配plan确认；查tag/实例/hitbox/async，不能盲交换callback；未知原因不得宣称已修 | 实际UI/actionhelper、A/B位置、重复A/旧plan/选中单位变化、两操作、confirm一次性 | 清算/配置各一组A准备、A无效、B确认；非全业务重测 |
| PU03/G08 | STATIC signature先推进再fallibleEmit | 分开尝试与成功登记；有限责任/相关恢复；挪赋值本身不证明恢复。不得混入可靠-only发布、D1/D2全迁移或NET1/2重开 | 真Bridge+FC+bindings emitter失败→同proof登记→原consumer，samevalue availability、reentry revision、静置有界，D1/strict不变 | 普通网络恢复即可，不造native throw |
| PU04/G04 | STATIC ACTIVE断言先于D/anchor；组合fault原生未见 | 先证明独立可靠的当前negative，再窄修；UNKNOWNACTIVE不是0；旧D不能自动证明现时退出 | 真Infrastructure当前negativevs读失败、positive、wrongref、第二变化、ownedCarrier退出 | 仅changed普通资格退出，不要求随机掠夺 |
| PU05/G14 | 既有LOCAL真owner两城同级count2→0unit；native时序未知 | **先唯一完成凭据/足够强delivery契约，再grant方案**；无>prior/差值loop/位置猜source/CALLING重放。没证据则停依赖切片报具体限制 | 真Crew+Store两城订单，同/异级、重复/乱序/取消/晚到、coldCALLING、创建和保存歧义，唯一unit/source/request | 仅确需时最小两城同级参数/计数/queue见证；新探针须上限与remove设计和后续授权 |
| PU06/G29 | STATIC信誉叶unknown→effective0可入合同；H3撤回v2模式政策 | **依ODP02**：严重root错误/原bytes保留；若统一R0极端继续启用，则被动和新风险一致0，其他严格门槛不变；STABLE不加R依赖；不改旧合同 | 真Store隔离leaf+Commerce+Capital：真实0vs政策0、III/IV、两mode、parent/余额/nativeoutcome未知拒绝、prepare-confirm变更、旧结算不变 | 普通quote/confirm、必要一份受影响结算；不刷RNG/损坏存档 |
| PU07/G11 | STATIC completionError持久，target解析先于领域相关性；native未证 | 核实constructed参数、对象时机、无关district/first顺序；正常缺陷妨碍U5则精确加入。禁猜顺序/清error/新见证；后者必要性和授权单独门禁 | 实际completion/admission相关/无关、missing/late对象、owner/type不符、重复、first证据，错误可定位 | 只有特定对象时序本地无法回答才观察，不重开认领全测 |
| PU08/G28 | STATIC foreigntargetfence+夺回等所有exit；最终恢复未知 | 分清合法foreign窗口、consumer/writebug、已回归端点；不得凭保留事件重放旧cleanup。新权威须Ownerpacket | 真Store+exitowner三种时序、ref/token/parent、old/new互斥、延迟完成 | 不扩大易主玩法；必要接口另授权 |
| PU09/G13 | 真原生earlyClaim已批，Gameplay取消完整语义未知 | 只核实事件真实性；不移植NarrativebCanceled，不加内部timer门槛；真实取消误发证实再最小过滤 | candidate/ref/receipt、普通timer+真实early、重复/晚到；取消只用已核实signature | 不重复三项目核心campaign，必要一次参数观察 |
| PU10/G06 | 无总督正常KNOWN1；正常UNKNOWN未新实测 | 查CONTROL/trait/modifier/ref/初始化/publish；统一ACTIVE不分裂；不靠复杂cache掩盖。正常缺陷妨碍U5才窄纳入 | 六属性/phase/ref夹具，注入异常不是原生复现；读中变化不缓存成功 | 先已有日志/诊断，确不足再提bounded采样，不自动加 |
| PU11/G25 | 最终候选加载、work和可移除性需证据；无新速度归因 | 只验实际改动闭包/restrictedLua/package/无闲置额外深扫重写；GC政策保留。完整P3退役留O7，不虚称已完成 | 对应PU真实组合、已知失败/限制、新观察者若有须独立disable/remove；不将局部PASS拼全绿 | 最小load/turn/idle及changed组合，既有collector优先，无CPU/RAM/%KPI |

## 与U5和完整债务的关系

PU01/02/03/05/06是已批优先范围，但准确方案仍受证据／ODP／唯一proof限制；PU04证实后窄修。PU07–10不是自动批次。Crew未解不能声称D5多城支持已验收，也不能借单城成功覆盖。

U5是迁移前行为基线。普通四专业/route/合同结果按原scoped证据复用，changed路径有delta；原S9/S10、P3、D1退出和最终正常root链必须在OptionB完成，不被U5PASS抹掉。Pre最小改造不是最终设计退化为冻结/HELD。

每PU后续独立可审查提交、RuntimeImpact、对应T门禁、实际命令/环境/结果/反例/限制；机器全Closure不默认进Git。本轮没有任何新LOCAL/USER_NATIVEPASS。

停止：重大语义/保存权威/不可逆/引用边界改变→Ownerpacket；缺原生proof→停依赖包提最小证据；不得弱化assert；未完成外部审计闭环与Owner实施授权→所有PU停在计划。部署/main不自动获批。
