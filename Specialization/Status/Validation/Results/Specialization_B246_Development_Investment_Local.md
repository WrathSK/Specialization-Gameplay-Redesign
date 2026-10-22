# B246 — Development Investment local implementation

Date: 2026-10-18

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

Source checkpoint: B246.273 / modinfo273; based on develop `fc8bcd5`, B245 runtime `006bf9c`.

Deployment: verified B246.273 from `6398be1`;260/260 source/live MATCH. No native B246 result is claimed here.

## Approved scope and decision

The user authorizes Development Investment, the existing <=0.01 Gold per-native-debit allowance, targeted local validation and guarded deployment, without timers or another Commerce batch. During implementation the loaded HD catalogue disproved the old same-tier-equal-cost assumption. The user explicitly chose the lowest theoretical purchase price among eligible next-tier alternatives, with the reference building and price shown in the UI. [D0057](../../../Design/Content/Commerce_D0057.json) records that decision; the contract remains city+district, never the quotation building. Frozen D0056 Content/Spec and old evidence are preserved.

The15% fractional quote, +50% selected-district building Production, working-specialist source slots, one active contract per target, next-eligible-building completion and source/target ownership termination follow accepted rules. ACTIVE/Identity/route/worker loss after signing does not cancel the investment. No refund, fixed duration, direct purchase/unlock, Industry-template prerequisite or Restructuring is added.

## Source evidence and implementation boundary

- Native source, read-only: `CIV6_ASSETS/Base/Assets/UI/Panels/ProductionPanel.lua`, the installed Civ VI macOS UI context. `GetPurchaseCost` is used at line1770, collection `IsComplete` at2002, `CanProduce(hash,false,true)` at2038. Here `CIV6_ASSETS` denotes the installed game Assets directory, resolved locally; no personal installation path is published. These call signatures do not prove every forbidden-purchase building returns a price.
- Loaded HD `DebugGameplay.sqlite`, read-only snapshot via `SPC_DEBUG_GAMEPLAY_DB`: `Buildings`, `HD_BuildingTiers`, `HD_DUMMY_BUILDINGS`, `DistrictReplaces`, `Modifiers` and `ModifierArguments`. HD Theater alternatives include Art Museum220P, Archaeological Museum180P and Opera450P at tier3; Neighborhood also has different same-tier costs. These are catalogue facts, not theoretical Gold quotes or a new conversion rule. Normal construction eligibility and minimum constructible tier, not array order, determine candidates.
- The UI reader calls `city:GetGold():GetPurchaseCost(YIELD_GOLD, buildingHash)` without `CanPurchase`. Every eligible same-tier price must be positive/readable to prove the minimum. Otherwise that district's quote is held and explained; no Production-derived fallback or hidden permission change.
- `DevelopmentInvestmentModel/Catalog`, the Gameplay service, UI reader/panel/project adapter and two SQL files implement this separate contract. `CityProgressionStore` gains only optional model-encoded Development records and direct accessors; `NetworkBridge` adds an outgoing projection of its existing verified input. `Commerce` publishes source invalidation and `Gameplay/CrewProjectOrder/modinfo` wire the entry. Capital calculation, transfer primitives, generic Store equality/reservations, GC and other module ownership remain unchanged.
- Native effect family is `MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION` with `DistrictType` and `Amount=50`; only owned Development carriers are changed. No direct Gold/Faith price modifier, district/Wonder acceleration or new purchase permission is inserted. Additivity with Standardization is the accepted target, pending the combined native check.

## Persistence, failure and event lifecycle

Store is the authority for locked contract terms and observed debit receipt. Version1 DECIMAL17_V1 preserves fractional amounts through the same Property conversion already observed in B243. The latest record per target history token bounds retention by city relationships, not signed-action count. Native balances/current building facts and temporary quotation choices are not second mutable authorities.

Confirmation revalidates the selected quote and prior state, reserves the target, saves DEBIT_INTENT and DEBIT_CALLING, invokes one native transfer, verifies direction and <=0.01 error, saves ACTIVE actual receipt and applies the effect. Exact saved-value comparisons are unchanged. Unknown native result, failed write/readback or effect application never triggers a second debit, compensation or guessed success. Fresh load closes a provably unused intent, holds an unresolved call, and rebuilds ACTIVE effects from saved contracts. Session reservations protect uncertain occupancy without new global persistence or reverse indexing.

New eligible building presence ends the contract even if it is not the quote building, or was completed by purchase/Cheat. Existing/pillaged building repair does not. Source/target confirmed ownership change withdraws and terminates; later invalidation/destruction/extinction is not silently given new Gameplay semantics. Unknown references hold the affected operation.

Existing building/transfer/load/player-turn/publication events drive updates; no timer, frame callback or new GC. Normal publish consumes dirty source state without fetching prices; explicit open/refresh/confirm reads native candidates. Confirmation reads only its selected target before payment. Building events reconcile relevant outstanding records; turn fallback checks outstanding contracts, not all buildings in the empire. Owned carriers are compare-before-write. UI selected row/request latch is local and cleared on close/load/owner change; quotes replace previous snapshots and invalidate on relevant input changes. Logs reuse the96-entry bounded diagnostics and existing collector without modification.

## Local verification

137 selected unittest methods PASS: **57 new B246 +80 retained direct regressions**. No historical assertion was weakened.

| Coverage | Result / evidence boundary |
|---|---|
| Actual native-shaped quote reader | Minimum same-tier price; lower tier selection; direct-purchase-disabled candidate; missing/zero/negative/throwing price held; current constructibility independent of current queue |
| Actual Store and service | Fresh-worker count; outgoing vs reverse/transitive/unknown route; stale quote; source/target/reference guards; same-domain multiple targets and cross-source target exclusivity |
| Monetary transaction | Fractional and quantized <=0.01 receipt; exact codec through Property conversion; insufficient balance; duplicate click/reentry; intent/calling/receipt failures; before/after-call exceptions and over-bound result; no replay/compensation |
| Completion and continuation | Alternate eligible building, purchase-shaped completion, building completion during debit, duplicate event, repair and unrelated-domain non-completion; route/ACTIVE/Identity/capacity loss continues; source/target owner change exits; unknown reference holds |
| Reconstruction | Fresh independent Lua VM with saved Properties rebuilds the signed contract/effect; closed contracts stay closed; unresolved call holds; corrupt known history is not empty |
| UI and SQL | One open snapshot, local selection, scalar-only confirmation/double-click latch, stale refresh, route-loss contract visibility, owner/close/subscription exit; actual loaded-HD SQL, exact carrier arguments, no completion reward; package/Text IDs |
| Work and isolation | Tested idle30 publications cause no new native quote/effect writes; B246 ordinary writes trigger0 cross-record uniqueness checks; other carriers preserved. Capital baseline remains14 reads/7 writes/2 monetary calls/0 uniqueness visits with identical values |
| Retained regressions | B241 Capital model/service, Capital UI/network; B245 receipt/failure/collector/value-work comparisons; B240 source filtering/Food/current eligibility |

New suites: `DevelopmentTests/test_b246_development.py` and `test_b246_development_ui.py`. Existing B241 UI Package build pins and B245's historical whole-Store-unchanged assertion are not applicable to an explicitly extended Store/package; they were not changed. Their relevant behavioral tests are included. All changed/new Lua sources compile under Lua5.1; XML/package metadata is checked. Context check passes for260 runtime files and815 guarded entries.33 added/current local links and anchors, XML/package metadata and the exact D0057 semantic delta pass review; frozen D0056 Spec is byte-identical to its previous accepted source. Staged publication is checked before commit. Local doubles and SQL shape do not prove native price availability, actual Production, CPU or memory improvements.

## One combined native flow

Keep the existing manual log collector running. Reuse a Standard-speed save with Commerce ACTIVE IV, at least one working Commercial Hub specialist, enough Gold and a direct outgoing domestic trade route to an owned target. Choose a target with a current constructible next-tier building and, if convenient, an already verified Standardization template. No special new city setup is required beyond those inputs.

1. In the Commerce city's production list open **发展投资**. Choose target city+district. Check the named quote building, theoretical Gold price and15% fee; press **确认发展投资** once. The contract becomes **执行中** and uses one slot. Native actual debit is captured in the existing log. If a quote is unavailable, stop that choice and supply the log rather than forcing a formula.
2. In the target, compare the selected district building's Production bonus before/after signing: the increase should be50 percentage points, additive with existing Standardization (e.g. baseline10% becomes60%, before other bonuses). An unrelated building should not acquire this bonus. Prefer the native bonus breakdown or a simple one-turn comparison; turn rounding is not a new balancing task. One screenshot is only needed if the native breakdown cannot be captured or disagrees.
3. Before the building completes, save once, fully quit and reload. Confirm the same contract is still **执行中**, the effect remains and there is no second payment. This step tests this batch's new persistent contract/occupancy, not the old Probe harness. Finish the eligible building naturally or by the existing Cheat workflow; the contract becomes **已完成**, only Development's50% disappears and the source slot is released. Inherit B245's Capital settlement test; do not repeat it.

Pass/fail distinctions: step1 proves the new native theoretical-price/actual-debit path; step2 proves the district-restricted primitive and additive integration; step3 proves new Development persistence and building completion exit. No conquest marathon, repeated default-OFF/re-enable sequence or full old lifecycle retest is requested.

## Stop boundary

User decision: minimum eligible theoretical price accepted and recorded; no remaining decision needed for this batch. Native unavailable prices must be reported, never approximated. User testing: the one flow above remains pending. Primary next: source commit/push and guarded B246.273 deployment are complete; await the one native flow, then review its evidence. Main B069.96, original evidence, configuration, other Mods and game launch remain outside scope.

## Verified deployment checkpoint

Clean/pushed source `6398be1030651157156679f99de709f6a6f873c6` passed automatic game-exit checks before both receipt-bound B245 restoration and B246 activation. Source/live260/260 files MATCH, modinfo273, digest `62d72cfdb6c3986de9c6e7199967dae2106d3d96ef60a777598236a8cf36d020`. Receipt `B246.273-6398be1-playtest.json` is DEVELOP_ACTIVE; stable/outgoing recovery retained, no pending transaction. Context, diff/links and staged publication checks pass. Main remains `e901a22`/B069.96, configuration/other Mods unchanged, no game launch. Only deployment documentation/metadata follow this source checkpoint; no new runtime change or native PASS. Stop for the combined flow above.
