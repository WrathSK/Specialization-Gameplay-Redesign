# Self-Healing Reconciliation Rules (Proposal for User Refinement)

Advisory / Non-authoritative / No design decision implied
Status: Stable (draft rule set for the user to refine; nothing here is adopted)
Maintainer: Advisor session (Claude), attribution only — not session authorization

**Scope.** This is a proposed general rule set for how features recover from missed events, ambiguous native outcomes and stuck states, so that a released mod does not permanently lose functionality per save. It expands the eight rules discussed with the user on 2026-10-13. It also answers the user's question about writing diagnostics to disk (Appendix A).

**Basis.** `develop` at `bae883a`.
- Prior Advisory work:
  - [Architecture_Engineering_Audit/Final_Review.md](../Architecture_Engineering_Audit/Final_Review.md) (AF-12, AF-13, AF-14, Expedition clusters A/B/D/E/H)
  - [Expedition_Review.md](../Architecture_Engineering_Audit/Expedition_Review.md)
  - [Future_Specialization_Feasibility](../Future_Specialization_Feasibility/Future_Specialization_Feasibility.md)
- Appendix A additionally used the local game configuration and Logs folder (read-only) and a web search, both authorized by the user on 2026-10-13.

**Status of every rule below.** These are proposals. Whether, where and how they apply is the user's gameplay decision (DESIGN_DECISION_REQUIRED). Several rules contradict currently recorded decisions; those conflicts are listed explicitly in §7. Nothing here authorizes implementation.

---

## 1. The problem

Most current state machines are **edge-triggered**: they advance only when a specific event is caught. For example:
- Expedition reaches TRAINING on reservation and NAMING on the birth+completion pair.
- It releases capacity only on an explicit UI CANCEL.

When an event is missed — the context isn't loaded, the player used another UI surface (Production Manager), load timing was unlucky, or the native engine never sent it — the record stays where it is. The current policy, "uncertain → HELD", then makes many of these states permanent. Examples:
- Expedition HELD with no unit (cap1 lost for the save)
- Investment INTENT
- Claim CALLING
- tradition UNKNOWN_INTERVAL
- `completionError` on every unassigned city
- an all-or-nothing network capture failing at every cold load

That policy was right for development: it surfaced native unknowns. For a released mod it means "functionality randomly and permanently disappears."

## 2. The principle: periodic level-triggered reconciliation

Treat the saved record as **belief** and the live game as **observation**. At a stable point each turn, compare the two and move belief toward observation using a fixed, safe rule table. A missed event is then no longer fatal: the next reconciliation repairs it. The system needs only "what is true at turn start", not "every edge was captured".

Safety comes from one asymmetry:

| Action class | Requirement | Reason |
|---|---|---|
| **Grant** (reward, permanent achievement, identity, capacity *increase*, Potential) | Positive evidence, granted exactly once | A wrong grant cannot be taken back and may duplicate |
| **Release / revert** (return capacity, clear a hold, re-offer an option, revert to a prior non-terminal phase) | Absence confirmed at a stable boundary | A release grants nothing; the worst case is that the player may try again |

The existing user-endorsed principle "never replay an uncertain irreversible native action" (`Specialization/Architecture/v2/D0032_Adaptation.md:58`) is **kept**. Self-healing never re-executes an uncertain action. It only re-observes and either releases or confirms.

## 3. Rules

**R1 — One reconciliation point per turn, plus load.**
- Reconcile at the enabled local player's turn start (`PlayerTurnActivated`, own player, after native production and movement settle) and once after load (`LoadScreenClose`).
- Never mid-event and never on foreign events.
- This reuses the existing per-turn hook: many writers already reconcile on `PlayerTurnActivated`, Expedition `Pulse` already runs there, and the GC trial is evaluated once per local turn. So this is a change of policy, not a new mechanism.
- Pair it with the existing per-turn GC opportunity. Do not add new periodic timers.

**R2 — Derive whatever the game can tell you; persist only what it cannot.**
- Derive from native state every reconcile:
  - capacity
  - occupancy
  - "does a unit or queue entry exist"
  - current yields
  - ACTIVE
- Persist only history the engine does not keep:
  - source binding
  - receipts of granted rewards
  - ages and counters
  - mother/child links
  - chosen options
- Example: Expedition capacity = owned Expedition units + Expedition queue entries in own cities, derived each reconcile instead of from the stored phase.

**R3 — Bounded scope.**
- Reconciliation reads only the enabled player's own cities and units, plus the specific foreign objects a record names (one target city or holy city).
- No world scans.
- Expected cost: O(own cities + own relevant units) per turn.

**R4 — Unreadable inputs defer; they never escalate.**
- If a needed fact cannot be read this turn (UI reader absent, getter UNKNOWN, network capture not VERIFIED), skip that record this turn and try again next turn.
- Only "read successfully and inconsistent" triggers a rule.
- This replaces "reader unavailable → HELD" (`Mod/ExpeditionTraining.lua:141-148`).

**R5 — Ambiguity has a deadline; at the deadline, release, never grant.**
- Each ambiguous state carries `since` (turn) and a deadline of at least one full turn boundary, so native production and late events have resolved.
- Still ambiguous at the deadline:
  - for release-type resolutions, release (R2/R6);
  - for grant-type resolutions, do not grant and stop waiting (R9).
- Proposed default deadline: the first reconcile at which `currentTurn ≥ since + 1` *and* a full own production phase has passed. The user may set a per-feature deadline.

**R6 — Every release bumps a generation.**
- Releasing a reservation, team or transaction increments the record's generation (the Expedition Store already supports this).
- A late event carrying the old generation is treated as an unrelated new fact and re-evaluated from scratch. It is never bound to the abandoned attempt.
- This is what makes "release on absence" safe against late births or completions.

**R7 — Rewards are receipt-keyed and idempotent.**
- Every grant carries a unique receipt key written in the same commit as the state change.
- Reconciliation that finds the receipt does nothing.
- Reconciliation may therefore run any number of times without duplicate rewards.

**R8 — Prefer reverting to the last safe non-terminal phase over holding.**
- When the evidence shows "the side effect provably did not happen", revert to the phase before the attempt, not to HELD. Examples:
  - travel never submitted
  - a stale request
  - validation failure before any write
- Holding is reserved for R10.

**R9 — Grant-type ambiguity resolves to "no grant + continue".**
- When evidence for a grant is contradictory or missing at the deadline:
  - do not grant;
  - record the lost opportunity in diagnostics;
  - unblock all other functions.
- A single missing grant must not disable unrelated abilities. This removes the current spread through `investmentPending` (AF-12).
- The user may designate specific cases as "player-favourable resolution" (§6, D2).

**R10 — The only remaining hard holds.**
- (a) The persisted record itself is unreadable or corrupt.
- (b) Applying a resolution would require granting without evidence.

Even then:
- hold **only that record**;
- never spread to other cities, other abilities or the whole player (AF-14);
- surface the hold in diagnostics.

**R11 — Partial facts degrade locally.**
- When one city's facts are unavailable, exclude or freeze that city's contribution for this turn and keep everything else.
- Do not fail the player-wide computation.
- This applies to network capture (AF-14, SD-07), to Government's "N distinct ACTIVE IV kinds", and to any future national aggregate.
- Whether to exclude or freeze is a per-aggregate user decision.

**R12 — Typed status, not error strings.**
- Providers return `VERIFIED / PENDING / CONFIRMED_INVALID / TERMINAL_HELD` plus a code.
- Consumers map status to action in one declared table.
- Error strings are diagnostics only.
- This makes R4, R9, R10 and R11 enforceable instead of relying on substring matching (AF-14 / X-02).

**R13 — Validate before mutating.**
- The "mutating" flag (which decides hold vs plain rejection) is set immediately before the first write, never before read-only validation.
- Stale, out-of-phase or invalid requests are plain rejections and the state does not change.
- This fixes Expedition cluster D (NAME after END; CONFIRM/CANCEL before the queue read).

**R14 — One owner per recovery path.**
- Each persisted phase has exactly one module responsible for reconciling it, on load and per turn.
- No split policies. Expedition cluster G is an example: the Gate holds on load and pre-empts Training's finer logic.

**R15 — Player-initiated natural actions are valid resolutions.**
- Where the player can express intent through the native UI, treat it as resolution. Examples:
  - removing the item from production (any surface)
  - changing production away from a 1T project
  - disbanding the unit
- Releases need no special button.
- This is how a release build resolves stuck states without a debug panel.

**R16 — Diagnostics are bounded, always on and non-blocking.**
- Every automatic resolution appends one entry to a bounded per-feature ring (e.g. the last 10 entries: turn, feature, record key, rule, from→to, reason code).
- Development: shown in the P0 panel. Optionally emitted via `print` and the FireTuner channel (Appendix A).
- Release: the same ring exists, but no panel is loaded.
- Diagnostics never change behaviour.

**R17 — Development and release share one code path.**
- Dev builds may additionally keep a "hold before resolving" mode for features under native investigation. A hold is itself information, as the user noted.
- The switch is one flag per feature, read at reconcile time (for example, the presence of the developer companion mod).
- Rules R1–R16 are identical in both builds. Only R16's display and the optional dev-hold differ.

**R18 — Save compatibility.**
- Reconciliation must accept older record shapes it understands.
- For a record from a newer or unknown schema, the default is read-only (no automatic resolution, no destructive cleanup), per AF-27 / Expedition K.
- A load-time conversion to HELD must not be persisted unless R10 applies. Today's in-memory-only conversion (`Mod/ExpeditionSpyGate.lua:21-37`) is the right shape.

**R19 — Cost budget.**
- Per-turn reconciliation must be O(own cities + own relevant units) with diff-only writes, so it does not multiply the world Commerce audits triggered by the global revision counter (AF-06b).
- Each reconcile writes at most one Store record per changed city per turn.

**R20 — No silent semantic substitution.**
- A resolution rule may release, revert, confirm or decline.
- It must not invent a different gameplay outcome. Examples of forbidden substitutions:
  - picking a "most likely" first specialization district;
  - converting a failed task into a partial reward.
- Such choices are explicit per-feature user decisions recorded in Design.

---

## 4. State classification (applies to every feature)

Each persisted transactional record should be classifiable into one of these kinds. Reconciliation logic is then per kind, not per feature.

| Kind | Meaning | Default reconciliation |
|---|---|---|
| `INTENT` | Decided to act; side effect not yet attempted | No side effect observed after the deadline → revert (R8). The side effect is observed → confirm and commit (R7) |
| `SIDE_EFFECT_ATTEMPTED` | Irreversible native call issued; outcome uncertain | Observe its result: success evidence → commit; failure evidence → revert; still ambiguous at the deadline → R9 (no grant) for grant-type, R5 release for capacity-type |
| `WAITING_NATIVE` | Waiting for engine progress (queue, travel, task timer) | Re-observe each turn. A disappeared prerequisite → release (R2/R6) |
| `ACTIVE` | Steady state | Re-derive the effects (carriers) from facts |
| `RELEASED` / `ENDED` | Done | Nothing |
| `TERMINAL_HELD` | Only R10 cases | Record-local; shown in diagnostics |

---

## 5. Application to known stuck points

Proposed defaults, all subject to §6 decisions.

| Feature / state | Today | Proposed reconciliation |
|---|---|---|
| Expedition RESERVED, never queued (`ET:127-128`) | HELD next turn | After the deadline, no queue entry and no unit → release capacity, bump generation, re-offer training |
| Expedition TRAINING, queue emptied by any surface, including Production Manager (`ET:122-126`, load `:123`) | Stranded; HELD after load | Same as above (absence of queue entry and unit). Covers cluster B without intercepting more UI contexts |
| Expedition birth+completion complete at load (`SG:33-35`) | HELD | Re-run the in-session Finish predicate at load (R14) |
| Expedition half receipt past the deadline | HELD | Exactly one Expedition unit exists at the source and is unbound → bind (grant-type, positive evidence). No unit → release |
| Expedition HELD with a surviving unit (various) | END only (destroys a paid unit) | Re-verify identity (one candidate, source and name consistent) → rebind to the last non-terminal phase. Several candidates → keep the bound one; others are ordinary units |
| Expedition TRAVELLING, never submitted (unit still at home after due+1) | HELD | Revert to CREATED (R8) |
| Expedition NAME after END, stale NAME | HELD | Plain rejection (R13) |
| Expedition reader unavailable | HELD after 12 publishes | Defer (R4) |
| Expedition closed or newer schema | BLOCKED; END refused | Read-only (R18). END allowed if the unit is provably owned |
| Investment INTENT, Settler still present | Permanent INTENT; blocks the city's other abilities | Revert INTENT (no consumption happened) |
| Investment INTENT, Settler gone, no receipt | Permanent INTENT | **User decision D2**: R9 (no grant) or player-favourable commit |
| Claim / Dialogue 1T: project removed from the queue, no completion | Claim: CALLING forever; Dialogue: cancellable | Abandon: no reward, timer reset (R15). Unify Claim with Dialogue |
| Claim CALLING with completion evidence but the commit failed | CALLING forever | Re-observe the completion fact (identity now present?) → commit by receipt (R7) |
| Research tradition `UNKNOWN_INTERVAL` / `OWNER_POLICY_UNRESOLVED` | Absorbing | Resume counting from the current turn without crediting missing turns (per D0040 reading; SD-02) |
| District completion not attributable (`CityProgressionStore.lua:1151-1158`) | `completionError` on every UNASSIGNED city | Hold only candidate cities within district range (proposed earlier). Next reconcile: re-read each candidate's completed specialization districts. Exactly one → assign (grant with evidence). None → clear. Several → user decision (R20) |
| Network capture, one city unreadable or unregistered (AF-14, SD-07) | Whole player fails at cold load; consumers withdraw or hold inconsistently | Exclude or freeze that city (R11); typed status (R12) |
| Store worker faulted by a failed write | Faulted for the session; loss exits may not run | Retry the write at the next reconcile with fresh readback. A persistently failing record → R10 local hold only |
| Missed city loss (record ACTIVE, live city foreign) | Never inferred on load | **User decision D5**: infer the loss at reconcile, or keep it held |
| Held return (recapture preconditions failed in the event window) | Permanent HELD_TRANSFER | Persist "return evidence accepted, preconditions pending"; re-check the preconditions each reconcile |

---

## 6. Decisions for the user to refine

These are DESIGN_DECISION_REQUIRED and are not decided here.

1. **D1 — Adopt the principle at all.** Self-healing as the release policy, with development holds optionally retained per feature (R17).
2. **D2 — Player-favourable cases.** Which grant-type ambiguities resolve in the player's favour rather than R9. Prime candidate: Investment INTENT where the Settler is gone.
3. **D3 — Deadlines.** The global default (R5) and any per-feature overrides (e.g. long tasks).
4. **D4 — Tolerance for rare over-capacity.** Accept that a race may briefly yield one extra team or unit, given R6 generations.
5. **D5 — Inferred loss and late return** (AF-13): infer a missed city loss at reconcile; accept a held return later once preconditions pass.
6. **D6 — Partial aggregates** (R11): per aggregate (network, Government N, future national counts), exclude vs freeze an unreadable city.
7. **D7 — Natural-action resolutions** (R15): which native actions count as abandonment (queue removal, production change, disband).
8. **D8 — Multi-candidate first completion** (district attribution): the rule when several specialization districts complete in the same unattributable window.
9. **D9 — Diagnostics surface in release** (R16): ring kept but hidden, or a minimal player-facing notification for resolutions that cost the player something.
10. **D10 — Scope.** Apply the rules retroactively to v0.1 features (Expedition, Claim, Investment, tradition, Store) before release, or only to new features.

## 7. Conflicts with currently recorded decisions

These need explicit user revision if the rules are adopted. They are not silently overridden here.

- **`Specialization/Architecture/v2/P0_N_Expedition.md:25` and B202 local `:10`** — "an empty queue alone does not release capacity." R2/R5 would release on confirmed absence after a deadline.
- **`P0_N_Expedition.md:58`** — a failed or ambiguous write keeps a bounded reservation or hold. R5 adds a deadline and a release.
- **`P0_N_Expedition.md:18`** — "do not silently … alter production on an ambiguous race." The rules never alter production; they release only capacity. Compatible, but worth confirming.
- **`P0_N_Expedition.md:94`** — "do not delete an old team to free a slot." The rules never delete a living team, so they are compatible. Releasing a slot when *no* team exists is the new element (D4).
- **B107 district-completion hold design** (`DevelopmentTests/test_b107_e2_founding.py:157-158`) — narrowed by the proposal; the test would change.
- **B169 UNKNOWN-reservation blocking of loss writes and admissions** (`Specialization/Architecture/Specialization_v0.1_Architecture.md:79`) — interacts with R10/R11 (Final_Review §6 item 4).

## 8. Suggested adoption path (if approved)

1. Record the accepted rules as a Shared-level contract (Design/Architecture, by Primary under authorization). Every feature then follows one policy.
2. Implement the typed status (R12) and the bounded diagnostics ring (R16) first. Both are small and make every later step observable.
3. Apply to Expedition first: cluster B via R2/R5, clusters A/D/E/G/H. Capacity is the most visible per-save loss and is directly involved in the B204 work.
4. Then Investment/Claim (R8/R9/R15), the district-completion hold, and the network capture (R11).
5. New features (Commerce, Industry, future professions) adopt the rules from the start. Their transaction designs only need to name their record kinds (§4) and deadlines.

---

## Appendix A — Diagnostics to disk (user-authorized local check and web search, 2026-10-13)

**Local facts** (read-only):
- The machine is Apple Silicon (`arm64`, M2 Pro).
- The game's Logs folder (`<CivUser>/Firaxis Games/Sid Meier's Civilization VI/Logs`) holds about 65 engine logs and CSVs, including:
  - `UserInterface.log`, which records `[DataError]` lines, e.g. a missing icon for the overflow-sink test project — a real minor finding;
  - `Modding.log`, `Database.log`, `GameCore.log`, `Startup.log`.
- There is **no `Lua.log`**.
- `AppOptions.txt` `[Debug]`: `EnableTuner 0`, `EnableDebugMenu 1`, `EnableLogCollection 0`, `EnableGameCoreEventLog 0`.

**External information** (another author's report; not verified here):
- A Civ VI tooling project built on Apple Silicon states that `Lua.log` "is not written on ARM Macs", while the FireTuner socket (enabled by `EnableTuner 1`) does open there. It uses that socket (localhost) to run Lua and read results back ([civ6-logger](https://github.com/PatrickJYKang/civ6-logger)).
- Community guidance: `print` output goes to `Lua.log` on Windows. FireTuner's Lua panel shows it live; FireTuner is enabled via `[Debug] EnableTuner 1` ([CivFanatics thread](https://forums.civfanatics.com/threads/how-to-use-lua-print.605740)).
- The macOS options file location matches the local finding ([Firaxis file locations](https://support.civilization.com/hc/en-us/articles/37657122743699)).

**Inference.**
- The missing `Lua.log` is most likely platform behaviour, not a project misconfiguration.
- The project's existing `print('[SPC]…')` lines are therefore currently invisible on this machine, which is consistent with the repository records ("Lua.log not found").

**Options** (user decision; nothing changed):
1. **Keep the P0 panel plus the bounded diagnostics ring (R16).** Zero setup, and it works in the current workflow (screenshots).
2. **FireTuner channel.** Set `EnableTuner 1` and read `print` output or query a diagnostics table over the local tuner socket, with a small local reader script. Costs:
   - a local-only remote-code surface while enabled, so turn it off after sessions;
   - possibly achievement implications (Windows labels the option "disables achievements");
   - it needs a tool that does not exist yet, which Primary would build under authorization.
   - It would let the native-test workflow capture exact event sequences without screenshots.
3. Engine CSV logs cannot carry mod output. They are useful only as native context (AI, trade, city build queues).

A one-session check of option 2 — enable the tuner, confirm the socket opens and that `print` output or a Lua query is retrievable — would settle it. That would be a game launch, which is the user's to perform.

## Checkpoint / handoff

**Stable file:** `Specialization/Reports/Advisory/Self_Healing_Rules/Self_Healing_Reconciliation_Rules.md`. It is ignored locally and contains no personal paths or secrets; `<CivUser>` is the game's user-data root. Writes are paused.

**User decision:** D1–D10 and the §7 conflicts; the diagnostics option in Appendix A.

**User testing:** none requested. **Primary next:** none, unless the user adopts rules and authorizes recording or implementation.
