# B038 文化3人口：小数与倍率复核

Document Owner: Codex
Build: B038 / modinfo49
Result: USER_GAME_TEST_PASS（本局Culture3人口0/1/2专家的半点收益与现有倍率相容范围）

三图city131073 EDINBURGH(TEST)、ACTIVE3、人口3、宜居度-1，last audit/live人数一致，状态READY。

|时间|专家数|expected/carrier|原生city:GetYield文化|右下角面板文化|
|---|---|---|---|---|
|12.45.14|0|0/0|2.609375|3.9|
|12.45.19|1|1.5/1.5|6.66015625|6.6|
|12.45.24|2|3/3|10.7109375|8|

每步原生增量均4.05078125，两人总增加8.1015625。使用精确Fraction复算，差值为1037/256，避免十进制显示舍入误判。面板零人/两人值再次滞后，不能用3.9/8替代原生值计算。

只读当前DebugGameplay.sqlite：Happinesses HAPPINESS_DISPLEASED覆盖宜居度-2..-1，NonFoodYieldModifier=-10。截图-1与该范围一致。原生District_CitizenYieldChanges Theater为2文化，Building_CitizenYieldChanges Amphitheater等每层建筑可加1；数据库定义不单独证明本城具体建筑清单，但原有每专家3文化与本次增量相容。

按原有每专家3文化加Lv3人口项0.5×3=1.5，合4.5，再经-10%得4.05；观测误差仅0.00078125。若人口项1.5被截成1，在相同原有3与倍率下应3.6而非4.05；若0.5系数被截为0，则应2.7。本次不支持丢失0.5，也不支持先整数截断再参与倍率。两专家原有6+人口3，共9，再×0.9=8.1，吻合8.1015625。

不能从截图完全排除所有其它产出/地块变化，不过两次稳定等增量、已知宜居度规则及配置一致，支持本场景原生0.5路线按预期工作。该PASS不证明所有城市/其它倍率组合、精确归属到某栋实际建筑，也不代表引擎源码级证明。

读数为668/256、1705/256、2742/256，提示当前原生Getter有1/256粒度的数值表示/中间计算精度。本次不足以确定floor/round/ceil、在哪一层发生量化，或所有API的通用精度；不把这项推论写成新的取整Design规则。

用户表示未来可以考虑系数1，但明确现在保持0.5。D0010和运行SQL/代码不变；系数1仅为未采纳备选，不标ACCEPTED、不发起设计改动。无需为本次读数把收益翻倍。

三张原图见../Evidence/B038-Culture/manifest.json；算术见Specialization_B038_Culture_Calculation.json。无需追加同场景测试。既往B029固定平坦收益路径的小数失败独立保留；不能因为本per-population路径通过就抹去旧失败。
