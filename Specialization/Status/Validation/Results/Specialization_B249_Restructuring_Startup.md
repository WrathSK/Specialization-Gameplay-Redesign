# B249 — Event-driven Restructuring startup

Evidence: B248 USER_GAME_TEST_FAIL; B249 STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.
Reviewed baseline: develop `1710c7e`, live B248.275 from `cbb9ce2`. New source: B249.276 / modinfo276. User explicitly authorizes this startup repair, targeted regression and guarded deployment; no Design change.

## B248 failure evidence and cause

The user reports the missing **重组团队** entry in a newly created game as well as after loading. Two existing ignored collector sessions contain eight distinct training-list observations: three at T45–46 and five in the new T1–3 context. All report the service present but `ready=false`, access marker absent, native visibility/eligibility false, and native cost500. Unit/marker definitions are available. The new context's trace begins before the UI load-close observation; no restructuring load/access observation appears in the captured windows. This identifies the unentered service readiness path, not a missing model or a cost/population defect. It does not establish that every Gameplay context lacks the native event.

Original logs are unchanged under `local/diagnostics/B205/` and remain excluded from Git:

| Session | records.log bytes | SHA256 |
|---|---:|---|
| session-20261019T054049Z-4515f6 | 37437 | dad5da5992796737b3c752e40f30f76bc6248caf71fb87e01dbf9ac0436c6a0b |
| session-20261019T055043Z-e1de87 | 22873 | 2b523fbe54232699b3019edcce8951330a86bcf9a6735dbaefda9e711483edaf |

Source review confirms that only the Restructuring `LoadScreenClose` callback could set `ready=true`; all other notifications merely called a Flush that returned while unready. The unchanged actual Store/service fixture reproduces permanent unready state when that notification is absent, precedes subscription, or the event is unavailable, despite confirmed Commerce ACTIVE IV and later investment/publication/turn events. B248 repaired a separate genuine same-turn notification omission; it did not repair this startup prerequisite.

The old service fixture explicitly fires LoadScreenClose after Start. That assumption concealed the native delivery gap. Five new regression methods were first run against unchanged B248 code and failed at the intended assertions (six cases including both birth/completion orders). Repeated load notifications also discarded live confirmation previews and unmatched training-event pairs; this is a LOCAL_SIMULATION finding, not an independently reported native failure.

## Minimal repair and state ownership

- One idempotent, module-local initializer checks the existing Store's FRESH/EXISTING status, EffectiveFacts reader, marker definitions and supported-player city collection. WAITING, HELD and unreadable dependencies leave readiness false and preserve dirty work. The service attempts initialization at normal Start and through existing publication, player/Governor, committed-city and optional load notifications. No P0 dependency, wall-clock timer, frame update or polling callback.
- Initial recovery is limited to a snapshot of supported, Store-owned current city references. Failed city recovery retains that reference for its next relevant event; it does not prevent another city's access. Success, mismatched/missing reference, confirmed exit or Gameplay-context disposal removes the obligation. No native city object or permanent cache is retained. This bounded session work is not a new save authority.
- Once ready, duplicate load notifications refresh current projections without resetting births, completions, previews or views. Ordinary native event pairing/turn expiry remains unchanged. The Store still owns all transaction receipts; no new field, capacity, binding or history semantics.
- Recovery retains the original distinction between confirmed native consumption and an intent without a consumption receipt. Only the confirmed receipt can finalize configuration; recovery never repeats unit destruction or infers success from absence.
- `REST_INIT_WAIT`, `REST_INIT_HELD` and `REST_INIT_READY` use the existing bounded scalar log. One replaceable stage/reason stamp suppresses repeated waiting messages. Existing access/list/transaction evidence remains available; no collector or diagnostic budget changes.

Runtime changes are limited to `Mod/Restructuring.lua` and the two version stamps. Unit SQL, UI/model/art, fixed500 cost, no population debit, no hard team cap, source binding, five-full-turn rule, profession histories, signed investments, Store, GC and other modules are unchanged.

## Local verification

**80 selected unittest methods PASS**: 22 new startup/recovery/package methods, 38 retained B247 Store/service/contract methods, 11 B248 access/read-only observation methods, five retained UI methods and four retained syntax/art/no-polling checks. Parameterized birth/completion order is additional coverage, not an inflated method count.

Coverage includes missing/early/unavailable load notification, WAITING/HELD/unknown Store state, missing facts/definitions, deferred city work, publication and player-event startup, empty initial city collection, wrong owner/inactive access, duplicate notifications, previews and birth/completion pairing, reentrant native-marker events, REALLOCATING restoration, confirmed-consumption recovery and unconfirmed-consumption holds. Existing same-turn investment, exact debit/consumption, source-versus-target loss, unrelated-city/history/contract behavior and UI read-only boundaries remain checked.

The one B248 pre-load assertion is updated to the approved **pre-Store-readiness** boundary, preserving wrong-owner/no-premature-read checks. Historical package tests pinned to modinfo274/275 are not relabeled as current PASS; the new test validates276, exact unique registration and the allowed runtime delta. Lua5.1 parsing passes. Actual source comparison confirms unchanged unit SQL, other runtime implementation and art. No native CPU/memory, real training, save-file or completed restructuring PASS is inferred.

## Minimal combined native flow

Run the existing collector normally; no P0 startup action is required. Use the standard-speed test scenario with a Commerce ACTIVE IV city.

1. Immediately after loading, open that city's ordinary production list. **重组团队** should appear with base500 Production. This tests the repaired startup delivery gap. If still absent, stop there and retain the log; do not wait turns or start another campaign to compensate.
2. If present, train one team and continue the still-unaccepted B247 flow: target a city with Potential>=2 and two completed, unpillaged eligible professional districts. At its current professional district, click **资产清算** → **确认资产清算**. Check one Potential loss and the restructuring state.
3. Save while restructuring, fully exit/restart and load once. Check the same team/target, retained Potential and continuing disruption. This covers the new transaction recovery route, not repeated Probe lifecycle testing.
4. After five full turns from liquidation, move the same team to the other eligible district in that city. Click **资产配置** → **确认资产配置**. Expect the new profession, retained P−1, normal ACTIVE calculation, disruption removed and one team consumed.

The transaction steps complete the existing B247 gate; they are not a new transfer/whole-profession matrix. Use logs, with screenshots only for a visible discrepancy. Held Culture features and unrelated audit work remain on hold.

## Deployment

W0003 deployment completed from clean/pushed `ad34b1fe88559e35cdf6b153d6838391556e223e`. Fresh automatic OS checks verified game exit immediately before both exact-receipt B248 restore and B249 activation. Receipt `B249.276-ad34b1f-playtest.json` records DEVELOP_ACTIVE.265/265 source/runtime files MATCH, digest `89eb1e79d7947ae9b3316dd38c4f6a3e9e23bb7adac80d8843dd65d606b4df00`. Stable and outgoing B248 recovery packages are verified; no pending marker. Main/stable B069.96, configuration and GC are unchanged; no game launch. Native entry and transaction acceptance remain pending.

User decision: none. User testing: the single entry-first combined flow above. Primary next: wait for the scoped native evidence; no subsequent batch is authorized automatically.
