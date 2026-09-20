# P0-C — Research IV 科研基础设施：具体实施计划

Status: PLAN_READY / PLANNED_NOT_AUTHORIZED. User explicitly requests plan first.
Authority: D0035 / Shared D0035; Research D0031 RES_L4_INFRA; A0161 and D0032_Implementation_Plan P0-C. Four-profession v0.1 scope unchanged; Military future only.
Baseline: B080.107/modinfo107, implementation c56c6de, repository39d5b09. P0-A facts and B1/B2 user acceptance inherited; new C effect not implemented/tested. STATIC_CONFIRMED below means source evidence, not engine acceptance.

## 目标与边界

仅把Research IV「科研基础设施」从shadow变成真实基础科技收益：当前Research Identity、Potential IV、ACTIVE IV，合格学院域最高单区域基础设施深度D，每名正在工作的科研专家增加D基础Science。D=min(10,合格普通建筑Tier权重之和)，不是完成百分比；多学院不累加D，按现有shadow统计合格学院的工作专家，不把其它领域专家纳入。不读取建筑Science或相邻actual yield反推D。

例：D3、2名专家 => +6基础Science；D6、2名 => +12；D10、5名 => +50。是额外基础收益，正常原生百分比仍由引擎结算；不是总城市Science保证值。ACTIVE跌破IV、无合格学院/专家0等确认状态撤销；UNKNOWN保留最后已验证结果。Potential和既有投资记录不变。

不实施：学术主持、学术传统、Research III两能力、Research Network重设计、Culture/Industry/Commerce新能力、Military、精度重构、机构UI、保存/易主迁移。旧Research人口Lv3Effects保留至P0-D1；工业Copy、文化Lv4Percent及B1/B2保持现行输出。完成只能称“Research IV科研基础设施已实现”，不是Research IV全部完成。

## 当前源码与精确退出清单

|对象|当前职责|C处理|
|---|---|---|
|ResearchInfrastructureShadow.lua / CurrentSpecializationFacts.lua / DistrictCompleteness.lua|D、当前状态、工作专家与D×workers只读plan|复用计算，建立正式单一writer；保留解释性诊断，实际应用与预期分开|
|Lv4Percent.lua + Data/Lv4Percent.sql|科研/文化每专家5个百分点，8bit各自投影|只退出Research分支；Culture输出保持|
|CopyYields.lua + Data/CopyYields.sql|科研非学院actual总收益50%转Science；工业50%Production网络|只退出Science目标与写入；保留Production和C2/D2协议|
|Gameplay.lua|Start、样本接收、worker/governor/action Audit、手动读|新writer接入真实变更；旧Research入口不再重建|
|Lv4CopyRead.lua / UI/P0Panel.lua|仍显示旧科研50%公式和百分比|对应科研诊断标为已退出/新基础设施读数；工业原有来源读数保留|
|UI/CopyYieldRefresh.lua / SampleLifecycle.lua|Copy共享采样运输|工业仍依赖；不能整体关闭或为C重做生命周期；新科研效果不依赖该UI sample|
|HalfYieldProbe.lua / Data/HalfYieldProbe.sql|B050显式半点实验，Science和Production各+0.5|实施前检查实验flag/载体污染；不将实验算为新效果、不默删工业收益|

正式旧effect allowlist共48：`BUILDING_SPC_LV4_PERCENT_RESEARCH_0..7`（8）；`BUILDING_SPC_B051_SCIENCE_POS_0..15`（16）、`NEG_0..15`（16）、`POP_0..7`（8）。对应SQL Modifier/BuildingModifier附着亦需失活，不能只删Lua入口。保留旧Type/Building ID为可识别tombstone并清理保存中的实例；不使用BUILDING_SPC前缀大清理。

每次切换前全Mod搜索这些ID及动态拼接/启动/Load/Audit/手动按钮；旧载体读取或清理未确认则新效果HELD。正常旧样本延迟不能重新执行cutover。B050的`SPC_B050_HALF_ENABLED`及`BUILDING_SPC_B050_{SCIENCE,PRODUCTION}_{POP,SUB}_0..7`属于独立实验，不混入48正式旧ID；先检查、报告隔离，若已启用不把混合产出当C验收。若需停止其入口须精确说明实验范围，不扩大到工业正式Copy。

## 依赖与primitive门禁

1. 复用P0-A当前事实/目录和B1/B2资格合同；B2用户PASS不扩大为所有目录/掠夺实机PASS。旧hash相同模块按W0001复用，改变输入边界才扩读。
2. 优先采用已存在的`Building_CitizenYieldChanges`原生专家基础yield路径，以小型内部载体表达整数D0..10；不复用旧全城Science百分比，也不直接调用ChangeYield作为每回合奖励。具体carrier数量/ID在实现前锁定，并检查全目录隔离。
3. STATIC_CONFIRMED：ResearchSupport.sql已使用该表给学院专家Food/Production。**尚未确认新Science载体的完整引擎行为**，尤其特色学院/多学院覆盖、掠夺与百分比叠加。因此先做SQL/实际Lua最小prototype和选定城市的native验证准备，不把模拟结果称实机PASS。
4. 如果该primitive无法覆盖已冻结的多学院语义，停止正式cutover并报告技术限制；可调查语义等价路径，不能暗改为仅锚定学院、只加全城固定Science或自动乘/取整。无需现在让用户选择Design。

## 具体实施顺序（获准后）

1. 锁定W0001上下文、48正式旧ID/附着/入口、B050实验隔离与新carrier清单；记录B080整包回滚点。
2. 独立验证原生专家Science数据定义及纯plan；检查特色、多学院和普通目录，所有实际写入均有完整verified输入。
3. 停止Research旧百分比/Copy writer与SQL效果附着，保留旧ID可清理。新writer先确认旧48清空，再启用唯一新投影；旧load、迟到sample、旧手动读不能复活旧效果。Culture百分比/IndustryCopy对照不变。
4. 新正式writer消费D/Identity/Potential/ACTIVE/当前城市引用；事件触发、相同输入零写、未知保留、确认失效撤销一次。无新的永久Property；版本化实现选择/精确清理不得依赖carrier反推历史。
5. 原按需诊断展示D组成、选中学院、工作专家、预期基础Science、实际载体配置、旧48残留数、HELD原因；不把carrier配置标为原生实测。必要时增加本批少量fixed counters，不逐事件日志。
6. 本地完整回归后commit/push，记录LOCAL_SIMULATION_PASS/引擎待验收；按当时W0003状态及退出/恢复点/hash门禁部署。用户一次最小验证后再记USER_GAME_TEST_PASS。不到下一P0批次。

## 事件与性能预算

直接输入：学院/普通建筑完成、移除、掠夺/修复；工作专家变化；总督/ACTIVE；专业投资/Identity；城市当前引用；load。复用已确认事件签名，可靠ID限定玩家/城市；未知签名保守有界fallback。每玩家每回合至多一次reconciliation，仍需事件直接刷新。无Publish/Playback无条件Audit、per-frame扫描、hover请求、重复全国fact capture。缓存依据完整输入而非“刚Audit过”；内部carrier事件忽略，避免自己的写入反复唤醒。新效果不增加Copy request。

## 本地验收与退出条件

- D0/1/3/6/10 × workers0/1/2/5 × ACTIVE0..4；Potential/Identity/引用/多学院最高D与专家总数；免费/特色/同Tier/掠夺/修复/未完成。
- 旧48预置任意组合，首次清理；重复0写；清理失败新效果不启用；加载/旧事件/迟到Copy响应不恢复旧Research效果。48旧SQL附着失活且ID仍可读。
- UNKNOWN事实/worker/建筑/载体读取保留正式收益；确认无资格/零输出准确撤销；epoch不误用旧引用。正常场景无隐藏module error。
- B080 Culture百分比、Industry Copy及B1/B2等非目标完整输出逐值一致；保留历史测试，新的显式delta wrapper只放行本批预期变化。
- 1/2/4/8城读取随规模线性；10k无关通知新增扫描/发送/写入0；同输入重复Audit写入0。
- 全Lua compile、SQL执行/载体与排除目录、modinfo、全runtime依赖回归、部署安全测试。Design字节不变。
- Exit：单writer、旧Research IV两路径不再生效、新基础Science可诊断；没有半迁移或以旧收益补缺的状态。具体primitive实机证据必须单独登记。

## 最小用户测试（未来，不是现在）

复用当前科研测试城，保存独立测试slot：ACTIVE IV，现有D下调专家0→1→2，检查新基础Science增量D/2D与旧48=0；同城方便时建一座普通学院建筑改变D；总督使ACTIVE降到III再恢复；保存重载一次确认旧效果未复活。原生总Science同时受到旧III、基础专家和正常百分比影响，使用诊断拆分，不强求总量等于D×workers。不要求人工无法触发的掠夺/新建四套测试局；特色/多学院未测须注明。

## Rollback / Gate

回滚B080完整包 + 切换前独立存档；不保证新版已保存载体能安全降级。无本轮部署/源码改动/版本提升。

GATE: PLAN_READY，待P0-C明确实施授权。无新的Blocking Design Decision；TS02专家Science/multi-Campus是实施内必须通过的technical gate，不是已通过。若发现能力语义冲突，停并报告，不修改Design。之后只建议按此计划实施P0-C。
