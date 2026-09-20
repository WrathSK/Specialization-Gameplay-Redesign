# Yield Precision Contract — deferred backlog

Document Owner: Codex
State: RECORDED_ONLY — no implementation or new investigation in B072

Future work classifies precision by interface / Modifier type / argument / settlement stage, never by a global “Civ VI supports/does not support fractions”. Existing evidence: city totals support nonintegers; fixed city yield observed1.5→1; population-based0.5 is user-verified; Copy Yield currently supports integer/0.5 construction and0.65 can raise COPY_PRECISION_UNSUPPORTED (current audit substitutes zero plan); Boost percentage has its own final floor(x+0.5) integer contract; Commerce IV deliberately floors final aggregate; Great Work flat yield has separate observed truncation. Existing accepted quantization remains unchanged. This entry does not authorize fixing/refactoring Copy Yield or changing Design.

## P0-D1 scoped investigation update

[HD policy evidence](../../Reports/Technical/HD_Policy_Fractional_PerPopulation_P0D1.md): per-population native Effect uses decimal Amount0.2/0.3/0.7 in installed policies and cache. Copy integer/half encoding is a local implementation restriction, not an engine-wide precision limit. Fixed city target mapping and exact settlement remain separate technical questions; no runtime change.
