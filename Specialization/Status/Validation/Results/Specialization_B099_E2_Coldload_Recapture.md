# B099 E2 cold-load / conquest recapture evidence — 2026-09-25

User confirms screenshot order: 06:28:58 after cold restart/load, **before conquest**; 06:29:57 after conquest. This supersedes only the prior report's untested cold-load/recapture status, not its frozen observations. No runtime/Design changes or deployment.

## Native observations

External archive: app-support `Specialization/Status/Validation/Evidence/B099_E2_Coldload_Recapture_20260925/`. Two reviewed originals moved with SHA256 verification; 40 current logs copied, manifest retained. No saves modified. LoadGameViewState records deserialize completion06:27:55, initialization06:27:58, startup06:28:02 and load end06:28:09.

| Evidence | Result |
|---|---|
| Cold-start load | User confirms successful load. Screenshot retains HELD_TRANSFER rev3, original0/262146 @28,34/token DEV-B013-P0-3, foreign current3/131073/token nil |
| Permanent authority before conquest | RESEARCH Potential2, investment1 retained across save/load; no proof every profession's permanent assets tested |
| Exit after cold-load | WITHDRAWN23/23, checked2322/removed0; research support/housing/GPP0/0/0; old target sourcefalse/receiverfalse/routes0 |
| Conquest | Second screenshot shows own unit capturing Washington; selected own city. This is a conquest return following an outbound diplomatic trade, not a symmetric trade-back test |
| Progression after conquest | B033 progression UNKNOWN: PROGRESSION_HELD, stack CityProgressionStore active/Base → EffectiveFacts Read/Describe → Gameplay request. Recapture did not unlock the authoritative read path |

The prior22/23 partial exit is no longer observed after cold-load. This does not identify the unfinished prior module or prove native RemoveBuilding performed removal: removed0 still means no actual removal observed. The independent wrong-owner Network diagnostic row remains invalid evidence of the target's current Network identity.

## Static explanation and remaining uncertainty

`Mod/CityProgressionStore.lua`:

- `active()` refuses reads unless the saved record is ACTIVE; this is the source of PROGRESSION_HELD. The report does not prove deletion/reset of Identity/Potential/receipts.
- `recapture()` first requires a matching original-owner/new-city/previous-owner CityTransfered notification and saved loss. It then requires live city TOKEN to equal the original saved token. A matching location or stored original token alone cannot satisfy it.
- The foreign city has token nil in both pre-load and post-load evidence. A missing token after return would therefore reject restoration, but there is **no post-conquest E2 token/candidate/rejection report** here. Cannot assert RETURN_IDENTITY_UNCONFIRMED actually fired.
- Only CityTransfered forwards owner arguments to this resolver. CityAddedToMap/Removed/Initialized reconcile without arguments; CityConquered has no E2 subscription. Whether this conquest emitted the expected CityTransfered signature/order remains unobserved. Event mismatch and live-token rejection remain separate candidates.
- `DevelopmentTests/test_p0_e2_recapture.py` keeps the token in its successful simulated loss/return path, explicitly tests missing-token rejection, and supplies the expected CityTransfered arguments. Those tests prove conditional safety, not native identity continuity. B097's native feasibility was not established by their PASS.

Existing `CityIdentityMapping.lua` / `CityIdentityExperiment.Shadow` provide a **separate E1 experiment**, with saved event-backed reference evidence and typed ownership events (including CityConquered). Its accepted native scope is a single free-city transition, not this two-transition trade/conquest sequence. This is a reusable investigation lead, not permission to promote that experiment to gameplay authority or invent a new cityKey. No names, standalone coordinates, guessed IDs or token copying may bypass identity proof.

## Validation disposition

- Cold-load of this foreign-held save: USER_GAME_TEST_PASS for load and displayed retained progression. Earlier in-session load crash remains a separate unresolved failure; not proof all hot loads fail or crash is fixed.
- B096 exit registration/readback after cold-load:23/23 observed, with visible research carriers absent and old network membership absent. Broader native Modifier removal and immediate transfer completion remain unproven.
- B097 conquest recapture: USER_GAME_TEST_FAIL for restoring accessible progression in this attempt; exact identity/event rejection unobserved.
- Post-return ACTIVE recomputation, current-route Network rebuild and accepted-recapture save/load: BLOCKED / NOT_VERIFIED. Do not certify them from absence of a restored state.
- No Claim/F gate opened. No Design decision required by this evidence.

## Recommended next bounded scope (not implemented)

Correct owner-safe diagnostic lookup and expose the existing per-module exit failure, transfer arguments, candidate/live token and rejection reason on demand. Inspect/validate conquest event evidence against the saved HELD reference before proposing any recapture identity adaptation. Do not ask the user to repeat a full loss/load cycle merely to reproduce the already established failure; a post-conquest E2 report can supplement the current evidence if available. Any production repair requires separate authorization. Preserve permanent records and refuse ambiguous identity throughout.
