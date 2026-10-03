# Yield Precision Contract — deferred backlog

## P0-D1 user result / future Design suggestion

User reports B083 tested district primitive only settles integer additions. B084 temporarily uses floor(50% × aggregate BASE), retaining district attribution. Do not generalize to per-population or other interfaces. User suggests considering Absolute Infrastructure Depth D for this ability in a future Design review; RECORDED_ONLY / NOT_ADOPTED. Research D0031 remains unchanged; no D formula, mapping or coefficient inferred.


Document Owner: Codex
State: RECORDED_ONLY — no implementation or new investigation in B072

Future work classifies precision by interface / Modifier type / argument / settlement stage, never by a global “Civ VI supports/does not support fractions”. Existing evidence: city totals support nonintegers; fixed city yield observed1.5→1; population-based0.5 is user-verified; Copy Yield currently supports integer/0.5 construction and0.65 can raise COPY_PRECISION_UNSUPPORTED (current audit substitutes zero plan); Boost percentage has its own final floor(x+0.5) integer contract; Commerce IV deliberately floors final aggregate; Great Work flat yield has separate observed truncation. Existing accepted quantization remains unchanged. This entry does not authorize fixing/refactoring Copy Yield or changing Design.

## P0-D1 scoped investigation update

[HD policy evidence](../../Reports/Technical/HD_Policy_Fractional_PerPopulation_P0D1.md): per-population native Effect uses decimal Amount0.2/0.3/0.7 in installed policies and cache. Copy integer/half encoding is a local implementation restriction, not an engine-wide precision limit. Fixed city target mapping and exact settlement remain separate technical questions; no runtime change.

## P0-L2A — Meaning flat GreatWork接口实测与Floor方向

[B151十图](../../Status/Validation/Results/Specialization_B151_P0L2A_Native_Precision.md)：本受控Science/Gold片段路径，0.5不保留、1.5→1、4.5→4，W2仍逐件整数部分；D1下一正常回合保持。所测半点精度FAIL、整数追加可复用，非引擎全局小数限制；六yield/最终结算/倍率隔离/未知作品资格仍未通过。

用户本次明确采用意义延展Floor，位置待确认；推荐每件同yield领域合计后Floor再乘W，与逐领域或整城Floor有不同结果。正式D0029仍no-rounding，待明确口径后按既有流程同步；不能据方向许可静默选择聚合边界。只针对本能力，不扩为0.1GPP、其它专业或全局量化。下一门禁范围见[当前计划](P0_L2_Meaning.md#推荐下一切片--p0-l2b门禁原型)，不重复小数长测。
