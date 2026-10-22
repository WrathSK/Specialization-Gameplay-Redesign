# B239 native review — Crew continuation and Commercialization eligibility

Date:2026-10-18. Review basis: develop `48d995c`; source/live B239.266, implementation `972e911`, receipt `B239.266-972e911-playtest.json`. This is an evidence/documentation checkpoint, not a new implementation or deployment. Previous [local results and test scope](Specialization_B239_Commercialization_Local.md) remain unchanged.

## Review summary

- **USER_GAME_TEST_PASS:** the user confirms paid Crew continuation occupancy now works. Logs preserve the same reservation7, cost338 and progress14 while resuming beside a living Crew; new admission remains unavailable at full occupancy.
- **Commercialization native acceptance remains pending.** The user recalls all configuration buttons disabled and then confirms Medina had none of the five required local districts. Disabled eligibility is consistent with accepted D0054; this is not evidence of a failed public network or a failed Gold carrier.
- The public network reaches VERIFIED/AVAILABLE, input7/derived7. Commerce reaches READY with two workers and zero configured Gold. One COMMERCE_READ succeeds; no COMMERCE_SELECT or effective COMMERCE_DOMAIN record appears in the captured interval.
- **STATIC_CONFIRMED / LOCAL_SIMULATION:** the P0 report omits every unselected domain. The configuration reason also prioritizes NOT_SELECTED over missing local eligibility. This weak explanation obscures the actual prerequisite; no UI change is implemented here.
- Next: continue the existing B239 session when the Commerce city has an eligible local district with ordinary infrastructure. Use the production-list **商业化 / 商业信誉** configuration window and explicitly enable that domain. No repeated Crew acceptance or new network test is requested. Gold/source exclusion, LIFO, Reputation and the shared new-state cold-load gate retain their untested scope.

## Captured evidence

The existing collector name/prefix B205 is not the tested build. The unchanged ignored session is `local/diagnostics/B205/session-20261018T172146Z-6d522b/`:288 distinct TRAIN records, contiguous seq12–299, turns26–32; summary ends INTERRUPTED. Thirty-six gate-print lines are separate from those records. Capture starts at seq12, so absence claims apply only to the captured interval; the visible build and user submission identify B239.266.

| Original file | Bytes | SHA256 |
|---|---:|---|
| records.log |112584|`ff9985cda8899906e5316546352bf06426c85f10d6935fef1e8a11cd5bb8aab7`|
| events.jsonl |3719|`faf75d8e6e989cd0e62f81868ae88b9ba8ee677600d59e86c39c75bf09a95052`|
| summary.txt |633|`a8bfde1fad6c888ae406e64e6338cd0ab48d6c2eb209fc76883fc41a1cbef25e`|

Five original screenshots were individually read, then moved from `ScreenShots/` to `local/legacy-workspace/Specialization/Status/Validation/Evidence/B239/`; original names and bytes retained,5/5 SHA256 MATCH. The ignored manifest records each before/after hash. Image1 shows the native five-route overview;2–5 show public network reports for Medina, Stirling, Edinburgh and Baghdad. None shows the Commercialization configuration window or an actual Gold delta. Raw screenshots and logs remain outside Git. The display reproduction script/result are retained under ignored `local/diagnostics/B239/native-review-20261018/`.

| Trace | Observed result |
|---|---|
| seq63–68 | New312 order plus an existing paid paused order occupies both slots; after completion living1+paused1 still has `wanted=false` |
| seq70–75 | Existing reservation7 resumes at14/338, then living1+queued1 remains full, followed by living2; no additional slot is admitted |
| seq22/69/117;137 | Another city65536 has the previously observed native-cost-mismatch hold, later READY. Preserve this separate conditional gap; do not infer repricing or a new failure in the accepted continuation city131073 |
| seq49/76/77/80/82 | Medina initially reports ACTIVE III required |
| seq274/278 and281/283 | Route revalidation holds resolve to Commerce READY; latest state has workers2 and Gold0 |
| seq285/287 | COMMERCE_READ accepted; public network has5 routes, VERIFIED/AVAILABLE, matching revision7 |

The culture appendix CN_REPORT_PENDING/REPORT_FACTS is separate from the verified public network. It is not a Commerce route failure. No new Culture investigation or acceptance is implied.

## Eligibility and route interpretation

[Accepted Commerce](../../../Design/Commerce.md#本地理解与外部价值来源) requires the Commerce city itself to have the mapped district: Campus, Theater, Industrial Zone, Holy Site or Harbor. Its local D contributes to the formula. A Commercial Hub alone unlocks none of those five domains. A remote city's district or specialization does not substitute for this local prerequisite.

For an enabled eligible domain, X is the highest matching **total city yield** among self and own cities with a valid direct domestic route in either direction. Remote candidates need neither the matching district nor a specialization. Take the maximum, not the sum; do not expand the candidate set through distribution or transitive connectivity. Exclude Commercialization-generated Gold as already specified.

Assume F→E remains present, E is the Commerce city and A is the capital:

| Routes involving E | Candidate cities for E | Not added through forwarding |
|---|---|---|
| F→E and E→A; A→B/C/D | E,F,A | B,C,D |
| F→E and E→B, or B→E; A→B/C/D | E,F,B | A,C,D |

A directly eligible city's current total yield can already reflect its legitimate effects. That does not make the contributing remote cities independent Commerce candidates. [Ordinary network distribution](../../../Design/Network.md#接收不等于取得转发权) and this direct-pair predicate remain distinct.

The submitted native route list gives Medina the candidate set **Medina, Edinburgh, Baghdad**. Stirling/Aberdeen are not candidates solely because Edinburgh connects to them. Public-report source listings are not the Commerce eligibility list.

## Source check and diagnostic follow-up

[NetworkBridge.CurrentDomesticPartners](../../../../Mod/NetworkBridge.lua) reads the verified direct-pair projection; [Commerce.prepare/resolve](../../../../Mod/Commerce.lua) uses local Shared D for eligibility and only self/direct partners for X; [CommerceCalculation.Layout](../../../../Mod/CommerceCalculation.lua) keeps those predicates separate. [OrdinaryBuildingCatalog.Domain](../../../../Mod/OrdinaryBuildingCatalog.lua) and [DistrictCompleteness.Calculate](../../../../Mod/DistrictCompleteness.lua) actually use the same DISTRICT_* keys as Commerce; the suspected key-namespace mismatch is rejected by direct source inspection.

The current [CommercePanel](../../../../Mod/UI/CommercePanel.lua) disables an unselected row when `eligible=false`. Layout supplies NOT_SELECTED first, even when the local district is absent. `Commerce.Describe` only prints selected rows. A bounded actual-consumer run with the existing [B239 fixture](../../../../DevelopmentTests/test_b239_commerce.py) confirms READY + five eligible rows + zero selections produces a P0 report with no domain rows. This demonstrates the report's blind spot; the fixture does not prove Medina's native district contents, which were confirmed by the user.

Suggested later presentation-only correction: explain missing local districts before unselected state; show each domain's local eligibility/D in the read-only report, and name the production-list configuration entry. Reuse current facts; no new scanning, timer, route rule or automatic selection. This suggestion is **not implementation authorization**.

User decision: no Gameplay change requested. User testing: existing B239 Commerce gates remain pending with the corrected setup explanation. Primary next: stop after evidence/context checks and this documentation commit; no new batch, runtime, Design, test-assertion, configuration, main or deployment changes.
