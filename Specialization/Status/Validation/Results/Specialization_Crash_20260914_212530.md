# Reduced-mod new-game idle crash — 2026-09-14 21:25:30 PDT

Document Owner: Codex
Evidence: user crash report + copied native logs; root cause UNKNOWN

User reports adding mostly HD/direct companions after minimal set, slower modest memory growth, then crash after4–5min idle. Preserve as a separate configuration, not original112-list or minimal-set result. No memory-monitor trend supplied with this crash; slow growth is user observation, not a quantified slope.

## Preserved before restart

External W/Specialization/Status/Validation/Evidence/Crash-20260914-212530/: original pasted crash report, Modding/Database/UserInterface/GameCore/Startup logs copied byte-for-byte with SHA256, consistent read-only SQLite backup of Mods database (including group settings), extracted Last-enabled-list.tsv and manifest. Live files/config untouched. Logs have21:25:30 mtimes matching crash wall time. Startup21:15:10 matches crash procLaunch21:15:07; PID39989. Modding ends with Stage: Initializing a new game, not loading old save.

Last two Enabled Mods blocks each50 entries. Includes39 official-content entries and these11 third-party entries:

- Mods Title Localization
- Enhanced Mod Manager
- Larger MODinUse Area
- Better Trade Screen
- Specialization (Scotland test)
- HD Civilizations and Leaders
- HD Civ6 Plus
- HD District Expansion
- HD Industries and Corporations
- Leugi Monopoly++ Corporation and Product Adjustments
- Leugi Monopoly++ Tycoons and Investors

No Switch Civilization in this set. Official mode availability is not evidence modes were enabled in match. Full exact UUIDs retained in TSV; UI labels may differ. This is the captured test configuration, not a final user-wide enabled list.

## Crash signature

EXC_CRASH/SIGABRT, signal6, abort called. Faulting thread7 TBB WinID5: __pthread_kill → pthread_kill → abort → abort_message → __cxa_pure_virtual → Civ6 image offset9223148 → libtbb workers. This is a native C++ pure-virtual-call termination path, not a named Lua exception or explicit memory-pressure kill. Object lifecycle/race/corruption are hypotheses, not diagnosed causes. No Lua module named on faulting stack; no proof HD, Specialization or a particular addon caused it. A separate thread waiting for Metal drawable does not establish graphics as cause. Crash vmSummary is virtual-region accounting, not comparable to prior physical-footprint measurement or proof of9.7GB RSS.

UserInterface/GameCore text search found no error/exception/assert/failed lines. Database has errors including missing localization trigger JNR_UC_THR_LocalizedText_Districts_en, FK and duplicate localization keys during initialization. These are preserved compatibility leads, NOT a demonstrated chain to the later TBB abort. No Lua.log existed in the inspected native Logs directory. Do not conflate this idle abort with prior construction-list crash without its matching signature.

## Next

User can restart and verify11-item list; originals now safe from log rotation. Reproduce unchanged configuration first and retain matching session/approximate turn, idle interval and whether any action preceded crash. No request to add/remove further items simultaneously. No code fix, deployment, memory attachment, game launch or config write this batch. Raw crash report contains private machine identifiers and stays outside Git; only this summary committed.
