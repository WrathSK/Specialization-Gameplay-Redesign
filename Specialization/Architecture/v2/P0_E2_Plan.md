# P0-E2 — 进度保存适配：具体计划

Status: AUTHORIZED / PARTIAL_IMPLEMENTATION_NOT_DEPLOYABLE。2026-09-21用户授权首段实施；当前同Owner保存链本地通过，确认退出的效果清理未完成。
Baseline: B094.121 / modinfo121，runtime source a113a6096e141112a5a7ef67453afd8cdc00ac3c。D0035 / A0161；四专业v0.1范围不变。

## 当前单人范围澄清（用户确认，2026-09-21）

当前实施只有本地人类玩家参与；AI、自由城市不启用Specialization，也不支持多人。AI/多人不增加当前依赖、测试或计划工作。此为当前配置/scope，不改写ELIG-001～006保留的未来通用资格，不把系统永久设计成Human-only；本轮Design字节保持不变。

### 已有Authority，不重新发明规则

| 路径 | 当前明确规则 | 依据 / 技术待办 |
|---|---|---|
| 玩家城失去所有权：自由城、交易给AI、被AI征服 | Identity/Potential/明确永久投资成果保留；全部本Mod效果休眠，连Lv1也不生效；不能投资，无AI专业循环或网络 | ELIG-004/005、PROG-004；需要保存与失效技术实现，不是待定Gameplay |
| 玩家夺回自己的原专业城 | 恢复原Identity、Potential和明确永久投资事实；不重新花Settler、不进入Claim；ACTIVE按当前总督、Network按当前路线重新计算 | PROG-004、ELIG-005；原城市连续性仍需验证，不以城市名/坐标单独认领 |
| 玩家首次征服没有专业历史的AI城市，有合格已完成区域 | 转移完成时一次冻结四专业去重LegacySet；提供候选Claim，可一直不选；后建区域不追加候选/不自动锁专业 | PROG-006/007；完成任一Claim锁Identity/P1，其它Claim退出（PROG-008） |
| 同上，LegacySet为空 | 无Claim，从征服完成后监听首个合格区域完成，锁Identity/P1 | PROG-009；未完成区域不入snapshot，之后完成可生效 |
| 旧档已丢记录/未知历史 | 不可把UNKNOWN当“确定无专业历史”的AI城 | 旧档初始化独立OPEN；不得借Claim补造丢失专业 |

修正上一轮讨论：原城Identity/Potential恢复与无专业AI城征服初始化早已有Design，并非必须由用户重新决定。Claim精确成本仍TBD，未来实施该入口时单独处理，不阻塞同Owner保存首段。本次用户明确的交易场景是**玩家失城给AI**；不擅自把未专业AI城交易给玩家等其它取得方式扩展成已经冻结的征服snapshot规则。

各专业明确成果的scope依然独立：Culture Dialogue累计倍率/使用时代额度随城；文化见闻及考察记录属于原Owner+来源城，原玩家夺回可按条件重新生效。Industry自身模板与实际完成Wonder归属不同，不能把当前拥有的Wonder当历史完成信用。Research学术传统的离开Identity暂停规则不等于新的征服时间规则。当前外方持有不运行能力、投资、累积工作或后台专业更新；将来引入长期时钟/合同必须显式处理未启用期间，不凭加载时差补算未经批准的成长/收益。此处不替未来合同结算/Team遗产作决定。

### 对E2计划的实际调整

保留首段“一座同Owner完整旧城：迁移→继续投资→读档”的窄授权单元，它是技术依赖，不是最终只支持永不易主。其后的计划顺序明确为：

1. 当前E2首段：同Owner进度/投资保存切换。
2. E2后续收束：**玩家失城→外方休眠→玩家夺回**的保存/效果撤销/恢复；既定Design不再标为未决，只验证实际事件和支持存档。
3. 独立征服初始化批次：**首次征服AI城**的snapshot与Claim/普通完成互斥；不挤入首段，先提出具体UI与成本边界计划。新自建城接管也须单独完成总计划剩余项。

以上均需各自审核/授权，不自动实施；无需AI自主投资、AI能力收益、多enabled竞争或multiplayer协议测试。

### 失去所有权必须真正关闭效果

只让AI不跑Audit并不充分：已有technical Building/Modifier可能仍留在城里。未来实现必须建立一次性、定域的退出清理路径，按旧/new city reference检查本Mod旧效果，撤销Local、专家支持、Network source/receiver、折扣及相关carrier；不可删除普通建筑或永久账本。清理不因newOwner未启用而提前return，也不把AI城加入常驻扫描。确认清理失败须可诊断，不能仅返回UNKNOWN就声称“全部不生效”。具体writer/carrier目录在实施时按受影响模块核对；本轮未修改它们。

外方持有期间只保留可支持夺回的最少被动身份记录/定域生命周期观察，不维护外方ACTIVE、收益或专业网络。夺回时先证明同城，再恢复当前玩家读模型；不足则技术HELD，不能把永久成果删掉或把技术不支持写成新玩法。

当前runtime `Probe.IsTestPlayer`只检查测试文明/领袖，不检查Human/local资格；这不是当前范围已被代码完整保证。后续首段要核对本地单人玩家门槛并统一路由，拒绝AI/多人启用；禁止偷偷扩展AI实现。为对退出的外方城市做必要清理而访问它，不等于给它启用专业资格。

## 1. E1结论与本批切片

E1已验证：独立Game记录可保存；Gameplay直接识别所测单次自由城转移；B094冷加载恢复单城映射。仅此原型范围USER_GAME_TEST_PASS。正式多城cityKey、收复/连续易主/征服/解放/同地重建、转移中断恢复没有普遍原生保证。

因此不把E1实验编号直接升级为全局authority。本次推荐授权的E2首段为：**一座显式选择、原Owner/引用/旧凭据完整、已经建立四专业之一的城市，在同Owner范围迁移进度并继续既有移民投资，冷加载保持结果。** 其它城保持旧路径。

这是E2的受限首段，不等于总计划中完整新城/跨Owner保存适配全部完成。后续新城首次专业、全城登记、跨Owner技术适配仍需收束（夺回Gameplay已由PROG-004明确）；不因首段PASS自动进入F。既有能力计算不改，既有收益仍由原consumer写入。

## 2. 实际读取链与必须接管的边界

| 当前模块 | 实际职责 | 本段处理 |
|---|---|---|
| BindingProbe | Game每Owner总账+City token；CityBuilt分配DEV序号（上限32） | 未迁移城保持；已登记城/位置及转移待确认范围先由新保存路由拦截，禁止当新建城再分配 |
| CityJournalProbe | 首个合格专业区域锁Identity及基础Potential1；City记录 | 已迁移城的事件/加载/故障GAP写入跳过；保留冻结来源，不双写 |
| FreshBindingHook / CityFlowProbe | 串接新城Journal；三阶段提交、load resume、SupportFacts | 新城仍旧路径；已迁移城所有写入口/resume提前跳过，避免冻结旧记录触发player-wide halted |
| EffectiveFacts | Flow基础Potential + 已完成投资凭据数；Governor产生ACTIVE | 接入唯一保存路由：迁移后只读新记录；旧路径仍服务其它城；接口输出与收益语义保持 |
| InvestmentAction | Prepare/Confirm、INTENT→单位标记/销毁→CONSUMED_CONFIRMED→receipt；load finish | 对迁移城替换读写后端与revision校验，保留单位消耗和receipt语义；旧City ledger不再写 |
| CurrentSpecializationFacts | EffectiveFacts只读外观 | 复用，验证UNKNOWN/mode不会被解释成NONE |
| NetworkInput / SampleLifecycle | 直接读旧token，Network还有“无Flow=未追踪城”分支 | 使用新路由的引用/参与状态检查；迁移有效城不得因旧Flow缺失被判NONE，HELD不得走新城默认值 |
| SourceYieldProbe | 直接读取CityFlow.SupportFacts | 迁移城改读统一基础事实，未迁移城保持；不得继续越过路由 |
| Standardization/模板及其它永久成果 | 独立专业ledger，并非全在EffectiveFacts中 | 本段不迁移模板/Dialogue等；不得声称易主后完整保存。所有权不推导 |
| CityInheritance / InheritanceShadow | 被隔离旧继承writer | 保持隔离，不调用Start/继承projection |

已完整阅读Journal/Flow/Investment/EffectiveFacts/CurrentFacts/FreshBindingHook，核对Binding写入段与Gameplay启动/分发，搜索所有直接旧key读取点。正式实施前按W0001补读精确受影响消费者，不默认全库重审。

## 3. 新保存authority：小型专业进度记录，不建通用框架

拟一个独立版本化Game Property `SPC_CITY_PROGRESSION_V1`，由一个Gameplay模块持有。本段只允许一个显式登记的测试城；后续扩容另审，不创建每帧同步或第二份可写历史。

- root：schema、revision、单城record；new key不存在不等于迁移成功。
- stable record key：由已验证原DEV token在本存档命名空间确定；仅支持本段受控登记，不宣称任意城市永久ID。
- origin/current reference、迁移来源owner/token/关键revision与来源摘要；原锚点固定，当前寻址单独保存。
- progression：Current Identity、Permanent Potential、first事实、mode；UNASSIGNED/SPECIALIZED/REALLOCATING区分。首段只导入SPECIALIZED；REALLOCATING仅合法类型和拒绝错误分支的合同，无创建Action。
- historical maximum：只记录已有证据所支持的下界及provenance，过去更高值未知，不把当前P伪造成完整历史。未来投资更新当前专业已观察最高值。
- investment：原receipt→unitUID集合、revision、可选pending；无单位/UI/carrier作为唯一authority。Potential与凭据数量必须一致。
- migration state：PREPARED / ACTIVE / HELD，与Gameplay mode及事实validity独立。ACTIVE这里指存储接管状态，不是专业ACTIVE等级。
- 专业ACTIVE不持久化，仍由当前Governor和Potential计算；数据暂不可用≠等级0。

Game记录随save恢复，不用外部文件/城市名称作key。单位删除等引擎副作用不是一次Game Property写入所能原子覆盖的，保留现有失败暂停语义，不承诺任意崩溃exactly-once。

## 4. 明确导入合同和切换顺序

可导入：当前原Owner、当前引用/token/Binding唯一匹配，Journal TRACKING、Flow DONE且逐值一致、四专业Identity及基础P1、投资receipt有效且无pending。首测优先Research P1–P3，以便在同次测试继续投资；P4可本地验证导入。

拒绝：未专业化/无追踪旧城、City记录已因易主丢失、任何pending/GAP/冲突、缺失历史、原Owner改变。**E1记录/截图/当前建筑不能代替缺失旧账本。** 有模板不代表本段导入模板；原模板继续其原Owner路径，不复制/扩散。

顺序：
1. 手动请求，读取不可变来源快照，验证资格；没有新效果，也不消耗单位。
2. 写新key PREPARED（完整目标及来源锚点），读回确认；从PREPARED开始所有目标城旧进度writer必须暂停，避免来源在切换中继续变化。
3. 再验证来源未变、目标仍同一城、无单位事务；提交ACTIVE并读回确认。
4. 统一read route切到新记录，旧City值冻结留作证据，不删除、不写回、不作为自动fallback；不发布虚假的0或重复收益。
5. 重复导入返回已完成，revision不增。PREPARED读档仅在同Owner/来源完整一致、无任何副作用时允许完成原导入，否则HELD；记录损坏、schema不识别、来源改变不自动重建。

失败后不能自动回到旧writer。切换marker与目标记录必须在同一Game值内，避免多key提交顺序造成两个authority。Gameplay初始化必须在旧writer/旧load hook可以运行之前恢复路由；恢复未就绪时暂停目标写入，不将缺读解释为未迁移。

## 5. 迁移后继续投资 / 发布

Prepare读取路由提供的同Owner事实、record revision、receipt集合；不依赖冻结City ledger判断新投资是否变化。Confirm再次验证，沿用原INTENT/单位标记/销毁确认/receipt提交顺序；每步只写新后端，保持原消耗规则与Potential上限。

读档：已确认消耗凭据可幂等完成；INTENT无法证明消耗则HELD，不自动销毁第二次或增加Potential。不放宽原单位ID复用保护。旧load恢复循环必须跳过迁移城，不能双finish。

更新后复用既有事实变化通知，只有Identity/Potential/ACTIVE或相关输入实际改变才发布。迁移前后相同事实不产生额外carrier churn；Network继续共享derived view，引用加入保存generation/revision时只在需要的事实边界失效。无hover请求、无generic pulse保存/扫描。

## 6. 易主和未支持范围

当前AI/自由城Owner不获得本Mod效果或投资资格；永久成果按ELIG-005休眠保留。本段暂未实现玩家夺回时的自动恢复，不改变PROG-004恢复规则。迁移城发生已确认移除/易主后，Game记录保留，路由变为HELD_TRANSFER；旧source资格按真实owner/reference失效退出，不继续凭旧owner激活收益。当前读取失败不能冒充已确认失效。

只识别同一坐标不足以领回历史；新Owner/收复时均不自动重锚专业账本。E1V2保留为独立实验，不在正式读链作继承许可证。对于已登记位置出现CityBuilt（可能是易主），先暂停新旧首次建立入口，不把它当从未专业化城市；本段不解决该位置后续真正新城的自动登记。

必须本地证明：目标暂停不污染同player其它城市的旧bucket，不触发误清除无关城；确认失去owner/reference时不会残留其正式来源效果。若现有consumer不能区分临时UNKNOWN与已确认退出，实施时扩充必要的明确失效出口，不能靠统一抛错隐瞒。不得将已明确的PROG-004/006～009重新列为待定；仅超出这些规则的真实新Gameplay边界才报告，不替用户补Legacy。

## 7. 最小文件范围

当前单人/仅玩家资格需核对`Probe.IsTestPlayer`与现有调用入口；只收紧当前启用范围，不新增AI/多人实现。拟新`CityProgressionStore.lua`（或相同职责小模块）；ADAPT EffectiveFacts、InvestmentAction、Binding/Journal/Flow目标城门禁、SourceYieldProbe和NetworkInput的直接旧存储判断；SampleLifecycle只在引用语义确需时改。Gameplay负责正确初始化顺序和手动导入/摘要诊断；复用现有实验按钮位置、同步旧Tooltip，不新增诊断面板。

收益SQL/carrier/Research公式/Design不变，CityIdentityMapping实验仍独立。旧writer不是全局删除，而是对迁移目标先停后切；其它城市旧行为不变。完整E2新城接管不塞入本段。

## 8. 验证：W0004 L3，仅受影响链

| 本地定向项目 | 验收 |
|---|---|
| P1/P2/P3/P4真实旧fixture导入 | Identity/P/first/receipt逐值等价；ACTIVE按Governor重新计算 |
| PREPARED/ACTIVE重复、重入、冷load、读回失败 | 单authority；不覆写冲突、不丢凭据、不自动回退旧writer |
| 移民投资/重复确认/单位ID复用/两阶段中断 | 只正确消耗一次；不确定阶段暂停；旧City ledger零新写 |
| 同玩家一迁移城+一旧城 | 路由分离，旧城正常；所有写入口/load/GAP/恢复不可漏 |
| 直接旧key读取回归 | Network不伪造NONE，SourceYieldProbe不越过路由；旧样本版本安全 |
| SAME事实与idle/重复通知 | 无新增carrier写/全城扫描/周期请求；新key状态变化才写 |
| 真实投资/Governor/owner事件 | 输入正确发布；UNKNOWN保留边界与confirmed withdrawal分开 |
| History / REALLOCATING fixture | History不等于Current，REALLOCATING不能进入NONE首次建立 |

全Lua/manifest/context、受影响收益/Network/投资/部署安全检查。无需机械重跑所有历史；针对持久中断与重复操作做有限压力/故障注入。原生版本环境同时覆盖缺少table.unpack，避免B093重复。

## 9. 实施后一次最小用户测试

一个独立测试档，一座完整旧科研P2或P3城市，另有一座旧城作为对照：按需迁移→看同样Identity/P/ACTIVE和已运行收益→用既有移民投资一次→另存冷加载→同一简明诊断确认新P、凭据数、存储来源；对照城仍旧路径。一次流程涵盖保存切换与单位事务，不要求用户手算hash或全模块收益。

不默认重复自由城实验；实际易主后的正式玩法不在首段验收。若实现需要原生特定失效证据，本地先缩小后再提出，不能把范围扩成长期综合测试。

## 10. 退出 / 回滚 / 授权

首段退出：目标同Owner记录和投资读写正式由新Game记录承担、旧writer目标零写、收益逐值一致、冷加载成功；未迁移城不退化。报告明确USER_GAME_TEST与本地模拟边界。

回滚使用B094完整包和**迁移前独立存档**。新投资后旧City账本已冻结，不能用旧包继续该档并声称无损；不提供自动反迁移。新key保留不清理，保留所有证据。

无新的Gameplay设计问题阻塞这一个受限切片。需要用户审核的是上述**E2首段scope**；跨Owner/新城/全量兼容仍未包含。通过首段后先报告E2剩余边界与下一计划，不自动进入F。

本轮只计划，runtime/Design/main/运行包均不改，无部署或Gameplay regression。

计划检查：现有context.py CLI的batch枚举尚未包含E2；本轮直接调用同一工具的check(manifest)完成全部schema/hash/authority检查，PASS（151 runtime files）。未修改工具逻辑；实施时只需将E2加入既有CLI枚举，不建立新验证器。git diff --check通过；本轮无Gameplay测试。


## B095.122 — 首段实施检查点（未完成，不部署）

用户补充：v0.1只开放Research/Culture/Industry/Commerce四专业区域；领域词汇/分派结构允许未来扩展，但本批不启用其它专业、不实施其玩法。`P.Families`四项不变；新保存导入明确只接受这四种Identity。Design/A0161不变。

### 已完成部分 / STATIC_CONFIRMED

- 新`CityProgressionStore.lua`单城、版本化Game Property `SPC_CITY_PROGRESSION_E2_V1`：原Owner/reference、基础Identity/P1、投资ledger/receipts、导入绑定证明；PREPARED→ACTIVE读回确认。不是外部文件，不以城市名作key，不是全局永久cityKey。
- 最多一个目标；初始化先于旧Binding/Journal/Flow；手动导入检查完整旧凭据且无pending。重复导入no-op，未知schema/来源变更/写入失败暂停；不补历史、不回退旧writer。PREPARED可在同Owner完整来源不变时读档完成。
- 已导入目标的Binding/Journal/FreshHook/Flow写入、GAP和load resume全部旁路；Flow.SupportFacts转读新base（SourceYieldProbe也经此路由）；EffectiveFacts从新ledger求Potential，并沿用当前总督求ACTIVE。其它城继续旧后端。
- InvestmentAction保留INTENT→单位标记/销毁→CONSUMED_CONFIRMED→receipt；目标仅写Game记录。目标故障不污染其它城市，未迁移城保留原player错误桶。Network禁止将受新路由管理的缺失旧Flow当作NONE。
- 复用两按钮：迁移进度左键旧记录只读、右键导入；进度保存左键读取新摘要。旧E1请求仍保留为独立证据入口，不作迁移凭据。
- `IsTestPlayer`加单人/人类门槛；原版UI的PlayerConfigurations:IsHuman、GameConfiguration.IsAnyMultiplayer提供静态API依据；原生Gameplay-context可用性仍需实机。未知接口fail closed，不退回AI启用。
- 无SQL/carrier定义/收益公式修改；无新周期扫描/hover request；新保存模块只在明确操作、load及城市生命周期事件访问单条记录。

### 本地证据 / LOCAL_SIMULATION_PASS（不等于Civ VI实机）

`DevelopmentTests/test_p0_e2.py`运行真实Lua保存/旧writer/EffectiveFacts/投资执行器：四专业×P1–P4共16种导入；重复/冷load；总督重算；真实旧回调目标零写；一新后端城+一旧后端城；移除旧账本仍读新记录；投资只消耗一次及幂等；单位ID复用；各写入失败窗口；PREPARED恢复/来源变更拒绝；未知schema；不接受MILITARY/REALLOCATING/GAP；迁移前后完整Network输入签名相同；无关通知不新增写；实际诊断dispatch。全Lua compile、modinfo inclusion与人类/单人门槛模拟通过。

模拟城市移除/引用变化仅证明保存为HELD_TRANSFER、保留账本和阻止旧城重新登记；**没有证明其所有实际收益退出**。HELD原Owner再出现时的Network旧view排除也仍须随退出合同收束，不等同于已经实现夺回。

### 阻塞 / 未完成项

按前缀批量移除`BUILDING_SPC_*`的尝试被自动审批拒绝（没有执行），原因：批量删除可能超出同Owner首段并破坏游戏状态。没有绕过审批、没有采用该清理路径。

随后只读确认：`ResearchApply.Audit`、`ResearchCross.Audit`、`ResearchChair.Audit`当前以`P.IsTestPlayer`过滤整个player，在AI接城后跳过；不能仅靠资格收紧宣称旧载体已退出。部分其它模块已有自己的清理逻辑，但尚未完成四专业全部效果的逐项退出覆盖证明。

本段计划§6要求确认失去owner/reference时不得残留正式效果，因此不能把同Owner模拟通过当作整个E2 PASS。当前为**可恢复的partial implementation checkpoint**，不是可部署候选。

下一最小修补：逐模块明确其拥有的实际carrier/退出入口，对受本批记录管理、确认退出的单城执行模块自身退出；不按全库前缀批量删除、不清普通建筑、不清永久账本、不恢复新Owner资格、不实现夺回/Claim。补齐相关退出/重复/UNKNOWN保持/Network失效的定向模拟，再复核已有收益消费者。需先解决上述审批边界。新cityKey/全城迁移/夺回/Claim/F仍不在本轮已完成范围。

尚未运行完整affected-consumer/部署安全验收，因为退出实现尚未完成；没有USER_GAME_TEST，没有部署。B095.122/modinfo122仅为develop未完成候选编号，外部运行包保持B094.121。


## B096.123 — confirmed ownership-loss scoped exit checkpoint

本节取代上节“退出未实现”的当前状态；旧检查点保留为历史。用户已明确授权定域退出，仍为 E2 PARTIAL / NOT_DEPLOYED，不是整体E2验收。

### 合同

仅一座显式迁移城市；CityTransfered 的旧Owner、新Owner/CityID与保存原引用、当前实际对象同时匹配，才保存 `loss` 与 HELD_TRANSFER。UNKNOWN/缺失getter/无匹配事件不确认，不清空永久进度。按模块注册的明确载体清单退出，清单全部预检为InternalOnly再移除当前存在项，不枚举全城建筑或按前缀删除。每模块成功后不重复运行；失败隔离、每session最多3次事件驱动尝试，无timer/polling；诊断列暂停模块。保存的确认在读档后仍需匹配同一目标引用，才重新执行幂等退出。

NetworkBridge先使用原confirmed-invalid发布合同撤销原Owner的完整verified snapshot（不可分割），清除source/receiver projection并通知既有consumer；不是创建AI网络，也不是局部拼造有效view。原Owner剩余网络等待正常完整verified输入重新建立，其他玩家bucket不变。

### Module-owned coverage（精确InternalOnly ID，含旧载体tombstone）

| Module | IDs | 退出对象 |
|---|---:|---|
| ResearchSupport / IndustrySupport | 3 / 9 | 专家支持 |
| Lv2Housing / Lv2GPP / Lv3Support | 9 / 32 / 12 | 住房、GPP、旧支持载体 |
| Lv3Effects / Lv4Percent | 11 / 8 | 旧文化/商业本地效果 |
| ResearchInfrastructure / ResearchCross / ResearchApply / ResearchChair | 52 / 43 / 25 / 104 | 科研当前收益及各自退休载体 |
| CrewProjects | 1 | 施工项目临时准入；不删除已有队伍 |
| HalfYieldProbe / PurchaseProbe | 32 / 2 | 手动探针的已有收益载体 |
| CopyYields | 40 | 工业copy当前载体 |
| StandardizationDiscount | 596 | 折扣目录；只清目标 applied cache，不清模板 |
| NetworkBoost | 1126 | 既有正式/整数/测试Network载体 |
| GreatWorkProbe / Dialogue / GreatWorkAdjacency | 2 / 11 / 156 | 巨作探针、对话效果、旧邻接；不清历史记录 |
| CommerceConvergence | 48 | 旧商业汇聚效果 |
| NetworkBridge | — | 原Owner snapshot confirmed invalid |
| YieldCarrierProbe | — | 两个明确临时plot flags归零 |

21组共2322个唯一ID。只读当前DB核验ID存在、InternalOnly、无重复ownership；这是目录静态覆盖，不是实际游戏安装2322座建筑。ConstructionProbe的已结算Production不是持续buff，不能倒扣；UnitActions/InvestmentAction receipts、Standardization模板、Binding/Journal/Flow永久记录保留。DistrictPrecisionProbe未自动启用，其退休载体归ResearchCross；SpecialistSupport退休载体归Lv3Support。UI/diagnostics/只读facts不施加效果，无额外删除入口；单位、城市历史与其它专业永久ledger不迁移。

### 验证与边界

L3定向 `test_p0_e2_exit.py --db <readonly DebugGameplay.sqlite>`：真实模块退出闭包+实际保存协调器；全部2322个载体模拟撤销，普通Library/其他城/永久Game与City账本不变；UNKNOWN、错误事件、重复100次零额外副作用；真实Network失效发布（下游Audit在该集成模型中为通知断言替身）、其他玩家不变、无AI bucket；冷load确认/UNKNOWN保持、单模块故障隔离和3次上限通过。继承test_p0_e2.py的四专业×P1–P4导入、同Owner投资/读档/失败恢复/旧writer隔离；全Lua编译与modinfo通过。STATIC_CONFIRMED + LOCAL_SIMULATION_PASS；没有原生移除/引擎modifier撤销USER_GAME_TEST。

未扩展：没有已保存确认且原生转移事件到达时对象尚不可读时仍UNKNOWN，不通过位置猜测身份；事件排序完整性待后续确认。确认后的目标不可读会暂停，后续生命周期事件/读档可重试。无城市毁坏重建匹配、新cityKey、夺回恢复、首次AI城Claim、全城迁移或F。重启可重新尝试幂等退出，不在save中持久化“已删载体”以免绕过实际对象核验。现有held城不因重新归原Owner自动恢复。

没有发现需破坏永久账本才能退出的模块；原生RemoveBuilding失败会暂停该模块并明确报告，绝不扩大删除范围。当前checkpoint不部署；外部B094.121与main保持不变。


## B097.124 — 原玩家同城夺回 partial checkpoint

用户接受B096后授权的下一最小段；未部署，不含首次AI城snapshot/Claim、全城迁移、新cityKey或F。D0035与各专业Design Authority未修改。

### 身份与状态

仍只接受显式迁移的一城：已有HELD_TRANSFER/loss记录 + CityTransfered的旧Owner等于保存foreign owner、新Owner等于origin local human、新ID等于当前实际对象 + 原位置 + **当前City旧绑定token等于保存原token**。不以城市名、坐标、区域反推历史。token缺失、事件不匹配、区域引用不明/多个匹配、未结束投资、前次模块退出未全部确认均HELD。返回采用一条`current`与`currentFirst`引用投影；origin/base/investment anchor与receipt保持原始历史，新投资写回时仅转换当前引用到原锚点，不改receipt。`lastLoss`和returnEvidence保存一次最近证据，不建立无限历史。

原cityID可被别城复用，因此旧writer排他范围只覆盖登记位置；其它位置不会因复用旧ID被认领。登记位置无凭据的新城仍不能恢复。第一次取得无记录AI城不会进入本路径。外方→另一外方链、丢失token、销毁重建不猜测匹配。

ACTIVE继续由EffectiveFacts读取当前Governor事实，无旧ACTIVE存储/恢复。原专业区域的当前ID通过当前完整同type区域确认，保留历史first.turn；引用不明确暂停，不选一个猜测。正常consumer沿既有CityTransfered/后续相关事件重算收益，保存模块不创建carrier。

### 永久state逐项

| State | 本段处理 | 边界 |
|---|---|---|
| 四专业Identity/Potential/投资receipts | 原Game记录保留；按新current引用读回；后续投资使用同一历史账本 | pending debit不猜测完成 |
| Industry自身Standardization模板 | 显式导入复制现有模板，之后由Standardization自己的验证/写入路径路由至Game记录；旧City账本冻结 | 已在B096失城且未保存模板的历史不补造；只暂停模板读，不阻断基础身份恢复 |
| 模板后续学习 | 正常本城completion事件仍可增加；夺回城不使用BUILDING_ADDED_RECHECK按现存建筑补录，避免AI期间施工信用 | 原生completion事件覆盖需实机；非迁移城保持旧路径 |
| Industry工程传统/Wonder实际完成、source Team容量 | 当前对应D0032永久系统未实施；不从现存Wonder或单位创造历史 | 后续专业实现按实际完工归属，Team易主仍独立边界 |
| Research Academic Tradition | 当前F未实施，无可恢复时钟/age，不补算失城时长 | 以后遵循保留age/离开Identity暂停，不从征服时差推公式 |
| Culture Dialogue / 文化见闻 | 当前Dialogue.lua是旧瞬态馆藏倍率，不是D0029累计ledger；见闻系统未实施，本轮不伪造永久记录 | 未来Dialogue累计/era quota跟城；见闻original-owner/source-city，不能统一继承 |
| Commerce合同/信誉/pity | D0032长期系统尚未实施，保留明确deferred Legacy边界，不创建/激活 | owner/conquest/Identity-loss合同与信誉仍待对应专业审查 |
| Crew永久settlement receipts | 原模块保存，不删、不重发既有settlement | 不是恢复当前buff；无新单位 |

### 临时state与Network

模块自有RegisterReturn只使当前输入失效，不施加收益：Copy/Industry generation reset；Discount样本、报价、ACK等重置并dirty；Dialogue generation/test sample与GreatWorkAdjacency sample清空；投资preview取消；D缓存dirty；Standardization仅目标新引用pending清除，其它城pending保留。都是单次已确认事件，无新timer/hover/polling。

TradeRouteProbe既有dirty signal加入CityTransfered（保持该模块拥有信号）。NetworkBridge撤销旧view，等待带当前signal的完整路线样本；迟到旧signal响应被拒绝。没有把保存的旧routes/ACTIVE/收益作为恢复权威。新Network仍由既有Capture/derive产生；不建AI bucket。按现有player-wide sample合同清缓存，不永久删除其它城市账本或收益。

### 本地验证

L3相关范围，`test_p0_e2_recapture.py`：真实保存/EffectiveFacts/InvestmentAction，P3→失城→新CityID88/区域ID99夺回→当前总督ACTIVE1/3→冷load→继续投资P4→再次loss/return；原base/receipts/binding逐值保留；100重复夺回不增revision；错误Owner/ID/token/首次取得/未完成退出/未完成debit拒绝；旧ID被他城复用不认领。真实NetworkBridge新signal接受空当前路线、拒绝旧响应，旧城市引用不进入新view，无AI网络。真实Standardization读取保存模板、旧City Property消失不丢已存知识、不补录AI建筑、后续模板更新可保存；缺失历史只hold模板。

`test_p0_e2_exit.py`复测21组2322明确ID撤销、普通建筑/其它城/永久账本、UNKNOWN、失败隔离/3次上限；增加真实模块return hooks旧samples清空、无carrier重放；继承已有16导入、同Owner投资/保存/失败恢复回归。全Lua编译、modinfo/W0001引用检查通过。**LOCAL_SIMULATION_PASS / STATIC_CONFIRMED，不是USER_GAME_TEST_PASS。** 没有运行全部历史压力测试，没有部署。

### 未解决技术边界 / 下一门禁

- 当前绑定token在原生跨Owner/夺回时是否保留未验证；缺失则技术HELD，绝不复制token到新城强行通过。不承诺已覆盖全部征服/自由城/交易路径。
- 需在foreign持有阶段完成B096模块退出（同session或foreign存档load重验）；如果直接加载已夺回而未确认事件/退出完成，保持HELD，不重放猜测事件。正常已确认ACTIVE夺回存档可冷load。
- 原生RemoveBuilding撤销与正常consumer再施加、事件排序、工业completion路径需后续最小实机验证；本轮无部署，暂不要求用户测试。
- 缺少工业pre-loss snapshot只暂停模板；不统一迁移其它专业未实施/deferred成果。
- **尚不建议直接实施首次AI城snapshot/Claim。** 可另行准备独立manifest，但当前夺回闭环仍有原生身份/事件证据门禁；Claim不能作为解决这些问题的替代。本轮STOP，等checkpoint审阅。


## B098.125 — 单城 native ownership round-trip validation

仅最小按需诊断，B096/B097认领/退出/恢复规则不改。复用“E2往返”（原进度保存）左键请求，无需选城，读取登记位置；右键原UI证据保留。报告原/现引用和token、保存stage/revision、最近转移事件/候选/拒绝原因、永久Potential/receipts、当前ACTIVE、模块退出计数与移除读回、科研支持/住房/GPP实存载体、Network epoch/input/derived/current reference。按需输出相同文本到Lua.log `[SPC][E2_NATIVE]`。无新持久debug结构；每模块固定一份最近退出核验、一个最近转移/候选，冷load清空，保存的既有loss/current仍读取。报告的退出计数是本次加载内观察，不是完整历史；carrier presence/readback不是原生yield settlement证明。

### 最小用户流程（独立测试存档；不启动游戏代测）

1. 用一座**非首都科研城**，Potential≥2（建议3）、当前ACTIVE≥2，至少图书馆/大学及一名工作专家。可行时保留一条已知国内商路以观察Network变化。先另存`E2-before`；选城，右键“迁移进度”一次，再左键“E2往返”。记录报告+城市收益/专家读数。以后不再右键迁移。
2. 优先将该城交易给AI，再左键“E2往返”（不需选外方城）：必须HELD_TRANSFER，退出完成，目标科研载体0，旧Network不含已失城的source/receiver。另存`E2-foreign`，读档后再读同一报告，检查永久Potential/receipt数与token/实际owner；不迁移AI、不对外方投资。
3. 原玩家通过交易取得同城；不安排合格已就职总督。读取“E2往返”+城市收益：ACCEPTED、Identity/Potential/receipt原值，ACTIVE应1；Lv2住房/GPP载体应0（Lv1支持可正常回来）。确认当前Network样本/引用，不能恢复旧路由；如路线未发生可验证变化，Network新路线重建仍NOT_TESTED，不硬判PASS。
4. 若前三步通过，恢复合格总督并等正常就职一次：ACTIVE和对应现行收益应恢复，仍不得重新投资达到旧Potential。最后保留测试存档与报告/Lua.log即可。失城→外方save/load是本轮必需边界；可选夺回后再另存读档，不代替外方边界。

交易若无法取回，不要求耗大量回合或战争；暂停并报告，再决定替代路径。交易成功只覆盖实测交易事件链，不自动覆盖征服、解放、自由城。无路线fixture时明确Network仅观察失效/当前input，不能声称完整route-change PASS。已装Cheat只可用户操作准备fixture，不改Mods、不绕过身份token，不用Claim。

### Stop / 证据分级

token不连续或无法证明同城→TECHNICAL_IDENTITY_BOUNDARY；事件到达对象不可读/缺少匹配事件→EVENT_ORDER_BOUNDARY；退出报失败或外方仍有载体/本Mod收益→NATIVE_WITHDRAWAL_BOUNDARY；save/load证据缺失→SAVE_IDENTITY_BOUNDARY。看到UNKNOWN/拒绝立即保留报告与当次Lua.log，不自动复制token、改CityID、按名字/坐标认领，也不修Gameplay绕过。

本地：真实报告在foreign HELD读取两次，永久Game记录/载体写入计数不变；沿用B096/B097定向L3回归与全Lua编译、modinfo/dispatch/W0001检查通过。未跑全历史压力测试。新增诊断不改变验证Authority。

当前native observed facts、withdrawal、recapture identity、ACTIVE重算、Network重建、save/load：**全部PENDING_USER_GAME_TEST，既非PASS也非FAIL**。不得将本地模拟复制到native结果栏。尚不能据此批准首次AI城snapshot/Claim implementation。本批只准备/部署测试包，由用户执行原生游戏步骤，回传后逐项判断。
