# R05 / R02–R06 — Minimal recovery-evidence persistence proposal

Status: USER_APPROVED_BOTH_EXTENSIONS — 2026-10-25. Technical implementation pending; no gameplay-rule amendment.

The user explicitly approved both minimal extensions in this Primary session. The network/deferred-lifecycle scope below is authorized;do not request routine reauthorization. D-1/D-2/D-7,Standardization-only A,native outcome protection and deployment/main boundaries remain unchanged.
Routing: existing [refactor intake](Audit_Followup_Priorities.md), R05. This is not a second backlog.

## What is already decided

U1 D-1/D-2 and the accepted S8 handoff require reliable siblings to update while valid old contributions from unreadable sources remain tagged RETAINED. UNKNOWN is never transaction proof. Confirmed source/receiver owner,reference or qualification loss still withdraws. The cold inseparable-aggregate exception A stays limited to Standardization. None of those choices is being reopened.

## Current evidence and exact limitation

- [Commerce.resolve](../../../Mod/Commerce.lua) retains per-domain/per-source `reference,eligible,X` in session-only `samples`. The saved Commerce record contains selection/reputation,not these source observations. On a new Lua context,only the sum encoded by the Gold carriers remains.
- [CultureNetwork.source/plan](../../../Mod/CultureNetwork.lua) retain source reference and full civilization sets in session-only `sourceSamples`/`contributions`. Carriers encode the union count,not its membership or attribution. Cold records explicitly start with empty contribution maps.
- Existing actual module fixtures reproduce cold Commerce15→6 and Culture1→0 after topology confirms with a necessary source unreadable. Both classify that first-time source UNKNOWN. They do not have the prior per-source facts required for D-2. These are local counterexamples,not native save-file evidence.

Aggregate inversion cannot solve this. Two cultural sources with overlapping civilization sets can produce the same union count while leaving different legitimate retained values after one confirmed exit. Commerce's summed rounded domain Gold similarly does not uniquely determine each source's raw value. Inferring a contribution from the total would fabricate provenance.

The authority texts need to be read together:

- [Network.md:55](../../Design/Network.md#未确认不等于失效): “冷加载只有旧组合载体、尚无法可靠分解各城贡献时，暂保留该组合值直到必要事实可用，不凭空分解或把未知部分归零。”
- [Shared_D0058 NETWORK_LAYER](../../Design/Content/Shared_D0058.json): D-2 requires “保留该来源仍有效的上次可靠贡献”; exception A explicitly says “仅适用于已审查的标准化合并物理载体”.

A generic aggregate hold is not a substitute for updating readable siblings and withdrawing confirmed lost sources. This report does not declare a new Design conflict or silently extend exception A. The concrete missing prerequisite is durable,verifiable attribution for Commerce/Culture.

## Recommended bounded extension for approval

Authorize a **derived network-recovery record**,then implement it in independent reviewed slices:

1. Its sole purpose is restoring the already accepted D-2 retained contributions across a new Lua context. It is not a new permanent achievement,route snapshot,qualification authority,quote,receipt or transaction credential.
2. Store only detached existing contribution fields:receiver and source owner/location/token/change witness,ability/domain,raw source value or civilization set,reference/provenance version,and a witness tying the contribution bundle to the confirmed applied carrier shape. Never store native objects,whole views,diagnostic histories or complete expanded closures.
3. Reuse existing working-set/source bounds. Define exact limits,ownership,encoding,readback/CAS,load validation,invalidation and removal before wiring the first writer. Persist only from reliable existing input/commit boundaries;never from a pending candidate,retained snapshot or UNKNOWN result. Compare same-value writes and do not create turn polling.
4. After load,accept only supported-version,bounded,complete records matching the same receiver/source lifecycle and installed carrier witness. Confirmed loss overrides retained values;unreadable sources remain RETAINED,never CONFIRMED. Missing,mismatched,unverifiable or partially written records cannot fabricate source data or authorize investment.
5. Prove carrier-write/recovery-record ordering and both failure directions before composition. An unknown native/save outcome is not permission to reconstruct a successful commit. No deployment or claim of old-save migration follows from this approval.
6. Add real writer+Store tests for cold mixed sources,overlapping culture sets,multiple Commerce domains,known loss plus unknown sibling,owner/reference reuse,unknown record versions,partial writes,source recovery,same-turn second change and bounded idle work. Preserve the current cold counterexamples on the previous source;do not weaken them.

This extension crossed the existing persistence/shared-contract boundary and has now received explicit narrow user approval. It is not a re-vote on D-1/D-2 or authorization to weaken saved authority and native outcome protections.

Alternative:leave R05 explicitly OPEN for this integration candidate and schedule that extension later. Do not claim complete D-2 cold-load support or zero the limitation in the backlog. Unaffected S9/U4/S10 engineering can continue either way.

## Second bounded extension: remember skipped lifecycle work (R02/R06)

B382 proves one recovery is already possible without extra state:Development contracts carry source owner/change epochs,so their skipped owner termination can be reconciled after reload. Capital has equivalent contract references. Other records do not always contain such a witness. Current Store isolation is a session-only observation;confirmed loss/return deliberately leaves opaque bytes unchanged. Its legacy lastLoss has no loss/return turn,and not every supported return uses a returnProof with a turn.

For example,after a temporary Commerce validation failure during loss/return,old selections can again match the original owner after reload. That payload alone cannot distinguish an old selection that must be cleared from a legitimate selection made after return. Repeatedly clearing all recaptured cities would destroy valid later choices. A Tradition record can similarly lack the boundary needed to rule out a held interval. Do not guess from current turn,one exception,or ownerChanges>0 alone.

Authorize a small **per-ability deferred-lifecycle witness** in the existing Store record:

- Written only at an already confirmed loss/return when that ability cannot perform its normal lifecycle transition. Fixed nine-owner keys;retain the last necessary owner/change/reference/turn episode per affected ability,not an event history or unbounded retry queue.
- Keep the original opaque ability bytes intact. The witness records the existing required transition;it does not invent ownership policy or prove the payload permanently bad.
- When the existing load/related availability boundary reliably validates the payload,apply that ability's existing lifecycle transform once,with full parent validation,CAS/readback and original owner/reference guards. Clear the witness only in the same confirmed Store commit. Failure preserves it;UNKNOWN never becomes an instruction to retry on idle.
- Money CALLING/HELD and native completion remain nonreplayable. A witness can prove a required cancellation/rebase/configuration clear,never prove an unknown payment or unit grant succeeded.
- New-supported-save coverage only;do not reconstruct missing historical episodes in old saves or silently migrate them. Test temporary failure across loss/return/cold load,second changes,partial write and independent abilities.

This is a persistence mechanism for existing rules,not new gameplay. It still needs narrow approval because it adds saved cross-module recovery evidence. Both extensions are authorized;implementation/evidence remains separate.

## R02 per-ability baseline intake (accepted D-7, not new policy)

All rows first require a supported record/version,strict valid identity/reference/envelope,and reliable bounded reads. CHECK_FAILED is only a validator observation;CHECK_UNKNOWN,missing initialization,one failed pcall,or a future version cannot prove permanent corruption. Repeated equal bad reads alone are also insufficient:enumerate and check the ability's actual alternative authority before declaring it unrecoverable. Native/money outcomes must be resolved independently. Existing deterministic metadata reconstruction stays first.

| Ability/group | Lawful baseline shape / remaining proof | Visible loss and engineering boundary |
|---|---|---|
| Expedition Insights | Supported `{version=1,records={}}` after all saved city/category receipts are proved unrecoverable | Old observations/full civilizations lost;unrelated city history stays |
| Dialogue | Existing `New()` zero total/serial/used shape;no unresolved pending native completion | Old multiplier history and era-use history lost;no completion replay |
| Engineering | Existing `New()` zero L/serial/receipts shape;no unresolved native completion | Old L lost;template knowledge and Wonder credit remain independent |
| Commerce configuration | Existing `New(currentOwner)` with empty selected list,keeping an independently valid reputation group | Existing domain choices lost;no new Gold or transaction credential |
| Commerce reputation | Legal age0 needs trustworthy P4 origin/receipt and a reliable current baseline;missing origin cannot be assigned the current load turn | Reputation benefit resets only after a valid origin proof;unresolved-origin boundary remains explicit |
| Research Tradition | Legal age0 likewise needs trustworthy city P4 origin/receipt/qualification;never fabricate its original start | Accumulated age lost;no lost-interval credit or invented P4 event |
| Template family | Exact typed empty knowledge/lifecycle must validate against the same city identity;do not recapture current buildings as invented history | Learned history lost;independent N and L remain;actual constructor proof still required |
| Claim timer | Nil only when independently proved terminal/cancelable under current project rules;not from unknown CALLING | No fabricated Claim receipt or native finish;terminal cleanup already implemented |
| Capital / Development | Existing `New()` structures exist,but zeroing cannot erase unresolved debit/credit/native outcomes as if settled | Paid principal/owed return/active contract may be lost;complete outcome proof or a separately exposed residue is required |

This table defines implementation prerequisites and losses,not permission to reset every failing group. Accepted D-7 already authorizes a lawful baseline once permanence is actually proved;Primary continues the deterministic/reconstructible cases internally. Only genuinely absent lawful-origin/outcome cases go to a user decision. No permanent HELD status is presented as the finished recovery feature.

## Approved scope and ongoing work

Recommended:approve both bounded saved-evidence extensions,keeping all existing D-1/D-2/D-7 rules,strict native outcomes and new-save limits. Primary will finish exact encoding/bounds/ordering tests in independent batches before production wiring,without routine stage approval requests.

Alternative:retain these specific limitations for later;do not call R05 cold attribution or skipped opaque lifecycle fully repaired. The remaining authorized display/applied-owner/U4/S10 work can continue either way.

User decision:both minimal extensions explicitly APPROVED on 2026-10-25;none pending for this scope.
User testing:U5 cold save/load,source loss/return and recovery after any approved implementation.
Primary next:write the approved constraints first,then implement durable deferred-lifecycle evidence and bounded derived network attribution in separately tested batches;continue S9–S10 without routine stage approvals. No deployment/main/game launch.


## Evidence locator

Scoped local source proof: `local/refactor/R05-B383-source-proof.json` (LOCAL_ONLY,not a permanent backup). It uses the existing `test_refactor_s4b.cold_commerce`/`culture(False)` actual module fixtures,with an installed old carrier,selected Campus and unreadable SCIENCE source,or an installed cultural carrier and unreadable source history,then delivers a complete verified route packet. Results:Commerce15→6,source UNKNOWN;Culture1→0,source UNKNOWN. Frozen/current source and input digest are in that local file;B383's tested code snapshot is separately identified in its result. The original source-local warm-retention,strict transaction and Standardization A tests remain unchanged.

## Network implementation contract intake — S9g2, before native wiring

A separate disposable derived slot is required;the potentially larger source bundle cannot enlarge or be inserted into the permanent record Copy envelope. Its exact native adapter/key remains a subsequent reviewed implementation step. The callback-only cell first proves the ordering independently. APPLIED means physical encoding was explicitly verified,not that every source is current or a transaction is eligible. A retained source must match an immutable source in the previous APPLIED bundle;an unconfirmed aggregate,UNKNOWN row,invalidated candidate or caller label alone cannot supply it. Newly confirmed input and carried old proof remain distinct. No original frozen Design/audit conclusion is rewritten.

Before any changed physical encoding,the old derived slot is invalidated with a bounded tombstone containing only version/family/sequence/receiver. A successful exact postread grants one private carrier ticket. After the caller has checked the actual complete carrier shape and source/lifecycle fence,finalization compares the tombstone and publishes the canonical bundle. A throw/drop/unreadable/stale postread cannot prove success or trigger replay. A pending/torn slot cannot be decoded as an applied contribution on cold load. Identical facts/shape need no metadata writes;actual health proof remains required. This is derived-state recovery,not an irreversible transaction or exactly-once guarantee.

The future native adapter must preserve confirmed-exit priority and make metadata failure explicit;it cannot leave an old apparently APPLIED record eligible after changing the carrier under that record. Review both positive failure and negative withdrawal/cleanup,including a later coincidentally equal encoding. Do not bypass current Store/reference guards or silently send unrelated UI/fact invalidations for a technical metadata write. Native storage size,real callback delivery and normal event write/scan cost remain U5/composition gates. No production slot or new saved field is implemented by the pure model/cell prerequisites.
