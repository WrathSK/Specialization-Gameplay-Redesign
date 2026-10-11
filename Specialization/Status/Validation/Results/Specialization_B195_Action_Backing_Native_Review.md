# B195 — recessed action backing alignment

**USER_GAME_TEST_FAIL for the shown backing alignment only.** One uploaded crop was visually reviewed: a selected Settler has two custom found-city-style actions whose recessed backing sits below the adjacent native action backing and reaches into the lower frame. The user independently identifies this mismatch. This is not an Expedition binding/activity failure and does not certify all other B195 icons or layout states.

The inspected native UnitPanel art/action-stack coordinate relationship and our bottom-anchored ActionSlot identify a reversed vertical offset. B196 changes only that decoration from `Offset="1,-2"` to `Offset="1,2"`, moving it upward four UI pixels. Button bounds, prepare/confirm ordering and execution are unchanged. Pixel alignment still needs the small native visual check; a local coordinate assertion is not rendered evidence.

Last recorded runtime under test is B195.222/modinfo222, source65f0038, receipt `B195.222-65f0038-playtest.json`; this review does not re-audit the external runtime. [Original B195 local result](Specialization_B195_Action_And_Project_Icons_Local.md) remains unchanged. B194 observed activity/timer/release evidence remains separate.

The original was moved, without renaming or overwriting, to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B195/2026-10-10/`. Pre/post SHA256 matched; the local manifest links this report. Raw pixels remain outside Git.

- `Screenshot 2026-10-10 at 10.52.15 PM.png`: 521305 bytes; SHA256 `df11eab0399f220946894fecea31f21cea542b407eecf7ee85156b0491beb8e8`.
