# P07c — 施工队来源、消费与生产注入

独立审计 IA20261007 / W12；基线 `189e8374bfee4b47bde2798aa5904ca6eafebb81`。slice覆盖完成，非总审计/native PASS；仅审计产物可写。

## 本slice回答的问题

**当前施工队训练、来源、单位消费、生产力注入和receipt各由谁拥有；新J1/J2能安全继承哪些接口？** 不实现新工业成本/容量、不重做全部队列或速度native测试。

旧运行链有明确单位/目标复核、单次消费、remaining限额与不重放不确定grant。训练来源/容量2/新成本/Wonder-only/保护撤退尚未落地，已在[Industry准备矩阵](../../Architecture/v2/Industry_Preparation.md)登记，不能当成新回归或未定玩法。

新增 **IA-P07c-F01：MEDIUM / FIX_BEFORE_NEXT_PROFESSION**：Crew的Player receipt写入无读回确认，即继续消费/注入。静默丢写注入中，消费与grant各1、返回成功文本而receipt0；抛错对照消费/grant0且HELD。没有观察到native静默丢写或重复grant。具体应在J1/J2让这些阶段参与库存/来源正确性之前补齐，不阻塞与此无关的功能。

永久receipt全表无上限是历史已知项，本轮只补传入payload规模，记 **IA-P07c-K01：OBSERVATION / MONITOR**；不重复报新内存泄漏。

## 正式规则与当前支持矩阵

[Industry D0045](../../Design/Content/Industry_D0045.json)的teams/team_inventory_capacity/professional_unit_protection及[Spec工业条款](../../Design/Specialization_v0.1_Design_Spec.md)规定实际目标。[J1/J2计划](../../Architecture/v2/Industry_Preparation.md)已经明确IMPLEMENTATION_NOT_AUTHORIZED/旧writer仍在，以下差距不重新开成Gameplay TBD。

| 项目 | 当前实际实现 | 当前接受目标 / 分类 |
|---|---|---|
| 训练项目发队 | 5个SQL completion modifier各grant1；Lua不再次grant | 可继承原语，不等于新来源/库存已实现 |
| 开放资格 | INDUSTRY/P≥1＋完整first literal Industrial Zone，5档同marker | III开I–III、IV额外IV–V，J1 deferred |
| 成本 | 280/460/820/1100/1500，旧Specs | 新150%/IV按真实Wonder N降至140/130/120%，J1 deferred |
| 训练来源 | 没有项目→新单位可靠绑定、source token、unit identity/original Owner ledger | 当前source Owner存活队伍2槽，所有档各1；J1技术门禁 |
| 来源下降/退出/易主 | access marker撤销，已完成单位使用不再查来源资格；不删除队伍 | 独立原Owner资产方向可保留；新Owner槽/原Owner夺回重计未实现 |
| 消费/容量释放 | Destroy与Player动作receipt；无来源slot writer | 消费/合法移除释放，活着撤退不释放；J1 deferred |
| 施工目标 | Buildings/Districts，包含Wonder | 现行Wonder-only、Megaproject未来不开放；J2 deferred |
| 施工量 | floor(档位×speed/100)，min剩余量一次AddProgress | 新能力要求locked基础量、无普通buff放大、无overflow；源码输入相符不证明所有原生结算 |
| 冷加载 | access marker重算，不replay grant；单位由引擎保存 | 来源inventory恢复没有实现，不能以普通单位存在推补来源 |
| 非捕获/保护 | civilian/1charge/CanCapture=0 | 该字段不等于不能被敌方捕获/摧毁；保护撤退/安全回归writer未实现，J2技术门禁 |

以上为已登记的设计适配缺口 **K02 / DEFER，分别在J1/J2实施前处理**。本轮不认为当前已有J1/J2测试PASS或需要推广旧源码，也不删旧合法单位。base-IZ literal检查未归一unique replacement family；专用白板文明下原生可达性未建立，只记录当前支持范围。

## State / writer map

| 状态 | owner / 真正用途 |
|---|---|
| 项目→生成单位 | [Data/CrewProjects.sql](../../../Mod/Data/CrewProjects.sql)精确5个native grant；[CrewProjects](../../../Mod/CrewProjects.lua)仅管理入口marker |
| 实际单位/1charge/owner | engine；[UnitActions](../../../Mod/UnitActions.lua)Confirm重新查当前资格、位置和单位，不从UI高亮授权 |
| prepared plan | UnitActions session，每player一个；turn/target/cost/progress/amount；Confirm先移除，重复不能重用 |
| SPC_CREW_RESERVED | 单位操作reservation，防再使用；不是永久训练来源 |
| SPC_CREW_ACTION_RECEIPTS_V1 | Player技术动作历史：request token→stage/numeric unitID/target cityID/target/amount；不是source-city provenance或库存 |
| native queue snapshot | [ConstructionProbe](../../../Mod/ConstructionProbe.lua)当前owner/target＋HD UI helper cost/progress，读取前后核一致 |
| 精度读数 | [CrewPrecision](../../../Mod/CrewPrecision.lua)仅最近动作前后观察，UNKNOWN/差值不改业务结果或重放 |
| access marker | CrewProjects当前派生事实；module-owned exact退出，无ordinary/永久history清理 |

实际链条：Prepare→复核→INTENT→unit reservation读回→Destroy/缺失确认→重新读目标→GRANT_ATTEMPTED→AddProgress(min)一次→COMPLETED。`busy[pid]`阻同请求重入；结果不明HELD，不自动恢复注入。

[Probe](../../../Mod/Probe.lua)14–22统一已接受速度Floor；不同速度显示/执行使用同一整数。ConstructionProbe7–24要求finite合法cost/progress、明确目标类型、HD helper及owner/target读后复核。UnitTargets再次匹配单位所在目标地块。native modifier是否扩大实际效果不能只靠min推断。

## Confirmed — IA-P07c-F01

**Player receipt安全门禁只有setter不抛错，没有持久读回。**

- UnitActions118–120直接更新整张Player receipts并调用P.SetProperty；没有old-value/shape/clone/readback确认。
- INTENT122之后开始reservation/Destroy；GRANT_ATTEMPTED128之后立即AddProgress；COMPLETED130也没有读回。
- Probe554只转发setter并计数，不负责确认。与P07a的Store/IA阶段读回不同，不能因为同一底层Property方法就继承其保证。

| 当前实际Lua＋明确故障fixture | Player receipt | 消费 | AddProgress | 输出 / 重复 |
|---|---:|---:|---:|---|
| 正常 | 1 | 1 | 1 | CREW CONSUMED；重复grant0 |
| 所有receipt setter静默drop | 0 | 1 | 1 | 同样成功文本；重复grant0 |
| INTENT setter抛错 | 0 | 0 | 0 | HELD；重复grant0 |

fixture Player getter返回deepcopy，避免表别名掩盖丢写；reservation与单位/目标操作不丢弃。**LOCAL结构证据确认的是缺确认门禁及条件后果，native silent-drop尚未观察。** 不能说实际玩家已丢记录、重复发放或原生grant金额错误。

Severity **MEDIUM**，timing **FIX_BEFORE_NEXT_PROFESSION**：尤其在J1/J2把receipt作为来源库存释放/恢复凭据前。当前保护仍有plan consumed、单位reserved/不存在、token历史、busy及不重放；它们限制重复副作用，却不证明receipt确已保存。未来新模块如果照抄“setter不抛错即持久成功”，会复制保存责任错误。

最小候选边界：Crew自己的record写核旧值/结构及读回；不可逆debit/grant前持久阶段必须确认；grant之后写失败保持明确不确定结果且绝不重放。不得只通过统一文案抹掉未知，也不统一Invest/Claim/Crew的不同成功证据，不新建万能transaction engine。未来验证用targeted drop/throw、Destroy后目标变化、AddProgress已生效后抛错与重复确认；不是重新要求所有生命周期人测。

COMPLETED只是正常AddProgress返回后的业务阶段，不等于已测精确native收益。[B042执行合同](../Technical/Specialization_B042_Crew_Unit_Actions.md)16明确不承诺引擎原子性/完备恢复；[B046观察合同](../Technical/Specialization_B046_Project_Precision.md)保持observer独立。保留这些反证，F01不以阶段名字制造误PASS。

## Known observation — IA-P07c-K01

[历史性能审计](../Technical/Specialization_Performance_Audit.md)177已经记录每次施工新增永久token、无固定总上限。本轮不是首次发现，也不归因之前进程增长。

成功N次动作，表保留N个receipt；每次3个阶段把整表传给setter。最小实际Luafixture得到：

| N | receipt数 | receipt setter次数 | 累计传入receipt entries |
|---:|---:|---:|---:|
| 1 | 1 | 3 | 3 |
| 8 | 8 | 24 | 108 |
| 64 | 64 | 192 | 6240 |

口径：最后一列为各setter参数表中条目数的和`3N(N+1)/2`，**不是实际Lua遍历/分配、引擎序列化字节或native耗时**。Source本身未遍历历史做计算，mock deepcopy成本不能冒充生产成本。条件性worst case是引擎每次处理完整table时历史成本增加；当前引擎实现/频率未测。

**OBSERVATION / MONITOR。** 在来源registry/新长期action接入前明确历史布局和去重保留责任，按证据补足预算；不能为内存图好看删除永久/不确定凭据。目标Architecture已有reviewed retention/tombstone要求，可复用，不新建telemetry或backup index。DEVspawn集合另属手动实验，不把它当正常训练来源。

## 复现、已有测试与原生证据

[最小脚本](Evidence/W12/reproduce_crew_receipts.py)／[原始JSON](Evidence/W12/crew_receipt_result.json)：3故障/对照＋N=1/8/64 history形状；actual Probe/ConstructionProbe/UnitActions，native单位/HD reader/queue/Property为mock，UnitTargets为明确目标stub；existing Lua5.5，不执行历史case、不安装、无游戏/数据库/runtime操作。结果pin源码/脚本hash。

三指定测试均HISTORICAL_OR_MODEL，旧路径及precision167.5不作为当前回归门槛；后继integer-speed已有Floor断言，不能为当前绿灯改写旧测试。它们确有正常消费/min/重复/位置/charge/turn/precision反证，但没有receipt drop、native effect/overflow或来源库存证明。

只读继承[B039用户DEV注入结果](../../Status/Validation/Results/Specialization_B039_User_Result.md)、[B042正常Crew用户陈述](../../Status/Validation/Results/Specialization_B042_User_Result.md)及B046限定整数观察；未重看截图。它们不证明新增来源/容量或当前未知故障窗口。源码min不外推所有原生mod组合，普通重载PASS不自动覆盖不确定副作用事务。

## 已核接口与未覆盖

实际阅读：CrewProjects/UnitActions/CrewPrecision/ConstructionProbe全文；Probe金额/Property、UnitTargets目标、Gameplay执行/Start及项目/单位SQL；Industry_D0045完整teams/inventory/protection对象、Spec相关节、J1/J2准备计划与B164工业盘点；3历史Crew测试/后继整数断言与具名结果/历史性能条目。无全Mod/全部历史/外部HD通读，截断检索不计全文。

未覆盖：真实项目完成新单位唯一来源匹配、捕获/撤退/安全返回接口、合法单位Owner消失、native setter失败语义、任意AddProgress multiplier/overflow、新库存冷加载、商业与重组未来事务。原型/旧链存在不等于新设计已实施，未定义unit Owner消失保持真正Design boundary，其它已定归属不重开。

下一 **P06b：city identity的事件证据与失城/返回传播**。从Store track/observe/reconcile/manager dispatch、CityIdentityRead、FreshBindingHook/CityFlow的直接admission/reference调用进入；复用P06a保存与P07投资/Claim事务，不逐能力重验。核事件fan-out/记录生命周期、UNKNOWN与confirmed loss、证据匹配/同址新代的明确支持边界；按真实引用选E2现有fixture，不扩展AI/多人/新cityKey或实施。P07其余未落地商业/REALLOCATING合同留对应Design/Commerce阶段，不因无源码创建假实现。
