# P0-E2 — 进度保存适配：具体计划

Status: PLANNED_NOT_AUTHORIZED。用户本轮授权推进计划，不授权runtime实施。
Baseline: B094.121 / modinfo121，runtime source a113a6096e141112a5a7ef67453afd8cdc00ac3c。D0035 / A0161；四专业v0.1范围不变。

## 1. E1结论与本批切片

E1已验证：独立Game记录可保存；Gameplay直接识别所测单次自由城转移；B094冷加载恢复单城映射。仅此原型范围USER_GAME_TEST_PASS。正式多城cityKey、收复/连续易主/征服/解放/同地重建、转移中断恢复没有普遍原生保证。

因此不把E1实验编号直接升级为全局authority。本次推荐授权的E2首段为：**一座显式选择、原Owner/引用/旧凭据完整、已经建立四专业之一的城市，在同Owner范围迁移进度并继续既有移民投资，冷加载保持结果。** 其它城保持旧路径。

这是E2的受限首段，不等于总计划中完整新城/跨Owner保存适配全部完成。后续新城首次专业、全城登记、跨Owner适配仍需收束；不因首段PASS自动进入F。既有能力计算不改，既有收益仍由原consumer写入。

## 2. 实际读取链与必须接管的边界

| 当前模块 | 实际职责 | 本段处理 |
|---|---|---|
| BindingProbe | Game每Owner总账+City token；CityBuilt分配DEV序号（上限32） | 未迁移城保持；已登记城/位置及转移待确认范围先由新保存路由拦截，禁止当新建城再分配 |
| CityJournalProbe | 首个合格专业区域锁Identity及基础Potential1；City记录 | 已迁移城的事件/加载/故障GAP写入跳过；保留冻结来源，不双写 |
| FreshBindingHook / CityFlowProbe | 串接新城Journal；三阶段提交、load resume、SupportFacts | 新城仍旧路径；已迁移城所有写入口/resume提前跳过，避免冻结旧记录触发player-wide halted |
| EffectiveFacts | Flow基础Potential + 已完成投资凭据数；Governor产生ACTIVE | 接入唯一保存路由：迁移后只读新记录；旧路径仍服务其它城；接口输出与收益语义保持 |
| InvestmentAction | Prepare/Confirm、INTENT→单位标记/销毁→CONSUMED_CONFIRMED→receipt；load finish | 对迁移城替换读写后端与revision校验，保留单位消耗和receipt语义；旧City ledger不再写 |
| CurrentSpecializationFacts | EffectiveFacts只读外观 | 复用，验证UNKNOWN/mode不会被解释成NONE |
| NetworkInput / SampleLifecycle | 直接读旧token，Network还有“无Flow=未追踪城”分支 | 使用新路由的引用/参与状态检查；迁移有效城不得因旧Flow缺失被判NONE，HELD不得走新城默认值 |
| SourceYieldProbe | 直接读取CityFlow.SupportFacts | 迁移城改读统一基础事实，未迁移城保持；不得继续越过路由 |
| Standardization/模板及其它永久成果 | 独立专业ledger，并非全在EffectiveFacts中 | 本段不迁移模板/Dialogue等；不得声称易主后完整保存。所有权不推导 |
| CityInheritance / InheritanceShadow | 被隔离旧继承writer | 保持隔离，不调用Start/继承projection |

已完整阅读Journal/Flow/Investment/EffectiveFacts/CurrentFacts/FreshBindingHook，核对Binding写入段与Gameplay启动/分发，搜索所有直接旧key读取点。正式实施前按W0001补读精确受影响消费者，不默认全库重审。

## 3. 新保存authority：小型专业进度记录，不建通用框架

拟一个独立版本化Game Property `SPC_CITY_PROGRESSION_V1`，由一个Gameplay模块持有。本段只允许一个显式登记的测试城；后续扩容另审，不创建每帧同步或第二份可写历史。

- root：schema、revision、单城record；new key不存在不等于迁移成功。
- stable record key：由已验证原DEV token在本存档命名空间确定；仅支持本段受控登记，不宣称任意城市永久ID。
- origin/current reference、迁移来源owner/token/关键revision与来源摘要；原锚点固定，当前寻址单独保存。
- progression：Current Identity、Permanent Potential、first事实、mode；UNASSIGNED/SPECIALIZED/REALLOCATING区分。首段只导入SPECIALIZED；REALLOCATING仅合法类型和拒绝错误分支的合同，无创建Action。
- historical maximum：只记录已有证据所支持的下界及provenance，过去更高值未知，不把当前P伪造成完整历史。未来投资更新当前专业已观察最高值。
- investment：原receipt→unitUID集合、revision、可选pending；无单位/UI/carrier作为唯一authority。Potential与凭据数量必须一致。
- migration state：PREPARED / ACTIVE / HELD，与Gameplay mode及事实validity独立。ACTIVE这里指存储接管状态，不是专业ACTIVE等级。
- 专业ACTIVE不持久化，仍由当前Governor和Potential计算；数据暂不可用≠等级0。

Game记录随save恢复，不用外部文件/城市名称作key。单位删除等引擎副作用不是一次Game Property写入所能原子覆盖的，保留现有失败暂停语义，不承诺任意崩溃exactly-once。

## 4. 明确导入合同和切换顺序

可导入：当前原Owner、当前引用/token/Binding唯一匹配，Journal TRACKING、Flow DONE且逐值一致、四专业Identity及基础P1、投资receipt有效且无pending。首测优先Research P1–P3，以便在同次测试继续投资；P4可本地验证导入。

拒绝：未专业化/无追踪旧城、City记录已因易主丢失、任何pending/GAP/冲突、缺失历史、原Owner改变。**E1记录/截图/当前建筑不能代替缺失旧账本。** 有模板不代表本段导入模板；原模板继续其原Owner路径，不复制/扩散。

顺序：
1. 手动请求，读取不可变来源快照，验证资格；没有新效果，也不消耗单位。
2. 写新key PREPARED（完整目标及来源锚点），读回确认；从PREPARED开始所有目标城旧进度writer必须暂停，避免来源在切换中继续变化。
3. 再验证来源未变、目标仍同一城、无单位事务；提交ACTIVE并读回确认。
4. 统一read route切到新记录，旧City值冻结留作证据，不删除、不写回、不作为自动fallback；不发布虚假的0或重复收益。
5. 重复导入返回已完成，revision不增。PREPARED读档仅在同Owner/来源完整一致、无任何副作用时允许完成原导入，否则HELD；记录损坏、schema不识别、来源改变不自动重建。

失败后不能自动回到旧writer。切换marker与目标记录必须在同一Game值内，避免多key提交顺序造成两个authority。Gameplay初始化必须在旧writer/旧load hook可以运行之前恢复路由；恢复未就绪时暂停目标写入，不将缺读解释为未迁移。

## 5. 迁移后继续投资 / 发布

Prepare读取路由提供的同Owner事实、record revision、receipt集合；不依赖冻结City ledger判断新投资是否变化。Confirm再次验证，沿用原INTENT/单位标记/销毁确认/receipt提交顺序；每步只写新后端，保持原消耗规则与Potential上限。

读档：已确认消耗凭据可幂等完成；INTENT无法证明消耗则HELD，不自动销毁第二次或增加Potential。不放宽原单位ID复用保护。旧load恢复循环必须跳过迁移城，不能双finish。

更新后复用既有事实变化通知，只有Identity/Potential/ACTIVE或相关输入实际改变才发布。迁移前后相同事实不产生额外carrier churn；Network继续共享derived view，引用加入保存generation/revision时只在需要的事实边界失效。无hover请求、无generic pulse保存/扫描。

## 6. 易主和未支持范围

本段实现不承诺新Owner获得专业进度或永久成果。迁移城发生已确认移除/易主后，Game记录保留，路由变为HELD_TRANSFER；旧source资格按真实owner/reference失效退出，不继续凭旧owner激活收益。当前读取失败不能冒充已确认失效。

只识别同一坐标不足以领回历史；新Owner/收复时均不自动重锚专业账本。E1V2保留为独立实验，不在正式读链作继承许可证。对于已登记位置出现CityBuilt（可能是易主），先暂停新旧首次建立入口，不把它当从未专业化城市；本段不解决该位置后续真正新城的自动登记。

必须本地证明：目标暂停不污染同player其它城市的旧bucket，不触发误清除无关城；确认失去owner/reference时不会残留其正式来源效果。若现有consumer不能区分临时UNKNOWN与已确认退出，实施时扩充必要的明确失效出口，不能靠统一抛错隐瞒。若牵涉新的征服玩法决定，则停止该支路并报告，不替用户制定Legacy。

## 7. 最小文件范围

拟新`CityProgressionStore.lua`（或相同职责小模块）；ADAPT EffectiveFacts、InvestmentAction、Binding/Journal/Flow目标城门禁、SourceYieldProbe和NetworkInput的直接旧存储判断；SampleLifecycle只在引用语义确需时改。Gameplay负责正确初始化顺序和手动导入/摘要诊断；复用现有实验按钮位置、同步旧Tooltip，不新增诊断面板。

收益SQL/carrier/Research公式/Design不变，CityIdentityMapping实验仍独立。旧writer不是全局删除，而是对迁移目标先停后切；其它城市旧行为不变。完整E2新城接管不塞入本段。

## 8. 验证：W0004 L3，仅受影响链

| 本地定向项目 | 验收 |
|---|---|
| P1/P2/P3/P4真实旧fixture导入 | Identity/P/first/receipt逐值等价；ACTIVE按Governor重新计算 |
| PREPARED/ACTIVE重复、重入、冷load、读回失败 | 单authority；不覆写冲突、不丢凭据、不自动回退旧writer |
| 移民投资/重复确认/单位ID复用/两阶段中断 | 只正确消耗一次；不确定阶段暂停；旧City ledger零新写 |
| 同玩家一迁移城+一旧城 | 路由分离，旧城正常；所有写入口/load/GAP/恢复不可漏 |
| 直接旧key读取回归 | Network不伪造NONE，SourceYieldProbe不越过路由；旧样本版本安全 |
| SAME事实与idle/重复通知 | 无新增carrier写/全城扫描/周期请求；新key状态变化才写 |
| 真实投资/Governor/owner事件 | 输入正确发布；UNKNOWN保留边界与confirmed withdrawal分开 |
| History / REALLOCATING fixture | History不等于Current，REALLOCATING不能进入NONE首次建立 |

全Lua/manifest/context、受影响收益/Network/投资/部署安全检查。无需机械重跑所有历史；针对持久中断与重复操作做有限压力/故障注入。原生版本环境同时覆盖缺少table.unpack，避免B093重复。

## 9. 实施后一次最小用户测试

一个独立测试档，一座完整旧科研P2或P3城市，另有一座旧城作为对照：按需迁移→看同样Identity/P/ACTIVE和已运行收益→用既有移民投资一次→另存冷加载→同一简明诊断确认新P、凭据数、存储来源；对照城仍旧路径。一次流程涵盖保存切换与单位事务，不要求用户手算hash或全模块收益。

不默认重复自由城实验；实际易主后的正式玩法不在首段验收。若实现需要原生特定失效证据，本地先缩小后再提出，不能把范围扩成长期综合测试。

## 10. 退出 / 回滚 / 授权

首段退出：目标同Owner记录和投资读写正式由新Game记录承担、旧writer目标零写、收益逐值一致、冷加载成功；未迁移城不退化。报告明确USER_GAME_TEST与本地模拟边界。

回滚使用B094完整包和**迁移前独立存档**。新投资后旧City账本已冻结，不能用旧包继续该档并声称无损；不提供自动反迁移。新key保留不清理，保留所有证据。

无新的Gameplay设计问题阻塞这一个受限切片。需要用户审核的是上述**E2首段scope**；跨Owner/新城/全量兼容仍未包含。通过首段后先报告E2剩余边界与下一计划，不自动进入F。

本轮只计划，runtime/Design/main/运行包均不改，无部署或Gameplay regression。

计划检查：现有context.py CLI的batch枚举尚未包含E2；本轮直接调用同一工具的check(manifest)完成全部schema/hash/authority检查，PASS（151 runtime files）。未修改工具逻辑；实施时只需将E2加入既有CLI枚举，不建立新验证器。git diff --check通过；本轮无Gameplay测试。
