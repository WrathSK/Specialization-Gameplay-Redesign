# Paired footprint — allocator growth and enabled-mod evidence

Document Owner: Codex
Session: session-20260915T031233028972-c242fe44
Build label B072.99; monitor1.0.1

## Runtime evidence

Same PID33157/start1789441632:907920, both identity checks match. Captures at2026-09-15T03:13:33.487Z and03:24:04.382Z (Vancouver Sep14 20:13:33–20:24:04),630.895sec apart. Both exit0/complete,0.4162/0.4531sec,2730bytes each. USER_GAME_TEST_PASS for paired collection, not leak attribution.31 trend rows over901.497sec, physical footprint11978368768→16008660480bytes (+4.0303 decimalGB). Not perfectly monotonic: one interval decreases. At samples immediately preceding the two captures:12368570880→15211249664bytes (+2.84268GB), approximately corroborating category delta; exact capture and trend timestamps differ by fractions of a second.

Native rounded MB labels preserved (not assumed exact decimal values):

| Category | First MB | Second MB | Delta MB |
|---|---:|---:|---:|
| IOAccelerator graphics |5308|5311|+3|
| MALLOC_TINY |815|3513|+2698|
| MALLOC_SMALL |921|1056|+135|
| MALLOC_MEDIUM |2844|2716|-128|
| MALLOC_LARGE |813|813|0|
| MALLOC_NANO |266|266|0|
| MALLOC_LARGE_REUSABLE |192|192|0|
| IOSurface |95|95|0|

Six MALLOC categories net+2705 native MB; TINY dominates net increase. TINY regions852→3550 (+2698), graphics regions15945→15945. These are allocator regions, not a count of Lua objects or leaked allocations. A growing allocator footprint can include retained allocations, fragmentation and unreleased allocator regions; this output cannot distinguish them. Stronger evidence than the prior single snapshot: this interval's growth is concentrated in heap allocator categories, not graphics. Cannot exclude UI activity allocating ordinary heap memory. Cannot name Specialization/HD/BTS as cause; no same-window counters, allocation traces or Lua ownership names.

## Enabled mods

User asks how to provide enabled rather than all installed mods despite localized names. Read-only discovered current log at W/Firaxis Games/Sid Meier's Civilization VI/Logs/Modding.log. Outer W/Logs/Modding.log is2023 stale and NOT used. Captured current log bytes separately without moving/modifying live log; last Enabled Mods block contains112 UUID/name entries including official DLC/game modes and Specialization. This is NOT112 third-party active gameplay mods or proof all game modes were selected.

Current log is later than monitored process window; default-enabled/frontend configuration must not be asserted as the test save's exact loaded set. It contains internal identities and names, e.g. Better Trade Screen, More Lenses, Better Report Screen, HD packages, Science/Civic Overflow Bug Fix and Overflow Bug Fix (Switchable Version). Mere co-presence is not conflict evidence. No disabling/removing mods from user's save authorized or performed.

Screenshots are usable with enabled filter and detail panel for ambiguous names; UUIDs and local modinfo localization can map them. Prefer captured same-run Modding.log after loading the affected save, or save load UI's required-mod list, to establish session context. Do not parse/read saves or modify configuration for this task.

## Archive and next step

Six supplied files11176bytes moved unchanged with SHA256 manifest to external W/Specialization/Status/Validation/Evidence/ExternalMonitor-20260914-201233/. Also preserved current Modding log copy/hash and extracted Current-enabled-config.tsv112 entries as clearly separate current-configuration evidence. Raw logs not committed. Next priority: confirm affected-save loaded set, map common event listeners/bridges, then design one-variable isolation; allocator category alone cannot identify a mod. No new gameplay test, tool attachment or code change this batch.
