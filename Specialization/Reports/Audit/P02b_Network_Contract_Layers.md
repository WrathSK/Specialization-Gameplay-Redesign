# P02b — 共同Network合同与独有payload边界

独立审计 IA20261007 / W15；基线 `2a61f34f128bf613e6d99703a8680acd886903c9`。slice覆盖完成；仅STATIC合同/代码/断言审阅，没有新LOCAL/native PASS或总审计结论。

## 问题与结论

**共同接入、来源、接收、转发及当前路线authority是否一致，新增payload会不会错用共同资格或旧公式？** 复用P09发布/封装、P12规模验证，不重新跑完整transport/每专业网络。

所查NET-001至004与当前Bridge没有新增共同拓扑矛盾。角色候选、业务资格、payload merge与效果writer必须分层；现存旧Culture/Industry/Commerce输出是已登记cutover缺口，不能标成当前新Design已实现。Research旧Inspiration明确保留待重设计，不应随Culture退休。

## 正式来源与真实实现

[Spec NET完整条款](../../Design/Specialization_v0.1_Design_Spec.md)241–263是共同方向/资格与保留Research公式；[Shared NETWORK_LAYER](../../Design/Content/Shared_D0045.json)明确无统一payload公式或固定ability slots；[Network阅读页](../../Design/Network.md)解释共同规则。专业资格按各自current Content，较旧[D0032 network目标合同](../../Architecture/v2/D0032_Adaptation.md)75–85的业务行受其页首supersession与新决定约束。

| accepted规则 | actual代码 / 反证 |
|---|---|
| 首都/Commerce为Trade Center | [Bridge](../../../Mod/NetworkBridge.lua)245–250：Commerce Identity/P≥1；capital另入，不要求CommerceIV |
| topology source候选 | R/C/I Identity/P≥1；不是所有payload已满足业务ACTIVE门槛，不需要中心与来源共享一个等级条件 |
| S→H direct | accepted own-origin routes，destination为己方中心/source匹配；Receive219先核op=pid，不能脱离前提报foreign numeric ID碰撞 |
| direct中心自然receive | 258–262加入recipient source set，不需H→H或额外IV资格 |
| 首都自身接入 | 255仅为已注册source kind自身加direct set并receive；不补一个未定义Commerce payload或让所有中心自动self |
| H→D distribution | 264–269只从H的direct source set建立recipients；recipient关系不反写center，非递归 |
| 多资格去重 | source/center/recipient用set，national按城市键计N；不是route/source/center数量 |
| current失效/reload | [Input](../../../Mod/NetworkInput.lua)与Bridge引用/epoch/seq/端点/trader/war保护，确认失效withdraw，UNKNOWN留最近确认并标重验证；网络历史不是永久authority |

recipient可以NONE/P0/其它专业，不要求自己是source。Foreign端点可因外贸路线验证被读reference/trader/war，但不读foreign专业/启用系统。国内方向不能改成任意无向reachability；Commerce自己的直接双向pair另有合同。

## Owner与更新边界

| 层 | owner及职责 |
|---|---|
| 永久资产 | Store/各具名业务ledger；receiver不会得到source历史产权 |
| 当前采集 | BackgroundRoutes snapshot；Sender拥有flight/seq，不是Gameplay接受authority |
| accepted input/common view | NetworkBridge唯一接受/验证/withdraw，Input签名含Identity/Potential/ACTIVE/ref/first与routes/capital/config |
| payload/effect | consumer自己的source gate/merge/业务版本/carrier/退出；publication不是收益事务 |
| contract | Commerce签约/锁定与异常终止；NET路线失效只直接影响连接资格，不能重写已成立合同 |

同route也需要当前Gov/身份/资本等事实变化；不能为性能略掉同回合变化。private view每player一份，Current查询复制/新数组，不Capture；这些反证没有关闭公开accepted bucket别名IA-P09b-F01。Topology版本不替代作品/template/config payload版本；接收的模板/Insights不能 re-export为自身历史。

## 当前payload与已接受新机制

| 类型 | 当前运行 / accepted目标 | 处理责任 |
|---|---|---|
| Research | 旧`k×max有效ACTIVE×sqrt(recipientN)`，最后一次half-up；RES005/NET-RC明确保留NETWORK_REDESIGN_REQUIRED | 不因没有新公式自动退出Research |
| Culture | 当前Boost仍旧Eureka scalar；新ACTIVEIV来源先独立完整3/3再过滤当前Owner自身文明、做文明集合UNION、receiver working specialist×K_C1 | N3 cutover；common source-city ID并集不是业务文明并集，也不能跨source拼半份 |
| Industry | 旧Discount≥I、全来源最高tier/旧CopyIV 50% sampledP仍在；新III模板并集，每个T仅在其actual holders内分别择construction/purchase最高 | H切换；不能全桥source改为III，也不能恢复旧“模板/最高效率来自不同source” |
| Commerce | 旧III connected-kind支持/IV incoming-only20% convergence仍在；新商业化self＋直接国内任意方向；发展签约IV→target直接outgoing，签后断路不取消 | P切换；distribution可达不能替代直接pair/签约；旧IVself额外资格不是共同中心接收规则 |

真实旧入口：Gameplay751/761/764/784 Start Copy/Discount/Boost/Convergence，Bridge59–63通知；BoostRefresh后台初始化不要求P0/贸易窗口打开。已在[实施退休矩阵](../../Architecture/v2/D0032_Implementation_Plan.md)、[Industry](../../Architecture/v2/Industry_Preparation.md)/[Commerce准备](../../Architecture/v2/Commerce_Preparation.md)登记，不新增“共享authority被改写”finding。

## 模型/断言/native的证据层

本轮正式测试只读，没有运行：

- `DevelopmentTests/NetworkState.lua`是旧pure provenance原型，capital-self不自动recipient、假设CommerceIV free-self；multisource/shadow模型不能作现行NET oracle。当前Mod没有NetworkState文件，derive在Bridge私有函数且验证nativecity。
- BatchA真实Input/Bridge，有同route资格/中心/capital/ACTIVE变化、UNKNOWN、端点/token/trader/war、seq/turn/epoch断言；native对象/EffectiveFacts/通知consumer为stub。
- BatchB七种非零route图与三方完整query输出比较、copies/metadata/通知内读取；比旧prototype强，仍非所有业务consumer/native实测。
- B134同回合scope/UNKNOWN留值，B136 realProbe/GovGate/EffectiveFacts＋一条非零route，foundation/ledger仍mock，不自动等于完整Store/E2。
- recapture Bridge例routes0只证明重建入口；30,000 Current查询只已发布view读取，不证明normalpublication五consumer工作集。

仅只读原生结果文字，未重看截图：[B027](../../Status/Validation/Results/Specialization_B027_User_Result.md)三路线direct中心接收/nonrecursive，B031删除目标route/N撤销；B026旧“中心不自然recipient”被D0009/B027取代，不当当前冲突。旧B054工业/旧B062商业各限所测收益与口述范围，不外推新合同/双币/所有撤销。后台UI当前路线来源已接受，不能重新要求纯Gameplay全集；来源许可不等于本Mod传输/收益全PASS。

## 复用的finding与扩展成本

无新增独立拓扑finding：

- IA-P09b-F01公开accepted bucket输入别名：MEDIUM/FIX_BEFORE_NEXT_PROFESSION，当前没有主动mutation caller；private查询copy不覆盖它。
- IA-P13a-F03 consumer独立事实/手列通知、IA-P13a-Q02新角色接入名单：保持MEDIUM/BEFORE_NEXT，不合并不同payload规则。
- IA-P13a-Q04 UI4096 vsSender/Bridge128/16384容量条件：MEDIUM/MONITOR；128/129结构证据复用，native合法容量未知，不加用户堆路线测试。
- P09b-Q02同份publication metadata以及processed ACK不等于每effect成功：既有隔离和候选边界保持，不据notify次数宣称收益结算。

新专业接入需分别处理Input identity whitelist、source/center/national/receiver角色、独有业务输入版本、consumer普通通知和exact退出。并不是每个新专业都应是source/center或全国聚合；Harbor无额外Network Ability的未来规则不要求共同层添一个slot。三处未衔接设计边界保持原状，本轮不调和。

实际readscope：完整NET/Shared layer/Network阅读页及直接专业network对象；Input全文、Bridge角色/输入发布/验证/query/失效具名段；A/B、B134/B136/E2/Current query及旧prototype/model直接断言；current source retired矩阵与准备页面、具名native文字。P09/P12复用，没有全读/重跑所有专业或历史wrapper。

下一 **P03a/P10a Research accepted规则→当前模块/长期资产对照**：Research_D0040完整content、Spec当前RES及对应接受/替代；已有Infrastructure/Cross/Apply/Chair/Tradition的模型/入口/资格/保存/退出与证据；复用Shared/Network及P06/P07/P08，不重新逐能力跑完整生命周期/native。优先查公共合同会随新增能力扩大返工的点，已知Research owner K01与网络重设计继续按实际deferred范围。这里只做审计，不进入L3或任何implementation。
