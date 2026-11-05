# 决定状态与原候选纠正

Status: Stable — `v3.1-review` 调查候选；可审阅，不代表审计关闭、正式接受或实施授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅新增本目录 Markdown；不改旧报告、生产、测试、工具、正式规范或状态；不运行验证／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 权威及状态

[本轮 Owner 原文](Owner_Handoff_20261104.md)高于 Codex／Claude 建议。本文件不是 Design successor。`OWNER_POLICY_RESOLVED`、`PLAN_REVISED_REAUDIT_PENDING`、`ENGINEERING_EVIDENCE_OPEN`、`FORMAL_SYNC_PENDING`各自独立；不存在“文件生成即最终关闭”。正式 D0058/A0183 的现状仍作为 T0，不能因新目标反写旧验收。

| 决定 | 已定范围 | 新候选纠正／剩余状态 |
|---|---|---|
| OD-1 | 同版本合法保存→恢复等价状态；相关事实未可靠重建，不凭缺输入动已恢复载体；真实新负事实正常处理 | 拒绝从“冷A退出B未知”直接推出降收益；不选审计(a)/(b)。正常加载写屏障与真实恢复时点需证，`ENGINEERING_EVIDENCE_OPEN`；NET/O3/FS03–04 |
| OD-2 | 可信合法 Commerce 身份退出，信誉按规则重置，旧叶暂不可读也不跳过 | 不是损坏历史自动清零。可信 parent/ref/事务+受控提交；保留异常证据和兄弟记录；PU06/O4/FS05–06 |
| OD-3 | 优先完成事件；必要且有证明的短暂未就绪，局部已登记待办可在本地回合开始有界续办 | 不全城轮询、不等待时间修历史；每因有 owner/限额/终态，旧 turn audits 须逐责任替代；PU03/O2/O3 |
| OD-4 | 只支持当前构建开启的游戏及同版本存档 | 删除跨版本迁移、旧合同新字段回填、无限 LEGACY 规划义务；持久化不兼容即新游戏；代码/部署备份回滚仍严格；O3/O4/O7 |
| ODP-01=B | 极端 warm：有效同引用来源会话见证；正常 cold 用可靠原生事实＋真历史重建，不默认持久化派生归因 | OD-1 澄清正常冷加载。旧候选严重 cold K-only/空K撤除政策**未由本轮批准**，从实施目标撤出；必要取舍先证后报 |
| ODP-02=A | 独立信誉叶严重异常，基础与实际用途的其它输入可靠时，临时 R0 供所有依赖 R 的用途／新VENTURE；STABLE无虚增R门槛 | 原历史不写回，错误可见；四类R来源、confirm见证及新合同锁terms；旧合同在其原构建内不追改；CREDIT_*等严格保护不豁免 |

OD-2不授权将未知 Capital 整个叶子或未决 receipts 一起重置。已有合法转换的失败保护重置，只能修改有可靠权威的对应字段，不能抹去合同／不确定付款。原“legacy/LEGACY”若指真实认领模式、绑定或 exact carrier cleanup，不等同跨版本兼容，可保留其生产职责。

## DEC01–14：逐项继承与澄清

依据为原 [Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3/Decision_Closure_Register.md:25](../../Convergence_PreDesign_v3/Decision_Closure_Register.md#L25)–38 及本轮原文 §2；原附件未重获的细节不凭此表发明。下面均是已定目标，工程和正式同步仍未完成。

| ID | 保留／修订后的确切边界 | 后继责任 |
|---|---|---|
| DEC01 | 每能力／用途独立；真实负事实优先，纯被动与不可逆严格区分；冷恢复受OD-1约束 | O1/O3/O4 |
| DEC02 | 统一ACTIVE，无总督正常KNOWN1；不建专业Governor缓存；未来容量不做 | O1 |
| DEC03 | raw事实冷重建；真实历史／收据保存；不默认派生持久化；OD-1/4优先 | O3/O4/O7 |
| DEC04 | 接管前不ACK；专业持有已接管责任；ACK不是应用／交易成功 | O2 |
| DEC05 | 专业schema/合法转换，Store管身份/CAS/读回/提交次序 | O4 |
| DEC06 | root-first；只保有证确定性／合法deferred；不造全面零基线重置流程 | O4/FS05 |
| DEC07 | 研习E完整严格；不由当前奇观／下限补造；巨构无N/E/L依赖 | O4/FS11 |
| DEC08 | Claim真原生提前完成合法；唯一候选/ref/receipt；不移植未核实bCanceled | PU09/O4 |
| DEC09 | 成功Start后声明普通订阅；phase0顺序和独特直接监听保留；mandatory exit不受普通订阅回滚误删 | O5 |
| DEC10 | 城市身份/历史与实例位置/资格分离；未来多实例仅预留 | O1/O4 |
| DEC11 | PU为O包可延续首片；未授权开始任何代码／U5／Option B | 全包 |
| DEC12 | 减少已证浪费，保必要恢复；无CPU/RAM/百分比承诺 | O8 |
| DEC13 | 首次完成查事件/目标/时机；不得猜first、清stickyerror或无证扩新持久层 | PU07/O4 |
| DEC14 | exit/recapture根因和严格端点；合法deferred按证据续接；不扩大城市易主玩法 | PU08/O4 |

| R | 当前目标（不重新投票） | 本轮具体补齐 |
|---|---|---|
| R1 | 分用途共享可靠事实，Cross只基础相邻，非全表UNKNOWN放行 | NET/每domain/target与权限边界 |
| R2 | 最小AcceptChange责任接管，revision/ref/ticket防重入 | phase0同步完成ACK，普通owner登记ACK；NewAudit＋四flush纳入 |
| R3 | 成功启动声明、中央校验、Seal后drain | mandatory fail-closed exit与可回滚普通订阅分开 |
| R4 | 专业转换/Store提交、显式root错误、有证deferred | OD-2合法退出信誉；暂不可读不可永久破坏 |
| R5 | PU01/02/03/05/06优先，PU04先证；其它只有正常缺陷阻U5才窄纳入 | 不把每PU再做成完整O包的重复实现 |
| R6 | ODP-02=A 已选，R0一致而严格窄边界 | quote/confirm/locked provenance，STABLE mode独立，未决CREDIT保护 |

## 对旧候选的明确撤回

1. 撤回 [Formal_Authority_Sync_Delta.md](../Formal_Authority_Sync_Delta.md) FS04中“cold无W→K-only；K空可撤”的预选异常业务政策；NET05/06同类例子和 O3验收随之替换。能编码K不等于获准这样支付。
2. 撤回 D1“keep/disable/exit”不存在开关的实验表述；改历史字节基线与实际目标差分，不创建假的删除分支。
3. 撤回旧合同缺新元数据的跨构建容错/回填要求、derived adapter无终点相容门禁。
4. 撤回每包例行原生测试；仅少量判别性触点。首次正式同步提前撤销原 S9 cold接线任务；合法deferred lifecycle、UI与真历史义务保留。

这些是候选计划纠正，不修改旧文件或正式已冻结决定；没有任何源代码修复在本轮完成。

## ODP-02=A 的实际Store状态→R来源映射（实施前合同草案）

四标签只是工程表示；不能把一个布尔reputationKnown=false自动换成已批准R0。每条均保正常资格门槛，额度/余额/网络/receipt另严格。

| 真实读取/校验情形 | 拟状态/有效R | 被动及新VENTURE／STABLE |
|---|---|---|
| 父/身份/ref/配置与信誉记录均可靠，IV有效 | R_CONFIRMED（包括真实age0） | 用已确认有效R；terms锁当前见证 |
| 正常资格低于IV，无当前信誉加成 | R_NOT_APPLICABLE / 有效0 | 按原III/IV门槛，不把不适用说成历史损坏；STABLE仍只看自身必需输入 |
| 已知独立leaf校验失败，parent/资格来源/配置及本用途其它权威另行完整通过，无法从权威直接重建age | R_POLICY_ZERO / 临时0 + 严重错误 | 保原leaf字节；商业化与新的VENTURE一致临时R0；STABLE无无关R gate |
| CHECK_UNKNOWN由缺validator/依赖未启动、运行异常或来源不可分类 | R_UNSAFE | 不是独立leaf损坏证明，不自动政策0；R依赖用途保持不安全，STABLE若其它必需基础已独立可信则不因R读取器不可用被拒。基础未证仍不得新交易 |
| ValidateReputation45–50涉及parent/qualification/投资receipt关系不一致 | R_UNSAFE，除非能独立证明故障仅leaf且基础仍可信 | 不能用“parent单独validate过了”就覆盖交叉authority冲突；STABLE也不能绕parent/身份不可靠 |
| DEFERRED_LIFECYCLE未完成实际owner/identity转换 | R_UNSAFE用于依赖该未决关系的用途 | 已批准R0不完成transition或洗掉opaque历史；按可靠原转换恢复；不能等一回合猜修 |
| whole Commerce leaf/config坏，或parent/envelope/ref/token失败 | 拒绝对应不安全读取 | 不将leaf-only例外扩大；可信不相关兄弟能力按其合同独立 |
| 本次source/treasury相关CREDIT_INTENT/CREDIT_CALLING或其它原生结果/receipt未决 | 严格原生门禁独立于R标签 | 新签受影响交易阻止；R_POLICY_ZERO也不豁免；已签仍原terms/receipt不盲重放 |
| 可信合法Commerce身份退出 | OD-2合法history transition，非R_POLICY_ZERO修复 | 原模型合法初始schema（无旧reputation/不沿用旧age）；可信转换可重置旧不可读信誉，保错误证据/兄弟，不能顺便抹未知Capital |

quote/confirm必须同时比值与来源见证（owner/ref/token、相关history/资格修订、状态/政策和适用mode）；数值都是0但来源变化必须重验。新确认合同锁terms和工程格式版本；同一支持build内历史恢复不追改既有合同。若编码形状改变则按OD4新开，不增加旧build无字段回填代码。
