# B048 — 科研/文化Lv4专家百分比

Design D0012 unchanged · Architecture A0103 · Build P0-B-048 / modinfo61

## 选择范围

先完成RES-004/CUL-004已明确且共同的组件：Research ACTIVE4每个工作Campus专家+5本城Science百分点，Culture ACTIVE4每个工作Theater专家+5本城Culture百分点。本轮不是完整Lv4实现。Research非Campus Actual基数50%转Science、Culture巨作保值/基础相邻、Industry IV输出、Commerce IV汇聚及Research/Culture网络Boost仍待后续；不把Crew取整规则传播到这些系统。

## 实现 — STATIC_CONFIRMED

源码/数据库证据，不等于实机。当前使用16个隐藏、零基础收益/住房/岗位的市中心Building carrier，以8bit整数记录0–255实际专家人数；每bit挂5×2^bit的MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER，Science/Culture完全分开。amount是百分点，不是直接科技/文化点数，不按城市当前总产出手算返还。

本机DebugGameplay.sqlite：该DynamicModifier是COLLECTION_OWNER/EFFECT_ADJUST_CITY_YIELD_MODIFIER。牛津大学OXFORD_ADDSCIENCEYIELD参数Science/20，百老汇BROADWAY_ADDCULTUREYIELD参数Culture/30；均由BuildingModifiers绑定。采用同一原生效果类型，让引擎处理与其它城市百分比的关系，不由本Mod猜测所有Mod的叠加公式。

Lv4Percent.lua复核当前test-player范围、城市Owner、EffectiveFacts.active==4与potential==4、Identity已完成区域的id/type，人数取区域plot:GetWorkerCount()。不读空岗位，不按Potential单独激活。与既有GPP/Lv3同样保留标准Campus/Theater测试范围，尚非通用replacement/future资格完成。

载体先撤旧再加新，幂等，异常时撤销本项，不动其它能力的建筑/账本。LoadScreenClose/回合/总督/人口与专家事件、完成/移除事件核对；还从既有Lv3Effects.Audit末尾衔接，所以已有后台专家/总督刷新与投资完成链路也会更新，不依赖用户打开P0。

## 报告与布局

P0增加Read Lv4 percent，原两个DEV免费施工按钮隐藏保留定义/回调，单位面板正式施工不动。读取只Describe，不触发收益更新；展示实际人数/生效人数/ACTIVE、配置百分点，明确载体不是实际效果。

UI附加同一城市对应产出的原生GetYieldToolTip（Base CitySupport.lua:329/332 Science、317 Culture使用同一接口），原生明细不由我们重建数学公式。确认cityID，避免切城错配；错误单列，不把空数据显示为PASS。控件设置与引擎明细长度的实际表现需本批观察。没有自动截图/游戏操作。

## LOCAL_SIMULATION_PASS

test_lv4_percent.py执行实际Lua：Research2专家10%、Culture3专家15%、不同城市/产出隔离、ACTIVE4→3→4、0/1/2专家、晋升/专家事件、资格撤销、区域未完成/移除等价缺失、owner变化、数据异常撤销、重复核对/新模块加载不叠加。保留无关建筑。实际SQL在只读DB的内存副本执行，核对16个carrier及原生Modifier字段。全运行Lua/XML/manifest路径检查通过。施工队/投资/原Lv3数值等受保护源码hash一致。

此结果不证明Civ VI载体挂载或实际产出已通过；当前USER_GAME_TEST_REQUIRED，见[三小项](../../Status/Validation/Cases/B048_Lv4_Percent.md)。已有住房/GPP刷新延迟不修复，未把它们的新测试重新派发。

备份：DevelopmentBackups/Specialization-before-B048-lv4-percent。无Design变更、UUID/配置变更，未启动游戏。
