# B160.187 — 多片不加算、单值与撤销重配的原生结果

用户确认多片不叠加，不再要求区分引擎选择“较早”或“较低”的内部算法。本次证据支持停止使用当前同yield二进制多片编码，并进入单值承载方案的计划；没有授权新实现。完整意义延展／L2 NOT_PASSED。

## 八图实际观察

原图依次为2026-10-03 21:53:35／21:53:44／21:53:53／21:54:02／21:54:14／21:54:16／21:54:32／21:54:52；逐张读取。**图5／6是同一个PAIR12报告的上下部分，图6不是REMAIN2。图8是SINGLE3，不是结束或冷加载。** 全部游戏顶部为T62，左侧Cheat科技／市政73／83不是回合号。

同fixture：Edinburgh(TEST)、player0／City393220，当前完整reference相同；`GREATWORK_QU_YUAN_1` Writing、ID1、`BUILDING_AMPHITHEATER` slot0、themed=false。名称只用于阅读，不充当persistent identity。固定诊断不消费D或更改Floor。

| 图 | 阶段 | 预期／载体配置 | 原生作品Production／相对基线 | 精确owned／native观察 |
|---|---|---:|---:|---|
| 1 | BASELINE | 0／0 | 0／0 | owned0、Meaning实例0 |
| 2 | SINGLE1 | 1／1 | 1／＋1 | owned1；instance12307、flat1 |
| 3 | CLEAR1 | 0／0 | 0／0 | owned0、Meaning实例0；旧收益仍hold |
| 4 | SINGLE2 | 2／2 | 2／＋2 | owned1；instance12314、flat2 |
| 5／6 | PAIR12 | 3／3 | 1／＋1 | owned2；instance12321 flat1、12328 flat2，二者Active=true／本城已核验 |
| 7 | REMAIN2 | 2／2 | 2／＋2 | owned1；仍为12328 flat2，本城已核验；＋1已退出 |
| 8 | SINGLE3 | 3／3 | 3／＋3 | owned1；instance12335 flat3、Active=true；归属诊断UNKNOWN:FORMAT |

前七图所有已观察Meaning／旧GWA Production实例城市UNKNOWN为0，旧GWA Production实例0；右键读取完整。PAIR12两实例均为本城District1048589并各有一个已核验subject，定义分别`SPC_MEANING_PROBE_PRODUCTION_0_WRITING`／`PRODUCTION_1_WRITING`，YieldChange1／2，ScalingFactor=nil。不是缺少＋2实例、配置被写成1或第二片未创建。

图7保留**同一个12328**，不是重新创建一个＋2以掩盖刷新：＋1退出后剩余原生实例的值立即可见为2。图8独立定义`SPC_MEANING_PROBE_PRODUCTION_SINGLE3_WRITING`、YieldChange3、ScalingFactor=nil；原生宿主getter为3，非按配置推算。

## 可确认的技术结论

- **USER_GAME_TEST_PASS（本fixture即时读数）：** 单片1、在旧writer仍hold时清至0、撤销后配置单片2；仅撤1后原健康2实例延续且读数恢复2；独立单值3实际读数3。
- **USER_GAME_TEST_FAIL（当前多片加算）：** 两个本城活动flat1／2不能得到3，本次为1，与[B159](Specialization_B159_Production_Combination_Native.md)及[B158相关反证](Specialization_B158_P0L2C_Five_Yield_Native.md)一致。当前二进制同yield多片不能作为正式Meaning承载。
- **未证明：** 所有yield／所有作品／所有金额都不能叠加；唯一内部选择顺序；正常回合结算、倍率隔离、精准recipient、W变化、全城正式能力及冷加载退出。无需继续追早／低优先算法来阻塞替代方案。

单值3成功不代表已经实施单值目录或正式writer。现B160普通Meaning Parts仍是旧多片编码，固定SINGLE3只供诊断；不把可用原型写成完整L2通过。

## 图8独立的诊断格式边界

图8owner与subject raw均出现：`District: 1048589, Owner: 0, SubType: 1, SubValue: -544493210, City: 393220`。报告本城Meaning实例0／城市UNKNOWN1，**不能解释为没有创建或没有收益**：同一报告明确instance12335、Active=true、flat3及独立原生值3。

直接核对[reader](../../../../Mod/UI/BoostGreatWorkRead.lua:330)：完整District正则的SubValue只接受`%d+`，所以负号被拒。源码明确SubType／SubValue是opaque；SubValue不参与city identity，实际归属仍须player／CityManager／district／parent／完整reference交叉核对。

这是**STATIC_CONFIRMED的reader格式缺口**，不是已证实城市identity失败；本次保持UNKNOWN，不事后重写成已核验。下一授权批次可仅接纳已观测的signed SubValue，保留其它ID非负及全部交叉检查，增加对应定向fixture。未观测的signed SubType或其它对象格式不顺便放宽。本轮不改代码。

## 未覆盖的退出门禁

没有直接END/OFF或启用副本冷加载报告，不能记USER_GAME_TEST_PASS；CLEAR1只是hold内局部撤销，不等于旧writer正常恢复或冷加载清理全部新片。原有[LOCAL证据](Specialization_B160_Production_Reconfiguration_Diagnostic_Local.md)保持其范围。本轮不要求用户继续重复旧实验；直接结束及冷加载可合并到下一获授权单值承载的同一次最小验收。

## 下一最小建议（未实施、待授权）

先仅Production单值承载，复用当前单城可逆门禁：本城每领域独立Floor后合计为每件`each.PRODUCTION`；合法整数0–10，0不建载体，其它值每城至多一个对应金额的carrier／每object一个flat Modifier。不把已乘W的total再赋给每件，不仅将多个原Modifier塞进同一building。其它yield暂不顺带切换。

保留27旧owned的精确清理、旧writer互斥、相同输入零写、同回合真实变化、UNKNOWN、失城／reference／load及失败hold；不会因为单值3成功就停用全城旧GWA。下批顺带补已观测signed SubValue诊断，并用一次短测覆盖真实模型值变化、W与直接退出／启用副本冷加载。精准recipient、倍率、正常结算及其余yield按自身门禁推进，不改Design或擅自正式cutover。详细manifest与实施须另获用户授权。

## 归档与运行边界

八张原图原名原字节移至ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B160_P0L2C_Reconfiguration_20261003_2153/`，manifest关联本结果，8/8 SHA256 MATCH；图片与manifest均不进Git；仅移动这八张原图，收件目录和.DS_Store保留。

source/live沿既有B160.187／modinfo187、source `83e191854983089a968629aafc3f7ff05a6aad11`及receipt `B160.187-83e1918-playtest.json` DEVELOP_ACTIVE记录。本轮未重核外部运行包或进程、不部署、不启动游戏；只归档及更新原生结果／Status／当前切片／已审阅导航hash。Mod、测试、Design、永久状态、GC、main及冻结结果不变；没有新Gameplay模拟／回归。
