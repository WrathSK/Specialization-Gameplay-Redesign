# 完成与唤醒责任矩阵：替代旧audit之前必须证明

Status: Stable — `v3.1-review` 调查候选；可审阅，不代表审计关闭、正式接受或实施授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅新增本目录 Markdown；不改旧报告、生产、测试、工具、正式规范或状态；不运行验证／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 1. 责任模型（候选，不是已存在API）

每条待办至少持有 cause、owner/city/ref/epoch、事实/交付revision、作用范围、尝试数和预算、最近失败、终态。词汇为工程候选，不新增中央业务逻辑或通用持久事件日志。pending≠成功、ACK≠效果/扣款/单位成功。正常可延迟范围必须先有实际责任登记；不可用收到任意事件为理由重新检查全城。

- **phase0** RestructuringSync→NetworkBridge 必须同步完成才能ACK，保留 `EmitDerived` 特许窗口；不能因启动先后改变顺序。票据按回调实际快照生成，不能只用owner合并键。
- **普通消费者** ACK只表示owner可靠登记了有限scope。登记失败仍由发送层保责；登记后失败由owner保责；false/缺target/FAILED/SKIPPED不得当成功。成功sibling不因别人失败重跑。
- 新的真实变化可升级ticket；旧ACK不得清掉新scope。退出/close/引用替换处理与注销明确，mandatory cleanup不当可丢订阅。
- `GameCoreEventPublishComplete`只能flush已登记工作，不能自行制造重试原因；同一cause同revision一次尝试，回调重入只允许一次追赶快照。异常不自动在下一帧/每回合复读。
- OD-3本地回合开始候选上限：**只在证明合法短暂未就绪且没有更直接通知后**登记；每scope每边界最多一次、同一证据最多两次后显式错误停止自动尝试。2是待LOCAL/原生证据核对的工程上限，不是“两回合即可认定损坏”。新可靠证据才可开启新ticket；旧失败反复自己制造新ticket不合法。

普通接管的结果建议明确为REGISTERED（已持久于本会话责任队列）、IRRELEVANT（已可靠判断不相关）、UNAVAILABLE/ERROR（未接管）；不能把旧nil/false直接视作成功。只有前两种可释放发送方ticket，IRRELEVANT需可靠scope依据。队列沿当前FC/Bindings的2048 scope硬上限作受审起点，不默认增容；超限显式错误并保责任，不截断丢通知。字段名/最终容量由Primary在实际工作量证明后确定，不新增Owner投票。

## 2. 原因→确切完成边界→owner→限额→旧职责替代

“事件存在”只由静态注册证明；送达/签名/读取时序未实证的格子明确OPEN，不能据此先删除旧fallback。

| W | 原因／当前证据 | 完成边界与目标owner | 有界范围／错误处置 | 取代旧职责及gate |
|---|---|---|---|---|
| W01 | Gameplay/Store未启动，UI先到；RuntimeWork493–510只粗略latch | composition Seal仅登记完成；Store HistoryStartStatus从WAITING到可靠FRESH/EXISTING后，由生产初始化owner主动发availability；LoadScreenClose/首publish是候选尝试边界，不预设全就绪 | 每加载一次init ticket；真实失败FAILED、依赖SKIPPED；永久HELD不循环 | StartReady隐式每回合attempt/首load全扫：保留到typed完成通知证明可替代 |
| W02 | UI首包在Gameplay可接操作之前丢失 | 已有LoadScreenClose、LocalPlayerTurnBegin及原生IsTurnActive；Sender/Bridge epoch+seq ACK | 每epoch/turn每具名生命周期至多一次发；无ACK只允许具名新可用性；完整proof验证不减 | NET-2现有恢复保留；LOCAL lost-first组合＋必要N-COLD |
| W03 | 相同内容但signal更新／首ACK拒绝 | dirty后UI相同snapshot新signal、Bridge acceptedSeq/inputVersion，Sender确认精确receipt | `failedTurn`不得把新证据整回合屏蔽；按attempt identity+失败原因保拒绝预算；非法相同包不重放 | Bridge PlayerTurnActivated925–930不得先删；先证signal-only/同值恢复 |
| W04 | 正常路线新增/到期/重建 | 现有TradeRouteActivityChanged/Added/Removed等→BackgroundRoutes dirty→publish/playback flush→完整NETWORK_PUSH→Bridge可靠发布 | 单玩家dirty合并；routeunit滤相关；≤128/≤16384上限另W16；不增加frame采样 | 接班完整后删除普通turn Refresh重采样，而非删必要订阅 |
| W05 | ACTIVE UNKNOWN_GOVERNOR | EffectiveFacts117–121无独立恢复publisher；NativeFacts59起四Governor事件是相关新事实；**恢复同值仍须生产availability通知** | 资格owner按相关city/owner已登记scope；不能只等raw值变化；正常UNKNOWN查root | O1/PU10须补typed恢复来源，再去consumer turn补算；若合法短窗确证，才OD-3窄drain |
| W06 | D/原生建筑事实尚未可读 | DistrictCompleteness204–227当前dirty/新turn重捕获；建筑/区域事件及load完成为采集入口，成功capture须发布availability（值相同也唤醒） | 同ref+generation，读中写失败不缓存为成功；仅已登记capture scope | 替代每回合深读前先证相关事件后getter可靠窗口；缺原生时点列N-COLD，非一律turn扫 |
| W07 | 新城未admit／首次专业完成尚无可靠对象 | Store现有CityInitialized/CityAddedToMap、OnDistrictConstructed与LoadScreenClose；目标Store admission/completion owner受控提交后主动唤醒 | 每candidate固定ref/ticket；不把未admitted当NONE；wrong-family先可靠过滤，不能全pending毒化 | PU07/O4；不猜first、不自行持久新证据；新native时序缺口才N0 |
| W08 | 专业模板/Insights等历史尚未完成读取或合法写后相同结果 | Store模板/insights commit及已有SourceChanged；目标专业history owner发布成功完成/availability，不让Bridge猜业务 | 每真正历史revision+ref；缺历史是错误而非等待回合；不把empty未知合法化 | 取代History turn scan/SourceChanged旁路冗余前证通知闭包 |
| W09 | 暂不可读的信誉独立叶子 | Store校验器/依赖明确恢复通知；OD-2合法身份退出是独立可信业务事件，不需等待旧叶读回 | 同parent/ref；R0窄政策不改变历史；CHECK_UNKNOWN/DEFERRED≠叶永久损坏 | PU06/O4；不安排每回合“看是否好了”；合法退出不遗漏reset |
| W10 | Bridge EmitDerived失败或消费者异常 | O2生产投递owner保留未接管ticket；注册成功/依赖可靠、一次相关完成或明确错误后新证据唤醒 | 每callback+scope/ref；旧通知水位与成功登记水位分离；上限与超限显错 | PU03；不是简单挪lastNotifiedProof赋值；关闭trace也能看失败 |
| W11 | 普通Binding→owner返回false、target缺失或owner busy | owner AcceptChange明确REGISTERED；Start失败显错、不假恢复；busy已有有效责任登记后下一safe drain | consumer/city/ref ticket，失败scope保留；成功siblings不再读；禁止一次后silentdrop | O2覆盖FC/Bindings、NewAudit、Commerce/Capital/StdEffects/Culture四flush；再去turn全重算 |
| W12 | phase0重入／EmitDerived合并行 | RestructuringSync先，Bridge后；同步完成后phase1；新无关cause下个snapshot | percallback不可变ticket，最多一次追赶；phase0失败不伪已发布 | O2/O5；明确缓存phase：同安全读取阶段共享，新阶段不复用越界facts |
| W13 | GreatWorkFacts/Dialogue transport ACK失败或同值 | GreatWorkFacts198–245已有只成功清pending先例；Dialogue paired sample/ACK/generation需同样接班 | 已登记city/ref，有界catch-up；不能随probe退出丢ACK | O2/O7；不直接把“callback未throw”当通用success（false须明确合同） |
| W14 | 三个一回合项目生产状态UNKNOWN／reader handshake失败 | 已核实的城市生产相关事件＋TimedProjectReaders有效backend/reader新绑定、既有必要init完成；Governor有序loss/return监听保留 | 仅项目城市/round；UNKNOWN非取消/完成；reader delivered先latch后wake35的失败接续纳R2静态复核 | PU09/O2/O4；不新增每回合全城poll；Claim真early不需内部timer；marker处理见A16 |
| W15 | 负事实withdraw部分失败／exit/recapture | 已有Store受控exit/return证据及新ref/实际cleanup确认；foreign与原回归端点授权严格 | 每loss generation、每必要owner；observer失败不能无证阻主流程，但有真实cleanup的owner须先迁责 | PU08/O4/O7；现有最多3次退出尝试不是无限重试许可；未证端点不重新清理 |
| W16 | 路线/负载超128/16384，定义/容量错误 | Sender53/59确定容量失败；明确unsupported/error，改善编码/上限属另受审工程切片 | 不截断当前集合、不假空网；同失败指纹不反复发；新输入降低容量后可靠再开 | O3/O8；不作为正常永久PENDING，也不增高上限掩盖问题 |
| W17 | Carrier原生写入/读回不确定 | 生产writer持写入结果/错误和新可靠readback；不可逆native只由原业务凭据恢复 | 限family/domain/target；不清零全部，不以unit后来不在场断言没发过 | O3/PU05/O4；旧错误保护迁走后才删诊断error helpers |
| W18 | 已确证合法短窗，但无更直接通知 | **仅证据登记后**在Events.LocalPlayerTurnBegin或Gameplay相应已核实本地开始边界drain已登记scope，不能并用二者双试 | owner/ref/ticket、候选最多2次；耗尽ERROR，历史UNKNOWN不进入 | OD-3例外表，逐格记录原生窗口证据。当前没有把所有UNKNOWN自动登记W18 |

## 3. R2实施证明范围

当前丢失点：[Mod/FactChanges.lua:182](../../../../../../../Mod/FactChanges.lua#L182)–203先换队列再callback；[Mod/FactConsumerBindings.lua:6](../../../../../../../Mod/FactConsumerBindings.lua#L6)–9/75–122缺target被跳过且清error；[Mod/RuntimeWork.lua:89](../../../../../../../Mod/RuntimeWork.lua#L89)–99取出pending后不保失败。Commerce491、Capital308、StdEffects311、Culture384四flush同类。Bridge133–142水位早于EmitDerived。[Mod/GreatWorkFacts.lua:198](../../../../../../../Mod/GreatWorkFacts.lua#L198)–245提供实际成功保留/重入先例，不能未经修改就称已覆盖全链。

LOCAL计划须跑真实生产者→FC→Binding→真实owner，包括throw/false/missing/FAILED/SKIPPED、两城市一成一败、failed owner后注册、同值恢复、旧ACK、回调写入导致新change、exit/close/load失效；记录调用数/捕获数，成功sibling没有额外deepread。所有13个NewAudit owner和四flush做实际调用清单后按合同迁移，数字是外审估计，不能只用一个stub代表全部。phase0同步及共享读取阶段T02必须真实集成验证。

## 4. 去旧入口前的清单

每个旧turn audit/Bridge Refresh记录“具体必要工作→上表W→新owner→LOCAL证据→是否尚缺native”。任何OPEN未接班，保留该必要入口并明确范围，不整体宣称O2/O3已完成；不得把旧入口删掉后靠“正常最终会刷新”补叙事。
