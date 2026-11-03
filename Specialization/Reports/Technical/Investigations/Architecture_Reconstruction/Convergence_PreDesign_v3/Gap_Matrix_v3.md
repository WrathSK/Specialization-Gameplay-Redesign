# Gap Matrix v3 与源码证据

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[决定登记](Decision_Closure_Register.md)｜[F合同](Fact_Subscription_Contract.md)｜[PU](Pre_U5_Final_Candidate.md)｜[O计划](Option_B_Final_Candidate_Plan.md)

## 1. 基线／证据边界

当前HEAD比v2源码基线`0c9c60e`只增加七份v2报告；从v1源码`920b4ed`起生产/测试/tools/formal均未改。本包分类改变来自Owner新目标和更精确阅读，不是修复。H3输入文件SHA256：`c0d0918647a77c8d1b4c10bacdb18bb7b5c99c3b720f5ce4e30e7137eda800ab`；hash不等于备份或独立权威。

`STATIC`=当前源码/正式文本；`LOCAL`=具名既有夹具结果，未本轮重跑；`USER_NATIVE`=原已记录用户场景，未重新读原档；`UNVERIFIED`=未知/推断。没有新测试、原生实验、日志批次分析、探针、DB/HD扫描、性能归因或footprint专项。

## 2. G01–G30

G01–29沿v2；G30是H3 P3下复核出的实际加载/职责耦合，不是Modifer数量发现。每行明确正常root已证或待证。

| G | 领域 | 正常根因／现状 | 目标责任 | 证据可靠性 | 候选方案 | 停止条件 | 影响/验收包 | 源码 |
|---|---|---|---|---|---|---|---|---|
| G01 | NET1 | 历史signal-only去重根因已修；本轮无变化 | 正常samevalue重证保留 | STATIC+既有LOCAL/USER_NATIVE范围 | 保留Sender三信号门槛，不用retained掩盖传输 | 旧ACK/重放保护被放宽则停 | O3依赖基线 | S04 |
| G02 | NET2 | 历史cold首发flight缺重发已有限修复；原生掉包具体点未证 | 有限就绪event恢复 | STATIC+既有LOCAL/ordinarynative | 保留两namedlifecyclebudget；O3可靠发布不要重开此缺陷 | 需要timer/无限retry则停 | O3 | S04 |
| G03 | 商业worker零计划 | 错误allowlist不含workerUNKNOWN；真实getter失败root未知 | 共享事实+专业重算 | STATIC可达，无新native复现 | PU01根因+错误不归零；O1/商业同refD-worker重算，非永冻Carrier | 需私有cache/新权威则停审 | PU01/O1 | S03 |
| G04 | 确认退出优先 | ACTIVE断言遮挡D/anchor负事实路径；组合原生未证 | 统一事实/精确effectexit | STATIC顺序，工程证据开放 | PU04证明currentnegative独立可靠才窄修；不UNKNOWN=0 | 只有旧D推测negative则不改 | PU04/O1 | S03 |
| G05 | 被动输入 | v2逐格未定部分由H3批准，未批准格不能全放行 | 共享owner/专业Pull | STATIC当前READY门槛；目标APPROVED | F表同reflastconfirmed+新事实，currentnegative优先；正常root先修 | 新语义格子需Owner则停依赖 | O1 | S03 |
| G06 | ACTIVE | 当前六属性；正常UNKNOWN无新证据，PrivateGovcache不是目标 | 统一ACTIVE拥有者 | STATIC+UNVERIFIED正常时序 | 源层root/就绪发布，来源独立；极端Ceiling保护必要性先证 | 正常下降补救/各专业cache禁止 | PU10/O1 | S01 |
| G07 | 通知接管 | 当前计attempt不是ACK，centralcollect非owner接管 | 中央交付/专业完成 | STATIC | R2可靠登记后ACK、revision防吞新变化，ownpending复用 | 中央重放发钱发unit/无界retry则停 | O2 | S02 |
| G08 | 通知水位 | lastNotifiedProof先于fallibleEmit | Bridge/协调责任 | STATIC错误路径 | PU03窄修登记水位+真实恢复；O2全链 | 只挪赋值无唤醒不验收 | PU03/O2 | S02 |
| G09 | cold来源归因 | 旧派生Model/Cell/Store未接生产，不是永久历史 | 网络事实/效果归因 | STATIC现状；Owner未决 | 先ODP01分A/B/C；不能自动接线或删除 | 无具体cold异常输出规则不得final | O3 | S05 |
| G10 | D7/错误 | 合法隔离/确定修复/deferred已在；v2全面基线恢复目标撤回 | 专业历史/Store | STATIC；FORMAL_SYNC_PENDING | 保留有证据合法机制，错误root显式，无全面reset | 猜origin/age/receipt或silentHELD结项禁止 | O4 | S07 |
| G11 | 首次完成 | target解析先相关性，completionErrorsticky；正常发生未证 | 完成事实/Store准入 | STATIC+UNVERIFIEDnative | PU07时机/ref/参数root，不猜first顺序或清error | 需新持久见证先证明必要另批 | PU07/O4 | S07 |
| G12 | 工业E | 完整coveragegate匹配批准；coverage错误root未修证 | IndustryHistory/Study | STATIC；既有故障测试 | 保持严格E，追采集/提交root，不下限绕过或当前拥有补史 | 假造E/层数禁止 | O4 | S08 |
| G13 | Claim提前完成 | 真正early是有意支持，不是缺timer缺陷；cancel完整语义未知 | Claimbusinessowner | STATIC+既有直接完成fixture | 保留nativeearly，candidate/ref/uniqueproof；PU09只验真实事件 | 移植Narrative参数/新增timer资格禁止 | PU09/O4 | S09 |
| G14 | Crew唯一proof | playercount+1可能两城都拒绝；recordedLOCALcounterexample，native时序未知 | Crewsource/order/unitowner | LOCAL既有+STATIC当前机理 | PU05先可信uniqueproof，后grant；不能按差值补单位 | 无proof停依赖，不能弱化D5 | PU05 | S10 |
| G15 | appliedUI | 已有publication部分，UI仍age/L候选算术 | effectowner→typedUI | STATIC | O6真实applied/gate/provenance，不用candidate当current | 缺owner结果不得编展示值 | O6 | S12 |
| G16 | 历史分工 | Store仍业务分支，独立Industry/Crewowner正式存在 | 专业纯规则/Store可靠提交 | STATIC | O4迁转换，不改变结果；opaque/CAS/readback保留 | 改生命周期结果需Owner | O4 | S07 |
| G17 | 身份/实例 | 当前单实例/匹配anchor真实边界 | 城市历史/实例资格 | STATIC；未来M1/M2未批 | 保持现边界，普通Potential单调，合法重组新episode例外 | 不提前选多实例/未来容量 | O1/O5 | S07 |
| G18 | 自声明 | 中央phase1list+散kindgate，全部四专业迁移 | 专业声明/中央匹配 | STATIC | O5成功Start导出/最终slot校验/失败隔离，共享能力只注册一次 | 自动插件/隐式业务资格禁止 | O5 | S02 |
| G19 | 严格事务 | 现有CAS/readback/stagedreceipt是真生产职责 | 业务owner/Store/native | STATIC+既有相关结果 | 保留no-replay；ODP02是唯一待审R窄例外，不扩其它unknown | 不确定原生结果不能重演 | 全包 | S06/S07 |
| G20 | 直接监听 | 独特完成/历史/原生操作需要原始证据 | 各owner | STATIC，signature有UNVERIFIED | 保留不可替代职责，只迁真正重复采集/wake | 不能按数量判断违规 | O2/O5/O7 | S09/S10 |
| G21 | 无效工作 | 已知wholecatalog/重复入口等workshape，CPU成本未测 | fact采集/consumer范围 | STATIC，非footprint审计 | O8实际消除已证冗余，必要proof/历史发现保留 | 性能理由不能丢合法变化 | O8 | S14 |
| G22 | 旧生产职责 | Probe/Dialogue/timing等仍loadbearing，Halfpositive已退 | 明确生产owner | STATIC | O7Q1–Q8搬职责再删，不能永久并存 | 按名删/未接caller禁止 | O7 | S13 |
| G23 | 删除安全 | stable拒extras；temporary事务强但无等价removed-diffreview | 部署事务工具 | STATIC | 首次删文件前两个工具审exactdeletedset/receipt/rollback/failpoint | 未知文件默认删禁止 | O7 | S15 |
| G24 | 正式同步 | 当前formal尚旧，H3目标不同，历史不改 | 正式D/A审批 | STATIC+FORMAL_SYNC_PENDING | FS逐条提案，决定后分配revision，未应用 | 报告不能自行覆盖formal/实现 | 正式同步门禁 | S16 |
| G25 | 性能证据 | 无新CPU/RAM/速度归因，局部结果不能全绿 | Primary验证/Owner感受 | STATIC既有记录/UNVERIFIED新量化 | 必要工作/最小浪费，真实闭包和有限native；无任意KPI | 不等待或引用独立footprint结论 | O8/PU11 | S14 |
| G26 | A/B按钮 | guard静态缺；native映射症状已报但helper未复现 | UIpreparedplan/业务confirm | STATIC+USER_NATIVE报告范围 | PU02guard+真正routing原因，B唯一confirm | 盲swapcallback禁止 | PU02 | S12 |
| G27 | 已延后范围 | PT017/18、multiitem、HDGPP、ownership等有明确边界 | 原各owner/项目 | 既有记录 | 不扩大修复/测试campaign；未改路径证据保留 | 未经授权新功能禁止 | 本计划边界 | S16 |
| G28 | 迟退出/夺回 | foreignloss.target可能回归后已不合法；不止漏wake | Storeepisode/各exitowner | STATICfence，最终native未知 | root区分窗口/bug/无效端点；合法延迟才事件接续 | 旧回调跨新owner/ref禁止 | PU08/O4 | S07 |
| G29 | 信誉跨用 | R0数值已流入新quote；目标改为统一容错条件，旧v2模式政策撤回 | 信誉历史owner/业务quote | STATIC；OPEN_OWNER_DECISION | ODP02确定启用/正式例外，严重root可见、原record/旧terms不改；Stable无R | 未决不默认选择模式禁用/自动例外 | PU06/O4 | S06 |
| G30 | 生产/诊断耦合（新增） | Bridge直接加载/构造trace；P含写屏障，Counters混Flight/GC | 生产kernel/可选observer | STATIC依赖，未执行absence故障 | O2/O5/O7提取生产和必要GC职责，diagnostic仅只读；真实disable/remove差分 | 不能只ENABLED=false或无脑删Probe/改GC | O2/O5/O7 | S11 |

## 3. 源码与正式合同索引

所有路径为repo相对；省略前缀的同格Lua basename归`Mod/`，UI明确标`Mod/UI/`。行号固定为本包sourcebaseline；source定位存在不等于语义/原生行为已证明。

| S | 当前定位 | 支持的有限结论 |
|---|---|---|
| S01 ACTIVE | Mod/Probe.lua:320–346; Mod/Data/GovernorProbe.sql:2–56; Mod/EffectiveFacts.lua:114–121/210–218/232–239; Mod/NativeFacts.lua:59–64; Mod/RuntimeWork.lua:459–468; Mod/Gameplay.lua:837–848 | 六原生属性、nil语义、NORMALceiling1、统一入口现状和publish边界；未证真实UNKNOWNroot，不假设在callback内深读 |
| S02协调 | Mod/FactChanges.lua:105–114/164–173/182–203; Mod/FactConsumerBindings.lua:11–46/52–122; Mod/NetworkBridge.lua:103–109/133–144; Mod/RuntimeComposition.lua:46–75; Mod/Gameplay.lua:1029–1036; Mod/RuntimeWork.lua:59–76/226–231/265–290 | attempt≠ACK；phase0与newRegister隔离不自动继承；当前水位先登记漏洞 |
| S03能力 | Mod/ResearchApply.lua:26–50/72–75; Mod/ResearchCross.lua:4/46–74; Mod/ResearchCrossSample.lua:20–52; Mod/ResearchInfrastructure.lua:31–54; Mod/ResearchChair.lua:34–47; Mod/Lv2Housing.lua:20–40; Mod/Lv2GPP.lua:43–65; Mod/Commerce.lua:123–165/323–356; Mod/GreatWorkFacts.lua:177–195 | current输入与获批重算差异；Cross无D，Applyper系数vs总量，住房tiers；workererrorbranch；GWsnapshot一致性 |
| S04网络正常链 | Mod/NetworkSender.lua:19–78; Mod/NetworkInput.lua:22–109; Mod/NetworkBridge.lua:103–109/133–144/215–235/303–400/620–660; Mod/UI/BackgroundRoutes.lua:213–241 | 已修NET1/2保留；当前仍发布pending/mixed/negativecontinuity，正常可靠-only是真迁移；strict接口不放宽 |
| S05 D2/标准化 | Mod/Commerce.lua:240–279; Mod/CultureNetwork.lua:15–25/137–173/308–314; Mod/NetworkRecoveryModel.lua:26–66; Mod/NetworkRecoveryCell.lua:76–120; Mod/NetworkRecoveryStore.lua:9–45; Mod/StandardizationEffects.lua:6/65–98/165–207; Mod/Data/StandardizationEffects.sql:23–29; Mod/Data/EngineeringStudy.sql:7–25 | 旧source归因为派生凭据非永久成就；当前值可重建但旧应用不能倒推；单一物理max不可两全额相加，未证需物理拆分 |
| S06信誉/交易 | Mod/CityProgressionStore.lua:521–524/1127–1141; Mod/Commerce.lua:24–31/151–155; Mod/CapitalInvestment.lua:182–184/343–345; Mod/CapitalInvestmentModel.lua:135–163; Specialization/Design/Content/Commerce_D0058.json:263/281/293; Specialization/Architecture/v2/Commerce_Preparation.md:200 | 有效parent的信誉leaf隔离可投影0；统一R0候选与原strict原则需精确例外，非正式绝对VENTURE禁令；Stable数学不依赖R |
| S07 Store/lifecycle | Mod/StoreSubrecords.lua:100–201; Mod/StoreLifecycleRecovery.lua:14–63; Mod/CityProgressionStore.lua:340/404–438/736–778/823–825/1061–1169/1175–1179/1255–1278/1306–1395/1413–1428/1563–1592/1977–1985/2102–2140; Mod/RestructuringModel.lua:79–94 | 现有可靠机制与业务分支、stickycompletion、foreignfence、合法重组P−1/新episode；不能清零/猜史/盲重放 |
| S08工业 | Mod/IndustryHistory.lua:48–61/180–210; Mod/EngineeringStudyProjects.lua:129/147–150; Mod/IndustryWonderEffects.lua:5–6/30–32/50–65; Mod/Data/EngineeringStudy.sql:29–41; DevelopmentTests/test_b235_engineering.py:189–199 | E严格历史；WonderEffects不读N/E/L/当前queue，native按时代filter；现有fixture只读取未运行 |
| S09 Claim | Mod/ClaimProjects.lua:111–139/144–197; Mod/Data/ClaimProjects.sql:4/7/10/13; Mod/CityProgressionStore.lua:872–897; DevelopmentTests/test_b124_claim.py:59–60; Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Architecture_Audit_B396.md:419/639 | cost1000000普通计时与intentionalearly兼容；NarrativebCanceled不代表Gameplay参数；native完整signature未知 |
| S10 Crew | Mod/UI/CrewProjectUI.lua:14–35; Mod/CrewProjects.lua:265–294; DevelopmentTests/test_refactor_s7d6_proof.py:23–50; Specialization/Status/Validation/Results/Refactor_S7d6_Crew_Proof_Gap.md | playercounter非cityproof；既有LOCAL0not2counterexample；晚到历史可发生性仍未证 |
| S11 P3 | Mod/NetworkBridge.lua:5/41–54; Mod/IndustryWonderEffects.lua:4; Mod/Probe.lua:553–569; Mod/NetworkSender.lua:8/19/29/71/78; Mod/PerformanceCounters.lua:128–147/236/338–351; Mod/Gameplay.lua:24/1014 | pcall参数求值前global访问不受保护，directNew/include；P生产writebarrier与Counters Flight/GC混合；不统计规模、不改GC政策 |
| S12 UI | Mod/RestructuringUI.lua:38–47; Mod/Restructuring.lua:203–225; Mod/ResearchTraditionEffects.lua:68–84; Mod/Gameplay.lua:249–281; Mod/InstitutionPresentation.lua:59–101; Mod/UI/InstitutionOverview.lua:25–36; Mod/UI/LevelBannerModel.lua:5–11 | Aguard与nativeclick原因不同；applied/candidate分离；UImirror不是事实/交易权威 |
| S13旧职责 | Mod/Gameplay.lua:862/874–876/906–930/995–1012; Mod/EffectiveFacts.lua:80; Mod/CityFlowProbe.lua:18/126–129; Mod/ConstructionProbe.lua:7–26; Mod/CultureInspiration.lua:70/198; Mod/Dialogue.lua:38–61/298–327; Mod/UI/DialogueRefresh.lua:26–46/94–99; Mod/SpecializationP0.modinfo:50 | Q1–Q8实际reader/writer/ACK/清理等，filename/retiredpositive非可删除证明 |
| S14工作证据 | Mod/UI/DialogueRefresh.lua:55–81/110–122/147; Mod/DistrictCompleteness.lua:69–100/182–240; Mod/PerformanceCounters.lua:155–165 | completecityproof与selectiveslots、Dcache/wholecatalog、有限export；workshape非CPU/RAM归因，无footprint专项结论 |
| S15删除 | tools/deploy.py:35–56; tools/temporary_playtest.py:37–94 | 两路径交易/删除审查不同，须受审exactremovedset与回滚，未执行 |
| S16正式/状态 | Specialization/Design/Specialization_v0.1_Design_Spec.md:20–26; Specialization/Design/Network.md:47–59; Specialization/Architecture/Specialization_v0.1_Architecture.md:16–27/138–175/634–646; Specialization/Status/Specialization_P0_Status.md:1–27 | Owner目标与当前formal区别；现行D/A/Status未改，U5未开始 |

## 4. 既有测试/原生证据复用边界

B397 Network Proof Transport的87项选定LOCAL结果、B395科研文化/B397工业/B399 Fifth和Coverage结果仅保留其具名场景；既有失败／nativeunknown继续有效，没重新执行。CrewOpenProof的PASS是缺口复现，不是D5PASS。test_refactor_s9f4、test_store_write_boundaries、test_refactor_s8c5c、test_great_work_notifications、test_refactor_s9g1–g4的已有机制是基础，不证明新目标已通过。

本轮只有新报告写入和文档QA；没有fixture、Lua/native/SQL实验、failureinjection或新的USER_NATIVE。全部源／正式／旧报告保持原字节。后续每个改变路径按计划重新验证，不能自动继承历史PASS。

## 5. 内部复核与文档检查

九份中文候选已完成三条独立定域内部复核；修正了统一ACTIVE只拥有当前投影/派生、不替代Store永久权威的说明，并把通知与反向接管ACK画为两条箭头。内部复核不是Claude Code外部审计，也不关闭Owner决定或未执行的技术证据。

文档QA：40个内部报告链接、113组源码定位存在且行号在界内；F01–60、G01–30、PU01–11、O1–8、DEC01–14、R1–6、FS01–12覆盖/顺序/唯一性核对通过。两幅Mermaid仅做结构/箭头含义审阅，未执行renderer；源码定位检查不证明所有语义或原生行为。H3 hash、源码HEAD及既有tracked/index在显式报告暂存前保持不变。后续发布另走staged隐私/凭据检查，不把此QA写成玩法测试PASS。
