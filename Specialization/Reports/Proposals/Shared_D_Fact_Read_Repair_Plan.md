# Shared D 普通事实与诊断分离：定域修复计划

Date: 2026-10-08。State: **IMPLEMENTATION_COMPLETE_AWAITING_USER**。评估baseline：develop `9659316`，工作树clean；source/live B169.196不变，B169最小保存验收已通过。用户已授权本独立Shared D切片，B170.197本地完成，见[实施与验证](../../Status/Validation/Results/Specialization_B170_Shared_D_Fact_Read_Local.md)。下文保留批准时范围；实际实现保留全presence检查，不改目录／其它finding。

## 为什么排第二

[最终审计](../Audit/P16b_P17_Final_Audit.md#建议处理顺序按返工增长和真实依赖排序)顺序2为 **IA-P13a-F02 / MEDIUM / FIX_BEFORE_NEXT_PROFESSION**。不是发现当前D算错，而是更多专业及内部carrier定义会增加普通采集的工作量；只缓存定义枚举不能消除每城presence检查，命中仍复制完整诊断树。

第一项Store已由B169定域处理，本计划不重开保存层。审计对D缓存超过8键轮巡的意见仍是MONITOR：当前合法D工作集>8未证，不因总城市20–40就扩大缓存或另加全量索引。

本finding同时涉及D与馆藏。本次建议只授权D切片；GW Collector逐建筑/动态槽位另成候选批次，不能用静态slots过滤假定完整，不能为同一个finding把两种语义绑成大改。此次评估不修改冻结审计证据。

## 当前代码核对

- `OrdinaryBuildingCatalog.Build`保存每个loaded Building的分类，numeric/string双键。它区分普通建筑、tier未知、ordinary但depth未审、替代冲突、未知建筑、内部carrier等；不能退化成“有tier才保留”的目录。
- `DistrictCompleteness.Start/capture`首次建立buildingOrder，之后每次miss仍对全部定义HasBuilding，并读取已存在建筑的位置/掠夺状态，构造district/building/excluded全明细；当前生产目标也有诊断读取。
- `Calculate`同一专业域选择最高单区域D、同值取最小districtID，不累加多社区；保留完整/掠夺、location/domain冲突及tier未明原因。
- `Read`持有≤8城cache，每次返回完整clone；ref/epoch/revision、dirty、新回合兜底和return失效均有既定职责。失败保留旧value但availability为TEMPORARILY_UNAVAILABLE，不能把VERIFIED当本次READY。
- 正常直接消费者：ResearchApply、ResearchChair、ResearchInfrastructure、CultureAesthetic、CultureMeaning；Shadow/Probe及Describe还需要完整解释。其中Chair/Aesthetic会消费逐建筑事实，Infrastructure显式检查ordinary tier/location，不能把API简化为domain→数字。
- `GreatWorkFacts.Collector`有独立完整presence/动态slot校验；本批不改。CurrentSpecializationFacts/EffectiveFacts的Identity/ACTIVE计算也不改。

## 独立批次目标

同一城市、同一可靠事实下，实际业务计划/收益/资格/UNKNOWN行为保持；正常读取不再构造或复制完整诊断排除树。目录扫描的缩减只做能证明安全的一部分，并与“少构造明细”的收益分别报告。

### 1. 先锁定最小业务事实合同

逐一列出上述五个实际consumer及其纯model读取字段，形成字段级差分测试。紧凑snapshot至少保留：

- reference/token、epoch/revision、validity、availability、错误/不完整原因；
- 区域id/type/baseDistrict/domain/plot、complete/pillaged、D与uncapped值、domain选择结果；
- consumer所需的逐建筑type/index、ordinary、tier及tierSource、completion/pillage、贡献与位置/目录冲突原因；
- depthEligible=false、tier=nil、当前未支持目录与未知分类的可判定状态。

只移除确实仅用于展示的名称、排除行展示副本/字符串等。不能因为某一个consumer仅需D，就丢掉其它consumer的合法性证据。必要副本隔离保留，不向调用者泄露可变cache内部对象。

### 2. 同一权威采集，正常/详细两种读取

在现有DistrictCompleteness内增加明确的紧凑读取入口，现有Read详细行为保留兼容；名称实施时确定。共用Catalog、reference及失效规则，不建立第二套独立D算法或长期状态。

正常路径只生成计算必需的事实和小型错误信息；完整诊断在明确查看时补采/构造。详细读取与普通读取不能各自演化成两个不同的当前真值；诊断如读到新事实，应通过同一当前采集/确认边界处理，不直接驱动额外收益或复用已失效数据。

同ref/同事实下切换详细模式不应无故制造新的业务revision或重复publish。保留旧详细revision用途时，必须先核现有使用点；不为减少通知而隐瞒真实变化。detail结果不跨失效/owner/load复用，不无界累积城市或历史快照。

### 3. 收窄presence扫描：只做可证明安全项

目录初始化可一次遍历全部定义，这是静态成本；目标是避免新增无关内部定义线性增加每城普通查询成本。

优先复用既有分类，建立“业务必需/必须保守检查”候选集合。ordinary、tier未知、替代冲突、未审普通域及可能影响合法性者不能过滤。仅对已证明不参与任何本批consumer业务/完整性判断的内部定义，考虑不进入普通presence列表；完整诊断仍可列出排除项。

不能仅凭`BUILDING_SPC_`前缀新增全局忽略、改变catalog含义或假定第三方建筑没有动态作用。不涉及删除carrier。必须核对旧全扫对这些行的失败语义：不能把业务未知吞成READY；若某行仍承担独立安全检查，就保留其检查。

若无法证明某类可排除，保留全扫该类，本批仍可完成明细分离；报告真实剩余B依赖，不假称全部扫描已优化。无需为此先调查新的native建筑枚举API或搭建全局建筑事件账本。

### 4. 迁移真实正常消费者

五个正常writer在所需字段覆盖后改用紧凑入口；共享纯model仅作必要形状适配，不改计算规则。ResearchInfrastructureShadow.WithWorkers是正常路径直接依赖，须核其业务读取，Describe继续完整诊断；CultureMeaningProbe仍用详细入口，除非实证需做最小兼容修改。

保存、投资、Claim、收益carrier/writer本体、旧效果退出、GC保持不变。若一个consumer有无法保持的未知语义，停止该子路径并报告，不能让一部分悄悄采用宽松资格。

## 触发、范围与状态生命周期

触发沿用当前dirty事件和新回合显式读取兜底；不改中央Gameplay事件链、不加每帧/每城/每回合新扫描，不采用“每城每回合只算一次”。同回合建筑/掠夺/修复/作品相关真实变化照常更新。

cache仍由DistrictCompleteness拥有，沿既有ref/token、epoch、dirty、owner/return、load边界失效，容量保持8。没有新Property/save schema/持久文件、跨consumer全局缓存、订阅总线或常驻计数器。

## 预计修改面（实施授权后）

| 文件/组 | 真实依赖与允许改动 |
|---|---|
| Mod/OrdinaryBuildingCatalog.lua | 保持分类语义，必要的普通候选索引；不扩目录支持 |
| Mod/DistrictCompleteness.lua | 紧凑读取、按需detail、同一确认/缓存边界 |
| ResearchApply/Chair/Infrastructure、CultureAesthetic/Meaning | 正常入口调用与必要字段适配 |
| 上述纯model、ResearchInfrastructureShadow | 只有确实依赖形状的最小适配；不改收益公式 |
| 对应既有tests与一个定向新入口 | 新旧实际Lua差分、读取/构造口径、mutation隔离与异常测试 |
| 现有Architecture、Status、当前批次manifest/index | 实施后正常记录，不在计划阶段激活新batch |

这不是“只改两个文件”的承诺：五个实际consumer是直接影响面。不会修改GW、RuntimeWork、Gameplay广播、NetworkBridge、Store、部署工具或其它审计项。包版本只在获授权实施后按现行流程分配。

## 本地验证：L2，公共事实边界的定向回归

复用test_p0_a、test_b133_redundant_reads、test_neighborhood_depth_catalog，以及ResearchApply/Chair/Infrastructure相关和CultureAesthetic/Meaning实际测试。实施前挑直接相关case，不机械运行所有历史wrapper，不改断言来掩盖差异。

1. **逐值对照**：固定Git基线实际旧实现与新实现，比较五个consumer输出/desired效果、资格、UNKNOWN、ref与必要revision语义；同回合真实变化不能漏。
2. **业务边界**：已完成/未完成/掠夺/修复；tier0/nil/T1–4；替代/域位置冲突；社区多实例选择；depth未审/未知目录；owner变更中读取、load/return失效、旧事实TEMPORARILY_UNAVAILABLE。
3. **普通与明细**：普通→详细→普通的结果一致；详细模式不额外发收益；修改返回对象不污染cache；hit/miss都验证；无关排除明细保留可读。
4. **规模口径分开**：用少量受控loaded定义数，例如B0、B0+100、B0+1000，分别增加确认无关内部定义及保守未知定义；统计定义枚举、每城HasBuilding、location/pillage、返回/构造明细行、五consumer整轮读取。不能用定义枚举下降冒充presence下降。
5. **退出条件**：普通hit不复制完整diagnostic树；miss不构造仅展示排除详情；若排除已证无关内部定义，则新增这类定义不增加普通presence次数。若某扫描仍随B增长，明确留下，不能以局部降低宣称F02全部关闭。

全部计数来自测试包装/隔离fixture，非新增生产telemetry；不换算native CPU/内存收益，不跑stress或要求40城存档。

## 最小实机建议

本地先完成。若仍只改变事实读取/投影、未改persistence或writer cleanup，继承B169保存验证及已有生命周期证据，**不要求保存启用态→关闭→冷加载→重启**。

一次连续session即可：利用现有科研或文化城，记录当前相关能力；完成一个可提高D的合格建筑，检查同回合预期收益变化及完整诊断一致；同城已有可行的掠夺/修复条件才顺带覆盖，不要求特意造局。第二种consumer若本地无法证明关键差异，再说明原因后增加最小对照。测试对象/预期差值在实现结果确定，不先要求用户测试当前旧包。

## 完成与停止

本批完成=Shared D事实/诊断边界明确、实际consumer差分通过、必要安全语义保留、成本口径可核证。P13a-F02整体仍有GW子项，不以局部完成销整个finding。

真正需要新Design、改变普通建筑资格/UNKNOWN策略、扩大缓存/事件架构、持久schema、替换公共writer时停止对应路径。其它finding不因本批一并授权。

用户需要决定：无新增Gameplay决策。
用户需要测试：本轮无；实施后至多上述一次最小功能对照，沿既有部署门禁。
Codex下一步：本地完成后按现行安全门禁处理测试部署；等待一次最小实机，不扩大其它finding或B168调查。
