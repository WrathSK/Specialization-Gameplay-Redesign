# 商业后续模块：调查与实施准备

State: PREPARATION_COMPLETE / IMPLEMENTATION_NOT_AUTHORIZED。
Review baseline: develop `f03558be2a8873e12eed6b8aff3257e313f1a398`；Spec D0047 / Commerce D0045 / Shared D0045 / Architecture A0161。

## 当前范围与停止点

本次只调查、准备计划。B165意义延展原生门禁仍待用户验收；本页不替换当前manifest、不启用新商业功能、不关闭旧writer、不部署。实际运行包、授权和证据只查[Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)与[Authority](../../Workflow/Authority.json)。未来按下列最小批次分别审核授权，不把整份准备计划视作实施许可。

正式规则来自[Commerce Content](../../Design/Content/Commerce_D0045.json)、[Spec商业节](../../Design/Specialization_v0.1_Design_Spec.md#8-commerce--commercial-hub--com)、[Shared具名生命周期](../../Design/Content/Shared_D0045.json#/concepts/LONG_TERM_STATE_LIFECYCLE)。人类完整设计见[商业阅读版](../../Design/Commerce.md)。本页规定技术准备、依赖和门禁，不成为另一份玩法权威。

## 当前落地与可复用范围

| 系统 | 实际状态 | 本轮确认的缺口 |
|---|---|---|
| 基础支持、二级资格 | 已自动接入，继承各自已测范围 | 不在本计划重做3F/3P、住房及基础GPP |
| 商业化 | 新机制没有正式writer | 缺领域配置、专家容量与暂停恢复、领域X、Gold投影；旧三类连接支持仍运行 |
| 资本投资 | 未实现 | 缺报价、扣款、锁定S/结果/期限、保护状态和恰好一次结算 |
| 发展投资 | 未实现 | 缺plot-only报价、合同容量、目标普通建筑+50%及终止/到期退出 |
| 商业信誉 | 未实现 | 缺首次IV起点、身份计龄与独立保存；不能套科研传统的Owner policy |
| 资产重组 | 未实现 | 缺500P专属团队、地图动作、REALLOCATING事务、P−1、扰动与配置完成 |
| 旧商业收益 | 自动路径尚在 | Lv3Effects的3项COM载体、CommerceConvergence的48项20%汇聚需要未来P正式切换 |

[落地盘点](../../Reports/Technical/Specialization_B164_Implementation_Landing_Audit.md#商业基础已接入新独有体系尚未落地)与当前直接代码相符。旧[InvestmentAction](../../../Mod/InvestmentAction.lua)是开拓者Potential投资，不是Gold合同。商业的技术可复用基础是：Shared D/工作专家事实、E2可靠城市引用、NetworkInput当前路线样本、请求版本/ACK/撤销和按需UI；它们的存在不证明新合同或新收益已通过。旧B062只证明所测20%Science/非叠加及用户口述撤销等，不能证明新Gold/资金精度；B137隔离只证明报告中的定域撤销/静默，不外推逐个载体真实收益全部PASS。

### 已确认的直接实现面

- [NetworkInput](../../../Mod/NetworkInput.lua)、[NetworkBridge](../../../Mod/NetworkBridge.lua)：现有路线输入与共同中心拓扑。商业化的直接双向资格、发展投资的outgoing资格须独立索引，不能以中心接收集合替代。
- [CityProgressionStore](../../../Mod/CityProgressionStore.lua)：稳定城市token、Game保存/读回、UNKNOWN/确认失城与恢复路由可复用。当前业务字段没有商业合同、配置或信誉；EffectiveFacts仍按基础P1加投资receipts推Potential，T的永久P−1必须定域适配，不能靠清Identity冒充；`active`仍限定原本地Owner，不能宣称已支持未来任意Owner系统。
- [CrewProjectOrder](../../../Mod/UI/CrewProjectOrder.lua)已包装`AdvanceProject`并在原生请求前调用Claim/TimedProjectSelection；[ClaimProjectUI](../../../Mod/UI/ClaimProjectUI.lua)和[TimedProjectSelection](../../../Mod/UI/TimedProjectSelection.lua)可作hook参考。旧spike中“仅排序”的描述不再是当前事实。但Claim是真实生产项目，尚未证明商业action entry能完全不入队。
- [Lv3Effects](../../../Mod/Lv3Effects.lua)、[CommerceConvergence](../../../Mod/CommerceConvergence.lua)、[Gameplay](../../../Mod/Gameplay.lua)及[modinfo](../../../Mod/SpecializationP0.modinfo)：旧writer实际接线，见下方定域切换清单。
- [Discount/Copy生命周期](Batch_C1_Discount_Lifecycle.md)、[dirty传播](Batch_D1_Discount_Propagation.md)与[公共更新合同](../Specialization_v0.1_Architecture.md#公共更新与临时状态接入约束)：复用真实输入/退出协议，不能把普通收益重算去重用于有序合同结算。

## 模块实施顺序与依赖

保留总计划O/P/Q/R/S/T标识，用子切片说明范围，不建立新的manifest体系。推荐先O只读事实，随后按已确定输入准备S记录/P配置与U3入口；P真实Gold、Q、R、T各自关闭对应门禁后再实施。S不是Q的后置奖励，T也不必等待全部投资能力完成。

| 切片 | 范围及完成边界 | 必须具备的输入/门禁 |
|---|---|---|
| **O：直接商路只读服务** | 同一verified snapshot建立incoming/outgoing/双向pair索引；只读资格与版本，不加收益、不改共同topology | 当前完整样本、owner/reference/路线有效性；复用已接受后台来源，不再要求纯Gameplay全集 |
| **S1：信誉记录与只读状态** | 标准速度首次Commerce IV建立起点；完整保留Identity回合+1、cap40；输出当前有效R，不加新收益 | 业务专属保存/身份退出/Owner冻结、完整回合判定与重复通知去重；非标准速度需决定 |
| **P1：领域配置与U3入口原型** | 五领域选择/order、LIFO暂停/恢复与无收益面板；旧writer保留并明确标注 | O、D、工作专家、当前资格、配置保存；X未定时不展示虚构正式Gold，不扣资金 |
| **P2：商业化正式效果与旧writer切换** | ACTIVE III五领域Gold；IV消费有效R；单writer、正常多城自动运行 | COM-DETAIL-X、native Gold精度/非递归与exact退出；P1、O及S读接口 |
| **Q1：稳健合同** | 一层报价/确认扣款、锁定具体S来源及条款、标准10T一次结算 | S池/等级/空池与同域排他范围已定；资金变更/持久提交的可靠执行证据 |
| **Q2：风险合同** | 确认时抽取并保存结果/立即更新隐藏保护；到期只揭示与结算 | Q1、保护换基本面和Owner政策；随机与隐藏字段不泄露；确认锁定有效R与退款比例 |
| **R：发展投资** | 确认时outgoing资格/plot-only报价、锁定合同、普通建筑+50%及到期/易主退出 | P_low/无解政策、目标渠道/目录、Production primitive与标准化加算；不要求整个工业体系先完成 |
| **T1：团队及动作原语** | production-only专属团队、训练来源/保护、两个区域动作与扰动接口；不先开放半成品重组 | 500P、无玩家删除、敌方保护回归、非Food及净余粮−75%的原生结算 |
| **T2：完整重组事务** | REALLOCATING、P−1、至少5完整标准回合、历史保留、一次配置/消耗与Owner异常终止 | T1、E2直接消费者的退出/配置闭环；非标准速度精确量化未定 |

O与工业G/H知识准备不消费Meaning载体，不依赖B165追加精度。但当前用户仅授权调查；B165反馈若触及Shared D/专家、E2引用或共用事件/桥接，实施前只复核实际受影响路径，其它未变规则/hash复用。B165不是所有商业技术原语的PASS/FAIL判据。

## O：只读资格，三种路线关系分开

[后台来源决定](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md)允许后台BTS/原版UI当前路线读入；保留现有样本完整性、版本、epoch与ACK，不重新寻找“纯Gameplay全路线”作为前置条件。

| 关系 | 可用条件 | 不能替代什么 |
|---|---|---|
| 商业化source | 自城，或己方其它城与本商业城任一方向直接有效国内路线 | Network分发可达不能凭空产生direct pair |
| 发展投资签约 | 本商业城→目标己方城的直接有效outgoing路线 | 反向路线、center reachability均不够；确认后的断路不取消合同 |
| 共同中心网络 | 沿既定NET拓扑接入/分发/首都规则 | 不决定资本S池；该池仍须Design确认 |

普通计算只返回必要索引/资格/版本，不构造全城诊断；同一确认快照可复用，route/owner/ref/完整性变化失效。读取UNKNOWN不能当空网络，失城确认继续触发受影响旧输出撤销。事件按变化端点与实际依赖定域；保留有界加载/回合核对，不每帧、hover或每个外国事件全城扫描。

Local（L2，若改变共同bridge则定域L3）：A→B/B→A、重复route去重、外方排除、自城、断路/UNKNOWN/新epoch、变更后所有真实直接consumer。Native仅在新增native getter/调用路径或既有样本不能证明的差异时补一个路线切换；完全复用来源时不要求单独实机。

## P与S：配置、当前效果与制度历史分开

P1保存用户选择和实际开启顺序；容量下降暂停最新项而不删配置，恢复按早先项优先。手动关闭移除该项，重开成为最新；保留Identity的ACTIVE不足保留配置，Identity退出或Owner变化清配置。冷加载恢复选择，再用当前ACTIVE/专家/D/路线资格重新派生有效项，不恢复旧收益snapshot。

P2只纳入Campus Science、Theater Culture、Industrial Production、Holy Faith、Harbor Gold；本城须有对应区域。`Gold_domain=0.1*D_local*X_highest_legal*(1+0.005*R_effective)`；D是Absolute Infrastructure Depth，X的组件/聚合仍待COM-DETAIL-X。自城或直接双向池取最高合法X，不扣来源yield；商业化Gold不能递归进入Harbor X。禁止直接用旧全国城市总产出、20%复制、Shared Yield Share或Meaning Floor替代该公式。

S首次IV后的信誉按Commerce Identity连续完整回合计龄；ACTIVE下降继续积累、效果只IV，Owner变化记录随城而非清零/分仓，unsupported时期专业机制休眠。Identity退出立即R=0；新Commerce身份重新起点。`R_effective`进入P倍率与Q风险失败本金返还，不能改变资本胜利概率/成功利润、发展投资或重组。资本确认锁定相关R条款，不因到期时Governor变化重报价格。

实现需独立声明配置owner、信誉owner、dirty版本及成功保存状态，不复用ResearchTradition的origin-owner暂停作为信誉规则。Local：同回合开关/order、capacity3→1→2→3、同D异X选择、非递归、Owner/Identity退出、重复计龄/保存；新持久字段为L3，纯投影为L2。Native：P最终Gold→同回合X或容量改变→精确退出；S只在新计龄/存储路径落地时测首次IV后的一个完整回合及ACTIVE下降时R继续/effectiveR暂停，必要同回合重载确认不重复计龄，不默认再跑旧Probe默认OFF仪式。

### P正式cutover的精确责任

1. Lv3Effects COM分支 owns `BUILDING_SPC_DEV_LV3_COM_RESEARCH/CULTURE/INDUSTRY`，旧SQL各给工作专家+2对应yield。只撤这3项，不退出其它专业或基础支持。
2. CommerceConvergence owns `BUILDING_SPC_B061_SCIENCE/CULTURE/PRODUCTION_0..15`共48项，旧CITY_CENTER `2^bit`最终值来自incoming-only总量20%。只退这48项及旧解释。
3. 关闭/互斥重建面包括Gameplay.Start/COMMERCE控制、Bridge.notify、native hooks、load/audit/return及NetworkIsolation；不能仅隐藏按钮或删定义。新效果confirmed失城也走自身module-owned withdrawal；UNKNOWN不误清。
4. 共同Trade Center topology、NetworkBoost的Research/Culture消费者及Industry BASE事实producer保留。当前NetworkBoost无Commerce payload，不能为P退整个Boost。
5. source/code/SQL/实验入口的exact allowlist在正式批次前再核对；本次未实施任何退出。正式切换先互斥停止旧正向入口→exact3+48撤销并确认→启用新投影；未确认则新HELD，保留cleanup Types，不能双写补缺。

## Q：合同与隐藏保护有各自的持久权威

Q1新签约要求当前Commerce ACTIVE>=III，先做无随机的稳健链。每次确认读当时剩余国库，锁`P=25%*treasury`、标准10T、domain、具体Commerce/S城市及Owner关系、D/S/C/r、期限、状态与quote版本。最高S同级按最早到达该级再稳定key决定；现有城市token不自动提供“最早到级”证据，需补业务记录/可靠来源，缺证据不随机挑。C读取确认时实际有效商业化状态；如尚未落地，不能用fixture配置或猜测C冒充正式签约。`r=.01*D*S*C`，商业化C=1.25，否则1；safe返还`P*(1+r)`，不能把本金再乘其他公式。

Q2确认即以当前保护计算概率、抽取、锁定并立即更新保护，与合同提交形成可恢复一致单元；UI期间不暴露locked outcome。基础概率`min(.8,.4+.01*D*S)`；C只改利润；成功`P*(1+3r)`，失败`P*(.5+.005*R_effective)`。保护为source city跨domain共享，失败收回距.8差额25%，成功或Identity退出reset；不反惩罚好运。新基本面结合与保护Owner归属是真TBD，不能用合同终止或信誉policy推导。

报价统一Gameplay生成，UI显示总返还与净收益；`E_net=E_total−P`，负值明确警告但可选。确认重验资格/资金/版本，stale拒绝，不悄改条款。Fractional Gold/principal/quote原生精度仍需验证，Industry Floor不授权Commerce Floor。

已签合同不因Governor、ACTIVE、Identity、D/S、route变化取消/重定价/重roll；Commerce城或具体锁定S城Owner变化则异常终止，本金不返、无正常结算/失败退款、不触发或倒回保护。合同、pity、R是三个业务状态，不合成一套“所有永久资产”策略。

Local L3：连续确认25%余额、同域排他、锁定S tie/source、重复扣款/到期/部分提交HELD、确认后reload不reroll、隐藏字段、不误用新R、两关键城Owner终止、无关城不影响。Native只测新资金/期限/锁定存储的不确定性：一笔确认→改变签约资格→到期一次；风险批次额外一个reload仍锁定的合同，因为这是新的随机持久ownership路径，不能由旧Probe OFF证据替代。模拟不给原生exactly-once全部PASS。

## R：报价与签约后的合同独立

确认时检查source IV、目标域合法及直接outgoing；每实际工作商业专家一份并行容量，容量下降不终止已签约。同target+domain全国最多一份，不同域可并行。锁标准10T、+50%普通建筑Production、plot-only报价`P_ref=P_low+.75*(P_high−P_low)`、价格`15*P_ref`；不按瞬时focus/锁人口定价，不借非地块Food补生存条件。P_low定义/无可行解政策待决；求解器实现可调查，不能替用户定义Food目标。

签后断路、ACTIVE/Identity/专家变化不取消；目标Identity变更本身不终止。Commerce来源或目标Owner变更则无退款终止、立即退出本合同+50%并释放slot。合格普通建筑与标准化百分比加算，不扩大到单位、奇观、区域或新增购买许可。

依赖是O、对应模板无关的普通建筑Production原语和加算证明；可与工业H3合作一次组合门禁，不要求工程传统/模板等全部完成。共享modifier接口并不共享合同/模板authority。Local L3涵盖价格状态不受focus变更影响、锁定条款、同target/domain互斥、capacity变化、断路续存、Owner退出、期限和幂等结算。Native为实际正常建筑进度的单独/共同百分比与到期退出；只补新存储/失效路径，不加无变化Probe冷载仪式。

## T：团队存续与绑定事务分别管理

T1由当前Commerce ACTIVE IV生产production-only 500P标准速度团队；不加入Gold购买或玩家删除，敌方交互保护撤退/安全回归的实际接口需证明，不能以`CanCapture=0`声称自身不可捕获。完成团队是独立原Owner资产，训练城资格/Identity/Owner变化不删除它。分别保存训练来源provenance与后续绑定的REALLOCATING事务target字段；二者允许同城，不能互作生命周期依据。

T2由同一Team在目标当前专业区域清算，再移至同一目标城另一合法专业区域配置；保留独立REALLOCATING状态，不走NONE/首次认领：旧Identity立即退出、Potential−1（P>=2）、至少5完整标准回合，非Food与净余粮−75%；计时到期只允许配置，不自动恢复；合法配置成功才一次提交新Identity/P−1并按当前事实重算ACTIVE、消耗绑定团队。完成前目标Owner变化终止/销毁半成品重组及绑定团队，不恢复旧Identity；以后重新取得按明确的候选snapshot/Claim例外。其它具名永久历史按各自合同保留；已签资本/发展合同不因Identity退出而自动取消，关键Owner变化才分别终止。训练source易主不能取消另城的已绑定事务。

Local L3必须审阅所有真实Identity/ACTIVE/REALLOCATING消费者、历史暂停/退出和合同续存调用点；定域覆盖保存/中断/重复动作/P−1/最低期/Owner目标终止，不能复制Claim成功逻辑冒充重组。Native分成受保护团队/净余粮原语与一个完整事务，新的持久状态/归属需一次有针对性的重载；未证原语不开放正式按钮。无统一救援队、自动退款或万能历史重置。

## 明确未决项与技术门禁

| 分类 | 内容 | 阻塞范围 |
|---|---|---|
| DESIGN：COM-DETAIL-X | source领域产出组件/聚合，含Harbor Gold非递归口径 | P2真实Gold，O/P1无收益可先准备 |
| DESIGN：CAPITAL-S / EXCLUSIVITY | domain/本地资格、合法S池、ACTIVE或Potential、空池、同域全国或source排他 | Q1/Q2；不把商业化池/白名单自动移入 |
| DESIGN：PITY-REBASE / PITY-OWNER | 已有保护与新基本面结合；保护Owner转移保留/清除/分仓 | Q2；已定合同Owner异常终止不等于保护清零 |
| DESIGN：REFERENCE | P_low及plot-only无饥饿解不存在时规则 | R正式报价；不阻止API/纯求解fixture调查 |
| DESIGN：SPEED | 非标准速度的投资/价格/重组/信誉精确合同 | 非标准速度正式路径，不复制Research速度公式 |
| DESIGN：具名Legacy未覆盖项 | 城市彻底销毁、原Owner消失、发展target后来非法等处置 | 仅相应路径，未决不推广为所有合同Owner规则TBD |
| TECHNICAL | pre-native action无队列、领域事实、资金小数、扣款/提交/结算恢复、S到级证据、Production加算、净余粮扰动、团队保护 | 各实际复用原语；API失败需改玩法时再交用户 |

上述现行规则取代旧D0032_Adaptation商业行中的配置/计龄/合同Owner deferred，以及TS06“只排序”、TS08/16已定单位归属待决、TS20系数/信誉未冻的旧描述；那些文件只保留当时技术线索，不再决定当前Gameplay。研习/成本/专业保护等与工业的共用调查可复用证据，但一个单位通过不代表全部专业单位原生通过。

这些是当前Content已经保留的窄项，不是本次新增设计冲突。名字成熟度/首测值/Balance Validation原样；不以技术准备代替设计决定，不为填完计划自行补数值。

## 实施前重核、验证与交付约定

每段只读本段Spec/Content对象及Shared具名合同，复用已审阅的共同基础。进入P cutover必须对exact IDs/callers做全Mod定向闭包；进入Q/R/T持久路径必须核对应Store/schema/Owner/退出依赖。不要把全部商业准备或中文阅读版加入日常必读。

新缓存/报价/队列由对应module负责：quote开panel建立、关闭/失效替换、confirm消费；pending合同只按到期或Design规定的关键Owner异常终止推进；诊断默认简报、明细按需；诊断历史/临时缓存有界，不自动裁剪永久业务历史或去重凭据。普通资格计算不构造完整展示；没有每帧/hover请求、粗粒度每城每回合一次限制、独立GC或长期全AI扫描。

当前证据只有本轮STATIC_CONFIRMED源/规则调查；没有新LOCAL_SIMULATION或USER_GAME_TEST结果。本轮只做文档/selector/context/diff检查，不跑玩法回归。未来每批按W0004：普通事实/收益L2，新增合同/计龄/REALLOCATING保存为L3定域测试，简单表现L1；继承未变共享原生证据，每步说明新增信息价值，不默认长测/full stress。已有UNKNOWN、失城撤销与永久历史保护不能为省测试削弱。

本轮用户无需实机测试；后续真正需要决定的项按上表进入对应Design Talk，不需一次全解决。Codex下一步等待B165反馈和下一独立批次授权；本页不派发新的已授权实施动作。
