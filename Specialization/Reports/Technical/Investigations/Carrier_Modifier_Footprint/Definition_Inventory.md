# Reproducible Definition Inventory

Investigation / Non-authoritative / No design decision implied

Status: Stable

Maintainer: Primary. Baseline: develop `3d0ac4b4c2b1c3d71cb46beb7d1093d191ade795`; 2026-11-02.

Source-only inventory; no source SQL execution, gameplay experiment or effective-loaded database PASS.

## Loading and source population

The manifest has44 InGame UpdateDatabase actions selecting49 distinct SQL files, with no action criteria/ruleset branch. LoadOrder is numeric, not textual order. The49 are each selected once. Their entries in `<Files>` are packaging; ImportFiles exposes Lua/GUI resources without automatically starting them. FrontEnd UpdateDatabase actions select two separate configuration files. Text, Icons and Colors actions address their own databases/surfaces and do not supply these gameplay Modifiers. These distinctions are checked from [Mod/SpecializationP0.modinfo:1](../../../../../Mod/SpecializationP0.modinfo#L1).

The manifest declares Rise and Fall, Gathering Storm, the reused Tycoon art mod and Teddy Persona as dependencies. Source queries additionally require HD tables such as `HD_BuildingTiers` / `HD_DUMMY_BUILDINGS`; a scheduled action is not proof that those dependencies exist or that SQL succeeds in a particular game. No current effective load is certified.

All65 SQL files under `Mod/` were lexed. Sixteen are not InGame UpdateDatabase inputs: two Config, ten Text and four Data icon/color files. The two historical SQL files under DevelopmentTests/Fixtures are outside the runtime package and are excluded from effective definitions; test scripts/fixtures are not additional load actions. Only the two Boost offline source generators were found in the current tools inventory. No generator was run.

## Literal source inventory — all49 gameplay SQL files

Each number counts tuples/unique IDs, not matching lines. `Types` includes all kinds; `B` means Buildings, `M` means Modifiers, `Args` means ModifierArguments, `Links` means BuildingModifiers, `RS/Req` means RequirementSets/Requirements. All1,790 literal Buildings are InternalOnly=1. Generated columns below are **additional to** literal columns. The state column classifies responsibility, not delete permission. Profession/ability follows the family name and the detailed dependency map in [Audit_Report](Audit_Report.md).

| SQL / source anchor | LoadOrder | Literal M | Literal B | Types | Args | Links | RS/Req | Additional generated M; B | Profession / ability | Role |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| [Mod/Data/BoostIntegerTest.sql:1](../../../../../Mod/Data/BoostIntegerTest.sql#L1) | 2000002 | 8 | 4 | 4 | 12 | 4 | 0/0 | 0; 0 | Legacy Boost controls | Manual legacy controls / cleanup |
| [Mod/Data/ClaimProjects.sql:1](../../../../../Mod/Data/ClaimProjects.sql#L1) | 2000006 | 0 | 4 | 8 | 0 | 0 | 0/0 | 0; 0 | Shared Claim access | Production ClaimProjects |
| [Mod/Data/Commerce.sql:1](../../../../../Mod/Data/Commerce.sql#L1) | 10001070 | 0 | 2 | 4 | 0 | 0 | 0/0 | 31; 31 | Commerce Commercialization/Capital | Production Commerce |
| [Mod/Data/CommerceConvergence.sql:1](../../../../../Mod/Data/CommerceConvergence.sql#L1) | 2000005 | 48 | 48 | 48 | 96 | 48 | 0/0 | 0; 0 | Legacy Commerce | Retired positive effects / cleanup |
| [Mod/Data/ConstantSupport.sql:1](../../../../../Mod/Data/ConstantSupport.sql#L1) | 1000 | 0 | 2 | 2 | 0 | 0 | 0/0 | 0; 0 | Culture/Commerce | Production ConstantSupport |
| [Mod/Data/CopyYields.sql:1](../../../../../Mod/Data/CopyYields.sql#L1) | 2000000 | 40 | 80 | 80 | 80 | 40 | 0/0 | 0; 0 | Legacy Research/Industry | Legacy cleanup / inert Science |
| [Mod/Data/Crew.sql:1](../../../../../Mod/Data/Crew.sql#L1) | 10001004 | 0 | 0 | 5 | 0 | 0 | 0/0 | 0; 0 | Industry Crew | Production Crew |
| [Mod/Data/CrewProjects.sql:1](../../../../../Mod/Data/CrewProjects.sql#L1) | 10001005 | 0 | 21 | 41 | 0 | 0 | 0/0 | 0; 0 | Industry Crew | Production CrewProjects |
| [Mod/Data/CultureAesthetic.sql:1](../../../../../Mod/Data/CultureAesthetic.sql#L1) | 10001030 | 0 | 1 | 1 | 0 | 0 | 0/0 | 16; 0 | Culture Aesthetic | Production CultureAesthetic |
| [Mod/Data/CultureInsightsTourism.sql:1](../../../../../Mod/Data/CultureInsightsTourism.sql#L1) | 10001033 | 0 | 0 | 0 | 0 | 0 | 0/0 | 192; 192 | Culture Insights | Production CultureInsightsTourism |
| [Mod/Data/CultureInspiration.sql:1](../../../../../Mod/Data/CultureInspiration.sql#L1) | 10001032 | 8 | 8 | 8 | 8 | 8 | 0/0 | 0; 0 | Culture Inspiration | Production CultureInspiration |
| [Mod/Data/CultureInspirationProbe.sql:1](../../../../../Mod/Data/CultureInspirationProbe.sql#L1) | 10001031 | 4 | 4 | 4 | 8 | 4 | 0/0 | 0; 0 | Culture legacy Inspiration | Retired / production withdrawal |
| [Mod/Data/CultureMeaningProbe.sql:1](../../../../../Mod/Data/CultureMeaningProbe.sql#L1) | 10001030 | 644 | 92 | 92 | 1939 | 644 | 0/0 | 0; 0 | Culture Meaning | Production + cleanup + disabled Culture |
| [Mod/Data/CultureNetwork.sql:1](../../../../../Mod/Data/CultureNetwork.sql#L1) | 10001034 | 0 | 32 | 32 | 0 | 0 | 0/0 | 0; 0 | Culture Network | Production CultureNetwork |
| [Mod/Data/DevelopmentInvestment.sql:1](../../../../../Mod/Data/DevelopmentInvestment.sql#L1) | 10001080 | 0 | 1 | 2 | 0 | 0 | 0/0 | R; R | Commerce Development | Production DevelopmentInvestment |
| [Mod/Data/Dialogue.sql:1](../../../../../Mod/Data/Dialogue.sql#L1) | 2000003 | 0 | 4 | 4 | 0 | 0 | 0/0 | 14max(E−1,0)+56[E≥2]; max(E−1,0) | Culture legacy Dialogue | Retired numeric / live transport and cleanup |
| [Mod/Data/DialogueEffects.sql:1](../../../../../Mod/Data/DialogueEffects.sql#L1) | 10001040 | 0 | 0 | 0 | 0 | 0 | 0/0 | 56E; 8E | Culture Dialogue | Production DialogueEffects |
| [Mod/Data/DialogueProjects.sql:1](../../../../../Mod/Data/DialogueProjects.sql#L1) | 2000006 | 0 | 1 | 2 | 0 | 0 | 0/0 | 0; 0 | Culture Dialogue access | Production DialogueProjects |
| [Mod/Data/DistrictPrecisionProbe.sql:1](../../../../../Mod/Data/DistrictPrecisionProbe.sql#L1) | 2000002 | 0 | 3 | 3 | 0 | 0 | 0/0 | 0; 0 | Legacy Research precision | Inert tombstones |
| [Mod/Data/EngineeringStudy.sql:1](../../../../../Mod/Data/EngineeringStudy.sql#L1) | 2000003 | 0 | 1 | 3 | 0 | 0 | 0/0 | E(2B+D)+3E; E(B+D)+3E | Industry Study/Wonder | Production EngineeringStudy |
| [Mod/Data/ExpeditionGate.sql:1](../../../../../Mod/Data/ExpeditionGate.sql#L1) | 10001050 | 0 | 0 | 2 | 0 | 0 | 0/0 | 0; 0 | Culture legacy Expedition | Production ExpeditionGate |
| [Mod/Data/ExpeditionSpyGate.sql:1](../../../../../Mod/Data/ExpeditionSpyGate.sql#L1) | 10001051 | 0 | 1 | 2 | 0 | 0 | 0/0 | 0; 0 | Culture Expedition | Production ExpeditionSpyGate |
| [Mod/Data/GovernorProbe.sql:1](../../../../../Mod/Data/GovernorProbe.sql#L1) | 1000 | 6 | 0 | 1 | 12 | 0 | 5/5 | 0; 0 | Shared ACTIVE facts | Production ACTIVE properties |
| [Mod/Data/GreatWorkAdjacency.sql:1](../../../../../Mod/Data/GreatWorkAdjacency.sql#L1) | 2000004 | 1092 | 156 | 156 | 3276 | 1092 | 0/0 | 0; 0 | Legacy Culture | Legacy cleanup |
| [Mod/Data/GreatWorkProbe.sql:1](../../../../../Mod/Data/GreatWorkProbe.sql#L1) | 2000002 | 8 | 2 | 2 | 23 | 8 | 0/0 | 0; 0 | Legacy manual Great Work | Manual experiment / cleanup |
| [Mod/Data/HalfYieldProbe.sql:1](../../../../../Mod/Data/HalfYieldProbe.sql#L1) | 2000000 | 32 | 32 | 32 | 64 | 32 | 0/0 | 0; 0 | Legacy manual precision | Retired experiment / cleanup |
| [Mod/Data/Identity.sql:1](../../../../../Mod/Data/Identity.sql#L1) | 1000 | 0 | 0 | 3 | 0 | 0 | 0/0 | 0; 0 | Legacy test identity | Legacy test shell / shared trait |
| [Mod/Data/IndustrySupport.sql:1](../../../../../Mod/Data/IndustrySupport.sql#L1) | 10001001 | 0 | 9 | 9 | 0 | 0 | 0/0 | 0; 0 | Industry | Production IndustrySupport |
| [Mod/Data/InternalCarrierPillage.sql:1](../../../../../Mod/Data/InternalCarrierPillage.sql#L1) | 10002000 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0; 0 | Shared all internal carriers | Companion data only; preserves all InternalOnly SPC buildings |
| [Mod/Data/Lv2GPP.sql:1](../../../../../Mod/Data/Lv2GPP.sql#L1) | 10001000 | 0 | 32 | 32 | 0 | 0 | 0/0 | 0; 0 | Shared four professions | Production Lv2GPP |
| [Mod/Data/Lv2Housing.sql:1](../../../../../Mod/Data/Lv2Housing.sql#L1) | 1200 | 0 | 9 | 9 | 0 | 0 | 0/0 | 0; 0 | Shared four professions | Production Lv2Housing |
| [Mod/Data/Lv3Effects.sql:1](../../../../../Mod/Data/Lv3Effects.sql#L1) | 10001003 | 0 | 19 | 19 | 0 | 0 | 0/0 | 0; 0 | Legacy Culture/Commerce/Research | Inert legacy cleanup |
| [Mod/Data/Lv3Support.sql:1](../../../../../Mod/Data/Lv3Support.sql#L1) | 10001002 | 0 | 12 | 12 | 0 | 0 | 0/0 | 0; 0 | Legacy four professions | Inert legacy cleanup |
| [Mod/Data/Lv4Percent.sql:1](../../../../../Mod/Data/Lv4Percent.sql#L1) | 10001006 | 0 | 16 | 16 | 0 | 0 | 0/0 | 0; 0 | Legacy Research/Culture | Inert legacy cleanup |
| [Mod/Data/NetworkBoost.sql:1](../../../../../Mod/Data/NetworkBoost.sql#L1) | 2000002 | 2064 | 1032 | 1032 | 3096 | 1032 | 0/0 | 0; 0 | Legacy Research/Culture | Legacy cleanup |
| [Mod/Data/NetworkBoostInteger.sql:1](../../../../../Mod/Data/NetworkBoostInteger.sql#L1) | 2000002 | 180 | 90 | 90 | 270 | 90 | 0/0 | 0; 0 | Legacy Research/Culture | Legacy cleanup |
| [Mod/Data/OverflowSinkTest.sql:1](../../../../../Mod/Data/OverflowSinkTest.sql#L1) | 0 | 0 | 1 | 2 | 0 | 0 | 0/0 | 0; 0 | Legacy project fixture | Disabled access fixture |
| [Mod/Data/PurchaseProbe.sql:1](../../../../../Mod/Data/PurchaseProbe.sql#L1) | 2000000 | 3 | 2 | 2 | 5 | 3 | 0/0 | 0; 0 | Manual purchase | Manual experiment / load cleanup |
| [Mod/Data/ResearchApply.sql:1](../../../../../Mod/Data/ResearchApply.sql#L1) | 2000002 | 0 | 25 | 25 | 0 | 0 | 0/0 | 0; 0 | Research | Production ResearchApply |
| [Mod/Data/ResearchChair.sql:1](../../../../../Mod/Data/ResearchChair.sql#L1) | 2000002 | 0 | 0 | 0 | 0 | 0 | 0/0 | 8C; 8C | Research | Production ResearchChair |
| [Mod/Data/ResearchCross.sql:1](../../../../../Mod/Data/ResearchCross.sql#L1) | 2000002 | 32 | 32 | 32 | 64 | 32 | 1/0 | 0; 0 | Research | Production ResearchCross |
| [Mod/Data/ResearchInfrastructure.sql:1](../../../../../Mod/Data/ResearchInfrastructure.sql#L1) | 10001020 | 0 | 4 | 4 | 0 | 0 | 0/0 | 0; 0 | Research | Production ResearchInfrastructure |
| [Mod/Data/ResearchSupport.sql:1](../../../../../Mod/Data/ResearchSupport.sql#L1) | 1000 | 0 | 1 | 1 | 0 | 0 | 0/0 | 0; 0 | Research | Production ResearchSupport |
| [Mod/Data/ResearchTradition.sql:1](../../../../../Mod/Data/ResearchTradition.sql#L1) | 2000007 | 5 | 5 | 5 | 10 | 5 | 0/0 | 0; 0 | Research | Production ResearchTradition |
| [Mod/Data/Restructuring.sql:1](../../../../../Mod/Data/Restructuring.sql#L1) | 10001090 | 1 | 2 | 3 | 1 | 1 | 0/0 | Y; 0 | Commerce Restructuring | Production Restructuring |
| [Mod/Data/StandardizationDiscount.sql:1](../../../../../Mod/Data/StandardizationDiscount.sql#L1) | 2000001 | 0 | 0 | 0 | 0 | 0 | 0/0 | 4B; 4B | Legacy Industry | Retired discount / withdrawal |
| [Mod/Data/StandardizationEffects.sql:1](../../../../../Mod/Data/StandardizationEffects.sql#L1) | 2000002 | 0 | 0 | 0 | 0 | 0 | 0/0 | B+D; B+D | Industry Standardization | Production StandardizationEffects |
| [Mod/Data/TestAmerica.sql:1](../../../../../Mod/Data/TestAmerica.sql#L1) | 10001100 | 0 | 0 | 2 | 0 | 0 | 0/0 | 0; 0 | Current test identity | Current test shell / shared trait |
| [Mod/Data/YieldCarrierProbe.sql:1](../../../../../Mod/Data/YieldCarrierProbe.sql#L1) | 1100 | 6 | 0 | 0 | 12 | 0 | 2/2 | 0; 0 | Shared manual precision | Manual, trait-attached / gated |

Literal totals: **M4,181; B1,790; Types1,836; Args8,976; Links3,043; RS8; Requirements7; TraitModifiers12; Building_CitizenYieldChanges79; Building_GreatPersonPoints48; Units9**. No duplicate literal IDs or composite argument/link keys were found within this population. Zero literal policies / UnitAbilities. Direct building-yield/GPP rows are not counted as Modifiers.

Catalog-independent generated families: Commerce adds31 M/B/Types/Links; Insights adds192 M/B/Types/Links; Aesthetic adds16 M/Links/RS/Requirements and no Buildings. Thus **M4,420; B2,013; Types2,059; Links3,282; RS24; Requirements23**, before catalog-dependent additions. The extra fixed ModifierArguments count is462 (Commerce62 + Insights384 + Aesthetic16), giving9,438 before catalog-dependent arguments.

## Exact catalog-dependent formulas

| Parameter | Exact loaded population / source |
|---|---|
| E | `COUNT(*) FROM Eras` as observed when the actions execute; not assumed equal to eight supported collection eras |
| B | Distinct BuildingType selected into SPC_B054_Targets by [Mod/Data/StandardizationDiscount.sql:3](../../../../../Mod/Data/StandardizationDiscount.sql#L3) (four levels per target) |
| D | District rows in SPC_StandardizationTargets, [Mod/Data/StandardizationEffects.sql:7](../../../../../Mod/Data/StandardizationEffects.sql#L7) |
| C | Actual matches of the13 named ResearchChair targets, [Mod/Data/ResearchChair.sql:2](../../../../../Mod/Data/ResearchChair.sql#L2) |
| R | Distinct qualifying PrereqDistrict in SPC_DevelopmentEffects, [Mod/Data/DevelopmentInvestment.sql:3](../../../../../Mod/Data/DevelopmentInvestment.sql#L3) |
| Y | `COUNT(*) FROM Yields WHERE YieldType<>'YIELD_FOOD'`, [Mod/Data/Restructuring.sql:12](../../../../../Mod/Data/Restructuring.sql#L12) |
| S | Conditional speed-correction Crew project rows, `SPC_CrewSpeedCosts` at CrewProjects.sql:68–99; affects Types/Projects, not Buildings/Modifiers |
| Q | Campus/replacement Districts selected into ResearchCross Requirements, [Mod/Data/ResearchCross.sql:4](../../../../../Mod/Data/ResearchCross.sql#L4) |

These are source-structure totals assuming all statements succeed, generated families do not collide with external IDs, and catalogs are unchanged between relevant actions. They are not queries of a currently verified game database.

For E≥2:

```text
Unique Modifiers = 4462 + 73E + (5+2E)B + (1+E)D + 8C + R + Y
Unique Buildings = 2012 + 12E + (5+E)B + (1+E)D + 8C + R
Unique Types     = Unique Buildings + 46 + S
BuildingModifiers links = Unique Modifiers − 1138
RequirementSets = 24
Requirements = 23 + Q
```

The1,138 Modifiers lacking BuildingModifiers in this source set are B055 Culture1,032 + B058 Culture90 + B057 Culture4 + Governor6 + YieldCarrier6. The last12 are Trait-attached; “no BuildingModifiers” is not “unattached.” No generated family reuses one Modifier on several buildings in this source graph.

Unreduced expressions for E≥1 (including E=1, where the simplified constants do not apply):

```text
M = 4420 + [14max(E−1,0) + 56·I(E≥2)] + 56E + 3E
    +4B+(B+D)+E(2B+D)+8C+R+Y
Bld = 2013 + max(E−1,0) +8E+3E+4B+(B+D)+E(B+D)+8C+R
```

The source's Engineering recursive seed starts at1 even for an empty Eras table, so the above0-era expressions are not a promise of valid empty-catalog execution. E≥2 is the stated supported algebra case. Four legacy Dialogue test buildings are already literal; their56 Modifiers arise from four14-row D2 clones and are generated only if D2 exists. Do not add those buildings twice. No actual E/B/D/C/R/Y values are claimed here.

| Generated family | Additional M / links | Additional Buildings | Construction or lookup dimensions |
|---|---:|---:|---|
| Commerce |31|31|Bits0–30|
| Aesthetic |16|0|Sixteen plot-property gates on one literal master|
| Insights |192|192|Final value1–192|
| ResearchChair |8C|8C|Target building×8bits|
| Old B054 |4B|4B|Target building×4tiers|
| Current STD base |B+D|B+D|Target building/district|
| Study levels |E(2B+D)|E(B+D)|Target×level; building target adds purchase link|
| Wonder |3E|3E|Era×10/20/30|
| Current Dialogue |56E|8E|5-point totals through40E×7categories|
| Legacy Dialogue |14max(E−1,0)+56I(E≥2)|max(E−1,0)|Seven categories×Culture/Tourism, plus4controls|
| Development |R|R|Distinct qualifying district|
| Restructuring |Y|0|Non-Food yields on literal disruption building|

ResearchCross adds Q Requirements/arguments and membership rows, not new carrier counts. Lv2Housing builds metadata from known buildings, not more than its nine literal Housing carriers. Crew speed corrections generate conditional project rows from GameSpeeds, not extra buildings/modifiers. Identity/TestAmerica copy naming/presentation associations; icons/text/color add none of these gameplay counts. InternalCarrierPillage inserts companion XP2 rows and is neither another building nor another Modifier definition.

## Largest contribution families and package scale

| Catalog-independent rank | M | B | Qualification |
|---|---:|---:|---|
| NetworkBoost |2,064|1,032|Legacy|
| GreatWorkAdjacency |1,092|156|Legacy|
| Meaning |644|92|Production plus compatibility/disabled options|
| Insights |192|192|Production SQL-generated constant|
| NetworkBoostInteger |180|90|Legacy|

These five account for4,172 of the4,420 catalog-independent Modifier subtotal. Copy40 belongs to the original spotlight subtotal, not the above top-five. Legacy Dialogue and target×level families are not ranked without catalog values. In particular Engineering's `E(2B+D)+3E` can be among the largest; the ranking is explicitly conditional rather than omitted from consideration.

All Data SQL source files together occupy2,234,760 bytes /13,247 text lines. The original five spotlight files occupy1,950,209 bytes; the three largest literal-Modifier sources total3,800 Modifiers. None of these source measurements predicts compressed package size or native RAM.

## Reference integrity result and its limits

The read-only parser found **zero missing targets in the literal InGame declaration graph** for:

1. ModifierArguments.ModifierId → Modifiers.
2. BuildingModifiers.ModifierId → Modifiers.
3. BuildingModifiers.BuildingType → Buildings.
4. Buildings.BuildingType → Types.
5. RequirementArguments.RequirementId → Requirements.
6. RequirementSetRequirements → RequirementSets and Requirements.
7. Modifiers' nonempty OwnerRequirementSetId/SubjectRequirementSetId → RequirementSets.
8. TraitModifiers.ModifierId → Modifiers (the Trait definition is separately declared by Identity).

Primary-key IDs and composite argument/link keys have no duplicates in that graph. The fixed-range expansions are distinct by constructed prefix/range; their matching Building/Type/Modifier/gate references were checked. Parameter-dependent joins, HD/native ModifierType / EffectType existence, external target objects, actual action success and final engine DB foreign keys remain **NOT_RUN**. The formulas expose every catalog-dependent family instead of silently treating SELECT as zero. These bounded source checks must not be described as full loaded-database integrity PASS.

## Inventory fingerprint

- SQL set digest: `56c7bfc85aec6b77b958bfa991c01043210b0b12544653e4abe22bd9079ad65f`.
- Digest construction: SHA256 over sorted `Mod/`-relative SQL path + NUL + per-file SHA256 + newline, UTF-8.
- Manifest SHA256: `59edc69b19cf5bdb197febc13feabf590281b97d2791918f0fafed81f5b8d767`.
- Executed method: the [embedded parser and source checks](Reproduction_Method.md); no gameplay tests or SQL replay. Raw intermediate inventory stayed outside the repository; no expanded Closure/DB/log is published.
