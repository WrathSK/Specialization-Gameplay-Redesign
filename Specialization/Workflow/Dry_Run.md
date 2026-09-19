# W0001 P0-B1 context dry-run / workflow validation

Date: 2026-09-18. Baseline cb5a3d48f18640d254f45a2af24f84bc2b2bb062.
Result: CONTEXT_VALIDATION_PASS. No P0-B1 implementation, gameplay test or engine PASS.
Design D0032 / Architecture A0161 / develop B077.104 unchanged. Status S0203 records workflow only.

## Reproducible measurement

Run from repo root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Workflow/context.py check P0-B1
PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Workflow/context.py self-test P0-B1
PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Workflow/context.py plan P0-B1
PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Workflow/context.py read P0-B1 11
```

| Text context proxy | Files | Projections | Bytes | Lines |
|---|---:|---:|---:|---:|
| Broad reference read-set | 166 | full files | 3577637 | 37848 |
| P0-B1 progressive read-set | 43 | 53 | 299418 | 4439 |

Text bytes reduced **91.6%**. Broad set is explicitly defined in context.py: all Mod, top-level v2 documents/inventory, current authority files, governance, full Status/ChangeLog, playtest contract and two relevant tests; deduplicated. It is NOT a measurement of an earlier conversation or actual token bill. It excludes historical Design Revisions, so does not inflate savings with archives. Proposed count includes governance, workflow/manifest overhead, whole direct source and two tests, including repeated JSON envelope metadata.

Hash verification still reads all125 Mod files and59 context files from disk; it emits only mismatches/totals. Savings concern text ingestion and repeated semantic review, NOT claiming zero byte I/O. Full source audit/required regression at future cutover has additional cost deliberately excluded from this start-context comparison. Unrelated file changes cause safe escalation rather than silently retaining the low count.

## Actual context acquisition dry-run

All53 projections were resolved/extracted in memory by check/plan; current revision headers, JSON effect IDs, unique Markdown sections/rows, file sets and hashes passed. This validates context availability, not future implementation quality. Reading sequence:

1. Governance/Authority/current Status and metadata; confirm batch authorization separately.
2. D0032 acceptance + content schema; each profession current base_effects; Industry approved support parameters; Shared eligibility/ontology; Spec participation/terms/progression.
3. A0160 State/Shared/Performance; exact B1 row + common acceptance; migration and writer retirement; actual P0-A/C2/D2 evidence; TS19 and playtest contract.
4.17 direct runtime files, including active writers, Industry producer/lifecycle, Gameplay dispatch, native wrappers, SQL carrier definitions and modinfo.
5. Current P0-A and D2 composite tests for verification planning. No test runs from the reader.

Not loaded by default: Research/Culture/Commerce entire higher-level abilities; future professions; historical Design revisions; B069 Source_Index/Event_Catalog; all unrelated runtime source; HD asset trees; old screenshot/log archives; full Status history. Current references/unknown semantics can still expand any of these when required.

P0-B1 is a writer retirement batch: at implementation start additionally search all Mod for `Lv3Support` and every fixed/Gold carrier ID and attachment, inspect all callers and preserve unaffected writers. This bounded identifier search is mandatory and is NOT an all-file full-text context dump. Unknown writers or unbounded dependency expansion escalate; actual cutover requires full regression.

## Ordered read ledger

All paths repository-relative; selectors/why are in P0-B1.json. Use zero-based N with read command.

| N | Path | Projection | Bytes |
|---|---|---|---:|
| 0 | `AGENTS.md` | full | 4037 |
| 1 | `Specialization/AGENTS.md` | full | 8239 |
| 2 | `Specialization/README.md` | full | 3232 |
| 3 | `Specialization/Workflow/README.md` | full | 10564 |
| 4 | `Specialization/Workflow/Authority.json` | full | 2093 |
| 5 | `Specialization/Workflow/P0-B1.json` | full | 14373 |
| 6 | `Specialization/Status/Specialization_P0_Status.md` | head | 2176 |
| 7 | `Specialization/Architecture/Specialization_v0.1_Architecture.md` | head | 1407 |
| 8 | `Specialization/Design/Specialization_v0.1_Design_Spec.md` | head | 558 |
| 9 | `Specialization/Design/Design_ChangeLog.md` | section | 1589 |
| 10 | `Specialization/Design/Content/README.md` | full | 4476 |
| 11 | `Specialization/Design/Content/Research_D0031.json` | json | 1293 |
| 12 | `Specialization/Design/Content/Industry_D0032.json` | json | 1694 |
| 13 | `Specialization/Design/Content/Culture_D0029.json` | json | 1060 |
| 14 | `Specialization/Design/Content/Commerce_D0032.json` | json | 940 |
| 15 | `Specialization/Design/Content/Industry_D0032.json` | json | 542 |
| 16 | `Specialization/Design/Content/Industry_D0032.json` | json | 557 |
| 17 | `Specialization/Design/Content/Shared_D0028.json` | json | 611 |
| 18 | `Specialization/Design/Content/Shared_D0028.json` | json | 933 |
| 19 | `Specialization/Design/Specialization_v0.1_Design_Spec.md` | section | 5366 |
| 20 | `Specialization/Design/Specialization_v0.1_Design_Spec.md` | section | 1515 |
| 21 | `Specialization/Design/Specialization_v0.1_Design_Spec.md` | section | 8824 |
| 22 | `Specialization/Architecture/v2/D0032_Adaptation.md` | section | 3431 |
| 23 | `Specialization/Architecture/v2/D0032_Adaptation.md` | section | 3561 |
| 24 | `Specialization/Architecture/v2/D0032_Adaptation.md` | section | 1961 |
| 25 | `Specialization/Architecture/v2/D0032_Implementation_Plan.md` | rows | 944 |
| 26 | `Specialization/Architecture/v2/D0032_Implementation_Plan.md` | section | 1914 |
| 27 | `Specialization/Architecture/v2/D0032_Implementation_Plan.md` | section | 2051 |
| 28 | `Specialization/Architecture/v2/D0032_Runtime_Archaeology.md` | rows | 2020 |
| 29 | `Specialization/Architecture/v2/P0_A_District_Completeness.md` | full | 10869 |
| 30 | `Specialization/Architecture/v2/Batch_C2_Copy_Industry_Lifecycle.md` | full | 10507 |
| 31 | `Specialization/Architecture/v2/Batch_D2_Runtime_Propagation.md` | full | 13191 |
| 32 | `Specialization/Architecture/v2/D0032_Technical_Spikes.md` | rows | 354 |
| 33 | `Specialization/Architecture/Playtest_Workflow.md` | full | 4899 |
| 34 | `Mod/ResearchSupport.lua` | full | 5963 |
| 35 | `Mod/IndustrySupport.lua` | full | 5445 |
| 36 | `Mod/Lv3Support.lua` | full | 5232 |
| 37 | `Mod/CurrentSpecializationFacts.lua` | full | 498 |
| 38 | `Mod/EffectiveFacts.lua` | full | 3775 |
| 39 | `Mod/RuntimeWork.lua` | full | 2292 |
| 40 | `Mod/SampleLifecycle.lua` | full | 6624 |
| 41 | `Mod/OrdinaryBuildingCatalog.lua` | full | 9101 |
| 42 | `Mod/DistrictCompleteness.lua` | full | 7328 |
| 43 | `Mod/Gameplay.lua` | full | 25001 |
| 44 | `Mod/Probe.lua` | full | 28468 |
| 45 | `Mod/UI/IndustryRefresh.lua` | full | 3657 |
| 46 | `Mod/Data/ResearchSupport.sql` | full | 660 |
| 47 | `Mod/Data/ConstantSupport.sql` | full | 853 |
| 48 | `Mod/Data/IndustrySupport.sql` | full | 4061 |
| 49 | `Mod/Data/Lv3Support.sql` | full | 5741 |
| 50 | `Mod/SpecializationP0.modinfo` | full | 16253 |
| 51 | `DevelopmentTests/test_p0_a.py` | full | 19830 |
| 52 | `DevelopmentTests/test_arch_v2_d2.py` | full | 16855 |

## Self-test / red-team result

Nine fault/positive cases PASS: stale manifest authority; missing writer gate; invalid heading; invalid JSON Pointer; stable ID mismatch; path traversal; absolute path; changed/new/deleted-file comparison; valid current manifest and selectors. Faults are in-memory only, no repository mutations. No gameplay tests executed, no disk writes from context.py.

Manual review confirms limits: hidden/dynamic dependencies and an incorrect historical summary cannot be proven absent by hash; writer search, source review and regression remain required. Both unchanged source and changed dependencies force consumer review. Hash renewal requires reviewed diff, never an automated refresh command. Computer Use remains UNRESOLVED / DEFERRED.

## Maintenance handoff

Workflow modifies only its directory, Status current navigation/S0203 and v2 README navigation. Existing Architecture/Design meaning is unchanged. Original B076 inventory stays frozen; Runtime_Index links114 unchanged inherited files and11 P0-A delta files to their evidence. Existing entry README stale D0025 text is explicitly warned about rather than rewritten outside this authorized scope.

Suggested future user request: **授权 P0-B1，按 W0001 与当前 manifest 执行，完成 commit/push 后停止；不部署。**

Next action: stop and await P0-B1 authorization. No P0-B2/C or Computer Use continuation.
