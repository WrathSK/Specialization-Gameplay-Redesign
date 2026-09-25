# B100 E2 conquest return: live binding absent — 2026-09-25

Screenshot 06:46:03 reviewed and original hash-archived to external app-support Specialization/Status/Validation/Evidence/B100_E2_Recapture_Token_20260925. Game still running per latest user statement; no runtime change, deployment or game interaction.

## Native evidence

B100.127 ACK, T13, HELD_TRANSFER rev3. Origin0/262146 @28,34, original DEV-B013-P0-3. Current0/327682 @28,34, token nil, MISSING. Permanent RESEARCH Potential2 investment1 retained. ACTIVE inactive/UNKNOWN. Saved loss3/131073 @28,34. Return RETURN_IDENTITY_UNCONFIRMED, candidate0/327682 from3. Game conquest notification identifies Washington captured by player's unit.

Displayed last-event sequence (all T13):

1. #18 CityRemovedFromMap(3,131073), argc2.
2. #19 CityAddedToMap(0,327682,28,34), argc4.
3. #20 CityInitialized(0,327682,28,34), argc4.
4. #21 CityTransfered(0,327682,3,-1173539618), argc4.

Fourth transfer argument remains uninterpreted. Latest slots are not a complete event log; the visible order/endpoints agree with saved foreign reference and current native object. No CityConquered row is displayed; this is not evidence that the engine emits no conquest-specific event.

Exit TARGET_UNAVAILABLE, completed23/23, checked2322/removed0. Research support/housing/GPP0/0/0. Network VERIFIED epoch1 input1 derive1, old/current target sourcefalse/receiverfalse/routes0; NO_CURRENT_INPUT. These are absence/readback facts, not proof accepted return or new Network rebuild.

## Confirmed blocker

STATIC_CONFIRMED + USER_GAME_TEST_FAIL (actual return does not restore accessible progression): CityProgressionStore.recapture passes its matching-event preconditions and sets the observed candidate, then asserts local-human qualification and equality of the live City token with root.base.token. The ACK report also passes the same player eligibility gate. Live token nil cannot equal the saved nonnil token; RETURN_IDENTITY_UNCONFIRMED is therefore explained by the missing live binding. **Missing CityTransfered delivery is ruled out for this attempt.**

B097's success mock retained token across loss/return; that conditional simulation does not cover this native behavior. The unchanged rev3 and displayed permanent values support retained authority, not data deletion. ACTIVE/Network recalculation have not run through an accepted return and remain unverified.

TARGET_UNAVAILABLE is separately explained by ExitConfirmed: it refuses a current object that no longer equals the saved foreign loss.target. Now0/327682 is not3/131073. Completed23/23 remains retained. This label does not mean a previously completed exit regressed to failed removal and must not trigger broad cleanup of the recaptured city.

Diagnostic limitation found during review: B100 observes Events.CityConquered, whereas the existing E1 experiment hooks GameEvents.CityConquered. The former has no row here; do not use that absence to assert the latter did not fire. This observation gap does not obscure this attempt's actual token rejection, since CityTransfered and matching candidate are present. No hook changed in this evidence-only turn.

## Next bounded proposal, not implemented

Adapt recapture identity proof around the existing persisted foreign reference and a strictly validated native transition chain, instead of assuming City property token survival. First define exact acceptance/ambiguity/reload boundaries using the observed remove/add/init/typed transfer evidence; preserve immutable historical records and require sufficient joined evidence. Coordinates alone, names, guessed old IDs and automatic token copying remain forbidden. Existing E1 mapping is an investigation reference, not automatically gameplay authority. No new cityKey/global migration/Claim/F or Design change authorized.

This native sample supplies concrete evidence for a narrow plan; it does not certify a general resolver or all conquest/load sequences. Retain refusal on incomplete/conflicting evidence. Existing ACTIVE/Network current-facts derivation must remain after identity acceptance, with no old snapshot replay. Do not ask for another repetition of this already diagnosed transfer simply to reproduce missing-token behavior. A repair and its local acceptance must precede the next minimal user test.
