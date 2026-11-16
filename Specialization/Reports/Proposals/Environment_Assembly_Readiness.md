# Environment assembly readiness — official / pinned HD

Primary candidate / 2026-11-07 / source `292240f` / D0059, A0184, S0907.
This scoped preparation follows the existing integrated roadmap §6 (A21–A26, O5a before O1). It is not a replacement plan or an implementation authorization. No runtime, Design, Architecture, test code, deployment or game configuration changed. The Owner authorized preparation and removal of the Leugi dependency; migration implementation remains at its review gate.

## Owner review

The independent official DB and accepted HD DB now support a concrete assembly proposal. The main remaining semantic boundary is a real fifth-level Campus building against the existing four-level consumer range. Definitions and art dependencies are identifiable; runtime equivalence and adapted no-HD behavior have not been tested.

Recommended first implementation slice: environment selection, owned schema/wrapper definitions, explicit final-data assembly ordering and Leugi art removal. Do not activate a partially migrated provider for production. O1 must then consume the common catalog through the existing shared-fact contract. UI-base assembly and callback adaptation retain their O5/O6 gates; this first slice alone is not a deployable no-HD package.

## Evidence and reproducibility

| Profile | Frozen identity | Gameplay DB SHA256 | Observed rows |
|---|---|---|---|
| Official | S0907 external `HD_Free_Baseline_2026-11-07/Capture_Official_Only`; 25 actual official Gameplay targets; no HD/SPC/Leugi | `a37e505731f433bbaf2507ec4cf1f0867019813d645c8c7943c3ceae1691bb32` | 138 Buildings; 84 BuildingPrereqs |
| HD comparison | S0903 `B413_HD_Baseline_20261106`; 94 actual Gameplay targets, including the fixed HD/UC extensions | `d483b5f2848907329b8439dc257c061ea285c4b90a88c22bdb792f0e4ab42439` | 4,888 Buildings; 348 BuildingPrereqs; includes internal SPC carriers |

Both immutable read-only DBs pass `quick_check`; no prerequisite references a missing Buildings row. This does **not** prove every edge represents a genuine upgrade, or that all future content is covered. Official and HD row counts are not performance comparisons.

Portable extraction (Python standard library; explicit snapshot paths):

```sh
python3 tools/inspect_environment_inputs.py --official-db "$SPC_OFFICIAL_DB" --hd-db "$SPC_HD_DB" --output "$SPC_EVIDENCE_DIR/assembly-inputs.json"
```

Use a new output filename. The tool refuses overwrites, checks source hashes before/after, checks required tables, and emits source rows, replacements, prerequisite relations and wrapper definitions. It does not assign Tier or certify native behavior. Repeated extraction produced identical SHA256 `2bc8ca3b6ffaef474fde16688a5f17e635490d79b4df6ed0a2da1302657a233e`. Detailed regenerable output stays outside Git; raw source archives remain unchanged. Local paths are resolved by the S0903/S0907 archive manifests. This is not a new permanent-backup claim.

## Exact chain findings

These are interpretations of the pinned rows under accepted N1/N2, not changes already made to the running game. Parallel alternatives establish the same position; they are not added together.

| Building / family | Official | Fixed HD | Consumer impact / disposition |
|---|---|---|---|
| Market → Bank → Stock Exchange | T1 → T2 → T3 | T2 → T3 → T4, following Fair / Waystation T1 | Expected environment difference. Preserve actual chain and D6/D10 rules. |
| Library → University → Research Lab | T1 → T2 → T3 | Library/Academy T1 → University/School T2 → Architecture/Laboratory/Liberal Arts/Real Academy T3 → Research Lab/Education T4 | Branch predecessors agree; no four independent increments. |
| `BUILDING_HD_DATA_CENTER` | Absent, not an error | Research Lab or Education T4 → **T5**; old HD table says T4 | Real supported building beyond OrdinaryBuildingCatalog's 0–4 guard. Do not clamp to T4. See bounded decision below. |
| `BUILDING_JNR_HOSPITIUM`, `BUILDING_JNR_GARDEN` | Absent | Alchemy Room/Monastery/Stave Church/Temple T2 → **T3**; old HD table says T4 | HD's explicit Holy Site bump is not an upgrade edge. Use T3 under N2; explain changed D/template grouping rather than demand old-value equality. |
| Industrial Water Mill → Workshop → Factory | Workshop T1 → Factory T2 | Water Mill/Wind Mill T1 → Workshop/Manufactory T2 → Factory T3 | Water Mill's Mill Race/River gates do not increase Tier (Owner N1). Preserve explicit positive classification. |
| Mansion | Absent | T1; Palace prerequisite belongs to City Center | Unlock condition, not a Neighborhood upgrade. |
| Sewer | City Center | Aqueduct | Existing ordinaryOnly map fixes Aqueduct. Environment-aware location mapping is necessary, but must not silently turn an ordinary-depth-unreviewed building into a D contributor. |
| City Center buildings | Individual prerequisites vary | Legacy Tier0, including independent branches | Do not number every center prerequisite as a regional upgrade chain. Preserve separate center grouping and development target policy; Palace/walls must not become D contributors by graph inference. |

A diagnostic walk found no unequal branch depths or unresolved replacement edges in the inspected 58 loaded named/replacement candidates in the official DB and 162 legacy-HD-catalog rows. That is a limited graph observation, **not** complete ontology/edge validation. The source named-depth whitelist has 123 IDs, many absent legitimately in the official environment. Unknown Mod buildings are not automatically admitted.

Source anchors: `Mod/OrdinaryBuildingCatalog.lua:203–258` (HD reads, 0–4 guard, ordinaryOnly map); `Mod/DistrictCompleteness.lua:17–50` (actual contributions/cap10); `Mod/ResearchChairModel.lua:21–29`; `Mod/Standardization.lua:24,68`; `Mod/StandardizationEffects.lua:136`; `Mod/DevelopmentInvestmentTargets.lua:19`. ENV-20261104, Workshop2465378070 `UpdateDataBase/HD_BuildingTiers.sql:16–25` explains old center0 and Holy Site bump. Its bounded updates are not a general graph solver.

### Bounded Owner decision: fifth-tier support

Shared_D0059 retains an explicit weight list 1–4 while its general formula sums actual Tier. The effective chain now establishes T5. Recommend explicitly supporting T5 as weight5, retaining `D=min(10,sum(Tier))`, all current eligibility/pillage rules and no new effect formula. This avoids either silently capping the building or publishing an incomplete D. Do not implement this range expansion until the Owner confirms the boundary.

Research_D0059 `RES_L4_CHAIR` explicitly covers ordinary **T1–T4** buildings. Keep that rule: T5 Data Center would receive no Chair bonus, though it can contribute to D and remain an ordinary building. Extending Chair to T5 is a separate gameplay change and is **not proposed**. Standardization grouping uses actual Tier, and Development targets use the lowest eligible candidate Tier; both require regression with the new value. Existing saved learned-template receipts compare district/Tier with the catalog and can reject changed classifications. Use the agreed new-save test boundary; do not rewrite old receipts or promise cross-build save compatibility.

## Proposed assembly slice

1. **Explicit profile selection.** Reuse evidenced ModInUse component criteria for official/HD variants. A single SPC-owned assembly/version marker records the selected provider. Require exactly one selected profile; no selection by HD table presence, and no presumed Gameplay Modding API.
2. **Common owned inputs.** Define compact owned catalog output/schema and the three wrappers below. Preserve separate ordinary/D eligibility, Standardization grouping and Development eligibility; a shared Tier source does not unify those business policies. Non-applicable, unavailable and malformed chains remain distinct.
3. **Final content ordering.** Candidate bands: common definitions 10003000; selected environment input 10003010; final catalog assembly 10003020; affected target/carrier generators 10003100+. These follow the inspected HD late support at10000000. Validate against the complete fixed active profile before choosing final numbers; equal-order components must not carry hidden dependencies. Refuse an incomplete assembly rather than silently proceeding.
4. **Split target generation from unconditional definitions.** `DevelopmentInvestment.sql:3–7` currently joins missing HD tables, whereas its access/project definitions at15–20 are common. Do the same separation for `StandardizationDiscount.sql:3–8`. Migrate the three Lua catalogs to the same owned result in O1, not to separately inferred UI tables. Retain existing carrier IDs and modifier arithmetic.
5. **Final cleanup definitions.** Move `InternalCarrierPillage.sql` after the last carrier generator (candidate10004000). Its current10002000 would run too early if generators move. Verify every internal SPC building has Pillage0 in each resulting DB. Retain existing exact exit ownership and fail-safe startup dependency handling; no second cleanup list.
6. **No premature runtime switch.** Current official UI replacements still depend on five HD bases and GetDataHelper. Selected official bases, actual callback signatures and mandatory cleanup must be ready before the separate fixed no-HD smoke. No default entry is declared READY merely because a marker/schema exists.

| Existing HD-only ModifierType | SPC-owned replacement must retain Collection / Effect |
|---|---|
| `MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST` | `COLLECTION_OWNER` / `EFFECT_ADJUST_BUILDING_PURCHASE_COST` |
| `MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE` | `COLLECTION_CITY_DISTRICTS` / `EFFECT_ADJUST_DISTRICT_YIELD_CHANGE` |
| `MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION` | `COLLECTION_OWNER` / `EFFECT_ADJUST_DISTRICT_PRODUCTION` |

All three names are absent from the official DB and present in the HD DB. Define distinctly SPC-owned wrapper names; verify the underlying primitive definitions and every referencing ModifierType in both assembled profiles. Presence is not proof of successful native effect execution. No copying HD base economy or specialist GPP into core.

## Leugi removal within the same assembly scope

The Owner explicitly withdrew retaining Leugi art (S0907). Remove all four dependency surfaces together after approval of the implementation slice:

- `SpecializationP0.modinfo` required Leugi UUID;
- `Specialization.dep` MonopolyPlus RequiredGameArtID;
- `ArtDefs/Units.artdef` Leu_Investor member and related references;
- `Data/Icons.sql:83–87` Investor fallback aliases, checking portrait/flag variants even where RawIcons overrides the main image.

Recommended official replacement: **modern Great Merchant** member `Great_Merchant_Male_Modern`. The installed Base `ArtDefs/Units.artdef` has a matching `UNIT_GREAT_MERCHANT_MALE_MODERN` entry, member and `GreatMerchantModern` audio, not merely a guessed asset name. Keep SPC unit identity, statistics, abilities and accepted custom icons; borrow only official visual/audio definitions. Use verified official fallback portraits/flags for uncovered icon variants. This is a candidate, not a rendered appearance acceptance. Do not redistribute official asset binaries. BTS has no current manifest/direct runtime dependency; keep its compatibility separate from core requirements.

## Gates and next authorization

Completed **STATIC_CONFIRMED**: pinned DB integrity, raw relation extraction, direct HD table dependencies, wrapper-name absence/presence, inspected art references and current load-order hazard. Extractor determinism/input immutability and failure guards were checked locally. No migrated SQL/provider or native effect was executed; existing HD gameplay acceptance is carried forward only within its original scope.

Before completing implementation:

- Profile-specific assembly in disposable copies from the independent DBs, with a faithful selected-component order. The HD final DB already contains SPC; do not replay duplicate generators on it and label that a fresh install. Define a controlled input fixture/reconstruction with explicit exclusions and compare to the frozen reference.
- Validate roots, equal-depth alternatives, replacements, N1 virtual gates, cross-district gates, missing/cyclic/unequal inputs and supported Tier ranges. Preserve consumer-specific ontology. Tests must exercise actual provider+consumer combinations, not only a graph helper.
- Check all SPC modifier references, generated target coverage, marker uniqueness, no HD-only JOIN in official selected path, final Pillage0 closure and HD-independent exit registration.
- Preserve source/runtime behavior for contracts, receipts, network pending semantics and irreversible actions. Do not integrate O2–O7 in this slice.
- After environment/UI assembly is complete: Owner-run fixed no-HD smoke and targeted UI/effect/cold-load/exit/irreversible-operation checks, against this official environment plus the adapted SPC build. Existing HD profile remains the regression comparison. No test now; no game launch or deployment authorized here.

**User decision:** confirm the bounded fifth-tier treatment and next assembly implementation scope; confirm modern Great Merchant as the replacement visual if acceptable. **User testing:** none now. **Primary next:** after approval, synchronize only the necessary accepted boundary and implement the reviewed first assembly slice; continue to its existing audit/native gates.
