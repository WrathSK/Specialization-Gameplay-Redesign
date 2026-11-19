# B527 architecture convergence closeout — scoped Advisor audit

> Advisory / Non-authoritative / No design decision implied

- **Status:** Stable
- **Maintainer:** Claude (Advisor session; role resolved under W0005 R9 by the Owner's instruction)
- **Requested by:** the Owner, through `Specialization/Reports/Proposals/Architecture_Convergence_Closeout_Audit_Handoff.md` (Status S1094)
- **Date:** 2026-11-17
- **Scope:** scoped closeout re-review of the approved convergence responsibilities (O1–O8), the recent hand-overs S1072–S1089, evidence inheritance and the five Architecture description candidates. This is not a new full audit of the trunk.
- **Fixed basis:**
  - audited runtime code B527.554, `5cf9b48463cc5f875ebab562cc89c9cedb9d0bcb`
  - closeout material and latest acceptance `9a298a91f5a5477851fe1189b3df8dacc9b4c6d2` (Status S1093); closeout draft SHA256 `baf5c78574b66dc655d8e082d8e1eb568f411534c058a8d3c87fe47d4b5cc87d` (re-hashed, matches)
  - stable comparison B489.516, `ce497054ed0ba440a03c5a7a66dfafc0d5721c3d`
  - temporary install source `1495cbd1a32d2877df5aab8ecedcacbd733f35d9` (its `Mod` tree equals the audited code)
  - Architecture A0185, Design D0060, four-profession content D0059
- **Worktree at audit time:** `develop` at `7e69d80a`, one commit after the material baseline. That commit adds the handoff and touches Status, Authority, the Context Lock and P0-H only. `git diff 5cf9b484 HEAD -- Mod` is empty, the worktree is clean and `context.py check P0-H` passes (314 runtime files). The fixed material was read with `git show`.
- **Method limit:** read-only. No test, game, probe or deployment tool was run and Git was used for queries only. Every local-evidence conclusion below rests on reading test definitions and saved artifacts. Every native conclusion rests on the retained collector records and engine load logs. Nothing here is a reproduction.
- **Evidence labels:** STATIC_CONFIRMED = code, database or record evidence read in this audit. LOCAL_SIMULATION_PASS = a saved local simulation result. USER_GAME_TEST_PASS = the Owner's native observation in the stated scenario. NOT_MEASURED = no evidence in the stated scope.

## 中文 Owner 摘要

当前阶段：架构收敛工程结项前的独立复核。审的是 B527.554 运行代码与结项稿，全程只读，没有运行任何测试或游戏。

结论：**有条件可以结项（CONDITIONALLY READY）**。没有发现会阻塞结项的运行缺陷。已批准的八项职责都有现行责任模块；25 个旧文件退出后没有残留的有效依赖；网络收益与不可逆操作的保护自 B489 稳定版以来没有被改动；本地测试记录与 B527 代码逐字节对应；两批实机记录与日志相符。

实际问题只有三处记录与措辞，都不影响玩法：

1. 无 HD 的 69 条目环境里，多出的 41 个 Mod 不全是界面 Mod，其中有会实际运行的玩法脚本和数据库更新。结论应写成“官方装配分支在这套实际配置下通过”，不能当作固定 28 条目官方环境在 B527 上通过。
2. 保留项清单漏了一条仍未观察的事项：HD 下工程研习加成的精确数值。
3. 五处正式说明更正都准确，可以按事实同步。但正式架构后段还有五节把已移除的模块写成现行，建议同批加上历史标注。

推荐下一步：Primary 修正上述措辞并完成事实同步，然后记录结项。

需要您决定：是否接受有条件结项；是否在晋升 main 之前，用固定 28 条目官方环境冷读一次现有存档做一次短测。这次短测是可选项，不阻塞结项。结项本身不需要新的实机测试。

## 1. Is the work ready for engineering closeout?

**CONDITIONALLY READY.** No runtime defect that blocks closeout was found. The three conditions are record corrections and need no code change.

**What the verdict covers.**

- Engineering closeout of the approved convergence scope on `develop` at B527.554: the O1–O8 responsibility transfer, the S1072–S1089 retirements and the evidence set as recorded.
- Supported saves: current-build new games and same-build saved games.
- Environments as measured: the fixed 94-target HD baseline, and the official data-assembly branch as observed in the 69-target no-HD configuration. B489.516's two pinned profiles are inherited for the capabilities whose owners are unchanged or changed only in who performs the old-carrier withdrawal (section 3.2).

**What it does not cover.** Main promotion and stable deployment keep their own gates. The verdict gives no B527 result for the pinned 28-target official profile, no compatibility statement for the 41 additional mods, no numeric Culture amount, no cold-load continuity of a positive no-HD Culture Network benefit, and nothing on performance or bilingual layout.

**Conditions.**

| # | Condition | Finding |
|---|---|---|
| C1 | State what the 41 additional entries contain and keep the claim at "official assembly branch in the observed configuration". | F-1 |
| C2 | Add the open HD Engineering Study uplift observation to the retained list. | F-2 |
| C3 | When the five corrections are synchronised, also mark Architecture lines 599–634 as historical, or record that this is deferred. | F-3 |

Runtime defects and the pending documentation sync are separate matters. Runtime defects: none found. Pending sync: five accurate candidates plus the extension in F-3 (section 2).

## 2. Can the five formal description corrections be handled as factual sync?

**Yes, all five.** Each matches the code at `5cf9b484`. None hides a rule choice or an implementation problem. The list is not exhaustive (F-3).

| # | Architecture location | Verdict | Code basis at `5cf9b484` | Wording note |
|---|---|---|---|---|
| 1 | Line 94, "当前专业事实" row | Accurate | `Mod/EffectiveFacts.lua:105–112`: the production branch asserts `foundationStore.Owns(city)` and reads `foundationStore.Base`. `Mod/CityProgressionStore.lua:1519–1521` sets `UsesNewAuthority=not legacyTest`. | The `else` branch at `Mod/EffectiveFacts.lua:111` still names `shared.CityFlowProbe`, whose file is no longer packaged. Describe it as reachable only through `StartLegacyTest` in test fixtures, with its module not shipped. |
| 2 | Line 105, Store and old shells | Accurate | BindingProbe, CityFlowProbe, CityJournalProbe and FreshBindingHook are deleted in `ce497054..5cf9b484`. No `include` or modinfo `File` entry remains. `Mod/CityProgressionStore.lua:1992–1993` returns true from `BlocksLegacy` in modern mode. | Three inheritance files remain packaged and unloaded (F-5). Keep the strict-identity and permanent-history sentences. |
| 3 | Line 97, "巨作事实" row | Accurate | `Mod/GreatWorkFacts.lua:388–462` holds the transport (`StartDialogueTransport`, `Receive`, `ConfirmSamplePair`, post-cleanup at `:455`, return slot at `:457`). `Mod/Gameplay.lua:787` starts it. `Mod/Dialogue.lua` and `Mod/DialogueModel.lua` are deleted. | The phrase "旧Dialogue独立投影保留" has to be removed, not only supplemented. `shared.Dialogue` survives as a retired transport record published by GreatWorkFacts. |
| 4 | Line 170, "收益应用与玩家呈现" | Accurate | `Mod/StandardizationCatalog.lua:29–62` and `Mod/StandardizationEffects.lua:18–19, 158–166, 476–482` own the B054 and B051 withdrawal. `Mod/LegacyCleanup.lua` hosts the purchase, Great Work, Commerce, level-3, Boost and Dialogue load cleanups (`:14, :28, :44, :84, :111, :217, :312`). Culture owners withdraw their own old carriers. | The same sentence says B234 "disables normal NetworkBoost output". `NetworkBoost.lua` is gone. Its exact withdrawal and startup now sit in `Mod/LegacyCleanup.lua:217–308`. |
| 5 | Line 174, UI prototype paragraph | Accurate, additive | `Mod/SpecializationP0.modinfo:10–19` defines the two environment criteria. Environment-exclusive `ReplaceUIScript` pairs exist for UnitPanel (`:62–63`), CityPanel (`:81–82`), CityPanelOverview (`:84–85`) and ProductionPanel (`:449–464`). The retained no-HD load log applies the official replacements. | Keep the prototype sentence as history and add the current pairs. |

## 3. Evidence: over-claims, omissions and inheritance

**Summary.** I found no over-claim that changes the verdict. There is one wording gap (F-1), one omission (F-2) and one provenance gap that Primary can close with existing commands (section 3.1, item 2). Inheritance from B489 holds for the stated owners.

### 3.1 Local evidence

The four S1089 artifacts support what S1089 claims.

| Stage | Tests | Status | Checked |
|---|---|---|---|
| O8IntegrationCandidate | 41 | LOCAL_SIMULATION_PASS | SHA256 matches Status |
| O7DialogueTransport | 44 | LOCAL_SIMULATION_PASS | SHA256 matches Status |
| NReadOnlyNetworkDiagnostic | 136 | LOCAL_SIMULATION_PASS | SHA256 matches Status |
| NStandardizationEffectReadback | 118 | LOCAL_SIMULATION_PASS | SHA256 matches Status |

- **Source binding.** Each artifact records `source_head` `49d02848` with `source_dirty=true`, because the run preceded the commit. The recorded 931-file source snapshot (`Mod`, `DevelopmentTests`, `tools`) is byte-identical to commit `5cf9b484`. The artifacts therefore bind to the audited code.
- **Environment.** CPython 3.14.8, Lupa 2.8, Lua 5.1 backend, as Status states.
- **Overlap.** The four stages overlap. Their union is 250 distinct passing tests, not 339.
- **What the new tests assert.** `DevelopmentTests/test_o8_integration_candidate.py` has three tests: the real work sender keeps two packets with and without the old model; the exact model removal round-trips; the temporary switch and restore run against the actual B489 package hashes (337 → 314 files, 25 removals, 2 additions).
- **Cited artifacts.** For S1072–S1089, every artifact that Status cites is LOCAL_SIMULATION_PASS, with one disclosed exception: the S1074 legacy-panel run (32 of 33; a stale byte-comparison test, later replaced by O7DialogueTransport 44/44). The 12 other FAIL artifacts in those directories are uncited iterations whose source snapshots differ from the cited runs.

Three limits apply.

1. **The package file model is not the native loader.** `DevelopmentTests/refactor_harness.py:62–98` states that `PackageVFS` does not model native include caching, basename aliases, external HD or official search, or native throw and nil semantics. The missing-file composition tests show that the package has no internal dependency on the removed paths. My own static scan agrees (section A.2). Native include behaviour for the loaded set is shown only by the two native sessions.
2. **Several slice stages have no artifact at the final commit.** They last passed at their own slice commits. `Mod/Gameplay.lua` and `Mod/LegacyCleanup.lua` changed in later slices.

   | Stage | Last passing artifact | Tests outside the final union |
   |---|---|---|
   | O7InspirationCleanup | S1081 | 45 |
   | O7MeaningCleanup | S1087 | 27 |
   | O7wLegacyCompletionRecordRetirement | S1081 | 25 |
   | O7AestheticCleanup | S1087 | 19 |
   | O7CommerceCleanup | S1085 | 18 |
   | NCommerceEffectReadback | S1083 | 11 |
   | O7Level3Cleanup | S1085 | 6 |
   | O7BoostCleanup, O7BoostStartupHandoff | S1086, S1088 | 4 |
   | NCultureNetworkEffectReadback | none in S1072–S1089 | not compared |

   The exposure is limited. In each case the owner module that the stage targets (`CultureInspiration.lua`, `CultureMeaning.lua`, `CultureAesthetic.lua`, `Commerce.lua`, the level-3 and Boost parts of `LegacyCleanup.lua`) did not change after the stage's last passing run, and `Mod/CultureNetwork.lua` is byte-identical to B489. What changed later is shared composition (`Gameplay.lua`, other parts of `LegacyCleanup.lua`, `GreatWorkFacts.lua`). After the S1088 commit only `Mod/DialogueModel.lua` (deleted), `Mod/Probe.lua`, the modinfo and `Mod/UI/DialogueRefresh.lua` changed. This is a provenance gap, not a suspected failure. Section C gives the commands.
3. **Fault handling is proven under artificial faults only.** Partial writes, failed readbacks and rejected removals are injected by the fixtures. No native write failure occurs in the captured sessions. The closeout draft does not claim otherwise.

### 3.2 Native evidence and inheritance

**HD Great Work and cold load (S1091).** The record is accurate.

- The manifest SHA256 matches.
- The 94 loaded gameplay targets equal the fixed HD baseline.
- The activation, distinct-era and city-local results (none at ACTIVE I; 1 and 2 at ACTIVE IV; 2 and 4 after the Medieval work moves in) are Owner observations with no screenshot, as S1091 says.

**No-HD Culture Network and load readiness (S1093).** The record is accurate, with the wording gap in F-1.

- The manifest SHA256 matches.
- The load log applies `SPC_EnvironmentOfficial` and no HD component. HD core `521b8777…` is absent from the 69 targets.
- The 69 targets include all 28 of the prior pinned official profile. All 41 additional entries also belong to the fixed HD baseline's 94.
- At T24 the trace shows `NETWORK_VERIFIED` with one route (seq1277), `CN_PROJECTED` for city 65536 with count 1 (seq1278), a second route (seq1293) and `CN_PROJECTED` for city 196610 with count 1 (seq1296). `CN_READY` follows at seq1281 and seq1297.
- `CN_PROJECTED` is recorded after the owner's reconcile and readback, so the configured carrier is confirmed by the mod. The benefit itself is the Owner's observation ("商路发出后立刻生效"), without numbers.
- The session contains a full 人文考察团 sequence through the mod's own flow (created, travelling, arrived, task preparing, task running) and trade routes dispatched at T24. It also shows accelerated setup, for example a 13,520 treasury change during T1 and a Culture IV city by T24. Treat it as cheat-assisted setup with the real ability flow, not as a natural-pace game.

**What the 69-target official-branch result supports.**

| Statement | Supported? | Basis |
|---|---|---|
| The official data-assembly branch was selected and HD was not loaded. | Yes | Load log |
| Startup and first-local-turn cleanup reached READY in two saved-game contexts of one new process. | Yes | seq290; seq446 → T2 seq526 |
| A same-turn route proof led to a positive Culture Network projection, with owner readback, for two receiving cities. | Yes | seq1277–1297 |
| The Owner saw the benefit appear immediately. | Yes, as an Owner observation | S1093 |
| The mod took the same route-source path it would take without Better Trade Screen. | Yes, STATIC_CONFIRMED | `Mod/UI/BackgroundRoutes.lua:1, :57` reads the native outgoing routes and has no Better Trade Screen dependency. The file is unchanged since B489. |
| The pinned 28-target official profile passes these points on B527. | No, NOT_MEASURED | No B527 session used that profile. |
| The official branch ran without third-party gameplay code. | No | F-1 |
| Exact Culture amounts are as designed. | No | Not supplied |
| A positive no-HD Culture Network benefit survives a cold load. | No, NOT_MEASURED | No reload followed the benefit. |
| The 41 additional mods are compatible in general. | No | One session |

For closeout, the supported wording is: *the previously open official-branch observations (positive Culture Network and first-supported-turn cleanup) are now observed on B527 in the official assembly branch, in a 69-target configuration that also loads third-party gameplay scripts and database updates; the pinned 28-target profile keeps its B489 scope.* The closeout draft's summary, evidence table and retained row already say most of this. C1 adds the missing fact about what the extra entries contain.

**Is a native fact still missing that blocks closeout?** No. The remaining difference is narrow. The pinned profile and the observed one select the same assembly branch, the same UI replacements and the same mod code path. They differ in the presence of third-party scripts and data. A defect that appears only without those 41 mods would have to come from an interaction that B489's pinned-profile acceptance did not show, in owners that have not changed since B489. I judge that unlikely enough not to block an engineering closeout. I recommend closing it before main promotion, because the stable baseline's acceptance names the pinned profiles.

**Optional minimal distinguishing step (one short session, Owner's choice).** Switch the mod configuration to the pinned official profile first, then cold-load the T24-or-later save from this session (or any official-profile save that already has a positive Culture Network benefit). Check that the load shows 28 targets. Before ending the turn, confirm that the positive benefit is still present. Then end the turn once. This one session separates three open facts: pinned-profile identity on B527, cold continuity of a positive no-HD benefit, and behaviour without the third-party scripts. The existing evidence cannot separate them, because its only positive sample was taken in the 69-target configuration and was never reloaded.

**Inheritance from B489.516.** Inheritance holds where the owner is unchanged or changed only in who performs the old-carrier withdrawal.

| Owner | Change `ce497054..5cf9b484` | B527 native observation | Inherited from |
|---|---|---|---|
| `CultureNetwork.lua`, `NetworkBridge.lua`, `NetworkInput.lua`, `NetworkSender.lua` | none | positive no-HD Culture Network (S1093) | B489 and earlier HD positive cold-load evidence |
| `Commerce.lua` | +3/−2, old cleanup call moved | none positive | B489 (S1047) |
| `StandardizationEffects.lua` | +7/−5, own withdrawal source | none positive (every sample has `expected=0`) | B489 HD positive cold reload (S1047) |
| `CultureAesthetic.lua` | +23/−2, own old-percent withdrawal | HD Great Work (S1091) | not needed |
| `CultureInspiration.lua`, `CultureMeaning.lua` | +47/−4 and +13/−2, absorbed exact old withdrawal | none specific | B489 official Research and Meaning (S1047) |
| `CapitalInvestment.lua`, `DevelopmentInvestment.lua`, `CrewProjects.lua`, `CityProgressionStore.lua`, `RuntimeComposition.lua`, `FactChanges.lua`, `RuntimeWork.lua` | none | none specific | B489 and earlier action acceptance (S0902, S0904, S0906, S1047) |

The retained old-carrier SQL still loads in both environments (for example `Data/CultureInspirationProbe.sql` has no criteria), so the absorbed withdrawals can validate their definitions in the official branch too.

### 3.3 Reading the readiness samples

The three readiness samples need care (F-6). `B055_GW` is PENDING at every `AFTER_LOAD` sample and READY at every `FIRST_LOCAL_TURN` sample. The `AFTER_LOAD` sample is taken before later-registered load-close listeners have run. Culture Aesthetic shows this: its load-close listener sets ready unconditionally (`Mod/CultureAesthetic.lua:232–235`), yet it is PENDING at `AFTER_LOAD` in the B489 and B527 sessions alike. A PENDING `AFTER_LOAD` value is therefore not evidence of a failed load-close cleanup, and the samples cannot tell whether readiness was reached at load close or at the turn. S1091, S1093 and the closeout draft claim readiness at the first local turn only. That claim is accurate.

Two smaller reading notes:

- `notReady` is never `NONE`. The entries `TPR` and `DP` report `UNKNOWN` in every sample at B489 and B527 alike. They have no boolean ready field. This is a pre-existing property of the summary, not a B527 change.
- One HD context (`session-20261118T013200Z-6569e2`) ended at T1 without a local-turn sample. S1091 already records it as unobserved.

## 4. Findings

**No finding blocks closeout.** The non-blocking findings follow in the requested structure.

### F-1 — The 69-target configuration includes third-party gameplay code (Low; evidence wording)

- **Type:** real native record (retained load log), compared with the B489 pinned official session.
- **Business scenario:** the Owner reads "official branch verified" and later relies on it for the pinned official profile or for a main promotion statement.
- **Existing contract:** Architecture "Accepted convergence boundaries" (support and evidence); roadmap O8: "Load/carrier readback alone not PASS… New game per changed build/environment"; handoff: "'不影响存档'标记不能单独证明完全没有运行影响".
- **Location:** Status S1093 (`Specialization/Status/Specialization_P0_Status.md:33–41`); closeout draft lines 47–49 and the retained row at line 58.
- **Evidence:** components present in the 69-target load and absent from the B489 pinned official load:
  - 8 `AddGameplayScripts` components: `CheckOverflow`, `CityCanalRework_AddScripts`, `Custom_Notifications_lua`, `KDWR_gameplay`, `OverflowBugFix_lua`, `goody_huts_detection`, `md_scripts`, `qd_cachemanager`
  - 2 `GameplayScripts` components: `ImprovedCombatReports_Config`, `PolicyChangeReminder_Config`
  - 14 `UpdateDatabase` components, mostly settings, notification and colour data
  - 16 `ReplaceUIScript` components. By component name none targets the six UI contexts this mod replaces, but a component name does not prove its target context, and one (`ReplaceUIScriptNew`) I could not attribute. All six contexts loaded in that session and the 人文考察团 chooser flow completed.
  - 16 `AddUserInterfaces` components
- **Mechanism:** the extras fit the Owner's explanation. They are entries that the engine takes from the current configuration rather than from the save. The load log shows that this class still includes gameplay scripts and database updates.
- **Minimal counterexample:** a reader takes "41 additional entries such as Better Trade Screen" to mean interface-only mods. The load log registers gameplay scripts from overflow-fix, movable-district, canal-rework and deal-cache mods in the same session. The result cannot be restated as "the official profile without third-party gameplay code".
- **Minimal remediation:** add one sentence to S1093's environment boundary and to the closeout draft: the additional entries include gameplay scripts and database updates, so the result demonstrates the official assembly branch in this configuration. No test is needed for this correction. The optional step in section 3.2 closes the remaining difference.

### F-2 — An open observation is missing from the retained list (Low; omission)

- **Type:** record evidence.
- **Business scenario:** after closeout, the retained list is used as the complete set of open native observations.
- **Existing contract:** Status S1048, `Specialization/Status/Specialization_P0_Status.md:584`: "Positive official Culture Network output and the exact HD Engineering Study uplift remain open observations."
- **Location:** closeout draft lines 53–63 ("结项后继续保留的事项"). The first item is now observed in the 69-target configuration. The second is not listed anywhere in the draft.
- **Evidence:** no B527 session has an uplift sample. In all five collector sessions every `INDUSTRY_STANDARDIZATION` row has `expected=0`, and every `ENGINEERING_STUDY` row is INELIGIBLE with count 0. The inherited native value is the B443 official observation (S0949, 10% → 12%).
- **Minimal remediation:** add one retained row: the exact HD 工程研习 uplift remains an open observation, to be noted during ordinary HD play.

### F-3 — The five candidates are accurate but not the whole stale-description set (Low; documentation)

- **Type:** document evidence at `HEAD`.
- **Business scenario:** a later session reads Architecture as the current implementation description, which the project map tells it to do.
- **Existing contract:** root guidance: do not infer current completion from old notes; Architecture already marks lines 541–597 with "历史baseline描述，非当前实现矩阵".
- **Location and evidence:** `Specialization/Architecture/Specialization_v0.1_Architecture.md`
  - `:599` "B055：网络Boost与巨作接口测试", `:617` "B052运行适配", `:623` "B053货币适配调查", `:627` "B054自动折扣运行适配" and `:631` "B054.71启动补偿" carry no historical banner. They describe `StandardizationDiscount`, `DiscountEligibility` and the Boost test interface in the present tense. Those modules left the package in this range. The B054 section opens "当前正式状态以本段及Status为准".
  - `:155` still says "当前仍保留部分旧专业consumer".
- **Minimal remediation:** put the existing historical banner on those five sections and adjust the line-155 sentence in the same factual sync. If Primary prefers to defer it, record that explicitly so that "five corrections" is not read as "all corrections".

### F-4 — The hidden network-isolation diagnostic can no longer be armed (Info)

- **Type:** code evidence.
- **Location:** `Mod/NetworkIsolation.lua:5, :7, :15–21, :54–62`; `Mod/UI/P0Panel.lua:148–158`.
- **Evidence:** arming needs acknowledgements from `SPC_CopyBackground` and `SPC_DiscountEligibility` and an `ExperimentalNetworkWithdraw` function on `shared.CopyYields` and `shared.StandardizationDiscount`. Their definers were removed in this range. No panel control dispatches the command at either baseline. If it were sent, the panel would fail closed with a readable message.
- **Impact:** none for players. The B137 diagnostic and the `ExperimentalNetworkWithdraw` paths in the remaining owners are inert.
- **Minimal remediation:** list it as inert in the closeout record, or retire it in a later cleanup slice. No action is needed for closeout.

### F-5 — Packaged files and branches that only tests can reach (Info)

- **Type:** code evidence.
- **Location:** `Mod/CityInheritance.lua:63, :70`, `Mod/InheritanceShadow.lua:26, :39` and `Mod/CityInheritanceRead.lua` are still listed in the modinfo and never included; `Mod/Gameplay.lua:800–802` clears their slots. `Mod/EffectiveFacts.lua:111` and `Mod/CityProgressionStore.lua:2157` are legacy-test branches that name deleted modules. `Mod/CityProgressionStore.lua:30–32` still lists four retired names in `returnPhase`.
- **Impact:** none in production. The package count of 314 includes three files with no runtime role.
- **Minimal remediation:** none for closeout. Mention them when candidate 2 is synchronised so that "shells retired" is not read as "no old city file remains".

### F-6 — The after-load sample cannot confirm the load-close cleanup (Info; native observation)

- **Type:** real native record plus code evidence.
- **Location:** `Mod/ReadinessSummary.lua:40–52`; `Mod/LegacyCleanup.lua:293–308`; Status S1088.
- **Evidence:** section 3.3. S1088 states that the new startup order "is not measured in native play". The native sessions now show the outcome (READY by the first supported local turn in every context that reached one). They do not show which of the two allowed boundaries did the work.
- **Impact:** none on supported saves, which carry no old Great Work carrier to remove.
- **Minimal remediation:** none. Keep the wording at "first local turn".

## 5. Retained limits and scope not independently verified

**Retained limits that stay open after closeout.**

- Turn-start route checks and the existing recovery entries (Owner decision, S1029).
- 施工队: other count orders and late callbacks. 认领: anomaly source. 人文考察团: border displacement.
- Historical fixture non-passes, kept at their own baselines. No full historical run was made.
- The pinned 28-target official profile on B527, and positive no-HD cold continuity (F-1).
- The exact HD 工程研习 uplift (F-2).
- Bilingual layout under real languages. Performance, long-game memory and native timing.
- Support scope: current-build new games and same-build saves.

**Not independently verified in this audit.**

- No test was executed. Local results were read, hashed and bound to source, not reproduced.
- Native behaviour was not observed by me. I read the retained records and logs. Lua console output is not in the retained set, so startup error prints cannot be checked.
- The internals of the trunk slices S0910–S0949 were not re-reviewed beyond their current entry points. I relied on Status records and my earlier Advisory reviews for those.
- City exit and transfer cleanup were not exercised natively on B527.
- S1091 and S1093 record no B527 native observation of positive Commerce, Standardization, Inspiration or Meaning, and the B527 traces contain no positive Commerce or Standardization row. These rest on inheritance (section 3.2).
- The bilingual text changes were sampled for behaviour preservation only.
- One `ReplaceUIScript` component in the 69-target load could not be attributed to a mod.

## A. What was checked and holds, by audit question

### A.1 Trunk responsibilities (O1–O8)

No approved production responsibility is untransferred (STATIC_CONFIRMED).

- **O1 and O5a.** `Mod/Gameplay.lua:711` composes EffectiveFacts on the Store. The environment SQL is selected by the two criteria in `Mod/SpecializationP0.modinfo:10–30`.
- **O2 and O5b.** `Mod/Gameplay.lua:661–699` reserves 29 exit and 22 return slots before their owners start. The reserved names equal the names registered in the tree. The only change from B489 is the removed `GreatWorkAdjacency` return slot. `Mod/RuntimeComposition.lua:12–29` makes a reserved slot fail closed when its owner did not start.
- **O3.** The three network writers are unchanged except for withdrawal ownership (section 3.2).
- **O4.** The Store, the investment actions, 施工队 and the timed projects are unchanged since B489. `Mod/DialogueProjects.lua:124–135` and `Mod/UI/TimedProjectQueueIntent.lua` replace a Chinese substring match with reason codes. The only B489 producer of that text was the Dialogue project owner.
- **O6.** Section 2, row 5.
- **O7.** Sections A.2 and 3.1.
- **O8.** Section 3.2.

### A.2 Completeness of the recent exits

The 25 deleted files leave no live dependency (STATIC_CONFIRMED).

- Every internal `include` target exists in the package. The targets that do not resolve inside the package are base-game or HD UI files.
- Every `shared` slot that is read without a producer is guarded, or belongs to an unloaded file or a legacy-test branch (F-5).
- Every UI request action has a Gameplay handler.
- The central LegacyCleanup exit keeps the same 11 catalogue groups (`Mod/LegacyCleanupCatalog.lua:5`). At B489 the old modules already ran under that central exit or as retired facades, so no group changed owner at exit time.
- The old-carrier SQL remains in the package, as O7 requires.
- The S1088 startup change keeps the earlier order: the Research attempt first, then the Great Work cleanup, now on Gameplay listeners (`Mod/LegacyCleanup.lua:293–308`).

### A.3 Network and irreversible-operation constraints

The constraints hold as far as static review and the recorded evidence reach.

- Pending retention, reliable negatives, current transaction proof and partial-write handling live in files that are unchanged since B489, or changed only in withdrawal ownership.
- The B486–B489 corrections from my S1032 review remain in place: the Commerce sample is recorded before the write, the Standardization source witness is retained, and Culture Network discards confirmed losses.
- Contract terms and unique completion proofs sit in unchanged owners.
- Fault-injection conclusions are local and artificial (section 3.1, item 3).

### A.4 to A.6

Local evidence: section 3.1. Native inheritance: section 3.2. The five corrections: section 2.

## B. Scope expansions and reasons

- **Roadmap goals at `fb7be65b`.** Read to compare O1–O8 with the closeout table. The closeout draft cites the goals by label only.
- **B489 official load log and the fixed HD baseline manifest.** Read to compute what the 41 additional entries contain and whether they belong to the HD baseline. The handoff asks for a judgment on the 69-target result.
- **`Mod/UI/BackgroundRoutes.lua`.** Read because Better Trade Screen is among the additional entries and the project has a recorded route-source decision.
- **`Mod/NetworkIsolation.lua` and `Mod/UI/P0Panel.lua`.** Followed from the deleted `CopyYields` and `StandardizationDiscount` producers to their remaining consumers.
- **B489 readiness samples.** Read to decide whether the PENDING after-load values are new in B527.

## C. Candidate changes and validation implications

These are suggestions for Primary. None is a precondition beyond C1–C3.

1. **Record corrections (C1–C3).** Documentation only. The existing publication checks and the Context Lock apply. No test is needed.
2. **Optional: bind the slice stages to the final commit.** Purpose: one artifact per stage at `5cf9b484`, so that the closeout record does not rest on module-identity reasoning. Missing evidence: section 3.1, item 2. Run each stage in its own process, with the same environment as S1089:

   ```sh
   python3.14 -B DevelopmentTests/run_refactor.py --stage <Stage> --output local/refactor/<dir>/closure.json
   ```

   Stages: `O7InspirationCleanup`, `O7MeaningCleanup`, `O7AestheticCleanup`, `O7CommerceCleanup`, `O7Level3Cleanup`, `O7BoostCleanup`, `O7BoostStartupHandoff`, `O7wLegacyCompletionRecordRetirement`, `NCommerceEffectReadback`, `NCultureNetworkEffectReadback`.
3. **Optional native step before main promotion.** Section 3.2. This is the Owner's test and the Owner's choice.

## D. Read ledger

- **Governance:** root and project guidance, W0005 with R9 and the shared advisory boundaries, the Advisory guidance and report template.
- **Closeout material:** the handoff; the closeout draft at `9a298a91` in full; Status CURRENT and S1094–S1088 in full; S1087–S1072, S1048, S1047, S0949 and S0902–S0906 as needed; Authority version pointers.
- **Architecture:** accepted convergence boundaries, environment assembly, the entry and responsibility table, facts and saves, network sections, effect application and presentation, P01–P10, and section headings from line 500 to the end.
- **Runtime source at `5cf9b484`:** `Gameplay.lua`, `LegacyCleanup.lua`, `LegacyCleanupCatalog.lua`, `EffectiveFacts.lua`, `CityProgressionStore.lua` (entry points and guards), `NetworkInput.lua`, `StandardizationCatalog.lua`, `StandardizationEffects.lua`, `GreatWorkFacts.lua`, `CultureAesthetic.lua`, `CultureInspiration.lua`, `CultureMeaning.lua`, `Commerce.lua` (changed parts), `NetworkIsolation.lua`, `ReadinessSummary.lua`, `RuntimeComposition.lua`, `DialogueProjects.lua`, `SpecializationP0.modinfo`, `UI/BackgroundRoutes.lua`, `UI/P0Panel.lua`, `UI/TimedProjectQueueIntent.lua`; the full `ce497054..5cf9b484 -- Mod` name and line statistics, with diffs of the changed owners.
- **Tests and artifacts:** `test_o8_integration_candidate.py`, `test_o7_legacy_panel_cleanup.py` (startup recovery), `refactor_harness.py` (`PackageVFS`), `refactor_selection.json`; every `closure.json` under `local/refactor/S1072-*` to `S1089-*` (status, source binding, test lists).
- **Native evidence:** both B527 manifests, their collector records and load logs; the B489 official and HD collector records and the B489 official load log; the fixed HD baseline manifest.

## E. Checkpoint and handoff

- **User decision:** accept the conditional closeout with C1–C3, or ask for changes. Decide whether to run the optional pinned-profile cold check before main promotion.
- **User testing:** none required for engineering closeout. Optional: the single short session in section 3.2.
- **Primary next:** apply C1–C3 with the factual Architecture sync under the current revision process; optionally refresh the slice stages at the final commit; then record the closeout. Main promotion and stable deployment follow their own authorization.

This report is Advisory. It authorizes no Design change, implementation, deployment or promotion.
