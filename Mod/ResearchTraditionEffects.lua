-- F2: transient, module-owned Science percentage. Store remains the age authority.
SPCResearchTraditionEffects={}
local M=SPCResearchTraditionEffects
local amounts={5,10,15,20,25}
local function name(n)return 'BUILDING_SPC_RESEARCH_TRADITION_'..n end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore)
 local data={ready=false,changes=0};shared.ResearchTraditionEffects=data
 local pending={};local busy=false;local definitions
 local function key(c)return c:GetOwner()..':'..c:GetID()end
 local function defs()
  if definitions then return definitions end
  local out={}
  for _,n in ipairs(amounts)do
   local row=assert(P.Info('Buildings',name(n)),'TRADITION_CARRIER_MISSING')
   assert((row.InternalOnly==true or row.InternalOnly==1) and row.PrereqDistrict=='DISTRICT_CITY_CENTER'
    and row.CitizenSlots==0 and row.Housing==0,'TRADITION_CARRIER_INVALID')
   out[#out+1]={amount=n,id=row.Index}
  end
  definitions=out;return out
 end
 local function desired(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'TRADITION_OWNER_UNKNOWN')
  local f=shared.EffectiveFacts.Read(pid,c)
  if f.specialization~='RESEARCH' then return 0 end
  assert(f.activeStatus=='KNOWN' and type(f.active)=='number','TRADITION_ACTIVE_UNKNOWN')
  if f.active<4 then return 0 end
  local t=store.ReadTradition(pid,c)
  if not t or t.state~='COUNTING' then return 0 end
  assert(t.cursor==Game.GetCurrentGameTurn(),'TRADITION_INTERVAL_NOT_CURRENT')
  local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()]
  return SPCResearchTradition.Shadow(t.age,assert(speed and speed.CostMultiplier,'TRADITION_SPEED_UNKNOWN')/100)
 end
 local function installed(c)
  local b=c:GetBuildings();local out={};local sum=0
  for _,d in ipairs(defs())do
   local has=P.HasBuilding(b,d.id);assert(type(has)=='boolean','TRADITION_CARRIER_UNKNOWN')
   local pillaged=false
   if has then pillaged=b:IsPillaged(d.id);assert(type(pillaged)=='boolean','TRADITION_CARRIER_STATE_UNKNOWN')end
   out[#out+1]={id=d.id,amount=d.amount,has=has,pillaged=pillaged}
   if has and not pillaged then sum=sum+d.amount end
  end
  return out,sum
 end
 function data.Read(pid,c)
  local want=desired(pid,c);local _,have=installed(c)
  return want,have
 end
 function data.Update(pid,c)
  if not data.ready or busy then return end
  busy=true
  local ok,err=pcall(function()
   local want=desired(pid,c);local rows=installed(c) -- validate all inputs before writing
   for _,v in ipairs(rows)do
    if v.has and (v.amount~=want or v.pillaged)then
     P.RemoveBuilding(c:GetBuildings(),v.id)
     assert(P.HasBuilding(c:GetBuildings(),v.id)==false,'TRADITION_REMOVE_FAILED')
     v.has=false;data.changes=data.changes+1
    end
   end
   for _,v in ipairs(rows)do if v.amount==want and not v.has then
    P.CreateBuilding(c:GetBuildQueue(),v.id)
    assert(P.HasBuilding(c:GetBuildings(),v.id)==true and c:GetBuildings():IsPillaged(v.id)==false,'TRADITION_CREATE_FAILED')
    data.changes=data.changes+1
   end end
  end)
  busy=false
  if not ok then data.lastError={city=key(c),reason=tostring(err)}
  elseif data.lastError and data.lastError.city==key(c) then data.lastError=nil end
 end
 function data.Mark(pid)
  if P.IsTestPlayer(pid)then pending[pid]=true end
 end
 function data.Flush()
  if not data.ready or busy or not next(pending)then return end
  local work=pending;pending={}
  for pid in pairs(work)do
   local ok,err=pcall(store.VisitTradition,pid,function(c)data.Update(pid,c)end)
   if not ok then data.lastError={city='STORE',reason=tostring(err)}
   elseif data.lastError and data.lastError.city=='STORE' then data.lastError=nil end
  end
 end
 local function hook(n,fn)local e=P.Field(Events,n);if e and e.Add then e.Add(fn)end end
 hook('LoadScreenClose',function()
  definitions=nil;pending={};data.lastError=nil;data.ready=true
  for pid in pairs(Players)do data.Mark(pid)end
  data.Flush()
 end)
 -- Age is settled by Store's earlier listener. No new world/district scan.
 for _,event in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted'})do hook(event,data.Mark)end
 hook('GameCoreEventPublishComplete',data.Flush)
 store.RegisterExit('ResearchTradition',function(c,loss)
  local ids={};for _,n in ipairs(amounts)do ids[#ids+1]=name(n)end
  store.RemoveOwned(c,loss,ids)
  data.lastError=nil -- one bounded diagnostic slot, never permanent state
 end)
end
