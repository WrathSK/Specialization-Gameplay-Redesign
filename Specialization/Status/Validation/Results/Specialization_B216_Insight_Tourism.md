# B216 — City Insight Tourism

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Source/live B216.243; deployment verified below. The user accepted B215 and authorized the next proposed local Tourism slice. N3 and source reattachment remain separate.

## B215 acceptance and deferred evidence

USER_GAME_TEST_PASS (user-reported): B215 completed without anomalies, including the requested idle controls. No new screenshots were provided. The existing manual collector session `local/diagnostics/B205/session-20261017T044056Z-27156c/` corroborates READ/ARRIVED followed by DISPATCH/TRAVELLING and SPY_REQUEST submitted for the same unit; it does not record every native idle action or prove cold-load restoration. The session ended INTERRUPTED, with no diagnostic alerts. The user deliberately saved during travel; validate that save with B216 rather than add another standalone test. WORKS/PLACES remain deferred until eligible foreign targets exist, not accepted by analogy with PEOPLE. Prior B215 evidence is preserved unchanged.

## Accepted contract and bounded implementation

Culture D0049 `contracts.observations` remains authoritative: supported-owner Culture ACTIVE IV projects +2 percentage points of local city Tourism per effective Insight. History is city-owned, retained on ACTIVE decline/identity exit and follows the city. Current-owner civilization entries remain historical but do not count. No second permanent multiplier or new save schema is introduced.

`CultureInsightsTourism.lua` owns only derived native buildings, session reference/count records and bounded per-city errors. It reads `CityProgressionStore.ExpeditionInsights` and `CurrentSpecializationFacts`. One final carrier represents N effective records (1–192); zero creates none. The 192 bound is the existing Store serialization capacity (3 categories ×64 civilizations), not a new balance decision. Each carrier has one Modifier=2N, MinimumEra=Ancient. Unknown same-reference evidence preserves the last confirmed projection and reports UNKNOWN; new references and load cleanup cannot inherit it.

Confirmed mission history is written before the Gate notifies only its archive city. Existing investment/current-facts/Governor/owner-turn and Store return paths reconcile relevant scope; confirmed Store exit withdraws exact owned IDs. Load removes saved derived effects before rebuilding, including effects in unsupported-owner cities. Building notifications caused by the writer are suppressed locally; bounded pending scope handles re-entry. No new per-frame or AI-event polling. Ordinary unchanged reconciliation reads the one expected carrier without rewriting it; full192-ID sweeps are limited to initialization/new references, fault cleanup and confirmed exit. Player eligibility events still visit that supported player's cities. This is not a claim of measured native CPU/memory improvement.

The selected-city **文化见闻** report is read-only and appends configured/UNKNOWN Tourism status to the existing collector prefix. It does not refresh gameplay merely because the panel opens. Three localization keys were added: `LOC_SPC_INSIGHT_TOURISM_NAME`, `LOC_SPC_INSIGHT_TOURISM_CURRENT`, `LOC_SPC_INSIGHT_TOURISM_UNKNOWN` (Chinese and English).

No changes to training/capacity/source binding, task duration/targets, persistent Store, Design, other Mods, GC, collector startup or game configuration.

## Native precedent and remaining risk

[B215 static investigation](Specialization_B215_Expedition_Idle_Actions.md#theater-building-tourism-investigation--static-evidence-only) establishes Film Studio's `MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS` → COLLECTION_OWNER / EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS. Installed HD uses Modifier50 / MinimumEraAncient. B216 reuses that primitive with the accepted 2N amount; it neither changes the Film Studio nor assumes several percentage carriers stack.

This is outgoing city Tourism **pressure**, not guaranteed to change the displayed base Tourism. All-source coverage, target modifiers, fractional settlement and interaction with other bonuses remain native questions. Static native UI references: `CIV_ASSETS/Base/Assets/UI/PartialScreens/WorldRankings.lua` uses `GetTouristsFromTooltip(targetPlayer)` for culture-victory destination details; `UI/WorldView/TourismBannerManager.lua` uses `GetTourismTooltipAt(plot)` and `GetTourismAt(plot)` for source tooltips. These UI-only observations are not treated as a Gameplay API or as proof that the tooltip exposes this multiplier.

## Local validation

123 tests PASS: actual projection module/model + in-memory loaded-DB SQL, existing Insight report, mission validation, actual Gate/task and idle-action suites. Added20 tests cover exact final-value replacement/zero, ACTIVE/identity transitions without deleting history, current-owner filtering, load/foreign cleanup, UNKNOWN versus zero/new reference, failed create/remove recovery, missing/pillaged carrier, confirmed versus unconfirmed exit/return, record/error pruning, read-only report, existing192 bound, metadata rejection, and actual Gate completion/cancellation notification scope. Native DB was read-only and copied into memory; test-only Make_Hash callback supplies its existing trigger dependency. No gameplay full regression, stress, game launch or new user result is claimed.

Context/schema/hash/selector and helper self-test PASS;371 changed-document links/anchors checked with no errors; complete package inventory221 files. Staged publication check is required before commit. No frozen hashes or accepted Design refreshed.

## One combined native session

1. Start the collector manually. Load the user's travelling save. Let the team arrive; confirm original archive city/source binding and that the ordinary mission buttons work. This covers the deliberately deferred travel-save check, not a new generic save/load campaign.
2. Select the archive Culture ACTIVE IV city and open **文化见闻**. Record effective N and configured +2N%; existing records should apply automatically without opening a separate probe. Capture one source Tourism tooltip (works plus another source if available) and one chosen foreign civilization's culture-victory Tourism tooltip as the before evidence. Do not expect national/base Tourism to rise by2N%.
3. Complete one still-unused **风土考察** for that archive city. Reopen **文化见闻**: N→N+1, configured percentage→2(N+1), with one final carrier. Keep works/buildings/policies/target relationship conditions unchanged where practical; note changes rather than repeat a long run. Capture the same native tooltips after completion/refresh. Carrier configuration alone is not native settlement PASS. If the UI does not expose a usable pressure amount, report that single limitation; do not ask the user to accumulate dozens of Insights or infer success from unchanged base Tourism.
4. WORKS/PLACES may be tested opportunistically if valid targets exist; otherwise carry their native evidence forward. No extra cold restart is required. ACTIVE withdrawal and reconstruction have targeted local coverage; any observed anomaly determines the next narrow native check rather than a blanket lifecycle campaign.

## Deployment

B216.243/modinfo243 DEVELOP_ACTIVE; source 3aff99b6305e32ca594179ce3db9d8bce8024a14; receipt B216.243-3aff99b-playtest.json;221/221 MATCH. Fresh automatic OS exit checks before both guarded switches; B215/stable recovery retained, no pending transaction. Configuration unchanged.

Source/runtime digest: `d6434d3603013ed97ad13df3ca3f938f7fbce8320b415ce64729475b92f2aab5`. Staged publication check PASS. No native test or game launch performed.
