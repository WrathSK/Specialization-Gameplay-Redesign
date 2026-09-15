# Yield Precision Contract — deferred backlog

Document Owner: Codex
State: RECORDED_ONLY — no implementation or new investigation in B072

Future work classifies precision by interface / Modifier type / argument / settlement stage, never by a global “Civ VI supports/does not support fractions”. Existing evidence: city totals support nonintegers; fixed city yield observed1.5→1; population-based0.5 is user-verified; Copy Yield currently supports integer/0.5 construction and0.65 can raise COPY_PRECISION_UNSUPPORTED (current audit substitutes zero plan); Boost percentage has its own final floor(x+0.5) integer contract; Commerce IV deliberately floors final aggregate; Great Work flat yield has separate observed truncation. Existing accepted quantization remains unchanged. This entry does not authorize fixing/refactoring Copy Yield or changing Design.
