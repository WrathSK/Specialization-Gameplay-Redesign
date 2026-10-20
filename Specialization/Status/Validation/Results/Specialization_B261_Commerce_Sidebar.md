# B261 — Commercialization sidebar and Escape routing

## Scope and evidence

User accepts B260 and approves the two-column Commercialization plan, additionally requiring Escape to close Commercialization and Development Investment before the game menu. Presentation only: retain D0057 selection history, eligibility, specialist capacity, source computation, per-domain Floor, saved state and existing native request/ack guards. No new timers, gameplay edits, image assets, external configuration or main changes.

## Implementation

Replace the centered five-row dialog with two equal-width native-style sidebars. Reuse accepted Development Investment header, source-city banner, native scrollbars,55x55 district icon backing, measured cards and90-unit action drawer. Window height is screen height minus27 top inset; secondary top148 matches the accepted wide layout; its bottom reaches the same viewport edge. At narrow widths, show one column with Back. Only explicit resize events relayout; no frame callback.

Selected domains appear first in persisted activation order; unselected domains follow the existing fixed domain order. Selection identity survives reordering. Rendering never writes that order. Most recently enabled eligible domains still suspend first under capacity reduction; reopening remains the newest activation. Effective domains show “正在商业化”; selected suspended domains show “已开启·暂停”. The domain card's state remains available even when configuration is disabled.

Selecting a domain only opens four content-height cards: Commercialization Value, Value Source, Operating Conditions, Current Status. Value distinguishes raw/per-domain floored Gold and city total base Gold from native percentage-adjusted income. Current backend only samples effective domains; inactive rows show explicit unavailable-until-effective text, never fabricated0 or stale source/value previews. Reputation and exact model values remain unchanged. State/errors/waiting/cleanup warnings belong in the status card. The sole toggle reads “进行商业化” or “停止商业化”, including stop for suspended selected domains. Pending requests disable repeats and preserve existing scalar reference/revision/token checks.

Native Base/Assets/UI/AnimSidePanelSupport.lua OnInputHandler receives an input object and reads GetMessageType()/GetKey(). Both prior panels instead compared their first argument directly with KeyUp, despite SetInputHandler(...,true). B261 normalizes object/userdata input and retains legacy argument compatibility. While open it consumes Escape, closes on KeyUp, and consumes KeyDown without closing so the matching release remains owned. Hidden panels return false. No popup queue or game-menu override is introduced; native input priority still requires user validation.

## Validation

LOCAL_SIMULATION_PASS:19 selected methods covering actual Commerce Lua rendering/toggle callbacks, no initial auto-selection or render-time writes, scalar operation identity/revision, double-click guard, stored order and stop/reopen placement, suspended labels, real values/no false previews, errors and cleanup warnings, invalid city/held state/shutdown, five viewport sizes, card flow/footer clearance, native/legacy Escape down/up on both panels and pass-through when closed. Retained production entry behavior, Development confirmation guards, B260 presentation and package/SQL/Lua checks pass. An initial broader legacy Action suite failed because its old adapter fixture lacks SPCDevelopmentInvestmentUI; unchanged production adapter was not weakened, and the final selection excludes that stale fixture. No full-suite or native-rendering PASS claim.

## Minimal native test

1. Open “商业化”, select one domain: no toggle occurs by selection alone. Check two equal columns, aligned top/content and viewport bottoms, native scrollbar and four cards.
2. Enable two eligible domains in order. Confirm markers/value/source; stop and reopen the first, which moves after the other. Existing effective choices can be used instead; no new specialist experiments are required.
3. Press Escape: close only this panel. Reopen Development Investment and press Escape: close only that panel. With both closed, Escape should retain normal game-menu behavior.

## Deployment

B261.288/modinfo288 locally validated; live B260 pending guarded deployment. B260 acceptance is recorded from the user's explicit confirmation; no other native acceptance expanded.
