# Military Freeze Candidate — synchronization and review

Document Owner: Codex
Design Authority: User
Date: 2026-09-20
State: FREEZE_CANDIDATE / NOT_READY_TO_FREEZE
Canonical baseline: D0032; new Design revision NOT_ALLOCATED
Scope: Design review only; no Architecture adaptation, implementation, deployment or v0.1 scope expansion.

## A. Authority and evidence

The complete [user decision record](Military_Freeze_Candidate_User_Record.md) is the normative source for this candidate. This review resolves historical references and classifies remaining questions; it does not override that record. Confirmed new decisions outrank old Military text. D0032 remains the published canonical revision until blocking answers are accepted and a new revision is explicitly integrated.

Read against [Authority](../Workflow/Authority.json), [W0001](../Workflow/README.md), [current Spec](Specialization_v0.1_Design_Spec.md), [ChangeLog](Design_ChangeLog.md), [Shared D0028](Content/Shared_D0028.json), [Content index](Content/README.md), A0161 and S0210 current headers. Runtime baseline B079.106/modinfo106, source implementation b420a967; P0-B1 user PASS, P0-B2 plan only. No Military runtime implementation is claimed.

Historical sources: [D0008](Revisions/Specialization_Design_Spec_D0008.md) MIL-001–013, particularly MIL-002/007 Insight and MIL-010–013 Mentorship; D0002 records Insight clarification, D0006 records Mentorship introduction. Current D0032 retains that old Military body, including MIL-013 explicit unresolved unit-system qualification. Old references remain historical evidence rather than additional new abilities. No universal current acquisition-path or unit-normalization contract was found that closes the candidate questions below.

## B–D. Candidate structure, names and Shared rules

| Level | Institution | Naming | Named ability | Confirmed role |
|---|---|---|---|---|
| I | 武备社 | PLACEHOLDER / NAMING_REVIEW_REQUIRED | None | Working Encampment specialists +3 Food/+3 Production |
| II | 武官所 | PLACEHOLDER / NAMING_REVIEW_REQUIRED | 行伍制度 — LOCKED | Shared housing +2 base General GPP/working specialist |
| III | 演武场 | LOCKED | 综合训练; 后勤编制 — LOCKED | Permanent birth training quality; maintenance logistics |
| IV | 讲武堂 | LOCKED | 战阵传授; 沙场领悟; 军略传承 — LOCKED | Mentor experience; veteran insight; local institutional memory |
| Network | Separate layer | 统一动员 — LOCKED | Not an institution ability slot | Matched active-unit production efficiency |

0/1/2/3 is the accepted arrangement, not a mandatory runtime schema. Institution entries follow approved presentation-only, cumulative Potential principles; ACTIVE controls abilities, not institution existence. No engine Buildings are authorized.

Base support stays3F3P at all levels. ACTIVE>=2 housing uses Shared eligible district +1 and each actually present eligible ordinary **Tier existence** +1; not weighted D and not per-building multiplicity. General GPP is base +2 per actual working military specialist and accepts ordinary GPP modifiers. No old +15% Combat XP or III5F5P survives in this candidate.

Philosophy: cities can develop broadly while retaining a military institutional focus. Social resources, organization, knowledge and talent become military capacity. Defense, preparation, expansion and emergency restructuring are valid. No peacetime economic yield is required to justify preparation costs.

## E. 综合训练

Read only Campus, Theater, Industrial Zone, Commercial Hub and Holy Site domains. Each needs at least one current eligible **Tier1** ordinary building, using Shared completion/pillage/ordinary ontology and appropriate unique replacement normalization. Bare district, Tier2 alone, D>0, or high D do not substitute for actual T1. Free but otherwise ordinary buildings count. Institutions/carriers do not. Each qualifying domain contributes permanent +1CS at eligible city training/creation, total0–5. Several T1 buildings in the same domain do not multiply the domain contribution.

Harbor/Government/Diplomatic/Preserve/Entertainment/Neighborhood/other domains are excluded. Three qualifying domains yield+3; five are not an activation threshold. The six-district/16-population example describes ordinary population-slot infrastructure assumptions, not a new hard16-population predicate overriding unique slot exemptions. Training quality competes with population, district slots and production that could instead build more troops.

## F. Provenance and formations

Already awarded birth CS survives subsequent building loss and city respecialization. Per-ability formation inheritance is maximum, e.g. max(4,5,1)=5. Different ability sources remain additive: training+4 and tradition birthCS+1 give+5. Elite cadre plus ordinary units is intended. No sum of repeated same-ability sources, averaging penalty or inferred extra restriction.

Acquisition eligibility remains MIL-BLOCK-01. Ability persistence through upgrades and native formation merge mechanics require technical verification; no implementation convenience may silently delete the intended provenance. A merged unit's city-dependent XP attribution is not settled by the CS maximum rule (MIL-BLOCK-02).

## G. 后勤编制

III unlocks a dedicated logistics support line. Preferred physical support unit escorts one combat unit1:1 and replaces covered ongoing strategic maintenance with additional Gold maintenance borne by the support. Training/purchase/upgrade upfront resources remain required. No free creation, virtual resource duplication or new source yield.

Successive versions cover their own and earlier supported maintenance-resource levels. Exact HD unit/resource/unlock table, production costs, Gold costs and speed treatment remain deferred. Uranium/endgame inclusion is explicitly DESIGN/BALANCE_REVIEW_REQUIRED, not silently included/excluded and not a body-freeze blocker under this request. Early10/laterhundreds-or1000 are loose discussion expectations, not configured values.

Support death matters; link/unlink, death, upgrade, embark, formation, resource settlement ordering, save/load, AI and overhead require a spike. Physical units are the preference; UI/UnitAbility contract is only a fallback to review after concrete technical evidence. No assumed fallback adoption or automatic gameplay-equivalence claim.

## H. 战阵传授 — historical formula accurately retained

D0008 MIL-010–012: qualified own land fighter, actual combat, adjacent one-hex own eligible land mentor with greatest actual promotion count; multiple mentors do not stack. New same-Promotion-Class restriction applies before choosing the mentor and overrides the old unrestricted class comparison.

`MentorshipXP = max(0, floor((P_mentor - P_fighter)/2))`.

It is independent bonus XP, not multiplied by normal combat XP modifiers, not capped by E, and has no added artificial hard cap. Actual promotions include lawful formation inheritance; XP level is not P. Fighter/mentor need not garrison or return home. Intermediate veterans can also learn from more promoted units: “新兵” does not silently become P=0-only. Normal mixed fronts should benefit; optimizing coverage is allowed. Attribution/eligibility and exact qualifying combat snapshot remain explicit questions rather than invented rules.

## I. 沙场领悟 and balance evidence

D0008 MIL-002/007 formula, now IV: `InsightXP = min(E, floor(P/2))`. E is current actual working Encampment specialists of the relevant city; no virtual Academy specialist. P is actual promotions, including lawful Corps/Army inheritance. Original E<=4 was the then-current slot environment, not a new universal +4 cap. Independent bonus XP does not rewrite the normal combat-XP system.

User reports the previous strict model established no faster high-level promotion, usually about one fewer combat, never two, sometimes zero. Record this as USER_REPORTED_HISTORICAL_BALANCE_CONCLUSION. The formula and selected tables are present in historical authority; this review has not reconstructed a complete combat-count proof. Do not replace it with an unsupported generic “positive feedback therefore snowball” claim. Unfixed Tradition XP additions are not automatically covered by the old proof.

**Current HD evidence changes an input:** installed HD `2465378070/UpdateDataBase/DL_GlobalParameters.sql:269` sets `EXPERIENCE_MAXIMUM_ONE_COMBAT=32`. The newer application-support `Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite` also returns32; the older outer `Cache/DebugGameplay.sqlite` returns8. Both inspected read-only. The latter's old8 must not be mistaken for the current HD environment. HD `DL_Policies.sql` links DRILL_EXPERIENCE and Amount50 (lines1288/1867/2504). This confirms relevant XP modifiers exist, not a complete loaded-combination balance proof.

Classification: STATIC_CONFIRMED database/source evidence; **BALANCE_REVALIDATION_REQUIRED** against the intended actual Mod set. No game run, no claim about final per-combat settlement, no new XP cap imposed. Preserve old8 as historical model input, not a new requirement to override HD32. Exact XP thresholds, combat types, existing modifiers and final Tradition parameters belong in later revalidation.

## J. 军略传承

IV adds a third Great General action, distinct from keeping aura and native retire. Consume the General permanently in the Military city, do not trigger native retire, persist knowledge as that city's local Military Tradition. No different-era General requirement. A weak retire General being attractive for legacy is intentional, especially at a tier boundary.

Finite discrete tiers, approximately6 is a target rather than fixed balance. Each tier enhances only one of birthCS, MentorshipXP or InsightXP; a six-tier arrangement would enhance each around twice. Thresholds/order/increments remain unset. No all-three-per-tier enhancement, national tradition or automatic Network boost. Historical military capital versus newly restructured city is intended. City-dependent unit benefit attribution is MIL-BLOCK-02, not solved by saying Tradition is local.

## K. 统一动员

Replace old free-unit progress pool with Command Source / active target / participants. Candidate command city has current Military qualification and currently produces an eligible military unit. Authority uses current effective level, IV>III>II>I, not permanent Potential alone. Only **Current Active Production Item** counts, never later queue contents.

No commander: first eligible candidate becomes commander. On relevant candidate production change, strictly higher authority takes over; equal authority does not. Current commander changing to another eligible unit retains command, updates target. Stop eligible production, lose qualification/city, respecialize or invalid target: one bounded reelection, highest current authority then earliest current continuous eligibility episode. Stable sequence may be persisted; no per-turn election.

Participants need not be Military. Connected eligible Industry/Commerce/Research/ordinary cities actively producing the matching normalized target receive Production efficiency only. They inherit no local trainingCS, Tradition, XP abilities or logistics access. Exact network election/recipient scope and normalization await MIL-BLOCK-03/04. Level-change precedence awaits MIL-BLOCK-05.

Target preference is specific normalized UnitType/UnitLine, not entire PromotionClass. Tank versus Artillery/aircraft/other production is a real coordination tradeoff. Bonus formula/size/scaling remains BALANCE_REQUIRED; Tradition does not automatically affect it.

Production changes update commander/target or the affected participant; topology changes update affected recipients; loss triggers bounded election. Events/API remain technical investigation, not implemented scheduling. No queue-spoofing concern, cooldown, completion deadline or cancellation penalty is introduced.

## L. Restructuring and supersession

Old civilian infrastructure qualifying immediately after becoming Military is intended. Commerce D0032 P→P−1, REALLOCATING>=5 complete turns, nonFood−75%, FoodSurplus−75% and old ability withdrawal remain unchanged. Prior civilian history does not automatically grant Military Tradition. Already trained permanent CS survives leaving Military. Command qualification immediately ends on leaving Military. Other Legacy decisions remain independent.

| Historical clause | Candidate disposition on future freeze |
|---|---|
| MIL-001 base3F3P, II housing/base General GPP | RETAINED with Shared ontology |
| MIL-001/005 +15% Combat XP | SUPERSEDED; no extra II effect |
| MIL-002 III5F5P | SUPERSEDED; support always3F3P |
| MIL-002/007 Insight | RE-ADOPT formula at IV; no oldIII duplicate |
| MIL-003/009 garrison+1XP | NOT_RETAINED in new three-ability IV; do not add a fourth ability |
| MIL-010–012 Mentorship | RE-ADOPT with same PromotionClass filter; unresolved MIL-013 is not silently solved |
| MIL-004 national L√N progress/threshold100/free unit | SUPERSEDED by active-production mobilization |
| NET-RC-004, OPEN-10 and old future-network summaries referencing MIL-004 | Update cross-references at actual canonical freeze, not now |
| HARB-005–009 / Aerodrome future references | No automatic new Military-to-Harbor/Air rewrite; FUTURE_CROSS_REFERENCE_REVIEW |

All historical snapshots remain intact. This candidate does not grant implementation permission or expand the four-profession P0 plan.

## M. Balance register

- 综合训练 +1/domain,max5 and Shared3F3P/+2baseGPP are user values, not missing balance.
- Tradition exact tier count/order/General thresholds, CS/XP increments and eventual combat-count revalidation.
- Logistics version production costs, Gold/T, economic pressure over eras and applicable speed scaling. Uranium/resource coverage deliberately deferred as design detail.
- Mobilization bonus fixed/level/participant/diminishing/speed choices remain explicitly unresolved balance parameters, no default.
- No unauthorized caps, cooldowns, resource generation or peacetime yields.

## N. Technical register — investigation only

STATIC_CONFIRMED means source/database evidence, not engine PASS. Unless explicitly stated below, items are TECHNICAL_INVESTIGATION_REQUIRED / future prototype and user test as necessary.

| Area | Evidence / smallest investigation boundary |
|---|---|
| T1 predicate | Existing Shared ordinary/Tier/pillage facts are a reusable direction. Must query eligible Tier1 existence, not D. Validate HD/unique catalog coverage; no universal vanilla support claim |
| Acquisition/provenance | Identify production, purchases, free grants/levy/duplication/capture separately once policy is chosen; permanent ability, upgrade and per-ability formation max need native proof |
| Unit normalization | No exported shared Military unit normalizer found in Mod. Read-only cached `UnitReplaces(CivUniqueUnitType,ReplacesUnitType)` provides replacement evidence; Units has PromotionClass/FormationClass. Tank and ModernArmor share heavy-cavalry class, which does not prove same target. Corps/Army normalization and inherited source require separate engine review |
| Logistics | Dedicated support line, escort link/unlink/create/destroy/death, upgrade, embark, formation, resource tick and Gold maintenance, save/AI/event overhead; fallback only after evidence |
| Mentorship/Insight | Combat event identity, eligibility, timing/positions/promotions, local one-hex selection, exactly-once independent XP; current HD inputs need balance revalidation |
| General legacy | Third action, consume without retire, local persistence/tier transitions, ownership and restructuring policies; no current implementation claim |
| Mobilization | Active production versus queue, effective-level events, stable eligibility sequence, participants/topology, selected-unit production modifier, native Corps/Army production and bounded reconciliation; no unnecessary polling |

Cached DB is one historical loaded catalog, not proof of every Mod combination. Source inspection cannot establish escort reliability, API event completeness or final resource settlement. No military gameplay simulation or USER_GAME_TEST_PASS claimed.

## O. Legacy register

Explicitly deferred: Tradition while outside Identity, conquest/owner change, historical institution presentation detail, logistics eligibility after source respecialization, permanent unit buffs on capture/owner changes, source loss and merged provenance for city-dependent effects. Basic IV attribution required for ordinary play is separated in BLOCK-02 below; extraordinary owner transitions may remain Legacy.

Confirmed: birth training CS survives building loss/respecialization; current command dies on respecialization; new Network does not retain old progress/free-unit effect. Never infer Research/Industry/Culture/Commerce inheritance policies for Military.

## P. Shared District Completeness review

Shared D0028 defines absolute weighted infrastructure depth `min(10,sum eligible tiers1/2/3/4)`; it does **not** normalize a locally complete T1–T3 district from6 to10, nor define an environment-specific denominator. Three-tier chain1+2+3=6; four-tier1+2+3+4=10; same-tier multiples/branches follow ordinary eligibility, actual existence and cap rules rather than universal chain assumptions. Highest single district is the current domain aggregation.

SHARED_DESIGN_REVIEW_REQUIRED: the player-facing “完善度” terminology versus unequal reachable maxima and HD/expansion Tier assignment warrants separate review. No conversion to percentage, rescaling, new cap or Shared revision here. Military training needs actualT1, so this does not block it. Unknown ordinary/Tier catalog objects require investigation, not silently assumed T1. Housing likewise remains Tier existence, not D.

## Q. Blocking gameplay decisions — five bounded groups

These are missing ordinary-play rules; numbers, APIs, naming, layout and explicitly deferred Legacy are excluded.

| ID | Required decision | Why existing authority does not answer |
|---|---|---|
| MIL-BLOCK-01 | Define eligible unit classes for 综合训练/统一动员 (only land combat, or naval/air too), and training acquisitions: production only or also Gold/Faith; treatment of free/levy/duplication/capture | “合格军事单位/新训练” is not a shared acquisition predicate; old land scope for XP cannot automatically authorize all new abilities |
| MIL-BLOCK-02 | Define which units belong to the Military IV XP system, their relevant city for current E/local Tradition, and ongoing eligibility when source ACTIVE falls; how merged different-source units choose that city. Confirm qualifying combat categories and pre/post-combat snapshot policy | D0008 MIL-013 explicitly left this open. Old formula supplies arithmetic, not recipient/source authority. BirthCS permanence does not imply permanent XP qualification or a mentor-city source |
| MIL-BLOCK-03 | Define target equivalence: same generation standard unit plus its unique replacements, versus full upgrade line; whether single/Corps/Army share target | UnitType, replacement and upgrade line differ mechanically. Same PromotionClass is expressly too broad |
| MIL-BLOCK-04 | Define commander election scope (player-wide versus each disconnected network), and whether participants must receive the elected command source or merely any valid Military source's network; source self-reception still follows chosen shared scope | Shared NET-001–003 preserves source/direct/center/distribution provenance, not a universal connected boolean; disconnected recipients otherwise ambiguous |
| MIL-BLOCK-05 | On ACTIVE change without production change, does a newly higher candidate immediately contest; does commanderIV→III while anotherIV exists cause reelection, or retain until production/qualification loss? | Higher takeover is tied to production events, while “Military资格下降” invalidates; a still-qualified lower level and a newly promoted rival need precedence |

No defaults selected. User may explicitly defer a boundary, but this review must not silently call it solved. Questions can be answered as grouped policies; no need for Balance numbers or technical APIs.

## R–W. Gate, files and stop

**NOT_READY_TO_FREEZE**, solely MIL-BLOCK-01–05. Lv1/II placeholders, finite-tier details, resource line/Uranium, Gold cost, production bonus, technical spikes and Legacy are non-blocking under the express deferrals. Closed Red Team disputes remain closed; complete list and full philosophy are preserved in the user record rather than selectively paraphrased away.

Changes: this review and verbatim candidate decision record only. Content navigation is hash-guarded by the active P0 workflow; it remains unchanged to avoid invalidating an unrelated implementation manifest. No D0033 allocation, accepted Spec/ChangeLog/Shared/profession content changes, Architecture/Status/Workflow modification or runtime edits. Git completion is reported in the task response to avoid self-referential commit hashes. Branch develop only; no main/tag/promotion/deploy.

Validation: Markdown local references, exact source-record payload/hash, protected baseline byte comparison, Workflow context integrity, diff whitespace/scope. These are documentation/static checks, not gameplay simulation. User game test: none. Stop after coherent docs commit/push and minimum decision questions; do not begin Architecture adaptation or implementation.
