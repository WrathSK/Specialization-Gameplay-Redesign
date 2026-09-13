-- B016 read-only Gameplay diagnostics. Never a production gate or persistent fact.
SPCEligibilityProbe={}
function SPCEligibilityProbe.Start(P,shared)
 local trait="TRAIT_CIVILIZATION_SPC_TEST" -- explicit current carrier configuration only
 local data={version=P.VERSION,hooks={},samples={}}
 shared.EligibilityProbe=data
 local function read(pid)
  local r={status="UNKNOWN"}
  local ok,err=pcall(function()
   assert(Players and Players[pid],"PLAYER_NOT_READY")
   local config=PlayerConfigurations and PlayerConfigurations[pid]
   assert(config,"CONFIG_NOT_READY")
   local civ=config:GetCivilizationTypeName()
   assert(type(civ)=="string" and #civ>0,"CIV_NOT_READY")
   assert(GameInfo and GameInfo.Traits and GameInfo.Traits[trait],"CARRIER_NOT_DEFINED")
   local found=false
   for row in GameInfo.CivilizationTraits() do
    assert(type(row.CivilizationType)=="string" and type(row.TraitType)=="string","BAD_TRAIT_ROW")
    if row.CivilizationType==civ and row.TraitType==trait then found=true end
   end
   r.status=found and "ENABLED" or "DISABLED";r.civilization=civ
   r.reason=found and "EXPLICIT_TRAIT_BINDING" or "NO_TRAIT_BINDING"
  end)
  if not ok then r.reason=tostring(err) end
  return r
 end
 local function sample(phase)
  local s={phase=phase,rows={},enabled=0,disabled=0,unknown=0,status="COMPLETE"}
  local ok,err=pcall(function()
   assert(Players,"PLAYERS_NOT_READY")
   local ids={}
   for pid in pairs(Players) do
    if type(pid)=="number" and pid>=0 and pid<math.huge and pid%1==0 then ids[#ids+1]=pid end
   end
   assert(#ids>0 and #ids<=128,"ROSTER_EMPTY_OR_TOO_LARGE")
   table.sort(ids)
   for _,pid in ipairs(ids) do
    local r=read(pid);s.rows[pid]=r
    local k=r.status:lower();s[k]=s[k]+1
    print("[SPC]["..P.VERSION.."][ELIGIBILITY]["..phase.."] player="..pid.." "..r.status.." "..r.reason)
   end
  end)
  if not ok then s.status="UNKNOWN";s.reason=tostring(err) end
  data.samples[phase]=s
 end
 local e=Events and Events.LoadScreenClose
 if e and type(e.Add)=="function" then
  local ok=pcall(e.Add,function() sample("LOAD_CLOSE") end)
  data.hooks.LoadScreenClose=ok and "REGISTERED" or "ERROR"
 else data.hooks.LoadScreenClose="ABSENT" end
 sample("INITIALIZE")
 -- No per-turn retries: preserve startup failures for this minimal diagnostic batch.
end
