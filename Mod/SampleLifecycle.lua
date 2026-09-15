-- C2 transport and identity only. Producers/consumers retain their own yield semantics.
SPCSampleLifecycle={}
local L=SPCSampleLifecycle
local function count(P,k,n) if P.Count then P.Count(k..'_'..n) end end
local function integer(n) return type(n)=='number' and n>=0 and n%1==0 end
function L.Reference(c,d,row)
 local function a(v) local s=type(v)..':'..tostring(v);return (#s..':'..s):gsub('[%%,;]',function(x) return string.format('%%%02X',string.byte(x)) end) end
 return a(c:GetOwner())..a(c:GetID())..a(c:GetX())..a(c:GetY())..a(c:GetProperty('SPC_DEV_BINDING_B013_TOKEN'))
  ..a(d:GetID())..a(d:GetX())..a(d:GetY())..a(row.DistrictType)
end
function L.Live(P,pid,industry)
 local out={};local n=0
 for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan')
  local c=assert(d:GetCity(),'SAMPLE_CITY_UNAVAILABLE');local complete=d:IsComplete()
  assert(type(complete)=='boolean' and type(c:GetOwner())=='number','SAMPLE_DISTRICT_UNAVAILABLE')
  local row=assert(P.Info('Districts',d:GetType()),'SAMPLE_TYPE_UNAVAILABLE')
  if c:GetOwner()==pid and complete and (not industry or row.DistrictType=='DISTRICT_INDUSTRIAL_ZONE') then
   n=n+1;assert(n<=512,'SAMPLE_ROW_LIMIT')
   out[c:GetID()..':'..d:GetID()]={cityID=c:GetID(),id=d:GetID(),type=row.DistrictType,reference=L.Reference(c,d,row),district=d,city=c}
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
 if old and old.signature==value.signature then old.turn=p.Turn;respond('UNCHANGED');count(P,k,'duplicate');return false end
 data.samples[pid]=value;respond('ACCEPTED');count(P,k,'apply');return true
end
-- One player-wide batch in flight per producer; no cross-module lock or history.
function L.Client(P,k,action,public)
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
    if ack.status=='ACCEPTED' or ack.status=='UNCHANGED' then last=key end
   elseif c.clock-public.sentAt<5 and pending.Turn==Game.GetCurrentGameTurn() then
    count(P,k,'pending');return false
   else pending=nil;public.pending=0;ExposedMembers['SPC_C2_'..k..'_issued']=nil;count(P,k,'timeout') end
  end
  return true
 end
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
