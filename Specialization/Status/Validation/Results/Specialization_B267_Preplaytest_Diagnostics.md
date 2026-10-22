# B267 — bounded pre-playtest diagnostics and experimental-project gate

Date: 2026-10-21
Status: DEPLOYED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
Basis: B266.293 / `0c2c4ae`; documentation HEAD `31f785a`; D0057 / A0177.

The user authorizes Primary to implement PRE-01 through PRE-05, choosing engineering details and stopping only for genuine gameplay decisions. Scope follows the [approved roadmap](../../../Reports/Proposals/Audit_Followup_Priorities.md#explicit-pre-playtest-implementation-list). No PR, main promotion, artwork application or release designation.

## Implementation plan

- PRE-01: separate meaningful scalar logging from bounded native sampling; change-only repeated states with identity-aware deduplication; explicit per-role/per-turn runaway marker; paired ring/reader limits and collector metadata/loss alerts. Preserve safe scalar filtering and read-only collection.
- PRE-02: observe initialization early, seal at the end of Gameplay startup, sample after load listeners finish and at first publish/local turn. Expose Store fresh readiness read-only; report retired controls separately. No startup repair.
- PRE-03: observe Commerce turn boundaries and network transitions/sender state. No yield, sender, topology or UNKNOWN policy changes.
- PRE-04: observe only the existing 35 ResearchSupport/Lv2GPP carriers; protect diagnostic callbacks, track changed health and native pillage notifications. No repair or immunity.
- PRE-05: retain the experimental overflow definition and startup dependency; gate ordinary production availability with an inaccessible requirement after source/schema checks.

## Validation / exit

Run actual-Lua diagnostic/readiness/carrier/network/Commerce counterexamples, Python collector/reader offline tests and the scoped existing affected regressions. Check package closure, Lua 5.1 syntax, XML/SQL and context integrity. Native load delivery, treasury accrual and pillage behavior remain USER_GAME_TEST_REQUIRED in the integrated playtest. Local simulation is not native PASS.

## Implemented result

B267.294 / modinfo294 implements PRE-01–05. No gameplay decision was required. Data gating was selected for PRE-05: retain the million-cost prototype and all existing readers, add one never-granted InternalOnly requirement building, and leave ordinary availability blocked. No artwork, main, PR or release tag changes.

- TRAIN ring: 256 entries; independent optional native sampling: 96 per producer; meaningful-output breaker: 512 per role per game turn with explicit throttle evidence. High-volume state deduplication is bounded to 4,096 identity entries. Temporal requests and receipts are not deduplicated. Alternate UI.DataError output keeps its separate 128-call guard; stdout collection remains the primary channel.
- Reader limits: 256 entries / 262 snapshot rows / 2 MiB; passive 8,192 TRAIN rows / 16 MiB / 16,384 frames per window. META, ring-overwrite and capture-error gaps are retained; these bounds are not a lossless-disconnection promise.
- Readiness reports Store and live-writer initialization gates, records early load timing and startup seal, and defers values until publish. Legacy cleanup and control modules are separate. The fixed 35-carrier observer retains UNKNOWN and distinguishes a missing-load first-turn baseline; it never rebuilds carriers.
- Commerce observations run on existing turn-end/start events, reading publications/carriers without Audit/Refresh. Network drops/rejections include safe packet coordinates; sender diagnostic fields do not add operations or retries. These are base-carrier observations, not proof of native net Gold settlement.

## Validation results

`test_b267_regression.py`: **243 tests PASS**, including 38 new B267 counterexamples and affected current network, Commerce, diagnostic, reader/collector and Store regressions. Tests use actual Lua modules and offline transport doubles; the project gate also executes against an in-memory copy of the explicitly configured, read-only engine database. Python syntax, all 187 Lua files (Lua 5.1), XML and package/context integrity are checked locally.

The runner records 12 explicit exclusions without changing frozen tests: eight superseded budget/buffer assertions have B267 replacements; four historical model/schema/UI fixture cases are not current delta gates. Earlier baseline probes reproduce the old B241 model/CAPITAL_MONEY_UNCONFIRMED, institutionTurns-schema and native UI InstanceManager mismatches. The unchanged UI fixtures are outside this diagnostics/data delta. No unrelated runtime behavior is repaired to satisfy historical fixtures.

A local regression caught fallback logger reentry after temporal deduplication was removed; the sink now suppresses diagnostic callbacks during its own native emission. The original reentry regression and a new B267 counterexample pass. Diagnostics-off comparisons preserve Commerce writes and published results.

## Native boundary / delivery

New-game/load trace delivery and readiness ordering, native Treasury accrual around turn boundaries, actual hidden-carrier pillage/repair behavior, and ordinary-list hiding of the experimental project remain USER_GAME_TEST_REQUIRED. Verify evidence delivery at the start of the integrated campaign; use collector `--idle-exit 300` through reloads. No new dedicated acceptance campaign is required and no native PASS is inferred.

User decision: none for PRE-01–05; first integrated-test baseline designation remains separate. User testing: the native observations above, alongside the existing REALLOCATING cold-load and additive-output checks. Primary next: guarded W0003 deployment after clean-source and game-exit checks; no PR or main promotion.


## Source publication and deferred activation

Implementation source `5b421e8aec064e4b435e903ac82a2fd85aef39e8` is committed and pushed to develop. The 23-file staged publication gate passed; local artwork and raw evidence remain ignored. No PR, main promotion or release tag.

The guarded activation command was rejected by automatic approval review before process creation. The reviewer requires explicit approval for this B267 activation and did not accept the recorded W0003 standing authorization as sufficient. Primary did not bypass the rejection. Read-only revalidation confirms B266.293 remains unchanged and DEVELOP_ACTIVE under its original receipt; no B267 receipt or pending transaction marker exists. B267 source package: 290 files, digest `af5ef23f6c1f9a368ec8b2e381e982dd05d01fb503736369d8aed65b5662ea01`.

User decision: approve this exact B267.294 activation. User testing: after activation, use the first integrated session's diagnostic/native checks. Primary next: on approval, repeat game-exit/source/live/recovery checks and execute the existing receipt-bound deployment tool. PRE-01–05 implementation itself is complete.


## Approved activation — 2026-10-21

The user explicitly approved this B267.294 deployment and asked whether integrated testing may start. Fresh process checks confirmed the game exited before each transaction step. Exact B266 receipt restoration and B267 activation completed using the existing tool, with no game launch between steps. Receipt: `B267.294-f385c48-playtest.json`; deployed source commit `f385c48eb86ffde66f15029b9c16fdfa2c3d5fed`; 290/290 source/live files MATCH; digest `af5ef23f6c1f9a368ec8b2e381e982dd05d01fb503736369d8aed65b5662ea01`. Stable and outgoing B266 recovery packages also MATCH, with no pending marker. Main/configuration/artwork remain unchanged; no PR or release tag.

B267 is available for the first integrated campaign. Read-only inspection confirms EnableTuner=1; game launch and native acceptance remain the user's work. Start the collector with `--idle-exit 300` before launching/loading, confirm records arrive, and begin a new Standard-speed game with the dedicated America/Roosevelt test identity and the previously agreed scope/precautions. Native diagnostics, REALLOCATING cold-load and Standardization + Development combination checks remain open until observed.

User decision: none required to begin the agreed tests. User testing: first integrated campaign and evidence delivery. Primary next: await the user's logs/observations; no further repair, deployment, PR or promotion is dispatched by this record.
