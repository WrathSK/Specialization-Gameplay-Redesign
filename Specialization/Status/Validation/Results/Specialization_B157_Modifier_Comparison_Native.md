# B157.184 — 基线／追加／直接退出的Modifier原生对照

Evidence: USER_GAME_TEST_PASS（本次实例进入／定域退出及S/G读数）；USER_GAME_TEST_FAIL（SINGLE3 Culture追加量）。完整意义延展／L2未通过。

## Fixture与三阶段结果

逐张核对2026-10-03 11:01:13–11:01:57十张截图。均T62、B157.184、玩家0／City393220，完整城市reference不变；GREATWORK_QU_YUAN_1定义基础Culture2，古罗马剧场为BUILDING_AMPHITHEATER，存在且未掠夺。SINGLE3，非主题；追加操作报告显示Culture ACTIVE4／合格1件／旧Dialogue0%。没有进入③100%倍率。

| 图／时间 | 阶段 | 配置S/G/C | 剧场作品实际Culture | 本玩家精确匹配实例／已检查定义 | 关键证据 |
|---|---|---|---:|---|---|
| 1–2，11:01:13／17 | BASELINE | 0/0/0 | 4 | 4／7055 | HD文化与旅游各2（本城与City65536各1）；未见Meaning、旧GWA Writing Culture |
| 3–7，11:01:26／28／35／37／39 | ACTIVE | 1/4/3 | 4 | 7／7076 | HD四项保留；Meaning文化3／金币4／科技1各1，旧GWA Writing Culture未见 |
| 8–10，11:01:50／54／57 | OFF | 0/0/0 | 4 | 5／7083 | Meaning三项退出；HD四项保留；旧GWA Writing Culture＋1重新出现 |

三个Modifier读取报告均为读取完整、未知玩家0／其它玩家跳过0。本次“精确匹配实例”包含已核验的另一座己方城市，**不是本城总实例数**；全局已检查定义数也不是城市扫描次数或收益总数。不用各阶段全局数量差推算其它Mod行为。

图3原有作品reader同时读到Science1.00／Gold4.00／Culture4.00，相对本次基线报告ΔS1／ΔG4／ΔC0；要求ΔC3未满足。整城Culture辅助27.92／Δ0与作品文化未变一致，但不是收益结算证明。两处作品Culture读数都基于GetBuildingYieldFromGreatWorks，不当作两个独立原生接口。城市面板其它总yield不作为独立配对：退出还会正常恢复其它旧GWA收益且面板可能延迟。

## 进入、挂载与退出

| 实例 | owner及唯一subject共同的District／City | 参数 | BASELINE／ACTIVE／OFF |
|---|---|---|---|
| HD_AMPHITHEATER_WRITING_CULTURE_BOOST（本城） | 1114126／393220 | Culture，flat2，scale=nil | 有／有／有 |
| HD同名文化（其它己方城） | 1179663／65536 | Culture，flat2，scale=nil | 有／有／有 |
| HD_AMPHITHEATER_WRITING_TOURISM_BOOST（本城） | 1114126／393220 | YieldType=nil（旅游业效果），flat=nil，scale150 | 有／有／有 |
| HD同名旅游（其它己方城） | 1179663／65536 | YieldType=nil（旅游业效果），flat=nil，scale150 | 有／有／有 |
| SPC_MEANING_PROBE_CULTURE_SINGLE3_WRITING | 1048589／393220 | Culture，flat3，scale=nil | 无／有／无 |
| SPC_MEANING_PROBE_GOLD_3_WRITING | 1048589／393220 | Gold，flat4，scale=nil | 无／有／无 |
| SPC_MEANING_PROBE_SCIENCE_1_WRITING | 1048589／393220 | Science，flat1，scale=nil | 无／有／无 |
| SPC_B060_CULTURE_P1_WRITING（旧GWA） | 1048589／393220 | Culture，flat1，scale=nil | 无／无／有 |

出现的每项均Active=true、subjects=1；所展示唯一subject的玩家／类型／raw与该项owner一致。所选城均“本城已核验”，另一城为“其它城已核验：0/65536”。Meaning三项与旧GWA映射同一District，HD映射另一District；没有区域类型名称证据，不解释SubType／SubValue为建筑类型，不把截图内对象直接命名为剧院／市中心。Active及subject正常**不等于Culture收益到账**。

本次Writing精确筛选范围未出现旧Dialogue Culture项；不能据此宣称其它作品类别／yield／所有城市完整退出。END后旧GWA＋1恢复是正常consumer重算，不是Meaning残留。只确认本次显式同session退出，不扩展为冷加载／失城／全家族原生PASS。

## 定域源码依据及结论

STATIC_CONFIRMED：CultureMeaningProbe的baseline分别hold旧GWA、清16项Meaning owned、旧Dialogue置0；ACTIVE投影现有S1／G4／SINGLE3；END先确认Meaning清除，再释放Dialogue和GWA按当前事实重算。精确路径见[Probe](../../../../Mod/CultureMeaningProbe.lua)、[GWA](../../../../Mod/GreatWorkAdjacency.lua)。未调用HD撤销。

[Meaning SQL](../../../../Mod/Data/CultureMeaningProbe.sql)将三项挂在各自CITY_CENTER隐藏建筑；HD直接来源／已加载DB对应普通AMPHITHEATER建筑，见[建筑来源](../../../Reports/Technical/Specialization_B155_Meaning_Culture_Path.md#古罗马剧场建筑与著作收益来源复核)。定域只读DB复核六个flat定义（HD Culture2、Meaning S1／G4／SINGLE3／SINGLE3_SCALE100、GWA Culture1）的附件、参数完整，owner／subject requirements与stack limits均NULL，flags均0，共用COLLECTION_OWNER／EFFECT_ADJUST_CITY_GREATWORK_YIELD。HD旅游项使用另一旅游业effect，不包含在这六项之中。这是定义证据，不能证明原生组合算法。

- **已一致：** 实例精确进入、旧GWA实验内退出、HD保持、END退出与旧writer正常恢复；S/G所测整数读数增量1／4。
- **失败：** Culture＋3实例正确映射本城且Active=true，作品仍4，未达预期7。已有B155两个候选FAIL保留，不继续用相同流程猜系数。
- **尚不能决定：** 同yield组合规则、宿主区域差异、未展示的资格层或读数／结算边界。没有证据把异常归因漏创建／误归城／旧GWA实验残留，也不能宣布Culture平加永久不可行、取最大／覆盖规则已证实。
- **独立未过门禁：** 精确作品recipient、Dialogue／theming隔离、正常回合结算／冷加载、Production／Food／Faith与正式六yield/all-city cutover。

## 下一最小建议（未实施／未授权）

不要求用户重复本次三阶段或旧长测。先核对已映射District的实际类型与DB附件宿主是否一致：复用已有district对象，只读GetType→GameInfo.Districts及Building.PrereqDistrict；不另建枚举、requirements全库扫描或writer。若准备替换宿主的原生候选，须先明确只改变何种挂载及精确撤销，单独获授权；当前不能凭参数与实例正常就宣布该替代可用。既有市政／外交条件后备仍未正式采用；Design D0042九域与Floor／K／生命周期不变。完整L2、L3/M/N/U2与正式cutover不自动推进。

## 归档与运行边界

10图已逐张查看，原名原字节移入ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B157_Modifier_Comparison_20261003/`，manifest关联本结果，10/10 SHA256 MATCH；原图不进Git。收件箱其它三份非图片资料未动。

source/live沿B157.184／source f75494b、既有receipt `B157.184-f75494b-playtest.json` DEVELOP_ACTIVE引用，本轮未重核外部包。仅证据／状态／计划和对应已审阅hash维护；Mod／Design／GC／永久Property／main未改，无新模拟／玩法回归／部署／游戏启动。前次[映射核验](Specialization_B157_Modifier_Mapping_Native.md)与[本地结果](Specialization_B157_Modifier_Mapping_Local.md)原件不改写。
