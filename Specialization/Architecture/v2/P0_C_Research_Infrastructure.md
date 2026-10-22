# P0-C — 科研基础设施正式切换 / B081.108

Status: COMPLETE / LOCAL_SIMULATION_PASS / USER_GAME_TEST_PASS (overall user acceptance; see scope below).
Authority: A0161, D0035 Shared / Research D0031 RES_L4_INFRA. Baseline B080.107 (4f26050 documents; c56c6de runtime). No Design changes.

## 用户验收更新

用户回复“Pass”，P0-C整体实机验收完成：[证据范围](../../Status/Validation/Results/Specialization_B081_P0C_User_Pass.md)。以下实施交付时的待测文字保留为历史测试要求，不代表仍需重复测试；未单独报告的边界不升级为实机PASS。下一批未授权。

## 用户摘要与环境澄清

用户明确：同城没有多个同一区域，社区例外；本批只处理学院。此前[多学院primitive门禁](P0_C_Primitive_Gate.md)不再阻塞当前环境，不要求用户人为制造多学院测试。共享D最高单区域算法和历史测试不改；正式writer遇到意外多个学院会明确HELD，不静默只给其中一个或发城市平坦补贴。普通/特色单学院的原生Science最终结算仍需一次用户验收，不能把已有Food/Production路径PASS扩大到新Science。

新科研基础设施：当前Research、Potential4、ACTIVE4、有效学院，每名工作科研专家额外D基础Science。四个内部载体的Building_CitizenYieldChanges为1/2/4/8，表示D0..10，无槽位/住房/城市平坦Science/百分比。D和工作专家沿用P0-A权威读取；D0或专家0不保留本项载体；原生其它百分比由引擎结算。

## 精确cutover

- 新唯一writer `ResearchInfrastructure.lua`；四个`BUILDING_SPC_RESEARCH_INFRA_0..3`，SQL在10001020加载，晚于现有HD基础改写和本Mod支持载体。
- 旧48 IDs：Research百分比8、B051 SCIENCE POS16/NEG16/POP8。Types/Buildings保留为无效果tombstone；Modifier/Argument/BuildingModifier附着删除。旧Lv4Percent只处理Culture，旧Copy只处理Production，新writer按精确48清单清理保存实例。
- 新writer先验证完整事实、全部新旧载体可读，再移除旧48/过期新bit，最后创建新bit。清理失败不启用新效果；相同配置不写。原生创建后核对存在、位置和非掠夺状态，不用成功返回值猜测安装成功。创建失败可能保留已完成的部分新bit并明确报错，下一次真实事件/回合恢复；不宣称多bit写入原子事务。
- UNKNOWN facts/ACTIVE/workers/建筑位置/普通建筑Tier/载体状态保留已验证配置；确认ACTIVE降级、身份失效、学院未完成/被掠夺、零D/零专家撤销。load重新读取，不保存新历史或新Property。
- B050半点实验独立保留；诊断若flag开启明确提示混合收益不可作本批验收。未默删实验Production或将实验算入新效果。
- 保留Culture百分比、Industry正式Copy/C2样本运输、Research旧Lv3/Network、B1/B2及其它专业。新科研不请求Copy UI actual yields；共享Copy UI继续服务Industry。

## 文件与职责

|文件|本批变化|
|---|---|
|Mod/ResearchInfrastructure.lua|资格、verified plan、48清理、四bit投影、直接事件与按需诊断|
|Mod/Data/ResearchInfrastructure.sql|四个原生专家Science内部载体|
|Mod/Lv4Percent.lua + Data/Lv4Percent.sql|只退出Research；Culture保持|
|Mod/CopyYields.lua + Data/CopyYields.sql|只退出Science；Production保持|
|Mod/Lv4CopyRead.lua|删除旧Research50%公式/无关本城区域明细，保留工业来源复核|
|Mod/Gameplay.lua|启动/真实专业行动/worker事实桥接；摘要与详情读路由|
|Mod/UI/P0Panel.lua|既有按钮左键摘要、右键学院组成；无新增定时器|
|Mod/Probe.lua、modinfo、UI/RuntimeAudit.lua|B081.108/modinfo108；runtime audit记录正确构建|

## 性能与事件

学院/普通建筑完成、移除、掠夺/修复及城市引用变化使有界D缓存dirty并刷新；worker/governor变化读取已缓存D。自己的BUILDING_SPC写事件不唤醒本writer；既有D服务可能标dirty，下一次需要时重读，不产生自动循环。实际专业/投资行动与现有LV2_GPP_DIRTY接入，不新增UI采样请求。

RuntimeWork保留每玩家每回合一次reconciliation；无Publish/Playback、单位移动、hover或每帧扫描监听。错误表每受影响玩家替换，仅现有城市，不存无限历史；复用city_scan/facts/dc_capture/building_create/remove等固定计数，无逐事件日志。城市枚举仍按事件player范围，不声称每个原生事件都已细化到单城。

|城市数|当前facts读取|D capture|district读取|fixture building checks|
|---:|---:|---:|---:|---:|
|1|1|1|1|220|
|2|2|2|2|440|
|4|4|4|4|880|
|8|8|8|8|1760|

数字来自actual Lua + fixture含全部本批新旧carrier的目录，不是实机建筑数量。10,000次无关事件reads/writes=0；同回合重复turn回调有界；漏掉真实事件下一turn恢复。native modifier engine内部工作量未由本地模型测量。

## 诊断

按钮“科研基础设施”：左键默认六行，仅当前能力；右键同一按钮显示学院建筑组成。每次点击一个读取请求，hover无请求，10k idle不新增发送。默认不拼接住房/GPP/工业报告，不逐行列48内部ID。

```text
P0-B-081.108 | 科研基础设施
科研资格：满足 | Potential=4 / ACTIVE=4
基础设施深度 D=3；工作科研专家=2
预期新增基础科技：6（每名 +3）
载体配置：每名 +3；旧科研四残留：0
配置不是原生实测；请对照城市科技明细。
```

详情含普通建筑normalized Tier、贡献、掠夺、排除原因、cap前后/选中区域。内部技术建筑默认省略，旧载体用残留数概括。UNKNOWN保留提示与B050污染提示不能被精简掉。非科研或ACTIVE不足明确未生效。原生城市总Science还含基础专家/旧III/其它Mod和百分比，不能要求总量等于D×workers。

## 本地验证与证据等级

入口：`DevelopmentTests/test_p0_c.py`、`test_p0_c_regression.py`；Python3.14 + /tmp/spc-b069-python Lupa环境。旧测试原件不改。

- STATIC_CONFIRMED：四新SQL定义；精确48保留ID但无效果附着；所有非目标SQL Modifier/Argument/BuildingModifier逐值保持；Mod作用域allowlist、Design字节、全部Lua compile、modinfo108/引用完整。
- LOCAL_SIMULATION_PASS：100组D×worker×ACTIVE的**实际载体配置**；repeat零写、48清理、删除失败阻止新创建、UNKNOWN保持/确认撤销/load/引用/特色/掠夺修复、正常场景无module errors；意外多学院仅报告不发错误部分结果。
- 1/2/4/8线性读取、10k generic idle；真实Gameplay request摘要/详情无写、真实UI左右键各一次发送及10k idle0。
- A/B/C1/D1/C2/D2/P0-A/B1/B2回归通过；旧Research48输出从历史等价oracle中明确排除，**新测试独立要求其不存在**；其他输出保持，不能用旧效果=新效果作为验收。旧P0-A组合报告已被C替代，独立实际C诊断测试负责新路由。
- 部署transaction安全测试通过（临时目录）：授权/hash/UUID/rollback/精确恢复/备份位于Mods外。不是实际部署完成声明。
- USER_GAME_TEST_REQUIRED：新专家Science在原生引擎的结算/特色替代/正常百分比交互。尚无用户PASS；不宣称55GB内存根因解决。

## 最小用户测试（部署后）

使用原科研测试城，先另存独立slot。ACTIVE IV，点击“科研基础设施”，应看到D、人数、每名配置D、旧残留0；专家0→1→2，读数应对应0/D/2D并对照原生专家科技变化。方便时同城加一座学院建筑观察D；ACTIVE降III后配置0，再恢复IV；保存读档确认旧残留仍0。一次城市流程即可，不要求人工掠夺、多学院或新四套游戏。

用户只需回传摘要/异常现象（若正常，PASS即可）；有不一致再右键提供学院组成。不要默认要求Lua大日志。

## Save / rollback / next gate

本批不是全面Research IV：学术主持/学术传统/新Lv3/Network未实现。B080整包和切换前独立存档为回滚边界，新四Building ID进入保存后不保证降级档兼容。main/stable不变；W0003允许完成并推送后部署，但必须退出/hash/恢复点检查。

下一建议按总计划为P0-D1，先由用户验收本批，再单独审阅/授权具体计划；本轮不开始。当前实际部署状态以Status/部署记录为准。
