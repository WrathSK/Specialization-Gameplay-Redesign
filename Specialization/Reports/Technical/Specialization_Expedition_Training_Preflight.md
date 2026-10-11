# Expedition normal training — implementation preflight

Date: 2026-10-11. User approved the normal-training/source-registration slice following B201. This checkpoint records a bounded technical dependency; it does not withdraw that approval, enable training, or establish native impossibility. No B202 build or deployment has been produced.

## Explicit cost clarification

User selected: **Use the same formula, counting Expeditions separately**. Ordinary Spy production history must not increase Expedition cost. Use the loaded Spy base cost/progression model/parameter for the Expedition unit type, letting its own production history drive progression. Do not hardcode the observed HD80/10 values. This clarification must be synchronized into the formal cost contract before shipping the implementation; existing frozen acceptance hashes must not be silently rewritten.

## Confirmed source facts

- Current `Mod/Data/ExpeditionSpyGate.sql`: `CanTrain=0`, placeholder `Cost=1`, separate Spy=1 unit type, no ordinary Spy definition changes.
- Current Gate CREATE checks Culture ACTIVE IV and binding token, saves CREATING reservation before `UnitManager.InitUnit`, gets the returned exact unit object/ID, then saves NAMING. This writer-owned source→unit link is why the P0 creation path is reliable. Normal native training must not reuse CREATE by spawning a second unit.
- Read-only current primary DebugGameplay.sqlite: UNIT_SPY Cost80; `COST_PROGRESSION_PREVIOUS_COPIES`, parameter10; no PurchaseYield. Database values are observed inputs, not new accepted constants.
- Loaded HD `Gameplay/Buildings.lua:MinistryOfNationalDefenseProduction` and `Gameplay/CivilizationTraits.lua:SumeriaProduceUnit`: `CityProductionCompleted(playerId,cityId,type,objectId,cancelled)` uses objectId as a GameInfo.Units row, not an instance ID.
- Existing repo production listeners consume city/project facts; none of the directly inspected Expedition/Crew paths supplies a tested native-training instance receipt.
- `Unit_BuildingPrereqs` has Unit/PrereqBuilding/NumSupported; Archaeologist uses Museum/1. That alone does not prove a global cap across several eligible Culture cities or queued work.
- Native `UnitFlagManager.lua` uses UI `GetArchaeologyHomeCity()` for archaeology display. Its applicability to our Spy-type unit has not been established. Do not enable artifact behavior merely to obtain a home-city value.

## Evidence-driven implementation boundary

A created-unit event provides instance identity but not a training-city receipt; the inspected production-completed handler supplies the city/type but not the instance. A unique matching unit near the city is not sufficient by itself. Two independently observed events require an owned, bounded correlation contract, not an assumed ordering.

Potential safe route still to establish: reserve the exact source/queue transaction before native training; correlate its confirmed native completion with a newly observed exact Expedition instance; reject pre-existing, unrelated, cancelled, multiple or unknown candidates. Retire bounded pending evidence on success/cancellation/hold; never adopt after load using proximity/name alone. Determine whether existing native queue prerequisites plus a narrow UI admission adapter can enforce cap1 without creating, deleting or refunding extra units.

This is **TECHNICAL_PROVENANCE_AND_QUEUE_BOUNDARY**, not proof that normal training is impossible. The public reference and inspected examples do not close the native event-order/instance-link question. A fail-closed implementation can be modeled locally, but its causal evidence must be made explicit before those tests could mean anything. Do not write a fake `CityCanTrain` mock and call it a supported Civ VI hook: search results for that name commonly describe Civ V.

## Exact continuation

1. Reuse `Mod/UI/CrewProjectOrder.lua` and its HD `DL_ProductionPanel` adapter pattern to inspect the unit admission/queue callbacks; do not replace the entire production UI.
2. Establish pre-training reservation and cancellation semantics against the actual queue surface, with only exact affected source/player queries. Existing Gate/Store reservation remains the one capacity authority.
3. Resolve native completed-city→new-unit evidence with a bounded receipt; verify both callback orders, duplicates, multiple candidates, source transfer and cold-load interruption locally. If direct evidence remains unavailable, propose one native observation or a separately approved controlled-production route; do not silently convert normal unit training into a project.
4. Once provenance and admission are viable, synchronize the accepted cost clarification, implement the scoped batch, run targeted checks, then prepare the already planned one-session training→binding→travel→task test. No auto-open diagnostic campaign or repeated B201 load ritual.

Approval remains valid for the original bounded implementation. No new gameplay decision is inferred; no normal training is advertised as ready. Reattachment/repeat missions/N2/N3 remain outside scope.

## External leads — non-authoritative

[Unit API reference](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/Unit) lists archaeology-specific home-city access; absence of a general method in a community list is not proof of engine absence. [GameEvents reference](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/GameEvents) lists UnitAddedToMap owner/ID. [GCO source](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_UnitScript.lua) records creation before completion and correlates waiting units through city plots; this is an implementation example, not sufficient proof for this project's stricter source contract. No GCO code copied or executed.
