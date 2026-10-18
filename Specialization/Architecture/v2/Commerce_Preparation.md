# Commerce implementation preparation

State: PLAN_READY / IMPLEMENTATION_NOT_AUTHORIZED. Updated2026-10-18 against develop `519dbac`, Commerce D0050, Shared D0045 and source/live B238.265. Batch grouping and the requested Crew repair share a proposed next checkpoint; this page does not authorize implementation or deployment.

## 当前范围与停止点

The user requests combining the remaining Industry Crew occupancy repair with the first Commerce batch. [B238 native review](../../Status/Validation/Results/Specialization_B238_Native_Review.md) records the confirmed counterexample. Industry's implemented main chain needs no additional ability batch; rare District-body purchase remains user-deferred, conditional protection/Faith/other-speed evidence stays explicitly bounded, and future balance is not a gate. Culture HOLD remains unchanged. Current runtime and authorization belong to [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state) and [Authority](../../Workflow/Authority.json).

Gameplay authority is [Commerce D0050](../../Design/Content/Commerce_D0050.json), [the Spec Commerce section](../../Design/Specialization_v0.1_Design_Spec.md#8-commerce--commercial-hub--com) and [Shared named lifecycle](../../Design/Content/Shared_D0045.json#/concepts/LONG_TERM_STATE_LIFECYCLE). This revision replaces the preparation's obsolete0.1 coefficient, unresolved X/S/exclusivity/protection list, plot-only Development quote and fixed10-turn Development term. It records no new Gameplay decision and does not transfer Industry/Meaning Floor to Commerce.

## 当前落地与可复用范围

| System | Current implementation | Remaining work |
|---|---|---|
| Commerce I/II support | Existing automatic support/qualification | Inherit scoped evidence; preserve baseline specialists/housing/GPP |
| Commercialization | New D0050 writer/configuration absent | Five-domain selection, direct-route source facts, Gold, suspension and exact old-writer cutover |
| Reputation | Absent | First permanent IV start, complete Identity-retaining turn age, cap40, current-IV effect gate |
| Capital Investment | Absent | Quote, debit, specific S source, locked outcome/protection, exactly-once settlement |
| Development Investment | Absent |15% theoretical purchase quote, one active contract per target city, +50% district-building production and completion exit |
| Restructuring | Absent |500P Team, REALLOCATING, one permanent Potential debit, disruption and configuration |
| Old Commerce | Still wired |3 connected-kind specialist carriers and48 Convergence carriers must retire with COM-A |

The old [InvestmentAction](../../../Mod/InvestmentAction.lua) is Settler/Potential investment, not a Gold contract. [EffectiveFacts](../../../Mod/EffectiveFacts.lua), [Store](../../../Mod/CityProgressionStore.lua), [NetworkInput](../../../Mod/NetworkInput.lua) and [NetworkBridge](../../../Mod/NetworkBridge.lua) provide reusable facts/references; their presence is not new Commerce acceptance.

### 已确认的直接实现面

- Primary read the local Stable Advisor report `Specialization/Reports/Advisory/Commerce_Plan_Review/Commerce_Plan_Audit.md` (SHA256 `7e94a5be592d771bea8142c7b2887da200e3b77aa92e89381f7d7b1de8f18458`, basis B231/`0ee4dc9`). It remains advisory and unchanged. Its linked unpublished dependency reports are not silently added to this checkpoint; the necessary planning conclusions are recorded here independently.
- C1 is confirmed: D0050 closes most old Design blockers. C3 is useful, but the three route relationships must remain separate. C4's S tie-break is still a narrow user decision for COM-B, not a COM-A blocker. C5 is interface-specific precision, not permission to round.
- Revalidated since the Advisor baseline: B232 proof/recovery publishing, B233 typed Industry knowledge, B234 current Standardization/Research-network retirement, and B235 Engineering state. Research's retired network effect is not a dependency of Capital's future ACTIVE lookup. Current `NetworkBridge.CurrentNational` covers Research/Culture aggregate projections, not a general per-domain connected-component membership API; it must not stand in for S selection.
- C2 primitive suggestions remain STATIC_CONFIRMED in the Advisor's cited loaded database, not re-executed native results here. Reuse current Industry production primitives for COM-C where semantics match; do not create a second modifier framework. Quote availability independent of purchase eligibility remains unproved.
- C6's event-first, Gameplay-owned writer, pre-native project interception, bounded diagnostics and context-faithful tests are adopted as implementation requirements. No timer/frame polling, extra GC or UI-open dependency.
- C7/C8 are planning advice: use existing specialization vocabulary, keep owners/lifecycles separate and schedule Restructuring last. Do not add a generic future-profession registry in COM-A or unify contracts merely because they share a Modifier API.

## 模块实施顺序与依赖

Keep the existing O/P/Q/R/S/T decomposition. Group native acceptance by usable capability, not one isolated probe per getter.

| Batch | Scope | New uncertainty / dependency |
|---|---|---|
| **Proposed B239: Crew occupancy + COM-A** | Crew repair below; O direct-pair facts; P1 selection/order; P2 current Gold and exact cutover; S1 reputation and read-only status | Gold precision/non-recursion, new configuration/reputation persistence, actual action entry; no Capital/Development/Restructuring |
| **COM-B Capital** | Q1 stable and Q2 venture, shared quote/confirm/maturity panel | Resolve S tie-break; connected-network source evidence; principal/return precision; reliable debit/locked outcome/one settlement |
| **COM-C Development** | R outgoing eligibility, theoretical price, selected district's buildings +50%, next eligible completion exit | Price reader and completion selection; one additive Standardization native comparison |
| **COM-D Restructuring** | T1 protected Team and T2 complete REALLOCATING transaction | Broadest Identity/ownership closure; split primitive and transaction only if native evidence requires it |

## Proposed B239 combined slice

The user requested one combined Industry/Commerce acceptance. Implementation still requires approval of this concrete scope; no new build is assigned by this planning record.

**Crew repair.** The current writer explicitly excludes PAUSED admissions from `reserved`, while resumption requests a new free slot. Count each admitted unfinished project, including a positive-progress paused one, once alongside surviving source-bound units. Resuming must reuse its existing admission, including at full occupancy; it must not require another slot. Completion exchanges the admitted slot for the living unit. Preserve native progress, project ID, locked price, capacity, source, receipts, UNKNOWN and no-replay protection. Separate actual queue count from total committed occupancy; do not replace every `reserved` use mechanically. Use existing order records and native inventory, not a new persistent counter or schema.

Synchronize Gameplay admission, published eligibility, the project row/tooltip and the readable report. A genuine zero-progress cancelled admission may leave; temporary absence/unreadable progress must not free paid work. Previously over-admitted B238 states must retain progress and units: reject further new orders, permit only safe existing continuation under the two-living-unit ceiling, and expose the occupancy reason; no automatic deletion/repricing or broad save migration. Precisely define and regression-test this recovery before shipping.

**Commerce deliverable.** Ordinary Commerce ACTIVE III cities can choose Campus/Science, Theater/Culture, Industrial/Production, Holy/Faith and Harbor/Gold domains where the corresponding local district exists. One actually working Commerce specialist permits one distinct effective domain. Persist choices/order, LIFO-suspend and automatically resume without losing configuration. Gameplay derives X, D, effective R and the current Gold; a readable panel shows selection, suspension reason, source, formula and result. Production-list entries open/toggle before the engine enqueues anything. Reputation starts at first permanent IV, accumulates under its own Identity contract, and only currently ACTIVE IV multiplies output. Preserve automatic operation without opening P0.

**Prerequisite closure inside the batch.** Read the existing [audit scheduling](../../Reports/Proposals/Audit_Followup_Priorities.md) only for affected findings. AF-06(b)'s global-write-triggered `CommerceConvergence.Audit()` still exists; retire that subscription with the old writer rather than copying it. Extend the current immutable/read-only network boundary for required route facts; do not read mutable `bridge.players` as a second authority. B232 fixed ordinary proof/recovery but did not remove `NetworkSender`'s silent128-route/16384-byte returns: include a minimal explicit transport-limit/unavailable signal and local boundary checks before adding the new route consumer. Do not increase caps, invent partial-route semantics, rewrite every network consumer, or reopen the general performance audit. Shared D/current facts reuse is bounded to a reliable input version and invalidates on real changes.

**Precision gate.** Preserve the raw D0050 formula. Existing fixed-city-yield truncation and old Convergence Floor do not validate fractional Commercialization Gold. Check the selected native writer, actual Gold accounting, applicable city modifiers and exclusion of its own Gold from Harbor X. If exact fractional output/non-recursion cannot be preserved, report the concrete limitation and proposed final quantization boundary for user decision before a formal writer cutover. No silent Floor, hidden cap, guessed inverse multiplier or Treasury lump-sum replacement. Preparatory UI/model work cannot be called delivered Commercialization.

**Local delta coverage.** Actual Crew writer: paused+living occupancy, full-cap resume, new-start rejection, current/old price, cancel, duplicate completion, failed readback and the existing over-admitted state; do not carry forward the old test asserting pause frees capacity. Actual Commerce path: event publication order, same-turn worker/D/X/route changes, direct versus distributed route inputs, new epoch/UNKNOWN/loss, LIFO3→1→2→3, selection load, reputation age/deactivation/identity exit, own-output recursion, exact3+48 retirement and no hidden-context frames. One readable current-state report and existing bounded log, not a new counter framework.

**One combined native session after local validation.** Use the current Industry campaign plus a Commerce III city with two working specialists and two eligible local domains. (1) With one living Crew and one paid paused order, new formation must be unavailable while old **续建** resumes at its old price/progress. (2) Open the delivered Commercialization entry, enable two domains, compare the named source/D/X and actual Gold, then remove/re-add one specialist: latest selection pauses and returns; no project enters the queue and old Commerce effects do not coexist. (3) One same-turn source change or route change verifies dependency delivery. One save/cold load may combine the new Commerce selection/reputation ownership with retained Crew occupancy; it is not another Probe default-OFF test. If IV is already convenient, one full turn checks reputation/effective-R separation; no40-turn grind. Existing Crew construction/N/E/L/discount acceptance is inherited. Enemy contact is opportunistic, not a forced separate session. Final button names and exact numeric expectations follow the implemented interface/approved precision.

Stop after this batch. COM-B/C/D remain separate, and no Culture HOLD or District-body purchase work is bundled.

## O：只读资格，三种路线关系分开

Use the accepted [background route source](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md), complete-sample proof, Gameplay epoch and endpoint references. Do not require a new pure-Gameplay all-route collector.

| Relationship | Qualification | Boundary |
|---|---|---|
| Commercialization | Self plus own city with a valid direct domestic route in either direction | Not center reachability; deduplicate partner cities |
| Development signing | Direct domestic Commerce source→target outgoing route | Reverse route insufficient; later route loss does not cancel signed contract |
| Capital S | Existing trade-route-connected domestic specialization network | Not the Commercialization pair pool, outgoing pool or global highest ACTIVE; expose actual eligible sources before selecting |

COM-A adds only the indexes it consumes; later batches extend the same verified snapshot as necessary. Facts/versions are read-only projections, not permanent ledgers. Invalidate on route/endpoint/Owner/reference/epoch changes. UNKNOWN is not empty; confirmed loss invokes exact withdrawal. No every-hover or per-consumer full-world rebuilding. Preserve existing scoped recovery and independent Culture/Industry consumers.

## P与S：配置、当前效果与制度历史分开

Commercialization uses `Gold_domain = 0.05 * D_local * X_highest_eligible_total_city_yield * (1 + 0.005 * R_effective)`. D is existing absolute infrastructure depth; X is total city Science/Culture/Production/Faith/Gold for the mapped domain, not district attribution. Exclude Commercialization-created Gold from X. Do not import the retired20% copy, a new cap, Industry Floor or Meaning's per-domain Floor.

Persist selected domains and activation order. Manual close removes one entry, reopening makes it newest. Capacity loss suspends latest selections; restoration resumes earliest first. Same Identity with ACTIVE loss retains configuration; Identity exit or Owner change clears it. Same-Owner/Identity load restores configuration and recomputes current effective entries, never restores an old yield snapshot.

Reputation starts on first **permanent Commerce IV institution**, not first current ACTIVE IV. Each complete Standard-speed turn retaining Commerce Identity adds1 up to40. ACTIVE loss retains and continues age, but current effects require ACTIVE IV. Identity exit resets; Owner change retains the institution record, unsupported owners do not run its mechanics. It multiplies Commercialization and later venture-failure refund only. Never copy Research's origin-owner clock policy or change an already signed contract.

### P正式cutover的精确责任

1. Retire only `BUILDING_SPC_DEV_LV3_COM_RESEARCH/CULTURE/INDUSTRY` (the3 old connected-kind specialist effects).
2. Retire only `BUILDING_SPC_B061_SCIENCE/CULTURE/PRODUCTION_0..15` (48 old Convergence effects), including its global-output callback and test controls. Preserve Types/definitions required for exact cleanup.
3. Close forward writers in Gameplay startup/requests, Bridge notification, native hooks, load/audit/return and isolation paths before cleanup; enable new output only after confirmed removal. Partial retirement holds only the affected output; never double-write a fallback.
4. Preserve baseline specialist support, housing/GPP, common topology, current CultureNetwork and StandardizationEffects. Keep the already retired Research network retired; do not restore it as a Capital prerequisite.

## Q：合同与隐藏保护有各自的持久权威

Commerce ACTIVE III can sign Capital Investment in implemented non-Commerce domains (currently Research/Culture/Industry); no local matching district required. D_eff=max(1,local D); S_eff=max(1,highest eligible current ACTIVE in the connected network), with no fabricated source when none exists. C=1.25 when this domain is actually commercialized, otherwise1. Each confirmation uses25% of then-remaining Treasury; term10 Standard turns; one unsettled contract per source city/domain, no national total cap.

Lock the concrete source/S cities and owner relations, quote version, principal, D/S/C, mode, returns, probability/outcome and maturity. Highest S ties use "earliest attaining that level" then stable key: clarify whether attainment refers to permanent institution or current ACTIVE before COM-B, since the current Store has no general ACTIVE-attainment history. Do not fabricate this from city age or receipt order.

`r=.01*D*S*C`; stable return `P*(1+r)`, venture success `P*(1+3r)`, failure `P*(.5+.005*R_effective)`. Base chance=min(.8,.4+.01*D*S). Hidden consecutive failure n belongs to source city+Owner, shared across its domains: `p=.8-(.8-p_base)*.75^n`; confirmation rolls/locks once and immediately updates n; success/Identity exit resets, domain/D/S changes retain, original-owner recapture restores valid own n. UI hides locked outcomes, shows total and net expected return; negative expected net does not prohibit choice.

Signed contracts survive ordinary ACTIVE/Identity/D/S/route changes. Source or locked S city Owner change terminates without refund/maturity/failure/pity settlement. Principal/return precision and debit+receipt crash windows require their own scoped tests; the new persistence warrants one maturity/reload test, not every old lifecycle ritual.

## R：报价与签约后的合同独立

Commerce ACTIVE IV plus a direct outgoing domestic route may fund an eligible target district's currently constructible next-tier building. Purchase eligibility is not required. Cost=`0.15 * theoretical Gold purchase price` under actual game/HD rules. No plot/food solver, raw-Production substitution or fixed10-turn term. Resolve price-reader context and final cost precision before COM-C.

Bind target city+district type. +50% Production applies only to that district type's buildings until its next eligible building completion, then withdraw and release occupancy. One active investment per target city across domains/sources; one source slot per working Commerce specialist. Existing contracts survive route, capacity, ACTIVE or Identity loss. Source/target Owner change ends with no refund and exact withdrawal. Later target invalidation remains an explicitly deferred edge, not invented compensation.

Reuse current Industry's effect family where appropriate, preserving separate owners and exact IDs. Standardization and Development percentages add; verify the combination once here. Inspect HD building prerequisites for alternative next-tier Theater/Neighborhood buildings only when they actually enter the catalogue. No new purchase rights, unit/Wonder/District acceleration or general Mod-compatibility framework.

## T：团队存续与绑定事务分别管理

Commerce ACTIVE IV trains a500P Standard-speed Team, production-only, protected from hostile capture/Owner conversion and without player deletion. Completed Team remains an original-owner asset even if its training city changes; source provenance differs from the later bound transaction target.

At a currently specialized target with Potential>=2, liquidation debits1 Potential once, closes old Identity and enters REALLOCATING. Non-Food yields and net Food surplus receive the accepted−75% disruption; do not reduce total Food or add population damage. After at least5 complete Standard turns, legal configuration in another eligible specialty district of the same city establishes new Identity at the debited Potential and consumes the bound Team. Elapsed time alone never restores Identity. Target transfer before configuration destroys this unfinished transaction/team per D0040/D0050; it does not erase every profession's historical asset. Existing signed investment contracts follow their own key-city rules.

COM-D reviews actual Identity/ACTIVE and exit/return consumers, validates disruption/protection and performs one complete transaction. It does not borrow the failed Expedition sleep-control route. Unsupported speeds, original-owner elimination or destroyed-city edge policies stay deferred rather than guessed.

## 明确未决项与技术门禁

| Item | Scope / timing |
|---|---|
| Fractional Commercialization Gold and exclusion of own amplified output | COM-A writer gate; no default Floor. A limitation requiring changed semantics goes to user |
| Capital earliest-attainment tie-break | Narrow Design clarification before COM-B; no impact on COM-A |
| Capital debit/returns and Development15% price precision | Decide at their respective implementation batch; do not pre-approve one rounding rule |
| Connected-network S source exposure | Technical COM-B boundary; common recipients/national max are not automatically the correct pool |
| Eligibility-independent theoretical purchase price / next-tier completion | Technical COM-C; no guessed formula |
| Team protection and actual net-food disruption | Technical COM-D; existing evidence is inherited only where the native path matches |
| Non-Standard speed; key city destroyed, original owner eliminated without transfer, Development target later invalid | D0050 deferred, nonblocking outside their named cases; retain conservative technical holds |

X, S ACTIVE/minimum/domain eligibility, Capital concurrency, venture n/Owner policy, Development pricing/duration/target limit and Standard-speed-only scope are already decided by D0050. They are not open Design questions anymore.

## 实施前重核、验证与交付约定

Use task-scoped Content objects and direct source/caller closure. Exact cutover IDs and current native getters must be checked at implementation; the Advisor report is not permission. Normal calculation reads only needed facts. Configuration/reputation are persistent business state; route/yield caches are derived, version-scoped and replaceable; UI snapshots are temporary, invalidated on input/selection changes and revalidated on confirmation. Diagnostics are bounded. No periodic timers, per-frame polling, extra GC or broad all-module migration.

This checkpoint contains source review, one actual-writer counterexample and documentation/context checks only. New Commerce has no LOCAL_SIMULATION_PASS or USER_GAME_TEST_PASS. New persistence/writer closure receives targeted L3, ordinary projection L2, text/layout L1. Inherit unchanged shared evidence and combine native steps by marginal information value. Publish only this batch's reviewed documentation; keep raw screenshots/logs and local reproduction ignored.

User decision: proposed B239 scope/precision gate for approval; Capital tie-break deferred to COM-B. User testing: none now. Primary next: implement only after scope approval; stop this planning checkpoint without code, runtime, configuration or deployment changes.
