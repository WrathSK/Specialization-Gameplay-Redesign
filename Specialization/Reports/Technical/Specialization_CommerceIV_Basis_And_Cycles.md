# Commerce IV：总产出条件备选与防反馈研究

Document Owner: Codex
Architecture Revision: A0061
Accepted Design: D0009（未改写）
Runtime: B027 / modinfo34（未改动）

## 本轮用户授权

用户要求继续研究；如果原有纯本地产出实现困难，允许不排除非本地产出、按实际产出计算，但必须防止递归循环。本报告按“被选择的科研/文化/工业来源城市实际总产出”理解，不改为商业接收城市自身总产出的20%。这是条件备选已获授权，不需再次请求研究许可；尚未确定精确应用与防反馈链路，本轮不将条件备选伪装成已完成D0009实现、不自动签发新Accepted Revision。正式采用时同步登记basis改变。

## 静态研究：STATIC_CONFIRMED

本机HD根目录：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070`。

| 路径 | 证据与边界 |
|---|---|
| Gameplay/Projects.lua:49 | Gameplay已有city:GetYield(YieldTypes.PRODUCTION)调用；证明源码先例，不等于本Mod S/C/P全数值/时点实测 |
| UI/Replacement/CitySupport.lua:316–332 | GetYield读取城市各yield，界面显示截断一位小数；计划直接读getter原值，不复制显示截断 |
| Gameplay/CityYield.lua:42–105 | 自建Property按sourceType记名义追加产出，通过AttachModifierByID应用差值；不是全城所有收益的来源分解 |
| UI/Replacement/CitySupport.lua:787–835 | 按账本重写tooltip分项；不能据此恢复百分比作用后的全部外来贡献 |
| UI/Replacement/RealModifierAnalysis.lua | BRS的Lua分析器手工按EffectType计算影响；如城市percent分支使用subject.Yields×Amount；不是引擎提供的精确反事实“剔除这些输入后的总产出”getter |
| UpdateDataBase/DL_City_Yield.sql | YIELD_CREATOR生成±1至50整数单城yield modifier；不能直接承载任意小数，不能默认把111.1变111 |

截至本次所查源码，没有找到可直接返回COM-006精确basis的原生分解接口。不是断言引擎不存在。为覆盖HD和其它机制手工重建全部yield及倍率，工程成本和漏算风险明显高于总产出getter；继续把精确剥离当作前置会拖延可玩版。建议优先验证用户已允许的总产出候选，原LOCAL接口保持可替换，不静默替代。

## 防循环：分清同轮更新和跨轮反馈

当前v0.1专业身份唯一（PROG-001），Convergence的source只能Research/Culture/Industry，target只能Commerce ACTIVE IV。故Convergence自身的复制边为 R/C/I→Commerce；Commerce的最终产出不是下一层Convergence合法source。即便双向商路存在，或另一个Commerce收到网络，也不得把它作为source。按直接来源和唯一身份过滤，阻断商业IV→商业IV的直接回路；中心角色不等于专业source身份。

采用绝对目标值（覆盖旧输出）而不是每刷新追加一次，且先读取所有source、再统一提交，避免重复更新和遍历顺序污染。但这些措施不能单独阻止跨轮经济反馈。反例两城各100、互相取对方20%：同步更新仍从120升至124再趋向125；这是重复复制，不能因为收敛就宣称无循环。

当前Industry IV仍按IZ区域Actual输出，不可改成工业城市总产出；Commerce汇聚计划加到city层，不能写进区域复制基数。这样可切断“工业源→商业→工业区域输出”的直接反馈通道，但其原生承载是否真的不进入district copy仍需实测，不能提前当成已证。其它Mod若把Commerce city yield返回上游source（通过特殊商路/百分比/复制），仍可能产生间接依赖；不能保证任意mod组合无环。

候选安全边界：只用真实直接R/C/I来源；旧输出由当前计划替换/撤销；专业/owner/ACTIVE变化时不能带着旧Commerce输出切换成source；观察到来源依赖Commerce输出时先定位回边，再决定隔离或采用精确扣除。不得默默截断合法收益或把阻断环路变成未获确认的新玩法限制。只读探针下一步应看S/C/P原值和来源身份；有真实city/district承载后再小批次验证反馈，不现在要求用户造复杂局。

## LOCAL_SIMULATION_PASS（非引擎）

新增纯离线ConvergencePlan.lua及test_convergence_plan.py，不载入modinfo。两个显式模式：LOCAL要求fixture已验证basis；TOTAL为条件备选。只输出浮点计划，不应用/取整。

验证逐yield最高而非最高ACTIVE、三类分别选择、20%保持小数、只收到distribution不能汇聚、Commerce不能作专业源、连续100次绝对更新不累加、来源移除回退/归零、owner和ACTIVE变化、无效/未验证basis拒绝，以及额外依赖成环时保守报UNKNOWN。依赖图由测试显式提供，不声称游戏已能完整检测未知Mod环路。无合适来源为0与读取失败UNKNOWN严格区分。

例：来源科研总2000（其中纯本地1700），TOTAL计划400，LOCAL计划340，明确表现玩法差异，不把两者称为等价。模拟中的双城反馈反例证明“先读后写”不是充分防环条件。

## 后续与当前边界

优先下一步：只读Getter原值/专业来源诊断，准备明确basis模式的应用接口；随后验证city层承载的精度、倍率及不反馈district copy。当前无新收益部署，不直接复用HD整数ChangeYield解决小数；不宣称20%最终可见增量已准确实现。用户无需重复B027，也不派新的实机批次。之前的可读性/断路测试继续延后。D0009原Spec不改，条件授权和需验证的差异在本报告与Status保持可追踪。
