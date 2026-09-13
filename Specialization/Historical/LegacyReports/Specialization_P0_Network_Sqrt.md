# Research / Culture Network：sqrt修订与效果适配边界

## 当前实现约定

Research→额外Inspiration百分点，Culture→额外Eureka百分点。`DeltaBoost=k×L×sqrt(N)`；k_R/k_C独立，初始各1；L为源ACTIVE level，不是potential。N是当前实际接受该类型网络的己方城市去重数。同一路线携带所有已接入网络规则不变，但路线数不参与强度公式。Commerce IV免费自接收也进入同一集合，与路线接收重叠只计一次。

当前没有可运行的网络结算。纯Lua prototype在DevelopmentTests/NetworkStrength.lua，未列入modinfo、未导入Gameplay。输入是已校验的接收城市UID列表与已解析的单个ACTIVE L；返回去重N及未取整networkStrength。它不识别所有权、路线有效性或选源，这些是后续拓扑层职责，不能把纯列表测试称为商路检测通过。

当前多源/多中心不同L如何合并未定义：旧逐中心求和已废弃，不自动取全国最高L、不相加sqrt强度。正式多源效果接线BLOCKED，待用户后续确定语义；本轮无需为此追加游戏测试。

## 本地技术证据

只读本机Cache/DebugGameplay.sqlite：ModifierArguments.Value为TEXT，Type默认为ARGTYPE_IDENTITY。DynamicModifiers表仅定义ModifierType/CollectionType/EffectType映射，其名字不能证明支持运行时动态数学表达式。

已对真实缓存的内存副本重写一个现有Boost Amount，分别存取0.5、11.313708498984761、sqrt(8)文本，均可原样保存。它只验证存储层接受字符串，**不能证明Boost效果支持浮点，更不能证明支持sqrt表达式**。实际缓存没有修改。

当前缓存中MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST / MODIFIER_PLAYER_ADJUST_CIVIC_BOOST的检查样本Amount是整数（如10、60、3、5、1）。和而不同UpdateDataBase/DL_Projects.sql:102、DL_Buildings.sql:1735等使用同类效果；Configs/HD_Configs.sql:13–14把科技/市政Boost默认设置为33。原生/Mod样本不提供本轮所需的动态小数精度证明，因此不硬编码基础40。

## 计划计算与应用

1. Gameplay拓扑层读取合法连接：构建connected sources、每类型recipient UID set，去重并保留接收资格来源。任一资格失效时仅移除该资格，仍有其他资格的城市保留。
2. 在ACTIVE L、接收集合或k变化时，Lua计算sqrt，保存可重建的浮点Network Strength；变化事件/加载后统一刷新，避免重复累计。显示格式和实际值分开。
3. BoostAdapter负责将强度映射到玩家全局的额外Inspiration/Eureka效果。在触发前完成门控刷新，已触发的boost不补发，断线不扣历史进度。
4. 首选调查预定义小数Amount效果＋可撤销条件门控：先测固定0.5/1.5是否有效，再决定动态表示。任意sqrt实数通常不能由有限预定义小数效果精确表达，需要精度规范或确认可靠运行时数值通道；当前没有证据可以直接传入无限精度动态Amount。
5. 若引擎效果只接受整数，向用户报告floor/round/ceil各自偏差和跳变点，取得规则后才实现。内部浮点仍保留；当前不选任何取整方式，不偷偷截断。若效果支持小数但需固定精度，也同样先报告并确认量化规范。
6. 若原生Boost路线不可行，再研究一次性额外进度注入；风险包括实际科技/市政成本与进度精度、触发事件先后、其他Mod重复补发、超额流向下一项。此方案不等价于直接修改Boost效果，不能未经验证就替换。

sqrt计算本身LOCAL_SIMULATION_PASS；引擎Boost效果、可撤销动态映射、多人确定性都仍未确认。浮点比较以后需明确稳定精度/变化阈值，不能因为显示四舍五入就更改真实强度。也不静默限制N来迁就预定义Modifier数量。

## 测试计划调整

当前B004只调查Gameplay路线状态来源；不执行Boost测试，Governor/Spec已通过，不重复。

后续Network P0先验证原始端点→合法recipient及去重，再用单源样例对照N=0/1/8/16、重复路线、Commerce IV与路线重叠、删除一种资格后仍有接收资格、失去最后资格清除、ACTIVE变化。Research与Culture可拥有不同N，必须各自显示。

再单独安排精度小批探针：控制同一未触发目标的成本和前置进度，分别以基线0、固定0.5、固定1.5额外百分点触发同一条件，对比实际新增进度；先选择足够高成本目标，避免生产/研究进度本身整数化掩盖小数效果。探针直接显示cost/progress/delta，不让用户算差值。需要同一触发前存档分支，不能对已触发目标反复测。撤销及再次启用另案验证，不能累计叠加。当前只设计顺序，尚未提供可执行效果按钮。

在确认数值表达路径后，才验证Culture IV N=16额外16pp、N=8约11.313708499pp。若只能量化，则成功判据必须使用用户确认后的量化规则；尚无规则时不能生成伪PASS。其他Boost相加、超过100、同回合接收变化/触发和已完成目标仍需要测试；sqrt递减不等于硬封顶。

P1预留职责：RecipientProvider / RecipientSet / StrengthCalculator / BoostAdapter分开，保存永久事实，派生网络与强度加载后重建。不实现全网络或卫星。当前B004未接入Boost或正式网络；原型均仅在DevelopmentTests中运行。

## Future auxiliary design：Spaceport / Entertainment

Spaceport仅架构记录，不是专业区域。玩家完成Launch Earth Satellite后，仅己方拥有Spaceport的城市双向自动联网：自身专业作为直接源自动接入Trade Center；自身自动接收Trade Center当前所有已接入网络。无需分发商路，不占Trade Route Capacity，绝不是帝国全城自动接入。它只减少终局微操，不直接添加飞天生产、科技、生产或激光站效率。

未来Spaceport provider和实际路线/Commerce IV接收资格共用去重集合。未建成/掠夺/易主等细节未来另行定义。当前不注册卫星事件，不添加Spaceport机制。

Entertainment Regional Support未来调整k或最终Strength效率参数，不给effective level+1，也不恢复线性per-route百分点。两个future系统不进入本次v0.1实现范围。
