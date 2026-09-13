# GW-002 实现准备与范围确认

Document Owner: Codex
Design: D0022 unchanged
Runtime: B059.83 unchanged

## 已完成调查

GW-002原文：每件合格文化Great Work获得本城专业区域Base Adjacency Yields的50%。GW-003明确分类仅GW001沿用D0020，GW002范围未决独立保留；Architecture还保留GW002遗物未决。用户最新“其他区域”与原文“本城专业区域”是否排除Theater也需明确。不从RES-004全非Campus Actual复制范围平移。

基础读取：Mod/UI/IndustryRefresh.lua:20，Plot:GetAdjacencyYield(pid,cityID,districtType,yieldIndex)，已在工业基础生产力实机验证；扩六yield与其它区域属于新增实机范围。Probe.lua:462同样读取基础；不改用district:GetYield或actual adjacency。完成状态沿用District:IsComplete，特色区用实际type查询基础值。

本机Districts.RequiresPopulation=1包含Campus、Theater、IZ、Commercial、Holy、Harbor、Encampment、Government、Diplomatic及特色替代；Entertainment等不在本机此列表。是否直接采用该名单属于当前待确认范围，不能因读取方便自动决定。

原生承载：MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD + GreatWorkObjectType + YieldType + YieldChange。本机HD_PAGODA_WRITING_FAITH=4，JNR_LIBERAL_ARTS_SCIENCE_GREATWORKOBJECT_WRITING及艺术/音乐Science=2，表明路径不只Culture。此前B055手动七类+2Culture已有测试基础。半点YieldChange未因B059百分比截断而自动判为同语义，须独立最小实测。

## 准备好的实现合同（范围确定后接入）

- 当前已完成合格区域逐yield基础值→本城基础相邻向量。
- 每作品追加向量=0.5×向量，完整浮点计算；作品数只用于诊断理论合计，不把乘作品数的值再写入逐作品Modifier。
- 原生逐类逐yield Modifier按同城当前值更新，先移旧后挂新；只Culture ACTIVE4，同档重复不累加。
- 不从已有巨作/城市产出反推，避免自身循环；不直接补旅游(基础yield没有旅游)。作品数/创建/移动沿用已修复事件收藏链路；区域完成/移除、邻接地块或改良变化、读档/回合触发基础值重建。仅相关变化/回合核对，不每帧全城扫描。
- 如半点无法原生保留，先报告实施限制与可选行为，不自动floor，也不自动改城市补贴而丢失作品倍率。
- 最小后续测试：整数基础相邻/1与2件作品；政策翻倍不改变本项；奇数基础形成0.5尾数及作品移出/总督降级撤销。前三项可在同存档小批次完成。

需要用户确认：作品七类/Relic排除；专业区域是否所有已完成RequiresPopulation且含Theater；原yield保留(学院→Science、工业→Production、商业→Gold等)而非统转Culture。这是范围确认，不重新追问已定50%/BASE/ACTIVE4。
