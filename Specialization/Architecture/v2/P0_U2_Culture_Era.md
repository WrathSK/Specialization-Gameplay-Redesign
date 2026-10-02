# P0-U2 — Culture时代馆藏Hybrid D展示准备计划

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED / UI_PROTOTYPE_REQUIRED。
Direction: USER_CONFIRMED_PRESENTATION_DIRECTION，来源D0032；玩法仍Culture D0029。基线和逐批边界见[准备入口](Culture_Preparation.md)。不是重新讨论方向，也不包含机构排版修整。

## 已批准的展示合同

Great Works管理界面的Culture城市附近显示紧凑摘要：`已覆盖N个时代｜缺：X、Y、Z`。不强制N/Total，不拿当前游戏时代/固定8或9作分母；无可靠可收藏全集时显示覆盖数与未确认说明。

Tooltip缓存明细按受支持作品历史时代列本城合格件数、缺失时代、国内其它城市是否有对应作品及可确认来源。真正国内没有与UNKNOWN/未全读取必须区分；长来源分页/截短只影响布局，完整信息仍可读，不假称所有名称能一屏显示。

只整理事实：不移动作品、优化主题、推荐交易价格/最优路线、向AI购买、自动准备Dialogue；国内索引不改变本城X。作品资格/时代直接消费K的共同事实，UI不另写一套分类/Era resolver。

## 已有候选与本轮证据

前期只读调查定位原版`GreatWorksOverview`城市实例/CityName及GreatWorkMoved；HD `GreatWorksSupport`替换Tooltip。这些是[D0031调查候选](../../Historical/Design/Records/Culture_Era_Presentation_D0031.md)，D0032已批准Hybrid D；**不是当前任意HD/UI Mod组合、分辨率和layout实机通过**。本轮没有重读外部游戏UI全集或实现hook。

现有K已提供confirmed本城馆藏、时代/件数及`Domestic`索引/availability/revision。`Summary`缺时代内组成；可在已确认发布时建立小型presentation read model，不能每hover深拷贝完整国内索引或请求Gameplay。

K `OnConfirmed`当前只比较L1所需X等输入，同一时代件数变化/国内来源移动未必触发它；U2必须结合实际馆藏/国内索引revision或补最小呈现变化通知。不能假定L1 callback覆盖全部Tooltip失效条件。

## 建议实施步骤与真实文件依赖

1. UI prototype获授权后，静态核对当次原版/HD支持hook与实际city/building分组；不硬编码每城一行，不覆盖无关Great Works核心逻辑。确定最小城市行摘要/Tooltip attachment。
2. K确认发布→read model（city/current ref、facts epoch/revision、era counts、domestic availability/source版本）→一次缓存文本/布局。不可从旧DialogueModel读时代，也不根据Effect carrier显示覆盖数。
3. open UI读取已有缓存；未就绪显示待确认，由既有后台有界就绪路径补齐。必要首次刷新复用现有collector调度，不另建持续扫描。
4. 创建/移动/交易、confirmed ownership、load/locale/布局尺度变动使对应缓存失效/替换。国内某era来源变化可以使引用该era的提示失效，不因此把所有城市本地X重算或发Gameplay收益。
5. prototype短验收后再润色排版与说明，不在本批实现L/M/N或所有机构UI。

预计最小涉及Great Works UI hook Lua/XML、本地化、K呈现读取/确认通知、modinfo和定向UI fixture。现有城市列表和scroll behavior保留，不建立第二个巨作窗口/自定义完整UI体系；接口不可靠时报告具体hook limitation，不擅自把approved方向换成另一方案。

## 缓存、范围和退出

Gameplay确认事实是唯一来源，UI拥有纯展示缓存；按current reference/epoch及事实版本替换，close/shutdown解除订阅并丢窗口实例，load不保留上session物件引用。source城市移除/易主不能继续显示stale拥有者作为confirmed国内来源。

Tooltip hover只返回缓存文本，零Gameplay request、零槽位读取、零国内全集构造。没有per-frame/per-second馆藏扫描；打开界面、确认变化、需要重新排版才处理相关实例。订阅只注册一次，重开不叠加listener；同内容不重复重建控件。

UNKNOWN同可靠引用可显示“最近确认/待复核”，不能当无作品或国内没有；陌生引用不展示旧city事实。缓存条目数与现有城市/可收藏Era集合有界，不维护每回合历史/操作日志，也不改变GC策略。

## 最小验证、回滚和退出

W0004 L1 UI/低长期state风险；若修改K共享通知，补直接受影响的K/L1/L3事实回归，不默认全历史测试/长测。

本地fixture覆盖：compact摘要、中文长era/city名、同era件数变化、国内有/无/UNKNOWN、两城移动与trade、owner/load/epoch失效、重复open/shutdown、hover零request和零collector调用。真实长名称/字体/tooltip placement仍需实机。

一个最小原生流程：打开有Culture馆藏的Great Works界面→读compact与Tooltip→移作品到国内另一城→再次hover核对双方时代数/来源→重开界面与一次UI scale；冷加载可合并于同批已有测试，不要求再一套截图。接口/layout失败只停止该展示路径，不影响已验Gameplay。

回滚移除本批UI hook/显示资源，保持K共享事实与L/M/N记录；不改作品、不回退或删除永久Gameplay数据。Exit为所测HD布局、刷新/缓存和hover零请求通过；不能将技术prototype验收写为所有缩放最终美术完成。

来源：[已批准方向D0032](../../Historical/Design/Records/Culture_Era_Presentation_D0032.md)、[K事实实际检查点](P0_K_Great_Work_Facts.md#b147174--facts-only-implementation-checkpoint)、[Culture正式work_pool](../../Design/Content/Culture_D0029.json)、[Presentation合同](Presentation_Institution_Carrier_Model.md)。
