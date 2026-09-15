# External Monitor — successful footprint classification

Document Owner: Codex
Session: session-20260915T025957200955-3dfae769
Build label: B072.99 (operator supplied, not runtime attestation)
Evidence: USER_GAME_TEST_PASS for one user-run footprint capture and external trend collection only; allocation-growth cause UNKNOWN.

## Session and trend

Four samples at UTC2026-09-15 02:59:57.202–03:01:27.669 (Vancouver Sep14 19:59:57–20:01:27), elapsed90.466sec. Same PID31610/start1789441110:873155. Metadata ENDED/stopped at03:01:46.741UTC, one capture. No manual markers. Latest user submission does not give an exact load-complete timestamp; do not invent it from the preceding suggested test steps.

Physical footprint bytes11856077632→12380202880: decimal11.8561→12.3802GB, +524125248bytes (~0.524GB), average0.3476GB/min. All3 intervals positive. RSS0.439→0.716 decimalGB, range0.439–0.901GB. CPU ps101.8–127.2%, threads31–32. None identifies allocation ownership. This is a different PID from both prior monitor sessions; their category levels cannot form a same-process growth comparison.

## Native footprint result

At03:00:57.645UTC (+60.444sec), tool returned complete/exit0,2730bytes,0.4096sec, identity_still_matches=true. Unlike prior vmmap timeout, classification is usable. The trend sample just before capture reports12215805568 physical-footprint bytes. Native human-readable summary rounds this to11 GB; do not interpret the labels as exact decimal bytes or treat this as a contradiction. Preserve native MB labels below; their values are rounded.

| Native dirty category | Reported size | Regions |
|---|---:|---:|
| IOAccelerator (graphics) |5290 MB|15946|
| MALLOC_MEDIUM |2734 MB|37|
| MALLOC_SMALL |875 MB|238|
| MALLOC_TINY |866 MB|911|
| MALLOC_LARGE |838 MB|43|
| MALLOC_NANO |254 MB|3|
| MALLOC_LARGE_REUSABLE |167 MB|8|
| Owned physical footprint (unmapped) |274 MB|2212|
| IOSurface |95 MB|14|
| untagged (VM_ALLOCATE) |52 MB|89|
| stack |2816 KB|62|

Six MALLOC categories total approximately5734 native MB, excluding separately listed allocator metadata. Graphics IOAccelerator5290MB is a similarly large component. Total26713 regions and32MB clean/7008KB reclaimable reported. Region counts are not UI element counts, Lua table counts or allocation counts and cannot establish a region leak from one sample. MALLOC is not synonymous with Lua; graphics is not synonymous with our UI or proof of a GPU-driver bug. Dirty accounting is not a report of corrupted memory.

## Consequence for investigation

This closes the narrow practical blocker of obtaining ANY native category snapshot on Civ VI with the current bounded tool. It does not prove large-game snapshot cost remains low for all sessions. A0.41sec capture is not a controlled monitor OFF/ON overhead comparison.

Both heap and graphics must remain investigation candidates. No evidence yet shows which grows: one category snapshot cannot assign the524MB trend delta to either category. Existing repeated-facts/Discount evidence remains a CPU/work hypothesis with runtime counter support, not established retained-allocation causality. Old B069 sample symbols likewise cannot identify a Lua module.

Next useful evidence is TWO footprint summaries from the SAME process/start identity with a trend interval between them. Existing capture cooldown is600seconds. Do not silently bypass it, lengthen this session after it ended, attach current game, or ask user to endure severe memory pressure just to obtain a second sample. Any shorter targeted capture protocol/tool change needs its own explicit scope. Keep game state/view comparable and mark load completion if measuring post-load idle. No new test is required merely to confirm this successful capture again.

## Archive / scope

Five supplied files4731bytes archived with original basenames and SHA256 verification at external W/Specialization/Status/Validation/Evidence/ExternalMonitor-20260914-195957/manifest.json. Raw content outside Git; inbox cleared of these files. This batch updates validation/status only, no gameplay, monitor source, Design, main, deployment or process attachment.
