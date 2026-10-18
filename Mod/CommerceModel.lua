-- Commerce owns only selected order and proven institution history. Current
-- ACTIVE, worker capacity, D/X and Gold are recomputed by the consumer.
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
function M.Validate(v,r)
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
 local t=v.reputation
 if t then
  assert(type(t)=='table' and t.version==1 and int(t.start) and int(t.cursor) and t.cursor>=t.start
   and int(t.age) and t.age<=40 and t.age<=t.cursor-t.start
   and type(t.receipt)=='string' and #t.receipt>0
   and (t.state=='COUNTING' or t.state=='DORMANT_OWNER' or t.state=='UNKNOWN_INTERVAL'),'COMMERCE_REPUTATION_INVALID')
  if r then
   assert(r.base.specialization=='COMMERCE' and r.investment and r.investment.investments[t.receipt]
    and r.base.first and t.start>=r.base.first.turn,'COMMERCE_REPUTATION_ORIGIN_UNAVAILABLE')
   local count=0;for _ in pairs(r.investment.investments)do count=count+1 end
   assert(count==3,'COMMERCE_REPUTATION_P4_REQUIRED')
  end
 end
 return v
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
 if t.state~='COUNTING' or t.age==40 then return n end
 local delta=turn-t.cursor
 if delta>1 then t.state='UNKNOWN_INTERVAL';return n end
 t.age=math.min(40,t.age+delta);t.cursor=turn
 return M.Validate(n)
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
