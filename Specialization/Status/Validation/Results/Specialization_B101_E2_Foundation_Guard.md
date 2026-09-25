# B101 E2 recapture: over-broad CityBuilt guard — 2026-09-25

Two reviewed screenshots (07:01:50,07:02:07) hash-archived under external app-support Specialization/Status/Validation/Evidence/B101_E2_Foundation_Guard_20260925. No runtime edits/deployment/game interaction in this review.

## Observed

B101.128 ACK T13 HELD_TRANSFER rev3. Origin0/262146 @28,34 token DEV-B013-P0-3; current0/327682 @28,34 token nil/MISSING. RESEARCH Potential2 investment1 retained. Saved foreign target3/131073. Exit TARGET_UNAVAILABLE but completed23/23, checked2322/removed0. Return and transition both RETURN_NEW_FOUNDATION, candidate0/327682 from3. Support/housing/GPP0/0/0; old/current source/receiverfalse/routes0; NO_CURRENT_INPUT. Second report fails with PROGRESSION_HELD at CityProgressionStore active/Base, as expected while acceptance is denied.

Actual last-event order, all T13:

- #18 GameEvents.CityConquered(0,3,327682,28,34), argc5.
- #19 CityRemovedFromMap(3,131073), argc2.
- #20 CityAddedToMap(0,327682,28,34), argc4.
- #21 CityInitialized(0,327682,28,34), argc4.
- #22 CityTransfered(0,327682,3,-1173539618), argc4.

This adds typed conquest evidence before removal. Latest slots are not a complete event history. CityBuilt itself is not in the diagnostic event slots, so its precise arguments, timing and emitter are not directly shown.

## Cause and limits

STATIC_CONFIRMED: RETURN_NEW_FOUNDATION has one assignment in CityProgressionStore.track: any CityBuilt whose x/y equal saved foreign target sets a latched transitionFault. That function is wired to GameEvents.CityBuilt. Recapture checks this fault before the withdrawal-completion assertion. Therefore **the reported blocker is not earlier22/23**; the screenshot displays23/23 and rejects at the foundation guard before checking it. TARGET_UNAVAILABLE only describes the now-departed foreign reference.

The current rule assumes CityBuilt at the target proves a new foundation, but this actual conquest session contains a matching typed conquest and subsequent endpoint chain while the guard has latched. B101 therefore cannot distinguish a conquest-associated CityBuilt signal from a genuine new foundation and rejects the user scenario. The first-party implementation made that insufficient semantic assumption; do not attribute the failure to user operation or ask them to replay the old incomplete exit.

Read-only source search: no CityBuilt emitter found in canonical Mod. Installed Workshop Lua search found HD Gameplay/Misc.lua and CityCanalRework.lua subscribers, not a demonstrated emitter. Native engine versus another source and exact CityBuilt timing remain unconfirmed. Do not claim HD caused it or claim CityBuilt always fires on conquest.

USER_GAME_TEST_FAIL for B101 acceptance in this scene. Permanent displayed state is retained. Current ACTIVE/Network rebuild and accepted-state save/load remain blocked. Earlier22/23 has independent unresolved history but is not the rejection shown here.

## Next scoped repair proposal (not implemented)

Use the now-observed GameEvents.CityConquered typed tuple (new owner, former owner, new ID, location), saved foreign reference and matching removal/add/init/transfer chain to disambiguate this conquest. Capture CityBuilt evidence rather than treating its name alone as an unconditional new-foundation veto. Do not simply delete new-foundation protection: genuine founding without matching typed transfer/conquest evidence, conflicting endpoints, multiple transitions and ambiguity must still reject. Keep event state bounded and do not copy tokens or enter Claim/new cityKey/global migration. Add a test where the exact conquest chain coexists with CityBuilt; current local foundation-rejection test intentionally models CityBuilt as a stop and did not model this native coexistence.

No need to load the pre-trade save or repeat withdrawal now. Keep existing foreign-held save. Await authorization for this narrow event-classification repair before another native test/deployment.
