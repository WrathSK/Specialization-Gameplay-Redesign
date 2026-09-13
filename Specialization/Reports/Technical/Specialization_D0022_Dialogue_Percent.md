# D0022：时代对话百分比与creator era

Document Owner: Codex
Accepted Design: D0022
Runtime: B058.76 / modinfo76 unchanged

## 当前契约

Spec GW-001/003唯一权威。百分比15×max(0,D−1)，Culture/Tourism统一；不额外cap，D7非最大值。固定yield、固定旅游追加、逐件最高值补差全部退出，不继续开发。件数只决定受益对象数量，不进入百分比。

## Creator era静态核对

当前DebugGameplay只读关联GreatWorks.GreatPersonIndividualType→GreatPersonIndividuals.EraType：286种非文物合格作品均有Era；25种文物无伟人关联。28种著作的作品Era与伟人Era不同，其它合格类型目前相同。例GREATWORK_HANFEI作品ERA_CLASSICAL、关联伟人ERA_ANCIENT；GREATWORK_YUE_SHU_YAO_LU作品ERA_MEDIEVAL、关联伟人ERA_ANCIENT。因此D0021把作品Era一律用于统计不符合本轮新定义。

按用户另行明确回答，仅Artifact使用其自身GreatWorks.EraType作为历史时代例外，其它按关联伟人EraType；时代键统一去重，文物与伟人同ERA只计一次。不是招募/创作操作发生的当前时代，也不是建筑/城市时代。

原版GreatWorksOverview.lua:558使用GetCreatorNameFromIndex显示实例creator名称，但未在本次查找到可靠的实例creator ID→Era直接API先例。数据关联是当前明确可用来源；特殊脚本若生成与关联元数据不同的创作者，报告异常，不从本地化姓名或当前时代猜测。HD可以修改关联/时代，运行时应使用实际GameInfo，不写死原版表。

## Modifier映射（STATIC_CONFIRMED，不代表新实机PASS）

Culture：MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD，GreatWorkObjectType=对应合格类型、YieldType=YIELD_CULTURE、ScalingFactor=100+BonusPercent。当前DB有CATHEDRAL_*_CULTURE_BONUS的ScalingFactor125及EL_ESCORIAL_PALACE等150先例。

Tourism：MODIFIER_SINGLE_CITY_ADJUST_TOURISM，GreatWorkObjectType=对应类型、ScalingFactor=100+BonusPercent；HD赵孟頫、古罗马剧场等有150倍率先例。D=2/3/6对应115/130/175；D≤1不挂加成。不给YieldChange固定值，不用YIELD_TOURISM，不写全帝国普通Culture/Tourism百分比。每城七个合格类型统一档位，不因该类几件作品重复附着相同Modifier。

同城已有相同类别Modifier与theming的叠加/结算顺序仍需实际比较，不凭参数名推断所有层都相乘或相加。采用原生自然结果，不为旧保值方案补偿。未来工程目录容量不能偷偷变成玩法cap。

## 最小实机计划（实现后再发，目前无新操作）

1. CultureIV固定两创作者时代收藏，保持专家/宜居度及其它修正：OFF/ON，记录D=2、ScalingFactor115、作品Culture/Tourism和整城总值。不含其它作品倍率时预期对应基础提升15%；同一组作品切换，避免把作品换入本身收益当bonus。
2. 已主题化固定收藏、D不变，仅同一百分比OFF/ON。对照作品Culture/Tourism变化，判断theming与统一百分比叠加；报告原生差值，不重建逐件模型。若无可用主题化收藏，该项可后验，不为此强制新局。

原生浮点尾差与UI刷新延迟记录；不从旧Boost整数接口结论推导GreatWork百分比精度。两项都需USER_GAME_TEST_REQUIRED，现有Culture平加实验不能覆盖百分比theming。

## 本轮校验

冻结D0021原文hash，D0022/ChangeLog/Architecture/Status/README同步；只读DB和原版/HD源码调查。无运行源码更改、未部署、未启动游戏、未commit/push。新能力尚未运行。
