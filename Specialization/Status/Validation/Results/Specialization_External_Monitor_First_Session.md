# External Monitor — first user Civ VI session

Document Owner: Codex
Evidence: USER_GAME_TEST_PASS for external trend collection and normal stop ONLY (user-run process evidence); memory root cause UNKNOWN.
Build label: B072.99 (operator supplied, not runtime attestation)
Session: session-20260915T023339806231-4085bf40

## Evidence and integrity

Read all four supplied files: session.json, trend.tsv, events.tsv, markers.tsv. 2743 bytes total. Archived unchanged with SHA256 manifest outside Git at legacy workspace W/Specialization/Status/Validation/Evidence/ExternalMonitor-20260914-193339/. W is the external Civilization VI application-support workspace. No screenshots or snapshots were supplied in this batch. Inbox cleared of these four files; originals frozen, no duplicate raw evidence committed.

UTC observation window 2026-09-15 02:33:39.807 to 02:40:40.067; Vancouver local 2026-09-14 19:33:39.807 to 19:40:40.067 PDT. 15 rows over 420.259 elapsed seconds, intervals about 30.01–30.02 seconds. PID28458/start identity1789439551:843773 unchanged across all rows. Metadata ENDED/stopped at02:41:01.142UTC, rows15, captures0. Normal monitor stop does not establish game exit.

## Resource trend

All GB below decimal (10^9 bytes); RSS, footprint and virtual size are distinct measures.

| Metric | First | Last | Interpretation |
|---|---:|---:|---|
| Physical footprint |10.381810752 GB|16.582378816 GB|+6.200568064 GB, all14 intervals positive|
| RSS |1.006190592 GB|0.477102080 GB|Resident pages; range0.477–1.339 GB|
| Virtual size |436.850638848 GB|442.157039616 GB|Address space, NOT RAM; +5.306400768 GB|
| ps CPU percent |90.2|133.6|Range61.0–133.6, median116.4; not per-sample CPU delta|
| Threads |29|31|Range29–32, no sustained thread-count expansion shown|

Footprint growth averaged0.88525 GB/min across this window. First30sec adds2.12376 GB; excluding the first60sec still gives +3.32540 GB over360.227sec (~0.55388 GB/min). Growth is therefore not solely the initial jump. Do not extrapolate to an entire game or call this proof of a leak.

RSS falling while footprint rises is not contradictory: these account for different resources. This dataset alone cannot quantify compression, swapping, graphics, heap or anonymous VM categories. Do not equate footprint precisely to Activity Monitor Memory without simultaneous matching measurements. No contemporaneous Activity Monitor screenshot supplied.

Collection wall time median13.927ms, max18.011ms per30sec interval. This measures collection latency, not monitor CPU/RAM overhead or a controlled OFF/ON comparison. Trend collection succeeded on the game process; long-run retention, game snapshot permissions/cost and leak attribution are not validated here.

## Missing correlation and attribution limits

Auto snapshots explicitly off; events.tsv contains only threshold_metric=physical_footprint_bytes, no error/capture events. Empty markers.tsv is a valid header-only file. No vmmap/footprint/sample captures, game counters, Turn or user action timeline accompany this session. Absence of anomaly events does not mean growth is normal: automatic captures were disabled.

The prior screenshot window19:07:52–19:08:47 used PID26280; this window starts19:33:39 with PID28458. Different process instances and non-overlapping windows: do not pair prior Standardization +2222/city scans +53328 counts with this session or claim this session was idle. Latest submission itself does not specify gameplay actions.

Confirmed: external monitor records continuing physical-footprint growth in a real Civ VI process. UNKNOWN: responsible allocation category, module, leak versus other accumulation, and whether game counters rose simultaneously. No evidence here justifies a gameplay fix or declares Batch B ineffective: cached derives and memory cause are separate questions.

## Next evidence, not executed

If a further capture is authorized, compare two time-separated manual vmmap/footprint summaries during growth, subject to existing timeout/cooldown protections. Pair one contemporaneous game counter reading only if safe. Native categories can narrow the question; they still do not identify Specialization as the cause. Do not automatically attach to the current game or enable sampling in response to this report.

This batch changes only validation/status documentation; no Mod, Design, Architecture, monitor implementation, runtime deployment or main changes.
