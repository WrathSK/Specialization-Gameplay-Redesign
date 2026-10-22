# B196 — explicit UI accepted; native-style sidebar reference retained

**USER_GAME_TEST_PASS for the reported B196 UI/input flow.** Five uploaded images were visually reviewed. The user states everything seems to work, identifies images3/4 as the desired UI and image5 as after mission completion, and explicitly confirms the Settler UI fix passed without an image. Functional acceptance does not mean the central prototype window is the desired final visual layout.

## Evidence and result

| Evidence | Direct observation / user statement | Scope |
|---|---|---|
| Image1, T86 | Custom **派遣到新城市** window; team艾莉森, sourceEdinburgh(Test), 待派遣; target selector currently斯巴达; 确认派遣 and two unit actions visible | Normal dispatch page and native artwork render in the shown setup. The displayed choice does not establish which target was finally submitted. |
| Image2, T88 | Selected custom expedition艾莉森 at东京; no unit-action buttons and no automatic report window visible | Consistent with the intended controlled-task empty action bar. The image contains no phase/timer readout, so it is not an independent raw SLEEP/timer measurement. |
| Images3/4, T88/T90 | Ordinary-Spy reference UI: **派遣间谍** city list, then **选择任务** task cards in a docked left panel; selected name埃伦 differs from the expedition | Explicit user presentation references, not evidence that B196 implemented these pages or that native espionage callbacks leaked into the custom team. |
| Image5, T90 | Custom expedition艾莉森 selected; two actions present and unavailable. Hovered **派遣到新城市** explains the one-task prototype limit and P0 END | Matches the expected completed one-shot UI. User explicitly identifies it as post-completion; no repeated mission/redispatch is expected in this build. |
| User overall report | Everything seems working fine | Accept the reported explicit entry/travel/task/locked-action/completion flow. Unpictured interaction is USER_REPORTED evidence, not inferred from a still image alone. |
| User Settler confirmation | UI fixed; no screenshot taken; explicit PASS | **USER_REPORTED_PASS** for Settler recessed backing. Do not request an image solely to repeat this check; no separate native crew run or all-scale certification is inferred. |

This closes the minimal B196 gate. [145 focused local checks](Specialization_B196_Expedition_Explicit_Actions_Local.md) remain local evidence; [B194 native activity/timer/release](Specialization_B194_Expedition_Pending_Activity_Native_Review.md) remains inherited. These images do not newly prove precise native mission/source-reward isolation, END deletion, all screen scales, cold-load reconstruction, formal training, reattachment or repeatable missions. No such retest is required for this unchanged prototype lifecycle.

## Presentation direction from images3/4

The desired normal interaction is a **docked left sidebar**, leaving the map visible, with a city list for dispatch and vertically arranged task cards for missions. Native frame/header/close treatment, compact icons, row spacing, selection and unavailable states are the visual references. This is more specific than merely placing Spy icons on a central diagnostic-style window.

Carry this direction into the [existing UI plan](../../../Architecture/v2/P0_N_Expedition_UI.md#b196-feedback--native-style-sidebar-reference). Reuse presentation where safe, while keeping our explicit actions, own capacity/source binding, independent timer and task-time input isolation. Native success/detection percentages, espionage rewards and mission callbacks are not part of this preference. Native target lists also do not expand the current prototype's eligibility. The user has supplied a presentation direction, not a new implementation authorization or a new Gameplay decision.

Image5 is expected prototype behavior, not a defect request: completion releases task activity but does not enable a second task/redispatch. P0 **人文考察·验证 → 结束并移除验证团** remains the recovery/cleanup entry. Formal lifecycle work stays a separate future batch.

## Archive and runtime provenance

Last verified deployed package: **B196.223/modinfo223**, source `e6e19e545eb0cc388c7418de62f55615c0ce0412`, receipt `B196.223-e6e19e5-playtest.json`; the prior deployment checkpoint recorded213/213 equality and retained B195/stable recovery. This documentation-only review inherits that receipt and does not re-inspect or replace the external runtime. Main, Mod, Design, tests and frozen prior results remain unchanged.

All five originals moved without renaming/overwriting into ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B196/2026-10-10/`; pre/post SHA256 matched. Local manifest associates image roles and this report. No raw image is committed.

- Image1 (B196_TEST): `Screenshot 2026-10-10 at 11.11.07 PM.png`, 12862034 bytes, SHA256 `0076f6d08f03c1823b5f9bf2046c8a4fce1dba928665e8b9934c33d7a27ba264`.
- Image2 (B196_TEST): `Screenshot 2026-10-10 at 11.12.40 PM.png`, 14751580 bytes, SHA256 `36084f47717e08a21596bbc4f96e03a0d3e855ed416f3896edfbc9f149c86b77`.
- Image3 (UI_REFERENCE): `Screenshot 2026-10-10 at 11.13.27 PM.png`, 14302563 bytes, SHA256 `7f154a16f94aefc123947c8ca1fb83cb671cf5749e214b13d96167a3c29ec367`.
- Image4 (UI_REFERENCE): `Screenshot 2026-10-10 at 11.14.40 PM.png`, 13052329 bytes, SHA256 `61f9c152bc68ecb10bf29d5d73e98ab1e03f4f8e5fa0b3fd8e76c22d3f43a76e`.
- Image5 (B196_TEST): `Screenshot 2026-10-10 at 11.15.02 PM.png`, 14971163 bytes, SHA256 `f25615a1eed0ec733f99fecbc8bc75bf2bcc64e97e9aa82fb916825519d23f4d`.
