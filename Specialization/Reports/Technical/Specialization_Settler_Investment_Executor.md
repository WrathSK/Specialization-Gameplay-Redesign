# Settler永久投资执行层准备

Document Owner: Codex
Design Rules: PROG-002 / PROG-003
Runtime: B031 / modinfo39 unchanged
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS

## 本轮范围

小数承载/Commerce IV按用户要求继续后续研究。选择共同Potential成长前置，新增DevelopmentTests/SettlerInvestmentExecutor.lua与test_settler_investment_executor.py。模块仅通过注入的离线存储/单位接口执行，不注册游戏、不消耗真实移民、不新增高级收益。CitySpecializationState仍负责唯一离线规则校验，不复制另一套等级/消耗规则。

## 正常路径

读取同城事实→PlanInvestment校验专业/己方移民/资格/cap/旧凭据→同表写INTENT并读回确认→紧邻消耗前重新验证单位owner、代际和位置→消耗→确认单位不存在→同表写CONSUMED_CONFIRMED并读回→CommitInvestment生成新事实→一次写入事实与投资凭据，同时清除pending。已完成receipt重放直接返回，不重复写或删单位。最高Lv4；Governor门控不作为永久投资的消耗前提。

同一个pending时拒绝第二动作；同实例重入会停止。此处write/read不代表Civ6原生原子事务，只是注入接口约束，不能把同步读回等同磁盘存档成功。

## 恢复和支持边界

已完成状态读档只读；CONSUMED_CONFIRMED恢复核对身份及单位仍不存在，只补提交，不再删单位。仅有INTENT，即使单位已经不在，也不能证明由本操作消耗：停止，不自动补发或重扣。消耗后、确认记录落盘前的异常窗口保留为人工检查边界；不实现自动退款，也不声称所有故障都可恢复。正常Cheat路径优先，不让这些边界无限阻塞功能。

离线unitUID/cityUID是假设已验证的身份，原生owner+unitID不是已证明的永久代际标识。io.validate必须由后续引擎接入检查同单位/owner/位置；io.presence必须区分ABSENT与读取失败UNKNOWN。本轮不能把fixture身份用作游戏凭据。io.read/write须保存整张记录而非分别更新facts/pending；预先存在有效store是本执行层前提，创建/迁移不在该模块中。

## 静态源码先例与接入缺口

本机HD Gameplay/Misc.lua:674–681 HDDestroyUnit使用UnitManager.GetUnit(playerId,unitId)，然后Players[playerId]:GetUnits():Destroy(unit)，由GameEvents.HDDestroyUnit触发。Gameplay/UnitAbilities.lua:55–59在宗教单位耗尽次数时同样调用Destroy；Gameplay/CivilizationTraits.lua:2182使用GetUnits():FindID。STATIC_CONFIRMED仅说明源码调用先例，不证明本项目操作后读取时序或Settler UI。

当前CityFlowProbe.lua:31将target限定未专业0或专业1，SupportFacts:119–126要求B020 facts与B015 journal一致。因此不能只写一个新的Potential Property或擅改一个表：否则正常读档、Lv1资格和网络都会受到影响。NetworkBridge当前也仅纳入potential==1的DEV来源。下一步先准备支持永久投资的存储整合/兼容旧记录，再设计最小真实移民动作，至少保持已有专业与Lv1收益、不让升级后的网络来源凭空消失。

## 本地证据

新executor测试通过：1→4连续升级、重复凭据、新executor恢复、cap拒绝、总督门槛4→1但Potential4保持；初始写失败零扣除；消耗后确认写失败保留INTENT；最终写失败后从CONSUMED_CONFIRMED完成一次；消耗未生效、位置变更、读取未知、disabled/错单位、重入均不授予额外升级。原test_city_specialization_state.py回归通过，包含真实新Lua VM的保存/重载模拟。

测试运行未连接Civ6，未写游戏配置或运行源码。无新增USER_GAME_TEST_PASS或实机批次。下一轮接入准备不得跳过旧存储约束，也无需重复总督原生读取的已通过测试。
