-- B036: background UI raw/base adjacency sampling; never opens a panel.
include('Probe')
local P=SPCP0
local active,busy=false,false
local sent,hooks={},{}
local sequence=0
local initialized=false
local function refresh()
 if not active or busy then return end
 local shared=ExposedMembers.SPC_P0
 if not shared or shared.Version~=P.VERSION or not shared.IndustrySupport or not shared.IndustrySupport.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 busy=true
 local ok,err=pcall(function()
  local live={}
  for _,d in Players[pid]:GetDistricts():Members() do
   local row=P.Info('Districts',d:GetType());local c=d:GetCity()
   if row and row.DistrictType=='DISTRICT_INDUSTRIAL_ZONE' and c and c:GetOwner()==pid and d:IsComplete() then
    local id=c:GetID();local k=pid..':'..id..':'..d:GetID();live[k]=true
    local good,value=pcall(function() return Map.GetPlot(d:GetX(),d:GetY()):GetAdjacencyYield(pid,id,d:GetType(),P.Info('Yields','YIELD_PRODUCTION').Index) end)
    local valid=good and type(value)=='number' and value>=0 and value<=255 and value%1==0
    local n=valid and value or -1
    if sent[k]~=n then
     sequence=sequence+1
     -- Mark before request to prevent synchronous publish recursion; retry send errors.
     local prior=sent[k];sent[k]=n
     local delivered,message=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
      {OnStart='SPC_P0_Request',Action='INDUSTRY_BASE',Token=P.VERSION..':industry:'..sequence,CityID=id,DistrictID=d:GetID(),BaseProduction=n})
     if not delivered then sent[k]=prior;error(message) end
    end
   end
  end
  for k in pairs(sent) do if not live[k] then sent[k]=nil end end
 end)
 if ok then initialized=true end
 busy=false
 if not ok then print('[SPC][B036][BASE_UI_ERROR] '..tostring(err)) end
end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
end
ContextPtr:SetInitHandler(function()
 if active then return end;active=true
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','LoadScreenClose','PlayerTurnActivated'}) do bind(name,refresh) end
 -- Retry initialization only until first successful sample; no per-frame world scan.
 bind('SystemUpdateUI',function() if not initialized then refresh() end end)
 refresh()
end)
ContextPtr:SetShutdown(function() active=false;for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end;hooks={} end)
