# Carrier / Modifier Footprint Audit

Investigation / Non-authoritative / No design decision implied

Status: Stable

Maintainer: Primary; independent read-only Carrier / Modifier audit

Baseline: develop `3d0ac4b4c2b1c3d71cb46beb7d1093d191ade795`, initially clean; 2026-11-02.

Scope: source definitions, manifest loading, actual consumers and compatibility, structural scaling. No implementation, gameplay test, probe, deployment, authority edit or v3 change.

## Executive findings

**“4,000+” is a static definition subtotal, not a count of active engine effects.** The five spotlight files contain exactly **4,020 unique Modifier IDs**. Of these, **3,376 belong to retired forward-effect families with live compatibility/cleanup dependencies**, **385 are current Meaning final-value definitions**, and **259 are Meaning definitions not chosen by the current positive production writer**. None of these groups is authorized for deletion.

Across all 65 SQL files under `Mod/`, the current manifest selects **49 distinct InGame UpdateDatabase SQL files in 44 actions**. Their literal declarations contain **4,181 unique Modifier IDs and 1,790 unique InternalOnly Buildings**. Adding three catalog-independent SQL-generated families gives **4,420 Modifier definitions and 2,013 Buildings before catalog-dependent expansions**. This is a source-derived subtotal, not the final loaded database total.

The final source-generated total depends on loaded building, district, era, yield and target catalogs. Its exact algebra is recorded in the [inventory](Definition_Inventory.md). **A current effective-loaded total is NOT_CONFIRMED:** the project has no configured read-only HD database in this environment. An unrelated old application cache was not substituted. Actual active instances, resident memory and engine time are **UNMEASURED**.

The largest catalog-independent Modifier families are NetworkBoost 2,064; GreatWorkAdjacency 1,092; Meaning 644; Insights Tourism 192; and NetworkBoostInteger 180. This is not a global ranking: generated Standardization/Engineering can overtake them depending on actual catalogs.

Three structural findings deserve attention:

1. Retired implementations retain expansive positive SQL graphs, exact stable building IDs and load/withdrawal dependencies. “Retired” does not mean “inert” or “safe to remove.”
2. Probe-named files are not optional units. `CultureMeaningProbe.sql` supplies current production effects; `GovernorProbe.sql` supplies the actual ACTIVE governor facts. Production ownership must be separated before diagnostics can exit safely.
3. Current Standardization grows with targets × final levels; Great Work effects grow with object categories × represented values. These are concrete expansion mechanisms. Their contribution to current CPU/RAM problems has not been measured.

## Reading order

- [Audit report](Audit_Report.md): meaning of the counts, dependencies, native constraints, scaling, options and Owner gates.
- [Definition inventory](Definition_Inventory.md): every gameplay SQL, literal counts, generated formulas, loading contexts and bounded integrity results.
- [Reproduction and evidence limits](Reproduction_Method.md): executable read-only source parser, read-only database queries, exact baseline and validation boundaries.

Existing Architecture Reconstruction and Convergence v3 materials are untouched. This topic provides investigation evidence only; approved Architecture Markdown remains authoritative. No new implementation priority or migration order is inferred.

## Handoff

- **User decision:** none needed to receive this audit. Starting optimization, changing compatibility support or changing encoding semantics needs a separate decision as described in the report.
- **User testing:** none requested now. Existing native evidence was read, not rerun or expanded into a new PASS.
- **Primary next:** stop at this report checkpoint. A future optimization starts with an explicitly supplied current HD database and one reviewed family, not bulk deletion or a new global architecture.
