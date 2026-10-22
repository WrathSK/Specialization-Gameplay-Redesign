# Mod Interaction Matrix

Document Owner: Codex
Current runtime: B072.99 / modinfo99 (unchanged)
Purpose: smallest known reproducing set / largest known non-reproducing set within observed conditions, not global proof.
Dependencies and exact UUIDs: [audit](../../Reports/Technical/Specialization_Mod_Interaction_Dependencies.md).

## Sets (exact third-party membership via audited aliases)

- BASE = SPC + BTS + EMM.
- FULL11 = BASE + CORE + CIV + DIST + IND + PRODUCT + TYCOON + TITLE + AREA.
- H = BASE + CORE.
- U = CIV + DIST + TITLE + AREA (legal on H).
- E = PRODUCT + TYCOON + IND (legal on H; IND requires the first two).

CORE=Civ6 Plus; CIV=Civilizations & Leaders; DIST=District Expansion; IND=HD Industries & Corporations; PRODUCT=Monopoly++ Corporation and Product Adjustments; TYCOON=Monopoly++ Tycoons and Investors; TITLE=Mods Title Localization; AREA=Larger MODinUse Area; SPC=Specialization; BTS=Better Trade Screen; EMM=Enhanced Mod Manager.

## Observed matrix (unknowns retained)

|ID|Exact third-party set|Closure|Duration/time|Memory start→end|Observation|Crash|Notes|
|---|---|---|---|---|---|---|---|
|O0|BASE|Official SPC expansions retained; third-party closure complete|User's window, duration UNKNOWN|UNKNOWN|No sustained growth observed|Separate earlier construction-list crash; not equated with memory|User confirmed multiple checks; map/mode details not independently captured; not permanent PASS|
|O1|FULL11|Complete|Sep14 crash21:25:30; user idle4–5min|UNKNOWN|Slow growth reported|Yes, native pure-virtual abort|PID39989; exact50 entries/11third-party archived; no Switch Civilization|
|O2a|FULL11|Complete by user confirmation|21:32:19→21:38:35;376s;Turn1/0city|9.23→9.59GB|Growth observed|None in window|PID41293; Activity Monitor Memory; mode ON user confirmed|
|O2b|FULL11|Same|21:38:35→21:44:24;349s|9.59→10.10GB|Growth observed|None in window|Includes founding first city; not pure idle baseline|
|O2c|FULL11|Same|21:44:24→21:46:55;151s|10.10→11.87GB|Growth observed|None in window|Operations/Turn1→19/second city; not used as idle slope|
|O2d|FULL11|Same|21:46:55→21:52:12;317s;Turn19/2city|11.87→13.01GB|Growth observed|None in window|Discount18602, facts74408, city_scan148816; correlation not causation|
|T1|H|CORE requires only official expansions; BASE complete|PENDING 300s/0city|PENDING|USER_GAME_TEST_REQUIRED|PENDING|Only current assigned test|

Current largest known non-reproducing third-party set: BASE, under its reported observation window.
Current smallest known reproducing third-party set: FULL11, among tested documented configurations; not claimed irreducible. Protocol differences prevent precise rate comparison until controlled reversal. Original112 set stays frozen historical evidence and is not this investigation's BASE.

## Uniform protocol

Every trial is a NEW game, never an old save with different enabled mods. Keep same build, GS ruleset, official DLC/modes (Monopolies ON), map size/type/seeds where practical, game speed, human civilization/leader and AI roster where possible. Do not let added leaders silently change random AI selection. Retain current graphics/window/focus conditions. Fully exit/restart between configurations to avoid carrying the previous process allocation history; user performs all actions.

On first interactive Turn1: no founding, movement, end turn or Diagnostics. Record start timestamp/Memory, remain idle300seconds, record end timestamp/Memory and whether rise was approximately continuous. Keep capture timing after load consistent. External monitor already exists: reuse normal30s trends, preferably auto-snapshots OFF identically in all trials; no new setup needed if Activity Monitor endpoints are easier. Compare like metrics (Activity Monitor Memory vs same; monitor physical_footprint vs same), never RSS vs Memory. Report crashes separately; a crash-shortened window is not a clean negative.

Return only enabled group, start/end time, start/end Memory, observed trend/crash, monitor session if captured. No fixed GB/min PASS cutoff. If indistinguishable, mark INCONCLUSIVE; only then consider matched two-city300s windows. Never repeat full five-stage sequence per combination.

## Adaptive decision tree (not a request to run all)

Test0: BASE already observed negative; do not repeat now.
Test1: H only (four third-party Mods).
- Growth returns: Test2=BASE (remove CORE), Test3=H (restore CORE). Stop additions. Confirm reproducible ON/OFF/ON association; this identifies CORE-added closure interaction, not sole culprit or exact script.
- No growth: Test2=H+U (add CIV,DIST,TITLE,AREA together).
  - Growth: Test3=H (remove U); then restore H+U in a later confirmation before splitting U into {CIV,DIST} and {TITLE,AREA}.
  - No growth: Test3=H+E (replace U with economic closure). This is a sibling subset compared against H, not one-mod contrast against Test2.
    - Growth: next remove E→H, then restore E before subdividing. To distinguish IND from its dependencies, test H+PRODUCT+TYCOON before adding IND; both Monopoly++ may be split individually if the pair reproduces.
    - No growth: neither half alone reproduces; do not exonerate either. FULL11 retest checks cross-half interaction/reproducibility. If reproduced, minimize by legal removal with dependency closure and retain each negative/positive set.

At first candidate-positive stop adding components; remove the LAST added closure and re-enable under same protocol. Unknown/inconclusive is not negative. For group splitting keep closure consistent; never leave IND enabled while disabling either Monopoly++ dependency. Maximum3 upcoming conditional trials described; currently user only needs T1.

## Priority contract

No DISCOUNT_AUTO_AUDIT_OFF, trigger instrumentation, formal Discount optimization, Batch C/D or compatibility patches until smallest-known set investigation is reviewed. Existing C² issue retained as independent performance debt. Once candidate closure is confirmed compare Discount behavior in BASE vs candidate to find interaction boundary, not pre-assume Discount root cause. Crash and memory outcomes remain separate columns. No new test outcome fabricated.

## Follow-up 22:32–23:04 (supersedes pending assumption that T1 was run exactly)

[Results](Results/Specialization_Mod_Isolation_2232.md). Run1=BASE+CORE+TITLE+AREA,1city204s9.30→9.50GB;2city203s11.08→11.76GB. Smaller known growth-observed set now six Mods, not an irreducible set. Run2=noHD+Cheat,3city1121s9.30→9.69GB; user confirms both helpers retained; Cheat UUID not independently captured, no new largest non-repro declared. Same PID45352 both runs. No crash captured; independent monotonic time series absent. Initial four-Mod T1 remains untested. Prefer next controlled CORE-only toggle with helpers+Cheat fixed; user confirms main-menu-only switching; no addon expansion or Discount change.

## Fresh-process zero-city toggle, 2026-09-15 (current priority)

[14-image result](Results/Specialization_HD_Toggle_20260915.md). OFF fixed companions=BASE+TITLE+AREA+Cheat; ON adds CORE, membership by user/protocol context. ON PID66765:307s9.12→9.30→9.51GB; OFF PID67538:315s8.89→8.86→8.88GB. Both zero city/Turn1, cities/districts/facts/writes all0, audit entry≈58/s both. No crash observed in windows. Extra settings pair excluded. OFF six-Mod set is largest documented no-growth window by cardinality among these current trials, not indefinite PASS; prior six-Mod positive set withoutCheat remains smaller growth-observed set than this seven-Mod ON. No irreducible culprit established. Current next test only re-enable CORE with companions/settings fixed and fresh process0city300s, completing ON/OFF/ON. Do not add optional HD modules or change Discount.

## CORE重新加入，2026-09-15 05:45–05:55（取代上节待测步骤）

[8图与崩溃](Results/Specialization_HD_Rechallenge_20260915.md)。同七Mod协议，第一次PID68667首图9.15GB后原生pure-virtual abort；无终点，不计算斜率。第二次PID69145零城316秒9.13→9.37→9.58GB（+.45）；audit+18342≈58/s，事实/扫描/派生/写入0，inflight1。ON/OFF/ON关联已复现，不是sole-HD根因证明。下一轮仅去SPC、保留CORE及其它五项，原版Robert替代已移除测试领袖；5分钟0城，只需Memory。领袖差异明确记录，必要时再匹配原版领袖对照。不改Discount，不加其它HD组件。

## 去SPC保留CORE：06:02–06:07（已完成，勿重发）

[6图](Results/Specialization_HD_Without_SPC_20260915.md)。CORE+BTS+EMM+TITLE+AREA+Cheat（按用户协议上下文），PID70353，Turn1/0城308秒8.78→8.92→8.97GB。前158秒+.14、后150秒+.05，增长减速；持续泄漏与平台期均未确认，不能列入明确non-repro或同根因repro。无SPC counters，不填0。原版Robert/不同地图/无诊断面板为比较差异。后续仅必要时延长同组合观察，不重做刚完成步骤；无源码修改。

## 无SPC的HD十分钟窗口（当前最新）

[4图](Results/Specialization_HD_Only_10min_20260915.md)。按上下文CORE+BTS+EMM+TITLE+AREA+Cheat，无SPC；仅Activity Monitor，配置/0城未独立截图。新PID71307（不是前场续测），621秒9.03→8.98→8.99→8.99GB，后302秒持平。记为本窗口no sustained growth observed；不将前场+.19短期增长视为同类持续泄漏已复现。两侧单独存在均有持平窗、一起有增长窗，支持交互候选但测试领袖/面板状态仍有差异。下一步只读交互路径调查，不派发新用户测试或改代码。
