# P07a — 投资凭据、单位消耗与恢复边界

独立审计 IA20261007 / W10；基线 `eda22faa06bcffbb6fbd778396af66b4aa292b7c`，slice覆盖完成，非总审计或native PASS。只写审计产物。

## 本slice回答的问题

**永久Potential、投资receipt、单位销毁与失败恢复是否有唯一责任；现有接口能否安全承接后续长期事务？** 聚焦Settler投资，不深入施工队、Claim、商业合同或每项收益生命周期。

正常事务责任清楚，未确认新的重复发放或Owner绕过：InvestmentAction唯一消费/finish，Store唯一现代持久后端，EffectiveFacts从完成receipt派生Potential。确认消耗未持久化时保持HELD、不自动重扣；确认阶段已保存时，同Owner冷加载可完成最终receipt。这里证明保守恢复分支，不等于原生任意时点都具有多对象原子性。

登记 **IA-P07a-Q01：MEDIUM / MONITOR**：若已确认pending与失城状态共同保留，当前夺回保护与投资恢复入口形成条件性死端。本地组合复现成立，**正常native可达性未建立**；不是实际损失事故，不升级为必须重构。没有新增FIX_NOW。

## 规则与权威

[Spec PROG-002/004](../../Design/Specialization_v0.1_Design_Spec.md)及[Shared SETTLER_INVESTMENT_CONFIRMATION](../../Design/Content/Shared_D0045.json)规定：准备前不消费；确认后消费、receipt与Potential视为原子完成；内部交错属于技术原子性/可靠恢复，不能新增半份Gameplay资产或跨Owner pending继承。正常永久成果保留不等于当前ACTIVE继续生效。

[当前E2合同](../../Architecture/v2/P0_E2_Plan.md)133–139要求不猜INTENT、不二次消费、现代后端恢复及事实发布。其较早“旧load循环跳过迁移城”不能解释成当前InvestmentAction完全不恢复现代后端：现有唯一finish会先通过Store路由。

[D0032目标合同](../../Architecture/v2/D0032_Adaptation.md)31–58明确：目前`1+receipt count`只能编码既有投资，未来重组P−1须独立合同；不能把当前投资ledger扩成万能长期事务。目标模式/未来能力存在不证明已实现。

## State ownership 与阶段map

| 状态 | owner / authority / 生命周期 |
|---|---|
| 正式Identity/P1、完成receipt | Store逐城Game slot；reader/writer副本；origin锚点不因当前CityID变化改写 |
| 当前城市/总督/单位事实 | engine；逐次合法读取，UNKNOWN不是P0；总督只影响ACTIVE，不限制永久投资合法性 |
| Potential / ACTIVE | EffectiveFacts：Potential=1+完成receipt数≤4；pending不计入；ACTIVE读取当前Governor gate，不保存旧值 |
| INTENT / CONSUMED_CONFIRMED | 投资ledger中的技术阶段；InvestmentAction唯一解释/转换；不是可独立继承的Gameplay资产 |
| plan、busy、halted、preview | session；IA plan拥有事务预览，UnitActions外层plan拥有按钮动作。移除/失效清preview；destructive失败停止重试；load丢preview并核持久事实 |
| 单位reservation | 单位Property，仅辅助证明具体消费，不能替代Game receipt；finish不重新Destroy |
| 当前收益/Network | 已提交事实的consumer；Gameplay正常/旧入口都有显式Refresh/Audit，不由receipt携带旧收益 |

实际路径：[InvestmentAction](../../../Mod/InvestmentAction.lua)、[EffectiveFacts](../../../Mod/EffectiveFacts.lua)、[Store](../../../Mod/CityProgressionStore.lua)、[UnitActions](../../../Mod/UnitActions.lua)。

| 阶段 | 精确行为 / 失败后果 |
|---|---|
| IA88–104 Prepare | 当前Owner、Identity/Potential、单位类型/位置/未预留；记录同回合anchor与ledger副本；仅session，零永久写/消费 |
| IA110–123 Confirm | 先核当前facts/旧receipt，再核prepared token/owner/city/turn/anchor/ledger/Potential/单位；前置失败REJECTED，无debit |
| IA124 / 43–50 | 先写INTENT，核旧值/当前引用/读回/写后facts；失败HELD，尚未调用Destroy |
| IA125–128 | 复核单位、写reservation并读回，Destroy，要求numeric ID不再存在；失败停在INTENT，不猜成功 |
| IA129 | 保存CONSUMED_CONFIRMED；若失败，持久INTENT不自动发P/重扣 |
| IA52–59 / 130 | 已确认阶段才finish；同reservation单位仍在则拒绝；添receipt、revision+1、清pending；不Destroy第二次 |
| IA144–161 LoadScreenClose | 清session preview，仅对当前人类城市读持久ledger；confirmed可finish，INTENT拒绝，未读city保持未知 |
| Store249–260 | 比较current投影旧值；持久anchor仍origin；保存新record；P4 Research年龄起点与第三receipt在同record提交，不独立补造 |
| Gameplay428–442 / 503–519 | 正常/旧投资入口结束后更新consumer。现有名单扩展成本已在P05b登记，不重复新增finding |

正常成功投资有3次持久阶段写；每次还做事实与读回核对。单次用户操作成本与公共Store全record检查的乘积复用IA-P06a-F01，不把每次验证机械删掉，也不把罕见按钮动作称高频热点。load一次遍历当前人类城市，是恢复路径；不因被称event-driven就推断零扫描。

## 冷加载与错误事实

| 持久结果 | 同Owner仍合法时恢复 | 能证明什么 |
|---|---|---|
| 无INTENT（初写未确认） | 不补receipt；单位尚未消费的断言在既有fixture | 无凭据不补造成功 |
| INTENT，单位消失 | HELD/P1，保留技术记录 | 不根据缺单位猜已消费，不二次消费；不能称成功原子完成 |
| CONSUMED_CONFIRMED | finish一次→receipt/P2，无Destroy | 确认凭据可恢复，不自动推断其它消耗 |
| 已完成receipt | 重复确认无副作用；正常UnitActions可能先因单位/plan缺失拒绝 | 幂等不要求每个入口返回相同成功文本 |
| owner/ref/token不可读 | 不fallback旧记录，不发0，不自动清history | 合法保护，稍后可读不等于此模块自动重试finish |

Store138–159区分当前引用与历史锚点；249–260恢复持久origin后写。modern Owns故障仍阻止旧后端接管。Store105–110去pending后复用结构validator，完整pending校验在EffectiveFacts31–42及IA阶段转换；**WriteInvestment不是任意caller都可安全使用的通用事务API**。这一扩展约束补证既有IA-P06a-F03，不制造第二个相同finding。唯一当前producer有完整校验。

## Provisional — IA-P07a-Q01

**confirmed pending × HELD_TRANSFER：自动恢复入口与夺回门禁互相阻断。**

- Store598–602保留investment并写HELD_TRANSFER；Investment getter/write要求ACTIVE（138–151）。
- IA144–161恢复只遍历当前人类城市；外国城不finish，不能在AI控制下擅自运行系统。
- Store559在ACTIVE/current返回提交前拒绝任何pending；IA162 return callback仅清preview。
- 所以当上述保存状态成立时，原Owner返回会停在RETURN_PENDING_INVESTMENT，自动finish也无法通过active门禁。不是把历史账本删除，而是record保留、暂不可用。

**强度：STATIC＋实际未修改Lua的LOCAL结构反例；native状态可达性UNKNOWN。** 最小fixture先令最终写失败留下CONSUMED_CONFIRMED；在下一次初始化时显式设置foreign-owner事实，之后走实际loss/原binding return。该foreign切换是注入，不证明玩家正常点击会在同步Confirm中操作外交，也不证明真实游戏会保存这个交错。

| 输入 / 对照 | return结果 | 重复/冷boot/控制城 |
|---|---|---|
| 已完成receipt | ACTIVE / P2 | 不重复debit/写record；控制城不变 |
| 持久INTENT | HELD_TRANSFER / RETURN_PENDING_INVESTMENT | 不补P或二次debit；控制城不变 |
| 持久CONSUMED_CONFIRMED | HELD_TRANSFER / RETURN_PENDING_INVESTMENT | 已确认也未被finish；控制城不变 |

[脚本](Evidence/W10/reproduce_pending_return.py)／[原始结果](Evidence/W10/pending_return_result.json)记录源码/fixture/脚本hash。复用W03 fixture声明，不执行原测试case；existing Lupa Lua5.5，无安装、DB、游戏、存档或runtime操作。original binding保留，不复制token、不按城市名或猜旧ID恢复。fixture过滤本地玩家城市以排除foreign；AuditNoEffects是明确退出stub，不证明真实carrier退出。

Severity **MEDIUM**（条件下整个record无法自动恢复）；timing **MONITOR**（没有正常native交错/当前事故证据，局部而非所有专业立即返工）。在增加新的永久副作用writer或修改投资/return时核这条恢复闭包；若获得具体native组合状态、late-load恢复缺陷或相同风险合同，再升级定域动作。不要求用户制造极端中途转Owner测试。

候选边界仅供未来授权修复：独立识别可靠confirmed技术记录与未知INTENT，明确同Owner完成恢复与ownership门禁的协调责任；不要为消除此保护而允许任意pending继承、不清记录、不猜成功。不能在本审计选择新的退款/继承玩法。

## 其它保留边界与反证

- **NO_ACTION**：Potential与ACTIVE分离；已完成receipt只算一次；INTENT不猜；单位移除正常事件清两层plan；receipt完成后ID被其它单位复用不否定可靠历史。
- **LOW / MONITOR支持前提**：Prepare只保存numeric unitID；UID在Confirm创建。若移除event缺失且ID被复用，preview无法区分替身。正常delivered事件有两层清plan，未证明原生丢事件，不单列confirmed defect或新实机门禁。
- **扩展提醒**：IA/UnitActions的两层preview及文本结果不同职责；当前没有双永久authority或误判成功证据。下一action新增时沿用明确token/阶段，不因DRY建万能executor。
- **恢复限制**：一次LoadScreenClose finish遇到暂不可读，不会同session周期自动重试；当前仍保留pending，后续load可再核。记录支持边界，不扩成每回合扫描。

## 测试证据与范围

本轮静态审阅正式测试，**没有运行完整历史/Gameplay回归**。只有上述3场景审计复现执行。

- `test_investment_store_bridge.py` / `test_settler_investment_executor.py`加载DevelopmentTests离线model/executor；写失败/Resume/reentry断言不直接证明现行IA或Store。
- `test_native_investment.py`仍使用旧路径/接口/version断言；Catalog59/78/83与Tests README明确它们是HISTORICAL_OR_MODEL，不报告当前导航缺陷，不修改它们求全绿。
- 反证：实际Store/IA有E2、B108、B136、B143定域断言。B108182–195覆盖正式逐城三写失败与控制城；B13699–112、161–177用当前GovernorGate并核现代V3；B14372–85覆盖第三receipt/传统起点同record失败和confirmed coldboot恢复。这里只核断言内容，没有新PASS。
- Q01组合此前未由这些摘段证明；离线executor consume-reentry不能代替IA真实callback。同步内存Property、立即Destroy及event列表不能证明Civ VI中途持久化、OS硬中断或真实交付顺序。

实际读取：IA/UnitActions/EffectiveFacts全文；Store投资/active/投影/保存/return/loss与manager wrapper具名段，复用P06a既有ownership；Gameplay两个dispatch消费名单；Spec PROG完整相关条款与Shared原子性对象；D0032永久/事务合同及E2投资/cutover段；三指定短测试/离线Lua、B108/B136/B143/E2直接fixture断言、Tests README/Catalog。Authority/CURRENT与W0001直接入口复核。没有全Mod或全历史通读，截断搜索/历史标题不算完成读取。

## 续接

P07a问题已收束；完整P07仍未完成。下一 **P07b：Claim / 完整1T项目的完成回调、持久timer与Identity提交**，从`Mod/ClaimProjects.lua`、Store ClaimStart/ClaimComplete/claimTimer、`Mod/TimedProject.lua`（后续按真实调用关系读取）进入；只按真实调用扩大到队列helper/测试/当前E2相应合同。施工队不可盲目发放的native grant另作P07c，不与Settler或Claim自动统一。继续前先保存此slice checkpoint；无新用户决策或实机要求。
