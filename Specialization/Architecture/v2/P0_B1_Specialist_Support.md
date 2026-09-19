# P0-B1 — all-level specialist support / B079.106

Document Owner: Codex
Authority: D0032; A0160 implementation plan under A0161; no Design revision change
State: IMPLEMENTATION_COMPLETE_AWAITING_USER
Evidence: STATIC_CONFIRMED + LOCAL_SIMULATION_PASS; not engine PASS
Baseline: 324f455 / B078.105. Main B069.96 unchanged.

## Scope and exclusive writer

Research/Culture/Commerce retain existing native per-working-specialist +3 Food/+3 Production at ACTIVE1–4. Industry retains +3 Food + existing K1=1 × BASE Production adjacency; actual adjacency is not substituted. Native citizen yield rules still determine occupied specialists; empty slots produce no specialist yield. No new carrier, Property, precision formula, Lv2/GPP/Housing, Network, III named ability, or P0-C Research effect is introduced.

`SpecialistSupport.lua` supplies the narrow anchor/retirement checks, not a new generic engine. ResearchSupport and IndustrySupport use existing EffectiveFacts and RuntimeWork ephemeral batch indexes: owner, permanent anchor, normalized family including unique replacements, completion, pillage and ACTIVE. Confirmed absence/ineligibility withdraws; unreadable facts/samples retain the last projection. Industry uses the C2 verified BASE sample and unchanged request/epoch/retry contract; family normalization also applies to sample discovery.

The exact retirement allowlist is four `BUILDING_SPC_DEV_LV3_{RESEARCH,CULTURE,COMMERCE,INDUSTRY}` IDs and eight `BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_0..7` IDs. Their SQL definitions remain inert tombstones; all old citizen-yield rows are removed. Existing objects are removed once, verified before adding support. Removal failure blocks the new support write and remains diagnostic. No broad prefix removal: population, adjacency, other Lv3/Lv4 and Network carriers remain unchanged for their own later batches.

Public Lv3Support.Start now creates a retirement-only facade. Original code remains unreachable as local historicalStart; no public control, load/turn callback or Industry receive can revive it. Gameplay investment/action paths refresh current support writers; GPP dirty no longer wakes the retired support writer. Historical fixtures and scripts remain untouched.

## Events and performance

Named load, district, governor and real specialization-action events update support. PlayerTurnActivated provides once-per-player-per-turn reconciliation. Pillage/repair event hooks are optional engine events with that turn safety net; no guaranteed native event coverage is claimed without game evidence. No Publish/Playback/frame/hover handler, new periodic sampler or request is added. Existing Industry UI lifecycle only gains pillage/repair dirty events. Worker changes need no carrier rewrite because native CitizenYieldChanges applies per occupied slot.

Each support Audit creates one temporary player district index and reads each city's facts once. Two distinct support modules may still each do one linear audit on a relevant event; this is not a claim of global single capture. Retirement checks twelve fixed IDs, not a database enumeration. No persistent unbounded cache/history.

## Local verification

Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_p0_b1.py --regression` in the configured local Lupa environment.

| Model | Result |
|---|---|
| Each writer: 1/2/4/8 cities × four professions × ACTIVE1–4 × workers0/1/3 | 192 normal scenarios per writer; no hidden module errors |
| Facts/district reads per audit at 1/2/4/8 cities | 1/2/4/8 respectively per writer |
| 10,000 unrelated notifications | No additional facts, district scans or Building writes |
| Real governor ACTIVE0/4, pillage/repair | Registered event path withdraws/restores; repeated unchanged event does not write |
| UNKNOWN ACTIVE/pillage or pending Industry sample | Retains confirmed projection; no fabricated zero |
| Retired IDs seeded in save model | Exactly12 removals once; no resurrection on duplicate/manual/load; unrelated population carrier survives |
| Cleanup failure | Blocks new add; subsequent valid retry recovers |
| SQL execution | Twelve inert tombstones; native 3F3P and Industry base formula retained |
| Read-only support diagnostics and legacy ON/OFF aliases | No writes |
| UI caption init and 10,000 idle UI callbacks | Explicit caption/color, no sends; actual visual rendering still requires user |

Composite runner retains A/B/C1/D1/C2/D2, P0-A and deployment safety regression. Only old Lv3Support output-equality cases that require the deliberately retired rule are excluded and replaced with the exact retirement/SQL tests. Eight unaffected D2 modules retain 1/2/4/8 × profession/ACTIVE/worker carrier comparison (1536 scenarios), normal-error checks, 30,000 Network-view reads, UI idle and sample epoch/stale/retry checks. Old test files are not edited or relabeled game PASS.

## User evidence / diagnostic / next gate

[B078 user evidence](../../Status/Validation/Results/Specialization_B078_P0A_20260918.md): D and workers read correctly; refresh sound gone; pillage not tested because the user lacks a controllable operation. This is not a current game-freeze incident.

Existing 专家与岗位 / SPECIALISTS now appends expected/actual support and retired-support status, read-only. The blank 区域完善度 / 科研影子 label receives a named XML caption, explicit color and initialization SetText; no extra panel entry or hover request. These visual changes are locally validated only.

Minimal combined game check after safe W0003 deployment: load a prepared test save, confirm B079.106; select an ACTIVE3/4 Research (or Culture/Commerce) city, assign/remove one working specialist and read 专家与岗位; base support must be extra3F3P rather than old5F5P. If an Industry city is already available, check extra3F + BASE P and no old III BASE×2 Gold. Other old abilities/native yields remain, so compare support components, not an unexplained entire-city total. Save/reload once only if convenient to check retired support stays absent. Confirm the D diagnostic button text. Do not manufacture disasters/AI wars for pillage.

P0-B1 local gate PASS, engine acceptance pending. Recommend P0-B2 next only after separate authorization; no B2/C/BatchE implementation. Memory55GB cause is not declared solved.
