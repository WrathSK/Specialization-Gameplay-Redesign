# Commerce implementation preparation

[现行商业设计](../../Design/Commerce.md)、[现行架构](../Specialization_v0.1_Architecture.md#current-authoritative-state)和 [Status CURRENT](../../Status/Specialization_P0_Status.md#current-authoritative-state)分别说明玩法、技术职责和实际进度。下文各检查点的状态、原生证据和限制按对应构建解读。

## 当前范围与停止点

现行网络待确认规则见 [Network Design](../../Design/Network.md#未确认不等于失效)及[配套架构](../Specialization_v0.1_Architecture.md#network-pending-hold-and-confirmation-recovery)。早期 B239/B240 的来源选择、采样和撤除分支沿用其原记录。

| 要追查的行为 | 实施与验证入口 |
|---|---|
| 商业化配置、信誉、当前金币和精确退出 | [B239 配置与信誉](#b239-implementation-and-validation)、[B240 来源与金币](#b240-implementation-and-validation) |
| 资本投资的锁定条款、保存和真实收据 | [B241 合同与结算](#b241-implementation-and-validation)、[B244 保存精度](#b244-lossless-capital-storage)、[B245 原生金库收据](#b245-bounded-native-money-receipts) |
| 发展投资的报价、目标和退出 | [B246 发展投资](#b246-development-investment) |
| 资产清算、配置及训练就绪 | [B247 身份事务](#b247-implementation-and-validation)、[B248 训练入口](#b248-training-access-follow-up)、[B249 启动与恢复](#b249-event-driven-readiness) |

[B489 两种环境的限定实机记录](../../Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047)记录实际比较和证据范围。早期商业化与施工队联合批次、资本投资和资产重组的实施计划见[固定发布版本](../../Historical/README.md#delivered-commerce-and-industry-implementation-plans-in-git-history)。

## 当前落地与可复用范围

以下为原准备阶段的直接实现与审计依据。具体运行模块的职责从现行架构进入。

### 已确认的直接实现面

- Primary read the local Stable Advisor report `Specialization/Reports/Advisory/Commerce_Plan_Review/Commerce_Plan_Audit.md` (SHA256 `7e94a5be592d771bea8142c7b2887da200e3b77aa92e89381f7d7b1de8f18458`, basis B231/`0ee4dc9`). It remains advisory and unchanged. Its linked unpublished dependency reports are not silently added to this checkpoint; the necessary planning conclusions are recorded here independently.
- C1 is confirmed: D0050 closes most old Design blockers. C3 is useful, but the three route relationships must remain separate. C4's S tie-break is still a narrow user decision for COM-B, not a COM-A blocker. C5 is interface-specific precision, not permission to round.
- Revalidated since the Advisor baseline: B232 proof/recovery publishing, B233 typed Industry knowledge, B234 current Standardization/Research-network retirement, and B235 Engineering state. Research's retired network effect is not a dependency of Capital's future ACTIVE lookup. Current `NetworkBridge.CurrentNational` covers Research/Culture aggregate projections, not a general per-domain connected-component membership API; it must not stand in for S selection.
- C2 primitive suggestions remain STATIC_CONFIRMED in the Advisor's cited loaded database, not re-executed native results here. Reuse current Industry production primitives for COM-C where semantics match; do not create a second modifier framework. B246 now supplies native quotation evidence for the submitted candidates; broader candidate/purchase-state combinations are not inferred.
- C6's event-first, Gameplay-owned writer, pre-native project interception, bounded diagnostics and context-faithful tests are adopted as implementation requirements. No timer/frame polling, extra GC or UI-open dependency.
- C7/C8 are planning advice: use existing specialization vocabulary, keep owners/lifecycles separate and schedule Restructuring last. Do not add a generic future-profession registry in COM-A or unify contracts merely because they share a Modifier API.

## O：只读资格，三种路线关系分开

Use the accepted [background route source](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md), complete-sample proof, Gameplay epoch and endpoint references. Do not require a new pure-Gameplay all-route collector.

| Relationship | Qualification | Boundary |
|---|---|---|
| Commercialization | Self, plus own direct domestic partners in either direction with the corresponding specialization Identity | Self is Identity-exempt; local domain district still required. No external ACTIVE/Governor/Potential/district gate, transitive reachability or qualification forwarding |
| Development signing | Direct domestic Commerce source→target outgoing route | Reverse route insufficient; later route loss does not cancel signed contract |
| Capital S | Existing trade-route-connected domestic specialization network | Not the Commercialization pair pool, outgoing pool or global highest ACTIVE; expose actual eligible sources before selecting |

COM-A adds only the indexes it consumes; later batches extend the same verified snapshot as necessary. Facts/versions are read-only projections, not permanent ledgers. Invalidate on route/endpoint/Owner/reference/epoch changes. UNKNOWN is not empty; confirmed loss invokes exact withdrawal. No every-hover or per-consumer full-world rebuilding. Preserve existing scoped recovery and independent Culture/Industry consumers.

## P与S：配置、当前效果与制度历史分开

Commercialization uses `Gold_domain = Floor(0.05 * D_local * X_highest_eligible_total_city_yield * (1 + 0.005 * R_effective))`, then sums domains (D0054). D is existing absolute infrastructure depth; X is total city Science/Culture/Production/Faith/Food for the mapped domain, not district attribution. Harbor reads total Food, not surplus (D0055). Take the maximum over self and matching-Identity direct partners, never their sum. All inputs are non-Gold; do not withdraw/reapply Commercialization Gold to sample X, subtract a historical Gold estimate or add a recursion solver. Do not import the retired20% copy or a new cap; the Floor here is its own explicit D0054 decision.

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

Commerce ACTIVE IV plus a direct outgoing domestic route may fund an eligible target district's currently constructible next-tier building. Purchase eligibility is not required. Cost=`0.15 * theoretical Gold purchase price` under actual game/HD rules. No plot/food solver, raw-Production substitution or fixed10-turn term. B246 uses the UI-context native cost getter independently of purchase permission; an unreadable eligible alternative holds that district quote. D0057 chooses the minimum eligible next-tier price and exposes its building as quote evidence, never a bound completion target. Preserve the fractional15% result; the user authorizes the existing <=0.01 per-call native receipt allowance, not price rounding or an invented conversion.

Bind target city+district type. +50% Production applies only to that district type's buildings until its next eligible building completion, then withdraw and release occupancy. One active investment per target city across domains/sources; one source slot per working Commerce specialist. Existing contracts survive route, capacity, ACTIVE or Identity loss. Source/target Owner change ends with no refund and exact withdrawal. Later target invalidation remains an explicitly deferred edge, not invented compensation.

Reuse current Industry's effect family where appropriate, preserving separate owners and exact IDs. Standardization and Development percentages add; the submitted B246 targets had no Standardization contribution, so verify this combination once in a later convenient session. Inspect HD building prerequisites for alternative next-tier Theater/Neighborhood buildings only when they actually enter the catalogue. No new purchase rights, unit/Wonder/District acceleration or general Mod-compatibility framework.

## T：团队存续与绑定事务分别管理

Commerce ACTIVE IV trains a500P Standard-speed Team, production-only, protected from hostile capture/Owner conversion and without player deletion. Completed Team remains an original-owner asset even if its training city changes; source provenance differs from the later bound transaction target.

At a currently specialized target with Potential>=2, liquidation debits1 Potential once, closes old Identity and enters REALLOCATING. Non-Food yields and net Food surplus receive the accepted−75% disruption; do not reduce total Food or add population damage. After at least5 complete Standard turns, legal configuration in another eligible specialty district of the same city establishes new Identity at the debited Potential and consumes the bound Team. Elapsed time alone never restores Identity. Target transfer before configuration destroys this unfinished transaction/team per D0040/D0050; it does not erase every profession's historical asset. Existing signed investment contracts follow their own key-city rules.

COM-D reviews actual Identity/ACTIVE and exit/return consumers, validates disruption/protection and performs one complete transaction. It does not borrow the failed Expedition sleep-control route. Unsupported speeds, original-owner elimination or destroyed-city edge policies stay deferred rather than guessed.

## 明确未决项与技术门禁

| Item | Scope / timing |
|---|---|
| Commercialization source / precision | D0055 and per-domain Floor implemented; B240 tested values/city modifiers/source filtering/withdrawal accepted. Treasury contract precision is a separate upcoming gate |
| Capital earliest-attainment tie-break | D0056 user confirms earliest establishment of the corresponding permanent institution level; missing reliable dates are not guessed |
| Capital debit/returns and Development15% price precision | B245 native accepted within observed cases; all four B246 debits match their quotes exactly. Preserve the <=0.01 per-call guard and fractional pricing; no universal precision claim |
| Connected-network S source exposure | Technical COM-B boundary; common recipients/national max are not automatically the correct pool |
| Eligibility-independent theoretical purchase price / next-tier completion | B246 submitted native prices and one eligible completion accepted; no guessed formula or claim for every alternative |
| Team protection and actual net-food disruption | Technical COM-D; existing evidence is inherited only where the native path matches |
| Non-Standard speed; key city destroyed, original owner eliminated without transfer, Development target later invalid | D0050 deferred, nonblocking outside their named cases; retain conservative technical holds |

X, S ACTIVE/minimum/domain eligibility, Capital concurrency, venture n/Owner policy, Development pricing/duration/target limit and Standard-speed-only scope are already decided by D0050. They are not open Design questions anymore.

## 实施前重核、验证与交付约定

Use task-scoped Content objects and direct source/caller closure. Exact cutover IDs and current native getters must be checked at implementation; the Advisor report is not permission. Normal calculation reads only needed facts. Configuration/reputation are persistent business state; route/yield caches are derived, version-scoped and replaceable; UI snapshots are temporary, invalidated on input/selection changes and revalidated on confirmation. Diagnostics are bounded. No periodic timers, per-frame polling, extra GC or broad all-module migration.

The original preparation review contained source evidence and one actual-writer counterexample only. B239/B240 local evidence is scoped below; the user accepts B239 capacity, report D/Reputation response and observed reputation growth, and B240 adds user acceptance of actual values/city modifiers/source filtering/withdrawal and the Commerce reload. New persistence/writer closure receives targeted L3, ordinary projection L2, text/layout L1. Inherit unchanged shared evidence and combine native steps by marginal information value. Publish only this batch's reviewed source/tests/documentation; keep raw screenshots/logs and local reproduction ignored.

User decision: B247 explicitly authorized; D0057 retained. User testing: one restructuring flow after guarded deployment, with a cold load during REALLOCATING. B246 acceptance remains scoped; additive Standardization stays opportunistic. Primary next: stop after this authorized batch.

## B239 implementation and validation

Historical B239 baseline, retained for provenance. Source eligibility and clean-Gold sampling below are superseded by B240; its original local result is frozen. B239 implemented the approved Crew occupancy repair, COM-A configuration/effects and Reputation; [local result and one combined native flow](../../Status/Validation/Results/Specialization_B239_Commercialization_Local.md).336 targeted checks pass; native Gold/clean-source freshness/UI/new persistence are pending. Current source/deployment remains solely in Status/Authority.

| Authority / resource | Owner and lifetime |
|---|---|
| Selected domains/order | CommerceModel + optional Store commerceKnown/value; maximum5, same-Identity load restores, Owner change clears; current suspension is derived |
| Reputation | Store starts at verified third investment, ticks complete Standard turns independently of ACTIVE, caps40 without further writes; unsupported Owner freezes, return excludes foreign gap; missing expected history held |
| D/X/current ACTIVE/workers | Current native/shared facts; one temporary audit batch, remote X does not require remote district/identity/Store; no stored yield snapshot |
| Direct routes | NetworkBridge private verified direct-pair index, copied API CurrentDomesticPartners; UNKNOWN distinct empty; transport-limit reason explicit, no partial route set |
| Gold/access | Commerce owns exactly31 Gold bits + one opener marker; staged own-Gold withdrawal → all plans → publication for Harbor inputs, exact readback/cleanup and residual diagnostics |
| UI | One pre-enqueue production opener, visible five-domain dashboard, immutable copied view, one explicit scalar select request with reference/token/revision; no hover request or timer |
| Pending/dependencies | Event-coalesced dirty cities and reverse X dependencies; replace memberships on new inputs, clear on confirmed loss; other profession native writes mark their real source city |
| Legacy | Exact3 Commerce flags +48 Convergence retired. No forward request/start/global-output audit; startup withdrawal only supported Store-confirmed cities. Other professions/basic support/topology retained |

First entry uses the existing permanent-city callback after Store/Claim commits; investment refresh is immediate and city-scoped. Construction callbacks do not treat district-type argument as cityID. No new periodic scan, GC, persistence framework or general Store rewrite. Existing eight-city Shared D cache remains unchanged; local-only D avoids new remote completeness scans.

The approved Floor is exclusive to Commercialization. New actual-Gold freshness after withdrawal is native-pending; encoding failure holds instead of clamps. Existing P4 without a reliable reputation start is explicitly unavailable; begin native reputation acceptance with III→IV. Failure cleanup does not claim zero while owned carriers remain.

After deployment, the one combined flow covers Crew pause/resume occupancy, two Commercialization selections and specialist restoration, one real same-turn source change, one Reputation turn, and one combined cold load. Inherit previous Industry and shared lifecycle acceptance; do not repeat old Probe rituals. Stop at B239; Capital/Development/Restructuring remain separate.

The current speed must reliably resolve to Standard by GameSpeedType. Other/unknown speeds hold Commerce effects and do not start/tick Reputation, without blocking ordinary investment commits or erasing existing business history. No guessed speed scaling.


## Network pending rule supersession

The accepted [network pending/confirmation contract](../Specialization_v0.1_Architecture.md#network-pending-hold-and-confirmation-recovery) supersedes B240's implemented withdrawal of Commercialization Gold when network inputs are temporarily unavailable. The B240 table distinguishes source-Identity UNKNOWN but did not specify the broader pending-network branch precisely; the old native/local reports remain frozen evidence, not the new rule. Keep last-applied network-derived carriers while pending, including cold load; confirmed eligibility loss and confirmed route loss retain their respective exact exits. Capital/Development transaction requirements and signed-contract survival rules remain unchanged. See [Design waiting rule](../../Design/Network.md#未确认不等于失效). Runtime adoption and native evidence are recorded by stage in Status.

## B240 implementation and validation

D0055 is implemented in the existing Commerce consumer. The [B240 native review](../../Status/Validation/Results/Specialization_B240_Native_Review.md) closes the tested scope; the former test flow below is retained as the implementation record, not a repeated assignment. [Local result and minimal native flow](../../Status/Validation/Results/Specialization_B240_Commercialization_Local.md).109 distinct targeted tests pass. This is LOCAL_SIMULATION_PASS, not native Gold, animation, CPU or memory acceptance.

| Input / state | Ownership and update contract |
|---|---|
| External source qualification | Verified direct domestic partners plus Store.Base Identity. Store.Owns distinguishes unenrolled cities from unreadable owned records; UNKNOWN holds rather than inferring identity. P.Family supplies only implemented profession mappings. Self is exempt, while local district eligibility remains unchanged |
| Source facts | City.GetYield for mapped total Science/Culture/Production/Faith/Food. Identity and yield reads are reused only inside one audit batch; no remote building scan, Governor/ACTIVE read, new persistent field or cross-batch yield cache |
| Dependencies | Retain every direct partner in reverse dependencies, including currently nonmatching identities. Identity commits can newly qualify a source; existing route/native fact/permanent-write and confirmed-loss/return callbacks deliver updates. Same-turn changes remain observable |
| Gold writer | Existing31 owned Gold bits and access marker. Compute non-Gold inputs, compare actual owned effects and change only differing bits. No source withdrawal/restoration phase. Unchanged updates and deferred native yield echoes perform zero effect writes; real changes, startup reconstruction and confirmed exit retain exact cleanup/readback/residual protection |
| UI | Five fields remain visible even when unselected. Missing local district takes precedence over not-selected, with a disabled-button explanation; Harbor says total Food. P0 reads the published view, never triggers recompute. Configuration remains the pre-enqueue production-list action |
| Permanent / temporary state | Existing Store selection/order and Reputation are unchanged. Batch facts expire when Audit returns; dirty input is event-flushed, dependency membership replaced on changes/exit, UI remains a copied read model. No timer/frame polling/GC change |

With only four professions implemented, external Holy/Harbor sources are not fabricated: these domains can currently use the Commerce city's own Faith/Food when its local district exists. This does not enable future specialization gameplay.

The targeted checks cover actual Commerce/Store/route/UI/SQL integration, including wrong Identity with higher yield, absent/unreadable identity, source exit/recovery, no remote D read, Food zero/change, no-change/deferred-event idempotence, cleanup failure, selection and reputation persistence. The three obsolete B239 clean-Gold test cases were replaced by D0055 counterexamples; frozen B239 evidence and unrelated assertions remain unchanged.

Native verification is one continuous Commerce session: local prerequisite/report clarity; Harbor total-Food/Gold comparison with no repeated building refresh; an available direct matching-Identity source; one same-turn source change and disabling a field. Finish the already pending Commerce configuration/Reputation save/cold-load check once, without repeating Crew, Academic Tradition or old Probe OFF/re-enable rituals. Use existing bounded logs; screenshots only for an actual yield/UI discrepancy. Stop after B240; Capital/Development/Restructuring need separate authorization.

## B241 implementation and validation

D0056 is implemented as B241.268: [local result, state/failure contract and one native flow](../../Status/Validation/Results/Specialization_B241_Capital_Local.md). 155 targeted checks pass; native money and the new contract save/maturity closure are pending. One ordinary capital panel covers stable and venture modes; old Commercialization/Floor and other modules retain their contracts.

Authoritative contracts/n live in the existing Store's optional per-city capital extension; pure schema/math live in CapitalInvestmentModel. The Store records actual permanent-institution establishment times on new confirmed investments, exposes guarded capital reads, and increments a confirmed-loss continuity counter. `CurrentCapitalSources` exposes the existing verified center/recipient source IDs, with current proof/reference checks. Unknown real tie dates hold that quote instead of inventing history. No separate topology, reverse city index or shared save-framework rewrite.

Treasury remains native authority. Persist INTENT/CALLING before the native operation; only immediate matching readback permits ACTIVE/SETTLED. A saved final receipt is not replayed; unknown CALLING holds without guessing from later balances. Quotation and UI are replaceable views; outcome/n stay private until settlement. Three domain slots retain only current/latest contracts. Existing turn/load/confirmed-transfer events drive business transitions; network/Commerce publications mark quote reads dirty. UI/publish never debits, rolls or settles. Access marker has no yield and uses exact loss cleanup.

The new native delta is Gold debit/credit precision and persisted contract settlement. Request the one combined session in the result, including one midterm cold load; inherit B240/old harness evidence. No new timer, frame polling, GC, AI specialization, Development Investment or Restructuring. User decision: accepted tie-break, no new rounding semantics. User testing: pending. Primary next: W0003 safe deployment if the game is verifiably closed, then stop at the native gate.

## B242 confirmation diagnostics

The [B241 first-confirmation review](../../Status/Validation/Results/Specialization_B241_Native_Review.md) supersedes its earlier pending-test handoff, without changing the frozen local result. The user authorizes only stage/readback evidence and honest paused feedback. [B242 implementation, validation and minimal session](../../Status/Validation/Results/Specialization_B242_Capital_Diagnostics_Local.md).

An optional failure-only observer at the existing Store readback boundary passes already obtained values into a bounded pure projection; it performs no additional native read or write. Request-local phase details and a single per-city failure in the existing replaceable view are observational, never persisted authority or permission to replay. Existing debit/credit intent/calling/receipt order, schema, failed-write reservations, per-city isolation and economic calculation remain unchanged. OPEN/REFRESH accepted means the read request was handled; view stage/canSign/reason independently describe whether signing is possible.

No timers, frame checks, new GC or source/world scans.194 targeted tests pass; native cause remains UNKNOWN. User testing is one confirmation plus one paused refresh if needed, with the existing manual collector. No new full save/load/settlement sequence in this diagnostic batch. Stop after guarded deployment and await evidence; COM-C/D remains unauthorized.

## B243 reliable failure observation

The [B242 native evidence](../../Status/Validation/Results/Specialization_B242_Native_Review.md) remains frozen. The user explicitly authorizes the [B243 restricted-Lua diagnostic repair](../../Status/Validation/Results/Specialization_B243_Capital_Diagnostics_Local.md). Ordinary guarded table reads remove the rawget dependency. The request retains base observation facts before protected detail projection/merge and distinguishes COMPLETE, ERROR and NOT_OBSERVED without changing the original Store error or allowing retry. Expected/actual numeric log values preserve round-trip precision; gameplay values remain unchanged.

123 targeted methods pass, including actual-Store failures, no-replay/isolation, unchanged per-value/Property-work comparison and existing bounded collector behavior. Store/model/UI, economic rules, permanent state and validation protections are unchanged. No timer, scan, GC or framework rewrite. After guarded deployment, one confirmation and one paused refresh if needed provide the missing native evidence; this batch does not claim that native signing is fixed. Stop for the log, without COM-C/D or new Design work.

## B244 lossless Capital storage

The user explicitly authorizes the [B244 representation-only repair](../../Status/Validation/Results/Specialization_B244_Capital_Storage_Local.md) after the [B243 native precision finding](../../Status/Validation/Results/Specialization_B243_Native_Review.md). Model-owned `DECIMAL17_V1` stores the ten monetary/probability/receipt fields as canonical round-trip text; Store's Capital readers/writers, validator and confirmed-loss termination adapt at that boundary. Public consumers still receive numeric business state. Raw Store envelopes retain exact pre/post comparisons; malformed/unknown encoding holds. No old-record reconstruction or second ledger.

A0171 documents only this Capital wire-format contract. Monetary rules, Treasury mutation/readback, no-replay receipts, hidden protection, references and generic Store guards are unchanged.121 selected methods pass, including26 new precision/failure/fresh-VM checks and immediate-baseline value/work comparisons. No timer, new scan, GC or collector/UI change. After safe deployment, one contract covers signing, midterm cold load and one-time maturity; local conversion is not native acceptance. Stop for that evidence, without COM-C/D or a money-rounding decision.

## B245 bounded native money receipts

The user accepts a per-native-call absolute discrepancy of at most 0.01 Gold and authorizes the [B245 receipt implementation](../../Status/Validation/Results/Specialization_B245_Capital_Receipts_Local.md). This supersedes B241–B244's tighter native monetary matching only; principal/return/probability formulas and strict raw Property equality stay unchanged. Each call requires readable balances and an actual nonzero change in the requested direction, then stores the actual debit/credit independently of theoretical amounts. No compensation, retry, rounding or cumulative correction is permitted. Exceptions, unknown outcomes and out-of-bound changes retain the existing CALLING/hold protection.

Capital business version 2 requires actual receipts; existing DECIMAL17_V1 encodes the additional three finite values. Store ownership, bounded three-slot lifecycle, loss handling and event wiring are unchanged. There is no old-attempt repair or general schema migration. Quotation/UI are derived, actual settled net uses observed paid minus debited, and the existing bounded trace records exact numeric evidence. 142 selected local methods pass, with coherent B244/B245: 14 reads/7 writes/2 money calls/0 cross-record uniqueness visits. Native debit, cold-load receipts and maturity still require the combined user test; local work equality is not a performance or engine-precision claim.

## B246 Development Investment

Approved scope: Development Investment only, plus its direct Store/network/UI adapters. D0057 selects the lowest theoretical Gold price among currently constructible next-tier candidates; the displayed building is quotation evidence, not contract identity. Preserve15% fractional pricing, the existing native <=0.01 debit receipt tolerance, exact saved values and no retry after an unresolved call. No refund or maturity timer; no new timers/frame polling, GC, Restructuring or other-profession work.

- **Facts and ownership.** `DevelopmentInvestmentCatalog` builds static ordinary HD-tier definitions once per context. UI `DevelopmentInvestmentRead` reads current district completion, building presence, native `CanProduce(hash,false,true)` and `city:GetGold():GetPurchaseCost(YIELD_GOLD,hash)` only on open/refresh/confirm. It never asks purchase permission or substitutes Production. The existing verified network input exposes a separate direct-outgoing projection; no transitive or reverse route qualification. Current source workers come from the established district/plot worker facts, independent of Commercialization yield readiness.
- **Persistent authority.** Source city Store records gain optional `developmentKnown/development`, with a model-owned DECIMAL17_V1 representation of numeric terms/actual receipts. One latest contract per target history token keeps records bounded by city relationships, not action count. City references retain Owner/change generation. Store equality, unknown reference guards and normal local-write isolation are unchanged. Current buildings/Gold/routes/ACTIVE are not saved as new authorities; only the signature facts needed to identify later completion and the locked quote/receipt are retained.
- **Confirmation.** A local selection sends only IDs and its revision/token. Re-read the chosen target and source qualification, compare the quote and prior saved state, reserve occupancy, save intent/calling, invoke one native debit, read its actual amount, save ACTIVE receipt, then apply the owned effect. Native errors or failed receipts retain a bounded session reservation or persistent held occupancy; no compensation/retry. A fresh load holds CALLING and closes a definitely unused INTENT; it never fabricates a receipt.
- **Effects and exits.** Dedicated district-building +50% carriers use the existing native Production family and preserve Standardization's ownership. Compare before write. A newly present eligible building in the selected domain ends the contract, including a different alternative or direct purchase/Cheat completion; repairing an already-present building does not. Route, specialist, ACTIVE or Identity decline only blocks new signatures. Confirmed source/target transfer terminates, withdraws and releases the slot without refund. Destruction/original-owner extinction/later target invalidation remain deferred Design boundaries, with unknown facts held rather than guessed.
- **Event and temporary lifecycle.** Existing building/transfer/load/turn/publication events and source/network invalidations drive work. A building event visits relevant outstanding records; normal publication processes only dirty source views and never constructs full quotes. Turn-boundary reconciliation checks only saved outstanding contract targets. Quotes are replaceable per-source snapshots and invalidated on relevant input changes; current UI selection is local and discarded on close/owner/load. Service mirrors are rebuilt from Store, occupancy is derived, session reservations survive uncertainty only within their context. Diagnostics reuse the existing bounded96-entry channel and collector. No parallel persistence/cache framework or polling fallback.

[Local verification and the single native flow](../../Status/Validation/Results/Specialization_B246_Development_Investment_Local.md) report137 selected methods (57 new,80 direct retained), Lua5.1 syntax, loaded-HD SQL and UI protocol checks. Static getter/Modifier evidence is not native pricing/additive-output proof. Ordinary publication has zero repeated native quote calls/effect writes in the tested idle case; this is not a native CPU or memory improvement claim. B245 Capital acceptance remains inherited and separate.

## B247 implementation and validation

B247.274 implements the approved Standard-speed slice. [Local evidence and native flow](../../Status/Validation/Results/Specialization_B247_Restructuring_Local.md) separate current facts, persistent history and native operation receipts.

Store retains original admission/identity/investment evidence and adds one optional current-identity transaction with explicit REALLOCATING, CONSUMING, SETTLED, DISCARDED and post-loss UNASSIGNED states. EffectiveFacts remains the consumer authority; no negative Settler receipt or rewrite of original Identity. Later investments belong to the new identity epoch, with retained old receipts and explicit first-P4 evidence. Existing exact-save/readback/occupancy protections remain; in-flight identity reads cannot publish an optimistic candidate.

The completed team owns original-owner provenance; the target city owns the transaction. Liquidation reserves the team target before the one-time P−1 save. Configuration saves intent, performs one native consume, records observed absence and commits only from a confirmed consumption receipt. Failed/unknown outcomes hold; cold load never blindly repeats destruction. Target loss discards the unfinished transaction/team and uses current claim candidates on recapture, while separately retained profession histories keep their accepted policies.

The source/target selection uses current native districts; access, disruption and UI are derived. Successful committed transitions publish through existing network/profession APIs; a local Standardization entry reconciles current eligible facts. Research tradition pauses, completed Culture/Industry histories remain, Commerce reputation/selections/failure protection reset, and signed investment contracts continue under their own owner-change rules. Five elapsed game turns only enable the explicit same-city configuration action. No wall-clock timer/frame fallback, GC change, general save/event refactor or automatic completion.

Native training is fixed 500 Production with PopulationCost 0 and no purchase/copy escalation. Native safe-retreat is reused; B248 replaces the original Builder presentation with installed Monopoly++ Investor art/icons (explicit provider dependency); delete UI/hotkey/callback is blocked only for this team. Established institutions, including Commerce, render as history where no longer current. Temporary event pairs, views, previews and diagnostics have defined replacement/turn/load/removal boundaries.

240 selected local methods pass, including actual dispatcher/Store/support/network input and real contract persistence/settlement tests; actual yields, protected native movement and the new real-save transaction remain USER_GAME_TEST_REQUIRED. Source and live deployment remain separately recorded in Status. B246 Standardization+Development overlap remains an optional later observation; no unrelated audit repair or next Commerce batch is implied.


## B248 training-access follow-up

[Evidence and minimal native gate](../../Status/Validation/Results/Specialization_B248_Training_Entry.md). The reported already-IV city has no training entry after load. Loaded unit definitions exist, but the submitted bounded log lacks the native prerequisite/list observation; that specific cause remains unresolved. A separate actual-Store reproduction confirms the missing committed-investment notification, now connected to a city-scoped Restructuring.Refresh. No new state authority, marker retry loop, timer, training rule or transaction change.

Read-only production-list diagnostics distinguish service readiness, marker readback, native visibility/eligibility and the existing list item. The UI never inserts the unit or substitutes for native qualification. Investor presentation uses the installed provider's art and atlas definitions; its gameplay is not inherited. Existing other-unit art remains unchanged.58 selected local methods pass; the native entry check precedes the original pending B247 transaction/cold-load flow.

## B249 event-driven readiness

[B248 evidence and B249 repair](../../Status/Validation/Results/Specialization_B249_Restructuring_Startup.md). The native service remains unready in both loaded and new-game observations. Its sole LoadScreenClose gate is replaced by one idempotent initializer using existing Store readiness, current facts and marker definitions. Start, existing publication/player/city events and optional load notifications can enter it; no P0 action or timer is required. WAITING/HELD dependencies preserve pending work rather than publishing guessed access.

Initial recovery owns only a bounded set of scalar references for the supported Store-owned cities present at startup. Each is removed on successful reconciliation, invalidation/confirmed exit or context disposal. Failed recovery is retried only when a relevant existing event visits that city. Derived markers remain native state; Store and unit Properties remain the transaction/binding authorities. Confirmed consumption may finish once; an unconfirmed native call stays held without replay.

Duplicate load notifications are refresh signals, not new Gameplay contexts: they cannot erase training pairs, action previews or views. Fresh-context Start owns those tables, and existing unit/turn cleanup remains. Bounded readiness reasons distinguish dependency waits from per-city reconciliation failure. The approved change updates initialization/ephemeral-lifecycle behavior only; cost, capacity, binding, transaction and effect contracts remain unchanged.80 selected local methods pass; native training entry and the original transaction/cold-load flow remain pending.
