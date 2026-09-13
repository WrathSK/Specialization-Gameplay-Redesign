-- Read-only native-API candidate, NOT registered in modinfo. No engine writes/events.
-- env is injected for tests; actual Gameplay context/return behavior still needs user proof.
local M={}
function M.New(env,trait)
 assert(type(trait)=="string" and #trait>0,"EXPLICIT_CARRIER_REQUIRED")
 local C={}
 function C.Read(player)
  local out={contextSource="GAMEPLAY_CANDIDATE",player=player,status="UNKNOWN",carrier=trait}
  local ok,reason=pcall(function()
   assert(type(player)=="number" and player>=0 and player<math.huge and player%1==0,"INVALID_PLAYER")
   assert(env.Players and env.Players[player],"PLAYER_NOT_READY")
   local config=env.PlayerConfigurations and env.PlayerConfigurations[player]
   assert(config,"CONFIG_NOT_READY")
   local civ=config:GetCivilizationTypeName()
   assert(type(civ)=="string" and #civ>0,"CIV_NOT_READY")
   assert(env.GameInfo and env.GameInfo.Traits and env.GameInfo.Traits[trait],"CARRIER_NOT_DEFINED")
   local found=false
   -- No early success: an interrupted database iteration must not appear complete.
   for row in env.GameInfo.CivilizationTraits() do
    assert(type(row.CivilizationType)=="string" and type(row.TraitType)=="string","BAD_TRAIT_ROW")
    if row.CivilizationType==civ and row.TraitType==trait then found=true end
   end
   out.status=found and "ENABLED" or "DISABLED"
   out.civilization=civ
  end)
  if not ok then out.status="UNKNOWN";out.reason=tostring(reason) end
  return out
 end
 return C
end
return M
