# Mod isolation：HD Core + UI helpers / no HD + Cheat Panel

Document Owner: Codex
Build: B072.99 / modinfo99; source/runtime unchanged
Evidence: 12 screenshots read individually, user descriptions; not a controlled ABA conclusion.

## Membership and protocol

Run1: user says planned Test1 plus TITLE and AREA: BASE+CORE+TITLE+AREA, six third-party Mods. This is not original T1 four-Mod set. Run2: user removed HD and added Cheat Panel, three cities; user confirms TITLE/AREA retained: BASE+TITLE+AREA+Cheat; exact Cheat UUID not independently captured. No fresh enabled-log captured, membership is user report. Do not infer helpers harmless merely because frontend/XML-only. No additional HD addons/Monopoly++ needed for observed Run1 growth, within reported membership.

All six Activity Monitor images show PID45352. Therefore do not certify independent process restarts; user confirms only returning to main menu and starting a new game, no process exit. Different maps, turn/state and Cheat use further limit causality. Run1 first two screenshots already show a city/minimap, Property writes7, not zero-city. Later screenshots show two cities/Turn18. Run2 shows three cities/Turn1. Native automatic audit remains FILE_API_UNAVAILABLE. No monitor time series delivered, only paired endpoints; monotonicity between captures not established. No crash shown in these windows; no assumption about after-window outcome.

## Time / Activity Monitor Memory

|Folder/pair|Time Sep14|Turn|Cities|Memory GB|Threads|Ports|
|---|---|---:|---|---:|---:|---:|
|1/a|22:32:42|1|1 visible|9.30|33|1462|
|1/b|22:36:06|1|same|9.50|33|1463|
|1/c|22:37:46|18|2 visible|11.08|33|1463|
|1/d|22:41:09|18|same|11.76|34|1458|
|2/a|22:46:02|1|3 user+visible|9.30|32|1404|
|2/b|23:04:43|1|same|9.69|34|1407|

Run1 a→b204s +0.20GB =0.0588GB/min. c→d203s +0.68GB =0.2010GB/min. b→c includes actions/17turns, not idle. Run2 a→b1121s +0.39GB =0.0209GB/min. Run1 two-city slope is about9.63×Run2 three-city slope, descriptive only; different turn/readiness and added Cheat prohibit causal ratio. Run2 is slower growth, not zero growth or permanent PASS. Memory drop between runs within same PID is not proof full process memory reset.

## Counter totals

|Counter|1/a|1/b|1/c|1/d|2/a|2/b|
|---|---:|---:|---:|---:|---:|---:|
|audit_standard|888|13138|17401|28616|2313|59753|
|facts|57|57|25482|70342|299|299|
|city_scan|1113|25613|149223|238943|291|291|
|district_scan|1053|25553|35674|80534|3886|348526|
|derive_requested|537|12787|19065|41495|36|36|
|derive_executed|0|0|3|3|0|0|
|cache_hit|0|0|5233|27663|0|0|
|building_check|3965|3965|2912724|2912724|18819|18819|
|building_create/remove|0/0|0/0|0/0|0/0|0/0|0/0|
|property_write|7|7|14|14|21|21|
|network send/receive|1/0|1/0|2/1|2/1|1/0|1/0|
|send_inflight|605|12855|13750|13750|2123|59563|

Run1 c→d: audits11215, facts44860=4×, city_scan89720=8×, district_scan44860, query/hit22430=2×. Mirrors earlier two-city nested scans; no changed derive/writes/network transmissions.
Run2: audits57440 (~51.24/s), district_scan344640=6×audit; facts/city_scan/query stay fixed, derive0, inflight1 and no Network ACK throughout. Hence high-frequency audit and region traversal also occur without HD. They do NOT follow the same successful candidate path as Run1 ready network. Do not interpret no-HD as same full code running more efficiently, nor claim exact region-loop attribution from counters alone. Remaining audit_lv3/boost/commerce/copy stay34/3/10/25; unit callbacks28 unchanged. Network send/receive are not all-module requests.

## Assessment / next single variable

Run1 six-Mod set is a smaller known growth-observed set than FULL11 (not proven minimal). Former original T1 remains unexecuted. Run2 is not confidently classified as non-reproducing because endpoint increased and intermediate trend unknown; retain original BASE window observation separately.

Do not add addons. Best next comparison: keep BASE+TITLE+AREA+Cheat fixed, new same-settings games and matching city/turn protocol, toggle CORE only. Start with no-CORE fresh-process0city300s, then CORE fresh-process0city300s; if comparable/inconclusive use same two-city state only afterward. This controls helpers without requiring user remove conveniences; creates a new six/seven-Mod baseline, not original BASE. User has confirmed Run2 retained both helpers; fixed non-HD set is BASE+TITLE+AREA+Cheat. Strictly no Discount code/instrumentation changes. User screenshots already useful; no need repeat full five-stage sequence.

## Archive

External W/Specialization/Status/Validation/Evidence/Mod-Isolation-20260914-2232/ preserves folders1/2 and original names;12PNG74229139bytes. All SHA256 verified before/after move, manifest.json written. No raw screenshots in Git, no other inbox material moved. Source/Design/main/deployment/config untouched.
