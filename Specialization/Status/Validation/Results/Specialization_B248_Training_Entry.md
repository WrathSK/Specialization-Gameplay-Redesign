# B248 — Restructuring training access and Investor presentation

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.
Baseline: develop `834d4c2`, deployed B247.274 from `88abdf9`. Source follow-up B248.275 / modinfo275. No new Design rule.

## Reported failure and evidence boundary

The user reports that **重组团队** is absent from the ordinary production list, not merely invisible on the map. The city was already Commerce IV, inspected immediately after loading, without advancing a turn. Therefore a same-turn investment notification defect alone does **not** explain this submitted case.

The current read-only loaded gameplay database contains the B247 unit, 500 Production / PopulationCost 0 / CanTrain 1 / no purchase / no cost progression, the exact access-building prerequisite and all six disruption modifiers. The corresponding Modding log records the B247 SQL/text application. HD's `UI/Replacement/DL_ProductionPanel.lua` (installed Workshop item 2465378070) includes units through native `CanProduce(parameters, true)` and distinguishes enabled state with `CanProduce(parameters, false, true)`. Our existing adapter does not explicitly filter this unit. Unit art does not supply training eligibility.

The submitted local collector session `session-20261019T052249Z-abc25b` contains 64 retained records, sequence 28–91, including other modules' load/network activity but no restructuring access/production-list snapshot. Its ring is bounded; absence of a REST record is not proof that this service failed to start. The original file remains ignored and unchanged. records.log SHA256: `2b0ef3136975b57b80c0561b283c5b733a493ace13a76878fca925901e41ae77`.

A separate definite defect is reproduced using the actual Store investment and actual Gameplay notification function: Commerce III → IV reports ACTIVE4, but the access marker is absent after investment and event publication; it appears only after the next player-turn event. `WriteInvestment` does not emit the generic permanent-write notification used by this service, and the committed-investment dispatcher omitted Restructuring. The existing-IV load fixture **does** rebuild a missing marker without a turn. Native load-time visibility remains unresolved; do not label the user's reported case fixed from this local result.

## Narrow changes

- Add Restructuring to the existing committed-investment notification. `Refresh(player, city)` marks only the proved changed city and uses the existing derived-marker writer. Duplicate notifications do not recreate the marker or write Store state. No polling, new Property, capacity, cost or transaction change.
- Add `REST_LOAD_BEGIN`, `REST_LOAD_RETURNED`, and post-readback `REST_ACCESS` observations to the existing bounded diagnostic stream. `expected` is current ACTIVE, `count` is Potential, and `mode` is Identity. Marker success is recorded only after the existing readback succeeds.
- The production-list read emits `REST_TRAINING_LIST`: service presence/readiness, marker presence, native exclusion visibility (`readyToSelect`), actual eligibility, price and whether the original list contains the unit (`count` 0/1; `paused` means its Disabled flag). Up to four allowlisted `LOC_...` failure keys are retained; arbitrary strings are redacted. No translated names, paths or authentication data. One replaceable selected-city/revision key suppresses duplicate UI queries. This observer neither requests gameplay actions nor injects a list item or bypasses `CanProduce`. Failures cannot break the ordinary production panel. The collector/protocol/budgets are unchanged.
- Reuse installed **Leugi's Monopoly++: Tycoons and Investors**, Workshop 2479197624, Mod/art ID `b248a322-3e2a-4a6a-830a-6b0d1f3435fc`, metadata version 1. The unit entry refers to `Leu_Investor`, its formation/embark/audio mapping, and existing Investor atlas entries, including white flag/portrait variants. The provider is an explicit mod/art dependency. No model binaries/textures are copied; no other Mod files are edited. Investor purchase/cost/capacity/abilities are not inherited. B247's Builder presentation remains historical evidence only.

## Local verification

**58 selected unittest methods PASS**: 15 new B248 checks, 38 actual B247 Store/service/contract checks and 5 retained UI checks. Checks include exact committed investment → target-city access, rejected requests, no duplicate writes, Governor withdrawal/return, load-time marker reconstruction, failed marker readback, unchanged original transaction/history/contract behavior, read-only production observation and redaction, Lua 5.1 parsing, Investor dependency/icon mapping, unchanged other unit art and package file registration. Unit gameplay SQL is byte-identical to B247. No frozen tests/results were rewritten; the old version-pinned B247 package assertions are not claimed as current package validation.

The native SQL loaded-row check is static database evidence. CanProduce outcomes, real model/icon rendering and the unresolved load-time hidden entry require native evidence; local simulation is not an engine PASS. No process-memory/CPU claim or gameplay regression requalification.

## Minimal combined native flow

Use the existing collector before loading. Open the already Commerce ACTIVE IV city's ordinary production list immediately, without needing a turn or P0. Look for **重组团队**, base 500 Production and Investor icon.

- If absent/disabled, stop there and retain the collector log; no blind next-turn workaround or further training is requested. `REST_LOAD_*`, `REST_ACCESS` and `REST_TRAINING_LIST` distinguish startup/qualification/native-list failures.
- If present, train it and observe the Investor model; then resume the original [B247 transaction flow](Specialization_B247_Restructuring_Local.md#one-native-acceptance-flow): **资产清算** → save/cold-load while REALLOCATING → after five full turns **资产配置**. One Potential loss, retained team/target/history, final new Identity and team consumption. No separate repeated save/load test for this presentation patch.

## Deployment

Pending guarded W0003 deployment from clean committed source. Current live package remains B247 until separately verified; main/stable remains B069.96. No game launch/configuration change.

User decision: none. User testing: the entry check followed by the already pending B247 flow only if available. Primary next: record the scoped result; no subsequent batch is authorized automatically.
