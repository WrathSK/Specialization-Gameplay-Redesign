# 玩家启用资格载体与城市事件接入准备

Document Owner: Codex
Design Reference: D0007 / ELIG-001..006 / PROG-004
Architecture Reference: A0025
Scope: READ_ONLY_CANDIDATE / NOT_DEPLOYED

## 本轮结论

STATIC_CONFIRMED表示本机代码/数据库证据，不等于实机运行。HD确实在Gameplay通过PlayerConfigurations与GameInfo.CivilizationTraits查询玩家Trait，modinfo确认上下文。当前Identity.sql已定义TRAIT_CIVILIZATION_SPC_TEST并只绑定测试文明，可以作为当前显式启用载体配置；核心读取器接受Trait参数，不硬编码文明、领袖或Human。本轮不改变绑定，不启用其他玩家。

LOCAL_SIMULATION_PASS表示本地模拟，不等于游戏通过。新增EligibilityCarrierCandidate.lua直接使用上述API形状，只读；test_eligibility_carrier.py覆盖正常/无绑定/未就绪/读表中断/重新建立读取器，以及内存SQLite执行实际Identity.sql中的两张资格相关表。没有运行整套Civ数据库，也未证实本候选在实际Gameplay的初始化时序。

## 静态证据位置

本机HD根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070`。
原版Assets根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets`。

| 文件与行 | 观察 | 能证明的边界 |
|---|---|---|
| HD Gameplay/CivilizationTraits.lua:6–32 | GetCivilizationTypeName + CivilizationTraits遍历 | Gameplay有静态数据库查询先例，不是动态effective Trait全集API |
| HD DL.modinfo:1867–1875 | DL_Scripts_Gameplay加载CivilizationTraits.lua及Misc.lua | 并非UI wrapper冒充Gameplay |
| HD Gameplay/CivilizationTraits.lua:17、45 | `_CAPTURED` Player Property为true也判拥有Trait | 通用HD helper含额外语义，不能无审查直接作为系统启用入口 |
| 当前运行Data/Identity.sql | Traits及CivilizationTraits显式绑定 | 当前载体已存在；数据库中原版Scotland没有被本SQL赋予此Trait |
| 原版DLC/AlexanderScenario/Scripts/AlexanderScenario.lua:174、248 | CityConquered(capturerID,ownerID,cityID,x,y)及注册 | 原生Gameplay征服事件先例，未证明涵盖交易/解放/忠诚变化 |
| 原版AlexanderScenario.modinfo:59–61 | AddGameplayScripts | 明确事件使用上下文 |
| HD Gameplay/Misc.lua:764–770 | CityBuilt、CityConquered转调城市处理 | 新旧owner/新cityID/位置可做重新核对信号，不构成永久UID |
| 当前BindingProbe.lua:121–122、CityJournalProbe.lua:154 | CityBuilt与LoadScreenClose | B015已有实机证据范围见Status；不扩展为本候选已通过 |

## 只读候选契约

`New(env, trait).Read(player)`不依赖本地UI、不调用GetLocalPlayer/IsHuman/GetCities/GetProperty、不持久保存资格；每次重新读取当前配置和完整绑定表。返回contextSource=GAMEPLAY_CANDIDATE，状态ENABLED/DISABLED/UNKNOWN，以及诊断carrier/civilization/reason。不能直接当作MOCK_ONLY核心输入或已通过的Gameplay事实。未来探针须显式记录实际调用上下文。

无匹配只有在玩家/配置/载体定义/表完整读取后才是DISABLED。配置缺失、空文明名、未定义carrier、迭代中断均UNKNOWN，即使中断前已找到匹配也不宣布成功。没有旧ENABLED缓存退路。

当前技术配置仅采用显式CivilizationTraits绑定；不自动采纳HD `_CAPTURED`，也不把LeaderTraits继承或动态Trait授予伪装成已支持。后续要增加其它授予方式，应独立定义可审计的资格来源；此处没有改变Design或限制未来载体。没有实现运行中资格开关或新增玩家UI。

## 生命周期接入顺序（准备，未注册新事件）

| 时间点 | 资格与运行处理 | 永久事实处理 |
|---|---|---|
| Gameplay初始化/LoadScreenClose | 先重建轻量参与者集合；未就绪UNKNOWN暂不运行，后续安全时点重试 | 不因缺失资格或旧记录为空新建/删除城市事实 |
| enabled玩家周期处理 | 使用当前有效资格再读取其城市/总督/网络；不得让disabled进入深枚举 | 只做已授权的正常操作 |
| CityBuilt | 先判owner资格，再走已有新城历史资格核对 | 不把所有AddedToMap当建城；不自动迁移DEV记录 |
| CityConquered | 新旧owner分别重新核对；旧派生状态立即失效，确认同城与新owner后才重算 | 保留原数据；缺少同城证明不转移、不清空，也不从位置猜UID |
| 城市删除或端点失效 | 原运行引用失效，不能继续发收益；检查相关参与者即可 | 不把同plot重建城认作原城；事实归档/城市终止凭据仍待适配 |
| 其它取得方式 | 交易、解放、忠诚易主的事件覆盖和参数需另查/验证 | 不宣称CityConquered覆盖所有转移 |

资格只是允许进入后续处理，不证明“从未启用且无成果”。当前配置没有绑定也不能证明过去从未参与。AcquireUnassigned所需历史凭据、跨owner同城证明、实际旧Modifier移除，仍是独立实现任务。未知资格应停止使用旧派生收益，但本轮尚无实际收益撤销代码。

若今后给真实事件接探针，优先只读记录：当前owner、资格状态及原因、新旧owner、城市定位、触发时点；不在同一批同时写征服成果。下一批只需验证无需打开UI的资格初始化/重载；未部署前不要求用户测试。

## 文件与保护

新增DevelopmentTests/EligibilityCarrierCandidate.lua、test_eligibility_carrier.py及本报告；当前入口文档更新。原有离线模型、运行包B015/modinfo22、Design、游戏配置、UUID均未改。修改前文档及保护hash在DevelopmentBackups/Specialization-before-eligibility-carrier，新增verification_result.json记录核对及本地结果。未启动游戏。

当前唯一验证/任务队列：[Status](../../Status/Specialization_P0_Status.md)。
