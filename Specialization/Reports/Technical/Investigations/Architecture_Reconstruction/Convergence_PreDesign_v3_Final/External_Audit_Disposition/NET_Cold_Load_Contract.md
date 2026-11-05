# NET：正常冷恢复、异常与真实变化

Status: Stable candidate — C3已由Claude短复查PLAN_CLOSED并获Owner接受；非正式规范／实施授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅修订候选／参考文档并作只读证据及文档完整性检查；不改冻结报告、生产、测试、工具、正式规范或状态，不运行生产测试／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 1. 模型：保存、原生恢复与Lua重建是三件事

符号：S=保存时真实业务状态；I=原生恢复的已安装载体／实际效果；F=当前可靠原生事实＋Mod真历史；W=有界会话级按来源见证；K=已独立确认贡献的集合（不是自动获准的部分支付）。I不是当前证明，也不能从整体I反推来源。W不跨加载。正常 same-build cold 应 F重建等价S，核对I幂等；**尚未证明Civ VI在何事件恢复所有隐藏建筑/Modifier/引用**。

| 阶段 | 可读／责任 | 允许写入 | 完成凭据／未知 |
|---|---|---|---|
| 保存前 | 当前引擎状态＋Store已提交历史＋实际载体；in-flight receipts不猜终局 | 只沿正常业务规则；保存不是额外结算 | 保存前已发生退出，应已在保存状态体现；不一致要查写入/存档次序 |
| 原生恢复中 | 城市/隐藏建筑/Modifier/ref的恢复先后未知 | 未可靠确认基础身份或载体时禁止猜清／修复 | N-COLD需观测；LoadScreenClose不是未经证明的全事实就绪凭据 |
| Lua冷初始化 | 缓存/拓扑证明/W/依赖索引重建；Store解码、owner/ref、ACTIVE、D/history逐层就绪 | 不因缺输入撤除、部分重算或覆盖I；不先清再采样 | 生产init责任持有；事件唤醒见[矩阵](Completion_Wake_Responsibility.md) |
| 首次可消费快照 | 同epoch/ref、完整所需F和可靠拓扑完成，读中无写／版本变化 | 按原公式一次差异核对，正常预期0写 | 字段完整不是native恢复证明；UNKNOWN未完成不伪READY |
| 初始化期间或之后的真实新变化 | 新route/身份/资格/ACTIVE/owner/ref/历史确证变化 | 负事实立即收紧严格交易及资格并登记被动撤除；cold整体I不可拆且无W时，在首个完整可消费快照应用对应减项，不凭空分解；接收城确认退出仍走其合法exact退出 | 必须写明依据/发生次序／完成责任；“Lua未读到”不是新负事实。不能无限以初始化为由不对账 |
| 严重错误 | 历史/读取/写入等异常，scope/原因显式报告 | 不未知当0/空网/退出；不反射性全清；不盲重放 | 正常冷输入不足不是错误终态；不可避免政策取舍才Owner Packet |

当前启动边界 [Mod/RuntimeWork.lua:493](../../../../../../../Mod/RuntimeWork.lua#L493)–510只等HistoryStartStatus且先latched；[Mod/Gameplay.lua:1031](../../../../../../../Mod/Gameplay.lua#L1031)明确composition完成是诊断，不等于Store/effects就绪。因此不能直接把这两个边界当完整冷恢复屏障。

## 1a. 哪些恢复自保存，哪些只能重建

| 对象 | 当前保存/读取归属 | 冷启动怎么恢复、尚缺什么证据 |
|---|---|---|
| 城市及隐藏建筑/Modifier、实际收益、owner/cityID/坐标 | engine对象；三个writer用GetBuildings/HasBuilding/GetBuildingLocation读presence，按exact定义Create/Remove；这些读写不证明engine恢复顺序 | 首次native可读presence/ref和真实效果分别观测。城市UI有缓存，不可单靠面板值宣布效果已恢复；未证所有Carrier与效果在同一边界可用 |
| identity/token/parent/envelope与真正专业history | CityProgressionStore受控Game/City Property、各专业schema/receipt；不是Lua cache | 校验保存record、当前绑定、owner/ref、合法deferred后开放读取；历史不可读是明确严重错误，不当缺少旧派生快照 |
| Commerce配置/信誉/资本发展合同 | Store保存；CommerceState提供投影；金额结算仍有实际treasury/原生receipt owner | samebuild解码可信条款；cold不会重签或按当前R改旧terms；临时R0不写回历史 |
| Commerce views/samples/依赖索引 | Commerce.Start会话局部tables，未持久化source分解 | 先observed nativeGold保I，再用可靠F/topology从真输入重算；无W不能把unknown源当0 |
| CultureNetwork records/sourceSamples及recipient依赖 | sourceSamples局部；initialize298–314读当前installed的kind/n；Insights真历史在Store | I只证明已安装整体，不能由count反推文明/来源；可靠Insights+topology齐后重建set并核对 |
| Standardization records/sources/old.loaded | records局部；227–244从presence采applied；templates/L真实历史在Store | loaded不是保存的来源权威；正常cold待F完整，按target max核对；warning/error需有完成责任，不永久loaded |
| Bridge buckets/views/inputProviders、UI shadow/epoch/seq | [Mod/NetworkBridge.lua:18](../../../../../../../Mod/NetworkBridge.lua#L18)及Start局部；Sender4–5、BackgroundRoutes init205–211会话状态 | 完整UI当前路线+Gameplay验证→store/facts可信→view发布；既有epoch/seq/replay保护保留；第一次采样不等于所有消费者已重建 |
| NetworkRecoveryModel/Cell/Store | 当前仅入包/独立测试，生产无接线 | 不是正常cold真历史来源；不为满足旧S9任务而接入；OD4按实际职责退出，不承诺跨构建读取 |

源码能确认哪些tables是会话局部、哪些地方读取载体以及Store保存API；**不能从这些代码静态证明原生engine在加载的哪个时点已恢复完整Modifier效果或ref**。本轮没有证明存在同版本不可避免例外，也没有理由选新的cold收益政策。

## 2. 逐家族T0：不要把当前代码描述成统一cold hold

以下为静态可达条件，不是新实机复现。`COLD`表示当前会话没有W；样例不假定正常存档真的已有新增来源退出。

| 家族／条件 | 当前实现T0 | 证据 | 目标／禁止 |
|---|---|---|---|
| Commerce，拓扑尚未有可用视图 | 没有previous+samples时网络assert失败，hold读取已安装Gold；有W时continuity只处理确证减项 | [Mod/Commerce.lua:183](../../../../../../../Mod/Commerce.lua#L183)–198、281–289、330 | 正常cold持有init责任；不将已装Gold标作当前证明 |
| Commerce，拓扑VERIFIED但来源暂不可读且无W | 可读source有best则Finish并写较小K结果，标RETAINED；某有效domain无best则resolve抛错，整城hold；self可能使best存在 | [Mod/Commerce.lua:244](../../../../../../../Mod/Commerce.lua#L244)–279、338–356 | OD-1禁止用正常未完成来源写部分低值；完整F后幂等。异常warm来源独立处理，domain失败不无证拖无关domain |
| CultureNetwork，cold无可用拓扑 | old载体在initialize读入；plan失败无可用negativePlan则保留old并报错 | [Mod/CultureNetwork.lua:230](../../../../../../../Mod/CultureNetwork.lua#L230)–244、298–314 | 正常重建不造空union，不用snapshot loaded作为权威 |
| CultureNetwork，拓扑VERIFIED、部分source不可读且无W | source空set+UNKNOWN参与union，可能从I改写为K的count；不是统一hold | [Mod/CultureNetwork.lua:137](../../../../../../../Mod/CultureNetwork.lua#L137)–174、185–204、249–270 | 同上；恢复完整来源后按文明set union/count，不叠同文明重复 |
| Culture负事实continuity+noW | 需本会话Bridge已先形成VERIFIED input后prune；仅在相应路径下可出现已安装n被不完整集合重写；不声称冷启动第一步必然清零 | [Mod/NetworkBridge.lua:215](../../../../../../../Mod/NetworkBridge.lua#L215)–235；[Mod/CultureNetwork.lua:190](../../../../../../../Mod/CultureNetwork.lua#L190)–203 | 分清首次证明／之后真实负事实，先证A何时退出 |
| Standardization | old.applied从native读入且loaded；continuity时old.loaded或无removed整体保留；即使拓扑确认，任一reason（含catalog warning）也触发cold aggregate hold | [Mod/StandardizationEffects.lua:165](../../../../../../../Mod/StandardizationEffects.lua#L165)–207、227–244 | 正常cold不先削I；分类warning与不可读/无效分开。完整事实后按target max幂等；不用无终点loaded hold代替完成责任 |
| Standardization本城+网络 | pending时本城新正值也被冻结；单source warning可冻结整个组合 | 同上194–206；warning138/144/146 | 初始化屏障后，合法本城和独立target按真实依赖更新；保max，不将self+remote相加；不擅自跨当前D1过渡合同 |

## 3. 修订NET01–NET06

| ID | 前提／目标 | 输出及交易 | 完成／失败责任 |
|---|---|---|---|
| NET01 正常拓扑变化 | dirty立刻使严格证明失效；共享owner在可靠阶段重采样；只发布完整可消费新事实 | 尚未有新可靠计划不改旧applied；不是“当前READY”；未完成不得新签交易 | shared持有采集→发送→ACK→专业接管全链ticket；首丢/同值/第二变都可完成 |
| NET02 正常同版本cold | S/I恢复＋F/索引重建；未完不动I；完成核对预期不变 | I是已恢复效果，不是当前network proof；不新授权交易 | N-COLD时序实证待补；具体加载/Store/Native事实完成通知，不以时间当事实 |
| NET03 warm来源极端失败 | topo可靠，已有同owner/ref/source W且未确认失效；可读新事实与合法W混合 | per-domain max→Floor→sum；culture union；std per-target max，provenance逐来源；混合不冒充fresh或严格交易 | 异常显式，引用/episode失效删对应W；只依相关新证据恢复 |
| NET04 真负事实 | 必须有可靠的owner/ref/身份/资格/route负事实，给出依据和发生时间；缺getter不是负事实 | 严格交易／资格立即失效；登记对应被动撤除。cold聚合I不可拆且无W时，不伪称可逐源扣减，在首个完整可消费快照撤除；有可靠独立分解才范围化更新。其它目标不误清，接收城确认失效按既有exact退出 | 指定owner/触发/完成凭据；权限或presence未知不猜写；不得以初始化无限拖延或把旧I当当前事实 |
| NET05 cold严重不能重建 | 先证已超正常加载窗口，正确phase仍不能解决；没有合法W不得猜分解I | 临时继续**no-write**：原已安装I不改，标记not-reconciled／可见严重错误，不作当前可靠事实，严格交易继续禁止。**这不是选定永久旧全额政策，也未选K-only／清空。** | 明确工程责任及相关新事实/可用性恢复触发；确证必须改变支付/损失政策才最小Owner Packet。不能把静默无限hold记作正常完成 |
| NET06 写失败／receiver未知 | reader/writer权限和成功读回必须独立；partial mutation不是已应用新计划 | 不反射性clear全部或发布0/APPLIED；发布可读实际残留/未知及失败scope；不因此放松native严格性 | 有界错误责任、准确写前后证据；重试要新证据，不能盲补建/重放native |

**负事实辨别例：** 若A保存前已失效，S/I理应已反映；若仅A初始化getter失败，属于未完成；若读档后A真实失效，按新事件处理；若没有新事件却S/F矛盾，先查native恢复/写入/保存顺序。旧例“A退出B未就绪→必降20到10”不作为正常cold验收预期。

### W的有界生命周期

见证键必须包含receiving owner/city/ref/episode、source引用和domain/target/family；同键替换而非累积快照。保留范围仅当前可靠拓扑工作集和仍在办理的具名责任，同会话引用/来源确证退出立即失效，cold清空，不按时间自动“恢复”。容量在O3首片以实际路线128/负载16384限制和三消费者最大工作集计算并记录硬上限/逐source数；该数尚待T03本地测量，不能声称已证明够用。溢出显错且停止无证接纳，不截断集合后冒充全结果/交易证明，也不清既有载体。会话W、pending票据与实际applied记录分别核容量/退出，避免换名成为无边界中央hold。

## 4. C3精确后继与必要验证

C3修订只澄清已批正常恢复合同：初始化期间的可靠负事实立即改变严格资格，但不可拆的被动整体不会被虚构分解；首个完整可消费快照完成已登记撤除。NET05在未获新政策前保持no-write、显错、未对账、不可交易。恢复是正常职责，未运行新代码或原生测试。

- [Mod/NetworkInput.lua:97](../../../../../../../Mod/NetworkInput.lua#L97)–109 的UNKNOWN role会进入输入provenance但被Bridge derive过滤（531–536），371–374仍可effectAvailable。目标保留未知参与范围，不能将过滤后集合冒作完整确认；与无关已证作用域分开。
- Commerce360–365／Culture274–276在部分写失败时clear全输出必须单独处置；值可被现有二进制编码表达，并不自动解决授权或部分原生写错误。
- LOCAL计划：真实Store＋Bridge＋三消费者，同一个保存快照重建；cold topo未到／ACTIVE或D未完／unknown role／history不可读，在没有新可靠负事实时确认写次数0且不伪交易；全部F齐后等价0写；cold期间真实source退出（立即禁交易、登记撤除、完整快照后扣除）；cold之后真实source退出；超正常窗口NET05标错/no-write/不可交易；warm W混合；写到半途失败的实际残留。为每来源记录confirmed/retained/unknown，应用状态另记not-reconciled/current/retained/error，不能仅RETAINED统包。
- N-COLD：合法当前build新档建立三网络效果，保存前记录已应用；冷启按已有LoadScreenClose、首个publish、LocalPlayerTurnBegin及Store/完整网络就绪边界观察nativepresence/ref/真实产出。只加可拆除观察者时需另行授权，不新定时器；不要求玩家制造异常/掠夺。
- severe cold无法在正常存档制造时用LOCAL验证不乱写，不能声称native已验证其商业取舍。完整时序未证前不得退役相关D1安全职责。
