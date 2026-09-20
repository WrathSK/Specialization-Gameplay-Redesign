# W0001 / P0-B2 revalidation — D0035

Date: 2026-09-20
State: PLAN_READY / IMPLEMENTATION_NOT_AUTHORIZED
Evidence: STATIC_CONFIRMED source/contract checks, not Gameplay simulation or engine PASS.

## Findings and scope

Before this task P0_B2_Plan.md existed, but no P0-B2.json; Authority still routed to completed B1 and the CLI accepted only B1. Added an actual B2 manifest and one CLI allowed-batch entry; no runtime tooling or Gameplay behavior changed. W0001 scope is explicitly four professions only. Military D0034 stays Design metadata/future record, not B2 content/dependency. Other future domains in the existing generic catalog do not authorize profession implementation.

D0033/34 Military changes have no B2 effect. D0035 clarifies absolute D and display term, keeps formula/ontology/pillage/unique/free rules unchanged, explicitly excludes Lv2 Housing from D consumers. Research RES_L2_TRAIN, Industry IND_L2_DIVISION, Culture CUL_L2_PATRONAGE and Commerce COM_L2_GUILD retain ACTIVE2/+1 district and distinct tier/+2baseGPP rules. Full objects reviewed, not just formulas. Shared maximum single-district D is not permission to change Lv2 anchored district selection. No new Gameplay conflict found.

## Actual source boundary

Read Lv2Housing/Lv2GPP/GPPRefresh and affected Gameplay handlers; inspected shared catalog/capture/RuntimeWork/current-facts interface and housing SQL. Writer paths still match B079 plan. Housing scans all player districts per city and drops state on unknown; GPP shares batch district facts but unreadable worker/ACTIVE may clear bits. The future batch must use complete verified plans and targeted dirty/reconciliation. No fixes made here.

Exact effect families are9housing+32GPP carriers. GPP SQL uses Building_GreatPersonPoints base rates2*2^bit; Culture has Writer/Artist/Musician rows. Retain definitions unless a verified narrow correction is separately documented; no new ability/carrier. Gameplay manual reads Describe only; unit/investment paths and dirty bridge can call audits. GPP dirty also wakes unrelated Lv3/Lv4 modules: preserve behavior outside the two writers, avoid a broad propagation redesign. CityInheritance caller found by full-Mod search remains quarantined; no ownership activation.

Existing Lv2 UI buttons are hidden, so implementation must provide a usable on-demand route by reusing existing diagnostic controls, not assume visible buttons. GPPRefresh generic notifications flush dirty state only, bounded tries3; no per-second sampling needed.

## Catalog gate (not semantic normalization)

Static crosswalk:50old housing entries;45have a named Shared allowlist counterpart. Missing5: BUILDING_FAIR(T1), BUILDING_HD_ART_PUBLISHING_HOUSE(T3), BUILDING_HD_DATA_CENTER(T5), BUILDING_HD_ELECTRONICS_FACTORY(T3), BUILDING_HD_INTERNET_COMPANY(T4). Named overlap alone does not prove tier/replacement correctness. Each old entry must receive RETAIN/RECLASSIFY/UNKNOWN disposition against actual relevant environment before cutover; no omission means deletion. OldDataCenter5 versus Shared0..4 remains unresolved adapter evidence, not authorization to clamp5→4 or impose Dcap10 on housing. If actual Design scope is ambiguous after evidence review, stop that cutover and ask the user. No current new Design decision identified.

Four-profession closure only. Broader Harbor/Neighborhood catalog gaps stay separately registered in Shared_D0035_Review; not mandatory B2 expansion. Unknown complete-input handling must not clear verified benefits. A mere catalog exclusion reason must not hide an old counted ordinary building.

## Reuse / hashes / authority

All126Mod files match inherited Runtime_Index hashes from B079.106; runtime index unchanged. No full unrelated runtime text re-audit or Gameplay regression run. Previously locked changed documents were Spec, ChangeLog and Content README: reviewed D0033–35 semantic deltas and current four-profession refs before refresh. Other hash-identical contracts/tests keep named B079/P0-A/B1/A–D2 provenance. New B2 direct refs and planning files added to lock. Prior B1 COMPLETE result remains historical and its authority map remains D0032; the current entry now uses B2. Future implementation must read direct modules required by manifest and honor conditional/audit triggers.

Architecture A0161 continues its original D0032 adaptation metadata; this review confirms only unchanged four-profession B2 applicability under D0035. It does not claim broad future Architecture adaptation. No Design revision or new Status revision created for this navigation note.

## Updated implementation sequence (requires separate authorization)

1. Confirm clean baseline/versions; exact old writer and41carrier inventory; resolve50-row catalog and replacement/Tier disagreements. Scope only relevant four-profession closure.
2. Build complete verified anchored Lv2 inputs from existing current facts/ordinary classification/native worker facts. Housing reads distinct Tier presence, not D or D-selected district. No new persistent state.
3. Adapt existing Housing/GPP writers in place: confirmed invalid withdrawal once, UNKNOWN holds last verified projection, unchanged input0writes, no old+new parallel authority.
4. Scope relevant district/building/pillage/worker/governor/Identity events; batch indexes and once-per-player-turn reconciliation. No generic full scan or new hover request.
5. Read-only diagnostics explain anchor, qualification, tier set/exclusions, workers and expected/actual existing carriers. Keep unknown-state explanations.
6. Local matrix,1/2/4/8city scaling,10kidle, SQL/syntax/manifest, P0-A/B1/A–D2 and deployment safety checks. Then coherent implementation commit/push and only authorized safe test deployment; current task never deploys.
7. Minimal later one-city housing/workers/GPP test. Optional existingCulture/governor case, no artificial forced pillage. Stop atB2; rollbackB079.106, no P0-C.

Exit: frozen eligibility, no silent catalog loss, baseGPP native percent path, verified-only writes, idle/scaling budget and unrelated outputs protected, usable diagnostics, explicit native untested limits. PLAN_READY does not mean preflight already resolved or implementation passed.

## Validation of this synchronization

W0001 check/plan/read/self-test forB2; Python syntax via in-memory compile; selected references and hashes; exact runtime file-set126; effect SQL inventory; protected Design/main/live integrity; git diff check. These validate navigation/planning only, not Lv2 fixes. Results and commit/push reported in task response. Stop awaiting user P0-B2 implementation authorization.
