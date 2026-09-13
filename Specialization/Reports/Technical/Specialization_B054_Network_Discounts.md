# B054 自动工业网络标准化折扣

Document Owner: Codex
Design: D0016 IND-NET-001..005
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED

## 运行流程

1. NetworkBridge.RecipientSources按当前后台全集、回合/信号/端点校验取得当前有效工业来源。NetworkBridge收到新批次通知StandardizationDiscount重新评估；不使用历史商路表。
2. EffectiveFacts给出每源ACTIVE；Standardization.ReadLedger是新增只读/克隆接口，复核原账本分类、位置、foundation，不写入。模板按D0015匹配组取并集；最高ACTIVE独立取max。没有模板即无对应候选，即使另一源等级高。失去有效源/无法可靠读取时清除旧收益而不删除永久账本。
3. SQL在HD目录加载后生成149种启用建筑×4档=596个内部载体（本机目录基准）；每个只挂载指定BuildingType的原生10/20/30/40购买成本Modifier。范围与Lua当前启用策略做测试交叉核对，原建筑、购买权限、Faith解锁均不修改。未启用/未知分类不生成载体，未来启用需显式更新策略/数据库。
4. UI/DiscountEligibility为空后台Context，无可见按钮依赖。仅对当前网络模板匹配候选调用原版ProductionPanel同一CityManager.CanStartCommand(city,PURCHASE,false,args,true)，args为building.Hash和Gold yieldIndex。原版另外调用CanAfford；本批不把钱包余额作为设计门槛，实际引擎是否在command check中还包含余额需保留观察边界。没有执行Purchase命令。
5. 后台发送generation/revision/seq/turn和完整逐候选布尔结果。游戏侧重新计算当前计划并复核完整性、重复、目标/owner，拒绝陈旧与部分样本；读档清空样本重建。不完整时不保持旧折扣。候选计划不依赖价格或载体，避免价格反馈成为网络事实。
6. 原生Gold资格通过的目标按当前等级附加恰好一个载体；先移除旧级别后加新级别。载体是可重建临时状态，永久模板不变。断网、降级、失去购买许可、易主非测试玩家均有清理；跨Owner专业继承仍为旧架构限制，不因本批实现清理就宣称继承完成。

## 货币与实验

采用B053已测原生指定建筑购买成本Effect，不猜YieldType参数、不退款、不改原生取整。D0016已允许隔离困难时同一合格建筑Faith价格同步享受折扣；并非全帝国Faith折扣或Faith-only建筑开放。用户只提供粮仓190，未给完整双币价格对，不推断精确算法。本批当前能否合法Gold购买仍由原生资格检查决定。

B053旧BASE/ON在当前面板隐藏，OFF保留，LoadScreenClose先清除旧实验再运行正式折扣。Read discounts只读计划、来源、配置，不刷新网络或挂载。后台身份/permission变化通过原生发布事件重新采样；如果效果改变在没有发布事件的路径延迟，实机结果再定位，不声明所有生命周期已通过。当前上限继承网络128路线/512城市，资格包60000字节；超限拒绝，不静默截断。

## 本地证据

`test_b054_discounts.py`内存SQLite执行真实新SQL（读取外部DB不写入），真实Catalog/Standardization/Discount/后台Lua组合，显式mock原生CanStartCommand：异源模板与最高级、BASIC组、禁用组、原生许可false、重复不累加、降级/断网撤销、资格消失、陈旧/部分样本、重载无需面板、来源owner冲突保留账本。测试中的Index/Hash映射是mock标识，不能替代引擎Hash验证；真实后台使用GameInfo.Hash。

不把mock价格/许可当实际引擎结果。Lua/XML、加载引用、面板位置和原有复制/账本回归另做检查。正式下一实机批次仅由Status链接派发。
