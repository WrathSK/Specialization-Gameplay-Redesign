# Future Specialization Feasibility: Implementation Difficulty and Performance Cost

Advisory / Non-authoritative / No design decision implied
Status: Stable
Maintainer: Advisor session (Claude), attribution only — not session authorization

**Scope.** This report covers the seven future four-level specializations outside v0.1: Military, Harbor, Government, Landscape/Preserve, Religion/Holy Site, Diplomatic Quarter and Community/Neighborhood. It assesses implementation difficulty and performance cost only. It does not judge design quality, balance or numbers. Auxiliary districts (Entertainment, Aqueduct, Dam, Canal, Aerodrome, Spaceport) are excluded at the user's request. The Alliance Diplomatic Missions framework is assessed only where a profession depends on it. Compatibility is assessed only for the user's HD environment.

**Basis.**
- `develop` at `bae883a`, clean worktree. Static reading only: no tests, no game launch, no file changes outside this report.
- External sources, all read-only:
  - Civ VI install `<CivVI>` (`Civ6.app/Contents/Assets`).
  - HD Workshop `2465378070` `<HD>`, version UNKNOWN.
  - District Expansion HD Workshop `2701747165` SQL (Community only).
  - Government only: the local composed `DebugGameplay.sqlite` game cache, opened read-only and immutable (see process notes).
- Builds on the earlier audit in this directory's sibling topic, [Architecture_Engineering_Audit](../Architecture_Engineering_Audit/Final_Review.md). AF-xx and SD-xx IDs refer to that audit.

**Evidence labels.**
- **FACT**: read in source or data.
- **INFERENCE**: reasoned, with stated confidence.
- **UNKNOWN**: needs native evidence.
- No LOCAL_SIMULATION or USER_GAME_TEST evidence is claimed. Native experiments ("spikes") are proposals only.

**Method.** Seven independent read-only assessments ran, one per profession. Each read the Design page and content, the current architecture and audit findings, the relevant Mod modules, and the base, DLC and HD data and Lua that decide whether a needed native effect or API exists, and in which context. This report consolidates their results. Each profession's full table is summarized here; the subagents' raw tables are not kept in the repository.

---

## 1. Overview

| Profession | Design maturity | Overall difficulty | Performance risk | Hardest parts | Native blockers that may force a DDR |
|---|---|---|---|---|---|
| Religion / Holy Site | Accepted direction; names and many boundaries open | **L–XL** (core S) | **LOW** with native routes; HIGH if Lua reacts to world religion events | Lv4 belief absorption (XL); Lv3 "reduce foreign pressure in other cities" (L–XL) | No proportional incoming-pressure modifier; belief changes are irreversible and class-capped |
| Government | Accepted baseline D0047; several working names/values open | **XL** (core S–M) | **LOW–MEDIUM**, amplified through policy events (AF-06) | Institution study (XL); policy-cost discount + first-change-free (L); Legacy selection (L) | No policy-cost modifier; native "free change" also frees government changes |
| Military | Core frozen (D0037) | **XL** (city side S–M) | **MEDIUM** (HIGH on current shared plumbing) | Field logistics (XL); Unified Mobilization (XL); unit training-snapshot infrastructure (L–XL) | No per-unit dynamic Gold maintenance; trained-unit grant semantics unproven |
| Harbor | Accepted D0037; mirrors Military | **XL** (two full lines) | **MEDIUM** | Sea logistics (XL); Export + Markets delivery (L–XL); naval mentorship on the snapshot foundation | No per-route or per-origin route-yield scaling; maritime-route classification is UI-only |
| Diplomatic Quarter | Accepted direction; **no named institutions or abilities** | **XL**, bimodal (data lines S, protectorate XL) | **LOW–MEDIUM** | Irreplaceable suzerainty; war ban on protectorates; spies "never die" | No suzerain lock; third-party-peace condition may be inexpressible; no death→capture conversion |
| Community / Neighborhood | Strong freeze candidate (not frozen) | **L–XL** | **MEDIUM**, conditionally HIGH | Domestic population redistribution (XL); international immigration (L); 职住融合 (L) | No population-transfer API; HD Hospital hook refunds or extra-grants population (breaks conservation) |
| Landscape / Preserve | Strong freeze candidate (only LAND-001…006 accepted) | **XL** | **MEDIUM** if bounded; HIGH on current plumbing | Ecological maintenance + team unit (XL); habitat propagation (L–XL); Appeal changes (L + likely DDR) | No "unworkable tile, yields unchanged" route; no per-plot or per-improvement Appeal effect |

**Calibration.** Culture Expedition N1 (one profession unit plus UI) took about 3.3k Lua lines, 29 test files and builds B178–B204 (AF-15). Military Logistics, Harbor Logistics, the Landscape team, and the Diplomat in the mission framework are each in that class or larger.

**Main conclusion.** Most "simple" abilities can be built with patterns this project already proved:
- hidden carrier plus SQL modifiers
- `Building_CitizenYieldChanges`
- Lv2 housing/GPP bits
- `EffectiveFacts` ACTIVE

The expensive parts cluster around four new capabilities that several professions need. Building each once, as a narrow shared primitive, is the main lever for keeping the post-v0.1 cost manageable (§3).

---

## 2. Cross-cutting prerequisites (before any fifth profession)

These are the earlier audit's FIX_BEFORE_DEPENDENT_FEATURE items, triggered by "a fifth kind" or by the profession's own write patterns.

1. **AF-28 kind descriptor.**
   - The four kinds are hard-coded in about 17–27 Lua files plus SQL and the Store's persisted-record checks (`Mod/Probe.lua:5-6`, `Mod/EffectiveFacts.lua:5`, `Mod/CityProgressionStore.lua:25,1012-1024`, `Mod/NetworkInput.lua:45-46`, `Mod/Lv2GPP.lua:8-10`, …).
   - If one list is missed, the fifth kind's city raises `NETWORK_IDENTITY_UNAVAILABLE`, and through AF-14 the whole player's network is withdrawn.
   - Do this once, before the first fifth kind.
   - Each profession also needs a decision on activation in existing saves. For example, Holy Site and Encampment completions were never recorded, because `family()` returns nil for them. That is a DDR.
2. **AF-06(b) keyed revisions + event normalization (AF-06a).**
   - Every profession adds writers. With today's global `SPC_RuntimeUIRevision`, each write triggers a world Commerce audit (`Mod/Probe.lua:552-554` → `Mod/CommerceConvergence.lua:157-166`).
   - Unit, combat, plot, religion and policy events must not go through `RuntimeWork.Hook`'s full-scope fallback (`Mod/RuntimeWork.lua:80`).
   - Several professions' events have owner-first signatures evidenced in base or HD code:
     - `OnCombatOccurred`
     - `GovernmentPolicyChanged`
     - `GovernmentChanged`
     - `CityProductionChanged`
     - plot events as `(x,y)`
3. **AF-07 carrier count.**
   - Every new `BUILDING_SPC_*` row is checked by D capture and the Great Work collector in every city. Rough additions per profession:

     | Profession | New carrier rows (rough) |
     |---|---|
     | Military | ~30–40 (up to +150 with per-line Mobilization) |
     | Harbor | ~100–160 |
     | Government | ~40–60 |
     | Religion | ~15–20 (Lv4 per-belief carriers could add hundreds) |
     | Landscape | small, if bit-encoded |
     | Community | up to ~500 if per-instance citizen carriers are used |

   - Keep rows few: put many modifiers on few carriers. Consider HD's plot-property "binary compress" carriers where plot-scoped (`<HD>/Gameplay/BinaryCompress.lua`), noting the old-save caveat B029. Alternatively, ship AF-07's domain-scoped presence check first.
4. **AF-01 Store extension registration.**
   - New persisted assets need it: Military Tradition, Harbor operating, import locks and tradition, Government study ledger and Legacy configuration, Community immigration ledger and policy toggles, Religion absorption entitlement, Landscape tasks and mother/child records.
   - Landscape's permanent **plot-bound** gains do not fit the per-city Store at all (§4.7).
5. **AF-12 typed holds and per-turn self-healing reconciliation** (discussed with the user on 2026-10-13; still a user decision). Every profession with a transaction would otherwise copy today's terminal-HELD pattern:
   - Government projects
   - Military and Harbor Great General/Admiral consume
   - Landscape tasks
   - Diplomat missions
   - Community settlements
6. **AF-03 UI native-read bridge.** Many needed reads are evidenced only in the UI context:
   - trade-route path and incoming routes
   - religious pressure
   - amenities
   - `plot:GetAppeal`
   - national parks
   - civilization metrics
   - spy mission records
   - current government (UNKNOWN)

   A single bridge with readiness and READER_ABSENT semantics avoids growing more Gameplay→UI closures.
7. **Expedition exit-side fixes (clusters A/B/E)** before reusing the Expedition training gate or task framework (Landscape team, Diplomat).

---

## 3. Shared building blocks (build once, reuse)

| Building block | Used by | Native basis (FACT unless noted) | Key spike |
|---|---|---|---|
| **Unit training snapshot** (attribute a unit to its training city; freeze per-ability buffs at birth; keep the maximum on formation; survive upgrade) | Military (quality CS, Insight E, Tradition), Harbor naval line, Religion theological strength | `MODIFIER_SINGLE_CITY_GRANT_ABILITY_FOR_TRAINED_UNITS` = `COLLECTION_CITY_TRAINED_UNITS` + `EFFECT_GRANT_ABILITY` (`<CivVI>/Base/Assets/Gameplay/Data/Modifiers.xml:2209-2213`). Used by Barracks, Royal Navy Dockyard, the HD trained-strength abilities and HD Mosque. Gameplay `ChangeAbilityCount` and unit `SetProperty` appear in shipped scripts | Whether Gold/Faith purchases count, whether free or levied units are excluded, retroactivity, persistence after the carrier is removed, upgrade and formation behaviour, save/load. Build it **domain-parametric** (land/sea/religious) |
| **Combat hook** (bonus XP on real combat) | Military Mentorship/Insight, Harbor naval equivalents | `GameEvents.OnCombatOccurred(attP, attU, defP, defU, …)` in Gameplay (HD `Boosts.lua:616`; base scenario scripts); `ChangeExperience` (HD `HD_Common.lua:105-110`) | Event timing relative to XP and melee advance; HD XP cap 32 per combat; `GetPromotions` in Gameplay; owner filter first |
| **N-turn full-production project primitive** (generalizes the Claim/Dialogue 1T transaction) | Government study (2T/3T) and Legacy (1T), Industry study (v0.1), possibly Community policy | Existing 1T: unfinishable project + end-of-turn marker + persisted CALLING + `FinishProgress` (`Mod/DialogueProjects.lua:45-56,163-186`) | Interruption and partial-progress semantics (DDR); game-speed rounding |
| **Profession unit + task framework** (training admission, source binding, capacity, multi-turn task, interruption, protection) | Landscape team, Diplomat (missions), Military/Harbor logistics units (link variant) | Hidden ACCESS building + `Unit_BuildingPrereqs` (`Mod/Data/ExpeditionSpyGate.sql:18-22`); Expedition task phases | Unit protection fields (AF-15, not yet investigated across professions); purchase bypass of NULL `PurchaseYield` (TS04) |
| **Plot-property (PF) gated plot yields** | Landscape (maintenance gains, buffer, Lv1), Community (per-instance fallback), Harbor (Port Link alternative) | `REQUIREMENT_PLOT_PROPERTY_MATCHES` with `EFFECT_ADJUST_PLOT_YIELD` / district-yield modifiers. The CultureAesthetic precedent has native settlement PASS (B149) | Plot properties as **permanent** authority (so far only disposable configuration in this project); behaviour across city/owner transfer; engine re-evaluation cost |
| **Route facts service** (maritime flag, incoming routes, per-route yields) | Harbor commercial line, Religion network (route b), Military Mobilization topology | UI `GetTradeRoutePath`, `city:GetTrade():GetIncomingRoutes()` (HD UI); existing BackgroundRoutes → NetworkSender → NetworkBridge | The sender caps routes at 128 or 16 KB and returns silently when over the cap (P13a-Q04); the Bridge asserts outgoing-only (`Mod/NetworkBridge.lua:227`) |

---

## 4. Per-profession assessment

Difficulty scale:
- **S** = a reused pattern plus SQL, about one batch.
- **M** = a new carrier family or one spike.
- **L** = a new subsystem or several unknowns.
- **XL** = no proven native carrier for the written rule, or a DDR first.

Performance classes:
- **P0** = static native modifier, about 0 Lua.
- **P1** = bounded own-city or event-O(1) work.
- **P2** = frequent own events or cross-city writes amplified by existing consumers.
- **P3** = world-scope or unbounded. Avoid.

### 4.1 Religion / Holy Site — L–XL, LOW risk with native routes

No institution or ability names exist yet. Rows use REL IDs.

| Ability | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind | AF-28 descriptor; Religion excluded from Lv2 GPP (no Prophet value) | L | P1 |
| Lv1 support +3F/+3P per working specialist | Hidden `Building_CitizenYieldChanges` carrier (SpecialistSupport/ResearchSupport pattern; TS19 primitive) | S | P1 |
| Lv2 housing | Reviewed Holy Site tier rows. The catalog already maps about 27 Holy Site buildings; HD moves some tiers | S | P1 |
| Lv2 theological strength | Bit carriers → `GRANT_ABILITY_FOR_TRAINED_UNITS`, an ability restricted to `CLASS_RELIGIOUS_ALL` using `MODIFIER_UNIT_ADJUST_COMBAT_STRENGTH`. HD Mosque and Debater are precedents | M | P1 / P0 |
| Lv3 support upgrade +5/+5 | Carrier swap or top-up | S | P1 |
| Lv3 self-stability | Soft route: `MODIFIER_SINGLE_CITY_RELIGION_IGNORE_PRESSURE` (Moksha "Citadel of God"; HD Monastic Isolation). Hard route: `SetAllCityToReligion` on owner-filtered events | S / M | P0 / P1 |
| Lv3 reduce foreign pressure on other own cities (proportional) | No incoming-proportional modifier found. Lua `AddReligiousPressure` bursts cannot be read back or applied idempotently across reloads | L–XL | P2 + P3 reads |
| Lv4 absorb a defeated religion's beliefs | Native `AddBelief` (capped at one belief per class per religion), HD-Potala-style cloned modifiers via `AttachModifierByID` (no detach found), or removable carriers. Plus holy-city detection, Store entitlement and a chooser UI | XL | P3 detection, O(religions) per turn |
| Network: trade-route pressure | Native player-wide `MODIFIER_PLAYER_ADJUST_TRADE_ROUTE_RELIGIOUS_PRESSURE` (cannot scale per route), or Lua bursts | M / L | P0 / P2 |

**Performance rule.** Never hook `CityReligionFollowersChanged` / `CityReligionChanged` through generic hooks. These are world-scope, frequent visualization events. If one is ever used, coalesce it to a dirty set drained at the enabled player's turn.

**DDR candidates**
- Birth-locked vs live theological strength.
- Soft vs hard lock, and what happens if the city already follows a foreign religion.
- Lv3 foreign-pressure semantics, if the spikes fail.
- Lv4 apply route, allowed belief classes, permanence.
- Network scope (domestic only vs all routes).
- Activation of the fifth kind in existing saves.
- What applies when the owner never founded a religion.
- Names.

**Spikes**
- S1: trained-unit ability with faith purchases.
- S2: ignore-pressure placed on a hidden building.
- S3: Gameplay reads of pressure and holy city.
- S4: burst semantics.
- S5–S6: `AddBelief` and the clone/attach route.
- S7: trade-route pressure modifier.
- S8: holy-city tracking.

### 4.2 Government — XL overall, core S–M, LOW–MEDIUM risk

| Ability | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind | AF-28. Native facts: `DISTRICT_GOVERNMENT` has `MaxPerPlayer=1` and `CaptureRemovesDistrict=1`, so the plaza is destroyed when the city is captured | L (M after AF-28) | P1 |
| L1 basic support (+G Food/Production per Government building) | Pure SQL. `MODIFIER_PLAYER_CITIES_ADJUST_BUILDING_YIELD_CHANGE` attached via `GovernmentModifiers` per government tier, with a city requirement "has gate carrier". The HD Autocracy Legacy uses the same modifier type. Lua only toggles the gate | S–M | P0 + P1 |
| L2 policy-cost discount | **No native cost modifier**: the cost comes from global `POLICY_COST_*` parameters, and one `UNLOCK_POLICIES` operation unlocks both policy and government changes. Routes: refund after payment, pre-fund via a GovernmentScreen replacement, or `SetCivicCompletedThisTurn(true)` (side effects) | L | P1, amplifies AF-06 |
| L3 institution study (gain another building's continuous effects; 1/2/3T) | N-turn project primitive + per-building cleaned modifier catalog. FACT: 9 buildings, 106 modifier rows, including one-shot unit grants, a self-referencing requirement, Great Work slots that are not modifiers, and an engine-coded Governor Title. Plus a Store ledger | XL | P1 |
| L3 Legacy selection (1T) | Per-Legacy carrier mirroring the `POLICY_GOV_*` wildcard Legacy card's `PolicyModifiers` (9 cards, 108 rows). Validity tracked via owner-filtered `Events.GovernmentChanged`. Reading the current government from Gameplay is UNKNOWN | L | P1 |
| L4 diversity slots (+N wildcard) | Numbered carriers with `MODIFIER_PLAYER_CULTURE_ADJUST_GOVERNMENT_SLOTS_MODIFIER`. Building-attached and conditional slots have precedents (Forbidden City, HD Data Center, Golden Age). N comes from confirmed ACTIVE IV counts | M | P2 |
| L4 first policy change per turn free | `SetCivicCompletedThisTurn(true)` at turn start. **Side effects:** it also allows a free government change, and it triggers HD's end-turn reminder. Alternative: refund route | L (with L2) | P1, amplifies |
| L4 governance yields (+k×G%) | `MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_MODIFIER` per tier. A multi-yield argument has an HD precedent | S–M | P0 |

**Performance.** The main risk is indirect. Cheaper policy changes mean more `GovernmentPolicyChanged` events, and each currently triggers a synchronous world Commerce audit (`Mod/CommerceConvergence.lua:168` via the full-scope `Hook`). Narrow these two events to the player before L2/L4 ship; owner-first signatures are evidenced.

**DDR candidates**
- What "Legacy Effect" means. Technically recommended: the native Legacy cards. Each government's engine-coded second bonus cannot be reproduced.
- G under Chiefdom (`Tier=NULL`) and anarchy.
- Policy-cost transaction side effects.
- Legacy duplicated with a slotted card.
- Multiple Government sources and the no-plaza case after capture.
- Study catalog boundary, plus 2T/3T interruption and rounding.

**Spikes**
- S1: Gameplay availability of the government and culture getters.
- S2: `SetCivicCompletedThisTurn` window.
- S3: native unlock transaction.
- S4: dynamic wildcard slot.
- S5: Legacy modifiers attached via a building.
- S6: tier gating via `GovernmentModifiers`.
- S7: study carrier side effects.
- S8: N-turn project.
- S9: plaza capture.

### 4.3 Military — XL, MEDIUM risk

| Ability | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind (Encampment) | AF-28 | M | static |
| Base +3F/+3P per Encampment specialist | CitizenYield carrier | S | event-city |
| Lv2 housing + GPP (General) | Lv2Housing (needs Encampment tier rows; none exist today) + Lv2GPP bits | S–M | event-city |
| Unit eligibility + training snapshot | Route A: native trained-unit grant. Route B: Lua snapshot at birth. Shared building block (§3) | L (XL if attribution fails) | event-unit |
| L3 training quality (+CS per domain with ordinary T1) | Ability via the snapshot + `DistrictCompleteness` T1 facts. Barracks and HD precedent | M on top of the snapshot | event |
| L3 training efficiency (D → unit production %) | `EFFECT_ADJUST_UNIT_PRODUCTION` with a land-combat UnitType list (`DOMAIN_LAND` may include civilians) | M (Design parameters open) | event-city |
| L3 field logistics (1:1 support unit; resource maintenance → Gold) | New unit line + link registry + `IGNORE_RESOURCE_MAINTENANCE` ability toggle. **No per-unit dynamic Gold-maintenance primitive** | XL | event-unit + per turn |
| L4 mentorship / insight (bonus XP) | Combat hook (§3) + `ChangeExperience` | L / M | world-event-filter |
| L4 tradition (Great General consumed → local tradition) | InvestmentAction-style INTENT/Destroy/COMMIT + UnitPanel overlay + Store ledger | L | O(1) |
| Unified Mobilization | Union-find over network components, history-dependent election, HD upgrade-line normalization, per-participant production carriers. `CurrentlyBuilding()` is Gameplay-usable | XL | event-city + topology |

**DDR candidates**
- Which acquisitions count.
- Snapshot route if the grant is retroactive or does not persist.
- Corps/army maximum rule if the consumed unit is unidentifiable.
- Upgrade persistence.
- Combat classification and XP caps.
- Efficiency filter.
- Logistics Gold model and link semantics.
- Tradition location and transfer behaviour.
- Mobilization tie-breaks, persistence of incumbency, UNKNOWN network.

**Spikes**
- S1: grant semantics.
- S2: upgrade and formation.
- S3: combat.
- S4: production list.
- S5: logistics.
- S6: Great General consume.
- S7: Mobilization inputs.
- S8: cost baseline.

### 4.4 Harbor — XL, MEDIUM risk

The **commercial line** needs a route-facts service the pipeline lacks today: maritime flag, incoming foreign routes, per-route yields, foreign relation lifecycle. It also needs a sea-connectivity service (`plot:GetAreaID()` union-find; canals UNKNOWN). The **naval line** mirrors Military and should reuse its snapshot, combat-hook and logistics work.

| Ability | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind + institutions (two sibling rows at III/IV) | AF-28; presentation keyed by institution id | L / S–M | ~0 / UI |
| L2 crew (housing; Admiral GPP) | Lv2 patterns, `GREAT_PERSON_CLASS_ADMIRAL` | S | per-own-city |
| L3 port link (+x per raw marine resource of other Harbor cities in the same sea network) | Sea-connectivity service + signed binary district Gold carriers | M | per-own-city |
| L3 markets (×(1+K·N) on qualified maritime routes) | **Not native per route.** Route-yield % exists only player-wide; the per-city flat applies to all international routes | L | per route |
| L4 export (hinterland BASE adjacency → per maritime route) | Research Cross BASE sampler pattern + aggregator; same delivery gap | L–XL | per own city × districts |
| L4 import (per-civilization supply locks) | UI metrics at 0→1 transitions + Store lifecycle. UNKNOWN must not count as 1→0 | L | O(majors) per event |
| L4 operating (turn counter → permanent route capacity) | Per-turn Store counter + `MODIFIER_PLAYER_ADJUST_TRADE_ROUTE_CAPACITY` carrier (Colossus precedent) | M | per port per turn (+1 Commerce audit per write under AF-06b) |
| Naval snapshot, training quality, training efficiency | Shared with Military (Royal Navy Dockyard precedent) | XL shared / M / S | event |
| Sea logistics | As Military, plus a sea stacking unknown (a sea support/civilian ship escorting a naval unit) | XL | per unit |
| Naval mentorship, insight, tradition (Great Admiral) | Shared combat hook; Admiral consume | L / M / M–L | event |

**Capacity limit.** Harbor raises route counts. If per-route `OriginYields` go on the wire, the sender's 16 KB cap becomes reachable, and over-cap is silent (P13a-Q04). Add an explicit over-cap status and a separate incoming/yield channel first.

**DDR candidates**
- Definition of a maritime route.
- Markets/Export delivery and rounding.
- Static vs dynamic sea connectivity.
- Import lifecycle when a route is renewed.
- Operating ticks on UNKNOWN turns.
- Permanent capacity: revocable building vs irrevocable attach.
- Sea logistics fallback.
- Unit eligibility.
- Formation max-merge.
- Mentorship timing.
- Admiral action location.
- Whether Harbor Gold enters Commerce's Harbor-domain X.

**Spikes S1–S13**
- S1: maritime classification.
- S2: incoming routes.
- S3: per-route scaling.
- S4: `OriginYields` precision.
- S5: sea connectivity.
- S6: capacity carrier.
- S7: civilization metrics.
- S8: attribution.
- S9: combat.
- S10: sea stacking.
- S11: Admiral consume.
- S12: hidden resources.
- S13: non-recursion of Port Link → Export.

### 4.5 Diplomatic Quarter — XL bimodal, LOW–MEDIUM risk

**The Design has no named institutions or abilities.** `Specialization/Design/Diplomatic.md:36-40` says these must not be invented. Assessment is per design line, DIP-002…005.

| Line | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind | AF-28. HD's Diplomatic Quarter needs the `DLC_Ethiopia` criteria; `MaxPerPlayer=-1` (several sources → DDR) | M | P0 |
| DIP-004 visibility +1…+4 | `MODIFIER_PLAYER_ADD_DIPLO_VISIBILITY` carrier (Printing and HD Chancery precedents) | S | P0 |
| DIP-005 Lv1 +1 spy capacity | `MODIFIER_PLAYER_GRANT_SPY` carrier. HD makes Chancery capacity permanent; removal UNKNOWN | S | P0 |
| DIP-003 envoy tiers ×2 (1/3/6) | Duplicate HD's `HD_CityStateBuffedObjects` SMALL/MEDIUM/LARGE rows gated by a carrier (HD Borobudur precedent) | M (+S, +S) | P0, but adds engine modifier volume (about +70–90% of that family; put the gate on the outer subject set) |
| DIP-002 protectorate registry + selection | Persisted registry + a hook into HD's city-state UI (another HD-private dependency) | L | P1 |
| DIP-002 suzerain "cannot be replaced" | **No lock exists.** Only after-the-fact repair via `GiveFreeTokenToPlayer` on `InfluenceChanged`, which HD uses in Gameplay. Rival scandal, Perry and quests can still flip it | XL | P1/P2 |
| DIP-002 majors at peace cannot declare war on protectorates | `BANNED_DIPLOMATIC_ACTION_SPECIFIC_CIVILIZATION` must sit on **each AI major**. The "at peace with the *protector*" (third-party) condition may not be expressible | XL | P1 |
| DIP-005 Lv2 XP on failed missions | UI `SpyMissionCompleted` bridge → Gameplay `ChangeExperience`. Escaped spies are off-map, so the grant must be deferred | M–L | P1 |
| DIP-005 Lv3 death-only reduction / Lv4 never die | Only lever is the escape boost, which also reduces capture. Revive via `InitUnit` loses identity | S approx / XL exact | P0/P1 |
| Mission framework (Diplomat) | About half of the Expedition scaffold transfers, along with its open exit-side defects. The native chooser excludes ALLIED targets | L–XL | P1 |

**DDR candidates**
- Suzerainty repair semantics.
- War-protection alternative.
- Slot scope and lifecycle (OPEN-12).
- Multi-source rule.
- Lv3/Lv4 approximations.
- Lv2 XP details.
- Capacity on ACTIVE drop.
- Diplomat identity.
- Alliance-points fallback.
- Presentation hooks into the HD city-state UI.

**Spikes S1–S12**
- S1–S2: war ban.
- S3: suzerain repair.
- S4–S6: data lines.
- S7: spy XP.
- S8: kill/capture split.
- S9: revive.
- S10: travel to an ally.
- S11: per-ally points.
- S12: spy reads in Gameplay.

### 4.6 Community / Neighborhood — L–XL, MEDIUM (conditionally HIGH) risk

This is the first profession that **mutates population**, moves value between cities, and needs effects on several instances of the same district.

| Ability (candidate) | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind (Neighborhood) | AF-28. Precedence over specialty first-completion is a DDR | L | P0 |
| I base support (+≈3F/+≈3P per specialist, all Neighborhood instances) | Native citizen carrier (one building type per city; per-instance scope UNKNOWN), or plot-property-gated district yield (CultureAesthetic precedent) | M | P1/P2 |
| II 职住融合 (≈0.1·D per specialist per adjacent district) | Same carrier choice per yield; citizen yields are **integer-only** | L | P2 |
| III 众力营城 (+5% production per 10 pop) | **Fully native:** `REQUIREMENT_CITY_HAS_X_POPULATION` tiers + district/building production % with `IsWonder=0` (Kilwa/HD precedent) | S | P0 |
| III international immigration | Per-turn writer; amenities evidenced only in UI; Store ledger; settlement via `City:ChangePopulation(1)` (Gameplay-proven in Firaxis scenarios) | L | P1, P2 at settlement |
| Population policy toggles | Button (S) or project (M) | S/M | P0 |
| Domestic redistribution network | Paired `ChangePopulation(-1/+1)` with readback, bounded per-turn batch, Network COMMUNITY source kind. **HD Hospital hook refunds a −1 75% of the time and adds an extra +1 20% of the time** (District Expansion `suburbs.sql`), so population is not conserved. Food basket after −1 UNKNOWN | XL | P2 (P3 if unbounded) |
| IV 移民拓居 (≈8 immigrants → Settler) | Ledger + `InitUnit` Settler (reserve before init) | M | P0 |
| IV 都会脉络 (transport completeness) | HD classification tables. Rail is **not** in HD's classification | M after DDR | P1 |
| IV 城市肌理 (+≈0.5%/shared district edge) | Edge count + integer city % carriers. 0.5% fractional amount UNKNOWN | M | P1 |

**Performance.** Population and worker events already fan out to many consumers:
- Lv3Effects, CopyYields and Commerce on population changes, at player scope.
- HalfYieldProbe's world loop on every population change.
- Six consumers on worker changes.

Community therefore adds load mainly by **multiplying existing audits**. Before any frequent population writer ships:
- Bound throughput.
- Decide all moves at one point per turn.
- Fix AF-06(b) and the HalfYieldProbe world loop.

**DDR candidates**
- HD Hospital vs conservation.
- Food basket after −1.
- Precedence of the fifth kind.
- Rounding stage.
- 都会脉络 inputs.
- Policy operation.
- Attribution fallback.
- Immigration formula details.
- Distribution ranking and floors.
- Partial-network semantics.
- 众力营城 scope.
- Lv2 structure.
- Settler spawn.
- Edge eligibility.

**Spikes S1–S10**
- S1: `ChangePopulation` behaviour.
- S2: Hospital hook.
- S3: amenities in Gameplay.
- S4: multi-Neighborhood carriers.
- S5: fractional %.
- S6: production scope.
- S7: population requirement timing.
- S8: Settler spawn.
- S9: rail.
- S10: cost per move.

### 4.7 Landscape / Preserve — XL, MEDIUM if bounded

| Ability (candidate) | Route | Diff | Perf |
|---|---|---|---|
| Fifth kind (Preserve) | AF-28. Preserve's domain is unmapped in Shared | M–L | event |
| L1 science/culture compensation on eligible resource improvements | Plot yield (city collection) with improved-resource requirements | S–M | static |
| L1 offset negative Appeal; L2 improvements raise Appeal | **No per-plot or per-improvement Appeal effect found.** Appeal effects are city-wide or per feature type; `Improvements.Appeal` is a static global column | L (gap) | → DDR |
| L2 earlier tree planting | Player-wide `MODIFIER_PLAYER_ADJUST_FEATURE_UNLOCK` (S). A city-gated variant needs `TerrainBuilder.SetFeatureType` in Gameplay, which is unproven (L) | S / L | static |
| L3 Appeal → Gold | `REQUIREMENT_PLOT_IS_APPEAL_BETWEEN` bands × improvement filter. The engine reacts natively. HD resorts convert tile Gold → Tourism, so beware double conversion | S–M | static |
| L3 landscape Gold → Tourism | CultureAesthetic-style district Tourism projection. `plot:GetAppeal` in Gameplay is UNKNOWN | M | per turn per city (≤91 plots) |
| L3 team unit + management capacity (0/1/1+parks) | Expedition-class training gate, source binding, capacity | XL | event + UI |
| L3 ecological maintenance (tile unworkable ~5T; permanent plot gain) | **No native route for "unworkable, displayed yields unchanged."** The gain must follow the plot through ACTIVE loss and transfer, so a city carrier cannot hold it; player/game-scoped plot yields would also benefit non-enabled owners | XL | per task (tiny) |
| L4 early Naturalist / park | City-gated variant unit or `GRANT_UNIT_IN_CITY`. Whether DESIGNATE_PARK is legal before the civic is UNKNOWN | M–L | event |
| L4 park → capacity; park buffer | Park enumeration evidenced only in UI; `Map.GetNeighborPlots` + PF bit | M / M | event |
| L4 habitat propagation | `ResourceBuilder.SetResourceType`. **HD re-purchases owned plots after creating a resource**, which implies a native defect on owned plots. Mother/child records | L–XL | one radius scan per completion |
| Network (amenities, happiness yield) | Amenity carrier + `EFFECT_ADJUST_CITY_HAPPINESS_YIELD` | M–L | event |

**Performance.** Landscape's own Lua is small: about 2k plot reads per turn at 6 cities. The amplifiers are:
- full-scope plot events (`RuntimeWork.lua:80`)
- the global revision counter on every plot-property write
- transfer sweeps
- carrier count

Keep writes diff-only, which the CultureAesthetic guard already does.

**DDR candidates**
- "Unworkable" alternatives.
- Appeal alternatives.
- Planting scope.
- Permanent-gain attachment and eligibility.
- Propagation details.
- Early park.
- Buffer scope.
- Team rules.
- Tourism display and rounding.
- Network aggregation.

**Spikes S1–S13**
- S1: work block.
- S2: per-plot Appeal.
- S3: PF yields across transfer.
- S4: Gameplay API availability.
- S5: resource creation.
- S6: early Naturalist.
- S7: feature placement.
- S8–S9: team.
- S10: parks.
- S11: Appeal bands.
- S12: happiness-yield modifier.
- S13: benchmark.

---

## 5. Suggested sequencing after v0.1 (technical view only; scope and priority are the user's)

1. **Platform first (one batch series):**
   - AF-28 kind descriptor
   - AF-06(b) keyed revisions, plus owner-first normalization for the events these professions use
   - AF-01 Store extension registration
   - typed holds / self-healing reconciliation (AF-12)
   - AF-03 read bridge
2. **First fifth kind to prove the platform: Religion or Government core.**
   - Religion's L1/L2 housing/L3 support/L3 soft lock is mostly native and S.
   - Government's L1, L4 yields and L4 slots are S–M with no new unit or route infrastructure.
   - Either validates the kind descriptor cheaply.
   - Defer Religion Lv3 foreign-pressure and Lv4 absorption, and Government study/policy-cost, until their spikes and DDRs settle.
3. **Military:** builds the unit training snapshot and the combat hook as domain-parametric modules. Logistics last.
4. **Harbor:** reuses the naval snapshot and combat hook. Its commercial line depends on Commerce slice O and the route-facts service.
5. **Diplomatic data lines:** visibility, spy capacity, envoy ×2. These can go early (S, P0) once the kind exists. The protectorate and spy-survival lines wait for spikes. Missions wait for the Expedition fixes and the profession-unit framework.
6. **Community and Landscape last.** Both are still freeze candidates. Both carry native gaps (population conservation under HD; unworkable tiles; per-plot Appeal) that are likely to need Design decisions before a plan.

**One bundled native spike session per profession** (the cheap, read-mostly checks listed above) would settle most route choices before any implementation planning, consistent with W0004.

---

## 6. Performance rules for all future professions

1. Filter to the enabled player and own cities **before** any fact read (SD-08 lesson). Never iterate all players' cities per event or per turn.
2. Never route unit, combat, plot, religion, policy or population events through the full-scope `RuntimeWork.Hook` fallback. Use owner-first handlers or coalesce to a per-turn drain.
3. Writes must be diff-only and batched. Each write currently costs a world Commerce audit until AF-06(b) is fixed.
4. `CityTransfered` cleanup must be scoped to the transferred city (AF-05), with exact-ID exits via `RegisterExit`.
5. Prefer native requirement-driven modifiers (engine-evaluated, about 0 Lua). Keep `BUILDING_SPC_*` row counts low (AF-07).
6. Per-turn reconciliation runs at one point per turn (the existing turn-start hook) and pairs with the existing per-turn GC opportunity.
7. Define one bounded late-game benchmark before the first unit-heavy or population-heavy profession (AF-25; the definition is a user decision).

---

## 7. Unknowns, limits and process notes

- **All native behaviour above is UNKNOWN until spiked.** In particular:
  - trained-unit grant semantics
  - combat event ordering
  - Gameplay availability of UI-evidenced APIs
  - plot-property permanence
  - `ChangePopulation` side effects
  - modifier re-evaluation cost
  - several "absence" claims (no per-plot Appeal effect, no incoming-pressure modifier, no policy-cost modifier, no per-unit Gold maintenance), which are limited to the searched base, DLC and HD files
- **Design maturity varies.** Community and Landscape are candidates. Diplomatic and Religion lack names. Difficulty grades assume the current texts and will shift with the DDR outcomes.
- **HD version is UNKNOWN.** HD-dependent routes (city-state buff tables, Hospital hook, BinaryCompress, resource re-purchase) are tied to the installed version and may change with Workshop updates (AF-04).
- **Process notes:**
  - The Government assessment opened the local composed game cache `DebugGameplay.sqlite` read-only (`mode=ro&immutable=1`) to count rows. That is slightly beyond the external roots named in its brief, but within the user's topic-scoped reading authorization. No other assessment queried a database.
  - No assessment wrote files. This report is the only file written for the topic.
- **Repository basis:** `bae883a`. Mod source is unchanged since the architecture audit's basis (`2b75e12` / `f843c0f`), apart from later documentation and tooling commits.

## Checkpoint / handoff

**Stable file:** `Specialization/Reports/Advisory/Future_Specialization_Feasibility/Future_Specialization_Feasibility.md`. It is ignored locally and contains no personal paths or secrets. Writes are paused.

**Intended use:** an input when planning each post-v0.1 profession. Recommended entry: §2 (platform prerequisites), §3 (shared building blocks), then the profession's §4 section and its spike list.

**User decisions:**
- Scope and priority of future professions.
- The DDR candidates listed per profession, as each profession is scheduled.
- Whether to authorize the per-profession spike sessions.

**User testing:** none requested. **Primary next:** none. This report authorizes no implementation.
