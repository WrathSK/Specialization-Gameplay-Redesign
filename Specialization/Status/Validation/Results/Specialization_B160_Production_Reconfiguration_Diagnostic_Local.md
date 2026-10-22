# B160.187 — Production撤销、重配与独立单值诊断

用户明确授权最小诊断实施。本批 STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；B160原生仍 USER_GAME_TEST_REQUIRED。B159单片＋2即时读数通过、双片＋1／＋2失败的原始证据保持，不因此宣布整个接口无叠加或唯一覆盖算法。完整L2 NOT_PASSED，不进行正式Meaning接入。

## 范围与实现

默认关闭、单个本地Culture ACTIVE IV城市、恰好一件当前确认支持的Writing。复用“生产力组合诊断”：左键推进，右键按需读取真实作品Production及精确实例；“结束验证”随时退出。

| 阶段 | 固定预期增量 | 本轮精确操作 |
|---|---:|---|
| BASELINE | 0 | 撤本模块owned，暂停本城旧GWA，Dialogue控制为0% |
| SINGLE1 | 1 | 创建已有＋1 |
| CLEAR1 | 0 | 仅撤＋1；仍保持旧收益暂停，不是END |
| SINGLE2 | 2 | 重新配置已有＋2 |
| PAIR12 | 3 | 清掉上一＋2，再按＋1／＋2创建 |
| REMAIN2 | 2 | 仅撤＋1；健康＋2不删除、不重建，原native实例应延续 |
| SINGLE3 | 3 | 清掉＋2，创建独立flat3单载体 |
| OFF | 0配置 | 清新owned确认后，旧模块按当前事实正常恢复；原生绝对值不能据OFF标签判定归零 |

PAIR12是已知失败对照，仍允许继续REMAIN2观察；其它异常先结束，不擅自换primitive或扩清理。独立＋3与双片具有相同总量，区分单值应用与多片组合；不是正式编码切换。诊断不读D、不动K／逐域Floor后同yield合计／W。

实际修改：

- `Mod/CultureMeaningModel.lua`：追加固定阶段metadata及独立＋3定义；普通Plan／Parts完整保留。Owned从26到27。
- `Mod/CultureMeaningProbe.lua`：固定八态推进、REMAIN2保留＋2、CLEAR1维持hold；按需View／中文阶段与下一步解释。沿原reference／UNKNOWN／loss／load／失败撤销合同，临时session不写永久Property。
- `Mod/Data/CultureMeaningProbe.sql`：只追加一个InternalOnly carrier及七个精确object附件（182→189）；沿原`MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD`／YieldChange=3，无新ScalingFactor或Requirements。原SQL前缀未改；目前只验证单Writing fixture，七附件定义不等于七类原生通过。
- `Mod/UI/BoostGreatWorkRead.lua`：按共享metadata校验新阶段，显式读取含独立＋3的Writing allowlist；CLEAR1／REMAIN2／SINGLE3给短提示。预期／配置／独立getter实测分离，不根据配置推断收益。
- `Mod/Text/TestText.sql`：复用中文／英文hint key说明流程；没有新增key、按钮、XML或icon。
- `Mod/Probe.lua`、`Mod/SpecializationP0.modinfo`：B160.187 / modinfo187；注册和181导入项不变。
- 三个直接测试文件：补八态、单值目录及退出断言；L2C抽取Panel fixture补真实的`UI.GetHeadSelectedCity`依赖，保留原零写／缓存断言，生产Panel未改。

## 本地证据

W0004 L2＋直接触及退出／加载的L3定向验证：`test_culture_meaning_diagnostic.py` 20方法＋`test_culture_meaning_l2c.py` 27方法，共47方法／58个实际subTest回调，0失败／错误／跳过（15.53s）。另20项原Modifier reader直接回归通过，与47中的继承断言有交集，不相加宣称独立覆盖。

| 证据 | 本地验证范围 |
|---|---|
| STATIC_CONFIRMED | 27精确owned／189附件；flat3七object与参数；普通Parts仍把3编码为1＋2；四个修改Lua语法、modinfo187／181唯一且存在导入、复用双语Text SQL |
| LOCAL_SIMULATION_PASS | 真实Lua／请求八阶段精确create/remove顺序；CLEAR1保持hold；REMAIN2只移除1、2零拆建；重复token、同回合变化、他城隔离、不读D |
| LOCAL_SIMULATION_PASS | getter独立给定10→11→10→12→11→12→13，PAIR12明确“不一致”，不是配置导出的假PASS；只读／缓存／迟到回复及引用／选择变化保护 |
| LOCAL_SIMULATION_PASS | 新＋3创建／移除／load失败保留退出保护、新token恢复；27项confirmed loss／reference／load退出，UNKNOWN不误清，普通建筑／binding／永久状态不变 |
| USER_GAME_TEST_REQUIRED | 各阶段真实差值、REMAIN2＋2原native实例是否延续、独立flat3、直接END与启用副本冷加载的原生撤销 |

既有Python3.14＋Lupa lua55环境；外部DB按main本机配置mode=ro读取，只在内存副本重建27精确定义，不改真实数据库。没有安装新环境、全历史回归、stress或游戏启动。一次初跑因测试fixture缺UI出错，补齐真实依赖后完整定向通过；没有删断言或修改Panel绕过。

## 更新与生命周期

没有新增事件订阅、每帧／hover Gameplay请求、常驻scan或GC入口。普通定域Audit及现有K/current fact路径继续运行；诊断本体只读资格／馆藏，不构造D明细。显式右键每token至多一次原生全局实例枚举，精确筛选与有界输出沿用；Show／Copy不重读。新增＋3纳入既有module-owned退出及一次load清理（精确目录27项），不是全库前缀清扫。永久状态、Shared目录、其它城市、GC、Design和main均未改。

## 一个最小实机流程

用现存已开启本Mod的存档副本，选Culture ACTIVE IV城、恰好一件支持著作且宿主未掠夺。**保持同回合、同城、同作品和总督；保持面板打开**，不需新建建筑或重做五yield长测。

1. 左键“生产力组合诊断”进入①基线，确认报告记录了可靠同回合基线。之后每次左键进入下一阶段，再右键读取真实Production及实例。
2. 依次看②单片1、③清零、④单片2；相对基线预期＋1、0、＋2。③仍在实验，旧收益没有恢复。记录读数，只有异常才需逐项截图。
3. 进入⑤双片1／2，右键留一份报告；随后⑥仅撤1，右键留一份报告。⑤已知可能实际＋1，继续⑥是本轮对照；⑥应＋2，且原＋2的instance ID应与⑤相同。配置2不能替代实测。
4. 进入⑦独立单片3，右键留一份报告；预期＋3。在此状态保存一个独立测试副本。点“结束验证”，右键留OFF报告，核对精确Meaning残留／实例，旧GWA正常恢复另算。
5. 完全退出后冷加载**⑦启用时保存**的副本。选同城、右键读取OFF，留一份报告。无同session基线是正常，必须看精确残留和原生绝对值，不把“未确认”写成0。

最多五份关键报告（⑤／⑥／⑦／直接OFF／冷加载OFF），其它读数可文字报告；可用原“复制／写日志”留完整内容。非⑤出现异常、UNKNOWN／截断或撤销失败时暂停对应路径并安全结束，不调整数值或盲目重试。

## 边界与下一步

[B159原生反证](Specialization_B159_Production_Combination_Native.md)、[B158原生与独立Catalog缺口](Specialization_B158_P0L2C_Five_Yield_Native.md)原件保留。原生实时读数不等于正常结算、倍率隔离、精准recipient或完整L2；独立＋3若成功仍需后续单yield单值方案计划和用户授权。本轮只等待此诊断，不自动正式cutover、Culture恢复或进入L3／M／N／U2。

源码commit、实际部署和receipt见[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)。回滚沿Git＋既有W0003精确receipt／staging恢复，不改安全工具或删除恢复包。
