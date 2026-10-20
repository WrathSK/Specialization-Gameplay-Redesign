# B259 — Measured badge and native Investment layout

## Scope and evidence

User authorizes investigation and direct repair after B258 screenshots. Other B258 repairs are accepted within observed scope: restored badge, active-first marker and prior sidebar changes; requested visual refinements remain outstanding. Two original screenshots are archived with before/after SHA256 under ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B258/`. Original records are unchanged. Latest steering also removes the repeated district-column city name and restores visible native left scrollbars for columns1/2.

## Measurement and implementation

Original3840x2160 screenshot, Edinburgh crop at(1940,1360),750x180: visible emblem top around y26 and segment bottom around137; defense-strip top around45 and banner bottom around139. These antialiased edges give approximately111px versus94px (1.18x), not subpixel precision. With the observed approximately1.875 physical-pixel/UI-unit scale, remove(111-94)/1.875≈9 units from the58-unit badge: use49px cell/control,49x53 root. Four10x4 segments at x1/13/25/37 and y49 preserve the6-unit bottom inset. Expected visible height is approximately94px. Bottom position and canonical update path remain unchanged. Other zoom/scaling still needs native visual review.

The existing approved B254 SVG raster is downsampled to196x196 (4x4 exact49px cells), lossless BGRA8 without mipmaps.153792 bytes; SHA256 `f4f3e925dd3f1d58027fdbd792099f64a7000a16c23b8fed859078ed6db3bcb6`. Decode matches raw pixels exactly; contact sheet reviewed. User approved this one fixed-blob publication exception. Existing assets and institution softness are unchanged.

Native reference: Base/Assets/UI/Choosers/EspionageChooser.xml DestinationChooserButtons:90-high drawer, centered Stack,285x41 confirmation at0,-3 and285x24 lightweight action at0,4. Reuse those dimensions/anchors/text treatment for Confirm and Refresh; no status text in the footer. Narrow-screen back navigation stays in the existing compact bar, replacing its duplicate Refresh while viewing details.

Window height returns to screen-height minus27 (its top inset), restoring the bottom edge. Wide secondary/tertiary column top changes150→148 from screenshot comparison (approximately2 physical pixels lower before); native appearance is not certified by this calibration. District city subtitle removed, district list begins54 below its column header. Columns1/2 retain native left scrollbars with AutoScrollBar=0 per user's explicit preference.

Fourth card “当前合同” follows “签约与延续”. It contains the most recent contract for the selected target/domain, status, approved amount and actual debit on separate lines. Existing stale/error/pending information is moved here unchanged, and disappears when cleared. Empty state is explicit. No monetary rules, transaction guards, shared data, gameplay, timers or persistent state change.

## Validation

LOCAL_SIMULATION_PASS:39 scoped methods: exact atlas/control geometry and existing asset hashes, canonical state/event tests, four-card measured flow, native footer XML, column bounds at five screen sizes, left scrollbars, no repeated city subtitle, error visibility/clearing, actual-receipt preservation, active-first ordering/selection identity, confirmation guards, package closure, SQL keys and Lua syntax. Historical equal-card/per-card-scroll/footer-error-position assertions are superseded; no full-suite PASS claim. UI fixtures do not render Civ VI textures or fonts.

## Native check

1. Inspect map badge: smaller main icon, bottom segments still aligned, top approximately at city-defense strip. No repeated investment required.
2. Open “发展投资”: verify column tops/bottoms, left scrollbars and district cards directly beneath the header. Footer should match native button proportions and contain only actions.
3. Select an existing contract: fourth card shows status, approved amount and actual debit on separate lines. Any naturally occurring stale/error message belongs there. No intentional new payment or induced error is required.

## Deployment

B259.286/modinfo286 DEVELOP_ACTIVE; source `acd0c0dfb96b0c3b25c0aa0385ba069256a74a90`; receipt `B259.286-acd0c0d-playtest.json`;279/279 MATCH; digest `a4c17e17df845e1ecb0cdfb4681a2156eb328ca0d149d67d83d74a516015fd70`. Fresh game-exit, exact B258 restoration and B259 activation verified; stable/outgoing recovery intact; no pending marker, game launch, main or configuration change.

39 scoped checks and279-runtime/899-context integrity checks PASS.17 source/text files passed publication scanning; exact DDS used its user-approved one-time exception. Native visual review pending. Main/stable, institution softness and held gameplay/audits unchanged.
