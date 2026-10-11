# B199 — explicit selection, mission preview and location strip

Source checkpoint: **B199.226 / modinfo226**. User-authorized refinements after the [B198 native review](Specialization_B198_Expedition_UI_Native_Review.md). **LOCAL_SIMULATION_PASS; rendered UI and foreign location visibility USER_GAME_TEST_REQUIRED.** [Status](../../Specialization_P0_Status.md#current-authoritative-state) and receipt determine actual deployment.

## Changes and boundaries

- Each normal relocation/task open starts with no city/task choice. Confirmation stays disabled until an explicit click; guarded request callbacks also reject an absent choice. Reopening resets selection. Diagnostic previous/next behavior is retained.
- City rows have no gold selector outline. Their selected-city banner carries the choice. The adjacent drawer shows the existing **无奖励验证任务**, two turns, as a read-only preview; travel time remains in the city/banner information. No automatic task starts on dispatch or arrival.
- Normal TASK closes only after a matching accepted owner/unit/token/activity lease in preparing/running state. It tolerates the native selection clearing after Start. Rejected, mismatched and already-HELD replies do not close the panel. A matching startup failure stays visible even if the engine clears selection; unrelated-unit errors are not attributed to this team. Pending acknowledgements retain existing close/Cancel protection. The independent activity bridge/timer continues after the presentation closes.
- Location strip: city center; a completed district containing a positively identified shared-catalog eligible Great Work; every completed Wonder, with its own `ICON_BUILDING_*`. Actual plot/building placement determines the host, not a Theater/prerequisite guess. Duplicate buildings/works at one location produce one icon; a work-bearing Wonder remains one Wonder icon. Missing size-32 atlas falls back to the existing generic Wonder icon while retaining its name.
- Unknown location reads retain known icons and display **地点信息未完整确认**, with a concise tooltip. Unknown rows allow room for that line. No raw reader IDs, work names, eras or full inventories are published. `READABLE` means the returned API snapshot was readable, not independently proven foreign completeness. These icons are preview facts, not new dispatch or mission permission.

Source changes are restricted to Window Lua/XML, the optional read-only presentation helper, bilingual text and package identity. Gate, capacity, native-name/source binding, travel adapter, activity implementation, task clock, one-shot/no-reward behavior, save schema, GC and ordinary Spy/HD behavior remain unchanged. Formal training/reattachment/persistence, repeat missions, N2/N3/U2 and rewards remain held.

The location reader follows native `CitySupport.lua` district→plot→`GetBuildingsAtLocation` and Wonder presentation, and `GreatWorksOverview.lua` slot/type reads; shared `GreatWorkCatalog.Resolve` classifies only occupied observed slots. It does not start GreatWorkFacts, scan the full building database/world, subscribe to events or write Properties. Presentation snapshots stay owned by one explicit open (TASK after its READ reply). Rendering/paging/resize use that snapshot; close discards it and retires callbacks. Native source examples are local-owner readers: foreign read completeness is not yet established. No global cache or additional hot-path polling was added.

Six new bilingual keys under `LOC_SPC_EXPEDITION_SPY_`: `NORMAL_SELECT_CITY`, `NORMAL_SELECT_TASK`, `NORMAL_MISSION_PREVIEW`, `NORMAL_MISSION_PREVIEW_DETAILS`, `NORMAL_LOCATIONS_INCOMPLETE`, `NORMAL_LOCATIONS_INCOMPLETE_TT`. Existing names and gameplay localization are unchanged. XML separates mission content from its selector overlay so an unselected card remains visible.

## Local evidence

**189 focused tests PASS** using actual current Lua and the configured read-only gameplay database: the preceding160 relevant cases,19 explicit-selection/ACK/display cases and10 location-reader tests. Suites cover relocation/sidebar/actions, Gate/task/activity/report/name-pool, and the new selection/location files. The initial186-case run passed; after a narrow failure-message priority correction, the19-case affected selection suite passed, including three added counterexamples (189 distinct tests overall). Tests retain exact native permission, wrong owner/source/name/target, stale row, one-shot request and ordinary-Spy isolation checks; old all-district expectations change only for the requested location semantics.

New coverage includes initial/reopened no-choice states; request guarding; read-only task preview; no city brace; synchronous/delayed accepted TASK close despite selection loss; mismatched token/unit/lease, rejection and immediate HELD remaining visible; independent two-turn completion after close; stale callbacks; visible incomplete data and no extra facts reads while rendering; each Wonder's atlas and missing/empty/error fallback. Reader cases cover actual host placement, deduplication, unfinished/absent Wonders, unsupported works, missing API/metadata, changed/hidden target, no writes, bounded scans and preview failure not blocking the separate travel preflight.

XML/SQL/custom bilingual keys, Python/Lua loading, scoped diff, links/selectors and context/integrity checks are part of this checkpoint. No broad gameplay/stress or shared save/load campaign. Local checks cannot prove native visual fit, foreign work disclosure or universal lifecycle behavior. Inherited B189/B194/B196 evidence remains limited to unchanged covered paths.

## One minimal native flow

One continuous session on verified B199. If the previous one-shot team is already finished/held, use P0 **人文考察·验证 → 结束并移除验证团**, then the usual source and **① 创建Spy验证团**. No save/reload ritual.

1. Select the team and open **派遣到新城市**: nothing is chosen and confirmation is disabled. Click a destination: the top banner updates without a gold city frame; the right drawer shows **任务预览**, with travel time left in the banner/list. Check available location icons/tooltips (city center, known work host, individual Wonder), or the concise incomplete-data notice. This tests the changed input and foreign/native presentation only. **确认派遣**.
2. After arrival, open **任务**: no task selected and Start disabled. Click **无奖励验证任务**, then **开始任务**: the sidebar closes after acceptance and task-time actions stay hidden. Continue the existing two turns to ensure closing the presentation did not interrupt the task. A failed request should remain visible with its reason. Finish using the existing P0 END.

One useful screenshot of the new strip/task selection or any error is enough. Do not create extra world content solely to force every icon type; unavailable coverage remains untested. No ordinary-Spy recruitment, save/load, capacity or name-pool retest is added because those implementations did not change.

User decision: none. User testing: the delta flow above. Codex next: review the results; no automatic formal mission implementation.
