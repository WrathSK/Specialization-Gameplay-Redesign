# B268 — Approved raw artwork integration

Status: LOCAL_SIMULATION_PASS / FIXED_BINARY_REVIEW_COMPLETE / USER_GAME_TEST_REQUIRED
Build: B268.295 / modinfo295. Design D0057 and Architecture A0178 remain the accepted gameplay/structure basis.

## User authority and selection

The user approved the right-hand alternative in all four comparison groups (01-06, 02-02, 07-02, 14-08), all thirteen remaining listed selections, and direct replacement. The source originals remain ignored, local-only and untracked; no original PNG publication or deletion is included. Only derived runtime DDS files are candidates for a fixed-file publication exception.

| Selected ID | Runtime use |
|---|---|
| 01-06 | EXPEDITION |
| 02-02 | RESTRUCTURING |
| 03-09 | CREW |
| 04-01 | TASK |
| 05-01 | WORKS |
| 06-01 | CREW_PREPARE |
| 07-02 | CREW_CONFIRM |
| 08-01 | LIQUIDATE |
| 09-02 | CONFIGURE |
| 10-05 | INVEST_PREPARE |
| 11-05 | INVEST_CONFIRM |
| 12-02 | COMMERCE |
| 13-05 | CAPITAL |
| 14-08 | DEVELOPMENT |
| 15-02 | DIALOGUE |
| 16-02 | ENGINEERING |
| 17-01 | CLAIM_MARK |

## Implementation and boundary

`tools/raw_icons_manifest.json` fixes the seventeen source hashes; `tools/build_raw_icons.py` checks them before reading pixels and writes deterministic lossless BGRA8 DDS, SQL and the build manifest. Source alpha>=8 bounds, aspect-preserving fit within86% of each cell and centered transparent margins are the only shaping operations. The investment pair shares union bounds and therefore the same transform. Existing raw colors, silhouette/candidate choices and subject geometry are preserved. There is no new image generation or whitening.

Eighteen exact-size atlases cover12/16/20/22/24/30/32/38/40/48/50/64/70/80/95/128/200/256 cells,5 columns by4 rows. Every DDS was independently decoded by Pillow and compared byte-for-byte in RGBA to its pre-encode atlas. New icon definitions load after the previous aliases in both frontend and in-game contexts. All27 Crew project variants, seven supported unit kinds with base/portrait/WHITE/FOW variants, the five action-project icons and custom unit/mission buttons are covered. Legacy Expedition Gate/Zero and unrelated native definitions are preserved.

Prepare/confirm remain separate steps. Restructuring chooses the liquidation/configuration artwork from its current action, and uses that action's artwork for both preview and confirmation. Expedition destination travel, target-civilization and individual-wonder icon semantics remain native. WORKS substitutes the selected artwork only in UI rendering, including its20px strip.

Claim icons use exact native district definitions with the approved mark overlaid by an Image child in the production list, queue, current-production view and city-banner production slot. Original district textures are packed in BLP resources; no guessed extraction, native-pixel redistribution or recreated district drawing is used. The existing LevelBanners UI context owns the template and listener. Native controls keep input, sizing, tooltip and production behavior. Non-claim recycling hides the mark; shutdown guards destruction of cross-context children. The decorative mark is quantized to a real available cell, and cell/control dimensions always match the [B256 native correction](Specialization_B256_Icon_Size_Repair.md). **The Civilopedia retains the native district base without the overlay; its independent display adapter is outside this minimal integration.**

No gameplay state, Property/schema, requests, eligibility, settlement, unit models/animations, timer policy, player access or configuration changes. Existing institution and city-level badges are unchanged. Unit flags retain native player-color multiplication; raw rendering may therefore differ by player colors and remains a native visual check.

## Evidence and validation

The prior B267 quick acceptance contains627 contiguous diagnostic records through turn6. All four professions reached Potential4/ACTIVE4, and their final institution facts were applied to UI. Startup writer gates were ready after load; Culture network subsequently ready/verified. One partial-frame capture was backfilled by the ring, with no sequence gap; the fallback error sink exhausted its own quota while meaningful collection continued. The final diagnostic META has suppressed=0/errors=0. This is scoped activation/presentation evidence, not full ability, yield, reload or pillage acceptance. Raw session evidence remains ignored and unmodified.

LOCAL_SIMULATION_PASS:28 selected methods: new artifact/SQL/actual-Lua tests, the existing Restructuring UI methods and Expedition SidebarRouting methods. Actual UI tests preserve the two-step request/plan guard, select distinct approved icons, retain phase-dependent Restructuring confirmation, and hide/reuse/clean claim marks. DDS hashes, payload dimensions/masks, atlas gutters, required sizes, package closure, native/legacy icon invariants and repeated RawIcons loading are checked. All188 Lua files compile under Lua5.1;32 XML/artdef/dep/modinfo files parse; both added Python sources parse.

An additional historical UnitPanelActionLayout run was examined, not rewritten: two assertions still demand the deliberately replaced native placeholder icons; three behavior failures reproduce when the unchanged HEAD UI source is substituted in memory. They are excluded from the passing count, not claimed fixed. B268's current structured-view action fixture checks the edited presentation/dispatch boundary; unchanged gameplay executors receive no new gameplay PASS.

USER_GAME_TEST_REQUIRED: inspect native32px list icons,38px actions,40px missions,95px portraits/flags and scaling; check ordinary/disabled/prepared/confirmed states and recycled claim rows; verify actual claim overlay startup/placement/click-through. Some detailed raw images are intentionally busy at20–32px. The provided local preview is a raster-size inspection, not game rendering. No game launch or configuration change occurred.

## Publication and deployment checkpoint

Prepared DDS files:18; total bytes:12640144; all decoded pixels MATCH. Fixed bundle SHA256: `a728ec540753a01cd5433038b37854f8c4668f4395ee780551e78f62f1df2766`. [Exact per-file hashes and dimensions](../../../../tools/raw_icons_build.json); [approved source selection](../../../../tools/raw_icons_manifest.json).

`tools/README.md` requires separate publication review for binary files. Primary completed the separate, narrow binary review under the user's explicit selected-art replacement authorization: independent visual/source mapping review, fixed per-file hashes, DDS header/payload checks, and independently decoded RGBA equality to the generated atlas. Each DDS contains only the approved image pixels and a fixed128-byte DDS header; there is no embedded PNG metadata, original game texture, local path or added textual payload. The18 exact files in the linked manifest are the sole publication exception; changed/regenerated bytes require review again. The24 text paths passed the normal staged gate, which is not a binary scan. A command-local hook exception may publish only this reviewed fixed bundle with those checked texts; no checker, hook, config or long-term protection rule is changed. No runtime replacement, PR, main promotion or release tag has occurred. Live remains B267.294 under its existing receipt until commit/publication and guarded game-exit deployment checks complete.

User decision: none outstanding within the explicit replacement scope. User testing: native raw-art acceptance after activation. Primary next: commit/push the exact reviewed batch and use the existing temporary-playtest transaction if the game is fully exited; otherwise defer activation.
