# Expedition B202–B204 Training and Source Binding Review (Phase A, independent)

Advisory / Non-authoritative / No design decision implied
Status: Stable (Phase A content frozen before Phase B)
Maintainer: Advisor session (Claude), attribution only — not session authorization
Scope: Correctness and structural review of B202–B204 Expedition training and source binding: reservation, production completion, unit identification, source-city verification, save/load, cancellation, ambiguous native outcomes. Cross-cutting Expedition risks are referenced to [Architecture_Findings.md](Architecture_Findings.md). Excluded: the already-known requirement that B204 needs a native user test. No test is requested here.
Basis: `develop` at `2b75e12` (HEAD later `f843c0f`, no `Mod/` or test change); runtime B204.231 (source `84773a8`). External, read-only base-game UI under `<CivVI>/Civ6.app/Contents/Assets/` (Base and Expansion2). HD = Workshop `2465378070`.

**Evidence status.** Everything below is STATIC_CONFIRMED source reading, or is labelled as inference. B204 remains USER_GAME_TEST_REQUIRED. Other agents' native records (B201–B203 reviews) are cited as another agent's interpretation. **[owner-verified]** marks lines the report owner re-read directly.

## Overall assessment

The B202–B204 design has several strengths:
- write-ahead reservation before any native action
- joint evidence binding (reserved city + queued entry + matching completion + one birth at the source + an exact unit count), with no guessing
- idempotent receipts in either event order
- a CAS/readback Store
- a generation-scoped team key

Within the happy path, nothing reviewed can create a duplicate team or grant something twice.

The weakness is structural and sits on the *exit* side:

1. **HELD is a terminal sink** (cluster A). Many paths enter it. The only exit destroys a live unit, and when no unit exists there is no exit at all. The player's single Expedition capacity (cap1) is then lost for the rest of that save.
2. **Cancellation is proven only by intercepting functions inside one UI context** (cluster B). Stock-UI removal paths outside that context strand the reservation, and after a reload it becomes a permanent unit-less HELD.
3. Several requests set the "mutating" flag before read-only validation, so stale or out-of-phase requests become terminal holds (D).
4. Durable Gameplay commits are followed by one-shot UI follow-ups that nothing recovers (E).
5. Gameplay authority depends on a UI-context reader hosted in the shared ProductionPanel replacement (F; see AF-03).

None of this blocks the pending B204 native test, which exercises the normal path. All of it matters before reattachment, N2 rewards and repeat missions build on this binding.

## Ratings summary

| Cluster | Root cause | Sev / Timing |
|---|---|---|
| A | HELD is a terminal sink: no team-preserving exit, no exit at all without a unit | HIGH / FBDF |
| B | Cancellation proven only by ProductionPanel interception; stock-UI removal elsewhere strands TRAINING | MEDIUM–HIGH / FIX_NOW |
| C | Completion event with `cancelled=true` treated as a terminal mismatch | LOW–MEDIUM (conditional) / FBDF |
| D | Mutation flag set before read-only validation → validation-only failures become HELD | MEDIUM / FBDF |
| E | Durable commit, then a one-shot UI follow-up with no recovery owner (reserve, cancel, travel) | MEDIUM / FBDF |
| F | Gameplay transitions depend on a UI-context reader in a single-winner replaced context | MEDIUM / FBDF (current impact LOW) |
| G | TRAINING load recovery split across Gate and Training; a complete receipt pair is HELD on load | LOW / MONITOR |
| H | HELD overloads meanings, discards the prior phase, stops tracking, records unreliable reasons | MEDIUM / FBDF (before reattachment) |
| I | Identity across native travel = native citizen-name equality + one-unit-per-type uniqueness | MEDIUM (long term) / FBDF; LOW in current scope |
| J | Source identity is an owner-scoped opaque reference; post-transfer cleanup depends on listener order | LOW / FBDF |
| K | Store schema closed and unversioned: a newer record reads as corrupt and END is blocked | LOW–MEDIUM / FBDF |
| L | Singleton runtime state, legacy gate still packaged, duplicate naming pipelines | LOW / DEFER (FBDF before multi-player) |

Where the two independent slices disagreed (E1 versus E2), both ratings are noted in the cluster.

## Lifecycle path table

`ET` = `Mod/ExpeditionTraining.lua`, `SG` = `Mod/ExpeditionSpyGate.lua`, `TUI` = `Mod/UI/ExpeditionTrainingUI.lua`, `CPO` = `Mod/UI/CrewProjectOrder.lua`.

| # | Path | Code path | Outcome | Defect? |
|---|---|---|---|---|
| L1 | Eligibility sync | TUI:28-37 → ET:61-63 | read-only `{eligible, phase}` | No |
| L2 | Reserve accepted | TUI:53-58 → ET:64-68 → SG:490-501 (save + readback) → marker | TRAINING persisted before marker and BUILD | No (strength) |
| L3 | Reserve rejected before mutation | ET:65-66; `mutation=false` (ET:58,79) | error reply, no state | No |
| L4 | Reserve fails after mutation (marker create or readback) | ET:67 → ET:36-45 → SG:129-139 | HELD, no unit | Fail-closed by design; enters A |
| L5 | BUILD issued and confirmed | TUI:85-106 → ET:69-76 (`n==1`) | TRAINING + queued | No |
| L6 | CONFIRM ack lost | ET:119-121 (Pulse self-heals) | queued set by Pulse | No (strength) |
| L7 | Reserve handshake lost before BUILD (age >12 at TUI:81-82; BUILD error at :96-97; QUEUE unconfirmed at :108-109; busy drop at ET:57) | next turn ET:127-128 | HELD, no unit (`TRAINING_ORDER_OUTCOME_UNKNOWN`) | **Yes** (E) [owner-verified TUI:81-82] |
| L8 | Deselected or native-denied after reserve | TUI:89-93 → CANCEL → ET:72-73 → SG:528-532 | ENDED, capacity freed | No (correct compensation) |
| L9 | Normal completion, either event order | ET:84-103 → SG:502-512; Pulse ET:113-114 → Finish | NAMING, bound to the exact unit | No (strength) |
| L10 | Duplicate notifications | SG:507; ET:89,99 | idempotent | No |
| L11 | Birth before queue confirmation | ET:90 | HELD with unit | Fail-closed; rare |
| L12 | Completion with `cancelled=true` for the reserved city and type | ET:100 → hold; later CANCEL refused at ET:70 | HELD, no unit | **Conditional** (C) |
| L13 | Half receipt across a turn | ET:116-118 | HELD | Genuine ambiguity; by design |
| L14 | Queue entry remains after both receipts | ET:115 | HELD with unit | Fail-closed |
| L15 | Explicit cancel in ProductionPanel | CPO:82-86 → TUI:60-67,101-106 → ET:69-73 → SG:528-532 | ENDED if the empty queue is seen within 12 ticks | No (budget caveat a3) |
| L16 | Replacement in ProductionPanel | CPO:91-97 (REPLACE_AT) → as L15 | ENDED | No |
| L17 | **Removal in ProductionManager** | base `ProductionManager.lua:210,291` → `ProductionHelper.lua:196-202` (not intercepted) → ET:122-126 in session; ET:123 on load | stranded TRAINING; HELD with no unit after load | **Yes** (B, a1) [owner-verified] |
| L18 | District or wonder placement replacing the reserved slot | base `Panels/ProductionPanel.lua:360-363,394-396` → CPO:91-96 (arms CANCEL at click) → BUILD only at confirmation (`StrategicView_MapPlacement.lua:26-31,72,248-253`) | ENDED if confirmed within budget; otherwise as L17 | **Conditional** (B, a2) |
| L19 | CANCEL follow-up lost (budget expiry, transmit throw, busy drop) | TUI:81-82,108-109,105-106; ET:57 | as L17 | **Yes** (B/E, a3) |
| L20 | CANCEL while Gameplay still reads `n==1` | ET:71-73 (mutation flag before the read) | HELD, no unit | **Yes, LOW** (D, a6) |
| L21 | Load: queued, entry present | ET:119-121 | resumes | No |
| L22 | Load: queued, entry missing | ET:123 | HELD, no unit | By design; compounds B |
| L23 | Load: reserved, not queued, same turn | ET:127 (no error), next turn ET:128 | HELD next turn; item not re-offered (TUI:43) | **Yes, LOW** (E) |
| L24 | Load with any receipt | SG:33-35 (in memory only) | HELD; a complete pair too | LOW (G, a11) |
| L25 | Load: queue reader missing | ET:109-110,142-148 | HELD after 12 publishes | Fail-closed (F) |
| L26 | Load: store corrupt, unreadable or newer schema | SG:24-27,331; `ExpeditionSpyStore.lua:89-96,113-115` | BLOCKED; END refused | A/K |
| L27 | Source captured during TRAINING | ET:153 (`TRAINING_SOURCE_CHANGED`) or CPS exit ET:154-157 (`TRAINING_SOURCE_LOST`) | HELD, no unit; marker removed only if CPS ran first | A (DDR) + J (a9) |
| L28 | Unrelated city transfer | ET:153; SG:580-585 | re-verify, no change | No |
| L29 | Naming reaches READY | `UI/ExpeditionTrainingName.lua:58-88` → SG:372-373,171-199 | CREATED | No |
| L30 | Naming PENDING or INVALID | ExpeditionTrainingName:76-77,103-108 | stays NAMING; observer STOPPED for the session | I |
| L31 | Gate-side NAME validation fails | SG:372-373,546 | HELD with unit | D |
| L32 | NAME processed after P0 END | SG:469 → :172-173 → :546 → :129-139 | ENDED becomes HELD, no unit | **Yes, LOW** (D, a5) |
| L33 | DISPATCH reply lost or pre-submit denial | SG:383-387; `UI/ExpeditionSpyWindow.lua:324-342,436-442,577-590`; `ExpeditionSpyRead.lua:376` | HELD at dueTurn+2, or immediately via STOP | **Yes** (E, a8) |
| L34 | P0 END | SG:461-469; Window:657 | ENDED, unit destroyed | The only exit from HELD with a unit |
| L35 | Unit removed by script or unknown cause | SG:586-588 (counter only); observe → :75-79/:242 | HELD, no unit | A |

## Clusters

### A. HELD is a terminal sink — HIGH / FBDF

E1-01 and E2-02 (both verifiers: QUALIFIED HIGH); E1-05 as a sub-case.

**Facts**
- `SG:129-139` `hold()` sets `phase='HELD'`, keeps only `stop`/`errorStep`/`errorDetail`, and saves unless the store is blocked.
- No exit path keeps the team:
  - CREATE refuses HELD (`SG:333`).
  - `T.Available` requires phase nil or ENDED and `#list==0` (`SG:486-489`).
  - Evidence, Finish and Cancel all require TRAINING (`SG:503,515,529`).
  - END requires an owned unit and `#list==1`, and destroys it (`SG:461-469`). It is sent only from the P0 DIAGNOSTIC view (`ExpeditionSpyWindow.lua:657`).
  - Everything except READ is refused while `storeBlocked` is set (`SG:331`).
- Entries to a unit-less HELD go through `failure()` → `T.Hold` (`ET:36-45`):
  - marker failure (`ET:67`)
  - completion mismatch (`:100`)
  - incomplete receipt (`:116-118`)
  - loaded queue missing (`:123`)
  - order outcome unknown (`:127-128`)
  - reader budget exhausted (`:143-148`)
  - source exit or change (`:9-13`, `:153-157`)
- Unit loss is only counted (`SG:586-588`); absence becomes `TEST_TEAM_CHANGED` / `NATIVE_IDENTITY_UNCONFIRMED`.
- Design: the cap counts surviving teams, and deleting an old team to free a slot is ruled out (`P0_N_Expedition.md:94`, 不删除旧团腾槽). A failed or ambiguous write keeps a bounded reservation or hold (`:58`).
- Tests assert HELD and not Available (`test_expedition_training.py:79-82,89-90,99-100`). No test exercises an exit from a unit-less HELD.

**Hold entries classified by evidence kind** (derived from code; this is what a future resolver would need to distinguish):

| Source | Unit? | Evidence kind |
|---|---|---|
| RESERVE marker or readback failure (ET:67) | No | Technical; BUILD was never issued (TUI builds only after `reply.reserved`) |
| ORDER_OUTCOME_UNKNOWN (ET:127-128) | No | Reserved, never seen queued; the `T.Cancel` predicate shape (SG:528-531) can be re-proved |
| LOADED_QUEUE_MISSING (ET:123) | No | Queued earlier, now empty, no receipts; `#list==0` can be re-proved |
| Reader unavailable or throwing (ET:22-29,143-148) | No | Transient UI infrastructure |
| Cancelled completion (ET:100) | No | Evidence of non-completion, misclassified (C) |
| Source exit or change in TRAINING | No | Confirmed negative or reference change |
| Half receipt (ET:116-118) | If born | Genuine ambiguity |
| Load with receipt (SG:33-35) | If born | Half pair ambiguous; full pair re-derivable (G) |
| NAME validation (SG:372-373) | Yes (none after END) | Validation only; nothing written (D) |
| STOP after travel pre-submit failure | Yes | Confirmed not-submitted (E) |
| NATIVE_IDENTITY_UNCONFIRMED / TEST_TEAM_CHANGED | No (as observed) | Ambiguous: travel or loss |
| Source or target change after creation (SG:96-119) | Yes | Design treats these as non-terminal (H) |
| STORE_CORRUPT / UNREADABLE (SG:24-27) | Any | Infrastructure; also blocks END |

**Counterevidence**
- Fail-closed hold is explicitly approved (`P0_N_Expedition.md:18,58`).
- Errors before mutation do not hold.
- A store-write-failure HELD lasts only for the session (`SG:45,136`).
- The load-time HELD conversion is in memory only (`SG:21-37`), so a future policy can re-evaluate persisted TRAINING, CREATING and ENDING records.
- Realistic unit-loss triggers are few (`CanCapture=0`, no native actions).

**Consequence.** Reattachment (`P0_N_Expedition.md:33,117`) and N2 commits that copy the assert→HELD pattern add more entries while the exits stay "END or nothing". N2's "unit loss does not clear history" rule (`:147`) has no confirmed-loss trigger to hook into.

**Remediation boundary (advisory)**
- Record a structured hold kind (ambiguous / confirmed-no-team / validation-only / transient-UI / with-unit) with Store invariants.
- Add one Gameplay-owned, bounded resolver that re-proves facts fresh, reusing the `T.Cancel` predicate shape, with a generation bump (the Store supports this at `SG:42`) so a late BUILD or birth cannot create a duplicate team.
- **DDR:** whether a proven no-team state releases cap1, who triggers it, and what happens to production already spent.

**Regression risk.** MEDIUM (touches the cap authority). The off-map enumeration question (whether `GetUnits():Members()` includes off-map Spies) is UNKNOWN and must be settled before any absence proof.

### B. Cancellation proven only by ProductionPanel interception — MEDIUM–HIGH / FIX_NOW

E1-02 (CONFIRMED MEDIUM/FIX_NOW) and E2-01 (CONFIRMED HIGH/FBDF). The impact is permanent per save and silent within the session, and it is reachable through stock UI rather than a fault; that supports HIGH. The likelihood depends on player habits; that supports MEDIUM. It is FIX_NOW because it is a correctness defect in the current slice. It does not block the pending B204 test, which does not exercise cancellation.

**Facts [owner-verified]**
- Interception exists only in the replaced ProductionPanel (`Mod/SpecializationP0.modinfo:357-362`): the `RemoveQueueItem` override (`CPO:82-86`) and the REPLACE_AT observer (`CPO:91-97`). `api.CancelQueue` (`TUI:60-67`) is the only producer of CANCEL.
- The base `ProductionManager` is a separate LuaContext (`<CivVI>/.../Base/Assets/UI/InGame.xml:56`). It includes its own `ProductionHelper` (`ProductionManager.lua:9`) and calls `RemoveQueueItem` from the trash button and right-click (`:210`, `:291`). That issues `BUILD` / `VALUE_REMOVE_AT` directly (`ProductionHelper.lua:196-202`).
- The Manager tab is shown in the normal layout (another agent cited `Panels/ProductionPanel.lua:2552-2555,2641-2644`). No reference to ProductionManager exists in Mod, tests or Architecture.
- Gameplay sees the removal (CityProductionQueueChanged marks dirty, ET:135-138) but the queued-and-empty branch only removes the marker and keeps the reservation, by design (`ET:122-126`, "Empty queue is not proof of cancellation"). On load, `ET:123` raises `TRAINING_LOADED_QUEUE_MISSING` → HELD.
- There is no in-session release: the item is offered only when `T.Available` (`TUI:41-43`), and `CancelQueue` arms only if an Expedition TRAIN entry is still at the index (`TUI:60-66`).
- The armed CANCEL polls at most 12 times, then clears without sending (`TUI:81-82,108-109`).
- `test_expedition_training.py:62-63` pins "an empty queue keeps TRAINING". No test models a non-intercepted removal.

**Inference.** High confidence for the Manager path; medium for the placement path (it depends on how many publish events fire while placement mode is open). The root cause is the B202 rule "an empty queue alone does not release capacity", combined with a single source of cancellation proof in one context and no bounded Gameplay-side way to resolve "queued, now empty, no receipts".

**Counterevidence.** ProductionPanel's own removal and replacement are captured. HD does not replace ProductionManager. Nothing is corrupted within the session. Holding on ambiguity is deliberate.

**Unknowns**
- Whether the Manager lists and removes the Expedition entry under HD with Chinese localization.
- Publish frequency during placement.
- Whether REPLACE_AT 0 from placement removes the item.

**Remediation boundary (advisory)**
1. *Technical:* also observe removal in ProductionManager, and give a placement-armed CANCEL a lifetime that covers placement. This is brittle and adds another single-winner replacement slot (F).
2. *Gameplay-side:* a bounded resolver for "queued earlier, now empty, no receipts, `#list==0`, source valid, after a full production-processing boundary". This changes the B202 evidence rule, so it is **DDR**. It also fixes L22 and L23.

Option 2 delays release by about one turn and must keep the late-event tests (`test_expedition_training.py:46-47,91-94`) passing.

**Regression risk.** LOW–MEDIUM.

### C. Cancelled completion treated as a terminal mismatch — LOW–MEDIUM (conditional) / FBDF

E1-03 (QUALIFIED LOW) and E2-09 (QUALIFIED MEDIUM/MONITOR).

**Facts**
- `ET:94-103` asserts `not cancelled` inside `run()` with default protect, so a cancelled event goes to `failure()` → HELD. A later CANCEL fails at `ET:70` before mutation.
- The native signature carries `canceled` (`TutorialUIRoot.lua:1919`), but the fixture always passes `false` (`test_expedition_training.py:33`).

**Inference.** A cancelled event cannot be completion evidence, so a terminal-mismatch classification is wrong. When it fires natively is UNKNOWN. If the engine raises `canceled=true` on queue removal, this rises to MEDIUM–HIGH, because the designed cancel path would then always end in HELD.

**Remediation.** Treat a cancelled completion as non-evidence: ignore it, or keep it as a hint that still requires the `T.Cancel` proof. Treating it as cancellation proof would be DDR (tied to B). It is cheap; bundle it with B.

### D. Mutation flag set before read-only validation — MEDIUM / FBDF

E1-10 (CONFIRMED LOW) and E2-05 (CONFIRMED MEDIUM).

**Facts**
- Gate NAME: `SG:372-373` runs `mutating=true;acceptName(pid,p)`. All asserts in `acceptName` (`:172-196`) precede its only writes (`:197-198`), and any error under `mutating` holds (`:546`). DISPATCH, TASK, STOP and END set the flag *after* their checks.
- NAME after END (L32): END leaves `{owner,phase='ENDED'}` (`:469`). A NAME arriving afterwards fails `BOUND_TEAM_REQUIRED` with the flag set, so HELD is persisted with no unit and no exit.
- Training: `ET:71` sets `mutation=true` before `queue(exact(s))`, so a reader throw, `TRAINING_MULTIPLE_QUEUE_ENTRIES` or `TRAINING_QUEUE_STILL_PRESENT` holds.
- Inconsistent terminality: the same name collision is non-terminal when the UI observer finds it (STOPPED, retried on reload; `ExpeditionTrainingName.lua:77,103-108`) and terminal when the Gate finds it (`SG:183,189,193`).

**Remediation.** Set the flag immediately before the first write (Gate `:197`; Training before marker, `T.Cancel` or `T.Evidence`), and return non-holding errors for stale or out-of-phase requests. Whether a genuine name contradiction should hold is **DDR**.

**Regression risk.** LOW (adapt `test_expedition_training_name_events.py:86-87`).

### E. Durable commit followed by a one-shot UI follow-up with no recovery owner — MEDIUM / FBDF

E1-11 (CONFIRMED LOW/MONITOR), E2-04 (CONFIRMED MEDIUM/FBDF), E2-11.

**Facts**
- **RESERVE.** The reservation is persisted (`ET:67`; `SG:499-500`) before the UI issues BUILD from its publish handler (`TUI:85-97`). The UI clears with no compensating CANCEL on age >12 (`TUI:81-82`) **[owner-verified]**, on a BUILD error (`:96-97`), and when QUEUE is unconfirmed (`:108-109`). Training also drops busy requests with no reply (`ET:57`).
- **CANCEL.** The native removal runs first (`CPO:84-85`). The stage is set to ACK before an unprotected `transmit` (`TUI:105-106`).
- **DISPATCH.**
  - TRAVELLING and `dueTurn` are saved before any native call (`SG:383-387`); the permit is transient (not in `fields`, `:9`; attached only to the reply, `:473`).
  - Travel is submitted only from the window's `reply()` while `pending` is set (`ExpeditionSpyWindow.lua:324-342`). A 10 s timeout or a DIAGNOSTIC close clears `pending` (`:436-442,580,588`).
  - A pre-submit `CanStartOperation` denial (`ExpeditionSpyRead.lua:376`) becomes STOP, which always holds.
- **Compensations that exist:** lost CONFIRM self-heals (`ET:119-121`); deselection or denial routes to CANCEL (`TUI:89-93`).

**Inference.** There are two protocols for "durable intent → one-shot native action". The mirror-driven activity bridge re-observes on load. The reply-handler-driven one has no recovery owner.

**Remediation.**
- Route every UI failure after a reservation through the CANCEL stage, which already re-proves an empty queue.
- Make follow-ups mirror-driven: a persisted "requested, not yet submitted" state, a UI actor that submits exactly once, and re-observation on load.
- Use per-token replies with an explicit BUSY reply (see AF-18).

Whether a provably-not-submitted travel reverts to CREATED is **DDR**.

### F. Gameplay transitions depend on a UI-context reader in a single-winner replaced context — MEDIUM / FBDF (current impact LOW)

E1-06, E2-03 (multiplayer sub-claim REFUTED), E2-10. Cross-cutting: [AF-03](Architecture_Findings.md).

**Facts**
- `ET:22-29` synchronously calls `ExposedMembers.SPC_ExpeditionQueueRead` ("GetAt is a UI surface") **[owner-verified]**, defined in `TUI:15-27`.
- `TUI` is constructed inside `CPO:74-77`, after unprotected construction of the other adapters (`:48-54`). The `GetDataHelper` override (`:13-19`) guards `trainingSelection==nil`, so an earlier adapter construction error silently removes both the Expedition item and the reader.
- A missing reader gives 12 publish events and then HELD (`ET:109-110,142-148`). A throwing reader holds immediately.
- NAME trusts the UI-attested `NameOffmapChecked` (`SG:174`) but re-verifies the visible name, pool, position, source and `#list` (`:175-195`).
- ProductionPanel replacement is at LoadOrder 150100 and hosts five adapters. UnitPanel, EspionageChooser and EspionagePopup are replaced at 2000006. HD is included by name but not declared.

**Remediation.** Classify reader absence or a throw as transient (stay pending, bound the wait by turns, show the status); pcall-isolate adapter construction; document the cross-context contract (absent ≠ fail; turn and owner stamps); declare or guard the HD dependency.

**Regression risk.** LOW for the reclassification.

### G. Split TRAINING load recovery; a complete receipt pair is HELD on load — LOW / MONITOR

E1-09, E2-07 (the "which module runs first" sub-claim REFUTED: the Gate loads at Start, `SG:476`, before Training starts, `Gameplay.lua:910-912`).

**Facts**
- `SG:33-35` converts TRAINING with *any* receipt to HELD, in memory only.
- Training's receipt-recovery branches with `recovery=true` (`ET:115,118`) are therefore unreachable on load; they are reached only through the in-session waiting-reader path.
- B202 local `:12` says only an *incomplete* pair remains HELD; the code also holds a *complete* pair. The record and the code disagree.

**Remediation.** Give phase recovery a single owner and re-run the in-session predicates on load before holding. Add a complete-pair load test.

### H. HELD overloads meanings and loses the prior phase — MEDIUM / FBDF (before reattachment)

E1-04 (CONFIRMED).

**Facts**
- `hold()` overwrites the phase (`SG:129-139`), and the Store requires no fields for HELD (`ExpeditionSpyStore.lua:49`).
- `observe()`, `data.Turn` and the CityTransfered handler skip HELD (`SG:214,567,581`), so a held travelling team's ID replacement and arrival are no longer followed.
- HELD is entered for any source-reference change (`SG:96-100`) and for any target or capital change (`:101-119`). Design says target loss means cancel without reward and keep the unit (`P0_N_Expedition.md:111`), and archive-city Owner change means abort, keep the unit and allow free reattachment (`:117`).
- `errorStep` is the Gate-local `step` (`SG:7,134`), so holds that start in Training record a stale step.
- The same capture yields either `TRAINING_SOURCE_CHANGED` or `TRAINING_SOURCE_LOST` depending on listener order (`ET:153` vs `:154-157`).

**Remediation.** Explicit non-terminal states (e.g. AWAITING_REATTACHMENT, TASK_CANCELLED) with Store invariants; a structured hold kind plus the phase it came from; a CPS-confirmed exit kept separate from "reference unreadable"; continuity tracking for held travelling units.

**Regression risk.** MEDIUM.

### I. Identity across native travel rests on citizen-name equality plus type uniqueness — MEDIUM long-term / FBDF; LOW in current scope

E1-07 (QUALIFIED LOW/MONITOR), E2-08 (QUALIFIED MEDIUM/FBDF), E2-12.

**Facts**
- `namePool` asserts `CIVILIZATION_SPC_TEST` (`SG:155-170`).
- `acceptName` requires pool membership or a unique localization, `#list==1`, and no same-named owned unit (`:171-199`).
- The travel candidate is selected by type with `#all==1` (`:226-231`).
- The test pool is copied from Scotland's citizen names (`Data/Identity.sql:21-24`).
- Unit IDs change on travel (B184 native review, another agent's record).
- `NativeName` scans the full CivilizationCitizenNames table on every wake-up (`ExpeditionSpyRead.lua:308-315`).

**Counterevidence.** The test-civilization restriction is approved scope (`P0_N_Expedition.md:21`). Name continuity worked natively for the current fixture (B189, another agent's record).

**Remediation.** Put identity behind a single resolver, log the observed name representation, investigate native carriers that survive travel, and cache the pool. The identity carrier for broader scope is **DDR**.

### J. Owner-scoped opaque source reference — LOW / FBDF

E1-08, E1-12, E1 verifier-missed.

**Facts**
- `sourceRef` = owner/ID/x/y/raw token (`NetworkInput.lua:7-10`), compared as a whole (`SG:96-100`). `exact()` also asserts the original owner (`ET:9-13`), so Training's own marker withdrawal after a transfer (`ET:41,107`) always fails, contradicting the comment at `ET:39-40`.
- Only the CPS exit callback can remove the marker after capture, and only while the phase is TRAINING (`ET:154-157`). If Training's CityTransfered listener (`ET:153`) runs first, the record is already HELD and the marker stays in the captor's city. The marker is the unit's only prerequisite (`Data/ExpeditionSpyGate.sql`), so the captor could train the unit.
- The exit callback matches by owner and cityID only (`ET:155-156`), whereas every other check uses the full reference.
- Tokenless recaptured cities can never be sources (SD-10 in [Architecture_Findings.md](Architecture_Findings.md) context; `ET:34` compares the raw token property).

**Remediation.** Store a structured, owner-independent source handle (token or E2 identity) next to the liveness reference. The exit callback should match the full identity and withdraw the marker whenever the record carries `trainingToken`, in any phase.

**Regression risk.** LOW.

### K. Closed, unversioned Store schema — LOW–MEDIUM / FBDF

E1-14 and E2 verifier-missed.

**Facts**
- Closed whitelists plus `schema==1` (`ExpeditionSpyStore.lua:5-12,30-43,89-92`).
- A rejection reads as `STORE_CORRUPT`, which on load blocks the store and refuses END on every load (`SG:24-27,331`).
- B202 added phases and fields under schema 1.
- The persisted field list is duplicated (`SG:9` vs `ExpeditionSpyStore.lua:7-11`).

**Remediation.** Bump the version on semantic additions; a distinct read-only `STORE_NEWER_SCHEMA`; a single field registry.

### L. Singleton runtime state, legacy gate, duplicate naming pipelines — LOW / DEFER (FBDF before multi-player)

E1-13, E2-14, E2-15.

**Facts**
- The Gate holds one `state` and loads only the first test player (`SG:7,21-23,476`). `T.Read(pid)` ignores `pid` (`:483-485`).
- The legacy `ExpeditionGate.lua` is packaged but not started; it would collide on `shared.ExpeditionGate` and its GameEvent.
- There are two naming pipelines (`ExpeditionSpyWindow.lua:278-323`; `ExpeditionTrainingName.lua:58-129`); per another agent's B203 review, their divergence was the B203 failure mechanism.
- A free P0 CREATE through `InitUnit` is still reachable.

## Concrete defects with failure scenarios

Native confirmation hints are suggestions only. No test is requested.

| ID | Defect | Scenario | Would confirm / refute |
|---|---|---|---|
| a1 (B) | Production Manager removal strands the reservation | Train → remove in the Manager tab → Gameplay removes the marker, keeps TRAINING, never re-offers; after reload, `TRAINING_LOADED_QUEUE_MISSING` → unit-less HELD | Confirm: P0 report shows TRAINING with an empty queue and no `[SPC][B202][TRAINING]` line; stop code after reload. Refute: the Manager does not list or remove the entry |
| a2 (B) | Placement confirmed after the CANCEL budget expires | Expedition at index 0; choose a district or wonder; CANCEL armed at click; confirm after more than 12 publish ticks → REPLACE_AT 0 → as a1. Variant: abandoning the placement leaves a sticky misleading `TRAINING_NATIVE_QUEUE_UNCONFIRMED` | Handshake error during placement, then TRAINING with an empty queue |
| a3 (B/E) | Intercepted CANCEL lost | Budget expiry, transmit throw or busy drop → as a1 | `TRAINING_HANDSHAKE_UNCONFIRMED` shown with TRAINING persisting |
| a4 (C) | Cancelled completion → HELD | Engine sends `canceled=true` for a removed TRAIN order | `TRAINING_COMPLETION_MISMATCH` right after a ProductionPanel removal |
| a5 (D) | NAME after END → unit-less HELD | Operator END races an observer NAME | Log: END→ENDED, then `step=NAME code=BOUND_TEAM_REQUIRED` |
| a6 (D) | CONFIRM/CANCEL flag before the queue read | Reader throws, or `n==1` on CANCEL | Stop code `TRAINING_QUEUE_UNKNOWN` / `TRAINING_QUEUE_STILL_PRESENT` |
| a7 (E) | Reserve handshake lost before BUILD (also a save in that window, L23) | Next turn `TRAINING_ORDER_OUTCOME_UNKNOWN` | Handshake error, then that stop code |
| a8 (E) | DISPATCH reply lost or pre-submit denial | TRAVELLING saved with the unit at home → `NATIVE_IDENTITY_UNCONFIRMED` after dueTurn+1, or STOP → HELD | DISPATCH line without a "submitted" line |
| a9 (J) | Marker leak after source capture | Training's listener runs before CPS → `TRAINING_SOURCE_CHANGED`, marker stays in the captor's city | `SOURCE_CHANGED` (leak possible) vs `SOURCE_LOST` (no leak); marker presence |
| a10 (J) | Exit callback matches owner and cityID only | City-ID reuse for the same player causes a false `TRAINING_SOURCE_LOST` | Refuted if city IDs are never reused |
| a11 (G) | Complete receipt pair held on load | Save between the second receipt and Finish | P0 report after such a load |
| a12 | Hold reasons never reach ordinary feedback | Observer converts an invalid view to IDLE and clears the error (`ExpeditionTrainingName.lua:30,62-64,95-98`); `UnavailableText` explains only NAMING (`ExpeditionSpyUI.lua:49-65`); the test's NAMING error reply cannot be produced by the real handler | If B204's test ends in a Gate HOLD, the tooltip shows a generic "unavailable" while the P0 report shows the error |
| a13 | Evidence events dropped while busy | `d.Birth`/`d.Complete` return silently if `busy` (`ET:47,88,97`); a re-entrant receipt leaves a half pair → `TRAINING_RECEIPT_INCOMPLETE` | That stop code with both native events in the log |
| a14 | Arrival detected only by turn polling | dueTurn+1 deadline (`SG:242`); the replaced unit shows no actions until observed | LOW; arrival passed natively within scope (another agent's record) |

## Test-evidence observations specific to Expedition

These are cross-referenced to AF-09, AF-20 and AF-22.

- `test_expedition_spy_name` (39 Gameplay NAME-authority negatives), `..._activity_diagnostic` and `..._activity_failure` were last executed at B194. B202–B204 changed name confirmation without re-running them.
- The Spy Gate `LoadScreenClose` handler (`SG:576-578`) is never exercised by any fixture.
- Single-slot event mocks let `ExpeditionTrainingName.lua:152` overwrite Training's `GameCoreEventPublishComplete`/`LoadScreenClose` handlers in `naming()` fixtures, so a Training load-recovery regression would pass the B204 wake-up tests.
- UI-only off-map Spy APIs leak into the Gameplay Gate's view in ui/window fixtures (`test_expedition_spy_gate.py:84-87` vs `:54-55`).
- The training UI cache-invalidation path (`TUI:30-33`) is unexercised, because mocks never bump `SPC_RuntimeUIRevision`.
- No test models: a removal not intercepted by ProductionPanel, `canceled=true`, a complete pair at load, an exit from a unit-less HELD, or NAME after END.

## Strengths worth preserving

- Write-ahead reservation and intent before every native action (RESERVE, CREATE, END, DISPATCH).
- Joint-evidence binding with no guessing: both event orders work, duplicates are idempotent, and unchanged saves skip writes.
- A source liveness reference with owner, cityID, x, y and token, which defeats city-ID reuse. A generation-scoped `teamKey` defeats UnitID reuse.
- Capacity derived from phase plus a fresh unit list, not a counter.
- Bounded deferred work and no replay of uncertain sends. Only the reserved city is marked dirty.
- Existing compensations (deselect or deny → CANCEL; lost CONFIRM self-heals).
- B204's event-first observer: exact-team match (owner, unitID, teamKey, trainingToken), re-checked after re-entrant notifications, never resends. Its result explicitly declines to claim a native diagnosis.
- Travel permits are consumed before the native request and never replayed.
- Source-city exit uses CPS's matched native ownership event, not getter absence.

## DESIGN_DECISION_REQUIRED (not decided here)

1. Release policy for a HELD record with no surviving unit (source lost before birth, unknown handshake outcome, stranded queue, missing reader): may it release cap1, under what fresh proof, triggered by whom, and what happens to production already spent? Design counts only surviving teams (`P0_N_Expedition.md:94`), keeps capacity on ambiguity (`:58`), and asks for a loss/refund decision (`:99`). The Owner-change rules (`:117`) cover only existing teams, not training in progress.
2. Cancellation evidence: may "queued earlier, now empty, no receipts, past a defined bound" count as cancellation (replacing the B202 rule)? May a native `canceled` completion count? Capturing every UI context instead is purely technical.
3. HELD with a surviving unit: is END (destroying a production-paid unit) acceptable as the only resolution, or should there be a non-destructive re-verify or rebind (this interacts with reattachment)?
4. Pre-binding naming failures (collision, default name, stale sample, name changed): hold, or stay retryable?
5. Travel that provably was never submitted: revert to CREATED, or hold?
6. The identity carrier for Expedition beyond `CIVILIZATION_SPC_TEST`.

## Unreviewed areas and UNKNOWNs

- **Not re-read in full:** `UI/ExpeditionSpyActivity.lua` (the SLEEP/RELEASE protocol; the critic flagged it as repeating the mutate-before-validate pattern), `ExpeditionSpyUnitPanel`/`Chooser`/`Popup` internals, `ExpeditionSpyWindow.lua` outside the cited ranges, `ExpeditionSpyStore.lua:60-85`, and HD's `EspionageSupport.lua`.
- **Purchase path:** `PurchaseYield` defaults to NULL and the mod does not set it, so gold purchase looks unavailable. Faith-purchase enablement for `CLASS_LANDCIVILIAN` via modifiers was not checked. A purchase would produce a birth without a completion.
- **Native questions:**
  - meaning of `canceled`
  - listener dispatch order
  - publish frequency during placement
  - autosave timing relative to receipt events
  - ExposedMembers lifetime across in-app loads
  - whether off-map Spies appear in `GetUnits():Members()`
  - marker survival on capture, and AI training of the unit
  - Spy-class unit fate on home-city capture
  - native name uniqueness and the `GetName` representation
  - whether the Production Manager is visible under HD with Chinese localization
