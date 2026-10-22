# B240 — Commercialization D0055 implementation

Date: 2026-10-18. Source basis: `57e8f91`. Build: B240.267 / modinfo267.
Evidence: STATIC_CONFIRMED + LOCAL_SIMULATION_PASS. USER_GAME_TEST_REQUIRED for this delta.

## Scope and cause

The user authorized [D0055](../../../Design/Content/Commerce_D0055.json) source Identity/Harbor total Food implementation, removal of repeated old Gold sampling, and the previous local-prerequisite UI correction. No new Design decision is made here.

B239 sampled Harbor from city Gold after temporarily removing owned Commercialization Gold, then restored it. That write/read/write phase repeated even with unchanged inputs and could generate another deferred native yield notification. The user's repeated building flash/sound report and old COMMERCE_CLEAN records are preserved in the [B239 review](Specialization_B239_Native_Review.md); the actual old Lua counterexample made40 carrier writes across10 unchanged updates. This explains a concrete repeated-write path, not every possible native delay or allocation.

D0055 removes the need for that phase: all five source yields are non-Gold. External sources also now require the matching specialization Identity; self remains exempt and must still have the local domain district.

## Implementation and ownership

- `Mod/Commerce.lua`: use Store.Owns/Base plus the existing implemented P.Family mapping for external Identity, with one-batch identity reuse. Preserve verified direct-route endpoints, UNKNOWN and reverse dependencies on currently ineligible partners. No remote ACTIVE/Governor/Potential or building scan is added.
- `Mod/CommerceCalculation.lua`: Harbor maps to total Food, never surplus. The formula, domain Floor then sum, selection/order, capacity and effective Reputation are unchanged.
- Existing owned Gold writer now changes only differing bits. Startup reconstruction, real-input updates, source loss, unavailable facts, legacy retirement, error readback and confirmed exit retain their existing exact cleanup responsibilities. No foreign consumer's effects are removed for sampling.
- `Mod/UI/CommercePanel.lua`, `Mod/Text/Commerce.sql` and the existing P0 Describe function explain missing local districts, show all five fields and label Harbor Food. P0 COMMERCE_READ consumes the published state without recomputation; the production-list action remains the configuration entry.
- Localization keys added: `LOC_SPC_COMMERCE_LOCAL_DISTRICT_REQUIRED`, `LOC_SPC_COMMERCE_NO_SOURCE`, `LOC_SPC_COMMERCE_SOURCE_IDENTITY_UNKNOWN`, in the existing two locale rows. No new icon/layout asset.
- No new persistence, timer/frame handler, GC strategy, source topology or Gameplay rule. Store, common Network, Industry, other professions and the original evidence are unchanged. Holy/Harbor external profession sources remain unavailable until their actual Identity is implemented; self Faith/Food remains legal.

## Targeted local results

109 distinct tests PASS, no failures/errors/skips:

- `DevelopmentTests/test_b240_commerce.py`: wrong/missing/unreadable Identity; no external ACTIVE/Potential/district requirement; source exit/re-entry/Owner loss; once-per-batch reads; total Food instead of Gold/surplus; true same-turn changes; zero/recovery; no sampling writes to another Commerce city; readable prerequisites and P0 read-only behavior.
- Existing `test_b239_commerce.py`, `test_b239_commerce_ui.py`, `test_b239_commerce_store.py`, `test_b239_commerce_network.py`, `test_b239_commerce_integration.py`: actual Lua writer, Store model/persistence, verified direct-route transport, view/selection protocol, exact legacy cleanup and loaded SQL in a read-only database copy.
- Three old clean-Gold algorithm tests are superseded by D0055 counterexamples; unknown owned-carrier cleanup remains explicitly guarded and tested. Frozen B239 results are not rewritten.

After initial output is installed,10 unchanged updates make **0 carrier writes**;10 P0 reads make **0 extra source-yield reads and 0 writes**. Deferred yield/building echoes drain without a further write; a real same-turn Food20→40 change still updates the result. This proves the local write behavior, not native CPU/memory improvement, absence of every flash or actual engine Gold settlement.

Reproduction uses the repository's existing Lua runtime/test setup and explicit read-only `SPC_DEBUG_GAMEPLAY_DB`. Ignored local summaries: `local/diagnostics/B240/local-checks.json` (109 test IDs/outcomes) and `static-checks.json` (syntax/links and actual old/new writer comparison). The comparison script is retained there as `reproduce_checks.py`; these are local evidence, not public native logs.

## One minimal native flow

Use a Commerce ACTIVE III/IV city with working Commercial specialists and a completed Harbor. Keep the normal collector running manually; use the existing campaign/setup and no unrelated new long test.

1. Open **城市生产列表 → 商业化 / 商业信誉**. Missing local domains should say **本城缺少对应区域**; the P0 **商业化 / 商业信誉** report should also explain the five fields and where configuration lives. This closes the previously observed grey-button/empty-report ambiguity.
2. Enable **港口 · 粮食价值**. Compare X with the source city's total Food, not net surplus, and the domain result with `Floor(0.05 × D × X × (1 + 0.005R))`. Compare native Gold before/after with other inputs held fixed; existing city multipliers may apply. Leave it on while interacting normally: repeated source-building flash/sound should stop.
3. If the existing setup has a directly connected Research/Culture/Industry city, enable that domain too. The source must be the largest eligible value among self and matching-Identity direct partners; unrelated high-output cities cannot win. Change one relevant worker allocation or complete one building; the current formula should refresh without reopening P0. For Harbor, a Food allocation change is enough to verify the new input/update path.
4. Disable that field and check its Gold contribution is withdrawn, with other fields preserved. Complete the previously pending Commerce configuration/Reputation save/cold-load check once: selection/order and history remain, effects rebuild from current facts. This is inherited unfinished B239 evidence, not a new B240 save mechanism or another Academic Tradition test.

Prefer captured COMMERCE_DOMAIN/current-state logs. A report's planned Gold does not prove actual native Gold; one yield comparison/screenshot is useful if the observed result disagrees. Do not repeat accepted Crew occupancy or old Probe default-OFF/exit/re-enable sequences. Keep source-yield/UI observations separate from actual yield arithmetic.

## Checks and stop

Targeted local tests are complete. Final local checks PASS: four changed Lua files compile, modinfo267 references resolve, all18 added/changed Markdown links/anchors resolve, and current context/hash plus selector self-tests pass. The current manifest reads only3 projections/41 lines. Staged publication and deployment are separately gated; W0003 exit/hash/clean-source checks remain mandatory. No native PASS is claimed here. Capital, Development, Restructuring and Culture HOLD are not started. User decision: none for B240. User testing: the flow above. Primary next: review its result, then stop or prepare the separately authorized next batch.


## Verified deployment checkpoint

Clean source commit `81efaa995c02eb16e3ba41b7b6f88d724a596607` was committed and pushed before W0003 deployment. Fresh automatic process checks confirmed game exit at both the exact B239 receipt restore and B240 activation.245/245 files MATCH, digest `903a0897142582bb338f868805a664eec38e14768fa3467834245ce542ec86c7`; receipt `B240.267-81efaa9-playtest.json` is DEVELOP_ACTIVE. B239/stable recovery remains intact; no pending transaction. Main remains `e901a22`/B069.96. Staged publication passed for18 implementation files. No game launch or configuration change. This confirms deployment only; the native gates above remain pending.
