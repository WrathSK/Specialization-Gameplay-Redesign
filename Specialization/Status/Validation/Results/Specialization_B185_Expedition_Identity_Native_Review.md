# B185.212 — travel identity failure and native Spy continuity

Date: 2026-10-10. Reviewed source/deployment `4d8ace2`, current documentation checkout `53aa474`. **PARTIAL native evidence: redirection works in the user's observed path; arrival binding NOT_PASSED; independent task NOT_REACHED.** No implementation or deployment is performed by this review. [Current slice](../../../Architecture/v2/P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) · [Frozen local checkpoint](Specialization_B185_Expedition_Identity_Task_Local.md).

## Four submitted screenshots

All four originals were read individually. Times identify their original filenames on 2026-10-10. The Git-ignored archive is `local/legacy-workspace/Specialization/Status/Validation/Evidence/B185/2026-10-10/`, relative to develop; original names/bytes and SHA256 manifest are retained. They are not public image attachments.

| Image / time | Observation | Scope |
|---|---|---|
| 1 / 2.20.33 PM / T86 | Created ID `3276829`, source Edinburgh(Test), city `393220`, position `(62,33)`, count1/1 and marker verification successful. | Creation marker/source readback observed. Immediate native classification0 is not a settled capacity measurement. |
| 2 / 2.20.37 PM / T86 | Same ID/source; Sparta travel2T + establish0T, native travel allowed, native classification1. Sources0; Gain Sources success-undetected1 / detected-success0, execution blocked. | Read-only eligibility, not mission execution/isolation PASS. |
| 3 / 2.20.41 PM / T86 | Travel starts, dueT88; same ID and verified marker at `(-9999,-9999)`, source preserved, count1/1. | Native off-map transition observed. |
| 4 / 2.21.48 PM / T88 | Visible ID `3342365` at `(23,15)`; report still TRAVELLING, unbound, reserved count1/1, observed team count1. Source line and marker-success line absent. Native classification1; player-level mission events0. | ID changed and binding gate did not accept arrival. No marker value for the new ID is printed; missing source line is not proof of erased source. T88 is within the gate's grace interval, so this is not a displayed timeout/HELD error. |

The user separately confirms original-button redirection works. This is **USER_GAME_TEST_PASS for that observed entry**, not proof of every chooser/popup/keyboard route or ordinary-Spy independence. The two-turn task and END are **NOT_REACHED / NOT_SUBMITTED in this evidence**, not failed timer/cleanup tests. No new cold-load, ordinary-Spy, promotion persistence or reward-isolation conclusion follows.

## Why a Spy can keep its name and rank while Unit ID changes

Installed native UI separates current map Units from travelling Spy records:

| Native/HD source (relative to the existing configured roots) | Evidence |
|---|---|
| `CIV_ASSETS/Base/Assets/UI/PartialScreens/EspionageOverview.lua:88–109` | Current Spies come from `player:GetUnits():Members()`. |
| Same file `128–136,734–758` | Travelling Spies come from `GetNumSpiesOffMap` / `GetNthOffMapSpy`; the UI reads `Name`, `Level`, `ReturnTurn`, `XLocation`, `YLocation` from these records. |
| `CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:604–618` | Lua submits `SPY_TRAVEL_NEW_CITY`; the actual transfer is native engine work. |
| `HD_CORE/Gameplay/UnitAbilities.lua:530–546` | HD explicitly notes city travel changes Unit ID while name persists. Its exact ordinary `UNIT_SPY` promotion path uses name-keyed player Properties. That workaround does not establish a safe unique key for our custom team. |
| Native overview `945–963` | The used callbacks are `SpyAdded(owner, unitID)` and `SpyRemoved(owner, counterSpyPlayer)`, not an old-ID/new-ID pair. |
| `CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:149–157` | Mission renewal searches by name because history lacks a Unit ID. This is not a general unique-identity guarantee. |

**STATIC_CONFIRMED:** native Spy continuity and a stable exposed map-unit ID are different contracts. The separate off-map record explains why native names/ranks can persist. **INFERENCE:** the changed ID is compatible with removal/rematerialization or replacement of the on-map representation. Literal C++ destruction/recreation, preservation of all promotions, and copying arbitrary Lua Unit Properties are **UNKNOWN** from the inspected Lua and screenshots. Our code only creates on CREATE and destroys on END; dispatch itself requests native travel ([Gate](../../../../Mod/ExpeditionSpyGate.lua), [reader](../../../../Mod/ExpeditionSpyRead.lua)).

Captured Spy records expose `NameIndex`, used as a `DealItemTypes.CAPTIVE` identifier (native overview802,817–831,870–894). No inspected call proves an equivalent readable key on both the travelling record and returned live Unit. It is a conditional research lead, not a ready binding contract. The public [PlayerDiplomacy reference](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerDiplomacy) does not document these travel details; its omission is not API-impossibility evidence. Installed native consumers are the stronger source here.

## Confirmed B185 lookup and reporting gap

[Gate lines93–106](../../../../Mod/ExpeditionSpyGate.lua) first asks `FindID(oldID)`, then searches **destination plot occupants** for the preserved marker. [Snapshot lines132–148](../../../../Mod/ExpeditionSpyGate.lua) separately finds the displayed new ID through the **player unit collection**, then checks binding against the old tracked lookup. It does not show the candidate's marker value/status or compare these enumeration surfaces.

Consequently the same visible result can mean:

- the new object lost the marker; or
- the marker survives on a unit visible through `Members()` but absent from plot enumeration; or
- lookup/publication timing prevents the expected object from being read reliably.

Whether native Spies are included by `Units.GetUnitsInPlot` in this fixture remains **UNKNOWN**. The new screenshots do not distinguish these cases. A fresh READ already re-runs observation; this is not simply an omitted arrival-event callback.

`sourceCity/sourceName/sourceRef` remain session-owned. [Window lines28–29](../../../../Mod/UI/ExpeditionSpyWindow.lua) hides the normal source line when unbound. This is a misleading presentation boundary, not evidence of data deletion; no code cleared the source during travel. Display should distinguish “record retained” from “returned unit verified.”

## Actual-module local counterexamples

Using the unchanged `gate()` / `arrival()` fixtures in [test_expedition_spy_task.py](../../../../DevelopmentTests/test_expedition_spy_task.py), three isolated in-memory runs create40, dispatch, expose41 at the target, and issue READ. Only simulated marker retention and plot enumeration differ:

| Mock condition | Phase / observed→tracked IDs | Marker / binding | Source |
|---|---|---|---|
| Preserved marker; plot omits Spy | TRAVELLING /41→40 | Present / unbound, reserved | city1 retained |
| Lost marker; plot includes Spy | TRAVELLING /41→40 | Absent / unbound, reserved | city1 retained |
| Preserved marker; plot includes Spy | ARRIVED /41→41 | Present / bound | city1 retained |

All three: count1, property writes1 (creation only), destroy calls0. This **LOCAL_SIMULATION** proves diagnostic ambiguity, not the native cause. The fixture itself constructs a replacement mock and optionally copies its property table; it does not establish actual engine preservation. Raw script/output are retained beside the ignored screenshot manifest as `repro.py` / `repro-result.txt`; no formal test file or assertion changed. Run with the existing Lupa lua55 / Python3.14 environment and `DevelopmentTests` on `PYTHONPATH`; no dependencies were installed. Initial default/historical dependency paths were unavailable; the existing compatible environment was then located and the three cases completed.

## Proposed next bounded repair — not implemented or newly authorized

1. Reuse the exact custom-type player collection already used by reporting to inspect the returned candidate during pending travel/explicit refresh. Accept continuity **only** on a uniquely matching surviving marker, exact Owner/type/ID readback, and valid retained source/target. Do not require a Spy to appear in physical plot-occupant enumeration. Avoid a permanent new all-unit scan outside pending travel/explicit diagnostics.
2. Report created/tracked/observed IDs, actual old/new lookup return IDs, marker absent/mismatch/match/unreadable, and plot-versus-player visibility. Always show the retained source as unverified while binding is unresolved. Preserve UNKNOWN, ambiguity and timeout protection; never copy the token onto a candidate or adopt by name, coordinates, ID arithmetic or sole presence.
3. Add local counterexamples for the enumeration difference plus missing/ambiguous markers. If native evidence then confirms marker loss, stop marker-based adoption and investigate the smallest engine continuity key/owned dispatch association separately; do not silently weaken matching.
4. Resume the existing single native session only after the delta exists: verified arrival → independent no-reward task → END. No repeated test of unchanged B185 and no save/load ritual. Formal N1/N2/N3/UI production work remains held.

The user suggests reusing the original button's icon after prototype verification. Record this as a future UI presentation preference; no icon asset or runtime UI change is made now.

## Maintenance boundary

Four images archived with pre/post SHA256 equality; active links/selectors/current context checked; only evidence/current documentation and reviewed hashes changed. Prior local/native records are not rewritten. Design, Mod, formal tests, runtime, external assets, GC, main and deployment remain unchanged. No game launch, gameplay regression or new native result is claimed.
