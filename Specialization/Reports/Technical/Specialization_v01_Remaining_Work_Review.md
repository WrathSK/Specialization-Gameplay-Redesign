# v0.1 剩余工作盘点与方案研究

> 交接取代说明：本文是D0013时的研究盘点，不是当前状态。Research/Industry固定复制已部署B051.67；其余工作及唯一顺序见Status。原“当前仅研究/恢复需指示”为当时约束。

Document Owner: Codex
Design reviewed: D0013 ACCEPTED
Runtime reviewed: P0-B-050 / modinfo64
Mode: RESEARCH_ONLY — no source/test/runtime changes

## 结论

当前是四专业Lv1–3主要Local机制可测试、部分Lv4已实现的开发版。独立测试文明、首次完成专业记录、移民永久投资、总督ACTIVE门控、工作专家、基础相邻、后台当前商路与分发、Crew五项目/单位及基本动作已推进并有按场景用户证据。不能把各种探针或离线模型一并算成正式玩法。

以下分为9个剩余机制工作包与3个集成工作包，作为排程单元而非等工作量或完成百分比；Future不计入。当前不部署任何一项，也不新派测试。

## 九个机制工作包

| 工作包 / Design | 当前证据 | 建议路线 | 未完成/限制 |
|---|---|---|---|
| 1 Research IV非学院复制 RES-004 | B049实际区域基数读取通过，B050半点实验通过 | 后台读取完整合格区域集；Gameplay重核城市/ACTIVE；按绝对目标金额替换专用city层收益 | 自动采样、动态撤销、合格区域范围、非半点值；诊断点击不得成为正式必需步骤 |
| 2 Industry IV网络输出 IND-004 | 当前来源/max/撤销只读通过 | 当前recipient对应有效IV源；各取IZ基数50%，按金额max；不把模板/折扣合并进同一L | 半点承载可继续集成但未实现；跨城发放/移除、人口重算、反馈隔离待接 |
| 3 标准化永久账本 IND-NET-004 | HD Tier目录STATIC_CONFIRMED，离线账本LOCAL_SIMULATION_PASS；D0013学习规则已确认 | 城市永久Property+首次Industry初始化标记+事件增量，来源并集现算 | 真正持久写入、学习事件/城市身份、允许清单；不得继续把学习触发与首次补录列未决 |
| 4 Gold-only建筑购买折扣 IND-NET-001..003 | 离线模板并集/最大折扣通过；原生建筑购买Effect先例 | 按当前有效来源派生每目标BuildingType折扣，模板提供者与最大等级可不同源 | 原生货币隔离及与已有折扣叠加需调查/测试，不能退款替代或放宽购买资格 |
| 5 Research Network Inspiration | sqrt/Lmax/N去重仅有离线模型，实际网络拓扑已可读 | 独立k_R；在触发前准备有效强度；研究原生modifier与精确目标进度方案 | 小数百分点、封顶、已触发不补发、无溢出、批量触发时序；尚无正式Boost |
| 6 Culture Network Eureka | 同上，对应独立k_C | 与5共用计算/事件契约，分别对科技/市政测试 | 不能复用城市半点收益接口当成Boost精度已解决，不回退线性或逐中心sum |
| 7 Culture IV Great Work基础相邻 GW-002 | 既有BASE读取；作品计数未有当前正式模块 | 当前城市slot/作品实例快照×本城合格专业区域BASE六yield，独立city层补贴 | 作品移动/交易/征服刷新、作品分类/区域范围、Tourism与theming影响未解决 |
| 8 Culture IV时代保值 GW-001 | WHAT含TBD，无运行补贴 | 单独策略模块：作品类型/原时代基准对照当前时代曲线，补非负差值 | 时代口径、类别曲线/缺失标准、Tourism与作品专属倍率需DESIGN_DECISION_REQUIRED，不能用帝国最高作品替代 |
| 9 Commerce IV Convergence COM-004..008 | 本地多源20%候选与city总量读取；无运行汇聚 | 每种direct source分别选本地自产最高；单独标记跨城输入与对应实际影响，先解决计算依赖再给收益 | 纯本地basis/百分比叠加/20%精度/反馈环；用户允许困难时总量备选是有条件授权，尚未采用 |

## 三个集成工作包

1. **通用参与资格与城市生命周期。** Design ELIG是通用player资格，当前Probe.IsTestPlayer仍固定测试文明/领袖，EffectiveFacts也依赖它。已有资格研究与离线契约不等于全局实现。先保留测试载体，未来将消费者统一接资格读取；不把多玩家/多人成功当已证。
2. **征服/继承/无Identity Claim。** D0010的已有Identity继承、非空LegacySet一次snapshot+Claim、空LegacySet普通首次完成三分支尚未形成完整原生流程。EffectiveFacts当前投资anchor含owner且严格相等，直接换owner会冲突，不能宣称征服已支持。计划拆稳定cityUID/当前owner，原件投资与模板保留，临时ACTIVE/network重建；Claim成本仍需设计确定，不推断自由赠送。
3. **玩家界面、正式运行边界与回归。** DEV读数不是最终专业/网络信息入口；需可见Identity/Potential/ACTIVE/收益/网络来源与模板详情，正常提示、实验开关隔离、旧存档支持范围、mod加载与已知原生UI延迟说明。现成按钮可用不表示完整呈现已完成。极端故障不抢占Cheat正常机制测试优先级。

## 进一步本机研究与含义

### 标准化：一次初始化 + 有效事件增量

HD Gameplay/RegionalYields.lua:256使用Events.BuildingAddedToMap(x,y,buildingId,playerId,...)标记需更新；这给出本机事件先例，**不证明它覆盖所有购买/免费获得情况**。运行既有GameEvents.OnBuildingConstructed可作另一入口。未来两者归一成“目标城市的指定建筑发生获得通知”，读取当前HasBuilding、owner、Industry身份、HD Tier和允许清单复核；通知不直接当事实。

首次Industry转换时只扫描一次本城已有建筑，保存初始化版本/完成标记；加载恢复仅检查标记与未完成的该次事务，不重新扫描每座城市。期间并发通知放入本城待处理集，完成后按BuildingType去重，防止初始扫描/事件重复记模板。后续只查询事件指向建筑，必要时延迟到安全阶段复核同一个目标，不持续扫描全国/全城。

模板Property原件以稳定城市身份保存，learned记录具体BuildingType与取得时分类版本。有效网络模板并集是派生缓存，不永久全国解锁。已Industry旧存档无新标记时需要明确一次迁移如何接续“首次Industry初始化”，不借迁移变成持续扫描；这属于部署边界，不再质疑用户已批准的既存建筑补录方向。允许清单具体内容尚未由“HD能分类”自动决定，特别不能将市中心Tier0全并成组。

### B050后的收益适配

B050两种组合提供了新的实机支持，推荐作为下一次实现起点：将绝对目标分成整数部分与半点余数，整数原生载体+半点组合各自可撤销；仅当目标确实在这个数域才可使用。人口变化要在对应城市重新计算补偿；load从当前事实重建。目标为0.25/0.1等时不能截断，仍保留技术限制并研究更细系数。若继续扩展二进制小数，也要评估原生数值粒度，B050不是任意分母精度承诺。

在正式网络代码之外制定收益输入记录，供Commerce过滤。仅“先读所有城市再写”不能防跨回合反馈；即使每次绝对覆盖，反馈公式仍可能逐回合膨胀。原生城市倍率下直接减配置输入可能错误（100本地+20输入再×1.5，最终180减20不是本地150），需验证真实受影响层。不得为了去环静默削弱合法来源。

### Boost原生事件与Great Work数据

HD Gameplay/Misc.lua:536–537注册CivicBoostTriggered/TechBoostTriggered；Wonders.lua:386–404的NotreDame例子读取被触发市政GetCultureCost，然后发Great Musician点数。它证明能获得触发目标，不证明能安全改该目标进度或自动限制overflow。不能把ChangeCurrentCulturalProgress当成对刚触发市政的定向补足：当前研究可能是另一个项目。下一步应研究被触发目标/当前研究/完成后的事件顺序，不凭相同名称拼接口。

HD UI/Additions/HD_Utils.lua:1176的GetCityGreatWorks遍历城市地块→建筑→slot，以GetGreatWorkInSlot得到实例index，再转type并按GreatWorkObjectType筛选。Gameplay/Governors.lua:42使用它统计类型/时代，是现成桥接/调用链线索。原helper最终只返回作品type，不能直接用来区分重复类型作品或记录移动；本项目应保留实例index+slot+city快照，再验证上下文可用性。Product、宗教题材艺术、Relic必须分别分类；后两者不是同类概念。

## 建议恢复实现后的顺序（本轮不执行）

A. Research/Industry 50%正式承载与后台刷新，共用一次验证；先能证明不丢半点、无重复、撤销正确。
B. 标准化一次初始化与事件增量，然后独立Gold/Faith价差检查；原生折扣不确定不阻止先保存合法永久成果。
C. Research/Culture Boost计算/触发/精度；封顶与量化决策集中讨论，不把B050结果外推。
D. Great Work计数/搬移/base补贴；时代曲线与倍率设计明确后再接保值。
E. Commerce IV纯本地产出/跨城输入隔离与20%承载，重点正常直接来源和撤销，随后跨回合反馈。
F. 通用资格/征服/Claim和正式信息界面，根据用户可玩目标穿插集成，不重做已通过的所有基础探针。

Future辅助区（包括Spaceport、Entertainment等）不进入本清单。Government titles规则已确认但属于Future，不误算为当前v0.1欠缺。旧B010探针继续待办，不作为当前后台网络实现未通过的替代结论。

## 文件与验证保护

本轮仅新研究报告/Design确认同步/结果/截图归档。运行B050/modinfo64不变，源码和DevelopmentTests前后SHA256核对；未运行实现测试、未新增SQL/Lua、未启动游戏。静态源码先例记STATIC_CONFIRMED，不等于新增游戏通过；唯一新增USER_GAME_TEST_PASS来自用户B050回报及五图。
