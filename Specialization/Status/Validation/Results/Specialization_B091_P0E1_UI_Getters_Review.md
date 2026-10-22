# B091.118 UI getter evidence — scoped native PASS

Two screenshots T8 at22:47:17/22:48:32 reviewed and hash-archived. Both show original ref0/131073 and current ref62/65536, experiment DEV-B013-P0-2. Both are post-transfer current-state observations; neither shows owned-city pre-transfer UI watch. Actual intervening actions/reload are not inferred from backgrounds.

| UI getter | Both screenshots |
|---|---|
| GetOriginalOwner | 0[number] |
| GetOwnerBeforeOccupation | 62[number] |
| GetJustConqueredFrom | -1[number] |
| GetLastTransferType | -738490196[number] |

UI API readability = USER_GAME_TEST_PASS for this Free City scene. This supports context-dependent availability compared with B090 Gameplay UNKNOWN; the earlier Gameplay diagnostic did not distinguish missing method from error/nonnumeric values, so exact Gameplay failure subtype remains unobserved.

OwnerBeforeOccupation equals current Free City owner62, not watched prior owner0. It cannot substitute for immediately previous owner in this path. JustConqueredFrom=-1 is a raw value, not owner0 evidence. Transfer type is a numeric value; do not label the enum without verified mapping. Its equality to B088's fourth CityTransfered argument is a cross-run correlation only, not a general event-signature proof.

Both UI event counts are0. Observer only watches after first explicit UI read in a load. This evidence does not establish whether the watcher was active at transfer, or whether any event fired. No event absence/failure PASS/FAIL assigned. No persistence conclusion added beyond B090. Identity gate remains HELD; no migration/E2/F.

If event evidence is pursued next, a pre-transfer save with current owner0 is needed: establish experiment if necessary, right-click 实验对照 BEFORE transfer (verify current0/131073), then transfer and right-click same load/turn. No need to repeat this merely to verify getter availability, which is already confirmed. No code/deployment/game launch in this review.
