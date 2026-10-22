# B161.188 — 意义延展Production单值门禁

用户在B160多片不叠加反馈后明确授权本最小方案。**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED；完整L2 NOT_PASSED。** 当前Design D0045不变。本批不是全城正式接入、其它yield切换或新的Gameplay规则。

## 范围与权威计算

默认OFF、单个本地Culture ACTIVE IV城市、已确认合格馆藏。工业区与军营各自 `floor(0.5 × D)` 后相加为每件Production，W仅乘整城总量。M.Plan七域／五yield公式不改；本次ActiveWriteYields仅Production。生产力0不建载体，1–10只选对应最终值；不是把旧多片Modifier塞到同一building中。

新增10个InternalOnly `BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_1..10`，每个对七个既有支持object有一个flat Modifier，YieldChange为对应整数、无ScalingFactor／新Requirements。旧27项完整保留为精确清理及旧固定诊断依据，Owned37／附件259；原189附件SQL前缀字节不变。七object定义不等于七类作品的原生验证。

## 模块与消费者

- Model：单Production最终值0–10目录／ActiveWriteYields；五yield影子计算及旧B160固定bit对照不改。
- Probe：普通OFF→BASELINE→ACTIVE→OFF只写Production；换值先确认撤销旧37，不变化零写。normal View拒绝旧bits／非Production残留或多个final，按需报告精确残留。先确认新效果撤销再释放旧GWA156／Dialogue hold，以当前事实恢复，不重放快照。
- SQL：只追加10×7定义。Gameplay只取消END强制固定诊断View；Panel复用原按钮左ADVANCE／右READ，结束按钮不变。仅匹配所选城／完整reference的显式READ首次token合并原生实例报告，ADVANCE／END／Copy／重复展示不枚举。
- reader：Production-only读每件预期／本城预期、独立宿主getter与精确Writing实例。SubValue仅接受已观测可选负号；District／Owner／City／SubType及parent／完整reference核对保留。UNKNOWN／迟到回复不变成0或PASS。其它yield明确未启用。OFF的绝对值含旧系统恢复，不靠归零判断退出。
- Probe版本／modinfo188／原中英本地化key更新；未新增按钮、XML或icon。直接测试新增单值suite，fixture仅补37精确目录和独立金额getter，旧five-yield／历史断言不删除；固定八态诊断适配实际END普通ACK，但原撤销断言保留。

## 本地验证

73项定向方法／78个实际subTest，0失败／错误／跳过；包括单值新suite、旧八阶段直接诊断、精确reader。运行环境是已存在的Python3.14＋Lupa lua55，外部DebugGameplay只读备份到内存，未修改外部DB。

覆盖：0–10有限单值、非法整数拒绝、逐域Floor反例／W0/1/2、实际Shared物理建筑／掠夺修复事件、同回合3→4→3／0与零变化零写、重复token、两城、UNKNOWN、确认loss／reference／load精确退出、创建／撤销失败保持hold、真实request／K样本配对及reentrant保护；精确37／259 SQL、独立native getter模拟、signed格式及错误ID／parent／reference拒绝、explicit一次／迟到回复／缓存和OFF残留读取。

Lua语法、Python AST、modinfo XML、精确SQL附件及旧SQL前缀检查通过。没有full historical／stress／原生游戏运行或性能长测。模拟getter／写入计数不能当作真实Civ VI收益或性能PASS；不运行已不适用于Production-only切片的历史five-yield writer套件，不修改那些断言使其变绿。

## 部署核对

运行源码commit `fcea2427786cc3230c8b3ad0b9f8564834311816` 已普通提交／推送，干净develop通过可靠OS游戏退出检查后，以既有W0003工具精确旧receipt恢复stable桥接并激活本包。receipt `B161.188-fcea242-playtest.json` 为DEVELOP_ACTIVE，source/live182/182 MATCH；B160与stable恢复点均MATCH，无pending transaction，未启动游戏。只证明部署一致性，原生值变化／退出／冷加载仍待用户短测。

## 一次最小实机流程

复用文化ACTIVE IV测试城；优先只留一件已支持著作，固定其它产出加成，采用独立测试存档。用现有建筑／Cheat准备**工业区D6、军营D0或D1**，预期每件Production3；看D报告确认输入，不凭建筑名字猜Tier。

1. 选中该城，P0面板“意义延展·生产力”左键一次准备基线，再右键记录实际Production；左键一次启用，右键核对每件3、本城3和一个VALUE_3活动实例。其它yield本批不测。
2. 本城军营补到D3（原目录合格T1＋T2即可），预期每件4；右键确认只剩VALUE_4／实际Production4。再增加一件已支持著作：每件仍4、本城预期及原生小计8、仍只一个最终值carrier。D／W变化使旧差值基线失效时，看绝对原生小计与实例，不把“差值未确认”当失败或PASS。
3. 保存**仍启用**副本；点“结束验证”，再右键确认owned0、本城Meaning Writing实例0、旧writer按当前事实恢复。原生Production可能包含恢复后的旧效果，不强求0。
4. 完全退出／冷加载该启用副本；选城右键应OFF、owned0、Meaning实例0。再手动基线→启用，确认每件4／W2总8仍正确，最后结束。

若现有城不便凑上述D，使用D报告中已知的非二进制单值（优先3或5）并使其改变到另一个值，按显示的每件预期及W核对；不用另开长测。最多保留启用、变化／W、END和冷加载四份关键报告。第一项真实值、精确退出／映射失败即停对应步骤；不继续更改金额碰运气。未知作品／主题化／倍率隔离／正常结算及其余object仍是独立技术门禁，不要求本次补测全部。

## 事件、生命周期与停止点

复用原一城fixture及CurrentSpecializationFacts／DistrictCompleteness／GreatWorkFacts。建筑／馆藏／总督／当前reference变化及原有限回合核对响应；self-carrier按exact37过滤，不新增订阅、polling、hover请求或GC。普通Audit不构造诊断；完整View／原生枚举只显式请求。保持同回合真实变化、UNKNOWN确认后再更新、失败保护及确认失城退出；load默认OFF，对保存的精确37做现有一次清理，不为AI运行专业系统或修改永久Property。

UI只保留最近token字符串／baseline，换请求、reference、回合、作品／主题／资格变化失效；不持久化native句柄或全局实例列表。本批局部换值最多一删一建，37精确存在检查为退出责任，零变化不写；不宣称原生分配改善。GC、E2历史、永久资产和其它专业不变。

[B160反证及观察范围](Specialization_B160_Production_Reconfiguration_Native.md)冻结保留。现批次本地完成后按W0003部署及收集上述一次实机验收；停止，不自动全城cutover、其它yield单值切换或L3／M／N／U2。source/live及receipt只从[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)确认，不从本文件存在推断部署。
