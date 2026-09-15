# Mod Interaction Dependency Audit

Document Owner: Codex
Scope: installed modinfo + read-only current Mods.sqlite; no configuration/source changes.
Evidence level: STATIC_CONFIRMED = manifest/database evidence, not gameplay compatibility PASS.

## Exact identities and manifest fingerprints

### TITLE
- UUID: `107a9043-4c73-4d5b-8007-79b55f19ba4a`
- Installed manifest: Workshop/2672533453/ModsTitleLocalization.modinfo
- SHA256: `6a515b7008661a07695b32fb571fa2697d535b842550c620076ca0612a515957`
- Dependencies: EMM
- References: none
- Declared Files: 4; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 1000, 10000

### EMM
- UUID: `47dccacd-f1d0-4f25-bb02-deb2b528c833`
- Installed manifest: Workshop/1601259406/EnhancedModManager.modinfo
- SHA256: `c9daf569e7ec8378dc37538b8ed562e5419edf42675f46d67fc6763df2aafde0`
- Dependencies: none
- References: none
- Declared Files: 7; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 9999, unspecified

### AREA
- UUID: `be80630c-536b-4aab-be68-d76453a6f439`
- Installed manifest: Workshop/2573589760/LargerMODinUseArea.modinfo
- SHA256: `353bde1ea36160451577ee071733df4f420c444edc0243d62450cf40b356d4fe`
- Dependencies: none
- References: none
- Declared Files: 3; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 10000, 10001, 10002

### BTS
- UUID: `8d4fa23a-ef43-440c-8422-2bec11f8f5d7`
- Installed manifest: Workshop/873246701/Better Trade Screen.modinfo
- SHA256: `795b8ed6fcee97f02a08ac702b20569257acbac8a7bc43a1f93f7270364f96b3`
- Dependencies: none
- References: none
- Declared Files: 21; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 10, 11, 12, 8, 9

### SPC
- UUID: `df9efdad-dd48-40a7-b868-87f0617bc16d`
- Manifest: live SpecializationP0/SpecializationP0.modinfo (B072.99)
- SHA256: `844f85959d0b4cdafb4d6cef586d315eb718029b1f3aee905fdf58682d58d86b`
- Dependencies: Rise and Fall (Scotland assets), Gathering Storm
- References: none
- Declared Files: 118; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 1000, 10001000, 10001001, 10001002, 10001003, 10001004, 10001005, 10001006, 1100, 1200, 150100, 2000000, 2000001, 2000002, 2000003, 2000004, 2000005, unspecified

### CORE
- UUID: `521b8777-0977-4859-a5ee-3e411a732e5c`
- Installed manifest: Workshop/2465378070/DL.modinfo
- SHA256: `1dd999b1717c1968d54e0deef62af48ec9394bf6e59ffd95afa285c4f9be21c8`
- Dependencies: Expansion: Gathering Storm, Expansion: Rise and Fall
- References: none
- Declared Files: 783; missing: ['GameModeSupport/MilitaryMode/ArmsComplement/DrugCombat.lua', 'GameModeSupport/MultiPlayerMode/DL_GameCapabilities.sql']
- Component LoadOrders (unique; unspecified is not inferred zero): -4, 1, 10, 100, 10000, 10000000, 100001, 100008, 10001, 101, 11000, 12000, 12001, 15000, 150000, 15001, 15002, 15005, 15006, 15007, 15008, 15009, 15010, 15012, 15015, 15016, 15017, 15020, 15050, 15500, 15602, 15603, 15604, 15605, 15606, 15610, 15700, 15750, 15854, 15855, 15999, 16000, 16001, 16003, 16005, 16008, 16010, 16011, 16012, 16014, 16015, 16016, 16017, 16018, 16019, 16020, 16021, 16050, 16052, 16054, 16056, 16058, 16060, 16062, 16064, 17000, 17001, 18200, 18201, 18500, 200, 20000, 200000, 20001, 22222, 25000, 25001, 26000, 28100, 28101, 28102, 28103, 28104, 28105, 30000, 4, 5, 5000, 5002, 6, unspecified

### CIV
- UUID: `32936394-6ae7-4e19-929d-fa47ebc7d055`
- Installed manifest: Workshop/2860503037/CivilizationsDiversity.modinfo
- SHA256: `aa45e7d5d1d911edafd99e09ed73eaf45f3a4ab265b7ed6935ddb6cee7c9a153`
- Dependencies: Expansion: Gathering Storm, Expansion: Rise and Fall, CORE
- References: none
- Declared Files: 167; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 10000, 12005, 16000, 16004, 16005, 16006, 16015, 16020, 16105, 16200, 17000, 18005, 18015, 20000, 20005, 30000, unspecified

### DIST
- UUID: `66add898-b3bb-4bd9-98a2-805d37f0da2e`
- Installed manifest: Workshop/2701747165/DistrictExpansionHD.modinfo
- SHA256: `043f3e9845fd8b4234e6e4f3f49ccd6e02168003323fdb5473dcba215af1184d`
- Dependencies: CORE, Expansion: Gathering Storm, Expansion: Rise and Fall
- References: none
- Declared Files: 49; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 1, 12000, 18000, 18001, 18002, 8000

### IND
- UUID: `c086b5a6-90d2-4dea-a32f-c642639b9469`
- Installed manifest: Workshop/2616754773/CorporationsDiversity.modinfo
- SHA256: `efa2094fefcab2074212ca59418ced47bc5e0c66b601c37069ddabaf65c7639f`
- Dependencies: Expansion: Gathering Storm, Expansion: Rise and Fall, DLC: Vietnam and Kublai Khan Pack, CORE, TYCOON, PRODUCT
- References: none
- Declared Files: 133; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 1, 100, 12001, 160000, 19000, 19010, 20000, 20002, 20003, 20004, 20010, 30001, unspecified

### PRODUCT
- UUID: `a64e1c66-ce48-4d80-8225-47402db353aa`
- Installed manifest: Workshop/2479195330/MonopolyPlusAdjustments.modinfo
- SHA256: `c01b0b232040da0868d905e26f96b10b1917790ed83c1643b7d3fb5237da13d5`
- Dependencies: Expansion: Gathering Storm, DLC: Kublai Khan and Vietnam
- References: none
- Declared Files: 8; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 100, 1000, 500, unspecified

### TYCOON
- UUID: `b248a322-3e2a-4a6a-830a-6b0d1f3435fc`
- Installed manifest: Workshop/2479197624/MonopolyPlus.modinfo
- SHA256: `d674993638665126f67b1d4058a6a9ddcf9b9a191e3d8cbe082ae6adbfd97e26`
- Dependencies: Expansion: Gathering Storm
- References: Kublai Khan and Vietnam DLC Pack
- Declared Files: 376; missing: none
- Component LoadOrders (unique; unspecified is not inferred zero): 1000, 110, 150, 50, unspecified

## Dependency graph

Arrows mean dependent → required. Official DLC remain fixed, not toggled as third-party trials.

```text
SPC → Rise & Fall + Gathering Storm
CORE → Rise & Fall + Gathering Storm
CIV → CORE (+ both expansions)
DIST → CORE (+ both expansions)
IND → CORE + PRODUCT + TYCOON (+ both expansions + Vietnam/Kublai DLC)
PRODUCT → Gathering Storm + Vietnam/Kublai DLC
TYCOON → Gathering Storm
TITLE → EMM
BTS / EMM / AREA → no declared mod dependency
```

TYCOON references Vietnam/Kublai DLC but does not declare it as a dependency. PRODUCT/TYCOON do not depend on one another and do not require CORE. References and component LoadOrder are not hard enable requirements. Current DB ModRelationships matches all 11 manifests' Dependency/Reference edges. Workshop collection recommendations are not being substituted for these declarations.

CORE requires none of the three HD addons. CIV and DIST can each be switched independently while CORE remains; neither requires the other. IND can be removed while leaving Monopoly++ enabled; removing either Monopoly++ requires removing IND too. The legal economic closure is CORE+PRODUCT+TYCOON+IND. Dependency-legal does not certify all runtime compatibility or absence of undocumented assumptions.

## Actual component scope

|Alias|Scope observed in manifest/files|Isolation meaning|
|---|---|---|
|SPC|Gameplay + UI + SQL; declares only official expansions|BASE negative observation is a zero-city diagnostic scope, not a vanilla-supported full game; HD-dependent functionality is not certified here|
|BTS|InGame UI + settings database; LoadOrder8–12|Keep fixed in BASE; not frontend-only|
|EMM|FrontEndActions only: mods.lua/xml, filters/text; import9999|No declared in-game script; keep fixed|
|TITLE|FrontEndActions only; overrides mods.lua/xml at10000; text1000/10000|Requires EMM; can toggle separately; do not infer in-game event loop from its name|
|AREA|InGame XML imports only: Base/XP1/XP2 InGameTopOptionsMenu;10000–10002|Runtime menu layout, not frontend-only; no added Lua/Gameplay action|
|CORE|107 InGame DB actions, 22 ReplaceUIScript actions, 8 AddGameplayScripts actions, 6 AddUserInterfaces actions (including conditional support)|Not a passive framework: core itself has gameplay and UI behavior. Main gameplay16017/16018, UI replacement often150000|
|CIV|Database changes, many gameplay scripts, Romania/Ottoman/Songhai UI contexts|Not portraits-only and not guaranteed inert when human uses Scotland; scripts/AI content may load subject to criteria|
|DIST|InGame DB/icons/text/art; no declared InGame Lua/UI script actions; frontend imports|Database/Modifier changes can influence existing core/engine scripts; cannot rule out merely because no Lua|
|IND|Gameplay HD_CD_* and Leu_* scripts at20002; new UI contexts and overrides; DB definitions12001, updates20000+, late30001|Core economic integration; must keep both Monopoly++ dependencies|
|PRODUCT|DB500 + compatibility1000, text/art; no AddGameplayScripts|Can test alone with required official DLC|
|TYCOON|DB150/110/50 and gameplay Leu_Warehouse_Functions/Leu_Transnational_Functions; art/icons|Can test alone; gameplay code exists|

Action counts include conditional definitions, not a claim all are active in each match. File checks covered declared Files, not exhaustive external include closure. Core has two missing declared files: DrugCombat.lua has no current matching InGame action; DL_GameCapabilities.sql is under MPTest_Mode_Expansion2. Record installation caveat, do not modify/reinstall or attribute idle growth to it. Current tests should retain normal single-player settings.

## Game-mode activation boundary

User explicitly confirms prior growing 11-Mod test had Monopolies & Corporations enabled. Keep GAMEMODE_MONOPOLIES=1 and Gathering Storm ruleset throughout current trials, including BASE/core-only. IND main database/gameplay/UI actions require Monopolies_Mode_Expansion2; simply enabling its Mod while mode is OFF does not test those actions. Official installed DLC availability alone never proves match mode enabled.

## Limits / next

This audit establishes legal subsets; it does not identify a culprit. Discount C² evidence remains valid but OFF switches, added trigger counters, optimization and Batch C/D are paused. Memory and __cxa_pure_virtual crash remain separate incidents. See ../../Status/Validation/Mod_Interaction_Matrix.md for adaptive test plan and result authority.
