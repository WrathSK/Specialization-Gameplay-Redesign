-- D2: ephemeral batch indexes, never persisted or shared across writes/batches.
SPCRuntimeWork={}
function SPCRuntimeWork.New(P,shared)
 local b={};local facts,byPlayer,live={}, {}, {}
 function b.Facts(pid,c)
  facts[pid]=facts[pid] or {};local t=facts[pid];local id=c:GetID()
  if not t[id] then t[id]=shared.EffectiveFacts.Read(pid,c) end
  return t[id]
 end
 function b.Districts(pid,c)
  if not byPlayer[pid] then
   local t={}
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan')
    local city=assert(d:GetCity(),'SAMPLE_CITY_UNAVAILABLE')
    if city:GetOwner()==pid then local id=city:GetID();t[id]=t[id] or {};t[id][#t[id]+1]=d end
   end
   byPlayer[pid]=t -- publish the index only after complete enumeration
  end
  return ipairs(byPlayer[pid][c:GetID()] or {})
 end
 function b.Live(pid,industry)
  local k=pid..':'..tostring(industry)
  if not live[k] then live[k]=SPCSampleLifecycle.Live(P,pid,industry) end
  return live[k]
 end
 return b
end
-- Only named publisher metadata is interpreted as a scope. Native event argument
-- layouts are not guessed here; their wrappers below explicitly identify player.
function SPCRuntimeWork.Player(scope,pid)
 return type(scope)~='table' or scope.player==nil or scope.player==pid
end
-- Only the named, synchronous investment result may narrow these two writers.
-- Native hooks/player scopes remain unchanged. Facts belong to this writer's
-- batch; the next writer must revalidate rather than reuse post-write inputs.
function SPCRuntimeWork.InvestmentCity(P,shared,scope,batch)
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local e=scope.investment;local pid=scope.player
 assert(type(e)=='table' and e.status=='COMMITTED' and e.cause=='INVESTMENT_COMMITTED'
  and type(pid)=='number' and pid==e.player and P.IsTestPlayer(pid),'INVESTMENT_SCOPE_UNKNOWN')
 assert(type(e.city)=='number' and e.city>=0 and e.city%1==0 and type(e.anchor)=='table'
  and e.anchor.owner==pid and e.anchor.cityID==e.city and type(e.anchor.token)=='string' and #e.anchor.token>0
  and type(e.receipt)=='string' and #e.receipt>0 and type(e.unitUID)=='string'
  and type(e.revision)=='number' and e.revision>=2 and e.revision<=4 and e.revision%1==0,'INVESTMENT_EVIDENCE_UNKNOWN')
 local player=assert(Players[pid],'INVESTMENT_PLAYER_UNAVAILABLE')
 local city=assert(player:GetCities():FindID(e.city),'INVESTMENT_CITY_UNAVAILABLE')
 assert(same(e.reference,{owner=city:GetOwner(),cityID=city:GetID(),x=city:GetX(),y=city:GetY()})
  and city:GetOwner()==pid,'INVESTMENT_REFERENCE_CHANGED')
 local f=batch.Facts(pid,city)
 assert(same(e.anchor,{owner=f.owner,cityID=f.cityID,token=f.token,first=f.first,specialization=f.specialization})
  and not f.investmentPending and f.investmentCount>=e.revision-1,'INVESTMENT_BINDING_CHANGED')
 assert(same(e.reference,{owner=city:GetOwner(),cityID=city:GetID(),x=city:GetX(),y=city:GetY()}),'INVESTMENT_CHANGED_DURING_READ')
 return city
end
function SPCRuntimeWork.Hook(P,source,name,fn)
 local e=P.Field(source,name);if not e or not e.Add then return end
 local lastTurn={}
 e.Add(function(pid,...)
  if name=='BuildingAddedToMap' or name=='BuildingRemovedFromMap' then
   local y,building,owner=...
   local row=P.Info('Buildings',building)
   if row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_') then return end
   if P.Observe then P.Observe('dispatch',name) end
   fn({player=type(owner)=='number' and owner or nil});return
  end
  if name=='PlayerTurnActivated' then
   if type(pid)~='number' then return end
   local turn=Game.GetCurrentGameTurn();if lastTurn[pid]==turn then return end
   lastTurn[pid]=turn;if P.Observe then P.Observe('dispatch',name) end;fn({player=pid});return
  end
  -- Civ VI native city/worker/governor events start with player ID. Events with
  -- plot-first or transfer signatures intentionally retain a full safety scope.
  if P.Observe then P.Observe('dispatch',name) end
  if name:match('^Governor') or name=='CityWorkerChanged' or name=='CityFocusChanged'
   or name=='CityPopulationChanged' then fn({player=pid});return end
  fn()
 end)
end
