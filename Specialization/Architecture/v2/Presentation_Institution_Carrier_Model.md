# Institution / Ability / Carrier — presentation architecture review

Document Owner: Codex
Record: PAC-I001 / 2026-09-15
Presentation Revision: PAC-R0002
Principle / cumulative presentation-only direction: USER_CONFIRMED
Implementation: NOT_STARTED; UI integration details pending review
Baseline: av2-runtime-b076.103; Mod commit6a84027; Design D0025 unchanged
Evidence: STATIC_CONFIRMED = code/database evidence, not in-game presentation acceptance
Scope: inventory + mapping + tooltip research only; no source/deployment/gameplay changes

## 用户摘要

已记录三层分离：机构是玩家看到的专业组织；能力包解释玩法；技术载体只负责实现。数据库1894个本Mod建筑定义全部InternalOnly，其中4个列为有条件机构候选、4个单体Lv3载体待设计审阅、1886个技术载体。数量是数据库定义，不是每城实例或内存占用。

用户已确认采用presentation-only机构条目：机构随永久Potential逐级累积，不随ACTIVE降级消失；每个机构只解释本阶段新增能力。可复用现有区域列表/Tooltip样式，技术carrier继续隐藏，不进入普通建筑计数、HD Tier、标准化或默认Infrastructure Value。没有本轮实机测试，下一步等待具体UI/Architecture审阅与实施授权。

## 1. Authoritative presentation principle

**PRES-001 Institution / permanent cumulative existence**: 每个已解锁阶段是独立专业机构，跟随永久Potential存在，不是同一建筑的升级外形。对于已建立Identity的城市，Potential=P时，Lv1至LvP机构同时存在；ACTIVE只控制对应Gameplay abilities当前是否生效。ACTIVE下降不得删除、替换或降级机构。Research Potential4同时显示学者结社、研修院、学术联合会、学术总署。低级机构名称是长期制度/RP语义，不是可丢弃Flavor Text。

**PRES-002 Stage-owned Ability Package**: 能力原则上归属于首次解锁阶段对应的机构；Lv1基础专业化说明，Lv2新增Ability，Lv3/Lv4各自新增Abilities。0/1/2/3复杂度进程作为信息层级意图，不凭此创造具体能力或强改当前能力数量。不要把继承能力全集塞进最高级Tooltip。一个Ability仍可由多个Modifier、carrier、Network/Lua共同实现，但实现对象不进入玩家说明。单个Tooltip只包含机构RP简介、本阶段新增named Ability Packages、必要当前状态。

**PRES-003 Technical implementation**: remain internal unless independently justified by institutional semantics/lifecycle. All numeric bits, negative corrections, per-pop compensation, recipient/output/boost selectors and experiments remain hidden. Effects are explained at the institution, including when actual effects reside in other cities or on the player.

**PRES-004 Authority**: Identity/Potential/progression facts remain authoritative. A presentation-only institution entry never reconstructs or changes these facts; it is not an engine Building. ACTIVE controls existing effects independently. New design-talk mechanics are not inferred from institution or ability names.

**PRES-005 Performance**: no new SetUpdate sampling, per-frame scans, full-city Audit, recurring requests, or writes on hover. Render from validated selected-city presentation state; invalidate on changed relevant input/version only. Identical input is a no-op. A view-open/selection on-demand bounded request may be needed if no valid view; not one request per hover. No changes to A–D2 network/sample contracts.

**PRES-006 Presentation-only exclusion**: 用户已接受在对应Specialty District城市UI中展示机构条目，而非普通engine Building。不新增Building Count，不进入HD building tier或Standardization普通模板；Infrastructure Value默认排除，只有明确Design规则点名才能例外。Technical carriers继续隐藏，不因机构展示取消InternalOnly。禁止把展示条目伪装为真实GameInfo Building送入普通建造/购买/维修链。

**PRES-007 Visual hierarchy / inactive abilities**: Ordinary Infrastructure与Specialization Institutions应尽可能可区分。优先原生列表中排序/小标题/图标或轻量样式差异，不要求全新UI。机构名称与条目不随ACTIVE消失；可只灰化未生效Ability正文，并配简短“当前未启用：需满足对应总督条件”等状态，不能仅依赖颜色。不得把总督条件简化为新的ACTIVE计算规则；使用已有确认状态。具体样式尚未实施或实机验证。

## 2. Inventory coverage and classification

Read-only external loaded DebugGameplay database, cross-checked against current Mod/Data SQL, manifest registration and Lua owners. All1894 SPC Buildings have InternalOnly=1. Counts can change with loaded HD building catalog/Eras: B054336=84 targets×4; Dialogue8 era selectors+3 probes. No owned ordinary infrastructure building is added by this Mod. Ordinary buildings below are external dependencies, not files to migrate. Full explicit IDs and disjoint family classification: [JSON inventory](Presentation_Carrier_Inventory.json).

Categories classify reuse potential, not current visibility. CANDIDATE is not permission to reveal; UNCLEAR is a semantic lifecycle decision, not an unidentified effect. None is a verified safe visible institution today. PAC-R0002后，这些候选只表示可复用的语义/映射素材；已接受的路线仍是presentation-only条目，绝不意味着把这4个候选真实建筑公开。

| Family | Count | Category | District |
|---|---:|---|---|
|`BUILDING_SPC_B050_PRODUCTION_POP`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B050_PRODUCTION_SUB`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B050_SCIENCE_POP`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B050_SCIENCE_SUB`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_PRODUCTION_NEG`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_PRODUCTION_POP`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_PRODUCTION_POS`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_SCIENCE_NEG`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_SCIENCE_POP`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B051_SCIENCE_POS`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B053_DISCOUNT`|1|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B053_FIXTURE`|1|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B054_<target>_<level>`|336|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B055_CULTURE_<L>_<N>`|516|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B055_GW_CITY`|1|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B055_GW_OBJECT`|1|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B055_RESEARCH_<L>_<N>`|516|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B057_CULTURE`|2|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B057_RESEARCH`|2|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B058_CULTURE`|45|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B058_RESEARCH`|45|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B059_D<D>`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B059_TEST<percent>`|3|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B060_<yield>_<sign><bit>`|156|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B061_CULTURE`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B061_PRODUCTION`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_B061_SCIENCE`|16|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_CREW_PROJECT_ACCESS`|1|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_DEV_COMMERCE_SUPPORT`|1|PLAYER_INSTITUTION_CANDIDATE|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_CULTURE_SUPPORT`|1|PLAYER_INSTITUTION_CANDIDATE|DISTRICT_THEATER|
|`BUILDING_SPC_DEV_GPP_COMMERCE`|8|INTERNAL_CARRIER|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_GPP_CULTURE`|8|INTERNAL_CARRIER|DISTRICT_THEATER|
|`BUILDING_SPC_DEV_GPP_INDUSTRY`|8|INTERNAL_CARRIER|DISTRICT_INDUSTRIAL_ZONE|
|`BUILDING_SPC_DEV_GPP_RESEARCH`|8|INTERNAL_CARRIER|DISTRICT_CAMPUS|
|`BUILDING_SPC_DEV_INDUSTRY_LV1`|8|INTERNAL_CARRIER|DISTRICT_INDUSTRIAL_ZONE|
|`BUILDING_SPC_DEV_INDUSTRY_LV1_-1`|1|PLAYER_INSTITUTION_CANDIDATE|DISTRICT_INDUSTRIAL_ZONE|
|`BUILDING_SPC_DEV_LV2_HOUSING`|9|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_DEV_LV3_COMMERCE`|1|UNCLEAR|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_LV3_COM_CULTURE`|1|INTERNAL_CARRIER|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_LV3_COM_INDUSTRY`|1|INTERNAL_CARRIER|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_LV3_COM_RESEARCH`|1|INTERNAL_CARRIER|DISTRICT_COMMERCIAL_HUB|
|`BUILDING_SPC_DEV_LV3_CULTURE`|1|UNCLEAR|DISTRICT_THEATER|
|`BUILDING_SPC_DEV_LV3_INDUSTRY`|1|UNCLEAR|DISTRICT_INDUSTRIAL_ZONE|
|`BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD`|8|INTERNAL_CARRIER|DISTRICT_INDUSTRIAL_ZONE|
|`BUILDING_SPC_DEV_LV3_POP_CULTURE`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_DEV_LV3_POP_RESEARCH`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_DEV_LV3_RESEARCH`|1|UNCLEAR|DISTRICT_CAMPUS|
|`BUILDING_SPC_DEV_RESEARCH_SUPPORT`|1|PLAYER_INSTITUTION_CANDIDATE|DISTRICT_CAMPUS|
|`BUILDING_SPC_LV4_PERCENT_CULTURE`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|
|`BUILDING_SPC_LV4_PERCENT_RESEARCH`|8|INTERNAL_CARRIER|DISTRICT_CITY_CENTER|

### Family owners / effect mapping

| SQL definition / current Lua owner | Current actual effect | Migration judgement |
|---|---|---|
| ResearchSupport.sql + ConstantSupport.sql / ResearchSupport.lua | R/C/Commerce Lv1 +3 food/+3 production per specialist | Three fixed district-local candidates. Preserve existing types/IDs and effects if later reused; Name/Description alone is insufficient for visibility/exclusion. |
| IndustrySupport.sql / IndustrySupport.lua | Lv1 fixed food carrier(-1); other8 bits encode BASE production | Only food-only -1 row is conditional candidate; never show eight bits as institutions. Candidate's tooltip must explain whole ability, not just food. |
| Lv2Housing.sql / Lv2Housing.lua |9 City Center housing selectors; explicit ordinary-building tier inputs | INTERNAL; selector count represents amount, not institution level. |
| Lv2GPP.sql / Lv2GPP.lua |32 district bits for specialist GPP (Culture three classes) | INTERNAL; zero workers can mean no active carrier although institution still exists. |
| Lv3Support.sql / Lv3Support.lua |4 fixed local top-ups plus8 Industry BASE Gold bits | Four fixed rows UNCLEAR as institutional reuse; they follow ACTIVE>=3 and disappear on downgrade. Gold bits internal. |
| Lv3Effects.sql / Lv3Effects.lua |16 per-pop R/C bits,3 Commerce connected-network specialist supports | INTERNAL; conditional network subsets do not define independent buildings. |
| Lv4Percent.sql / Lv4Percent.lua |16 per-worker city percentage bits | INTERNAL; zero-worker case prevents stable marker use. |
| CopyYields.sql / CopyYields.lua |80 positive/negative/population correction bits; Research local copy / Industry recipient production | INTERNAL; recipient effects cannot be the source city's institution. No precision changes. |
| CrewProjects.sql / CrewProjects.lua |City Center access marker gates5 Industry projects | INTERNAL; RequiredBuilding links and district placement must remain. Explain Crew access under Industry institution, do not move/rename ID as polish. |
| StandardizationDiscount.sql / StandardizationDiscount.lua |336 target/level carriers; max-source discounted purchase on recipients | INTERNAL; templates are ledger facts, not these buildings. Carrier count is not infrastructure. |
| NetworkBoostInteger.sql / NetworkBoost.lua |90 integer Boost selectors, plus HD extra-boost property | INTERNAL; player effect written via capital, not institution at each source. |
| NetworkBoost.sql + BoostIntegerTest.sql / NetworkBoost.lua |1032 legacy L/N selectors +4 integer probes | INTERNAL legacy cleanup/test; old ID definitions do not mean old linear gameplay is active. Preserve IDs for existing cleanup/save compatibility. |
| Dialogue.sql / Dialogue.lua |8 D selectors at25%×(D−1),3 test percentages | INTERNAL; collection-dependent replacement is not an institution upgrade. |
| GreatWorkAdjacency.sql / GreatWorkAdjacency.lua |156 yield/sign/bit coefficients | INTERNAL; no forced names for correction arithmetic. |
| CommerceConvergence.sql / CommerceConvergence.lua |48 yield bits for current20% direct-source max aggregation | INTERNAL; B061 prefix remains in restored B062 implementation, not proof failed isolated B061 code returned. |
| HalfYieldProbe.sql / HalfYieldProbe.lua |32 experimental population/subtraction carriers | INTERNAL probe only, not institution candidate. |
| PurchaseProbe.sql / PurchaseProbe.lua |fixture+discount experiment | INTERNAL; the fixture is not ordinary infrastructure despite simulating a purchase. |
| GreatWorkProbe.sql / GreatWorkProbe.lua |2 old city/object probe carriers | INTERNAL experiment/cleanup. |
| YieldCarrierProbe.sql |Modifier/trait definitions; no additional SPC Building rows | Technical non-building implementation; not omitted from conceptual mapping. |
| GovernorProbe.sql, Properties, unit/action scripts |title requirements, permanent progression, Crew/investment operations | Non-building facts/actions; no UI building per such object. |

ORDINARY_INFRASTRUCTURE examples: Library, University, Workshop, Factory, Amphitheater, Art Museum, Market, Bank and replacements remain ordinary buildings; they supply slots/tiers/yields read by the current effects. DB currently reports respective HD tiers1/2/1/2/1/2/2/3. Do not infer universal tiers from these examples (current explicit housing catalog has its own reviewed rows). No move/rename/reclassification of external definitions.

## 3. Institution → ability → implementation mapping

The following names come from this user request, not current D0025 strings. Record Research labels as supplied; Industry III PLACEHOLDER and IV STRONG CANDIDATE stay exactly those maturity levels. Culture/Commerce labels were not supplied: no invented names. New ability titles are presentation concepts awaiting precise new Design rules; not permission to silently relabel old gameplay as new gameplay.

| Institution stage | Player ability grouping (current capability, not new design) | Current implementation owners |
|---|---|---|
| Research I 学者结社 |Lv1 specialist support; network participation|ResearchSupport; NetworkBridge/NetworkBoost|
| Research II 研修院 |housing and specialist GPP|Lv2Housing; Lv2GPP|
| Research III 学术联合会 |specialist top-up; population-related Science|Lv3Support; Lv3Effects|
| Research IV 学术总署 |User supplied future labels: 科研基础设施 / 学术主持 / 学术传统. Exact assignment to future rules pending; current abilities remain specialist % and non-Campus copy (lower-stage rules stay at their own institutions).|Lv4Percent; CopyYields; NetworkBridge/Boost; not one carrier each|
| Industry I 匠作坊 |specialist food/BASE production, Crew project access, template/network participation|IndustrySupport; CrewProjects; Standardization ledger; NetworkBridge/Discount|
| Industry II 百工会馆 |housing, Engineer GPP|Lv2Housing; Lv2GPP|
| Industry III 工程部 (PLACEHOLDER) |specialist top-up / BASE Gold|Lv3Support; IndustrySupport|
| Industry IV 土木工程总院 (STRONG CANDIDATE) |User supplied 巨构工程学 / 工程实践 / 工程传统; future exact Rule IDs pending. Current Industry recipient copy/discount retain current rules.|CopyYields; StandardizationDiscount; NetworkBridge|
| Culture I–IV (names pending) |I support/network; II housing/GPP; III top-up/population Culture; IV specialist %, era dialogue, GW BASE adjacency|ResearchSupport; Lv2Housing/GPP; Lv3Support/Effects; Lv4Percent; Dialogue; GreatWorkAdjacency; NetworkBoost|
| Commerce I–IV (names pending) |I support/Trade Center; II housing/GPP; III connected-network specialist benefits; IV direct-source convergence|ResearchSupport; NetworkBridge; Lv2Housing/GPP; Lv3Support/Effects; CommerceConvergence|

**Confirmed cumulative mapping**: Research Potential4的四个条目分别保留各自名称、RP与解锁阶段能力；ACTIVE降到1时四个条目仍在，较高阶段的受限能力显示当前未启用。Network等条件也按各Ability自己的规则展示，不把“机构存在”等同于“全部能力当前生效”。Culture/Commerce表中的I–IV合写仅为审计汇总；实际展示必须拆成各自阶段条目，不能集中在IV。

## 4. Tooltip/UI investigation — local primary source evidence

External paths are read-only references, not bundled source. BASE below = Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets; HD = Steam/steamapps/workshop/content/289070/2465378070.

- BASE/UI/Panels/CityPanelOverview.lua:176–205 builds district rows with BuildingInstance, then calls ToolTipHelper.GetBuildingToolTip(hash, playerId, city), SetToolTipString. Reuse row style/stack and scoped hook, not replace whole city UI. Regional location can be represented by parent district row without creating a native Building.
- BASE/UI/ToolTipHelper.lua:127–239 reads Name, Description, appends native stats and Locale.Lookup(description). Static multiline descriptions and icons are available. Default helper also says 'building' and shows effect statistics: raw carrier tooltip is not suitable for aggregated abilities. Description-only is cheap but cannot represent city-specific Potential/ACTIVE without a scoped extension.
- BASE/UI/CitySupport.lua:688–738 enumerates GetBuildingsAtLocation and increments BuildingsNum for non-wonders. No general institution exclusion exists here. InternalOnly is not a universal native-count immunity promise.
- HD/UI/Loaders/ToolTipLoader_DL.lua:225 onward replaces Building tooltip; City Policy routes to a separate tooltip. Existing precedent for semantic dispatch, but load order and context-local include ownership matter. Avoid replacing the HD-wide helper globally. Delegate untouched rows to whichever helper is actually active.
- HD/SubMods/CityPolicies/UI/CityPanelOverview_CityPolicies.lua:21–45 wraps panel data, hides internal/CityPolicy City Center buildings, and adds separate city-policy presentation via LuaEvents. This is a pattern for presentation-only entries; this particular hook filters City Center only, not evidence of universal hiding in all districts.
- HD/UI/Replacement/DL_PlotToolTip.lua:37 hides InternalOnly; HD/UI/Replacement/DL_ProductionPanel.lua:159 hides it from production; HD/UI/Civilopedia/CivilopediaPage_District.lua:177 additionally checks dummy classification. Hiding is surface-specific and must be verified, not assumed from one flag.
- Current Mod/UI/CityPotential.lua uses bounded selected-city CITY_PRESENTATION_READ view, but also a retained0.5s scalar callback. Reuse response concepts/epoch references, NOT copy the timer as a new institution polling loop. Current view is not a complete future ability-package contract.

Nested hover-within-tooltip navigation is NOT established by these static references. First pass use one normal multiline tooltip; optional existing details/civilopedia entry later. No promise that stock ToolTipString supports clickable nested tooltips. Hover should format cached semantic text, never query carriers/Network/whole empire.

## 5. Classification side effects and minimum safe architecture

HD/UpdateDataBase/HD_BuildingTiers.sql:12–16 automatically selects IsWonder=0, InternalOnly=0, district buildings; dummy exclusion happens later, and requirements/highest-tier tables are generated from this data. Late deletion alone cannot guarantee all already-generated requirements are repaired. Current DB: SPC overlap HD_BuildingTiers=0, housing tier inputs=0, B054 eligible target IDs=0;12 SPC IDs occur in HD_DUMMY_BUILDINGS (three Lv1 constants+nine housing rows). Most other SPC rows rely on InternalOnly/load order rather than explicit dummy membership. Do not generalize those12 to all1894.

Current StandardizationCatalog.lua:14–16 excludes internal/wonder/dummy, but has no universal institution registry check. StandardizationDiscount.sql also selects eligible HD tier rows. Simply unhiding/inserting an institution may admit it into future catalog generation and other building enumeration. Some current building event handlers skip BUILDING_SPC_ by prefix, but that is NOT a guarantee for all consumers or external mods.

No current Infrastructure Value system was found in the accepted Spec or database tables. Establish explicit semantic predicate for future consumers (ordinary infrastructure only), not an implementation in this batch. Native opaque 'number of buildings' effects cannot be globally patched by a SQL taxonomy alone. Pillage/repair/sale/capture and building-completion side effects also matter if a real Building is used.

### Accepted direction and superseded alternatives (not implemented)

1. **USER_CONFIRMED: cumulative presentation-only institution entries inside existing specialty-district UI.** Keep current carriers hidden and untouched. Registry maps institutionId/specialization/level→name/description/abilityIds; implementation bindings remain developer metadata. Scoped UI extension creates one native-style row for each unlocked stage (1..Potential, at most4 per current specialization) from a validated city view; no real Building, hence no added engine building count, template, repair/sale/production effect. Do not inject fake GameInfo IDs into vanilla paths that assume a real building row; render its tooltip directly on the added instance. Must check HD expansion/CityPolicies replacement chain and avoid double instances. This is a small UI integration, not a new standalone panel. If that hook cannot be composed safely, report the limitation rather than silently replace HD.
2. **SUPERSEDED alternative: reuse of fixed carrier as a real institution.** Not the accepted PAC-R0002 route; retained only as investigation history. Four candidates reduce extra objects, but only after lifecycle decision, exact visibility surfaces, explicit institution exclusion and production/purchase prevention are proven. Preserve carrier type IDs and arithmetic. Do not move Crew marker/City Center correction objects to districts. ACTIVE-sensitive Lv3 rows stay UNCLEAR until institution semantics resolved.
3. **SUPERSEDED alternative: new real facade buildings.** Outside the accepted presentation-only route; do not create16 or fall back to this without a new explicit decision. Even zero-yield unbuildable facade has native building-count and event side effects. Not a safe automatic fallback.

### Proposed data and lifecycle contract

InstitutionDefinition (stable semantic ID, specialization, unlockPotential, district family, localization, maturity) → stage-owned ordered AbilityDefinitions (rule IDs, description, active requirements) → implementation bindings (module/technical IDs, developer-only). Many-to-many links; no carrier-presence inference.

CityPresentationView: epoch+current owner/city reference+anchor district+identity+Potential+ACTIVE+presentation revision+validity. Read existing authoritative facts once only when an actual relevant fact changes or on-demand cache miss. Bounded cache for selected/open cities; clear at close/load/owner-reference invalidation. Content equality stops publication/render. Missing sample marks details unavailable, not false0 abilities or gameplay withdrawal. Rendering never schedules gameplay Audits, writes Property/Buildings, or enumerates1894 definitions each time. Static registry resolves once; transient instances reused/reset on city change. For valid Potential P, render the cumulative set {Institution1..InstitutionP}; ACTIVE changes only per-ability status/text, never this set. On close/load, discarding UI instances/cache is not removal of permanent institutional achievements. No institution ledger or permanent Property is introduced for this mirror.

Direct progression/eligibility/governor owners should publish changed lightweight presentation facts; not 'some Audit ran'. District pillage/retirement and localization/definition revision must invalidate relevant visible row where necessary. No new generic publish listener that scans cities, and no periodic query loop. If current sources cannot produce reliable presentation notifications, record a narrow bridge dependency for approval; do not restore polling as compensation.

## 6. Review decisions and staged migration proposal

Resolved by user in PAC-R0002: permanent Potential ownership, cumulative institutions, stage-owned Ability Packages and presentation-only entries. These are no longer DESIGN_DECISION_REQUIRED. “latest Potential replaces lower institutions” and real-building reuse are superseded suggestions, not current recommendations.

Remaining review before implementation:
- Culture/Commerce names and precise future named Ability→Rule ID assignment; Industry III/IV retain PLACEHOLDER/STRONG CANDIDATE. No new Gameplay approved by naming alone.
- District panel placement and compatibility hook; preferred lightweight subsection “专业机构” after ordinary buildings, ascending stage1→4. Same native row dimensions; distinguish with a small icon/label, not a separate new screen.
- Inactive rendering: keep institution name normal, dim only unavailable ability text and add a short status. Compare existing native color/text styles; no new assets required by this decision.
- Missing/pillaged district and noncurrent-owner display require later review; do not infer that permanent institutions are destroyed. Existing ownership/inheritance scope remains deferred.

After review only: (1) approve semantic registry/mapping, (2) prototype one specialization/one row without gameplay changes, (3) validate visibility/tooltip/HD composition and zero idle requests, (4) extend remaining labels, (5) consider any necessary carrier migration separately with save/cleanup plan. Never delete old IDs or redesign bits merely to clean inventory. This does not start BatchE.

Future minimal acceptance (not requested now): selected city's correct district row+abilities; investment and governor changes show distinct Potential/ACTIVE; Potential4 retains all four institutions at ACTIVE1; zero-worker city still has institutions; hover/open-close repeated idle produces0 sends/scans/writes after cache ready; existing Standardization/Tier/ordinary count unchanged; HD replacement order/pillage/load cases. Existing milestone is protected; no new mechanics or fractional precision work.

## 7. Verification / boundaries

STATIC_CONFIRMED inventory counts, local source paths and side-effect gates above. No simulation of an unimplemented UI and no USER_GAME_TEST_PASS claimed. Current1894 ID groups are disjoint/complete in JSON; 4 candidate+4 unclear+1886 internal=1894,0 new ordinary infrastructure. Existing native ordinary-building examples remain outside owned carrier inventory. Database opened mode=ro, no game launch, no files under Mod changed, no deployment. D0025 remains accepted unchanged; this approved architectural principle is stored here, not a new inferred gameplay Design revision. Cumulative presentation-only direction accepted; concrete UI integration remains pending review/implementation authorization, no test required.

## PAC-R0002 decision history

User explicitly approved this investigation direction and rejected the initial highest-Potential-only suggestion. Permanent cumulative institutions and stage-owned abilities now replace that proposal. Earlier inventory classifications remain an audit of existing implementation objects, not permission to make those objects visible. Architecture/Presentation documents only; accepted D0025 gameplay text and all Mod files unchanged. Commit/push expressly authorized for this documentation batch; no UI implementation or deployment.
