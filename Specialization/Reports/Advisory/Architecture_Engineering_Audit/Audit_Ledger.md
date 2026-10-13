# Architecture and Engineering Audit — Ledger

Advisory / Non-authoritative / No design decision implied
Status: Stable
Maintainer: Advisor session (Claude), attribution only — not session authorization
Scope: User-authorized comprehensive architecture/engineering audit (2026-10-12): modularity, state/persistence, performance/scalability, native integration, shared mechanisms/debt, testing/evidence, plus focused B202–B204 Expedition training/source-binding review. Exclusions: gameplay balance, wording, known native-test requirements, implementation, tests execution, deployment, Git writes, game launch.
Basis: repository `develop` at `2b75e129ad304bbebd2986b25595bfb178d0f803` (clean worktree, in sync with `origin/develop`); runtime build B204.231 / modinfo231 (source `84773a8`); Authority S0546 / A0161 / D0049; manifest `Specialization/Workflow/P0-N1.json`. External: configured Civ VI install and Workshop 289070 (HD) roots, read-only.

## Phase plan and independence rule

| Phase | Content | State |
|---|---|---|
| A | Independent investigation from Authority, Status CURRENT, Design, Architecture, Mod source, DevelopmentTests, relevant history and external sources. `Specialization/Reports/Audit/` (previous comprehensive audit) is deliberately NOT read in Phase A. | Complete — persisted in Architecture_Findings.md and Expedition_Review.md before any Phase B reading |
| B | Cross-review against `Specialization/Reports/Audit/P16b_P17_Final_Audit.md` after Phase A findings are persisted | Complete — Final_Review.md §2 |
| C | Final prioritized assessment in `Final_Review.md` | Complete — Final_Review.md §3–§8 |

## Phase A investigation slices

| Slice | Question | Output |
|---|---|---|
| A1 | Modularity, dependency direction, central dispatch, init order, cost of adding a specialization | Architecture_Findings.md |
| A2 | State/persistence: source of truth, identity, ownership, reservations, receipts, UNKNOWN, save/load, partial failure | Architecture_Findings.md |
| A3 | Performance/scalability: hot paths, scans, cache invalidation, event bursts, cross-context traffic, GC | Architecture_Findings.md |
| A4 | Native integration: events, UI/Gameplay boundary, ReplaceUIScript compatibility with base/HD, ordering | Architecture_Findings.md |
| A5 | Shared mechanisms and technical debt: probes/test data shipped, duplicated infra, legacy writers | Architecture_Findings.md |
| A6 | Testing/evidence: harness fidelity, negative cases, PASS-claim boundaries | Architecture_Findings.md |
| A7 | Design ↔ Architecture ↔ implementation consistency and future-specialization integration | Architecture_Findings.md |
| E1/E2 | B202–B204 Expedition training, reservation, production completion, unit identification, source binding, save/load, cancellation, ambiguous outcomes | Expedition_Review.md |

Each slice is followed by an adversarial verification pass; only verified or explicitly qualified findings are persisted.

## Basis change during audit

- While Phase A ran, `develop` advanced from `2b75e12` to `f843c0f` ("docs: make Advisor reading authorization topic-scoped"), changing only `Specialization/Reports/Advisory/AGENTS.md` and `Specialization/Workflow/Context_Lock.json`. `git diff --stat 2b75e12 f843c0f` shows no change under `Mod/`, `DevelopmentTests/`, Design, Architecture or Status, so all source evidence remains valid at `f843c0f`. That commit also writes into tracked guidance the topic-scoped reading rule the user gave this session.

## Phase A execution record

- Run 1 (read-only workflow, 19 agents): nine independent investigation slices (A1–A7, E1, E2). Each was followed by a separate adversarial verifier that re-read the cited code and could CONFIRM, QUALIFY or REFUTE each finding and adjust severity/timing. A completeness critic (X) then covered unowned cross-cutting gaps. Result: 126 slice findings (none REFUTED outright; many QUALIFIED/down-rated), about 52 verifier-reported missed issues and 10 critic findings. Raw structured output is kept in session scratch space, not in the repository.
- Run 2 (read-only): consolidation of same-root findings into clusters.
- Main-session spot checks (static re-reading by the report owner):
  - A1-02 CONFIRMED: `Mod/CrewPrecision.lua:22-46` wraps `UnitActions.Run` and returns only `result`. `Mod/UnitActions.lua:159-161` returns `output,investment`. `Mod/Gameplay.lua:792-799` starts CrewPrecision after UnitActions. `Mod/Gameplay.lua:490-491` therefore passes `nil` to `refreshInvestmentSupport`, and its scoped branch and DialogueProjects entry refresh (`Mod/Gameplay.lua:21-37`) never execute on this path.
  - A6-04 QUALIFIED: all 32 `DevelopmentTests/*.py` files referenced by `P0-N1.json` are Git-tracked. The defect is that the executed closure and runner exist only in the ignored local evidence workspace. In addition, three suites the manifest describes as direct regressions (`test_expedition_spy_name`, `..._activity_diagnostic`, `..._activity_failure`) have not been in a recorded executed closure since B196. `test_expedition_gate.py` is an intentionally frozen fixture provider.
  - E1-02/E2-01 CONFIRMED statically: CANCEL is only produced by `Mod/UI/ExpeditionTrainingUI.lua:58-65` (`api.CancelQueue`, called from the ProductionPanel replacement). The empty-queue branch at `Mod/ExpeditionTraining.lua:122-126` deliberately keeps the reservation, and load recovery at `:123` raises `TRAINING_LOADED_QUEUE_MISSING`, which `failure()` turns into HELD. Native removal surfaces other than the replaced panel remain UNKNOWN (no native test).
  - E1-11 CONFIRMED statically: `Mod/UI/ExpeditionTrainingUI.lua:81-82` clears a pending handshake after 12 pulses without sending a compensating CANCEL.

## Phase B execution record

- Phase A files were written before any Phase B reading: `Architecture_Findings.md` and `Expedition_Review.md`, both marked Stable.
- The prior audit was then read: `Specialization/Reports/Audit/P16b_P17_Final_Audit.md`, committed in `e02ef75` (2026-10-07). Its last cross-check baseline is `194a459` (runtime B168.195). Since then there are 116 commits, 36 of which touch `Mod/`. The relevant ones are:
  - `943f26c` B169: Store reference-check bounding
  - `343868e` B170: Shared D facts separated from diagnostics
  - `bc54482` B173: Great Work consumer isolation
  - `dcc43aa` B174: scoped investment updates
  - B175–B177: Dialogue M
  - B178–B204: Expedition
- Cross-review run 1 (11 read-only agents) failed: every agent ended on a usage-limit error and returned nothing. Run 2 re-ran the same script and all 11 agents completed: 10 per-finding-group reviewers plus one constraints reviewer. Each re-read the cited code at HEAD, checked the later commits, and classified each prior finding (RESOLVED / PARTIALLY_RESOLVED / OPEN / CHANGED / SUPERSEDED) and its relation to Phase A.
- Report-owner re-verification before adopting corrections that lower Phase A ratings:
  - `Mod/Data/GovernorProbe.sql:34-38` — the ACTIVE gate needs an established governor, which bounds the D working set.
  - `Specialization/Architecture/v2/P0_M_Dialogue.md:10,83` — keeping the Dialogue transport/governor duty is a deliberate decision.
  - `Mod/CityProgressionStore.lua:1088-1091` — an UNKNOWN reservation also blocks admission.
  - `Specialization_v0.1_Architecture.md:79` — B169 contract.
- Phase A files are left as written. Phase B corrections are recorded in Final_Review.md §2.4–§2.5, which takes precedence.
- Expansion reason: checking each prior finding's status at HEAD requires reading the prior per-phase reports (`Specialization/Reports/Audit/*.md`) and the commits after `194a459` that touch the cited code. The stop condition is one status and relation verdict per prior finding group.

## Read ledger (significant entries and expansions)

- Entry: root/Specialization AGENTS, Specialization README, Workflow W0005/R9/W0001/W0004, Advisory AGENTS/README, Authority.json, Status CURRENT block, modinfo load structure, Architecture README / v2 README outline.
- Expansion reasons are recorded per slice below as investigation proceeds.
- Phase A slice ledgers (summarized). Each slice read its question's full core modules: Gameplay.lua, CityProgressionStore.lua, the Expedition modules, the UI replacement scripts, the network and fact modules, DistrictCompleteness, NetworkBoost, PerformanceCounters, RuntimeWork, and the cited carrier writers. It also read the current Architecture sections (`Specialization_v0.1_Architecture.md` current parts, v2 README, D0032 Adaptation/Implementation Plan, Batch D1/D2, P0_N_Expedition, P0_E2 current slice) and the relevant DevelopmentTests files.
- Historical results were read as another agent's interpretation. Main sources: the B025, B064, B072, B076, B077, B129, B169, B170, B174, B175 and B182–B204 results and reviews.
- External, read-only:
  - Base UI files under `<CivVI>/Civ6.app/Contents/Assets/`: InGame.xml, ProductionManager.lua, ProductionHelper.lua, Panels/ProductionPanel.lua, StrategicView_MapPlacement.lua, ActionPanel.lua, the Espionage* files, TutorialUIRoot.lua (event signatures), CityBannerManager.lua, Civ6Common.lua.
  - HD Workshop `2465378070`: DL.modinfo, DL_UnitPanel/DL_CityPanel/DL_ProductionPanel/DL_CityPanelOverview/HD_ActionPanel heads, HD_BuildingTiers.sql.
  - Bounded greps of Workshop modinfos for the same LuaContexts, and for GameEvents names.
  - Reason for each: settle native context, include-chain and event-signature questions that repository code cannot answer. No disk, backup or save scan.
- Ignored local evidence read (inside the repository root): `local/legacy-workspace/Specialization/Status/Validation/Evidence/B204/local/` — runner, log tail and SHA256 list. Reason: establish exactly what the "478 tests PASS" claim covers.
- Not read: the user's Mods.sqlite or enabled mod set; DebugGameplay.sqlite (no configured path); saves; logs; screenshots.
- Process notes:
  - Two subagents created small temporary files in the session scratch directory, outside the repository, contrary to their instruction. No repository, game, Workshop or protected file was modified.
  - The main session wrote only the four Markdown files in this topic directory.
  - No Git write, test run, deployment or game launch occurred.

## Continuation points

- All phases are complete, and all four files are Stable with writes paused for the checkpoint. Corrections go back to the report owner.
- Next entry: user review of Final_Review.md §3.1 and §4. Acceptance for Git follows the existing checkpoint process (Primary reviews read-only, the user accepts named files, Primary commits). Accepting the files for Git does not accept the recommendations or authorize implementation.
