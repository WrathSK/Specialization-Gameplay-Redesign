# Yield Precision Contract — deferred backlog

## P0-D1 user result / future Design suggestion

User reports B083 tested district primitive only settles integer additions. B084 temporarily uses floor(50% × aggregate BASE), retaining district attribution. Do not generalize to per-population or other interfaces. User suggests considering Absolute Infrastructure Depth D for this ability in a future Design review; RECORDED_ONLY / NOT_ADOPTED. Research D0031 remains unchanged; no D formula, mapping or coefficient inferred.


Document Owner: Codex
State: RECORDED_ONLY — no implementation or new investigation in B072

Future work classifies precision by interface / Modifier type / argument / settlement stage, never by a global “Civ VI supports/does not support fractions”. Existing evidence: city totals support nonintegers; fixed city yield observed1.5→1; population-based0.5 is user-verified; Copy Yield currently supports integer/0.5 construction and0.65 can raise COPY_PRECISION_UNSUPPORTED (current audit substitutes zero plan); Boost percentage has its own final floor(x+0.5) integer contract; Commerce IV deliberately floors final aggregate; Great Work flat yield has separate observed truncation. Existing accepted quantization remains unchanged. This entry does not authorize fixing/refactoring Copy Yield or changing Design.

## P0-D1 scoped investigation update

[HD policy evidence](../../Reports/Technical/HD_Policy_Fractional_PerPopulation_P0D1.md): per-population native Effect uses decimal Amount0.2/0.3/0.7 in installed policies and cache. Copy integer/half encoding is a local implementation restriction, not an engine-wide precision limit. Fixed city target mapping and exact settlement remain separate technical questions; no runtime change.
