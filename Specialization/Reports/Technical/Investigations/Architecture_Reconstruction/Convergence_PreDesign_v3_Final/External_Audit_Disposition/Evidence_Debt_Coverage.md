# 证据、输入及附属债务覆盖索引

Status: Stable — `v3.1-review` 调查候选；可审阅，不代表审计关闭、正式接受或实施授权。

Primary｜2026-11-04｜develop `954dc67aca007082a5a164becdbafbacbad1403a`；D0058 / A0183 / S0866。B399.426 仅为现有部署记录，本轮未验运行包。

本轮仅新增本目录 Markdown；不改旧报告、生产、测试、工具、正式规范或状态；不运行验证／探针，不提交／推送，不启动游戏或部署。文内 LOCAL / NATIVE 均为未来验证要求，除明确标为“既有记录”外没有新 PASS。

## 基线、输入与完整读取证明界线

HEAD `954dc67aca007082a5a164becdbafbacbad1403a` 与origin/develop一致；入场干净。候选十文件发布commit954dc67、前一候选记录719eb61；9addf8d到当前保护范围无运行源码差异。旧文行号全部按实际当前文件重新定位，来源行存在不代表结论通过。审计原件当前仅本地可读，未在`git ls-files`中；本轮不自动发布它们。

| 原件 | SHA256／状态 |
|---|---|
| [本轮Owner handoff逐字副本](Owner_Handoff_20261104.md) | `be655cc5e99ee97ba77e51749809152cd24b164f69c4f580f70d1ff2f788b04b`；全文99行，按原bytes复制，不加前言改正文 |
| [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final.md](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final.md) | `3394864bd5ab28606dcf1ecc321bae5a7172ebdd571b6515bec2c206e3774e31`；294行、42,291 bytes；完整读 |
| [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md) | `376ffed30181226f22147a7875113631b68068671b1f8c263975e5a00f80f041`；295行、75,564 bytes；完整读 |
| 前轮Owner `handoff.md` | 原Final README39记录哈希`2289c1924ae963566db9922b5497333cecdc88203eb974d920bae2f7675e42d4`，本轮给定原路径不可取得；hash不是备份，不把其内容猜写成“原始指令” |

本轮hand-off行数以副本实际统计为准；不依赖示意的bytes/行数作为权限。所有本轮LOCAL/native未执行：本文只是源码、测试**定义**和文件引用复核。外审行标“as reported”的原证据等级不因进入覆盖表提升为Codex已重跑。每A独立复核的实际代码/正式条款见[处置表](Audit_Finding_Disposition.md)。

## Read Ledger（重要扩展与排除）

| 阅读面 | 范围与原因 | 证据／排除 |
|---|---|---|
| Mandatory first | 两外审正文/附件先完整读，再读原Final十文件、其v3引用/决定/事实/正式同步；Owner原文逐条确认 | 完整外审不是摘要；保原作者/原文 |
| 当前路由 | 根/项目/Investigation guidance、Authority版本/manifest、Status CURRENT、Workflow/Playtest适用门禁 | 只定位当前授权；不把旧S0–10或持续部署视为本轮代码许可 |
| Cold/网络 | Sender/Bridge/Input→Commerce/CultureNetwork/StandardizationEffects、RuntimeWork init、EffectiveFacts/DC/NativeFacts | 因A01–05/12和OD1展开实际call；未读外部save/DB、不启动probe、不验证引擎保存时点 |
| R/业务 | Store isolation/合法exit/commit→CommerceModel/Capital Model+owner；Shared/Commerce正式字段 | 因A07/11/OD2；只读，不人为构坏记录 |
| 传播/项目 | FC/Bindings/RuntimeWork/GreatWorkFacts；Crew/Claim/Dialogue/Study、TimedProjectReaders；Store admission/exit/return | A09–17；原生签名和频度仍UNVERIFIED |
| P3/部署 | Gameplay composition/include→FreshBinding/Binding/Journal/Flow、Probe、Construction/Precision、Flight/GC、trace/errors、SQL/modinfo/LegacyCleanup；两部署工具相关事务 | 仅直接依赖/注册与具体旧职责，不全盘扫HD、不处理无关Mod、不开游戏 |
| 测试定义 | refactor_harness、s9e6历史比较、s4b/相关旧A和s9g1–4、受影响fixture引用 | 不调用test runner、不生成新Closure、不注入故障；未来验证列方案 |

## 六条lead：没有因为Owner反馈而丢失

| Lead | 处置／后继 |
|---|---|
| L-01 | A08；详对应A及NET/W/FS表；原建议不等Owner决定 |
| L-02 | A01/A04；详对应A及NET/W/FS表；原建议不等Owner决定 |
| L-03 | A01/A02/NET05；详对应A及NET/W/FS表；原建议不等Owner决定 |
| L-04 | A14；详对应A及NET/W/FS表；原建议不等Owner决定 |
| L-05 | A13；详对应A及NET/W/FS表；原建议不等Owner决定 |
| L-06 | A20/FS05；详对应A及NET/W/FS表；原建议不等Owner决定 |

## 九组逐行结果索引（67项）

保留外审原判词，逐行指回原件；只作覆盖索引，不复制展开源码闭包。INVARIANT条目是既定规则保持，不要求再投票或新做一轮全量native。

| 原ID | 原外审判词 | 处置覆盖 | 原文 |
|---|---|---|---|
| G9-1 | CONFIRMED, Low | INVARIANT-01 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:173](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L173) |
| G9-2 | CONFIRMED, Low | INVARIANT-02 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:174](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L174) |
| G9-3 | CONFIRMED, Low | INVARIANT-03 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:175](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L175) |
| G9-4 | CONFIRMED, Low | INVARIANT-04 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:176](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L176) |
| G1-1 | GAP, High | A01/A04 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:184](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L184) |
| G1-2 | GAP, High | A02 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:185](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L185) |
| G1-3 | GAP, Medium | A03 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:186](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L186) |
| G1-4 | GAP, Medium | A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:187](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L187) |
| G1-5 | Adjacent, Medium | A02 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:188](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L188) |
| G1-6 | CONFIRMED, Low | A02/A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:189](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L189) |
| G1-7 | CONFIRMED, Low | A04/A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:190](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L190) |
| G2-1 | REFUTED (candidate's T0 description), High | A04 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:198](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L198) |
| G2-1a | Qualified | A04 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:199](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L199) |
| G2-2 | GAP, High | A01/A04 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:200](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L200) |
| G2-3 | GAP, Medium-High | A05 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:201](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L201) |
| G2-4 | GAP, Medium | A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:202](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L202) |
| G2-5 | Adjacent, Medium | A04/A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:203](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L203) |
| G2-6 | REFUTED for current code, Medium | A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:204](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L204) |
| G2-7 | GAP, Low-Medium | A05/A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:205](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L205) |
| G2-8 | CONFIRMED, Low | A01/A12 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:206](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L206) |
| G3-1 | GAP, High | A03 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:214](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L214) |
| G3-2 | GAP, Medium | A03/A14 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:215](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L215) |
| G3-3 | GAP, Medium | A08 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:216](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L216) |
| G3-4 | CONFIRMED no production use; GAP, Medium | A06 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:217](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L217) |
| G3-5 | GAP, Medium | A03 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:218](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L218) |
| G3-6 | GAP, Medium | A03 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:219](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L219) |
| G3-7 | Low-Medium | A03/A08 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:220](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L220) |
| G4-1 | Adjacent current defect, Medium-High (rare, money) | A07 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:228](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L228) |
| G4-2 | CONFIRMED current defect, Medium | A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:229](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L229) |
| G4-3 | GAP, Medium | A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:230](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L230) |
| G4-4 | GAP, Medium | A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:231](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L231) |
| G4-5 | CONFIRMED + GAP, Medium | A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:232](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L232) |
| G4-6 | CONFIRMED, Low | A11 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:233](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L233) |
| G4-7 | Medium | A06/A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:234](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L234) |
| G4-8 | Out of scope, Low | A06 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:235](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L235) |
| G4-9 | Low | A08 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:236](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L236) |
| G5-1 | GAP, Medium-High | A10 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:244](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L244) |
| G5-2 | CONFIRMED + GAP, Medium | A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:245](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L245) |
| G5-3 | GAP, Medium | A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:246](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L246) |
| G5-4 | GAP, Medium | A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:247](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L247) |
| G5-5 | GAP, Medium | A02/A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:248](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L248) |
| G5-6 | GAP, Medium | A02 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:249](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L249) |
| G5-7 | CONFIRMED + Low-Medium | A09/A10 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:250](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L250) |
| G5-8 | Low | A09 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:251](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L251) |
| G6-1 | New, High (conditional on one ambiguous grant) | A15 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:259](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L259) |
| G6-2 | CONFIRMED, High if the native timing occurs | A15 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:260](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L260) |
| G6-3 | CONFIRMED (narrow), Medium | A15 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:261](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L261) |
| G6-4 | CONFIRMED, Medium (cancel UNVERIFIED) | A16 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:262](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L262) |
| G6-5 | New, Medium (native drop UNVERIFIED) | A16 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:263](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L263) |
| G6-6 | CONFIRMED, Low | A11/A15/A16 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:264](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L264) |
| G6-7 | CONFIRMED + GAP, Medium | A17 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:265](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L265) |
| G6-8 | CONFIRMED + GAP, Medium | A17 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:266](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L266) |
| G7-1 | GAP, High | A18 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:274](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L274) |
| G7-2 | GAP, High | A18 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:275](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L275) |
| G7-3 | GAP, High | A18/A19 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:276](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L276) |
| G7-4 | GAP, High | A18 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:277](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L277) |
| G7-5 | GAP, Medium | A18 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:278](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L278) |
| G7-6 | Location CONFIRMED; rule GAP, Medium | A19 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:279](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L279) |
| G7-7 | GAP, Medium | A19 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:280](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L280) |
| G7-8 | GAP, Medium | A18 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:281](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L281) |
| G7-9 | CONFIRMED + GAP, Low | A18/A19 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:282](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L282) |
| G8-1 | CONFIRMED, Low | A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:290](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L290) |
| G8-2 | CONFIRMED, Low | A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:291](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L291) |
| G8-3 | CONFIRMED, Low | A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:292](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L292) |
| G8-4 | Missed by candidate, Low | A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:293](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L293) |
| G8-6 | Note | A20 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:294](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L294) |
| G8-5 | GAP / conflicts with an accepted user decision, Medium-High | A06 | [Specialization/Reports/Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md:295](../../../../../Advisory/Architecture_Engineering_Audit/Independent_Audit_v3_Final_Evidence.md#L295) |

INVARIANT-01：八时代启迪24%/对话40，作品池/计次/历史不变。INVARIANT-02：巨构current era＋统一ACTIVE，无N/E/L。INVARIANT-03：Cross基础相邻/Apply逐域/文化网络union与商业max/Floor保留。INVARIANT-04：无中央资格推导/全面推送改造/自动发现bus。静态源码与旧具名测试可继承，不扩大native PASS。

## 主报告§VI附属债务：32项逐行接管

| 原报告行／原项目 | 对应A | 修订位置／未来责任 |
|---|---|---|
| 214 — Standardization warning-triggered cold freeze | A04/A12 | O3；NET T0/NET02，warning不等故障 |
| 215 — Per-domain / per-target independence; Standardization self increase while pending | A12 | O3；domain/target/self独立，cold受OD1 |
| 216 — Bridge drops unknown-role sources; `effectAvailability` ignores `input.pending` | A05 | O3；role与availability |
| 217 — Write failure zeroes output | A12 | O3；实际残留/error不反射性clear |
| 218 — `failedTurn` blocks proof sends for the rest of a turn | A02 | PU03/O3；新证据有界发送 |
| 219 — Bridge central holds (`negativeHeld`/`dormant`/`queuedWork`/prune view) | A03 | D1-03–06；O3 |
| 220 — Over-limit routes/payload hold | A20 | W16/O3/O8；容量显式error |
| 221 — Dead code: `withdraw()`/CONFIRMED_INVALID branches, `proofPending`, Bridge `consumerError`, `roleUnknown`, CultureMeaningProbe Bindings row, unused includes/imports | A03/A18 | O3/O5/O7；逐call核dead，不以grep名清理 |
| 222 — Identity-exit reset skipped during leaf isolation | A07 | PU06/O4；OD2合法reset |
| 223 — CREDIT_* missing from signing guard; mode-specific signing; R provenance and status mapping | A11 | PU06/O4；R分类/mode/CREDIT guard |
| 224 — Silent delivery drops; owner retention in NewAudit and four flushes | A09 | O2；FC/Bindings/NewAudit/四flush接管 |
| 225 — Unique Governor listeners | A09 | O5/O8保有序Governor监听 |
| 226 — Mandatory fail-closed exit gates vs FS09 | A10 | O5；mandatory exit先迁责 |
| 227 — Crew receipts per player+type; ambiguous-grant end | A15 | PU05/O4；每completion唯一receipt/新证据 |
| 228 — Claim/Dialogue access marker removed on UNKNOWN; Claim CALLING terminal | A16 | PU09/O4；UNKNOWN marker/Claim CALLING |
| 229 — Recapture needs all ~45 exits; optional exits gate production; retry-count exit recovery | A17/A18 | PU08/O4/O7；真实端点/必要exit |
| 230 — G11 reach across unassigned cities | A17 | PU07/O4；completionError范围 |
| 231 — DEV probe chain as fact-path prerequisite | A18 | P3-03–05；O1/O7 |
| 232 — UnitSiteProbe startup dependency | A18 | P3-07；O7 |
| 233 — PerformanceCounters load-time binding; unguarded `P.Count` | A18/A19 | P3-01/02/16/17；O1/O2/O7 |
| 234 — Trace factory built unguarded in ~10 modules + UI; error classification in diagnostics | A18 | P3 §3工厂和生产error |
| 235 — GC gate invariants (Flight vs enabled, nil gate, latch) | A19 | P3 §4；现GC/Flight不变 |
| 236 — PurchaseProbe production cleanup; BoostRefresh waits on GreatWorkProbe | A18 | P3-14/15；cleanup/readiness |
| 237 — Test-named SQL used by production; duplicated modinfo component | A18/A19 | P3-24；SQL/duplicate组件 |
| 238 — Derived-save adapter, Store stamp, tests s9g1-s9g4, static alarm | A06 | D1-12/P3-23；不接新生产、逐责退出 |
| 239 — D1/exception-A tests needing deliberate rewrite | A03 | D1原测试逐断言处置 |
| 240 — True-absence harness layer | A19 | PU11/O7；VFS/真实composition |
| 241 — Commerce UNKNOWN allowlist misses DEPTH/CAPACITY; `clear()` removes ACCESS marker; double ACTIVE/WORKERS subscription | A12/A09 | PU01/O3/O5；未知分类、ACCESS与双Binding分开 |
| 242 — `Standardization.Refresh` drops work when busy | A09 | O2；Standardization忙时责任接管 |
| 243 — Store admission hook error poisons pending candidates | A17 | PU07/O4；freshHook错误影响scope |
| 244 — Standardization adopts installed carriers after same-owner reference change | A17/A04 | PU08/O3；新ref不可无证adopt已安装结果 |
| 245 — Misleading "DEV/Probe/read-only" headers on production files | A18 | P3-01–25；注释服从实际职责 |

## B396交叉核对与证据边界

附件48–62的B396核对保留：已修NET-1 signal指纹和NET-2具名生命周期恢复在当前Sender仍存在，O3不能撤重放/严格交易防护；其它Commerce UNKNOWN、ACTIVE、CREDIT、receiver、firstcompletion、工程E等未完成职责分别归A02/05/11/12/17及原G；不是把B396所有历史项重新开修。旧reported native结果只按B399具名场景，不将expiry证明所有原生移除入口。

不受本次修订影响的债仍按原G01–30和DEC/R保留，非机械清空backlog：多item队列、HD GPP、PT017额外金币根因、边境移除Expedition等现有停放范围不因本轮外审扩大。

## 本轮文件QA与完整性

交付前核对：所有A01–20都有裁定/级别/可达条件/映射/具体改文/LOCAL-native与关闭状态；九组ID和32债无漏行；新报告链接目标/行存在；Owner副本哈希一致；十旧候选与两外审原件哈希不变；受保护tracked区域无diff；HEAD/index不变。该QA只校验文档及字节保护，不是Gameplay、Context Lock validator、原生或LOCAL模拟PASS。本地路径/哈希不是永久备份；本轮无提交/推送。
