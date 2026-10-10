# B176.203 — Dialogue high-percentage carrier comparison

State: LOCAL_CONTROL_PASS / USER_GAME_TEST_REQUIRED. D0049 unchanged; this is the user-authorized temporary carrier test, not cumulative-history integration or a full P0-M acceptance.

## Evidence and implementation boundary

The configured read-only `debug_gameplay_db` from the existing main local config was queried on 2026-10-09 (SHA256 `42b1f5286fa16a9ed89e610145283acfe78f299fcce1852178790d1df3c521fe`). The outer Cache database was initially located but is not the configured evidence baseline; the entries below were rechecked against the configured database. No external DB, HD attachment or game asset was changed.

| Existing attachment | Native mechanism / arguments | What it establishes |
|---|---|---|
| Amphitheater `HD_AMPHITHEATER_WRITING_CULTURE_BOOST` | `MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD`; WRITING, CULTURE, `YieldChange=2` | Flat Culture addition; not itself a percentage example |
| Amphitheater `HD_AMPHITHEATER_WRITING_TOURISM_BOOST` | `MODIFIER_SINGLE_CITY_ADJUST_TOURISM`; WRITING, `ScalingFactor=150` | Existing +50% Tourism configuration |
| Cabinet `HD_CABINET_GREATWORKOBJECT_WRITING_TOURISM_BOOST` | Same Tourism type / factor150 | Another existing theatre-building percentage source |
| Broadcast Center / Film Studio `HD_BROADCAST_MUISIC_TOURISM_BOOST` | Same Tourism type; MUSIC, factor200 | Existing +100% configuration |
| Cathedral `CATHEDRAL_LANDSCAPE_CULTURE_BONUS` | Same GreatWork yield type; LANDSCAPE, CULTURE, factor125 | Existing Culture percentage example, outside the theatre district |

Both single-city types use `COLLECTION_OWNER`; their effects are `EFFECT_ADJUST_CITY_GREATWORK_YIELD` and `EFFECT_ADJUST_CITY_TOURISM`. This is STATIC_CONFIRMED database evidence, not proof of stacking order or settlement. The existing Dialogue family already uses these primitives. No new native API is invented.

Reuse [Dialogue](../../../../Mod/Dialogue.lua)'s exact held writer. The existing +100% carrier has `ScalingFactor=200`; the added +200% carrier has factor300. Each has 14 attachments: Culture and Tourism for seven existing work categories. Remove old owned level/test before adding one replacement; never +100 and +200 together. No broad building cleanup or modification of the Amphitheater's +2 Culture.

The P0 **时代对话** button keeps **left-click read-only**. **Right-click** cycles one bound city through 0% baseline → +100% → +200% → END/current AUTO. Current Culture ACTIVE III or IV, a current paired collection and exact owner/reference are required to begin/advance. A repeated request does not advance twice. A failed native transition remains visibly unconfirmed and the next click attempts scoped exit. Confirmed loss/transfer ends the temporary test. Load reconstructs ordinary current effects rather than treating a saved test building as history.

Only one session fixture and one latest action receipt are retained. The existing sampling/event path is reused; no new event subscription, periodic census, persistent Property, history/quota change, independent GC or test history log. Temporary holds preserve the legacy Meaning API's default IV gate; the new control explicitly uses III. New source uses the existing current-facts/sample/ref and exact loss cleanup paths. Ordinary AUTO retains its old formula/IV gate until a separately approved cutover.

**Meaning Extension remains automatically active**, including its five current additions; Culture additions remain quarantined. This deliberately keeps the real coexistence environment. The test only projects Culture/Tourism percentages: it does not claim support for all native yield types. The configured DB also has supported-category HD works with native Food/Production/Science/Faith. Their exact admitted catalogue coverage, native-only multiplication and Meaning separation remain later M boundaries. Do not infer a full solution from this carrier test.

## Local validation

**16/16 new targeted methods PASS** in [test_dialogue_carrier_control.py](../../../../DevelopmentTests/test_dialogue_carrier_control.py): real Dialogue Lua/request handler and in-memory SQL; factor200/300, 14 exact attachments, unchanged HD examples, IV/III, 0→100→200→END, replacement/duplicate clicks, current-facts restoration, changed collection, UNKNOWN, wrong reference/owner/other city, removal/create faults, confirmed loss, cold session reconstruction, no permanent writes, unchanged project reporting, current package/import/file set, Chinese localization and P0 callbacks.

**18 additional selected related methods PASS**: eight maintained automatic Meaning cases, five applicable old probe cases, four B175 project/history cases and the actual left-click/non-overlap panel check. Existing B175 restart evidence is inherited; no repeat user save/load ritual is added.

Two additionally selected historical `MeaningProbeTests` cases **FAIL identically on the unchanged `af3bc4c` Dialogue baseline**: `test_new_write_failure_and_no_early_old_resume` and `test_duplicate_action_token_does_not_cycle`. The first expects an old bit carrier (`SCIENCE_1`) in the former probe path; the second assumes its older multi-stage advance sequence. Their assertions were not changed or silently counted PASS. They are not the current automatic Meaning entry. New control has its own actual-source duplicate/failure/END counterexamples above. Overall attempted selection: 36 methods, 34 PASS, 2 reproduced historical incompatibilities; no new regression found in that selection. Old version-pinned B059/modinfo77, B165/192, B166/193 and B175/202 package checks are not claimed current; current203 and localization8 checks are explicit.

Tests use Python3.14, existing Lupa lua55 and `SPC_DEBUG_GAMEPLAY_DB` supplied from the existing local config. Source database copied to memory only. These checks establish local behavior, not native yield, save serialization, CPU or memory improvement. The existing context helper registers P0-M2 in its batch-name list only; selector/schema/integrity logic is unchanged. Static checks:333 scoped Markdown links/anchors, current P0-M2 selectors/schema/reference integrity (194 runtime/515 guarded context files), independent helper self-test and3 helper tests PASS; scoped diff/JSON/hash review PASS. No all-history rehash.

## One minimal native session

Use one existing Culture III/IV city containing an ordinary Writing work whose yields are easy to read; an existing Culture IV fixture also keeps Meaning visible. Keep works, buildings, specialists, Governor and theme state unchanged throughout. No Dialogue project completion or accumulated100% history is needed.

1. Right-click **时代对话** once: report **0%基线**. Open the Great Works view and note the same work's Culture/Tourism and visible Meaning additions. This removes this city's old Dialogue percentage only, leaving the real HD/Printing/theme environment.
2. Right-click again: **＋100%**, configuration confirmed. Read the same work. This tests native percentage response while Meaning remains active; a carrier's mere existence is not yield PASS.
3. Right-click again: **＋200%**. Read the same work. This distinguishes replacement from stacking/residual +100%. With unchanged additive surroundings and no floor boundary, the percentage-caused delta should double relative to baseline; do not assume the already-buffed displayed total itself must double/triple.
4. Right-click again: test ends and **normal old percentage** is reported from current facts. Confirm yields return to their ordinary state. Earned +5% and used era remain unchanged; left-click still reads them.

A same-session before/after comparison is sufficient for this control. If the work view updates but city/turn settlement contradicts it, preserve that distinction and only then request the specific missing settlement observation; do not blanket repeat cold-load/defaultOFF/re-enable. If no response, stacking, or Meaning inflation appears, stop that gate and report it; do not rewrite the accepted native-only contract or alter another Mod to force a pass. Whole-city yield changes can contain other modifiers; report exact visible values instead of assuming a stacking pool.

## Checkpoint / remaining work

Source B176.203; recorded live remains B175.202 until the existing W0003 transaction succeeds. No promotion/main change. New cumulative multiplier, all-native-yield coverage, native-only/Meaning separation and automatic old-writer cutover remain unimplemented/unproven. M1 project/history and B174 accepted observations remain as [recorded](Specialization_B175_Dialogue_B174_Native_Result.md). No N/U2, GPP investigation, Design change or unrelated repair.
