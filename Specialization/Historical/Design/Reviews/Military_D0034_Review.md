# Military D0034 — Comprehensive Training depth amendment

Document Owner: Codex
Design Authority: User
State: DESIGN_FROZEN core structure / explicit BALANCE_DESIGN_DETAIL_REQUIRED
Date: 2026-09-20

[Military_D0034](../../../Design/Content/Military_D0034.json) replaces Military_D0033 as current content. D0033 JSON/review and the exact previous Spec snapshot remain historical. Only 综合训练 is expanded; six named abilities, all names, other Military contracts and other professions retain their rules. No implementation, Architecture adaptation, deployment or P0 scope expansion.

## Accepted structure

Breadth: same five domains (Campus/Theater/Industrial/Commercial/HolySite), actual eligible ordinaryT1 gives permanent birth+1CS per domain, maximum5. Existing acquisition/provenance and per-ability formation inheritance remain. Depth never grants extra CS.

Depth: the same domains' Shared absolute infrastructure D contributes to this city's military training efficiency. D is actual weighted eligible infrastructure, not relative completion. The existing min(10,sum Tier1/2/3/4 weights), exclusions, pillage rules and highest single district per domain apply. Cross-domain aggregation is NOT decided by that within-domain maximum.

| Normal chain | D | Quality/domain | Depth efficiency |
|---|---:|---:|---|
| No ordinary buildings | 0 | 0 | None |
| T1 | 1 | +1CS | None/not started |
| T1+T2 | 3 | +1CS | Begins |
| +T3 | 6 | +1CS | Higher |
| +T4 | 10 | +1CS | Further increase |

This table freezes structural ordering, not Production percentages or an executable threshold. A complete three-tier chain can provide meaningful efficiency atD6; an additional fourth tier may provide more atD10. No100%-built requirement, environmental normalization to10 or new relative Shared metric. This resolves the Military consumer's absolute-versus-relative choice without declaring all other consumers' reviews finished.

Five T1-only domains can produce+5CS without depth benefit; three deep qualified domains produce+3CS with greater efficiency. Five deep domains may combine both at high city-development cost. Neither five domains nor full development is a minimum. Standard six-population-limited-district/16-population example is not an additional hard predicate.

## Deferred details — do not silently fill

Coefficient/Production conversion, linear/discrete/diminishing curve, per-domain contributions versus total-D mapping, cap, speed scaling, equality across military classes, Gold/Faith purchase applicability. Exact onset predicate and nonstandard building arrangements (onlyT2/onlyT3/same-tier multiples) require detail before implementation; D≈3 examples do not automatically settle them. Whether T1 quality qualification also gates depth is not independently confirmed. These are explicitly deferred design details, not newly imposed freeze blockers.

Confirmed purchase eligibility concerns permanent quality buffs. It does not authorize a purchase discount or faster purchase mechanism. Likewise permanent unit-snapshot/formation-max rules concern awarded unit buffs; local training efficiency is not a post-birth unit benefit. The two layers share an ability, not an implementation or persistence rule.

No formula, modifier, stacking math, new carrier, exact value or extra ability is chosen. Research/Industry/Culture/Commerce and Shared_D0028 bytes remain unchanged. Existing Military frozen-core status is retained with these visible implementation prerequisites.

## Review / evidence / workflow

Document structural/JSON/reference/hash checks only; no Gameplay simulation or game PASS. Published D0033 hashes remain untouched; new Spec/Military hashes recorded in ChangeLog. Workflow navigation points to D0034; old P0 context remains explicitly stale, not automatically rehashed. A0161 is still adapted throughD0032, not newly adapted to Military. Stop after docs commit/push; no user test.
