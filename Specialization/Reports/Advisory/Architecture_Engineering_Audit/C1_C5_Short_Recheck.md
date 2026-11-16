# Short re-check — C1–C5 plan corrections and the Tier/HD supplement

Advisory / Non-authoritative. No implementation, Design decision or acceptance implied.

Status: Stable
Date: 2026-11-04
Author: Claude (Advisor)
Requested by: Primary, through `Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/External_Audit_Disposition/Claude_Targeted_Reaudit_Package.md`.
Basis: develop `954dc67`. Tracked source is unchanged since the targeted review; only `Specialization/Reports/Technical/Engine_Reference.md` is untracked.

**Candidate bytes:** every reviewed file matches the after-hashes in ER-20261104 `Owner_Disposition_20261104/Final_Handoff_Manifest.json`:

| File | SHA256 prefix |
|---|---|
| Integrated roadmap DRAFT | `611c43b8` |
| Finding disposition | `502afbf1` |
| FS delta | `64b3d9d8` |
| NET | `cdfb76a4` |
| P3 | `57c73913` |
| PU navigation | `ffd19d81` |
| Owner gate | `16a48a0b` |
| Package | `11a19dbd` |
| Disposition README | `d17687d8` |
| Engine Reference | `a96f2c77` |

**Prior review:** `Targeted_Reaudit_Integrated_Roadmap.md` (SHA256 `7f442259…605f0b`), unchanged.

**Scope:** only the changed rows and their necessary affected closure. This is not a new full audit, and unchanged accepted professions were not re-read.

**Read-only:** no code, tests, probes, game, deployment, formal edits or Git writes.

**Labels:** STATIC_CONFIRMED means read in source or the database; INFERENCE means a reasoned conclusion; NEEDS_NATIVE means it needs in-game evidence. Nothing in this report is a LOCAL or native PASS.

## Verdict

- **C1–C5 are all PLAN_CLOSED.**
- **No new major Pre blocker.** The narrow request may proceed: (1) durable publication, then (2) first formal sync, then (3) PU01 only.
- **One factual correction (N1) for the Tier record.** It belongs to the later O1/O5a provider gate. Carry its one-clause wording into the FS02/07 Tier record when the formal sync is drafted.
- **A21–A26 remain OPEN.** They are properly scheduled HD gates, not plan prerequisites for this request.

## C1–C5

| ID | Result | Reason (locator) | Remaining Pre blocker |
|---|---|---|---|
| **C1 / A15** | **PLAN_CLOSED** | See "C1 detail" below. | None. PU05b native evidence stays OPEN; only the attribution cutover waits. |
| **C2 / A16/A17** | **PLAN_CLOSED** | §4: PU07 is a definite Claim-entry prerequisite, "not conditional on reproducing broad U5 incidence". It carries the traced chain Store 2104–2108 → HoldCompletion 823–826 → `active` 340 → Claim marker. PU09 runs after PU07 with the enumerated root map: completionError→PU07, Governor/pending→PU10/O1, isolation→restore validation, era→Dialogue. "Current-production" is no longer named a root. The Dialogue pre-load window (B395) is kept separate. The optional N0 marker-removal observation is present. A17's ExpeditionTraining result is in PU08. | None. |
| **C3 / A01** | **PLAN_CLOSED** | FS delta §3 FS03/04, NET §1 (row 5), NET04, NET05 and NET §4. During unfinished initialization, a reliable negative fact immediately revokes strict eligibility/transactions and registers the passive withdrawal. An indivisible cold aggregate is reduced at the first complete consumable snapshot, with no invented per-source split. A missing getter is not a negative fact, and initialization cannot defer real change indefinitely. NET05 is no-write, unreconciled, a visible severe error and no transactions. It is explicitly not a payout, K-only or clear policy; an Owner packet is needed only for a real policy change. The LOCAL plan contains both arms. | None. |
| **C4 / A27** | **PLAN_CLOSED** (execution pending, correctly named) | See "C4 detail" below. | Execution (publication plus verified retrieval) before the first formal-sync transaction. This is already the plan's named prerequisite. |
| **C5 / A22/A23** | **PLAN_CLOSED** | §1 graph and §4: O5a precedes O1's first official provider, and O5b follows O2. U5 freezes the full "原版" profile, and post-migration HD regression uses that exact profile. Reduced HD is an optional, separate certification (§6 matrix). Companions are pinned by Workshop ID, Mod ID and version (§6). | None. |

**C1 detail (A15).**
- **What the plan says.** In §4, PU05a separates per-source/order unresolved receipts from the per-type consumed high-water. Admission is `Events.CityProjectCompleted(playerID,cityID,projectID)`, bound to that city's admitted order serial and source token. PU05a is "not held behind PU05b".
- **Feasible against the code (STATIC_CONFIRMED):**
  - The high-water `count` is already persisted at CALLING, before InitUnit (`Mod/CrewProjects.lua:281-285`).
  - Moving only the unresolved marker therefore keeps another city's strict `+1` (`:278`) valid.
  - The city's own CALLING order still fails its stage check (`:274-276`), so it keeps its own slot with an error.
  - Duplicates still return (`:273`).
  - The shared block removed is `:277`.
- **PU05b keeps S7d6** with a precise close condition: a completion-specific witness or a qualified native contract that separates the recorded indistinguishable histories, plus actual-owner replay/duplicate tests.
- B238 is limited to single-completion delivery.
- §10.1 keeps the irreversible-proof carve-out.

**C4 detail (A27).**
- **What the plan says:**
  - §4 "C4 durable preservation, before first formal sync": publish, push and read back, or use another approved durable archive. Local ignored files, the Raw archive and hashes are not a backup.
  - The formal-sync exit gate requires superseded candidates to leave the default reading path.
  - §2/§4 name the "sole current plan table", and `PU_Option_B_Revised_Plan.md` is now navigation only.
  - §10.1 adds the normal-path clause. Workflow RIC item 4 only links to it, and the S7d6 carve-out is kept.
- **Feasibility check:** no machine paths in the Advisory reports or the candidate set. Publication follows the existing Advisory checkpoint process.

## New substantive deltas (Tier/HD supplement only)

The Owner Tier correction is recorded consistently: DRAFT §1/§6/§8, ER05, the FS 2026-11-04 block and the Owner gate.

Three points verified:
- **HD's algorithm (STATIC_CONFIRMED).** In ENV-20261104 HD `UpdateDataBase/HD_BuildingTiers.sql:11-23`, district buildings start at 1 and city-center buildings at 0. Three any-prerequisite passes then set 2/3/4, which gives the longest path capped at 4. Finally, non-religious Holy Site T3 buildings are bumped to T4.
- **The reader rejects tiers above 4** (`Mod/OrdinaryBuildingCatalog.lua:222-225`, `TIER_UNSUPPORTED`).
- **Spec AQ-001 is future-only.** It sits under §11 "Future辅助系统 — OUT_OF_V0.1" (`Specialization/Design/Specialization_v0.1_Design_Spec.md:515,525-527`).

**Bounded queries on GAME-CACHE** (SHA256 `972069a7…0489`, the same bytes as Primary's Tier evidence; HD-populated "原版" profile):

| Query over the 162 HD tier rows (max 4) | Count | Buildings |
|---|---|---|
| Tier-4 row with a tier-4 prerequisite (cap) | 1 | Data Center |
| Holy Site bump | 2 | Hospitium, Garden (same-district prerequisites max T2) |
| Unequal same-district alternatives | 0 | — |
| Cross-district prerequisites, other than city center | 0 | — |
| Prerequisite outside the tier table | 1 | Water Mill (N1) |

**N1 — Factual correction: one exception candidate is missing.**
- **Class and location.** Later O1/O5a provider gate. DRAFT §6 Tier contract items 2–3 and the candidate table; ER05 candidate list.
- **Fact (STATIC_CONFIRMED).** `BUILDING_IZ_WATER_MILL` (Industrial Zone, HD T1) has one BuildingPrereq: `BUILDING_JNR_MILL_RACE`. That is a district-less HD dummy gate, which itself requires `BUILDING_JNR_DUMMY_IZ_RIVER`. `BUILDING_WORKSHOP`'s alternatives are Water Mill and Wind Mill.
- **Failure mechanism (INFERENCE).** Item 3 makes missing references and incomplete chains explicit errors. Item 2 makes incomplete alternatives an ambiguity. So a provider that reads this gate as a missing predecessor would:
  1. error Water Mill;
  2. leave Workshop's alternatives incomplete;
  3. fail the U5-profile Industrial Zone chain closed (Workshop and its successors).

  That would hit 工业 D, and through it Standardization targets.
- **Minimal fix:**
  - In item 2, classify district-less, InternalOnly or HD-dummy gate prerequisites as unlock conditions, like the Palace case. They are neither upgrade edges nor missing references.
  - Add a Water Mill row to the candidate table; its expected result is T1, as in HD.

**N2 — Precision: state the same-profile parity target.**
- **Class and location.** O1 provider acceptance / O8. §4 O8 "Same-profile HD before/after"; §6 contract item 4.
- **What the queries imply (INFERENCE).** In the U5 profile the contract should reproduce HD's values outside a small set:
  - Data Center (cap);
  - Hospitium and Garden (bump);
  - Mansion (city-center unlock) and Water Mill (N1), both of which must still compute T1.
- **Minimal fix.** Say that the U5-profile before/after expects equality with HD_BuildingTiers outside the enumerated rows. The enumerated rows take their values from the provider audit or the small Owner packet.
- **Why.** Otherwise a legitimate delta reads as a regression or is "fixed" by copying HD's bump. For example, Hospitium T4→T3 changes that building's D weight.

**N3 — Precision: one owner for the HD-free UI adapters, and a fixed slot for the smoke.**
- **Class and location.** Before HD-adapted authorization.
- **The double listing:**
  - The same base/callback work appears in the §6 O5a UI bullet, the §4 O5a row ("after base/hook/exit assembly ready") and the FS FS09/10 entry ("official UI callbacks … before SPC no-HD smoke").
  - It also appears in the §4 O6 row (bases, callback adapters, GetDataHelper counterpart).
  - A26 exit lists appear in PU08, O5a and the P3 Q row.
- **Consequence.** The user's single fixed smoke has no definite position in the sequence.
- **Minimal fix.** Name one owner. For example:
  - O5a covers base selection, moving ActionPanel off the no-HD path and HD-independent exits (PU08 owns the exact exit lists; O5a verifies). The smoke follows.
  - O6 covers the GetDataHelper callback counterpart and applied presentation, accepted in O8.

Nothing else material. Cosmetic churn is omitted.

## Authorization question

C1–C5 are plan-closed and there is no new major Pre blocker. **The narrow request may proceed to the Owner:**

1. privacy-reviewed durable publication with verified retrieval;
2. the first formal sync within the accepted FS scope, including N1's clause in the Tier record;
3. PU01 only, on the current HD provider. PU01 does not touch Tier derivation.

The O1 official provider, O5a and O6 HD adaptation keep their own evidence and authorization. A21–A26 stay OPEN, and N1–N3 belong to them.

## Read ledger and limits

**Read:**
- Package, full.
- DRAFT, all 399 lines.
- FS delta, NET, PU navigation and Owner gate, all in full.
- Disposition 1–59.
- P3 104–120.
- Engine Reference ER01–ER07.
- Owner-disposition supplement metadata.

**Source spot-checks:**
- `Mod/CrewProjects.lua:84-90,255-300`.
- `Mod/OrdinaryBuildingCatalog.lua:196-262`.
- DistrictCompleteness tier use.
- Spec 515–527.
- HD SQL 1–40.

**Database:** GAME-CACHE, opened read-only and immutable. Bounded queries via a scratch script outside the repository.

**Not re-read:** unchanged A01–A20 evidence; the Store/Claim chain lines (verified at the same HEAD in the targeted review); professions outside the changed rows.

**Limits:**
- GAME-CACHE is the HD-populated profile. N1/N2 counts describe the U5 profile only; the HD-free set needs the A21 database.
- No code or test execution.

## Handoff

- **User decision:** approve or withhold the narrow publication → formal sync → PU01 request when Primary submits it. No second planning vote.
- **User testing:** none now.
- **Primary next:**
  1. Mark C1–C5 plan-closed.
  2. Add N1 (one clause and one table row) to DRAFT §6 / ER05 and the FS02/07 Tier record.
  3. Record N2/N3 against A22/A25 in the existing ledger.
  4. Then submit the request.
- **Advisor:** this file is Stable and contains no machine paths. Writes are paused; further re-checks only on request.
