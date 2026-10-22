# P0-B2 — Lv2 Housing / base GPP qualification plan

Status: IMPLEMENTED_LOCAL_PASS — B080.107; [implementation/evidence](P0_B2_Lv2_Qualification.md). Plan below records pre-implementation gates.
Authority: D0035, Research D0031, Culture D0029, Industry/Commerce D0032, Shared D0035; A0160 plan / A0161 runtime contracts.
Baseline: B079.106 / modinfo106; implementation b420a96; P0-B1 user PASS (including Industry), recorded fe07b5b.
Evidence here: STATIC_CONFIRMED source observations only. No new implementation, prototype, deployment or game test.

## D0035 revalidation — 2026-09-20

[Executable context manifest](../../Workflow/P0-B2.json) and [review evidence](../../Workflow/P0-B2_Revalidation.md). Historical revalidation did not authorize implementation; user subsequently explicitly authorized P0-B2. v0.1 scope is exactly Research/Culture/Industry/Commerce. Military D0034 and other future Designs add no required consumers, dependencies, carriers or tests to B2.

Shared D0035 changes semantic/display interpretation of D, not ordinary eligibility or Lv2 rules. Housing uses distinct Tier existence, never weighted D/relative completion, and GPP uses actual workers. Do not import Military depth-efficiency or birth-buff rules. Existing scope, rollback B079.106 and exit gates stand.

Catalog preflight remains mandatory:50 old housing IDs,45 directly present in current Shared allowlist; five absent IDs are FAIR, HD_ART_PUBLISHING_HOUSE, HD_DATA_CENTER, HD_ELECTRONICS_FACTORY and HD_INTERNET_COMPANY (BUILDING_ prefix). Absence does not authorize deletion. Old DATA_CENTER Tier5 versus shared supported0..4 must be resolved from installed definitions/authority before cutover, not clamped. This is not a newly decided Tier cap for Housing. Audit only four-profession relevant entries/replacements; Harbor/Neighborhood completeness and Military are separate future work. Unknown or ambiguous rows cannot silently shrink valid housing.

Actual diagnostics buttons exist but are Hidden=1 in P0Panel.xml. Future B2 may expose/reuse a bounded existing diagnostic entry as necessary; no panel redesign. LV2_GPP_DIRTY also calls old Lv3/Lv4 consumers; preserve unrelated call behavior, do not widen B2 into their redesign. CityInheritance's caller is quarantined/unstarted, not permission to restore ownership.

## Goal / unchanged rules

Adapt existing Lv2Housing and Lv2GPP to shared current eligibility. ACTIVE>=2 (and valid current Identity/Potential/anchor) enables the package. No new named ability or balance change.

- Housing: corresponding eligible specialty district +1, each distinct eligible ordinary-building Tier represented in it +1. Not sum(Tier), not D, not each building. Same-tier duplicates contribute one housing increment; missing lower tiers are not imputed. Example district+T1+T2: +3 Housing, while D=3 coincidentally; district+T1+T2+T3: +4 Housing, not D6 or7.
- Each working specialist: +2 BASE GPP; Research Scientist, Industry Engineer, Commerce Merchant. Culture: Writer+Artist+Musician each+2. Native percent modifiers remain applicable. Empty slots contribute0; never ChangePointsTotal.
- Finished free ordinary buildings and reviewed unique replacements qualify; pillaged/unfinished/internal/institution/Palace/Wonder objects do not. Housing input is not worker count; GPP input is not D.
- Preserve existing city specialty anchor scope; do not extrapolate highest-D selection into Lv2 anchor changes or sum multiple same-domain districts. If current authority requires another scope during implementation review, surface that conflict before changing it.

## Findings from actual B079 sources

| Current source | Confirmed issue / reusable part | Proposed disposition |
|---|---|---|
| Lv2Housing.lua | literal base DistrictType; separate SPC_Lv2HousingTiers; HasBuilding without location/pillage; every city enumerates player districts | ADAPT eligibility + batch index, reuse 9 housing carriers |
| Lv2Housing process | unknown ACTIVE or failed facts becomes empty desired set | preserve verified projection on temporary failure; explicit invalidity withdraws |
| Lv2GPP.lua | RuntimeWork already shares batch facts/districts; native base-GPP carrier math valid; literal district type and no pillage | KEEP bit/math/native base path, ADAPT normalized eligibility |
| Lv2GPP reconcile | unreadable input becomes workers0 and removes carriers before raising error | validate complete plan before writes; temporary unknown holds; confirmed zero withdraws once |
| GPPRefresh.lua | dirty-only UI notification, tries<=3, generic callbacks flush but do not mark dirty | KEEP bounded bridge; inspect only directly needed event qualification, no lifecycle rewrite |
| Gameplay.lua | existing LV2_*_READ, LV2_GPP_DIRTY and explicit action refresh | retain APIs; scope housing refresh where possible, no unrelated consumer rewrite |
| OrdinaryBuildingCatalog / DistrictCompleteness | shared ontology, actual location/pillage and explanatory rows, bounded cache | reuse fact producer; do not copy formula/catalog into housing |
| CurrentSpecializationFacts / EffectiveFacts / SpecialistSupport | progression authority already established | reuse read/anchor facts where semantically identical; no progression writer change |

STATIC audit caveat: old housing SQL names BUILDING_HD_DATA_CENTER as Tier5 and defines carrier slots0..8. P0-A D catalog accepts only0..4 and does not review every old housing entry. Therefore do not blindly replace housing with D.value, D>0 filtering, or silent tier clamp. Before code cutover diff all old housing catalog rows against shared ontology/replacements and the actual loaded definitions, producing RETAIN/RECLASSIFY/UNKNOWN evidence. Shared ordinary eligibility and ability-specific supported Tier are separate. Resolve data/adaptor mismatches from authority and installed evidence; if a real gameplay ambiguity remains, stop that change and request Design decision. Current read-only DebugGameplay snapshot returned no Tier>4 rows although a normal Data Center definition exists; its configuration/load provenance is not proven to be this runtime, so it does not settle the mismatch.

## Implementation sequence after authorization

1. Export exact live writer/carrier/caller inventory and catalog compatibility matrix; establish expected old/new deltas. Protect P0-A/B1 and unrelated modules.
2. Build one verified per-city Lv2 input from current facts + relevant anchor + shared ordinary-building qualification. Reuse existing modules; at most a small Lv2 read helper if both writers need it, no generic ability framework. Consume explanatory rows/tier presence, not weighted D. Unknown member means incomplete plan; no partial withdrawal.
3. Adapt housing then GPP in the same narrow batch. Both remove stale bits before adding changed bits, write only differences. Confirmed ACTIVE<2, lost valid anchor, pillage or workers0 (GPP) remove once. Same input causes0 writes; temporary failure retains previous plan and diagnostic error, never confirmed empty.
4. Named building/district completion/removal/pillage/repair, governor, workers and specialization action events dirty only affected facts/consumers where reliable IDs exist. Unknown event signatures use bounded scope fallback, not guessed argument positions. Once-per-player-turn reconciliation handles missed events. Generic Publish/Playback can flush existing dirty notification only; no unconditional city scan.
5. Extend existing read-only housing/GPP diagnostics: qualification, included buildings and normalized Tier set, exclusions/pillage, expected vs actual carrier amount, workers, added base points per class, unavailable reason. Prefer current diagnostic slots/combined read; no panel redesign or hover request.

## Source boundary / retirement

Likely edits: Lv2Housing.lua, Lv2GPP.lua, focused Gameplay dispatch; tests and diagnostics. Conditional changes only: existing fact producer/read helper, housing tier adapter SQL, GPPRefresh direct events, existing panel label/report wiring and build registration. Any shared change requires P0-A/B1 consumer regression.

Exclusive effect IDs: BUILDING_SPC_DEV_LV2_HOUSING_0..8 (9) and BUILDING_SPC_DEV_GPP_{RESEARCH,CULTURE,INDUSTRY,COMMERCE}_0..7 (32). Keep current native definitions and IDs unless a verified adapter correction requires narrowly documented change; no new yield carrier. The old inference paths cease to be authorities when each existing writer is switched; no parallel old/new application. Same IDs allow idempotent reconciliation of old developer saves, with no new permanent state/migration planned. If persisted schema becomes necessary, return for scope review.

No new III/IV abilities, Research Infrastructure application, Standardization/Network/Commerce redesign, precision, History/ownership/inheritance, Institution UI, general event framework or BatchE. B1 retired carriers remain retired.

## Local acceptance matrix

| Cases | Required result |
|---|---|
| Four professions, ACTIVE1/2/3/4, workers0/1/multiple | II gate correct; 2 base GPP per class/worker; no above-II multiplier |
| Empty district / T1 / T1+T2 / T1+T2+T3 / T1..T4 / onlyT3 | Housing1/2/3/4/5/2 respectively when qualified |
| Same-tier duplicate / free / unique building and district | distinct-tier housing, correct normalization, no per-building overcount |
| Pillaged building / district / repaired / unfinished | excluded while confirmed invalid, restored once on valid change; no deleted permanent history |
| Missing worker/ACTIVE/building facts | no transient clear→restore or partial writes |
| Valid workers>0→0; ACTIVE2→1→2 | legitimate withdrawal/re-enable exactly once |
| Wrong reference / load / repeated manual reads | no stale cross-city application; rebuild safely; read-only diagnostic |
| 1/2/4/8 cities | measured facts/district reads and building checks; no C² player-wide district capture |
| 10,000 unrelated notifications / unchanged repeated input | no new full scan, request or Building/Property write |
| Native GPP SQL + percent modifier contract | base-layer rows correct; never direct additive instant points |

Run focused Lua/SQL tests and dependency/full-runtime regression appropriate to replacing both writers. Preserve historical tests; an explicit wrapper documents only approved eligibility/UNKNOWN deltas, with new assertions replacing conflicting old behavior. Keep normal-case error assertions. Run syntax, manifest, exact effect allowlist, P0-A/B1 and deployment safety checks. Gameplay equivalence is expected on already-valid old scenarios, not on deliberately corrected pillage/unique/UNKNOWN scenarios.

## Minimal future user test (not requested now)

One existing Research city suffices for initial native acceptance: ensure ACTIVE2 and known ordinary tiers; use current diagnostics and city housing, assign0→1→2 specialists and observe added base Scientist GPP0→2→4 alongside native Great People UI. If practical, one governor downgrade/re-establishment checks gating using the same city; do not require a new map or forced disasters/AI wars. If the save already has a cultural city, one read checks all three point classes; do not demand four new cities. Percentage stacking is tested in game only if not covered by reliable existing native evidence, ideally using an already-active modifier in this save. Pillage/replacements receive local coverage; inaccessible engine cases remain explicitly untested, not silently game PASS.

## Exit, rollback and authorization

Exit: eligibility matches frozen rules; verified plans only; existing carrier/base-GPP behavior intact; no unintended old+new effect; local matrices and idle/scaling regression pass; clear on-demand diagnostics. Then coherent commit/push develop, W0003 safe test deployment with game exited and exact previous-package backup/hash, minimal user acceptance, stop. B079.106 is the rollback source/package boundary; main remains unchanged. No automatic P0-C.

No blocking Design decision identified for the planned batch today. Catalog compatibility above is a mandatory implementation preflight, not permission to silently drop old objects. Approval of this plan is still required before code changes; planning does not authorize implementation or deployment.
