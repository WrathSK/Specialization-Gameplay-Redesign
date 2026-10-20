# B264 — User acceptance and city UI investigation

## Scope and acceptance

The user completed the combined B263 neutral Roosevelt shell / B264 institution-tooltip review. Record **USER_GAME_TEST acceptance for that presentation scope**, with one intermittent Culture activation/availability anomaly below. The user also requested read-only investigation of a city-panel shortcut, then confirmed that the old profession/Potential entry below the P0 launcher can be removed in that follow-up UI batch. Neither request authorizes the proposed repair or button implementation. No PR or main promotion is authorized.

Source reviewed: `fed3225`, runtime `3da40dc`, B264.291/modinfo291. The worktree and Context Lock were clean/matching before investigation. This record does not change Mod, tests, Design, Architecture, configuration or deployment.

## Submitted evidence

Preserve the original ignored files in `local/diagnostics/B205/`:

| Session | Captured scope | records.log SHA256 |
|---|---|---|
| `session-20261020T131418Z-c49cac` | 129 unique trace records, 16 gate prints; turns 1–8 | `db31da9ef766601f072fa6fd8258f72e50b269864b10bd1b5885ff2a1d0c9027` |
| `session-20261020T135446Z-0921ea` | 332 unique trace records; turns 8–17 | `62a1e90e9a3532d30bfe3008c2768346b3069ea5e68b0412d243d17492094821` |

The first session starts with a retained-ring snapshot already containing turn-1 history. Neither session captures governor promotions or the selected-city presentation/admission replies at the moment of failure. The second collector reports two `PARTIAL_FRAME_AT_DEADLINE` passive-window boundaries; do not treat an empty alert summary as complete error coverage. Raw logs remain ignored and unmodified.

**User observation:** on the first turn the capital became Culture with Potential IV. After a level-I governor established, consecutive promotions reached level IV. Banner ACTIVE badge/segments and P0 facts were correct, but the Culture IV institution remained inactive and Expedition training was absent. Replacing the governor restored both. Later Research/Commerce/Industry checks were normal. No repeat test is requested.

**Trace facts:** in the first session, seq 70 shows the capital's Expedition production row at turn 3, with native cost 60; seq 76 reserves training and seq 91 completes identity confirmation. Arrival is confirmed at turn 6 (seq 106); the PEOPLE task succeeds for Brazil at turn 8, records a new Insight and returns to the centre. Seq 129 shows idle actions available after release. These establish later recovery in the captured run, not the missed failure-time governor sequence. The second session contains Commerce/network pending reads followed by READY/AVAILABLE states; no new investment payment-failure evidence is established by those read-only pending records.

## Refresh finding

**P0 clarification:** the actual `城市专业 / 潜力` callback sends `PROGRESSION_READ`; `Gameplay.lua` calls `EffectiveFacts.Describe`, which reads current facts. The user's P0 ACTIVE IV result is therefore evidence that the effective level was already IV at that read, consistent with the independent banner. Reading P0 does not publish or invalidate the separate cached `CityPresentationView` or training SYNC reply. The stale displays must be repaired; P0 should not be demoted as the explanation.

**STATIC_CONFIRMED:** all these consumers ultimately use the existing `EffectiveFacts.Read` / `Probe.GovernorGate` result, but their invalidation differs:

- [Banner projection](../../../../Mod/LevelBannerState.lua) directly marks governor assignment/establishment/promotion/change and drains on native publish/playback completion. It does not require a carrier/property write to notice ACTIVE.
- [City presentation reader](../../../../Mod/UI/CityPotential.lua) marks its selected-city request dirty only when city, turn or `SPC_RuntimeUIRevision` changes. It does not subscribe to governor changes or the banner's fact revision. [InstitutionOverview](../../../../Mod/UI/InstitutionOverview.lua) renders the returned `CityPresentationView`; re-opening the native details page alone does not obtain a new Gameplay reply.
- [Training UI](../../../../Mod/UI/ExpeditionTrainingUI.lua) caches SYNC eligibility against city, turn, `SPC_RuntimeUIRevision` and Expedition activity revision. Once a reply is consumed, ordinary refresh/publish notifications do not re-request eligibility unless that key changes. [Gameplay admission](../../../../Mod/ExpeditionTraining.lua) reads current ACTIVE when a new request actually arrives; the availability cache can prevent that request.
- `Probe.CreateBuilding`, `RemoveBuilding` and `SetProperty` advance `SPC_RuntimeUIRevision`. It is an owned-write counter, not a complete governor/ACTIVE fact revision. Native governor changes need not advance it when derived effects have nothing to change.

**LOCAL_SIMULATION_PASS / defect reproduced:** current Lua was executed in the existing isolated display/training fixtures, without editing fixtures or source. In both cases an initial ACTIVE III reply was consumed, ACTIVE changed to IV with city/turn/write revision unchanged, and ten further update/refresh drains retained the old inactive/hidden state. Incrementing only the write revision refreshed both the institution row and training availability. The institution case executed `CityPotential → InstitutionOverview → Institutions`; the training case executed the current UI adapter and Gameplay SYNC handler.

This confirms a shared invalidation gap and provides a strong explanation for the reported pair of symptoms. The native failure-time sequence was not recorded, so the exact event ordering in that occurrence remains unobserved. Governor replacement or unrelated effect writes can mask the gap, which also explains why later tests may succeed. This is a stale consumer result, not evidence that Potential or governor promotions were lost.

B264 changed institution formatting/localization plus build stamps only. `CityPotential`, training UI, EffectiveFacts, governor gate and banner event wiring are unchanged by B264. Keep the previously held Expedition mission-lifecycle investigation separate from this training-list refresh defect.

## City-panel shortcut feasibility

**STATIC_CONFIRMED, installed-source review:** native `CIV6_ASSETS/Base/Assets/UI/Panels/CityPanel.xml` and the installed HD `2465378070/UI/Replacement/CityPanel.xml` retain `ActionStack`. HD `DL.modinfo` identifies version 2.2; the existing Mod includes `DL_CityPanel` and preserves its implementation. Native action controls use 44×53 logical units, 32×32 symbols, 3-unit stack spacing and `UnitPanel_ActionButton` / `UnitPanel_ActionGroupSlot` artwork. These are logical dimensions, not Retina screenshot pixels.

The native `CityPanelOverview.lua` exposes `LuaEvents.CityPanel_ToggleOverviewBuildings`, `OnToggleBuildingsTab` and `GetSelectedTabButton`. Selecting Buildings calls `ViewPanelBreakdown`, the very surface extended by our institution category. HD's City Policies/Suk wrapper chain retains that tab/navigation route. The older `CityPanel_ShowBreakdownTab` emit in CityPanel is not the verified receiving path and should not be used without a receiver.

A small Mod-owned control can be attached to the existing action stack, using the existing 32px profession/ACTIVE badge atlas and native button base. No new artwork, binary exception, whole-panel replacement or gameplay operation is needed. The button should be visible only for the player's eligible specialized city, use the current fact projection, and explain its destination in a Chinese tooltip. An unknown ACTIVE must not be rendered as a fabricated level.

The native Buildings event is a toggle: invoking it while that same tab is open closes it. A guarded open-and-select wrapper must preserve the requested behavior: closed → open Buildings; another tab → Buildings; already on Buildings → remain open. It must keep native overview toggle state, selected city, Escape and HD controls intact. One additional button consumes approximately 47 logical horizontal units; native-scale layout/interaction still needs one visual check.

## Proposed next batch — not authorized

Proposed B265 combines only the following related UI work:

1. Repair the selected-city institution and Expedition admission invalidation. Relevant governor/fact events mark the affected result stale; native publish/playback completion obtains fresh authoritative facts/replies and updates both consumers. Preserve in-flight admission/token checks, capacity, costs, source binding and the actual Gameplay admission gate. Do not create saved state, manufacture an unrelated building write, poll more frequently or introduce timers/frame-based fact updates. Replace the touched legacy presentation polling driver with the bounded event/response path as needed.
2. Add the native-style ACTIVE shortcut to the city-panel action row, using the existing badge artwork and verified Buildings-tab route. Reuse current facts; preserve the original buttons and their geometry. Do not add the four-segment banner display to this button.
3. Remove the old profession/Potential badge immediately below the P0 launcher, as requested by the user. `UI/CityPotential.xml` owns the visible badge, but its Lua script also drives the shared institution read/notification path. Remove the visual entry while retaining that needed read responsibility in the event-driven presentation path; do not simply unload the context and strand the institution panel. Keep the P0 diagnostic launcher and reports.
4. Retain bounded diagnostics for affected city/fact revision, presentation reply ACTIVE and training SYNC eligibility so a future mismatch is diagnosable from the collector. Do not log every frame or every unchanged notification.

Local validation should cover same-turn III→IV with no effect writes, promotion/demotion/reassignment, duplicate notifications, stale replies/selection changes, and direct tab opening without accidental closing. A later minimal native check can combine one governor promotion with the new shortcut and training-row visibility; do not ask the user to reproduce the old failure before implementing an approved repair.

- User decision: approval of the proposed batch is still required.
- User testing: B263/B264 presentation accepted; no immediate extra test requested.
- Primary next: wait for repair/shortcut authorization. No implementation, deployment, PR or main promotion.
