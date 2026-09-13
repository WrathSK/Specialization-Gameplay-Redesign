# B030：固定城市收益精度与激活对照

Document Owner: Codex
Build: P0-B-030 / modinfo37
Design: D0009 unchanged
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 结论与证据边界

B029 configured=1.5、实际delta=1不能区分“0.5被忽略/截断”和“HALF实例未激活”。Lua按原值写入0/1属性，Describe只计算配置，不写收益；SQL HALF Amount为字符串0.5，无Lua取整。当前缓存只读查询EFFECT_ADJUST_CITY_YIELD_CHANGE带小数点的Amount仅3条，均为本项目HALF；EFFECT_ADJUST_CITY_YIELD_PER_POPULATION有101条带小数点参数。这是定义证据，不是引擎运行证明，查询范围也不是所有Civ6可能机制。

本机HD UpdateDataBase/HD_Regional_Yields.sql:114–129使用同种固定城市收益效果与二进制属性门控；Gameplay/RegionalYields.lua:228调用Utils.BinaryCompress。UpdateDataBase/DL_Buildings.sql:549、622的工厂使用另一种每人口产出效果，Amount=0.5。不同Effect不能推导相同精度。现有SQL/Lua不是原生C++实现，仍未确定丢失发生在解析、效果计算或激活阶段。

## 最小诊断改动

保留六个Modifier及原有ONE/HALF ID，HALF仅为历史槽位名。第二槽Amount从0.5改为1.5，ONE仍1。按钮先启用ONE，再同时启用第二槽；累计配置为1→2.5，重复仍2.5，OFF全清零。探针标题明确B030及new game required。仅显式用户点击触发，不接网络或高级资格，不自动升级旧档实例。

必须用安装B030之后的新局：GameInfo存在、面板版本正确都不能证明旧存档运行实例已重新建立。测试不需要区域、专家、商路或高级专业。B029旧档和整数/半点结果保持历史，不重写。

在无额外倍率、人口或状态变化且第一步delta=1的同回合条件下：
- 第二步delta=2.5：支持本场景固定小数；不证明任意精度或20%最终收益。
- 第二步delta=2：第二槽有贡献但小数缺失，支持数值精度限制假说；不能由1.5单点推导负数/全部取整规则或精确内部原因。
- 第二步delta=1：没有第二槽可观察贡献，不能判精度；继续查激活/实例。
- 其它/三项不一致：保存读数，不自行修正，检查倍率与上下文。

## 本地验证

DevelopmentTests/test_precision_control.py通过。当前数据库mode=ro打开，复制到内存；仅内存移除旧探针行再应用当前SQL，外键错误集合不增加；六效果只绑定测试Trait。所有Lua语法、XML ID/文件引用及UUID/version37检查通过。实际Lua请求分发、同城STEP/OFF/重复、owner拒绝、缺定义OFF与只读报告验证通过。三种第二槽输出0/1/1.5分别模拟，结果如实报告1/2/2.5；模拟不声称原生小数支持。首次运行测试夹具因前一项清空GameInfo后未重建失败，修正夹具后通过，非运行源码失败。

## 若固定小数不支持的后续研究

保留内部浮点目标，不先取整。每人口小数效果可作为候选，但直接使用会让收益随人口变化；需要证明能够补偿人口且避免残留，不能直接替代固定20%。百分比城市收益会改变计算基数/叠加顺序；跨回合余数发放会改变即时收益、生产与倍率，均不能静默采用。尚未判原设计不可实现，无需本轮设计决定。

本批只派[一个诊断案例](../../Status/Validation/Cases/B030_Precision_Control.md)，等待用户结果。自动Lv1、网络桥、Accepted Design、旧Tests均未改；B010和旧网络撤销/可读性批次继续暂停。
