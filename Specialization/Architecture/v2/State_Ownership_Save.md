# State Ownership Map + Persistence / Save Contract

Document Owner: Codex
Evidence: STATIC_CONFIRMED (source baseline见README)

## 1. 状态归属全表

Authority指业务事实的真正来源；“Building保存投影”表示引擎会保存建筑，但该建筑不是业务权威。Read会执行的计算与可触发的对账在桥接/事件文档另列。

| State | Authority | Persistent? | Derived? | Writer | Readers | Rebuild source | Save/load behavior | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Specialization Identity | Journal first-completion + Flow一致性 + Binding确认 | City+Game | 否（Flow是持久校验投影） | CityJournal/CityFlow/Binding | EffectiveFacts→全部正式效果 | 不能由现有区域重猜历史 | Load验证三份一致；缺史/冲突停止 | [CityFlowProbe.lua:120](../../../Mod/CityFlowProbe.lua) |
| Potential | foundation potential1 + 已确认投资receipt数 | City投资表 | 值派生；投资事实永久 | InvestmentAction（非ACTIVE写入者） | EffectiveFacts/全部高级能力 | basePotential + count(investments),最多3笔 | pending单独验证；不按Governor降低潜力 | [EffectiveFacts.lua:18](../../../Mod/EffectiveFacts.lua) |
| ACTIVE / Effective Level | Potential + 原生总督资格投影 | 不另保存 | 是 | EffectiveFacts.Read即时返回 | Local/network/targets | 每次读取Flow/投资/RoleFacts | 未知资格返回nil而非猜等级 | [EffectiveFacts.lua:46](../../../Mod/EffectiveFacts.lua) |
| Governor资格 | 引擎Governor及SQL Requirements | 引擎属性投影 | 是 | 原生Modifier写SPC_P0_GOV_* | Probe.CityRoleFacts→EffectiveFacts | 控制标记+present/established/2/3/4要求 | control缺失或属性不一致为UNKNOWN | [Data/GovernorProbe.sql:1](../../../Mod/Data/GovernorProbe.sql) |
| Binding facts | Game binding ledger+City token联合确认 | 是 | 否 | BindingProbe CityBuilt | Journal/Flow/EffectiveFacts | 新城事件分配serial；不可从坐标恢复身份 | 32累计限制；owner/id/x/y绑定，转移不支持 | [BindingProbe.lua:25](../../../Mod/BindingProbe.lua) |
| Completion观察 | 首次观察记录B014；非Identity权威 | City | 诊断证据 | CompletionRecordProbe | 诊断 | 不能证明Mod加载前历史 | 仅绑定有效时记录；既有记录不覆盖 | [CompletionRecordProbe.lua:5](../../../Mod/CompletionRecordProbe.lua) |
| Completion事件历史 | 最近64条观察 | 否 | 诊断 | CompletionProbe | P0Panel | 下一次事件；不供正式恢复 | 每次Context重置 | [CompletionProbe.lua:80](../../../Mod/CompletionProbe.lua) |
| Settler投资记录 | 已确认消耗+receipt / pending协议 | City及Unit | 否 | InvestmentAction | EffectiveFacts/恢复/预览 | 永久成功receipt；不是current unit count | CONSUMED_CONFIRMED可finish；INTENT不猜消耗 | [InvestmentAction.lua:4](../../../Mod/InvestmentAction.lua) |
| Crew action记录 | Player receipt保存不可重复执行意图 | Player及Unit | 否 | UnitActions | 确认去重/人工诊断 | 不自动replay AddProgress | INTENT/GRANT_ATTEMPTED/COMPLETED永留；无自动恢复 | [UnitActions.lua:6](../../../Mod/UnitActions.lua) |
| Standardization learned ledger | 工业城已经合法获得的建筑知识 | City | 否 | Standardization初始化/Queue→Flush | StandardizationDiscount/诊断 | 一次补录+合格建筑事件；旧知识不能仅靠现存建筑重建 | 验证foundation/位置/catalog tier；改变分类需迁移 | [Standardization.lua:122](../../../Mod/Standardization.lua) |
| Trade Route complete snapshot | 后台UI当前逐城GetOutgoingRoutes，经计数/端点完整性验证 | 否 | 是（批准输入adapter的当前样本） | BackgroundRoutes→NetworkSender→NetworkBridge.Receive | 网络及Commerce IV | 初始化/dirty/回合完整读取 | load清空内存并重读；历史事件非事实 | [NetworkBridge.lua:50](../../../Mod/NetworkBridge.lua) |
| Direct sources | 当前Identity+有向source→center商路；首都自身例外 | 否 | 是 | NetworkBridge.derive | ConnectedKinds/National/RecipientSources | 当前city facts+verified routes | 非持久；集合以当前cityID索引 | [NetworkBridge.lua:96](../../../Mod/NetworkBridge.lua) |
| Trade Centers | 原生capital或Commerce Identity | 否 | 是 | NetworkBridge.derive | direct/distribution | GetCapitalCity+EffectiveFacts | 无需商路自造身份；当前非永久UID键 | [NetworkBridge.lua:99](../../../Mod/NetworkBridge.lua) |
| Distribution recipients | center直接接入source集合随outgoing国内route分发 | 否 | 是 | NetworkBridge.derive | National/RecipientSources | 同一完整routes+centers | 接收不递归成为direct source；cityID去重 | [NetworkBridge.lua:115](../../../Mod/NetworkBridge.lua) |
| Research/Culture Strength | max ACTIVE(source),去重recipient数,k×L×sqrt(N) | 否 | 是 | National→NetworkBoost.Plan | Boost adapter | 每次Plan重新National；未共享derived revision | 回合/事件重算；不保存历史强度 | [NetworkBoost.lua:35](../../../Mod/NetworkBoost.lua) |
| Network Boost应用 | FinalRaw最终一次floor(x+0.5) | Building保存投影 | 是 | NetworkBoost Audit | 原生Boost modifier/诊断 | 当前National Plan；capital carrier互斥 | 初始化Clean全局再建；testRaw仅session | [NetworkBoost.lua:26](../../../Mod/NetworkBoost.lua) |
| Commerce III | Commerce ACTIVE≥3+本center直接连接类型 | Building保存投影 | 是 | Lv3Effects | 原生专家收益 | ConnectedKinds；每城重新derive | 读取失败→空wanted；不从已有carrier回推连接 | [Lv3Effects.lua:33](../../../Mod/Lv3Effects.lua) |
| Commerce IV Convergence | direct incoming合格source原生城市总yield最大值×20% floor | Building保存投影 | 是 | CommerceConvergence | 原生城市yield/诊断 | verified routes+EffectiveFacts+source GetYield | load清旧投影；mode默认AUTO；plans先全算再全写 | [CommerceConvergence.lua:9](../../../Mod/CommerceConvergence.lua) |
| Industry网络 / 折扣资格 | recipient source集+最高ACTIVE+模板group并集+原生Gold购买资格 | 样本内存/Building投影 | 是 | StandardizationDiscount/UI DiscountEligibility | 原生折扣/诊断 | RecipientSources+ledger+CanStartCommand | 样本按generation/revision/turn验证；过期wanted为空 | [StandardizationDiscount.lua:49](../../../Mod/StandardizationDiscount.lua) |
| Research/Culture IV专家百分比 | ACTIVE4 + 工作专家数 | Building投影 | 是 | Lv4Percent | 原生yield百分比 | EffectiveFacts + GetWorkerCount | load/worker/governor等重算，旧carrier不作资格 | [Lv4Percent.lua:7](../../../Mod/Lv4Percent.lua) |
| Great Work Dialogue | 当前作品ID/type；creator era（artifact历史era例外） | 样本内存/Building投影 | 是 | DialogueRefresh→Dialogue | 原生文化/旅游modifier；GWA共享collection | UI slots→DB mapping→25%×(D−1) | sample当回合有效；Init清旧；invalid清样本 | [Dialogue.lua:52](../../../Mod/Dialogue.lua) |
| Great Work adjacency | 当前合格作品数+RequiresPopulation完成区域BASE六yield | 样本内存/Building投影 | 是 | DialogueRefresh+GWA.Receive/Audit | 原生每件作品yield | 当前district集合/BASE vector + Dialogue collection | 附带样本独立验证；先Dialogue.Audit可见旧Adj sample | [GreatWorkAdjacency.lua:49](../../../Mod/GreatWorkAdjacency.lua) |
| Housing | ACTIVE≥2 + identity district + 本城tier presence | Building投影 | 是 | Lv2Housing | 原生住房/诊断 | facts + district + tier DB/buildings | load全世界对账；UI同回合延迟另属原生呈现 | [Lv2Housing.lua:12](../../../Mod/Lv2Housing.lua) |
| GPP | ACTIVE≥2 + 实际工作专家数×2 | Building投影 | 是 | Lv2GPP | 原生伟人点百分比体系 | GetWorkerCount；不读已应用GPP反推 | load/worker/dirty重算；不是ChangePointsTotal | [Lv2GPP.lua:27](../../../Mod/Lv2GPP.lua) |
| Lv1常数专家F/P | Identity+first completed district | Building投影 | 是 | ResearchSupport | 原生专家yield | EffectiveFacts/原生district | 错误city记录会session跳过；load重置 | [ResearchSupport.lua:51](../../../Mod/ResearchSupport.lua) |
| Industry Lv1/Lv3 BASE | UI原生BASE P样本+工业Identity/ACTIVE | 样本内存/Building投影 | 是 | IndustrySupport→Lv3Support | 专家3F/baseP及Lv3额外F/Gold | Map plot adjacency；非actual fallback | sample仅districtID/value，无generation/turn/seq合同 | [IndustrySupport.lua:62](../../../Mod/IndustrySupport.lua) |
| Lv3常数top-up | ACTIVE≥3+专业身份 | Building投影 | 是 | Lv3Support | 原生专家yield | EffectiveFacts + 工业ReadBase | 每次全局scan，差异write | [Lv3Support.lua:41](../../../Mod/Lv3Support.lua) |
| Lv3科研/文化人口收益 | ACTIVE≥3 + workers×0.5人口系数 | Building投影 | 是 | Lv3Effects | 原生population yield modifier | EffectiveFacts/workers；引擎人口参与结算 | observed缓存仅诊断，非权威 | [Lv3Effects.lua:30](../../../Mod/Lv3Effects.lua) |
| Copy Yield：Research IV / Industry IV | 当前区域原生GetYield vector + facts/network/pop | 样本内存/Building投影 | 是 | CopyYieldRefresh→CopyYields | 城市科技/生产力 | 科研非Campus全区域total一半；工业最高源P一半 | sample按turn/full district set；不读carrier推导基数 | [CopyYields.lua:34](../../../Mod/CopyYields.lua) |
| Crew project access / queue | 工业Identity→access；引擎queue/project完成→单位 | Building+原生queue/unit | access派生；付费项目进度引擎权威 | CrewProjects / 原生project modifier | 项目UI/引擎 | facts+identity工业区 | Lua只对账access，不replay项目发单位 | [CrewProjects.lua:1](../../../Mod/CrewProjects.lua) |
| Unit action preview / lens | 即时unit/queue/位置+facts，非执行授权 | 否 | 是 | UnitActions/InvestmentAction/UnitTargets + UI | tooltip/lens/confirm（再次原生校验） | 当前原生数据；HD queue helpers | 计划session/当回合有效；移动/变化取消 | [UnitActions.lua:30](../../../Mod/UnitActions.lua) |
| Potential显示 | Gameplay EffectiveFacts返回 | 否 | 是 | CityPotential requests + Gameplay reply | 短标识tooltip | 仅选中城市当前事实 | 2s请求、timeout隐藏；不写Potential | [UI/CityPotential.lua:1](../../../Mod/UI/CityPotential.lua) |
| Diagnostics / performance | 直接Lua调用计数与最近诊断样本 | 否（print外部日志） | 诊断 | PerformanceCounters/各模块/P0Panel | 用户手动报告 | 不用于收益授权 | 28固定指标；UI日志128不同文本/模块；readings无显式cap | [PerformanceCounters.lua:1](../../../Mod/PerformanceCounters.lua) |
| Probe/test controls | 手动显式实验指令，不是Design永久事实 | 见下节细表 | 测试权威仅实验域 | Storage/Envelope/Half/Yield/Purchase/GW/Boost/Commerce | 实验modifier和诊断 | 不得用于正式Identity/Route恢复 | 部分flag跨load保留，不能一概称读档全部OFF | [HalfYieldProbe.lua:11](../../../Mod/HalfYieldProbe.lua) |

## 2. 永久保存合同与异常边界

| Key / identity | 保存理由/介质 | 跨owner与load信任 | Migration / growth |
|---|---|---|---|
| Game `SPC_DEV_BINDING_B013_P{pid}` + City `SPC_DEV_BINDING_B013_TOKEN` | UID分配counter/records + 城市token联合确认；Game RESERVED→City token→Game CONFIRMED三写 | owner/cityID/x/y/serial全核对；partial不修复；load只读审计。不是owner-independent城市注册簿 | schema1；counter≤32且records数=counter，无销毁城市prune。不能直接删记录重用编号；需明确迁移 |
| City `SPC_DEV_CITY_JOURNAL_B015` | 建城时NONE/0，首次合格区域**完成**锁定专业/1；first district/type/turn | token/owner/cityID/位置/health一致才可信；玩家session halted或持久GAP停止提交，不猜旧城 | 不自动修复缺史；永久Identity源，不可因DEV文件名删掉 |
| City `SPC_DEV_CITY_FLOW_B020` | before/target/facts与stage保存提交协议，同时保存Journal副本 | DONE且与Journal相等才SupportFacts；读档恢复许可需先Journal load，未分配城额外检查不存在已完成区域 | BEFORE_PENDING/TARGET_PENDING load保持HELD，不自动补写；三次写非单事务。双份同义事实有顺序依赖 |
| City `SPC_DEV_INVESTMENT_LEDGER_V1` / Unit `SPC_DEV_INVESTMENT_UNIT` | anchor含owner/cityID/token/first/spec，永久最多3笔投资receipt；pending用于防重复消耗 | INTENT不能确定扣除则HELD；CONSUMED_CONFIRMED可完成最后提交；跨owner anchor不再一致，当前不移植 | schema/revision1+n校验；成功集合有上限；不要删pending来“修复” |
| City `SPC_STANDARDIZATION_LEDGER_V1` | learned BuildingType→district/tier/turn/evidence，知识不因建筑失去而忘记 | uid=STD:foundation、坐标、目录tier验证；读供折扣时再确认foundation。首次工业身份补录现存目录内建筑，之后事件增量 | 目录tier/district变化报STD_CATALOG_MIGRATION_REQUIRED；不静默重分组。learned受目录种类数量限制；pending事件至原turn+2 |
| Player `SPC_CREW_ACTION_RECEIPTS_V1` + Unit `SPC_CREW_RESERVED` | 不可逆消耗/注入凭据，INTENT→GRANT_ATTEMPTED→COMPLETED | 当前城市ID/target/amount随receipt存；确认需当前计划；load计划消失，不自动重放不确定AddProgress | 没有schema/owner-independent UID迁移合同；每次成功施工新增token，未见prune/cap；读整表再写整表，P0结构风险非已测泄漏 |
| 引擎City Buildings / queue / Units / GreatWorks | 引擎正常存档对象；成果与carrier都物理存在 | 业务建筑/建造队列/劳动力/作品是输入；SPC收益carrier只是输出。正常load各模块重新比对/部分先Clean再重建 | 不批量删除保存的carrier来猜状态；新旧数据库兼容问题不在本轮变更 |
| City `SPC_P0_GOV_*` | 原生requirement modifier投影；不是永久总督事实 | 以control=1和一致的present/established/req检查读取；未知不当作无总督 | Lua不迁移/直接写资格；引擎重算可存在时序延迟；counter不包含原生内部Property写 |

永久城市ID目前只是**原owner内确认的DEV token**。路线归一化key=`owner:trader|owner:city>owner:city`是快照身份，不能用于继承；Network recipient以当前cityID去重，仅在本玩家当前城市集合等价，不是Design承诺的永久UID合同。

## 3. 隔离继承与历史数据

Gameplay末尾显式清除`CityInheritanceRead / InheritanceShadow / CityInheritance / OnPermanentCityWrite`，三个模块不Start。`Binding.Resolve`的继承分支因此无活动provider。

- Game `SPC_INHERITANCE_SHADOW_V1`（旧字段records/watch/events/sequence/revision）和`SPC_CITY_INHERITANCE_V1`（records）若旧档存在，保留但不作为当前authority、不更新。
- CityInheritanceRead的watch只在旧模块启动时为session内存，不是永久证据。
- 当前不能承诺赠送/征服后uid、journal、flow、投资、模板自动迁移。部分收益模块CityTransfered清除输出，不等于永久成果继承已实现。
- 不处理32-city限制、旧cityID记录、Crew receipts增长；此次只登记。cityID被重用时缓存键可能撞旧状态，不能仅凭坐标认定同城。

## 4. Derived重建与历史cache

| Derived组 | Load来源 / 重建 | 有没有误用旧history | 留存/清理情况 |
|---|---|---|---|
| Routes/topology | UI全量当前route→Gameplay校验；epoch随Start增加 | 未用TradeEvents或AutoRouteProbe端点作正式路线；同session等待重验保留last verified是批准合同 | UI完整替换；formal rows≤128；player bucket随session，detailPage按city积累 |
| ACTIVE | 每次flow+投资+Governor projection | 无历史ACTIVE恢复 | 无共享读缓存；每读深复制/校验上游 |
| Industry BASE | UI每次地区扫描→city/district匹配→sample | 内存sample未持久；但没有turn/epoch/seq，正确性依赖UI主动刷新 | UI sent有live prune，Gameplay samples未有city prune |
| Copy / Discount / Dialogue / GWA | 各自session generation/turn/revision和native set校验 | 不恢复存档sample；旧sample不能跨turn使用，失败清样本 | turn过期可能先撤销再收新样本；这与Route保留lastverified不同 |
| Boost / Commerce / Dialogue / GWA | 初始化可先全世界清旧carrier，再重建 | 不从carrier推回资格/来源 | ready/errors/last在session；部分缓存保留已消失city键，无统一生命周期 |
| 常数Lv1 / Housing / GPP / Lv3 / Lv4 / CrewAccess | load遍历原生城市、EffectiveFacts后差异写 | 无从历史事件恢复当前收益 | errors/observed等pid:cid缓存多数无prune；并非所有模块都是无限事件数组 |
| StandardizationDiscount.applied | 首次读实际carrier得old，之后以应用缓存更新 | 缓存不是模板authority；但以后remove只枚举old，外部新增carrier可能漏收敛 | CityTransfered清applied；普通audit不完整重建old。ARCHITECTURE_MISMATCH（对账合同缺口） |
| Preview/lens/UI | 当前选择、queue、位置、资格；确认再次检查 | 不持久化preview作为扣款权限 | 单计划/pid、单pending；超时有限；readings/error字典需未来prune |

## 5. 残留probe/test状态（不能全部当只读）

| 状态/Key | 真正写入者 | load / 副作用 / 隔离等级 |
|---|---|---|
| `SPC_P0_MARKER` City | Gameplay MARK_CITY | 手动持久marker；不影响身份 |
| `SPC_P0_FIRST_SPEC` / `SPC_P0_FIRST_ELIGIBLE` | 当前只有诊断读，未见本版写入 | 不作为正式专业事实 |
| `SPC_DEV_STORAGE_B012_P{pid}` Game | StorageProbe手动WRITE | 合成固定样例，只空时写，不覆盖冲突 |
| `SPC_DEV_COMPLETION_B014` City | CompletionRecordProbe自动首次完成 | 持久诊断旁路，不驱动Journal；额外写入仍真实存在 |
| `SPC_DEV_ENVELOPE_B019_P{pid}` Game | EnvelopeProbe手动NEXT | 六步有限fixture，load只读；不能混同Flow |
| `SPC_B029_ONE/HALF` Plot | YieldCarrierProbe手动STEP/OFF | 跨load保留直到OFF，实际影响实验yield，未自动关闭 |
| `SPC_B050_HALF_ENABLED` City | HalfYieldProbe手动ON/OFF | 跨load继续自动按人口维护实验carrier；隐藏按钮不等于关闭已保存flag |
| B053 fixture/discount buildings | PurchaseProbe手动 | load全局清OFF |
| B055 GW CITY/OBJECT buildings | GreatWorkProbe手动 | BoostRefresh INIT / Dialogue Init / transfer清理；原生载体可能持久，必须执行初始化 |
| Boost testRaw / Dialogue off,test / GWA off / Commerce mode,testCity | 各Gameplay手动control | session内，重载默认AUTO；初始化/首次采样清旧实验投影 |
| `SPC_CREW_DEV_SPAWN` Player | UnitActions隐藏SPAWN | token集合持久且无cap；只有显式实验，不作正式项目凭据 |
| ConstructionProbe plans | 隐藏DEV prepare/apply | session；Apply可无Crew注入250；ReadSnapshot被正式Crew复用，因此不能整模块删 |
| Qualification/Eligibility probes | 只读诊断许可模型 | 不驱动正式P.IsTestPlayer；名册刷新仅init/load |
| AutoRouteProbe / TradeEvents / CompletionProbe / Stage | Gameplay诊断 | recent事件有32/64界限；AutoRouteProbe按player替换；RouteSignalRevision却是正式dirty输入，不能整模块删 |

## 6. 明确的ARCHITECTURE_MISMATCH

- **AM01 永久城市authority合同未完全实现**：PROG-004/NET-RC-002要求长期城市成果/UID语义；实际owner+cityID严格anchor与32城DEV registry。用户已接受当前self-founded/no-transfer范围，仍是待迁移实现缺口，不是新设计待定。
- **AM02 单一事实入口不单一**：Journal与Flow同时保存first/spec/basePotential，Flow读必须逐次等于Journal；并非可从一个永久原件随时无损重建的纯cache。需要保存迁移设计，不能简单删“重复表”。
- **AM03 参与者成本**：ELIG-004意图非参与者不承担周期专业成本；多个Audit每次遍历所有Players/城市检查/清理carrier。资格读通常被挡住，但全球枚举/Building checks真实存在。生命周期必要清理与周期扫描应分开。
- **AM04 Revision覆盖不足**：NetworkBridge revision只随完整route fingerprint变化；身份/首都/ACTIVE可改变source或强度而revision不动。当前靠即时derive避免完全依赖旧拓扑；不能把它直接当全NetworkState revision来加cache。
- **AM05 applied缓存对账不完整**：见Discount表；仅known applied作为remove全集，偏离“真实事实重建任意派生缓存”的最终目标。
- **AM06 旧标签误导**：BackgroundRoutes/ShadowRouteState的`UI_SHADOW_ONLY`及NetworkBridge“No yields”注释已过时；正式消费者确实使用其已验证输入。批准来源合同不变；这是自描述与实际职责不一致，不是取消adapter授权。

本轮不修复上述差异，不改Design，不恢复隔离模块。
