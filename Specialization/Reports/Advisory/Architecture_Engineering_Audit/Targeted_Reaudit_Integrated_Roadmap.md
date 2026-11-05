# Targeted re-audit — integrated architecture-convergence candidate (v3.1-review + HD decoupling)

Advisory / Non-authoritative / No design decision implied
Status: Stable
Maintainer: Advisor (Claude Code); attribution only, not session authorization.
Scope: Owner-requested independent targeted pre-implementation re-review of the integrated roadmap, the Engine Reference first tranche, Codex's A01–A20 dispositions and their revised NET / D1 / wake / P3 / PU / FS products. Read-only. Excludes code/test/formal edits, test execution, probes, game launches and any re-audit of unchanged accepted professions.
Basis: develop `954dc67aca007082a5a164becdbafbacbad1403a` (D0058 / A0183 / S0866), tracked tree clean; one untracked input `Specialization/Reports/Technical/Engine_Reference.md` (SHA256 `a1d0df8c…d933`). Candidate and original-audit hashes match the review manifest (16/16). External sources are cited by label only: **ER-20261104** (local engine-reference tranche: Owner originals, official macOS extracts OFF-*, pinned community files SUK/HEM/CRU/GCO); **ENV-20261104** (completed environment backup: HD Workshop 2465378070 v2.2, its companions, Leugi Workshop 2479197624); **GAME-CACHE** (the game-built `DebugGameplay.sqlite` of the original 72-Mod profile, last written 2026-11-01, opened read-only/immutable). Labels: STATIC_CONFIRMED (code/data read), INFERENCE, NEEDS_NATIVE. No LOCAL_SIMULATION or USER_GAME_TEST result was produced.

## How to read

Section I gives the verdict. Section II sorts what must close, and before which authorization, into the four timing classes the Owner asked for. Section III gives the per-finding results: it reuses A01–A20 for residuals and continues with A21–A28 for new items. Sections IV–VI assess the HD decoupling, the Engine Reference and the document structure. Section VII records what holds. Section VIII is the read ledger and its limits; IX is the handoff.

Verdicts use the re-audit package vocabulary: PLAN_ACCEPTED, PLAN_GAP, EVIDENCE_OPEN, plus CANDIDATE_CLAIM_WRONG where a stated fact does not match the source.

## I. Verdict

**CONDITIONALLY READY, split by scope.**

- **First formal sync, the durable Pre-U5 first slices and the original-HD U5 baseline:** ready once five plan corrections close (C1–C5 in Section II). None needs a new gameplay vote. Each is a plan or wording change Primary can make and the Advisor can re-check quickly.
- **The HD-decoupling slices** (official providers in O1, data/UI assembly in O5/O6, and any HD-free game launch): **not yet ready for their own implementation authorization.** The static seam inventory is good. However, the assembly, test-basis, tier-framing, UI and exit closure have concrete gaps (A21–A26). As written, these would cause rework or silent disabling. They do not block the scope above, because U5 stays the HD baseline. They must close before the first HD-adapted slice is authorized.

No Critical issue. The Owner decisions (OD-1–4, ODP-01=B, ODP-02=A) are integrated correctly. The NET / D1 / wake / P3 products are concrete and match the code at the cited lines. The cross-profession exit matrix holds. The remaining risk sits in two places:

- Two Pre-U5 slices (PU05, PU09) whose wording would either hold a fixable defect behind a native gate or ship protection without its root cause.
- The HD-decoupling plan, which is sound in direction but under-specified where SQL, UI and tests meet the engine.

## II. What must close, and when

| Class | ID | What closes it | Owner input? |
|---|---|---|---|
| **1. Before implementation authorization** (formal sync / Pre-U5 / U5) | C1 = A15 | Split PU05: (a) re-key the unresolved-grant receipt per source/order now, LOCAL only; (b) multi-completion attribution waits on the existing S7d6 capture. Name the admission event and arguments. State the evidence standard that closes (b). | Only if (b)'s standard relaxes the accepted D5/S7d6 reading |
| | C2 = A16 | Replace PU09's generic root gate with the enumerated throw sites and their owners. Make the sticky `completionError` fix a PU09 dependency or unconditional for Claim candidates. | No |
| | C3 = A01 | Add two sentences to the FS03/04 successor text: (i) a real negative fact during unfinished cold initialization; (ii) the interim state of NET05. | No |
| | C4 = A27 | Publish (or distill into formal text) the Stable candidate set and both audits before the first formal sync. Name one current plan table. Apply the §10.1 wording fix. | Publication is Primary's normal checkpoint |
| | C5 = A22 (part) / A23 (part) | Two cheap roadmap statements. First, post-migration HD regression runs on the U5 profile, and the "minimal HD" profile is a separate certification. Second, move O5's data-selection seam (O5a) ahead of O1's first official provider. | No |
| **2. Before / within the corresponding slice** | A21 | HD-free test basis: pinned per-profile game-built DBs; a LoadOrder-faithful SQL gate. Needs one short user DB-capture launch, which can merge with the U5 session. | Approve the touchpoint |
| | A22 | Tier framing: re-point the source to `HD_BuildingTiers`. Adopt the chain-depth reading of Shared.md:140. Name the HD companion Mods in the environment matrix. | One-line confirmation of the reading |
| | A23 | O5a data-assembly contract: LoadOrder bands, override semantics, an SPC assembly marker, carriers generated after the final mapping, and DevelopmentInvestment.sql split. | No |
| | A24 | Static "every referenced ModifierType is defined" gate; choose the wrapper replacement. | No |
| | A25 | UI bases for HD-free (try-list or criteria). HD-only hook points such as `GetDataHelper`. Move TimedTurnProbe's ActionPanel replacement off the HD-free path. All before any HD-free launch with SPC. | No |
| | A26 | Exit/cleanup duties that must not depend on HD-derived catalogs; HD-free startup closure. | No |
| | A10, A17, A18, A19 residuals | Registration of mandatory exits independent of Start; ExpeditionTraining exit result; live "discount" SQL kept off the retirement list; absence-harness sizing. | No |
| **3. Final integration** | A14 residual | Name the environment-sensitive set that needs HD-free native acceptance. Do not plan a second full medium-scale campaign by default. Record third-party Mod auto-update as an unsupported mid-campaign environment change. | Approve the final-acceptance scope |
| **4. Non-blocking documentation** | A28 | Engine Reference precision items. Minor line/range fixes. Cross-context Flight wording. | No |

## III. Findings

### Inherited findings with residual gaps

**A15 — Crew completion (PU05). PLAN_GAP, inherits High. Class 1.**

- **What the plan gets right (PLAN_ACCEPTED):** city/order/source/reference scope, one-shot receipts, and no speculative InitUnit recovery. It keeps CALLING-before-create (`Mod/CrewProjects.lua:280-282`) and forbids snapshot/regrant machinery.
- **The coupling (STATIC_CONFIRMED).** Admission is already per city:
  - `Mod/CrewProjects.lua:369-370` subscribes `CityProjectCompleted`.
  - The handler uses the event's city id to select that city's own order (`:265,:270,:274`).
  - The coupling is only in the proof and the receipt. The receipt is one player Property keyed by ProjectType (`:84-90,:272`), and `assert(not prior or prior.stage=='BOUND')` (`:277`) lets one unresolved grant block every city's same-type completion.
- **The defect is fixable without new evidence (INFERENCE from `:273/:277/:278`).** Keep a per-type consumed high-water and move the unresolved-grant marker to its source/order. The existing strict `+1` proof still separates a new completion from a duplicate.
- **What is wrong with the plan wording.** PU05's stop rule ("无唯一proof停该切片") holds this fix behind the separate two-cities-same-turn (+2) attribution gate. That contradicts its own "不能wholeplayer…永久阻塞".
- **The open native question is already specified in the project:**
  - `Specialization/Status/Validation/Results/Refactor_S7d6_Crew_Proof_Gap.md:15,28` defines the D5 proof rule and the minimal capture.
  - `Specialization_B238_Native_Review.md:32` already shows single-completion Gameplay delivery with city attribution.
  - The plan cites neither, so its N0 is broader than needed.
- **Evidence-standard tension.** §10.1's "a theoretical failure is not evidence" conflicts with S7d6's untested late-duplicate concern unless the plan states that the Addendum's irreversible-operation carve-out applies. It also needs to say what evidence closes D5.
- **Minimal correction:**
  - Split PU05 into (a) and (b).
  - Admission = `Events.CityProjectCompleted(player, city, project)` bound to that city's admitted order serial and source token.
  - N0 for (b) = the S7d6 capture only: two same-tier cities in the same turn; firing on removal/cancel at 0 and >0 progress; duplicate/late delivery.
  - An unresolved CALLING keeps only its own slot, with an explicit error.
  - Ask the Owner only if (b)'s closure standard relaxes the accepted D5 reading.

**A16 — Claim/Dialogue UNKNOWN (PU09). PLAN_GAP, Medium. Class 1.**

- **What the plan gets right:** marker preservation is boundary protection, not a root fix; reliable negatives still remove access; Claim's true early completion stays legal.
- **The root gate is generic and misses the main Claim cause (STATIC_CONFIRMED):**
  - `Mod/CityProgressionStore.lua:2104-2108`: one `OnDistrictConstructed` whose plot has no resolvable city calls `HoldCompletion` on **all** workers.
  - `:823-826`: that sets a sticky `completionError` on every UNASSIGNED/ACTIVE schema≥2 root (the Claim candidates).
  - `:340`: `active()` then asserts on it forever, so `ClaimState` throws and the marker is removed (`Mod/ClaimProjects.lua:39-50`).
  - The owner of this is PU07, which is conditional ("只有证明…影响U5才纳入"). The Claim root cause therefore has no definite slice.
- **Normal cold load is not a Claim cause (INFERENCE):** the Store loads its index synchronously at Start (`:1641-1660`), and Claim audits wait for LoadScreenClose/Sync.
- **Dialogue does have a real initialization window.** `StartReady` (`Mod/RuntimeWork.lua:493-510`) can run before LoadScreenClose, while `known` depends on the six Governor properties (`Mod/EffectiveFacts.lua:112-121`, `Mod/Probe.lua:321-346`). B395 already records "saved ACTIVE early UNKNOWN → actual Load recovery".
- **Misdirected item:** "current-production availability" is not a marker-removal cause in either module.
- **Minimal correction:**
  - Map each throw site to its owner: `completionError` → PU07/A17 (made a PU09 prerequisite); Governor/pending → PU10/O1; isolation → Store restore validation; era → Dialogue.
  - Drop "current-production".
  - If N0 runs, add one observation: remove the marker under a queued project at 0 and >0 progress. Whether that cancels the project remains UNVERIFIED (`Specialization_B044_Crew_Projects.md:37`).

**A01 — Normal cold load (NET). PLAN_ACCEPTED in substance, PLAN_GAP in two sentences. Medium. Class 1 (wording before FS03/04 is frozen).**

- **What holds:** the NET02 model (no writes from incomplete inputs; idempotent reconciliation) and the per-family T0 table, which matches the code.
- **The two cases the contract cannot yet execute:**
  - **(i) A reliable negative fact arriving before cold initialization finishes.** Installed outputs are single aggregates: Commerce holds `observed(x.c)` total Gold (`Mod/Commerce.lua:281-289`), Culture a set count, and Standardization a per-target level. Cold sessions have no W. So "withdraw A without being masked by unknown sibling B" (NET04) cannot be computed without B, while NET02 forbids writing from B-less input. Practically rare (real negatives arrive in other players' turns, after initialization), but the text must say what to do.
  - **(ii) NET05 says neither K-only nor old-full is selected, but code must do something.** OD-1's no-write rule already defines the interim state: the installed output stays, flagged unreconciled, with a visible error and no transactions.
- **Minimal correction (FS03/04):**
  - During unfinished initialization, a confirmed negative fact immediately revokes strict eligibility. Its passive withdrawal is registered and applied at the first consumable snapshot.
  - Sibling unreadiness beyond initialization is NET05: the installed output is kept by the no-write rule, flagged and reported, with no transaction, and any other outcome requires an Owner Packet.

**A10 — Mandatory exits under a failed or skipped owner. PLAN_GAP, Medium-Low. Class 2 (FS09 wording; PU08/O5).**

- **The mechanism (STATIC_CONFIRMED):**
  - Registration happens inside Start. `Mod/RuntimeComposition.lua:12-16` returns `SKIPPED_DEPENDENCY` before running a module.
  - Commerce builds an unguarded diagnostics trace (`Mod/Commerce.lua:21`) before its RegisterExit (`:560`). NetworkBridge indexes the diagnostics global before its pcall (`Mod/NetworkBridge.lua:41,43`).
  - All four cross-city families depend on NetworkBridge (`Mod/Gameplay.lua:942,985,991,1018`).
  - ExitConfirmed and recapture count only registered exits (`Mod/CityProgressionStore.lua:1268-1280,1334-1335`).
  - Result: fail-open — no gate, and no block on recapture.
- **My calibration of the sub-audit's "blocks O7":** Start failures are deterministic per build and database. Under OD-4 an owner that fails never installs carriers in that campaign, and O7's absence arm would itself show FAILED. Harm needs carriers already in the save plus a later Start failure. That happens through a mid-campaign environment change (for example a Workshop auto-update of HD or a companion) or a future state-dependent Start path.
- **Minimal correction:** FS09/O5 state that mandatory exact-family exit duties are registered independently of Start success (the LegacyCleanup pattern, `Mod/Gameplay.lua:853-859`), or that a FAILED/SKIPPED carrier owner makes the exit unconfirmed. Add a LOCAL arm covering a failed/skipped owner plus an installed carrier plus capture.

**A14 — Native touchpoints. PLAN_ACCEPTED for the HD scope; PLAN_GAP for HD-free. Medium. Classes 2/3.**

- **The gap:** N0/U5/N2/Final contain no step that produces an HD-free database or first proves that SPC loads without HD. Both are needed before HD-free local checks mean anything (see A21).
- **Acceptance burden:**
  - §6 ("Both profiles validate … all currently supported professional mechanisms") and O8 ("campaigns for each environment") read as two full medium-scale campaigns.
  - The Owner's INTEGRATED §4.3 says to merge native observation by necessary question and not to retest all gameplay automatically.
- **Minimal correction:**
  - Add one non-conditional, short HD-free load smoke right after the O5a assembly seam (A23), which can be merged with the A21 DB capture.
  - Limit HD-free native acceptance to the environment-sensitive set: catalog/tier mapping, wrappers, queue/wonder sampling, UI bases, SQL assembly and startup.
  - Environment-independent rules (Store histories, receipts, formulas, delivery) rely on LOCAL tests on both databases plus the one HD medium-scale sample.

**A17 — Exit matrix. PLAN_ACCEPTED with one Low gap. Class 2.**

- **Verified (STATIC_CONFIRMED):** 45 literal RegisterExit sites, 44 unique names, 29 expected direct registrations and 11 LegacyCleanup groups.
- **No handler and no Store path selects cleanup by the city's current profession:** `Mod/CityProgressionStore.lua:1185-1202,1268-1280`, and each handler passes its full family list.
- **No logging-only gate among the 29.**
- **Gap — ExpeditionTraining exit always reports success.** `Mod/ExpeditionTraining.lua:299-304` wraps RemoveOwned in `run()`, whose `pcall` (`:123-129`) swallows any error. The exit therefore always returns normally ("finished"), even if removal failed. When the module is busy it also returns without inspecting the marker.
- **Fix:** return the removal result explicitly.
- **Doc:** `Mod/LegacyCleanup.lua` has 136 lines; the DRAFT cites 1–148.

**A18 — Production/diagnostic separation. PLAN_ACCEPTED (P3 complete in substance) plus one Medium caution. Class 2.**

- **The "retired discount" SQL is a live input (STATIC_CONFIRMED):**
  - `Mod/Data/StandardizationDiscount.sql:2-8` builds `SPC_B054_Targets` from HD tables.
  - `Mod/Data/StandardizationEffects.sql:3-6` builds every BUILDING Standardization target from it.
  - `Mod/Data/EngineeringStudy.sql:10-13` builds every level from those targets.
- **Consequence:** retiring that file by name (O7) or decoupling it without re-sourcing (O1) breaks live Standardization and Engineering Study. The legacy withdrawal list (`Mod/StandardizationDiscount.lua:7-12`) is derived from the same table.
- **Precision items (sub-audit, spot-checked):**
  - `Store:2061` asserts `shared.BindingProbe` on every fresh admission (P3-03).
  - Four UI files include `DiagnosticLog` unguarded.
  - 23 UI files include `Probe`, which binds Counters.

**A19 — Flight/GC. PLAN_ACCEPTED. Class 2.**

- **Preserved:** GC policy (one NETWORK_INFLIGHT continuation, none for ROUTES_PENDING), the negative-heap latch and the single fullcollect. Extraction happens early.
- **Precision:** the in-flight state is written from the UI context. NetworkSender calls `SPCPerformance.Flight` unguarded (`Mod/NetworkSender.lua:8,19,29,35,71,78`) into the Gameplay-created object (`Mod/Gameplay.lua:24`). P3-16 covers this duty but does not name the cross-context path.
- **Harness work is real and unsized.** `DevelopmentTests/refactor_harness.py:48-66` loads straight from disk, and the fixtures pre-inject diagnostics globals. The absence arm must not pre-define them, must test include() in both the throw and silent-nil modes, and must include a UI context.

### New findings

**A21 — No HD-free test basis; SQL tests cannot see LoadOrder. PLAN_GAP, High for the HD slices. Class 2 (before the first HD-adapted slice).**

- **How the tests get their data (STATIC_CONFIRMED):**
  - SQL/DB tests read the external game-built cache DB (`DevelopmentTests/project_paths.py:5-15`; 21 test files reference it).
  - That DB reflects whatever profile last launched — currently 原版, with HD and SPC.
  - The tests execute SPC SQL against that *final* database, where all content already exists.
- **They therefore cannot detect cross-Mod LoadOrder effects.** In GAME-CACHE, `SPC_Lv2HousingTiers` (LoadOrder 1200, before HD content at 11000+) has only 21 official rows. Local tests treat its list as complete. The table has no production reader, so this is not a live defect — but it is native proof of the blind spot.
- **What the plan says:** the DRAFT requires "an actual official-definition test basis" but schedules no step that produces one. Without it, "HD-free local checks start with the first adapted slice" has no data.
- **Minimal correction:**
  - One user-run DB-capture launch per new profile: official + Leugi, with and without SPC. It needs no gameplay and can be merged with the U5 session.
  - Keep pinned, hashed copies as external read-only fixtures, and parameterize tests by profile so a later relaunch cannot silently switch environment.
  - Gate SQL by inspecting game-built DBs, not by replaying SPC SQL on a final DB.
- **The same capture also settles three NEEDS_NATIVE questions:** per-file SQL error continuation, undefined-ModifierType handling, and the official prerequisite graph.

**A22 — Tier source mis-framed; profile closure missing. CANDIDATE_CLAIM_WRONG + PLAN_GAP, High for the HD slices. Class 1 (comparability statement) / Class 2 (rest).**

- **What the candidate says.** ER05/§6 locate the "Bank3 / ResearchLab4 / Workshop2" delta in `Mod/Data/Lv2Housing.sql`, and the DRAFT warns "do not guess a logical building tier from prerequisite depth".
- **What the source shows (STATIC_CONFIRMED):**
  - `SPC_Lv2HousingTiers` has no production reader (git grep).
  - Production tiers come from `GameInfo.HD_BuildingTiers` via `Mod/OrdinaryBuildingCatalog.lua:203-207`, then D, Lv2 housing (`Mod/Lv2Housing.lua:24-40`), Standardization and Development targets.
  - HD computes tiers as prerequisite-chain depth (ENV-20261104 HD `UpdateDataBase/HD_BuildingTiers.sql:11-22`).
- **Where the current numbers come from (GAME-CACHE):**
  - Bank 3 is HD's own: Market requires HD's `BUILDING_FAIR` (also `BUILDING_JNR_WAYSTATION`).
  - `HD_BuildingTiers` gives Workshop 2 because its prerequisites are `BUILDING_IZ_WATER_MILL`/`BUILDING_JNR_WIND_MILL`.
  - Research Lab 4 comes from four `BUILDING_JNR_*` prerequisites.
  - Those buildings come from HD District Expansion (Workshop 2701747165, which depends on HD) and the UC District Expansion series — companions enabled in 原版 that the environment matrix never names. HD Corporations (2616754773) is a further unnamed companion.
  - Official GS prerequisites form three-tier chains: Library→University→Research Lab, Workshop→Factory→Power Plant, Market→Bank→Stock Exchange (OFF-DEF `Buildings.xml:191-213`).
- **The accepted Design already covers this.** `Specialization/Design/Shared.md:140` says three- and four-tier complete chains (D6/D10) are both legitimate and are not normalized across Mod environments. `Shared_D0058.json` makes HD taxonomy adapter input, not semantic authority.
- **So the plan has two problems:**
  - The official mapping is largely determined: tier = the loaded environment's prerequisite-chain depth, owned by SPC with an HD-equivalent algorithm. Ordinary-building classification stays a separate semantic rule.
  - The "minimal HD" profile will legitimately differ from the U5 原版 numbers (INFERENCE: Workshop 1 / Research Lab 3 without the companions).
- **Minimal correction:**
  - Re-point ER05 to the real source.
  - Ask the Owner to confirm in one line that Shared.md:140 means per-environment chain depth. Keep any packet for genuinely non-chain cases only: multiple prerequisite alternatives, the Holy Site exception, unique replacements, Government Plaza, buildings without prerequisites, and Spec:527's "tier2 Sewer".
  - Name the companion Mods as members of the 原版 reference or as explicitly excluded.
  - Run post-migration HD regression on the U5 profile, and treat the minimal HD profile as a separate certification.

**A23 — Data-assembly contract and order (O5a before O1). PLAN_GAP, Medium-High. Class 1 (order) / Class 2 (contract).**

- **The order problem.** O1 is to ship official and HD providers "with necessary SQL inputs", but SQL selection is O5, which comes after O1 in the flowchart. HD JOIN statements cannot coexist unconditionally with an HD-free load (`Mod/Data/StandardizationDiscount.sql:5`, `Mod/Data/DevelopmentInvestment.sql:5`), so O1 would have to invent an interim selection that O5 then replaces.
- **Facts the contract must reflect (STATIC_CONFIRMED):**
  - SPC's modinfo has no criteria at all.
  - Negative `<ModInUse inverse="1">` is used by HD itself (ENV-20261104 HD `DL.modinfo:134,173,177`).
  - Per the sub-audit, it is natively honored on this macOS install (INFERENCE, strong): UC Campus content gated by an inverse criterion is absent from GAME-CACHE. CRU's community manifest-vocabulary notes also list `inverse` (Windows analysis). ER03's premise that a negative criterion would have to be invented is therefore false.
  - `DevelopmentInvestment.sql` puts the HD JOIN (`:3-7`) before the project/access definitions (`:15-20`) in the same file.
- **The contract must state:**
  1. LoadOrder bands for SPC base, HD mapping (after HD 16001 and its companions), and target/carrier generation, all ahead of the dependent SPC components.
  2. Override semantics: replace rows in an SPC-owned mapping, or select mutually exclusive components.
  3. An SPC-owned assembly marker that Lua reads. HD-table presence must not be the selector, and `Modding.IsModActive` is evidenced only in UI context.
  4. All carriers generated after the final mapping.
  5. HD-dependent statements never share a file with unconditional definitions.
- **Minimal correction:** split O5 into O5a (data-component selection) and O5b (Lua subscription/Start). Deliver O5a with or before O1's first official provider.

**A24 — Silent effect absence for HD-defined wrapper types. PLAN_GAP, Medium-High. Class 2.**

- **Why there is no load error (GAME-CACHE schema, STATIC_CONFIRMED).** `Modifiers` has no foreign key on `ModifierType` (only its RequirementSet columns), and `DynamicModifiers` keys to `Types`.
- **Which live carriers depend on HD wrappers:**
  - `MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION`: `Mod/Data/StandardizationEffects.sql:23-25`, `Mod/Data/EngineeringStudy.sql:17`.
  - `MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST`: `Mod/Data/EngineeringStudy.sql:23`.
  - `MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE`: `Mod/Data/ResearchCross.sql:13…58`.
- **Failure mechanism:** without HD these carrier rows still load, carrier buildings can be created, and SPC's readback reports them applied — but the effect type is undefined. That is the "silently disabling a mechanism" case §1 forbids, and it surfaces as no SQL or load error.
- **Minimal correction:**
  - Add a static gate on each game-built DB: every ModifierType referenced by a loaded Modifier has a DynamicModifiers row.
  - Choose the replacement as an engineering decision. Either SPC-named wrappers (the candidate's plan; Carrier/Modifier IDs do not embed the type name, so there is no ID churn), or `INSERT OR IGNORE` of the same three definitions after HD (HD-identical when present). The latter leaves HD names in core.

**A25 — HD-free UI bases and HD-only hook points. PLAN_GAP, High for any HD-free launch. Class 2 (before the first HD-free launch with SPC).**

- **The five HD-based replacements (STATIC_CONFIRMED).** All seven SPC ReplaceUIScript entries are unconditional; the two Espionage replacements use official bases. These five (`Mod/SpecializationP0.modinfo:30,48,50,51,459`) each include an HD base:
  - `DL_ProductionPanel` (`Mod/UI/CrewProjectOrder.lua:2`)
  - `DL_UnitPanel` (`Mod/UI/ExpeditionSpyUnitPanel.lua:2`)
  - `DL_CityPanel` (`Mod/UI/TimedProjectCityPanel.lua:2`)
  - `DL_CityPanelOverview`, with an XP2 fallback (`Mod/UI/InstitutionOverview.lua:3-5`)
  - `HD_ActionPanel` (`Mod/UI/TimedTurnProbe.lua:2`)
- **An HD-only hook.** `Mod/UI/CrewProjectOrder.lua:33-44` overrides `GetDataHelper`, which exists only in HD's `UI/Replacement/DL_ProductionPanel.lua:106`; the official panel uses other entry points. Without HD the override is never invoked, so the Render barrier (`SPCRestructuringUI.ObserveTraining`) and SPC project filtering go silently inactive.
- **Failure mechanism without HD:**
  - If `include()` of a missing file is silent — INFERENCE from HD's own try-list pattern on this install — the replaced contexts lose their native implementation.
  - TimedTurnProbe replaces ActionPanel, so the end-turn UI would break. The plan files it under O7 only.
- **Minimal correction:**
  - Each replacement resolves its base by explicit try-list (HD `DL_*` → official GS replacement → base) or is criteria-gated.
  - List HD-only hook symbols per UI file as adapter work.
  - Move the ActionPanel replacement off the HD-free path before the first HD-free launch.

**A26 — Exit and startup closure without HD. PLAN_GAP, Medium-High. Class 2.**

- **Exits jam (STATIC_CONFIRMED).** The StandardizationEffects exit calls `validate()` first (`Mod/StandardizationEffects.lua:363-370`), which builds a catalog that asserts HD tables. In an HD-free game every lost city's exit therefore throws, and that city's return/recapture is blocked.
- **Development has no exit at all.** It builds its catalog eagerly at Start and FAILS (sub-audit: `Mod/DevelopmentInvestment.lua:26`, `Mod/DevelopmentInvestmentCatalog.lua:5,13`), so its exit is never registered (see A10).
- **DistrictCompleteness degrades per city.** Its build is lazy, so every D read fails closed per city. That affects housing, Research infrastructure, ResearchApply, ResearchChair, CultureAesthetic and CultureMeaning.
- **The legacy list is HD-derived.** Legacy withdrawal lists come from the same HD-built table (A18).
- **Minimal correction:**
  - Exact-ID cleanup lists and exit validation must not depend on HD-derived catalogs. A confirmed-absent no-op must be reachable in both environments.
  - Record the per-module HD-free startup effect in §6's effect column.

**A27 — Provenance, single plan entry and normative wording. PLAN_GAP, Medium. Class 1 (before the first formal sync).**

- **Every new decision basis is a git-ignored local file:** the disposition set, the DRAFT and both audits.
- **The tracked v3-final entries are stale.** `External_Audit_Package.md` and the original candidate README still say the audit has not started.
- **This conflicts with the Workflow rule.** `Specialization/Workflow/README.md` (Advisory/Investigation checkpoints) says unpublished reports cannot be the sole durable basis for authoritative recovery.
- **Two plan tables must be read together:** DRAFT §4 and `PU_Option_B_Revised_Plan.md` §2–3.
- **§10.1 wording.** As worded, the normative paragraph could be read to forbid normal reconciliation. Normal initialization, availability recovery and post-load reconciliation (P06, OD-1) are the normal path, not "recovery machinery". The proposed Workflow sentence also restates the rule instead of referencing it.
- **Minimal correction:**
  - Publish or distill before the first formal sync.
  - Make "the candidate set leaves the default reading path" an exit criterion of that sync.
  - Name one current plan table.
  - Add the one-clause clarification to §10.1.

**A28 — Engine Reference precision. Low / doc. Class 4.**

1. **ER05 tier source** — see A22. This is the only substantive factual error.
2. **ER03 negative criteria** — premise false; see A23.
3. **ER02 wonder lead.** The official UI identifies a placed but unfinished wonder by plot: `Plot:GetWonderType()` plus `HasBuilding` for completion (OFF-13 `PlotToolTip.lua:669,782-783`; OFF-14 `MapSearchPanel.lua:583,637`). That is stronger than `GetConstructionsAtLocation`. Its Gameplay-context semantics remain NEEDS_NATIVE. Also add `Mod/UnitSiteProbe.lua:52` (reads `HD_UNCOMPLETED_WONDER`) to the inventory.
4. **ER02 transport.** Name the existing SPC reader-slot transport (`Mod/TimedProjectReaders.lua`, `ExposedMembers.SPC_EngineeringStudyRead`, `SPC_ExpeditionQueueRead`) so O4 does not build a second one.
5. **ER01 cancel flag.** OFF-03 `TutorialUIRoot.lua:1919` names the fifth `CityProductionCompleted` formal `canceled`. That is consistent with CRU `wasCancelled` and SUK `bCancelled` (shared community ancestry). It is an official naming lead, not behavior proof.
6. **ER01 Gameplay delivery.** ER01's "Gameplay delivery … not established" is broader than the project's existing native records (B238, B126/B129, B175–B177).
7. **ER06 PLOT_PROPERTY requirement.** `REQUIREMENT_PLOT_PROPERTY_MATCHES` is declared in the game DB `Types` as KIND_REQUIREMENT (no HD source found), and an official scenario uses it. Its live SPC use (`Mod/Data/CultureAesthetic.sql:25`) writes its own plot properties (`Mod/CultureAesthetic.lua:56,72,126,132`), so the HD-absence risk is low.
8. **CRU build parity.** CRU analysed Windows and Linux binaries of the same Steam build as this Mac install (CRU `README.md:17,34`). The semantics are therefore same-version but other-platform. Addresses are not portable, and the Aspyr binary is not analysed.

## IV. HD decoupling — what is proved, inferred or needs the engine

| Area | STATIC_CONFIRMED | INFERENCE | NEEDS_NATIVE |
|---|---|---|---|
| Manifest / third-party | No HD Dependency/Reference in SPC (`Mod/SpecializationP0.modinfo:845-850`). Leugi needs GS only and merely References Kublai/Vietnam. | — | — |
| SQL | Two HD-JOIN files. The live chain `SPC_B054_Targets → Standardization/EngineeringStudy`. Three HD wrapper types in live carriers. No FK on ModifierType. SPC LoadOrders vs HD phases. | Negative criteria honored on this build. | Per-file SQL error continuation; engine handling of undefined ModifierType; SPC criteria evaluation. |
| Lua startup | HD-table asserts. Development fails at Start. DistrictCompleteness fails per city. Std exit needs HD. GameInfo presence via pcall exists. | `Modding.IsModActive` UI-only. | Absent-table pcall behavior in Gameplay. |
| UI | Five unconditional replacements with HD bases. `GetDataHelper` is HD-only. Official GS replacements exist. | include(missing) is silent. | SPC panels on official bases. |
| Effects | Three wrappers = official Collection/Effect. 17 official types. PLOT_PROPERTY requirement is official. | SPC wrappers behave identically. | Per-primitive scope/rounding/stacking (already gated). |
| Inputs | Queue helper wraps official UI calls only. `HD_UNCOMPLETED_WONDER` is written by HD `Gameplay/Misc.lua:584-599`. Official `GetWonderType` UI usage. | `GetWonderType` covers placed-unfinished in Gameplay. | That Gameplay-context check. |
| Tiers | Production tier = HD chain depth over the loaded graph; 原版 values shaped by companions; Shared.md:140. | Minimal-HD tiers differ. | None (a static DB answers it). |

**Coordination with O1–O8, Pre-U5 and U5.** The integrated order is right in its big choices:

- U5 stays the original-HD baseline.
- There is no O9.
- PU01/03/06 are first users of the final interfaces.
- Document work rides with slices.

Three corrections are needed:

1. **O5a before O1** (A23).
2. **Tests and touchpoints for HD-free exist before the first adapted slice** (A21/A14).
3. **Small Pre-U5 duplicate-migration risks are named in the PU acceptance criteria** (sub-audit, INFERENCE):
   - PU08 must not re-derive legacy lists from HD tables.
   - PU02's UnitPanel work sits on HD's `DL_UnitPanel` and needs O6 re-validation on `UnitPanel_Expansion2`.
   - PU05 should read Crew snapshots through a provider seam so O4 swaps only the provider.

No hidden dependency forces HD-free work into Pre-U5.

## V. Engine Reference assessment

**The reference does its job.** It is question-based and short. It separates official consumers, community claims and unknowns. It keeps licenses and platform limits explicit (HEM MIT; CRU CC-BY-4.0 docs + MIT code; SUK and GCO without a license, so reference only). It claims no Mac or native PASS. **No community claim is used as an engine contract.**

**Its errors are conservative, with one exception.** Most of the items in A28 make the reference over-cautious: negative criteria, the scenario usage, Gameplay delivery, the canceled-flag lead, build parity. They do not over-claim. The exception is the tier-source mislocation (ER05). It would misframe an Owner packet, so it must be fixed before any tier discussion.

## VI. Document structure assessment

**No second authority.** Every candidate file is labelled non-authoritative. The Engine Reference sits in the Technical reference role. The evidence rule gets one proposed Architecture home. The FS delta targets existing formal files. The four-role model, the per-slice document column and the seven-line handoff template are lightweight, and no governance platform is introduced.

**Traceability inside the candidate is strong:** hashes, source IDs, re-checked line numbers and an explicit local manifest. Its weakness is durability (A27).

**Burden has not yet gone down — it has gone up for now.** The current candidate reading set is roughly 255 KB of new local material on top of the 109 KB tracked v3-final set, with the plan split across two tables and heavy abbreviation density. That is acceptable for a review phase. The reduction is promissory, however: it happens only if the first formal sync distills the decisions into the existing formal files and retires the candidate set from default reading. Making that an explicit sync exit criterion (A27) turns the promise into a gate.

## VII. What holds

- **OD-1–4 / ODP-01=B / ODP-02=A** integration: normal cold load is restoration; the K-only preset is withdrawn; there is no cross-version obligation; the lawful-exit reset holds; the turn-start drain is narrow.
- **NET:** the T0 per-family table matches `Mod/Commerce.lua:183-289`, `Mod/CultureNetwork.lua:137-244` and `Mod/StandardizationEffects.lua:165-244`. The startup boundary is correctly called non-proof (`Mod/RuntimeWork.lua:493-510`, `Mod/Gameplay.lua:1031`).
- **D1-01–12:** every branch has a destination, O3 owns it, and the T0/T1 historical-byte diff replaces the non-existent disable switch.
- **W01–W18:** each pending cause has a completion edge, an owner, a bound and an error end. `failedTurn`, same-value recovery and the R2 loss points are confirmed: `Mod/FactChanges.lua:182-203`, `Mod/RuntimeWork.lua:89-99`.
- **Decision closure, the R-source table and the CREDIT guard gap:** `Mod/CapitalInvestment.lua:140-143`.
- **A06:** derived-recovery modules are packaged only (`Mod/SpecializationP0.modinfo:153-155,612-613`; Store stamp at `Mod/CityProgressionStore.lua:318,1751-1754`).
- **Coverage:** all 32 attached debt rows are taken over. The FS line references were verified (Spec 16/24/26/281/283; Architecture 18/19/168/171/175; Status CURRENT:20).
- **The Addendum products are present:** the evidence-driven rule with a single home after P10, the cross-profession matrix, and separate project-root gates.
- **The doc measurements were verified:** Context Lock 1,302 files / 337,561 bytes; P0-H `AUTHORIZED` with `implementation_authorized:false`.

## VIII. Read ledger and limits

**Read in full:**
- The review entry and manifest.
- The four Owner originals (ADDENDUM, INTEGRATED, LIFECYCLE, DISPOSITION).
- The DRAFT.
- The Engine Reference.
- The re-audit package, the disposition README, A01–A20, NET, Wake, D1, Decision Closure, the PU/O plan, the FS delta and Owner Gate.
- The Evidence coverage §VI.

**Two bounded read-only sub-audits**, never more than two at once, each writing incremental notes. Every High claim was then re-verified at source by the Advisor.
- Crew / Claim / exits / P3 / GC: 445,296 tokens.
- HD seams: 496,386 tokens.

**Necessary expansions:**
- **Selected HD backup files:** tiers, wrappers, UI wrappers, `Misc.lua`, `DL.modinfo`, and the District Expansion manifest. Reason: candidate HD claims needed source checks.
- **The backup's official-modinfo metadata and a few installed official files** (sub-audit; e.g. a CivRoyale scenario XML). Reason: settling criteria syntax and requirement-type usage.
- **GAME-CACHE read-only queries:** schema FKs, tiers, prerequisites, Types and `SPC_Lv2HousingTiers` count. Reason: native-built data was the only way to see LoadOrder and FK effects.
- **Prior native records:** B238, B395, B044, S7d6. Reason: to bound the remaining native questions.
- No save, log, screenshot or other Mod file outside those listed was opened.

**Limits:**
- No runtime, test, probe or game.
- The older H1/H2/H3 originals remain unavailable; no conclusion here depends on them.
- Not re-checked: per-family ID lists against SQL; Capital/Development lifecycle beyond exits; full UI bodies; GreatWork DLC subsets.
- Sub-audit INFERENCE items are labelled as such.

## IX. Checkpoint / handoff

- **Completed scope.** This is a targeted re-audit of the integrated candidate's changed contracts and their affected closure, covering the five Owner focus areas. Stable file: this report only. Advisor writes to it are paused.
- **Re-check request.** After Primary revises PU05/PU09, the FS03/04 sentences and the O5a order, a short Advisor re-check of those rows is enough for the Pre-U5 scope. The HD supplement (A21–A26) gets its own short re-check before the first HD-adapted slice is authorized.

User decision:

1. Accept the CONDITIONALLY READY scope split.
2. Confirm in one line that Shared.md:140 means per-environment prerequisite-chain depth, or ask for a tier packet.
3. Approve one short HD-free DB-capture launch (no play; can merge with the U5 session) and one non-conditional HD-free load smoke after O5a.
4. Approve the targeted, not full, HD-free final-acceptance scope.

User testing: none now.

Primary next: add dispositions for A21–A28 and the A01/A10/A14–A19 residuals to the existing ledger. Close C1–C5. Revise the Engine Reference (ER01/02/03/05/06). Publish or distill the candidate set before the first formal sync. Then request the short re-check and the Owner's implementation authorization.
