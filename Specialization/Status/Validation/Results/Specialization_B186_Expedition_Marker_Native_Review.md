# B186.213 — native arrival marker absent; controlled-name proposal

Date: 2026-10-10. Reviewed source `c627529`, documentation HEAD `d56f829`. **USER_GAME_TEST: arrival binding NOT_PASSED; custom task/END NOT_TESTED in this submission.** No implementation, runtime replacement or Design change in this review. [Frozen local checkpoint](Specialization_B186_Expedition_Arrival_Lookup_Local.md) remains unchanged.

## Submitted evidence

Two originals individually read and archived byte-exact to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B186/2026-10-10/`. `manifest.json` records names/sizes/SHA256;2/2 pre/post hashes match. Times below identify original filenames, not new test steps.

| Screenshot | Observed facts | Evidence limit |
|---|---|---|
| 6.48.04 PM, T86 | TRAVELLING; unit3276829 at(-9999,-9999); created/current IDs equal; visible and exact-lookup markers MATCH; source Edinburgh(Test), city393220, reference MATCH; count1/1; expected T88; native total1/maximum5, normal0; source turns0 and mission events0 | This verifies the existing marker is readable during the off-map phase; it is not an arrival result. |
| 6.49.19 PM, T88 | Still TRAVELLING/unbound with reserved capacity; visible unit3342365 at(23,15); collection count1; visible marker ABSENT and exact-lookup marker ABSENT; plot membership PRESENT; source reference MATCH and retained city393220 displayed | Actual destination read no longer suffers the prior plot-visibility ambiguity. Arrival is not accepted at the sampled due turn; no later HELD screenshot supplied. |
| Same T88 image | Created/tracked IDs3276829/3276829; lookup by created ID, tracked ID and observed3342365 all returns public ID3342365, each with absent marker | A stale requested ID can resolve to a new public ID in this observed route. This does not expose the native object's pointer or prove literal C++ deletion/recreation. |

Native maximum5→5, ordinary count0→0 and trainability yes→yes are reported; native total1. The temporary native-slot cost remains accepted. No independent task completion, END, new harmless-contact claim or general ordinary-Spy isolation PASS is inferred. The two images do not record the unit's raw/custom name.

## What is now established

In [Gate markerStatus](../../../../Mod/ExpeditionSpyGate.lua), ABSENT means the Property getter completed and returned nil; it is separate from unreadable, wrong owner/type and mismatch. The same marker was readable off-map in the preceding screenshot. **The namespaced unit Property is not available on the returned unit in this observed journey.** The city source has not been lost: its separate `sourceCity/sourceRef` still validates.

The B186 collection-based lookup and diagnostics answer the specific ambiguity left by B185. Merely changing lookup order again will not make this absent marker prove continuity. The guard correctly refuses adoption; no unchanged-package retest is requested. Global conclusions about every Spy Property or literal engine replacement remain unproved.

## User proposal and scoped technical assessment

The user proposes putting the bound city's name in the exclusive unit's name, updating it on reattachment. This is a practical candidate transport for identity because native Spy continuity already uses names. It is not rejected merely because it is a workaround. **City display text alone should not become city authority**: city renaming or a later newly trained team from the same city should not accidentally reinterpret an old binding.

A minimal proposed visible label is `人文考察团·爱丁堡 [E01]` (illustration only, not a frozen name or constant identifier). City text is readable; a short team key is fixed for that team's lifetime and fresh for a replacement. The existing own record keeps the exact source reference. Matching the controlled raw name/key identifies the team; it does not search for a city by name. Future authorized reattachment changes the source record and city label while retaining the team key. That future action still follows the accepted source-loss/reattachment contract; this proposal grants no free arbitrary rebind.

### Confirmed name surfaces

Paths are relative to the existing installed native asset/HD roots; no external source is modified.

| Source | STATIC_CONFIRMED evidence |
|---|---|
| `CIV_ASSETS/Base/Assets/UI/PartialScreens/EspionageOverview.lua:128–135,734–744` | Off-map Spy records provide Name and Level; UI uses them during travel. |
| `CIV_ASSETS/Base/Assets/UI/Popups/EspionagePopup.lua:150–155` | Mission renewal searches the live Spy collection by raw `pUnit:GetName() == kMissionHistory.Name` because history lacks Unit ID. |
| `HD_CORE/Gameplay/UnitAbilities.lua:530–546` | Exact ordinary UNIT_SPY path explicitly describes ID changing during travel while name persists, and uses GetName-keyed player Properties for reward history. This is precedent, not our binding authority. |
| `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua:2806–2814` | Native UI rename uses NAME_UNIT, PARAM_NAME and UnitManager.RequestCommand. |
| Native UnitPanel.lua:447–451; `HD_CORE/UI/Replacement/DL_UnitPanel.lua:114–118` | Rename availability is gated by CanStartCommand/rename capability; custom-Spy eligibility is not established. |
| Native UnitPanel.xml:332 | Standard rename text input has a48-character maximum. Keep a suffix short and do not truncate its identity portion; this is UI evidence, not proof of a universal engine limit. |

A bounded read-only check did not establish a direct Gameplay SetName setter. The confirmed UI command still requires custom-unit eligibility and exact readback. Standard Spy names being carried does **not** prove our arbitrary assigned name survives travel. Locale.Lookup/displayed labels must not be used instead of the raw name/key comparison.

## Next proposed minimal patch — awaiting authorization

1. Keep Spy=1, own cap1/source, current native travel and no-reward timer. Try the verified naming command only for the exact owned prototype; require successful raw-name readback before dispatch. If the custom Spy cannot be renamed, stop this specific route and report; do not alter native/HD definitions to force it.
2. Store the expected controlled team name/key in the existing prototype session record. On arrival use the existing player collection, exact owner/type/current-ID readback, unique expected key/name and valid source/target. This deliberately replaces the failed Property continuity assumption **if approved**, rather than silently accepting any lone Spy. Do not copy the missing marker as purported proof.
3. Report name preparation, before/after raw-name agreement, preserved source and new ID. Unexpected rename, duplicate key or invalid source remains a bounded stop. No new global registry, city-key system, saved-journey schema, name-to-city search or whole-world scan. Formal persistence/reattachment remains a later N1 boundary; a surviving name alone does not reconstruct missing prototype session state after load.
4. Local regression targets assignment/readback failure, duplicate or changed names, wrong owner/type/source, changed IDs and unchanged cap/task/END. Native delta is one session: confirmed assigned name → travel/new-ID name agreement → existing2T no-reward task → END. Do not add general rename/collision/cold-load campaigns to the user flow. If initial naming fails, stop before travel.

This is the recommended plan, not implementation authorization. Full N1 training/reattachment, N2/N3, rewards and icon/UI completion remain on hold. No test of unchanged B186 requested. The user decides whether to approve this small controlled-name prototype.

## Maintenance

Only evidence/current technical plan/Status and necessary reviewed metadata change. Screenshots remain ignored; prior records stay frozen. Mod, tests, Design, runtime, main, external game files and GC are unchanged. No gameplay tests, game launch or deployment performed. Current source/live stays B186.213/sourcec627529; receipt is retained, not re-verified by this screenshot review.
