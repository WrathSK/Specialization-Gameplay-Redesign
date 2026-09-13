# Specialization v0.1 Architecture — A0111

Document Owner: Codex
Architecture Revision: A0111
Design Spec Synced Through: D0014
Design Spec SHA256: 759365dd68c3b4a166b0f05e250b72f14e33dcc145c3889f6afefa16f999005c
Latest Accepted Design Revision: D0014
Latest Accepted Design SHA256: 759365dd68c3b4a166b0f05e250b72f14e33dcc145c3889f6afefa16f999005c
Sync Status: SYNCED_WITH_LIMITATIONS
Implementation Build: P0-B-051 / modinfo67

## CURRENT AUTHORITATIVE STATE

本版为交接同步，仅整理HOW，不改Source/Design。规则引用Accepted Spec；验证/下一任务由[Status](../Status/Specialization_P0_Status.md)统一维护。真实收益已运行，许多旧文件名/注释仍带Probe/DEV，这是部署边界而非“全部只是读取”。

## 运行结构

模块路径相对于README中唯一运行Mod根；加载关系以SpecializationP0.modinfo及Gameplay.lua实际include/Start为准。

| 层 | 实际入口 | 职责与当前边界 |
|---|---|---|
| 测试载体/门控 | Data/Identity.sql、Frontend、Probe.lua:IsTestPlayer | 独立测试文明/领袖；当前消费者仍固定测试资格，不是已完成ELIG通用多玩家适配 |
| 新城与首次完成 | BindingProbe、CityJournalProbe、FreshBindingHook、CityFlowProbe | 双侧绑定与City Property阶段写入；普通新城按有效完成通知锁定，已有匹配正常存档恢复；不凭现有区域猜缺失历史 |
| 统一当前专业事实 | EffectiveFacts.lua | 合并foundation与投资账本；读取当前总督门槛得到ACTIVE；身份锚点含owner，完整征服继承尚未支持 |
| 移民投资 | InvestmentAction、UnitActions、UI/UnitPanelActions | Prepare不消耗；Confirm复核后INTENT→单位消费确认→提交；重复/上限/失效处理，旧未确认INTENT不盲重扣 |
| 工作专家/本地效果 | ResearchSupport、IndustrySupport、Lv2Housing、Lv2GPP、Lv3Support、Lv3Effects、Lv4Percent | 原生隐藏建筑/Modifier及基于工作人数的绝对状态；部分实际率可延迟到下回合刷新 |
| 商路来源 | UI/BackgroundRoutes、ShadowRouteState、NetworkSender | 后台City:GetTrade():GetOutgoingRoutes完整集合；无需打开贸易窗口；名称含shadow不意味着当前未桥接 |
| 游戏侧网络 | NetworkBridge、TradeRouteProbe | seq/epoch/turn/signal、端点归属与CountOutgoingRoutes核对；当前source/center/recipient重建；不是历史事件当路线事实 |
| Lv4固定复制 | UI/CopyYieldRefresh、CopyYields、Lv4CopyRead、Data/CopyYields.sql | 背景Actual采样→Gameplay复核→绝对city层收益；界面独立复核与实际配置分开显示 |
| Crew | CrewProjects、ConstructionProbe、UnitActionSitePolicy、UnitTargets、UnitActions、CrewPrecision及对应UI | 五项目原生完成产队；实际合法区域/建筑/奇观地块；限额生产力、消费和超额浪费，单位面板确认与地图目标标记 |
| 保留实验 | YieldCarrierProbe、HalfYieldProbe及旧P0读取 | 与正式自动机制区分；Half ON额外实验会污染本轮对照，测试前Half OFF |

## 持久事实与派生状态

CityFlow使用SPC_DEV_CITY_FLOW_B020；EffectiveFacts/投资使用SPC_DEV_INVESTMENT_LEDGER_V1。底层仍依赖BindingProbe与B015 journal，不重命名Property或把旧DEV表无条件迁移成可信历史。阶段读回/停止模型可在DevelopmentTests找到，但不等于崩溃恢复、跨OwnerUID和全部历史连续性已解决。

专业/潜力/投资是持久事实；当前总督、来源/中心/接收集合、输出及载体是派生状态。未来标准化ledger也应保存城市永久掌握记录，当前网络模板并集另外计算。不得以旧内部建筑或过去商路事件补造当前连接。

## 后台商路与网络

用户已接受后台UI/BTS同源读取；禁止的是需要手动打开UI。正式运行来源是UI中的CityTrade当前列表，Gameplay可确认数量/任务但未找到完整可靠端点枚举；不要重新强求纯Gameplay作为开发前置。

传输行含op/oc/dp/dc/trader，边界128条、16384字符；当前按trader去重，端点用当前owner/cityID映射，非永久跨Owner城市UID承诺。发送包验证epoch、seq、回合、dirty signal及Gameplay CountOutgoingRoutes，再derive。计数相同不证明路线端点相同，因此仍需完整源快照。事件只促刷新；UNKNOWN不能当有效空网或保留旧奖励。

NetworkBridge派生direct中心来源与distribution recipient；D0009 direct即接收，首都self特殊来源；仅分发接收不形成递归direct relay。ConnectedKinds服务Commerce III，RecipientSources服务Industry IV。Research/Culture Strength模型仍在离线Tests，尚无正式Boost应用。

## 收益与精度

Base用于Industry I/III；Actual复制采用district:GetYield六yield口径，不是仅政策后相邻，不是city:GetYield。B051.67按D0014枚举所有已完成区域，科研排除Campus，不再按四专业或RequiresPopulation过滤；市中心也在枚举。Industry IV仍只从有效IV源锚定IZ取实际生产力，按输出金额max。未完成不计、无产出贡献0，缺失数据明确拒绝。

CopyYields.Plan支持0..65535.5范围内整数/半点，半点人口1..255。整数正负二进制位+per-population系数补偿，80个独立InternalOnly建筑；先撤旧再加新、重复不写相同状态。更细小数明确技术限制，不套Crew取整。消费者使用当前ACTIVE及真实网络；后台事件发布/播放/加载/回合入口和初始化fallback，计时器仅补充。读报告不写入收益。

城市百分比由引擎作用。新范围尤其市中心/Mod区域是否把本项city层收入返回district getter，仍需原生反馈观察；不静默排除类型，也不假定绝对覆盖足以防环。B051.67单项测试仍待用户。详细证据见[技术索引](../Reports/Technical/README.md)。

## 下一实现策略与边界

标准化：D0013的学习触发与首次补录已定。以现有StandardizationLedger离线契约为起点，明确允许建筑目录，再接一次初始化和事件目标增量复核；不要持续扫描。HD明确Tier不等于所有建筑已被批准，50条四区域目录只是研究样本。永久UID/迁移/捕获边界必须明确，不能承诺当前owner锚点已支持征服。Gold-only价格必须独立验证，不能退款代替。

Commerce IV尚无正式汇聚。保留Eligible Local Basis策略接口；用户允许困难时研究总量备选、前提防递归，是条件授权，未采用为Accepted Spec替代。不能简单从含倍率最终总量减名义跨城输入。Boost/GW也未接收益；不将半点路径成功当成sqrt百分点、Tourism/theming全精度已解决。

Conquest三分支/ELIG通用系统已有离线模型，未接完整原生流程；多个已启用玩家/多人确定性及非参与者扫描成本仍待集成。部分旧模块周期遍历所有玩家，不符合最终ELIG-004成本目标，不将其合理化为设计变更。复制模块已限制周期参与者，仅生命周期做休眠载体清理。

## HISTORICAL NOTES

[此前A0110全文](../Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_fresh_agent_handoff.md)保留全部旧调查/阶段与来源链接；其中A000x等待、纯Gameplay阻塞、无正式收益、四区域复制限制等不再代表当前。精确原字节另存本轮DevelopmentBackups。既有Historical及结果原件未改。
