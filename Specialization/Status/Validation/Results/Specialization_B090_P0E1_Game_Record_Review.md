# B090.117 — single-city Game record native evidence

Three screenshots reviewed, T8, 2026-09-20 22:33:57 / 22:34:12 / 22:35:34; archived originals and SHA256 manifest alongside this report's evidence reference. No runtime change/deployment in this review.

| Stage | Visible result | Evidence scope |
|---|---|---|
| Begin | 单城实验已建立并保存到Game记录 | Startup fix USER_GAME_TEST_PASS in this scene |
| Free City transfer | DEV-B013-P0-2; origin0/131073 → current62/65536;HELD revision2;events5/saved5 | Independent Game experiment remains readable and checkpointed after transfer |
| Reload-stage | same token/refs/revision2/HELD;current events0,saved5; saved/current reference一致 | Experiment Game persistence USER_GAME_TEST_PASS for this supplied sequence; no claim of complete payload byte comparison |

GetOriginalOwner=0 is readable in both post-transfer views. GetOwnerBeforeOccupation, GetJustConqueredFrom, GetLastTransferType=UNKNOWN. UNKNOWN combines unavailable getter, exception or nonnumeric return in current diagnostic; screenshots cannot distinguish these, or prove global absence of the APIs. OriginalOwner does not establish immediately previous owner or unique city generation.

HELD is expected evidence protection, not the prior startup pause and not a write failure. The resolver requires native previous-owner corroboration; this scene does not supply it. Saved state remains HELD across reload, and old saved events are not replayed as fresh authorization. Screenshots show event counts, not full event payloads; do not infer the exact five arguments from prior B088 tests.

Conclusion: the user-proposed direction of storage independent of City Properties now has a working Game-property/save proof for this one-city Free City case. It does not require external disk files or city-name identity. No profession ledger was migrated or restored. This does not prove recapture, raze/refound, ID reuse, repeated conquest or all save branches. E1 overall identity gate stays HELD; E2/F not authorized by this result.

Next recommendation: narrowly investigate how to corroborate transfer when Gameplay previous-owner getters are UNKNOWN (distinguish API availability/return and existing event payload evidence, potentially UI read-only source). Do not silently weaken identity proof to original-owner/name/coordinate alone. No repeat of this same three-step test is needed now.
