# B215 — Expedition idle actions and Tourism preparation

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Source B215.242; runtime remains B214.241 until the guarded deployment record below.

## Approved implementation

Only the exact owned Expedition's idle action list changes. CREATED, ARRIVED and released TASK_COMPLETE use existing native rows/icons/localization for **跳过回合 / 休眠**, and native **唤醒** when eligible. The native/HD base click handler retains its turn-processing/interface checks; the general Spy action builder remains bypassed because it registers espionage hotkeys. Clicks recheck exact selection/owner, current published phase/lock and native permission. Missing/throwing/unreadable permission does not authorize a request.

PREPARING/RUNNING/recovery/release locks still return no actions. Previously captured idle callbacks cannot wake task-owned sleep. Manual idle sleep stays native-owned and does not acquire/write a task lease; the existing activity bridge already distinguishes pre-existing sleep and does not wake it during cleanup. No new state, save fields, scans, subscriptions or localizations. Ordinary units retain their existing builder/callback. Capacity, binding, training, mission target/timer/reward and GC remain unchanged.

Direct implementation: `Mod/UI/ExpeditionSpyUnitPanel.lua`; package labels in Probe/modinfo. Native references inspected read-only: `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua` operation construction669–713 and click2493–2541; installed HD `UI/Replacement/DL_UnitPanel.lua` command/operation construction and click998–1012. Paths are source labels, not commands. Loaded DB confirms SLEEP/SKIP are zero-turn operations without InterfaceMode; WAKE is a command without InterfaceMode. Existing native action rendering supplies icon backing.

## Local verification

90 tests PASS across new `test_expedition_idle_actions` and existing actions UI, task and activity UI suites;31 actual Gate/package/database tests PASS separately. The8 new methods cover idle skip/sleep/wake, native signatures, denied/unknown readers, current/stale lock, selection/owner/mirror change, native turn gate, unknown/travel phases, ordinary-unit delegation and task-owned sleep isolation. Fixtures do not establish native visibility, timing or rendered layout.

## Theater-building Tourism investigation — static evidence only

The user suggested a Theater building precedent. The loaded configured read-only gameplay DB and installed HD source establish:

| Source | Modifier / arguments | Boundary |
|---|---|---|
| Film Studio (`BUILDING_FILM_STUDIO`) | `FILMSTUDIO_ENHANCEDLATETOURISM`: `MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS`; MinimumEra=ERA_ANCIENT, Modifier=50 | A city Tourism-pressure candidate, not a GreatWorkObjectType-filtered effect |
| Dynamic modifier mapping | COLLECTION_OWNER → EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS | Engine effect, not Lua reward code |
| Native Buildings.xml699,1217–1225 and native Buildings_Text.xml | Native modifier100 / ERA_MODERN; text describes Tourism pressure from this city towards other civilizations in the Modern era | Destination-era/pressure semantics must be retained in interpretation |
| HD `UpdateDataBase/DL_Buildings.sql:369–371` | Explicitly changes MinimumEra to Ancient and Modifier to50 | Confirms loaded overrides, not an independent native acceptance test |
| Amphitheater / broadcast / cinema-type works effects | MODIFIER_SINGLE_CITY_ADJUST_TOURISM with GreatWorkObjectType and ScalingFactor | Work-type filters; not evidence of whole-city coverage |
| Grand Hotel | Improvement Tourism +50 and district adjacency Tourism | Also not universal city Tourism |

All direct Theater-building modifier bindings were checked; no attach-modifier indirection was present in this loaded set. This is stronger than guessing that omitting a Great Work filter yields a universal effect. It does not yet prove all-source coverage, percentage stacking, fractional settlement or city-panel display. No changes to HD, SQL or any Tourism writer were made.

### Recommended next Tourism slice (requires approval)

Investigate/implement the accepted local `+2 percentage points × effective Insights` using the Film Studio engine effect with MinimumEra=Ancient as the leading candidate, after confirming eligibility for the supported ruleset. Use the existing city history and current ACTIVE facts; derived effect state remains replaceable. Do not add a second permanent bonus ledger or world scan. Revalidate/withdraw on the existing relevant history, ACTIVE and owner/load boundaries. Review direct native carrier ownership/cleanup consumers before choosing an exact representation; do not assume multiple percentage carriers sum.

The minimal new native gate should separate city-source Tourism pressure from the displayed base Tourism. Use two identifiable source types if feasible, compare the same target civilization/turn conditions before and after the candidate and on removal; other-city output/target multipliers must be controlled or recorded. An explicit larger diagnostic magnitude may be proposed if +2% is unreadable, but is not implemented or pre-authorized here. If the candidate cannot represent accepted whole-city semantics, report the technical gap rather than silently narrowing it to works. N3 remains separate.

## Minimal B215 user check

With the manually started collector and an idle team, click **跳过回合**, then **休眠** when native eligibility permits; confirm **唤醒** is available and restores ordinary idle control. Confirm the existing dispatch/task buttons remain usable after waking, and a running mission still hides idle actions. One continuous session; no repeated training or cold-load campaign. Use a screenshot only for visible layout/availability problems: existing Gate logs do not capture every native idle button click, so an oral confirmation is sufficient for successful idle behavior. WORKS/PLACES remain deferred to future available targets, not a gate for B215. No new automatic collector startup.

## Deployment

Pending verified game exit and the existing guarded transaction. No game launch or native PASS.
