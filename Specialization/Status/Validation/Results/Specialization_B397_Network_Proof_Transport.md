# B397 — pre-U5 network proof transport repair (NET-1 / NET-2)

Status: locally validated and deployed; native recovery awaits user verification. Recorded 2026-10-31.
Baseline: develop eeb4a08; runtime B396.423; D0058 / A0183 / S0856. User explicitly authorizes this narrow transport repair under the existing Primary workflow. Main promotion is not authorized. Option B architecture convergence is deferred until after U5.

## Confirmed defects and authorized scope

Current NetworkSender treats equal fingerprint + VERIFIED as duplicate without the Bridge-required signal equality. A real Lua51 Sender/BackgroundRoutes/Bridge composition reproduces zero sends while TransactionCurrent is false after a signal-only event. An undelivered request also holds its same-turn flight across LoadScreenClose; a real asynchronous composition reproduces no resend and a blocked proof. These are local reproductions, not proof of the exact native packet-loss stage inferred by the Advisor.

Repair only Sender and its BackgroundRoutes lifecycle caller. Preserve complete snapshots, epoch/turn/signal/count/endpoint validation, monotonic sequence/replay and acceptedSeq receipts, strict transaction reads, failedTurn/limit protection, network isolation, D-1 physical-effect freezing and the existing consumer-wake path. No new retained-fact interface, passive reconciliation change, profession formula/pricing, save field, GC rule, S9/S10 retirement or Principles A/B/C migration. Advisor originals remain read-only.

## Runtime Impact Contract and selected gates

- Facts/collection: reuse the complete existing UI snapshot and unchanged Bridge validation. No new network fact source or gameplay getter. Lifecycle recovery recollects through the same bounded collector, never trusts a retained carrier as proof.
- Cause/scope: signal-only changes now send even for equal content. Explicit LoadScreenClose and LocalPlayerTurnBegin can replace an unacknowledged flight; normal publish/playback/SystemUpdateUI cannot reopen it. LocalPlayerTurnBegin only wakes outstanding transport/turn wait or incomplete sampling.
- Bounds: one in-flight request; at most one actual operation at each of the two named lifecycle boundaries per Bridge epoch/game turn. Repeated boundaries do not replenish that budget. Ordinary idle pulses send nothing after receipt and cannot retry a missing receipt. No timer/fixed delay/frame retry. Existing route128/payload16384/city512/read-attempt3 limits remain.
- Availability: known inactive turn defers an operation without spending recovery budget. Missing/throwing IsTurnActive retains the prior transport attempt with UNAVAILABLE observation, never a reliable-active or READY claim. The unchanged Bridge receipt/validation remains the only proof authority.
- Dependencies: Sender -> BackgroundRoutes current complete sample -> existing script transport -> Bridge Receive/notification -> existing consumers. No new automatic consumer or shared service.
- Failure/recovery: process a seen ACK/rejection before deciding lifecycle retry; never clear known failedTurn on a lifecycle wake. Higher Seq rejects late old packets; epoch/turn/stop discards transient recovery state. awaitTurn is sender-owned transient scheduling state, not diagnostics or saved authority.
- Tests: T01 lifecycle/cause locality, T02 producer-to-consumer invalidation closure, T05 finite recovery/idle bounds, T08 same-turn signal/ACK/epoch freshness and strict transactions; exact Workflow gate applicability is limited to this transport closure. Use real Lua51 Sender+collector+Bridge+FC/Culture and representative Commerce/Capital/Development proof guards. Add first-drop, repeated wake/idle, late ACK/replay, inactive/unknown API, zero routes, limits, stop/epoch and D-1 tests. Existing relevant network/project-transaction regressions and restricted Lua51 compile/package/context checks follow. No all-history suite or new Closure snapshot.

## Evidence and handoff

Current source and the NET records in the user's Independent_Architecture_Audit_B396 / companion Evidence were reviewed. Existing Architecture P01-P10 and network confirmation-recovery/D-1 clauses, Network Design and PT015 govern; the audit does not itself authorize new architecture. Local/native labels remain separate.

User decision: none for the authorized repair; any scope expansion stops for review. User testing: after safe deployment, reuse one planned Commerce test for load-turn proof recovery, unchanged-content signal catch-up, Commerce READY and Capital/Development quote/confirmation, without repeating accepted Research/Culture abilities. Primary next: complete targeted validation, metadata, reviewed commit/publication and existing safe deployment gates; report any blocked publication/deployment accurately.

## Implementation and local results

NET-1: DUPLICATE now requires matching fingerprint, VERIFIED and both Bridge/snapshot/current signal equality. Identical route content with a new signal is fully resubmitted and accepted by unchanged Bridge validation; proof availability and consumer notification recover without changing logical inputVersion.

NET-2: only a new LoadScreenClose or LocalPlayerTurnBegin witness may replace a missing-receipt flight. Each kind permits at most one actual operation per Bridge epoch/local game turn. Pending lifecycle sampling is one bounded scalar record, retained across the existing three collection attempts and synchronous busy/reentry; a failed read cannot lose the only recovery witness. An armed bit drains a newly deferred witness once, without replenishing no-progress read attempts. A newer lifecycle witness supersedes the older one; stale turn/epoch witness is not used to authorize recovery. Stop/shutdown discards it. Known inactive waits in transport-owned awaitTurn without polling native activity on idle frames. Unchanged current proofs do not collect again merely for LocalPlayerTurnBegin. Packet format, Bridge, strict consumers and all profession business sources are unchanged.

Python3.14.8 / Lupa2.8, actual Lua5.1 modules with explicit native/transport doubles. **LOCAL_SIMULATION_PASS:87 methods** in the final selection. New file has34 methods:23 focused cases and11 retained historical proof/limit assertions under actual FC/Lua51 fixture adaptation;no old assertion is changed and no synthetic consumer notification is added. The new restricted case executes without os/io/debug/package/require/rawget/loadfile/dofile/collectgarbage and Lua5.2 table helpers. Runtime compile/XML/manifest closure passes in the same selection.

Reproduce from repository root, with the existing Lupa2.8 environment on PYTHONPATH plus DevelopmentTests and tools:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_b397_network_transport test_refactor_s5c2 test_refactor_s5a2.Freshness test_refactor_s9e1.RemovedTraders test_refactor_s9e6 test_b241_capital.Runtime.test_unknown_network_holds_quotes_without_new_money test_b241_capital_ui.Network test_b246_development.Network test_b267_preplaytest.Package.test_actual_lua51_syntax_and_manifest_closure
```

Important discriminations: same-value signal catch-up reaches real FC bindings;one dropped initial packet recovers on load without advancing turn;two missing receipts can use the later local-begin witness;1000ordinary pulses cause zero extra sends;repeated lifecycle boundaries do not exceed three total operations in the lost-flight scenario;known inactive preserves recovery budget and does no idle activity polling;temporary collection failure and native-send reentry preserve the witness;EMPTY proof cannot restore old routes;late old Seq/epoch cannot replace the newer receipt;seen-but-rejected or throwing requests remain failed for that turn;isolation/shutdown stops recovery. Explicit topology-PENDING retains old Culture carriers while both Capital source proof and Development outgoing proof remain unavailable. Actual Capital and Development service guards refuse unknown network without charging money.

## Baseline failures and evidence limits

The first broader legacy selection was not all green. Independently fixing Sender/BackgroundRoutes to eeb4a08 reproduces exactly the same10failing methods/11error records across the30 original B232/B239 methods. They assert old synchronous consumer payloads/notifications or earlier confirmed-loss semantics. The11 applicable unchanged assertions are rerun by the new fixture profile. No production shim or weakened assertion was added for the remaining old expectations. An additionally tried B243 diagnostic-log-bound method and B246 combined route-reason method fail outside the changed transport path;the latter's actual unknown-network/no-charge guard passes separately. They are not claimed repaired or PASS. The former old diagnostic bound is unrelated to network and was not expanded into another audit.

The primary defects were independently reproduced before editing with actual Lua51 Sender/collector/Bridge. A review found the temporary-read/busy lost-witness case in the first repair draft;four direct regression cases were added and passed after witness retention. Complete machine closures are not submitted. Source is recoverable through the normal Git commit for this batch;local simulation does not establish native packet delivery/order or why the old first request failed to enter Gameplay.

## Minimal native delta during the planned Commerce test

1. In the next supported-build Commerce test session,keep the existing collector open. With at least one valid domestic route and an eligible commercial city,save and reload once. In that loaded local turn,wait for ordinary UI processing without opening the trade UI or advancing the turn solely to recover proof. Short pending is allowed;whole-turn UNAVAILABLE/IN_FLIGHT is the failure signature.
2. Check public route proof,then the existing Commercialization view and the planned Capital/Development quotation and confirmation. Once proof is confirmed,they must no longer be held merely by old signal/first-load transport. Other eligibility/price/target gates stay strict;an unrelated HELD reason is not evidence to relax them.
3. Continue the planned test through the next normal turn with route content unchanged. Confirm proof catches up after signal changes and consumers recover. Collect NETWORK_VERIFIED/NETWORK_SIGNAL_STALE,net_send/net_receive,Commerce READY and actual contract/debit rows. No accepted Research/Culture retest or forced pillage is requested.

Native event availability/order,actual script-operation delivery,and untested nonzero Commerce/contract outcomes remain **USER_GAME_TEST_REQUIRED**. Both lifecycle retries can still be lost;after their finite budget,the sender retains existing fail protections and waits for a later real lifecycle/turn rather than inventing success. This batch does not promise to solve every PT015 or zero-revenue cause.

User decision:authorization covers repair and safe develop deployment;the user additionally approved publishing the prior eeb4a08 report together,subject to privacy checks. User testing:only the combined Commerce-session delta above. Primary next:complete publication checks,push verified develop,then exact receipt-bound deployment if reliably exited;no main promotion or unrelated migration.


## Static and deployment preparation

All219runtime Lua files compile with Lua5.1;25XML files parse;341unique modinfo file references resolve across342runtime files. Only NetworkSender,BackgroundRoutes and the two build-identity files differ from baseline runtime. NetworkBridge,profession business modules,SQL/save definitions and formal Design/Architecture remain byte-identical. The first context check identified the same four reviewed runtime files also present in Context_Lock;their named duplicate hash entries were synchronized after source review,without unrelated rehash. Current live B396 and its exact receipt/stable B307 recovery package match in read-only preflight;main is clean. Source version424 is not called deployed until a completed verified receipt below.


## Verified temporary develop deployment — 2026-10-31

The privacy/publication gate passed all12batch files;the user explicitly approved including the unchanged earlier listener-report commit eeb4a08. Both commits were pushed to develop. Reliable OS process checks before each transaction found no running game. The existing tool restored B396 through its exact receipt,then activated B397 from source `aa51febb4b99ad21e51416066a737620b2eff8a2`. Live **342/342 MATCH**,SHA256 `4c14e43d73e98a3f03593422575ce880fad7adc55d4c5c39abd959055fddc0b7`,receipt `B397.424-aa51feb-playtest.json` phase DEVELOP_ACTIVE. Stable B307 and outgoing B396 recovery packages both match;no pending transaction remains. Main stays B307.334. No game launch,user-save mutation or native PASS.

Context integrity passes342runtime files/1290guarded inputs and its self-test;static alarms have no new/widened occurrence. Only deployment/result/current-pointer metadata is updated after the tested source commit;Mod/test bytes remain unchanged.

User decision:none pending. User testing:the combined Commerce-session reload/next-turn/READY/eligible investment delta above. Primary next:stop at verified B397 deployment and review the user's next logs;Option B convergence and S9/S10 work remain deferred/outside this batch.
