# HD文化政策小数收益路径 — P0-D1补充调查

Evidence: STATIC_CONFIRMED（安装SQL + 只读DebugGameplay.sqlite一致），用户报告游戏存在非半点收益；本轮没有新增逐值引擎测量。Mod/HD/Design/运行包均未修改。

## 既有报告

Specialization_Fractional_PerPopulation_Evidence.md已明确每人口小数与平坦城市收益不同，但仅分析B038每人口0.5；B050报告验证3/4人口构造固定半点。Yield_Precision_Backlog登记0.65超出现有Copy编码器范围。未找到对本次四张政策逐条attachment/Amount的既有专项调查。

## 当前本机定义

HD根：Steam/steamapps/workshop/content/289070/2465378070。
主定义：UpdateDataBase/DL_Policies.sql；中文名：Texts/HD_Text_Policies.sql。

| 政策/ID | 已核对的收益实现 | 条件/额外结构 |
|---|---|---|
| 草药提纯 POLICY_HD_HERBAL_MEDICINE | HD_HERBAL_MEDICINE_POP_SCIENCE_MODIFIER：YieldType=SCIENCE、Amount=0.3、MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION | 上层PLAYER_IMPROVEMENTS_ATTACH_MODIFIER筛选农场/种植园/伐木场，子modifier有可见资源owner requirement；不是无条件全国单次0.3。其它Gold/GPP附件不属于此次Science精度结论 |
| 数字孪生 POLICY_HD_DIGITAL_TWIN | 复用HD_DISTANCE_EDUCATION_{DistrictType}_POPULATION_{YieldType}，SCIENCE/CULTURE各Amount=0.2、MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_PER_POPULATION | 按DistrictCorrespondingYieldType_HD中RequiresPopulation=1生成，每域对应城市拥有该区域要求；另有Campus/Theater各100%相邻倍率附件，不能将它们与每人口0.2混为同一效果 |
| 教育学 POLICY_GRAND_OPERA | POP_CULTURE_1/2/3，每个Amount=0.3、同一PLAYER_CITIES每人口Modifier | 每个对应剧院Tier存在要求；HD区域扩展2701747165/Database/theater.sql:361–372添加Tier4同样0.3；缓存有4个附件。不能据旧Changelog的0.2/0.4等版本取代当前SQL |
| 社会统计学 POLICY_SOCIAL_STATISTICS | POPULATION_SCIENCE/CULTURE各Amount=0.7、同一PLAYER_CITIES每人口Modifier | CITY_HAS_4_SPECIALTY_DISTRICTS_REQUIREMENTS实际Requirement Amount=4 |

SQL行参考：草药1420/2000/2408/2741–2743；社会1301/1884/2527–2530；教育1399/1977/2697–2702；数字1736/2290/3265及3963–3998动态生成。

只读缓存核对：草药3个attachment；数字20个（含2个100%相邻）；教育4个；社会2个。记录的是该缓存状态，不宣称当前游戏启用组合、运行中已挂载数或任意HD版本。

## 共同原生效果

MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_PER_POPULATION：COLLECTION_PLAYER_CITIES。
MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION：COLLECTION_OWNER。
两者均为EFFECT_ADJUST_CITY_YIELD_PER_POPULATION。
ModifierArguments直接写十进制Amount；没有为这些0.2/0.3/0.7先变成0.5步长，没有相关政策专属Lua逐回合发放路径。

因此“非0.5参数有HD正式SQL先例”已STATIC_CONFIRMED。精确最终结算误差、舍入时机、任意实数精度仍不能从SQL推断；原GetYield观察到的1/256粒度也不等于引擎全局合同。

## 对上一轮P0-D1门禁结论的修正

应区分：
1. 原生每人口Amount能配置0.2/0.3/0.7：有明确HD先例。
2. 现有CopyYields.Plan只编码整数/半点：这是本Mod编码器边界，不是该Effect只能半点。
3. P0-D1目标是固定城市Science=0.5×BASE总和，并非人口×指定系数。还要解决从目标值到原生配置的映射、人口变化重算、量化、幂等与无重复附着。

上一轮仅凭现有编码器拒绝0.25/0.65就停止技术推进，依据不充分；其反例只证明旧编码器不能直接复用。不能把它们当引擎不支持，也不能把尚未观察到的细分BASE当已发生故障。

下一步应优先调查现有原生per-population路径如何承载固定目标量，而非重新证明Civ VI有没有小数。数学上k=target/pop可抵消人口，但这不是现成实现：动态Amount入口、有限系数目录/等价分解、非二进制系数和人口变化原生结算都需验证。不能为了使用政策路径给P0-D1新增人口乘数，也不能创建无限Modifier/历史表。没有必要现在改变Design或让用户再次批准同一P0-D1范围。

本轮只记录调查，未实现/部署新carrier；P0-D1原生精度技术项仍待验证，但研究方向已由上述真实先例收窄。用户当前无需测试。
