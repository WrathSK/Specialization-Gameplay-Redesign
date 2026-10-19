# B249 native review — Training, disruption and configuration

Date: 2026-10-18 (America/Vancouver; collector filenames use 2026-10-19 UTC). Reviewed develop HEAD `22e9722`; unchanged source/deployment **B249.276 / modinfo276**, implementation `ad34b1f`. **USER_GAME_TEST_PASS for the observed same-turn training unlock, liquidation, disruption, manual configuration and new-profession effect cases.** The originally planned cold load while REALLOCATING remains **USER_GAME_TEST_REQUIRED**; this submission does not contain that recovery case.

## Accepted results

The user confirms that the prior city was deliberately left at ACTIVE III to check same-turn unlocking. In this run the existing commercial city starts at Potential IV / ACTIVE III, then reaches ACTIVE IV in the same T3. The native list changes from no permission to one selectable restructuring team with cost500. The B249 initializer is ready before the UI load-close event; the earlier missing startup is no longer the blocker in this observed session.

| Result | Logged evidence | Acceptance scope |
|---|---|---|
| Same-turn unlock | seq18: Potential4 / ACTIVE3, no marker; seq43: ACTIVE4 and marker present; seq47: native visibility and eligibility true, one list item, cost500; all T3 | USER_GAME_TEST_PASS for this transition. The cost is a native quotation, not independent measurement of normal multi-turn Production spending. |
| Training and source binding | seq48: one REST_TRAINED / AVAILABLE for source city65536 | A training completion has a confirmed team binding. No claim about whether completion was natural or accelerated. |
| Liquidation | Target city131073 has Culture Potential2 at seq51; seq55 at T3 records REALLOCATING / NONE / Potential1, started3 and due8; seq56 records ACTIVE0 / Potential1 | One permanent Potential debit and current-identity exit are observed. The same team key links training, liquidation and configuration. |
| Disruption | The user verifies -75% other yields and -75% surplus Food | USER_GAME_TEST_PASS from explicit manual observation. The trace does not contain numerical native yield or surplus measurements; configured state alone is not used as yield proof. |
| No automatic configuration | Target remains NONE / ACTIVE0 / Potential1 at T8 seq104/107 and T9 seq114/116; configuration occurs only at T9 seq121 | Five elapsed turns make manual configuration possible; they do not restore the city automatically. Actual completion is six turn increments after T3. |
| Illegal targets | The user verifies that a non-eligible district such as an Encampment cannot confirm configuration, and a Potential1 city cannot be liquidated | USER_GAME_TEST_PASS from manual observation. There is no per-attempt rejection event in this trace, so the specific attempted tiles/clicks are not reconstructed from missing log entries. |
| Successful configuration | seq121: REST_CONFIGURED / SETTLED / INDUSTRY / Potential1; seq122: Industry ACTIVE1 / Potential1 | The one team completes the same target's transaction. The event is emitted after native unit removal/readback, consumption receipt, Store finalization and disruption-marker removal/readback in the unchanged source. |
| New profession effects | T9 seq123/132: network AVAILABLE; seq124: Industry history reconciled; seq125/135: district templates committed; seq126/136: Industry support VERIFIED | The user confirms the new profession's abilities work. The trace corroborates same-turn publication and owned support updates; it is not an independent measurement of every Industry yield. |

Only one REST_TRAINED, one REST_LIQUIDATED and one REST_CONFIGURED occur in the captured sequence. The configuration retains the original post-liquidation Potential1. A later same-turn observation at seq133 shows Industry Potential2; that subsequent change is outside the liquidation debit comparison and is not mislabeled as another configuration or debit.

## Log and source cross-check

The submitted session contains **136 unique records, seq1–136 without gaps**, T3–9, one Gameplay context and one UI LOAD_CLOSE. There is no REST_INIT_HELD, REST_SYNC_HELD, REST_TRAINING_HELD, REST_REQUEST_HELD or REST_PUBLICATION_HELD. Collector reconnects do not create additional Gameplay contexts and are not evidence of save/load.

The eight CAPITAL_FAILURE observations are COMMERCE_PENDING refresh-dependency waits during startup/network revalidation. Subsequent Commerce READY and network AVAILABLE records appear, including seq130/132 after the last wait. They do not prevent the observed restructuring transaction. Two CREW_PRECISION UNKNOWN observations provide no construction injection result and are not promoted to a Crew regression or PASS. No unrelated repair is opened.

Direct review was limited to the current restructuring contract, `Restructuring.lua`, `RestructuringModel.lua`, the current startup result and Industry support trace semantics. `REST_ACCESS.expected` means ACTIVE and `count` means Potential; `REST_LIQUIDATED` / `REST_CONFIGURED.expected` means retained Potential. These fields are decoded by their actual emitter, not by their generic names. Native permission is read independently by the existing production-list observer.

The unchanged implementation checks the target's current specialty district and Potential>=2 before liquidation; configuration checks the same target city, a different supported complete/unpillaged specialty district and the five-turn minimum. The emitted SETTLED event follows confirmed unit consumption and effect-marker withdrawal. These code facts explain the trace, while the user's observations establish the stated illegal-action and real-yield results. The80 selected local methods from the [B249 startup result](Specialization_B249_Restructuring_Startup.md#local-verification) are inherited without rerunning or reclassifying them as native evidence.

## Remaining validation boundary

This run proves the continuous-session core flow. It does not show a new Gameplay context restoring an already REALLOCATING transaction, REST_RESTORED, or a user-confirmed cold restart while restructuring. Keep that **one original pending recovery case**; do not repeat the accepted unlock, yield, illegal-target and waiting checks merely to fill another test session. When convenient, a saved in-progress transaction can supply the existing cold-load check: same team/target, retained Potential, disruption and remaining wait, followed by normal manual completion. This validates the new transaction/reconstruction path, not the unchanged general Probe lifecycle.

Target conquest, hostile-contact retreat, all other profession histories and signed-contract combinations receive no new native PASS from this run. Their existing local evidence and task boundaries remain unchanged; no expanded native matrix is requested. B246's separate optional Standardization combination and held Culture work are also unchanged.

## Evidence retention

Original files remain unchanged and Git-ignored under `local/diagnostics/B205/session-20261019T061229Z-e05aa9/`. This is a local locator, not a public evidence download. The review relies on these logs and the user's explicit observations; no screenshot is required or claimed to have been re-inspected.

| File | Bytes | SHA256 |
|---|---:|---|
|records.log|45361|`0d7e03f20120213d2d3d36d56c944e1e7a01a6b274b81e6edab44f1cff2e8f3a`|
|events.jsonl|2555|`e092553d4c0eff426d6b06227c662afec576de870c38f68ea3d65fb77d168869`|
|summary.txt|647|`0f5cfdeea0b85dc616de531eed13874027b8b14d0961ee22be8e382b0294f357`|

## Checkpoint

The B249 startup/same-turn access repair and original B247 continuous restructuring flow are accepted within the observations above. No implementation defect is identified in this run. Source and the recorded deployment stay B249.276 from `ad34b1f`, receipt `B249.276-ad34b1f-playtest.json`; this review performs no deployment or live game query. Main/stable B069.96, Design, Architecture, tests, source, configuration, GC and frozen earlier evidence remain unchanged. Only this new result and current Status/navigation/review metadata are updated.

User decision: none. User testing: retain the one original REALLOCATING cold-load check for a convenient session; no repeat of completed steps is requested here. Primary next: document/reference/context/publication checks, normal develop commit/push, then stop without another implementation batch.
