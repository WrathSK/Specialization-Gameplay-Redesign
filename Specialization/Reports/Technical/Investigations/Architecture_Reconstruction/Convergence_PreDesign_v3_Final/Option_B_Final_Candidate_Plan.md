# Option B：v3-final完整迁移与退出门禁

调查材料／后继候选；不覆盖正式规范。

Status: Stable（可审阅的候选文档，不是工程或实机 PASS）。

维护者：Primary｜日期：2026-11-03｜实际 develop：`719eb61b410765fb6e8703a47840ce3cec3fa823`。正式记录仍为 D0058／A0183／S0866；B399.426 仅为既有部署记录，本轮未重新验包。

**NO IMPLEMENTATION AUTHORIZATION。** 本主题承接原 H3 中文交付；仅新增候选 Markdown，原 v3 九文件及代码／测试／工具／正式规范／治理／运行包均不改。

## 排期依赖与硬门禁

本候选 → Owner认可送审 → Claude独立只读审计 → 每Finding disposition；重大问题先改计划并必要重审 → Owner再次明确批准正式同步／实施范围 → 先同步受影响successor条款 → 获批Pre-U5窄修 → **U5迁移前基线** → O1→O2→O3/O4/O5；O6依ownerapplied接口可独立推进 → O7 → O8 → Owner收敛验收。

O4纯转换、O5机械声明、O6独立投影可按各自前提分片，不把示意顺序当所有文件全串行；也不能越过真实依赖。O7里被O1/O2/O5需要的production接口必须提前提取，最终删旧文件才留到O7。D1／诊断的不同三态差分是独立轴，不能只做一次开关测试替代。

每片有Runtime Impact（来源真复用、事件范围、最坏扫描/重复计算、cache容量寿命、依赖、恢复触发及针对门禁）、独立小提交与简洁结果/限制，完整机器Closure仍按现行政策留本地。所有下表验证**均未执行**；L2/L3和T01–08为现行工作流门禁，不是新增规范。

## O1–O8逐包候选

### O1

| 项 | 精确候选要求 |
|---|---|
| 入口 | U5基线＋获批F合同，相关FS02/07已同步 |
| 职责／等价 | 统一ACTIVE及受审采样、同ref被动重算；写屏障与phase边界先保留；不建专业Governor缓存 |
| 最小LOCAL | L3，T01/02/04/08；2–3真消费者共享/写后失效、first/cold/negative/同回合第二变化 |
| USER_NATIVE / UNVERIFIED | 只changed资格/普通load；不要求故意造UNKNOWN |
| 失败停止 | 正常UNKNOWN根因未清不可用fallback结项；未批准格子不扩 |
| 回退／兼容 | 不改历史schema；effect变更用独立fixture与exactowner回退，已写native不得假原子撤销 |
| 文本／诊断／删除时点 | FS02/07；P生产adapter若被需要先提取 |

### O2

| 项 | 精确候选要求 |
|---|---|
| 入口 | O1相关事实合同；FS08及P3边界先同步 |
| 职责／等价 | 可靠接管ACK、revision/ref/reentry、错误可见；中央不重放业务；专业owner保留失败责任 |
| 最小LOCAL | L3，T02/05/08；真实producer→FC→Bindings→owner的throw/missing/noACK/旧ACK/新change/同值恢复/close/load |
| USER_NATIVE / UNVERIFIED | 仅本地不能回答delivery/window才最小采样 |
| 失败停止 | 成功sibling无额外深读；静置不补预算；不能ACK当效果/付款成功 |
| 回退／兼容 | session责任按可靠初始化重建，无通用事件存档；旧路由撤离须真实链差分 |
| 文本／诊断／删除时点 | FS08/10；production错误/交付不依赖trace；保留phase0特许EmitDerived |

### O3

| 项 | 精确候选要求 |
|---|---|
| 入口 | O1/O2＋FS03/04=B同步＋NET矩阵审计通过 |
| 职责／等价 | 可靠topology正常发布；warm W／cold K partial／negative；原S9cold重定；D1按E1–E7退役 |
| 最小LOCAL | L3，T02/04/05/06/08；真Bridge+3消费者，cold无W有/无K、失效+unknownsibling、各自max/union/Floor、partial writefail；保留NET1/2 |
| USER_NATIVE / UNVERIFIED | 仅真正缺的native确认/读回；不让玩家造随机失效 |
| 失败停止 | partial不能READY或transaction；cold不猜O，不保已失效残差；根因未闭不删D1 |
| 回退／兼容 | 保留真实历史/收据/SQL IDs及旧技术opaque证据；不自动接/批量删NetworkRecoveryStore数据 |
| 文本／诊断／删除时点 | FS03/04；禁用/真删除D1不得牵出未移交production调用 |

### O4

| 项 | 精确候选要求 |
|---|---|
| 入口 | 相关FS05/06/07先同步；ODP02=A；原生唯一proof按各业务独立 |
| 职责／等价 | 专业schema/合法转换与Store提交分离；root/合法deferred保留；R0窄来源和合同锁定；不全面reset |
| 最小LOCAL | L3，T06/08；原payload/合法transition/CAS/opaque差分；真实Store+Commerce+Capital；CALLING/receipt不重放；E/Dialogue/Insights独立 |
| USER_NATIVE / UNVERIFIED | 只changed合同/load或明确原生未知；不扩大易主玩法 |
| 失败停止 | 需新恢复权威／破坏schema／新端点授权先Owner Packet；严重错误不能靠R0表现正常结项 |
| 回退／兼容 | 新quote provenance向后读取旧terms；恢复不追改旧合同；源码回退≠保存/付款回退 |
| 文本／诊断／删除时点 | FS05/06/07；生产错误持有者独立于可选日志 |

### O5

| 项 | 精确候选要求 |
|---|---|
| 入口 | O2接管入口、成功Start事务和明确composition清单；FS09同步 |
| 职责／等价 | 四专业成功Start后自声明；共享owner一次；中央校验/分发，独特原生完成监听保留 |
| 最小LOCAL | L3，T01/02/05；四专业前后等价、FAILED/SKIPPED/missing/duplicate/type/ref、无半订阅；phase0/Seal/drain |
| USER_NATIVE / UNVERIFIED | 通常LOCAL足够，只有具体native顺序缺口才最小观察 |
| 失败停止 | 不能按kind推业务资格、自动发现插件或无序化phase0；失败不得伪READY |
| 回退／兼容 | 按consumer逐片切换，无结束条件双路禁止；失败回退保原启动可达性 |
| 文本／诊断／删除时点 | FS09/10；bindings对productionowner而不是probe/file名注册 |

### O6

| 项 | 精确候选要求 |
|---|---|
| 入口 | owner真实applied/ref/typedreply合同；FS12展示段同步 |
| 职责／等价 | 完成原S9 D11 owner→reply→机构/banner；current/retained/partial/error/preview分开 |
| 最小LOCAL | L2，T02/08；写失败/cold未观察/退出/选城/ref；真owner publication到UI，不仅字符串匹配 |
| USER_NATIVE / UNVERIFIED | changed applied/partial展示一组，不重做布局/图标campaign |
| 失败停止 | 缺owner值则显示未知，不能用age/L候选冒充收益或UI补ACTIVE |
| 回退／兼容 | 不重设计已验收比例/颜色/布局；UI cache丢失从owner重读 |
| 文本／诊断／删除时点 | FS12；新R0政策值与真实R0也可追溯 |

### O7

| 项 | 精确候选要求 |
|---|---|
| 入口 | 相关O3/4/5/6职责完成；Q账本；FS10；两个部署工具受审删除能力 |
| 职责／等价 | 先迁生产kernel/writebarrier/Flight/现GC、Q1–8及exactcleanup，后移除旧Lua/import/replacement/可选观察者依赖 |
| 最小LOCAL | L3，T06/08；三组独立fixture：观察开/关/真缺file+global；两个工具exact removedset/receipt/failpoint/restore |
| USER_NATIVE / UNVERIFIED | 最小changed load/turn/business smoke；不live重复不确定交易做对照 |
| 失败停止 | 只开关无absence不算；生产差异/未知extras/SQL破坏未批则停 |
| 回退／兼容 | 删除采用普通新提交、精确已审集合、版本/hash/整包恢复点；保存历史和收据不删，GC策略不变 |
| 文本／诊断／删除时点 | FS10；首次发运删除前stable/temporary均过门禁，不能用本轮报告当删除批准 |

### O8

| 项 | 精确候选要求 |
|---|---|
| 入口 | 实际接口稳定，G差异逐项有证据；FS12完成标准 |
| 职责／等价 | 去已证重复采集/无关wake/冗余scan-write/retry与容量放大；必要通知/历史发现保留；全链验收 |
| 最小LOCAL | L3 relevant closure，T01–08按风险；scope/capacity/work counters/idle/secondchange；已知失败逐项处置 |
| USER_NATIVE / UNVERIFIED | 最小changed/load/turn/idle，Owner实机可接受性；无虚假CPU/RAM/%承诺 |
| 失败停止 | 每G关闭或具体证据例外经Owner批准；不能局部PASS拼全绿、旧层长期并存 |
| 回退／兼容 | 最终源码/保存/部署恢复能力分别复核；旧PASS只继承未改场景 |
| 文本／诊断／删除时点 | FS12；正式文本↔实现一致，D1/P3真退出，Owner最终验收 |


## D1-E1–E7：退出不能以hold成功替代

| Gate | 必须验证（本轮未执行） |
|---|---|
| D1-E1 | 普通create/expire/reestablish/cold/signal-only由共享层可靠阶段完成，不给专业普通UNKNOWN正向事件 |
| D1-E2 | dirty立即严格proof失效＋责任登记；首发丢失/同值恢复/同回合第二变/旧ACK均有正确交接，无idle预算 |
| D1-E3 | source/route/receiver/ref/role确认负事实优先；unknownsibling不遮失效；NET03–06精确partial和权限边界成立 |
| D1-E4 | reliable self正常更新；Standardization per-target max、Culture文明并集、Commerce max→domainFloor→sum不变，不能无证改rounding/叠加 |
| D1-E5 | 同初始独立fixture中旧hold保留／禁用的正常行为相同；目标严重错误按B矩阵验证而非要求旧例外A结果相同；partial不授权交易 |
| D1-E6 | D1专用分支／入口／模块如有可撤者真不存在（不是假开关），生产正确/错误/恢复仍可达；不把旧hold改名挪中央；shared未完成责任不是业务hold替身 |
| D1-E7 | FS03/04后继已批；必要changed原生证据＋Owner准许退役；代码/保存/部署兼容及生产职责无遗漏 |

正常短暂未收到新可靠计划时保留既有applied，是事件因果链自然连续性，不等于另设consumerUNKNOWNhold。持续不能可靠完成仍是root问题；不能靠这一解释把D1隐式永久化。

## 原S9/S10及P3清偿账本

| 原义务 | 后继交付，不机械清空 | 位置 |
|---|---|---|
| S9 cold source | **已批B替换**：当前拓扑/源值/真历史重建，warm有界见证，cold无见证NETpartial/negative/恢复；不因旧adapter存在就接入 | O3/FS04；[Mod/NetworkRecoveryStore.lua:15](../../../../../../Mod/NetworkRecoveryStore.lua#L15) |
| S9 applied UI | 真实owner→typedreply→机构/banner；partial/retained/error非候选数值 | O6/FS12 |
| S9 adapter/targets/replies/capture | 仅迁实际依赖，保选城/ref/资格/写屏障和合法采样；已完成模块不重开全审 | O1/O5/O6 |
| S9 deferred/subrecords | 保留可靠权威可确定转换和合法延迟；修root，不全reset/全删 | O4/FS05/07 |
| Q1 InspirationProbe | 生产exact withdrawal迁走，保留旧ID和必要定义 | O7；[Mod/CultureInspiration.lua:70](../../../../../../Mod/CultureInspiration.lua#L70) |
| Q2 timing/UI | TimedProject*正式显示/选择与旧ProjectTurnRead/TimedTurnProbe替换层分别核查，迁实际caller再撤replacement；不凭包清单认定其业务计算 | O7；[Mod/UI/TimedProjectDisplay.lua:6](../../../../../../Mod/UI/TimedProjectDisplay.lua#L6)；[Mod/SpecializationP0.modinfo:50](../../../../../../Mod/SpecializationP0.modinfo#L50) |
| Q3 Construction/Precision | ReadSnapshot是Crew生产输入；Precision是UnitActions装饰器，保返回三元组／结果。唯一发放proof独立 | O7；[Mod/CrewProjects.lua:303](../../../../../../Mod/CrewProjects.lua#L303)；[Mod/ConstructionProbe.lua:7](../../../../../../Mod/ConstructionProbe.lua#L7)；[Mod/CrewPrecision.lua:22](../../../../../../Mod/CrewPrecision.lua#L22) |
| Q4 Meaning | 实验Lua未启动不能推出同名SQL可删；生产92ID验证/cleanup仍在，必要职责留productionowner | O7；[Mod/CultureMeaning.lua:9](../../../../../../Mod/CultureMeaning.lua#L9) |
| Q5 ExpeditionGate | 旧路径与当前SpyGate/保存/SQL分开；只退真实旧职责，不修新Expedition功能 | O7 |
| Q6 identity/inheritance | 按实际Start/调用迁生产映射/隔离，inactive实验分别核实，不按名字整组删 | O7；原v3Q6范围保持 |
| Q7 Dialogue | 旧positive退休，但paired sample、ACK、generation、ready、cleanup仍移交 | O7；[Mod/Dialogue.lua:298](../../../../../../Mod/Dialogue.lua#L298)；[Mod/UI/DialogueRefresh.lua:26](../../../../../../Mod/UI/DialogueRefresh.lua#L26) |
| Q8 Half/GreatWorkProbe | Halfpositive已early return；其它reader/exactcleanup分别迁移；观察者可真缺失 | O7；[Mod/Gameplay.lua:930](../../../../../../Mod/Gameplay.lua#L930)；[Mod/LegacyCleanupCatalog.lua:10](../../../../../../Mod/LegacyCleanupCatalog.lua#L10) |
| G30 kernel | P写屏障、Flight及现GC安全控制先独立；trace factory和collector最终仅观察 | O1/O2/O5前提＋O7收口；[Mod/Probe.lua:553](../../../../../../Mod/Probe.lua#L553)；[Mod/PerformanceCounters.lua:204](../../../../../../Mod/PerformanceCounters.lua#L204) |
| 双部署删除 | stable和temporary都审批准before/after/hash/精确removed set，拒未知extras；receipt记删除；failpoint/完整backup恢复，不盲copy | O7首次删文件部署之前；[tools/deploy.py:50](../../../../../../tools/deploy.py#L50)；[tools/temporary_playtest.py:37](../../../../../../tools/temporary_playtest.py#L37) |
| SQL/save IDs | 必要稳定ID、opaque技术数据、真历史和receipts保留。Carrier专项缩减/重编码/破坏相容不自动获批 | 全包；仅发生新真实取舍才Owner Packet |

## 双差分与结束条件

诊断开／关／缺file+global三组独立fixture比较启动、ACTIVE、历史/receipt、own载体、Money/Unit、交接/恢复、typed业务UI；只允许观测输出不同。禁止在live重复不确定扣款/创建来对照。D1的保留／禁用／真实退出另一轴，正常等价、已批准B异常按新规则验证，不能要求新旧不同政策全相同而弱化断言。

G01–30每项必须真实关闭或有具体证据/Owner批准例外；重大审计Finding不得“实施后再看”结项。候选内部QA、接口起名、文件减少、旧测试PASS及U5均不能替代职责实际移交、D1/P3退出、正式一致和收敛验收。
