# P02a — Shared accepted合同与技术分层

独立审计 IA20261007 / W14；基线 `ac1a2b727e5f840d75c66ed7be439b0bc2171a02`。slice覆盖完成；只有静态合同/实现/断言审阅，不新增LOCAL/native PASS或总审计结论。

## 本slice回答的问题

**共同概念的Gameplay、目标Architecture、实际接口及验证是否各有明确职责，未来新增专业能否正确使用？** 复用已核持久/派生/UNKNOWN和P06/P07/P13；Network完整连接合同另P02b。

所核普通建筑、绝对D、Yield Share、Lv2、Potential/ACTIVE没有新增独立规则冲突。成熟共享路径无需逐专业重做native/save/load。记录一个 **LOW / DEFER** 阅读精度候选：Content README总括“null表示TBD”，但Shared明确no-map/exclusion的gpp=null不是未决。不得据此补自然GPP或改玩法。

## 三层来源与current scope

- [Spec](../../Design/Specialization_v0.1_Design_Spec.md)与[Shared D0045](../../Design/Content/Shared_D0045.json)是accepted Gameplay；[Content索引](../../Design/Content/README.md)明确已纳入内容的公式/文案/映射由JSON维护、未纳入未来规则由Spec保留。Markdown阅读版不是第二套可独立改动authority。
- [D0032适配合同](../../Architecture/v2/D0032_Adaptation.md)描述目标技术责任与业务记录，不证明未来cityKey/modes已落地，不授权实施。较早Owner/TBD假设由后续accepted决定取代。
- [现行Architecture系统说明](../../Architecture/Specialization_v0.1_Architecture.md)与P06/P07源码证据说明当前已落地边界。当前四专业、白板测试文明、单人本地人类；AI未来可启用的Design与当前human-only implementation不冲突。

Shared `implementation_status=NOT_IMPLEMENTED`不能作为整项目live台账：JSON不直接作为Mod运行输入，当前D/Lv2确有实现；新增A–G、专业单位保护、首都未来改制也不能因部分共享服务运行而视为完成。状态与部署查Authority/Status，hash不是语义PASS。

## 共同规则→实际接口

| accepted规则 | 当前直接实现 | 边界 / 结论 |
|---|---|---|
| 普通建筑是正常建造/购买/免费取得的真实普通基础设施；排除Palace/Wonder/institution/internal | [OrdinaryBuildingCatalog](../../../Mod/OrdinaryBuildingCatalog.lua)具名名单/分类，ordinary与depthEligible分开 | 不用InternalOnly=0或Tier>0自动扩scope；未知对象明确不纳入 |
| current资格：未完成/掠夺不贡献或受益；永久模板例外 | [DistrictCompleteness](../../../Mod/DistrictCompleteness.lua)当前完成、pillage、位置与domain核证 | 当前不存在不删除明确永久历史；模板不是D输入 |
| D=每座合格普通building Tier和、cap10，同domain取最高单区域 | D17–51及snapshot/缓存 | 同Tier逐栋计、缺层不补、三层6/四层10，不做Relative Completeness或建满归一化 |
| 一份Gold3，其余Science/Culture/P/Food/Faith1 | [ResearchApplyModel](../../../Mod/ResearchApplyModel.lua)、[MeaningModel](../../../Mod/CultureMeaningModel.lua)明确转换 | 只对使用份额的能力；domain名单/floor位置仍能力独有 |
| II住房：实际专业anchor本体1＋不同合格正Tier各1 | [Lv2Housing](../../../Mod/Lv2Housing.lua)14–35 | B2接受合同明确Tier存在性；不是D或每栋多计，也不取另一更高D区域 |
| II actual worker每class基础GPP2，Culture三类各2 | [Lv2GPP](../../../Mod/Lv2GPP.lua)9–36验证实际SQL/class/worker | 原生基础GPP接受百分比；不是直接发点数，不读D代人数 |
| Potential永久投资；ACTIVE当前资格 | [EffectiveFacts](../../../Mod/EffectiveFacts.lua)46–55与[CurrentFacade](../../../Mod/CurrentSpecializationFacts.lua) | P1＋完成receipt；当前Gov派生，UNKNOWN active=nil；不保存旧ACTIVE/网络/carrier恢复 |
| 已建立机构与能力激活分开 | Adaptation34/89、机构展示目标及当前科研原型 | CurrentIdentity＋当前Potential1..P；旧历史机构不供能力，historical peak不复活当前P。原型不是四专业完整UI |

以上是静态一致性核对，不能写成Shared全部能力/原生/环境覆盖PASS。

## UNKNOWN与轻量接口扩展约束

`CurrentFacade.validity=VERIFIED`与`active=nil / UNKNOWN_GOVERNOR`可同时存在；表示Identity/投资读取成功，不表示所有维度已知。[SpecialistSupport.Anchor](../../../Mod/SpecialistSupport.lua)与当前writers明确拒绝UNKNOWN ACTIVE，保留投影，不当0。

D的VERIFIED/READY表示本实现目录capture成功；可以带ordinary=true/tier=nil的解释行。Housing、Infrastructure、Apply、Meaning各自校需要的行；只拿domains.value不校所需资格，会丢失边界。未来compact API须同时带相关可用性/原因，不能靠简化数字降低分配。补证IA-P13a-F02/优化Q05，不单列新当前defect。

P13a-F01的cache8问题仍MONITOR，合法C_D>8未证；1000城一次遍历cache≤8不能证明正常二次复用。P13a-F02静态definition缓存后仍逐presence与P06a-F03专业保存/词汇耦合保持原timing。本slice不重跑原反例或提高priority凑问题。

Gold3换算目前在能力模型内重复字面值，但现行一致；不为DRY把不同domain集合、资格、取整合成统一Shared公式。ResearchApply按同yield分组后每专家Floor，Meaning逐domain实际yield Floor后相加再乘W，是各自已接受口径。

## A–G与特殊事务不能统一

| 资产类 | accepted owner/生命周期 | 当前接入判断 |
|---|---|---|
| A城市历史 | 跟持久城市，历史/当前使用/增长分别判断；unsupported休眠，各资产例外优先 | 科研K01 OWNER_POLICY_UNRESOLVED是已知适配，模板有实际initialize/restore/reconcile；不统称全实现 |
| B文明历史 | 实际完成文明的Wonder/era信用，城市转移不转移 | N/E未来collector不能从现持Wonder补造 |
| C机构关系 | Commerce信誉随持续Identity，Owner不重置，Identity退出R0 | 不是永久A或所有机构统一年龄，待Commerce独立阶段 |
| D已签合同 | 普通ACTIVE/Identity/route变化不追溯取消，关键城Owner变化按精确合同异常终止 | 不能一律随城休眠或继续付款；当前未落地系统按计划 |
| E进行中 | Dialogue/Study完整1T＋永久提交才成果；中断无半份；Expedition/REALLOCATING各自退出 | 不套Claim自然/Cheat提前完成许可；不把CALLING当成功 |
| F配置/派生 | ACTIVE/Network/carrier重算；商业选择/顺序持久、容量LIFO暂停，Identity/Owner退出清栈 | 不用旧收益快照作authority，与信誉不同 |
| G单位来源 | 完成单位原Owner资产；训练provenance/容量/archive/target事务分别处理；不可敌方capture/转Owner | CanCapture=0不是保护撤退已实现，J1/J2/source归属门禁复用P07c |

REALLOCATING不是NONE，不能first completion/Settler首次建立/Claim；P−1不是`1+receipt count`能表达。配置前目标Owner变更销毁该未完成事务及绑定Team，后续按明确snapshot/Claim例外，不能清其它所有历史。当前无重组动作，不因尚无该schema报当前扣P错误；依赖批次前必须落实。

future原始首都三阶段改制完整记录，明确NOT_V0.1：保持P、无普通5T/Team，Stage3成功才消费原城一次权利。它不增加本轮runtime/context/test依赖。真正未定仅未讨论的单位原Owner消失、完整城市销毁处置、未来未映射领域与具名专业未决；不可捕获/重挂靠/当前Owner计槽已定，不重开TBD。

## 阅读/覆盖候选 — IA-P02a-Q01

**LOW / DEFER。** Content README36“null表示TBD”应按完整对象状态读。Shared270–295的Government/Diplomatic/Neighborhood为NO_NATURAL_GPP_MAPPING，Theater为EXCLUDED_CULTURAL_GP_LOOP。这些是已决定的no-map/exclusion，不是未决。Theater domain表也不替代Spec SHARED-002文化专家三class GPP。当前writers有独立明确映射，未确认误授/漏授，不要求Gameplay决定。

目录覆盖prose是边界/调查线索，不是永远未修问题：当前Catalog已具名补DataCenter/Fair/ArtPublisher，B164修复Neighborhood三项depth名单。不能沿历史coverage句再报这些全部未分类；也不能由几个具名补齐推整个HD/区域扩展已PASS。Tier0普通身份、depth无正值和建筑能力资格继续分开。

## 现有验证的真实覆盖

本轮只审断言，不执行Gameplay tests/新复现：

- P0-A/P0-B2执行真实Catalog/D/facade/Lv2 writers及SQL，native GameInfo/城市/位置/worker/事件/ACTIVE为fixture；可证明所选规则与zero-write/投影guard，不是完整环境。
- B164 Neighborhood测试仅从readonly DB取4精确对象，余目录仍fixture；实际D→Apply/跨城/未知保护有断言，当前归类STATIC/LOCAL并入后续验收，不提升USER_GAME_TEST。
- B099及B136实际Probe资格/当前六属性gate，含非零playerID。foundation/Store有部分stub；不能把它们或数值fixture当资格→E2→所有consumer/native全链。
- B035具名用户百分比组合与B034/80住房有既有人工证据；native立即显示/所有倍率/所有pillage未全面证明，正确继承原范围，不新增重复人测。
- context/helper/schema是W0001完整性，不是Shared Gameplay语义schema。本slicehash/link PASS也只机械证据。

实际readscope：Shared全336行、Content README权威/当前/历史分工；Spec SCOPE/ELIG/TERMS/PROG/SHARED相关完整对象/节；当前Architecture shared/current/derived/presentation及Adaptation直接合同；Catalog/D/current/gate/anchor/Lv2与份额模型；相关P0A/B2/B099/B136/Neighborhood/份额/helper断言及具名结果。复用P06/P07/P13，未通读全专业/历史/DB/截图，也未实施任何统一模型或规则修补。

下一 **P02b共同Network合同与资格方向**：Shared NETWORK_LAYER＋Spec Network完整节、Network当前规则/例外及D0032 network目标合同，对照NetworkInput/Bridge具名derive角色和已核P09publication；专业consumer只在判共享边界所需精确片段读取，不重做所有网络收益或route native验证。分清目标收集、source/receiver/forward、首都self、方向/去重/失效与不可递归；三处未衔接设计边界继续保持。
