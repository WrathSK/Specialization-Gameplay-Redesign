# B399 — route and shared-project coverage reconciliation

2026-11-01. Primary documentation-only reconciliation at `7edbea1`,following the user's coverage clarification. Runtime remains B399.426 / `4915170`,D0058/A0183 unchanged. **Do not start U5. Await the user's next task after this record.** No implementation,tests,probes,game launch,deployment or main promotion.

This narrows the testing recommendations in the [previous review](Specialization_B399_Button_Treasury_U5_Review.md);that result's observations are preserved. Missing native evidence for an uncommon entry point is not automatically a new player-test prerequisite.

## 1. Ordinary route and source-change coverage is sufficient

| Tested behavior | Evidence and accepted scope |
|---|---|
| Real route creation and later re-establishment | Third Industry run establishes/recreates links and applies Standardization;subsequent Commerce tests obtain READY and real contract confirmations. This is not dependent on opening P0. |
| Actual edge expiry/removal | Fifth-run native Game_TradeManager.csv2/4 records New York→Baltimore expiry at67T and San Francisco→Baltimore at68T;receiver templates/max strength withdraw. [Fifth review](Specialization_B399_Fifth_Playtest_20261101.md),Standardization section. No killed trader or deleted city is needed to prove that a route really disappeared. |
| Source qualification disappears and returns | Industry governor departure/return produces receiver template loss/restoration in the [Industry review](Specialization_B397_Industry_Playtest_20261031.md),C721/772/945. Fifth-run Commercialization also withdraws/restores with ACTIVE qualification. |
| Source identity changes | Industrial city B's asset liquidation removes its former profession while the city and surviving network remain. Fifth-run liquidation/reconfiguration receipts and Standardization source changes supply this ordinary source-exit coverage. This is not a city-ownership transition. |
| Updated source values/templates and multiple sources | Building/template and study-level changes propagate;two Industrial cities provide overlapping templates with max-value purchase behavior. The user also observes forwarding and later withdrawal. Preserve the measured purchase/production scopes rather than re-requesting every profession. |
| Ordinary cold load and proof catch-up | Multiple loaded sessions restore usable proofs within the turn;unchanged route counts catch up to new signals. Commerce,Capital,Development and source effects work after loading. This closes ordinary recovery in the observed scenarios,not deliberately lost packets or unreadable-source fault branches. |

A route expiring tests **topology/edge loss**;governor departure or asset liquidation tests **source eligibility/identity loss**. The user has exercised both. Do not describe the route tests as merely static or missing genuine disconnection.

### Remaining limits,without new mandatory native scenarios

1. **Different native entry points:**trader death,route plunder,and city removal/transfer were not deliberately observed. [NetworkBridge.lua](../../../../Mod/NetworkBridge.lua),877–891/911–920,has separate notifications and filters for these entry points before common proof revalidation. Expiry does not prove those event signatures/delivery;it does prove the shared missing-route outcome. Primary covers entry routing/filtering with local tests and retains opportunistic long-play observations. Do not require uncontrolled AI attacks or deleting cities/traders. Ownership gameplay remains separately excluded.
2. **Strong-source fallback:**max-value merge is covered;the currently summarized observations do not independently demonstrate the strongest eligible source disappearing while a weaker eligible source remains,with the result degrading rather than clearing. In the fifth run,the second industrial source had already been liquidated before the strong route expired. Prioritize local producer/consumer composition;record a later natural example if it occurs,not a separate player-test campaign.
3. **Fault/partial-read recovery:**a lost/late proof,partially unreadable source,and inseparable aggregate during cold UNKNOWN are distinct from normal expiry/loading. Sender/Bridge fault cases already have scoped local evidence;unfinished accepted Commerce/Culture per-source recovery integration remains Primary engineering work. The user is not asked to manufacture UNKNOWN or packet loss. Do not mark that unfinished implementation PASS from ordinary native recovery.

These are bounded evidence/engineering limits,not a reason to reopen the completed route mainline or add a mandatory trader-death/city-removal campaign.

## 2. Claim does share the tested timing route

All three owners import [TimedProjects.lua](../../../../Mod/TimedProjects.lua). They use its Queue classification and WorkSet block/wake/recovery mechanisms,and [TimedProjectModel.lua](../../../../Mod/TimedProjectModel.lua) for full-turn boundaries. Current call sites include [ClaimProjects.lua](../../../../Mod/ClaimProjects.lua),22–27/144–166;[DialogueProjects.lua](../../../../Mod/DialogueProjects.lua),65–70/236–243;and [EngineeringStudyProjects.lua](../../../../Mod/EngineeringStudyProjects.lua),49–55/turn advancement.

[Existing actual-owner tests](../../../../DevelopmentTests/test_refactor_s7d1.py),104–151,parameterize Claim,Dialogue and Engineering for UNKNOWN recovery,confirmed queue outcomes and full-turn/cancellation behavior. The relevant two RealOwners methods were already run independently in B399's178-method local validation. No additional run or new engine PASS is claimed by this documentation.

**Disposition:**remove the previous standalone Claim full-turn/reload campaign suggestion from the current mandatory native list. The same shared timing mechanism does not need three complete repetitions merely because three projects use it. Use the accepted Dialogue/Study native evidence for shared-mechanism coverage,together with the actual-owner local regressions for Claim. Only a Claim-specific anomaly or a later change to its independent path would justify a focused extra native check.

Retain two precise limits:

- Eligibility,reference checks and permanent outcomes remain owner-specific. Claim freezes candidates and commits the profession/anchor/Potential1;Dialogue consumes a start-era opportunity and adds its reward;Study increments L against E. Shared technical coverage is not invented USER_GAME_TEST_PASS for every unobserved outcome.
- [TimedProjectQueueIntent.lua](../../../../Mod/UI/TimedProjectQueueIntent.lua),4–5,opts only Dialogue/Engineering into the B398/B399 automatic UI queue-re-entry feature. Claim shares the timing foundation,not this later opt-in UI policy. Do not claim identical behavior in every UI permutation;this does not create a new Claim test demand or authorize widening the policy.

## 3. Current hold and responsibilities

- Keep ordinary four-profession,network/source-change,contract,age,restructuring and sole-project acceptance. No renewed whole-profession or route-loss campaign.
- A/Baction repair,remaining Crew attribution/use-after-load evidence,and accepted engineering closures remain tracked. Their existence does not start implementation in this task.
- Primary engineering duties include original cold-source recovery integration,duty migration/retirement and safe package deletion/rollback. Do not turn them into missing player tests;post-U5Option B remains later.
- The final integrated candidate eventually needs its localized regression/load/performance check. **U5 is not started or scheduled now.** No new launch/deploy/test action is requested while waiting for the user's other work.
- PT01741/52origin,multi-item queue timing,HD GPP,uncontrolled pillage/ownership and parked Police semantics retain their earlier nonblocking/deferred boundaries.

User decision:none requested. User testing:none now;no dedicated trader-kill/city-removal or repeat Claim timer campaign. Primary next:record/publish this narrowed coverage and wait for the user's next task,without starting U5 or any repair/refactor batch.
