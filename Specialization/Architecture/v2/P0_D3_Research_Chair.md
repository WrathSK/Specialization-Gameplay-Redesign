# P0-D3 学术主持 — B086.113 / modinfo113

Status: IMPLEMENTATION_COMPLETE_AWAITING_USER / LOCAL_SIMULATION_PASS。不是Civ VI实机PASS。
Authority: Research D0031 RES_L4_CHAIR、Shared D0035 ordinary/current eligibility；A0161。Baseline19bbc9c / B085.112（D2用户整体PASS）。本批已获用户“授权实施”，不进入下一批。

## 用户可见结果

Research Potential4 / ACTIVE4时，W名正在工作科研专家使本城每座合格普通学院T1–4建筑各增加W基础科技。三名专家、图书馆＋大学：每栋+3，合计+6。按建筑逐座计，不按Tier加权、不按D、不受Dcap10截断；T4与T1同样每栋+W。没有floor新规则；W为整数。不是城市/区域平铺，也不是另加专家Science。

免费普通、特色替代、同Tier多栋均按当前ordinary资格；掠夺/未完成/内部载体/Wonder等排除。共享事实、catalog、D公式未改。旧人口8/科研IV48已退效果维持；基础支持、Lv2、P0-C、D1/D2及其它专业字节不改。

## 技术路径及证据门禁

STATIC_CONFIRMED：只读当前DebugGameplay中`MODIFIER_BUILDING_YIELD_CHANGE`为`COLLECTION_OWNER / EFFECT_ADJUST_BUILDING_YIELD_CHANGE`；参数BuildingType/YieldType/Amount。HD自建筑例子包括炼金房/工坊；**区域扩展Database/entertainment.sql:185–209**将BUILDING_JNR_TOURNEY附加到同城其它指定普通建筑，使用HD alias MODIFIER_SINGLE_CITY_ADJUST_BUILDING_YIELD，其collection/effect与原版类型完全相同。这是同城跨建筑投影的具体先例。

HD GOV_SCIENCE虽有Library/University/Data Center目标，但实际ModifierType为PLAYER_CITIES，属全国效果，**没有复用其作用域**。此前初查“学院建筑先例”不等于已确认单城市例，最终实现只取OWNER路径。只读HD DL_Modifiers.sql与DebugGameplay确认alias定义。没有修改外部Mod/DB。

原生当前DB备份到内存、Make_Hash替身后执行新SQL成功：13个当前存在的已审Campus目标、104个内部carrier/对应modifier。SQL不是修改全球Building_YieldChanges：每个carrier只引用一个BuildingType与固定Science，附着在当前城市。无Building_CitizenYieldChanges，非population、非district-flat、非city-flat。static先例足以建立候选，真实native归属/倍率/撤销仍USER_GAME_TEST_REQUIRED，不把本地SQL解码当引擎结算。

## 实际文件与authority

- `ResearchChairModel.lua`：仅逐建筑纯计划。共享逐栋事实不丢失；不读取D数值求收益。
- `ResearchChair.lua`：唯一writer，CurrentSpecializationFacts→共享建筑快照→W→完整配置读→移除差异→创建差异。所有候选及旧配置先完整验证再写。
- `Data/ResearchChair.sql`：13个已审BuildingType的定义投影，加载时只选择实际存在目标。Lua仍按shared ordinary/Tier/location判定，SQL列表不是另一个ordinary authority。特色替代针对实际BuildingType，不把Madrasa当Library写。
- 每目标8个整数bit（1…128），表达0–255专家。当前只读DB所有Campus Building声明槽位之和20（这是静态样本，不是所有可能动态slot证明）。256及以上显式CHAIR_ENCODING_RANGE保留旧配置，不截断W，不创造Design cap；异常扩展环境须另审编码。全已审环境定义104，不在内存保留逐事件历史。
- Gameplay增加启动/三个既有显式action/progression调用/按需dispatch；UI复用当前诊断位“学术主持”，暂隐藏旧商业汇聚按钮但保留代码/效果。版本及RuntimeAudit元数据同步。

## 生命周期与性能

未知ACTIVE/worker/建筑/位置/carrier：保留上次确认值并中文说明。测试发现nil worker可能被两阶段plan当作尚需读取，已在writer显式检查有限非负整数，禁止误当0clear。

确认低于IV、非Research、学院失效、worker0：撤销；单栋掠夺/移除只撤销该栋，修复恢复；每次相同结果no-op。load清除定义/错误缓存并读取当前事实，对原生已存载体差异校正，不新增永久Property/账本/ownership迁移。token/当前学院引用检查沿既有单学院合同，多学院异常保留并诊断。

P0-C先注册负责共享建筑dirty，本模块不再次mark dirty；内部SPC Building通知沿RuntimeWork过滤。普通建筑/区域/资格/worker事件+每玩家每回合一次reconciliation；签名无法城市定域时保留有限安全范围，不声称已经完美单城增量。无Publish/Playback/UI timer/单位移动全扫描，无新UI sample/hover请求/逐事件日志。

本地三consumer(P0-C+D2+D3)同批测试，每城学院两普通建筑、W2：

| 城市 | 建筑快照capture | 专业事实读数 | 区域读数 | 建筑检查 | 初次carrier写入（三consumer） |
|---:|---:|---:|---:|---:|---:|
|1|1|3|1|341|4|
|2|2|6|2|682|8|
|4|4|12|4|1364|16|
|8|8|24|8|2728|32|

fixture只含12个目标（Data Center不在旧P0-A fixture），实际安装DB13目标；该常数不是所有环境承诺。共享缓存仍<=8。10k无关通知新增读取/扫描/写0；UI10k idle发送0；两次手动read各发送1。同回合10k turn通知只首个确认；新回合再确认一次。内部carrier写入不改变D/revision；实际普通建筑事件多个consumer共用一次capture。

## 验证

`DevelopmentTests/test_research_chair.py`：210实际writer配置（7建筑集合×5ACTIVE×6worker数0/1/2/3/20/255）；同Tier/缺低Tier/Dcap反例、两城同BuildingType不同W、独立解码实际SQLprojection、UNKNOWN保留/确认撤销一次、单建筑pillaged/unfinished/remove/restore、特色/未知排除、load/token/编码超限、正常不得隐藏module错误、真实diagnostic/UI dispatch、性能与范围保护。这里只模拟native容器，非引擎。

`test_research_chair_regression.py`：P0-D2/D1/C/B2/B1/A及AV2原生命周期回归通过；仅显式版本/新增文件预期适配，不改历史tests。全部Lua编译、modinfo113/143文件清单、Design/非目标runtime字节保护通过。部署及temporary_playtest事务测试通过。STATIC_CONFIRMED与LOCAL_SIMULATION_PASS，不扩大为实机、全目录、所有HD交互或55GB问题解决。

## 诊断与最小用户测试

左键：`工作科研专家3｜合格学院建筑2｜每栋+3科技｜合计基础科技预期+6｜配置一致`。右键：相关建筑名称、Tier、每栋预期/配置/中文排除原因。配置、数学预期不是原生读数。没有为每次hover加UI↔Gameplay接口。

确认标题B086.113；同一Research ACTIVE IV城，图书馆＋大学等两座已审普通学院建筑，0→1→2名专家，对照原生各建筑Science明细（不是仅城市总量）。每加1专家每栋应+1。增加一座普通建筑后该栋同样+W；便利时降ACTIVE/恢复与保存读档一次确认不叠加。P0-C亦随专家给Science，不能把城市总变化全归于主持。无需手动掠夺；有另一普通学院城可顺手对照不串城，不要求另建世界。

已获W0003测试部署常设授权；正式部署需clean commit/push、进程退出、完整B085恢复点、事务hash核对，另记部署报告。新载体入档后的向后存档兼容不承诺，保留切换前独立存档。完成后等待本批用户验收，不启动学术传统或其它批次。
