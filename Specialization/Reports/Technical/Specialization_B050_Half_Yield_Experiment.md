# B050：固定半点收益的独立实验

Document Owner: Codex
Build: P0-B-050 / modinfo64
Design: D0012 unchanged; RES-004 / IND-004 implementation research

## 为什么是新路线

Building_YieldDistrictCopies本机表仍只有三列，无比例参数。ModifierArguments当前Type只有ARGTYPE_IDENTITY、LinearScaleFromDefaultHandicap、ScaleByGameSpeed；没有查到可直接用城市Property作为浮点Amount的本机先例，这不是宣称引擎绝不支持。原固定城市yield Amount1.5的小数失败不能重试后当成功；HD CityYield拼Modifier名称也不是小数接口。

已通过的B038支持每人口Amount0.5。利用二进制可精确表示系数：设人口p=2^v×q，q为奇数，则

`p × 2^(-v-1) - (q-1)/2 = 0.5`。

例如人口3：3×0.5−1=0.5；人口4：4×0.125−0=0.5；人口6：6×0.25−1=0.5。没有按人口任意除法，没有对目标收益floor，分解中的整除只计算整数扣除。即使数学精确，原生两种Effect的计算层、精度、刷新顺序仍必须实机确认。

## 已部署的是实验，不是正式收益

HalfYieldProbe.lua仅显式HALF_ON开启当前测试城市，目标固定+0.5 Science和+0.5 Production。DEV Property SPC_B050_HALF_ENABLED控制启用；单独32个内部city-center建筑分别提供8档每人口系数和8位整数扣除，两类yield独立。Native types为MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION与MODIFIER_SINGLE_CITY_ADJUST_YIELD_CHANGE，后者只接受整数负数。

未开启的城市不加载体；重复ON不叠加、不覆盖ON前基线；Read只读；OFF先撤载体再清开关，异常保留可重试清理。人口变化/回合/读档检查；未知/非参与者撤本实验载体，不改变永久专业记录。若原生城市人口事件时序造成短暂旧组合，必须由测试发现，尚未用于正式生产力。范围1..255为实验支持边界，超限拒绝/撤销，不截断人口。

报告原生GetYield及ON前差值是实测读数；配置公式不是实测。人口变化后旧基线不再比较。城市百分比会影响最终增量，不能无视宜居度；不能把人口变化本身的科技增量算进实验收益。先关、改变人口、再开，得到同人口基线。

面板用已重复的P0投资按钮位置放ON/OFF，用旧GPP读取位置放Read half test，原按钮Hidden保留；单位面板投资/Crew不变。无新增按钮行。B049复制模型/NetworkBridge/投资/Crew/已通过Lv4百分比源码逐字不变。

## 适用边界

若实测通过，只支持本实验范围的固定半点组合候选。实际复制基数若有非整数，50%不一定为半点；Commerce20%也不一定能用此算法。不得据此将任意小数默认量化到0.5。正式集成还需当前基数后台读取、输入变化/撤销、倍率与循环隔离；本轮未接入。

## 本地验证

STATIC_CONFIRMED：本机原生Modifier类型、HD大学0.5每人口先例、SQL内存副本执行，32无Trait绑定内部载体，全部Lua/XML/manifest64检查。LOCAL_SIMULATION_PASS：真实Lua模块全255人口数学精确，ON/repeat/Read/人口/重载/OFF；不是游戏运行通过。test_b050_half_standardization.py同时检查受保护源码未改。

USER_GAME_TEST_REQUIRED：仅两个人口下同城ON/OFF新接口组合；不重复B049复制读取。没有启动游戏。
