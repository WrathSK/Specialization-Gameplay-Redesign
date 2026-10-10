# B182 Spy=0 review — dispatch blocked before travel

Date: 2026-10-10. Reviewed package: **B182.209 / modinfo209**, implementation `03a10723197d76d0ec7729e30670c7b4a45b19b3`. **N1 partial; dispatch gate failed; coexistence not reached.** This is evidence and technical advice for a possible Design discussion, not a new Design decision or authorization to implement another route.

## Result and screenshots

All three submitted originals were visually inspected in order. The selected target is Sparta. The city behind the panel is not evidence of arrival at that target.

| Screenshot | Native observation | Supported conclusion |
|---|---|---|
| 1 — 10:23:58, T84 | Team count1/1; own unit3145757 at(62,33); source Edinburgh (Test), city393220; bound/ready; other units on tile0; Spy capacity5→5 | **USER_GAME_TEST_PASS, creation/readback scope only.** One independent fixture and its source are visible. No second-create attempt or overlap shown |
| 2 — 10:25:01, T85 | Same unit, Owner indication, position, source and count; native travel2 + establishment0 =2; native Spy travel eligibility rejected; unit panel movement0/4 | **USER_GAME_TEST_PASS for these duration reads and observed pre-dispatch continuity.** Eligibility rejection is real, but does not identify its cause. Movement0 is not proof of an attempted right-click being blocked |
| 3 — 10:26:11, T85 | `当前操作未完成：API_UNAVAILABLE`; timing read still2+0; Spy capacity still5→5; no journey/due-turn/arrival report | **USER_GAME_TEST_FAIL for completing dispatch.** No evidence of actual travel, exact foreign-center placement or harmless coexistence. The error renderer suppresses unit/source lines, so their absence does not prove the unit or binding was deleted |

No same-tile military/civilian contact, hostile contact, successful END, duplicate creation, or save/load result is in this submission. These are **NOT_TESTED**, not FAIL. Both successful readbacks show other-unit count0. No additional user test is requested during this evidence review.

## Why this is not evidence that Spy=0 cannot travel

The actual [Gameplay gate](../../../../Mod/ExpeditionGate.lua) calls `c:IsCapital()` inside `target()` (line49), before writing `startTurn`, `dueTurn` or `TRAVELLING`. The API maintainer documents [City:IsCapital](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/City.IsCapital) as **UI-only**. The [UI reader](../../../../Mod/ExpeditionGateRead.lua) using it successfully therefore does not establish its availability to Gameplay. [PlayerCities:GetCapitalCity](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/PlayerCities.GetCapitalCity) is documented in both contexts and is already used by our Gameplay-side [NetworkInput](../../../../Mod/NetworkInput.lua); it is a candidate for a later narrow repair, not a change made here.

**Confirmed source/test defect:** [the current local fixture](../../../../DevelopmentTests/test_expedition_gate.py) supplies `targetCity:IsCapital()` to Gameplay. That conceals the documented context difference. The gate's `reason()` maps unclassified Lua exceptions to `API_UNAVAILABLE`; its log prints only that reduced code. Therefore the screenshot is not a direct native stack trace identifying this method, and cannot establish that `PlaceUnit` itself was unavailable or rejected stacking.

Two read-only local runs loaded the unchanged real module through the existing Lua55/Lupa fixture; no source/test file was edited:

| Fixture | Dispatch result | Stored due turn | PlaceUnit calls | Team/source after request |
|---|---|---:|---:|---|
| Existing mock, including Gameplay `IsCapital` | TRAVELLING, no error |83, from start81 +2 |0; not due yet | count1, unit40, source1, bound/same-unit true |
| Same mock, only `targetCity.IsCapital=nil` | CREATED, `API_UNAVAILABLE` | absent |0 | same count/unit/source/binding |

Raw exception in the second run: `attempt to call a nil value (method 'IsCapital')`, actual gate line49. **LOCAL_SIMULATION_CONFIRMED counterexample**, not a native arrival test or proof that this is the only native failure. The legacy documented `/tmp/spc-b069-python` dependency path was unavailable; the existing `/private/tmp/spc-l2c-python` Lupa installation with Python3.14 ran the comparison. Nothing was installed. Reproduction: instantiate `Gate().runtime()` from `test_expedition_gate`, call `req('CREATE','c')`, remove only the method for the second fixture, then `dispatch('dispatch')`; capture the existing `pcall` error in memory. The normal module and mock are unchanged. This review did not rerun the full 62+10 suite or reclassify its earlier result as native evidence.

The inspected current GameCore/UserInterface logs contained no `N1_ZERO`, `ExpeditionGate` or `API_UNAVAILABLE` trace; no Lua.log was present in those known log locations. No game/configuration change was made to enable logging. **Most directly supported explanation: a Gameplay/UI API mismatch in the prototype. Exact native exception remains unconfirmed.**

## Capacity and city binding

- **Our capacity:** creation/readback shows1/1 across T84→T85. Static code counts both exact old/new fixture types and refuses creation when occupied. This is independent of native Spy accounting, but native duplicate-create enforcement and post-arrival count are not newly proven.
- **Native Spy capacity:** the displayed maximum remains5→5 throughout. `GetSpyCapacity()` reads the maximum, not used slots or ordinary-Spy trainability. It does not prove every Spy subsystem is unaffected. The installed stock overview filters `.Spy`; this prototype is Spy0 and is not counted by that particular loop.
- **Source binding:** the same own unit3145757 and source city393220 remain visible across the two successful readbacks. Actual code checks the stored owner/city/coordinates/token reference, not the displayed name alone. The third image hides these fields because of its error; the local counterexample preserves them, but post-failure native binding was not separately observed.
- **Persistence:** the prototype deliberately owns session-only binding/timing. No Property/Store write or formal saved journey was implemented. A loaded native fixture counts toward capacity but is cleanup-only without a guessed binding. No formal persistence or reattachment PASS is claimed.

## Which parts require Spy=1?

| Component | Current answer | Evidence / limit |
|---|---|---|
| Dedicated management window, own cap/source record and task timer | **No Spy1 requirement in our architecture** | Gameplay owns these records; they do not call native Spy missions. Current runtime demonstrates creation/readback, not completed travel |
| Travel/establishment duration getters | **Spy0 works for this fixture/target** | B182 returns2+0; prior B180 getter evidence is consistent. Do not generalize to all targets/conditions |
| Ordinary movement-input lock | **Independent of Spy1 statically** | Installed `Base/Assets/UI/WorldInput.lua:803,898` checks `IgnoreMoves`. Current0/4 display alone is not a native command-path test |
| Unmodified native Spy chooser and overview membership | **Explicitly require Spy1** | Installed `Choosers/EspionageChooser.lua:630–639` rejects non-Spies; `PartialScreens/EspionageOverview.lua:88–100` counts only `.Spy` units. We can keep our own window |
| Native `SPY_TRAVEL_NEW_CITY` execution and off-map lifecycle | **Not established for Spy0** | Eligibility rejected in this fixture; zero movement/target/other conditions were not isolated. We did not submit the operation or perform a Spy1 control, and native implementation is not exposed |
| Our independent timed `PlaceUnit` arrival | **Still untested natively; Spy1 necessity unknown** | The identified API boundary occurs before timer/placement. An exposed placement method does not prove foreign-city occupancy legality |
| Harmless overlap with foreign military/civilians, including war | **Unknown for the proposed custom shell** | `Stackable=1`, retreat0 and Spy0 are separate fields, not demonstrated immunity. No observed overlap or contact in these screenshots; do not import B180 retreat evidence as coexistence PASS |
| Independent deterministic missions, capacity and archive semantics on a future Spy1 shell | **Could remain ours, but isolation unproven** | Spy1 would also enter stock Spy classification. Used slots, targets, native identity/lifecycle and incidental native/HD hooks need specific verification; our own counter cannot cancel those effects |

No evidence here makes Spy1 necessary for the **gameplay concept**. What explicitly needs it is entry into certain **stock Spy UI paths**. Borrowing all native movement/immunity behavior merely by removing `CLASS_SPY` is not supported: `Units.Spy`, tags, promotion class, input rules and native operations are distinct.

## Implications for a Design revision

**Do not revise the no-walking / harmless-coexistence requirement merely to accommodate this dispatch error.** A narrow API-context correction plus accurate error reporting is the highest-information next technical step if separately authorized. It should preserve cap/source guards and use context-faithful mocks; then native testing need only reach arrival and overlap, without repeating unrelated lifecycle tests.

Keep these implementation choices distinct for the discussion:

1. **Spy0 map unit:** preserves separation from espionage. Its foreign placement and harmless contact still need proof; this submission has not rejected the route.
2. **Spy1 shell with our own tasks:** may offer useful native travel behavior, but ordinary Spy accounting, target restrictions, identity continuity and unwanted completion/detection/HD effects remain isolation questions. The existing [investigation](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#direct-spy-reuse-without-detection--follow-up-requested-by-the-user) distinguishes detection-gated diplomacy from unrelated mission-completion rewards. Do not promise “always succeeds” means undetected, or use HD's reward pipeline for future Expedition Era Score.
3. **Logical team with map presentation:** a possible contingency if native unit coexistence proves unsuitable. It would change how selection, physical presence and native interactions are represented, and needs user approval and rendering investigation. It is not implemented or adopted.

The latest explicit Expedition direction already differs from the formal Shared retreat contract. Before formal N1 integration, record the named exception without changing other professional units. This review itself changes no accepted Design. N2/N3, era UI, formal training/persistence/reattachment and rewards remain held. **Next boundary: user reviews this report; no automatic fix, Spy1 switch or extra test.**

## Evidence archive and repository checks

Original filenames preserved under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B182/2026-10-10/`. **3/3 SHA256 MATCH** before/after archival. No image committed; no duplicate left in the inbox. This table is the evidence manifest for this result.

| Original filename | Bytes | SHA256 |
|---|---:|---|
| `Screenshot 2026-10-10 at 10.23.58 AM.png` | 13053614 | `795df8c7731e063ccb746b72779228ed719f7fa0250afbcc1df6d32e83afbc4d` |
| `Screenshot 2026-10-10 at 10.25.01 AM.png` | 13639351 | `78c0874daf45b3d6eccc89a3ba3c3e7fa9515f42256d692249a963c347479dfe` |
| `Screenshot 2026-10-10 at 10.26.11 AM.png` | 13326783 | `ff756d254bcc326731327c5286fe137758305c71bc23421a35ef54a4248eb44c` |

Only this new result and directly affected current technical/plan/status/context pointers are changed. The B182 local result, B180 evidence and all prior frozen reports remain unchanged. Mod, DevelopmentTests, Design, runtime, deployment tools, GC and main remain unchanged. Runtime identity comes from the existing deployment record; this review does not reverify external runtime equality or deploy anything.

**Review checks:**59 scoped links/anchors PASS; current manifest/schema/selector/hash integrity PASS (202 runtime files /540 guarded files); protected-file and main-isolation checks PASS; diff reviewed and whitespace check PASS. Status CURRENT remains10 lines. Two actual-module counterexample runs completed as above; no gameplay regression, new native test, game launch or deployment.
