# B188.215 — native naming eligibility stops the session

Date: 2026-10-10. **USER_GAME_TEST_FAIL at native rename eligibility.** The exact UI unit is now readable; no rename command is submitted. Arrival/name survival, independent task and END are **NOT_TESTED** in this submission. This is an evidence/investigation checkpoint, not repair implementation authorization.

Source: `21f2bf1cec8cf32a8d7cb9ac97a40ec9447120f8`; documentation HEAD `ae625b71d47779204132098cef08f74aa13da3fe`. Recorded live receipt remains `B188.215-21f2bf1-playtest.json`; this review does not reverify or change runtime. The [110-method local result](Specialization_B188_Expedition_UI_Readiness_Local.md) and [B187 failure](Specialization_B187_Expedition_Name_Preflight_Native_Review.md) remain frozen with their original evidence scope.

## Native observations

Both originals were individually read. They are two scroll positions of the same T86 report.

| Evidence | Observed fact | Interpretation / limit |
|---|---|---|
| 7.29.55 PM | HELD / 实验暂停; stage COMMAND, `NAME_COMMAND_NOT_ALLOWED`, wrapped as `ISOLATION_OR_REQUEST_STOP` | B188 has reached the command-permission gate, beyond B187's exact-unit preflight failure. |
| Same image | Own count1/1, one visible team3342365 at source(62,33); retained source Edinburgh (Test), city393220; source reference MATCH | Source binding and capacity remain intact. This is not a new source-loss result. |
| Same image | Expected name `Edinburgh (Test) [E0-33001D-2]`; observed `人文考察团·间谍隔离验证`; collection/exact name MISMATCH; plot PRESENT; created/tracked/visible IDs all3342365 | Default name remains. No name-string, length or encoding rejection is demonstrated because submission is not reached. |
| 7.29.57 PM | Native maximum5→5, ordinary Spies0→0, trainable yes→yes; native total1; `SLOT_COST_ACCEPTED` | Current publication/ordinary-Spy preflight succeeds in this fixture. Temporary native-slot cost remains accepted; this is not every ordinary-Spy scenario. |
| Same image | Target斯巴达, arrival UNKNOWN; mission events0/NONE; STOP detail includes Gate line283 and `NAME_COMMAND_NOT_ALLOWED` | No journey, independent no-reward task or END evidence is added. |

## Exact failure path

[Read.SubmitName](../../../../Mod/ExpeditionSpyRead.lua) lines187–198 rechecks exact unit readiness, rename capability and command constants, then asserts `UnitManager.CanStartCommand(u, UnitCommandTypes.NAME_UNIT, true) == true` at line195. The screenshot's error is this assertion. `RequestCommand` at line198 was not reached; Gate line283 only wraps the failure. [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) runs the post-creation audit after readiness and then calls SubmitName once.

The native return did **not equal boolean true**. Its actual false/nil/other value is not recorded, so do not claim a captured false return or engine-provided rejection explanation. A truthy nonboolean result would pass the native UI guard but fail B188; this return-type possibility also remains unobserved, not a confirmed fix. The current evidence does not support increasing the readiness wait as the remedy. Exact unit readability does not prove every native command condition has settled; the engine predicate and returned value remain unobserved. B188's local tests model allowed/disallowed commands; they cannot prove this custom unit is eligible in the native engine.

## Bounded native / HD evidence

External source aliases below identify read-only installed sources, not public repository links: `CIV_ASSETS` is `Civ6.app/Contents/Assets`; `HD_CORE` is the installed HD Workshop package2465378070. The existing configured gameplay DB was opened read-only. No external source/DB was edited.

| Source | STATIC_CONFIRMED fact |
|---|---|
| `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua:447–451,2806–2814` | Native rename uses the same CanStartCommand signature and PARAM_NAME/RequestCommand pattern. Its guard uses Lua truthiness; B188 requires boolean true. No incorrect command parameter was found. |
| `HD_CORE/UI/Replacement/DL_UnitPanel.lua:114–118` | Same truthiness/capability guard as native UI, without a Spy-specific override in this branch. |
| `CIV_ASSETS/Base/Assets/Gameplay/Data/UnitCommands.xml:24,48` and loaded `UnitCommands` | NAME_UNIT is registered; no prerequisite tech/civic or DisabledHelp explains this rejection. The predicate is delegated to the engine. |
| `CIV_ASSETS/Base/Assets/Gameplay/Data/GlobalParameters.xml:605` and loaded DB | `UNIT_EXPERIENCE_LEVEL_FOR_CUSTOM_NAME=2`. UnitPanel lines2770–2777/2795–2800 place rename in its veterancy/unique-name UI. |
| Loaded `Units` | Custom `UNIT_SPC_EXPEDITION_SPY`: Spy1, PROMOTION_CLASS_SPY, CanTrain0, CanEarnExperience0. Ordinary UNIT_SPY has CanEarnExperience1. Both ImmediatelyName0. |

**Inference, not confirmed root cause:** veteran-level eligibility is a concrete plausible blocker for this fresh non-experience prototype. The actual engine predicate, its treatment of Spies and this unit's internal eligibility remain **UNKNOWN**. Do not turn the inference into a general Spy rename prohibition or award XP/change global parameters as an assumed fix.

A bounded exact `:SetName(` / `:SetName (` search over28 native `DLC/*/Scripts/*.lua` files found no calls. This establishes no supported setter signature/context; it does not prove no setter exists. Loaded `UnitNames` has ID/NameType/TextKey, generic prefix/suffix groups and no Spy/custom group; it is not a per-UnitType Spy name pool. It does not establish where native Spy names originate or that a custom pool would work. No unsupported setter, blind RequestCommand bypass or speculative name-pool implementation was attempted.

## Next boundary — technical evidence before another patch

No repeat of unchanged B188 and no save/load ritual is requested. Before proposing another implementation, establish a supported exact-unit naming route or native Spy name-assignment surface from primary/local API evidence, including context, readback and custom-type eligibility. Keep this investigation limited to naming/continuity; do not reopen travel, rewards or capacity design.

If a supported route is found, propose a minimal change preserving own cap1, exact source authority, one-time assignment/readback and unambiguous arrival matching. Native name survival still needs the already-pending arrival gate. If no safe route is established, report that boundary before selecting another identity strategy; do not adopt a unit from its city name, location or merely being the only matching unit. City display text is never source authority. No global threshold, ordinary Spy/HD definition, earned XP, permanent schema or formal N1/N2/N3/U2/reward change is authorized here.

## Archive and maintenance

Ignored archive: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B188/2026-10-10/`. Original filenames preserved;2/2 moves verified by pre/post SHA256 and linked by local manifest. Screenshots are not committed.

- `Screenshot 2026-10-10 at 7.29.55 PM.png`: 13278288 bytes; SHA256 `d2ca86366b393717e0a55fdd8acc57925eea9a2fef2b0268195ec65f24c48bb7`.
- `Screenshot 2026-10-10 at 7.29.57 PM.png`: 13355231 bytes; SHA256 `bdabef328e223baf9e1759531c764e829fe6638aa7996059a4ba57d8fedf3f85`.

Only this result, current navigation/Status/plan and reviewed metadata change. Mod, formal tests, Design, previous frozen evidence, runtime, main and GC remain unchanged. No game launch, deployment or gameplay regression. Documentation validation is limited to changed/new links, current selectors, schema/hash integrity and diff review; no native result beyond the two images is claimed.
