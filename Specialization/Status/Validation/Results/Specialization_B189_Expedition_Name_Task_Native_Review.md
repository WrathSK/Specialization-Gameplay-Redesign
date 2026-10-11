# B189.216 — native name continuity, source binding and independent task

Date: 2026-10-10. **USER_GAME_TEST_PASS within the observed session:** native personal-name continuity, accepted arrival with original source, and independent two-turn completion without the observed native mission/source effects. **END: USER_GAME_TEST_PASS, user-reported only.** Automatic task activity/needs-orders suppression is **not implemented**; the user reports manual idle/sleep action is still necessary. This is not formal N1 completion or a persistent identity proof.

Source `b2b945f3d720689f4b1c3dfd61f853a93a2e423e`; documentation baseline `b64e0731bdea3cfb1d9d452a4dc9bddc1f1a9b96`. Recorded live receipt remains `B189.216-b2b945f-playtest.json`, last verified211/211 MATCH. This review neither re-verifies nor changes the external runtime. [B189 local evidence](Specialization_B189_Expedition_Native_Name_Local.md) and earlier failed attempts remain frozen; no local tests are rerun for this documentation-only checkpoint.

## Individually inspected evidence

| Image / turn | Visible facts | Supported conclusion |
|---|---|---|
| 1 / 7.55.38 PM / T86 | Native dispatch in progress; pool CIVILIZATION_SPC_TEST40; confirmed/current native name **艾莉森**; own cap1/1; team3276829 off-map(-9999,-9999); source **Edinburgh (Test), city393220**, binding retained | Native nondefault name was confirmed before dispatch. This first image is already in transit, not a capture of the instant of assignment. The cached preparation observation's off-map count0 is not a live census during travel. |
| 2 / 7.56.43 PM / T88 | Arrived at斯巴达(23,15); created3276829→current3342365; name艾莉森 retained, collection/exact lookup names MATCH, plot contains team, source reference MATCH; source stillEdinburgh (Test), own cap1/1 | The observed native name survives the public-ID change and the prototype accepts the returning team with the original source. City-name text is not the source authority. |
| 3 / 7.57.16 PM / T88 | Independent task running; startT88/dueT90; completions0/1; rewards none; source turns0→0, native operation-1, additional native mission completion events0 | Independent task starts without starting a native espionage mission. |
| 4 / 7.58.40 PM / T89 | Same named/bound team; completions0/1; source turns0→0, native operation-1, events0/NONE | Task has not completed early after one turn. |
| 5 / 7.59.26 PM / T90 | Same named/bound team; completions1/1; source turns0→0, native operation-1, events0/NONE | Task completes at its two-turn boundary; no Gain Sources duration or mission completion event appears in the observed diagnostics. The team is still present in this image. |

After clarification, the user confirmed clicking **结束并移除验证团** worked and the team disappeared; they omitted a screenshot after many prior tests. Record this as user-reported END success, **not** a viewed post-END0/1 report or measured native-slot-count release. No repeat is requested.

The visible ordinary-Spy fields remain maximum5→5, ordinary count0→0 and source trainableyes→yes. The custom unit's native Spy count is1 during the task. This supports the existing fixture and the temporarily accepted slot cost; it is not proof of fully independent native Spy capacity or all ordinary-Spy combinations. A same-tile other-unit count1 is visible, but is not a new hostile-contact immunity test.

## Interpretation and limits

- **Continuity:** successful for this newly created, uniquely named test-civilization team and journey. The public UnitID changes; this does not prove the engine literally deletes/recreates its internal Spy record. Names are a bounded session continuity candidate with existing ambiguity checks, not a globally unique permanent registry.
- **Source/capacity:** original source reference and cap1 readback remain correct across travel/task. The source is the independently retained exact city record, not the selected city or the personal name. No permanent city Property or capacity rules changed.
- **Task isolation:** UI reads `GetSpyOperation()==-1`, Gain Sources remaining0→0, and the observed player-level mission-completion counter stays0. [Gate](../../../../Mod/ExpeditionSpyGate.lua)305–313/185–193 writes only its own start/due/completion fields and has no reward writer. Together these support the scoped no-native-mission/no-reward prototype. They are not an exhaustive audit of every hidden native/third-party side effect or a formal N2 reward implementation.
- **END:** user-confirmed removal; no extra claim about post-END diagnostics that were not captured.
- **Busy state:** user's report of manually putting the unit to rest is consistent with source. The independent timer never submits sleep/hold or another activity operation. The custom unit panel currently offers management plus **SKIP_TURN**, not a task-owned native busy state; do not assume the user's word “sleep” identifies the exact operation used. Completing the timer does not imply needs-orders integration is complete.
- **Unchanged limits:** no save/load reconstruction, formal training, reattachment, multi-team registry, N2/N3/U2/rewards or general war/target-transition acceptance is added by this session.

## Next bounded proposal

See [task activity investigation](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#task-activity-investigation--after-b189). Preferred technical candidate: a verified, task-owned native SLEEP state plus exact-type input isolation and internal release, while the existing Gameplay timer remains authoritative. It is not ordinary player-controlled sleep and not Gain Sources under a different label. Native custom-Spy eligibility and wake behavior remain unproved; implementation requires approval.

No new user test now. A future approved activity patch should test only start→no manual idle action/no wake control→two turns with the window closed→completion/normal management restored, with other units' order prompts preserved. It should retain current no-reward/name/source checks and stop on unsupported activity rather than force end turn. New sleep persistence must be considered explicitly during implementation; today's session-only timer cannot reconstruct a saved task.

## Archive and checks

Ignored archive: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B189/2026-10-10/`. All5 originals were visually read, moved without renaming/overwriting, and verified by pre/post SHA256; manifest links them to this result. No screenshots or raw game files enter Git.

- `Screenshot 2026-10-10 at 7.55.38 PM.png`: 13344010 bytes; SHA256 `f02bbe10ef7ea8302ef01bee5652e5fccf9455dfbb25bdce8a3de65bfaf83c2f`.
- `Screenshot 2026-10-10 at 7.56.43 PM.png`: 13448969 bytes; SHA256 `13a57ab4241bf74f95e9c0d3248eec0b887945449ea1404b72d96a45147c75db`.
- `Screenshot 2026-10-10 at 7.57.16 PM.png`: 13448458 bytes; SHA256 `4c9c7dfbcfe373aead643e3d069317d2eb170bcba4158746dac42ca9a9239bbe`.
- `Screenshot 2026-10-10 at 7.58.40 PM.png`: 12536054 bytes; SHA256 `a2a43f52f0aafcba5df6f12b8b606807aaf54a031fa9de46f232a76953106bfa`.
- `Screenshot 2026-10-10 at 7.59.26 PM.png`: 13115389 bytes; SHA256 `e445024e3af07b724219d286faacc421eec5cf8cfc23dbf3255131db36314d65`.

Only this evidence, the existing technical report/current navigation and reviewed metadata are updated. Checks: changed/new Markdown links and anchors, current section selectors, P0-N1 context/schema/hash integrity and diff/allowlist review. Mod, tests, Design, prior frozen results, runtime, main and GC remain unchanged. No game launch, deployment or gameplay regression.
