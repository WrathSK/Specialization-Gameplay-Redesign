# P0-F 科研学术传统 — 分段实施计划

状态：P0-F1 B143.170限定 USER_GAME_TEST_PASS；F2 B144.171限定 USER_GAME_TEST_PASS。验收见[B143证据](../../Status/Validation/Results/Specialization_B143_F1_Pass.md)。基线为B142.169、D0036总Spec中的Research_D0031；本计划不改变Design。用户已验收模板记录与重启保持，见[B142证据](../../Status/Validation/Results/Specialization_B142_Template_Pass.md)。本页维护F1定域合同与结果；部署事实以Status及receipt为准。

## 玩法合同与依赖

正式来源：[Research_D0031](../../Design/Content/Research_D0031.json)的`RES_L4_TRADITION`及[总实施计划](D0032_Implementation_Plan.md#实施批次合同)。本城首次永久科研Potential4起累计；标准速度age0为5%，满10/20/30/40回合为10/15/20/25%，最高25%。其它速度阈值分别为floor(10*j*s)，不能先取整s或反复使用已取整的10T阈值。仍有Research Identity时，ACTIVE下降不暂停年龄；转出Research（含失去该Identity的REALLOCATING）暂停并保留，重新转回续算、不补离开时间。实际收益仅ACTIVE≥4启用。无新Balance选择。

直接依赖：E2逐城Game记录及可靠身份/投资提交、当前Research Identity/Potential/ACTIVE facts、P0-C已退出的旧Research IV百分比路径、现有定域收益/诊断与性能合同。工业模板及其原生折扣补测不是F依赖；未知外交取得、销毁同址新代、未来专业不进入本批。

## P0-F1 年龄保存与影子计算

目标：先证明“首次P4→可靠年龄→保存恢复→预期加成”链路。此批不施加新科技收益，不新建收益carrier；不重做E2或全局保存架构。完成后停在一次最小原生验收，F2另行授权。

| 范围 | 计划 |
|---|---|
| 持久authority | 在现有城市record中增加科研专属、带版本的传统记录，由Store验证/写入；字段至少表达可靠首次P4起点、累计合格年龄、最后结算位置与暂停/保护状态。不得由UI、carrier或当前CityID单独保存；最终字段在获授权后的精确调用点审查中落定 |
| 首次启动 | 只在能证明本次合法首次永久Research P4时建立记录；读取或重复通知不能重新初始化。与投资/身份提交的先后及失败续接必须核对，不允许先报成功再丢掉首次起点 |
| 计龄与恢复 | 单一结算路径按合格区间计算，重复通知/同回合读档不重复增加，暂停不补算；不受专家数或总督临时离开影响。正常读档只恢复可靠记录，不用墙钟、存档文件时间或城市名推断年龄 |
| 影子输出 | 年龄、下一阶段、若ACTIVE4时应有的百分比，以及当前是否满足收益门槛；Game Speed接口先做定向静态确认。UNKNOWN不变成0、不补发收益 |
| 诊断 | 复用按需诊断入口/缓存，显示本城起点、年龄、阶段、当前ACTIVE及暂停原因；不记录无限历史或新增hover Gameplay请求 |

可能涉及`CityProgressionStore`、首次P4的投资提交调用点、`EffectiveFacts`的必要只读入口、Gameplay启动/既有变化通知和一个科研专属模块；仅必要的P0面板报告接线。具体路径须在授权实施时读取直接源码和消费者，不由此表许可全量重构。

**两个不得猜测的边界**：

1. 当前已P4但没有可靠首次P4记录：旧投资receipt不含足够turn证据。不得按开局、当前turn或投资次数补年龄。F1测试从P3之前存档开始；无法证明起点的旧P4城报告“起点不可确认”，保留其其它既有能力。这是本切片技术支持限制，不是新增“旧城永远无传统”Gameplay规则；若以后需要支持，再提出明确方案/用户决定。
2. 跨Owner学术传统归属尚未定义。F1仅验证同Owner合同；失城仍按E2退出当前效果，保留记录并报告未决边界，不在夺回时擅自合并/激活/补算传统。不能类推工业模板的城市经验规则。Identity内的暂停/恢复规则已确认，但尚未实现的转专业动作只做本地状态合同测试，不新建转专业UI。

## 更新范围、验证和退出条件

沿用现有已确认的变更通知：首次P4、Research Identity变化、owner可靠变更、load和本地玩家回合结算。普通Governor/ACTIVE变化只改变当前启用判断，不启动第二套年龄更新；同回合真实身份变化必须按序处理。普通计算只读所需标量，诊断明细按需构造。仅核对已登记的相关科研城，失效/完成时释放临时工作；不能把每个事件扩成全玩家/全世界扫描或每帧工作。GC策略保持既有合同。

W0004 L3定域验证：首次P4原子性/重复完成、年龄0及各阶段前后、速度独立floor、同回合多事件、ACTIVE降级仍计龄、Research Identity暂停/恢复、save/load、失败写入不伪确认、UNKNOWN/其它城市隔离、未定义跨Owner不误激活；沿用直接相关E2投资/保存回归。只记录所改路径的必要工作量，不默认跑全部历史或内存长测。

最小未来实机流程（须F1实现后才执行）：复用一城P3及其独立存档，通过现有投资达P4→报告起点/age0/预期5%→短暂降低ACTIVE并过少量回合，确认影子年龄仍增加→保存完整退出/重启，确认年龄保持且同回合不重复累计。阶段10/20/30/40与全部速度边界先由本地测试覆盖，不要求用户等待40回合。若普通游戏操作难以快速降级/恢复Governor，沿现有已验证Cheat准备手段，不改正式阈值。

F1退出：本地定域通过，原生首次起点/计龄/重启保持得到限定确认；明确仍未施加收益。实际失败只收窄到对应边界，不重开性能专项。回滚用前一已知包及F1写入前存档；不保证旧代码消费新专属字段。

## 后续P0-F2：接入实际收益（本轮不授权）

复用F1已确认的年龄/阶段，只在ACTIVE4时施加本城Science百分比；实现module-owned进入/更新/退出/读档重建。先精确核查旧Research百分比writer/载体已经停用，防止old+new叠加；不复制Culture/Commerce公式。按需报告同时显示预期与实际配置。最小一城检查初始5%、总督门槛退出/恢复和冷加载；原生百分比路径若出现技术问题，报告具体边界，不修改Research Design。

F1最小实机验收已关闭；下述三步保留为原验收流程，不再派发。F2未实施且未授权。不自动进入F2、未知Legacy或其它专业。

## B143.170 — F1 implementation and validation

**原实施记录：STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；当时USER_GAME_TEST_REQUIRED，现由B143限定验收关闭。** 用户“授权实施计划”只授权F1。没有Science写入、SQL收益或新carrier，GC/Network/模板目录与折扣均未变。

持久字段为既有逐城Game record内`researchTradition={version=1,start,age,cursor,state,receipt}`；父record提供城市/owner authority。最后一笔P3→P4投资的CONSUMED_CONFIRMED→committed写入同时建立age0与receipt起点，失败不单独提交其中一半；投资确认本身的完整事务与失败恢复不变。已有P4而无起点不补造。未定义的跨Owner在已确认失城写入中标为OWNER_POLICY_UNRESOLVED，保留age；夺回不自动续算。

单一Store计龄路径在本地人类PlayerTurnActivated与LoadScreenClose处理已登记records，只对已有传统且当前ACTIVE record读取同城引用/标量身份，不扫描建筑、不读取总督/专家/完整D事实。ACTIVE等级不参与年龄计算。相同回合不重复写；同回合加载无写入；下一回合加载可结算一次。当前无转专业动作；Research→NONE/REALLOCATING→Research的有序暂停/续算在纯模型验证，未来实际身份writer须在切换时调用该合同，不能只依赖回合末发现变化。

年龄区间只接受连续0/1回合；多回合缺口不推断其身份连续性，标UNKNOWN_INTERVAL、保留age等待调查。这是原生事件/加载技术保护，不是额外玩法扣龄。未知owner/binding不写年龄；若下次可靠观察已跨过缺口，保持保护。失败只保留本record最新错误，无重试队列/无限历史。传统记录结构损坏沿已有Store规则暂停该城，不能静默重建；其它城市保持隔离。

Game speed静态证据：复用Probe.CrewAmount既有`GameConfiguration.GetGameSpeedType()`→`GameInfo.GameSpeeds.CostMultiplier/100`约定。当前只读HD数据库值Online50/Quick67/Standard100/Epic150/Marathon300。独立floor各阈值；不是先round10T。接口原生F1接线仍需下面一城测试，不据数据库或模拟宣称实机。

本地入口：`DevelopmentTests/test_b143_tradition.py`（Lupa lua55）。覆盖实际Store/Investment首次P4及失败续接、same-turn重复/按需报告零写、ACTIVE1仍计龄、冷加载、旧P4缺起点、损坏、UNKNOWN间隔与跨Owner保持；5种速度×126个年龄边界、纯身份暂停/恢复。相关回归B136 progression、B140模板A–G及B142实际HD目录/T0均PASS；既有fixture故意触发的HELD日志不代表正常路径失败。未跑全历史或stress。原临时Lupa目录已不存在，本次临时环境重新安装既定2.8 wheel，lua55导入及上述运行通过。

诊断：P0面板“主持 / 传统影子”，左键主持完整明细，**右键传统影子**；保留原主持明细可达。报告起点、age、阶段、当前ACTIVE、下阶段与保护原因，明确“未施加科技收益”。只在点击时沿现有请求桥读Store与EffectiveFacts；不hover采样、不增加按钮或GC入口。

最小用户测试（一次、一城，建议独立存档）：
1. 使用尚为科研P3的城市，以正常移民投资达到P4；右键“主持 / 传统影子”，标准速度应age0、预期5%，显示首次P4回合。
2. 调离总督使ACTIVE下降；过2个玩家回合，报告age2，门槛未满足；不要求此批出现实际百分比收益。
3. 保存并完全退出、冷启动读档；同回合重复读取，age保持2、不重置不增加。提交一次报告/确认即可，勿重做40回合或内存长测。

回滚保留B142运行包与F1写入前存档；未承诺旧包理解新增字段。F1本地完成不等于native PASS，不允许由此开始F2。

部署记录：B143.170，source `fa9fcd4`，receipt `B143.170-fa9fcd4-playtest.json` DEVELOP_ACTIVE；172/172一致，B142/stable恢复点保留。游戏退出核验后用既有事务工具切换，未启动游戏；原生F1限定验收已关闭，见本页顶部证据；不扩大未测范围。

## P0-F2 具体实施计划 — 已授权

目标：在F1可靠年龄之上，接入本城实际科技百分比。Design不变：age0=5%，标准10/20/30/40分别10/15/20/25%，仅当前Research Identity且ACTIVE≥4有效；年龄仍由Store维护，carrier只是可重建的瞬时效果。

### 实现范围与旧writer边界

1. 复用`ResearchTradition.Shadow`与`CityProgressionStore.ReadTradition`，增加本专业效果consumer；不建立第二份年龄、不补旧P4起点。不接入跨Owner归属、转专业UI或其它E2尾项。
2. 优先复用已有城市百分比primitive `MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER`，新建学术传统专用、精确命名的隐藏carrier定义，采用互斥的5/10/15/20/25档或等价可验证编码，最终编码在实施时确认；不复活旧科研carrier。
3. 已静态核对：当前`Lv4Percent.lua`仅遍历CULTURE；`ResearchInfrastructure.Retired`仍精确清除旧`BUILDING_SPC_LV4_PERCENT_RESEARCH_0..7`。F2保持两者职责，新命名不得与该退休清单重叠，数据库最终附件与旧Research modifier停用状态在实施前定向核对。不要把旧文件名/历史注释当成现行Research writer。
4. 模块拥有自己的添加、更新和撤销，只处理精确IDs；ACTIVE下降/可靠非科研/确认失城时撤销。向既有E2 RegisterExit注册该模块退出，保存年龄不清零。OWNER_POLICY_UNRESOLVED、UNKNOWN_INTERVAL、缺起点均不激活。临时UNKNOWN保留错误与现有一致性保护，不把未知解释成新资格，也不能绕过已确认失城退出。
5. 重用现有按钮，显示年龄、当前门槛、应有百分比与已配置百分比；配置不是原生收益实测。原生城市产出明细用于验收；继续隐藏技术carrier，不增加机构或专业能力。

可能文件：ResearchTradition（或一个科研专用效果模块）、Gameplay初始化/请求、最小专用SQL和modinfo、P0Panel必要文案/已有carrier隐藏目录、相关定向测试。Store只在确有年龄变化通知接口依赖时作最小扩展；不改永久数据语义、GC、模板/Network或其它收益公式。

### 事件、事实与生命周期

只在首次P4提交、年龄跨档、可靠资格变化、load与确认owner变化时更新相关城市。通过现有通知/有界回合核对接入，保留同回合总督变化；不新增每帧/hover请求或每个事件全城事实扫描。普通计算只取传统、当前身份/ACTIVE、当前专用carrier，避免构造D/建筑/专家明细。瞬时待处理集合以现有持久引用定域，处理完成即释放；缓存加载清空、失城撤销，诊断仅当前值和最近异常。重复通知在状态不变时零carrier写入；年龄每回合增长不意味着每回合重建同档收益。

### 验证与退出

W0004 L2业务集成＋涉及保存/失城调用点的L3定域回归，不跑历史全套/内存长测：
- 5档数值/速度阈值与ACTIVE进入、下降、恢复；同回合变化不丢。
- 相同状态、重复通知零写入；按档替换无累加；旧Research效果不叠加；Culture writer不变。
- 真实模块的确认失城撤销、UNKNOWN保护、缺起点/跨Owner暂不生效；年龄/receipt不被carrier操作修改。
- 冷加载仅重建当前合法效果，失败明确报告；沿用相关F1/E2测试，不扩大PASS。
- SQL在当前只读外部DB的内存副本检查Modifier绑定、隐藏和互斥定义；Lua/XML/context检查。

未来最小实机验收：可复用本次F1存档的同一城，年龄2仍处5%档。先看ACTIVE1无本项；建立合格总督至ACTIVE4，原生城市科技明细出现+5%且报告配置匹配；再次调离应退出，恢复后保存冷启动应正确恢复且不重复。其它城市因素/百分比可能同时变化，应核对本项明细与同一快照下原生计算，不要求全城总科技简单乘1.05。不要求重测40回合；若原生界面无法区分本项，实施后提供一个针对该歧义的最小对照，不虚报效果PASS。

完成本地验证后按现有授权/退出核验部署独立测试build，保留B143包及测试前存档；失败退回B143与配套存档，F1年龄不由回滚工具清零。退出条件：本地通过＋限定实际百分比/资格退出恢复/冷加载验收通过。当前无阻塞F2的Design决策；技术primitive接线验证仍属于F2任务。完成后停止，不自动进入后续能力。


## B144.171 — F2 implementation and validation

用户已明确授权F2。`ResearchTraditionEffects`拥有五个互斥5/10/15/20/25科技百分比carrier，SQL使用既有城市科技百分比primitive；Store继续唯一拥有年龄/receipt。无新增永久字段、旧科研效果复活、其它专业或GC改动。旧Research八档附件保持停用；新定义InternalOnly且零住房/槽位，沿既有机构隐藏路径处理。

首次P4提交只标记；Store先结算年龄，效果模块在加载就绪或publish收尾读取已登记传统城市。待处理按本地玩家合并，只遍历Store登记记录，不扫描世界/建筑目录；总督事件与既有FactsChanged桥保留同回合资格响应。只有五个自有carrier读取/差异写入，不构造D/专家诊断明细。空pending立即返回；缓存加载清空，pending处理完释放，错误只留最后一条。单城未知不阻塞其它record；UNKNOWN不授予新资格，确认失城走精确module-owned退出。跨Owner、UNKNOWN_INTERVAL、无可靠起点不激活，永久记录不由效果consumer清除。

本地证据：`test_b144_tradition_effects.py`实际Store/效果模块模拟五档、同回合ACTIVE4→1→4、重复零写、冷加载、确认失城/跨Owner暂停、普通建筑与年龄/receipt保留、其它城隔离、native写入失败后明确报错与相关事件重试；当前只读HD数据库的内存副本核对五组SQL绑定、隐藏、零槽位/住房及旧Research附件缺席。B143计龄与B136进度定向回归通过。STATIC_CONFIRMED / LOCAL_SIMULATION_PASS，不等于原生百分比或隐藏实测；无全历史/stress/内存长测。

最小用户验收（一次、复用F1科研城）：
1. P4、ACTIVE1时，P0“主持 / 学术传统”右键应有/配置均0；年龄继续保留。
2. 合格总督建立至ACTIVE4，报告应有/配置匹配年龄档（age<10标准速度为5%），核对原生城市科技百分比明细；调离后本项退出。其它科研能力/百分比同时变化，不能简单用城市总科技乘1.05作断言。
3. 恢复ACTIVE4后保存、完全退出、冷启动读档；本项按当前年龄/ACTIVE重建，重复报告不叠加。截图最终报告与科技明细，说明退出/恢复观察即可；不要求40回合测试。

回滚使用保留的B143包及本次测试前存档。B144新增SQL定义，不能以旧包继续新测试存档作为兼容承诺。本批退出点为原生验收；没有授权自动进入其它能力。

部署：B144.171 / modinfo171，source `5364c0e`，receipt `B144.171-5364c0e-playtest.json` DEVELOP_ACTIVE；174/174 MATCH，游戏退出/无pending事务/B143与stable恢复包已核验。未启动游戏；实际科技收益仍待上述一次用户验收。


## B144 F2 native acceptance

[六图与用户陈述](../../Status/Validation/Results/Specialization_B144_F2_Pass.md)完成F2限定USER_GAME_TEST_PASS：起始5%及冷重启为用户确认；T57-age10配置10%，科技总修正30%（基础综合大学20%），总督调离后回落20%为图示证据。基础与加成验算见结果；有限显示精度不用于证明UI延迟。F2门禁关闭，不要求重复；后续能力仍需新计划/授权。上方实施阶段“待测”保留为当时记录，不再派发该测试。
