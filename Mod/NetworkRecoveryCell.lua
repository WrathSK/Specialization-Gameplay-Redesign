-- Explicit callback-only commit mechanism. The future actual slot adapter owns
-- namespace, native reads/writes, carrier facts, lifecycle fences and work scope.
-- No native/global access, timer, event, transaction authority or idle blob cache.
SPCNetworkRecoveryCell={}
local M=SPCNetworkRecoveryCell
local function same(a,b,usage)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not(usage and k=='status')and not same(v,b[k])then return false end end
 for k in pairs(b)do if not(usage and k=='status')and a[k]==nil then return false end end;return true
end
local function reason(err)
 local ok,s=pcall(tostring,err);return ok and s:sub(1,180)or'NREC_CELL_UNKNOWN'
end
local function context(v)
 assert(type(v)=='table'and getmetatable(v)==nil,'NREC_CELL_REFERENCE_UNKNOWN')
 for k in pairs(v)do assert(k=='reference'or k=='stamp','NREC_CELL_REFERENCE_UNKNOWN')end
 assert(type(v.reference)=='string'and #v.reference>0 and #v.reference<=512
  and type(v.stamp)=='string'and #v.stamp>0 and #v.stamp<=512,'NREC_CELL_REFERENCE_UNKNOWN')
 return {reference=v.reference,stamp=v.stamp}
end
local function pending(family,sequence,receiver)
 local function frame(s)return #s..':'..s end
 return 'P'..frame('1')..frame(family)..frame(string.format('%.0f',sequence))..frame(receiver.reference)..frame(receiver.stamp)
end
local function pendingRead(raw)
 assert(#raw<=1100,'NREC_CELL_PENDING_INVALID');local at=2
 local function get()
  local c=raw:find(':',at,true);assert(c and c-at>=1 and c-at<=4,'NREC_CELL_PENDING_INVALID')
  local text=raw:sub(at,c-1);assert(text=='0'or text:match('^[1-9]%d*$'),'NREC_CELL_PENDING_INVALID')
  local n=tonumber(text);assert(n<=512 and c+n<=#raw,'NREC_CELL_PENDING_INVALID')
  local s=raw:sub(c+1,c+n);at=c+n+1;return s
 end
 assert(get()=='1','NREC_CELL_VERSION_UNSUPPORTED');local family,seq=get(),get()
 assert(seq:match('^[1-9]%d*$'),'NREC_CELL_SEQUENCE_UNKNOWN');local sequence=tonumber(seq)
 assert(sequence and sequence<9007199254740991 and sequence%1==0 and string.format('%.0f',sequence)==seq,'NREC_CELL_SEQUENCE_UNKNOWN')
 local receiver=context({reference=get(),stamp=get()});assert(at==#raw+1,'NREC_CELL_PENDING_INVALID')
 assert(pending(family,sequence,receiver)==raw,'NREC_CELL_PENDING_INVALID')
 return {state='INVALIDATED',family=family,sequence=sequence,receiver=receiver}
end
function M.New(family,readOnce,writeOnce,current)
 assert(family=='COMMERCE'or family=='CULTURE','NREC_CELL_FAMILY_INVALID')
 assert(type(readOnce)=='function'and type(writeOnce)=='function'and type(current)=='function','NREC_CELL_CALLBACK_REQUIRED')
 local C=assert(SPCNetworkRecoveryModel,'NREC_CELL_MODEL_REQUIRED')
 local d={reads=0,writes=0};local busy=false;local active
 local function now()return context(current())end
 local function check(receiver)assert(same(now(),receiver),'NREC_CELL_REFERENCE_CHANGED')end
 local function read()
  d.reads=d.reads+1;local raw=readOnce();assert(raw==nil or type(raw)=='string'and #raw<=C.MaxBytes+1,'NREC_CELL_VALUE_INVALID');return raw
 end
 local function parse(raw)
  if raw==nil then return {state='EMPTY',family=family,sequence=0}end
  if raw:sub(1,1)=='P'then local p=pendingRead(raw);assert(p.family==family,'NREC_CELL_FAMILY_CHANGED');return p end
  assert(raw:sub(1,1)=='A','NREC_CELL_PHASE_UNKNOWN');local value=C.Decode(raw:sub(2));assert(value.family==family,'NREC_CELL_FAMILY_CHANGED')
  return {state='APPLIED',family=family,sequence=value.sequence,receiver=value.receiver,value=value}
 end
 local function write(expected,value,receiver)
  check(receiver);assert(read()==expected,'NREC_CELL_STALE');check(receiver)
  d.writes=d.writes+1;local ok,why=pcall(writeOnce,value)
  local readable,actual=pcall(read)
  assert(ok,reason(why));assert(readable and actual==value,'NREC_CELL_WRITE_UNCONFIRMED');check(receiver)
 end
 function d.Read(shape)
  if busy or active then return {state='BUSY'}end
  busy=true;local ok,out=pcall(function()
   local receiver=now();local value=parse(read());check(receiver)
   if value.state=='APPLIED'then
    if not same(value.receiver,receiver)then return {state='STALE_REFERENCE',sequence=value.sequence}end
    if not same(value.value.shape,shape)then return {state='SHAPE_MISMATCH',sequence=value.sequence}end
    return {state='APPLIED',sequence=value.sequence,value=value.value}
   end
   return {state=value.state,sequence=value.sequence}
  end);busy=false
  if not ok then d.error=reason(out);return {state='UNAVAILABLE',reason=d.error}end
  d.error=nil;return out
 end
 function d.Begin(value,validateInputs)
  if busy or active then return nil,'NREC_CELL_BUSY'end
  busy=true;local ok,out=pcall(function()
   assert(type(validateInputs)=='function','NREC_CELL_INPUT_PROOF_REQUIRED')
   local wire=C.Encode(value);local candidate=C.Decode(wire);check(candidate.receiver)
   local oldRaw=read();local old=parse(oldRaw);check(candidate.receiver)
   assert(candidate.sequence==old.sequence+1,'NREC_CELL_SEQUENCE_CHANGED')
   for id,s in pairs(candidate.sources)do
    local function previous()
     assert(old.state=='APPLIED'and same(old.receiver,candidate.receiver),'NREC_CELL_RETAINED_PROOF_UNAVAILABLE')
     local prior=old.value.sources[id]
     assert(prior and prior.status~='UNKNOWN'and prior.reference==s.reference and prior.stamp==s.stamp,'NREC_CELL_RETAINED_FACT_CHANGED')
     return prior
    end
    if family=='COMMERCE'then
     for domain,row in pairs(s.domains or {})do if(row.status or s.status)=='RETAINED'then
      local prior=previous();local value=prior.domains[domain]
      assert(value and(value.status or prior.status)~='UNKNOWN'and same(value,row,true),'NREC_CELL_RETAINED_FACT_CHANGED')
     end end
    elseif s.status=='RETAINED'then assert(same(previous(),s,true),'NREC_CELL_RETAINED_FACT_CHANGED')end
   end
   assert(validateInputs(C.Decode(wire),old.value and C.Decode(oldRaw:sub(2))or nil)==true,'NREC_CELL_INPUT_UNCONFIRMED')
   check(candidate.receiver)
   local unchanged=false
   if old.state=='APPLIED'then
    local compare=C.Decode(wire);compare.sequence=old.sequence;unchanged='A'..C.Encode(compare)==oldRaw
   end
   local invalid=unchanged and oldRaw or pending(family,candidate.sequence,candidate.receiver)
   if not unchanged then write(oldRaw,invalid,candidate.receiver)end
   local ticket={};active={ticket=ticket,wire=wire,expected=invalid,receiver=candidate.receiver,shape=candidate.shape,
    sequence=unchanged and old.sequence or candidate.sequence,unchanged=unchanged}
   return ticket
  end);busy=false
  if not ok then active=nil;d.error=reason(out);return nil,d.error end
  d.error=nil;return out
 end
 function d.Finish(ticket,verifyApplied)
  if busy or not active or ticket~=active.ticket then return nil,'NREC_CELL_TICKET_INVALID'end
  busy=true;local a=active
  local ok,out=pcall(function()
   assert(type(verifyApplied)=='function','NREC_CELL_CARRIER_PROOF_REQUIRED');check(a.receiver)
   assert(read()==a.expected,'NREC_CELL_STALE');check(a.receiver)
   local shape={};for k,v in pairs(a.shape)do shape[k]=v end
   assert(verifyApplied(shape,context(a.receiver))==true,'NREC_CELL_CARRIER_UNCONFIRMED');check(a.receiver)
   if not a.unchanged then write(a.expected,'A'..a.wire,a.receiver)
   else assert(read()==a.expected,'NREC_CELL_STALE');check(a.receiver)end
   return {sequence=a.sequence,unchanged=a.unchanged}
  end)
  active=nil;busy=false
  if not ok then d.error=reason(out);return nil,d.error end
  d.error=nil;return out
 end
 function d.Abort(ticket)
  if busy or not active or ticket~=active.ticket then return false end
  active=nil;d.error='NREC_CELL_ABORTED';return true
 end
 function d.Status()return {active=active~=nil,busy=busy,reads=d.reads,writes=d.writes,error=d.error}end
 return d
end
