# B163.190 — 六产出实机反馈与两项独立缺口

**USER_GAME_TEST_PASS：本次一城、著作、五项非文化产出的初始配置、所测D变化与W2读数。USER_GAME_TEST_FAIL：Culture追加。社区D覆盖缺口仍存在；完整L2 NOT_PASSED。** 不将符合不完整目录的Food1当作社区完整三层D6通过。

## 五图实际观察

逐张读取2026-10-04 09:29:03、09:29:24、09:30:52、09:31:15、09:31:57五图，均B163.190、T62、Culture ACTIVE4，界面城市Edinburgh(TEST)。城市名只作阅读标签。用户说明图1／2准备和启用、图3学院／商业D增至6、图4圣地D6、图5移入第二件巨作；不从名称反推城市身份或未显示的建筑清单。

| 图／阶段 | W | 每件预期 S／P／G／Food／Faith | 原生宿主小计 S／P／G／Food／Faith | Culture观察 |
|---|---:|---|---|---|
| 1 基线 | 1 | 0／0／0／0／0 | 0／0／0／0／0 | 原生4；Meaning实例0／旧GWA0／HD文化1 |
| 2 启用 | 1 | 1／5／4／1／1 | 1／5／4／1／1；有效差值相同 | 要求追加3，实际4→4、Δ0；Meaning6／旧GWA0／HD文化1 |
| 3 学院／商业D变化 | 1 | 3／5／9／1／1 | 3／5／9／1／1 | 每件预期追加3，原生仍4 |
| 4 圣地D变化 | 1 | 3／5／9／1／3 | 3／5／9／1／3 | 每件预期追加3，原生仍4 |
| 5 第二件著作 | 2 | 3／5／9／1／3 | 6／10／18／2／6 | 预期本城追加6，原生小计8；没有有效W2基线，不能用图1的4制造差值 |

图3–5明确提示原配对因D／馆藏变化失效，“实测差值未确认”，这是正确保护；当前绝对值与所列模型总量一致。界面背后的馆藏图标也显示对应数值，但与报告属于同族原生读数，不作独立结算证据。图2的有效同回合Culture差值足以记录失败，不能以Active实例／配置正确把失败改为PASS。

本次Science1→3、Gold4→9、Faith1→3及W1→2符合单最终值方案；Production5→W2总10与Food1→W2总2符合当前输入。没有拍摄本次END、完整实例明细、主题化／Dialogue倍率或正常回合结算，不新增这些门禁PASS，不派发重复冷加载测试。既有[B162定域清理／END](Specialization_B162_Meaning_Load_Cleanup_Native.md)与[B161 Production](Specialization_B161_Production_Single_Value_Native.md)只继承各自已测范围。

## 两项问题分别处理

**Culture。** 新剧院宿主仍未兑现追加。用户提出HD同类实现干扰假设并条件授权：若移除／合并外部效果有风险，则再次隔离市政／外交文化。[本次只读调查](../../../Reports/Technical/Specialization_B163_Culture_Coexistence_And_Neighborhood_Depth.md#culture共存与外部效果接管风险)确认HD文化直接附普通剧场，没有独立可撤载体；现有模块没有已验证的单项HD撤销入口，接管还影响其它城市／作品与退出、倍率语义。选择临时实施隔离后备，不接管HD。D0046接受的设计仍保留，Culture当前技术实现延期；不是宣布引擎永远不能实现或已证明取最小／首项。B163代码尚未改为五产出，不能声称运行隔离已完成。

**社区。** [B158已记录](Specialization_B158_P0L2C_Five_Yield_Native.md#社区d6与当前目录覆盖是独立问题)的别墅／公交站仍在ordinaryOnly；本次进一步核对豪宅同样未获D资格。ordinary=true并不等于depthEligible=true。当前定义农贸市场T3、别墅T1、公交站T2；若本城三者完整且未掠夺，当前目录只计D3、Food每件1，补齐后才是D6、Food每件3。本次截图未提供逐建筑D明细，不把全部建筑实存／未掠夺状态算作截图已证；缺口有直接源码与数据库证据。Shared绝对D／cap10／Floor／最高单社区规则不改，不以改公式补偿目录。

## 归档与停止

五张已读原图原名原字节移动到ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B163_Final_Yields_20261004_0929/`，manifest关联本记录，**5/5 SHA256 MATCH**。原图和manifest不进Git，收件箱及其它文件保留。

本轮仅截图归档、只读源码／当前内层DB／HD定义核对和文档状态维护，没有新玩法模拟、实机测试、代码修复、部署、游戏启动或其它Mod修改。source／live仍沿B163.190、运行源码`3763677`、既有receipt `B163.190-3763677-playtest.json`／182 MATCH记录；本轮未重新核验外部运行包。main稳定B069.96、Design、永久数据及GC不改。

下一[定域修复计划](../../../Architecture/v2/P0_L2_Meaning.md#下一最小修复--文化隔离与社区d目录)仅落实本模块文化隔离并补三项社区D目录；实施仍待批次授权。不继续HD合并实验、不要求本轮新测试、不自动正式cutover或进L3／M／N／U2。
