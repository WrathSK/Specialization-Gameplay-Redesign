# Specialization External Runtime Monitor 1.0

Document Owner: Codex
Scope: optional macOS developer tooling, not Mod content. Never deploy or add to modinfo.

## Start / stop

Python3 standard library only. Start Civ VI yourself, then in Terminal:

```sh
cd /Users/xutingzheng/Projects/Specialization-Gameplay-Redesign-develop
python3 tools/external_monitor/monitor.py start --build B072.99
```

`--build` is a USER-SUPPLIED label, not a game query. Use B071.98 if that is actually your package. At the time this tool was made, live was B072.99; this tool did not switch it. It selects exactly one Civ6_Exe_Child at startup or refuses. `--pid NUMBER` is optional, still checks the native process name. It neither launches nor waits for a future game. No other process is silently chosen. Keep this terminal running; Ctrl+C stops only the monitor (after any in-progress bounded diagnostic finishes). It exits when target exits/identity changes or ordinary access is lost; restarting Civ VI requires a NEW monitor session.

Default interval30 seconds (`--interval`10–3600). Default automatic snapshots OFF. No debugger, hook, injection, game API, configuration/save reads, RSS shell polling loop, or OCR. Regular statistics use libproc (plus one targeted ps CPU read), not vmmap/footprint commands. Only process identity and OS accounting are read, no game virtual memory is read by our code.

The printed session path is used for optional commands in another terminal:

```sh
python3 tools/external_monitor/monitor.py mark --session /PATH/TO/SESSION "noticed slowdown"
python3 tools/external_monitor/monitor.py capture --session /PATH/TO/SESSION vmmap
python3 tools/external_monitor/monitor.py capture --session /PATH/TO/SESSION footprint
python3 tools/external_monitor/monitor.py capture --session /PATH/TO/SESSION sample
python3 tools/external_monitor/monitor.py stop --session /PATH/TO/SESSION
```

Markers write UTC immediately. Other commands queue ONE tiny request, processed at the next sample boundary (normally30s, longer during a bounded capture). Duplicate pending request is refused; Ctrl+C remains available. Nothing is sent to Civ VI. No monitor daemon/startup item is installed. Do not launch multiple monitor instances against the same root; an exclusive lock prevents it.

## Output / retention

Default root: `~/Library/Logs/SpecializationExternalMonitor/`, outside game directories and Git. `--log-dir` can select a new empty standalone directory; nonempty unowned roots, symlinks and game/runtime/save path components are rejected. Cleanup only removes marked monitor session directories here, never game/Mod logs.

Each `session-UTCtimestamp-uniqueid/` contains:
- session.json: schema1/version1.0/build label/start/end UTC/target PID/name/start seconds+microseconds/state.
- trend.tsv: one row per sample; max4MiB, reaching cap ends collection without losing prior rows.
- events.tsv: metric selection/capture result/failure or suppression, max128KiB.
- markers.tsv: explicit user markers only, max128KiB, text capped200characters.
- capture-NN-vmmap/footprint/sample.txt when requested: each max2MiB.

At most8 capture attempts total, including at most2 manual sample attempts; automatic captures at most6. Data per generated session is below24MiB. On startup reserve24MiB and prune oldest owned sessions to keep at most20 and aggregate allocated log content below256MiB. Whichever limit is reached first applies. This is logical content size, not filesystem allocation accounting. Older logs will eventually be removed; copy a relevant session outside this managed root before many more runs. Cleanup runs only at startup. Mid-process kill/power failure can leave state RUNNING with partial final row; timestamps still identify the session. Stream flush is not a promise of power-loss fsync durability.

No infinite data structure: four-sample growth window, five threshold flags, fixed scalar state/last capture only. No per-sample JSON metadata rewrite; small TSV append/close each sample. Write/access failure ends monitoring; no high-frequency retry. stdout only announces start/end, not every measurement.

## TSV schema and exact meanings

`timestamp_utc`, `elapsed_seconds` (monotonic session duration), `pid`, `process_start_sec`, `process_start_usec`, `rss_bytes`, `physical_footprint_bytes`, `virtual_size_bytes`, `cpu_pct_ps`, `thread_count`, `collection_ms`.

- RSS: native proc_taskinfo.pti_resident_size, currently resident bytes. Not virtual reservations and not Activity Monitor's general Memory label.
- Physical footprint: native proc_pid_rusage RUSAGE_INFO_V0.ri_phys_footprint, kernel footprint accounting; different from resident size. No claim of exact equality with Activity Monitor. If unavailable, empty field; the optional API is disabled after first failure.
- Virtual size: pti_virtual_size, address-space size. Large reservations are common; NOT RAM and NEVER a threshold metric.
- CPU: `/bin/ps -p PID -o pcpu=` percentage, recent/decayed average provided by ps, NOT an exact interval CPU delta. Can exceed100% across cores. Blank if optional CPU read fails.
- Thread count: native pti_threadnum. Collection ms includes two identity reads, native statistics and the ps call, not a heavy capture.

Native ABI sizes checked against installed SDK: BSDInfo136, TaskInfo96, RUsageV0 96bytes. Identity is PID+native start seconds/microseconds+name, checked before and after ordinary read. Changed identity ends old session, never appends new PID. Snapshot commands also check before/after and reject changed identity results; PID-based OS utilities have a tiny unavoidable process-exit/reuse race at command launch, so cannot provide an atomic lifetime pin.

Timestamps are UTC ISO8601; align screenshots' local time using timezone. No knowledge of turn/cities/Network counters is inferred. If a future game log provides its own timestamps, join offline; B072's FILE_API_UNAVAILABLE remains unresolved. External monitoring does not supply missing internal counters.

## Optional snapshots / cost controls

Enable only deliberately: `start --build B072.99 --auto-snapshots vmmap` (or footprint). First baseline after60seconds. Later first unrecorded absolute threshold10/15/20/30/40 decimal GB, or at least256MiB/min growth in each of3 consecutive windows. Uses physical footprint if available, otherwise RSS with metric explicitly recorded; switching metric resets comparison history. Thresholds are evidence triggers, NOT leak verdicts.

Cooldown600seconds across ALL captures, including manual; limits above. Deferred threshold crossings coalesce at next eligible checkpoint. Snapshot timeout5seconds; max2MiB output; too slow (>3s), timeout, permission/error exit disables that tool for session. `sample` is NEVER automatic: manual5seconds,10ms sampling interval, timeout15seconds; duration>10s disables it. Timeout/output limit terminates ONLY the child diagnostic utility. No forkCorpse, heap dump, allocations tracing, automatic sudo or security-policy changes. Failed privilege check is evidence, not a request to disable platform protections.

## Local validation / readiness

[Benchmark and boundary report](../../Specialization/Reports/Technical/Specialization_External_Monitor_Validation.md). 13 pure tests include10000 samples/20-session and total-byte retention,4-entry history, PID reuse, exit/no rediscovery, timeout/output caps, directory guard, marker and locking. Native tests used a NEW synthetic64MiB Python process, NEVER the current game. vmmap/footprint/sample worked on that process, but game attachment permissions and large-process costs are UNKNOWN.

Candidate for a USER-STARTED short30s trend session; not certified for every Civ VI configuration. No current game was observed or sampled by this implementation task. Begin with automatic snapshots OFF. You need not periodically read Counters. After slowdown/crash/long play provide the relevant whole MONITOR session folder and approximate turn/symptom. Do not upload all game Logs. If needed, use one manual in-game Counter screenshot for timestamp correlation.

## Future Instruments (not executed)

Current Command Line Tools install did not provide xctrace. Full Xcode/Instruments could later record a short Allocations/VM Tracker window after a reproducible trigger is found. Distribution-game permissions and available symbols must be checked then. No hours-long allocation trace, no installation/launch here. Apple sources: https://developer.apple.com/videos/play/wwdc2024/10173/ and https://developer.apple.com/library/archive/technotes/tn2434/_index.html .

## Reproduce local checks without touching game

```sh
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_external_monitor.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/external_monitor/benchmark.py local/external-monitor-benchmark.json
```

Benchmark deliberately creates its OWN worker. Do not replace its PID with a game PID. Raw outputs are temporary/ignored, not bundled gameplay assets.
