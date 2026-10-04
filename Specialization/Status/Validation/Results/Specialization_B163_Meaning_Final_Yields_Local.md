# B163.190 — 六产出最终值承载与文化恢复技术门禁

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。单城可逆验证，不是完整意义延展／全城cutover PASS。

## 授权、发现与最小改动

用户批准原五产出最终值计划，并明确“把文化再加回来，然后授权实施”。D0046仅恢复Government Plaza／Diplomatic Quarter→Culture；K0.5首测、每域Floor→同yield合计→W、份额、资格和独立追加不变。其它专业／Shared及永久状态不改。

[B160反证](Specialization_B160_Production_Reconfiguration_Native.md)说明Production多片不按预期叠加，B161最终值已获所测3→5／W2=10证据。但[B155/B157](Specialization_B157_Modifier_Comparison_Native.md)早已出现单一Culture＋3、实例有效／HD＋2持续而CultureΔ0，不能宣称文化根因已由Production解决。本次新Culture最终值以剧院为宿主，形成真实技术差异；不撤HD、不补差，实际挂载和共存仍需原生门禁。

| 责任／文件 | 本批实际变化 |
|---|---|
| CultureMeaningModel.lua | 九域六yield；每件S5／P10／G30／Food5／Faith5／C10；0无载体、各yield正值只一个；保留旧精确目录 |
| Data/CultureMeaningProbe.sql | 旧37／259字节不变，追加55／385→92／644；C10个final要求剧院，其余市中心；原7个object附件，flat整数、无ScalingFactor |
| CultureMeaningProbe.lua | 六项projection／View／简报；按声明宿主验证定义；旧B162就绪／清理算法沿用但精确目录扩为92，正常one-fixture最多6个final |
| UI/BoostGreatWorkRead.lua、UI/P0Panel.lua | 默认六行中文预期／原生差值与异常摘要；实际DistrictType核对Culture宿主；READ一次全局枚举，明细同token缓存导出；换城／跨回合／signature变化清缓存、已消费token不重扫 |
| Text/TestText.sql、Probe.lua、modinfo | “意义延展·六产出”及B163.190／190标识；原结束入口沿用 |
| tests | 新当前六yield suite；旧共享SQL fixture扩目录、cleanup seed扩92，固定Production诊断阶段与历史语义断言保持 |

## 本地结果与证据边界

**82方法／195subTest PASS，0 failure／error／skip。** Lupa lua55与现存Python3.14，外部Firaxis DebugGameplay严格只读复制到内存后应用本批SQL，不修改游戏／HD数据库。选择当前FinalYield22方法＋StartupCleanup12＋固定Production诊断中15方法＋RetainedModifier2＋既有独立Modifier31。旧Production-only普通入口／旧Panel源码片段提取／旧modinfo版本wrapper不作为当前行为断言，由新真实入口／Panel／syntax／package覆盖；历史断言不改，未跑全历史／stress。

覆盖九域D0..10、逐域Floor反例／W0/1/2、全部合法最终值与非法拒绝、92精确定义与644附件／实际PrereqDistrict／无ScalingFactor、旧SQL完整prefix、同回合只替换变化值与零重复写、UNKNOWN保留与已确认变化、reference／loss／两城隔离、新目录load清理、失败锁停／新token恢复、部分创建失败不混旧新、同步通知有界、真实请求及K配对、旧writer撤销失败和import registry。

原生读数fixture独立于配置：模拟Culture预期＋2但实际仍4时报告Δ0异常，实际6才报告Δ2；宿主Theater／错误CityCenter／未知分别通过／不完整。Show／Copy零重复原生枚举、换城／同token signature变化后不保留旧成功摘要和明细。Lua语法、modinfo190所有引用及D0045 Spec冻结字节一致已在suite通过。

模拟没有证明Civ VI实际将新carrier挂入剧院、六yield共存、作品精准recipient、百分比隔离或正常结算。B161／B162已测共享证据只继承匹配范围，不把全部共享路径重新派给用户，也不扩大原PASS。90个本地链接／锚点、当前selector与accepted hash检查PASS；context check／self-test PASS（182 runtime／437 guarded文件），另2项当前Panel／syntax定向复核PASS；实际source/live身份以[Status](../../Specialization_P0_Status.md#current-authoritative-state)和部署receipt为准。

## 性能、持久化与退出

无新事件注册、每帧／hover Gameplay请求、AI能力、全城事实采集、GC或永久Property。普通ready仍常数判断，one-fixture exact检查37→92；首次startup/load既有有界城市清理覆盖扩大后的92IDs，FAILED不自动重复删除。session／lastPlan／action receipt均沿既有替换、END、loss、load退出；原生枚举只explicit READ，每token一次，原生全局列表的物化成本不能说成单城成本。

本城旧GWA由自身模块撤exact156、Dialogue当前reference置0%；先撤本模块owned确认，再释放旧writer按当前事实恢复，不重放快照。B162清理算法／持久化模型不变，扩大目录和新宿主由本地失败／load回归及本次native END直接覆盖；若出现新宿主退出异常再定域扩测试。

## 一次连续session验收

复用Culture ACTIVE IV城市、一件已支持著作和古罗马剧场。保持其余作品、政策与主题状态稳定；市政／外交的文化预期必须大于0，否则没有覆盖文化共存，可用已支持合格建筑补足D，不扩Catalog。

1. 左键“意义延展·六产出”准备基线，右键读数；再左键启用、右键读取。核对六项非零预期与实际；尤其Culture在原生＋HD基线上追加，如基线4／each2，应变6。无非零输入的yield标未测，不能记PASS。
2. 同session给一个领域增加合格普通建筑，使每件值跨一个取整档，右键核对原生值随新值变化，明细唯一final替换旧final。无需逐领域造六次建筑；旧值不得残留相加。
3. 加入第二件支持著作，核对each不变、该城作品追加总量翻倍；本城总量不等于作品单件原生基础值。D／W变化会使旧Δ配对失效，报告明确“差值未确认”是正确保护；比较预期／原生绝对值／实例，不拼旧Δ。只有确需重新配对时才结束并准备新基线。
4. “结束验证”后右键，Meaning精确carrier／Writing实例应0，HD正常效果保留，旧writer按当前事实恢复。只看OFF文本不算撤销PASS；有配置不算入账PASS。

每一步只验证本批新增原生不确定性：六项单值共存、替换、W和新精确目录／Culture宿主退出。不默认保存启用态、手动关闭、退出冷加载、再次启用整套harness循环。文化失败先END并停文化路径；记录宿主／实例／实际值，不能改Design、撤HD、补城市收益或强行通过。通过后仍不自动全城cutover／L3／M／N／U2。

## 部署记录

W0003：source `37636776d9ce00cebcbefbf600af24984f2c6451`，B163.190／modinfo190，receipt `B163.190-3763677-playtest.json` DEVELOP_ACTIVE，182/182 MATCH。游戏退出由可靠OS进程检查确认，旧B162精确receipt先恢复stable再激活，B162／stable恢复点保留，无pending marker、无游戏启动；不提升native证据。
