# 保存层定域修复计划

Date: 2026-10-08 / America/Vancouver
State: **PLANNED_NOT_AUTHORIZED**
Review baseline: develop `e02ef7519d17c5733ebc324a4fa3bc9aa458a5c2`，clean／与origin同步；登记source/live B168.195不变。

本文件是用户要求的修复方案，等待审核及明确implementation授权；不取代当前Authority/manifest/Status，也不恢复B168实机待办。审计已经收束，原报告及原始证据不改写。本轮只提交本计划，无实现、玩法测试或部署。

## 目标和单批范围

第一批处理两个相邻问题：

1. **IA-P06a-F01**：普通可靠记录字段写入重复扫描全部城市引用。把跨城检查移到恢复、新注册和有效引用改变的边界。
2. **IA-P06a-F02**：坏current/loss端点再次被共享检查直接解引用，扩大为collection fault。隔离不可读record，保留其历史和位置reservation，避免阻断其它正常城市读取及不变引用写。

依据：[保存层审计与实际Lua反例](../Audit/P06a_State_Ownership.md)、[最终优先级](../Audit/P16b_P17_Final_Audit.md)、[实际Store](../../../Mod/CityProgressionStore.lua)。审计40记录/40计龄写的1600次访问是唯一性循环次数，不是native耗时；本批验收同一口径，不承诺进程内存零增长。

不加入全量owner-by-ref索引、不新增持久字段/文件/状态机。仍由Store持有唯一提交权；业务model及原有record schema不变。

## 现有事实与不能误改的保护

- `storage.Write`676–694先比manager旧snapshot、Game旧值，再扫描其它record；写/readback成功后才更新envelope。
- worker `save`160–164先完整validate并持有candidate，失败hold目标；本批不顺带改变提交期间reader可见性（Q01）。
- load727–745保留index位置、创建worker，然后扫描引用；badrevision能局部hold，但badcurrent导致共享解引用失败（F02）。
- 新城1009–1039先index reservation读回、再City token、record；不得改成盲目覆盖或自动补完整空record。
- 已有可信record在恢复时发生真实引用碰撞：保留collection hold。提交前candidate碰撞：保留拒绝目标写/hold目标worker，不扩大成所有城市停写。
- Native当前引用、历史origin和binding token各有职责；有效引用按既有`loss.target → current → origin`选择。不得拿城市名、单独坐标或历史CityID猜当前对象。

## 实施步骤

### 1. 安全提取有效引用

在Store内部复用一个小型引用校验入口，输出可靠的`(owner, cityID)`或明确不可用。检查所选端点结构，避免对boolean／错误table取字段；损坏字段不能静默当缺失、回退origin或生成新引用。完整业务校验仍保留，不以此替代record validator。

坏业务字段但端点可靠的record仍保留引用占用，例如坏revision；不能按worker是否ready把所有坏record排除。坏／缺record的index与位置reservation不删除、不重建、不退回旧City Property writer。

### 2. 恢复时一次检查

load时安全收集可确认的端点并检查真实碰撞。不可读record保持局部HELD，保留原件和reservation；正常对照城可读取、可做不变引用更新。

无法解析的端点仍是不确定占用，不能宣称全集合唯一性已经证实。任何依赖该未知占用才能证明安全的新登记／引用变更继续保守拒绝；不以跳过坏数据换PASS。可靠getter返回nil按既有未完成登记reservation处理；getter抛错、复制失败或结构不可信属于未知，不能当缺record。未知端点只拒绝无法证明安全的目标新登记／有效引用变更，不直接把正常城市设为collection fault，不按部分字段猜引用。

本目标是修复坏字段直接引起的跨城解引用故障，**不是保证损坏存档下所有结构性动作都可继续**，也不修复／猜补坏record。

### 3. 普通写快速路径

完整validate后，比较manager已提交旧snapshot与candidate的有效身份对：

| 写入类型 | 跨record唯一性检查 | 保留步骤 |
|---|---|---|
| 年龄、receipt、timer、模板等业务字段改变，但有效引用不变 | 不再扫描全部record | 完整record验证、旧snapshot比较、Game旧值比较、写锁、写/readback、成功后副本更新 |
| 首次record提交／新登记／有效引用改变 | 仍进行安全跨record检查 | 已有占用、未知占用保护、真实碰撞拒绝、stale/readback等全部门禁 |
| 恢复 | 一次安全集合检查 | Schema/index、位置、record与绑定校验；不写历史、不重放副作用 |

失城与夺回不能按“只是stage改变”走快路径：只要实际有效引用改变就走结构检查。同回合真实变化继续允许，不加“每城每回合最多写一次”。复制隔离和目标完整校验不删除；本批只减少重复跨城检查，不声称所有分配／扫描归零。

### 4. 引用变更失败时保留占用

当前代码setter抛错会跳过readback；若底层实际已写入candidate，Game与envelope可能不同。这是源码可见的失败窗口，原生可达性未证明，不报告成已经发生的事故。

对**首次record提交／引用变更未正常成功确认，且不能可靠证明Game仍等于旧snapshot**的失败token，保留旧引用及候选引用的session reservation。首次提交旧值为nil，不补造旧引用；每个已hold token至多一个候选，不维护全量反向索引、不写存档、不自动重试。setter失败后读到完整candidate也只证明可能占用，不能晋升成功snapshot或恢复worker。读回既非旧值也非candidate时标明确未知占用并保守阻止相关结构写，二元reservation不冒充覆盖任意第三值。重新加载按实际可靠记录重新建立检查，不直接重放failed candidate。

单城失败仍hold目标；其它正常不变引用写不被无必要停止。后续结构写必须核这些可能占用，不能拿envelope旧snapshot当Game已确认真值。若最小路径不能保持现有失城撤销／恢复保护，停止该具体路径，报告需要扩大哪些调用点；不静默牺牲安全性。

## 预计修改面

| 文件 | 预计内容 |
|---|---|
| `Mod/CityProgressionStore.lua` | 有效引用提取、load隔离、write快／结构路径、有限失败占用；不改对外业务API |
| `DevelopmentTests/test_store_write_boundaries.py`（建议新增定向入口） | 实际Store、真实字段形状、少量计数与注入；不复制新模拟框架 |
| 当前对应Store/E2定向tests | 仅必要fixture接入；原断言和冻结通过记录保留，不能改到全绿 |
| 既有Architecture保存说明、实施结果、Status及必要W0001索引 | implementation获授权后记录新协议和证据，按已审变化同步hash；不整库rehash |

本计划先单独落在Proposals；不新建批次manifest、不把当前P0-L3A替换为已授权修复。获准实施时再登记该批准确依赖与版本；build/modinfo届时分配，不预先写成已完成或已部署。

## 本地验证：W0004 L3，限定保存风险

不运行全历史玩法套件、notification stress或新的内存长测。复用B108多城/E2、投资/Claim、模板和传统的实际fixture及已有成熟证据；仅运行与本次改动相交的回归。

| 验证组 | 必须得到的结果 |
|---|---|
| N/T成本 | N/T=8/8、20/20、40/40、40/1；初始化之外，引用不变的年龄写跨record唯一性访问0。年龄/receipt等逐值和实际写次数保持；仍有其它工作，不称总成本0 |
| 同回合变化 | 重复无变化零额外写；同回合真实投资／timer／模板变更可保存，不能被粗粒度限频跳过 |
| 结构边界 | 新登记、loss、recapture变ID检查碰撞；现存碰撞load整体hold，candidate碰撞只拒绝目标，控制城不被改写 |
| 损坏隔离 | current/loss/nested endpoint不同坏shape、坏revision但有效引用、缺record reservation、坏index；正常对照城读写正确，未知不被当合法首次初始化 |
| 失败/readback | stale、silent-drop、throw-before、throw-after-apply（含可靠读到candidate）、readback错误／第三值各自区分；目标hold／旧snapshot／候选占用符合可靠证据，相关引用不被再占用 |
| 保存恢复 | actual Property fixture重建Store，记录和历史逐值保持，加载不写、未完成操作不盲重放；UNKNOWN与其它城市隔离继续成立 |

旧审计脚本／结果保留不改。新检查可用Git固定基线对照旧代码，计数仅指明确循环，不新增常驻telemetry。新测试替身必须采用真实Store loss／record结构，不能再用合成targetID掩盖接口差异。

## 最小实机与部署边界

先完成本地checkpoint并提交，再处理部署。**本计划及本轮不包含部署授权或当前实机请求。** 新测试包仍须既有game-exit/source/hash/receipt/recovery门禁；不回退B168或改变GC。

因本批真正修改保存及load检查，建议后续只有一次最小实机：现有已支持存档中，查看两座城市记录（尽量一座已有Research传统）→过一个正常玩家回合，确认记录／年龄按原规则变化→一次合法投资或本来可做的业务写→保存退出、冷加载→确认两城Identity/Potential/receipts/模板／年龄保持。没有符合条件的传统城时不要求造40城或人为破坏存档；具体fixture在实施结果后固定。

这是验证新保存边界，不是共享Probe ON/OFF生命周期重测。无需重复所有能力、所有易主/夺回或几十回合长测；异常才追加能区分具体原因的步骤。本地访问次数减少不能写成原生内存／CPU已改善。B168 GPP待办独立保留，不能由本批通过替代。

## 排除与完成条件

不处理F03业务扩展框架、Q01提交可见性、Q02return通知顺序、科研Owner保龄适配、事件广播/缓存/GC、Crew/Standardization本体、Probe session错字段、Claim旧key、商业合同／REALLOCATING；不修改Design、save schema、cityKey、AI/multiplayer、main或永久成果归属。

退出条件：成本快路径和逐值行为通过；恢复/结构检查仍有正确碰撞保护；坏record不被清空／猜补、普通对照城正常；未知写入占用有明确保护；定向回归与文档/context检查完成。若需要改持久schema、业务ownership或扩公共事件架构，停止对应路径另报，不以本方案授权。

用户需要决定：是否接受这一个定域批次及上述保守故障边界，再明确授权implementation。
用户需要测试：当前无；本地完成后仅上述一次最小流程。
Codex下一步：本计划提交后停止，等待授权；不实施或部署。
