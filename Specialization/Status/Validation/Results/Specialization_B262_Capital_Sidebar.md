# B262 — Capital Investment sidebar and Commerce footer

## Scope and evidence

User approves the planned Capital Investment three-column presentation and requests Commercialization's single-button footer match the outer vertical margins of the earlier two-button drawer. Reviewed original B261 screenshot archived with verified before/after hash in ignored local evidence. It shows the Commercialization layout and oversized drawer; do not infer complete toggle or Escape acceptance. B260 prior acceptance remains unchanged.

## Implementation

Capital Investment now uses domain → investment mode → details. Domain cards reuse the Commerce district card; fixed Research/Culture/Industry order, not Commercialization activation order. Unsettled active contracts show “正在投资”; pending/held transactions show “合同待核对”. Two mode cards display Stable/Venture and concise existing quote outcomes. No initial domain/mode auto-selection. Domain selection retains the existing explicit CAPITAL_REFRESH quote path; mode selection only renders. Refresh keeps selection by identity; changing domain clears mode. Confirm alone sends the selected mode with existing token/revision/CityToken guards; pending and unavailable states also block the callback directly.

Four content-measured cards: Quote and Principal, Returns and Risk, Quote Basis, Current Contract. Preserve10-turn terms, original source/fundamentals and help text; show mode-specific quote returns/probability/expectation and existing downside warnings. Current contract is independent from selected preview mode, with its own locked terms/mode, actual debit, maturity and actual credited result. Monetary display lines are separate. Missing actual debit remains unknown rather than assumed principal. Existing pause-stage diagnostics and request/quote errors appear in this card, never in button labels.

Reused Development Investment geometry: three295-wide columns, top inset27, wide secondary/tertiary top148 and matching viewport bottoms; native left domain/mode scrollbars, content scroll in details,90-high two-action footer with41/24 controls and centered labels. Narrow widths use existing one-column/back-bar approach. Native input object and legacy Escape handling matches B261; consume while open, close on release, pass through while closed. ScreenResize is the only sizing event; no timers or frames.

Commercialization wide footer changes90→66 by removing the absent24-unit secondary action; the centered confirm retains native41-unit height and prior offsets. Narrow mode still shows Back and retains90. Detail viewport grows with the released24 units. This is presentation calibration pending native visual review.

No gameplay formula/source changes, persistent state, contract lifecycle,0.01 tolerance or debit/credit protections changed. No new art, main, game configuration or held-item work.

## Validation

LOCAL_SIMULATION_PASS:20 targeted methods, including actual Lua callbacks for no auto-selection/signing during browsing; both modes' scalar requests and repeat guard; synchronous acknowledgement; fixed ordering/selection refresh; separate locked contract/current quote; held/error stage; settled Venture outcome and actual credit; five viewport sizes and narrow navigation; Escape; invalid/held Commerce state and retained B261 tests;66/90 Commerce footer selection; XML named-control links, package closure, SQL and Lua syntax. Native appearance/input routing remains USER_GAME_TEST_REQUIRED. No full-suite or new financial-engine acceptance claim.

## Minimal native test

1. Open “商业化”: inspect single-button upper/lower margins; no need to toggle existing choices.
2. Open “资本投资”: choose a domain, switch between “稳健投资” and “风险投资”; inspect equal-width aligned columns and all four cards. Selection alone must not sign. Inspect an existing contract if available; selected preview mode must not overwrite its locked mode/terms.
3. Click “刷新报价”, verify selection stays. Press Escape: closes panel without opening game menu. No fresh contract or10-turn settlement required for this UI-only batch; native financial acceptance from B245 remains scoped to its original evidence.

## Deployment

B262.289/modinfo289 locally complete; live B261 pending guarded deployment. Stop after minimal UI feedback.
