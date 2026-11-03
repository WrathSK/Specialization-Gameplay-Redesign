# Fact & Subscription Contract：v3 候选

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[状态登记](Decision_Closure_Register.md)｜[决定包](Owner_Gate_Stop_Report.md)｜[Gap与源码](Gap_Matrix_v3.md)

## 1. 事实契约：正常可靠、错误显式、极端保护不算结项

每类事实只有明确维护者；共享者通过稳定接口采集／公开，专业不重复全图扫描。值、值版本、可用性／错误、owner／city／token／reference、采样episode分别表达。确认负事实是合法数据，不是读取失败。错误不得变成0、空集合、无总督、已取消、已完成或已失效。

合法引擎短暂未准备应在事实拥有层登记待完成责任，凭已核实事件／初始化／可用性边界完成采集；正常不把UNKNOWN业务事实传播给专业。持续未准备、非法值或自有历史未知是严重错误，保留有限原因和证据，停止受影响不安全操作；不能靠无限publish／逐回合全城扫描或时间经过“恢复”。

获批纯被动用途的极端保护可用同一有效引用的最后确认输入，结合其他新确认事实重算；不是对所有格子的通用授权，也不成为异常root关闭标准。首次无值不编造。当前可靠负事实必须覆盖旧输入；真实建筑移除不能因旧D/集合仍在而继续合法。count／eras／categories必须来自同一GreatWork版本。

## 2. 统一 ACTIVE／Potential

统一角色接口（沿现有EffectiveFacts／CurrentSpecializationFacts演进，名称由工程落地确定）拥有当前读取投影与ACTIVE派生职责，提供身份、Potential、ACTIVE、引用／版本和错误状态；它不取代Store的永久身份、投资收据及可靠提交权威。专业只读取ACTIVE，不访问Governor专用属性或持有私有Ceiling cache。未来管理容量只是替代底层输入的接口演进方向，未获批实施。

底层当前六属性由原生Modifier维护；conditional nil合法false，正常无总督是KNOWN ceiling1。CONTROL缺失、读取失败、层级不一致等应定位真实root。先审事件／publish／初始化边界；未证明需要时不建设复杂跨事件缓存。若极端保护确有证据必要，只能由统一拥有层保留原始可靠Ceiling，结合当前可靠Potential／身份推导，不缓存旧派生ACTIVE作为新资格。

普通同一合法进度episode的Potential单调；非法下降严重报错，不构造常规补救状态机。既有合法资产重组P−1／新身份episode按原获批事务处理，旧输入不得跨出新episode。

## 3. 网络正常发布与过渡保护

1. dirty立即使严格route/proof凭据失效，登记共享采集／交付责任；不会等预测“下一个变化”才登记。
2. 共享拥有层校验完整快照、signal／epoch／引用／端点及当前角色；完整可靠拓扑才发专业的正常可消费更新。错误／合法未准备的诊断状态与正常正向发布分离。
3. 专业Pull时取得该可靠版本；新的role/route变化不能被旧ACK或同值去重吞掉。同值但可用性真正恢复仍有责任完成。
4. 确认空网正常发布；失败不冒充空网。已确认route/source/身份／owner/ref/ACTIVE退出要按精确负事实路径及时处理，不能等unknownsibling，更不能借旧Carrier批准交易。
5. 当前D1仍有效并保留到获批退出。目标是共享层完成root链和可靠交付，而非给每专业UNKNOWN后让它“成功冻结”。异步确认期间旧效果自然尚未收到新计划，不等于把旧事实冒称current。
6. D2最终选择依ODP01。旧正式D2与窄Standardization例外现在不删；也不无条件接入冷归因。永久Insights／模板／L与旧派生归因严格分开。
7. 标准化先逻辑分开self与可靠remote，再由单一owner写max；直接两个全额相加错误。真正remote异常时允许使用什么旧贡献，依ODP01／过渡D1具体合同；未决不伪造默认。

## 4. 变化交付与专业接管（R2，工程方案）

- 中央状态最小是“待交付／已接管”；尝试／错误元数据独立。`AcceptChange(scope,ticket)` 必须先登记到专业own pending或同步证明无需动作，才能ACK。
- ticket含session、consumer、scope引用、单调revision，不带整包事实／原生对象。实际字段名与容器不是Owner决定。
- FC→Bindings collect仍是中央内部搬运，不算专业接管。ACK只清对应版本的交付责任，不证明Carrier写成功，不授权奖励／扣款。
- 回调期间的新变化有新责任；旧ACK不得清它。丢ACK可同ticket幂等再次交付，不能重复业务；专业接管后的业务失败由该owner保留、报错并凭新证据恢复。
- 无ACK责任可见保留，相关新事实／可用性／合法lifecycle/init才武装再次交付；静置publish不能创造预算。成功siblings不因另一失败重复深读。
- session待办由既有初始化／已确认历史重建，不增加通用事件存档；不可逆结果仍用专属持久收据。没有可靠唤醒时报告具体缺口，不能以timer兜底。
- 可选Diagnostic不可成为Accept／drain／恢复执行依赖。业务错误状态与持久交易证据由生产owner维护，观测者只能读取。

## 5. 专业自声明订阅（R3）

四个现有专业全部迁移，使用明确composition清单：成功Start后的owner导出稳定consumer ID、existing kinds/topics、scope能力和接管入口。中央最终Bindings槽统一验证／匹配／注册，之后才sealed drain。失败Start不留下半注册；duplicate ID、非法类型、missing callback、FAILED／SKIPPED owner显式错误。

保留phase0 RestructuringSync→NetworkBridge及既有EmitDerived精确顺序；不能把基础设施次序混入无序专业列表。独有完成／历史／native-operation监听可保留并写明理由。声明只表达依赖，不自动赋予网络、GPP、资本投资或历史资格。实际代码接口由Primary制定；不遍历shared发现插件，不造大中央业务公式表。

## 6. F01–F60 批准与证据映射

以下每格均继承有效ref／确认负事实优先／首次不造值／不可逆严格原则。`ENGINEERING_EVIDENCE_OPEN` 不是批准实验结果；未明确放行的异常复用格子维持当前安全边界，若证据显示需新语义再提交Owner，不能批量默认批准。

| F编号 | 输入／用途 | v3契约 | 状态 |
|---|---|---|---|
| F01 | 科研／文化／商业基础支持：角色与真实anchor资格 | 统一ACTIVE；锚点负事实优先；不额外批准未知锚点的长期复用 | APPROVED方向；ENGINEERING_EVIDENCE_OPEN |
| F02 | 工业基础支持：基础生产相邻采样 | 不是weighted D；同ref样本复用按现有确认语义核查，不新增私有cache | ENGINEERING_EVIDENCE_OPEN；不假造具体异常授权 |
| F03 | 二级住房：普通tier存在 | 数字D不等于建筑集合；保持真实建筑移除／失格优先，复用格子未单独放行前维持现边界 | ENGINEERING_EVIDENCE_OPEN |
| F04 | 二级GPP：实际工作人口 | 合法同ref纯被动保留worker方向保留；查实际计数采样／恢复，不重开HD实机campaign | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F05 | 二级GPP：资格 | 只读统一ACTIVE；没有GPP自己的Governorfallback | APPROVED；FORMAL_SYNC_PENDING |
| F06 | 学以致用：领域D | 同ref最后确认D+其它新可靠事实重算；floor／分组不变 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F07 | 学以致用：worker计划总量 | 实际Carrier系数是per[y]，worker用于计划总量；不凭显示计算添加生产依赖 | APPROVED用途分离；ENGINEERING_EVIDENCE_OPEN |
| F08 | 跨学科：D | N/A；不会因为D引发通知就变成D公式输入 | APPROVED歧义关闭 |
| F09 | 跨学科：基础相邻采样 | 允许同ref最后确认采样，非D；不同有效引用不复用 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F10 | 跨学科：当前区域资格 | 真实完成／移除／掠夺／reference负事实优先，不能由旧相邻样本恢复资格 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F11 | 科研基础设施：D/建筑集合 | 同ref最后确认与新事实组合；可靠建筑负事实立即生效 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F12 | 科研基础设施：worker | 适用last-confirmed重算；G04的独立已确认退出优先，不用UNKNOWN=0 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F13 | 学术主持：普通建筑集合 | 适用最后确认；真实移除／失格覆盖旧集合，不把数字D替代所有资格 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F14 | 学术主持：worker | 同ref被动重算，真实资格退出优先 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F15 | 学术传统当前投影 | 历史严格可靠，ACTIVE统一；不能从当前Carrier猜年龄 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F16 | 学术传统计龄 | 永久年龄／origin／cursor严格；不补猜漏记时间 | APPROVED严格路径 |
| F17 | 科研资格共同输入 | 统一ACTIVE；不读底层Governor细节、不各自建cache | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F18 | 风雅熏陶：巨作时代 | 来自同一共享GWsnapshot；转移和失格优先；合法纯被动保护不得掩盖root | APPROVED方向；ENGINEERING_EVIDENCE_OPEN |
| F19 | 风雅熏陶：普通建筑 | 检查ordinary／位置／完成／掠夺，不使用tier数值；可靠负事实优先 | APPROVED现有语义；ENGINEERING_EVIDENCE_OPEN |
| F20 | 意义延展：巨作count/类别 | 同一版本集合派生；不能新count+旧类别拼装；未知类别不是0 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F21 | 意义延展：领域D | 合法纯被动同reflast-confirmed；域资格／可靠移除优先，具体覆盖按现有公式 | APPROVED方向；ENGINEERING_EVIDENCE_OPEN |
| F22 | 巨作启迪：时代集合 | 一致共享GW，重复同年代不增加时代；无D/worker依赖 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F23 | DialogueEffects累计total | Dialogue永久累计独立严格，不是Insights见闻 | APPROVED严格历史 |
| F24 | DialogueEffects馆藏资格 | 一致GWsnapshot的count/类别；不能拿此被动样本批准项目奖励 | APPROVED方向；ENGINEERING_EVIDENCE_OPEN |
| F25 | 时代对话项目奖励 | 当前资格、queue、quota、真实完成采样／receipt严格 | APPROVED不可逆路径 |
| F26 | 人文考察团任务 | 独立严格任务／位置／单位／完成凭据；不扩大为Expedition修复程序 | APPROVED严格路径；既有功能问题另列 |
| F27 | 见闻旅游投影 | Insights历史严格，文化所属和引用明确；不能由Dialogue层数替代 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F28 | 文化网络拓扑 | 正常只消费共享层可靠拓扑；D1过渡保护不删、须退役证据 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F29 | 文化网络来源Insights派生集合 | 真实永久Insights与旧派生贡献分开；D2最终政策待ODP01 | OPEN_OWNER_DECISION（D2）；历史严格已批准 |
| F30 | 文化网络接收资格 | 现有identity/anchor门槛，不盲复制本城ACTIVE门槛 | APPROVED原规则；ENGINEERING_EVIDENCE_OPEN |
| F31 | 文化资格共同输入 | 统一ACTIVE，不建文化Governor缓存 | APPROVED |
| F32 | 标准化组合输出 | 公式仍max；D1当前保护但不得成为正常长期本城阻塞；remote异常依ODP01 | APPROVED目标；OPEN_OWNER_DECISION（来源异常） |
| F33 | 标准化模板/L | 专业永久历史严格，当前来源资格可靠；持久旧归因不等于历史 | APPROVED；OPEN_OWNER_DECISION（D2） |
| F34 | 巨构工程学 | Lua=current玩家时代+ACTIVE/ref；静态时代定义+原生奇观时代筛选；无N/E/L、无新增Lua队列扫描 | APPROVED；STATIC当前已匹配 |
| F35 | 工程研习E | 全国不同奇观时代完整历史严格；不借E下限发奖，不从当前拥有补历史 | APPROVED |
| F36 | 工程研习L/完成 | 独立严格项目／quota／timer／receipt | APPROVED |
| F37 | 施工队创建 | 唯一completion/source/request/unit；累计差值只发现缺口 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F38 | 施工队使用 | 已锁定资产和当前目标/一次消费结果严格，未知不可重放 | APPROVED |
| F39 | 工业资格共同输入 | 统一ACTIVE，底层管理容量未来替代未实施 | APPROVED |
| F40 | 商业化角色资格 | 统一ACTIVE；已确认退出优先，极端保护不是正常未知入口 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F41 | 商业化选择配置 | 受保护Store权威，不从缓存／空表猜选择 | APPROVED严格配置 |
| F42 | 商业化本城D | 同ref最后确认D+其它新确认事实重算，不能一律冻结所有Carrier | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F43 | 商业化工作人口 | 同ref适用保留重算；先查并修复UNKNOWN→零计划root；共享事实拥有者维护 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F44 | 商业化来源资格 | 可靠拓扑+现有来源身份/ref规则，不新增未批准source等级 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F45 | 商业化来源X/旧贡献 | 当前可重建X与当时旧X归因分开；是否保留D2待ODP01 | OPEN_OWNER_DECISION；正常采集root已批准 |
| F46 | 商业化网络pending | D1只作过渡保护；正常不向专业发布UNKNOWN拓扑 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F47 | 商业信誉被动计算 | 权威历史正常必须可靠；若极端继续则统一R0，不改保存值 | APPROVED一致性；OPEN_OWNER_DECISION（启用） |
| F48 | 商业化定义/编码/ref/readback | 当前可靠校验必须保留，不当可随意stale事实 | APPROVED |
| F49 | 新风险投资R条款 | 不能沿用v2模式封锁为已选政策；启用例外时R0统一并锁定，严格例外待ODP02 | OPEN_OWNER_DECISION；FORMAL_SYNC_PENDING |
| F50 | 稳健投资独立条款 | 正常公式无R；不得因共用报价结构新增R依赖，其他门槛仍严格 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F51 | 已签资本结算 | 锁定合同／owner／due／native outcome严格；不得用新R重算旧条款 | APPROVED |
| F52 | 发展投资签约 | 当前资格、worker容量、target/price/outgoing proof严格；被动保留不授权新投资 | APPROVED |
| F53 | 发展投资已签效果 | 原承诺按既有worker退出/目标完成/owner规则；不回头重新签约 | APPROVED |
| F54 | 移民/资产重组 | 真实plan、Unit/City提交、native不可逆结果严格；A准备B确认保持 | APPROVED；ENGINEERING_EVIDENCE_OPEN（UI） |
| F55 | Claim永久认领 | 真实原生提前完成合法，不要求内部timer；candidate/ref/唯一receipt不放松 | APPROVED；ENGINEERING_EVIDENCE_OPEN（事件真实性） |
| F56 | 机构实际收益显示 | owner实际applied/原因/来源；candidate不冒充current | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F57 | 旗帜ACTIVE | 只投影统一接口；未知是错误或明确未准备，不由UI补推总督/资格 | APPROVED；ENGINEERING_EVIDENCE_OPEN |
| F58 | 机构结构/历史UI | same-ref展示连续性与当前ACTIVE／收益分开，不给业务授权 | APPROVED |
| F59 | P0/诊断 | 稳定只读观测，移除不改变生产；生产错误状态不能只存在可选trace | APPROVED；ENGINEERING_EVIDENCE_OPEN（G30） |
| F60 | 全部不可逆客户端 | 严格当前授权/receipt；唯ODP02可明确新增R0业务例外，不能靠retained/ACK授权 | APPROVED严格原则；OPEN_OWNER_DECISION（窄例外） |

## 7. 生产／诊断隔离契约

生产包含事实采集权威、历史／通知／Carrier／事务／生命周期清理、原生写屏障和必要Flight bookkeeping；它们不得依赖可选trace factory／Collector存在。已有GC控制属已批准运行政策，先分离明确owner，不能随诊断删除改变策略。

后续disable/remove差分使用相同初始状态的独立夹具：诊断开、关闭、模块／global真实不存在三组；比较启动、ACTIVE、历史／收据、Carrier集合、Money/Unit结果、通知／恢复和typed业务UI。允许消失的只是诊断数据和监听。不能在实机重放不确定扣款／创建来“对照”。先迁移仍有生产职责的Probe再删，不能仅靠ENABLED=false通过就宣布可移除。
