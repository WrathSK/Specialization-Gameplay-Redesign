# Military D0033 — freeze review

Document Owner: Codex
Design Authority: User
State: DESIGN_FROZEN / implementation and balance pending
Accepted: 2026-09-20

## Authority

[Military_D0033](../../../Design/Content/Military_D0033.json) is the single mechanical content authority. [Original brief](../../../Design/Military_Freeze_Candidate_User_Record.md) and [candidate review](../../../Design/Military_Freeze_Candidate_Review.md) remain unchanged historical evidence. Five subsequent user answers close MIL-BLOCK-01–05. D0032 Spec is preserved byte-for-byte in Revisions; other profession/Shared JSON unchanged. New Design revision does not authorize Military implementation or expand the current four-profession P0 plan.

## Five decisions resolved

1. Land combat only. Production and purchase (Gold/Faith) included. Free/levied/duplicated/captured acquisitions count only with confirmed attribution to this city; otherwise excluded. This is an eligibility rule, not proof the engine can identify every acquisition.
2. Unit abilities are permanent training snapshots, not dynamic source-city benefits. E and applicable Tradition parameters are locked at grant; current actual unit/mentor promotions and adjacency remain combat inputs. Thus the old formula arithmetic remains, but old “current source-city E at combat” semantics are superseded. Later city ACTIVE/Identity/building/specialist/Tradition changes do not alter existing unit buffs. Same Military ability max on merge, different abilities separate; no ongoing merged-unit source-city choice required. “All abilities as buffs” here concerns awarded unit training effects, not converting Housing, logistics or Network into permanent global effects.
3. Whole upgrade unit line is a common mobilization target, including corresponding unique replacements and single/Corps/Army. Not whole PromotionClass. Database mapping/API reliability remains technical.
4. Each disconnected eligible network has its own commander; cities respond only to their own network commander. Shared direct/distribution/non-recursive membership is retained; not every road-connected city and not a new reverse-route rule. Component/split-merge representation belongs to later Architecture review.
5. ACTIVE changes are relevant events: a newly higher candidate takes over without a production switch, and a lowered commander yields to a higher candidate. Equal authority retains incumbent; actual invalidation uses the confirmed bounded election/tie-break.

BLOCKING_DESIGN_DECISION: None. No replacement balance values, new unit cap, cooldown or extra gameplay adopted.

## Formula and evidence boundaries

Mentorship keeps D0008 range1/highest eligible own mentor/independent bonus with same PromotionClass restriction. Insight keeps min(E_birth,floor(P_current/2)), now IV with immutable training E. These are not fixed XP awards frozen regardless of later promotions. No normal combat-XP cap override. Current installed HD SQL and newer cached database32 versus old model8 remains BALANCE_REVALIDATION_REQUIRED; old user-reported proof is not discarded but not claimed re-proven for changed inputs, new Tradition increments or the new birth snapshot.

Technical review remains for combat-event snapshots/exceptional combat categories, acquisition attribution, per-ability compound buff representation/max inheritance, upgrades, logistics link/tick/save/AI, GG consume-without-retire, unit-line mapping and active-production events. None authorizes silent fallback or implementation. If a native boundary produces materially different player rules, return for decision before implementation.

## Preserved non-blocking items

Lv1武备社/Lv2武官所 are placeholders; III演武场/IV讲武堂 and all ability names locked. Tradition thresholds/order/increments, logistics costs/coverage/Uranium and mobilization bonus/scaling remain as registered. City Tradition/ownership/logistics Legacy is independent from already-awarded unit permanence. Shared D absolute-depth versus relative-completion issue remains separate; training uses actualT1, not D.

Old +15%XP, III5F5P, garrison training and free-unit progress pool are superseded in current Military. Historical Harbor/Aerodrome content is not rewritten: its old cross-references refer to historical D0008, not permission to automatically mirror D0033. No changes to Research/Industry/Culture/Commerce.

## Workflow and verification

Authority navigation advances to D0033/Military_D0033. Existing P0-B1 completion evidence remains valid at its D0032 baseline; its reusable context is explicitly STALE_PENDING_REVIEW. Context_Lock hashes are deliberately not blindly regenerated. A0161 remains adapted through D0032, not falsely marked adapted to new Military. Next implementation requires contextual refresh and separate authorization; P0-B2 remains plan only.

Checks: JSON/reference parsing; D0032 snapshot and old canonical hashes; narrow Spec supersession; no runtime/UI/SQL/main/live changes; diff whitespace. No game test or gameplay simulation claimed. Commit/push develop only, no deployment/tag/promotion. Stop after freeze.
