# v0.1 playtest readiness — B266 accepted

Date: 2026-10-20. Review basis: develop `34ee4c1`, unchanged deployed source `0c2c4aec852411c40c0998c2693dad1346f470dd`, **B266.293 / modinfo293**. This is a documentation and readiness checkpoint, not a new implementation batch.

## Decision and scope

The user reports that B266 acceptance is complete and requests one final v0.1 check, explicitly **without a PR**. Record **USER_GAME_TEST_PASS for the combined B266 UI recovery review**: new-city institutions, the city-panel shortcut and the remaining profession-color presentation check. This is the user's overall acceptance, not a new set of independently measured per-item observations. No new screenshot/log analysis or game operation is claimed.

The previous B265 failure remains preserved in its [frozen result](Specialization_B266_Institution_Refresh_Recovery.md). The difficult consecutive-governor-promotion scenario remains an ordinary-play observation, as the user requested; B266 acceptance does not claim a new controlled reproduction of it.

**Conclusion: no new blocker was found for the user-approved four-profession v0.1 playtest scope. B266.293 is ready to be designated as its first playtest candidate.** This is not completion of every accepted Design provision, all lifecycle tests, balance or the deferred audits. The user's [post-playtest priority decision](../../../Reports/Proposals/Audit_Followup_Priorities.md#v01-playtest-scheduling-checkpoint) remains controlling.

No baseline tag, release, PR, main promotion or new deployment is created. The user has not yet designated this candidate as the long-play node or ended W0003 standing permission; this check changes neither rule.

## Functional closeout

| Area | Available mainline and applicable evidence | Retained limit |
|---|---|---|
| Research | Specialist support, infrastructure, interdisciplinary research, application, academic leadership and Academic Tradition are implemented. [D3 acceptance](Specialization_B086_P0D3_User_Pass.md) and [Tradition acceptance](Specialization_B144_F2_Pass.md) retain their actual scopes. | Old Research network effects are deliberately retired for v0.1; the redesign is deferred. No new universal Research native PASS is inferred. |
| Culture | Specialist support, Aesthetic influence, the implemented automatic Meaning subset, Inspiration, era Dialogue, Insight Tourism and Culture Network operate under the accepted compromises. The [B232 implementation/evidence index](Specialization_B232_Native_Review.md#culture-implementation-and-remaining-scope) records their boundaries and network update/withdrawal acceptance. | Intermittent Expedition task/activity issues, remaining Government/Diplomacy Meaning and era-coverage presentation remain held. Existing working missions, Insight history and effects remain enabled. |
| Industry | Wonder history/typed templates, specialist support, Standardization, Engineering Tradition/Practice, Megaproject Engineering and Crew training/injection are implemented. [B233](Specialization_B233_Native_Review.md), [B234](Specialization_B234_Native_Review.md), [B235](Specialization_B235_Native_Review.md), [B236](Specialization_B236_Native_Review.md) and [B239 occupancy acceptance](Specialization_B239_Native_Review.md) supply the relevant history/effect/refresh/reservation evidence. | Exact District-body purchase discounts remain unimplemented and deferred. Accepted native rounding and Crew amplification are retained. The IV increment uses the accepted existing carrier; do not convert its displayed projection into a newly measured native increment. |
| Commerce | [Commercialization/Reputation](Specialization_B240_Native_Review.md), [Capital signing/cold-load/settlement](Specialization_B245_Native_Review.md), [Development investment](Specialization_B246_Native_Review.md), and [Restructuring core flow](Specialization_B249_Native_Review.md) have scoped acceptance. Per-call Gold tolerance remains 0.01, with the existing strict saved receipts and repeat protection. | Restructuring cold-load and the simultaneous Standardization/Development combination remain the two integration checks below. Deferred city-loss boundaries are not marked passed. |
| Entry and UI | B262 Capital UI was accepted in the [B263 authorization record](Specialization_B263_Roosevelt_Test_Shell.md#scope-and-evidence). The neutral Roosevelt shell and institution formatting were [accepted with B264](Specialization_B264_Acceptance_and_City_UI_Investigation.md#scope-and-acceptance); B265's institution regression is now accepted as repaired by B266. | Minor institution-icon softness remains deferred. No claim of every UI scaling/environment combination. |

### Inherited implementation review

This review checked actual Gameplay startup and current registration, rather than treating old plan headers as current status. Research writers, Industry history/Standardization/Engineering, Commerce/Capital/Development/Restructuring and Culture writers are registered. `NetworkBoost`, `CopyYields`, old `StandardizationDiscount`, Great Work adjacency and old Commerce convergence retain their explicit retirement paths. The new test selection is the independent America/Roosevelt pair; the legacy Scotland registration remains disabled for new games.

Twenty-one named core Lua files are byte-unchanged against the B249 functional checkpoint `ad34b1f`: ResearchInfrastructure, ResearchCross, ResearchApply, ResearchChair, ResearchTraditionEffects, CultureAesthetic, CultureMeaning, CultureInspiration, DialogueProjects, DialogueEffects, IndustryHistory, StandardizationEffects, EngineeringStudyProjects, IndustryWonderEffects, CrewProjects, Commerce, CapitalInvestment, DevelopmentInvestment, Restructuring, NetworkInput and NetworkBridge. This preserves the relevance of earlier evidence; it is not a new all-system native test.

The intervening Store/Gameplay/Training differences were also inspected: detached institution summaries, read-only banner publication, refresh after proved investment commits, and bounded admission/presentation diagnostics. They do not revise formulas, saved schemas or transaction amounts. The separate Roosevelt name-pool/access adaptation and city UI lifecycle changes retain their B263/B265/B266 evidence. Not every file changed since B249 is described as presentation-only or unchanged.

## First playtest boundary

Use the existing supported environment: Gathering Storm, the installed HD setup, the Roosevelt persona dependency, Standard speed, single-player human, and the dedicated Chinese **America / Roosevelt (Bull Moose) test pair**. Only Research, Culture, Commerce and Industry are in scope. Ordinary civilizations, AI/multiplayer access and future professions are not enabled by this readiness decision. Legacy Scotland saves retain their existing access; no save conversion is performed.

The user will avoid own-city-loss scenarios in this campaign. Continue normal play without repeating completed batch rituals. Observe these two integration cases when convenient:

1. Save while a city is REALLOCATING, fully exit/restart, load, and finish its existing manual configuration. Check the same team/target, retained Potential, disruption and remaining wait. The continuous B249 flow is already accepted.
2. On a matching building, observe Standardization and Development investment together, then the existing completion/withdrawal path. B246 separately established the 50% effect and lifecycle; it did not exercise a positive Standardization contribution on that target.

The existing collector can accompany play under the user's manual-start workflow. Logs are preferred for identity, receipts, state and transitions; screenshots remain useful for actual appearance or a native yield the logs do not measure. No collector, game or Tuner session is started by this check.

## Retained high-priority follow-ups

The existing follow-up plan remains the single scheduling record. After the v0.1 playtest: own-city-loss consequences across modules; Expedition task root cause/repair and related held placement/source-loss work; remaining Meaning Extension; exact Industry District purchase discount; Research network redesign; era-coverage presentation; remaining independent and Advisor audits. Original severity, evidence gaps and accepted working paths remain intact.

Restructuring cold-load and additive investment effects are inside-playtest checks, not silently moved to post-playtest or marked passed. Consecutive governor promotions and icon softness remain the existing incidental UI observations. Accepted engine Floor behavior and Crew amplification remain future balance observations, not new compensating code.

## Current verification and deployment

STATIC_CONFIRMED in this check:

- Clean develop matched origin at the review start. D0057 / A0177 and the existing manifest/Context Lock passed: 288 runtime files, 924 guarded context files before this new report.
- All 287 registered files plus modinfo exactly match the 288-file source package, with no duplicate registration or missing action file. All 185 Lua files compile under Lua 5.1; all 32 XML/artdef/dep/modinfo files parse. The package contains no raw screenshots, logs, saves, databases, Python bytecode or symlinks.
- Source and live packages match 288/288, digest `c4a99db788159d5a986a963760543a8a331d2343e863cde4d002e5feb8eebab3`. Receipt `B266.293-0c2c4ae-playtest.json` is DEVELOP_ACTIVE and identifies the exact source above. Mod is unchanged since that deployed source commit.
- Stable and outgoing B265 recovery snapshots match their receipts. No pending deployment marker exists.
- Main remains clean at `e901a224faae1274563fae07012116543bee6759`, B069.96/modinfo96, 115 files, digest `7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df`.
- No tracked raw image/log/save/database files were found by the scoped extension check. This is not a repeat of the complete historical privacy audit.

LOCAL_SIMULATION_PASS remains the named earlier batch evidence, including B266's 64 targeted tests. Those unchanged tests are not rerun or relabeled native in this documentation-only check. New checks cover package/static integrity and document/reference/current-state consistency; no whole-history regression or performance campaign is run.

Final document/reference checks (16 links/anchors), Context Lock (288 runtime / 925 guarded files) and whitespace checks PASS. The staged publication gate must pass before this checkpoint is committed. Only this report, Status, Authority, P0-H and their Context Lock entries change. Runtime, Design, Architecture, tests, configuration, frozen evidence, other roles' files, main and deployment remain unchanged.

## Handoff

- User decision: designate the first v0.1 playtest baseline when ready; PR/main promotion remains unapproved.
- User testing: ordinary campaign with the two integration observations above; no additional B266 retest.
- Primary next: complete owned documentation checks, normal develop commit/push, then stop. No further implementation or deployment is authorized by this readiness review.
