# B099 E2 partial native evidence / in-session load crash — 2026-09-25

User confirms trading the city to AI, saving, then loading from inside the running game (not a cold process restart). No code/Design/deployment changes in this review.

## Evidence

External archive: app-support `Specialization/Status/Validation/Evidence/B099_E2_Transfer_Crash_20260925/`; six original screenshots moved with matching SHA256, supplied crash report, 70 current log files and two T13 manual saves copied with manifest. Original save files untouched; exact user-selected filename not confirmed, two candidate saves preserved by timestamp. All observations below are T13.

| Time | Observed |
|---|---|
|06:19:46|ACK; city262146 RESEARCH; Potential2, ACTIVE2 KNOWN, completed investment1, pendingfalse, Ledger PRESENT|
|06:19:48|Governor ACK; present/established1; title thresholds2/3/4 all1, ceiling4. Old raw-role UNKNOWN lines come from legacy Probe.Role with no persistent writer, not proof current permanent ledger lost|
|06:19:52|Specialists ACK; campus workers2, complete true; support actual RESEARCH, changes2/errorNONE, retiredRemoved0/errorNONE|
|06:20:12|Game progression record active, old City writer frozen; RESEARCH P2/A2, investment1, pendingfalse|
|06:20:27|ACTIVE record rev2, origin/current0/262146 @28,34; token DEV-B013-P0-3 matches; support/housing/GPP carrier counts1/3/1; network VERIFIED epoch1 input11 derive11, source/receiver true, routes2|
|06:20:58|HELD_TRANSFER rev3, current3/131073 @28,34, token nil; permanent RESEARCH/P2/investment1 retained; ACTIVE inactive/UNKNOWN; confirmed loss3/131073; exits PARTIAL_HELD22/23, checked2322 IDs/removed0; support/housing/GPP0/0/0; old source/receiver false, routes0; network VERIFIED epoch1 input13 derive12|

B099 basic request/gate repair USER_GAME_TEST_PASS for these three diagnostic replies and readable current facts. Does not certify every ability formula/native settlement.

Confirmed transfer and in-session permanent-record retention PASS for this one traded city. Withdrawal is PARTIAL, not full PASS: all21 carrier-set readbacks account for2322 checked IDs, but23 registered exits include NetworkBridge and YieldCarrierProbe. Screenshot omits per-module exitErrors; cannot identify the unfinished module from22/23 alone. Removed0 means callbacks found no carrier to remove, so no proof native RemoveBuilding executed successfully here; engine transfer/other updates may already have removed them. Visible research carriers absent and old network membership absent are narrower positive observations.

## Blocking boundaries before any recapture claim

1. TECHNICAL_IDENTITY_BOUNDARY: live city token became nil on transfer. Saved original token still exists, but B097 requires the same live token on recapture. No recapture attempted/observed; cannot certify automatic token restoration or copy it to bypass the gate.
2. WITHDRAWAL_COMPLETION_BOUNDARY: PARTIAL_HELD22/23. Need existing module error/reason exposed before choosing a repair; no broad carrier deletion.
3. DIAGNOSTIC_REFERENCE_BOUNDARY: NativeDescribe selects old player's Network bucket but indexes current foreign cityID without owner/reference match. Screenshot row shows owner0/city131073 @28,29, DEV-B013-P0-2 ACTIVE3: different from target owner3/city131073 @28,34. This row cannot prove stale target Network replay. Its owner-safe lookup needs a minimal diagnostic fix; current source/receiver check uses original target IDs separately.

## Crash

PID2456 Civ6_Exe_Child, ARM64; 06:21:51.1916 -0700; WinMain thread2; EXC_BAD_ACCESS/SIGSEGV, KERN_INVALID_ADDRESS0x1c8. Unsymbolicated main-executable offsets begin9757596,9584540,11801696. No named Lua/mod frame identifies a cause. This signature differs from earlier __cxa_pure_virtual/abort reports; no same-root-cause claim. VM summary TOTAL11.7G/MALLOC9.1G are virtual-region figures, not measured RSS or proof of renewed55GB incident.

net_connection_debug records save06:21:32, load attempt06:21:39. LoadGameViewState ends with prior successful06:14 load; there is no new completed load phase in that file. This does not establish whether the crash occurred in teardown, deserialize, or Mod load callbacks. Database log includes other content/icon duplicate constraints; these are preserved, not attributed as crash cause. No Lua.log available. Native stack alone cannot attribute failure to Game Property, E2 withdrawal or HD.

Save/load round-trip: USER_GAME_TEST_FAIL in this in-session attempt (crash), cause UNKNOWN / NATIVE_LOAD_BOUNDARY. Cold restart load NOT_TESTED. B097 recapture identity, changed-governor ACTIVE recomputation and current-route rebuild after recapture NOT_TESTED. B096 full native withdrawal NOT_PASS. Claim gate remains closed.

## Next scope

Stop ownership tests for now; evidence/save copies preserved. Proposed next investigation: expose failed exit module/reason and correct diagnostic owner/reference lookup, inspect existing load/exit native calls against the new observations. No guessing token/cityKey or changing Design. A later single cold-start load of the preserved foreign save may distinguish hot-load failure, but not requested as immediate repeated testing. No Claim/F or production repair in this evidence review.
