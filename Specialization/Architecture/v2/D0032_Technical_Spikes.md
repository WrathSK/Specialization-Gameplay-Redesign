# D0032 技术验证门禁

Document Owner: Codex
Architecture: A0160 / planning only
Baseline: B076.103; Design D0032 mixed authority map见[D0032_Adaptation](D0032_Adaptation.md)。

本表的STATIC_CONFIRMED仅确认定义/调用存在，不保证结算、叠加、时序或保存正确。所有原型均须另行授权；本轮没有创建原型或要求用户启动游戏。测试尽量复用一个小存档，只有对应批次就绪才要求一次短测。

| ID / 问题 | Design要求与当前证据 | 当前证据等级 | 最小原型 / 用户测试 / 阻塞批次 |
|---|---|---|---|
| TS01 区域完善度与普通建筑 | Shared逐建筑求和、单区域cap10、同领域取最高；现有Housing按Tier存在性，不能复用其结果；StandardizationCatalog提供HD tier/替代证据但不是完整普通建筑本体 | STATIC_CONFIRMED；目录与事件覆盖待验证 | 一个普通/特色/免费建筑目录fixture和纯D consumer，测试缺低tier/同tier多栋/掠夺修复/多区域。未来一城短测；P0-A |
| TS02 科研数值primitive | 新BASE相邻、0.5D Yield Share、每专家D Science、每座普通建筑主持收益、城市Science百分比。旧Copy实测整数/半点不意味着支持任意小数；Boost量化不能复用为城市yield规则 | TECHNICAL_INVESTIGATION_REQUIRED；旧路径证据见Yield_Precision_Backlog | 按每种modifier路径分别对照原生产出，不创造round规则。A纯计算不阻塞；C/D/F各自原型后一次短测 |
| TS03 Food Surplus -75% | 原版CitySupport.lua growth计算使用foodSurplus及GetOverallGrowthModifier；HD CityPolicies有ADJUST_CITY_GROWTH Amount=-75原生先例。存在growth modifier不等于在其它增长加成下精确净余粮×0.25 | STATIC_CONFIRMED primitive；精确叠加/负余粮 TECHNICAL_INVESTIGATION_REQUIRED | 正/零/负余粮及已有增长bonus四组对照，确认消费不变、不制造额外饥饿。若仅相加growth modifier则记录语义差异，不能擅自改Design；T1/T2需实机 |
| TS04 Production-only团队 | 原版Units支持可训练且PurchaseYield为空（如Spy）；通用文明/黄金时代/宗教购买modifier可开Faith渠道，仅置空字段不足以证明不可买 | STATIC_CONFIRMED 基础字段；PROTOTYPE_REQUIRED 通用旁路 | 原生与HD典型Gold/Faith购买解锁下实际CanStartCommand及面板；禁止仅靠隐藏按钮。T1需一次短测，未通过不得发布资产重组 |
| TS05 发展投资生产modifier | MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION有owner-city原生路径，DistrictType/Amount有静态先例；能否严格只过滤普通建筑、特色替代、叠加Standardization仍未证实 | STATIC_CONFIRMED primitive；PROTOTYPE_REQUIRED | 单目标领域普通/非普通各一项，对照建造progress、cost/purchase不变、两个bonus同时/独立撤销。R/H3依赖，需实机 |
| TS06 Project action入口 | 原生/HD ProductionPanel可定位AdvanceProject请求；现有CrewProjectOrder只排序，不能证明已实现拦截 | STATIC_CONFIRMED hook候选；UI_PROTOTYPE_REQUIRED | 一个无收益假入口，点击前拦截production请求，原队列/生产保持；一次panel快照、hover零请求。U3/P/Q/R依赖，需实机 |
| TS07 合同锁定随机结果 | 当前InvestmentAction已有意图/消耗凭据而非Commerce合同；引擎Property可存记录。无法仅凭静态代码保证扣金/保存原子性 | TECHNICAL_INVESTIGATION_REQUIRED / PROTOTYPE_REQUIRED | 独立source-city合同+pity记录，确认时roll更新，重复确认、存读档、到期重复事件、中断扣款/发款模型。UI不泄露结果。Q1/Q2需一次短测；禁用真实金额fixture直发正式版 |
| TS08 REALLOCATING | 当前Flow首次建立模型不含此合法状态；不能清空Identity后交回first-district流程 | ARCHITECTURE_REQUIRED / PROTOTYPE_REQUIRED | 持久事务独立于Team，P>=2、最少完整5T、提前就位不可配置、配置消费一次；失去Team策略尚DESIGN_DEFERRED。E2/T2需实机；不阻塞A |
| TS09 城市历史身份 | Binding token核对原owner/cityID且32累计上限。Dialogue要求跨owner城市连续性，observations要求原owner+source-city，不能把两者合并继承 | STATIC_CONFIRMED 缺口；PROTOTYPE_REQUIRED | 新cityKey与currentRef分离、旧schema迁移/冲突HELD、转移/夺回/删除/读档；没有可证明映射则不迁移。E1/E2及M/N/T依赖 |
| TS10 时代对话完整生产回合 | 当前Dialogue为即时25%×(D−1)样本投影，没有项目START-era quota/连续生产回合状态 | PROTOTYPE_REQUIRED | 一个项目跨时代开始/完成、X0、切走再回来、加生产/购买/队列/读档，必须完整连续一回合；不可用FinishProgress模拟已等满。M需实机 |
| TS11 原生Great Work收益专属倍率 | 当前整类GW modifier有实际文化/旅游路径；新Design涵盖native yields且明确排除Meaning追加，原生modifier是否同时放大追加需验证 | STATIC_CONFIRMED 分类modifier；PROTOTYPE_REQUIRED 结算隔离 | 同作品native与独立追加各有可辨值，检验倍率/theming/旅游。不能默默把Tourism-only fallback当最终Design。M需实机 |
| TS12 每件作品0.1 base GPP | Lv2GPP整数载体已验证；不能证明0.1能进入base且吃其它GPP倍率；大预言家映射已确认，不接管引擎溢出 | TECHNICAL_INVESTIGATION_REQUIRED / PROTOTYPE_REQUIRED | 1件/若干件与既有GPP multiplier对照，读累计base与结算差；L3需实机，不按显示整数猜丢失 |
| TS13 人文考察交互 | Spy-like UI/部署可研究，但原生Spy敌对、宣战撤回/失败机制不代表Design授权 | TECHNICAL_INVESTIGATION_REQUIRED / UI_PROTOTYPE_REQUIRED | 训练source绑定、合法major三类目标、战争前后部署/任务、目标失效取消无奖励、固定成功单位保留、2T速度floor、ACTIVE下降继续记录。N1/N2逐阶段短测；不得静默继承capture/death |
| TS14 整城Tourism倍率 | MODIFIER_SINGLE_CITY_ADJUST_TOURISM存在；需要证明涵盖城市总Tourism而非仅GreatWorks/特定来源 | STATIC_CONFIRMED primitive；PROTOTYPE_REQUIRED | GW和另一种Tourism来源同时对照，ACTIVE4暂停/恢复，原owner转移边界；N2，需实机 |
| TS15 Hybrid D与GW事实 | GreatWorksOverview/GW移动事件、HD tooltip候选可复用；当前UI样本并非所有新eligibility/history已实现 | STATIC_CONFIRMED 候选；UI_PROTOTYPE_REQUIRED | supported Work+Artifact不同era、创建/移城/交易/转移仅更新受影响城市+国内索引；hover零request，分辨率/HD布局一次短测。K/U2 |
| TS16 Team source与capacity | 当前Crew项目直接原生授予单位；UnitActions有消耗凭据，没有可靠source registry/capacity=2生产门禁 | STATIC_CONFIRMED 缺口；PROTOTYPE_REQUIRED | 完成绑定source，含读档/重复完成事件/同回合双完成、排队完成时容量、合法移除释放一次；所有tier1slot、ACTIVE下降/转专业不删队。捕获/易主仍Design待决；队列并发满槽时如何处置既有Production若涉及损失/返还，不由Architecture擅定。J1需实机 |
| TS17 Standardization最终双路径 | 当前为模板建筑匹配+购买折扣；新区分本地/网络知识、独立最高construction/purchase效率、区域模板；没有完整生产路径 | STATIC_CONFIRMED 旧代码；PROTOTYPE_REQUIRED | 2source知识/效率不同、本地III、一个Gold/Faith资格目标+生产目标，union与独立max；生产与发展投资叠加按TS05。H1/H2/H3需实机 |
| TS18 Wonder完成历史 | 当前未提供全局从开局记录实际完成文明/来源城的账本；仅读当前Wonder持有者无法正确追溯征服 | TECHNICAL_INVESTIGATION_REQUIRED / PROTOTYPE_REQUIRED | 完成事件签名、cityKey、Wonder own era、重复/加载，提供安装前历史缺失诊断；G/I2/I3需实机。未知历史不能从现Owner反推 |
| TS19 群体专家与Housing | 新支持基础数值部分可复用；Housing tier-presence与区域完善度不同，掠夺不受益及多特色实例需统一事实 | STATIC_CONFIRMED 现有载体；PROTOTYPE_REQUIRED 边界 | 同一小城调专家/掠夺修复/总督，验证+3/+3全等级、IndustryBASE、II GPP及Housing；B1/B2各一次短测 |
| TS20 商业化数值/信誉 | authority明确source strongest和LIFO，但各领域source value/公式以及信誉具体影响未冻结 | DESIGN/BALANCE_REQUIRED（非技术替代权） | 先只做route/quote框架与诊断fixture；正式能力要等相应定义。O不受阻，P/S的正式效果不能填0或照搬旧20% |

## 只读来源与限制

- `Mod/`实际调用/SQL与完整文件hash见[D0032_Runtime_Inventory.json](D0032_Runtime_Inventory.json)，不是仅从旧Status推断。
- 当前本机 `Cache/DebugGameplay.sqlite` 查询确认上述DynamicModifiers、Units和购买机制定义；本次查询中SPC Buildings数量为0，因此它不证明当前运行包已加载，也不能用它重算旧PAC1894载体。未修改DB/config。
- 原版 `Civ6.app/Contents/Assets/Base/Assets/UI/CitySupport.lua` growth显示/计算链及HD `SubMods/CityPolicies/CityPolicies.sql` 是静态线索；实际引擎结算仍要测。引用本机已安装资料，不假定其它版本相同。
- 更完整的既有Commerce静态调查见Design的Commerce D0032 Review；本轮没有提升其证据等级。
- 旧半点、整数Boost、GW独立截断属于各接口不同合同；本轮无精度改造，无把任意小数统一floor。
