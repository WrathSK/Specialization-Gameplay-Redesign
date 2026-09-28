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
