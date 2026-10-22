# B195.222 — compact native-style action slots and existing project icons

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; native rendering pending.** The user explicitly requested the screenshot5 visual corrections and existing one-turn project icons. [B194 screenshots](Specialization_B194_Expedition_Pending_Activity_Native_Review.md) separately pass the observed task Sleep/two-turn completion/release gate. B195 does not alter that activity implementation.

## Applied presentation changes

- [UnitPanelActions Lua](../../../../Mod/UI/UnitPanelActions.lua) collapses the hidden confirmation slot: one action width44, two actions width90. Prepare is offset0 when idle and46 when prepared, keeping its right-edge position; Confirm remains a separate left-hand control. Existing exact plan-token checks, pending disable, two-click prepare/confirm, executors, callbacks, events and fact reads are unchanged.
- [XML](../../../../Mod/UI/UnitPanelActions.xml) adds the native recessed UnitPanel_ActionGroupSlot/Glow behind the two buttons, width47/93 and height41. Native button hitboxes remain44×53, icons38×38. The control owns only its backing; it does not alter/reset native action instance managers. Current rendering alignment at different UI scales remains a visual check.
- [Icon aliases](../../../../Mod/Data/Icons.sql) use the existing native Spy unit icon/portrait for UNIT_SPC_EXPEDITION_SPY. Old Builder-based Gate/Spy0 prototypes stay unchanged. Current management action already uses native Spy travel artwork.
- Four identity-claim projects use the native Campus/Theater/Industrial Zone/Commercial Hub Great Person project icons respectively; 时代对话 uses the Theater project icon. Existing frontend/ingame registration is retained. Crew projects are not one-turn projects and keep existing Builder icons; the obsolete generic overflow test fixture has no district and is unchanged.
- No new localization key, art asset, gameplay state, task/native mission call, reward, capacity/binding, duration, project cost or permanent field.

Native source checked read-only: `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.xml`34–39,492–495,506–510 and `UnitPanel.lua`752–760 establish action stack/backing. `CIV_ASSETS` means the installed Civ6.app/Contents/Assets resolved for this machine, not a public evidence link. `UI/Icons/Icons_Projects.xml`, `Icons_Units.xml`, `Icons_UnitPortraits.xml` and native ProductionPanel's project icon lookup establish alias names. No native/HD file was changed.

## Checks

**44 focused tests PASS**: current action layout9, native icon aliases4, existing Expedition package/gate31. Actual UI Lua and crew executor were exercised with isolated native controls: distinct Prepare/Confirm hitboxes, repeated Prepare inert, exact confirmation consumes once and caps progress, stale token/target/unit/turn collapse, unrelated units hidden. The Settler test exercises its structured UI contract, not a new investment acceptance claim. Actual icon SQL runs in an in-memory database with distinguishable native sources; it checks all five project aliases, Spy icon/portrait, old prototypes/crew/native definitions unchanged and one registration per context.

New layout tests replace no historical assertions. Old snapshot-bound B045 tests remain frozen rather than being silently reinterpreted as current rendering tests. The only changed existing test is the package build version assertion. Independent source/native-style review found no actionable issue. Local coordinate arithmetic and XML validity do not prove native pixel alignment or all screen scales. No broad gameplay/stress or new save/load campaign.

## Minimal visual check after verified deployment

At the next convenient session, select an investment Settler or construction crew: one backed action should occupy one slot; preparing should add a separate confirmation on its left without making a repeated click consume the unit. No need to spend a unit solely for appearance. Look at available one-turn projects in the production list and the Expedition icon; confirm recognizable native artwork and no clipping/blank reserved slot. Only available project types need checking; do not manufacture four conquest fixtures for icon validation.

B194 activity/capacity/binding source is byte-identical. Do not repeat the two-turn or save/load test for these cosmetic changes. Formal **派遣 / 任务** entry changes, no auto-popup and complete task-time button hiding are recorded in the [existing UI plan](../../../Architecture/v2/P0_N_Expedition_UI.md#next-ui-batch--explicit-dispatch-and-task-actions); they are not implemented in B195. N2/N3, rewards, formal training/reattachment/persistence and repeated-task gameplay stay held.

Source and actual deployment are distinguished in [Status](../../Specialization_P0_Status.md#current-authoritative-state); this implementation report alone does not claim deployment.
