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
