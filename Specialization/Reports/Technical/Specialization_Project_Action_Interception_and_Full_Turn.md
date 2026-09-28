# 城市项目作为操作入口，以及时代对话完整生产回合调查

2026-09-27，用户要求只调查并保存；没有实现或试运行本文方案。STATIC_CONFIRMED 指已读源码/数据库定义；不代表原生实机验证。本文与同批E2征服快照实现相互独立。

## 结论先行

- 商业方案确实是“点击城市项目列表中的专用条目→截住原生生产请求→打开专用界面或发送操作请求”。它不是先入队再完成、退款或恢复队列。
- 原版和本机HD提供清楚的点击路径，可以做窄范围UI适配；仍需针对实际加载链、队列模式和弹窗关闭行为prototype。当前Mod只有施工队项目排序适配，没有通用商业操作拦截器。
- 这能避免该条目进入生产队列，因而不把它变成接受溢出/收获生产力的目标；但它也没有自动占用城市生产。适合商业开面板/切换，不等于满足时代对话。
- **Cost=1不能证明连续完整一回合。** 未找到可直接声明“这个项目只收正常回合生产、不收溢出/收获/外部AddProgress”的项目字段。未找到≠证明引擎绝无办法；需要定向原型，不应直接实施猜测的退款或全城减产。
- 时代对话更值得验证的是：生产占用与完成资格分离，Gameplay记录连续占用区间，完整生产回合才允许结算。如何可靠保留占用、处理即时生产和中断，仍是技术门禁。本报告不批准改变玩法或用纯等待计时替代城市生产占用。

## 1. 既有设计和当前实现不是同一状态

[Commerce D0032](../../Design/Content/Commerce_D0032.json)的商业化切换、资本投资/发展投资面板采用项目操作入口；[已接受审阅](../../Historical/Design/Reviews/Commerce_D0032_Review.md)记录请求前拦截方向。[Culture D0029](../../Design/Content/Culture_D0029.json)要求不受生产力/溢出影响，连续占用一个完整城市生产回合；中断需重新连续占用完整回合，启动时代额度、完成时X等合同不变。

当前[Dialogue.lua](../../../Mod/Dialogue.lua)仍是旧馆藏倍率writer，没有实现这个连续生产项目合同，不能拿它证明计时已经可行。[CrewProjectOrder.lua](../../../Mod/UI/CrewProjectOrder.lua)只排序施工队项目，不能当作已有通用点击拦截器。本轮没有修改这两个文件。

## 2. 点击到底经过什么

本机原版 `Base/Assets/UI/Panels/ProductionPanel.lua`：项目行左键回调（约889行）调用 `AdvanceProject(data.City,item)`，随后调用 `CloseAfterNewProduction()`。`AdvanceProject`（约410行）设置 `PARAM_PROJECT_TYPE`、插入队列方式，再调用 `CityManager.RequestOperation(city, CityOperationTypes.BUILD, parameters)`。

所以两个动作可以分开：

1. 玩家看到一个熟悉的项目行，点击它。
2. 我们的UI适配检查它是否为明确列出的本Mod操作条目。
3. 普通项目仍原样交给原函数；专用条目直接走自己的处理，并且不发送BUILD请求。
4. 若是资本投资，打开同屏面板；打开时取一次合并报价/资格快照。玩家本地选择领域、模式等，hover只读缓存。
5. 玩家确认才发一次Gameplay请求。Gameplay重新检查城市、身份、资格、价格/状态版本与重复请求，决定是否建立合同；UI不能自行扣钱、roll结果或写永久记录。
6. Gameplay返回确认状态，UI更新展示。取消面板不产生合同，也不占生产队列。

这里的“拦截”是替换/包装特定UI回调，不是获得引擎所有生产来源的总开关，也不是全局覆盖CityManager.RequestOperation。任何其它UI或Mod可以有自己的直接请求路径，因此Gameplay仍须独立验证。

**不能漏掉的细节：** 只包装AdvanceProject并return，原项目行闭包仍会继续执行CloseAfterNewProduction。原型必须连同这条后续关闭行为处理，否则面板可能刚打开就被原生流程关闭。也要核对入队模式、当前项过滤、禁用原因、费用/回合显示；不能显示假的“1锤/1回合”来伪装纯操作按钮。重复点击、切城、关闭面板、读档重开都必须不造成重复操作。

本机HD `UI/Replacement/DL_ProductionPanel.lua` include Babylon Heroes版或原版ProductionPanel，并包装多处列表/UI函数；Heroes版又include ProductionPanel。当前项目自己的CrewProjectOrder include HD面板。适配应接在这条现有链中，只处理自己的明确条目，避免整文件替换HD或破坏其余项目。实际其他UI Mod的加载优先级仍需实机确认。

## 3. 溢出锤Mod做了什么

已读取本机Workshop `2589004769`：**溢出锤bug修复【可切换手动版】 / Overflow Bug Fix (Switchable Version)**，作者DeepLogic。该Mod文件存在不等于本次存档已确认启用或手动/自动状态已确认。

`OverflowBugFix_Switchable.lua`默认auto_apply_overflow=true；监听CityProductionChanged，自动模式调用Gameplay公开的AddZeroProduction，另有手动按钮。`OverflowBugFix_helper.lua`调用 `city:GetBuildQueue():AddProgress(0)`。它没有为时代对话或本Mod项目设置排除条件。零新增值仍可触发队列应用现有溢出；这是本Mod的静态实现意图，当前组合原生效果尚未重新测试。

[作者说明](https://steamcommunity.com/sharedfiles/filedetails/?id=2589004769)将问题描述为溢出在特定完成计算中丢失，修复方式是提前应用已有溢出。因此不能把“原版所有溢出默认清零、下一项绝不继承”作为技术前提。本文未做原版全规则实测，也不依据评论推断所有项目类型行为。

如果专用条目根本没进生产队列，它的点击不会经BUILD改变生产目标；上述Mod不会把溢出加到一个不存在的生产项目上。但它仍可以对城市原有生产队列运行，不能据此宣称城市所有生产注入被禁用。

## 4. 为什么1锤、禁止溢出、禁止砍树是三个不同问题

| 方案 | 能做到什么 | 仍缺什么 |
|---|---|---|
| 普通Cost=1项目 | 定义很低的生产成本 | 即时生产可能立即完成；不是时间锁 |
| 截住项目点击，不入队 | 不让这个按钮成为原生生产目标 | 原生产照常运行，未付出完整生产回合 |
| 项目完成后延迟发奖励 | 控制奖励最早结算时间 | 项目可能早已退出，余下生产时间用于别的项目，不满足连续占用 |
| 用生产百分比抑制 | 可能改变某类正常生产效率 | 未证实过滤储存溢出、砍树及脚本AddProgress；还可能改变其它产出 |
| 高成本占位项目+独立时间门槛 | 可作为持续占用原型方向 | 任意大注入能否提前完成、如何安全结束、剩余生产/队列处理都未证实 |
| 独立占用状态+Gameplay计时 | 可把时间作为权威条件 | 必须证明它真实占用了城市生产，并正确中断/恢复；不能只是“等下一回合” |

收获/砍树是后续单位操作，和“点击项目行”不是同一条请求。原版UnitPanel向UnitManager查询/发送单位操作；本机HD另有 `Gameplay/HD_Common.lua` 的CityAddProgressPercentage直接调用BuildQueue:AddProgress(amount)。因此仅拦截生产面板不会拦截这些来源。

这次检查的基础Projects schema包含Cost、进度模型、各种解锁/次数条件，没有发现逐项目IgnoreOverflow/IgnoreHarvest或固定完整回合字段。不在收获事件发生后假定可以安全扣回生产： native完成可能已执行、项目可能退出、砍树资源也已消失。将这种补偿法列为高风险候选而非推荐实现。屏蔽玩家砍树按钮也不是生产过滤，会改变合法玩家行动，且不能覆盖其它Mod或脚本来源；本轮没有授权这种玩法限制。

## 5. 后续最小prototype建议（尚未授权）

先单独验证纯商业入口：一个专用项目行打开空的单层界面，队列/进度/金币/合同均不变，普通项目仍能建造；包括HD队列模式和反复开关/切城。此时不混入时代对话计时。

时代对话原型另行处理：

- 明确Gameplay保存启动城市、启动Game Era、连续生产占用状态和结算去重信息；不由UI或原生“锤满了”独占完成权威。
- 在真实城市生产处理边界确认完整占用；切换生产即打断，不能用“当前回合号大于开始回合号”单独证明连续工作。
- 用自然生产、已有溢出、自动/手动溢出应用、收获生产、脚本AddProgress、切换再切回、同回合重复、保存读档分别定向检验；避免一开始做大规模组合模拟。
- 原生提前完成、队列继续生产、误吞普通项目溢出或中断时被补算，任一出现即停止该路径。不靠重置整城生产、修改第三方Mod或隐藏提前完成来过关。
- 若不能可靠做到，报告具体IMPLEMENTATION_LIMITATION；不能把“连续完整城市生产回合”偷偷改成“点击后等待一个回合”。

**状态：** 点击链、当前适配链、溢出Mod/AddProgress调用和本次schema检查为STATIC_CONFIRMED。商业拦截UI为PROTOTYPE_REQUIRED；时代对话完整占用/生产来源隔离为TECHNICAL_INVESTIGATION_REQUIRED及PROTOTYPE_REQUIRED。没有LOCAL模拟或USER_GAME_TEST证明这些方案运行成功；现在无需用户游戏测试。

## 6. 可复用用途与边界

已有设计的自然用途：商业化开关、资本投资面板、发展投资面板。它们的城市项目行是操作入口/轻量Dashboard，实际合同及资格由Gameplay掌握。其它选择器或确认界面在技术上也可参考，但这不授权新增能力，也不代表所有项目都应该变成按钮。

Claim仍遵守用户本轮再次确认：**完成对应城市项目才建立专业；候选只有一个也不自动认定。** 不能借此UI调查把Claim改成免费即时点击。时代对话同样保留自己的真实生产占用规则。

## 本次读取的外部文件位置

- 原版根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/`；Base/Assets/UI/Panels/ProductionPanel.lua、UnitPanel.lua；Base/Assets/Gameplay/Data/Schema/01_GameplaySchema.sql；DLC/Babylon/UI/Replacements/ProductionPanel_Babylon_Heroes.lua。
- Workshop根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/`；2589004769的modinfo、Switchable.lua、helper.lua；2465378070的UI/Replacement/DL_ProductionPanel.lua、Gameplay/HD_Common.lua。

这些路径为此次只读调查证据，不作为跨机器部署配置；未修改原版、HD或溢出Mod。未来版本变更后应重新核对相关hook，不因本报告静态结论跳过prototype。

## 7. 固定且只需一个生产回合：增量调查（2026-09-27）

用户进一步探索严格固定一回合，不是授权实施，也未批准Claim计划中的Cost=1建议。分开三个条件：①不能提前完成；②连续经历一次真实城市生产结算后必须完成，不随城市生产力变慢；③该次结算确实被项目占用，不能同时建造其它目标。仅计回合号或延迟奖励只能处理部分条件。

### 新核对的事实

- 本机Base Projects schema 2178起含Cost、CostProgressionModel等，没有直接每项目FixedTurns/IgnoreOverflow/IgnoreHarvest字段；这一限定搜索不是全引擎不存在的证明。Expansion2碳捕获与援助项目也使用普通400/200 Cost，不是定时项目先例。
- 本机HD Gameplay/CivilizationTraits.lua的TrajanCityProductionChanged（约3128起）在政府区/对应建筑路径调用BuildQueue:FinishProgress()；GreatPersons.lua、UnitAbilities.lua另有直接调用。证明主动完成有现成源码用例，不证明调用对本项目的完成事件、溢出及队列顺序已实测。
- [Sukritact的CityBuildQueue接口记录](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CityBuildQueue)列AddProgress、FinishProgress、CurrentlyBuilding为Gameplay接口，多项进度getter只标UI；未列通用项目进度setter/生产暂停入口。记录可能不完整，不能凭列表断言接口绝不存在，更不能把UI getter直接放进Gameplay模拟并宣称可用。
- 现有溢出修复在生产变化时调用AddProgress(0)，原生收获与HD直接AddProgress来自其它路径。因此UI点击拦截不等于全生产入口过滤。

### 可探索的实现路线（均未实机证明）

| 路线 | 能解决的部分 | 不能据此承诺的部分 |
|---|---|---|
| Cost设成当前城市每回合生产量 | 在该瞬间显示约1回合 | 总督/市民/修正变动、已有进度、溢出及收获使时间改变；不能保证固定 |
| 项目专属生产抑制＋完整回合后FinishProgress | 若抑制真实覆盖所有增量，可隔离锤量和计时 | 百分比修正可能相加/被抵消；是否影响溢出/收获/脚本AddProgress未知；不能写成已找到过滤器 |
| 高成本无收益占位项目＋完整回合后FinishProgress | 候选原型：项目占队列、回合后主动完成，不依赖城市产能达到成本 | 有限高成本不是不可完成标志，大量注入仍可提前完成；可能吞掉旧溢出或产生错误结余，不能作为严格保证交付 |
| 拦截点击＋自定义定时行动 | 完成逻辑完全由Gameplay计时 | 原队列仍生产，除非另有可靠独占/暂停原语；否则是等待行动而非占用城市生产项目 |
| 完成回调中撤销/重新入队 | 能发现提前完成 | 回调时原生奖励/队列推进可能已发生，无法保证复原；不推荐作为安全默认 |

**优先原型不是完整能力：** 先验证一个无收益占位项目的生产结算边界和主动完成语义，再调查能否严格阻断提前完成。如果高成本候选被输入击穿，明确判它只适合受限实验，不提高数字掩盖缺陷。若没有可靠独占与输入隔离，严格固定生产回合仍是TECHNICAL_INVESTIGATION_REQUIRED；不能将纯计时行动作为等价实现。

### 最小分步验证建议（需另行授权）

1. 单城无收益项目，记录实际生产项目、完成事件和玩家回合相关事件顺序；不能假定PlayerTurnActivated总在城市生产后，也不能将读档触发当完成一回合。
2. 确认自然连续生产一次后主动完成（含低/零生产对照）；核对队列下一项没有偷偷获得本应占用的当回合生产。FinishProgress前再次验证当前项目，防止错误完成别的目标。先只证明时序与占用，未证明额外生产隔离。
3. 同一fixture加入已有溢出、溢出Mod自动/手动应用、一次收获、直接AddProgress的定向注入；检查既不提前完成，也不提前推进下一项或重复奖励。针对通用FinishProgress作弊调用不宣称绝对防护，明确支持边界。
4. 切出/切回及完整重启验证持续性。计时必须跟实际占用，不按日历差补算。任何提前完成/错结算/普通队列生产损失都停止对应方案。

### 额外生产力的去向尚需区分

“不让溢出/收获加速项目”与“不消耗/丢失这些生产力”不是同一句话。项目若接收并吞掉它们、但计时仍一回合，只证明不能加速，没有证明真正拒收。未来方案必须报告：启动前已有溢出保留还是消耗、期间砍树所得暂存还是丢失/流向其它目标、城市该回合正常生产如何处理。当前未授权销毁/退款/暂存这些产出，不能擅自实现。必要时在原语调查后由用户决定游戏语义，而非现在强造资金式生产力账本。

当前结论：有主动完成的STATIC依据；没有已确认的全来源隔离或严格一回合项目方案。仍是只读调查，没有新能力、载体、原型、本地模拟或用户游戏测试；Claim Cost=1仅为既有待审核建议，不因本讨论自动通过/废除或修改Design。

## 8. 空生产队列作为隔离层的候选（2026-09-27）

用户提出利用无生产目标时砍树生产被浪费的行为。只读继续调查；不是接受新Design或授权实现。

### 找到的更强依据与适用限制

[官方September 2019补丁说明](https://support.civilization.com/hc/en-us/articles/39409989034643-Patch-Notes-September-2019-Update) Production Overflow段明确描述：为防止玩家在城市无生产时强制结束回合来积存overflow，引擎会在turn end清理overflow；奇观失败返还的salvage另存，等玩家再次turn active才并入。官网页面现发布于2025，是2019补丁文档的重刊，不是2025新机制。

这支持“无生产目标跨越特定回合边界可能清除普通overflow”的调查方向，**不证明无目标砍树当下立即归零**，也不证明salvage、正常城市每回合生产、HD或溢出Mod额外路径都同样清除。社区检索存在空队列砍树后同回合放区域仍获得生产的玩家陈述；本轮没有实机复核，不能作为确定机制，只是不能直接接受即时丢弃假设的线索。最终结论依据官方描述/本地源码，当前组合仍待测试。

本机原版ProductionHelper.lua:196的RemoveQueueItem用BUILD + VALUE_REMOVE_AT + PARAM_QUEUE_LOCATION移除选定项。它证明有UI队列编辑路径，不证明可无损暂停并恢复任意队列，也不意味着取消项目能清空其既有生产进度。

本机ActionPanel.lua把ENDTURN_BLOCKING_PRODUCTION映射为需选择生产；OnInputHandler中Shift+Enter使用ACTION_ENDTURN/REASON=UserForced，源码注释为Unsupported。没有找到只豁免本Mod一座占用城市、同时保留其它城市/单位阻塞的现成接口。本机HD_ActionPanel未提供本调查所需的该局部豁免。不能把全局强制结束回合作为产品方案；隐藏提示也不等于引擎阻塞解除。

已安装OverflowBugFix的CityProductionChanged在auto模式（AI分支亦如此）调用AddProgress(0)，手动按钮也能调用；对“目前没有生产”的情况没有自己的排除判断。因此清队列、恢复队列都有可能触发应用暂存生产的入口，实际事件顺序尚需原生验证。

### 可探索的空队列定时方案

不是在砍树瞬间临时切走项目再切回；若该回合生产尚未被清理，切回时仍可能应用到项目。条件式方向是：

1. 用户开始专用定时项目，Gameplay记录该城独占生产的活动状态；UI显示进行中，但原生队列保持空。
2. 跨越真实生产结算和普通overflow清理边界，该城不生产其它目标。若玩家改建其它内容，按该能力既定中断规则处理，而非强行清除新选择。
3. 确认连续占用完成，才结算并解除占用；恢复普通生产必须晚于所依赖的清理边界，且不得重复清算或吞掉无关进度。

优点：没有原生项目进度条可被收获锤直接填满，计时可以不依赖城市生产力；不需要用巨大成本模拟不可完成。但以下四项不解决就不能交付：

- **结束回合阻塞**：正常结束回合能通过，仍保留其它未完成动作的提醒/阻塞。
- **生产去向**：实测无目标跨回合是否同时处理正常产能、已有overflow、即时harvest与salvage；不能把某一来源观察推广到全部。
- **连续性/持久化**：切城/改建/入队/读取存档不会丢失独占状态或让该城同时生产别的东西；不能仅比较两个时点为空而漏掉中途生产。
- **项目语义**：这是“空队列承载的自定义定时项目”，不天然产生CityProjectCompleted。若最终不能以真实项目完成满足Claim已接受规则，必须先交用户审核，不能悄悄改成等待行动；时代对话亦必须证明真实生产机会被占用。

现阶段优先以原生空队列行为做小型事实验证，而不是实现清队列/存队列/全局结束回合接管。为缩小状态风险，未来首个原型可限定开始时无排队后续项的单城，但这种原型限制不是正式能力的新资格。

### 最小事实实验建议（未实施，当前无需用户立即测试）

同一城市/存档分支：A空队列砍树后同回合选择项目；B空队列砍树后跨回合再选；C空队列不砍树、跨回合再选；另对照已有overflow。先在纯原版确认区别，再在当前HD+溢出修复组合确认（实际启用状态要核对）。记录选项前后与下一回合进度、正常产能、是否被要求选择生产；如需Shift+Enter只能作为事实实验并注明，不等于可交付正常流程。无需覆盖所有Mod组合或完整玩法原型。

结论：用户思路有官方回合末清理描述支持，值得保留；它是“跨回合隔离”的候选，不是“无目标即时销毁所有生产”的已证实原语。当前最大新门禁是局部生产阻塞豁免与正常生产机会/额外生产去向的原生验证。未实施、未部署，Claim计划及Design保持原有待审核状态。

## 9. 正常结束回合时定域豁免：用户提出的新候选与范围收窄

2026-09-27用户提出：正常结束回合时检查阻塞，若仅由本Mod定时项目造成则走Shift+Enter同源通道。另明确本Mod不负责溢出Mod的生产分配，只负责本项目必须占用且仅占用一个回合。此为继续探索，未授权实现；不改变Claim待审核参数或正式Design。

### 新静态依据

本机Base ActionPanel.lua OnRefresh约166行同时使用GetFirstEndTurnBlocking及 **NotificationManager.GetAllEndTurnBlocking(localPlayer)**。所以无需仅依赖最高优先级阻塞。返回值在本机代码中用于遍历阻塞**类型**，不据此假设它提供每个阻塞城市的完整列表。

同文件DoEndTurn约525行：先检查CanUnreadyTurn、消息处理中状态，再查阻塞；无阻塞时另外调用CheckUnitsHaveMovesState、CheckCityRangeAttackState，才发送普通ACTION_ENDTURN。Shift+Enter在OnInputHandler使用同一ACTION_ENDTURN但带REASON=UserForced。存在可调用路径，不代表可安全对普通点击无条件替换。

HD_ActionPanel.lua include ActionPanel并保存BASE_DoEndTurn；约288行包装DoEndTurn，政策提醒开启时还提供继续/改政策确认。该提醒不只是GetAllEndTurnBlocking中的一项。下一原型必须保留实际HD链的提醒与玩家选项，而不是直接跳过BASE/HD逻辑。未知其它UI替换链按真实环境验证，不宣称通用兼容。

### 建议候选门禁（尚未实现）

仅在玩家主动正常结束回合的请求上做一次有界检查，不per-frame扫描、不自动替玩家结束回合：

1. 当前单人本地玩家有效、当前回合完整可操作、未处理中/未已提交；撤回回合等原路径保留。
2. 从Gameplay取得当前有效项目占用状态并核对owner/city/reference/turn；读不到或过期则不豁免，不以UI文字/空队列本身证明占用。
3. 读取全部阻塞类型；任意非生产阻塞、未知类型都保留正常路径。确认所有实际“需生产”城市都能归属到本Mod有效占用；有普通空队列城市则不能强制结束。必须验证逐城覆盖方法，不能只验证一个FindEndTurnBlocking返回对象。
4. 保留原版独立单位/城市远程攻击检查及HD政策提醒等正常结束分支；玩家点击其它特定阻塞提醒时不劫持其导航。
5. 仅剩本Mod占用城市的生产阻塞，且前述事实再次确认仍有效，才允许发送一次UserForced结束请求。处理请求在途/重复点击；保存/重载后重建事实，不重放旧UI确认。
6. 自动结束回合选项先保持现状，不静默扩大为自动强制；手动Shift+Enter本来具有的行为不由本模块全局改写。具体按钮/Enter/HD确认回调接入点需原型核对。

示例：定时项目城A + 未选科技→不豁免；A + 普通空队列城B→不豁免；A + 未处理单位→保留原提示；A/B均有效定时占用且其它要求完成→候选允许一次结束。未知/丢失项目状态→停止豁免。

### 用户明确收窄后的研究目标

不实现自有溢出银行、补偿/退款、为第三方Mod修复分配、不管理既有砍树收益应流到哪项。前节“生产去向”从独立交付目标收窄为**只验证与本项目时间/生产独占有关的效果**：额外输入不能提前完成本项目；该城不能同时生产另一项；一次实际占用后结束，低产能不得多等，读档不得多算。

因此空队列期间即使原生/第三方暂存了收获产出、项目结束后才用于其它项目，只要未违反已接受的生产占用规则，本轮不擅自清理或接管。仍需检查正常城市生产是否在项目期间被储存并以后兑现，致使所谓“占用”并没有付出设计要求的生产机会；若出现该情况，报告事实并请用户判断，不扩大工程去自行扣产。

### 下一最小原型建议与证据等级

A：先只验证完整阻塞检查＋逐城归属和原版/HD提醒保留，使用上述正反例，确认只在正常结束请求时触发。B：再结合单城空队列定时占用，验证一次真实生产结算、额外输入不能提前完成、切换中断、完整重启和幂等结束。两步都不先实现正式能力或伪造CityProjectCompleted。

STATIC_CONFIRMED：上述原版/HD代码路径。PROTOTYPE_REQUIRED：全部阻塞覆盖、局部豁免安全性、实际结算时序和连续占用。没有本轮LOCAL/USER_GAME_TEST；不需用户现在启动游戏。此前“未找到局部豁免接口”仍成立，但用户提出的有条件使用全局通道成为可验证替代候选，不应继续视为完全没有入口。

## 10. 活动项目门控：最小本地验证

2026-09-27用户建议只在选中同类定时项目的生命周期内启用检查，并授权验证。本轮完成独立本地门控模型，不是挂载到Civ VI的项目原型。没有Mod修改、结束回合请求或部署。

### 门控边界

建议由各城市有效活动项目记录派生一个session活动集合，而非再保存一份可能失真的全局布尔值。只有Gameplay已确认开始占用才加入，单纯点开菜单或将项目排在未来队列中不启用；完成/取消/中断/已确认失去资格移除相应活动。记录绑定city reference与本次activity token，迟到的旧完成不能删除该城新启动的活动。多城并行时须等最后一个活动退出才关闭门控。

无活动项目→正常结束路径，零阻塞扫描；有活动项目→仅在玩家明确结束请求时读取完整阻塞快照。不按每帧/每回合扫描。若第一次有其它阻塞，玩家处理后再次点击必须重新核对；不能把“一次性状态”误做成每回合只允许检查一次。只有已提交且请求在途才防重，不缓存旧“可结束”结论。自动结束选项暂不扩展。

读档后从已确认活动记录重建；重建完成前不允许豁免。项目本身的持久化仍是待验证合同，测试没有证明引擎save/load接口或生产结算顺序。UI缓存只是门控提示，不能取代Gameplay有效状态。

### 可重复的本地证据

[Test model](../../../DevelopmentTests/test_timed_project_gate_model.py) 使用Python标准库，明确不伪造Civ VI接口。运行 `PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_timed_project_gate_model.py`：13个测试通过，**LOCAL_SIMULATION_PASS — independent gate model only**。

覆盖：无项目零扫描；自动请求不豁免；活动下显式请求及重复防护；多城只结束一个；旧token迟到；完成/取消/confirmed loss退出；非生产/未知阻塞；普通空队列城及token不匹配；单位/HD独立提醒；过期/缺失/读取失败快照；核对期间状态改变；处理阻塞后再次点击；重建已确认集合；提交重入/结果不明不重发。测试只统计模型扫描与提交调用，不声称测得真实引擎耗时或quota节省。

重要限制：模型把“完整逐城生产阻塞快照”“独立提醒已清”“活动记录有效”作为输入合同，它们如何在Civ VI/HD可靠获得尚未验证。模型不会让这些前提自动变成STATIC/NATIVE事实。本地通过也没有证明空队列占用恰好一回合或真实跨session恢复。

### 当前边界

原生下一步仍需小型UI/Gameplay测试入口验证：真实全部阻塞及逐城归属、HD提示保留，再验证空队列跨一次生产结算。此次未制作/部署该原生包，用户目前无需测试，不能登记项目方案整体PASS。当前Claim计划仍待审核，B111运行包与既有验收不变。不先把本模型扩展成通用任务框架或实现时代对话。


## 11. B112.139 — native blocker observation prototype

2026-09-27用户授权原型验证；本包只完成前述A阶段的**原生观测入口**，不把未知的逐城阻塞覆盖直接当作UserForced许可。B阶段空队列连续生产占用、固定一回合完成、收获/溢出隔离及保存恢复尚未实现/验证。Claim、时代对话和收益均未接入。

### 实际接线与安全边界

`UI/TimedTurnProbe.lua`作为ActionPanel的ReplaceUIScript，include本机已查证的HD_ActionPanel→ActionPanel链，包装DoEndTurn但始终且仅调用一次原HD函数。未知或异常只关闭本观察器，不吞掉原结束操作；不调用RequestAction/城市操作/Property写入，不改变队列、生产力、原手动Shift+Enter或自动结束路径。本包针对当前HD安装，不宣称其它ActionPanel替换Mod或纯原版通用兼容。

使用现有诊断面板两个性能按钮位置，改为「开始单城观察」「回合原型报告」；其它E2/能力入口不变。开始要求本地单人人类测试文明、当前选中己方城市且队列为空。只是session单城观察，不是Gameplay有效项目记录，也不借坐标证明永久城市身份。开始/读报告均不做全城扫描；只有armed后的显式DoEndTurn读取全部阻塞类型、首阻塞、逐城队列（最多128城，超过报UNKNOWN）、单位/城市攻击独立检查、HD政策提醒启用状态及相同条件、请求处理中/已提交/可撤回状态。空城名称最多显示8个，计数继续完整计算。

无观察时直接原路径；报告是最近请求的缓存，阅读/hover不请求Gameplay。取消、回合改变、下一次读取发现失城/队列非空/未知时解除；重载默认关闭，不将旧UI报告当作项目保存。无per-frame/per-turn城市扫描，事件只检查已arm的玩家/回合常量；原HD刷新行为未改。

“候选条件满足”只表示这些读数符合候选筛选，不是已证明可以豁免结束回合。尤其空队列全集是否等于生产阻塞全集仍需native核对。本包始终保留原按钮行为，通常仍跳到选生产；这是预期，不是强制结束失败。静态调用点还包括原版死亡/观察者路径，本包未启用任何强制通道；后续豁免不能仅凭DoEndTurn被调用就推断一定来自玩家点击，必须单独区分调用来源。

### 本地验证与证据

W0004 L2：实际Lua原型使用独立API fixture的13项定向测试（`DevelopmentTests/test_b112_turn_probe.py`）通过：idle零扫描、候选只观察、其它阻塞与同回合重试、普通空城、独立单位/远程/HD提醒、未知暂停但原函数执行、队列改变、跨回合/缓存读取、失城/资格、手动取消/新session、指定阻塞原样传递、稀疏/未知枚举/扫描上限、XML/manifest/改动Lua语法。`UI.RequestAction` fixture直接抛错，确保原型不走强制通道。原HD函数只计数替身，不声称模拟了原生HD实现。

STATIC_CONFIRMED：本机原版/HD调用链、原型无Gameplay写入。LOCAL_SIMULATION_PASS：上述实际Lua与既有13项门控模型。USER_GAME_TEST_REQUIRED：ReplaceUIScript实际加载顺序、完整阻塞/逐城代理、HD原按钮保持；当前无原生PASS。未运行玩法全回归/stress。回滚仅需已知良好B111包；原型无新增存档字段。

### 最小实机流程（一座主观察城，可用现有测试存档）

1. 确认诊断版本B112.139。选择己方城A，手动使队列为空；点击「开始单城观察」。关闭面板，点正常结束回合，再左键「回合原型报告」并截图。不要Shift+Enter。若未载入/暂停/没有新采样，截图停止。
2. 同一回合先保留一种真实其它待办（未选科技/市政，或待行动单位），点正常结束并读报告；处理它以后再点一次、截图。直到其它事项处理完，只剩A选生产，预期报告候选满足，但原按钮仍要求生产。无需为了政策提醒专门耗费多回合；没有遇到就记未覆盖。
3. 若方便，让另一己方城B也暂时空队列，仍观察A，再点结束并截图：应显示其它空城、候选未满足。给B恢复生产后再次读数应更新。最后右键报告取消观察，给A恢复生产，照常继续。

本轮不要求砍树/溢出/存档测试；那些属于尚未实现的B阶段，不用本包伪验证。用户仅需最少的负例＋A唯一空城＋可选B对照；本次真实覆盖到的HD提醒另行记录，未出现不能判PASS。收到证据以后才能决定是否进入条件豁免和固定回合占用下一原型，不自动实施。


### B112 native evidence update — 2026-09-27

[三图结果](../../Status/Validation/Results/Specialization_B112_Turn_Blocker_Observation.md)：所测观测路径USER_GAME_TEST_PASS；生产条目按两城返回两次，随后缩为一次；同回合重试正确更新，HD提醒条件可读。不能将独立单位检查false覆盖列表中的UNITS。原型仍未发强制请求/建立定时项目；不扩大成全场景阻塞覆盖或固定回合PASS。新增按钮标题空白待后续修复。


## 12. B113.140 — guarded next-turn button prototype

2026-09-27用户授权：仅测试占用城缺生产时，按钮不再显示“需要生产”，应显示下一回合且能够点击过回合。当前实现仅单人本地测试文明、手动单城session实验，不是正式项目authority；Claim、Dialogue、固定一完整生产回合与收益未接入。

### 显示与行动分离

保留HD_ActionPanel→ActionPanel原链及DoEndTurn。新增包装OnRefresh：原刷新完成后，满足严格测试资格才覆盖主按钮文字/图标/tooltip；只剩测试生产阻塞时显示正常下一回合，仍有其它通知则显示第一个其它待办。普通B城空队列、未知或资格失败保留原显示。无其它通知时隐藏旧次级通知图标；多种真实通知保留原次级列表，不篡改NotificationManager数据、不撤销原生通知。

只允许显式主按钮、普通Enter及EndTurn输入action进入新判断。DoEndTurn本身不改，死亡/观察者及次级通知原路径不触发豁免；自动结束不扩展，原生Shift+Enter不变且不得用它作本原型PASS证据。原生输入action来源及多个输入回调时序仍需实机验证。

每次明确点击都重新读事实，不依赖显示缓存；要求本玩家存活/回合可操作、非处理中/已提交/可撤回、非教程/自动演示；全部阻塞格式与首阻塞一致；恰好一个生产阻塞、仅测试城一个空队列；FindEndTurnBlocking生产通知的owner/未dismiss/位置也须对应测试城。通知位置仅是当前任务对应证据，不是永久cityKey。新原生位置接口未得到B112截图证明；缺失则暂停，不以数量或坐标猜测绕过。

其它通知优先交原HD DoEndTurn处理；独立单位与城市攻击保留选择路径。HD政策提醒条件存在时显示检查政策，并使用相同文案/更换与继续选择；继续确认后再核对活动token及全部当前事实，再且仅再允许一次UserForced。旧弹窗确认、增加的新阻碍、取消或换活动不能继承旧许可。未知请求结果保持防重，不盲目再发；跨回合实验结束，重载未arm。

### 性能、显示与限制

无活动不扫描。原生相关事件仅标dirty并合并RequestRefresh；显示刷新复用缓存，不每帧扫描，不从hover/读报告请求Gameplay。主动作永远新鲜复核。最多128城；普通队列改变中断测试。原生刷新仍正常运行，不承诺消除其它Mod已有刷新成本。两个诊断按钮增加明确Label ID并在初始化SetText，修复B112空标题；待实机确认。

原型不改变生产队列、不写保存Property、不接生产结算或收益；仅为这次显式测试绕过一项生产阻塞。**实际过回合成功也不能证明城市已独占生产一完整回合。** 砍树/溢出、连续占用、取消/恢复与保存仍下一独立原型边界。不将本实验的session token作为正式项目持久化方案。

### 验证

W0004 L2，`DevelopmentTests/test_b113_turn_gate.py`：21项实际Lua定向模拟PASS，包括显示下一回合/其它待办、普通空城、点击重读、防重/重入/不明请求、通知位置/归属未知、独立单位/远程攻击、HD政策更换/确认/新阻碍/旧token、普通Enter与原DoEndTurn区分、Shift路径保留、dirty合并/缓存读取、回合结束/新session、非活动/教程/自动演示/列表异常、XML/显式Label/改动Lua语法与无保存写入。基于独立native fixtures，不代表HD实际UI渲染/Popup/引擎请求通过；未运行无关玩法全回归或stress。

STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED：真实生产通知位置、刷新/回调实际绑定、按钮显示、政策选择、一次跨回合。B112观测的限定实机PASS保留，不扩大。遇到“原型暂停”、按钮未更新或意外跳过其它待办则截图停止；不要用Shift+Enter绕过。

### 最小用户流程

1. 使用独立测试存档，在本回合先让A/B均空队列，选择A，点「开启单城测试」。仍有真实待办时保留对应按钮；只剩A/B空时仍应要求生产。读取报告一次作为负例。
2. 给B安排生产，A保持空，处理其余待办；右下角应自动成为「下一回合」。若HD新政策提醒未处理，先显示「检查政策」，可更换或确认继续，不能无提示跳过。截图按钮和原型报告；通知位置未知则停止。
3. 点击右下角下一回合（不要Shift+Enter），等待进入下一回合，读取报告截图：应只发一次请求并显示测试关闭。A仍无生产目标，下一回合恢复普通“需要生产”；没有项目奖励，这是预期。

无需砍树/溢出/保存测试；本包没有该机制。无需把B112所有其它待办重跑一遍。原型回滚恢复B112已保留包，不增加存档schema。当前仅部署此测试包，不自动推进正式能力。


## 13. B113 boundary investigation and alternative routes

2026-09-27用户要求先调查当前失败及其它方案；本轮仅只读本机原版/HD代码、已存报告与公开作者资料，没有修复/制作原型、测试、部署或Design变化。B113原生FAIL保持。

### 找到的具体读取遗漏（STATIC_CONFIRMED）

本机原版 `Base/Assets/UI/Panels/NotificationPanel.lua`，`LookAtNotification`（约642–685行）明确分开两个合同：

- `IsLocationValid()`为真才读取`GetLocation()`，用于镜头移动。
- `IsTargetValid()`为真时读取`GetTarget()`，返回`targetPlayerID, targetID, targetType`。
- 当`targetType == PlayerComponentTypes.CITY`，按Players[targetPlayerID]:GetCities():FindID(targetID)取得城市。即使没有有效Location，仍可从这个城市取得位置并选择该城。
- `OnChooseCityProductionActivate`（同文件约1090附近，按函数名定位）调用`LookAtNotification`，然后发送`LuaEvents.NotificationPanel_ChooseProduction()`。生产通知的正常操作本来就使用这套对象目标路径。

B113代码直接调用GetLocation并检查是否是number，然后要求与测试城坐标一致；没有先读IsLocationValid，也未读GetTarget。**数字类型并不证明位置有效；位置不是通知目标城市的唯一原生表达。** 将其作为必须满足的硬门槛缺少依据，是本原型的具体实现遗漏，而非Design矛盾。应优先验证原生target tuple，不是删掉归属保护。

实际19:30:37截图只能证明匹配false，未记录原始位置、LocationValid、TargetValid、target tuple。因此“该通知位置无效而目标城市有效”是得到原版代码支持的优先假说，不是已观察事实；也不能断言只改GetTarget就必然通过。未知/冲突应停，不从单独坐标、城名或阻塞数量猜城市。

### 下一最小修复/观测建议（未实施）

沿原生合同只采集：通知ID/type/owner、LocationValid及有效时的位置、TargetValid与target owner/ID/type、测试城owner/ID；同时显示未通过的operable子条件，避免“其它条件未知”的模糊诊断。当前单城门禁可要求有效CITY target精确匹配测试城，再核本次session/owner/队列和全部其它阻塞。无有效target或冲突保留原按钮并报告，不用旧坐标硬门槛代替。今后多城不能只依赖FindEndTurnBlocking返回的一条对象，需另验完整通知对应集合；本轮不扩展。

该方案不创建persistent cityKey，不涉及E2跨所有者识别；只是当前UI对象归属。通过后仍要测试按钮刷新/点击和一次实际跨回合，不能借STATIC提前登记PASS。

### 替代路线比较：分开按钮问题与完整生产占用问题

| 路线 | 按钮/原生生产提示 | 固定一回合与额外生产 | 判断 |
|---|---|---|---|
| A. 空队列＋真实通知target过滤＋Gameplay独立占用 | 需要定域适配ActionPanel；已具备采样与显式请求路径，target读取有原版依据 | 项目不作为原生进度目标，锤不能直接完成它；但实际连续生产结算、其它生产不得并行、保存/中断及机会成本仍需证据 | 当前优先；这次失败不足以否定整条路线。先解决target，不增加更宽强制逻辑 |
| B. 原生无收益高成本占位项目＋Gameplay计时＋主动结束 | 队列非空，通常无需处理缺生产按钮；原生UI整合更自然 | 有限大成本不是无限，额外输入可能提前完成；FinishProgress/移出占位项的残余进度、溢出、队列顺序与中断仍有风险 | 可作备用受限原型，不满足严格保证之前不能当最终方案 |
| C. 原生项目＋专属生产抑制＋计时完成 | 队列占用与按钮可走正常路径 | 未找到能覆盖原生收获、旧溢出、HD脚本AddProgress等所有输入的项目开关；-100%修正不自动等于全部输入归零 | 不优于A，仍需独立接口调查，不将普通乘数当全来源过滤器 |
| D. Cost=1或成本跟随当回合产能，完成后延迟奖励 | 原生生产路径简单 | 可被即时生产提前退出；延迟奖励不会让已经空闲的城市继续付出生产机会成本；产能变化/0产能也破坏固定时长 | 不是现行严格语义的等价实现 |
| E. 项目行只开自定义定时行动面板 | 不进入队列则不新增缺生产问题，已有生产可继续 | 只实现等待，不占用生产；除非另有可靠独占机制 | 商业菜单适用；直接用于时代对话会改Gameplay，不自动采用 |
| F. 直接dismiss生产通知或常开强制结束 | 可能暂时隐藏提示/跳过检查 | 通知可能再生成，且不等于停止原生阻塞；可能越过其它待办，仍没解决生产占用 | 不推荐，不作为降低复杂度的捷径 |

空队列路线仍有两个不同难度层：①通知/UI识别与安全显式结束；②真正连续占用一次城市生产结算、切换中断、0产能也只一回合、额外输入不提前完成、读档不多算。①现已找到局部可验证修正方向；②仍是主要未知。没有依据现在承诺②一定容易，也不能由①的一次错误断言②不可能。

### 外部参考及限定

- [Store Production作者页面](https://steamcommunity.com/sharedfiles/filedetails/?id=3676624054)：明确写项目Cost=999999，并提供把储存生产用于完成当前生产的UI。说明高成本占位是Mod作者使用的实际方向；并非不可完成/固定一回合方案。该Mod本机未安装，本轮未取得源码，不声称其内部储存/事件处理已审阅，也不采用其额外储存玩法。
- [Repeat Project作者页面](https://steamcommunity.com/workshop/filedetails/?id=1505351262)：重复运行项目解决排队操作，不提供严格计时或禁止即时生产证明。本轮不将其它Mod的重复项目宣称为时间锁。
- [Sukritact CityBuildQueue接口记录](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CityBuildQueue)：列AddProgress、FinishProgress及项目进度/队列getter；没有由该页面证实的通用“暂停生产且仍占队列”或全来源项目锁。页面非完整引擎规范；缺项不证明接口绝不存在。
- 本机Base `Gameplay/Data/Schema/01_GameplaySchema.sql` Projects表重核仍是Cost/成长模型/资格/次数等，没有在该表找到FixedTurns/IgnoreOverflow/IgnoreHarvest。OuterDefenseRepair是特定修防语义，不能当通用计时字段挪用。未重新运行DB或游戏。

公开检索没有找到可直接复用且已证明满足本项目全部约束的现成方案。无新实机/模拟PASS。建议先以原生target合同修正A的最小门禁，若target也无法可靠归属，再停止该路径比较B的受限原型；不边失败边扩大强制范围。本次只保存调查，下一实施需授权，用户当前无需测试。


## 14. B114.141 — native notification target repair

用户授权最小修复。B113实机失败与§13调查保留；本轮不扩大为正式固定回合项目。

归属改用原版NotificationPanel的`IsTargetValid()` → `GetTarget()`：通知属于当前玩家、未dismiss、有效目标的owner/ID/type同时匹配当前测试城市与CITY枚举。现有城市对象/所有者/本回合/空队列核对仍保留。`GetLocation`是镜头位置，不再作为城市归属条件；不从名称、坐标或通知数量猜测目标。目标无效/不匹配不放行，接口/字段未知暂停。诊断显示有效性、目标玩家/对象/类型及失败的操作状态。

其它B113保护不变：实际其它阻塞、其它空城、独立单位/城市攻击、HD政策确认及确认后重读、显式点击/普通Enter、请求前重复提交锁、同会话一次性状态、事件合并刷新、无hover扫描。原生DoEndTurn与Shift+Enter路径不改。无Property/队列/收益写入。

W0004 L2：`DevelopmentTests/test_b114_notification_target.py` 28项LOCAL_SIMULATION_PASS；继承B113保护测试，仅明确取代2项旧坐标判据及版本断言，旧文件不改。增加错误owner/ID/type、无效/缺失字段、点击及政策确认时目标变化、城市消失、诊断原因；相机位置调用直接报错的fixture仍可通过有效目标路径。Lua语法与modinfo文件检查STATIC_CONFIRMED。模拟不证明原生通知在该存档提供有效目标。

最小USER_GAME_TEST_REQUIRED：只让测试A城队列为空，其他城市指定生产并处理其他真实待办；选A点击“开启单城测试”，看右下角是否显示“下一回合”；先读一次“回合原型报告”，再正常点击右下角，确认只前进一回合且测试关闭。不要Shift+Enter。失败则保留报告截图，尤其目标有效/玩家/对象/类型和未放行原因，不反复强制请求。不是固定完整生产回合、砍树/溢出隔离或Claim验收。


### B114 native acceptance — 2026-09-27

[两图与用户人工确认](../../Status/Validation/Results/Specialization_B114_Target_Turn_Pass.md)：本场景CITY目标有效且匹配、正常按钮回合21→22、临时测试关闭、原生生产待办恢复；用户确认后续点击只开A队列。USER_GAME_TEST_PASS限此路径，§14待测项在此范围关闭。正式计时/生产占用、砍树/溢出隔离、保存恢复仍未验证，不自动进入实施。


## 15. Next prototype plan — production settlement and interruption

状态：PLAN_ONLY。B114限定原生按钮/目标/自动关闭验收已完成；用户“继续”后整理下一最小计划，不授权于本节直接实施。不是正式Claim、Dialogue或通用项目框架。采用§9用户范围：不负责第三方溢出分配，不建立生产力银行/退款，不修改第三方Mod。

### 目标与先后顺序

下一最小实施切片：**单城、无收益、session-only生产结算观察**。复用B114已验证的显式开始/按钮/保护，新增足够区分“日历变化”和“真实城市生产结算”的定域证据；先验证占用与中断，再加定向额外生产输入。不能把PlayerTurnActivated或turn+1直接写成完整生产回合已完成。

1. 实施前只读核对实际可用的Gameplay/UI生产与回合事件，以及队列/目标进度读取接口，确认参数/context。候选事件只有实际存在、接线验证后才列为证据；缺少可证明结算的事件/数值观测，报告TECHNICAL_PRODUCTION_BOUNDARY，不用事件名字猜顺序。
2. 通过既有UI→Gameplay请求桥开始一次单城session观察；Gameplay重新核对当前本地人类、城市引用、空队列。仅保存内存中的本次token、开始回合及有界事件记录，不写永久Property/既有E2账本。UI展示缓存结果；不建立真实项目、不伪造项目完成事件。
3. 观察仅限目标城与必要本地玩家事件；选定事件到来才读相关对象。无活动立即返回；不全城逐回合扫描、不per-frame或hover请求。日志固定上限，溢出明确报证据不完整，不静默丢失关键事件。
4. 原生非空生产选择/入队事件一经确认，立即将本次观察标为中断；后来再次清空不能恢复旧token的连续性。手动重新开始才形成新观察。不得主动清除玩家新队列、自动恢复旧队列或阻止合法砍树。
5. Owner/城市对象失效、接口未知、事件证据矛盾则退出豁免并保留简短原因；UI不把旧快照当当前许可。重复通知不重复结束。沿用B114请求防重，另审Gameplay确认与UI缓存失效间的接线，不借机重构桥。
6. 回到本地玩家新回合后，停止本次观察并展示结算事实；只有充分证据才标记“观察到一次生产结算”。只有回合号变化则明确“计时已前进，生产结算未证实”。不发奖励，不标真实项目完成。

### 最少实机步骤与判据

复用一座有正常生产力的A城和一个已有存档分支；其它城市按正常方式安排生产。报告尽量只显示城市、开始/结束回合、队列连续性、关键事件顺序、相关进度变化、结论及缺失依据。

| 情形 | 操作 | 要回答的问题 |
|---|---|---|
| 基线 | 记录一个此前未投入生产的普通目标Q；A空队列开始观察，正常过回合，再选择Q并记录即时进度 | 实际生产结算时A是否仍无目标、期间是否没有生产其它内容；空队列正常产能是否被以后兑现。不能仅以Q进度0推断所有生产来源均清零 |
| 中断负例 | 开始观察后选普通生产目标，再清空队列 | 旧观察必须已经中断；不能因结束时再次为空而算连续占用；普通生产操作不能被自动撤回 |
| 一次收获 | 从同一前置存档分支，A空队列开始后砍树/收获一次，再正常过回合 | 额外输入不造成提前观察完成、不自动创建其它生产；是否跨越同样结算边界。无需决定或修正收获最终流向 |

基线/中断先通过再做收获；基线失败即暂停，不要求用户继续所有分支。正式开始实机前按可用存档和工具压缩具体操作；需要读档分支时使用已知稳妥的完全退出再载入，不把此前同session载入崩溃扩散成新的调查。

已有溢出作为后续同一fixture的定向补充，只有能可靠构造并观测起始值才测试；不要求用户研究溢出Mod内部。不用Cheat的FinishProgress充当自然生产证据。低/零生产对照及完整读档恢复不塞入首个session观察切片；它们仍是正式固定时长合同后续必需门禁，不能随首切片PASS自动关闭。

### 最小本地验证与可能改动范围

W0004 L2，只有接入持久化时才另定L3切片。针对实际Lua测试：无观察零工作、开始资格/目标token、相关事件顺序、切换再清空必然中断、重复/迟到通知、失城/未知停止、UI确认过期不豁免；继承B114按钮安全测试，静态检查modinfo/直接调用点。不要用fixture预设事件顺序证明引擎顺序，不跑无关玩法回归/stress。

预计仅触及TimedTurnProbe、现有诊断/请求桥最小入口、一个必要的定域Gameplay观察模块（若现有模块无法合理容纳）、modinfo/版本和本批测试/记录。具体Gameplay接线在授权实施时按实际直接依赖核对，不预先承诺不存在的事件或跨context方法，不改E2永久状态和现有收益writer。

### 停止、回滚与后续门禁

若无法证明一次真实结算、空队列正常产能被以后兑现导致机会成本含义不明、无法捕捉中途切换、错误吞掉普通目标进度，停止对应路径并报告。不要自行扣生产、改Design或把纯等待改名为生产占用。原型无永久状态/收益，回滚B114包恢复已知按钮原型；不自动清理用户存档/队列。

通过本片只允许提出下一计划：Gameplay权威的连续占用与完成条件、save/load恢复/去重，再接正式项目入口。Claim须真实满足已接受的“完成城市项目”，不能借自定义timer自动建立Identity；Dialogue的启动时代/完成时X及一次额度也不在本片。正式多城并行、全部政策/阻塞组合及产品UI另行验证。

当前没有新增Design决定要求，没有新用户测试包。审批对象是上述最小session观察切片；当前不部署、不启动游戏、不实施Claim/F。


## 16. B115.142 — session production observation implementation

§15已获用户“首选实施”授权，按最小原型实施；无正式Gameplay项目、收益或持久化。B114按钮验收保持其原范围，新异步Gameplay确认和中断链仍待原生验证。

### 已核对接口与接线

原版Base UI `CityPanel.lua` 的CityProductionChanged/Completed/Updated以owner、cityID开头；TutorialUIRoot.lua记录Changed的orderType/unitType/canceled/typeModifier。CityBannerManager.lua监听CityProductionQueueChanged。HD Gameplay使用GameEvents.PlayerTurnStarted及Events.PlayerTurnActivated。这些是监听候选的STATIC依据，不证明所有事件在Gameplay到达、回调发生于结算之后、空队列仍发Updated或原生队列字段的全部空值形态。

沿用Gameplay.lua的SPC_P0_Request入口，添加两个提前返回的定域动作TIMED_PRODUCTION_BEGIN/CANCEL，原eligibility/token检查保留；TimedProductionProbe.lua只维护单次内存状态和不超过24条事件，ExposedMembers发布副本。UI通过已有EXECUTE_SCRIPT通道请求，匹配本次token/owner/city/turn且Gameplay ACTIVE确认后才启用B114豁免。未知/拒绝不放行。token使用session序号，取消只接受原token；UI重新加载不凭旧结果自行arm。

Gameplay当前目标用已在ConstructionProbe使用的CurrentlyBuilding读取；成功读取nil/空字符串作为无目标候选，其他返回值停止并显示原值，不假定UI的hash=0能跨context套用。完整队列为空由已验证UI GetSize再次核对；不把该实验当作已完成Gameplay队列authority。开始或关键接口缺失显示具体原因，不改为空默认值。

观察CityProductionChanged/QueueChanged/Updated/Completed、PlayerTurnDeactivated、GameEvents.PlayerTurnStarted、PlayerTurnActivated、CityRemovedFromMap；仅匹配观察对象读取。目标改变/队列改变/完成通知保守中断，即使读取时已经再次为空；UI也在变化事件立即撤销豁免，防止等待合并刷新期间切换再清空。若原生同名事件实际上仅为无目标刷新导致误中断，应记录EVENT_SEMANTICS_BOUNDARY，不能未经证据放宽。Updated只记有限参数和当前目标，不当作一次完整结算。

到本玩家新回合观察结束，明确“完整生产结算未证实”，不发完成奖励。UI回合关闭不提前取消Gameplay待收集证据；Gameplay先关闭时UI仍在回合变化后释放提交锁。报告最多显示首3/尾5条，其余保留缓存供现有写日志按钮导出。按需报告另读取当前UI队列及原生目标进度getter（CitySupport.lua已有对应Buildings/Districts/Units/Projects路径）；不在hover请求、不写进度。

### 验证与风险边界

W0004 L2：`DevelopmentTests/test_b115_production_observer.py` **45项LOCAL_SIMULATION_PASS**：继承B114按钮保护、实际Gameplay请求函数分发/非法token、异步确认、目标切换再清空、缺hook、额外Updated不完成、其它城/玩家不扫描、边界结束不冒充结算、24条上限、迟到取消/重复开始、重开session为空、Gameplay/UI先后顺序与提交锁。Lua语法/modinfo155文件存在检查STATIC_CONFIRMED。测试fixture不证明原生事件顺序；没有玩法全回归或stress。未新增存档字段、carrier、生产操作或第三方改动。

原生仍需确认Gameplay空值、监听送达、异步确认与中断；若只观察到turn变化而无城市生产证据，结果仍是TECHNICAL_PRODUCTION_BOUNDARY。原型不会自动判完整生产回合PASS。正常产能是否被以后兑现、额外输入是否破坏占用仍需下面原生读数，不能提前宣布隔离已完成。

### 最小用户流程：先基线，再中断

使用独立测试存档。选此前未投入生产的普通目标Q，先指定Q并截图当前生产进度，然后手动清空A队列；其它城市安排好生产。

1. A空队列点“开启单城测试”，再点“回合原型报告”。必须显示Gameplay ACTIVE；若STOPPED/一直等待/未知则截图暂停。关闭面板，处理其它待办，正常点击下一回合，不Shift+Enter。
2. 新回合先左键报告截图；再给A选择同一Q，立即左键报告截图（不要再过回合）。这提供事件序列及即时目标进度；不得把进度来源直接归于正常产能，需结合开始基线。
3. 基线未报异常时，手动清空A，重新开启观察，然后选择Q再清空；左键报告应显示中断/关闭，原生生产待办恢复。不得自动清队列或沿用旧观察完成。

本包先只请求这一个基线+中断流程。收获/已有溢出实验待上述接口事实确认后用相同fixture定向追加；不让用户在开始失败时继续一整套测试。完整重启恢复、低/零产能和正式计时/入口尚未实施，不随本包验收关闭。游戏已退出获用户确认，验证后按W0003部署，保留B114恢复点；回滚无需清除存档字段。


### B115 native start failure and test correction — 2026-09-27

[第一步截图](../../Status/Validation/Results/Specialization_B115_Empty_Target_Boundary.md)确认空队列时Gameplay返回NONE；仅nil/空字符串判据错误拒绝，观察未开始。下一修复必须统一开始/采样判据并补测试；UI空队列不能解析hash为正在生产纪念碑，错误堆栈应退出简报。保留旧本地证据局限，不将开始失败解释为结算方案已失败。

§15/§16中要求玩家“选Q再清空”“中断后再清空”的原生操作步骤由用户纠正：仅使用自然完成后的空队列；基线先空队列跨回合再选此前未投入Q，中断为另一次自然空队列开始后选择Q。不能把原生队列编辑接口推断为玩家可清空当前生产。切换再清空仅本地防御性模拟，不要求用户做或通过强制清队列实现。此前测试说明保留为已被本段取代的过程记录。


## 17. B116.143 — NONE sentinel and concise diagnostics repair

用户授权修复B115开始失败。统一empty判据用于开始与后续采样，明确接受原生截图确认的字符串NONE以及原有nil/空字符串；不接受其他近似字符串、false或数值0，不改变接口失败停止、真正目标变化中断、异步确认和B114按钮保护。

空UI队列先返回“无生产目标”，不读取hash、不查GameInfo或目标进度；非空队列要求有效非零hash、唯一类型与合法数值进度。不能把空队列时纪念碑=0当作真实目标。Gameplay错误完整内容写日志并保留errorDetail供已有诊断导出；屏幕只显示去掉路径/堆栈的短原因，开始与后续读取共用处理。无生产/奖励/永久状态写入。

`DevelopmentTests/test_b116_empty_target.py`：53项LOCAL_SIMULATION_PASS，继承B115实际Lua/UI/请求保护并以NONE为默认fixture；补开始/Updated/回合边界、合法空值、非精确NONE拒绝、空队列不读取残留hash、非空真实进度/零hash拒绝、行内/多行堆栈缩短及全文留存。Lua/modinfo检查STATIC_CONFIRMED，原生开始和生产结算仍USER_GAME_TEST_REQUIRED；没有无关全回归/stress。

测试只用自然生产完成后未选目标的A城：开启→报告应ACTIVE→正常过回合→报告截图→选择此前未投入的普通目标Q→立即报告截图。任何开始错误立即暂停，不要求手动清空生产；中断测试另一次自然空队列开始后选择Q即可。收获/溢出/正式固定回合项目未推进。

部署安全：本次普通sandbox的ps被拒绝，获准只读进程检查后确认无Civ6/Civilization/Aspyr进程。应先自动尝试可用进程检查，仅不可确认时询问退出状态，不将过去一次权限失败永久当作环境限制；不改部署机制/Workflow。


### B116 native baseline — 2026-09-27

[三图证据](../../Status/Validation/Results/Specialization_B116_Production_Baseline.md)：NONE开始修复及空队列诊断限定PASS；BEGIN→Deactivated→Started后ENDED，随后选择粮仓进度8。完整生产结算与机会成本未定。观察在Started自动停止，不可把采集窗口内无Updated外推成整个周期不发事件；粮仓8点不能未经起始/输入核对就归因正常产能。先查来源/事件窗口，不进入正式计时或收获验证。活动中断未由“结束后选择目标”证明。


## 18. B116 follow-up — overflow application versus production origin

2026-09-27，用户授权继续只读调查。用户已明确：选择粮仓前面板无该建筑已有进度，选择后才出现8点；期间无砍树/收获/Cheat。不能再将其表述成仅“不记得旧投入”。本节不修改B116冻结截图证据，不实施、不部署。

### STATIC_CONFIRMED：独立溢出Mod的应用入口

完整读取本机Workshop `289070/2589004769` 的 `OverflowBugFix.modinfo`、`OverflowBugFix_Switchable.lua`、`OverflowBugFix_helper.lua`。Switchable第27–39行监听CityProductionChanged：人类在自动模式调用AddZeroProduction，AI不受开关影响；不筛选目标类型或取消参数。helper第5–9行仅调用 `city:GetBuildQueue():AddProgress(0)`。该Mod没有自己的生产力账本、跨回合积累公式或8点计算，也没有改写回合末清零的代码。

因此存在与截图吻合的链：选择粮仓→生产目标变化→AddProgress(0)→由引擎应用已有生产存储。[作者说明](https://steamcommunity.com/sharedfiles/filedetails/?id=2589004769)同样说明其功能是把已有溢出立即应用于新目标。静态链并非本次实机调用trace，尚不能证明它是唯一触发者；更不能把“它负责应用”写成“它产生了这8点”。

Switchable第9、41–61行已有A/M开关：M模式停止人类自动应用，另一个手动按钮对选中城市调用同一AddZeroProduction。开关是局部内存变量，初始化默认A；冷加载后需重新确认M。M→A切换本身不调用AddProgress。无需卸载Mod或更改本项目代码即可进行应用时机对照。

### 引擎清理与来源仍未确认

[Firaxis September 2019 patch notes](https://support.civilization.com/hc/en-us/articles/39409989034643-Patch-Notes-September-2019-Update)记录回合末强制清除overflow、防止空队列强制过回合囤积，并记录部分奇观返还到turn-active再应用。它不证明当前Mac/HD组合的具体结算顺序，也不等于所有场景的生产都被立即删除。不能据此判定这8点必然是旧溢出或必然是空队列回合产能。

B116观察在首个新回合PlayerTurnStarted处ENDED；其后生产通知不再采集。三条记录未出现Updated不能证明之后没有结算。Base/Expansion2 UI的定向搜索未发现现成overflow读取getter；这不是“引擎不存在该接口”的证明。HD CivilizationTraits中的对应生产变化hook有特定领袖/区域完成路径，未在这些直接hook中发现通用“选粮仓赠8点”；未排除全部HD/其它Mod行为。

### 下一最小验证建议（尚未执行）

优先复用如有的“新回合、尚未选粮仓”存档，冷加载后先切M，再选择粮仓记进度，随后按该Mod手动应用按钮再记进度。若0→8，则直接支持已有生产存储经AddProgress(0)兑现；若选目标时已为8，则不能归因这个自动入口，需保留其它路径调查。不要把切M当作清除存储，也不要卸载Mod或修改存档。

此对照仅查应用机制。查来源需要更早的同一基线分支，比较空队列过回合前/后的可应用存储；清除和重新积累可能同时发生，差值不能未经事件证据直接等同正常产能。若现有存档不适用，不要求伪造基线或重跑整套流程。后续若改观察器，应将“过回合豁免结束”与“有限只读结算证据采集结束”分开，另获实施授权；不延长项目、补扣生产或包装第三方函数绕过未知。

结论：应用路径STATIC_CONFIRMED、与截图一致的因果解释仍待原生对照；8点来源与完整生产机会成本仍TECHNICAL_INVESTIGATION_REQUIRED。没有新增LOCAL模拟或USER_GAME_TEST结论；正式固定回合项目、收获隔离、Claim/F均未推进。


### B116 native M/A comparison — 2026-09-27

[四图对照](../../Status/Validation/Results/Specialization_B116_Overflow_Mode.md)：M模式21→22回合空队列后粮仓0；用户Cheat完成粮仓、切A后再观察22→23，磨坊8，城市显示8.3/回合。与前次无Cheat的A模式粮仓8及AddProgress(0)静态路径共同支持自动溢出参与即时应用。不是同一目标同基线单变量实验，也未执行M下手动按钮0→8，不扩大为唯一因果或精确来源证明。Cheat是第二段来源的局限，不否定模式差异与上一轮证据。

不再要求重复相同模式现象；本项目不能把“空队列”等同“生产存储已清除”。尚需解决的是固定回合占用的生产隔离合同，不是修改第三方Mod。8与8.3接近不足证明floor或精确回合来源；关闭自动也不代表库存消失。下一建议为原生存储/结算与本项目定域隔离的只读调查，任何新写入/原型需另授权。无新实施、测试包或Design变更。


## 19. Production isolation follow-up — negative progress precedent and remaining primitive gate

2026-09-27，用户授权继续研究；只读本机相关API调用、Projects schema和外部作者源码，无原型写入/部署/游戏操作。承接§18及四图结果，前轮无Cheat的A模式粮仓8与本轮M模式粮仓0是主要对照，后段A模式磨坊8仅补充；不再将Cheat局限扩展到全部证据或要求重复证明自动应用影响。

### 搜索范围与直接结果

定向搜索本机原版/DLC Assets及已安装Workshop Lua中的Set/Change/Get/Clear Overflow、ProductionOverflow、ProjectProgress、ProductionProgress与负数AddProgress调用。命中主要为项目进度读取和科文溢出辅助；未找到城市生产overflow直接读写/清除先例，也未找到已安装Lua中的字面负数AddProgress调用。这是限定符号搜索，不是全API穷尽或所有Mod语义审计。没有把Civ V的City:SetOverflowProduction一类文档套用到Civ VI。

[Sukritact CityBuildQueue](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CityBuildQueue)列Gameplay AddProgress/FinishProgress，项目进度getter列在UI；未提供经该页面确认的overflow setter。不能据此声称不存在未收录接口。下一次如做原型，可只读枚举实际Gameplay/UI对象可访问方法，分开两context，不通过猜参数调用陌生写入API。

### 新发现：GCO确有负数AddProgress用法，但不能直接移植

读取作者[Gedemon/Civ6-GCO 的 GCO_CityScript.lua](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_CityScript.lua)（读取日期如上；master不是冻结版本）。DoConstruction约5841–6006行仅在当前目标有Units/Buildings row且production>0时进入；效率不足时约5995行调用AddProgress(-production)，把actualProd缓存，在CityProductionUpdated约7527–7535再AddProgress补入并清缓存。作者意图是先抵消正常结算，避免提前生成目标，然后应用实际效率。源码存在是STATIC_CONFIRMED，不等于本项目或该Mod当前原生验收。

关键限制：约5992–5993行作者仍将“能否保存负进度，尤其目标成本小于单回合产能”列为TODO。空队列不满足该row分支，项目也不在该分支；没有展示空队列负数会扣overflow。GetProductionYield/GetProductionProgress约7742–7747是作者自建GCO包装，不是新增原生City方法。不能复制一个看似简单的负数调用，就宣布能清除8点或保证一回合。

本机Cheat Panel `1528155583/Base/UI/Script/Cheat_Menu_Panel_Script.lua` CompleteProduction约68–73调用FinishProgress，不是显式AddProgress(大量数值)。这减少了“Cheat显式灌巨额锤”的依据，但FinishProgress对内部存储的影响仍未观察，不能由调用名宣布无副作用。此调查不要求用户重新证明前两段A/M结果。

### 三条候选路线的取舍

| 路线 | 可复用的依据 | 必须先证明的边界 | 当前判断 |
|---|---|---|---|
| 空队列＋精确定域生产抵消 | B114按钮与B116空目标已验；GCO负数调用提供新先例 | 空队列负数究竟扣目标/存储/被clamp/形成负债；结算时序；只抵消占用回合，不误删此前合法溢出；收获仍需单独确认 | 优先研究primitive，不直接投入正式能力 |
| 真实无收益占位项目＋时间门槛 | 原生队列可占生产；AddProgress/FinishProgress可操作 | 高成本仍有限，收获/自动应用可提前完成；提前完成后排队目标可能获益；没有确认的“不可自然完成”字段；主动完成余量去向 | 保留备选，不能把无限大成本当严格保证 |
| 占用期间压低城市/项目生产 | 现有modifier系统可表达部分产能调整 | 不证明旧存储/收获/直接AddProgress被过滤；百分比叠加和撤销时序；其它生产转换能力交互 | 未优于精确定域方案，不能仅挂-100%就宣布解决 |

Base Projects表复核仍未发现固定时长/IgnoreOverflow/IgnoreHarvest字段。Cost为INTEGER并不证明-1有“无限”语义；不得借数据库允许负数推断引擎合同。UI入口拦截只能控制进入动作，不能控制之后的所有生产来源。拦截/替换第三方AddZeroProduction也只挡一个触发者，不处理原生存储；不是推荐兼容方案。

### 推荐下一最小技术原型（仅建议，未实施授权）

先验证负数primitive能否触及空队列存储，而不是马上做时代对话。限定一座独立测试城、单次手动触发、没有正式奖励/保存字段/全城扫描；同一基线分支对照，新增的必须是真正的原生证据，不能以Lua模拟证明C++行为。

- 第一门禁：可访问方法只读枚举；负数写入仅用已确认AddProgress，先在专用测试目标确认精确下降/clamp行为，不能对玩家有价值建筑作未经核对的回扣。
- 第二门禁：空队列中单次负数调用后选择测试目标，比较无调用分支，再观察下一回合是否有延后负债。已知存储量不能凭8.3面板直接假定；若无法构造/读取受控基线，先停，不以大负数清零冒充精确抵消。
- 同时修正证据窗口：回合按钮豁免按时关闭，但有限只读采集继续覆盖后续本玩家激活/相关生产事件；这些事件先作为观测，不预设任一事件就是完整结算结束。
- 若空队列负数无效或只改其它目标/出现不可解释负债，停止该路线；若有效，再研究实际结算输入和旧溢出保留，随后才安排收获/中断/冷加载。不得自动把整个存储删除定义成项目成本。

这比再切一次A/M有信息增量，但含实验性生产写入，必须另行授权。仍没有STATIC可以证明的完整一回合实现，亦没有证据证明绝无实现办法。本轮不提出Design修改、不把等待替代生产占用、不要求新增用户实机流程。当前建议明确收敛到primitive验证，避免重复整套按钮/溢出模式验收。


## 20. B117.144 — authorized forfeiture contract and minimal storage primitive test

### 用户已接受的本片Gameplay合同

本轮用户明确：进入该特殊项目时，放弃城市全部当前未分配production overflow/stored production，包括项目开始前合法存量；项目占用期间正常产生或chop/feature removal、Bonus Resource harvest及类似一次性注入的生产不能转移给下一个目标。无需维护旧存量/新增量账本。此决定取代§19“必须保留旧合法溢出”的候选限制，不改其它资格/时长/中断规则；正常目标已拥有的progress不属于未分配存储，不能误扣。记录为本轮明确接受的规则，不是Codex技术推断；正式项目接入前须按Design修订流程同步相关Spec/Content/阅读版，本批不扩展整个Design revision。

### 本批范围与实际实现

用户授权技术可行性及最小测试。先验证负数primitive，未把未知接口自动接入项目。B117.144新增OverflowStorageProbe与UI/OverflowStorageRead，由现有Gameplay请求桥接、P0Panel既有隐藏按钮位置接入“溢出清除试验”；原B116观察器/按钮逻辑保持原字节。没有正式项目、carrier、奖励、持久属性、自动扣锤或第三方Mod改动。

左键第一次：只读UI队列和所有Buildings/Districts/Units/Projects进度（一次最多4096项），Gameplay确认己方合格城、当前目标精确空值、接口/事件可用，并记本回合/城市位置/生产事件epoch。第二次左键：重新核对UI队列、进度快照、owner/city/位置/回合；Gameplay再核对同一token和状态未变，锁存后仅一次AddProgress(-1000)。这是诊断量，不是可靠的“全清”算法，存储超过1000或负债语义都不能宣称全清。未知/非空/变化一律拒绝；事件缺失拒绝。每城每次加载一次写入，异常也不重试；会话最多16城，实际测试只用一城。

首次ack后UI核对各目标进度是否变化，不写目标进度、不以零变化证明存储清空；缺接口/未知读数先停止。右键只读结果及变化进度，允许显示负值而不隐藏异常。无hover请求/每帧扫描/自动重发；GameCoreEventPublishComplete只在显式请求等待时检查缓存，确认后停止；生产事件只使当前prepared城失效。旧过回合豁免独立，清除实验不自动过回合或改队列。

### 验证证据与未完成目标

W0004按有限生产写入风险采用定向验证：77项LOCAL_SIMULATION_PASS（真实Lua与请求分发/UI模块，含B116 53项直接回归）；Lua加载、modinfo144的157文件清单/重复检查STATIC_CONFIRMED。新用例覆盖两次点击、负数一次调用、重复/错误token、非空/未知、城/owner/回合变化、事件变化后回到空、缺接口/缺事件、原生异常锁存、延迟ack不自动重发、已有进度受损报告、负读数可见。模拟的storage clamp/debt/target三种引擎候选均只报CALLED_NOT_PROVEN，不把fixture模型当原生结论。未跑无关全回归/stress。

| 用户目标 | 本包支持的验证 | 当前证据 |
|---|---|---|
| 进入时清未分配存储 | 自然空队列上显式执行一次候选调用，之后看新目标 | USER_GAME_TEST_REQUIRED，未自动接入开始按钮 |
| 不误扣已有目标进度 | 准备/确认/ack对照全部可读目标进度 | 本地保护通过；原生仍待验，必须有非零旧进度才覆盖非平凡场景 |
| 不留负债 | 清除后选Q，再跨一个正常生产回合看增长 | USER_GAME_TEST_REQUIRED，不自动补生产修复 |
| chop/harvest不向后溢出 | 同一测试前档另分支，空队列注入后再调用候选清除 | 第一门禁通过后再做；并未自动监听清除所有注入 |
| 替代实现 | 本报告§19已有原生占位项目/产能调整候选及反证 | 负数实机失败则停止此路线，再收窄替代原型；不加大负数掩盖失败 |

### 最小用户测试：先一例，失败立即停止

仅独立测试档；保留调用前存档，不覆盖它。若负进度写入引擎，回滚Mod不能撤销已保存的生产状态，必须回到测试前档。暂时不要把实验后存档作为长局继续。

1. 使用此前“自然空队列过完回合、还没选粮仓”的状态，溢出Mod保持A。若只有过回合前档，仍按已验证单城测试过一回合，先不选目标。不要先Cheat完成目标来构造本次存储。
2. “溢出清除试验”左键准备，显示尚未写入；再左键确认。截图。若REJECTED、UNCERTAIN、普通目标进度变化、读取失败则停；CALLED_NOT_PROVEN只表示调用返回，不是成功清空。
3. 选择此前未投入的Q，右键“溢出清除试验”截图。预期候选成功表现为Q仍0；若仍8（或其它存储残留）则本路径未通过，不连续扣除。
4. 正常生产Q一个回合，再右键截图。应有正常正增长；仍0/负值/异常少产即负债或其它边界，停。不预先规定8.3的floor/小数结算。

仅1–4通过后，才从测试前档另分支验证一次chop，再另分支Bonus Resource harvest：目标城空队列注入→候选清除→选Q及正常下一回合，需另一个无清除分支确认注入原本能到达该城后续目标。每次实际注入数值记录，超过1000不能用本测试量证明全清。无需同轮完成全部步骤；正常已有目标进度保护可用已有部分建造进度的同城补充，不要求玩家手动清空生产或改造全部fixture。

原型不会在项目开始/结束自动清理；因此第一门禁PASS也不是完整最终项目PASS。之后还需决定可靠清除primitive的全范围和执行时机、项目占用期注入、取消/中断与保存重载收尾；不借本包进入Claim/F。

部署记录：B117.144 source `c488942`，已只读确认无游戏进程；按既有工具B116→稳定桥→B117，157/157源/运行文件MATCH，receipt `B117.144-c488942-playtest.json`。B116运行恢复包保留，main未修改/推广，未启动游戏。实际native验证仍待用户。

### B117 native result — negative production debt

2026-09-27 [四图原生结果](../../Status/Validation/Results/Specialization_B117_Negative_Production_Boundary.md)：空队列单次AddProgress(-1000)之后选磨坊为−992，下一正常回合−984，原生面板亦为−984/60。清零候选USER_GAME_TEST_FAIL / NATIVE_NEGATIVE_STORAGE_BOUNDARY。上方“待验”表和步骤保留原测试计划身份，现由此结果关闭第一门禁：不自动clamp到零，有延后负进度；即时目标快照未变不能证明安全。停止这条盲目负数清零候选，不继续chop/harvest，不猜测补回生产。

全清Gameplay合同保持；这不证明所有清除方式不可行，也不证明内部存储布局。后续仅调查明确重置接口、可靠读取实际存储后精确扣除或独立承接清理；均未获原生确认。本次只归档证据，无代码、部署、正式项目或Claim/F推进。测试后应回实验前存档，Mod回滚不能撤销已保存负进度。

## 21. Post-B117 — reset, exact subtraction and disposable sink investigation

2026-09-27；用户授权只读调查。依据B117已归档的−992→−984反证，本节不调用任何游戏API，不修改Mod/第三方Mod/存档，不部署。原“全清未分配存储＋占用期生产不得转移”合同保持。

### 直接重置与可读取事实

复核[Sukritact CityBuildQueue方法目录](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/CityBuildQueue)及本机原版Base/DLC Lua、已安装Workshop Lua的定向符号搜索：未找到有可核对调用先例的生产overflow getter/setter/reset，也未找到通用SetProjectProgress。这是搜索边界，不是引擎API不存在的证明。未来只读枚举实际Gameplay/UI对象可访问方法仍有价值；不得猜写入方法/参数。

原版`Base/Assets/UI/CitySupport.lua:274`及`Panels/ProductionPanel.lua:2222`确实读取GetProjectProgress(project.Index)：它是指定项目的进度，不是城市全部未分配存储。目录里的GetProductionYield没有本轮本机Base/DLC Lua调用先例，参数及是否涉及存量不能凭名字断定。CitySupport:237将GetCurrentProductionTypeModifier用作MilitaryFormationType；它不是可用来消除生产倍率的通用百分比getter。

原版`ProductionHelper.lua:196–201`移除队列项仅发送BUILD/VALUE_REMOVE_AT，没有清除进度调用；不能用这个UI动作证明项目进度或overflow被删除。TunerCityPanel:103的CreateIncompleteBuilding是建筑放置/进度接口，不能推定能重置城市池。删除建筑的接口也不等价于清未分配生产，更不应借删除普通建筑解决。

### 其它溢出Mod提供什么、不能提供什么

本机Workshop `2772516161/Gameplay/OverflowBugFixGameplay.lua:1–23`把科技溢出存在虚拟科技，使用SetResearchProgress读写并清零；UI又有对应虚拟市政路径。`2604740398/CheckOverflow.lua:8–35`通过临时修改科技/市政进度、读取剩余回合来逐步夹逼溢出（终止精度0.05），不是纯只读getter，也不是精确城市生产存储接口。两者均依赖科技/市政专用setter，不能移植函数名到CityBuildQueue，也不能宣称它们证明城市存储可安全清零。未修改这些Mod。

### 三条路径的结论

| 路径 | 已知依据 | 当前缺口/处理 |
|---|---|---|
| 直接reset | 当前搜索无确认先例 | 保留TECHNICAL_INVESTIGATION_REQUIRED；先只读方法枚举，不伪造API |
| 空队列按精确存量扣除 | B117证明负调用能随后影响目标；并未证明精确抵消安全 | 没有可靠存量getter；不从8.3城市产能、剩余回合或截图整数反推全池。盲目−1000退出 |
| 独立目标承接→读取其进度→精确扣除 | 原生项目进度可读，AddProgress可写；把隐藏存量显现到专用目标有可测试依据 | 组合尚未实测：扣除对象、倍率/精度、延迟存量、切换回返、大额注入先完成、取消/重载均待证实。优先缩成单次primitive实验 |

第三条不是“堆一个极高Cost就解决”。有限Cost始终可能被大额注入跨过；生产完成事件可能晚于原生成果/溢出的发生。取消队列项不代表删除其已投入进度；换一批新项目ID躲残留也不是可维护清理方案。-100%产能不能自动推出stored/chop/harvest/AddProgress全部被屏蔽。让项目自然完成或FinishProgress也不能无证据当作销毁全部余量。

### 推荐下一最小原型（计划，未实施）

不重复B117大负数实验。先验证“已知目标进度的精确扣除”是否成立，再决定是否值得开发承接项目：

1. 独立实验前档，一座城、一个无收益的专用测试项目；读取实际可见方法，不调用陌生writer。项目Cost只是实验防提前完成条件，不是最终无限容量承诺。
2. 当前目标与owner/回合固定，确认项目尚未完成。通过一次有界应用使存量进入此项目，读到确认进度p；无法读到可靠数值、出现完成/切换/额外事件即停止，不能把UNKNOWN当0。
3. 仅对当前专用目标一次AddProgress(-p)。观测本目标是否真为0、其它已有目标是否不变、是否产生未分配负债；不得在UI读取后跨任意操作仍使用陈旧p，也不得失败循环回扣。
4. 切到对照目标并正常生产一回合，验证没有正/负残留。这个组合native通过以后，才安排chop/harvest、同回合中断、重载与大额完成窗口。

UI getter→Gameplay writer不是自动原子事务；确认快照、事件失效、跨context读数精度都是原型门禁。测试通过也只能证明该受控数值/目标组合，不能升级为任意注入全清或固定一回合项目可交付。若精确扣除仍只制造隐藏债务，则停止该组合，回到直接接口调查，不继续依赖补偿抵消。

本轮结论：没有已证实可直接替换B117的可靠全清实现；有一个比盲扣更可证伪、范围更小的下一验证方向。STATIC_CONFIRMED仅限上述本机源码调用；新方案保持TECHNICAL_INVESTIGATION_REQUIRED / PROTOTYPE_REQUIRED，没有新LOCAL或USER_GAME_TEST PASS。无需用户本轮重新测试。


## 22. B118.145 — authorized exact-project subtraction primitive

用户授权§21最小实验。B118替换B117固定−1000入口，不保留可执行盲扣；仍是实验而非正式固定一回合能力。新增PROJECT_SPC_OVERFLOW_SINK_TEST，中文“溢出承接实验（无收益）”，City Center资格、Cost1000000/无成长，只为受控实验避免早完成；无GPP、转换、completion modifier或任何奖励。不是无限sink承诺。玩家手动选择项目，本Mod不改队列、不FinishProgress、不自动AddProgress(0)、不调用其它Mod。

现有“精确扣除试验”左键准备、再次左键单次扣除；右键只读。要求该项目是唯一队列目标、0<p≤10000；0/负数/超界/未知拒绝。即时UI读数桥独立挂在ExposedMembers，避免Gameplay初始化替换状态表导致入口丢失。UI准备保存同城全部可读进度，确认再比；Gameplay准备与写入前通过即时UI读数桥重读项目、队列、回合和进度，并与本次请求及prepared p匹配。期间相关生产事件、owner/位置/回合变化拒绝。写入前锁存每城每次加载一次，即使原生异常也不能重试；最大16城只为会话边界，实测只一城。AddProgress(-p)不自行floor。跨context路径、原生数值精度仍待实机确认；不声称事务原子性。

UI把专用项目变化与其它目标变化分开：期望项目p→0、其它0项变化。任何非零/负数/其它目标受损即停止；即时0也只报读数，不报全清PASS。无hover/per-frame扫描，只有显式准备/确认/报告扫描一城目标（最多4096）；ack只在请求等待时读取缓存。B116计时/按钮原型保持原字节。未添加保存属性，未进入Claim/F，未改变正式Design。

本地证据：75项定向LOCAL_SIMULATION_PASS（直接B116回归53＋精确primitive22），含实际P0Panel初始化、Gameplay dispatch、正数/小数、未知/负数/超限、时序/事件/对象变更、重复与异常不重发、延后请求重读、错误扣到隐藏池/其它目标时报告失败。Lua语法、modinfo145的158文件与SQL fixture STATIC_CONFIRMED。实际DebugGameplay数据库只读复制至内存验证新增项目schema/FK；其Make_Hash原生函数本地不可用，明确使用本地stand-in，仅确认SQL结构，未证明native hash或数据库载入。没有无关全回归/stress。

### 本次最小实机步骤与停止条件

1. 完全重启后读取B117扣除之前的测试档；不要使用已经负进度的存档。保留溢出Mod原自动A设置。选择一座测试城，在城市生产列表选“溢出承接实验（无收益）”，队列只保留这一项。它不是要求玩家把已有未完成目标清空；可以正常切换目标。若找不到项目/按钮、数据库未加载或文本异常，截图停止。
2. 诊断“精确扣除试验”右键读数并截图。若项目已经承接正进度，可继续；若为0，仅正常生产一回合再准备。这一分支只验证已分配项目进度，不证明已有overflow被捕获；不要砍树/Cheat构造本次基线。负数/超过10000/项目完成立即停止。
3. 左键准备，确认显示p；不做其它操作，再左键扣一次。右键截图：项目应p→0、其它目标变化0项。拒绝/未知/非零或负值均停止，不能靠反复点击修复。
4. 同一回合切换到此前0进度的正常目标Q（替换项目，不把Q仅排在后面）；右键与原生生产面板截图，Q应仍0。正常生产一回合，再截图，应正常正增长且无负债。不要返回测试项目再次执行扣除。

当前只验证一次受控项目清理和后续残留。chop/harvest、超大注入提前完成、中断/存读收尾均后置；任何失败回测试前档。新数据库项目若旧开发档没有载入，不修改存档硬塞对象，先报告具体数据库边界。源码回滚不修复已保存生产状态。实机全部USER_GAME_TEST_REQUIRED。

部署：source `582a1e7`；只读进程确认游戏退出，既有工具完成B117恢复点→稳定桥→B118，158/158 MATCH；receipt `B118.145-582a1e7-playtest.json`，DEVELOP_ACTIVE。未启动游戏，main未改。


## 23. B118 screenshot ambiguity and timed dummy completion proposal

2026-09-28 [五图结果](../../Status/Validation/Results/Specialization_B118_Exact_Progress_Inconclusive.md)：即时7→7是缓存，后续Read过滤零和未变化项，无法区分最终归零与未变；工期119180→119181只是更新线索。NATIVE_RESULT_INCONCLUSIVE，不宣布FAIL/PASS。hover仍提−1000是旧说明，实际B118为−p，须在下一获授权修复中一并处理。本轮无代码/部署。

用户方案：高成本无收益dummy承接旧overflow、正常产能和chop/harvest，满足完整生产回合后强制完成，独立发奖。此方向技术上有候选组成，并不因负数实验问题被否决：B118已有无收益高成本项目；本机Cheat_Menu_Panel_Script.lua:68–74存在BuildQueue:FinishProgress()调用。该先例只确认可调用的完成路径，未证明其如何处理投入、隐藏存储、完成余量、自动下一队列或事件顺序。不能先拿到奖励再补生产漏洞。

建议验证顺序：先专用无收益项目有进度→单次FinishProgress→确认完成、切0进度目标、下一正常回合检查余量/负债；同时修报告为“即时样本/当前读数”分开，明确显示当前目标、进度0或负数。先不发奖。通过后才验证正常回合结束时机、chop/harvest及重复/中断/存读。正式奖励需独立记录启动时点与连续占用，并在合格结束时恰好一次；不能任意原生CityProjectCompleted都给奖，否则Cheat或极大注入可能提前触发。

有限高Cost不等于不能提前完成。须检测意外原生完成，并拒绝把它当合格计时完成；但是这只能保护奖励，不能自动保护溢出。没有确认完整生产结算事件之前，不把PlayerTurnDeactivated/首个PlayerTurnStarted直接当安全结束点；B116观察窗口局限继续适用。

显示1回合：本机Base CitySupport.lua:269–304对项目读取GetTurnsLeft/进度/成本并返回Turns、百分比；HD DL_ProductionPanel.lua:600同样为项目读取GetTurnsLeft。因此可以在UI仅对本项目覆盖预计时间文本为“1回合／本回合结束时完成”，而不修改真实Cost或全局GetTurnsLeft。但这是UI prototype方向，不是已验证hook；生产列表、当前城市面板、队列/Tooltip和HD替换页须一致，进度条应表达计时而非百万成本。显示修改不能使引擎本身按1回合结算。中断或尚未进入计时状态时，不能无条件显示即将完成。

当前建议由“继续扣锤”转向上述无奖励FinishProgress最小可行性门禁，等待用户明确实施授权；不擅自将讨论变为新Design或强制完成实现。旧全清与占用期隔离合同保持，无需本轮重复游戏测试。


## 24. B119.146 — standalone native FinishProgress experiment

2026-09-28，用户明确提供Cheat Panel完成项目不产生溢出的既有观察，并要求确认独立实现后授权原型。只读核对Workshop1528155583的CheatMenuPanel.modinfo把Base/UI/Script/Cheat_Menu_Panel_Script.lua注册为Gameplay script；该脚本68–74行CompleteProduction仅获取player/city/buildQueue、确认player、调用原生FinishProgress()，没有额外清池、进度补偿或自建overflow账本。B119在自己的Gameplay中直接调用q:FinishProgress()，不调用Cheat函数、UI、ExposedMembers或依赖该Mod。用户观察是有价值的先例，不扩展成任意项目/所有注入场景的原生保证。

### 已实施范围

保留B118无收益高Cost项目和两次确认/单城定域保护；允许已读进度0至10000（0可测试完成路径，但不证明正存量被吸收）。Gameplay当前目标、唯一队列、即时UI读数、owner/位置/回合、准备后生产事件和进度必须一致。锁存后一次FinishProgress，异常不重试，每城每次加载最多一次。没有AddProgress、奖励、计时完成或自动排队；不会完成普通建筑/单位/其它项目。本批仍不改显示1回合，因为计时规则尚未实施。

诊断改为“完成承接试验”：左键准备，再左键原生完成；右键每次重读当前回合/城市/队列、目标名称及进度（包括0/负值）、实验项目保留进度；另列相对准备时其它目标变化。调用记录与当前读数分栏，不缓存即时读数作为当前结论，不把0或未变化项隐藏。未知目标/缺接口明确报不可确认。旧−1000 tooltip与扣除文案已移除。仍是显式操作的一城有界读取，无hover/每帧扫描。

### 本地证据及最小用户测试

79项定向LOCAL_SIMULATION_PASS（53项直接旧计时观察器回归＋26项完成/保护/显示检查）；Lua/modinfo146的158文件STATIC_CONFIRMED。涵盖实际P0Panel/Gameplay入口、没有Cheat符号仍可调用、仅FinishProgress无AddProgress、0值和负值显示、延迟引擎更新后重新读取、未变正数不省略、完成返回但模拟残留仍不报nativePASS、重复/异常/错误目标/延后请求/事件变化保护。没有运行无关全回归或stress。原生完成及无残留仍USER_GAME_TEST_REQUIRED；不要求玩家卸载其它Mod破坏存档，仅本Mod不引用它们。

1. 使用实验前正常存档（避开B117负进度档）；保持自动溢出A。选择“溢出承接实验（无收益）”为唯一队列目标。不要使用Cheat完成。右键“完成承接试验”截图；最好已有正进度，否则正常生产一回合再准备。
2. 左键准备，再左键原生完成一次。稍候右键刷新截图：当前应无生产目标/队列0；实验项目保留进度读数如实记录，不以该值单独决定是否存在城市存量。若仍显示实验项目，可再右键读取（不重复左键）；未知/错误/意外完成其它目标立即停止。
3. 同回合选择此前0进度的普通目标Q，右键截图：当前目标Q、进度应0。正常生产一回合后再右键截图，Q应正常增长，无额外正溢出或负债。若进度异常，停止，不自行补生产。

这是手动FinishProgress primitive；不要求自动按一回合完成或显示1T。门禁通过后才考虑chop/harvest、结算事件、提前完成、一次性奖励、中断/存读和专项目计时UI。无新正式Design，Claim/F未推进。

B119部署：source b3667b2，进程确认游戏退出，B118恢复点与稳定桥保留；158/158 MATCH，receipt B119.146-b3667b2-playtest.json，DEVELOP_ACTIVE。未启动游戏或修改main。

### B119 native acceptance — scoped manual completion PASS

2026-09-28 [四图及用户陈述](../../Status/Validation/Results/Specialization_B119_Native_Finish_Pass.md)：项目7→原生完成→队列空/保留进度0/其它目标未变→同回合纪念碑0/50；下一回合正常由用户明确确认，无截图。此最小路径USER_GAME_TEST_PASS；不追认B118扣除，不扩大chop/harvest、任意存量、自动时序或重载。高回合显示尚未改，仍由高成本估算，符合B119范围。下一建议为完整回合定时＋专项目显示1T的窄计划；先明确结算顺序与提前完成/注入门禁，不自动实现。

## 25. Post-B119 plan — full-turn lifecycle and truthful one-turn presentation

2026-09-28；用户仅授权提供计划。本文不是实现授权。复用B119手动FinishProgress限定PASS，不重做无争议primitive；本轮无源码/部署。采用两段窄范围门禁，避免一边猜结算顺序、一边将“1回合”显示写成已成立事实。

### 目标及共享边界

目标是玩家选择无收益dummy后，它占用本城一个完整正常生产周期；该周期全部结算到dummy，完成后下一次可操作时释放生产位。下一目标不继承本次承接的存储/投入。最终UI仅对此项目显示“1回合／本轮生产结算后完成”。本阶段仍不发奖励、不接时代对话、Claim或其它正式能力，不改Design。Cost保持实验保护值，不宣称无限容量。

一个完整回合不是现实计时、不是从点击起等24小时，也不是仅GameTurn加1。开始前该回合已为其它项目正常结算的生产不倒扣。开始后的连续占用覆盖下一次该城正常生产结算；中途换目标则本次中断，切回重新开始。队列后排项目不视为已启动；只跟踪选定实验城当前唯一dummy。自动完成后的自身事件不再次视为玩家中断或重复完成。

### P-B120A — 单城生产结算顺序证据（建议先授权这一段）

目的：填补B116在首个PlayerTurnStarted停止的采样窗口，不新增生产写入。复用既有计时观察入口但明确“dummy结算观察”，与旧NONE/回合按钮豁免隔离；dummy是实际生产目标，正常下一回合按钮应自然可用，不再调用强制过回合路径。

- 对当前选定己方测试城、当前唯一dummy显式开启一次session观察，记录owner/city/位置、起始回合、目标和准确项目进度。
- 只监听该城ProductionChanged/QueueChanged/Updated/Completed及本玩家Deactivated、Started、Activated、GameEvents.PlayerTurnStartComplete。最后一个在本机HD ResourceCost.lua:69与另一Mod OverflowBugFixGameplay.lua:93有使用先例；仅STATIC候选，名称不证明结算已完。
- 不在首次Started停止；按事件顺序记录Gameplay目标与可获得的UI确认样本，区别事件即时/稍后缓存读数。共享读数桥不可用或UI尚旧时明确UNKNOWN，不能补造“0”。相关事件只追加有限样本；达到容量或观察跨过一个完整目标周期仍无法判断，停止并报告，不悄悄丢弃。无计时轮询、无全城扫描、无每帧采样。
- 用户在下一次能够操作时点击一次只读“结束观察/报告”，记录终点；不是依赖该点击自动完成项目。这个观察完整窗口用于判断候选时点前后是否仍有生产结算，并记录实际发生的顺序，不以事件名/单次进度变化直接宣布通用保证。
- 正常进度增长帮助识别结算，不成为未来完成资格：零生产城市也应按完整周期完成。无法区分的零产能案例暂列边界，不能以等待到p>0改Gameplay。
- 切目标/换Owner/城市移除/提前完成/接口不明立即中断；反复选回不能续算。重复通知只记录，不发任何完成调用。本段session-only，重载视为观察结束，重新开始实验；不写存档schema、不保证自动恢复。

可能修改：TimedProductionProbe.lua及现有诊断入口/读模型、小量直接测试；不改生产数据库、收益writer、B119手动完成实现或回合按钮豁免合同。验证L3但仅定向：事件次序变体、重复、无事件、UNKNOWN、同回合切出切回、其它城/owner、限额停止、重载初始化。用户最小流程：一城dummy开启→正常结束回合→恢复操作后只读报告，一组截图；无手动强制过回合、无Cheat。

退出：得到明确的候选结算末端及其局限；若仍不能确认，记EVENT_ORDER_BOUNDARY，只收窄调查，不自动进入B。回滚仅该诊断源码，无持久状态迁移。

### P-B120B — 定时自动完成＋1回合呈现（依赖A，另行授权）

A证据审阅后，选用经过核对的候选末端，不能在此计划预先指定Started/StartComplete必然安全。计划结构：显式启动→ACTIVE→周期完成候选→重新检查owner/城/当前dummy/连续性→先锁存COMPLETING→一次原生FinishProgress→确认项目退出→DONE。重复事件不得再调用；异常/未知进入STOPPED，不尝试补锤或完成普通目标。记录原始起点，UI重开不能重置周期。

仅一城、无奖励实验。若事件到达顺序与A不同、玩家已能对目标执行新动作、观察窗口仍有晚到产能等，停止该自动路径，不能把失败变成“再等一回合”。跨回合UI缓存不能作为唯一完成权威。零生产仍依据被验证的周期边界；边界不可证明则拒绝自动完成并报告限制，不偷偷改变资格。session-only原型重载会显示未激活，玩家重新开始；正式持久化恢复另列后续门禁，不声称可交付存档合同。

显示只覆盖本项目：未启动“需开启计时实验”；ACTIVE“1回合／本轮生产结算后完成”；STOPPED给具体原因；DONE释放生产位。生产列表、当前城市面板、队列/tooltip按实际原版/HD入口核对，不能全局改GetTurnsLeft。生产百分比不再用百万成本表达计时；不触碰其它项目的工期。开始入口可先沿用显式诊断按钮，尚不自动拦截所有Project点击；正式玩家入口留后续接入。

可能修改：定域计时模块、B119原生完成调用保护、P0Panel；当前项目UI数据适配（Base CitySupport与HD ProductionPanel路径先做最小hook核对，不先承诺复制整个UI）。不得为显示效果把真实Cost改成1。按钮/页面未能一致拦截则标UI_PROTOTYPE_BOUNDARY，不向玩家假称所有页面已显示1T。

本地验证：A事件重放、完成一次性、不同目标不完成、中断、重载停止、UI0/负/未知、迟到通知、不产生奖励；相关旧观察/完成回归，原版/HD显示只对本项目变化。用户一次正常流程：开dummy计时→看1T→正常过回合自动释放→选原0目标应0→正常增长；另从实验前档验证一次切走再切回必须重启，不与正常分支混用。

### 生产注入与后续门禁

A不混入chop/harvest，以免无法区分正常结算。B正常周期通过后，在同一个prototype、独立实验前档分支验证一次chop与一次Bonus Resource harvest：投入dummy、不得提早有效完成、计时完成后Q为0且下一正常回合增长。无需先实现奖励。未覆盖前不能宣布“所有生产隔离PASS”。

有限Cost被超量注入提前完成属于明确停止边界：停止计时，不发奖，不自动重建/连发项目，不修复其它目标；若产能已经外溢则整条隔离门禁FAIL。不得把高Cost当设计上的绝对上限。用户可使用Cheat构造压力对照但不要求安装它；正常chop/harvest证据独立。取消时已承接进度如何最终清理、存读恢复、完整参数范围以及正式能力奖励的一次性/时代quota仍后置，不能通过原型偷偷冻结。

### 完成判断

B119既有PASS保持。A解决“在什么时候完成”；B验证“自动完成且显示准确”；注入分支验证“生产不会逃逸”。三者不是一项PASS。正式一回合能力接入前仍需补中断/存读/大额早完成边界及相关Design合同同步。本计划无新的Gameplay决定请求；只有技术事实不成立才回报，不以技术方便改规则。下一允许动作仅等待用户授权P-B120A，不自动实施B或发奖。
