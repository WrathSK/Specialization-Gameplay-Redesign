# Claude Code独立审计入口：v3-final候选（尚未启动）

调查材料／后继候选；不覆盖正式规范。

Status: Stable（可审阅的候选文档，不是工程或实机 PASS）。

维护者：Primary｜日期：2026-11-03｜实际 develop：`719eb61b410765fb6e8703a47840ce3cec3fa823`。正式记录仍为 D0058／A0183／S0866；B399.426 仅为既有部署记录，本轮未重新验包。

**NO IMPLEMENTATION AUTHORIZATION。** 本主题承接原 H3 中文交付；仅新增候选 Markdown，原 v3 九文件及代码／测试／工具／正式规范／治理／运行包均不改。

## 可直接交给Reviewer的任务

你是独立外部只读Reviewer。先确认Owner已经认可本候选**用于审计**；如果没有，不开始。本包目前仅准备交接，未启动Claude，不预填任何审计PASS或Finding。你可以反驳Codex，包括指出候选仍不足以实施。

只读核对正式Design/Architecture、真实代码、消费者、加载、现有测试定义和本计划。不得改代码/测试/工具/正式规范/Status/Authority/部署包，不运行新probe/native/fault injection或启动游戏，不自动修复。所需未执行事实列为最小验证要求。

### 短阅读顺序

1. [README](README.md)＋[Owner Gate](Owner_Gate_Stop_Report.md)：ODP01=B／ODP02=A已定、无新Owner票决的具体理由与授权状态。
2. [Fact Contract](Fact_Subscription_Contract.md)：NET01–06、K/W/O、三类真实公式、R0来源／锁定，F01–60受影响与继承。
3. [Formal Sync](Formal_Authority_Sync_Delta.md)：FS03/04/06新精确文字及其它FS继承，再看当前正式文本，不以报告替代正式权威。
4. [Pre-U5](Pre_U5_Final_Candidate.md)＋[O1–O8](Option_B_Final_Candidate_Plan.md)：顺序、入口、等价、LOCAL/USER_NATIVE、停止/回退/删除门禁。
5. [G01–30与源码](Gap_Matrix_v3.md)＋[Decision Closure](Decision_Closure_Register.md)：逐疑点跟真实calls，原v3未变条目用精确原行继承，不需全量通读历史。
6. Carrier独立专项仅按Gap的生产职责/SQL/save/退出交叉引用读，不能把数量优化当本计划授权。

### 基线和优先源码

审计时重新确认HEAD／working-tree／正式版本。候选基线719eb61（D0058/A0183/S0866）；相对原v3源码9addf8d只增加13报告，生产字节不变。B399.426仅既有部署记录，本轮未验包。新候选发布只新增本目录Markdown，不构成新runtime版本。

- 网络：[Mod/NetworkBridge.lua:20](../../../../../../Mod/NetworkBridge.lua#L20)、[Mod/NetworkBridge.lua:103](../../../../../../Mod/NetworkBridge.lua#L103)、[Mod/NetworkBridge.lua:133](../../../../../../Mod/NetworkBridge.lua#L133)、[Mod/NetworkInput.lua:70](../../../../../../Mod/NetworkInput.lua#L70)。
- partial来源/物理：[Mod/Commerce.lua:240](../../../../../../Mod/Commerce.lua#L240)/281；[Mod/CultureNetwork.lua:137](../../../../../../Mod/CultureNetwork.lua#L137)/185/298；[Mod/StandardizationEffects.lua:111](../../../../../../Mod/StandardizationEffects.lua#L111)/165/191/227；[Mod/CommerceCalculation.lua:31](../../../../../../Mod/CommerceCalculation.lua#L31)。
- 信誉/承诺：[Mod/CityProgressionStore.lua:521](../../../../../../Mod/CityProgressionStore.lua#L521)/1127；[Mod/StoreSubrecords.lua:100](../../../../../../Mod/StoreSubrecords.lua#L100)；[Mod/CapitalInvestment.lua:140](../../../../../../Mod/CapitalInvestment.lua#L140)/182/235/343；[Mod/CapitalInvestmentModel.lua:135](../../../../../../Mod/CapitalInvestmentModel.lua#L135)/151/175。
- 交付/启动：[Mod/FactChanges.lua:164](../../../../../../Mod/FactChanges.lua#L164)/182；[Mod/FactConsumerBindings.lua:11](../../../../../../Mod/FactConsumerBindings.lua#L11)/75/109；[Mod/Gameplay.lua:837](../../../../../../Mod/Gameplay.lua#L837)/1029；[Mod/RuntimeComposition.lua:45](../../../../../../Mod/RuntimeComposition.lua#L45)。
- 退役/安全：[Mod/Probe.lua:553](../../../../../../Mod/Probe.lua#L553)；[Mod/PerformanceCounters.lua:204](../../../../../../Mod/PerformanceCounters.lua#L204)；[Mod/NetworkSender.lua:8](../../../../../../Mod/NetworkSender.lua#L8)；[tools/deploy.py:50](../../../../../../tools/deploy.py#L50)与[tools/temporary_playtest.py:37](../../../../../../tools/temporary_playtest.py#L37)。

### 请优先反证

1. 正常UNKNOWN根因是否归事实owner并能在可靠阶段完成，而非把hold搬中央；dirty立即失效strict，negative不等unknown sibling。
2. B的cold无见证／K-empty／未知receiver／负事实＋不可分aggregate是否精确可实现；没有把未知源记0、把partial作READY或破坏独立合法sibling；标准化max、Culture并集、Commerce每domainFloor保持。
3. 旧Standardization冷例外A和派生保存许可是否在后继规范明确替代；D1过渡不会无结束条件常驻；保留／禁用／真退出差分可执行。
4. A是否严格只限信誉叶子；真实0/不适用0/政策0可区分；VENTURE准备确认比来源并锁terms，恢复不改合同；STABLE不加无关R门槛；其它UNKNOWN/native结果仍拒绝。
5. R2真正到专业登记才ACK，旧ACK/同值恢复/第二次变化不丢；R3四专业声明和phase0/Seal/FAILED隔离保持；独特原生完成监听不误删。
6. Mod真实历史不猜造、不可逆收据/Carrier幂等/单位唯一proof保持；Crew累计差值不能发unit，Claim真early不能被timer误挡。
7. P3/旧Probe生产写屏障、Flight/GC、cleanup/ACK实际迁完才disable/remove；真实缺file/global通过，不只是ENABLED=false；SQL ID不随Lua删。
8. 双部署exactdeletedset、未知extras、receipt/failpoint/restore与旧档/新provenance相容有明确门禁；代码回退没有被冒称保存/native回退。
9. 已批准公式、rounding、source资格、八收藏时代、Cross基础相邻、Wonder无N/E/L等独立性保持；没有为形式统一增加业务或中央推送。

### 所需输出及处置

每Finding给ID、严重度、可达反例、当前formal＋目标、具体源码/分支、影响F/G/PU/O/FS、最小验证、建议及是否确需Owner。区分STATIC、既有LOCAL/USER_NATIVE、UNVERIFIED，未执行不写PASS。

Primary随后维护下表；**目前为空，因为外部审计尚未进行**：

| Finding ID | 证据／反证 | Accept / Rebut / OwnerDecision | 修正位置与影响包 | 最小验证／重审 | 当前关闭状态 |
|---|---|---|---|---|---|

Accept必须修计划/合同；Rebut须可复查证据；OwnerDecision提交最短Packet并暂停依赖。严重/结构性问题在实施前解决，必要时交Reviewer重审；不能“等代码写完再看”关闭。Owner审阅Finding闭环后**再次明确批准**正式同步与实施范围，才可开始获批工作。审计PASS和Git发布无自动权限。

User decision：先Owner认可此包供审计。User testing：无。Primary next：不自动调用Claude或创建审计会话。
