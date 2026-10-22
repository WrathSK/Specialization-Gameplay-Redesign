# P04b/P11b — Commerce合同、制度历史与当前旧writer

独立审计 IA20261007 / W19；基线 `a75c73aba9d14739233d87e20025ea8c07b98041`。项目本体只读。slice覆盖完成不是新商业能力实现/native或总审计PASS。

## 结论

[Commerce D0045](../../Design/Content/Commerce_D0045.json)与[Spec COM](../../Design/Specialization_v0.1_Design_Spec.md#8-commerce--commercial-hub--com)的新商业化、资本/发展合同、信誉与资产重组**均未实现**；当前是基础/II＋旧三类连接专家支持＋旧20%汇聚。这个差距已在[商业准备](../../Architecture/v2/Commerce_Preparation.md)及[B164落地盘点](../../Reports/Technical/Specialization_B164_Implementation_Landing_Audit.md)登记，不将设计冻结/旧验收说成新商业完成。

最重要的接入约束是**签约资格与已成立合同分离、多个状态各有ownership**。配置、信誉、pity、已签资金合同、团队与REALLOCATING目标不是一个生命周期。已有Store/Claim/投资原语能提供引用/保存基础，不能不加业务合同直接成为商业长期状态系统。本slice没有新独立confirmed finding；保存成本/专业业务耦合、通知名单和writer失败边界沿现有ID。

## Accepted → target → current矩阵

| 系统 | 正式规则与真实未决 | 当前source |
|---|---|---|
| 基础/II/中心 | 各级实际专家3F3P；II Housing与Merchant base GPP；共同NET保留 | Shared writer已接；贸易中心不是新商业收益payload |
| 商业化P | ACTIVE III，五域Campus/Theater/Industrial/Holy/Harbor映射S/C/P/F/G；每工作专家1不同域容量；本地D×最高合法X×0.1×(1+0.005R_effective)，自城或任意方向direct国内源，不扣源/递归Gold | 新配置/Gold writer无；旧Lv3 COM支持＋旧Convergence不是X或新公式。X组件/聚合仍DESIGN_DECISION_REQUIRED，不套Shared份额/Floor/整城实际产出 |
| 信誉S | 首次永久IV起点，Commerce Identity完整标准T+1，cap40；不足ACTIVE IV仍增长，但效果仅IV；owner变化不清零/分仓，unsupported休眠 | 无信誉字段/起点/tick；不能复制Research原Ownerhold或年龄cap100 |
| 资本Q | III新签约；每次本金25%当前余额/10标准T；r=.01DSC，C=1.25或1；safe总返P(1+r)、风险成功P(1+3r)、失败P(.5+.005R确认值)；基础概率min(.8,.4+.01DS) | 无Gold扣款/合同/outcome/到期writer。S资格/池/level/空池/同域排他scope仍TBD；不能拿Settler InvestmentAction的Potential receipt替代 |
| 隐藏保护Q2 | source city跨域共享，确认时roll/lock/立即更新；失败追回距.8差额25%，成功/Identity退出清零；不反惩罚好运 | 无pity字段；新基本面如何组合及跨Owner保留/分仓/清零仍真正TBD，合同Owner异常终止不等于pity失敗/倒回 |
| 发展R | IV确认需source→target direct；按plot-only P_low+.75(P_high−P_low)报价15P_ref；10T普通建筑+50%；工作专家给并行容量、全来源target+domain唯一；标准化加算 | 无quote/合同/+50%writer。P_low目标及无plot食物可行解仍TBD，不按focus当前Production报价；当前模板不是资格 |
| 团队T1 | IV production-only500P；不可敌方capture/转Owner、受保护安全回归、无主动删除；完成团队原Owner独立资产 | 无新团队/provenance/保护；一般Crew/CreateUnit实现不证明这些规则 |
| 重组T2 | 目标有Identity且P≥2，清算入独立REALLOCATING/P−1，至少5完整标准T；非Food/net Food surplus−75%；时间到不自动恢复，合法配置成功才消耗团队并重算ACTIVE | 无REALLOCATING/P−1/绑定事务/扰动。现有Potential=1+receipts不能直接表达永久损耗；Claim不是重组状态机 |

所有值是v0.1首测，非标准速度精确规则未决。没有Commerce Floor/额外cap授权。报价Gameplay生成一份，UI同屏显示source S及概率/总返还/净收益，不重复算一套；项目列表是pre-native action entry，不是先入queue再伪完成。既有真实1T Claim hook仅是技术线索。

## State ownership／成立后继续合同

| 状态 | ACTIVE或Identity变化 | Owner与cold-load合同 |
|---|---|---|
| 商业化选择/order | 保有CommerceIdentity时ACTIVE不足保留；容量降LIFO暂停，不删，恢复先旧项；主动关删/重新开最新 | Identity退出或Owner变清；same-owner合法load恢复配置后按当前事实派生，不恢复effect snapshot |
| 信誉R | ACTIVE降保留并正常Identity计龄；离开Commerce立即0，再建立从0 | Owner变化不清零/分仓；unsupported专业机制休眠，不补算；与Research保留年龄及配置清空不同 |
| 已签资本 | Governor/ACTIVE/Identity/D/S/C/route普通变化不取消、不改价、不reroll | Commerce城或锁定具体S城任一换Owner异常终止：不返本金，不maturity/失败退款/修改保护；load恢复锁定outcome和receipt |
| 已签发展 | Governor/ACTIVE/Identity/route/专家capacity下降不取消；target Identity变化但目标合法继续 | Commerce来源或target Owner变：无退款、立即撤+50%/释放slot；目标非法处置另TBD，不从Owner规则类推 |
| 训练完成团队 | 训练城资格/Identity退出仍保留，来源只是provenance | 训练sourceOwner变化不删/转交；绑定后由另一个target事务控制，不能按source-loss通用清理删除 |
| REALLOCATING事务 | 无currentIdentity/ACTIVE，不走NONE/firstClaim；5T后仍扰动直到配置 | target配置前易主毁当轮未完成事务/资本/旧currentIdentity及绑定团队；夺回后按明确新candidate/Claim例外，不复活半成品；具名永久history按各自规则保留 |
| hidden pity | 成功/退出Identity重置；已签合同失去资格不重新抽结果 | Ownerpolicy真正TBD；Owner rupture本身不触发/回滚确认时pity更新 |

资本S必须锁**具体城市**，最高level并列按最早达到再稳定key；稳定cityKey自身不能证明到级时间。新合同需要key-city Owner relation、uniqueID、quote/version、锁值/outcome、确认扣款和到期receipt。保存完成前扣款/roll/保护更新的失败恢复不能从旧“单位消耗＋P提升”原样移植；当前未实现，不报告已发生重复扣款事故。

## Current writer、可复用公共路径与性能

[CommerceConvergence](../../../Mod/CommerceConvergence.lua)当前AUTO：ACTIVE IV、verified背景路线incoming-only；不同RESEARCH/CULTURE/INDUSTRY来源选实际整城yield最高值×20%最终floor，48个bit carrier。Audit先把所有目标plan建完再apply，同次新投影不会影响另一目标plan；batch共享城市facts/yield和按destination route索引。这是旧公式的有限防递归，不是新五域X资格或所有跨回合反馈已消除。

[Lv3Effects](../../../Mod/Lv3Effects.lua)COM分支仍按current connected kinds给3个工作专家载体。Gameplay783–784启动Convergence；共同Bridge notify和native hooks仍接旧writer。正式P cutover须停止旧正向入口，精确撤3＋48，再开新writer；只隐藏按钮/删SQL不安全。其它profession/NET/基础效果不能为此整退。

| 未来可复用 | 不应复制／改动前需要核证 |
|---|---|
| 当前Owner/ref、事实/Domain D、validity/version、exact owned exits | confirmed contract成立后依赖锁值及两城市Owner，不一直依赖ACTIVE/当前route；不能把yieldUNKNOWN退出等同合同终止 |
| 背景route可信样本 | 一个snapshot建立direct双向P候选和outgoing R索引；共同center recipients不能替代两者，未知不能空；新业务history变化即使route不变仍刷新相关consumer |
| Store唯一持久权威/读回 | 各自纯模型/具名写API；P06a-F01每写全record检查和F03业务耦合需在增加长期writer前收窄；不再加平行city历史文件/统一永久状态机 |
| RuntimeWork batch/cause/scope | 同回合真实更新、关键两城市Owner状态转换有序；不要每城每回合限一次、全世界扫AI或独立GC |

正常Convergence plans为C目标、route索引一次R、按incoming边与资格读取，约O(C+R+来源读取)，再逐城48 owned检查；首次清理一次world范围。通用输出revision仅在变化后触发Audit，结束更新seenOutput以避免本轮self-write反复失效；这是既有B135–138约束，源码调用数不能转native耗时/内存量。新P应复用确认输入和必要facts，不复制旧整城actual-yield诊断/全部carrier遍历作为默认业务框架。

## 测试证据及余界

旧B038人工确认固定专家+2S/+2C/+2P，缺当时连接失效/新局原生回报；旧B062通过只限旧20%Science（6→11、两源仍+5）/所测非叠加和用户口述退出；不能证明新Gold小数、资金锁定/结算、项目action无queue或REALLOCATING。B137实验隔离退出seed每个owned ID及五actual consumers，证明对应机械退出、幂等/失败/哨兵保护；没有actual Store loss组合，正常Store exact出口另据源码/先前Store协议，不声称51个载体逐一native收益。先前[P12a](P12a_Scaling_Validation_Boundaries.md)已核：30,000已发布query不是真实全writer×城市/建筑/路线扩展负载；D2确有3来源/5接收/15incoming非零旧Convergence/yield-only变化，但Bridge/facts为stub，独立facts/district规模loop不含Convergence、九module分别启动。ConvergencePlan是MOCK_ONLY/OFFLINE_PROPOSAL纯模型，不是正常writer或原生反馈证明。不据历史测试数宣布新商业scalePASS，不为尚未授权商业补stress/native仪式。

[商业准备](../../Architecture/v2/Commerce_Preparation.md)顶部仍提B165待验，是当时准备位置；它同时明确当前状态/授权转Status。B166当前已经限定通过，不应拿旧句阻塞独立O/S准备或宣称今天许可新实施。Spec/Content/准备保留真实窄TBD，不因null补0：X、S/同域scope、pity-rebase/Owner、参考态/无解、速度、城销毁/目标非法/原Owner消失。团队不可capture是已定而技术待证，不再是OwnerGameplay TBD。

当前旧Convergence active未知/Plan抛错会转amount={}；Lv3旧资格非数也转空。不把它们继承为新合同的UNKNOWN/资格失效处置；Future确认合同须独立状态，不依赖旧yield Audit的空投影。isolated(nil)与每pid Plan门控有余工作，但尚无新效果违规证据。

本slice未新造具体native gate、没有修改规则/状态/实现或查看外部证据。完整可信工作集、全部SQL/owned退出闭包留下一slice；本报告不宣布所有current Commerce effect安全。

实际readscope：完整Commerce724行及SpecCOM、Shared具名A–G、准备O/P/Q/R/S/T；current Convergence全文/Lv3 COM与exit/Gameplay-Bridge接线、Store81–104/807–844及EffectiveFacts35–56具名状态；B038/B062结果、B062/Lv3/ConvergencePlan与D2/B137 direct fixtures/断言定向审阅。没有全部历史/所有套件/外部DB或截图读取。当前Store只UNASSIGNED/SPECIALIZED、P=base＋receipts，没有资金合同/商业配置/R/pity/REALLOCATING业务API，不能靠删receipts表达P−1。

下一P05a/P08b：modinfo注册与Gameplay/UI真实根→Start/include动态门控→exact owned SQL及退出归属；形成正常/probe/退休/不启动清单，复用已读模块，不重复每能力native验收。
