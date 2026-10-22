# P06a — 城市持久状态的权威、写入边界与扩展成本

Audit-only / Non-authoritative。2026-10-07，source review baseline `dbac359`；Mod与W02/B168.195源码不变。此slice回答：**谁拥有主要城市永久状态，提交/恢复/失败的边界是否明确，新增长期资产会如何扩大公共保存成本？** 它不证明所有专业生命周期正确，不修改现行合同，也不授权修复。

## 结论与覆盖边界

当前production只有一个城市进度持久权威：`CityProgressionStore`管理紧凑Game索引和逐城Game记录。下游使用复制结果及具名写API；没有发现活跃的第二个canonical进度writer。ACTIVE、Network和carrier不作为永久恢复真值。旧City保存路径在正常Start被明确拦截，不能因代码仍存在就认定双写。

实际Lua定向复现确认两项结构问题：逐城计龄叠加每写全记录引用检查形成乘积成本；坏record的部分字段能突破单城故障隔离。另确认了注入setter回调中的未提交值可见性，但原生可达性未知。专业状态与核心保存的耦合、隐含回调阶段值得在继续增加长期资产前明确接口；没有证据支持重写整个保存系统或建立通用state/transaction engine。

P06a覆盖完成；完整E2事件正确性、所有专业永久资产、单位事务、native中断原子性仍留P06后续/P07/P10/P11。既有USER_GAME_TEST仅按原场景继承，本次无新原生测试。

## Authority与state ownership map

当前合同：Architecture总文档51–59；E2计划B108合同768–779、B109修正804–810、B140模板1292–1300；Shared_D0045完整`LONG_TERM_STATE_LIFECYCLE`81–167；Industry_D0045 `template_knowledge`427–447。目标Adaptation23–42不可当作已落地schema。E2旧阶段的范围/待授权文字不是今日授权，当前批次仍按Authority/Status。

| 状态 | 唯一owner／存储 | mutable mirror与调用边界 | 恢复、失效、退出 |
|---|---|---|---|
| 城市索引与分配序号 | Store；`SPC_PROGRESSION_INDEX_V3` | 私有index、positions；index项保留origin/serial；没有新的通用cityKey | `copyIndex/loadIndex`；缺索引仅合法start-enabled初始化；损坏共享索引/有效引用碰撞整体hold |
| 单城Identity、首次完成、投资、所有权证明 | Store；`SPC_PROGRESSION_CITY_V3_<token>` | worker.root、manager.envelope是有主从关系的运行镜像；Game slot持久化；Base/Investment复制并投影current引用 | origin和receipt不改为新CityID；current/currentFirst另存；确认loss→HELD；未知不补造；写失败hold目标worker |
| 工业模板与初始化凭据 | 同一逐城记录；Standardization解释业务 | Read/WriteTemplates；模板与INITIALIZED/reconcilePending同次提交；外部不取得root alias | 首次UNINITIALIZED允许当前事实初始化；可靠历史并当前建筑集合；缺损不能伪装首次；接收方网络模板不是本城历史 |
| 科研年龄 | 同一逐城记录；Store调用ResearchTradition模型 | 首次P4与receipt同次建立；只有Store计龄；Effects/诊断只读 | ACTIVE变化不改变年龄写权；0/1可靠区间、缺口暂停；当前Owner旧暂停分支见已知缺口K01 |
| Claim计时／完成receipt | 同一逐城记录；ClaimProjects经具名API提交 | ClaimState复制；views/active/dirty/syncAck是调度/显示状态 | 计时不是独立UI存档；完成提交身份/receipt并清timer；本slice没有重新验全原生项目生命周期 |
| native/current事实 | 原生Owner/ref/token/Governor；EffectiveFacts组合当前与永久来源 | 无持久ACTIVE快照；基础事实与投资读结果是副本 | UNKNOWN不当NONE/0；每次active检查记录stage/真实引用/绑定；失城后重新计算而非重放旧效果 |
| exit/return注册与结果 | Store协调；各module拥有精确carrier/cache出口 | callbacks、finished/attempts/exitErrors/exitReads是session状态；单模块有限尝试 | load后重新核目标/撤销；Network先退出；returns目前是提交前回调，见Q02 |
| transition与新城候选 | Store session临时状态 | 每种native event最后一份；transition/conquest/foundation固定槽；pending成功后移除，失败候选保留 | 不在load补造缺失事件链；pending上限map plot count，非无限重试队列；失败候选是否需要更细退出留P13b |

直接消费者：CityFlowProbe126–135、EffectiveFacts15–57、InvestmentAction38–59/121–129、Standardization31–43/119–141、ClaimProjects19/32/113–115/147/162–167、ResearchTradition44–48、ResearchTraditionEffects28/78。Store153–166、273–275、324–325对外复制。旧Binding/Journal/Flow writer guard和production BlocksLegacy（Store908–909）禁止fallback；Gameplay786–792不启动旧CityInheritance。

### 提交和恢复的实际顺序

- 新城：index reservation读回 → City token读回 → record读回。中断留下reservation，重载held，不回退legacy或假造完整空记录。不是跨原生调用原子事务；现行合同明确接受失败暂停。
- 已有城：验证输入 → 先替换worker.root副本 → 检查manager旧值和Game旧值 → 全记录current引用唯一性检查 → 写Game/readback → 更新envelope副本。失败后worker锁停；不自动重试原生副作用。
- load：验证index，逐entry复制record并创建worker；worker完整validate；之后共享reference检查。F02指出后两步对坏端点的隔离缺口。
- 失城：可靠事件与live ref一致才保存loss/HELD，按module出口撤销。返回先验证身份链/已撤销状态，再调用returns，最后提交ACTIVE/current。返回期间的当前效果重算依赖后续正常事件/flush，不能把RegisterReturn当成已提交通知。

## Confirmed findings

### IA-P06a-F01 — 每次永久字段写入重复检查全部城市引用

**MEDIUM · FIX_NOW（建议在继续接入长期计龄/合同writer前处理，不构成实施许可或全项目停工）**。证据：STATIC_CONFIRMED + LOCAL_STRUCTURAL_REPRODUCTION。

Store `storage.Write`676–694无论current引用是否改变，都会在684–687遍历全部`envelope.records`。科研计龄171–182、820–824为每座有有效传统的城每个本地回合保存一次；原B108仅有稀疏“meaningful writes”的O(C)保护，现已进入持续积累热路径。设N为已保存记录数，T为本轮实际计龄写入数：仅该唯一性检查就访问N×T条记录；N包括保留的HELD历史记录。读取/写入各自还复制、校验整条目标record，成本随本城已存历史体积增长，但不复制整个帝国记录。

| fixture记录N | 计龄T | 本回合record writes | 实测唯一性loop访问（含自身） | 推导的其它引用检查T×(N−1) |
|---:|---:|---:|---:|---:|
|8|8|8|64|56|
|20|20|20|400|380|
|40|40|40|1600|1560|
|40|1|1|40|39|

全部城市ACTIVE1，年龄仍正常增长，故此工作集不依赖同时配备40名总督。重复同回合：额外write=0、额外唯一性loop=0；**仍有worker遍历/读取/模型计算**，不能报告重复工作全部消失。没有测原生耗时、分配量、存档大小或用户实际N/T；不将1600次Lua表访问称为已发生卡顿。

候选修复边界：只在有证据的reference变更/注册/恢复边界验证或维护唯一性；普通已验证身份下的标量更新不重复全表碰撞扫描。保留stale Game记录校验、损坏隔离、UNKNOWN和引用冲突，不按“每城每回合一次”压制真实变化。不需中央通用调度器。现在主要改Store内部约束及定向测试，更多独立长期writer继续依赖该协议后，切换和验收面会增加。

未来修复验证：相同有效输入记录/写入结果不变；N/T独立缩放；同回合真实更新、同回合重复、loss/current重绑定、重复引用、stale写、坏索引/record、保存读回失败及跨城隔离。不要只测总写入数而漏掉内部遍历。

### IA-P06a-F02 — 单城坏端点可扩大为共享authority失败

**HIGH · DEFER（局部故障隔离缺陷；修复面稳定，无需为本次审计停工）**。证据：STATIC_CONFIRMED + LOCAL_STRUCTURAL_REPRODUCTION；不是已发生原生存档损坏的报告。

`loadIndex`731–740浅校验origin/base/token后把row放入envelope，worker restore481–485会完整validate并hold坏record，但坏row仍参与742–745的共享refs处理。若只把A.current设为boolean，worker拒绝A之后，共享检查对boolean取owner会抛错；外层757转为collection fault，正常B也不可读。对照只破坏A.revision时，B可读。两例均无load写入，B的mock记录编码不变。

有效record之间真正的引用碰撞应整体hold，这是既有合同；这里是**不构成合法reference的单城字段损坏**被未隔离地再次解引用。E2 B108779承诺目标record故障不停止无关record，不能把revision样例通过扩成所有结构损坏都隔离。现有B108测试114–115只破坏revision，没有覆盖坏current/loss端点。

候选修复边界：load时把原始/已验证endpoint/隔离结果清楚区分；共享碰撞检查和后续write扫描不得直接消费无效endpoint。不要把坏record删除、重新初始化、回退旧历史或跳过真实碰撞。有效索引与origin仍保留，以便阻止位置重复登记。未来验证包含坏current/loss各shape、重复有效引用、缺record reservation、对照城读写与冷加载、坏索引整体hold；不要求用户人为破坏实机存档。

### IA-P06a-F03 — 专业记录扩展与保存核心的耦合逐步增加

**MEDIUM · FIX_BEFORE_NEXT_PROFESSION**，并应在下一种永久资产接入前明确同样边界。STATIC_CONFIRMED；当前四专业不是错误实现。

Store同时处理通用binding/record读回与业务字段：直接调用ResearchTradition.Validate/Begin/Advance（95、181、254–261），嵌入其loss状态（600–601）；模板首次完成/Claim设置初始化标记（314、342），返回反向调用Standardization.ValidateRetained（572–579）。未来每个年龄、合同或研习模块若照抄，需要修改共同validate/初始化/投资/退出/返回/调度多个位置，扩大共享保存回归。

此外支持名单分散于Store24、CityIdentityRead65、EffectiveFacts5/24、ClaimProjects9–10、Probe5–6、NetworkInput45–46。Store105–110仍构造旧TOKEN/JOURNAL/FLOW结构借Preview校验；只扩展一个专业映射不能贯通读写。**这些名单并非全部同义**：支持Identity目录可共享，Network角色/Claim支持/业务能力资格不能机械合并。

候选边界：保留Store唯一保存和原子提交权，明确专业纯模型的验证/初始化/有序转换输入与返回patch，拒绝任意WriteRawRecord；普通身份词汇与业务角色分开；旧Preview保持历史适配职责。依据当前合同，不推荐建立通用state/ability/transaction framework或自动生成所有专业规则。

未来验证：四专业既有记录逐值保持；未知专业仍拒绝；批准的新专业经过完整调用链；新增字段在claim/投资/load/loss/return中保留；不同资产A–G语义不得合并；过期副本、读取隔离、写失败暂停和业务原子性不回归。

## Provisional与保留边界

| ID | severity / timing | 证据与限制 | 下一最小区分／验证 |
|---|---|---|---|
| IA-P06a-Q01 提交前候选root可读 | MEDIUM / MONITOR | save160–164先换root；active138–151不检查writing。注入丢弃模板写的setter hook时，ReadTemplates读到尚未持久化的模板；写后失败则读取hold。真实引擎是否同步触发此reader/效果consumer **NOT_ESTABLISHED**，未发现原生泄漏收益 | 新增同步提交回调前明确提交可见性；定域核对真正setter→callback链。有需要才提出native区分；目前无用户测试要求 |
| IA-P06a-Q02 return回调阶段和注册顺序隐含 | LOW / FIX_BEFORE_NEXT_PROFESSION | returns在ACTIVE/current提交前执行；Standardization只排队169–170；CultureAesthetic253/Meaning246立即Audit但另有CityTransfered监听。Gameplay先Store再consumer；部分注册是if store静默跳过；TraditionEffects89–91明确依赖更早Store listener | 区分pre-commit invalidate与post-commit facts-ready；组合入口验证依赖。未证明当前顺序漏效果，不要求全生命周期重测；交P09b核传播闭包 |
| IA-P06a-Q03 pending/历史record增长边界 | OBSERVATION / MONITOR | 成功候选移除，失败候选保留至session结束；map plot cap；永久历史不自动删。没有无界retry队列证据；城市销毁/位置复用仍明确未支持 | P13b按内容和间接引用检查实际保留；不得为内存删历史或发明毁城语义 |
| IA-P06a-Q04 读取名称与错误诊断 | LOW / DEFER | ReadTemplates264–269可做legacy capture写，但production Found/Acquire和Import均置captured，不是正常持续写。坏/缺record载入时原getter/浅校验reason可变成REGISTRATION_INCOMPLETE | 触及该兼容边界时分离纯读与capture或明示；保留原错误原因。不扩大当前重构 |

## 已知设计适配缺口与排除项

**K01：科研失城/返回旧暂停不是新TBD。** Shared_D0045 A类及Research_D0040已经规定年龄随city、unsupported owner休眠；当前Store601和ResearchTradition.Advance仍保存/保持OWNER_POLICY_UNRESOLVED，Effects只接受COUNTING。既有[B164落地审查](../Technical/Specialization_B164_Implementation_Landing_Audit.md)40/96/137已记录同一缺口。本审计静态复核仍存在，归为MEDIUM / DEFER的局部已接受设计适配；不重复创造新Design问题、不深挖全部能力，也不把历史F合同覆盖最新Design。涉及该路径的未来实施必须遵循当前来源。

排除/NO_ACTION（仅限所查边界）：

- root/envelope/Game副本有不同职责；复制隔离不是第二权威，也不能为省分配删除必要隔离。
- index reservation先写是明确失败保护；不自动补空record，不假承诺任意native崩溃exactly-once。
- 现代getters为positions→worker直接寻址；没有每次facts读全城district。
- 现代普通record写没有复制/重写整个collection/index；F01仅指共享引用检查成本。
- legacy writer存在不等于production在运行；旧导入adapter只供历史fixture，不承诺旧档兼容。
- A–G长期状态合同不同；REALLOCATING尚未接入的P-1不能用旧1+receipt count模型直接实现。当前无该动作，不算当前减P错误；未来为明确实现前置约束。
- 未见全局scope getter里自动运行完整UI/native诊断；E2 NativeDescribe为按需请求。pending、诊断、永久历史数量不能相互替代当作泄漏证据。

## 复现、来源和阅读记录

[最小实际Lua复现](Evidence/W03/progression_store_reproduction.py)与[原始结果](Evidence/W03/progression_store_result.json)。脚本只输出JSON，默认从脚本位置定位repo；需要已安装Python及`lupa.lua55`，按DevelopmentTests README提供环境。不安装依赖、不访问游戏/DB/存档/外部运行包，不运行旧测试cases。

复用`test_p0_e1.py`的fixture、`test_p0_e2.py`的event/native object声明和`test_b108_e2_multicity.py`的production helper声明；显式切换production Start并适配当前真实GovernorGate的6项native-shaped properties。真实Mod保持字节不变。Lua `pairs`观察器只统计实际Store唯一性循环的yield；其它引用比较列是基于循环的推导数量，不是独立测得的原生比较计数。另一只读审阅者检查脚本与结果，未发现实质fixture错误；因此收窄了“重复扫描为0”和“持久字节”的标签，最终结果使用唯一性扫描及mock record表述。

本slice新增实际读取：

- 主任务Store1–390、420–1182（中间诊断部分仅worker审阅/本slice相关入口）；ResearchTradition全模块；CityIdentityRead1–135；EffectiveFacts；Standardization读写/验证/return、ResearchTraditionEffects读数/flush/注册、Gameplay Start与旧Inheritance停用调用点。
- 合同审阅：当前Architecture1–117；E2 CURRENT、B096/B097/B101–B103及B108/B109/B140定域合同；Adaptation13–74；Implementation Plan128–137；Spec SCOPE/ELIG、TERMS/PROG；Shared完整LONG_TERM_STATE_LIFECYCLE；Industry template_knowledge；F相关保存/效果合同。没有重读全部专业或历史。
- 消费者审阅：Store exported API真实Mod调用点，CityFlow/EffectiveFacts/InvestmentAction/Standardization/Claim/ResearchTradition及exact exit/return注册；canonical Game key只命中Store。未对每个consumer的全部逻辑作正确性复审。
- 定向测试阅读：B108多城保存/失败与B109 origin修正、B128未认领返回失败、B136 current facts/progression、B140模板、B143传统。只读取相关声明/断言；本次未运行这些历史套件，不修改断言。
- 本地检查仅上述7个fixture配置的最小复现与context引用检查；native结论、系统总体PASS、真实内存改善全部未新增。

下一slice：P09b，基于已核Network/GreatWorkFacts map，核清提交前/后事实、跨Context接受/ACK/publication、消费者顺序与失败隔离。不要重复W02复杂度扫描或每能力save/load；从GreatWorkFacts Receive/OnConfirmed、CultureAesthetic/Meaning注册、NetworkBridge accepted input/private view/public compatibility边界开始。
