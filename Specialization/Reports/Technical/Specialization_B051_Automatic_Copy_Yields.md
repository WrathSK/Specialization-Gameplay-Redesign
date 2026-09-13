# B051 自动科研 / 工业IV复制收益

Document Owner: Codex
Design reviewed: D0013 ACCEPTED — RES-004 / IND-004 / IND-NET-003
Implementation: P0-B-051 / modinfo65
Validation: STATIC_CONFIRMED + LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED

## 本轮范围

用户已授权从研究恢复实施。先实现剩余清单A组的两项50%收益，不把标准化、Gold折扣、Boost、Great Work或Commerce IV一并宣称完成。设计原文、五档Crew、投资、既有NetworkBridge及Lv4百分比均未修改。B050已通过的独立实验继续保留，但验收本轮前需Half OFF。

## 计算与刷新

`UI/CopyYieldRefresh.lua`独立InGame context每约1秒读取本地测试玩家完整已完成专业区域的六种`district:GetYield`；无P0/贸易面板打开依赖。不读取城市总产出当复制来源，也不使用Base adjacency代替Actual复制基数。后台采样的变化才提交；读档代际及Gameplay序号确认避免相同数据不重发或请求丢失后永久停留。

`CopyYields.lua`重新核对完整区域集合、城市归属、首个专业区域、当前ACTIVE及NetworkBridge的新鲜来源。科研只计算已明确的四类专业区域中非Campus部分；若存在未确定范围的其它专业区域，报告范围限制并不发放部分小计。工业对当前接收集合内各ACTIVE4工业源取IZ生产力50%的最大值，不求和，不使用Potential或历史来源。

人口/总督/回合/转移事件和既有Lv3/network刷新链会重新核对。源断开、降级及未知数据撤销本项旧载体；数据恢复后按当前事实重建。读档清空派生采样再后台恢复，持久载体不作为计算权威。周期计算只面向参与玩家；读档/转移时额外清理非参与Owner可能继承的本批载体，不建立其专业状态。

展示保留Read Lv4 copy，新增“本项预期 / 已配置 / 原生总量”。读取不触发写入；“已配置”只代表载体状态，不证明引擎已经发放相同增量。没有网络是正常0，不显示调用栈；未知新鲜度与没有网络仍区分。原始失败原因写Lua.log。

## 数值承载与限制

绝对目标为整数或半点时使用80个专属InternalOnly市中心建筑：两类产出各16个正整数位、16个负整数位、8个人口系数位。无市民槽、无住房、无Trait挂接、无区域复制表规则。整数是原生city yield change；半点用B050方案的人口二进制系数及整数补偿。例如3人口需要0.5时为3×0.5−1，4人口为4×0.125；其它整数部分直接加入。先撤旧位再加新位，重复检查不写相同状态；保存投资/模板等永久事实不受影响。

支持目标0..65535.5且为0.5的整数倍；半点分量支持人口1..255。0.25等更细目标明确`COPY_PRECISION_UNSUPPORTED`并清除该项旧值，不取整，不转换为另一设计。非标准专业区域范围、通用多玩家资格、完整征服流程仍未解决。本轮是限定适配，不是所有Mod组合/任意小数完整实现。

城市原生百分比（如宜居度、科研IV专家百分比）继续由引擎计算。半点补偿跨人口自动变化、同回合原生缓存更新时间、源区域是否彻底排除本项城市层输入必须实机确认；数学/mock正确不能替代它们。若出现持续反馈增长，停止扩大部署并回传，不通过取整或任意截顶掩盖。

## 本地验证

`DevelopmentTests/test_b051_copy_yields.py`直接加载真实Lua模块与真实后台脚本：255人口多金额精确恒等式；无面板启动；非相邻跨产出、Campus排除；源max/降级/撤销；人口重算；当前集合变化；unknown范围与精度拒绝；重复/只读不累加；读档同回合相同payload重发；丢失请求重试；非参与Owner清理。结果LOCAL_SIMULATION_PASS（本地模拟，非Civ VI实机）。

只读本机DebugGameplay.sqlite复制到内存执行SQL，检查80建筑、80绑定、系数、无Trait挂载；所有运行Lua语法、XML、modinfo路径与UUID检查通过，STATIC_CONFIRMED（静态证据，非实机）。关键Crew/Investment/NetworkBridge/Lv4Percent/HalfYieldProbe与B051前备份字节相同。

备份：DevelopmentBackups/Specialization-before-B051-copy-yields。未启动游戏、未改变配置。实机仅派[三项小批次](../../Status/Validation/Cases/B051_Automatic_Copy_Yields.md)。用户结果前不得标USER_GAME_TEST_PASS。
