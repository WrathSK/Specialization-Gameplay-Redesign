# D0010同步：征服城市的一次快照与互斥初始化

Document Owner: Codex
Accepted Design Revision: D0010
Accepted Spec SHA256: a8393b5fa879b060acfa3b89c8a3fc906a2d50849a1a83bcea193506ed9a12e2
Previous Design Revision: D0009
Architecture Revision: A0078
Sync Status: SYNCED_WITH_LIMITATIONS
Runtime: P0-B-034 / modinfo42（本次sync不改）

## 用户摘要

已按D0010区分有候选的征服城、没有候选的征服城及已有专业的继承城，并阻止旧离线入口继续把所有无专业征服城初始化为普通first-completion。当前磁盘未部署专门的征服初始化/Claim项目，也没有已派发的Conquest批次；因此本次更新实现准备和本地测试，不声称修复了一个已有实机征服功能。

用户无需为此次sync操作；B034住房批次仍有效。Claim精确成本尚待后续落地，当前不要求决定，也不擅自设置数值。

## 差异与权威

逐行对比冻结D0009：只有SCOPE-001、ELIG-005征服分流、PROG-001/004/005、新增PROG-006–010、OPEN-04及版本说明变化。住房、专家GPP、Network direct接收/max/sqrt和Commerce IV没有变化。

D0009冻结hash仍为07920f9e87bd7cb08089bdb5bfd1aa6f74ed6483a02fb6167db61cecd76c31d8；新Spec与ChangeLog接受hash一致。设计意图以D0010为准；本文只记录适配，不建立另一份玩法数值表。

## 当前工程冲突清单

| 文件/位置 | 发现 | 本次处理 |
|---|---|---|
| DevelopmentTests/CitySpecializationState.lua / AcquireUnassigned | VERIFIED_NEVER_ENABLED_NO_FACTS后直接生成可普通Complete的schema1记录，未区分非空LegacySet | 关闭这个旧shortcut，明确返回D0010_CONQUEST_INITIALIZER_REQUIRED；不能再将其作为已适配取得入口 |
| DevelopmentTests/test_player_eligibility.py | 无snapshot的取得后直接完成学院并锁定Research | 改为验证旧入口拒绝；新的A/B/C交给独立D0010契约测试 |
| Architecture“专业写入必须由完成事件确认” | 对Claim不成立 | 当前架构区分普通完成与Legacy Claim两种合法Identity origin；已有Identity走转移，不初始化 |
| Reports/Technical/Specialization_D0007_Eligibility_Model.md | 记录旧AcquireUnassigned设计及当时PASS | 保留历史，不回写原研究证据；当前适用性由本文及Status明确取代 |
| CityJournalProbe/EffectiveFacts/ResearchSupport/Lv2Housing等实际运行 | 首次完成记录/owner绑定支持新建DEV城市，要求first区域凭据，不具备Claim来源或永久同城转移适配 | 本次不改运行，不伪造完成通知接Claim；作为Conquest实现的明确前置 |
| Conquest用户测试计划 | 未找到已派发专用测试；既有B011/B013/B015/B033均明确不覆盖征服 | 不编造“旧Conquest已通过”；未来三类验收分别设计，当前不派发 |

TradeRouteProbe中的CityConquered监听用于商路诊断，并不等于专业继承。面板CAPTURE动作是采集诊断，不是征服动作。

## 实现架构与缺口

### 1. 征服边界和一次快照

候选信号为GameEvents.CityConquered(newPlayerId, oldPlayerId, newCityId, x, y)。本机HD Gameplay/Misc.lua:767及其注册会以新owner/city访问城市；官方AlexanderScenario/Scripts/AlexanderScenario.lua也注册该事件。它证明有Gameplay先例，不证明本Mod在此时能获得最终完整区域全集，也不证明跨owner永久UID。

拟先验证当前城市owner、同城转移凭据、完整区域枚举及读取时点。只有ownership transition完成边界上的完整可信快照才可提交。部分枚举/未就绪不能当空集合；延迟到下一回合扫描可能混入新完成区域，不能自动称为conquest-time snapshot。应先捕获边界观测证据；若时点不可靠且无法还原，标记技术阻塞，不能悄悄改成晚扫或普通first-completion。

已有Identity优先检查并转移永久事实；不能先依据现有建筑给其分配模式。缺Property不等于证明没有Identity/历史成果。旧档加载没有真实征服凭据时保持独立OPEN。

### 2. 区域族与冻结记录

复用DistrictFamily的Districts+DistrictReplaces映射。当前数据库静态识别10个v0.1类型（四种标准区域及Seowon、Observatory、Acropolis、Hansa、Oppidum、Suguba），链式/循环/冲突测试通过；真实征服替代区域转换仍待实测。不是把RequiresPopulation或任意“看起来像专业区域”的区域纳入。

未来持久记录需包含同城UID、一次transition凭据、采样边界、初始化mode、冻结LegacySet、候选区域证据及revision；仅在首次合法边界生成。空与未读到必须区别。候选集合是永久初始化事实，不是跟随城市建设更新的缓存；读档恢复使用保存内容，不重新扫描选择模式。后续同事件重入只能核对相同transition，不能重新添加候选。

新离线ConquestInitialization.lua只演示mode/集合/Identity来源契约，不是最终Property schema；输入为MOCK_ONLY证明。重载JSON/新VM验证不等于Civ VI城市Property保存或跨owner转移验证。尚未确认的“未Claim城市再次易主”持久转移适配不自动重置模式；旧记录不同owner/transition需要明确转移适配，不自行重新snapshot。

### 3. 完成事件隔离

Legacy模式的普通区域完成不产生Identity，也不增加候选。Normal模式只处理边界之后交付的有效完成通知；加载/转移重放不是新完成。未确定初始化模式时暂停提交，不能提前用普通完成抢先锁定。候选快照为空后才建立普通历史起点，不能调用伪造新建城的Foundation事件。

目前schema1事实将firstCompletion视为所有Identity必需证据，实际DEV收益还读取f.first。后续统一事实须增加合法Identity origin（FIRST_COMPLETION或LEGACY_CLAIM）及对应专业区域锚点，消费者读取已验证专业身份/区域，不以伪造firstCompletion兼容Claim。已有投资/模板不重置；迁移必须显式，不因schema升级丢失原有成果。

### 4. Claim提供/完成

拟为四种专业分别定义低成本确认项目，项目可见性/可执行性取决于当前owner资格、Legacy mode、冻结集合成员及未锁定状态。完成时Gameplay重新验证同样条件；成功后一次锁定Identity/Potential1，所有Claim立即不可再用，排队/重复回调不能覆盖或再发。

项目条件提供、完工通知、撤销/失效的实际API与UI更新尚待实现/实机确认。未填写精确成本，未假定Cost=1能在所有生产/速度环境保证一回合。若技术方案会违背极低/短确认约束，应报告DESIGN_DECISION_REQUIRED，不静默增加投资成本。

已有Identity城市走永久成果转移，Eligibility/ACTIVE/Network重新读取新owner事实；不用旧owner总督或网络缓存。现有B033账本anchor固定owner/cityID，不能假装已支持这一层。

## 本地验证与证据等级

STATIC_CONFIRMED：Spec hash/diff、旧入口定位、运行文件引用调查、原版/HD事件先例及当前区域族数据库证据。静态证据不等于游戏运行通过。

LOCAL_SIMULATION_PASS：新增test_conquest_initialization.py运行真实离线Lua，涵盖A/B/C互斥、冻结去重、替代族、未完成排除、后续建设不扩充/不锁定、无限期等待、Claim选项退出及不可改选、Normal边界后完成、JSON/新VM恢复不重扫、未知状态/旧档不虚构取得。test_player_eligibility、test_d0005_models、test_district_family三组回归通过；既有Identity的Potential4/凭据/模板保存、新owner ACTIVE及休眠保持已有本地范围。

没有新增USER_GAME_TEST_PASS。Runtime/Design/既有结果与备份未改；备份位于DevelopmentBackups/Specialization-before-D0010-sync。

## Conquest推进与未来验收计划（未派发，不要求现在测试）

1. 先完成可靠同城/转移边界观察、快照与持久模式适配，再接两种Identity origin和Claim条件；不能先打开全体征服城普通first-completion。
2. Case A：无Identity敌城接管时有完整Campus，另有未完工Hub；冻结只能Research，完成Hub不扩充、不自动专业化，重载仍相同，Claim Research后其它选项关闭。可附Campus+IZ两候选确认，但不将每个组合都作为首批前置。
3. Case B：接管时仅未完工Hub；无Claim，之后完成Hub才Commerce/Potential1，后续Campus不覆盖；验证与A模式互不切换。
4. Case C：已有Identity/Potential的城市转移，身份、投资/模板保留；新owner ACTIVE/网络重算，不出现Claim。

首次只派最小的边界/快照验证，待有实际实现包才给用户按钮和数字；最终三个设计案例均须覆盖，但不把无意义的Cheat city-delete当作真实ownership transition证明。目前唯一已派发且仍有效的是B034住房测试。
