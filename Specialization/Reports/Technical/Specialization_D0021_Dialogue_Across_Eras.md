# D0021：时代对话原生路径调查

Document Owner: Codex
Design: Accepted D0021
Runtime: B058.76 / modinfo76（本轮不修改/部署）

## 设计及旧路线退出

规则唯一权威位置为Spec GW-001/003。旧D0020最高基础值/逐件不同差额算法与强制倍率恢复不再开发。当前代码GreatWorkBasis为旧只读探针，冻结为阶段记录；下一实现替换显示，不再派旧测试。本轮没有改源码、UUID或任何游戏配置。

## Era来源（STATIC_CONFIRMED，不是新实机PASS）

对城市每个slot取GetGreatWorkInSlot，GetGreatWorkTypeFromIndex映射GameInfo.GreatWorks[workType].EraType。原版Base/Assets/UI/GreatWorksOverview.lua:558–568读取该行并展示带时代的作品类型；:347、607用EraType比较文物主题化。因此优先采用数据库作品时代标签。

当前只读DebugGameplay：ARTIFACT25、LANDSCAPE40、MUSIC80、PORTRAIT28、RELIGIOUS18、SCULPTURE27、WRITING93，共311种合格类型，EraType无缺失。Relic24/Product966缺Era且本来排除，不计D。HD会调整作品EraType，这是当前mod组合的作品定义；不以原版静态缓存覆盖。文物的标签是文物所归属历史时代，不是玩家挖掘时的时代；著作/艺术也不是玩家实际点击激活伟人的回合或当前时代。GreatPersonIndividuals的时代属于伟人条目，不能替代已有GreatWork.EraType。

缺失Era的未来作品不擅自记为“未知时代”或玩家时代；将本次采样标为不完整并报告，不能悄悄改变D定义。作品move/卖出/城市归属变化后重新从当前集合重算，不保留曾经最大D；ACTIVE条件仍由CultureIV门控。

## Culture统一加成

MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD：GreatWorkObjectType、YieldType=YIELD_CULTURE、YieldChange=bonus，对七类分别挂同值。B055原生+2C著作已验证；这只支持该场景，未证明所有类别/theming。D由全城合格作品去重后统一计算，不逐类别各算D。D≤1撤销载体，重复刷新幂等，移动最后一件某时代作品应降档。

## Tourism固定追加仍需验证

HD赵孟頫/市场/古罗马剧场等MODIFIER_SINGLE_CITY_ADJUST_TOURISM先例以GreatWorkObjectType+ScalingFactor作用，属于百分比放大，不能写ScalingFactor=bonus来实现固定+bonus。当前Yields中无YIELD_TOURISM，不能假设GreatWork YieldChange可直接传它。

另有原生EFFECT_ADJUST_DISTRICT_TOURISM_CHANGE及MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE，现有Argument Amount=1/2/3等为固定区域旅游候选。可考虑限定本城City Center这唯一目标，Amount=合格作品数×bonus，作为独立旅游追加。它不伪装成作品intrinsic yield，可能不吃作品theming；D0021已允许报告这种自然行为。此路线仍需核对唯一目标/旅游面板实际入口与倍率，不能凭SQL声明成功。不恢复逐件倍率反推。

## 最小原生验证计划（尚无新按钮，本轮无需执行）

1. 非主题化CultureIV城、固定收藏和专家/宜居度，至少两时代：OFF/ON比较作品文化、城市文化、城市旅游总量；同时记录作品数和D。若4件跨2时代，原始增量各4；城市文化倍率由报告同时显示后核算。
2. 同一份已主题化收藏，保持D/作品数不变，仅切同一bonus OFF/ON：比作品文化/旅游与城市旅游总量，判断统一加成是否被主题化放大。不能用“换了一批作品、D也变化”的前后对比推断theming；若目前无主题化收藏，不强求新局，该项保留后验。

旅游若落在City Center来源，作品栏可能不增加而城市/帝国旅游增加，必须记录来源而非只看作品栏判失败。自然吃theming则保留；不吃则报告，不新增复杂模拟。先验证统一bonus基本生效，再复用同收藏主题化对照，最少两组。

## 本轮检查

Design/ChangeLog/Architecture/Status同步与D0020冻结hash；只读SQL查询/source inspection；公式例子D=0/1/2/3/6→0/0/1/2/5，12件D6→60。这是静态算术，不冒充运行Lua测试。未新增运行机制、未启动游戏或commit/push。统一Culture/Tourism/theming综合效果仍USER_GAME_TEST_REQUIRED。
