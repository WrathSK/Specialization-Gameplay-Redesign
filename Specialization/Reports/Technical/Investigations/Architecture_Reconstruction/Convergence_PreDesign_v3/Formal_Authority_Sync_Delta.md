# Formal Authority Sync Delta：精确修订候选，未应用

调查材料／候选契约，不是正式架构权威或实施授权。

状态：Stable（本轮证据版本可审阅；重大决定未关闭，不称 v3-final）｜维护者：Primary

日期：2026-11-02｜源码基线：`9addf8d01dcbcb46d28e59ffa5625950f4540e57`｜正式基线：D0058／A0183／S0866。运行包仅引用记录 B399.426，本轮未重新核验部署。


[Owner决定包](Owner_Gate_Stop_Report.md)｜[源码索引](Gap_Matrix_v3.md)｜[最终计划](Option_B_Final_Candidate_Plan.md)

## 应用规则

H3为Owner已确认目标，v1/v2/v3均非正式规范。当前D0058/A0183/SAFE004保持原字节。本文件只提案：重大决定闭环→Owner认可最终候选→Claude独立审计及finding处理→Owner再次放行并单独明确正式同步/实施范围，才按现有D/A修订流程处理。审计PASS本身不授权写入。

不提前分配新的D/A编号/acceptance日期，不重算并宣称hash已接受，不修改Status/Authority/ContextLock。受保护已接受Content/历史修订不就地覆写；正式执行时按既有successor/freeze流程生成新版本并更新当前入口。旧报告和U1原始决定不改写。

以下文字为候选替换/新增段落，不是代码已经做到。源路径均在Specialization下；行号指当前基线。

## FS01 — 正常/异常与批准阶段

**位置：** Design/Specialization_v0.1_Design_Spec.md:14–26，下一受批Scope/SAFE；Architecture/Specialization_v0.1_Architecture.md:16–27/634–646；Workflow当前实施/验证约定的相应说明。

**现状：**旧Scope／A0183仍记S2–S10及广义恢复目标；当前Status仍在B399等候；不能误用旧授权开始本轮实施。

**拟新增：**
> 架构收敛以Owner确认的最终目标为准。正常相关事实由拥有层可靠采集、登记变化与交付；Mod自有历史/统一ACTIVE等正常路径的UNKNOWN、非法状态和损坏须显式报错并定位根因，不作为长期业务状态。事实拥有层可处理经证实的短暂原生未准备窗口；极端保护不等于根因已修或验收完成。最终候选经Owner认可、独立外部只读审计、发现逐项闭环、Owner再次放行及明确实施授权后，才执行获批Pre-U5、U5基线与OptionB。历史授权、报告发布和审计PASS均不自动授权本轮代码/规范/部署修改。

**批准依赖：**H3已定；具体新revision和实施范围仍后续授权。

## FS02 — 统一 ACTIVE 与正常 Potential

**位置：** Architecture/Specialization_v0.1_Architecture.md:71–88/172/186；Design/Shared.md共同资格段落及下一Shared Content相应条目。旧资产重组P−1规则（Shared_D0058.json:128、RestructuringModel）保留。

**拟替换/补入：**
> ACTIVE由统一事实拥有接口提供，专业只消费当前角色/等级及引用，不依赖Governor实现细节。当前底层Ceiling采样须先解决真实时序/引用/初始化错误。只有已证明必要且获准的极端被动用途，可由统一拥有层使用同一有效引用的最后可靠原始Ceiling结合当前可靠Potential/身份推导；不保留旧派生ACTIVE作新资格，不建立各专业或复杂跨事件总督缓存。未来管理容量只作为接口可替换来源，不在本次实施。
>
> 同一合法普通进度episode的Potential单调递增；非法下降是严重错误，不建立常规下降补救。既有明确批准的资产重组/身份转换开启独立episode并沿原规则处理，旧输入不得跨越。

**原因：**替换v1/v2错误常规下降示例和分散Governorfallback提议；不是新增管理容量玩法。

## FS03 — 网络可靠正常发布／D1过渡退出

**位置：** Design/Network.md:47–59中:49/:53/:59；Architecture/Specialization_v0.1_Architecture.md:138–148中:142/:144/:146/:148；下一Shared Content网络条目。

**拟替换核心：**
> 路线dirty立即使依赖当前证明的严格资格失效并登记共享采集/交付责任。共享网络拥有层在取得完整可靠拓扑后，才发布专业的正常可消费更新。经证实的短暂未准备在拥有层凭明确事件/初始化边界完成；错误/未准备不伪装为空网或普通正向输入，持续失败须显式报错、查根因。确认负事实、来源/接收资格及owner/reference退出独立及时处理，不等待未知sibling。
>
> 现行D1及组合物理载体保护在迁移阶段保留；只有正常可靠链、同值恢复/cold/丢包/第二变化/负事实、严格交易与保留/禁用/真实移除差分通过并经Owner批准后退出。过渡期不以新目标私自绕过现行组合保护；最终不能以成功冻结或共享层隐匿pending当作收敛。非网络本城效果不得因无关网络长期阻塞，标准化仍保持既有max公式。旧效果不能证明current网络或授权新交易；已签断路可续合同不加新网络门槛。

**批准依赖：**可靠正常目标/D1过渡已批；具体退役事实未证；相关D2处置须FS04闭环，不能现在删除保护。

## FS04 — D2 分支文字（OPEN_OWNER_DECISION）

**位置：** Design/Network.md:55/57；Architecture/Specialization_v0.1_Architecture.md:18/145；下一Shared网络条目与原coldsource完成义务。**先ODP01，不应用任何分支。**

- **若选A：**“正常根因链优先可靠重建；极端、引用仍有效的来源读取失败可沿D2保留上次实际应用贡献，已确认负事实优先。必要cold归因按受批派生见证保存，非永久成就/交易凭据；exactshape、引用、版本、写读回及双向失败保护验证。暂留成功不作为异常根因关闭。”
- **若选B：**“仅保留经界定的会话极端来源保护；冷加载优先从引擎及正式历史重建，不默认新增旧应用归因持久层。无法及时重建时按Owner明确的异常输出/隔离规则处理，不能假分解旧aggregate、把未读作0或误撤无关贡献。” **冷异常与sibling条款尚需选择后写全，不能仅凭此摘要送final审计。**
- **若选C：**“退出来源分解保留，正常只发布可靠输入；严重失败在拥有层显式停止不安全依赖。按Owner明确的确认负事实/已应用效果处置规则处理，不用旧混合贡献伪装current。” **替代异常/负事实处置尚需Owner明确，不能默认为全清。**

真实Insights／模板／L／合同收据不属于可随D2退出的数据。Standardization-only冷例外的保留/退出须与所选分支一起精确裁定，不能自动推广到所有专业。

## FS05 — SAFE004 与历史错误：替换零基线程序目标

**位置：** Design/Specialization_v0.1_Design_Spec.md:26 SAFE004；Design/Content/Shared_D0058.json:227–235的后继ABILITY_SUBRECORD_RECOVERY；Architecture/Specialization_v0.1_Architecture.md:21/640。

**拟替换文字：**
> 基础identity、reference与record envelope严格保护；单能力错误在可安全分离时隔离，不拖累其它有效能力。Mod自有历史在正常路径必须可靠；读取错误/损坏/非法状态应显式严重报错、保留有限证据并优先定位采集、引用、时机或提交根因。不得猜历史、补造收据、清记录回零、用静默长期HELD或无界retry作为完成方案，不建设全面零基线恢复程序。
>
> 保留经过实际权威证明的确定性重建和合法延迟生命周期处理，逐项审查而非机械删除；临时不可读不覆盖原字节，合法新建初始记录不等于损坏后回零。未知付款/创建/完成结果不可重放或抹除。缺安全权威时只阻止受影响不安全路径、报告具体边界；新恢复权威/持久见证需Owner另批。

**原因：**H3/DEC06C明确取代旧广义合法零基线完成方向，不改历史U1原文；保留StoreSubrecords/recoverDeferred真实合法机制。

## FS06 — 信誉权威／极端R0与严格事务（OPEN_OWNER_DECISION）

**位置：** Spec SAFE003:24；Commerce_D0058.json:263/281/293的后继条目；A0183:639；Architecture/v2/Commerce_Preparation.md:200。

**所有选项共同的拟文：**
> 信誉是Mod拥有的可靠永久历史，不是等待原生变化的普通事实。正常未知是严重Store/身份/历史错误，须显式报错、保留原证据并查root。不得改写年龄为0、发明历史或追改已签合同。STABLE公式不依赖R，不因共用报价实现新增资格依赖；其它current资格、余额、收据和不可逆保护保持。

**若ODP02启用统一继续，精确补入：**
> 当且仅当parent/身份/引用和Commerce配置可靠、仅信誉叶子不可用且无未决native结果时，按Owner批准的极端业务政策暂以有效R=0进行所有R相关计算，包括被动与新风险条款。必须保留“历史未确认、值来自异常政策”的可定位状态，不伪称保存R已知；此为严格交易所需R输入的显式窄业务例外，非保留旧值授权。新合同锁定已选R0条款，历史恢复不重算旧合同。该政策不涵盖其它未知输入，不构成通用恢复或正常UNKNOWN许可。

**若不启用：**明确停止受损R所授权的不安全路径并报错的范围；不把v2模式政策当已批准一致容错，也不阻断无R依赖的安全动作。当前Formal未有无条件VENTURE绝对禁令，不虚报冲突；需要裁定的是例外启用/严格原则边界。

## FS07 — 七责任与历史 owner

**位置：** A0183:20/67–106；专业历史合同的当前owner段落。

**拟替换/新增：**
> 专业历史模块拥有schema及合法业务转换；共享Store负责所管理城市记录的身份/parent/token/envelope、CAS、readback、opaque sibling保留和提交次序。已有独立Industry/Crew/Treasury等权威owner不机械收编。“Store负责可靠持久化”不等于Store定义所有业务规则，也不保证跨City/Unit/Treasury的天然原子回滚。
>
> 专业只以当前事实派生/撤除Carrier，永久历史与瞬时收益分别处理。纯delegate不改变身份token、不写其它owner记录、不直接调用native money/unit、不重放不确定完成。

现有失城/夺回/重组各业务结果不在本批擅改；root导致需新端点清理权威时另提Ownerpacket。

## FS08 — P03/P06 可靠交付

**位置：** A0183:168/171，当前public更新/临时状态条款；Workflow RuntimeImpact/targeted gates相应验证说明。

**拟文：**
> 确认相关变化立即登记责任；可合并冗余重算但不得丢处理中后续变化。协调层只在专业可靠登记pending或同步证明无操作并返回匹配ACK后解除该版本交付责任。ACK不证明效果应用/交易资格。未接管责任显式保留；专业接管后自行完成、核对、报错及凭相关新证据恢复。旧ACK不清新revision；无界retry、静置创造预算、中央重放业务均禁止。session队列按已有可靠初始化边界重建，不增加通用事件日志存档；不可逆专属收据不变。

## FS09 — 专业声明／初始化次序

**位置：** A0183运行入口/集成合同，现Bindings与startup说明。

**拟文：**
> 四专业及共享能力拥有者按明确composition清单在成功启动后声明稳定consumerID、fact/topic、scope能力与接管入口；共享能力不按四专业重复注册。中央统一校验/注册/分发，失败启动不得残留半订阅，重复/无效类型/missing/FAILED/SKIPPED显式错误。保留RestructuringSync→NetworkBridge phase0和现EmitDerived精确时序，sealed后才首次drain。独特原生完成/历史监听保留。不自动发现插件、不从kind推断业务资格。

字段名、容器、Lua文件布局是工程实现，不再提交Owner选名称。

## FS10 — P3生产／诊断退出

**位置：** A0183 P08/P09:173–174、D12:643，后续RuntimeImpact/T gates观察成本/退役条款。

**拟文：**
> 可选Probe/Collector/Diagnostic不能承载正式计算、历史、交付、Carrier、事务或生命周期清理的必需执行职责；长期价值先提取为生产拥有者。观测只读稳定接口，关闭/移除仅丢诊断。实际缺file/global而非仅开关，startup/资格/记录/Carrier/不可逆结果/接管恢复/业务UI差分必须相同。生产writebarrier、必要Flight bookkeeping和已有受批GC控制须明确归属并保持策略，不能作为计数器一起删除。按真实职责迁移Q1–Q8、exactownedcleanup和双部署删除回滚后才撤旧层。

不按Probe数量或Modifier数量验收；独立footprint专项不在本同步范围。

## FS11 — 巨构工程学与工程研习分离

**位置：** Architecture/v2/Industry_Preparation.md相应巨构/历史段、A0183:92–100与后继Industry内容中的技术引用说明；不改变数值公式。

**拟澄清：**
> 巨构工程学仅依赖当前玩家时代、资格/引用和静态时代定义；原生EFFECT_ADJUST_WONDER_ERA_PRODUCTION按当前建造奇观的时代筛选。当前实现无需Lua读取生产目标，不依赖已建奇观N/E/L。工程研习的全国完成奇观时代E是另一独立严格历史输入，完整覆盖要求不变。

当前代码已匹配此区分，不为形式统一添加queue采集或历史依赖。

## FS12 — D11应用展示与性能完成标准

**位置：** A0183:150–158/642，P05/P09及结项验证条款。

**拟文：**
> UI显示owner实际applied、当前资格/来源和错误；候选/preview/最后确认应用/未知必须区分，不能由年龄或L自行算作当前收益。UI context独有事实采集仍只为共享事实来源。
>
> 以必要工作、最小浪费和有限原生可接受性为标准：处理已证重复采集/无关wake/无效写/不合理放大，保留必要通知与历史发现。不设任意CPU/RAM/%门槛；STATICworkshape、LOCAL计数、USER_NATIVE感受/测量分层，不把全进程内存当本Mod归因。所有必须差异关闭或有证据具体获批例外，不留无结束条件双路径。

## 同步审核清单

每FS：Owner目标是否已定／是否依ODP；准确受影响段落；后继文件与旧冻结保留；纯语义/行为变化是否明确；依赖接口/加载次序/测试；接受hash及Status/Authority更新仅在后续获批正式同步批次。新R0/D2例外不能提前写成accepted；本轮不生成新正式版本或应用patch。
