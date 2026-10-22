# P08a — 效果归属与公共载体更新边界

Audit IA20261007 / W05；2026-10-07。审查baseline `77568aa`。**Audit-only；不是正式Architecture合同，也不是修复授权。** 本slice只回答代表性效果更新协议的扩展边界，不宣称全部carrier、生命周期或原生收益通过。

## 回答的问题与结论

新增能力时，哪些“读取现存载体→撤旧→加新→读回确认→退出”步骤可以安全复用，哪些仍必须由能力自己拥有？沿前序P06a/P09b已有图检查学以致用、学术主持、意义延展及真实Store退出入口，没有重新审每项能力的完整存档周期。

**值得在更多能力复制前整理的是失败、重入和验证责任的合同，而不是建立全能CarrierService。** 三个模块都有精确ID集合和读回检查，却采用不同的部分失败、引用重验和重入策略。直接提取统一writer会悄悄改变行为。Apply/Chair的共同机械步骤可以是首个小范围候选；专业计算、载体编码、UNKNOWN和永久资产归属不应一起迁移。

本轮没有新发现要求立即暂停全部功能。一个维护/扩展缺口标为 `FIX_BEFORE_NEXT_PROFESSION`；人工注入复现的运行风险保留 `MONITOR`，没有证明它在Civ VI中发生。未改变前序 `IA-P06a-F01 / FIX_NOW` 等finding及排序依据。

## Effect ownership / source-of-truth map

源码路径默认相对于仓库根；下文行号均为本baseline。

| 层／模块 | 真正拥有的状态 | 读取与投影 | 生命周期与不可合并的职责 |
|---|---|---|---|
| Shared current facts / D / GreatWorkFacts | 各自已确认的当前输入；专业writer不是这些事实的权威 | writer用当前Identity、Potential、ACTIVE及所需D、worker、作品事实生成计划 | UNKNOWN不能直接改成零；本slice复用前序source-of-truth审计，不重做Governor/城市身份设计 |
| `ResearchApply` | 精确25个Campus载体（5 yields×5 bits）；ready/busy/errors/changes是会话数据 | 每名实际科研专家的系数；同yield先合并再floor。已安装载体每次从native读取，不保存收益快照 | worker=0时系数可继续存在，实际收益为0。失城用本模块精确集合退出；不能套Chair的worker=0清除语义 |
| `ResearchChair` | 当前已加载普通学院建筑target×8 bits；会话错误/忙碌状态 | 对具名建筑附加W Science；target由SQL与已加载Buildings交集决定 | worker=0撤销；单栋不合格只撤该栋。不是专家系数或城市总收益；实际T不能仅按候选表写死 |
| `CultureMeaning` | 精确92个可清理ID；当前每yield至多一个最终值；session records、cleanupPending、pending、writing guard | records是同引用最近已确认投影，不是永久权威；当前正常写五产出，Culture仍隔离。旧bit/实验ID只作精确清理 | 同引用UNKNOWN保留已确认配置；新引用/冷启动/不支持输入有更严格清理。真实事实重建，不能重放旧保存carrier作为收益权威 |
| `CityProgressionStore.RemoveOwned` | 已确认loss的target授权与本次退出结果；**不拥有全库carrier清单** | 模块提供exact names；全量预检定义/InternalOnly/presence，再逐项引用重验、删除、读回 | 只适用confirmed ownership loss。不是普通差异更新器；不清永久账本，不决定恢复收益 |
| native Buildings / Modifier | 实际已安装效果，可能与desired plan暂时不同 | presence/location/pillage读回用于验证 | native实例是投影结果，不是专业身份、永久历史或缓存的权威 |

依据：[Apply合同](../../Architecture/v2/P0_D2_Research_Apply.md)、[Chair合同](../../Architecture/v2/P0_D3_Research_Chair.md)、[Meaning当前合同](../../Architecture/v2/P0_L2_Meaning.md)、[E2退出合同](../../Architecture/v2/P0_E2_Plan.md)。不同附着语义见 `Mod/Data/ResearchApply.sql:2–16`、`ResearchChair.sql:2–20`、`CultureMeaningProbe.sql:865–887`。公共更新要求见[Architecture现有约束](../../Architecture/Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)，本轮仅引用，不改写。

## 实际操作协议比较

| 边界 | Apply / Chair | Meaning | 判断 |
|---|---|---|---|
| 写前读取 | 完整owned集合presence；存在项还需location/health全部可读 | 每ID检查presence；已存在且仍想保留的项再查health | 都有UNKNOWN保护；读取强度不同，不以“少读”自动替代 |
| 撤旧 | 第一项删除/读回失败即停止本城，尚未开始新增 | 每ID捕错，继续尽力清理；任何撤销未确认都阻止新增 | 都保留remove-before-add，失败进度不同 |
| 加新后确认 | 每次确认presence、Campus落点、未掠夺 | 每次确认presence、expected owner/reference；未立即确认新增location/health | 不能把某一套验证直接当所有载体通用要求 |
| 新增中途失败 | per-city pcall记录错误；已新增部分保留，下次Audit收敛 | 再尝试清空本模块精确集合，删除session计划；清理失败仍报错 | 都不是native原子事务；也不能声称Apply/Chair静默吞错 |
| Audit重入 | busy直接return，没有pending | 合并重算范围；最多一次立即catch-up，进一步变化等下个真实边界 | ordered ownership转换不进入普通重算队列；没有每城每回合一次粗限流 |
| confirmed loss | 都把精确名单交真实Store | 同左 | 已存在的公共出口应复用，不能再按前缀全城删除 |

行号：`ResearchApply.lua:47–93,138–140`；`ResearchChair.lua:47–91,124–126`；`CultureMeaning.lua:24–57,88–173,242–246`；`CityProgressionStore.lua:492–533`。

### IA-P08a-F01 — 公共机械步骤的失败／验证合同仍隐含在各writer中

**Confirmed architecture/validation debt；MEDIUM / FIX_BEFORE_NEXT_PROFESSION。** 证据是上述真实源码差异与直接测试的不同覆盖，而不是“代码相似就必须DRY”。正常收益语义并不相同；问题在于新增模块若只复制某个循环，会连同未声明的部分失败、引用和重入策略一起复制。

当前Apply/Chair最相似，机械边界主要在两个writer；Meaning是反例/对照，不能无条件迁入同一协议。若未来每种yield/专业继续独立复制，修正某类native失败或补测试需要逐writer重新确认，且“提取公共函数”容易混入行为变化。

建议候选边界（尚不实施）：

- exact-ID presence读取、删除后确认、调用方指定的新增后健康/落点/引用验证；结果必须能区分已写部分、确认失败与当前未知。
- 先明确每个writer允许保留部分配置还是要求尽力清空；机械提取和行为修复分开评审。不要承诺引擎没有提供的原子rollback。
- desired IDs、bits或最终值编码、专业门槛、UNKNOWN策略、冷启动清理、重入调度及永久归属继续由模块拥有。Store现有confirmed-loss helper职责不扩张。
- 如果两个writer的实际合同无法一致，先明确接口/验证规范并保留各自实现即可；不以“公共化”为完成指标。

未来验证应针对共享机械层和各caller的真实策略：静默删除失败阻止新增、静默新增失败/写后异常、写后读回UNKNOWN、调用方声明的落点/健康/引用检查、重复零写入、忙碌期间真实重算不被意外丢弃。不要要求每个新yield重做无变化的全套save/load实机仪式。

### IA-P08a-Q01 — 写中资格变化的重入可被跳过；native可达性未定

**条件性行为已由实际Lua复现；MEDIUM / MONITOR。** 与P09b-Q01的Aesthetic busy模式同类，但这里补充了两个实际科研writer的可核反例；最终总审计应按共同调度风险去重，不能按模块数量重复抬高严重性。

[复现脚本](Evidence/W05/reproduce_projection_protocol.py)执行未修改Apply/Chair、两份model、RuntimeWork与CurrentSpecializationFacts。native城市/建筑、EffectiveFacts、D和元数据由独立fixture提供；使用现有Lupa的Lua5.5，**不是Civ VI Lua VM/原生事件时序**。没有执行正式玩法测试套件或外部DB。

| 注入与实际结果 | Apply | Chair |
|---|---|---|
| 第一次Create成功后，fixture ACTIVE4→1并同步调用实际Audit | busy分支跳过；外层仍完成3个旧plan载体；无error、无pending | 同样完成4个旧plan载体；无error、无pending |
| 下一次显式Audit（ACTIVE仍1） | 3→0，正常退出 | 4→0，正常退出 |
| 独立场景：第二次Create在写入前抛错 | 1个已写carrier保留，记录错误 | 1个已写carrier保留，记录错误 |
| 取消故障后的下一Audit | 恢复完整3个，错误清除 | 恢复完整4个，错误清除 |

四个场景的结果见[原始JSON](Evidence/W05/projection_protocol_result.json)，包含实际读取源码、fixture及最终脚本SHA256。Chair使用两个代表target，因此4只是此fixture所需bit数量，不是正式所有建筑配置。

第二组只证明部分失败的当前策略，不证明它违反一个已存在的全有或全无合同。第一组证明“只要真实资格在busy内部同步变化，该通知不会被保留”；没有证明原生正常运行会出现这种顺序、持续错误收益或存档污染。若后续功能新增这种同步调用，或出现真实missed update，再定域升级。不能将其写成已发生的游戏漏洞或当前全项目阻塞。

## 定向测试覆盖与真实边界

| 现有证据 | 已覆盖什么 | 不能由此推断什么 |
|---|---|---|
| `test_research_apply.py:28–40,58–60`；`test_research_chair.py:24–49` | 当前资格、floor、worker0差异、UNKNOWN保持、正常撤销恢复、重复零写入；Chair多配置/两城解码 | 共享`test_p0_c.py:19–33`创建通常立即成功且健康、位置确定；不覆盖本轮写中资格重入、第二次新增失败或silent no-op/readback UNKNOWN等写中故障 |
| `test_culture_meaning_automatic.py:107–141,159–185` | 同引用UNKNOWN、新引用清理、owner改变、silent remove、残留阻止新增、有界重入 | 不代表全部create故障已测。旧probe `:845–874`的Create no-op/after-write异常不能升级成正常writer覆盖 |
| Meaning automatic继承Aesthetic fixture `test_culture_aesthetic.py:103–107` | 模块退出接线/范围 | fixture Store简化了loss匹配、InternalOnly预检、逐项引用重验/读回；不是实际Store×Meaning联合验证 |
| `test_p0_e2_exit.py:22–39,45–103,123–137` | 实际旧模块精确清单不重叠，真实Store错误target/UNKNOWN/永久账本与普通建筑保护、重复退出、独立模块失败和3次上限 | 模块表不含CultureMeaning；native删除总是成功，整回调抛错不等于删除循环中途故障。历史fixture和新Meaning测试不能直接拼成全闭环证据 |

**IA-P08a-Q02：真实Store×Meaning及写中故障的联合覆盖缺口。LOW / FIX_BEFORE_NEXT_PROFESSION**（或更早修改该共同出口时）。这不是确认的退出故障。Store仅检查单模块名单内重复，跨模块排他性由声明与定向检查保证；旧集成测试漏掉Meaning，下一接入应补当前声明的碰撞检查，不能因此创建全局长期registry或使用prefix推断归属。未来只补真实边界的定向fixture，不要求用户再测全部永久资产/冷加载。静态已核Store完整preflight、逐项target/readback、模块级隔离与有界重试，不因为fixture简化就否定已有安全机制。

## Hot-path补充：归属精确，不等于更新成本已经最小

只补充既有 `IA-P13a-F03/F05/Q05`，不创建重复性能finding。以下是源码loop/接口调用量级，不是native耗时、内存分配或游戏每回合实际次数。

设C为本次被访问城市数，T为实际已加载Chair targets，H为现存owned载体数，E为实际投递到该listener的相关通知数。已知inactive计划也可能走清理检查；UNKNOWN在更早层抛错时不会到达这些读取。

| 路径／触发 | 每次数据规模与近似成本 | 现有保护与worst case |
|---|---|---|
| Apply / Chair正常Audit | Apply至少25次presence/已访问城，加存在项location/health；Chair对应8T。总量约O(C×(25+8T))，另有facts/D成本 | RuntimeWork限制支持player、过滤内部建筑通知；Audit仍按该player枚举城市，未使用city粒度。无变化不重复写，但仍读；T源码候选13并不等于实际13 |
| Meaning scoped或fallback Audit | 每访问城先遍历92个清理ID；当前想保留的最终值再作少量检查；O(C×92)，另有facts/works/D | 支持city范围、own-writing过滤、精确四家族事件过滤、bounded catch-up；一次world startup退休清理是另一路，不能计成每事件全世界扫描 |
| 三模块内部建筑通知过滤不同 | Apply/Chair Hook过滤`BUILDING_SPC_*`；Meaning只过滤自身/旧GWA/Dialogue/Aesthetic精确家族 | 如果native为科研载体发Added/Removed，Meaning可被唤醒检查同城，即使它是Research并最终INACTIVE；可多出O(E×92)presence检查，参数无法定位城市时可能player fallback。**真实事件次数与延迟未测**，不能按每次Create必定发事件乘算实机成本 |
| confirmed-loss退出 | 模块精确名单完整presence预检＋实际存在项移除/读回；O(K+H) | 每模块每session至多3次attempt，成功不重复；这是安全事务边界，不建议为了优化跳过UNKNOWN或全量预检 |

`RuntimeWork.lua:35–40`是**通知过滤**，不是前缀删除；不能混同。Meaning92包含历史/实验清理范围，不能仅因当前最多五个desired值就删除旧ID。任何快路径/共享snapshot建议仍须处理跨城依赖、外部native变化、UNKNOWN和退出；本slice不足以关闭P13a-Q05的全部mutation闭包。

### IA-P08a-Q03 — 退出诊断汇总不含失败尝试的部分进度

**STATIC_CONFIRMED；LOW / DEFER。** `CityProgressionStore.lua:517`只在整模块RemoveOwned成功后保存checked/removed；若若干项已删除后失败，这次部分进度不进入该汇总。`PARTIAL_HELD`和模块error仍明确，不构成静默成功或永久记录损坏。以后修改退出报告时把数字限定为成功尝试的统计即可；不为此展开全部退出协议或新增长期计数。

## 已排除的解释与保留机制

- **按全库前缀删除普通建筑：未在所审三条退出路径发现。** Store只收模块exact names，先检查InternalOnly；名字前缀不能作为替代的安全保证。
- **所有carrier可统一成bit编码：不成立。** Meaning单一最终值来自已记录的native叠加限制；Apply专家系数、Chair具名建筑和Meaning每作品不共用计算合同。
- **Create/Remove没有检查布尔true即为bug：不成立。** `Probe.lua:551–553`只是转交原生返回，未定义bool成功合同；当前以presence等读回确认，nil返回不代表失败。
- **缺少Meaning逐次owner检查即可断言Research失城后继续发放：证据不足。** 实际退出若移除了刚创建ID，紧随presence断言也可能阻止外层继续；未证明原生交错，未伪造同城/owner路径。
- **Meaning已验证全部失败模式：不成立。** 对新增位置/健康的检查与Research不同，但没有原生错误创建证据；分别保留验证职责，不补造缺陷。
- **必须创建全局ownership registry：无此必要结论。** 当前模块拥有exact集合/出口是清楚的；跨集合冲突可由定向静态检查发现，不需新增长期状态。所审三族不重叠不等于全Mod已核。

## 实际读取、检查与未覆盖

沿此前已核入口复用W02/P06a/P09b。三个只读子审阅分工为writer行为、合同/测试、Store/SQL与成本；主任务独立核关键分支及portable四场景。

- 模块：`ResearchApply.lua`、`ResearchChair.lua`及两model全文；`CultureMeaning.lua:1–248`及MeaningModel相关完整projection/owned定义；`CurrentSpecializationFacts.lua`、`RuntimeWork.lua:1–56`；`EffectiveFacts.lua:12–19`只读接口，复现没有执行真实EffectiveFacts。
- Store：`CityProgressionStore.lua:488–539,834–847`精确出口及manager转接，复用P06a持久化map；`Probe.lua:547–554`native包装。没有重新阅读全部Mod。
- 定义：Apply SQL精确家族、Chair SQL全文；Meaning SQL的92个literal Building定义/相应代表Modifier，未把regex/static计数当加载DB结果。三个symbolic家族无重叠；Meaning Owned92与SQL92匹配（82 City Center、10 Theater），Apply25与SQL25匹配；Chair13个候选×8为104上限，实际交集T未读外部DB。
- 合同：D2/D3实施页、E2 `226–258`、Meaning current `14–22`；主Architecture `77–105`；只沿直接依赖核证，不重读所有Design。
- 测试：Apply全文；Chair `1–72`及两historical wrapper；P0C fixture `8–39`；E2 exit全文（阅读，未执行其runpy历史链/外部DB）；Meaning automatic `19–76,107–190,205–233`；Aesthetic `49–108`；旧probe `836–876`；B136的精确exit范围；B138只定位，不把spy当真实writer重入覆盖。
- 实际运行：四个隔离实际Lua注入，断言均成立，保存原始JSON；使用已存在Lupa，无安装。`context.py check P0-L3A` PASS186 runtime /469 guarded文件，仅引用完整性。审计产物语法/JSON/hash/link/diff核对，不改正式索引/hash。

**NOT_YET_AUDITED：** 全部模块carrier ownership、完整原生失败/同步时序、Actual Yield、所有consumer闭包、native分配/延迟、完整存档与事务。没有新增native PASS、无新实机请求，B168仍暂缓。

下一既定slice为 **P05b/P16a模块依赖与新增专业接入成本**：从`Mod/Gameplay.lua`的include/Start和`Mod/SpecializationP0.modinfo`注册进入，沿`EffectiveFacts`、`CurrentSpecializationFacts`、`CityProgressionStore`的专业词汇/接入注册、`NetworkInput/NetworkBridge`角色及已核RuntimeWork调用点扩读。只回答第五/第六专业需要改哪些中央边界、复制哪些生命周期以及是否有反向依赖；复用本页/P06a/P09b，不重跑本slice或逐能力native gate。
