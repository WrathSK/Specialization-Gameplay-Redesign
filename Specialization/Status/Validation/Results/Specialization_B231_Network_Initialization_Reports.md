# B231 — Cityless-player initialization and independent network reports

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source/live B231.258; verified deployment is recorded below.

## Approved boundary and B230 evidence

The user approved three narrow fixes: guard initialization city collections, restore shared read-only network diagnostics independently of the Culture consumer, and retain concrete failure stage plus sanitized error evidence. Expedition task/activity/capacity/source/rewards, permanent state, Design, Research calculation, GC, configuration and main remain unchanged. No timer, polling, forced wake or repeated command is added.

B230 native session `local/diagnostics/B205/session-20261018T015458Z-ce5807/` remains ignored and unmodified:

| Original | SHA256 |
|---|---|
| records.log | c156778555a57f646847f2043833c486f82356bb4cdcd1f5b1c75c8ba24ed6f6 |
| events.jsonl | 60f490c879e3116f1405a4c91ecbb25edd0bd0c691fa0f2f54ee6f61bb9ca616 |
| summary.txt | 2d4e0b25815b18842189f943d21e32164bf4bf5a539f242ebb5f731ac86a67c5 |

The collector retained46 unique records across7 contexts, ending INTERRUPTED. T79 NETWORK_HEALTH reports Culture ready=false/READ_ERROR while Bridge is ready with VERIFIED/AVAILABLE input1→1. Explicit reports replace that error with CN_NOT_READY. Later input2→2 is NEEDS_REVALIDATION, a separate state. This is a Culture initialization failure despite an already constructed shared topology, not evidence that the shared network never built anything. B230's two visible report actions incorrectly routed exclusively to the failed consumer.

STATIC_CONFIRMED / LOCAL_SIMULATION_PASS: B230 CultureNetwork initialization unconditionally calls `player:GetCities():Members()`. With one cityless player slot, the actual B230 Lua fails at CultureNetwork.lua:235, ready=false and receiver coefficient0. B231 with the same input initializes and projects coefficient1. This confirms a code defect and a compatible explanation for the native symptom; B230 masked the original native exception, so the exact native stack is not retrospectively established.

The same session captures two completed missions with wake/release to ARRIVED. A later idle read again shows SLEEP/SKIP denied despite AWAKE; that unresolved Expedition behavior is retained, not repaired or expanded into this batch's test gate. Prior Insight records are unchanged.

## Changes and ownership

- Culture initialization checks the city collection before iterating. A legitimate nil collection is skipped; exceptions and unknown carrier presence still fail visibly. Actual cities under unsupported owners still receive exact owned-carrier cleanup. Existing once-per-context and event-driven retry behavior is preserved; repeated load notifications do not erase rebuilt effects.
- Initialization retains definition-validation, city-collection, carrier-cleanup or player-reconciliation phase. Reports/logs retain a known contract code or Lua error class, allowlisted source filename and numeric line. Full paths, arbitrary messages and names are not included. A concrete initialization failure takes precedence over generic CN_NOT_READY.
- NetworkBridge.ReadSnapshot inspects the already published private topology without Refresh, Verified, Input, fact collection, publication or carrier writes. It reports known/missing/stale input distinctly; source cities, centers, selected-city receivers and related route directions are visible. Details paginate five rows per click. The original shared compute/publication/validation/event paths remain byte-identical to B230.
- NetworkBridge.Report independently protects public and Culture report reads. A missing/throwing Culture consumer cannot hide public topology. Gameplay routes the existing NETWORK_READ/NETWORK_DETAIL actions here; buttons retain their Chinese names **网络概况** and **网络来源 / 接收**. Current Culture coefficient, matching workers and expected yield remain a separate observation, not a claim of independently measured native yield.
- Existing bounded trace receives NETWORK_PUBLIC and page-level NETWORK_LINK observations; failure metadata is added to NETWORK_HEALTH/NETWORK_WAIT/NETWORK_REPORT_ERROR. The existing64-row ring and96-record producer budget stay unchanged. No public report work is added to ordinary computation; names are UI-only. Collector parser/logic is unchanged, and late-reader retrieval is covered.

## Local validation

143 targeted tests PASS:22 new B231 cases plus121 existing scoped tests. They cover nil/empty collections, foreign exact cleanup, thrown getters vs legitimate nil, carrier/definition errors, safe phase/location reporting, subsequent-event recovery, idempotence, consumer missing/throwing/failed-init isolation, published/missing/stale topology, pagination, no native/fact/Property writes, intact Gameplay request routing, late collector retrieval and bounded output. Existing Culture projection, UNKNOWN/exit/return, release diagnostics, P0 callbacks and collector tests remain included.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<LOCAL_LUPA>:DevelopmentTests python3 -m unittest test_b231_network_initialization_reports test_b230_culture_network_ready test_culture_network.Projection test_b229_retained_diagnostics test_b228_native_network_diagnostics test_p0_panel_current_layout test_expedition_trace_reader test_expedition_trace_collector`. `<LOCAL_LUPA>` denotes the existing local test dependency directory, not a directly runnable literal path.

The optional historical `test_arch_v2_batch_b.py` wrapper cannot complete its inherited B069 fixture: a missing indexed player/bucket fails at the first background-route assertion. Re-running that wrapper against the B230 versions of all changed imported runtime files gives the same error. It is not counted as PASS and its fixture/assertions remain unchanged. The current actual-Lua shared-topology fixture and scoped projection regressions pass. No gameplay-wide regression, native yield/rendering claim, or new save/load acceptance is made.

Context/schema/selectors, changed-path links, Lua parsing, XML metadata, publication gate and final diff are checked at the commit checkpoint. Only reviewed changed hashes are refreshed. Existing frozen results and raw evidence remain unchanged.

## One minimal native flow

Use the existing campaign and manual collector; no new team, mission, cold-load loop or forced refresh is required.

1. Load normally with the collector running. Select a known recipient city and click **网络概况**. It should show route count, source/center roles and per-network reception, followed by Culture state rather than only a generic wait. This checks ordinary-event initialization independently of opening the report.
2. Click **网络来源 / 接收**; click again if there are multiple pages. Check a recognizable source→center→recipient route and city names. This checks the restored public report and direction. The same scalar relationships are collected automatically; screenshots are only needed for a visual discrepancy.
3. For an existing connected ACTIVE IV Culture source with a full three-category foreign-civilization set, verify the recipient report's matching-specialist coefficient and ordinary native specialist Culture. For one distinct eligible civilization and W matching working specialists, the extra Culture is W. If no eligible set exists, only readiness/report coverage is accepted; do not manufacture a long new mission sequence. If initialization or input still fails, retain the log and stop that path: the report now distinguishes phase/error and shared-input state.

User decision: none. User testing: the network delta above only. Primary next: review B231 collected evidence; Expedition remains pending without a new speculative repair.

## Deployment

B231.258/modinfo258 DEVELOP_ACTIVE; source 168bb25df3eaf21d9c411538f1c9bcfc209571a6; receipt B231.258-168bb25-playtest.json;226/226 MATCH, digest 75e7b7f56789874f42bfa1f27f29628c754625dbf5cfc76a52a8367580be7681. Automatic game-exit checks before both guarded switches; B230/stable recovery retained, no pending transaction. Stable main remains B069.96; no game launch or configuration change. Native gate remains pending.
