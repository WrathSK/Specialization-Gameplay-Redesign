# Commerce Freeze Candidate — review against D0031

Document Owner: Codex
Design Authority: User
State: FREEZE_CANDIDATE / TWO_REQUIRED_DECISIONS_PENDING
Proposed revision: D0032, NOT_ALLOCATED
Scope: Design documents only. Not Architecture adaptation, UI implementation or runtime promotion.

## Authority and freeze gate

Candidate mechanical record: [Commerce candidate](Content/Commerce_Freeze_Candidate.json), NOT canonical. Current accepted Spec remains D0031, unchanged. Research_D0031, Industry_D0031, Culture_D0029, Shared_D0028 and all historical files retain bytes. After required answers, proposed D0032 should freeze current Spec and introduce Commerce content, Industry capacity closure and Culture approved presentation direction. No D0032 authority is created in this review.

Freeze means accepted core design, not BALANCE_COMPLETE, TECHNICALLY_CONFIRMED, IMPLEMENTED or USER_GAME_TESTED. User expressly permits deferral of domain source-value mapping, quote fundamentals/formulas, reputation targets, stacking, speed scaling and future Legacy. These items must remain visible and be decided before their dependent implementation; no default20%, share conversion, floor, source-Identity filter or contract behavior may be inferred from old Convergence.

User follow-up: only Potential>=2 may liquidate; successful configuration consumes restructuring Team. Team loss after liquidation is explicitly deferred, not silently solved by replacement/rollback. All Commerce levels retain3F/3P; old5F/5P upgrade cancelled. Two response-dependent decisions remain pending in candidate contracts: COM-BLOCK-01 hidden pity sharing scope; COM-BLOCK-02 live Development contract route interruption. Their answers change gameplay, not only numbers. No default chosen; formal freeze and revision creation wait for answers.

## Legacy audit / precise supersession

| Previous authority | Decision |
|---|---|
| COM-0013F3P and Trade Center identity | RETAINED; food/production support all levels per follow-up |
| SHARED-001 / COM-002 | RETAINED district+each tier1Housing, ACTIVE>=2; institution is not a housing Building |
| SHARED-002 / COM-002 | RETAINED +2 base Merchant GPP per working specialist, normal modifiers |
| COM-0035F5P | SUPERSEDED explicitly by user; not cancelled merely for symmetry |
| COM-003 connected-kind+2S/C/P | SUPERSEDED by new Lv3 packages |
| COM-004–00920% direct actual-source copy and floor | SUPERSEDED; no additional S/C/P convergence alongside Gold commercialization |
| Old IV-exclusive self-reception | Already SUPERSEDED D0009, not revived |
| NET-001–004 centers, direct reception/distribution | RETAINED shared infrastructure; not Commerce-only ability/payload |
| Old incoming-only source rule | Not new commercialization rule; direct route either direction qualifies, development remains outgoing only |

No recent accepted new Commerce mapping/quote formula found in canonical Design content. Historical runtime reports of20% actual-city yield are evidence of old implementation, not new mapping authority. No silent import from HD or Shared yield-share mapping.

## Narrow cross-design consistency

1. Development and Industry Standardization coexist with independent causes and qualification. Both may affect construction; combined stacking remains expressly pending, no strongest/additive/multiplicative assumption.
2. Restructuring liquidation leaves Research Identity, so D0031 tradition pauses. Retained age resumes on return without catch-up; current effect still needs Research ACTIVE4. Do not infer Culture/Industry/Commerce Legacy from this.
3. REALLOCATING must be excluded ordinary NONE/first-completion/Legacy Claim. The new explicit exception to old permanent-Potential/locked-Identity language belongs in Spec, not a hidden implementation workaround.
4. Commercialization references Shared D, including same-domain maximum single district, cap10, ordinary-only and pillage exclusions. It does not automatically adopt Research/Culture coefficients or shares.
5. Government/Diplomatic source-value mapping stays open; Shared domains do not decide economic source value. No unrelated profession changes.
6. Capacity2 binds completed Teams to training Industry source. Each tier1slot, IV noextra; downgrade/respecialization does not delete existing units. Source binding and creation-at-cap are future implementation gates. Captures/owner transitions remain explicitly unresolved.
7. Hybrid D uses Culture_D0029 work_pool/era rules including unknown-work exclusion. Domestic era index is an information lookup, never civilization-wide Dialogue X.

No new shared economic formula needed. Shared_D0028 remains unchanged. Spec records cross-system REALLOCATING exclusion; no generic finance/state schema is implemented. Commerce design content extends schema-v1 with nested contracts, parameters, supersession, legacy and architecture requirement registries; these are documentation objects, not a save schema.

## Architecture adaptation requirements — not an implementation

- Current Identity / Historical State / REALLOCATING are separate. Per-city/per-specialization former institutions/historical max cannot reactivate abilities or count as infrastructure.
- Persistent unique investment contracts: source/target/domain/mode/principal/start/maturity/locked outcome/quote version/effect lifecycle; exactly-once settlement and action deduplication, save/load preservation.
- Persist hidden pity and reputation, and authoritative toggle activation order for LIFO. Neither UI order nor current carriers reconstructs authority.
- Keep directional route endpoints; commercial direct undirected qualification and investment outgoing qualification are distinct predicates.
- Two-stage restructuring transaction persists independently of Team: original/reallocatable capital, city/reference, source/Team, liquidation/disruption dates, destination and completion. Lost-Team policy remains user-deferred.
- Existing Crew project grant (`Mod/Data/CrewProjects.sql`) creates unit via native completion modifier. Current Crew access and action receipts are not a persistent training-source capacity registry. Future binding must connect each completed Team with one source and release exactly once on consumption/legal removal; no continuous empire scan as substitute.
- Gameplay computes one combined panel snapshot and revalidates confirm; local UI selection/hover reads cached facts. Intercept project action before native production request. No fake production completion/queue restoration.
- Protect A–D2 contracts and av2-runtime-b076.103; no repeated audits, periodic polling or per-hover requests. Existing historical AV2-I001 maps are not claims that B076 still performs old scans.

## Static technical investigation

STATIC_CONFIRMED means inspected local source/database, not native gameplay verification. Database inspected read-only; it is a cached loaded catalog, not proof of every future Mod combination.

### Food Surplus

Native `Base/Assets/UI/CitySupport.lua:486–492` reads `GetFoodSurplus()` separately and calculates projected gain as surplus × `GetOverallGrowthModifier()`. Loaded DynamicModifiers maps `MODIFIER_SINGLE_CITY_ADJUST_CITY_GROWTH` to `COLLECTION_OWNER / EFFECT_ADJUST_CITY_GROWTH`. HD `SubMods/CityPolicies/CityPolicies.sql:122,172` uses that modifier with Amount−75 for labor policy. Its separate consumption modifiers are not part of this proposed effect.

This establishes a growth-stage candidate rather than total-food penalty. TECHNICAL_INVESTIGATION_REQUIRED: whether −75 is additive with existing growth modifiers or a standalone25% multiplier, housing/amenity limits, zero/negative surplus and exact settlement behavior. No claim it always gives0.25×otherwise-final growth. Candidate A uses native growth−75 (may have different stacking); candidate B would need a reliably isolated surplus-stage multiplier if available. Neither is authorized silent fallback; totalFood−75, consumption changes, starvation/population removal are forbidden. USER_GAME_TEST_REQUIRED only at later prototype, not now.

### Production-only restructuring unit

Loaded Units schema exposes CanTrain, MustPurchase, PurchaseYield. Normal production-enabled/non-must-purchase with no purchase currency is a candidate for ordinary buy-path denial, not proof against all overrides. DynamicModifiers includes EFFECT_ENABLE_UNIT_FAITH_PURCHASE; `COMMEMORATION_INFRASTRUCTURE_GA_PURCHASE_CIVILIAN` and HD/class-specific grants show faith eligibility can come from modifiers. Unit promotion/class/tag selection and native CanStartCommand must be checked against these grants. No purchase-price hack or implicit allowlist immunity is confirmed. Production-only remains Design; universal purchase bypass prevention is TECHNICAL_INVESTIGATION_REQUIRED / future USER_GAME_TEST_REQUIRED.

### Other static candidates

- Single-city building production: native `MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION`, DistrictType/Amount precedent. Ordinary-only, unique districts/buildings, acquisition/removal and combined stacking are prototype gates.
- Project-as-action: native ProductionPanel project click ultimately dispatches production request; existing CrewProjectOrder only sorts entries. An interception hook is required before dispatch, not a presently implemented Commerce action UI.
- GreatWorksOverview has city rows and GreatWorkMoved; HD GreatWorksSupport alters tooltips. Existing D0031 investigation supports candidate hook, not compatible final layout. Cache invalidation for create/move/trade/ownership and missing-era universe still needs prototype.
- Current Properties/receipts demonstrate persistent state mechanisms, not an implemented atomic locked-outcome/restructuring contract. Save compatibility, partial write recovery and unique IDs require adaptation.

## Remaining register / classifications

| Category | Items | Freeze handling |
|---|---|---|
| BALANCE_REQUIRED | Commercialization coefficients/domain numeric values/cap/floor; principal/term/returns/probability hardcap/pity change; Development cost/term/bonus/cap; Team cost/disruption final values/speed; reputation thresholds/effects/cap | No invented values; initial5T and−75% remain user values, not final balance |
| DESIGN_DECISION_REQUIRED explicitly deferred by user | Source-value mapping/share usage; exact quote fundamentals; exact reputation affected mechanics; contract stacking; speed convention; post-liquidation Team loss | Not declared numerically solved; must close before dependent implementation |
| ARCHITECTURE_REQUIRED | State ownership, save/load, idempotent contracts, directional route predicates, capacity/source binding | Not Gameplay simplification |
| UI_PROTOTYPE_REQUIRED | Project interception, single-layer panels, hybrid era display and HD hooks | No current game test request |
| LEGACY_REVIEW_REQUIRED | Contracts/reputation/Teams after respecialization, historical commercialization, former institutions, conquest/ownership | No cross-profession automatic inheritance |

## External review not adopted

No cancellation of3F3P or Shared development; no national Dialogue era count, residency, cooldown or project lock; no national-unique Culture observations; no Gold/Science blueprint analysis; no single interpretation domain per Great Work. Industry core personally learns templates; advanced Wonder focus and filling old Wonder eras are intended, bounded by future balance. No Team expiry, maintenance, decay, era restriction, one-Team-per-turn or future-Wonder prohibition. Repeated high-level Culture fieldwork is accepted soft diminishing return, not a new hard cap.

## Verification scope

Documentation structural checks, reference/hash and narrow diff review only. No Gameplay source changes, Mod version bump, game launch, deployment, tag, main edit or Architecture sync/implementation. No LOCAL_SIMULATION_CONFIRMED or USER_GAME_TEST_PASS claimed for these new mechanics.

## D0031 closures — accepted user decisions, awaiting canonical revision integration

### Industry capacity

User confirms per eligible Engineering Mobilization Industry source city capacity=2; every completed tier1–5 Team occupies1slot, IV adds no slots. Bind each completed Team to training city until consumed/legally removed. ACTIVE loss preserves completed Teams; only current qualification allows production. Leaving Industry preserves Teams but stops replenishment; later consumption does not create generic capacity usable by new specialization. Capture/city ownership/Team ownership/original-owner disappearance remain DESIGN_DECISION_REQUIRED / TECHNICAL_REVIEW_REQUIRED. No production decay, maintenance, expiry, Wonder/production-era restrictions, one-Team-per-turn or future-Wonder ban. These accepted clauses supersede D0031's unresolved capacity choices when integrated; no runtime claim.

### Culture Hybrid D

Direction now USER_CONFIRMED PRESENTATION DIRECTION, not merely recommendation. Great Works city summary: 已覆盖N个时代｜缺：X、Y、Z, no required denominator. Cached tooltip: each supported era/count/missing status/domestic availability and preferably source cities, or explicit no domestic work. Culture_D0029 eligibility and historical era authority shared; unknown Mod works excluded. No auto movement/theming/optimization/AI purchase/Dialogue preparation. Open/data-change aggregation and confirmed create/move/trade/ownership invalidation, hover zero requests/no per-second scan. Layout/pixels/icons/wrapping/scaling/HD hook/placement/cache lifecycle remain PROTOTYPE_REQUIRED. Gameplay content unchanged.

## Completion gate

BLOCKING_DESIGN_DECISION: COM-BLOCK-01 and COM-BLOCK-02 only. Team loss explicitly marked/deferred by user. No Balance numbers requested now. Formal D0032 canonical update and DESIGN_FROZEN withheld until those answers; this does not reopen confirmed names, abilities, capacity or Hybrid D. No implementation or game test authorized. Current batch commits only candidate/review, preserving authority history; later accepted revision is a separate coherent documentation commit.
