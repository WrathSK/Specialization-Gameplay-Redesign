# B102 E2 chain-order rejection — 2026-09-25

Two reviewed images07:12:46/07:12:58 archived with matching hashes in external app-support Specialization/Status/Validation/Evidence/B102_E2_Chain_Order_20260925. Local reproduction output copied separately, explicitly not a native log. No source/runtime edits or deployment.

## Native observations

B102.129 report current0/327682 @28,34 token nil; retained RESEARCH Potential2 investment1. Exit23/23, checked2322/removed0, TARGET_UNAVAILABLE for departed foreign3/131073. Return/candidate: RETURN_CHAIN_ORDER,0/327682 from3. CityBuilt pending conquest comparison. Current ACTIVE inactive/UNKNOWN; carriers0/0/0, Network VERIFIED epoch1 input1 derive1, old/current sourcefalse/receiverfalse/routes0, NO_CURRENT_INPUT. Top lines of the first report are clipped; do not invent hidden revision/header contents. Second report PROGRESSION_HELD at active/Base confirms acceptance did not occur.

Displayed per-type latest events, T13:

1. #18 CityBuilt(0,327682,28,34).
2. #19 CityConquered(0,3,327682,28,34).
3. #20 CityRemovedFromMap(3,131073).
4. #21 CityAddedToMap(0,327682,28,34).
5. #22 CityInitialized(0,327682,28,34).
6. #23 CityTransfered(0,327682,3,-1173539618).

These latest events are correctly ordered for B102. They do not expose earlier overwritten same-type notifications. Again this is not22/23 or RETURN_WITHDRAWAL_UNCONFIRMED.

## Reproduced defect / evidence boundary

CityProgressionStore.track currently sets RETURN_CHAIN_ORDER for any CityAddedToMap/CityInitialized at the tracked location when no transition removal has started, before determining whether it is merely the saved foreign-held object appearing during load. transitionFault is latched and survives a later valid removal/add/init/transfer chain. Thus a load-time object hydration notification can poison a future legitimate recapture.

Actual-runtime local reproduction (read-only runpy fixture; no repository edit): run existing test_p0_e2_recapture/B101 fixture, then held(); Events.CityAddedToMap.Fire(62,40,4,5); matching CityBuilt + CityConquered; removed(); added(); initialized(); transferred(). Result HELD_TRANSFER/RETURN_CHAIN_ORDER. Identical control without the pre-transition foreign add gives ACTIVE. Both assertions passed. This demonstrates a lifecycle initialization bug, not just a suggested hypothesis. Existing B102 tests varied CityBuilt timing but did not deliver saved foreign-city add/init hydration before the transition; that omission allowed the defect to pass local acceptance.

The native screenshot's earliest fault-producing notification is **not directly retained**, so exact native trigger remains inferred, supported by the reproduction and correct latest chain. Do not label the entire native call history proven. No evidence of permanent data loss or renewed memory incident. USER_GAME_TEST_FAIL for B102 return; accepted-state ACTIVE/Network/save-load remain unverified.

## Next bounded correction, not implemented

Separate baseline foreign-object hydration from an actual in-progress ownership transition. Exact saved foreign reference add/init notifications before removal must not latch an order error. Keep rejection of genuinely premature original-owner candidates, conflicting references, new foundations and broken in-progress chains. Do not blindly clear every prior error upon removal. Add cold-load foreign add/init permutations and repeated-load notifications to the real-store acceptance tests, then replay the complete screenshot sequence; retain ambiguity/withdrawal/current-facts gates. A bounded explanation of the first fault would prevent latest-event snapshots from obscuring its cause. No token copying, Claim/new cityKey/global migration or Design changes.

Do not request another repeat of the current native scenario before fixing and verifying this gap. Preserve the existing foreign-held save. This turn records the failure only; implementation/deployment await authorization.
