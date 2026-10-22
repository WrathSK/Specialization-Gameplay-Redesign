# Mod isolation baseline and initial listener triage

Document Owner: Codex
User clarification: original save set includes Switch Civilization; user will disable groups and test new games.

User subsequently reviewed the enumerated third-party list (original112-entry numbering, official DLC omitted) and replied “这些都存在”. In the context of the requested original-save enabled-set confirmation, record all listed third-party entries as user-confirmed baseline members, including Switch Civilization and Specialization. No exclusions were supplied. This is user configuration evidence, not runtime proof every script executes or compatibility PASS. Barbarian Clans and Tech/Civic Shuffle actual in-game activation remain separately unconfirmed. Later test configurations must record their own removed entries and must not overwrite this baseline.

Use frozen112 UUID/name list at external W/Specialization/Status/Validation/Evidence/ExternalMonitor-20260914-201233/Current-enabled-config.tsv as the user-confirmed original set. Do not substitute later111 or94 sets. Current latest native log20:41:27 last block2737071.864 has94 entries without Switch; selected database group 原版 includes Switch with Disabled0. These describe different selection/configuration stages and cannot establish immediate refresh semantics. Preserve original baseline independently of subsequent user toggles.

Initial static search covered local absolute-path manifests in the112 list and their Lua files, not arbitrary installed mods. Literal event matches include unselected/imported variants and comments: they are leads, not execution or leak evidence. No external source edited.

Switch Civilization manifest has BOTH Gameplay and UI components despite description saying UI-only. Gameplay PlayerTurnActivated returns immediately when pendingTargetID<0; otherwise it attempts the pending switch on target turn. UI registers LocalPlayerChanged, LocalPlayerTurnBegin and LoadGameViewStateDone. No SetUpdate/SystemUpdateUI/GameCoreEventPublishComplete loop found in its inspected Lua. This does not prove compatibility or eliminate indirect interactions after a switch.

Better World Tracker Unit List subscribes GameCoreEventPublishComplete to OnDirtyCheck, with removal code. Map Search Extension subscribes playback and uses SetUpdate for IncrementalSearch; not evidence it searches continuously while closed. Science/Civic Overflow Bug Fix SystemUpdateUI handler inspected only checks ScreenResize with TODO, so event-name count alone would falsely prioritize it. Other switchable Overflow fix handles CityProductionChanged and calls ExposedMembers.OFBF.AddZeroProduction. Need execution/guard investigation before calling either a conflict.

Specialization's unfiltered Discount Audit and pre-cache full fact reads remain strongest observed repeated-work leads (prior counters), not proven retained-allocation causes. Paired footprint points to MALLOC_TINY growth, not a mod name. Next investigation should follow active callbacks and guards, not merely popular-mod reputation or co-presence.

New-game group-disable tests are broad screening, NOT strict comparisons to a developed save: city/unit/network/GW counts and acquired modifiers also change. Use a full-set new-game control of similar map/settings and idle window when interpreting results. A negative fresh-game result cannot clear modules only exercised by mature cities. Retain runtime Modding.log after each test load (before next launch overwrites it), monitor session, group removed and approximate game scale. No requirement to stop user's original long-play save, modify it, or expose account secrets.

No source/deployment/config changes or process attachment; current monitor/tool and main unchanged.
