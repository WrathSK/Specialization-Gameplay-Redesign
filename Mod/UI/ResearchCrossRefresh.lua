include('Probe')
include('SampleLifecycle')
include('ResearchCrossSample')
local P=SPCP0;local busy=false;local hooks={};local dirty=true;local seenGeneration,seenTurn
local public={state='LOADED',attempts=0,requests=0};ExposedMembers.SPC_ResearchCrossBackground=public
local client=SPCSampleLifecycle.Client(P,'cross','RESEARCH_CROSS_SAMPLE',public)
local function refresh()
 local shared=ExposedMembers.SPC_P0;local data=shared and shared.ResearchCross
 if busy or not shared or shared.Version~=P.VERSION or not data or not data.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 local turn=Game.GetCurrentGameTurn()
 if data.generation~=seenGeneration or turn~=seenTurn then dirty=true end
 if not dirty and public.pending==0 and not client.NeedsSample() then return end
 public.attempts=public.attempts+1
 if not client.Before(data) then return end
 if not dirty and not client.NeedsSample() then return end
 dirty=false;seenGeneration=data.generation;seenTurn=turn
 busy=true;local rows={};local n=0
 local ok,err=pcall(function()
  local replaces=SPCResearchCrossSample.Replacements(P)
  for _,r in pairs(SPCSampleLifecycle.Live(P,pid,false)) do
   local d=r.district;local pillaged=d:IsPillaged();assert(type(pillaged)=='boolean','CROSS_PILLAGE_UNKNOWN')
   local fields={r.cityID,r.id,r.reference,pillaged and '1' or '0'}
   local domain=SPCResearchCrossModel.Domain(r.type,replaces)
   for _,y in ipairs(SPCResearchCrossModel.Yields) do
    local value=0
    if domain and not pillaged then value=Map.GetPlot(d:GetX(),d:GetY()):GetAdjacencyYield(pid,r.cityID,d:GetType(),P.Info('Yields','YIELD_'..y).Index) end
    assert(type(value)=='number' and value==value and math.abs(value)<1e8,'CROSS_BASE_UNAVAILABLE')
    fields[#fields+1]=string.format('%.17g',value)
   end
   n=n+1;rows[#rows+1]=table.concat(fields,',')
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
 for _,name in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired',
  'CityProductionCompleted','ImprovementAddedToMap','ImprovementRemovedFromMap',
  'FeatureAddedToMap','FeatureRemovedFromMap','CityTileOwnershipChanged','CityAddedToMap','CityRemovedFromMap','CityTransfered',
  'GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted',
  'GovernmentChanged','GovernmentPolicyChanged','ResearchCompleted','CivicCompleted',
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
 if ExposedMembers.SPC_ResearchCrossBackground==public then ExposedMembers.SPC_ResearchCrossBackground=nil end
end)
