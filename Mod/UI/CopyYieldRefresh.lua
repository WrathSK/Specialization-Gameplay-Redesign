include('Probe')
include('SampleLifecycle')
local P=SPCP0;local busy=false;local hooks={};local dirty=true;local seenGeneration,seenTurn,seenWrites
local public={state='LOADED',attempts=0,requests=0};ExposedMembers.SPC_CopyBackground=public
local client=SPCSampleLifecycle.Client(P,'copy','COPY_YIELD_SAMPLE',public)
local function refresh()
 local shared=ExposedMembers.SPC_P0;local data=shared and shared.CopyYields
 if busy or not shared or shared.Version~=P.VERSION or not data or not data.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 public.attempts=public.attempts+1
 if not client.Before(data) then return end
 local turn=Game.GetCurrentGameTurn();local writes=ExposedMembers.SPC_RuntimeUIRevision or 0
 if data.generation~=seenGeneration or turn~=seenTurn or writes~=seenWrites then dirty=true end
 if not dirty and not client.NeedsSample() then return end
 dirty=false;seenGeneration=data.generation;seenTurn=turn;seenWrites=writes
 busy=true;local rows={};local n=0
 local ok,err=pcall(function()
  for _,r in pairs(SPCSampleLifecycle.Live(P,pid,false)) do
    local sum,prod=0,0
    for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}) do
     local v=r.district:GetYield(P.Info('Yields','YIELD_'..y).Index)
     assert(type(v)=='number' and v==v and math.abs(v)<1e8,'COPY_UI_YIELD_UNKNOWN')
     sum=sum+v;if y=='PRODUCTION' then prod=v end
    end
    n=n+1;rows[#rows+1]=r.cityID..','..r.id..','..r.reference..','..string.format('%.17g',sum)..','..string.format('%.17g',prod)
  end
  table.sort(rows)
 end)
 public.error=not ok and tostring(err) or nil;public.count=n
 client.Send(pid,data,ok,rows,n);busy=false
end
local function safe() local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err) end end
local function bind(name,fn) local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end end
local function mark() dirty=true end
ContextPtr:SetInitHandler(function()
 -- Generic notifications only drain marked work / bounded C2 pending state.
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','SystemUpdateUI'}) do bind(name,safe) end
 for _,name in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged',
  'CityProductionCompleted','ImprovementAddedToMap','ImprovementRemovedFromMap',
  'FeatureAddedToMap','FeatureRemovedFromMap','CityTileOwnershipChanged','CityAddedToMap','CityRemovedFromMap','CityTransfered',
  'GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityWorkerChanged','CityFocusChanged',
  'CityPopulationChanged','GovernmentChanged','GovernmentPolicyChanged','ResearchCompleted','CivicCompleted',
  'ResourceAddedToMap','ResourceRemovedFromMap'}) do bind(name,mark) end
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'}) do
  bind(name,function(x,y,id)
   local row=P.Info('Buildings',id)
   if row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_') then return end
   dirty=true
  end)
 end
 bind('PlayerTurnActivated',safe) -- turn key: at most one full sample fallback per local turn
 bind('LoadScreenClose',function() client.Reset();dirty=true;safe() end)
 ContextPtr:SetUpdate(function(dt) client.Tick(dt) end) -- scalar timeout clock, never reads game state or sends
 safe()
end)
ContextPtr:SetShutdown(function()
 client.Close();ContextPtr:ClearUpdate()
 for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end
 if ExposedMembers.SPC_CopyBackground==public then ExposedMembers.SPC_CopyBackground=nil end
end)
