# 工业后续模块：调查与实施准备

State: PREPARATION_COMPLETE / IMPLEMENTATION_NOT_AUTHORIZED。
Review baseline: develop `f03558be2a8873e12eed6b8aff3257e313f1a398`；Spec D0047 / Industry D0045 / Shared D0045 / Architecture A0161。

## 当前范围与正式来源

本轮调查、计划，不实现、不改Design/目录/数值、不退出旧工业效果、不部署。B165仍是待验意义延展切片；实际进度/授权看[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)，本页不增加日常必读集合。

[Industry Content](../../Design/Content/Industry_D0045.json)与[Spec工业节](../../Design/Specialization_v0.1_Design_Spec.md#7-industry--industrial-zone--ind)规定玩法；[Shared具名生命周期](../../Design/Content/Shared_D0045.json#/concepts/LONG_TERM_STATE_LIFECYCLE)规定A城市历史/B文明信用/G专业单位等分别归属。人类设计见[工业阅读版](../../Design/Industry.md)。D0045已给首测值及中断、Gold/Faith、每模板实际holder规则，不能重开成公式TBD。

## 当前落地矩阵与直接依赖

| 系统 | 目前真正落地 | 缺口及直接文件 |
|---|---|---|
| 基础支持/II住房/GPP | 自动接入，保留已测证据 | [IndustrySupport](../../../Mod/IndustrySupport.lua)等不是本轮重写目标 |
| 建筑模板账本 | initialize/restore/reconcile/已初始化空/损坏保护已接入 | [Standardization](../../../Mod/Standardization.lua)、[Store](../../../Mod/CityProgressionStore.lua)；[B142](../../Status/Validation/Results/Specialization_B142_Template_Pass.md)只证明所测记录/重启 |
| 区域模板 | 尚未正式记录 | [Catalog](../../../Mod/StandardizationCatalog.lua)只列建筑，OnDistrictConstructed仅Discover建筑，不等于typed District知识 |
| 标准化效果 | 旧AUTO折扣仍在 | [Discount](../../../Mod/StandardizationDiscount.lua)ACTIVE>=1、group并集/全来源最高等级；[SQL](../../../Mod/Data/StandardizationDiscount.sql)Level×10%；没有当前+10%建设writer |
| 本城标准化/合法币种 | 当前不能当已完成 | Discount仅取网络recipients，缺非连网工业self；[DiscountEligibility](../../../Mod/UI/DiscountEligibility.lua)只读Gold CanStartCommand，不能证明Faith合法渠道 |
| N/E/L与三项工程能力 | 没有当前历史collector/保存业务字段或正式writer | 本城真奇观N、文明真完成时代E、城市研习L均须各自可靠权威；现持奇观不是完成Owner证据 |
| 队伍 | 旧项目/单位/施工路径运行 | [CrewProjects](../../../Mod/CrewProjects.lua)、[项目SQL](../../../Mod/Data/CrewProjects.sql)未按III/IV、2槽及新成本；[UnitTargets](../../../Mod/UnitTargets.lua)/[UnitActions](../../../Mod/UnitActions.lua)仍允许普通建筑/区域 |
| 旧工业IV生产网络 | Copy自动Production仍在 | [CopyYields](../../../Mod/CopyYields.lua)50% actual Production不是当前模板网络，须未来精确退出 |

新发现补充[B164盘点](../../Reports/Technical/Specialization_B164_Implementation_Landing_Audit.md#工业账本已补齐最新效果合同尚未适配)：self来源、typed District、Gold/Faith资格、原生项目直接grant和`CanCapture=0`均有真实实现差距；不能以文件存在/旧PASS推为新机制落地。

[NetworkBridge](../../../Mod/NetworkBridge.lua)按Potential建立共同topology，工业在自己consumer过滤当前ACTIVE>=III；不要把全桥改为III。C1/D1折扣样本/ACK/dirty、C2引用退出及[公共更新合同](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)可继承，不重新发明事件总线/独立事实collector。

## 推荐顺序与最小批次

复用总计划G/H/I/J ID。G历史与H1知识可分别准备；III标准化基线不依赖E/L研习完成，高档队不依赖工程传统。先关闭每条原语门禁，再切真实writer，不用旧收益填新能力空缺。

| 切片 | 交付边界 | 直接依赖/停止条件 |
|---|---|---|
| **G：N/E奇观完成历史** | 只建可靠事实/保存，没有新收益 | 实际完成事件/城与文明归属、Wonder自身Era、可信创建起点及重复去重；无法证明不反推 |
| **H1：typed模板知识增量** | 保留建筑reconcile，增加已批准区域模板及归一/保存 | 可靠首次/旧history/schema区别；不扩目录、不修改折扣 |
| **H2：合法购买原语与plan** | 每模板实际holder、self/network来源、Gold/Faith逐渠道资格/报价/退出 | H1；III0、IV2L；native合法价及无新增购买权 |
| **H3：建设原语与plan** | 同holder输入，III10%、IV10+2L%，普通建筑/区域建设 | H1、Production百分比/真实进度；同Commerce发展+50%加算 |
| **H正式基线cutover** | H2/H3原语各自确认后一个定域切换，退旧折扣与Industry Copy | exclusive writer、exact cleanup、可靠L状态；不是本轮实施许可 |
| **I-Tradition：工程传统研习** | E提供可学额度，IV完整1T成功提交城市L+1并增强标准化 | G、L/E保存、当前资格/真实中断/原子成功；未完成轮不能续半进度 |
| **J1＋I-Practice：队伍来源/库存/组建成本** | J1先完善训练来源/2槽/III-IV分档；Practice再用N改变成本 | J1资格/原生grant/binding；G提供N，Practice不改capacity或注入 |
| **J2：Wonder-only固定施工与单位保护** | 一次消费/释放槽、固定注入无溢出、敌方保护回归 | J1及实际保护/注入原语；不允许普通建筑/区域，不重放不确定执行 |
| **I-Macro：巨构工程学** | 本城普通生产旧时代Wonder10/20/30%，不影响队伍注入 | 当前Era/Wonder own Era、资格、实际Production原语；独立于N/E/L门槛 |

H2/H3可以先做无收益模型/原语验证，再合并正式基线切换，避免只移除旧折扣却把新建设能力误报完整。每模板IV增强必须有可靠L；首次L初始化要有确切“该账本此前未建立”依据，已有历史缺失不能填0。未来批次需写清支持的初始化起点，不因缺史阻塞不依赖它的III路径。

## G：本城经验N与文明信用E不是同一账本

现行规则从游戏开始记录实际奇观完成，不要求工业身份/ACTIVE/Governor。每次可靠完成可产生：A本城真实完成记录N，以及B实际完成文明的Wonder自身Era去重集合E。城易主N随城，E留实际完成文明；征服、持有或当前时代均不等于过去完成信用。

当前代码没有对应collector。可复用Store的稳定token、Game保存/读回校验和HELD连续性路由；`active`/recapture仍限定原本地Owner，不能宣称已支持任意新Owner或未登记外国城市的持久引用。G实施前要证明完成时的城市绑定及文明证据能保存；外国时期的A经验只接可靠已保存/当前可证明本地完成事实。轻量处理明确Wonder完成事件不等于为AI运行专业；不增加所有AI城市长期建筑监听或周期全城考古。

对于已经运行但从未收集N/E的测试存档，没有“过去已完整记录”的凭据。当前持有奇观不能反推全历史/实际完成Owner；不能初始化E=0冒充已知从开局无完成，不能用当前Building扫描伪造N完整。优先用可信创建起点的测试局验证从开局collector；若现有原生接口能可靠证明部分本地完成，只将其与可靠N历史并入，不据此补文明E。无法确认收集覆盖或历史恢复时，保持UNKNOWN/HELD，停止依赖路径，不发猜测奖励。

Local L3：未工业时完成、不同Owner的城市N/文明E分离、同Era去重/同事件幂等、转移不转E、缺失/损坏/可靠空账本及保存失败。Native最小delta：一座非工业城真实完成一座奇观→验证N/E与own Era→合法成为工业城后读取；新增持久collector需一次保存重载，但不是重跑E2所有交易/认领场景。Exit只证明历史事实，不宣称工程收益已实现。

## H：历史知识、合法来源与效率三个层次

### H1知识增量

建筑账本沿IND-TEMPLATE-006：合法首次初始化、已有可靠历史恢复、当前合格建筑并入、历史损坏四种情况分开；保留当前缺失/掠夺/拆除的可靠历史，非支持Owner建后消失且未记录的对象不猜。继承B140–B142的有限证据，不每次重验完整旧建筑生命周期。

增加typed District记录与特色base归一，在已批准区域完成/合法初始化时增量写入；不能把区域完成回调目前的建筑Discover当成已记录区域。保持模板记录范围与启用目标目录分离；City Center分组仍为建筑，不新增City Center district template；不拿Shared D目录直接替换标准化目录，不扩当前市中心组/宗教或特色权限。

Local L3：新旧typed数据、可信首次与initialized-empty/缺史、已完成区域/replacement、重复通知、合法reconcile并集不反删。Native只测新增区域记录/相应重载，旧建筑记录继承B142；这是新保存schema差异，不需要再次从头做所有E2。

### H2/H3来源与目标计划

来源包括合格工业本城self，以及共同topology实际能接收的工业来源；只在consumer过滤ACTIVE>=III。每模板T收集实际holder，再分别construction MAX与合法purchase MAX；不同模板UNION。无模板来源再高L也不能放大T。self不要求伪造路线，center/reception由NET负责，receiver不因此成为永久知识owner或递归source。

D0045原例：A L7持大学/研究所，B L2持大学/银行，C L5持工厂→大学/研究所24%、银行14%、工厂20%。旧“模板来源与全国最高效率可不同”的算法被正式取代。III来源输出建设10%/购买0%；IV建设10+2L%、购买2L%；ACTIVE不足III仅保留知识/成果、不输出。L>E仍利用全L，E只管以后研习。

construction只作用于当前合法的普通建筑/区域目标，Wonder排除；purchase只作用于该目标本来合法的Gold/Faith各渠道。已有CanStartCommand仅Gold，需要Faith对应实际资格；价格字段不证明权限。如果原生同一成本modifier可靠影响两种合法价格且不新增许可，可以复用，但须证明而非假设。归一/group/catalog不改变科技、市政、互斥、特色、宗教资格。

与Commerce R共用普通建筑Production primitive和加算证据即可：同目标20%+50%=70%，不乘算、不共享模板authority，不要求R等待全部工业。当前R未实现，H3可以先测自身真实正常Production；R落地时只补组合delta，不要求H3提前伪造正式合同。 首段可靠L0应无购买折扣；2L真实价格增强在Tradition产生可靠L后合并确认。纯fixture的L只用于模型/原语验证，不冒充正式城市成果。

Local L2/首次cutover定域L3：holder例、最高来源退出后的回退、self/network去重、非holder、非法渠道、特色目标/区域、UNKNOWN不误清、confirmed loss撤销、普通Production与成本区别。Native只补真实价格、建设progress、来源变化及新增组合，不默认旧长测/全历史。

### H正式切换的exact所有者

- StandardizationDiscount owns实际加载`SPC_B054_Targets`生成的`BUILDING_SPC_B054_<BuildingType>_<1..4>`及附件；需按加载目标导出具体allowlist。其Start/Audit/Receive/load/return/exit必须互斥，不能只换SQL留下旧selector重建。
- CopyYields当前只写Production：`BUILDING_SPC_B051_PRODUCTION_POS_0..15`、`NEG_0..15`、`POP_0..7`共40精确ID。退出其Gameplay.Start、COPY_YIELD_SAMPLE、Bridge fanout、load/audit/return和[CopyYieldRefresh](../../../Mod/UI/CopyYieldRefresh.lua)producer；不恢复已退Research Copy。
- 最后旧Copy consumer退出后再关闭其actual sample发送/旧控制；保留IndustrySupport的BASE producer、其它独立诊断、NET topology与无关专业。实验HalfYieldProbe的Science/Production64项及`SPC_B050_HALF_ENABLED`只在本批真实涉及时检查，不能前缀删全库。
- 原Type定义保留到确定退出，未知清理HELD；确认退出后才能正常启用新投影，普通样本延迟不反复做cutover。旧入口/load不能复活，非相关建筑/账本不受影响。

## I：三项工程能力分别接入

| 能力 | 事实与正式效果 | 保存/退出与原生差异 |
|---|---|---|
| 工程传统 | 全国E供新研习；本城IV且L<E完整1 Production Turn成功永久提交L+1；输出建设10+2L与合法购买2L | L为A城市历史、身份/ACTIVE/Owner变化保留；III仅10/0，不研习；低III不输出。未来合法Owner E<L也不截断L |
| 工程实践 | 当前IV按本城真实N0/1–2/3–5/6+成本150/140/130/120%；III始终150% | N长期保留，但收益按当前IV；只改组建成本，不强化模板/施工力，不新增槽位 |
| 巨构工程学 | 当前IV本城自行普通生产旧时代Wonder，当前文明Era−Wonder自身Era差1/2/3+给10/20/30%；当前Era无加成 | 当前派生效果、资格下降精确退出；不看N/E/L，不修改已训练队伍的锁定capacity或注入 |

研习未完成时，Governor导致ACTIVE不足IV、Identity退出、REALLOCATING、Owner变化或正常生产中断取消本轮，不增L/不存半进度；再次合格完整重做，已提交L不变。该规则D0045已定，不再标“中断Design TBD”。[TimedProject](../../../Mod/TimedProject.lua)仍是session无奖励/无保存原型；[Claim](../../../Mod/ClaimProjects.lua)已有特定续接，但正式Dialogue1T永久倍率事务还未实现。复用已验1T执行原语不等于L的提交/真实中断/save已PASS，不能导入Dialogue时代配额或倍率。

Tradition L3本地：L<E/L=E/L>E、完整回合/中断/Owner与重复成功、提交失败、不重复/跨加载计功、恢复只派生当前效果。Native一轮成功＋一轮真正中断后重做，新增L持久重载有具体信息价值。Practice L2本地成本阈值全矩阵，native只补一个实际成本跨档；Macro L2普通Wonder增量与固定Team隔离，原语证据不同不能一项通过算三项完成。

## J：训练成本、永久队伍、固定施工分开

### J1来源、2槽与新成本

当前[项目SQL](../../../Mod/Data/CrewProjects.sql)原生modifier直接grant单位，[CrewProjects](../../../Mod/CrewProjects.lua)只按Identity/原锚点开放五档。正式J1须证明完成门禁/grant与实际新单位一一绑定、训练来源token与unit identity/原Owner可靠保存，不能按单位名/相邻坐标猜或重复grant。

III开放I–III，IV额外IV–V，无E4/5门槛。每训练source当前Owner的存活本城出身队伍总2槽，所有档各1；完成队伍属于独立原Owner资产，source总督/ACTIVE/Identity/Owner变化不删、不停止使用。旧Owner队伍不占新Owner来源容量，原Owner夺回重新计其旧存活队；消费/合法移除释放，活着保护撤退不释放。

| 档 | 锁定基础施工力 | III或IV N0成本150% | IV N1–2成本140% | IV N3–5成本130% | IV N6+成本120% |
|---|---:|---:|---:|---:|---:|
| I | 250 | 375 | 350 | 325 | 300 |
| II | 420 | 630 | 588 | 546 | 504 |
| III | 750 | 1125 | 1050 | 975 | 900 |
| IV | 1000 | 1500 | 1400 | 1300 | 1200 |
| V | 1360 | 2040 | 1904 | 1768 | 1632 |

均为标准速度首测值；其它速度保留已接受scaling方向，capacity锁为`floor(reference*speed CostMultiplier/100)`，最终Production/Gold/Cost需整数时按D0045 Floor，不做无必要中间Floor。Practice只改投入不改锁定capacity。native其它速度成本载体仍需验证，不能改成另一套玩法舍入。

实际修改依赖包括CrewProjects、项目/单位/动作SQL、[Probe](../../../Mod/Probe.lua)Specs、训练完成handler、Gameplay/modinfo/Text/UI直接caller；这些仍读旧280/460/820/1100/1500，不能只改一个SQL表。`BUILDING_SPC_CREW_PROJECT_ACCESS`、五项目及`SPC_PROJECT_GRANT_CREW_<capacity>`授予附件需要逐项cutover。旧排队项目满槽/资格下降时仍能grant，是实际技术门禁；不能静默删队列、扣锤、退款或删除已完成队伍来绕过。DEV Spawn不得越新来源/库存成为正式资产，未知来源显式隔离。

Local L3：档位门槛、同回合多完成/重复通知、队列满槽、保存、Owner切换/夺回、活着撤退与合法消耗、其它城隔离。Native一个source完成两队→第三受限→合法消耗释放；新的unit-binding/source-owner路径需要定域失城/恢复或重载，不再重复E2城市身份全流程。无法证明grant/容量门禁则只停止J，不影响H或Macro。

### J2目标、固定注入与保护

正式目标只Wonder，Megaproject仅future；停止UnitTargets/UnitActions普通Buildings/Districts授权，保留Settler investment分支。[ConstructionProbe](../../../Mod/ConstructionProbe.lua)仍供正式链必要事实，不能整模块删除。

现有UnitActions为一次destroy→`AddProgress(min(amount,remaining))`，不重放不确定原生执行；新消费确认前重验单位/目标Owner与ref、目标tile/当前Wonder/remaining/1charge及永久训练provenance/unit绑定完整性，成功才精确释放slot一次。不重新要求训练source当前Industry/ACTIVE或Owner与单位相同；来源降级、退出工业或易主均不阻止已有队伍使用。注入只取锁定基础capacity，不受Macro、奇观政策、宜居度或其它普通Production百分比放大；余量浪费，后续目标/空队列不得保存overflow。

敌方直接capture/Owner转换已被D0045禁止，必须证明保护撤退/安全回归；`CanCapture=0`只禁本单位主动capture，不证明自身受保护。源城变化不取消已有队伍；活着回归仍占库存。未定义的是原unit Owner完全消失等具名处置，不把普通source转移又写成Design TBD。

Local L2＋涉及unit保存L3：合法/非法目标、预览到确认变化、恰好/超量、失败不消费、未知执行不重放、重复消费/slot只释放一次。Native一个带正常Wonder百分比的目标测固定注入及下一目标无溢出，另一个敌方交互证明不转Owner且回归；这些是新增原语，不用旧Cheat完成或CanCapture字段替代。正式可玩Exit须同时有训练/库存/使用/保护及实际入口，不能只做P0面板手动开关就称落地。

## 已确定规则、技术未知与真正未决

| 分类 | 内容 | 影响范围 |
|---|---|---|
| 已定，非TBD | 每模板holder内MAX、III10/0及IV2L、Gold/Faith合法渠道、N/E/L归属、研习中断、III/IV开放队档、2槽/Owner计槽、固定注入、非捕获与Floor | 按上述当前规则实施，不重开Design |
| TECHNICAL | Wonder完成证据/创建起点/外国时期连续性、N/E/L业务保存与恢复、typed District增量、self resolver、逐渠道资格/成本效果、1T提交/中断、项目grant满槽门禁、动态成本/速度、unit绑定与安全回归、固定注入与加算 | 各依赖切片；局部失败不阻塞全部工业或其它专业 |
| DESIGN未覆盖 | 原unit Owner完全消失等非普通source变化处置；城市彻底摧毁等未涵盖历史/绑定处理 | 只相应路径；不得借本计划建立统一永久资产清理规则 |
| 成熟度/Balance | 机构/队伍/研习项目候选或TBD名称，首测数值待真实平衡 | 不擅自冻结名称，不把首测认作最终平衡 |

模板可靠性不需要D归一化；标准化本身不是D consumer。Shared普通建筑/D目录覆盖与标准化typed目录是不同责任，不借工业准备扩HD Catalog。三处未衔接future设计边界及AI/MP范围保持，不做全城迁移/new cityKey。

## 后续验证、性能与授权

每段按直接source/consumer/state闭包读取；仅H/J正式cutover搜索全部Mod exact相关ID/callers，不通读全仓历史。共同基础hash未变可复用，新增账本与grant路径不能因为旧E2已PASS免掉本地保存/失城/重复验证。只对新增native风险追加最小实机；普通yield切片不默认保存启用态→END→冷载OFF→重新启用仪式。

普通事实复用现有EffectiveFacts与模板summary，诊断明细按需。N/E collector只在明确完成事件写增量；来源资格、模板/holder/L版本或真实路线变化才更新相关receiver。队伍registry由J负责单位退出/消费和source容量失效；pending1T由Tradition负责完成/取消/加载。缓存/队列有明确owner/失效/替换/结束，不把L或N历史为性能清掉，也不添加每帧/hover、粗粒度每城每回合一次或独立GC。

本轮STATIC_CONFIRMED调查完成；只做文档/context检查，未运行新的玩法模拟或原生测试。未来H/Macro/Practice为L2，历史/模板schema/L与unit库存为L3相关定域验证；无需默认全历史/stress/旧长测。当前用户无需测试、无需重新决定已经冻结的工业机制。Codex下一步等待B165反馈及一个独立最小batch授权；建议工业先G历史门禁或H1知识增量，不直接一次实施整个工业。
