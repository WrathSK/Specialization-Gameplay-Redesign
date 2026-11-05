-- Commerce owns only selected order and proven institution history. Current
-- ACTIVE, worker capacity, D/X and Gold are recomputed by the consumer.
if not SPCTurnLedger then include('TurnLedger')end
SPCCommerceModel={}
local M=SPCCommerceModel
local domains={DISTRICT_CAMPUS=true,DISTRICT_THEATER=true,DISTRICT_INDUSTRIAL_ZONE=true,DISTRICT_HOLY_SITE=true,DISTRICT_HARBOR=true}
local function copy(v)if type(v)~='table'then return v end;local n={};for k,x in pairs(v)do n[k]=copy(x)end;return n end
M.Copy=copy
local function int(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
-- v0.1 Commerce has no speed scaling. Require an actual current speed row;
-- a coincidental CostMultiplier=100 is not proof of Standard speed.
function M.IsStandardSpeed()
 local config=GameConfiguration
 if not config or type(config.GetGameSpeedType)~='function'then return false,'COMMERCE_SPEED_UNKNOWN'end
 local ok,id=pcall(config.GetGameSpeedType)
 if not ok or id==nil then return false,'COMMERCE_SPEED_UNKNOWN'end
 local readable,row=pcall(function()return GameInfo and GameInfo.GameSpeeds and GameInfo.GameSpeeds[id]end)
 if not readable or not row or type(row.GameSpeedType)~='string'then return false,'COMMERCE_SPEED_UNKNOWN'end
 if row.GameSpeedType~='GAMESPEED_STANDARD'then return false,'COMMERCE_STANDARD_SPEED_ONLY'end
 return true,'COMMERCE_STANDARD_SPEED'
end
function M.New(owner)
 assert(int(owner),'COMMERCE_OWNER_INVALID');return {version=1,owner=owner,selected={}}
end
function M.ValidateConfiguration(v,r)
 assert(type(v)=='table' and v.version==1 and int(v.owner) and type(v.selected)=='table','COMMERCE_STATE_INVALID')
 local seen,n={},0
 for i,domain in pairs(v.selected)do
  assert(int(i) and i>=1 and i<=5 and domains[domain] and not seen[domain],'COMMERCE_SELECTION_INVALID');seen[domain]=true;n=n+1
 end
 assert(n==#v.selected,'COMMERCE_SELECTION_GAP')
 for i=1,n do assert(domains[v.selected[i]],'COMMERCE_SELECTION_GAP')end
 if r then
  local a=r.loss and r.loss.target or r.current or r.origin
  assert(a and v.owner==a.owner,'COMMERCE_OWNER_REFERENCE_CHANGED')
 end
 return v
end
function M.ValidateReputation(t,r)
 if t then
  assert(type(t)=='table' and t.version==1 and int(t.start) and int(t.cursor) and t.cursor>=t.start
   and int(t.age) and t.age<=40 and t.age<=t.cursor-t.start
   and type(t.receipt)=='string' and #t.receipt>0
   and (t.state=='COUNTING' or t.state=='DORMANT_OWNER' or t.state=='UNKNOWN_INTERVAL'),'COMMERCE_REPUTATION_INVALID')
  if r and t.qualification then SPCRestructuringModel.ValidateQualification(t.qualification,r,t.receipt,t.start,'COMMERCE')
  elseif r then
   assert(r.base.specialization=='COMMERCE' and r.investment and r.investment.investments[t.receipt]
    and r.base.first and t.start>=r.base.first.turn,'COMMERCE_REPUTATION_ORIGIN_UNAVAILABLE')
   local count=0;for _ in pairs(r.investment.investments)do count=count+1 end
   assert(count==3,'COMMERCE_REPUTATION_P4_REQUIRED')
  end
 end
 return t
end
function M.Validate(v,r)
 M.ValidateConfiguration(v,r);M.ValidateReputation(v.reputation,r)
 return v
end
-- Read-only evidence is separate from usable R. A failed shape check is not a
-- permanent-corruption verdict,and a missing dependency/parent proof is not R0.
function M.ReputationInput(v,r,isolation,deferred)
 local function unknown(reason)return {status='UNKNOWN',reason=reason or 'COMMERCE_REPUTATION_UNKNOWN'}end
 if deferred then return unknown('COMMERCE_REPUTATION_DEFERRED_LIFECYCLE')end
 local t=v and v.reputation
 if isolation then
  if isolation.status=='CHECK_FAILED'then
   local ok,why=pcall(M.ValidateReputation,t)
   if not ok and type(why)=='string'and why:match('COMMERCE_REPUTATION_INVALID$')then
    return {status='SEVERE_LEAF',reason='COMMERCE_REPUTATION_INVALID'}
   end
  end
  return unknown(type(isolation.reason)=='string'and isolation.reason:sub(1,180)or nil)
 end
 local ok,why=pcall(M.ValidateReputation,t,r)
 if not ok then return unknown('COMMERCE_REPUTATION_VALIDATION_UNAVAILABLE')end
 if not t then return {status='ABSENT',reason='COMMERCE_REPUTATION_NOT_ESTABLISHED'}end
 return {status='CONFIRMED',age=t.age,state=t.state,reason='COMMERCE_REPUTATION_CONFIRMED'}
end
function M.ReputationUse(input,f)
 local history=type(input)=='table'and input.status or 'UNKNOWN'
 local function result(status,reason,effective,age)
  return {status=status,reason=reason,historyStatus=history,effective=effective,age=age}
 end
 if type(f)~='table'or f.activeStatus~='KNOWN'or not int(f.active)or f.active>4
  or not int(f.potential)or f.potential>4 or f.active>f.potential or type(f.specialization)~='string'then
  return result('UNKNOWN','COMMERCE_REPUTATION_QUALIFICATION_UNKNOWN')
 end
 if f.specialization~='COMMERCE'or f.active<4 then
  return result('NOT_APPLICABLE','COMMERCE_REPUTATION_ACTIVE_IV_REQUIRED',0)
 end
 if history=='CONFIRMED'and int(input.age)and input.age<=40 and input.state=='COUNTING'then
  return result('CONFIRMED','COMMERCE_REPUTATION_CONFIRMED',input.age,input.age)
 elseif history=='SEVERE_LEAF'and input.reason=='COMMERCE_REPUTATION_INVALID'then
  return result('POLICY_ZERO','COMMERCE_REPUTATION_ISOLATED_LEAF_POLICY',0)
 end
 return result('UNKNOWN',history=='ABSENT'and 'COMMERCE_REPUTATION_REQUIRED_HISTORY_MISSING'
  or history=='CONFIRMED'and 'COMMERCE_REPUTATION_NOT_COUNTING'
  or type(input)=='table'and input.reason or 'COMMERCE_REPUTATION_UNKNOWN')
end
function M.ReputationText(use)
 if use and use.status=='POLICY_ZERO'then
  return '商业信誉记录异常；本次按无信誉加成政策计价（R=0），原记录未改写。'
 elseif use and use.status=='NOT_APPLICABLE'then
  return '当前不使用商业信誉加成（需商业 ACTIVE IV）。'
 elseif use and use.status=='CONFIRMED'then
  return '商业信誉 '..use.age..'；当前使用 '..use.effective
 end
 return '商业信誉暂不可确认；不据此新增信誉加成。'
end
function M.Select(v,domain,enabled)
 M.Validate(v);assert(domains[domain] and type(enabled)=='boolean','COMMERCE_SELECTION_REQUEST_INVALID')
 local n=copy(v);local found
 for i,name in ipairs(n.selected)do if name==domain then found=i;break end end
 if enabled and not found then n.selected[#n.selected+1]=domain
 elseif not enabled and found then table.remove(n.selected,found)end
 return M.Validate(n)
end
function M.EffectiveSelections(v,capacity)
 M.Validate(v);assert(int(capacity),'COMMERCE_CAPACITY_UNKNOWN')
 local out={effective={},suspended={}}
 for i,domain in ipairs(v.selected)do local list=i<=capacity and out.effective or out.suspended;list[#list+1]=domain end
 return out
end
function M.BeginReputation(v,turn,receipt)
 M.Validate(v);assert(not v.reputation and int(turn) and type(receipt)=='string' and #receipt>0,'COMMERCE_REPUTATION_START_REJECTED')
 local n=copy(v);n.reputation={version=1,start=turn,cursor=turn,age=0,receipt=receipt,state='COUNTING'}
 return M.Validate(n)
end
function M.Exit(v)
 M.Validate(v);return M.New(v.owner) -- actual Identity exit, never temporary ACTIVE loss
end
function M.Advance(v,turn,identity)
 M.Validate(v);assert(int(turn) and type(identity)=='string','COMMERCE_REPUTATION_TURN_UNKNOWN')
 if identity~='COMMERCE'then return M.Exit(v)end
 local n=copy(v);local t=n.reputation;if not t then return n end
 assert(turn>=t.cursor,'COMMERCE_REPUTATION_TURN_REVERSED')
 if t.state=='DORMANT_OWNER' or t.state=='COUNTING'and t.age==40 then return n end
 local cursor,credit,skipped=SPCTurnLedger.Advance(t.cursor,turn,t.state=='COUNTING',t.state=='UNKNOWN_INTERVAL')
 t.age=math.min(40,t.age+credit);t.cursor=cursor;t.state='COUNTING'
 return M.Validate(n),skipped
end
function M.OwnerChanged(v,owner,turn)
 M.Validate(v);assert(int(owner) and int(turn),'COMMERCE_OWNER_UNKNOWN')
 local n=copy(v);n.owner=owner;n.selected={}
 if n.reputation then
  assert(turn>=n.reputation.cursor,'COMMERCE_REPUTATION_TURN_REVERSED')
  n.reputation.cursor=turn
  if n.reputation.state=='COUNTING'then n.reputation.state='DORMANT_OWNER'end
 end
 return M.Validate(n)
end
function M.Resume(v,owner,turn)
 M.Validate(v);assert(int(owner) and int(turn),'COMMERCE_OWNER_UNKNOWN')
 local n=copy(v);n.owner=owner;n.selected={}
 if n.reputation then
  assert(turn>=n.reputation.cursor,'COMMERCE_REPUTATION_TURN_REVERSED')
  n.reputation.cursor=turn -- never count an unsupported Owner's interval
  if n.reputation.state=='DORMANT_OWNER'then n.reputation.state='COUNTING'end
 end
 return M.Validate(n)
end
