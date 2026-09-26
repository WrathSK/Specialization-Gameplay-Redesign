# B105 E2 — native event sequences / Publish interleaving

Evidence: four screenshots captured 2026-09-25 23:26:51–23:27:56, all B105.132, Turn13, page1/1. Originals visually reviewed and archived externally under app-support `Specialization/Status/Validation/Evidence/B105_E2_Event_Boundary_20260925`; manifest.json records original names and 4/4 SHA256 equality. No source/runtime change or deployment in this review.

## Native observations

Images1/2: selected Settler before founding and resulting city New York, position25,31. Image1 contains Start EMPTY only. Image2 contains the full displayed trace:

```text
1 Start EMPTY
2 Built 0 / 393219
3 Publish CITY / 0 / 393219
4 Added 0 / 393219
5 Initialized 0 / 393219
6 Publish CITY / 0 / 393219
7 Playback CITY / 0 / 393219
```

Images3/4: selected own EDINBURGH (TEST), position28,29, then transfer from player0 to player4, matching the requested gift test. Image3 contains Start CITY / 0 / 131073. Image4:

```text
1 Start CITY / 0 / 131073
2 Built 4 / 131073
3 Publish CITY / 4 / 131073
4 Removed 0 / 131073
5 Added 4 / 131073
6 Initialized 4 / 131073
7 Transfer 4 / 131073 / 0 / -1821839791
8 Publish CITY / 4 / 131073
9 Playback CITY / 4 / 131073
```

No Conquered, ReadRequest, missing-hook, observer-error or trace-limit row is shown. Header reports Publish/Playback/Transfer listeners true; actual rows additionally establish delivery. The transfer reason hash is recorded verbatim, not independently decoded. The pictures establish ownership change; the trade-dialog operation itself is not pictured. City ID numerically stays131073 in this transfer; this is not a general CityID preservation guarantee.

## Evidence and decision

**USER_GAME_TEST_PASS (scoped observer)**: manual start and subsequent event/boundary capture work for these two sequences, including foreign-held readback. This is not full E2 enrollment PASS.

**NATIVE_OBSERVED / EVENT_BATCH_BOUNDARY**: the first Publish occurs after Built but before Added/Initialized in both cases; in transfer it is also before Removed/Transfer. At this early Publish, city lookup already reports the new owner. Thus neither first Publish nor a current city object proves delivery of the complete ownership lifecycle. A current snapshot may be ahead of notification delivery. This directly rejects the proposed first-Publish-as-completion assumption, rather than leaving it merely untested.

The user's correlated-sequence idea remains useful: a transfer has positive old/new-owner evidence and an explicit Transfer later in the sequence. Built alone remains ambiguous. Playback follows the shown chains and second Publish, but two samples do not prove it is a universal Gameplay transaction boundary. No ReadRequest occurs, so these captured boundaries are not first introduced after the observer's manual read marker. This does not exclude unrelated engine/mod operations as sources of Publish.

No destruction/rebuild, conquest-with-publish-markers, save/load or new authoritative enrollment was tested here. Existing B103/B104 results stand. No inference from absence of a following event to confirmed destruction or genuine founding is authorized.

## Next narrow step

Do not repeat these two tests. Keep automatic fresh enrollment OFF at the plan's explicit stop condition. Revise the classifier proposal around positive transfer-completion evidence; for genuine founding, investigate positive native founding/Settler-operation evidence or a documented stronger completion boundary. Treat Playback-after-chain as a candidate, not a proven guarantee; do not replace the failed assumption with a fixed delay, counting Publish notifications, polling, name/coordinate identity or token copying. Keep destruction/rebuild retirement closed until its own evidence is sufficient.

No new Design decision is identified. A scoped technical plan update is the next action for review; no implementation, Claim, F or deployment is performed by this evidence review.
