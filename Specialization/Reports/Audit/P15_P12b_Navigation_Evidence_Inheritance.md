# P15/P12b — 当前导航、历史证据与测试继承

独立审计 IA20261007 / W21；基线 `77e09471f5d2ac8b3370dd2d85298f2530237dfc`。只读核证；没有修文档、改hash、重新看截图/运行包或新增测试。slice覆盖完成不是全部历史/原生行为PASS。

## 结论

当前Authority/CURRENT→具体切片/停止点的路由清楚，重要反证仍从活动入口可达，测试导航没有将local/部署MATCH扩大成nativePASS。旧阶段文字有维护问题，但不构成新授权、当前实现全部失败或性能专项仍阻塞的证据。

新增 **IA-P15-F01 LOW / DEFER**：Design阅读导航的当前Spec/Culture版本标签过时；实际链接指当前来源，没有错选规则。其余旧派工/索引问题沿IA-P01-F04/F05/Q02/Q03/Q04补证，保持原timing，不按每条旧文字另立finding。

## 活动入口与有效限制

| 路径 | 所核可达性／角色 |
|---|---|
| [Architecture入口](../../Architecture/README.md)→[主说明](../../Architecture/Specialization_v0.1_Architecture.md) | 当前结构、target/current区别、真实CURRENT/Authority；Batch D1与P0-D1已明分，不要求顺序读完历史 |
| [v2分类](../../Architecture/v2/README.md)→现行Shared/Network/直接计划 | 基础合同不等于当年进度仍活动；显式权威/授权由CURRENT，旧考古不能当当前模块清单 |
| [技术索引](../Technical/README.md)→丢史/事件反证 | 不从名字、单独坐标、当前区域猜旧身份；B105 firstPublish不是事务结束，B106/B103等限定原生路径不扩大所有ownership |
| 主Architecture性能约束→[B129结项](../Technical/Specialization_B129_Event_Memory_Investigation.md)978–986 | 稳定化已收束/剩余归因非阻塞、重开条件可达；Technical索引仍强调B138 trial/rootcauseOPEN，但不会使结项信息丢失 |
| 当前[L2](../../Architecture/v2/P0_L2_Meaning.md)及Technical→[Culture隔离](../Technical/Specialization_B163_Culture_Coexistence_And_Neighborhood_Depth.md) | bits非叠加、PAIR12反例、HD不得接管、normal唯一writer/retired GWA保留；不是只藏在Historical |
| Architecture→[Playtest](../../Architecture/Playtest_Workflow.md) | receipt/source/target/恢复包/pending事务职责可找到；文件链接存在不证明当前外部恢复包可用，沿P14a限制 |
| [Design](../../Design/README.md)→Content/Spec/ChangeLog | 普通阅读/内部正式来源/未来范围明确；较新文件不自动覆盖未取代规则，未来专业不扩v0.1 |
| [Historical](../../Historical/README.md)→[Design历史](../../Historical/Design/README.md) | 归档接受来源仍可有效，D0032 Hybrid D尚为展示依据；冻结原目录相对语境及替代入口明确，不把原件旧路径当active故障 |

没有删除或重新归档独有约束/失败证据；三处未衔接设计边界保持原样。主Architecture的D0032 target baseline有职责，不能为“版本一致”机械改成D0048。GWA虽然列在Start结构，retired明确，不据此判旧正收益还活动。

## 旧文字／新finding

| 内容 | evidence / severity / timing | 反证与影响 |
|---|---|---|
| IA-P15-F01 Design README59标签 | STATIC / LOW / DEFER | 写当前Spec/市政D0047、CultureD0046；Authority/Content/ChangeLog已Spec/CultureD0048。链接实际当前文件；下次导航维护改标签，非Gameplay冲突 |
| IA-P01-F04 E2旧current切片 | 原LOW / DEFER | E2前三行B141待修、B142/下一F1未授权残留；同页18明确先查CURRENT，主结构已列F2，不能据旧句退回进度或新实施 |
| IA-P01-Q04/F05 v2 Culture B165待测 | 原分级/DEFER | Culture_Preparation8/17正确B166限定PASS、B168待办、M/N/UI未授权；不能把九域未全落地等同七域writer全未完成 |
| IA-P01-Q02 Technical性能直链 | 原LOW / DEFER | 缺结项直链但主Architecture95已直达结项；rootcauseOPEN真实，不代表工程门禁未解除，不新长测 |
| IA-P01-Q03 Playtest旧权限文案 | 原LOW / DEFER | W0003明确覆盖旧develop禁部署说明；此次audit仍禁止部署，不因standing permission越界 |

这些陈旧描述是可维护性问题，继续增加专业不会迫使多模块返工；不抢占已证明的公共保存/传播/事实成本问题。

## 当前测试和实机风险预算

[Tests README](../../../DevelopmentTests/README.md)、[Catalog](../../../DevelopmentTests/Test_Catalog.json)、[Validation入口](../../Status/Validation/README.md)都从当前manifest选维护中的测试；旧broad wrappers只是特定历史回归，非默认全部执行。Catalog不是动态全inventory，实际文件或旧PASS数量不代表全实现覆盖。

当前[P0-L3A manifest](../../Workflow/P0-L3A.json)目标仍固定Scientist probe退出/诊断；39LOCAL、186/186部署一致性与nativeUSER_DEFERRED分层正确。当前[L3](../../Architecture/v2/P0_L3_Inspiration.md)/[Backlog](../../Status/Playtest_Backlog.md)明确无需现在测试，未启用Floor、六class/M/N/UI未授权。旧后段完整版测试表不覆盖顶部停止点，本审计也不恢复它。

| 已有证据 | 继承边界 |
|---|---|
| K/L/currentResearch/Industry/Commerce | 只继承相同源码/primitive/ownership与已测场景；B166冷重建人工无图、B142模板不是新holder/N/E/L、B062Science不是新Gold合同 |
| Shared成熟生命周期 | 未变路径local回归及已有具名native范围优先；新增persistence/exit/reference路径才补对应native差异，不重复Probe ON→save→OFF→cold默认OFF仪式 |
| P12规模证据 | 单遍1000城≠多轮warm cache；30,000published queries≠更新负载；syntheticACTIVE/facts不能证明原生同规模合法工作集；D2/B137的实际module局部反证保留 |
| P01-F01/F02 | 当前pointer确选CUL_L4_INSPIRE，但无expected_id独立保护；helper schema子集有已核缺口，checkPASS不代表全部schema/授权/Gameplay |
| P08b-F01 | 39LOCAL的loss test造targetID，不能证明真实Storepayload的会话forget；4ID退出与session生命周期分开，W20已核，不新增同finding或native要求 |

**不因此降低本地错误保护或重写断言。** 历史全runner含已被cutover取代的断言，本次未跑；预期不兼容不能一概报当前regression，也不能改到全绿。原生小数/GPP有效倍率、精确Production归因、themingBalance等仍各自限定开放，非全项目停工理由。

## Action-scoped恢复走读

只读问题：Authority→真实CURRENT→问题相关完整section/object。验收归档：本次停止/测试合同＋实际证据＋受影响状态，接受不授权修复。高风险实施：当前切片直接依赖＋相应fixture/owned/保存路径，含conditional context；不能从checkPASS或历史implementation_authorized=true给本次audit授实现权。

[W0001恢复](../../Workflow/README.md#action-scoped-reading-and-interruption-recovery)仍要求先worktree/HEAD/dirty，区分建议/授权/实施中/local完成/部署/native，必要时才核receipt；blind rehash/reset禁止。该走读验证导航可定位，不是fresh-agent/compaction实验。Audit本身从本ledger/Git source继续，不把正式Status改成审计台账。

## 链接、外部证据与未覆盖

三路review的受限6README/mapping/index129本地路径及ChangeLog106路径存在；29项当前8Content source/ref路径、2Shared pointer定位。父任务另核Design/Historical两层/Architecture两层/Technical六入口的224本地链接及anchor，0失败；这两个口径不同且有重叠，不相加为“全仓通过”。未逐篇核冻结原件内部全部相对links；存在路径不证明source语义/接受范围。

[Legacy mapping](../Proposals/Legacy_Workspace_Relocation.md)与Phase1直接index样例B029-NewGame/B024/B029-Fail映射目录存在，relocation index记4/3/3精确文件名；只读metadata，没有原图内容/字节/hash复验。Phase1旧672bundled/1289historicalunresolved/119local-only及迁移1275等是原记录，不是今天active失败数或重新证实完整性。备份、游戏/HD、日志、DB和存档仍外部，不靠Git HEAD猜live包/存档。

实际读scope：上述入口全文/当前接受与角色段，主Architecture至120/E2前35/CulturePrep当前区/L2具名反证/Playtest全文/B129965–988/丢史前20、CURRENT/Authority/currentmanifest、W0001/W0004/test导航/现有finding及三个mapping样例；其余只机械定位指定links/source_refs。未读全Historical、全部长报告/测试或截图/外部部署包；没有新工具平台、Gameplay测试、rehash或文件修复。

下一P16/P17：基于已保存maps、实证和完整当前四专业矩阵，交叉核HIGH/FIX_NOW/BEFORE_NEXT的真实工作集、共同根因/返工增长面、最小candidate边界及验证要求；关闭被反证解释，列明未执行native/外部项。此时才综合回答“继续增加能力前最值得先处理什么”，不凭severity单排序，也不实施任何修复。
