# B263 — Roosevelt (Bull Moose) neutral test shell

## Scope and evidence

The user accepted B262 and explicitly authorized replacing the selectable Scotland test shell with an independent America / Roosevelt (Bull Moose, 罗斯福（进步党）) shell. Preserve the older shell without exposing it for new-game selection. Keep specialization access, remove all native America/Roosevelt unique gameplay, use Chinese presentation, complete local checks and the existing guarded develop deployment, then wait for the user's test. **No PR or main promotion is authorized.** B262 acceptance is the user's stated UI acceptance; it does not expand any older gameplay PASS.

This is a presentation/identity-entry batch. D0057 and A0177 profession rules, capacities, source binding, transaction protections, saved histories, GC, held audit issues and held Expedition repair remain unchanged. There is no save migration, new timer or frame mechanism. Existing Scotland test saves retain their original IDs and access; they are not converted to America. The new shell is tested in a new game.

## Implementation

- [New selection](../../../../Mod/Config/TestAmerica.sql): separate `CIVILIZATION_SPC_AMERICA` + `LEADER_SPC_T_ROOSEVELT`, Gathering Storm domain, native Bull Moose portrait/background and explicit Chinese selection/ability text. No unique-unit/building selection items. The complete older [registration](../../../../Mod/Config/Players.sql) remains commented for deliberate reactivation; its gameplay definitions, art references and name pool remain present.
- [Gameplay identity](../../../../Mod/Data/TestAmerica.sql) uses an explicit presentation-table allow-list. It copies America city/citizen and six GS geographic naming pools, capital, ethnicity, leader presentation metadata, biography metadata, quotes, loading illustration/intro/audio and diplomacy background. The only attached civilization trait is the existing specialization access trait. No American civilization traits, Roosevelt leader traits, agenda or start bias is copied. Gameplay inheritance remains `LEADER_DEFAULT`; inheriting the native Roosevelt gameplay identity would reintroduce powers.
- Named native icon aliases and the complete original Roosevelt color row (including alternate jerseys) provide America/Bull Moose presentation. [Text](../../../../Mod/Text/TestAmerica.sql) adds Chinese UI copy in both supported display languages and aliases existing Chinese historical biography, without cloning native strategy descriptions that promise the removed powers.
- Explicit `Leaders`, `FallbackLeaders`, `Civilizations` and append-only `Cultures` ArtDefs map the new IDs to native Roosevelt model, fallback portrait, music and American/European city/unit appearance. The package registers the appropriate art consumers and Teddy persona dependency. These are text references to installed assets; no proprietary binary art/audio is bundled. Ordinary America, Teddy, Rough Rider and Scotland definitions remain untouched.
- [Public eligibility](../../../../Mod/Probe.lua) now accepts only the two exact new/legacy identity pairs, preserving the existing human-only single-player checks. [Expedition name recognition](../../../../Mod/ExpeditionSpyGate.lua) accepts the new civilization's copied native citizen pool while retaining the old pool. Training costs, slots, reservations, source-city binding, task behavior and rewards are unchanged. Diagnostic identity text reports the actual selected pair.

## Source basis

Read-only sources, not new native acceptance:

- `CIV6_ASSETS`: installed macOS Civilization VI 1.4.6, build 376653.178. `DLC/TeddyRoosevelt/Data/TeddyRoosevelt_Leaders.xml` and `TeddyRoosevelt_ConfigData.xml` identify Bull Moose as `LEADER_T_ROOSEVELT`; Rough Rider uses a separate ID. The persona pack is a declared dependency.
- `CIV6_ASSETS/Base/ArtDefs/Leaders.artdef`: the default leader maps to Cleopatra (`ART_LEADER_CLEO`), whereas Roosevelt maps to `ART_LEADER_THEO` and its native lighting/BLP entry. This explains the existing neutral-inheritance art fallback risk; explicit art aliases address it without gameplay inheritance. Native rendering is still to be verified.
- `CIV6_ASSETS/Base/ArtDefs/FallbackLeaders.artdef`, `Civilizations.artdef`, `Cultures.artdef`, and `Base/Assets/UI/Colors/PlayerColors.xml`: exact native reference subtrees and palette. Culture lists append the new civilization instead of replacing existing lists.
- `CIV6_ASSETS/Base/Assets/Gameplay/Data/Civilizations.xml`, `DLC/Expansion2/Data/Expansion2_NamedPlaces.xml` and `Expansion2_Schema.sql`: city/citizen/geographic data and table contracts. `Base/Assets/UI/FrontEnd/LoadScreen.lua` supplies the loading/intro fields; Civilopedia's leader page recursively reads inherited traits, so a neutral gameplay parent is retained.
- `HD_SOURCE`: installed Harmony in Diversity, Workshop 2465378070, `DL.modinfo` version 2.2. `UpdateDataBase/DL_Civilizations.sql`, `DLCSupport/DL_Vietnam.sql`, and `UI/Replacement/America_UI.lua` were followed for the America/Teddy abilities: the relevant modifiers are trait-bound, and the American UI entry is property-gated by `AmericaProperty`. The independent shell does not acquire those traits/property. This scoped review is not a claim about every future external Mod.

Source-root labels are locators, not public URLs. External game/HD files were read-only. Native cache schemas were copied into memory for verification; that older base cache is not represented as a current loaded HD/GS database.

## Validation

LOCAL_SIMULATION_PASS:

- Fourteen targeted unittest methods: ten new [identity regressions](../../../../DevelopmentTests/test_b263_test_civilization.py), three existing training reservation/event/idempotence regressions, and existing package/syntax closure. Exact pair selection, AI/multiplayer/unknown rejection, neutral traits/inheritance, unchanged original/legacy data, Chinese biography versus removed-power descriptions, independent icon aliases and model/fallback registration are covered. Actual Training/Store/Gate Lua confirms both shells retain source-city binding and name confirmation with no second reservation or duplicate name write.
- Existing `test_b099_eligibility.py` passed the actual public eligibility and Gameplay rejection-to-UI path. The new standalone fixture initially lacked the shared Lua include loader; that test setup was repaired to load the real dependency before the successful run. No runtime assertion was relaxed.
- Read-only external verification: cached native schemas plus installed GS named-place rows, all copied into memory. Complete identity SQL succeeded with zero new foreign-key violations. America copied 40 cities, 40 citizen names, 12 rivers, 7 volcanoes, 9 mountains, 5 deserts, 13 lakes and 10 seas. Ten Roosevelt and sixteen America Chinese history entries were available and aliased. Native trait/modifier/unit/building/start-bias/agenda rows and legacy identity rows were unchanged. New leader/model/fallback/music references and every palette field matched their native source subtrees after changing only the public identity.
- Package contains 288 runtime files. XML parsing, Lua syntax, file registration, staged publication and context checks are separate from native rendering. No binary publication exception is needed.

USER_GAME_TEST_REQUIRED: selection presence/absence, original loading presentation, in-game leader scene and actual new-shell specialization access. Actual native citizen-name assignment can be observed when an Expedition is naturally trained; held task/arrival problems are not reopened here. No new native save compatibility, audio or rendering PASS is claimed.

## Minimal native test

1. Start a new Gathering Storm game using **美国（专业测试）／罗斯福（进步党·专业测试）**. The old Scotland test entry should be absent. Inspect the portrait, loading illustration, Chinese introduction and city names. Original America/Roosevelt remains a separate normal choice.
2. After founding the first city, click the leader portrait: it should show Roosevelt rather than Cleopatra. The new civilization should have no America/Roosevelt unique ability, unit or building; establishing a supported district should expose the existing specialization institution/access normally. Cheat Panel may be used for this access check.
3. During subsequent normal play, check the first Expedition's native American name and ordinary source confirmation when available. This is an observation of the newly selected name pool, not a repeat of held Expedition lifecycle tests. No cold-load ritual or old-save conversion is required by this shell batch.

## Deployment

B263.290/modinfo290 locally complete. Live remains B262.289 until the clean-source/game-exit/receipt deployment gates pass. Stop for user feedback after deployment. No PR.
