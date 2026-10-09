# Diplomatic Specialization — Design Talk Handoff

Date: 2026-10-09
Status: **Non-authoritative discussion record**. Preserve decisions, candidates, alternatives and unknowns. Do not implement or promote candidates to formal Design without separate user authorization.

## Instructions for Main Task

Read the minimum relevant AGENTS, Workflow and current Diplomatic Design authority. Preserve this discussion in an appropriate non-authoritative proposal/handoff document. Identify conflicts with accepted authority rather than silently overwriting it. Follow existing document and Git rules; do not change code, tests, runtime or Investigation reports. Chinese remains the primary language for authoritative gameplay Design; this English handoff is a development aid.

Status labels: **Chosen direction** = explicitly selected in discussion, not necessarily synchronized to formal authority; **Candidate** = preferred but revisable; **Open** = undecided; **Technical unknown** = requires evidence/testing; **Deferred** = not currently selected.

## Identity and principles

Diplomacy represents **open, institutionalized foreign relations**: alliances, envoys, city-state control, diplomatic personnel and cooperation. Native Spies remain available but are not enhanced by this specialization. Diplomats are not Spy reskins. Prioritize strategic allocation over repeated micromanagement. Diplomat units are **granted free**, not built. Foreign missions aim for roughly **5 turns**, deterministic completion, and **one-time rewards**; no default capture, escape, detection, promotion or random success system. Avoid independent post-mission timed buffs.

Three Diplomat roles: (1) foreign mission for a one-time outcome; (2) city-state posting to maintain stable suzerainty; (3) Lv IV home-city posting for ongoing global cooperation and network yields.

## Current level structure

| Level | Ability | Status | Outline |
|---|---|---|---|
| I | Basic support | Candidate | Simple Government-like support; no formula agreed |
| II | Influence | Chosen direction | Extra Influence scaling possibly with Government Tier; values open |
| III-A | Diplomat institution | Chosen direction | Grant first Diplomat, basic foreign missions, permanent mission-domain unlock on first alliance of each type |
| III-B | Stable suzerainty | Candidate / technical unknown | 10 Envoys + stationed Diplomat; suppress competitors' envoys above 9 |
| IV-A | City-state protection | Candidate / technical unknown | Rule-level ban on other majors voluntarily declaring war on protected city-states |
| IV-B | Diplomatic corps expansion | Candidate | Alliance-network milestones grant additional Diplomats |
| IV-C | Global cooperation | Candidate placeholder | Indefinite home-city Diplomat posting boosts corresponding specialization network yields |

Names and exact coefficients remain open.

## Lv I and II

Lv I should remain simple, low cognitive burden, similar in spirit to Government baseline support. No settled yields or formula.

Lv II provides **Influence**. Government Tier is a promising scaling input. Influence naturally supports the city-state 1/3/6/10 Envoy progression. Passive **Diplomatic Favor** was disfavored: HD delays World Congress, Favor is often stockpiled/sold and may simply become Gold. Favor is not banned from future mission costs or rewards. Stockpile-based passive buffs were also disfavored due to balance and hoarding incentives.

## Lv III-A — Diplomat system

- **Direct grant:** Receive first Diplomat upon unlocking Lv III, without production cost. This avoids Spy-style delayed payoff.
- **Alliance learning:** First establishing a Research, Cultural, Economic, Military or Religious Alliance permanently unlocks the corresponding foreign mission domain. Once unlocked, the task can target **any eligible foreign civilization**, not only the alliance partner; later alliance expiration does not revoke knowledge.
- **Foreign missions:** Approximately 5 turns; deterministic completion when valid; one-time reward at completion. Avoid post-mission N-turn buffs, Spy success probability and personal XP/promotion systems. Target changes, interruptions, deployment/travel and eligibility remain open.
- **Technical:** Reuse general UI/mission concepts where feasible, not native Spy identity or espionage operations by assumption. The Culture Humanities Expedition may eventually provide a technical precedent.

### Research foreign mission: Cooperative Research — most developed

Chosen design direction: At completion, grant **one Eureka**. Let A = player's completed technologies, B = target civilization's completed technologies; take **K = A union B**. Starting from K, traverse the directed technology prerequisite graph outward **one edge layer at a time**. At the **nearest layer containing eligible targets**, uniformly randomly select one Eureka. If the layer has none, continue outward without a fixed depth cap.

Eligibility: player has not completed the candidate, has not received its Eureka, and it supports a relevant Eureka. **Do not require all prerequisite technologies to be completed.** Do not require the target civilization to lack that technology. No player choice, no priority for currently researched tech, no compensation if the target is far ahead. The user accepts that a far-future Eureka may be temporarily less useful; another mission or home-city cooperation may be preferable.

Open: exact graph-layer handling, HD-altered prerequisites, per-tech foreign completion reads, specific Eureka grant, no-candidate behavior, snapshot timing and mission lifecycle. Do not invent a fallback reward.

### Cultural foreign mission candidates

**Cultural Exchange:** one **Inspiration**, likely mirroring the union of both civilizations' completed Civics and outward layer search. This is a **candidate**, not fully frozen to Research's detailed algorithm; Civic-specific eligibility remains open.

**Great Work Promotion:** one-time Tourism burst against the target, broadly analogous to a Rock Band performance. Directly serves Cultural Victory and may be less useful elsewhere. Candidate only; do not automatically merge with Cultural Exchange or add a special Alliance III rider.

### Other foreign mission domains

Economic, Military and Religious missions remain **undesigned**. Do not invent their effects. A small set of generic/basic Lv III foreign tasks may exist; exact list is open.

## Lv III-B — Stable suzerainty

Candidate: A city-state with **at least 10 player Envoys** and **one stationed Diplomat** gains stable suzerainty. The 1/3/6 native Envoy thresholds extend elegantly to 10 as a strategic commitment. A stationed Diplomat creates a personnel opportunity cost.

No confirmed permanent native lock. Current technical fallback: periodically remove **other civilizations' Envoys above 9** at the protected city-state, allowing normal participation through 9 but limiting competition for control. This is not proven to prevent transient flips or all edge cases. Open: exact activation, preexisting suzerainty, loss below 10, tie handling, multiple AI, timing, read/load, conquest, posting removal and UI transparency. A Spy-style one-time expulsion is not equivalent: AI may redeploy stockpiled Envoys.

## Lv IV-A — City-state protection

Candidate: Other major civilizations cannot **voluntarily declare war** on a city-state currently under stable protection. Requires a **target-specific rule-level prohibition**, not merely higher AI opinion. Relevant native action-ban families exist but targeted major-to-city-state protection is **unverified**. Existing wars, indirect war entry, emergencies and state changes remain open.

## Lv IV-B — Diplomatic corps expansion

Preferred candidate: grant additional Diplomats when the **historical maximum of simultaneous active Alliances** reaches a new milestone. Conceptual cumulative grants = `1 + historical maximum simultaneous alliances`. The base 1 comes from Lv III; Lv IV enables expansion. Grants are free, not producible. Historical maximum prevents renewals/breakups from farming repeated grants and avoids deleting personnel when alliances expire.

Open: whether pre-Lv-IV alliance history counts; national vs source-city accounting; multiple diplomatic cities; loss/replacement; save/load; ownership; exact grant timing. Map-size dependence was judged acceptable in principle: more civilizations also mean more diplomatic responsibilities. The earlier current-alliance soft-cap model was displaced by historical grant milestones.

## Lv IV-C — Global Cooperation (placeholder)

At Lv IV, a Diplomat may **remain posted in a Diplomatic specialization city indefinitely** to coordinate one field of global cooperation. While posted, grant a continuous **percentage yield modifier to the relevant specialization network**, not nationwide by default. Same-domain postings **do not stack**. No five-turn restart, and no separate lingering timer. This is intentionally a late-game, lower-micromanagement use for expanding personnel.

Provisional **additive** formula: `Bonus_X = Base_X + CityState_X + Alliance_X + Specialization_X`. Candidate inputs: relevant city-states where the player has **at least 6 Envoys** (currently attractive versus counting only suzerains); current relevant alliance level; corresponding domestic specialization/network development. Ordinary target around **5–8%**, with **~10%** discussed as a possible high-end test target, **not an accepted cap or coefficient**. Domain mappings and network eligibility remain open.

The user considered even a nationwide 10% yield effect potentially defensible relative to three extra Settlers, but explicitly chose **network scope** for design consistency. The simplistic three-settler / thirty-city comparison is only a balance intuition, not a proof.

If a better Lv IV-C emerges, **Global Cooperation may merge with Lv IV-B** under institutional corps development. Do not merge preemptively.

## Alliance levels and rejected complexity

Loaded HD investigation showed advanced alliances are **not mainly trade-route bonuses**: they already reward Eureka/research, culture/tourism/GPP, city-state influence and suzerain benefits, military production/vision/promotions, and religion/faith. Do not recreate those effects without a reason.

A scheme of **three tasks per each of five Alliance types** (15 tasks) was rejected as a choice/maintenance burden. Giving each Alliance III a unique foreign-task extra effect was deferred. Percentage strengthening does not naturally fit discrete rewards such as **one Eureka / one Inspiration**. Alliance level can still contribute to Global Cooperation's continuous modifier.

Domestic districts unlocking task domains were also set aside in favor of **historical Alliance type** unlocks. Diplomat capacity from completing different task categories was disfavored because it forces unwanted missions. Diplomat personal experience, timed Gain Sources-like preparation, random success probabilities, Spy capture and post-mission 10–20-turn agreements were all disfavored or rejected for complexity. A 90% success cap was explored but then abandoned in favor of deterministic missions.

## Technical evidence and boundaries

Relevant non-authoritative Investigation reports: Diplomacy surface overview; city-state control/protection and Diplomat-vs-Spy semantics; `Spy_Mission_Probability_and_Diplomat_Reuse.md` (Stable); current HD Alliance effects inquiry. Their conclusions must be read from the actual files, not inferred from this handoff.

The Spy probability report confirms the UI queries `UnitManager.GetResultProbability` but **does not** establish the hidden formula or universal 90% cap; safe native non-Spy reuse remains unknown. Other technical unknowns include foreign tech/civic completion enumeration, tree traversal, granting Eureka/Inspiration, custom missions, stable suzerainty maintenance, targeted war veto, personnel grants and save/load/notification handling. Static definitions are not native test PASS.

## Remaining design agenda

1. Decide Cultural Exchange vs Great Work Promotion and Civic Inspiration selection.
2. Develop compact Economic, Military and Religious foreign missions.
3. Define generic Lv III foreign missions, if any.
4. Set Lv I support and Lv II Influence formula.
5. Set Global Cooperation domain mappings, 6-Envoy vs suzerain criterion, additive coefficients, network range and stacking.
6. Resolve diplomatic corps grant/lifecycle details.
7. Validate city-state control and war protection before implementation.
8. Decide later whether Lv IV-C stays independent or merges with IV-B.

## Main Task deliverable

Preserve this as a non-authoritative discussion handoff in the appropriate existing repository location, after minimal authority/workflow inspection. Report exact path, conflicts with accepted Design, checks and any authorized documentation commit/push. **Do not implement, test, deploy, change formal Design Authority, or silently decide open questions.** Stop and wait for the user's next authorization.

---

## Repository comparison — 2026-10-09

### Record scope and provenance

The user authorized saving this proposal, comparing it with accepted Design, and committing/pushing this document only. This is **not authorization to synchronize formal Design or implement any of the proposed mechanisms**. The source handoff above is preserved byte-for-byte; its instructions describe this recording task, not standing authority for future changes.

- Source: supplied `Diplomacy_Design_Talk_Handoff.md`, dated 2026-10-09; 13,112 bytes.
- Source SHA256: `0eeeb7567cb178e3a4796aa9d55dd5ee3c753c826ceda6a552480a320e911653` (source portion only, excluding this comparison).
- Comparison baseline: develop commit `e27897d3c1fb7ab04f01079c9ca989a1d306e190`; Design D0049 as indexed by [Authority](../../Workflow/Authority.json).
- Formal sources: current Spec [DIP](../../Design/Specialization_v0.1_Design_Spec.md#diplomatic-quarter--dip) and [DIP-MISSION](../../Design/Specialization_v0.1_Design_Spec.md#alliance-diplomatic-missions--dip-mission), plus OPEN-12 / OPEN-13. The [Design ChangeLog](../../Design/Design_ChangeLog.md), Accepted D0008, records mission acceptance with each clause's maturity preserved.
- Existing reading pages: [Diplomatic](../../Design/Diplomatic.md) and [Diplomatic Missions](../../Design/DiplomaticMissions.md). They continue to present accepted sources; this proposal does not supersede them.

“Chosen direction” is a discussion selection. “Candidate,” “Open,” “Technical unknown” and “Deferred” retain their distinct meanings. Being saved in Git does not promote any of these to accepted Design. All conflicts below remain unresolved for a separately authorized Design revision.

### Differences requiring an explicit future Design decision

| Topic | Current accepted source | Supplied discussion | Comparison and unresolved boundary |
|---|---|---|---|
| Specialization identity, Spies and visibility | DIP-001 retains City-State/protectorate, Spy/visibility and Alliance/Missions lines. DIP-004 gives level-based visibility; DIP-005 gives Spy capacity and survival/experience benefits. | Diplomacy is open institutional relations; native Spies receive no specialization enhancement. | Direct conflict with DIP-005 and the Spy portion of DIP-001. Visibility is omitted rather than explicitly replaced; do not silently remove DIP-004. |
| Early levels and Envoy benefits | DIP-002 / 004 / 005 already give level-I benefits; DIP-003 doubles the 1/3/6-Envoy benefit tiers at II/III/IV. | I basic support is a candidate without a formula; II Influence is a chosen direction with scaling and values open. | This proposes a different progression. Whether the current Envoy-benefit boosts are replaced or retained remains undecided; neither a new support formula nor an automatic combination is authorized. |
| City-state control | DIP-002 defines permanent protectorate slots at 1/2/3/4 and suzerainty that cannot be replaced. Scope and loss/ACTIVE boundaries remain explicitly unresolved. | III-B proposes at least 10 Envoys plus a posted Diplomat; a corrective cap on competitors at 9 is a technical fallback candidate. | Permanent slots and conditional posting are different contracts. Periodic correction has not been shown equivalent to preventing replacement; it cannot silently satisfy or weaken the existing guarantee. |
| City-state war protection | DIP-002 prohibits declarations by major civilizations at peace with the player. Allowing war and then pulling the player into it is explicitly rejected. | IV-A proposes a target-specific prohibition on voluntary declarations by other majors; existing wars and indirect entry remain open. | Both the level and protected relationship scope differ. The proposed prohibition is technically unverified; the existing rejection of the war-entry fallback remains part of current authority. |
| Diplomat identity, unlocks and targets | DIP-MISSION-001 uses Spy for non-allies and Diplomat for allies, preferentially reusing the native unit and district-targeted interaction framework; exact unlocks remain TBD in 003. | Free non-Spy Diplomats; first alliance of each type permanently unlocks a mission domain that can then target any eligible foreign civilization. | This changes the platform and target contract and adds persistent unlocks/personnel grants. General UI reuse does not imply native Spy operations are reusable or accepted for this proposal. |
| Mission progression and timing | DIP-MISSION-003 retains Spy XP, Era Score and promotion value; 004 retains Gain Sources. Mission periods remain TBD. | Valid missions complete deterministically in roughly five turns, with one-time rewards and no default personal XP/promotion, preparation or capture system. | The XP/promotion/preparation direction conflicts. Roughly five turns is not a frozen duration. Era Score is not explicitly settled by the handoff; omission is not a repeal. Interruptions, travel and target eligibility remain open. |
| Research and Cultural rewards | DIP-MISSION-006 explicitly replaced guaranteed Eureka with a probabilistic secondary reward; 007 likewise allows successful Cultural Exchange without Inspiration. | Cooperative Research chooses one guaranteed Eureka using the completed-tech union and nearest eligible graph layer; Cultural Exchange is a one-Inspiration candidate, not yet bound to that algorithm. | Guaranteed Research reward and the selection algorithm are substantive changes, not clarification of 006. Cultural selection remains a candidate. No-candidate handling, graph details and snapshot timing must not be invented. |
| Existing mission catalogue and timed benefits | DIP-MISSION-005–014 record distinct mechanisms and maturities, including Import Fair supply, Migration Agreement, Maritime Trade Agreement, military and religious directions, and future/candidate tasks. | Economic/Military/Religious missions remain undesigned in the new discussion; post-mission timed buffs are disfavored; a compact catalogue is preferred. | “Undesigned” refers to this proposal, not absence of existing authority. The old catalogue contains both accepted directions and candidates. A future revision must explicitly retain, replace, defer or retire relevant entries; do not erase them or promote all of them to fully frozen mechanisms. |

### Additions and maturity that must remain separate

- **Corps expansion:** historical simultaneous-alliance milestones and the conceptual `1 + historical maximum` grant count are candidates. They do not yet define national/source-city ownership, pre-IV history, multiple sources, replacement, loss, loading or grant timing. The meaning of a level unlock versus current ACTIVE eligibility is not settled by this handoff.
- **Global Cooperation:** network-scoped, same-domain non-stacking home posting is the proposed direction; mappings, eligibility and coefficients remain open. The additive formula, six-Envoy input and 5–8% / approximately 10% figures retain their stated candidate or balance-discussion status. This does not replace existing Shared/Network contracts automatically.
- **Foreign missions:** deterministic completion does not resolve interrupted, invalid-target or no-candidate outcomes. Research has a more developed discussion rule than Cultural Exchange; the Research algorithm must not be copied into Civics as accepted authority.
- **Continuity:** the proposal and its remaining design agenda are future discussion material. No v0.1 scope, Culture implementation, current task authorization or test status changes follow from this record. B173 user testing remains on hold under the user's existing instruction.

### Evidence boundary and next handoff

The comparison above is a document-level review of current accepted clauses and the supplied proposal. It is not a feasibility investigation or native validation. Technical assertions in the preserved source—about HD alliance effects, native action-ban families and Spy probability APIs—are attributed to the supplied discussion and were **not independently reverified in this pass**. Referenced Investigation reports remain non-authoritative and were not edited or included in this commit. No LOCAL_SIMULATION_PASS or USER_GAME_TEST_PASS is claimed.

A later user-approved Design revision must explicitly resolve the differences above while preserving candidates and genuine TBDs. Formal sources and their Chinese reading pages would then be synchronized together under the existing workflow. Until that authorization, this file is a discussion reference only; it is not a new authority index, implementation manifest or mandatory context entry.
