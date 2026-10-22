# B108.135 E2 — native initialization failure

Reviewed 2026-09-27. USER_GAME_TEST_FAIL for the new-game progression/readability checkpoint; later investment/isolation/coldload assertions NOT_RUN. User stopped after B/C completed districts. Two original screenshots visually reviewed, archived externally under `Specialization/Status/Validation/Evidence/B108_E2_Initialization_Failure_20260927`; manifest records original filenames/bytes/SHA256, 2/2 unchanged. No runtime or save edited; no deployment or game launch.

## Observed evidence

Both images show P0-B-108.135, Turn1, and `B033 progression UNKNOWN` with `CityProgressionStore.lua:623: function expected instead of nil`. At16:13:30 the selected city is Edinburgh (Test); at16:13:34 it is Aberdeen (Test). Both show the same failure chain: line623 initialization → stored error → check512 → find656 → requireCity662 → store.Base668 → EffectiveFacts.Read. B033 is an inherited diagnostic label, not proof that an old B033 package is deployed.

User says these are B/C after district completion; screenshots confirm unreadable specialization, not the exact construction event sequence or a successful registration. No A-city report, investment or coldload evidence was submitted. Do not infer loss of stored records or permanent save corruption from UNKNOWN alone.

## Narrow static correlation

Canonical B108 line623 invokes `GameConfiguration.IsSavedGame()` inside the new-game initialization pcall. Lines619/639 retain failures; check512 rejects later reads. This explains a common initialization failure reaching both cities rather than proving two distinct district-classification bugs. Classification: NATIVE_INITIALIZATION_API_BOUNDARY. The precise native binding/context cause behind “function expected instead of nil” remains investigation-required; this is not yet proof that the Lua table member itself is nil. The deployed file was not independently hashed in this review; image build/line matches recorded B108 source.

The existing local test supplies `GameConfiguration.IsSavedGame` as a mock function. It also removes that mock in a negative case and checks no properties are written. Those tests establish local behavior/fail-closed safety, not availability of the real Gameplay-context API. Prior FrontEnd LoadScreen usage was STATIC evidence only; the plan explicitly left native initialization unconfirmed. Local PASS is retained at its original scope, not promoted to native PASS.

## Disposition

Stop the current test; do not request investment/save-load repetition while initialization is broken. Proposed next repair scope: establish a positively confirmed new-game/load signal available in the actual context, preserve old/unknown-save no-write guards, and replace the verbose repeated traceback with a short actionable initialization report. No unconditional “missing index means new game”, no restored migration fallback, no Claim/F or Design change. Repair and any subsequent deployment require the applicable authorization and game-exit gate; this review does not implement them.
