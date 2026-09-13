# Specialization P0 Status

Document Owner: Codex
Status Revision: S0117
Implementation Build: P0-B-051 / modinfo67
Architecture Revision Reviewed: A0112
Design Revision Reviewed: D0014
Latest Accepted Design Revision: D0014
Design Sync State: SYNCED_WITH_LIMITATIONS
Work State: PHASE1_MIGRATION_COMPLETE_AWAITING_USER_REVIEW

## CURRENT AUTHORITATIVE STATE

本轮仅迁移项目与适配测试路径，Mod与Accepted Design字节不变，旧游戏运行包未覆盖。当前四专业Lv1–3主体、科研/文化IV专家百分比、科研/工业IV固定复制、投资与Crew已有运行实现；不是“全部P0仍只读”。整体v0.1未完成，不给虚构完成百分比。

当前唯一最小用户批次是B051.67扩展非学院区域复制。尚未收到本细版结果；B051.66用户已确认工业网络4.5P及科研标准区域50%/半点正常，不能要求重测这些成功项。新代理不得从“人工pass”推断未回报的其它case已通过。

## 验证等级

STATIC_CONFIRMED=源码/数据库静态证据；LOCAL_SIMULATION_PASS=本地模拟，均不代表引擎通过。USER_GAME_TEST_REQUIRED=待用户游戏验证；USER_GAME_TEST_PASS/FAIL=用户已实际验证的明确场景。BLOCKED=无法继续而需技术突破/设计决定；DEFERRED只是延后，不是假失败。配置载体正确不等于原生产出正确；截图与口述分别标注。

## 当前实现与验证矩阵

| 模块 | 当前实现 | 已有证据及局限 |
|---|---|---|
| 独立文明、City Property、总督/专家基础接口 | 运行 | A1/A2及新局总督present/established/2–4门槛、实际工作专家按用户确认通过；旧证据见历史快照 |
| 新城完成→身份、正常读档 | CityFlow/B020–21运行 | [B020](Validation/Results/Specialization_B020_User_Result.md)、[B021](Validation/Results/Specialization_B021_User_Result.md) USER_GAME_TEST_PASS，含Cheat同回合完成；不是无历史旧城自动初始化或极端丢写恢复 |
| 移民投资/ACTIVE | 运行至Potential4，单位面板准备/确认 | [B033](Validation/Results/Specialization_B033_User_Result.md)、[B035](Validation/Results/Specialization_B035_User_Result.md)、[B043](Validation/Results/Specialization_B043_User_Result.md)用户证据，含上限拒绝与总督门控；不宣称完整征服继承 |
| Research/Culture/Commerce Lv1 | 自动运行 | [B024](Validation/Results/Specialization_B024_User_Result.md)用户通过；新城、建筑、多个专家与不更改既有专业按回报范围 |
| Industry Lv1 | 自动Base相邻专家支持 | [B036更正](Validation/Results/Specialization_B036_User_Confirmation.md)用户确认通过：额外2P是原生工业专家基础，不应扣掉 |
| 共同Lv2住房、基础GPP | 自动运行 | [住房](Validation/Results/Specialization_B034_User_Result.md)、[GPP](Validation/Results/Specialization_B035_User_Result.md)用户通过；百分比组合只支持已测情况；已接受延迟见技术索引 |
| 四专业Lv3 | 支持档位、科研/文化人口奖励、工业BaseP/Gold、商业网络类型奖励运行 | [B037修复通过](Validation/Results/Specialization_B037_Promotion_User_Pass.md)、[科研](Validation/Results/Specialization_B038_Population_User_Result.md)、[文化](Validation/Results/Specialization_B038_Culture_User_Result.md)及用户其余正常回报；不擅改0.5 |
| 后台商路/网络拓扑 | 全集后台桥接、direct/recipient分开，无需开UI | [B026历史](Validation/Results/Specialization_B026_User_Result.md)、[D0009 direct接收](Validation/Results/Specialization_B027_User_Result.md)、[删目的城撤销](Validation/Results/Specialization_B031_User_Result.md)通过；自然完成/战争/掠夺等不据此全通过 |
| Crew五项目/单位/目标/确认/限额注入 | 运行，五档、速度整数、排序与UX已落实 | [B043](Validation/Results/Specialization_B043_User_Result.md)、[UX](Validation/Results/Specialization_B045_User_Result.md)、[快速速度澄清](Validation/Results/Specialization_B046_User_Clarification.md)等用户结果；B048用户通过。不能据一级/五级实测外推所有速度全部档位 |
| Research/Culture IV专家百分比 | 运行 | [B048](Validation/Results/Specialization_B048_User_Result.md) USER_GAME_TEST_PASS；不是Culture全部IV完成 |
| Research/Industry IV固定复制 | B051.67运行 | [B051.66结果](Validation/Results/Specialization_B051_66_User_Result.md)工业4.5P/科研标准区域半点通过；旧范围错误FAIL已修，新所有非Campus范围仍USER_GAME_TEST_REQUIRED |
| 标准化模板 / Gold折扣 | 仅研究与离线契约，无原生ledger/折扣 | D0013学习触发已决定；具体允许目录、事件/Property接入和货币隔离未完成 |
| Research/Culture Boost | 离线强度模型，无正式额外Boost | sqrt/Lmax/N去重已定；精度、封顶、触发时序待处理 |
| Culture IV两项Great Work效果 | 未实现 | 分类/时代曲线/倍率仍有设计待决，不能用P.WorkTypes候选表代替批准 |
| Commerce IV汇聚 | 离线计划与实验，无正式汇聚 | Accepted 20%/direct/local basis；条件总量备选尚未采用，防反馈和任意小数未解决 |
| 通用ELIG / Conquest Claim与跨Owner继承 | 离线契约/候选，运行适配不完整 | 固定测试载体与owner锚点仍在；不能重置投资解决征服，也不能把Future全部提到v0.1 |

## 下一任务（只有此队列有效）

1. **先接收B051.67结果。** 使用[现成最小步骤](../Reports/Technical/Specialization_D0014_All_District_Copy.md)：原科研IV城市，不重开局；读报告应覆盖全部非学院区域、预期=已配置且原生科技增加。顺带社区/娱乐等不占人口名额区域，无产出不得阻断；重复读取不持续增长。市中心也已纳入，尤其留意是否引发输入回流。失败只修对应路径，不先扩展新功能。
2. **该项通过且用户允许继续后，下一工程工作包是标准化永久记录。** 从DevelopmentTests/StandardizationLedger.lua与[记录研究](../Reports/Technical/Specialization_Standardization_Storage_Research.md)开始。先从HD Tier导出可审核候选目录，确认允许范围尚未被当前Spec确定的部分；不要默用50条研究样本当已批准名单。再对Industry首次身份一次补录，后续只复核事件所指建筑，保存城市永久记录与初始化标记，验证重复、保存读档、合法获得方式。先不接购买折扣，也不要求先解决全部极端继承问题，但要明确当前支持边界。
3. 后续顺序：Gold-only原生折扣验证→Research/Culture Boost→Great Work→Commerce IV。通用资格/Conquest/正式展示按依赖穿插，均未授权在本次交接轮实施。详见研究报告索引；不是这轮自动执行清单。

## BLOCKED / DESIGN DECISION REQUIRED / DEFERRED

- DESIGN_DECISION_REQUIRED：标准化具体允许建筑目录/特殊组不能仅据HD可分类自动定；学习时机/首次补录已由IND-NET-004解决，**不要再问是否按购买/免费获得记录**。
- DESIGN_DECISION_REQUIRED：Boost量化/封顶，Great Work时代标准/类别/Tourism与theming语义，Claim精确成本等按Spec OPEN保留。Research全非学院范围已由D0014解决，不再列未决；GW范围不是自动同步扩展。
- IMPLEMENTATION_LIMITATION：固定复制仅整数/半点及当前人口/金额范围；跨Owner稳定UID、完整Conquest、旧存档缺史初始化、非参与者周期成本、多玩家/多人一致性未完成。无可靠纯Gameplay端点全集不再是主线BLOCKED。
- DEFERRED：B010原探针未测且用户明确延后；商路自然结束/战争/取消/商人掠夺等尚无完整对应实机证据，不把Cheat删除城市等同所有生命周期通过。不给用户重发旧大批测试。
- NO_FIX / NO_ADDITIONAL_TEST：已接受住房/GPP显示与getter刷新延迟；未来失败须区分载体状态和原生总量，不用该备注掩盖真正未应用。

## 交接与证据

[技术索引](../Reports/Technical/README.md)、[交接审计](../Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md)、[测试运行](../../DevelopmentTests/README.md)。测试原始结果冻结，纠正写新结果。ScreenShots仅待投递，不代替Evidence；用户无图但明确口述可按范围记PASS。

[此前S0115全文](../Historical/DocumentSnapshots/Specialization_P0_Status_before_fresh_agent_handoff.md)保存早期A001–B051矩阵、每批历史及完整证据索引；该文件所有“下一项/待测”均为历史，不与本队列并存。

## Phase 1停止点

本轮等待用户审核迁移报告，不开始Git Phase 2或任何下一项玩法开发。B051.67 USER_GAME_TEST_REQUIRED保持原状，不新增实机要求。旧Evidence、ScreenShots、DevelopmentBackups均为外部只读审计材料；路径映射见../Reports/Proposals/Phase1_External_Materials.md。
