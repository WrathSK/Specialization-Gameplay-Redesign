# B186.213 — Expedition arrival lookup and identity diagnostics

Date: 2026-10-10. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** User explicitly approved the bounded patch after the [B185 native review](Specialization_B185_Expedition_Identity_Native_Review.md). This implements that proposal only; original native/local evidence stays frozen.

## Cause and bounded change

B185 sought arrival through old-ID lookup and physical plot occupants, but displayed the returned unit using the player's unit collection. Actual-module counterexamples showed that a preserved marker on a Spy absent from plot occupants and a genuinely missing marker could produce the same unbound display. The lookup/reporting gap is confirmed; native marker loss and literal engine delete/recreate remain UNKNOWN.

- [Gate](../../../../Mod/ExpeditionSpyGate.lua) now enumerates the player's exact prototype collection while travel is pending. A candidate must have the original surviving unit marker, correct owner/type, the expected destination, and valid source/target references. The exact `FindID(candidateID)` object must independently pass ID, owner/type, marker and position checks. Extra prototype units or duplicate marker matches block acceptance.
- No adoption by name, a lone unit, position or ID arithmetic; no marker copying. Marker absence/mismatch/unreadability retains the existing source and capacity reservation, with the existing arrival grace period and held-state protection. Exact-type explicit END is unchanged.
- Physical plot membership is diagnostic-only for arrival. Pending travel performs one player-unit collection scan per observation. A READ reuses its one collection result; ordinary task turns after arrival still use the tracked unit/source directly, with no all-unit scan. This is a bounded correctness change, not a demonstrated native performance improvement.
- [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua) shows a short marker/readback/plot/source summary. Unbound cases add created/tracked/observed IDs, actual lookup IDs and sampled/due turns. Raw marker contents are not exposed. Retained source is shown explicitly as unverified binding, rather than omitted. Throwing old-ID reads cannot discard the other diagnostics.
- Diagnostics are bounded current-request scalars; no history buffer, new persistent field, extra Property write, recurring UI read or new task is introduced. Creation still writes exactly one unit marker. Native travel, independent no-reward timer, ordinary-Spy UI routing, own cap1 and the temporarily accepted native-slot cost are unchanged.

New localized suffixes under `LOC_SPC_EXPEDITION_SPY_`, in Chinese and English: `RETAINED_SOURCE`, `IDENTITY_SUMMARY`, `IDENTITY_IDS`, `IDENTITY_LOOKUPS`, `IDENTITY_TURN`, and status suffixes `IDENTITY_MATCH/ABSENT/MISMATCH/UNREADABLE/NO_UNIT/NO_SESSION/WRONG_UNIT/AMBIGUOUS/PRESENT/OFF_MAP`. No new button, layout asset or icon. The later native-icon reuse preference remains on hold.

## Local validation and evidence boundary

**81 test methods PASS:**14 new [binding tests](../../../../DevelopmentTests/test_expedition_spy_binding.py),31 current gate/reader/window/package checks,26 identity/timer/UI checks and10 P0-panel checks. Actual Lua runs under Lupa Lua55; unchanged unit SQL is applied only to an in-memory copy of the explicitly configured read-only HD DB.

New counterexamples cover plot omission/unavailable/throwing; absent/wrong/unreadable markers; old/new ID aliasing, missing/throwing lookups and a different exact-lookup object; source/target invalidity; duplicate markers and old prototypes; reserved capacity; unchanged exact END; repeated notification idempotence; retained-source UI; one pending scan versus no arrived task scan; and refusal to invent binding in a cold session. Existing tests retain normal Spy protection, no-reward task timing, native UI pass-through and no extra native mission/reward calls.

One initial new UI assertion expected due turn83, but the inherited UI fixture intentionally reports travel3+establish1 from turn81, i.e.85. The test expectation was corrected to the fixture, without changing timing code. Independent code/test review found an unprotected old-ID read in snapshot; it was guarded and the throwing-FindID/GetID counterexamples now pass. No assertion was removed to bypass a failure.

Package/XML/localization, Lua syntax, changed-document links/anchors, current selectors/context/hash integrity and diff are checked for this checkpoint. No full gameplay regression, stress or new native observation occurred. Native marker survival, task isolation and cleanup are still pending; local success cannot prove them.

## One minimal native session

After deployment of **B186.213**, use the existing Culture IV fixture. If an old prototype remains, first use **结束并移除验证团**. Keep other Spy missions idle during the short comparison because the existing mission-event counter is player-level. No save/restart ritual is required; saved journey reconstruction is not implemented.

1. **专业化诊断 → 人文考察·验证 → ① 创建Spy验证团**, choose the same target, then **② 读取派遣与情报隔离 → ③ 原生派遣**. After the shown arrival turn, click **刷新报告**. Expected: arrival accepted, source verified, own count1/1. The created/native IDs may differ only with matching marker and exact readback. If unbound/held, capture the identity summary/details and stop this route. This distinguishes a plot-lookup gap from marker loss or unreadable identity evidence.
2. If bound, click **④ 无奖励任务（2回合）**, close the window and advance the two shown player turns. Refresh: completion1/1, reward none, native operation-1, source turns unchanged (0 if baseline0), mission-event delta0, no native/HD reward notification. This tests the previously unreached independent timer, not Gain Sources execution.
3. **结束并移除验证团**, then **刷新报告** after publication: own count0 and native used count back to the initial baseline. This checks exact cleanup of the returned identity. Original-button routing already has scoped user evidence; inspect it only incidentally. No new ordinary Spy needs to be created for this session.

Unknown fields remain UNKNOWN. If the marker is absent, this patch must not recover it by guessing or copying; the next identity approach requires its own evidence and approval. Formal training, persistent journeys/reattachment, N2/N3, rewards, era UI, Design, Store schema, GC and main are unchanged.

## Source and runtime

Source checkpoint: **B186.213 / modinfo213**. At local validation, the last deployed package remains B185.212 (`4d8ace2`, receipt `B185.212-4d8ace2-playtest.json`). Deployment and exact source commit are recorded separately in current Status/Authority and the deployment receipt; this report does not infer runtime from HEAD. Stop after the guarded deployment and wait for the one-session evidence.
