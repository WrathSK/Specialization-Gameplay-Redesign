# B231 native review — Initial success, stalled network revalidation

Status: **USER_GAME_TEST_PASS for initialization and the tested initial bonus; public diagnostic output confirmed; USER_GAME_TEST_FAIL for updating the bonus after a second complete civilization.** A narrow B232 repair is proposed, not authorized or implemented.

## Baseline and retained evidence

Reviewed develop HEAD `ec61c7e`; deployed B231.258/modinfo258 from `168bb25`, receipt `B231.258-168bb25-playtest.json`. The existing deployment record establishes226/226 equality and digest `75e7b7f56789874f42bfa1f27f29628c754625dbf5cfc76a52a8367580be7681`; this review does not perform a new deployment or runtime verification. [B231 implementation/local result](Specialization_B231_Network_Initialization_Reports.md) remains unchanged. Main/stable B069.96 remains unchanged.

Original collector session: `local/diagnostics/B205/session-20261018T021847Z-d9f013/` (ignored local evidence).132 unique records,8 contexts,61 Gate prints; session ends INTERRUPTED. No new screenshots are present. Raw logs are retained in place, not published or rewritten.

| Original | SHA256 |
|---|---|
| records.log | e41d96c1df2e469796acb1d737cd682fcdbbdff53f9046b45cb3109d8b6e2f96 |
| events.jsonl | 21f9e6ef50d2f014ad78a0e1603a10be66e626ca5d365d86a425fdd9575f835a |
| summary.txt | b8545d114c274b948daecd9fb324b72b6986e62db84cb192c58532f5819e8ef0 |

## Native chronology and verdict

Times below are the collector's UTC clock labels; turn and record sequence identify the actual game observations.

| Observation | Result and evidence boundary |
|---|---|
| T85,02:20:08–02:20:43,seq10–18 | Culture ready=true; shared input VERIFIED/AVAILABLE, input/derived1→1 then2→2. Three recorded recipients end at coefficient1. Selected city65536 has5 matching workers and expected extra Culture5 at02:20:15. User confirms the initial native bonus works; configured expected output alone is not an independent native yield measurement. |
| T85 Insight report | City65536 has9 effective records. Khmer has all three categories; Gaul has PEOPLE and PLACES only. Tourism report18%. |
| T86,02:21:54,seq26 | Shared availability becomes NEEDS_REVALIDATION; Culture remains initialized. This is before Gaul completes its third category. |
| T89,02:24:45 | WORKS succeeds for Gaul with insight=NEW. The adjacent Culture reconciliation records still say CN_NETWORK_PENDING / NEEDS_REVALIDATION. The mission reaches ARRIVED after release in this observed run; no broader Expedition acceptance is implied. |
| T89,02:25:34–02:28:50 | Shared input/derived versions advance together from3→3 to12→12, but availability stays NEEDS_REVALIDATION. Computing new current-city facts does not clear the route-proof hold. |
| T89,02:29:43 and02:30:20 | City65536 has10 historical/effective records; Gaul and Khmer each have PEOPLE+WORKS+PLACES. Tourism report20%. The new Insight is present; this is not a missing reward or missing historical record. Tourism percentage here is report evidence, not a new independent settlement test. |
| T89,02:29:54–02:29:57,seq124–129 | Public report independently exposes2 routes,2 sources,2 centers,3 recipients, and route/center/source/receiver rows, while correctly reporting NETWORK_REVALIDATION_PENDING. Public diagnostics now provide useful data even when Culture is held. Only the captured detail page is confirmed; no claim that every UI page/layout was inspected. |

With both complete civilizations eligible and reachable, the source contribution should rise from1 to2 Culture per matching working specialist. Five workers would mean5→10 if still unchanged; the later log does not establish that worker count. The user reports the expected update did not occur, consistent with the explicit pending state. **Overall B231 is partial, not full Culture-network PASS.**

The bounded Culture trace contributes96 records including its context start. Later absence of more Culture records is not evidence of no execution; the later explicit public report still records the pending state. The existing producer bound is unchanged.

## Confirmed mechanism

STATIC_CONFIRMED and LOCAL_SIMULATION_PASS, using the unchanged B231 source:

1. [NetworkBridge.CheckEvidence](../../../../Mod/NetworkBridge.lua) marks accepted routes NEEDS_REVALIDATION. Endpoint/trader checks preserve known routes but do not prove the complete route set is current or clear this flag. A general UnitRemovedFromMap notification can enter this path even when the route contents remain unchanged.
2. [NetworkSender](../../../../Mod/NetworkSender.lua) returns immediately whenever the current UI fingerprint equals the receiver fingerprint. It does not distinguish an already verified duplicate from the same complete route set needed to answer a revalidation request. A fresh equal-content snapshot is therefore suppressed indefinitely. [BackgroundRoutes](../../../../Mod/UI/BackgroundRoutes.lua) can resample on existing events/turn boundaries, yet the sender still discards the proof.
3. A manually delivered valid equal-content packet clears revalidation and availability, but [NetworkBridge.Refresh](../../../../Mod/NetworkBridge.lua) treats an unchanged fact signature as an input duplicate and does not notify consumers. A waiting Culture projection needs another later relevant event to recover. Revalidation recovery must be observable separately from a topology/fact content change.
4. For a changed valid route candidate, Refresh calculates availability before applying the candidate's VERIFIED flag. It can publish a fresh derived view while still exposing the old pending availability. The next Refresh clears availability, again without notification when the signature is equal.
5. [ExpeditionSpyGate](../../../../Mod/ExpeditionSpyGate.lua) already calls CultureNetwork.SourceChanged after a successful Insight write. [CultureNetwork](../../../../Mod/CultureNetwork.lua) reads fresh history per batch and deliberately refuses new projection from a pending shared topology. With a continuously AVAILABLE network, the same actual code updates coefficient1→2 correctly.

The native log proves the stuck revalidation state and successful Gaul record; it does not name the first T86 invalidating native event or record sender skip counters. The actual-source counterexamples establish a sufficient concrete defect and reproduce the reported failure without changing rewards, formulas or persistence. No need to request another blind native reproduction before fixing this defect.

## Bounded local counterexamples

The read-only local harness imports the existing `test_culture_network.fixture` without executing the obsolete historical test wrapper, then loads actual NetworkSender alongside actual NetworkBridge and CultureNetwork. UI.RequestPlayerOperation is simulated; this proves the Lua control flow, not the native transport. No source or formal test assertion is edited. All8 targeted assertions pass as reproduction/control checks, not as a repaired implementation.

| Scenario | Observed result |
|---|---|
| Control: second complete civilization while AVAILABLE | Coefficient1→2. |
| Unchanged route set, unrelated unit-removal invalidation, fresh sender snapshot, second complete civilization | Sender requests0; NEEDS_REVALIDATION; coefficient remains1. |
| Three further turn/event refreshes with the same valid route contents | Sender requests still0; four duplicate skips total; coefficient still1. |
| Explicitly deliver the same valid complete packet | AVAILABLE/VERIFIED, unchanged input/derived version1; coefficient still1 because no consumer notification. |
| Explicit consumer retry after that valid proof | Coefficient2, zero Property writes. |
| Deliver a changed valid route candidate while pending | Input/derived2, revalidation VERIFIED but availability NEEDS_REVALIDATION; coefficient1. |
| Refresh after that candidate | AVAILABLE, coefficient still1 without recovery notification. |
| Control: confirmed removal of an actual route trader | CONFIRMED_INVALID/UNAVAILABLE; old network coefficient removed to0. |

Local script and raw results are retained under `local/diagnostics/B231/revalidation-review/`, ignored by Git. Run from the repository root with the existing local Lupa dependency:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="<LOCAL_LUPA>:DevelopmentTests" python3 local/diagnostics/B231/revalidation-review/reproduce.py
```

`<LOCAL_LUPA>` is a configured local dependency path, not a literal runnable value. The existing B231143-test result remains inherited from its implementation record; this review does not rerun or expand it into native PASS.

## Proposed B232 boundary — awaiting implementation authorization

- Repair the event-driven revalidation handshake: an accepted fingerprint only suppresses a fully verified duplicate; a current complete UI snapshot must be deliverable when route revalidation is pending. Ensure invalidation has a corresponding request on the existing event/publication path, including the case where UI unit-event filtering differs. Preserve one in-flight request, bounded retries and ordinary duplicate suppression; no timer or frame-polling mechanism.
- Commit successful route proof before deriving published availability. Clear only the uncertainty actually resolved by that proof; unreadable current facts remain UNKNOWN/pending. Never force AVAILABLE merely because the city history changed or retained endpoints still exist.
- Notify consumers once on a genuine pending→AVAILABLE recovery even with unchanged topology/signature. Do not invent an input-version change or rebuild the topology merely to deliver this notification. Preserve confirmed-loss withdrawal and source/receiver isolation.
- Expected runtime scope: NetworkSender/NetworkBridge, and BackgroundRoutes only if needed to carry the existing event-driven proof request. Culture history/rewards/carrier formula, Expedition, Research gameplay rules, persistent schema, GC, Design and main remain unchanged. Add focused actual-source sender→bridge→consumer regression rather than another general diagnostic system.
- Local gates: equal-content proof recovery; repeated dirty notifications/ACK/dedup; changed-candidate availability order; recovery with unchanged content notifying once; fact UNKNOWN held; stale/partial/wrong-epoch packets rejected; route loss still withdraws; second full civilization updates related recipients only; repeated successful state creates no duplicate effects. Check relevant shared consumers because this is a public bridge.
- After local implementation, one minimal existing-save session can verify pending clears and the recorded two-civilization set produces coefficient2; one further complete set checks the history delta when available. No demand to repeat all old missions, cold loads or unrelated lifecycle tests. No additional user testing is requested now.

User decision: authorize or adjust this narrow repair. User testing: none now. Primary next: stop at this review/plan checkpoint; no code change or deployment is authorized by the test submission.
