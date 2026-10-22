# B175.202 — Era Dialogue project/history gate + B174 combined package

Date: 2026-10-09. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.**
Baseline: develop `dcc43aa5c828bd0f2aa5d3d121734f5db5cb6ad3` (B174 source-only); recorded deployed B173.200 before this batch. Authority: Culture D0049 `CUL_L3_DIALOGUE`, full Dialogue/work-pool contracts and Shared D0045 lifecycle A/E/F. No Design change.

## Delivered scope

This is the approved first [P0-M slice](../../../Architecture/v2/P0_M_Dialogue.md#current-slice--b175202-project-and-history). The normal production list offers **时代对话** to Culture ACTIVE III+. A 1,000,000-cost real project uses the accepted one-turn native completion route. It requires one current queue item; no P0 enable switch, empty-queue workaround or blocker bypass. The current project, city panel and banner reuse the established timing display.

The first slice records real accepted Dialogue history: START Game Era, one successful completion per city/START era, completion-time supported era diversity X, +5×X percentage points, and a dedup receipt. X0 consumes the era opportunity. Repeated successes in different Game Eras add without an additional gameplay cap. These are city-owned records in the existing Store, not owner-partitioned copies or a new city identity system.

**The new cumulative yield multiplier is not applied in this batch.** Old Dialogue effects and its K sampling/ACK transport remain unchanged. The read-only P0 **时代对话** button explicitly says the cumulative record is not yet actual output. Native-only yield projection and retirement of the old writer require later scoped work; no full P0-M PASS is claimed.

B174's independently reviewed investment propagation repair is included. Housing and GPP still consume its proved commit result. Only one additional target-city entry refresh is notified when an investment makes Dialogue eligible; a Dialogue startup/notification exception cannot erase the investment result or block those two writers.

## State, event and failure boundaries

| Owner | Data / lifetime |
|---|---|
| Existing CityProgressionStore record | Optional `dialogueKnown=true` plus versioned Dialogue history, receipts, cumulative total, serial, last result and at most one pending attempt. Absence means never initialized only when both fields are absent; a witness/data mismatch or invalid record holds. No new Game property key/index. |
| DialogueProjectModel | Pure validation and begin/end/calling/complete/cancel transitions. Cancellation removes only the pending attempt, not successful city history. |
| DialogueProjects | Exact entry marker and bounded current-city view/dirty/pending maps. Confirmed owner loss invokes the existing module-owned exit; no broad building removal. Current ACTIVE is read, never restored from a snapshot. |
| UI adapter | Selection intent, bounded load handshake, display and one synchronous target-city completion read. UI cannot issue receipts or write saved history. Retry state ends on acknowledgement, limit or removal; unchanged view revisions do not rebuild display strings. |

Selection is only intent: Gameplay checks the real queue and authoritative city reference before persisting ACTIVE. Local turn deactivation records end-turn proof; the next local turn persists CALLING **before** invoking `FinishProgress`. Native `CityProjectCompleted` confirms the project; a fresh single-city read uses the existing reviewed collector/catalogue, checks reference and turn again, and supplies X. It never consumes an old background ACK or infers X from a carrier.

A single Store commit saves receipt, used START era and total together. Known ACTIVE loss, identity ineligibility, normal production interruption and confirmed owner loss cancel an unfinished attempt without using the successful quota. A same-publish away/back production change cannot preserve half-progress. UNKNOWN pauses rather than becoming zero or deleting history. REALLOCATING/identity cancellation is covered at the transition model boundary; this batch does not implement asset restructuring.

When completion-time facts are unavailable, the attempt holds without quota/reward. Later collection changes cannot repair that missing historical observation. CALLING after load is not reissued; a session-local completion arm prevents a late duplicate from resampling after an uncertain permanent commit. The user can abandon an unresolved attempt by choosing an ordinary production target, then start a fresh full turn if the quota is still unused. Stop and report the original uncertainty before doing this during acceptance.

The already accepted exceptional native forced completion remains distinct: if the real project completes early, record it as forced; do not call it proof of a full production turn. No new anti-cheat mechanism or production tracking ledger is added.

Only pending projects are considered at local turn stages. Initial load and a confirmed Game Era change reconcile local entry markers once; Governor changes reconcile qualification, preserving ordered cancellation. Completion and explicit report requests collect only that city. No additional per-frame scanner, AI monitoring, shared GC, new global dispatcher or ordinary-yield writer is introduced. Local operation counts are not native CPU/memory evidence.

## Local checks and inheritance

- New [project/actual Store suite](../../../../DevelopmentTests/test_dialogue_projects.py): legal entry, current X versus start X, START-era change, X0, duplicate/quota, production interruption, known/unknown ACTIVE, completed/pending load reconstruction, CALLING no replay, sample/reference/turn failures, write failures, second loss after a changed CityID, two-city isolation, and uncapped pure history accumulation.
- New [UI/package suite](../../../../DevelopmentTests/test_dialogue_project_ui.py): actual collector/Plan, 0/1 queue admission, one BEGIN, load SYNC never inventing a start, bounded retries, unchanged-publish no collection/notification, normal-item display isolation, actual P0 read callback/visibility/layout, SQL and package registration. SQL uses the read-only configured database's table DDL in memory; distinct Type hashes are fixture-supplied because native hash assignment is outside SQLite DDL.
- Unchanged Claim UI/handshake/filter assertions and B127 timer/load groups run through adapters loading the new direct include; no historical assertions rewritten. Three additional actual Store investment/template/load/return groups retain existing checks.
- B174's 20 behavioral methods rerun, including actual normal/DEV ingress, both writers, fault evidence and scoped 8/20/40-city counters. Its old build201/package-bound static method is not applicable to build202; current package/static checks replace that version check, not its behavior assertions.
- Combined run: **63 methods / 66 explicit subtests PASS**. Lua syntax, XML/modinfo202 exact file registration (194 package files including modinfo), current selectors/context, document links and diff reviewed separately. No broad gameplay regression/stress or native test was run by Codex.

Run the two new suites with Python + `lupa.lua55`, `PYTHONDONTWRITEBYTECODE=1` and `SPC_DEBUG_GAMEPLAY_DB` (or existing `local/config.json:debug_gameplay_db`). The database is read-only; no installation/game launch is needed. B174 comparison additionally needs its recorded Git baseline. See the existing test environment instructions.

Native event ordering, live synchronous UI-to-Gameplay completion sampling and actual save serialization remain **USER_GAME_TEST_REQUIRED**. Existing high-cost project/Claim evidence supports reuse of that primitive, not a native PASS for the new Dialogue transaction. Unknown all-Owner/destruction/rebuilt-city boundaries remain unchanged. For rollback after this test, keep the pre-batch save and corresponding package receipt; do not promise that an old package understands a saved Dialogue attempt or clear history to make it load.

## 一次合并验收流程

尽量用同一座文化城：文化I、有正在工作的剧院专家，总督已满足III条件，且可以放入已支持的不同年代巨作。若没有合适的低等级文化城，B174用一座现有低等级专业城，Dialogue用现有文化III/IV城即可；不必专门重建完整测试世界。使用实施前存档的测试副本。

1. **B174投资刷新。** 正常使用开拓者从I投资到II。用P0 **城市专业 / 潜力**确认II；确认本城已有二级住房／对应GPP效果正常进入，另一座未操作城市不受影响。GPP按已知原生行为可等下一回合再看，不做全国小数归因或旧B173数值复测。同一文化城随后再投资到III即可。
2. **Dialogue启动与取消。** 打开P0 **时代对话**，确认文化ACTIVE III+、本时代机会未使用及当前合格馆藏时代数。在正常城市生产列表选择 **时代对话**，确认显示1回合及报告“完整一回合计时中”。同回合改选一个普通目标，再读报告：本轮取消、累计不增加、机会仍未使用。此步只验证新的业务取消，不要求调总督／易主等整套旧生命周期。
3. **Dialogue重新开始与完成取样。** 再次选择 **时代对话**。若方便，在结束回合前移入／移出一件唯一年代的已支持作品，让时代数从X1变为X2。正常结束这一回合。项目应完成；P0 **时代对话**应显示完成时X2、增加`5×X2`个百分点、本启动时代机会已使用，同一时代不能再选。不要用实际巨作产出核对这个累计数：新倍率尚未接入。本次过回合也可读取第1步的GPP刷新结果。
4. **一次保存／冷加载。** 完成后保存测试副本，完全退出再载入。直接读P0 **时代对话**：累计值和已用时代保持，不因加载再加一次；同一时代仍不可重选。这里验的是本批新Gameplay历史／额度的保存，不是Probe默认OFF或重复启停。

每步的信息价值分别是：正常投资的定域传播；新项目取消不收费；真实完成事件＋完成时取样＋额度；新持久记录不丢失／不重复。第3步若无法方便改变年代，可验证固定X，但必须把“完成时变化取样”标为未覆盖，不能代记PASS。一张完成报告和一句冷加载确认通常足够；异常才补相应画面。无需逐回合截图、GPP四舍五入排查、反复重启或额外长测。

若项目持续“确认中/已暂停”、正常一回合未完成、额度误用、累计不符或读档丢失：停止该路径，保留报告和测试存档，不靠重复点击、Cheat完成或改档绕过。区分 PROJECT_EVENT_ORDER / COMPLETION_SAMPLE / PERSISTENCE 边界后再修复。

## Deployment and next boundary

The source checkpoint contains both B174 and this first Dialogue slice. Deployment is recorded only after the existing W0003 receipt/hash/game-exit transaction completes; the pre-transaction live reference is B173.200. No main promotion or new native acceptance is implied.

Await the combined user result. Later native-only multiplier work and old Dialogue writer retirement remain separate, unimplemented slices. Do not advance N/U2, another audit repair or another profession automatically.

## Deployment checkpoint — 2026-10-09

Verified OS game exit and clean/pushed source `886484a69189ac6c5cdacfd409f065f66957387f`. Existing W0003 tools restored the exact B173 receipt's stable bridge, retaining the outgoing B173 package, then activated B175.202. Receipt `B175.202-886484a-playtest.json`: **DEVELOP_ACTIVE / 194/194 MATCH**, no pending transaction; B173 and stable recovery packages retained. Main/source contracts and GC unchanged; no game launch or new native PASS. Deployment metadata is committed separately from the implementation.
