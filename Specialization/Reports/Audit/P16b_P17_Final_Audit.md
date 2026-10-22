# 独立审计最终报告：继续扩展前的公共返工风险

Audit IA20261007 / W22 / P16b–P17。State: **AUDIT_COMPLETE_WITH_EXPLICIT_LIMITS**。

这是当前四专业与公共基础设施的范围限定静态／定域复现审计，不是项目运行总PASS、正式Architecture、Design决定或修复授权。主任务与独立只读子审阅交叉核证；不宣称外部机构认证。全部审计产物和确切来源在[ledger](Specialization_Independent_Audit_Ledger.md)。原finding和已完成阶段原文保留，本文负责去重、排序及证据限制。

## 最值得先处理什么

**继续增加长期状态writer之前，最有依据的是收窄保存层的每写全记录引用检查。** 当前真实Store按N/T=8/8、20/20、40/40有64/400/1600次引用检查访问，N/T=40/1为40。计龄城市均ACTIVE I，合法增长不要求同时40个高级总督。多换一块carrier或多跑GC不能消除此结构成本。

下一批公共改进应围绕真实依赖者处理：普通事实采集与全部建筑／诊断耦合、多consumer重复采集和手列传播、专业业务反向进入保存核心、馆藏单callback链、公开accepted input可变别名，以及每个writer的机械失败／读回合同。它们比局部能力数字或旧UI措辞更会随专业增长扩大修改面。

**没有证据要求现在整体重写，也没有依据把所有MEDIUM变成当前四专业或B168测试的统一阻塞。** HIGH问题也可能高度局部、可延期；severity和timing分开。自动GC及性能专项结项维持，审计没有重新打开长期内存调查。

## 基线与执行证据

起点develop `7de45dddba1f874ae21d2f1335bf911b485f8ab4`；最后交叉核证基线 `194a459abb4bf0e6295bacee55dd9744c57099e9`。其间项目Mod、Design、正式Architecture/Status/Workflow、tests/tools、main均未改；所有commit仅审计产物。main仍`e901a224faae1274563fae07012116543bee6759`。

登记source/live B168.195／modinfo195、L3-A实机USER_DEFERRED按当前Authority/Status保留。P01曾只读核对应receipt/目录事实；本审计后续没有从更晚HEAD猜运行包，也没有重新核验当前外部恢复包、游戏Mod加载栈或启动游戏。context186Mod/469guarded完整性检查不是语义／Gameplay／nativePASS。

实际复现使用未改业务模块／真实工具与受控native对象、临时文件系统或内存DB。Lua为已有Lupa5.5，不是Civ VI VM。原始脚本／JSON／hash及stub范围在对应报告，不以模拟计数换算native时间、分配字节或进程泄漏。

## 建议处理顺序：按返工增长和真实依赖排序

| 顺序与ID | severity / timing | 当前证据与扩展后的成本 | 最小candidate boundary与未来验证 |
|---|---|---|---|
| 1 · P06a-F01 | MEDIUM / FIX_NOW | 每个可靠计龄写都遍历N记录，T个writer形成N×T；新M/N/S历史writer会增加频率/业务耦合 | 保存层注册/恢复/reference变化维护唯一性；已验证ref的普通标量写避免全表。保留stale/readback、真实冲突及坏记录reservation。N/T独立变化＋ref变化/坏shape/写失败，不设计新的state engine |
| 2 · P13a-F02 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | 缓存定义只减少枚举，D miss仍逐B_loaded presence、GW有C×B_loaded；新internal定义也放大普通采集 | primitive事实与按需detail分离，紧凑snapshot含完整资格/availability/UNKNOWN原因，不能只给数。B/eligible-domain/W及同回合真实变更定向核，保留损坏/未支持目录判定 |
| 3 · P13a-F03 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | 三条Gameplay手列consumer链、多模块独立player scans；新能力复制注册不保证提交后收到新事实 | 先对已有三条链声明cause、player/city范围、已提交依赖与通知；保留worker筛选/全国依赖/late事实补撤销。有一个真实producer×受影响真实consumers组合即可，不先迁移全部listeners/建总线 |
| 4 · P06a-F03／P13a-Q02 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | Identity至少5文件＋Claim3文件校验；专业模型/初始化/tick进入Store，更多资产扩大中央修改面 | 明确Identity词汇/能力role和具名纯业务转换patch；Store保留提交/revision/有序转换。下一Identity或永久业务接入前核，不把不同网络role或A–G资产合并 |
| 5 · P13a-F04 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | GW callback链前置异常可越过Meaning，同内容新seq/idle不补发；更多订阅者扩大隐式顺序面 | 具名订阅及逐consumer异常隔离，ACK仍表示处理采集，不表示收益成功。下一正常GW consumer前补前置异常/等内容/新事实对照；不阻塞现有B168诊断 |
| 6 · P09b-F01 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | public accepted input可改，UNKNOWN fallback读改后对象；private Current副本安全、当前无主动mutation caller | 封装accepted input/control并保留兼容只读投影，不机械给全部查询深复制。新公开caller前核mutation/UNKNOWN fallback及epoch/ref失效 |
| 7 · P08a-F01（Q02补证） | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | Apply/Chair/Meaning的失败/readback/重入机械约定不同，简化Store fixture遮盖真实字段；W20已出现局部例子 | 明确小型操作结果、exact owned/preflight/读回/部分失败/catch-up；业务model、对象范围、舍入/成功凭据仍各自负责。按真实Storepayload和一个实际writer验证，不统一万能carrier engine |
| 8 · P06b-F01 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | 每个foreign Transfer向C_registered record定位，1/4/20/40次GetCityAt；不同于普通consumer fanout | 先以位置/可证端点收窄候选，Removed覆盖current/origin/loss/transition，Transfer早期UNKNOWN保留定域fallback。频率/native成本未知，不按mock内部遍历报C² |

具体依据：[保存边界](P06a_State_Ownership.md)、[采集与规模](P12a_Scaling_Validation_Boundaries.md)、[跨Context传播](P09b_Propagation_Boundaries.md)、[专业接入](P05b_P16a_Module_Extensibility.md)、[机械投影](P08a_Effect_Ownership.md)、[事件定位](P06b_Identity_Event_Boundaries.md)。

这些是建议修复边界，**不是实施计划已批准**。更准确的BEFORE_NEXT常是“下一个实际依赖该接口的模块之前”，不要求新能力先完成上表全部项。第一项若触及共享endpoint检查，要同时覆盖P06a-F02，不能为加速跳过无效数据保护。

功能定域证据：[Crew事务](P07c_Crew_Transaction_Boundaries.md)、[模板初始化](P03b_P10b_Industry_Contract_Runtime.md)、[Probe真实字段形状](P05a_P08b_Registration_Owned_Closure.md)。

功能定域门禁另排：**P07c-F01** Crew receipt读回在J1/J2使用来源/库存凭据前；**P10b-F01** nil存在性初始化在H1 typed知识扩展前。二者MEDIUM/BEFORE_NEXT；有真实注入反例但native silent-drop/nil未观察，不能称当前玩家重复grant或存档丢失，也不阻塞不依赖它们的功能。

## 主要state ownership合成图

| 状态层 | 权威／拥有者 | 当前/保存/退出边界 |
|---|---|---|
| index/reservation | Store collection manager | 唯一record/定位与坏记录保护；不是专业收益或整个城市历史可随意清理 |
| 逐城Game记录 | Store worker＋业务纯validator | base Identity/Potential receipts、current/currentFirst、loss/returnProof及业务字段；历史origin不同于当前native endpoint |
| working candidate／committed envelope | Store提交路径 | immutable候选/读回/revision；setter同步可见性为Q01条件风险，未证native消费者读到未提交收益 |
| 当前native事实 | Civ引擎，Probe facade及CurrentFacts采集 | Governor/人口/专家/普通建筑/当前route/works；不是永久历史，UNKNOWN不补0 |
| 可靠业务历史 | 具名业务model＋Store保存 | 模板可靠空/init/缺史/reconcilePending、Research年龄等各自合同；尚未实施M/N/R/pity不能伪造字段或类推所有归属 |
| Investment pending | InvestmentAction解释＋Store提交 | INTENT/confirmed技术证据/COMPLETED业务receipt分开；未知不盲重放不可逆单位消耗 |
| Claim timer／CALLING／receipt | Claim model/producer＋Store | native调用意图不等完成；成功证据/业务提交/marker/active调度分别维护，cold重建不重发未知副作用 |
| Crew技术receipt | Player Property动作历史 | 不是训练provenance或source两槽库存；unit grant/AddProgress为另一不可逆native阶段 |
| 可信输入/derived网络 | producer/Sender→Bridge私有accepted→derive | 当前/最近确认bounded值、epoch/version；public别名风险与复制查询分开，receive≠recursive source |
| K馆藏事实 | UI采集＋Gameplay GreatWorkFacts确认 | 当前W/X/目录/native refs与domestic索引；不等永久见闻报告；单callback链扩展风险已列 |
| caches/queues/session | 各具名module | ready/dirty/batch/pending/flight有own失效/退出；小orphan keys/cursors不等native大对象泄漏 |
| carrier／native instance | 每个业务writer、native engine | exact名单/plot flags/动态目录；carrier配置≠结算成功，exit finished≠全部session已忘 |
| UI/diagnostic mirror | 独立UI/按需readout | 只读snapshot/quote，不能反推身份/有效倍率；公共表修改、匿名teardown边界保留 |
| GC/logging | Performance唯一协调／RuntimeAudit observer | bounded记录和时机/错误锁停；不清永久Property、停原GC、由新模块再加GC |
| 外部运行包 | deployment tool＋receipt/backup | Git source不同于live；staging/target/no-unrelated-mod/recovery职责不能由Git代替 |

未来商业已签合同持续资格与新签资格分开；训练source与绑定target分开；Culture城市历史、Industry城市N/文明E/城市L、机构信誉及pity又不同。**不建议为了DRY统一长期资产/状态机/收益公式。** source/tool facade的旧名字不是可删除证据；retired定义仍承担cleanup，Store现代adapter/validator仍有生产职责。

## Hot-path合成：量纲与保护

C为实际被访问城市，C_D为本轮合法D工作集，B为loaded定义，W作品，R路线，E_net为真实展开业务edges，N/T为保存record/当轮writer；不同集合不可互代。

| 路径 | 调用频率×规模／近似复杂度 | 现有保护／worst case及证据限制 |
|---|---|---|
| Store计龄保存 | 合法local完整T更新×T writers×N引用检查 → O(NT) | 同回合cursor不重复计龄；真实Lua独立N/T反例。不测native耗时/serializer分配 |
| D采集 | miss×B presence，consumer轮巡C_D | cache≤8有界；9键轮巡可全部miss但当前合法C_D>8未证。维持MONITOR，不能用40总城强迫扩大cache |
| GW采集 | dirty/回合核对×C×B与slots/W | full确认用于排除/未知，callbacks收敛。不能删除完整性校验；normal/detail可分，非每帧全扫 |
| 业务consumer | cause→多个独立C遍历/事实读取 | batch局部共享、事件/worker筛选已有；11C等是条件调用链推导，不是每事件固定量。新增消费者前收窄依赖 |
| 网络derive | actual changed input / current事实重核 → O(C+R+U+E_net) | Current只查询已发布、不再Capture；version/cache/明确范围。真实edges与全国依赖不能全称冗余O(C²) |
| native身份事件 | 一次事件×C_registered定位 | 1/4/20/40实测visit，零无关写。频率/引擎查找代价未测，外国失效补撤销不可一刀删 |
| native载体核对 | 每writer×自身exact IDs，动态target另算 | 1720注册固定并集不是每次所有模块都扫1720；部分fail/readback协议仍需合约，不机械省所有检查 |
| UI/diagnostic | dirty/selected＋on-demand枚举 | 0.2/0.25/0.5s检查≠同频全城重算；GameEffects READ/END有界；少数匿名hooks释放UNKNOWN |
| GC | 单一协调条件/冷却/quiet机会 | 已验运行缓解保留；Lua统计非Mod独占，process−Lua不构成native泄漏。无新GC调用/调参 |

Crew6240等是setter参数表条目累计，不是序列化字节或Lua分配；dirty残留8ID、页cursor和旧flight只是已证形状，不能拼成进程增长根因。性能专项结项不要求零增长，也不因剩余归因未知停工。

## Finding登记与限制

共有**23个F登记、24个Q／观察登记**；F“confirmed”指源码缺口或明确受控条件下后果，不是23起原生事故。Q包含OBSERVATION、扩展约束和候选，不算24个已证缺陷。已知Research K01/旧业务适配/Crew历史形状不是重复new F。

| F组／ID | severity / timing | 真正证据和限制 |
|---|---|---|
| P01-F01 | MEDIUM / DEFER | 稳定ID独立保护未配置，当前pointer仍正确；非当前错选 |
| P01-F02 | LOW / MONITOR | helper schema子集，部分类型/路径反例PASS；非授权或全部schema |
| P01-F03/F04/F05 | LOW / DEFER | 旧元数据/阶段/导航文字，CURRENT与明示角色有强反证 |
| P06a-F01/F03 | MEDIUM / FIX_NOW、BEFORE_NEXT | 保存N×T/业务耦合，见优先表 |
| P06a-F02 | HIGH / DEFER | 人工bad current=true使正常B也不可读；load写0、B编码不变，正常writer产生该形状未证。是读取隔离缺陷，不叫跨城数据损坏；修面稳定、须保留valid碰撞/坏记录reservation |
| P06b-F01 | MEDIUM / BEFORE_NEXT | 原生事件定位broadcast结构，非当前native卡顿 |
| P07b-F01 | LOW / DEFER | 第二loss清origin key而current key残留；timer/marker正确、dirty/cold可清，无额外完成 |
| P07c-F01 | MEDIUM / BEFORE_NEXT | silent-drop receipt fixture仍grant/consume一次但receipt0，throw对照零副作用，重复grant0；native丢写未知 |
| P08a-F01 | MEDIUM / BEFORE_NEXT | 机械失败/readback约定隐含；partial错误可诊断，后续Audit可收敛，不是原子writer |
| P08b-F01 | LOW / DEFER | real loss形状Probe会话不forget，4carrier正确退出、load恢复；actual Probe＋Store stub，不是full/native联合证明 |
| P09b-F01 | MEDIUM / BEFORE_NEXT | public input alias条件反例；当前caller不主动改，private副本安全 |
| P10b-F01 | MEDIUM / BEFORE_NEXT | nil presence提交可靠empty，后续普通Discover不补；throw pending可恢复，newbuilding/reentry可能补，不能称永久不可恢复 |
| P13a-F01 | MEDIUM / MONITOR | 8cache轮巡反例，合法C_D>8尚未证 |
| P13a-F02/F03/F04 | MEDIUM / BEFORE_NEXT | 普通采集/fanout/单callback三种不同杠杆，不只因都“扫描/广播”合并 |
| P13a-F05 | LOW / DEFER | 普通reconcile未用明细，局部alloc未native量测 |
| P13b-F01 | LOW / MONITOR | orphan dirty8、合法空全样本清0，非native漏内存 |
| P14a-F01 | MEDIUM / DEFER | stable rename生效/赋值前中断误清marker、旧backup完整；临时tool同窗口保journal。下次stable apply/tool维护前定域处理，非当前部署事故 |
| P15-F01 | LOW / DEFER | Design导航版本标签旧，实际链接当前正确，非玩法冲突 |

Q主要保留群：setter重入未提交可见、忙碌skip后下一Audit才收敛、UNKNOWN Transfer后无loss补确认、pending×loss恢复HELD、Claim CALLING未知结果、publication共享metadata、128路线/16384字节容量、UI teardown、dirty/flight/cursor间接保留。各原ID/等级/触发和反证在ledger/直接报告，不按模块数累加风险。

特别不能升级的解释：INTENT不等confirmed业务成果；confirmed技术证据也不自动继承half receipt。CALLING写失败零调用而恢复due可合法一次调用；最终Identity提交失败不盲重放，新合法completion能恢复。多数writer内部已catch业务异常，新真实样本也可恢复；GW F04不是所有异常永久失效。

## 已接受但未实现：与架构缺陷分开

| 专业/层 | 当前真实范围／缺口 |
|---|---|
| Shared/NET | 四专业身份/Potential/ACTIVE、D/普通建筑、Housing/GPP及共同拓扑已接；部分HD目录对象PASS不等完整Mod环境目录PASS |
| Research | 六本地包已接；Network保留旧范围/重设计标记。原Owner return后的年龄OWNER_POLICY_UNRESOLVED hold是已登记Design→实现适配K01，MEDIUM/DEFER，不重新叫GameplayTBD |
| Industry | 模板init/restore/reconcile与可靠空/缺史区别已有；H/G/I/J的新holder/N/E/L/研习/Macro/Practice/队伍尚未落地。两个对应门禁已列，不称模板功能整体失败 |
| Culture | K/L1及七域五yield L2 normal AUTO已接，GWA retired；Gov/Dip Culture隔离，theming暂许可Balance。L3只有B168 probe待验；M/N/U2未实施，旧Dialogue仍动态，不能以旧positiveAUTO证明新永久M |
| Commerce | 基础/II与旧COM3＋Convergence48运行；新P/Q/R/S/T无executor。已签合同/信誉/pity/配置/团队/重组ownership已逐项对照，真实窄TBD保留，不类推统一永久成果 |
| 未来专业 | Accepted未来设计/候选/参数与v0.1scope分开；五/六专业最小中央修改面已测，不因无实现报故障或开放AI/multiplayer |

Culture精确队列Production归因、GPP fractional/effective multiplier、themingBalance等仍限定开放；native gate仅阻依赖原语，不把全部功能恢复开发挂在未归因内存上。真实Design未决仍经用户Design Talk，审计不补值、不改名字/范围/成熟度。

## A–L覆盖与审计结束的含义

| 原范围 | 本次实质覆盖 | 明确保留NOT_YET_AUDITED／UNKNOWN |
|---|---|---|
| A Authority/Workflow/Status | P01/P15当前pins、授权、selector、入口/停止点 | 完整schema/所有历史manifest语义不由check证明 |
| B Design→Architecture | P02–04完整Shared/NET/四专业合同、目标/当前矩阵 | 全部阅读版逐句/未来所有正文不重审，三处未衔接边界保留 |
| C Architecture→Mod/runtime | P05、P10/11实际组合/UI roots/normal-probe-retired/直接writers | 外部最终HD/游戏override和native加载trace未证 |
| D Tests | P12与各能力真实fixtures/assertions、local/native分层/继承 | 不运行全历史suite，不给所有native组合PASS |
| E 生命周期 | P06/P07 current Store/identity/投资/Claim/Crew/Tradition/模板、直接exit/return | 所有callback交错/serialization/native原子性；未实施业务无executor可验 |
| F Effect ownership | P08代表操作协议及全固定/动态生成与精确归属 | 三dynamic实际loaded集合、全部native结算/退出不可由静态集合证明 |
| G 性能/GC | P13主hot paths/成本反例/选定间接保留/GC职责 | 全部对象图、原生频率/CPU/分配字节/整包负载/零泄漏未证 |
| H Deployment | P14两工具事务、四临时失败场景、branch/source/runtime分工 | 当前外部恢复包、掉电/并行、所有promotion历史未复验 |
| I 历史/导航 | P15活动入口、重要反证、限定mapping/link | 全部Frozen内链/原件bytes/远端链接/截图存档不重检 |
| J 债务/复杂度 | P05/P16中央接入、纯业务/保存/传播/兼容必要性 | 不证明可安全删所有defensive/legacy层，也无整体重写依据 |
| K 已接受缺口 | 四专业current/target、K01及具体待实现清单 | 未实现不是new regression，已定不重新TBD |
| L 完成声明 | 具名结果和source/fixture/native/部署范围交叉核 | 审计覆盖不等运行通过；人工无截图仍按原USER_REPORTED |

17个逻辑领域均完成这份**限定的静态／证据／定域复现审计**所需回答；余项具体列出，不改写成PASS或声称全部文件逐行审完。交叉审阅没有发现一个仍未调查、又必须先完成才能回答当前公共返工优先级的高价值架构slice；不再用“还没审全部可能性交错”无限延长本任务。

保留NO_ACTION：永久历史、去重receipts/reservations不可为GC删；UNKNOWN与confirmed loss不同；当前/最近确认不是无限历史；legacyadapter不等双writer；retired定义仍可精确退出；foreign/late补撤销和读回不能机械去掉；Git commit、runtime hash、receipt、恢复包有独立职责。既有源/主分支/运行包隔离不重构。

## 用户下一步与停止边界

本次无需新Gameplay决定、用户补截图或额外实机长测。**下一步是用户审核上面的具体候选边界与处理顺序，再另行授权修复。** 建议首个独立小批次只处理保存层引用检查成本和必要坏shape/读回反证；其它公共方向按真实consumer接入分别推进，不把八项绑成一次大改。

B168实机仍待办，用户可按原计划选择恢复；本审计不授新实施、部署或测试。审计结束后停止，没有顺手修复任何finding或推进玩法。

最终检查：21份审计Markdown、276个本地link/anchor无缺失；current context186/469完整性PASS；非Audit tracked diff空、main未变。未重跑任何全suite或用户实机；提交身份/推送/clean状态由本次Git checkpoint提供。
