# B161.188 — Production单值原生结果与OFF残留

**USER_GAME_TEST_PASS（所测著作的3→5重配、W2总10及signed字段映射）；USER_GAME_TEST_FAIL（重启后OFF仍残留VALUE_5）；直接END NOT_CONFIRMED；完整L2 NOT_PASSED。** 用户确认前四图在重启前，后三图在重启后；未记录保存／END的准确顺序，不据此猜测存档启用状态或哪次通知实际发生。

## 七图观察

全部原图逐张读取。所选本地城市为Edinburgh(TEST)，owner0／City393220；城市名只作阅读标签，实例归属仍按District／父城／完整reference核验。以下3→5是实际输入与读数，不能改写成测试建议中的3→4／8。原计划允许等价的已知非二进制值。

| 图／时间 | 实际状态 | 预期、配置与原生观察 | 可得结论 |
|---|---|---|---|
| 1／22:39:18 | BASELINE，W1 | 每件预期3，配置0，原生Production0 | 当前配对基线 |
| 2／22:39:26 | ACTIVE，W1 | each／配置／原生均3，Δ＋3；owned1，唯一VALUE_3实例12464；旧GWA Production实例0 | 最终值3真正产生＋3 |
| 3／22:39:56 | 改D后ACTIVE，W1 | each／配置／原生均5；owned1，唯一VALUE_5实例12490，旧VALUE_3不在精确名单；旧GWA Production0 | 3被5替换，未读到8或旧3残留；旧配对基线失效，不强行使用差值 |
| 4／22:40:02 | 巨作界面，两件著作 | Edinburgh同一宿主内W2，Production小计10 | 每件5×2＝10，非按已乘W的总值再逐件应用 |
| 5／22:44:12 | 用户确认重启后，巨作界面 | 同城W2仍显示Production10；旧Science／Gold／Faith等出现 | 单凭此图不能分配收益来源或证明退出 |
| 6／22:44:31 | OFF报告 | 每件预期nil，但configuredProduction5、remainingOwned1；VALUE_5实例12490 Active=true／本城核验，旧GWA Production同时有2个活动实例；宿主小计10 | OFF控制状态与真实撤销不一致，新旧writer并存 |
| 7／22:44:32 | 同一OFF报告的下半部分 | VALUE_5 flat5；旧GWA Writing P0／P1实例12599／12578（flat0.5／1）亦Active=true／本城核验 | 补齐图6残留证据；不是独立END测试 |

图2／3的所扫Writing实例城市UNKNOWN为0。图3及重启后负数opaque SubValue仍通过严格城市核验：这是B161 signed格式补丁的所见原生证据，不将SubValue用于身份，也不扩大到未见对象格式。图4证明该宿主两件著作的小计，不冒充完整全城recipient、其它作品、其它yield、倍率隔离或正常回合入账证据。实例Active不等于旧、新收益按数值相加；本轮只确认并存，不推测引擎内部优先级。

## 退出与证据边界

重启后的**OFF＋owned1＋本城VALUE_5活动实例＋旧writer恢复**违背预期的临时实验退出／新旧互斥合同，分类为`NATIVE_LOAD_WITHDRAWAL_BOUNDARY`，不能把它解释成用户没做完步骤而忽略。没有重启前直接END的图片，所以直接END仅NOT_CONFIRMED，不能登记END FAIL或PASS；准确保存来源、实际加载通知顺序及失败调用仍未知。

本次单值Production技术方向已取得上述增量PASS，收益本身无需重测；B161整体退出门禁及正式L2尚未通过。只阻塞依赖此临时writer清理／互斥的后续切换，不宣称永久账本损坏，不扩大为全项目性能或存档调查。

## 定域源码核对：已知入口与尚未证实的原因

STATIC_CONFIRMED：[Probe](../../../../Mod/CultureMeaningProbe.lua)新会话为ready=false、OFF、target=nil，Start不立即清理。首次reset依赖LoadScreenClose、后续本地玩家回合或ADVANCE；[Gameplay普通READ](../../../../Mod/Gameplay.lua)只取View。reset在枚举0城时也能标ready；CollectionConfirmed在无target时退出，Audit在未ready／无target时退出，不能由可靠后台样本补首次清理。无target且OFF时END可仅返回，不代表已撤销保存载体。

旧[Dialogue](../../../../Mod/Dialogue.lua)／[GWA](../../../../Mod/GreatWorkAdjacency.lua)可由自己的Init／当前样本恢复，只清自己的精确owned目录，不清Meaning37。因此旧writer恢复不保证Meaning首次清理已发生。加载通知缺失／过早、实际清理失败等仍是待区分假设，不据静态入口缺口认定实机唯一根因。

[B161原本地73方法／78subTest](Specialization_B161_Production_Single_Value_Local.md)保留：主要夹具在城市已可读后主动fire LoadScreenClose，确认目录与退出算法；未覆盖保存载体＋全新会话＋漏失／早到通知＋当前READ／后台旧writer恢复这一组合。Mock移除立即生效也不能证明native实例持久化与时序。本轮未改断言或重跑玩法回归。

## 长期验证原则与本批收敛

采用[本批delta／共享证据继承](../../../Workflow/README.md#native-delta-and-inherited-evidence)。原“启用副本→结束→完全退出→冷加载OFF→再启用”主要测试Probe harness，不是新的Production公式；不再作为每个能力的默认验收循环。当前切片的连续session核心见[计划](../../../Architecture/v2/P0_L2_Meaning.md#已授权切片--production单值承载)，已测3→5／W2不要求重做。

证据按实际范围继承：[B157](Specialization_B157_Modifier_Comparison_Native.md)只确认当时所测同session精确退出／旧writer恢复，不能升级为新增VALUE目录或冷加载PASS；[B160](Specialization_B160_Production_Reconfiguration_Native.md)的CLEAR1是hold内局部撤销，不等于END；[B158](Specialization_B158_P0L2C_Five_Yield_Native.md#第四步与冷加载的证据边界)仅有OFF控制观察，冷加载撤销未确认。其它能力的冷加载PASS也不证明Meaning全部退出。这些边界保留，不以缩短测试制造共享生命周期PASS。

## 下一最小建议（未实施、待授权）

仅修Probe首次清理／就绪与OFF残留边界：先补持久化VALUE_5＋全新session的漏失load、过早load／0城随后可读两个本地反例，沿实际READ／后台样本调用；保持READ只读、不靠打开面板初始化、不新增轮询或全局事件重构。核对旧writer恢复的先后顺序，继续精确37／UNKNOWN／foreign／撤销失败保护，不清普通建筑或永久记录。

在可靠有界入口完成幂等清理，不能将暂时0城当作已清；OFF报告须区分session未启用与清理已确认，END ACK不能掩盖残留。具体修复及直接受影响消费者需要另获实施授权，当前不改运行代码。

修复后仅复用已观察残留的测试存档，一次冷加载＋精确读取，区分“VALUE_5／Meaning实例归零且旧writer按当前事实恢复”与“仍残留／混写”；本地模拟不能确认native持久化／加载时序，所以这个具体异常值得实测。若修复改变END，再补直接END一项；不重做3→5／W2、不要求新长测或整套重新启用循环。现在不要求用户补测。

## 归档与本轮范围

七张原图原名原字节移至ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B161_P0L2C_SingleValue_20261003_2239/`，manifest关联本结果，7/7 SHA256 MATCH；图片与manifest均不进Git，收件目录／其它文件保留。

运行包沿最近核对的B161.188／modinfo188，source `fcea242`及receipt `B161.188-fcea242-playtest.json` DEVELOP_ACTIVE／182 MATCH记录；本轮未重新核验外部包／进程，没有部署或启动游戏。只更新长期验证指导、当前验收范围／Status／已审阅导航hash及本结果；Design／Mod／测试／永久数据／GC／main不变。
