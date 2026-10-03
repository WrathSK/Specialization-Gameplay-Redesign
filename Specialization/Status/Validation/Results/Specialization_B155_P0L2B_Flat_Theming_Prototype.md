# B155.182 — 平加共存与主题化独立追加原型

State: LOCAL_COMPLETE / USER_GAME_TEST_REQUIRED；原生固定追加／native-only／theming隔离未确认。
Authority: Culture D0041；当前Meaning模型逐领域Floor／K0.5／份额／九域／作品资格保持。用户授权先做技术原型；不接入正式六yield／all-city能力。
Source: 441b85f609e5e9c70e5cb5eb58ba34a88870bd52；B155.182 / modinfo182。部署状态只见[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)，本页不从源码commit推断外部包。

## 范围与真实依据

[B154原件](Specialization_B154_P0L2B_Native_Combination.md)四态2/3/6/4、配置3Culture但实际追加Δ1/2；本场景FAIL保持。没有主动撤销HD+2不能排除间接共存。只读当前DB同effect1378个Modifier：1258 YieldChange、120 ScalingFactor、两者同时声明0；元数据不说明组合算法。显式100仍待实机，不写成修复。

原14项保留，module-owned新增2个single3候选并精确负责全部16项的退出／load／loss。后两项仅允许每件理论Culture3；无silent fallback／clamp。模式SPLIT→SINGLE3→SINGLE3_SCALE100仅OFF时经独立配置按钮切换，原验证按钮右键仍只读；配置按钮右键复用module-owned End直接结束，重复token幂等，OFF重复结束不写收益。四态操作仍原单城流程，其它城市／HD效果不动。

读取现允许可靠theming boolean，未知拒绝；作品／建筑／主题／引用／D／回合／资格／人口／候选配置改变使当前四态缓存失效，最多4组。按需读S/G/C及前4个建筑小计，所有建筑参与总计；普通计算不构造这些诊断，无per-frame／hover请求或GC改动。**预期追加始终A×W，不乘主题倍率**；实际不同就保留技术失败，不补差或改系数。

## 本地验证

79项Meaning实际Lua／SQL定向测试PASS（21.412s），26项K直接回归PASS（0.092s）。6个改动Lua语法、XML／控件ID、本地化SQL／中英文key与diff静态检查通过。这里只能STATIC_CONFIRMED／LOCAL_SIMULATION_PASS，不证明引擎倍率算法、真实UI布局或settlement。保留原断言，新断言针对16项owned、候选互斥／错误量、重复／退出／加载／两城、theme已知／未知／变动与fixed期望；不跑full历史／stress。

## 一个最小实机流程

用存档副本，Culture ACTIVE4、每件理论追加Culture3、作品都明确支持；固定同城同回合／D／Governor／人口／其它倍率。先复用B154非主题单作品fixture，无需重复旧完整矩阵：

1. 测试关闭时点击“切换验证配置”，选择**单一+3**。点击“意义延展验证”取得①基线；再点到②追加，记录作品文化差值。预期+3（W1）。右键仅刷新当前读数。错误量先停，不把配置当实测。
2. 若Δ3正确，再到③旧对话100%与④倍率基线。两次追加差值均应3；Dialogue本身也必须在有／无追加时产生相同原生增量（原B154作品定义基值2，不把HD平加当基值）。全部正确才记本场景native-only；若追加变6，只记flat结果，隔离失败。
3. 需要结束时，右键“切换验证配置”，直接退出而不继续倍率阶段，确认OFF及旧基线恢复。第一候选不正确时，只在基线恢复后左键切换**单一+3／倍率100%候选**，做同一短对照；如显式100把Dialogue压掉不能判PASS。已经找到可行候选不强求把全部候选测完。
4. 用户准备好的已主题普通博物馆作为独立第二fixture：艺术馆3件同类不同艺术家，或考古馆3件同时代不同文明文物，原生UI与报告theme=true、W=3。保持固定馆藏，重新开始①→②：Culture追加期望9（A3×W3），非18。S/G的非零配置也分别按各自A×W。若基础追加正确才继续③／④，完成后OFF；首个失败停对应路径，无需再做长测或新冷加载。

后两候选必须Culture3；未满足时只报告资格错误，不施加候选。其它参数、全部作品／D及其余修正固定；若需要排因，将同一收藏分散到未主题槽位后另起基线，**仅针对具体歧义另行安排**，不默认增测试。艺术馆不要用重复艺术家当干净未主题对照。

## 证据与未来可改空间

追加、Dialogue来源隔离、theming独立各自单独记录PASS/FAIL；读数正确也不自动证明正常回合入账。未知同类recipient、其它三yield、all-city及cutover继续独立门禁。当前候选失败先退出；两个获授权flat候选均失败时停止该primitive，不凭经验换公式。

若真实主题化使追加呈2倍，保留配置／实际读数／撤销结果，作为未来用户允许theme包含追加时可复用的技术档案；当前则属于独立追加合同不满足，不能借此宣布成功。不同路径／建筑／作品类型不类推。Meaning无Tourism，印刷术只Tourism，不解释Culture异常。
