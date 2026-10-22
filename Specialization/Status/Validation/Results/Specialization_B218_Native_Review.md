# B218 — Occupied destination displacement and Spy-path investigation

Evidence review only. Source/live B218.245 remains unchanged. Prior [diagnostic implementation](Specialization_B218_Placement_Diagnostic.md) and frozen evidence are preserved. No repair implementation is authorized by this report.

## Native results

| Session / stage | Requested | Actual before → after | Target occupancy | Result |
|---|---|---|---|---|
| 053327 / mission |18,13|20,13 →17,13|Owner1 ID1572874 type0; Spy=false/Stackable=false; unchanged|MISSION_MOVE / EXACT_PLACEMENT_REJECTED|
| 053800 / mission |18,13|20,13 →18,13|Empty before; Expedition only after|Preparation, running and PLACES completion succeed|
| 053800 / return |20,13|18,13 →21,12|Owner1 ID2162690 type213; Spy=false/Stackable=false; unchanged|RETURN_CENTRE / EXACT_PLACEMENT_REJECTED|

The user waited for the wonder occupant to leave and identifies the return occupant as civilian 口述学者. Logs record type IDs, not localized names; SQLite rowid must not be used as GameInfo.Index. The same Expedition ID1638400/type244 survives each call. **Strong native evidence now narrows the practical failure to generic placement onto occupied destinations.** The exact closed-engine predicate (formation/owner/type/other eligibility) remains inferred, but repeating empty/occupied tests is not needed before investigating the primitive.

In the successful empty-wonder run, UI logs WAITING20,13→CONVERGED18,13. B217 therefore handles a real separate publication delay; it cannot correct Gameplay placement to a nearby tile. At05:41:11 PLACES SUCCESS / CIVILIZATION_KHMER / insight=NEW occurs before return failure. At05:41:19 archive historical3/effective3 includes Khmer PLACES; configured Tourism becomes6%. This supports mission completion and the history update, not independent native Tourism settlement/rounding proof. Preserve the earned record; do not replay the mission/reward to recover position.

No MOVE_EVENT appears. The first session ends GAME_EXITED with one PARTIAL_FRAME_AT_DEADLINE; the second ends INTERRUPTED without capture_error. B218 observes UnitMoveComplete; native UnitFlagManager also handles UnitTeleported separately. Missing MOVE_EVENT is not proof of no later engine event. Immediate Gameplay readback and the occupied/empty comparison are the stronger evidence.

## Earlier coexistence was real

[B184 native review](Specialization_B184_Expedition_Spy1_Native_Review.md), image4, records native arrival in Sparta with one other unit on the tile. [B189 native review](Specialization_B189_Expedition_Name_Task_Native_Review.md) records same-tile other-unit count1 during native travel plus a city-centre independent task. Those records did not establish the other unit's type or generic placement onto occupied mission plots. The user did not misremember coexistence; it was a different movement route.

## Direct source and database investigation

- `Mod/ExpeditionSpyRead.lua`, SubmitTravel: CanStartOperation/RequestOperation(SPY_TRAVEL_NEW_CITY). This retains the native arrival route.
- `Mod/ExpeditionSpyGate.lua`, relocate: RestoreMovement then generic PlaceUnit. It serves task placement, return to centre and alternate entry-city continuation. All three share the risk; the entry path has no new native failure evidence.
- Installed Civ VI `Base/Assets/UI/Choosers/EspionageChooser.lua:606` submits native city travel. `Base/Assets/UI/Popups/EspionagePopup.lua:327` submits the selected native task with target coordinates. `Base/Assets/Gameplay/Data/UnitOperations.xml:113` maps STEAL_TECH_BOOST to Campus. These inspected paths use engine operations rather than Lua PlaceUnit. No independent collision bypass was found in the inspected Lua/schema. The user's ordinary-Spy Campus observation is consistent with that distinct route.
- Read-only configured DebugGameplay.sqlite: both units have Spy1/Stackable1/IgnoreMoves1, DOMAIN_LAND, CIVILIAN formation. Ordinary Spy has CLASS_SPY/CLASS_LAND_UNITS/CLASS_KEQING_BUFF_UNITS; Expedition CLASS_LANDCIVILIAN. Inspected CLASS_SPY ability/modifier bindings grant promotions, sight, influence/yields or escape; no independent stacking override identified. Adding that tag blindly risks unrelated HD effects. Hidden engine use of tags is not ruled out.
- Other Units-row differences are identity/name, sight/moves, purchase/maintenance, TeamVisibility, advisor and experience. None is demonstrated as the occupancy switch. Do not copy all fields as a guessed repair.
- Installed `Base/Assets/UI/UnitFlagManager.lua:1151` handles UnitTeleported separately, a concrete diagnostic gap.

Public primary sources: [Sukritact's API index](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager) lists separate MoveUnit/PlaceUnit/RequestOperation surfaces without an occupied-Spy guarantee. [GCO's actual callsite](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_AIUnitScript.lua) uses MoveUnit for an adjacent destination and checks actual coordinates. [The original modder's experiment](https://forums.civfanatics.com/threads/lua-ai-control.633786/) reports historical multi-tile/pathfinding limits. MoveUnit is an investigation candidate, not a demonstrated drop-in collision-free teleport on this Mac/HD build.

## Proposed next boundary

Investigate the movement primitive, not additional waiting. A minimal ordinary-Spy/Expedition comparison at the same occupied target can distinguish generic placement policy from custom-type behavior. An alternative such as MoveUnit must first be checked against its path/eligibility constraints; capture exact positions, occupant stability, same-unit identity and native-operation state, including UnitTeleported events. Prefer one bounded user-triggered diagnostic over repeated manual scenarios. This is a future disposable-save prototype, not permission to modify ordinary Spies now.

If a safe primitive exists, replace only the shared relocate boundary and verify task/return/entry consumers. Keep exact-position protection, independent task/reward ownership, capacity and source binding. No timer/polling, forced retry, neighboring-tile acceptance, displacement/deletion of other units, unit replacement or native espionage task as a transport hack. If independent exact placement cannot meet the contract, present the technical limitation and a separate Design decision rather than silently changing task locations.

No new test is requested now. Await approval of the concrete next batch. Code/tests/Design/runtime/main/configuration remain unchanged; raw evidence is ignored and preserved.

## Evidence digests

`local/diagnostics/B205/session-20261017T053327Z-62eed5`:

- `records.log` SHA256 `1177bf62ff712e3e4c41ae1b9eef225bf9b35247730c16dfec34cb8f3656084b`.
- `events.jsonl` SHA256 `cadb0e93715979d10f20b5dd95a592e303547f0e4f9ec4182cea25157c3e39e1`.
- `summary.txt` SHA256 `57cd8e72ce81104a6b1ea1968e48a741fca2d644988175183cd668fa41a90a7e`.

`local/diagnostics/B205/session-20261017T053800Z-78c7ba`:

- `records.log` SHA256 `0f12d35447df4aacde210274b3a98feb513503db2dc42b01c1923e0d38307bd4`.
- `events.jsonl` SHA256 `60e934fd0469e7d5c65a18ab171656fa72b09adfbf3e825d970146cf260c109f`.
- `summary.txt` SHA256 `05a57160a7c81488939281ab57d49d2bcbbdb0110c6940721df1667dee435d55`.
