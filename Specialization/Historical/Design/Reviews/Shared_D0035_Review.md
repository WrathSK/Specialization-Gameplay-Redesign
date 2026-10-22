# Shared D0035 — semantic clarification / consumer confirmation

Document Owner: Codex
Design Authority: User
State: ACCEPTED
Baseline: D0034; Military_D0034 unchanged

## Authority and terminology

[Shared_D0035](../../../Design/Content/Shared_D0035.json) is current Shared authority. D = Absolute Infrastructure Depth; formal Chinese display name **区域基础设施深度**. “区域” fixes the calculation scope, “基础设施” excludes a city's general development or unrelated district assets, “深度” avoids implying percentage completion. Historical “区域完善度” remains an alias, not a second fact. No global Lua/API rename or UI change.

Formula remains min(10,sum eligible ordinary building tier weights1/2/3/4). Cap10 is not a guaranteed fully-built value. Three-tier chainD6 and four-tier chainD10 intentionally differ; additional investment can yield more depth and corresponding ability value. No environment denominator or normalized percentage. Same-tier counts, missing-tier handling, pillage/free/unique/ordinary exclusions and highest-single-district aggregation are unchanged.

No Relative Completeness/C/RelativeD is introduced. Current consumers reward actual infrastructure; Military does not need full completion. An added lateT4 must not itself delay the earlier depth benefit until full completion. Future review opens only for a specific consumer requiring completion relative to its own legal tree. No assumed20–40-turn technical prediction or current balance proof is created.

## Consumer matrix and reference consistency

| Current content | Rule | Result |
|---|---|---|
| Research D0031 | 科研基础设施 | Absolute D; formula unchanged |
| Research D0031 | 学以致用 | Absolute D; formula unchanged |
| Culture D0029 | 意义延展 | Absolute D; formula unchanged |
| Culture D0029 | 巨作启迪 | Absolute D; formula unchanged |
| Commerce D0032 | 商业化已明确引用D部分 | Absolute D; no new conversion |
| Military D0034 | 综合训练Depth→Efficiency | Absolute D; existing onset structure/conversion deferrals preserved |
| Commerce D0032 | 资本投资及发展投资未冻结公式 | UNRESOLVED; no implied relative metric or new D effect |
| Industry D0032 | Standardization | NOT_D_CONSUMER; template/tier rules |
| Shared Lv2 | Housing | NOT_D_CONSUMER; Tier existence |
| Military D0034 | 综合训练Breadth→Quality | NOT_D_CONSUMER; actual eligibleT1 existence |

The current Spec explicitly resolves existing Shared_D0028 imports through this semantic amendment. Profession content files stay byte-identical: no repeat Military rewrite, no mechanically version-bumping five professions for a terminology change. Stable DISTRICT_DEVELOPMENT identifier is retained; D0035 preserves all mathematical/ontology keys and other Shared concepts. Original file references still resolve to historical evidence; the new override governs current interpretation only. A future generator must use current Authority and the override, not blindly treat the old imported file as the latest semantic authority.

## Catalog coverage — separate implementation backlog

| Previously investigated object/group | Independent follow-up |
|---|---|
| Data Center | Audit actual installed ID/tier/ordinary classification and catalog coverage |
| 集市 / Fair/Bazaar labels | Resolve actual object IDs/translation; do not confuse existing Grand Bazaar entry with every集市 |
| Art Publisher | Audit ordinary eligibility and tier mapping |
| Harbor expansion buildings | Audit exact installed replacements/branches and catalog omissions |
| HD Neighborhood buildings (villa/mansion/bus families) | Audit actual IDs/domains; similar names in another district are not coverage proof |

These are Catalog / environment coverage / implementation adaptation tasks, not reasons to normalize D. This review records previously investigated gaps; it does not certify every named translated object as a unique missing ID or repair any catalog. P0-A user PASS covers observed buildings and D/working-specialist reads; no full HD/expansion catalog PASS and no unperformed pillage test claimed. Future catalog changes need their own review/tests and authorization, not an implicit P0-B2 start.

## Display / Architecture impact

Canonical Shared had “区域完善度” name/Tooltip; Research_D0031/Culture_D0029 have ability tooltip text using that word, Commerce/Military have Shared D references. Current Spec now carries the semantic override. Inspected current contracts say capped10 or “when reaching10”, not universally fully built=10.

Later presentation work should render the new term in profession descriptions, Civilopedia, P0Panel labels/tooltips and ResearchInfrastructureShadow reports. Architecture names DistrictCompleteness/Shared concept IDs are mathematical contracts, not mandates to rename files/APIs. A0161 adaptation/P0-A reports and historical reviews retain their historical wording and evidence; no Architecture adaptation performed here. Terminology migration must not change cache/version/state semantics.

## Gate and verification

No new Gameplay rule, coefficient, threshold, ability, implementation authorization or blocking decision. Military D0034 breadth/depth/onset/unresolved conversion is unchanged. Shared D0028 and D0034 Spec snapshot retained exactly. Current Design Spec and Shared advance toD0035; other profession revisions stay unchanged. ChangeLog stores new hashes. Workflow navigation updates; previously stale P0 context stays explicitly stale rather than automatically rehashed. Runtime/main/live untouched; no deploy/game test. Stop after docs commit/push.
