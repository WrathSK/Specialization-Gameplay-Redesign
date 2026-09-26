# B106 E2 — FOUND_CITY native evidence / scoped PASS

Two screenshots delivered by user, captured 2026-09-26 04:24:28 and04:24:55. Both show B106.133, Turn13, page1/1; no missing page, missing-hook warning, error, overflow or ReadRequest. Originals visually reviewed and archived with2/2 SHA256 equality under external app-support `Specialization/Status/Validation/Evidence/B106_E2_Found_City_Pass_20260926`; manifest.json retains filenames/hashes. No runtime/Design/deployment change in this review.

## 1. Founding positive evidence — position25,31

Header: Gameplay, UnitActivate=true, FOUND_CITY=-1828126782, starting Settler1114117. Full displayed order:

```text
1 Start EMPTY
2 Built 0 / 393219
3 Publish CITY / 0 / 393219
4 Added 0 / 393219
5 Initialized 0 / 393219
6 FoundCity 0 / 1114117 / -1828126782 / true
7 Publish CITY / 0 / 393219
8 Playback CITY / 0 / 393219
```

The signed reason equals the engine enum read by the observer. Activation owner0 and unit1114117 match the manually selected own Settler used to arm capture. The event passes the location filter at25,31; it arrives after Initialized and before the next Publish in this sample. It is delivered in Gameplay, not relayed from UI. Unit ID1114117 is not city ID393219. We did not query whether the unit still exists at callback; this remains unmeasured and is unnecessary for scalar evidence capture.

## 2. Transfer negative control — position28,29

Header: UnitActivate=true, same FOUND_CITY enum, no starting Settler. Full displayed order:

```text
1 Start CITY / 0 / 131073
2 Built 2 / 131073
3 Publish CITY / 2 / 131073
4 Removed 0 / 131073
5 Added 2 / 131073
6 Initialized 2 / 131073
7 Transfer 2 / 131073 / 0 / -1821839791
8 Publish CITY / 2 / 131073
9 Playback CITY / 2 / 131073
```

The requested trade-control trace shows local owner0→owner2, no FoundCity or UnitActivate row at that location. This is one observed negative control, not proof of absence for every possible transfer variant. The trade dialog is not pictured; the ownership transfer itself is explicit. Numeric city ID happens to stay131073, not a universal stable-ID guarantee.

## Conclusion / exact scope

**USER_GAME_TEST_PASS** means the user has natively validated this checkpoint's Gameplay event delivery and distinguishing signal in the tested founding and transfer pair. Startup enum is available; real FoundCity is captured with matching pre-observed Settler identity/location. This closes B106's minimal evidence gate. No repetition needed.

B105's rejection of first-Publish completion still stands. The successful route is positive founding evidence plus a current-city/initialization match, not waiting until no transfer arrived. This supports a narrow registration implementation proposal. It does not certify that automatic registration already exists, that Initialized always precedes FoundCity, or that transferred cities can never emit this reason under every engine/mod path.

Unverified here: automatic pre-founding Settler observation (manual arm supplied it), completion-before-registration sequencing, new NONE/P0 persistence and first specialization completion, duplicate application, load interrupted between evidence stages, conquest/raze/rebuild with this signal, and all third-party/script-created city cases. Keep these as bounded implementation/local validation concerns; do not require the user to repeat unrelated B103/B104 tests. Existing B103 recapture and B104 two-city results remain valid in their scopes. No confirmed-destruction inference or historical-record overwrite.

## Next proposal, not implemented

Revise the authorized fresh-city slice to consume a matching positive FOUND_CITY reason and actual local-human city reference, with bounded correlation and deduplication; preserve the successful transfer path. The plan must explicitly remove the manual-arm dependency and handle either delivery order, missing/conflicting evidence, old-location history conflicts, and early district completion without guessing identity. Read the enum, never hardcode the observed hash. Do not require the Settler object to survive its own founding action.

No new Design decision is identified. No immediate user test requested. Prepare the narrowed registration/cutover plan for review; do not automatically implement registration, Claim, new cityKey, general migration or F on a screenshot submission.
