# B033：实际移民投资入口（限定测试文明）

Document Owner: Codex
Build: P0-B-033 / modinfo41
Design: D0009 / PROG-002, PROG-003 unchanged
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 实际行为

新增InvestmentAction.lua注册Gameplay模块；面板Prepare investment读取选中移民所在市中心，向既有SPC_P0_Request发送INVEST_PREPARE，返回目标、等级和单位ID。Prepare不写Property，不消耗；Confirm investment发送保存的PlanToken，由Gameplay对相同玩家/城市/当前回合/基础anchor/账本/等级/单位类型及位置重新检查。只允许现有测试文明、已跟踪专业城、标准UNIT_SETTLER；首版仅支持市中心操作，非永久设计限制。不要求总督建立、满血或移动力，不复制HD专属条件。

一个确认请求内：写INTENT并读回→给同单位写独立保留标记并读回→GetUnits():Destroy(unit)→FindID确认单位消失→写CONSUMED_CONFIRMED并读回→同表追加投资凭据、revision+1并清pending。账本由EffectiveFacts校验；总Potential=基础1+已完成凭据数，最多4。B015/B020原记录完全不写，不单独持久化ACTIVE。请求与单位标记含城市token/下一投资序号，避免同回合读档后UI序号重用碰撞。已完成凭据重放直接返回，不重复消耗；UI在单位消失后预览清空，再确认会提示重新准备。

单位删除事件清除对应预览，避免删除后数值ID复用继续旧预览；同回合预览限定及消耗前的当前状态复验不等于跨征服永久单位身份。玩家/城市永久身份仍沿用限定DEV token，未实现通用征服继承。

## 恢复与安全边界

正常DONE读档不写、不删单位。LoadScreenClose后，仅CONSUMED_CONFIRMED可验证当前城市及单位保留标记后补提交；INTENT绝不因为单位已不存在就自动补发。写入或消耗未确认时本玩家投资停止，保留现场；没有退款、没有自动再扣。删除后引擎FindID如果未立即更新，将返回UNIT_DEBIT_UNCONFIRMED并停下，需实机确定。此为正常单位API时序待验证，不以模拟冒充通过。

未确认操作仅影响投资入口；已完成投资事实/Lv1/拓扑继续经读入口检查，不发未完成投资收益。已消耗但未持久确认窗口仍可能需要人工处理，不宣称跨引擎单位/Property原子事务。初始存储写失败即停止，不先删单位。

## 集成

Gameplay新增两个action白名单和分发；InvestmentAction在EffectiveFacts之后、ResearchSupport之前初始化。EffectiveFacts只读输出更新为B033，pending增加原生unitID校验；没有新数据库定义。面板新增两个英文按钮，不覆盖HD UnitPanel，不使用HD默认自动删除框架。UUID保持，旧存档可加载，不必新局。未新增Lv2住房/GPP、Lv3–4或网络正式收益；ACTIVE仅显示已满足的等级。

## 验证

新增test_native_investment.py执行真实EffectiveFacts/InvestmentAction与原生形状mock，覆盖准备零写/零消耗、1→4、重复receipt、正常重载、cap/非移民/离城/回合变化/anchor变化/删除预览失效、INTENT/确认/最终写失败及确认后恢复只提交。实际P0Panel request函数测试选中单位→市中心→prepare/confirm参数；实际Gameplay request分发验证通过。全部Lua语法、XML ID/manifest引用及UUID/version41通过。

运行test_effective_facts.py旧回归时仅在内存适配version40→41及只读文案，旧测试文件不改。真实网络完整拓扑/撤销和Lv1新城/恢复/高Potential仍保留carrier回归通过。两组LOCAL_SIMULATION_PASS不是实机单位消耗或原生Property存档通过。故障fixture的RECOVERY_HELD打印是预期断言场景，不是本机游戏报错。

唯一[实机批次](../../Status/Validation/Cases/B033_Settler_Investment.md)：旧专业城1→2、重复确认不再扣、保存重载。只需一名移民；不重测原始总督接口。若本案失败停止扩展，回传截图/错误。小数与Commerce IV、B010继续暂停。
