# B046 — 连续项目排列与非标准速度观测

Build: P0-B-046 / modinfo59 · Architecture: A0100 · Design: D0011 unchanged

## 当前结果

B045用户已明确通过，见[记录](../../Status/Validation/Results/Specialization_B045_User_Result.md)。五档连续排序按用户要求不安排独立验收；顺带在后续项目测试观察即可。当前恢复项目完成链路与非标准速度精度验证，未自行采用取整、改成本或结算。

## 排序：STATIC_CONFIRMED

此状态仅为源码/数据库证据，不是游戏PASS。

本机HD `UI/Replacement/DL_ProductionPanel.lua:610` 按Cost排序，所以五档虽相对递增却被其它项目穿插。未发现Projects的独立排序字段能绕开这个UI排序，不能改Cost来凑顺序。

新增本Mod `UI/CrewProjectOrder.lua`，ReplaceUIScript在HD的150000之后150100加载，include现有DL_ProductionPanel，再包装GetDataHelper。保留现有每条项目的数据/引用（Cost、Disabled、Hash等），只将可见Crew项目按固定Type等级归组插入首个Crew原位置；其它项目之间顺序不变，不注入不存在/不可见项目。通常等同以一级项目位置为组首。此适配针对当前HD面板；未来其它Mod同时替换ProductionPanel可能需要兼容适配，不宣称全UI组合通用。HD原文件未修改，排序不影响生产队列顺序。

## 精度读取：新增只读诊断

`CrewPrecision.lua`包装已有UnitActions.Run，施工确认前后读取目标/成本/进度。原UnitActions.lua及完整结算保持逐字节不变；诊断失败不阻止、不重试原动作，不写Property，不发放/删除单位。临时替换的目标枚举响应会恢复，避免覆盖地图标记回复。

- 仅记录本次加载最近一次Crew确认，临时内存，不回放历史。
- 对同一目标计算observed=after-before，expected=min(原有速度金额,剩余需求)，difference=observed-expected。
- 被拒绝的动作不归为精度测量；完成/切换目标后不能将两个目标的进度相减；读取失败报告unknown。
- Unit actions / sites新增`Read Crew precision`，显示所选城市五个项目的理论成本、原生GetProjectCost、GetProjectProgress、本局各档金额、己方各档Crew总数量及最近一次差值。
- 只读按钮不发送游戏动作。无选中城市时可用本次确认记录中的目标城市；若无该记录则提示选城。此报告与单位tooltip分离，不改变已通过的简洁文案。

## 当前速度证据与未知

D0011原规则：项目成本与投入同速缩放，未定整数取整方式。本机GameSpeeds.CostMultiplier为Online50、Quick67、Standard100、Epic150、Marathon300。UI原生源码通过GetProjectCost取得引擎结果，不暴露内部量化公式；Lua实际施工仍按原有amount×multiplier/100传给AddProgress。

快速67%理论值：

| 档 | 理论项目成本 | 原有公式生产力 |
|---|---:|---:|
| 一 | 187.6 | 167.5 |
| 二 | 308.2 | 281.4 |
| 三 | 549.4 | 502.5 |
| 四 | 737 | 670 |
| 五 | 1005 | 911.2 |

这些是公式计算，不是实机结果。原生GetProjectCost是否取整、AddProgress是否保留半点/其它小数、两侧是否同精度仍USER_GAME_TEST_REQUIRED。不得用项目列表四舍五入显示判定内部机制。小于1e-6的浮点差异暂在报告标“读取相符”，不据此确定引擎任意精度算法；保留原始数字供研究。若确认有限精度需调整设计，单独提交DESIGN_DECISION_REQUIRED，不默默floor/round或改金额。

## LOCAL_SIMULATION_PASS

实际排序模块：混合列表归组、1→5、子集、不改其它项相对顺序、不改变对象字段、幂等。实际观察模块包裹实际消费函数：67%传入167.5，浮点引擎mock观察167.5；故意截整的mock观察167并准确报告差值−0.5；观察失败仍执行原动作一次。实际报告读取成本/数量/差值且不发动作。此前UX、消费、投资、25组速度、SQL内存与语法路径回归通过。该状态仅本地模拟，不等于真实Civ VI通过。

## 当前用户批次

[三步快速速度测试](../../Status/Validation/Cases/B046_Crew_Precision.md)。用现有快速档优先，没有才新建；先读五成本，最低档项目完成两次，选其中一支对剩余需求>200的目标施工并读差值。排序顺便看，不额外截图验收。普通速度重复与其它精度组合不在本轮重新要求。

备份：DevelopmentBackups/Specialization-before-B046-project-precision。未改UUID、Design、Civ VI配置、HD源码；未启动游戏。
