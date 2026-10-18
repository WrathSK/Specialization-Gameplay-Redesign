# B238 — accepted Crew modifiers and Industry closeout

State: LOCAL_SIMULATION_PASS / COMBINED_NATIVE_PENDING. Source build B238.265, modinfo265. Review baseline `1c07056` / B237.264. Deployment provenance is owned by Status/Authority; this record does not assert deployment or a new native PASS.

## Decision and implementation

The user accepts native Production amplification of Crew base input for v0.1, with future empirical balance review recorded only in documentation. [D0053 acceptance](../../../Design/Design_ChangeLog.md#accepted-d0053--2026-10-18) supersedes the old exact-final-output requirement. Tier-I260, higher tiers, formation prices, start lock, source/capacity, Wonder-only targeting, one use and no-overflow rule remain. No timer, GC, event, permanent schema or formation-path change.

`UnitActions` removes the B237 pre-debit hold and restores the existing single `AddProgress(min(base, remaining))` request after validated receipt/reservation/debit and a final unchanged-target check. Native modifiers are neither inverted nor removed; errors after a possibly destructive step are held, never replayed. `CrewPrecision` preserves the typed investment receipt and distinguishes base input from actual same-target delta; target completion/change is not measured by subtracting different targets. The existing bounded collector accepts only two additional scalar keys, `baseCapacity` and `baseInput`, with unchanged budgets. No new polling or collection schedule.

Player unit/project/institution descriptions, construction preview, existing Industry reports and the direct UnitSites precision-report consumer now describe base Production and applicable modifiers; they do not predict an exact final progress or display future balance notes. New localized keys: `LOC_SPC_CREW_BASE_PREVIEW`, `LOC_SPC_CREW_BASE_CONFIRM`, `LOC_SPC_CREW_BASE_READY` in both existing languages. The obsolete hold key is removed. `IndustryWonderEffects` changes its report text only; its effect calculation is unchanged.

B237's paused order/progress implementation is inherited unchanged. Current Design/Spec/reading pages and active Architecture/plan navigation are synchronized; D0052 Spec is frozen byte-for-byte, old Content and B236/B237 results remain untouched. The current P0-H context stays scoped to CURRENT, this result, the B238 contract section and the complete Crew contract object.

## Local evidence

276 targeted tests PASS: 234 runtime/model/UI/DB tests and42 collector/diagnostic tests. Includes8 new B238 checks, restored stale-plan/receipt/debit/uncertain-grant checks, and20 B237 continuity checks.100 existing loaded speed/tier/price subcases remain covered. Actual Store/writers are exercised; the native-shaped multiplier fixture intentionally does not pretend to reproduce native overflow handling.

- Multipliers1/1.54/2 preserve a260 base request; the native-shaped result can exceed260. Exactly one unit debit/request and one slot release; repeated confirmation cannot credit again.
- Remaining100 clips the base request to100, without guessing a bonus inverse. This checks request construction only, not engine no-overflow behavior.
- Wrong target, changed progress/binding, unconfirmed receipt/debit and pre/post-grant exceptions retain rejection/no-replay protections. Old saved locked capacities are not rewritten.
- Preview has no fabricated final progress. Observer failure does not change success/receipt; changed targets produce no false delta. Final localization SQL contains applicable-modifier wording and no balance disclaimer.
- The first sandbox run passed256 tests;20 collector tests could not create their existing ignored `local/` temp directories. Those20 passed when rerun with the required filesystem access, without source/assertion changes. This was a test-environment error, not a runtime failure.

Inherited exclusions are explicit and unchanged: `test_b235_engineering.Package.test_project_and_exact_files` and `test_investment_update_propagation.InvestmentPropagation.test_syntax_package_and_unchanged_contracts` are historical package-stamp checks; `test_actual_construction_team_transport_remains_unscoped` assumes the superseded ordinary-building Crew target. They are not included in276; current package/static checks replace only the obsolete package expectation. No unrelated assertion was weakened.

Static checks:237 package files, reviewed Lua/JSON/XML syntax, active Markdown targets/anchors, current context selectors and helper self-test pass. Only reviewed hashes advance. Main, frozen prior records, Store, Crew prices and GC remain unchanged.

## Inherited native evidence and limits

[B236 native review](Specialization_B236_Native_Review.md) preserves user-confirmed slots/release, IV entry, new-price Practice and template-holder distinction, plus observed amplified use/no-overflow in that session. The amplification formerly failed D0052; the recorded observation is unchanged and its rule compatibility changes only under D0053. B237 continuation and the restored B238 action still need the combined acceptance below. Local tests do not establish native performance, an exact stacking formula or universal overflow behavior.

## One combined B237/B238 acceptance

Use the existing Industry campaign and manual collector; no new campaign, broad lifecycle retest or repeated screenshots are requested. Report-only checks use **工业历史 / 模板**; unit actions use **施工** then **确认施工**.

1. **Keep unfinished work.** Start a new **组建一级施工队** and accumulate nonzero progress. Switch to an ordinary production target and cross the next existing工程实践 threshold (N1/3/6) through a Wonder completion. Reopen production: the old **（续建）** entry must retain its locked price and progress; a fresh future order quotes the new price. If a threshold is already available during ordinary play, use it instead of constructing several extra Wonders.
2. **One cold-load, two pending questions.** Resume that old entry, save while unfinished, fully restart once and finish it. Confirm its progress/price survived, the unit has its correct source and260 base capacity at Standard speed, and the source count is correct. A surviving Crew may share this save to check its pending bound-unit recovery. Glance at Industry III/IV institution text here; no separate UI session.
3. **Restored normal construction.** On a legal own Wonder, use **施工 → 确认施工**. The unit is consumed once and releases its slot; applicable modifiers are allowed. Prefer a nearly completed Wonder so the same operation can check that the next target does not inherit Crew surplus. Logs record requested base and any reliable same-target delta; no expectation of exactly260 final progress and no need to isolate the whole modifier formula.
4. **Only if readily available:** let an enemy contact another surviving Crew; verify protective retreat rather than capture/Owner conversion and that the living Crew still occupies its source slot. Otherwise record protection as still pending and combine it later; do not force a separate setup.

Each step addresses a changed/pending Crew boundary. Previously accepted support, N/E/L, Gold quotes, Macro arithmetic and template-source rules are inherited. No per-turn screenshot series, unrelated Culture test, new long memory run or repeated save/load cycle.

## Industry completion assessment

The main Industry chain is implemented: support/II, typed templates/N/E, III Standardization, IV study/enhancement/Macro, Practice, paid source-bound Crews and institutions. It is **not yet all-native-accepted**: B237 continuation, cold unit/order recovery and deferred protection remain as above.

The user explicitly classifies **purchase discounts on the District body itself** as a rare, nonblocking v0.1 deferral. That writer is not implemented; it is not an unaccepted finished feature. Building purchase discounts and District construction acceleration are separate and remain. No all-District substitute or new purchasing right is added. Faith prices/other speeds retain conditional native gaps, not mandatory new scenarios. The future Commerce Development Investment combination belongs to that writer's later integration. Original unit Owner extinction/total city destruction remain existing undefined boundaries.

Once the combined Crew acceptance passes, the implemented Industry main chain can proceed to the next authorized profession without waiting for modifier isolation, balance, District-body purchase or unrelated held Culture work. No future batch is started by this record.
