# 投资提交后的定域更新：修复计划

Date: 2026-10-08。State: **PLANNED_NOT_AUTHORIZED**。
评估baseline：develop `c4b5b85`，clean／origin同步；source/live B171.198。本轮只评估与写计划，不实施、不部署、不修改当前任务或Design。

## 排序与本批问题

[最终审计顺序3](../Audit/P16b_P17_Final_Audit.md#建议处理顺序按返工增长和真实依赖排序)为 **IA-P13a-F03 / MEDIUM / FIX_BEFORE_NEXT_PROFESSION**：提交后的consumer名单与更新范围散落，多模块各自player-wide遍历。每加能力继续复制会扩大未来修改面。

B169保存层修复、B170 Shared D正常/详细分离已完成限定验收；P13a-F02全定义presence和GW动态槽位仍开放，不假装已全部解决。本计划选择顺序3的可靠提交传播切片，不把剩余扫描打包一起改。

最小垂直组合：**真实移民投资提交 → 本城Lv2住房／工作专家GPP刷新**。不能只优化P0面板DEV投资；正常单位面板经过UnitActions.Run同样调用InvestmentAction.Confirm，两个入口都需覆盖。其它消费者和全国Network先保留既有范围。

## 已核现状及依赖

| 入口/模块 | 实际职责与限制 |
|---|---|
| Gameplay：UNIT_ACTIONS_READ/PREPARE/CONFIRM返回后 | 三种动作共用手列刷新链；真实移民投资及施工队操作共用此入口，不能把所有单位操作当投资 |
| Gameplay：INVEST_PREPARE/CONFIRM返回后 | 另列同类consumer；Prepare/拒绝也刷新，不能未证明就全部删除兜底 |
| Gameplay：LV2_GPP_DIRTY | UI晚到事实＋WorkerOnly/FactsChanged筛选；本批只记录合同，保持原调用与筛选 |
| InvestmentAction.Confirm | INTENT→单位消耗确认→最终receipt写/readback；目前只返回展示字符串，没有可靠机器提交结果 |
| UnitActions.Run | 移民Confirm转交InvestmentAction，但pcall/提示整理只保存一个返回值；施工队另有不可逆事务，不能类推 |
| Lv2Housing／Lv2GPP.Audit | RuntimeWork.Player只筛player；循环访问该玩家所有城市，虽可靠投资只影响一城 |
| RuntimeWork.New／SpecialistSupport.Anchor | batch.Facts是单Audit内缓存；Districts首次建立全player区域索引。缩小城市访问不自动消除此区域遍历 |

精确证据：[传播/接入审计](../Audit/P05b_P16a_Module_Extensibility.md#传播接入真正会随能力数量扩大的名单)、[跨Context边界](../Audit/P09b_Propagation_Boundaries.md)。源码在Mod/Gameplay.lua、InvestmentAction.lua、UnitActions.lua、RuntimeWork.lua、Lv2Housing.lua、Lv2GPP.lua、SpecialistSupport.lua。

## 最小实现边界（待授权）

### 1. 提交结果不从文字解析

InvestmentAction保持原展示字符串兼容，增加一个具名第二返回值，明确区分可靠新提交、可靠已提交／无新提交、不确定／部分失败；只带本次原因、player、可靠city reference/binding与必要提交证据，不建持久字段或会话历史。

新提交只能依据最终receipt成功readback及当前身份事实；不能以消耗移民成功、函数返回、文字包含INVESTED或请求原本类型代替。若提交完成但后续报告生成失败，要依实际可证提交状态分类；若证据不足，UNKNOWN。不得为了得到简洁结果改变Store写/readback或永久语义。

UnitActions在移民路径保留这一结果穿过pcall及输出整理；其它单位类型不伪造投资结果。不修改施工队grant、进度注入、receipt或不可逆失败策略。

### 2. 一处投资通知合同，两条真实入口接入

在现有Gameplay组合层定义小型具名投资通知入口：cause、可靠target、已提交依赖、两consumer与顺序明确。DEV Confirm及正常移民Confirm使用同一入口，且只在确认最终提交后发目标更新。

记录三条现有中央链的不同职责，但本批不迁移全部名单、不自动发现模块、不新建总线/调度器。Prepare、拒绝、重复Confirm、缺失/矛盾结果和其它UnitActions操作保留既有刷新行为，除非具体回归已证明可以安全收窄；首批不以“没有新提交”为由全面跳过补核。

一次可靠新投资只替换这两consumer在原手列位置的刷新，不再在同一链额外追加第二次调用。原有native事件仍可发生，不能承诺整个操作只更新一次，更不能按城/回合限频屏蔽真变化。

### 3. 两个consumer支持可靠单城scope

Lv2Housing/GPP接受明确单城scope：直接通过owner的GetCities():FindID取对象，确认当前Owner/reference/binding与提交结果一致，再读取各自完整当前事实。不能先遍历全部城市再用if过滤并把计数伪装成本城定位。

无scope、player-only及原native hooks维持原逻辑；UNKNOWN、不可信target或reference变化保留安全fallback/退出，不能把其它owner新同ID城当投资城。定域处理只清/更新本城错误，不抹掉其它城市未解决的错误；每模块仍拥有自己的carrier和撤销路径。

### 4. 失败不扩大为投资重放

两个consumer独立调用/记录失败，一个异常不能阻止另一个执行；未知不能变零或新激活。失败只留下已有定域错误/待后续既有核对，不重试单位消耗或永久receipt，不新增无界队列或重试状态机。

Network及未迁移consumer继续原player/full核对，因全国/跨城依赖不能假装仅影响投资城。foreign/late事实补撤销、失城/return/load、worker-only/mixed cause原合同保持。

### 5. 不共享跨写入旧事实

两consumer仍各自读取当前资格，不把RuntimeWork batch跨消费者写入或跨事件持有。结果table只属于本次调用链，消费后不累积。全player区域索引暂时保留；不借本批替换native区域API或改变SpecialistSupport。

## 预计修改面

实现：Gameplay.lua、InvestmentAction.lua、UnitActions.lua、RuntimeWork.lua、Lv2Housing.lua、Lv2GPP.lua；Probe/modinfo只更新正常build标识。

直接只读合同：CityProgressionStore、EffectiveFacts、SpecialistSupport、NetworkBridge、现有unit/investment UI。若为最小方案必须改这些语义，停止该子路径，说明真实依赖，不扩保存/身份框架。

新增一个实际producer＋两个consumer的定向测试入口；必要Architecture/Status/result/当前manifest与已审hash按现行流程维护。无新长期状态、GC参数、Design或mod资产目录。

## 验证与可核证目标

**L3，限定提交传播/失败风险**；使用实际InvestmentAction＋UnitActions＋真实住房/GPP writer，不能仅用三个假的callback计算次数。复用test_investment_store_bridge、test_settler_investment_executor、住房/GPP相关fixture；旧test_native_investment/test_b135_gpp_scope固定路径/版本只作受控fixture或case来源，不改历史断言取得全绿。

- 投资I→II、本城住房/GPP按当前事实建立；Governor不足时Potential增长，ACTIVE仍按门槛，不错误给收益。
- DEV与正常移民两入口都覆盖；预览／拒绝／重复Confirm保留补核，不重复永久写或单位消耗。
- 同回合连续真实投资、专家/Governor变更保持响应，不使用每城每回合去重。
- getter/setter/readback失败、throw-after-write、部分held、提交后报告异常、reentrant各按可证明结果分流；不伪造成功或重放副作用。
- wrong Owner/token、对象消失/易主、UNKNOWN与对照城隔离；单城错误不清空对照城错误。
- 一个consumer抛错时另一个仍执行；相关native hooks、UI worker-only/late/mixed、foreign撤销、Networksource/receiver路径不回归。
- 8/20/40城单次可靠投资通知，**只统计两个迁移consumer的目标城市处理，从2C到2**；反例/无scope仍按原范围。不把它当整次投资总扫描降幅。

另外分别记录全国区域index、其它consumer/Network扫描、native事件额外调用、事实读取和carrier写次数。RuntimeWork.Districts的player-wide索引仍可能存在；不把外层城市访问下降称全部native读取下降，不换算CPU/内存改善。不跑全历史/stress或要求原生40城长测。

## 最小原生与退出条件

本地通过、另过部署安全门禁后，沿用户已有保存：一次正常移民投资I→II，确认目标住房/工作专家GPP在实际刷新时机生效、对照城正常；不要求新存档或重复冷加载。GPP可能过回合刷新，不能即时未变就判失败。优先与下次功能使用合并；既有Store/B169保存与B170事实证据继承。

完成条件：真实两入口提供可靠typed结果；确认提交后两个consumer能定域且不漏真实变化；失败与UNKNOWN/全国依赖保持；实际数值及writer行为对照通过、访问计数量纲明确。只完成P13a-F03这个投资组合，不宣称三条链/全部消费者已迁移。

下一个专业、完整广播迁移、共享跨writer缓存、Claim/GW回调及Store return次序另行授权。当前不改运行包，不激活新manifest，不分配新build。

用户需要决定：是否授权此独立修复；GPP/Floor设计决定与本批分开。
用户需要测试：本轮无；若实施，仅上述一次投资定域验收，不重做GPP小数系列。
Codex下一步：保存计划并停止，等待用户审核。
