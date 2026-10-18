# B233.260 — Industry completion history and typed template knowledge

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Approved IND-1 only; no new Industry effects.
Pre-change checkpoint: `fa8df2f` (source/live B232.259). The user authorized B233 and selected a new campaign for Industry validation.

## Delivered boundary

- `Mod/IndustryHistory.lua` records supported-player native `Events.WonderCompleted(x,y,buildingIndex,owner,cityID,...)` into one Game Property. Foreign events return before any city lookup or write. A completion receipt has its original completing owner, city reference, proven Store token when available, Wonder plot, own era and completion turn. City N and civilization E are read projections, not separately mutable counters. No requirement for Industry, ACTIVE or a governor at completion.
- Own era is resolved through the Wonder's prerequisite technology/civic and `Eras`. Unknown metadata stays UNKNOWN. The configured read-only DB has 53 non-internal Wonders, all globally unique and all with resolvable own eras; the single-Wonder-type receipt key rejects an unsupported non-unique definition rather than silently conflating it.
- Startup reuses Store's confirmed pristine-start status. Existing saved history is structurally restored; missing old history is marked unavailable, not complete zero. No DWR data is imported; current possession never supplies civilization E. The external Mod supplied an API lead only.
- A receipt write uses expected-value comparison and native readback before publishing. Reentrant distinct completion events drain synchronously once; duplicate Wonder IDs retain original attribution. A failure holds the module. One bounded attempt marks the **actual valid readback** coverage unavailable without replacing corrupt data or replaying a completion. If storage cannot retain that protection, the report explicitly requires a pre-event save; local tests do not claim crash/power-loss durability.
- H1 adds a separately typed `districts` component under the existing city template record. Accepted District families and native unique replacements normalize to the base type. Completed Districts are unioned at legal initialization/re-entry and targeted completion; old building rows and revisions are unchanged. Removing a current building/District never deletes recorded knowledge.
- `templateLifecycle.districtsKnown` and the typed component commit atomically. Missing established knowledge remains held. A legacy building-only record may only label newly observed Districts as `PRESENT_AT_ADOPTION`, never fabricated complete pre-adoption history; this is not a compatibility promise for old test saves.
- AF23 integration: Store return uses structural/provenance validation. Today's catalog cannot erase old knowledge or prevent Identity restoration. The unchanged legacy discount consumer retains strict catalog checks and remains building-only; District rows do not activate discounts.

## Ownership, event scope and limits

The existing Store remains the only city identity authority. Its read-only historical reference supports active registered cities; original-owner return uses the existing proof across changed cityID. During implementation, the user clarified that foreign completion tracking is unnecessary: conquest/Industry entry should inspect the acquired city instead. The unpublished foreign-recording path was removed before commit.

Lawful Industry initialization/claim, re-entry and load readiness reuse Standardization's single-city entry. N is the union of reliable retained completions and presently existing Wonders. Reconciliation observations are token-bound and never create completing-owner/era credit. Repeated scans are idempotent; missing current buildings never erase recorded N. Foreign completions and unobservable foreign construction/removal are not recorded or reconstructed. Saved corrupt authority remains held, rather than silently replaced by a scan. A Wonder-history failure does not block ordinary building/District template recording.
History normal work is one completion callback and a bounded-by-Wonder-catalog atomic receipt copy; there is no turn/world Wonder scan. A cached Wonder definition list is checked only for the entering/restored Industry city. A session readiness bit suppresses repeated scans after confirmation; failure leaves it retryable through existing events/load, without a new persistent queue or timer. N/E lists/text are built only for the read-only report. Template initial/re-entry scans are single-city; ordinary District completion resolves that event's city and type. Existing bounded event-publication retries and turn reconciliation remain; no timer/frame polling or GC change is added. The existing diagnostic ring/budget is reused, with scalar `INDUSTRY_*` entries; collector tools are unchanged.

## Local verification

All results below are local evidence, not native acceptance or CPU/memory improvement:

| Check | Result / covered delta |
|---|---|
| `test_industry_history.py` | 25 tests PASS; actual Store/History/Standardization sources, completion before specialization/ACTIVE, own eras, repeat/reentrant notifications, foreign event exclusion, actual Store claim with present-Wonder N/no E, loss/return with new cityID and local union, cold load, known empty/missing/corrupt, readback failure/coverage hold, UI read-only/idle, typed normalization/partial Districts, catalog drift and effect isolation |
| Inherited B140 inside that suite | Original assertions retained, with native-shaped District fixture additions only; first initialize, reconcile union, no reverse deletion, missing/corrupt guards, Claim/return, unrelated-city isolation and actual legacy discount plan/carriers |
| `test_industry_catalog.py` | 2 tests PASS against configured read-only DB; 53 Wonder / 0 unknown era / 162 building-template rows; actual replacement normalization; inherited B142 Tier 0, missing history, catalog and discount assertions unchanged |
| `test_store_write_boundaries.py` | 18 tests PASS, including frozen-baseline per-value comparison and normal-write uniqueness visits remaining zero (8/20/40 records); no new native performance claim |
| Existing trace reader + collector | 59 offline tests PASS; first sandboxed run could not create fixture directories under ignored `local/`; rerun with the necessary filesystem access passed, no assertion or tool changes |

Total: 104 unittest tests; inherited multi-case assertions are not counted a second time. Lua/XML/SQL registration, changed links, current manifest/schema/selectors, hashes and diff/publication review are checked at the coherent checkpoint. The context helper only gains the `P0-GH1` CLI choice for the new manifest; schema, selectors, validation policy and authorization logic are unchanged. No gameplay full regression or game launch.

## One new-save native session

Use B233.260 loaded from campaign creation, with the normal manual collector running. Select an owned city and click **工业历史 / 模板** in P0; this button only reads and logs, never starts collection.

1. Before this city becomes Industry, finish one recognizable Wonder through normal production completion (Cheat acceleration is acceptable; do not seed a saved Property). Confirm **N=1**, and **E=1** for its **own** era if this is the civilization's first completed Wonder. Other cities' completions may raise E; compare the era list rather than expecting 1 blindly. This tests the new native event and attribution.
2. Give that same city a lawful Industry identity (e.g. complete Industrial Zone as its first specialization District). Confirm the Industrial Zone District template and existing ordinary-building templates. Finish one further eligible District, e.g. Campus; confirm one additional District template. No investment or governor is needed for collecting knowledge. This tests the new typed/native District path; it is not a discount test.
3. Save and fully restart once, reload, then read **工业历史 / 模板** in that city. N/E, era set and both District records must remain. New persistent fields justify this one cold-load check. No repeated OFF/ON or long session is required.

The report's key N/E/coverage/template counts and completion receipts are logged automatically. Screenshots are needed only for an unreadable/mismatched report. Stop and retain the log/save if history is held or a write is unconfirmed. Existing unrelated native gates remain on HOLD.

## Checkpoint and next gate

Source/live build: B233.260 / modinfo260 from `b82eabf216810017d56c350e03ccf631bde505ea`. W0003 receipt `B233.260-b82eabf-playtest.json` confirms227/227 files MATCH, digest `0530efdf3e1b3da3f153ed45aac8642a39c9e05a9356c5b12fae6c52eb3662e1`. OS checks confirmed game exit before both switches; outgoing B232/stable recovery retained and no pending transaction. No game launch or native acceptance. Main, Design, GC, saves, game configuration, original Advisor/audit evidence and unrelated Culture mechanics are unchanged.

User decision: none inside IND-1. User testing: the single new-save flow above, on the verified deployed package. Primary next: stop at this batch; review its native result, then propose/authorize IND-2 (III standardization + exact old-writer cutover), not automatic implementation.
