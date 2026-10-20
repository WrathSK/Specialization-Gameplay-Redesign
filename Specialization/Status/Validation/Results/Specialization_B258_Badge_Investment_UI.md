# B258 — Map badge restoration and Development Investment sidebar

## Approved scope and evidence

The user explicitly authorizes the B257 missing main badge repair together with the pending Development Investment presentation refinements. **USER_GAME_TEST_PASS (B257, limited):** no-governor Potential-only investment refresh and four-segment bottom alignment. **USER_GAME_TEST_FAIL:** the main map badge is absent. Archived screenshot and SHA256 review: ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B257/`. Frozen B257 reports remain unchanged.

## Implementation

The rendering regression is isolated to the B257 Grid path; the exact native texture/slicing failure remains unproved. Restore the previously working Image SetIcon path with a new exact58px cell and58px control. Preserve the58x62 root,6-unit bottom inset, all four segments, canonical projection, commit notification and institution32px assets. No new timer, gameplay change or persistent state. Existing softness remains deferred.

The approved16 SVGs are rendered and downsampled into one lossless BGRA8 DDS,232x232,215424 bytes, no mipmaps. SHA256 `9d3277bca2704363223d7346592cbbcadd793883a851a2f190a1c0434258ad54`. Decoding reproduces all raw pixels exactly; contact sheet reviewed. The user approved the one-time publication exception for this exact blob. No permanent gate bypass.

Development Investment keeps the existing snapshot, confirmation and money protocol. Wide-layout secondary/tertiary columns start150 units below the window top, below the source summary. Equal column widths; headings left aligned. Detail cards use measured wrapped content heights and one right-side, auto-hiding overflow scrollbar instead of three left-side scrollbars. The building icon sits beside its name, above grouped quote values. Paragraph spacing and top inset prevent crowded/clipped first lines. Window bottom clearance12 units and footer padding keep both actions above the edge. Narrow-screen navigation remains supported.

Only ACTIVE contracts receive the city-card upper-right “正在投资” marker and sort first. Pending/HELD/completed/terminated receipts retain their existing inspectable state rather than being described as active. Stable city identity preserves selection across reordering; detached UI groups do not modify published contracts. Monetary rounding remains display-only. City/district scrollbars now auto-hide when unnecessary.

## Local validation

LOCAL_SIMULATION_PASS:40 scoped methods covering matching badge cell/control sizes, package closure, Lua syntax, unchanged32/64px hashes, canonical state/lifetime, Potential-only commit publication, active-first ordering, completed/held distinctions, selection identity, no duplicate confirmation, no extra request on resize, narrow navigation, header/footer/card geometry and display/transaction separation. Five screen sizes are checked by UI fixtures, not by the native renderer.

Historical B252/B253 equal-third/per-card-scroll assertions are superseded by this explicit layout change; historical package version pins are not rewritten. An exploratory B246 definitions run lacked the explicit external DB configuration; those gameplay DB checks are outside this UI-only delta and are not claimed PASS. The final40-method run uses canonical repository fixtures (a temporary-runner import collision was corrected before that run).

## Minimal native check

1. Inspect a city banner: main badge visible again; four-segment bottom remains aligned. No repeat investment/save-load required for already accepted B257 behavior.
2. Open “发展投资”. Existing active targets should appear first with “正在投资” at upper right. Choose a city, then a district. Verify lowered second/third columns, left-aligned titles, building/name row, readable paragraphs and unclipped footer buttons. No new payment is needed for visual acceptance.
3. Scroll only if details overflow; ordinary city/district lists should not display an unnecessary scrollbar. Report any native sizing/clipping discrepancy; local simulation is not native rendering acceptance.

## Publication and deployment

B258.285/modinfo285 locally verified; live remains B257 pending normal guarded deployment. Main/stable B069.96, institution softness, held gameplay and audits remain unchanged.
