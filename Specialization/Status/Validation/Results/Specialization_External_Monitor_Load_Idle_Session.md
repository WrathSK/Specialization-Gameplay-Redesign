# External Monitor — load then idle session

Document Owner: Codex
Scope: evidence review only; no source, runtime, Design or monitor changes
Session: session-20260915T025052160250-1500e9e2
Build label: B072.99 (user supplied)

## User chronology and observed facts

User started game, started monitor, loaded save, made no further game operations, exited game, then stopped monitor. Exact load completion and exit timestamps were not provided. User chronology is evidence; do not relabel the whole interval idle.

8 trend rows, same PID30320/start1789440630:739460, UTC2026-09-15 02:50:52.161–02:54:27.446 (Vancouver Sep14 19:50:52–19:54:27), elapsed215.283sec. Session ended02:54:56.544UTC with reason stopped. This does not contradict user exit-before-stop: no subsequent process-exit observation is recorded; no exact exit time can be inferred.

Physical footprint (decimal GB): initial4.225953152; +30sec6.245400704; +60sec11.691712832; final12.441659264. Full +8.215706112 GB includes loading and is NOT a measured idle leak rate. From +60.096 to +215.284sec: +0.749946432 GB over155.188sec (~0.290 GB/min). From +95.193sec: +0.480429120 GB over120.091sec (~0.240 GB/min). All7 intervals positive, but short irregular growth does not establish indefinite retention/leak or module causality. Without a load-complete marker these suffixes are time windows, not proven pure post-load intervals. CPU ps peaks543.1% at30sec, later116.9–128.5%; cannot define loading completion from CPU alone.

## Snapshot failure, not an empty memory map

Automatic baseline vmmap began around+60sec. completion=timeout, duration5.0761sec, exit_code255, bytes0, identity_still_matches=true. events records tool_disabled vmmap. capture-01-vmmap.txt is genuinely empty, preserved as failed evidence; no allocation category exists to interpret. Timeout does not establish permission denial or a broken game API. Synthetic-process success did not establish large-game capture cost.

The next row gap is35.097sec, consistent with the bounded synchronous capture delaying the next30sec sampling cycle. Later intervals resume about30sec. Trend collection continued after capture failure. No markers. No same-window game counters, no successful vmmap/footprint or sample. No causal claim against HD/BTS/Specialization.

USER_GAME_TEST_PASS only for ongoing external trend collection and capture-failure suppression visible in this run. USER_GAME_TEST_FAIL for obtaining the requested vmmap baseline within the current5sec limit. Root cause remains UNKNOWN. No timeout increase, automatic reattachment or deployment performed.

## Archive and next evidence

Five supplied files,2531 bytes, original basenames and SHA256 verified in external W/Specialization/Status/Validation/Evidence/ExternalMonitor-20260914-195052/manifest.json. Empty capture preserved. Raw files outside Git; inbox cleared of this batch.

Next minimal optional experiment: use existing footprint capture path rather than repeat vmmap or increase its timeout. Start monitor AFTER load completion so elapsed window is unambiguous; one bounded automatic baseline at60sec, then stop without waiting10min for another snapshot. A single category summary can inform direction, but two successful same-process snapshots would ultimately be needed for category growth attribution. Game footprint tool permission/cost remains unverified. User executes; no extra game manipulation or long stress run required.
