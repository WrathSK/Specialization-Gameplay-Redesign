# B229 — Retained network waiting evidence and complete release diagnostics

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B229.256; verified deployment below; native acceptance pending.

## Approved scope and investigation

User authorized retaining network wait details in the existing bounded trace, covering both release exits and checking release criteria. No new timer, forced wake or repeat native command. Capacity, binding, task/reward/history, schema and GC remain unchanged.

B228 submitted sessions `session-20261018T010120Z-e08dca` and `session-20261018T010420Z-187a37` contain no new full completion/release chain and no NETWORK_WAIT/NETWORK_INPUT print. T81 load shows ARRIVED with native SLEEP and Wake allowed; later action signatures change. T75 startup is AWAKE/ready with Sleep/Wake denied, followed by clean REJECTED/ARRIVED. Old/current Wake query shapes agree in those records. Do not claim the signature fix solved that denial or attribute loaded Sleep to a captured B228 release.

STATIC_CONFIRMED: the installed Base UnitPanel.lua:4053–4072 uses activity for the status icon and IsReadyToMove separately for entry coloring. This is not a native release-completion contract. There is insufficient evidence to make readiness or Wake eligibility a new release gate. Preserve existing owned AWAKE/HOLD confirmation and unknown-write protection; no speculative native recovery. Local false-readiness/HOLD tests explicitly protect this boundary.

## Implementation

- All release ACK paths use one small diagnostic wrapper. ACTIVITY_RELEASE includes releaseBranch=ENTRY_READ / SECOND_READ / UNOWNED before ACK. The previously silent second-read exit and unowned exit are covered. Diagnostic errors cannot block ACK. All native command/ownership semantics remain unchanged.
- Culture Network waiting reports retain one scalar NETWORK_WAIT record in the existing B205 ring, including failure layer/reason, readiness and bridge input/derived/revalidation/error fields. Existing reader/collector accepts it with the prior field-order repair. A late snapshot can retrieve it while retained; no promise beyond the existing64-entry ring/96-record per-producer budget or across process exit.
- One replaceable last-wait signature suppresses unchanged consecutive report snapshots. No per-city history/cache, polling, new listener or persistent field. Existing immediate Chinese report/print remains. Successful report clears the signature; the underlying ring retains its own dedup/budget rules. Reads do not Refresh the network or mutate carriers.
- No arbitrary errors, paths, names or tokens are retained. Optional diagnostic failure does not replace the waiting report.

## Local checks

255 targeted offline tests PASS, including9 new actual-source checks: both owned release exits, unowned Sleep, false readiness, failed diagnostic ring, late fixed-query snapshot, identical-state dedup/state change, ring/budget bounds and failure-tolerant reports. Existing B228 print-only tests now accept both already-allowlisted print and TRAIN channels without weakening semantics. Activity/pending/recovery/integration, B227 no-frame checks, network projection and collector regressions remain covered. No live query or native performance claim.

## Minimal native gate

Start the existing collector manually. Perform one ordinary task through completion, then try another task or dispatch. If rejected, retain the log rather than repeat clicks. For the affected culture city, open **文化见闻** once while it shows waiting; the report now remains recoverable through the current bounded ring even if its immediate print was missed. No cold-load or long-test requirement. This batch improves evidence completeness; recurring native denial and the actual network failure are still open until the records identify them.

User decision: none within this batch. Primary next: review retained reasons and release branch/state; do not bypass native permissions or rewrite network qualification.

## Verified deployment

B229.256/modinfo256 DEVELOP_ACTIVE; source 90865599b303f0ee2e575e43378625d6870da7a3; receipt B229.256-9086559-playtest.json;226/226 MATCH, digest d6912eb5658641b2d423ec3edc16d162bb29c9948c8bc20fba3c28d34d6f73a6. Automatic game-exit checks at both guarded switches; B228/stable recovery retained, no pending transaction. No game launch, configuration or main change.
