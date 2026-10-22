# B091.118 — watched Free City transfer chain

USER_GAME_TEST_PASS scoped to UI event observation in this supplied sequence. T8, experiment DEV-B013-P0-2. Before22:52:04 current0/131073; UI events0. After22:52:19 current62/65536; UI captures, in displayed order:

- CulturalIdentityCityConverted(62,65536,0,24576)
- CityTransfered(62,65536,0,-738490196)

OriginalOwner remains0; OwnerBeforeOccupation0→62; JustConqueredFrom remains-1; LastTransferType1634873444→-738490196. Fourth arguments and transfer enum names UNKNOWN. No inference that CityTransfered third parameter is always previous-owner merely because its value matches in this scene.

Native Expansion2/UI/Loaders/TutorialLoader_Expansion1.lua:96–120 subscribes CulturalIdentityCityConverted(player,cityID,fromPlayer), resolves new city via CityManager.GetCity(player,cityID), and uses fromPlayer as previous owner in lost/won-loyalty logic. Combined static and supplied runtime evidence supports new-owner/new-city/from-owner=62/65536/0 for this Cheat Free City path. Installed Cheat Panel MakeFreeCity calls CityManager.TransferCityToFreeCities; no special Specialization action created the transition.

This closes the missing BEFORE-watch evidence from the previous B091 pair. No new save/load proof is claimed here; B090 remains the independent experiment persistence evidence. UI screenshot does not prove the same callback has fired in Gameplay. Existing Gameplay module registers it but resolver ignores it and still requires previous-owner getters; its HELD result therefore reflects that restrictive implementation, not absence of all usable transfer evidence.

No native test of recapture/repeated conquest/gift/liberation/raze-refound provided. No professional ledger restoration or permanent identity certification. Raw images hash-archived; runtime/main/deployment unchanged.
