# B092.119 P0-E1 event shadow — native evidence

Evidence: USER_GAME_TEST_PASS for the observed single Free City transfer shadow only. Not full P0-E1 identity or migration acceptance.

Four screenshots, all T8 / DEV-B013-P0-2, reviewed visually and archived with 4/4 SHA256 equality; see adjacent `Specialization_B092_P0E1_Shadow_Evidence.json`. Source/runtime unchanged.

| Capture | Observed result |
|---|---|
| 23:00:10 Gameplay before | Origin/current 0/131073; ORIGIN_RECORDED revision1; live/saved events0; shadow HELD because reference unchanged (expected). |
| 23:00:13 UI before | Origin/current 0/131073; OriginalOwner0; OwnerBeforeOccupation0; JustConqueredFrom−1; LastTransferType1634873444; UI events0. |
| 23:00:32 Gameplay after | Origin0/131073 → current62/65536; stored HELD revision2; live/saved events6; no overflow; **SHADOW_CANDIDATE**. |
| 23:00:41 UI after | Same references; OriginalOwner0; OwnerBeforeOccupation62; JustConqueredFrom−1; LastTransferType−738490196; UI events2. |

Gameplay event order exactly as displayed:

```text
CityBuilt T8 (62,65536,28,29)
CityRemovedFromMap T8 (0,131073)
CityAddedToMap T8 (62,65536,28,29)
CityInitialized T8 (62,65536,28,29)
CulturalIdentityCityConverted T8 (62,65536,0,24576)
CityTransfered T8 (62,65536,0,-738490196)
```

UI independently displays the last two events with matching arguments. Extra event arguments remain uninterpreted.

## Meaning and limits

- Direct Gameplay receives the typed oldOwner-bearing signal, origin removal and current reference/location evidence. A UI→Gameplay sample bridge is unnecessary for this observed path; UI is corroboration only.
- Stored HELD is the old getter-based conclusion, deliberately separate from the new read-only shadow. It is not an experiment pause or shadow failure. No binding/ledger migration or gameplay benefit follows SHADOW_CANDIDATE.
- CityBuilt precedes CityRemovedFromMap here: event names alone do not establish refoundation. This actual order works for the observed shadow.
- B090 previously demonstrated independent Game-record persistence through transfer/load. These four images do not test persistence of the shadow (it is not saved), formal migration, reconquest, repeated transfer, gifting, liberation, raze/refound or loading mid-transfer. Do not combine separate experiments into universal identity proof.
- No need to repeat these four captures. Next recommended work is a bounded E1 support-boundary / persistent identity mapping plan for review. No new implementation, cutover, E2/F or deployment is authorized by this evidence record.
