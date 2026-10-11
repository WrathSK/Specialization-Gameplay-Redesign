# B187.214 — name preparation native failure

Date: 2026-10-10. **USER_GAME_TEST_FAIL at pre-dispatch name preparation.** Arrival/name survival, independent task and END are **NOT_TESTED** in this submission. This is an evidence/plan checkpoint, not repair authorization.

Source: `198234b68f99c401b4b3d439356cf497e9cff727`; reviewed documentation HEAD `fda30868d28bbcd7c51130bbce5821bc79930866`. Recorded live receipt remains `B187.214-198234b-playtest.json`; no deployment or runtime re-verification in this review. [Original local result](Specialization_B187_Expedition_Controlled_Name_Local.md) stays frozen; its98 scoped methods did not cover delayed publication of a newly created Gameplay unit into the UI context.

## Native observations

Both originals were individually read. They show the same T86 report, with the second image scrolled down.

| Evidence | Observed fact | Limit |
|---|---|---|
| 7.10.20 PM | HELD / 实验暂停; `ISOLATION_OR_REQUEST_STOP`; own count1/1, one visible test team, source `Edinburgh (Test)` city393220/reference MATCH; team3342365 at source(62,33) | Source/capacity are retained; the report does not show an outbound journey. |
| Same image | Expected name includes `Edinburgh (Test) [E0-33001D-2]`; observed `人文考察团·间谍隔离验证`; name confirmation absent; collection and exact lookup name MISMATCH; plot PRESENT | The team still has its default name. This alone does not prove the engine refused a rename command. |
| Same image | Created/tracked/visible IDs all3342365; created/tracked/current lookups return3342365; target斯巴达; expected arrival UNKNOWN | No changed-ID arrival or B186-style returned Property loss was tested here. |
| 7.10.23 PM | STOP detail includes `ExpeditionSpyGate.lua:283: ISOLATION_OR_REQUEST_STOP: SPY_TEST_TEAM_REQUIRED`; mission events0/NONE; native total0, maximum5→5, ordinary Spies0→0, trainable yes→yes | Native classification0 differs from Gameplay-visible team1. It supports a publication/read-context gap but is not proof of its exact cause or exemption from native capacity. |

The diagnostic's one bundled assertion does not identify whether the UI unit was absent, its actual ID/owner disagreed, or its DB type could not be confirmed. The exact native failing operand remains **UNKNOWN**. No new harmless-coexistence, ordinary-Spy isolation or task-reward result is inferred.

## Confirmed implementation gap and local counterexample

The direct path is [Window CREATE reply](../../../../Mod/UI/ExpeditionSpyWindow.lua) → `prepareName` → [Read.SubmitName](../../../../Mod/ExpeditionSpyRead.lua). CREATE immediately calls the UI lookup/naming path after accepting the Gameplay reply. `afterPublish` refreshes diagnostics later; it does not postpone naming. The bounded name-readback wait starts only **after** SubmitName succeeds.

At the reviewed source, Read line166 asserts exact unit/ID/owner/type before rename capability, CanStartCommand and RequestCommand at line172. Gate line283 only wraps STOP. Given this preparation-stage error, the rename request was not reached. There is therefore no evidence yet that NAME_UNIT is unavailable to this custom Spy or that controlled names cannot survive travel.

A read-only reproduction uses the actual B187 Gate/Read/Window and existing fixture, with separate Gameplay/UI unit visibility. Gameplay creation succeeds while the UI collection temporarily returns no new unit:

| Local result | Observation |
|---|---|
| Initial creation | HELD with the same `SPY_TEST_TEAM_REQUIRED`; created1, count1, source retained; rename requests0, travel requests0 |
| UI publishes afterward; refresh | Unit becomes readable, but session remains HELD; no late rename/travel |
| Explicit END | Exact test unit removed in simulation |

**LOCAL_COUNTEREXAMPLE_REPRODUCED**, not a recording of native publication internals. It proves the implementation cannot tolerate this plausible cross-context timing. The screenshot and native-total mismatch are consistent with it; they do not uniquely establish it. No native call trace was available in this bounded review. No production code or formal tests were changed.

## Proposed bounded repair — awaiting approval

1. Distinguish UI unit-not-yet-readable from definite wrong ID/owner/type or unavailable DB definition. Wait read-only through the existing bounded publication/update hooks for the exact created unit before submitting NAME_UNIT. Definite mismatches stop; permanent absence times out with a specific reason.
2. Evaluate the post-creation ordinary-Spy comparison after that readiness boundary. Keep source/capacity reserved. Submit rename exactly once, then retain the existing raw-name readback and Gameplay confirmation gate before dispatch; do not weaken identity checks or automatically dispatch.
3. Report the failed stage and specific lookup condition. Closing/cancelling/timing out must leave no delayed surprise command. Add actual-module cases with separate UI/Gameplay views: delayed success, timeout, definite mismatches, close, and unchanged raw-name/arrival/task/END behavior.

Candidate implementation boundary: Window, Read, necessary localized diagnostic text and targeted tests, with only minimal Gate reporting changes if required. Spy=1, own cap1, exact source authority, independent no-reward timer, normal Spy definitions, permanent state and Design stay unchanged. No new registry or city-name authority.

**No repeat of unchanged B187 requested.** After an approved and locally checked repair, reuse the same continuous session: **① 创建Spy验证团** confirms name → **③ 原生派遣** confirms arrival/source → **④ 无奖励任务（2回合）** → **结束并移除验证团**. Only resume later steps if the preceding gate succeeds. No extra save/load ritual or formal N1/N2/N3/U2/rewards.

## Evidence archive and maintenance

Ignored local archive: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B187/2026-10-10/`. Both originals moved with filenames preserved and pre/post SHA256 equality; manifest associates this report. Local reproduction script/output are retained beside them with hashes. They are not public native logs or formal regression results.

- `Screenshot 2026-10-10 at 7.10.20 PM.png`: 13487996 bytes; SHA256 `4d298ce59a0777b50607d51db40725d79908eb33f26e64d5d07f6ba3ba673efe`.
- `Screenshot 2026-10-10 at 7.10.23 PM.png`: 13624659 bytes; SHA256 `f202521fd0d788a68999d60d0151599cf04facb3a77b1b0b61701476d5069472`.
- `b187_delayed_ui_publication_repro.py`: 2015 bytes; SHA256 `fffd3e3abaaa8bdab7e67259ac138dca772ebd2b820da728e570e5f791802db2`.
- `b187_delayed_ui_publication_result.txt`: 1057 bytes; SHA256 `60b38cda44a34bf0d9de4cceb183902696d5d7478b0d2b5d72a526acc8acde63`.

This checkpoint changes only current evidence/plan/Status and reviewed metadata. Mod, formal tests, Design, previous frozen results, runtime, main and GC are unchanged. No game launch, deployment or broad regression.

Documentation checks:13 changed/new Markdown links and anchors pass; P0-N1 selector/schema/hash check passes (211 runtime files,563 guarded files). CURRENT stays8 lines; current N1 slice11 lines. Protected source/tests/Design/runtime index and main match the pre-review checkpoint. No full gameplay regression was run.
