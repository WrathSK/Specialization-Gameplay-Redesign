# Architecture v2 D2 — Remaining runtime consumers / event propagation

Document Owner: Codex
Build: develop B076.103 / modinfo103
Baseline: B075.102 / 5dc6221 (accepted C2)
Design: D0025 unchanged
State: LOCAL_SIMULATION_PASS; USER_GAME_TEST_PASS scoped short idle; temporarily deployed; no stable promotion
Mainline: A → B → C1 → D1 → C2 → D2 → E

## 用户摘要

本批整理样本、收益消费者和后台UI的调度。去掉Copy每秒扫描、Industry/Lv3执行完成后的无条件连锁检查、巨作旧样本提前检查以及多个UI固定间隔跨Context读取。城市事实/区域按同步批次共享，正式Network查询只读取A/B已验证视图。

正常有效输入的载体结果与B075逐值一致；精度、公式、Design、单位结算不变。STATIC_CONFIRMED表示静态源码证据；LOCAL_SIMULATION_PASS是实际Lua+模拟原生API通过，不是游戏运行通过。55GB ROOT CAUSE UNKNOWN；不能据此宣告内存泄漏修复。用户现在无需操作；建议审阅后选A临时部署长测，E继续后置。

## Trigger / owner 矩阵

| Consumer | DIRECT | INDIRECT | RECONCILIATION | DIAGNOSTIC / unchanged healthy paths |
|---|---|---|---|---|
| Copy | population, governor/current identity, district removal; UI district/building/improvement/feature/policy/tech/civic/resource/worker changes | verified Copy sample replacement; real Network publication | UI sample turn key once/local turn; Gameplay once/player/turn | Describe keeps manual live check; no1s sample poll |
| Industry Lv1 | identity/building/district/terrain evidence | verified base sample replacement | once/player/turn | ReadBase live/read-only; no worker-triggered Lv1 audit |
| Industry Lv3 / shared support | governor/identity; district retirement | base sample replacement only | once/player/turn | no Industry-Audit-finished fan-out; temporary sample holds retained |
| Lv3 effects / Commerce III | governor, workers, population/focus, district/building | Network publication for direct connected kinds | once/player/turn | no unconditional Lv4/Copy audit on completion |
| Lv4 per-worker % | governor/worker/population/focus, district/building | late worker UI notification | once/player/turn | formula/bit carriers unchanged |
| Network Boost | explicit test/control and ownership cleanup | A/B complete Network publication | once/player/turn (not every player's turn scanning all) | National read uses verified view; bounded init max3 per observed turn |
| Commerce IV | governor/worker/population/focus, building/production/territory/policy/tech/civic; retained native completion hooks | actual Mod write scalar change, Network publication | once/player/turn | city yields read fresh in batch; never cache by Network revision |
| Dialogue | collection create/move, slot/district/city/governor evidence in existing UI owner | received collection packet | existing UI turn dirty; remove redundant Gameplay turn audit against prior-turn sample | UI generic pulse already dirty-gated and retransmission bounded: retained byte-for-byte |
| GW adjacency | same collection/base-adjacency owner | adjacency packet processed after matching collection | shares UI owner turn reconciliation | remove Dialogue.Audit-finished call with OLD adjacency; governor audits both explicitly |
| Crew project access | identity/anchor, district/completion/transfer | none from Industry base audit | once/player/turn | no settlement/project/target modifications |
| GPP | workers/focus/governor + retained native completion | UI late worker notification, scoped player | one local/player turn; max3 throwing sends per dirty input | no arbitrary Network capture for worker-only notices; no Boost/Dialogue fan-out |
| Discount / Routes | D1/B069 existing owners | unchanged | unchanged | unchanged byte-for-byte |
| Runtime audit | local turn end, scalar counters | none | unchanged | file API gate failure still applies; do not promise Lua file log availability |

Native plot/transfer/GameEvents signatures are not guessed as player IDs. Such rare direct events retain full participant scope; native worker/governor/player-turn wrappers use known player scope. Native building notifications exclude BUILDING_SPC_ carriers; the actual-write scalar coalesces them after writes instead of reentering per bit. This is not a promise of one Audit per every real event: a direct callback plus a later actual verified publication can both be necessary. Unknown/unsupported third-party notification coverage is covered by the next-turn safety check, not fast polling. HD `UI/Custom/CityButton_ResourceClassification.lua`/`Gameplay/RegionalYields.lua` and Governor files provide local precedents for production/building/policy/governor event names; no HD changes, no guarantee all optional names exist in every context.

## Shared work and publication

`RuntimeWork.New` is ephemeral per synchronous Audit: Facts once/city; district collection indexed once/player then per-city slices. Index publishes only after full enumeration; dropped at Audit exit. It creates no saved state, cross-turn cache or history. Copy validates one current district set and one verified sample-row set per player/batch, indexed by city. Industry Lv3 shares its batch index with ReadBase. All arithmetic and write-if-different rules stay intact.

Network adds `CurrentNational`, `CurrentConnectedKinds`, `CurrentRecipientSources`: require ready owner, VERIFIED complete input plus contract/epoch/player/inputVersion/derivedFor/signature match. They never call Capture or derive. Existing explicit Refresh, old diagnostic queries, route evidence and owner event hooks remain. NEEDS_REVALIDATION availability can retain the last VERIFIED input; CONFIRMED_INVALID cannot be read as valid. Copy joins actual Network publication directly, replacing its dependency on unrelated Lv3 execution.

Commerce creates one incoming-edge index and caches source facts/native yields only within the current batch. All plans still precede writes. A fixed ephemeral `SPC_RuntimeUIRevision` advances only after actual P.CreateBuilding/RemoveBuilding/SetProperty calls. Generic Commerce/UI drains compare the scalar first, so unchanged input performs no expensive work. This is conservative actual-output invalidation (not a claim every write changes Commerce yield), no per-event arrays. No new counters are required: existing facts/district/city/write/transport/Audit counters measure the paths.

## UI scheduling

Copy/Industry keep C2 Before/ACK/epoch/reference/bounded3-send semantics. `NeedsSample()` only exposes whether an unfinished bounded transport attempt needs a producer; direct dirty, turn or actual write can request fresh sampling. Pending blocks produce; a stable accepted sample with no dirty returns before Live/GetYield. SetUpdate now only advances the scalar C2 timeout clock.

CityPotential: selection/turn/actual write requests once, not every2s; unchanged text is not set again. Unit actions: same unit position/turn/input retains verified view instead of expiring1.5s and querying every0.5s. Queue/production/district/transfer events and completed user action dirty it; identical tooltip/layout does no work. Legal-target lens: selection/position/turn/write/production events request; remove5s periodic target enumeration. Irreversible confirmation still revalidates in unchanged Gameplay logic. Timeout waits do not resend indefinitely; next real change/selection/turn permits recovery.

Retained0.2/0.25/0.5s UI callbacks only observe a selected object, scalar revisions, response tokens and local timeout; no periodic Gameplay requests or district/city scans. They support asynchronous response display/native selection changes. Hidden UnitSites returns before formatting/layout. P0Panel retains its width-equality anchor and on-demand bounded request; no-flight idle no longer increments a misleading busy_skip counter. Crew access no longer audits ordinary building/project completion because it depends on identity/anchor, not those outputs. Visible diagnostics and explicitly clicked detailed reads remain intentionally on-demand work. No UI names/artwork/presentation redesign.

## Local evidence

Run `DevelopmentTests/test_arch_v2_d2.py` (Lupa lua55). It executes actual current Lua and Git B075 code; native objects are deterministic mocks.

- Nine modules ×192 carrier-map comparisons =1,728 comparisons; normal cases also assert no module errors. Research/Culture/Industry/Commerce, active1–4, workers0/1/3, cities1/2/4/8; additional nonzero3-source/5-recipient Commerce actual-yield updates match B075.
- Copy/Industry each10,000 generic notifications: district/city/building scans0, sends0, writes0 after settling. Each of the nine consumers also receives4×10,000 idle pulses: fact/district reads and writes0.
- 30,000 actual shared Network queries: Capture0; direct ACTIVE change captures5 cities once/publishes once; temporary failure retains published state. A/B full output matrices additionally pass.
- CityPotential / UnitPanelActions / UnitTargetMarkers each10,000 ticks: new requests0; next turn and actual-write revision each request1. Hidden UnitSites10,000 ticks: UI operations0/requests0. GPP/Boost throwing transport10,000 notifications: max3 sends.
- Actual Great Work fixture scenarios: creation/move/era/classification/ACTIVE/adjacency carriers; unchanged formula. Existing healthy Dialogue UI code is unchanged.
- C2/C1/D1/A/B/B069 regression passes. Frozen tests are not edited: C2 wrapper explicitly supplies direct sample/governor change signals previously represented by generic pulses; only version stamps and those scheduling assumptions adapted. Lifecycle/output assertions retained. D1 scaling/39 outputs and B168 topology outputs retained.
- Whole Mod Lua syntax / manifest references pass; no SQL/Design changes, no game or deployment calls.

Measured district enumerations per batch (fixture one district/city; deterministic enumeration order):

| Module | 1 city old→new | 2 | 4 | 8 |
|---|---:|---:|---:|---:|
| Copy |2→1|8→2|32→4|128→8|
| Lv3 Effects |2→1|6→2|20→4|72→8|
| Industry Lv1 / Lv3 Support / Lv4 % / GPP / Crew |1→1|3→2|10→4|36→8|

Copy fact reads3C→C; othersC→C in this matrix. Copy Network queriesC→C, now verified-view reads without national capture; other indexed specialist modules0. Each explicit batch processesC cities / executes1 module Audit; already-verified batch sends0 requests. Cold producer/replacement still necessarily reads/validatesD districts in its own context. Complexity is O(C+D+relevant network edges), not a claim no topology can have O(C²) actual edges. Commerce source reads are once/source/batch. Real engine counts and native event order still need USER_GAME_TEST_REQUIRED (user game evidence).

## Boundaries and recommendation

No E, persistence/ownership,32-city,precision,balance,HD or runtime deployment changes. Standalone historical entrypoints retain old version assertions; use the D2 wrapper. No claim to fix55GB; native heap growth attribution remains UNKNOWN. Existing Lua audit FILE_API_UNAVAILABLE remains; use existing external monitor for memory trends if user elects to test.

After commit/push/clean: Architecture v2 Runtime Milestone Candidate. Suggested tag: `av2-runtime-b076.103` (not created). Recommend optionA: separately authorize temporary develop deployment, verify one ordinary save load + active/route/worker/building/GW/crew-preview updates and a next-turn fallback, then long-play external memory monitoring. No immediate test or deployment required this batch; do not auto-startE or promote main.

Protection check: main remains e3651f9 / clean. Live119 files match deployed8b2ca3a (B072.99) Git blob hashes exactly. D0025 SHA25681dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b unchanged.

## Interrupted-work recovery audit — 2026-09-15

Recovered the expected 30 modified and three untracked files on develop at 5dc6221; nothing restored/reset/discarded. Existing D2 implementation and test/report files were intact, with no unexplained non-D2 changes. Re-ran the D2 suite (including A/B/C1/D1/C2/B069) and both deployment safety suites; all passed. Deployment tests use temporary fixtures, not the live package.

Final review removed an out-of-scope `confirmedOnly` global reference from the manual Network diagnostic entrypoint and added an explicit refresh assertion. Corrected the v2 index's stale D2-pending sentence. No gameplay rules, Design, main or deployed files changed. No real-game validation claimed; commit/push records this recovered batch, not new scope.

## Subsequent user validation / milestone

See [2026-09-15 paired screenshots](../../Status/Validation/Results/Specialization_B076_Runtime_Milestone_20260915.md). Short idle expensive-work suppression passed; Memory stable at displayed precision. Tag `av2-runtime-b076.103` records this scoped milestone. Earlier no-deployment/candidate statements describe implementation completion, superseded by authorized temporary deployment and this evidence. Network/Discount pending with zero ACK remains unresolved; no full gameplay or55GB root-cause closure.
