# E2 city lifecycle — other Mod source investigation

Read-only source investigation, 2026-09-25. Baseline B105.132, D0035/A0161; no runtime/Design/deployment change. Evidence is STATIC_CONFIRMED (source use), not USER_GAME_TEST_PASS for the referenced approach. B105's native Publish interleaving remains authoritative for our tested environment.

## Main conclusion

Do not search for one universal end-of-all-city-events signal as a prerequisite for every path. Positive, operation-specific evidence is a better candidate: transfer completion for ownership changes; a dedicated founding reason for self-founding. Other Mods show correlated events, effect-specific caches and pending-operation reconciliation, not a universally proven identity service. Coordinates can correlate evidence; they alone cannot establish persistent identity after destruction/rebuild.

## Compared implementations

### 1. Gedemon GCO: correlate removal and addition/initialization

[Author source, GCO_ModUtils.lua lines1176–1235](https://github.com/Gedemon/Civ6-GCO/blob/master/Scripts/GCO_ModUtils.lua#L1176-L1235).

Caches district-removal owner/CityID/turn by coordinates. Addition and initialization at that location in the same turn consult the cache, query the city, compare GetOriginalOwner to the cached owner, then attempt captured-city notifications. No Publish/Playback completion requirement in this block. Added has a duplicate flag; initialization clears the matched entry.

Useful: retain old reference before destruction of the engine object, correlate multiple positive events. Limitations visible in source: district type is not filtered in this callback; original owner is not necessarily immediately previous owner after repeated conquest; same-turn location matching alone cannot exclude raze/rebuild. The initialized dispatch is literally `GameEvents.CapturedCityInitialized.Add(...)`, not a normal Call, so this block is not a drop-in verified solution. The clearing shown is success-path, not a general bounded-cache policy. Borrow the correlation principle, not its entire implementation.

### 2. Gedemon AutoPlay: dedicated founding reason

[Author source, AutoPlay_InGame.lua lines582–599](https://github.com/Gedemon/Civ6-AutoPlay/blob/master/AutoPlay_InGame.lua#L582-L599).

Registers Events.UnitActivate, tests eReason against EventSubTypes.FOUND_CITY, and positions the observer camera at the reported coordinates. Later same-name notification code also checks this reason, but the earlier registered callback is the relevant concrete registration. This is an InGame/UI observer, not a persistent Gameplay identity writer.

Useful: a positive founding-specific signal rather than absence of conquest/transfer. Unknown: Gameplay availability, enum availability there, delivery relative to Built/Initialized, unit survival at callback, visibility/quick-movement/load behavior. Neither notifications nor camera use prove the stronger guarantees needed for a ledger.

Installed original Firaxis code independently uses the same path: Base/Assets/UI/Automation/Automation_ObserverCamera.lua603–621 and Automation_NarrationManager.lua179–188. Both gate presentation by visibility; do not infer that Gameplay receives the event or that our handler should inherit their camera/notification gates.

### 3. HD civilization extension: narrow conquest/removal cache

Installed Workshop2860503037/Lua/Assyria.lua29–80. Assyria caches current turn and population under the capturing player's new city ID on GameEvents.CityConquered. Its removal reward checks that player's same-turn cached city, the trait, and an absent current city object. Ashurbanipal's sibling handler uses the cache and traits without the same object-absence check.

Useful: scope interpretation using prior meaningful evidence; Removed alone does not mean razed. This code awards civilization-specific rewards, not durable identity migration. The shown cache is not consumed on reward, and missing object is not a universal destruction proof. Do not import its negative-evidence test into E2 permanent-history deletion. Source read only; no claim of tested correctness.

HD core2465378070/Gameplay/CivilizationTraits.lua2527–2550 directly responds to GameEvents.CityConquered for Nader Shah's effect. It demonstrates that a conquest-specific consumer can use typed conquest evidence without waiting for generic UI flush. It does not cover gifted cities or classify founding.

### 4. Captive Leaders: reconcile a known pending operation

Installed Workshop3795382610/CaptiveGameplay.lua2346,2557–2597,3019–3024,3158; modinfo identifies “把战败领袖收为战利品（Captive Leaders）”. It records pending liberation target IDs, then on GameEvents.OnGameTurnStarted checks whether they remain in the local player's city collection before settlement. Author comments say CityLiberated was unreliable for their major-civilization use; this is the author's report, not our test.

Useful: reconcile only a known pending action rather than globally infer history from every missing city. Do not copy its predicate: “no longer held locally” also allows other loss/destruction outcomes and does not prove which owner received the same persistent city. Its old-save branch settles absent target lists; that fallback is inappropriate for E2's no-invented-history contract. Turn reconciliation is not per-frame polling but can still be too late for our new-city first-completion path.

## Primary community observations / version limits

- [Gedemon's 2018 author explanation](https://forums.civfanatics.com/threads/destroy-building-on-city-capture.610970/): uses district removal followed by city initialization for capture; explicitly had not tested the then-mentioned CityConquered path. Historical precedent, not current engine guarantee.
- [2017 modders' direct event observations](https://forums.civfanatics.com/threads/detecting-city-ownership-change-raze.609448/): removed/add/initialized ordering, old reference unavailable during removal, load also emitting Added; GetJustConqueredFrom proposed for conquest before Keep/Raze/Liberate. Useful caution, not proof for trade/recapture/all versions. No safe universal destruction-complete event established there.
- [Sukritact's CityBuilt documentation](https://sukritact.github.io/civilization-modding-wiki/civ-6/lua/GameCoreEvent.CityBuilt/) locates it in GameEvents and documents parameters; it does not establish founding-only semantics. Our B105 directly shows transfer also emits Built.
- Search also returned Civ VII event documentation. Excluded: VII events such as CityRazingStarted cannot be assumed to exist in VI.

Public master URLs are moving references, consulted on the date above. Installed sources are identified below by read-only hashes; none were modified. These are a targeted sample, not an exhaustive audit of Workshop or a claim that no other strategy exists.

## Recommended smallest next proposal (not implementation)

1. Preserve B103/B104 transfer/recapture authority. Explicit matching Transfer plus existing old/new-reference evidence remains stronger than early Publish. Do not rewrite that working path based on third-party examples.
2. Extend only the bounded observer, if separately authorized, to record UnitActivate reason/owner/unit/location alongside the existing trace; check Gameplay first. Record FOUND_CITY enum availability explicitly. If UI-only, capture that fact separately; a UI assertion must not automatically become durable Gameplay authority.
3. Correlate positive founding evidence with actual current local-human city owner/reference and existing initialization evidence, using bounded session tuples and deduplication. It must identify a new founding operation, not revive the prior city's ledger at that plot. Investigate ordering locally; never assume the settler still exists at the callback or treat an operation request as successful completion.
4. Only after native delivery is established can the authorized fresh-city registration plan substitute this evidence for the failed Publish boundary. Missing/conflicting evidence stays unresolved; no timeout, fixed Publish count, polling or coordinate-only inheritance.
5. Keep confirmed destruction/history retirement separate. A positive new founding can establish a new-city candidate without first inventing a generic “no successor means razed” rule. Existing-record conflict still needs explicit handling; this does not authorize cityKey redesign, legacy overwrite or removal of the two-record cap.

Minimal future native test, only after an observer proposal is authorized: one ordinary Settler founding and one transfer negative control with the new event included. No repeat full migration/investment/governor/save loop. If delivery is absent, report context boundary rather than silently switching to UI authority. No user test needed for this static investigation itself.

## Disposition

New positive founding candidate found; EVENT_BATCH_BOUNDARY is not closed by external source reading. No Design decision/change, gameplay tests, runtime edits, deployment, game launch, Claim or F. Next is scoped evidence proposal, not automatic implementation.

## Installed source provenance

- `/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2860503037/Lua/Assyria.lua`
  SHA256 `feffbaf039657172cec6e4e018dc70ce536587a8d251155023c49ac369d9860a`

- `/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070/Gameplay/CivilizationTraits.lua`
  SHA256 `ee31d203a7e64e0c8b11521ead00178c736ea03b9edf7f9f1f456b812c6e53bc`

- `/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/3795382610/CaptiveGameplay.lua`
  SHA256 `2bc219d57b15977446e0216013d8d1332705258d76c0ea993902b70d3913d696`

- `/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI/Automation/Automation_ObserverCamera.lua`
  SHA256 `7ad1468805d1544bdea5580a897824eb89b2d086100bbce0da78cf202453e96e`

- `/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets/Base/Assets/UI/Automation/Automation_NarrationManager.lua`
  SHA256 `a6dda0d13d68673908f187458fb530e05f664e8823708c1e4163a7405e2a5e1f`
