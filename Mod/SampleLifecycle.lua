-- C2 transport and identity only. Producers/consumers retain their own yield semantics.
SPCSampleLifecycle={}
local L=SPCSampleLifecycle
local function count(P,k,n) if P.Count then P.Count(k..'_'..n) end end
local function integer(n) return type(n)=='number' and n>=0 and n%1==0 end
local function reference(c,id,x,y,kind)
 local function a(v) local s=type(v)..':'..tostring(v);return (#s..':'..s):gsub('[%%,;]',function(x) return string.format('%%%02X',string.byte(x)) end) end
 return a(c:GetOwner())..a(c:GetID())..a(c:GetX())..a(c:GetY())..a(c:GetProperty('SPC_DEV_BINDING_B013_TOKEN'))
  ..a(id)..a(x)..a(y)..a(kind)
end
local function locatedReference(c,d,row)
 local id,x,y=d:GetID(),d:GetX(),d:GetY()
 return reference(c,id,x,y,row.DistrictType),x,y
end
function L.Reference(c,d,row)return (locatedReference(c,d,row))end
function L.AnchorReference(c,d,g)return reference(c,d.id,g.x,g.y,d.type)end
function L.Live(P,pid,industry)
 local out={};local n=0
 for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan')
  local c=assert(d:GetCity(),'SAMPLE_CITY_UNAVAILABLE');local complete=d:IsComplete()
  assert(type(complete)=='boolean' and type(c:GetOwner())=='number','SAMPLE_DISTRICT_UNAVAILABLE')
  local row=assert(P.Info('Districts',d:GetType()),'SAMPLE_TYPE_UNAVAILABLE')
  if c:GetOwner()==pid and complete and (not industry or P.Family(row.DistrictType)=='INDUSTRY') then
   n=n+1;assert(n<=512,'SAMPLE_ROW_LIMIT')
   local ref,x,y=locatedReference(c,d,row)
   out[c:GetID()..':'..d:GetID()]={cityID=c:GetID(),id=d:GetID(),type=row.DistrictType,reference=ref,x=x,y=y,district=d,city=c}
  end
 end
 return out
end
function L.Reset(data,k)
 local key='SPC_C2_'..k..'_generation';ExposedMembers[key]=(ExposedMembers[key] or 0)+1
 data.generation=ExposedMembers[key];data.samples={};data.seq={};data.responses={}
end
function L.Receive(P,data,k,pid,p,industry)
 count(P,k,'receive')
 local issued=ExposedMembers['SPC_C2_'..k..'_issued']
 if not data.ready or not P.IsTestPlayer(pid) or type(p)~='table' or not issued
  or issued.pid~=pid or issued.epoch~=p.ClientEpoch or issued.seq~=p.Seq or issued.generation~=p.Generation
  or p.Generation~=data.generation or not integer(p.Seq) or p.Turn~=Game.GetCurrentGameTurn() then count(P,k,'stale');return false end
 local ack=data.responses[pid]
 if ack and ack.epoch==p.ClientEpoch and p.Seq<=ack.seq then count(P,k,'duplicate');return false end
 local wasUnavailable=ack and ack.status=='UNAVAILABLE'
 local function respond(status) data.responses[pid]={epoch=p.ClientEpoch,seq=p.Seq,generation=p.Generation,status=status} end
 if p.Valid~=1 then respond('UNAVAILABLE');return false end
 local ok,value=pcall(function()
  assert(type(p.Data)=='string' and #p.Data<=60000 and integer(p.Count) and p.Count<=512,'SAMPLE_SIZE')
  local live=L.Live(P,pid,industry);local rows,canonical={},{};local n=0
  for line in p.Data:gmatch('[^;]+') do
   local cid,did,reference,x,y=line:match('^(%d+),(%d+),([^,]+),([^,]+),([^,]+)$')
   cid,did,x,y=tonumber(cid),tonumber(did),tonumber(x),tonumber(y)
   assert(cid and did and x and y and x==x and y==y and math.abs(x)<1e8 and math.abs(y)<1e8,'SAMPLE_VALUE')
   if industry then assert(x>=0 and x<=255 and x%1==0 and y==0,'SAMPLE_BASE_INVALID') end
   local key=cid..':'..did;local d=live[key];assert(d and d.reference==reference,'SAMPLE_REFERENCE_STALE')
   assert(not rows[key],'SAMPLE_DUPLICATE_ROW')
   rows[key]={cityID=cid,id=did,type=d.type,reference=reference,total=x,production=y,value=x}
   n=n+1;canonical[#canonical+1]=key..','..reference..','..string.format('%.17g',x)..','..string.format('%.17g',y)
  end
  assert(n==p.Count,'SAMPLE_PARTIAL');for key in pairs(live) do assert(rows[key],'SAMPLE_PARTIAL') end
  table.sort(canonical);return {rows=rows,signature=table.concat(canonical,';'),turn=p.Turn}
 end)
 if not ok then data.receiveErrors=data.receiveErrors or {};data.receiveErrors[pid]=tostring(value);respond('UNAVAILABLE');count(P,k,'stale');return false end
 data.receiveErrors=data.receiveErrors or {};data.receiveErrors[pid]=nil;data.seq[pid]=p.Seq
 local old=data.samples[pid]
 if old and old.signature==value.signature then old.turn=p.Turn;respond('UNCHANGED');count(P,k,'duplicate');return false,wasUnavailable and 'CONFIRMED_RECOVERED' or 'CONFIRMED_UNCHANGED' end
 local changed=L.ChangedCities(old,value,function(row)return table.concat({row.reference,row.total,row.production},',')end)
 data.samples[pid]=value;respond('ACCEPTED');count(P,k,'apply');return true,'CONFIRMED_CHANGED',changed
end
-- One player-wide batch in flight per producer; no cross-module lock or history.
function L.Client(P,k,action,public,options)
 local c={clock=0};local pending,epoch,generation,last,key,tries,seq
 local function reset()
  local e='SPC_C2_'..k..'_epoch';ExposedMembers[e]=(ExposedMembers[e] or 0)+1;epoch=ExposedMembers[e]
  ExposedMembers['SPC_C2_'..k..'_issued']=nil
  pending=nil;generation=nil;last=nil;key=nil;tries=0;seq=0;public.pending=0;public.state='RESET'
 end
 c.Reset=reset
 function c.Tick(dt) if type(dt)=='number' and dt>=0 then c.clock=c.clock+math.min(dt,10) end end
 function c.Before(data)
  count(P,k,'attempt')
  if generation~=data.generation then reset();generation=data.generation end
  if pending then
   local ack=data.responses[Game.GetLocalPlayer()]
   if ack and ack.epoch==epoch and ack.seq==pending.Seq and ack.generation==generation then
    public.state=ack.status;pending=nil;public.pending=0
    if ack.status=='ACCEPTED' or ack.status=='UNCHANGED' then last=key
    elseif ack.status=='UNAVAILABLE' and options and options.recoveryProof then last=nil end
   elseif c.clock-public.sentAt<5 and pending.Turn==Game.GetCurrentGameTurn() then
    count(P,k,'pending');return false
   else pending=nil;public.pending=0;ExposedMembers['SPC_C2_'..k..'_issued']=nil;count(P,k,'timeout') end
  end
  return true
 end
 -- D2 scheduling query only; ACK/retry ownership stays inside this client.
 function c.NeedsSample() return not pending and tries<3 and (not key or key~=last) end
 function c.Send(pid,data,valid,rows,n)
  local turn=Game.GetCurrentGameTurn();local payload=valid and table.concat(rows,';') or ''
  local signature=generation..':'..turn..':'..tostring(valid)..':'..payload
  if signature==last then count(P,k,'duplicate');return end
  if signature~=key then key=signature;tries=0 end
  if tries>=3 then public.state='RETRY_EXHAUSTED';return end
  tries=tries+1;seq=seq+1
  pending={OnStart='SPC_P0_Request',Action=action,Token=P.VERSION..':'..k..':'..epoch..':'..seq,
   ClientEpoch=epoch,Seq=seq,Generation=generation,Turn=turn,Valid=valid and 1 or 0,Count=valid and n or 0,Data=payload}
  ExposedMembers['SPC_C2_'..k..'_issued']={pid=pid,epoch=epoch,seq=seq,generation=generation}
  public.pending=1;public.sentAt=c.clock;public.requests=(public.requests or 0)+1;public.state='PENDING'
  count(P,k,'send');if tries>1 then count(P,k,'retry') end
  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,pending)
  if not ok then public.error=tostring(err);public.state='SEND_ERROR' end
 end
 function c.Close()
  if ExposedMembers['SPC_C2_'..k..'_epoch']==epoch then ExposedMembers['SPC_C2_'..k..'_issued']=nil end
  pending=nil;public.pending=0
 end
 reset();return c
end

-- UI producer work only. Encoded rows and ring membership are disposable scalars,
-- never saved authority; Gameplay still verifies each complete C2 batch.
function L.Sampler(P,industry,encode,limit)
 local s={};local owner,rows,index,full,work,serial,epoch,lastValid,lastWire,lastCount
 function s.Reset()
  L.InvalidateBaseProduction()
  owner=nil;rows=nil;index=nil;full=true;work={};serial=0;epoch={};lastValid=nil;lastWire=nil;lastCount=0
 end
 function s.All()L.InvalidateBaseProduction();serial=serial+1;full=true;work={}end
 function s.Owner(pid)
  if owner~=nil and integer(pid)and pid~=owner then return false end
  s.All();return true
 end
 local function coordinate(x,y)return integer(x)and integer(y)end
 local function at(x,y)return tostring(x)..':'..tostring(y)end
 function s.Plot(x,y)
  if not coordinate(x,y)or not rows or not index then s.All();return true end
  local hit=index[at(x,y)];if not hit then return false end
  L.InvalidateBaseProduction();serial=serial+1;for key in pairs(hit)do work[key]=true end;return true
 end
 function s.District(pid,did,cid,x,y)
  -- Other owners' districts may change our adjacency. Own membership is rebuilt;
  -- foreign metadata never authorizes dropping a nearby tracked district.
  if owner==nil or not integer(pid)or pid==owner then s.All();return true end
  return s.Plot(x,y)
 end
 function s.Pending()return full or next(work)~=nil end
 local function observe(pid,key,old)
  local districts=Players[pid]:GetDistricts()
  if type(districts.FindID)~='function'then return nil end -- old compatibility adapter
  local d=assert(districts:FindID(old.id),'SAMPLE_TRACKED_DISTRICT_UNKNOWN')
  local c=assert(d:GetCity(),'SAMPLE_CITY_UNAVAILABLE');local row=assert(P.Info('Districts',d:GetType()),'SAMPLE_TYPE_UNAVAILABLE')
  assert(c:GetOwner()==pid and c:GetID()==old.cityID and d:GetID()==old.id and d:IsComplete()==true,'SAMPLE_TRACKED_REFERENCE_CHANGED')
  local ref,x,y=locatedReference(c,d,row)
  assert(ref==old.reference and row.DistrictType==old.type and x==old.x and y==old.y,'SAMPLE_TRACKED_REFERENCE_CHANGED')
  return {cityID=old.cityID,id=old.id,type=old.type,reference=ref,x=x,y=y,district=d,city=c}
 end
 local function geometry(values)
  if not Map or type(Map.GetAdjacentPlot)~='function'then return nil end
  local map={}
  local function add(x,y,key)
   assert(coordinate(x,y),'SAMPLE_GEOMETRY_UNKNOWN');local k=at(x,y);map[k]=map[k]or {};map[k][key]=true
  end
  for key,r in pairs(values)do
   add(r.x,r.y,key)
   for direction=0,5 do local p=Map.GetAdjacentPlot(r.x,r.y,direction)
    if p then add(p:GetX(),p:GetY(),key)end
   end
  end
  return map
 end
 function s.Read(pid,turn)
  if owner~=pid then s.Reset();owner=pid end
  if not s.Pending()and lastValid~=nil then return lastValid,lastWire,lastCount end
  local ticket,lifetime=serial,epoch;local all=full;local todo=work;full=false;work={}
  local ok,value=pcall(function()
   local live
   if all or not rows then live=L.Live(P,pid,industry)
   else
    live={}
    for key in pairs(todo)do
     local old=assert(rows[key],'SAMPLE_TRACKED_ROW_UNKNOWN');local r=observe(pid,key,old)
     if not r then live=L.Live(P,pid,industry);all=true;break end
     live[key]=r
    end
   end
   local nextRows={};if not all and rows then for key,r in pairs(rows)do nextRows[key]=r end end
   for key,r in pairs(live)do
    local wire=encode(pid,r,turn);assert(type(wire)=='string','SAMPLE_WIRE_UNKNOWN')
    nextRows[key]={cityID=r.cityID,id=r.id,type=r.type,reference=r.reference,x=r.x,y=r.y,wire=wire}
   end
   local wires={};local n=0
   for _,r in pairs(nextRows)do n=n+1;assert(n<=512,'SAMPLE_ROW_LIMIT');wires[n]=r.wire end
   table.sort(wires);assert(#table.concat(wires,';')<=limit,'SAMPLE_SIZE')
   local nextIndex=index
   if all then nextIndex=geometry(nextRows)end
   return {rows=nextRows,index=nextIndex,wires=wires,n=n}
  end)
  -- Do not overwrite/clear a cause delivered by a native getter while reading.
  if ticket~=serial or lifetime~=epoch then return nil,nil,0,'SAMPLE_SUPERSEDED'end
  if not ok then lastValid=false;lastWire={};lastCount=0;return false,{},0,value end
  rows=value.rows;index=value.index;lastWire=value.wires;lastCount=value.n;lastValid=true
  return true,lastWire,lastCount
 end
 s.Reset();return s
end
-- Only verified coordinate signatures use ring filtering. Unknown scope retains
-- conservative full recovery; local technology/policy can change many adjacencies.
function L.BindSampler(P,s,bind,workers)
 for _,name in ipairs({'ImprovementAddedToMap','ImprovementRemovedFromMap','ImprovementChanged',
  'FeatureAddedToMap','FeatureRemovedFromMap','ResourceAddedToMap','ResourceRemovedFromMap'})do
  bind(name,function(x,y)s.Plot(x,y)end)
 end
 for _,name in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged'})do
  bind(name,function(pid,did,cid,x,y)s.District(pid,did,cid,x,y)end)
 end
 for _,name in ipairs({'CityProductionCompleted','CityAddedToMap','CityRemovedFromMap','GovernorAssigned','GovernorChanged','GovernorEstablished',
  'GovernorPromoted','GovernmentChanged','GovernmentPolicyChanged','ResearchCompleted','CivicCompleted'})do
  bind(name,function(pid)s.Owner(pid)end)
 end
 if workers then for _,name in ipairs({'CityWorkerChanged','CityFocusChanged','CityPopulationChanged'})do bind(name,function(pid)s.Owner(pid)end)end end
 -- This native event has owner/city only; a foreign border change may alter
 -- an adjacent local district, so do not pretend its geometry is known.
 for _,name in ipairs({'CityTransfered','CityTileOwnershipChanged'})do bind(name,s.All)end
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do
  bind(name,function(x,y,id,owner)
   local row=P.Info('Buildings',id)
   if row and type(row.BuildingType)=='string'and row.BuildingType:match('^BUILDING_SPC_')then return end
   -- Buildings can change policy/modifier-derived adjacency. Scope only known owner.
   s.Owner(owner)
  end)
 end
end
-- Compare only already validated scalar payloads. No native sampling, and no UI
-- supplied affected-city claim becomes gameplay authority.
function L.ChangedCities(old,value,signature)
 if not old then return nil end
 local cities={}
 for key,row in pairs(value.rows)do local prior=old.rows[key]
  if not prior or signature(row)~=signature(prior)then cities[row.cityID]=true end
 end
 for key,row in pairs(old.rows)do if not value.rows[key]then cities[row.cityID]=true end end
 return cities
end

-- Narrow cross-UI reuse: one native BASE Production value, never effect/role
-- authority. The stamp contains only current scalar producer/write lifetimes.
function L.InvalidateBaseProduction()
 local c=ExposedMembers.SPC_C2_BaseProduction
 if c and c.schema==1 then c.revision=c.revision+1;c.rows={};c.count=0;c.textBytes=0 end
end
local function productionStamp(P,turn)
 local e=ExposedMembers;local g=e.SPC_P0
 local i,x=g and g.IndustrySupport,g and g.ResearchCross
 if not g or g.Version~=P.VERSION or not i or not x or not i.ready or not x.ready
  or not integer(turn)then return nil end
 local fields={e.SPC_C2_industry_generation,e.SPC_C2_cross_generation,
  e.SPC_C2_industry_epoch,e.SPC_C2_cross_epoch}
 for n=1,4 do if not integer(fields[n])then return nil end end
 if i.generation~=fields[1]or x.generation~=fields[2]then return nil end
 fields[5]=turn;fields[6]=e.SPC_RuntimeUIRevision or 0
 fields[7]=i.sampleRevision or 0;fields[8]=x.sampleRevision or 0
 for n=5,8 do if not integer(fields[n])then return nil end end
 return table.concat(fields,':')
end
function L.ReadBaseProduction(P,pid,r,districtType,yieldIndex,turn)
 local function native()
  if P.Count then P.Count('adj_base_capture')end
  return Map.GetPlot(r.x,r.y):GetAdjacencyYield(pid,r.cityID,districtType,yieldIndex)
 end
 local function indexScalar(v)return type(v)=='number'and v==v and math.abs(v)<1e8 or type(v)=='string'and #v<=256 end
 local stamp=productionStamp(P,turn)
 if not stamp or not integer(pid)or not integer(r.id)or not integer(r.cityID)
  or not integer(r.x)or not integer(r.y)or type(r.reference)~='string'or type(r.type)~='string'
  or not indexScalar(districtType)or not indexScalar(yieldIndex)then return native()end
 local e=ExposedMembers;local c=e.SPC_C2_BaseProduction
 if not c or c.schema~=1 or c.version~=P.VERSION then
  c={schema=1,version=P.VERSION,authority='NATIVE_SAMPLE_ONLY',revision=0,rows={},count=0,textBytes=0}
  e.SPC_C2_BaseProduction=c
 end
 if c.stamp~=stamp then c.stamp=stamp;c.rows={};c.count=0;c.textBytes=0 end
 local key=tostring(pid)..':'..tostring(r.id)
 local prior=c.rows[key]
 local function same(row)
  return row and row.reference==r.reference and row.city==r.cityID and row.x==r.x and row.y==r.y
   and row.type==r.type and row.districtType==districtType and row.yieldIndex==yieldIndex
 end
 if same(prior)and type(prior.value)=='number'and prior.value==prior.value and math.abs(prior.value)<1e8 then
  if P.Count then P.Count('adj_base_hit')end;return prior.value
 end
 local revision=c.revision
 local value=native() -- a thrown/unknown read is never installed or retried here
 if e.SPC_C2_BaseProduction==c and c.revision==revision and productionStamp(P,turn)==stamp
  and type(value)=='number'and value==value and math.abs(value)<1e8 and type(r.reference)=='string'then
  local bytes=#r.reference+(type(r.type)=='string'and #r.type or 0)
  local oldBytes=prior and prior.textBytes or 0
  if (prior or c.count<512)and c.textBytes-oldBytes+bytes<=262144 then
   c.rows[key]={reference=r.reference,city=r.cityID,x=r.x,y=r.y,type=r.type,
    districtType=districtType,yieldIndex=yieldIndex,value=value,textBytes=bytes}
   if not prior then c.count=c.count+1 end;c.textBytes=c.textBytes-oldBytes+bytes
  end
 end
 return value
end
