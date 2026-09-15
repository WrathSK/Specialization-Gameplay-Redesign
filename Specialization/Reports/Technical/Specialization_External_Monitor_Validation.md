# External Runtime Monitor1.0 — local validation

Document Owner: Codex
Scope: develop tooling only; Mod B072.99/modinfo99 unchanged; main unchanged
Evidence: LOCAL_SIMULATION_PASS plus native tools on own synthetic process. NOT Civ VI performance PASS.

## CPU/resource benchmark

Four3-second phases OFF/ON/OFF/ON on one freshly-created64MiB Python worker. ON deliberately sampled about every0.1s (28 observations/phase), much faster than production30s, to measure per-call costs. Worker CPU: OFF0.2711s/3.0157s and0.2773s/3.0379s; ON0.2806s/3.0393s and0.2796s/3.0238s. No large difference in this short synthetic run; this is NOT proof of zero overhead for Civ VI.

ON median collection times5.704ms /4.376ms; max9.078ms /6.162ms. Monitor CPU0.09356s/0.064385s; ps children0.092075s/0.071991s for28 samples each. Combined approx5.75ms CPU/sample; amortized at30s about0.019% of one core is an ESTIMATE, not a measured long-game CPU percentage. Monitor native RSS24,231,936 bytes, footprint18,253,504bytes during benchmark; ps CPU2.2% reflected deliberately rapid testing and must not be labelled production CPU. Worker RSS79,527,936/footprint74,630,208 bytes. Virtual size ~420GB is address reservation, NOT physical memory usage.

Native diagnostic tools on ONLY the synthetic worker:

| Tool | Wall seconds | Output bytes | Exit |
|---|---:|---:|---:|
| vmmap -summary |1.2993|5055|0|
| footprint -p |0.0507|1671|0|
| sample5s/10ms |5.2670|58344|0|

Large Civ VI permissions/costs remain USER_GAME_TEST_REQUIRED if user chooses snapshots. Defaults remain auto snapshots OFF and sample manual only. No Instruments launched; xcrun could not locate xctrace. No current game PID discovered or read.

## Example short session

Actual synthetic session59 trend rows,7709 bytes total, closed normally; target exit detected. Build label SYNTHETIC-NOT-GAME, native PID/start identity, UTC timestamps and native process readings. It is an accelerated validation session, not evidence of any game turn. Row structure:

`timestamp_utc  elapsed_seconds  pid  process_start_sec  process_start_usec  rss_bytes  physical_footprint_bytes  virtual_size_bytes  cpu_pct_ps  thread_count  collection_ms`

Keep distinct from current user screenshot evidence:55s Activity Monitor11.06→11.34GB, Standardization+2222, city scans+53328, full derives1, building/property/send/receive deltas0. Correlation hypothesis only; external monitor does not establish allocation causality or solve FILE_API_UNAVAILABLE.

## Tests / guards

13 tests:10000 writes/fixed4-entry window; 20-session retention and total byte pressure; target exit/no rediscovery; start-identity change rejection; unknown/symlink/game directory refusal; single-monitor lock; mark/stop; noisy subprocess2MiB truncation; subprocess timeout; fixed threshold/cooldown/auto count. SDK C sizeof versus ctypes:136/96/96 confirmed. Only temp files and own test worker used.

Long-run caps: trend4MiB ends monitoring; events/markers128KiB each; at most8 captures ×2MiB,6 automatic/2 sample limits; <=24MiB reserved per session; <=20 sessions and256MiB managed retained content. Never prune game log trees. No Mod files changed; no deployment, source precision or C/D work. Instrumentation outcome remains a candidate for user-started trend monitoring, not a statement that55GB issue is fixed.
