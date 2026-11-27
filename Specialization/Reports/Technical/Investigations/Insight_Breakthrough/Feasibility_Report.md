# Insight Breakthrough (洞见突破) — technical feasibility

Investigation / Non-authoritative / No design decision implied

Status: Stable

Maintainer: Primary, by explicit Owner handoff on 2026-11-27.

Scope: native support for the Owner's first-draft rules (below). Excluded: final gameplay design, project cost, usage limits, the manuscript requirement, implementation, prototypes and native tests.

Basis:

- Repository: develop `346239a5abd3f318a6be438437dbee736529af56` (clean; B552.579 installed). Design: D0067, which contains no 洞见突破 text.
- Database: the configured `debug_gameplay_db`, the pinned B413 HD baseline, SHA256 `d483b5f2848907329b8439dc257c061ea285c4b90a88c22bdb792f0e4ab42439`, read-only. It also contains this mod's own rows; every count below excludes `SPC_*` rows.
- External sources, cited by label:
  - `<Civ6 Assets>`: the installed game's `Assets` directory (base game and DLC).
  - `<HD>`: Harmony in Diversity, Steam Workshop item 2465378070, modinfo version 2.2.
  - `<Workshop N>`: other locally installed Workshop items, by item ID.

Evidence labels: STATIC_CONFIRMED means code or database evidence. USER_GAME_TEST_PASS means a scenario the Owner tested in game. USER_GAME_TEST_REQUIRED means still untested in game.

## Summary

**Feasible. Nothing blocks it.** Each of the five questions has a native or HD precedent:

| Question | Answer | Main limit |
|---|---|---|
| Detect tech completion | Yes: `Events.ResearchCompleted` | The payload carries no completion source |
| Query prerequisites and Eureka state | Yes: `TechnologyPrereqs`, `HasBoostBeenTriggered`, `HasTech`, `CanResearch` | None found |
| Complete the chosen tech immediately | Yes: `SetResearchProgress(tech, GetResearchCost(tech))`, which HD's free tech uses | Timing and event order not yet seen in game |
| Prevent chains | Yes: our own code starts the completion, so it can mark it | A short-lived marker should be saved |
| Player selection | Yes: our own window plus the existing request path | Do not replace the HD tech tree |

Three facts need one short native check (see the last section). The open design questions are listed under Handoff.

## The first draft under investigation

As the Owner supplied it on 2026-11-27 (not Design):

1. A Research IV city completes a dedicated project and becomes Prepared.
2. When the civilization completes Technology A, its direct successors are inspected.
3. Technology B qualifies when all of these hold:
   - A is a direct prerequisite of B;
   - every other prerequisite of B is complete;
   - B's Eureka has triggered;
   - B is not complete and can be researched now.
4. If candidates exist, the player may pick one, and it completes immediately.
5. A successful breakthrough consumes the Prepared state.
6. With no candidate, the Prepared state stays.
7. A tech completed by a breakthrough cannot trigger another breakthrough.

The original candidate also needed one unredeemed Great Scientist manuscript per breakthrough. Whether that stays is open.

**Owner decision, 2026-11-27:** the prerequisite check does not distinguish how a technology was completed.

## Confirmed facts and evidence

### 1. Detecting completion

- **The event exists and carries three arguments** (STATIC_CONFIRMED). `Events.ResearchCompleted(player, tech, isCanceled)`. Source: `<Civ6 Assets>/Base/Assets/UI/WorldViewIconsManager.lua:395`; other base UI handlers take the first two arguments only.
- **It works in Gameplay context** (STATIC_CONFIRMED). This mod already listens to it in production: `Mod/Commerce.lua:703` and `Mod/SampleLifecycle.lua:210`.
- **It has no source field.** Normal research, goody huts, Oxford University, HD free tech and Great Person grants all raise the same event. Under the Owner decision above this does not matter: any completed tech counts.
- **`isCanceled=true` should be ignored.** What it means is not documented.

### 2. Prerequisites and Eureka state

- **Prerequisites** (STATIC_CONFIRMED). The `TechnologyPrereqs(Technology, PrereqTech)` table holds 167 rows for 99 technologies. One technology has at most 6 prerequisites (`TECH_OFFWORLD_MISSION`), and 103 technologies act as a prerequisite of something. Finding A's direct successors is one small scan of this table.
- **The query methods run in Gameplay context** (STATIC_CONFIRMED). `<HD>` Gameplay scripts call them:

| Method | Where HD calls it |
|---|---|
| `HasBoostBeenTriggered` | `Gameplay/Boosts.lua:34` |
| `TriggerBoost` | `Gameplay/Boosts.lua:40` |
| `HasTech` | `Gameplay/GreatPersons.lua:39` |
| `GetResearchCost` | `Gameplay/GreatPersons.lua:69` |

  `CanResearch` runs in a Gameplay script at `<Workshop 2772516161>/Gameplay/OverflowBugFixGameplay.lua:9`.
- **Eureka coverage** (STATIC_CONFIRMED). 104 technologies; 99 have a `Boosts` row, all at `Boost=34`. The five without one are `TECH_ANIMAL_HUSBANDRY`, `TECH_MINING`, `TECH_POTTERY`, `TECH_FUTURE_TECH` and `TECH_FAKE_TECH`. Under rule 3 these five can never be candidates. That is a property of the rule, not a defect.

### 3. Completing a selected technology

- **Recommended: set progress to full cost** (STATIC_CONFIRMED precedent). `<HD>/Gameplay/Misc.lua:172–180` implements HD's free tech. A tech-tree click calls `GameEvents.HD_FreeTechSwitch`. The Gameplay handler decrements the `HD_FREE_TECH` player property and calls `SetResearchProgress(techId, GetResearchCost(techId))`. The base Napoleon scenario does the same in `<Civ6 Assets>/Base/Assets/Scenarios/NapoleonScenario/NapoleonScenario_StartScript.lua:15`.
- **Not seen in our own game** (USER_GAME_TEST_REQUIRED):
  - whether completion happens at once or at the next turn processing;
  - whether `ResearchCompleted` fires exactly once, and when;
  - whether it behaves the same on a technology that is not the current research.

  HD's working feature is strong supporting evidence, not a test of ours.
- **Possible interaction with another mod.** The pinned database contains `TECH_FAKE_TECH`. That comes from `<Workshop 2772516161>` (Science/Civic overflow fix), which temporarily switches current research to a fake technology (`OverflowBugFixGameplay.lua:1–23`). The native check should confirm the two do not conflict.

Alternatives considered:

| Mechanism | Evidence | Verdict |
|---|---|---|
| `MODIFIER_PLAYER_GRANT_SPECIFIC_TECHNOLOGY` (`TechType` argument) | 6 non-mod uses, e.g. `TRAIT_MAORI_MANA_SAILING` | Needs one modifier, and in practice one carrier, per technology (about 99). B534 retired 1,126 similar hidden buildings because they made every city query them on load. Not recommended |
| `SetTech(index, true)` | DLC scenarios only, e.g. `<Civ6 Assets>/DLC/NubiaScenario/Scripts/NubiaScenario.lua:228` | Unknown whether it runs the normal completion pipeline (event, era score, unlocks). Not recommended |
| `ChangeCurrentResearchProgress` | Several Workshop scripts | Only affects the current research; we would have to change the player's research target. Not recommended |
| `TriggerBoost` | `<HD>/Gameplay/Boosts.lua:40` | Grants a Eureka, not a completion. Not applicable |
| `MODIFIER_PLAYER_GRANT_RANDOM_TECHNOLOGY` | Goody huts, Oxford | Random choice, so the player cannot pick. Not applicable |

### 4. Preventing chains (rule 7)

- **A marker set before completion.** Our Gameplay code starts every breakthrough completion. Before calling `SetResearchProgress`, it records "B is being completed by a breakthrough". When `ResearchCompleted(player, B)` arrives, it opens no new breakthrough opportunity and clears the marker.
- **Save the marker.** If the event turns out to fire later, at turn processing, a save can fall between the call and the event. So the marker should be saved: one integer per player, cleared on use.
- **Unaffected by the Owner decision.** That decision is about prerequisite checks. Rule 7 is about what counts as a trigger, and it stays.

### 5. Player selection

- **Request path** (STATIC_CONFIRMED in this mod). UI-to-Gameplay requests go through the existing script request (`UI.RequestPlayerOperation` with `EXECUTE_SCRIPT`). The Gameplay side re-checks everything before completing: B is still incomplete, still researchable and Eureka-triggered, the opportunity is still current, and Prepared is still held.
- **UI shape.** A small dedicated window listing the current candidates.
- **Do not replace the tech tree.** `<HD>/UI/Replacement/DL_TechTree.lua:16–31` already replaces `TechTree.lua`; a second replacement would conflict.
- **HD's free-tech flow is a UX precedent only.** It calls Gameplay directly from UI through `ExposedMembers.GameEvents` (`<HD>/Gameplay/Misc.lua:4`) instead of a player operation, so we cannot reuse the code.
- **Reusing the `HD_FREE_TECH` counter is not recommended.** HD's tech tree lets the player spend it on any researchable technology, so rule 3 cannot be enforced. It would also share a counter with HD's own grants (Oxford, Arecibo, Grace Hopper, an Aeronautical commemoration) and make the ability depend on HD.

### Prior native evidence about boosts

From the retired Research network boost, B055–B058 (USER_GAME_TEST_PASS within those tests; it does not cover this ability):

- player-level boost-percentage modifiers work natively;
- HD's base Eureka is 34% of cost;
- extra percentage points are truncated to an integer before they affect progress;
- Eurekas already triggered are not re-granted.

The display-only HD property `HD_Player_Extra_Tech_Boost` mirrors such bonuses in tooltips (`<HD>/UI/Loaders/ToolTipLoader_TCP.lua:76`); the actual effect is `MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST`. The original records were retired with the Network boost carriers in B534 (`eab3968d`). The earlier Status history is at commit `36eceb2bf6d5d619783c02546a053a8c25896f33`, file `Specialization/Status/Specialization_P0_Status.md`.

## Minimal persistent state (inference)

| State | Scope | Why it must survive a save |
|---|---|---|
| Prepared | one flag per city, in the existing city progression Store | It is spent later |
| Open opportunity | one record per player: the triggering technology A | Without it, a reload before the player chooses loses the opportunity |
| Breakthrough in progress | one integer per player, cleared on use | Rule 7, in case the event is deferred |

Candidate lists are recomputed when the window opens and are never stored. The Prepared project can probably reuse the existing project infrastructure; that has not been checked in detail.

## Inferences, counter-evidence and unknowns

- **The free-tech precedent is behavioural, not measured.** That HD's free tech completes a technology is inferred from a shipped feature. It has not been observed in this mod's context.
- **`isCanceled` is undocumented.** Its meaning in the completion event is unknown.
- **Multiplayer and AI are out of scope.** The current player scope is single-player human only.
- **Overflow is untested.** Unknown whether completing a technology that is also the current research moves surplus science onto the next technology as normal.

## Minimal native check (suggestion, not a test result)

One short session with the test panel:

1. Choose a technology whose Eureka has triggered and that is not yet researched. Set its progress to full cost.
2. Record whether it completes at once, how many times `ResearchCompleted` fires and when, and whether current research is affected.
3. Save and reload, and confirm the result persists.

This answers the timing, event-order and overflow questions above. It is a suggestion only and authorizes no implementation.

## Read Ledger

- **Stage A:** `Specialization/Design/Research.md` (D0067; no 洞见突破 text); `local/config.json` for the pinned database; the Owner's first-draft rules.
- **Stage B, repository history:** retired boost work (`eab3968d`: the prior `Mod/Data/NetworkBoost.sql`) and the historical Status at `36eceb2b` (B055–B058 sections).
- **Stage B, database:** `DynamicModifiers`, `Modifiers` and `ModifierArguments` for tech, boost and science effects; `GlobalParameters`; `Boosts`; `Technologies`; `TechnologyPrereqs`.
- **Stage B, external:** `<Civ6 Assets>` and `<Workshop *>` Lua, searched only for the specific API names `TriggerBoost`, `SetResearchProgress`, `ChangeCurrentResearchProgress`, `SetTech`, `SetResearchingTech`, `HasBoostBeenTriggered`, `HasTech`, `CanResearch`, `GetResearchCost`, `ResearchCompleted`, `HD_FREE_TECH` and `HD_Player_Extra_Tech_Boost`. The matching definitions and call sites were then read in `<HD>/Gameplay/Misc.lua`, `<HD>/Gameplay/Boosts.lua`, `<HD>/UI/Replacement/DL_TechTree.lua` and `<Workshop 2772516161>/Gameplay/OverflowBugFixGameplay.lua`.
- **Not done:** recursive reading of HD or other mods; reading backups; native tests.

## Handoff

- **Completed scope:** the five feasibility questions, the alternative mechanisms and a minimal state outline.
- **Key limits:** completion timing and event order are untested in game; the event carries no source.
- **Interpretation to confirm.** The Owner decision is read as covering both A and B's other prerequisites. Any completion of A opens the check, and any completed prerequisite of B satisfies it; only a breakthrough-completed technology is excluded as a trigger (rule 7).
- **Decisions for the Owner:**
  1. How long an unused opportunity lasts: the current turn only, until the next completion, or until used.
  2. With several Prepared cities, which one is consumed; and what happens to Prepared when a city is lost or drops below ACTIVE IV.
  3. Project cost, usage limits and the manuscript requirement (already open).
- **Continuation:** after the design decisions and the native check, Primary may plan Design and implementation under separate authorization.
