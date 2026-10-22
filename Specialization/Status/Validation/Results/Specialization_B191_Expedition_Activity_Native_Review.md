# B191 — activity-state preflight failure and native task reuse boundary

**USER_GAME_TEST_FAIL: task startup; native SLEEP eligibility/write NOT_REACHED.** Two T88 screenshots were visually reviewed. The user reports the same apparent outcome and asks whether another unit or the native Spy task system can provide the required behavior. This is an evidence/investigation checkpoint, not an implementation or deployment.

## What this run actually demonstrates

- Before the attempted task, screenshot1 shows the named team 艾莉森, current ID3342365 versus created3276829, original Edinburgh(Test) city393220, position23,15, own capacity1/1, and matching name/source readbacks. The retained B189 continuity evidence is not overturned.
- Screenshot2 shows **ACTIVITY_UNEXPECTED_STATE**, task HELD, retained source and a refresh-to-verify binding message. This is different from B190 ACTIVITY_SLEEP_CONSTANTS_UNAVAILABLE. Native Spy capacity remains5→5, ordinary Spy count0→0 and observed completion events0. No native reward or task completion is demonstrated.
- In [actual B191 bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua), this error comes from the initial activity guard: the reading did not equal the accepted SLEEP/AWAKE/HOLD values. It occurs before the new action-hash lookup, CanStartOperation or RequestOperation. Thus this screenshot proves neither successful hash lookup nor native SLEEP denial. The exact activity value, its type and live enum values were not printed and remain UNKNOWN. Do not assume ACTIVITY_OPERATION from the screenshot.
- The report now exposes the precise branch and does not equate HELD with lost binding. Its post-failure matching source is not freshly verified merely because the pre-failure image matched. SLEEP/readiness/timer/release remain unreached; no unchanged-package retest is requested.

Two bounded in-memory reproductions used the actual bridge and existing fixture: native Spy operation-1 with mock generic activity3 or4 produces this exact error, with0 eligibility calls and0 Sleep requests. These values are counterexamples, **not measurements of the live activity**. No fixture/test/source edit or engine API execution occurred. B191's197 local methods retain their scope; they did not establish the native arrival activity value.

## What is exposed in the native Spy system

`CIV_ASSETS` below means installed Civ6.app/Contents/Assets. Files were read-only. These source coordinates are not public file links.

| Layer | Direct source | Consequence |
|---|---|---|
| Native mission list and eligibility | Base/Assets/UI/Choosers/EspionageChooser.lua:190–240 | Lua enumerates UnitOperations/UI categories and asks native CanStartOperation. UI construction is reusable; list presence does not prove a custom executor. |
| Mission submission | Base/Assets/UI/Popups/EspionagePopup.lua:472–475 | RequestOperation receives the operation Hash. The inspected Lua does not contain the engine operation body. |
| Native mission activity and duration | Base/Assets/UI/Panels/UnitPanel.lua:2143–2161 | ACTIVITY_OPERATION gates GetSpyOperation/GetSpyOperationEndTurn/GetTimeToComplete display. Our independent timer does not assign this native operation state. |
| Awaiting assignment | Base/Assets/UI/PartialScreens/EspionageOverview.lua:659–686 | Operation-1 displays awaiting assignment, separately from generic activity. It does not establish AWAKE/HOLD. |
| Native automatic chooser | Base/Assets/UI/Choosers/EspionageChooser.lua:738–758 | Separately checks IsReadyToMove and ACTIVITY_AWAKE. Readiness, operation and activity must not be collapsed into one flag. |
| Data configuration | Base/Assets/Gameplay/Data/Schema/01_GameplaySchema.sql:3006–3030 | Labels/UI category/Turns/probability/target fields exist. No handler inheritance/alias or Lua completion-body field in the inspected table. A cloned Gain Sources row inheriting its executor is unproved, not declared impossible. |

This is a layered interface: exposed data + Lua UI/request/readers + native execution. The public [UnitManager API inventory](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager) likewise distinguishes GetActivityType, eligibility and request methods; it is incomplete and cannot prove all other interfaces absent. Existing travel/name/coexistence evidence supports reusing the Spy shell in its measured scope; it does not require replacing our capacity/source/timer with native espionage.

Gain Sources has a documented automatic-success/no-risk contract, but grants native source strength; Listening Post also succeeds automatically but grants diplomatic visibility (Base/Assets/Text/en_US/Espionage_Text.xml:59–63,282–283). Counterspy has own-city targeting and defense effects. EspionagePopup.lua:257–267 suppresses reward presentation, not native effects. The previously recorded [HD completion/source-effect boundary](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#gain-sources-as-a-possible-task-template--user-follow-up) remains: no proved per-custom-unit suppression, no alteration of ordinary Spy state/listeners. That HD finding is inherited here, not claimed as a new full HD re-audit.

## Other native unit behaviors

| Comparison | Verified surface | Why it is not yet a neutral task primitive |
|---|---|---|
| Trader's multi-turn route | UnitPanel.lua:2164–2195 reads actual outgoing routes/TraderUnitID; UI/Choosers/TradeRouteChooser.lua:826–835 submits MAKE_TRADE_ROUTE | Real trade-route execution, movement and effects are coupled. Copying the presentation does not provide a no-effect busy state. |
| Ordinary sleep/skip/fortify | Gameplay/Data/UnitOperations.xml:78–79,102–103; UnitPanel.lua:4054–4066 | Sleep is the closest generic candidate; Skip is per-turn. B191 has not reached actual Sleep eligibility. The user's earlier B189 report that manual sleep permits turns is relevant user evidence, not a trace of this automated call. |
| Heal / religious heal | Text/en_US/InGameText.xml:2952–2953,2853–2854; Gameplay/Data/Units.xml:757 | Fortify-until-healed is health dependent; RELIGIOUS_HEAL is the Guru's charged heal action, not religious task sleep. |
| Alert / WAIT_FOR | UnitOperations.xml:119–120; InGameText.xml:2937–2938 | WAIT_FOR is localized as Alert; no verified wait-N-turns contract. Do not infer one from its name. |
| Aircraft patrol | Text/en_US/Civilopedia_Concepts_Text.xml:1023–1035 | Persistent activity has air-base/domain/combat semantics; not an independent harmless timer. |
| Official scripted action/timer | DLC/PiratesScenario/UI/Replacements/UnitPanel_PiratesScenario.lua:78–83; Scripts/PiratesScenario_UnitCommands.lua:45,87,127–132 | EXECUTE_SCRIPT routes to custom logic/property timers, with FinishMoves separately. Useful precedent for independent tasks, not a generic native busy-state setter. |

Actual ready-unit selection uses GetFirstReadyUnit (Base/Assets/UI/ActionPanel.lua:438,644). Hiding a prompt alone does not change engine readiness. No inspected alternative establishes a reusable no-effect busy-for-N-turns executor.

## Recommendation — no new implementation authorized

Do not infer that only rewriting native espionage can work. The current blocker is still the custom activity preflight. Before another writer patch, obtain one coherent, exact-unit read-only observation: raw activity/type; relevant live ActivityTypes values; native Spy operation/end turn; readiness; native SLEEP eligibility and available failure detail. This discriminates a representation/enum mismatch, an unhandled legitimate idle state, and a genuinely incompatible native activity. Do not blindly whitelist ACTIVITY_OPERATION or force Wake; a real operation must remain protected.

If the actual engine accepts SLEEP for the independently verified idle team, keep the bounded independent timer/owned activity route and correct only its evidenced precondition. If it denies Sleep, record that native reason and compare a scoped neutral operation alternative; Gain Sources copying/effect isolation would be a separate research/prototype decision. Neither route is implemented here. No request to repeat naming, cold load or broad task tests; unchanged B191 testing stops.

## Evidence archive and checks

Both originals were visually read and moved without renaming/overwriting into ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B191/2026-10-10/`; pre/post SHA256 matched. Local manifest points to this report. No image or raw log is committed.

- `Screenshot 2026-10-10 at 9.22.11 PM.png`: 12866003 bytes; SHA256 `4a154a80cd57d930b10d65a790b9a0a1e2ff26f4dcdfadeac0fe29240d27526a`.
- `Screenshot 2026-10-10 at 9.22.22 PM.png`: 12986112 bytes; SHA256 `b3abefe85c3ccd6ec3f7aaf9f0996ba0763d640f33d3ea3d28b5aef3809a28cd`.

Changed-document links/anchors, current selectors/context/hash consistency and exact documentation diff scope are checked. Mod, tests, Design, GC, main, deployment tools and external runtime remain unchanged. No game launch, native probe, implementation or new unit operation.
