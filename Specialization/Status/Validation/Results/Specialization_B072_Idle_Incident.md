# B072.99 native logging failure and same-turn workload evidence

Document Owner: Codex
Evidence: six user screenshots, three time-paired game/Activity Monitor captures; user reports no gameplay actions and unchanged turn59.
Validation: USER_GAME_TEST_FAIL for native automatic logging. Residual repeated work observed; allocation root cause UNKNOWN. Narrow shared-derive behavior confirmed in this interval, not a complete Batch B or memory acceptance.

| Local time 2026-09-14 | 19:07:52 | 19:08:12 | 19:08:47 | Delta55s |
|---|---:|---:|---:|---:|
| Civ VI Memory (GB, PID26280) |11.06|11.13|11.34|+0.28|
| audit_standard |2007|2782|4229|2222|
| facts |27252|39652|62804|35552|
| city_scan |42500|61100|95828|53328|
| district_scan |27911|43411|72351|44440|
| derive_requested |6778|9878|15666|8888|
| derived_cache_hit |5577|8677|14465|8888|
| input_duplicate |5569|8669|14457|8888|
| derive_executed |1|1|1|0|
| derived_cache_miss |1|1|1|0|
| route_scan |3|3|3|0|
| building_check |643683|643683|643683|0|
| building_create/remove |1/1|1/1|1/1|0/0|
| property_write |0|0|0|0|
| net_send/receive |1/1|1/1|1/1|0/0|

Also unchanged: unit_cb0; route revalidation71; publication1; same_snapshot2; fact_change/input_publication/input_version_change1; withdrawals/confirmed invalid/stale rejects0; inflight0 peak1; Lv3 audits75, Boost3, Commerce70, Copy76, busy1423, send timeout0. Counts are screenshot observations, not a sampled call trace. Camera/map differs in third image; no claim of a completely untouched UI—user reports no gameplay actions, counters are manually observed.

## Findings

All three show Runtime audit=DISABLED | FILE_API_UNAVAILABLE. This is the first io/open capability guard in UI/RuntimeAudit.lua, before HOME resolution or file open; not evidence of folder permissions, bad filename, or disk full. Current file transport cannot run in this native context. Its stored traceback is displayed diagnostics, not proof of repeated exception execution or a crash. No automatic turn-history claim; long-play logging gate failed. Existing local simulations validated portable stdio/model behavior only.

Same input produced no new complete derive, publish or building/property changes in55s. Cache is serving reads. However facts/scan work continues:2222 Discount audits, exactly4 queries/16 facts/24 city scans/20 district scans per additional audit over this observation. Static code matches: StandardizationDiscount listens to GameCoreEventPublishComplete and iterates cities; RecipientSources calls currentView, which calls Refresh/Capture before its cache lookup. This establishes a strong repeat-work hotspot, NOT proof that a specific Lua table or native allocation accounts for memory growth. No new Mod send/receive in interval; native/other-mod events remain possible. Lack of building writes means this window is not the previous0→restore building churn. Short memory growth alone does not establish sustained unbounded leakage or attribute all RAM to this Mod.

Do not broaden Batch B into a completed memory fix. Recommend a separately authorized targeted investigation/reduction of generic Discount triggers and repeated fact capture (C/D boundary), plus a genuinely available log transport. No code/fallback/deployment performed here. No extra stressful game test required; do not use this build expecting a reliable automatic full-game log.

## Archive

All29 inbox files (19PNG,8text/log,2Finder metadata),175305820 bytes, moved with SHA256-before/after verification to external workspace:
`W/Specialization/Status/Validation/Evidence/20260914-Memory-Incidents/`
Manifest `manifest.json` has original paths, archive paths, size, mtime, SHA256 and VERIFIED_COMPLETE. Six current screenshots under B072.99;13 earlier afternoon images and B069-memory-incident subtree under B069.96-existing-materials; Finder metadata separately preserved. Basenames and bytes unchanged; inbox retained and empty. No raw evidence/private desktop backgrounds added to Git.

Old logs are B069 evidence, not current B072: sample PID7312 versus current screenshot PID26280; network log timestamps14:11–15:25. Header/tail/inventory reviewed for separation. Earlier screenshots are preserved existing materials, not newly revalidated for B072. No fresh B072 log/sample supplied. Old evidence references can resolve through manifest source→archive mapping.
