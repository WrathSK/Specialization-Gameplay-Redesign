# B159.186 — 单城著作 Production 组合与退出诊断

用户在B158组合失败后明确“授权实施诊断”。本批STATIC_CONFIRMED／LOCAL_SIMULATION_PASS；原生单片／组合／退出及冷加载仍待用户验证。完整L2 NOT_PASSED，不改D0043设计、Shared D、逐领域Floor、Catalog、永久状态或GC。

## 实际范围

现有“意义延展验证”入口暂改“生产力组合诊断”：左键依次BASELINE → SINGLE2 → PAIR12 → END/OFF；右键只读当前作品Production及精确native实例，OFF也可读。仅一个本地人类Culture ACTIVE IV城、恰好一件当前已确认的支持Writing；不要求特定D或新增建筑。不启用Culture候选、其它yield或全城正式接入。

- `CultureMeaningProbe.lua`复用原单fixture／module-owned退出合同。固定技术对照为0、＋2、＋1和＋2（合计3），不是能力数值或新Gameplay公式。只复用已有`PRODUCTION_1`及`PRODUCTION_0`定义；切到PAIR12先撤上一＋2，再按＋1／＋2顺序创建。无SQL／模型／新carrier定义变更。
- 初始资格读取现有CurrentSpecializationFacts与GreatWorkFacts。Writing类别以完整`GREATWORKOBJECT_WRITING`确认；诊断本体不读D。已确认不合格馆藏／资格撤新片；临时UNKNOWN保留最近已确认配置并阻止推进，不隐式END。重复token幂等，清新owned确认后才释放旧GWA／Dialogue；load默认OFF，不重放实验。
- `Gameplay.lua`新增显式诊断ADVANCE／READ请求，READ只生成本次只读view。view给当前资格、26精确owned目录的当前残留／掠夺状态及作品引用，未知不伪装为0；普通建筑和永久Property不清。
- `UI/BoostGreatWorkRead.lua`单独读取真实宿主作品Production；同回合／同引用／同作品位置／主题／资格的可靠BASELINE才允许差值。预期、配置、实际读数分开；同yield组合不符明确报“不一致”，即时一致不作结算或完整能力PASS。OFF仍读实际作品／实例，退出差值含旧系统恢复，不能仅因OFF或载体数0宣布完整撤销。
- native collector仅显式右键执行，精确筛选26 Meaning Writing附件和旧GWA Production Writing附件；严格已有District对象／当前父城映射，显示instance ID／Arguments／Active／owner／subjects。截断或未知会报告，不推断引擎组合算法。复用原有有界枚举／token缓存，不保存native handles。
- `UI/P0Panel.lua`同ACK／复制日志复用字符串；换城／回合或引用过期后永久废弃该token读数，不回选重播或重扫。close／load取消迟到Meaning回复、释放读数，不改变Gameplay阶段。复用Text keys（中／英文）；`Probe.lua`／modinfo更新B159.186。无XML／icon新增。

普通更新沿用既有定域事件与有界核对；没有每帧／hover请求、新常驻全城scan、GC入口或永久账本。显式读数扫描本城宿主，显式实例诊断可能读取全局实例列表但输出／枚举受既有边界限制。load沿用一次精确26定义清理，并非AI专业运行。

## 本地验证

`DevelopmentTests/test_culture_meaning_diagnostic.py`最终18方法／31子测试，0失败、0错误（最终6.538s；含最后的迟到回复及OFF解释修正）；证据仅LOCAL_SIMULATION_PASS。

| 检查 | 范围 |
|---|---|
| 真实Lua／请求 | 现有K确认采样→当前资格→实际Gameplay请求→BASELINE／SINGLE2／PAIR12／OFF；＋2撤后＋1/＋2创建顺序；重复token／混合旧实验拒绝；其它城市隔离 |
| 生命周期／失败 | 工作ID／位置变化、非Writing／多件、UNKNOWN保持且不推进、END移除失败保留hold及新token恢复、load／confirmed loss／reference退出精确26项；普通建筑及binding保留 |
| 原生读数模拟 | getter独立指定10→12→11→11，不由配置反推收益；单片Δ2、两片Δ1明确不符、OFF残留／UNKNOWN／空枚举不伪称撤销PASS；nil／NaN／inf未知不变0 |
| UI隔离 | actual Panel缓存／Copy不重读、不写Gameplay；换城及回选无旧报告重放；close／load迟到ACK不重建已释放基线 |
| 继承回归 | 两组9项仍适用旧Modifier token／UNKNOWN／严格District/parent/subject检查直接复用，旧断言未改；不是全部历史测试 |

诊断D保护只禁止本体读取，允许真实既有CultureAesthetic在旧GWA退出事件上的合法D核对；没有停用L1来制造测试通过。另既有reader直接20项回归通过（与上表9项有交集，不能相加宣称38项独立覆盖）。旧Panel路由／Copy／modinfo184固定断言不属于当前入口，不改旧断言凑全绿。

5个修改Lua在已有本地Lua5.5环境语法检查PASS；modinfo186的181导入文件唯一、存在；中／英文复用Text keys与SQL语法PASS。外部本机当前内层DebugGameplay仅mode=ro读取，测试在内存副本应用源SQL；不改真实数据库。测试不证明Civilization VI引擎的收益叠加／结算／内存行为。W0004 L2＋直接退出／load相关L3，未运行full historical／stress或长测。

## 一个最小实机流程

用已启用本Mod的现有存档副本，选本地Culture ACTIVE IV城：**本城恰好1件已支持著作Writing，宿主未掠夺**。不用新建D建筑；同一轮不动总督、作品、政策、建筑或主题化。

1. 打开P0面板，左键“生产力组合诊断”一次。等①基线报告明确“同回合基线已记录”；若未确认或报错，停止并投递。保持面板打开。
2. 再左键一次进入②单片＋2，再右键读取实例，截图这一份；再左键进入③两片＋1／＋2，再右键读取实例，截图这一份。预期相对①分别＋2／＋3；配置和实例存在不能代替实际差值。若不符，仍可完成下面安全退出／冷加载读数以区分残留，不重试其它primitive。
3. ③启用时存独立测试副本；点“结束验证”，再右键“生产力组合诊断”读取OFF，截图。需区分Meaning退出与旧GWA正常恢复；报告不会把旧系统恢复收益算成新片残留。
4. 完全退出游戏，冷加载刚才**③启用时保存**的副本。选同城、右键读取OFF，截图这一份。没有同session基线是正常；比较精确残留／实例／原生绝对值与直接END，不能把差值“未确认”当0。

最多四份关键报告；可点击现有复制／写日志将完整报告存Lua.log，不逐回合截图、不重做五yield长测。报UNKNOWN／截断明确保留边界；不自动补造记录、调整公式或扩大清理。若先发生END失败、引用或退出错误，停止该路径并投递，不续其它实验。

## 原证据与停止点

[B158原生组合FAIL及独立社区目录缺口](Specialization_B158_P0L2C_Five_Yield_Native.md)保持；本批不扩Catalog，也不改D语义。精确recipient、Dialogue／theming独立、正常结算和全城cutover仍各自未通过；本次不是新能力实施或完整L2验收。部署实际commit／receipt见[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)，普通commit不等于部署。完成本批后等待这一次原生诊断，不自动进L3／M／N／U2。
