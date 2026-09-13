# B036：工业 Lv1 专家收益

Document Owner: Codex
Design Reference: D0010 IND-001 / Base adjacency terminology
Implementation: P0-B-036 / modinfo44

## 当前范围

自动实现限定DEV工业专业的每名工业区工作专家 +3 Food、+本工业区 Base Production adjacency 的Production。不改专业/投资账本，不以ACTIVE2门控Lv1。施工队仍待实现，因此本报告不宣称工业Lv1全部能力完成。B035实机测试依用户要求延后，保留已部署四类GPP，之后四类一起验证。

## 数据与应用

和而不同 RealModifierAnalysis.lua:994–998明确区分实际与原始相邻，以Plot:GetAdjacencyYield(ownerID,cityID,districtType,yieldID)取基础相邻。旧UI基础/政策翻倍区分已有用户证据；不能据此宣称新桥接通过。

IndustryRefresh为无控件后台UI，加载后、游戏状态发布/播放完成、回合开始读取本地测试玩家的完整工业区。只传城市ID、区域ID和Base Production数值；值不变不重发，发送错误允许重试，重载重新采样。初始化仅在成功采样前使用SystemUpdateUI重试，空集合成功后不每帧扫描。不要求打开任何面板。不调用district:GetAdjacencyYield或GetYield，不复制政策翻倍、行业额外产出或专家自身产出，避免自反馈。

Gameplay IndustrySupport.Receive重新检查当前归属、完整工业区及ID；实际应用另核对EffectiveFacts中的专业与首个区域锚点。数值只存本次加载内存，可重新采样；不是永久专业事实。新局和正常读档恢复、实际事件时序仍需用户验证。当前只自动采样本地测试玩家，不声称AI/多人通用支持。

9个工业区内部建筑：一个Food3，8个Production权重1..128。原生Building_CitizenYieldChanges按工作专家生效；不新增槽位、住房、GPP，不按人数发城市平坦收益。SQL在HD全局改写之后加载。0基础相邻仍给Food3、Production0。读取失败用无效标记撤销收益；缺失初始化样本显示PENDING。支持整数0..255，小数/负值/超界拒绝并报告，不取整、不clamp、不降级为actual。若实机出现这些值，再研究精确承载，不能改设计。

Read auto Lv1对工业专业显示B036基础相邻、预期/实际载体量及错误；它只读，不触发补发。载体量不是测得的实际专家产出，必须看原生专家提示。

## 验证

STATIC_CONFIRMED：只读当前HD数据库复制到内存执行新SQL；9行专家收益/零槽位住房；全部Lua语法、manifest文件与UUID检查。Make_Hash仅fixture。

LOCAL_SIMULATION_PASS：实际IndustrySupport和后台IndustryRefresh模块贯通，基础5→7→0、actual独立变化、重复刷新、无效值/接口错误撤销与恢复、失去资格/区域未完成撤销、重新初始化采样、只读报告不写入；B035原测试仅内存适配manifest43→44后回归通过，原测试文件未改。原生每专家叠加/倍率不属于模拟证明。

USER_GAME_TEST_REQUIRED：新桥接真实初始化/恢复、原生专家+3F/+BaseP、相邻更新与政策不污染基础。病例见B036。B035未测、延后，不标PASS。
